# I18N Translation - Examples

This document provides concrete examples of common internationalization scenarios.

## Table of Contents

1. [Example 0: Complete Project Internationalization (NEW)](#example-0-complete-project-internationalization-new)
2. [Example 1: New Project Setup](#example-1-new-project-setup)
3. [Example 2: Completing Partial Translations](#example-2-completing-partial-translations)
4. [Example 3: Splitting Large Files](#example-3-splitting-large-files)
5. [Example 4: React i18next Project](#example-4-react-i18next-project)
6. [Example 5: Vue I18n Project](#example-5-vue-i18n-project)

---

## Example 0: Complete Project Internationalization (NEW)

**Scenario**: User has a React app without any i18n and wants to add complete multi-language support for English and Chinese.

### User Request
> "My React app currently only has hardcoded strings. I want to add Chinese (Simplified) support with complete coverage."

### Phase 1: String Extraction & Translation File Creation

#### Step 1: Scan All Source Files

```bash
# Find all React component files
find src -type f \( -name "*.jsx" -o -name "*.tsx" \)
# Found: 47 files

# Find all template files
find . -type f -name "*.html"
# Found: 2 files

echo "Total files to scan: 49"
```

#### Step 2: Extract All User-Facing Strings

```bash
# Extract JSX text content
grep -rh ">[^<{]*<" src/ | grep -v "^[[:space:]]*$" | sort -u | head -50

# Results (first 50 strings):
- "Save"
- "Cancel"
- "Delete"
- "Edit"
- "Loading..."
- "Error"
- "Success"
- "Log In"
- "Sign Up"
- "Email"
- "Password"
- "Forgot Password?"
- "Dashboard"
- "Settings"
- "Profile"
- "Logout"
- ... (35 more strings)

# Extract button text
grep -rh "<button[^>]*>[^<]*</button>" src/ --include="*.jsx" | sed 's/<[^>]*>//g' | sort -u
# Found: 15 unique button texts

# Extract validation messages
grep -rh "message=['\"]" src/ | grep -E "(required|invalid|error)" | sort -u
# Found: 8 validation messages

# Extract placeholders
grep -rh 'placeholder="[^"]*"' src/ --include="*.jsx" | sort -u
# Found: 12 placeholders
```

#### Step 3: Categorize and Organize Strings

**Extracted strings summary:**
- Total unique strings: 156
- Common UI (buttons, labels): 45
- Authentication (login, signup): 28
- Dashboard: 35
- Settings: 22
- Validation: 15
- Errors: 11

**Organization:**
```
1. common.json (45 keys) - buttons, labels, status, navigation
2. auth.json (28 keys) - login, signup, password reset
3. dashboard.json (35 keys) - dashboard components
4. settings.json (22 keys) - settings pages
5. validation.json (15 keys) - form validation
6. errors.json (11 keys) - error messages
```

#### Step 4: Create Translation Files

**Source file: `public/locales/en/common.json`**
```json
{
  "save": "Save",
  "cancel": "Cancel",
  "delete": "Delete",
  "edit": "Edit",
  "submit": "Submit",
  "close": "Close",
  "loading": "Loading...",
  "success": "Success",
  "error": "Error",
  "warning": "Warning",
  "confirm": "Confirm",
  "back": "Back",
  "next": "Next",
  "previous": "Previous"
}
```

**Target file: `public/locales/zh-Hans/common.json`**
```json
{
  "save": "保存",
  "cancel": "取消",
  "delete": "删除",
  "edit": "编辑",
  "submit": "提交",
  "close": "关闭",
  "loading": "加载中...",
  "success": "成功",
  "error": "错误",
  "warning": "警告",
  "confirm": "确认",
  "back": "返回",
  "next": "下一步",
  "previous": "上一步"
}
```

(Repeat for all 6 namespace files: common, auth, dashboard, settings, validation, errors)

#### Step 5: Automatic Component Integration (No Migration Guide Needed)

**AI automatically performs ALL integration tasks:**

**1. Install i18next dependencies:**
```bash
npm install i18next react-i18next i18next-browser-languagedetector
```

**2. Create i18n configuration:**
**File: `src/i18n.js`**
```javascript
import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';
import LanguageDetector from 'i18next-browser-languagedetector';

import enCommon from './locales/en/common.json';
import enAuth from './locales/en/auth.json';
import enDashboard from './locales/en/dashboard.json';
import enSettings from './locales/en/settings.json';
import enValidation from './locales/en/validation.json';
import enErrors from './locales/en/errors.json';

import zhCommon from './locales/zh-Hans/common.json';
import zhAuth from './locales/zh-Hans/auth.json';
import zhDashboard from './locales/zh-Hans/dashboard.json';
import zhSettings from './locales/zh-Hans/settings.json';
import zhValidation from './locales/zh-Hans/validation.json';
import zhErrors from './locales/zh-Hans/errors.json';

const resources = {
  en: {
    common: enCommon,
    auth: enAuth,
    dashboard: enDashboard,
    settings: enSettings,
    validation: enValidation,
    errors: enErrors,
  },
  zhHans: {
    common: zhCommon,
    auth: zhAuth,
    dashboard: zhDashboard,
    settings: zhSettings,
    validation: zhValidation,
    errors: zhErrors,
  },
};

i18n
  .use(LanguageDetector)
  .use(initReactI18next)
  .init({
    resources,
    fallbackLng: 'en',
    interpolation: {
      escapeValue: false,
    },
  });

export default i18n;
```

**3. AI modifies ALL components automatically:**
```jsx
// Before AI modification:
<button>Save</button>

// After AI modification:
import { useTranslation } from 'react-i18next';

function MyComponent() {
  const { t } = useTranslation('common');
  return <button>{t('save')}</button>;
}
```

**4. AI adds LanguageSwitcher component:**
**File: `src/components/LanguageSwitcher.jsx`**
```jsx
import { useTranslation } from 'react-i18next';

function LanguageSwitcher() {
  const { i18n } = useTranslation();

  return (
    <select
      value={i18n.language}
      onChange={(e) => i18n.changeLanguage(e.target.value)}
    >
      <option value="en">English</option>
      <option value="zhHans">中文</option>
    </select>
  );
}

export default LanguageSwitcher;
```

**No migration guide needed** - AI performs all modifications automatically.

### Phase 2: Automatic Integration (AI Implementation)

**AI automatically modifies ALL React components:**

1. Installs i18next dependencies
2. Configures i18next in the app
3. Replaces hardcoded strings in ALL components with useTranslation hooks
4. Adds language switcher component
5. Tests integration and reports results

### Completion Report

```
✓ Detection Complete
  - Framework identified: React
  - i18next installed: Yes

✓ String Extraction Complete
  - Scanned: 49 files (.jsx, .tsx, .html)
  - Extracted: 156 unique strings
  - Organized into: 6 namespace files

✓ Translation Files Created
  - English: 156 keys across 6 files
  - Chinese: 156 keys across 6 files
  - Coverage: 100%

✓ Automatic Integration Complete
  - Modified: 47 component files
  - Added: useTranslation hooks to all components
  - Added: LanguageSwitcher component
  - Added: i18n configuration
  - Tested: Language switching working

✓ Ready to Use
  - All components now use translation keys
  - Language switcher functional
  - No manual intervention required
```

### Key Features of This Example

**This example demonstrates:**
1. **Complete project scan** - Scans ALL files for hardcoded strings
2. **Fully automated workflow** - Detection, installation, extraction, integration
3. **Automatic component modification** - AI modifies ALL React components
4. **No migration guide needed** - AI performs all implementation work
5. **Comprehensive coverage** - 156 strings across 49 files, 100% extraction and integration

---

## Example 1: New Project Setup

**Scenario**: User wants to add Chinese (Simplified) support to an existing React app that only has English.

### User Request
> "My React app currently only supports English. I want to add Chinese (Simplified) support."

### Discovery Phase

**1. Find existing i18n structure:**
```bash
find . -name "*.json" -path "*/locales/*"
# Found: public/locales/en/common.json (156 keys)
```

**2. Identify framework:**
```bash
grep -r "i18next" package.json
# Found: "react-i18next": "^23.0.0"
# Framework: React i18next
```

**3. Assess file size:**
```bash
jq 'keys | length' public/locales/en/common.json
# Result: 156 keys
# Decision: Split recommended (> 200 keys threshold not met, but close)
```

### Implementation

**Option A: Keep Single File (Since < 200 keys)**

```
public/locales/
├── en/
│   └── common.json    # 156 keys
└── zh-Hans/
    └── common.json    # Create this
```

**Translation Process:**

```bash
# 1. Read source file
cat public/locales/en/common.json

# 2. Count keys (156 total)

# 3. Translate systematically (first 10 keys shown)
{
  "welcome": "Welcome",
  "login": "Log In",
  "logout": "Log Out",
  "signup": "Sign Up",
  "dashboard": "Dashboard",
  "settings": "Settings",
  "profile": "Profile",
  "save": "Save",
  "cancel": "Cancel",
  "delete": "Delete"
  // ... 146 more keys
}

→

{
  "welcome": "欢迎",
  "login": "登录",
  "logout": "登出",
  "signup": "注册",
  "dashboard": "仪表板",
  "settings": "设置",
  "profile": "个人资料",
  "save": "保存",
  "cancel": "取消",
  "delete": "删除"
  // ... 146 more keys
}
```

**4. Validation:**
```bash
# Verify key counts match
echo "English: $(jq 'keys | length' public/locales/en/common.json)"
# English: 156

echo "Chinese: $(jq 'keys | length' public/locales/zh-Hans/common.json)"
# Chinese: 156

# Validate JSON syntax
jq . < public/locales/zh-Hans/common.json > /dev/null && echo "✓ Valid"
# ✓ Valid
```

**5. Completion Report:**
```
✓ Completed: common.json (156/156 keys)
✓ All placeholders preserved
✓ JSON syntax validated
✓ Ready for testing
```

---

## Example 2: Completing Partial Translations

**Scenario**: User has a partial German translation (only 60% complete) and wants it finished.

### User Request
> "My German translation is incomplete. The AI stopped halfway through. Can you complete it?"

### Discovery Phase

**1. Assess current state:**
```bash
# English source
jq 'keys | length' public/locales/en/common.json
# Result: 156 keys

# German target (incomplete)
jq 'keys | length' public/locales/de/common.json
# Result: 94 keys
# Completion: 60.3%
# Missing: 62 keys
```

**2. Identify missing keys:**
```bash
# Find keys in English but not in German
jq -r 'keys[]' public/locales/en/common.json > /tmp/en_keys.txt
jq -r 'keys[]' public/locales/de/common.json > /tmp/de_keys.txt
grep -vxFf /tmp/de_keys.txt /tmp/en_keys.txt
# Missing keys: submit, confirmPassword, emailSent, etc.
```

### Implementation

**Systematic Completion Process:**

```json
// Current German file (94 keys)
{
  "welcome": "Willkommen",
  "login": "Anmelden",
  // ... 92 more keys
}

// Add missing keys (62 keys)
{
  "welcome": "Willkommen",
  "login": "Anmelden",
  // ... existing 92 keys ...

  // NEW - Add these 62 missing translations:
  "submit": "Absenden",
  "confirmPassword": "Passwort bestätigen",
  "emailSent": "E-Mail gesendet",
  "loading": "Laden...",
  "success": "Erfolg",
  "error": "Fehler",
  "warning": "Warnung",
  "info": "Information",
  // ... 54 more keys
}
```

**Validation:**
```bash
# Verify completion
jq 'keys | length' public/locales/de/common.json
# Result: 156 keys (100%)

# Verify no missing keys
diff <(jq -r 'keys[]' public/locales/en/common.json | sort) \
     <(jq -r 'keys[]' public/locales/de/common.json | sort)
# Result: No differences
```

**Completion Report:**
```
✓ Completed: common.json (156/156 keys)
✓ Added 62 missing translations
✓ 100% parity with source
✓ JSON syntax validated
```

---

## Example 3: Splitting Large Files

**Scenario**: User has a monolithic translation file with 523 keys that causes AI to lose track and produce incomplete translations.

### User Request
> "My translation file is too large and the AI keeps missing translations. Help me split it."

### Discovery Phase

**1. Assess file size:**
```bash
jq 'keys | length' public/locales/en/common.json
# Result: 523 keys
# Verdict: DEFINITELY needs splitting
```

**2. Analyze key patterns:**
```bash
jq -r 'keys[]' public/locales/en/common.json | head -20
# Pattern detected:
# - auth.*
# - dashboard.*
# - settings.*
# - common.*
# - errors.*
```

### Implementation

**Step 1: Group keys by prefix**

```bash
# Analyze key prefixes
jq -r 'keys[]' public/locales/en/common.json | cut -d'_' -f1 | sort | uniq -c
#   45 common
#   78 auth
#  156 dashboard
#   89 settings
#  155 errors
```

**Step 2: Create split files**

```bash
# Create new structure
mkdir -p public/locales/en public/locales/zh-Hans

# Split into logical files
public/locales/en/
├── common.json      # 45 keys - General UI elements
├── auth.json        # 78 keys - Authentication flows
├── dashboard.json   # 156 keys - Dashboard features
├── settings.json    # 89 keys - Settings pages
└── errors.json      # 155 keys - Error messages
```

**Step 3: Extract content for each file**

```json
// common.json (45 keys)
{
  "appName": "MyApp",
  "welcome": "Welcome",
  "loading": "Loading...",
  "save": "Save",
  "cancel": "Cancel",
  "delete": "Delete",
  "edit": "Edit",
  "close": "Close",
  "back": "Back",
  "next": "Next",
  // ... 35 more common UI elements
}

// auth.json (78 keys)
{
  "login": "Log In",
  "logout": "Log Out",
  "signup": "Sign Up",
  "email": "Email",
  "password": "Password",
  "forgotPassword": "Forgot Password?",
  "resetPassword": "Reset Password",
  "loginSuccess": "Successfully logged in",
  "loginFailed": "Login failed",
  // ... 69 more auth-related keys
}

// dashboard.json (156 keys)
{
  "dashboardTitle": "Dashboard",
  "overview": "Overview",
  "statistics": "Statistics",
  "recentActivity": "Recent Activity",
  "quickActions": "Quick Actions",
  // ... 151 more dashboard keys
}

// settings.json (89 keys)
{
  "settings": "Settings",
  "profile": "Profile",
  "account": "Account",
  "notifications": "Notifications",
  "privacy": "Privacy",
  // ... 84 more settings keys
}

// errors.json (155 keys)
{
  "error": "Error",
  "warning": "Warning",
  "networkError": "Network error",
  "serverError": "Server error",
  "notFound": "Not found",
  // ... 150 more error keys
}
```

**Step 4: Create matching structure for target language**

```bash
# Create Chinese files (empty structure first)
touch public/locales/zh-Hans/{common,auth,dashboard,settings,errors}.json

# Translate each file systematically
```

**Step 5: Update i18n configuration**

```javascript
// Before: Single namespace
i18n.init({
  ns: ['common'],
  defaultNS: 'common'
});

// After: Multiple namespaces
i18n.init({
  ns: ['common', 'auth', 'dashboard', 'settings', 'errors'],
  defaultNS: 'common'
});
```

**Step 6: Update code references**

```javascript
// Before
import { t } from 'i18next';
t('dashboardTitle');

// After - specify namespace
import { t } from 'i18next';
t('dashboard:dashboardTitle');
// Or use useTranslation hook
const { t } = useTranslation('dashboard');
t('dashboardTitle');
```

### Translation After Split

Now translate each file independently:

```
✓ Completed: common.json (45/45 keys)
✓ Completed: auth.json (78/78 keys)
✓ Completed: dashboard.json (156/156 keys)
✓ Completed: settings.json (89/89 keys)
✓ Completed: errors.json (155/155 keys)

Total: 523/523 keys (100%)
```

**Benefits of Splitting:**
- ✅ Each file is manageable size
- ✅ AI can maintain context throughout each file
- ✅ Easier to identify missing translations
- ✅ Faster to load and process
- ✅ Better organization by feature

---

## Example 4: React i18next Project

**Scenario**: React app using react-i18next with complex interpolation and pluralization.

### Source File

```json
// public/locales/en/common.json
{
  "greeting": "Hello, {{name}}!",
  "unreadMessages": "You have {{count}} unread message",
  "unreadMessages_plural": "You have {{count}} unread messages",
  "lastLogin": "Last login: {{date, date}}",
  "userInfo": "User: {{name}} ({{email}})",
  "deleteConfirm": "Are you sure you want to delete '{{item}}'?",
  "progress": "{{completed}}/{{total}} tasks completed ({{percent}}%)"
}
```

### Target File (Chinese)

```json
// public/locales/zh-Hans/common.json
{
  "greeting": "你好，{{name}}！",
  "unreadMessages": "您有 {{count}} 条未读消息",
  "unreadMessages_plural": "您有 {{count}} 条未读消息",
  "lastLogin": "上次登录：{{date, date}}",
  "userInfo": "用户：{{name}}（{{email}}）",
  "deleteConfirm": "确定要删除 '{{item}}' 吗？",
  "progress": "已完成 {{completed}}/{{total}} 项任务（{{percent}}%）"
}
```

### Key Considerations

**1. Placeholders preserved:**
- `{{name}}` → `{{name}}` ✅
- `{{count}}` → `{{count}}` ✅
- `{{date, date}}` → `{{date, date}}` ✅

**2. Plurals:**
- Chinese doesn't have plural forms like English
- Use the same translation for both singular and plural
- Keep both keys to maintain structure parity

**3. Date/number formatting:**
- Keep formatting syntax: `{{date, date}}`
- i18next handles locale-specific formatting

**4. Cultural adjustments:**
- Changed "you" to "您" (formal you)
- Adjusted punctuation for Chinese conventions
- Changed parentheses to full-width （）for better readability

---

## Example 5: Vue I18n Project

**Scenario**: Vue 3 app using vue-i18n with YAML format.

### Source File

```yaml
# src/locales/en.yaml
app:
  name: "My Application"
  version: "Version {{version}}"

nav:
  home: "Home"
  about: "About"
  contact: "Contact"

forms:
  email: "Email address"
  password: "Password"
  submit: "Submit"
  required: "This field is required"
  invalid: "Invalid format"

messages:
  welcome: "Welcome back, {name}!"
  success: "Operation successful"
  error: "An error occurred"
```

### Target File (Chinese)

```yaml
# src/locales/zh-Hans.yaml
app:
  name: "我的应用"
  version: "版本 {{version}}"

nav:
  home: "首页"
  about: "关于"
  contact: "联系我们"

forms:
  email: "电子邮件地址"
  password: "密码"
  submit: "提交"
  required: "此字段为必填项"
  invalid: "格式无效"

messages:
  welcome: "欢迎回来，{name}！"
  success: "操作成功"
  error: "发生错误"
```

### Validation

```bash
# Validate YAML syntax
ruby -e "require 'yaml'; YAML.load_file('src/locales/zh-Hans.yaml')"
# Or using Python
python -c "import yaml; yaml.safe_load(open('src/locales/zh-Hans.yaml'))"

# Verify structure matches
yq diff src/locales/en.yaml src/locales/zh-Hans.yaml
```

---

## Example 6: Progressive Enhancement

**Scenario**: Start with single file, then split as project grows.

### Phase 1: Small Project (50 keys)

```
locales/
├── en/
│   └── common.json    # 50 keys
└── zh-Hans/
    └── common.json    # 50 keys
```

### Phase 2: Growth (200 keys) - Time to Split

```
locales/
├── en/
│   ├── common.json      # 50 keys
│   └── features.json    # 150 keys (NEW)
└── zh-Hans/
    ├── common.json      # 50 keys
    └── features.json    # 150 keys (NEW)
```

### Phase 3: Large Project (500+ keys) - Further Split

```
locales/
├── en/
│   ├── common.json       # 50 keys
│   ├── auth.json         # 80 keys (split from features)
│   ├── dashboard.json    # 120 keys (split from features)
│   ├── settings.json     # 100 keys (split from features)
│   └── reports.json      # 150 keys (remaining)
└── zh-Hans/
    ├── common.json       # 50 keys
    ├── auth.json         # 80 keys
    ├── dashboard.json    # 120 keys
    ├── settings.json     # 100 keys
    └── reports.json      # 150 keys
```

---

## Common Translation Patterns

### Pattern 1: Buttons and Actions

```json
// English
{
  "submit": "Submit",
  "cancel": "Cancel",
  "delete": "Delete",
  "edit": "Edit",
  "save": "Save"
}

// Chinese
{
  "submit": "提交",
  "cancel": "取消",
  "delete": "删除",
  "edit": "编辑",
  "save": "保存"
}
```

### Pattern 2: Validation Messages

```json
// English
{
  "required": "{{field}} is required",
  "minLength": "{{field}} must be at least {{min}} characters",
  "maxLength": "{{field}} must not exceed {{max}} characters",
  "invalidEmail": "Please enter a valid email address"
}

// Chinese
{
  "required": "{{field}} 为必填项",
  "minLength": "{{field}} 至少需要 {{min}} 个字符",
  "maxLength": "{{field}} 不能超过 {{max}} 个字符",
  "invalidEmail": "请输入有效的电子邮件地址"
}
```

### Pattern 3: Navigation Menus

```json
// English
{
  "dashboard": "Dashboard",
  "analytics": "Analytics",
  "reports": "Reports",
  "settings": "Settings",
  "logout": "Log Out"
}

// Chinese
{
  "dashboard": "仪表板",
  "analytics": "分析",
  "reports": "报告",
  "settings": "设置",
  "logout": "登出"
}
```

### Pattern 4: Date and Time

```json
// English
{
  "today": "Today",
  "yesterday": "Yesterday",
  "tomorrow": "Tomorrow",
  "lastWeek": "Last week",
  "nextWeek": "Next week"
}

// Chinese
{
  "today": "今天",
  "yesterday": "昨天",
  "tomorrow": "明天",
  "lastWeek": "上周",
  "nextWeek": "下周"
}
```

---

## Testing Your Translations

### 1. Manual Testing Checklist

```bash
# Load application in each language
# Test all pages and components
# Verify:
□ All text displays correctly
□ No missing translations (no raw keys like "common.welcome")
□ Placeholders work correctly
□ No encoding issues
□ Text fits in UI elements
□ Cultural appropriateness
```

### 2. Automated Testing

```javascript
// Test that all keys have translations
const en = require('./public/locales/en/common.json');
const zh = require('./public/locales/zh-Hans/common.json');

const enKeys = Object.keys(en);
const zhKeys = Object.keys(zh);

const missing = enKeys.filter(key => !zhKeys.includes(key));

if (missing.length > 0) {
  console.error('Missing translations:', missing);
  process.exit(1);
}

console.log('✓ All keys have translations');
```

---

## Summary of Key Examples

| Scenario | Solution | Files Created |
|----------|----------|---------------|
| New language, small project (< 200 keys) | Single file | 1 file per language |
| Complete partial translations | Add missing keys systematically | Update existing files |
| Large project (> 200 keys) | Split by feature/domain | 5-10 files per language |
| React with i18next | Use namespace imports | Match React structure |
| Vue with YAML | Maintain YAML structure | Use YAML format |

Remember: **Always aim for 100% completion** before moving to the next file!
