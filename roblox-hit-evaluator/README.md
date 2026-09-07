# Roblox Hit Evaluator｜Roblox 游戏爆款评估 Skill

给一个 Roblox 游戏链接，让 Codex、OpenClaw 或支持 Agent Skills 的研究Agent去查数据、判断潜力、留下可复查的预测。不是只生成一篇“看起来很有潜力”的分析。

## 最快开始

把完整目录保留下来，交给Agent安装，之后给游戏链接即可。建议第一次只评估一个游戏，先验证采集与报告路径，不批量改造雷达。

**Codex：**目录放到当前项目 `.agents/skills/roblox-hit-evaluator/`。

**OpenClaw：**目录放到对应Agent工作区 `skills/roblox-hit-evaluator/`。

目录内必须有`SKILL.md`，保留`references/`、`scripts/`和`templates/`。依据是官方Skills文档，链接在`references/research-basis.md`。安装后使用新会话；若未发现Skill，检查当前Agent工作区/权限/技能列表。不同部署的实际根目录由Agent核实，不擅自修改全局配置。

### 交给Codex安装

```text
读取我提供的 roblox-hit-evaluator 完整目录。
将它安装为当前项目可用的本地Skill，保持SKILL.md、references、scripts和templates结构。
先核验当前工具实际使用的Skill目录，只新增这个Skill的文件，不修改业务代码、依赖、全局配置和现有Skill。
安装完成后确认能够读取主指令和引用文件，并运行附带测试。
不要重构机会雷达，不要建立调度系统，不要部署。
```

### 单游戏研究

```text
使用 $roblox-hit-evaluator 评估这个 Roblox 游戏：
[粘贴官方游戏链接]

先真实采集，再计算评分和输出报告，不要只给研究计划。
缺少API Key时使用现有搜索/浏览器，不要把任务丢回给我。
给出潜力分、证据覆盖、缺失界限、主要支持与反证，并保存本次预测。
没有历史就给早期候选判断，不伪造7日曲线。
本次不做SEO建站建议，不设置定时任务，不修改业务代码。
```

### 复查同一游戏

```text
使用 roblox-hit-evaluator 的 recheck/review 流程。
先读取这个游戏上一次保存的 assessment.json 和 scored.json，再采集最新资料。
将新评估写入新目录，不覆盖原始预测。
对已到期目标输出实际命中/未命中；未到期写PENDING，缺数据写INCOMPLETE。
说明本轮新证据让原判断增强还是减弱，不用事后资料改写旧分数。
```

### 多候选比较

```text
使用 roblox-hit-evaluator 比较以下游戏：[链接列表]。
先逐个消歧，采用同一模型、数据截止和查询范围。
分别展示完整分/局部分/证据覆盖，不把缺资料的新游戏直接判低潜力。
给出值得继续研究的排序及一个最重要的下一动作。
本轮未做完的候选明确列出，不用只读介绍页的结果冒充深度研究。
```

## 包里有什么

- `SKILL.md`：触发、范围、实际执行步骤和验收。
- `references/collection.md`：来源矩阵、查询策略、无Key路径、停止条件。
- `references/metrics-and-scoring.md`：五组15项、数值档位、观察档位、缺失处理。
- `references/model.json`：当前模型的机器可读导出；执行权威在`evaluate.py`。
- `references/outcomes.md`：30日目标、冻结预测、7/14/30天复盘口径。
- `references/research-basis.md`：历史资料采用/纠正与官方文档。
- `scripts/collect_public.py`：一次性Roblox快照；可选YouTube样本采集。
- `scripts/evaluate.py`：历史派生指标、输入检查、评分、预测冻结与结果复查。
- `templates/`：待填评估JSON和中文报告模板。
- `examples/`：**明确标注的合成示例，不是真实游戏数据**。
- `tests/`：本地单元测试。

## 能力与边界

需要Agent已有的浏览器/搜索/网络权限才能实际调查。Skill不会凭空添加这些能力。

Python工具要求Python 3.10或以上，不需要pip安装。YouTube API Key是可选项；未配置时使用已有浏览器/搜索。不要把Skill配置或聊天当密钥仓库。

```bash
python -m unittest discover -s tests -v
python scripts/evaluate.py score examples/synthetic-assessment.json --out /一个尚不存在的文件路径/scored-demo.json
```

Windows、macOS、Linux均使用标准库路径处理；实际Python启动命令由Agent根据环境选择。上面的示例路径需要替换。输出文件默认拒绝覆盖。

采集脚本只负责部分结构化数据，不自动完成视频观看、社区研究和语义证据核验；这些由加载Skill的Agent按手册继续完成。不能只跑一次快照脚本就宣称“深度研究完成”。

评分是研究优先级，不是爆款概率。30/25/15/20/10权重是本次v0.1设计，未经样本外训练和概率校准。没有进行盈利、收益或排名承诺。

Skill不自动开始定时任务。需要长期监测时，由用户另行授权现有调度系统调用，不新增常驻服务或框架。

## 本次验证

本地47项单元测试通过，包括未知不填0、未来时间拒绝、游戏身份混合拒绝、时段采样偏差、单峰不算持续爆发、预测hash检查、密钥脱敏等。2026-09-07还用公开Roblox游戏页完成了一次只读快照采集，Place ID、Universe ID和公开统计字段均成功解析。

尚未完成YouTube API端到端采集，也没有覆盖所有Codex/OpenClaw部署方式。官方接口和Skill格式已按2026-09-07公开文档核验；当前可靠结论是计算、校验逻辑和一次Roblox公开快照采集通过，不是“已验证能预测爆款”。

脚本能检查结构、数字、引用ID与时间，不会自动证明来源文字属实或Agent的观察没有偏差。第一轮应人工抽看证据和关键视频后再用于持续监测。

## License

本目录随仓库按 [MIT License](../LICENSE) 发布。Roblox和YouTube名称及商标归各自权利人所有；本项目与其无隶属或背书关系。
