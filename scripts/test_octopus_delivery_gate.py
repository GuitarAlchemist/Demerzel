import json
import hashlib
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

try:
    from scripts.octopus_delivery_gate import certify, create_request
except ModuleNotFoundError:  # `unittest discover -s scripts` imports top-level tests.
    from octopus_delivery_gate import certify, create_request


FIXTURES = Path(__file__).parents[1] / "fixtures" / "octopus-delivery"


class OctopusDeliveryGateTests(unittest.TestCase):
    def test_request_fingerprint_is_bound_to_exact_git_diff(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            repo = Path(temp_dir) / "repo"
            repo.mkdir()
            subprocess.run(["git", "init", "-q", str(repo)], check=True)
            subprocess.run(
                ["git", "-C", str(repo), "config", "user.email", "test@example.com"],
                check=True,
            )
            subprocess.run(
                ["git", "-C", str(repo), "config", "user.name", "Test"],
                check=True,
            )
            tracked = repo / "reviewed.txt"
            tracked.write_text("before\n", encoding="utf-8")
            subprocess.run(["git", "-C", str(repo), "add", "reviewed.txt"], check=True)
            subprocess.run(["git", "-C", str(repo), "commit", "-qm", "base"], check=True)
            base = subprocess.run(
                ["git", "-C", str(repo), "rev-parse", "HEAD"],
                capture_output=True,
                check=True,
                text=True,
            ).stdout.strip()
            tracked.write_text("after\n", encoding="utf-8")
            subprocess.run(["git", "-C", str(repo), "commit", "-qam", "head"], check=True)
            head = subprocess.run(
                ["git", "-C", str(repo), "rev-parse", "HEAD"],
                capture_output=True,
                check=True,
                text=True,
            ).stdout.strip()
            commit_range = f"{base}..{head}"

            request_path = create_request(
                repo,
                repo / ".octo" / "runs",
                "run-test",
                "task-test",
                commit_range,
                ["claude-sonnet"],
            )

            diff = subprocess.run(
                ["git", "-C", str(repo), "diff", "--binary", "--no-ext-diff",
                 commit_range, "--"],
                capture_output=True,
                check=True,
            ).stdout
            request = json.loads(request_path.read_text(encoding="utf-8"))
            self.assertEqual(
                "sha256:" + hashlib.sha256(diff).hexdigest(),
                request["commit_fingerprint"],
            )
            self.assertTrue((request_path.parent / "providers").is_dir())

    def test_timeout_and_stale_global_results_fail_closed(self):
        run_dir = FIXTURES / "timeout-stale" / "run-20260718"

        report = certify(run_dir / "request.json", run_dir / "providers")

        self.assertEqual("BLOCKED", report["certification"])
        self.assertEqual(["claude-sonnet"], report["failed"])
        self.assertEqual(["gemini"], report["stale_rejected"])
        self.assertEqual([], report["successful"])
        self.assertEqual(
            ["claude-sonnet", "gemini"], report["missing_required"])
        self.assertEqual({}, report["scorecard"])

    def test_current_evidence_completes_without_default_scorecards(self):
        run_dir = FIXTURES / "success-current" / "run-current"

        report = certify(run_dir / "request.json", run_dir / "providers")

        self.assertEqual("COMPLETE", report["certification"])
        self.assertEqual(
            ["claude-sonnet", "gemini"], report["successful"])
        self.assertEqual({
            "reliability": "unknown",
            "security": {
                "claude-sonnet": {
                    "score": 8,
                    "finding_ids": ["SEC-1"],
                }
            },
        }, report["scorecard"])

    def test_no_diff_result_is_rejected_as_irrelevant(self):
        run_dir = FIXTURES / "irrelevant-no-diff" / "run-no-diff"

        report = certify(run_dir / "request.json", run_dir / "providers")

        self.assertEqual("BLOCKED", report["certification"])
        self.assertEqual(["claude-sonnet"], report["irrelevant_rejected"])
        self.assertEqual(["claude-sonnet"], report["missing_required"])
        self.assertEqual({}, report["scorecard"])

    def test_failed_provider_preflight_cannot_be_certified(self):
        source = FIXTURES / "success-current" / "run-current"
        with tempfile.TemporaryDirectory() as temp_dir:
            run_dir = Path(temp_dir) / "run-current"
            shutil.copytree(source, run_dir)
            result_path = run_dir / "providers" / "claude-sonnet.json"
            result = json.loads(result_path.read_text(encoding="utf-8"))
            result["preflight"] = {
                "status": "failed",
                "checks": ["claude auth precedence"],
            }
            result_path.write_text(json.dumps(result), encoding="utf-8")

            report = certify(run_dir / "request.json", run_dir / "providers")

            self.assertEqual("BLOCKED", report["certification"])
            self.assertEqual(["claude-sonnet"], report["failed"])
            self.assertEqual(["gemini"], report["successful"])

    def test_cli_writes_blocked_report_and_returns_nonzero(self):
        run_dir = FIXTURES / "timeout-stale" / "run-20260718"
        script = Path(__file__).with_name("octopus_delivery_gate.py")
        with tempfile.TemporaryDirectory() as temp_dir:
            output = Path(temp_dir) / "certification.json"

            completed = subprocess.run(
                [
                    sys.executable,
                    str(script),
                    "certify",
                    "--request",
                    str(run_dir / "request.json"),
                    "--providers-dir",
                    str(run_dir / "providers"),
                    "--output",
                    str(output),
                ],
                capture_output=True,
                check=False,
                text=True,
            )

            self.assertEqual(1, completed.returncode)
            self.assertEqual(
                "BLOCKED", json.loads(output.read_text(encoding="utf-8"))[
                    "certification"])


if __name__ == "__main__":
    unittest.main()
