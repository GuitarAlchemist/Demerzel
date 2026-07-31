import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

import aiw_budget_gate
from aiw_budget_gate import _request_sha256, evaluate, load_policy


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


class PolicySchemaTests(unittest.TestCase):
    """The policy gates real spend and arrives as an ordinary PR diff, so an
    unrecognized or out-of-bounds key must fail the load, not slip through."""

    def load_mutated_policy(self, mutator):
        """Write a mutated copy of the shipped policy and load it."""
        policy = json.loads(json.dumps(POLICY))
        mutator(policy)
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        path = Path(directory.name) / "policy.json"
        path.write_text(json.dumps(policy), encoding="utf-8")
        return load_policy(path)

    def test_shipped_policy_validates(self):
        self.assertEqual(POLICY, load_policy(aiw_budget_gate.POLICY_PATH))

    def test_an_unpinned_provider_id_is_rejected(self):
        # The tier-keyed guards constrain the shape GIVEN a tier, and the
        # per-id pins only bind the seven known providers. An EIGHTH id was
        # unconstrained: it could declare itself local-seat with no receipt
        # issuer, and reserve + release billed with no approval artifact.
        # Inert today only because routing is hardcoded to pinned ids -- a
        # property of the call sites, not a guarantee of this schema.
        def mutate(policy):
            policy["providers"].append({
                "id": "jules-v2", "tier": "local-seat",
                "cost_model": "subscription-or-local",
                "requires_manual_approval": False,
            })

        with self.assertRaisesRegex(ValueError, "policy is invalid"):
            self.load_mutated_policy(mutate)

    def test_a_pinned_provider_cannot_be_renamed_out_of_its_pin(self):
        # Renaming sidesteps a per-id pin: the constraint keys on the id, so
        # changing the id escapes it. The closed enum is what stops this.
        def mutate(policy):
            provider = next(p for p in policy["providers"] if p["id"] == "jules")
            provider["id"] = "jules-v2"

        with self.assertRaisesRegex(ValueError, "policy is invalid"):
            self.load_mutated_policy(mutate)

    def test_metered_provider_cannot_be_downgraded_to_local_seat(self):
        # The tier-keyed guards constrain the shape GIVEN a tier -- but tier is
        # editable in the same diff. Downgrading jules to local-seat escaped
        # every metered guard and allowed a billed reservation with no approval
        # artifact and no trusted receipt. Known providers are pinned by id.
        def mutate(policy):
            provider = next(p for p in policy["providers"] if p["id"] == "jules")
            provider["tier"] = "local-seat"
            provider["cost_model"] = "subscription-or-local"
            provider["requires_manual_approval"] = False
            provider.pop("trusted_receipt_issuer", None)

        with self.assertRaisesRegex(ValueError, "policy is invalid"):
            self.load_mutated_policy(mutate)

    def test_local_provider_cannot_be_promoted_to_metered_cloud(self):
        for provider_id in (
                "claude-code-cli", "codex-cli", "antigravity", "augment-code"):
            with self.subTest(provider=provider_id):
                def mutate(policy):
                    provider = next(
                        item for item in policy["providers"]
                        if item["id"] == provider_id)
                    provider["tier"] = "metered-cloud"
                    provider["cost_model"] = "provider-billing"
                    provider["requires_manual_approval"] = True
                    provider["trusted_receipt_issuer"] = "billing.example.com"

                with self.assertRaisesRegex(ValueError, "policy is invalid"):
                    self.load_mutated_policy(mutate)

    def test_trusted_receipt_issuer_cannot_be_repointed(self):
        # Any well-formed hostname passed the pattern, so the issuer could be
        # repointed at an attacker-controlled host and still validate.
        def mutate(policy):
            provider = next(p for p in policy["providers"] if p["id"] == "jules")
            provider["trusted_receipt_issuer"] = "evil.attacker.com"

        with self.assertRaisesRegex(ValueError, "policy is invalid"):
            self.load_mutated_policy(mutate)

    def test_validation_error_names_the_offending_field(self):
        # "True was expected" alone locates nothing in a 7-provider file.
        def mutate(policy):
            provider = next(p for p in policy["providers"] if p["id"] == "jules")
            provider["requires_manual_approval"] = False

        with self.assertRaisesRegex(ValueError, r"\$\.providers\[\d+\]\.requires_manual_approval"):
            self.load_mutated_policy(mutate)

    def test_metered_provider_cannot_claim_a_free_cost_model(self):
        # The metered branch pinned only the issuer and approval flag, so a
        # paid provider could label itself "subscription-or-local" and pass.
        # The local-seat branch already pinned cost_model; this restores the
        # symmetry. cost_model is read by no production code today, which is
        # exactly why a wrong value would go unnoticed.
        def mutate(policy):
            provider = next(p for p in policy["providers"]
                            if p["tier"] == "metered-cloud")
            provider["cost_model"] = "subscription-or-local"

        with self.assertRaisesRegex(ValueError, "policy is invalid"):
            self.load_mutated_policy(mutate)

    def test_unknown_root_key_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "policy is invalid"):
            self.load_mutated_policy(
                lambda p: p.update({"max_spend_multiplier": 100}))

    def test_unknown_provider_key_is_rejected(self):
        # The concrete #772 finding: an out-of-range multiplier added to the
        # metered `jules` provider left the whole suite green.
        def mutate(policy):
            provider = next(p for p in policy["providers"] if p["id"] == "jules")
            provider["cost_multiplier"] = 1000
        with self.assertRaisesRegex(ValueError, "policy is invalid"):
            self.load_mutated_policy(mutate)

    def test_unknown_defaults_key_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "policy is invalid"):
            self.load_mutated_policy(
                lambda p: p["defaults"].update({"max_cost_eur": 2.0}))

    def test_zero_cost_cap_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "policy is invalid"):
            self.load_mutated_policy(
                lambda p: p["defaults"].update({"max_cost_usd": 0}))

    def test_negative_cycle_cap_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "policy is invalid"):
            self.load_mutated_policy(
                lambda p: p["cycle"].update({"max_cost_usd": -1}))

    def test_zero_parallel_packets_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "policy is invalid"):
            self.load_mutated_policy(
                lambda p: p["cycle"].update({"max_parallel_packets": 0}))

    def test_zero_retries_is_accepted_as_a_tightening(self):
        loaded = self.load_mutated_policy(
            lambda p: p["defaults"].update({"max_retries": 0}))
        self.assertEqual(0, loaded["defaults"]["max_retries"])

    def test_unknown_cost_model_is_rejected(self):
        def mutate(policy):
            policy["providers"][0]["cost_model"] = "free-lunch"
        with self.assertRaisesRegex(ValueError, "policy is invalid"):
            self.load_mutated_policy(mutate)

    def test_missing_required_provider_field_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "policy is invalid"):
            self.load_mutated_policy(lambda p: p["providers"][0].pop("tier"))

    def test_metered_provider_without_receipt_issuer_is_rejected(self):
        def mutate(policy):
            provider = next(p for p in policy["providers"] if p["id"] == "jules")
            provider.pop("trusted_receipt_issuer")
        with self.assertRaisesRegex(ValueError, "policy is invalid"):
            self.load_mutated_policy(mutate)

    def test_metered_provider_cannot_drop_manual_approval(self):
        def mutate(policy):
            provider = next(p for p in policy["providers"] if p["id"] == "jules")
            provider["requires_manual_approval"] = False
        with self.assertRaisesRegex(ValueError, "policy is invalid"):
            self.load_mutated_policy(mutate)

    def test_selection_order_cannot_name_an_undeclared_provider(self):
        # Two layers reject an unroutable selection_order entry, and this test
        # targets the SECOND deliberately. The id enum catches ids that are not
        # known at all, so an entry like "shadow-provider" now fails at the
        # schema before load_policy's cross-reference check ever runs. The
        # cross-reference is still the only thing catching a KNOWN id that this
        # policy does not declare, so drop a real provider and route to it.
        def mutate(policy):
            # selection_order already lists notebooklm, so only drop the
            # provider -- appending it too would trip uniqueItems first and
            # test the wrong layer.
            policy["providers"] = [p for p in policy["providers"]
                                   if p["id"] != "notebooklm"]

        with self.assertRaisesRegex(ValueError, "undeclared providers"):
            self.load_mutated_policy(mutate)

    def test_selection_order_rejects_a_wholly_unknown_id(self):
        # The layer above: an id outside the allowlist never reaches the
        # cross-reference check.
        with self.assertRaisesRegex(ValueError, "policy is invalid"):
            self.load_mutated_policy(
                lambda p: p["selection_order"].append("shadow-provider"))

    def test_duplicate_provider_ids_are_rejected(self):
        def mutate(policy):
            policy["providers"].append(json.loads(json.dumps(policy["providers"][0])))
        with self.assertRaisesRegex(ValueError, "duplicate provider ids"):
            self.load_mutated_policy(mutate)

    def test_invalid_policy_exits_2_not_1(self):
        """Exit 2 is 'fail closed / invalid'; exit 1 is a governed block. An
        unloadable policy must never be mistaken for an ordinary denial."""
        policy = json.loads(json.dumps(POLICY))
        policy["defaults"]["max_cost_usd"] = -5
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "aiw-budget-policy.json"
            path.write_text(json.dumps(policy), encoding="utf-8")
            with mock.patch.object(aiw_budget_gate, "POLICY_PATH", path):
                self.assertEqual(2, aiw_budget_gate.main(["--policy", str(path)]))

    def test_valid_policy_block_still_exits_1(self):
        """Control for the test above: with the shipped policy, a governed
        block is exit 1, so exit 2 really does isolate invalidity."""
        with tempfile.TemporaryDirectory() as directory:
            req = Path(directory) / "request.json"
            ledger = Path(directory) / "ledger.json"
            cycle = Path(directory) / "cycle.json"
            req.write_text(json.dumps(
                request(job_id="cli-block", provider="gemini-cli",
                        estimated_cost_usd=1.0)), encoding="utf-8")
            with mock.patch.object(aiw_budget_gate, "LEDGER_PATH", ledger), \
                    mock.patch.object(aiw_budget_gate, "CYCLE_LEDGER_PATH", cycle), \
                    mock.patch.object(aiw_budget_gate, "APPROVAL_PATH",
                                      Path(directory) / "approval.json"), \
                    mock.patch.object(aiw_budget_gate, "RECEIPT_PATH",
                                      Path(directory) / "receipt.json"):
                code = aiw_budget_gate.main([
                    "--request", str(req), "--ledger", str(ledger),
                    "--cycle-ledger", str(cycle),
                    "--approval", str(Path(directory) / "approval.json"),
                    "--receipt", str(Path(directory) / "receipt.json")])
            self.assertEqual(1, code)


