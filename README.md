# 7Deer Skills

An open-source skill library for SEO automation, content pipelines, and AI agent workflows.

Built from real project work, this repository packages reusable skills with `SKILL.md` docs, scripts, templates, and references you can copy into your own projects.

## Why Star This Repo

- Turn Google Trends data into production-ready SEO page workflows
- Generate game code pages in minutes instead of rebuilding the same templates
- Reuse AI agent, scraping, and content automation skills across projects

## Quick Value

This repository is designed for builders working on:

- AI agent workflows
- SEO automation systems
- content-heavy Next.js projects
- Python automation pipelines
- Roblox and game utility sites

## P0 Skills

These are the three strongest entry points in the repository.

| Skill | Input | Output | Best For |
| --- | --- | --- | --- |
| `google-trends-to-pages` | Rising keywords from Google Trends | SEO page plans, intent classification, page structure workflows | SEO content operations |
| `multi-game-codes-hub` | Game codes JSON or structured code data | Production-ready code page templates with SEO structure | Roblox and game sites |
| `roblox-game-data-scraper` | Trello, Discord, Reddit, and game data sources | Structured game data for downstream site generation | Game data collection |

## Top Use Cases

### 1. Google Trends -> SEO Pages

Input:

```text
"yba codes" (+400%)
"how to get fuga in jujutsu infinite" (+90%)
```

Output:

- intent classification
- page type selection
- page structure templates
- SEO-ready content workflow

### 2. Game Codes Data -> Published Page

Input:

```json
{
  "gameName": "Your Bizarre Adventure",
  "gameSlug": "yba",
  "activeCodes": [
    { "code": "GULLIBLE", "reward": "5 Lucky Arrows" }
  ]
}
```

Output:

- code page template
- active / expired code sections
- FAQ schema support
- reusable components for code tables and copy actions

### 3. Raw Community Sources -> Structured Game Data

Input:

- Trello boards
- Discord channels
- Reddit threads

Output:

- normalized data files
- reusable scraping patterns
- downstream inputs for site pages, guides, and update workflows

## Workflow Visuals

### SEO Automation Flow

```mermaid
flowchart LR
  A[Google Trends Keywords] --> B[Intent Classification]
  B --> C[Template Selection]
  C --> D[SEO Page Structure]
  D --> E[Published Content Workflow]
```

### Game Codes Flow

```mermaid
flowchart LR
  A[Codes JSON or Source Data] --> B[Page Generator]
  B --> C[Next.js Page Output]
  C --> D[Schema and SEO Sections]
  D --> E[Deployable Page]
```

### Agent Skill Reuse Flow

```mermaid
flowchart LR
  A[Skill in 7Deer Skills] --> B[Copy into .agent/skills]
  B --> C[Reuse Scripts and Templates]
  C --> D[Ship Faster in New Projects]
```

## English Summary

7Deer Skills is a reusable library of practical skills extracted from real projects. Instead of starting from scratch, you can reuse agent workflows, SEO automation patterns, content generation modules, scraping utilities, and Next.js/Python building blocks across projects.

## Skill Catalog

### SEO and Content

- `google-trends-to-pages`
- `nextjs-seo-booster`
- `nextjs-seo-foundations`
- `seo-auditor`
- `youtube-content-gen`
- `youtube-game-keywords`

### Data and Research

- `roblox-game-data-scraper`
- `data-scraper-intent`
- `keyword-competition-analysis`
- `youtube-intel`
- `youtube-transcribe`

### Backlinks and Distribution

- `backlink-discovery`
- `backlink-intelligence`
- `seo-backlink-submitter`
- `seo-link-strategy`

### Game and Utility Workflows

- `multi-game-codes-hub`
- `roblox-site-architect`
- `rpg-stat-catalyst`
- `favicon-icon-generator`

### AI Agent and Builder Tools

- `python-agent-engine`
- `gemini-thinking-protocol`
- `plugin-architect`

## Repository Structure

```text
7deer_skills/
|- google-trends-to-pages/
|- multi-game-codes-hub/
|- roblox-game-data-scraper/
|- nextjs-seo-booster/
|- nextjs-seo-foundations/
|- seo-auditor/
|- python-agent-engine/
|- data-scraper-intent/
|- backlink-discovery/
|- backlink-intelligence/
|- seo-backlink-submitter/
|- seo-link-strategy/
|- youtube-content-gen/
|- youtube-game-keywords/
|- youtube-intel/
|- youtube-transcribe/
|- roblox-site-architect/
|- rpg-stat-catalyst/
|- favicon-icon-generator/
|- gemini-thinking-protocol/
|- plugin-architect/
|- .github/
|- CONTRIBUTING.md
|- SECURITY.md
`- LICENSE
```

## Quick Start

### Clone into an Agent Skills Directory

```bash
git clone https://github.com/kennyzir/7deer_skills.git .agent/skills
```

### Add as a Git Submodule

```bash
git submodule add https://github.com/kennyzir/7deer_skills.git .agent/skills
```

### Copy a Single Skill

If you only need one workflow, copy that skill directory into your own project and follow its `SKILL.md`.

## How to Evaluate a Skill

Each top-level skill should give you:

- a clear `SKILL.md`
- reusable code or templates
- a practical workflow, not just abstract prompts
- enough structure to adapt it into a real project

## Security Notes

- No real API keys, tokens, or credentials should be committed
- Use placeholders like `your_api_key_here`
- Review `.gitignore` before adding generated reports or project-specific data
- See [SECURITY.md](./SECURITY.md) for reporting guidance

## Contributing

Contributions are welcome. Before opening a pull request:

- keep skills self-contained
- include or update `SKILL.md`
- document required dependencies
- sanitize examples and remove secrets

See [CONTRIBUTING.md](./CONTRIBUTING.md).

## Suggested GitHub Topics

If you want better repository discovery, add these topics on GitHub:

- `ai-agents`
- `seo`
- `nextjs`
- `python`
- `automation`
- `prompts`
- `tooling`
- `content-generation`

## License

MIT License. See [LICENSE](./LICENSE).
