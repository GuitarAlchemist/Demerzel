#!/usr/bin/env python3
"""Regression guard for the AIW advisory lane selector (#737).

Runs under `python -m unittest discover -s scripts` (no pytest). Asserts:
  * forbidden roles are blocked (the governance boundary);
  * mode gating honors work_class (net-new blocked in DRAINING, fix survives);
  * HALTED collapses to read-only review;
  * every emitted decision validates against advisory-decision.schema.json;
  * the committed examples/aiw/*.example.md fixtures each resolve to their
    documented "Expected decision" — so the examples cannot silently rot and the
    selector cannot be unwired from its canonical policy.

String-based parsing only (no regex), per repo convention.
"""

from __future__ import annotations

import json
from pathlib import Path
import unittest

import jsonschema

from aiw_lane_selector import load_lanes, select_lane

REPO_ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = REPO_ROOT / "schemas" / "advisory-decision.schema.json"
EXAMPLES_DIR = REPO_ROOT / "examples" / "aiw"


def _extract_json_block(text):
    """Return the first ```json ... ``` fenced block in `text`, parsed."""
    marker = "```json"
    start = text.find(marker)
    if start == -1:
        raise AssertionError("no ```json block found")
    body_start = start + len(marker)
    end = text.find("```", body_start)
    if end == -1:
        raise AssertionError("unterminated ```json block")
    return json.loads(text[body_start:end])


def _extract_expected_decision(text):
    """Return the value after the 'Expected decision:' line."""
    key = "Expected decision:"
    idx = text.find(key)
    if idx == -1:
        raise AssertionError("no 'Expected decision:' line found")
    line_end = text.find("\n", idx)
    if line_end == -1:
        line_end = len(text)
    return text[idx + len(key):line_end].strip()


class LaneSelectorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.policy = load_lanes()
        with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
            cls.schema = json.load(f)

    def _decide(self, **request):
        result = select_lane(request, self.policy)
        # Every decision must be schema-valid, always.
        jsonschema.validate(result, self.schema)
        return result["rule_result"]

    def test_forbidden_role_is_blocked(self):
        # Gemini is read-only; pushing code is a forbidden governance boundary.
        r = self._decide(worker="gemini", requested_role="code_pusher",
                         fan_out_mode="NORMAL", subject="pull_request")
        self.assertEqual(r["decision"], "block")
        self.assertIn("CAPABILITY.FORBIDDEN_ROLE", r["reason_codes"])

    def test_forbidden_checked_before_mode(self):
        # Forbidden must win even when the mode would otherwise allow the class.
        r = self._decide(worker="claude", requested_role="final_merge_decider",
                         fan_out_mode="NORMAL", subject="pull_request")
        self.assertEqual(r["decision"], "block")
        self.assertIn("CAPABILITY.FORBIDDEN_ROLE", r["reason_codes"])

    def test_unknown_worker_blocked(self):
        r = self._decide(worker="skynet", requested_role="builder_fixer",
                         fan_out_mode="NORMAL", subject="worker_task")
        self.assertEqual(r["decision"], "block")
        self.assertIn("CAPABILITY.UNAVAILABLE", r["reason_codes"])

    def test_role_not_in_lane_warns(self):
        # navigator belongs to augment, not claude.
        r = self._decide(worker="claude", requested_role="navigator",
                         fan_out_mode="NORMAL", subject="worker_task")
        self.assertEqual(r["decision"], "warn")
        self.assertIn("CAPABILITY.MISMATCH", r["reason_codes"])

    def test_net_new_feature_blocked_in_draining(self):
        r = self._decide(worker="claude", requested_role="builder_fixer",
                         fan_out_mode="DRAINING", subject="pull_request")
        self.assertEqual(r["decision"], "block")
        self.assertIn("SYSTEM.BACKPRESSURE_HIGH", r["reason_codes"])

    def test_fix_survives_draining_as_fallback(self):
        r = self._decide(worker="claude", requested_role="draft_to_ready_helper",
                         fan_out_mode="DRAINING", subject="pull_request")
        self.assertEqual(r["decision"], "recommend")
        self.assertIn("LANE.SECONDARY_FALLBACK", r["reason_codes"])

    def test_primary_match_allows(self):
        r = self._decide(worker="gemini", requested_role="read_only_critic",
                         fan_out_mode="NORMAL", subject="pull_request")
        self.assertEqual(r["decision"], "allow")
        self.assertIn("LANE.PRIMARY_MATCH", r["reason_codes"])

    def test_halted_collapses_to_read_only_review(self):
        # A review role survives HALTED...
        r = self._decide(worker="gemini", requested_role="read_only_critic",
                         fan_out_mode="HALTED", subject="pull_request")
        self.assertEqual(r["decision"], "allow")
        # ...but navigation (mutation-adjacent read work) does not.
        r2 = self._decide(worker="augment", requested_role="navigator",
                          fan_out_mode="HALTED", subject="issue")
        self.assertEqual(r2["decision"], "block")

    def test_unknown_mode_escalates(self):
        r = self._decide(worker="claude", requested_role="builder_fixer",
                         fan_out_mode="TURBO", subject="worker_task")
        self.assertEqual(r["decision"], "escalate")

    def test_invalid_subject_escalates(self):
        r = self._decide(worker="claude", requested_role="builder_fixer",
                         fan_out_mode="NORMAL", subject="galaxy")
        self.assertEqual(r["decision"], "escalate")
        self.assertIn("SCOPE.UNDEFINED", r["reason_codes"])

    def test_every_lane_role_has_a_registry_entry(self):
        # Terminology reconciliation guard: every role a worker references must be
        # defined once in `roles` with a work_class the mode_blocks vocabulary knows.
        roles = self.policy["roles"]
        known_classes = set(self.policy.get("work_classes", {}))
        for name, lane in self.policy["workers"].items():
            for role in [lane["primary"]] + lane.get("secondary", []) + lane.get("forbidden", []):
                self.assertIn(role, roles, f"{name} references undefined role {role}")
                self.assertIn(roles[role]["work_class"], known_classes,
                              f"role {role} has unknown work_class")

    def test_example_fixtures_match_documented_decisions(self):
        fixtures = sorted(EXAMPLES_DIR.glob("*.example.md"))
        self.assertTrue(fixtures, "no example fixtures found — the selector would have no live consumer")
        for path in fixtures:
            text = path.read_text(encoding="utf-8")
            request = _extract_json_block(text)
            expected = _extract_expected_decision(text)
            result = self._decide(**request)
            self.assertEqual(result["decision"], expected,
                             f"{path.name}: expected {expected}, got {result['decision']}")


if __name__ == "__main__":
    unittest.main()
