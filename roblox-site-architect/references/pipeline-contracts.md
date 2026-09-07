# Roblox Site Growth Pipeline Contracts

Use these contracts for artifacts created by `roblox-site-architect`. They make research and implementation reviewable across agents and tools without assuming a specific framework or service.

## Storage and format

Store the seven Markdown artifacts under `<project-root>/pipeline/`:

1. `01-opportunity-report.md`
2. `02-keyword-map.md`
3. `03-source-ledger.md`
4. `04-site-plan.md`
5. `05-seo-audit.md`
6. `06-deployment-report.md`
7. `07-growth-backlog.md`

Markdown is the canonical format because each stage needs decisions, tables, caveats, and links that remain readable in code review. Use a YAML header for machine-readable handoff metadata and Markdown tables for repeated records.

## Common header

Every artifact begins with this header:

```yaml
---
artifact: 01-opportunity-report
status: partial
game: "Canonical Roblox game name"
scope: "Decision or work covered by this artifact"
generated_at: "2030-01-15T10:30:00Z"
observed_through: "2030-01-15T09:45:00Z"
upstream:
  - "none"
sources:
  - "SRC-001"
gaps:
  - "What is missing and why it matters"
---
```

Required common fields:

| Field | Contract |
|---|---|
| `artifact` | Exact artifact identifier without the `.md` suffix. |
| `status` | Exactly `complete`, `partial`, or `blocked`. |
| `game` | Canonical game name, or `unknown` with a gap. |
| `scope` | The bounded decision/work represented by this file. |
| `generated_at` | UTC ISO-8601 time when the artifact was produced. Not a verification claim. |
| `observed_through` | Latest UTC time actually represented by checked evidence, or `unknown`. |
| `upstream` | Earlier artifact identifiers used, or `none`. |
| `sources` | Source IDs used by conclusions, or an empty list with a gap. |
| `gaps` | Explicit missing/conflicting inputs; empty only when none are material. |

## Status rules

- `complete`: all artifact-specific handoff conditions are satisfied.
- `partial`: the artifact is usable but has named gaps that do not invalidate the permitted handoff.
- `blocked`: a missing input, authorization, or capability prevents a defensible handoff.

An artifact cannot be `complete` when a required table cell is unknown, a required external result is absent, or a blocking finding remains unresolved. Changing status requires updating `generated_at`, the decision narrative, and the handoff section.

## Common body sections

Each artifact contains these sections in order:

1. `## Decision or outcome`
2. `## Evidence and analysis`
3. `## Unknowns and conflicts`
4. `## Handoff`

Facts cite source IDs or command/result IDs. Inferences are labeled. Unknowns are never replaced with plausible values. The handoff states the next permitted stage, carried gaps, and any user authorization still required.

## 01-opportunity-report

Path: `<project-root>/pipeline/01-opportunity-report.md`

Minimum body fields:

| Field | Minimum content |
|---|---|
| Game identity | Roblox URL/ID, canonical title, developer, identity confidence. |
| Evaluation question | Horizon, audience, and decision being made. |
| Demand/momentum | Timestamped measures or `unknown`. |
| Supply/competition | Observed alternatives and content gaps. |
| Supporting evidence | Facts with source IDs and observation times. |
| Counter-evidence | Strongest contrary facts or alternative explanations. |
| Decision | `pursue`, `hold`, or `reject`, with reasoning. |
| Confidence limits | What could change the decision. |

Handoff condition: identity is resolved, the decision is explicit, material unknowns are visible, and a `pursue`/defensible `hold` decision identifies what Stage 02 should research. `reject` closes the pipeline unless scope changes.

## 02-keyword-map

Path: `<project-root>/pipeline/02-keyword-map.md`

Use one row per keyword cluster:

| Field | Minimum content |
|---|---|
| `cluster_id` | Stable local ID. |
| Queries | Representative query plus variants. |
| Locale | Language/region. |
| Intent | User need, not just query syntax. |
| Demand evidence | Source ID, measure, and observation time; never invented volume. |
| Competition evidence | Current result/supply observations and source IDs. |
| Target | Proposed route, existing route, or watchlist. |
| Disposition | `build`, `update`, `merge`, `watch`, or `reject`. |
| Priority | P0/P1/P2 with rationale and uncertainty. |

Handoff condition: priority clusters are non-duplicative, map to a target/disposition, and identify the factual evidence needed by Stage 03.

## 03-source-ledger

Path: `<project-root>/pipeline/03-source-ledger.md`

Use one row per source observation:

