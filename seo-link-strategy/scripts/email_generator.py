"""
外链邮件个性化生成器
给定你的网站信息 + 目标平台，自动抓取对方页面内容，生成个性化邮件
"""

import asyncio
import os
import re
import sys
from urllib.parse import urlparse

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__))))

from playwright.async_api import async_playwright


# ============================================================
# 产品数据库（维护你的产品信息）
# ============================================================

PRODUCT_DB = {
    "example-game.com": {
        "name": "ExampleGame",
        "url": "https://example-game.com",
        "type": "game",
        "tagline": "A free, no-login-required browser game",
        "category": "Browser game",
        "category_keywords": ["browser game", "free game", "online game", "casual game"],
        "unique_selling_points": [
            ("100% free, no account required", "instant browser play — open and go"),
            ("H5 iframe format", "no download, no install, works on any device"),
            ("Multiple modes", "single player, multiplayer, competitive"),
            ("Active community", "community creating new content daily"),
        ],
        "competitors": ["competitor1", "competitor2", "competitor3"],
        "editor_angles": {
            "alternatives_article": (
                "Your readers are actively looking for free alternatives. "
                "ExampleGame is the most accessible option: no login, no download, "
                "works on any device with a browser."
            ),
            "game_directory": (
                "Free browser games are highly searched. "
                "ExampleGame's H5 format makes it perfect for your directory — "
                "readers can play instantly without leaving the page."
            ),
            "reddit_community": (
                "ExampleGame is a topic of organic interest in gaming communities. "
                "Sharing it provides real value to players looking for free alternatives."
            )
        }
    },
    "example-tool.com": {
        "name": "ExampleTool",
        "url": "https://example-tool.com",
        "type": "tool",
        "tagline": "AI-powered developer tool with pay-per-call pricing",
        "category": "Developer Tools",
        "category_keywords": ["AI tool", "developer tools", "automation", "API"],
        "unique_selling_points": [
            ("Production-ready features", "covers common automation tasks"),
            ("Pay-per-call pricing", "no subscription needed — pay only when you use it"),
            ("Framework agnostic", "works with any tech stack — no lock-in"),
            ("Free tier available", "developers can start building without upfront cost"),
        ],
        "competitors": ["competitor1", "competitor2", "competitor3"],
        "editor_angles": {
            "alternatives_article": (
                "Your readers need a way to extend their capabilities. "
                "ExampleTool provides production-ready features "
                "instead of building every tool from scratch."
            ),
            "product_directory": (
                "ExampleTool fills a gap in the developer tool stack — "
                "where developers find and pay for exactly the features they need."
            ),
            "reddit_community": (
                "ExampleTool solves common developer pain points — "
                "pay per call instead of subscription, works with any framework."
            )
        },
        "outreach_history": [
            # {"date": "2026-04-03", "platform": "ExampleDirectory", "email": "example@example.com",
            #  "result": "sent", "from": "your_email@example.com"},
        ]
    }
}


def get_product(product_url):
    """根据URL获取产品信息"""
    # 尝试直接匹配
    if product_url in PRODUCT_DB:
        return PRODUCT_DB[product_url]
    # 提取域名匹配
    parsed = urlparse(product_url)
    domain = parsed.netloc.replace("www.", "").lower()
    for key, val in PRODUCT_DB.items():
        key_domain = urlparse(key).netloc.replace("www.", "").lower()
        if domain == key_domain or domain in key_domain or key_domain in domain:
            return val
    return {}


# ============================================================
# 邮件模板库
# ============================================================

EMAIL_TEMPLATES = {
    "alternatives_article": {
        "subject": "Suggestion: Add {product_name} to your {competitor} Alternatives list",
        "body": """Hi {editor_name},

I noticed your article "{article_title}" on {platform_name} — really comprehensive list of {topic} alternatives.

I wanted to suggest adding **{product_name}** ({product_url}) to your list.

What makes it worth including for your readers:
{usp_list}

{editor_angle}

Here's a short description you can use:
{product_name} — {tagline}

Happy to provide screenshots or more details if you'd like to add it.

Thanks!
{sender_name}
{product_name} | {product_url}"""
    },

    "game_directory": {
        "subject": "Submission: {product_name} — free {category} for your directory",
        "body": """Hi {platform_name} team,

I'd like to submit **{product_name}** ({product_url}) for your game directory.

**Product:** {product_name}
**Category:** {category}
**URL:** {product_url}
**Description:** {tagline}

**Why it fits your directory:**
{editor_angle}

Contact: {sender_email}

Thanks!
{sender_name}"""
    },

    "resource_page": {
        "subject": "Useful resource for your readers: {product_name}",
        "body": """Hi {editor_name},

I came across your resources page on {platform_name} — great curation of {topic} tools.

I wanted to let you know about **{product_name}** ({product_url}) — {tagline}.

{editor_angle}

I think your readers who enjoy {topic} would find this useful. Happy to provide more details if needed.

Thanks!
{sender_name}
{product_url}"""
    },

    "general": {
        "subject": "Hi from {product_name} — a useful free {category} tool",
        "body": """Hi {editor_name},

I wanted to introduce **{product_name}** ({product_url}) — {tagline}.

{editor_angle}

Would love to know if this is something your readers might benefit from. Happy to share more info.

Thanks!
{sender_name}
{product_name} | {product_url}"""
    }
}


