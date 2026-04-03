---
name: backlink-discovery
description: |
  外链机会发现引擎。用户输入目标网址，立即用 web_search 开始多轮关键词派生搜索，
  目标发现 300 个相关平台后自动停止，结果存入该网址专属数据库。
  不限外链方式（论坛/GitHub/Wiki/目录等），只发现不执行。
  触发：用户提供网址，说"发现外链"、"找外链机会"、"发现外链机会"。
---

# Backlink Discovery — 外链机会发现引擎

## 核心逻辑

**每个 URL = 独立发现任务，目标 300 个平台。**

```
用户输入 https://xxx.com
  → 立即用 web_search 开始前台搜索
  → 多轮关键词派生，持续发现
  → 达到 300 个平台后停止
  → 结果存入数据库

下次输入 https://yyy.com
  → 新的独立发现任务
  → 各自数据库，互不干扰
```

## 触发方式

```
发现 https://xxx.com 的外链机会（目标300个）
```

## 执行流程（前台 web_search）

### Step 1：接收任务，提取种子关键词

解析目标 URL，实时提取种子关键词（不写死）：

```
https://robloxcalc.com
  ↓
种子关键词：roblox, calculator, math, lua, game, game calculator, gaming, education, tool
```

### Step 2：多轮 web_search（前台执行）

每轮用 `web_search` 搜索 8-12 个查询，从结果提取平台域名 → 分类 → 判断相关度。

**搜索词思路要宽**，不要只搜"xxx alternatives"：
- 竞品 + "free tools list"
- 竞品 + "directory submit"
- 竞品 + "community"
- 竞品 + "tutorial resources"
- 竞品 + "wiki"
- 竞品 + "github awesome list"
- 竞品 + "for kids/math/education"
- 竞品 + "game dev"
- 竞品 + "fan sites blogs"
- 竞品 + "similar games"
- 竞品 + "submit free"

每轮结束后从发现结果中派生新关键词 → 进入下一轮。

停止条件：
- 达到 300 个平台 → 停止
- 连续 2 轮无新发现 → 停止

### Step 3：结果写入数据库

每个 URL 独立数据库目录：

```
memory/backlink-discovery/{提取的域名}/
├── platforms.json      # 所有发现平台（含相关度、方式分类）
└── summary.md         # 汇总报告
```

### Step 4：返回结果

发现完成后返回：
- 总平台数 + P0/P1/P2 分布
- 外链方式分布
- Top 10 高相关平台
- 数据存放路径

用户查询时读数据库返回最新状态。

## 数据库读取

```
查询 https://xxx.com 的外链发现结果
→ 读 memory/backlink-discovery/xxx_com/platforms.json
→ 返回 P0/P1/P2 分类 + 外链方式分布 + 完成状态
```

## 平台分类体系

| 分类 | 相关度 | 说明 |
|------|--------|------|
| 🔴 P0 | ≥0.7 | 主题高度相关，明显外链机会 |
| 🟡 P1 | 0.4-0.7 | 较相关，可尝试 |
| 🟢 P2 | <0.4 | 关联一般 |

## 外链方式分类

| 方式 | 适用平台 |
|------|---------|
| forum_post | Reddit、Discord、GameFAQs 等社区 |
| github_pr | GitHub Awesome Lists、资源列表 |
| wiki_edit | Wikipedia、Fandom Wiki |
| alternatives_article | Alternatives/对比文章站 |
| directory_submit | 目录站、产品提交页 |
| guest_post | Dev.to、Hashnode、技术博客 |
| email_outreach | 有联系邮箱的任意平台 |
| social_post | Twitter、LinkedIn |
| manual_review | 其他方式 |

## 输出格式

```
# {网站} 外链机会发现报告

## 发现状态
- 状态：已完成
- 平台库：X / 300 个
- 发现时间：时间

## 🔴 P0 高相关平台（X 个）
[表格]

## 🟡 P1 中相关平台（X 个）
[按类型分组列出]

## 🟢 P2 低相关平台（X 个）

## 📊 外链方式分布
- Forum 发帖：X 个
- GitHub PR：X 个
- Alternatives Outreach：X 个
- 目录提交：X 个
- 其他：X 个

## 🔄 下一步
建议执行 backlink-executor 处理 P0 平台
```

## 注意事项

- **前台执行** — 用 web_search 直接跑，不用 sessions_spawn（Playwright 会被搜索引擆拦截）
- **思路要宽** — 游戏、教育、工具、社区、博客、GitHub、Wiki 都是外链来源
- **不要笃定"到顶了"** — 相关平台数量往往比第一眼预估的多很多
- **每个 URL 独立任务** — 不同 URL 互不干扰
- **目标 300 个平台** — 达到后自动停止
- **只发现不执行** — 执行放 backlink-executor
- **长期积累** — 数据库不覆盖，持续追加
