#!/usr/bin/env python3
"""PSY-011 analysis: which jumps in the citation counts are the instrument changing.

Reads observed-input.json (written by extract.py) and scenarios.json, never
the repository, and writes results.json. Every result is an exact count, a
difference or a ratio of counts, or a mean and a standard deviation of counts
or of counts per day; no random number is drawn.

Run from the repository root:
    python -I scripts/streeling_fixtures/psychohistory/psy-011/analyze.py
    python -I scripts/streeling_fixtures/psychohistory/psy-011/analyze.py --check
"""

from __future__ import annotations

import argparse
import copy
import json
import math
import sys
from dataclasses import dataclass
from datetime import datetime
from fractions import Fraction
from pathlib import Path

# This program lives under scripts/ (CONTRIBUTING.md: no executable code outside scripts/); its data stays
# under state/streeling/fixtures/. FIXTURE_FILE is the path the program would have next to that data.
FIXTURE_FILE = (Path(__file__).resolve().parents[4]
                / "state/streeling/fixtures/psychohistory/psy-011" / Path(__file__).name)

HERE = FIXTURE_FILE.parent
NO_ROW, ABSENT, NULL = ".", "-", "n"
DECIMALS = {"ratio": 6, "percent": 2, "statistic": 4}
CLASSES = ("no_count", "first_count", "instrument_change", "same_instrument")
PARTS = CLASSES[1:]  # the three ways a run's total can move
NO_SOURCE = "no citation_source"
SERIES = {
    "total": "step of the citation count summed over every artifact that has a count",
    "recorded_delta": "sum of delta_citations as the feeder wrote it (the step hidden by a rebaseline flag is not in it)",
    "same_instrument": "sum of the count steps of rows whose previous row has a count from the same source",
}
DAY = 86400  # seconds
# Label (see extract.py, label()) of the artifact for which the producer's docstring gives a count before and after.
DOCSTRING_ARTIFACT = "policies / alignment-policy.yaml"
CHECKS: dict[str, int] = {}  # self-check -> times evaluated


@dataclass
class Log:
    """The observed log once classified, with the landmark runs that several sections of the results need."""

    runs: list[dict]  # the snapshot's runs in time order: index, timestamp, rows
    table: dict[str, list[dict]]  # artifact -> its rows in run order
    records: list[dict]  # one classified record per row
    counters: dict  # measure(records)
    per_run: list[dict]  # totals(records, number of runs)
    key_run: int = -1  # first run whose rows carry the citation_source key
    first_feeder: int = -1  # first run that has a citation count
    seed_runs: int = 0  # runs that hold seed rows

    def stamp(self, index: int) -> str:
        return self.runs[index]["timestamp"]


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


def statistic(value: Fraction | float) -> float:
    return round(float(value), DECIMALS["statistic"])


def feeder_rule(previous: dict | None, count: int, source: str | None) -> tuple[bool, int]:
    """Lines 90-99 of the pinned scripts/quality_trend.py, for one row.

    previous is None when the artifact has no earlier row, else its last row as
    {"count": int or None, "source": str or None}; a key that the earlier row
    lacks reads as None, as dict.get returns it. Returns (rebaseline, delta_citations).
    """
    rebaseline = previous is not None and previous["source"] != source
    previous_count = (previous["count"] or 0) if previous is not None else 0
    return rebaseline, 0 if rebaseline else count - previous_count


def load_rows(snapshot: dict) -> dict[str, list[dict]]:
    """Per artifact, its rows in run order, decoded from the aligned strings."""
    runs = len(snapshot["runs"])
    letters = snapshot["encoding"]["citation_source_values"]
    table = {}
    for artifact in snapshot["artifacts"]:
        columns = (artifact["citation_count"].split(" "), artifact["delta_citations"].split(" "),
                   artifact["citation_source"], artifact["rebaseline"], artifact["baseline_flag"])
        if any(len(column) != runs for column in columns):
            raise ValueError(f"{artifact['name']}: a column is not aligned with the {runs} runs")
        rows = []
        for index, (count, delta, source, flag, seed) in enumerate(zip(*columns)):
            if len({cell == NO_ROW for cell in (count, delta, source, flag, seed)}) != 1:
                raise ValueError(f"{artifact['name']}: run {index} is a row in one column and not in another")
            if count == NO_ROW:
                continue
            if (source == ABSENT) != (flag == ABSENT):
                raise ValueError(f"{artifact['name']}: run {index} has one of citation_source and rebaseline only")
            rows.append({"run": index, "count": None if count == ABSENT else int(count), "delta": int(delta),
                         "has_key": source != ABSENT, "source": None if source in (ABSENT, NULL) else letters[source],
                         "flag": None if flag == ABSENT else flag == "t", "seed": seed == "s"})
        table[artifact["name"]] = rows
    return table


def classify(table: dict[str, list[dict]]) -> list[dict]:
    """One record per row: its class against the unit's previous row, and what the pinned rule gives.

    no_count           the row has no citation_count (a seed row)
    first_count        the row has a count and no earlier row of the unit has one
    instrument_change  the previous row has a count and another citation_source
    same_instrument    the previous row has a count and the same citation_source
    """
    records = []
    for name, rows in table.items():
        previous = None
        for row in rows:
            record = dict(row) | {"unit": name, "has_previous": previous is not None,
                                  "previous_count": previous["count"] if previous else None}
            if row["count"] is None:
                record |= {"class": "no_count", "step": None, "rule": None}
            else:
                seen = None if previous is None else {"count": previous["count"], "source": previous["source"]}
                if previous is None or previous["count"] is None:
                    kind, step = "first_count", None
                else:
                    kind = "instrument_change" if previous["source"] != row["source"] else "same_instrument"
                    step = row["count"] - previous["count"]
                record |= {"class": kind, "step": step, "rule": feeder_rule(seen, row["count"], row["source"])}
            records.append(record)
            previous = row
    return records


