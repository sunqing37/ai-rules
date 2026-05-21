# AI Rules — 统一 AI 编码规范

一套可通过 Git Submodule 引用的统一 AI 编码规范和技能定义，确保跨项目、跨工具的 AI 辅助编码行为保持一致。

## 使用方式

### 作为 Git Submodule 引用

```bash
# 在目标项目中添加 submodule
git submodule add https://github.com/your-org/ai-rules.git .ai-rules
git submodule update --init --recursive
```

### 在项目 Instructions 中引用

Submodule 引入后，只需在项目的 AI 指令文件中告知工具读取 `.ai-rules/` 下的规范文件。AI 工具会自动加载并遵循这些规范，无需手动复制 skills 或逐个工具配置。

不同工具的指令文件位置：

| AI 工具 | 指令文件 |
|---------|----------|
| DeepSeek TUI | `.deepseek/instructions.md` |
| Claude Code | `CLAUDE.md` 或 `AGENTS.md` |
| Cursor | `.cursor/rules/` 目录下 `.mdc` 文件 |

**推荐做法：** 在项目的 `AGENTS.md`（或对应指令文件）中写入：

```markdown
# 项目编码规范

本项目遵循统一 AI 编码规范，详见 `.ai-rules/` 目录。

在编写代码前，请阅读以下规范文件：
- .ai-rules/rules/general.md         — 通用编码原则
- .ai-rules/rules/git-conventions.md  — Git 提交和分支规范
- .ai-rules/rules/code-review.md     — 代码审查规范
- .ai-rules/rules/documentation.md   — 文档规范
- .ai-rules/rules/line-endings.md    — 换行符管理规范

如需特定领域规范，参阅 `.ai-rules/skills/` 下对应的 Skill 定义。
```

如果 AI 工具支持从项目目录加载 skills，可额外将 `.ai-rules/skills/` 配置为 skill 路径。各工具具体配置方式参见其文档。

## 目录结构

```
ai-rules/
├── README.md                       # 本文件
├── rules/                          # 通用编码规范（语言无关）
│   ├── general.md                  # 通用编码原则
│   ├── git-conventions.md          # Git 提交和分支规范
│   ├── code-review.md              # 代码审查规范
│   ├── documentation.md            # 文档规范
│   └── line-endings.md             # 换行符 (LF/CRLF) 管理规范
├── skills/                         # AI Skills（跨工具通用）
│   ├── general-coding/             # 通用编码 skill
│   ├── code-review/                # 代码审查 skill
│   ├── git-workflow/               # Git 工作流 skill
│   ├── android-mad/                # Android MAD 开发规范
│   ├── android-feature-workflow/   # Android 功能交付流程
│   └── backend-kotlin/             # Kotlin 后端开发规范
└── templates/                      # 项目模板文件
    ├── .editorconfig
    ├── .gitattributes              # Git 换行符控制
    └── gitignore-templates/        # 各类项目的 .gitignore 模板
```

## 规范层级

| 层级 | 说明 | 适用场景 |
|------|------|----------|
| `rules/` | 语言无关的通用规范 | 所有项目、所有开发者 |
| `skills/` | AI 工具直接加载的 Skill 定义 | AI 辅助编码时自动触发 |
| `templates/` | 可直接复制的模板文件 | 新项目初始化 |

## 维护

- 修改规范后，在 `CHANGELOG.md` 中记录变更
- 遵循 [Semantic Versioning](https://semver.org/) 进行版本管理
- 各项目通过 submodule 版本锁定引用特定版本的规范
