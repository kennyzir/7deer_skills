export function generateFAQSchema(gameName: string) {
  return {
    '@context': 'https://schema.org',
    '@type': 'FAQPage',
    mainEntity: [
      {
        '@type': 'Question',
        name: `How do I redeem ${gameName} codes?`,
        acceptedAnswer: {
          '@type': 'Answer',
          text: `Open ${gameName}, click Settings, find the Codes button, enter the code exactly as shown, and click Submit.`
        }
      },
      {
        '@type': 'Question',
        name: `Why isn't my ${gameName} code working?`,
        acceptedAnswer: {
          '@type': 'Answer',
          text: 'Codes are case-sensitive and may have expired. Check the expiration date and ensure correct spelling without extra spaces.'
        }
      },
      {
        '@type': 'Question',
        name: `How often are new ${gameName} codes released?`,
        acceptedAnswer: {
          '@type': 'Answer',
          text: 'New codes are typically released during game updates, milestones, and special events. Check back weekly for new codes!'
        }
      },
      {
        '@type': 'Question',
        name: `Do ${gameName} codes expire?`,
        acceptedAnswer: {
          '@type': 'Answer',
          text: 'Yes, most codes expire after a few weeks or when the next update is released. We update this page daily to mark expired codes.'
        }
      }
    ]
  };
}

export function generateBreadcrumbSchema(gameName: string, gameSlug: string, baseUrl: string = 'https://jujutsucalc.com') {
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
