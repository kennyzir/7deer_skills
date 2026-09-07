---
name: itchio-new-game-hunt
description: Hunt for fresh browser-playable games on itch.io /newest that are worth building SEO arbitrage sites for. Crawls new releases, scores them by signals, produces ranked shortlist.
metadata:
  category: software-development
  triggers:
    - "itch.io 新游发现"
    - "找 itch 游戏套利"
    - "itch new game hunt"
    - "发现值得建站的 itch 游戏"
    - "itchio SEO 套利"
    - "scan itch.io for games"
---

# itch.io New Game Hunt → SEO Arbitrage Discovery

## 核心理念

itch.io 新游套利的黄金窗口：游戏刚上线 → Google 索引不完整 → 搜索竞争低 → 第一时间建站截获流量。本 skill 专注**发现环节**：从 itch.io 新游列表中筛选出「有 SEO 套利价值」的游戏。

## 筛选漏斗（4 层）

```
itch.io /newest (36/page)
    ↓ 第 1 层: Play in browser
~20 games
    ↓ 第 2 层: 详情页信号扫描 + 评分
~5-8 games
    ↓ 第 2.5 层: Google Trends 搜索需求验证
~3-5 games（砍掉搜不到的）
    ↓ 第 3 层: 竞品度评估
1-3 高价值候选
```

---

## Phase 1：列表页批量发现

### 目标 URL

```
https://itch.io/games/newest/platform-web/free
```
> 注意：itch.io 有 Cloudflare 安全验证。如果被拦截，回退到 `/games/newest` 然后靠 CSS 选择器过滤 "Play in browser"。

### 提取方法

在 `/games/newest` 页面的浏览器 console 执行：

```js
(() => {
  const cells = document.querySelectorAll('.game_cell');
  return [...cells].map(cell => {
    const titleEl = cell.querySelector('.title, .game_title');
    const title = titleEl ? titleEl.textContent.trim() : '';
    const link = cell.querySelector('a[data-action="game_grid"], a.thumb_link');
    const url = link ? link.getAttribute('href') : '';
    const dataText = cell.querySelector('.game_cell_data')?.textContent || '';
    const hasPlayInBrowser = /Play in browser/i.test(dataText);
    const genreEl = cell.querySelector('.game_genre');
    const genre = genreEl ? genreEl.textContent.trim() : '';
    const authorEl = cell.querySelector('.game_author a');
    const author = authorEl ? authorEl.textContent.trim() : '';
    const imgEl = cell.querySelector('img');
    const thumbUrl = imgEl ? (imgEl.src || imgEl.getAttribute('data-lazy_src') || '') : '';
    return { title, url, author, genre, thumbUrl, hasPlayInBrowser };
  }).filter(g => g.hasPlayInBrowser && g.title);
})()
```

**关键过滤：**
- ✅ `hasPlayInBrowser === true` → 才能建站内嵌
- ❌ 游戏名为空 → 跳过
- ❌ 标题含 `[WIP]`/`[Demo]`/`[Prototype]` → 未完成品，跳过
- ⚠️ 标题是非英语（如纯中文/阿拉伯语）→ 英语搜索流量有限，标注 `NON_EN`

**输出：** 第一轮筛选列表（通常 15-22 个/页）

---

## Phase 2：详情页信号扫描（逐个）

对 Phase 1 的每个候选游戏，进入详情页提取信号。

### 重要：避免每次点击 Embed 按钮

Embed 按钮触发 modal dialog，太低效。改用以下方式：

#### 方法 A：直接拼接 embed URL（推荐）

