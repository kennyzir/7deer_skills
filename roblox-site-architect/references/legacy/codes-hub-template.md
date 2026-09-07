# Multi-Game Codes Hub Template

Originally from `multi-game-codes-hub` skill. Consolidated into `roblox-site-architect` umbrella.

Rapidly create complete, SEO-optimized code pages for any Roblox game in ~5 minutes.

## Page Structure
1. Hero (H1 + timestamp)
2. Active Codes table (green badge + copy button)
3. How to Redeem guide
4. Expired Codes table (grey)
5. FAQ (Schema)
6. Related Content links

## Component Library
- `CopyButton.tsx` — client-side clipboard with feedback
- `CodeTable.tsx` — active/expired status variants
- `FAQSchema` generator

## Multilingual
EN, ES, PT, RU with hreflang tags

## SEO Checklist
- H1 with game name + "Codes"
- Meta with "free/working/YYYY"
- 3+ internal links
- FAQ schema
- OG image
- "Last Updated" timestamp
- Semantic HTML tables

## Automation
Discord code monitor → auto-update → trigger deploy + periodic validity checks

## Case Study: Jujutsu Infinite
50K+/mo, 28% bounce, 5-min creation, top-3 ranking in 2 weeks
