# 快速示例：搜索意图分类

这个示例展示如何用 `google-trends-to-pages` 技能对关键词进行搜索意图分类。

## 示例关键词

```
how to get six eyes jujutsu infinite     → informational / guide / HowTo
yba codes april 2026                     → navigational / codes_page / FAQPage
best stands in yba tier list             → commercial / tier_list / ItemList
jujutsu infinite trading value list      → informational / data_table / Dataset
```

## 使用方式

将关键词传入 `intent_classifier.py`：

```python
import sys
sys.path.insert(0, '../../google-trends-to-pages/resources')
from intent_classifier import classify_intent

keywords = [
    "how to get six eyes jujutsu infinite",
    "yba codes april 2026",
    "best stands in yba tier list",
    "jujutsu infinite trading value list",
]

for kw in keywords:
    result = classify_intent(kw)
    print(f"{kw}")
    print(f"  → type: {result['type']}, template: {result['template']}, schema: {result['schema']}")
    print()
```

## 输出说明

| 字段 | 含义 |
|------|------|
| type | 搜索意图类型（informational / navigational / commercial / transactional） |
| template | 推荐页面模板 |
| schema | 推荐 Schema.org 结构化数据类型 |
