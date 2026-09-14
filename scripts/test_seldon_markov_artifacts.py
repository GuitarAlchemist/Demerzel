#!/usr/bin/env python3
"""Bind schemas/seldon/markov-transition.schema.json to real data (epic #596).

Every state/markov/*.markov-transitions.json artifact must:
- have a non-empty `transitions` table whose rows conform to the schema,
  as do the rows of `transitions_by_worker`;
- have outgoing probabilities summing to 1 per (from_state, worker);
- carry `absorption` rows with probabilities in [0, 1] summing to 1, and a
  `held_out` block whose accuracies and losses are in range;
- declare itself advisory (the #596 non-goals: no gating, no auto-merge).

Fails closed: if no artifact exists, the schema has nothing to validate and
the test says so instead of passing vacuously.
"""
from __future__ import annotations

import copy
import json
import math
import unittest
from collections import defaultdict

from jsonschema.validators import Draft202012Validator

import demerzel_kit

SCHEMA = demerzel_kit.ROOT / "schemas" / "seldon" / "markov-transition.schema.json"
ARTIFACTS = sorted((demerzel_kit.ROOT / "state" / "markov").glob("*.markov-transitions.json"))
TOL = 1e-9


def _is_prob(x) -> bool:
    return isinstance(x, (int, float)) and not isinstance(x, bool) and 0.0 <= x <= 1.0


def validate_artifact(data: dict, validator: Draft202012Validator) -> list[str]:
    """Return every problem found in one artifact (empty list = valid)."""
    errors: list[str] = []
    if data.get("advisory") is not True:
        errors.append("advisory must be true")

    transitions = data.get("transitions")
    if not isinstance(transitions, list) or not transitions:
        errors.append("transitions must be a non-empty list")
        transitions = []
    for table, rows in (("transitions", transitions),
                        ("transitions_by_worker", data.get("transitions_by_worker", []))):
        mass: dict[tuple[str, str | None], float] = defaultdict(float)
        for i, row in enumerate(rows):
            for e in validator.iter_errors(row):
                errors.append(f"{table}[{i}]: {e.message}")
            if isinstance(row, dict) and _is_prob(row.get("probability")):
                mass[(row.get("from_state"), row.get("worker"))] += row["probability"]
        for key, total in mass.items():
            if abs(total - 1.0) > TOL:
                errors.append(f"{table} {key}: outgoing probabilities sum to {total}")

    absorption = data.get("absorption")
    if not isinstance(absorption, list) or not absorption:
        errors.append("absorption must be a non-empty list")
        absorption = []
    for i, row in enumerate(absorption):
        parts = [row.get(k) for k in ("p_merged", "p_rejected", "p_unresolved")]
        if not all(_is_prob(p) for p in parts):
            errors.append(f"absorption[{i}]: p_merged/p_rejected/p_unresolved must be in [0, 1]")
        elif abs(sum(parts) - 1.0) > 1e-6:
            errors.append(f"absorption[{i}]: probabilities sum to {sum(parts)}")
        cond = row.get("p_merged_given_resolved")
        if cond is not None and not _is_prob(cond):
            errors.append(f"absorption[{i}]: p_merged_given_resolved must be in [0, 1]")

    held_out = data.get("held_out")
    if not isinstance(held_out, dict) or not held_out.get("scores"):
        errors.append("held_out.scores must be a non-empty list")
    else:
        for i, score in enumerate(held_out["scores"]):
            if not _is_prob(score.get("accuracy")):
                errors.append(f"held_out.scores[{i}].accuracy must be in [0, 1]")
            for j, loss in enumerate(score.get("log_loss", [])):
                v = loss.get("log_loss")
                if not (isinstance(v, (int, float)) and math.isfinite(v) and v >= 0):
                    errors.append(f"held_out.scores[{i}].log_loss[{j}] must be finite and >= 0")
                if not _is_prob(loss.get("epsilon")):
                    errors.append(f"held_out.scores[{i}].log_loss[{j}].epsilon must be in [0, 1]")
        if not all(isinstance(held_out.get(k), int) and held_out[k] >= 0
                   for k in ("train_sequences", "test_sequences", "test_transitions")):
            errors.append("held_out counts must be non-negative integers")
    return errors


class TestSeldonMarkovArtifacts(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.validator = Draft202012Validator(json.loads(SCHEMA.read_text(encoding="utf-8")))

    def load(self, path):
        return json.loads(path.read_text(encoding="utf-8"))

    def test_at_least_one_artifact_exists(self):
        self.assertTrue(ARTIFACTS, "no state/markov/*.markov-transitions.json to validate")

    def test_artifacts_are_valid(self):
        for path in ARTIFACTS:
            self.assertEqual(validate_artifact(self.load(path), self.validator), [], path.name)

    def assert_rejected(self, mutate, needle):
        self.assertTrue(ARTIFACTS)
        data = copy.deepcopy(self.load(ARTIFACTS[0]))
        mutate(data)
        errors = validate_artifact(data, self.validator)
        self.assertTrue(any(needle in e for e in errors), errors)

    def test_rejects_out_of_range_absorption(self):
        self.assert_rejected(lambda d: d["absorption"][0].update(p_merged=7), "absorption[0]")

    def test_rejects_absorption_not_summing_to_one(self):
        self.assert_rejected(lambda d: d["absorption"][0].update(p_unresolved=0.5), "sum to")

    def test_rejects_out_of_range_accuracy(self):
        self.assert_rejected(lambda d: d["held_out"]["scores"][2].update(accuracy=3), "accuracy")

    def test_rejects_empty_transitions(self):
        self.assert_rejected(lambda d: d.update(transitions=[]), "transitions must be")

    def test_rejects_unknown_state(self):
        self.assert_rejected(lambda d: d["transitions"][0].update(to_state="pr.limbo"), "transitions[0]")

    def test_rejects_probabilities_not_summing_to_one(self):
        self.assert_rejected(lambda d: d["transitions"][0].update(probability=0.99), "sum to")

    def test_rejects_non_advisory(self):
        self.assert_rejected(lambda d: d.update(advisory=False), "advisory")


if __name__ == "__main__":
    unittest.main()
