# 验证记录

生成/核验日期：2026-09-07。

## 已执行

- Python语法检查：`scripts/evaluate.py`、`scripts/collect_public.py`。
- `python -m unittest discover -s tests -v`：47 tests，全部通过。
- 合成样本确定性评分：72.7；权重合计100；模型导出与脚本一致。
- 测试只使用明确标注的合成数据/网络错误模拟，不混入真实预测结果。
- 公开Roblox只读采集：使用官方游戏页成功解析Place ID、Universe ID及公开统计字段；测试输出保存在系统临时目录，未提交仓库。

## 未完成

- YouTube API端到端采集：未提供可选的`YOUTUBE_API_KEY`，未消耗外部配额。
- Codex/OpenClaw具体部署中的Skill发现、工具授权及工作区适配。
- 实际游戏的人工证据质量复核、前瞻30日预测、样本外验证、概率校准。

这些限制不靠“测试PASS”消除。分数是探索性研究工具，不是可靠成功概率。
