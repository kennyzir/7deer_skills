# SEO Audit Checklist: [PAGE_NAME] - [DATE]

## 1. Metadata Check
- [ ] **Title**: 50-60 chars, Primary Keyword first.
- [ ] **Title Freshness**: Includes dynamic time marker (e.g., current month).
- [ ] **Title Uniqueness**: Distinct from Homepage title.
- [ ] **Description**: 120-160 chars, includes CTA & numbers.
- [ ] **Keywords**: 10-15 terms, NO hardcoded dates.
- [ ] **Canonical URL**: Set with full absolute URL & trailing slash (`/path/`).
- [ ] **OpenGraph**: Title, Description, URL, Type, SiteName present.
- [ ] **OG Image**: Valid 1200x630 image (verify file exists!).
- [ ] **Twitter Card**: `summary_large_image` set.

## 2. Structured Data (JSON-LD) Check
- [ ] **BreadcrumbList**: Present and valid.
- [ ] **FAQPage**: Min 5 Questions (if applicable).
- [ ] **HowTo**: 3-7 Clear Steps (if applicable).
- [ ] **ItemList**: Complete list elements (if applicable).
- [ ] **Validation**: Passed https://validator.schema.org/

## 3. Page Content Check
- [ ] **H1**: Only ONE per page, contains Primary Keyword.
- [ ] **Heading Hierarchy**: H1 > H2 > H3 (No skipping levels).
- [ ] **Quick Answer Box**: Prominent summary for Featured Snippets (High traffic pages).
- [ ] **FAQ Section**: Matches JSON-LD content, accordion style.
- [ ] **Internal Links**: "Related Guides" section (3-6 links) with descriptive anchor text.

## 4. Site-Level Check
- [ ] **Sitemap**: Added to `sitemap.ts` with correct priority.
- [ ] **Navigation**: Linked from Header/Footer (if important).
- [ ] **Orphan Check**: Page is reachable via internal links.

## 5. Technical Performance Check
- [ ] **Build Status**: Successful build (No errors).
- [ ] **SSG Verification**: Rendered as Static `○` or SSG `●`.
- [ ] **HTML Size**: < 150KB (Uncompressed).
- [ ] **Images**: Using `<Image>` component, `priority` on LCP image.
- [ ] **Core Web Vitals**: LCP < 2.5s, CLS < 0.1.

## Results
- **Build Pass**: ⬜ Yes / ⬜ No
- **Schema Valid**: ⬜ Yes / ⬜ No
- **HTML Size**: ___ KB
- **Notes**:
