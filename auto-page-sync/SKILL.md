---
name: auto-page-sync
description: 仓库 Markdown/JSON 内容自动同步到前端页面，配置 GitHub Actions 定时拉取 + 部署，保持 Google SEO 内容新鲜度。支持日报、博客、Changelog、Landing Page 等多种页面模式。
keywords: auto sync, github actions, cron, markdown, blog, report, landing page, seo freshness, sitemap, content pipeline, static site
version: 1.0
---

# Auto Page Sync — 仓库内容自动同步到前端页面

将仓库中的 Markdown / JSON 内容自动同步到前端项目，生成对应页面，并通过 GitHub Actions 定时更新，确保 Google SEO 内容新鲜度。

## When This Skill Applies

- 当用户说「把仓库的 XX 目录同步到网站」时
- 当用户说「每天自动更新页面内容」时
- 当用户需要把 Markdown 报告、博客文章、Changelog 展示到前端时
- 当用户提到「SEO 内容新鲜度」「定时更新」「自动部署」时
- 当用户需要配置 GitHub Actions 定时同步内容到前端时

## 核心价值

手动更新网站内容既耗时又容易遗忘。这个 Skill 让你：
- 只管往仓库写 Markdown，前端页面自动生成
- GitHub Actions 定时拉取，零人工干预
- 每次更新自动触发部署，Google 爬虫看到的永远是最新内容
- 支持多种页面形态，一套机制复用所有项目

## Instructions

### Step 1: 分析内容源

1. 读取用户指定的仓库目录结构
2. 识别内容格式（Markdown、JSON、YAML）
3. 分析内容组织方式（按日期、按分类、单文件）
4. 确定元数据提取规则（标题、日期、标签等）

```bash
# 典型的内容源结构
daily-reports/
├── 2026-04-10/
│   ├── morning-report.md
│   └── youtube-report.md
├── 2026-04-11/
│   ├── morning-report.md
│   └── youtube-report.md

# 或者博客结构
blog/
├── 2026-04-10-my-first-post.md
├── 2026-04-11-another-post.md
```

### Step 2: 选择页面模式

根据内容类型选择合适的模式：

| 模式 | 适用场景 | 路由结构 | 特点 |
|------|---------|---------|------|
| A: 日报型 | 每日报告、周报 | `/reports/[date]` | 日期导航 + Tab 切换 |
| B: 博客型 | 文章、教程 | `/blog/[slug]` | 列表页 + 分类筛选 |
| C: 动态区块型 | Landing Page 数据 | 更新现有页面区块 | 无新路由 |
| D: Changelog 型 | 更新日志 | `/changelog` | 单页时间线 |

### Step 3: 创建静态数据管道

将内容文件复制到前端项目的 `public/data/` 目录，并生成索引文件。

**目标目录结构：**
```
public/data/{content-type}/
├── index.json          # 索引文件
├── 2026-04-10/
│   ├── report-a.md
│   └── report-b.md
└── 2026-04-11/
    ├── report-a.md
    └── report-b.md
```

**index.json 标准格式：**
```json
{
  "dates": ["2026-04-11", "2026-04-10"],
  "latest": "2026-04-11",
  "items": {
    "2026-04-11": [
      {
        "slug": "unique-identifier",
        "title": "显示标题",
        "icon": "🎮",
        "filename": "source-file.md",
        "description": "可选摘要",
        "tags": ["可选标签"]
      }
    ]
  }
}
```

### Step 4: 生成前端页面

根据目标框架生成页面代码。以下以 Next.js App Router 为例：

**必须遵循的原则：**
- 读取项目现有的 `layout.tsx`、`globals.css`、组件库，匹配设计风格
- 使用项目已安装的依赖（如 `react-markdown`、`remark-gfm`）
- 响应式设计，移动端友好
- 支持暗色模式（如果项目已有）

**日报型页面结构（模式 A）：**
```
app/reports/page.tsx              # 重定向到最新日期
app/reports/[date]/page.tsx       # 日期详情页
components/report-viewer.tsx      # 内容渲染组件
```

**博客型页面结构（模式 B）：**
```
app/blog/page.tsx                 # 文章列表页
app/blog/[slug]/page.tsx          # 文章详情页
components/blog-card.tsx          # 文章卡片组件
```

**内容渲染组件核心逻辑：**
```tsx
// 使用 react-markdown + remark-gfm 渲染 Markdown
import ReactMarkdown from "react-markdown"
import remarkGfm from "remark-gfm"

<article className="prose prose-neutral dark:prose-invert max-w-none">
  <ReactMarkdown remarkPlugins={[remarkGfm]}>
    {markdownContent}
  </ReactMarkdown>
</article>
```

### Step 5: 添加导航入口

在项目的全局导航中添加新页面链接，使用与现有导航一致的样式。

### Step 6: 配置 GitHub Actions 定时同步

创建 `.github/workflows/sync_{content_type}.yml`：

