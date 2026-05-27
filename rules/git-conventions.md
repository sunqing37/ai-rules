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

## AI 工具提交安全规范

> **强制规则**：禁止在 shell 中直接运行任何形式的 `git commit` 命令。
> 所有提交统一通过 `scripts/git-commit.py` 完成。

### 背景

AI 编码工具（Cursor、GitHub Copilot、Windsurf 等）在执行 shell 命令时，可能通过
regex 注入器在 `git commit -m` 的提交信息中追加 AI 署名行，例如：

```
Co-authored-by: Cursor <cursoragent@cursor.com>
```

这类注入行会污染提交历史，且难以在事后批量清理。

### 解决方式

`scripts/git-commit.py` 通过 git **plumbing** 命令直接构造 commit object：

| 步骤 | 命令 | 说明 |
|------|------|------|
| 1 | `git write-tree` | 从暂存区创建 tree object |
| 2 | `git commit-tree <tree> -p <parent> -m <msg>` | 创建 commit object |
| 3 | `git update-ref refs/heads/<branch> <commit>` | 更新分支引用 |

整个过程不经由 `git commit` 这个 porcelain 命令，AI 工具的 regex 注入器无法在
plumbing 层面拦截和追加 trailer 行。

### 使用方式

```bash
# 通过 -m 参数
scripts/git-commit.py -m "feat(auth): add OAuth2 login support"

# 通过文件
scripts/git-commit.py -F /tmp/commit-msg.txt

# 通过管道
echo "fix(api): handle null response" | scripts/git-commit.py
```

### 远端同步检查

脚本在构造 commit 前执行远端同步检查，确保本地分支不会落后于远端：

1. 解析当前分支的上游跟踪分支（`@{u}`），无上游则跳过
2. `git fetch <remote> <branch>` 拉取远端最新提交
3. 比较 `HEAD..@{u}`，如果本地落后则**非零退出**，拒绝提交

这避免了 AI 工具在过期的本地分支上提交后，推送时出现 non-fast-forward 冲突。

```bash
# 遇网络问题时，确认无冲突后可跳过
scripts/git-commit.py --skip-upstream-check -m "chore: update deps"
```

### 自动 --check

脚本在构造 commit 前自动执行 body 洁净度检查，命中以下模式之一时**非零退出**，
拒绝提交：

- `Co-authored-by:` — 任何形式的 AI 署名
- `Signed-off-by:` — 非授权的签名行
- 连续空行 — 不符合 Conventional Commits 格式

如果收到 `[--check]` 错误，说明提交信息被 AI 工具注入了非预期的 trailer 行，
需清除后重新提交。

---

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
