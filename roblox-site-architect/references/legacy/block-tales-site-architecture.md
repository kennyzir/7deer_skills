# Block Tales Site — Architecture Reference

**用途：** 对照清单。建新游戏站时，逐项核对是否已在模板站里覆盖。

---

## 目录结构

```
{site-a}/ 或 {site-b}/
├── src/
│   ├── app/
│   │   ├── layout.tsx              ← 根布局（必须）
│   │   ├── page.tsx               ← 首页
│   │   ├── not-found.tsx          ← 404
│   │   ├── sitemap.ts             ← 动态 sitemap（必须）
│   │   ├── robots.txt             ← 或 robots.ts
│   │   ├── codes/page.tsx         ← Hub 页面
│   │   ├── calculator/page.tsx     ← Hub 页面
│   │   ├── tier-list/
│   │   │   ├── page.tsx           ← 列表总页
│   │   │   └── [slug]/page.tsx   ← 动态详情页（必须）
│   │   ├── beginner-guide/page.tsx
│   │   ├── updates/page.tsx
│   │   ├── about/page.tsx
│   │   ├── terms/page.tsx
│   │   └── privacy-policy/page.tsx
│   ├── components/
│   │   ├── Header.tsx             ← 顶部导航（必须）
│   │   └── Footer.tsx             ← 底部免责（必须）
│   ├── data/
│   │   ├── game.config.json       ← 游戏配置（必须）
│   │   ├── pickaxes.json          ← 主数据（必须）
│   │   └── codes.json             ← codes 数据
│   └── lib/
│       ├── data.ts                ← getter 函数（必须）
│       └── seo.ts                 ← Schema 构建函数（必须）
├── public/
│   ├── robots.txt
│   └── og-default.svg             ← OG 默认图（必须）
└── scripts/
    └── git-deploy.py              ← 部署脚本（必须）
```

---

## layout.tsx 标准模板

```tsx
import type { Metadata } from 'next';
import { getGameConfig } from '@/lib/data';
import Header from '@/components/Header';
import Footer from '@/components/Footer';
import './globals.css';

const config = getGameConfig();

export const metadata: Metadata = {
  title: {
    default: config.seo.siteTitle,
    template: `%s | ${config.game.name}`,
  },
  description: config.seo.siteDescription,
  keywords: [...config.seo.primaryKeywords, ...config.seo.secondaryKeywords],
  alternates: { canonical: config.seo.baseUrl },
  openGraph: {
    title: config.seo.siteTitle,
    description: config.seo.siteDescription,
    url: config.seo.baseUrl,
    siteName: config.game.name,
    images: [{ url: `${config.seo.baseUrl}/og-default.svg`, width: 1200, height: 630 }],
    type: 'website',
  },
  twitter: {
    card: 'summary_large_image',
    title: config.seo.siteTitle,
    description: config.seo.siteDescription,
    images: [`${config.seo.baseUrl}/og-default.svg`],
  },
  robots: { index: true, follow: true },
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" className="scroll-smooth">
      <head>
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <link rel="icon" href="/favicon.svg" type="image/svg+xml" />
      </head>
      <body className="min-h-screen bg-white dark:bg-gray-950 text-gray-900 dark:text-gray-100 font-sans antialiased">
        <Header />
        <main className="min-h-[calc(100vh-180px)]">{children}</main>
        <Footer />
      </body>
    </html>
  );
}
```

---

## Header.tsx 标准模板

```tsx
import Link from 'next/link';
import { getGameConfig } from '@/lib/data';

const config = getGameConfig();

export default function Header() {
  return (
    <header className="border-b border-gray-200 dark:border-gray-800 bg-white/80 dark:bg-gray-950/80 backdrop-blur-sm sticky top-0 z-50">
      <div className="max-w-6xl mx-auto px-4 h-14 flex items-center justify-between">
        <Link href="/" className="font-bold text-lg tracking-tight hover:text-amber-400 transition-colors">
          {config.game.name}
        </Link>
        <nav className="flex items-center gap-1 text-sm font-medium">
          <Link href="/tier-list" className="px-3 py-2 rounded-md hover:bg-gray-100 dark:hover:bg-gray-800">
            Tier List
          </Link>
          <Link href="/calculator" className="px-3 py-2 rounded-md hover:bg-gray-100 dark:hover:bg-gray-800">
            Calculator
          </Link>
          <Link href="/codes" className="px-3 py-2 rounded-md hover:bg-gray-100 dark:hover:bg-gray-800">
            Codes
          </Link>
          <Link href="/beginner-guide" className="px-3 py-2 rounded-md hover:bg-gray-100 dark:hover:bg-gray-800">
            Guide
          </Link>
          <Link href="/updates" className="px-3 py-2 rounded-md hover:bg-gray-100 dark:hover:bg-gray-800">
            Updates
          </Link>
        </nav>
      </div>
    </header>
  );
}
```

---

## Footer.tsx 标准模板

