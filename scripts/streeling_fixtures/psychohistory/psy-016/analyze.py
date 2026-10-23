#!/usr/bin/env python3
"""PSY-016 analysis: Brier and logarithmic scores of probability forecasts on the label pairs.

Reads observed-input.json (written by extract.py) and scenarios.json, never
the repository, and writes results.json. Brier scores are exact fractions.
The only floats that come from the C library are logarithms; each is stored
to 6 decimals after a check that it does not sit on a rounding boundary.

Run from the repository root:
    python -I -B scripts/streeling_fixtures/psychohistory/psy-016/analyze.py
    python -I -B scripts/streeling_fixtures/psychohistory/psy-016/analyze.py --check
"""

from __future__ import annotations

import argparse
import copy
import json
import math
import random
import sys
from datetime import datetime
from fractions import Fraction
from pathlib import Path

# This program lives under scripts/ (CONTRIBUTING.md: no executable code outside scripts/); its data stays
# under state/streeling/fixtures/. FIXTURE_FILE is the path the program would have next to that data.
FIXTURE_FILE = (Path(__file__).resolve().parents[4]
                / "state/streeling/fixtures/psychohistory/psy-016" / Path(__file__).name)

HERE = FIXTURE_FILE.parent
NO_ROW, NO_LABEL, SEED = ".", "-", "s"
DECIMALS = {"score": 9, "sum": 6, "ratio": 6, "percent": 2, "log": 6, "day": 3}
PINNED_COMMIT = "4b03838800dcd4894f1e026461979bff1d985ca8"
# Counts every module of the path must find at PINNED_COMMIT (the syllabus's shared facts).
SHARED_FACTS = {"rows": 1548, "artifacts": 18, "usable_pairs": 1529, "changed": 1,
                "from_a_seed_row": 11, "between_feeder_runs": 1518}
SUBSETS = ("all_usable_pairs", "from_a_seed_row", "between_feeder_runs")
CHECKS: dict[str, int] = {}  # self-check -> times evaluated


def check(name: str, condition: bool, detail: str = "") -> None:
    """A self-check that can fail: abort instead of writing a wrong result."""
    if not condition:
        raise AssertionError(f"self-check failed: {name}" + (f" ({detail})" if detail else ""))
    CHECKS[name] = CHECKS.get(name, 0) + 1


def prob(value) -> Fraction:
    """A probability from scenarios.json, read as the exact decimal it is written as."""
    p = Fraction(str(value))
    if not 0 <= p <= 1:
        raise ValueError(f"not a probability: {value!r}")
    return p


def shown(value: Fraction, kind: str = "score") -> dict:
    """An exact fraction with its rounded decimal value."""
    return {"exact": str(value), "value": round(float(value), DECIMALS[kind]) + 0.0}


def share(part: Fraction, whole: Fraction) -> dict:
    if whole == 0:
        return {"exact": "undefined: the total is 0", "percent": None}
    return {"exact": str(part / whole), "percent": round(float(100 * part / whole), DECIMALS["percent"]) + 0.0}


def skill(score: Fraction, reference: Fraction) -> dict:
    """Brier skill score 1 - BS / BS_ref; undefined when the reference scores 0."""
    if reference == 0:
        return {"exact": "undefined: the reference score is 0", "value": None}
    return shown(1 - score / reference, "ratio")


def log_value(x: float) -> float:
    """Round a logarithm to the stored decimals, refusing a value that sits on a rounding boundary."""
    scaled = x * 10 ** DECIMALS["log"]
    check("no stored logarithm is within 0.000001 of a rounding boundary of its last digit",
          abs(scaled - math.floor(scaled) - 0.5) > 1e-6, repr(x))
    return round(x, DECIMALS["log"]) + 0.0


def squared_errors(cells: list[tuple]) -> Fraction:
    """Sum of (p - o)^2 over cells (stated probability p, outcome o, number of cases)."""
    return sum((count * (p - outcome) ** 2 for p, outcome, count in cells), Fraction(0))


def log_loss(cells: list[tuple]) -> float | None:
    """Sum of -ln(probability given to what happened); None when a case that happened was given 0."""
    total = 0.0
    for p, outcome, count in cells:
        given = p if outcome else 1 - p
        if given == 0:
            return None
        total += count * -math.log(float(given)) + 0.0
    return total


def score_row(cells: list[tuple], reference: Fraction) -> dict:
    """Brier and logarithmic score of one forecaster on one set of cases.

    cells: (stated probability of the event, outcome 1 or 0, number of cases).
    reference: the Brier score of the base-rate forecast on the same cases.
    """
    cases = sum(count for _, _, count in cells)
    events = [cell for cell in cells if cell[1]]
    total, from_events = squared_errors(cells), squared_errors(events)
    log_total, log_events = log_loss(cells), log_loss(events)
    return {
        "squared_error_sum": shown(total, "sum"),
        "brier_score": shown(total / cases),
        "event_cases": {"squared_error_sum": shown(from_events, "sum"),
                        "share_of_the_squared_error": share(from_events, total),
                        "log_loss_sum": None if log_events is None else log_value(log_events)},
        "brier_skill_vs_base_rate": skill(total / cases, reference),
        "log_score": {"log_loss_sum": None if log_total is None else log_value(log_total),
                      "value": None if log_total is None else log_value(log_total / cases),
                      "infinite": log_total is None},
    }


