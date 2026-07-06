import json
import tempfile
import unittest
import unittest.mock as mock
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
import run_ml_feedback_cycle as r
import demerzel_kit as kit

class TestRunMLFeedbackCycle(unittest.TestCase):
    def test_dry_run_does_not_write(self):
        with mock.patch("subprocess.run") as m_run, \
             mock.patch.object(r, "_halt_active", return_value=(False, "")), \
             mock.patch.object(r, "_resolve_producers", return_value={"paths": {"p": "mock"}, "notes": {}}):
            m_run.return_value = mock.Mock(returncode=0, stdout="ok", stderr="")
            rc = r.main(["--dry-run"])
            self.assertEqual(rc, 0)

    def test_halt_aborts_cycle(self):
        with mock.patch.object(r, "_halt_active", return_value=(True, "halted")), \
             mock.patch.object(r, "_resolve_producers", return_value={"paths": {"p": "mock"}, "notes": {}}):
            rc = r.main(["--dry-run"])
            self.assertEqual(rc, 3)

    def test_run_ml_feedback_writes_artifact(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            with mock.patch("subprocess.run") as m_run, \
                 mock.patch.object(r, "_halt_active", return_value=(False, "")), \
                 mock.patch.object(r, "_resolve_producers", return_value={"paths": {"confidence_calibrator": "mock"}, "notes": {}}), \
                 mock.patch.object(kit, "now_iso", return_value="2026-07-06T12:00:00Z"), \
                 mock.patch.object(kit, "write_artifact") as mock_write:

                m_run.return_value = mock.Mock(returncode=0, stdout="ok", stderr="")
                rc = r.main(["--repos-root", str(root)])
                self.assertEqual(rc, 0)
                mock_write.assert_called_once()

if __name__ == "__main__":
    unittest.main()
