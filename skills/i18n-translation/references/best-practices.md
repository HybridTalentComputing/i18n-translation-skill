# Translation Best Practices

This reference document provides detailed guidelines for ensuring high-quality translations that maintain fidelity to the source text.

## 🎯 Translation Fidelity Principles

### Core Principle: Faithful to Source

**ALL translations must be faithful to the source text:**

1. **No Additions** - Never add words not present in source
2. **No Deletions** - Never omit content from source
3. **No Changes** - Preserve exact meaning and tone
4. **No Improvements** - Don't "fix" or enhance the source

**Translation is not adaptation.** The goal is to convey the EXACT same message in a different language, not to improve or localize the content.

### Examples of Correct vs Incorrect Translation

#### Example 1: Simple Button Text

**Source:** "Save Changes"

❌ **Incorrect:**
- "保存" (Save - too simple, loses "Changes")
- "请保存您的更改" (Please save your changes - added "Please" and "your")
- "保存修改并关闭" (Save changes and close - added "and close")

✅ **Correct:**
- "保存更改" (Save changes - faithful to source)

#### Example 2: Error Message

**Source:** "Email is required"

❌ **Incorrect:**
- "请输入邮箱" (Please enter email - added "Please")
- "邮箱地址不能为空" (Email address cannot be empty - different wording)

✅ **Correct:**
- "邮箱为必填项" (Email is required - faithful)

#### Example 3: With Interpolation

**Source:** "Hello {{name}}, you have {{count}} new messages"

❌ **Incorrect:**
- "你好，你有新消息" (Missing placeholders)
- "欢迎 {{name}}，您收到了 {{count}} 条新消息！" (Added exclamation mark)
- "Hello {{name}}，you have {{count}} new messages" (Mixed languages)

✅ **Correct:**
- "你好 {{name}}，你有 {{count}} 条新消息" (Preserves placeholders exactly)

#### Example 4: Formal vs Informal

**Source:** "Please enter your password"

❌ **Incorrect (if source is formal):**
- "输入密码" (Enter password - too casual, missing "Please")

✅ **Correct:**
- "请输入您的密码" (Please enter your password - maintains formality)
- "请输入密码" (Acceptable if concise style is appropriate for context)

### Placeholder Preservation Rules

**CRITICAL:** All placeholders MUST be preserved exactly as they appear in the source.

#### Placeholder Types

1. **Double Curly Braces:** `{{variable}}`
   ```
   Source: "Hello {{name}}"
   ✅ Target: "你好 {{name}}"
   ❌ Target: "你好 {{name}}" (different spacing)
   ❌ Target: "你好{name}}" (missing braces)
   ```

2. **Single Curly Braces:** `{variable}`
   ```
   Source: "Hello {name}"
   ✅ Target: "你好 {name}"
   ```

3. **Percent Sign:** `%variable%`
   ```
   Source: "Hello %name%"
   ✅ Target: "你好 %name%"
   ```

4. **Dollar Sign:** `$variable`
   ```
   Source: "Hello $name"
   ✅ Target: "你好 $name"
   ```

5. **Positional:** `{0}`, `{1}`
   ```
   Source: "Hello {0}, you have {1} messages"
   ✅ Target: "你好 {0}，你有 {1} 条消息"
   ```

**Rule:** Detect the interpolation style from source and preserve it EXACTLY.

### HTML and Markdown Preservation

**Preserve all formatting tags:**

```
Source: "Click <a href='/help'>here</a> for **help**"
✅ Target: "点击<a href='/help'>此处</a>获取**帮助**"
❌ Target: "点击此处获取帮助" (removed HTML/Markdown)
```

### Tone and Style Preservation

**Match the source tone:**

| Source Tone | Example | Target Tone | Example |
|------------|---------|-------------|---------|
| Formal | "Please verify your email" | Formal | "请验证您的邮箱" |
| Casual | "Check your email" | Casual | "查看你的邮箱" |
| Technical | "Authentication failed" | Technical | "身份验证失败" |
| Friendly | "Welcome back!" | Friendly | "欢迎回来！" |

