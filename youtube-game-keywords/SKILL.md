---
name: youtube-game-keywords
description: |
  YouTube 订阅频道游戏关键词提取工具。自动抓取订阅频道视频，识别游戏关键词，
  归类为 Roblox / 独立游戏 / 主机PC 等赛道，生成结构化日报。
  触发词：YouTube 游戏关键词日报 / YouTube 订阅源 / 游戏热度 / YouTube game keywords。
  附有独立运行脚本，详见 README.md。
---

# YouTube Game Keywords Skill

从 YouTube 订阅频道抓取游戏相关内容，识别游戏关键词并生成结构化日报。

---

## 🚀 快速开始

### 前置要求

| 依赖 | 说明 |
|------|------|
| **OpenClaw** | 本 skill 运行于 OpenClaw 环境（https://openclaw.ai） |
| **飞书 Bot** | 需要已配置好的飞书 Bot 和 `feishu_doc` / `message` 工具权限 |
| **Browser 工具 + YouTube 登录态** | 用于抓取订阅页（⚠️ 必须已登录 YouTube，见下方说明） |
| **OpenClaw Browser 配置** | 详见"Browser 配置说明"章节 |

### 飞书 Bot 所需权限

| 权限名称 | 权限标识 | 用途 |
|---------|---------|------|
| **云文档** | `docx:document` | 创建飞书云文档写入日报 |
| **发消息** | `im:message:send_as_bot` | 向用户发送飞书消息 |
| **读取消息** | `im:message` | 消息交互（可选） |

> 💡 权限开通路径：飞书开放平台 → 应用 → 权限管理 → 搜索权限名称 → 开通

### 环境变量

| 变量 | 说明 | 必需 |
|------|------|------|
| `FEISHU_TARGET_USER` | 飞书通知目标用户的 open_id | 可选（默认发给当前对话用户） |

### 定时任务配置

```json
{
  "name": "YouTube Game Keywords 日报",
  "schedule": { "kind": "cron", "expr": "0 10 * * *", "tz": "Asia/Shanghai" },
  "payload": {
    "kind": "agentTurn",
    "message": "使用 youtube-game-keywords skill，执行 YouTube 订阅频道游戏关键词日报任务。",
    "timeoutSeconds": 900
  },
  "delivery": { "mode": "announce", "channel": "feishu" }
}
```

---

## 🔐 Browser 配置说明（必须先完成）

### 为什么需要登录态？

YouTube 订阅页 `/feed/subscriptions` **未登录用户无法访问**。不登录只看到"推荐订阅"内容，不是你的真实订阅列表。

OpenClaw 的 browser 和你的本地浏览器**共享同一个浏览器 profile**，所以：

1. 你在 Chrome/Safari/Edge 里登录了 YouTube
2. OpenClaw browser 打开订阅页就自动带着你的登录态

### 配置步骤

**方法一：使用已有的 Chrome profile（推荐）**

```bash
# 找到你的 Chrome profile 目录
# macOS 默认：
# ~/Library/Application Support/Google/Chrome/

# 启动 OpenClaw browser 使用指定 profile
openclaw browser start --profile ~/Library/Application\ Support/Google/Chrome/Default

# 然后在浏览器里手动登录 YouTube（只需一次）
```

**方法二：启动独立的 Chrome profile 供 OpenClaw 专用**

```bash
# 1. 创建新的 Chrome profile 目录
mkdir -p ~/openclaw-browser-profile

# 2. 启动 OpenClaw browser 指定该 profile
openclaw browser start --profile ~/openclaw-browser-profile

# 3. 首次使用：Browser 打开 https://www.youtube.com 并登录
# 以后每次运行都自动保持登录态
```

### 验证配置是否成功

在 OpenClaw 里执行：

```javascript
browser(action=open, url="https://www.youtube.com/feed/subscriptions")
// 等页面加载（3-5秒），然后：
browser(action=snapshot)
// 如果看到"订阅"内容（频道列表）而不是"登录"提示，说明配置成功
```

### ⚠️ 常见问题

| 问题 | 原因 | 解决 |
|------|------|------|
| 页面显示"登录 YouTube" | Browser 没有 YouTube 登录态 | 手动在 OpenClaw browser 里登录 YouTube |
| 能打开但视频列表为空 | 订阅列表为空或页面没加载完 | 页面需多次滚动触发懒加载 |
| 报错 "not logged in" | fetch_subscriptions.sh 检测到未登录 | 先在 browser 登录 YouTube |
| Cron 任务抓不到数据 | 定时任务 browser session 和手动不同 | 需确保 browser profile 持久化 |

