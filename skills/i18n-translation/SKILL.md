---
name: i18n-translation
description:
  Intelligent i18n workflow with translation-first approach. Use for: i18n, internationalization,
  translation, localization, l10n, multi-language support, or translating application content.

  ALWAYS creates translation files first (core value). THEN checks debugging capability to determine
  if source code can be auto-modified. If debuggable: auto-modify components + auto-verify.
  If NOT debuggable: provide migration guide only (no code modification).

  Ensures 100% coverage by scanning all file types (.js, .jsx, .ts, .tsx, .vue, .html). Translation
  fidelity: faithful to source with no additions/deletions. Includes secondary quality review
  phase. Supports file splitting (>200 keys).
---

# I18N Translation

Automated internationalization workflow with translation-first approach and intelligent mode detection.

## Quick Start

This skill provides a systematic 8-phase workflow:
1. **String Extraction** - Extract all user-facing strings (ALWAYS)
2. **File Splitting** - Split large files if needed
3. **Translation Files** - Create translations for all languages (ALWAYS)
4. **Debug Detection** - Check if project can be auto-tested
5. **Conditional Integration** - Auto-modify OR migration guide
6. **Validation** - Verify completeness and accuracy
7. **Auto-Verification** - Test if debuggable
8. **Quality Review** - Secondary quality check (ALWAYS)

## When to Use This Skill

- User requests: i18n, internationalization, translation, localization, multi-language support
- Adding new language to existing project
- Completing partial translations
- Splitting large translation files
- Translating application content

## Critical Rules (READ FIRST)

### ✅ TRANSLATION FILES FIRST (ALWAYS CREATE)

**Translation files are ALWAYS created first, regardless of debugging capability:**

This is the core value - providing complete translations for all target languages.

- ✅ **ALWAYS** create translation files (en/, zh-Hans/, es/, etc.)
- ✅ **ALWAYS** extract all hardcoded strings from source
- ✅ **ALWAYS** translate with 100% coverage (zero missing keys)
- ✅ **ALWAYS** preserve placeholders and structure exactly
- ✅ **ALWAYS** validate JSON/YAML syntax

**Translation file creation is NEVER conditional on debugging capability.**

**Value proposition:** Even if source code cannot be modified, translation files have immediate value:
- Can be used by translators for manual integration
- Can be version controlled and tracked
- Provide complete translation coverage
- Enable future integration when project becomes testable

### 🔍 AUTO-DEBUGGING DETECTION (AFTER TRANSLATIONS)

**ONLY AFTER translation files are created, check if project can be auto-tested/debugged:**

```bash
# Detection Checklist
grep -E "(jest|vitest|cypress|playwright|mocha)" package.json  # Test framework?
grep -E '"(dev|start|test)"' package.json                          # Dev scripts?
ls -la vite.config.* webpack.config.* tsconfig.json vue.config.js   # Build config?
[ -d "node_modules" ] && echo "OK" || echo "MISSING"                 # Dependencies installed?
```

**Purpose:** Determine if source code can be safely modified and verified.

**Decision Matrix:**
```
Can Auto-Debug Project?
├── ✅ All 4 checks pass
│     → PROCEED WITH SOURCE CODE MODIFICATION
│     → Install i18n dependencies ✅
│     → Modify ALL component files ✅
│     → Auto-verify integration works ✅
│     → Run tests if available ✅
│
└── ⚠️ Any check fails
      → DO NOT MODIFY SOURCE CODE
      → Keep translation files ✅
      → Generate migration guide ✅
      → Provide before/after examples ✅
      → NO dependency installation ❌
      → NO source code modification ❌
```

**WHY this order:**
1. **Translation first** - Core value, always useful
2. **Debug detection second** - Safety check for code modification
3. **Conditional integration** - Modify only if can verify
4. **Quality review** - Ensure nothing was missed

### ✅ QUALITY REVIEW MANDATE (SECONDARY CHECK)

