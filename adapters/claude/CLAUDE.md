# Claude Code Instructions

This project uses shared AI coding rules from `.ai-rules/`.

## Required Reading

Before making code changes, read these rules:

- `.ai-rules/rules/general.md`
- `.ai-rules/rules/git-conventions.md`
- `.ai-rules/rules/code-review.md`
- `.ai-rules/rules/documentation.md`
- `.ai-rules/rules/line-endings.md`

## Task Skills

Load the most relevant Skill before working:

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
