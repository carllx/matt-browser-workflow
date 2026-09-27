#!/usr/bin/env python3
"""
scripts/check_evidence.py

一个无模型调用、无第三方依赖的确定性 IDE Evidence 完整性检查器 (Feasibility Probe)。
核心原则：
  1. 外部契约 (Contract) 具有唯一权威性 (External Contract Authority)；
  2. 证据包 (Evidence) 仅描述实际发生的事实，不得自行定义或改写验收标准；
  3. 严格执行三分法 (PASS / FAIL / UNVERIFIED)，核心不变式：Missing evidence != PASS。

退出码 (Exit Codes):
  0: PASS (证据完整且全部满足外部契约要求)
  1: FAIL (硬性失败、SHA 不匹配、被拒、超时或存在伪造声明)
  2: UNVERIFIED (证据不足，契约所要求数据缺失或未完成，但未构成硬失败)
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

PROVES_SCOPE = [
    "Candidate SHA 与 External Contract Expected SHA 精确匹配 (Exact candidate SHA match)",
    "Evidence Provenance 与 Candidate SHA 精确绑定 (Provenance matches candidate SHA)",
    "External Contract 规定的 Required Checks 全部存在且通过 (Contract-required checks verified)",
    "每项 Check 的 Terminal State 为成功终态 (Recorded terminal states verified)",
    "External Contract 规定的 Required Acceptance 全部存在且裁决为 PASS (Contract-required acceptance verified)",
]

DOES_NOT_PROVE_SCOPE = [
    "命令本身的底层语义是否完全正确 (Semantic correctness of commands)",
    "ChatGPT Project / Browser 侧是否真实加载了对应规则 (Rules loaded in Browser)",
    "Agent 认知与推理质量 (Agent reasoning validity)",
    "Browser 与 IDE 的实际协作流畅度与人工中继成本 (Collaboration friction & relay cost)",
    "是否符合 Matt 哲学或无过度设计 (Matt philosophy & non-overdesign compliance)",
    "全局工作流验证 (NOT 'Workflow verified')",
]


def evaluate_contract_and_evidence(
    contract: Optional[Dict[str, Any]],
    evidence: Optional[Dict[str, Any]],
    expected_sha_override: Optional[str] = None,
    load_error: Optional[str] = None,
) -> Tuple[str, List[str]]:
    """
    对 Evidence 是否满足独立的 External Contract 执行确定性事实判断。
    
    返回:
      (verdict, findings)
      verdict 必须是: PASS | FAIL | UNVERIFIED
    """
    findings: List[str] = []

    # 0. 检查 fixture / payload 是否具有合法的 contract 与 evidence 边界
    if load_error:
        findings.append(load_error)
        return "FAIL", findings

    if contract is None or not isinstance(contract, dict):
        findings.append(
            "Missing valid external contract object. "
            "Self-certifying payloads without independent contract authority are strictly rejected."
        )
        return "FAIL", findings

    if evidence is None or not isinstance(evidence, dict):
        findings.append("Missing valid evidence payload object.")
        return "FAIL", findings

    # 1. 外部契约权威性提取 (External Contract Authority)
    expected_sha = expected_sha_override or contract.get("expected_candidate_sha")
    if not expected_sha:
        findings.append("External contract missing 'expected_candidate_sha'.")
        return "UNVERIFIED", findings

    required_checks = contract.get("required_checks", [])
    if not isinstance(required_checks, list):
        findings.append("External contract 'required_checks' must be a list.")
        return "UNVERIFIED", findings

    required_acceptance = contract.get("required_acceptance", [])
    if not isinstance(required_acceptance, list):
        findings.append("External contract 'required_acceptance' must be a list.")
        return "UNVERIFIED", findings

    # 2. 检查 Evidence 基本事实要素是否存在
    candidate_sha = evidence.get("candidate_sha")
    if not candidate_sha:
        findings.append("Evidence missing 'candidate_sha'.")
        return "UNVERIFIED", findings

    provenance = evidence.get("provenance")
    if not provenance or not isinstance(provenance, dict) or not provenance.get("commit_sha"):
        findings.append("Evidence missing 'provenance' or 'provenance.commit_sha'.")
        return "UNVERIFIED", findings

    check_runs = evidence.get("check_runs")
    if check_runs is None or not isinstance(check_runs, list):
        findings.append("Evidence missing 'check_runs' list.")
        return "UNVERIFIED", findings

    # 3. 权威 SHA 比对
    # Evidence 不得自定 expected_sha；必须精确匹配外部契约
    if candidate_sha != expected_sha:
        findings.append(
            f"Candidate SHA mismatch: evidence declared '{candidate_sha}', "
            f"external contract expected '{expected_sha}'."
        )
        return "FAIL", findings

    prov_sha = provenance.get("commit_sha")
    if prov_sha != candidate_sha:
        findings.append(
            f"Stale evidence provenance: provenance commit '{prov_sha}' != candidate SHA '{candidate_sha}'."
        )
        return "FAIL", findings

    # 4. Check Runs 状态比对（对照外部契约要求）
    claimed_overall = str(evidence.get("claimed_overall_status", "")).upper()
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
            pass  # 明确成功
        else:
            incomplete_checks.append(f"{req} (state={state}, exit_code={exit_code})")

    # 5. Acceptance Records 检查（对照外部契约要求）
    acceptance_records = evidence.get("acceptance_records", [])
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

    # 核心负例防护：若外部契约要求项缺失，但 evidence 声称整体 PASS，判为虚假声称 -> FAIL
    if (missing_checks or missing_acceptance) and claimed_overall == "PASS":
        findings.append(
            f"False claim: evidence claimed overall PASS, but external contract required items are missing: "
            f"missing_checks={missing_checks}, missing_acceptance={missing_acceptance}."
        )

    if findings:
        return "FAIL", findings

    # 7. 证据不足裁决 (UNVERIFIED) - Missing evidence != PASS
    if missing_checks:
        findings.append(f"Missing external contract required check(s): {missing_checks}.")
    if missing_acceptance:
        findings.append(f"Missing external contract required acceptance record(s): {missing_acceptance}.")
    if incomplete_checks:
        findings.append(f"Incomplete terminal states: {incomplete_checks}.")

    if findings:
        return "UNVERIFIED", findings

    # 8. 成功裁决 (PASS)
    findings.append("Candidate SHA matches external contract exactly.")
    findings.append("Evidence provenance strictly corresponds to candidate.")
    findings.append(
        f"All {len(required_checks)} contract-required checks verified (terminal_state=success, exit_code=0)."
    )
    if required_acceptance:
        findings.append(
            f"All {len(required_acceptance)} contract-required acceptance records verified (verdict=PASS)."
        )
    return "PASS", findings


def print_report(case_name: str, verdict: str, findings: List[str], verbose: bool = False):
    print(f"=== Evidence Check Report: {case_name} ===")
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


def load_fixture_contract_and_evidence(
    fixture_path: Path,
) -> Tuple[Optional[Dict[str, Any]], Optional[Dict[str, Any]], str, Optional[str]]:
    """
    加载测试用例 fixture。
    严格要求顶层必须同时包含 'contract' 和 'evidence' 对象。
    绝对不从旧式 payload 自动推导 contract，拒绝自证明。
    """
    with open(fixture_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    if not isinstance(data, dict):
        return None, None, "FAIL", "Fixture root must be a JSON object."

    expected_verdict = data.get("meta_expected_verdict", "UNKNOWN")

    if "contract" not in data or "evidence" not in data:
        err = (
            "Invalid fixture structure: missing top-level 'contract' and/or 'evidence' object. "
            "Self-certifying payloads without independent external contract are strictly rejected."
        )
        return None, None, expected_verdict, err

    if not isinstance(data["contract"], dict) or not isinstance(data["evidence"], dict):
        err = "Invalid fixture structure: top-level 'contract' and 'evidence' must both be JSON objects."
        return None, None, expected_verdict, err

    return data["contract"], data["evidence"], expected_verdict, None


def run_self_test(fixtures_dir: Path) -> bool:
    """运行内建自测，验证三分法：GOOD -> PASS, BAD -> FAIL, INCOMPLETE -> UNVERIFIED"""
    print(">>> Running Self-Test Suite on Fixtures in:", fixtures_dir)
    fixtures = sorted([f for f in fixtures_dir.glob("*.json") if not f.name.startswith("sample_")])
    if not fixtures:
        print("ERROR: No test fixtures found in", fixtures_dir)
        return False

    all_passed = True
    print(f"{'Fixture File':<54} | {'Expected':<12} | {'Actual':<12} | {'Status'}")
    print("-" * 87)

    for fix in fixtures:
        contract, evidence, expected_verdict, load_err = load_fixture_contract_and_evidence(fix)
        actual_verdict, findings = evaluate_contract_and_evidence(contract, evidence, load_error=load_err)

        status = "MATCH" if actual_verdict == expected_verdict else "MISMATCH"
        if status != "MATCH":
            all_passed = False
        print(f"{fix.name:<54} | {expected_verdict:<12} | {actual_verdict:<12} | {status}")

    print("-" * 87)
    if all_passed:
        print("RESULT: ALL FIXTURE TESTS PASSED (External Contract Authority & Trichotomy verified).")
    else:
        print("RESULT: SOME FIXTURE TESTS FAILED.")
    return all_passed


def main():
    parser = argparse.ArgumentParser(
        description="Deterministic IDE Evidence Checker (External Contract Authority)"
    )
    parser.add_argument("--contract", type=str, help="Path to external contract JSON")
    parser.add_argument("--evidence", type=str, help="Path to evidence JSON")
    parser.add_argument("--fixture", type=str, help="Path to test case JSON containing both contract and evidence")
    parser.add_argument("--expected-sha", type=str, help="Override expected candidate SHA")
    parser.add_argument("--self-test", action="store_true", help="Run self-test against fixtures directory")
    parser.add_argument("--fixtures-dir", type=str, default="scripts/fixtures", help="Fixtures directory path")
    parser.add_argument("--verbose", "-v", action="store_true", help="Print detailed scope boundaries")

    args = parser.parse_args()

    if args.self_test:
        fix_dir = Path(args.fixtures_dir)
        success = run_self_test(fix_dir)
        sys.exit(0 if success else 1)

    contract: Optional[Dict[str, Any]] = None
    evidence: Optional[Dict[str, Any]] = None
    load_err: Optional[str] = None
    case_name = "check"

    if args.contract and args.evidence:
        with open(args.contract, "r", encoding="utf-8") as f:
            contract = json.load(f)
        with open(args.evidence, "r", encoding="utf-8") as f:
            evidence = json.load(f)
        case_name = f"{Path(args.contract).name} + {Path(args.evidence).name}"
    elif args.fixture:
        fix_path = Path(args.fixture)
        if not fix_path.exists():
            print(f"Error: Fixture file not found: {fix_path}", file=sys.stderr)
            sys.exit(1)
        contract, evidence, _, load_err = load_fixture_contract_and_evidence(fix_path)
        case_name = fix_path.name
        if args.contract:
            with open(args.contract, "r", encoding="utf-8") as f:
                contract = json.load(f)
    else:
        parser.print_help()
        sys.exit(1)

    verdict, findings = evaluate_contract_and_evidence(
        contract, evidence, args.expected_sha, load_error=load_err
    )
    print_report(case_name, verdict, findings, verbose=args.verbose)

    # Exit code mapping: PASS -> 0, FAIL -> 1, UNVERIFIED -> 2
    if verdict == "PASS":
        sys.exit(0)
    elif verdict == "FAIL":
        sys.exit(1)
    else:
        sys.exit(2)


if __name__ == "__main__":
    main()
