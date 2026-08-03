import json
import io
import tempfile
import unittest
import unittest.mock as mock
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
import demerzel_halt as h

ROOT = Path(__file__).resolve().parents[1]


def _halt_args(**over):
    base = dict(reason="Investigating cost burn", halted_by=None, scope=h.DEFAULT_SCOPE,
                expires_at=None, exempt_agents=None, incident_url=None, issue_ref=None)
    base.update(over)
    return mock.Mock(**base)


class TestValidate(unittest.TestCase):
    def test_valid_marker_has_no_errors(self):
        marker = {
            "schema_version": h.SCHEMA_VERSION,
            "halted_at": "2026-06-25T00:00:00Z",
            "halted_by": "demerzel-cli:test",
            "reason": "stop",
            "scope": h.DEFAULT_SCOPE,
            "expires_at": None,
            "exempt_agents": [],
        }
        self.assertEqual(h.validate(marker), [])

    def test_bad_scope_is_rejected(self):
        marker = {
            "schema_version": h.SCHEMA_VERSION,
            "halted_at": "2026-06-25T00:00:00Z",
            "halted_by": "demerzel-cli:test",
            "reason": "stop",
            "scope": "not-a-scope",
            "expires_at": None,
            "exempt_agents": [],
        }
        self.assertTrue(h.validate(marker))


class TestHaltSeam(unittest.TestCase):
    """End-to-end through the demerzel_kit seam: cmd_halt() with marker_path pointed
    at a tmp dir and kit.now_iso stubbed, proving the script writes a schema-valid
    marker to disk via kit.atomic_write without touching the real ~/.demerzel."""

    def _halt_in(self, tmp, **over):
        target = Path(tmp) / "HALT-ALL"
        with mock.patch.object(h, "marker_path", return_value=target), \
             mock.patch.object(h.kit, "now_iso", return_value="2026-06-25T12:00:00Z"):
            rc = h.cmd_halt(_halt_args(**over))
        return rc, target

    def test_halt_writes_schema_valid_marker_to_disk(self):
        with tempfile.TemporaryDirectory() as d:
            rc, target = self._halt_in(d)
            self.assertEqual(rc, 0)
            self.assertTrue(target.exists(), "marker must be written to disk")
            marker = json.loads(target.read_text(encoding="utf-8"))
            self.assertEqual(marker["halted_at"], "2026-06-25T12:00:00Z")  # uses kit.now_iso
            self.assertEqual(marker["reason"], "Investigating cost burn")
            self.assertEqual(h.validate(marker), [])
            try:
                import jsonschema
            except ImportError:
                self.skipTest("jsonschema not installed")
            schema = json.loads((ROOT / "schemas" / "halt-all.schema.json")
                                .read_text(encoding="utf-8"))
            jsonschema.validate(marker, schema)

    def test_invalid_marker_is_not_written(self):
        with tempfile.TemporaryDirectory() as d:
            rc, target = self._halt_in(d, scope="not-a-scope")
            self.assertEqual(rc, 2)  # schema-validation failure
            self.assertFalse(target.exists(), "invalid marker must never reach disk")

    def test_status_uses_fail_closed_shared_reader(self):
        with tempfile.TemporaryDirectory() as d:
            target = Path(d) / "HALT-ALL"
            target.write_text('{"expires_at":"2020-01-01T00:00:00Z"}', encoding="utf-8")
            stderr = io.StringIO()
            with mock.patch.object(h, "marker_path", return_value=target), \
                 mock.patch("sys.stderr", stderr):
                rc = h.cmd_status(mock.Mock())
        self.assertEqual(rc, 0)
        self.assertIn("halt_all_invalid", stderr.getvalue())


if __name__ == "__main__":
    unittest.main()
