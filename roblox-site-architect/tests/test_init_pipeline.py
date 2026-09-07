from __future__ import annotations

import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import unittest

import yaml


SKILL_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = SKILL_ROOT / "scripts" / "init_pipeline.py"
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
MINIMUM_FIELDS = {
    "01-opportunity-report.md": (
        "Game identity",
        "Evaluation question",
        "Demand/momentum",
        "Supply/competition",
        "Supporting evidence",
        "Counter-evidence",
        "Decision",
        "Confidence limits",
    ),
    "02-keyword-map.md": (
        "cluster_id",
        "Queries",
        "Locale",
        "Intent",
        "Demand evidence",
        "Competition evidence",
        "Target",
        "Disposition",
        "Priority",
    ),
    "03-source-ledger.md": (
        "source_id",
        "Source",
        "Publisher/type",
        "observed_at",
        "Evidence captured",
        "Claim supported",
        "Freshness",
        "Reliability/conflict",
        "Claim index",
    ),
    "04-site-plan.md": (
        "Route/unit",
        "Purpose",
        "Evidence",
        "Content/data contract",
        "Internal-link role",
        "State",
        "Acceptance checks",
        "Local result",
    ),
    "05-seo-audit.md": (
        "check_id",
        "Category",
        "Target",
        "Result",
        "Severity",
        "Evidence",
        "Remediation/retest",
    ),
    "06-deployment-report.md": (
        "Deployment state",
        "Revision/build",
        "Target",
        "Deployment result",
        "Reachability check",
        "Claim/data set",
        "Source/owner",
        "Recheck trigger",
        "Review gate",
        "Failure behavior",
        "Scheduling state",
    ),
    "07-growth-backlog.md": (
        "item_id",
        "Type/target",
        "Evidence/rationale",
        "Effort/risk",
        "Next action/owner",
        "Success metric",
        "Authorization",
        "State/result",
    ),
}


class PipelineInitializerTests(unittest.TestCase):
    def run_cli(
        self, project_root: Path, *extra: str, cwd: Path | None = None
    ) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [
                sys.executable,
                str(SCRIPT),
                "--project-root",
                str(project_root),
                "--game",
                "Verified Test Name",
                *extra,
            ],
            cwd=cwd,
            text=True,
            capture_output=True,
            check=False,
        )

    def test_default_dry_run_is_json_and_writes_nothing(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            project_root = Path(temporary_directory) / "project"
            project_root.mkdir()

            result = self.run_cli(project_root)

            self.assertEqual(result.returncode, 0, result.stderr)
            plan = json.loads(result.stdout)
            self.assertEqual(plan["mode"], "dry-run")
            self.assertEqual(plan["status"], "not-applied")
            self.assertEqual(len(plan["artifacts"]), 7)
            self.assertFalse((project_root / "pipeline").exists())

    def test_apply_creates_exactly_seven_contract_compliant_files(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            project_root = Path(temporary_directory) / "project"
            project_root.mkdir()

            result = self.run_cli(project_root, "--scope", "Offline test", "--apply")

            self.assertEqual(result.returncode, 0, result.stderr)
            response = json.loads(result.stdout)
            self.assertEqual(response["mode"], "apply")
            self.assertEqual(response["status"], "created")
            pipeline_dir = project_root / "pipeline"
            self.assertEqual(
                {path.name for path in pipeline_dir.iterdir()}, set(ARTIFACTS)
            )

            for index, filename in enumerate(ARTIFACTS):
                with self.subTest(filename=filename):
                    content = (pipeline_dir / filename).read_text(encoding="utf-8")
                    parts = content.split("---", 2)
                    self.assertEqual(parts[0], "")
                    header = yaml.safe_load(parts[1])
                    self.assertEqual(header["artifact"], filename.removesuffix(".md"))
                    self.assertEqual(header["status"], "partial" if index == 0 else "blocked")
                    self.assertEqual(header["game"], "Verified Test Name")
                    self.assertEqual(header["scope"], "Offline test")
                    self.assertRegex(
                        header["generated_at"],
                        r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$",
                    )
                    self.assertEqual(header["observed_through"], "unknown")
                    self.assertEqual(header["sources"], [])
                    self.assertTrue(header["gaps"])
                    expected_upstream = (
                        [] if index == 0 else [ARTIFACTS[index - 1].removesuffix(".md")]
                    )
                    self.assertEqual(header["upstream"], expected_upstream)
                    if index:
                        self.assertIn(expected_upstream[0], " ".join(header["gaps"]))

                    section_positions = [content.index(section) for section in REQUIRED_SECTIONS]
                    self.assertEqual(section_positions, sorted(section_positions))
                    self.assertIsNone(re.search(r"@@[A-Z0-9_]+@@", content))
                    for field in MINIMUM_FIELDS[filename]:
                        self.assertIn(field, content)

    def test_script_resolves_templates_from_any_working_directory(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            temporary_root = Path(temporary_directory)
            project_root = temporary_root / "project"
            unrelated_cwd = temporary_root / "elsewhere"
            project_root.mkdir()
            unrelated_cwd.mkdir()

            result = self.run_cli(project_root, "--apply", cwd=unrelated_cwd)

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(
                {path.name for path in (project_root / "pipeline").iterdir()},
                set(ARTIFACTS),
            )

    def test_existing_artifact_causes_atomic_failure(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            project_root = Path(temporary_directory) / "project"
            pipeline_dir = project_root / "pipeline"
            pipeline_dir.mkdir(parents=True)
            conflict = pipeline_dir / "04-site-plan.md"
            conflict.write_text("keep me\n", encoding="utf-8")

            result = self.run_cli(project_root, "--apply")

            self.assertEqual(result.returncode, 2)
            error = json.loads(result.stderr)
            self.assertEqual(error["status"], "error")
            self.assertIn("already exists", error["error"])
            self.assertEqual(conflict.read_text(encoding="utf-8"), "keep me\n")
            self.assertEqual(list(pipeline_dir.iterdir()), [conflict])

    def test_invalid_game_and_root_fail_without_writes(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            temporary_root = Path(temporary_directory)
            valid_root = temporary_root / "project"
            valid_root.mkdir()
            bad_game = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPT),
                    "--project-root",
                    str(valid_root),
                    "--game",
                    "   ",
                    "--apply",
                ],
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(bad_game.returncode, 2)
            self.assertFalse((valid_root / "pipeline").exists())

            invalid_root = temporary_root / "not-a-directory"
            invalid_root.write_text("file\n", encoding="utf-8")
            bad_root = self.run_cli(invalid_root, "--apply")
            self.assertEqual(bad_root.returncode, 2)
            self.assertEqual(invalid_root.read_text(encoding="utf-8"), "file\n")

    def test_pipeline_symlink_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            temporary_root = Path(temporary_directory)
            project_root = temporary_root / "project"
            outside = temporary_root / "outside"
            project_root.mkdir()
            outside.mkdir()
            (project_root / "pipeline").symlink_to(outside, target_is_directory=True)

            result = self.run_cli(project_root, "--apply")

            self.assertEqual(result.returncode, 2)
            self.assertEqual(list(outside.iterdir()), [])

    def test_force_option_is_not_available(self) -> None:
        help_result = subprocess.run(
            [sys.executable, str(SCRIPT), "--help"],
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(help_result.returncode, 0)
        self.assertNotIn("--force", help_result.stdout)

    def test_template_directory_contains_exactly_seven_maintained_templates(self) -> None:
        self.assertEqual(
            {path.name for path in TEMPLATE_ROOT.glob("*.md")}, set(ARTIFACTS)
        )


if __name__ == "__main__":
    unittest.main()
