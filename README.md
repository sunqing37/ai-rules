# AI Rules — 统一 AI 编码规范

一套可通过 Git Submodule 引用的统一 AI 编码规范、AI Skill 定义和项目模板，帮助不同项目、不同 AI 编码工具保持一致的编码行为。

## 适用场景

- 多个项目希望复用同一套 AI 编码规范
- Cursor、Claude Code、DeepSeek TUI、Codex 等工具需要共享项目指令
- Android、Kotlin 后端、Git 工作流、代码审查等场景需要可复用的 Skill
- 新项目初始化时需要快速复制 `.editorconfig`、`.gitattributes`、`PROJECT_INDEX.md` 等基础模板

## 快速开始

### 1. 作为 Git Submodule 引用

```bash
# 在目标项目中添加 submodule
git submodule add https://github.com/sunqing37/ai-rules.git .ai-rules
git submodule update --init --recursive
```

### 2. 在项目 Instructions 中显式引用

AI 工具不会天然保证递归加载 `.ai-rules/` 下的全部文件。建议在目标项目的项目级指令文件中显式声明项目索引和需要读取的规则文件。

不同工具的常见指令文件位置：

| AI 工具 | 指令文件 |
|---------|----------|
| Codex / Claude Code | `AGENTS.md` |
| Claude Code | `CLAUDE.md` |
| Cursor | `.cursor/rules/*.mdc` |
| DeepSeek TUI | `.deepseek/instructions.md` |

推荐在项目 `AGENTS.md` 或对应指令文件中写入：

```markdown
# 项目编码规范

本项目遵循统一 AI 编码规范，规则位于 `.ai-rules/`。

在编写代码前，请按顺序读取：
1. `PROJECT_INDEX.md` 或 `.ai/PROJECT_INDEX.md` — 项目当前结构、模块职责和 AI 工作入口
2. `.ai-rules/rules/` 下与任务相关的规则文件
3. `.ai-rules/skills/` 下与任务类型相关的 Skill 定义

如果项目索引缺失、明显过期或与源码冲突，请说明风险，并回退到必要的源码检查。
```

### 3. 使用适配模板

仓库提供了常见 AI 工具的适配模板，可复制到目标项目：

```text
adapters/
├── codex/AGENTS.md
├── claude/CLAUDE.md
├── cursor/ai-rules.mdc
└── deepseek/instructions.md
```

### 4. 复制项目模板

```bash
cp .ai-rules/templates/.editorconfig .editorconfig
cp .ai-rules/templates/.gitattributes .gitattributes
cp .ai-rules/templates/PROJECT_INDEX.md PROJECT_INDEX.md
```

如需使用 AI 安全提交脚本：

```bash
python .ai-rules/scripts/git-commit.py -m "feat(scope): add feature"
```

## 目录结构

```text
ai-rules/
├── README.md                       # 本文件
├── CHANGELOG.md                    # 变更记录
├── CONTRIBUTING.md                 # 贡献指南
├── LICENSE                         # 开源许可证
├── rules/                          # 通用编码规范（语言无关）
│   ├── general.md                  # 通用编码原则
│   ├── git-conventions.md          # Git 提交和分支规范
│   ├── code-review.md              # 代码审查规范
│   ├── documentation.md            # 文档规范
│   └── line-endings.md             # 换行符管理规范
├── skills/                         # AI Skills（跨工具通用）
│   ├── general-coding/             # 通用编码 Skill
│   ├── code-review/                # 代码审查 Skill
│   ├── git-workflow/               # Git 工作流 Skill
│   ├── android-mad/                # Android MAD 开发规范
│   ├── android-feature-workflow/   # Android 功能交付流程
│   └── backend-kotlin/             # Kotlin 后端开发规范
├── adapters/                       # 不同 AI 工具的项目指令模板
│   ├── codex/
│   ├── claude/
│   ├── cursor/
│   └── deepseek/
├── templates/                      # 项目模板文件
│   ├── .editorconfig
│   ├── .gitattributes
│   ├── PROJECT_INDEX.md            # 面向 AI 的项目目录索引模板
│   └── gitignore-templates/
└── scripts/                        # 辅助脚本
    └── git-commit.py               # AI 安全提交脚本
```

## 规范层级

| 层级 | 说明 | 适用场景 |
|------|------|----------|
| `rules/` | 人读的完整规范，是规则的主要事实来源 | 所有项目、所有开发者 |
| `skills/` | 面向 AI 执行的压缩版 Skill | AI 辅助编码时按任务类型触发 |
| `adapters/` | 不同 AI 工具的入口模板 | 项目接入时复制或参考 |
| `templates/` | 可直接复制的项目模板 | 新项目初始化 |
| `scripts/` | 辅助落地脚本 | 提交、校验、初始化等自动化场景 |

如果 `rules/` 与 `skills/` 出现冲突，以 `rules/` 为准；`skills/` 应作为 AI 执行摘要同步维护。

## 维护约定

- 修改规范后，在 `CHANGELOG.md` 中记录变更
- 项目顶层目录、核心模块、入口文件、构建/测试命令或架构约束变化时，同步更新 `PROJECT_INDEX.md`
- 遵循 [Semantic Versioning](https://semver.org/) 进行版本管理
- 发布稳定版本时创建 `vMAJOR.MINOR.PATCH` tag
- 各项目通过 submodule 版本锁定引用特定版本的规范
- 新增或修改 Skill 时，同步检查对应 `rules/` 是否需要更新

## License

MIT License. 详见 [LICENSE](LICENSE)。
