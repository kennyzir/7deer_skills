# RB Auto Golden Homepage Model

## Table of contents

1. Purpose
2. Core model
3. Primary player job
4. Main engine
5. Layout variants
6. Query treatment and intent ownership
7. Homepage content budget
8. Strong and weak patterns

## 1. Purpose

The homepage is the root search product of a new game site. It must do more than introduce the game or list recent posts. It should:

1. make the game and page purpose immediately understandable;
2. solve one central player job directly;
3. provide non-generic information gain;
4. organize the site into player-task hubs;
5. transfer attention and internal authority to the right child pages;
6. preserve one canonical owner for each search intent.

The model evaluates a controlled new-site scenario. Do not use external authority, current traffic, domain age, backlinks, or keyword volume in the structural score.

## 2. Core model

A golden homepage contains these conceptual layers. The exact UI may differ.

```text
1. Hero
   Game entity + page purpose + one player promise

2. Immediate utility
   Main engine: calculator, planner, comparator, checklist,
   first-hour route, live data, or a comparable decision asset

3. Critical answers
   Two or three immediate high-value answers

4. Core gameplay loop
   Game-specific mechanics, steps, and outcomes

5. One deep differentiator
   The single issue the homepage answers better than ordinary wikis

6. Task hubs
   Four to six routes organized by player state or next decision

7. Focused FAQ
   Real decision questions, not keyword paraphrases

8. Full guide map
   Important child intent owners reachable from the homepage
```

This is a model, not a fixed visual template. A homepage may merge sections when the player journey remains clear.

## 3. Primary player job

The primary player job is one sentence describing the main progress a player should make on the homepage.

Strong examples:

- Plan a viable build before spending irreversible stat points.
- Choose the best affordable upgrade before rebirthing.
- Avoid the three choices that can lock a class route.
- Decide which starter and early route to use in the first 30 minutes.
- Compare trade values before accepting an exchange.
- Build a team that covers the next boss’s weaknesses.

Weak examples:

- Learn everything about the game.
- Find guides, codes, tier lists, and more.
- Explore the ultimate wiki.
- Become the best player.

A homepage may support many secondary intents, but it must have only one dominant primary job.

## 4. Main engine

The main engine is the homepage mechanism that creates specific player value. It is selected by the game’s central decision, not the genre label alone.

### Valid engine families

| Engine | Suitable player problem | Typical output |
|---|---|---|
| Build Planner | Stat/class/weapon allocation | Viable build and trade-offs |
| Damage Calculator | Combo or threshold decision | DPS, hits-to-kill, breakpoints |
| Value/Trade Comparator | Exchange uncertainty | Relative value and fairness |
| Upgrade/Rebirth ROI | Resource allocation | Payback, priority, next upgrade |
| Team Builder | Coverage and composition | Gaps, synergies, replacements |
| Starter Selector | Irreversible early choice | Recommended starter and route |
| Anti-Softlock Checklist | Permanent or costly mistakes | Safe prerequisites and warnings |
| First-Hour Route | Unclear progression | Ordered actions and milestones |
| Live Stats/Data | Dynamic entity state | Current snapshot and comparisons |
| Database/Search | Entity discovery | Filtered, structured answer set |

### Engine fit questions

- Is the engine tied to a central mechanic?
- Does it help with an important decision?
- Does it produce a result that generic prose cannot?
- Will a player use it at a meaningful moment?
- Is it suitable for the homepage, or should the full version live on a child route?

A visual widget with no meaningful input, comparison, or decision output is not a main engine.

## 5. Layout variants

### Tool-first

Use when an interactive utility is the strongest differentiator.

```text
Hero → Main engine → Result explanation → Critical answers
→ Core loop → Task hubs → Guide map
```

### Risk-first

Use when players can make costly or irreversible mistakes.

```text
Hero warning → Critical risk → Checklist/safe route
→ Build/class/weapon hubs → Guide map
```

### Route-first

Use when the game is new, data is sparse, or progression confusion dominates.

```text
Hero → Choose current problem → First-hour route
→ Codes/controls/starter → Progression hubs → Guide map
```

### Data-first

Use when reliable dynamic or structured game data is the asset.

```text
Hero → Live snapshot → Current decision module
→ Database → Task hubs → Updates → Guide map
```

### Mixed

Use only when one engine remains clearly dominant. A page that gives equal visual weight to codes, tier list, news, calculator, wiki, and blog posts is usually generic, not mixed.

## 6. Query treatment and intent ownership

Every query family has one canonical owner.

### Homepage treatment levels

| Treatment | Meaning | Coverage value guidance |
|---|---|---:|
| primary | `/` is the definitive destination | 1.0 |
| direct | complete compact answer on `/` | 1.0 |
| summary | useful conclusion + descriptive child link | 0.6 |
| status | current state + child owner link | 0.5 |
| link-only | contextual route without answer | 0.25 |
| keyword-only | heading or phrase with no useful answer | 0 |
| excluded | intentionally absent | 0 |

Coverage value is diagnostic, not the full 14-point query-coverage score.

### Root-owned intents

Typical root-owned families:

- game entity/name;
- game wiki or guide hub;
- the selected homepage main-engine query family.

### Child-owned intents

Typical child owners:

- complete codes list;
- full tier list;
- full progression walkthrough;
- complete weapons/items/classes database;
- detailed boss, NPC, or map guide;
- full calculator when homepage contains only a mini version.

### Full-tool rule

Choose one:

```text
A. Full tool on homepage; no duplicate tool page.
B. Mini/demo on homepage; full tool on one child route.
```

Never keep materially identical full inputs, formulas, and outputs on both `/` and a child page.

### Summary rule

A child-owned intent may appear on the homepage as:

```text
clear conclusion
+ 3–5 representative items
+ reason to continue
+ descriptive internal link
```

Do not copy the child page’s full table, full walkthrough, or full answer block.

## 7. Homepage content budget

A focused homepage normally contains:

- 1 primary player job;
- 1 main engine;
- 2–3 critical direct answers;
- 1 full core-loop explanation;
- 1 deep differentiator;
- 4–6 task hubs;
- 3–5 representative entities per summarized child intent;
- 1 complete guide map.

This budget is not a word-count limit. It prevents the homepage from becoming eight complete child pages joined together.

## 8. Strong and weak patterns

### Strong

- The first viewport names the game, player problem, and useful action.
- The main engine appears early and produces a real decision result.
- The core loop uses named mechanics and consequences.
- Every major child page is linked with descriptive context.
- Homepage summaries and child pages have visibly different jobs.
- Query coverage comes from usable answers, not headings.

### Weak

- “Welcome to the ultimate wiki” is the only proposition.
- Latest posts dominate the homepage.
- A Codes section contains no code or explicit no-code status.
- A Tier List ranks only rarity labels without named units.
- Advice remains valid after replacing the game name with another title.
- A full calculator, tier list, or progression guide is duplicated on a child route.
- Every card uses “Read more” without explaining the target decision.