**After ALL work is complete, perform a secondary quality review:**

**Review Checklist:**
- [ ] **Translation Completeness**: 100% key parity (source vs target)
- [ ] **Placeholder Preservation**: All {{variables}}, {variables}, %variables% present
- [ ] **Syntax Validation**: JSON/YAML files are valid
- [ ] **Fidelity Check**: No additions/deletions/changes to meaning
- [ ] **Structure Match**: Nesting, arrays, data types match source
- [ ] **No Regressions**: Translation didn't introduce issues

**For FULLY AUTOMATED mode (code modified):**
- [ ] Build succeeds (npm run build / yarn build)
- [ ] Dev server starts (npm run dev / yarn dev)
- [ ] No console errors
- [ ] Language switching works
- [ ] All translations display correctly

**For FILES-ONLY mode (code NOT modified):**
- [ ] Migration guide is comprehensive
- [ ] Before/after examples are clear
- [ ] Manual installation steps are complete
- [ ] Integration checklist is provided

**Quality gate:** Do not claim completion until ALL checks pass.

### ✅ COMPLETE COVERAGE MANDATE

**Every user-facing string must be extracted and translated:**

**Scan ALL file types:**
- JavaScript/TypeScript: `.js`, `.jsx`, `.ts`, `.tsx`
- Vue: `.vue`
- Templates: `.html`, `.ejs`, `.hbs`
- Styles: `.css`, `.scss`, `.less` (for content strings)

**Extract ALL string types:**
- UI text: labels, buttons, headings, descriptions
- Messages: toasts, alerts, confirmations
- Validation: error messages, help text
- Placeholders: input placeholders, aria-labels
- Dynamic: template strings with variables

**Document findings:**
- Count total strings extracted
- Categorize by feature/module
- Report coverage statistics

### 🎯 TRANSLATION FIDELITY (CRITICAL)

**ALL translations must be faithful to source:**

1. **No Additions** - Never add words not present in source
2. **No Deletions** - Never omit content from source
3. **No Changes** - Preserve exact meaning and tone
4. **No Improvements** - Don't "fix" or enhance the source

**Translation is not adaptation.** The goal is to convey the EXACT same message in a different language, not to improve or localize the content.

**Preserve Placeholders:**
```
✅ Good: "Hello {{name}}, you have {{count}} messages"
❌ Bad: "你好，你有消息" (missing placeholders)
❌ Bad: "您好 {{name}}，您有 {{count}} 条新消息！" (added exclamation)
```

## Core Workflow

### Phase 1: String Extraction (ALWAYS)

**Extract all hardcoded strings from source code:**

```bash
# Scan all component files
find src -type f \( -name "*.tsx" -o -name "*.jsx" -o -name "*.vue" \)

# Extract strings
grep -rh ">[^<{]*<" src/
grep -rh 'placeholder="[^"]*"' src/
```

**Categorize by type:**
- UI elements: buttons, labels, menus
- Messages: toasts, alerts, notifications
- Validation: error messages, help text
- Content: headings, descriptions

**Output:** List of all strings with counts and categories.

### Phase 2: File Splitting (IF NEEDED)

**Decision: Split if total keys > 200**

**Split by feature (recommended):**
```
locales/
├── en/
│   ├── common.json       # Shared UI (save, cancel, delete)
│   ├── auth.json         # Authentication (login, signup, password)
│   ├── dashboard.json    # Dashboard features
│   ├── settings.json     # Settings pages
│   └── errors.json       # Error messages
```

**Split by domain:**
```
locales/
├── en/
│   ├── ui.json           # Buttons, labels, menus
│   ├── messages.json     # Notifications, alerts
│   └── validation.json   # Form validation
```

**Why split?** Large files cause AI to lose track and miss translations. Smaller files = better quality.

### Phase 3: Translation File Generation (ALWAYS)

