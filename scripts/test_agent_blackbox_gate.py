"""Invariant tests for the agent-blackbox risk-report merge gate.

The gate conflates nothing: *reporting* the risk and *enforcing* the verdict are
separate steps with opposite failure policies. Reporting may fail (a 5xx on the
comments API says nothing about the risk of a change — see #773); enforcement may
not (it is the merge gate itself).

These tests pin that asymmetry against the workflow YAML so a later edit cannot
quietly invert it — the concern #641 raises about PRs that weaken the guardrail
gating them.
"""

import unittest
from pathlib import Path

import yaml

WORKFLOW = Path(__file__).resolve().parent.parent / ".github" / "workflows" / "agent-blackbox.yml"

COMMENT_STEP = "Comment risk report"
ENFORCE_STEP = "Enforce verdict"


def _steps() -> list[dict]:
    # PyYAML parses the unquoted `on:` key as boolean True; irrelevant here, we
    # only read jobs.
    doc = yaml.safe_load(WORKFLOW.read_text(encoding="utf-8"))
    return doc["jobs"]["risk-report"]["steps"]


def _step(name: str) -> dict:
    for step in _steps():
        if step.get("name") == name:
            return step
    raise AssertionError(f"step {name!r} not found in risk-report job")


class TestReportingIsNonBlocking(unittest.TestCase):
    """Reporting is best-effort: it retries, and it may not fail the job."""

    def test_comment_step_exists(self):
        self.assertIsNotNone(_step(COMMENT_STEP))

    def test_comment_step_is_continue_on_error(self):
        step = _step(COMMENT_STEP)
        self.assertIs(
            step.get("continue-on-error"),
            True,
            "the comment step must not be able to fail the gate; a transient 5xx "
            "on POST /issues/{n}/comments is not a risk signal (#773)",
        )

    def test_comment_step_retries_5xx(self):
        step = _step(COMMENT_STEP)
        retries = step.get("with", {}).get("retries")
        self.assertIsNotNone(retries, "comment step must set an explicit retries count")
        self.assertGreaterEqual(
            int(retries), 1, "retries: 0 is what made a platform outage block a merge (#773)"
        )

    def test_comment_step_does_not_exempt_5xx_from_retry(self):
        # github-script's default retry-exempt list is 400,401,403,404,422 — all 4xx.
        # If someone adds 5xx codes here, retries stop covering the outage case.
        exempt = str(_step(COMMENT_STEP).get("with", {}).get("retry-exempt-status-codes", ""))
        for code in exempt.replace(" ", "").split(","):
            if code:
                self.assertLess(
                    int(code), 500, f"{code} is exempted from retry, defeating the #773 fix"
                )


class TestEnforcementStaysFailClosed(unittest.TestCase):
    """Enforcement is the gate. It must be able to fail the job."""

    def test_enforce_step_exists(self):
        self.assertIsNotNone(_step(ENFORCE_STEP))

    def test_enforce_step_is_not_continue_on_error(self):
        step = _step(ENFORCE_STEP)
        self.assertNotEqual(
            step.get("continue-on-error"),
            True,
            "the verdict path must stay fail-closed — a 'block' verdict has to fail "
            "the job, or risk-report is no longer a merge gate (#773 non-goal)",
        )

    def test_enforce_step_runs_after_comment_step(self):
        names = [s.get("name") for s in _steps()]
        self.assertLess(
            names.index(COMMENT_STEP),
            names.index(ENFORCE_STEP),
            "enforcement must run after reporting, so a skipped comment still reaches the gate",
        )

    def test_only_the_reviewed_label_can_bypass_enforcement(self):
        # The single sanctioned bypass is the human-attestation label. If another
        # escape hatch appears in this step, it is a new way to merge unreviewed.
        run = _step(ENFORCE_STEP).get("run", "")
        self.assertIn("AGENT_BLACKBOX_REVIEWED", run)
        self.assertEqual(
            run.count("exit 0"),
            1,
            "exactly one unconditional-success path (the reviewed-label override) "
            "should exist in the enforcement step",
        )


if __name__ == "__main__":
    unittest.main()
