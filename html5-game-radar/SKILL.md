---
name: html5-game-radar
description: |
  HTML5 游戏发现雷达 - 多源监测又新又热的 HTML5 游戏，识别 SEO 套利窗口。

  触发条件：
  - 用户说「跑 HTML5 雷达」、「启动 HTML5 监控」、「HTML5 游戏扫描」
  - 每天 cron 自动触发（建议 10:00 / 16:00）

  监测平台：
  1. itch.io — 独立游戏最大源头，HTML5 首发首选
  2. Reddit r/webgames — 玩家发现新游戏第一线
  3. Google Trends — 搜索量爆发判断
  4. X/Twitter — 游戏病毒扩散早期信号（基于游戏名搜索）
  5. Crazy Games / YouTube — 补充信号源

  信号评分（0-20）判断游戏是否值得做 SEO 内容。
---

# HTML5 Game Radar — 游戏发现雷达

## 核心目标

发现**又新又热**的 HTML5 游戏，在 SEO 空白期抢先建站截流。

```
游戏爆发（玩家在找）
    ↓
Google 搜索量 ↑  但内容页 ↓（SEO 空白）
    ↓
你抢先建站 → 截流搜索流量
```

---

## 工作流程

```
Step 1: itch.io 监测（最新 HTML5 游戏，?sort=date）
Step 2: Reddit r/webgames 新帖扫描
Step 3: Google 搜索量 + 竞争度验证
Step 4: X/Twitter 扩散信号（用游戏名搜索）
Step 5: 汇总评分 + 排序
Step 6: 推送 Feishu
```

---

## Step 1: itch.io HTML5 新游戏抓取

**目标 URL：** `https://itch.io/games/tag-html5?sort=date`

**⚠️ 重要：** itch.io 的 votes 和 date 是懒加载 JS，无法从 DOM 提取。评分改用「标题关键词 + 类型」作为主要打分依据。

**Browser 操作流程：**
1. `browser(action="navigate")` → `https://itch.io/games/tag-html5?sort=date`
2. 滚动 3 次，每次 `window.scrollBy(0, 800)`
3. `browser evaluate` 提取游戏列表

**提取字段：**
```javascript
document.querySelectorAll('.game_cell').forEach(cell => {
  const title = cell.querySelector('.title')?.innerText || '';
  const dev = cell.querySelector('.game_author a')?.innerText || '';
  const genre = cell.querySelector('.game_genre')?.innerText || '';
  const url = cell.querySelector('.title')?.href || '';
  results.push({ title, dev, genre, url });
});
```

**信号判断：**
- 标题含「new」「free」「multiplayer」「io」「survival」= 热门类型信号
- 游戏类型为 Action/Adventure/Survival/Puzzle = 高价值类型
- ⚠️ 过滤 Jam 游戏：标题含「jam」「Ludum」「 GMTK」「Game Jam」= 低价值

---

## Step 2: Reddit r/webgames 扫描

`scripts/reddit_monitor.py` 需要通过 `--reddit-script` 或专用环境变量 `HTML5_REDDIT_SCRIPT` 指向已有的 `reddit.ts`。未配置时停止，不会调用 `npx`；默认输出 JSON 到 stdout，只有显式 `--output` 才创建新文件且不会覆盖已有路径。

```bash
python3 scripts/reddit_monitor.py --reddit-script /path/to/reddit.ts
python3 scripts/reddit_monitor.py --reddit-script /path/to/reddit.ts --output reddit_output.json
```

**使用 reddit-research skill 的 CLI：**
```bash
npx tsx reddit.ts new webgames --limit 30
```

**过滤 HTML5/浏览器游戏相关帖子：**
```bash
npx tsx reddit.ts search "html5 OR browser game OR itch.io" --sub webgames --sort new --limit 20
```

**信号判断：**
- 单帖 upvotes > 50 = 强信号
- 单帖评论 > 20 = 讨论活跃
- 含游戏链接（非自荐）= 玩家主动分享

---

## Step 3: Google 搜索量 + 竞争度验证

**对 Top 5 游戏名执行：**

用 browser 打开 Google 搜索：
```
https://www.google.com/search?q=[游戏名]+game+online+free
```

**在页面 snapshot 中检查：**
- 搜索结果数量（Accessibility tree 中的「约 X 个结果」）
- 是否有 Wikipedia / 主流媒体提及
- 是否有 Fandom wiki / 攻略站

**SEO 套利判断：**
```
搜索结果 < 50,000 = ✅ 低竞争（SEO 友好）
搜索结果 50,000-200,000 = ⚠️ 中等竞争
搜索结果 > 200,000 = ❌ 高竞争（红海）
有 Wikipedia = ✅ 流量精准（值得做）
有 Fandom wiki = ✅ 已有内容生态（可截流）
```

---

## Step 4: X/Twitter 扩散信号