def ranking(rows: dict, key) -> list[str]:
    """Names from the best (lowest) score to the worst; an infinite score comes last."""
    values = {name: key(row) for name, row in rows.items()}
    finite = [value for value in values.values() if value is not None]
    check("no two forecasters tie in a ranking", len(set(finite)) == len(finite))
    return sorted(values, key=lambda name: (values[name] is None, values[name] or 0, name))


def load_pairs(snapshot: dict) -> tuple[list[dict], dict]:
    """The forecast unit: two consecutive rows of one artifact, both labelled (a recount of extract.py)."""
    stamps = [datetime.strptime(run["timestamp"], "%Y-%m-%dT%H:%M:%SZ") for run in snapshot["runs"]]
    pairs, counts = [], {"rows": 0, "row_pairs": 0, "pairs_without_a_label": 0}
    for artifact in snapshot["artifacts"]:
        labels, flags = artifact["effectiveness_to"], artifact["baseline_flag"]
        if not len(labels) == len(flags) == len(stamps):
            raise ValueError(f"{artifact['name']}: a string is not aligned with the {len(stamps)} runs")
        rows = [(index, labels[index], flags[index] == SEED) for index in range(len(stamps)) if labels[index] != NO_ROW]
        counts["rows"] += len(rows)
        for (first, earlier, seed), (second, later, _) in zip(rows, rows[1:]):
            counts["row_pairs"] += 1
            if NO_LABEL in (earlier, later):
                counts["pairs_without_a_label"] += 1
                continue
            pairs.append({"artifact": artifact["name"], "earlier_run": first, "later_run": second,
                          "from_seed_row": seed, "changed": int(earlier != later), "labels": f"{earlier} to {later}",
                          "gap_days": (stamps[second] - stamps[first]).total_seconds() / 86400})
    return pairs, counts


def subsets(pairs: list[dict]) -> dict[str, list[dict]]:
    return {"all_usable_pairs": pairs,
            "from_a_seed_row": [pair for pair in pairs if pair["from_seed_row"]],
            "between_feeder_runs": [pair for pair in pairs if not pair["from_seed_row"]]}


def tally(pairs: list[dict]) -> dict[tuple, int]:
    """Number of pairs by (starts at a seed row, changed): all a forecaster of this lesson can see."""
    counts = {(seed, outcome): 0 for seed in (True, False) for outcome in (1, 0)}
    for pair in pairs:
        counts[(pair["from_seed_row"], pair["changed"])] += 1
    return counts


def cells_for(tallies: dict, forecaster: dict) -> list[tuple]:
    """A set of pairs as (stated probability, outcome, number of pairs) for one forecaster."""
    return [(forecaster["from_a_seed_row" if seed else "between_feeder_runs"], outcome, count)
            for (seed, outcome), count in tallies.items() if count]


def build_forecasters(cfg: dict, base_rate: Fraction) -> dict[str, dict]:
    """Each forecaster as the probability it states on a seed-row pair and on a pair between feeder runs."""
    forecasters = {}
    for name, spec in cfg["constant"].items():
        hindsight = spec["probability_of_change"] == "in_sample_base_rate"
        p = base_rate if hindsight else prob(spec["probability_of_change"])
        forecasters[name] = {"kind": "constant", "from_a_seed_row": p, "between_feeder_runs": p,
                             "uses_hindsight": hindsight, "description": spec["description"]}
    for name, spec in cfg["rule_based"].items():
        forecasters[name] = {"kind": "rule", "from_a_seed_row": prob(spec["from_a_seed_row"]),
                             "between_feeder_runs": prob(spec["between_feeder_runs"]),
                             "uses_hindsight": True, "description": spec["description"]}
    return forecasters


def describe_forecasters(forecasters: dict) -> dict:
    described = {}
    for name, forecaster in forecasters.items():
        stated = (shown(forecaster["from_a_seed_row"]) if forecaster["kind"] == "constant" else
                  {key: shown(forecaster[key]) for key in ("from_a_seed_row", "between_feeder_runs")})
        described[name] = {"kind": forecaster["kind"], "description": forecaster["description"],
                           "uses_hindsight": forecaster["uses_hindsight"], "stated_probability_of_change": stated}
    return described