if __name__ == "__main__":
    unittest.main()


class TestPolicyInvalidIsDistinct(unittest.TestCase):
    """#794: a corrupt policy and an ordinary budget block need opposite
    responses, so they must not be the same exception class."""

    def _load_mutated(self, mutator):
        policy = json.loads(json.dumps(POLICY))
        mutator(policy)
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        path = Path(directory.name) / "policy.json"
        path.write_text(json.dumps(policy), encoding="utf-8")
        return load_policy(path)

    def test_schema_violation_raises_policy_invalid(self):
        def mutate(policy):
            policy["defaults"]["max_cost_usd_per_job"] = -999
        with self.assertRaises(aiw_budget_gate.PolicyInvalid):
            self._load_mutated(mutate)

    def test_undeclared_selection_order_raises_policy_invalid(self):
        def mutate(policy):
            policy["selection_order"].append("no-such-provider")
        with self.assertRaises(aiw_budget_gate.PolicyInvalid):
            self._load_mutated(mutate)

    def test_missing_file_raises_policy_invalid(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        with self.assertRaises(aiw_budget_gate.PolicyInvalid):
            load_policy(Path(directory.name) / "absent.json")

    def test_unparseable_file_raises_policy_invalid(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        path = Path(directory.name) / "policy.json"
        path.write_text("{not json", encoding="utf-8")
        with self.assertRaises(aiw_budget_gate.PolicyInvalid):
            load_policy(path)

    def test_policy_invalid_is_still_a_value_error(self):
        # main() maps ValueError to exit 2; that mapping must not change.
        self.assertTrue(issubclass(aiw_budget_gate.PolicyInvalid, ValueError))

    def test_shipped_policy_does_not_raise(self):
        self.assertEqual(POLICY, load_policy(aiw_budget_gate.POLICY_PATH))


class TestNoteReleaseFailure(unittest.TestCase):
    """#794: a swallowed release leaves the reservation open. Record it, so an
    unreconciled reservation is detectable instead of silent."""

    def _ledger(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        return Path(directory.name) / "cycle.json"

    def test_records_the_swallow_against_an_open_reservation(self):
        path = self._ledger()
        aiw_budget_gate.reserve(POLICY, request(job_id="aiw-1"), path)
        self.assertTrue(aiw_budget_gate.note_release_failure(path, "aiw-1", "boom"))
        cycle = json.loads(path.read_text())
        note = cycle["release_failures"][0]
        self.assertEqual(note["job_id"], "aiw-1")
        self.assertIn("boom", note["error"])
        self.assertTrue(note["reservation_open"])
        self.assertTrue(note["at"].endswith("Z"))

    def test_note_does_not_disturb_ledger_invariants(self):
        # _read_cycle asserts reserved_cost == sum(reservations) and
        # active_packets == len(reservations). A note must not perturb either,
        # or the next reserve() would fail closed on a ledger it wrote itself.
        path = self._ledger()
        aiw_budget_gate.reserve(POLICY, request(job_id="aiw-1"), path)
        before = json.loads(path.read_text())
        aiw_budget_gate.note_release_failure(path, "aiw-1", "boom")
        after = json.loads(path.read_text())
        self.assertEqual(before["reserved_cost_usd"], after["reserved_cost_usd"])
        self.assertEqual(before["active_packets"], after["active_packets"])
        self.assertEqual(before["reservations"], after["reservations"])
        aiw_budget_gate.reserve(POLICY, request(job_id="aiw-2"), path)  # still loadable

    def test_notes_accumulate(self):
        path = self._ledger()
        aiw_budget_gate.reserve(POLICY, request(job_id="aiw-1"), path)
        aiw_budget_gate.note_release_failure(path, "aiw-1", "first")
        aiw_budget_gate.note_release_failure(path, "aiw-1", "second")
        self.assertEqual(len(json.loads(path.read_text())["release_failures"]), 2)

    def test_never_raises_when_the_ledger_is_unwritable(self):
        # Recording a failure must not become a second failure.
        path = self._ledger()
        path.write_text("{not json", encoding="utf-8")
        self.assertFalse(aiw_budget_gate.note_release_failure(path, "aiw-1", "boom"))


class TestCliAbandonVerb(unittest.TestCase):
    """#896: an APPROVED metered run reserved through the CLI had no terminal
    state an operator could reach. `--release-job` demands a trusted provider
    receipt (`_validate_receipt`) and a metered provider's receipt cannot be
    self-issued, so the reservation stayed open forever; after
    cycle.max_parallel_packets such runs the provider-agnostic packet cap blocked
    EVERY lane, including the free subscription one.

    PR #914 gave the AFK governor `abandon()`, but the governor passes
    approval=None and therefore can never run an approved metered job at all --
    the CLI is the only path an approved metered run takes, and it had no abandon
    verb. This exposes it. No receipt is synthesised; see
    test_metered_release_is_abandoned_not_forged in test_run_afk_cycle.py.
    """

    def setUp(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.dir = Path(directory.name)
        # Every canonical path is redirected into the tempdir: a failing test
        # must never mutate the committed .octo/ ledger state.
        self.policy_path = self.dir / "aiw-budget-policy.json"
        self.policy_path.write_text(
            aiw_budget_gate.POLICY_PATH.read_text(encoding="utf-8"), encoding="utf-8")
        self.cycle = self.dir / "cycle.json"
        self.ledger = self.dir / "ledger.json"
        self.approval_path = self.dir / "approval.json"
        self.receipt_path = self.dir / "receipt.json"
        self.request_path = self.dir / "request.json"
        self.metered = next(p["id"] for p in POLICY["providers"]
                            if p.get("tier") == "metered-cloud"
                            and p.get("trusted_receipt_issuer"))

    def cli(self, args):
        with mock.patch.object(aiw_budget_gate, "POLICY_PATH", self.policy_path), \
                mock.patch.object(aiw_budget_gate, "CYCLE_LEDGER_PATH", self.cycle), \
                mock.patch.object(aiw_budget_gate, "LEDGER_PATH", self.ledger), \
                mock.patch.object(aiw_budget_gate, "APPROVAL_PATH", self.approval_path), \
                mock.patch.object(aiw_budget_gate, "RECEIPT_PATH", self.receipt_path):
            return aiw_budget_gate.main(args)

    def reserve_approved(self, job_id, estimated_cost_usd=1.0):
        """Drive an approved metered reserve exactly as an operator must: a
        committed approval artifact bound to the request fingerprint."""
        req = {"job_id": job_id, "provider": self.metered,
               "estimated_cost_usd": estimated_cost_usd}
        self.request_path.write_text(json.dumps(req), encoding="utf-8")
        self.approval_path.write_text(json.dumps(approval(req)), encoding="utf-8")
        self.assertEqual(0, self.cli(["--request", str(self.request_path)]),
                         "approved metered reserve should be allowed")
        return req

    def read_cycle(self):
        return json.loads(self.cycle.read_text(encoding="utf-8"))

    def test_release_without_a_receipt_leaves_the_reservation_open(self):
        """The leak itself, stated as a fact about `--release-job`. This is why
        an abandon verb is needed rather than a looser release."""
        self.reserve_approved("aiw-896-a")
        self.assertEqual(2, self.cli(
            ["--release-job", "aiw-896-a", "--actual-cost-usd", "0.0"]))
        cycle = self.read_cycle()
        self.assertIn("aiw-896-a", cycle["reservations"])
        self.assertEqual(1, cycle["active_packets"])

    def test_abandon_job_reaches_a_terminal_state_from_the_cli(self):
        self.reserve_approved("aiw-896-b", estimated_cost_usd=1.25)
        code = self.cli(["--abandon-job", "aiw-896-b", "--reason", "no provider receipt"])
        self.assertEqual(0, code)
        cycle = self.read_cycle()
        self.assertEqual({}, cycle["reservations"])
        self.assertEqual(0, cycle["active_packets"])
        self.assertAlmostEqual(0.0, cycle["reserved_cost_usd"])
        # Charged, not credited back: unverified is not the same as free.
        self.assertAlmostEqual(1.25, cycle["actual_cost_usd"])
        entry = cycle["unreconciled"][0]
        self.assertFalse(entry["receipt_verified"])
        self.assertEqual(self.metered, entry["provider"])
        self.assertIn("no provider receipt", entry["reason"])

    def test_abandon_is_reported_as_abandoned_not_released(self):
        """An abandon must never be mistakable for a clean release: the decision
        written to the budget ledger is the operator's only record of which
        happened."""
        self.reserve_approved("aiw-896-c")
        self.cli(["--abandon-job", "aiw-896-c", "--reason", "receipt unobtainable"])
        self.assertEqual("abandoned",
                         json.loads(self.ledger.read_text(encoding="utf-8"))["decision"])

    def test_abandon_requires_a_reason(self):
        """An abandonment with no recorded reason is an unauditable write."""
        self.reserve_approved("aiw-896-d")
        self.assertEqual(2, self.cli(["--abandon-job", "aiw-896-d"]))
        self.assertIn("aiw-896-d", self.read_cycle()["reservations"])

    def test_abandoning_an_unknown_job_fails_closed(self):
        self.reserve_approved("aiw-896-e")
        self.assertEqual(2, self.cli(["--abandon-job", "no-such-job", "--reason", "x"]))
        self.assertIn("aiw-896-e", self.read_cycle()["reservations"])

    def test_release_and_abandon_cannot_be_requested_together(self):
        with self.assertRaises(SystemExit):
            self.cli(["--release-job", "a", "--abandon-job", "a", "--reason", "x"])

    def test_abandon_unwedges_the_gate_for_every_other_lane(self):
        """The #896 acceptance criterion at the CLI: cap+1 approved metered runs
        no longer exhaust the provider-agnostic packet cap, so the free
        subscription lane -- which had nothing to do with them -- still reserves."""
        cap = int(POLICY["cycle"]["max_parallel_packets"])
        for n in range(cap + 1):
            job = f"aiw-896-cap-{n}"
            self.reserve_approved(job, estimated_cost_usd=0.01)
            self.assertEqual(0, self.cli(
                ["--abandon-job", job, "--reason", "no provider receipt"]))
        free = aiw_budget_gate.reserve(
            POLICY, request(job_id="aiw-896-free"), self.cycle)
        self.assertEqual("allow", free["decision"],
                         f"free lane blocked after {cap + 1} metered runs: {free['reasons']}")

    def test_an_honest_release_still_reconciles_and_is_not_abandoned(self):
        """The honest path must stay honest: when a trusted receipt DOES exist,
        `--release-job` reconciles verified spend and nothing is abandoned.
        Abandonment is the fallback for an unobtainable receipt, never the
        default for metered work."""
        req = self.reserve_approved("aiw-896-honest", estimated_cost_usd=1.0)
        issuer = next(p["trusted_receipt_issuer"] for p in POLICY["providers"]
                      if p["id"] == self.metered)
        self.receipt_path.write_text(
            json.dumps(receipt(req, issuer, 0.42)), encoding="utf-8")
        code = self.cli(["--release-job", "aiw-896-honest", "--actual-cost-usd", "0.42"])
        self.assertEqual(0, code)
        cycle = self.read_cycle()
        self.assertEqual({}, cycle["reservations"])
        self.assertEqual(0, cycle["active_packets"])
        self.assertAlmostEqual(0.42, cycle["actual_cost_usd"])  # measured, not estimated
        self.assertNotIn("unreconciled", cycle)
        self.assertEqual("released",
                         json.loads(self.ledger.read_text(encoding="utf-8"))["decision"])
