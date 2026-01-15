# Modular Translation File Architecture

## Problem: Monolithic Translation Files Don't Scale

**The issue with single large translation files:**

❌ **Context window limits** - Large files consume excessive tokens
❌ **Slow loading** - Parsing 500KB+ JSON files impacts performance
❌ **Merge conflicts** - Multiple translators editing the same file
❌ **Parallel processing** - Can't split work across multiple agents
❌ **Maintenance nightmare** - Hard to find and update specific keys
❌ **Build performance** - Rebuilding entire translation bundle on any change

**Real-world example:**
- Small app (< 1000 strings): Single file is fine (~50KB)
- Medium app (1000-5000 strings): Starting to creak (~150KB)
- Large app (5000-10000+ strings): Completely unworkable (~500KB+)

---

## Solution: Modular Translation Files

Split translations by **feature domain/namespace**:

```
src/i18n/locales/
├── en/
│   ├── common.json        # Shared UI elements
│   ├── chat.json          # Chat interface
│   ├── settings.json      # Settings pages
│   ├── history.json       # Task history
│   ├── mcp.json          # MCP configuration
│   ├── account.json      # User account
│   ├── welcome.json      # Welcome/onboarding
│   └── errors.json       # Error messages
└── zh/
    ├── common.json
    ├── chat.json
    ├── settings.json
    ├── history.json
    ├── mcp.json
    ├── account.json
    ├── welcome.json
    └── errors.json
```

**Benefits:**
✅ **Context-efficient** - Only load needed namespaces (~10-20KB each)
✅ **Parallel work** - Different agents work on different files simultaneously
✅ **Fast builds** - Only rebuild changed namespaces
✅ **Easy maintenance** - Find keys in small, focused files
✅ **Team collaboration** - Different translators own different files
✅ **Scalable** - Add new features without touching existing files

---

## When to Split Files

### Split Immediately When:
- **Project has 10+ top-level namespaces** (different features)
- **Translation file > 100KB** (single language)
- **Team has multiple translators** working in parallel
- **Using subagents** for translation work
- **Build times are slow** due to i18n

### Keep Single File When:
- **Small project** (< 1000 strings total)
- **Single developer** working on i18n
- **Rapid prototyping** (can refactor later)

---

## File Splitting Strategy

### Option 1: Split by Namespace (Recommended)

**One file per major namespace:**

```
locales/
├── en/
│   ├── common.json      # All 'common' namespace keys
│   ├── chat.json        # All 'chat' namespace keys
│   ├── settings.json    # All 'settings' namespace keys
│   └── history.json     # All 'history' namespace keys
└── zh/
    ├── common.json
    ├── chat.json
    ├── settings.json
    └── history.json
```

**When to use:** Most projects, clear separation between features

---

### Option 2: Split by Feature Domain

**Group related namespaces together:**

```
locales/
├── en/
│   ├── core.json          # common + errors + validation
│   ├── chat-system.json  # chat + chatView + chatTextArea
│   ├── user-management.json # account + profile + auth
│   ├── configuration.json  # settings + mcp
│   └── views.json         # history + welcome + browser
└── zh/
    ├── core.json
    ├── chat-system.json
    ├── user-management.json
    ├── configuration.json
    └── views.json
```

**When to use:** Many small namespaces that are logically related

---

### Option 3: Split by Component Size

**Balance file sizes (target 10-30KB each):**

```
locales/
├── en/
│   ├── ui-elements.json     # All button/label strings (~20KB)
│   ├── messages.json        # All user messages (~30KB)
│   ├── configuration.json   # All settings/config (~25KB)
│   ├── actions.json         # All action descriptions (~15KB)
│   └── states.json          # All loading/error states (~10KB)
```

**When to use:** Clear size categories, less concern about feature boundaries

---

## i18next Configuration for Modular Files

### Using HTTP Backend (Recommended for Production)

