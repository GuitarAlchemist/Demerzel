#!/usr/bin/env python3
"""PSY-009 analysis: how concentrated the trigger log is, and what that does to a plan sized on the mean.

Reads observed-input.json (written by extract.py) and scenarios.json, never
the repository, and writes results.json. Every stored number is an integer
count or an exact fraction of integers rounded once (half up), so the file
is the same on every machine. The synthetic logs are drawn with
random.Random and the seeds stored in scenarios.json.

Run from the repository root:
    python -I scripts/streeling_fixtures/psychohistory/psy-009/analyze.py
    python -I scripts/streeling_fixtures/psychohistory/psy-009/analyze.py --check
"""

from __future__ import annotations

import argparse
import json
import math
import random
import sys
from collections import deque
from datetime import date, datetime, timedelta
from fractions import Fraction
from pathlib import Path
from typing import NamedTuple

# This program lives under scripts/ (CONTRIBUTING.md: no executable code outside scripts/); its data stays
# under state/streeling/fixtures/. FIXTURE_FILE is the path the program would have next to that data.
FIXTURE_FILE = (Path(__file__).resolve().parents[4]
                / "state/streeling/fixtures/psychohistory/psy-009" / Path(__file__).name)

HERE = FIXTURE_FILE.parent
PERCENTS = (50, 75, 90, 95, 99)  # the percentiles reported for the daily counts
ROUND: dict[str, int] = {}  # filled from scenarios.json: share, percent, gini, mean
CHECKS: dict[str, int] = {}  # self-check -> times evaluated

GINI_FORMULA = ("G = sum over i of (2 i - n - 1) x_i / (n T), with the n daily counts sorted in increasing order "
                "x_1 <= ... <= x_n and T their total")


def check(name: str, condition: bool, detail: str = "") -> None:
    """A self-check that can fail: abort instead of writing a wrong result."""
    if not condition:
        raise AssertionError(f"self-check failed: {name}" + (f" ({detail})" if detail else ""))
    CHECKS[name] = CHECKS.get(name, 0) + 1


def rounded(value: Fraction, decimals: int) -> float:
    """Exact rounding, half up, of a fraction of integers."""
    scale = 10 ** decimals
    return math.floor(Fraction(value) * scale + Fraction(1, 2)) / scale


def share(numerator: int, denominator: int) -> dict:
    value = Fraction(numerator, denominator)
    return {"exact": f"{numerator}/{denominator}", "value": rounded(value, ROUND["share"]),
            "percent": rounded(100 * value, ROUND["percent"])}


def amount(value: Fraction, kind: str = "mean") -> dict:
    value = Fraction(value)
    return {"exact": str(value), "value": rounded(value, ROUND[kind])}


# --- concentration measures -------------------------------------------------

def gini(counts: list[int]) -> Fraction:
    """Rank formula (GINI_FORMULA). 0 when all days are equal, (n - 1) / n when one day holds everything."""
    ordered, total = sorted(counts), sum(counts)
    return Fraction(sum((2 * rank - len(ordered) - 1) * value for rank, value in enumerate(ordered, 1)),
                    len(ordered) * total)


def gini_from_mean_difference(counts: list[int]) -> Fraction:
    """Second formula: the mean absolute difference between two days, divided by twice the mean."""
    return Fraction(sum(abs(a - b) for a in counts for b in counts), 2 * len(counts) * sum(counts))


def gini_from_lorenz_area(counts: list[int]) -> Fraction:
    """Third formula: 1 minus twice the area under the Lorenz polygon (trapezoids)."""
    cumulative = doubled = 0
    for value in sorted(counts):
        doubled += 2 * cumulative + value
        cumulative += value
    return 1 - Fraction(doubled, len(counts) * sum(counts))


def checked_gini(counts: list[int], label: str) -> Fraction:
    value = gini(counts)
    check("the three formulas for the Gini coefficient agree",
          value == gini_from_mean_difference(counts) == gini_from_lorenz_area(counts), label)
    return value


