"""Contract tests for Demerzel cycle-driver execution policy declarations."""

from __future__ import annotations

import ast
from pathlib import Path
import shlex
import unittest

import yaml


ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github" / "workflows" / "ml-governance-schedule.yml"


def _module_docstring(relative_path: str) -> str:
    source = (ROOT / relative_path).read_text(encoding="utf-8")
    return ast.get_docstring(ast.parse(source)) or ""


class CycleDriverExecutionPolicyTests(unittest.TestCase):
    def test_afk_cycle_declares_manual_or_external_ownership(self) -> None:
        docstring = _module_docstring("scripts/run_afk_cycle.py")

        self.assertIn("Execution policy: manual-or-external.", docstring)
        self.assertIn("No GitHub Actions workflow schedules this driver.", docstring)
        self.assertIn("no automatic\nfreshness guard", docstring)

    def test_ml_feedback_declares_external_cycle_and_read_only_tripwire(self) -> None:
        docstring = _module_docstring("scripts/run_ml_feedback_cycle.py")
        workflow = yaml.safe_load(WORKFLOW.read_text(encoding="utf-8"))
        triggers = workflow.get("on", workflow.get(True, {}))

        self.assertIn("Execution policy: externally-scheduled.", docstring)
        self.assertIn("read-only freshness tripwire", docstring)
        self.assertIn("schedule", triggers)
        self.assertEqual({"contents": "read"}, workflow.get("permissions"))
        self.assertIn("freshness", workflow.get("jobs", {}))
        self.assertTrue(
            all("permissions" not in job for job in workflow["jobs"].values())
        )

        entrypoint_steps = workflow["jobs"]["entrypoint"]["steps"]
        smoke = next(
            step
            for step in entrypoint_steps
            if step.get("name") == "ML-feedback orchestrator dry-run (strict)"
        )
        self.assertEqual(
            [
                "python",
                "scripts/run_ml_feedback_cycle.py",
                "--dry-run",
                "--strict",
                "--repos-root",
                "_siblings",
            ],
            shlex.split(smoke["run"]),
        )


if __name__ == "__main__":
    unittest.main()
