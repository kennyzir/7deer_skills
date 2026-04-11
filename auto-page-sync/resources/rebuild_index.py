#!/usr/bin/env python3
"""
rebuild_index.py — 通用报告/博客索引重建脚本

用法:
  python rebuild_index.py --dir public/data/reports
  python rebuild_index.py --dir public/data/reports --types report_types.json

功能:
  扫描指定目录下的日期文件夹，为每个 .md 文件生成元数据，
  输出 index.json 供前端页面消费。
"""

import json
import os
import argparse
import re
from pathlib import Path


DEFAULT_REPORT_TYPES = {}


def extract_title_from_md(filepath: str) -> str:
    """从 Markdown 文件的第一个 # 标题提取标题"""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line.startswith("# "):
                    title = line.lstrip("# ").strip()
                    if "|" in title:
                        title = title.split("|")[0].strip()
                    return title
    except Exception:
        pass
    return ""


def slug_from_filename(filename: str) -> str:
    return filename.replace(".md", "")


def build_index(reports_dir: str, report_types: dict) -> dict:
    reports_path = Path(reports_dir)
    if not reports_path.exists():
        return {"dates": [], "latest": "", "items": {}}

    date_pattern = re.compile(r"^\d{4}-\d{2}-\d{2}$")
    dates = sorted(
        [d.name for d in reports_path.iterdir()
         if d.is_dir() and date_pattern.match(d.name)],
        reverse=True
    )

    items = {}
    for date in dates:
        date_path = reports_path / date
        date_items = []
        for fname in sorted(os.listdir(date_path)):
            if not fname.endswith(".md"):
                continue
            filepath = date_path / fname
            if fname in report_types:
                meta = report_types[fname].copy()
            else:
                title = extract_title_from_md(str(filepath))
                meta = {
                    "slug": slug_from_filename(fname),
                    "title": title or slug_from_filename(fname).replace("-", " ").title(),
                    "icon": "📄",
                }
            meta["filename"] = fname
            date_items.append(meta)
        if date_items:
            items[date] = date_items

    valid_dates = sorted(items.keys(), reverse=True)
    return {
        "dates": valid_dates,
        "latest": valid_dates[0] if valid_dates else "",
        "items": items,
    }


def main():
    parser = argparse.ArgumentParser(description="Rebuild reports index.json")
    parser.add_argument("--dir", required=True, help="Path to reports directory")
    parser.add_argument("--types", default=None, help="Path to report_types.json (optional)")
    parser.add_argument("--output", default=None, help="Output path (default: {dir}/index.json)")
    args = parser.parse_args()

    report_types = DEFAULT_REPORT_TYPES
    if args.types and os.path.exists(args.types):
        with open(args.types, "r", encoding="utf-8") as f:
            report_types = json.load(f)

    index = build_index(args.dir, report_types)

    output_path = args.output or os.path.join(args.dir, "index.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(index, f, ensure_ascii=False, indent=2)

    print(f"Index rebuilt: {len(index['dates'])} dates, latest={index['latest']}")


if __name__ == "__main__":
    main()
