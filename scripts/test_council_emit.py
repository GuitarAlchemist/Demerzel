import json
import unittest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
import council_emit as c

ROOT = Path(__file__).resolve().parents[1]


def _green_a():
    return c.review_from_blackbox("pass")


def _approve_b(risk="low"):
    return c.review_from_cross_model("Looks good.\nVerdict: APPROVE", "claude", risk)


class TestReviewBuilders(unittest.TestCase):
    def test_blackbox_green_is_pass_band(self):
        r = c.review_from_blackbox("pass")
        self.assertEqual(r["reviewer"], "reviewer_a")
        self.assertEqual(r["correctness_score"], c.SCORE_BLACKBOX_GREEN)
        self.assertEqual(r["constitutional_alignment"], "pass")

    def test_blackbox_red_requests_changes(self):
        r = c.review_from_blackbox("fail")
        self.assertEqual(r["correctness_score"], c.SCORE_BLACKBOX_RED)
        self.assertEqual(r["constitutional_alignment"], "fail")

    def test_blackbox_pending_is_none(self):
        self.assertIsNone(c.review_from_blackbox("pending"))
        self.assertIsNone(c.review_from_blackbox(None))

    def test_cross_model_approve(self):
        r = c.review_from_cross_model("fine\nVerdict: APPROVE", "gemini", "medium")
        self.assertEqual(r["correctness_score"], c.SCORE_XMODEL_APPROVE)
        self.assertEqual(r["constitutional_alignment"], "pass")

    def test_cross_model_request_changes(self):
        r = c.review_from_cross_model("issue\nVerdict: REQUEST_CHANGES", "codex", "low")
        self.assertEqual(r["correctness_score"], c.SCORE_XMODEL_REQUEST_CHANGES)
        self.assertEqual(r["constitutional_alignment"], "fail")

    def test_cross_model_none(self):
        self.assertIsNone(c.review_from_cross_model(None, None, "low"))


class TestSynthesize(unittest.TestCase):
    def test_two_approvals_approve_strictest_wins(self):
        verdict, conf, _ = c.synthesize([_green_a(), _approve_b()])
        self.assertEqual(verdict, "APPROVE")
        # min(0.75, 0.85) = 0.75
        self.assertAlmostEqual(conf, 0.75)

    def test_red_a_rejects(self):
        verdict, conf, _ = c.synthesize([c.review_from_blackbox("fail"), _approve_b()])
        self.assertEqual(verdict, "REJECT")  # a constitutional fail present
        self.assertAlmostEqual(conf, c.SCORE_BLACKBOX_RED)

    def test_request_changes_b_below_threshold(self):
        rb = c.review_from_cross_model("Verdict: REQUEST_CHANGES", "claude", "low")
        verdict, conf, _ = c.synthesize([_green_a(), rb])
        self.assertEqual(verdict, "REJECT")  # rb alignment fail -> reject
        self.assertAlmostEqual(conf, c.SCORE_XMODEL_REQUEST_CHANGES)

    def test_empty_is_reject(self):
        verdict, conf, _ = c.synthesize([])
        self.assertEqual(verdict, "REJECT")
        self.assertEqual(conf, 0.0)


class TestBuildVerdictSchema(unittest.TestCase):
    def _schema(self):
        return json.loads((ROOT / "schemas" / "council-verdict.schema.json").read_text(encoding="utf-8"))

    def test_verdict_id_pattern_and_required_fields(self):
        v = c.build_verdict(365, "Some change", [_green_a(), _approve_b()], "2026-06-23", 1)
        self.assertRegex(v["verdict_id"], r"^council-\d{4}-\d{2}-\d{2}-\d{3}$")
        schema = self._schema()
        for key in schema["required"]:
            self.assertIn(key, v, f"missing required field {key}")
        self.assertIn(v["trigger_condition"], ["high_risk_self_merge", "borderline_confidence"])
        self.assertIn(v["verdict"], ["APPROVE", "REQUEST_CHANGES", "REJECT"])
        for rev in v["reviews"]:
            self.assertIn(rev["reviewer"], ["reviewer_a", "reviewer_b"])
            self.assertGreaterEqual(rev["correctness_score"], 0.0)
            self.assertLessEqual(rev["correctness_score"], 1.0)

    def test_jsonschema_validates_when_available(self):
        try:
            import jsonschema
        except ImportError:
            self.skipTest("jsonschema not installed")
        v = c.build_verdict(365, "Some change", [_green_a(), _approve_b()], "2026-06-23", 2)
        jsonschema.validate(v, self._schema())


if __name__ == "__main__":
    unittest.main()
