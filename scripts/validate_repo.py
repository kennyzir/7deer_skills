#!/usr/bin/env python3
"""Validate repository-level skill structure, references, and Python syntax."""

from __future__ import annotations

import re
import sys
import tokenize
from pathlib import Path, PurePosixPath
from urllib.parse import unquote, urlsplit

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML is required; install it with: python3 -m pip install PyYAML")
    raise SystemExit(2)


REPO_ROOT = Path(__file__).resolve().parents[1]
SKILL_NAME_RE = re.compile(r"^[a-z0-9-]+$")
ALLOWED_FRONTMATTER_KEYS = {
    "name",
    "description",
    "license",
    "compatibility",
    "allowed-tools",
    "metadata",
}
FENCED_BLOCK_RE = re.compile(r"^[ \t]*(```|~~~).*?^[ \t]*\1[ \t]*$", re.MULTILINE | re.DOTALL)
MARKDOWN_LINK_RE = re.compile(r"!?\[[^\]\n]*\]\(([^)\n]+)\)")
INLINE_CODE_RE = re.compile(r"`([^`\n]+)`")
RESOURCE_PREFIXES = {"assets", "examples", "references", "resources", "scripts", "templates", "tests"}
IGNORED_PYTHON_DIRS = {".git", ".mypy_cache", ".pytest_cache", ".venv", "__pycache__", "node_modules", "venv"}
PRIVATE_MAC_PATH_RE = re.compile("/" + r"Users/[A-Za-z0-9._-]+/")

# These are known business-content defects outside the repository-baseline scope.
# Every exception is exact, must be exercised, and should be removed when repaired.
MISSING_REFERENCE_ALLOWLIST: dict[str, str] = {}

PYTHON_SYNTAX_ALLOWLIST: dict[str, str] = {}


class Results:
    def __init__(self) -> None:
        self.errors: list[str] = []
        self.warnings: list[str] = []
        self.skill_count = 0
        self.python_count = 0

    def error(self, message: str) -> None:
        self.errors.append(message)

    def warn(self, message: str) -> None:
        self.warnings.append(message)


def repo_path(path: Path) -> str:
    return path.relative_to(REPO_ROOT).as_posix()


def parse_frontmatter(skill_file: Path, results: Results) -> str:
    relative = repo_path(skill_file)
    try:
        text = skill_file.read_text(encoding="utf-8")
    except UnicodeDecodeError as exc:
        results.error(f"{relative}: is not valid UTF-8 ({exc})")
        return ""

    if text.startswith("\ufeff"):
        results.error(f"{relative}: starts with a UTF-8 BOM")
        return text.lstrip("\ufeff")
    if not text.startswith("---\n"):
        results.error(f"{relative}: missing opening YAML frontmatter delimiter")
        return text

    end = text.find("\n---\n", 4)
    if end == -1:
        results.error(f"{relative}: missing closing YAML frontmatter delimiter")
        return text

    try:
        metadata = yaml.safe_load(text[4:end])
    except yaml.YAMLError as exc:
        results.error(f"{relative}: invalid YAML frontmatter ({exc})")
        return text

    if not isinstance(metadata, dict):
        results.error(f"{relative}: frontmatter must be a YAML mapping")
        return text

    unsupported_keys = set(metadata) - ALLOWED_FRONTMATTER_KEYS
    if unsupported_keys:
        results.error(
            f"{relative}: unsupported top-level frontmatter key(s): "
            f"{', '.join(sorted(unsupported_keys))}"
        )

    name = metadata.get("name")
    description = metadata.get("description")
    if not isinstance(name, str) or not name.strip():
        results.error(f"{relative}: frontmatter requires a non-empty string 'name'")
    else:
        if len(name) > 64:
            results.error(f"{relative}: name must be no more than 64 characters")
        if not SKILL_NAME_RE.fullmatch(name):
            results.error(f"{relative}: name '{name}' must use lowercase letters, digits, and hyphens")
        if name.startswith("-") or name.endswith("-"):
            results.error(f"{relative}: name must not start or end with a hyphen")
        if "--" in name:
            results.error(f"{relative}: name must not contain consecutive hyphens")
        if name != skill_file.parent.name:
            results.error(f"{relative}: name '{name}' does not match directory '{skill_file.parent.name}'")
    if not isinstance(description, str) or not description.strip():
        results.error(f"{relative}: frontmatter requires a non-empty string 'description'")
    elif len(description.strip()) > 1024:
        results.error(f"{relative}: description must be no more than 1024 characters")

    compatibility = metadata.get("compatibility")
    if "compatibility" in metadata:
        if not isinstance(compatibility, str) or not compatibility.strip():
            results.error(f"{relative}: compatibility must be a non-empty string when provided")
        elif len(compatibility.strip()) > 500:
            results.error(f"{relative}: compatibility must be no more than 500 characters")

    additional_metadata = metadata.get("metadata")
    if "metadata" in metadata:
        if not isinstance(additional_metadata, dict):
            results.error(f"{relative}: metadata must be a mapping")
        else:
            for key, value in additional_metadata.items():
                if not isinstance(key, str) or not isinstance(value, str):
                    results.error(f"{relative}: metadata keys and values must all be strings")
                    break

    return text[end + 5 :]


