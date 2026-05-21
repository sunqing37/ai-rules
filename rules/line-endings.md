# 换行符管理规范

统一的换行符（LF/CRLF）管理策略，避免跨平台协作中的换行符混乱。

## 问题背景

不同操作系统使用不同的换行符：

| 系统 | 换行符 | 表示 |
|------|--------|------|
| Linux / macOS | LF | `\n` |
| Windows | CRLF | `\r\n` |

混用会导致：
- Git diff 显示全文件变更（每行都被标记为修改）
- CI 流水线中换行符检查失败
- 代码审查时无法定位真实改动
- 脚本文件在不同平台上执行异常

## 推荐策略

**仓库内部统一使用 LF，通过 Git 和编辑器配置在本地自动转换。**

### 三层防线

| 层级 | 工具 | 作用 |
|------|------|------|
| 1. 编辑器 | `.editorconfig` | 开发者在编辑时即使用正确换行符 |
| 2. Git | `.gitattributes` | 提交时强制转换为 LF，检出时按平台处理 |
| 3. CI | lint 规则 | 阻断不合规的换行符进入仓库 |

## .editorconfig 配置

确保所有编辑器使用 LF：

```ini
root = true

[*]
charset = utf-8
end_of_line = lf
insert_final_newline = true
trim_trailing_whitespace = true

# Windows 批处理文件必须使用 CRLF
[*.{bat,cmd}]
end_of_line = crlf

# PowerShell 脚本（CRLF 更安全）
[*.ps1]
end_of_line = crlf
```

## .gitattributes 配置（核心防线）

Git 层面的换行符控制，比编辑器配置更可靠：

```
# 默认行为：自动检测文本文件，提交时统一为 LF
* text=auto

# 明确指定文本文件类型（提交时 Git 会标准化为 LF）
*.kt          text eol=lf
*.kts         text eol=lf
*.java        text eol=lf
*.xml         text eol=lf
*.gradle      text eol=lf
*.properties  text eol=lf
*.md          text eol=lf
*.yml         text eol=lf
*.yaml        text eol=lf
*.json        text eol=lf
*.ts          text eol=lf
*.tsx         text eol=lf
*.js          text eol=lf
*.css         text eol=lf
*.html        text eol=lf

# Windows 脚本文件需要 CRLF
*.bat         text eol=crlf
*.cmd         text eol=crlf
*.ps1         text eol=crlf

# 二进制文件不转换
*.png         binary
*.jpg         binary
*.jpeg        binary
*.gif         binary
*.ico         binary
*.jar         binary
*.zip         binary
*.gz          binary
*.tar         binary
*.ttf         binary
*.otf         binary
*.eot         binary
*.woff        binary
*.woff2       binary
*.keystore    binary
*.jks         binary
```

## Windows 开发者配置

Windows 开发者需要额外注意：

### Git 全局配置

```bash
# 确保 Git 在 checkout 时转换为 CRLF，commit 时转为 LF
git config --global core.autocrlf true
```

此设置的含义：
- `git checkout`：LF → CRLF（Windows 本地可正常编辑）
- `git commit`：CRLF → LF（仓库内保持 LF）

如果项目 `.gitattributes` 已配置 `eol=lf`，Git 会优先使用 `.gitattributes` 的规则。

### IDE 配置

- **IntelliJ IDEA / Android Studio**: `Settings → Editor → Code Style → Line separator` 设为 `LF`
- **VS Code**: 右下角状态栏点击换行符指示器，选择 `LF`
- **VS Code 全局设置**: `"files.eol": "\n"`

## CI 检查

在 CI 流水线中添加换行符检查：

### GitHub Actions 示例

```yaml
- name: Check line endings
  run: |
    # 检查是否有 CRLF 被提交
    git ls-files | xargs file | grep -l "CRLF" && exit 1 || exit 0
```

### 禁止提交 CRLF（pre-commit hook）

```bash
#!/bin/bash
# .git/hooks/pre-commit
if git diff --cached --name-only | xargs grep -l $'\r' -- ; then
    echo "ERROR: CRLF detected. Run 'git add --renormalize .' to fix."
    exit 1
fi
```

## 已有仓库迁移

如果仓库已存在换行符混乱，按以下步骤修复：

```bash
# 1. 备份当前状态
git stash

# 2. 添加 .gitattributes（见上方模板）

# 3. 重新规范化所有文件
git add --renormalize .

# 4. 提交
git commit -m "chore: normalize line endings to LF"
```

## 特殊场景

### 生成的文件

由工具自动生成的文件（如 Gradle wrapper、protobuf 生成代码）：
- **不要手动修改其换行符**
- 确保生成工具配置正确
- 或将生成目录加入 `.gitattributes` 对应规则

### Shell 脚本（Linux/macOS）

`.sh` 文件必须使用 LF，否则在 Linux 上无法执行：

```
*.sh          text eol=lf
```

### Makefile

Makefile 要求 tab 缩进 + LF 换行，`.editorconfig` 中已配置。

## 检查清单

新项目初始化时确认：

- [ ] `.editorconfig` 根目录已放置，`end_of_line = lf`
- [ ] `.gitattributes` 根目录已放置，核心文件类型指定 `text eol=lf`
- [ ] 二进制文件标记为 `binary`
- [ ] Windows 脚本文件指定 `eol=crlf`
- [ ] CI 中包含换行符检查
- [ ] 团队成员确认编辑器换行符设置
