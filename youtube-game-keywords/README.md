# YouTube Game Keywords — 独立运行版

本目录包含可**独立运行**的脚本版本，无需依赖外部 Python 包。

## 文件说明

| 文件 | 说明 |
|------|------|
| `SKILL.md` | OpenClaw Skill 标准格式（供 Agent 调用） |
| `README.md` | 本文档（独立运行说明） |
| `scripts/fetch_subscriptions.sh` | 通过 OpenClaw Agent 抓取 YouTube 订阅（需 openclaw CLI） |
| `scripts/analyze_keywords.py` | 纯 Python 游戏关键词提取（无需 API key） |

## 快速开始

### 前置要求

- [ ] OpenClaw 已安装（https://openclaw.ai）
- [ ] openclaw CLI 已配置 `openclaw configure`
- [ ] 飞书 Bot 已配置（用于发送消息）

### Step 1：抓取数据

```bash
cd scripts
chmod +x fetch_subscriptions.sh
./fetch_subscriptions.sh ../data/videos.json
```

> ⚠️ 需要 OpenClaw browser 已登录 YouTube（在同一浏览器 session 下）

### Step 2：生成报告

```bash
chmod +x analyze_keywords.py
python3 analyze_keywords.py ../data/videos.json --output ../data/report.txt
```

### Step 3：发送飞书（手动）

```bash
# 使用 openclaw message 工具发送 report.txt 内容
```

## 完整 Cron Job（推荐）

在 OpenClaw 中配置定时任务，直接引用 SKILL.md，Agent 会自动完成全流程：

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

## 飞书 Bot 权限配置

本 skill 需要飞书 Bot 具备以下权限：

| 权限 | 标识 | 说明 |
|------|------|------|
| 云文档 | `docx:document` | 创建飞书文档 |
| 发消息 | `im:message:send_as_bot` | 发送飞书消息 |

开通路径：飞书开放平台 → 应用 → 权限管理 → 搜索权限名称 → 开通

## 游戏词库扩展

编辑 `scripts/analyze_keywords.py` 中的 `KNOWN_GAMES` dict 可扩展游戏识别范围。

格式：
```python
"游戏名关键词": {"type": "Roblox|PC/Console", "genre": "类型", "tier": "main|sub|rising|trending"}
```
