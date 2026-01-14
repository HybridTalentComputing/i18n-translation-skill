# General JSON/YAML Translation Strategy

This guide covers translation strategies for general JSON and YAML i18n files that don't use framework-specific libraries like React i18next or Vue I18n.

## ⚠️ CRITICAL RULES

### AUTO-DEBUGGING CAPABILITY DETECTION (CRITICAL)

**Before any installation or code modification, AI checks:**

**Detection Checklist:**
```bash
# 1. Check for test framework
grep -E "(jest|vitest|mocha|jasmine)" package.json

# 2. Check for test/run scripts
grep -E '"(test|start|dev)"' package.json

# 3. Check for build configuration
ls -la package.json tsconfig.json 2>/dev/null

# 4. Verify node_modules exists
[ -d "node_modules" ] && echo "OK" || echo "MISSING"
```

**Decision Matrix:**
```
Can Auto-Debug?
├── ✅ Has test framework + Has test scripts + Has build config + Has node_modules
│     → FULLY AUTOMATED MODE
│     → Install i18n packages ✅
│     → Modify source files ✅
│     → Auto-verify with tests ✅
│
└── ⚠️ Missing any of the above
      → FILES-ONLY MODE
      → Create translation files ✅
      → Generate migration guide ✅
      → NO installation ❌
      → NO code modification ❌
```

### FULLY AUTOMATED MODE (When debugging possible)

**Detection Result:** Project can be auto-tested/debugged

**AI performs ALL tasks automatically:**
- ✅ Install i18n dependencies (i18next, etc.)
- ✅ Extract all hardcoded strings
- ✅ Generate translation files
- ✅ Modify ALL component files
- ✅ Add configuration files
- ✅ Auto-verify with tests

**No manual intervention required.**

### FILES-ONLY MODE (When debugging NOT possible)

**Detection Result:** Project cannot be auto-tested/debugged

**AI performs ONLY these tasks:**
- ✅ Create translation files
- ✅ Create config templates
- ✅ Generate comprehensive migration guide
- ✅ Provide before/after examples

**AI does NOT perform:**
- ❌ NO dependency installation
- ❌ NO source code modification
- ❌ NO config file changes

**User must manually:**
1. Install dependencies
2. Follow migration guide
3. Update components manually
4. Test manually

### Complete Coverage Requirement

**Every user-facing string must be extracted:**
- Scan: .js, .jsx, .ts, .tsx, .vue, .html, .css, .scss files
- Extract: UI text, messages, validation, placeholders, aria-labels
- Document: Count strings found and categorize by feature

## When to Use This Strategy

Use this approach for:
- Backend API translations
- Node.js applications
- Mobile apps (React Native, Flutter)
- Desktop applications (Electron)
- Custom i18n implementations
- Generic JSON/YAML translation files

## Comprehensive String Extraction Workflow

### Step 1: Scan All Source Files

```bash
# Find all JavaScript/TypeScript files
find src -type f \( -name "*.js" -o -name "*.jsx" -o -name "*.ts" -o -name "*.tsx" \)

# Find all Vue files
find src -type f -name "*.vue"

# Find all template files
find . -type f \( -name "*.html" -o -name "*.ejs" -o -name "*.hbs" \)

# Count total files to scan
echo "Total source files: $(find src -type f \( -name "*.js" -o -name "*.jsx" -o -name "*.ts" -o -name "*.tsx" -o -name "*.vue" \) | wc -l)"
```

### Step 2: Extract User-Facing Strings

**React/Vue Components:**
```bash
# Extract JSX/Vue template strings
grep -rh ">[^<{]*<" src/ | grep -v "^[[:space:]]*$" | sort -u | head -100

# Find button/label text
grep -rh "button.*>[^<]*<" src/
grep -rh "label.*>[^<]*<" src/
grep -rh "placeholder=["] src/
```

**JavaScript/TypeScript Strings:**
```bash
# Find string literals related to UI
grep -rh "['\"]\w\+\(\s\+\w\+\)*['\"]" src/ --include="*.js" --include="*.ts" | \
  grep -E "(button|label|title|message|error|success|warning|text|placeholder|loading)" | \
  sort -u | head -100
```

