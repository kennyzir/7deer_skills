---
artifact: 02-keyword-map
status: blocked
game: @@GAME_JSON@@
scope: @@SCOPE_JSON@@
generated_at: @@GENERATED_AT_JSON@@
observed_through: unknown
upstream:
  - "01-opportunity-report"
sources: []
gaps:
  - "Missing completed or defensible handoff from 01-opportunity-report."
---

## Decision or outcome

Blocked pending the Stage 01 opportunity handoff.

## Evidence and analysis

| cluster_id | Queries | Locale | Intent | Demand evidence | Competition evidence | Target | Disposition | Priority |
|---|---|---|---|---|---|---|---|---|
| Unassigned | Unknown | Unknown | Unknown | None collected | None collected | Unknown | Pending | Pending |

## Unknowns and conflicts

- Keyword demand, competition, intent, and target mapping remain unknown.

## Handoff

| Next stage | Permitted when | Carried gaps | Authorization |
|---|---|---|---|
| 03-source-ledger | Priority clusters are non-duplicative and have targets, dispositions, and evidence needs. | All unresolved keyword gaps. | Not required for offline research. |