def score_set(tallies: dict, forecasters: dict) -> dict:
    """Every forecaster on one set of pairs, against that set's own base rate."""
    pairs = sum(tallies.values())
    changed = sum(count for (_, outcome), count in tallies.items() if outcome)
    base_rate = Fraction(changed, pairs)
    reference = base_rate * (1 - base_rate)
    rows = {}
    for name, forecaster in forecasters.items():
        row = score_row(cells_for(tallies, forecaster), reference)
        if forecaster["kind"] == "constant":
            reliability = (forecaster["from_a_seed_row"] - base_rate) ** 2
            check("constant forecast: Brier score = (p - base rate)^2 + base rate (1 - base rate)",
                  Fraction(row["brier_score"]["exact"]) == reliability + reference)
            row["decomposition"] = {"reliability_term": shown(reliability), "uncertainty_term": shown(reference)}
            check("no constant forecast has positive Brier skill against the base rate of the set it is scored on",
                  reference == 0 or Fraction(row["brier_skill_vs_base_rate"]["exact"]) <= 0)
        rows[name] = row
    by_brier = ranking(rows, lambda row: Fraction(row["brier_score"]["exact"]))
    by_log = ranking(rows, lambda row: row["log_score"]["value"])
    for name, row in rows.items():
        row["rank_by_brier_score"], row["rank_by_log_score"] = by_brier.index(name) + 1, by_log.index(name) + 1
    return {"pairs": pairs, "changed": changed, "base_rate_of_change": shown(base_rate),
            "brier_score_of_the_base_rate_of_this_set": shown(reference),
            "forecasters": rows, "ranking_by_brier_score": by_brier, "ranking_by_log_score": by_log}


def observed_section(snapshot: dict, recount: dict, sets: dict) -> dict:
    """What the snapshot holds: the pairs, the event, and the one pair that changed."""
    described = {}
    for name, members in sets.items():
        gaps = [pair["gap_days"] for pair in members]
        changed = sum(pair["changed"] for pair in members)
        described[name] = {"pairs": len(members), "changed": changed, "unchanged": len(members) - changed,
                           "base_rate_of_change": shown(Fraction(changed, len(members))),
                           "shortest_gap_days": round(min(gaps), DECIMALS["day"]),
                           "longest_gap_days": round(max(gaps), DECIMALS["day"])}
    pairs = sets["all_usable_pairs"]
    changes = [{"artifact": pair["artifact"], "labels": pair["labels"], "from_seed_row": pair["from_seed_row"],
                "earlier_row": snapshot["runs"][pair["earlier_run"]]["timestamp"],
                "later_row": snapshot["runs"][pair["later_run"]]["timestamp"],
                "gap_days": round(pair["gap_days"], DECIMALS["day"]),
                "pairs_with_an_outcome_in_an_earlier_run": sum(other["later_run"] < pair["later_run"] for other in pairs)}
               for pair in pairs if pair["changed"]]
    return {"kind": "observed: counted from observed-input.json",
            "rows": recount["rows"], "runs": len(snapshot["runs"]), "artifacts": len(snapshot["artifacts"]),
            "row_pairs": recount["row_pairs"], "pairs_without_a_label": recount["pairs_without_a_label"],
            "usable_pairs": len(pairs),
            "unit": "one forecast = two consecutive rows of one artifact, both with an effectiveness_to label",
            "subsets": described, "changed_pairs": changes}


def cross_checks(snapshot: dict, recount: dict, sets: dict, forecasters: dict, scores: dict) -> None:
    """Accounting identities and known answers on the observed scores."""
    counts, pairs = snapshot["counts"], sets["all_usable_pairs"]
    changed = sum(pair["changed"] for pair in pairs)
    check("recount of rows and pairs equals extract.py's counts",
          (recount["rows"], recount["row_pairs"], recount["pairs_without_a_label"], len(pairs), changed)
          == (counts["rows"], counts["consecutive_pairs"]["row_pairs"], counts["consecutive_pairs"]["pairs_without_a_label"],
              counts["consecutive_pairs"]["usable_pairs"], counts["consecutive_pairs"]["changed"]))
    check("row pairs = rows - artifacts", recount["row_pairs"] == recount["rows"] - len(snapshot["artifacts"]))
    check("pairs from a seed row + pairs between feeder runs = usable pairs",
          len(sets["from_a_seed_row"]) + len(sets["between_feeder_runs"]) == len(pairs))
    if snapshot["source"]["commit"] == PINNED_COMMIT:
        check("counts at the pinned commit equal the path's shared facts",
              {"rows": recount["rows"], "artifacts": len(snapshot["artifacts"]), "usable_pairs": len(pairs),
               "changed": changed, "from_a_seed_row": len(sets["from_a_seed_row"]),
               "between_feeder_runs": len(sets["between_feeder_runs"])} == SHARED_FACTS)
    whole = scores["all_usable_pairs"]["forecasters"]
    check("the Brier score of 'never' is the share of pairs that changed",
          Fraction(whole["never"]["brier_score"]["exact"]) == Fraction(changed, len(pairs)))
    check("the base-rate forecaster is the reference on all pairs: skill 0",
          Fraction(whole["base_rate"]["brier_skill_vs_base_rate"]["exact"]) == 0)
    for name, forecaster in forecasters.items():
        parts = [Fraction(scores[subset]["forecasters"][name]["squared_error_sum"]["exact"]) for subset in SUBSETS]
        check("squared errors of the two subsets add up to those of all pairs", parts[0] == parts[1] + parts[2])
        mirrored = [(1 - p, 1 - outcome, count) for p, outcome, count in cells_for(tally(pairs), forecaster)]
        check("scoring 'unchanged' with 1 - p gives the same Brier score as scoring 'changed' with p",
              squared_errors(mirrored) == parts[0])
    finite = {name: row["log_score"]["value"] for name, row in whole.items()
              if forecasters[name]["kind"] == "constant" and not row["log_score"]["infinite"]}
    check("among constant forecasts the in-sample base rate has the lowest logarithmic score",
          min(finite, key=finite.get) == "base_rate")
    quiet = scores["between_feeder_runs"]["forecasters"]
    check("a forecast of exactly 0 has an infinite logarithmic score once the event happens",
          whole["never"]["log_score"]["infinite"] and not quiet["never"]["log_score"]["infinite"])