**⚠️ 在 Step 1/2 获取游戏名之后执行。用游戏名搜 X，不要泛搜。**

**搜索词构造：**
```
"[游戏名]" html5
"[游戏名]" "new game" site:twitter.com
"[游戏名]" "everyone playing"
```

**执行流程：**
1. 从 itch.io/Reddit 结果提取 Top 10 游戏名
2. 对每个游戏构造 1-2 个 X 搜索
3. 用 `browser(action="navigate")` 打开 X 搜索
4. 用 JS 提取：推文数、含游戏链接的帖子

**简化收集 JS（X 未登录版最多 9 条）：**
```javascript
document.querySelectorAll('article[data-testid="tweet"]').forEach(t => {
  const text = t.querySelector('[lang]')?.innerText || '';
  const likes = t.querySelector('[data-testid="like"] span')?.innerText || '0';
  if (text.includes('game_name')) results.push({ text, likes });
});
```

**信号判断：**
- ≥3 条相关推文 = 🟢 爆发前兆
- 1-2 条 = 🟡 关注中
- 0 条 = ⚪ 沉默期

---

## Step 5: 信号评分（0-20）

⚠️ **注意**：itch.io 票数和发布日期为懒加载，无法从 DOM 提取。评分系统改用以下替代信号：

| 信号维度 | 分值 | 判断依据 |
|---------|------|---------|
| **标题关键词** | +1~5 | 含「new」「free」「multiplayer」「io」=+2；含「online」「survival」「roguelike」=+1 |
| **游戏类型** | +1~3 | Action/Adventure/Survival/Puzzle=+3；Simulation/Strategy=+2；Other=+1 |
| **开发活跃度** | +1~2 | 开发者有多个游戏=+2；首次发布=+1 |
| **Reddit 信号** | +1~4 | upvotes > 100=4, > 50=3, > 20=2 |
| **Google 竞争度** | +1~4 | 结果<5万=4, <20万=3, <50万=2, >50万=1 |
| **X/Twitter 信号** | +1~3 | ≥3条=3, 2条=2, 1条=1 |

**阈值判断：**
- **15-20 分**：🔥 立即行动 — 立刻建站/写内容
- **10-14 分**：✅ 值得做 — 写攻略/合集页
- **5-9 分**：⚠️ 观察 — 加入监控列表
- **< 5 分**：❌ 跳过 — 竞争已饱和或信号太弱

---

## Step 6: 推送 Feishu

**报告格式：**

```
🎮 HTML5 Game Radar | {{ DATE }}

🏆 Top 信号游戏

## [游戏名]
- 平台：itch.io / Reddit / X
- 类型：[游戏类型]
- 信号分数：{{ }}/20
- SEO 窗口：✅ 低竞争 / ⚠️ 中等 / ❌ 高竞争
- Google 搜索结果：约 X 个
- X 信号：X 条相关推文
- 套利建议：建攻略页 / 合集页 / 评测页
- 链接：[游戏链接]

📊 信号汇总
- itch.io 新游戏：N 个
- Reddit 讨论帖：N 篇（X 条高信号）
- X 扩散信号：N 条
- 高价值候选：N 个（≥10分）
```

---

## Cron 配置

```javascript
{
  "name": "HTML5 Game Radar 每日扫描",
  "schedule": { "kind": "cron", "expr": "0 10,16 * * *", "tz": "Asia/Shanghai" },
  "sessionTarget": "isolated",
  "payload": {
    "kind": "agentTurn",
    "message": "使用 html5-game-radar skill 执行 HTML5 游戏发现扫描：\n\n1. 打开 browser 访问 itch.io ?sort=date，收集游戏名+类型（SKILL.md Step 1）\n2. 用 reddit-research skill 扫描 r/webgames 新帖（SKILL.md Step 2）\n3. 对 Top 5 游戏验证 Google 搜索量和竞争度（SKILL.md Step 3）\n4. 用游戏名在 X/Twitter 搜索扩散信号（SKILL.md Step 4）\n5. 按 0-20 分评分标准打分（SKILL.md Step 5）\n6. 执行完毕后立即用 message 工具发飞书（SKILL.md Step 6）",
    "timeoutSeconds": 600
  },
  "delivery": { "mode": "none" }
}
```

---

## 已知限制

1. **itch.io votes/date 不可提取**：懒加载 JS，评分改用标题关键词 + 类型
2. **X 未登录限制**：最多 9 条结果，用游戏名精准搜索弥补
3. **Google Trends API**：需要 API Key，改用 browser 打开搜索页判断竞争度
4. **Jam 游戏干扰**：过滤标题含「jam」「Ludum」「Game Jam」的游戏

---

## 参考资料

- SEO 套利方法论：见 `references/seo_arbitrage_logic.md`
- 平台首发特点：见 `references/platform_signals.md`
