---
name: roblox-homepage-ranking-auditor
description: Audit a Roblox or game-site homepage against the RB Auto Golden Homepage model. Use when Codex must inspect a live homepage or repository, identify the primary player job and main engine, score structural ranking potential across eight dimensions, detect empty query modules, weak information gain, root/child intent conflicts, duplicate full tools, generic content, and missing P0 internal links, then return evidence-backed PASS/REMEDIATE/BLOCKED and minimal repair orders. Do not use for generic site-wide SEO audits, backlink analysis, traffic forecasting, or factual accuracy scoring alone.
metadata:
  short-description: Audit golden homepage ranking structure
---

# Roblox Homepage Ranking Auditor

## Objective

Determine whether an existing game-site homepage conforms to the **RB Auto Golden Homepage** model and has strong **homepage structural ranking potential** under a controlled assumption:

- new site;
- zero backlinks and zero domain history;
- no advantage from keyword search volume or game popularity;
- facts are evaluated separately from homepage structure;
- the audit compares what the homepage itself is designed to do, not current rankings.

The primary output is not “good SEO” or “bad SEO.” It is:

1. What player job the homepage owns.
2. What main engine creates non-generic value.
3. Which query families belong to `/` and which belong to child routes.
4. Whether the homepage directly answers, summarizes, routes, or merely names each intent.
5. An eight-dimension structural score out of 100.
6. Structural blockers, separate delivery gates, and minimal repair work orders.

## When This Skill Applies

Use this skill when the user asks Codex to:

- audit a Roblox/game-site homepage for new-site ranking potential;
- judge whether a homepage matches the RB Auto golden model;
- review whether the homepage has a suitable main engine;
- detect a thin, templated, keyword-only, or generic homepage;
- inspect homepage versus child-page intent ownership;
- find homepage/internal-page cannibalization or duplicate calculators;
- produce a homepage score, verdict, and actionable repair plan;
- validate a newly generated RB Auto homepage before launch.

## Do Not Use This Skill For

- backlink, DR, DA, domain-age, or brand-strength analysis;
- estimating current traffic or keyword search volume;
- generic full-site technical SEO audits;
- checking factual accuracy as part of the 100-point structural score;
- evaluating maintainability, future extensibility, or production cost inside the structural score;
- rewarding a page merely for adding “verified,” dates, sources, author bios, or social proof;
- redesigning the whole repository when only the homepage is under review.

## Non-Negotiable Model Boundary

Keep these systems separate:

### A. Homepage Structural Ranking Power — scored 0–100

Measures the homepage model itself:

- main-topic clarity;
- core-intent satisfaction;
- query coverage;
- information gain;
- content depth and specificity;
- topic structure;
- internal-link efficiency;
- search-intent boundary.

### B. Fact Consistency Gate — PASS / FAIL / NOT_CHECKED

Checks whether facts, codes, data, labels, formulas, and child-page values are consistent. It never adds or removes points from the structural score.

### C. Delivery and Runtime Gate — PASS / FAIL / NOT_CHECKED

Checks whether the rendered page, mobile experience, links, and tools actually work. It never adds points to the structural score.

### D. Technical Eligibility Gate — PASS / FAIL / NOT_CHECKED

Checks whether the page is eligible to participate normally in search: successful response/build, indexability, canonical, crawlable content, and crawlable links.

A strong homepage model can receive a high structural score while publication remains blocked by factual, runtime, or technical failure. Do not merge these conclusions.

## Required Audit Modes

Use the strongest available mode. Do not ask the user for information already present in the repository.

1. **Combined mode — preferred**: repository + built HTML/live URL + child routes.
2. **Repository mode**: inspect source, data, route map, and build output.
3. **URL mode**: inspect live rendered homepage and discover same-domain child routes.
4. **HTML snapshot mode**: inspect supplied/exported HTML; mark unavailable gates `NOT_CHECKED`.

## Required Evidence Sources

Before scoring, inspect as many of these as exist:

- homepage source component;
- metadata definition;
- homepage data/content source;
- route manifest or sitemap;
- keyword/page mapping;
- page-generation plan or homepage contract;
- built/exported homepage HTML;
- at least the P0 child pages linked by the homepage;
- the complete tool route if a mini/full tool exists;
- browser/runtime behavior for interactive engines;
- current Git SHA and worktree status for repository audits.

Never score from a screenshot alone when source or HTML is available.

## Required Resources

Read these before completing the corresponding step:

- [references/golden-homepage-model.md](references/golden-homepage-model.md): model, layouts, engines, and intent ownership.
- [references/scoring-rubric.md](references/scoring-rubric.md): exact scoring anchors and thresholds.
- [references/hard-blockers.md](references/hard-blockers.md): blocker definitions and evidence requirements.
- [references/audit-procedure.md](references/audit-procedure.md): repository, HTML, URL, and runtime workflow.
- [references/report-template.md](references/report-template.md): mandatory final report shape.

