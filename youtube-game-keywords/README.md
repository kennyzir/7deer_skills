# YouTube Game Keywords — OpenClaw Skill 版

本 skill 有两种使用方式：

1. **OpenClaw Agent 模式**（推荐）：Agent 读 SKILL.md 自动执行全流程
2. **Python 脚本模式**：直接运行 `analyze_keywords.py`（抓取仍需 openclaw CLI）

## 文件说明

| 文件 | 说明 |
|------|------|
| `SKILL.md` | OpenClaw Skill 标准格式（供 Agent 调用） |
| `README.md` | 本文档（含 Python 脚本模式说明） |
| `scripts/fetch_subscriptions.sh` | 通过 OpenClaw Agent 抓取 YouTube 订阅（需 openclaw CLI） |
| `scripts/analyze_keywords.py` | 纯 Python 游戏关键词提取（无需 API key） |

---

## ⚠️ 最重要的前提：YouTube 登录态

**YouTube 订阅页（`/feed/subscriptions`）必须登录才能访问。**

这不是本 skill 的限制，是 YouTube 的限制。未登录状态下打开订阅页会跳转到登录页，抓不到任何数据。

### Browser 配置（必须先完成）

OpenClaw browser 和你的本地浏览器共享同一个 Chrome profile。

**macOS 示例：**

```bash
# 1. 找到你的 Chrome profile
# 通常在 ~/Library/Application Support/Google/Chrome/

# 2. 启动 OpenClaw browser 指定该 profile
openclaw browser start --profile ~/Library/Application\ Support/Google/Chrome/Default

# 3. 在打开的浏览器里打开 https://www.youtube.com 并登录
# 只需登录一次，以后自动保持登录态
```

**验证是否成功：**

```bash
# 打开订阅页，看到频道列表而不是登录框，即为成功
openclaw browser open "https://www.youtube.com/feed/subscriptions"
```

### ⏰ 定时任务配置

本 skill 支持每天自动执行。在 OpenClaw 中运行以下命令即可启用定时：

```bash
openclaw cron add \
  --name "YouTube Game Keywords 日报" \
  --schedule "0 10 * * *" \
  --tz "Asia/Shanghai" \
  --payload-kind agentTurn \
  --payload-message "使用 youtube-game-keywords skill，执行 YouTube 订阅频道游戏关键词日报任务。按照 skill 完整流程执行：1. 先尝试运行官方脚本（超时则降级用 browser 抓 YouTube 订阅页）2. 整理游戏关键词日报 3. 发送飞书消息到飞书用户 4. 创建飞书云文档并写入完整报告 5. 在飞书消息里附上文档链接" \
  --payload-timeout 900 \
  --delivery-mode announce \
  --delivery-channel feishu
```

**或手动创建 Cron Job（JSON）：**
```json
{
  "name": "YouTube Game Keywords 日报",
  "schedule": { "kind": "cron", "expr": "0 10 * * *", "tz": "Asia/Shanghai" },
  "sessionTarget": "isolated",
  "payload": {
    "kind": "agentTurn",
    "message": "使用 youtube-game-keywords skill，执行 YouTube 订阅频道游戏关键词日报任务。",
    "timeoutSeconds": 900
  },
  "delivery": {
    "mode": "announce",
    "channel": "feishu",
    "to": "user:YOUR_OPEN_ID",
    "accountId": "default"
  }
}
```

将 `YOUR_OPEN_ID` 替换为你的飞书 open_id。可选调整：
- `expr`: `"0 10 * * *"` → 改为其他时间（如 `"0 18 * * *"` 为每天 18:00）
- `timeoutSeconds`: `900` → 15分钟足够

---

## 快速开始

### Step 1：配置 Browser + 登录 YouTube（一次性）

```bash
mkdir -p ~/openclaw-browser-profile
openclaw browser start --profile ~/openclaw-browser-profile
# 在打开的浏览器里登录 YouTube
```

### Step 2：抓取数据

```bash
cd scripts
chmod +x fetch_subscriptions.sh
./fetch_subscriptions.sh ../data/videos.json
```

### Step 3：生成报告

```bash
python3 analyze_keywords.py ../data/videos.json --output ../data/report.txt
```

---

## 飞书 Bot 权限配置

| 权限 | 标识 | 说明 |
|------|------|------|
| 云文档 | `docx:document` | 创建飞书文档 |
| 发消息 | `im:message:send_as_bot` | 发送飞书消息 |

开通路径：飞书开放平台 → 应用 → 权限管理 → 搜索权限名称 → 开通

---

## 游戏词库扩展

编辑 `scripts/analyze_keywords.py` 中的 `KNOWN_GAMES` dict 可扩展游戏识别范围：

```python
"游戏名关键词": {"type": "Roblox|PC/Console", "genre": "类型", "tier": "main|sub|rising|trending"}
```
