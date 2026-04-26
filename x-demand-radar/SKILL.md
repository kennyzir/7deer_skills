---
name: x-demand-radar
description: |
  AI 需求雷达 - 自动抓取 X/Twitter 上蕴含未满足需求的「特征帖」，分析后直接推送飞书。

  触发条件：
  - 用户说「跑需求雷达」、「启动需求监控」、「X 需求扫描」
  - 每天 cron 自动触发（早上 9:00）

  特征贴定义：
  - 包含痛点关键词："I wish" / "someone should build" / "why no" / "missing" / "need an AI" / "million dollar idea"
  - 带 AI 相关词："AI tool" / "AI app" / "AI website" / "AI product"
  - min_faves:30，-filter:replies
  - 时间：最近 30 天

  使用 browser 工具抓取 X 高级搜索结果，配合 AI 总结，直接发送飞书。
---

# X Demand Radar - AI 需求雷达

## 工作流程

```
[Cron: 每天 9:00 AM]
       ↓
[构造 4 组搜索词矩阵]
       ↓
[browser: 逐组打开 X 高级搜索]
       ↓
[JavaScript: 边滚动边收集所有已加载帖子]
       ↓
[合并去重 → 过滤 → Top 15 排序]
       ↓
[AI: 逐条分析 - 输出需求标题+痛点+MVP方案+评分]
       ↓
[message: 直接发送飞书]
```

## Step 1: 构造多组搜索词矩阵

**必须跑满 3 组不同的搜索词组合**，覆盖不同表达方式，避免遗漏：

```javascript
const SINCE_DATE = new Date();
SINCE_DATE.setDate(SINCE_DATE.getDate() - 30);
const SINCE_STR = SINCE_DATE.toISOString().split('T')[0];

// 搜索词矩阵 — 至少跑 3 组
const SEARCH_GROUPS = [
  {
    label: '组1: someone should build',
    q: '(AI tool OR AI app OR AI website OR AI product) ("someone should build" OR "should build a") min_faves:30 -filter:replies'
  },
  {
    label: '组2: I wish / missing',
    q: '(AI tool OR AI app OR AI website OR AI product) ("I wish" OR "I\'m missing" OR "missing a") min_faves:30 -filter:replies'
  },
  {
    label: '组3: why no / need an AI',
    q: '(AI tool OR AI app OR AI website OR AI product) ("why no one built" OR "need an AI" OR "million dollar idea") min_faves:30 -filter:replies'
  },
  {
    label: '组4: if only there was',
    q: '(AI tool OR AI app OR AI website OR AI product) ("if only there was" OR "wish there was" OR "there should be an") min_faves:30 -filter:replies'
  }
];

// 每组构造 URL
const url = `https://x.com/search?q=${encodeURIComponent(group.q + ' since:' + SINCE_STR)}&src=typed_query&f=live`;
```

**执行规则**：每组单独抓取、去重、合并后统一排序，最多取 Top 15。

## Step 2: 抓取页面 + JS 滚动收集

⚠️ **关键：X 搜索只渲染约9条帖子，滚动时是替换不是追加。需要用 JavaScript 边滚动边收集。**

```javascript
// 在 browser evaluate 中运行
async function collectAllPosts() {
  let allPosts = [];
  let prevCount = 0;
  let scrolls = 0;  // ✅ 修复：声明在函数作用域内
  const maxScrolls = 10;

  while (scrolls < maxScrolls) {
    // 提取当前页面的所有帖子
    const articles = document.querySelectorAll('article[aria-labelledby]');
    articles.forEach((a) => {
      const textEl = a.querySelector('[lang]');
      const text = textEl?.innerText || '';
      if (!text || text.length < 30) return;

      const likesEl = a.querySelector('[data-testid="like"] span');
      const likes = likesEl
        ? parseInt(likesEl.innerText.replace(/[,K]/g, '').replace('K', '000')) || 0
        : 0;

      const authorEl = a.querySelector('[data-testid="User-Name"] span a');
      const author = authorEl?.href?.split('/').pop() || '';

      const timeEl = a.querySelector('time');
      const time = timeEl?.getAttribute('datetime') || '';

      const link = authorEl?.href || '';

      // 去重
      if (!allPosts.some(p => p.text === text)) {
        allPosts.push({ text, likes, author, time, link });
      }
    });

    if (allPosts.length === prevCount && scrolls > 2) break; // 连续两次没新内容则停止
    prevCount = allPosts.length;

    window.scrollBy(0, 600);
    await new Promise(r => setTimeout(r, 1800));  // ✅ 加长等待时间确保渲染
    scrolls++;
  }

  return allPosts.sort((a, b) => b.likes - a.likes);
}
```

**执行规则**：每组搜索词单独跑一次 `collectAllPosts()`，结束后合并去重（以 text 字段去重），统一按点赞数排序后取 Top 15。

## Step 3: 合并 + 过滤规则

```javascript
const excludePatterns = [
  'already exists', 'already built', 'try it at',
  'check this out', 'here is the tool', 'i built this',
  'we built', 'launched:', 'show hn', 'github.com',
  'product hunt', 'beta.access'
];

