# Block Tales Keyword-to-Page Pipeline

Originally from `{game-name}-keyword-to-page` skill. Consolidated into `roblox-site-architect` umbrella.

Uses **Data Architecture Mode B** (multi-file JSON + accessor layer), unlike the Mode A single-file approach.

## Project Specifics
- Game: Block Tales (Spaceman Moonbase, Demo 5)
- Repo: `kennyzir/{repo-name}`
- Local path: `<project-root>`

## Data Architecture (Mode B)
```
src/data/bosses.json, cards.json, game.config.json
src/lib/data.ts → getBosses(), getCards(), getGameConfig()
Sitemap auto-generates boss routes from bosses.json
```

## Boss Detail Page Template
HP/BP/attack table + weaknesses + strategy + recommended cards + video

## Pitfalls
- Sitemap auto-generates from bosses (just add to JSON)
- `videoId` requires manual YouTube lookup
- New boss entries go first in JSON array
- `config.routes` must be synced

## Current Pages
10 pages: bosses list, 3 boss detail pages, demo-5, cards, codes, community, korbloxian-empire, simulator

## Weekly Cadence
Tue/Wed keyword mining → Thu expected Demo content → Fri game update check → Sat/Sun high traffic monitoring
