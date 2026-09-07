from __future__ import annotations

import json
from pathlib import Path
import re
import subprocess
import sys
import unittest
from urllib.parse import unquote, urlsplit

import yaml


REPO_ROOT = Path(__file__).resolve().parents[1]
CATALOG_CONFIG = REPO_ROOT / "catalog.json"
CATALOG_DOCUMENT = REPO_ROOT / "CATALOG.md"
README = REPO_ROOT / "README.md"
GENERATOR = REPO_ROOT / "scripts" / "generate_catalog.py"
EXPECTED_CI_TESTS = {
    "roblox-hit-evaluator": 47,
    "roblox-site-architect": 17,
    "multi-game-codes-hub": 8,
    "seo-backlink-submitter": 7,
    "signallayer-backlinks-client": 6,
}
EXPECTED_SAFETY_CHECKS = {
    "html5-game-radar": 5,
    "seo-link-strategy": 7,
}
ARTIFACTS = (
    "01-opportunity-report.md",
    "02-keyword-map.md",
    "03-source-ledger.md",
    "04-site-plan.md",
    "05-seo-audit.md",
    "06-deployment-report.md",
    "07-growth-backlog.md",
)
MARKDOWN_LINK = re.compile(r"!?\[[^\]\n]*\]\(([^)\n]+)\)")


def frontmatter(skill_file: Path) -> dict[str, object]:
    text = skill_file.read_text(encoding="utf-8")
    end = text.find("\n---\n", 4)
    return yaml.safe_load(text[4:end])


class CatalogTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.config = json.loads(CATALOG_CONFIG.read_text(encoding="utf-8"))
        cls.entries = [
            entry for group in cls.config["groups"] for entry in group["skills"]
        ]
        cls.readme = README.read_text(encoding="utf-8")
        cls.catalog = CATALOG_DOCUMENT.read_text(encoding="utf-8")

    def test_catalog_covers_every_top_level_skill_exactly_once(self) -> None:
        actual = {
            frontmatter(path)["name"] for path in sorted(REPO_ROOT.glob("*/SKILL.md"))
        }
        configured = [entry["name"] for entry in self.entries]
        self.assertEqual(len(actual), 32)
        self.assertEqual(len(configured), len(set(configured)))
        self.assertEqual(set(configured), actual)

    def test_catalog_separates_behavior_and_safety_maturity(self) -> None:
        tested = {
            entry["name"]: entry["ci_tests"]
            for entry in self.entries
            if entry["maturity"] == "ci-tested"
        }
        self.assertEqual(tested, EXPECTED_CI_TESTS)
        self.assertEqual(sum(tested.values()), 85)
        for entry in self.entries:
            if entry["name"] not in EXPECTED_CI_TESTS:
                self.assertNotIn("ci_tests", entry)
        safety_checked = {
            entry["name"]: entry["ci_checks"]
            for entry in self.entries
            if entry["maturity"] == "safety-checked"
        }
        self.assertEqual(safety_checked, EXPECTED_SAFETY_CHECKS)
        self.assertEqual(sum(safety_checked.values()), 12)
        untested = [
            entry for entry in self.entries if entry["maturity"] == "not-ci-tested"
        ]
        self.assertEqual(len(untested), 25)
        for entry in untested:
            self.assertNotIn("ci_tests", entry)
            self.assertNotIn("ci_checks", entry)
        self.assertIn(
            "当前五个明确标记的技能在 CI 中共运行 85 个行为测试",
            self.readme,
        )

    def test_generated_catalog_has_no_drift(self) -> None:
        result = subprocess.run(
            [sys.executable, str(GENERATOR), "--check"],
            cwd=REPO_ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_catalog_descriptions_come_from_skill_frontmatter(self) -> None:
        for skill_file in sorted(REPO_ROOT.glob("*/SKILL.md")):
            metadata = frontmatter(skill_file)
            description = " ".join(str(metadata["description"]).split()).replace(
                "|", "\\|"
            )
            with self.subTest(skill=metadata["name"]):
                self.assertIn(description, self.catalog)

    def test_readme_uses_verified_install_path_and_pipeline_artifacts(self) -> None:
        self.assertFalse(self.readme.startswith("\ufeff"))
        self.assertIn(".agents/skills", self.readme)
        self.assertNotIn(".agent/skills", self.readme)
        self.assertNotIn("使用示例", self.readme)
        self.assertIn("Proof, not promises", self.readme)
        self.assertIn("85", self.readme)
        for artifact in ARTIFACTS:
            self.assertIn(artifact, self.readme)

    def test_readme_keeps_customer_value_and_single_star_cta(self) -> None:
        for outcome in (
            "不想凭感觉选游戏",
            "避免关键词、证据、页面、上线和外链各自断裂",
            "可恢复、可复盘",
        ):
            self.assertIn(outcome, self.readme)
        star_cta_lines = [
            line
            for line in self.readme.splitlines()
            if "stargazers" in line and "持续更新" in line and "独立站开发者" in line
        ]
        self.assertEqual(len(star_cta_lines), 1)

    def test_readme_states_concrete_rb_auto_boundary(self) -> None:
        for boundary in ("私有 Agent 工具源码", "操作说明", "首站陪跑"):
            self.assertIn(boundary, self.readme)
        self.assertIn("已经使用 AI/Codex 做站", self.readme)
        self.assertIn("基于真实数据持续运营", self.readme)
        self.assertIn("不承诺搜索排名、流量或收入", self.readme)

    def test_readme_does_not_regress_to_examples_or_directory_tree(self) -> None:
        self.assertNotIn("使用示例", self.readme)
        self.assertNotRegex(self.readme, r"[├└]──")
        headings = [line.casefold() for line in self.readme.splitlines() if line.startswith("#")]
        self.assertFalse(
            any("目录结构" in heading or "repository structure" in heading for heading in headings)
        )
        self.assertLessEqual(len(self.readme.splitlines()), 125)

    def test_relative_readme_and_catalog_links_exist(self) -> None:
        for document in (README, CATALOG_DOCUMENT):
            content = document.read_text(encoding="utf-8")
            for raw_target in MARKDOWN_LINK.findall(content):
                target = raw_target.strip().split(maxsplit=1)[0]
                parsed = urlsplit(target)
                if parsed.scheme or target.startswith(("#", "mailto:")):
                    continue
                relative = unquote(parsed.path).removeprefix("./")
                with self.subTest(document=document.name, target=target):
                    self.assertTrue((REPO_ROOT / relative).exists())


if __name__ == "__main__":
    unittest.main()