def measure(records: list[dict]) -> dict:
    """Every counter of the classification, from the classified rows."""
    by_class = {name: [r for r in records if r["class"] == name] for name in CLASSES}
    counted = [r for r in records if r["class"] != "no_count"]
    nonzero = [r for r in records if r["delta"] != 0]
    changed = [r for r in records if r["step"]]
    first, change, same = by_class["first_count"], by_class["instrument_change"], by_class["same_instrument"]
    same_by_source: dict[str, dict] = {}
    for r in same:
        cell = same_by_source.setdefault(r["source"] or NO_SOURCE, {"pairs": 0, "count_changed": 0})
        cell["pairs"] += 1
        cell["count_changed"] += bool(r["step"])
    return {
        "rows": len(records),
        "units": len({r["unit"] for r in records}),
        "rows_by_class": {name: len(rows) for name, rows in by_class.items()},
        "first_count": {
            "rows": len(first),
            "after_a_row_without_count": sum(r["has_previous"] for r in first),
            "first_row_of_the_unit": sum(not r["has_previous"] for r in first),
            "nonzero_delta": sum(r["delta"] != 0 for r in first),
            "nonzero_delta_after_a_row_without_count": sum(r["delta"] != 0 and r["has_previous"] for r in first),
            "nonzero_delta_in_a_first_row": sum(r["delta"] != 0 and not r["has_previous"] for r in first),
            "zero_delta": sum(r["delta"] == 0 for r in first),
            "sum_of_delta": sum(r["delta"] for r in first),
        },
        "instrument_change": {
            "rows": len(change),
            "runs": len({r["run"] for r in change}),
            "count_changed": sum(bool(r["step"]) for r in change),
            "count_unchanged": sum(not r["step"] for r in change),
            "raised": sum(r["step"] > 0 for r in change),
            "lowered": sum(r["step"] < 0 for r in change),
            "nonzero_delta": sum(r["delta"] != 0 for r in change),
            "flagged_rebaseline": sum(r["flag"] is True for r in change),
            "sum_of_steps": sum(r["step"] for r in change),
        },
        "same_instrument": {
            "pairs": len(same),
            "count_changed": sum(bool(r["step"]) for r in same),
            "nonzero_delta": sum(r["delta"] != 0 for r in same),
            "runs_with_a_change": len({r["run"] for r in same if r["step"]}),
            "sum_of_steps": sum(r["step"] for r in same),
            "by_source": same_by_source,
        },
        "two_definitions": {
            "rows_with_nonzero_delta_citations": len(nonzero),
            "rows_where_the_count_changed": len(changed),
            "both": sum(bool(r["step"]) for r in nonzero),
            "nonzero_delta_only": sum(not r["step"] for r in nonzero),
            "count_changed_only": sum(r["delta"] == 0 for r in changed),
            "either": len({(r["unit"], r["run"]) for r in nonzero + changed}),
        },
        "nonzero_delta_rows_by_class": {name: sum(r["delta"] != 0 for r in by_class[name]) for name in CLASSES},
        "count_changes_by_class": {name: sum(bool(r["step"]) for r in by_class[name]) for name in CLASSES[2:]},
        "row_pairs": {
            "row_pairs": len(records) - len({r["unit"] for r in records}),
            "starting_at_a_row_without_count": sum(r["has_previous"] for r in records) - len(change) - len(same),
            "across_an_instrument_change": len(change),
            "same_instrument": len(same),
        },
        "rule_reproduction": {
            "rows_with_a_count": len(counted),
            "delta_mismatches": sum(r["rule"][1] != r["delta"] for r in counted),
            "rows_with_a_rebaseline_flag": sum(r["flag"] is not None for r in counted),
            "flag_mismatches": sum(r["flag"] is not None and r["rule"][0] != r["flag"] for r in counted),
            "flagged_rows_not_at_an_instrument_change": sum(r["flag"] is True and r["class"] != "instrument_change"
                                                            for r in records),
        },
    }


def totals(records: list[dict], runs: int) -> list[dict]:
    """Per run: the summed count, the summed delta_citations, and the summed count step by class."""
    per_run = [{"rows": 0, "rows_with_count": 0, "total": 0, "recorded_delta": 0,
                "first_count": 0, "instrument_change": 0, "same_instrument": 0} for _ in range(runs)]
    for r in records:
        cell = per_run[r["run"]]
        cell["rows"] += 1
        cell["recorded_delta"] += r["delta"]
        if r["count"] is None:
            continue
        cell["rows_with_count"] += 1
        cell["total"] += r["count"]
        cell[r["class"]] += r["count"] if r["class"] == "first_count" else r["step"]
    return per_run


def check_accounting(tag: str, table: dict, records: list[dict], counters: dict, per_run: list[dict]) -> None:
    """The accounting identities of one classified log (the observed one, the hand-computed case, the transfer task)."""
    by_class, pairs, first = counters["rows_by_class"], counters["row_pairs"], counters["first_count"]
    check(f"{tag}: the four classes sum to the rows", sum(by_class.values()) == counters["rows"])
    check(f"{tag}: row pairs = rows - units = pairs from a row without count + across a change + same instrument",
          pairs["row_pairs"] == pairs["starting_at_a_row_without_count"] + pairs["across_an_instrument_change"]
          + pairs["same_instrument"])
    check(f"{tag}: every unit has exactly one first count",
          by_class["first_count"] == counters["units"] and first["rows"] == first["nonzero_delta"] + first["zero_delta"])
    check(f"{tag}: a unit has a row in every run from its first row on",
          all([row["run"] for row in rows] == list(range(rows[0]["run"], rows[0]["run"] + len(rows)))
              for rows in table.values()))
    check(f"{tag}: rows without a count carry a zero delta",
          all(r["delta"] == 0 for r in records if r["class"] == "no_count"))
    two = counters["two_definitions"]
    check(f"{tag}: non-zero deltas and count changes split into both, one only and the other only",
          two["rows_with_nonzero_delta_citations"] == two["both"] + two["nonzero_delta_only"]
          and two["rows_where_the_count_changed"] == two["both"] + two["count_changed_only"]
          and two["either"] == two["both"] + two["nonzero_delta_only"] + two["count_changed_only"])
    check(f"{tag}: non-zero deltas by class sum to the non-zero deltas",
          sum(counters["nonzero_delta_rows_by_class"].values()) == two["rows_with_nonzero_delta_citations"])
    check(f"{tag}: count changes by class sum to the count changes",
          sum(counters["count_changes_by_class"].values()) == two["rows_where_the_count_changed"])
    check(f"{tag}: same-instrument pairs by source sum to the same-instrument pairs",
          sum(cell["pairs"] for cell in counters["same_instrument"]["by_source"].values())
          == counters["same_instrument"]["pairs"])
    previous_total = 0
    for cell in per_run:
        check(f"{tag}: step of the total = first counts + steps at an instrument change + same-instrument steps",
              cell["total"] - previous_total == cell["first_count"] + cell["instrument_change"] + cell["same_instrument"])
        previous_total = cell["total"]
    check(f"{tag}: latest total = sum of the three parts over all runs",
          per_run[-1]["total"] == sum(cell[key] for cell in per_run for key in PARTS))


def band(history: list, rule: dict) -> tuple[Fraction, Fraction, float] | None:
    """Mean and squared allowed distance (both exact) and standard deviation of the rule over `history`.

    None when the history is too short for the next value to be tested.
    """
    if len(history) < rule["minimum_history_steps"]:
        return None
    mean = Fraction(sum(history), len(history))
    variance = Fraction(sum(x * x for x in history), len(history)) - mean * mean
    return mean, rule["multiplier"] ** 2 * variance, math.sqrt(float(variance))


