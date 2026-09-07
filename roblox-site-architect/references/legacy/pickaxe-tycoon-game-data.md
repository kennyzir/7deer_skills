# {Game Name} — Game Data Reference

Game domain: `{site-a}.gg`
Repository: `<project-root>`
Roblox ID: `73814003954154`
Genre: Tycoon / Simulator
Developer: Popular Marketplace

---

## YouTube Creators (authoritative)

| Creator | Subs | Role |
|---------|------|------|
| Bax | 3.18M | Major coverage — "I Took {Game Name} TOO FAR" (38,997 views in 3 days) |
| AlphaShoe | 185 | Early game mechanics — "I Bought 1,500 PICKAXES"揭露升级路径 |
| RBXPLAYZ07 | small | Tier progression series — "Reaching Pickaxe Tier 10" |
| Darklord | 16.4K | Codes coverage |

**Bax's Roblox Support Code**: `Baxtrix`（创作者码，不是游戏兑换码）

---

## Pickaxe Progression (confirmed from AlphaShoe video)

```
Coal Pickaxe → Stone Pickaxe → Crystal Pickaxe → Crystal Pickaxe II
```

AlphaShoe got **2 Crystal Pickaxes** after buying 1,500 total pickaxes.
Video title: "I Bought 1,500 PICKAXES in Roblox {Game Name}!"

---

## 10-Tier System (confirmed from RBXPLAYZ07 series)

Game has **10 numeric Pickaxe Tiers** (not letter grades). Reaching Tier 10 is the stated goal.
Video: "Episode 4: Reaching Pickaxe Tier 10 & Climbing the Leaderboard!"

Letter grades (S/A/B/C/D) are a content presentation layer — the game uses numeric tiers internally.

---

## Pickaxe List (10 total, from YouTube research)

| ID | Name | Tier | Grade | Power | Price | Notes |
|----|------|------|-------|-------|-------|-------|
| coal | Coal Pickaxe | 1 | D | 1 | Free | Starting pickaxe |
| stone | Stone Pickaxe | 2 | D | 3 | $100 | |
| copper | Copper Pickaxe | 3 | C | 8 | $500 | |
| iron | Iron Pickaxe | 4 | C | 20 | $2,500 | |
| gold | Gold Pickaxe | 5 | B | 55 | $12,000 | |
| diamond | Diamond Pickaxe | 6 | B | 150 | $75,000 | |
| crystal | Crystal Pickaxe | 7 | A | 400 | $350,000 | AlphaShoe got this at 1,500 total purchases |
| crystal-ii | Crystal Pickaxe II | 8 | A | 900 | Merge only | Two Crystal → one Crystal II |
| void | Void Pickaxe | 9 | S | 2,500 | $2,000,000 | |
| void-ii | Void Pickaxe II | 10 | S | 5,000 | Merge only | Two Void → one Void II = MAX TIER |

**Key insight**: Crystal II and Void II can ONLY be obtained through merging. They have no shop price.

---

## High-Traffic Keywords (from YouTube search)

| Keyword | Views | Opportunity |
|---------|-------|-------------|
| {Game Name} script auto collect | 6,854 | Script/exploit流量，高竞争 |
| "I Took {Game Name} TOO FAR" | 38,997 (3 days) | Bax 3.18M subscriber video |
| {Game Name} merge | 0 results | **高机会低竞争** |
| {Game Name} Tier 10 | confirmed demand | 无好结果 |
| {Game Name} codes | active search | Codes页核心词 |

---

## Codes Status (as of 2026-05-27)

No active codes confirmed. Game is new (updated May 2026).
Darklord (16.4K) posts codes videos — monitor this channel.
No Beebom/PCGamesN coverage yet.

---

## Deployment

Repository: `git@github.com:kennyzir/{site-a}.git`
Cloudflare: `{site-a}` Pages project
Deploy: `wrangler pages deploy out --project-name={site-a}`
