#!/usr/bin/env python3
"""
ChatGPT Project 官方部署包构建与核验工具 (Deployment Bundle Builder & Verifier)

用途：
从指定的不可变 Git 引用（如 release commit 或 tag）中提取核心交付文件，
计算 SHA-256 内容哈希并生成 manifest.json，最终打包为可发布的 zip 资产包。

保证：
1. 部署包内容严格来自 Git 提交对象，绝不从本地脏工作区复制；
2. 生成机器可核验的 manifest.json；
3. 支持构建与独立解包核验两种模式。
"""

import argparse
import hashlib
import json
import os
import subprocess
import sys
import zipfile
from datetime import datetime, timezone

DELIVERABLE_FILES = [
    "project-instructions.md",
    "browser-agent-playbook.md",
    "browser-workflow-spec.md",
]


def run_git(args, cwd=None):
    """运行 git 命令并返回 stdout 字符串"""
    cmd = ["git"] + args
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=cwd, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"Git 命令失败: {' '.join(cmd)}\n错误输出: {result.stderr.strip()}")
    return result.stdout.strip()


def run_git_bytes(args, cwd=None):
    """运行 git 命令并返回原始 bytes"""
    cmd = ["git"] + args
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=cwd)
    if result.returncode != 0:
        raise RuntimeError(f"Git 命令失败: {' '.join(cmd)}\n错误输出: {result.stderr.decode('utf-8', errors='replace').strip()}")
    return result.stdout


def compute_sha256(data: bytes) -> str:
    """计算 bytes 的 SHA-256 哈希值"""
    return hashlib.sha256(data).hexdigest()


def extract_version_from_instructions(content: str) -> str:
    """从 project-instructions.md 内容中解析 WORKFLOW_REF"""
    for line in content.splitlines():
        line = line.strip()
        if line.startswith("WORKFLOW_REF:"):
            parts = line.split(":", 1)
            if len(parts) == 2:
                return parts[1].strip()
    return "unknown"


def build_bundle(ref: str, output_dir: str, explicit_version: str = None) -> dict:
    """从指定 git ref 构建官方部署包"""
    # 1. 获取完整 commit SHA
    commit_sha = run_git(["rev-parse", ref])
    print(f"[*] 来源 Git 引用: {ref} -> commit SHA: {commit_sha}")

    # 2. 从 git 对象中抽取三个交付文件
    file_contents = {}
    for filename in DELIVERABLE_FILES:
        git_path = f"chatgpt-project/{filename}"
        try:
            content_bytes = run_git_bytes(["show", f"{commit_sha}:{git_path}"])
            file_contents[filename] = content_bytes
        except Exception as e:
            sys.exit(f"[!] 无法从 {ref} 中读取 {git_path}: {e}")

    # 3. 确定版本标识
    instructions_text = file_contents["project-instructions.md"].decode("utf-8")
    detected_version = extract_version_from_instructions(instructions_text)
    version = explicit_version or detected_version
    print(f"[*] 部署包版本标识: {version}")

    # 4. 计算哈希与构建 manifest
    now_iso = datetime.now(timezone.utc).isoformat()
    manifest_data = {
        "workflow_version": version,
        "release_commit_sha": commit_sha,
        "generated_at": now_iso,
        "files": {},
    }

    print("\n--- 文件哈希清单 (Artifact Hashes) ---")
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

    manifest_bytes = json.dumps(manifest_data, indent=2, ensure_ascii=False).encode("utf-8")

    # 5. 打包为 zip
    os.makedirs(output_dir, exist_ok=True)
    bundle_filename = f"matt-browser-workflow-chatgpt-project-{version}.zip"
    bundle_path = os.path.join(output_dir, bundle_filename)

    with zipfile.ZipFile(bundle_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for filename in DELIVERABLE_FILES:
            zf.writestr(filename, file_contents[filename])
        zf.writestr("manifest.json", manifest_bytes)

    with open(bundle_path, "rb") as f:
        bundle_sha256 = compute_sha256(f.read())
    bundle_size = os.path.getsize(bundle_path)

    print(f"\n[+] 部署包生成成功: {bundle_path}")
    print(f"    ZIP SHA-256: {bundle_sha256}")
    print(f"    ZIP 大小:    {bundle_size} 字节")

    return {
        "bundle_path": bundle_path,
        "bundle_sha256": bundle_sha256,
        "bundle_size": bundle_size,
        "manifest": manifest_data,
    }


def verify_bundle(zip_path: str):
    """核验已有 zip 部署包的内部完整性"""
    if not os.path.isfile(zip_path):
        sys.exit(f"[!] 找不到文件: {zip_path}")

    print(f"[*] 开始核验部署包: {zip_path}")
    with zipfile.ZipFile(zip_path, "r") as zf:
        namelist = zf.namelist()
        if "manifest.json" not in namelist:
            sys.exit("[!] 部署包中缺失 manifest.json，无法核验！")

        manifest_bytes = zf.read("manifest.json")
        manifest = json.loads(manifest_bytes.decode("utf-8"))
        print(f"[*] Manifest 声明版本: {manifest.get('workflow_version')}")
        print(f"[*] Manifest 声明 Commit: {manifest.get('release_commit_sha')}")

        for filename in DELIVERABLE_FILES:
            if filename not in namelist:
                sys.exit(f"[!] 部署包缺失核心交付文件: {filename}")
            actual_data = zf.read(filename)
            actual_sha = compute_sha256(actual_data)
            expected_sha = manifest["files"][filename]["sha256"]
            if actual_sha != expected_sha:
                sys.exit(f"[!] 哈希不匹配！文件: {filename}\n    期望: {expected_sha}\n    实际: {actual_sha}")
            print(f"  [OK] {filename}: SHA-256 匹配")

    print("[+] 部署包内部完整性核验全部 PASS！")


def main():
    parser = argparse.ArgumentParser(description="ChatGPT Project 官方部署包构建与核验工具")
    parser.add_argument("--ref", default="HEAD", help="来源 Git 引用（如 HEAD、release 分支或 tag），默认 HEAD")
    parser.add_argument("--output-dir", default=".", help="输出目录，默认当前目录")
    parser.add_argument("--version", help="显式指定版本号（如 v0.17），默认自动从 instructions 中读取")
    parser.add_argument("--verify", help="核验指定的部署包 zip 文件路径")

    args = parser.parse_args()

    if args.verify:
        verify_bundle(args.verify)
    else:
        build_bundle(args.ref, args.output_dir, args.version)


if __name__ == "__main__":
    main()
