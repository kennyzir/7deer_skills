#!/usr/bin/env python3
"""Normalize user-supplied backlink candidates and captured contact evidence."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import re
import sys
from typing import Any, Sequence
from urllib.parse import urlsplit


EMAIL_PATTERN = re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.I)
ALLOWED_FIELDS = {"name", "source_url", "observed_at", "captured_text", "notes"}


class InputError(ValueError):
    """Raised when evidence cannot be normalized safely."""


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Extract observed contact addresses from user-supplied captured text. "
            "No network requests are made."
        )
    )
    parser.add_argument("--input", required=True, help="Candidate/evidence JSON file")
    parser.add_argument(
        "--output",
        help="Create a new JSON file instead of printing to stdout",
    )
    return parser.parse_args(argv)


def require_text(value: Any, field: str, maximum: int = 2000) -> str:
    if not isinstance(value, str) or not value.strip():
        raise InputError(f"{field} must be a non-empty string")
    normalized = value.strip()
    if len(normalized) > maximum:
        raise InputError(f"{field} is too long")
    if any(not character.isprintable() for character in normalized):
        raise InputError(f"{field} must be a single printable line")
    return normalized


def validate_source_url(value: Any) -> str:
    url = require_text(value, "source_url")
    parsed = urlsplit(url)
    if parsed.scheme not in {"http", "https"} or not parsed.hostname:
        raise InputError("source_url must be an absolute HTTP(S) URL")
    if parsed.username or parsed.password:
        raise InputError("source_url must not contain credentials")
    return url


def validate_observed_at(value: Any) -> str | None:
    if value is None:
        return None
    timestamp = require_text(value, "observed_at", 100)
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z", timestamp):
        raise InputError("observed_at must be a UTC ISO-8601 timestamp ending in Z")
    try:
        parsed = datetime.fromisoformat(timestamp.removesuffix("Z") + "+00:00")
    except ValueError as error:
        raise InputError("observed_at must be a valid UTC ISO-8601 timestamp") from error
    if parsed.utcoffset() != timezone.utc.utcoffset(parsed):
        raise InputError("observed_at must be UTC")
    return timestamp


def read_input(input_path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(input_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise InputError("input must be a readable UTF-8 JSON file") from error
    if not isinstance(payload, dict) or set(payload) != {"opportunities"}:
        raise InputError("input must contain only an opportunities array")
    if not isinstance(payload["opportunities"], list):
        raise InputError("opportunities must be an array")
    return payload


def normalize_opportunity(value: Any) -> dict[str, object]:
    if not isinstance(value, dict):
        raise InputError("each opportunity must be an object")
    unexpected = set(value) - ALLOWED_FIELDS
    if unexpected:
        raise InputError(f"opportunity contains unsupported fields: {sorted(unexpected)}")

    name = require_text(value.get("name"), "name", 300)
    source_url = validate_source_url(value.get("source_url"))
    observed_at = validate_observed_at(value.get("observed_at"))
    captured_text = value.get("captured_text")
    if captured_text is not None and not isinstance(captured_text, str):
        raise InputError("captured_text must be a string when provided")
    if captured_text and not observed_at:
        raise InputError("captured_text requires observed_at")
    notes = value.get("notes", "")
    if not isinstance(notes, str):
        raise InputError("notes must be a string")

    emails: list[str] = []
    seen: set[str] = set()
    for match in EMAIL_PATTERN.findall(captured_text or ""):
        normalized = match.lower()
        if normalized not in seen:
            seen.add(normalized)
            emails.append(match)

    status = "observed" if emails and observed_at else "unknown"
    if status == "unknown" and not notes.strip():
        notes = "No contact address was observed in the supplied evidence."
    return {
        "name": name,
        "source_url": source_url,
        "observed_at": observed_at,
        "status": status,
        "emails": emails if status == "observed" else [],
        "notes": notes.strip(),
    }


def build_result(payload: dict[str, Any]) -> dict[str, object]:
    contacts = [normalize_opportunity(item) for item in payload["opportunities"]]
    return {
        "generated_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace(
            "+00:00", "Z"
        ),
        "contacts": contacts,
    }


def resolve_output(raw_output: str | None) -> Path | None:
    if raw_output is None:
        return None
    if not raw_output.strip():
        raise InputError("output path must not be empty")
    output = Path(raw_output.strip()).expanduser().resolve(strict=False)
    if output.exists() or output.is_symlink():
        raise InputError("output path already exists; refusing to overwrite it")
    if not output.parent.is_dir():
        raise InputError("output parent directory does not exist")
    return output


def emit_result(result: dict[str, object], output: Path | None) -> None:
    content = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if output is None:
        sys.stdout.write(content)
        return
    with output.open("x", encoding="utf-8", newline="\n") as output_file:
        output_file.write(content)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        output = resolve_output(args.output)
        payload = read_input(Path(args.input).expanduser().resolve(strict=False))
        result = build_result(payload)
    except InputError as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 2
    try:
        emit_result(result, output)
    except OSError:
        print("ERROR: output could not be written", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
