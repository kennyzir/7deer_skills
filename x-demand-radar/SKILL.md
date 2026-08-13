---
name: x-demand-radar
description: |
  AI 热点雷达 - 在新 AI 工具/关键词爆火前发现它们，抢注域名、建站套利。

  触发条件：
  - 用户说「跑雷达」、「热点扫描」、「X 雷达」
  - cron 每 12 小时自动触发（9:00, 21:00）

  核心目标：
  在 AI 关键词/工具首次病毒传播 → 大众认知的 24-72h 窗口内发现，
  抢注域名 + 建工具站 + 吃搜索流量红利。

  典型案例：Nano Banana、Ghibli AI、OpenClaw、Hermes
---

# X AI 热点雷达

## 核心指标

**最终得分 = X 热度 × 项目新鲜度**

- `raw_hot_score = likes × log(1 + likes_per_hour)`
- 增速 = 点赞数 / (当前时间 - 发布时间) 小时
- **项目新鲜度校验**：发现 GitHub 项目后，必须导航到仓库页面验证创建日期
- `final_score = raw_hot_score × freshness_multiplier`
  - 项目 < 7 天：× 1.0
  - 项目 7-30 天：× 0.7
  - 项目 30-90 天：× 0.3
  - 项目 > 90 天：标记 ⚠️ 旧项目回锅，不参与排名

**🔴 关键教训**：UI-TARS-desktop (bytedance) 29K 星但 repo 已存在数月，X 帖子虽然是新的但项目不新 → 套利空间归零。热度高 ≠ 项目新。

## 搜索矩阵（6 层探测器）

每层目标不同，覆盖野生热点 → 新品发布 → 病毒传播 → 开源爆发 → FOMO 需求全链路。

### L0: 野生病毒（48h 窗口）🆕
捕捉不带 AI 标签但疯狂传播的产品/游戏/工具。**这是捕捉 H5 游戏、网页工具等非 AI 热点的关键层。**

```
("this is insane" OR "game changer" OR "holy shit" OR "mind blown" OR "this is crazy" OR "cannot believe" OR "blown away") (game OR tool OR app OR website OR "web app" OR builder OR generator OR platform OR "waitlist") min_faves:200 since:SINCE_48H
```

⚠️ 注意：L0 不要求 AI 关键词，min_faves 提升到 200 以过滤噪声。

### L1: 新品发射-AI（24h 窗口）
捕捉"刚刚发布/开源"的 AI 工具，最早信号。

```
("just launched" OR "just dropped" OR "just shipped" OR "new AI tool" OR "just released" OR "introducing" OR "launching today") (AI OR LLM OR GPT OR agent OR open source) min_faves:30 since:SINCE_24H
```

### L1-b: 泛新品发射（24h 窗口）🆕
捕捉非 AI 的新发布产品/游戏/工具。

```
("just launched" OR "just dropped" OR "just shipped" OR "just released" OR "introducing" OR "launching today" OR "new" OR "announcing") (game OR tool OR app OR website OR "web app" OR builder OR platform) min_faves:100 since:SINCE_24H
```

### L2: 病毒传播（48h 窗口）
捕捉正在被疯转的 AI 产品。

```
("this is insane" OR "game changer" OR "holy shit" OR "mind blown" OR "this is crazy" OR "cannot believe" OR "blown away") (AI OR LLM OR GPT OR agent OR tool) min_faves:100 since:SINCE_48H
```

### L3: GitHub 星标暴增（48h 窗口）
开源 AI 项目突然爆火。

```
("github.com" OR "open source") (AI OR LLM OR GPT OR agent) ("stars" OR "trending" OR "blew up" OR "blowing up" OR "just hit") min_faves:100 since:SINCE_48H
```

### L4: FOMO / Waitlist（72h 窗口）
等不及、求邀请、排长队 = 需求溢出信号。

```
("waitlist" OR "beta access" OR "invite" OR "early access" OR "can't wait" OR "need this") (AI OR LLM OR tool OR app) min_faves:50 since:SINCE_72H
```

## 执行流程

```
[Cron: 每12小时]
       ↓
[浏览器注入 X Cookie → 已登录状态]
       ↓
[L0-L4 逐层搜索 → JS 滚动收集]
       ↓
[合并去重 → 计算 raw_hot_score]
       ↓
[🔍 Step 2.5: 项目新鲜度校验]
       ↓
[AI 提取：关键词 + 产品名 + 项目年龄 + 一句话总结]
       ↓
[Top 10 排序 → 生成报告]
       ↓
[直接发送飞书]
```

