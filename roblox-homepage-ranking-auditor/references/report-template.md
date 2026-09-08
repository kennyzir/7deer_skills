# Homepage Golden Model Audit — <site/game>

## 1. Final verdict

```text
STRUCTURAL_VERDICT: PASS | REMEDIATE | BLOCKED
STRUCTURAL_SCORE: 0.0 / 100
PUBLICATION_VERDICT: READY | NOT_READY | NOT_VERIFIED
AUDIT_CONFIDENCE: 0 / 100
```

One-paragraph answer: Is this homepage structurally capable of acting as the root search product for a zero-authority new site, and what is the decisive reason?

## 2. Audit scope and baseline

| Item | Value |
|---|---|
| Target URL/route | |
| Repository | |
| Branch / SHA | |
| Worktree | clean / dirty / unavailable |
| Evidence mode | combined / repository / URL / HTML |
| Build/runtime tested | yes / no |
| Child routes inspected | |
| Limitations | |

## 3. Reconstructed homepage strategy

```yaml
game_archetype:
primary_player_job:
player_problem:
main_engine:
  type:
  mode:
  location:
layout_variant:
strategy_basis: DECLARED | OBSERVED | INFERRED
```

## 4. Eight-dimension scorecard

| Dimension | Raw /5 | Weighted | Evidence | Main reason |
|---|---:|---:|---|---|
| Main-topic clarity | | /10 | | |
| Core-intent satisfaction | | /20 | | |
| Query coverage | | /14 | | |
| Information gain | | /18 | | |
| Content depth and specificity | | /14 | | |
| Topic structure | | /8 | | |
| Internal-link efficiency | | /10 | | |
| Search-intent boundary | | /6 | | |
| **Total** | | **/100** | | |

## 5. Query-family ownership map

| Query family | Relevance | Canonical owner | Homepage treatment | Direct answer | Evidence | Conflict |
|---|---|---|---|---|---|---|

## 6. Main-engine assessment

- Engine fit:
- What input/action the user performs:
- What result the user receives:
- Why it is or is not L3 information gain:
- Correct owner: homepage / child page:
- Duplicate-tool finding:

## 7. Structural blockers

| Code | Severity | Evidence | Affected user/search result |
|---|---|---|---|

Write `NONE` when there are no blockers.

## 8. Separate publication gates

| Gate | Result | Evidence | Effect |
|---|---|---|---|
| Technical eligibility | PASS/FAIL/NOT_CHECKED | | publication only |
| Fact consistency | PASS/FAIL/NOT_CHECKED | | publication only |
| Delivery/runtime | PASS/FAIL/NOT_CHECKED | | publication only |

## 9. What is already strong

Name only structural strengths supported by evidence. Do not reward backlinks, traffic, dates, or generic claims.

## 10. Highest-leverage failures

Rank the three issues that most reduce the homepage’s ability to satisfy intent or route the site.

## 11. Minimal repair work orders

For each P0/P1 repair include:

```yaml
id:
priority:
problem_code:
user_result:
allowed_files:
must_preserve:
change:
acceptance_criteria:
tests:
out_of_scope:
```

## 12. Final decision

State exactly one:

- Ready to publish under the golden homepage model.
- Structurally promising but requires listed repairs before publication.
- Structurally blocked; do not publish this homepage as the site root.
- Structural audit complete, but publication cannot be verified without missing gate evidence.
