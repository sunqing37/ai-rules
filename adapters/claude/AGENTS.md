# Project AI Instructions

This project uses shared AI coding rules from `.ai-rules/`.

Before coding, read context in this order:

1. Project index: `PROJECT_INDEX.md` or `.ai/PROJECT_INDEX.md` if present.
2. Task-relevant rules from `.ai-rules/rules/`.
3. Task-specific skills from `.ai-rules/skills/` when relevant.

If the project index is missing, stale, or conflicts with source code, mention the risk and fall back to the minimal source inspection needed for the task.

Do not run `git commit` directly. Use:

```bash
python .ai-rules/scripts/git-commit.py -m "<type>(<scope>): <subject>"
```
