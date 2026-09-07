from __future__ import annotations

import importlib.util
import io
import json
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import AsyncMock, patch


SCRIPTS_PATH = Path(__file__).parents[1] / "scripts"
if str(SCRIPTS_PATH) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_PATH))


def load_script(module_name: str):
    script_path = SCRIPTS_PATH / f"{module_name}.py"
    spec = importlib.util.spec_from_file_location(module_name, script_path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


batch_submit = load_script("batch_submit")
quick_submit = load_script("quick_submit")


class BatchAndCompatibilityTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)
        base = Path(self.temp_dir.name)
        self.target_file = base / "target.json"
        self.target_file.write_text(
            json.dumps(
                {
                    "name": "Example Tool",
                    "url": "https://example.com",
                    "description": "A useful example tool.",
                    "email": "owner@example.com",
                }
            ),
            encoding="utf-8",
        )
        self.directories_file = base / "directories.txt"
        self.directories_file.write_text(
            "# submission forms\nhttps://directory.example/submit\n",
            encoding="utf-8",
        )
        self.batch_arguments = [
            "--target",
            str(self.target_file),
            "--directories",
            str(self.directories_file),
        ]
        self.single_arguments = [
            "--directory",
            "https://directory.example/submit",
            "--target",
            str(self.target_file),
        ]

    def test_batch_defaults_to_offline_plan(self) -> None:
        output = io.StringIO()
        fake_batch = AsyncMock()
        with patch.object(batch_submit, "submit_batch", fake_batch), redirect_stdout(output):
            exit_code = batch_submit.main(self.batch_arguments)

        self.assertEqual(exit_code, 0)
        fake_batch.assert_not_awaited()
        result = json.loads(output.getvalue())
        self.assertEqual(result["mode"], "batch-dry-run")
        self.assertEqual(result["status"], "not_submitted")

    def test_batch_submit_flag_opens_explicit_gate(self) -> None:
        fake_result = {
            "mode": "submit",
            "status": "submit_triggered",
            "directory": "https://directory.example/submit",
            "site": "https://example.com",
            "filled_fields": ["name", "url", "description", "email"],
        }
        fake_submit = AsyncMock(return_value=fake_result)
        output = io.StringIO()
        with patch.object(batch_submit, "submit_live", fake_submit), redirect_stdout(output):
            exit_code = batch_submit.main([*self.batch_arguments, "--submit"])

        self.assertEqual(exit_code, 0)
        fake_submit.assert_awaited_once()
        result = json.loads(output.getvalue())
        self.assertEqual(result["mode"], "batch-submit")
        self.assertEqual(result["status"], "submit_triggered")

    def test_compatibility_entry_defaults_to_dry_run(self) -> None:
        output = io.StringIO()
        fake_submit = AsyncMock()
        with patch.object(
            quick_submit.submit_to_directory, "submit_live", fake_submit
        ), redirect_stdout(output):
            exit_code = quick_submit.main(self.single_arguments)

        self.assertEqual(exit_code, 0)
        fake_submit.assert_not_awaited()
        self.assertEqual(json.loads(output.getvalue())["mode"], "dry-run")


if __name__ == "__main__":
    unittest.main()