def rule_detail(steps: list[int], position: int, rule: dict) -> dict:
    """The two-sigma rule for the step at `position`, against all earlier steps (exact decision)."""
    history, step = steps[:position], steps[position]
    limits = band(history, rule)
    if limits is None:
        return {"step": step, "earlier_steps": len(history), "tested": False, "flagged": False}
    mean, bound, deviation = limits
    smallest = math.floor(mean) + 1
    while (smallest - mean) ** 2 <= bound:
        smallest += 1
    return {"step": step, "earlier_steps": len(history), "tested": True,
            "mean": statistic(mean), "standard_deviation": statistic(deviation),
            "distance_from_mean": statistic(abs(step - mean)),
            "allowed_distance": statistic(rule["multiplier"] * deviation),
            "smallest_upward_step_that_would_be_flagged": smallest,
            "flagged": (step - mean) ** 2 > bound}


def rate_detail(rates: list[Fraction], position: int, rule: dict) -> dict:
    """The same rule for a step per day at `position`, against all earlier steps per day (exact decision)."""
    limits, rate = band(rates[:position], rule), rates[position]
    if limits is None:
        return {"step_per_day": statistic(rate), "tested": False, "flagged": False}
    mean, bound, deviation = limits
    return {"step_per_day": statistic(rate), "tested": True,
            "mean": statistic(mean), "standard_deviation": statistic(deviation),
            "distance_from_mean": statistic(abs(rate - mean)),
            "allowed_distance": statistic(rule["multiplier"] * deviation),
            "flagged": (rate - mean) ** 2 > bound}


def series_steps(per_run: list[dict], first: int) -> dict[str, list[int]]:
    """Step series over the runs after `first`, the first run that has a total."""
    later = range(first + 1, len(per_run))
    return {"total": [per_run[i]["total"] - per_run[i - 1]["total"] for i in later],
            "recorded_delta": [per_run[i]["recorded_delta"] for i in later],
            "same_instrument": [per_run[i]["same_instrument"] for i in later]}


def two_sigma(per_run: list[dict], first: int, rule: dict, label) -> dict:
    """The rule on each of the three step series; `label` names a run by its index."""
    out = {}
    for name, steps in series_steps(per_run, first).items():
        details = [rule_detail(steps, position, rule) for position in range(len(steps))]
        nonzero = [{"run": label(first + 1 + position)} | detail
                   for position, detail in enumerate(details) if detail["step"] != 0]
        out[name] = {"definition": SERIES[name], "steps": len(steps), "tested_steps": sum(d["tested"] for d in details),
                     "nonzero_steps": len(nonzero), "flagged_steps": sum(d["flagged"] for d in details),
                     "flagged_runs": [entry["run"] for entry in nonzero if entry["flagged"]],
                     "nonzero_step_details": nonzero}
        check("two-sigma rule: every step with enough earlier steps is tested, and only tested steps are flagged",
              sum(d["tested"] for d in details) == max(0, len(steps) - rule["minimum_history_steps"])
              and all(d["tested"] or not d["flagged"] for d in details))
    return out


def hand_computed_cases(rule: dict) -> None:
    """Two artifacts over six runs, and four step histories, worked by hand in the README."""
    toy = {"runs": [{"timestamp": f"2026-01-0{day}T00:00:00Z"} for day in range(1, 7)],
           "encoding": {"citation_source_values": {"a": "g1"}},
           "artifacts": [
               {"name": "a", "citation_count": "- 3 3 9 9 11", "delta_citations": "0 3 0 0 0 2",
                "citation_source": "---aaa", "rebaseline": "---tff", "baseline_flag": "s-----"},
               {"name": "b", "citation_count": ". . 2 2 2 2", "delta_citations": ". . 2 0 0 0",
                "citation_source": "..--nn", "rebaseline": "..--ff", "baseline_flag": "..----"}]}
    table = load_rows(toy)
    records = classify(table)
    counters = measure(records)
    per_run = totals(records, 6)
    check_accounting("hand-computed case", table, records, counters, per_run)
    check("hand-computed case: 10 rows = 1 without count + 2 first counts + 1 instrument change + 6 same instrument",
          counters["rows_by_class"] == {"no_count": 1, "first_count": 2, "instrument_change": 1, "same_instrument": 6})
    check("hand-computed case: 3 non-zero deltas, 2 count changes, 1 row is both, 1 change remains",
          counters["two_definitions"] == {"rows_with_nonzero_delta_citations": 3, "rows_where_the_count_changed": 2,
                                          "both": 1, "nonzero_delta_only": 2, "count_changed_only": 1, "either": 4}
          and counters["same_instrument"]["count_changed"] == 1)
    check("hand-computed case: the rule reproduces every delta and every flag",
          counters["rule_reproduction"]["delta_mismatches"] == 0 and counters["rule_reproduction"]["flag_mismatches"] == 0)
    check("hand-computed case: totals 0, 3, 5, 11, 11, 13 = recorded deltas 7 + hidden step 6",
          [cell["total"] for cell in per_run] == [0, 3, 5, 11, 11, 13]
          and sum(cell["recorded_delta"] for cell in per_run) == 7 and counters["instrument_change"]["sum_of_steps"] == 6)
    check("hand-computed rule: after 1, 3, 1, 3 (mean 2, standard deviation 1) a step of 6 is flagged and 4 is not",
          rule_detail([1, 3, 1, 3, 6], 4, rule)["flagged"] and not rule_detail([1, 3, 1, 3, 4], 4, rule)["flagged"]
          and rule_detail([1, 3, 1, 3, 6], 4, rule)["smallest_upward_step_that_would_be_flagged"] == 5)
    check("hand-computed rule: after an all-zero history any non-zero step is flagged; too short a history is not tested",
          rule_detail([0, 0, 0, 1], 3, rule)["flagged"] and not rule_detail([0, 0, 0, 0], 3, rule)["flagged"]
          and not rule_detail([0, 0, 5], 2, rule)["tested"])
    daily = [Fraction(step) for step in (1, 3, 1, 3)]
    check("hand-computed rule per day: after 1, 3, 1, 3 per day, 6 in three days (2 per day) is not flagged "
          "and 3 in half a day (6 per day) is",
          not rate_detail(daily + [Fraction(6, 3)], 4, rule)["flagged"]
          and rate_detail(daily + [3 / Fraction(1, 2)], 4, rule)["flagged"])


def rule_cases(cases: list[dict]) -> list[dict]:
    """The pinned rule applied to each imaginary row of scenarios.json."""
    out = []
    for case in cases:
        previous = case["previous"]
        rebaseline, delta = feeder_rule(previous, case["count"], case["source"])
        step = None if previous is None or previous["count"] is None else case["count"] - previous["count"]
        out.append({"name": case["name"], "description": case["description"], "previous": previous,
                    "count": case["count"], "source": case["source"], "rebaseline": rebaseline,
                    "delta_citations": delta, "count_step": step,
                    "step_not_in_delta_citations": 0 if step is None else step - delta})
    return out


