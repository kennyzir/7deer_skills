import { MetadataRoute } from 'next';

// Replace with your site URL constant
const SITE_URL = process.env.NEXT_PUBLIC_SITE_URL || 'https://yourwebsite.com';

export const dynamic = 'force-static';

export default function sitemap(): MetadataRoute.Sitemap {
    const staticRoutes = [
        '',
        '/about',
        '/contact',
        '/privacy',
        '/terms',
    ];

    const sitemapEntries = staticRoutes.map(route => ({
        url: `${SITE_URL}${route}`,
        lastModified: new Date(),
        changeFrequency: 'weekly' as const,
        priority: route === '' ? 1 : 0.8,
    }));

    return sitemapEntries;
}
