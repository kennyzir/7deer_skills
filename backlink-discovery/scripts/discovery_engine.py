"""
外链机会发现引擎
接收目标 URL → 多轮关键词派生 → 动态搜索 → 平台发现 → 存入数据库
"""

import asyncio
import json
import re
import os
import sys
import subprocess
import time
import urllib.parse
from datetime import datetime
from urllib.parse import urlparse
from typing import List, Dict, Set, Tuple

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__))))


# ============================================================
# Web Search（使用 DuckDuckGo API，不被拦截）
# ============================================================

def web_search(query: str, count: int = 10) -> List[Dict]:
    """
    用 DuckDuckGo HTML 页面抓取搜索结果（不被 bot 检测拦截）
    返回：[{url, title, snippet}, ...]
    """
    try:
        encoded_q = urllib.parse.quote(query)
        # 使用 DuckDuckGo HTML 版本
        url = f"https://html.duckduckgo.com/html/?q={encoded_q}&kl=wt-wt"

        result = subprocess.run(
            ["curl", "-s", "-L", "--max-time", "15",
             "-H", "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
             "-H", "Accept: text/html",
             url],
            capture_output=True, text=True, timeout=20
        )

        html = result.stdout
        if not html:
            return []

        results = []

        # 解析 DuckDuckGo HTML 结果
        # 格式：<a rel="nofollow" class="result__a" href="URL">TITLE</a> ... <a class="result__snippet" href="URL">SNIPPET</a>
        # 找所有链接
        link_pattern = re.compile(
            r'<a[^>]+class="result__a"[^>]+href="(https?://[^"]+)"[^>]*>([^<]+)</a>',
            re.IGNORECASE
        )

        for match in link_pattern.finditer(html):
            url_found = match.group(1).strip()
            title = re.sub(r'<[^>]+>', '', match.group(2)).strip()

            if url_found and title and "duckduckgo" not in url_found:
                parsed = urlparse(url_found)
                domain = parsed.netloc.replace("www.", "")
                if domain:
                    results.append({
                        "url": url_found,
                        "domain": domain,
                        "title": title[:200],
                        "query_used": query,
                        "found_at": datetime.now().isoformat()
                    })

        # 去重（同一域名的多个结果只取第一个）
        seen = set()
        unique = []
        for r in results:
            if r["domain"] not in seen:
                seen.add(r["domain"])
                unique.append(r)

        return unique[:count]

    except Exception as e:
        return []


# ============================================================
# 关键词派生引擎
# ============================================================

class KeywordEngine:
    """从 URL 动态派生多维关键词"""

    def __init__(self, url: str):
        self.url = url
        self.parsed = urlparse(url)
        self.domain = self.parsed.netloc.replace("www.", "")
        self.path_hint = self.parsed.path.strip("/").split("/")[0] if self.parsed.path else ""

    def extract_base_keywords(self) -> List[str]:
        """从 URL 提取种子关键词（多维度）"""
        keywords = set()

        # 域名分词
        domain_name = self.domain.replace(".com", "").replace(".org", "").replace(".io", "")
        parts = re.split(r'[-_.]', domain_name)
        keywords.update([p.lower() for p in parts if len(p) > 1])

        # 路径分词
        path_parts = re.split(r'[-_./]', self.path_hint)
        keywords.update([p.lower() for p in path_parts if len(p) > 1])

        # 追加通用品类词（基于域名特征猜测）
        domain_lower = self.domain.lower()
        if "calc" in domain_lower or "calculator" in domain_lower:
            keywords.update(["calculator", "calculation", "math", "mathematics", "game calculator"])
        if "roblox" in domain_lower:
            keywords.update(["roblox", "roblox studio", "game calculator", "lua", "roblox developer"])
        if "game" in domain_lower or "play" in domain_lower:
            keywords.update(["game", "gaming", "web game", "browser game"])
        if "tool" in domain_lower or "util" in domain_lower:
            keywords.update(["tool", "utility", "online tool"])

        # 去噪
        stopwords = {"the", "and", "for", "you", "your", "best", "free", "top", "cool", "com"}
        keywords = {k for k in keywords if k not in stopwords and len(k) > 1}

        return list(keywords)

    def derive_keywords(self, base_keywords: List[str]) -> List[str]:
        """从种子关键词派生多维长尾关键词"""
        derived = set()
        seeds = [k.lower() for k in base_keywords if len(k) > 1]

        for seed in seeds:
            # 品类扩展
            derived.add(f"{seed} calculator")
            derived.add(f"{seed} calculation tool")
            derived.add(f"{seed} math")
            derived.add(f"free {seed} calculator")
            derived.add(f"online {seed} calculator")

            # 场景扩展
            derived.add(f"{seed} game")
            derived.add(f"{seed} gaming")
            derived.add(f"{seed} web game")
            derived.add(f"free {seed} game")
            derived.add(f"{seed} browser game")

            # 开发者场景
            derived.add(f"{seed} developer tool")
            derived.add(f"{seed} creator")
            derived.add(f"{seed} builder")
            derived.add(f"{seed} resource")
            derived.add(f"{seed} for developers")
            derived.add(f"{seed} studio")

            # 对比/替代
            derived.add(f"best {seed} alternatives")
            derived.add(f"{seed} alternatives free")
            derived.add(f"similar to {seed}")
            derived.add(f"awesome {seed}")
            derived.add(f"top {seed} tools")

            # 问题词
            derived.add(f"how to use {seed}")
            derived.add(f"{seed} for game")
            derived.add(f"{seed} online free")

            # 年份长尾
            for year in [2025, 2026]:
                derived.add(f"best {seed} {year}")

        return list(derived)[:80]

    def build_search_queries(self, keywords: List[str]) -> List[str]:
        """构建搜索查询列表"""
        queries = []
        for kw in keywords[:20]:
            queries.extend([
                f'"{kw}" "best alternatives"',
                f'"{kw}" "free" "tools" "list"',
                f'"{kw}" "directory" "submit" "free"',
                f'"{kw}" alternatives site:.com',
                f'awesome {kw}',
                f'best {kw} tools',
            ])

        seen = set()
        unique = []
        for q in queries:
            if q not in seen and len(q) < 120:
                seen.add(q)
                unique.append(q)

        return unique[:40]


