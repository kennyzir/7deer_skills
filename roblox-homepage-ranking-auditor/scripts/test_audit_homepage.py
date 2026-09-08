from __future__ import annotations

import importlib.util
import tempfile
import unittest
import sys
from pathlib import Path

MODULE_PATH = Path(__file__).with_name("audit_homepage.py")
SPEC = importlib.util.spec_from_file_location("audit_homepage", MODULE_PATH)
assert SPEC and SPEC.loader
AUDIT = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = AUDIT
SPEC.loader.exec_module(AUDIT)


class HomepageAuditScannerTests(unittest.TestCase):
    def analyze(self, html: str, game_name: str = "Test Game"):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "index.html"
            path.write_text(html, encoding="utf-8")
            return AUDIT.analyze_page(AUDIT.load_file(str(path)), game_name)

    def test_empty_codes_promise_is_flagged(self):
        result = self.analyze(
            """
            <html><head><title>Test Game Codes</title></head><body><main>
            <h1>Test Game Wiki</h1><h2>Active Codes</h2><p>Check back soon for rewards.</p>
            </main></body></html>
            """
        )
        codes = {item["code"] for item in result["warnings"]}
        self.assertIn("EMPTY_CODES_PROMISE_HINT", codes)

    def test_explicit_zero_code_status_is_not_flagged(self):
        result = self.analyze(
            """
            <html><body><main><h1>Test Game Wiki</h1>
            <h2>Active Codes</h2><p>There are no active codes right now.</p>
            </main></body></html>
            """
        )
        codes = {item["code"] for item in result["warnings"]}
        self.assertNotIn("EMPTY_CODES_PROMISE_HINT", codes)

    def test_generic_anchor_ratio(self):
        result = self.analyze(
            """
            <html><body><main><h1>Test Game Build Planner</h1>
            <a href='/a/'>Read more</a><a href='/b/'>Learn more</a>
            <a href='/codes/'>Current Test Game codes</a>
            </main></body></html>
            """
        )
        self.assertAlmostEqual(result["links"]["main_generic_anchor_ratio"], 2 / 3, places=3)

    def test_section_similarity_detects_substantial_overlap(self):
        repeated = " ".join(
            f"NamedMechanic{i} requires Item{i} before Level{i} and changes Route{i}."
            for i in range(1, 40)
        )
        home = [{"heading": "Progression", "text": repeated}]
        child = [{"heading": "Full Progression", "text": repeated + " extra detail"}]
        matches = AUDIT.section_similarities(home, child, "Test Game")
        self.assertTrue(matches)
        self.assertGreaterEqual(matches[0]["similarity"], 0.5)

    def test_tool_signature_similarity(self):
        html = """
        <html><body><main><h1>Test Game Build Planner</h1>
        <label for='str'>Strength</label><input id='str' name='strength' type='number'>
        <button>Calculate build</button></main></body></html>
        """
        left = self.analyze(html)["tool_signature"]
        right = self.analyze(html)["tool_signature"]
        self.assertEqual(AUDIT.tool_similarity(left, right), 1.0)


if __name__ == "__main__":
    unittest.main()
