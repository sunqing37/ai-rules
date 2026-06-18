# Changelog

本项目遵循 [Keep a Changelog](https://keepachangelog.com/) 格式，并使用 [Semantic Versioning](https://semver.org/) 进行版本管理。

## [Unreleased]

### Added

- 新增 `PROJECT_INDEX.md` 模板，作为面向 AI 的项目目录索引。
- 新增 AI 项目索引规范，明确索引结构、维护时机以及与 CHANGELOG 的边界。
- 新增常见 AI 工具适配模板：Codex、Claude Code、Cursor、DeepSeek TUI。
- 新增 `CONTRIBUTING.md`，说明规范维护和贡献流程。
- 新增 `LICENSE`，明确开源许可证。

### Changed

- 优化各 AI 工具适配模板，要求优先读取项目索引，再按任务读取相关规则和 Skill。
- 优化 README，明确 AI 工具需要显式引用 `.ai-rules/` 规则文件。
- 优化 Android MAD Skill，使其区分新项目严格模式和存量项目兼容模式。
- 优化 Android 功能交付流程，按复杂度选择流程，避免简单任务过度确认。
- 对齐 `.editorconfig` 与换行符规范，补充 `.cmd`、`.ps1` 的 CRLF 配置。

### Fixed

- 改进 `scripts/git-commit.py` 的上游分支 fetch 逻辑，避免 `feature/x` 等分支名被错误处理。
- 移除对连续空行的过度限制，保留对 AI 注入 trailer 的检查。
- 为启用 DCO 的项目增加 `--allow-signed-off-by` 选项。

## [0.1.0] - 2026-06-18

### Added

- 初始版本：通用编码规范、Git 规范、代码审查规范、文档规范、换行符规范。
- 初始 Skills：通用编码、代码审查、Git 工作流、Android MAD、Android 功能流程、Kotlin 后端。
- 初始模板：`.editorconfig`、`.gitattributes`。
- 初始 AI 安全提交脚本：`scripts/git-commit.py`。