def negative_controls(table: dict, snapshot: dict, base: dict, key_run: int) -> dict:
    """Plant one defect at a time in a copy of the rows and confirm that the counters see it."""
    target = next(name for name, rows in sorted(table.items())
                  if rows[0]["run"] == 0 and any(row["flag"] for row in rows))
    hand_run, grep_run = key_run // 2, key_run + (len(snapshot["runs"]) - key_run) // 2

    def recount(edit) -> dict:
        planted = copy.deepcopy(table)
        edit({row["run"]: row for row in planted[target]})
        return measure(classify(planted))

    def bump(rows):
        rows[hand_run]["count"] += 1

    def delta_on_flagged_row(rows):
        rows[key_run]["delta"] = 5

    def stray_flag(rows):
        rows[grep_run]["flag"] = True

    def silent_source_change(rows):
        for index in rows:
            if index >= grep_run:
                rows[index]["source"] = "another-source"

    bumped, delta, flagged, silent = (recount(edit) for edit in (bump, delta_on_flagged_row, stray_flag,
                                                                 silent_source_change))
    hand = base["same_instrument"]["by_source"][NO_SOURCE]["count_changed"]
    check("negative control: a count bumped for one run where no source is recorded is counted as two changes",
          bumped["same_instrument"]["by_source"][NO_SOURCE]["count_changed"] == hand + 2
          and bumped["rule_reproduction"]["delta_mismatches"] == base["rule_reproduction"]["delta_mismatches"] + 2)
    check("negative control: a non-zero delta on a rebaseline row is counted",
          delta["nonzero_delta_rows_by_class"]["instrument_change"]
          == base["nonzero_delta_rows_by_class"]["instrument_change"] + 1
          and delta["rule_reproduction"]["delta_mismatches"] == base["rule_reproduction"]["delta_mismatches"] + 1)
    check("negative control: a rebaseline flag without a change of source is reported",
          flagged["rule_reproduction"]["flag_mismatches"] == base["rule_reproduction"]["flag_mismatches"] + 1
          and flagged["rule_reproduction"]["flagged_rows_not_at_an_instrument_change"]
          == base["rule_reproduction"]["flagged_rows_not_at_an_instrument_change"] + 1)
    check("negative control: a change of source without a flag is reported",
          silent["instrument_change"]["rows"] == base["instrument_change"]["rows"] + 1
          and silent["rule_reproduction"]["flag_mismatches"] == base["rule_reproduction"]["flag_mismatches"] + 1)
    stamp = lambda index: snapshot["runs"][index]["timestamp"]  # noqa: E731
    return {
        "planted_in": target,
        "count_raised_by_one_for_one_run": {
            "run": stamp(hand_run),
            "count_changes_where_no_source_is_recorded_before_and_after":
                [hand, bumped["same_instrument"]["by_source"][NO_SOURCE]["count_changed"]],
            "rows_whose_delta_the_rule_does_not_reproduce_before_and_after":
                [base["rule_reproduction"]["delta_mismatches"], bumped["rule_reproduction"]["delta_mismatches"]]},
        "delta_of_5_written_on_a_rebaseline_row": {
            "run": stamp(key_run),
            "nonzero_deltas_at_an_instrument_change_before_and_after":
                [base["nonzero_delta_rows_by_class"]["instrument_change"],
                 delta["nonzero_delta_rows_by_class"]["instrument_change"]]},
        "rebaseline_flag_set_where_the_source_did_not_change": {
            "run": stamp(grep_run),
            "flags_the_rule_does_not_reproduce_before_and_after":
                [base["rule_reproduction"]["flag_mismatches"], flagged["rule_reproduction"]["flag_mismatches"]]},
        "source_changed_without_a_flag": {
            "run": stamp(grep_run),
            "instrument_change_rows_before_and_after":
                [base["instrument_change"]["rows"], silent["instrument_change"]["rows"]],
            "flags_the_rule_does_not_reproduce_before_and_after":
                [base["rule_reproduction"]["flag_mismatches"], silent["rule_reproduction"]["flag_mismatches"]]},
    }


def transfer_log(task: dict) -> dict[str, list[dict]]:
    """The learner's defect log: one row per component and week, written with the feeder's rule."""
    table = {}
    for component in task["components"]:
        if len(component["counts"]) != task["weeks"] - component["first_week"] + 1:
            raise ValueError(f"transfer task: {component['name']} does not have one count per week")
        rows, previous = [], None
        for offset, count in enumerate(component["counts"]):
            week = component["first_week"] + offset
            source = [entry["source"] for entry in component["sources"] if entry["from_week"] <= week][-1]
            flag, delta = feeder_rule(previous, count, source)
            rows.append({"run": week, "count": count, "delta": delta, "has_key": True, "source": source,
                         "flag": flag, "seed": False})
            previous = {"count": count, "source": source}
        table[component["name"]] = rows
    return table


def transfer_levels(table: dict, records: list[dict], per_run: list[dict], week: int) -> dict:
    """Question 2 of the transfer task: each component and the total on both sides of the change of source."""
    levels = []
    for name in table:
        row = next(r for r in records if r["unit"] == name and r["run"] == week)
        levels.append({"component": name, "source_changed": row["class"] == "instrument_change",
                       "count_before": row["previous_count"], "count_after": row["count"], "step": row["step"],
                       "rebaseline": row["flag"], "delta_recorded": row["delta"]})
    return {
        "week_of_the_source_change": week,
        "per_component": levels,
        "total_the_week_before": per_run[week - 1]["total"],
        "total_that_week": per_run[week]["total"],
        "step_of_the_total": per_run[week]["total"] - per_run[week - 1]["total"],
        "sum_of_recorded_delta_that_week": per_run[week]["recorded_delta"],
        "ratio_of_totals": ratio(per_run[week]["total"], per_run[week - 1]["total"]),
    }


