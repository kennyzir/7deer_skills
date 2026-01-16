---
name: seo-auditor
description: A comprehensive SEO audit framework and checklist for web projects. Includes a reusable checklist template and common validation rules.
---

# SEO Auditor

A battle-tested SEO audit framework extracted from real-world projects. Use this to systematically review any new website or page for SEO compliance.

## Resources Included

1.  **`resources/checklist_template.md`**: A generalized Markdown checklist for auditing any page.
2.  **`resources/audit_rules.js`**: A simple Node.js script to check common SEO issues (H1, Meta Tags, Canonical).

## Usage

### 1. Manual Audit with Checklist
Copy `resources/checklist_template.md` to your project (e.g., `AUDIT-NOTES.md`) and fill it out for each page/sprint.

### 2. Automated Check (Basic)
Run the `audit_rules.js` script against your built HTML files:

```bash
node .agent/skills/seo-auditor/resources/audit_rules.js ./out/index.html
```

This will check for:
*   Missing or multiple `<h1>` tags
*   Missing `<meta name="description">`
*   Missing `<link rel="canonical">`
*   `<title>` length (warn if < 30 or > 70 chars)

## Key Principles (from the Checklist)

1.  **Title**: 50-60 chars, primary keyword first, unique per page.
2.  **Description**: 120-160 chars, include CTA and numbers.
3.  **Canonical URL**: Always set, use trailing slash consistently.
4.  **Structured Data**: Use FAQPage (min 5 questions), HowTo, ItemList as appropriate.
5.  **Internal Links**: Every page should have 3-6 related links. Avoid orphan pages.