def select_template(platform_info, product_info):
    """根据平台类型选择合适的邮件模板"""
    ptype = platform_info.get("type", "").lower()
    if "alternatives" in ptype or "article" in ptype:
        return EMAIL_TEMPLATES["alternatives_article"]
    elif "directory" in ptype or "game" in ptype:
        return EMAIL_TEMPLATES["game_directory"]
    elif "resource" in ptype or "blog" in ptype:
        return EMAIL_TEMPLATES["resource_page"]
    return EMAIL_TEMPLATES["general"]


# ============================================================
# 页面内容抓取 + 竞品分析
# ============================================================

async def fetch_alternatives_article(page, platform, product_info):
    """
    抓取目标平台的 Alternatives 文章页面，分析已收录的竞品
    返回: {article_title, listed_competitors, gap_analysis, article_url}
    """
    result = {
        "platform": platform["name"],
        "article_url": None,
        "article_title": None,
        "listed_items": [],
        "listed_competitors": [],
        "gap_analysis": None,
        "status": "not_found"
    }

    # 构建可能的文章URL
    category = product_info.get("category_keywords", [""])[0]
    base = f"https://{platform['domain']}"

    # 常见 Alternatives 文章 URL 模式
    article_url_patterns = [
        base + f"/best-{category}-alternatives/",
        base + f"/{category}-alternatives/",
        base + f"/free-{category}-alternatives/",
        base + "/geoguessr-alternatives/",
        base + "/geoguessr-alternatives",
    ]

    async with async_playwright() as pw:
        browser = await pw.chromium.launch(headless=True)
        page = await browser.new_page()

        for url in article_url_patterns:
            try:
                print(f"  尝试: {url}")
                resp = await page.goto(url, timeout=15000, wait_until="domcontentloaded")
                if resp and resp.status in (200, 301, 302):
                    await asyncio.sleep(2)
                    content = await page.content()

                    # 提取标题
                    title_match = re.search(
                        r'<title[^>]*>([^<]+)</title>', content, re.IGNORECASE)
                    title = title_match.group(1).strip() if title_match else None

                    # 提取正文（简化版：找主要段落）
                    text_content = re.sub(r'<script[^>]*>.*?</script>', '',
                                          content, flags=re.DOTALL)
                    text_content = re.sub(r'<style[^>]*>.*?</style>', '',
                                          text_content, flags=re.DOTALL)
                    text_content = re.sub(r'<[^>]+>', ' ', text_content)
                    text_content = re.sub(r'\s+', ' ', text_content).strip()

                    # 提取竞品名称（常见的 GeoGuessr 替代品名称）
                    known_competitors = product_info.get("competitors", [])
                    found_competitors = []
                    for comp in known_competitors:
                        if comp.lower() in text_content.lower():
                            found_competitors.append(comp)

                    # 尝试提取列表项（更精准的竞品定位）
                    list_items = re.findall(
                        r'<li[^>]*>([^<]+)<', content, re.IGNORECASE)
                    list_items = [i.strip() for i in list_items if len(i.strip()) > 3]

                    result["article_url"] = url
                    result["article_title"] = title
                    result["listed_competitors"] = list(set(found_competitors))
                    result["listed_items"] = list_items[:20]  # 前20个列表项
                    result["status"] = "found"
                    result["gap_analysis"] = generate_gap_analysis(
                        product_info, found_competitors, list_items
                    )

                    print(f"  ✅ 找到文章: {title}")
                    print(f"     已收录竞品: {', '.join(found_competitors) or '无'}")
                    await browser.close()
                    return result

            except Exception as e:
                print(f"  失败: {str(e)[:40]}")
                continue

        await browser.close()

    return result


