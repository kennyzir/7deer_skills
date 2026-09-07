# Keyword-to-Page Pipeline (Roblox)

## 7-Step Pipeline

1. **Keyword Mining** → 2. **Value Assessment** → 3. **Decision** → 4. **Page Build** → 5. **Data Update** → 6. **Build Verify** → 7. **Deploy**

---

### Step 1: Keyword Mining (Multi-Source)

YouTube video descriptions contain **"Related keywords"** blocks — these are the video creator's own SEO targets and are gold for mining. Always check the description text below the fold.

**Source Priority (for codes/discovery):**
1. **Gaming media** (Beebom, PCGamesN, Eurogamer, Pocket Tactics, Game8) — authoritative, timestamped updates
2. **YouTube descriptions** — actual "Related keywords" blocks + video titles + view counts
3. **YouTube snapshots** — "Searches related to..." in sidebar (use Yahoo browser for hot/trending)
4. **Reddit** — useful for unconfirmed codes BUT only as signal, not confirmation (e.g. `lucky2026` appeared on Reddit but NOT on any authoritative gaming site → do NOT add to site without corroboration)
5. **TikTok** — secondary signal for viral mechanics, NOT for data accuracy

**For codes specifically:**
- Cross-reference at least 2 authoritative gaming sites (Beebom + PCGamesN minimum)
- Reddit-only codes = unverified signal, watch but don't ship
- Beebom "Update: added new codes on [DATE]" = strongest confirmation signal available
- Watch for reward description changes (e.g. `BEE` code: "Brainrot" → actual is "Honey" for Update 8 Bee Event)

**For mechanics/features:**
- YouTube view counts: 50K+ = confirmed hot, 10K-50K = trending, <10K = niche
- LukeBlox/CoralBlox pattern: major updates get dual coverage from both creators within 24-48hrs
- "Monk's Base" + "Radioactive Rarity" in same video title = Update 9 confirmed live

---

### Step 2: Value Assessment

| Signal | Assessment |
|--------|------------|
| YouTube 50K+ views in <7 days | High volume, confirmed demand |
| Gaming media "new" label | Fresh content, compete on completeness |
| Beebom/PCGamesN listing | High authority signal |
| Reddit-only (no gaming media) | Unverified — monitor only |
| YouTube description "Related keywords" block | High intent, creator-verified search terms |

---

### Step 3: Decision

- **High value** (high volume + low/medium competition + low制作 cost) → build immediately
- **Discrepancy found** (existing data is wrong) → fix data, don't build new page
- **Unverified signal** (Reddit only) → log to watchlist, do not ship
- **No new opportunity** → report "no new keywords" and end

---

### Step 4: Page Build

Next.js App Router pattern:
- `PageIntro` component for header
- Metadata: `${monthYear}` in title/description
- `canonical` + OpenGraph + Twitter card
- Breadcrumb schema via `buildBreadcrumbSchema`
- FAQ schema via `buildFaqSchema`
- Dynamic routes: `app/[category]/[slug]/page.tsx`

---

### Step 5: Data Update

**Mode A (single source of truth):** `src/data/site.ts`

For codes specifically — add new codes at the TOP of the array (newest first). Fields: `code`, `reward`, `status`, `addedDate`.

For brainrots — append to `brainrots[]` array in `src/data/site.ts`.

For bases — append to `bases[]` array.

---

### Step 6: Build Verify

```bash
npm run build 2>&1 | tail -20
```
Must show `○` or `●` for all routes. Any `✗` = error, fix before push.

---

### Step 7: Deploy

```bash
git add -A && git commit -m "feat: [描述]" && git push
```
Cloudflare Pages auto-deploys on push to `main`.

---

## Game-Specific Data (be-lucky-block)

See: `references/be-lucky-block-game-data.md`