```tsx
export default function Footer() {
  return (
    <footer className="border-t border-gray-200 dark:border-gray-800 mt-16 py-8">
      <div className="max-w-6xl mx-auto px-4 text-center text-sm text-gray-500">
        <p className="mb-2">
          {config.game.name} Guide & Tools — Fan-made companion site. Not affiliated with Roblox or {config.game.developer}.
        </p>
        <p>Game data sourced from public Roblox API and community YouTube creators. Updated daily.</p>
      </div>
    </footer>
  );
}
```

---

## lib/data.ts 标准结构

```typescript
import mainData from '@/data/{type}.json';
import configData from '@/data/game.config.json';

export interface ItemType {
  id: string;
  slug: string;
  name: string;
  // ... 其他字段
}

const items: ItemType[] = (mainData as { items: ItemType[] }).items;
const config = configData as GameConfig;

export function getItems(): ItemType[] { return items; }
export function getItemBySlug(slug: string): ItemType | undefined {
  return items.find((i) => i.slug === slug);
}
export function getGameConfig(): GameConfig { return config; }
// ... 其他 helper 函数
```

---

## lib/seo.ts 标准结构

必须导出：`buildBreadcrumbSchema`、`buildFAQSchema`（或 `generateFAQSchema`）

```typescript
export function buildBreadcrumbSchema(items: { name: string; item: string }[]) {
  return {
    '@context': 'https://schema.org',
    '@type': 'BreadcrumbList',
    itemListElement: items.map((item, index) => ({
      '@type': 'ListItem',
      position: index + 1,
      name: item.name,
      item: item.item,
    })),
  };
}

export function buildFAQSchema(faqs: { question: string; answer: string }[]) {
  return {
    '@context': 'https://schema.org',
    '@type': 'FAQPage',
    mainEntity: faqs.map((faq) => ({
      '@type': 'Question',
      name: faq.question,
      acceptedAnswer: { '@type': 'Answer', text: faq.answer },
    })),
  };
}
```

---

## sitemap.ts 动态模板

```typescript
import { MetadataRoute } from 'next';
import { getItems, getGameConfig } from '@/lib/data';

export const dynamic = 'force-static';

const config = getGameConfig();
const baseUrl = config.seo.baseUrl;

export default function sitemap(): MetadataRoute.Sitemap {
  const items = getItems();

  const staticRoutes = config.routes.map((route) => ({
    url: `${baseUrl}${route.path}`,
    lastModified: new Date(),
    changeFrequency: (route.path === '/' ? 'daily' : 'weekly') as 'daily' | 'weekly',
    priority: parseFloat(route.priority),
  }));

  const itemRoutes = items.map((item) => ({
    url: `${baseUrl}/{section}/${item.slug}`,
    lastModified: new Date(),
    changeFrequency: 'weekly' as const,
    priority: 0.8,
  }));

  return [...staticRoutes, ...itemRoutes];
}
```

---

## 动态 [slug]/page.tsx 标准结构

```typescript
import type { Metadata } from 'next';
import { notFound } from 'next/navigation';
import Link from 'next/link';
import { getItems, getItemBySlug } from '@/lib/data';
import { buildBreadcrumbSchema, buildFAQSchema } from '@/lib/seo';

const items = getItems();

export function generateStaticParams() {
  return items.map((item) => ({ slug: item.slug }));
}

export async function generateMetadata({ params }: { params: Promise<{ slug: string }> }): Promise<Metadata> {
  const { slug } = await params;
  const item = getItemBySlug(slug);
  if (!item) return { title: 'Not Found' };
  return {
    title: `${item.name} — ${config.game.name} Guide`,
    description: item.description,
    alternates: { canonical: `${config.seo.baseUrl}/{section}/${slug}` },
  };
}

export default async function ItemDetailPage({ params }: { params: Promise<{ slug: string }> }) {
  const { slug } = await params;
  const item = getItemBySlug(slug);
  if (!item) notFound();

  return (
    <main className="mx-auto max-w-4xl px-4 py-10">
      {/* Breadcrumb */}
      <nav className="text-sm text-gray-500 mb-6">
        <a href="/" className="hover:text-amber-400">Home</a>
        <span className="mx-2">›</span>
        <Link href="/{section}" className="hover:text-amber-400">{Section}</Link>
        <span className="mx-2">›</span>
        <span className="text-gray-300">{item.name}</span>
      </nav>
      {/* Content */}
    </main>
  );
}
```

---

## scripts/git-deploy.py 标准脚本

```python
#!/usr/bin/env python3
"""Git add + commit + push for {project-name}."""
import subprocess, sys

proj = "/path/to/your/project"
msg = sys.argv[1] if len(sys.argv) > 1 else "chore: update"

for cmd in [
    ["git", "add", "-A"],
    ["git", "commit", "-m", msg],
    ["git", "push"],
]:
    r = subprocess.run(cmd, cwd=proj, capture_output=True, text=True)
    if r.returncode != 0:
        print("STDERR:", r.stderr.strip())
        sys.exit(r.returncode)
    if r.stdout.strip():
        print(r.stdout.strip())
```