**Create source language files (e.g., en/):**
```json
{
  "buttons": {
    "save": "Save",
    "cancel": "Cancel",
    "delete": "Delete"
  },
  "messages": {
    "welcome": "Welcome",
    "loading": "Loading...",
    "success": "Success"
  }
}
```

**Create target language files (e.g., zh-Hans/):**
```json
{
  "buttons": {
    "save": "保存",
    "cancel": "取消",
    "delete": "删除"
  },
  "messages": {
    "welcome": "欢迎",
    "loading": "加载中...",
    "success": "成功"
  }
}
```

**CRITICAL Requirements:**
- ✅ 100% key coverage (zero missing)
- ✅ All placeholders preserved exactly
- ✅ Structure matches source
- ✅ JSON/YAML syntax valid

**This phase ALWAYS executes, regardless of debugging capability.**

### Phase 4: Auto-Debugging Detection

**Execute detection checklist:**

```bash
# 1. Check for test framework
grep -E "(jest|vitest|cypress|playwright|mocha)" package.json

# 2. Check for dev scripts
grep -E '"(dev|start|test)"' package.json

# 3. Check for build config
ls -la vite.config.* webpack.config.* tsconfig.json vue.config.js

# 4. Check dependencies
[ -d "node_modules" ] && echo "OK" || echo "MISSING"
```

**Determine mode:**

**Mode A: Auto-Debugging Possible** (All 4 checks pass)
- Proceed to Phase 5: Source Code Modification

**Mode B: Auto-Debugging NOT Possible** (Any check fails)
- Skip to Phase 6: Migration Guide Generation

### Phase 5: Conditional Source Code Integration

**Mode A: Auto-Debugging Possible → Modify Source Code**

**AI performs:**
1. Install i18n dependencies
2. Modify ALL component files to use translation functions
3. Add i18n configuration
4. Wrap app with provider
5. Add language switcher component

**Example:**
```tsx
// Before
<button>Save</button>

// After
import { useTranslation } from 'react-i18next';
function MyComponent() {
  const { t } = useTranslation();
  return <button>{t('buttons.save')}</button>;
}
```

**Mode B: Auto-Debugging NOT Possible → DO NOT Modify Code**

**AI performs:**
1. Create i18n configuration template
2. Generate comprehensive migration guide
3. Provide before/after examples for each component
4. Document manual integration steps

**Example output:**
```markdown
# I18N Migration Guide

## Translation Files Created
✅ public/locales/en/common.json (156 keys)
✅ public/locales/zh-Hans/common.json (156 keys)

## Manual Installation
npm install i18next react-i18next i18next-browser-languagedetector

## Manual Integration Steps
1. Copy src/i18n/config.ts to your project
2. Import in App.tsx: import './i18n/config';
3. Update components using examples below
...
```

### Phase 6: Validation

**Validate translation files (BOTH modes):**

```bash
# Check JSON syntax
jq . < locales/zh-Hans/common.json

# Compare key counts
echo "Source: $(jq 'keys | length' locales/en/common.json) keys"
echo "Target: $(jq 'keys | length' locales/zh-Hans/common.json) keys"

# Verify all keys present
diff <(jq -r 'keys[]' locales/en/common.json | sort) \
     <(jq -r 'keys[]' locales/zh-Hans/common.json | sort)
```

**Validation checklist:**
- ✅ All keys translated (100% parity)
- ✅ Placeholders preserved
- ✅ JSON/YAML syntax valid
- ✅ Structure matches source

### Phase 7: Auto-Verification (IF DEBUGGABLE)

**Only for Mode A (Auto-Debugging Possible):**

**AI automatically verifies integration:**

1. **Run Build**
   ```bash
   npm run build
   # Verify: No TypeScript errors
   ```

2. **Run Dev Server**
   ```bash
   npm run dev
   # Verify: Server starts without errors
   ```