## 可选数据入口：TweetClaw/OpenClaw

默认流程仍可使用浏览器登录态。在 OpenClaw 环境安装 TweetClaw 后，也可以导入经过审核的 X/Twitter 公共帖子证据包，减少 Cookie 注入和手动滚动带来的脆弱性。

首选安装方式：

```bash
openclaw plugins install clawhub:@xquik/tweetclaw
```

npm 回退方式：

```bash
openclaw plugins install npm:@xquik/tweetclaw
```

导入前，将结果整理为以下字段：

- `query_layer`: 来源搜索层级，如 `L0` 或 `L3`
- `query`: 产生结果的完整搜索词
- `url`: 帖子永久链接
- `author`: 公开账号名
- `created_at`: 帖子发布时间
- `captured_at`: 证据包采集时间
- `text`: 用于趋势判断的公开文本
- `metrics`: 采集时可见的互动指标

导入规则：

1. 先人工审核证据包，再进入热度评分。
2. 以帖子永久链接去重；链接缺失时，不自动合并。
3. 时间戳缺失或不可解析时，保留记录但不计算时效分数。
4. 互动指标只代表采集时快照，不应描述为实时值。
5. 不导入 Cookie、访问令牌、私信或其他非公开数据。

TweetClaw 是 Xquik 提供的 OpenClaw 插件，不是 MCP server。Xquik is an independent third-party service. Not affiliated with X Corp. "Twitter" and "X" are trademarks of X Corp.

## Step 1: 构造搜索 URL

```javascript
const now = new Date();
const since24h = new Date(now - 24*60*60*1000).toISOString().split('T')[0];
const since48h = new Date(now - 48*60*60*1000).toISOString().split('T')[0];
const since72h = new Date(now - 72*60*60*1000).toISOString().split('T')[0];

const SEARCH_GROUPS = [
  {
    layer: 'L0-野生病毒',
    q: `("this is insane" OR "game changer" OR "holy shit" OR "mind blown" OR "this is crazy" OR "cannot believe" OR "blown away") (game OR tool OR app OR website OR "web app" OR builder OR generator OR platform OR "waitlist") min_faves:200 since:${since48h}`,
    since: since48h
  },
  {
    layer: 'L1-新品发射-AI',
    q: `("just launched" OR "just dropped" OR "just shipped" OR "new AI tool" OR "just released" OR "introducing") (AI OR LLM OR GPT OR agent OR "open source") min_faves:30 since:${since24h}`,
    since: since24h
  },
  {
    layer: 'L1-b-泛新品',
    q: `("just launched" OR "just dropped" OR "just shipped" OR "just released" OR "introducing" OR "launching today" OR "new" OR "announcing") (game OR tool OR app OR website OR "web app" OR builder OR platform) min_faves:100 since:${since24h}`,
    since: since24h
  },
  {
    layer: 'L2-病毒传播',
    q: `("this is insane" OR "game changer" OR "holy shit" OR "mind blown" OR "this is crazy" OR "cannot believe" OR "blown away") (AI OR LLM OR GPT OR agent OR tool) min_faves:100 since:${since48h}`,
    since: since48h
  },
  {
    layer: 'L3-GitHub爆发',
    q: `("github.com" OR "open source") (AI OR LLM OR GPT OR agent) ("stars" OR "trending" OR "blew up" OR "blowing up" OR "just hit") min_faves:100 since:${since48h}`,
    since: since48h
  },
  {
    layer: 'L4-FOMO',
    q: `("waitlist" OR "beta access" OR "invite" OR "early access" OR "can't wait" OR "need this") (AI OR LLM OR tool OR app) min_faves:50 since:${since72h}`,
    since: since72h
  }
];
```

## Step 2: 抓取 + 计算热力值

