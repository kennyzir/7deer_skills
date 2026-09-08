# Homepage Structural Ranking Power Rubric

## Table of contents

1. Scoring method
2. Required thresholds
3. Dimension anchors
4. Information-gain levels
5. Query-coverage method
6. Evidence rules

## 1. Scoring method

Rate each dimension from `0` to `5` in `0.5` increments.

```text
weighted_score = raw_rating / 5 × dimension_weight
```

Do not use unsupported precision. Show raw rating, weighted score, evidence, and the main reason.

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
| Total | 100 |

## 2. Required thresholds

Structural PASS requires all of the following:

```text
total >= 85
main_topic_clarity >= 8/10
core_intent_satisfaction >= 17/20
information_gain >= 14/18
search_intent_boundary >= 5/6
structural_blockers == 0
```

A high total cannot hide a failed primary job, weak information gain, or root/child conflict.

## 3. Dimension anchors

### 3.1 Main-topic clarity — 10

Question: Can a user and search system identify the game, page purpose, primary player problem, and next action from the prominent area?

| Raw | Anchor |
|---:|---|
| 0 | Wrong/unclear entity or no meaningful homepage purpose. |
| 1 | Game name appears, but proposition is only generic “wiki/guide.” |
| 2 | Game and broad page type are clear; primary task remains ambiguous or buried. |
| 3 | First viewport clearly states game plus one useful page purpose. |
| 4 | Entity, primary player problem, promise, and next action align across title/H1/hero. |
| 5 | One dominant proposition is unmistakable; supporting modules reinforce rather than compete with it. |

Cap at 3 when title/H1/hero make materially different promises.

### 3.2 Core-intent satisfaction — 20

Question: Does the homepage actually help the largest/most important player job rather than merely naming it?

| Raw | Anchor |
|---:|---|
| 0 | No defensible primary player job. |
| 1 | A list of topics or links; no answer or useful action. |
| 2 | Problem is named, but answer is generic, shallow, or buried. |
| 3 | Player receives a usable answer, route, checklist, status, or mini-tool. |
| 4 | Homepage completes a meaningful high-impact player task with clear output or decision support. |
| 5 | The main engine solves a central, costly, repeated, or urgent decision and dominates the page journey. |

Cap at 2 when the purported main engine is decorative or non-functional by design.

### 3.3 Query coverage — 14

Question: How many valid search-intent families are meaningfully handled without diluting the page?

| Raw | Anchor |
|---:|---|
| 0 | No identifiable query family beyond accidental text. |
| 1 | Game-name/entity intent only, or several keyword-only headings. |
| 2 | Two to three families receive weak answers or context-free links. |
| 3 | Four to six relevant families receive direct, summary, status, or contextual treatment. |
| 4 | Six to nine relevant families are useful and mapped to clear owners. |
| 5 | Broad but disciplined coverage: the core family is strong, secondary families are useful, and no family exists merely to stuff keywords. |

Do not count `keyword-only` treatment. Do not reward irrelevant breadth.

### 3.4 Information gain — 18

Question: What can the user learn, calculate, compare, decide, or do here that an ordinary generic wiki introduction does not provide?

| Raw | Anchor |
|---:|---|
| 0 | Only L0 generic statements. |
| 1 | Mostly L0 with isolated names or facts. |
| 2 | Consistent L1 specificity but little decision support. |
| 3 | Multiple L1 assets plus at least one useful L2 comparison, priority, route, or consequence. |
| 4 | One strong L2 engine or a lightweight but real L3 utility/data interaction. |
| 5 | One validated L3 engine that produces a meaningful result, or multiple strong L2 assets forming an uncommon decision product. |

Do not reward a visual widget that returns no meaningful result.

### 3.5 Content depth and specificity — 14

Question: Does the homepage explain this game’s actual mechanics rather than expanding genre-level common sense?