### Step 3: Categorize Strings

Group extracted strings into categories:

1. **common** - Universal UI (buttons, status, navigation)
2. **[feature]** - Feature-specific (auth, dashboard, settings, etc.)
3. **validation** - Form validation messages
4. **errors** - Error messages

### Step 4: Create Translation Files

Based on categorized strings, create JSON/YAML files for each language.

### Step 5: Automatic Code Integration

**AI automatically modifies ALL component files:**
- Replace hardcoded strings with translation function calls
- Import necessary i18n libraries
- Update all template literals and JSX content
- Ensure all components use translation keys

**No migration guide needed** - AI performs all code modifications directly.

## File Format Detection

### JSON Format
```json
{
  "key": "value",
  "nested": {
    "key": "value"
  }
}
```

### YAML Format
```yaml
key: value
nested:
  key: value
```

## Common File Locations

```
locales/
translations/
i18n/
lang/
config/locales/
src/translations/
```

## File Structure Patterns

### Flat Structure (Simple)
```
locales/
├── en.json
├── zh-Hans.json
└── es.json
```

### Nested Structure (By Language)
```
locales/
├── en/
│   └── messages.json
├── zh-Hans/
│   └── messages.json
└── es/
    └── messages.json
```

### Modular Structure (Large Projects)
```
locales/
├── en/
│   ├── common.json
│   ├── auth.json
│   └── errors.json
├── zh-Hans/
│   ├── common.json
│   ├── auth.json
│   └── errors.json
└── es/
    ├── common.json
    ├── auth.json
    └── errors.json
```

## Translation Syntax Patterns

### 1. Simple Key-Value

**JSON:**
```json
// English
{
  "welcome": "Welcome",
  "goodbye": "Goodbye"
}

// Chinese
{
  "welcome": "欢迎",
  "goodbye": "再见"
}
```

**YAML:**
```yaml
# English
welcome: Welcome
goodbye: Goodbye

# Chinese
welcome: 欢迎
goodbye: 再见
```

### 2. Nested Keys

**JSON:**
```json
// English
{
  "user": {
    "name": "Name",
    "email": "Email",
    "password": "Password"
  }
}

// Chinese (maintain nesting)
{
  "user": {
    "name": "姓名",
    "email": "电子邮箱",
    "password": "密码"
  }
}
```

**YAML:**
```yaml
# English
user:
  name: Name
  email: Email
  password: Password

# Chinese
user:
  name: 姓名
  email: 电子邮箱
  password: 密码
```

### 3. Interpolation (Multiple Styles)

**Style A: Double Curly Braces**
```json
{
  "greeting": "Hello {{name}}",
  "message": "You have {{count}} messages"
}
```

**Style B: Single Curly Braces**
```json
{
  "greeting": "Hello {name}",
  "message": "You have {count} messages"
}
```

**Style C: Percent Sign**
```json
{
  "greeting": "Hello %name%",
  "message": "You have %count% messages"
}
```

**Style D: Dollar Sign**
```json
{
  "greeting": "Hello $name",
  "message": "You have $count messages"
}
```

**CRITICAL**: Detect the interpolation style from the source file and preserve it exactly in translations.

### 4. Positional Interpolation

```json
// English
{
  "message": "Hello {0}, you have {1} messages"
}

// Chinese (maintain positions)
{
  "message": "你好 {0}，您有 {1} 条消息"
}
```

### 5. Pluralization

**Pattern A: Separate Keys**
```json
{
  "item_one": "One item",
  "item_other": "{{count}} items",
  "item_zero": "No items"
}
```

**Pattern B: Pipe Separated**
```json
{
  "item": "no items | one item | {{count}} items"
}
```

**Pattern C: Nested**
```json
{
  "item": {
    "zero": "No items",
    "one": "One item",
    "other": "{{count}} items"
  }
}
```

## Splitting Strategy

### Decision Tree

```
Total keys in file > 200?
├── YES → Can you group by feature?
│         ├── YES → Split by feature
│         └── NO → Split by domain
└── NO → Single file is OK
```

