#!/usr/bin/env python3
"""PSY-018 analysis: a rolling-origin backtest of citation counts, and three leaks.

Reads observed-input.json (written by extract.py) and scenarios.json, never
the repository, and writes results.json. Every result is an exact count or an
exact fraction, rounded only when it is stored. The one random draw is a
seeded cross-check of an exact average and uses random.Random(seed).random().

Run from the repository root:
    python -I scripts/streeling_fixtures/psychohistory/psy-018/analyze.py
    python -I scripts/streeling_fixtures/psychohistory/psy-018/analyze.py --check
"""

from __future__ import annotations

import argparse
import copy
import json
import math
import random
import sys
from datetime import datetime, timezone
from fractions import Fraction
from itertools import combinations
from pathlib import Path

# This program lives under scripts/ (CONTRIBUTING.md: no executable code outside scripts/); its data stays
# under state/streeling/fixtures/. FIXTURE_FILE is the path the program would have next to that data.
FIXTURE_FILE = (Path(__file__).resolve().parents[4]
                / "state/streeling/fixtures/psychohistory/psy-018" / Path(__file__).name)

HERE = FIXTURE_FILE.parent
NO_ROW, ABSENT = ".", "-"
METHODS = ("persistence", "mean", "drift")
KINDS = ("before_its_rebaseline_row", "from_its_rebaseline_row", "never_rebaselined")
DECIMALS = {"ratio": 6, "percent": 2, "day": 3}
CHECKS: dict[str, int] = {}  # self-check -> times evaluated


def check(name: str, condition: bool, detail: str = "") -> None:
    """A self-check that can fail: abort instead of writing a wrong result."""
    if not condition:
        raise AssertionError(f"self-check failed: {name}" + (f" ({detail})" if detail else ""))
    CHECKS[name] = CHECKS.get(name, 0) + 1


def num(value) -> dict:
    """An exact fraction and its rounded decimal value."""
    value = Fraction(value)
    exact = str(value) if value.denominator < 10 ** 12 else "not shown: the denominator has more than 12 digits"
    return {"exact": exact, "value": round(float(value), DECIMALS["ratio"])}


def div(numerator, denominator) -> dict:
    if denominator == 0:
        return {"exact": f"undefined: {Fraction(numerator)}/0", "value": None}
    return num(Fraction(numerator) / denominator)


def change(reported, honest) -> dict:
    """How far a reported error lies from the honest one, as a share of the honest one."""
    if honest == 0:
        return {"exact": f"undefined: ({Fraction(reported)} - 0)/0", "percent": None}
    value = Fraction(reported) / honest - 1
    return {"exact": str(value), "percent": round(float(100 * value), DECIMALS["percent"])}


def levels(values: list[int]) -> list[list[int]]:
    """Run-length form of a series: [[value, consecutive rows], ...]."""
    out: list[list[int]] = []
    for value in values:
        if out and out[-1][0] == value:
            out[-1][1] += 1
        else:
            out.append([value, 1])
    return out


def levels_text(values: list[int]) -> str:
    """The run-length form as one readable string: '42 for 21 rows, then 44 for 11 rows'."""
    return ", then ".join(f"{value} for {rows} row{'s' if rows != 1 else ''}" for value, rows in levels(values))