def generate_gap_analysis(product_info, listed_competitors, list_items):
    """
    基于已收录竞品，生成你的产品的差异化角度
    """
    product_name = product_info["name"]
    product_url = product_info["url"]

    # USP 分析
    usps = product_info.get("unique_selling_points", [])

    # 找出差异化 USP（竞品没强调的）
    unique_usps = []
    for usp_text, usp_detail in usps:
        mentioned = any(usp_text.lower() in comp.lower() or
                      comp.lower() in usp_text.lower()
                      for comp in listed_competitors)
        if not mentioned:
            unique_usps.append((usp_text, usp_detail))

    gap = {
        "product_name": product_name,
        "product_url": product_url,
        "already_listed_count": len(listed_competitors),
        "listed_competitors": listed_competitors,
        "differentiated_usps": unique_usps[:3],  # 最多3个差异化USP
        "recommendation": None
    }

    # 生成推荐角度
    if len(listed_competitors) == 0:
        gap["recommendation"] = (
            f"This article doesn't list any specific competitors yet. "
            f"{product_name} could be featured as the primary free alternative."
        )
    else:
        gap["recommendation"] = (
            f"The article covers {len(listed_competitors)} competitors. "
            f"{product_name} differentiates with: "
            + "; ".join([u[0] for u in unique_usps[:2]])
            if unique_usps else
            f"{product_name} is a strong free alternative to add."
        )

    return gap


def generate_personalized_email(platform_info, product_info, gap_analysis,
                                 sender_name, sender_email):
    """
    根据抓取结果，生成完全个性化的邮件
    """
    template = select_template(platform_info, product_info)
    editor_angle = platform_info.get("editor_angle",
        product_info.get("editor_angles", {}).get(
            platform_info.get("type", "").lower().split()[0],
            product_info.get("editor_angles", {}).get("alternatives_article", "")
        ))

    # 构建 USP 列表
    if gap_analysis and gap_analysis.get("differentiated_usps"):
        usp_list = "\n".join(
            f"- {u[0]} — {u[1]}"
            for u in gap_analysis["differentiated_usps"]
        )
    else:
        usp_list = "\n".join(
            f"- {u[0]} — {u[1]}"
            for u in product_info.get("unique_selling_points", [])[:3]
        )

    # 提取文章标题中的竞品词
    competitor_hint = "GeoGuessr"
    if gap_analysis and gap_analysis.get("listed_competitors"):
        competitor_hint = gap_analysis["listed_competitors"][0].title()

    # 填充模板
    subject = template["subject"].format(
        product_name=product_info["name"],
        competitor=competitor_hint,
        platform_name=platform_info["name"],
        category=product_info.get("category", "")
    )

    body = template["body"].format(
        editor_name=platform_info.get("editor_name", "there"),
        platform_name=platform_info["name"],
        article_title=gap_analysis["article_title"] if gap_analysis else f"{product_info['category']} alternatives",
        product_name=product_info["name"],
        product_url=product_info["url"],
        tagline=product_info.get("tagline", ""),
        category=product_info.get("category", ""),
        usp_list=usp_list,
        editor_angle=editor_angle or "",
        sender_name=sender_name,
        sender_email=sender_email,
        topic=product_info.get("category", "")
    )

    return {
        "to": platform_info.get("email", ""),
        "subject": subject,
        "body": body,
        "platform": platform_info["name"],
        "article_url": gap_analysis.get("article_url") if gap_analysis else None,
        "gap_analysis": gap_analysis
    }


# ============================================================
# 主执行函数
# ============================================================