def link_destination(raw: str) -> str:
    destination = raw.strip()
    if destination.startswith("<") and ">" in destination:
        return destination[1 : destination.index(">")]
    return destination.split(maxsplit=1)[0]


def reference_candidates(skill_dir: Path, body: str) -> set[str]:
    """Return only explicit file references, excluding fenced examples and templates."""
    prose = FENCED_BLOCK_RE.sub("", body)
    candidates = {link_destination(match.group(1)) for match in MARKDOWN_LINK_RE.finditer(prose)}

    for match in INLINE_CODE_RE.finditer(prose):
        candidate = match.group(1).strip()
        normalized = candidate.removeprefix("./")
        first_part = PurePosixPath(normalized).parts[0] if normalized else ""
        if (
            first_part in RESOURCE_PREFIXES
            and (skill_dir / first_part).is_dir()
            and PurePosixPath(normalized).suffix
        ):
            candidates.add(candidate)

    return candidates


def resolve_reference(skill_dir: Path, raw_reference: str) -> Path | None:
    reference = unquote(urlsplit(raw_reference).path).strip()
    if not reference or reference.startswith("/"):
        return None
    if urlsplit(raw_reference).scheme or raw_reference.startswith(("#", "mailto:")):
        return None
    if any(marker in reference for marker in ("{", "}", "<", ">", "*")):
        return None

    relative = PurePosixPath(reference.removeprefix("./"))
    if relative.parts and relative.parts[0] == skill_dir.name:
        return REPO_ROOT.joinpath(*relative.parts).resolve()
    return skill_dir.joinpath(*relative.parts).resolve()


def validate_references(skill_file: Path, body: str, results: Results, used: set[str]) -> None:
    source = repo_path(skill_file)
    for raw_reference in sorted(reference_candidates(skill_file.parent, body)):
        target = resolve_reference(skill_file.parent, raw_reference)
        if target is None:
            continue
        try:
            relative_target = repo_path(target)
        except ValueError:
            results.error(f"{source}: reference escapes the repository: {raw_reference}")
            continue
        if target.exists():
            continue
        if relative_target in MISSING_REFERENCE_ALLOWLIST:
            used.add(relative_target)
            results.warn(
                f"{source}: allowlisted missing reference {relative_target} "
                f"({MISSING_REFERENCE_ALLOWLIST[relative_target]})"
            )
        else:
            results.error(f"{source}: referenced file does not exist: {relative_target}")


def validate_skills(results: Results) -> None:
    used_allowlist: set[str] = set()
    for skill_file in sorted(REPO_ROOT.glob("*/SKILL.md")):
        results.skill_count += 1
        body = parse_frontmatter(skill_file, results)
        validate_references(skill_file, body, results, used_allowlist)

    stale = set(MISSING_REFERENCE_ALLOWLIST) - used_allowlist
    for path in sorted(stale):
        results.error(f"stale missing-reference allowlist entry: {path}")


def validate_python(results: Results) -> None:
    used_allowlist: set[str] = set()
    for python_file in sorted(REPO_ROOT.rglob("*.py")):
        if IGNORED_PYTHON_DIRS.intersection(python_file.relative_to(REPO_ROOT).parts):
            continue
        results.python_count += 1
        relative = repo_path(python_file)
        try:
            with tokenize.open(python_file) as source_file:
                source = source_file.read()
            compile(source, relative, "exec")
        except (SyntaxError, UnicodeDecodeError) as exc:
            if relative in PYTHON_SYNTAX_ALLOWLIST:
                used_allowlist.add(relative)
                results.warn(
                    f"{relative}: allowlisted Python syntax failure "
                    f"({PYTHON_SYNTAX_ALLOWLIST[relative]}): {exc}"
                )
            else:
                results.error(f"{relative}: Python syntax check failed: {exc}")

    stale = set(PYTHON_SYNTAX_ALLOWLIST) - used_allowlist
    for path in sorted(stale):
        results.error(f"stale Python-syntax allowlist entry: {path}")


def validate_portable_paths(results: Results) -> None:
    for path in sorted(REPO_ROOT.rglob("*")):
        if not path.is_file():
            continue
        relative_parts = path.relative_to(REPO_ROOT).parts
        if IGNORED_PYTHON_DIRS.intersection(relative_parts):
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        for line_number, line in enumerate(text.splitlines(), 1):
            if PRIVATE_MAC_PATH_RE.search(line):
                results.error(
                    f"{repo_path(path)}:{line_number}: hard-coded macOS user path is not portable"
                )


def main() -> int:
    results = Results()
    validate_skills(results)
    validate_python(results)
    validate_portable_paths(results)

    for warning in results.warnings:
        print(f"WARN: {warning}")
    for error in results.errors:
        print(f"ERROR: {error}")

    print(
        f"Checked {results.skill_count} top-level skills and "
        f"{results.python_count} Python files: "
        f"{len(results.errors)} error(s), {len(results.warnings)} allowlisted warning(s)."
    )
    return 1 if results.errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
