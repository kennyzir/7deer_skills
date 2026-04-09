---
name: site-keyword-research
description: 整站关键词研究与挖掘。输入一个网站域名或URL，自动分析站点主题、生成关键词矩阵、研究搜索竞争度，最终输出完整的关键词策略报告。触发条件：用户说"分析网站关键词"、"关键词研究"、"keyword research"、"挖掘某网站的关键词"、或提供一个URL说"分析这个网站的SEO关键词机会"。
---

# Site Keyword Research Skill

输入一个网站域名，输出完整的关键词研究与竞争度分析报告。

## 输入解析

接受三种格式：
- `https://example.com` → 提取 domain
- `example.com` → 直接使用
- `www.example.com` → 提取 domain

```bash
echo "example.com" | sed 's|https\?://||' | cut -d'/' -f1
```

## 工作流程

### Step 1 — 站点主题分析

使用 `web_fetch` 抓取首页内容（maxChars: 3000），识别：
- 站点定位（产品/工具/内容/电商）
- 核心主题和垂直领域
- 目标用户群体
- 主要产品/服务描述

同时抓取 `/robots.txt` 和首页 HTML 标题/meta 描述辅助判断。

### Step 2 — 关键词种子词生成

基于站点主题，用浏览器 Google 搜索以下内容作为种子词来源：

1. **主题种子**：搜索 `[核心主题] related searches` 获取相关词
2. **竞品种子**：搜索 `[核心主题] alternatives` 或 `best [核心主题] tools`
3. **"people also search for"**：从 Google SERP 的 PASF 区域提取长尾词
4. **种子关键词扩展**：搜索 `[核心主题] + tool/platform/free/software` 变体

生成 15-25 个候选关键词，覆盖以下类型：

| 类型 | 意图 | 示例 |
|------|------|------|
| 产品词 | Transactional | [主题] + tool/generator/creator |
| 教程词 | Informational | how to [主题], [主题] guide |
| 问题词 | Informational | [主题] + tutorial, [主题] + questions |
| 比较词 | Commercial | best [主题], [主题] vs, [主题] alternatives |
| 免费词 | Transactional | free [主题], [主题] free |

### Step 3 — 关键词筛选与优先级

从候选词中选出 5-8 个最有价值的词进行详细 SERP 分析，选择标准：

**优先选：**
- 有明确搜索意图的词
- 竞品分析显示内容薄弱的词
- 包含免费/最佳/替代等高意图修饰词的词

**排除：**
- 过于宽泛的泛流量词（如只用 "marketing"）
- 与站点主题无关的词
- 纯品牌词（除非是竞品分析）

### Step 4 — SERP 竞争度分析（核心）

对每个入选关键词，调用浏览器分析流程：

```
https://www.google.com/search?q=<编码关键词>&hl=en
```

用 `browser snapshot compact=true` 抓取，识别：
- 广告主数量和密度
- 前10自然结果类型（工具/博客/目录/论坛）
- Featured Snippet 存在性
- 视频结果区
- "People Also Search For" 长尾推荐

按以下维度打分（1-5分，分低=竞争弱=机会大）：

| 维度 | 1分 | 3分 | 5分 |
|------|-----|-----|-----|
| 广告主 | 0个 | 3-5个 | 6个以上 |
| 高权重站比例 | 无 | 2-3个 | 5个以上 |
| Featured Snippet | 无 | 1个 | 多个 |
| 视频结果 | 无 | 1-2个 | 3个以上 |
| 内容深度信号 | 薄页为主 | 混合 | 深度内容主导 |

**总分 5-10 分 = 低竞争（机会大）**
**总分 11-17 分 = 中竞争（可切入）**
**总分 18-25 分 = 高竞争（红海）**

### Step 5 — 输出报告

按 `references/output-template.md` 的结构输出完整报告。

---

## 关键原则

- **严禁只分析单个词**：没有足够样本无法判断站点整体关键词策略
- **先确定主题再选词**：避免生成与站点无关的泛词
- **用浏览器而非 web_search**：Google SERP 数据是核心，DuckDuckGo 数据仅供参考辅助
- **给每个分析过的词打分**：方便用户横向比较优先级
- **PASF 词 = 免费洞察**：Google 推荐的 "People Also Search For" 是最具参考价值的用户真实需求映射，务必提取

---

## 错误处理

| 场景 | 处理 |
|------|------|
| web_fetch 403/404 | 跳过该 URL，用已知主题信息继续分析 |
| 站点是全新站（DA=0）| 在报告中标注"新站，竞品分析重点关注内容差距而非域名权重" |
| 关键词无搜索结果 | 从候选词中替换为其他长尾 |
| Google 反爬（弹出验证）| 改用 web_search 补充数据，并在报告中说明"该词数据来源于 DuckDuckGo" |

---

## 参考文件

- 完整报告模板：`references/output-template.md`
- 关键词竞争度分析框架（单页版）：`keyword-competition-analysis/SKILL.md`
