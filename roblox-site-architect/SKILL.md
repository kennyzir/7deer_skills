---
name: roblox-site-architect
description: Orchestrate an evidence-backed seven-stage Roblox site growth pipeline from opportunity assessment through keyword research, source collection, site planning, SEO QA, freshness, and growth. Use when work needs staged artifacts and explicit handoffs rather than a one-click site generator.
metadata:
  version: "4.0"
---

# Roblox Site Growth Pipeline

Coordinate research, planning, implementation, validation, and growth work for a Roblox-focused site. This Skill is a workflow orchestrator: it defines stage gates and deliverables, but it does not claim to generate or deploy a complete production site by itself.

## Operating model

The pipeline has seven ordered stages. Each stage writes one durable Markdown artifact under `<project-root>/pipeline/` using the schema in [references/pipeline-contracts.md](references/pipeline-contracts.md). Read that contract before starting or resuming work.

Use a named supporting Skill only when it is available in the current environment and relevant to the request. If it is unavailable, either:

1. produce an equivalent artifact using available capabilities such as searching the web, reading files, and running local commands; or
2. mark the artifact `partial` or `blocked`, record the missing capability and evidence gap, and stop at the affected gate.

Never state that a Skill, tool, build, deployment, submission, or external action ran unless its actual result is available in the current work record.

### Status and progression

- `complete`: all exit criteria are met with cited evidence.
- `partial`: useful work exists, but named gaps remain. Proceed only when those gaps cannot invalidate the next decision.
- `blocked`: a required input, authorization, or capability is absent. Do not advance.

When resuming, inspect existing artifacts in numeric order. Preserve prior evidence, note superseded conclusions, and update timestamps instead of silently rewriting history.

## Inputs

Establish these before Stage 01:

- the Roblox game name or canonical game URL;
- the intended audience, locale, and business objective if known;
- `<project-root>` if a target project already exists;
- the user's requested scope: research only, planning, local implementation, or authorized external release.

Unknown inputs stay explicitly unknown. A game name alone does not authorize building, purchasing, publishing, or outreach.

## Seven-stage pipeline

### 01 Opportunity

**Purpose:** decide whether the game/site opportunity deserves further research.

**Preferred supporting Skill:** `roblox-hit-evaluator` when available.

**Entry criteria**

- A candidate game can be distinguished from similarly named games.
- The evaluation horizon and decision question are stated.

**Work**

- Confirm canonical Roblox identity, developer, creation/release context, and observable activity.
- Measure demand, momentum, content supply, and uncertainty from timestamped public evidence.
- Separate breakout potential from SEO-site viability; they are related but not identical.
- Record counter-evidence and missing observations.

**Artifact:** `<project-root>/pipeline/01-opportunity-report.md`.

**Exit criteria**

- The game identity is unambiguous.
- A `pursue`, `hold`, or `reject` decision is stated with evidence and confidence limits.
- Material unknowns and the next validation action are explicit.
- `blocked` stops the pipeline; `reject` ends it unless the user changes the objective.

### 02 Keywords

**Purpose:** turn the opportunity into a prioritized, non-duplicative search-demand map.

**Preferred supporting Skills:** `site-keyword-research`, `keyword-competition-analysis`, and `google-trends-to-pages` when available and relevant.

**Entry criteria**

- Stage 01 is `complete`, or its remaining gaps do not affect keyword discovery.
- Target locale and game identity are known.

**Work**

- Collect query evidence from current search results, trends, platform language, and target-site coverage.
- Cluster by intent rather than by superficial wording.
- Map each cluster to a proposed page, existing page, or watchlist item.
- Record demand/competition evidence separately from inferred priority.
- Avoid inventing search volume when no measurement source is available.

**Artifact:** `<project-root>/pipeline/02-keyword-map.md`.

**Exit criteria**

- Each priority cluster has intent, evidence, target route or disposition, and rationale.
- Cannibalization and duplicate-page risks are identified.
- P0/P1 work is small enough to implement and trace back to sources.

### 03 Evidence

**Purpose:** assemble a source ledger that can support every factual page claim.

**Preferred supporting Skills:** `roblox-game-data-scraper` for supported public Trello collection, `youtube-transcribe` for supplied or accessible videos, and other relevant evidence Skills when available.

**Entry criteria**

- Priority page intents from Stage 02 are known.
- Required claim types are listed: codes, mechanics, values, steps, dates, or comparisons.

**Work**

- Collect primary sources first; use secondary/community sources as attributed signals.
- Store source URL or stable identifier, publisher, captured time, relevant excerpt/field, and claim supported.
- Reconcile conflicts without averaging incompatible facts.
- Mark volatile claims with a freshness expectation.
- Do not infer a game code, numeric value, redemption step, or mechanic from generic genre conventions.

**Artifact:** `<project-root>/pipeline/03-source-ledger.md`.

**Exit criteria**

- Every planned factual section maps to at least one source or is marked unknown.
- Codes, numeric values, and redemption instructions have explicit support and observation time.
- Conflicts, stale sources, and unsupported page ideas are visible to the next stage.

### 04 Site plan and build

**Purpose:** convert validated demand and evidence into a scoped information architecture and local implementation.

**Preferred supporting Skill:** `multi-game-codes-hub` for its implemented codes-page generator when relevant; otherwise work directly in the target project with its existing framework and conventions.

**Entry criteria**

- Stage 02 identifies target routes and intent.
- Stage 03 supports the facts needed by the initial scope.
- `<project-root>` and local change scope are confirmed before implementation.

**Work**

