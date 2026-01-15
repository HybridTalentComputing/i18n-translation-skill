# Translation Patterns and Examples

This document provides comprehensive patterns and examples for translating React components using i18next.

## Table of Contents

1. [Basic Patterns](#basic-patterns)
2. [Advanced Patterns](#advanced-patterns)
3. [Component-Specific Patterns](#component-specific-patterns)
4. [Common Mistakes](#common-mistakes)
5. [Real-World Examples](#real-world-examples)

---

## Basic Patterns

### 1. Simple Text Content

**Pattern:** Replace static text with `t()` call.

**Before:**
```tsx
<div>
  <h1>Welcome</h1>
  <p>This is the settings page</p>
</div>
```

**After:**
```tsx
const { t } = useTranslation("settings")

<div>
  <h1>{t("welcome")}</h1>
  <p>{t("description")}</p>
</div>
```

**Translation files:**
```json
{
  "settings": {
    "welcome": "Welcome",
    "description": "This is the settings page"
  }
}
```

```json
{
  "settings": {
    "welcome": "欢迎",
    "description": "这是设置页面"
  }
}
```

---

### 2. Attributes

**Pattern:** Translate attributes like `placeholder`, `title`, `alt`.

**Before:**
```tsx
<input placeholder="Enter your email" />
<button title="Click to submit">Submit</button>
<img src="avatar.png" alt="User avatar" />
<label htmlFor="email">Email address</label>
```

**After:**
```tsx
const { t } = useTranslation("form")

<input placeholder={t("emailPlaceholder")} />
<button title={t("submitTitle")}>{t("submit")}</button>
<img src="avatar.png" alt={t("userAvatar")} />
<label htmlFor="email">{t("emailLabel")}</label>
```

**Translation files:**
```json
{
  "form": {
    "emailPlaceholder": "Enter your email",
    "submitTitle": "Click to submit",
    "submit": "Submit",
    "userAvatar": "User avatar",
    "emailLabel": "Email address"
  }
}
```

---

### 3. Button Text

**Pattern:** Extract button text and descriptions.

**Before:**
```tsx
<button onClick={handleSubmit}>Save Changes</button>
<button onClick={handleCancel}>Cancel</button>
<button onClick={handleDelete} className="danger">
  Delete Account
</button>
```

**After:**
```tsx
const { t } = useTranslation("buttons")

<button onClick={handleSubmit}>{t("save")}</button>
<button onClick={handleCancel}>{t("cancel")}</button>
<button onClick={handleDelete} className="danger">
  {t("deleteAccount")}
</button>
```

**Translation files:**
```json
{
  "buttons": {
    "save": "Save Changes",
    "cancel": "Cancel",
    "deleteAccount": "Delete Account"
  }
}
```

---

### 4. Conditional Text

**Pattern:** Use translation keys based on conditions.

**Before:**
```tsx
<div>
  {status === "loading" && <p>Loading data...</p>}
  {status === "success" && <p>Data loaded successfully</p>}
  {status === "error" && <p>Failed to load data</p>}
</div>
```

**After:**
```tsx
const { t } = useTranslation("status")

<div>
  {status === "loading" && <p>{t("loading")}</p>}
  {status === "success" && <p>{t("success")}</p>}
  {status === "error" && <p>{t("error")}</p>}
</div>
```

**Translation files:**
```json
{
  "status": {
    "loading": "Loading data...",
    "success": "Data loaded successfully",
    "error": "Failed to load data"
  }
}
```

---

## Advanced Patterns

### 5. Interpolation

**Pattern:** Insert dynamic values into translations.

**Before:**
```tsx
<p>Welcome, {userName}!</p>
<p>You have {unreadCount} new messages</p>
<p>Signed in as {userEmail}</p>
```

**After:**
```tsx
const { t } = useTranslation("user")

<p>{t("welcome", { userName })}</p>
<p>{t("unreadMessages", { count: unreadCount })}</p>
<p>{t("signedInAs", { email: userEmail })}</p>
```

**Translation files:**
```json
{
  "user": {
    "welcome": "Welcome, {{userName}}!",
    "unreadMessages": "You have {{count}} new messages",
    "signedInAs": "Signed in as {{email}}"
  }
}
```

**Chinese translations:**
```json
{
  "user": {
    "welcome": "欢迎，{{userName}}！",
    "unreadMessages": "您有 {{count}} 条新消息",
    "signedInAs": "登录为 {{email}}"
  }
}
```

---

### 6. Plurals

**Pattern:** Handle singular/plural forms.

**Before:**
```tsx
<p>
  {itemCount === 1
    ? "1 item selected"
    : `${itemCount} items selected`}
</p>
```

**After (using i18next plural features):**
```tsx
const { t } = useTranslation("list")

<p>{t("itemsSelected", { count: itemCount })}</p>
```

**Translation files:**
```json
{
  "list": {
    "itemsSelected_one": "{{count}} item selected",
    "itemsSelected_other": "{{count}} items selected"
  }
}
```

**Chinese (Chinese doesn't have plurals):**
```json
{
  "list": {
    "itemsSelected_other": "已选择 {{count}} 个项目"
  }
}
```

**Alternative (simpler, separate keys):**
```tsx
<p>{t(itemCount === 1 ? "oneItem" : "manyItems", { count: itemCount })}</p>
```

```json
{
  "list": {
    "oneItem": "1 item selected",
    "manyItems": "{{count}} items selected"
  }
}
```

---

### 7. Complex Sentences

**Pattern:** Break complex strings into smaller, reusable parts.

**Before:**
```tsx
<div>
  <h1>Settings</h1>
  <p>
    Configure your application preferences and account settings below.
    Changes will be saved automatically.
  </p>
</div>
```

**After (option 1 - single key):**
```tsx
const { t } = useTranslation("settings")

<div>
  <h1>{t("title")}</h1>
  <p>{t("description")}</p>
</div>
```

```json
{
  "settings": {
    "title": "Settings",
    "description": "Configure your application preferences and account settings below. Changes will be saved automatically."
  }
}
```

**After (option 2 - split into parts):**
```tsx
<div>
  <h1>{t("title")}</h1>
  <p>
    {t("description1")} {t("description2")}
  </p>
</div>
```

```json
{
  "settings": {
    "title": "Settings",
    "description1": "Configure your application preferences and account settings below.",
    "description2": "Changes will be saved automatically."
  }
}
```

**Recommendation:** Use option 1 for coherence, option 2 only if segments are reused elsewhere.

---

### 8. Dates and Times

**Pattern:** Use date formatters, not translations.

**Before:**
```tsx
<p>Created on January 15, 2026</p>
<p>Last modified 2 hours ago</p>
```

**After (use Intl or formatters):**
```tsx
import { formatDate, formatRelativeTime } from "@/utils/date"

<p>Created on {formatDate(date)}</p>
<p>Last modified {formatRelativeTime(lastModified)}</p>
```

**For static time references:**
```tsx
<p>{t("createdOn", { date: formatDate(date) })}</p>
```

```json
{
  "common": {
    "createdOn": "Created on {{date}}"
  }
}
```

---

### 9. Numbers and Currency

**Pattern:** Use number formatters.

**Before:**
```tsx
<p>Total: $1,234.56</p>
<p>Discount: 25%</p>
```

**After:**
```tsx
import { formatCurrency, formatPercent } from "@/utils/number"

<p>Total: {formatCurrency(1234.56, "USD")}</p>
<p>Discount: {formatPercent(0.25)}</p>
```

---

### 10. Links and URLs

**Pattern:** Translate link text, not URLs.

**Before:**
```tsx
<a href="/docs">Documentation</a>
<a href="https://example.com">Visit our website</a>
```

**After:**
```tsx
<a href="/docs">{t("documentation")}</a>
<a href="https://example.com">{t("visitWebsite")}</a>
```

---

### 11. Lists and Arrays

**Pattern:** Translate list items individually.

**Before:**
```tsx
<ul>
  <li>Read the documentation</li>
  <li>Configure your settings</li>
  <li>Start using the app</li>
</ul>
```

**After:**
```tsx
const { t } = useTranslation("onboarding")

<ul>
  <li>{t("step1")}</li>
  <li>{t("step2")}</li>
  <li>{t("step3")}</li>
</ul>
```

```json
{
  "onboarding": {
    "step1": "Read the documentation",
    "step2": "Configure your settings",
    "step3": "Start using the app"
  }
}
```

---

### 12. Multiple Namespaces

**Pattern:** Use strings from different namespaces.

**Before:**
```tsx
<div>
  <h1>User Profile</h1>
  <button>Save</button>
  <button>Cancel</button>
</div>
```

**After:**
```tsx
const { t: tProfile } = useTranslation("profile")
const { t: tCommon } = useTranslation("common")

<div>
  <h1>{tProfile("title")}</h1>
  <button>{tCommon("save")}</button>
  <button>{tCommon("cancel")}</button>
</div>
```

---

## Component-Specific Patterns

### 13. Modal/Dialog

**Before:**
```tsx
<Modal isOpen={showModal}>
  <ModalHeader>Confirm Deletion</ModalHeader>
  <ModalBody>
    Are you sure you want to delete this item? This action cannot be undone.
  </ModalBody>
  <ModalFooter>
    <Button onClick={onCancel}>Cancel</Button>
    <Button onClick={onConfirm} danger>
      Delete
    </Button>
  </ModalFooter>
</Modal>
```

**After:**
```tsx
const { t } = useTranslation("modal")

<Modal isOpen={showModal}>
  <ModalHeader>{t("confirmDelete")}</ModalHeader>
  <ModalBody>{t("deleteWarning")}</ModalBody>
  <ModalFooter>
    <Button onClick={onCancel}>{t("cancel")}</Button>
    <Button onClick={onConfirm} danger>
      {t("delete")}
    </Button>
  </ModalFooter>
</Modal>
```

```json
{
  "modal": {
    "confirmDelete": "Confirm Deletion",
    "deleteWarning": "Are you sure you want to delete this item? This action cannot be undone.",
    "cancel": "Cancel",
    "delete": "Delete"
  }
}
```

---

### 14. Form with Validation

**Before:**
```tsx
<form onSubmit={handleSubmit}>
  <label htmlFor="email">Email Address</label>
  <input
    type="email"
    id="email"
    placeholder="Enter your email"
  />
  {errors.email && <span className="error">Email is required</span>}

  <label htmlFor="password">Password</label>
  <input
    type="password"
    id="password"
    placeholder="Enter a strong password"
  />
  {errors.password && <span className="error">Password must be at least 8 characters</span>}

  <button type="submit">Sign In</button>
</form>
```

**After:**
```tsx
const { t } = useTranslation("auth")

<form onSubmit={handleSubmit}>
  <label htmlFor="email">{t("emailLabel")}</label>
  <input
    type="email"
    id="email"
    placeholder={t("emailPlaceholder")}
  />
  {errors.email && <span className="error">{t("emailRequired")}</span>}

  <label htmlFor="password">{t("passwordLabel")}</label>
  <input
    type="password"
    id="password"
    placeholder={t("passwordPlaceholder")}
  />
  {errors.password && <span className="error">{t("passwordMinLength")}</span>}

  <button type="submit">{t("signIn")}</button>
</form>
```

```json
{
  "auth": {
    "emailLabel": "Email Address",
    "emailPlaceholder": "Enter your email",
    "emailRequired": "Email is required",
    "passwordLabel": "Password",
    "passwordPlaceholder": "Enter a strong password",
    "passwordMinLength": "Password must be at least 8 characters",
    "signIn": "Sign In"
  }
}
```

---

### 15. Table Headers and Cells

**Before:**
```tsx
<table>
  <thead>
    <tr>
      <th>Name</th>
      <th>Email</th>
      <th>Status</th>
      <th>Actions</th>
    </tr>
  </thead>
  <tbody>
    {users.map(user => (
      <tr key={user.id}>
        <td>{user.name}</td>
        <td>{user.email}</td>
        <td>{user.status}</td>
        <td>
          <button>Edit</button>
          <button>Delete</button>
        </td>
      </tr>
    ))}
  </tbody>
</table>
```

**After:**
```tsx
const { t } = useTranslation("users")

<table>
  <thead>
    <tr>
      <th>{t("nameHeader")}</th>
      <th>{t("emailHeader")}</th>
      <th>{t("statusHeader")}</th>
      <th>{t("actionsHeader")}</th>
    </tr>
  </thead>
  <tbody>
    {users.map(user => (
      <tr key={user.id}>
        <td>{user.name}</td>
        <td>{user.email}</td>
        <td>{t(user.status)}</td>
        <td>
          <button>{t("edit")}</button>
          <button>{t("delete")}</button>
        </td>
      </tr>
    ))}
  </tbody>
</table>
```

```json
{
  "users": {
    "nameHeader": "Name",
    "emailHeader": "Email",
    "statusHeader": "Status",
    "actionsHeader": "Actions",
    "active": "Active",
    "inactive": "Inactive",
    "pending": "Pending",
    "edit": "Edit",
    "delete": "Delete"
  }
}
```

---

### 16. Loading and Empty States

**Before:**
```tsx
{isLoading ? (
  <div className="loading">
    <Spinner />
    <p>Loading your data...</p>
  </div>
) : data.length === 0 ? (
  <div className="empty">
    <p>No items found</p>
    <p>Try adjusting your filters</p>
  </div>
) : (
  <div>{/* content */}</div>
)}
```

**After:**
```tsx
const { t } = useTranslation("state")

{isLoading ? (
  <div className="loading">
    <Spinner />
    <p>{t("loadingData")}</p>
  </div>
) : data.length === 0 ? (
  <div className="empty">
    <p>{t("noItems")}</p>
    <p>{t("tryFilters")}</p>
  </div>
) : (
  <div>{/* content */}</div>
)}
```

```json
{
  "state": {
    "loadingData": "Loading your data...",
    "noItems": "No items found",
    "tryFilters": "Try adjusting your filters"
  }
}
```

---

### 17. Navigation Items

**Before:**
```tsx
<nav>
  <NavLink to="/">Home</NavLink>
  <NavLink to="/about">About</NavLink>
  <NavLink to="/products">Products</NavLink>
  <NavLink to="/contact">Contact</NavLink>
</nav>
```

**After:**
```tsx
const { t } = useTranslation("nav")

<nav>
  <NavLink to="/">{t("home")}</NavLink>
  <NavLink to="/about">{t("about")}</NavLink>
  <NavLink to="/products">{t("products")}</NavLink>
  <NavLink to="/contact">{t("contact")}</NavLink>
</nav>
```

---

### 18. Notifications and Alerts

**Before:**
```tsx
{showNotification && (
  <Alert type="success" onClose={handleClose}>
    <strong>Success!</strong> Your changes have been saved.
  </Alert>
)}

{showError && (
  <Alert type="error" onClose={handleClose}>
    <strong>Error!</strong> Failed to save changes. Please try again.
  </Alert>
)}
```

**After:**
```tsx
const { t } = useTranslation("alerts")

{showNotification && (
  <Alert type="success" onClose={handleClose}>
    <strong>{t("successTitle")}</strong> {t("successMessage")}
  </Alert>
)}

{showError && (
  <Alert type="error" onClose={handleClose}>
    <strong>{t("errorTitle")}</strong> {t("errorMessage")}
  </Alert>
)}
```

```json
{
  "alerts": {
    "successTitle": "Success!",
    "successMessage": "Your changes have been saved.",
    "errorTitle": "Error!",
    "errorMessage": "Failed to save changes. Please try again."
  }
}
```

---

### 19. Error Messages

**Pattern:** Handle different error types.

**Before:**
```tsx
{error === "network" && <p>Network error. Please check your connection.</p>}
{error === "auth" && <p>Authentication failed. Please log in again.</p>}
{error === "not_found" && <p>The requested resource was not found.</p>}
{error === "permission" && <p>You don't have permission to access this.</p>}
```

**After:**
```tsx
const { t } = useTranslation("errors")

{error === "network" && <p>{t("network")}</p>}
{error === "auth" && <p>{t("auth")}</p>}
{error === "not_found" && <p>{t("notFound")}</p>}
{error === "permission" && <p>{t("permission")}</p>}
```

```json
{
  "errors": {
    "network": "Network error. Please check your connection.",
    "auth": "Authentication failed. Please log in again.",
    "notFound": "The requested resource was not found.",
    "permission": "You don't have permission to access this."
  }
}
```

---

### 20. Tooltip and Help Text

**Before:**
```tsx
<Tooltip content="Click to edit your profile picture">
  <img src="avatar.png" alt="Avatar" />
</Tooltip>

<span className="help-text">
  This setting controls who can see your profile.
</span>
```

**After:**
```tsx
const { t } = useTranslation("help")

<Tooltip content={t("editAvatarTooltip")}>
  <img src="avatar.png" alt={t("avatar")} />
</Tooltip>

<span className="help-text">
  {t("profileVisibilityHelp")}
</span>
```

```json
{
  "help": {
    "editAvatarTooltip": "Click to edit your profile picture",
    "avatar": "Avatar",
    "profileVisibilityHelp": "This setting controls who can see your profile."
  }
}
```

---

## Common Mistakes

### ❌ Mistake 1: Not translating attributes

**Wrong:**
```tsx
<input placeholder="Enter email" /> {/* Hardcoded */}
```

**Correct:**
```tsx
<input placeholder={t("emailPlaceholder")} />
```

---

### ❌ Mistake 2: Concatenating translations

**Wrong:**
```tsx
<p>{t("welcome")}, {userName}!</p>
```

```json
{
  "welcome": "Welcome"
}
```

**Correct:**
```tsx
<p>{t("welcome", { userName })}</p>
```

```json
{
  "welcome": "Welcome, {{userName}}!"
}
```

---

### ❌ Mistake 3: Forgetting ARIA labels

**Wrong:**
```tsx
<button aria-label="Close dialog">×</button>
```

**Correct:**
```tsx
<button aria-label={t("closeDialog")}>×</button>
```

---

### ❌ Mistake 4: Translating technical terms

**Wrong:**
```json
{
  "api": "应用程序接口" /* Don't translate API */
}
```

**Correct:**
```json
{
  "api": "API"
}
```

---

### ❌ Mistake 5: Inconsistent key naming

**Wrong:**
```json
{
  "submit": "Submit",
  "SubmitButton": "Submit",
  "btn-submit": "Submit"
}
```

**Correct:**
```json
{
  "submitButton": "Submit"
}
```

---

### ❌ Mistake 6: Not organizing by namespace

**Wrong:**
```json
{
  "save": "Save",
  "email": "Email",
  "title": "Settings",
  "delete": "Delete",
  "loading": "Loading"
}
```

**Correct:**
```json
{
  "common": {
    "save": "Save",
    "delete": "Delete",
    "loading": "Loading"
  },
  "settings": {
    "title": "Settings"
  },
  "form": {
    "email": "Email"
  }
}
```

---

## Real-World Examples

### Example 1: Complete Chat Component

**Before:**
```tsx
export const ChatView = () => {
  return (
    <div className="chat">
      <header>
        <h1>Chat</h1>
        <button>New Conversation</button>
      </header>

      <div className="messages">
        {messages.length === 0 && (
          <div className="empty">
            <p>No messages yet</p>
            <p>Start a conversation!</p>
          </div>
        )}
        {messages.map(msg => (
          <div key={msg.id} className={msg.sentByUser ? "user" : "assistant"}>
            <span className="sender">{msg.sender}</span>
            <p>{msg.text}</p>
            <span className="timestamp">{formatTime(msg.timestamp)}</span>
          </div>
        ))}
      </div>

      <div className="input-area">
        <input
          placeholder="Type a message..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
        />
        <button onClick={handleSend}>Send</button>
      </div>

      {isLoading && <p>Sending message...</p>}
      {error && <p className="error">Failed to send message</p>}
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
      <header>
        <h1>{t("title")}</h1>
        <button>{t("newConversation")}</button>
      </header>

      <div className="messages">
        {messages.length === 0 && (
          <div className="empty">
            <p>{t("empty.noMessages")}</p>
            <p>{t("empty.startConversation")}</p>
          </div>
        )}
        {messages.map(msg => (
          <div key={msg.id} className={msg.sentByUser ? "user" : "assistant"}>
            <span className="sender">{msg.sender}</span>
            <p>{msg.text}</p>
            <span className="timestamp">{formatTime(msg.timestamp)}</span>
          </div>
        ))}
      </div>

      <div className="input-area">
        <input
          placeholder={t("inputPlaceholder")}
          value={input}
          onChange={(e) => setInput(e.target.value)}
        />
        <button onClick={handleSend}>{t("sendButton")}</button>
      </div>

      {isLoading && <p>{t("sending")}</p>}
      {error && <p className="error">{t("sendError")}</p>}
    </div>
  )
}
```

**Translation files:**
```json
{
  "chat": {
    "title": "Chat",
    "newConversation": "New Conversation",
    "empty": {
      "noMessages": "No messages yet",
      "startConversation": "Start a conversation!"
    },
    "inputPlaceholder": "Type a message...",
    "sendButton": "Send",
    "sending": "Sending message...",
    "sendError": "Failed to send message"
  }
}
```

---

### Example 2: Complete Settings Page

**Before:**
```tsx
export const SettingsView = () => {
  return (
    <div className="settings">
      <h1>Settings</h1>

      <section>
        <h2>General</h2>
        <label>
          <input type="checkbox" checked={darkMode} onChange={toggleDarkMode} />
          Dark mode
        </label>
        <label>
          <input type="checkbox" checked={notifications} onChange={toggleNotifications} />
          Enable notifications
        </label>
      </section>

      <section>
        <h2>Language</h2>
        <p>Select your preferred language</p>
        <select value={language} onChange={handleLanguageChange}>
          <option value="en">English</option>
          <option value="zh">中文</option>
        </select>
      </section>

      <section>
        <h2>Account</h2>
        <button>Change Password</button>
        <button>Log Out</button>
      </section>

      <div className="actions">
        <button onClick={handleSave}>Save Changes</button>
        <button onClick={handleCancel}>Cancel</button>
      </div>
    </div>
  )
}
```

**After:**
```tsx
import { useTranslation } from "react-i18next"

export const SettingsView = () => {
  const { t } = useTranslation("settings")
  const { t: tCommon } = useTranslation("common")

  return (
    <div className="settings">
      <h1>{t("title")}</h1>

      <section>
        <h2>{t("general.title")}</h2>
        <label>
          <input type="checkbox" checked={darkMode} onChange={toggleDarkMode} />
          {t("general.darkMode")}
        </label>
        <label>
          <input type="checkbox" checked={notifications} onChange={toggleNotifications} />
          {t("general.notifications")}
        </label>
      </section>

      <section>
        <h2>{t("language.title")}</h2>
        <p>{t("language.description")}</p>
        <select value={language} onChange={handleLanguageChange}>
          <option value="en">{t("language.english")}</option>
          <option value="zh">{t("language.chinese")}</option>
        </select>
      </section>

      <section>
        <h2>{t("account.title")}</h2>
        <button>{t("account.changePassword")}</button>
        <button>{t("account.logOut")}</button>
      </section>

      <div className="actions">
        <button onClick={handleSave}>{tCommon("save")}</button>
        <button onClick={handleCancel}>{tCommon("cancel")}</button>
      </div>
    </div>
  )
}
```

**Translation files:**
```json
{
  "settings": {
    "title": "Settings",
    "general": {
      "title": "General",
      "darkMode": "Dark mode",
      "notifications": "Enable notifications"
    },
    "language": {
      "title": "Language",
      "description": "Select your preferred language",
      "english": "English",
      "chinese": "中文"
    },
    "account": {
      "title": "Account",
      "changePassword": "Change Password",
      "logOut": "Log Out"
    }
  },
  "common": {
    "save": "Save Changes",
    "cancel": "Cancel"
  }
}
```

---

**End of Patterns**
