# SEO Audit Checklist: [PAGE_NAME] - [DATE]

## 1. Metadata Check
- [ ] **Title**: 50-60 characters, primary keyword first, unique vs homepage.
- [ ] **Description**: 120-160 characters, includes CTA and numbers.
- [ ] **Keywords**: 10-15 terms, no hardcoded dates (use dynamic).
- [ ] **Canonical URL**: Set, uses trailing slash.
- [ ] **OpenGraph**: title, description, url, type present.
- [ ] **Twitter Card**: card type set (summary_large_image or summary).

## 2. Structured Data (JSON-LD) Check
- [ ] **BreadcrumbList**: Present for navigation context.
- [ ] **FAQPage**: Min 5 questions (if applicable).
- [ ] **HowTo**: 3-7 clear steps (if applicable).
- [ ] **ItemList**: For list/ranking pages (if applicable).
- [ ] Schema validated with https://validator.schema.org/

## 3. Content Check
- [ ] **H1**: Only one, includes primary keyword.
- [ ] **Heading Hierarchy**: H1 > H2 > H3, no skipping levels.
- [ ] **Quick Answer Box**: Present for high-traffic pages.
- [ ] **FAQ Section**: Min 3 questions, matches JSON-LD.
- [ ] **Internal Links**: 3-6 descriptive anchor texts.

## 4. Site-Level Check
- [ ] **Sitemap**: Page added to `sitemap.xml` or `sitemap.ts`.
- [ ] **Navigation**: Page linked from Header/Footer (if important).
- [ ] **Homepage**: Link added from homepage (if high-priority).

## 5. Performance Check
- [ ] **Build**: Page generates as static (○ or ●).
- [ ] **HTML Size**: < 150KB.
- [ ] **Images**: Optimized (WebP/AVIF), use `<Image>` component.
- [ ] **LCP**: < 2.5s (via Lighthouse).

## Results
- **Build Status**: ⬜ Pass / ⬜ Fail
- **Schema Validation**: ⬜ Pass / ⬜ Fail
- **Page Size**: ___ KB
- **Notes**:
