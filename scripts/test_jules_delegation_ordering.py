"""The Jules delegation marker must be written AFTER Jules accepts, never before.

Why this test exists (#925). `jules-auto-delegate.yml` writes a
`<!-- jules-delegated -->` comment, and `has_delegation_marker` treats any issue
carrying it as permanently ineligible for automatic delegation. The marker used to be
written in the preflight step, before the Jules create-session call ran at all — so a
delegation that failed, no-opped, or was silently dropped by Jules still left behind a
receipt saying it had succeeded.

That is not hypothetical. Six issues (#596, #594, #543, #527, #517, #471) were marked
delegated on 2026-06-30 and Jules never opened a single pull request. Every scheduled run
for the following month skipped them, and the workflow reported success throughout,
because "nothing left to delegate" and "delegation is broken" produce identical output.

The ordering is the whole defect, so the ordering is what this pins. A comment saying
"write the marker after" is what the workflow already had, in its header, describing the
opposite of what the code did.
"""
from __future__ import annotations

import unittest
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover - yaml is installed in CI
    yaml = None

REPO_ROOT = Path(__file__).resolve().parent.parent
WORKFLOW = REPO_ROOT / ".github" / "workflows" / "jules-auto-delegate.yml"
MARKER = "<!-- jules-delegated -->"
JULES_ENDPOINT = "https://jules.googleapis.com/v1alpha/sessions"


def _steps() -> list[dict]:
    data = yaml.safe_load(WORKFLOW.read_text(encoding="utf-8"))
    return data["jobs"]["delegate"]["steps"]


def _writes_marker(step: dict) -> bool:
    """True when the step POSTS a comment carrying the marker.

    Deliberately not "the marker literal appears in this step". The preflight step
    legitimately contains `marker='<!-- jules-delegated -->'` as the needle for its
    eligibility grep, and the first version of this test flagged that assignment as a
    write — a guard bound to the wrong subject, which is the exact family of bug it was
    written to catch. Reading a marker and writing one are opposite operations that share
    a string.

    A write is a `gh issue comment` invocation whose body carries the marker, either as
    the literal or via the `$marker` variable the workflow expands into it.
    """
    for line in str(step.get("run", "")).splitlines():
        if "gh issue comment" not in line:
            continue
        if MARKER in line or "$marker" in line:
            return True
    return False


def _invokes_jules(step: dict) -> bool:
    run = str(step.get("run", ""))
    return (step.get("name") == "Delegate to Jules"
            and "-X POST" in run
            and JULES_ENDPOINT in run)


@unittest.skipIf(yaml is None, "pyyaml not installed")
class TestDelegationMarkerOrdering(unittest.TestCase):
    def test_workflow_is_parseable_and_invokes_jules(self):
        """Guard the guard: if the provider step moves, ordering must be updated."""
        steps = _steps()
        indexes = [i for i, step in enumerate(steps) if _invokes_jules(step)]
        self.assertEqual(
            1, len(indexes),
            f"expected exactly one POST to {JULES_ENDPOINT}; found {len(indexes)}. "
            "If the provider step moved, update this test — do not delete it.")

    def test_marker_is_never_written_before_jules_runs(self):
        steps = _steps()
        jules_at = next(i for i, step in enumerate(steps) if _invokes_jules(step))

        writers = [i for i, s in enumerate(steps) if _writes_marker(s)]
        self.assertTrue(
            writers,
            f"no step writes {MARKER}; the scheduled listener would re-delegate the "
            "same issue forever. Did the marker literal change?")

        early = [i for i in writers if i < jules_at]
        self.assertEqual(
            [], early,
            f"step(s) {early} write the delegation marker before "
            f"the Jules API call runs at step {jules_at}. A receipt written before the "
            "thing it attests to converts a failed delegation into a permanent record "
            "of a successful one, and the issue is then skipped forever (#925). "
            "Write the marker only after the delegation is confirmed.")

    def test_a_failed_delegation_reports_and_leaves_the_issue_eligible(self):
        """Failing silently is what made this invisible for a month."""
        steps = _steps()
        failure_steps = [s for s in steps if "failure()" in str(s.get("if", ""))]
        self.assertTrue(
            failure_steps,
            "no step runs on failure(); a failed delegation would leave no trace on the "
            "issue, and the only signal would be a red run nobody is watching.")
        for step in failure_steps:
            self.assertFalse(
                _writes_marker(step),
                "the failure path must NOT write the delegation marker — the issue has "
                "to stay eligible for retry.")


if __name__ == "__main__":
    unittest.main()
