"""Tests for the compliance-report contract-instance gate in validate_governance.

The gate (galactic-protocol.md v1.3.0 §Implementation Status) must be TRUE —
a malformed report fails — without being theater: a report shaped like the
real emitter output (scripts/compliance_report.py) passes, and an empty
directory is a note, not a failure.
"""
import contextlib
import io
import json
import tempfile
import unittest
from pathlib import Path

try:
    from scripts.validate_governance import check_compliance_reports
except ModuleNotFoundError:  # `unittest discover -s scripts` imports top-level tests.
    from validate_governance import check_compliance_reports

try:
    import jsonschema  # noqa: F401
    HAS_JSONSCHEMA = True
except ImportError:  # pragma: no cover
    HAS_JSONSCHEMA = False


def _valid_report() -> dict:
    """A report shaped exactly like scripts/compliance_report.py output."""
    return {
        "id": "cr-ix-20260721",
        "repo": "ix",
        "agent": "compliance-reporter",
        "reporting_period": {
            "from": "2026-06-21T00:00:00Z",
            "to": "2026-07-21T00:00:00Z",
        },
        "constitutional_compliance": [
            {"article": "Article 7 - Auditability", "status": "compliant"},
        ],
        "policy_compliance": [
            {"policy": "persona-requirements", "status": "compliant"},
        ],
        "violations": [],
        "overall_status": "compliant",
        "reported_at": "2026-07-21T00:00:00Z",
        "channel": "crisp",
        "message_id": "0239b368-6f61-4960-b1b0-b5ff4bcc24f8",
        "origin_repo": "ix",
        "origin_agent": "compliance-reporter",
        "content_hash": "c105b257520277a06d0e4ec09cefe464f7ab2b4bb96b02346744a508ee41e05e",
        "hash_algorithm": "sha256",
        "timestamp": "2026-07-21T00:00:00Z",
    }


def _run(reports_dir: Path) -> tuple[int, int]:
    with contextlib.redirect_stdout(io.StringIO()):
        return check_compliance_reports(reports_dir)


class ComplianceReportGateTests(unittest.TestCase):
    def test_missing_or_empty_directory_is_not_a_failure(self):
        with tempfile.TemporaryDirectory() as root:
            self.assertEqual((0, 0), _run(Path(root) / "does-not-exist"))
            self.assertEqual((0, 0), _run(Path(root)))

    @unittest.skipUnless(HAS_JSONSCHEMA, "jsonschema not installed")
    def test_valid_report_passes(self):
        with tempfile.TemporaryDirectory() as root:
            path = Path(root) / "cr-ix-20260721.json"
            path.write_text(json.dumps(_valid_report()), encoding="utf-8")
            self.assertEqual((1, 0), _run(Path(root)))

    @unittest.skipUnless(HAS_JSONSCHEMA, "jsonschema not installed")
    def test_malformed_report_fails(self):
        bad = _valid_report()
        del bad["overall_status"]           # missing required field
        bad["repo"] = "not-a-real-repo"     # enum violation
        with tempfile.TemporaryDirectory() as root:
            (Path(root) / "cr-bad.json").write_text(json.dumps(bad), encoding="utf-8")
            self.assertEqual((0, 1), _run(Path(root)))

    @unittest.skipUnless(HAS_JSONSCHEMA, "jsonschema not installed")
    def test_missing_integrity_fields_fail(self):
        bad = _valid_report()
        for field in ("message_id", "origin_repo", "origin_agent",
                      "content_hash", "hash_algorithm", "timestamp"):
            del bad[field]
        with tempfile.TemporaryDirectory() as root:
            (Path(root) / "cr-no-integrity.json").write_text(json.dumps(bad), encoding="utf-8")
            self.assertEqual((0, 1), _run(Path(root)))

    @unittest.skipUnless(HAS_JSONSCHEMA, "jsonschema not installed")
    def test_unparseable_json_fails(self):
        with tempfile.TemporaryDirectory() as root:
            (Path(root) / "cr-broken.json").write_text("{not json", encoding="utf-8")
            self.assertEqual((0, 1), _run(Path(root)))


if __name__ == "__main__":
    unittest.main()
