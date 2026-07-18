import json
import tempfile
import unittest
from pathlib import Path

from aiw_budget_gate import _request_sha256, evaluate


ROOT = Path(__file__).parents[1]
POLICY = json.loads((ROOT / "state/driver/aiw-budget-policy.json").read_text())


def request(**overrides):
    value = {
        "job_id": "aiw-test",
        "provider": "claude-code-cli",
        "estimated_cost_usd": 0,
        "cycle_spend_usd": 0,
        "estimated_total_tokens": 10000,
        "estimated_model_calls": 1,
        "estimated_retries": 0,
        "estimated_runner_minutes": 5,
        "cycle_active_packets": 0,
    }
    value.update(overrides)
    return value


def receipt(req, issuer, actual_cost_usd, **overrides):
    """Build a trusted provider receipt bound to a reserved request."""
    value = {
        "schema_version": "1.0",
        "kind": "provider-receipt",
        "job_id": req["job_id"],
        "provider": req["provider"],
        "request_sha256": _request_sha256(req),
        "issuer": issuer,
        "receipt_id": "rcpt-0001",
        "observed_at": "2026-07-18T01:00:00Z",
        "actual_cost_usd": actual_cost_usd,
    }
    value.update(overrides)
    return value


def approval(req, **overrides):
    """Build a separate approval artifact bound to a request's fingerprint."""
    value = {
        "schema_version": "1.0",
        "kind": "human-approval",
        "decision": "approve",
        "job_id": req["job_id"],
        "provider": req["provider"],
        "request_sha256": _request_sha256(req),
        "approval_id": "appr-0001",
        "approver": "sol",
        "approved_at": "2026-07-18T00:00:00Z",
    }
    value.update(overrides)
    return value


