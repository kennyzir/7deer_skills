---
name: nextjs-seo-booster
description: A complete SEO toolkit for Next.js applications, including structured data (Schema.org), dynamic sitemap generation, and meta tags.
version: 1.1
---

# Next.js SEO Booster Protocol

**Role**: Full-Stack SEO Toolkit
**Core Function**: 提供开箱即用的 SEO 组件代码，加速开发流程。

## When This Skill Applies
*   当用户需要 **JSON-LD Schema** 代码实现时。
*   当用户需要生成 **Dynamic Sitemap** 代码时。
*   当 `nextjs-seo-foundations` 确定了标准，需要具体组件落地时。

## Instructions

本 Skill 提供了即插即用的代码组件。

### Prerequisites
使用此 Skill 前必须安装 Type Definitions:
```bash
npm install -D schema-dts
```

### 1. Structured Data Component
*   **Source**: `resources/StructuredData.tsx`
*   **Usage**: 这是一个通用的 Schema 注入组件。它不再依赖项目特定的配置，而是通过 Props 或环境变量工作。

### 2. Sitemap Generator
*   **Source**: `resources/sitemap.ts`
*   **Usage**: 复制到 `app/sitemap.ts` 并配置路由列表。

## Actions
*   使用 `copy-item` 将资源文件复制到项目 `components/` 目录。
