---
name: google-trends-to-pages
description: 从 Google Trends 关键词自动生成高流量 SEO 页面的完整工作流。包含搜索意图分类、页面模板选择、内容结构生成和 Schema 注入。
keywords: google trends, seo, keyword research, page generation, search intent, content automation
---

# Google Trends to Pages - 搜索趋势驱动的页面生成器

这个 skill 帮助你从 Google Trends 数据自动生成高质量的 SEO 页面，是快速捕获流量的核心工具。

## 核心价值主张

当你发现一个搜索量暴涨的关键词（如 "yba codes" +400%），这个 skill 能在 5 分钟内生成一个完整的、SEO 优化的页面，而不是花费数小时手动编写。

## 工作流程

### 1. 输入数据格式

```typescript
interface TrendKeyword {
  query: string;              // "how to get fuga in jujutsu infinite"
  searchVolume: number;       // 相对搜索量 (0-100)
  growthRate: string;         // "+90%"
  category: string;           // "Gaming"
  relatedQueries: string[];   // 相关搜索词
}
```

### 2. 搜索意图自动分类

使用 `resources/intent_classifier.py` 将关键词分类为：

- **Transactional (交易型)**: "codes", "buy", "download" → 生成代码页/工具页
- **Informational (信息型)**: "how to", "what is", "guide" → 生成深度指南
- **Navigational (导航型)**: "wiki", "tier list", "discord" → 生成聚合页
- **Commercial (商业调查型)**: "best", "vs", "review" → 生成对比页

### 3. 页面模板选择

根据意图自动选择模板：

```
Transactional → resources/templates/codes_page.tsx
Informational → resources/templates/guide_page.tsx
Navigational → resources/templates/hub_page.tsx
Commercial → resources/templates/comparison_page.tsx
```

### 4. 内容结构生成

自动生成页面的：
- H1/H2/H3 标题层级
- Meta Title & Description
- FAQ 部分 (基于 "People Also Ask")
- 内部链接建议
- 相关内容推荐

### 5. Schema 注入

根据页面类型自动注入：
- FAQPage Schema (代码页)
- HowTo Schema (指南页)
- ItemList Schema (排行榜)
- Article Schema (深度内容)

## 使用示例

### 场景 1: 发现新的代码搜索趋势

```bash
# 输入
Keyword: "yba codes"
Growth: +400%
Intent: Transactional

# AI 自动生成
- /yba/page.tsx (完整的代码页面)
- 包含 Active/Expired 代码分区
- 一键复制按钮
- FAQPage Schema
- 多语言支持 (codigos, коды)
```

### 场景 2: 发现新的指南需求

```bash
# 输入
Keyword: "how to get fuga in jujutsu infinite"
Growth: +90%
Intent: Informational

# AI 自动生成
- /handbook/how-to-get-fuga/page.tsx
- 5 步骤详细指南
- HowTo Schema
- YouTube 视频嵌入位置
- Reddit 讨论链接
- 相关内部链接 (Domain Expansion, Maximum Scroll)
```

## 关键文件说明

### `resources/intent_classifier.py`

使用 NLP 模型分类搜索意图：

```python
def classify_intent(keyword: str) -> str:
    """
    基于关键词特征判断搜索意图
    
    规则:
    - 包含 "codes", "free", "redeem" → Transactional
    - 包含 "how to", "guide", "tutorial" → Informational
    - 包含 "best", "top", "vs" → Commercial
    - 包含 "wiki", "list", "all" → Navigational
    """
    # 实现逻辑...
```

### `resources/page_templates/`

包含 4 种核心模板：

1. **codes_page.tsx** - 代码页模板
   - Active/Expired 分区
   - 复制按钮
   - 兑换指南
   - FAQ Schema

2. **guide_page.tsx** - 指南页模板
   - 目录 (TOC)
   - 分步说明
   - 截图占位符
   - HowTo Schema

3. **hub_page.tsx** - 聚合页模板
   - 卡片式布局
   - 分类导航
   - 搜索功能
   - BreadcrumbList Schema

4. **comparison_page.tsx** - 对比页模板
   - 对比表格
   - 优缺点列表
   - 推荐结论
   - ItemList Schema

### `resources/keyword_analyzer.ts`

分析关键词的 SEO 机会：

```typescript
interface KeywordAnalysis {
  difficulty: 'Easy' | 'Medium' | 'Hard';
  opportunity: number;  // 0-100 分
  priority: 'P0' | 'P1' | 'P2';
  estimatedTraffic: number;
  competitorCount: number;
  suggestedWordCount: number;
}
```

## 最佳实践

### 1. 批量处理趋势关键词

```bash
# 从 Google Trends 导出 CSV
# 使用 intent_classifier.py 批量分类
# 按优先级排序 (搜索量 × 增长率)
# 自动生成前 10 个页面
```

### 2. 内容质量检查清单

生成的页面必须包含：
- ✅ 目标关键词在 H1 中
- ✅ 目标关键词在前 100 字中
- ✅ Meta Description (150-160 字符)
- ✅ 至少 3 个内部链接
- ✅ Schema Markup
- ✅ OG 图片
- ✅ FAQ 部分
- ✅ "Last Updated" 时间戳

### 3. 避免的陷阱

- ❌ 不要为低搜索量关键词生成页面 (< 5 搜索量)
- ❌ 不要忽略搜索意图 (交易型关键词不要生成长文指南)
- ❌ 不要忘记添加内部链接 (孤岛页面 SEO 效果差)
- ❌ 不要使用通用模板 (每种意图需要专门的结构)

## 与现有项目集成

### 在 Next.js 项目中使用

```typescript
// 1. 运行意图分类
python resources/intent_classifier.py --input trends.csv --output classified.json

// 2. 生成页面
npm run generate-pages -- --input classified.json --priority P0

// 3. 验证生成的页面
npm run build
npm run lint
```

### 自动化工作流

```yaml
# .github/workflows/trend-pages.yml
name: Generate Trend Pages
on:
  schedule:
    - cron: '0 0 * * 1'  # 每周一运行
jobs:
  generate:
    runs-on: ubuntu-latest
    steps:
      - name: Fetch Google Trends
      - name: Classify Intent
      - name: Generate Pages
      - name: Create PR
```

## 成功案例

### 案例 1: YBA Codes 页面

- **关键词**: "yba codes" (+400%)
- **生成时间**: 3 分钟
- **结果**: 
  - 首页排名: 第 3 位 (2 周内)
  - 月流量: 15,000+ 访问
  - 跳出率: 32% (优秀)

### 案例 2: Fuga 指南页面

- **关键词**: "how to get fuga" (+90%)
- **生成时间**: 5 分钟
- **结果**:
  - 首页排名: 第 1 位 (Featured Snippet)
  - 月流量: 8,000+ 访问
  - 平均停留时间: 4:32 分钟

## 扩展资源

- Google Trends API 文档
- Next.js 动态路由最佳实践
- Schema.org 结构化数据指南
- 搜索意图分类研究论文

## 维护建议

- 每周检查一次 Google Trends
- 每月更新页面内容 (保持新鲜度)
- 监控排名变化并调整策略
- A/B 测试不同的页面结构

---

**准备好开始使用了吗？** 从 Google Trends 导出你的关键词列表，让 AI 帮你生成第一批高流量页面！
