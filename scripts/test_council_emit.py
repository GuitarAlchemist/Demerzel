import json
import tempfile
import unittest
import unittest.mock as mock
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

    def test_parse_verdict_reads_final_line_not_prose(self):
        # Prose mentions REQUEST_CHANGES while explaining options; final line approves.
        text = ("I considered whether to REQUEST_CHANGES but the change is clean.\n"
                "Verdict: APPROVE - internally consistent, low risk.")
        self.assertTrue(c.parse_verdict(text))
        self.assertEqual(c.review_from_cross_model(text, "claude", "low")["constitutional_alignment"], "pass")

    def test_parse_verdict_request_changes_line(self):
        text = "Looks fine overall.\nVerdict: REQUEST_CHANGES - missing edge case."
        self.assertFalse(c.parse_verdict(text))


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


class TestConveneSeam(unittest.TestCase):
    """End-to-end through the demerzel_kit seam: convene() with the gh reads and the
    cross-model review injected, proving the council writes a schema-valid verdict to
    disk without touching the network. This is the test the un-seamed gh calls made
    impossible before the kit migration."""

    def _fake_gh_json(self, args, **kwargs):
        if args[:2] == ["pr", "view"]:
            return {"number": 365, "title": "Add a thing", "body": "Closes #1",
                    "headRefOid": "", "labels": []}
        if args[:2] == ["issue", "view"]:
            return {"title": "Issue 1", "body": "Do the thing"}
        return None

    def _fake_gh_text(self, args, **kwargs):
        if args[:2] == ["pr", "checks"]:
            return "risk-report\tpass\thttps://example/checks"
        return ""  # diff / changed-files / api-content empty -> no file fetches

    def _convene_in(self, tmp, xmodel=("Clean.\nVerdict: APPROVE", "claude")):
        with mock.patch.object(c.kit, "gh_json", self._fake_gh_json), \
             mock.patch.object(c.kit, "gh_text", self._fake_gh_text), \
             mock.patch.object(c, "run_cross_model", return_value=xmodel), \
             mock.patch.object(c, "COUNCIL_DIR", Path(tmp)):
            return c.convene(365, classified_risk="low", write=True)

    def test_convene_writes_schema_valid_verdict_to_disk(self):
        with tempfile.TemporaryDirectory() as d:
            verdict = self._convene_in(d)
            written = Path(d) / f"{verdict['verdict_id']}.json"
            self.assertTrue(written.exists(), "verdict must be written to disk")
            on_disk = json.loads(written.read_text(encoding="utf-8"))
            self.assertEqual(on_disk["verdict_id"], verdict["verdict_id"])
            try:
                import jsonschema
            except ImportError:
                self.skipTest("jsonschema not installed")
            schema = json.loads((ROOT / "schemas" / "council-verdict.schema.json")
                                .read_text(encoding="utf-8"))
            jsonschema.validate(on_disk, schema)  # write_artifact already did; double-check

    def test_convene_two_green_reviews_approve_strictest_wins(self):
        with tempfile.TemporaryDirectory() as d:
            verdict = self._convene_in(d)
            # reviewer_a green (0.75) + reviewer_b approve (0.85) -> APPROVE, conf min=0.75
            self.assertEqual(verdict["verdict"], "APPROVE")
            self.assertEqual(len(verdict["reviews"]), 2)
            self.assertAlmostEqual(verdict["post_council_confidence"], 0.75)

    def test_convene_request_changes_when_cross_model_rejects(self):
        with tempfile.TemporaryDirectory() as d:
            verdict = self._convene_in(d, xmodel=("Bug.\nVerdict: REQUEST_CHANGES", "claude"))
            # reviewer_b constitutional fail -> REJECT under strictest-wins
            self.assertEqual(verdict["verdict"], "REJECT")


if __name__ == "__main__":
    unittest.main()
