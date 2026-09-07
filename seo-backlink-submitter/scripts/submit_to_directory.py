#!/usr/bin/env python3
"""Safely prepare or explicitly submit one site to one directory form."""

from __future__ import annotations

import argparse
import asyncio
import json
import re
import sys
from pathlib import Path
from typing import Any, Sequence
from urllib.parse import urlsplit


REQUIRED_FIELDS = ("name", "url", "description", "email")
EMAIL_RE = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")
FIELD_SELECTORS = {
    "name": (
        'input[name*="name" i]',
        'input[id*="name" i]',
        'input[placeholder*="name" i]',
    ),
    "url": (
        'input[name*="url" i]',
        'input[name*="website" i]',
        'input[name*="link" i]',
        'input[type="url"]',
    ),
    "description": (
        'textarea[name*="desc" i]',
        'textarea[id*="desc" i]',
        'textarea[placeholder*="desc" i]',
        'input[name*="description" i]',
    ),
    "email": (
        'input[type="email"]',
        'input[name*="email" i]',
        'input[id*="email" i]',
    ),
    "category": (
        'input[name*="category" i]',
    ),
}
SUBMIT_SELECTORS = (
    'button[type="submit"]',
    'input[type="submit"]',
    'button:has-text("Submit")',
)


class InputError(ValueError):
    """Raised when user-provided target data is unsafe or incomplete."""


def validate_http_url(value: str, label: str) -> str:
    parsed = urlsplit(value)
    if parsed.scheme not in {"http", "https"} or not parsed.hostname:
        raise InputError(f"{label} must be an absolute http:// or https:// URL")
    if parsed.username or parsed.password:
        raise InputError(f"{label} must not contain embedded credentials")
    return value


def load_target(path: Path) -> dict[str, Any]:
    try:
        raw = path.read_text(encoding="utf-8")
    except OSError as exc:
        raise InputError(f"cannot read target file '{path}': {exc}") from exc

    try:
        target = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise InputError(f"target file '{path}' is not valid JSON: {exc.msg}") from exc

    if not isinstance(target, dict):
        raise InputError("target JSON must be an object")

    for field in REQUIRED_FIELDS:
        value = target.get(field)
        if not isinstance(value, str) or not value.strip():
            raise InputError(f"target field '{field}' must be a non-empty string")
        target[field] = value.strip()

    validate_http_url(target["url"], "target url")
    if not EMAIL_RE.fullmatch(target["email"]):
        raise InputError("target field 'email' must be a valid email address")

    category = target.get("category")
    if category is not None and (not isinstance(category, str) or not category.strip()):
        raise InputError("optional target field 'category' must be a non-empty string")
    if isinstance(category, str):
        target["category"] = category.strip()

    tags = target.get("tags")
    if tags is not None and (
        not isinstance(tags, list)
        or not all(isinstance(tag, str) and tag.strip() for tag in tags)
    ):
        raise InputError("optional target field 'tags' must be a list of non-empty strings")

    return target


async def fill_first_visible(page: Any, selectors: Sequence[str], value: str) -> bool:
    for selector in selectors:
        element = await page.query_selector(selector)
        if element is not None and await element.is_visible():
            await element.fill(value)
            return True
    return False


async def submit_live(directory_url: str, target: dict[str, Any]) -> dict[str, Any]:
    try:
        from playwright.async_api import async_playwright
    except ImportError as exc:
        raise RuntimeError(
            "live submission requires Playwright; install it with "
            "'python3 -m pip install playwright' and 'playwright install chromium'"
        ) from exc

    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch(headless=True)
        try:
            page = await browser.new_page()
            await page.goto(directory_url, timeout=30_000, wait_until="domcontentloaded")

            filled_fields: list[str] = []
            for field, selectors in FIELD_SELECTORS.items():
                value = target.get(field)
                if isinstance(value, str) and await fill_first_visible(page, selectors, value):
                    filled_fields.append(field)

            if not filled_fields:
                raise RuntimeError("no supported visible form fields were found")

            for selector in SUBMIT_SELECTORS:
                button = await page.query_selector(selector)
                if button is not None and await button.is_visible():
                    await button.click()
                    await page.wait_for_timeout(1_500)
                    return {
                        "mode": "submit",
                        "status": "submit_triggered",
                        "directory": directory_url,
                        "site": target["url"],
                        "filled_fields": filled_fields,
                    }

            raise RuntimeError("no visible submit control was found; nothing was submitted")
        finally:
            await browser.close()


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Prepare one directory submission; defaults to a network-free dry run."
    )
    parser.add_argument("--directory", required=True, help="Directory submission form URL")
    parser.add_argument("--target", required=True, type=Path, help="Target JSON file")
    parser.add_argument(
        "--submit",
        action="store_true",
        help="Explicitly allow browser navigation, form filling, and submit-button clicking",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        directory_url = validate_http_url(args.directory, "directory url")
        target = load_target(args.target)
    except InputError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    if not args.submit:
        print(
            json.dumps(
                {
                    "mode": "dry-run",
                    "status": "not_submitted",
                    "directory": directory_url,
                    "site": target["url"],
                    "target_name": target["name"],
                    "available_fields": sorted(target),
                    "next_step": "Review this plan, then rerun with --submit to allow a real submission.",
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        return 0

    try:
        result = asyncio.run(submit_live(directory_url, target))
    except Exception as exc:
        print(f"ERROR: live submission failed: {exc}", file=sys.stderr)
        return 1

    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
