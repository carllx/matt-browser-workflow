#!/usr/bin/env python3
"""
ChatGPT Project 官方部署包构建与核验工具 (Deployment Bundle Builder & Verifier)

用途：
从指定的不可变 Git 引用（如 release commit 或 tag）中提取核心交付文件，
计算 SHA-256 内容哈希并生成 manifest.json，确定性打包为 zip 资产。

保证与安全边界：
1. 部署包内容严格来自 Git 提交对象，绝不从本地脏工作区复制；
2. 确定性构建：时间戳与文件权限严格从不可变提交导出，相同 SHA 多次构建产生相同 ZIP 哈希；
3. 发布身份防伪造：正式发布模式严格核对发布 tag、Instructions、Playbook 与 Spec 的版本一致性；
   候选预览模式强制添加 `-candidate.zip` 后缀，避免混淆；
4. 验证模式分级：明确区分 ZIP 内部自洽检查与基于 Git 权威来源的交叉核验。
"""

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import zipfile
from datetime import datetime, timezone

DELIVERABLE_FILES = sorted([
    "project-instructions.md",
    "browser-agent-playbook.md",
    "browser-workflow-spec.md",
])


class BundleError(Exception):
    """部署包构建与校验相关的异常"""
    pass


def run_git(args, cwd=None, text=True):
    """统一运行 git 命令，支持文本与二进制模式，避免代码重复"""
    cmd = ["git"] + args
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=cwd, text=text)
    if result.returncode != 0:
        err = result.stderr if text else result.stderr.decode("utf-8", errors="replace")
        raise RuntimeError(f"Git 命令执行失败: {' '.join(cmd)}\n错误输出: {err.strip()}")
    return result.stdout.strip() if text else result.stdout


def compute_sha256(data: bytes) -> str:
    """计算 bytes 的 SHA-256 哈希值"""
    return hashlib.sha256(data).hexdigest()


def extract_version_from_instructions(content: str) -> str:
    """从 project-instructions.md 中提取 WORKFLOW_REF"""
    for line in content.splitlines():
        line = line.strip()
        if line.startswith("WORKFLOW_REF:"):
            parts = line.split(":", 1)
            if len(parts) == 2:
                return parts[1].strip()
    return "unknown"


def extract_version_from_markdown_header(content: str) -> str:
    """从 Markdown 标题中提取版本号（如 v0.17）"""
    match = re.search(r"\b(v\d+\.\d+(?:\.\d+)?)\b", content)
    return match.group(1) if match else "unknown"