- Define page purpose, primary query cluster, source dependencies, route, internal-link role, and acceptance checks.
- Prefer the smallest coherent launch scope; do not add generic codes, tier, wiki, or calculator pages without demand and evidence.
- Preserve the target project's design system, data architecture, and build conventions.
- Implement only locally authorized work. Generated content remains a draft until evidence and project checks pass.

**Artifact:** `<project-root>/pipeline/04-site-plan.md`.

**Exit criteria**

- Every planned/built route maps to keyword intent and evidence.
- The artifact distinguishes `planned`, `implemented`, `verified`, and `deferred` routes.
- Local typecheck/build/test outcomes are recorded from real command results.
- Unsupported claims and placeholder content are absent from release candidates.

### 05 SEO QA and deploy

**Purpose:** validate technical/content SEO and determine release readiness; deploy only with authorization.

**Preferred supporting Skills:** `nextjs-seo-foundations`, `nextjs-seo-booster`, and `seo-auditor` when applicable and available.

**Entry criteria**

- Stage 04 defines the release candidate and acceptance checks.
- Required local builds/tests have run or are recorded as gaps.

**Work**

- Check crawlability, indexability, canonical URLs, metadata, structured data, sitemap/robots behavior, internal links, accessibility, and responsive rendering.
- Check that titles and dates do not claim freshness or verification beyond the source ledger.
- Classify findings by severity and retest fixes.
- If deployment or a repository push is requested, obtain explicit authorization immediately before the external action and capture its real result.

**Artifact:** `<project-root>/pipeline/05-seo-audit.md`.

**Exit criteria**

- Blocking SEO/build findings are resolved or explicitly accepted by the user.
- The release decision is `ready`, `not-ready`, or `released` with evidence.
- `released` is used only when a real deployment result and reachable target are available.

### 06 Freshness

**Purpose:** record deployment state and define a maintainable evidence-refresh loop.

**Preferred supporting Skills:** `seo-autopilot` and `auto-page-sync` only when their implemented capabilities match the target project.

**Entry criteria**

- Stage 05 has a release decision.
- Volatile claims and their source cadence are known.

**Work**

- Record the deployed revision/URL and verification time when deployment actually occurred; otherwise record `not deployed`.
- Define which inputs change, how staleness is detected, who reviews changes, and which checks gate publication.
- Prefer pull-request or reviewable update flows for factual content.
- Creating a scheduled task requires explicit authorization; planning one does not.

**Artifact:** `<project-root>/pipeline/06-deployment-report.md`.

**Exit criteria**

- Deployment status is factual and backed by a result, or explicitly `not deployed`.
- Volatile facts have owners/sources, review cadence, and failure behavior.
- Any proposed automation distinguishes planned configuration from active scheduling.

### 07 Growth

**Purpose:** prioritize measurable distribution and authority-building experiments after the site is ready.

**Preferred supporting Skills:** `backlink-discovery`, `seo-link-strategy`, and `seo-backlink-submitter` when available and relevant.

**Entry criteria**

- The target pages are release-ready or released.
- Audience, differentiator, and measurable growth objective are known.

**Work**

- Build a ranked backlog of internal-link, content-gap, partnership, directory, and outreach opportunities.
- Record expected value, evidence, effort, risk, owner, and success metric.
- Separate discovery from execution. A candidate directory or contact is not a completed backlink.
- Draft outreach or submission payloads without sending unless explicitly authorized.

**Artifact:** `<project-root>/pipeline/07-growth-backlog.md`.

**Exit criteria**

- Each backlog item has a target, rationale, next action, metric, and authorization requirement.
- Completed items include a real external result; unexecuted items remain planned.
- Follow-up measurement dates are proposals unless a schedule was actually authorized and created.

## Evidence policy

For every artifact and page claim, label the epistemic state:

- **Fact:** directly supported by a cited source or observed command/tool result.
- **Inference:** a reasoned interpretation that names its supporting facts and uncertainty.
- **Unknown:** missing, conflicting, inaccessible, or too stale to rely on.

Never fill a missing value with a plausible genre default. Game codes, numeric stats, item values, dates, and redemption steps require source-level support. Community consensus must remain attributed as community evidence.

`generated_at` records when an artifact or page was produced. It is not a verification timestamp. Use `observed_at` for when a source was actually checked, and never convert generation time into a claim that content was verified or updated.

## External side-effect boundary

The following actions require the user's explicit authorization for the specific target and action:

- purchasing or registering a domain;
- deploying or publishing a site;
- pushing commits or changing a remote repository;
- creating or enabling a scheduled task;
- sending email or outreach messages;
- submitting a directory listing, backlink request, or external form.

Research, drafts, local files, and dry-run plans do not authorize those effects. Immediately before an authorized action, confirm that the target and payload still match the request. Record the actual result, failure, or uncertainty. Without a real result, use `planned`, `prepared`, `attempted`, or `unknown`—never `deployed`, `sent`, `submitted`, `indexed`, or `completed`.

## Handoffs and stopping rules

- Stop on `blocked`; state the missing input, why it matters, and the smallest user action needed.
- A `partial` artifact may hand off only when its gaps cannot invalidate the next stage; copy those gaps forward.
- Do not skip an artifact because implementation already exists. Reconstruct the artifact from evidence and mark what was observed versus assumed.
- If the user requests only one stage, complete that stage and stop. Do not infer authorization for later stages.

## Legacy references

Historical case studies and earlier execution manuals are isolated under `references/legacy/`. They are not loaded by default, are not current instructions, and may contain stale product assumptions, unsupported metrics, or project-specific architecture. Read a legacy file only when the user explicitly asks for that historical case or when a specific retrospective is needed to explain a decision; validate every claim before reuse.
