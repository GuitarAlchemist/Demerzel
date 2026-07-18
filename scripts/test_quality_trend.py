import json
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

try:
    from scripts.quality_trend import build_rows
    from scripts.quality_trend_freshness import evaluate, sync_alert
except ModuleNotFoundError:  # `unittest discover -s scripts` imports top-level tests.
    from quality_trend import build_rows
    from quality_trend_freshness import evaluate, sync_alert


NOW = datetime(2026, 7, 18, 13, tzinfo=timezone.utc)


class QualityTrendTests(unittest.TestCase):
    def test_build_rows_carries_forward_absolute_baseline(self):
        with tempfile.TemporaryDirectory() as root:
            evolution = Path(root) / "evolution"
            output = Path(root) / "quality"
            evolution.mkdir()
            output.mkdir()
            (evolution / "sample.evolution.json").write_text(json.dumps({
                "artifact": "sample",
                "created_at": "2026-07-01T00:00:00Z",
                "metrics": {
                    "citation_count": 5,
                    "violation_count": 1,
                    "compliance_rate": 0.8,
                },
                "assessment": {"effectiveness": {"truth_value": "T"}},
            }), encoding="utf-8")
            (output / "2026-06.jsonl").write_text(json.dumps({
                "artifact": "sample",
                "citation_count": 3,
                "violation_count": 0,
                "compliance_rate": 0.5,
                "effectiveness_to": "U",
            }) + "\n", encoding="utf-8")

            row = build_rows(str(evolution), str(output), NOW)[0]

            self.assertEqual(2, row["delta_citations"])
            self.assertEqual(1, row["delta_violations"])
            self.assertAlmostEqual(0.3, row["delta_compliance"])
            self.assertEqual("U", row["effectiveness_from"])
            self.assertEqual("T", row["effectiveness_to"])


class QualityTrendFreshnessTests(unittest.TestCase):
    def _write_evidence(self, root: str, timestamp: datetime) -> None:
        path = Path(root) / "2026-07.jsonl"
        path.write_text(
            json.dumps({"timestamp": timestamp.isoformat()}) + "\n",
            encoding="utf-8")

    def test_exact_threshold_is_fresh_but_fraction_over_is_stale(self):
        with tempfile.TemporaryDirectory() as root:
            self._write_evidence(root, NOW - timedelta(days=3))
            self.assertFalse(evaluate(root, NOW, 3)["stale"])

            self._write_evidence(root, NOW - timedelta(days=3, seconds=1))
            self.assertTrue(evaluate(root, NOW, 3)["stale"])

    def test_malformed_or_missing_evidence_fails_closed(self):
        with tempfile.TemporaryDirectory() as root:
            (Path(root) / "2026-07.jsonl").write_text(
                "not-json\n{\"timestamp\": \"not-a-date\"}\n", encoding="utf-8")
            result = evaluate(root, NOW, 3)
            self.assertTrue(result["stale"])
            self.assertIsNone(result["age_days"])

    def test_stale_alert_is_created_then_removed_on_recovery(self):
        with tempfile.TemporaryDirectory() as root:
            alert = Path(root) / ".freshness-alert.json"
            stale = {"stale": True, "age_days": 4, "reason": "stale"}
            sync_alert(stale, alert, NOW, 3)
            self.assertTrue(alert.exists())
            self.assertEqual("quality-trend-stale", json.loads(
                alert.read_text(encoding="utf-8"))["alert"])

            sync_alert({"stale": False, "age_days": 0, "reason": "fresh"},
                       alert, NOW, 3)
            self.assertFalse(alert.exists())


if __name__ == "__main__":
    unittest.main()
