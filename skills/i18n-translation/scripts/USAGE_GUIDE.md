# i18n File Detection Workflow Guide

## 🎯 核心思路

**问题：** Claude 在国际化过程中需要反复搜索文件，浪费时间

**解决：** 先用脚本快速识别所有需要国际化的文件，生成清单供 Claude 直接使用

---

## 📋 工作流程

### Step 1: 快速扫描识别文件

```bash
python scripts/find-i18n-files.py src --format json --output i18n_files.json
```

**输出示例：**
```json
{
  "metadata": {
    "scan_time": "2024-01-15 10:30:00",
    "statistics": {
      "total_files_scanned": 500,
      "files_needing_i18n": 127,
      "total_strings_found": 3456,
      "average_strings_per_file": 27.2
    }
  },
  "files": [
    {
      "path": "/path/to/file.tsx",
      "relative_path": "src/components/Header.tsx",
      "size_bytes": 4567,
      "string_count": 45,
      "needs_i18n": true,
      "indicators": {
        "buttons": 5,
        "labels": 3,
        "placeholders": 2,
        "attributes": 8,
        "string_literals": 27
      }
    },
    // ... more files
  ]
}
```

### Step 2: Claude 读取文件清单

Claude 现在可以：
1. 读取 `i18n_files.json`
2. 按优先级处理文件（字符串数量从多到少）
3. 精确知道需要修改哪些文件
4. 避免反复搜索

### Step 3: Claude 执行国际化

Claude 根据 `i18n_files.json` 中的文件列表，逐个处理：
```python
# Claude 的处理流程
for file in sorted_files_by_priority:
    extract_strings(file)
    translate_strings()
    modify_source_code(file)
```

---

## 🚀 使用场景

### 场景 1: 大型项目首次国际化

```bash
# 1. 快速扫描（2-5秒）
python scripts/find-i18n-files.py src --output i18n_files.json

# 输出：[OK] Scan Complete (in 3.45s)
#      Found 127 files needing i18n with 3456 total strings

# 2. 告诉 Claude
# "请读取 i18n_files.json，按照优先级处理这些文件的国际化"

# 3. Claude 精确处理，无需搜索
```

### 场景 2: 增量更新国际化

```bash
# 1. 扫描变更的文件
python scripts/find-i18n-files.py src --min-strings 10 --output i18n_updates.json

# 2. 只处理新增或修改的文件
# "Claude，处理 i18n_updates.json 中的文件"
```

### 场景 3: 评估工作量

```bash
# 生成统计报告
python scripts/find-i18n-files.py src --format text --output i18n_report.txt

# 输出可读的工作量评估
```

---

## 📊 输出格式选择

### JSON 格式（推荐 Claude 使用）

```bash
python scripts/find-i18n-files.py src --format json --output i18n_files.json
```

**优点：**
- ✅ Claude 易于解析
- ✅ 包含完整元数据
- ✅ 支持优先级排序
- ✅ 可与其他脚本集成

**使用方式：**
```markdown
# 在对话中告诉 Claude
"请读取 i18n_files.json，按照 string_count 降序处理这些文件的国际化"

# Claude 会：
1. 读取 JSON 文件
2. 按优先级排序
3. 逐个处理文件
4. 追踪进度
```

### CSV 格式（适合人工审查）

```bash
python scripts/find-i18n-files.py src --format csv --output i18n_files.csv
```

**优点：**
- ✅ Excel 可打开
- ✅ 适合人工审查
- ✅ 可以添加备注
- ✅ 生成统计报告

**适用场景：**
- 项目经理审查
- 人工确认优先级
- 工作量评估
- 进度追踪

### Text 格式（适合快速查看）

```bash
python scripts/find-i18n-files.py src --format text --output i18n_report.txt
```

**优点：**
- ✅ 人类可读
- ✅ Markdown 格式
- ✅ 包含统计摘要
- ✅ 适合文档记录

---

## 🔧 高级选项

### 最小字符串阈值

```bash
# 只处理包含 10+ 字符串的文件
python scripts/find-i18n-files.py src --min-strings 10 --output priority_files.json
```

**用途：**
- 优先处理重要文件
- 过滤掉只含少量字符串的文件
- 分阶段国际化

### 自定义文件类型

