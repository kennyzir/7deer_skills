---
name: keyword-competition-analysis
description: 谷歌关键词竞争度分析。当用户要求分析某个关键词的搜索竞争度、SEO难度、关键词排名机会、市场调研，或要求"分析下XXX关键词"时触发。使用浏览器抓取Google搜索结果页作为主要数据源，输出结构化竞争度报告。
---

# Keyword Competition Analysis

基于 Google 搜索结果页的关键词竞争度分析技能。

## 工作流程

### Step 1：发起搜索

使用 `browser` 工具打开 Google 搜索结果页：

```
https://www.google.com/search?q=<URL编码的关键词>
```

### Step 2：获取快照

用 `browser snapshot compact=true` 抓取搜索结果页，识别：
- 广告数量和广告主
- 前10自然结果标题 + 域名
- 是否有精选摘要、视频结果、People Also Search For
- 结果类型分布（官方文档/社区/工具/视频/论坛）

### Step 3：二次验证（如需要）

打开1-2个典型结果页面，快速确认：
- 内容深度（页面字数/内容量级）
- 页面优化痕迹（标题、H标签、keywords标签）
- 域名大致权重感

### Step 4：输出报告

按以下结构输出，详见 [references/output-template.md](references/output-template.md)：

1. 基本信号评分表
2. 竞争者画像
3. 机会识别
4. 综合判断

## 评分维度说明

| 维度 | 评估重点 |
|------|---------|
| 广告主密度 | 多 = 商业价值高 = 竞争激烈 |
| 结果主体 | 高权重站（官方/维基/Quora）为主 = 壁垒高 |
| 内容深度 | 300字浅页面 vs 3000字+深度内容 |
| 精选摘要 | 有 = SEO空间被压缩 |
| 视频结果 | 有 = 视频布局已是红海 |
| 域名年龄感 | 全是老站 = 难；有机会站点出现 = 可切入 |

## 低竞争突破口识别

- 结果里有 PDF/PPT/论坛/Quora → 内容生态弱，机会
- 没有视频结果 → 视频是机会
- 工具/导航类结果多 → 内容站有机会
- Search Intent 混杂（教程+产品混排）→ 细分人群可切

## 长尾词发现

从 People Also Search For 区域提取高价值长尾方向：
- 资源导向（...GitHub, ...examples）
- 评测导向（Best ...，...vs...）
- 教程导向（how to ..., ...tutorial）

## 注意事项

- Google 搜索有反爬，优先用 `browser` 工具而非 `web_search`
- 不要依赖结果总数（谷歌已取消精确数字）
- 综合判断要带时效性提示（新市场窗口 vs 成熟红海）
