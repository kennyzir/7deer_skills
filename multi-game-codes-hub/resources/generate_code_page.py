#!/usr/bin/env python3
"""Generate one Roblox codes page from validated JSON data."""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence
from urllib.parse import urlsplit


SKILL_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_TEMPLATE_PATH = SKILL_ROOT / "resources" / "templates" / "codes_page.tsx"
TEMPLATE_VARIABLE_RE = re.compile(r"{{\s*[^{}]+\s*}}")
SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
REQUIRED_CODE_FIELDS = ("code", "reward")
TOP_LEVEL_FIELDS = {
    "gameName",
    "gameSlug",
    "baseUrl",
    "activeCodes",
    "expiredCodes",
    "redemptionSteps",
    "faq",
}
CODE_FIELDS = {"code", "reward", "expiryDate", "conditions"}
FAQ_FIELDS = {"question", "answer"}

REDEMPTION_SECTION = """        <section className="mb-12 p-6 bg-gradient-to-br from-zinc-900 to-black border border-zinc-800 rounded-lg">
          <h2 className="text-2xl font-bold mb-4">How to Redeem {gameName} Codes</h2>
          <ol className="list-decimal list-inside space-y-3 text-sm text-zinc-400">
            {redemptionSteps.map((step, index) => (
              <li key={index}>{step}</li>
            ))}
          </ol>
        </section>"""

FAQ_SCHEMA_DEFINITION = """  const faqSchema = {
    '@context': 'https://schema.org',
    '@type': 'FAQPage',
    mainEntity: faqItems.map(item => ({
      '@type': 'Question',
      name: item.question,
      acceptedAnswer: { '@type': 'Answer', text: item.answer },
    })),
  };
  const faqSchemaMarkup = { __html: JSON.stringify(faqSchema) };"""

FAQ_SCHEMA_SCRIPT = """      <script type="application/ld+json" dangerouslySetInnerHTML={faqSchemaMarkup} />"""

FAQ_SECTION = """        <section className="mb-8">
          <h2 className="text-xl font-bold mb-4">Frequently Asked Questions</h2>
          <div className="space-y-4">
            {faqItems.map((item, index) => (
              <details key={index} className="group border border-glass-border rounded-lg bg-card/40">
                <summary className="cursor-pointer p-4 font-medium text-zinc-200 group-open:border-b group-open:border-glass-border">
                  {item.question}
                </summary>
                <div className="p-4 text-sm text-zinc-400">{item.answer}</div>
              </details>
            ))}
          </div>
        </section>"""


class InputError(ValueError):
    """Raised when input data or a template cannot produce a safe page."""


def validate_base_url(value: Any) -> str:
    if not isinstance(value, str) or not value.strip():
        raise InputError("baseUrl must be a non-empty string")
    normalized = value.strip().rstrip("/")
    parsed = urlsplit(normalized)
    if parsed.scheme not in {"http", "https"} or not parsed.hostname:
        raise InputError("baseUrl must be an absolute http:// or https:// URL")
    if parsed.username or parsed.password:
        raise InputError("baseUrl must not contain embedded credentials")
    if parsed.query or parsed.fragment:
        raise InputError("baseUrl must not contain a query string or fragment")
    return normalized


def validate_codes(value: Any, field_name: str) -> List[Dict[str, Any]]:
    if not isinstance(value, list):
        raise InputError(f"{field_name} must be an array")
    normalized = []
    for index, entry in enumerate(value):
        if not isinstance(entry, dict):
            raise InputError(f"{field_name}[{index}] must be an object")
        unknown_fields = set(entry) - CODE_FIELDS
        if unknown_fields:
            raise InputError(
                f"{field_name}[{index}] contains unknown field(s): "
                f"{', '.join(sorted(unknown_fields))}"
            )
        for required_field in REQUIRED_CODE_FIELDS:
            field_value = entry.get(required_field)
            if not isinstance(field_value, str) or not field_value.strip():
                raise InputError(
                    f"{field_name}[{index}].{required_field} must be a non-empty string"
                )
        normalized_entry = {
            field: entry[field].strip() if isinstance(entry[field], str) else entry[field]
            for field in entry
        }
        for optional_field in CODE_FIELDS - set(REQUIRED_CODE_FIELDS):
            if optional_field in normalized_entry and (
                not isinstance(normalized_entry[optional_field], str)
                or not normalized_entry[optional_field]
            ):
                raise InputError(
                    f"{field_name}[{index}].{optional_field} must be a non-empty string"
                )
        normalized.append(normalized_entry)
    return normalized


def validate_string_array(value: Any, field_name: str) -> List[str]:
    if not isinstance(value, list):
        raise InputError(f"{field_name} must be an array")
    normalized = []
    for index, entry in enumerate(value):
        if not isinstance(entry, str) or not entry.strip():
            raise InputError(f"{field_name}[{index}] must be a non-empty string")
        normalized.append(entry.strip())
    return normalized


def validate_faq(value: Any) -> List[Dict[str, str]]:
    if not isinstance(value, list):
        raise InputError("faq must be an array")
    normalized = []
    for index, entry in enumerate(value):
        if not isinstance(entry, dict):
            raise InputError(f"faq[{index}] must be an object")
        unknown_fields = set(entry) - FAQ_FIELDS
        if unknown_fields:
            raise InputError(
                f"faq[{index}] contains unknown field(s): "
                f"{', '.join(sorted(unknown_fields))}"
            )
        normalized_entry = {}
        for field in sorted(FAQ_FIELDS):
            field_value = entry.get(field)
            if not isinstance(field_value, str) or not field_value.strip():
                raise InputError(f"faq[{index}].{field} must be a non-empty string")
            normalized_entry[field] = field_value.strip()
        normalized.append(normalized_entry)
    return normalized


