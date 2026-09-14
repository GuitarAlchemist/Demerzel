#!/usr/bin/env python3
"""Bind schemas/seldon/markov-transition.schema.json to real data (epic #596).

Every state/markov/*.markov-transitions.json artifact must:
- carry at least one row, each conforming to the schema;
- have outgoing probabilities summing to 1 per (from_state, worker);
- declare itself advisory (the #596 non-goals: no gating, no auto-merge).

Fails closed: if no artifact exists, the schema has nothing to validate and
the test says so instead of passing vacuously.
"""
from __future__ import annotations

import json
import unittest
from collections import defaultdict
from pathlib import Path

from jsonschema.validators import Draft202012Validator

REPO = Path(__file__).resolve().parent.parent
SCHEMA = REPO / "schemas" / "seldon" / "markov-transition.schema.json"
ARTIFACTS = sorted((REPO / "state" / "markov").glob("*.markov-transitions.json"))


class TestSeldonMarkovArtifacts(unittest.TestCase):
    def test_at_least_one_artifact_exists(self):
        self.assertTrue(ARTIFACTS, "no state/markov/*.markov-transitions.json to validate")

    def test_rows_conform_to_schema(self):
        validator = Draft202012Validator(json.loads(SCHEMA.read_text(encoding="utf-8")))
        for path in ARTIFACTS:
            data = json.loads(path.read_text(encoding="utf-8"))
            rows = data["transitions"] + data.get("transitions_by_worker", [])
            self.assertTrue(rows, path.name)
            for i, row in enumerate(rows):
                errors = [e.message for e in validator.iter_errors(row)]
                self.assertEqual(errors, [], f"{path.name} row {i}: {row}")

    def test_outgoing_probabilities_sum_to_one(self):
        for path in ARTIFACTS:
            data = json.loads(path.read_text(encoding="utf-8"))
            for table in ("transitions", "transitions_by_worker"):
                mass: dict[tuple[str, str | None], float] = defaultdict(float)
                for row in data.get(table, []):
                    mass[(row["from_state"], row.get("worker"))] += row["probability"]
                for key, total in mass.items():
                    self.assertAlmostEqual(total, 1.0, places=9, msg=f"{path.name} {table} {key}")

    def test_artifacts_are_advisory(self):
        for path in ARTIFACTS:
            data = json.loads(path.read_text(encoding="utf-8"))
            self.assertIs(data.get("advisory"), True, path.name)


if __name__ == "__main__":
    unittest.main()
