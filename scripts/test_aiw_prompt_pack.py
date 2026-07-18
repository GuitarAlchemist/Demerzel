#!/usr/bin/env python3
"""Unittest suite for the AIW prompt-pack + harness execution rules (issue #648).

Runs under the repo's `python -m unittest discover -s scripts` harness (no pytest).
"""

from __future__ import annotations

import json
import os
from pathlib import Path
import tempfile
import unittest

from aiw_prompt_pack import PromptPack, generate_prompt, check_harness_execution_rules


REPO_ROOT = Path(__file__).resolve().parents[1]
EXAMPLE = REPO_ROOT / "examples" / "aiw-harness-result.example.json"

VALID_TEMPLATE = """
## Role
## Task
## Source of truth
## Context bundle
## Allowed scope
## Non-goals
## Constraints
## Required process
## Required outputs
## Stop conditions

You are acting as: <provider-role>.
Issue: <issue-url-or-number>
Allowed paths: <path>
"""

INVALID_TEMPLATE = """
## Role
## Task
## Source of truth
## Context bundle
## Allowed scope
## Non-goals
## Required process
## Required outputs
## Stop conditions

Missing Constraints
"""


def _tempfile(text: str, suffix: str = "") -> str:
    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=suffix, encoding="utf-8") as f:
        f.write(text)
        return f.name


class PromptPackTests(unittest.TestCase):
    def test_contains_required_sections(self):
        path = _tempfile(VALID_TEMPLATE)
        try:
            self.assertTrue(PromptPack(path).validate_sections())
        finally:
            os.unlink(path)

    def test_missing_sections_raises(self):
        path = _tempfile(INVALID_TEMPLATE)
        try:
            with self.assertRaises(ValueError) as ctx:
                PromptPack(path).validate_sections()
            self.assertIn("## Constraints", str(ctx.exception))
        finally:
            os.unlink(path)

    def test_generated_prompt_requires_issue_and_paths(self):
        path = _tempfile(VALID_TEMPLATE)
        try:
            with self.assertRaises(ValueError) as ctx:
                generate_prompt(path, **{"provider-role": "docs-worker", "issue-url-or-number": "123"})
            self.assertIn("allowed paths", str(ctx.exception))

            with self.assertRaises(ValueError) as ctx:
                generate_prompt(path, **{"provider-role": "docs-worker", "path": "docs/"})
            self.assertIn("issue number", str(ctx.exception))

            prompt = generate_prompt(path, **{
                "provider-role": "docs-worker", "issue-url-or-number": "123", "path": "docs/"})
            self.assertIn("Issue: 123", prompt)
            self.assertIn("Allowed paths: docs/", prompt)
        finally:
            os.unlink(path)


class HarnessRuleTests(unittest.TestCase):
    def test_missing_test_command_blocks_patch_and_pr(self):
        for mode in ("patch", "pr"):
            ok, reason = check_harness_execution_rules({"autonomy_mode": mode, "test_command": ""})
            self.assertFalse(ok)
            self.assertIn("missing test command", reason)
        ok, _ = check_harness_execution_rules({"autonomy_mode": "patch", "test_command": "pytest"})
        self.assertTrue(ok)
        ok, _ = check_harness_execution_rules({"autonomy_mode": "draft", "test_command": ""})
        self.assertTrue(ok)

    def test_high_critical_risk_blocks(self):
        for risk in ("high", "critical"):
            ok, reason = check_harness_execution_rules({"risk_level": risk})
            self.assertFalse(ok)
            self.assertIn("high/critical risk", reason)
        ok, _ = check_harness_execution_rules({"risk_level": "low"})
        self.assertTrue(ok)

    def test_budget_cap_enforced(self):
        ok, reason = check_harness_execution_rules(
            {"budget": {"estimated_cost_usd": 10.0, "max_cost_usd": 5.0}})
        self.assertFalse(ok)
        self.assertIn("budget cap exceeded", reason)
        ok, _ = check_harness_execution_rules(
            {"budget": {"estimated_cost_usd": 2.0, "max_cost_usd": 5.0}})
        self.assertTrue(ok)

    def test_retry_count_capped(self):
        ok, reason = check_harness_execution_rules({"retry_count": 3, "budget": {"max_retries": 2}})
        self.assertFalse(ok)
        self.assertIn("retry count is capped", reason)
        ok, _ = check_harness_execution_rules({"retry_count": 1, "budget": {"max_retries": 2}})
        self.assertTrue(ok)

    def test_notebooklm_needs_export(self):
        ok, reason = check_harness_execution_rules({"source_type": "notebooklm"})
        self.assertFalse(ok)
        self.assertIn("NotebookLM output cannot be treated as canonical", reason)
        ok, _ = check_harness_execution_rules(
            {"source_type": "notebooklm", "exported_link": "https://example.com"})
        self.assertTrue(ok)

    def test_harness_output_validates_against_schema(self):
        ok, reason = check_harness_execution_rules({}, harness_result_path=str(EXAMPLE))
        self.assertTrue(ok, reason)

        bad = _tempfile(json.dumps({"job_id": "123"}), suffix=".json")
        try:
            ok, reason = check_harness_execution_rules({}, harness_result_path=bad)
            self.assertFalse(ok)
            self.assertIn("schema validation", reason)
        finally:
            os.unlink(bad)


if __name__ == "__main__":
    unittest.main()