itch.io game_id 在页面 HTML 中有多处出现：
```js
// 在详情页 console 提取 game_id
const embedLink = document.querySelector('a[href*="/embed/"]');
const dataGameId = document.body.getAttribute('data-game_id');
const pageScripts = [...document.querySelectorAll('script')]
  .find(s => s.textContent.includes('"id":'))?.textContent;
const idMatch = pageScripts?.match(/"id":(\d+)/);
const gameId = dataGameId || (embedLink?.href?.match(/\/embed\/(\d+)/)?.[1]) || (idMatch?.[1]);
// embed URL = `https://itch.io/embed/${gameId}`
```

#### 方法 B：如果方法 A 失败，点 Embed modal

```js
// 点 Embed 按钮 → 读取 textarea
document.querySelector('textarea')?.value  // 提取 iframe 中的 src
```

### 详情页信号提取清单

```js
// 在详情页 console 执行完整提取
(() => {
  const r = {};

  // === 基础信息 ===
  r.title = document.querySelector('h1')?.textContent?.trim() || 
            document.querySelector('.game_title')?.textContent?.trim() || '';
  r.url = window.location.href;
  
  // === Embed URL ===
  const dataGameId = document.body?.getAttribute('data-game_id') || 
                     document.querySelector('[data-game_id]')?.getAttribute('data-game_id');
  const embedLink = document.querySelector('a[href*="/embed/"]');
  const embedHref = embedLink?.getAttribute('href') || '';
  r.gameId = dataGameId || (embedHref.match(/\/embed\/(\d+)/)?.[1]) || '';
  r.embedUrl = r.gameId ? `https://itch.io/embed/${r.gameId}` : '';
  
  // === 描述 ===
  const descEl = document.querySelector('.formatted_description, .game_description, [class*="description"]');
  r.description = descEl ? descEl.textContent.trim().substring(0, 2000) : '';
  
  // === 标签/分类 ===
  r.tags = [...document.querySelectorAll('a[href*="/tag-"]')]
    .map(a => a.textContent.trim().toLowerCase());
  r.genres = [...document.querySelectorAll('a[href*="/genre-"]')]
    .map(a => a.textContent.trim());
  
  // === 评分 ===
  const ratingEl = document.querySelector('.star_rating, [itemprop="ratingValue"], [class*="aggregate"]');
  const ratingText = ratingEl?.textContent?.trim() || ratingEl?.getAttribute('content') || '';
  r.rating = parseFloat(ratingText) || 0;
  r.ratingCount = 0;
  const countEl = document.querySelector('[itemprop="ratingCount"], [class*="rating_count"]');
  if (countEl) r.ratingCount = parseInt(countEl.textContent) || 0;
  
  // === 下载/浏览/评论数 ===
  const statEls = document.querySelectorAll('.game_info_panel_widget .stat, .stats .stat, [class*="stat"]');
  statEls.forEach(el => {
    const text = el.textContent;
    if (/view/i.test(text)) r.views = parseInt(text.replace(/\D/g,'')) || 0;
    if (/download/i.test(text)) r.downloads = parseInt(text.replace(/\D/g,'')) || 0;
    if (/comment/i.test(text)) r.comments = parseInt(text.replace(/\D/g,'')) || 0;
  });
  
  // === 发布/更新时间 ===
  const dateEl = document.querySelector('.game_date, time, [class*="published"], [class*="updated"]');
  r.publishDate = dateEl ? dateEl.textContent.trim() : '';
  
  // === 开发者 ===
  const authorEl = document.querySelector('.game_author a, [class*="author"] a, [class*="owner"] a');
  r.author = authorEl ? authorEl.textContent.trim() : '';
  r.authorUrl = authorEl ? authorEl.getAttribute('href') : '';
  
  // === Devlog 数 ===
  const devlogEls = document.querySelectorAll('.devlog_list .devlog_post, [class*="devlog"] li');
  r.devlogCount = devlogEls.length;
  
  // === 平台支持 ===
  r.platforms = [...document.querySelectorAll('.platform_img, [class*="platform"] img')]
    .map(p => p.getAttribute('title') || p.getAttribute('alt') || '')
    .filter(Boolean);
  
  // === 是否免费 ===
  const priceEl = document.querySelector('.game_price, .price_tag, [class*="price"]');
  r.price = priceEl ? priceEl.textContent.trim() : 'Free';
  r.isFree = !priceEl || /free|name your|donation/i.test(r.price);
  
  // === og:image ===
  const ogImg = document.querySelector('meta[property="og:image"]');
  r.ogImage = ogImg ? ogImg.getAttribute('content') : '';
  
  return r;
})()
```

### 信号评分模型（Phase 2 详情页，满分 80）

> Phase 2 只打 80 分基础分。Phase 2.5 的 Google Trends 验证追加 0-35 分趋势分，总分上限 100。

| 信号 | 提取字段 | 权重 | 评分规则 |
|------|---------|:---:|------|
| **可嵌入性** | `embedUrl` | 🔴 硬性门槛 | 无 embedUrl → **直接淘汰** |
| **游戏类型匹配** | `tags`, `genres` | 20 | 含 `html5` + `action`/`puzzle`/`arcade`/`shooter`/`simulation` → +20；Visual Novel/Interactive Fiction → +5（搜索意图低） |
| **社交证明** | `rating`, `ratingCount`, `comments`, `downloads` | 20 | rating≥4 → +10；ratingCount≥10 → +5；comments≥3 → +5 |
| **活跃度** | `devlogCount`, `publishDate` | 15 | devlog≥2 → +8；7天内更新 → +7 |
| **开发者信誉** | `author` (多款作品?) | 10 | 开发者有 ≥3 款作品 → +10 |
| **标题搜索友好度** | `title` 文本分析 | 10 | 标题含明确搜索关键词 → +10；纯品牌名/造词 → +3 |
| **语言** | `title`, `description` | 5 | 英语 → +5；多语言 → +3；纯非英语 → +1 |

**Phase 2 评分分级：**
- 🟢 ≥ 50 分 → 进入 Phase 2.5 趋势验证
- 🟡 30-49 分 → 可观测，等信号增强
- 🔴 < 30 分 → 跳过

**Phase 2.5 趋势分追加：**
- Google Trends 验证通过 → +0 到 +35 → 总分重算
- 最终 ≥ 60 分 → 进入 Phase 3 竞品评估

---

## Phase 2.5：Google Trends 搜索需求验证

> ⚠️ **关键漏斗层**：Phase 2 的「搜索量潜力」评分只是基于标题关键词的**推断**。Phase 2.5 用真实趋势数据**验证**推断是否成立。
> **工具限制：** terminal 环境的 pytrends 无法连接 Google（被墙），必须通过 **browser 工具**访问 Google Trends 页面 + JS 提取数据。

### 执行时机

对 **Phase 2 评分 ≥ 30 分** 的候选逐个查询趋势。

### 查询方式：批量对比

Google Trends 支持一次 URL 比较最多 5 个搜索词。建议**每批 3-4 个游戏名 + 1 个锚定词**：

```
锚定词选择：
- 高搜索量：  "snake game"（日均~20-30）→ 作为「有需求」的参照线
- 中等搜索量："escape room game" → 作为「中等需求」参照
- 零搜索量：  留空让新游戏自然暴露
```

**URL 构造：**
```
https://trends.google.com/trends/explore?q={keyword1},{keyword2},{keyword3},{anchor}&date=now%207-d&geo=US
```
- `date=now%207-d` → 过去 7 天（看到实时趋势）
- `geo=US` → 美国市场（英语搜索主力）
- 关键词中空格用 `%20` 编码

### 数据提取 JS

在 Google Trends 页面加载后，用 `browser_console` 执行：

```js
(() => {
  // 1. 平均搜索兴趣值
  const avgRow = [...document.querySelectorAll('tr')].find(tr => {
    const td = tr.querySelector('td');
    return td && td.textContent.trim() === 'Average';
  });
  const averages = avgRow 
    ? [...avgRow.querySelectorAll('td')].slice(1).map(td => td.textContent.trim())
    : [];

  // 2. 时间序列（第二个 table）
  const tables = document.querySelectorAll('table');
  const dataTable = tables.length > 1 ? tables[1] : null;
  const timeSeries = dataTable
    ? [...dataTable.querySelectorAll('tr')].slice(1).map(row => {
        const cells = [...row.querySelectorAll('td')];
        if (cells.length < 2) return null;
        return {
          time: cells[0]?.textContent?.trim(),
          values: cells.slice(1).map(c => c.textContent.trim())
        };
      }).filter(Boolean)
    : [];
  
  // 3. 非零数据点统计
  const nonZeroPts = timeSeries.filter(ts => ts.values.some(v => v !== '0'));
  
  // 4. 峰值
  const allVals = timeSeries.flatMap(ts => ts.values.map(Number).filter(n => !isNaN(n) && n > 0));
  const maxVal = allVals.length > 0 ? Math.max(...allVals) : 0;
  
  // 5. "Not enough data" 警告
  const warnings = [...document.querySelectorAll('[class*="warning"], .error-message, [class*="not_enough"]')]
    .map(el => el.textContent.trim())
    .filter(t => t.includes('enough data') || t.includes('spelled correctly'));

  // 6. 地区分布（第三个 table，如果有）
  const regionTable = tables.length > 2 ? tables[2] : null;
  const regions = regionTable
    ? [...regionTable.querySelectorAll('tr')].slice(1, 4).map(row => {
        const cells = [...row.querySelectorAll('td')];
        return cells.length > 1 
          ? { region: cells[0]?.textContent?.trim(), value: cells[1]?.textContent?.trim() } 
          : null;
      }).filter(Boolean)
    : [];
  
  return {
    averages,
    nonZeroPercent: timeSeries.length > 0 
      ? Math.round(nonZeroPts.length / timeSeries.length * 100) 
      : 0,
    maxValue: maxVal,
    hasData: nonZeroPts.length > 0,
    warnings: warnings.slice(0, 3),
    regions
  };
})()
```

### 趋势评分模型

| 趋势信号 | 评分逻辑 | 分数 |
|----------|---------|:---:|
| 平均搜索值 > 0 | 有需求被记录 | +15 |
| 平均搜索值 ≥ 锚定词的 50% | 需求可观 | +10 |
| 非零数据点 > 50% | 需求持续非偶然 | +10 |
| 峰值 ≥ 30（相对值） | 有搜索爆发潜力 | +10 |
| warnings 含 "not enough data" | 无搜索需求验证 → **-20（罚分）** | — |
| 平均值 = 0 且无 warning | 偶发搜索 → 保留但标记 | +0 |

**趋势分级：**
- 🟢 ≥ 20 分（从趋势获得）→ 搜索需求已验证，继续 Phase 3
- 🟡 5-19 分 → 低需求但非零，加入观测列表
- 🔴 < 5 分 → 搜索需求未验证，从候选列表移除

### 批处理策略（节省 browser 调用）

```
第 1 批：锚定词 "snake game" + 游戏1 + 游戏2
    → 拿到锚定线 + 两个游戏的相对值