### Split by Feature

```
messages.json (350 keys)
├── auth.json (75 keys)
├── dashboard.json (100 keys)
├── settings.json (80 keys)
├── notifications.json (60 keys)
└── errors.json (35 keys)
```

### Split by Domain

```
messages.json (400 keys)
├── ui.json (120 keys) - buttons, labels, menus
├── validation.json (80 keys) - form validation
├── messages.json (100 keys) - notifications, alerts
└── content.json (100 keys) - page content
```

## Translation Workflow

### Phase 1: File Analysis

```bash
# Detect file format
file en/messages.json
# Output: JSON data

file en/messages.yaml
# Output: YAML text

# Count total keys
jq 'keys | length' en/messages.json  # JSON
# or
yq eval '.keys | length' en/messages.yaml  # YAML

# Detect interpolation style
grep -oE '\{\{[^}]+\}\}|\{[^}]+\}|%[^%]+%' en/messages.json | head -5
```

### Phase 2: Create Target Structure

```bash
# Create matching directory structure
cp -r en zh-Hans

# Or create empty files
mkdir -p zh-Hans
touch zh-Hans/messages.json
```

### Phase 3: Systematic Translation

**CRITICAL: Translation Fidelity Rules**

Before translating, ensure:
1. ✅ **Faithful to source** - Translate EXACTLY what source says
2. ✅ **No additions** - Don't add words or explanations
3. ✅ **No deletions** - Don't omit content from source
4. ✅ **No changes** - Preserve exact meaning and tone
5. ✅ **Structure preservation** - Keep placeholders, formatting, HTML

For each translation key:
1. **Read the key-value pair**
2. **Identify placeholders** - Note all interpolation patterns
3. **Translate the text** - Preserve placeholders exactly, translate faithfully
4. **Maintain structure** - Keep nesting, arrays, etc.
5. **Validate syntax** - Check JSON/YAML is valid

### Phase 4: Validation

```bash
# JSON validation
jq . < zh-Hans/messages.json > /dev/null && echo "✓ Valid JSON" || echo "✗ Invalid JSON"

# YAML validation
yq eval zh-Hans/messages.yaml > /dev/null && echo "✓ Valid YAML" || echo "✗ Invalid YAML"

# Compare key counts
echo "Source: $(jq 'keys | length' en/messages.json) keys"
echo "Target: $(jq 'keys | length' zh-Hans/messages.json) keys"

# Verify all keys present
diff <(jq -r 'keys[]' en/messages.json | sort) \
     <(jq -r 'keys[]' zh-Hans/messages.json | sort)
```

### Phase 5: Completeness Check

```
MANDATORY: Before claiming completion:
1. Count keys in source file
2. Count keys in target file
3. They MUST match exactly
4. Any missing keys = incomplete translation
```

## Common Patterns by Category

### Navigation
```json
{
  "nav": {
    "home": "Home",
    "about": "About",
    "contact": "Contact",
    "dashboard": "Dashboard",
    "settings": "Settings",
    "logout": "Logout"
  }
}
```

### Actions
```json
{
  "actions": {
    "save": "Save",
    "cancel": "Cancel",
    "delete": "Delete",
    "edit": "Edit",
    "create": "Create",
    "update": "Update",
    "submit": "Submit",
    "confirm": "Confirm"
  }
}
```

### Validation
```json
{
  "validation": {
    "required": "{{field}} is required",
    "invalid": "Invalid {{field}}",
    "minLength": "{{field}} must be at least {{min}} characters",
    "maxLength": "{{field}} cannot exceed {{max}} characters",
    "email": "Please enter a valid email address",
    "url": "Please enter a valid URL"
  }
}
```

### Status
```json
{
  "status": {
    "loading": "Loading...",
    "success": "Success",
    "error": "Error",
    "warning": "Warning",
    "info": "Information"
  }
}
```

### Time
```json
{
  "time": {
    "today": "Today",
    "yesterday": "Yesterday",
    "tomorrow": "Tomorrow",
    "lastWeek": "Last week",
    "nextWeek": "Next week",
    "lastMonth": "Last month",
    "nextMonth": "Next month"
  }
}
```

