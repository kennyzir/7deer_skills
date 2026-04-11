# Steering Template — SEO Autopilot

> 复制此文件到你的项目 `.kiro/steering/seo-autopilot.md`，替换 `{placeholder}` 为实际值。

```markdown
---
inclusion: manual
---

# SEO Autopilot — Processing Instructions

## Report Directory
{report_directory}/

## State Tracking
{report_directory}/processed.json

## Processing Pipeline

### Phase 0: Discover New Reports
1. Read processed.json for already-handled reports
2. Scan report directory for new .md files
3. If none found, stop

### Phase 1: Parse Report
Extract from each new report:
- Top keywords with priority
- Search intent (transactional / informational)
- Competition score
- Recommended page type and URL slug

### Phase 2: Deduplicate
Compare keywords against:
- {navigation_file} — existing page hrefs
- {blog_file} — existing blog slugs
Skip keywords already covered (including semantic overlaps)

### Phase 3: Page Type Decision
- Transactional / Emotional intent → Landing page
- Informational intent → Blog post
- Max 3 pages per report

### Phase 4: Generate Content
Follow the project existing patterns:
- Landing pages: copy the structure of {example_landing_page}
- Blog posts: use the blog system at {blog_file}
- Include: metadata, canonical, OpenGraph, JSON-LD, FAQ schema, internal links, CTA

### Phase 5: Register
- Add to {navigation_file} (footer: true)
- Add to {sitemap_file} (landing: 0.85, blog: 0.6)

### Phase 6: SEO Audit
- Title < 60 chars, contains primary keyword
- Description < 160 chars
- Canonical URL set
- JSON-LD WebPage + FAQ schema
- H1 unique, contains keyword
- 3-5 internal links
- CTA to {main_cta_page}

### Phase 7: Commit + Push
- git add all new/modified files
- git commit -m "feat(seo): add N pages from keyword report [date]"
- git push origin main

### Phase 8: Update State
Update processed.json with report name, date, and pages created

## Limits
- Max 3 pages per report
- Prioritize high priority keywords first
- Skip keywords with semantic overlap to existing pages
```

## Placeholder Reference

| Placeholder | Description | Example |
|-------------|-------------|---------|
| `{report_directory}` | 关键词报告存放目录 | `keyword-research` |
| `{navigation_file}` | 导航注册文件 | `lib/navigation.ts` |
| `{blog_file}` | 博客数据文件 | `lib/blog.ts` |
| `{sitemap_file}` | Sitemap 文件 | `app/sitemap.ts` |
| `{example_landing_page}` | 现有落地页示例 | `app/emotional-tarot/page.tsx` |
| `{main_cta_page}` | 主转化页面 | `/draw` |
