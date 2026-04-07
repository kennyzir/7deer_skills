# YouTube Game Keywords — 独立运行版

本目录包含可**独立运行**的脚本版本。

## 文件说明

| 文件 | 说明 |
|------|------|
| `SKILL.md` | OpenClaw Skill 标准格式（供 Agent 调用） |
| `README.md` | 本文档（独立运行说明） |
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

### 定时任务场景注意

如果用 cron job 跑本 skill，需要确保 OpenClaw browser 的 profile 目录是固定的，不会被清空。建议使用专用 Chrome profile 目录（不要用 Default）。

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