# ============================================================
# 平台分类引擎
# ============================================================

LINK_METHODS = {
    "github_pr": "GitHub PR / 资源列表",
    "wiki_edit": "Wiki 词条编辑",
    "alternatives_article": "Alternatives 文章 Outreach",
    "directory": "目录提交",
    "forum_post": "论坛发帖/评论",
    "guest_post": "Guest Post / 文章引用",
    "social_post": "社交媒体帖子",
    "email_outreach": "冷邮件 outreach",
    "press_release": "新闻稿/记者联系",
    "education_resource": "教育资源页提交",
    "manual_review": "需人工评估",
}


def classify_platform(domain: str, title: str) -> Tuple[str, float, str]:
    """
    判断平台类型、外链方式、相关度
    返回：(最佳外链方式, 相关度0-1, 平台类型)
    """
    combined = f"{domain} {title}".lower()
    method_scores = {}

    # GitHub 资源列表
    if "github.com" in domain or "github" in combined:
        if any(k in combined for k in ["awesome", "list", "curated", "resource"]):
            return "github_pr", 0.8, "GitHub Resource List"
        return "github_pr", 0.5, "GitHub"

    # Wiki
    if any(k in domain for k in ["wikipedia", "fandom", "wikia", "wiki"]):
        return "wiki_edit", 0.7, "Wiki/Encyclopedia"

    # Alternatives 文章
    if any(k in combined for k in ["alternatives", "best ", "vs ", "similar to", "comparison"]):
        if any(k in combined for k in ["free", "tool", "game", "app"]):
            return "alternatives_article", 0.85, "Alternatives Article"

    # 目录站
    if any(k in combined for k in ["directory", "directory", "submit"]):
        if any(k in combined for k in ["free", "tool", "game", "app", "software"]):
            return "directory", 0.7, "Directory"

    # 游戏论坛
    if any(k in combined for k in ["reddit", "forum", "community"]):
        return "forum_post", 0.6, "Forum/Community"

    # 开发者博客
    if any(k in combined for k in ["dev.to", "hashnode", "medium", "blog"]):
        return "guest_post", 0.65, "Developer Blog"

    # 新闻/媒体
    if any(k in combined for k in ["news", "article", "media", "press"]):
        return "press_release", 0.5, "News/Media"

    # 教育
    if any(k in combined for k in ["education", "teacher", "school", "university", "learning"]):
        return "education_resource", 0.7, "Education"

    # Product Hunt 类
    if "producthunt" in domain or "alternativeto" in domain:
        return "directory", 0.6, "Product Discovery"

    return "manual_review", 0.3, "Unknown"


# ============================================================
# 数据库管理
# ============================================================

DB_BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "memory")


def get_target_dir(target_url: str) -> str:
    domain = urlparse(target_url).netloc.replace("www.", "")
    target_dir = os.path.join(DB_BASE, domain)
    os.makedirs(target_dir, exist_ok=True)
    return target_dir


