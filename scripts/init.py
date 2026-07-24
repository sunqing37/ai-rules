#!/usr/bin/env python3
"""Add an AGENTS.md file that points a consumer project to ai-rules.

Run this from the root of a project that references this repository at
``.ai-rules``:

    python .ai-rules/scripts/init.py
"""

import argparse
import shutil
import sys
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parent.parent
AGENTS_TEMPLATE = REPOSITORY_ROOT / "adapters/codex/AGENTS.md"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="向目标项目添加引用 .ai-rules 的 AGENTS.md。",
    )
    parser.add_argument(
        "--target",
        type=Path,
        default=Path.cwd(),
        help="目标项目目录（默认：当前目录）。",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="覆盖目标项目中已存在的 AGENTS.md。",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    target = args.target.resolve()
    if not target.is_dir():
        print(f"Error: 目标目录不存在或不是目录: {target}", file=sys.stderr)
        return 1

    destination = target / "AGENTS.md"
    if destination.exists() and not args.force:
        print(f"[skipped] {destination} 已存在；使用 --force 可覆盖。")
        return 0

    existed = destination.exists()
    shutil.copy2(AGENTS_TEMPLATE, destination)
    result = "overwritten" if existed else "created"
    print(f"[{result}] {destination}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
