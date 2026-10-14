#!/usr/bin/env python3
"""PSY-005 analysis: the persistence baseline on the effectiveness labels.

Reads observed-input.json (written by extract.py) and scenarios.json, never
the repository, and writes results.json. Everything is an exact count or a
ratio of counts; no random number is drawn.

Run from the repository root:
    python -I state/streeling/fixtures/psychohistory/psy-005/analyze.py
    python -I state/streeling/fixtures/psychohistory/psy-005/analyze.py --check
"""

from __future__ import annotations

import argparse
import copy
import json
import math
import sys
from datetime import datetime, timezone
from fractions import Fraction
from pathlib import Path

HERE = Path(__file__).resolve().parent
NO_ROW, NO_LABEL, SEED = ".", "-", "s"
DECIMALS = {"ratio": 6, "percent": 2, "day": 3}
CHECKS: dict[str, int] = {}  # self-check -> times evaluated


def check(name: str, condition: bool, detail: str = "") -> None:
    """A self-check that can fail: abort instead of writing a wrong result."""
    if not condition:
        raise AssertionError(f"self-check failed: {name}" + (f" ({detail})" if detail else ""))
    CHECKS[name] = CHECKS.get(name, 0) + 1


def ratio(numerator: int, denominator: int) -> dict:
    if denominator == 0:
        return {"exact": f"{numerator}/0", "value": None, "percent": None}
    value = Fraction(numerator, denominator)
    return {"exact": f"{numerator}/{denominator}", "value": round(float(value), DECIMALS["ratio"]),
            "percent": round(float(100 * value), DECIMALS["percent"])}


def skill(errors: int, reference_errors: int) -> dict:
    """Skill of accuracy against a reference on the same pairs: 1 - E / E_ref."""
    if reference_errors == 0:
        return {"exact": "undefined: the reference made no error", "value": None}
    value = 1 - Fraction(errors, reference_errors)
    return {"exact": str(value), "value": round(float(value), DECIMALS["ratio"])}


def load_rows(snapshot: dict) -> dict[str, list[tuple]]:
    """Per artifact, its rows in run order: (run_index, from, to, is_seed)."""
    runs = len(snapshot["runs"])
    table = {}
    for artifact in snapshot["artifacts"]:
        strings = [artifact[key] for key in ("effectiveness_from", "effectiveness_to", "baseline_flag")]
        if any(len(string) != runs for string in strings):
            raise ValueError(f"{artifact['name']}: a label string is not aligned with the {runs} runs")
        rows = []
        for index, (label_from, label_to, flag) in enumerate(zip(*strings)):
            if len({label_from == NO_ROW, label_to == NO_ROW, flag == NO_ROW}) != 1:
                raise ValueError(f"{artifact['name']}: run {index} is a row in one string and not in another")
            if label_to != NO_ROW:
                rows.append((index, None if label_from == NO_LABEL else label_from,
                             None if label_to == NO_LABEL else label_to, flag == SEED))
        table[artifact["name"]] = rows
    return table


def count_rows(table: dict) -> dict:
    classes = {"both_labels": 0, "from_missing_only": 0, "to_missing_only": 0, "both_missing": 0}
    for rows in table.values():
        for _, label_from, label_to, _ in rows:
            classes["both_labels" if label_from and label_to else "from_missing_only" if label_to
                    else "to_missing_only" if label_from else "both_missing"] += 1
    return classes


def consecutive_pairs(table: dict) -> tuple[list[dict], int, int]:
    """The forecast unit: two consecutive rows of one artifact, both labelled.

    Returns the usable pairs, the number of row pairs, and how many rows carry
    an effectiveness_from that differs from the previous row's effectiveness_to.
    """
    pairs, row_pairs, mismatches = [], 0, 0
    for name, rows in table.items():
        for earlier, later in zip(rows, rows[1:]):
            row_pairs += 1
            mismatches += later[1] != earlier[2]
            if earlier[2] and later[2]:
                pairs.append({"artifact": name, "earlier_run": earlier[0], "later_run": later[0],
                              "earlier_label": earlier[2], "later_label": later[2], "from_seed_row": earlier[3]})
    return pairs, row_pairs, mismatches


