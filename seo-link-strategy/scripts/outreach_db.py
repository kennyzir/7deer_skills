"""
外链平台动态发现 + 邮件外链库
给定目标网站 URL，动态搜索相关平台，长期积累到本地数据库
"""

import asyncio
import json
import re
import sys
import os
from datetime import datetime
from urllib.parse import urlparse

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__))))

from playwright.async_api import async_playwright


# ============================================================
# 外链库存储
# ============================================================

DB_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "memory", "outreach_db")
os.makedirs(DB_DIR, exist_ok=True)

PLATFORM_DB_FILE = os.path.join(DB_DIR, "platforms.json")
EMAIL_DB_FILE = os.path.join(DB_DIR, "email_history.json")


def load_platform_db():
    if os.path.exists(PLATFORM_DB_FILE):
        with open(PLATFORM_DB_FILE) as f:
            return json.load(f)
    return {"platforms": [], "last_updated": None}


def save_platform_db(db):
    db["last_updated"] = datetime.now().isoformat()
    with open(PLATFORM_DB_FILE, "w") as f:
        json.dump(db, f, indent=2, ensure_ascii=False)


def load_email_history():
    if os.path.exists(EMAIL_DB_FILE):
        with open(EMAIL_DB_FILE) as f:
            return json.load(f)
    return {"emails": [], "sequences": []}


def save_email_history(hist):
    with open(EMAIL_DB_FILE, "w") as f:
        json.dump(hist, f, indent=2, ensure_ascii=False)


# ============================================================
# 关键词提取
# ============================================================

def extract_keywords_from_url(url, product_type="game"):
    """
    从 URL 和类型生成搜索关键词
    """
    parsed = urlparse(url)
    domain = parsed.netloc.replace("www.", "")
    path_hint = parsed.path.strip("/").split("/")[0] if parsed.path else ""

    # 基于路径的关键词
    base_keywords = [domain.replace(".com", "").replace(".org", "").replace("-", " ")]

    # 类型相关的关键词
    type_keywords = {
        "game": ["game", "free game", "online game", "browser game", "H5 game",
                "guessing game", "geography game", "trivia", "educational game"],
        "tool": ["tool", "software", "app", "free tool", "online tool",
                "productivity", "automation"],
        "saas": ["SaaS", "software", "platform", "tool", "service"],
        "content": ["blog", "article", "guide", "tutorial", "resource"],
    }

    keywords = set(base_keywords + type_keywords.get(product_type, []))

    # 添加 site: 搜索变体
    search_queries = [
        f'"{domain}" "best" "alternatives"',
        f'"best free {domain}" "alternatives"',
        f'"{path_hint or domain}" "tools I use"',
        f'site:{domain} "contact" OR "about"',
        f'"{path_hint or domain}" submit "directory"',
        f'"{path_hint or domain}" "submit your" "free"',
        f'best free {path_hint or domain} alternatives 2025 OR 2026',
        f'"alternatives to" "{path_hint or domain}" "free"',
    ]

    return {
        "base_keywords": list(keywords),
        "search_queries": search_queries,
        "domain": domain
    }


def generate_search_queries(url, product_type):
    """
    给定网站，生成多组搜索查询来发现相关平台
    """
    kw = extract_keywords_from_url(url, product_type)
    queries = []

    # Alternatives 文章查询
    for keyword in kw["base_keywords"]:
        queries.extend([
            f'"{keyword}" "best free alternatives" 2026',
            f'"{keyword}" "alternatives you should try"',
            f'best free {keyword} alternatives site:com',
            f'best {keyword} to use instead of',
            f'"{keyword}" "vs" "similar" "free"',
        ])

    # 目录发现查询
    for keyword in kw["base_keywords"][:3]:
        queries.extend([
            f'submit free {keyword} directory',
            f'"{keyword}" "submit your site" free',
            f'free {keyword} directory list submit',
        ])

    # 资源页查询
    queries.extend([
        f'best {kw["domain"]} tools I use',
        f'awesome list {kw["domain"]}',
    ])

    # 去重
    seen = set()
    unique = []
    for q in queries:
        if q not in seen:
            seen.add(q)
            unique.append(q)

    return unique[:20]  # 限制搜索量


# ============================================================
# 平台发现（从搜索结果）
# ============================================================

