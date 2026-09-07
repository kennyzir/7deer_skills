from __future__ import annotations

import re
import unittest
from pathlib import Path


SKILL_ROOT = Path(__file__).resolve().parents[1]
SKILL_FILE = SKILL_ROOT / "SKILL.md"
CONTRACT_FILE = SKILL_ROOT / "references" / "pipeline-contracts.md"
FORBIDDEN_TERMS = (
    "/Users/" + "zirer",
    "." + "hermes",
    "skill_" + "view",
    "delegate_" + "task",
    "browser_" + "navigate",
    "cron" + "job",
)
FORBIDDEN = re.compile("|".join(re.escape(term) for term in FORBIDDEN_TERMS), re.IGNORECASE)

STAGES = (
    "### 01 Opportunity",
    "### 02 Keywords",
    "### 03 Evidence",
    "### 04 Site plan and build",
    "### 05 SEO QA and deploy",
    "### 06 Freshness",
    "### 07 Growth",
)

ARTIFACTS = (
    "01-opportunity-report",
    "02-keyword-map",
    "03-source-ledger",
    "04-site-plan",
    "05-seo-audit",
    "06-deployment-report",
    "07-growth-backlog",
)


class PipelineDocumentationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.skill = SKILL_FILE.read_text(encoding="utf-8")
        cls.contract = CONTRACT_FILE.read_text(encoding="utf-8")

    def test_skill_stays_within_portable_size_limit(self) -> None:
        self.assertLessEqual(len(self.skill.splitlines()), 500)

    def test_active_documents_contain_no_private_paths_or_tool_bindings(self) -> None:
        for path, content in (
            (SKILL_FILE, self.skill),
            (CONTRACT_FILE, self.contract),
        ):
            with self.subTest(path=path):
                self.assertIsNone(FORBIDDEN.search(content))

    def test_all_seven_stages_have_entry_and_exit_criteria(self) -> None:
        positions = []
        for stage in STAGES:
            self.assertIn(stage, self.skill)
            positions.append(self.skill.index(stage))
        self.assertEqual(positions, sorted(positions))
        self.assertEqual(self.skill.count("**Entry criteria**"), 7)
        self.assertEqual(self.skill.count("**Exit criteria**"), 7)

    def test_all_artifacts_are_declared_in_skill_and_contract(self) -> None:
        for artifact in ARTIFACTS:
            with self.subTest(artifact=artifact):
                self.assertIn(artifact, self.skill)
                self.assertIn(artifact, self.contract)

    def test_contract_is_linked_and_defines_handoff_metadata(self) -> None:
        self.assertIn(
            "[references/pipeline-contracts.md](references/pipeline-contracts.md)",
            self.skill,
        )
        for field in (
            "status",
            "generated_at",
            "observed_through",
            "sources",
            "gaps",
            "## Handoff",
            "complete",
            "partial",
            "blocked",
        ):
            self.assertIn(field, self.contract)

    def test_evidence_policy_distinguishes_knowledge_states_and_times(self) -> None:
        for term in (
            "**Fact:**",
            "**Inference:**",
            "**Unknown:**",
            "Game codes",
            "numeric stats",
            "redemption steps",
            "generated_at",
            "observed_at",
        ):
            self.assertIn(term, self.skill)

    def test_external_side_effects_require_explicit_authorization(self) -> None:
        self.assertIn("explicit authorization", self.skill)
        for action in (
            "purchasing or registering a domain",
            "deploying or publishing a site",
            "pushing commits",
            "scheduled task",
            "sending email",
            "submitting a directory listing",
        ):
            self.assertIn(action, self.skill)
        self.assertIn("Without a real result", self.skill)

    def test_legacy_materials_are_excluded_from_default_instructions(self) -> None:
        self.assertIn("not loaded by default", self.skill)
        self.assertIn("are not current instructions", self.skill)
        self.assertTrue((SKILL_ROOT / "references" / "legacy" / "README.md").is_file())

    def test_v4_has_no_old_bundle_entry_points(self) -> None:
        self.assertNotIn("resources/", self.skill)
        self.assertIn("does not include a complete starter project", self.skill)
        for old_entry_point in (
            SKILL_ROOT / "resources" / "scripts" / "setup-site.sh",
            SKILL_ROOT / "resources" / "scripts" / "deploy.sh",
        ):
            with self.subTest(path=old_entry_point):
                self.assertFalse(old_entry_point.exists())


if __name__ == "__main__":
    unittest.main()
