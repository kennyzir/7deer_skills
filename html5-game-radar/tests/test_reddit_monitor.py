from __future__ import annotations

from contextlib import redirect_stderr, redirect_stdout
import importlib.util
import io
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest import mock


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "reddit_monitor.py"
MONITOR_SHELL = SCRIPT.parent / "html5_monitor.sh"
SPEC = importlib.util.spec_from_file_location("reddit_monitor", SCRIPT)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class RedditMonitorTests(unittest.TestCase):
    def invoke(self, arguments: list[str]) -> tuple[int, str, str]:
        stdout = io.StringIO()
        stderr = io.StringIO()
        with redirect_stdout(stdout), redirect_stderr(stderr):
            status = MODULE.main(arguments)
        return status, stdout.getvalue(), stderr.getvalue()

    def test_missing_configuration_does_not_run_subprocess(self) -> None:
        with mock.patch.dict(os.environ, {}, clear=True), mock.patch.object(
            MODULE.subprocess, "run"
        ) as runner:
            status, stdout, stderr = self.invoke([])

        self.assertEqual(status, 2)
        self.assertEqual(stdout, "")
        self.assertIn("not configured", stderr)
        runner.assert_not_called()

    def test_nonexistent_script_does_not_run_subprocess(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory, mock.patch.object(
            MODULE.subprocess, "run"
        ) as runner:
            missing = Path(temporary_directory) / "missing.ts"
            status, _, stderr = self.invoke(["--reddit-script", str(missing)])

        self.assertEqual(status, 2)
        self.assertIn("not an existing file", stderr)
        runner.assert_not_called()

    def test_configured_script_uses_its_parent_as_cwd_and_writes_new_output(self) -> None:
        raw = (
            "⬆️ 42 New browser game | r/webgames | by u/example | 2 hours ago\n"
            "https://game.example/play\n"
        )
        with tempfile.TemporaryDirectory() as temporary_directory:
            temporary_root = Path(temporary_directory)
            script = temporary_root / "reddit-cli" / "reddit.ts"
            script.parent.mkdir()
            script.write_text("// local fixture\n", encoding="utf-8")
            output = temporary_root / "reddit.json"
            completed = subprocess.CompletedProcess([], 0, stdout=raw, stderr="")
            with mock.patch.object(
                MODULE.subprocess, "run", return_value=completed
            ) as runner:
                status, stdout, stderr = self.invoke(
                    ["--reddit-script", str(script), "--output", str(output)]
                )

            self.assertEqual(status, 0, stderr)
            self.assertEqual(stdout, "")
            self.assertEqual(len(json.loads(output.read_text(encoding="utf-8"))), 1)
            self.assertEqual(runner.call_count, 2)
            for call in runner.call_args_list:
                command = call.args[0]
                self.assertEqual(command[:3], ["npx", "--no-install", "tsx"])
                self.assertEqual(command[3], str(script.resolve()))
                self.assertEqual(call.kwargs["cwd"], str(script.parent.resolve()))

    def test_existing_output_is_not_overwritten_or_executed(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            temporary_root = Path(temporary_directory)
            script = temporary_root / "reddit.ts"
            script.write_text("// local fixture\n", encoding="utf-8")
            output = temporary_root / "reddit.json"
            output.write_text("keep\n", encoding="utf-8")
            with mock.patch.object(MODULE.subprocess, "run") as runner:
                status, _, stderr = self.invoke(
                    ["--reddit-script", str(script), "--output", str(output)]
                )

            self.assertEqual(status, 2)
            self.assertIn("refusing to overwrite", stderr)
            self.assertEqual(output.read_text(encoding="utf-8"), "keep\n")
            runner.assert_not_called()

    def test_monitor_wrapper_uses_script_relative_paths_and_explicit_output(self) -> None:
        content = MONITOR_SHELL.read_text(encoding="utf-8")
        self.assertNotIn(".openclaw/workspaces", content)
        self.assertNotIn("/tmp/reddit_output.json", content)
        self.assertIn('--output "$REDDIT_OUTPUT"', content)
        self.assertIn("HTML5_REDDIT_OUTPUT", content)


if __name__ == "__main__":
    unittest.main()
