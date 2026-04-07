# 🛠️ 7Deer Skills Library

> **开源技能库** - 可复用的 AI Agent 能力模块集合

这是一个开源技能库，包含了从实际项目中提炼出来的可复用代码模块和指令模板。
将此仓库克隆到任何新项目的 `.agent/skills` 目录，AI Agent 即可自动加载这些能力。

**🌟 特色**: 所有技能均包含完整文档、代码示例和使用指南，开箱即用。

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

### 数据采集 & 分析
| # | 技能名称 | 描述 | 适用场景 |
|---|---------|------|---------|
| 7 | **roblox-game-data-scraper** | Trello/Discord/Reddit 游戏数据抓取 | Roblox 游戏网站 |
| 8 | **data-scraper-intent** | 数据提取 & 搜索意图分析（爬虫 + LLM） | SEO/数据采集 |

### 外链建设
| # | 技能名称 | 描述 | 适用场景 |
|---|---------|------|---------|
| 9 | **backlink-discovery** | 外链机会发现引擎（web_search 多轮派生） | 外链建设 |
| 10 | **keyword-competition-analysis** | 谷歌关键词竞争度分析 | SEO 调研 |
| 11 | **seo-backlink-submitter** | 批量目录提交工具（Playwright 自动化） | 外链分发 |
| 12 | **seo-link-strategy** | 外链策略生成器（发现→评估→执行） | 外链营销 |

### 游戏 & 工具
| # | 技能名称 | 描述 | 适用场景 |
|---|---------|------|---------|
| 13 | **multi-game-codes-hub** | 快速生成游戏代码页面（模板 + 组件） | Roblox/游戏网站 |
| 14 | **rpg-stat-catalyst** | RPG 数值计算核心（属性加点 + 阈值） | 游戏类应用 |
| 15 | **roblox-site-architect** | Roblox 游戏工具站 SEO 架构 | Roblox 游戏网站 |

### AI & 开发工具
| # | 技能名称 | 描述 | 适用场景 |
|---|---------|------|---------|
| 16 | **python-agent-engine** | Python AI Agent 引擎（ReAct + 工具调用） | Python AI 应用 |
| 17 | **gemini-thinking-protocol** | 核心认知引擎（第一性原理 + 系统思维） | 复杂需求分析 |
| 18 | **plugin-architect** | AI Skills/Plugins 构建标准方法论 | 创建新技能 |

### 其他工具
| # | 技能名称 | 描述 | 适用场景 |
|---|---------|------|---------|
| 19 | **favicon-icon-generator** | Favicon & Icon 生成器（SVG + PWA） | Web 应用图标系统 |

---

## 🚀 快速开始

### 方法 1: 克隆到新项目（推荐）
```bash
# 在新项目根目录执行
git clone https://github.com/kennyzir/7deer_skills.git .agent/skills
```

### 方法 2: 作为 Git Submodule
```bash
git submodule add https://github.com/kennyzir/7deer_skills.git .agent/skills
```

### 方法 3: 手动复制
直接复制需要的技能文件夹到项目的 `.agent/skills/` 目录中。

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

---

## 📁 目录结构

```
7deer_skills/
├── README.md                          # 本文档
├── P0_SKILLS_COMPLETION.md            # P0 技能完成报告
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
├── nextjs-seo-booster/                # Next.js SEO 工具包
├── python-agent-engine/               # Python AI Agent 引擎
├── rpg-stat-catalyst/                 # RPG 数值计算核心
├── seo-auditor/                       # SEO 审计框架
├── backlink-discovery/                # 外链机会发现引擎
├── keyword-competition-analysis/      # 关键词竞争度分析
├── seo-backlink-submitter/            # 批量目录提交工具
├── seo-link-strategy/                 # 外链策略生成器
├── data-scraper-intent/               # 数据提取 & 意图分析
├── youtube-content-gen/               # YouTube 内容生成器
├── youtube-game-keywords/             # YouTube 游戏关键词提取
├── favicon-icon-generator/            # Favicon & Icon 生成器
├── gemini-thinking-protocol/          # 核心认知引擎
├── plugin-architect/                  # AI Skills 构建标准
├── roblox-site-architect/             # Roblox 站点架构
└── nextjs-seo-foundations/            # Next.js SEO 工程化规范
```

---

## 🔐 安全说明

> ⚠️ **重要：本仓库不包含任何敏感信息**

- ✅ 所有代码均不包含 API Key、Token 或密码
- ✅ 涉及外部 API 的技能通过环境变量读取密钥
- ✅ 示例代码使用占位符（如 `your_api_key`）
- ✅ 已通过安全扫描，无敏感数据泄露

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

- **总技能数**: 19 个
- **P0 核心技能**: 3 个
- **代码行数**: 10,000+ 行
- **文档页数**: 50+ 页
- **时间节省**: 平均 80-95%

---

## 🎯 适用项目类型

- ✅ Roblox 游戏工具站
- ✅ SEO 内容站点
- ✅ 游戏攻略网站
- ✅ Next.js Web 应用
- ✅ Python AI 应用
- ✅ 数据采集项目

---

## 📝 更新日志

### 2026-04-07
- 添加 youtube-game-keywords（YouTube 订阅频道游戏关键词提取）

### 2026-04-04 (最新)
- 🔥 添加 **google-trends-to-pages**（Google Trends → SEO 页面生成器）
- 🔥 添加 **multi-game-codes-hub**（5 分钟生成游戏代码页面）
- 🔥 添加 **roblox-game-data-scraper**（Trello/Discord/Reddit 数据抓取）
- 📝 更新 README，添加使用示例和安全说明
- 📊 添加 P0_SKILLS_COMPLETION.md 完成报告
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

欢迎贡献新技能或改进现有技能！

1. Fork 本仓库
2. 创建新分支 (`git checkout -b feature/new-skill`)
3. 提交更改 (`git commit -m 'Add new skill: xxx'`)
4. 推送到分支 (`git push origin feature/new-skill`)
5. 创建 Pull Request

### 技能提交规范

每个技能应包含：
- `SKILL.md` - 完整文档
- `resources/` - 代码和资源文件
- 使用示例和测试数据
- 清晰的使用说明

---

## 📄 License

MIT License - 开源分享，欢迎使用和贡献

---

## 📧 联系方式

- GitHub: [@kennyzir](https://github.com/kennyzir)
- Repository: [7deer_skills](https://github.com/kennyzir/7deer_skills)

---

**⭐ 如果这个技能库对你有帮助，请给个 Star！**
