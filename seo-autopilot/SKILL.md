---
name: seo-autopilot
description: 全自动 SEO 内容新鲜度引擎。监听关键词研究报告目录，自动生成落地页和博客文章，运行 SEO 审计后推送更新。适用于任何需要定期更新内容以保持 Google 排名新鲜度的网站项目。支持 Next.js / Astro / Nuxt 等主流框架。
keywords: seo automation, keyword report, content freshness, landing page generation, blog generation, google rankings, automated deployment, git autopull
---

# SEO Autopilot — 全自动内容新鲜度引擎

> 把关键词研究报告变成已部署的 SEO 页面，零人工干预。

## 核心价值

当你有一个外部 Agent（如 OpenClaw）定期生成关键词研究报告并推送到 Git 仓库时，这个 skill 会：

1. **自动检测**新报告（通过 git autofetch + fileCreated hook）
2. **自动解析**报告中的 Top 关键词和推荐动作
3. **自动去重**（跳过已有页面覆盖的关键词）
4. **自动决策**页面类型（落地页 vs 博客文章）
5. **自动生成**符合项目风格的页面代码
6. **自动审计**（Technical SEO + EEAT 双门检查）
7. **自动推送**（git commit + push → 触发自动部署）

**时间节省**: 从报告到页面上线，传统方式需要 2-4 小时/页，自动化后 < 5 分钟/页。

## 完整自动化链路

```
┌─────────────────────────────────────────┐
│  外部 Agent（OpenClaw 等）              │
│  生成关键词报告 → git push              │
└──────────────┬──────────────────────────┘
               │ (git push to main)
               ▼
┌─────────────────────────────────────────┐
│  IDE（Kiro / Claude Code / Cursor）     │
│  git.autofetch: true (每 2 分钟)        │
│  git.pullOnFetch: true                  │
│  → 自动拉取新 commit                    │
└──────────────┬──────────────────────────┘
               │ (检测到新 .md 文件)
               ▼
┌─────────────────────────────────────────┐
│  fileCreated Hook 触发                  │
│  Pattern: {report_dir}/*.md             │
│  → 启动 Agent 执行流水线                │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│  Agent 执行 8 阶段流水线               │
│  解析 → 去重 → 决策 → 生成 → 审计      │
│  → git commit + push                    │
└──────────────┬──────────────────────────┘
               │ (git push to main)
               ▼
┌─────────────────────────────────────────┐
│  自动部署（Vercel / Cloudflare / etc）  │
│  新页面上线生产环境                      │
└─────────────────────────────────────────┘
```

## 使用场景

- 独立站 SEO 内容持续更新（保持 Google 排名新鲜度）
- 多站点批量内容生产
- 关键词研究 → 页面上线的全链路自动化
- 任何需要定期发布新 SEO 内容的项目

## 前置依赖

| 依赖 | 说明 | 必须？ |
|------|------|--------|
| Git 仓库 | GitHub / GitLab / Bitbucket | ✅ |
| 外部关键词报告源 | 定期推送 .md 报告到仓库的 Agent 或脚本 | ✅ |
| Web 框架 | Next.js / Astro / Nuxt / 静态站 | ✅ |
| 自动部署 | Vercel / Cloudflare Pages / Netlify | ✅ |
| IDE 保持打开 | Kiro / Claude Code / Cursor（需要运行 hook） | ✅ |

## 安装方式

```bash
# 方式 1: 只复制这个 skill
cp -r 7deer_skills/seo-autopilot .agent/skills/seo-autopilot

# 方式 2: 克隆整个技能库
git clone https://github.com/kennyzir/7deer_skills.git .agent/skills
```

## 启动命令

安装后，对 Agent 说：

```
启动 SEO autopilot，报告目录是 keyword-research/
```

或英文：

```
Set up SEO autopilot, report directory is keyword-research/
```

Agent 会自动执行 7 步 setup 流程。

---

## Setup 流程（Agent 自动执行）

### Step 1: 发现项目结构

Agent 需要识别：
- 框架类型（Next.js / Astro / Nuxt / 静态）
- 页面系统（如何创建页面）
- 博客系统（如何存储博客文章）
- 导航/Sitemap 注册方式
- 现有 SEO 模式（metadata、JSON-LD、canonical）
- 关键词报告目录位置

### Step 2: 配置 Git 自动拉取

创建或更新 `.vscode/settings.json`：

```json
{
  "git.autofetch": true,
  "git.autofetchPeriod": 120,
  "git.autoStash": true,
  "git.pullOnFetch": true
}
```

> ⚠️ 不要覆盖已有设置，只合并这些 key。

### Step 3: 创建 fileCreated Hook

创建 Kiro hook 监听报告目录：