async def discover_platforms_from_search(query, max_results=10):
    """
    用搜索引擎发现提到某个关键词 + "alternatives" 的文章站
    返回发现的平台列表
    """
    discovered = []

    # DuckDuckGo 搜索
    search_url = f"https://duckduckgo.com/?q={query.replace(' ', '+')}&ia=web"

    async with async_playwright() as pw:
        browser = await pw.chromium.launch(headless=True)
        page = await browser.new_page()

        try:
            await page.goto(search_url, timeout=20000, wait_until="domcontentloaded")
            await asyncio.sleep(3)

            # 提取搜索结果
            links = await page.query_selector_all("a[data-testid='result-title']")
            results = []
            for link in links[:max_results]:
                href = await link.get_attribute("href")
                title = await link.inner_text()
                if href and "://" in href:
                    results.append({"url": href, "title": title.strip()})

            # 从URL提取域名
            for r in results:
                parsed = urlparse(r["url"])
                domain = parsed.netloc.replace("www.", "")
                if domain:
                    discovered.append({
                        "domain": domain,
                        "url": r["url"],
                        "article_title": r["title"],
                        "discovered_from_query": query,
                        "discovered_at": datetime.now().isoformat()
                    })

        except Exception as e:
            print(f"  搜索失败: {str(e)[:40]}")
        finally:
            await browser.close()

    return discovered


def extract_contacts_from_page_sync(html_content, domain):
    """
    从页面 HTML 提取邮箱（同步版）
    """
    emails = re.findall(r'[\w.+-]+@[\w-]+\.[\w.-]+', html_content)
    valid = [e for e in emails if not any(x in e.lower() for x in
        ["noreply", "no-reply", "example", "localhost", "test.", ".png", ".jpg"])]
    return list(set(valid))


async def check_platform_contact(page, platform_url, domain):
    """
    检测平台是否有联系表单或邮箱
    """
    result = {
        "domain": domain,
        "url": platform_url,
        "email": None,
        "contact_url": None,
        "submit_url": None,
        "has_form": False,
        "requires_login": False,
        "requires_payment": False,
        "notes": ""
    }

    try:
        resp = await page.goto(platform_url, timeout=15000, wait_until="domcontentloaded")
        status = resp.status if resp else 0
        await asyncio.sleep(2)

        content = await page.content()

        # 提取邮箱
        emails = extract_contacts_from_page_sync(content, domain)
        if emails:
            result["email"] = emails[0]

        # 检测提交表单
        contact_paths = ["/contact", "/submit", "/submit-a-tool", "/add",
                         "/list", "/contribute", "/developers"]
        for path in contact_paths:
            try:
                resp2 = await page.goto(platform_url + path, timeout=10000)
                if resp2 and resp2.status < 400:
                    result["submit_url"] = platform_url + path
                    result["has_form"] = True
                    break
            except:
                pass

        # 检测是否需要登录/付费
        text_lower = content.lower()
        if any(k in text_lower for k in ["login", "sign in", "account required"]):
            result["requires_login"] = True
        if any(k in text_lower for k in ["paid", "premium", "subscription required",
                                          "upgrade", "pro plan"]):
            result["requires_payment"] = True

    except Exception as e:
        result["notes"] = str(e)[:50]

    return result


# ============================================================
# 主发现流程
# ============================================================

async def discover_and_enrich(target_url, product_type="game", max_platforms=15):
    """
    完整流程：
    1. 生成搜索关键词
    2. 动态发现平台
    3. 检测联系人
    4. 保存到数据库
    """
    print(f"[Outreach DB] 开始动态发现...")
    print(f"目标: {target_url}")
    print(f"类型: {product_type}")
    print()

    # Step 1: 生成搜索查询
    queries = generate_search_queries(target_url, product_type)
    print(f"[Step 1] 生成 {len(queries)} 个搜索查询")
    for q in queries[:5]:
        print(f"  - {q}")
    print()

    # Step 2: 搜索发现平台
    all_discovered = []
    for query in queries:
        print(f"[Step 2] 搜索: {query[:60]}...")
        found = await discover_platforms_from_search(query, max_results=5)
        print(f"  → 发现 {len(found)} 个平台")
        all_discovered.extend(found)
        await asyncio.sleep(1.5)

    # 去重（按域名）
    seen_domains = set()
    unique_platforms = []
    for p in all_discovered:
        if p["domain"] not in seen_domains:
            seen_domains.add(p["domain"])
            unique_platforms.append(p)

    print(f"\n[Step 2 完成] 去重后: {len(unique_platforms)} 个独立平台")
    print()

    # Step 3: 加载已有库，对比过滤
    db = load_platform_db()
    existing_domains = {p["domain"] for p in db["platforms"]}
    new_platforms = [p for p in unique_platforms if p["domain"] not in existing_domains]

    print(f"[Step 3] 已有库: {len(db['platforms'])} 个平台")
    print(f"         新发现: {len(new_platforms)} 个平台")
    print()

    if not new_platforms:
        print("没有新平台需要检测")
        return db

    # Step 4: 检测新平台的联系人
    print(f"[Step 4] 检测 {min(len(new_platforms), max_platforms)} 个新平台的联系方式...")
    checked = []

    async with async_playwright() as pw:
        browser = await pw.chromium.launch(headless=True)
        page = await browser.new_page()

        for p in new_platforms[:max_platforms]:
            print(f"  检测: {p['domain']}... ", end="", flush=True)
            contact = await check_platform_contact(page, f"https://{p['domain']}", p["domain"])
            checked.append({**p, **contact})
            status = []
            if contact["email"]:
                status.append(f"📧 {contact['email']}")
            if contact["has_form"]:
                status.append("📝 有表单")
            if contact["requires_login"]:
                status.append("🔐 需登录")
            if contact["requires_payment"]:
                status.append("💰 需付费")
            if not status:
                status.append("❌ 无公开联系")
            print("; ".join(status))
            await asyncio.sleep(1)

        await browser.close()

    # Step 5: 合并到库
    db["platforms"].extend(checked)

    # 分类 P0/P1/P2
    for p in checked:
        p["tier"] = classify_platform(p)

    save_platform_db(db)
    print(f"\n[Step 5 完成] 平台库已更新，共 {len(db['platforms'])} 个平台")

    return db


