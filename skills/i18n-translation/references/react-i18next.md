# React i18next Translation Strategy

React i18next is the most popular internationalization framework for React applications. This guide provides specific strategies for translating React apps effectively.

## ⚠️ CRITICAL RULES

### AUTO-DEBUGGING CAPABILITY DETECTION (CRITICAL)

**Before any installation or code modification, AI checks:**

**Detection Checklist:**
```bash
# 1. Check for test framework
grep -E "(jest|vitest|cypress|playwright)" package.json

# 2. Check for dev/test scripts
grep -E '"(dev|start|test)"' package.json

# 3. Check for build configuration
ls -la vite.config.* webpack.config.* tsconfig.json 2>/dev/null

# 4. Verify node_modules exists
[ -d "node_modules" ] && echo "OK" || echo "MISSING"
```

**Decision Matrix:**
```
Can Auto-Debug?
├── ✅ Has test framework + Has dev scripts + Has build config + Has node_modules
│     → FULLY AUTOMATED MODE
│     → Install react-i18next ✅
│     → Modify all components ✅
│     → Auto-verify with tests ✅
│
└── ⚠️ Missing any of the above
      → FILES-ONLY MODE
      → Create translation files ✅
      → Generate migration guide ✅
      → NO installation ❌
      → NO component modification ❌
```

### FULLY AUTOMATED MODE (When debugging possible)

**Detection Result:** React project can be auto-tested/debugged

**AI performs ALL tasks automatically:**
- ✅ Install i18next, react-i18next, i18next-browser-languagedetector
- ✅ Extract all hardcoded strings from .jsx/.tsx files
- ✅ Generate translation files (JSON) with namespace structure
- ✅ Modify ALL React components to use useTranslation hook
- ✅ Wrap app with I18nextProvider
- ✅ Add language switcher component
- ✅ Auto-verify integration

**No manual intervention required.**

### FILES-ONLY MODE (When debugging NOT possible)

**Detection Result:** React project cannot be auto-tested/debugged

**AI performs ONLY these tasks:**
- ✅ Create translation files (public/locales/)
- ✅ Create i18n config template
- ✅ Generate comprehensive React migration guide
- ✅ Provide before/after component examples

**AI does NOT perform:**
- ❌ NO npm installation
- ❌ NO component file modifications
- ❌ NO app configuration changes

**User must manually:**
1. npm install i18next react-i18next i18next-browser-languagedetector
2. Copy i18n config to src/i18n.js
3. Import in app: import './i18n';
4. Update components using migration guide

### Complete Coverage Requirement

**Every user-facing string must be extracted:**
- Scan: .jsx, .tsx files
- Extract: JSX text content, button/label text, toasts, alerts, validation messages
- Document: Count strings found and categorize by feature/namespace

## Identifying React i18next Projects

**Package.json indicators:**
```json
{
  "dependencies": {
    "react-i18next": "^23.0.0",
    "i18next": "^23.0.0"
  }
}
```

**Common file locations:**
```
public/locales/{language}/{namespace}.json
src/i18n/locales/{language}/{namespace}.json
src/locales/{language}/{namespace}.json
```

## Comprehensive String Extraction for React

### Step 1: Scan All React Files

```bash
# Find all React component files
find src -type f \( -name "*.jsx" -o -name "*.tsx" \)

# Count total files
echo "Total React files: $(find src -type f \( -name "*.jsx" -o -name "*.tsx" \) | wc -l)"
```

### Step 2: Extract JSX Strings

```bash
# Extract JSX text content (between tags)
grep -rh ">[^<{]*<" src/ --include="*.jsx" --include="*.tsx" | grep -v "^[[:space:]]*$" | sort -u | head -100

# Extract button text
grep -rh "<button[^>]*>[^<]*</button>" src/ --include="*.jsx" --include="*.tsx" | sed 's/<[^>]*>//g' | sort -u

# Extract label text
grep -rh "<label[^>]*>[^<]*</label>" src/ --include="*.jsx" --include="*.tsx" | sed 's/<[^>]*>//g' | sort -u

# Extract input placeholders
grep -rh 'placeholder="[^"]*"' src/ --include="*.jsx" --include="*.tsx" | sort -u

# Find toast/notification messages
grep -rh "message=['\"]" src/ --include="*.jsx" --include="*.tsx"
grep -rh "title=['\"]" src/ --include="*.jsx" --include="*.tsx" | grep -E "(toast|notification|alert)"

# Find strings in conditional rendering
grep -rh "{.*['\"]\w\+\(\s\+\w\+\)*['\"].*}" src/ --include="*.jsx" --include="*.tsx" | grep -E "(button|label|title|text)"
```