第 2 批：锚定词 "snake game" + 游戏3 + 游戏4
    → 同锚定词保持可比性
...
```

> **关键逃逸条件：** 如果一批中的锚定词也返回 0（整个 Trends 页面数据异常）→ 标记此次扫描异常，不淘汰任何游戏，改天重扫。

---

## Phase 3：竞品度评估（对高价值候选）

对 **Phase 2 评分 ≥ 40 分** 的候选，评估 Google SERP 竞争情况：

### 快速检查（30 秒/游戏）

1. 基于游戏标题构造搜索词：`"{title} game"` 或 `"play {title} online"`
2. 打开 Google 搜索（可以用 `browser_navigate` 或 SerpAPI）
3. 检查首页前 10 结果：

| SERP 格局 | 评估 | 行动 |
|-----------|:---:|------|
| 0-2 个独立站 + itch.io 排第 1 | 🟢 窗口大开 | 立即建站 |
| 3-5 个中等站 | 🟡 竞争存在 | 差异化可行性评估 |
| 5+ 个强站 | 🔴 窗口关闭 | 跳过 |
| 0 个搜索结果 | ⚪ 无搜索需求 | 跳过（白费力气） |

### 中等站评估标准

```
- 标题是否精准匹配 "{GameName} Game Online"？
- H1 是否含 "play" + "free" 关键词？
- 是否有 FAQ section？
- 内容深度 ≥ 500 词？
- 是否有结构化数据 (VideoGame Schema)？
→ 如果现有站点在这 5 项中缺 ≥ 3 项 → 有超越空间
```

---

## Phase 4：最终推荐输出

生成结构化推荐报告：

```markdown
# 🎯 itch.io 新游套利发现报告
**日期：** 2026-XX-XX
**来源：** https://itch.io/games/newest
**扫描：** 36 个游戏 → 20 个 browser-playable → [N] 个高价值

