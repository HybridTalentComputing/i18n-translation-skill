---
name: i18n-complete
description: Complete internationalization implementation for web applications. Provides systematic AI-driven workflow to achieve 100% i18n coverage with zero hardcoded strings. Use for adding i18n to new projects, migrating hardcoded strings to i18n, adding new language support, or auditing i18n coverage. Includes extraction patterns, component migration strategies, namespace organization, and validation checklists. Works with React, Vue, Angular, and similar frameworks. No scripts required - all work done by AI following structured methodology.
---

# i18n-Complete: Full Internationalization Implementation

Implement complete internationalization (i18n) for web applications with 100% coverage. This skill provides a systematic, AI-driven workflow to eliminate all hardcoded strings and establish a scalable translation system.

## Quick Start

For immediate i18n implementation:

1. **Read the complete workflow:** See [workflow.md](references/workflow.md) for the 5-phase process
2. **Plan file structure:** See [modular-files.md](references/modular-files.md) for splitting strategy
3. **Extract strings systematically:** Process every component, extract ALL user-facing text
4. **Set up infrastructure:** Install i18next, create modular translation files
5. **Migrate components:** Replace hardcoded strings with `t()` calls
6. **Validate thoroughly:** Ensure zero hardcoded strings remain

**⚠️ Important:** For projects with > 1000 strings, you MUST split translation files by namespace. See [modular-files.md](references/modular-files.md) for complete guidance.

**Expected outcome:** 100% of UI text uses i18n system, application works flawlessly in all supported languages.

---

## When to Use This Skill

Use this skill when:

- Adding i18n to a new project
- Migrating existing hardcoded strings to i18n
- Adding support for additional languages
- Auditing or improving existing i18n implementation
- Ensuring complete i18n coverage

**Key principle:** 100% coverage is the only acceptable standard. Zero hardcoded strings in UI.

---

## Core Methodology

### The 5-Phase Workflow

**Phase 1: Project Analysis** (5-10 min)
- Identify framework, build tool, and component structure
- Check for existing i18n setup
- Create component inventory
- Design namespace structure

**Phase 2: String Extraction** (30-60 min)
- Systematically read each component
- Extract ALL user-facing strings (text, placeholders, labels, messages, etc.)
- Organize by namespace and component
- Create master translation list

**Phase 3: Translation Infrastructure** (15-20 min)
- Install i18next (or framework-appropriate library)
- Create i18n configuration
- Create complete translation files for all languages
- Add type definitions (if TypeScript)

**Phase 4: Component Migration** (40-80 min)
- Update each component to use `useTranslation` hook
- Replace ALL hardcoded strings with `t()` calls
- Handle interpolation, plurals, and complex patterns
- Ensure zero hardcoded strings remain

**Phase 5: Validation** (10-15 min)
- Verify no hardcoded strings remain (search patterns)
- Validate translation file syntax and consistency
- Test language switching
- Verify translation quality
- Complete all checklist items

**Total time:** 1.5-3 hours for typical app (50-100 components)

### Success Criteria

✅ 100% of user-facing text uses i18n
✅ Zero hardcoded strings in UI components
✅ Translation files complete for all languages
✅ Application works perfectly in all supported languages
✅ No console errors or warnings

---

## Implementation Guide

### Step 1: Understand the Project

Before touching any code:

1. **Identify the framework:**
   - React → use `i18next` + `react-i18next`
   - Vue → use `vue-i18n`
   - Angular → use `@ngx-translate/core`
   - Other → check framework documentation

2. **Analyze component structure:**
   ```bash
   Glob: "src/components/**/*.{tsx,jsx,vue}"
   Glob: "src/views/**/*.{tsx,jsx,vue}"
   ```

3. **Check existing i18n:**
   ```bash
   Grep: "i18n|i18next|vue-i18n" (case insensitive)
   ```

4. **Create component inventory:**
   - List all components by category (layout, features, common, utility)
   - Note components with heavy UI text
   - Identify migration priority

### Step 2: Extract All Strings

For **each component**, without exception:

1. Read the component file
2. Extract **every** user-facing string:
   - Text content: `<div>Hello World</div>`
   - Labels: `<label>Email</label>`
   - Placeholders: `<input placeholder="Enter email" />`
   - Button text: `<button>Submit</button>`
   - Headings: `<h1>Dashboard</h1>`
   - Messages: `<p>Error occurred</p>`
   - Attributes: `title`, `aria-label`, `alt`
   - Options: `<option>English</option>`

3. Determine appropriate namespace
4. Create translation key using naming conventions
5. Add to master translation list

