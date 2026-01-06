# I18N Translation - Quick Start

## 5-Minute Overview

This Skill ensures **complete, high-quality internationalization** with **file splitting for large projects**.

## When to Use

- User mentions: i18n, translation, localization, multi-language
- Existing translations are incomplete
- Large i18n files cause issues
- Adding language support to existing project

## Quick Decision Tree

```
Project has i18n files?
├── YES → Are they complete?
│         ├── YES → Add new language or maintain existing
│         └── NO → Complete the translations
└── NO → Set up i18n structure from scratch
```

## 3-Step Process

### 1. Discovery (Do this first!)
```bash
# Find existing i18n files
find . -name "*.json" -path "*/locales/*" -o -name "*.json" -path "*/i18n/*"

# Identify framework
grep -r "i18next\|vue-i18n\|@ngx-translate" package.json
```

### 2. File Splitting (If > 200 keys)
```
✓ Split by feature/module: auth.json, dashboard.json, settings.json
✓ Or split by domain: ui.json, messages.json, validation.json
✓ Create matching structure for each target language
```

### 3. Systematic Translation
```
For EACH language file:
1. Read entire source file
2. Count total keys
3. Translate EVERY key (mandatory)
4. Validate placeholders preserved
5. Verify JSON/YAML syntax
6. Report: "Translated X/Y keys for [filename]"
```

## Critical Rules

### ⚠️ NON-NEGOTIABLE

1. **100% Coverage Required**
   - Every source key MUST have a translation
   - Count keys before/after to verify
   - No partial translations accepted

2. **File Size Limits**
   - Aim for 100-200 keys per file
   - Split larger files BEFORE translating
   - Smaller files = better AI editing

3. **Placeholder Preservation**
   - ALL variables/interpolations must be preserved
   - `{{name}}` → `{{name}}` (not translated)
   - `{0}`, `{1}` → Must remain in translation

4. **Validation After Each File**
   - Check JSON syntax: `jq . < file.json`
   - Verify key counts match source
   - Test in application if possible

## File Splitting Examples

### By Feature (Recommended)
```
locales/
├── en/
│   ├── common.json       # 45 keys
│   ├── auth.json         # 32 keys
│   ├── dashboard.json    # 78 keys
│   └── settings.json     # 51 keys
└── zh/
    ├── common.json
    ├── auth.json
    ├── dashboard.json
    └── settings.json
```

### By Domain
```
locales/
├── en/
│   ├── ui.json           # Buttons, labels, menus
│   ├── messages.json     # Notifications, alerts
│   ├── validation.json   # Form errors
│   └── content.json      # Page content
```

## Translation Checklist

For each file:
- [ ] Read entire source file first
- [ ] Count total keys
- [ ] Translate all keys (100%)
- [ ] Verify placeholders preserved
- [ ] Validate JSON/YAML syntax
- [ ] Report completion: "Translated X/Y keys"

## Framework Quick Reference

| Framework | Location Pattern | File Format |
|-----------|-----------------|-------------|
| React (i18next) | `public/locales/` or `src/i18n/locales/` | JSON |
| Vue (vue-i18n) | `src/locales/` | JSON or YAML |
| Angular | `src/assets/i18n/` | JSON |
| General | Any `locales/` or `translations/` | JSON/YAML |

## Common Commands

```bash
# Find all i18n files
find . -type f \( -name "*.json" -o -name "*.yaml" -o -name "*.yml" \) -path "*/locale*"

# Count keys in JSON file
jq 'keys | length' en/common.json

# Validate JSON syntax
jq . < en/common.json > /dev/null && echo "Valid" || echo "Invalid"

# Compare key counts between source and target
echo "Source: $(jq 'keys | length' en/common.json)"
echo "Target: $(jq 'keys | length' zh/common.json)"
```

## Progress Tracking Template

```
📊 Translation Progress: English → Chinese

✓ Completed: common.json (45/45 keys)
✓ Completed: auth.json (32/32 keys)
⏳ In Progress: dashboard.json (45/78 keys)
⏸️ Pending: settings.json (0/51 keys)

Total: 77/206 keys (37.4%)
```

## Emergency Recovery

If interrupted:
1. Identify last completed file
2. Start next file from beginning
3. Don't continue mid-file
4. Re-validate all completed files

## Need More Detail?

- [Full Documentation](./SKILL.md)
- [Examples](./EXAMPLES.md)
- [React Strategy](./strategies/react-i18next.md)
- [Vue Strategy](./strategies/vue-i18n.md)

## Remember

> **Complete coverage is non-negotiable. Partial translations are worse than no translations.**

Always verify 100% key parity between source and target files.