def hand_computed_case() -> None:
    """Four pairs worked by hand in the README: outcomes 1, 0, 0, 0; stated 0.5, 0.5, 0, 0."""
    tallies = {(True, 1): 1, (True, 0): 1, (False, 1): 0, (False, 0): 2}
    forecaster = {"from_a_seed_row": Fraction(1, 2), "between_feeder_runs": Fraction(0)}
    row = score_row(cells_for(tallies, forecaster), Fraction(1, 4) * Fraction(3, 4))
    check("hand-computed case: squared errors 1/2, Brier 1/8, skill 1/3, log score 0.346574",
          (row["squared_error_sum"]["exact"], row["brier_score"]["exact"], row["brier_skill_vs_base_rate"]["exact"],
           row["log_score"]["value"]) == ("1/2", "1/8", "1/3", 0.346574))
    sure = [(Fraction(1), 1, 1), (Fraction(0), 0, 3)]
    wrong = [(Fraction(0), 1, 1), (Fraction(1), 0, 3)]
    check("bounds: a forecast equal to the outcome scores 0, its opposite scores 1 and an infinite log score",
          (squared_errors(sure), log_loss(sure), squared_errors(wrong) / 4, log_loss(wrong)) == (0, 0.0, 1, None))


def changes_needed(pairs: int, forecasters: dict) -> dict:
    """How many changed pairs a constant p > 0 needs before it scores below 'never' on the same pairs."""
    table = {}
    for name, forecaster in forecasters.items():
        p = forecaster["from_a_seed_row"]
        if forecaster["kind"] != "constant" or p == 0:
            continue
        quotient = pairs * p / 2
        needed = math.floor(quotient) + 1
        better = [k for k in range(pairs + 1) if k * (1 - p) ** 2 + (pairs - k) * p ** 2 < k]
        check("brute force: a constant p beats 'never' exactly when the changed pairs exceed pairs * p / 2",
              better == list(range(needed, pairs + 1)))
        table[name] = {"stated_probability_of_change": shown(p), "pairs": pairs,
                       "pairs_times_p_over_2": shown(quotient, "sum"), "changed_pairs_needed": needed}
    return table


def kind_of(seed: bool, outcome: int) -> str:
    return ("changed" if outcome else "unchanged") + (", from a seed row" if seed else ", between feeder runs")


def one_pair_section(pairs: list[dict], forecasters: dict, scores: dict) -> dict:
    """Leave one pair out and rank again: how many removals alter the ranking by Brier score?"""
    tallies = tally(pairs)
    whole = scores["all_usable_pairs"]
    full = whole["ranking_by_brier_score"]
    removals, same = [], 0
    for (seed, outcome), count in tallies.items():
        if not count:
            continue
        reduced = dict(tallies)
        reduced[(seed, outcome)] -= 1
        rows = {}
        for name, forecaster in forecasters.items():
            cells = cells_for(reduced, forecaster)
            loss = log_loss(cells)
            rows[name] = {"brier_score": shown(squared_errors(cells) / (len(pairs) - 1)),
                          "log_score": {"value": None if loss is None else log_value(loss / (len(pairs) - 1)),
                                        "infinite": loss is None}}
        order = ranking(rows, lambda row: Fraction(row["brier_score"]["exact"]))
        by_log = ranking(rows, lambda row: row["log_score"]["value"])
        same += count * (order == full)
        removals.append({"removed_pair": kind_of(seed, outcome), "pairs_of_this_kind": count,
                         "ranking_by_brier_score": order, "same_as_the_ranking_on_all_pairs": order == full,
                         "brier_scores": {name: rows[name]["brier_score"] for name in order},
                         "ranking_by_log_score": by_log,
                         "log_scores": {name: rows[name]["log_score"] for name in by_log}})
    check("leave-one-out removals account for every pair",
          sum(removal["pairs_of_this_kind"] for removal in removals) == len(pairs))
    never, base = (Fraction(whole["forecasters"][name]["brier_score"]["exact"]) for name in ("never", "base_rate"))
    check("'never' trails the base-rate forecast by the square of the base rate",
          never - base == Fraction(whole["base_rate_of_change"]["exact"]) ** 2)
    first = Fraction(whole["forecasters"][full[0]]["brier_score"]["exact"])
    return {"kind": "computed; every forecaster keeps the probabilities it states on all pairs",
            "ranking_on_all_pairs": full,
            "ranking_between_feeder_runs": scores["between_feeder_runs"]["ranking_by_brier_score"],
            "leave_one_pair_out": {"removals": len(pairs), "removals_that_keep_the_ranking": same,
                                   "removals_that_change_the_ranking": len(pairs) - same,
                                   "by_kind_of_removed_pair": removals},
            "lead_of_the_base_rate_over_never": shown(never - base),
            "lead_of_the_first_forecaster_over_the_base_rate": {"forecaster": full[0], **shown(base - first)},
            "changed_pairs_needed_to_beat_never": changes_needed(len(pairs), forecasters)}


