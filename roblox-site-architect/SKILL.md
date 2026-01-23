---
name: roblox-site-architect
description: 专用于构建高流量 Roblox 游戏工具站的 SEO 架构与工程化方法论
version: 1.0
---

# 🏗️ Roblox Site Architect (RSA) Protocol

**Role**: SEO Architect (流量架构师)
**Core Function**: 快速构建符合工业标准的 Roblox 游戏工具站。

## When This Skill Applies
*   当用户要求 "Create a new site" 或 "Plan a new game project" 时。
*   当用户询问 "How to get traffic?" 或 "SEO Strategy" 时。
*   当需要生成 `game.config.json` 或设计站点架构时。

## Instructions

### 1. 核心方法论 (The Theory)

#### 1.1 三层架构模型 (The 3-Layer Architecture)
所有站点必须遵循以下分层，以实现 80% 的代码复用：
*   **Layer 1: 核心层 (Core)**: 100% 复用的基础设施 (Next.js, Sitemap, CF Pages)。
*   **Layer 2: 主题层 (Theme)**: `game.config.json` 驱动的 UI 风格。
*   **Layer 3: 特性层 (Feature)**: 加点模拟器、抽卡模拟器等游戏特异性功能。

#### 1.2 关键词布局策略 (Keyword Strategy)
*   **Hub**: 首页及一级导航 (Codes, Trello, Wiki)。
*   **Spoke (PSEO)**: 批量生成的实体页 (Weapons, Fruits)。
*   **Trending**: 注入 `GAME_VERSION` 变量 (e.g., "Updated for 4.0")。

### 2. 实操落地指南 (Actionable Instructions)

#### Step 1: 建立配置源
创建 `data/game.config.json` 是第一步。
```json
{
  "seo": { "gameName": "Blox Fruits", "version": "Update 21" },
  "routes": [{ "path": "/codes", "keyword": "codes" }]
}
```

#### Step 2: 实现 PSEO 动态页
*   Data: `data/items.ts`
*   Route: `app/items/[slug]/page.tsx`
*   Metadata: 动态生成 Title/Description

#### Step 3: 部署自动化内容管线 (The Gemini Loop)
不要手动写 Blog。
*   **Source**: YouTube 视频。
*   **Process**: 使用 `youtube-content-gen` 技能每天自动生成。
*   **Goal**: 保持 "Content Velocity"。

### 3. Verification
*   检查是否所有 Hub 页面都存在。
*   检查 PSEO 页面是否生成了正确的 Sitemap。
