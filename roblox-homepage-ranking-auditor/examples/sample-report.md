# Homepage Golden Model Audit — Example Game

```text
STRUCTURAL_VERDICT: REMEDIATE
STRUCTURAL_SCORE: 81.2 / 100
PUBLICATION_VERDICT: NOT_READY
AUDIT_CONFIDENCE: 92 / 100
```

The homepage has a clear build-planning engine and strong internal routes, but the complete calculator is duplicated on `/calculator/`, and the Codes block names the intent without returning a code or explicit zero-code status.

## Strategy

```yaml
game_archetype: rpg-build
primary_player_job: Plan a viable build before spending stat points.
player_problem: Players cannot see whether stats meet weapon and survival thresholds.
main_engine:
  type: build-planner
  mode: full
  location: both
layout_variant: tool-first
strategy_basis: OBSERVED
```

## Decisive blockers

- `HOME_DUPLICATE_FULL_TOOL`: `/` and `/calculator/` expose the same inputs and outputs.
- `HOME_EMPTY_CODES_PROMISE`: homepage shows “Codes” but gives neither codes nor an explicit no-active-codes state.

## Minimal P0 repair

Move the complete calculator ownership to `/`; remove the duplicate child implementation or redirect it to `/#build-planner`. Preserve the homepage hero, build results, and existing child content unrelated to the calculator.
