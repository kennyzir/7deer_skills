interface FAQItem {
  question: string;
  answer: string;
}

export function generateFAQSchema(items: FAQItem[]) {
  return {
    '@context': 'https://schema.org',
    '@type': 'FAQPage',
    mainEntity: items.map(item => ({
      '@type': 'Question',
      name: item.question,
      acceptedAnswer: {
        '@type': 'Answer',
        text: item.answer
      }
    }))
  };
}

export function generateBreadcrumbSchema(gameName: string, gameSlug: string, baseUrl: string) {
  return {
    '@context': 'https://schema.org',
    '@type': 'BreadcrumbList',
    itemListElement: [
      {
        '@type': 'ListItem',
        position: 1,
        name: 'Home',
        item: baseUrl
      },
      {
        '@type': 'ListItem',
        position: 2,
        name: `${gameName} Codes`,
        item: `${baseUrl}/${gameSlug}`
      }
    ]
  };
}

export function generateItemListSchema(gameName: string, codes: Array<{ code: string; reward: string }>) {
  return {
    '@context': 'https://schema.org',
    '@type': 'ItemList',
    name: `Active ${gameName} Codes`,
    numberOfItems: codes.length,
    itemListElement: codes.map((code, idx) => ({
      '@type': 'ListItem',
      position: idx + 1,
      name: code.code,
      description: code.reward
    }))
  };
}
