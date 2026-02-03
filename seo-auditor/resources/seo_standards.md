# SEO Standards & Guidelines

> **Role Definition**: As an SEO Architect, every new page or feature must undergo a comprehensive SEO review according to these standards.
> **Core Principle**: SEO is not an afterthought; it is the first step of page design. Every page is a traffic entry point.

---

## 🎯 SEO Audit Process (Mandatory)

### Audit Timing
1.  **Pre-Development** - Define target keywords and search intent.
2.  **Post-Development** - Check item by item against the checklist.
3.  **Pre-Deployment** - Verify HTML output and technical performance.
4.  **Post-Launch Monitoring** - Track via Google Search Console.

### Audit Cycle
-   **New Pages**: Mandatory audit upon completion.
-   **Existing Pages**: Quarterly review.
-   **High Traffic Pages**: Monthly review.

---

## 📋 Part 1: Metadata Standards

### 1.1 Title Tag

**Format Template**:
```
{Primary Keyword} ({Time Marker}) - {Value Proposition} | {Brand Name}
```

**Requirements**:
- [ ] Length: 50-60 characters (Google truncation point).
- [ ] Primary keyword placed at the very beginning.
- [ ] Include time marker (Dynamic Month/Year) for freshness.
- [ ] Distinct from Homepage Title (**Critical**).
- [ ] Avoid keyword stuffing.

**Correct Example**:
```typescript
// Dynamic Month Title
const currentMonth = new Date().toLocaleDateString('en-US', { month: 'long', year: 'numeric' });
title: `Project Codes (${currentMonth}) - All Working Rewards & Loots`
```

### 1.2 Description Tag

**Requirements**:
- [ ] Length: 120-160 characters.
- [ ] Include primary keyword and 1-2 long-tail keywords.
- [ ] Include Call to Action (CTA).
- [ ] Include numbers/data for credibility.
- [ ] Semantic complement to title, no repetition.

**Correct Example**:
```typescript
description: "All 8 working Project codes for January 2026. Get free rewards, currency, and items. Updated daily with new redemption codes. Redeem now before expiration!"
```

### 1.3 Keywords Tag

**Requirements**:
- [ ] Quantity: 10-15 keywords.
- [ ] Include primary keyword variations.
- [ ] Include long-tail keywords (Search Intent).
- [ ] Include LSI Keywords.
- [ ] **No Hardcoded Months** (Use year or dynamic generation).

### 1.4 Canonical URL

**Mandatory Rules**:
- [ ] Must set `alternates.canonical`.
- [ ] URL must use trailing slash format consistently (e.g., `/codes/` not `/codes`).
- [ ] Use full absolute URL (including domain).

```typescript
alternates: {
  canonical: 'https://www.example.com/section/',
}
```

### 1.5 OpenGraph

**Required Fields**:
- [ ] `title` - Can be different from meta title, optimized for social sharing.
- [ ] `description` - Short and punchy.
- [ ] `url` - Canonical URL.
- [ ] `type` - Correct type (website/article).
- [ ] `siteName` - Brand Name.

**Image Standards**:
- [ ] Size: 1200x630 pixels.
- [ ] Format: PNG or JPG.
- [ ] **Do not reference non-existent images!**

### 1.6 Twitter Card

```typescript
twitter: {
  card: 'summary_large_image',  // Use summary_large_image if image exists, else summary
  title: '...',
  description: '...',
}
```

---

## 📊 Part 2: Structured Data Standards

### 2.1 Schema Selection Guide

| Page Type | Recommended Schema | Priority |
| :--- | :--- | :--- |
| FAQ/Guide Page | `FAQPage` | ★★★★★ |
| Tutorial/How-To | `HowTo` | ★★★★★ |
| List/Ranking | `ItemList` | ★★★★☆ |
| Tool/Calculator | `SoftwareApplication` | ★★★★☆ |
| Article/News | `Article` | ★★★☆☆ |
| All Pages | `BreadcrumbList` | ★★★★★ |

### 2.2 FAQPage Schema

