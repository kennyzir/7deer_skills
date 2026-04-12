# 🛠️ 7Deer Skills — Agent Skills 开放标准技能库

> 25 个可复用的 AI Agent 技能模块，基于 [Agent Skills 开放标准](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills)构建。
> 克隆到项目中，你的 AI Agent 即可自动发现并加载这些能力。

这是一个开源技能库，包含了从实际项目中提炼出来的可复用代码模块和指令模板。
将此仓库克隆到任何新项目的 `.agent/skills` 目录，AI Agent 即可自动加载这些能力。

每个技能都不是凭空设计的 — 它们来自真实的独立站运营、游戏工具站搭建和出海内容项目，经过反复打磨后整理成可复用模块。

### 🌟 特色

🔍 **SEO 全链路自动化** — 从 Google Trends 热词发现，到搜索意图分类，到页面自动生成，再到外链建设和关键词竞争度分析。`google-trends-to-pages` 能把一个上升关键词在几分钟内变成一个带 Schema 标记的 SEO 页面；`site-keyword-research` 用三层漏斗（30 词初筛 → 10 词 SERP 分析 → 3 词定方向）帮你找到真正值得做的词。

🎮 **游戏站批量生产** — 做 Roblox 游戏工具站最头疼的是内容更新。`multi-game-codes-hub` 让你 5 分钟从一个 JSON 文件生成完整的代码兑换页面（含 Active/Expired 分区、一键复制、FAQ Schema）；`roblox-game-data-scraper` 直接从 Trello 看板和 Discord 频道抓取游戏数据，不用手动搬运。

📣 **社交媒体内容运营** — `null-axiom-twitter` 不是简单的推文生成器，它内置了完整的人设体系、五大内容支柱和发布节奏规划，能按比例自动选择话题方向，生成三个不同风格的草稿（锐利版 / 故事版 / 数据版）供你挑选。

📺 **YouTube 内容情报** — `youtube-intel` 帮你扫描一个类目的竞争格局（六步工作流：需求分析 → 策略制定 → 数据获取 → 清洗 → 识别 → 保存），`youtube-transcribe` 把视频转成文字稿存入 memory，`youtube-content-gen` 再把视频内容转化成 SEO 页面。

🔗 **外链建设自动化** — 从发现机会（`backlink-discovery`）到评估目录（`backlink-intelligence`）到生成个性化邮件（`seo-link-strategy`）到批量提交（`seo-backlink-submitter`），四个技能串起完整的外链工作流。

🧩 **不是 prompt 收集，是可执行的工作流** — 每个技能都包含 `SKILL.md` 文档 + 可直接运行的脚本 / 模板 / 参考文件。不是告诉你「应该怎么做」，而是直接帮你做。

🔄 **内容自动同步** — `auto-page-sync` 让你只管往仓库写 Markdown，前端页面自动生成。配合 GitHub Actions 定时拉取，Google 爬虫看到的永远是最新内容。支持日报、博客、Changelog、Landing Page 等多种页面模式，一套机制复用所有项目。