## Special Considerations

### 1. Arrays

```json
// English
{
  "items": ["First", "Second", "Third"]
}

// Chinese (maintain array structure)
{
  "items": ["第一", "第二", "第三"]
}
```

### 2. Boolean/Number Values

```json
// English
{
  "settings": {
    "enabled": true,
    "count": 42,
    "rate": 3.14
  }
}

// Chinese (non-translatable values stay the same)
{
  "settings": {
    "enabled": true,
    "count": 42,
    "rate": 3.14
  }
}
```

Only translate string values, preserve booleans and numbers.

### 3. Empty Strings

```json
{
  "placeholder": "Enter text...",
  "empty": ""
}
```

Preserve empty strings - they may be intentional.

### 4. HTML/Markdown

```json
{
  "description": "Click <a href='/help'>here</a> for **help**",
  "instruction": "1. Do this\n2. Do that\n3. Done"
}
```

Preserve HTML tags and Markdown formatting.

## Validation Scripts

### JSON Validation Script

```bash
#!/bin/bash
# validate-json.sh

for file in "$@"; do
  if jq . < "$file" > /dev/null 2>&1; then
    echo "✓ $file"
  else
    echo "✗ $file (Invalid JSON)"
    exit 1
  fi
done
```

### YAML Validation Script

```bash
#!/bin/bash
# validate-yaml.sh

for file in "$@"; do
  if yq eval "$file" > /dev/null 2>&1; then
    echo "✓ $file"
  else
    echo "✗ $file (Invalid YAML)"
    exit 1
  fi
done
```

### Key Count Comparison Script

```bash
#!/bin/bash
# compare-keys.sh

SOURCE="$1"
TARGET="$2"

if [ ! -f "$SOURCE" ] || [ ! -f "$TARGET" ]; then
  echo "Usage: compare-keys.sh <source> <target>"
  exit 1
fi

# Determine format (JSON or YAML)
if [[ "$SOURCE" == *.json ]]; then
  SOURCE_KEYS=$(jq -r 'keys[]' "$SOURCE" | sort)
  TARGET_KEYS=$(jq -r 'keys[]' "$TARGET" | sort)
elif [[ "$SOURCE" == *.yaml ]] || [[ "$SOURCE" == *.yml ]]; then
  SOURCE_KEYS=$(yq eval 'keys | .[]' "$SOURCE" | sort)
  TARGET_KEYS=$(yq eval 'keys | .[]' "$TARGET" | sort)
else
  echo "Unsupported file format"
  exit 1
fi

# Compare
MISSING=$(comm -23 <(echo "$SOURCE_KEYS") <(echo "$TARGET_KEYS"))
EXTRA=$(comm -13 <(echo "$SOURCE_KEYS") <(echo "$TARGET_KEYS"))

if [ -n "$MISSING" ]; then
  echo "Missing keys in target:"
  echo "$MISSING"
fi

if [ -n "$EXTRA" ]; then
  echo "Extra keys in target:"
  echo "$EXTRA"
fi

if [ -z "$MISSING" ] && [ -z "$EXTRA" ]; then
  echo "✓ Key counts match perfectly"
fi
```

## Best Practices Summary

**Key Rules for General JSON/YAML Translation:**

1. **Detect Interpolation Style** - Look for `{{}}`, `{}`, `%`, `$` patterns
2. **Preserve Placeholders** - Never modify or remove interpolation syntax
3. **Maintain Structure** - Keep nesting, arrays, data types unchanged
4. **Validate Syntax** - Check JSON/YAML validity after each file
5. **Compare Key Counts** - Ensure 100% parity between source and target
6. **Handle Special Cases** - HTML, Markdown, arrays, booleans
7. **Split Large Files** - >200 keys should be split by feature/domain

**Quality Checks:**
- ✅ All keys translated
- ✅ Placeholders preserved
- ✅ JSON/YAML syntax valid
- ✅ Structure matches source
- ✅ Special characters preserved

**Remember**: Different projects use different interpolation syntax. Always detect and preserve the exact style used in the source file!
