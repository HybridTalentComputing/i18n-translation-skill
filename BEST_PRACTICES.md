# Agent Skills Best Practices

This guide outlines best practices for creating effective Agent Skills based on Anthropic's official documentation and architectural patterns.

## Overview

Agent Skills are filesystem-based modular capabilities that extend Claude's functionality. Each Skill packages instructions, metadata, and optional resources (scripts, templates) that Claude uses automatically when relevant.

**Key Principles:**
- Skills teach Claude **how to do** something (procedural knowledge)
- Skills load progressively to optimize token usage
- Skills are reusable across conversations and projects
- Skills combine to build complex workflows

## 1. Progressive Disclosure Design

Skills use a three-level loading architecture. Design your Skill to take advantage of this:

```
Level 1: Metadata (~100 tokens)
├── Loaded at startup
├── Provides discovery information
└── Tells Claude when to trigger this Skill

Level 2: Instructions (<5k tokens)
├── Loaded when Skill is triggered
├── Contains core procedural knowledge
└── Main guidance for Claude

Level 3: Resources (unlimited, on-demand)
├── Loaded only when referenced
├── Scripts, reference docs, templates
└── Accessed via bash without consuming context
```

### Best Practice
Don't put everything in `SKILL.md`. Move large reference materials, examples, and documentation to separate files that load only when needed.

## 2. Write Effective Descriptions

The `description` field in YAML frontmatter is critical for discovery. It must tell Claude both what the Skill does AND when to use it.

### Example

```yaml
---
name: excel-data-analysis
description: >
  Analyze Excel spreadsheets using pandas and openpyxl.
  Use when user mentions Excel, .xlsx files, spreadsheets,
  or needs data analysis/visualization from Excel files.
---
```

### Guidelines
- **Be specific**: Mention concrete use cases and keywords
- **Include triggers**: List scenarios when Claude should activate this Skill
- **Keep it focused**: Under 1024 characters
- **Think like Claude**: What information would help you recognize when to use this?

## 3. Choose the Right Content Type

Each content type has different strengths:

| Content Type | Best For | Token Cost | When Loaded |
|--------------|----------|------------|-------------|
| **Instructions** | Workflows, best practices, guidance | Low (under 5k) | When Skill triggers |
| **Scripts** | Deterministic operations, automation | Zero (only output counts) | When executed |
| **Resources** | API docs, schemas, templates, examples | Zero (until accessed) | On-demand via bash |

### Decision Framework

- **Use Instructions** for flexible guidance that requires reasoning
- **Use Scripts** for repetitive, deterministic operations
- **Use Resources** for factual lookup and reference materials

## 4. Structure Your Skill Directory

Organize your Skill like an employee onboarding guide:

```
your-skill/
├── SKILL.md              # Required: Main instructions
├── QUICKSTART.md         # Optional: Quick reference
├── EXAMPLES.md           # Optional: Usage examples
├── REFERENCE.md          # Optional: Detailed documentation
├── TROUBLESHOOTING.md    # Optional: Common issues
└── scripts/              # Optional: Executable utilities
    ├── validate.py
    └── transform.py
```

### Required Fields

Every `SKILL.md` must include:

```yaml
---
name: your-skill-name
description: Brief description of what this Skill does and when to use it
---
```

### Field Requirements

**name:**
- Maximum 64 characters
- Lowercase letters, numbers, and hyphens only
- Cannot contain: "anthropic", "claude", or XML tags

**description:**
- Maximum 1024 characters
- Cannot contain XML tags
- Must be non-empty

## 5. Writing Style Guidelines

Think of `SKILL.md` as an onboarding guide for a new team member.

### Do's
- ✅ Provide clear, step-by-step instructions
- ✅ Include concrete examples
- ✅ Cover common scenarios and edge cases
- ✅ Reference additional files for details
- ✅ Use code blocks for examples

### Don'ts
- ❌ Don't state the obvious (Claude already knows how to code)
- ❌ Don't write generic content without specific context
- ❌ Don't duplicate information that's in general documentation
- ❌ Don't write walls of text without structure

### Example Structure

```markdown
# Your Skill Name

## Quick Start
[Brief 2-3 sentence overview of how to use this Skill]

## When to Use This Skill
[Clear criteria for when this Skill is relevant]

## Core Workflow
1. Step one
2. Step two
3. Step three

## Examples
### Example 1: [Scenario]
[Concrete example with code/output]

### Example 2: [Scenario]
[Concrete example with code/output]

## Additional Resources
- See [EXAMPLES.md](EXAMPLES.md) for more use cases
- See [REFERENCE.md](REFERENCE.md) for detailed API documentation
```

## 6. When to Use Skills vs. Other Building Blocks

### Use Skills When
- You find yourself typing the same prompt repeatedly across conversations
- You need procedural knowledge that applies across multiple projects
- You want to combine multiple capabilities into a workflow
- You have organizational workflows or standards to enforce

### Use Prompts When
- You're giving one-time instructions
- Providing immediate context
- Having conversational back-and-forth
- Testing ideas before formalizing

