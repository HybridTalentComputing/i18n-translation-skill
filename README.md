# AI Coding Skills Collection

A curated collection of Agent Skills for extending Claude's capabilities in AI-assisted software development.

**[English](./README.md)** | **[中文](./README.zh-CN.md)**

## Overview

This repository contains multiple Agent Skills that extend Claude's capabilities for specialized development tasks. Each skill provides structured workflows, best practices, and tools for specific domains.

## Included Skills

### 1. i18n-translation
Internationalization and translation workflow automation.
- Extract translatable strings from source code
- Generate and manage translation files (JSON, YAML, etc.)
- Synchronize translation keys across multiple languages
- Detect missing or outdated translations
- Validate translation file syntax

**Location**: `skills/i18n-translation/`

### 2. deepwiki
Automated documentation generation and codebase analysis.
- Generate comprehensive documentation from code
- Create API documentation, architecture docs, and guides
- Analyze code patterns and best practices
- Produce structured reports for various project types
- Deep codebase research and analysis

**Location**: `skills/deepwiki/`

## Best Practices Guide

This repository also includes a comprehensive **Agent Skills Best Practices** guide based on Anthropic's official documentation:

- Progressive disclosure design patterns
- Writing effective skill descriptions
- Choosing the right content types (instructions, scripts, resources)
- Security best practices
- Platform constraints and portability
- Skill lifecycle management

**Location**: `BEST_PRACTICES.md` | [中文版](./BEST_PRACTICES_CN.md)

## Getting Started

### Official Documentation
- [Agent Skills Overview](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview) - Official Anthropic documentation
- [Official Skills Repository](https://github.com/anthropics/skills) - Reference implementations
- [Skills Explained](https://claude.com/blog/skills-explained) - How Skills compare to Prompts, Projects, MCP, and Subagents

### Installation

Each skill can be used independently:
1. Navigate to the skill directory (e.g., `skills/i18n-translation/`)
2. Ensure the skill is properly configured with metadata
3. Claude will automatically detect and load the skill when relevant

## Repository Structure

```
ai-coding-skill/
├── README.md                    # This file
├── README.zh-CN.md              # Chinese version
├── CLAUDE.md                    # Guidance for Claude Code
├── BEST_PRACTICES.md            # Agent Skills best practices guide
├── BEST_PRACTICES_CN.md         # Best practices (Chinese)
├── LICENSE                      # Apache License 2.0
└── skills/                      # Skills directory
    ├── i18n-translation/        # Internationalization skill
    │   ├── SKILL.md            # Main skill instructions
    │   └── references/         # Reference materials
    │       ├── workflow.md
    │       ├── patterns.md
    │       ├── namespaces.md
    │       ├── modular-files.md
    │       └── checklist.md
    └── deepwiki/                # Documentation generation skill
        ├── SKILL.md            # Main skill instructions
        ├── README.md           # Skill documentation
        ├── assets/             # Templates and resources
        │   ├── document_templates/
        │   └── report_templates/
        └── references/         # Reference materials
            ├── deep_research_prompts.md
            ├── documentation_standards.md
            ├── code_patterns.md
            └── analysis_framework.md
```

## Usage Examples

### i18n-translation Skill

**Creating Translation Files:**

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

### deepwiki Skill

**Generate Documentation:**
- "Create API documentation for the authentication service"
- "Analyze the codebase and generate architecture documentation"
- "Document the component structure of the payment module"

**Deep Code Analysis:**
- "Research and document the data flow patterns in this project"
- "Create a comprehensive troubleshooting guide for the deployment process"

## Getting Started

### Official Documentation
- [Agent Skills Overview](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview) - Official Anthropic documentation
- [Official Skills Repository](https://github.com/anthropics/skills) - Reference implementations
- [Skills Explained](https://claude.com/blog/skills-explained) - How Skills compare to Prompts, Projects, MCP, and Subagents

### Installation

Each skill can be used independently:
1. Navigate to the skill directory (e.g., `skills/i18n-translation/`)
2. Ensure the skill is properly configured with metadata
3. Claude will automatically detect and load the skill when relevant

## Contributing

Contributions are welcome! Areas for improvement:

- **New Skills**: Add specialized skills for other development workflows
- **Enhanced Examples**: Improve existing skill examples and templates
- **Documentation**: Enhance best practices and guides
- **Testing**: Add validation scripts and test cases

When contributing:

1. Follow existing code style and patterns
2. Add comprehensive documentation for new skills
3. Update README files as needed
4. Ensure cross-platform compatibility

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](./LICENSE) file for details.
