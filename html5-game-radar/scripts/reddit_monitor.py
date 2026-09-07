#!/usr/bin/env python3
"""Run a configured Reddit CLI and extract HTML5/browser-game posts."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import re
import subprocess
import sys
from typing import Any, Sequence


REDDIT_SCRIPT_ENV = "HTML5_REDDIT_SCRIPT"


class ConfigurationError(ValueError):
    """Raised before any subprocess or output operation can begin."""


class RedditCliError(RuntimeError):
    """Raised when the configured Reddit CLI does not complete successfully."""


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Scan r/webgames with an explicitly configured reddit.ts CLI. "
            "JSON is printed to stdout unless --output is supplied."
        )
    )
    parser.add_argument(
        "--reddit-script",
        help=f"Path to reddit.ts (or set {REDDIT_SCRIPT_ENV})",
    )
    parser.add_argument(
        "--output",
        help="Create a new JSON output file; existing paths are never overwritten",
    )
    parser.add_argument("--timeout", type=float, default=30.0)
    return parser.parse_args(argv)


def resolve_reddit_script(cli_value: str | None) -> Path:
    configured = cli_value or os.environ.get(REDDIT_SCRIPT_ENV)
    if not configured or not configured.strip():
        raise ConfigurationError(
            f"Reddit CLI is not configured; pass --reddit-script or set {REDDIT_SCRIPT_ENV}"
        )
    script = Path(configured.strip()).expanduser().resolve(strict=False)
    if not script.is_file():
        raise ConfigurationError("configured Reddit CLI path is not an existing file")
    return script


def resolve_output(raw_output: str | None) -> Path | None:
    if raw_output is None:
        return None
    if not raw_output.strip():
        raise ConfigurationError("output path must not be empty")
    output = Path(raw_output.strip()).expanduser().resolve(strict=False)
    if output.exists() or output.is_symlink():
        raise ConfigurationError("output path already exists; refusing to overwrite it")
    if not output.parent.is_dir():
        raise ConfigurationError("output parent directory does not exist")
    return output


def run_reddit_cli(
    script: Path,
    arguments: Sequence[str],
    timeout: float,
    runner: Any = None,
) -> str:
    if runner is None:
        runner = subprocess.run
    command = ["npx", "--no-install", "tsx", str(script), *arguments]
    try:
        result = runner(
            command,
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=str(script.parent),
            check=False,
        )
    except subprocess.TimeoutExpired as error:
        raise RedditCliError("Reddit CLI timed out") from error
    except OSError as error:
        raise RedditCliError("Reddit CLI could not be started") from error
    if result.returncode != 0:
        raise RedditCliError(f"Reddit CLI failed with exit code {result.returncode}")
    return result.stdout


def extract_posts(raw_output: str) -> list[str]:
    """Extract post-shaped blocks from the Reddit CLI Markdown output."""
    posts: list[str] = []
    post_block: list[str] = []
    for line in raw_output.strip().splitlines():
        is_start = "⬆️" in line or "⬆" in line
        if is_start and post_block:
            posts.append("\n".join(post_block))
            post_block = []
        if is_start or post_block:
            post_block.append(line)
            if not line.strip():
                posts.append("\n".join(post_block))
                post_block = []
    if post_block:
        posts.append("\n".join(post_block))
    return posts


def parse_post(post_text: str) -> dict[str, object]:
    result: dict[str, object] = {
        "title": "",
        "upvotes": 0,
        "comments": 0,
        "author": "",
        "time": "",
        "url": "",
        "sub": "webgames",
        "raw": post_text,
    }
    lines = post_text.splitlines()
    for line in lines:
        upvotes_match = re.search(r"[⬆️⬆]\s*(\d+)", line)
        if upvotes_match:
            result["upvotes"] = int(upvotes_match.group(1))
        time_match = re.search(r"(\d+)\s*(hour|day|minute|week|month)", line, re.I)
        if time_match:
            result["time"] = f"{time_match.group(1)} {time_match.group(2)}"
        author_match = re.search(r"by\s+u/(\w+)", line, re.I)
        if author_match:
            result["author"] = author_match.group(1)
        url_match = re.search(r"https?://[^\s)]+", line)
        if url_match:
            result["url"] = url_match.group(0)

    first_line = lines[0] if lines else ""
    title = re.sub(r"^[⬆️⬆]\s*\d+\s*", "", first_line).strip()
    result["title"] = re.sub(r"\s*\|\s*r/\w+\s*\|\s*by.*$", "", title).strip()
    return result


def filter_html5_related(post: dict[str, object]) -> bool:
    title = post.get("title")
    if not isinstance(title, str) or not title:
        return False
    keywords = (
        "html5", "html 5", "browser game", "web game", "itch.io",
        "no download", "play in browser", "free to play", "online game",
        "unblocked", "io game", ".io", "crazy games", "miniclip",
        "kongregate", "armor games", "gamepix", "new game",
        "just released", "first look",
    )
    title_lower = title.lower()
    return any(keyword in title_lower for keyword in keywords)


def collect_posts(script: Path, timeout: float) -> list[dict[str, object]]:
    raw_outputs = (
        run_reddit_cli(script, ["hot", "webgames", "--limit", "50"], timeout),
        run_reddit_cli(script, ["new", "webgames", "--limit", "30"], timeout),
    )
    unique: dict[str, dict[str, object]] = {}
    for raw_output in raw_outputs:
        for post_text in extract_posts(raw_output):
            post = parse_post(post_text)
            title = post["title"]
            if isinstance(title, str) and filter_html5_related(post):
                unique.setdefault(title, post)
    return sorted(unique.values(), key=lambda post: int(post["upvotes"]), reverse=True)


def emit_json(posts: list[dict[str, object]], output: Path | None) -> None:
    payload = json.dumps(posts, ensure_ascii=False, indent=2) + "\n"
    if output is None:
        sys.stdout.write(payload)
        return
    with output.open("x", encoding="utf-8", newline="\n") as output_file:
        output_file.write(payload)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        if args.timeout <= 0:
            raise ConfigurationError("timeout must be greater than zero")
        script = resolve_reddit_script(args.reddit_script)
        output = resolve_output(args.output)
    except ConfigurationError as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 2

    try:
        posts = collect_posts(script, args.timeout)
        emit_json(posts, output)
    except RedditCliError as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1
    except OSError:
        print("ERROR: output could not be written", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
