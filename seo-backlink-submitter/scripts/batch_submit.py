#!/usr/bin/env python3
"""Prepare or explicitly submit one target to a list of directories."""

from __future__ import annotations

import argparse
import asyncio
import json
import sys
from pathlib import Path
from typing import Any, Sequence

from submit_to_directory import InputError, load_target, submit_live, validate_http_url


def load_directories(path: Path) -> list[str]:
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except OSError as exc:
        raise InputError(f"cannot read directories file '{path}': {exc}") from exc

    directories: list[str] = []
    seen: set[str] = set()
    for line_number, line in enumerate(lines, 1):
        value = line.strip()
        if not value or value.startswith("#"):
            continue
        try:
            validate_http_url(value, f"directory URL on line {line_number}")
        except InputError as exc:
            raise InputError(f"invalid directories file '{path}': {exc}") from exc
        if value not in seen:
            seen.add(value)
            directories.append(value)

    if not directories:
        raise InputError(f"directories file '{path}' contains no submission URLs")
    return directories


async def submit_batch(
    directories: Sequence[str], target: dict[str, Any]
) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    for directory in directories:
        try:
            results.append(await submit_live(directory, target))
        except Exception as exc:
            results.append(
                {
                    "mode": "submit",
                    "status": "error",
                    "directory": directory,
                    "site": target["url"],
                    "error": str(exc),
                }
            )
    return results


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Prepare batch directory submissions; defaults to a network-free dry run."
    )
    parser.add_argument("--target", required=True, type=Path, help="Target JSON file")
    parser.add_argument(
        "--directories", required=True, type=Path, help="Text file containing one URL per line"
    )
    parser.add_argument(
        "--submit",
        action="store_true",
        help="Explicitly allow browser navigation, form filling, and submit-button clicking",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        target = load_target(args.target)
        directories = load_directories(args.directories)
    except InputError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    if not args.submit:
        print(
            json.dumps(
                {
                    "mode": "batch-dry-run",
                    "status": "not_submitted",
                    "site": target["url"],
                    "target_name": target["name"],
                    "directory_count": len(directories),
                    "directories": directories,
                    "next_step": "Review this plan, then rerun with --submit to allow real submissions.",
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        return 0

    results = asyncio.run(submit_batch(directories, target))
    failed = sum(result["status"] == "error" for result in results)
    print(
        json.dumps(
            {
                "mode": "batch-submit",
                "status": "completed_with_errors" if failed else "submit_triggered",
                "site": target["url"],
                "results": results,
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