def classify_platform(platform):
    """
    根据平台特征自动分类
    """
    domain = platform.get("domain", "").lower()
    article_title = platform.get("article_title", "").lower()
    notes = platform.get("notes", "").lower()

    if "alternatives" in article_title or "best" in article_title:
        return "P0"  # Alternatives 文章站
    elif platform.get("has_form") and not platform.get("requires_payment"):
        return "P1"  # 有表单可免费提交
    elif "directory" in domain or "directory" in notes:
        return "P1"  # 目录站
    elif platform.get("requires_login") or platform.get("requires_payment"):
        return "P2"  # 需要登录或付费
    else:
        return "P2"  # 社区/资源页


# ============================================================
# 平台库查询
# ============================================================

def query_platforms(product_type=None, tier=None, has_email=None, limit=None):
    """
    查询平台库
    product_type: 'game' | 'tool' | etc (保留字段)
    tier: 'P0' | 'P1' | 'P2'
    has_email: True | False | None(不限)
    limit: int
    """
    db = load_platform_db()

    results = db["platforms"]

    if tier:
        results = [p for p in results if p.get("tier") == tier]
    if has_email is True:
        results = [p for p in results if p.get("email")]
    elif has_email is False:
        results = [p for p in results if not p.get("email")]

    if limit:
        results = results[:limit]

    return results


def print_platform_report(platforms, title="平台库查询结果"):
    print(f"\n{'='*60}")
    print(f"{title}")
    print(f"{'='*60}\n")

    by_tier = {"P0": [], "P1": [], "P2": []}
    for p in platforms:
        tier = p.get("tier", "?")
        if tier in by_tier:
            by_tier[tier].append(p)

    for tier in ["P0", "P1", "P2"]:
        tier_platforms = by_tier[tier]
        if not tier_platforms:
            continue
        icon = {"P0": "🔴", "P1": "🟡", "P2": "🟢"}.get(tier, "⚪")
        print(f"{icon} [{tier}] — {len(tier_platforms)} 个平台")

        actionable = [p for p in tier_platforms if p.get("email")]
        no_email = [p for p in tier_platforms if not p.get("email")]

        if actionable:
            print(f"   ✅ 可直接发邮件 ({len(actionable)}):")
            for p in actionable[:10]:
                print(f"     - {p['domain']} → {p.get('email', 'N/A')}")
        if no_email:
            print(f"   ⚠️ 无邮箱 ({len(no_email)}):")
            for p in no_email[:5]:
                print(f"     - {p['domain']} ({p.get('submit_url', '无提交页')})")
        print()

    print(f"共 {len(platforms)} 个平台，"
          f"可发邮件 {sum(1 for p in platforms if p.get('email'))} 个")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="外链平台动态发现")
    parser.add_argument("target_url", help="目标网站 URL")
    parser.add_argument("--type", default="game", help="网站类型")
    parser.add_argument("--max", type=int, default=15, help="最多检测平台数")
    parser.add_argument("--query-only", action="store_true", help="只生成搜索查询，不实际搜索")
    parser.add_argument("--list", action="store_true", help="列出已有平台库")
    parser.add_argument("--tier", default=None, help="只显示特定层级 P0/P1/P2")
    parser.add_argument("--has-email", action="store_true", help="只显示有邮箱的")
    args = parser.parse_args()

    if args.list:
        platforms = query_platforms(tier=args.tier, has_email=args.has_email if args.has_email else None)
        tier_name = args.tier or "所有"
        print_platform_report(platforms, f"平台库 ({tier_name})")
    elif args.query_only:
        queries = generate_search_queries(args.target_url, args.type)
        print(f"生成 {len(queries)} 个搜索查询:")
        for i, q in enumerate(queries, 1):
            print(f"  {i}. {q}")
    else:
        db = asyncio.run(discover_and_enrich(args.target_url, args.type, args.max))
        print()
        print_platform_report(db["platforms"], "最终平台库")
