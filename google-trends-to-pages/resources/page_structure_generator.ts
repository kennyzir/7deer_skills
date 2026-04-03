/**
 * 页面结构生成器
 * 
 * 根据关键词和意图自动生成页面的内容结构
 */

interface PageStructure {
  h1: string;
  metaTitle: string;
  metaDescription: string;
  sections: Section[];
  faq: FAQ[];
  internalLinks: InternalLink[];
  schemaMarkup: object;
}

interface Section {
  h2: string;
  h3?: string[];
  content: string;
  type: 'intro' | 'steps' | 'table' | 'list' | 'comparison';
}

interface FAQ {
  question: string;
  answer: string;
}

interface InternalLink {
  text: string;
  url: string;
  context: string;
}

/**
 * 为交易型关键词生成代码页结构
 */
export function generateCodesPageStructure(keyword: string, gameName: string): PageStructure {
  return {
    h1: `${gameName} Codes (March 2026) - Free Rewards & Spins`,
    metaTitle: `${gameName} Codes (March 2026) | Active & Expired Codes`,
    metaDescription: `All working ${gameName} codes for March 2026. Get free spins, cash, and exclusive rewards. Updated daily with new codes!`,
    
    sections: [
      {
        h2: 'Active Codes',
        type: 'table',
        content: 'Table with columns: Code | Reward | Expires'
      },
      {
        h2: 'How to Redeem Codes',
        h3: ['Step 1: Launch the Game', 'Step 2: Open Settings', 'Step 3: Enter Code'],
        type: 'steps',
        content: 'Step-by-step redemption guide with screenshots'
      },
      {
        h2: 'Expired Codes',
        type: 'table',
        content: 'Historical codes for reference'
      },
      {
        h2: 'FAQ',
        type: 'list',
        content: 'Common questions about codes'
      }
    ],
    
    faq: [
      {
        question: `How do I redeem ${gameName} codes?`,
        answer: `Open the game, click the Settings icon, find the "Codes" or "Redeem" button, enter the code exactly as shown, and click Submit.`
      },
      {
        question: `Why isn't my code working?`,
        answer: `Codes are case-sensitive and may have expired. Check the expiration date and ensure you're typing it correctly.`
      },
      {
        question: `How often are new codes released?`,
        answer: `New codes are typically released during game updates, milestones (like 1M likes), and special events. Check back weekly!`
      }
    ],
    
    internalLinks: [
      {
        text: `${gameName} Tier List`,
        url: `/tier-list`,
        context: 'After redeeming codes, check which characters are strongest'
      },
      {
        text: `${gameName} Wiki`,
        url: `/wiki`,
        context: 'Learn more about game mechanics'
      },
      {
        text: `${gameName} Trading Guide`,
        url: `/wiki/trading`,
        context: 'Use your spins to get valuable items'
      }
    ],
    
    schemaMarkup: {
      '@context': 'https://schema.org',
      '@type': 'FAQPage',
      mainEntity: [] // 填充 FAQ 数据
    }
  };
}

/**
 * 为信息型关键词生成指南页结构
 */