[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](./LICENSE)
[![Skills](https://img.shields.io/badge/skills-25-blue.svg)](#-完整技能清单)
[![Agent Skills Standard](https://img.shields.io/badge/standard-Agent_Skills-8A2BE2.svg)](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills)
[![Contributions Welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg)](./CONTRIBUTING.md)

---

## ⚡ 30 秒上手

```bash
# 克隆到项目的 skills 目录，Agent 自动加载
git clone https://github.com/kennyzir/7deer_skills.git .agent/skills
```

就这样。你的 Agent 会自动扫描每个 `SKILL.md` 的 name 和 description，在你的请求匹配时自动激活对应技能。

---

## 🔌 兼容的 IDE / Agent 框架

本技能库遵循 Anthropic 发起的 **Agent Skills 开放标准**（SKILL.md 格式），已被以下工具原生支持：

| IDE / 框架 | 技能目录位置 | 加载方式 |
|-----------|------------|---------|
| **Claude Code** | `.agent/skills/` | 自动发现，`/skill-name` 斜杠命令调用 |
| **Kiro** (AWS) | `.agent/skills/` | 自动发现，匹配请求时激活 |
| **Cursor** | `.cursor/skills/` 或 `.agent/skills/` | 通过 Rules 引用或自动加载 |
| **VS Code + Copilot** | `.agent/skills/` | GitHub Copilot Agent 模式自动加载 |
| **OpenAI Codex** | `.agent/skills/` | 自动发现 |
| **Gemini CLI** | `.agent/skills/` | 自动发现 |
| **OpenClaw** | `~/.openclaw/skills/` 或项目内 `.agent/skills/` | 自动加载，ClawHub 分发 |
| **Windsurf** | `.agent/skills/` | 自动发现 |

### 不同 IDE 的安装方式

```bash
# Claude Code / Kiro / VS Code Copilot / Codex / Gemini CLI（通用）
git clone https://github.com/kennyzir/7deer_skills.git .agent/skills

# Cursor（也支持 .agent/skills，或复制到 .cursor/skills）
git clone https://github.com/kennyzir/7deer_skills.git .agent/skills

# OpenClaw（全局安装，所有项目共享）
git clone https://github.com/kennyzir/7deer_skills.git ~/.openclaw/skills/7deer

# 只要一个技能？直接复制文件夹
cp -r 7deer_skills/google-trends-to-pages .agent/skills/
```

### 技能如何工作

```
1. 启动时 → Agent 只读取每个 SKILL.md 的 name + description（轻量）
2. 你的请求匹配 → Agent 加载完整 SKILL.md 指令
3. 执行时 → 按需加载 scripts / templates / references
```

这就是 Agent Skills 标准的「渐进式披露」机制 — 不会一次性塞满上下文，只在需要时加载。

---

## 🎯 核心技能 (P0 优先级)

这些是最常用、最实用的技能，适合快速启动新项目：

| # | 技能名称 | 描述 | 时间节省 | 适用场景 |
|---|---------|------|---------|---------|
| 🔥 | **google-trends-to-pages** | 从 Google Trends 关键词自动生成 SEO 页面 | 90% | SEO 内容生产 |
| 🔥 | **multi-game-codes-hub** | 5 分钟生成完整的游戏代码页面 | 95% | Roblox/游戏网站 |
| 🔥 | **roblox-game-data-scraper** | 从 Trello/Discord/Reddit 抓取游戏数据 | 80% | 游戏数据采集 |

---

## 📦 完整技能清单

### SEO & 内容生成
| # | 技能名称 | 描述 | 适用场景 |
|---|---------|------|---------|
| 1 | **google-trends-to-pages** | Google Trends → SEO 页面（意图分类 + 模板选择） | SEO 内容自动化 |
| 2 | **nextjs-seo-booster** | Next.js SEO 工具包（结构化数据 + Sitemap） | 任何 Next.js 网站 |
| 3 | **nextjs-seo-foundations** | Next.js SEO 工程化规范（Metadata + Performance） | Next.js 14+ 应用 |
| 4 | **seo-auditor** | SEO 审计框架（检查清单 + 自动化脚本） | 网站 SEO 优化 |
| 5 | **youtube-content-gen** | YouTube 内容生成器（视频转 SEO 页面） | 攻略/教程类站点 |
| 6 | **youtube-game-keywords** | YouTube 订阅频道游戏关键词提取 | 内容创作/游戏赛道 |
| 7 | **site-keyword-research** | 整站关键词研究（30词初筛→10词详析→3词定方向） | SEO 关键词调研 |
| 8 | **seo-autopilot** | 全自动 SEO 内容新鲜度引擎（报告 → 生成 → 审计 → 部署） | SEO 内容自动化 |

### 数据采集 & 分析
| # | 技能名称 | 描述 | 适用场景 |
|---|---------|------|---------|
| 8 | **roblox-game-data-scraper** | Trello/Discord/Reddit 游戏数据抓取 | Roblox 游戏网站 |
| 9 | **data-scraper-intent** | 数据提取 & 搜索意图分析（爬虫 + LLM） | SEO/数据采集 |
| 10 | **youtube-intel** | YouTube 内容情报与竞品监测（Discovery + Monitoring） | 选题策划/竞品分析 |
| 11 | **youtube-transcribe** | YouTube 视频转录（yt-dlp + whisper） | 视频内容提取 |

### 外链建设
| # | 技能名称 | 描述 | 适用场景 |
|---|---------|------|---------|
| 12 | **backlink-discovery** | 外链机会发现引擎（web_search 多轮派生） | 外链建设 |
| 13 | **backlink-intelligence** | AI/Tools 目录外链情报收集与评估 | 外链情报 |
| 14 | **keyword-competition-analysis** | 谷歌关键词竞争度分析 | SEO 调研 |
| 15 | **seo-backlink-submitter** | 批量目录提交工具（Playwright 自动化） | 外链分发 |
| 16 | **seo-link-strategy** | 外链策略生成器（发现→评估→邮件→自动发送） | 外链营销 |

### 游戏 & 工具
| # | 技能名称 | 描述 | 适用场景 |
|---|---------|------|---------|
| 17 | **multi-game-codes-hub** | 快速生成游戏代码页面（模板 + 组件） | Roblox/游戏网站 |
| 18 | **rpg-stat-catalyst** | RPG 数值计算核心（属性加点 + 阈值） | 游戏类应用 |
| 19 | **roblox-site-architect** | Roblox 游戏工具站 SEO 架构 | Roblox 游戏网站 |

### 自动化 & CI/CD
| # | 技能名称 | 描述 | 适用场景 |
|---|---------|------|---------|
| 20 | **auto-page-sync** | 仓库内容自动同步到前端页面（GitHub Actions 定时拉取 + SEO 新鲜度） | 报告/博客/Landing Page 自动更新 |

### AI & 开发工具
| # | 技能名称 | 描述 | 适用场景 |
|---|---------|------|---------|
| 21 | **python-agent-engine** | Python AI Agent 引擎（ReAct + 工具调用） | Python AI 应用 |
| 22 | **gemini-thinking-protocol** | 核心认知引擎（第一性原理 + 系统思维） | 复杂需求分析 |
| 23 | **plugin-architect** | AI Skills/Plugins 构建标准方法论 | 创建新技能 |

### 社交媒体 & 内容运营
| # | 技能名称 | 描述 | 适用场景 |
|---|---------|------|---------|
| 24 | **null-axiom-twitter** | Twitter/X 推文自动生成（人设调性 + 五大内容支柱） | 个人品牌运营 |

### 其他工具
| # | 技能名称 | 描述 | 适用场景 |
|---|---------|------|---------|
| 25 | **favicon-icon-generator** | Favicon & Icon 生成器（SVG + PWA） | Web 应用图标系统 |

---

## 🚀 快速开始

### 方法 1: 一键克隆（推荐）

```bash
# 在项目根目录执行，适用于 Claude Code / Kiro / VS Code Copilot / Codex / Gemini CLI
git clone https://github.com/kennyzir/7deer_skills.git .agent/skills
```

### 方法 2: Git Submodule（团队协作推荐）

```bash
git submodule add https://github.com/kennyzir/7deer_skills.git .agent/skills
```

### 方法 3: npx 一键安装（无需 git）

```bash
# 下载到当前项目
npx degit kennyzir/7deer_skills .agent/skills
```

### 方法 4: 只要某个技能

```bash
# 只复制你需要的技能
npx degit kennyzir/7deer_skills/google-trends-to-pages .agent/skills/google-trends-to-pages
```

### 安装后验证

```bash
# 检查技能是否就位
ls .agent/skills/*/SKILL.md

# 在 Claude Code 中测试
# 输入 / 查看可用的斜杠命令，你应该能看到所有技能
```

---

## 💡 使用示例

### 示例 1: 生成游戏代码页面

```bash
# 1. 准备数据文件
cat > yba_codes.json << EOF
{
  "gameName": "Your Bizarre Adventure",
  "gameSlug": "yba",
  "activeCodes": [
    {"code": "GULLIBLE", "reward": "5 Lucky Arrows"}
  ]
}
EOF

# 2. 生成页面（5 分钟完成）
python .agent/skills/multi-game-codes-hub/resources/generate_code_page.py \
  --input yba_codes.json \
  --output ./src/app/yba/page.tsx

# 3. 完成！页面已生成，包含：
# ✅ Active/Expired 代码分区
# ✅ 一键复制按钮
# ✅ FAQ Schema 标记
# ✅ SEO 优化的 Metadata
```

### 示例 2: 抓取 Trello 游戏数据

```python
from trello_scraper import TrelloScraper

# 初始化抓取器（公开看板不需要 API Key）
scraper = TrelloScraper()

# 抓取看板数据
data = scraper.scrape_board('jujutsu-infinite-board-id')

# 输出结构化 JSON
# {
#   "cards": [...],
#   "lists": [...],
#   "labels": [...]
# }
```

### 示例 3: 搜索意图分类

```python
from intent_classifier import classify_intent

# 分类搜索意图
intent = classify_intent("how to get six eyes jujutsu infinite")

# 输出:
# {
#   "type": "informational",
#   "template": "guide",
#   "schema": "HowTo"
# }
```

### 示例 4: 整站关键词研究

```
输入：example.com
输出：
  阶段一 → 30+ 候选词（标注来源：PASF / RS / AI-主题 / 竞品）
  阶段二 → 10 词 SERP 详细分析 + 竞争度打分
  阶段三 → Top 3 关键词 + 具体操作建议 + 落地页方案
```

### 示例 5: YouTube 内容情报

```
输入："AI 工具类目有没有机会"
输出：
  六步工作流 → 需求分析 → 策略制定 → 数据获取 → 清洗 → 识别 → 保存
  竞争度评估：🔴高 / 🟡中 / 🟢低
  切入机会 + 数据支撑
```

---

## 📁 目录结构

```
7deer_skills/
├── README.md                          # 本文档
├── CONTRIBUTING.md                    # 贡献指南
├── SECURITY.md                        # 安全说明
├── LICENSE                            # MIT License
│
├── google-trends-to-pages/            # 🔥 Google Trends → SEO 页面
│   ├── SKILL.md
│   └── resources/
│       ├── intent_classifier.py
│       └── page_structure_generator.ts
│
├── multi-game-codes-hub/              # 🔥 游戏代码页面生成器
│   ├── SKILL.md
│   ├── USAGE.md
│   └── resources/
│       ├── generate_code_page.py
│       ├── templates/codes_page.tsx
│       ├── components/
│       ├── schemas/
│       └── examples/
│
├── roblox-game-data-scraper/          # 🔥 游戏数据抓取器
│   ├── SKILL.md
│   └── resources/
│       └── trello_scraper.py
│
├── seo-autopilot/                     # 全自动 SEO 内容新鲜度引擎
│   ├── SKILL.md
│   └── references/
│       ├── steering-template.md
│       └── setup-checklist.md
├── site-keyword-research/             # 整站关键词研究
│   ├── SKILL.md
│   └── references/
│       └── output-template.md
│
├── null-axiom-twitter/                # Twitter/X 推文生成
│   └── SKILL.md
│
├── youtube-intel/                     # YouTube 内容情报
│   ├── SKILL.md
│   └── references/
│       ├── data-model.md
│       ├── discovery-template.md
│       └── workflow.md
│
├── youtube-transcribe/                # YouTube 视频转录
│   ├── SKILL.md
│   └── scripts/
│       └── transcribe.sh
│
├── youtube-content-gen/               # YouTube 内容生成器
├── youtube-game-keywords/             # YouTube 游戏关键词提取
├── nextjs-seo-booster/                # Next.js SEO 工具包
├── nextjs-seo-foundations/            # Next.js SEO 工程化规范
├── seo-auditor/                       # SEO 审计框架
├── auto-page-sync/                    # 🆕 仓库内容自动同步到前端
│   ├── SKILL.md
│   └── resources/
│       ├── rebuild_index.py
│       ├── sync_workflow_template.yml
│       └── report_types_example.json
├── python-agent-engine/               # Python AI Agent 引擎
├── data-scraper-intent/               # 数据提取 & 意图分析
├── backlink-discovery/                # 外链机会发现引擎
├── backlink-intelligence/             # 外链情报收集与评估
├── keyword-competition-analysis/      # 关键词竞争度分析
├── seo-backlink-submitter/            # 批量目录提交工具
├── seo-link-strategy/                 # 外链策略生成器
├── roblox-site-architect/             # Roblox 站点架构
├── rpg-stat-catalyst/                 # RPG 数值计算核心
├── favicon-icon-generator/            # Favicon & Icon 生成器
├── gemini-thinking-protocol/          # 核心认知引擎
└── plugin-architect/                  # AI Skills 构建标准
```

---

## 🔐 安全说明

> ⚠️ **重要：本仓库不包含任何敏感信息**

- ✅ 所有代码均不包含 API Key、Token 或密码
- ✅ 涉及外部 API 的技能通过环境变量读取密钥
- ✅ 示例代码使用占位符（如 `your_api_key`）
- ✅ 已通过安全扫描，无敏感数据泄露

详细安全政策请参阅 [SECURITY.md](./SECURITY.md)。

### 环境变量配置示例

如果某个技能需要 API Key，请在项目中设置环境变量：

```bash
# .env 文件示例
TRELLO_API_KEY=your_trello_api_key_here
TRELLO_TOKEN=your_trello_token_here
GEMINI_API_KEY=your_gemini_api_key_here
OPENAI_API_KEY=your_openai_api_key_here
```

---

## 📊 技能统计

- **总技能数**: 25 个
- **P0 核心技能**: 3 个
- **代码行数**: 15,000+ 行
- **文档页数**: 70+ 页
- **时间节省**: 平均 80-95%

---

## 🎯 适用项目类型

- ✅ Roblox 游戏工具站
- ✅ SEO 内容站点
- ✅ 游戏攻略网站
- ✅ Next.js Web 应用
- ✅ Python AI 应用
- ✅ 数据采集项目
- ✅ 个人品牌 / 社交媒体运营
- ✅ YouTube 内容创作
- ✅ 自动化内容同步 / 定时更新站点

---

## 📝 更新日志


### 2026-04-12
- 🔥 添加 **seo-autopilot**（全自动 SEO 内容新鲜度引擎，关键词报告 → 页面生成 → 审计 → 部署）
- 📊 技能总数 → 25

### 2026-04-12
- 🆕 添加 **auto-page-sync**（仓库内容自动同步到前端页面，GitHub Actions 定时拉取 + SEO 新鲜度保障）
- 📊 技能总数从 24 → 25

### 2026-04-11
- 🔥 添加 **null-axiom-twitter**（Twitter/X 推文自动生成，含人设调性 + Reddit 回帖支持）
- 🔥 添加 **site-keyword-research**（整站关键词研究，三层方法论：30词初筛→10词详析→3词定方向）
- 📈 升级 **youtube-intel** v2.0（重构 Discovery 工作流，新增六步流程）
- 🔧 修复 **youtube-transcribe**（修复硬编码路径 + android GVS PO Token fallback）
- 📝 添加 CONTRIBUTING.md、SECURITY.md、LICENSE
- 📊 技能总数从 19 → 24

### 2026-04-07
- 添加 youtube-game-keywords（YouTube 订阅频道游戏关键词提取）

### 2026-04-04
- 🔥 添加 **google-trends-to-pages**（Google Trends → SEO 页面生成器）
- 🔥 添加 **multi-game-codes-hub**（5 分钟生成游戏代码页面）
- 🔥 添加 **roblox-game-data-scraper**（Trello/Discord/Reddit 数据抓取）
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

## 🤝 贡献指南

欢迎贡献新技能或改进现有技能！详细规范请参阅 [CONTRIBUTING.md](./CONTRIBUTING.md)。

### 技能提交规范

每个技能应包含：
- `SKILL.md` - 完整文档
- `resources/` - 代码和资源文件
- 使用示例和测试数据
- 清晰的使用说明

---

## 📄 License

MIT License - 开源分享，欢迎使用和贡献。详见 [LICENSE](./LICENSE)。

---

## 📧 联系方式

- GitHub: [@kennyzir](https://github.com/kennyzir)
- Repository: [7deer_skills](https://github.com/kennyzir/7deer_skills)

---

**⭐ 如果这个技能库对你有帮助，请给个 Star！**

