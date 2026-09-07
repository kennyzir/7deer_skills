from __future__ import annotations

import importlib.util
import io
import json
import os
import re
import subprocess
import sys
import tempfile
import unittest
from contextlib import contextmanager, redirect_stderr, redirect_stdout
from datetime import datetime, timezone
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
REPO_ROOT = SKILL_ROOT.parent
SCRIPT_PATH = SKILL_ROOT / "resources" / "generate_code_page.py"
SPEC = importlib.util.spec_from_file_location("generate_code_page", SCRIPT_PATH)
assert SPEC is not None and SPEC.loader is not None
generator = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(generator)


@contextmanager
def working_directory(path: Path):
    previous = Path.cwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(previous)


def valid_config() -> dict:
    return {
        "gameName": "Your Bizarre Adventure",
        "gameSlug": "yba",
        "baseUrl": "https://codes.example",
        "activeCodes": [{"code": "ACTIVE", "reward": "50 Spins"}],
        "expiredCodes": [{"code": "OLD", "reward": "25 Spins"}],
    }


class GenerateCodePageTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)
        self.temp_path = Path(self.temp_dir.name)

    def test_default_template_works_from_arbitrary_cwd_and_replaces_values(self) -> None:
        caller_dir = self.temp_path / "unrelated" / "caller"
        caller_dir.mkdir(parents=True)
        generated_at = datetime(2031, 1, 2, 3, 4, tzinfo=timezone.utc)

        with working_directory(caller_dir):
            output = generator.generate_code_page(
                valid_config(), Path("output/page.tsx"), now_utc=generated_at
            )
            content = output.read_text(encoding="utf-8")

        self.assertIn("https://codes.example/yba", content)
        self.assertIn("January 2031", content)
        self.assertIn("2031-01-02", content)
        self.assertNotRegex(content, re.compile(r"{{\s*[^{}]+\s*}}"))
        self.assertNotIn("jujutsucalc.com", content)

    def test_explicit_template_path_is_relative_to_caller(self) -> None:
        config_path = self.temp_path / "input.json"
        config_path.write_text(json.dumps(valid_config()), encoding="utf-8")
        template_path = self.temp_path / "custom.tsx"
        template_path.write_text("{{gameName}} at {{baseUrl}}", encoding="utf-8")

        with working_directory(self.temp_path), redirect_stdout(io.StringIO()):
            exit_code = generator.main(
                [
                    "--input",
                    "input.json",
                    "--output",
                    "custom-output.tsx",
                    "--template",
                    "custom.tsx",
                ]
            )

        self.assertEqual(exit_code, 0)
        self.assertEqual(
            (self.temp_path / "custom-output.tsx").read_text(encoding="utf-8"),
            "Your Bizarre Adventure at https://codes.example",
        )

    def test_invalid_base_url_fails_without_output(self) -> None:
        config = valid_config()
        config["baseUrl"] = "ftp://invalid.example"
        input_path = self.temp_path / "invalid.json"
        output_path = self.temp_path / "should-not-exist.tsx"
        input_path.write_text(json.dumps(config), encoding="utf-8")
        errors = io.StringIO()

        with redirect_stderr(errors):
            exit_code = generator.main(
                ["--input", str(input_path), "--output", str(output_path)]
            )

        self.assertEqual(exit_code, 2)
        self.assertIn("baseUrl", errors.getvalue())
        self.assertFalse(output_path.exists())

    def test_unknown_template_variable_fails_without_output(self) -> None:
        template_path = self.temp_path / "unknown.tsx"
        template_path.write_text("{{gameName}} {{notSupported}}", encoding="utf-8")
        output_path = self.temp_path / "should-not-exist.tsx"

        with self.assertRaisesRegex(generator.InputError, "notSupported"):
            generator.generate_code_page(
                valid_config(), output_path, template_path=template_path
            )

        self.assertFalse(output_path.exists())

    def test_quick_game_codes_command_runs_from_repository_root(self) -> None:
        output_path = self.temp_path / "quick-example.tsx"
        result = subprocess.run(
            [
                sys.executable,
                "multi-game-codes-hub/resources/generate_code_page.py",
                "--input",
                "examples/quick-game-codes/sample_codes.json",
                "--output",
                str(output_path),
            ],
            cwd=REPO_ROOT,
            check=False,
            capture_output=True,
            text=True,
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        content = output_path.read_text(encoding="utf-8")
        self.assertIn("https://example.com/yba", content)
        self.assertIn("GULLIBLE", content)
        self.assertNotRegex(content, re.compile(r"{{\s*[^{}]+\s*}}"))
        self.assertNotIn("jujutsucalc.com", content)

    def test_seo_intent_example_runs_real_api_from_repository_root(self) -> None:
        result = subprocess.run(
            [sys.executable, "examples/seo-intent-classification/example.py"],
            cwd=REPO_ROOT,
            check=False,
            capture_output=True,
            text=True,
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        rows = json.loads(result.stdout)
        self.assertEqual(
            [row["intent"] for row in rows],
            ["Informational", "Transactional", "Commercial", "Navigational"],
        )


if __name__ == "__main__":
    unittest.main()