def transfer_task(task: dict, rule: dict) -> dict:
    """The 'transfer_task' section: the learner's log through the same classification as the observed one."""
    weeks, table = task["weeks"], transfer_log(task)
    records = classify(table)
    counters = measure(records)
    per_run = totals(records, weeks + 1)
    check_accounting("transfer task", table, records, counters, per_run)
    check("transfer task: the log rule reproduces itself",
          counters["rule_reproduction"]["delta_mismatches"] == 0 and counters["rule_reproduction"]["flag_mismatches"] == 0)
    change_weeks = sorted({r["run"] for r in records if r["class"] == "instrument_change"})
    if len(change_weeks) != 1:
        raise ValueError("transfer task: expected one week with a change of source")
    levels = transfer_levels(table, records, per_run, change_weeks[0])
    first_week = min(r["run"] for r in records)
    steps = series_steps(per_run, first_week)
    questions = []
    for question in task["two_sigma_questions"]:
        detail = rule_detail(steps[question["series"]], question["week"] - first_week - 1, rule)
        questions.append({"series": question["series"], "week": question["week"]} | detail)
    listed = lambda rows, keys: [{"component": r["unit"], "week": r["run"]} | {key: r[key] for key in keys}  # noqa: E731
                                 for r in sorted(rows, key=lambda r: (r["run"], list(table).index(r["unit"])))]
    first_total, last_total = per_run[first_week]["total"], per_run[weeks]["total"]
    growth = {key: sum(cell[key] for cell in per_run[first_week + 1:]) for key in PARTS}
    check("transfer task: growth of the total = later first counts + instrument change + same-instrument steps",
          last_total - first_total == sum(growth.values()))
    return {
        "note": task["note"],
        "unit": task["unit"],
        "rows": counters["rows"],
        "q1_log_rule": {
            "rows_flagged_rebaseline": listed([r for r in records if r["flag"]], ("previous_count", "count", "delta")),
            "rows_with_nonzero_delta": listed([r for r in records if r["delta"] != 0], ("delta", "class")),
            "nonzero_delta_rows_by_class": counters["nonzero_delta_rows_by_class"],
        },
        "q2_levels": levels,
        "q3_classification": {
            "two_definitions": counters["two_definitions"],
            "count_changes_by_class": counters["count_changes_by_class"],
            "same_instrument_changes": listed([r for r in records if r["class"] == "same_instrument" and r["step"]],
                                              ("previous_count", "count", "step")),
            "same_instrument_pairs": counters["same_instrument"]["pairs"],
            "total_by_week": [cell["total"] for cell in per_run[first_week:]],
            "growth_of_the_total": {"first_week_total": first_total, "last_week_total": last_total,
                                    "growth": last_total - first_total,
                                    "first_counts_of_components_added_later": growth["first_count"],
                                    "steps_at_the_source_change": growth["instrument_change"],
                                    "same_instrument_steps": growth["same_instrument"],
                                    "same_instrument_share_of_growth": ratio(growth["same_instrument"],
                                                                             last_total - first_total)},
        },
        "q4_two_sigma": questions,
        "q5": "no single answer: see the review brief",
    }


def observed_log(snapshot: dict) -> Log:
    """The snapshot's rows, classified and counted, with the accounting identities checked."""
    table = load_rows(snapshot)
    records = classify(table)
    log = Log(snapshot["runs"], table, records, measure(records), totals(records, len(snapshot["runs"])))
    check_accounting("observed", log.table, log.records, log.counters, log.per_run)
    return log


def recount_checks(log: Log, counts: dict) -> tuple[dict, dict]:
    """The group of cross-checks: extract.py's counts recounted, and the pinned rule against every row.

    Returns the rows by citation_source and by rebaseline flag, and sets the landmark runs of the log.
    """
    records, counters, runs, per_run = log.records, log.counters, log.runs, log.per_run
    by_source = {"key absent": sum(not r["has_key"] for r in records),
                 "null": sum(r["has_key"] and r["source"] is None for r in records)}
    for r in records:
        if r["source"] is not None:
            by_source[r["source"]] = by_source.get(r["source"], 0) + 1
    by_flag = {"key absent": sum(r["flag"] is None for r in records), "true": sum(r["flag"] is True for r in records),
               "false": sum(r["flag"] is False for r in records)}
    check("recount of rows, runs, artifacts and rows per run equals extract.py's counts",
          (counters["rows"], len(runs), counters["units"], [cell["rows"] for cell in per_run])
          == (counts["rows"], counts["runs"], counts["artifacts"], [run["rows"] for run in runs]))
    check("recount of citation_source, rebaseline, baseline and non-zero delta rows equals extract.py's counts",
          (by_source, by_flag, sum(r["seed"] for r in records), counters["rows_by_class"]["no_count"],
           counters["two_definitions"]["rows_with_nonzero_delta_citations"])
          == (counts["rows_by_citation_source"], counts["rows_by_rebaseline_flag"], counts["rows_flagged_baseline"],
              counts["rows_without_citation_count"], counts["rows_with_nonzero_delta_citations"]))
    check("the rows without a count are exactly the rows flagged baseline",
          all(r["seed"] == (r["class"] == "no_count") for r in records))
    reproduction = counters["rule_reproduction"]
    check("the pinned rule reproduces delta_citations in every row that has a count",
          reproduction["delta_mismatches"] == 0, str(reproduction))
    check("the pinned rule reproduces every recorded rebaseline flag",
          reproduction["flag_mismatches"] == 0 and reproduction["flagged_rows_not_at_an_instrument_change"] == 0)
    check("runs either carry the citation_source key on every row or on none",
          all(len({r["has_key"] for r in records if r["run"] == index}) == 1 for index in range(len(runs))))
    keyed = [index for index in range(len(runs)) if any(r["has_key"] for r in records if r["run"] == index)]
    log.key_run = keyed[0]
    check("once the citation_source key appears, every later run carries it",
          keyed == list(range(log.key_run, len(runs))))
    log.seed_runs = sum(any(r["seed"] for r in records if r["run"] == index) for index in range(len(runs)))
    log.first_feeder = next(index for index in range(len(runs)) if per_run[index]["rows_with_count"])
    return by_source, by_flag


def artifact_rows(log: Log, evolution: dict[str, dict]) -> list[dict]:
    """One entry per artifact: its count on each side of the first run that carries citation_source."""
    key_run, stamp = log.key_run, log.stamp
    per_artifact = []
    for name, rows in log.table.items():
        own = [r for r in log.records if r["unit"] == name]
        at = next((r for r in own if r["run"] == key_run), None)
        if at is None or not at["has_previous"]:
            raise ValueError(f"{name}: no row on both sides of the first run that carries citation_source")
        before = [r["count"] for r in own if r["run"] < key_run and r["count"] is not None]
        record = evolution[name]
        per_artifact.append({
            "artifact": name, "rows": len(rows), "first_row": stamp(rows[0]["run"]),
            "citation_source_from_that_run_on": at["source"], "rebaseline_flag_in_that_run": at["flag"],
            "count_before": at["previous_count"], "rows_before_with_a_count": len(before),
            "distinct_counts_before": len(set(before)), "count_after": at["count"], "step": at["step"],
            "delta_citations_recorded": at["delta"],
            "after_over_before": ratio(at["count"], at["previous_count"])["value"],
            "latest_count": own[-1]["count"],
            "same_instrument_changes": [{"run": stamp(r["run"]), "step": r["step"]}
                                        for r in own if r["class"] == "same_instrument" and r["step"]],
            "citation_paths": record["citation_paths"], "last_cited": record["last_cited"],
        })
        check("an artifact's latest row agrees with its evolution record at the pin",
              (own[-1]["count"], own[-1]["source"]) == (record["citation_count"], record["citation_source"]))
    return per_artifact


def source_section(snapshot: dict) -> dict:
    """The 'source' section: the pinned commit, the files read and the code lines quoted."""
    return {"repository": snapshot["source"]["repository"], "commit": snapshot["source"]["commit"],
            "files": [entry["path"] for key in ("files", "scripts", "evolution_records")
                      for entry in snapshot["source"][key]],
            "code_lines_quoted": [f"{q['path']}#L{q['first_line']}-L{q['last_line']}" if q["last_line"] != q["first_line"]
                                  else f"{q['path']}#L{q['first_line']}" for q in snapshot["code_quotes"]]}


