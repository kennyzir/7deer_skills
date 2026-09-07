# Be a Lucky Block — Game Data Reference

Game domain: `{site-a}.gg`
Repository: `<project-root>`

---

## Known YouTube Creators (authoritative)

| Creator | Subscribers | Role |
|---------|-----------|------|
| CoralBlox | ~770K | Primary coverage, patch confirms |
| LukeBlox | ~1.02M | Primary coverage, patch confirms |
| DeluxPlays | ~1.39M | Secondary/casual coverage |
| Pawablox | ~581K | Codes/content |
| AlphaBolt | ~1.14M | Codes/content |

**Dual-coverage rule**: Both CoralBlox AND LukeBlox post about same update within 48hrs = confirmed live.

---

## Update Timeline (as of 2026-05-24)

| Update | Date | Key Content |
|--------|------|-------------|
| Update 9 | 2026-05-17 | Toy King Event, Radioactive Mutations, Monk brainrot, Arcade, Claw Machine, Training Weights |
| Update 8 | 2026-05-09 | Bee Event, Frenzy Blocks, MAX LEVEL, Automated Run |
| Update 7 | ~2026-05-02 | DinoByte Mining, Infinity Event, Mining Shafts, Index System |
| Update 5/6 | 2026-04-25 | Coral vs Luke, Prevatic, Slayer's Base, LA Admin fusion |
| Update 4 | ~2026-04 | Core additions |
| Devil Event | 2026-03-28 | Devilivion's Base, Devil Lucky Block |
| Zeus Event | ~2026-03 | Angelic brainrots, Zeus Lucky Block |

**Saturday cadence**: Game updates every Saturday. Mine keywords Fri/Sat.

---

## Codes — Authoritative Sources

| Source | Reliability |
|--------|-------------|
| Beebom | ⭐⭐⭐⭐⭐ — "Update: added new codes on [DATE]" = strongest signal |
| PCGamesN | ⭐⭐⭐⭐⭐ |
| Eurogamer | ⭐⭐⭐⭐ |
| Pocket Tactics | ⭐⭐⭐⭐ |
| Game8 | ⭐⭐⭐⭐ |
| Reddit r/Roonby | ⭐⭐ — signal only, NOT confirmation |

**Current codes (13 total, as of 2026-05-24):**

| Code | Reward | Added |
|------|--------|-------|
| RADIOACTIVE | 150 Honey (Update 9) | 2026-05-16 |
| BEE | 100 Honey (Bee Event) | 2026-05-14 |
| DinoByte | Brainrot (DinoByte Event) | 2026-05-05 |
| R5M93 | 50 Spin Coins | 2026-05-04 |
| CORALUKE | Coffee Coins / Brainrot | 2026-04-25 |
| BIRD | 10 Tokens | 2026-05-16 |
| M2ZF4KYR | 2 Easter Blocks | 2026-04-25 |
| EASTER | 35 Tokens | 2026-04-11 |
| FIX31 | 10 Tokens | 2026-04-11 |
| R81KM461 | 2x Brainrots | 2026-04-11 — ⚠️ Beebom lists as active (2026-05-16), site has in expiredCodes. Verify. |
| GOD | Brainrot | 2026-03-28 |
| DEVIL | Brainrot | 2026-03-28 |
| ZEUS | Angelzini Bananini | 2026-03-28 |
| RELEASE | Brr Brr Patapim | 2026-03-01 |

**Expired (4):** CORALBLOX, LUKEBLOX, SPRINGHYPE, BRAINROTDAY

**Common discrepancies found:**
- `BEE` code: was "Brainrot" → actual is "100 Honey" (Bee Event currency)
- `R5M93`: was "Brainrot" → actual is "50 Spin Coins"
- Reward descriptions evolve with events — always cross-check latest gaming media

---

## Watchlist (Unverified)

| Item | Source | Action |
|------|--------|--------|
| `lucky2026` code | Reddit | Monitor only — NOT corroborated by Beebom/PCGamesN |
| Monk's Base speed | YouTube/TikTok | Watch for official confirmation |
| Update 10 | Prediction | Projected May 24-31, 2026 |

---

## Deployment

```bash
npm run build 2>&1 | tail -20  # verify
git add -A && git commit -m "feat: [description]" && git push
```
Cloudflare Pages auto-deploys on push to `main`.
