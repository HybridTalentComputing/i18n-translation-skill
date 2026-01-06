---
name: i18n-translation
description:
  Complete internationalization (i18n) translation workflow for web and software projects.
  Use when user mentions: i18n, internationalization, translation, localization, l10n,
  multi-language support, translation files, JSON/YAML translation, or needs to translate
  application content to multiple languages. Ensures complete coverage with file splitting
  for large projects to optimize AI editing.
---

# I18N Translation

## Quick Start

This Skill provides a systematic approach to internationalizing software applications with complete translation coverage. It handles:

- **Complete Coverage**: Methodical translation of all user-facing text to prevent partial/incomplete translations
- **File Splitting**: Strategies for breaking large i18n files into smaller, AI-friendly chunks
- **Quality Assurance**: Context-aware translations, terminology consistency, and validation
- **Framework Support**: React i18next, Vue I18n, and general JSON/YAML formats

## When to Use This Skill

- User requests internationalization or localization features
- User mentions adding multi-language support
- User needs to translate existing application content
- User wants to split large translation files
- User reports incomplete or partial translations
- User needs to maintain translation consistency across a project

## Core Workflow

### Phase 1: Discovery and Planning

1. **Identify the Project Structure**
   ```bash
   # Find existing i18n files
   find . -name "*.json" -path "*/locales/*" -o -name "*.json" -path "*/i18n/*" -o -name "*.yaml" -path "*/translations/*"
   ```

2. **Detect the Framework**
   - React → i18next (react-i18next)
   - Vue → Vue I18n
   - Angular → @ngx-translate
   - General → JSON/YAML key-value files

3. **Identify Source Language and Target Languages**
   - Ask user: "What is the source language? What languages do you want to support?"

4. **Assess Project Size**
   - Count total translation keys
   - Estimate if files need splitting (> 200 keys per file is a good threshold)

### Phase 2: File Splitting Strategy (For Large Projects)

**CRITICAL**: Large i18n files cause AI to miss translations or stop mid-task. Always split for projects with > 200 translation keys.

#### Splitting Principles

1. **By Feature/Module** (Recommended)
   ```
   locales/
   ├── en/
   │   ├── common.json       # Shared UI elements
   │   ├── auth.json         # Authentication module
   │   ├── dashboard.json    # Dashboard module
   │   ├── settings.json     # Settings module
   │   └── errors.json       # Error messages
   └── zh/
       ├── common.json
       ├── auth.json
       ├── dashboard.json
       ├── settings.json
       └── errors.json
   ```

2. **By Domain/Context**
   ```
   locales/
   ├── en/
   │   ├── ui.json           # Buttons, labels, menus
   │   ├── messages.json     # Notifications, toasts
   │   ├── validation.json   # Form validation messages
   │   └── content.json      # User-generated content
   ```

3. **By Screen/Page** (for very large apps)
   ```
   locales/
   ├── en/
   │   ├── login.json
   │   ├── home.json
   │   ├── profile.json
   │   └── admin.json
   ```

#### Implementation Steps

1. **Create a master source file** (en/common.json) with ALL keys
2. **Split into logical groups** based on your chosen strategy
3. **Create matching structure** for each target language
4. **Document the split strategy** in a I18N_STRUCTURE.md file

**Example Split Command**:
```bash
# Use jq to split a large JSON file
# Or manually organize based on key prefixes (e.g., auth.*, dashboard.*)
```

### Phase 3: Systematic Translation Process

**MANDATORY: Complete Coverage Protocol**

Follow this sequence for EACH target language file:

#### Step 1: File-Level Assessment
```
Before translating, always:
1. Read the entire source file
2. Count total keys
3. Verify file size (aim for < 200 keys per file)
4. Confirm target language and locale
```

#### Step 2: Context Gathering
```
For each translation key:
1. Understand the context (where is it used?)
2. Identify placeholders ({{variable}}, {0}, etc.)
3. Note formatting requirements (dates, currencies, plurals)
4. Check for related UI elements (buttons near forms, etc.)
```

#### Step 3: Translation Execution
```
For EACH key in the file:
1. Translate the source text to target language
2. Preserve ALL placeholders and variables
3. Maintain tone and formality level
4. Keep translations concise (UI text should be brief)
5. Use terminology consistently (define key terms in first file)
```

#### Step 4: Validation
```
After completing a file:
1. Verify ALL keys are translated (zero missing)
2. Check placeholder syntax matches source
3. Validate JSON/YAML syntax
4. Test length constraints (e.g., German text can be 30% longer)
5. Ensure no encoding issues
```

#### Step 5: Completeness Check
```
MANDATORY: Before claiming completion:
1. Count keys in source vs. target files
2. They MUST match exactly
3. Any missing keys = incomplete translation
4. Report: "Translated X/Y keys for [filename]"
```

### Phase 4: Quality Assurance

1. **Terminology Consistency**
   - Create a glossary for domain-specific terms
   - Use consistent translations for key terms across files
   - Save as [LANGUAGE]_GLOSSARY.md

