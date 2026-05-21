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
