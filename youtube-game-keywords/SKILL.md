---
name: youtube-game-keywords
description: |
  YouTube 订阅频道游戏关键词提取工具。自动抓取订阅频道视频，识别游戏关键词，
  归类为 Roblox / 独立游戏 / 主机PC 等赛道，生成结构化日报。
  触发词：YouTube 游戏关键词日报 / YouTube 订阅源 / 游戏热度 / YouTube game keywords。
---

# YouTube Game Keywords Skill

从 YouTube 订阅频道抓取游戏相关内容，识别游戏关键词并生成结构化日报。

## 环境配置

| 变量 | 说明 |
|------|------|
| `YOUTUBE_SUBS_SCRIPT_DIR` | 官方脚本所在目录（可选，未配置时使用 browser 降级方案） |
| `FEISHU_TARGET_USER` | 飞书通知目标用户的 open_id（可选，默认使用 skill 调用者的上下文） |

## 数据来源

- 优先：本地 YouTube 订阅抓取脚本（`$YOUTUBE_SUBS_SCRIPT_DIR/scripts/run_openclaw_subscriptions_hot_games.sh`）
- 降级：browser 直接访问 `https://www.youtube.com/feed/subscriptions`

## 执行流程

### Step 1：尝试运行本地脚本（如已配置）

```bash
cd "$YOUTUBE_SUBS_SCRIPT_DIR" && zsh scripts/run_openclaw_subscriptions_hot_games.sh
```

读取生成的报告：
```bash
cat "$YOUTUBE_SUBS_SCRIPT_DIR/data/reports/openclaw_subscriptions_digest.txt"
```

如果脚本超时（SIGKILL/exit code != 0）或 `YOUTUBE_SUBS_SCRIPT_DIR` 未配置，立即切换 Step 2。

### Step 2：Browser 降级抓取

```javascript
browser(action=open, url="https://www.youtube.com/feed/subscriptions")
```

等页面加载完成后：
```javascript
browser(action=snapshot, refs="aria")
```

解析页面中的视频列表，提取：视频标题、频道名、播放量、上线日期。

### Step 3：识别游戏关键词

| 分类 | 说明 |
|------|------|
| Roblox | Roblox 相关内容 |
| 独立游戏 | 单机/独立制作游戏 |
| 主机/PC 大作 | 3A/主流游戏 |
| 直播 | Twitch/直播相关 |
| 其他 | 不属于以上类别 |

### Step 4：整理日报格式

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

### Step 5：发送飞书消息

```javascript
message(action=send, channel="feishu", target="user:$FEISHU_TARGET_USER", message=日报全文)
```

### Step 6：创建飞书云文档

```javascript
feishu_doc(action=create, title="YouTube 订阅频道日报 YYYY-MM-DD", owner_open_id="$FEISHU_TARGET_USER")
feishu_doc(action=write, doc_token=<创建的文档token>, content=完整报告内容)
```

### Step 7：在飞书消息里附上文档链接

## 注意事项

- Browser 降级方案需要登录态，页面可能需要滑动加载才能抓全
- 脚本超时（约 60s）时自动切换 browser 降级方案
- 播放量 >100K 的内容优先呈现
- 本 skill 不包含任何 API Key，所有外部依赖通过环境变量或本地脚本接入
