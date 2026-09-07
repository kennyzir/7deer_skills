#!/usr/bin/env python3
"""Generate CATALOG.md from catalog.json and Skill frontmatter."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from typing import Any, Sequence

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML is required; install it with: python3 -m pip install PyYAML")
    raise SystemExit(2)


REPO_ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = REPO_ROOT / "catalog.json"
OUTPUT_PATH = REPO_ROOT / "CATALOG.md"
MATURITY_LABELS = {
    "ci-tested": "CI-tested",
    "safety-checked": "Safety/contract checked",
    "not-ci-tested": "Not in repository CI",
}
BOUNDARY_LABELS = {
    "research-output": "May read external sources; produces research/local artifacts",
    "local-output": "Produces or changes local files/code",
    "external-gated": "Can reach external side effects; explicit authorization required",
    "guidance": "Guidance or library; execution depends on the consuming task",
}


class CatalogError(ValueError):
    """Raised when the catalog source is invalid."""


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="Fail if CATALOG.md differs from the generated content",
    )
    return parser.parse_args(argv)


def read_frontmatter(skill_file: Path) -> dict[str, Any]:
    text = skill_file.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise CatalogError(f"missing YAML frontmatter: {skill_file.relative_to(REPO_ROOT)}")
    end = text.find("\n---\n", 4)
    if end == -1:
        raise CatalogError(f"unclosed YAML frontmatter: {skill_file.relative_to(REPO_ROOT)}")
    metadata = yaml.safe_load(text[4:end])
    if not isinstance(metadata, dict):
        raise CatalogError(f"invalid YAML frontmatter: {skill_file.relative_to(REPO_ROOT)}")
    return metadata


def load_skill_descriptions() -> dict[str, str]:
    descriptions: dict[str, str] = {}
    for skill_file in sorted(REPO_ROOT.glob("*/SKILL.md")):
        metadata = read_frontmatter(skill_file)
        name = metadata.get("name")
        description = metadata.get("description")
        if name != skill_file.parent.name:
            raise CatalogError(
                f"frontmatter name does not match directory: {skill_file.relative_to(REPO_ROOT)}"
            )
        if not isinstance(description, str) or not description.strip():
            raise CatalogError(f"missing description: {skill_file.relative_to(REPO_ROOT)}")
        descriptions[name] = " ".join(description.split())
    return descriptions


def load_config() -> dict[str, Any]:
    try:
        config = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise CatalogError(f"cannot read catalog.json: {error}") from error
    if not isinstance(config, dict) or config.get("schema_version") != 1:
        raise CatalogError("catalog.json must be an object with schema_version 1")
    if not isinstance(config.get("groups"), list) or not config["groups"]:
        raise CatalogError("catalog.json must define a non-empty groups list")
    return config


def validate_config(config: dict[str, Any], descriptions: dict[str, str]) -> None:
    configured_names: list[str] = []
    group_ids: set[str] = set()
    for group in config["groups"]:
        if not isinstance(group, dict):
            raise CatalogError("each catalog group must be an object")
        group_id = group.get("id")
        if not isinstance(group_id, str) or not group_id or group_id in group_ids:
            raise CatalogError(f"invalid or duplicate group id: {group_id!r}")
        group_ids.add(group_id)
        if not isinstance(group.get("title"), str) or not group["title"].strip():
            raise CatalogError(f"group {group_id} requires a title")
        if not isinstance(group.get("description"), str) or not group["description"].strip():
            raise CatalogError(f"group {group_id} requires a description")
        if not isinstance(group.get("skills"), list) or not group["skills"]:
            raise CatalogError(f"group {group_id} requires a non-empty skills list")

        for skill in group["skills"]:
            if not isinstance(skill, dict):
                raise CatalogError(f"group {group_id} contains a non-object skill entry")
            name = skill.get("name")
            maturity = skill.get("maturity")
            boundary = skill.get("boundary")
            if not isinstance(name, str) or not name:
                raise CatalogError(f"group {group_id} contains an invalid skill name")
            if maturity not in MATURITY_LABELS:
                raise CatalogError(f"skill {name} has invalid maturity {maturity!r}")
            if boundary not in BOUNDARY_LABELS:
                raise CatalogError(f"skill {name} has invalid boundary {boundary!r}")
            if maturity == "ci-tested":
                if not isinstance(skill.get("ci_tests"), int) or skill["ci_tests"] <= 0:
                    raise CatalogError(f"CI-tested skill {name} requires a positive ci_tests count")
                if "ci_checks" in skill:
                    raise CatalogError(f"CI-tested skill {name} must not declare ci_checks")
            elif maturity == "safety-checked":
                if not isinstance(skill.get("ci_checks"), int) or skill["ci_checks"] <= 0:
                    raise CatalogError(
                        f"safety-checked skill {name} requires a positive ci_checks count"
                    )
                if "ci_tests" in skill:
                    raise CatalogError(f"safety-checked skill {name} must not declare ci_tests")
            elif "ci_tests" in skill or "ci_checks" in skill:
                raise CatalogError(
                    f"skill without repository checks {name} must not declare check counts"
                )
            configured_names.append(name)

    duplicates = sorted({name for name in configured_names if configured_names.count(name) > 1})
    if duplicates:
        raise CatalogError(f"duplicate catalog skills: {duplicates}")
    configured = set(configured_names)
    actual = set(descriptions)
    if configured != actual:
        raise CatalogError(
            f"catalog coverage mismatch; missing={sorted(actual - configured)}, "
            f"unknown={sorted(configured - actual)}"
        )


def escape_table_cell(value: str) -> str:
    return value.replace("\\", "\\\\").replace("|", "\\|")


def render_catalog(config: dict[str, Any], descriptions: dict[str, str]) -> str:
    skill_total = len(descriptions)
    behavior_test_total = sum(
        skill.get("ci_tests", 0)
        for group in config["groups"]
        for skill in group["skills"]
    )
    safety_check_total = sum(
        skill.get("ci_checks", 0)
        for group in config["groups"]
        for skill in group["skills"]
    )
    lines = [
        "<!-- Generated by scripts/generate_catalog.py. Edit catalog.json or Skill frontmatter, then regenerate. -->",
        "",
        "# Skill Catalog",
        "",
        f"This catalog covers all {skill_total} top-level Skills. Descriptions come directly from each `SKILL.md` frontmatter; grouping, maturity, and execution boundaries come from `catalog.json`.",
        "",
        "Maturity is deliberately narrow: **CI-tested** means a complete behavior suite is used as a maturity signal; **Safety/contract checked** means CI covers only narrow default-safety or input/output contracts; **Not in repository CI** means no repository-level checks. The current CI-tested rows account for "
        f"{behavior_test_total} behavior tests, while safety/contract-checked rows account for "
        f"{safety_check_total} checks.",
        "",
        "Execution-boundary labels describe the broadest behavior represented by a Skill. Reading external sources still depends on tool availability and access. Sending, submitting, deploying, purchasing, scheduling, or calling a paid/mutating API always requires explicit user authorization.",
        "",
    ]

    for group in config["groups"]:
        lines.extend(
            [
                f"## {group['title']}",
                "",
                group["description"],
                "",
                "| Skill | Frontmatter description | Maturity | Execution boundary |",
                "|---|---|---|---|",
            ]
        )
        for skill in group["skills"]:
            maturity = MATURITY_LABELS[skill["maturity"]]
            if skill["maturity"] == "ci-tested":
                maturity += f" ({skill['ci_tests']} tests)"
            elif skill["maturity"] == "safety-checked":
                maturity += f" ({skill['ci_checks']} checks)"
            lines.append(
                "| "
                f"[`{skill['name']}`]({skill['name']}/SKILL.md) | "
                f"{escape_table_cell(descriptions[skill['name']])} | "
                f"{maturity} | {BOUNDARY_LABELS[skill['boundary']]} |"
            )
        lines.append("")

    return "\n".join(lines)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        descriptions = load_skill_descriptions()
        config = load_config()
        validate_config(config, descriptions)
        generated = render_catalog(config, descriptions)
    except CatalogError as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 2

    if args.check:
        try:
            current = OUTPUT_PATH.read_text(encoding="utf-8")
        except (OSError, UnicodeError) as error:
            print(f"ERROR: cannot read {OUTPUT_PATH.name}: {error}", file=sys.stderr)
            return 1
        if current != generated:
            print(
                "ERROR: CATALOG.md is out of date; run python scripts/generate_catalog.py",
                file=sys.stderr,
            )
            return 1
        print(f"CATALOG.md is current ({len(descriptions)} skills)")
        return 0

    with OUTPUT_PATH.open("w", encoding="utf-8", newline="\n") as output_file:
        output_file.write(generated)
    print(f"Wrote {OUTPUT_PATH.relative_to(REPO_ROOT)} ({len(descriptions)} skills)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