| Field | Minimum content |
|---|---|
| `source_id` | Stable ID referenced by all later claims. |
| Source | URL or stable identifier. |
| Publisher/type | Official, primary, secondary, or community. |
| `observed_at` | UTC time the source was actually checked. |
| Evidence captured | Relevant excerpt, field, transcript position, or result. |
| Claim supported | Exact claim scope. |
| Freshness | Volatility and recheck expectation. |
| Reliability/conflict | Limitations, contradictions, and resolution status. |

Also maintain a claim index mapping page/section claims to source IDs. Game codes, numeric values, redemption steps, release dates, and mechanics must appear in that index or remain unknown.

Handoff condition: every factual element required by P0 scope has support or an explicit gap; conflicts and stale observations are not hidden.

## 04-site-plan

Path: `<project-root>/pipeline/04-site-plan.md`

Use one row per route or build unit:

| Field | Minimum content |
|---|---|
| Route/unit | Target route or component/data unit. |
| Purpose | User need and keyword cluster IDs. |
| Evidence | Required source IDs. |
| Content/data contract | Fields and unknown behavior. |
| Internal-link role | Parent/child/related relationship when evidenced. |
| State | `planned`, `implemented`, `verified`, or `deferred`. |
| Acceptance checks | Observable content, type, build, and rendering checks. |
| Local result | Actual command/result ID or `not run`. |

Handoff condition: release scope is bounded, every route traces to demand/evidence, local results are factual, and unsupported placeholder content is excluded.

## 05-seo-audit

Path: `<project-root>/pipeline/05-seo-audit.md`

Use one row per check/finding:

| Field | Minimum content |
|---|---|
| `check_id` | Stable audit ID. |
| Category | Crawl/index, metadata, structured data, content, links, accessibility, performance, or build. |
| Target | Route/file/URL checked. |
| Result | `pass`, `fail`, `not-run`, or `not-applicable`. |
| Severity | Blocking/high/medium/low when failed. |
| Evidence | Actual command/result, rendered observation, or source ID. |
| Remediation/retest | Change and real retest result. |

The decision section is exactly `ready`, `not-ready`, or `released`. `released` requires an authorized deployment result and reachable target; otherwise record readiness only.

Handoff condition: blocking findings are resolved or explicitly accepted, and deployment authorization/result state is unambiguous.

## 06-deployment-report

Path: `<project-root>/pipeline/06-deployment-report.md`

Minimum deployment fields:

| Field | Minimum content |
|---|---|
| Deployment state | `not-deployed`, `attempted`, `failed`, or `deployed`. |
| Revision/build | Commit/revision and real build result, or `unknown`. |
| Target | Authorized environment/URL, or `none`. |
| Deployment result | Provider/command result ID and UTC time, not an inference. |
| Reachability check | Checked URL, UTC time, result, and limitations. |

Use one row per freshness rule:

| Field | Minimum content |
|---|---|
| Claim/data set | What can become stale. |
| Source/owner | Source IDs and responsible reviewer. |
| Recheck trigger | Cadence or event signal. |
| Review gate | Checks required before publication. |
| Failure behavior | Hold, alert, roll back, or mark unknown. |
| Scheduling state | `proposed` or `active` with a real scheduling result. |

Handoff condition: deployment claims match real results, volatile facts have a review loop, and proposed schedules are not represented as active.

## 07-growth-backlog

Path: `<project-root>/pipeline/07-growth-backlog.md`

Use one row per growth item:

| Field | Minimum content |
|---|---|
| `item_id` | Stable backlog ID. |
| Type/target | Internal link, content gap, partner, directory, outreach, or experiment and its target. |
| Evidence/rationale | Source IDs and expected mechanism. |
| Effort/risk | Relative estimate and external-side-effect risk. |
| Next action/owner | Concrete next step and responsible party. |
| Success metric | Observable outcome and measurement window. |
| Authorization | `not-required`, `required`, or authorized result ID. |
| State/result | `planned`, `prepared`, `attempted`, `completed`, or `rejected`; completed needs a real result. |

Handoff condition: priorities are measurable, execution authority is explicit, and no draft, candidate, or attempted submission is mislabeled as a completed backlink or outreach result.

## Cross-artifact traceability

Before marking the pipeline complete, verify these links:

- Stage 02 clusters cite Stage 01 opportunity evidence.
- Stage 03 claims identify the Stage 02 routes/needs they support.
- Stage 04 routes cite cluster IDs and source IDs.
- Stage 05 checks cite Stage 04 release units and real results.
- Stage 06 cites the Stage 05 release decision and any deployment result.
- Stage 07 items cite released/ready routes and measurable objectives.

If a referenced artifact changes materially, mark affected downstream artifacts `partial` until reviewed again. Preserve prior observation times; a new document generation time never refreshes old evidence.