def build_bundle(ref: str, output_dir: str, official_release: bool = False, release_tag: str = None) -> dict:
    """从指定 git ref 构建部署包，保证确定性与发布身份约束"""
    # 1. 获取完整 commit SHA
    try:
        commit_sha = run_git(["rev-parse", ref])
    except Exception as e:
        raise BundleError(f"无法解析 Git 引用 '{ref}': {e}")

    print(f"[*] 来源 Git 引用: {ref} -> commit SHA: {commit_sha}")

    # 2. 从 Git commit 时间导出确定性时间戳（消除生成时随机性）
    try:
        commit_time_epoch = int(run_git(["log", "-1", "--format=%ct", commit_sha]))
        commit_dt = datetime.fromtimestamp(commit_time_epoch, tz=timezone.utc)
        zip_time = (commit_dt.year, commit_dt.month, commit_dt.day,
                    commit_dt.hour, commit_dt.minute, commit_dt.second)
    except Exception as e:
        raise BundleError(f"无法从 commit {commit_sha} 提取提交时间: {e}")

    # 3. 从 Git 树中提取三个交付文件
    file_contents = {}
    for filename in DELIVERABLE_FILES:
        git_path = f"chatgpt-project/{filename}"
        try:
            content_bytes = run_git(["show", f"{commit_sha}:{git_path}"], text=False)
            file_contents[filename] = content_bytes
        except Exception as e:
            raise BundleError(f"无法从 {ref} 中提取 {git_path}: {e}")

    # 4. 解析各文件内部声明的版本
    instructions_text = file_contents["project-instructions.md"].decode("utf-8")
    playbook_text = file_contents["browser-agent-playbook.md"].decode("utf-8")
    spec_text = file_contents["browser-workflow-spec.md"].decode("utf-8")

    instr_ver = extract_version_from_instructions(instructions_text)
    playbook_ver = extract_version_from_markdown_header(playbook_text)
    spec_ver = extract_version_from_markdown_header(spec_text)

    print(f"[*] 文件内部版本声明: instructions={instr_ver}, playbook={playbook_ver}, spec={spec_ver}")

    # 5. 发布身份与模式核对
    if official_release:
        # 正式发布模式：必须核验 Git tag 与三文件版本一致性，绝不允许静默造假
        detected_tag = None
        if release_tag:
            detected_tag = release_tag
            tag_commit = run_git(["rev-parse", f"{release_tag}^{{commit}}"])
            if tag_commit != commit_sha:
                raise BundleError(f"指定的 release tag '{release_tag}' 指向的 commit ({tag_commit}) 与目标 commit ({commit_sha}) 不匹配！")
        else:
            try:
                detected_tag = run_git(["describe", "--tags", "--exact-match", commit_sha])
            except Exception:
                raise BundleError(f"目标 commit {commit_sha} 未指向任何 Git Release Tag，无法执行 --official-release 构建！")

        target_version = detected_tag.lstrip("refs/tags/")
        if not (target_version == instr_ver == playbook_ver == spec_ver):
            raise BundleError(
                f"正式发布版本不一致！\n"
                f"  Git Tag:           {target_version}\n"
                f"  Instructions Ref:  {instr_ver}\n"
                f"  Playbook Header:   {playbook_ver}\n"
                f"  Spec Header:       {spec_ver}\n"
                f"全部声明必须 100% 严格吻合，严禁伪造正式发布身份。"
            )

        release_mode = "official_release"
        version_label = target_version
        bundle_filename = f"matt-browser-workflow-chatgpt-project-{version_label}.zip"
        print(f"[+] 官方发布身份核查通过: {version_label} (Tag: {detected_tag})")
    else:
        # 候选预览模式：明确命名带有 -candidate 后缀，不得赋予正式发布文件名
        release_mode = "candidate_preview"
        detected_tag = None
        version_label = instr_ver if instr_ver != "unknown" else "dev"
        bundle_filename = f"matt-browser-workflow-chatgpt-project-{version_label}-candidate.zip"
        print(f"[!] 注意：当前处于候选预览模式 (candidate_preview)")
        print(f"    生成产物将命名为: {bundle_filename}，严禁作为生产正式发布 Asset！")

    # 6. 计算 SHA-256 并构造确定性 manifest
    manifest_data = {
        "commit_timestamp": commit_dt.isoformat(),
        "files": {},
        "release_commit_sha": commit_sha,
        "release_mode": release_mode,
        "release_tag": detected_tag,
        "workflow_version": version_label,
    }

    print("\n--- 交付文件哈希清单 ---")
    for filename in DELIVERABLE_FILES:
        data = file_contents[filename]
        sha = compute_sha256(data)
        size = len(data)
        manifest_data["files"][filename] = {
            "sha256": sha,
            "size_bytes": size,
        }
        print(f"  {filename}:")
        print(f"    SHA-256: {sha}")
        print(f"    Size:    {size} 字节")

    manifest_bytes = json.dumps(manifest_data, indent=2, sort_keys=True, ensure_ascii=False).encode("utf-8")

    # 7. 确定性打包（固定 entry 时间戳与权限，消除生成时随机性）
    os.makedirs(output_dir, exist_ok=True)
    bundle_path = os.path.join(output_dir, bundle_filename)

    with zipfile.ZipFile(bundle_path, "w", zipfile.ZIP_DEFLATED) as zf:
        # 先写 Deliverable Files（按字母排序）
        for filename in DELIVERABLE_FILES:
            data = file_contents[filename]
            zinfo = zipfile.ZipInfo(filename=filename, date_time=zip_time)
            zinfo.compress_type = zipfile.ZIP_DEFLATED
            zinfo.external_attr = 0o644 << 16  # rw-r--r--
            zf.writestr(zinfo, data)

        # 后写 manifest.json
        zinfo_m = zipfile.ZipInfo(filename="manifest.json", date_time=zip_time)
        zinfo_m.compress_type = zipfile.ZIP_DEFLATED
        zinfo_m.external_attr = 0o644 << 16
        zf.writestr(zinfo_m, manifest_bytes)

    with open(bundle_path, "rb") as f:
        bundle_sha256 = compute_sha256(f.read())
    bundle_size = os.path.getsize(bundle_path)

    print(f"\n[+] 部署包生成成功: {bundle_path}")
    print(f"    ZIP SHA-256: {bundle_sha256}")
    print(f"    ZIP 大小:    {bundle_size} 字节")
    print(f"    构建模式:    {release_mode}")

    return {
        "bundle_filename": bundle_filename,
        "bundle_path": bundle_path,
        "bundle_sha256": bundle_sha256,
        "bundle_size": bundle_size,
        "manifest": manifest_data,
    }