### Step 3: Organize by Namespace

Group extracted strings into namespaces:

1. **common.json** - Shared UI (buttons, labels, status)
2. **auth.json** - Authentication (login, signup, password)
3. **dashboard.json** - Dashboard features
4. **settings.json** - Settings pages
5. **validation.json** - Form validation messages
6. **notifications.json** - Toasts, alerts, confirmations

### Step 4: Create Namespace Files

Create translation files for each namespace.

### Step 5: Automatic Component Integration

**AI automatically modifies ALL React components:**
- Import `useTranslation` hook in components with hardcoded strings
- Replace hardcoded text with `t('namespace:key')` calls
- Preserve all interpolation variables and component props
- Handle toast/alert messages with translation functions
- Ensure proper namespace usage

**No migration guide needed** - AI performs all component modifications directly.

## File Structure

### Standard Structure
```
public/locales/
├── en/
│   ├── translation.json    # Default namespace
│   ├── common.json
│   └── auth.json
├── es/
│   ├── translation.json
│   ├── common.json
│   └── auth.json
└── zh-Hans/
    ├── translation.json
    ├── common.json
    └── auth.json
```

### Recommended Split for React Apps

By feature (React apps are typically component-based):

```
public/locales/
├── en/
│   ├── common.json           # Shared UI elements
│   ├── auth.json             # Login, signup, password reset
│   ├── dashboard.json        # Dashboard components
│   ├── settings.json         # Settings pages
│   ├── profile.json          # User profile
│   └── notifications.json    # Toast/alert messages
└── zh-Hans/
    ├── (matching structure)
```

## React i18next Specific Features

### 1. Interpolation

React i18next uses double curly braces for interpolation:

```json
// English
{
  "greeting": "Hello {{name}}",
  "message": "You have {{count}} new messages",
  "linkText": "Click {{link}} for more info"
}

// Chinese (preserve {{ }})
{
  "greeting": "你好 {{name}}",
  "message": "您有 {{count}} 条新消息",
  "linkText": "点击 {{link}} 查看更多信息"
}
```

### 2. Pluralization

```json
// English (has plural forms)
{
  "item": "one item",
  "item_plural": "{{count}} items",
  "message_zero": "No messages",
  "message_one": "One message",
  "message_other": "{{count}} messages"
}

// Chinese (no plural forms - use same translation)
{
  "item": "{{count}} 个项目",
  "item_plural": "{{count}} 个项目",
  "message_zero": "没有消息",
  "message_one": "一条消息",
  "message_other": "{{count}} 条消息"
}
```

**Note**: Even for languages without plurals, maintain the same key structure to match the source file.

### 3. Formatting

```json
{
  "price": "Price: {{value, currency}}",
  "date": "Date: {{value, date}}",
  "time": "Time: {{value, time}}",
  "number": "Count: {{value, number}}"
}
```

Keep the formatting syntax intact. React i18next handles the actual formatting based on locale.

### 4. Nesting

```json
// English
{
  "nav": {
    "home": "Home",
    "about": "About",
    "contact": "Contact"
  },
  "user": {
    "profile": "Profile",
    "settings": "Settings",
    "logout": "Logout"
  }
}

// Chinese (maintain nesting structure)
{
  "nav": {
    "home": "首页",
    "about": "关于",
    "contact": "联系我们"
  },
  "user": {
    "profile": "个人资料",
    "settings": "设置",
    "logout": "登出"
  }
}
```

### 5. Arrays

```json
// English
{
  "items": [
    "First item",
    "Second item",
    "Third item"
  ]
}

// Chinese
{
  "items": [
    "第一项",
    "第二项",
    "第三项"
  ]
}
```

## Code Integration Patterns

### Using the `t` function

```javascript
import { useTranslation } from 'react-i18next';

function MyComponent() {
  const { t } = useTranslation();

  return (
    <div>
      <h1>{t('welcome')}</h1>
      <p>{t('greeting', { name: 'John' })}</p>
    </div>
  );
}
```

### Using namespaces

```javascript
// Default namespace (translation.json)
const { t } = useTranslation();

// Specific namespace
const { t } = useTranslation('auth');

// Multiple namespaces
const { t } = useTranslation(['common', 'dashboard']);
```

### When splitting files, update namespace usage:

```javascript
// Before (single file)
import { useTranslation } from 'react-i18next';
const { t } = useTranslation();
t('dashboard.title');

// After (split by feature)
import { useTranslation } from 'react-i18next';
const { t } = useTranslation('dashboard');
t('title');  // namespace prefix is no longer needed
```

## Common React Component Translations

