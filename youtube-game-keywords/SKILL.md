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
| **Browser 工具** | 用于抓取 YouTube 订阅页（需 Chromium 内核浏览器） |

### 飞书 Bot 所需权限

本 skill 会调用以下飞书 API，需要在飞书开放平台给 Bot 开通对应权限：

| 权限名称 | 权限标识 | 用途 |
|---------|---------|------|
| **云文档** | `docx:document` | 创建飞书云文档写入日报 |
| **发消息** | `im:message:send_as_bot` | 向用户发送飞书消息 |
| **读取消息** | `im:message` | 消息交互（可选） |

> 💡 权限开通路径：飞书开放平台 → 应用 → 权限管理 → 搜索并开通以上权限

### 环境变量

| 变量 | 说明 | 必需 |
|------|------|------|
| `FEISHU_TARGET_USER` | 飞书通知目标用户的 open_id | 可选（默认发给当前对话用户） |

### 定时任务配置

如需每天自动执行，可在 OpenClaw 中创建 cron job：

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

## 📁 技能文件说明

本 skill 包含以下文件（见 skill 压缩包）：

```
youtube-game-keywords/
├── SKILL.md                        # Skill 标准格式（本文件）
├── README.md                       # 独立运行说明
└── scripts/
    ├── fetch_subscriptions.sh       # OpenClaw Agent 抓取脚本（chmod +x）
    └── analyze_keywords.py          # 纯 Python 关键词分析（无需 API key）
```

---

## 📋 执行流程

### Step 1：Browser 抓取 YouTube 订阅页

使用 browser 工具打开并抓取订阅频道：

```javascript
browser(action=open, url="https://www.youtube.com/feed/subscriptions")
```

等页面加载完成后：
```javascript
browser(action=snapshot, refs="aria")
```

解析页面中的视频列表，提取：
- `title`：视频标题
- `channel_name`：频道名
- `view_text`：播放量（如 "123K views"）
- `published_text`：发布时间（如 "2 days ago"）
- `url`：视频链接

> ⚠️ 需要 YouTube 账号处于登录态，页面需多次滑动（3-5次）加载更多内容。

### Step 2：识别游戏关键词

使用 `scripts/analyze_keywords.py` 进行分类（可选，纯规则无需 API key）：

```bash
python3 scripts/analyze_keywords.py data/videos.json --output data/report.txt
```

或直接用 Agent 自己做 LLM 分类，输出结构化 JSON。

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

## 🔧 独立运行（无需 Agent）

如果想在命令行直接运行，不通过 OpenClaw Agent：

```bash
# 1. 抓取数据（需要 openclaw CLI）
chmod +x scripts/fetch_subscriptions.sh
./scripts/fetch_subscriptions.sh ./data/videos.json

# 2. 分析关键词
python3 scripts/analyze_keywords.py ./data/videos.json --output ./data/report.txt

# 3. 查看报告
cat ./data/report.txt
```

---

## ⚠️ 注意事项

1. **YouTube 登录态**：Browser 方案需要 YouTube 登录态
2. **播放量**：Browser 显示多少就填多少，不强制要求
3. **播放量 >100K** 的内容优先呈现
4. **无游戏内容时**：注明"今日订阅频道无游戏相关更新"
5. **open_id 获取**：飞书用户 open_id 可在 Bot 收到消息时从事件 payload 中获取
6. **本 skill 不包含任何 API Key**，所有外部依赖通过环境变量或本地脚本接入