**i18n config:**
```typescript
import i18n from "i18next"
import { initReactI18next } from "react-i18next"
import HttpBackend from "i18next-http-backend"
import LanguageDetector from "i18next-browser-languagedetector"

i18n
  .use(HttpBackend)
  .use(LanguageDetector)
  .use(initReactI18next)
  .init({
    lng: "en",
    fallbackLng: "en",

    backend: {
      loadPath: "/locales/{{lng}}/{{ns}}.json",
      // Loads: /locales/en/chat.json, /locales/zh/chat.json
    },

    ns: ["common", "chat", "settings", "history"], // Namespaces to load
    defaultNS: "common",

    react: {
      useSuspense: false,
    },
  })
```

**Benefits:**
- ✅ Lazy loading - Only loads namespaces when used
- ✅ Browser caching - Each file cached separately
- ✅ Production-optimized - Minimal bundle size

---

### Using ES Modules (Recommended for Development)

**i18n config:**
```typescript
import i18n from "i18next"
import { initReactI18next } from "react-i18next"
import LanguageDetector from "i18next-browser-languagedetector"

// Dynamic imports for each namespace
const loadTranslations = async (lng: string, ns: string) => {
  switch (ns) {
    case "common":
      return (await import(`./locales/${lng}/common.json`)).default
    case "chat":
      return (await import(`./locales/${lng}/chat.json`)).default
    case "settings":
      return (await import(`./locales/${lng}/settings.json`)).default
    // ... add all namespaces
    default:
      throw new Error(`Unknown namespace: ${ns}`)
  }
}

i18n
  .use(LanguageDetector)
  .use(initReactI18next)
  .init({
    lng: "en",
    fallbackLng: "en",

    ns: ["common", "chat", "settings", "history"],
    defaultNS: "common",

    resources: {
      en: {
        common: await loadTranslations("en", "common"),
        chat: await loadTranslations("en", "chat"),
        // ... load all namespaces
      },
      zh: {
        common: await loadTranslations("zh", "common"),
        chat: await loadTranslations("zh", "chat"),
        // ... load all namespaces
      },
    },

    react: {
      useSuspense: false,
    },
  })
```

**Benefits:**
- ✅ Type-safe - TypeScript validates all imports
- ✅ Build-time checks - Catch missing files during build
- ✅ Tree-shaking - Unused namespaces can be eliminated

---

### Using Resource Bundles (Simplest for Small Projects)

**i18n config:**
```typescript
import commonEn from "./locales/en/common.json"
import chatEn from "./locales/en/chat.json"
import settingsEn from "./locales/en/settings.json"
import commonZh from "./locales/zh/common.json"
import chatZh from "./locales/zh/chat.json"
import settingsZh from "./locales/zh/settings.json"

i18n
  .use(initReactI18next)
  .init({
    lng: "en",
    fallbackLng: "en",

    resources: {
      en: {
        common: commonEn,
        chat: chatEn,
        settings: settingsEn,
      },
      zh: {
        common: commonZh,
        chat: chatZh,
        settings: settingsZh,
      },
    },

    ns: ["common", "chat", "settings"],
    defaultNS: "common",

    react: {
      useSuspense: false,
    },
  })
```

**Benefits:**
- ✅ Simple - No additional libraries needed
- ✅ Fast - All translations loaded immediately
- ✅ Predictable - Clear what's loaded

**When to use:** Small projects, < 5 namespaces

---

## Component Usage with Modular Files

### Specifying Namespace

**Option 1: Use with namespace**
```typescript
import { useTranslation } from "react-i18next"

function ChatComponent() {
  const { t } = useTranslation("chat")

  return (
    <div>
      <h1>{t("chatView.title")}</h1>
      <p>{t("chatTextArea.placeholder")}</p>
    </div>
  )
}
```

**Option 2: Multiple namespaces**
```typescript
function SettingsComponent() {
  const { t: tCommon } = useTranslation("common")
  const { t: tSettings } = useTranslation("settings")

  return (
    <div>
      <h1>{tSettings("title")}</h1>
      <button>{tCommon("save")}</button>
      <button>{tCommon("cancel")}</button>
    </div>
  )
}
```

