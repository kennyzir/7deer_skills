# 7Deer Skills

**面向 AI Agent 的、可组合且可审计的 Roblox 游戏站增长工作流。**

从发现游戏机会，到关键词研究、证据整理、站点规划、SEO QA、上线后的持续更新与外链增长，每一步都有明确产物、证据边界和停止条件。这里不是“一键生成生产站点”的承诺；你需要选择合适的 Skills、提供项目上下文，并对部署、提交和付费 API 等外部动作明确授权。

[![CI](https://github.com/kennyzir/7deer_skills/actions/workflows/validate.yml/badge.svg)](https://github.com/kennyzir/7deer_skills/actions/workflows/validate.yml)
[![GitHub stars](https://img.shields.io/github/stars/kennyzir/7deer_skills?style=flat)](https://github.com/kennyzir/7deer_skills/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/kennyzir/7deer_skills?style=flat)](https://github.com/kennyzir/7deer_skills/forks)
[![License](https://img.shields.io/github/license/kennyzir/7deer_skills)](LICENSE)

[`roblox-hit-evaluator`](roblox-hit-evaluator/SKILL.md) 用公开证据和缺失数据边界判断一个候选游戏是否值得继续；[`roblox-site-architect`](roblox-site-architect/SKILL.md) 将后续工作编排成七阶段、七份可审计的 Markdown artifact。其他 Skills 按需加入，而不是被包装成一个不可检查的黑箱。

## 从游戏信号到可衡量的增长

| 阶段 | 用户要回答的问题 | 主要 Skills | 阶段产物 |
|---|---|---|---|
| 01 机会 | 这个 Roblox 游戏值得继续研究吗？ | **[`roblox-hit-evaluator`](roblox-hit-evaluator/SKILL.md)**、**[`roblox-site-architect`](roblox-site-architect/SKILL.md)** | `01-opportunity-report.md` |
| 02 关键词 | 用户在搜什么，哪些需求值得做？ | [`site-keyword-research`](site-keyword-research/SKILL.md)、[`keyword-competition-analysis`](keyword-competition-analysis/SKILL.md)、[`google-trends-to-pages`](google-trends-to-pages/SKILL.md) | `02-keyword-map.md` |
| 03 证据 | 页面里的代码、数值、机制和步骤由什么支持？ | [`roblox-game-data-scraper`](roblox-game-data-scraper/SKILL.md)、[`youtube-transcribe`](youtube-transcribe/SKILL.md) | `03-source-ledger.md` |
| 04 规划与建站 | 最小可发布范围、路由和验收条件是什么？ | **[`roblox-site-architect`](roblox-site-architect/SKILL.md)**、[`multi-game-codes-hub`](multi-game-codes-hub/SKILL.md) | `04-site-plan.md` |
| 05 SEO QA 与上线 | 当前版本是否 ready，是否真的已经发布？ | [`nextjs-seo-foundations`](nextjs-seo-foundations/SKILL.md)、[`nextjs-seo-booster`](nextjs-seo-booster/SKILL.md)、[`seo-auditor`](seo-auditor/SKILL.md) | `05-seo-audit.md` |
| 06 持续更新 | 哪些事实会过期，如何复查，部署状态是什么？ | [`seo-autopilot`](seo-autopilot/SKILL.md)、[`auto-page-sync`](auto-page-sync/SKILL.md) | `06-deployment-report.md` |
| 07 外链增长 | 哪些增长动作可衡量、可授权、可复盘？ | [`backlink-discovery`](backlink-discovery/SKILL.md)、[`seo-link-strategy`](seo-link-strategy/SKILL.md)、[`seo-backlink-submitter`](seo-backlink-submitter/SKILL.md) | `07-growth-backlog.md` |

七份 artifact 统一保存在 `<project-root>/pipeline/`。它们使用共同的 YAML header 记录 `status`、`generated_at`、`observed_through`、`upstream`、`sources` 和 `gaps`，正文统一包含决策、证据、未知项与 handoff。具体契约见 [`pipeline-contracts.md`](roblox-site-architect/references/pipeline-contracts.md)。

## 开始使用

Codex 的项目级 Skills 路径是 `.agents/skills`。下面先安装仓库，再以 dry-run 查看七份 artifact 的明确目标；只有加上 `--apply` 才会创建文件。

```bash
mkdir -p .agents
git clone https://github.com/kennyzir/7deer_skills.git .agents/skills

python3 .agents/skills/roblox-site-architect/scripts/init_pipeline.py \
  --project-root "$PWD" \
  --game "<canonical Roblox game name>" \
  --scope "<bounded research or delivery scope>"
```

每个 Skill 都以 `SKILL.md` 描述触发条件、流程和边界。其他 Agent 是否自动发现 Skills、使用什么目录，取决于该工具当前实现；请以对应工具的官方文档为准，不要假设它们与 Codex 使用相同路径。完整选择入口见 [CATALOG.md](CATALOG.md)。

## 七个可审计产物

1. `01-opportunity-report.md`：游戏身份、需求/供给证据、反证、决策与置信边界。
2. `02-keyword-map.md`：关键词 cluster、意图、证据、目标路由与优先级。
3. `03-source-ledger.md`：来源观察、真实观察时间、支持的 claim 与冲突。
4. `04-site-plan.md`：发布范围、内容/数据契约、内链角色与本地验收结果。
5. `05-seo-audit.md`：逐项 SEO/build 检查、严重性、修复与 release decision。
6. `06-deployment-report.md`：真实部署状态、可达性检查与 freshness review loop。
7. `07-growth-backlog.md`：目标、依据、风险、授权状态、指标和实际结果。

初始化器使用 [`assets/pipeline-templates`](roblox-site-architect/assets/pipeline-templates/) 中维护的七个模板。初始状态只表示“工作尚未完成”：01 为 `partial`，02–07 因缺少 upstream 为 `blocked`；`observed_through` 是 `unknown`，生成时间不会被当作证据验证时间。已有 pipeline 应按数字顺序恢复，不能通过再次初始化覆盖。

## Proof, not promises / 用验证说话

当前五个明确标记的 Skills 在 CI 中共运行 85 个行为测试：

- `roblox-hit-evaluator`：47
- `roblox-site-architect`：17
- `multi-game-codes-hub`：8
- `seo-backlink-submitter`：7
- `signallayer-backlinks-client`：6

CI 还单独运行目录一致性测试。仓库验证器检查所有顶层 `SKILL.md` 的 frontmatter、命名、相对引用和 Python 语法；目录生成器检查 [CATALOG.md](CATALOG.md) 是否完整且无漂移。这些结果证明的是当前被检查的行为和结构，不代表所有 Skills 具有相同成熟度，也不构成流量、排名或收入承诺。每个 Skill 的 CI 状态与执行边界以生成目录为准。

本地可运行与 CI 相同的结构检查：

```bash
python3 scripts/generate_catalog.py --check
python3 scripts/validate_repo.py
```

## 开源仓库与 RB Auto

7Deer Skills 是 MIT License 的开源仓库：Skills 可单独查看、组合、修改和审计，编排与运行由你负责。

[RB Auto](https://rbauto.ludusdex.com/?utm_source=github&utm_medium=readme&utm_campaign=7deer_skills) 是面向 Roblox 游戏站的集成化产品，提供更集中的工作流与持续维护，适合希望缩短自行整合路径的人。它与本仓库的定位不同，也不承诺搜索排名、流量或收入。

| 7Deer Skills | RB Auto |
|---|---|
| 开源、可组合、可审计 | 集成化产品与持续维护 |
| 自行选择工具与编排流程 | 更集中地衔接落地步骤 |
| 适合开发、研究与自定义 | 适合希望减少整合工作的人 |

## 安全、贡献与许可

读取公开资料、生成草稿和修改本地文件，不自动授权外部副作用。发送消息、提交表单或外链、部署、push、购买服务/域名、创建定时任务，以及调用付费或会改变远端状态的 API，都需要用户对具体目标与动作明确授权。

- [CONTRIBUTING.md](CONTRIBUTING.md)：贡献范围与检查清单
- [SECURITY.md](SECURITY.md)：漏洞报告与敏感信息边界
- [LICENSE](LICENSE)：MIT License

<details>
<summary><strong>联系七鹿 / 7Deer</strong></summary>

- GitHub：[@kennyzir](https://github.com/kennyzir)
- 关于七鹿：[认识七鹿](https://rbauto.ludusdex.com/about/?utm_source=github&utm_medium=readme&utm_campaign=7deer_skills)
- 产品与案例：[RB Auto](https://rbauto.ludusdex.com/?utm_source=github&utm_medium=readme&utm_campaign=7deer_skills) · [实践记录](https://rbauto.ludusdex.com/cases/?utm_source=github&utm_medium=readme&utm_campaign=7deer_skills)
- 内容动态：[即刻「七鹿 AI」](https://m.okjike.com/users/ea42b30c-24db-434b-b969-650d7473f69e)

微信交流请备注「GitHub Skills」。

<img src="assets/wechat-7deer.png" alt="七鹿微信二维码" width="320" />

</details>
