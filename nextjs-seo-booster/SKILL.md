---
name: nextjs-seo-booster
description: A complete SEO toolkit for Next.js applications, including structured data (Schema.org), dynamic sitemap generation, and meta tags.
---

# Next.js SEO Booster

This skill helps you instantly add professional-grade SEO capabilities to a Next.js (App Router) project.

## Components Included
1.  **StructuredData.tsx**: Injects Google-compliant JSON-LD schema (WebSite, Organization, SoftwareApplication).
2.  **sitemap.ts**: Dynamically generates `sitemap.xml` for all your routes, including programmatic SEO pages.

## Usage Instructions

### 1. Structured Data (JSON-LD)
Copy `resources/StructuredData.tsx` to your `components/` directory.
Import and use it in your root layout (`app/layout.tsx`):

```tsx
import StructuredData from '@/components/StructuredData';

export default function RootLayout({ children }) {
  return (
    <html>
      <head>
          <StructuredData />
      </head>
      <body>{children}</body>
    </html>
  );
}
```

### 2. Sitemap Generation
Copy `resources/sitemap.ts` to your `app/` directory.
Modify the `const routes` array to match your website's pages.

### 3. Verification
- Visit `http://localhost:3000/sitemap.xml` to see your sitemap.
- Use Google's Rich Results Test to validate the structured data.