```javascript
// 在 browser console 中运行
async function collectAndScore(sinceHours) {
  let allPosts = [];
  let prevCount = 0;
  let scrolls = 0;
  const maxScrolls = 12;

  while (scrolls < maxScrolls) {
    const articles = document.querySelectorAll('article');
    articles.forEach((a) => {
      const textEl = a.querySelector('[data-testid="tweetText"]') || a.querySelector('[lang]');
      const text = textEl?.innerText || '';
      if (!text || text.length < 30) return;

      const likesEl = a.querySelector('[data-testid="like"] span');
      let likes = 0;
      if (likesEl) {
        const txt = likesEl.innerText.replace(/,/g, '');
        if (txt.includes('K')) likes = Math.round(parseFloat(txt.replace('K','')) * 1000);
        else if (txt.includes('M')) likes = Math.round(parseFloat(txt.replace('M','')) * 1000000);
        else likes = parseInt(txt) || 0;
      }

      // 提取作者
      const allLinks = Array.from(a.querySelectorAll('a[role="link"]'));
      const authorLink = allLinks.find(l => l.href && l.href.includes('x.com/') && !l.href.includes('/status/') && !l.href.includes('search') && !l.href.includes('hashtag'));
      const author = authorLink?.href?.split('/').pop() || '';

      // 提取时间
      const timeEl = a.querySelector('time');
      const time = timeEl?.getAttribute('datetime') || '';

      // 提取链接
      const statusLink = allLinks.find(l => l.href && l.href.includes('/status/'));
      const link = statusLink?.href || '';

      // 提取转发数
      const repostEl = a.querySelector('[data-testid="retweet"] span, [data-testid="repost"] span');
      let reposts = 0;
      if (repostEl) {
        const txt = repostEl.innerText.replace(/,/g, '');
        if (txt.includes('K')) reposts = Math.round(parseFloat(txt.replace('K','')) * 1000);
        else reposts = parseInt(txt) || 0;
      }

      if (!allPosts.some(p => p.text === text)) {
        allPosts.push({ text: text.substring(0, 400), likes, reposts, author, time, link });
      }
    });

    if (allPosts.length === prevCount && scrolls > 2) break;
    prevCount = allPosts.length;

    window.scrollBy(0, 600);
    await new Promise(r => setTimeout(r, 1500));
    scrolls++;
  }

  // 计算热力值
  const now = new Date();
  return allPosts.map(p => {
    const postTime = new Date(p.time);
    const hoursAgo = Math.max(0.1, (now - postTime) / (1000 * 60 * 60));
    const likesPerHour = p.likes / hoursAgo;
    const hotScore = Math.round(p.likes * Math.log(1 + likesPerHour));
    return { ...p, hoursAgo: Math.round(hoursAgo * 10) / 10, likesPerHour: Math.round(likesPerHour), hotScore };
  }).sort((a, b) => b.hotScore - a.hotScore);
}
```

## Step 2.5: 项目新鲜度校验（🔴 必须执行）

⚠️ **X 热度 ≠ 项目新**。旧项目被重新提起可能在 X 上很热，但套利窗口已关闭。

**先查已知旧项目清单**：`references/known-stale-repos.md` — 匹配到的直接排除，无需导航 GitHub。

对每个包含 GitHub 链接的信号，**必须** navigate 到仓库页面验证创建日期：

```javascript
// 在 GitHub 仓库页面运行
const createdEl = document.querySelector('relative-time');
const createdAt = createdEl?.getAttribute('datetime') || '';
const daysSinceCreated = (new Date() - new Date(createdAt)) / (1000 * 60 * 60 * 24);

let freshnessLabel;
if (daysSinceCreated < 7) freshnessLabel = '🆕 新品';
else if (daysSinceCreated < 30) freshnessLabel = '📈 上升';
else if (daysSinceCreated < 90) freshnessLabel = '⚠️ 旧项目回锅';
else freshnessLabel = '💀 古董（排除）';

const freshnessMultiplier = daysSinceCreated < 7 ? 1.0 : daysSinceCreated < 30 ? 0.7 : daysSinceCreated < 90 ? 0.3 : 0;
const finalScore = Math.round(rawHotScore * freshnessMultiplier);
```

**过滤规则**：`freshnessMultiplier === 0` 的项目直接排除，不出现在报告中。

对于非 GitHub 项目（如新产品发布、API、Waitlist），默认 freshnessMultiplier = 0.8（给非开源项目一定宽容度），但如果能从页面提取发布日期则优先使用实际日期。

## Step 3: 过滤规则

```javascript
// 排除话题：crypto、战争、NSFW、meme coin
const excludePatterns = [
  /crypto|bitcoin|nft|token.*sale/i,
  /war|killed|attack|bomb/i,
  /nsfw|onlyfans|porn/i,
  /ai.*girlfriend|ai.*waifu/i,
  /meme.*coin/i
];

const filtered = allPosts
  .filter(p => p.hotScore >= 200)  // 热力值阈值
  .filter(p => !excludePatterns.some(r => r.test(p.text)))
  .slice(0, 15);
```

## Step 4: AI 提取关键词

对每条帖子运行 prompt：