## 🟢 高价值候选 (≥60分)

| # | 游戏名 | 评分 | 类型 | 搜索潜力 | 竞品度 | 推荐行动 |
|---|--------|:---:|------|:---:|:---:|------|
| 1 | {title} | {score} | {genre} | 🟢/🟡 | 🟢 | 立即建站 |
| 2 | ... |

## 🟡 观测列表 (40-59分)

| # | 游戏名 | 评分 | 类型 | 缺失信号 | 观测建议 |
|---|--------|:---:|------|------|------|
| 1 | {title} | {score} | {genre} | 评论/评分为0 | 1周后复查 |

## 🔴 已淘汰

- {title} — 原因: {淘汰理由}
```

---

## 自动化运行模式

### 模式 A：单次扫描（手动触发）
```
browser_navigate → /newest → 提取 Phase 1 列表（JS console）
→ 对每个 Play in browser 候选 → 详情页 → Phase 2 信号提取 + 评分
→ 对 ≥30 分候选 → 分批 Google Trends → Phase 2.5 趋势验证
→ 对 趋势通过 + ≥50 总分 → Google SERP → Phase 3 竞品评估
→ 输出 Phase 4 报告
```

### 模式 B：定时扫描（cron job）
```
每天 1 次 → itch.io /newest → Phase 1 → Phase 2 → Phase 2.5
→ 仅输出趋势通过候选 → 本地保存 JSON
```

---

## pitfall

1. **Cloudflare 拦截**：itch.io /newest/platform-web/free 容易触发 CF challenge。回退方案：用 `/games/newest` 基础页，靠 Play in browser 文本在 JS 中过滤
2. **视觉小说/互动小说陷阱**：genre=Visual Novel 的游戏搜索意图更偏 "read" 而非 "play"，建站转化率低 — 分数惩罚 -15
3. **非英语游戏**：标题/描述为葡萄牙语、西班牙语等的游戏 → 英语搜索流量极少。如果是特定语言市场可考虑，但通用套利价值低
4. **评分 0 ≠ 无价值**：刚上线 1 天的游戏评分/评论均为 0 是正常的。此时优先看游戏类型 + 标题关键词 + 开发者活跃度
5. **只做列表页评分会漏掉好游戏**：itch.io 列表页不显示评分/评论/downloads —**必须进详情页**
6. **不要用 "Play in browser" 筛选 URL 直接访问**：`/newest/platform-web/free` 更易触发 CF 验证；在基础 `/newest` 页用 JS 过滤更稳定
7. **Embed URL 不是 iframe src 直链**：itch.io embed 是 `<iframe src="https://itch.io/embed/{id}">`，这是完整游戏页面的嵌入形式，可以直接用
8. **搜索量 ≠ 可套利**：有些游戏名是品牌词（如 "Snake.DB"、"ATARI 2600"），虽然搜索量大但会被官网占满，套利价值 0
9. **Google Trends 访问路径**：terminal 的 pytrends 库无法连接 Google（被墙），**必须使用 browser 工具**访问 trends.google.com。browser 工具有独立网络通路，可正常访问
10. **Trends 数据 0 很常见**：新游戏刚上线几天，Google Trends 返回 0 是正常现象。不要仅凭 0 就淘汰 — 查看 Phase 2 其他信号（类型、标题友好度、开发者活跃度）做综合判断
11. **锚定词必须稳定**：每批 Trends 查询必须用同一个锚定词（如 "snake game"），否则不同批次的相对值不可比
12. **URL 编码陷阱**：游戏名含特殊字符（`☆`、`!`、`'`）时需 URL 编码。建议用 `encodeURIComponent()` 处理游戏名后再拼 URL
