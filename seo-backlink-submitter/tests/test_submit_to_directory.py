from __future__ import annotations

import importlib.util
import io
import json
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path
from unittest.mock import AsyncMock, patch


SCRIPT_PATH = Path(__file__).parents[1] / "scripts" / "submit_to_directory.py"
SPEC = importlib.util.spec_from_file_location("submit_to_directory", SCRIPT_PATH)
assert SPEC is not None and SPEC.loader is not None
submitter = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(submitter)


class SubmitToDirectoryTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)
        self.target_file = Path(self.temp_dir.name) / "target.json"
        self.target = {
            "name": "Example Tool",
            "url": "https://example.com",
            "description": "A useful example tool.",
            "email": "owner@example.com",
            "category": "Developer Tools",
            "tags": ["AI", "Tools"],
        }
        self.target_file.write_text(json.dumps(self.target), encoding="utf-8")
        self.arguments = [
            "--directory",
            "https://directory.example/submit",
            "--target",
            str(self.target_file),
        ]

    def test_default_is_network_free_dry_run(self) -> None:
        output = io.StringIO()
        fake_submit = AsyncMock()
        with patch.object(submitter, "submit_live", fake_submit), redirect_stdout(output):
            exit_code = submitter.main(self.arguments)

        self.assertEqual(exit_code, 0)
        fake_submit.assert_not_awaited()
        result = json.loads(output.getvalue())
        self.assertEqual(result["mode"], "dry-run")
        self.assertEqual(result["status"], "not_submitted")

    def test_invalid_target_is_rejected(self) -> None:
        self.target.pop("email")
        self.target_file.write_text(json.dumps(self.target), encoding="utf-8")
        errors = io.StringIO()

        with redirect_stderr(errors):
            exit_code = submitter.main(self.arguments)

        self.assertEqual(exit_code, 2)
        self.assertIn("target field 'email'", errors.getvalue())

    def test_submit_flag_opens_explicit_submission_gate(self) -> None:
        expected = {
            "mode": "submit",
            "status": "submit_triggered",
            "directory": "https://directory.example/submit",
            "site": "https://example.com",
            "filled_fields": ["name", "url"],
        }
        fake_submit = AsyncMock(return_value=expected)
        output = io.StringIO()

        with patch.object(submitter, "submit_live", fake_submit), redirect_stdout(output):
            exit_code = submitter.main([*self.arguments, "--submit"])

        self.assertEqual(exit_code, 0)
        fake_submit.assert_awaited_once()
        self.assertEqual(json.loads(output.getvalue()), expected)


if __name__ == "__main__":
    unittest.main()
