---
name: roblox-game-data-scraper
description: 从 Roblox 游戏的公开 Trello 看板采集卡片，并提取物品与兑换码结构化数据。适用于无需登录的公开看板资料整理和 JSON 数据准备。
metadata:
  keywords: roblox, trello, public board, data scraping, game data, codes, items
---

# Roblox Trello Game Data Scraper

这个 Skill 只提供公开 Trello 看板采集能力。使用 [resources/trello_scraper.py](resources/trello_scraper.py) 调用 Trello 公共 API，读取列表和卡片并提取物品与兑换码。

## 已实现范围

- 通过看板 ID 获取公开 Trello 看板的列表与卡片。
- 从名称包含 `item`、`weapon`、`accessory` 或 `equipment` 的列表提取物品。
- 从名称包含 `code` 的列表提取兑换码，并根据列表名称判断 Active/Expired。
- 从卡片描述和标签提取稀有度、掉落率、部分属性、获取方式与奖励。
- 将提取结果序列化为 JSON。

解析采用启发式规则。字段没有在卡片中出现时会返回 `None`、空字典或 `Unknown`，不要把缺失值补写成事实。

## 未实现边界

Discord、Reddit、Roblox 游戏内 API、持续监控、类型文件生成和自动部署目前均未实现。它们只属于 roadmap；不要声称已采集这些来源，也不要为它们配置凭据或定时任务。

## 前置条件

- Python 3.8+
- `requests`
- 一个无需登录即可访问的公开 Trello 看板 ID

安装依赖：

```bash
python3 -m pip install requests
```

## 使用流程

1. 从公开看板 URL `https://trello.com/b/<board-id>/...` 取得 `<board-id>`。
2. 在 Python 中实例化 `TrelloScraper` 并调用 `get_board_data(board_id)`。
3. 分别调用 `extract_items(board_data)` 和 `extract_codes(board_data)`。
4. 保留原始来源 URL 和抓取时间，并人工复核启发式解析结果。

```python
import json
from resources.trello_scraper import TrelloScraper

scraper = TrelloScraper()
board_data = scraper.get_board_data("your-public-board-id")
output = {
    "items": [vars(item) for item in scraper.extract_items(board_data)],
    "codes": scraper.extract_codes(board_data),
}
print(json.dumps(output, ensure_ascii=False, indent=2))
```

直接执行脚本会运行文件底部的示例看板，并在当前目录写入 `trello_data.json`。通用工作流应导入 `TrelloScraper`，显式提供自己的看板 ID 和输出位置。

## 输出字段

物品记录包含：

- `name`
- `category`
- `rarity`
- `drop_rate`
- `stats`
- `obtain_method`
- `description`

兑换码记录包含：

- `code`
- `reward`
- `status`
- `notes`

## 错误与数据边界

- 私有、删除或不存在的看板会由 `requests` 的 HTTP 错误终止。
- Trello 卡片格式变化可能降低提取完整度；应保留原始卡片内容以便复核。
- 公开访问不需要 API Key。若未来使用私有看板，只能从调用方传入凭据，不能写入 Skill 文件或仓库。

## Roadmap

Discord 和 Reddit 采集只有在实现真实客户端、凭据边界、限流处理和离线测试后才能加入“已支持”范围。在此之前，相关数据必须由用户另行提供并注明来源。
