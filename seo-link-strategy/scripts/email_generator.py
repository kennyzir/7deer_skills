#!/usr/bin/env python3
"""Generate local outreach drafts from user-provided, observed contact data."""

from __future__ import annotations

import argparse
from datetime import datetime, timedelta, timezone
import json
from pathlib import Path
import re
import sys
from typing import Any, Sequence
from urllib.parse import urlsplit


EMAIL_PATTERN = re.compile(r"^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}$", re.I)
ROOT_FIELDS = {"product", "sender", "contacts"}
PRODUCT_FIELDS = {"name", "url", "tagline", "selling_points"}
SENDER_FIELDS = {"name", "email"}
CONTACT_FIELDS = {
    "name",
    "email",
    "source_url",
    "observed_at",
    "status",
    "context",
}
MAX_CLOCK_SKEW = timedelta(minutes=5)


class InputError(ValueError):
    """Raised before any draft output is written."""


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Generate JSON outreach drafts from a user-provided input file. "
            "This command never sends messages."
        )
    )
    parser.add_argument("--input", required=True, help="Product/contact JSON file")
    parser.add_argument(
        "--output",
        help="Create a new JSON file instead of printing drafts to stdout",
    )
    return parser.parse_args(argv)


def require_text(value: Any, field: str, maximum: int = 4000) -> str:
    if not isinstance(value, str) or not value.strip():
        raise InputError(f"{field} must be a non-empty string")
    normalized = value.strip()
    if len(normalized) > maximum:
        raise InputError(f"{field} is too long")
    return normalized


def validate_url(value: Any, field: str) -> str:
    url = require_text(value, field, 2000)
    parsed = urlsplit(url)
    if parsed.scheme not in {"http", "https"} or not parsed.hostname:
        raise InputError(f"{field} must be an absolute HTTP(S) URL")
    if parsed.username or parsed.password:
        raise InputError(f"{field} must not contain credentials")
    return url


def validate_email(value: Any, field: str) -> str:
    email = require_text(value, field, 320)
    if not EMAIL_PATTERN.fullmatch(email):
        raise InputError(f"{field} must be a valid email address")
    return email


def validate_observed_at(value: Any) -> str:
    timestamp = require_text(value, "contact.observed_at", 100)
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z", timestamp):
        raise InputError("contact.observed_at must be a UTC ISO-8601 timestamp")
    try:
        observed_at = datetime.fromisoformat(timestamp.removesuffix("Z") + "+00:00")
    except ValueError as error:
        raise InputError("contact.observed_at must be a valid UTC time") from error
    if observed_at > datetime.now(timezone.utc) + MAX_CLOCK_SKEW:
        raise InputError("contact.observed_at must not be in the future")
    return timestamp


def require_object(value: Any, field: str, allowed: set[str]) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise InputError(f"{field} must be an object")
    unexpected = set(value) - allowed
    if unexpected:
        raise InputError(f"{field} contains unsupported fields: {sorted(unexpected)}")
    return value


def read_input(input_path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(input_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise InputError("input must be a readable UTF-8 JSON file") from error
    if not isinstance(payload, dict) or set(payload) != ROOT_FIELDS:
        raise InputError("input must contain exactly product, sender, and contacts")
    return payload


def validate_product(value: Any) -> dict[str, object]:
    product = require_object(value, "product", PRODUCT_FIELDS)
    if set(product) != PRODUCT_FIELDS:
        raise InputError("product requires name, url, tagline, and selling_points")
    selling_points = product["selling_points"]
    if not isinstance(selling_points, list) or not selling_points:
        raise InputError("product.selling_points must be a non-empty array")
    normalized_points = [
        require_text(point, "product.selling_points item", 1000) for point in selling_points
    ]
    return {
        "name": require_text(product["name"], "product.name", 300),
        "url": validate_url(product["url"], "product.url"),
        "tagline": require_text(product["tagline"], "product.tagline", 1000),
        "selling_points": normalized_points,
    }


def validate_sender(value: Any) -> dict[str, str]:
    sender = require_object(value, "sender", SENDER_FIELDS)
    if set(sender) != SENDER_FIELDS:
        raise InputError("sender requires name and email")
    return {
        "name": require_text(sender["name"], "sender.name", 300),
        "email": validate_email(sender["email"], "sender.email"),
    }


def validate_contact(value: Any) -> dict[str, object]:
    contact = require_object(value, "contact", CONTACT_FIELDS)
    required = {"name", "source_url", "observed_at", "status", "email"}
    if not required.issubset(contact):
        raise InputError("each contact requires name, email, source_url, observed_at, and status")
    status = contact["status"]
    if status not in {"observed", "unknown"}:
        raise InputError("contact.status must be observed or unknown")

    normalized: dict[str, object] = {
        "name": require_text(contact["name"], "contact.name", 300),
        "source_url": validate_url(contact["source_url"], "contact.source_url"),
        "status": status,
        "context": "",
    }
    context = contact.get("context", "")
    if not isinstance(context, str):
        raise InputError("contact.context must be a string")
    normalized["context"] = context.strip()

    if status == "observed":
        normalized["email"] = validate_email(contact["email"], "contact.email")
        normalized["observed_at"] = validate_observed_at(contact["observed_at"])
    else:
        if contact["email"] is not None:
            raise InputError("unknown contacts must not claim an email value")
        normalized["email"] = None
        normalized["observed_at"] = (
            validate_observed_at(contact["observed_at"])
            if contact["observed_at"] is not None
            else None
        )
    return normalized


def build_draft(
    product: dict[str, object], sender: dict[str, str], contact: dict[str, object]
) -> dict[str, object]:
    selling_points = "\n".join(f"- {point}" for point in product["selling_points"])
    context = contact["context"] or "The user identified this audience as relevant."
    subject = f"Resource suggestion: {product['name']}"
    body = (
        f"Hello {contact['name']} team,\n\n"
        f"I am sharing {product['name']} ({product['url']}) for your consideration.\n\n"
        f"{product['tagline']}\n\n"
        f"Why it may be relevant:\n{selling_points}\n\n"
        f"Context: {context}\n\n"
        "Please review it only if it fits your audience and editorial rules.\n\n"
        f"Thanks,\n{sender['name']}\n{sender['email']}"
    )
    return {
        "recipient_name": contact["name"],
        "recipient_email": contact["email"],
        "source_url": contact["source_url"],
        "observed_at": contact["observed_at"],
        "subject": subject,
        "body": body,
        "delivery_status": "not-sent",
    }


def build_result(payload: dict[str, Any]) -> dict[str, object]:
    product = validate_product(payload["product"])
    sender = validate_sender(payload["sender"])
    contacts_value = payload["contacts"]
    if not isinstance(contacts_value, list):
        raise InputError("contacts must be an array")
    contacts = [validate_contact(contact) for contact in contacts_value]
    drafts = [
        build_draft(product, sender, contact)
        for contact in contacts
        if contact["status"] == "observed"
    ]
    skipped = [
        {
            "name": contact["name"],
            "source_url": contact["source_url"],
            "observed_at": contact["observed_at"],
            "status": "unknown",
            "reason": "No observed contact address was supplied.",
        }
        for contact in contacts
        if contact["status"] == "unknown"
    ]
    return {
        "generated_at": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace(
            "+00:00", "Z"
        ),
        "delivery_status": "not-sent",
        "drafts": drafts,
        "skipped": skipped,
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
