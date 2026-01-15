# Complete i18n Implementation Workflow

This document provides a systematic, AI-driven workflow for implementing complete internationalization (i18n) for web applications. This workflow is designed to be executed entirely by an AI model without scripts.

## Overview

The workflow consists of 5 phases:

1. **Project Analysis** - Understand the codebase structure and framework
2. **String Extraction** - Systematically extract all user-facing strings
3. **Translation Infrastructure** - Set up i18n system and create translation files
4. **Component Migration** - Update all components to use translations
5. **Validation** - Verify completeness and correctness

**Success Criteria:**
- 100% of user-facing text uses i18n system
- Zero hardcoded strings in UI components
- Translation files are complete and organized
- Application works flawlessly in all supported languages

---

## Phase 1: Project Analysis

### Goal
Understand the project structure, framework, and existing i18n setup.

### Steps

#### 1.1 Identify Framework and Technology

**Check the main entry point and configuration files:**

```
Read: package.json
Read: {framework}.config.js/ts (vite.config, next.config, etc.)
Read: tsconfig.json
```

**Identify:**
- UI framework: React, Vue, Angular, Svelte, etc.
- Build tool: Vite, Webpack, Next.js, etc.
- TypeScript or JavaScript
- Component library (if any)

**Example for React + Vite:**
```json
// package.json
{
  "dependencies": {
    "react": "^18.0.0"
  },
  "devDependencies": {
    "vite": "^5.0.0"
  }
}
```

#### 1.2 Check for Existing i18n

**Search for existing i18n implementations:**

```
Grep: "i18n|i18next|react-i18next|vue-i18n" (case insensitive)
Glob: "**/locales/**"
Glob: "**/i18n/**"
Glob: "**/lang/**"
```

**If i18n exists:**
- Note the library used (i18next, vue-i18n, etc.)
- Check supported languages
- Identify the translation file structure
- Document any existing translations

**If no i18n exists:**
- Plan to install i18next (React) or appropriate library
- Design translation file structure
- Choose base language (usually English)

#### 1.3 Analyze Component Structure

**Map the component hierarchy:**

```
Glob: "src/components/**/*.{tsx,jsx,vue}"
Glob: "src/views/**/*.{tsx,jsx,vue}"
Glob: "src/pages/**/*.{tsx,jsx,vue}"
```

**Categorize components by function:**
- Layout components (Header, Sidebar, Footer)
- Feature components (Chat, Settings, Profile)
- Common components (Button, Input, Modal)
- Utility components (Loading, Error, Empty)

**Create a component inventory:**
```markdown
## Component Inventory

### Layout
- src/components/layout/Header.tsx
- src/components/layout/Sidebar.tsx
- src/components/layout/Footer.tsx

### Features
- src/components/chat/ChatView.tsx
- src/components/settings/SettingsView.tsx
- src/components/profile/ProfileView.tsx

### Common
- src/components/common/Button.tsx
- src/components/common/Input.tsx
- ...
```

### Phase 1 Completion Checklist

- [ ] Framework identified (React/Vue/etc.)
- [ ] Build tool identified
- [ ] Existing i18n checked and documented
- [ ] Component inventory created
- [ ] Translation file structure planned

---

## Phase 2: String Extraction

### Goal
Extract ALL user-facing strings from components systematically.

### Strategy

**Process components in priority order:**
1. High-frequency components (Chat, Settings, Home)
2. Feature-specific components
3. Common/shared components
4. Layout components
5. Utility components

**For each component:**

#### 2.1 Read the Component

```
Read: src/components/{category}/{ComponentName}.{ext}
```

#### 2.2 Extract Strings

**Identify ALL strings that users see:**

✅ **Extract:**
- Text content: `<div>Hello</div>`
- Labels: `<label>Email</label>`
- Placeholders: `<input placeholder="Enter email" />`
- Button text: `<button>Submit</button>`
- Titles/headings: `<h1>Dashboard</h1>`
- Error messages: `<p>Invalid input</p>`
- Success messages: `<p>Saved successfully</p>`
- Tooltips: `title="Click to edit"`
- Aria labels: `aria-label="Close dialog"`
- Alt text: `alt="User avatar"`
- Options in selects/radios