### Use Projects When
- You need persistent background knowledge
- Organizing work around a specific initiative
- Building a knowledge base for a team

### Use MCP When
- You need to access external data sources (Google Drive, Slack, databases)
- Connecting to business tools (CRM, project management)
- You have custom systems to integrate

### Use Subagents When
- You need independent task execution
- You want to restrict tool permissions
- You're building specialized workflows in Claude Code

**Key Distinction:**
- **MCP** connects Claude to data
- **Skills** teach Claude what to do with that data
- Use them together: MCP for connectivity, Skills for procedural knowledge

## 7. Security Best Practices

Skills provide Claude with new capabilities through instructions and code. Follow these security guidelines:

### Essential Practices
- ✅ Only use Skills from trusted sources (created by you or Anthropic)
- ✅ Audit all files: SKILL.md, scripts, images, resources
- ✅ Review for unusual patterns (unexpected network calls, file access)
- ✅ Verify operations match the Skill's stated purpose

### High-Risk Patterns
- ⚠️ Skills that fetch data from external URLs
- ⚠️ Skills with unexpected network calls
- ⚠️ Scripts that access sensitive data
- ⚠️ Operations that don't match the Skill's description

### Treat Skills Like Software
Installing a Skill is like installing software. Only use Skills from trusted sources, especially when integrating into production systems with access to sensitive data.

## 8. Environment Constraints

Different platforms have different limitations. Design your Skill accordingly:

### Claude API
- ❌ No network access
- ❌ No runtime package installation
- ✅ Only pre-installed packages available

### Claude Code
- ✅ Full network access
- ✅ Local package installation (install locally, avoid global)
- ✅ All system capabilities

### Claude.ai
- ⚠️ Varying network access (depends on user/admin settings)
- ⚠️ Check file creation settings for your environment

### Design for Portability
If you want your Skill to work across platforms, design for the most restrictive environment (Claude API).

## 9. Skill Lifecycle

### Creating Skills
1. Start with identifying repetitive prompts in your workflow
2. Design the Skill structure (SKILL.md + supporting files)
3. Write effective metadata (name + description)
4. Create progressive disclosure structure
5. Test with Claude and iterate

### Testing Skills
- Verify Claude triggers the Skill at appropriate times
- Check that instructions are clear and followed correctly
- Ensure referenced files load when needed
- Test scripts execute properly
- Validate token efficiency (are you loading too much upfront?)

### Iterating Skills
- Monitor when Claude fails to use the Skill appropriately
- Refine description if triggering is inconsistent
- Add examples for common failure modes
- Split large Skills into multiple focused Skills if needed

## 10. Common Pitfalls to Avoid

### 1. Overstuffing SKILL.md
**Problem**: Putting everything in one file wastes tokens

**Solution**: Use progressive disclosure. Move reference materials to separate files.

### 2. Vague Descriptions
**Problem**: Claude doesn't know when to trigger your Skill

**Solution**: Be specific about use cases and keywords in the description.

### 3. Reinventing the Wheel
**Problem**: Writing what Claude already knows

**Solution**: Focus on domain-specific, organizational, or procedural knowledge, not general capabilities.

### 4. Ignoring Platform Constraints
**Problem**: Skill assumes capabilities that don't exist in all environments

**Solution**: Design for the most restrictive platform you plan to support.

### 5. Missing Progressive Disclosure
**Problem**: All content loads at once, wasting tokens

**Solution**: Structure content across multiple files that load on-demand.

## 11. Checklist for Creating Effective Skills

Use this checklist before finalizing your Skill:

- [ ] **Description**: Clearly states what the Skill does and when to use it
- [ ] **Metadata**: Follows naming conventions (no reserved words, lowercase)
- [ ] **Structure**: Main instructions in SKILL.md, references in separate files
- [ ] **Examples**: Includes concrete usage examples
- [ ] **Progressive Loading**: Large reference materials separated
- [ ] **Platform Compatibility**: Works within target environment constraints
- [ ] **Security**: Audited for potential risks, especially external calls
- [ ] **Testing**: Verified that Claude triggers and uses it correctly
- [ ] **Documentation**: Clear instructions for both Claude and human maintainers

## Resources

- [Official Agent Skills Documentation](https://console.anthropic.com/docs/en/agents-and-tools/agent-skills/overview)
- [Agent Skills Engineering Blog](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills)
- [Official Skills Repository](https://github.com/anthropics/skills)
- [Skills Explained: How Skills compares to prompts, Projects, MCP, and subagents](https://claude.com/blog/skills-explained)

## Summary

**The Golden Rule**: If you find yourself typing the same prompt repeatedly across multiple conversations, it's time to create a Skill.

Effective Skills:
1. Load progressively (metadata → instructions → resources)
2. Have clear, specific descriptions
3. Separate concerns (instructions vs. scripts vs. resources)
4. Work within platform constraints
5. Follow security best practices
6. Are like onboarding guides: clear, structured, and actionable

Think of Skills as teaching Claude expertise that any agent can apply, not just customizing one specific interaction.