const filtered = allPosts
  .filter(p => p.likes >= 30)
  .filter(p => p.text.length >= 80)
  .filter(p => !excludePatterns.some(w => p.text.toLowerCase().includes(w)))
  .slice(0, 10); // Top 10
```

## Step 4: AI 分析 Prompt

```
你是 AI 需求雷达分析师。从以下 X 帖子中提取：
- **需求标题**：一句话概括要做什么（英文，≤10词）
- **痛点描述**：为什么这个需求没被满足？供给低的原因？（1-2句）
- **MVP 想法**：独立开发者 7 天能完成的最小方案（1-2句）
- **优先级评分**：1-10（基于点赞数+需求普遍性+实现难度）
- **验证建议**：下一步如何验证这个需求？（1句）

发推者：@{{ author }}
正文：{{ text }}
点赞：{{ likes }}

输出格式（MD）：
## [需求标题]
**痛点**：{{ 痛点描述 }}
**MVP**：{{ MVP 方案 }}
**评分**：{{ }}/10
**验证**：{{ 下一步 }}
---
```

## Step 5: 发送结果

### Telegram 推送格式

```
🔍 AI Demand Radar | {{ DATE }}

{{ AI_SUMMARY_RESULTS }}

---
📊 扫描参数
关键词：AI tool/app/website/product + 痛点词
时间范围：{{ SINCE }} - {{ UNTIL }}
原始帖子：{{ COUNT }} 条
精选：{{ TOP_COUNT }} 条
推送时间：{{ NOW }}
```

### Notion 创建卡片

Database 字段：
- **Name**: 需求标题
- **Pain Point**: 痛点描述
- **MVP Idea**: MVP 方案
- **Score**: 评分
- **Source**: @作者 | 原始链接
- **Status**: Backlog

## Step 5（最后）: 直接发送飞书

⚠️ **必须在本 skill 执行完毕后立即用 `message` 工具发送飞书**，不要依赖 cron 的 announce 模式间接投递。

```javascript
// 分析完成后，立即发送飞书
await message({
  action: 'send',
  channel: 'feishu',
  target: 'user:open_id',  // 收件人的 open_id
  message: `🔍 AI Demand Radar | ${DATE}\n\n${AI_RESULTS}\n\n---\n📊 扫描参数\n搜索词组：${SEARCH_GROUPS.length} 组\n时间范围：${SINCE_STR} - ${UNTIL_STR}\n原始帖子：${TOTAL_COUNT} 条\n精选：${TOP_COUNT} 条\n推送时间：${NOW}`
});
```

**禁止**：在 skill 执行流程中出现「依赖 cron 发送」的情况。每次执行完毕后必须立刻通过 `message` 工具推送结果。

## Cron 配置

```javascript
{
  "name": "X Demand Radar 每日扫描",
  "schedule": { "kind": "cron", "expr": "0 9 * * *", "tz": "Asia/Shanghai" },
  "sessionTarget": "isolated",
  "payload": {
    "kind": "agentTurn",
    "message": "使用 x-demand-radar skill 执行每日需求扫描：\n\n1. 构造 4 组搜索词（见 SKILL.md Step 1）\n2. 对每组搜索词分别用 browser 打开 X 高级搜索并用 JS 滚动收集（见 SKILL.md Step 2）\n3. 合并去重后过滤：点赞≥30、排除已有解决方案、字数>80（见 SKILL.md Step 3）\n4. Top 15 按热度排序\n5. 对每条帖子调用 AI 分析（见 SKILL.md Step 4）\n6. 【关键】执行完毕后立即用 message 工具发飞书，不要等 cron announce\n7. 如果配置了 Notion，也在 Notion 数据库创建卡片",
    "timeoutSeconds": 600
  },
  "delivery": {
    "mode": "none"  // ✅ 改为 none，避免重复推送；真正的推送在 skill 内部用 message 直接发
  }
}
```

## 配置变量 (TOOLS.md)

在 workspace 的 TOOLS.md 中维护：

```markdown
### X Demand Radar
- X_SEARCH_KEYWORD: (AI tool OR AI app OR AI website OR AI product) (I wish OR "someone should build" OR "why no" OR missing OR "need an AI" OR "million dollar idea")
- X_SEARCH_SINCE_DAYS: 30
- MIN_FAVES: 30
- TELEGRAM_CHAT_ID: <your-chat-id>
- NOTION_DATABASE_ID: <your-database-id>
- NOTION_API_KEY: <your-api-key>
```

## 已知限制

1. **Browser 抓取限制**：X 未登录用户只能看到约9条结果，需要多次滚动 — 已通过 JS 滚动收集解决
2. **懒加载**：X 搜索结果无限滚动，每次滚动加载新批次 — 已通过 `prevCount` 检测连续无新内容则提前停止
3. **时间衰减**：越旧的帖子越难被抓取，建议30天刷新周期
4. **付费推广过滤**：部分帖子是付费推广（如 @PetClaw_ai），需人工过滤

## 升级方案（可选）

如需稳定抓取更多结果，建议使用：
- **Apify X Scraper** ($0.35/1000条) - 支持完整分页
- **n8n 定时触发** - 自动化工作流
- OpenClaw 只负责 AI 分析 + 推送