def in_row_pairs(table: dict) -> list[dict]:
    """The cross-check unit: effectiveness_from and effectiveness_to of one row."""
    return [{"artifact": name, "later_run": row[0], "earlier_label": row[1], "later_label": row[2], "seed_row": row[3]}
            for name, rows in table.items() for row in rows if row[1] and row[2]]


def tally(pairs: list[dict]) -> dict:
    changed = sum(pair["earlier_label"] != pair["later_label"] for pair in pairs)
    return {"pairs": len(pairs), "changed": changed, "unchanged": len(pairs) - changed}


def persistence(pairs: list[dict]) -> dict:
    counts = tally(pairs)
    return counts | {"persistence_errors": counts["changed"],
                     "persistence_accuracy": ratio(counts["unchanged"], counts["pairs"]),
                     "base_rate_of_change": ratio(counts["changed"], counts["pairs"])}


def score_model(pairs: int, changes: int, called: int, false_alarms: int) -> dict:
    """A forecaster described by its calls, on `pairs` forecasts holding `changes` changes."""
    missed = changes - called
    errors = missed + false_alarms
    alarms = called + false_alarms
    if not (0 <= called <= changes and 0 <= false_alarms <= pairs - changes):
        raise ValueError("a model's calls do not fit the number of changed and unchanged pairs")
    if changes:
        accuracy, reference = Fraction(pairs - errors, pairs), Fraction(pairs - changes, pairs)
        check("skill identity (A - A_ref)/(1 - A_ref) = 1 - E/E_ref",
              (accuracy - reference) / (1 - reference) == 1 - Fraction(errors, changes))
    return {"changes_called": called, "changes_missed": missed, "false_alarms": false_alarms, "alarms": alarms,
            "errors": errors, "accuracy": ratio(pairs - errors, pairs), "skill_vs_persistence": skill(errors, changes),
            "share_of_changes_called": ratio(called, changes), "share_of_alarms_that_were_false": ratio(false_alarms, alarms)}