class BudgetGateTests(unittest.TestCase):
    def test_local_cli_is_allowed_without_paid_approval(self):
        result = evaluate(POLICY, request())
        self.assertEqual("allow", result["decision"])

    def test_cloud_provider_requires_explicit_approval(self):
        result = evaluate(POLICY, request(provider="gemini-cli"))
        self.assertEqual("block", result["decision"])
        self.assertIn("provider_requires_manual_approval", result["reasons"])

    def test_self_attested_manual_approval_in_request_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "manual_approval is not accepted"):
            evaluate(POLICY, request(
                provider="jules", manual_approval=True, estimated_cost_usd=1.5))

    def test_metered_provider_blocked_without_approval_artifact(self):
        result = evaluate(POLICY, request(provider="jules", estimated_cost_usd=1.5))
        self.assertEqual("block", result["decision"])
        self.assertIn("provider_requires_manual_approval", result["reasons"])

    def test_approved_cloud_job_is_allowed_under_caps(self):
        req = request(provider="jules", estimated_cost_usd=1.5)
        result = evaluate(POLICY, req, approval=approval(req))
        self.assertEqual("allow", result["decision"])

    def test_approval_bound_to_wrong_request_is_rejected(self):
        req = request(provider="jules", estimated_cost_usd=1.5)
        stale = approval(req, request_sha256="0" * 64)
        with self.assertRaisesRegex(ValueError, "approval request_sha256 does not match"):
            evaluate(POLICY, req, approval=stale)

    def test_approval_for_wrong_provider_is_rejected(self):
        req = request(provider="jules", estimated_cost_usd=1.5)
        wrong = approval(req, provider="gemini-cli")
        with self.assertRaisesRegex(ValueError, "approval provider does not match"):
            evaluate(POLICY, req, approval=wrong)

    def test_cost_cap_blocks_before_invocation(self):
        result = evaluate(POLICY, request(estimated_cost_usd=2.01))
        self.assertEqual("block", result["decision"])
        self.assertIn("job_cost_cap_exceeded", result["reasons"])

    def test_cycle_cap_blocks_before_invocation(self):
        result = evaluate(POLICY, request(cycle_spend_usd=9, estimated_cost_usd=2))
        self.assertIn("cycle_cost_cap_exceeded", result["reasons"])

    def test_token_and_retry_caps_block(self):
        result = evaluate(POLICY, request(
            estimated_total_tokens=200001, estimated_retries=2))
        self.assertIn("token_cap_exceeded", result["reasons"])
        self.assertIn("retry_cap_exceeded", result["reasons"])

    def test_parallel_cap_blocks(self):
        result = evaluate(POLICY, request(cycle_active_packets=4))
        self.assertIn("parallel_packet_cap_exceeded", result["reasons"])

    def test_unknown_provider_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "not allowlisted"):
            evaluate(POLICY, request(provider="unknown"))

    def test_job_cannot_widen_policy_cap(self):
        with self.assertRaisesRegex(ValueError, "cannot exceed policy default"):
            evaluate(POLICY, request(max_cost_usd=200))

    def test_nan_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "non-negative number"):
            evaluate(POLICY, request(estimated_cost_usd=float("nan")))

    def test_nan_policy_cycle_cap_is_rejected(self):
        policy = json.loads(json.dumps(POLICY))
        policy["cycle"]["max_cost_usd"] = float("nan")
        with self.assertRaisesRegex(ValueError, "non-negative number"):
            evaluate(policy, request())

    def test_cycle_reservation_blocks_aggregate_overrun(self):
        from aiw_budget_gate import reserve
        policy = json.loads(json.dumps(POLICY))
        policy["cycle"]["max_cost_usd"] = 2
        with tempfile.TemporaryDirectory() as directory:
            cycle = Path(directory) / "cycle.json"
            first = reserve(policy, request(job_id="one", estimated_cost_usd=2), cycle)
            second = reserve(policy, request(job_id="two", estimated_cost_usd=1), cycle)
            self.assertEqual("allow", first["decision"])
            self.assertEqual("block", second["decision"])
            self.assertIn("cycle_cost_cap_exceeded", second["reasons"])

    def test_reservation_records_provider_and_request_sha(self):
        from aiw_budget_gate import _request_sha256, reserve
        with tempfile.TemporaryDirectory() as directory:
            cycle = Path(directory) / "cycle.json"
            req = request(job_id="one")
            reserve(POLICY, req, cycle)
            entry = json.loads(cycle.read_text())["reservations"]["one"]
            self.assertEqual("claude-code-cli", entry["provider"])
            self.assertEqual(_request_sha256(req), entry["request_sha256"])

    def test_reservation_reuse_with_identical_request_is_idempotent(self):
        from aiw_budget_gate import reserve
        with tempfile.TemporaryDirectory() as directory:
            cycle = Path(directory) / "cycle.json"
            req = request(job_id="one", estimated_cost_usd=0.5)
            reserve(POLICY, req, cycle)
            second = reserve(POLICY, req, cycle)
            self.assertTrue(second["reservation_reused"])
            self.assertEqual(0.5, second["budget"]["estimated_cost_usd"])

    def test_reservation_reuse_with_changed_request_fails_closed(self):
        from aiw_budget_gate import reserve
        with tempfile.TemporaryDirectory() as directory:
            cycle = Path(directory) / "cycle.json"
            reserve(POLICY, request(job_id="one", estimated_cost_usd=0.1), cycle)
            with self.assertRaisesRegex(ValueError, "fingerprint"):
                reserve(POLICY, request(job_id="one", estimated_cost_usd=1.9), cycle)

    def test_reservation_reuse_cannot_switch_provider(self):
        from aiw_budget_gate import reserve
        with tempfile.TemporaryDirectory() as directory:
            cycle = Path(directory) / "cycle.json"
            reserve(POLICY, request(job_id="one"), cycle)
            with self.assertRaisesRegex(ValueError, "fingerprint"):
                reserve(POLICY, request(job_id="one", provider="codex-cli"), cycle)

    def test_release_records_actual_cost_and_frees_capacity(self):
        from aiw_budget_gate import release, reserve
        with tempfile.TemporaryDirectory() as directory:
            cycle = Path(directory) / "cycle.json"
            reserve(POLICY, request(job_id="one"), cycle)
            result = release(cycle, "one", 0.25)
            self.assertEqual("released", result["decision"])
            state = json.loads(cycle.read_text())
            self.assertEqual(0, state["active_packets"])
            self.assertEqual(0.25, state["actual_cost_usd"])

    def test_metered_release_requires_trusted_receipt(self):
        from aiw_budget_gate import release, reserve
        with tempfile.TemporaryDirectory() as directory:
            cycle = Path(directory) / "cycle.json"
            req = request(job_id="j1", provider="jules", estimated_cost_usd=1.5)
            reserve(POLICY, req, cycle, approval=approval(req))
            with self.assertRaisesRegex(ValueError, "receipt"):
                release(cycle, "j1", 1.5, policy=POLICY)

    def test_metered_release_rejects_untrusted_issuer(self):
        from aiw_budget_gate import release, reserve
        with tempfile.TemporaryDirectory() as directory:
            cycle = Path(directory) / "cycle.json"
            req = request(job_id="j1", provider="jules", estimated_cost_usd=1.5)
            reserve(POLICY, req, cycle, approval=approval(req))
            forged = receipt(req, "attacker.example.com", 1.5)
            with self.assertRaisesRegex(ValueError, "not trusted"):
                release(cycle, "j1", 1.5, policy=POLICY, receipt=forged)

    def test_metered_release_with_trusted_receipt_records_actual(self):
        from aiw_budget_gate import release, reserve
        with tempfile.TemporaryDirectory() as directory:
            cycle = Path(directory) / "cycle.json"
            req = request(job_id="j1", provider="jules", estimated_cost_usd=1.5)
            reserve(POLICY, req, cycle, approval=approval(req))
            good = receipt(req, "jules.googleapis.com", 1.25)
            result = release(cycle, "j1", 1.25, policy=POLICY, receipt=good)
            self.assertEqual("released", result["decision"])
            state = json.loads(cycle.read_text())
            self.assertEqual(0, state["active_packets"])
            self.assertEqual(1.25, state["actual_cost_usd"])

    def test_metered_release_blocks_over_budget_actual(self):
        from aiw_budget_gate import release, reserve
        with tempfile.TemporaryDirectory() as directory:
            cycle = Path(directory) / "cycle.json"
            req = request(job_id="j1", provider="jules", estimated_cost_usd=1.5)
            reserve(POLICY, req, cycle, approval=approval(req))
            overrun = receipt(req, "jules.googleapis.com", 9.99)
            result = release(cycle, "j1", 9.99, policy=POLICY, receipt=overrun)
            self.assertEqual("over_budget", result["decision"])
            self.assertIn("actual_cost_cap_exceeded", result["reasons"])
            # Real spend is still recorded truthfully even when it is blocked.
            self.assertEqual(9.99, json.loads(cycle.read_text())["actual_cost_usd"])

    def test_metered_receipt_actual_must_match_release_amount(self):
        from aiw_budget_gate import release, reserve
        with tempfile.TemporaryDirectory() as directory:
            cycle = Path(directory) / "cycle.json"
            req = request(job_id="j1", provider="jules", estimated_cost_usd=1.5)
            reserve(POLICY, req, cycle, approval=approval(req))
            mismatch = receipt(req, "jules.googleapis.com", 1.25)
            with self.assertRaisesRegex(ValueError, "actual_cost_usd"):
                release(cycle, "j1", 0.01, policy=POLICY, receipt=mismatch)

    def test_actual_receipts_count_against_next_reservation(self):
        from aiw_budget_gate import release, reserve
        policy = json.loads(json.dumps(POLICY))
        with tempfile.TemporaryDirectory() as directory:
            cycle = Path(directory) / "cycle.json"
            reserve(policy, request(job_id="one"), cycle)
            release(cycle, "one", 10.0)
            result = reserve(policy, request(job_id="two", estimated_cost_usd=1), cycle)
            self.assertEqual("block", result["decision"])
            self.assertIn("cycle_cost_cap_exceeded", result["reasons"])

    def test_noncanonical_runtime_path_is_rejected(self):
        from aiw_budget_gate import LEDGER_PATH, _bind_canonical
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaisesRegex(ValueError, "must be"):
                _bind_canonical("--ledger", Path(directory) / "ledger.json", LEDGER_PATH)

    def test_canonical_runtime_path_is_accepted(self):
        from aiw_budget_gate import LEDGER_PATH, _bind_canonical
        self.assertEqual(LEDGER_PATH.resolve(),
                         _bind_canonical("--ledger", LEDGER_PATH, LEDGER_PATH))

    def test_local_seat_providers_route_without_approval(self):
        for provider in ("claude-code-cli", "codex-cli", "antigravity", "augment-code"):
            result = evaluate(POLICY, request(provider=provider))
            self.assertEqual("allow", result["decision"], provider)

    def test_metered_providers_require_approval(self):
        for provider in ("gemini-cli", "jules", "notebooklm"):
            result = evaluate(POLICY, request(provider=provider))
            self.assertEqual("block", result["decision"], provider)
            self.assertIn("provider_requires_manual_approval", result["reasons"])

    def test_cli_ledger_shape_is_json_serializable(self):
        result = evaluate(POLICY, request())
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "ledger.json"
            path.write_text(json.dumps(result), encoding="utf-8")
            self.assertEqual("allow", json.loads(path.read_text())["decision"])


if __name__ == "__main__":
    unittest.main()