```yaml
name: Sync {ContentType} to Frontend

on:
  schedule:
    - cron: '{cron_expression}'  # UTC 时间，注意时区转换
  workflow_dispatch:              # 允许手动触发

permissions:
  contents: write

jobs:
  sync:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
      with:
        fetch-depth: 0

    - name: Sync content files
      run: |
        set -e
        SRC="{source_directory}"
        DST="{frontend_public_data_path}"
        mkdir -p "$DST"
        if [ -d "$SRC" ]; then
          for dir in "$SRC"/*/; do
            name=$(basename "$dir")
            if [[ "$name" =~ ^[0-9]{4}-[0-9]{2}-[0-9]{2}$ ]]; then
              mkdir -p "$DST/$name"
              cp -f "$dir"*.md "$DST/$name/" 2>/dev/null || true
            fi
          done
        fi

    - name: Rebuild index.json
      run: |
        python3 .agent/skills/auto-page-sync/resources/rebuild_index.py \
          --dir "{frontend_public_data_path}"

    - name: Commit and Push
      run: |
        git config --local user.email "github-actions[bot]@users.noreply.github.com"
        git config --local user.name "github-actions[bot]"
        git pull --rebase || true
        git add {target_paths}
        git diff --quiet && git diff --staged --quiet || \
          (git commit -m "🔄 Auto-sync: {content_type} [deploy]" && git push)
```

**Cron 时间计算：**
- 用户说「每天 X 点（北京时间）」→ `X - 8` 小时 = UTC 时间
- 内容生成时间 + 1 小时 = 同步时间（确保内容已就绪）
- 示例：内容 10:00 生成 → 同步 cron 设为 `0 3 * * *`（UTC 03:00 = 北京 11:00）

### Step 7: SEO 优化（推荐）

1. **Sitemap 自动更新** — 在同步脚本中追加新 URL，设置 `lastmod` 和 `changefreq: daily`
2. **页面 Meta 标签** — 从 Markdown 标题提取 `<title>` 和 `<meta description>`
3. **结构化数据** — 博客型用 `Article` schema，报告型用 `Report` schema
4. **内容新鲜度信号** — 页面显示「最后更新时间」，可选生成 RSS Feed

## Actions

### 可用资源文件

- `resources/rebuild_index.py` — 通用索引重建脚本，可在 GitHub Actions 或本地运行
- `resources/sync_workflow_template.yml` — GitHub Actions workflow 模板，替换占位符即可用
- `resources/report_types_example.json` — 报告类型映射示例

## 完成检查清单

- [ ] 内容文件已复制到 `public/data/` 并可通过 URL 访问
- [ ] `index.json` 正确列出所有内容条目
- [ ] 前端页面能正确渲染 Markdown（含表格、代码块）
- [ ] 页面风格与项目整体一致
- [ ] 导航栏已添加入口
- [ ] GitHub Actions workflow 语法正确
- [ ] Cron 时间设置正确（注意 UTC 转换）
- [ ] Commit message 包含 `[deploy]` 触发自动部署
- [ ] 无 TypeScript 编译错误

## 使用示例

### 示例 1: 每日数据报告
```
用户输入：
"把 daily-reports/ 目录的报告同步到网站，做成报告页面，每天 11 点更新"

AI 执行：
1. 分析 daily-reports/ → 按日期组织，每天 2 份 Markdown 报告
2. 选择模式 A（日报型）
3. 复制到 public/data/reports/，生成 index.json
4. 创建 /reports/[date] 页面 + report-viewer 组件
5. 导航栏添加「每日报告」
6. 创建 sync_daily_reports.yml，cron: '0 3 * * *'
```

### 示例 2: 技术博客
```
用户输入：
"把 blog/ 目录的文章展示到网站，做成博客，每周一更新"

AI 执行：
1. 分析 blog/ → 按文件组织，Markdown 带 frontmatter
2. 选择模式 B（博客型）
3. 复制到 public/data/blog/，生成 index.json
4. 创建 /blog 列表页 + /blog/[slug] 详情页
5. 导航栏添加「Blog」
6. 创建 sync_blog.yml，cron: '0 0 * * 1'（每周一 UTC 00:00）
```

### 示例 3: Landing Page 数据更新
```
用户输入：
"把 data/stats.json 的数据同步到首页的统计区块，每天更新"

AI 执行：
1. 分析 data/stats.json → 单文件 JSON
2. 选择模式 C（动态区块型）
3. 复制到 public/data/stats.json
4. 修改首页组件读取该 JSON 渲染统计区块
5. 创建 sync_stats.yml，cron: '0 2 * * *'
```

## 支持的框架

| 框架 | 页面生成 | Markdown 渲染 | 备注 |
|------|---------|--------------|------|
| Next.js (App Router) | ✅ 完整支持 | react-markdown + remark-gfm | 推荐 |
| Next.js (Pages Router) | ✅ 支持 | react-markdown + remark-gfm | |
| Astro | ✅ 支持 | 内置 Markdown 支持 | |
| Hugo / Jekyll | ✅ 支持 | 原生 Markdown | 静态站点 |
| Vite + React | ✅ 支持 | react-markdown | 需手动路由 |

## 注意事项

- 内容源和前端项目在同一仓库时最简单；跨仓库需要在 Actions 中配置多仓库 checkout
- 首次同步大量历史内容时注意 Git commit 大小
- 不同部署平台（Cloudflare Pages / Vercel / Netlify）的自动部署触发方式可能不同
- 确保 Markdown 文件使用 UTF-8 编码
