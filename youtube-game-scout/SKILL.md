---
name: youtube-game-scout
description: 从 YouTube 订阅内容中抓取并分析新游戏信号，生成带评分和平台分类的游戏发现报告。适用于通过 Chrome CDP 监测频道和筛选潜力游戏。
---

# YouTube Game Scout Skill

## 概述

通过 CDP (Chrome DevTools Protocol) 自动化抓取 YouTube 订阅频道，识别新游戏发现信号，生成结构化游戏发现报告。

## 核心功能

1. **CDP 滚动抓取** — 连接 Chrome 浏览器，滚动 YouTube 订阅 feed，提取视频元数据
2. **游戏信号分析** — 0-20 分信号评分，识别 NEW/UPDATE/EMERGING 关键词
3. **平台分类** — 区分 Roblox/Steam/itch.io/HTML5/AAA 游戏
4. **报告生成** — 输出 markdown 格式游戏发现报告

## 脚本说明

### `cdp_game_scout.js`

CDP 游戏侦察脚本。通过 Chrome 远程调试端口连接浏览器，滚动订阅 feed 并提取视频数据。

**前置条件：**
- Chrome 浏览器需开启远程调试端口：`--remote-debugging-port=18800`
- Node.js 环境
- `ws` npm 模块：`npm install -g ws`

**使用方法：**
```bash
# 1. 启动 Chrome（macOS）
open -a "Google Chrome" --args --remote-debugging-port=18800

# 2. 运行抓取脚本
NODE_PATH=$HOME/.npm-global/lib/node_modules \
  node cdp_game_scout.js
```

**输出：**
- `/tmp/yt_games_final.json` — 原始视频数据
- 终端打印抓取进度

### `analyze_game_discovery.py`

游戏发现信号分析器。读取 JSON 数据，输出评分后的游戏发现报告。

**前置条件：**
- Python 3.7+
- 无额外依赖

**使用方法：**
```bash
python3 analyze_game_discovery.py
```

**评分维度（0-20 分）：**

| 信号 | 分值范围 | 说明 |
|------|---------|------|
| NEW GAME | +5-10 | 首次发现/新发布 |
| UPDATE | +3-5 | 游戏更新版本 |
| EMERGING | +4-8 | 上升期游戏 |
| PLATFORM | +1-3 | 平台明确度 |
| GENRE | +1-2 | 类型清晰度 |
| PERSONAL REVIEW | +2 | "I played/tried" 亲测信号 |
| WORTH IT | +1 | 价值评估信号 |

**输出：**
- `/tmp/game_discovery_report.md` — 结构化报告

## 工作流程

```
手动浏览订阅频道（browser 工具）
    ↓
运行 cdp_game_scout.js 抓取数据
    ↓
运行 analyze_game_discovery.py 分析
    ↓
生成游戏发现报告
    ↓
（可选）推送至 Feishu 文档
```

## 配置

- **CDP WebSocket URL**: `ws://127.0.0.1:18800/devtools/page/<TARGET_ID>`
- **抓取深度**: 25 次滚动（~5 天视频覆盖）
- **数据存储**: `/tmp/yt_games_final.json`

## 局限性

- 需手动登录 YouTube 获取订阅 feed 访问权限
- 频道名称提取受 YouTube Shadow DOM 影响
- 滚动深度有限，超出窗口的视频不会被抓取
- 建议配合 YouTube Game Keywords cron（10:00 CST）使用
