#!/usr/bin/env python3
"""
scripts/test_deployment_integrity.py

用于验证部署加固评测基准 D1、D2、D3 的确定性测试套件 (Deployment Integrity Test Suite)。
验证项目：
- D1 负例契约：Runtime Integrity 漂移时串行 Fail-Closed 阻断，下游调用为 0；
- D2 正例算法：PROJECT_REPO 合法替换归一化零误报，且防篡改检测有效；
- D3 部署包：确定性构建（重复构建哈希相同）与不可变 Git 交叉核验。
"""

import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

# 引入构建脚本中的核心逻辑
sys.path.insert(0, str(Path(__file__).resolve().parent))
from build_deployment_bundle import (
    DELIVERABLE_FILES,
    BundleError,
    build_bundle,
    compute_sha256,
    extract_version_from_instructions,
    run_git,
    verify_bundle,
)


def normalize_instructions_for_verification(content: str, placeholder: str = "PROJECT_REPO: <SET_PER_CHATGPT_PROJECT>") -> str:
    """
    按规范 §7.1 与 Playbook §20.B 实现的 Instructions 归一化比对逻辑：
    将 PROJECT_REPO 的具体仓库绑定行归一化为标准占位符，其余内容保持逐字比对。
    """
    normalized_lines = []
    for line in content.splitlines():
        if re.match(r"^PROJECT_REPO:\s*.+$", line.strip()):
            normalized_lines.append(placeholder)
        else:
            normalized_lines.append(line)
    return "\n".join(normalized_lines) + ("\n" if content.endswith("\n") else "")


class MockBrowserRuntime:
    """
    模拟 Browser Lead 执行启动自检协议 (Startup & Runtime Integrity Barrier)
    """
    def __init__(self, canonical_instructions: str, canonical_sources: dict):
        self.canonical_instructions = canonical_instructions
        self.canonical_sources = canonical_sources
        self.downstream_calls = []

    def call_downstream_tool(self, tool_name: str, args: dict):
        """记录对目标仓库 live state（如 Issue/Branch/Tracker）的调用"""
        self.downstream_calls.append({"tool": tool_name, "args": args})

    def execute_startup_barrier(self, loaded_instructions: str, loaded_sources: dict) -> dict:
        """
        按顺序执行启动强屏障 (Ordered Dependency Barrier)：
        1. 归一化 PROJECT_REPO 并核验 Instructions 与 Sources
        2. 存在漂移 -> FAIL-CLOSED 阻断，不执行任何下游调用
        3. 核验通过 -> 放行，进入 Step 2 (Bounded Project Sync)
        """
        normalized_loaded = normalize_instructions_for_verification(loaded_instructions)
        normalized_canonical = normalize_instructions_for_verification(self.canonical_instructions)

        loaded_hash = compute_sha256(normalized_loaded.encode("utf-8"))
        canonical_hash = compute_sha256(normalized_canonical.encode("utf-8"))

        # 检查 Instructions
        if loaded_hash != canonical_hash:
            return {
                "verdict": "FAIL_CLOSED_DRIFT",
                "reason": "Instructions 内容发生未授权漂移",
                "downstream_calls_count": len(self.downstream_calls),
                "user_recovery_hint": "请从 GitHub Release 重新下载官方部署压缩包覆盖恢复",
            }

        # 检查 Sources
        for name, canonical_content in self.canonical_sources.items():
            if loaded_sources.get(name) != canonical_content:
                return {
                    "verdict": "FAIL_CLOSED_DRIFT",
                    "reason": f"Sources 文件 '{name}' 内容不匹配",
                    "downstream_calls_count": len(self.downstream_calls),
                    "user_recovery_hint": "请从 GitHub Release 重新下载官方部署压缩包覆盖恢复",
                }

        # 校验通过，允许进入下游现场读取
        self.call_downstream_tool("read_project_issue_list", {"state": "open"})
        self.call_downstream_tool("get_project_active_branch", {})

        return {
            "verdict": "PASS",
            "reason": "Runtime Integrity Verified",
            "downstream_calls_count": len(self.downstream_calls),
        }


def test_d1_ordered_barrier():
    """测试 D1：漂移时 Fail-Closed 串行阻断，下游零调用"""
    print("\n[TEST D1] 运行 D1 串行屏障行为断言测试...")
    canonical_instr = Path("chatgpt-project/project-instructions.md").read_text(encoding="utf-8")
    canonical_sources = {
        "browser-agent-playbook.md": Path("chatgpt-project/browser-agent-playbook.md").read_text(encoding="utf-8"),
        "browser-workflow-spec.md": Path("chatgpt-project/browser-workflow-spec.md").read_text(encoding="utf-8"),
    }

    # 负例 1：Instructions 中依赖锁定 MAT_REF 被私自篡改
    tampered_instr = canonical_instr.replace("8b78b531ab965735c5dc74f6f7a219e1e37326df", "0000000000000000000000000000000000000000")
    runtime1 = MockBrowserRuntime(canonical_instr, canonical_sources)
    res1 = runtime1.execute_startup_barrier(tampered_instr, canonical_sources)

    assert res1["verdict"] == "FAIL_CLOSED_DRIFT", f"期望阻断，但返回: {res1}"
    assert res1["downstream_calls_count"] == 0, f"违反串行屏障！下游调用次数应为 0，实际为: {res1['downstream_calls_count']}"
    assert "重新下载" in res1["user_recovery_hint"]
    print("  [OK] 负例 1 (MAT_REF 篡改): 成功阻断且下游调用计数 == 0")

    # 负例 2：Playbook 内容发生漂移
    tampered_sources = dict(canonical_sources)
    tampered_sources["browser-agent-playbook.md"] = canonical_sources["browser-agent-playbook.md"] + "\n# 未授权附加规则"
    runtime2 = MockBrowserRuntime(canonical_instr, canonical_sources)
    res2 = runtime2.execute_startup_barrier(canonical_instr, tampered_sources)

    assert res2["verdict"] == "FAIL_CLOSED_DRIFT"
    assert res2["downstream_calls_count"] == 0
    print("  [OK] 负例 2 (Playbook 漂移): 成功阻断且下游调用计数 == 0")

    print("[PASS] D1 场景行为契约测试全部通过！")