❌ **Don't Extract:**
- Code comments: `// TODO: fix this`
- Debug logs: `console.log("Loading...")`
- Technical identifiers: `id="user-input"`
- CSS class names: `className="error-message"`
- API URLs/endpoints
- Internal state values (not shown to users)

#### 2.3 Create String Entries

For each extracted string, create an entry with:

**Format:**
```json
{
  "componentCategory": {
    "componentName": {
      "stringKey": "The actual English text"
    }
  }
}
```

**Example:**
```json
{
  "chat": {
    "chatView": {
      "title": "Chat",
      "sendMessage": "Send",
      "inputPlaceholder": "Type a message...",
      "emptyState": "No messages yet. Start the conversation!"
    }
  }
}
```

#### 2.4 Handle Complex Patterns

**Interpolation:**
```tsx
// Before
<p>Welcome, {userName}!</p>

// After (in translation file)
"welcome": "Welcome, {{userName}}!"
```

**Plurals:**
```tsx
// Before
<p>{count === 1 ? "1 message" : `${count} messages`}</p>

// After
"message_one": "{{count}} message",
"message_other": "{{count}} messages"
```

**Conditionals:**
```tsx
// Before
<p>{status === 'loading' ? 'Loading...' : 'Done'}</p>

// After (separate keys)
"loading": "Loading...",
"done": "Done"
```

**Formatting:**
```tsx
// Before
<p>Signed in as {email}</p>

// After
"signedInAs": "Signed in as {{email}}"
```

#### 2.5 Document Context

For ambiguous strings, add comments:

```json
{
  "button": {
    "submit": "Submit", // For forms
    "send": "Send", // For messages
    "post": "Post" // For social media
  }
}
```

### Phase 2 Execution Pattern

**Process one component at a time:**

1. Read component file
2. Extract ALL visible strings
3. Categorize by component and meaning
4. Add to master translation list
5. Mark component as "extracted"

**Example extraction session:**

```bash
# Read ChatView component
Read: src/components/chat/ChatView.tsx

# Extract strings found:
# - "New Conversation" button
# - "Type a message..." placeholder
# - "Send" button
# - "Thinking..." loading state
# - "Error sending message" error
# - "Attachment" button
# - "Voice message" button

# Add to translations:
{
  "chat": {
    "chatView": {
      "newConversation": "New Conversation",
      "inputPlaceholder": "Type a message...",
      "sendButton": "Send",
      "thinking": "Thinking...",
      "sendError": "Error sending message",
      "attachment": "Attachment",
      "voiceMessage": "Voice message"
    }
  }
}
```

### Phase 2 Completion Checklist

- [ ] All components read
- [ ] All user-facing strings extracted (100% coverage)
- [ ] Strings organized by component and category
- [ ] Complex patterns (interpolation, plurals) handled
- [ ] Master translation list complete
- [ ] Zero hardcoded strings remain in UI

---

## Phase 3: Translation Infrastructure

### Goal
Set up i18n system and create complete translation files.

### 3.1 Install i18n Library

**For React:**
```bash
npm install i18next react-i18next i18next-browser-languagedetector
```

**For Vue:**
```bash
npm install vue-i18n
```

**For Next.js:**
```bash
npm install next-i18next
```

### 3.2 Create i18n Configuration

**Example for React (src/i18n/config.ts):**
```typescript
import i18n from "i18next"
import { initReactI18next } from "react-i18next"
import LanguageDetector from "i18next-browser-languagedetector"

import enTranslations from "./locales/en.json"
import zhTranslations from "./locales/zh.json"

const resources = {
  en: { translation: enTranslations },
  zh: { translation: zhTranslations },
}

i18n
  .use(LanguageDetector)
  .use(initReactI18next)
  .init({
    resources,
    fallbackLng: "en",
    lng: "en",
    interpolation: { escapeValue: false },
    detection: {
      order: ["localStorage", "navigator"],
      lookupLocalStorage: "app-language",
      caches: ["localStorage"],
    },
  })

export default i18n
```

### 3.3 Create Translation Files

**File structure:**
```
src/i18n/
├── config.ts
└── locales/
    ├── en.json (base language - copy extracted strings here)
    └── zh.json (target language - translate all strings)
```

