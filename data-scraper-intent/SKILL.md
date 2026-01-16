---
name: data-scraper-intent
description: A toolkit for web data extraction and search intent analysis. Includes patterns for handling lazy-loaded content and LLM prompts for classifying search keywords.
---

# Data Scraper & Intent Analyzer

This skill provides reusable patterns and prompts for two common SEO/data tasks:
1.  **Web Data Extraction**: Handling tricky scenarios like lazy-loaded images, Next.js Image components, and paginated content.
2.  **Search Intent Classification**: Using LLMs to classify keywords into actionable content categories.

## Resources Included

1.  **`resources/scraping_patterns.md`**: A guide with code snippets on how to handle common web scraping challenges using Playwright/Puppeteer.
2.  **`resources/intent_prompts.md`**: Ready-to-use LLM prompts for classifying search keywords.

## Usage

### 1. Data Extraction Patterns
Review `resources/scraping_patterns.md` when you need to extract data from:
*   Websites using lazy-loading for images (e.g., `loading="lazy"`, IntersectionObserver).
*   Next.js apps using `<Image>` component (srcset, blur placeholders).
*   Sites with infinite scroll or "Load More" buttons.

### 2. Intent Analysis
Copy the prompts from `resources/intent_prompts.md` and use them with your LLM of choice (GPT-4, DeepSeek, Claude) to classify keywords from Google Trends, SEMrush, or Ahrefs.

## Example Workflow (Trend to Page)

1.  **Input**: A list of rising keywords from Google Trends.
2.  **Step 1**: Use the "Keyword Intent Classifier" prompt to categorize them.
3.  **Step 2**: For "Informational" intents, create guide pages.
4.  **Step 3**: For "Transactional" intents, create tool pages.
5.  **Output**: A prioritized list of pages to create.