def test_d2_placeholder_normalization():
    """测试 D2：PROJECT_REPO 归一化零误报与防篡改断言"""
    print("\n[TEST D2] 运行 D2 PROJECT_REPO 归一化比对测试...")
    canonical_instr = Path("chatgpt-project/project-instructions.md").read_text(encoding="utf-8")
    canonical_sources = {
        "browser-agent-playbook.md": Path("chatgpt-project/browser-agent-playbook.md").read_text(encoding="utf-8"),
        "browser-workflow-spec.md": Path("chatgpt-project/browser-workflow-spec.md").read_text(encoding="utf-8"),
    }

    # 正例 1：用户合法替换为具体 HTTPS 目标仓库
    bound_instr_1 = canonical_instr.replace(
        "PROJECT_REPO: <SET_PER_CHATGPT_PROJECT>",
        "PROJECT_REPO: https://github.com/carllx/matt-browser-workflow"
    )
    runtime1 = MockBrowserRuntime(canonical_instr, canonical_sources)
    res1 = runtime1.execute_startup_barrier(bound_instr_1, canonical_sources)

    assert res1["verdict"] == "PASS", f"合法绑定应通过，但返回: {res1}"
    assert res1["downstream_calls_count"] == 2, "合法通过后应顺利执行后续同步"
    print("  [OK] 正例 1 (HTTPS 仓库绑定): 归一化判定 PASS，零误报")

    # 正例 2：用户合法替换为 SSH 格式仓库
    bound_instr_2 = canonical_instr.replace(
        "PROJECT_REPO: <SET_PER_CHATGPT_PROJECT>",
        "PROJECT_REPO: git@github.com:my-org/my-app.git"
    )
    runtime2 = MockBrowserRuntime(canonical_instr, canonical_sources)
    res2 = runtime2.execute_startup_barrier(bound_instr_2, canonical_sources)

    assert res2["verdict"] == "PASS"
    print("  [OK] 正例 2 (SSH 仓库绑定): 归一化判定 PASS，零误报")

    # 边界对照反例：用户修改了 PROJECT_REPO，但同时偷偷删改了正文规则
    tampered_bound = bound_instr_1.replace("WORKFLOW_REF: v0.17", "WORKFLOW_REF: v0.18-fake")
    runtime3 = MockBrowserRuntime(canonical_instr, canonical_sources)
    res3 = runtime3.execute_startup_barrier(tampered_bound, canonical_sources)

    assert res3["verdict"] == "FAIL_CLOSED_DRIFT"
    assert res3["downstream_calls_count"] == 0
    print("  [OK] 对照反例 (绑定同时篡改版本): 精准识别并拦截，防篡改有效")

    print("[PASS] D2 场景归一化与防篡改测试全部通过！")


def test_d3_bundle_determinism_and_verification():
    """测试 D3：确定性构建与 Git 权威来源交叉核验"""
    print("\n[TEST D3] 运行 D3 确定性构建与 Git 交叉核验测试...")
    temp_dir = tempfile.mkdtemp(prefix="mbw_test_d3_")
    try:
        dir_a = os.path.join(temp_dir, "build_a")
        dir_b = os.path.join(temp_dir, "build_b")

        # 1. 连续两次构建 HEAD，验证确定性
        res_a = build_bundle(ref="HEAD", output_dir=dir_a)
        res_b = build_bundle(ref="HEAD", output_dir=dir_b)

        assert res_a["bundle_sha256"] == res_b["bundle_sha256"], (
            f"确定性构建失败！两次构建哈希不一致:\n  A: {res_a['bundle_sha256']}\n  B: {res_b['bundle_sha256']}"
        )
        assert res_a["bundle_size"] == res_b["bundle_size"]
        assert "-candidate.zip" in res_a["bundle_filename"], "候选构建必须包含 -candidate 后缀"
        print(f"  [OK] 确定性验证: 两次构建 SHA-256 完全一致 ({res_a['bundle_sha256']})")

        # 2. 内部自洽校验
        verify_bundle(res_a["bundle_path"])
        print("  [OK] 内部自洽检查通过")

        # 3. 与 Git 来源交叉核验
        verify_bundle(res_a["bundle_path"], against_git_ref="HEAD")
        print("  [OK] 与 Git 引用 'HEAD' 交叉核验通过")

        # 4. 未打 tag 时尝试 --official-release 必须被拒绝
        try:
            build_bundle(ref="HEAD", output_dir=dir_a, official_release=True)
            assert False, "未打 tag 时执行 --official-release 应当抛出异常被拒绝！"
        except BundleError as be:
            assert "未指向任何 Git Release Tag" in str(be)
            print("  [OK] 防伪造验证: 未打 tag 时拒绝执行 --official-release")

    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)

    print("[PASS] D3 场景确定性与核验测试全部通过！")


def main():
    print("=== 开始运行 Deployment Integrity (D1/D2/D3) 评测验证套件 ===")
    test_d1_ordered_barrier()
    test_d2_placeholder_normalization()
    test_d3_bundle_determinism_and_verification()
    print("\n=== 全部测试顺利通过！(ALL TESTS PASSED) ===")


if __name__ == "__main__":
    main()
