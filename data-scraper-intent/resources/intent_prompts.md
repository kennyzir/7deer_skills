# Search Intent Analysis Prompts

Use these prompts with your LLM (GPT-4, Claude, DeepSeek) to classify keywords for SEO content planning.

---

## Prompt 1: Keyword Intent Classifier

**Use Case**: Given a list of keywords, classify each by search intent.

```
You are an expert SEO analyst. For each keyword below, classify it into ONE of these categories:
1. **Informational**: User wants to learn or understand something. (e.g., "how to...", "what is...")
2. **Navigational**: User wants to find a specific website or page. (e.g., "[brand] login", "[game] wiki")
3. **Transactional**: User wants to take an action or use a tool. (e.g., "[game] codes", "[tool] calculator")
4. **Commercial**: User is researching before a purchase. (e.g., "[product] review", "[product] vs [product]")

Output as a JSON array: [{ "keyword": "...", "intent": "...", "reasoning": "..." }]

Keywords:
{PASTE_KEYWORDS_HERE}
```

---

## Prompt 2: Content Type Recommender

**Use Case**: After classifying intent, decide what type of content to create.

```
Based on the keyword intents below, recommend the best content type for each.

Content Types:
- **Guide Page**: Deep-dive article with H2 sections, FAQ, and images.
- **Tool Page**: Interactive calculator, checker, or generator.
- **List Page**: Rankings, "Top 10", or curated collections.
- **Hub Page**: A central index page linking to multiple sub-pages.
- **Comparison Page**: A vs B analysis.

For each keyword, output: { "keyword": "...", "content_type": "...", "page_title_suggestion": "..." }

Intents:
{PASTE_CLASSIFIED_KEYWORDS_HERE}
```

---

## Prompt 3: Google Trends Filter

**Use Case**: Filter a list of Google Trends keywords to keep only those relevant to your niche.

```
I run a website about [YOUR_NICHE]. Below is a list of "rising" keywords from Google Trends.

Your task:
1. Filter out any keywords that are NOT relevant to my niche.
2. For remaining keywords, rate them 1-5 on "content opportunity" (5 = high search volume, low competition, high user intent).
3. Sort by rating, descending.

Output as a markdown table: | Keyword | Relevance | Rating | Reason |

Keywords:
{PASTE_TREND_KEYWORDS_HERE}
```

---

## Prompt 4: FAQ Question Generator

**Use Case**: Generate FAQ questions for a given topic to use in FAQPage schema.

```
I am writing a page about "[TOPIC]".
Generate 6-8 frequently asked questions that users might search for on Google.

Rules:
1. Questions should start with "How", "What", "Where", "When", "Why", or "Can".
2. Questions should be specific, not generic.
3. Prioritize questions with high search volume potential.

Output as a numbered list.
```
