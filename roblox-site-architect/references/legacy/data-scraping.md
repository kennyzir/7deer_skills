# Game Data Scraping Pipeline

Originally from `roblox-game-data-scraper` skill. Consolidated into `roblox-site-architect` umbrella.

## 4 Data Sources
1. **Trello boards** — Official game data
2. **Discord channels** — Real-time codes/announcements
3. **Reddit communities** — Player wisdom, trading values
4. **In-game APIs** — Player counts, leaderboards

## Output Types
- `GameCode` — codes and rewards
- `GameItem` — items with rarity/stats
- `Technique` — techniques with moves/PvP ratings
- `TradeValue` — trading values with demand/trend

## Automation
- GitHub Actions cron (every 6h)
- Data versioning with dated snapshots
- Auto-commit + deploy

## Risk Controls
Rate limiting, robots.txt compliance, data dedup, validation rules
