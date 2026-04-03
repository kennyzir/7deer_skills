# 🛠️ 7Deer Skills Library

> **开源技能库** - 可复用的 AI Agent 能力模块集合

这是一个开源技能库，包含了从多个项目中提炼出来的可复用代码模块和指令模板。
将此仓库克隆到任何新项目的 `.agent/skills` 目录，AI Agent 即可自动加载这些能力。

---

## 📦 技能清单

| # | 技能名称 | 描述 | 适用场景 |
|---|---------|------|---------|
| 1 | **nextjs-seo-booster** | Next.js SEO 工具包（结构化数据 + Sitemap） | 任何 Next.js 网站 |
| 2 | **nextjs-seo-foundations** | Next.js SEO 工程化规范（Metadata + Performance） | Next.js 14+ 应用 |
| 3 | **python-agent-engine** | Python AI Agent 引擎（ReAct 模式 + 工具调用） | Python 后端 AI 应用 |
| 4 | **rpg-stat-catalyst** | RPG 数值计算核心（属性加点 + 阈值计算） | 游戏类应用 |
| 5 | **seo-auditor** | SEO 审计框架（检查清单 + 自动化脚本） | 任何网站 SEO 优化 |
| 6 | **data-scraper-intent** | 数据提取 & 搜索意图分析（爬虫模式 + LLM Prompt） | SEO/数据采集工作流 |
| 7 | **youtube-content-gen** | YouTube 内容生成器（视频转 SEO 页面） | 攻略/教程类站点 |
| 8 | **favicon-icon-generator** | Favicon & Icon 生成器（SVG + PWA + 自动化） | Web 应用图标系统 |
| 9 | **gemini-thinking-protocol** | 核心认知引擎（第一性原理 + 系统思维） | 复杂需求分析 |
| 10 | **plugin-architect** | AI Skills/Plugins 构建标准方法论 | 创建新技能 |
| 11 | **roblox-site-architect** | Roblox 游戏工具站 SEO 架构 | Roblox 游戏网站 |
| 12 | **backlink-discovery** | 外链机会发现引擎（web_search 多轮关键词派生） | 外链建设 |
| 13 | **keyword-competition-analysis** | 谷歌关键词竞争度分析 | SEO 调研 |
| 14 | **seo-backlink-submitter** | 批量目录提交工具（Playwright 自动化） | 外链分发 |
| 15 | **seo-link-strategy** | 外链策略生成器（三阶段：发现→评估→执行） | 外链营销 |

---

## 🚀 如何使用

### 方法 1: 克隆到新项目
```bash
# 在新项目根目录执行
git clone https://github.com/kennyzir/7deer_skills.git .agent/skills
```

### 方法 2: 作为 Git Submodule
```bash
git submodule add https://github.com/kennyzir/7deer_skills.git .agent/skills
```

### 方法 3: 手动复制
直接复制需要的技能文件夹到项目中。

---

## 📁 目录结构

```
7deer_skills/
├── README.md                      # 本文档
├── backlink-discovery/            # 外链机会发现引擎
├── data-scraper-intent/          # 数据提取 & 搜索意图分析
├── favicon-icon-generator/        # Favicon & Icon 生成器
├── gemini-thinking-protocol/      # 核心认知引擎
├── keyword-competition-analysis/  # 关键词竞争度分析
├── nextjs-seo-booster/            # Next.js SEO 工具包
├── nextjs-seo-foundations/        # Next.js SEO 工程化规范
├── plugin-architect/              # AI Skills 构建标准
├── python-agent-engine/           # Python AI Agent 引擎
├── roblox-site-architect/         # Roblox 站点架构
├── rpg-stat-catalyst/             # RPG 数值计算核心
├── seo-auditor/                   # SEO 审计框架
├── seo-backlink-submitter/        # 批量目录提交工具
├── seo-link-strategy/             # 外链策略生成器
└── youtube-content-gen/           # YouTube 内容生成器
```

---

## 🔐 安全说明

> ⚠️ **所有技能均不包含任何 API Key 或敏感数据。**
> 涉及外部 API 的技能通过环境变量读取密钥。

---

## 📝 更新日志

### 2026-04-04
- 添加 backlink-discovery（外链机会发现引擎）
- 添加 keyword-competition-analysis（关键词竞争度分析）
- 添加 seo-backlink-submitter（批量目录提交工具）
- 添加 seo-link-strategy（外链策略生成器）

### 2026-02-09
- 添加 favicon-icon-generator（图标生成系统）
- 添加 gemini-thinking-protocol（认知引擎）
- 添加 plugin-architect（技能构建标准）
- 添加 roblox-site-architect（Roblox 站点架构）
- 添加 nextjs-seo-foundations（SEO 工程化规范）

### 2026-01-17
- 初始化技能库
- 添加 5 个核心技能模块

---

## 📄 License

MIT License - 开源分享，欢迎使用和贡献
