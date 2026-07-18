#!/usr/bin/env python3
"""Regression guard: the AIW budget gate must stay wired into a live consumer.

The budget gate (scripts/aiw_budget_gate.py) is only worth its weight if a real
provider-invocation path calls it. jules-auto-delegate.yml delegates to `jules`,
a metered-cloud provider, so it must run the gate BEFORE the Jules action and must
not silently proceed when the gate blocks. This test fails closed if that wiring
is removed or reordered, so the "declared-but-unconsumed" gap cannot silently
return.
"""

from __future__ import annotations

import unittest
from pathlib import Path


WORKFLOW = (Path(__file__).resolve().parents[1]
            / ".github" / "workflows" / "jules-auto-delegate.yml")
GATE_INVOKE = "python3 scripts/aiw_budget_gate.py"
JULES_ACTION = "uses: google-labs-code/jules-action"


class AiwBudgetConsumerWiringTests(unittest.TestCase):
    def setUp(self) -> None:
        self.text = WORKFLOW.read_text(encoding="utf-8")

    def test_gate_is_invoked(self) -> None:
        self.assertIn(GATE_INVOKE, self.text,
                      "jules-auto-delegate.yml must invoke the AIW budget gate")

    def test_gate_runs_before_jules_delegation(self) -> None:
        gate_at = self.text.find(GATE_INVOKE)
        action_at = self.text.find(JULES_ACTION)
        self.assertNotEqual(gate_at, -1, "budget gate invocation is missing")
        self.assertNotEqual(action_at, -1, "jules-action step is missing")
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


if __name__ == "__main__":
    unittest.main()
