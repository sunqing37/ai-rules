# Project AI Instructions

This project uses shared AI coding rules from `.ai-rules/`.

Before coding, read:

- `.ai-rules/rules/general.md`
- `.ai-rules/rules/git-conventions.md`
- `.ai-rules/rules/code-review.md`
- `.ai-rules/rules/documentation.md`
- `.ai-rules/rules/line-endings.md`

Use task-specific skills from `.ai-rules/skills/` when relevant:

- Android tasks: `.ai-rules/skills/android-mad/SKILL.md`
- Android feature work: `.ai-rules/skills/android-feature-workflow/SKILL.md`
- Kotlin backend tasks: `.ai-rules/skills/backend-kotlin/SKILL.md`
- Code review: `.ai-rules/skills/code-review/SKILL.md`
- Git workflow: `.ai-rules/skills/git-workflow/SKILL.md`

When creating commits, prefer the safe commit script:

```bash
python .ai-rules/scripts/git-commit.py -m "<type>(<scope>): <subject>"
```