---

## 📁 技能文件说明

```
youtube-game-keywords/
├── SKILL.md                        # Skill 标准格式（本文件）
├── README.md                       # 独立运行说明
└── scripts/
    ├── fetch_subscriptions.sh       # OpenClaw Agent 抓取脚本
    └── analyze_keywords.py         # 纯 Python 关键词分析（无需 API key）
```

---

## 📋 执行流程

### Step 1：Browser 抓取 YouTube 订阅页

> ⚠️ **重要**：执行此步前必须确认 OpenClaw browser 已登录 YouTube（见上方配置说明）。

```javascript
browser(action=open, url="https://www.youtube.com/feed/subscriptions")
```

等页面加载完成后（建议等待 3-5 秒）：
```javascript
browser(action=snapshot, refs="aria")
```

**必须多次滚动加载**（因为是无限滚动列表）：
```javascript
browser(action=act, kind="press", key="End", times=5)
```

解析页面中的视频列表，提取：
- `title`：视频标题
- `channel_name`：频道名
- `view_text`：播放量（如 "123K views"）
- `published_text`：发布时间（如 "2 days ago"）
- `url`：视频链接

### Step 2：识别游戏关键词

使用 `scripts/analyze_keywords.py`（纯规则，无需 API key）：

```bash
python3 scripts/analyze_keywords.py data/videos.json --output data/report.txt
```

或直接用 Agent 做 LLM 分类。

游戏分类：

| 分类 | 说明 |
|------|------|
| Roblox | Roblox 相关内容 |
| 独立游戏 | Deckbuilder / Roguelike / Horror / Adventure 等 |
| 主机/PC 大作 | 3A/主流游戏 |
| 直播 | Twitch/直播相关 |
| 其他 | 不属于以上类别 |

### Step 3：整理日报格式

```
📺 YouTube 订阅频道日报 — YYYY-MM-DD

【今日概要】一句话总结今日最显著的 trend

【Roblox 赛道】
- [游戏名] — [频道] — [播放量] — [一句话描述]

【独立游戏赛道】
- [游戏名] — [频道] — [播放量] — [一句话描述]

【主机/PC 赛道】
- [游戏名] — [频道] — [播放量] — [一句话描述]

【值得关注的独立游戏】（播放量 >50K 的非 Roblox 游戏）
| 游戏 | 频道 | 播放 | 类型 | 亮点 |

【算法流量猎奇发现】（高播放量但非主流内容）
| 游戏 | 频道 | 播放 | 猎奇点 |
```

### Step 4：发送飞书消息

```javascript
message(action=send, channel="feishu", target="user:$FEISHU_TARGET_USER", message=日报全文)
```

### Step 5：创建飞书云文档

```javascript
feishu_doc(action=create, title="YouTube 订阅频道日报 YYYY-MM-DD", owner_open_id="$FEISHU_TARGET_USER")
feishu_doc(action=write, doc_token=<创建的文档token>, content=完整报告内容)
```

### Step 6：在飞书消息里附上文档链接

---

## 🔧 独立运行（无需 OpenClaw Agent）

```bash
# 1. 抓取数据
chmod +x scripts/fetch_subscriptions.sh
./scripts/fetch_subscriptions.sh ./data/videos.json

# 2. 分析关键词
python3 scripts/analyze_keywords.py ./data/videos.json --output ./data/report.txt

# 3. 查看报告
cat ./data/report.txt
```

> ⚠️ 独立运行同样需要在运行前确保 `openclaw` CLI 已登录 YouTube（在 browser 里登录一次即可）。

---

## ⚠️ 注意事项

1. **YouTube 登录态是必须项**：Browser 未登录则完全无法抓取订阅页，这是 YouTube 的限制，无法绕过
2. **播放量 >100K** 的内容优先呈现
3. **无游戏内容时**：注明"今日订阅频道无游戏相关更新"
4. **open_id 获取**：飞书用户 open_id 可在 Bot 收到消息时从事件 payload 中获取
5. **本 skill 不包含任何 API Key**，所有外部依赖通过环境变量或本地脚本接入
6. **Browser profile 必须持久化**：定时任务场景下确保 browser profile 不会每次清空，导致重新需要登录
