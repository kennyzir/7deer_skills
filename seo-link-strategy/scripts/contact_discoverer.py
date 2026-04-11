"""
外链平台联系人自动发现脚本
给定目标网站 URL，自动发现相关外链平台的编辑/联系人的邮箱
"""

import asyncio
import os
import re
import sys
from urllib.parse import urlparse

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__))))

from playwright.async_api import async_playwright

# ============================================================
# 外链平台分级体系
# ============================================================

PLATFORM_TIERS = {
    "P0": [
        # === Alternatives 文章站（最高价值）===
        {
            "name": "TechCult",
            "domain": "techcult.com",
            "type": "Alternatives 文章",
            "submit_url": "https://techcult.com/contact",
            "contact_patterns": ["/contact", "/about", "/team", "/writer"],
            "email_hints": ["info@", "contact@", "editor@", "hello@"],
            "author_page_pattern": "/author/",
            "twitter_hint": "techcultco",
            "notes": "有大量 GeoGuessr/游戏 Alternatives 文章"
        },
        {
            "name": "Beebom",
            "domain": "beebom.com",
            "type": "Alternatives 文章",
            "submit_url": "https://beebom.com/contact/",
            "contact_patterns": ["/contact", "/about", "/team"],
            "email_hints": ["contact@", "hello@", "tips@"],
            "author_page_pattern": "/author/",
            "notes": "主编 Abubakar Mohammed，文章质量高"
        },
        {
            "name": "PrivacySavvy",
            "domain": "privacysavvy.com",
            "type": "Alternatives 文章",
            "submit_url": "https://privacysavvy.com/contact-us/",
            "contact_patterns": ["/contact", "/about", "/team"],
            "email_hints": ["contact@", "hello@", "admin@"],
            "notes": "Ademilade Shodipe Dosunmu，无公开邮箱，需 Twitter/LinkedIn"
        },
        {
            "name": "Tech4Fresher",
            "domain": "tech4fresher.com",
            "type": "Alternatives 文章",
            "submit_url": "https://tech4fresher.com/contact-us/",
            "contact_patterns": ["/contact", "/about", "/team"],
            "email_hints": ["admin@", "contact@", "hello@"],
            "notes": "Tathagata Das，admin@tech4fresher.com 已验证"
        },
        {
            "name": "SolutionSuggest",
            "domain": "solutionsuggest.com",
            "type": "Alternatives 文章",
            "submit_url": "https://solutionsuggest.com/contact/",
            "contact_patterns": ["/contact", "/about", "/team"],
            "email_hints": ["editor@", "contact@", "hello@"],
            "notes": "Nick Cullen，editor@solutionsuggest.com 已验证"
        },
        {
            "name": "GeckoAndFly",
            "domain": "geckoandfly.com",
            "type": "Alternatives 文章",
            "submit_url": "https://geckoandfly.com/contact/",
            "contact_patterns": ["/contact", "/about", "/team"],
            "email_hints": ["contact@", "hello@", "admin@"],
            "notes": "已有产品收录"
        },
        {
            "name": "GameRant",
            "domain": "gamerant.com",
            "type": "Alternatives 文章",
            "submit_url": "https://gamerant.com/contact/",
            "contact_patterns": ["/contact", "/about"],
            "email_hints": ["contact@", "tips@", "hello@"],
            "notes": "DA 高，编辑量大，提交需通过官方渠道"
        },
        {
            "name": "AlternativeTo",
            "domain": "alternativeto.net",
            "type": "目录站 + Alternatives",
            "submit_url": "https://alternativeto.net/page/about/",
            "contact_patterns": ["/about", "/contact"],
            "email_hints": ["info@", "contact@"],
            "notes": "可免费创建产品页面，编辑性链接价值高"
        },
    ],

    "P1": [
        # === 游戏目录站 ===
        {
            "name": "FreeArcade",
            "domain": "free-arcade.com",
            "type": "游戏目录",
            "submit_url": "https://free-arcade.com/submit-game",
            "contact_patterns": ["/contact", "/about"],
            "email_hints": ["contact@", "submit@", "hello@"],
            "notes": "免费发布，自助提交"
        },
        {
            "name": "SilverGames",
            "domain": "silvergames.com",
            "type": "游戏目录",
            "submit_url": "https://silvergames.com/submit-game",
            "contact_patterns": ["/contact", "/about"],
            "email_hints": ["contact@", "submit@", "hello@"],
            "notes": "免费发布，自助提交"
        },
        {
            "name": "itch.io",
            "domain": "itch.io",
            "type": "开发者/游戏社区",
            "submit_url": "https://itch.io/developers/announce",
            "contact_patterns": ["/about"],
            "email_hints": ["info@", "contact@"],
            "notes": "免费发布，在开发者社区发帖宣布即可"
        },
        {
            "name": "CrazyGames",
            "domain": "crazygames.com",
            "type": "游戏目录",
            "submit_url": "https://www.crazygames.com/developers",
            "contact_patterns": ["/developers", "/about"],
            "email_hints": ["developer@", "contact@"],
            "notes": "需要申请，但有 API 接入"
        },
        {
            "name": "HTML5GameDevs",
            "domain": "html5gamedevs.com",
            "type": "开发者论坛",
            "submit_url": "https://html5gameDevs.com/",
            "contact_patterns": ["/contact"],
            "email_hints": ["contact@", "hello@"],
            "notes": "论坛形式，可发帖介绍"
        },
    ],

    "P2": [
        # === Reddit 社区 ===
        {
            "name": "Reddit r/geoguessr",
            "domain": "reddit.com/r/geoguessr",
            "type": "社区",
            "submit_url": "https://www.reddit.com/r/geoguessr/submit",
            "contact_patterns": [],
            "email_hints": [],
            "notes": "发帖介绍产品，贡献价值，不要直接发链接"
        },
        {
            "name": "Reddit r/gaming",
            "domain": "reddit.com/r/gaming",
            "type": "社区",
            "submit_url": "https://www.reddit.com/r/gaming/submit",
            "contact_patterns": [],
            "email_hints": [],
            "notes": "大型社区，发帖需要遵守规则"
        },
        {
            "name": "Reddit r/SideProject",
            "domain": "reddit.com/r/SideProject",
            "type": "社区",
            "submit_url": "https://www.reddit.com/r/SideProject/submit",
            "contact_patterns": [],
            "email_hints": [],
            "notes": "适合 indie 项目展示"
        },
        # === GitHub Awesome ===
        {
            "name": "awesome-geography",
            "domain": "github.com/heilcheng/awesome-agent-skills",
            "type": "GitHub Awesome",
            "submit_url": "https://github.com/heilcheng/awesome-agent-skills/pulls",
            "contact_patterns": [],
            "email_hints": [],
            "notes": "PR 提交地理学习资源列表"
        },
        {
            "name": "awesome-games",
            "domain": "github.com/Gruutak/awesome-games",
            "type": "GitHub Awesome",
            "submit_url": "https://github.com/Gruutak/awesome-games/pulls",
            "contact_patterns": [],
            "email_hints": [],
            "notes": "游戏合集 PR"
        },
        # === 教育类 ===
        {
            "name": "Sheppard Software",
            "domain": "sheppardsoftware.com",
            "type": "教育游戏站",
            "submit_url": "https://sheppardsoftware.com/contact-us/",
            "contact_patterns": ["/contact", "/about"],
            "email_hints": ["contact@", "info@"],
            "notes": "地理教育游戏，适合此类外链"
        },
        {
            "name": "LizardPoint",
            "domain": "lizardpoint.com",
            "type": "教育游戏站",
            "submit_url": "https://lizardpoint.com/contact.php",
            "contact_patterns": ["/contact", "/about"],
            "email_hints": ["contact@", "info@"],
            "notes": "地理测验，可联系添加链接"
        },
    ]
}


