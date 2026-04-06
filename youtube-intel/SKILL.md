---
name: youtube-intel
description: YouTube内容情报与竞品监测。当用户需要分析YouTube频道、追踪竞品动态、发现内容机会时触发。功能：1) Monitoring - 监测指定频道的更新频率、内容方向、数据表现；2) Discovery - 输入类目/关键词，扫描市场机会与竞争程度。用于选题策划、竞品分析、内容策略制定。
---

# youtube-intel · YouTube内容情报

## 核心功能

### Monitoring模式（竞品监测）

**触发词**：
- "帮我盯着XXX频道"
- "监测这几个频道"
- "这个频道最近发了什么"

**输出**：
```
频道：XXX
最近更新：X期节目
平均播放量：X
更新频率：X期/周
内容方向：XXX
最近爆款：XXX（X万播放）
趋势：上升/平稳/下降
```

---

### Discovery模式（选题发现）

**触发词**：
- "我想做XX类目，有没有机会"
- "帮我扫描XX市场"
- "这个关键词竞争大吗"

**输出**：
```
类目：XXX
市场热度：🔥/📉/📊（上升/下降/平稳）
搜索结果数：X
头部集中度：高/中/低（前三名吃掉XX%流量）
竞争格局：
  - 频道A：XX万订阅，内容方向XXX，平均X万播放
  - 频道B：XX万订阅，内容方向XXX，平均X万播放
切入机会：
  - 差异化角度：XXX
  - 建议标签：XXX
  - 建议标题方向：XXX
风险：
  - XXX
数据可信度：高中低（有X个频道数据来自直接抓取）
```

---

## 数据源（优先级排序）

### Primary（首选，真实可信）
1. **YouTube搜索** - `browser`工具，搜索关键词，解析视频列表
2. **YouTube频道页** - `browser`工具，直接访问频道页面抓数据

### Secondary（备选）
3. **Social Blade** - `web_fetch`抓频道数据（socialblade.com/youtube/user/XXX）
4. **YouTube Data API** - 如果有API key可用

### 搜索被拦截时的备选流程
```
web_search/web_fetch 失败
↓
使用 browser 工具，profile="openclaw"，action="open" 打开YouTube搜索页
↓
action="snapshot" 获取页面内容
↓
解析标题、播放量、频道名、发布时间
```

---

## 数据抓取流程

### Discovery完整流程
1. 用 `browser` 打开 YouTube 搜索页
2. 解析搜索结果，提取：视频标题、频道名、播放量、发布时间
3. 对每个发现的相关频道，用 `browser` 访问频道页获取更多信息
4. 综合所有数据，生成市场竞争报告

### Monitoring完整流程
1. 接收频道URL或名称
2. 从memory读取历史数据（如果存在）
3. 用 `browser` 访问频道页面获取最新数据
4. 对比历史数据，输出差异变化
5. 更新memory频道档案

---

## 数据解析规则

YouTube搜索结果解析（from snapshot）：
```
- 标题：heading 或 link 的 text
- 频道名：从 "前往频道：XXX" 或 "@XXX" 提取
- 播放量：从 "X万次观看" 或 "X次观看" 提取
- 发布时间：从 "X个月前" / "X天前" / "X年前" 提取
- 视频URL：从 link href 提取（/watch?v=XXX）
```

---

## 数据模型（统一）

```yaml
channel:
  name: string
  url: string          # YouTube频道URL
  handle: string       # @xxx格式
  subscribers: number  # 订阅数（估算）
  avg_views: number   # 平均播放量（估算）

video:
  title: string
  url: string         # /watch?v=XXX
  views: number        # 播放量
  published_days_ago: number  # 发布时间（天）
  channel: string

market_analysis:
  keyword: string
  search_date: date
  total_results: number  # 搜索结果总数
  top_channels[]:
    - name: string
      subscriber_count: string
      avg_views: number
      video_count_in_results: number
  data_source: string   # "browser|youtube_api|social_blade"
  data_confidence: "high" | "medium" | "low"
  notes: string
```

---

## 注意事项

- **搜索结果只显示前20-30个**，不代表完整市场
- **播放量为近似值**，YouTube有时模糊化显示（"1万次观看"）
- **数据置信度标注**：来自直接抓取=高，来自估算=中，来自历史数据=低
- Social Blade有速率限制，单次请求间隔≥5秒
- browser工具有速率限制，每次操作间隔≥2秒

---

## 频道档案存储（Memory）

每个监测频道在memory中存储：
```
memory/channels/{channel-handle}.md
```

档案包含：
- 最后更新时间
- 最新视频列表
- 关键数据指标
- 趋势分析

---

## 输出目的地（Output Destinations）

默认输出到当前对话。如需输出到其他平台，使用以下指令：

### 输出到飞书文档

**触发词**：
- "输出到飞书"
- "生成飞书文档"
- "写到飞书"

**操作**：
1. 使用 `feishu_doc` 工具创建文档
2. 文档标题格式：`ContentIntel_报告_{类型}_{日期}`
3. 内容格式：Markdown，结构化报告

**文档结构**：
```
# ContentIntel 报告

## 基本信息
- 报告类型：Discovery / Monitoring
- 生成时间：YYYY-MM-DD HH:mm
- 数据来源：YouTube直接抓取

## 核心发现
...

## 详细数据
...

## 建议/结论
...
```

### 输出到 Notion

**触发词**：
- "输出到Notion"
- "生成Notion页面"
- "写到Notion"

**操作**：
1. 使用 Notion API 创建页面（需要配置 Notion Integration Token）
2. 页面标题：`ContentIntel_{类型}_{日期}`
3. 内容块：标题 + 表格 + 文本

**页面结构**：
- 数据库模式（推荐）：建立 ContentIntel Reports 数据库
  - 属性：报告类型、关键词/频道、日期、置信度
  - 页面内容：报告正文

**Notion配置（参考 references/notion-integration.md）**

---

## Bundled Resources

详细数据模型定义：See [references/data-model.md](references/data-model.md)

工作流操作手册：See [references/workflow.md](references/workflow.md)

飞书/Notion输出集成：See [references/output-integrations.md](references/output-integrations.md)

Discovery报告模板与真实案例：See [references/discovery-template.md](references/discovery-template.md)
