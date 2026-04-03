"""
外链机会发现 — Agent Task 任务
由 cron 或用户触发，用 OpenClaw agent 的 web_search 工具执行多轮搜索
"""

TARGET_URL = "https://robloxcalc.com"  # 由触发者传入
MAX_ROUNDS = 3

# ============================================================
# 任务说明：这个文件是一个 PROMPT 模板
# 实际由 OpenClaw agent 执行搜索
# ============================================================

DISCOVERY_PROMPT = """
# 外链机会发现任务

目标网站：{target_url}

## 任务

对目标网站进行外链机会发现，执行 {max_rounds} 轮搜索，每轮搜索后分析结果并派生新关键词。

## Step 1：提取种子关键词

从目标 URL 提取多维种子关键词：
- 品牌词、品类词、功能词、场景词
- 例如：robloxcalc.com → roblox, calculator, math, lua, game calculator

## Step 2：第1轮搜索

用 web_search 工具搜索以下查询（每个查5-10个结果）：

种子查询（基于种子关键词）：
1. "{{seed_kw}}" alternatives 2026（替换为你的种子词）
2. best free {{seed_kw}} tools
3. awesome {{seed_kw}} resources
4. {{seed_kw}} directory submit free
5. game calculator alternatives free

对每个搜索结果，提取：URL、域名、标题、摘要。

## Step 3：第2轮搜索

基于第1轮发现的平台，派生新关键词，继续搜索：
- 从第1轮结果中找平台类型（如 reddit.com/r/gamedev）
- 用平台类型关键词搜索更多同类平台
- 继续搜索 alternatives 相关的长尾词

## Step 4：第3-5轮（如需要）

重复 Step 3，持续发现新平台。

## Step 5：汇总

把所有发现的平台按以下方式分类：

🔴 P0 高相关（主题高度相关，有明显外链机会）：
- 平台名、URL、类型（论坛/目录/Alternatives文章/Wiki等）、最佳外链方式、相关度评分(0-1)

🟡 P1 中相关（有一定关联，可尝试）：
🟢 P2 低相关（关联度一般）

## 输出格式

```
# 外链机会发现报告 — {target_url}

## 种子关键词
- ...

## 搜索轮次
- 第1轮：X 个平台
- 第2轮：X 个平台  
- ...

## 🔴 P0 高相关平台
| 平台 | URL | 类型 | 最佳外链方式 | 相关度 |
|------|-----|------|------------|-------|

## 🟡 P1 中相关平台
...

## 🟢 P2 低相关平台
...

## 外链方式分布
- Forum/社区发帖：X 个
- GitHub PR：X 个
- Alternatives 文章：X 个
- 目录提交：X 个
- 其他：X 个
```

## 注意事项

- 每轮搜索至少查5个不同查询
- 优先发现 Reddit 社区、GitHub 资源列表、Alternatives 文章站、Wiki、教育资源站
- 不要只搜索目标品牌名，要搜索品类词（如 "game calculator" 而不只是 "roblox calculator"）
- 发现平台后记录完整 URL

开始执行。
"""

# ============================================================
# 关键词提取（用于生成任务 prompt）
# ============================================================

import re
from urllib.parse import urlparse


def extract_keywords(url: str) -> list:
    """从 URL 提取种子关键词"""
    parsed = urlparse(url)
    domain = parsed.netloc.replace("www.", "")
    path = parsed.path.strip("/")

    keywords = set()

    # 域名分词
    for part in re.split(r'[-_.]', domain):
        if len(part) > 1:
            keywords.add(part.lower())

    # 路径分词
    for part in re.split(r'[-_./]', path):
        if len(part) > 1:
            keywords.add(part.lower())

    # 品类猜测
    d = domain.lower()
    if "calc" in d:
        keywords.update(["calculator", "calculation", "math"])
    if "roblox" in d:
        keywords.update(["roblox", "game calculator", "lua"])
    if "game" in d:
        keywords.update(["game", "gaming"])
    if "tool" in d:
        keywords.update(["tool", "utility"])

    return list(keywords)


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python3 discovery_task.py <target_url> [rounds]")
        sys.exit(1)

    target = sys.argv[1]
    rounds = int(sys.argv[2]) if len(sys.argv) > 2 else 3
    seeds = extract_keywords(target)
    seed_kw = seeds[0] if seeds else target

    prompt = DISCOVERY_PROMPT.format(
        target_url=target,
        max_rounds=rounds,
        seed_kw=seed_kw
    )
    print(prompt)