def verify_bundle(zip_path: str, against_git_ref: str = None):
    """
    核验 zip 部署包完整性与官方发布身份。
    - 基础模式：核验 zip 内部文件与 manifest 自洽性（输出自洽限制警告）；
    - Git 交叉模式 (--against-git)：核验 zip 与指定不可变 Git 提交/Tag 的对象完全一致。
    """
    if not os.path.isfile(zip_path):
        raise BundleError(f"找不到指定的 ZIP 文件: {zip_path}")

    print(f"[*] 开始核验部署包: {zip_path}")
    with zipfile.ZipFile(zip_path, "r") as zf:
        namelist = zf.namelist()
        if "manifest.json" not in namelist:
            raise BundleError("部署包中缺失 manifest.json，无法进行完整性核验！")

        manifest_bytes = zf.read("manifest.json")
        try:
            manifest = json.loads(manifest_bytes.decode("utf-8"))
        except Exception as e:
            raise BundleError(f"manifest.json 格式损坏: {e}")

        declared_ver = manifest.get("workflow_version")
        declared_commit = manifest.get("release_commit_sha")
        declared_mode = manifest.get("release_mode")
        print(f"[*] Manifest 声明版本: {declared_ver}")
        print(f"[*] Manifest 声明 Commit: {declared_commit}")
        print(f"[*] Manifest 声明模式: {declared_mode}")

        # 1. 内部自洽性校验
        for filename in DELIVERABLE_FILES:
            if filename not in namelist:
                raise BundleError(f"部署包中缺失核心交付文件: {filename}")
            actual_data = zf.read(filename)
            actual_sha = compute_sha256(actual_data)
            expected_sha = manifest.get("files", {}).get(filename, {}).get("sha256")
            if actual_sha != expected_sha:
                raise BundleError(f"内部哈希不匹配！文件: {filename}\n  期望: {expected_sha}\n  实际: {actual_sha}")
            print(f"  [OK] {filename}: 内部 SHA-256 匹配")

        print("[+] 内部自洽性检查全部通过 (Internal Self-Consistency PASS)")

        # 2. 若无 Git 权威来源交叉核验，输出显式警告
        if not against_git_ref:
            print("[WARN] 注意：当前仅完成 ZIP 内部自洽校验 (Self-Consistency Only)！")
            print("       该结果未与 Git 官方不可变来源交叉核对，不得单独作为发布 provenance 权威证据。")
            return

        # 3. 权威 Git 来源交叉核对
        print(f"\n[*] 正在与不可变 Git 引用 '{against_git_ref}' 进行交叉核验...")
        git_commit = run_git(["rev-parse", against_git_ref])
        if declared_commit != git_commit:
            raise BundleError(
                f"来源 Commit 不匹配！\n"
                f"  Git 引用 ({against_git_ref}) 解析出的 SHA: {git_commit}\n"
                f"  ZIP manifest 声明的 SHA:            {declared_commit}"
            )

        for filename in DELIVERABLE_FILES:
            git_path = f"chatgpt-project/{filename}"
            git_data = run_git(["show", f"{git_commit}:{git_path}"], text=False)
            git_sha = compute_sha256(git_data)
            zip_data = zf.read(filename)
            zip_sha = compute_sha256(zip_data)

            if git_sha != zip_sha:
                raise BundleError(f"与 Git 权威对象不匹配！文件: {filename}\n  Git 实际: {git_sha}\n  ZIP 内容: {zip_sha}")
            print(f"  [PASS] {filename}: 与 Git blob SHA-256 100% 吻合")

        print(f"[PASS] 官方发布身份与 Git 来源交叉核验完全通过 (Official Release Provenance Verified)。")


def main():
    parser = argparse.ArgumentParser(description="ChatGPT Project 官方部署包确定性构建与核验工具")
    parser.add_argument("--ref", default="HEAD", help="来源 Git 引用（如 HEAD、commit 或 release tag），默认 HEAD")
    parser.add_argument("--output-dir", default=".", help="输出目录，默认当前目录")
    parser.add_argument("--official-release", action="store_true", help="开启正式发布构建模式（强制核实 release tag 与三文件版本一致性）")
    parser.add_argument("--release-tag", help="显式指定目标 Git release tag 名称（在 official-release 模式下使用）")
    parser.add_argument("--verify", help="核验指定的部署包 zip 文件路径")
    parser.add_argument("--against-git", help="与指定的不可变 Git 引用交叉比对（配合 --verify 使用）")

    args = parser.parse_args()

    try:
        if args.verify:
            verify_bundle(args.verify, against_git_ref=args.against_git)
        else:
            build_bundle(
                ref=args.ref,
                output_dir=args.output_dir,
                official_release=args.official_release,
                release_tag=args.release_tag,
            )
    except BundleError as be:
        print(f"\n[FAIL] 部署包校验错误: {be}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"\n[ERROR] 意外错误: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