## Translation Quality Checklist

### Before Submitting Translation

For each translation key, verify:

- [ ] **No Added Words** - No words added that aren't in source
- [ ] **No Omitted Words** - All content from source is present
- [ ] **No Meaning Changes** - Exact same meaning as source
- [ ] **Placeholders Preserved** - All {{variables}}, {variables}, %variables% present
- [ ] **HTML Preserved** - All tags like <a>, <strong>, <br> present
- [ ] **Markdown Preserved** - All **bold**, *italic*, `code` present
- [ ] **Tone Matched** - Formal/casual/technical tone matches source
- [ ] **No Grammar Errors** - Target language grammar is correct
- [ ] **Natural Phrasing** - Sounds natural in target language (while being faithful)

### Common Pitfalls

#### Pitfall 1: Over-Translation

**Source:** "Log In"

❌ **Over-translated:**
- "登录系统" (Login to the system - added "to the system")
- "点击登录" (Click to login - added "Click to")

✅ **Correct:**
- "登录" (Login - faithful)

#### Pitfall 2: Under-Translation

**Source:** "I agree to the terms and conditions"

❌ **Under-translated:**
- "同意" (Agree - too simple, lost content)

✅ **Correct:**
- "我同意条款和条件" (I agree to terms and conditions)

#### Pitfall 3: Localization Instead of Translation

**Source:** "Football" (meaning American football)

❌ **Localized incorrectly:**
- "足球" (Soccer/association football - wrong sport)

✅ **Correct:**
- "橄榄球" (American football - faithful to source meaning)

**Note:** Only localize when the source meaning is intentionally generic. When source is specific, be specific.

#### Pitfall 4: Politeness Level Mismatch

**Source:** "Sign up" (casual, modern web app)

❌ **Too formal:**
- "注册账号" (Register account - too formal)

✅ **Correct:**
- "注册" or "加入" (Sign up or Join - matches casual tone)

#### Pitfall 5: Placeholder Corruption

**Source:** "{{count}} items selected"

❌ **Corrupted placeholders:**
- "{{count}} 项选中" (Wrong word order)
- "已选择 {{count}} 个项目" (Added words)

✅ **Correct:**
- "已选中 {{count}} 项" (Selected {{count}} items)

## Context-Aware Translation

### UI Context Matters

Consider WHERE the text appears:

#### Buttons
- Keep short (2-4 words if possible)
- Use verb-first structure
- Match button conventions in target language

**Examples:**
- "Save Changes" → "保存更改" (not "更改保存")
- "Cancel" → "取消" (standard)
- "Submit" → "提交" (standard)

#### Labels
- Include colon if source has it
- Match field type (text, email, password)

**Examples:**
- "Email:" → "邮箱："
- "Password:" → "密码："

#### Error Messages
- Be clear and direct
- Maintain urgency level
- Don't soften the message

**Examples:**
- "Invalid email" → "邮箱格式无效" (not "邮箱可能有问题" - too soft)
- "Required field" → "必填项" (not "这是必填的哦" - too casual)

#### Success Messages
- Match celebration level
- Don't over-embellish

**Examples:**
- "Saved successfully" → "保存成功" (not "恭喜您，保存成功啦" - too much)
- "Done!" → "完成！" (matches exclamation)

## Cultural Considerations

### What NOT to Change

Even when content seems culturally specific:

**Source:** "Black Friday Sale"

❌ **Incorrect:**
- "双11大促" (Changed to Chinese shopping festival)

✅ **Correct:**
- "黑色星期五大促" (Black Friday sale - faithful)

**Source:** "Last name"

