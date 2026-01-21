# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is the "ai-coding-skill" repository - a collection of Agent Skills for AI-assisted software development. It contains multiple specialized skills that extend Claude's capabilities for different development workflows.

**Included Skills:**
- `i18n-translation` - Internationalization and translation workflow automation
- `deepwiki` - Automated documentation generation and codebase analysis

**Key References:**
- Agent skills documentation: https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview
- Official skills repository: https://github.com/anthropics/skills

## Repository Structure

```
ai-coding-skill/
├── README.md                    # Main project documentation (English)
├── README.zh-CN.md              # Chinese version documentation
├── CLAUDE.md                    # This file
├── BEST_PRACTICES.md            # Agent Skills best practices guide
├── LICENSE                      # Apache License 2.0
└── skills/                      # Skills directory
    ├── i18n-translation/
    └── deepwiki/
```

## Development

When working with this repository:
- This is a documentation/skill definition repository
- No build system or dependencies (documentation-only)
- Changes should be made directly to documentation files
- Follow standard Git workflow for updates

## Skill Usage

### i18n-translation Skill

Use this skill when:
- Users need to add or update internationalization content
- Working with translation files across multiple languages
- Extracting strings for localization
- Synchronizing translation keys
- Validating translation file formats

### deepwiki Skill

Use this skill when:
- Users need to generate documentation from code
- Analyzing codebase structure and patterns
- Creating API documentation or architecture docs
- Producing structured technical reports
- Deep research and analysis of codebases
