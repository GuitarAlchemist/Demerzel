import json
import subprocess
import sys
import tempfile
import unittest
import unittest.mock as mock
from datetime import datetime, timezone
from pathlib import Path
from types import SimpleNamespace

sys.path.insert(0, str(Path(__file__).resolve().parent))
import demerzel_kit as kit


def _proc(returncode=0, stdout="", stderr=""):
    """A CompletedProcess-shaped stand-in for an injected gh runner."""
    return SimpleNamespace(returncode=returncode, stdout=stdout, stderr=stderr)


class TestPrimitives(unittest.TestCase):
    def test_now_iso_is_utc_rfc3339(self):
        self.assertRegex(kit.now_iso(), r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")

    def test_atomic_write_creates_parents_and_content(self):
        with tempfile.TemporaryDirectory() as d:
            target = Path(d) / "nested" / "deep" / "out.json"
            kit.atomic_write(target, '{"ok": true}')
            self.assertEqual(target.read_text(encoding="utf-8"), '{"ok": true}')
            # the temp sibling must not survive a successful write
            self.assertFalse((target.with_suffix(".json.tmp")).exists())


class TestValidate(unittest.TestCase):
    def test_invalid_data_raises(self):
        try:
            import jsonschema
        except ImportError:
            self.skipTest("jsonschema not installed")
        # empty object is missing every required council-verdict field
        with self.assertRaises(jsonschema.ValidationError):
            kit.validate({}, "council-verdict")

    def test_absent_jsonschema_degrades(self):
        # Simulate jsonschema being unavailable: validate must return, not raise.
        real = sys.modules.get("jsonschema")
        sys.modules["jsonschema"] = None  # forces `import jsonschema` to ImportError
        try:
            kit.validate({}, "council-verdict")  # would raise if it actually validated
        finally:
            if real is not None:
                sys.modules["jsonschema"] = real
            else:
                sys.modules.pop("jsonschema", None)


class TestHaltState(unittest.TestCase):
    NOW = datetime(2026, 8, 3, tzinfo=timezone.utc)

    @staticmethod
    def _write(path, **overrides):
        marker = {
            "schema_version": 1,
            "halted_at": "2026-08-03T00:00:00Z",
            "reason": "operator stop",
            **overrides,
        }
        path.write_text(json.dumps(marker), encoding="utf-8")

    def test_absent_is_inactive(self):
        with tempfile.TemporaryDirectory() as d:
            state = kit.halt_state(Path(d) / "HALT-ALL", self.NOW)
        self.assertEqual(
            state,
            {"present": False, "valid": True, "active": False,
             "reason": None, "errors": None, "marker": None},
        )

    def test_valid_marker_is_active_until_expiry(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "HALT-ALL"
            self._write(path, expires_at="2026-08-03T01:00:00Z")
            active = kit.halt_state(path, self.NOW)
            self._write(path, expires_at="2026-08-02T23:00:00Z")
            expired = kit.halt_state(path, self.NOW)
        self.assertTrue(active["valid"])
        self.assertTrue(active["active"])
        self.assertFalse(expired["active"])

    def test_unreadable_invalid_and_unvalidated_markers_fail_closed(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "HALT-ALL"
            path.write_text("{", encoding="utf-8")
            unreadable = kit.halt_state(path, self.NOW)

            path.write_bytes(b"\xff")
            invalid_encoding = kit.halt_state(path, self.NOW)

            path.write_text('{"schema_version": 1}', encoding="utf-8")
            invalid = kit.halt_state(path, self.NOW)

            self._write(path)
            real = sys.modules.get("jsonschema")
            sys.modules["jsonschema"] = None
            try:
                unvalidated = kit.halt_state(path, self.NOW)
            finally:
                if real is not None:
                    sys.modules["jsonschema"] = real
                else:
                    sys.modules.pop("jsonschema", None)

        for state in (unreadable, invalid_encoding, invalid, unvalidated):
            with self.subTest(reason=state["reason"]):
                self.assertTrue(state["present"])
                self.assertFalse(state["valid"])
                self.assertTrue(state["active"])
                self.assertIsNotNone(state["errors"])

    def test_read_error_fails_closed(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "HALT-ALL"
            self._write(path)
            with mock.patch.object(Path, "read_text", side_effect=OSError("denied")):
                state = kit.halt_state(path, self.NOW)
        self.assertFalse(state["valid"])
        self.assertTrue(state["active"])
        self.assertIn("denied", state["errors"])


class TestWriteArtifact(unittest.TestCase):
    def test_writes_pretty_json_with_newline(self):
        with tempfile.TemporaryDirectory() as d:
            out = Path(d) / "a.json"
            kit.write_artifact(out, {"b": 1, "a": 2})
            text = out.read_text(encoding="utf-8")
            self.assertTrue(text.endswith("\n"))
            self.assertEqual(json.loads(text), {"b": 1, "a": 2})

    def test_invalid_against_schema_does_not_write(self):
        try:
            import jsonschema  # noqa: F401
        except ImportError:
            self.skipTest("jsonschema not installed")
        with tempfile.TemporaryDirectory() as d:
            out = Path(d) / "bad.json"
            with self.assertRaises(Exception):
                kit.write_artifact(out, {}, schema="council-verdict")
            self.assertFalse(out.exists(), "invalid artifact must never reach disk")


class TestGhSeam(unittest.TestCase):
    def test_gh_json_parses_stdout(self):
        out = kit.gh_json(["pr", "view", "1"], run=lambda *a, **k: _proc(stdout='{"number": 1}'))
        self.assertEqual(out, {"number": 1})

    def test_gh_json_none_on_nonzero(self):
        self.assertIsNone(kit.gh_json(["x"], run=lambda *a, **k: _proc(returncode=1, stderr="boom")))

    def test_gh_json_none_on_unavailable(self):
        def boom(*a, **k):
            raise OSError("gh not found")
        self.assertIsNone(kit.gh_json(["x"], run=boom))

    def test_gh_json_none_on_non_json(self):
        self.assertIsNone(kit.gh_json(["x"], run=lambda *a, **k: _proc(stdout="not json")))

    def test_gh_text_returns_stdout(self):
        self.assertEqual(kit.gh_text(["pr", "diff", "1"], run=lambda *a, **k: _proc(stdout="DIFF")), "DIFF")

    def test_gh_text_ok_nonzero_keeps_stdout(self):
        # gh pr checks exits non-zero when a check failed, but the table is valid.
        run = lambda *a, **k: _proc(returncode=1, stdout="risk-report\tfail\t")
        self.assertEqual(kit.gh_text(["pr", "checks", "1"], ok_nonzero=True, run=run),
                         "risk-report\tfail\t")

    def test_gh_text_none_on_nonzero_by_default(self):
        self.assertIsNone(kit.gh_text(["x"], run=lambda *a, **k: _proc(returncode=1)))


if __name__ == "__main__":
    unittest.main()