def expected_scores(truth: Fraction, stated: Fraction) -> dict:
    """Expected score per case when the event has probability `truth` and the forecaster states `stated`."""
    brier = truth * (1 - stated) ** 2 + (1 - truth) * stated ** 2
    absolute = truth * (1 - stated) + (1 - truth) * stated
    check("expected Brier score = (stated - truth)^2 + truth (1 - truth)",
          brier == (stated - truth) ** 2 + truth * (1 - truth))
    log = log_loss([(stated, 1, truth), (stated, 0, 1 - truth)])
    return {"brier": brier, "absolute_error": absolute, "log_score": None if log is None else log_value(log)}


def proper_case(case: dict, grid: list[Fraction], draws: int, tolerance: int) -> dict:
    """One assumed true probability: expected scores on the grid, then a seeded sample of cases."""
    truth = prob(case["true_probability"])
    if truth not in grid:
        raise ValueError("the true probability must be one of the stated probabilities")
    rng = random.Random(case["seed"])
    events = sum(rng.random() < float(truth) for _ in range(draws))
    check("simulated frequency lies within the stated number of standard errors of the true probability",
          (events - draws * truth) ** 2 <= tolerance ** 2 * draws * truth * (1 - truth))
    rows, expected, simulated = [], {}, {}
    for stated in grid:
        scores = expected_scores(truth, stated)
        sample = [(stated, 1, events), (stated, 0, draws - events)]
        mean_brier = squared_errors(sample) / draws
        mean_absolute = (events * (1 - stated) + (draws - events) * stated) / draws
        expected[stated], simulated[stated] = scores, {"brier": mean_brier, "absolute_error": mean_absolute}
        rows.append({"stated": float(stated), "expected_brier": shown(scores["brier"], "ratio"),
                     "expected_brier_above_its_minimum": shown((stated - truth) ** 2, "ratio"),
                     "expected_absolute_error": shown(scores["absolute_error"], "ratio"),
                     "expected_log_score": scores["log_score"],
                     "simulated_brier": round(float(mean_brier), DECIMALS["ratio"]),
                     "simulated_absolute_error": round(float(mean_absolute), DECIMALS["ratio"])})
    lowest = {rule: float(min(grid, key=lambda q: expected[q][rule])) for rule in ("brier", "absolute_error")}
    lowest["log_score"] = float(min((q for q in grid if expected[q]["log_score"] is not None),
                                    key=lambda q: expected[q]["log_score"]))
    lowest_simulated = {rule: float(min(grid, key=lambda q: simulated[q][rule])) for rule in ("brier", "absolute_error")}
    corner = float(0 if truth < Fraction(1, 2) else 1)
    check("proper: expected Brier and logarithmic scores are lowest at the true probability",
          lowest["brier"] == lowest["log_score"] == float(truth))
    check("not proper: expected absolute error is lowest at 0 or 1, not at the true probability",
          lowest["absolute_error"] == corner != float(truth))
    check("the simulated means are lowest at the same stated probabilities as the expected scores",
          lowest_simulated == {"brier": float(truth), "absolute_error": corner})
    deviation = abs(events - draws * truth) / math.sqrt(draws * truth * (1 - truth))
    return {"true_probability": shown(truth, "ratio"), "by_stated_probability": rows,
            "lowest_expected_score_at": lowest,
            "simulation": {"seed": case["seed"], "draws": draws, "events": events,
                           "frequency": shown(Fraction(events, draws), "ratio"),
                           "standard_errors_from_the_true_probability": round(float(deviation), 2),
                           "lowest_mean_score_at": lowest_simulated}}


def proper_scoring_section(cfg: dict) -> dict:
    grid = [prob(value) for value in cfg["stated_probabilities"]]
    return {"kind": "synthetic: assumed true probabilities, closed-form expectations and a seeded sample",
            "definition": "A scoring rule is proper when a forecaster's expected score is best if the stated "
                          "probability equals the probability the forecaster believes.",
            "formulas": {"expected_brier": "t (1 - q)^2 + (1 - t) q^2 = (q - t)^2 + t (1 - t)",
                         "expected_absolute_error": "t (1 - q) + (1 - t) q = t + q (1 - 2 t)",
                         "expected_log_score": "-t ln q - (1 - t) ln(1 - q), natural logarithm"},
            "draws_per_case": cfg["draws"],
            "cases": [proper_case(case, grid, cfg["draws"], cfg["tolerance_in_standard_errors"]) for case in cfg["cases"]]}


