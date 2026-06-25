import hashlib
import json
import sys
import tempfile
import unittest
import unittest.mock as mock
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import apply_ml_feedback as a
import demerzel_kit as kit


def _sign(doc: dict) -> dict:
    """Attach valid integrity fields (mirrors _verify_integrity's hash recipe) so
    the recommendation passes the §2 content_hash gate."""
    integrity_keys = {"message_id", "origin_repo", "origin_agent",
                      "content_hash", "hash_algorithm"}
    payload = {k: v for k, v in doc.items() if k not in integrity_keys}
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    doc["content_hash"] = hashlib.sha256(canonical).hexdigest()
    doc["hash_algorithm"] = "sha256"
    return doc


def _threshold_rec(message_id="ml-rec-001", confidence=0.9, nudge=0.05) -> dict:
    return _sign({
        "pipeline_id": "ml-feedback-loop",
        "recommendation_type": "threshold_adjustment",
        "recommendation": {
            "rationale": "Observed overconfidence-then-revision; nudge threshold up.",
            "parameters": {"threshold_nudge": nudge},
        },
        "confidence": confidence,
        "evidence": {"observations": 12},
        "constitutional_check": {"passed": True},
        "timestamp": "2026-06-25T00:00:00Z",
        "message_id": message_id,
        "origin_repo": "ix",
    })


class TestGate(unittest.TestCase):
    """Pure decision logic — no IO."""

    def test_high_confidence_threshold_applies(self):
        self.assertEqual(a._gate(_threshold_rec(confidence=0.9))[0], "apply")

    def test_below_governance_gate_escalates(self):
        self.assertEqual(a._gate(_threshold_rec(confidence=0.75))[0], "escalate")

    def test_below_proceed_gate_rejects(self):
        self.assertEqual(a._gate(_threshold_rec(confidence=0.5))[0], "reject")

    def test_forbidden_type_rejected(self):
        doc = _threshold_rec()
        doc["recommendation_type"] = "modify_constitution"
        self.assertEqual(a._gate(doc)[0], "reject")

    def test_integrity_tamper_detected(self):
        doc = _threshold_rec()
        doc["confidence"] = 0.91  # mutate after signing -> hash mismatch
        ok, _ = a._validate(doc)
        self.assertFalse(ok)


class TestApplySeam(unittest.TestCase):
    """End-to-end through the demerzel_kit seam: run main() with --demerzel-root
    pointed at a tmp dir, proving the applier reads the inbox and writes a
    schema-shaped belief + audit + summary to disk via kit.write_artifact —
    without hardwiring Path(__file__).parents[1]. Mirrors TestConveneSeam in
    test_council_emit.py. kit.gh_json/gh_text are patched to assert this IO path
    never touches GitHub (the applier should not, post-migration)."""

    def _seed_inbox(self, root: Path, doc: dict) -> Path:
        inbox = root / "state" / "oversight" / "ml-recommendations"
        inbox.mkdir(parents=True, exist_ok=True)
        p = inbox / f"{doc['message_id']}.json"
        p.write_text(json.dumps(doc), encoding="utf-8")
        return p

    def test_apply_writes_belief_and_processes_inbox(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            src = self._seed_inbox(root, _threshold_rec(nudge=0.05))
            with mock.patch.object(kit, "gh_json", side_effect=AssertionError("no gh")), \
                 mock.patch.object(kit, "gh_text", side_effect=AssertionError("no gh")):
                rc = a.main(["--demerzel-root", str(root)])
            self.assertEqual(rc, 0)

            belief_path = root / "state" / "beliefs" / "confidence-calibration.belief.json"
            self.assertTrue(belief_path.exists(), "belief must be written via kit.write_artifact")
            belief = json.loads(belief_path.read_text(encoding="utf-8"))
            self.assertAlmostEqual(belief["calibration"]["threshold_nudge"], 0.05)
            self.assertEqual(belief["calibration"]["prior_nudge"], 0.0)

            # audit + summary artifacts landed under the tmp root, not the repo
            audit = root / "state" / "oversight" / "ml-feedback-audit.json"
            self.assertTrue(audit.exists())
            self.assertEqual(json.loads(audit.read_text())["events"][-1]["event"],
                             "ml_recommendation_applied")

            # processed recommendation moved out of the inbox
            self.assertFalse(src.exists())
            self.assertTrue((root / "state" / "oversight" / "ml-recommendations"
                             / "processed" / src.name).exists())

    def test_dry_run_writes_nothing(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            src = self._seed_inbox(root, _threshold_rec())
            rc = a.main(["--demerzel-root", str(root), "--dry-run"])
            self.assertEqual(rc, 0)
            self.assertFalse((root / "state" / "beliefs"
                              / "confidence-calibration.belief.json").exists())
            self.assertTrue(src.exists(), "dry-run must not move the inbox file")

    def test_nudge_is_clamped_to_cap(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            self._seed_inbox(root, _threshold_rec(nudge=0.99))  # over the +/-0.10 cap
            a.main(["--demerzel-root", str(root)])
            belief = json.loads((root / "state" / "beliefs"
                                 / "confidence-calibration.belief.json").read_text())
            self.assertEqual(belief["calibration"]["threshold_nudge"], a.NUDGE_CAP)


if __name__ == "__main__":
    unittest.main()
