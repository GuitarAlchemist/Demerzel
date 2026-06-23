import unittest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
import run_afk_cycle as g


class TestClassifyRisk(unittest.TestCase):
    def test_constitution_is_critical(self):
        issue = {"title": "Update Asimov constitution Article 4",
                 "body": "edit constitutions/asimov.constitution.md",
                 "labels": [{"name": "agent-implement"}]}
        risk, mode = g.classify_risk(issue)
        self.assertEqual(risk, "critical")
        self.assertEqual(mode, "per-iteration")

    def test_policy_is_critical(self):
        issue = {"title": "Refine alignment policy", "body": "tweak policies/alignment-policy.yaml",
                 "labels": []}
        self.assertEqual(g.classify_risk(issue)[0], "critical")

    def test_schema_migration_is_high(self):
        issue = {"title": "Schema migration for personas", "body": "migrate schema",
                 "labels": []}
        risk, mode = g.classify_risk(issue)
        self.assertEqual(risk, "high")
        self.assertEqual(mode, "per-iteration")

    def test_persona_is_medium(self):
        issue = {"title": "Update skeptical-auditor persona voice", "body": "persona tweak",
                 "labels": []}
        self.assertEqual(g.classify_risk(issue)[0], "medium")

    def test_docs_is_low(self):
        issue = {"title": "Fix typo in README", "body": "documentation typo", "labels": []}
        risk, mode = g.classify_risk(issue)
        self.assertEqual(risk, "low")
        self.assertEqual(mode, "boundary-only")


class TestEligibility(unittest.TestCase):
    def test_critical_not_eligible(self):
        self.assertFalse(g.is_eligible({"title": "edit constitutions/x", "body": "", "labels": []}))

    def test_low_eligible(self):
        self.assertTrue(g.is_eligible({"title": "fix docs typo", "body": "", "labels": []}))


class TestLoopState(unittest.TestCase):
    def test_loop_id_pattern_and_required_fields(self):
        issue = {"number": 42, "title": "Fix docs typo", "body": "x", "labels": []}
        st = g.build_loop_state(issue, seq=1, risk="low", mode="boundary-only", today="2026-06-22")
        self.assertRegex(st["loop_id"], r"^loop-\d{4}-\d{2}-\d{2}-\d{3}$")
        for key in ("loop_id", "goal", "repo", "risk", "governance_mode", "status", "iterations"):
            self.assertIn(key, st)
        self.assertEqual(st["repo"], "demerzel")
        self.assertIn("#42", st["goal"])


if __name__ == "__main__":
    unittest.main()
