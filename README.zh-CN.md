# AI 编程技能集合

一个精选的 Agent Skills 集合，用于扩展 Claude 在 AI 辅助软件开发方面的能力。

**[English](./README.md)** | **[中文](./README.zh-CN.md)**

## 概述

此仓库包含多个 Agent Skills，用于扩展 Claude 在特定开发任务中的能力。每个技能都为特定领域提供结构化的工作流程、最佳实践和工具。

## 包含的技能

### 1. i18n-translation
国际化和翻译工作流自动化。
- 从源代码中提取可翻译字符串
- 生成和管理翻译文件（JSON、YAML 等）
- 同步多种语言间的翻译键
- 检测缺失或过时的翻译
- 验证翻译文件语法

**位置**: `skills/i18n-translation/`

### 2. deepwiki
自动化文档生成和代码库分析。
- 从代码生成全面的文档
- 创建 API 文档、架构文档和指南
- 分析代码模式和最佳实践
- 为各种项目类型生成结构化报告
- 深度代码库研究和分析

**位置**: `skills/deepwiki/`

## 最佳实践指南

此仓库还包含基于 Anthropic 官方文档的综合 **Agent Skills 最佳实践**指南：

- 渐进式披露设计模式
- 编写有效的技能描述
- 选择正确的内容类型（指令、脚本、资源）
- 安全最佳实践
- 平台约束和可移植性
- 技能生命周期管理

**位置**: `BEST_PRACTICES.md` | [English](./BEST_PRACTICES.md)

## 快速开始

### 官方文档
- [Agent Skills 概述](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview) - Anthropic 官方文档
- [官方 Skills 仓库](https://github.com/anthropics/skills) - 参考实现
- [Skills 详解](https://claude.com/blog/skills-explained) - Skills 与 Prompts、Projects、MCP 和 Subagents 的比较
- [在线查看本集合](https://skills.sh/HybridTalentComputing/ai-coding-skills) - 技能在线查看器

### 安装

#### 通过 npm 快速安装（推荐）

```bash
# 安装本集合中的所有技能
npx skills install HybridTalentComputing/ai-coding-skills

# 或单独安装某个技能
npx skills install HybridTalentComputing/ai-coding-skills#i18n-translation
npx skills install HybridTalentComputing/ai-coding-skills#deepwiki-skill
```

### 支持的 IDE

这些技能兼容以下开发环境：

- **Claude Code** - 完整支持
- **Codex** - 完整支持
- **Cursor** - 完整支持
- **OpenCode** - 完整支持
- **Trae** - 完整支持

安装后，技能会在相关上下文中自动加载。

## 仓库结构

```
ai-coding-skill/
├── README.md                    # 英文版说明
├── README.zh-CN.md              # 中文版说明（本文件）
├── CLAUDE.md                    # Claude Code 工作指南
├── BEST_PRACTICES.md            # Agent Skills 最佳实践指南（英文）
├── BEST_PRACTICES_CN.md         # Agent Skills 最佳实践指南（中文）
├── LICENSE                      # Apache License 2.0
└── skills/                      # 技能目录
    ├── i18n-translation/        # 国际化技能
    │   ├── SKILL.md            # 主要技能指令
    │   └── references/         # 参考材料
    │       ├── workflow.md
    │       ├── patterns.md
    │       ├── namespaces.md
    │       ├── modular-files.md
    │       └── checklist.md
    └── deepwiki/                # 文档生成技能
        ├── SKILL.md            # 主要技能指令
        ├── README.md           # 技能文档
        ├── assets/             # 模板和资源
        │   ├── document_templates/
        │   └── report_templates/
        └── references/         # 参考材料
            ├── deep_research_prompts.md
            ├── documentation_standards.md
            ├── code_patterns.md
            └── analysis_framework.md
```

## 使用示例

### i18n-translation 技能

**创建翻译文件：**

```json
// en.json
{
  "welcome": "Welcome to our application",
  "goodbye": "Goodbye!"
}

// zh-CN.json
{
  "welcome": "欢迎使用我们的应用",
  "goodbye": "再见！"
}
```

### deepwiki 技能

**生成文档：**
- "为认证服务创建 API 文档"
- "分析代码库并生成架构文档"
- "记录支付模块的组件结构"

**深度代码分析：**
- "研究并记录项目中的数据流模式"
- "为部署过程创建全面的故障排除指南"

## 贡献

欢迎贡献！可以改进的领域：

- **新技能**：为其他开发工作流添加专业技能
- **增强示例**：改进现有技能的示例和模板
- **文档**：增强最佳实践和指南
- **测试**：添加验证脚本和测试用例

贡献时请：

1. 遵循现有代码风格和模式
2. 为新技能添加全面的文档
3. 根据需要更新 README 文件
4. 确保跨平台兼容性

## 许可证

本项目采用 Apache License 2.0 许可 - 详见 [LICENSE](./LICENSE) 文件。