def get_all_platforms():
    """返回所有平台（扁平列表）"""
    all_platforms = []
    for tier, platforms in PLATFORM_TIERS.items():
        for p in platforms:
            p["tier"] = tier
            all_platforms.append(p)
    return all_platforms


def find_platforms_for_site_type(site_type):
    """
    根据网站类型推荐匹配的 P0 平台
    site_type: 'game' | 'tool' | 'saas' | 'content' | 'blog'
    """
    type_mapping = {
        "game": ["TechCult", "Beebom", "PrivacySavvy", "Tech4Fresher",
                 "SolutionSuggest", "FreeArcade", "SilverGames", "itch.io",
                 "Reddit r/geoguessr", "Reddit r/gaming", "awesome-geography"],
        "tool": ["TechCult", "Beebom", "PrivacySavvy", "AlternativeTo",
                 "Tech4Fresher", "ProductHunt", "FreeArcade"],
        "saas": ["ProductHunt", "AlternativeTo", "G2", "Capterra",
                 "TechCult", "Beebom"],
        "content": ["TechCult", "Beebom", "GeckoAndFly", "GameRant"],
        "blog": ["TechCult", "Beebom", "GeckoAndFly"],
    }
    return type_mapping.get(site_type, [])


def extract_domain(url):
    """从 URL 提取域名"""
    parsed = urlparse(url)
    domain = parsed.netloc.lower()
    if domain.startswith("www."):
        domain = domain[4:]
    return domain


