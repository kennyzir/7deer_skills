---
name: seo-auditor
description: "Runs SEO audits on web pages — checks meta tags, validates structured data, reviews heading hierarchy, audits canonical URLs, and verifies performance. Use when the user asks for an SEO audit, site audit, search engine optimization check, on-page SEO review, or technical SEO analysis of a page or website."
---

# SEO Auditor

A battle-tested SEO audit framework extracted from real-world high-traffic projects.

## Resources

1.  **[resources/seo_standards.md](resources/seo_standards.md)**: Detailed guidelines on Metadata, Schema, Content, and Performance standards.
2.  **[resources/checklist_template.md](resources/checklist_template.md)**: Markdown checklist for auditing any page.
3.  **[resources/audit_rules.js](resources/audit_rules.js)**: Node.js script to check common SEO issues (H1, Meta Tags, Canonical).

## Workflow

### 1. Manual Audit
For every significant page update or new feature:

1.  **Read the Standards**: Review `resources/seo_standards.md`.
2.  **Create a Checklist**: Copy `resources/checklist_template.md` to your project (e.g., `docs/audits/PAGE_NAME_AUDIT.md`).
3.  **Verify & Check**: Go through each item — verify it against the standards.
4.  **Cross-check**: Run the automated check (below) and fix any issues it catches. Re-audit affected items.

### 2. Automated Check
Run `audit_rules.js` against built HTML files:

```bash
node .agent/skills/seo-auditor/resources/audit_rules.js ./out/index.html
```

Example output (pass):
```
✓ H1 tag found: "Best AI Tools for 2026"
✓ Meta description found (142 chars)
✓ Canonical URL set: https://example.com/ai-tools/
```

Example output (fail):
```
✗ Missing H1 tag
✗ Meta description too short (28 chars, minimum 50)
✓ Canonical URL set: https://example.com/page/
```

Fix any failures, then re-run the script to confirm resolution.

## Quick Reference (Top 5 Rules)

1.  **Title**: 50-60 chars, unique, dynamic date (e.g. "(June 2026)").
2.  **Canonical**: ALWAYS set, ALWAYS use trailing slash (`/path/`).
3.  **Schema**: Use `FAQPage` (5+ Qs) or `HowTo` to capture rich results.
4.  **Internal Links**: Every page needs 3-6 outgoing links in a "Related" section.
5.  **Performance**: HTML size < 150KB, use `<Image>` component.
