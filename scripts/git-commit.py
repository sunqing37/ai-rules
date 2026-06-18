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

脚本在构造 commit 前自动执行 message 洁净度检查，拒绝包含 AI 注入特征的提交信息。
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
    ("Generated-by", re.compile(r"^Generated-by\s*:", re.IGNORECASE)),
    ("AI-generated-by", re.compile(r"^AI-generated-by\s*:", re.IGNORECASE)),
]

_SIGNED_OFF_BY_PATTERN = re.compile(r"^Signed-off-by\s*:", re.IGNORECASE)
_CONVENTIONAL_SUBJECT = re.compile(
    r"^(feat|fix|docs|style|refactor|perf|test|chore|ci|build|revert)(\([^)]+\))?!?: .+"
)


def run_git(args: list[str], check: bool = True) -> str:
    """运行 git 命令，返回 strip 后的 stdout。"""
    result = subprocess.run(
        ["git"] + args,
        capture_output=True,
        text=True,
        check=check,
    )
    return result.stdout.strip()


def validate_message(message: str, allow_signed_off_by: bool = False) -> None:
    """检查提交信息是否干净，拒绝包含 AI 注入特征的 message。"""
    subject = message.split("\n", 1)[0].strip()
    if len(subject) > 72:
        print(
            f"[--check] 提交标题超过 72 字符: {len(subject)}",
            file=sys.stderr,
        )
        sys.exit(1)

    if not _CONVENTIONAL_SUBJECT.match(subject):
        print(
            "[--check] 提交标题不符合 Conventional Commits 格式: "
            "<type>(<scope>): <subject>",
            file=sys.stderr,
        )
        sys.exit(1)

    for line_no, line in enumerate(message.split("\n"), start=1):
        stripped = line.strip()
        if not stripped:
            continue

        if _SIGNED_OFF_BY_PATTERN.search(stripped) and not allow_signed_off_by:
            print(
                f"[--check] 第 {line_no} 行命中禁止模式 'Signed-off-by': {stripped}",
                file=sys.stderr,
            )
            print(
                "[--check] 如项目启用了 DCO，可显式添加 --allow-signed-off-by",
                file=sys.stderr,
            )
            sys.exit(1)

        for name, pattern in _BLOCKED_PATTERNS:
            if pattern.search(stripped):
                print(
                    f"[--check] 第 {line_no} 行命中禁止模式 {name!r}: {stripped}",
                    file=sys.stderr,
                )
                sys.exit(1)


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
        "--allow-signed-off-by",
        action="store_true",
        help="允许 Signed-off-by trailer，用于启用 DCO 的项目",
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

    try:
        upstream = run_git(["rev-parse", "--abbrev-ref", f"{branch}@{{u}}"])
        remote = run_git(["config", f"branch.{branch}.remote"])
        merge_ref = run_git(["config", f"branch.{branch}.merge"])
    except subprocess.CalledProcessError:
        # 无上游配置，本地分支，允许提交
        return

    print(f"[upstream] 正在 fetch {upstream} ...", file=sys.stderr)
    try:
        # 使用 branch.<name>.merge，避免 feature/x 这类分支被错误 fetch。
        run_git(["fetch", remote, merge_ref])
    except subprocess.CalledProcessError as exc:
        print(
            f"[upstream] fetch 失败: {exc.stderr.strip() if exc.stderr else exc}",
            file=sys.stderr,
        )
        print("[upstream] 无法确认远端状态，使用 --skip-upstream-check 跳过", file=sys.stderr)
        print("[upstream] 暂存区变更未被修改，可稍后重试", file=sys.stderr)
        sys.exit(1)

    try:
        behind = run_git(["rev-list", "--count", f"HEAD..{upstream}"])
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

    validate_message(message, allow_signed_off_by=args.allow_signed_off_by)

    has_staged = subprocess.run(
        ["git", "diff", "--cached", "--quiet"]
    ).returncode != 0

    if not has_staged:
        if args.allow_empty:
            try:
                tree = run_git(["rev-parse", "HEAD^{tree}"])
            except subprocess.CalledProcessError:
                tree = EMPTY_TREE_HASH
        else:
            print(
                "Error: 没有暂存的变更。使用 --allow-empty 允许空提交。",
                file=sys.stderr,
            )
            sys.exit(1)
    else:
        tree = run_git(["write-tree"])

    try:
        parent = run_git(["rev-parse", "HEAD"])
    except subprocess.CalledProcessError:
        parent = None

    try:
        branch = run_git(["rev-parse", "--abbrev-ref", "HEAD"])
        if branch == "HEAD":
            print("Error: 当前处于 detached HEAD 状态，无法更新分支引用", file=sys.stderr)
            sys.exit(1)
    except subprocess.CalledProcessError:
        print("Error: 无法获取当前分支名", file=sys.stderr)
        sys.exit(1)

    check_upstream(branch, skip=args.skip_upstream_check)

    cmd = ["commit-tree", tree]
    if parent:
        cmd.extend(["-p", parent])
    cmd.extend(["-m", message])

    commit_hash = run_git(cmd)
    run_git(["update-ref", f"refs/heads/{branch}", commit_hash])

    print(f"[OK] {commit_hash[:7]} → refs/heads/{branch}")
    subject = message.split("\n")[0][:72]
    print(f"     {subject}")


if __name__ == "__main__":
    main()
