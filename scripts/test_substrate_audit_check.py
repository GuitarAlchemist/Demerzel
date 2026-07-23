"""Unit tests for substrate_audit_check — the substrate-audit comparison core.

Fixture-driven: no hari, no hari-core, no network. Exercises slug parity with
the projector, the classification of each divergence class, and the end-to-end
exit code through main() against an in-memory report + tmp belief files.
"""

import io
import json
import tempfile
import unittest
import unittest.mock as mock
from contextlib import redirect_stdout
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
import substrate_audit_check as sac


class TestSlug(unittest.TestCase):
    def test_strips_leading_date_prefix(self):
        self.assertEqual(sac.slug("2026-03-17-behavioral-test-coverage"), "demerzel/behavioral-test-coverage")

    def test_no_date_prefix_left_intact(self):
        self.assertEqual(sac.slug("confidence-calibration"), "demerzel/confidence-calibration")

    def test_non_date_leading_hyphens_not_stripped(self):
        # "consumer-repo-integration-status" has >3 parts but part 0 is not a digit.
        self.assertEqual(
            sac.slug("consumer-repo-integration-status"), "demerzel/consumer-repo-integration-status"
        )


class TestClassify(unittest.TestCase):
    def test_agree_same_value(self):
        self.assertEqual(sac.classify("T", "True"), "agree")
        self.assertEqual(sac.classify("P", "Probable"), "agree")

    def test_trigger_affirmative_vs_contradictory(self):
        # The measured failure mode: hand T/P, substrate Contradictory.
        self.assertEqual(sac.classify("T", "Contradictory"), "trigger")
        self.assertEqual(sac.classify("P", "Contradictory"), "trigger")

    def test_within_chain_strength_diff_is_divergence_not_trigger(self):
        # confidence-calibration's known v0 mapping artifact: hand P, substrate True.
        self.assertEqual(sac.classify("P", "True"), "divergence")
        self.assertEqual(sac.classify("T", "Probable"), "divergence")

    def test_negative_or_unknown_vs_contradictory_warns_not_fails(self):
        # Not false confidence -> divergence (WARN), not a trigger (FAIL).
        self.assertEqual(sac.classify("F", "Contradictory"), "divergence")
        self.assertEqual(sac.classify("D", "Contradictory"), "divergence")
        self.assertEqual(sac.classify("U", "Contradictory"), "divergence")

    def test_no_opinion_when_substrate_absent(self):
        self.assertEqual(sac.classify("T", None), "no-opinion")


class TestAudit(unittest.TestCase):
    def test_records_match_the_2026_07_20_live_snapshot(self):
        beliefs = [
            ("2026-03-17-behavioral-test-coverage.belief.json", "T"),
            ("2026-03-17-demerzel-framework-integrity.belief.json", "T"),
            ("2026-03-18-consumer-repo-integration-status.belief.json", "T"),
            ("confidence-calibration.belief.json", "P"),
            ("remediation-effectiveness.belief.json", "P"),
            ("empty-placeholder.belief.json", "U"),  # projector skipped: no evidence
        ]
        final_beliefs = {
            "demerzel/behavioral-test-coverage": "Contradictory",
            "demerzel/demerzel-framework-integrity": "True",
            "demerzel/consumer-repo-integration-status": "True",
            "demerzel/confidence-calibration": "True",
            "demerzel/remediation-effectiveness": "Probable",
        }
        by_slug = {r["slug"]: r for r in sac.audit(beliefs, final_beliefs)}
        self.assertEqual(by_slug["demerzel/behavioral-test-coverage"]["status"], "trigger")
        self.assertEqual(by_slug["demerzel/confidence-calibration"]["status"], "divergence")
        self.assertEqual(by_slug["demerzel/demerzel-framework-integrity"]["status"], "agree")
        self.assertEqual(by_slug["demerzel/consumer-repo-integration-status"]["status"], "agree")
        self.assertEqual(by_slug["demerzel/remediation-effectiveness"]["status"], "agree")
        self.assertEqual(by_slug["demerzel/empty-placeholder"]["status"], "no-opinion")


class TestMainExit(unittest.TestCase):
    def _run(self, beliefs, final_beliefs):
        """Write belief files + report to a tmp dir, run main(), capture (rc, stdout)."""
        with tempfile.TemporaryDirectory() as d:
            bdir = Path(d) / "beliefs"
            bdir.mkdir()
            for name, tv in beliefs:
                (bdir / name).write_text(json.dumps({"truth_value": tv, "evidence": {}}), encoding="utf-8")
            report = Path(d) / "report.json"
            report.write_text(json.dumps({"final_beliefs": final_beliefs}), encoding="utf-8")
            buf = io.StringIO()
            with redirect_stdout(buf):
                rc = sac.main(["--report", str(report), "--beliefs-dir", str(bdir)])
            return rc, buf.getvalue()

    def test_trigger_exits_nonzero_and_emits_error(self):
        rc, out = self._run(
            [("2026-03-17-behavioral-test-coverage.belief.json", "T")],
            {"demerzel/behavioral-test-coverage": "Contradictory"},
        )
        self.assertEqual(rc, 1)
        self.assertIn("::error::", out)
        self.assertIn("re-evaluation trigger", out)

    def test_benign_divergence_warns_but_passes(self):
        rc, out = self._run(
            [("confidence-calibration.belief.json", "P")],
            {"demerzel/confidence-calibration": "True"},
        )
        self.assertEqual(rc, 0)
        self.assertIn("::warning", out)
        self.assertNotIn("::error::", out)

    def test_all_agree_is_clean_pass(self):
        rc, out = self._run(
            [("2026-03-17-demerzel-framework-integrity.belief.json", "T")],
            {"demerzel/demerzel-framework-integrity": "True"},
        )
        self.assertEqual(rc, 0)
        self.assertNotIn("::warning", out)
        self.assertNotIn("::error::", out)

    def test_missing_final_beliefs_is_usage_error(self):
        with tempfile.TemporaryDirectory() as d:
            report = Path(d) / "report.json"
            report.write_text(json.dumps({"event_count": 0}), encoding="utf-8")
            buf = io.StringIO()
            with redirect_stdout(buf):
                rc = sac.main(["--report", str(report), "--beliefs-dir", d])
            self.assertEqual(rc, 2)


if __name__ == "__main__":
    unittest.main()
