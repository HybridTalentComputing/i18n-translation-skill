# Vue I18n Translation Strategy

Vue I18n is the official internationalization plugin for Vue.js. This guide provides specific strategies for translating Vue applications effectively.

## Identifying Vue I18n Projects

**Package.json indicators:**
```json
{
  "dependencies": {
    "vue-i18n": "^9.0.0",
    "vue-i18n-next": "^9.0.0"
  }
}
```

**Common file locations:**
```
src/locales/{language}.json
src/locales/{language}.yaml
src/i18n/{language}.json
src/translations/{language}.json
```

## File Structure

### Standard Structure (Vue 3 + Vue I18n v9)
```
src/locales/
├── en.json           # English
├── es.json           # Spanish
└── zh-Hans.json      # Chinese (Simplified)
```

### Modular Structure (Recommended for large apps)
```
src/locales/
├── en/
│   ├── index.json    # Main translations
│   ├── auth.json
│   ├── dashboard.json
│   └── settings.json
├── es/
│   ├── index.json
│   ├── auth.json
│   ├── dashboard.json
│   └── settings.json
└── zh-Hans/
    ├── index.json
    ├── auth.json
    ├── dashboard.json
    └── settings.json
```

## Vue I18n Specific Features

### 1. Interpolation

Vue I18n supports multiple interpolation styles:

**Named interpolation** (recommended):
```json
// English
{
  "greeting": "Hello {name}",
  "message": "You have {count} new messages"
}

// Chinese
{
  "greeting": "你好 {name}",
  "message": "您有 {count} 条新消息"
}
```

**List interpolation**:
```json
// English
{
  "greeting": "Hello {0} {1}"
}

// Chinese
{
  "greeting": "你好 {0} {1}"
}
```

### 2. Pluralization

```json
// English
{
  "apple": "no apples | one apple | {count} apples",
  "car": "{n} car | {n} cars"
}

// Chinese (simpler plural rules)
{
  "apple": "{count} 个苹果",
  "car": "{n} 辆车"
}
```

**Note**: Vue I18n v9 uses pipe `|` separator for plural forms. Preserve this structure even for languages with simpler plural rules.

### 3. Linked Messages

```json
// English
{
  "message": {
    "hello": "Hello @:message.world",
    "world": "World"
  }
}

// Chinese
{
  "message": {
    "hello": "你好 @:message.world",
    "world": "世界"
  }
}
```

Preserve the `@:key.path` syntax for linked messages.

### 4. Formatting

```json
{
  "price": "Price: {price}",
  "date": "Date: {date}",
  "number": "Count: {amount}"
}
```

Vue I18n handles formatting via custom formatters in configuration.

## Code Integration Patterns

### Using Composition API (Vue 3)

```javascript
import { useI18n } from 'vue-i18n';

export default {
  setup() {
    const { t, locale } = useI18n();

    return {
      greeting: t('greeting'),
      changeLocale: (lang) => locale.value = lang
    };
  }
};
```

### Using Options API

```javascript
export default {
  computed: {
    greeting() {
      return this.$t('greeting');
    }
  },
  methods: {
    changeLocale(lang) {
      this.$i18n.locale = lang;
    }
  }
};
```

### Template usage

```vue
<template>
  <div>
    <h1>{{ $t('welcome') }}</h1>
    <p>{{ $t('greeting', { name: userName }) }}</p>
  </div>
</template>
```

## Common Vue Component Translations

### Navigation Components
```json
{
  "nav": {
    "home": "Home",
    "about": "About",
    "contact": "Contact",
    "dashboard": "Dashboard",
    "settings": "Settings"
  }
}
```

### Form Components
```json
{
  "form": {
    "label": {
      "name": "Name",
      "email": "Email",
      "password": "Password"
    },
    "error": {
      "required": "This field is required",
      "email": "Please enter a valid email",
      "minLength": "Minimum {min} characters required"
    },
    "button": {
      "submit": "Submit",
      "cancel": "Cancel",
      "reset": "Reset"
    }
  }
}
```

### Validation Messages
```json
{
  "validation": {
    "required": "{field} is required",
    "email": "Invalid email format",
    "min": "{field} must be at least {min} characters",
    "max": "{field} cannot exceed {max} characters"
  }
}
```

## Configuration Examples

### Vue 3 + Vue I18n v9

```javascript
// src/i18n/index.js
import { createI18n } from 'vue-i18n';
import en from '../locales/en.json';
import zhHans from '../locales/zh-Hans.json';

const i18n = createI18n({
  legacy: false,  // Use Composition API mode
  locale: 'en',
  fallbackLocale: 'en',
  messages: {
    en,
    'zh-Hans': zhHans
  }
});

export default i18n;
```

### Modular Configuration

```javascript
// src/i18n/index.js
import { createI18n } from 'vue-i18n';

function loadLocaleMessages() {
  const locales = require.context('../locales', true, /[a-z0-9]+\.json$/i);
  const messages = {};

  locales.keys().forEach(key => {
    const matched = key.match(/([a-z0-9]+)\./i);
    if (matched && matched.length > 1) {
      const locale = matched[1];
      messages[locale] = locales(key);
    }
  });

  return messages;
}

export default createI18n({
  legacy: false,
  locale: 'en',
  fallbackLocale: 'en',
  messages: loadLocaleMessages()
});
```