# ============================================================
# 联系人发现核心逻辑
# ============================================================

async def find_contacts_on_platform(page, platform):
    """
    对单个目标平台执行联系人发现
    返回：{email, author_name, author_page, twitter, linkedin, status, source}
    """
    result = {
        "platform": platform["name"],
        "domain": platform["domain"],
        "type": platform["type"],
        "tier": platform.get("tier", "P?"),
        "email": None,
        "author_name": None,
        "author_page": None,
        "twitter": None,
        "contact_url": None,
        "status": "unknown",
        "source": None,
        "notes": platform.get("notes", "")
    }

    base_url = f"https://{platform['domain']}"

    # 1. 尝试直接抓首页 + 页脚（最快）
    try:
        await page.goto(base_url, timeout=15000, wait_until="domcontentloaded")
        await asyncio.sleep(1.5)
        content = await page.content()
        emails = re.findall(r'[\w.+-]+@[\w-]+\.[\w.-]+', content)
        # 过滤常见非联系人邮箱
        valid_emails = [e for e in emails if not any(x in e.lower() for x in
            ["noreply", "no-reply", "example", "domain", "localhost", "test."])]
        if valid_emails:
            # 优先匹配平台的 email_hints
            for hint in platform.get("email_hints", []):
                for e in valid_emails:
                    if hint.replace("@", "") in e.lower():
                        result["email"] = e
                        result["source"] = "homepage/footer"
                        result["status"] = "found"
                        break
                if result["email"]:
                    break
            # 如果没匹配到 hint，取第一个
            if not result["email"] and valid_emails:
                result["email"] = valid_emails[0]
                result["source"] = "homepage/footer (unconfirmed)"
                result["status"] = "found_unconfirmed"
    except Exception as e:
        result["notes"] = f"Homepage error: {str(e)[:50]}"

    # 2. 尝试联系页
    for path in platform.get("contact_patterns", []):
        if result["email"] and result["status"] == "found":
            break
        try:
            contact_url = base_url + path
            await page.goto(contact_url, timeout=15000, wait_until="domcontentloaded")
            await asyncio.sleep(1.5)
            content = await page.content()
            emails = re.findall(r'[\w.+-]+@[\w-+\.]+', content)
            for hint in platform.get("email_hints", []):
                for e in emails:
                    if hint.replace("@", "") in e.lower():
                        result["email"] = e
                        result["contact_url"] = contact_url
                        result["source"] = f"contact page: {path}"
                        result["status"] = "found"
                        break
                if result["email"]:
                    break
        except Exception:
            pass

    # 3. 尝试作者页
    if platform.get("author_page_pattern"):
        try:
            author_url = base_url + platform["author_page_pattern"]
            await page.goto(author_url, timeout=15000, wait_until="domcontentloaded")
            await asyncio.sleep(1.5)
            content = await page.content()
            # 找作者名字
            author_names = re.findall(r'(?:Written by|By|Author:?)\s+([A-Z][a-z]+\s+[A-Z][a-z]+)',
                                      content, re.IGNORECASE)
            if author_names:
                result["author_name"] = author_names[0].strip()
            # 找邮箱
            emails = re.findall(r'[\w.+-]+@[\w-]+\.[\w.-]+', content)
            for hint in platform.get("email_hints", []):
                for e in emails:
                    if hint.replace("@", "") in e.lower():
                        result["email"] = e
                        result["author_page"] = author_url
                        result["source"] = f"author page: {path}"
                        result["status"] = "found"
                        break
        except Exception:
            pass

    # 4. 提取 Twitter handle
    try:
        await page.goto(base_url, timeout=15000, wait_until="domcontentloaded")
        await asyncio.sleep(1)
        twitter_links = await page.query_selector_all('a[href*="twitter.com"], a[href*="x.com"]')
        for link in twitter_links[:3]:
            href = await link.get_attribute("href")
            if href and ("twitter.com" in href or "x.com" in href):
                result["twitter"] = href
                break
    except Exception:
        pass

    return result


