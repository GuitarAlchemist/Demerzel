"""#957: Jules approval must survive a fresh workflow dispatch without replay."""

from __future__ import annotations

import re
import unittest
from pathlib import Path


WORKFLOW = (Path(__file__).resolve().parents[1]
            / ".github" / "workflows" / "jules-auto-delegate.yml")


class JulesApprovalHandshakeTests(unittest.TestCase):
    def setUp(self) -> None:
        self.text = WORKFLOW.read_text(encoding="utf-8")

    def test_manual_dispatch_requires_an_explicit_approval_id(self) -> None:
        self.assertRegex(
            self.text,
            r"(?ms)^      approval_id:\n"
            r"        description:.*\n"
            r"        required: true$")
        self.assertIn("APPROVAL_ID: ${{ inputs.approval_id || '' }}", self.text)

    def test_job_identity_is_stable_across_fresh_runs(self) -> None:
        job_id_line = next(
            line for line in self.text.splitlines()
            if line.strip().startswith('job_id="jules-issue-'))
        self.assertIn(
            'job_id="jules-issue-${issue}-approval-${APPROVAL_ID}"',
            job_id_line)
        self.assertNotIn("GITHUB_RUN_ID", job_id_line)

    def test_approval_id_is_validated_before_request_construction(self) -> None:
        validate_at = self.text.find("invalid approval_id")
        job_id_at = self.text.find('job_id="jules-issue-')
        self.assertNotEqual(validate_at, -1)
        self.assertLess(validate_at, job_id_at)
        validation = self.text[max(0, validate_at - 300):validate_at]
        self.assertRegex(validation, r"\^\[A-Za-z0-9\].*\{0,63\}\$")

    def test_automatic_triggers_cannot_invent_paid_authority(self) -> None:
        self.assertIn("if: github.event_name == 'workflow_dispatch'", self.text)
        missing_at = self.text.find('if [ -z "$APPROVAL_ID" ]')
        gate_at = self.text.find("python3 scripts/aiw_budget_gate.py --request")
        self.assertNotEqual(missing_at, -1)
        self.assertLess(missing_at, gate_at)
        missing_branch = self.text[missing_at:gate_at]
        self.assertIn('echo "proceed=false" >> "$GITHUB_OUTPUT"', missing_branch)
        self.assertIn("exit 0", missing_branch)

    def test_paid_dispatch_is_pinned_to_the_default_branch_environment(self) -> None:
        self.assertIn("environment: jules-paid-default-branch", self.text)
        self.assertIn("secrets.JULES_PAID_API_KEY", self.text)
        self.assertNotIn("secrets.JULES_API_KEY", self.text)
        self.assertIn("ref: ${{ github.event.repository.default_branch }}", self.text)
        self.assertIn("DEFAULT_BRANCH: ${{ github.event.repository.default_branch }}",
                      self.text)
        self.assertIn("REF_NAME: ${{ github.ref_name }}", self.text)
        guard_at = self.text.find('if [ "$REF_NAME" != "$DEFAULT_BRANCH" ]')
        gate_at = self.text.find("python3 scripts/aiw_budget_gate.py --request")
        self.assertNotEqual(guard_at, -1)
        self.assertLess(guard_at, gate_at)

    def test_blocked_phase_prints_an_exact_approval_template(self) -> None:
        block_at = self.text.find('if [ "$budget_rc" -ne 0 ]')
        allow_at = self.text.find("AIW budget gate allowed jules")
        block = self.text[block_at:allow_at]
        self.assertIn("request_sha256", block)
        self.assertIn("approval_id", block)
        self.assertIn("approved_at", block)
        self.assertIn("approver", block)
        self.assertIn("aiw-budget-ledger.json", block)

    def test_a_previous_approval_does_not_make_phase_one_unreachable(self) -> None:
        gate_at = self.text.find("python3 scripts/aiw_budget_gate.py --request")
        before_gate = self.text[:gate_at]
        self.assertIn('approval_artifact=".octo/aiw-approval.json"', before_gate)
        self.assertIn('committed_approval_id', before_gate)
        self.assertIn('mv "$approval_artifact" "$RUNNER_TEMP/stale-aiw-approval.json"',
                      before_gate)
        self.assertIn("invalid committed Jules approval artifact", before_gate)

    def test_consumed_approval_cannot_be_replayed_even_with_force(self) -> None:
        consumed_check_at = self.text.find("approval id has already been consumed")
        force_check_at = self.text.find('if [ "$FORCE" != "true" ]')
        gate_at = self.text.find("python3 scripts/aiw_budget_gate.py --request")
        self.assertNotEqual(consumed_check_at, -1)
        self.assertLess(consumed_check_at, force_check_at)
        self.assertLess(consumed_check_at, gate_at)
        consumed_branch = self.text[max(0, consumed_check_at - 500):force_check_at]
        self.assertIn("exit 1", consumed_branch)

    def test_only_workflow_authored_markers_can_consume_approval(self) -> None:
        function_at = self.text.find("bot_comments()")
        function_end = self.text.find("\n          }", function_at)
        function = self.text[function_at:function_end]
        self.assertIn(
            'select(.user.login == "github-actions[bot]")', function,
            "an arbitrary issue commenter must not be able to consume authority")
        self.assertIn("--paginate", function)

    def test_comment_api_failure_fails_closed(self) -> None:
        function_at = self.text.find("has_approval_marker()")
        function_end = self.text.find("\n          }", function_at)
        function = self.text[function_at:function_end]
        self.assertIn("return 2", function)
        self.assertIn("could not verify Jules approval consumption", self.text)

    def test_attempt_marker_consumes_the_exact_approval_before_jules(self) -> None:
        marker = "<!-- jules-approval-attempted:$APPROVAL_ID -->"
        self.assertIn(marker, self.text)
        consume_at = self.text.find("- name: Consume one-shot Jules approval")
        delegate_at = self.text.find("- name: Delegate to Jules")
        self.assertNotEqual(consume_at, -1)
        self.assertLess(consume_at, delegate_at)
        consume = self.text[consume_at:delegate_at]
        self.assertIn("APPROVAL_ID: ${{ steps.gate.outputs.approval_id }}", consume)
        self.assertEqual(1, len(re.findall(re.escape(marker), consume)))

    def test_provider_call_requires_a_valid_created_session(self) -> None:
        delegate_at = self.text.find("- name: Delegate to Jules")
        finalize_at = self.text.find("- name: Finalize AIW budget reservation")
        delegate = self.text[delegate_at:finalize_at]
        self.assertIn("curl --fail-with-body", delegate)
        self.assertNotIn("--retry", delegate)
        self.assertIn('test("^sessions/[^/]+$")', delegate)
        self.assertIn("session_name=", delegate)
        self.assertNotIn("google-labs-code/jules-action@", delegate)


if __name__ == "__main__":
    unittest.main()