### Navigation Components
```json
{
  "nav": {
    "home": "Home",
    "dashboard": "Dashboard",
    "settings": "Settings",
    "profile": "Profile",
    "logout": "Logout"
  }
}
```

### Form Components
```json
{
  "form": {
    "required": "This field is required",
    "invalid": "Invalid format",
    "email": "Email address",
    "password": "Password",
    "confirmPassword": "Confirm Password",
    "submit": "Submit",
    "cancel": "Cancel"
  }
}
```

### Button Components
```json
{
  "button": {
    "save": "Save",
    "delete": "Delete",
    "edit": "Edit",
    "cancel": "Cancel",
    "confirm": "Confirm",
    "close": "Close"
  }
}
```

### Status Messages
```json
{
  "status": {
    "loading": "Loading...",
    "success": "Success",
    "error": "Error",
    "warning": "Warning"
  }
}
```

## React Router Integration

```javascript
// Translate route titles
const routes = [
  {
    path: '/dashboard',
    title: 'dashboard:title',  // Use t('dashboard:title')
    component: Dashboard
  }
];
```

## Translation Workflow for React Apps

### Step 1: Identify all components
```bash
# Find all component files
find src -name "*.jsx" -o -name "*.tsx"
```

### Step 2: Extract translation keys
Look for `t('key')` patterns in components:
```bash
grep -rh "t('" src/ | sort -u
```

### Step 3: Organize by component/feature
```
common.json       → Shared keys across multiple components
auth.json         → Auth components (LoginForm, SignupForm, etc.)
dashboard.json    → Dashboard components
settings.json     → Settings components
```

### Step 4: Translate systematically
For each namespace file:
1. Read entire source file
2. Count total keys
3. Translate each key maintaining structure
4. Validate JSON syntax
5. Report completion

### Step 5: Update component imports (if splitting)
```javascript
// Before
import { useTranslation } from 'react-i18next';
const { t } = useTranslation();

// After (with namespace)
import { useTranslation } from 'react-i18next';
const { t } = useTranslation('auth');
```

## Testing in React

### Manual Testing
```javascript
// Test with different languages
i18next.changeLanguage('en');
i18next.changeLanguage('zh-Hans');
i18next.changeLanguage('es');
```

### Check for missing translations
```javascript
// Enable missing key handler
i18next.init({
  saveMissing: true,
  missingKeyHandler: (lng, ns, key) => {
    console.warn(`Missing translation: ${lng}.${ns}.${key}`);
  }
});
```

## Common React i18next Pitfalls

### 1. Missing namespace prefix
```javascript
// Wrong (when using namespaces)
t('welcome')

// Correct
t('common:welcome')
// OR
const { t } = useTranslation('common');
t('welcome')
```

### 2. Breaking interpolation
```json
// Wrong - removed placeholders
{
  "greeting": "你好"
}

// Correct - preserved placeholders
{
  "greeting": "你好 {{name}}"
}
```

### 3. Not maintaining key structure
```json
// English source
{
  "user": {
    "name": "Name",
    "email": "Email"
  }
}

// Wrong - flattened structure
{
  "user.name": "姓名",
  "user.email": "电子邮箱"
}

// Correct - maintain nesting
{
  "user": {
    "name": "姓名",
    "email": "电子邮箱"
  }
}
```

## Quick Commands

```bash
# Validate all JSON files
for file in public/locales/*/*.json; do
  jq . < "$file" > /dev/null && echo "✓ $file" || echo "✗ $file"
done

# Count keys in each file
for file in public/locales/en/*.json; do
  echo "$file: $(jq 'keys | length' "$file") keys"
done

# Compare key counts between languages
echo "English: $(jq 'keys | length' public/locales/en/translation.json)"
echo "Chinese: $(jq 'keys | length' public/locales/zh-Hans/translation.json)"
```

## Configuration Example

```javascript
// i18n.js
import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';
import Backend from 'i18next-http-backend';
import LanguageDetector from 'i18next-browser-languagedetector';

i18n
  .use(Backend)
  .use(LanguageDetector)
  .use(initReactI18next)
  .init({
    fallbackLng: 'en',
    debug: false,

    ns: ['common', 'auth', 'dashboard', 'settings'],
    defaultNS: 'common',

    backend: {
      loadPath: '/locales/{{lng}}/{{ns}}.json',
    },

    interpolation: {
      escapeValue: false,
    },
  });

export default i18n;
```

## Summary

**Key Points for React i18next:**
1. Preserve all `{{variable}}` placeholders
2. Maintain nesting structure
3. Use namespaces to organize translations
4. Keep plural keys even for languages without plurals
5. Validate JSON syntax after each file
6. Test with `i18next.changeLanguage()`

**Remember**: After splitting files, update namespace usage in React components!
