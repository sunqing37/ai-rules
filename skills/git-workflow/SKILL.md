---
name: git-workflow
description: Git 工作流 Skill，当用户进行 Git 操作、编写提交信息、创建分支、发起 PR/MR 时使用。提供 Conventional Commits 格式和分支命名规范。
---

# Git 工作流 Skill

为 AI 编码助手提供统一的 Git 操作规范。

## 分支命名

在创建分支时使用以下格式：

```
<type>/<short-description>
```

type 取值：
- `feature/` — 新功能
- `bugfix/` — Bug 修复
- `hotfix/` — 紧急修复
- `refactor/` — 重构
- `chore/` — 构建/工具
- `docs/` — 文档

short-description 使用小写字母和连字符，不超过 4 个词。

示例: `feature/user-login`, `bugfix/null-pointer-fix`

## 提交信息格式

每次提交必须遵循 Conventional Commits 格式：

```
<type>(<scope>): <subject>
```

常用 type：
- `feat` — 新功能
- `fix` — Bug 修复
- `docs` — 文档
- `refactor` — 重构
- `perf` — 性能优化
- `test` — 测试
- `chore` — 构建/工具

规则：
- subject 使用祈使语气（`add` 而非 `added`）
- subject 不超过 72 字符
- scope 标明影响范围（可选但推荐）

### Breaking Change

破坏性变更在 type 后加 `!`：

```
feat(api)!: change auth response format

BREAKING CHANGE: token field renamed to accessToken
```

## PR/MR 描述模板

创建 PR 时使用以下模板：

```markdown
## 变更说明
<简要描述>

## 变更类型
- [ ] feat / fix / refactor / docs / chore

## 测试
- [ ] 单元测试通过
- [ ] 手动验证完成

## 检查清单
- [ ] 代码符合规范
- [ ] 测试已添加
- [ ] 文档已更新
```

## 操作原则

- 不直接推送到 main/master 分支
- 合并前确保 CI 通过
- PR 体积控制在 400 行以内
- 了解项目使用 Squash Merge 还是 Merge Commit