def exercise_1(p: Fraction, tallies: dict, scores: dict) -> dict:
    """A constant forecaster that is not in the lesson's table, term by term."""
    pairs, changed = sum(tallies.values()), sum(count for (_, outcome), count in tallies.items() if outcome)
    whole, feeder = scores["all_usable_pairs"], scores["between_feeder_runs"]
    row = score_row([(p, 1, changed), (p, 0, pairs - changed)],
                    Fraction(whole["brier_score_of_the_base_rate_of_this_set"]["exact"]))
    return {"stated": float(p), "changed_pairs": changed, "unchanged_pairs": pairs - changed,
            "squared_error_of_the_changed_pairs": row["event_cases"]["squared_error_sum"],
            "squared_error_of_the_unchanged_pairs": shown((pairs - changed) * p ** 2, "sum"),
            "squared_error_sum": row["squared_error_sum"], "brier_score": row["brier_score"],
            "brier_score_between_feeder_runs": shown(squared_errors([(p, 0, feeder["pairs"])]) / feeder["pairs"]),
            "share_of_the_changed_pairs": row["event_cases"]["share_of_the_squared_error"],
            "squared_error_sum_of_the_base_rate": whole["forecasters"]["base_rate"]["squared_error_sum"],
            "brier_skill_vs_base_rate": row["brier_skill_vs_base_rate"]}


def exercise_2(name: str, tallies: dict, forecasters: dict, scores: dict, one_pair: dict) -> dict:
    """The rule-based forecaster group by group, and what is left of it without the changed pair."""
    groups = []
    for (seed, outcome), count in tallies.items():
        if count:
            error = (forecasters[name]["from_a_seed_row" if seed else "between_feeder_runs"] - outcome) ** 2
            groups.append({"pairs": kind_of(seed, outcome), "count": count,
                           "stated": float(forecasters[name]["from_a_seed_row" if seed else "between_feeder_runs"]),
                           "squared_error_each": shown(error, "sum"), "squared_error": shown(count * error, "sum")})
    rows = scores["all_usable_pairs"]["forecasters"]
    row = rows[name]
    total, from_changed = (Fraction(part["squared_error_sum"]["exact"]) for part in (row, row["event_cases"]))
    check("exercise 2: the groups add up to the forecaster's squared-error sum",
          sum(Fraction(group["squared_error"]["exact"]) for group in groups) == total)
    without = next(removal for removal in one_pair["leave_one_pair_out"]["by_kind_of_removed_pair"]
                   if removal["removed_pair"].startswith("changed"))
    return {"forecaster": name, "groups": groups, "squared_error_sum": row["squared_error_sum"],
            "brier_score": row["brier_score"],
            "share_of_the_changed_pair": row["event_cases"]["share_of_the_squared_error"],
            "squared_error_sum_of_the_base_rate": rows["base_rate"]["squared_error_sum"],
            "brier_skill_vs_base_rate": row["brier_skill_vs_base_rate"], "rank_on_all_pairs": row["rank_by_brier_score"],
            "without_the_changed_pair": {"pairs": sum(tallies.values()) - 1,
                                         "squared_error_sum": shown(total - from_changed, "sum"),
                                         "brier_score": without["brier_scores"][name],
                                         "rank": without["ranking_by_brier_score"].index(name) + 1}}


def exercise_5(whole: dict, feeder: dict) -> dict:
    """Logarithmic score of one forecaster with and without the changed pair, from the stored (rounded) sums."""
    total, from_changed = whole["log_score"]["log_loss_sum"], whole["event_cases"]["log_loss_sum"]
    part = None if total is None else round(100 * from_changed / total, DECIMALS["percent"])
    return {"between_feeder_runs": feeder["log_score"], "all_usable_pairs": whole["log_score"],
            "log_loss_of_the_changed_pair": from_changed,
            "share_of_the_log_loss_from_the_changed_pair_percent": part}


def worked_examples(cfg: dict, tallies: dict, forecasters: dict, scores: dict, one_pair: dict) -> dict:
    """Intermediate values of the lesson's exercises that the tables do not show."""
    truth = prob(cfg["exercise_4_true_probability"])
    stated = [prob(value) for value in cfg["exercise_4_stated_probabilities"]]
    whole, feeder = scores["all_usable_pairs"]["forecasters"], scores["between_feeder_runs"]["forecasters"]
    needed = one_pair["changed_pairs_needed_to_beat_never"]
    return {
        "kind": "computed on the observed pairs (exercises 1, 2, 3 and 5) and synthetic (exercise 4)",
        "exercise_1": exercise_1(prob(cfg["exercise_1_stated_probability"]), tallies, scores),
        "exercise_2": exercise_2(cfg["exercise_2_forecaster"], tallies, forecasters, scores, one_pair),
        "exercise_3": {name: needed[name] for name in cfg["exercise_3_forecasters"]},
        "exercise_4": {"true_probability": float(truth),
                       "expected": [{"stated": float(q), "brier": shown(expected_scores(truth, q)["brier"], "ratio"),
                                     "absolute_error": shown(expected_scores(truth, q)["absolute_error"], "ratio")}
                                    for q in stated]},
        "exercise_5": {name: exercise_5(whole[name], feeder[name]) for name in cfg["exercise_5_forecasters"]},
    }


