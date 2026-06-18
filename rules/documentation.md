# 文档规范

统一的文档编写规范，适用于所有项目。

## 文档原则

1. **文档即代码**: 文档与代码同等重要，随代码一同维护和审查。
2. **时效性**: 保持文档与代码同步更新，过时文档比没有文档更危险。
3. **面向读者**: 明确文档的目标读者（新手、使用者、贡献者），选择合适的内容深度。
4. **简洁清晰**: 用最少的文字说明最关键的信息。

## 必要文档清单

每个项目至少应包含：

| 文档 | 用途 | 优先级 |
|------|------|--------|
| `README.md` | 项目概览、快速开始 | 必须 |
| `CONTRIBUTING.md` | 贡献指南 | 推荐 |
| `CHANGELOG.md` | 变更日志 | 推荐 |
| `PROJECT_INDEX.md` | 面向 AI 的项目目录索引和工作入口 | 大型项目推荐 |
| `LICENSE` | 许可证 | 必须 |
| API 文档 | 接口说明 | 视项目而定 |
| 架构文档 | 系统设计说明 | 大型项目推荐 |

## README.md 规范

### 结构

```markdown
# 项目名称
一句话描述项目用途。

## 快速开始
环境要求 + 最小可运行步骤。

## 核心特性
项目主要功能列表。

## 安装
详细的安装步骤。

## 使用
基本使用方法和示例。

## API 文档（如适用）
接口概览和链接。

## 架构（如适用）
系统架构概述。

## 贡献
如何参与贡献，指向 CONTRIBUTING.md。

## 许可证
许可证信息。
```

### 要求

- **必须有 Quick Start**: 新人在 5 分钟内跑通
- **代码示例可运行**: 直接复制粘贴应能执行
- **保持更新**: 接口和命令变更时同步更新

## CHANGELOG.md 规范

遵循 [Keep a Changelog](https://keepachangelog.com/) 格式：

```markdown
# Changelog

## [1.2.0] - 2025-05-20

### Added
- 新增 OAuth2 登录支持

### Changed
- 将默认超时时间从 5s 调整为 10s

### Deprecated
- `login()` 方法将在 v2.0 中移除，请使用 `authenticate()`

### Fixed
- 修复并发环境下的连接池耗尽问题

### Security
- 修复 CVE-2025-xxxx 中的认证绕过漏洞
```

## PROJECT_INDEX.md 规范

`PROJECT_INDEX.md` 是面向 AI 编码助手的轻量项目索引，用于在大型项目中快速建立上下文，减少每次任务前对大量源码和文档的重复读取。

### 目标

- **快速定位**: 帮助 AI 先理解项目结构，再按任务读取必要文件。
- **当前快照**: 描述项目当前最新结构，而不是历史变更过程。
- **低成本维护**: 只记录稳定、关键的信息，避免复制完整源码或长篇设计文档。
- **降低误读风险**: 当索引与源码冲突时，以源码为准，并同步修正索引。

### 推荐位置

优先使用项目根目录的 `PROJECT_INDEX.md`。如果项目已有专门的 AI 文档目录，也可使用 `.ai/PROJECT_INDEX.md`，但需要在项目级 AI 指令文件中明确路径。

### 推荐结构

```markdown
# Project Index

## Overview
一句话说明项目用途、主要业务目标和核心技术栈。

## Directory Map
列出顶层目录及其职责，避免展开到过细层级。

## Key Modules
按模块说明职责、入口文件、常见修改点和相关测试位置。

## Architecture Notes
记录关键架构约束、分层规则、生成代码位置和禁止事项。

## Build and Test
列出最常用的构建、测试、静态检查命令及适用场景。

## AI Working Guide
说明 AI 应先读本索引，再按任务读取相关源码；索引缺失或过期时应提示维护。

## Freshness
记录最近一次结构确认日期、维护责任人或触发更新条件。
```

### 维护要求

以下变更发生时，必须同步检查并按需更新 `PROJECT_INDEX.md`：

- 新增、删除、移动或重命名顶层目录。
- 新增、拆分、合并或废弃核心模块。
- 入口文件、构建命令、测试命令、主要配置位置发生变化。
- 架构分层、代码生成规则、禁止修改区域或跨模块依赖约束发生变化。
- README、ADR 或 API 文档中影响 AI 定位工作的内容发生变化。

### 与 CHANGELOG.md 的边界

- `CHANGELOG.md` 记录按版本组织的历史变更，回答“发生过什么”。
- `PROJECT_INDEX.md` 记录当前项目结构和 AI 工作入口，回答“现在应该从哪里开始”。
- 目录或模块结构调整时，`CHANGELOG.md` 记录变更摘要，`PROJECT_INDEX.md` 更新为最新结构快照。
- AI 编码时应优先读取 `PROJECT_INDEX.md` 获取当前结构，再按需查看 `CHANGELOG.md` 理解历史背景。

### AI 使用要求

项目提供 `PROJECT_INDEX.md` 时，AI 编码助手应遵循以下顺序：

1. 先读取 `PROJECT_INDEX.md` 或 `.ai/PROJECT_INDEX.md`。
2. 根据索引定位任务相关模块、测试和约束。
3. 只读取与任务相关的源码、规则和 Skill，避免无差别扫描整个项目。
4. 如果索引缺失、明显过期或与源码冲突，应明确说明并回退到必要的源码检查。

## API 文档规范

### 格式

每个 API 端点至少包含：

```markdown
## GET /api/users/:id

获取指定用户信息。

### 路径参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| id | string | 是 | 用户 ID |

### 查询参数

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| include_profile | boolean | 否 | false | 是否包含关联资料 |

### 请求示例

GET /api/users/123?include_profile=true

### 响应

#### 200 OK

{
  "id": "123",
  "name": "张三",
  "email": "zhangsan@example.com"
}

#### 404 Not Found

{
  "error": "user_not_found",
  "message": "用户 123 不存在"
}
```

### 工具建议

- **REST API**: 使用 Swagger/OpenAPI 注解
- **GraphQL**: 使用内置的 Schema 文档
- **gRPC**: 使用 protobuf 注释

## 代码注释规范

见 `rules/general.md` 中的「注释规范」章节。

## 架构文档规范 (ADR)

对于重要的架构决策，使用 ADR (Architecture Decision Record) 记录：

```markdown
# ADR-001: 使用 PostgreSQL 替代 MySQL

## 状态
已采纳

## 上下文
项目需要处理大量 JSON 数据和复杂的地理空间查询...

## 决策
选择 PostgreSQL，因为其 JSONB 支持和 PostGIS 扩展...

## 影响
- 运维团队需要学习 PostgreSQL 管理
- 现有 MySQL 数据需要迁移
```

## 多语言文档

- 如果项目面向多语言用户，README 应提供多语言版本
- 使用 `README.zh-CN.md` 这样的命名方式
- 主 `README.md` 使用英语（或根据团队主要语言决定）
