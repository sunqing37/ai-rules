#!/usr/bin/env python3
"""
AI 安全 Git 提交流程。

通过 git plumbing 命令（write-tree / commit-tree / update-ref）直接构造
commit object，不经过 `git commit` 这类 porcelain 命令。AI 工具的 regex 注入器
无法在 plumbing 层面拦截和追加 Co-authored-by 等 trailer 行。

用法:
    scripts/git-commit.py -m "<message>"
    scripts/git-commit.py -F <file>
    echo "<message>" | scripts/git-commit.py

脚本在构造 commit 前自动执行 body 洁净度检查，拒绝包含 AI 注入特征的提交信息。
"""

import argparse
import re
import subprocess
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# 常量
# ---------------------------------------------------------------------------
EMPTY_TREE_HASH = "4b825dc642cb6eb9a060e54bf899d9cf5edcae06"

# ---------------------------------------------------------------------------
# 禁止的 trailer 模式 —— AI 工具可能注入的行
# ---------------------------------------------------------------------------
_BLOCKED_PATTERNS: list[tuple[str, re.Pattern[str]]] = [
    ("Co-authored-by", re.compile(r"^Co-authored-by\s*:", re.IGNORECASE)),
    ("Signed-off-by (unauthorized)", re.compile(r"^Signed-off-by\s*:")),
]


def run_git(args: list[str], check: bool = True) -> str:
    """运行 git 命令，返回 strip 后的 stdout。"""
    result = subprocess.run(
        ["git"] + args,
        capture_output=True,
        text=True,
        check=check,
    )
    return result.stdout.strip()


def validate_body(message: str) -> None:
    """检查提交信息是否干净，拒绝包含 AI 注入特征的 message。"""
    for line_no, line in enumerate(message.split("\n"), start=1):
        line = line.strip()
        if not line:
            continue
        for name, pattern in _BLOCKED_PATTERNS:
            if pattern.search(line):
                print(
                    f"[--check] 第 {line_no} 行命中禁止模式 {name!r}: {line}",
                    file=sys.stderr,
                )
                sys.exit(1)

    # 额外检查：body 不应包含连续两个空行（git 标准）
    blank_count = 0
    for line in message.split("\n"):
        if line.strip() == "":
            blank_count += 1
            if blank_count > 1:
                print(
                    "[--check] 提交信息包含连续空行，不符合 Conventional Commits 格式",
                    file=sys.stderr,
                )
                sys.exit(1)
        else:
            blank_count = 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="AI 安全提交流程 —— 通过 git plumbing 命令构造 commit",
    )
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "-m", "--message",
        type=str,
        help="提交信息（与 git commit -m 一致）",
    )
    group.add_argument(
        "-F", "--file",
        type=str,
        help="从文件读取提交信息",
    )
    parser.add_argument(
        "--allow-empty",
        action="store_true",
        help="允许空提交（无暂存变更时也创建 commit）",
    )
    parser.add_argument(
        "--skip-upstream-check",
        action="store_true",
        help="跳过远端同步检查（仅在确认无冲突时使用）",
    )
    return parser.parse_args()


def check_upstream(branch: str, skip: bool = False) -> None:
    """确保本地分支与远端同步，避免推送时冲突。

    1. 解析上游跟踪分支（无上游 → 跳过）
    2. git fetch 拉取远端最新
    3. 比较 HEAD..@{u}，落后则拒绝提交
    """
    if skip:
        print("[upstream] 已跳过远端同步检查", file=sys.stderr)
        return

    # 是否有上游跟踪分支
    try:
        upstream = run_git(["rev-parse", "--abbrev-ref", f"{branch}@{{u}}"])
    except subprocess.CalledProcessError:
        # 无上游配置，本地分支，允许提交
        return

    print(f"[upstream] 正在 fetch {upstream} ...", file=sys.stderr)
    try:
        run_git(["fetch", upstream.split("/", 1)[0], branch])
    except subprocess.CalledProcessError as exc:
        print(
            f"[upstream] fetch 失败: {exc.stderr.strip() if exc.stderr else exc}",
            file=sys.stderr,
        )
        print("[upstream] 无法确认远端状态，使用 --skip-upstream-check 跳过", file=sys.stderr)
        print("[upstream] 暂存区变更未被修改，可稍后重试", file=sys.stderr)
        sys.exit(1)

    # 统计落后提交数
    try:
        behind = run_git(["rev-list", "--count", f"HEAD..{branch}@{{u}}"])
    except subprocess.CalledProcessError:
        return

    if int(behind) > 0:
        print(
            f"[upstream] 本地分支落后远端 {behind} 个提交，请先 pull/rebase 后再提交",
            file=sys.stderr,
        )
        sys.exit(1)


def get_message(args: argparse.Namespace) -> str:
    """从参数、文件或 stdin 获取提交信息。"""
    if args.message:
        return args.message
    if args.file:
        return Path(args.file).read_text(encoding="utf-8").strip()
    # stdin
    if sys.stdin.isatty():
        print("Error: 请通过 -m、-F 或管道提供提交信息", file=sys.stderr)
        sys.exit(1)
    return sys.stdin.read().strip()


def main() -> None:
    args = parse_args()
    message = get_message(args)

    if not message:
        print("Error: 提交信息不能为空", file=sys.stderr)
        sys.exit(1)

    # ---- 前置检查：body 洁净度 ----
    validate_body(message)

    # ---- 1. 写 tree ----
    # locale 无关预检：git diff --cached --quiet 替代 stderr 字符串匹配
    has_staged = subprocess.run(
        ["git", "diff", "--cached", "--quiet"]
    ).returncode != 0

    if not has_staged:
        if args.allow_empty:
            try:
                tree = run_git(["rev-parse", "HEAD^{tree}"])
            except subprocess.CalledProcessError:
                # 仓库尚无提交记录，使用 git 空 tree 魔数
                tree = EMPTY_TREE_HASH
        else:
            print(
                "Error: 没有暂存的变更。使用 --allow-empty 允许空提交。",
                file=sys.stderr,
            )
            sys.exit(1)
    else:
        tree = run_git(["write-tree"])

    # ---- 2. 获取父提交 ----
    try:
        parent = run_git(["rev-parse", "HEAD"])
    except subprocess.CalledProcessError:
        parent = None  # 初始提交

    # ---- 3. 获取当前分支名 ----
    try:
        branch = run_git(["rev-parse", "--abbrev-ref", "HEAD"])
        if branch == "HEAD":
            print("Error: 当前处于 detached HEAD 状态，无法更新分支引用", file=sys.stderr)
            sys.exit(1)
    except subprocess.CalledProcessError:
        print("Error: 无法获取当前分支名", file=sys.stderr)
        sys.exit(1)

    # ---- 4. 远端同步检查 ----
    check_upstream(branch, skip=args.skip_upstream_check)

    # ---- 5. 构造 commit object ----
    cmd = ["commit-tree", tree]
    if parent:
        cmd.extend(["-p", parent])
    cmd.extend(["-m", message])

    commit_hash = run_git(cmd)

    # ---- 6. 更新分支引用 ----
    run_git(["update-ref", f"refs/heads/{branch}", commit_hash])

    print(f"[OK] {commit_hash[:7]} → refs/heads/{branch}")
    subject = message.split("\n")[0][:72]
    print(f"     {subject}")


if __name__ == "__main__":
    main()
