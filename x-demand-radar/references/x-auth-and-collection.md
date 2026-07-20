# X/Twitter Auth & Cookie Injection

## Prerequisite

The browser session is stateless. Every new browser session starts logged out. Must inject the `auth_token` cookie before any search.

## Cookie Injection Procedure

```
1. Navigate to https://x.com (not x.com/search)
2. In browser_console, run:
   document.cookie = "auth_token=your_auth_token_here; domain=.x.com; path=/; secure; SameSite=None";
3. Navigate to https://x.com/home to verify login
4. Confirm snapshot shows the expected account name and "Home / X" title
5. Now proceed to search URLs
```

## Cookie Expiry & Session Management

- **Every Hermes session starts with a fresh browser.** Cookie does NOT persist between agent turns. Must re-inject at the START of every cron run.
- If navigated search URL redirects to x.com/i/flow/login → cookie already expired → re-inject immediately
- Always verify login with x.com/home BEFORE starting any search. Check snapshot for the expected account name and "Home / X" title.
- After injection, navigate to x.com/home FIRST, then proceed to search URLs.
- If search redirects mid-session (can happen after 5-10 minutes), re-inject at x.com and resume the layer.

**Cron-workflow checklist (every run):**
1. `browser_navigate` to https://x.com
2. `browser_console`: inject auth_token cookie
3. `browser_navigate` to https://x.com/home
4. Verify snapshot shows the expected account → proceed
5. If not → cookie stale, request new token from user

## Browser Console Async Pattern

**WRONG** (will fail with "Illegal return statement"):
```javascript
async function collect() { ... }
return await collect();
```

**CORRECT** (must use IIFE):
```javascript
(async function() {
  // ... collection logic ...
  return JSON.stringify(results);
})()
```

## Collection Function Template

```javascript
(async function() {
  await new Promise(r => setTimeout(r, 2000)); // wait for page load
  let allPosts = [];
  let prevCount = 0;
  let scrolls = 0;
  const maxScrolls = 12;
  const now = new Date();

  while (scrolls < maxScrolls) {
    const articles = document.querySelectorAll('article');
    articles.forEach((a) => {
      // text extraction
      const textEl = a.querySelector('[data-testid="tweetText"]') || a.querySelector('[lang]');
      const text = textEl?.innerText || '';
      if (!text || text.length < 25) return;

      // likes with K/M parsing
      const likesEl = a.querySelector('[data-testid="like"] span');
      let likes = 0;
      if (likesEl) {
        const txt = likesEl.innerText.replace(/,/g, '');
        if (txt.includes('K')) likes = Math.round(parseFloat(txt.replace('K','')) * 1000);
        else if (txt.includes('M')) likes = Math.round(parseFloat(txt.replace('M','')) * 1000000);
        else likes = parseInt(txt) || 0;
      }

      // author extraction (filter out status/hashtag/search links)
      const allLinks = Array.from(a.querySelectorAll('a[role="link"]'));
      const authorLink = allLinks.find(l =>
        l.href && l.href.includes('x.com/') &&
        !l.href.includes('/status/') && !l.href.includes('search') && !l.href.includes('hashtag')
      );
      const author = authorLink?.href?.split('/').pop() || '';

      // time
      const timeEl = a.querySelector('time');
      const time = timeEl?.getAttribute('datetime') || '';

      // status link
      const statusLink = allLinks.find(l => l.href && l.href.includes('/status/'));
      const link = statusLink?.href || '';

      // hotScore calculation
      const postTime = new Date(time);
      const hoursAgo = Math.max(0.1, (now - postTime) / (1000 * 60 * 60));
      const likesPerHour = Math.round(likes / hoursAgo);
      const hotScore = Math.round(likes * Math.log(1 + likesPerHour));

      // dedup by text
      if (!allPosts.some(p => p.text === text)) {
        allPosts.push({
          text: text.substring(0, 300), likes, author, time, link,
          hoursAgo: Math.round(hoursAgo*10)/10, likesPerHour, hotScore
        });
      }
    });

    // stop if no new posts after 2 scroll attempts
    if (allPosts.length === prevCount && scrolls > 2) break;
    prevCount = allPosts.length;

    window.scrollBy(0, 700);
    await new Promise(r => setTimeout(r, 1500));
    scrolls++;
  }

  return JSON.stringify(allPosts.sort((a,b) => b.hotScore - a.hotScore));
})()
```

## X Search Quirks

- `min_faves:N` filter works but can be inconsistent — results are sparse with N≥100 + complex queries
- Complex boolean OR queries reduce result count significantly
- `since:YYYY-MM-DD` works combined with `min_faves`
- `-filter:replies` is reliable
- `f=live` tab gives "Latest"; omit for "Top" (usually better signal quality for hot detection)
- **Today's News sidebar**: On every search results page, the right sidebar shows "Today's News" with trending topics and post counts (e.g., "OpenAI Launches GPT-Realtime-2 · 19 hours ago · 11.2K posts"). These are EXCELLENT supplementary signals — topics appearing here with >10K posts and <24h age are top-tier hot keywords. Always check the sidebar snapshot after each search layer.
- X search pagination is infinite scroll — the JS collection function must scroll-and-collect. X replaces (not appends) results on scroll, so collection must happen within each scroll cycle.
- Posts about already-existing products or marketing content dominate results. Filtering must happen post-collection.

## HotScore Formula

```
hotScore = likes × log(1 + likesPerHour)
likesPerHour = likes / hoursSincePosted
hoursSincePosted = max(0.1, (now - postTime) / 3600000)
```

This formula balances absolute popularity (likes) with velocity (growth rate).
- A 1000-like post at 10/h → 1000 × log(11) ≈ 2398
- A 100-like post at 100/h → 100 × log(101) ≈ 462
- Velocity is weighted logarithmically to prevent tiny posts with high velocity from dominating