| Raw | Anchor |
|---:|---|
| 0 | Nearly all meaningful copy is generic. |
| 1 | Game name and genre nouns are substituted into reusable advice. |
| 2 | Some named entities and steps exist, but mechanisms and conditions remain vague. |
| 3 | Explains actual mechanics, ordered steps, requirements, or outcomes. |
| 4 | Adds choices, priorities, conditions, trade-offs, consequences, and concrete examples. |
| 5 | High density of game-specific entities and relationships, including exceptions or decision thresholds, with little filler. |

If more than half of meaningful paragraphs survive the game-name deletion test, cap at 2.

### 3.6 Topic structure — 8

Question: Do headings and modules form a coherent player journey and semantic hierarchy?

| Raw | Anchor |
|---:|---|
| 0 | No usable hierarchy or unrelated page blocks. |
| 1 | Section sprawl, repeated H1s, or blog-feed dominance. |
| 2 | Headings exist but order follows template slots rather than player decisions. |
| 3 | Logical hierarchy with a visible main engine and relevant supporting sections. |
| 4 | Sections follow player state: promise → action → explanation → next decisions. |
| 5 | The entire hierarchy reinforces one primary job while secondary hubs remain easy to scan. |

### 3.7 Internal-link efficiency — 10

Question: Does the homepage transfer users and internal authority to the site’s most important child intent owners?

| Raw | Anchor |
|---:|---|
| 0 | No usable internal links, broken links, or script-only navigation. |
| 1 | Mostly generic anchors, footer links, or latest-post cards. |
| 2 | Some important pages linked, but P0 coverage or context is weak. |
| 3 | At least 80% of P0 routes are linked contextually with descriptive anchors. |
| 4 | 100% of P0 routes are one click away in main content and links explain the next player decision. |
| 5 | Links are prioritized by player state, avoid orphaning, and create a clear hub-to-cluster graph without clutter. |

A link existing only in global footer/navigation does not prove a strong homepage hub.

### 3.8 Search-intent boundary — 6

Question: Are root and child pages assigned distinct jobs with one canonical owner for every query family?

| Raw | Anchor |
|---:|---|
| 0 | Same full tool/content appears on `/` and child page, or ownership is fundamentally contradictory. |
| 1 | Multiple query families have two full owners. |
| 2 | Substantial copied tables, walkthroughs, or answers create likely competition. |
| 3 | Most owners are clear; minor duplication or ambiguous treatment remains. |
| 4 | Homepage summarizes child-owned intents and fully owns only the root/main-engine families. |
| 5 | Every family has one owner, overlap stays within budget, and full-tool routing is unambiguous. |

## 4. Information-gain levels

| Level | Definition | Examples |
|---|---|---|
| L0 | Genre-level common sense | “Upgrade to become stronger.” |
| L1 | Concrete game-specific facts and steps | Named NPC, item, requirement, route step. |
| L2 | Decision support | Priority, comparison, consequence, safe route, threshold. |
| L3 | Computed or personalized result | Calculator, planner, comparator, queryable database, team analysis. |

Minimum expectation:

```text
one L3 module
OR, when a valid L3 engine is not possible, at least two strong L2 modules
```

## 5. Query-coverage method

Create a query-family ledger before assigning the 14-point score.

Suggested fields:

```text
family
relevance
canonical_owner
homepage_treatment
direct_answer_present
descriptive_link_present
evidence
```

Diagnostic treatment values:

```text
primary/direct = 1.0
summary = 0.6
status = 0.5
link-only = 0.25
keyword-only/excluded = 0
```

Use the sum to compare coverage quality, but apply expert judgment for relevance and dilution. A page should not gain by adding dozens of marginal query families.

## 6. Evidence rules

- Every dimension needs at least one concrete evidence item.
- Ratings above 4 require rendered-page evidence, not source intention alone.
- Information-gain rating 5 requires working behavior or a complete rendered data asset.
- Internal-link rating above 3 requires inspection of actual `href` targets.
- Intent-boundary rating above 3 requires inspection of relevant child pages or a trustworthy route/content contract.
- When evidence is missing, keep the structural judgment based on observed structure and lower `audit_confidence`; do not automatically reduce the score merely because evidence is unavailable.
