import json
import tempfile
import unittest
from pathlib import Path

from aiw_budget_gate import evaluate


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


class BudgetGateTests(unittest.TestCase):
    def test_local_cli_is_allowed_without_paid_approval(self):
        result = evaluate(POLICY, request())
        self.assertEqual("allow", result["decision"])

    def test_cloud_provider_requires_explicit_approval(self):
        result = evaluate(POLICY, request(provider="gemini-cli"))
        self.assertEqual("block", result["decision"])
        self.assertIn("provider_requires_manual_approval", result["reasons"])

    def test_approved_cloud_job_is_allowed_under_caps(self):
        result = evaluate(POLICY, request(
            provider="jules", manual_approval=True, estimated_cost_usd=1.5))
        self.assertEqual("allow", result["decision"])

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

    def test_cli_ledger_shape_is_json_serializable(self):
        result = evaluate(POLICY, request())
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "ledger.json"
            path.write_text(json.dumps(result), encoding="utf-8")
            self.assertEqual("allow", json.loads(path.read_text())["decision"])


if __name__ == "__main__":
    unittest.main()
