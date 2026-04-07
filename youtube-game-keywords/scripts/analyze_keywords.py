#!/usr/bin/env python3
"""
analyze_keywords.py
从 YouTube 视频列表 JSON 中提取游戏关键词，生成结构化日报。

用法:
    python3 analyze_keywords.py INPUT_JSON [--output REPORT_PATH] [--max-candidates N]

依赖:
    pip install openai  (仅用于 GPT 分类，可选)
    或使用纯规则模式（默认，无需 API key）

纯规则模式说明:
    - 不需要任何 API key
    - 使用内置游戏名称词库 + 正则匹配
    - GPT 分类模式可通过 --use-gpt 开启（需要 OPENAI_API_KEY 环境变量）
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Optional

# ─────────────────────────────────────────
# 游戏词库（覆盖主流 + 独立 + Roblox）
# ─────────────────────────────────────────
KNOWN_GAMES: dict[str, dict] = {
    # Roblox Brainrot 系列
    "vacuum for brainrots": {"type": "Roblox", "genre": "Brainrot", "tier": "main"},
    "shuffle a brainrot": {"type": "Roblox", "genre": "Brainrot", "tier": "main"},
    "obby but you're a": {"type": "Roblox", "genre": "Obby", "tier": "main"},
    "titan trial": {"type": "Roblox", "genre": "RPG", "tier": "sub"},
    "blox fruits": {"type": "Roblox", "genre": "Action", "tier": "main"},
    "adopt me": {"type": "Roblox", "genre": "Social", "tier": "main"},
    "pet simulator": {"type": "Roblox", "genre": "Sim", "tier": "sub"},
    "brookhaven": {"type": "Roblox", "genre": "Sandbox", "tier": "main"},
    "tower of hell": {"type": "Roblox", "genre": "Platformer", "tier": "sub"},
    "murder mystery": {"type": "Roblox", "genre": "Social Deduction", "tier": "sub"},
    " royale high": {"type": "Roblox", "genre": "Roleplay", "tier": "sub"},
    "welcome to bloxburg": {"type": "Roblox", "genre": "Life Sim", "tier": "sub"},
    "work at a pizza": {"type": "Roblox", "genre": "Sim", "tier": "sub"},
    "mm2": {"type": "Roblox", "genre": "Murder Mystery", "tier": "sub"},
    "bee swarm": {"type": "Roblox", "genre": "Sim", "tier": "sub"},
    "King Legacy": {"type": "Roblox", "genre": "Action", "tier": "main"},
    "Anime Vanguard": {"type": "Roblox", "genre": "Anime", "tier": "main"},
    "Project Slayers": {"type": "Roblox", "genre": "Anime", "tier": "main"},
    "Grow a Garden": {"type": "Roblox", "genre": "Sim", "tier": "main"},
    "Dandy's World": {"type": "Roblox", "genre": "Horror", "tier": "main"},
    "Bite By Night": {"type": "Roblox", "genre": "Horror", "tier": "main"},
    "Sailor Piece": {"type": "Roblox", "genre": "Anime", "tier": "main"},
    "Lucky Block": {"type": "Roblox", "genre": "Sim", "tier": "sub"},
    "Escape Forest for Brainrots": {"type": "Roblox", "genre": "Brainrot", "tier": "sub"},
    "Football Rush Simulator": {"type": "Roblox", "genre": "Sim", "tier": "sub"},
    "Chicken Rocket": {"type": "Roblox", "genre": "Brainrot", "tier": "sub"},
    "Tap Simulator": {"type": "Roblox", "genre": "Sim", "tier": "sub"},
    "Clean Crew": {"type": "Roblox", "genre": "Horror", "tier": "upcoming"},

    # Steam / 独立游戏
    "minecraft": {"type": "PC/Console", "genre": "Sandbox", "tier": "main"},
    "terraria": {"type": "PC/Console", "genre": "Sandbox", "tier": "sub"},
    "stardew valley": {"type": "PC/Console", "genre": "Sim", "tier": "sub"},
    "hollow knight": {"type": "PC/Console", "genre": "Metroidvania", "tier": "sub"},
    "celeste": {"type": "PC/Console", "genre": "Platformer", "tier": "sub"},
    "hades": {"type": "PC/Console", "genre": "Roguelike", "tier": "sub"},
    "slay the spire": {"type": "PC/Console", "genre": "Deckbuilder", "tier": "main"},
    "slay the spire 2": {"type": "PC/Console", "genre": "Deckbuilder", "tier": "main"},
    "project lunky": {"type": "PC/Console", "genre": "Roguelike", "tier": "rising"},
    "bridger": {"type": "PC/Console", "genre": "Puzzle", "tier": "rising"},
    "mouthwashing": {"type": "PC/Console", "genre": "Horror", "tier": "rising"},
    "dungeon settlers": {"type": "PC/Console", "genre": "Roguelike", "tier": "rising"},
    "eversiege": {"type": "PC/Console", "genre": "Roguelike", "tier": "rising"},
    "sin & siege": {"type": "PC/Console", "genre": "Roguelike", "tier": "rising"},
    "signal zone": {"type": "PC/Console", "genre": "Strategy", "tier": "rising"},
    "idols of ash": {"type": "PC/Console", "genre": "Horror", "tier": "rising"},
    "project songbird": {"type": "PC/Console", "genre": "Adventure", "tier": "rising"},
    "woman simulator": {"type": "PC/Console", "genre": "Casual", "tier": "trending"},
    "nintendo": {"type": "PC/Console", "genre": "General", "tier": "sub"},
    "playstation": {"type": "PC/Console", "genre": "General", "tier": "sub"},
    "xbox": {"type": "PC/Console", "genre": "General", "tier": "sub"},
    "street fighter": {"type": "PC/Console", "genre": "Fighting", "tier": "sub"},
    "dragon quest": {"type": "PC/Console", "genre": "RPG", "tier": "sub"},
    "rimworld": {"type": "PC/Console", "genre": "Sim", "tier": "sub"},
    "dspgaming": {"type": "PC/Console", "genre": "General", "tier": "live"},
}

# Roblox 特征词
ROBLOX_SIGNALS = ["roblox", "blox", "obey me", "tds ", "bedwars", "build a boat", "arsenal", "phantom forces"]
# 独立游戏特征
INDIE_SIGNALS = ["indie game", "steam", "itch.io", "gog", "humble"]
# 主机大作特征
CONSOLE_SIGNALS = ["playstation", "xbox", "nintendo switch", "ps5", "xbox series"]


def parse_views(view_text: str) -> int:
    """从播放量文本提取数字。"""
    if not view_text:
        return 0
    text = view_text.lower().replace(",", "").replace(".", "")
    m = re.search(r"([\d.]+)\s*(k|K)?(m|M)?(b|B)?", text)
    if not m:
        return 0
    num = float(m.group(1))
    if m.group(2):  # K
        num *= 1_000
    elif m.group(3):  # M
        num *= 1_000_000
    return int(num)


def relative_to_date(published_text: str) -> Optional[datetime]:
    """将 '2 days ago' 等文本转为日期。"""
    if not published_text:
        return None
    text = published_text.lower().strip()
    now = datetime.now(timezone.utc)
    days_match = re.search(r"(\d+)\s*(day|d)", text)
    if days_match:
        return now - timedelta(days=int(days_match.group(1)))
    weeks_match = re.search(r"(\d+)\s*(week|w)", text)
    if weeks_match:
        return now - timedelta(weeks=int(weeks_match.group(1)))
    months_match = re.search(r"(\d+)\s*(month|mo)", text)
    if months_match:
        return now - timedelta(days=int(months_match.group(1)) * 30)
    hours_match = re.search(r"(\d+)\s*(hour|h)(?!r)", text)
    if hours_match:
        return now - timedelta(hours=int(hours_match.group(1)))
    return None


def classify_game(title: str, channel_name: str, url: str) -> Optional[dict]:
    """用规则引擎识别游戏，返回 game dict 或 None。"""
    title_lower = title.lower()
    url_lower = url.lower() if url else ""

    # 跳过直播
    if "live" in title_lower or "livestream" in title_lower:
        if not any(s in title_lower for s in ROBLOX_SIGNALS + INDIE_SIGNALS + CONSOLE_SIGNALS):
            return None

    # 跳过非游戏
    skip_patterns = ["meme", "compilation", "reaction", "vlog", "music video", "shorts"]
    if any(p in title_lower for p in skip_patterns) and not any(s in title_lower for s in ["game", "play", "roblox"]):
        return None

    game_type = "Unknown"
    genre = "General"

    # Roblox 检测
    if any(s in title_lower for s in ROBLOX_SIGNALS) or "roblox.com" in url_lower:
        game_type = "Roblox"
        for game_name, info in KNOWN_GAMES.items():
            if game_name in title_lower:
                genre = info["genre"]
                break
    # 独立/PC/Console 检测
    elif any(s in title_lower for s in INDIE_SIGNALS) or any(s in title_lower for s in CONSOLE_SIGNALS):
        game_type = "PC/Console"
        for game_name, info in KNOWN_GAMES.items():
            if game_name in title_lower:
                genre = info["genre"]
                break
        if game_type == "Unknown":
            genre = "PC Game"
    else:
        # 遍历词库
        for game_name, info in KNOWN_GAMES.items():
            if game_name in title_lower:
                game_type = info["type"]
                genre = info["genre"]
                break

    if game_type == "Unknown":
        return None

    return {
        "name": title,
        "type": game_type,
        "genre": genre,
        "channel": channel_name,
        "url": url,
    }


def build_digest(videos: list[dict], max_candidates: int = 12) -> str:
    """生成文本格式日报。"""
    today = datetime.now().strftime("%Y-%m-%d")

    # 分类收集
    roblox = []
    indie = []
    console = []
    live = []

    for v in videos:
        game = classify_game(v.get("title", ""), v.get("channel_name", ""), v.get("url", ""))
        if not game:
            continue
        game["views"] = parse_views(v.get("view_text", ""))
        game["published_text"] = v.get("published_text", "")

        t = game["type"]
        if t == "Roblox":
            roblox.append(game)
        elif t == "PC/Console":
            if "live" in game["name"].lower():
                live.append(game)
            elif game["genre"] in ("Deckbuilder", "Roguelike", "Horror", "Adventure", "Puzzle"):
                indie.append(game)
            else:
                console.append(game)

    # 按播放量排序
    for lst in [roblox, indie, console, live]:
        lst.sort(key=lambda x: x["views"], reverse=True)

    lines = [f"📺 YouTube 订阅频道日报 — {today}", ""]
    lines.append("【今日概要】")
    if roblox:
        top = roblox[0]
        lines.append(f"Roblox 赛道最热：{top['name']}（{top['channel']}，{top['views']:,} 播放）")
    if indie:
        top = indie[0]
        lines.append(f"独立游戏亮点：{top['name']}（{top['channel']}，{top['views']:,} 播放）")
    lines.append("")

    def section(title: str, items: list[dict], limit: int):
        if not items:
            return
        lines.append(f"【{title}】")
        for item in items[:limit]:
            v = f"{item['views']:,}" if item['views'] else "?"
            lines.append(f"- {item['name']} — {item['channel']} — {v} 播放")
        lines.append("")

    section("Roblox 赛道", roblox, 6)
    section("独立游戏赛道", indie, 6)
    section("主机/PC 赛道", console, 4)
    section("直播相关", live, 3)

    # 猎奇发现：播放量 > 50K 但不在词库里
    weird = [v for v in videos if parse_views(v.get("view_text", "")) > 50_000 and not classify_game(v.get("title", ""), "", "")]
    if weird:
        weird.sort(key=lambda x: parse_views(x.get("view_text", "")), reverse=True)
        lines.append("【算法流量猎奇发现】（高播放量非主流内容）")
        for v in weird[:3]:
            lines.append(f"- {v['title']} — {v['channel_name']} — {v.get('view_text','?')} — 猎奇内容")
        lines.append("")

    lines.append("---")
    lines.append(f"数据来源：YouTube 订阅频道 | 共处理 {len(videos)} 条视频")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="从 YouTube 视频 JSON 中提取游戏关键词日报")
    parser.add_argument("input_json", help="fetch_subscriptions.sh 输出的 JSON 文件路径")
    parser.add_argument("--output", "-o", help="输出报告路径（默认输出到 stdout）")
    parser.add_argument("--max-candidates", type=int, default=12, help="每赛道最大条目数")
    args = parser.parse_args()

    input_path = Path(args.input_json)
    if not input_path.exists():
        print(f"ERROR: 文件不存在: {input_path}", file=sys.stderr)
        sys.exit(1)

    videos = json.loads(input_path.read_text(encoding="utf-8"))
    digest = build_digest(videos, max_candidates=args.max_candidates)

    if args.output:
        Path(args.output).write_text(digest, encoding="utf-8")
        print(f"[youtube-game-keywords] 报告已保存: {args.output}")
    else:
        print(digest)


if __name__ == "__main__":
    main()