---

## Organizing Translation Work by File

### Parallel Processing Strategy

**Split work by namespace file:**

```
Agent 1: common.json      → 250 keys
Agent 2: chat.json        → 300 keys
Agent 3: settings.json    → 200 keys
Agent 4: history.json     → 150 keys
Agent 5: mcp.json        → 180 keys
```

**Each agent:**
1. Extracts strings for its namespace
2. Creates English translation file
3. Translates to all target languages
4. Validates translations
5. Creates pull request

**Benefits:**
- ✅ Parallel processing - 5x faster
- ✅ Clear ownership - No merge conflicts
- ✅ Focused context - Smaller file, easier to understand
- ✅ Independent testing - Each file can be tested separately

---

## Migration Path: From Monolith to Modular

### Step 1: Identify Natural Breaks

Analyze existing namespace structure:

```bash
# List all top-level namespaces
cat en.json | jq 'keys' | grep -v "^_"
```

Example output:
```
["common", "chat", "settings", "history", "mcp", "account", "welcome", "errors"]
```

### Step 2: Create Namespace Files

For each namespace, create separate file:

```bash
# Extract 'chat' namespace
cat en.json | jq '.chat' > en/chat.json
cat zh.json | jq '.chat' > zh/chat.json

# Extract 'settings' namespace
cat en.json | jq '.settings' > en/settings.json
cat zh.json | jq '.settings' > zh/settings.json

# ... repeat for all namespaces
```

### Step 3: Update i18n Configuration

Change from single file to modular:

**Before:**
```typescript
import enTranslations from "./locales/en.json"
import zhTranslations from "./locales/zh.json"
```

**After:**
```typescript
// Option A: Use HTTP backend
backend: {
  loadPath: "/locales/{{lng}}/{{ns}}.json",
}

// Option B: Dynamic imports
const chatEn = await import("./locales/en/chat.json")
const settingsEn = await import("./locales/en/settings.json")
```

### Step 4: Update Component Imports

No changes needed! Components already use namespaces:

```typescript
const { t } = useTranslation("chat")  // Still works
```

### Step 5: Validate and Test

1. Check all files load correctly
2. Test language switching
3. Verify no missing keys
4. Measure performance improvement

---

## File Size Guidelines

### Target Sizes

- **Small namespace** (< 500 keys): 5-15KB ✅
- **Medium namespace** (500-2000 keys): 15-50KB ✅
- **Large namespace** (2000-5000 keys): 50-100KB ⚠️ Consider splitting
- **Huge namespace** (> 5000 keys): > 100KB ❌ Must split

### When to Split Further

If a namespace file is > 50KB:

```
chat.json (80KB)
  ↓ Split into:
├── chat-core.json      (25KB) - Main chat UI
├── chat-messages.json  (30KB) - Message display
├── chat-input.json     (15KB) - Input controls
└── chat-browser.json   (10KB) - Browser integration
```

---

## Best Practices

### Do's ✅

1. **Plan namespaces upfront** - Before extracting strings
2. **One namespace per file** - Clear 1:1 mapping
3. **Consistent naming** - `chat.json` for "chat" namespace
4. **Keep files balanced** - Aim for 10-30KB each
5. **Document structure** - Create README.md in locales/ directory
6. **Use subtasks** - Assign each file to different agent
7. **Version control** - Each file in separate PR
8. **Load lazily** - Only load needed namespaces

### Don'ts ❌

1. **Don't create tiny files** - < 50 keys → merge into common
2. **Don't split arbitrarily** - Follow feature boundaries
3. **Don't mix namespaces** - One file = one namespace
4. **Don't forget to update config** - Must add to ns array
5. **Don't ignore dependencies** - If namespace A uses keys from B, load both
6. **Don't create deep nesting** - Files should be flat structure
7. **Don't hardcode paths** - Use dynamic imports or HTTP backend

---

## Advanced: Dynamic Namespace Loading

### Lazy Load Namespaces on Demand

