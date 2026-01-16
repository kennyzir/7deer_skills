# Web Scraping Patterns

This document provides code snippets and strategies for common web scraping challenges.

## 1. Handling Lazy-Loaded Images

**Problem**: Images don't appear in the initial HTML because they use `loading="lazy"` or IntersectionObserver.

**Solution (Playwright)**:
```javascript
// Scroll to bottom to trigger lazy loading
await page.evaluate(async () => {
    await new Promise((resolve) => {
        let totalHeight = 0;
        const distance = 500;
        const timer = setInterval(() => {
            window.scrollBy(0, distance);
            totalHeight += distance;
            if (totalHeight >= document.body.scrollHeight) {
                clearInterval(timer);
                resolve();
            }
        }, 100);
    });
});

// Wait for images to load
await page.waitForTimeout(2000);

// Now extract image src
const images = await page.$$eval('img', (imgs) => imgs.map(img => img.src));
```

## 2. Extracting Images from Next.js `<Image>` Component

**Problem**: Next.js `<Image>` uses `/_next/image?url=...&w=...&q=...` URLs and `srcset`.

**Solution**:
```javascript
// Get the best quality image from srcset
const images = await page.$$eval('img', (imgs) => {
    return imgs.map(img => {
        // Option 1: Parse srcset for highest resolution
        if (img.srcset) {
            const sources = img.srcset.split(',').map(s => s.trim().split(' '));
            // Get the last (usually largest) one
            return sources[sources.length - 1][0];
        }
        // Option 2: Use src directly
        return img.src;
    });
});

// Decode Next.js image URL if needed
function decodeNextImageUrl(url) {
    try {
        const parsed = new URL(url);
        if (parsed.pathname === '/_next/image') {
            return parsed.searchParams.get('url');
        }
    } catch {}
    return url;
}
```

## 3. Handling Paginated Content ("Load More" Buttons)

**Solution (Playwright)**:
```javascript
let allItems = [];

while (true) {
    // Extract current items
    const items = await page.$$eval('.item-class', els => els.map(el => el.textContent));
    allItems.push(...items);
    
    // Try to click "Load More"
    const loadMoreBtn = await page.$('button:has-text("Load More")');
    if (!loadMoreBtn) break;
    
    await loadMoreBtn.click();
    await page.waitForTimeout(1500); // Wait for new content
}

console.log(`Total items: ${allItems.length}`);
```

## 4. Bypassing Basic Bot Detection

**Strategies**:
1.  **User-Agent**: Set a realistic browser User-Agent.
2.  **Headful Mode**: Run browser in non-headless mode.
3.  **Random Delays**: Add `Math.random() * 1000` to waits.
4.  **Stealth Plugin**: Use `playwright-extra` with `puppeteer-extra-plugin-stealth`.

```javascript
const { chromium } = require('playwright-extra');
const stealth = require('puppeteer-extra-plugin-stealth')();
chromium.use(stealth);

const browser = await chromium.launch({ headless: false });
```

## 5. Extracting Structured Data from JSON-LD

**Solution**:
```javascript
const jsonLd = await page.$$eval('script[type="application/ld+json"]', scripts => {
    return scripts.map(script => JSON.parse(script.textContent));
});

// Find FAQPage schema
const faqSchema = jsonLd.find(s => s['@type'] === 'FAQPage');
if (faqSchema) {
    console.log('FAQ Questions:', faqSchema.mainEntity.map(q => q.name));
}
```
