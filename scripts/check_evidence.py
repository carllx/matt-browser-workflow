#!/usr/bin/env python3
"""
scripts/check_evidence.py

一个无模型调用、无第三方依赖的确定性 IDE Evidence 完整性检查器 (Feasibility Probe)。
用于机器验证 Evidence Bundle 的事实要素：SHA 匹配、终态记录、Provenance、执行完整性。

退出码 (Exit Codes):
  0: PASS (证据完整且全部通过)
  1: FAIL (硬性失败、SHA 不匹配、被拒、超时或存在伪造声明)
  2: UNVERIFIED (证据不足，数据缺失或未完成，且未构成硬失败)
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

PROVES_SCOPE = [
    "Candidate SHA 与 Expected SHA 精确匹配 (Exact candidate SHA match)",
    "Evidence Provenance 与 Candidate SHA 精确绑定 (Provenance matches candidate SHA)",
    "声明的 Required Checks 记录全部存在 (Required check records exist)",
    "每项 Check 的 Terminal State 为可验证终态 (Recorded terminal states verified)",
    "Required Acceptance 记录存在且裁决为明确 PASS (Acceptance records present & pass)",
]

DOES_NOT_PROVE_SCOPE = [
    "命令本身的底层语义是否完全正确 (Semantic correctness of commands)",
    "ChatGPT Project / Browser 侧是否真实加载了对应规则 (Rules loaded in Browser)",
    "Agent 认知与推理质量 (Agent reasoning validity)",
    "Browser 与 IDE 的实际协作流畅度与人工中继成本 (Collaboration friction & relay cost)",
    "是否符合 Matt 哲学或无过度设计 (Matt philosophy & non-overdesign compliance)",
    "全局工作流验证 (NOT 'Workflow verified')",
]


def evaluate_evidence(
    bundle: Dict[str, Any], expected_sha: Optional[str] = None
) -> Tuple[str, List[str]]:
    """
    对 Evidence Bundle 执行确定性事实判断。
    
    返回:
      (verdict, findings)
      verdict 必须是: PASS | FAIL | UNVERIFIED
    """
    findings: List[str] = []
    
    # 1. 确定期望 SHA
    target_sha = expected_sha or bundle.get("expected_sha")
    candidate_sha = bundle.get("candidate_sha")
    
    # 2. 检查基本要素是否存在（判断数据是否足以开始）
    if not candidate_sha:
        findings.append("Missing candidate_sha in bundle.")
        return "UNVERIFIED", findings
        
    if not target_sha:
        findings.append("Missing expected_sha (neither specified via CLI nor in bundle).")
        return "UNVERIFIED", findings

    provenance = bundle.get("provenance")
    if not provenance or not isinstance(provenance, dict) or not provenance.get("commit_sha"):
        findings.append("Missing provenance or provenance.commit_sha.")
        return "UNVERIFIED", findings

    required_checks = bundle.get("required_checks")
    if required_checks is None or not isinstance(required_checks, list):
        findings.append("Missing or invalid required_checks declaration.")
        return "UNVERIFIED", findings

    check_runs = bundle.get("check_runs")
    if check_runs is None or not isinstance(check_runs, list):
        findings.append("Missing check_runs list.")
        return "UNVERIFIED", findings

    # 3. 硬核事实比对：SHA 匹配
    if candidate_sha != target_sha:
        findings.append(f"Candidate SHA mismatch: declared '{candidate_sha}', expected '{target_sha}'.")
        return "FAIL", findings

    prov_sha = provenance.get("commit_sha")
    if prov_sha != candidate_sha:
        findings.append(f"Stale evidence provenance: provenance SHA '{prov_sha}' != candidate SHA '{candidate_sha}'.")
        return "FAIL", findings

    # 4. Check Runs 状态索引与分析
    claimed_overall = bundle.get("claimed_overall_status", "").upper()
    runs_by_name = {c.get("name"): c for c in check_runs if isinstance(c, dict) and "name" in c}

    missing_checks = []
    failed_checks = []
    denied_checks = []
    timeout_checks = []
    incomplete_checks = []

    for req in required_checks:
        if req not in runs_by_name:
            missing_checks.append(req)
            continue
            
        run = runs_by_name[req]
        state = str(run.get("terminal_state", "")).lower()
        exit_code = run.get("exit_code")

        if state == "failure" or (exit_code is not None and exit_code != 0):
            failed_checks.append(f"{req} (state={state}, exit_code={exit_code})")
        elif state == "denied":
            denied_checks.append(f"{req} (tool denied)")
        elif state == "timeout":
            timeout_checks.append(f"{req} (execution timeout)")
        elif state == "success" and exit_code == 0:
            pass  # 正确通过
        else:
            incomplete_checks.append(f"{req} (state={state}, exit_code={exit_code})")

    # 5. Acceptance Records 检查
    required_acceptance = bundle.get("required_acceptance", [])
    acceptance_records = bundle.get("acceptance_records", [])
    acc_by_name = {a.get("name"): a for a in acceptance_records if isinstance(a, dict) and "name" in a}

    missing_acceptance = []
    failed_acceptance = []
    for acc in required_acceptance:
        if acc not in acc_by_name:
            missing_acceptance.append(acc)
            continue
        rec = acc_by_name[acc]
        verdict = str(rec.get("verdict", "")).upper()
        if verdict != "PASS":
            failed_acceptance.append(f"{acc} (verdict={verdict})")

    # 6. 硬失败裁决 (FAIL)
    if failed_checks:
        findings.append(f"Required command(s) failed: {', '.join(failed_checks)}.")
    if denied_checks:
        findings.append(f"Tool denied in required check(s): {', '.join(denied_checks)}.")
    if timeout_checks:
        findings.append(f"Timeout occurred in required check(s): {', '.join(timeout_checks)}.")
    if failed_acceptance:
        findings.append(f"Required acceptance check(s) rejected: {', '.join(failed_acceptance)}.")

    # 核心负例防护：若缺失 check 或 acceptance，但 bundle 声称 PASS，判为伪造/虚假陈述 -> FAIL
    if (missing_checks or missing_acceptance) and claimed_overall == "PASS":
        findings.append(
            f"False claim: bundle claimed overall PASS, but required items are missing: "
            f"missing_checks={missing_checks}, missing_acceptance={missing_acceptance}."
        )

    if findings:
        return "FAIL", findings

    # 7. 证据不足裁决 (UNVERIFIED) - Missing evidence != PASS
    if missing_checks:
        findings.append(f"Missing required check execution results: {missing_checks}.")
    if missing_acceptance:
        findings.append(f"Missing required acceptance records: {missing_acceptance}.")
    if incomplete_checks:
        findings.append(f"Incomplete terminal states: {incomplete_checks}.")

    if findings:
        return "UNVERIFIED", findings

    # 8. 成功裁决 (PASS)
    findings.append("All candidate SHAs match exact target.")
    findings.append("Evidence provenance strictly corresponds to candidate.")
    findings.append(f"All {len(required_checks)} required checks passed with terminal_state=success and exit_code=0.")
    if required_acceptance:
        findings.append(f"All {len(required_acceptance)} required acceptance records verified with verdict=PASS.")
    return "PASS", findings


def run_checker(fixture_path: Path, expected_sha: Optional[str] = None) -> Tuple[str, List[str]]:
    with open(fixture_path, "r", encoding="utf-8") as f:
        bundle = json.load(f)
    return evaluate_evidence(bundle, expected_sha)


def print_report(fixture_name: str, verdict: str, findings: List[str], verbose: bool = False):
    print(f"=== Evidence Check Report: {fixture_name} ===")
    print(f"Verdict: {verdict}")
    print("Findings:")
    for f in findings:
        print(f"  - {f}")
    if verbose:
        print("\nScope Boundaries:")
        print("  What this checker PROVES:")
        for p in PROVES_SCOPE:
            print(f"    [+] {p}")
        print("  What this checker does NOT PROVE:")
        for d in DOES_NOT_PROVE_SCOPE:
            print(f"    [-] {d}")
    print("-" * 50)


def run_self_test(fixtures_dir: Path) -> bool:
    """运行内建自测，验证三分法：GOOD -> PASS, BAD -> FAIL, INCOMPLETE -> UNVERIFIED"""
    print(">>> Running Self-Test Suite on Fixtures in:", fixtures_dir)
    fixtures = sorted(fixtures_dir.glob("*.json"))
    if not fixtures:
        print("ERROR: No fixtures found in", fixtures_dir)
        return False

    all_passed = True
    print(f"{'Fixture File':<42} | {'Expected':<12} | {'Actual':<12} | {'Status'}")
    print("-" * 75)

    for fix in fixtures:
        with open(fix, "r", encoding="utf-8") as f:
            data = json.load(f)
        expected_verdict = data.get("meta_expected_verdict", "UNKNOWN")
        actual_verdict, findings = evaluate_evidence(data)
        
        status = "MATCH" if actual_verdict == expected_verdict else "MISMATCH"
        if status != "MATCH":
            all_passed = False
        print(f"{fix.name:<42} | {expected_verdict:<12} | {actual_verdict:<12} | {status}")

    print("-" * 75)
    if all_passed:
        print("RESULT: ALL FIXTURE TESTS PASSED (Trichotomy verified: PASS, FAIL, UNVERIFIED).")
    else:
        print("RESULT: SOME FIXTURE TESTS FAILED.")
    return all_passed


def main():
    parser = argparse.ArgumentParser(description="Deterministic IDE Evidence Checker")
    parser.add_argument("--fixture", type=str, help="Path to evidence JSON fixture")
    parser.add_argument("--expected-sha", type=str, help="Expected candidate SHA override")
    parser.add_argument("--self-test", action="store_true", help="Run self-test against fixtures directory")
    parser.add_argument("--fixtures-dir", type=str, default="scripts/fixtures", help="Fixtures directory path")
    parser.add_argument("--verbose", "-v", action="store_true", help="Print detailed scope boundaries")

    args = parser.parse_args()

    if args.self_test:
        fix_dir = Path(args.fixtures_dir)
        success = run_self_test(fix_dir)
        sys.exit(0 if success else 1)

    if not args.fixture:
        parser.print_help()
        sys.exit(1)

    fixture_path = Path(args.fixture)
    if not fixture_path.exists():
        print(f"Error: Fixture file not found: {fixture_path}", file=sys.stderr)
        sys.exit(1)

    verdict, findings = run_checker(fixture_path, args.expected_sha)
    print_report(fixture_path.name, verdict, findings, verbose=args.verbose)

    # Exit code mapping: PASS -> 0, FAIL -> 1, UNVERIFIED -> 2
    if verdict == "PASS":
        sys.exit(0)
    elif verdict == "FAIL":
        sys.exit(1)
    else:
        sys.exit(2)


if __name__ == "__main__":
    main()
