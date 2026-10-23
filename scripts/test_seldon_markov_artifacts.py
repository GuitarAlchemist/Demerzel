#!/usr/bin/env python3
"""Bind schemas/seldon/markov-transition.schema.json to real data (epic #596).

Every state/markov/*.markov-transitions.json artifact must:
- have a non-empty `transitions` table and a `transitions_by_worker` list
  whose rows conform to the schema, with no duplicate (from, to, worker) row;
- be internally consistent: each row's probability is its sample_size over
  its (from_state, worker) block's total, rows into a stuck state carry no
  median (the step sits at the stale threshold), every worker block has at
  least `method.worker_min_outgoing` transitions, and no worker row exceeds
  the global row it refines;
- carry an `absorption` row for every transient state that has outgoing
  transitions, and each row must be what the first-order chain in
  `transitions` implies (merged and rejected mass imply the same
  continuation share), with p_merged_given_resolved = p_merged / resolved;
- carry `observed_outcomes` counts that add up, for the same states;
- carry a `held_out` block whose accuracies are k / test_transitions, whose
  models share one epsilon sweep, whose order histogram covers every test
  transition, and whose cluster sign test p matches its cluster counts;
- declare itself advisory (the #596 non-goals: no gating, no auto-merge).

The checks are meant for PR-lifecycle artifacts: `absorption`, `observed_outcomes`
and `held_out` are required of every file the glob matches. A later artifact
without them (a capability-stream table, say) needs its own glob.

Fails closed: if no artifact exists, the schema has nothing to validate and
the test says so instead of passing vacuously.
"""
from __future__ import annotations

import copy
import json
import math
import unittest
from collections import defaultdict
from datetime import datetime

from jsonschema.validators import Draft202012Validator

import demerzel_kit

SCHEMA = demerzel_kit.ROOT / "schemas" / "seldon" / "markov-transition.schema.json"
ARTIFACTS = sorted((demerzel_kit.ROOT / "state" / "markov").glob("*.markov-transitions.json"))
TOL = 1e-9
TERMINAL = ("pr.merged", "pr.rejected")


def _is_prob(x) -> bool:
    return isinstance(x, (int, float)) and not isinstance(x, bool) and 0.0 <= x <= 1.0


def _is_count(x) -> bool:
    return isinstance(x, int) and not isinstance(x, bool) and x >= 0


def _is_utc(x) -> bool:
    try:
        datetime.strptime(x, "%Y-%m-%dT%H:%M:%SZ")
        return True
    except (TypeError, ValueError):
        return False


def sign_test_p(a: int, b: int) -> float:
    """Exact two-sided binomial sign test (1.0 when there are no clusters)."""
    n = a + b
    if n == 0:
        return 1.0
    return min(1.0, 2 * sum(math.comb(n, k) for k in range(min(a, b) + 1)) / 2 ** n)


def _check_table(table: str, rows: list, validator, errors: list[str]) -> dict:
    """Schema, duplicate, probability = count / block total, stuck medians."""
    blocks: dict[tuple, list[dict]] = defaultdict(list)
    seen: set[tuple] = set()
    for i, row in enumerate(rows):
        for e in validator.iter_errors(row):
            errors.append(f"{table}[{i}]: {e.message}")
        if not isinstance(row, dict):
            continue
        key = (row.get("from_state"), row.get("to_state"), row.get("worker"))
        if key in seen:
            errors.append(f"{table}[{i}]: duplicate row {key}")
        seen.add(key)
        if "stuck" in str(row.get("to_state")) and "median_duration_hours" in row:
            errors.append(f"{table}[{i}]: a row into {row['to_state']} must not carry "
                          "median_duration_hours (it would be the stale threshold)")
        if _is_prob(row.get("probability")) and _is_count(row.get("sample_size")):
            blocks[(row.get("from_state"), row.get("worker"))].append(row)
    for (from_state, worker), block in blocks.items():
        total_p = sum(r["probability"] for r in block)
        if abs(total_p - 1.0) > TOL:
            errors.append(f"{table} {(from_state, worker)}: outgoing probabilities sum to {total_p}")
        n = sum(r["sample_size"] for r in block)
        for r in block:
            if abs(r["probability"] - r["sample_size"] / n) > TOL:
                errors.append(f"{table} {(from_state, worker)} -> {r.get('to_state')}: probability "
                              f"{r['probability']} != sample_size/total {r['sample_size']}/{n}")
    return blocks


