---
name: nextjs-seo-foundations
description: Next.js 14 应用的生产级 SEO 工程化规范 (Metadata, Schema, Performance)
version: 1.0
---

# 🚀 Next.js SEO Foundations

**Role**: SEO Engineer (SEO 工程师)
**Core Function**: 确保代码符合 Technical SEO 工业标准。

## When This Skill Applies
*   当用户要求 "Check SEO" 或 "Optimize page" 时。
*   当编写 `generateMetadata` 函数时。
*   当添加 `StructuredData` 或 JSON-LD 时。
*   当进行代码审查 (Code Review) 涉及性能指标 (LCP/CLS) 时。

## Instructions

本 Skill 定义了构建高流量 Next.js 站点的**工程标准**。

### 1. Metadata 架构 (The Logic of Tags)

#### 1.1 动态标题策略
*   **Rule**: 必须包含 `Month Year` 以保持新鲜度。
*   **Code Pattern**:
    ```typescript
    export async function generateMetadata(): Promise<Metadata> {
      const date = new Date();
      const monthYear = date.toLocaleDateString('en-US', { month: 'long', year: 'numeric' });
      return { title: `Codes (${monthYear}) ...` }
    }
    ```

#### 1.2 Canonical URL 强制性
*   **Fatal Error**: 缺少 Canonical 会导致权重分散。
*   **Fix**: 统一使用**带尾部斜杠**的绝对路径。

### 2. 结构化数据体系 (Schema Graph)

任何高流量页面 (Hub Page) 必须包含 Schema 组合拳：
1.  **BreadcrumbList**: 层级结构。
2.  **FAQPage**: 抢占 PAA 区域 (>= 5 Questions)。
3.  **VideoGame**: 产品本体。

### 3. 性能即 SEO (Performance as SEO)

#### 3.1 图片优化 (LCP)
*   **Rule**: 首屏大图 (Hero Image) 必须添加 `priority` 属性。

#### 3.2 交互延迟 (FID/INP)
*   **Optimization**: 将非首屏交互组件 (Chart, Calculator) 使用 `next/dynamic` 延迟加载。

## Commands
*   `/audit-seo [url]`: 运行 SEO 完整性检查。