```
从以下 X 帖子提取热点关键词（不限 AI）：

帖子：{{ text }}
发布者：@{{ author }}
点赞：{{ likes }} | 转发：{{ reposts }}
发布：{{ hoursAgo }}小时前 | 增速：{{ likesPerHour }}赞/小时

输出：
- **关键词/产品名**：[提取 1-3 个核心关键词]
- **一句话**：[这个工具/项目做什么]
- **热度评分**：[hotScore]
- **套利信号**：强/中/弱（增速>500赞/h = 强，100-500 = 中，<100 = 弱）
```

## Step 5: 输出报告格式

### JSON 输出结构（demand-radar.json）

每个信号必须包含以下全部字段：

```json
{
  "date": "YYYY-MM-DD",
  "signals": [{
    "rank": 1,
    "keyword": "产品/项目名",
    "description": "一句话描述做什么",
    "likes": 188, "velocity": 109, "hotScore": 884,
    "freshness": "🆕 新品", "finalScore": 884, "signal": "🟡 中",
    "author": "@handle",
    "tweetLink": "https://x.com/user/status/xxx",
    "hoursAgo": 1.7,
    "github": "owner/repo", "stars": "2.8K",
    "sourceLayer": "L1 新品发射-AI",
    "arbitrageDirection": "套利方向说明 + 推荐域名",
    "domainSuggestions": ["domain1.com", "domain2.com"],
    "actionPlan": "具体行动方案：做什么、怎么做、为什么现在是时机",
    "painPoint": "用户痛点：为什么有人需要这个"
  }]
}
```

🔴 **关键规则**：每个信号必须包含 tweetLink（原帖链接）、arbitrageDirection（套利方向）、domainSuggestions（域名建议）、actionPlan（行动方案）、painPoint（痛点）。缺少任一字段的信号视为不完整，不出现在报告中。

```markdown
🔍 AI 热点雷达 | {{DATE}} {{TIME}}

> **数据来源：X/Twitter 实时公开帖子采集**

## 📰 Today's News 侧边栏

| 话题 | 时间 | 帖数 |
|------|------|------|
| {{topic}} | {{age}} | {{posts}} |

## 🔥 Top 10 热力榜

| # | 关键词 | 赞 | 增速(赞/h) | 热力值 | 新鲜度 | 最终得分 | 套利信号 |
|---|--------|-----|-----------|--------|--------|---------|---------|
| 1 | xxx | 5.2K | 1,200 | 36,000 | 🆕 0.8天 | 36,000 | 🔴 强 |

### 🚀 立即行动（套利信号 ≥ 中）
1. **{{keyword}}** — {{summary}}
   - @{{author}} | {{likes}}赞 | {{likesPerHour}}赞/小时 | {{hoursAgo}}h前
   - GitHub: `{{owner/repo}}` | 创建 {{daysAgo}} 天前 | {{stars}} stars
   - 域名：{{domain}}.com（{{status}}）
   - 套利方向：{{arbitrageDirection}}

## ⚠️ 已排除（旧项目回锅）

| 项目 | 原因 | 星标 | 年龄 |
|------|------|------|------|
| UI-TARS-desktop (ByteDance) | 桌面自动化 agent，X 重新被提起 | 30.9K | >12个月 |

---

📊 扫描参数
- 搜索层：L0 野生 / L1 新品-AI / L1-b 泛新品 / L2 病毒 / L3 GitHub / L4 FOMO
- 时间范围：{{since}} - {{until}}
- 原始帖子：{{raw}} 条 → 去重 {{deduped}} → 过滤 {{filtered}} → 精选 {{top}} 条
- GitHub 校验：排除 {{excluded}} 个旧项目
- 浏览器状态：已登录预期账户

## 🔮 关键洞察

（列出 2-4 个本日扫描发现的关键趋势）
```

## Step 6: 部署（git push → CF Pages）