async def discover_contacts_for_site(target_url, site_type="game", only_tiers=None):
    """
    主函数：给定目标网站 + 类型，返回相关外链平台的联系人信息

    target_url: 你的网站 URL（用于判断上下文）
    site_type: 'game' | 'tool' | 'saas' | 'content' | 'blog'
    only_tiers: ['P0'] | ['P0', 'P1'] | None 表示全部
    """
    # 获取推荐的平台列表
    recommended_names = find_platforms_for_site_type(site_type)
    all_platforms = get_all_platforms()

    # 过滤
    platforms_to_check = []
    for p in all_platforms:
        if p["name"] in recommended_names:
            if only_tiers is None or p["tier"] in only_tiers:
                platforms_to_check.append(p)

    print(f"[Contact Discoverer] 发现 {len(platforms_to_check)} 个相关平台")

    async with async_playwright() as pw:
        browser = await pw.chromium.launch(headless=True)
        page = await browser.new_page()

        results = []
        for p in platforms_to_check:
            print(f"  正在检测: {p['name']} ({p['tier']})...")
            result = await find_contacts_on_platform(page, p)
            results.append(result)

            icon = {"found": "✅", "found_unconfirmed": "⚠️", "unknown": "❌"}.get(
                result["status"], "❌")
            email_display = result["email"] or "未找到"
            print(f"    {icon} {result['platform']}: {email_display}")

            await asyncio.sleep(1.5)

        await browser.close()

    return results


async def print_report(results, target_url):
    """格式化输出联系人报告"""
    print(f"\n{'='*60}")
    print(f"联系人发现报告 — {target_url}")
    print(f"{'='*60}\n")

    found = [r for r in results if r["status"] in ("found", "found_unconfirmed")]
    not_found = [r for r in results if r["status"] == "unknown"]

    print(f"✅ 已找到联系人 ({len(found)} 个平台):")
    for r in found:
        tier_icon = {"P0": "🔴", "P1": "🟡", "P2": "🟢"}.get(r["tier"], "⚪")
        confirm = "" if r["status"] == "found" else " ⚠️未确认"
        print(f"  {tier_icon} [{r['tier']}] {r['platform']}")
        print(f"     邮箱: {r['email']}{confirm}")
        if r.get("author_name"):
            print(f"     作者: {r['author_name']}")
        if r.get("twitter"):
            print(f"     Twitter: {r['twitter']}")
        if r.get("notes"):
            print(f"     备注: {r['notes']}")
        print()

    if not_found:
        print(f"❌ 未找到联系人 ({len(not_found)} 个平台):")
        for r in not_found:
            tier_icon = {"P0": "🔴", "P1": "🟡", "P2": "🟢"}.get(r["tier"], "⚪")
            print(f"  {tier_icon} [{r['tier']}] {r['platform']} — {r['notes'] or '无公开联系方式'}")

    print(f"\n📋 外链优先级建议:")
    p0_with_email = [r for r in results if r["tier"] == "P0" and r["email"]]
    if p0_with_email:
        print(f"  优先发邮件 ({len(p0_with_email)} 个 P0 平台有邮箱):")
        for r in p0_with_email:
            print(f"    → {r['email']} ({r['platform']})")

    return results


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="外链平台联系人自动发现")
    parser.add_argument("target_url", help="你的网站 URL")
    parser.add_argument("--type", default="game", choices=["game", "tool", "saas", "content", "blog"],
                        help="网站类型")
    parser.add_argument("--tiers", default=None, help="只检查的层级，如 P0,P1")
    args = parser.parse_args()

    only_tiers = args.tiers.split(",") if args.tiers else None

    results = asyncio.run(discover_contacts_for_site(
        args.target_url,
        site_type=args.type,
        only_tiers=only_tiers
    ))

    asyncio.run(print_report(results, args.target_url))