def load_db(target_url: str) -> Dict:
    target_dir = get_target_dir(target_url)
    pf = os.path.join(target_dir, "platforms.json")
    kf = os.path.join(target_dir, "keywords.json")
    sf = os.path.join(target_dir, "search_rounds.json")

    platforms = []
    if os.path.exists(pf):
        with open(pf) as f:
            data = json.load(f)
            platforms = data.get("platforms", [])

    keywords = {"seed": [], "derived": [], "used_queries": [], "found_domains": []}
    if os.path.exists(kf):
        with open(kf) as f:
            keywords = json.load(f)

    rounds = []
    if os.path.exists(sf):
        with open(sf) as f:
            rounds = json.load(f)

    return {
        "platforms": platforms,
        "keywords": keywords,
        "rounds": rounds,
    }


def save_db(target_url: str, db: Dict):
    target_dir = get_target_dir(target_url)
    with open(os.path.join(target_dir, "platforms.json"), "w") as f:
        json.dump({"platforms": db["platforms"], "last_updated": datetime.now().isoformat()}, f, indent=2)
    with open(os.path.join(target_dir, "keywords.json"), "w") as f:
        json.dump(db["keywords"], f, indent=2)
    with open(os.path.join(target_dir, "search_rounds.json"), "w") as f:
        json.dump(db["rounds"], f, indent=2)


# ============================================================
# 搜索执行
# ============================================================

def search_round_duckduckgo(queries: List[str]) -> Tuple[List[Dict], Set[str]]:
    """执行一组搜索，返回发现的平台域名列表"""
    all_domains = set()
    all_platforms = []

    for query in queries:
        results = web_search(query, count=8)
        for r in results:
            if r["domain"] and "duckduckgo" not in r["domain"]:
                all_platforms.append(r)
                all_domains.add(r["domain"])
        time.sleep(0.5)

    return all_platforms, all_domains


# ============================================================
# 主发现流程
# ============================================================

def run_discovery(target_url: str, max_rounds: int = 5):
    """
    执行多轮发现
    """
    print(f"[Discovery Engine] 启动")
    print(f"目标: {target_url}")
    print(f"最大轮次: {max_rounds}")
    print()

    engine = KeywordEngine(target_url)
    db = load_db(target_url)

    existing_domains = set(db["keywords"].get("found_domains", []))
    used_queries = set(db["keywords"].get("used_queries", []))

    print(f"[状态] 已有平台: {len(existing_domains)} 个")

    # Step 1: 种子关键词
    if not db["keywords"]["seed"]:
        seeds = engine.extract_base_keywords()
        db["keywords"]["seed"] = seeds
        print(f"[Step 1] 种子关键词: {seeds}")
    else:
        print(f"[Step 1] 复用种子: {db['keywords']['seed']}")

    # Step 2: 派生关键词
    if not db["keywords"]["derived"]:
        derived = engine.derive_keywords(db["keywords"]["seed"])
        db["keywords"]["derived"] = derived
        print(f"[Step 2] 派生关键词: {len(derived)} 个")
    else:
        print(f"[Step 2] 复用派生: {len(db['keywords']['derived'])} 个")

    # 多轮搜索
    all_new_platforms = []
    all_new_domains = set()

    for round_num in range(1, max_rounds + 1):
        # 获取待搜索关键词
        if round_num == 1:
            keywords_to_search = db["keywords"]["derived"][:15]
        else:
            # 从已发现域名标题提取新关键词（如果派生词用完了）
            if all_new_platforms:
                new_kw = [p["title"].lower() for p in all_new_platforms if len(p["title"]) > 3]
                keywords_to_search = new_kw[:10]
            else:
                keywords_to_search = db["keywords"]["derived"][round_num*5:(round_num+1)*5]

        if not keywords_to_search:
            print(f"[Round {round_num}] 无关键词，停止")
            break

        # 构建查询
        queries = engine.build_search_queries(keywords_to_search)
        queries = [q for q in queries if q not in used_queries]

        if not queries:
            print(f"[Round {round_num}] 无新查询，停止")
            break

        print(f"\n[Round {round_num}] 搜索 {len(queries)} 个查询...")

        platforms_found, domains_found = search_round_duckduckgo(queries[:20])

        # 标记已用
        for q in queries[:20]:
            used_queries.add(q)

        # 去重 + 新增
        new_this_round = 0
        for p in platforms_found:
            if p["domain"] not in existing_domains and p["domain"] not in all_new_domains:
                # 分类
                method, relevance, ptype = classify_platform(p["domain"], p["title"])
                p["method"] = method
                p["relevance"] = relevance
                p["platform_type"] = ptype
                p["discovered_round"] = round_num

                all_new_platforms.append(p)
                all_new_domains.add(p["domain"])
                existing_domains.add(p["domain"])
                new_this_round += 1

        # 记录轮次
        db["rounds"].append({
            "round": round_num,
            "queries_used": queries[:20],
            "platforms_found": len(platforms_found),
            "new_platforms": new_this_round,
            "timestamp": datetime.now().isoformat()
        })

        print(f"  本轮搜索: {len(platforms_found)} 个结果")
        print(f"  新平台: +{new_this_round} 个")
        print(f"  平台库累计: {len(all_new_domains)} 个新平台")

        # 保存进度
        db["platforms"].extend(all_new_platforms)
        db["keywords"]["found_domains"] = list(existing_domains)
        db["keywords"]["used_queries"] = list(used_queries)
        save_db(target_url, db)

        # 如果2轮都没新发现，停止
        if new_this_round == 0 and round_num >= 2:
            print(f"\n连续2轮无新发现，停止")
            break

    # 最终保存
    db["platforms"].extend(all_new_platforms)
    save_db(target_url, db)

    # 生成汇总
    summary = generate_summary(db["platforms"])

    print(f"\n{'='*60}")
    print(f"发现完成")
    print(f"{'='*60}")
    print(summary["text"])
    print(f"\n平台库: {len(db['platforms'])} 个平台")
    print(f"数据目录: {get_target_dir(target_url)}")

    return db, summary