def source_key_block(log: Log, by_source: dict, per_artifact: list[dict]) -> dict:
    """The 'citation_source_key' block of the observed section: where the key appears and what it holds."""
    runs, key_run, stamp = log.runs, log.key_run, log.stamp
    same_date = [index for index in range(len(runs)) if stamp(index)[:10] == stamp(key_run)[:10]]
    at_key = [r for r in log.records if r["run"] == key_run]
    return {
        "runs_without_the_key": key_run, "runs_with_the_key": len(runs) - key_run,
        "feeder_runs_without_the_key": key_run - log.seed_runs,
        "first_run_with_the_key": {
            "timestamp": stamp(key_run), "run_number": key_run + 1, "feeder_run_number": key_run + 1 - log.seed_runs,
            "rows": len(at_key), "rows_with_a_source_value": sum(r["source"] is not None for r in at_key),
            "rows_with_null": sum(r["source"] is None for r in at_key),
            "rows_flagged_rebaseline": sum(r["flag"] is True for r in at_key),
            "runs_on_that_utc_date": len(same_date), "position_among_them": same_date.index(key_run) + 1},
        "last_run_without_the_key": stamp(key_run - 1),
        "source_values": sorted(source for source in by_source if source not in ("key absent", "null")),
        "artifacts_with_a_source_value": sum(a["citation_source_from_that_run_on"] is not None for a in per_artifact),
        "artifacts_with_null_source": [{"artifact": a["artifact"], "citation_paths": a["citation_paths"],
                                        "count_before": a["count_before"], "count_after": a["count_after"]}
                                       for a in per_artifact if not a["rebaseline_flag_in_that_run"]],
    }


def observed_section(log: Log, counts: dict, by_source: dict, by_flag: dict, per_artifact: list[dict]) -> dict:
    """The 'observed' section: what the snapshot holds, recounted from its rows."""
    runs, records, counters, stamp = log.runs, log.records, log.counters, log.stamp
    return {
        "kind": "observed: counted from observed-input.json",
        "rows": counters["rows"], "runs": len(runs), "seed_runs": log.seed_runs,
        "feeder_runs": len(runs) - log.seed_runs, "run_dates_utc": counts["run_dates_utc"],
        "first_run": stamp(0), "first_feeder_run": stamp(log.first_feeder), "last_run": stamp(len(runs) - 1),
        "artifacts": counters["units"],
        "rows_per_run": {str(size): sum(run["rows"] == size for run in runs)
                         for size in sorted({run["rows"] for run in runs})},
        "rows_without_citation_count": counters["rows_by_class"]["no_count"],
        "rows_with_citation_count": counters["rule_reproduction"]["rows_with_a_count"],
        "rows_by_citation_source": by_source,
        "rows_by_rebaseline_flag": by_flag,
        "citation_source_key": source_key_block(log, by_source, per_artifact),
        "rebaseline_rows": {"rows": by_flag["true"], "runs": len({r["run"] for r in records if r["flag"]}),
                            "artifacts": len({r["unit"] for r in records if r["flag"]})},
        "latest_rows_agreeing_with_the_evolution_records": len(per_artifact),
    }


def feeder_rule_section(log: Log, cases: list[dict]) -> dict:
    """The 'feeder_rule' section: the pinned rule in words, on the observed rows and on the imaginary ones."""
    return {
        "kind": "the pinned rule, re-implemented; rule_cases are imaginary rows from scenarios.json",
        "statement": "rebaseline = the artifact has a previous row AND that row's citation_source differs from the "
                     "current one (a missing key reads as null); delta_citations = 0 if rebaseline, else the count "
                     "minus the previous row's count, taken as 0 when there is no previous row or it has no count; "
                     "citation_count is written as read in either case",
        "reproduction_on_observed_rows": log.counters["rule_reproduction"],
        "rule_cases": rule_cases(cases),
    }


def docstring_cross_check(per_artifact: list[dict], code_quotes: list[dict]) -> dict:
    """The producer's docstring gives a count before and after for one artifact: compare them with the record."""
    docstring = " ".join(line.strip() for quote in code_quotes
                         if quote["path"] == "scripts/evolution_metrics.py" and quote["first_line"] == 4
                         for line in quote["text"])
    alignment = next(a for a in per_artifact if a["artifact"] == DOCSTRING_ARTIFACT)
    return {
        "quoted_lines": "scripts/evolution_metrics.py#L4-L8", "text": docstring,
        "artifact": alignment["artifact"], "count_before": alignment["count_before"],
        "count_after": alignment["count_after"],
        "docstring_gives_the_same_two_numbers": f"alignment-policy said {alignment['count_before']} citations while "
                                                f"{alignment['count_after']} tracked files name it" in docstring}


def instrument_change_section(log: Log, per_artifact: list[dict], code_quotes: list[dict]) -> dict:
    """The 'instrument_change' section: the run where citation_source first appears, artifact by artifact."""
    key_run, per_run, counters = log.key_run, log.per_run, log.counters
    change_runs = sorted({r["run"] for r in log.records if r["class"] == "instrument_change"})
    flagged = [a for a in per_artifact if a["rebaseline_flag_in_that_run"]]
    rise = max(flagged, key=lambda a: (a["step"], a["artifact"]))
    fall = min(flagged, key=lambda a: (a["step"], a["artifact"]))
    brief = lambda a: {key: a[key] for key in ("artifact", "count_before", "count_after", "step")}  # noqa: E731
    defined = [a["after_over_before"] for a in flagged if a["after_over_before"] is not None]
    check("instrument-change rows are the flagged rows of the first run with the key",
          change_runs == [key_run] and len(flagged) == counters["instrument_change"]["rows"])
    check("steps of the flagged artifacts sum to the step of the total in that run",
          sum(a["step"] for a in flagged) == per_run[key_run]["total"] - per_run[key_run - 1]["total"]
          == counters["instrument_change"]["sum_of_steps"])
    return {
        "kind": "computed",
        "run": log.stamp(key_run),
        "counts": counters["instrument_change"],
        "sum_of_counts_before": sum(a["count_before"] for a in flagged),
        "sum_of_counts_after": sum(a["count_after"] for a in flagged),
        "after_over_before": ratio(sum(a["count_after"] for a in flagged), sum(a["count_before"] for a in flagged)),
        "largest_rise": brief(rise), "largest_fall": brief(fall),
        "after_over_before_per_artifact": {
            "smallest": min(defined), "largest": max(defined),
            "undefined_because_the_count_before_is_0": len(flagged) - len(defined)},
        "total_over_all_artifacts": {
            "before": per_run[key_run - 1]["total"], "after": per_run[key_run]["total"],
            "step": per_run[key_run]["total"] - per_run[key_run - 1]["total"],
            "after_over_before": ratio(per_run[key_run]["total"], per_run[key_run - 1]["total"]),
            "sum_of_delta_citations_in_that_run": per_run[key_run]["recorded_delta"]},
        "producer_docstring_cross_check": docstring_cross_check(per_artifact, code_quotes),
        "per_artifact": per_artifact,
    }


