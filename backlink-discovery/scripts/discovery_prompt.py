"""
外链发现 Agent Prompt
生成发现任务的完整 prompt，用于 sessions_spawn 触发 isolated agent
"""

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

    # 品类猜测（扩大覆盖）
    d = domain.lower()
    # 计算器类
    if any(k in d for k in ["calc", "calculator"]):
        keywords.update(["calculator", "calculation", "math", "mathematics",
                        "game calculator", "online calculator", "math tool"])
    # Roblox 类
    if any(k in d for k in ["roblox"]):
        keywords.update(["roblox", "roblox studio", "roblox developer", "lua",
                        "roblox scripting", "roblox game", "roblox creator"])
    # 游戏类
    if any(k in d for k in ["game", "play", "gaming"]):
        keywords.update(["game", "gaming", "web game", "browser game",
                        "online game", "free game", "HTML5 game"])
    # 工具类
    if any(k in d for k in ["tool", "util"]):
        keywords.update(["tool", "utility", "online tool", "free tool"])
    # SEO 类
    if any(k in d for k in ["seo"]):
        keywords.update(["SEO", "search engine optimization", "webmaster tools"])
    # 营销类
    if any(k in d for k in ["marketing", "market"]):
        keywords.update(["marketing", "digital marketing", "growth"])
    # 写作/内容类
    if any(k in d for k in ["writing", "writer", "content"]):
        keywords.update(["writing tool", "content creation", "AI writing"])
    # 代理/Agent类
    if any(k in d for k in ["agent", "agentic"]):
        keywords.update(["AI agent", "agentic AI", "agent framework", "LLM agent"])
    # 通用品类扩展（对所有域名都加）
    if len(keywords) < 3:
        keywords.update(["online tool", "free tool", "web app"])

    # 去噪
    stopwords = {"the", "and", "for", "you", "your", "com", "org", "io", "net"}
    keywords = {k for k in keywords if k not in stopwords and len(k) > 1}

    return list(keywords)


def build_discovery_prompt(target_url: str, target_count: int = 300) -> str:
    """生成完整的发现任务 prompt"""

    seeds = extract_keywords(target_url)
    seed_display = ", ".join(seeds[:8])

    prompt = f"""
# 外链机会发现任务

## 目标网站
{target_url}

## 种子关键词
{seed_display}

## 任务目标
发现与该网站最相关的外链机会平台，目标 {target_count} 个平台后自动停止。

---

## Step 1：多轮搜索

使用 web_search 工具，执行多轮搜索。每轮搜索 5-10 个不同查询。

### 种子搜索（Round 1）
用以下查询进行搜索（每个查 5-10 个结果）：

1. "{seeds[0] if seeds else target_url} alternatives 2026"
2. "best free {seeds[0] if seeds else 'tool'} alternatives"
3. "awesome {seeds[0] if seeds else target_url} list"
4. "{seeds[0] if seeds else target_url} directory submit free"
5. "{seeds[0] if seeds else target_url} for developers"

对每个搜索结果，记录：
- URL
- 域名
- 标题

### Round 2+：派生新关键词继续搜索

从 Round 1 结果中提取新关键词：
- 从平台标题提取相关词（如发现 reddit.com/r/gamedev → 派生出 "gamedev community"）
- 继续搜索更多同类平台

继续搜索：
6. "{seeds[0] if seeds else target_url} game development tool alternatives"
7. "best {seeds[0] if seeds else target_url} tools 2026"
8. "free {seeds[0] if seeds else target_url} for gamers"
9. "{seeds[0] if seeds else target_url} vs similar tools"
10. "online {seeds[0] if seeds else target_url} free"

重复以上过程，每轮记录新发现的平台，直到达到 {target_count} 个平台。

---

## Step 2：平台分类

对每个发现的平台，判断：

### 平台类型
| 平台关键词 | 类型 |
|-----------|------|
| reddit, forum, community | 论坛/社区 |
| github awesome | GitHub 资源列表 |
| wikipedia, fandom, wiki | Wiki/百科 |
| alternatives, "best X alternatives" | Alternatives 文章站 |
| directory, "submit your" | 目录站 |
| dev.to, hashnode, medium, blog | 开发者博客 |
| producthunt, alternativeto | 产品发现平台 |
| education, teacher, school | 教育资源站 |
| news, article, press | 新闻/媒体 |

### 最佳外链方式
| 平台类型 | 最佳外链方式 |
|---------|------------|
| 论坛/社区 | forum_post（发帖/评论）|
| GitHub 资源列表 | github_pr（提 PR）|
| Wiki | wiki_edit（编辑词条）|
| Alternatives 文章站 | alternatives_article（联系编辑添加）|
| 目录站 | directory_submit（提交产品页）|
| 开发者博客 | guest_post（写文章带链接）|
| 有联系邮箱 | email_outreach（发邮件）|
| 教育站 | education_resource（提交教育资源）|
| 其他 | manual_review（需人工评估）|

### 相关度评分（0-1）
考虑：主题相关度 + 受众重叠度 + 链接价值潜力

---

## Step 3：写入数据库

将每轮发现结果追加写入文件：

文件路径：`memory/{提取的域名}/platforms.json`

格式（JSON，追加模式）：
```json
{{
  "domain": "平台域名",
  "url": "完整URL",
  "title": "平台标题",
  "method": "最佳外链方式",
  "platform_type": "平台类型",
  "relevance": 0.85,
  "discovered_round": 1,
  "discovered_at": "ISO时间戳"
}}
```

如果文件不存在，先创建空数组 `{{"platforms": []}}`。

**每轮结束后立即写入，不要等到全部完成。**

---

## Step 4：达到目标后生成汇总

当平台数量达到 {target_count} 个，或连续 2 轮无新发现时：

### 生成 summary.md

写入路径：`memory/{提取的域名}/summary.md`

内容：
```
# {target_url} 外链机会发现报告

## 发现状态
- 状态：已完成
- 平台总数：X / {target_count}
- 发现时间：ISO时间戳

## 🔴 P0 高相关平台（X 个）
| 平台 | URL | 类型 | 最佳外链方式 | 相关度 |
|------|-----|------|------------|-------|

## 🟡 P1 中相关平台（X 个）
...

## 🟢 P2 低相关平台（X 个）
...

## 📊 外链方式分布
- Forum 发帖：X 个
- GitHub PR：X 个
- Alternatives Outreach：X 个
- 目录提交：X 个
- Wiki 编辑：X 个
- Guest Post：X 个
- 其他：X 个
```

---

## 注意事项

- **不要只搜索品牌词**，要搜索品类词和长尾词
- **优先发现**：Reddit 社区、GitHub Awesome Lists、Alternatives 文章站、Wiki、教育站
- **每轮写盘**（避免中断丢失进度）
- **达到 {target_count} 个平台后停止**
- **去重**：同一域名只记录一次
"""

    return prompt


def get_domain_key(url: str) -> str:
    """获取域名 key（用于目录名）"""
    parsed = urlparse(url)
    domain = parsed.netloc.replace("www.", "").replace(".", "_")
    return domain


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        url = sys.argv[1]
        count = int(sys.argv[2]) if len(sys.argv) > 2 else 300
        print(build_discovery_prompt(url, count))
    else:
        print("Usage: python3 discovery_prompt.py <url> [target_count]")