export function generateGuidePageStructure(keyword: string, topic: string): PageStructure {
  // 从关键词提取主题
  const cleanTopic = keyword.replace(/how to |in jujutsu infinite|guide/gi, '').trim();
  
  return {
    h1: `How to ${cleanTopic} - Complete Guide (2026)`,
    metaTitle: `How to ${cleanTopic} | Step-by-Step Guide (2026)`,
    metaDescription: `Learn how to ${cleanTopic} with our detailed guide. Includes tips, requirements, and common mistakes to avoid. Updated for 2026!`,
    
    sections: [
      {
        h2: 'Quick Summary (TL;DR)',
        type: 'list',
        content: '3-5 key points summarizing the guide'
      },
      {
        h2: 'Requirements',
        type: 'list',
        content: 'What you need before starting (level, items, etc.)'
      },
      {
        h2: 'Step-by-Step Guide',
        h3: ['Step 1', 'Step 2', 'Step 3', 'Step 4', 'Step 5'],
        type: 'steps',
        content: 'Detailed walkthrough with screenshots'
      },
      {
        h2: 'Tips & Tricks',
        type: 'list',
        content: 'Expert advice and shortcuts'
      },
      {
        h2: 'Common Mistakes',
        type: 'list',
        content: 'What to avoid'
      },
      {
        h2: 'FAQ',
        type: 'list',
        content: 'Frequently asked questions'
      }
    ],
    
    faq: [
      {
        question: `What level do I need to ${cleanTopic}?`,
        answer: `Typically level 300+ is recommended, but check the requirements section above.`
      },
      {
        question: `How long does it take to ${cleanTopic}?`,
        answer: `Depending on your preparation, it can take 30 minutes to 2 hours.`
      }
    ],
    
    internalLinks: [
      {
        text: 'Leveling Guide',
        url: '/handbook/leveling',
        context: 'If you need to level up first'
      },
      {
        text: 'Best Builds',
        url: '/builds',
        context: 'Optimize your character for this task'
      }
    ],
    
    schemaMarkup: {
      '@context': 'https://schema.org',
      '@type': 'HowTo',
      name: `How to ${cleanTopic}`,
      step: [] // 填充步骤数据
    }
  };
}

/**
 * 为商业调查型关键词生成对比页结构
 */
export function generateComparisonPageStructure(keyword: string): PageStructure {
  return {
    h1: `${keyword} - Complete Ranking & Comparison (2026)`,
    metaTitle: `${keyword} | Tier List & Rankings (March 2026)`,
    metaDescription: `Discover the ${keyword} with our expert tier list. Updated for March 2026 with detailed comparisons and recommendations.`,
    
    sections: [
      {
        h2: 'Tier List Overview',
        type: 'intro',
        content: 'Introduction to the ranking system'
      },
      {
        h2: 'S-Tier (Best)',
        type: 'comparison',
        content: 'Top-tier options with pros/cons'
      },
      {
        h2: 'A-Tier (Great)',
        type: 'comparison',
        content: 'Strong alternatives'
      },
      {
        h2: 'B-Tier (Good)',
        type: 'comparison',
        content: 'Solid mid-tier options'
      },
      {
        h2: 'C-Tier (Average)',
        type: 'comparison',
        content: 'Situational picks'
      },
      {
        h2: 'Ranking Criteria',
        type: 'list',
        content: 'How we evaluate and rank'
      }
    ],
    
    faq: [
      {
        question: `What makes an S-tier option?`,
        answer: `S-tier options excel in multiple areas: damage, utility, ease of use, and versatility across different game modes.`
      }
    ],
    
    internalLinks: [
      {
        text: 'Build Guides',
        url: '/builds',
        context: 'Learn how to use these top-tier options'
      }
    ],
    
    schemaMarkup: {
      '@context': 'https://schema.org',
      '@type': 'ItemList',
      itemListElement: [] // 填充排名数据
    }
  };
}

/**
 * 主函数：根据意图选择合适的生成器
 */
export function generatePageStructure(
  keyword: string,
  intent: 'Transactional' | 'Informational' | 'Commercial' | 'Navigational',
  context?: { gameName?: string; topic?: string }
): PageStructure {
  switch (intent) {
    case 'Transactional':
      return generateCodesPageStructure(keyword, context?.gameName || 'Game');
    case 'Informational':
      return generateGuidePageStructure(keyword, context?.topic || keyword);
    case 'Commercial':
      return generateComparisonPageStructure(keyword);
    case 'Navigational':
      // 导航型页面通常是聚合页，结构类似对比页
      return generateComparisonPageStructure(keyword);
    default:
      return generateGuidePageStructure(keyword, keyword);
  }
}