3. **Test Language Switching**
   - Verify translation keys resolve correctly
   - Check for missing keys in console
   - Test major components

4. **Generate Verification Report**
   ```
   ✓ Build successful (0 errors)
   ✓ Dev server running
   ✓ Language switching functional
   ✓ All translations verified
   ```

### Phase 8: Quality Review (ALWAYS)

**Secondary quality check to ensure nothing was missed:**

**Review ALL translations:**
- [ ] Random sample check (10% of keys)
- [ ] Verify no placeholders were missed
- [ ] Check for consistency in terminology
- [ ] Validate tone is appropriate

**Review integration (if code was modified):**
- [ ] All components updated
- [ ] No hardcoded strings remaining
- [ ] Imports are correct
- [ ] Configuration is valid

**Review migration guide (if code was NOT modified):**
- [ ] Guide is comprehensive
- [ ] Examples are clear and accurate
- [ ] Steps are in logical order
- [ ] Manual tester can follow successfully

**Final quality gate:**
```
✓ Translation files: 100% complete
✓ Placeholders: 100% preserved
✓ Syntax: All files valid
✓ Fidelity: All translations faithful to source
✓ (If auto-modified) Integration: Tested and working
✓ (If files-only) Migration guide: Comprehensive and clear

🎉 I18N WORK COMPLETE
```

## When to Read References

**Load these reference files when needed:**

### Framework-Specific Guidance

- **references/react-i18next.md**
  - Read WHEN: Working with React projects
  - Contains: React-specific patterns, useTranslation hook, I18nextProvider setup

- **references/vue-i18n.md**
  - Read WHEN: Working with Vue projects
  - Contains: Vue-specific patterns, $t() and useI18n(), plugin registration

- **references/general.md**
  - Read WHEN: Working with generic JSON/YAML, Node.js, mobile, desktop apps
  - Contains: General patterns, interpolation detection, file formats

### Detailed Examples

- **references/examples.md**
  - Read WHEN: Need concrete implementation examples
  - Contains: Complete before/after examples, step-by-step walkthroughs

### Best Practices

- **references/best-practices.md**
  - Read WHEN: Need translation quality guidelines
  - Contains: Fidelity principles, quality checklists, common pitfalls

## Using Utility Scripts

**Location:** `scripts/` directory

**Available scripts:**

### extract-strings.py
**Purpose:** Extract hardcoded strings from source code

**Use WHEN:**
- Phase 1: String extraction
- Need to scan large codebases systematically
- Starting i18n from scratch

**Usage:**
```bash
python scripts/extract-strings.py src --format json --output extracted_strings.json
```

**Output:** Categorized strings with counts

### split-i18n.py
**Purpose:** Split large i18n files by feature/prefix

**Use WHEN:**
- Phase 2: File splitting (if > 200 keys)
- Need to organize translations by feature

**Usage:**
```bash
python scripts/split-i18n.py locales/en/common.json locales/en/ --by-prefix
```

**Output:** Multiple smaller files organized by feature

### validate-i18n.py
**Purpose:** Validate translation completeness across languages

**Use WHEN:**
- Phase 6: Validation
- Phase 8: Quality Review
- Checking for missing keys

**Usage:**
```bash
python scripts/validate-i18n.py locales en zh-Hans es
```

**Output:** Report of missing keys, key counts, validation status

## Common Scenarios

### Scenario 1: React Project with Tests (Full Workflow)

**Phase 1-3:** Extract strings, split files, create translations (ALWAYS)
```
✓ Extracted 156 strings from 47 files
✓ Created 6 namespace files
✓ Translated to Chinese (156 keys)
```

**Phase 4:** Auto-Debugging Detection
```
✓ Has Vitest
✓ Has dev script
✓ Has vite.config.ts
✓ Has node_modules
→ Mode A: Auto-Debugging Possible
```

**Phase 5:** Modify Source Code
```
✓ Installed i18next, react-i18next
✓ Modified 47 component files
✓ Added i18n config
✓ Updated App.tsx
```

