from __future__ import annotations

from contextlib import redirect_stderr, redirect_stdout
import ast
import importlib.util
import io
import json
from pathlib import Path
import re
import tempfile
import unittest


SKILL_ROOT = Path(__file__).resolve().parents[1]
CONTACT_SCRIPT = SKILL_ROOT / "scripts" / "contact_discoverer.py"
EMAIL_SCRIPT = SKILL_ROOT / "scripts" / "email_generator.py"
SKILL_FILE = SKILL_ROOT / "SKILL.md"
EMAIL_LITERAL = re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.I)


def load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


CONTACTS = load_module("safe_contact_discoverer", CONTACT_SCRIPT)
EMAILS = load_module("safe_email_generator", EMAIL_SCRIPT)


def invoke(module, arguments: list[str]) -> tuple[int, str, str]:
    stdout = io.StringIO()
    stderr = io.StringIO()
    with redirect_stdout(stdout), redirect_stderr(stderr):
        status = module.main(arguments)
    return status, stdout.getvalue(), stderr.getvalue()


def write_json(path: Path, payload: object) -> None:
    path.write_text(json.dumps(payload), encoding="utf-8")


def valid_draft_input() -> dict[str, object]:
    return {
        "product": {
            "name": "Example Product",
            "url": "https://product.example",
            "tagline": "A user-provided description",
            "selling_points": ["A user-provided differentiator"],
        },
        "sender": {"name": "Your Name", "email": "your_email@example.com"},
        "contacts": [
            {
                "name": "Example Directory",
                "email": "editor@example.com",
                "source_url": "https://directory.example/contact",
                "observed_at": "2030-01-15T09:45:00Z",
                "status": "observed",
                "context": "Relevant to the supplied audience.",
            },
            {
                "name": "Unknown Candidate",
                "email": None,
                "source_url": "https://candidate.example/contact",
                "observed_at": "2030-01-15T10:00:00Z",
                "status": "unknown",
            },
        ],
    }


class SafeLinkStrategyTests(unittest.TestCase):
    def test_contact_without_capture_remains_unknown_and_does_not_guess(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            input_path = Path(temporary_directory) / "input.json"
            write_json(
                input_path,
                {
                    "opportunities": [
                        {
                            "name": "Example Directory",
                            "source_url": "https://directory.example/contact",
                        }
                    ]
                },
            )
            status, stdout, stderr = invoke(CONTACTS, ["--input", str(input_path)])

        self.assertEqual(status, 0, stderr)
        contact = json.loads(stdout)["contacts"][0]
        self.assertEqual(contact["status"], "unknown")
        self.assertIsNone(contact["observed_at"])
        self.assertEqual(contact["emails"], [])

    def test_contact_is_observed_only_with_capture_source_and_time(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            input_path = Path(temporary_directory) / "input.json"
            write_json(
                input_path,
                {
                    "opportunities": [
                        {
                            "name": "Example Directory",
                            "source_url": "https://directory.example/contact",
                            "observed_at": "2030-01-15T09:45:00Z",
                            "captured_text": "Contact editor@example.com for review.",
                        }
                    ]
                },
            )
            status, stdout, stderr = invoke(CONTACTS, ["--input", str(input_path)])

        self.assertEqual(status, 0, stderr)
        contact = json.loads(stdout)["contacts"][0]
        self.assertEqual(contact["status"], "observed")
        self.assertEqual(contact["source_url"], "https://directory.example/contact")
        self.assertEqual(contact["observed_at"], "2030-01-15T09:45:00Z")
        self.assertEqual(contact["emails"], ["editor@example.com"])

    def test_capture_without_observation_time_fails_before_output(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            temporary_root = Path(temporary_directory)
            input_path = temporary_root / "input.json"
            output = temporary_root / "contacts.json"
            write_json(
                input_path,
                {
                    "opportunities": [
                        {
                            "name": "Example Directory",
                            "source_url": "https://directory.example/contact",
                            "captured_text": "editor@example.com",
                        }
                    ]
                },
            )
            status, _, _ = invoke(
                CONTACTS, ["--input", str(input_path), "--output", str(output)]
            )

            self.assertEqual(status, 2)
            self.assertFalse(output.exists())

    def test_email_generator_uses_input_and_only_emits_not_sent_drafts(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            input_path = Path(temporary_directory) / "input.json"
            write_json(input_path, valid_draft_input())
            status, stdout, stderr = invoke(EMAILS, ["--input", str(input_path)])

        self.assertEqual(status, 0, stderr)
        result = json.loads(stdout)
        self.assertEqual(result["delivery_status"], "not-sent")
        self.assertEqual(len(result["drafts"]), 1)
        self.assertEqual(result["drafts"][0]["delivery_status"], "not-sent")
        self.assertEqual(len(result["skipped"]), 1)
        self.assertEqual(result["skipped"][0]["observed_at"], "2030-01-15T10:00:00Z")

    def test_invalid_draft_input_fails_before_output_creation(self) -> None:
        payload = valid_draft_input()
        payload["contacts"][0]["observed_at"] = None
        with tempfile.TemporaryDirectory() as temporary_directory:
            temporary_root = Path(temporary_directory)
            input_path = temporary_root / "input.json"
            output = temporary_root / "drafts.json"
            write_json(input_path, payload)
            status, _, _ = invoke(
                EMAILS, ["--input", str(input_path), "--output", str(output)]
            )

            self.assertEqual(status, 2)
            self.assertFalse(output.exists())

    def test_existing_draft_output_is_not_overwritten(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            temporary_root = Path(temporary_directory)
            input_path = temporary_root / "input.json"
            output = temporary_root / "drafts.json"
            write_json(input_path, valid_draft_input())
            output.write_text("keep\n", encoding="utf-8")
            status, _, _ = invoke(
                EMAILS, ["--input", str(input_path), "--output", str(output)]
            )

            self.assertEqual(status, 2)
            self.assertEqual(output.read_text(encoding="utf-8"), "keep\n")

    def test_public_files_have_no_real_contact_literals_or_sending_implementation(self) -> None:
        for path in (SKILL_FILE, CONTACT_SCRIPT, EMAIL_SCRIPT):
            content = path.read_text(encoding="utf-8")
            with self.subTest(path=path):
                self.assertTrue(
                    all(address.lower().endswith("@example.com") for address in EMAIL_LITERAL.findall(content))
                )
                self.assertNotIn("已验证", content)
                self.assertNotIn("PRODUCT_DB", content)
                self.assertNotIn("PLATFORM_TIERS", content)

        for path in (CONTACT_SCRIPT, EMAIL_SCRIPT):
            tree = ast.parse(path.read_text(encoding="utf-8"))
            imported = set()
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    imported.update(alias.name.split(".", 1)[0] for alias in node.names)
                elif isinstance(node, ast.ImportFrom) and node.module:
                    imported.add(node.module.split(".", 1)[0])
            functions = {
                node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)
            }
            with self.subTest(path=path):
                self.assertTrue({"smtplib", "requests", "playwright", "googleapiclient"}.isdisjoint(imported))
                self.assertFalse(any(name.startswith("send") for name in functions))


if __name__ == "__main__":
    unittest.main()