2. **Context Validation**
   - Review translations in actual UI when possible
   - Check for awkward phrasing or culturally inappropriate content
   - Verify date/number/currency formats

3. **Regression Testing**
   - After code changes, identify new translation keys
   - Add them to ALL language files
   - Maintain parity across all languages

## Translation Best Practices

### General Rules

1. **Preserve Placeholders**
   ```
   Source: "Hello {{name}}, you have {{count}} messages"
   ❌ Bad: "你好，你有消息"
   ✅ Good: "你好 {{name}}，你有 {{count}} 条消息"
   ```

2. **Maintain Tone**
   - Formal: Use formal address (您 instead of 你 in Chinese)
   - Casual: Match the source informality level
   - Consistent: Keep tone consistent across all files

3. **Consider Length**
   - UI elements (buttons, labels): Keep translations 30% shorter than source
   - Long-form content: Can expand up to 50% depending on language
   - German, Russian: Allow for 30% expansion
   - Chinese, Korean: Often more concise than English

4. **Handle Special Cases**

   **Plurals**:
   ```json
   {
     "message_count": {
       "zero": "No messages",
       "one": "One message",
       "other": "{{count}} messages"
     }
   }
   ```

   **Gender**:
   ```json
   {
     "welcome": "Welcome, {{gender, select, male{Mr.} female{Ms.} other{Dear}}} {{name}}"
   }
   ```

   **Dates/Currency**:
   ```json
   {
     "price": "Price: {{value, currency, USD}}",
     "date": "Date: {{value, date, long}}"
   }
   ```

### Framework-Specific Guidelines

See strategy files for detailed guidance:
- [React i18next Strategy](./strategies/react-i18next.md)
- [Vue I18n Strategy](./strategies/vue-i18n.md)
- [General JSON/YAML Strategy](./strategies/general.md)

## Common Pitfalls to Avoid

### 1. Incomplete Translation
**Problem**: AI stops after translating 50-70% of keys

**Solution**:
- Always work file-by-file
- Count keys before and after
- Explicitly verify completion before moving on
- Use the Completeness Check (Phase 3, Step 5)

### 2. Broken File Syntax
**Problem**: Missing commas, unclosed braces

**Solution**:
- Validate JSON/YAML after each file
- Use tools: `jq . < file.json` for JSON validation
- Test files load in the application

### 3. Lost Placeholders
**Problem**: Variables removed during translation

**Solution**:
- Double-check every translation contains ALL placeholders
- Use automated validation if possible
- Compare placeholder counts: source vs. target

### 4. Inconsistent Terminology
**Problem**: Same word translated differently across files

**Solution**:
- Create and maintain a glossary
- Review terminology after first file is complete
- Reference glossary for all subsequent files

### 5. File Too Large
**Problem**: Single file with 500+ keys causes AI to lose track

**Solution**:
- Split files by feature/domain BEFORE translating
- Aim for 100-200 keys per file
- Use systematic naming convention

## Progress Tracking

Always provide progress updates to the user:

```
✓ Completed: common.json (45 keys)
✓ Completed: auth.json (32 keys)
⏳ In Progress: dashboard.json (78/120 keys)
⏸️ Pending: settings.json (0 keys)
⏸️ Pending: errors.json (0 keys)

Overall Progress: 77/229 keys (33.6%)
```

## When to Split Files

Use this decision tree:

```
Total keys in project > 200?
│
├── YES → Can you group by feature/module?
│         │
│         ├── YES → Split by feature/module
│         └── NO → Split by domain/context
│
└── NO → Single file is acceptable
```

**Recommended thresholds**:
- < 100 keys: Single file
- 100-500 keys: Split by feature (3-5 files)
- 500-1000 keys: Split by feature (5-10 files)
- > 1000 keys: Split by feature + domain (10+ files)

## Additional Resources

- [EXAMPLES.md](./EXAMPLES.md) - Concrete translation examples
- [strategies/react-i18next.md](./strategies/react-i18next.md) - React-specific guidance
- [strategies/vue-i18n.md](./strategies/vue-i18n.md) - Vue-specific guidance
- [strategies/general.md](./strategies/general.md) - General JSON/YAML guidance

## Emergency Recovery

If translation process is interrupted:

1. **Assess Current State**
   ```bash
   # Find partially translated files
   # Compare key counts between source and target
   ```

2. **Resume Strategy**
   - Identify last completed file
   - Start next file fresh
   - Don't try to "continue" mid-file

3. **Validation**
   - Verify all previously completed files are intact
   - Re-validate JSON/YAML syntax
   - Continue systematic process

## Success Criteria

Translation is complete when:
- ✅ All source files have corresponding target language files
- ✅ Every key in source has a translation in target (100% parity)
- ✅ All placeholders and variables preserved
- ✅ JSON/YAML syntax is valid
- ✅ Files load without errors in the application
- ✅ Terminology is consistent across all files
- ✅ Context and tone are appropriate for target audience

Remember: **Complete coverage is non-negotiable**. Partial translations are worse than no translations.