**Phase 6-7:** Validation and Verification
```
✓ JSON valid
✓ 100% key parity
✓ Build successful
✓ Dev server running
```

**Phase 8:** Quality Review
```
✓ Translation fidelity verified
✓ No hardcoded strings remaining
✓ Language switching functional
```

### Scenario 2: Vue Project without Tests (Translation Only)

**Phase 1-3:** Extract strings, split files, create translations (ALWAYS)
```
✓ Extracted 203 strings from 52 files
✓ Created 5 namespace files
✓ Translated to Chinese (203 keys)
```

**Phase 4:** Auto-Debugging Detection
```
✗ No test framework
✓ Has dev script
✓ Has vite.config.js
✗ No node_modules
→ Mode B: Auto-Debugging NOT Possible
```

**Phase 5:** Generate Migration Guide (NO code modification)
```
✓ Created i18n config template
✓ Generated VUE_MIGRATION_GUIDE.md
✓ Provided before/after examples
✗ Did NOT install packages
✗ Did NOT modify .vue files
```

**Phase 6:** Validation
```
✓ JSON valid
✓ 100% key parity
✓ Placeholders preserved
```

**Phase 7:** Skip (not debuggable)

**Phase 8:** Quality Review
```
✓ Translation fidelity verified
✓ Migration guide comprehensive
✓ Examples clear and accurate
```

**Report:**
```
✓ Translation Files Created: 203 keys across 5 namespaces
✓ Quality Review: Complete
⏸️ Manual Integration Required: See VUE_MIGRATION_GUIDE.md
```

### Scenario 3: Add Language to Existing Project

**Phase 1-3:** Extract from existing translations, create new language
```
✓ Read en/ files (existing)
✓ Created zh-Hans/ files (new language)
✓ Translated 1,245 keys
```

**Phase 4:** Auto-Debugging Detection (uses existing detection result)

**Phase 5-8:** Based on detection (same as Scenario 1 or 2)

## Troubleshooting

### Issue: Build fails after integration

**Mode A (Auto-Debugging Possible):**
1. Check console for TypeScript errors
2. Verify import paths are correct
3. Ensure all translation keys exist
4. Fix errors and re-run build
5. Re-run Phase 7 verification

### Issue: Missing translation keys in console

**Both Modes:**
1. Run validation script: `python scripts/validate-i18n.py`
2. Identify missing keys
3. Add translations to target language files
4. Re-validate
5. Re-run Phase 8 quality review

### Issue: Placeholders not working

**Common causes:**
- Placeholder syntax mismatch ({{var}} vs {var})
- Missing variables in translation function call
- Typo in placeholder name

**Solution:**
- Verify interpolation style matches source
- Check all placeholders preserved in translation
- Ensure variables passed to translation function
- Re-run Phase 8 quality review

## Success Criteria

**Translation is complete when:**

### Translation Files (ALWAYS REQUIRED)
- ✅ Every source key has target translation (100% parity)
- ✅ All placeholders preserved exactly
- ✅ JSON/YAML syntax is valid
- ✅ Structure matches source
- ✅ No missing keys
- ✅ Translation fidelity maintained

### Source Code Integration (Mode A ONLY)
- ✅ Build succeeds (npm run build)
- ✅ Dev server runs (npm run dev)
- ✅ Language switching works
- ✅ No console errors
- ✅ All translations display correctly

### Migration Guide (Mode B ONLY)
- ✅ Guide is comprehensive
- ✅ Installation steps are clear
- ✅ Examples are accurate
- ✅ Integration checklist is complete

### Quality Review (ALWAYS REQUIRED)
- ✅ Random sample check passed
- ✅ Terminology is consistent
- ✅ Tone is appropriate
- ✅ No regressions introduced

**Remember:** Partial translations are worse than no translations. 100% coverage is non-negotiable.