**Create base language file (en.json):**
- Copy ALL extracted strings from Phase 2
- Organize by namespace (component categories)
- Ensure consistent naming
- Verify no missing strings

**Example structure:**
```json
{
  "common": {
    "loading": "Loading...",
    "error": "Error",
    "success": "Success",
    "cancel": "Cancel",
    "confirm": "Confirm",
    "save": "Save",
    "delete": "Delete"
  },
  "chat": {
    "chatView": {
      "title": "Chat",
      "newConversation": "New Conversation",
      "inputPlaceholder": "Type a message...",
      "sendButton": "Send",
      "thinking": "Thinking...",
      "sendError": "Error sending message"
    }
  },
  "settings": {
    "settingsView": {
      "title": "Settings",
      "saved": "Settings saved successfully"
    }
  }
}
```

### 3.4 Create Target Language File

**For Chinese (zh.json):**
- Copy entire en.json structure
- Translate ALL values (keep keys identical)
- Maintain same nesting and organization
- Ensure cultural appropriateness

**Example:**
```json
{
  "common": {
    "loading": "加载中...",
    "error": "错误",
    "success": "成功",
    "cancel": "取消",
    "confirm": "确认",
    "save": "保存",
    "delete": "删除"
  },
  "chat": {
    "chatView": {
      "title": "聊天",
      "newConversation": "新建对话",
      "inputPlaceholder": "输入消息...",
      "sendButton": "发送",
      "thinking": "思考中...",
      "sendError": "发送消息时出错"
    }
  }
}
```

**Translation quality guidelines:**
- Use natural, native phrasing
- Maintain consistency (same term = same translation)
- Consider context (UI space, tone)
- Test for length (Chinese is often shorter)
- Avoid literal translations

### 3.5 Add Type Definitions (TypeScript)

**Create src/i18n/types.ts:**
```typescript
export interface TranslationResources {
  common: {
    loading: string
    error: string
    success: string
    // ... all common strings
  }
  chat: {
    chatView: {
      title: string
      newConversation: string
      // ... all chat strings
    }
  }
  // ... all namespaces
}
```

This enables autocomplete and type safety.

### Phase 3 Completion Checklist

- [ ] i18n library installed
- [ ] Configuration file created
- [ ] Base language file (en.json) complete with all strings
- [ ] Target language file (zh.json) complete with all translations
- [ ] Type definitions created (if TypeScript)
- [ ] i18n initialized in main entry point
- [ ] Translation files validated (valid JSON, matching structure)

---

## Phase 4: Component Migration

### Goal
Update ALL components to use the i18n system instead of hardcoded strings.

### 4.1 Update Main Entry Point

**Initialize i18n in main.tsx / App.tsx:**
```typescript
import "./i18n/config" // Must be imported first
```

### 4.2 Migration Pattern for Each Component

**For every component:**

#### Step 1: Add useTranslation Hook

```typescript
import { useTranslation } from "react-i18next"

export const MyComponent: React.FC = () => {
  const { t } = useTranslation("namespace") // Use appropriate namespace
  // ...
}
```

#### Step 2: Replace Strings with t() Calls

**Before:**
```tsx
<div className="header">
  <h1>Dashboard</h1>
  <p>Welcome back, User!</p>
  <button>Save</button>
</div>
```

**After:**
```tsx
<div className="header">
  <h1>{t("dashboard.title")}</h1>
  <p>{t("dashboard.welcomeBack", { name: "User" })}</p>
  <button>{t("common.save")}</button>
</div>
```

#### Step 3: Handle All String Types

**Text content:**
```tsx
// Before
<span>Loading data...</span>

// After
<span>{t("common.loadingData")}</span>
```

**Attributes:**
```tsx
// Before
<input placeholder="Enter your email" />
<button title="Click to submit">Submit</button>
<img alt="User profile picture" />

// After
<input placeholder={t("form.emailPlaceholder")} />
<button title={t("form.submitTitle")}>{t("form.submit")}</button>
<img alt={t("profile.userAvatar")} />
```

**Interpolation:**
```tsx
// Before
<p>Hello, {userName}!</p>

// After
<p>{t("greeting.hello", { userName })}</p>
```

**Conditionals:**
```tsx
// Before
<p>{isLoading ? "Loading..." : "Complete"}</p>

// After
<p>{t(isLoading ? "common.loading" : "common.complete")}</p>
```