def validate_artifact(data: dict, validator: Draft202012Validator) -> list[str]:
    """Return every problem found in one artifact (empty list = valid)."""
    errors: list[str] = []
    states = validator.schema["properties"]["from_state"]["enum"]
    if data.get("advisory") is not True:
        errors.append("advisory must be true")
    if not _is_utc(data.get("as_of")):
        errors.append("as_of must be a UTC timestamp like 2026-09-14T21:01:50Z")
    method = data.get("method") if isinstance(data.get("method"), dict) else {}
    min_worker = method.get("worker_min_outgoing")
    if not (_is_count(min_worker) and min_worker >= 1):
        errors.append("method.worker_min_outgoing must be a positive integer")
        min_worker = None

    transitions = data.get("transitions")
    if not isinstance(transitions, list) or not transitions:
        errors.append("transitions must be a non-empty list")
        transitions = []
    by_worker = data.get("transitions_by_worker")
    if not isinstance(by_worker, list):
        errors.append("transitions_by_worker must be a list")
        by_worker = []
    global_blocks = _check_table("transitions", transitions, validator, errors)
    worker_blocks = _check_table("transitions_by_worker", by_worker, validator, errors)
    global_n = {(r["from_state"], r["to_state"]): r["sample_size"]
                for block in global_blocks.values() for r in block}
    for i, row in enumerate(by_worker):
        if isinstance(row, dict) and row.get("worker") is None:
            errors.append(f"transitions_by_worker[{i}]: worker is required")
    refined: dict[tuple, int] = defaultdict(int)
    for (from_state, worker), block in worker_blocks.items():
        n = sum(r["sample_size"] for r in block)
        if worker is not None and min_worker is not None and n < min_worker:
            errors.append(f"transitions_by_worker {(from_state, worker)}: {n} outgoing transitions, "
                          f"below method.worker_min_outgoing {min_worker}")
        for r in block:
            refined[(from_state, r.get("to_state"))] += r["sample_size"]
    for key, n in refined.items():
        if n > global_n.get(key, 0):
            errors.append(f"transitions_by_worker {key}: {n} samples across workers, "
                          f"more than the {global_n.get(key, 0)} in transitions")

    absorption = data.get("absorption")
    if not isinstance(absorption, list) or not absorption:
        errors.append("absorption must be a non-empty list")
        absorption = []
    # Row (from, to) -> probability in the global first-order chain.
    chain = {(r["from_state"], r["to_state"]): r["probability"]
             for block in global_blocks.values() for r in block}
    implied = {"pr.merged": (1.0, 0.0), "pr.rejected": (0.0, 1.0)}
    absorbed: dict[str, dict] = {}
    for i, row in enumerate(absorption):
        if not isinstance(row, dict):
            errors.append(f"absorption[{i}] must be an object")
            continue
        state = row.get("state")
        if state not in states or state in TERMINAL:
            errors.append(f"absorption[{i}]: state {state!r} is not a transient schema state")
        elif state in absorbed:
            errors.append(f"absorption[{i}]: duplicate state {state}")
        parts = [row.get(k) for k in ("p_merged", "p_rejected", "p_unresolved")]
        if not all(_is_prob(p) for p in parts):
            errors.append(f"absorption[{i}]: p_merged/p_rejected/p_unresolved must be in [0, 1]")
            continue
        if abs(sum(parts) - 1.0) > 1e-6:
            errors.append(f"absorption[{i}]: probabilities sum to {sum(parts)}")
        resolved = row["p_merged"] + row["p_rejected"]
        cond = row.get("p_merged_given_resolved")
        if resolved > 0 and not (_is_prob(cond) and abs(cond - row["p_merged"] / resolved) < 1e-6):
            errors.append(f"absorption[{i}]: p_merged_given_resolved {cond} != "
                          f"p_merged / (p_merged + p_rejected) = {row['p_merged'] / resolved}")
        if row.get("sample_size") != sum(r["sample_size"] for r in global_blocks.get((state, None), [])):
            errors.append(f"absorption[{i}]: sample_size {row.get('sample_size')} != "
                          f"transitions leaving {state} in transitions")
        absorbed[state] = row
        implied[state] = (row["p_merged"], row["p_rejected"])
    for from_state, _ in global_blocks:
        if from_state not in TERMINAL and from_state not in absorbed:
            errors.append(f"absorption: no row for {from_state}, which has outgoing transitions")
    # First-order chain: p(s) = k_s * sum_t P(t|s) p(t), where k_s is the share
    # of visits to s that continue. Merged and rejected mass must agree on k_s.
    visits: dict[str, float] = {}
    for state, row in absorbed.items():
        nxt = [(t, p) for (f, t), p in chain.items() if f == state]
        if any(t not in implied for t, _ in nxt):
            continue  # a missing absorption row is already reported
        em = sum(p * implied[t][0] for t, p in nxt)
        er = sum(p * implied[t][1] for t, p in nxt)
        km = row["p_merged"] / em if em > 0 else None
        kr = row["p_rejected"] / er if er > 0 else None
        k = km if km is not None else kr
        if (km is not None and kr is not None and abs(km - kr) > 1e-6) or (k is not None and not 0 < k <= 1 + 1e-9):
            errors.append(f"absorption {state}: p_merged/p_rejected are not implied by the "
                          f"first-order chain in transitions (continuation shares {km} vs {kr})")
        elif k is not None:
            visits[state] = row["sample_size"] / k

    observed = data.get("observed_outcomes")
    if not isinstance(observed, list):
        errors.append("observed_outcomes must be a list")
        observed = []
    observed_states = set()
    for i, row in enumerate(observed):
        counts = [row.get(k) if isinstance(row, dict) else None
                  for k in ("prs_visiting", "merged", "rejected", "open")]
        if not all(_is_count(c) for c in counts):
            errors.append(f"observed_outcomes[{i}]: prs_visiting/merged/rejected/open must be non-negative integers")
            continue
        state = row.get("state")
        observed_states.add(state)
        if counts[0] != sum(counts[1:]):
            errors.append(f"observed_outcomes[{i}]: merged + rejected + open = {sum(counts[1:])}, "
                          f"not prs_visiting {counts[0]}")
        if state in visits and counts[0] > round(visits[state]):
            errors.append(f"observed_outcomes[{i}]: {counts[0]} PRs visit {state}, more than the "
                          f"{round(visits[state])} visits the chain implies")
    if observed_states != set(absorbed):
        errors.append(f"observed_outcomes states {sorted(observed_states)} != absorption states {sorted(absorbed)}")

    held_out = data.get("held_out")
    if not isinstance(held_out, dict) or not held_out.get("scores"):
        errors.append("held_out.scores must be a non-empty list")
        return errors
    n_test = held_out.get("test_transitions")
    if not all(_is_count(held_out.get(k)) for k in ("train_sequences", "test_sequences", "test_transitions")):
        errors.append("held_out counts must be non-negative integers")
        n_test = None
    elif _is_count(data.get("prs")) and held_out["train_sequences"] + held_out["test_sequences"] != data["prs"]:
        errors.append("held_out train_sequences + test_sequences != prs")
    if not (_is_utc(held_out.get("cutoff")) and _is_utc(data.get("as_of"))
            and held_out["cutoff"] <= data["as_of"]):
        errors.append("held_out.cutoff must be a UTC timestamp no later than as_of")
    sweeps = set()
    for i, score in enumerate(held_out["scores"]):
        acc = score.get("accuracy")
        if not _is_prob(acc):
            errors.append(f"held_out.scores[{i}].accuracy must be in [0, 1]")
        elif n_test and abs(acc * n_test - round(acc * n_test)) > 1e-6:
            errors.append(f"held_out.scores[{i}].accuracy {acc} is not k / {n_test} test transitions")
        losses = score.get("log_loss")
        if not isinstance(losses, list) or not losses:
            errors.append(f"held_out.scores[{i}].log_loss must be a non-empty list")
            continue
        for j, loss in enumerate(losses):
            v = loss.get("log_loss")
            if not (isinstance(v, (int, float)) and math.isfinite(v) and v >= 0):
                errors.append(f"held_out.scores[{i}].log_loss[{j}] must be finite and >= 0")
            if not _is_prob(loss.get("epsilon")):
                errors.append(f"held_out.scores[{i}].log_loss[{j}].epsilon must be in [0, 1]")
        sweeps.add(tuple(loss.get("epsilon") for loss in losses))
    if len(sweeps) > 1:
        errors.append(f"held_out.scores use different epsilon sweeps: {sorted(sweeps, key=str)}")
    hist = held_out.get("vlmm_order_histogram")
    if not (isinstance(hist, list) and all(_is_count(h) for h in hist) and sum(hist) == n_test):
        errors.append(f"held_out.vlmm_order_histogram must count all {n_test} test transitions")
    dis = held_out.get("disagreement")
    keys = ("vlmm_only_correct", "first_order_only_correct",
            "clusters_favoring_vlmm", "clusters_favoring_first_order")
    if not (isinstance(dis, dict) and all(_is_count(dis.get(k)) for k in keys)):
        errors.append("held_out.disagreement counts must be non-negative integers")
    else:
        if dis["clusters_favoring_vlmm"] > dis["vlmm_only_correct"] or \
                dis["clusters_favoring_first_order"] > dis["first_order_only_correct"]:
            errors.append("held_out.disagreement: more clusters than disagreeing transitions")
        p = dis.get("cluster_sign_test_p")
        want = sign_test_p(dis["clusters_favoring_vlmm"], dis["clusters_favoring_first_order"])
        if not _is_prob(p):
            errors.append("held_out.disagreement.cluster_sign_test_p must be in [0, 1]")
        elif abs(p - want) > 1e-9:
            errors.append(f"held_out.disagreement.cluster_sign_test_p {p} != sign test of its clusters {want}")
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

    @staticmethod
    def row(rows, from_state, to_state, worker=None):
        return next(r for r in rows if (r["from_state"], r["to_state"], r.get("worker"))
                    == (from_state, to_state, worker))

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

    # Internal consistency: each of these used to pass the shape-only checks.

    def test_rejects_swapped_probabilities(self):
        def mutate(d):
            merged = self.row(d["transitions"], "pr.ready_for_review", "pr.merged")
            rejected = self.row(d["transitions"], "pr.ready_for_review", "pr.rejected")
            merged["probability"], rejected["probability"] = rejected["probability"], merged["probability"]
        self.assert_rejected(mutate, "!= sample_size/total")

    def test_rejects_duplicate_row(self):
        def mutate(d):
            merged = self.row(d["transitions"], "pr.ready_for_review", "pr.merged")
            merged["probability"] /= 2
            d["transitions"].append(dict(merged))
        self.assert_rejected(mutate, "duplicate row")

    def test_rejects_threshold_median_on_stuck_row(self):
        def mutate(d):
            next(r for r in d["transitions"] if "stuck" in r["to_state"])["median_duration_hours"] = 336
        self.assert_rejected(mutate, "must not carry median_duration_hours")

    def test_rejects_worker_block_below_minimum(self):
        self.assert_rejected(lambda d: d["transitions_by_worker"].append(
            {"from_state": "pr.stuck_ready", "to_state": "pr.merged", "probability": 1.0,
             "worker": "jules", "sample_size": 1}), "below method.worker_min_outgoing")

    def test_rejects_worker_row_without_worker(self):
        self.assert_rejected(lambda d: d["transitions_by_worker"][0].pop("worker"), "worker is required")

    def test_rejects_missing_transitions_by_worker(self):
        self.assert_rejected(lambda d: d.pop("transitions_by_worker"), "transitions_by_worker must be a list")

    def test_rejects_inconsistent_conditional_merge_rate(self):
        self.assert_rejected(lambda d: d["absorption"][0].update(p_merged_given_resolved=0.1),
                             "p_merged_given_resolved")

    def test_rejects_unknown_absorption_state(self):
        self.assert_rejected(lambda d: d["absorption"][0].update(state="pr.limbo"),
                             "is not a transient schema state")

    def test_rejects_missing_absorption_row(self):
        def mutate(d):
            d["absorption"] = [a for a in d["absorption"] if a["state"] != "pr.stuck_ready"]
        self.assert_rejected(mutate, "no row for pr.stuck_ready")

    def test_rejects_absorption_not_implied_by_chain(self):
        def mutate(d):
            a = next(a for a in d["absorption"] if a["state"] == "pr.stuck_draft")
            a["p_merged"], a["p_unresolved"] = a["p_merged"] + 0.05, a["p_unresolved"] - 0.05
            a["p_merged_given_resolved"] = a["p_merged"] / (a["p_merged"] + a["p_rejected"])
        self.assert_rejected(mutate, "not implied by the first-order chain")

    def test_rejects_observed_outcomes_not_adding_up(self):
        self.assert_rejected(lambda d: d["observed_outcomes"][3].update(merged=18), "not prs_visiting")

    def test_rejects_missing_log_loss(self):
        def mutate(d):
            for score in d["held_out"]["scores"]:
                score.pop("log_loss")
        self.assert_rejected(mutate, "log_loss must be a non-empty list")

    def test_rejects_out_of_range_sign_test_p(self):
        self.assert_rejected(lambda d: d["held_out"]["disagreement"].update(cluster_sign_test_p=7),
                             "cluster_sign_test_p must be in [0, 1]")

    def test_rejects_accuracy_not_a_fraction_of_test_transitions(self):
        def mutate(d):
            next(s for s in d["held_out"]["scores"] if s["model"] == "first_order")["accuracy"] = 0.99
        self.assert_rejected(mutate, "is not k / 355")

    def test_rejects_garbage_as_of(self):
        self.assert_rejected(lambda d: d.update(as_of="yesterday"), "as_of must be")


if __name__ == "__main__":
    unittest.main()