### YAML Format Support

```javascript
import { createI18n } from 'vue-i18n';
import yaml from 'js-yaml';
import fs from 'fs';

function loadYamlLocale(locale) {
  const content = fs.readFileSync(`./src/locales/${locale}.yaml`, 'utf-8');
  return yaml.load(content);
}

const i18n = createI18n({
  legacy: false,
  locale: 'en',
  messages: {
    en: loadYamlLocale('en'),
    'zh-Hans': loadYamlLocale('zh-Hans')
  }
});
```

## Splitting Strategies for Vue Apps

### By Feature (Recommended)

```
src/locales/
├── en/
│   ├── common.json       # Shared components (buttons, labels)
│   ├── auth.json         # Authentication (login, signup)
│   ├── dashboard.json    # Dashboard pages
│   ├── settings.json     # Settings pages
│   └── validation.json   # Form validation messages
└── zh-Hans/
    └── (matching structure)
```

### By Route

```
src/locales/
├── en/
│   ├── home.json
│   ├── about.json
│   ├── profile.json
│   └── admin.json
└── zh-Hans/
    └── (matching structure)
```

## Translation Workflow for Vue Apps

### Step 1: Identify all translation keys
```bash
# Find all $t() and t() calls in Vue files
grep -rh "\$t\|t(" src/ --include="*.vue" --include="*.js"
```

### Step 2: Organize keys by feature
Group keys by the component or route where they're used.

### Step 3: Create split structure
If total keys > 200, split into multiple files.

### Step 4: Translate each file systematically
For each locale file:
1. Read entire source file
2. Count total keys
3. Translate each key maintaining structure
4. Validate JSON/YAML syntax
5. Report completion

### Step 5: Update Vue configuration
Add new locale files to the i18n configuration.

## Special Vue I18n Considerations

### 1. HTML in translations

```json
// If source contains HTML
{
  "message": "Click <a href='/help'>here</a> for help"
}

// Preserve HTML structure in target
{
  "message": "点击 <a href='/help'>这里</a> 获取帮助"
}
```

### 2. Component interpolation (Vue I18n v9)

```json
{
  "welcome": "Welcome to {0}",
  "withComponent": "Check {0} for more info"
}
```

These work with Vue components. Keep the placeholder syntax intact.

### 3. DateTime and NumberFormat

```json
// These are typically handled by Vue I18n's formatters
{
  "date": "Date: {date}",
  "number": "Number: {num}",
  "currency": "Price: {price}"
}
```

Keep the placeholders; Vue I18n will handle formatting.

## Testing in Vue

### Switch Languages
```javascript
// In component
this.$i18n.locale = 'zh-Hans';

// Or with Composition API
const { locale } = useI18n();
locale.value = 'zh-Hans';
```

### Check for Missing Keys
```javascript
// Enable missing key handler
const i18n = createI18n({
  missing: (locale, key) => {
    console.warn(`Missing translation: ${locale}.${key}`);
  }
});
```

## Common Vue I18n Pitfalls

### 1. Breaking interpolation syntax
```json
// Wrong - changed to different syntax
{
  "greeting": "你好 {{name}}"
}

// Correct - kept original syntax
{
  "greeting": "你好 {name}"
}
```

Vue I18n uses `{name}` not `{{name}}`.

### 2. Losing plural structure
```json
// English source
{
  "apple": "no apples | one apple | {count} apples"
}

// Wrong - simplified too much
{
  "apple": "{count} 个苹果"
}

// Correct - maintain pipe structure
{
  "apple": "{count} 个苹果 | {count} 个苹果 | {count} 个苹果"
}
```

### 3. Breaking linked messages
```json
// English
{
  "foo": "@:bar"
}

// Wrong - removed link
{
  "foo": "some translation"
}

// Correct - keep the link
{
  "foo": "@:bar"
}
```

## Quick Commands

```bash
# Validate JSON files
for file in src/locales/*.json; do
  jq . < "$file" > /dev/null && echo "✓ $file" || echo "✗ $file"
done

# Validate YAML files
for file in src/locales/*.yaml; do
  yq eval "$file" > /dev/null && echo "✓ $file" || echo "✗ $file"
done

# Count keys in each locale
echo "English: $(jq 'keys | length' src/locales/en.json)"
echo "Chinese: $(jq 'keys | length' src/locales/zh-Hans.json)"

# Find all translation keys in Vue files
grep -rho "{{ \$t('[^']*') }}" src/ | sed "s/.*{{ \$t('\([^']*\) }}.*/\1/" | sort -u
```

## Best Practices Summary

**Key Points for Vue I18n:**
1. Use `{name}` syntax for interpolation (not `{{name}}`)
2. Maintain plural pipe structure `|` for all languages
3. Preserve linked message syntax `@:key.path`
4. Split large files by feature or route
5. Validate JSON/YAML after each file
6. Test language switching in browser
7. Keep HTML tags intact if present in source

**Remember**: Vue I18n uses different syntax than React i18next. Pay attention to interpolation and pluralization formats!