Use [assets/rubric.yaml](assets/rubric.yaml) as the machine-readable source for weights and thresholds.

## Workflow

### 0. Freeze the Audit Baseline

For a repository audit:

1. Record repository root, branch, HEAD SHA, and worktree status.
2. Do not modify source files in audit-only mode.
3. Record the exact URL, local route, or HTML file being audited.
4. Record the audit timestamp and evidence limitations.
5. If the worktree is dirty, continue read-only unless user requested repairs; never discard, stash, or overwrite unrelated work.

### 1. Locate the Homepage Truth Sources

Search the repository rather than guessing framework paths. Find:

- root route implementation;
- layout and metadata;
- content/data inputs;
- homepage-specific components;
- interactive tools;
- child-route definitions;
- sitemap/navigation/route manifest;
- research artifacts and keyword-to-page mapping.

Create a short source map with file paths and purposes.

### 2. Reconstruct the Intended Homepage Strategy

Infer or read the following, labeling every item as `DECLARED`, `OBSERVED`, or `INFERRED`:

```yaml
game_archetype: rpg-build | simulator-roi | collection-team | trade-value | route-progression | risk-softlock | data-live | other
primary_player_job: one sentence
player_problem: one sentence
main_engine:
  type: build-planner | damage-calculator | value-comparator | trade-comparator | upgrade-roi | rebirth-planner | team-builder | starter-selector | anti-softlock-checklist | first-hour-route | live-stats | database | other | none
  mode: full | mini | route | checklist | data | none
  location: homepage | child-page | both | absent
layout_variant: tool-first | risk-first | route-first | data-first | mixed | generic
```

Rules:

- Choose one primary player job, not a list of all possible intents.
- Select the main engine by the game’s central player decision, not genre name alone.
- A first-hour route or anti-softlock checklist can be a valid main engine; it need not be a calculator.
- If the homepage has no defensible primary job or main engine, state that explicitly. Do not invent one to improve the score.

### 3. Build the Query-Family and Intent-Ownership Map

For every meaningful query family, assign exactly one canonical owner and one homepage treatment:

```yaml
query_family: game-codes
canonical_owner: /codes/
homepage_treatment: primary | direct | summary | status | link-only | excluded
answer_depth: full | partial | status-only | none
evidence: selector, source path, or excerpt
```

Use these definitions:

- `primary`: the homepage is the definitive destination.
- `direct`: homepage gives a complete usable answer for a compact intent.
- `summary`: homepage gives a useful conclusion plus a reason to visit the child owner.
- `status`: homepage gives a current state, such as “3 active codes” or “none active.”
- `link-only`: contextual, descriptive route only; not counted as a direct answer.
- `excluded`: intentionally absent from the homepage.

Every query family must have one owner. Do not let both `/` and a child route own the same complete intent.

### 4. Run the Deterministic Evidence Scanner

Use the included scanner where possible:

```bash
python .agents/skills/roblox-homepage-ranking-auditor/scripts/audit_homepage.py \
  --url "https://example.com/" \
  --game-name "Example Game" \
  --child-url "https://example.com/codes/" \
  --child-url "https://example.com/tier-list/" \
  --output "artifacts/homepage-audit/homepage_machine_evidence.json"
```

For exported HTML:

```bash
python .agents/skills/roblox-homepage-ranking-auditor/scripts/audit_homepage.py \
  --html "out/index.html" \
  --game-name "Example Game" \
  --child-html "out/codes/index.html" \
  --child-html "out/tier-list/index.html" \
  --output "artifacts/homepage-audit/homepage_machine_evidence.json"
```

The scanner supplies evidence and warnings. It does **not** replace semantic scoring. Review every machine flag before accepting it.

### 5. Apply the Technical Eligibility Gate

Evaluate separately:

- HTTP/build success;
- no accidental `noindex`;
- root canonical is correct;
- primary content exists in rendered HTML;
- P0 internal links are crawlable anchors;
- mobile and desktop do not intentionally expose different core content;
- no redirect or client-only failure hides the homepage.

Do not continue to a publish-ready verdict if this gate fails, but still complete the structural audit when evidence permits.

### 6. Score the Eight Structural Dimensions

Use [references/scoring-rubric.md](references/scoring-rubric.md).

For each dimension:

1. assign a raw rating from 0 to 5 in 0.5 increments;
2. cite at least one concrete positive or negative evidence item;
3. calculate `weighted_score = raw_rating / 5 × weight`;
4. state the single most important reason for the score;
5. do not reward claims that are unsupported by rendered content or working behavior.

Weights:

