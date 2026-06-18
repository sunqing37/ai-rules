# Claude Code Instructions

This project uses shared AI coding rules from `.ai-rules/`.

## Required Reading

Before making code changes, read context in this order:

1. Project index: `PROJECT_INDEX.md` or `.ai/PROJECT_INDEX.md` if present.
2. Task-relevant rules from `.ai-rules/rules/`.
3. The most relevant Skill from `.ai-rules/skills/`.

If the project index is missing, stale, or conflicts with source code, mention the risk and fall back to the minimal source inspection needed for the task.

## Task Skills

Load only the Skill relevant to the current task:

- General coding: `.ai-rules/skills/general-coding/SKILL.md`
- Code review: `.ai-rules/skills/code-review/SKILL.md`
- Git workflow: `.ai-rules/skills/git-workflow/SKILL.md`
- Android: `.ai-rules/skills/android-mad/SKILL.md`
- Android feature workflow: `.ai-rules/skills/android-feature-workflow/SKILL.md`
- Kotlin backend: `.ai-rules/skills/backend-kotlin/SKILL.md`

## Git Safety

Do not run `git commit` directly. Use:

```bash
python .ai-rules/scripts/git-commit.py -m "<type>(<scope>): <subject>"
```
