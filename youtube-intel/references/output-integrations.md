# youtube-intel 输出集成

## 飞书文档输出

### 触发条件
- 用户说 "输出到飞书" / "生成飞书文档" / "写到飞书"
- 报告内容较长（超过2000字）

### 操作步骤

1. **使用 `feishu_doc` 工具创建文档**
   ```typescript
   feishu_doc(
     action: "create",
     title: "youtube-intel_{类型}_{YYYYMMDD}",
     folder_token: "{optional folder token}"
   )
   ```

2. **写入报告内容**
   ```typescript
   feishu_doc(
     action: "write",
     doc_token: "{上一步创建的文档token}",
     content: "{Markdown格式报告}"
   )
   ```

### 飞书文档模板

```markdown
# youtube-intel {报告类型}报告

## 基本信息
- 报告类型：{Discovery / Monitoring}
- 生成时间：{YYYY-MM-DD HH:mm}
- 数据来源：{YouTube直接抓取 / Social Blade / 混合}
- 数据置信度：{高 / 中 / 低}

## 核心发现
{3-5个关键点}

## {Discovery: 市场分析 / Monitoring: 频道动态}

## 详细数据

## 建议/结论

---
由 youtube-intel Skill 自动生成
```

---

## Notion 输出

### 触发条件
- 用户说 "输出到Notion" / "生成Notion页面"

### 操作步骤

1. 确保 Notion Integration Token 已配置
2. 创建新页面或写入已有数据库

### Notion 页面结构

```
Parent: database_id or page_id
Properties:
  - Name: "youtube-intel_{类型}_{日期}"
  - 类型: Select {Discovery, Monitoring}
  - 关键词/频道: RichText
  - 日期: Date
  - 置信度: Select {High, Medium, Low}

Content Blocks:
  - 标题 Heading 1
  - 基本信息 BulletedList
  - 核心发现 Heading 2 + Paragraph
  - 数据表格 Table
  - 建议 Heading 2 + Paragraph
```

### Notion 配置（memory/notion-config.md）

```markdown
# Notion Integration 配置

## 需要配置
- notion_api_key: Secret token from Notion integration
- parent_page_id: 默认父页面（可选）

## 数据库字段要求
如果使用数据库模式，需要以下字段：
- Name (title)
- 报告类型 (select)
- 关键词/频道 (rich_text)
- 日期 (date)
- 置信度 (select)
```

---

## 输出优先级

默认顺序：
1. **对话直接输出** - 快速、简短报告
2. **飞书文档** - 详细报告、长期保存
3. **Notion** - 需要进一步编辑或与现有Notion工作流集成

用户可以通过指令覆盖默认行为。
