from __future__ import annotations

import copy
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


if __name__ == "__main__":
    unittest.main()