async def generate_emails_for_product(product_url, product_type, platforms_with_emails,
                                      sender_name, sender_email):
    """
    给定产品和已发现联系人的平台列表，生成个性化邮件

    product_url: 你的网站 URL
    product_type: 'game' | 'tool' | 'saas' | 'content' | 'blog'
    platforms_with_emails: 联系人发现阶段的结果列表
    sender_name: 发件人名字
    sender_email: 发件人邮箱
    """
    product = get_product(product_url)
    if not product:
        print(f"[ERROR] 产品 {product_url} 不在 PRODUCT_DB 里")
        print("请先在 email_generator.py 的 PRODUCT_DB 中注册你的产品")
        return []

    print(f"[Email Generator] 为 {product['name']} 生成个性化邮件")
    print(f"目标平台数: {len(platforms_with_emails)}")
    print()

    # 过滤出有邮箱的平台
    actionable = [p for p in platforms_with_emails
                  if p.get("email") and p.get("status") in ("found", "found_unconfirmed")]

    results = []

    for platform in actionable:
        print(f"[{platform['name']}] 生成个性化邮件...")

        gap_analysis = None

        # 对 Alternatives 类型平台，抓取文章页面
        ptype = platform.get("type", "").lower()
        if "alternatives" in ptype or "article" in ptype:
            async with async_playwright() as pw:
                browser = await pw.chromium.launch(headless=True)
                page = await browser.new_page()
                ga = await fetch_alternatives_article(page, platform, product)
                gap_analysis = ga
                browser.close()
        else:
            # 非 Alternatives 平台，直接用通用角度
            gap_analysis = {
                "status": "skipped",
                "article_url": None,
                "recommendation": platform.get("editor_angle",
                    f"{product['name']} fits {platform['name']}'s {ptype} focus")
            }

        # 生成邮件
        email = generate_personalized_email(
            platform, product, gap_analysis, sender_name, sender_email
        )
        results.append(email)

        print(f"  ✅ Subject: {email['subject']}")
        if gap_analysis and gap_analysis.get("gap_analysis"):
            ga = gap_analysis["gap_analysis"]
            if ga.get("differentiated_usps"):
                print(f"     差异化USP: {', '.join([u[0] for u in ga['differentiated_usps']])}")
            if ga.get("recommendation"):
                print(f"     角度: {ga['recommendation'][:80]}...")
        print()

    return results


async def print_email_report(emails):
    """打印邮件报告"""
    print(f"\n{'='*65}")
    print(f"个性化邮件报告 — {len(emails)} 封邮件")
    print(f"{'='*65}\n")

    for i, email in enumerate(emails, 1):
        print(f"📧 邮件 {i}: {email['platform']}")
        print(f"   To: {email['to']}")
        print(f"   Subject: {email['subject']}")
        print(f"   Article: {email['article_url'] or 'N/A'}")
        print()
        print("   ── 正文预览 ──")
        lines = email["body"].split("\n")
        for line in lines[:12]:
            print(f"   {line}")
        if len(lines) > 12:
            print(f"   ... ({len(lines)-12} more lines)")
        print()
        print(f"   {'─'*40}")

    print(f"\n✅ {len(emails)} 封个性化邮件已生成")

    actionable = [e for e in emails if e["to"]]
    no_email = [e for e in emails if not e["to"]]
    if no_email:
        print(f"\n⚠️ {len(no_email)} 个平台无邮箱，跳过:")
        for e in no_email:
            print(f"   - {e['platform']}")


if __name__ == "__main__":
    # 测试：生成示例产品的邮件
    import argparse
    parser = argparse.ArgumentParser(description="生成外链个性化邮件")
    parser.add_argument("product_url", help="你的网站 URL")
    parser.add_argument("--sender-name", default="YourName", help="发件人名字")
    parser.add_argument("--sender-email", default="your_email@example.com", help="发件人邮箱")
    args = parser.parse_args()

    # 模拟已发现的联系人数据（从 contact_discoverer 传入）
    mock_platforms = [
        {
            "name": "Tech4Fresher",
            "domain": "tech4fresher.com",
            "type": "Alternatives 文章",
            "email": "admin@tech4fresher.com",
            "status": "found",
            "editor_name": "Tathagata Das",
            "editor_angle": "100% free browser game — open and play instantly, perfect for readers looking for free GeoGuessr alternatives"
        },
        {
            "name": "SolutionSuggest",
            "domain": "solutionsuggest.com",
            "type": "Alternatives 文章",
            "email": "editor@solutionsuggest.com",
            "status": "found",
            "editor_name": "Nick Cullen",
            "editor_angle": "Unique H5 iframe format — readers can play without leaving the page, addresses the gap between video-based and self-hosted alternatives"
        },
        {
            "name": "Beebom",
            "domain": "beebom.com",
            "type": "Alternatives 文章",
            "email": "contact@beebom.com",
            "status": "found",
            "editor_name": "Abubakar",
            "editor_angle": "Multiplayer + community maps — sets it apart from single-player alternatives"
        },
    ]

    # 先确定产品类型
    from urllib.parse import urlparse
    domain = urlparse(args.product_url).netloc.replace("www.", "")
    product_type = "game" if "game" in domain or "guess" in domain else "tool"

    results = asyncio.run(generate_emails_for_product(
        args.product_url,
        product_type,
        mock_platforms,
        args.sender_name,
        args.sender_email
    ))

    asyncio.run(print_email_report(results))