def quantile(counts: list[int], percent: int) -> int:
    """Nearest rank: the value at position ceil(percent * n / 100) of the counts sorted in increasing order."""
    ordered = sorted(counts)
    return ordered[max(-(-percent * len(ordered) // 100), 1) - 1]


def median(counts: list[int]) -> Fraction:
    """The middle value of the sorted counts; the mean of the two middle values when their number is even."""
    ordered, middle = sorted(counts), len(counts) // 2
    return Fraction(ordered[middle]) if len(ordered) % 2 else Fraction(ordered[middle - 1] + ordered[middle], 2)


def days_to_reach(counts: list[int], percent: int) -> tuple[int, int]:
    """Smallest number of busiest days that hold at least `percent` of the events, and what they hold."""
    total, running = sum(counts), 0
    for days, value in enumerate(sorted(counts, reverse=True), 1):
        running += value
        if 100 * running >= percent * total:
            return days, running
    raise ValueError("no events")


def concentration(counts: list[int], top_ks: list[int], half_percent: int, lorenz_percents: list[int],
                  label: str) -> dict:
    days, total = len(counts), sum(counts)
    descending = sorted(counts, reverse=True)
    ascending = descending[::-1]
    top = [{"busiest_days": k, "events": sum(descending[:k])} | share(sum(descending[:k]), total)
           for k in top_ks if k <= days]
    needed, held = days_to_reach(counts, half_percent)
    lorenz = []
    for percent in lorenz_percents:
        quiet = -(-percent * days // 100)
        lorenz.append({"quietest_days_percent": percent, "days": quiet, "events": sum(ascending[:quiet])}
                      | {"share": share(sum(ascending[:quiet]), total)}
                      | {"the_other_days": days - quiet, "their_events": sum(descending[:days - quiet])})
        check("the quietest days and the other days hold all the events",
              sum(ascending[:quiet]) + sum(descending[:days - quiet]) == total, label)
    active = [value for value in counts if value]
    gini_all, gini_active = checked_gini(counts, label), checked_gini(active, label + ", active days")
    check("adding empty days moves the Gini coefficient by the exact identity G_all = 1 - (m / n)(1 - G_active)",
          gini_all == 1 - Fraction(len(active), days) * (1 - gini_active), label)
    mean = Fraction(total, days)
    above = sum(value > mean for value in counts)
    check("shares of the busiest days never decrease and stay at or below 1",
          all(a["events"] <= b["events"] <= total for a, b in zip(top, top[1:])), label)
    return {
        "calendar_days": days, "events": total, "active_days": len(active), "empty_days": days - len(active),
        "busiest_days": top,
        "days_needed_for_half": {"half_percent": half_percent, "days": needed, "events": held} | share(held, total),
        "lorenz_points": lorenz,
        "gini_calendar_days": amount(gini_all, "gini"),
        "gini_active_days": amount(gini_active, "gini"),
        "gini_largest_possible_on_these_days": amount(Fraction(days - 1, days), "gini"),
        "mean_per_calendar_day": amount(mean),
        "mean_per_active_day": amount(Fraction(total, len(active))),
        "median_calendar_day": amount(median(counts)),
        "days_above_the_mean": above,
        "days_at_or_below_the_mean": days - above,
    }


def without_busiest(counts: list[int], dropped: int) -> dict:
    descending = sorted(counts, reverse=True)
    rest = descending[dropped:]
    full, mean = Fraction(sum(counts), len(counts)), Fraction(sum(rest), len(rest))
    return {"days_dropped": dropped, "events_dropped": sum(descending[:dropped]), "events_left": sum(rest),
            "days_left": len(rest), "mean": amount(mean),
            "mean_change_percent": rounded(100 * (mean - full) / full, ROUND["percent"]),
            "median": amount(median(rest))}


# --- capacity plans (an assumed handling rule) -------------------------------

def simulate(counts: list[int], capacity: int, tolerance: int, queue_limit: int | None = None) -> dict:
    """Handle at most `capacity` events a day, oldest first; the rest waits. See scenarios.json, capacity."""
    queue: deque[list[int]] = deque()  # [arrival day, events still waiting]
    waits: dict[int, int] = {}  # wait in days -> events handled after that wait
    backlog = largest = days_with_backlog = days_above_limit = 0
    largest_day = None
    for day, arrivals in enumerate(counts):
        if arrivals:
            queue.append([day, arrivals])
            backlog += arrivals
        room = min(capacity, backlog)
        backlog -= room
        while room:
            head = queue[0]
            taken = min(room, head[1])
            waits[day - head[0]] = waits.get(day - head[0], 0) + taken
            room -= taken
            head[1] -= taken
            if not head[1]:
                queue.popleft()
        if backlog > largest:
            largest, largest_day = backlog, day
        days_with_backlog += backlog > 0
        days_above_limit += queue_limit is not None and backlog > queue_limit
    last = len(counts) - 1
    handled_late = sum(events for wait, events in waits.items() if wait > tolerance)
    left_late = sum(waiting for arrival, waiting in queue if last - arrival >= tolerance)
    result = {
        "capacity_per_day": capacity,
        "capacity_offered": capacity * len(counts),
        "handled": sum(waits.values()),
        "handled_on_arrival_day": waits.get(0, 0),
        "handled_later_within_tolerance": sum(events for wait, events in waits.items() if 0 < wait <= tolerance),
        "handled_late": handled_late,
        "left_at_end": backlog,
        "left_at_end_already_late": left_late,
        "left_at_end_undetermined": backlog - left_late,
        "late_events": handled_late + left_late,
        "longest_wait_of_a_handled_event_days": max(waits) if waits else None,
        "oldest_event_left_at_end_age_days": last - queue[0][0] if queue else None,
        "largest_backlog_at_end_of_day": largest,
        "largest_backlog_day_index_from_0": largest_day,
        "days_ending_with_a_backlog": days_with_backlog,
    }
    if queue_limit is not None:
        result["days_ending_above_the_queue_limit"] = days_above_limit
    check("capacity accounting: handled + left = arrivals; on the day + later + late = handled",
          result["handled"] + backlog == sum(counts)
          and result["handled_on_arrival_day"] + result["handled_later_within_tolerance"] + handled_late == result["handled"]
          and result["handled"] <= result["capacity_offered"])
    return result


def smallest_capacity(counts: list[int], tolerance: int) -> int:
    """Smallest whole daily capacity with no late event (bisection: more capacity never delays an event)."""
    low, high = 1, max(counts)
    while low < high:
        middle = (low + high) // 2
        if simulate(counts, middle, tolerance)["late_events"] == 0:
            high = middle
        else:
            low = middle + 1
    return low


def plan_capacity(plan: dict, counts: list[int]) -> int:
    if plan["name"] == "mean_rounded_up":
        return -(-sum(counts) // len(counts))
    if plan["name"] == "peak":
        return max(counts)
    return quantile(counts, plan["quantile_percent"])


def run_plans(counts: list[int], plans: list[dict], tolerance: int, queue_limit: int | None, first: date | None) -> list:
    rows = []
    mean = Fraction(sum(counts), len(counts))
    for plan in plans:
        capacity = plan_capacity(plan, counts)
        row = {"plan": plan["name"], "rule": plan["rule"]} | simulate(counts, capacity, tolerance, queue_limit)
        row["capacity_as_a_multiple_of_the_mean"] = rounded(capacity / mean, ROUND["mean"])
        row["capacity_used"] = share(row["handled"], row["capacity_offered"])
        if first is not None:
            index = row["largest_backlog_day_index_from_0"]
            row["largest_backlog_day"] = None if index is None else (first + timedelta(days=index)).isoformat()
        rows.append(row)
    return rows


def capacity_hand_case(case: dict) -> dict:
    result = simulate(case["counts"], case["capacity"], case["wait_tolerance_days"])
    for key, expected in case["expected"].items():
        check("the capacity rule reproduces the case worked by hand", result[key] == expected, f"{key}: {result[key]}")
    return {"counts": case["counts"], "capacity": case["capacity"],
            "wait_tolerance_days": case["wait_tolerance_days"]} | {key: result[key] for key in case["expected"]}


# --- synthetic control --------------------------------------------------------

def synthetic_logs(days: int, events: int, logs: int, seed: int):
    rng = random.Random(seed)
    for _ in range(logs):
        counts = [0] * days
        for _ in range(events):
            counts[min(days - 1, int(rng.random() * days))] += 1
        yield counts


def summary(values: list, permille: list[int], kind: str = "mean") -> dict:
    ordered = sorted(values)

    def at(mark: int):
        return ordered[max(-(-mark * len(ordered) // 1000), 1) - 1]

    def shown(value):
        return value if isinstance(value, int) else rounded(value, ROUND[kind])

    picks = {"min": ordered[0]}
    picks[f"p{permille[0] / 10:g}".replace(".", "_")] = at(permille[0])
    picks["median"] = at(500)
    picks[f"p{permille[1] / 10:g}".replace(".", "_")] = at(permille[1])
    picks["max"] = ordered[-1]
    out = {key: shown(value) for key, value in picks.items()}
    out["mean"] = rounded(Fraction(sum(ordered), len(ordered)), ROUND[kind])
    return out


def log_measures(counts: list[int], tolerance: int, with_capacity: bool) -> dict:
    days, total = len(counts), sum(counts)
    descending = sorted(counts, reverse=True)
    full, rest = Fraction(total, days), Fraction(total - descending[0], days - 1)
    row = {
        "busiest_day_events": descending[0],
        "top_4_events": sum(descending[:4]),
        "top_10_events": sum(descending[:10]),
        "days_needed_for_half": days_to_reach(counts, 50)[0],
        "events_on_the_quietest_half_of_days": sum(descending[days - -(-50 * days // 100):]),
        "gini_calendar_days": gini(counts),
        "median_calendar_day": median(counts),
        "empty_days": counts.count(0),
        "mean_change_percent_without_the_busiest_day": 100 * (rest - full) / full,
    }
    if with_capacity:
        mean_plan = simulate(counts, -(-total // days), tolerance)
        p95 = quantile(counts, 95)
        row |= {
            "smallest_capacity_without_a_late_event": smallest_capacity(counts, tolerance),
            "p95_of_daily_counts": p95,
            "late_events_with_capacity_p95": simulate(counts, p95, tolerance)["late_events"],
            "late_events_with_capacity_mean_rounded_up": mean_plan["late_events"],
            "left_at_end_with_capacity_mean_rounded_up": mean_plan["left_at_end"],
            "handled_on_arrival_day_with_capacity_mean_rounded_up": mean_plan["handled_on_arrival_day"],
            "longest_wait_days_with_capacity_mean_rounded_up": mean_plan["longest_wait_of_a_handled_event_days"],
        }
    return row


KIND_OF = {"gini_calendar_days": "gini", "mean_change_percent_without_the_busiest_day": "percent"}
# Comparisons with the observed log: +1 means "at least as large", -1 "at most as large".
AS_CONCENTRATED = {"busiest_day_events": 1, "top_4_events": 1, "top_10_events": 1, "gini_calendar_days": 1,
                   "empty_days": 1, "smallest_capacity_without_a_late_event": 1,
                   "days_needed_for_half": -1, "events_on_the_quietest_half_of_days": -1, "median_calendar_day": -1}


def at_least_as_concentrated(rows: list[dict], observed: dict) -> dict:
    return {key: sum(sign * row[key] >= sign * observed[key] for row in rows) for key, sign in AS_CONCENTRATED.items()}


def poisson_control(counts: list[int], config: dict, tolerance: int) -> tuple[dict, dict, list[dict]]:
    """The section of results.json, the summaries over the synthetic logs, and the measures of each log."""
    days, events, logs, permille = len(counts), sum(counts), config["logs"], config["summary_permille"]
    rows = []
    for log in synthetic_logs(days, events, logs, config["seed"]):
        check("every synthetic log has the observed number of events and days",
              sum(log) == events and len(log) == days)
        rows.append(log_measures(log, tolerance, with_capacity=True))
    check("the synthetic batch has the stated number of logs", len(rows) == logs, str(len(rows)))
    summaries = {key: summary([row[key] for row in rows], permille, KIND_OF.get(key, "mean")) for key in rows[0]}
    for key in ("busiest_day_events", "top_4_events", "top_10_events", "events_on_the_quietest_half_of_days"):
        held = [row[key] for row in rows]
        summaries[key]["as_percent_of_all_events"] = {
            "min": rounded(Fraction(100 * min(held), events), ROUND["percent"]),
            "mean": rounded(Fraction(100 * sum(held), events * logs), ROUND["percent"]),
            "max": rounded(Fraction(100 * max(held), events), ROUND["percent"])}

    expected_empty = days * Fraction(days - 1, days) ** events
    mean_empty = Fraction(sum(row["empty_days"] for row in rows), logs)
    limit = Fraction(str(config["empty_days_tolerance"]["absolute"]))
    check("known answer: the batch mean of empty days is the exact expectation n ((n - 1) / n) ** T, within tolerance",
          abs(mean_empty - expected_empty) <= limit, f"{float(mean_empty):.4f} against {float(expected_empty):.4f}")

    replication = [log_measures(log, tolerance, with_capacity=False)
                   for log in synthetic_logs(days, events, logs, config["replication_seed"])]
    tolerances = config["replication_tolerance"]
    compared = {}
    for name, key, scale, kind in (("gini_calendar_days", "gini_calendar_days", Fraction(1), "gini"),
                                   ("top_4_share_percent", "top_4_events", Fraction(100, events), "percent")):
        first = Fraction(sum(row[key] for row in rows), logs) * scale
        second = Fraction(sum(row[key] for row in replication), logs) * scale
        check("the replication batch (another seed) agrees with the main batch within the stated tolerance",
              abs(first - second) <= Fraction(str(tolerances[name])), name)
        compared[name] = {"main_batch_mean": rounded(first, ROUND[kind]), "replication_batch_mean": rounded(second, ROUND[kind]),
                          "tolerance": tolerances[name]}

    observed = log_measures(counts, tolerance, with_capacity=True)
    exceed = at_least_as_concentrated(rows, observed)
    planted = at_least_as_concentrated(rows + [observed], observed)
    check("negative control: the observed log, added to the batch, is counted once by every comparison",
          all(planted[key] == exceed[key] + 1 for key in exceed))
    return {
        "kind": "synthetic: logs with the observed total and number of days, each event on a day drawn uniformly at random",
        "note": config["note"],
        "generator": config["generator"],
        "logs": logs, "seed": config["seed"], "days": days, "events_per_log": events,
        "summary_keys": f"min, the {permille[0] / 10:g}th and {permille[1] / 10:g}th percentiles (nearest rank), "
                        "the median (nearest rank), max and mean over the logs",
        "summaries": summaries,
        "observed_log_with_the_same_measures": {
            key: (value if isinstance(value, int) else rounded(value, ROUND[KIND_OF.get(key, "mean")]))
            for key, value in observed.items()},
        "synthetic_logs_at_least_as_concentrated_as_the_observed_log": exceed,
        "comparison_directions": "counts of synthetic logs whose value is >= the observed one, except "
                                 "days_needed_for_half, events_on_the_quietest_half_of_days and median_calendar_day (<=)",
        "known_answer_empty_days": {
            "exact_expectation": rounded(expected_empty, 4), "batch_mean": rounded(mean_empty, 4),
            "tolerance": config["empty_days_tolerance"]["absolute"],
            "formula": "days * ((days - 1) / days) ** events"},
        "replication": {"seed": config["replication_seed"], "logs": logs} | compared,
        "negative_control": {
            "what": "the same comparisons after adding the observed log to the batch: each count must rise by exactly 1",
            "counts_with_the_observed_log_added": planted},
    }, summaries, rows


def classify_candidates(candidates: dict, summaries: dict, observed: dict, events: int) -> dict:
    out = {}
    for name, log in candidates.items():
        row = {"top_4_events": log["top_4_events"], "top_4_share": share(log["top_4_events"], events),
               "gini_calendar_days": log["gini_calendar_days"]}
        verdicts = {}
        for key in ("top_4_events", "gini_calendar_days"):
            value, s = Fraction(str(log[key])), summaries[key]
            low, high = [Fraction(str(s[k])) for k in s if k.startswith("p")]
            if value > Fraction(str(s["max"])):
                verdicts[key] = "above every synthetic log"
            elif value < Fraction(str(s["min"])):
                verdicts[key] = "below every synthetic log"
            elif low <= value <= high:
                verdicts[key] = "inside the central 95% of the synthetic logs"
            else:
                verdicts[key] = "inside the range of the synthetic logs, outside their central 95%"
        row["against_the_synthetic_logs"] = verdicts
        row["against_the_observed_log"] = {
            "top_4_events_observed": observed["top_4_events"],
            "top_4_events_as_percent_of_observed": rounded(Fraction(100 * log["top_4_events"], observed["top_4_events"]),
                                                           ROUND["percent"]),
            "gini_observed": rounded(observed["gini_calendar_days"], ROUND["gini"]),
            "less_concentrated_than_observed_on_both": log["top_4_events"] < observed["top_4_events"]
            and Fraction(str(log["gini_calendar_days"])) < observed["gini_calendar_days"]}
        out[name] = row
    return out


# --- the observed log ----------------------------------------------------------

def daily_counts(stamps: list[datetime], offset_hours: int = 0) -> tuple[date, list[int]]:
    """Events per calendar day, the day boundary moved by `offset_hours` from UTC midnight."""
    per_day: dict[date, int] = {}
    for stamp in stamps:
        day = (stamp + timedelta(hours=offset_hours)).date()
        per_day[day] = per_day.get(day, 0) + 1
    first, last = min(per_day), max(per_day)
    return first, [per_day.get(first + timedelta(days=offset), 0) for offset in range((last - first).days + 1)]


def consecutive_runs(days: list[date], events_on: dict[date, int], gap: int = 1) -> list[dict]:
    """Group the days: a day at most `gap` days after the previous one stays in the same run."""
    runs: list[list[date]] = []
    for day in sorted(days):
        if runs and day - runs[-1][-1] <= timedelta(days=gap):
            runs[-1].append(day)
        else:
            runs.append([day])
    return [{"days": [day.isoformat() for day in run], "events": sum(events_on[day] for day in run)} for run in runs]


def episodes_of(days: list[date], events_on: dict[date, int], rule: dict) -> dict:
    """PSY-008's episodes (burst days at most `gap_days` apart) and the pair of busiest days inside each."""
    def apart(first: str, last: str) -> int:
        return (date.fromisoformat(last) - date.fromisoformat(first)).days

    burst = [day for day, events in events_on.items() if events >= rule["burst_day_from"]]
    episodes = [{"first_burst_day": run["days"][0], "last_burst_day": run["days"][-1], "burst_days": len(run["days"]),
                 "events_on_burst_days": run["events"],
                 "busiest_days_inside": [day.isoformat() for day in sorted(days)
                                         if run["days"][0] <= day.isoformat() <= run["days"][-1]]}
                for run in consecutive_runs(burst, events_on, rule["gap_days"])]
    pairs = consecutive_runs(days, events_on)
    check("each pair of busiest days lies inside one episode of burst days, the two pairs inside different episodes, "
          "and the episodes hold every burst day once",
          sum(episode["burst_days"] for episode in episodes) == len(burst) and len(pairs) == 2
          and [episode["busiest_days_inside"] for episode in episodes if episode["busiest_days_inside"]]
          == [pair["days"] for pair in pairs])
    return {"rule": rule["note"], "burst_day_from": rule["burst_day_from"], "gap_days": rule["gap_days"],
            "burst_days": len(burst), "episodes": episodes,
            "days_between_the_episodes": [apart(a["last_burst_day"], b["first_burst_day"])
                                          for a, b in zip(episodes, episodes[1:])],
            "days_between_the_two_pairs_of_busiest_days": {
                "from": pairs[0]["days"][-1], "to": pairs[1]["days"][0],
                "days": apart(pairs[0]["days"][-1], pairs[1]["days"][0])}}


def busiest_window(counts: list[int], width: int, first: date) -> dict:
    sums = [sum(counts[start:start + width]) for start in range(len(counts) - width + 1)]
    best = max(sums)
    start = sums.index(best)
    return {"window_days": width, "first_day": (first + timedelta(days=start)).isoformat(),
            "last_day": (first + timedelta(days=start + width - 1)).isoformat(), "events": best} | share(best, sum(counts))


def hand_cases(cases: list[dict]) -> list[dict]:
    out = []
    for case in cases:
        counts = case["counts"]
        value = checked_gini(counts, case["name"])
        top = Fraction(max(counts), sum(counts))
        check("hand-computed case: the Gini coefficient and the share of the busiest day are the values worked by hand",
              value == Fraction(case["gini"]) and top == Fraction(case["top_1_share"]), case["name"])
        out.append({"name": case["name"], "counts": counts, "gini": amount(value, "gini"),
                    "share_of_the_busiest_day": str(top)})
    for days in (2, 5, 119):
        check("all days equal gives a Gini coefficient of 0", checked_gini([7] * days, "equal") == 0, str(days))
        check("everything on one day of n gives a Gini coefficient of (n - 1) / n",
              checked_gini([0] * (days - 1) + [42], "one day") == Fraction(days - 1, days), str(days))
    return out


def transfer_task(task: dict) -> dict:
    counts = task["daily_counts"]
    measures = concentration(counts, task["top_k"], task["half_share_percent"], task["lorenz_day_percents"], "transfer task")
    tolerance = task["wait_tolerance_days"]
    plans = run_plans(counts, task["plans"], tolerance, None, None)
    smallest = smallest_capacity(counts, tolerance)
    check("transfer task: one unit of capacity less than the smallest sufficient one leaves a late ticket",
          simulate(counts, smallest, tolerance)["late_events"] == 0
          and simulate(counts, smallest - 1, tolerance)["late_events"] > 0)
    return {
        "kind": "synthetic: a hypothetical support desk, not Streeling data",
        "note": task["note"], "unit": task["unit"], "daily_counts": counts,
        "sorted_in_increasing_order": sorted(counts),
        "concentration": measures,
        "without_the_busiest_days": [without_busiest(counts, dropped) for dropped in task["drop_busiest_days"]],
        "capacity": {"handling_rule": "the rule of scenarios.json, capacity.handling_rule, with tickets for events",
                     "wait_tolerance_days": tolerance, "plans": plans,
                     "smallest_capacity_without_a_late_ticket": smallest,
                     "late_tickets_with_one_unit_less": simulate(counts, smallest - 1, tolerance)["late_events"],
                     "with_that_capacity": simulate(counts, smallest, tolerance)},
    }


# --- the sections of results.json, in the order in which analyze() calls them ---

class Log(NamedTuple):
    """The observed log, recounted from the event rows of the snapshot."""
    stamps: list[datetime]
    types: list[str]
    first: date
    counts: list[int]
    calendar: list[date]
    by_type: dict[str, int]

    @property
    def days(self) -> int:
        return len(self.counts)

    @property
    def total(self) -> int:
        return len(self.stamps)


def read_log(snapshot: dict) -> Log:
    """Recount everything from the event rows, through a second code path."""
    recorded, design = snapshot["counts"], snapshot["design"]
    events = [row.split(" ") for row in snapshot["events"]]
    stamps = [datetime.strptime(stamp, "%Y-%m-%dT%H:%M:%SZ") for stamp, _ in events]
    types = [kind for _, kind in events]
    first, counts = daily_counts(stamps)
    days, total = len(counts), len(events)
    calendar = [first + timedelta(days=offset) for offset in range(days)]
    by_type = {kind: types.count(kind) for kind in sorted(set(types))}
    check("recount from the event rows equals the counts made by extract.py",
          counts == snapshot["daily_counts"]["values"] and first.isoformat() == snapshot["daily_counts"]["first_day"]
          and total == recorded["events"] == snapshot["source"]["files"] and days == recorded["calendar_days"]
          and sum(value > 0 for value in counts) == recorded["active_days"]
          and counts.count(0) == recorded["empty_days"] and by_type == recorded["by_type"]
          and calendar[-1].isoformat() == recorded["last_day"])
    check("the two design files state the number of orphaned triggers that the folder holds",
          design["orphaned_triggers_stated_by_the_skill_file"] == design["orphans_stated_by_the_workflow_file"] == total)
    return Log(stamps, types, first, counts, calendar, by_type)


def header(snapshot: dict) -> dict:
    """The first keys of results.json: what was read and how the numbers are rounded."""
    source = snapshot["source"]
    return {
        "schema_version": "0.1.0",
        "module_id": snapshot["module_id"],
        "source": {"repository": source["repository"], "commit": source["commit"],
                   "folder": source["folder"], "files": source["files"],
                   "manifest_sha256": source["manifest_sha256"]},
        "rounding": {"rule": "exact fractions of integers, rounded half up once when written",
                     "share_decimals": ROUND["share"], "percent_decimals": ROUND["percent"],
                     "gini_decimals": ROUND["gini"], "mean_decimals": ROUND["mean"]},
    }


def observed_section(log: Log, snapshot: dict, scenarios: dict) -> dict:
    measures = concentration(log.counts, scenarios["top_k"], scenarios["half_share_percent"],
                             scenarios["lorenz_day_percents"], "observed log")
    check("mean times days = events; days above the mean + the others = days",
          Fraction(log.total, log.days) * log.days == log.total
          and measures["days_above_the_mean"] + measures["days_at_or_below_the_mean"] == log.days)
    return {
        "kind": "computed from the observed event rows",
        "day_rule": "the day of an event is the UTC date of its JSON timestamp",
        "first_day": log.first.isoformat(), "last_day": log.calendar[-1].isoformat(),
        "events_by_type": log.by_type,
        "design_stated_by_the_repository": snapshot["design"],
        "distinct_type_repo_ref_combinations": snapshot["counts"]["distinct_type_repo_ref_combinations"],
    } | measures


def rank_days(log: Log, top_ks: list[int]) -> tuple[list[dict], list[date], dict[str, int]]:
    """The busiest days in order, the dates of the four busiest, and the number of days at each count."""
    counts = log.counts
    ranking = sorted(range(log.days), key=lambda index: (-counts[index], index))
    ranked = [{"rank": rank, "day": log.calendar[index].isoformat(), "events": counts[index]}
              for rank, index in enumerate(ranking[:max(top_ks)], 1)]
    check("the fourth and fifth busiest days are not tied, so 'the four busiest days' names four dates",
          counts[ranking[3]] > counts[ranking[4]])
    top_four = [log.calendar[index] for index in ranking[:4]]
    days_by_count = {str(value): counts.count(value) for value in sorted(set(counts))}
    check("the table of days by count covers every day and every event",
          sum(days_by_count.values()) == log.days
          and sum(int(value) * n for value, n in days_by_count.items()) == log.total)
    return ranked, top_four, days_by_count


def lorenz_curve(log: Log) -> list[int]:
    """Cumulative events from the quietest day to the busiest."""
    curve, running = [], 0
    for value in sorted(log.counts):
        running += value
        curve.append(running)
    check("the Lorenz curve ends at the total", curve[-1] == log.total and len(curve) == log.days)
    return curve


def mean_and_median_section(log: Log, observed: dict, days_by_count: dict, scenarios: dict) -> dict:
    """Mean and median: what one day, a month or a date of reading does to them."""
    months: dict[str, list[int]] = {}
    for day, value in zip(log.calendar, log.counts):
        months.setdefault(day.isoformat()[:7], []).append(value)
    by_month = [{"month": month, "days": len(values), "events": sum(values),
                 "mean": amount(Fraction(sum(values), len(values))), "median": amount(median(values))}
                for month, values in months.items()]
    check("the months partition the log", sum(row["days"] for row in by_month) == log.days
          and sum(row["events"] for row in by_month) == log.total)
    to_date = []
    for text in scenarios["checkpoints"]["dates"]:
        seen = [value for day, value in zip(log.calendar, log.counts) if day <= date.fromisoformat(text)]
        to_date.append({"read_on": text, "days": len(seen), "events": sum(seen),
                        "mean_to_date": amount(Fraction(sum(seen), len(seen))), "median_to_date": amount(median(seen)),
                        "mean_rounded_up": -(-sum(seen) // len(seen)),
                        "busiest_day_to_date": max(seen),
                        "percentiles_to_date": {f"p{percent}": quantile(seen, percent) for percent in PERCENTS}})
    check("the last checkpoint is the whole log",
          to_date[-1]["days"] == log.days and to_date[-1]["events"] == log.total
          and to_date[-1]["mean_to_date"] == observed["mean_per_calendar_day"])
    whole = {f"p{percent}": quantile(log.counts, percent) for percent in PERCENTS}
    check("percentiles read to date: those of the last reading are those of the whole log, and at every reading "
          "they do not decrease with the level and stay at or below the busiest day read",
          to_date[-1]["percentiles_to_date"] == whole
          and all(list(row["percentiles_to_date"].values()) == sorted(row["percentiles_to_date"].values())
                  and row["percentiles_to_date"]["p99"] <= row["busiest_day_to_date"] for row in to_date))
    check("the median is the middle value, or the mean of the two middle values when their number is even; the "
          "nearest-rank 50th percentile then takes the lower of the two",
          median([1, 2, 9]) == 2 and median([1, 2, 4, 9]) == 3 and quantile([1, 2, 4, 9], 50) == 2)
    means = [Fraction(row["mean_to_date"]["exact"]) for row in to_date]
    return {
        "kind": "computed",
        "mean_per_calendar_day": observed["mean_per_calendar_day"],
        "median_calendar_day": observed["median_calendar_day"],
        "most_frequent_daily_count": {
            "events": int(max(days_by_count, key=lambda value: (days_by_count[value], -int(value)))),
            "days": max(days_by_count.values())},
        "quantiles_nearest_rank": whole,
        "quantile_rule": scenarios["quantile_rule"],
        "median_rule": scenarios["median_rule"],
        "without_the_busiest_days": [without_busiest(log.counts, dropped)
                                     for dropped in scenarios["drop_busiest_days"]],
        "by_month": by_month,
        "read_to_date": to_date,
        "mean_to_date_range": {"lowest": rounded(min(means), ROUND["mean"]),
                               "highest": rounded(max(means), ROUND["mean"]),
                               "highest_over_lowest": rounded(max(means) / min(means), ROUND["mean"])},
    }


def day_boundary_section(log: Log, scenarios: dict) -> dict:
    """Robustness: the same measures when the day starts at another hour."""
    offsets, half = scenarios["day_boundary_offsets_hours"], scenarios["half_share_percent"]
    rows = []
    for offset in range(offsets["from"], offsets["to"] + 1):
        _, shifted = daily_counts(log.stamps, offset)
        check("moving the day boundary keeps every event", sum(shifted) == log.total)
        if offset == 0:
            check("a day boundary moved by 0 hours reproduces the UTC daily counts", shifted == log.counts)
        descending = sorted(shifted, reverse=True)
        rows.append({"offset_hours": offset, "calendar_days": len(shifted),
                     "active_days": sum(value > 0 for value in shifted), "busiest_day_events": descending[0],
                     "top_4_events": sum(descending[:4]),
                     "top_4_share_percent": rounded(Fraction(100 * sum(descending[:4]), log.total), ROUND["percent"]),
                     "days_needed_for_half": days_to_reach(shifted, half)[0],
                     "gini_calendar_days": rounded(gini(shifted), ROUND["gini"]),
                     "median_calendar_day": rounded(median(shifted), ROUND["mean"])})
    lowest = min(rows, key=lambda row: (row["top_4_events"], row["offset_hours"]))
    highest = max(rows, key=lambda row: (row["top_4_events"], -row["offset_hours"]))
    day_ahead = daily_counts(log.stamps, 24)
    check("negative control: a boundary moved by a whole day shifts the dates and changes no count",
          day_ahead[1] == log.counts and day_ahead[0] == log.first + timedelta(days=1))
    return {
        "note": offsets["note"], "rows": rows,
        "top_4_share_percent_lowest": {"offset_hours": lowest["offset_hours"],
                                       "value": lowest["top_4_share_percent"], "events": lowest["top_4_events"]},
        "top_4_share_percent_highest": {"offset_hours": highest["offset_hours"],
                                        "value": highest["top_4_share_percent"], "events": highest["top_4_events"]},
        "offsets_where_the_four_busiest_days_hold_at_least_half":
            sum(2 * row["top_4_events"] >= log.total for row in rows),
        "offsets": len(rows),
        "gini_lowest": min(row["gini_calendar_days"] for row in rows),
        "gini_highest": max(row["gini_calendar_days"] for row in rows),
    }


def type_subsets_section(log: Log, scenarios: dict) -> dict:
    """Robustness: the same measures on the events of one group of types, over the same calendar days."""
    subsets = scenarios["type_subsets"]
    rows = {}
    for name in ("without_push", "push_only"):
        per_day: dict[date, int] = {}
        for stamp, kind in zip(log.stamps, log.types):
            if kind in subsets[name]:
                per_day[stamp.date()] = per_day.get(stamp.date(), 0) + 1
        subset_counts = [per_day.get(day, 0) for day in log.calendar]
        rows[name] = {"types": subsets[name]} | concentration(
            subset_counts, [1, 4, 10], scenarios["half_share_percent"], [50], name)
    check("the two type subsets are disjoint and hold every event between them",
          not set(subsets["without_push"]) & set(subsets["push_only"])
          and rows["without_push"]["events"] + rows["push_only"]["events"] == log.total
          and set(subsets["without_push"]) | set(subsets["push_only"]) == set(log.by_type))
    return {"note": subsets["note"]} | rows


def busiest_days_section(log: Log, ranking: tuple, observed: dict, scenarios: dict) -> dict:
    ranked, top_four, days_by_count = ranking
    by_type = {kind: sum(1 for stamp, k in zip(log.stamps, log.types) if k == kind and stamp.date() in top_four)
               for kind in log.by_type}
    check("the events of the four busiest days, split by type, add up",
          sum(by_type.values()) == observed["busiest_days"][scenarios["top_k"].index(4)]["events"])
    return {
        "kind": "computed",
        "ranked": ranked,
        "the_four_busiest_days_as_runs_of_consecutive_dates":
            consecutive_runs(top_four, dict(zip(log.calendar, log.counts))),
        "events_of_the_four_busiest_days_by_type": by_type,
        "episodes_of_burst_days": episodes_of(top_four, dict(zip(log.calendar, log.counts)), scenarios["episodes"]),
        "busiest_windows_of_consecutive_days": [busiest_window(log.counts, width, log.first)
                                                for width in scenarios["window_days"]],
        "days_by_count": days_by_count,
    }


def deduplicated_section(log: Log, snapshot: dict, observed: dict, half: int) -> dict:
    """The design's own deduplication rule, with an assumed wake once a day."""
    recorded = snapshot["counts"]
    check("every event has the same repo and ref, so the type is the only part of the deduplication key that varies",
          recorded["distinct_repos"] == 1 and recorded["distinct_refs"] == 1
          and recorded["distinct_type_repo_ref_combinations"] == len(log.by_type))
    kinds_on: dict[date, set] = {}
    for stamp, kind in zip(log.stamps, log.types):
        kinds_on.setdefault(stamp.date(), set()).add(kind)
    merged = [len(kinds_on.get(day, ())) for day in log.calendar]
    check("merged triggers: at least one on every active day and never more than the number of types",
          max(merged) <= len(log.by_type) and sum(value > 0 for value in merged) == observed["active_days"])
    return {
        "kind": "synthetic: the rule is stated by the design (observed); waking once at the end of each UTC day is assumed, "
                "because the driver was never scheduled",
        "rule": snapshot["design"]["deduplication_rule"],
        "distinct_type_repo_ref_combinations_in_the_log": recorded["distinct_type_repo_ref_combinations"],
        "trigger_files": log.total, "merged_triggers": sum(merged), "largest_day": max(merged),
        "days_by_merged_count": {str(value): merged.count(value) for value in sorted(set(merged))},
        "merged_as_share_of_files": share(sum(merged), log.total),
    } | {key: value for key, value in concentration(merged, [1, 4, 10], half, [50], "merged").items()
         if key in ("busiest_days", "gini_calendar_days", "mean_per_calendar_day", "median_calendar_day")}


SIMULATED = ("capacity_offered", "handled", "left_at_end", "late_events", "longest_wait_of_a_handled_event_days",
             "largest_backlog_at_end_of_day")


def plans_sized_before_the_end(log: Log, capacity: dict, checkpoints: list[str]) -> dict:
    """Each plan sized on the days read up to a date, then run on the days that follow (empty queue at the start)."""
    tolerance, readings = capacity["wait_tolerance_days"], []
    for text in checkpoints[:-1]:
        cut = sum(day <= date.fromisoformat(text) for day in log.calendar)
        seen, rest = log.counts[:cut], log.counts[cut:]
        check("a reading date splits the log into days read and days left, and neither part is empty",
              0 < cut < log.days and sum(seen) + sum(rest) == log.total)
        sized = []
        for plan in capacity["plans"]:
            value = plan_capacity(plan, seen)
            result = simulate(rest, value, tolerance)
            sized.append({"plan": plan["name"], "capacity_read_on_that_day": value,
                          "capacity_read_on_the_whole_log": plan_capacity(plan, log.counts)}
                         | {key: result[key] for key in SIMULATED}
                         | {"capacity_used": share(result["handled"], result["capacity_offered"])})
        enough = smallest_capacity(rest, tolerance)
        check("days left: no late event with their smallest sufficient capacity, at least one with one unit less",
              simulate(rest, enough, tolerance)["late_events"] == 0
              and simulate(rest, enough - 1, tolerance)["late_events"] > 0)
        readings.append({"read_on": text, "days_read": cut, "days_left": len(rest),
                         "events_on_the_days_left": sum(rest), "busiest_day_left": max(rest),
                         "smallest_capacity_without_a_late_event_on_the_days_read": smallest_capacity(seen, tolerance),
                         "smallest_capacity_without_a_late_event_on_the_days_left": enough,
                         "plans": sized})
    return {"kind": "synthetic: the same assumed rule; each plan is sized on the days read up to a date and run on "
                    "the days that follow",
            "note": capacity["earlier_readings_note"],
            "readings": readings}


def capacity_section(log: Log, design: dict, capacity: dict, checkpoints: list[str]) -> dict:
    """Capacity plans: an assumed rule on the observed arrivals. The orchestrator adds the synthetic logs and the hand case."""
    counts, total = log.counts, log.total
    tolerance, queue_limit = capacity["wait_tolerance_days"], design["queue_depth_max_triggers"]
    check("the wait tolerance in days is the design's staleness limit in hours",
          tolerance * 24 == design["staleness_hours"])
    plans = run_plans(counts, capacity["plans"], tolerance, queue_limit, log.first)
    peak_plan = next(row for row in plans if row["plan"] == "peak")
    check("a capacity equal to the busiest day leaves nothing waiting",
          peak_plan["late_events"] == 0 and peak_plan["largest_backlog_at_end_of_day"] == 0
          and peak_plan["handled_on_arrival_day"] == total)
    late_by_capacity = [simulate(counts, value, tolerance)["late_events"] for value in range(1, max(counts) + 1)]
    check("more capacity never makes more events late",
          all(a >= b for a, b in zip(late_by_capacity, late_by_capacity[1:])))
    smallest = smallest_capacity(counts, tolerance)
    check("the smallest sufficient capacity is exact: no late event with it, at least one with one unit less",
          late_by_capacity[smallest - 1] == 0 and late_by_capacity[smallest - 2] > 0)
    nothing = simulate(counts, 0, tolerance)
    check("negative control: with no capacity nothing is handled and every event is left",
          nothing["handled"] == 0 and nothing["left_at_end"] == total)
    smallest_row = simulate(counts, smallest, tolerance, queue_limit)
    mean = Fraction(total, log.days)
    return {
        "kind": "synthetic: an assumed handling rule applied to the observed daily counts; the repository states "
                "that the consumer of these triggers was never scheduled, so nothing here was measured",
        "handling_rule": capacity["handling_rule"],
        "wait_tolerance_days": tolerance, "wait_tolerance_note": capacity["wait_tolerance_note"],
        "queue_limit_from_the_design": queue_limit,
        "mean_per_calendar_day": amount(mean),
        "plans": plans,
        "smallest_capacity_without_a_late_event": {
            "capacity_per_day": smallest,
            "as_a_multiple_of_the_mean": rounded(smallest / mean, ROUND["mean"]),
            "late_events_with_one_unit_less": late_by_capacity[smallest - 2],
        } | {key: smallest_row[key] for key in ("capacity_offered", "handled", "handled_on_arrival_day",
                                                "longest_wait_of_a_handled_event_days", "largest_backlog_at_end_of_day",
                                                "days_ending_above_the_queue_limit")}
          | {"capacity_used": share(smallest_row["handled"], smallest_row["capacity_offered"])},
        "late_events_by_capacity_from_1": late_by_capacity,
        "plans_sized_on_an_earlier_reading": plans_sized_before_the_end(log, capacity, checkpoints),
    }


def capacity_on_the_synthetic_logs(rows: list[dict], summaries: dict, observed_measures: dict) -> dict:
    def wanted(key: str) -> bool:
        return "capacity" in key or key == "p95_of_daily_counts"

    late = {plan: sum(row[f"late_events_with_capacity_{plan}"] > 0 for row in rows) for plan in ("mean_rounded_up", "p95")}
    for plan, logs in late.items():
        counted = summaries[f"late_events_with_capacity_{plan}"]
        check("synthetic logs with a late event: none when the largest number of late events is 0, more than half "
              "of the logs when the median number is above 0",
              (logs == 0) == (counted["max"] == 0) and (counted["median"] > 0) <= (2 * logs > len(rows)), plan)
    return {
        "kind": "synthetic arrivals and an assumed rule",
        "logs": len(rows),
        **{key: summaries[key] for key in summaries if wanted(key)},
        "observed_log": {key: observed_measures[key] for key in observed_measures if wanted(key)},
        "logs_with_at_least_one_late_event": {f"with_capacity_{plan}": logs for plan, logs in late.items()},
    }


def analyze(snapshot: dict, scenarios: dict) -> dict:
    """One function per section of results.json, called in the order in which the self-checks are recorded."""
    CHECKS.clear()
    ROUND.clear()
    ROUND.update({key[:-len("_decimals")]: value for key, value in scenarios["rounding"].items()
                  if key.endswith("_decimals")})
    log = read_log(snapshot)
    observed = observed_section(log, snapshot, scenarios)
    ranking = rank_days(log, scenarios["top_k"])
    curve = lorenz_curve(log)
    mean_and_median = mean_and_median_section(log, observed, ranking[2], scenarios)
    day_boundary = day_boundary_section(log, scenarios)
    type_subsets = type_subsets_section(log, scenarios)
    busiest = busiest_days_section(log, ranking, observed, scenarios)
    deduplicated = deduplicated_section(log, snapshot, observed, scenarios["half_share_percent"])
    capacity = capacity_section(log, snapshot["design"], scenarios["capacity"], scenarios["checkpoints"]["dates"])
    tolerance = capacity["wait_tolerance_days"]
    control, summaries, rows = poisson_control(log.counts, scenarios["poisson_control"], tolerance)
    observed_measures = log_measures(log.counts, tolerance, with_capacity=True)
    return header(snapshot) | {
        "observed": observed,
        "busiest_days": busiest,
        "lorenz_and_gini": {
            "kind": "computed",
            "gini_formula": GINI_FORMULA,
            "other_formulas_checked_equal": ["mean absolute difference between two days / (2 * mean)",
                                             "1 - 2 * area under the Lorenz polygon"],
            "lorenz_curve_cumulative_events_from_the_quietest_day": curve,
            "hand_computed_cases": hand_cases(scenarios["hand_computed_cases"]["cases"]),
        },
        "mean_and_median": mean_and_median,
        "robustness": {
            "kind": "computed: the same measures under other analysis choices (day boundary, types counted), and the "
                    "log as the design's deduplication rule would have merged it",
            "day_boundary": day_boundary,
            "type_subsets": type_subsets,
            "deduplicated_once_a_day": deduplicated,
        },
        "poisson_control": control,
        "capacity": capacity | {
            "same_rule_on_the_synthetic_logs": capacity_on_the_synthetic_logs(rows, summaries, observed_measures),
            "hand_case": capacity_hand_case(scenarios["capacity"]["hand_case"]),
        },
        "candidate_logs": {"kind": "synthetic: imaginary summaries classified against the synthetic logs",
                           "note": scenarios["candidate_logs"]["note"],
                           "logs": classify_candidates(scenarios["candidate_logs"]["logs"], summaries,
                                                       observed_measures, log.total)},
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
    except (AssertionError, ArithmeticError, IndexError, KeyError, ValueError, OSError) as exc:
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
