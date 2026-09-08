# Structural Blockers

A blocker is a concrete structural failure, not an aesthetic preference. Record exact evidence and affected query family.

## Fatal structural blockers

### HOME_NO_PRIMARY_PLAYER_JOB

No single player outcome dominates the homepage. The page is only a collection of “codes, wiki, guides, tier list, updates” blocks.

Evidence requirement: title/H1/hero/module hierarchy cannot support one primary job.

### HOME_NO_MAIN_ENGINE

No module creates meaningful L2 or L3 value and no strong first-hour route, checklist, or decision asset acts as the engine.

Evidence requirement: all candidate modules remain L0/L1 or are simple navigation.

### HOME_ENGINE_MISMATCH

The featured engine solves a marginal problem while the page/research clearly shows a different central player decision.

Evidence requirement: compare observed core mechanics/player friction with the engine’s output.

### HOME_KEYWORD_ONLY_MODULE

A module uses a query label but provides neither a usable answer, an explicit status, nor a contextual child route.

Examples: “Codes,” “Tier List,” or “Best Builds” heading followed by generic filler.

### HOME_EMPTY_CODES_PROMISE

The page promises current codes in title, hero, or heading, but contains:

- no actual code;
- no explicit “no active codes” state;
- no clear owner link or check result.

A truthful zero-code status is not a blocker.

### HOME_FAKE_TIER_LIST

A Tier List lacks named rankable entities or actual comparison logic. Ranking only “rare is better than common” does not satisfy the intent.

### HOME_LOW_GAME_SPECIFICITY

More than half of meaningful homepage copy remains reusable after replacing the game name and generic genre nouns.

Machine heuristics are hints; Codex must confirm semantically.

### HOME_NO_L2_OR_L3_GAIN

The homepage contains no decision support beyond facts or navigation. It has no L3 engine and fewer than two strong L2 modules.

### HOME_FULL_CHILD_DUPLICATION

A child-owned complete table, walkthrough, answer block, or database is substantially reproduced on the homepage.

Evidence guidance:

- section token similarity above 0.50 with at least 50 meaningful tokens; or
- manual evidence that both pages complete the same user task with materially the same content.

### HOME_INTENT_OWNER_CONFLICT

A query family has more than one canonical/full owner, or the implementation contradicts the declared mapping.

### HOME_DUPLICATE_FULL_TOOL

The homepage and a child route expose materially the same full inputs, formula/rules, and outputs.

A mini/demo homepage tool linked to a complete child tool is allowed when scope and outputs differ clearly.

### HOME_P0_LINK_MISSING

An essential P0 child intent owner is not linked from the homepage’s main content with a crawlable, descriptive anchor.

### HOME_GENERIC_FALLBACK

The generated homepage silently fell back to a generic welcome/hero/latest-post template because a homepage contract or content asset was missing.

## Non-structural gates

These do not alter structural score, but can block publication.

### HOME_TECH_INELIGIBLE

Examples: failed build/HTTP response, accidental noindex, wrong canonical, missing rendered body, non-crawlable P0 links.

### HOME_FACT_CONSISTENCY_FAIL

Examples: shared code status, entity value, tier, formula, or labels conflict between homepage and child page.

### HOME_RUNTIME_FAIL

Examples: tool outputs never change, form cannot submit, critical content is hidden after failed hydration, or mobile interaction is unusable.

## Severity rules

- Fatal structural blocker → `STRUCTURAL_VERDICT: BLOCKED`.
- Non-fatal weakness without blocker → score normally and create repair order.
- Technical/fact/runtime failure → publication not ready; structural score remains separate.
- Never create multiple blockers for the same root cause merely to exaggerate severity.