def hypothesis_check(cfg: dict, forecasters: dict, scores: dict, proper: dict) -> dict:
    """The research cycle's hypothesis, written before the first run, against the results."""
    limit, allowed = prob(cfg["constant_forecasts_up_to"]), prob(cfg["maximum_spread_of_brier_scores"])
    constant = {name: row for name, row in scores["all_usable_pairs"]["forecasters"].items()
                if forecasters[name]["kind"] == "constant"}
    rows = {name: row for name, row in constant.items() if forecasters[name]["from_a_seed_row"] <= limit}
    briers = [Fraction(row["brier_score"]["exact"]) for row in rows.values()]
    spread = max(briers) - min(briers)
    shares = [row["event_cases"]["share_of_the_squared_error"]["percent"] for row in rows.values()]
    skills = [Fraction(row["brier_skill_vs_base_rate"]["exact"]) for row in constant.values()]
    lowest = [(case["true_probability"]["value"], case["lowest_expected_score_at"]) for case in proper["cases"]]
    parts = {
        "brier_scores_of_small_constant_forecasts_lie_within_the_stated_spread": spread < allowed,
        "the_changed_pair_supplies_most_of_each_of_those_scores":
            min(shares) > cfg["minimum_share_of_the_changed_pair_percent"],
        "no_constant_forecast_has_positive_brier_skill": max(skills) <= 0,
        "a_forecast_of_exactly_0_has_an_infinite_log_score": constant["never"]["log_score"]["infinite"],
        "expected_brier_is_lowest_at_the_true_probability": all(at["brier"] == truth for truth, at in lowest),
        "expected_absolute_error_is_not": all(at["absolute_error"] != truth for truth, at in lowest),
    }
    return {"kind": "computed; the thresholds are those of the hypothesis in the research-cycle record",
            "constant_forecasts_considered": list(rows), "spread_of_their_brier_scores": shown(spread),
            "maximum_spread_in_the_hypothesis": float(allowed),
            "smallest_share_of_the_changed_pair_percent": min(shares),
            "largest_brier_skill_of_a_constant_forecast": shown(max(skills), "ratio"),
            "parts": parts, "every_part_holds": all(parts.values()),
            "note": "Two parts are identities and could not have failed: a constant forecast cannot beat the base rate of "
                    "the set it is scored on, and -ln(0) is infinite. The spread and the share are the empirical parts."}


def negative_controls(snapshot: dict, forecasters: dict, scores: dict) -> dict:
    """Plant one flipped label in a copy of the snapshot: the zero count between feeder runs must move."""
    runs = len(snapshot["runs"])
    target = next(a["name"] for a in snapshot["artifacts"]
                  if a["first_run_index"] == 0 and len(set(a["effectiveness_to"])) == 1)
    index = runs // 2
    planted = copy.deepcopy(snapshot)
    artifact = next(a for a in planted["artifacts"] if a["name"] == target)
    original = artifact["effectiveness_to"][index]
    other = "D" if original != "D" else "T"
    labels = artifact["effectiveness_to"]
    artifact["effectiveness_to"] = labels[:index] + other + labels[index + 1:]
    pairs, _ = load_pairs(planted)
    after = {name: score_set(tally(members), forecasters) for name, members in subsets(pairs).items()}
    before_after = {}
    for subset in ("all_usable_pairs", "between_feeder_runs"):
        never = [version[subset]["forecasters"]["never"] for version in (scores, after)]
        before_after[subset] = {
            "changed_pairs": [scores[subset]["changed"], after[subset]["changed"]],
            "brier_score_of_never": [row["brier_score"]["exact"] for row in never],
            "log_score_of_never_is_infinite": [row["log_score"]["infinite"] for row in never]}
    quiet = before_after["between_feeder_runs"]
    check("negative control: one planted label flip adds two changed pairs, both between feeder runs",
          all(counts["changed_pairs"][1] == counts["changed_pairs"][0] + 2 for counts in before_after.values()))
    check("negative control: the zero Brier score of 'never' between feeder runs becomes 2 / pairs",
          Fraction(quiet["brier_score_of_never"][1]) == Fraction(2, scores["between_feeder_runs"]["pairs"]))
    check("negative control: the logarithmic score of 'never' between feeder runs becomes infinite",
          quiet["log_score_of_never_is_infinite"] == [False, True])
    return {"planted_in": {"artifact": target, "run_index": index, "run": snapshot["runs"][index]["timestamp"],
                           "observed_label": original, "label_flipped_to": other},
            "before_and_after_the_flip": before_after}


