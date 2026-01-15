# Namespace Organization Guide

This document provides comprehensive guidance on organizing translation keys by namespace for optimal maintainability and scalability.

## Table of Contents

1. [Namespace Principles](#namespace-principles)
2. [Recommended Namespace Structure](#recommended-namespace-structure)
3. [Naming Conventions](#naming-conventions)
4. [Category Guidelines](#category-guidelines)
5. [Examples](#examples)
6. [Anti-Patterns](#anti-patterns)

---

## Namespace Principles

### 1. Purpose of Namespaces

Namespaces organize translation keys into logical groups, providing:

✅ **Better organization** - Related strings grouped together
✅ **Easier maintenance** - Find and update translations faster
✅ **Improved performance** - Load only needed namespaces
✅ **Clearer context** - Translators understand where strings are used
✅ **Scalability** - Add new features without conflicts

### 2. When to Create Namespaces

**Create a new namespace when:**
- A distinct feature/area has 5+ translation keys
- Strings are specific to a particular component or feature
- You want to keep translations logically separated
- Different teams might work on different areas

**Don't create a namespace when:**
- Only 1-2 strings exist (use `common` namespace)
- Strings are generic and reused everywhere
- The namespace would be redundant with existing ones

### 3. Granularity Level

**Aim for medium granularity:**

❌ **Too coarse** (one big namespace):
```json
{
  "app": {
    "save": "...",
    "title": "...",
    "email": "...",
    "sendMessage": "...",
    "delete": "...",
    "loading": "..."
  }
}
```

✅ **Just right** (feature-based namespaces):
```json
{
  "common": {
    "save": "...",
    "delete": "...",
    "loading": "..."
  },
  "chat": {
    "sendMessage": "...",
    "title": "..."
  },
  "form": {
    "email": "..."
  }
}
```

❌ **Too fine** (every component separate):
```json
{
  "header": { "title": "..." },
  "footer": { "text": "..." },
  "sidebar": { "toggle": "..." },
  "button1": { "save": "..." },
  "button2": { "delete": "..." }
}
```

---

## Recommended Namespace Structure

### Standard Namespaces

Most applications should use these standard namespaces:

#### 1. `common` - Shared UI Elements

**Purpose:** Generic strings used throughout the app

**Contents:**
- Action buttons: save, cancel, delete, edit, confirm
- States: loading, error, success, pending
- Common labels: name, email, password, submit
- Universal terms: yes, no, close, back

**Example:**
```json
{
  "common": {
    "actions": {
      "save": "Save",
      "cancel": "Cancel",
      "delete": "Delete",
      "edit": "Edit",
      "confirm": "Confirm",
      "submit": "Submit",
      "reset": "Reset",
      "refresh": "Refresh",
      "search": "Search",
      "clear": "Clear"
    },
    "states": {
      "loading": "Loading...",
      "error": "Error",
      "success": "Success",
      "pending": "Pending",
      "complete": "Complete",
      "empty": "No data",
      "notFound": "Not found"
    },
    "labels": {
      "name": "Name",
      "email": "Email",
      "password": "Password",
      "username": "Username",
      "description": "Description",
      "title": "Title"
    },
    "booleans": {
      "yes": "Yes",
      "no": "No",
      "true": "True",
      "false": "False",
      "enabled": "Enabled",
      "disabled": "Disabled"
    },
    "time": {
      "today": "Today",
      "yesterday": "Yesterday",
      "tomorrow": "Tomorrow",
      "justNow": "Just now",
      "minutesAgo": "{{minutes}} minutes ago"
    }
  }
}
```

---

#### 2. Feature-Based Namespaces

Create a namespace for each major feature:

**`chat` - Chat/messaging:**
```json
{
  "chat": {
    "title": "Chat",
    "newConversation": "New Conversation",
    "inputPlaceholder": "Type a message...",
    "sendButton": "Send",
    "attachment": "Attachment",
    "voiceMessage": "Voice Message",
    "thinking": "Thinking...",
    "empty": {
      "noMessages": "No messages yet",
      "startConversation": "Start a conversation!"
    }
  }
}
```

**`settings` - Settings/configuration:**
```json
{
  "settings": {
    "title": "Settings",
    "saved": "Settings saved successfully",
    "general": {
      "title": "General",
      "darkMode": "Dark mode",
      "notifications": "Enable notifications"
    },
    "language": {
      "title": "Language",
      "description": "Select your preferred language"
    }
  }
}
```

**`auth` - Authentication:**
```json
{
  "auth": {
    "signIn": {
      "title": "Sign In",
      "emailLabel": "Email",
      "passwordLabel": "Password",
      "submitButton": "Sign In",
      "forgotPassword": "Forgot password?",
      "noAccount": "Don't have an account?",
      "signUpLink": "Sign up"
    },
    "signUp": {
      "title": "Sign Up",
      "nameLabel": "Full Name",
      "emailLabel": "Email",
      "passwordLabel": "Password",
      "confirmPasswordLabel": "Confirm Password",
      "submitButton": "Create Account",
      "hasAccount": "Already have an account?",
      "signInLink": "Sign in"
    },
    "errors": {
      "invalidCredentials": "Invalid email or password",
      "weakPassword": "Password is too weak",
      "emailExists": "An account with this email already exists"
    }
  }
}
```

**`profile` - User profile:**
```json
{
  "profile": {
    "title": "My Profile",
    "edit": "Edit Profile",
    "avatar": "Profile Picture",
    "changeAvatar": "Change Picture",
    "fullName": "Full Name",
    "bio": "Bio",
    "location": "Location",
    "website": "Website",
    "joinedDate": "Joined {{date}}"
  }
}
```

**`dashboard` - Dashboard/home:**
```json
{
  "dashboard": {
    "title": "Dashboard",
    "welcome": "Welcome back, {{name}}!",
    "overview": "Overview",
    "recentActivity": "Recent Activity",
    "quickActions": "Quick Actions",
    "stats": {
      "totalUsers": "Total Users",
      "activeNow": "Active Now",
      "revenue": "Revenue",
      "growth": "Growth"
    }
  }
}
```

---

#### 3. Component-Based Namespaces

For reusable UI components:

**`modal` - Dialogs/modals:**
```json
{
  "modal": {
    "close": "Close",
    "confirm": "Confirm",
    "cancel": "Cancel",
    "delete": {
      "title": "Confirm Deletion",
      "message": "Are you sure you want to delete this? This action cannot be undone."
    },
    "unsavedChanges": {
      "title": "Unsaved Changes",
      "message": "You have unsaved changes. Do you want to save them before leaving?"
    }
  }
}
```

**`table` - Data tables:**
```json
{
  "table": {
    "noData": "No data available",
    "loading": "Loading data...",
    "error": "Failed to load data",
    "pagination": {
      "showing": "Showing {{start}} to {{end}} of {{total}} entries",
      "previous": "Previous",
      "next": "Next",
      "page": "Page"
    },
    "actions": {
      "view": "View",
      "edit": "Edit",
      "delete": "Delete"
    }
  }
}
```

**`form` - Form components:**
```json
{
  "form": {
    "required": "This field is required",
    "invalid": "Invalid format",
    "tooShort": "Must be at least {{min}} characters",
    "tooLong": "Must be no more than {{max}} characters",
    "invalidEmail": "Please enter a valid email address",
    "passwordMismatch": "Passwords do not match",
    "submit": "Submit",
    "reset": "Reset Form"
  }
}
```

---

#### 4. Context-Specific Namespaces

**`errors` - Error messages:**
```json
{
  "errors": {
    "network": "Network error. Please check your connection.",
    "server": "Server error. Please try again later.",
    "notFound": "The requested resource was not found.",
    "unauthorized": "You don't have permission to access this.",
    "validation": "Please check your input and try again.",
    "unknown": "An unknown error occurred. Please try again."
  }
}
```

**`notifications` - Toast/alert messages:**
```json
{
  "notifications": {
    "success": {
      "saved": "Saved successfully",
      "deleted": "Deleted successfully",
      "updated": "Updated successfully"
    },
    "error": {
      "generic": "Something went wrong",
      "tryAgain": "Please try again"
    },
    "info": {
      "loading": "Please wait...",
      "processing": "Processing..."
    }
  }
}
```

**`validation` - Form validation:**
```json
{
  "validation": {
    "required": "{{field}} is required",
    "minLength": "{{field}} must be at least {{min}} characters",
    "maxLength": "{{field}} must be no more than {{max}} characters",
    "invalidEmail": "Please enter a valid email address",
    "invalidUrl": "Please enter a valid URL",
    "passwordMismatch": "Passwords do not match",
    "invalidFormat": "{{field}} format is invalid"
  }
}
```

---

## Naming Conventions

### Key Naming Style

**Use camelCase for all keys:**

✅ **Good:**
```json
{
  "chat": {
    "sendMessage": "Send Message",
    "inputPlaceholder": "Type a message...",
    "emptyState": "No messages"
  }
}
```

❌ **Bad:**
```json
{
  "chat": {
    "send_message": "Send Message",  // snake_case
    "InputPlaceholder": "Type...",   // PascalCase
    "EMPTYSTATE": "No messages"      // UPPER_CASE
  }
}
```

### Hierarchical Organization

**Use dot notation for hierarchy:**

```tsx
// In component
const { t } = useTranslation("chat")

<h1>{t("title")}</h1>
<p>{t("empty.noMessages")}</p>
<button>{t("actions.send")}</button>
```

```json
{
  "chat": {
    "title": "Chat",
    "empty": {
      "noMessages": "No messages",
      "startConversation": "Start chatting"
    },
    "actions": {
      "send": "Send",
      "attach": "Attach File"
    }
  }
}
```

### Descriptive but Concise

**Balance clarity with brevity:**

✅ **Good:**
```json
{
  "sendMessage": "Send Message",
  "deleteConfirmation": "Are you sure?",
  "emailPlaceholder": "Enter your email"
}
```

❌ **Bad (too verbose):**
```json
{
  "buttonThatSendsMessageToChat": "Send Message",
  "messageConfirmingDeleteAction": "Are you sure?",
  "inputFieldPlaceholderForEmail": "Enter your email"
}
```

❌ **Bad (too vague):**
```json
{
  "send": "Send Message",
  "confirm": "Are you sure?",
  "placeholder": "Enter your email"
}
```

---

## Category Guidelines

### When to Use Each Namespace

| Namespace | Use When... | Example |
|-----------|-------------|---------|
| `common` | String used in 3+ places | "Save", "Cancel", "Loading" |
| `{feature}` | Feature-specific UI | Chat messages, Dashboard stats |
| `settings` | Settings/configuration | "Dark mode", "Language" |
| `auth` | Login/signup/forgot password | "Sign in", "Reset password" |
| `errors` | Error messages | "Network error", "Not found" |
| `validation` | Form validation | "Required field", "Invalid format" |
| `notifications` | Success/error toasts | "Saved successfully" |
| `modal` | Dialog text | "Confirm deletion" |
| `form` | Generic form elements | "Submit", "Required" |
| `table` | Data table UI | "No data", "Previous page" |

---

## Examples

### Example 1: E-Commerce App

```json
{
  "common": { /* shared actions */ },
  "home": {
    "hero": {
      "title": "Welcome to Our Store",
      "subtitle": "Find the best products",
      "shopNow": "Shop Now"
    },
    "featured": {
      "title": "Featured Products",
      "viewAll": "View All"
    }
  },
  "product": {
    "addToCart": "Add to Cart",
    "buyNow": "Buy Now",
    "outOfStock": "Out of Stock",
    "inStock": "In Stock",
    "quantity": "Quantity",
    "specifications": "Specifications",
    "reviews": "Reviews"
  },
  "cart": {
    "title": "Shopping Cart",
    "empty": "Your cart is empty",
    "subtotal": "Subtotal",
    "shipping": "Shipping",
    "total": "Total",
    "checkout": "Checkout"
  },
  "checkout": {
    "title": "Checkout",
    "shipping": "Shipping Information",
    "payment": "Payment Method",
    "review": "Review Order",
    "placeOrder": "Place Order"
  }
}
```

---

### Example 2: Project Management App

```json
{
  "common": { /* shared */ },
  "projects": {
    "title": "Projects",
    "create": "Create Project",
    "delete": "Delete Project",
    "archive": "Archive Project",
    "settings": "Project Settings",
    "members": "Project Members"
  },
  "tasks": {
    "title": "Tasks",
    "create": "Create Task",
    "assignee": "Assignee",
    "dueDate": "Due Date",
    "priority": "Priority",
    "status": "Status",
    "move": "Move Task",
    "delete": "Delete Task"
  },
  "team": {
    "title": "Team",
    "members": "Members",
    "invite": "Invite Member",
    "remove": "Remove Member",
    "admin": "Admin",
    "member": "Member"
  },
  "activity": {
    "title": "Activity",
    "filter": "Filter Activity",
    "latest": "Latest",
    "older": "Older"
  }
}
```

---

### Example 3: Social Media App

```json
{
  "common": { /* shared */ },
  "feed": {
    "title": "Feed",
    "newPost": "New Post",
    "like": "Like",
    "comment": "Comment",
    "share": "Share",
    "empty": "No posts yet"
  },
  "profile": {
    "title": "Profile",
    "edit": "Edit Profile",
    "followers": "Followers",
    "following": "Following",
    "posts": "Posts",
    "joinDate": "Joined {{date}}"
  },
  "messages": {
    "title": "Messages",
    "newConversation": "New Message",
    "send": "Send",
    "typing": "Typing...",
    "online": "Online",
    "offline": "Offline"
  },
  "notifications": {
    "title": "Notifications",
    "markAllRead": "Mark All as Read",
    "like": "liked your post",
    "comment": "commented on your post",
    "follow": "started following you",
    "mention": "mentioned you"
  }
}
```

---

## Anti-Patterns

### ❌ Anti-Pattern 1: Flat Structure

**Don't flatten everything:**
```json
{
  "saveButton": "Save",
  "cancelButton": "Cancel",
  "deleteButton": "Delete",
  "sendButton": "Send",
  "chatTitle": "Chat",
  "settingsTitle": "Settings",
  "profileTitle": "Profile"
}
```

**Why it's bad:** Hard to maintain, no organization, difficult to find related strings.

---

### ❌ Anti-Pattern 2: Too Many Namespaces

**Don't create a namespace for every small component:**
```json
{
  "header": { "title": "..." },
  "footer": { "text": "..." },
  "sidebar": { "toggle": "..." },
  "buttonPrimary": { "submit": "..." },
  "buttonSecondary": { "cancel": "..." }
}
```

**Why it's bad:** Over-fragmentation, harder to reuse strings, more boilerplate.

---

### ❌ Anti-Pattern 3: Duplicating Common Strings

**Don't repeat common strings in feature namespaces:**
```json
{
  "common": {
    "save": "Save",
    "cancel": "Cancel"
  },
  "chat": {
    "save": "Save",      // ❌ Duplicate
    "cancel": "Cancel",  // ❌ Duplicate
    "sendMessage": "Send Message"
  }
}
```

**Why it's bad:** Maintenance nightmare, inconsistent translations, wasted space.

---

### ❌ Anti-Pattern 4: Inconsistent Naming

**Don't mix naming conventions:**
```json
{
  "chat": {
    "sendMessage": "Send",
    "user_name": "Username",     // snake_case
    "EmptyState": "No messages", // PascalCase
    "VIEW-PROFILE": "View"       // kebab-case with caps
  }
}
```

**Why it's bad:** Confusing, error-prone, hard to remember keys.

---

### ❌ Anti-Pattern 5: Deep Nesting

**Don't nest too deeply:**
```json
{
  "chat": {
    "message": {
      "list": {
        "item": {
          "actions": {
            "send": "Send"
          }
        }
      }
    }
  }
}
```

**Why it's bad:** Excessive verbosity, hard to use, difficult to maintain.

**Limit to 3-4 levels maximum.**

---

## Best Practices Summary

### ✅ Do's

1. **Group by feature** - Create namespaces for logical features
2. **Use `common` for shared strings** - Don't repeat common actions
3. **Keep it flat-ish** - 2-3 levels of nesting maximum
4. **Use camelCase** - Consistent naming convention
5. **Be descriptive** - Keys should be self-documenting
6. **Plan for growth** - Structure should scale with app
7. **Keep related items together** - Group functionally

### ❌ Don'ts

1. **Don't over-fragment** - Not every component needs a namespace
2. **Don't under-organize** - One big namespace is not maintainable
3. **Don't duplicate** - Reuse strings via `common` namespace
4. **Don't nest too deep** - Keep hierarchy reasonable
5. **Don't mix conventions** - Stick to camelCase
6. **Don't use vague names** - Be specific and clear
7. **Don't forget context** - Organize by usage/context

---

## Migration Strategy

If you have an existing flat namespace structure, migrate gradually:

**Step 1:** Identify feature groups
**Step 2:** Create new namespaces
**Step 3:** Move keys to new namespaces
**Step 4:** Update components to use new structure
**Step 5:** Remove old keys
**Step 6:** Test thoroughly

---

**End of Namespace Guide**