def remaining_changes(log: Log, evolution: dict[str, dict]) -> dict:
    """The count changes left once first counts and instrument changes are set aside, and what their records share."""
    stamp = log.stamp
    remaining = [r for r in log.records if r["class"] == "same_instrument" and r["step"]]
    remaining_runs = sorted({r["run"] for r in remaining})
    paths = {r["unit"]: evolution[r["unit"]]["citation_paths"] or [r["unit"]] for r in remaining}
    shared = [{"artifacts": [a, b], "shared_citation_paths": sorted(set(paths[a]) & set(paths[b]))}
              for a in paths for b in paths if a < b and set(paths[a]) & set(paths[b])]
    last_cited = sorted({evolution[r["unit"]]["last_cited"] for r in remaining} - {None})
    return {
        "rows": len(remaining), "runs": len(remaining_runs), "run": [stamp(index) for index in remaining_runs],
        "previous_run": [stamp(index - 1) for index in remaining_runs],
        "steps": [r["step"] for r in remaining], "sum_of_steps": sum(r["step"] for r in remaining),
        "artifacts": [{"artifact": r["unit"], "count_before": r["previous_count"], "count_after": r["count"],
                       "citation_paths_measured": paths[r["unit"]]} for r in remaining],
        "artifacts_sharing_a_citation_path": shared,
        "distinct_last_cited_in_their_evolution_records": last_cited,
        "last_cited_lies_between_the_previous_run_and_this_run":
            [stamp(index - 1) < moment <= stamp(index) for index in remaining_runs for moment in last_cited],
    }


def classification_section(log: Log, evolution: dict[str, dict]) -> dict:
    """The 'classification' section: every row against the artifact's previous row."""
    counters, same = log.counters, log.counters["same_instrument"]
    listed = [{"artifact": r["unit"], "run": log.stamp(r["run"]), "class": r["class"],
               "previous_count": r["previous_count"], "count": r["count"], "count_step": r["step"],
               "delta_citations": r["delta"], "rebaseline": r["flag"]}
              for r in sorted(log.records, key=lambda r: (r["run"], r["unit"])) if r["delta"] != 0 or r["step"]]
    check("the listed rows are the rows with a non-zero delta or a changed count",
          len(listed) == counters["two_definitions"]["either"])
    return {
        "kind": "computed",
        "definitions": {
            "no_count": "the row has no citation_count (a seed row)",
            "first_count": "the row has a count and no earlier row of the artifact has one: nothing to compare with",
            "instrument_change": "the previous row has a count and another citation_source (a missing key reads as null)",
            "same_instrument": "the previous row has a count and the same citation_source",
            "count changed": "the row's count differs from the previous row's count (defined only when that row has one)",
        },
        "rows_by_class": counters["rows_by_class"],
        "first_count": counters["first_count"],
        "instrument_change": counters["instrument_change"],
        "same_instrument": same | {"share_changed": ratio(same["count_changed"], same["pairs"])},
        "two_definitions": counters["two_definitions"],
        "nonzero_delta_rows_by_class": counters["nonzero_delta_rows_by_class"],
        "count_changes_by_class": counters["count_changes_by_class"],
        "row_pairs": counters["row_pairs"],
        "remaining_once_instrument_changes_and_first_counts_are_set_aside": remaining_changes(log, evolution),
        "rows_with_a_nonzero_delta_or_a_changed_count": listed,
    }


def total_series_section(log: Log) -> dict:
    """The 'total_series' section: the count summed over artifacts, and its growth split by cause."""
    per_run, first_feeder = log.per_run, log.first_feeder
    first_total, latest_total = per_run[first_feeder]["total"], per_run[-1]["total"]
    growth = {key: sum(cell[key] for cell in per_run[first_feeder + 1:]) for key in PARTS}
    whole = {key: sum(cell[key] for cell in per_run) for key in growth}
    check("growth of the total since the first feeder run = later first counts + instrument change + same-instrument steps",
          latest_total - first_total == sum(growth.values()))
    check("sum of every recorded delta_citations = first counts + same-instrument steps",
          sum(cell["recorded_delta"] for cell in per_run) == whole["first_count"] + whole["same_instrument"])
    check("per run, recorded delta_citations = first counts + same-instrument steps",
          all(cell["recorded_delta"] == cell["first_count"] + cell["same_instrument"] for cell in per_run))
    event_runs = [{"run": log.stamp(index), "run_number": index + 1, "rows": cell["rows"], "total": cell["total"],
                   "step_of_the_total": cell["total"] - (per_run[index - 1]["total"] if index else 0),
                   "sum_of_delta_citations": cell["recorded_delta"], "first_counts": cell["first_count"],
                   "steps_at_the_instrument_change": cell["instrument_change"],
                   "same_instrument_steps": cell["same_instrument"]}
                  for index, cell in enumerate(per_run)
                  if cell["recorded_delta"] or cell["first_count"] or cell["instrument_change"] or cell["same_instrument"]]
    return {
        "kind": "computed",
        "definition": "total = citation_count summed over the artifacts that have a count in the run",
        "first_feeder_total": first_total, "latest_total": latest_total, "growth": latest_total - first_total,
        "latest_over_first": ratio(latest_total, first_total),
        "growth_by_cause": {"first_counts_of_artifacts_added_later": growth["first_count"],
                            "steps_at_the_instrument_change": growth["instrument_change"],
                            "same_instrument_steps": growth["same_instrument"]},
        "same_instrument_share_of_growth": ratio(growth["same_instrument"], latest_total - first_total),
        "latest_total_by_cause": {"first_counts": whole["first_count"],
                                  "steps_at_the_instrument_change": whole["instrument_change"],
                                  "same_instrument_steps": whole["same_instrument"]},
        "sum_of_all_recorded_delta_citations": sum(cell["recorded_delta"] for cell in per_run),
        "runs_with_a_nonzero_part": event_runs,
        "total_by_run": [cell["total"] if cell["rows_with_count"] else None for cell in per_run],
    }


def seconds_between(earlier: str, later: str) -> int:
    """Whole seconds from one run timestamp to another."""
    moments = [datetime.strptime(stamp, "%Y-%m-%dT%H:%M:%SZ") for stamp in (earlier, later)]
    return int((moments[1] - moments[0]).total_seconds())


def run_gaps(log: Log) -> list[int]:
    """Seconds between each run after the first feeder run and the run before it: one gap per step of a series."""
    first = log.first_feeder
    gaps = [seconds_between(log.stamp(index - 1), log.stamp(index)) for index in range(first + 1, len(log.runs))]
    check("run gaps: one positive gap per step, and they sum to the time from the first feeder run to the last run",
          all(gap > 0 for gap in gaps) and len(gaps) == len(series_steps(log.per_run, first)["total"])
          and sum(gaps) == seconds_between(log.stamp(first), log.stamp(len(log.runs) - 1)))
    return gaps