def transfer_task(task: dict) -> dict:
    """Expected answers of the learner task, from the hypothetical release log in scenarios.json."""
    releases, rollbacks = task["releases"], task["rollbacks"]
    base_rate = Fraction(rollbacks, releases)
    reference = base_rate * (1 - base_rate)
    check("transfer task: 'climate' states the base rate of the log",
          prob(task["constant_forecasters"]["climate"]) == base_rate)
    groups = list(task["watcher"].values())
    check("transfer task: the watcher's two groups account for every release and every rollback",
          (sum(g["releases"] for g in groups), sum(g["rollbacks"] for g in groups)) == (releases, rollbacks))
    rows = {name: score_row([(prob(p), 1, rollbacks), (prob(p), 0, releases - rollbacks)], reference)
            for name, p in task["constant_forecasters"].items()}
    cells, terms = [], []
    for name, group in task["watcher"].items():
        p, hit, quiet = prob(group["stated"]), group["rollbacks"], group["releases"] - group["rollbacks"]
        cells += [(p, 1, hit), (p, 0, quiet)]
        terms.append({"group": name, "stated": float(p), "releases": group["releases"], "rollbacks": hit,
                      "squared_error_of_the_rollbacks": shown(hit * (1 - p) ** 2, "sum"),
                      "squared_error_of_the_other_releases": shown(quiet * p ** 2, "sum"),
                      "log_loss_of_the_rollbacks": log_value(log_loss([(p, 1, hit)])),
                      "log_loss_of_the_other_releases": log_value(log_loss([(p, 0, quiet)]))})
    rows["watcher"] = score_row(cells, reference)
    belief = prob(task["question_4_belief"])
    statements = []
    for stated in task["question_4_statements"]:
        expected = expected_scores(belief, prob(stated))
        statements.append({"stated": float(prob(stated)), "expected_brier": shown(expected["brier"], "ratio"),
                           "expected_absolute_error": shown(expected["absolute_error"], "ratio")})
    return {"note": task["note"], "event": task["event"], "releases": releases, "rollbacks": rollbacks,
            "base_rate": shown(base_rate, "ratio"), "brier_score_of_the_base_rate": shown(reference),
            "q1_q2_q3_forecasters": rows, "q3_watcher_term_by_term": terms,
            "q3_ranking_by_brier_score": ranking(rows, lambda row: Fraction(row["brier_score"]["exact"])),
            "q3_ranking_by_log_score": ranking(rows, lambda row: row["log_score"]["value"]),
            "q4_belief": float(belief), "q4_expected_scores": statements}


def analyze(snapshot: dict, scenarios: dict) -> dict:
    if scenarios["rounding"] != {f"{key}_decimals": value for key, value in DECIMALS.items()}:
        raise ValueError("scenarios.json rounding does not match analyze.py")
    hand_computed_case()
    pairs, recount = load_pairs(snapshot)
    sets = subsets(pairs)
    base_rate = Fraction(sum(pair["changed"] for pair in pairs), len(pairs))
    forecasters = build_forecasters(scenarios["forecasters"], base_rate)
    scores = {name: score_set(tally(members), forecasters) for name, members in sets.items()}
    cross_checks(snapshot, recount, sets, forecasters, scores)
    one_pair = one_pair_section(pairs, forecasters, scores)
    proper = proper_scoring_section(scenarios["proper_scoring"])
    result = {
        "module_id": snapshot["module_id"],
        "rounding": "Brier scores to 9 decimals; squared-error sums, skills and expected scores to 6; percentages to 2; "
                    "logarithmic scores and log-loss sums to 6 (natural logarithm); days to 3; 'exact' is the unrounded fraction",
        "source": {"repository": snapshot["source"]["repository"], "commit": snapshot["source"]["commit"],
                   "files": [entry["path"] for entry in snapshot["source"]["files"]]},
        "observed": observed_section(snapshot, recount, sets),
        "event": scenarios["event"],
        "forecasters": {"kind": "synthetic forecasters (assumed probabilities) scored on the observed pairs"}
                       | describe_forecasters(forecasters),
        "scores": {"kind": "computed", "brier_score": "mean of (p - o)^2 over the pairs, o = 1 if the label changed",
                   "log_score": "mean of -ln(probability given to what happened); infinite if that probability is 0",
                   "brier_skill": "1 - Brier score / Brier score of the base rate of the same set"} | scores,
        "one_pair": one_pair,
        "proper_scoring": proper,
        "hypothesis_check": hypothesis_check(scenarios["hypothesis_check"], forecasters, scores, proper),
        "worked_examples": worked_examples(scenarios["worked_examples"], tally(pairs), forecasters, scores, one_pair),
        "negative_controls": negative_controls(snapshot, forecasters, scores),
        "transfer_task": transfer_task(scenarios["transfer_task"]),
    }
    result["checks"] = [{"check": name, "times_evaluated": times, "passed": True} for name, times in CHECKS.items()]
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--input", type=Path, default=HERE / "observed-input.json")
    parser.add_argument("--scenarios", type=Path, default=HERE / "scenarios.json")
    parser.add_argument("--output", type=Path, default=HERE / "results.json")
    parser.add_argument("--check", action="store_true",
                        help="recompute and compare with the output file instead of writing it")
    args = parser.parse_args()
    try:
        result = analyze(json.loads(args.input.read_text(encoding="utf-8")),
                         json.loads(args.scenarios.read_text(encoding="utf-8")))
    except (AssertionError, ArithmeticError, KeyError, ValueError, OSError) as exc:
        print(f"analyze.py: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 1
    text = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.check:
        same = args.output.read_bytes().replace(b"\r\n", b"\n") == text.encode("utf-8")
        print(f"analyze.py: {args.output.name} {'matches' if same else 'DIFFERS FROM'} a fresh run "
              f"({len(CHECKS)} self-checks passed)")
        return 0 if same else 1
    with open(args.output, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(text)
    print(f"analyze.py: {len(CHECKS)} self-checks passed -> {args.output.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
