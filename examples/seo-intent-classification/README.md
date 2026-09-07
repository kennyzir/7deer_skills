# 快速示例：搜索意图分类

这个离线示例调用 `google-trends-to-pages/resources/intent_classifier.py` 的真实 API。从仓库根目录运行：

```bash
python3 examples/seo-intent-classification/example.py
```

`classify_intent(keyword)` 直接返回 Title Case 字符串：`Transactional`、`Informational`、`Navigational` 或 `Commercial`，不是字典。

`analyze_keyword(keyword, search_volume, growth_rate)` 返回字典，包含：

- `keyword`
- `intent`
- `template`
- `priority`
- `priority_score`
- `suggested_word_count`
- `schema_type`

示例会断言 `analyze_keyword()` 的 `intent` 与 `classify_intent()` 一致，并以 JSON 输出关键词、意图、优先级和 Schema 类型。它不访问网络。