def gap_days(snapshot: dict, earlier: int, later: int) -> float:
    stamps = [datetime.strptime(snapshot["runs"][index]["timestamp"], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
              for index in (earlier, later)]
    return (stamps[1] - stamps[0]).total_seconds() / 86400


# ---------------------------------------------------------------- reading the snapshot

def load_rows(snapshot: dict) -> dict[str, list[dict]]:
    """Per artifact, its rows in run order, decoded from the run-aligned strings."""
    runs = len(snapshot["runs"])
    table = {}
    for artifact in snapshot["artifacts"]:
        columns = [artifact["citation_count"].split(" "), artifact["delta_citations"].split(" "),
                   artifact["baseline_flag"], artifact["rebaseline_flag"], artifact["citation_source"]]
        if any(len(column) != runs for column in columns):
            raise ValueError(f"{artifact['name']}: a column is not aligned with the {runs} runs")
        rows = []
        for index, (count, delta, seed, rebaseline, source) in enumerate(zip(*columns)):
            if len({cell == NO_ROW for cell in (count, delta, seed, rebaseline, source)}) != 1:
                raise ValueError(f"{artifact['name']}: run {index} is a row in one column and not in another")
            if count != NO_ROW:
                rows.append({"run": index, "count": None if count == ABSENT else int(count), "delta": int(delta),
                             "seed": seed == "s", "rebaseline": rebaseline == "r", "source": source})
        table[artifact["name"]] = rows
    return table


def split_series(table: dict) -> list[dict]:
    """A series is one artifact under one instrument: it restarts at each row flagged rebaseline."""
    series = []
    for name, rows in table.items():
        counted = [row for row in rows if row["count"] is not None]
        starts = [index for index, row in enumerate(counted) if row["rebaseline"]]
        bounds = sorted({0, len(counted), *starts})
        for first, end in zip(bounds, bounds[1:]):
            part = counted[first:end]
            kind = KINDS[1] if part[0]["rebaseline"] else KINDS[0] if starts else KINDS[2]
            series.append({"artifact": name, "kind": kind, "runs": [row["run"] for row in part],
                           "values": [row["count"] for row in part], "deltas": [row["delta"] for row in part],
                           "sources": sorted({row["source"] for row in part})})
    return series


def consecutive_pairs(table: dict) -> list[tuple]:
    """Pairs of consecutive rows of one artifact that both carry a count."""
    return [(name, earlier, later) for name, rows in table.items() for earlier, later in zip(rows, rows[1:])
            if earlier["count"] is not None and later["count"] is not None]


def delta_rule_mismatches(table: dict) -> tuple[int, int]:
    """Rows whose delta_citations differs from the feeder's rule: 0 on a rebaseline, else count - previous count."""
    checked = mismatches = 0
    for rows in table.values():
        previous = None
        for row in rows:
            if row["count"] is not None:
                checked += 1
                mismatches += row["delta"] != (0 if row["rebaseline"] else row["count"] - (previous or 0))
            previous = row["count"]
    return checked, mismatches


# ---------------------------------------------------------------- forecasts and scores

def forecast(values: list[int], origin: int) -> dict[str, Fraction]:
    """Forecasts of row origin + 1 from rows 1 to origin only (rows are numbered from 1)."""
    last = values[origin - 1]
    return {"persistence": Fraction(last),
            "mean": Fraction(sum(values[:origin]), origin),
            "drift": last + Fraction(last - values[0], origin - 1)}


def naive_scale(values: list[int], origin: int) -> Fraction:
    """In-sample MAE of the one-step naive forecast over rows 1 to origin (Hyndman and Koehler 2006)."""
    return Fraction(sum(abs(b - a) for a, b in zip(values[:origin], values[1:origin])), origin - 1)


def rolling_origin(values: list[int], min_train: int) -> list[dict]:
    """One forecast per row that has at least min_train rows before it."""
    out = []
    for origin in range(min_train, len(values)):
        made = forecast(values, origin)
        out.append({"target_row": origin + 1, "actual": values[origin], "forecasts": made,
                    "errors": {method: values[origin] - made[method] for method in METHODS},
                    "scale": naive_scale(values, origin)})
    return out


def absolute_errors(group: list[dict], min_train: int) -> tuple[int, dict, dict]:
    """Forecasts, sum of absolute errors per method and forecasts with an error per method, pooled over series."""
    forecasts, sums, nonzero = 0, {m: Fraction(0) for m in METHODS}, {m: 0 for m in METHODS}
    for series in group:
        for row in rolling_origin(series["values"], min_train):
            forecasts += 1
            for method in METHODS:
                sums[method] += abs(row["errors"][method])
                nonzero[method] += row["errors"][method] != 0
    return forecasts, sums, nonzero


def score(group: list[dict], min_train: int) -> dict:
    """Pooled rolling-origin errors of several series, as stored in results.json."""
    forecasts, sums, nonzero = absolute_errors(group, min_train)
    return {"forecasts": forecasts,
            "methods": {method: {"forecasts_with_an_error": nonzero[method],
                                 "sum_of_absolute_errors": num(sums[method]),
                                 "mae": div(sums[method], forecasts),
                                 "relative_mae_against_persistence": div(sums[method], sums["persistence"])}
                        for method in METHODS}}


def mae_of_level(rows: list[int], level: Fraction) -> Fraction:
    """Mean absolute error of one constant forecast over some rows."""
    return sum((abs(value - level) for value in rows), Fraction(0)) / len(rows)


def time_split(values: list[int], test_rows: int) -> tuple[Fraction, Fraction]:
    """Test MAE of a fitted level on the last rows: fitted on the rows before them, then on every row."""
    train, test = values[:-test_rows], values[-test_rows:]
    return (mae_of_level(test, Fraction(sum(train), len(train))),
            mae_of_level(test, Fraction(sum(values), len(values))))


def random_split(values: list[int], test_rows: int) -> dict:
    """Exact test MAE of a level fitted on the other rows, over every choice of test rows.

    Works for a series with at most two distinct values: k counts the test rows at the higher one.
    """
    low, high = min(values), max(values)
    if set(values) - {low, high}:
        raise ValueError("random_split handles a series with at most two distinct values")
    lows, n = values.count(low), len(values)
    highs = n - lows
    cases, splits = [], 0
    for k in range(max(0, test_rows - lows), min(test_rows, highs) + 1):
        ways = math.comb(highs, k) * math.comb(lows, test_rows - k)
        level = Fraction(low * (lows - test_rows + k) + high * (highs - k), n - test_rows)
        cases.append({"k": k, "ways": ways,
                      "mae": (abs(low - level) * (test_rows - k) + abs(high - level) * k) / test_rows})
        splits += ways
    check("random split: the cases cover every choice of test rows", splits == math.comb(n, test_rows))
    return {"splits": splits, "cases": cases,
            "expected": sum((case["ways"] * case["mae"] for case in cases), Fraction(0)) / splits}


def random_split_enumerated(values: list[int], test_rows: int) -> Fraction:
    """The same average by listing every split (small series only)."""
    total, splits = Fraction(0), 0
    for test in combinations(range(len(values)), test_rows):
        train = [value for index, value in enumerate(values) if index not in test]
        total += mae_of_level([values[index] for index in test], Fraction(sum(train), len(train)))
        splits += 1
    return total / splits


def random_split_simulated(values: list[int], test_rows: int, seed: int, draws: int) -> Fraction:
    """The same average over seeded random splits: the test rows are those with the smallest keys."""
    rng = random.Random(seed)
    train_rows, total = len(values) - test_rows, 0
    for _ in range(draws):
        keys = [rng.random() for _ in values]
        test = sorted(range(len(values)), key=keys.__getitem__)[:test_rows]
        train_sum = sum(values) - sum(values[index] for index in test)
        total += sum(abs(values[index] * train_rows - train_sum) for index in test)
    return Fraction(total, train_rows * test_rows * draws)


def single_step(values: list[int]) -> tuple[int, int, int]:
    """(rows at the first level, rows at the second, step) of a series with exactly one step."""
    shape = levels(values)
    if len(shape) != 2:
        raise ValueError("expected a series with exactly one step")
    return shape[0][1], shape[1][1], shape[1][0] - shape[0][0]


# ---------------------------------------------------------------- self-checks with known answers

def hand_computed_case() -> None:
    """The series 5 5 5 7 7 7, worked by hand in the README."""
    values = [5, 5, 5, 7, 7, 7]
    rows = rolling_origin(values, 2)
    sums = [sum(abs(row["errors"][method]) for row in rows) for method in METHODS]
    check("hand-computed case 5 5 5 7 7 7: 4 forecasts, absolute errors 2 (persistence), 47/10 (mean), 19/6 (drift)",
          (len(rows), sums) == (4, [2, Fraction(47, 10), Fraction(19, 6)]))
    check("hand-computed case: in-sample scale 0, 0, 2/3, 1/2 at the four origins",
          [row["scale"] for row in rows] == [0, 0, Fraction(2, 3), Fraction(1, 2)])
    check("hand-computed case: last two rows as test, level 11/2 from the first four (MAE 3/2), 6 from all six (MAE 1)",
          time_split(values, 2) == (Fraction(3, 2), 1))
    check("hand-computed case: the random-split formula equals a listing of the 15 splits",
          random_split(values, 2)["expected"] == random_split_enumerated(values, 2)
          and random_split(values, 2)["splits"] == 15)


def closed_forms(varying: list[dict], min_train: int) -> None:
    """One step in a flat series: the three sums of absolute errors have a closed form."""
    for series in varying:
        first, second, step = single_step(series["values"])
        rows = rolling_origin(series["values"], min_train)
        sums = {method: sum(abs(row["errors"][method]) for row in rows) for method in METHODS}
        n = first + second
        harmonic = lambda a, b: sum((Fraction(1, k) for k in range(a, b + 1)), Fraction(0))  # noqa: E731
        check("closed form: persistence errs once, by the step", sums["persistence"] == abs(step))
        check("closed form: mean so far errs by step * c * (1/c + ... + 1/(n-1))",
              sums["mean"] == abs(step) * first * harmonic(first, n - 1))
        check("closed form: drift errs by step * (1 + 1/c + ... + 1/(n-2))",
              sums["drift"] == abs(step) * (1 + harmonic(first, n - 2)))


# ---------------------------------------------------------------- sections of results.json

def observed_section(snapshot: dict, table: dict) -> dict:
    counts = snapshot["counts"]
    rows = [row for series in table.values() for row in series]
    seed_runs = {row["run"] for row in rows if row["seed"]}
    feeder = [index for index in range(len(snapshot["runs"])) if index not in seed_runs]
    gaps = [gap_days(snapshot, a, b) for a, b in zip(feeder, feeder[1:])]
    recount = {
        "rows": len(rows), "runs": len(snapshot["runs"]),
        "run_dates_utc": len({run["timestamp"][:10] for run in snapshot["runs"]}), "artifacts": len(table),
        "rows_flagged_baseline": sum(row["seed"] for row in rows),
        "rows_with_a_citation_count": sum(row["count"] is not None for row in rows),
        "rows_flagged_rebaseline": sum(row["rebaseline"] for row in rows),
        "rows_by_citation_source": {"key_absent": sum(row["source"] == ABSENT for row in rows),
                                    "null": sum(row["source"] == "n" for row in rows),
                                    "git-grep-v1": sum(row["source"] == "g" for row in rows)},
        "rows_with_a_nonzero_delta_citations": sum(row["delta"] != 0 for row in rows),
    }
    check("recount of rows, runs, dates, artifacts, flags and non-zero deltas equals extract.py's counts",
          recount == {key: counts[key] for key in recount})
    check("rows with a count = rows - seed rows",
          recount["rows_with_a_citation_count"] == recount["rows"] - recount["rows_flagged_baseline"])
    check("rows by citation_source sum to the rows", sum(recount["rows_by_citation_source"].values()) == len(rows))
    return {
        "kind": "observed: counted from observed-input.json",
        **recount,
        "seed_runs": len(seed_runs), "feeder_runs": len(feeder),
        "first_feeder_run": snapshot["runs"][feeder[0]]["timestamp"],
        "last_feeder_run": snapshot["runs"][feeder[-1]]["timestamp"],
        "gaps_between_consecutive_feeder_runs": {
            "gaps": len(gaps), "shortest_days": round(min(gaps), DECIMALS["day"]),
            "longest_days": round(max(gaps), DECIMALS["day"])},
        "feeder_rule_for_delta_citations": snapshot["feeder_rule"],
    }


def step_rows(snapshot: dict, changed: list[tuple]) -> list[dict]:
    return [{"artifact": name, "run": snapshot["runs"][later["run"]]["timestamp"], "from": earlier["count"],
             "to": later["count"], "step": later["count"] - earlier["count"], "rebaseline_row": later["rebaseline"],
             "delta_citations": later["delta"],
             "days_since_previous_run": round(gap_days(snapshot, earlier["run"], later["run"]), DECIMALS["day"])}
            for name, earlier, later in changed]


def variation_section(snapshot: dict, table: dict) -> dict:
    """How much the counts vary, and the two different sets of 'rows where something changed'."""
    pairs = consecutive_pairs(table)
    changed = [pair for pair in pairs if pair[1]["count"] != pair[2]["count"]]
    by_date: dict[str, int] = {}
    for _, _, later in changed:
        date = snapshot["runs"][later["run"]]["timestamp"][:10]
        by_date[date] = by_date.get(date, 0) + 1
    recount = {"pairs_of_consecutive_rows_with_a_count": len(pairs), "count_changed": len(changed),
               "count_unchanged": len(pairs) - len(changed), "count_changed_by_utc_date": by_date,
               "pairs_ending_at_a_rebaseline_row": sum(later["rebaseline"] for _, _, later in pairs)}
    check("recount of the pairs of consecutive rows equals extract.py's counts",
          recount == snapshot["counts"]["consecutive_rows"])
    check("pairs of consecutive rows with a count = rows with a count - artifacts",
          len(pairs) == snapshot["counts"]["rows_with_a_citation_count"] - len(table))
    value_rows = {(name, later["run"]) for name, _, later in changed}
    delta_rows = {(name, row["run"]) for name, rows in table.items() for row in rows if row["delta"] != 0}
    first_counted = {(name, next(row["run"] for row in rows if row["count"] is not None)) for name, rows in table.items()}
    rebaseline_rows = {(name, row["run"]) for name, rows in table.items() for row in rows if row["rebaseline"]}
    check("every row with a non-zero delta and an unchanged count is the artifact's first row with a count",
          delta_rows - value_rows <= first_counted)
    check("every row with a changed count and a zero delta is a rebaseline row", value_rows - delta_rows <= rebaseline_rows)
    checked, mismatches = delta_rule_mismatches(table)
    at_rebaseline = [pair for pair in changed if pair[2]["rebaseline"]]
    elsewhere = [pair for pair in changed if not pair[2]["rebaseline"]]
    per_artifact = [{"artifact": name, "rows_with_a_count": sum(row["count"] is not None for row in rows),
                     "levels": levels_text([row["count"] for row in rows if row["count"] is not None]),
                     "count_changes": sum(pair[0] == name for pair in changed),
                     "count_changes_outside_a_rebaseline_row": sum(pair[0] == name for pair in elsewhere)}
                    for name, rows in table.items()]
    return {
        "kind": "computed from the observed counts",
        **recount,
        "count_changes_at_a_rebaseline_row": len(at_rebaseline), "count_changes_elsewhere": len(elsewhere),
        "sum_of_absolute_steps_at_a_rebaseline_row": sum(abs(l["count"] - e["count"]) for _, e, l in at_rebaseline),
        "sum_of_absolute_steps_elsewhere": sum(abs(l["count"] - e["count"]) for _, e, l in elsewhere),
        "artifacts_whose_count_changes": sum(a["count_changes"] > 0 for a in per_artifact),
        "artifacts_whose_count_changes_outside_a_rebaseline_row":
            sum(a["count_changes_outside_a_rebaseline_row"] > 0 for a in per_artifact),
        "artifacts_whose_count_never_changes": sum(a["count_changes"] == 0 for a in per_artifact),
        "two_sets_of_twenty": {
            "rows_with_a_nonzero_delta_citations": len(delta_rows),
            "rows_whose_count_differs_from_the_previous_row": len(value_rows),
            "rows_in_both_sets": len(delta_rows & value_rows),
            "nonzero_delta_but_count_unchanged": len(delta_rows - value_rows),
            "nonzero_delta_but_count_unchanged_reason": "first row with a count: the feeder subtracts 0",
            "count_changed_but_delta_zero": len(value_rows - delta_rows),
            "count_changed_but_delta_zero_reason": "rebaseline row: the feeder writes 0",
            "set_used_by_this_module": "rows whose count differs from the previous row",
        },
        "delta_rule_check": {"rows_checked": checked, "rows_that_break_the_rule": mismatches},
        "count_changes": step_rows(snapshot, changed),
        "per_artifact": per_artifact,
    }


def series_section(snapshot: dict, series: list[dict], min_train: int, pairs_total: int, rebaseline_pairs: int) -> dict:
    by_kind = {}
    for kind in KINDS:
        group = [s for s in series if s["kind"] == kind]
        by_kind[kind] = {"series": len(group), "rows": sum(len(s["values"]) for s in group),
                         "pairs_of_consecutive_rows": sum(len(s["values"]) - 1 for s in group),
                         "forecasts": sum(max(0, len(s["values"]) - min_train) for s in group),
                         "series_that_vary": sum(len(set(s["values"])) > 1 for s in group),
                         "citation_source_codes_seen": sorted({code for s in group for code in s["sources"]})}
    totals = {key: sum(group[key] for group in by_kind.values())
              for key in ("series", "rows", "pairs_of_consecutive_rows", "forecasts", "series_that_vary")}
    check("series rows sum to the rows with a count", totals["rows"] == snapshot["counts"]["rows_with_a_citation_count"])
    check("pairs inside a series = pairs of consecutive rows - pairs ending at a rebaseline row",
          totals["pairs_of_consecutive_rows"] == pairs_total - rebaseline_pairs)
    check("forecasts = pairs inside a series - one pair per series (two training rows)",
          min_train != 2 or totals["forecasts"] == totals["pairs_of_consecutive_rows"] - totals["series"])
    check("a series that starts at a rebaseline row is counted by git grep throughout",
          by_kind[KINDS[1]]["citation_source_codes_seen"] == ["g"] and "g" not in
          by_kind[KINDS[0]]["citation_source_codes_seen"] + by_kind[KINDS[2]]["citation_source_codes_seen"])
    second_rows = sum(s["values"][index] != s["values"][index - 1] for s in series for index in range(1, min_train))
    return {
        "kind": "computed",
        "definition": "A series is one artifact under one instrument: its rows that carry a count, restarted at "
                      "each row flagged rebaseline: true.",
        **totals, "by_kind": by_kind,
        "count_changes_in_pairs_too_early_to_be_a_target": second_rows,
        "list": [{"artifact": s["artifact"], "kind": s["kind"], "first_run": snapshot["runs"][s["runs"][0]]["timestamp"],
                  "last_run": snapshot["runs"][s["runs"][-1]]["timestamp"], "rows": len(s["values"]),
                  "levels": levels_text(s["values"])} for s in series],
    }


def worked_rows(snapshot: dict, series: dict, min_train: int) -> list[dict]:
    """The forecasts around the step of one series, with their in-sample scale, for the worked answers."""
    first, _, _ = single_step(series["values"])
    wanted = {first + 1, first + 2, len(series["values"])}
    out = []
    for row in rolling_origin(series["values"], min_train):
        if row["target_row"] in wanted:
            out.append({
                "target_row": row["target_row"], "origin_row": row["target_row"] - 1,
                "target_run": snapshot["runs"][series["runs"][row["target_row"] - 1]]["timestamp"],
                "actual": row["actual"],
                "forecasts": {method: num(row["forecasts"][method]) for method in METHODS},
                "errors": {method: num(row["errors"][method]) for method in METHODS},
                "in_sample_scale_at_the_origin": num(row["scale"]),
                "scaled_errors": {method: div(abs(row["errors"][method]), row["scale"]) for method in METHODS}})
    return out


def forecast_gaps(snapshot: dict, series: list[dict], min_train: int, bounds: dict) -> dict:
    """One run ahead is not one day ahead: the time from each origin to its target."""
    gaps = [gap_days(snapshot, s["runs"][origin - 1], s["runs"][origin])
            for s in series for origin in range(min_train, len(s["values"]))]
    short = sum(gap < bounds["about_a_day_from"] for gap in gaps)
    long = sum(gap > bounds["about_a_day_to"] for gap in gaps)
    return {"forecasts": len(gaps), "shortest_days": round(min(gaps), DECIMALS["day"]),
            "longest_days": round(max(gaps), DECIMALS["day"]), "under_half_a_day": short,
            "about_a_day": len(gaps) - short - long, "over_a_day_and_a_half": long}


def rolling_section(snapshot: dict, series: list[dict], min_train: int, bounds: dict) -> dict:
    varying = [s for s in series if len(set(s["values"])) > 1]
    flat = [s for s in series if len(set(s["values"])) == 1]
    pooled = score(series, min_train)
    by_kind = {kind: {"series": sum(s["kind"] == kind for s in series)}
               | score([s for s in series if s["kind"] == kind], min_train) for kind in KINDS}
    never = score(flat, min_train)
    check("no method errs on a series that never varies",
          all(method["forecasts_with_an_error"] == 0 for method in never["methods"].values()))
    check("pooled persistence error = sum of the absolute steps at target rows",
          absolute_errors(series, min_train)[1]["persistence"]
          == sum(abs(s["values"][i] - s["values"][i - 1]) for s in series for i in range(min_train, len(s["values"]))))
    check("by-kind forecasts sum to the pooled forecasts",
          sum(group["forecasts"] for group in by_kind.values()) == pooled["forecasts"])
    closed_forms(varying, min_train)
    per_series = []
    for s in varying:
        first, second, step = single_step(s["values"])
        per_series.append({"artifact": s["artifact"], "kind": s["kind"], "rows": len(s["values"]),
                           "rows_before_the_step": first, "rows_from_the_step": second, "step": step,
                           "levels": levels_text(s["values"]),
                           "step_run": snapshot["runs"][s["runs"][first]]["timestamp"]}
                          | score([s], min_train) | {"worked_rows": worked_rows(snapshot, s, min_train)})
    return {
        "kind": "computed",
        "definition": "For every row of a series with at least min_training_rows rows before it: forecast it from "
                      "the rows before it only, one run ahead; error = actual - forecast.",
        "min_training_rows": min_train,
        "methods": {"persistence": "the last value", "mean": "the mean of every value so far",
                    "drift": "the last value plus the average change per run so far: (last - first) / (rows - 1)"},
        "pooled": pooled,
        "by_kind": by_kind,
        "series_that_never_vary": {"series": len(flat)} | never,
        "series_that_vary": per_series,
        "time_from_origin_to_target": forecast_gaps(snapshot, series, min_train, bounds),
    }


def scaled_error_section(series: list[dict], min_train: int) -> dict:
    """The scaled error of Hyndman and Koehler: error / in-sample MAE of the naive forecast."""
    forecasts = positive = 0
    unscalable = {method: 0 for method in METHODS}
    sums = {method: Fraction(0) for method in METHODS}
    never_defined = 0
    for s in series:
        rows = rolling_origin(s["values"], min_train)
        never_defined += all(row["scale"] == 0 for row in rows)
        for row in rows:
            forecasts += 1
            positive += row["scale"] > 0
            for method in METHODS:
                if row["scale"] > 0:
                    sums[method] += abs(row["errors"][method]) / row["scale"]
                else:
                    unscalable[method] += row["errors"][method] != 0
    whole = {}
    for s in series:
        if len(set(s["values"])) > 1:
            scale = naive_scale(s["values"], len(s["values"]))
            rows = rolling_origin(s["values"], min_train)
            whole[s["artifact"]] = {"scale": num(scale)} | {
                method: div(sum(abs(row["errors"][method]) for row in rows), scale * len(rows)) for method in METHODS}
    check("the whole-series scale gives the same scaled errors on every series that varies",
          len({json.dumps(value, sort_keys=True) for value in whole.values()}) == 1)
    return {
        "kind": "computed",
        "definition": "scaled error = |error| / scale, where scale is the mean absolute change between consecutive "
                      "rows of the training rows (rows 1 to the origin)",
        "forecasts": forecasts, "forecasts_with_a_positive_scale": positive,
        "forecasts_with_a_zero_scale": forecasts - positive,
        "series_with_no_scaled_error_at_all": never_defined,
        "errors_that_cannot_be_scaled": unscalable,
        "mean_scaled_error_over_the_forecasts_with_a_positive_scale": {
            method: div(sums[method], positive) for method in METHODS},
        "leak_scale_computed_on_the_whole_series": {
            "note": "Leaky variant: the scale is computed once on every row of the series, target rows included; "
                    "the scaled error is then defined for every forecast of a series that varies.",
            "artifacts": sorted(whole), **next(iter(whole.values()))},
    }


def leak_frame(values: list[int], test_rows: int) -> dict:
    """One fitted level, three ways to test it on test_rows rows of one series."""
    honest, whole = time_split(values, test_rows)
    shuffled = random_split(values, test_rows)
    return {"training_rows": len(values) - test_rows, "test_rows": test_rows,
            "split_in_time_mae": num(honest),
            "leak_1_level_fitted_on_every_row_mae": num(whole),
            "leak_1_change": change(whole, honest),
            "leak_3_random_split_expected_mae": num(shuffled["expected"]),
            "leak_3_change": change(shuffled["expected"], honest)}


def cut_sweep(values: list[int], min_train: int) -> dict:
    """The same comparison for every cut that leaves min_train training rows and at least one test row."""
    cuts = list(range(min_train, len(values)))
    raw = []
    for train in cuts:
        honest, whole = time_split(values, len(values) - train)
        raw.append((honest, whole, random_split(values, len(values) - train)["expected"]))
    out = {"cuts": len(cuts), "note": "MAE of the fitted level on the test rows, rounded to 6 decimals; changes in percent"}
    for leak, position in (("leak_1", 1), ("leak_3", 2)):
        changes = [row[position] / row[0] - 1 for row in raw]
        out[leak] = {"cuts_where_the_leak_lowers_the_error": sum(c < 0 for c in changes),
                     "cuts_where_it_makes_no_difference": sum(c == 0 for c in changes),
                     "cuts_where_the_leak_raises_the_error": sum(c > 0 for c in changes),
                     "largest_fall_percent": round(float(100 * min(changes)), DECIMALS["percent"]),
                     "largest_fall_at_training_rows": cuts[changes.index(min(changes))],
                     "largest_rise_percent": round(float(100 * max(changes)), DECIMALS["percent"]),
                     "largest_rise_at_training_rows": cuts[changes.index(max(changes))]}
    check("cut sweep: lowered + unchanged + raised = cuts, for both leaks",
          all(sum(list(out[leak].values())[:3]) == len(cuts) for leak in ("leak_1", "leak_3")))
    return out | {"rows": [
        {"training_rows": train, "test_rows": len(values) - train,
         "split_in_time_mae": round(float(honest), DECIMALS["ratio"]),
         "leak_1_mae": round(float(whole), DECIMALS["ratio"]),
         "leak_1_change_percent": change(whole, honest)["percent"],
         "leak_3_mae": round(float(shuffled), DECIMALS["ratio"]),
         "leak_3_change_percent": change(shuffled, honest)["percent"]}
        for train, (honest, whole, shuffled) in zip(cuts, raw)]}


def target_feature_leak(table: dict, series: list[dict], min_train: int) -> dict:
    """Leak 2: persistence plus the target row's own delta_citations."""
    forecasts = honest_errors = leaky_errors = 0
    honest_sum = leaky_sum = 0
    for s in series:
        for index in range(min_train, len(s["values"])):
            forecasts += 1
            honest = abs(s["values"][index] - s["values"][index - 1])
            leaky = abs(s["values"][index] - (s["values"][index - 1] + s["deltas"][index]))
            honest_errors, leaky_errors = honest_errors + (honest != 0), leaky_errors + (leaky != 0)
            honest_sum, leaky_sum = honest_sum + honest, leaky_sum + leaky
    pairs = consecutive_pairs(table)
    misses = [(earlier, later) for _, earlier, later in pairs if earlier["count"] + later["delta"] != later["count"]]
    check("on every pair of consecutive rows, previous count + delta_citations misses only at rebaseline rows",
          all(later["rebaseline"] for _, later in misses))
    return {
        "forecast": "previous count + delta_citations of the target row",
        "forecasts": forecasts,
        "persistence": {"forecasts_with_an_error": honest_errors, "sum_of_absolute_errors": honest_sum,
                        "mae": div(honest_sum, forecasts)},
        "with_the_leaked_feature": {"forecasts_with_an_error": leaky_errors, "sum_of_absolute_errors": leaky_sum,
                                    "mae": div(leaky_sum, forecasts)},
        "change": change(leaky_sum, honest_sum),
        "on_all_pairs_of_consecutive_rows": {
            "note": "No restart at rebaseline rows: the feature fails exactly where the feeder wrote 0.",
            "pairs": len(pairs), "pairs_the_feature_misses": len(misses),
            "sum_of_absolute_errors_with_the_feature": sum(abs(l["count"] - e["count"] - l["delta"]) for e, l in misses),
            "sum_of_absolute_errors_of_persistence": sum(abs(l["count"] - e["count"]) for _, e, l in pairs)},
    }


def leakage_section(table: dict, series: list[dict], cfg: dict, min_train: int) -> dict:
    varying = [s for s in series if len(set(s["values"])) > 1]
    share = Fraction(*cfg["time_split"]["test_share"])
    rows_for = lambda values: max(1, int(len(values) * share))  # noqa: E731
    frames = {s["artifact"]: leak_frame(s["values"], rows_for(s["values"])) for s in varying}
    check("the series that vary have one shape: the three tests give the same numbers on each",
          len({json.dumps(frame, sort_keys=True) for frame in frames.values()}) == 1)
    check("a fitted level makes no error on a series that never varies, under any of the three tests",
          all(time_split(s["values"], rows_for(s["values"])) == (0, 0)
              and random_split(s["values"], rows_for(s["values"]))["expected"] == 0
              for s in series if len(set(s["values"])) == 1))
    values = varying[0]["values"]
    test_rows = rows_for(values)
    honest = time_split(values, test_rows)[0]
    shuffled = random_split(values, test_rows)
    draw = cfg["random_split_cross_check"]
    simulated = random_split_simulated(values, test_rows, draw["seed"], draw["draws"])
    check("seeded random splits agree with the exact average within the tolerance",
          abs(simulated - shuffled["expected"]) < Fraction(str(draw["tolerance"])))
    rolling = rolling_origin(values, min_train)
    so_far = sum(abs(row["errors"]["mean"]) for row in rolling)
    whole = sum(abs(row["actual"] - Fraction(sum(values), len(values))) for row in rolling)
    return {
        "kind": "computed on the series that vary; the series that never vary add zero error under every test",
        "definition": "A backtest leaks when the forecast scored for a target row was computed from anything not "
                      "yet recorded at its origin: the target, a later row, or a number derived from them.",
        "artifacts": sorted(frames),
        "fitted_level_on_the_last_quarter": frames[varying[0]["artifact"]] | {
            "leak_3_splits": shuffled["splits"],
            "leak_3_splits_reporting_at_least_the_split_in_time_mae":
                sum(case["ways"] for case in shuffled["cases"] if case["mae"] >= honest),
            "leak_3_lowest_and_highest_mae_of_one_split":
                [num(min(case["mae"] for case in shuffled["cases"])), num(max(case["mae"] for case in shuffled["cases"]))],
            "leak_3_seeded_cross_check": {"seed": draw["seed"], "draws": draw["draws"], "mae": num(simulated)}},
        "leak_2_feature_that_encodes_the_target": target_feature_leak(table, series, min_train),
        "leak_1_under_the_rolling_origin": {
            "note": "Same targets as rolling_origin: the mean so far against the mean of the whole series.",
            "forecasts": len(rolling), "mean_so_far_mae": div(so_far, len(rolling)),
            "whole_series_mean_mae": div(whole, len(rolling)), "change": change(whole, so_far)},
        "cut_sweep": cut_sweep(values, min_train),
    }


def dependence_section(snapshot: dict, series: list[dict], min_train: int, extrapolation: dict) -> dict:
    """How many independent events the backtest holds."""
    steps = [(s["artifact"], s["runs"][index], s["values"][index] - s["values"][index - 1])
             for s in series for index in range(1, len(s["values"])) if s["values"][index] != s["values"][index - 1]]
    change_runs = sorted({run for _, run, _ in steps})
    varying = [s for s in series if len(set(s["values"])) > 1]
    profiles = {json.dumps([[str(row["errors"][m]) for m in METHODS] for row in rolling_origin(s["values"], min_train)])
                for s in varying}
    target_runs = {s["runs"][index] for s in series for index in range(min_train, len(s["values"]))}
    window = [s for s in series if s["kind"] == KINDS[1]]
    window_steps = {len(s["values"]) - 1 for s in window}
    check("every series that starts at a rebaseline row has the same number of rows", len(window_steps) == 1)
    check("every count change inside a series lies in a series that starts at a rebaseline row",
          {artifact for artifact, _, _ in steps} <= {s["artifact"] for s in window} and all(s in window for s in varying))
    per_change_run = Fraction(window_steps.pop(), len(change_runs))
    return {
        "kind": "computed",
        "count_changes_inside_a_series": len(steps),
        "artifacts": sorted(artifact for artifact, _, _ in steps),
        "distinct_runs_with_a_change": len(change_runs),
        "change_runs": [snapshot["runs"][run]["timestamp"] for run in change_runs],
        "distinct_steps": sorted({step for _, _, step in steps}),
        "distinct_error_profiles_among_the_series_that_vary": len(profiles),
        "target_runs": len(target_runs),
        "target_runs_with_a_persistence_error": len(change_runs),
        "independent_events_at_most": len(change_runs),
        "coin_flip_illustration": {
            "note": "Chance that one method beats another on every comparison if each were a fair coin flip.",
            "four_independent_series": str(Fraction(1, 2) ** len(varying)),
            "one_event": str(Fraction(1, 2) ** len(change_runs))},
        "extrapolation": {
            "kind": "computed under a stated assumption, not a forecast",
            "assumption": extrapolation["assumption"],
            "run_to_run_steps_between_rebaselined_runs": int(per_change_run * len(change_runs)),
            "run_to_run_steps_per_change_run": num(per_change_run),
            "targets": [{"change_runs_expected": target, "run_to_run_steps_needed": num(target * per_change_run),
                         "runs_needed": math.ceil(target * per_change_run) + 1}
                        for target in extrapolation["target_change_runs"]]},
    }


def whole_record_section(table: dict, min_train: int) -> dict:
    """The same backtest without restarting the series at rebaseline rows."""
    whole = [{"values": [row["count"] for row in rows if row["count"] is not None]} for rows in table.values()]
    pooled = score(whole, min_train)
    at_rebaseline = sum(abs(later["count"] - earlier["count"])
                        for _, earlier, later in consecutive_pairs(table) if later["rebaseline"])
    total = absolute_errors(whole, min_train)[1]["persistence"]
    check("whole record: persistence errs by the steps at rebaseline rows plus the steps inside a series",
          total == at_rebaseline + absolute_errors(split_series(table), min_train)[1]["persistence"])
    return {
        "kind": "computed; a contrast, not the module's main test",
        "note": "One series per artifact, rebaseline rows kept as targets: the forecast then has to anticipate a "
                "change of instrument.",
        "series": len(whole), **pooled,
        "persistence_error_at_rebaseline_rows": at_rebaseline,
        "share_of_the_persistence_error_at_rebaseline_rows": div(at_rebaseline, total)
        | {"percent": round(float(100 * at_rebaseline / total), DECIMALS["percent"])},
    }


def measure(snapshot: dict, min_train: int) -> dict:
    """The counters that the negative controls must be able to move."""
    table = load_rows(snapshot)
    series = split_series(table)
    pairs = consecutive_pairs(table)
    return {
        "count_changes": sum(earlier["count"] != later["count"] for _, earlier, later in pairs),
        "rows_that_break_the_delta_rule": delta_rule_mismatches(table)[1],
        "series": len(series),
        "series_that_vary": sum(len(set(s["values"])) > 1 for s in series),
        "persistence_sum_of_absolute_errors":
            sum(abs(s["values"][i] - s["values"][i - 1]) for s in series for i in range(min_train, len(s["values"]))),
        "forecasts_missed_with_the_leaked_feature":
            sum(s["values"][i] != s["values"][i - 1] + s["deltas"][i] for s in series for i in range(min_train, len(s["values"]))),
    }


def set_token(artifact: dict, key: str, index: int, token: str, separator: str) -> None:
    cells = artifact[key].split(separator) if separator else list(artifact[key])
    cells[index] = token
    artifact[key] = separator.join(cells)


def negative_controls(snapshot: dict, series: list[dict], min_train: int) -> dict:
    """Plant a defect in a copy of the snapshot and confirm that each counter sees it."""
    base = measure(snapshot, min_train)
    flat = next(s for s in series if s["kind"] == KINDS[1] and len(set(s["values"])) == 1)
    run = flat["runs"][len(flat["runs"]) // 2]
    jump = max((s for s in series if s["kind"] == KINDS[1]), key=lambda s: (abs(s["values"][0] - prior(series, s)), s["artifact"]))

    def planted(artifact_name: str, edits: list[tuple]) -> dict:
        clone = copy.deepcopy(snapshot)
        artifact = next(a for a in clone["artifacts"] if a["name"] == artifact_name)
        for key, index, token, separator in edits:
            set_token(artifact, key, index, token, separator)
        return measure(clone, min_train)

    blip = planted(flat["artifact"], [("citation_count", run, str(flat["values"][0] + 1), " ")])
    wrong_delta = planted(flat["artifact"], [("delta_citations", run, "1", " ")])
    unflagged = planted(jump["artifact"], [("rebaseline_flag", jump["runs"][0], "f", "")])
    size = abs(jump["values"][0] - prior(series, jump))
    check("negative control: one planted count is seen as two changes, two broken deltas and one more varying series",
          (blip["count_changes"], blip["rows_that_break_the_delta_rule"], blip["series_that_vary"],
           blip["persistence_sum_of_absolute_errors"], blip["forecasts_missed_with_the_leaked_feature"])
          == (base["count_changes"] + 2, base["rows_that_break_the_delta_rule"] + 2, base["series_that_vary"] + 1,
              base["persistence_sum_of_absolute_errors"] + 2, base["forecasts_missed_with_the_leaked_feature"] + 2))
    check("negative control: one planted delta_citations breaks the rule once and the leaked feature once",
          (wrong_delta["rows_that_break_the_delta_rule"], wrong_delta["forecasts_missed_with_the_leaked_feature"],
           wrong_delta["count_changes"]) == (base["rows_that_break_the_delta_rule"] + 1,
                                             base["forecasts_missed_with_the_leaked_feature"] + 1, base["count_changes"]))
    check("negative control: a removed rebaseline flag merges two series and adds the jump to the persistence error",
          (unflagged["series"], unflagged["persistence_sum_of_absolute_errors"], unflagged["rows_that_break_the_delta_rule"])
          == (base["series"] - 1, base["persistence_sum_of_absolute_errors"] + size, base["rows_that_break_the_delta_rule"] + 1))
    return {
        "before": base,
        "one_count_raised_by_1": {"artifact": flat["artifact"], "run": snapshot["runs"][run]["timestamp"], "after": blip},
        "one_delta_citations_set_to_1": {"artifact": flat["artifact"], "run": snapshot["runs"][run]["timestamp"],
                                         "after": wrong_delta},
        "one_rebaseline_flag_removed": {"artifact": jump["artifact"], "run": snapshot["runs"][jump["runs"][0]]["timestamp"],
                                        "jump": size, "after": unflagged},
    }


def prior(series: list[dict], later: dict) -> int:
    """The last count of the same artifact's series before a rebaseline row."""
    return next(s["values"][-1] for s in series if s["artifact"] == later["artifact"] and s["kind"] == KINDS[0])


def transfer_task(task: dict) -> dict:
    min_train = task["min_training_rows"]
    series = [{"artifact": name, "values": values} for name, values in task["series"].items()]
    values = task["series"][task["worked_series"]]
    steps = [(s["artifact"], index + 1) for s in series for index in range(1, len(s["values"]))
             if s["values"][index] != s["values"][index - 1]]
    rows = rolling_origin(values, min_train)
    target = next(row for row in rows if row["target_row"] == task["scaled_error_target_week"])
    test_rows = task["time_split_test_rows"]
    honest, whole = time_split(values, test_rows)
    weeks = task["random_split_test_weeks"]
    train = [value for week, value in enumerate(values, 1) if week not in weeks]
    given = mae_of_level([values[week - 1] for week in weeks], Fraction(sum(train), len(train)))
    shuffled = random_split(values, len(weeks))
    check("transfer task: the random-split formula equals a listing of every split",
          shuffled["expected"] == random_split_enumerated(values, len(weeks)))
    first, _, _ = single_step(values)
    varying = [s for s in series if len(set(s["values"])) > 1]
    profiles = {json.dumps([[str(row["errors"][m]) for m in METHODS] for row in rolling_origin(s["values"], min_train)])
                for s in varying}
    persistence_sum = sum(abs(row["errors"]["persistence"]) for row in rows)
    # The task's change column: this week's count minus last week's. Adding it to last week's count gives the target.
    changes = [0] + [later - earlier for earlier, later in zip(values, values[1:])]
    leaked_sum = sum(abs(values[i] - (values[i - 1] + changes[i])) for i in range(min_train, len(values)))
    return {
        "note": task["note"],
        "q1_counting": {"series": len(series), "rows": sum(len(s["values"]) for s in series),
                        "forecasts": sum(len(s["values"]) - min_train for s in series), "count_changes": len(steps),
                        "distinct_weeks_with_a_change": len({week for _, week in steps}),
                        "series_that_never_vary": sum(len(set(s["values"])) == 1 for s in series)},
        "q2_rolling_origin": {"series": task["worked_series"]} | score([{"values": values}], min_train) | {
            "absolute_errors_by_target_week": [
                {"week": row["target_row"]} | {method: num(abs(row["errors"][method])) for method in METHODS}
                for row in rows]},
        "q3_scaled_error": {
            "series_with_no_scaled_error_at_all": sum(len(set(s["values"])) == 1 for s in series),
            "scale_at_the_origin_before_the_step": num(naive_scale(values, first)),
            "target_week": target["target_row"], "scale_at_its_origin": num(target["scale"]),
            "scaled_errors": {method: div(abs(target["errors"][method]), target["scale"]) for method in METHODS}},
        "q4_leaks": {
            "split_in_time": {"test_weeks": list(range(len(values) - test_rows + 1, len(values) + 1)), "mae": num(honest)},
            "level_fitted_on_every_week": {"mae": num(whole), "change": change(whole, honest)},
            "change_column": {"forecast": "last week's count + this week's change",
                              "rolling_origin_mae": div(leaked_sum, len(rows)),
                              "persistence_rolling_origin_mae": div(persistence_sum, len(rows)),
                              "change": change(leaked_sum, persistence_sum)},
            "random_split_given": {"test_weeks": weeks, "mae": num(given), "change": change(given, honest)},
            "random_split_all": {"splits": shuffled["splits"], "expected_mae": num(shuffled["expected"]),
                                 "splits_with_every_test_week_after_the_step":
                                     next(case["ways"] for case in shuffled["cases"] if case["k"] == len(weeks))}},
        "q5_dependence": {"series_that_vary": len(varying),
                          "distinct_error_profiles": len(profiles),
                          "independent_events_at_most": len({week for _, week in steps})},
    }


def analyze(snapshot: dict, scenarios: dict) -> dict:
    if scenarios["rounding"] != {f"{key}_decimals": value for key, value in DECIMALS.items()}:
        raise ValueError("scenarios.json rounding does not match analyze.py")
    min_train = scenarios["rolling_origin"]["min_training_rows"]
    table = load_rows(snapshot)
    series = split_series(table)
    hand_computed_case()
    observed = observed_section(snapshot, table)
    variation = variation_section(snapshot, table)
    return {
        "module_id": snapshot["module_id"],
        "rounding": "values to 6 decimals, percentages to 2 decimals, days to 3 decimals; 'exact' is the unrounded "
                    "fraction, left out when its denominator has more than 12 digits",
        "source": {"repository": snapshot["source"]["repository"], "commit": snapshot["source"]["commit"],
                   "files": [entry["path"] for entry in snapshot["source"]["files"] + snapshot["source"]["context_files"]]},
        "observed": observed,
        "variation": variation,
        "series": series_section(snapshot, series, min_train, variation["pairs_of_consecutive_rows_with_a_count"],
                                 variation["pairs_ending_at_a_rebaseline_row"]),
        "rolling_origin": rolling_section(snapshot, series, min_train, scenarios["run_gap_bounds_days"]),
        "scaled_error": scaled_error_section(series, min_train),
        "leakage": leakage_section(table, series, scenarios["leakage"], min_train),
        "dependence": dependence_section(snapshot, series, min_train, scenarios["extrapolation"]),
        "whole_record_contrast": whole_record_section(table, min_train),
        "negative_controls": negative_controls(snapshot, series, min_train),
        "transfer_task": transfer_task(scenarios["transfer_task"]),
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
