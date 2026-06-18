# Contributing Guide

感谢你维护这套 AI 编码规范。这个仓库的目标不是堆砌规则，而是沉淀一套可复用、可落地、可被 AI 工具稳定执行的工程规范。

## 维护原则

1. **规则少而准**：优先保留能显著提升代码质量和协作效率的规则。
2. **可执行**：每条规则都应尽量给出判断标准、示例或模板。
3. **项目兼容**：规范应兼顾新项目最佳实践和存量项目渐进改造。
4. **单一事实来源**：`rules/` 是完整规范；`skills/` 是面向 AI 执行的摘要。
5. **避免绝对化**：除安全、数据损坏、提交污染等强约束外，不轻易使用“必须”“严禁”。

## 目录职责

| 目录 | 职责 |
|------|------|
| `rules/` | 人读的完整规范，是主要事实来源 |
| `skills/` | AI 工具直接使用的任务摘要版 |
| `adapters/` | 各 AI 工具的项目接入模板 |
| `templates/` | 可复制到业务项目的基础模板 |
| `scripts/` | 帮助规范落地的工具脚本 |

## 修改规范的流程

1. 修改 `rules/` 中对应规范。
2. 如果变更会影响 AI 执行行为，同步修改相关 `skills/`。
3. 如果变更影响项目接入方式，同步更新 `adapters/` 或 `README.md`。
4. 在 `CHANGELOG.md` 的 `[Unreleased]` 记录变更。
5. 检查 README 中引用的路径是否真实存在。

## Skill 编写建议

每个 `SKILL.md` 应包含：

- YAML frontmatter：`name`、`description`
- 适用场景
- 执行流程
- 输出格式
- 与 `rules/` 的关系说明

建议在 Skill 顶部声明：

```markdown
Source of truth: `../../rules/xxx.md`。本 Skill 是面向 AI 执行的摘要版；如与 `rules/` 冲突，以 `rules/` 为准。
```

## 提交规范

提交信息遵循 Conventional Commits：

```text
<type>(<scope>): <subject>
```

常用 type：

- `feat`: 新增规则、模板、脚本能力
- `fix`: 修复错误规则、脚本 bug、路径错误
- `docs`: 文档调整
- `refactor`: 结构调整但不改变规则语义
- `chore`: 工具、格式、维护类变更

推荐使用安全提交脚本：

```bash
python scripts/git-commit.py -m "docs: update android skill"
```

## 发布版本

发布稳定版本时：

1. 更新 `CHANGELOG.md`，将 `[Unreleased]` 内容移动到新版本号。
2. 创建 SemVer tag：`vMAJOR.MINOR.PATCH`。
3. 在依赖项目中更新 submodule 指向对应 tag 或 commit。