```bash
# 只扫描 Vue 组件
python scripts/find-i18n-files.py src --file-types vue --output vue_files.json

# 扫描特定类型
python scripts/find-i18n-files.py src --file-types tsx,jsx --output react_files.json
```

### 排除特定目录

```bash
# 排除测试和示例文件
python scripts/find-i18n-files.py src --exclude "node_modules,dist,build,__tests__,examples"
```

### 并行处理控制

```bash
# 使用更多工作进程加速
python scripts/find-i18n-files.py src --workers 16 --output i18n_files.json
```

---

## 💡 Claude 使用示例

### 示例 1: 完整工作流

```markdown
用户:
"使用 i18n-translation skill 国际化这个项目"

Claude:
"我来帮您国际化。首先让我读取文件清单..."
[读取 i18n_files.json]
"找到 127 个需要国际化的文件，共 3456 个字符串。
我将按优先级处理（字符串数量从多到少）：

1. src/components/Header.tsx (45 strings) - 处理中
2. src/views/Dashboard.tsx (38 strings) - 处理中
3. ..."
```

### 示例 2: 增量更新

```markdown
用户:
"新添加了 5 个组件，需要国际化"

Claude:
"让我先扫描新增的文件..."
[运行 find-i18n-files.py]
"检测到 5 个新文件需要处理：
1. src/components/NewFeature.tsx (23 strings)
2. ..."
```

### 示例 3: 分阶段处理

```markdown
用户:
"先国际化前 20 个最重要的文件"

Claude:
[读取 i18n_files.json]
"好的，我将处理字符串数量最多的前 20 个文件：
1. src/components/Header.tsx (45 strings)
...
20. src/utils/helpers.tsx (15 strings)

完成后将继续处理剩余的 107 个文件。"
```

---

## 📈 性能对比

### 传统方式（无文件清单）

```
Claude 处理流程：
1. Grep 搜索所有 .tsx 文件: 10s
2. 逐个打开检查: 30s
3. 重复搜索字符串: 20s
总计: 60s 搜索时间 + 实际处理时间
```

### 新方式（使用文件清单）

```
Claude 处理流程：
1. 读取 i18n_files.json: 1s
2. 直接处理文件: 无需搜索
总计: 1s 准备时间 + 实际处理时间

节省: 59s 搜索时间！
```

---

## 🎯 最佳实践

### 1. 项目初始化时

```bash
# 生成初始文件清单
python scripts/find-i18n-files.py src --output i18n_files.json

# 提交到版本控制
git add i18n_files.json
git commit -m "Add i18n file detection results"
```

### 2. 定期更新清单

```bash
# 每周或每次大更新后
python scripts/find-i18n-files.py src --output i18n_files.json
```

### 3. 工作量评估

```bash
# 生成可读报告
python scripts/find-i18n-files.py src --format text --output i18n_report.txt

# 查看统计
cat i18n_report.txt
```

### 4. 团队协作

```bash
# 生成 CSV 分配任务
python scripts/find-i18n-files.py src --format csv --output i18n_tasks.csv

# 在 Excel 中分配给团队成员
# 添加"负责人"、"状态"、"完成日期"等列
```

---

## 🔍 与其他脚本配合

### 完整工作流

```bash
# Step 1: 找出需要国际化的文件
python scripts/find-i18n-files.py src --output i18n_files.json

# Step 2: 提取字符串（可选，Claude 会自动做）
python scripts/extract-strings-fast.py src --format json --output all_strings.json

# Step 3: 验证完成情况
python scripts/validate-i18n.py locales en zh-Hans
```

---

## ✅ 检查清单

使用前确认：
- [ ] Python 3.7+ 已安装
- [ ] 源代码目录存在
- [ ] 有足够的磁盘空间保存输出文件

使用后检查：
- [ ] 输出文件已生成
- [ ] 文件数量符合预期
- [ ] 可以被 Claude 正确读取

---

## 🎉 总结

**核心价值：**
- ✅ 避免反复搜索文件
- ✅ 明确工作范围
- ✅ 可量化工作量
- ✅ 提升处理效率

**推荐使用方式：**
1. 项目开始时运行一次
2. 生成 `i18n_files.json`
3. 告诉 Claude 读取并按优先级处理
4. 定期更新文件清单

**预期效果：**
- Claude 工作效率提升 50%+
- 避免遗漏文件
- 进度可追踪
- 工作量可评估