❌ **Incorrect:**
- "姓名" (Name - doesn't match Western naming convention context)

✅ **Correct:**
- "姓氏" (Last name/Surname - faithful)

### When Adaptation IS Acceptable

Only when the source INTENTIONALLY allows flexibility:

**Source:** "Contact us" (generic)

✅ **Acceptable adaptations:**
- "联系我们" (Contact us - standard)
- "联系客服" (Contact customer service - context-specific)

But prefer the most faithful translation unless context requires otherwise.

## Number and Date Formats

### Preserve Format Semantics

**Numbers:**
```
Source: "1,234.56"
✅ Target: "1,234.56" (Keep same if target locale uses same format)
✅ Target: "1 234,56" (French format - if French target locale)
❌ Target: "一千二百三十四点五六" (Chinese characters - wrong format)
```

**Dates:**
```
Source: "January 15, 2024"
✅ Target: "2024年1月15日" (Chinese format)
✅ Target: "15 janvier 2024" (French format)
❌ Target: "2024/01/15" (Different format)
```

**Note:** Follow target locale conventions for date/number formatting.

## Validation Script Usage

Use `scripts/validate-i18n.py` to check:

```bash
python scripts/validate-i18n.py locales en zh-Hans

# Output:
# ✓ Key counts match: 156 keys in both en and zh-Hans
# ✓ All placeholders preserved
# ✅ Validation complete
```

## Quality Assurance Workflow

### 1. Self-Check During Translation

For each key:
1. Read source carefully
2. Identify all placeholders
3. Translate faithfully
4. Verify placeholders are present
5. Check tone matches

### 2. Automated Validation

After completing a file:
```bash
# Validate JSON/YAML syntax
jq . < locales/zh-Hans/common.json

# Compare key counts
jq -r 'keys[]' locales/en/common.json | sort > en_keys.txt
jq -r 'keys[]' locales/zh-Hans/common.json | sort > zh_keys.txt
diff en_keys.txt zh_keys.txt
```

### 3. Context Review

For critical UI text:
- Read surrounding context
- Check where text appears
- Verify translation fits the UI
- Test in application if possible

## Troubleshooting Quality Issues

### Issue: Translation feels unnatural

**Possible causes:**
- Too literal (word-for-word)
- Doesn't follow target language conventions
- Grammar is correct but phrasing is odd

**Solution:**
- Re-read source
- Identify the core message
- Express that same message naturally in target language
- Verify you haven't added/removed meaning

### Issue: Text doesn't fit UI

**Possible causes:**
- Target language is more verbose than source
- UI doesn't accommodate longer text

**Solutions:**
1. **Concise translation:** Find shorter way to say same thing
2. **Abbreviation:** Use standard abbreviations in target language
3. **UI adjustment:** (If fully automated mode) Report to user that UI expansion may be needed

**Example:**
- Source: "Email Address" (15 chars)
- Target: "电子邮箱地址" (6 chars) - actually shorter!
- But if target is longer: "邮箱" (Email) - acceptable abbreviation

### Issue: Multiple valid translations

**When there are multiple ways to translate:**

**Choose based on:**
1. **Context:** What fits the UI/ situation?
2. **Consistency:** What have you used for similar text?
3. **Convention:** What's standard in this type of app?
4. **Fidelity:** Which is most faithful to source?

**Example:**
- Source: "Settings"
- Options: "设置", "配置", "设定"
- Most common: "设置" (Choose this unless context suggests otherwise)

## Summary: The Golden Rules

1. **Faithfulness First** - Never add, remove, or change meaning
2. **Preserve Placeholders** - All variables must be present
3. **Match Tone** - Formal/casual/technical level must match
4. **Natural Phrasing** - Should sound natural in target language
5. **Context Awareness** - Consider WHERE and HOW text is used
6. **Validate Thoroughly** - Use scripts and manual checks
7. **100% Coverage** - Every key must be translated

**Remember:** A good translation is invisible - users don't notice it's a translation. A bad translation breaks immersion and trust.