def generate_summary(platforms: List[Dict]) -> Dict:
    """生成汇总"""
    if not platforms:
        return {"text": "未发现任何平台", "by_method": {}, "total": 0}

    # 按相关度排序
    high = sorted([p for p in platforms if p.get("relevance", 0) >= 0.7],
                  key=lambda x: x.get("relevance", 0), reverse=True)
    mid = sorted([p for p in platforms if 0.4 <= p.get("relevance", 0) < 0.7],
                key=lambda x: x.get("relevance", 0), reverse=True)
    low = sorted([p for p in platforms if p.get("relevance", 0) < 0.4],
                key=lambda x: x.get("relevance", 0), reverse=True)

    by_method = {}
    for p in platforms:
        m = p.get("method", "unknown")
        if m not in by_method:
            by_method[m] = []
        by_method[m].append(p)

    lines = []
    lines.append(f"🔴 P0 高相关平台 ({len(high)} 个):")
    for p in high[:10]:
        method_label = LINK_METHODS.get(p.get("method", ""), p.get("method", ""))
        lines.append(f"  - [{p['domain']}] {method_label} (rel={p.get('relevance', 0):.2f})")

    lines.append(f"\n🟡 P1 中相关平台 ({len(mid)} 个):")
    for p in mid[:5]:
        method_label = LINK_METHODS.get(p.get("method", ""), p.get("method", ""))
        lines.append(f"  - [{p['domain']}] {method_label}")

    lines.append(f"\n🟢 P2 低相关平台 ({len(low)} 个):")
    for p in low[:5]:
        method_label = LINK_METHODS.get(p.get("method", ""), p.get("method", ""))
        lines.append(f"  - [{p['domain']}]")

    lines.append(f"\n📊 按外链方式分布:")
    for method, plats in sorted(by_method.items(), key=lambda x: len(x[1]), reverse=True):
        label = LINK_METHODS.get(method, method)
        lines.append(f"  - {label}: {len(plats)} 个")

    return {
        "text": "\n".join(lines),
        "high": high,
        "mid": mid,
        "low": low,
        "by_method": by_method,
        "total": len(platforms)
    }


def query_results(target_url: str) -> Dict:
    """查询已有结果"""
    db = load_db(target_url)
    if not db["platforms"]:
        return {"status": "empty", "message": "暂无数据，请运行发现引擎"}

    summary = generate_summary(db["platforms"])
    return {
        "status": "found",
        "total": len(db["platforms"]),
        "last_updated": db["platforms"][-1].get("found_at") if db["platforms"] else None,
        "summary": summary,
        "db_path": get_target_dir(target_url)
    }


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="外链机会发现引擎")
    parser.add_argument("target_url", help="目标网站 URL")
    parser.add_argument("--rounds", type=int, default=5, help="搜索轮次")
    parser.add_argument("--query", action="store_true", help="仅查询已有结果")
    args = parser.parse_args()

    if args.query:
        result = query_results(args.target_url)
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        db, summary = run_discovery(args.target_url, args.rounds)
