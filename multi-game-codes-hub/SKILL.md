---
name: multi-game-codes-hub
description: Generate a Next.js Roblox codes page from validated JSON using a reusable TSX template. Use when creating or regenerating a single game's active/expired codes page with metadata, copy controls, FAQ, and breadcrumb schema.
metadata:
  keywords: roblox codes, promo codes, game codes, nextjs page generator, faq schema
---

# Multi-Game Codes Hub

Generate one Next.js codes page from explicit game data. The included generator renders a TSX template; it does not discover, monitor, translate, or validate codes against Roblox.

## Implemented resources

- [resources/generate_code_page.py](resources/generate_code_page.py): validates JSON and renders a page.
- [resources/templates/codes_page.tsx](resources/templates/codes_page.tsx): Next.js page template for active/expired codes, redemption guidance, metadata, FAQ, and breadcrumbs.
- [resources/components/CopyButton.tsx](resources/components/CopyButton.tsx): client-side copy control with a fallback.
- [resources/components/CodeTable.tsx](resources/components/CodeTable.tsx): optional reusable code table.
- [resources/schemas/faq_schema.ts](resources/schemas/faq_schema.ts): FAQ, breadcrumb, and item-list schema helpers.
- [USAGE.md](USAGE.md): concise CLI reference.

The generated template imports `@/components/CopyButton`; copy the included component into that alias or change the import for the target project.

## Input contract

```json
{
  "gameName": "Your Bizarre Adventure",
  "gameSlug": "yba",
  "baseUrl": "https://example.com",
  "activeCodes": [
    {
      "code": "CODE123",
      "reward": "50 Spins",
      "expiryDate": "2026-04-30",
      "conditions": "Optional"
    }
  ],
  "expiredCodes": [
    {
      "code": "OLDCODE",
      "reward": "25 Spins"
    }
  ]
}
```

Required top-level fields:

- `gameName`: non-empty string.
- `gameSlug`: lowercase letters/digits separated by single hyphens.
- `baseUrl`: absolute HTTP(S) site URL without credentials, query, or fragment. A trailing slash is normalized away.
- `activeCodes` and `expiredCodes`: arrays when provided; each entry requires non-empty string `code` and `reward`.

`baseUrl` drives canonical and breadcrumb URLs. Never reuse an example domain for a real site.

## Generate a page

From the Skill directory:

```bash
python3 resources/generate_code_page.py \
  --input resources/examples/yba_codes.json \
  --output /tmp/yba-codes-page.tsx
```

The default template is resolved relative to this Skill, so the command also works when the script is invoked from another current working directory. `--input`, `--output`, and an explicitly supplied `--template` retain normal CLI semantics: relative paths resolve from the caller's current directory and absolute paths remain absolute.

To use a custom template:

```bash
python3 resources/generate_code_page.py \
  --input ./game.json \
  --output ./page.tsx \
  --template ./custom-codes-page.tsx
```

Generation uses the current UTC month, year, and date. It fails before writing output if the JSON is invalid, required values are missing, URLs are invalid, or any `{{templateVariable}}` remains unresolved.

## Template variables

- `{{gameName}}`
- `{{gameSlug}}`
- `{{baseUrl}}`
- `{{rewards}}`
- `{{activeCodesData}}`
- `{{expiredCodesData}}`
- `{{lastUpdated}}`
- `{{currentMonth}}`
- `{{currentYear}}`

## Verification

After generation:

1. Confirm the output contains the target `baseUrl` and no unrelated domain.
2. Confirm no `{{...}}` placeholder remains.
3. Copy or adapt the required component imports.
4. Run the target Next.js project's typecheck, lint, and build.
5. Review codes and redemption instructions against a cited primary source; the generator does not verify factual accuracy.

## Roadmap and boundaries

Discord/Twitter monitoring, automatic code validity checks, automatic expiry updates, multilingual generation, community submissions, and deployment automation are not implemented. Treat them as roadmap items only; do not invoke nonexistent scripts such as `discord_code_monitor.py`, `code_validator.py`, `update_codes.py`, or `generate_multilingual.py`.
