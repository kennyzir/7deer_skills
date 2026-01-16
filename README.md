# 🛠️ My Skills Library

> **私有技能库** - 可复用的 AI Agent 能力模块集合

这是一个个人技能库，包含了从多个项目中提炼出来的可复用代码模块和指令模板。
将此仓库克隆到任何新项目的 `.agent/skills` 目录，AI Agent 即可自动加载这些能力。

---

## 📦 技能清单

| # | 技能名称 | 描述 | 适用场景 |
|---|---------|------|---------|
| 1 | **nextjs-seo-booster** | Next.js SEO 工具包（结构化数据 + Sitemap） | 任何 Next.js 网站 |
| 2 | **python-agent-engine** | Python AI Agent 引擎（ReAct 模式 + 工具调用） | Python 后端 AI 应用 |
| 3 | **rpg-stat-catalyst** | RPG 数值计算核心（属性加点 + 阈值计算） | 游戏类应用 |
| 4 | **seo-auditor** | SEO 审计框架（检查清单 + 自动化脚本） | 任何网站 SEO 优化 |
| 5 | **data-scraper-intent** | 数据提取 & 搜索意图分析（爬虫模式 + LLM Prompt） | SEO/数据采集工作流 |

---

## 🚀 如何使用

### 方法 1: 克隆到新项目
```bash
# 在新项目根目录执行
git clone https://github.com/kennyzir/my-skills.git .agent/skills
```

### 方法 2: 作为 Git Submodule
```bash
git submodule add https://github.com/kennyzir/my-skills.git .agent/skills
```

### 方法 3: 手动复制
直接复制需要的技能文件夹到项目中。

---

## 📁 目录结构

```
my-skills/
├── README.md                   # 本文档
├── nextjs-seo-booster/         # Skill 1
│   ├── SKILL.md
│   └── resources/
├── python-agent-engine/        # Skill 2
│   ├── SKILL.md
│   └── resources/
├── rpg-stat-catalyst/          # Skill 3
│   ├── SKILL.md
│   └── resources/
├── seo-auditor/                # Skill 4
│   ├── SKILL.md
│   └── resources/
└── data-scraper-intent/        # Skill 5
    ├── SKILL.md
    └── resources/
```

---

## 🔐 安全说明

> ⚠️ **所有技能均不包含任何 API Key 或敏感数据。**
> 涉及外部 API 的技能（如 `python-agent-engine`）通过环境变量读取密钥。

---

## 📝 更新日志

### 2026-01-17
- 初始化技能库
- 添加 5 个核心技能模块

---

## 📄 License

Private - 仅供个人使用