```typescript
// Load chat namespace only when entering chat
const loadChatNamespace = async () => {
  if (!i18n.hasResourceBundle("en", "chat")) {
    const chatEn = await import("./locales/en/chat.json")
    const chatZh = await import("./locales/zh/chat.json")

    i18n.addResourceBundle("en", "chat", chatEn.default)
    i18n.addResourceBundle("zh", "chat", chatZh.default)
  }
}

// In component
useEffect(() => {
  loadChatNamespace()
}, [])
```

**Benefits:**
- ✅ Initial load much faster
- ✅ Smaller bundle size
- ✅ Load features on-demand

---

## Validation

### Check File Sizes

```bash
# List all English files with sizes
ls -lh locales/en/*.json

# Expected output:
# -rw-r--r--  12K en/common.json
# -rw-r--r--  25K en/chat.json
# -rw-r--r--  18K en/settings.json
```

### Validate Consistency

```bash
# Check all languages have same namespaces
comm -23 <(ls locales/en/ | sort) <(ls locales/zh/ | sort)

# Should output nothing (if same namespaces)
```

### Count Translation Keys

```bash
# Count keys in each namespace file
for file in locales/en/*.json; do
  echo "$file: $(jq 'keys | length' "$file") keys"
done
```

---

## Real-World Example: Large E-Commerce App

**Monolithic approach (BAD):**
```
locales/
├── en.json (450KB, 15000 keys)  ❌ Too large
└── zh.json (450KB, 15000 keys)
```

**Modular approach (GOOD):**
```
locales/
├── en/
│   ├── common.json (15KB)         # Shared UI
│   ├── catalog.json (85KB)        # Product catalog
│   ├── cart.json (45KB)           # Shopping cart
│   ├── checkout.json (65KB)       # Checkout flow
│   ├── account.json (55KB)        # User account
│   ├── orders.json (75KB)         # Order history
│   ├── payments.json (40KB)       # Payment processing
│   ├── search.json (35KB)         # Search functionality
│   └── notifications.json (30KB)  # User notifications
└── zh/
    ├── common.json (12KB)
    ├── catalog.json (82KB)
    ├── cart.json (42KB)
    ├── checkout.json (62KB)
    ├── account.json (52KB)
    ├── orders.json (72KB)
    ├── payments.json (38KB)
    ├── search.json (33KB)
    └── notifications.json (28KB)
```

**Parallel work assignment:**
- Agent 1: common + notifications
- Agent 2: catalog + search
- Agent 3: cart + checkout
- Agent 4: account + orders
- Agent 5: payments

**Result:** 5x faster, no merge conflicts, focused context

---

## Summary: Decision Tree

```
Start: Do you have i18n files?
  ↓
Yes → Are they > 100KB?
  ↓
  Yes → SPLIT by namespace immediately
  ↓
  No → Do you have 10+ namespaces?
    ↓
    Yes → SPLIT by namespace
    ↓
    No → Keep single file (for now)
      ↓
      Monitor file size as you add keys
      ↓
      Split when > 100KB
```

**Key principle:** Split **before** it becomes a problem, not after.

---

## Checklist: Modular File Setup

### Planning Phase
- [ ] Identified all namespaces in project
- [ ] Estimated keys per namespace
- [ ] Chose file splitting strategy
- [ ] Created namespace-to-file mapping document

### Implementation Phase
- [ ] Split monolithic file into namespace files
- [ ] Updated i18n configuration (HTTP backend or dynamic imports)
- [ ] Added all namespaces to `ns` array in config
- [ ] Updated component imports (if needed)
- [ ] Tested all namespaces load correctly

### Validation Phase
- [ ] Verified each file < 100KB
- [ ] Confirmed all languages have matching files
- [ ] Tested language switching works
- [ ] Measured performance improvement
- [ ] No console errors about missing resources

### Documentation Phase
- [ ] Created locales/README.md with structure
- [ ] Documented which components use which namespaces
- [ ] Added guidelines for adding new namespaces
- [ ] Updated team workflow documentation

---

**End of Modular Translation File Architecture**
