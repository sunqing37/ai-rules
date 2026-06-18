# DeepSeek TUI Instructions

本项目使用 `.ai-rules/` 中的统一 AI 编码规范。

开始编码前，请读取：

- `.ai-rules/rules/general.md`
- `.ai-rules/rules/git-conventions.md`
- `.ai-rules/rules/code-review.md`
- `.ai-rules/rules/documentation.md`
- `.ai-rules/rules/line-endings.md`

根据任务类型读取对应 Skill：

- Android：`.ai-rules/skills/android-mad/SKILL.md`
- Android 功能交付：`.ai-rules/skills/android-feature-workflow/SKILL.md`
- Kotlin 后端：`.ai-rules/skills/backend-kotlin/SKILL.md`
- 代码审查：`.ai-rules/skills/code-review/SKILL.md`
- Git 工作流：`.ai-rules/skills/git-workflow/SKILL.md`

提交时不要直接运行 `git commit`，优先使用：

```bash
python .ai-rules/scripts/git-commit.py -m "<type>(<scope>): <subject>"
```