**Pattern to follow:**

```
For component: src/components/chat/ChatView.tsx

Extracted strings:
- "Chat" → chat.chatView.title
- "New Conversation" → chat.chatView.newConversation
- "Type a message..." → chat.chatView.inputPlaceholder
- "Send" → chat.chatView.sendButton
```

### Step 3: Set Up i18n Infrastructure

**For React projects:**

1. Install dependencies:
   ```bash
   npm install i18next react-i18next i18next-browser-languagedetector
   ```

2. Create configuration (`src/i18n/config.ts`):
   ```typescript
   import i18n from "i18next"
   import { initReactI18next } from "react-i18next"
   import LanguageDetector from "i18next-browser-languagedetector"

   import enTranslations from "./locales/en.json"
   import zhTranslations from "./locales/zh.json"

   i18n
     .use(LanguageDetector)
     .use(initReactI18next)
     .init({
       resources: {
         en: { translation: enTranslations },
         zh: { translation: zhTranslations },
       },
       fallbackLng: "en",
       lng: "en",
       interpolation: { escapeValue: false },
     })

   export default i18n
   ```

3. Create translation files:
   - `src/i18n/locales/en.json` - Copy all extracted strings here
   - `src/i18n/locales/zh.json` - Translate all values to Chinese

4. Initialize in main entry point:
   ```typescript
   import "./i18n/config" // Must be first import
   ```

### Step 4: Migrate All Components

For **each component**:

1. Add `useTranslation` hook:
   ```typescript
   import { useTranslation } from "react-i18next"

   export const MyComponent: React.FC = () => {
     const { t } = useTranslation("namespace")
   ```

2. Replace **every** hardcoded string:
   ```tsx
   // Before
   <h1>Settings</h1>
   <button>Save</button>
   <input placeholder="Enter email" />

   // After
   <h1>{t("title")}</h1>
   <button>{t("save")}</button>
   <input placeholder={t("emailPlaceholder")} />
   ```

3. Handle special cases:
   - Interpolation: `t("greeting", { name: userName })`
   - Conditionals: `t(isLoading ? "loading" : "complete")`
   - Multiple namespaces: `const { t: tCommon } = useTranslation("common")`

4. Verify component still works

**Pattern examples:** See [patterns.md](references/patterns.md) for 20+ detailed examples.

### Step 5: Validate Thoroughly

**Complete these checks:**

1. **Search for remaining hardcoded strings:**
   ```bash
   Grep: all components for text patterns
   Expected: Zero user-facing hardcoded strings
   ```

2. **Validate translation files:**
   - Verify JSON syntax
   - Ensure key consistency between languages
   - Check no missing translations
   - Verify no placeholder text

3. **Test language switching:**
   - Load app in English
   - Switch to Chinese
   - Verify ALL text changes
   - Check console for errors

4. **Review translation quality**
5. **Complete checklist:** See [checklist.md](references/checklist.md)

---

## Reference Documentation

### Comprehensive Guides

**[workflow.md](references/workflow.md)** - Complete 5-phase workflow
- Detailed process for each phase
- Execution strategies
- Quality standards
- Time estimates
- Common pitfalls

**[patterns.md](references/patterns.md)** - Translation patterns and examples
- 20+ real-world examples
- Before/after code comparisons
- Common patterns (interpolation, plurals, etc.)
- Component-specific patterns
- Mistakes to avoid

**[namespaces.md](references/namespaces.md)** - Namespace organization
- Namespace principles and best practices
- Recommended structure
- Naming conventions
- Category guidelines
- Anti-patterns to avoid

**[checklist.md](references/checklist.md)** - Complete validation checklists
- Phase-specific checklists
- Quality criteria
- Acceptance criteria
- Common issues to check

---

## Key Principles

### 1. Completeness is Non-Negotiable

**100% coverage means:**
- Every user-facing string uses i18n
- No "small strings" overlooked
- No "we'll do this later" exceptions
- Zero tolerance for hardcoded text

### 2. Systematic Processing

**Process components methodically:**
- One component at a time
- Every string extracted
- Every component migrated
- No skipping ahead

### 3. Organize by Namespace

**Use logical namespaces:**
- `common` - Shared UI elements
- `{feature}` - Feature-specific strings
- `settings` - Settings/configuration
- `errors` - Error messages
- etc.

See [namespaces.md](references/namespaces.md) for complete guide.

### 4. Quality Over Speed

**Don't rush:**
- Each phase must be complete before moving to next
- Use checklists to verify
- Validate thoroughly
- Fix issues immediately