def run_spacing(log: Log, gaps: list[int], spacing: dict) -> dict:
    """The 'run_spacing' block: how unevenly the feeder runs are spaced in time."""
    first, ordered, middle = log.first_feeder, sorted(gaps), len(gaps) // 2
    median = Fraction(ordered[middle - 1] + ordered[middle], 2) if len(gaps) % 2 == 0 else Fraction(ordered[middle])

    def gap_entry(gap: int) -> dict:
        position = gaps.index(gap)
        return {"seconds": gap, "days": statistic(Fraction(gap, DAY)),
                "from": log.stamp(first + position), "to": log.stamp(first + position + 1)}

    per_date: dict[str, int] = {}
    for index in range(first, len(log.runs)):
        per_date[log.stamp(index)[:10]] = per_date.get(log.stamp(index)[:10], 0) + 1
    short_hours, long_hours = spacing["short_gap_hours"], spacing["long_gap_hours"]
    return {
        "kind": "computed from the run timestamps; days are rounded to 4 decimals",
        "gaps_between_consecutive_feeder_runs": len(gaps),
        "shortest": gap_entry(ordered[0]),
        "longest": gap_entry(ordered[-1]),
        "median_days": statistic(median / DAY),
        "gaps_shorter_than": {"hours": short_hours, "gaps": sum(gap < short_hours * 3600 for gap in gaps)},
        "gaps_longer_than": {"hours": long_hours, "gaps": sum(gap > long_hours * 3600 for gap in gaps)},
        "utc_dates_with_more_than_one_feeder_run": {date: runs for date, runs in per_date.items() if runs > 1},
    }


def per_day_control(log: Log, gaps: list[int], rule: dict) -> dict:
    """Negative control for 'same flags': a short enough gap makes the per-day rule flag a step the per-run rule passes."""
    steps = series_steps(log.per_run, log.first_feeder)["total"]
    position = max(index for index, step in enumerate(steps) if step != 0)
    planted = gaps[:position] + [min(gaps)] + gaps[position + 1:]
    before, after = (rate_detail([Fraction(step * DAY, gap) for step, gap in zip(steps, some)], position, rule)
                     for some in (gaps, planted))
    check("negative control: the last non-zero step of the total, moved to the shortest observed gap, is flagged "
          "by the rule per day and not by the rule per run",
          not before["flagged"] and after["flagged"] and not rule_detail(steps, position, rule)["flagged"])
    return {"series": "total", "run": log.stamp(log.first_feeder + 1 + position), "step": steps[position],
            "gap_seconds_before_and_after": [gaps[position], planted[position]],
            "step_per_day_before_and_after": [before["step_per_day"], after["step_per_day"]],
            "flagged_before_and_after": [before["flagged"], after["flagged"]]}


def per_day(log: Log, gaps: list[int], rule: dict) -> dict:
    """The 'per_day' block: the same rule on each step divided by the days since the previous run."""
    first, out = log.first_feeder, {}
    for name, steps in series_steps(log.per_run, first).items():
        per_run_flags = [rule_detail(steps, position, rule)["flagged"] for position in range(len(steps))]
        even = [Fraction(step) for step in steps]
        check("rule per day: with equal gaps it flags exactly the steps that the rule per run flags",
              [rate_detail(even, position, rule)["flagged"] for position in range(len(steps))] == per_run_flags)
        rates = [Fraction(step * DAY, gap) for step, gap in zip(steps, gaps)]
        details = [rate_detail(rates, position, rule) for position in range(len(rates))]
        out[name] = {
            "flagged_steps": sum(d["flagged"] for d in details),
            "flagged_runs": [log.stamp(first + 1 + position) for position, d in enumerate(details) if d["flagged"]],
            "same_flags_as_the_rule_per_run": [d["flagged"] for d in details] == per_run_flags,
            "nonzero_step_details": [
                {"run": log.stamp(first + 1 + position), "step": steps[position],
                 "days_since_the_previous_run": statistic(Fraction(gaps[position], DAY))} | details[position]
                for position in range(len(steps)) if steps[position] != 0]}
    return {
        "kind": "computed; the same analysis rule, on steps per day",
        "definition": "each step divided by the time since the previous run, in days; a step per day is flagged when "
                      "it differs from the mean of all earlier steps per day by more than the rule's multiple of "
                      "their population standard deviation; days and steps per day are rounded to 4 decimals",
        "series": out,
        "negative_control": per_day_control(log, gaps, rule),
    }


def two_sigma_section(log: Log, rule: dict, spacing: dict) -> dict:
    """The 'two_sigma' section: the alarm rule on the three step series, per run and then per day."""
    series = two_sigma(log.per_run, log.first_feeder, rule, log.stamp)
    gaps = run_gaps(log)
    return {
        "kind": "computed with an analysis rule from scenarios.json; not a project alarm",
        "rule": f"a step is flagged when it differs from the mean of all earlier steps of its series by more than "
                f"{rule['multiplier']} population standard deviations of those steps; a step with fewer than "
                f"{rule['minimum_history_steps']} earlier steps is not tested",
        "steps_start_after": log.stamp(log.first_feeder),
        "series": series,
        "run_spacing": run_spacing(log, gaps, spacing),
        "per_day": per_day(log, gaps, rule),
    }


def analyze(snapshot: dict, scenarios: dict) -> dict:
    """One function per section of results.json; the calls are in the order in which the self-checks are recorded."""
    if scenarios["rounding"] != {f"{key}_decimals": value for key, value in DECIMALS.items()}:
        raise ValueError("scenarios.json rounding does not match analyze.py")
    rule = scenarios["two_sigma_rule"]
    evolution = {a["name"]: a["evolution_record"] for a in snapshot["artifacts"]}
    hand_computed_cases(rule)
    log = observed_log(snapshot)
    by_source, by_flag = recount_checks(log, snapshot["counts"])
    per_artifact = artifact_rows(log, evolution)
    change = instrument_change_section(log, per_artifact, snapshot["code_quotes"])
    classification = classification_section(log, evolution)
    series = total_series_section(log)
    sigma = two_sigma_section(log, rule, scenarios["run_spacing"])
    controls = negative_controls(log.table, snapshot, log.counters, log.key_run)
    transfer = transfer_task(scenarios["transfer_task"], rule)
    return {
        "module_id": snapshot["module_id"],
        "rounding": "ratios to 6 decimals, percentages to 2 decimals, means and standard deviations to 4 decimals; "
                    "'exact' is the unrounded fraction",
        "labels": snapshot["labels"],
        "source": source_section(snapshot),
        "observed": observed_section(log, snapshot["counts"], by_source, by_flag, per_artifact),
        "feeder_rule": feeder_rule_section(log, scenarios["rule_cases"]["cases"]),
        "instrument_change": change,
        "classification": classification,
        "total_series": series,
        "two_sigma": sigma,
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