**Lists/arrays:**
```tsx
// Before
const items = ["Option 1", "Option 2", "Option 3"]

// After
const items = [
  t("options.option1"),
  t("options.option2"),
  t("options.option3"),
]
```

#### Step 4: Handle Multiple Namespaces

If a component uses strings from multiple namespaces:

```typescript
const { t: tCommon } = useTranslation("common")
const { t: tSettings } = useTranslation("settings")

return (
  <div>
    <button>{tCommon("save")}</button>
    <h1>{tSettings("title")}</h1>
  </div>
)
```

### 4.3 Component-by-Component Execution

**Process in order:**

1. **High-priority components first:**
   - Main views (Chat, Settings, Home)
   - Navigation components
   - Critical user flows

2. **Then medium-priority:**
   - Feature-specific components
   - Forms and modals

3. **Finally low-priority:**
   - Utility components
   - Error boundaries
   - Loading states

**For each component:**
```
1. Read the component file
2. Identify all hardcoded strings
3. Add useTranslation hook with appropriate namespace
4. Replace each string with t() call
5. Verify the translation key exists
6. Test the component (if possible)
7. Mark as "migrated"
```

**Example migration:**

**Before (src/components/chat/ChatView.tsx):**
```tsx
export const ChatView = () => {
  return (
    <div className="chat">
      <h1>Chat</h1>
      <input placeholder="Type a message..." />
      <button>Send</button>
      {isLoading && <p>Sending...</p>}
      {error && <p>Error sending message</p>}
    </div>
  )
}
```

**After:**
```tsx
import { useTranslation } from "react-i18next"

export const ChatView = () => {
  const { t } = useTranslation("chat")

  return (
    <div className="chat">
      <h1>{t("chatView.title")}</h1>
      <input placeholder={t("chatView.inputPlaceholder")} />
      <button>{t("chatView.sendButton")}</button>
      {isLoading && <p>{t("chatView.sending")}</p>}
      {error && <p>{t("chatView.sendError")}</p>}
    </div>
  )
}
```

### 4.4 Handle Special Cases

**Dynamic strings (computed values):**
```tsx
// If string contains dynamic parts, use interpolation
<p>Page {currentPage} of {totalPages}</p>
// →
<p>{t("pagination.pageInfo", { current: currentPage, total: totalPages })}</p>
```

**Third-party library strings:**
```tsx
// Some libraries have their own i18n
// Configure library separately, don't mix with app i18n
```

**Date/number formatting:**
```tsx
// Use i18n formatters, not translation strings
import { useFormatDate, useFormatNumber } from './i18n/formatters'
```

**SVG text:**
```tsx
// SVG text elements also need translation
<text x="10" y="20">{t("chart.title")}</text>
```

### Phase 4 Completion Checklist

- [ ] Main entry point imports i18n config
- [ ] ALL components migrated (100% coverage)
- [ ] Zero hardcoded strings remain
- [ ] All translation keys exist in translation files
- [ ] Namespaces used correctly
- [ ] Interpolation handled properly
- [ ] No broken references or missing keys

---

## Phase 5: Validation

### Goal
Verify complete and correct i18n implementation.

### 5.1 String Coverage Validation

**Verify no hardcoded strings remain:**

```
Grep: all components for hardcoded text patterns

Patterns to search:
- ">\s*[A-Z][a-z]+\s*<" (capitalized words in JSX)
- placeholder="[^"]*[A-Za-z]{3,}[^"]*" (placeholders with text)
- title="[^"]*[A-Za-z]{3,}[^"]*" (titles with text)
- aria-label="[^"]*[A-Za-z]{3,}[^"]*" (aria-labels with text)
- alt="[^"]*[A-Za-z]{3,}[^"]*" (alt text with text)

All matches should be:
- Technical terms (API, ID, URL, etc.)
- Brand names that don't translate
- Already using t() function
```

**Expected result:** Zero user-facing hardcoded strings

### 5.2 Translation File Validation

**Check translation files:**

1. **Valid JSON:**
   ```bash
   # Parse each JSON file
   cat src/i18n/locales/en.json | jq .
   cat src/i18n/locales/zh.json | jq .
   ```

