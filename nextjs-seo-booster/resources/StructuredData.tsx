import { SITE_URL } from '@/lib/constants';

export default function StructuredData() {
    const jsonLd = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "WebSite",
                "name": "YOUR_WEBSITE_NAME",
                "alternateName": ["ALT_NAME_1", "ALT_NAME_2"],
                "url": SITE_URL,
                "description": "YOUR_WEBSITE_DESCRIPTION",
                "potentialAction": {
                    "@type": "SearchAction",
                    "target": {
                        "@type": "EntryPoint",
                        "urlTemplate": `${SITE_URL}/search?q={search_term_string}`
                    },
                    "query-input": "required name=search_term_string"
                }
            },
            {
                "@type": "Organization",
                "name": "YOUR_ORG_NAME",
                "url": SITE_URL,
                "logo": `${SITE_URL}/images/logo.png`,
                "contactPoint": {
                    "@type": "ContactPoint",
                    "contactType": "customer support",
                    "url": `${SITE_URL}/contact`
                }
            }
        ]
    };

    return (
        <script
            type="application/ld+json"
            dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }}
        />
    );
}
