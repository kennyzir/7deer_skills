# Audit Procedure

## 1. Repository discovery

Record:

```bash
git rev-parse --show-toplevel
git branch --show-current
git rev-parse HEAD
git status --short
```

Search for the root route and metadata using repository-aware commands rather than assuming a framework:

```bash
find . -maxdepth 4 -type f \( -name 'page.*' -o -name 'index.*' -o -name 'routes.*' -o -name 'sitemap.*' \)
rg -n "metadata|canonical|homepage|homePage|hero|calculator|planner|tier list|codes" .
```

Identify:

- homepage source;
- data inputs;
- shared components;
- main-engine implementation;
- child pages;
- sitemap/route manifest;
- keyword-page mapping or research artifacts;
- build/export commands.

## 2. Rendered evidence

Prefer the project’s documented build command. Do not invent a migration or dependency upgrade.

Typical checks:

```bash
npm test
npm run build
```

Locate generated HTML and run the machine scanner. If the framework has no static export, use a local server and URL mode.

## 3. URL inspection

Capture:

- response status;
- final URL after redirects;
- title, meta description, robots, canonical;
- H1/H2/H3 hierarchy;
- visible module order;
- forms, fields, buttons, and output regions;
- main-content internal links and anchors;
- child-route content for overlapping intents.

Do not infer rendered content solely from source conditionals.

## 4. Runtime inspection

For an interactive engine:

1. record default state;
2. enter a valid input set;
3. trigger calculation/selection;
4. confirm the result changes meaningfully;
5. enter invalid or boundary input;
6. confirm error handling;
7. repeat at mobile viewport;
8. capture selectors/screenshots/logs when available.

Normal functionality is a gate, not a structural bonus.

## 5. Intent-boundary inspection

For every child-owned query family:

1. identify homepage section;
2. identify child owner;
3. compare headings, tables, steps, FAQ, and tool inputs/outputs;
4. determine whether homepage is summary/status/link-only or a second full answer;
5. record similarity evidence and ownership conclusion.

Use the scanner’s section similarity output as a lead, not the final verdict.

## 6. Genericity inspection

Remove or mentally replace:

- game name;
- “Roblox”;
- generic nouns such as pet, boss, coins, upgrade, powerful.

Mark each meaningful paragraph:

```text
L0 generic
L1 game-specific fact
L2 decision support
L3 computed/personalized output
```

Report the approximate L0 share. Do not treat navigation labels, legal footer, or boilerplate as meaningful body paragraphs.

## 7. Source-to-render reconciliation

For every claimed required block, prove three layers where possible:

```text
source/data exists
→ component consumes it
→ built/live HTML exposes it
```

A JSON object or JSX component that never appears in the rendered homepage is not homepage evidence.

## 8. Output directory

```bash
mkdir -p artifacts/homepage-audit
```

Write:

- `homepage_machine_evidence.json` from scanner;
- `homepage_audit.json` from semantic audit;
- `homepage_audit.md` for the user;
- `homepage_repair_orders.json` when repairs are needed.

## 9. Audit-only safety

Unless the user explicitly asks for changes:

- do not edit source;
- do not install a new framework;
- do not update dependencies beyond what is needed to run the included scanner in an isolated environment;
- do not commit, push, merge, or deploy;
- do not delete generated files that predate the audit.