```json
{
  "name": "SEO Autopilot",
  "version": "1.0.0",
  "when": {
    "type": "fileCreated",
    "patterns": ["{report_dir}/*.md"]
  },
  "then": {
    "type": "askAgent",
    "prompt": "新的关键词研究报告已检测到。按照 #seo-autopilot steering 执行完整流水线：解析报告 → 去重 → 决策页面类型 → 生成页面(最多3个) → 注册 navigation + sitemap → SEO 审计 → git commit and push → 更新 processed.json。"
  }
}
```

### Step 4: 创建 Steering 文件

创建 `.kiro/steering/seo-autopilot.md`，包含完整的 8 阶段处理指令（见 references/steering-template.md）。

### Step 5: 初始化状态追踪

创建 `{report_dir}/processed.json`：

```json
{
  "processed": []
}
```

### Step 6: 验证

- [ ] `.vscode/settings.json` 已配置 autofetch + pullOnFetch
- [ ] Hook 文件已创建
- [ ] Steering 文件已创建
- [ ] processed.json 已初始化
- [ ] 至少有一份报告可用于测试

### Step 7: 测试运行

用现有报告执行一次完整流水线，验证所有环节正常。

---

## 8 阶段处理流水线

### Phase 0: 发现新报告
读取 processed.json → 扫描报告目录 → 过滤未处理的报告

### Phase 1: 解析报告
提取 Top 关键词、搜索意图、竞争度、推荐页面类型

### Phase 2: 去重
对比现有页面（navigation + blog），跳过已覆盖的关键词

### Phase 3: 页面类型决策
- Transactional / Emotional → 落地页
- Informational → 博客文章
- 每次报告最多生成 3 个页面

### Phase 4: 内容生成
按项目现有模式生成页面代码（metadata、JSON-LD、FAQ、内链、CTA）

### Phase 5: 注册
添加到 navigation 系统 + sitemap

### Phase 6: SEO 审计
- Title < 60 chars，含主关键词
- Description < 160 chars
- Canonical URL
- JSON-LD WebPage + FAQ schema
- H1 唯一且含关键词
- 3-5 个内链
- CTA 到主转化页面

### Phase 7: 提交推送
git add → commit → push

### Phase 8: 更新状态
更新 processed.json，记录已处理报告和生成的页面

---

## 关键词报告格式要求

报告为 Markdown 格式，需包含以下内容之一：

- "Top N 关键词" 或 "推荐动作" 章节，列出关键词和优先级
- 包含 keyword / intent / competition / action 列的表格

Agent 会自适应解析不同格式的报告。

## 状态追踪格式

```json
{
  "processed": [
    {
      "report": "2026-04-10-keyword-research.md",
      "processedAt": "2026-04-10",
      "pagesCreated": [
        { "type": "landing", "slug": "/personalized-tarot", "keyword": "personalized tarot card generator" }
      ],
      "skipped": [
        { "keyword": "oracle card generator AI", "reason": "Already covered by /ai-oracle-card-generator" }
      ]
    }
  ]
}
```

---

## 适配不同框架

| 框架 | 页面位置 | 博客位置 | Sitemap |
|------|---------|---------|---------|
| Next.js (App Router) | `app/{slug}/page.tsx` | `lib/blog.ts` 或 `content/blog/*.mdx` | `app/sitemap.ts` |
| Next.js (Pages Router) | `pages/{slug}.tsx` | `pages/blog/[slug].tsx` | `next-sitemap.config.js` |
| Astro | `src/pages/{slug}.astro` | `src/content/blog/*.md` | `astro.config.mjs` |
| Nuxt | `pages/{slug}.vue` | `content/blog/*.md` | `nuxt.config.ts` |
| 静态 HTML | `{slug}/index.html` | `blog/{slug}/index.html` | `sitemap.xml` |

---

## 限制与注意事项

- **IDE 必须保持打开**: Hook 只在 IDE 运行时生效
- **每次最多 3 页**: 避免内容质量下降
- **语义去重**: 不只是 URL 匹配，还要判断语义重叠
- **不覆盖已有页面**: 只创建新页面，不修改现有内容
- **需要网络连接**: git pull/push 需要网络

## 常见问题

| 问题 | 解决方案 |
|------|---------|
| Hook 没触发 | 检查 filePatterns 是否匹配报告文件名 |
| 自动 pull 不工作 | 重启 IDE，确认 settings.json 已加载 |
| 页面风格不匹配 | 更新 steering 文件中的示例页面引用 |
| 重复生成页面 | 检查 processed.json 是否正确更新 |
| git push 失败 | 检查 git 凭证 / SSH key 配置 |
| Build 失败 | 确保引用的 mock 数据 / 组件在远端存在 |

---

## 实战案例

CardMuse.com 使用此 skill 实现了：
- OpenClaw Agent 每 2 天生成关键词报告
- Kiro 自动拉取 + 处理报告
- 每次报告生成 2-3 个新 SEO 页面
- Vercel 自动部署
- 从报告推送到页面上线 < 5 分钟

---

## License

MIT