def gap_days(snapshot: dict, earlier: int, later: int) -> float:
    stamps = [datetime.strptime(snapshot["runs"][index]["timestamp"], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
              for index in (earlier, later)]
    return (stamps[1] - stamps[0]).total_seconds() / 86400


def horizon(snapshot: dict, pair: dict, bounds: dict) -> str:
    if pair["from_seed_row"]:
        return "from_a_seed_row"
    gap = gap_days(snapshot, pair["earlier_run"], pair["later_run"])
    if gap < bounds["about_a_day_from"]:
        return "feeder_runs_under_half_a_day_apart"
    return "feeder_runs_about_a_day_apart" if gap <= bounds["about_a_day_to"] else "feeder_runs_further_apart"


def hand_computed_case() -> None:
    """Two artifacts over four runs, worked by hand in the README."""
    toy = {"runs": [{"timestamp": f"2026-01-0{day}T00:00:00Z"} for day in range(1, 5)],
           "artifacts": [
               {"name": "a", "effectiveness_from": "-TTF", "effectiveness_to": "TTFF", "baseline_flag": "----"},
               {"name": "b", "effectiveness_from": ".-P-", "effectiveness_to": ".P-P", "baseline_flag": ".---"}]}
    table = load_rows(toy)
    pairs, row_pairs, mismatches = consecutive_pairs(table)
    check("hand-computed case: 7 rows, 5 row pairs, 3 usable pairs, 1 changed, accuracy 2/3, in-row pairs 3, 0 mismatches",
          (sum(map(len, table.values())), row_pairs, tally(pairs), persistence(pairs)["persistence_accuracy"]["exact"],
           len(in_row_pairs(table)), mismatches) == (7, 5, {"pairs": 3, "changed": 1, "unchanged": 2}, "2/3", 3, 0))


def negative_controls(snapshot: dict, bounds: dict, base: dict) -> dict:
    """Plant a defect in a copy of the snapshot and confirm each counter sees it."""
    target = next(a["name"] for a in snapshot["artifacts"] if a["consecutive_changed"] == 0 and a["first_run_index"] == 0)
    index = len(snapshot["runs"]) // 2

    def recount(replacement: str) -> tuple[dict, int, dict]:
        planted = copy.deepcopy(snapshot)
        artifact = next(a for a in planted["artifacts"] if a["name"] == target)
        labels = artifact["effectiveness_to"]
        artifact["effectiveness_to"] = labels[:index] + replacement + labels[index + 1:]
        pairs, _, mismatches = consecutive_pairs(load_rows(planted))
        between = [pair for pair in pairs if horizon(planted, pair, bounds) != "from_a_seed_row"]
        return tally(pairs), mismatches, tally(between)

    original = next(a for a in snapshot["artifacts"] if a["name"] == target)["effectiveness_to"][index]
    other = "D" if original != "D" else "T"
    flipped, flipped_mismatches, flipped_between = recount(other)
    blanked, _, _ = recount(NO_LABEL)
    check("negative control: one planted label flip is counted as two changed pairs",
          flipped["changed"] == base["changed"] + 2 and flipped["pairs"] == base["pairs"])
    check("negative control: the zero count between feeder runs can become non-zero",
          flipped_between["changed"] == base["between_feeder_runs_changed"] + 2)
    check("negative control: a label that no longer matches effectiveness_from is reported",
          flipped_mismatches == base["mismatches"] + 1)
    check("negative control: one blanked label in mid-history removes two usable pairs",
          blanked["pairs"] == base["pairs"] - 2 and blanked["changed"] == base["changed"])
    return {
        "planted_in": {"artifact": target, "run_index": index, "run": snapshot["runs"][index]["timestamp"],
                       "observed_label": original},
        "label_flipped_to": other,
        "changed_pairs_before_and_after_the_flip": [base["changed"], flipped["changed"]],
        "changed_pairs_between_feeder_runs_before_and_after_the_flip":
            [base["between_feeder_runs_changed"], flipped_between["changed"]],
        "from_to_mismatches_before_and_after_the_flip": [base["mismatches"], flipped_mismatches],
        "usable_pairs_before_and_after_blanking_the_label": [base["pairs"], blanked["pairs"]],
    }


def transfer_task(task: dict) -> dict:
    artifacts = sum(group["artifacts"] for group in task["artifact_groups"])
    rows = sum(group["artifacts"] * group["rows_each"] for group in task["artifact_groups"])
    row_pairs = rows - artifacts
    pairs = row_pairs - 2 * task["rows_without_a_label_in_mid_history"]
    changes = task["changed_pairs"]
    cost = task["miss_to_false_alarm_cost_ratio"]
    models = {name: score_model(pairs, changes, model["changes_called"], model["false_alarms"])
              for name, model in task["models"].items()}
    for model in models.values():
        model["weighted_cost"] = cost * model["changes_missed"] + model["false_alarms"]
    return {
        "note": task["note"],
        "q1_counting": {"artifacts": artifacts, "rows": rows, "row_pairs": row_pairs, "usable_pairs": pairs,
                        "changed_pairs": changes, "unchanged_pairs": pairs - changes,
                        "persistence_accuracy": ratio(pairs - changes, pairs),
                        "base_rate_of_change": ratio(changes, pairs)},
        "q2_q3_q4_models": models,
        "q4_cost": {"miss_to_false_alarm_cost_ratio": cost, "persistence_weighted_cost": cost * changes,
                    "ranking_by_accuracy": sorted(models, key=lambda name: (-models[name]["accuracy"]["value"], name)),
                    "ranking_by_weighted_cost": sorted(models, key=lambda name: (models[name]["weighted_cost"], name))},
    }


def analyze(snapshot: dict, scenarios: dict) -> dict:
    if scenarios["rounding"] != {f"{key}_decimals": value for key, value in DECIMALS.items()}:
        raise ValueError("scenarios.json rounding does not match analyze.py")
    bounds = scenarios["horizon_bounds_days"]
    counts = snapshot["counts"]
    table = load_rows(snapshot)
    pairs, row_pairs, mismatches = consecutive_pairs(table)
    inside = in_row_pairs(table)
    classes = count_rows(table)
    rows = sum(map(len, table.values()))
    all_pairs = persistence(pairs)
    n, changes = all_pairs["pairs"], all_pairs["changed"]

    hand_computed_case()
    check("recount of rows, runs, dates and artifacts equals extract.py's counts",
          (rows, len(snapshot["runs"]), len({run["timestamp"][:10] for run in snapshot["runs"]}), len(table))
          == (counts["rows"], counts["runs"], counts["run_dates_utc"], counts["artifacts"]))
    check("recount of label presence classes equals extract.py's counts", classes == counts["rows_by_label_presence"])
    check("recount of consecutive pairs equals extract.py's counts",
          (row_pairs, n, changes, all_pairs["unchanged"], mismatches)
          == tuple(counts["consecutive_pairs"][key] for key in ("row_pairs", "usable_pairs", "changed", "unchanged",
                                                                "from_differs_from_previous_to")))
    check("recount of in-row pairs equals extract.py's counts",
          tally(inside) | {"seed_rows_among_pairs": sum(pair["seed_row"] for pair in inside)} == counts["in_row_pairs"])
    check("label presence classes sum to the rows", sum(classes.values()) == rows)
    check("row pairs = rows - artifacts", row_pairs == rows - len(table))
    check("usable pairs = row pairs - pairs without a label",
          n == row_pairs - counts["consecutive_pairs"]["pairs_without_a_label"])
    check("changed + unchanged = usable pairs", changes + all_pairs["unchanged"] == n)
    not_seed = {(pair["artifact"], pair["later_run"], pair["earlier_label"], pair["later_label"])
                for pair in inside if not pair["seed_row"]}
    check("in-row pairs outside seed rows are exactly the consecutive pairs",
          not_seed == {(pair["artifact"], pair["later_run"], pair["earlier_label"], pair["later_label"]) for pair in pairs}
          and len(not_seed) == n == len(inside) - sum(pair["seed_row"] for pair in inside))
    check("every pair joins two neighbouring runs", all(pair["later_run"] == pair["earlier_run"] + 1 for pair in pairs))

    per_artifact = []
    for name, artifact_rows in table.items():
        own = persistence([pair for pair in pairs if pair["artifact"] == name])
        labels = sorted({row[2] for row in artifact_rows if row[2]})
        per_artifact.append({"artifact": name, "rows": len(artifact_rows),
                             "first_row": snapshot["runs"][artifact_rows[0][0]]["timestamp"], "labels_seen": labels}
                            | {key: own[key] for key in ("pairs", "changed", "unchanged", "persistence_accuracy")})
    check("per-artifact pairs and changes sum to the totals",
          (sum(a["pairs"] for a in per_artifact), sum(a["changed"] for a in per_artifact)) == (n, changes))

    per_run = []
    for index in range(1, len(snapshot["runs"])):
        own = tally([pair for pair in pairs if pair["later_run"] == index])
        per_run.append({"run": snapshot["runs"][index]["timestamp"], "rows": snapshot["runs"][index]["rows"],
                        "days_since_previous_run": round(gap_days(snapshot, index - 1, index), DECIMALS["day"])} | own)
    check("per-run pairs and changes sum to the totals",
          (sum(r["pairs"] for r in per_run), sum(r["changed"] for r in per_run)) == (n, changes))
    quiet_runs = sum(run["changed"] == 0 for run in per_run)

    names = ("from_a_seed_row", "feeder_runs_under_half_a_day_apart", "feeder_runs_about_a_day_apart",
             "feeder_runs_further_apart")
    grouped = {name: [] for name in names}
    for pair in pairs:
        grouped[horizon(snapshot, pair, bounds)].append(pair)
    by_horizon = {}
    for name in names:
        gaps = sorted({round(gap_days(snapshot, p["earlier_run"], p["later_run"]), DECIMALS["day"]) for p in grouped[name]})
        by_horizon[name] = {"run_gaps": len({p["later_run"] for p in grouped[name]}),
                            "shortest_gap_days": gaps[0] if gaps else None,
                            "longest_gap_days": gaps[-1] if gaps else None} | persistence(grouped[name])
    between = persistence([pair for name in names[1:] for pair in grouped[name]])
    check("horizon groups sum to the totals",
          (sum(g["pairs"] for g in by_horizon.values()), sum(g["changed"] for g in by_horizon.values())) == (n, changes))
    check("pairs from a seed row + pairs between feeder runs = usable pairs",
          by_horizon["from_a_seed_row"]["pairs"] + between["pairs"] == n)

    targets = {label: sum(pair["later_label"] == label for pair in pairs) for label in snapshot["encoding"]["labels"]}
    check("target-label shares sum to 1", sum(Fraction(count, n) for count in targets.values()) == 1)
    constant = {label: {"correct": count, "errors": n - count, "accuracy": ratio(count, n),
                        "skill_vs_persistence": skill(n - count, changes)} for label, count in targets.items()}
    best_constant = max(targets, key=lambda label: (targets[label], label))

    models = scenarios["synthetic_candidates"]["models"]
    for name, model in models.items():
        check(f"synthetic candidate {name} accounts for every observed change",
              model["changes_called"] + model["changes_missed"] == changes)
    candidates = {name: {"description": model["description"]} | score_model(n, changes, model["changes_called"], model["false_alarms"])
                  for name, model in models.items()}
    check("a candidate with persistence's errors has skill 0", candidates["echo"]["skill_vs_persistence"]["value"] == 0)
    weighted = {}
    for cost in scenarios["miss_to_false_alarm_cost_ratios"]:
        weighted[f"miss_costs_{cost}_false_alarms"] = {"persistence": cost * changes} | {
            name: cost * model["changes_missed"] + model["false_alarms"] for name, model in candidates.items()}
    alarm = candidates["cautious_alarm"]
    break_even = Fraction(alarm["false_alarms"], changes - alarm["changes_missed"])

    cells = scenarios["cited_example"]["table"]
    hits, false_alarms = cells["forecast_tornado_observed_tornado"], cells["forecast_tornado_observed_none"]
    missed, quiet = cells["forecast_none_observed_tornado"], cells["forecast_none_observed_none"]
    total = hits + false_alarms + missed + quiet
    finley = {"source": scenarios["cited_example"]["source"], "url": scenarios["cited_example"]["url"],
              "forecasts": total, "tornadoes": hits + missed,
              "accuracy": ratio(hits + quiet, total), "accuracy_of_never_forecasting_a_tornado": ratio(false_alarms + quiet, total),
              "skill_vs_never_forecasting_a_tornado": skill(false_alarms + missed, hits + missed),
              "share_of_tornadoes_called": ratio(hits, hits + missed),
              "share_of_alarms_that_were_false": ratio(false_alarms, hits + false_alarms)}

    latest = snapshot["runs"][-1]["rows"]
    extrapolation = {"assumption": scenarios["extrapolation"]["assumption"], "pairs_per_observed_change": ratio(n, changes)["exact"],
                     "artifacts_in_the_latest_run": latest, "targets": []}
    for target in scenarios["extrapolation"]["target_changes"]:
        needed = Fraction(target * n, changes)
        extrapolation["targets"].append({"expected_changes": target, "pairs_needed": math.ceil(needed),
                                         "runs_needed_before_rounding_up": round(float(needed / latest), DECIMALS["ratio"]),
                                         "runs_needed": math.ceil(needed / latest)})

    controls = negative_controls(snapshot, bounds, {"pairs": n, "changed": changes, "mismatches": mismatches,
                                                    "between_feeder_runs_changed": between["changed"]})
    transfer = transfer_task(scenarios["transfer_task"])
    seed_runs = sum(any(row[3] for rows in table.values() for row in rows if row[0] == index)
                    for index in range(len(snapshot["runs"])))
    return {
        "module_id": snapshot["module_id"],
        "rounding": "ratios to 6 decimals, percentages to 2 decimals, days to 3 decimals; 'exact' is the unrounded fraction",
        "source": {"repository": snapshot["source"]["repository"], "commit": snapshot["source"]["commit"],
                   "files": [entry["path"] for entry in snapshot["source"]["files"] + snapshot["source"]["evolution_records"]]},
        "observed": {
            "kind": "observed: counted from observed-input.json",
            "rows": rows, "runs": len(snapshot["runs"]), "seed_runs": seed_runs, "feeder_runs": len(snapshot["runs"]) - seed_runs,
            "run_dates_utc": counts["run_dates_utc"], "first_run": snapshot["runs"][0]["timestamp"],
            "last_run": snapshot["runs"][-1]["timestamp"], "artifacts": len(table),
            "rows_per_run": {str(size): sum(run["rows"] == size for run in snapshot["runs"])
                             for size in sorted({run["rows"] for run in snapshot["runs"]})},
            "rows_flagged_baseline": counts["rows_flagged_baseline"],
            "rows_by_label_presence": classes,
            "rows_with_a_missing_label": snapshot["rows_with_a_missing_label"],
            "label_changes": snapshot["label_changes"],
        },
        "forecast_unit": {
            "kind": "computed",
            "definition": "One forecast = one artifact at two consecutive rows of its history, both with an "
                          "effectiveness_to label: the earlier label is the forecast, the later label is the outcome.",
            "row_pairs": row_pairs, "pairs_without_a_label": row_pairs - n, "usable_pairs": n,
            "cross_check_in_row": {
                "definition": "effectiveness_from against effectiveness_to inside one row, both present",
                "pairs": len(inside), "changed": tally(inside)["changed"],
                "seed_rows_with_no_earlier_row": sum(pair["seed_row"] for pair in inside),
                "pairs_outside_seed_rows": len(not_seed),
                "rows_whose_from_differs_from_the_previous_to": mismatches,
                "persistence_accuracy": ratio(tally(inside)["unchanged"], len(inside)),
            },
        },
        "persistence": {"kind": "computed", "all_usable_pairs": all_pairs, "between_feeder_runs": between,
                        "by_horizon": by_horizon,
                        "run_level": {"definition": "one forecast per target run: 'no label changes in this run'",
                                      "target_runs": len(per_run), "runs_without_a_change": quiet_runs,
                                      "runs_with_a_change": len(per_run) - quiet_runs,
                                      "accuracy": ratio(quiet_runs, len(per_run))}},
        "constant_label_forecasts": {"kind": "computed; the best constant label is chosen with hindsight",
                                     "target_labels": targets, "best_constant_label": best_constant, "forecasts": constant},
        "skill": {
            "kind": "synthetic candidates scored on the observed pairs",
            "formula": "skill = (A - A_ref) / (1 - A_ref) = 1 - E / E_ref, with A accuracy and E errors on the same pairs",
            "reference": "persistence", "reference_errors": changes,
            "skill_by_error_count": {str(errors): skill(errors, changes)["value"] for errors in range(5)},
            "skill_between_feeder_runs": skill(0, between["changed"]),
            "candidates": candidates,
            "weighted_cost": weighted,
            "cautious_alarm_break_even_cost_ratio": {"exact": str(break_even), "value": round(float(break_even), DECIMALS["ratio"])},
        },
        "cited_example_finley_1884": {"kind": "cited historical data, used as an analogy"} | finley,
        "extrapolation": {"kind": "computed under a stated assumption, not a forecast"} | extrapolation,
        "per_artifact": per_artifact,
        "per_run": per_run,
        "negative_controls": controls,
        "transfer_task": transfer,
        "checks": [{"check": name, "times_evaluated": times, "passed": True} for name, times in CHECKS.items()],
    }


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
    args.output.write_bytes(text.encode("utf-8"))
    print(f"analyze.py: {len(CHECKS)} self-checks passed -> {args.output.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
