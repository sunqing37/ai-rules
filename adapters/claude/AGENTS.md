# Project AI Instructions

This project uses shared AI coding rules from `.ai-rules/`.

Before coding, read:

- `.ai-rules/rules/general.md`
- `.ai-rules/rules/git-conventions.md`
- `.ai-rules/rules/code-review.md`
- `.ai-rules/rules/documentation.md`
- `.ai-rules/rules/line-endings.md`

Use task-specific skills from `.ai-rules/skills/` when relevant.

Do not run `git commit` directly. Use:

```bash
python .ai-rules/scripts/git-commit.py -m "<type>(<scope>): <subject>"
```
