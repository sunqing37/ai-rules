# Git 提交和分支规范

统一的 Git 工作流规范，适用于所有项目。

## 分支策略

### 主分支

| 分支 | 说明 | 保护 |
|------|------|------|
| `main` / `master` | 生产就绪代码 | 禁止直接推送，仅通过 PR/MR 合并 |
| `develop` | 集成分支 | 禁止直接推送，仅通过 PR/MR 合并 |

### 功能分支命名

```
<type>/<issue-id>-<short-description>
```

- **type**: `feature`, `bugfix`, `hotfix`, `chore`, `refactor`, `docs`
- **issue-id**: 关联的工单编号（可选但推荐）
- **short-description**: 简短描述，使用小写字母和连字符

**示例:**
- `feature/JIRA-1234-user-login`
- `bugfix/5678-fix-null-pointer`
- `hotfix/9012-critical-security-patch`
- `chore/update-dependencies`
- `refactor/extract-auth-module`

## 提交信息规范 (Conventional Commits)

### 格式

```
<type>(<scope>): <subject>

[optional body]

[optional footer]
```

### Type 类型

| Type | 说明 | 示例 |
|------|------|------|
| `feat` | 新功能 | `feat(auth): add OAuth2 login support` |
| `fix` | Bug 修复 | `fix(api): handle null response from upstream` |
| `docs` | 文档变更 | `docs(readme): update installation guide` |
| `style` | 代码格式（不影响逻辑） | `style: format with project code style` |
| `refactor` | 重构（非功能变更） | `refactor(db): extract connection pool logic` |
| `perf` | 性能优化 | `perf(query): add index on user_id column` |
| `test` | 测试相关 | `test(auth): add unit tests for login flow` |
| `chore` | 构建/工具变更 | `chore(deps): bump kotlin to 2.1.0` |
| `ci` | CI/CD 变更 | `ci: add code coverage reporting` |

### 规则

1. **subject 使用祈使语气**: `add` 而非 `adds` 或 `added`
2. **subject 首字母小写**（英文）
3. **subject 不超过 72 字符**
4. **scope 可选但推荐**: 标明影响范围
5. **body 解释「为什么」和「是什么」**（可选）
6. **footer 引用工单或标注 Breaking Change**（可选）

### Breaking Change 标注

```
feat(api)!: change authentication response format

BREAKING CHANGE: AuthResponse.token is now AuthResponse.accessToken
```

或在 footer 中：

```
feat(api): change authentication response format

BREAKING CHANGE: AuthResponse.token is now AuthResponse.accessToken

Closes #1234
```

## Pull Request / Merge Request 规范

### PR 标题

与提交信息格式一致：

```
<type>(<scope>): <subject>
```

### PR 描述模板

```markdown
## 变更说明
简要描述本次变更的目的和内容。

## 变更类型
- [ ] 新功能 (feat)
- [ ] Bug 修复 (fix)
- [ ] 重构 (refactor)
- [ ] 文档 (docs)
- [ ] 其他 (chore/ci/test)

## 测试
- [ ] 单元测试通过
- [ ] 集成测试通过
- [ ] 手动测试完成

## 截图/演示（如适用）
<截图>

## 检查清单
- [ ] 代码符合项目规范
- [ ] 新增必要的测试
- [ ] 文档已更新
- [ ] 无明显性能问题
```

### 合并策略

- **优先使用 Squash Merge**: 将功能分支的所有提交压缩为一个有意义的提交
- **保持提交历史清洁**: 避免合并提交杂乱
- **PR 合并后删除源分支**

## 版本管理 (Semantic Versioning)

遵循 [SemVer 2.0.0](https://semver.org/) 规范：

```
MAJOR.MINOR.PATCH
```

- **MAJOR**: 不兼容的 API 变更
- **MINOR**: 向后兼容的功能新增
- **PATCH**: 向后兼容的 Bug 修复

## Tag 命名

```
v<MAJOR>.<MINOR>.<PATCH>
```

示例: `v1.2.3`, `v2.0.0-rc.1`