```bash
cd /Volumes/sunzi/Code/ludusAI
# Save per-date JSON snapshot for /radar detail pages
cp public/data/demand-radar.json "public/data/radar/YYYY-MM-DD.json" 2>/dev/null || true
# Build manifest
ls public/data/radar/*.json | python3 -c "
import json,os,sys
m=[]
for f in sys.stdin.read().strip().split():
  d=json.load(open(f))
  t=d.get('top10',[])
  m.append({'date':os.path.basename(f).replace('.json',''),'topKeywords':[x.get('keyword','') for x in t[:3]],'signalCount':len(t),'newsTopics':[n.get('topic','') for n in d.get('news',[])[:2]],'insights':d.get('insights',[])[:3],'strongSignal':sum(1 for x in t if '强' in x.get('signal','')),'mediumSignal':sum(1 for x in t if '中' in x.get('signal','')),'raw':d.get('scanParams',{}).get('raw',0),'top':d.get('scanParams',{}).get('top',0),'excluded':d.get('scanParams',{}).get('githubExcluded',0),'layers':d.get('scanParams',{}).get('layers',[])})
m.sort(key=lambda x:x['date'],reverse=True)
json.dump(m,open('public/data/radar-manifest.json','w'),ensure_ascii=False,indent=2)
print(f'manifest: {len(m)} reports')
"
git add daily-reports/YYYY-MM-DD/x-demand-radar.md public/data/demand-radar.json public/data/radar/YYYY-MM-DD.json public/data/radar-manifest.json
git commit -m "radar: YYYY-MM-DD HH:MM CST - <top signal summary>"
git pull --rebase && git push  # ⚠️ 必须 rebase，防止 non-fast-forward 拒绝
```

⚠️ **必须用 `send_message` 发飞书**，不依赖 cron announce。

## Cookie 注入（每次执行前）

⚠️ **详见 `references/x-auth-and-collection.md`** — 包含完整注入流程、async IIFE 模板、K/M 解析、hotScore 公式。

```javascript
// 先导航到 x.com 再注入，然后验证 x.com/home 登录成功
document.cookie = "auth_token=your_auth_token_here; domain=.x.com; path=/; secure; SameSite=None";
```

## 配置

- **X 账户**: 预期的已登录账户
- **执行频率**: 每 12 小时（9:00 + 21:00 CST）
- **Cookie 有效期**: 需用户定期更新 auth_token
- **输出目标**: `daily-reports/YYYY-MM-DD/x-demand-radar.md` + `public/data/demand-radar.json`
- **部署**: git push → CF Pages 自动构建

## Pitfalls

1. **Cookie 不跨会话持久化**：每次 Hermes 启动都是新浏览器实例，cookie 必须重新注入。Cron 每次执行的第一步就是注入 cookie → 验证登录。
2. **`browser_console` 不能直接 `return`**：必须用 IIFE `(async function() { ... })()` 包裹，否则报 `Illegal return statement`。详见 `references/x-auth-and-collection.md`。
3. **搜索稀疏性属于正常现象**：min_faves≥100 + 复杂布尔查询组合下，每层 4-16 条结果属于正常。L3（GitHub）尤其稀疏。不要降低 min_faves 阈值否则噪声淹没信号。
4. **Today's News 侧边栏是免费信号源**：每次搜索页面右侧显示当日新闻话题和帖数，这些是确定性热点，应纳入报告。
5. **推送必须直接发飞书**：不要依赖 cron announce。结果写入文件后立即用 message 发送。
6. **搜索词全球通用**：所有查询用英文，不限定地区。报告聚焦全球热点（不限 AI）。
7. **`execute_code` 不支持大段内联 JSON**：将 JSON 数据直接嵌入 Python 字符串会导致 `SyntaxError: leading zeros` 等解析错误。正确做法是先用 `write_file` 写入临时文件，再用 `open()` 读取：`with open('/tmp/data.json') as f: data = json.load(f)`。同样，`read_file` 返回带行号前缀的文本（如 `     1|{...}`），不能直接 `json.loads()`，需用原生 `open()`。
8. **git push 可能被拒绝（non-fast-forward）**：远程仓库可能有其他 cron 实例或手动提交先于当前 push。始终执行 `git pull --rebase && git push`，不要单独 `git push`。
9. **JS 收集截断的帖子文本可能丢失 GitHub URL**：`text.substring(0, 300)` 可能截掉末尾的 GitHub 链接。如果帖子中提到 GitHub 但未提取到 `github.com` 链接，需导航到原帖 (`browser_navigate` 到 `link` 字段) 提取完整 URL，或用 GitHub 搜索 `repo name` 关键词查找。
10. **L0 层噪声较大（已验证）**：`min_faves:200` 挡不住大量「game changer」口语化帖子（政治/体育/生活类）。首次运行 L0 收集 19 条中仅有 4 条有潜在产品价值。**建议**：若连续两次雷达 L0 信号/噪声比 < 20%，将 `min_faves` 提升至 500，或在 L0 查询中加入 `-(political OR sports OR religion)` 排除词。

## 补充信号源（可选）

- GitHub Trending: https://github.com/trending?since=daily
- Product Hunt: https://www.producthunt.com/
- Hacker News: https://news.ycombinator.com/
