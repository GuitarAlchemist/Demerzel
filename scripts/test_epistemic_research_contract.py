from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path
import unittest

from validate_epistemic_research import validate_proposal


ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "fixtures" / "epistemic-research-proposal.sample.json"


class EpistemicResearchContractTests(unittest.TestCase):
    def setUp(self) -> None:
        self.proposal = json.loads(FIXTURE.read_text(encoding="utf-8"))

    def test_reference_fixture_is_valid(self) -> None:
        self.assertEqual(validate_proposal(self.proposal), [])

    def test_requires_two_competing_hypotheses(self) -> None:
        self.proposal["hypotheses"].pop()
        self.assertTrue(any("hypotheses" in issue for issue in validate_proposal(self.proposal)))

    def test_requires_exactly_one_null_hypothesis(self) -> None:
        self.proposal["hypotheses"][0]["role"] = "alternative"
        self.assertTrue(any("$.hypotheses" in issue for issue in validate_proposal(self.proposal)))

    def test_requires_exact_integer_uncertainty_mass(self) -> None:
        self.proposal["uncertainty"]["U"] = 999_999
        self.assertIn(
            "uncertainty T/P/U/D/F/C must sum to exactly 1000000 ppm",
            validate_proposal(self.proposal),
        )

    def test_refuses_authority_or_paid_execution(self) -> None:
        authority = copy.deepcopy(self.proposal)
        authority["authority"]["executionAuthorized"] = True
        self.assertTrue(any("executionAuthorized" in issue for issue in validate_proposal(authority)))

        paid = copy.deepcopy(self.proposal)
        paid["probe"]["maxCost"]["value"] = 1
        self.assertTrue(any("$.probe.maxCost.value" in issue for issue in validate_proposal(paid)))

    def test_proposal_id_is_bound_to_revision_digest(self) -> None:
        self.proposal["proposalId"] = "erp-" + "d" * 64
        self.assertIn("proposalId must equal erp-<revision.digest>", validate_proposal(self.proposal))

    def test_rejects_non_canonical_timestamp_even_with_matching_digest(self) -> None:
        self.proposal["createdAt"] = "2026-08-14T13:30:00.000-04:00"
        self._rematerialize()
        self.assertTrue(any("createdAt" in issue for issue in validate_proposal(self.proposal)))

    def test_rejects_whitespace_only_contract_text(self) -> None:
        cases = [
            ("question", lambda proposal: proposal.__setitem__("question", "   ")),
            ("falsifier", lambda proposal: proposal["hypotheses"][1].__setitem__("falsifier", "\t")),
            ("negativeControl", lambda proposal: proposal["probe"].__setitem__("negativeControl", "\n")),
            ("unit", lambda proposal: proposal["probe"]["maxCost"].__setitem__("unit", "   ")),
        ]
        for label, mutate in cases:
            with self.subTest(path=label):
                proposal = copy.deepcopy(self.proposal)
                mutate(proposal)
                self.assertTrue(any(label in issue for issue in validate_proposal(proposal)))

    def test_rejects_padded_text_even_with_matching_digest(self) -> None:
        original = copy.deepcopy(self.proposal)
        for padding in ("  ", "\ufeff"):
            with self.subTest(padding=ascii(padding)):
                self.proposal = copy.deepcopy(original)
                self.proposal["question"] = f"{padding}Which boundary is supported?{padding}"
                self._rematerialize()
                self.assertTrue(any("question" in issue for issue in validate_proposal(self.proposal)))

    def test_rejects_declared_missing_field_and_provenance_controls(self) -> None:
        cases = [
            lambda proposal: proposal["hypotheses"][1].pop("falsifier"),
            lambda proposal: proposal["probe"].pop("negativeControl"),
            lambda proposal: proposal["probe"]["maxCost"].pop("unit"),
            lambda proposal: proposal["origin"]["inputRevision"].__setitem__("digest", "latest"),
        ]
        for mutate in cases:
            proposal = copy.deepcopy(self.proposal)
            mutate(proposal)
            with self.subTest(proposal=proposal):
                self.assertNotEqual(validate_proposal(proposal), [])

    def test_rejects_content_tampering_with_old_materialization(self) -> None:
        self.proposal["question"] = "A different question with the old digest."
        self.assertIn(
            "revision.digest does not match canonical proposal body",
            validate_proposal(self.proposal),
        )

    def _rematerialize(self) -> None:
        body = copy.deepcopy(self.proposal)
        body.pop("proposalId")
        body.pop("revision")
        digest = hashlib.sha256(
            json.dumps(body, ensure_ascii=False, separators=(",", ":"), sort_keys=True).encode("utf-8")
        ).hexdigest()
        self.proposal["proposalId"] = f"erp-{digest}"
        self.proposal["revision"] = {"algorithm": "sha256", "digest": digest}


if __name__ == "__main__":
    unittest.main()
