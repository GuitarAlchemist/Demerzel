import io
import json
import tempfile
import unittest
import unittest.mock as mock
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
import monitor_baml_and_learning as m


class TestCheckBlockersUsesSharedHaltReader(unittest.TestCase):
    """check_blockers() must decide via demerzel_halt.is_active() rather than
    re-reading + re-parsing the marker file itself, so schema/expiry/fail-safe
    semantics stay owned by the shared reader (the pre-fix version had none)."""

    def test_no_marker_passes(self):
        with tempfile.TemporaryDirectory() as d:
            stdout = io.StringIO()
            with mock.patch("sys.stdout", stdout):
                m.check_blockers(Path(d))
        self.assertIn("[PASS] No active HALT-ALL", stdout.getvalue())

    def test_active_marker_reports_reason(self):
        with tempfile.TemporaryDirectory() as d:
            (Path(d) / "HALT-ALL").write_text(json.dumps({
                "schema_version": 1,
                "halted_at": "2026-06-25T00:00:00Z",
                "halted_by": "demerzel-cli:test",
                "reason": "operator stop",
                "scope": "loops-only",
                "expires_at": None,
                "exempt_agents": [],
            }), encoding="utf-8")
            stdout = io.StringIO()
            with mock.patch("sys.stdout", stdout):
                m.check_blockers(Path(d))
        out = stdout.getvalue()
        self.assertIn("[BLOCKER]", out)
        self.assertIn("operator stop", out)

    def test_expired_marker_passes(self):
        with tempfile.TemporaryDirectory() as d:
            (Path(d) / "HALT-ALL").write_text(json.dumps({
                "schema_version": 1,
                "halted_at": "2026-06-25T00:00:00Z",
                "halted_by": "demerzel-cli:test",
                "reason": "operator stop",
                "scope": "loops-only",
                "expires_at": "2020-01-01T00:00:00Z",
                "exempt_agents": [],
            }), encoding="utf-8")
            stdout = io.StringIO()
            with mock.patch("sys.stdout", stdout):
                m.check_blockers(Path(d))
        self.assertIn("[PASS] No active HALT-ALL", stdout.getvalue())

    def test_unreadable_marker_fails_closed(self):
        with tempfile.TemporaryDirectory() as d:
            (Path(d) / "HALT-ALL").write_text("not json", encoding="utf-8")
            stdout = io.StringIO()
            with mock.patch("sys.stdout", stdout):
                m.check_blockers(Path(d))
        out = stdout.getvalue()
        self.assertIn("[BLOCKER]", out)
        self.assertIn("fail-safe", out)


if __name__ == "__main__":
    unittest.main()