### 5. Test Everything

**Verification is critical:**
- Test language switching
- Check for console errors
- Verify translation quality
- Test all user flows

---

## Common Patterns

### Basic Text

```tsx
// Before
<h1>Welcome</h1>

// After
<h1>{t("welcome")}</h1>
```

### Interpolation

```tsx
// Before
<p>Hello, {userName}!</p>

// After
<p>{t("greeting", { userName })}</p>

// Translation file
"greeting": "Hello, {{userName}}!"
```

### Attributes

```tsx
// Before
<input placeholder="Enter email" />
<button title="Click to submit">Submit</button>

// After
<input placeholder={t("emailPlaceholder")} />
<button title={t("submitTitle")}>{t("submit")}</button>
```

### Multiple Namespaces

```tsx
const { t: tCommon } = useTranslation("common")
const { t: tSettings } = useTranslation("settings")

<button>{tCommon("save")}</button>
<h1>{tSettings("title")}</h1>
```

See [patterns.md](references/patterns.md) for 20+ more examples.

---

## Troubleshooting

### Issue: Missing Translation Keys

**Symptom:** Console warnings about missing keys

**Solution:**
- Verify key exists in translation file
- Check namespace matches
- Verify key name spelling
- Check JSON syntax

### Issue: Text Not Switching

**Symptom:** Language changed but text didn't update

**Solution:**
- Verify i18n.changeLanguage() is called
- Check component uses useTranslation hook
- Ensure component re-renders on language change
- Verify language code is correct

### Issue: Hardcoded Strings Remaining

**Symptom:** Some text doesn't translate

**Solution:**
- Search for remaining hardcoded strings
- Check if string is user-facing
- Verify component was migrated
- Check for dynamically generated strings

### Issue: Layout Broken with Translations

**Symptom:** UI looks wrong after translation

**Solution:**
- Some languages have longer text (German, Finnish)
- Use flexible layouts
- Test with longer strings
- Consider CSS `word-break` or text truncation

---

## Quality Standards

### Completeness

- [ ] All components processed
- [ ] All strings extracted
- [ ] All strings translated
- [ ] Zero hardcoded strings remain

### Correctness

- [ ] Valid JSON in translation files
- [ ] All keys match between languages
- [ ] No missing translations
- [ ] No TypeScript errors (if applicable)

### Functionality

- [ ] App works in all languages
- [ ] Language switching works
- [ ] No console errors
- [ ] All features work

### Quality

- [ ] Translations are natural and accurate
- [ ] Consistent terminology
- [ ] Appropriate tone
- [ ] Culturally suitable

---

## Quick Reference

### Essential Commands

```bash
# Install dependencies (React)
npm install i18next react-i18next i18next-browser-languagedetector

# Validate JSON
cat src/i18n/locales/en.json | jq .

# Find hardcoded strings
grep -r '">[A-Z]' src/components/
```

### Key File Locations

```
src/i18n/
├── config.ts (or index.ts)
├── types.ts (optional, for TypeScript)
└── locales/
    ├── en.json (base language)
    └── zh.json (target language)

src/main.tsx - Initialize i18n
```

### Hook Usage

```typescript
// Single namespace
const { t } = useTranslation("namespace")

// Multiple namespaces
const { t: tCommon } = useTranslation("common")
const { t: tFeature } = useTranslation("feature")

// With interpolation
t("key", { variable: value })
```

---

## Estimated Effort

For typical applications:

| Component Count | Time Required |
|----------------|---------------|
| Small (< 25 components) | 1-1.5 hours |
| Medium (25-75 components) | 1.5-3 hours |
| Large (75-150 components) | 3-5 hours |
| Very Large (> 150 components) | 5+ hours |

**Time breakdown:**
- Phase 1: 5-10%
- Phase 2: 30-40%
- Phase 3: 10-15%
- Phase 4: 35-45%
- Phase 5: 5-10%

---

## Success Indicators

✅ When i18n is complete:
1. User can switch language and see ENTIRE app translate
2. No base language text remains when target language selected
3. No console errors or warnings
4. All functionality works in all languages
5. Translation quality is high and natural

---

## Getting Help

If stuck:

1. **Review the workflow:** [workflow.md](references/workflow.md)
2. **Check examples:** [patterns.md](references/patterns.md)
3. **Verify organization:** [namespaces.md](references/namespaces.md)
4. **Use checklists:** [checklist.md](references/checklist.md)

---

**Remember:** 100% coverage is the standard. Zero tolerance for hardcoded strings in user-facing UI.
