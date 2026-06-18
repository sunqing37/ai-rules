# DeepSeek TUI Instructions

本项目使用 `.ai-rules/` 中的统一 AI 编码规范。

开始编码前，请按顺序读取上下文：

1. 项目索引：优先读取 `PROJECT_INDEX.md` 或 `.ai/PROJECT_INDEX.md`（如存在）。
2. 任务相关规则：按需读取 `.ai-rules/rules/` 下与任务相关的规则文件。
3. 任务相关 Skill：按需读取 `.ai-rules/skills/` 下与任务类型相关的 Skill。

如果项目索引缺失、明显过期或与源码冲突，请说明风险，并回退到完成任务所需的最小源码检查。

常用 Skill：

- Android：`.ai-rules/skills/android-mad/SKILL.md`
- Android 功能交付：`.ai-rules/skills/android-feature-workflow/SKILL.md`
- Kotlin 后端：`.ai-rules/skills/backend-kotlin/SKILL.md`
- 代码审查：`.ai-rules/skills/code-review/SKILL.md`
- Git 工作流：`.ai-rules/skills/git-workflow/SKILL.md`

提交时不要直接运行 `git commit`，优先使用：

```bash
python .ai-rules/scripts/git-commit.py -m "<type>(<scope>): <subject>"
```