| Dimension | Weight |
|---|---:|
| Main-topic clarity | 10 |
| Core-intent satisfaction | 20 |
| Query coverage | 14 |
| Information gain | 18 |
| Content depth and specificity | 14 |
| Topic structure | 8 |
| Internal-link efficiency | 10 |
| Search-intent boundary | 6 |
| **Total** | **100** |

### 7. Apply the Genericity Test

Perform both tests:

#### Game-name deletion test

Mentally replace the game name with `[GAME]`. Determine how much meaningful body copy could be reused unchanged for unrelated games in the same genre.

#### Entity/mechanic density test

Count whether the page contains concrete:

- named entities;
- mechanics;
- steps;
- conditions;
- choices;
- numerical relationships;
- consequences;
- exceptions;
- personalized outputs.

Do not confuse long copy with depth.

### 8. Detect Structural Blockers

Apply [references/hard-blockers.md](references/hard-blockers.md). Each blocker requires evidence. Never create a blocker from aesthetics or personal preference.

At minimum check:

- missing primary player job;
- missing or mismatched main engine;
- keyword-only modules;
- empty Codes promise;
- fake Tier List;
- low game specificity;
- full homepage/child duplication;
- intent-owner conflict;
- duplicate full tool;
- missing P0 homepage links;
- generic fallback homepage;
- absence of meaningful L2/L3 information gain.

### 9. Apply the Separate Gates

#### Fact Consistency Gate

Compare shared facts and structures across homepage and child pages. Output only `PASS`, `FAIL`, or `NOT_CHECKED` with evidence. Do not change structural points.

#### Delivery and Runtime Gate

Test tools, forms, buttons, responsive layout, and rendered output. Output only `PASS`, `FAIL`, or `NOT_CHECKED` with evidence. Do not add structural points for normal functionality.

### 10. Determine Verdicts

#### Structural verdict

- `PASS`: score ≥ 85, no structural blocker, core intent ≥ 17/20, information gain ≥ 14/18, intent boundary ≥ 5/6, main-topic clarity ≥ 8/10.
- `REMEDIATE`: score 75–84.99, or total ≥ 85 but a required subscore misses threshold, with no fatal structural blocker.
- `BLOCKED`: score < 75 or any fatal structural blocker.

#### Publication verdict

- `READY`: structural verdict is PASS and all three gates are PASS.
- `NOT_READY`: any gate FAIL or structural verdict REMEDIATE/BLOCKED.
- `NOT_VERIFIED`: structural audit completed but one or more required publication gates are NOT_CHECKED.

### 11. Produce Minimal Repair Work Orders

In audit-only mode, do not edit code. Output repair work orders.

Each work order must solve one core homepage problem and contain:

```yaml
id: HOME-REPAIR-001
priority: P0 | P1 | P2
problem_code: HOME_DUPLICATE_FULL_TOOL
user_result: one visible outcome
allowed_files: explicit paths or discovery rule
must_preserve: explicit existing blocks/behavior
change: precise minimal change
acceptance_criteria: testable conditions
tests: commands and browser checks
out_of_scope: explicit exclusions
```

Follow scope-cutting rules:

- one work order, one core user/search problem;
- do not introduce a new framework;
- do not rewrite correct blocks;
- do not create generic abstractions before repeated need;
- do not bundle site-wide redesign into homepage repair;
- P0 repairs first; defer optional polish.

### 12. Write Mandatory Outputs

Create:

```text
artifacts/homepage-audit/
├── homepage_audit.md
├── homepage_audit.json
├── homepage_machine_evidence.json
└── homepage_repair_orders.json
```

Use [assets/homepage_audit.schema.json](assets/homepage_audit.schema.json) for JSON shape and [references/report-template.md](references/report-template.md) for the human report.

## Audit Confidence

Report `audit_confidence` separately from structural score. It measures evidence completeness, not homepage quality.

Suggested evidence coverage:

- live or exported rendered HTML: 25;
- homepage source and data inputs: 20;
- child routes inspected: 15;
- build/runtime interaction tested: 15;
- keyword/page mapping or homepage plan inspected: 10;
- internal link and route manifest inspected: 10;
- mobile viewport inspected: 5.

Do not shrink or inflate the structural score based on audit confidence. State limitations instead.

## Completion Contract

The audit is incomplete unless the final response contains:

1. `STRUCTURAL_VERDICT`.
2. `STRUCTURAL_SCORE / 100`.
3. `PUBLICATION_VERDICT`.
4. Reconstructed primary player job and main engine.
5. Eight-dimension score table with evidence.
6. Root/child intent-ownership map.
7. Structural blockers with exact evidence.
8. Separate technical, factual, and runtime gates.
9. The three highest-leverage repairs in priority order.
10. Machine-readable artifact paths or an explicit statement that artifact creation was impossible.

Never end with a generic list of SEO suggestions.