def validate_config(data: Any) -> Dict[str, Any]:
    if not isinstance(data, dict):
        raise InputError("input JSON must be an object")

    unknown_fields = set(data) - TOP_LEVEL_FIELDS
    if unknown_fields:
        raise InputError(
            f"input JSON contains unknown top-level field(s): "
            f"{', '.join(sorted(unknown_fields))}"
        )

    game_name = data.get("gameName")
    if not isinstance(game_name, str) or not game_name.strip():
        raise InputError("gameName must be a non-empty string")

    game_slug = data.get("gameSlug")
    if not isinstance(game_slug, str) or not SLUG_RE.fullmatch(game_slug):
        raise InputError("gameSlug must contain lowercase letters, digits, and single hyphens")

    return {
        "gameName": game_name.strip(),
        "gameSlug": game_slug,
        "baseUrl": validate_base_url(data.get("baseUrl")),
        "activeCodes": validate_codes(data.get("activeCodes", []), "activeCodes"),
        "expiredCodes": validate_codes(data.get("expiredCodes", []), "expiredCodes"),
        "redemptionSteps": validate_string_array(
            data.get("redemptionSteps", []), "redemptionSteps"
        ),
        "faq": validate_faq(data.get("faq", [])),
    }


def load_json(path: Path) -> Dict[str, Any]:
    try:
        raw = path.read_text(encoding="utf-8")
    except OSError as exc:
        raise InputError(f"cannot read input file '{path}': {exc}") from exc
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise InputError(f"input file '{path}' is not valid JSON: {exc.msg}") from exc
    return validate_config(data)


def load_template(template_path: Optional[Path] = None) -> str:
    path = DEFAULT_TEMPLATE_PATH if template_path is None else template_path
    try:
        return path.read_text(encoding="utf-8")
    except OSError as exc:
        raise InputError(f"cannot read template '{path}': {exc}") from exc


def reward_summary(active_codes: List[Dict[str, Any]]) -> str:
    rewards = set()
    for entry in active_codes:
        reward = entry["reward"]
        if "Spin" in reward:
            rewards.add("Spins")
        if "Cash" in reward or "Yen" in reward:
            rewards.add("Cash")
        if "Arrow" in reward:
            rewards.add("Arrows")
    return ", ".join(sorted(rewards)) or "rewards"


def generate_code_page(
    config: Dict[str, Any],
    output_path: Path,
    template_path: Optional[Path] = None,
    now_utc: Optional[datetime] = None,
) -> Path:
    data = validate_config(config)
    template = load_template(template_path)
    current = now_utc or datetime.now(timezone.utc)
    if current.tzinfo is None:
        current = current.replace(tzinfo=timezone.utc)
    else:
        current = current.astimezone(timezone.utc)

    has_faq = bool(data["faq"])
    replacements = {
        "{{gameNameJson}}": json.dumps(data["gameName"], ensure_ascii=False),
        "{{gameSlugJson}}": json.dumps(data["gameSlug"], ensure_ascii=False),
        "{{baseUrlJson}}": json.dumps(data["baseUrl"], ensure_ascii=False),
        "{{rewardsJson}}": json.dumps(reward_summary(data["activeCodes"]), ensure_ascii=False),
        "{{activeCodesData}}": json.dumps(data["activeCodes"], indent=2, ensure_ascii=False),
        "{{expiredCodesData}}": json.dumps(data["expiredCodes"], indent=2, ensure_ascii=False),
        "{{redemptionStepsData}}": json.dumps(
            data["redemptionSteps"], indent=2, ensure_ascii=False
        ),
        "{{faqItemsData}}": json.dumps(data["faq"], indent=2, ensure_ascii=False),
        "{{generatedDateJson}}": json.dumps(current.strftime("%Y-%m-%d")),
        "{{currentMonthJson}}": json.dumps(current.strftime("%B")),
        "{{currentYearJson}}": json.dumps(current.strftime("%Y")),
        "{{redemptionSection}}": REDEMPTION_SECTION if data["redemptionSteps"] else "",
        "{{faqSchemaDefinition}}": FAQ_SCHEMA_DEFINITION if has_faq else "",
        "{{faqSchemaScript}}": FAQ_SCHEMA_SCRIPT if has_faq else "",
        "{{faqSection}}": FAQ_SECTION if has_faq else "",
    }

    content = template
    for placeholder, replacement in replacements.items():
        content = content.replace(placeholder, replacement)

    unresolved = sorted(set(TEMPLATE_VARIABLE_RE.findall(content)))
    if unresolved:
        raise InputError(f"template contains unresolved variables: {', '.join(unresolved)}")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(content, encoding="utf-8")
    return output_path


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Generate a Roblox codes page")
    parser.add_argument("--input", required=True, type=Path, help="Input JSON file")
    parser.add_argument("--output", required=True, type=Path, help="Output TSX file")
    parser.add_argument(
        "--template",
        type=Path,
        help="Optional template path; relative paths resolve from the current working directory",
    )
    return parser


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        config = load_json(args.input)
        output = generate_code_page(config, args.output, args.template)
    except InputError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    print(f"Generated codes page: {output}")
    print(f"Game: {config['gameName']}")
    print(f"Active codes: {len(config['activeCodes'])}")
    print(f"Expired codes: {len(config['expiredCodes'])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
