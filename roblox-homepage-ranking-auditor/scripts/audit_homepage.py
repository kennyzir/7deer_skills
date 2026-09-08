#!/usr/bin/env python3
"""Collect deterministic HTML evidence for the RB Auto Golden Homepage audit.

This script intentionally does not produce the final semantic 100-point score.
It extracts reproducible evidence that Codex must review under SKILL.md.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup, Tag

USER_AGENT = (
    "Mozilla/5.0 (compatible; RB-Auto-Golden-Homepage-Auditor/1.0; "
    "+https://github.com/kennyzir/7deer_skills)"
)

GENERIC_ANCHORS = {
    "read more",
    "learn more",
    "view more",
    "view",
    "click here",
    "details",
    "more",
    "open",
    "go",
    "see more",
    "explore",
}

STOPWORDS = {
    "the", "a", "an", "and", "or", "but", "to", "of", "in", "on", "for", "with",
    "from", "by", "at", "as", "is", "are", "was", "were", "be", "been", "being",
    "this", "that", "these", "those", "it", "its", "you", "your", "we", "our", "they",
    "their", "can", "will", "may", "should", "how", "what", "when", "where", "why",
    "roblox", "game", "games", "guide", "wiki", "best", "latest", "more", "all",
}

NO_ACTIVE_CODES_PATTERNS = [
    r"no\s+(?:currently\s+)?active\s+codes",
    r"no\s+(?:working|valid|available)\s+codes",
    r"there\s+are\s+no\s+active\s+codes",
    r"none\s+(?:are\s+)?active",
    r"0\s+active\s+codes",
]

TOOL_WORDS = {
    "calculator", "planner", "builder", "comparator", "selector", "analyzer", "simulator",
    "checker", "optimizer", "estimator", "database", "filter", "search",
}

QUERY_HEADING_PATTERNS = {
    "codes": re.compile(r"\b(codes?|promo\s+codes?|redeem)\b", re.I),
    "tier_list": re.compile(r"\btier\s*list\b|\brankings?\b", re.I),
    "builds": re.compile(r"\bbuilds?\b|\bstats?\s+build\b", re.I),
    "progression": re.compile(r"\bprogression\b|\bbeginner\b|\bfirst\s+(?:hour|30\s*minutes?)\b", re.I),
    "updates": re.compile(r"\bupdates?\b|\bpatch\s+notes?\b", re.I),
    "controls": re.compile(r"\bcontrols?\b|\bkeybinds?\b", re.I),
    "map": re.compile(r"\bmaps?\b|\blocations?\b", re.I),
}

MEANINGFUL_TAGS = {"p", "li", "td", "th", "code", "label", "button", "figcaption", "dt", "dd"}
HEADING_TAGS = {"h1", "h2", "h3"}


@dataclass
class PageInput:
    source: str
    source_type: str
    requested_url: str | None
    final_url: str | None
    status_code: int | None
    html: str


def normalize_space(value: str) -> str:
    return re.sub(r"\s+", " ", value or "").strip()


def normalize_token(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", value.lower()).strip()


def load_url(url: str, timeout: float) -> PageInput:
    response = requests.get(
        url,
        timeout=timeout,
        headers={"User-Agent": USER_AGENT, "Accept": "text/html,application/xhtml+xml"},
        allow_redirects=True,
    )
    response.raise_for_status()
    return PageInput(
        source=url,
        source_type="url",
        requested_url=url,
        final_url=response.url,
        status_code=response.status_code,
        html=response.text,
    )


def load_file(path: str) -> PageInput:
    file_path = Path(path).expanduser().resolve()
    if not file_path.is_file():
        raise FileNotFoundError(f"HTML file not found: {file_path}")
    return PageInput(
        source=str(file_path),
        source_type="html_file",
        requested_url=None,
        final_url=None,
        status_code=None,
        html=file_path.read_text(encoding="utf-8", errors="replace"),
    )


def soup_for(html: str) -> BeautifulSoup:
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup(["script", "style", "noscript", "template", "svg"]):
        tag.decompose()
    return soup


def visible_text(soup: BeautifulSoup) -> str:
    root = soup.find("main") or soup.find("body") or soup
    return normalize_space(root.get_text(" ", strip=True))


def extract_metadata(soup: BeautifulSoup) -> dict[str, Any]:
    title = normalize_space(soup.title.get_text(" ", strip=True)) if soup.title else ""
    description_tag = soup.find("meta", attrs={"name": re.compile(r"^description$", re.I)})
    robots_tags = soup.find_all("meta", attrs={"name": re.compile(r"^(robots|googlebot)$", re.I)})
    canonical_tag = soup.find("link", attrs={"rel": lambda value: value and "canonical" in value})
    robots_values = [normalize_space(tag.get("content", "")) for tag in robots_tags]
    return {
        "title": title,
        "meta_description": normalize_space(description_tag.get("content", "")) if description_tag else "",
        "canonical": normalize_space(canonical_tag.get("href", "")) if canonical_tag else "",
        "robots": robots_values,
        "noindex": any("noindex" in value.lower() for value in robots_values),
    }


def extract_headings(soup: BeautifulSoup) -> list[dict[str, Any]]:
    headings: list[dict[str, Any]] = []
    for idx, tag in enumerate(soup.find_all(list(HEADING_TAGS))):
        text = normalize_space(tag.get_text(" ", strip=True))
        if not text:
            continue
        headings.append(
            {
                "index": idx,
                "level": int(tag.name[1]),
                "text": text,
                "id": tag.get("id"),
            }
        )
    return headings


def extract_sections(soup: BeautifulSoup) -> list[dict[str, Any]]:
    root = soup.find("main") or soup.find("body") or soup
    sections: list[dict[str, Any]] = []
    current: dict[str, Any] = {
        "heading": "[pre-heading content]",
        "level": 0,
        "id": None,
        "parts": [],
    }

    for tag in root.find_all(list(HEADING_TAGS | MEANINGFUL_TAGS)):
        if not isinstance(tag, Tag):
            continue
        if tag.name in HEADING_TAGS:
            if current["parts"] or current["heading"] != "[pre-heading content]":
                sections.append(current)
            current = {
                "heading": normalize_space(tag.get_text(" ", strip=True)),
                "level": int(tag.name[1]),
                "id": tag.get("id"),
                "parts": [],
            }
            continue

        # Avoid counting nested tags twice, e.g. a <code> inside an <li>.
        if any(parent.name in MEANINGFUL_TAGS for parent in tag.parents if isinstance(parent, Tag)):
            continue
        text = normalize_space(tag.get_text(" ", strip=True))
        if text:
            current["parts"].append(text)

    if current["parts"] or current["heading"] != "[pre-heading content]":
        sections.append(current)

    result: list[dict[str, Any]] = []
    for index, section in enumerate(sections):
        text = normalize_space(" ".join(section["parts"]))
        result.append(
            {
                "index": index,
                "heading": section["heading"],
                "level": section["level"],
                "id": section["id"],
                "text": text,
                "word_count": len(re.findall(r"\b\w+\b", text)),
            }
        )
    return result


def heading_skips(headings: list[dict[str, Any]]) -> list[dict[str, Any]]:
    skips: list[dict[str, Any]] = []
    for previous, current in zip(headings, headings[1:]):
        if current["level"] - previous["level"] > 1:
            skips.append({"from": previous, "to": current})
    return skips


def internal_link(href: str, base_url: str | None) -> tuple[bool, str]:
    if not href or href.startswith(("#", "mailto:", "tel:", "javascript:")):
        return False, href
    if base_url:
        absolute = urljoin(base_url, href)
        return urlparse(absolute).netloc == urlparse(base_url).netloc, absolute
    parsed = urlparse(href)
    return not parsed.netloc, href


def extract_links(soup: BeautifulSoup, base_url: str | None) -> dict[str, Any]:
    links: list[dict[str, Any]] = []
    for tag in soup.find_all("a"):
        href = normalize_space(tag.get("href", ""))
        anchor = normalize_space(tag.get_text(" ", strip=True))
        is_internal, normalized_href = internal_link(href, base_url)
        if not href:
            continue
        links.append(
            {
                "anchor": anchor,
                "href": href,
                "normalized_href": normalized_href,
                "internal": is_internal,
                "generic_anchor": normalize_token(anchor) in GENERIC_ANCHORS,
                "inside_main": tag.find_parent("main") is not None,
                "inside_nav": tag.find_parent("nav") is not None,
                "inside_footer": tag.find_parent("footer") is not None,
            }
        )

    internal = [item for item in links if item["internal"]]
    main_internal = [item for item in internal if item["inside_main"]]
    generic = [item for item in main_internal if item["generic_anchor"]]
    return {
        "all": links,
        "internal_count": len(internal),
        "main_internal_count": len(main_internal),
        "main_generic_anchor_count": len(generic),
        "main_generic_anchor_ratio": round(len(generic) / len(main_internal), 4) if main_internal else None,
    }


def extract_tool_signature(soup: BeautifulSoup) -> dict[str, Any]:
    root = soup.find("main") or soup.find("body") or soup
    fields: list[str] = []
    for tag in root.find_all(["input", "select", "textarea"]):
        label = ""
        if tag.get("id"):
            label_tag = root.find("label", attrs={"for": tag.get("id")})
            if label_tag:
                label = normalize_space(label_tag.get_text(" ", strip=True))
        signature = "|".join(
            filter(
                None,
                [
                    tag.name,
                    normalize_token(tag.get("type", "")),
                    normalize_token(tag.get("name", "")),
                    normalize_token(tag.get("id", "")),
                    normalize_token(tag.get("placeholder", "")),
                    normalize_token(label),
                ],
            )
        )
        if signature:
            fields.append(signature)

    buttons = [
        normalize_token(tag.get_text(" ", strip=True))
        for tag in root.find_all("button")
        if normalize_space(tag.get_text(" ", strip=True))
    ]
    tool_headings = [
        normalize_space(tag.get_text(" ", strip=True))
        for tag in root.find_all(list(HEADING_TAGS))
        if any(word in normalize_token(tag.get_text(" ", strip=True)).split() for word in TOOL_WORDS)
    ]
    return {
        "field_count": len(fields),
        "fields": sorted(set(fields)),
        "buttons": sorted(set(buttons)),
        "tool_headings": tool_headings,
        "has_interactive_signal": bool(fields and buttons),
    }


def section_for_pattern(sections: list[dict[str, Any]], pattern: re.Pattern[str]) -> list[dict[str, Any]]:
    return [section for section in sections if pattern.search(section["heading"])]


def code_tokens(soup: BeautifulSoup) -> list[str]:
    tokens: list[str] = []
    for tag in soup.find_all("code"):
        value = normalize_space(tag.get_text(" ", strip=True))
        if 2 <= len(value) <= 80:
            tokens.append(value)
    for tag in soup.find_all(attrs={"data-code": True}):
        value = normalize_space(tag.get("data-code", ""))
        if value:
            tokens.append(value)
    return sorted(set(tokens))


def has_no_active_codes_statement(text: str) -> bool:
    return any(re.search(pattern, text, re.I) for pattern in NO_ACTIVE_CODES_PATTERNS)


def probable_named_tier_items(section_text: str) -> int:
    # A deliberately conservative hint, not a semantic verdict.
    chunks = re.split(r"[\n|•·;]+", section_text)
    candidates: set[str] = set()
    generic = {
        "s tier", "a tier", "b tier", "c tier", "d tier", "best", "strong", "weak",
        "common", "rare", "epic", "legendary", "mythical", "starter", "standard",
    }
    for chunk in chunks:
        value = normalize_space(chunk)
        if not (2 <= len(value.split()) <= 12):
            continue
        normalized = normalize_token(value)
        if not normalized or normalized in generic:
            continue
        if re.search(r"\b[A-Z][A-Za-z0-9'_-]{2,}(?:\s+[A-Z][A-Za-z0-9'_-]{2,})*\b", value):
            candidates.add(value)
    return len(candidates)


def tokenize_for_similarity(text: str, game_name: str | None) -> set[str]:
    game_tokens = set(normalize_token(game_name or "").split())
    tokens = re.findall(r"[a-z0-9]{2,}", text.lower())
    return {
        token
        for token in tokens
        if token not in STOPWORDS and token not in game_tokens and not token.isdigit()
    }


def jaccard(left: set[str], right: set[str]) -> float:
    if not left or not right:
        return 0.0
    return len(left & right) / len(left | right)


def section_similarities(
    home_sections: list[dict[str, Any]],
    child_sections: list[dict[str, Any]],
    game_name: str | None,
    threshold: float = 0.35,
) -> list[dict[str, Any]]:
    matches: list[dict[str, Any]] = []
    for home in home_sections:
        home_tokens = tokenize_for_similarity(home["text"], game_name)
        if len(home_tokens) < 25:
            continue
        for child in child_sections:
            child_tokens = tokenize_for_similarity(child["text"], game_name)
            if len(child_tokens) < 25:
                continue
            score = jaccard(home_tokens, child_tokens)
            if score >= threshold:
                matches.append(
                    {
                        "home_heading": home["heading"],
                        "child_heading": child["heading"],
                        "similarity": round(score, 4),
                        "home_token_count": len(home_tokens),
                        "child_token_count": len(child_tokens),
                    }
                )
    return sorted(matches, key=lambda item: item["similarity"], reverse=True)


def tool_similarity(home: dict[str, Any], child: dict[str, Any]) -> float:
    home_set = set(home["fields"] + home["buttons"])
    child_set = set(child["fields"] + child["buttons"])
    return round(jaccard(home_set, child_set), 4)


def analyze_page(page: PageInput, game_name: str | None) -> dict[str, Any]:
    soup = soup_for(page.html)
    metadata = extract_metadata(soup)
    headings = extract_headings(soup)
    sections = extract_sections(soup)
    base_url = page.final_url or page.requested_url
    links = extract_links(soup, base_url)
    tools = extract_tool_signature(soup)
    codes = code_tokens(soup)

    query_sections: dict[str, Any] = {}
    for key, pattern in QUERY_HEADING_PATTERNS.items():
        matches = section_for_pattern(sections, pattern)
        query_sections[key] = [
            {
                "heading": item["heading"],
                "word_count": item["word_count"],
                "text_preview": item["text"][:500],
            }
            for item in matches
        ]

    codes_text = " ".join(item["text"] for item in section_for_pattern(sections, QUERY_HEADING_PATTERNS["codes"]))
    tier_matches = section_for_pattern(sections, QUERY_HEADING_PATTERNS["tier_list"])
    tier_text = " ".join(item["text"] for item in tier_matches)

    visible = visible_text(soup)
    game_name_present = None
    if game_name:
        game_name_present = normalize_token(game_name) in normalize_token(visible)

    warnings: list[dict[str, Any]] = []
    h1_count = sum(1 for item in headings if item["level"] == 1)
    if h1_count == 0:
        warnings.append({"code": "NO_H1", "message": "No rendered H1 found."})
    elif h1_count > 1:
        warnings.append({"code": "MULTIPLE_H1", "message": f"Found {h1_count} rendered H1 elements."})

    if metadata["noindex"]:
        warnings.append({"code": "NOINDEX", "message": "Robots metadata contains noindex."})

    if query_sections["codes"] and not codes and not has_no_active_codes_statement(codes_text):
        warnings.append(
            {
                "code": "EMPTY_CODES_PROMISE_HINT",
                "message": "Codes-labelled section found without <code>/data-code tokens or an explicit no-active-codes statement.",
            }
        )

    tier_named_items = probable_named_tier_items(tier_text)
    if tier_matches and tier_named_items < 3:
        warnings.append(
            {
                "code": "LOW_TIER_ITEM_COUNT_HINT",
                "message": "Tier-list section appears to contain fewer than three probable named rankable items; semantic review required.",
                "probable_named_items": tier_named_items,
            }
        )

    if links["main_generic_anchor_ratio"] is not None and links["main_generic_anchor_ratio"] > 0.4:
        warnings.append(
            {
                "code": "HIGH_GENERIC_ANCHOR_RATIO",
                "message": "More than 40% of main-content internal anchors are generic.",
                "ratio": links["main_generic_anchor_ratio"],
            }
        )

    skips = heading_skips(headings)
    if skips:
        warnings.append(
            {
                "code": "HEADING_LEVEL_SKIP",
                "message": "Heading hierarchy skips one or more levels.",
                "count": len(skips),
            }
        )

    if game_name and not game_name_present:
        warnings.append(
            {
                "code": "GAME_NAME_NOT_FOUND",
                "message": "Configured game name was not found in rendered main content.",
            }
        )

    return {
        "source": asdict(page) | {"html": None},
        "metadata": metadata,
        "visible_word_count": len(re.findall(r"\b\w+\b", visible)),
        "game_name_present": game_name_present,
        "headings": headings,
        "heading_skips": skips,
        "sections": sections,
        "query_sections": query_sections,
        "code_tokens": codes,
        "tier_probable_named_item_count": tier_named_items,
        "links": links,
        "tool_signature": tools,
        "warnings": warnings,
    }


def load_pages(values: Iterable[str], loader: Any) -> list[PageInput]:
    pages: list[PageInput] = []
    for value in values:
        pages.append(loader(value))
    return pages


def build_report(args: argparse.Namespace) -> dict[str, Any]:
    if bool(args.url) == bool(args.html):
        raise ValueError("Provide exactly one of --url or --html for the homepage.")

    home_input = load_url(args.url, args.timeout) if args.url else load_file(args.html)
    home = analyze_page(home_input, args.game_name)

    child_inputs: list[PageInput] = []
    for url in args.child_url:
        child_inputs.append(load_url(url, args.timeout))
    for path in args.child_html:
        child_inputs.append(load_file(path))

    children: list[dict[str, Any]] = []
    duplicate_hints: list[dict[str, Any]] = []

    for child_input in child_inputs:
        child = analyze_page(child_input, args.game_name)
        similarities = section_similarities(home["sections"], child["sections"], args.game_name)
        tools_score = tool_similarity(home["tool_signature"], child["tool_signature"])
        child_record = {
            "source": child["source"],
            "metadata": child["metadata"],
            "headings": child["headings"],
            "query_sections": child["query_sections"],
            "tool_signature": child["tool_signature"],
            "section_similarities": similarities[:25],
            "tool_signature_similarity": tools_score,
            "warnings": child["warnings"],
        }
        children.append(child_record)

        for match in similarities:
            if match["similarity"] >= 0.50:
                duplicate_hints.append(
                    {
                        "code": "FULL_CHILD_DUPLICATION_HINT",
                        "child": child["source"]["source"],
                        **match,
                    }
                )
        if (
            home["tool_signature"]["has_interactive_signal"]
            and child["tool_signature"]["has_interactive_signal"]
            and tools_score >= 0.70
        ):
            duplicate_hints.append(
                {
                    "code": "DUPLICATE_FULL_TOOL_HINT",
                    "child": child["source"]["source"],
                    "tool_signature_similarity": tools_score,
                }
            )

    top_section_words = Counter(
        {section["heading"]: section["word_count"] for section in home["sections"]}
    ).most_common(10)

    return {
        "schema_version": "1.0",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "tool": "rb-auto-golden-homepage-machine-evidence",
        "game_name": args.game_name,
        "homepage": home,
        "children": children,
        "duplicate_hints": duplicate_hints,
        "summary": {
            "homepage_warning_count": len(home["warnings"]),
            "child_count": len(children),
            "duplicate_hint_count": len(duplicate_hints),
            "top_sections_by_word_count": [
                {"heading": heading, "word_count": count} for heading, count in top_section_words
            ],
            "semantic_audit_required": True,
        },
        "limitations": [
            "The scanner does not determine the primary player job or final structural score.",
            "Named tier-item detection and duplication checks are conservative heuristics.",
            "Runtime behavior, mobile usability, factual accuracy, and intent ownership require Codex review.",
        ],
    }


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--url", help="Live homepage URL.")
    parser.add_argument("--html", help="Path to exported homepage HTML.")
    parser.add_argument("--game-name", help="Expected game name for evidence checks.")
    parser.add_argument("--child-url", action="append", default=[], help="Child URL; repeat as needed.")
    parser.add_argument("--child-html", action="append", default=[], help="Child HTML path; repeat as needed.")
    parser.add_argument("--timeout", type=float, default=20.0, help="HTTP timeout in seconds.")
    parser.add_argument("--output", required=True, help="JSON output path.")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        report = build_report(args)
        output = Path(args.output).expanduser().resolve()
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"Wrote machine evidence: {output}")
        print(json.dumps(report["summary"], ensure_ascii=False, indent=2))
        return 0
    except (ValueError, FileNotFoundError, requests.RequestException) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
