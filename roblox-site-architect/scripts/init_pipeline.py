#!/usr/bin/env python3
"""Safely initialize the seven Roblox Site Growth Pipeline artifacts."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import re
import sys
from typing import Sequence


SKILL_ROOT = Path(__file__).resolve().parents[1]
TEMPLATE_ROOT = SKILL_ROOT / "assets" / "pipeline-templates"
ARTIFACTS = (
    "01-opportunity-report.md",
    "02-keyword-map.md",
    "03-source-ledger.md",
    "04-site-plan.md",
    "05-seo-audit.md",
    "06-deployment-report.md",
    "07-growth-backlog.md",
)
REQUIRED_SECTIONS = (
    "## Decision or outcome",
    "## Evidence and analysis",
    "## Unknowns and conflicts",
    "## Handoff",
)
COMMON_HEADER_FIELDS = (
    "artifact",
    "status",
    "game",
    "scope",
    "generated_at",
    "observed_through",
    "upstream",
    "sources",
    "gaps",
)
PLACEHOLDERS = {
    "@@GAME_JSON@@",
    "@@SCOPE_JSON@@",
    "@@GENERATED_AT_JSON@@",
}
PLACEHOLDER_PATTERN = re.compile(r"@@[A-Z0-9_]+@@")
DEFAULT_SCOPE = "Initialize the Roblox Site Growth Pipeline"


class ValidationError(ValueError):
    """Raised when initialization cannot safely begin."""


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Plan creation of seven pipeline artifacts. Nothing is written unless "
            "--apply is supplied."
        )
    )
    parser.add_argument("--project-root", required=True, help="Existing project directory")
    parser.add_argument("--game", required=True, help="Canonical Roblox game name")
    parser.add_argument(
        "--scope",
        default=DEFAULT_SCOPE,
        help=f"Bounded pipeline scope (default: {DEFAULT_SCOPE!r})",
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="Create pipeline/ and all seven artifacts after successful preflight",
    )
    return parser.parse_args(argv)


def validate_single_line(value: str, label: str, maximum: int) -> str:
    normalized = value.strip()
    if not normalized:
        raise ValidationError(f"{label} must not be empty")
    if len(normalized) > maximum:
        raise ValidationError(f"{label} must be at most {maximum} characters")
    if any(not character.isprintable() for character in normalized):
        raise ValidationError(f"{label} must be a single printable line")
    return normalized


def validate_project_root(raw_root: str) -> Path:
    if not raw_root.strip():
        raise ValidationError("project root must not be empty")
    root = Path(raw_root).expanduser().resolve(strict=False)
    if not root.exists():
        raise ValidationError(f"project root does not exist: {root}")
    if not root.is_dir():
        raise ValidationError(f"project root is not a directory: {root}")
    if root == Path(root.anchor):
        raise ValidationError("project root must not be a filesystem root")
    return root


def load_templates() -> dict[str, str]:
    if not TEMPLATE_ROOT.is_dir():
        raise ValidationError(f"template directory is missing: {TEMPLATE_ROOT}")

    expected = set(ARTIFACTS)
    actual = {path.name for path in TEMPLATE_ROOT.glob("*.md") if path.is_file()}
    if actual != expected:
        missing = sorted(expected - actual)
        unexpected = sorted(actual - expected)
        raise ValidationError(
            f"template set mismatch; missing={missing}, unexpected={unexpected}"
        )

    templates: dict[str, str] = {}
    for filename in ARTIFACTS:
        template_path = TEMPLATE_ROOT / filename
        try:
            template = template_path.read_text(encoding="utf-8")
        except (OSError, UnicodeError) as error:
            raise ValidationError(f"cannot read template {template_path}: {error}") from error
        found = set(PLACEHOLDER_PATTERN.findall(template))
        if found != PLACEHOLDERS:
            raise ValidationError(
                f"template {template_path} has invalid placeholders: {sorted(found)}"
            )
        templates[filename] = template
    return templates


def render_templates(
    templates: dict[str, str], game: str, scope: str, generated_at: str
) -> dict[str, str]:
    replacements = {
        "@@GAME_JSON@@": json.dumps(game, ensure_ascii=False),
        "@@SCOPE_JSON@@": json.dumps(scope, ensure_ascii=False),
        "@@GENERATED_AT_JSON@@": json.dumps(generated_at),
    }
    rendered: dict[str, str] = {}
    for filename in ARTIFACTS:
        content = templates[filename]
        for marker, value in replacements.items():
            content = content.replace(marker, value)
        unresolved = PLACEHOLDER_PATTERN.findall(content)
        if unresolved:
            raise ValidationError(
                f"rendered artifact {filename} has unresolved placeholders: {unresolved}"
            )
        rendered[filename] = content
    validate_rendered_templates(rendered)
    return rendered


def validate_rendered_templates(rendered: dict[str, str]) -> None:
    for index, filename in enumerate(ARTIFACTS):
        content = rendered[filename]
        if not content.startswith("---\n") or "\n---\n" not in content[4:]:
            raise ValidationError(f"template {filename} has an invalid YAML header boundary")
        header, body = content[4:].split("\n---\n", 1)
        header_fields = tuple(
            line.split(":", 1)[0]
            for line in header.splitlines()
            if line and not line[0].isspace() and ":" in line
        )
        if header_fields != COMMON_HEADER_FIELDS:
            raise ValidationError(
                f"template {filename} has invalid common header fields: {header_fields}"
            )

        artifact = filename.removesuffix(".md")
        expected_status = "partial" if index == 0 else "blocked"
        for expected_line in (
            f"artifact: {artifact}",
            f"status: {expected_status}",
            "observed_through: unknown",
            "sources: []",
        ):
            if expected_line not in header.splitlines():
                raise ValidationError(f"template {filename} is missing {expected_line!r}")
        if not re.search(
            r'^generated_at: "\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z"$',
            header,
            re.MULTILINE,
        ):
            raise ValidationError(f"template {filename} has a non-UTC generated_at value")

        if index == 0:
            if "upstream: []" not in header.splitlines():
                raise ValidationError(f"template {filename} must start without upstream")
        else:
            upstream = ARTIFACTS[index - 1].removesuffix(".md")
            if f'  - "{upstream}"' not in header.splitlines():
                raise ValidationError(
                    f"template {filename} must identify missing upstream {upstream}"
                )
            if upstream not in header.partition("gaps:")[2]:
                raise ValidationError(
                    f"template {filename} gap must identify missing upstream {upstream}"
                )

        body_sections = tuple(
            line for line in body.splitlines() if line in REQUIRED_SECTIONS
        )
        if body_sections != REQUIRED_SECTIONS:
            raise ValidationError(
                f"template {filename} has invalid common body sections: {body_sections}"
            )


def validate_targets(project_root: Path) -> tuple[Path, list[Path]]:
    pipeline_dir = project_root / "pipeline"
    if pipeline_dir.is_symlink():
        raise ValidationError(f"pipeline target must not be a symlink: {pipeline_dir}")
    if pipeline_dir.exists() and not pipeline_dir.is_dir():
        raise ValidationError(f"pipeline target is not a directory: {pipeline_dir}")
    targets = [pipeline_dir / filename for filename in ARTIFACTS]
    conflicts = [target for target in targets if target.exists() or target.is_symlink()]
    if conflicts:
        formatted = ", ".join(str(path) for path in conflicts)
        raise ValidationError(f"artifact already exists; no files were written: {formatted}")
    return pipeline_dir, targets


def create_artifacts(
    pipeline_dir: Path, targets: list[Path], rendered: dict[str, str]
) -> None:
    created_files: list[Path] = []
    created_directory = False
    try:
        if not pipeline_dir.exists():
            pipeline_dir.mkdir()
            created_directory = True
        for target in targets:
            handle = target.open("x", encoding="utf-8", newline="\n")
            created_files.append(target)
            with handle:
                handle.write(rendered[target.name])
    except BaseException:
        for created_file in reversed(created_files):
            try:
                created_file.unlink()
            except OSError:
                pass
        if created_directory:
            try:
                pipeline_dir.rmdir()
            except OSError:
                pass
        raise


def build_result(
    *,
    mode: str,
    status: str,
    project_root: Path,
    pipeline_dir: Path,
    targets: list[Path],
    game: str,
    scope: str,
    generated_at: str,
) -> dict[str, object]:
    return {
        "mode": mode,
        "status": status,
        "project_root": str(project_root),
        "pipeline_dir": str(pipeline_dir),
        "game": game,
        "scope": scope,
        "generated_at": generated_at,
        "artifacts": [str(target) for target in targets],
    }


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        project_root = validate_project_root(args.project_root)
        game = validate_single_line(args.game, "game", 200)
        scope = validate_single_line(args.scope, "scope", 1000)
        templates = load_templates()
        generated_at = (
            datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")
        )
        rendered = render_templates(templates, game, scope, generated_at)
        pipeline_dir, targets = validate_targets(project_root)
    except ValidationError as error:
        print(json.dumps({"status": "error", "error": str(error)}), file=sys.stderr)
        return 2

    if not args.apply:
        print(
            json.dumps(
                build_result(
                    mode="dry-run",
                    status="not-applied",
                    project_root=project_root,
                    pipeline_dir=pipeline_dir,
                    targets=targets,
                    game=game,
                    scope=scope,
                    generated_at=generated_at,
                ),
                ensure_ascii=False,
                indent=2,
            )
        )
        return 0

    try:
        create_artifacts(pipeline_dir, targets, rendered)
    except OSError as error:
        print(
            json.dumps(
                {
                    "status": "error",
                    "error": f"write failed; new artifacts were rolled back: {error}",
                }
            ),
            file=sys.stderr,
        )
        return 1

    print(
        json.dumps(
            build_result(
                mode="apply",
                status="created",
                project_root=project_root,
                pipeline_dir=pipeline_dir,
                targets=targets,
                game=game,
                scope=scope,
                generated_at=generated_at,
            ),
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