**Minimum Requirement**: 5 FAQ questions (Google recommendation).

**Design Principles**:
1.  Cover real user search intent.
2.  Start with What/How/Where/When.
3.  Concise answers (Featured Snippet friendly).
4.  Include keywords naturally.

### 2.3 HowTo Schema

**Design Principles**:
1.  One clear action per step.
2.  3-7 steps recommended.
3.  Include specific locations/values.

### 2.4 ItemList Schema

Used for ranking lists or collections. Ensure `itemListElement` is populated correctly with `ListItem`.

---

## 📄 Part 3: Page Content Standards

### 3.1 Heading Hierarchy

```
H1 - Main Page Title (Only ONE, contains primary keyword)
  H2 - Major Section Title
    H3 - Sub-section Title
```

### 3.2 Quick Answer Box (Featured Snippet Optimization)

**Mandatory for High Traffic Pages**:
Create a distinct section near the top that directly answers the user's query.

```css
/* Example CSS */
.quickAnswer {
  background: var(--featured-bg);
  border-left: 4px solid var(--accent);
  padding: 1rem 1.5rem;
  margin: 1.5rem 0;
}
```

### 3.3 Internal Linking

**Mandatory**:
- [ ] "Related Guides" section at the bottom.
- [ ] 3-6 internal links.
- [ ] Descriptive anchor text (avoid "Click Here").
- [ ] Trailing slash on URLs.

---

## 🔗 Part 4: Site-Level SEO

### 4.1 Sitemap

Every new page must be added to `sitemap.ts` (or `sitemap.xml`) with appropriate priority:
-   `1.0`: Homepage
-   `0.9`: High traffic / Hub pages
-   `0.8`: Main guides
-   `0.6`: Secondary pages
-   `0.3`: Policy pages

### 4.2 Navigation

-   Ensure meaningful pages are reachable from Header/Footer.
-   Avoid orphan pages.

---

## ⚡ Part 5: Technical Performance

### 5.1 Core Web Vitals Targets

| Metric | Target | Tool |
| :--- | :--- | :--- |
| LCP (Largest Contentful Paint) | < 2.5s | Lighthouse |
| FID (First Input Delay) | < 100ms | Lighthouse |
| CLS (Cumulative Layout Shift) | < 0.1 | Lighthouse |
| TTFB (Time to First Byte) | < 600ms | WebPageTest |

### 5.2 HTML Size

-   Single Page HTML < 150KB (Uncompressed).
-   Check for excessive inlined data or CSS.

### 5.3 Static Generation (Next.js)

-   Ensure pages are Static (`○`) or SSG (`●`).
-   Avoid `λ (Dynamic)` unless absolutely necessary.

### 5.4 Image Optimization

-   Use `<Image>` component.
-   Add `priority` to LCP image.
-   Use WebP/AVIF formats.

---

## 🐛 Part 6: Common Pitfalls

| Error | Consequence | Correction |
| :--- | :--- | :--- |
| **Duplicate Title** | Content cannibalization | Unique title per page |
| **Hardcoded Month** | Content outdated | Dynamic generation |
| **Bad OG Image** | Broken social shares | File existence check |
| **Missing Schema** | No rich snippets | Validate Schema |
| **Orphan Page** | Not indexed | Add visible links |

---

## 🔧 Part 7: Tools & Scripts

### HTML Size Check (PowerShell)

```powershell
# View largest 15 HTML files
Get-ChildItem -Path "out" -Recurse -Filter "*.html" | `
  Select-Object @{Name='Path';Expression={$_.FullName.Replace((Get-Location).Path + '\out\','')}}, `
  @{Name='SizeKB';Expression={[Math]::Round($_.Length/1KB, 2)}} | `
  Sort-Object SizeKB -Descending | Select-Object -First 15
```

### Online Validators

-   [Schema Validator](https://validator.schema.org/)
-   [Rich Results Test](https://search.google.com/test/rich-results)
-   [PageSpeed Insights](https://pagespeed.web.dev/)
