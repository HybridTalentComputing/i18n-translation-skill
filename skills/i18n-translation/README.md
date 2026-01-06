# I18N Translation Agent Skill

A comprehensive Agent Skill for ensuring complete, high-quality internationalization (i18n) translations with support for file splitting in large projects.

## Overview

This Skill solves common i18n problems:
- ✅ **Complete Coverage**: Ensures 100% of translation keys are translated (no partial/incomplete translations)
- ✅ **File Splitting**: Strategies for breaking large i18n files into AI-friendly chunks
- ✅ **Quality Assurance**: Context-aware translations with placeholder preservation
- ✅ **Framework Support**: React i18next, Vue I18n, and general JSON/YAML formats

## When to Use This Skill

Activate this Skill when:
- User mentions: i18n, internationalization, translation, localization, l10n
- User needs multi-language support for their application
- Existing translations are incomplete or partial
- Large i18n files cause AI to lose track and miss translations
- User wants to add a new language to an existing project

## Key Features

### 1. Systematic Translation Process
The Skill follows a rigorous 5-phase process:
1. **Discovery**: Identify existing i18n structure and framework
2. **File Splitting**: Split large files (>200 keys) by feature/domain
3. **Translation**: Systematic translation with 100% coverage guarantee
4. **Validation**: Placeholder preservation, syntax validation, completeness checks
5. **Quality Assurance**: Terminology consistency, context validation

### 2. File Splitting Strategies

**By Feature** (Recommended):
```
locales/
├── en/
│   ├── common.json       # Shared UI elements
│   ├── auth.json         # Authentication flows
│   ├── dashboard.json    # Dashboard features
│   └── settings.json     # Settings pages
```

**By Domain**:
```
locales/
├── en/
│   ├── ui.json           # Buttons, labels, menus
│   ├── messages.json     # Notifications, alerts
│   └── validation.json   # Form validation
```

### 3. Progressive Disclosure

The Skill loads information progressively:
- **SKILL.md**: Main workflow and best practices
- **QUICKSTART.md**: Quick reference for common tasks
- **EXAMPLES.md**: Concrete translation examples
- **strategies/**: Framework-specific guidance (React, Vue, General)
- **scripts/**: Utility scripts for file operations

## File Structure

```
i18n-translation/
├── SKILL.md                      # Main skill documentation
├── QUICKSTART.md                 # Quick reference guide
├── EXAMPLES.md                   # Concrete examples
├── README.md                     # This file
├── strategies/
│   ├── react-i18next.md          # React i18next specific guide
│   ├── vue-i18n.md               # Vue I18n specific guide
│   └── general.md                # General JSON/YAML guide
└── scripts/
    ├── split-i18n.py             # Split large i18n files
    └── validate-i18n.py          # Validate translation completeness
```

## Usage Examples

### Example 1: New Language Addition

**User Request**: "Add Chinese support to my React app"

**Skill Workflow**:
1. Detect framework (React i18next)
2. Find existing i18n files (`public/locales/en/`)
3. Create matching structure for Chinese
4. Translate all keys systematically
5. Validate completeness (100% key parity)
6. Report: "Translated 156/156 keys across 3 files"

### Example 2: Complete Partial Translations

**User Request**: "My German translation is incomplete"

**Skill Workflow**:
1. Compare source (English) vs. target (German) key counts
2. Identify missing keys (e.g., 62 missing out of 156)
3. Add missing translations systematically
4. Validate and report completion

### Example 3: Split Large Files

**User Request**: "Split my 500-key i18n file for better AI editing"

**Skill Workflow**:
1. Analyze key patterns (auth.*, dashboard.*, etc.)
2. Create feature-based split structure
3. Extract keys into separate files
4. Update i18n configuration
5. Provide migration guide

## Utility Scripts

### split-i18n.py

Split large i18n JSON files by feature/prefix:

```bash
python scripts/split-i18n.py locales/en/common.json locales/en/ --by-prefix
```

Output:
```
Loading locales/en/common.json...
Total keys: 523
Analyzing key prefixes...
Key distribution by prefix:
  auth: 78 keys
  dashboard: 156 keys
  settings: 89 keys
  common: 200 keys

Splitting into 4 feature files...
  ✓ Created auth.json (78 keys)
  ✓ Created dashboard.json (156 keys)
  ✓ Created settings.json (89 keys)
  ✓ Created common.json (200 keys)
```

### validate-i18n.py

Validate translation completeness:

```bash
python scripts/validate-i18n.py locales en zh-Hans es
```

Output:
```
Loading en files...
Found 3 files: common, auth, dashboard

==================================================
Language: zh-Hans
==================================================

Validating en -> zh-Hans...
  ✓ Perfect match (45 keys)

Validating en -> zh-Hans...
  ✗ Missing 12 keys in zh-Hans:
    - auth.confirmPassword
    - auth.resetPassword
    ... and 10 more

==================================================
Language: es
==================================================
...
```

## Framework-Specific Guidance

### React i18next
- See [strategies/react-i18next.md](strategies/react-i18next.md)
- Uses `{{variable}}` interpolation syntax
- Supports pluralization with `_plural` suffix
- Namespace-based file organization

### Vue I18n
- See [strategies/vue-i18n.md](strategies/vue-i18n.md)
- Uses `{variable}` interpolation syntax
- Pluralization with pipe `|` separator
- Supports both JSON and YAML formats

### General JSON/YAML
- See [strategies/general.md](strategies/general.md)
- Works with any i18n format
- Auto-detects interpolation style
- Suitable for backend, mobile, desktop apps

## Best Practices

1. **100% Coverage Required**
   - Every source key must have a translation
   - Count keys before/after to verify
   - No partial translations accepted

2. **File Size Limits**
   - Aim for 100-200 keys per file
   - Split larger files before translating
   - Smaller files = better AI editing

3. **Placeholder Preservation**
   - ALL variables must be preserved
   - `{{name}}` → `{{name}}` (not translated)
   - Detect and match source interpolation style

4. **Validation**
   - Validate JSON/YAML after each file
   - Compare key counts between languages
   - Test in application when possible

## Success Criteria

Translation is complete when:
- ✅ All source files have corresponding target files
- ✅ Every key has a translation (100% parity)
- ✅ All placeholders preserved
- ✅ JSON/YAML syntax is valid
- ✅ Files load without errors
- ✅ Terminology is consistent

## Contributing

When improving this Skill:
1. Follow the structure and style of existing documentation
2. Add concrete examples for new scenarios
3. Test with real i18n files
4. Update this README if adding new features

## License

This Skill is part of the agent-skills-coding project and is licensed under the Apache License 2.0.

## Quick Links

- [Main Documentation](SKILL.md)
- [Quick Start Guide](QUICKSTART.md)
- [Examples](EXAMPLES.md)
- [React i18next Guide](strategies/react-i18next.md)
- [Vue I18n Guide](strategies/vue-i18n.md)
- [General JSON/YAML Guide](strategies/general.md)
