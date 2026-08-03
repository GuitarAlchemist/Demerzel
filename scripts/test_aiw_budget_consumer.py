#!/usr/bin/env python3
"""Regression guard: the AIW budget gate must stay wired into a live consumer.

The budget gate (scripts/aiw_budget_gate.py) is only worth its weight if a real
provider-invocation path calls it. jules-auto-delegate.yml delegates to `jules`,
a metered-cloud provider, so it must run the gate BEFORE the Jules API call and must
not silently proceed when the gate blocks. This test fails closed if that wiring
is removed or reordered, so the "declared-but-unconsumed" gap cannot silently
return.
"""

from __future__ import annotations

import re
import unittest
from pathlib import Path


WORKFLOW = (Path(__file__).resolve().parents[1]
            / ".github" / "workflows" / "jules-auto-delegate.yml")
GATE_INVOKE = "python3 scripts/aiw_budget_gate.py"
JULES_INVOKE = "https://jules.googleapis.com/v1alpha/sessions"
FINALIZER_INVOKE = "python3 scripts/aiw_budget_gate.py --abandon-open-provider jules"
UPLOAD_ACTION = "uses: actions/upload-artifact@"
PINNED_UPLOAD_ACTION = (
    "uses: actions/upload-artifact@"
    "ea165f8d65b6e75b540449e92b4886f43607fa02")


class AiwBudgetConsumerWiringTests(unittest.TestCase):
    def setUp(self) -> None:
        self.text = WORKFLOW.read_text(encoding="utf-8")

    def test_gate_is_invoked(self) -> None:
        self.assertIn(GATE_INVOKE, self.text,
                      "jules-auto-delegate.yml must invoke the AIW budget gate")

    def test_gate_runs_before_jules_delegation(self) -> None:
        gate_at = self.text.find(GATE_INVOKE)
        action_at = self.text.find(JULES_INVOKE)
        self.assertNotEqual(gate_at, -1, "budget gate invocation is missing")
        self.assertNotEqual(action_at, -1, "Jules create-session call is missing")
        self.assertLess(gate_at, action_at,
                        "the budget gate must run before delegating to Jules")

    def test_block_is_a_governed_stop_not_a_silent_proceed(self) -> None:
        # A blocked reservation must set proceed=false so the existing
        # `if: steps.gate.outputs.proceed == 'true'` guard skips delegation.
        self.assertIn("AIW budget gate blocked jules", self.text)
        self.assertIn('echo "proceed=false" >> "$GITHUB_OUTPUT"', self.text)

    def test_invalid_request_fails_closed(self) -> None:
        # exit 2 (invalid request/policy or non-canonical path) fails the job.
        self.assertIn("failing closed", self.text)

    def test_finalizer_recovers_from_ledger_without_step_outputs(self) -> None:
        self.assertIn(FINALIZER_INVOKE, self.text)
        finalizer_at = self.text.find(FINALIZER_INVOKE)
        finalizer_step = self.text[self.text.rfind("- name:", 0, finalizer_at):finalizer_at]
        self.assertIn("if: always()", finalizer_step)
        self.assertNotIn("steps.gate.outputs.reservation_open", finalizer_step)
        self.assertNotIn("steps.gate.outputs.job_id", finalizer_step)

    def test_jules_timeout_leaves_cleanup_margin(self) -> None:
        action_at = self.text.find(JULES_INVOKE)
        record_at = self.text.find("- name: Record confirmed delegation")
        self.assertNotEqual(action_at, -1, "Jules create-session call is missing")
        action_step_at = self.text.rfind("- name:", 0, action_at)
        step_timeout = re.search(
            r"timeout-minutes:\s*(\d+)", self.text[action_step_at:record_at])
        self.assertIsNotNone(step_timeout, "Jules needs its own step timeout")
        job_header = self.text[
            self.text.find("  delegate:"):self.text.find("    steps:")]
        self.assertNotIn("timeout-minutes", job_header,
                         "a global deadline can kill the budget finalizer")

    def test_finalizer_is_guarded_and_runs_after_result_reporting(self) -> None:
        jules_at = self.text.find(JULES_INVOKE)
        record_at = self.text.find("- name: Record confirmed delegation")
        report_at = self.text.find("- name: Report failed delegation")
        finalizer_at = self.text.find(FINALIZER_INVOKE)
        self.assertNotEqual(finalizer_at, -1, "reservation finalizer is missing")
        self.assertLess(jules_at, finalizer_at)
        self.assertLess(finalizer_at, record_at,
                        "finalization must precede fallible success reporting")
        self.assertLess(finalizer_at, report_at,
                        "finalization must precede fallible failure reporting")
        finalizer_step = self.text[self.text.rfind("- name:", 0, finalizer_at):finalizer_at]
        self.assertIn("if: always()", finalizer_step)
        self.assertNotIn("continue-on-error", finalizer_step,
                         "finalization errors must keep the job red")

    def test_finalizer_never_forges_a_release_or_receipt(self) -> None:
        self.assertIn(FINALIZER_INVOKE, self.text)
        self.assertNotIn("--release-job", self.text)
        self.assertNotIn("aiw-receipt", self.text)

    def test_terminal_ledgers_are_uploaded_after_finalization(self) -> None:
        finalizer_at = self.text.find(FINALIZER_INVOKE)
        upload_at = self.text.find(UPLOAD_ACTION)
        self.assertNotEqual(upload_at, -1, "terminal ledger upload is missing")
        self.assertLess(finalizer_at, upload_at,
                        "artifact must capture the post-finalization ledger")
        upload_step = self.text[self.text.rfind("- name:", 0, upload_at):]
        self.assertIn("if: always()", upload_step)
        for ledger in (".octo/aiw-budget-ledger.json",
                       ".octo/aiw-cycle-ledger.json"):
            check_at = self.text.find(f"test -f {ledger}")
            self.assertNotEqual(check_at, -1, f"{ledger} existence is not verified")
            self.assertLess(check_at, upload_at,
                            "both ledgers must be verified before upload")

    def test_budget_artifact_is_unique_and_narrow(self) -> None:
        upload_at = self.text.find(UPLOAD_ACTION)
        self.assertNotEqual(upload_at, -1, "terminal ledger upload is missing")
        upload_step = self.text[self.text.rfind("- name:", 0, upload_at):]
        self.assertIn(PINNED_UPLOAD_ACTION, upload_step)
        self.assertIn(
            "name: aiw-budget-ledgers-${{ github.run_id }}-${{ github.run_attempt }}",
            upload_step)
        self.assertIn("include-hidden-files: true", upload_step)
        path_block = re.search(
            r"(?m)^          path: \|\n((?:            \S.*\n)+)", upload_step)
        self.assertIsNotNone(path_block, "artifact needs an explicit path list")
        self.assertEqual(
            [".octo/aiw-budget-ledger.json", ".octo/aiw-cycle-ledger.json"],
            [line.strip() for line in path_block.group(1).splitlines()],
            "artifact must contain only the two budget ledgers")
        self.assertNotRegex(upload_step, r"(?m)^\s+path:\s*\.octo/?\s*$",
                            "never publish the entire hidden .octo directory")


if __name__ == "__main__":
    unittest.main()