2. **Matching keys:**
   - All keys in en.json exist in zh.json
   - All keys in zh.json exist in en.json
   - Structure is identical

3. **No missing translations:**
   - Every value in zh.json is translated (not English)
   - No empty strings
   - No "TODO" placeholders

4. **Completeness check:**
   ```
   Extract all translation keys from en.json
   Extract all translation keys from zh.json
   Compare: should be identical
   ```

### 5.3 Component Validation

**Test component behavior:**

1. **Load app in English (default)**
   - All text displays correctly
   - No missing translation warnings in console
   - UI looks correct

2. **Switch language to Chinese**
   - All text switches to Chinese
   - No remaining English text
   - Layout still looks good (text length changes)

3. **Check console:**
   - No warnings about missing keys
   - No i18n errors

### 5.4 Type Safety Validation (TypeScript)

**If using TypeScript:**

```bash
# Run type checker
npm run type-check
# or
npx tsc --noEmit
```

**Should have:**
- No type errors
- All t() calls use valid keys
- Autocomplete works for translation keys

### 5.5 Manual Spot Check

**Randomly sample 10-20 components:**

```
For each sampled component:
1. Read the component file
2. Verify ALL user-facing strings use t()
3. Verify translation keys exist
4. Check for proper namespace usage
5. Verify interpolation (if any)
```

### 5.6 Translation Quality Check

**Review Chinese translations:**

- Natural, native phrasing
- Consistent terminology
- Appropriate tone
- Culturally suitable
- No translation errors

**Common issues to check:**
- Machine translation artifacts
- Inconsistent terminology
- Too literal translations
- Wrong context

### Phase 5 Completion Checklist

- [ ] Zero hardcoded strings found (Grep search)
- [ ] All translation files valid JSON
- [ ] All keys match between languages
- [ ] No missing translations
- [ ] No console warnings/errors
- [ ] Type checking passes (if TypeScript)
- [ ] Manual spot check passes
- [ ] Translation quality verified

---

## Execution Guidelines for AI

### How to Use This Workflow

**When implementing i18n for a project:**

1. **Start with Phase 1** - Analyze the project thoroughly
2. **Complete each phase fully** before moving to next
3. **Be systematic** - Process every component, don't skip
4. **Verify completion** - Use checklists at each phase
5. **Iterate if needed** - If issues found, fix and re-validate

### Quality Standards

**100% Coverage:**
- Every user-facing string must be extracted
- Every component must be migrated
- Zero hardcoded strings in UI

**Completeness:**
- All translation files complete
- No missing keys
- No TODO placeholders

**Correctness:**
- Valid JSON
- Valid TypeScript (if applicable)
- No broken references
- Proper namespace usage

### Time Estimation

For a typical medium-sized app (50-100 components):

- Phase 1: 5-10 minutes
- Phase 2: 30-60 minutes (largest phase)
- Phase 3: 15-20 minutes
- Phase 4: 40-80 minutes (largest phase)
- Phase 5: 10-15 minutes

**Total: ~1.5-3 hours** for complete i18n implementation

### Common Pitfalls

❌ **Don't skip components** - Must migrate ALL components
❌ **Don't leave strings** - Even "small" strings matter
❌ **Don't mix languages** - Consistent language per file
❌ **Don't forget attributes** - Placeholders, titles, alts
❌ **Don't guess namespaces** - Use consistent organization
❌ **Don't rush validation** - Thorough checking is critical

### Success Indicators

✅ When i18n is complete:
- User can switch language and see ENTIRE app translate
- No English remains when Chinese is selected
- No console errors or warnings
- All functionality works in both languages
- Translation quality is high

---

## Quick Reference

### Essential Commands

```bash
# Install dependencies (React)
npm install i18next react-i18next i18next-browser-languagedetector

# Validate JSON
cat src/i18n/locales/en.json | jq .

# Find hardcoded strings (example)
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

src/main.tsx (or App.tsx) - Initialize i18n
```

### Common Patterns

```typescript
// Hook usage
const { t } = useTranslation("namespace")

// Simple translation
t("key")

// With interpolation
t("key", { variable: value })

// Multiple namespaces
const { t: tCommon } = useTranslation("common")
const { t: tFeature } = useTranslation("feature")
```

---

**End of Workflow**
