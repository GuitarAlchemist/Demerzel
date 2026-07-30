"""Guard: the overseer must never report green from a stale oracle artifact.

`state/quality/<domain>/last.json` records `oracle_status`. Nothing recomputed
it, so a literal `"ok"` committed on 2026-05-16 kept the overseer reporting
`loop-eligible` for two months after the oracle actually went red (#782). The
artifact was a claim about the past being read as a fact about the present.

These tests pin the fix from both ends:

  * a fresh artifact still reaches `loop-eligible` and exit 0, so the guard is
    not vacuously red;
  * stale / missing / unparseable / undatable artifacts all fail closed —
    `oracleStatus` is never left as `ok`, the mode is never `loop-eligible`,
    and the process exits non-zero.

The exit code is asserted explicitly, not just the printed verdict: a guard
that prints red and exits 0 is the failure mode this repo keeps re-finding.
"""

import json
import os
import shutil
import subprocess
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path
from tempfile import TemporaryDirectory

ROOT = Path(__file__).resolve().parent.parent
OVERSEER = ROOT / "scripts" / "dev-process-overseer.ps1"
DOMAIN = "demerzel-harness"
PWSH = shutil.which("pwsh")

BASELINE = {
    "schema_version": 1,
    "domain": DOMAIN,
    "metric": "harness_ready",
    "primary_baseline": 1.0,
    "_harness": {"oracle_command": "pwsh scripts/verify.ps1"},
    "scope_boundary": {"allow_edit": ["**"], "protected_paths": [".env"]},
}


def _stamp(hours_ago: float) -> str:
    moment = datetime.now(timezone.utc) - timedelta(hours=hours_ago)
    return moment.strftime("%Y-%m-%dT%H:%M:%SZ")


def _last(hours_ago: float, status: str = "ok") -> dict:
    return {
        "domain": DOMAIN,
        "emitted_at": _stamp(hours_ago),
        "metric_name": "harness_ready",
        "metric_value": 1.0,
        "oracle_status": status,
        "oracle_command": "pwsh scripts/verify.ps1",
    }


class OverseerRun:
    """Result of one overseer invocation against a throwaway repo root."""

    def __init__(self, returncode: int, report: dict, stderr: str):
        self.returncode = returncode
        self.report = report
        self.stderr = stderr

    @property
    def mode(self) -> str:
        return self.report["workflowMode"]

    @property
    def domain(self) -> dict:
        domains = self.report["domains"]
        if isinstance(domains, dict):
            domains = [domains]
        return domains[0]

    @property
    def codes(self) -> list:
        findings = self.report["findings"]
        if isinstance(findings, dict):
            findings = [findings]
        return [finding["code"] for finding in findings]


@unittest.skipUnless(PWSH, "pwsh is required to exercise the overseer")
class DevProcessOverseerFreshnessTest(unittest.TestCase):
    def run_overseer(self, last_json_text: str | None) -> OverseerRun:
        with TemporaryDirectory() as temporary:
            repo = Path(temporary)
            domain_dir = repo / "state" / "quality" / DOMAIN
            domain_dir.mkdir(parents=True)
            (domain_dir / "baseline.json").write_text(
                json.dumps(BASELINE), encoding="utf-8")
            if last_json_text is not None:
                (domain_dir / "last.json").write_text(
                    last_json_text, encoding="utf-8")

            # The overseer resolves HALT-ALL under the home directory; point it
            # at the fixture so a real marker on the developer's box cannot
            # change the verdict under test.
            environment = dict(os.environ)
            environment["USERPROFILE"] = str(repo)
            environment["HOME"] = str(repo)

            completed = subprocess.run(
                [PWSH, "-NoProfile", "-File", str(OVERSEER),
                 "-RepoRoot", str(repo), "-Json", "-NoEmit"],
                capture_output=True, text=True, env=environment, check=False)

        self.assertTrue(
            completed.stdout.strip(),
            f"overseer printed no JSON; stderr={completed.stderr}")
        return OverseerRun(completed.returncode,
                           json.loads(completed.stdout),
                           completed.stderr)

    def test_fresh_artifact_is_green(self):
        run = self.run_overseer(json.dumps(_last(hours_ago=1)))
        self.assertEqual("loop-eligible", run.mode)
        self.assertEqual("ok", run.domain["oracleStatus"])
        self.assertEqual(0, run.returncode, run.stderr)

    def test_stale_ok_artifact_is_not_green(self):
        run = self.run_overseer(json.dumps(_last(hours_ago=24 * 60)))
        self.assertNotEqual("ok", run.domain["oracleStatus"])
        self.assertNotEqual("loop-eligible", run.mode)
        self.assertIn("oracle-status-stale", run.codes)
        self.assertNotEqual(0, run.returncode)

    def test_artifact_without_readable_timestamp_is_not_green(self):
        payload = _last(hours_ago=1)
        payload["emitted_at"] = "whenever"
        run = self.run_overseer(json.dumps(payload))
        self.assertNotEqual("ok", run.domain["oracleStatus"])
        self.assertNotEqual("loop-eligible", run.mode)
        self.assertIn("oracle-timestamp-unreadable", run.codes)
        self.assertNotEqual(0, run.returncode)

    def test_missing_artifact_is_not_green(self):
        run = self.run_overseer(None)
        self.assertNotEqual("loop-eligible", run.mode)
        self.assertIn("missing-oracle-output", run.codes)
        self.assertNotEqual(0, run.returncode)

    def test_unparseable_artifact_is_not_green(self):
        run = self.run_overseer('{"oracle_status": "ok",')
        self.assertNotEqual("loop-eligible", run.mode)
        self.assertIn("missing-oracle-output", run.codes)
        self.assertNotEqual(0, run.returncode)


if __name__ == "__main__":
    unittest.main()
