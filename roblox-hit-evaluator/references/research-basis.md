# 研究依据与本版改动

## 方法来源与证据边界

本版的候选指标来自早期探索性案例研究，覆盖增长、玩法、参与/决策、传播和更新等方向。原始研究材料不是本 Skill 的运行依赖，也未随仓库发布；其中的案例存在重叠、筛选偏差和结果信息泄漏风险。因此：

- 不声称模型已由“100个独立样本”验证；
- 不把探索性案例占比当作样本外预测能力；
- 不采纳未经独立验证的概率函数、AUC或准确率；
- 不要求使用者能够访问任何私有报告、聊天或工作区文件。

本仓库公开的是可审计的规则、模板、合成样本和测试。任何人都可以检查计算逻辑，但这不等于已经证明模型能预测真实爆款。

## 设计目标与本版规则

- 设计目标：真实采集、量化指标、可由研究Agent执行、适合独立开发者、事实与推测分开，并避免与本次评估无关的系统扩张。
- 方法方向：增长、玩法、参与/决策、传播、更新；显式保留缺失数据；将爆款潜力和SEO应用分开。
- v0.1新增规则：30/25/15/20/10权重、15个子项、离散档位、18小时桶覆盖线、缺失界限、总分资格、30日双目标及复盘程序。这些都是工作假设，不是已验证的最佳权重。

## 没有照抄旧报告的内容

不把0搜索量/无50个实体当爆款禁入条件；不把首次发现晚自动扣爆款分；不把有宠物、RNG或“百万组合”当结果证据；不固定需要100页/几十页才能做站；不把不可靠的新站竞争评分混入游戏潜力；不把70%峰值回撤机械当失败；不把端点更新时间等同内容更新；不直接用旧模型把总分转概率。

源报告中的30成功/30对照属于有意选择的案例，不是随机总体。特征占比只能描述这些样本，且部分选样和编码含结果信息；本Skill不把它们称为经过独立验证的预测力。

## 当前官方文档（核验日期2026-09-07，运行时仍须复核）

- [S1] Codex Skills / Build skills：`https://developers.openai.com/codex/skills`（当前重定向到 `https://learn.chatgpt.com/docs/build-skills`）。确认SKILL.md + YAML、支持资源/脚本、本地`.agents/skills`。
- [S2] OpenClaw Skills：`https://docs.openclaw.ai/skills`；创建指南 `https://docs.openclaw.ai/tools/creating-skills`。确认workspace `skills/`、SKILL.md结构。Skill不提供额外工具/凭证权限。
- [S3] Roblox Games API reference：`https://create.roblox.com/docs/cloud/reference/domains/games`；Universes：`https://create.roblox.com/docs/cloud/reference/features/universes`。确认官方公开详情、favorites count、votes等接口类别；具体入口可能调整。
- [S4] Roblox Analytics dashboard：`https://create.roblox.com/docs/production/analytics/analytics-dashboard`。后台分析涉及所有者/授权权限，不能从公开快照伪造留存、DAU、收入。
- [S5] YouTube Search list：`https://developers.google.com/youtube/v3/docs/search/list`；Videos：`https://developers.google.com/youtube/v3/docs/videos`。查询时间参数、分页与当前视频资源统计；不能用当前值恢复首24小时数据。

2026-09-07已用公开Roblox游戏页完成一次只读快照采集，Place ID、Universe ID和公开统计字段均成功解析。YouTube采集仍依赖可选的`YOUTUBE_API_KEY`，未配置时应改用现有浏览器或搜索能力。单次端到端成功不证明第三方入口长期稳定，更不证明评分具备预测效度。
