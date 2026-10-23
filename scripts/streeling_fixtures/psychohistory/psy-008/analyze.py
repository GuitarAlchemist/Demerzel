#!/usr/bin/env python3
"""PSY-008 analysis: daily counts of the archived trigger log against a Poisson benchmark.

Reads observed-input.json (written by extract.py) and scenarios.json, never
the repository, and writes results.json. Counts, means and variances are exact
rational numbers, and the Poisson probabilities are summed in integer
arithmetic: no exp, log or pow of the C library reaches a stored digit. Every
variance is the sample variance (divisor n - 1).

Run from the repository root:
    python -I scripts/streeling_fixtures/psychohistory/psy-008/analyze.py
    python -I scripts/streeling_fixtures/psychohistory/psy-008/analyze.py --check
"""

from __future__ import annotations

import argparse
import json
import math
import random
import sys
from datetime import date, datetime, timedelta
from fractions import Fraction
from pathlib import Path

# This program lives under scripts/ (CONTRIBUTING.md: no executable code outside scripts/); its data stays
# under state/streeling/fixtures/. FIXTURE_FILE is the path the program would have next to that data.
FIXTURE_FILE = (Path(__file__).resolve().parents[4]
                / "state/streeling/fixtures/psychohistory/psy-008" / Path(__file__).name)

HERE = FIXTURE_FILE.parent
DECIMALS = {"ratio": 6, "percent": 2, "count": 2}
WEEKDAYS = ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday")
CHECKS: dict[str, int] = {}  # self-check -> times evaluated


def check(name: str, condition: bool, detail: str = "") -> None:
    """A self-check that can fail: abort instead of writing a wrong result."""
    if not condition:
        raise AssertionError(f"self-check failed: {name}" + (f" ({detail})" if detail else ""))
    CHECKS[name] = CHECKS.get(name, 0) + 1


def number(value: Fraction) -> dict:
    exact = str(value.numerator) if value.denominator == 1 else f"{value.numerator}/{value.denominator}"
    return {"exact": exact, "value": round(float(value), DECIMALS["ratio"])}


def share(numerator: int, denominator: int) -> dict:
    value = Fraction(numerator, denominator)
    return {"exact": f"{numerator}/{denominator}", "value": round(float(value), DECIMALS["ratio"]),
            "percent": round(float(100 * value), DECIMALS["percent"])}


def probability(value: Fraction) -> dict:
    return {"value": round(float(value), DECIMALS["ratio"]), "percent": round(float(100 * value), DECIMALS["percent"])}


def expected(trials: int, value: Fraction) -> float:
    return round(float(trials * value), DECIMALS["count"])


def root(value: Fraction) -> float:
    return math.sqrt(float(value))


def scientific(value: Fraction) -> dict:
    """value = mantissa x 10^power with 1 <= mantissa < 10, found by exact comparison."""
    power = 0
    while value >= Fraction(10) ** (power + 1):
        power += 1
    while value < Fraction(10) ** power:
        power -= 1
    mantissa = round(float(value / Fraction(10) ** power), 2)
    if mantissa >= 10:
        mantissa, power = 1.0, power + 1
    return {"mantissa": mantissa, "power_of_ten": power, "text": f"{mantissa:.2f}e{power:+d}"}


def moments(values: list[int]) -> dict:
    """Exact mean, sample variance (divisor n - 1) and index of dispersion."""
    n, total, squares = len(values), sum(values), sum(value * value for value in values)
    mean = Fraction(total, n)
    variance = Fraction(n * squares - total * total, n * (n - 1))
    return {"n": n, "total": total, "squares": squares, "mean": mean, "variance": variance,
            "index": variance / mean if total else None}


def quantile(values: list[int], level_percent: int) -> int:
    """Nearest rank: the k-th smallest value with k = ceil(level * n / 100)."""
    return sorted(values)[-(-level_percent * len(values) // 100) - 1]


def describe(values: list[int]) -> dict:
    m = moments(values)
    return {"n": m["n"], "total": m["total"], "sum_of_squares": m["squares"], "mean": number(m["mean"]),
            "sample_variance": number(m["variance"]), "standard_deviation": round(root(m["variance"]), DECIMALS["ratio"]),
            "index_of_dispersion": number(m["index"]), "zeros": values.count(0), "median": quantile(values, 50),
            "minimum": min(values), "maximum": max(values)}


def dispersion_scale(n: int, index: Fraction, band: int | None = None) -> dict:
    """Under a Poisson process (n - 1) x index is about chi-square with n - 1 degrees of freedom."""
    deviation = math.sqrt(2 / (n - 1))
    scale = {"standard_deviation_of_the_index_under_poisson": round(deviation, DECIMALS["ratio"]),
             "observed_index_minus_one_in_those_units": round((float(index) - 1) / deviation, DECIMALS["count"])}
    if band is not None:
        scale["index_band_for_a_constant_rate"] = [round(1 - band * deviation, DECIMALS["ratio"]),
                                                   round(1 + band * deviation, DECIMALS["ratio"])]
    return scale


class Poisson:
    """Poisson probabilities for a rational mean, in exact integer arithmetic.

    weights[k] is mean^k / k! times one common integer factor. The series stops
    after `terms` and is renormalised; `dropped` bounds the share left out.
    """

    def __init__(self, mean: Fraction, terms: int):
        if not 0 < mean < terms:
            raise ValueError("the Poisson mean must lie between 0 and the number of series terms")
        a, b = mean.numerator, mean.denominator
        weight, weights = b ** terms * math.factorial(terms), []
        for k in range(terms + 1):
            weights.append(weight)
            if k < terms:
                weight, remainder = divmod(weight * a, b * (k + 1))
                if remainder:
                    raise ArithmeticError("a Poisson weight is not an integer")
        self.mean, self.terms, self.weights, self.total = mean, terms, weights, sum(weights)
        self.dropped = Fraction(weights[-1]) * mean / (terms + 1) / (1 - mean / (terms + 2)) / self.total

    def p(self, low: int, high: int | None = None) -> Fraction:
        """P(low <= X <= high); without `high`, P(X >= low)."""
        top = self.terms if high is None else min(high, self.terms)
        return Fraction(sum(self.weights[low:top + 1]), self.total)

    def quantile(self, level_percent: int) -> int:
        running = 0
        for k, weight in enumerate(self.weights):
            running += weight
            if 100 * running >= level_percent * self.total:
                return k
        raise ArithmeticError("quantile not reached")

    def mean_and_variance(self) -> tuple[Fraction, Fraction]:
        first = Fraction(sum(k * weight for k, weight in enumerate(self.weights)), self.total)
        second = Fraction(sum(k * k * weight for k, weight in enumerate(self.weights)), self.total)
        return first, second - first * first


def checked_poisson(mean: Fraction, terms: int, label: str) -> Poisson:
    benchmark = Poisson(mean, terms)
    first, variance = benchmark.mean_and_variance()
    tiny = Fraction(1, 10 ** 100)
    check(f"{label}: the summed Poisson series has mean and variance equal to its parameter (within 1e-100)",
          abs(first - mean) < tiny and abs(variance - mean) < tiny)
    check(f"{label}: the Poisson terms left out of the series weigh less than 1e-200",
          benchmark.dropped < Fraction(1, 10 ** 200))
    return benchmark


def load_events(snapshot: dict) -> list[tuple[datetime, str]]:
    events = []
    for row in snapshot["events"]:
        stamp, kind = row.split(" ")
        events.append((datetime.strptime(stamp, "%Y-%m-%dT%H:%M:%SZ"), kind))
    if events != sorted(events):
        raise ValueError("the events of observed-input.json are not in time order")
    return events


def daily_series(events: list[tuple[datetime, str]], offset_hours: int = 0) -> tuple[date, list[int]]:
    """Events per calendar day from the first to the last day, days without event included."""
    days = [(moment + timedelta(hours=offset_hours)).date() for moment, _ in events]
    first = min(days)
    series = [0] * ((max(days) - first).days + 1)
    for day in days:
        series[(day - first).days] += 1
    return first, series


def claim_days(values: list[int], claim: dict) -> dict:
    low, high = claim["value"] - claim["tolerance"], claim["value"] + claim["tolerance"]
    return {"statement": claim["statement"], "value": claim["value"], "band": [low, high],
            "days_with_exactly_the_value": share(values.count(claim["value"]), len(values)),
            "days_inside_the_band": share(sum(low <= value <= high for value in values), len(values))}


def tolerance_band(values: list[int], tolerance_percent: int) -> tuple[Fraction, Fraction]:
    mean = Fraction(sum(values), len(values))
    return mean * (100 - tolerance_percent) / 100, mean * (100 + tolerance_percent) / 100


def longest_run(flags: list[bool]) -> int:
    best = current = 0
    for flag in flags:
        current = current + 1 if flag else 0
        best = max(best, current)
    return best


def growth_steps(values: list[int], factor: int) -> int:
    return sum(later > earlier and later >= factor * earlier for earlier, later in zip(values, values[1:]))


def window_report(series: list[int], length: int, tolerance_percent: int, factor: int, band: int) -> dict:
    if len(series) % length:
        raise ValueError(f"a window of {length} days does not divide {len(series)} days")
    totals = [sum(series[start:start + length]) for start in range(0, len(series), length)]
    check("window totals add up to the events", sum(totals) == sum(series))
    report = {"window_days": length, "totals": totals} | describe(totals)
    report |= dispersion_scale(len(totals), moments(totals)["index"], band)
    low, high = tolerance_band(totals, tolerance_percent)
    report["tolerance_band"] = [round(float(low), DECIMALS["count"]), round(float(high), DECIMALS["count"])]
    report["windows_within_tolerance_of_the_mean"] = share(sum(low <= value <= high for value in totals), len(totals))
    report["steps_between_neighbouring_windows"] = len(totals) - 1
    report["steps_where_the_total_at_least_doubles"] = growth_steps(totals, factor)
    return report


def poisson_report(benchmark: Poisson, values: list[int], claim: dict, level: int) -> dict:
    """Days a Poisson benchmark expects against the days counted in `values`."""
    n = len(values)
    low, high = claim["value"] - claim["tolerance"], claim["value"] + claim["tolerance"]
    burst_from = benchmark.quantile(level) + 1
    check("Poisson quantile: the cumulative probability first reaches the level at the reported count",
          benchmark.p(0, burst_from - 2) < Fraction(level, 100) <= benchmark.p(0, burst_from - 1))
    rows = {
        "no_event": (benchmark.p(0, 0), values.count(0)),
        "exactly_one_event": (benchmark.p(1, 1), values.count(1)),
        "exactly_the_claimed_value": (benchmark.p(claim["value"], claim["value"]), values.count(claim["value"])),
        "inside_the_claimed_band": (benchmark.p(low, high), sum(low <= value <= high for value in values)),
        "above_the_poisson_quantile": (benchmark.p(burst_from), sum(value >= burst_from for value in values)),
    }
    return {"mean": number(benchmark.mean), "variance": number(benchmark.mean),
            "quantile_level_percent": level, "quantile": burst_from - 1,
            "cumulative_probability_one_below_the_quantile": round(float(benchmark.p(0, burst_from - 2)), DECIMALS["ratio"]),
            "cumulative_probability_at_the_quantile": round(float(benchmark.p(0, burst_from - 1)), DECIMALS["ratio"]),
            "burst_day_from": burst_from,
            "days": {name: {"probability": probability(p), "expected_days": expected(n, p), "observed_days": observed}
                     for name, (p, observed) in rows.items()}}


def parse_schedule(crons: list[str]) -> dict:
    """Hour, minute and weekdays of cron lines of the form 'M H * * D' or 'M H * * D-D'."""
    times, weekdays = set(), set()
    for cron in crons:
        minute, hour, day_of_month, month, day_of_week = cron.split()
        if (day_of_month, month) != ("*", "*"):
            raise ValueError(f"unexpected cron line {cron!r}")
        times.add(f"{int(hour):02d}:{int(minute):02d}")
        for part in day_of_week.split(","):
            low, _, high = part.partition("-")
            weekdays.update(range(int(low), int(high or low) + 1))
    if len(times) != 1:
        raise ValueError("the cron lines do not share one time of day")
    return {"cron_utc": crons, "time_of_day_utc": times.pop(),
            "weekdays": [WEEKDAYS[(day - 1) % 7] for day in sorted(weekdays)]}


def hand_computed_case(terms: int) -> None:
    """Five days worked by hand in the README, and a Poisson distribution with mean 2."""
    values = [0, 1, 1, 2, 6]
    m = moments(values)
    check("hand-computed case: counts 0 1 1 2 6 give mean 2, sample variance 11/2, index 11/4, median 1, 80% quantile 2",
          (m["total"], m["squares"], m["mean"], m["variance"], m["index"], quantile(values, 50), quantile(values, 80))
          == (10, 42, 2, Fraction(11, 2), Fraction(11, 4), 1, 2))
    check("hand-computed case: longest run of true flags in 0 1 1 0 1 is 2, steps that at least double in 1 2 3 7 0 5 are 3",
          (longest_run([False, True, True, False, True]), growth_steps([1, 2, 3, 7, 0, 5], 2)) == (2, 3))
    two = checked_poisson(Fraction(2), terms, "hand-computed case")
    check("hand-computed case: Poisson mean 2 gives P(0) = 0.135335, P(X <= 2) = 0.676676, P(X >= 6) = 0.016564, 99% quantile 6",
          (round(float(two.p(0, 0)), 6), round(float(two.p(0, 2)), 6), round(float(two.p(6)), 6), two.quantile(99))
          == (0.135335, 0.676676, 0.016564, 6))
    check("hand-computed case: the exact P(0) agrees with math.exp(-2) to 12 decimals",
          abs(float(two.p(0, 0)) - math.exp(-2)) < 1e-12)
    check("hand-computed case: scientific notation gives 1/8000 = 1.25e-4", scientific(Fraction(1, 8000))
          == {"mantissa": 1.25, "power_of_ten": -4, "text": "1.25e-4"})


def control_logs(events: int, days: int, benchmark: Poisson, claim: dict, level: int, settings: dict) -> dict:
    """Synthetic logs with the observed size: the code must be able to return a small index."""
    even = [events // days + (1 if day < events % days else 0) for day in range(days)]
    rng = random.Random(settings["seed"])
    constant = [0] * days
    for _ in range(events):
        constant[int(rng.random() * days)] += 1
    planted = list(even)
    planted[days // 2] += settings["planted_burst_events"]
    burst_from = benchmark.quantile(level) + 1
    low, high = claim["value"] - claim["tolerance"], claim["value"] + claim["tolerance"]

    def report(values: list[int]) -> dict:
        summary = describe(values)
        return {key: summary[key] for key in ("n", "total", "mean", "sample_variance", "index_of_dispersion", "zeros",
                                              "median", "maximum")} | {
            "days_inside_the_claimed_band": sum(low <= value <= high for value in values),
            "burst_days": sum(value >= burst_from for value in values)}

    band = settings["index_band_standard_deviations"] * math.sqrt(2 / (days - 1))
    indices = {name: moments(values)["index"] for name, values in (("even", even), ("constant", constant), ("planted", planted))}
    check("control: an evenly spread log with the observed mean has an index of dispersion below 0.01, no empty day "
          "and no burst day", sum(even) == events and indices["even"] < Fraction(1, 100)
          and report(even)["zeros"] == 0 and report(even)["burst_days"] == 0)
    check("control: a seeded constant-rate log of the observed size has an index of dispersion within the band around 1",
          sum(constant) == events and abs(float(indices["constant"]) - 1) <= band)
    check("control: one planted burst lifts the index of the even log above the constant-rate log's and is counted "
          "as one burst day", indices["planted"] > indices["constant"] and report(planted)["burst_days"] == 1)
    return {
        "kind": "synthetic logs, not project data",
        "seed": settings["seed"],
        "evenly_spread": {"how": "the observed events spread as evenly as possible over the observed days"} | report(even),
        "constant_rate": {"how": "each observed event placed on a day drawn uniformly with random.Random(seed).random()",
                          "accepted_index_band": [round(1 - band, DECIMALS["ratio"]), round(1 + band, DECIMALS["ratio"])]}
                         | report(constant),
        "planted_burst": {"how": f"the evenly spread log with {settings['planted_burst_events']} events added to one day"}
                         | report(planted),
    }


def transfer_task(task: dict, terms: int) -> dict:
    values = task["daily_counts"]
    m = moments(values)
    n, total, active = m["n"], m["total"], sum(value > 0 for value in values)
    claim = task["claimed_rate"]
    benchmark = checked_poisson(m["mean"], terms, "transfer task")
    poisson = poisson_report(benchmark, values, claim, task["burst_day_level_percent"])
    band = task["index_band_standard_deviations"]
    weeks = window_report(values, task["window_days"], task["window_tolerance_percent"], 2, band)
    scale = dispersion_scale(n, m["index"], band)
    check("transfer task: hand-computed mean 3, mean per active day 4, sample variance 34, index 34/3, weekly totals 6 8 61 9",
          (m["mean"], Fraction(total, active), m["variance"], m["index"], weeks["totals"])
          == (3, 4, 34, Fraction(34, 3), [6, 8, 61, 9]))
    return {
        "note": task["note"],
        "q1_counting": {
            "days": n, "events": total, "days_with_an_event": active, "days_without_event": share(n - active, n),
            "mean_per_calendar_day": number(m["mean"]), "mean_per_active_day": number(Fraction(total, active)),
            "histogram": {str(value): values.count(value) for value in sorted(set(values))},
            "claim": claim_days(values, claim)},
        "q2_dispersion": {"sum_of_squares": m["squares"],
                          "sum_of_squared_deviations": number(m["squares"] - Fraction(total * total, n)),
                          "sample_variance": number(m["variance"]),
                          "index_of_dispersion": number(m["index"])}
                         | {key: value for key, value in scale.items() if key != "index_band_for_a_constant_rate"},
        "q3_poisson_benchmark": poisson | {
            "busiest_day": max(values), "probability_of_a_day_at_least_that_busy": scientific(benchmark.p(max(values)))},
        "q4_weeks": {key: weeks[key] for key in ("window_days", "totals", "mean", "sample_variance", "index_of_dispersion",
                                                 "median", "tolerance_band", "windows_within_tolerance_of_the_mean")},
        "q5_reference": {
            "note": "No single answer. One usable falsifier of 'about three a day': over the next log of the same "
                    "length, the index of dispersion of the daily counts falls outside the band below.",
            "index_band_standard_deviations": band,
            "index_band_for_a_constant_rate": scale["index_band_for_a_constant_rate"],
            "figures_to_report_in_place_of_the_mean": {
                "days_without_event": share(n - active, n), "median": quantile(values, 50),
                "quantile_90_nearest_rank": quantile(values, 90), "maximum": max(values),
                "burst_days": sum(value >= poisson["burst_day_from"] for value in values),
                "events_on_burst_days": sum(value for value in values if value >= poisson["burst_day_from"]),
                "longest_run_of_neighbouring_burst_days": longest_run([value >= poisson["burst_day_from"] for value in values])}},
    }


class DailyLog:
    """The events of the snapshot as counts per UTC calendar day, in total and per type."""

    def __init__(self, events: list[tuple[datetime, str]]):
        self.events = events
        self.first, self.series = daily_series(events)
        self.n, self.total = len(self.series), sum(self.series)
        self.day = [self.first + timedelta(days=index) for index in range(self.n)]
        self.active = sum(value > 0 for value in self.series)
        self.by_day: list[list[tuple[datetime, str]]] = [[] for _ in range(self.n)]
        for moment, kind in events:
            self.by_day[(moment.date() - self.first).days].append((moment, kind))
        self.types = sorted({kind for _, kind in events}, key=lambda kind: (-sum(k == kind for _, k in events), kind))
        self.type_series = {kind: [sum(k == kind for _, k in rows) for rows in self.by_day] for kind in self.types}
        self.moments = moments(self.series)


def source_section(snapshot: dict) -> dict:
    source = snapshot["source"]
    return {"repository": source["repository"], "commit": source["commit"],
            "trigger_folder": {key: source["trigger_folder"][key] for key in ("path", "files", "git_tree", "manifest_sha256")},
            "files": [entry["path"] for entry in source["files"]]}


def observed_section(log: DailyLog, snapshot: dict) -> dict:
    """The counts made by extract.py, cross-checked against a recount of the event rows."""
    counts, producer = snapshot["counts"], snapshot["producer_workflow"]
    series, types, type_series, n, total, active = log.series, log.types, log.type_series, log.n, log.total, log.active
    check("recount of events, days and types equals extract.py's counts",
          (total, len(log.events), log.first.isoformat(), log.day[-1].isoformat(), n, active, n - active,
           {kind: sum(type_series[kind]) for kind in types})
          == (counts["events"], counts["events"], counts["first_day"], counts["last_day"], counts["calendar_days"],
              counts["active_days"], counts["days_without_event"], counts["by_type"]))
    check("active days + days without event = calendar days", active + series.count(0) == n)
    check("per-type daily counts add up to the daily counts",
          all(sum(type_series[kind][index] for kind in types) == series[index] for index in range(n)))
    check("each archived file is one run of the producer workflow: run ids and timestamps are all distinct",
          counts["distinct_run_ids"] == counts["distinct_timestamps"] == total)
    writable = [kind for kind in producer["trigger_types_it_can_write"] if "$" not in kind]
    check("every archived type is one the producer workflow can write",
          all(kind in writable or kind.startswith("issue_") for kind in types))
    check("the producer workflow's comment states the archived number of events",
          producer["orphaned_triggers_stated_in_comment"] == total)
    return {
        "kind": "observed: counted from observed-input.json",
        "events": total, "first_event": counts["first_event"], "last_event": counts["last_event"],
        "first_day": log.first.isoformat(), "first_weekday": WEEKDAYS[log.first.weekday()],
        "last_day": log.day[-1].isoformat(),
        "calendar_days": n, "active_days": active, "days_without_event": n - active,
        "distinct_run_ids": counts["distinct_run_ids"], "distinct_senders": counts["distinct_senders"],
        "distinct_repos": counts["distinct_repos"],
        "producer_workflow": producer,
        "types_the_producer_can_write_but_the_archive_never_holds": [kind for kind in writable if kind not in types],
    }


def day_histogram(log: DailyLog) -> dict:
    """Number of days for each daily count that occurs."""
    histogram = {str(value): log.series.count(value) for value in sorted(set(log.series))}
    check("histogram days add up to the calendar days and its events to the total",
          (sum(histogram.values()), sum(int(value) * days for value, days in histogram.items())) == (log.n, log.total))
    return histogram


def poisson_section(log: DailyLog, benchmark: Poisson, claim: dict, level: int) -> dict:
    return ({"kind": "a benchmark distribution with the observed mean, not data and not a fitted model"}
            | poisson_report(benchmark, log.series, claim, level)
            | {"dispersion": dispersion_scale(log.n, log.moments["index"]),
               "series_terms": benchmark.terms, "arithmetic": "exact integers; no exp, log or pow"})


def day_bands(log: DailyLog, benchmark: Poisson, typical: int, burst_from: int) -> list[dict]:
    """Empty, typical, middle and burst days: observed days and events, and the days the benchmark expects."""
    series, n = log.series, log.n
    limits = [(0, 0), (1, typical), (typical + 1, burst_from - 1), (burst_from, None)]
    bands = []
    for low, high in limits:
        inside = [value for value in series if value >= low and (high is None or value <= high)]
        bands.append({"events_per_day": f"{low}" if low == high else f"{low} or more" if high is None else f"{low} to {high}",
                      "days": len(inside), "share_of_days": share(len(inside), n), "events": sum(inside),
                      "poisson_expected_days": expected(n, benchmark.p(low, high))})
    check("the bands partition the days and the events",
          (sum(band["days"] for band in bands), sum(band["events"] for band in bands)) == (n, log.total)
          and sum(benchmark.p(low, high) for low, high in limits) == 1)
    return bands


def daily_counts_section(log: DailyLog, claim: dict, histogram: dict, bands: list[dict]) -> dict:
    series, n, total, active, m = log.series, log.n, log.total, log.active, log.moments
    return {
        "kind": "computed",
        "series": " ".join(str(value) for value in series),
        "series_note": f"events per UTC calendar day, {log.first.isoformat()} first, days without event included",
        "histogram": histogram,
        "mean_per_calendar_day": number(m["mean"]),
        "mean_per_active_day": number(Fraction(total, active)),
        "sum_of_squared_counts": m["squares"],
        "sample_variance": number(m["variance"]),
        "standard_deviation": round(root(m["variance"]), DECIMALS["ratio"]),
        "index_of_dispersion": number(m["index"]),
        "days_without_event": share(n - active, n),
        "mode": {"events": max(histogram, key=lambda value: (histogram[value], -int(value))),
                 "days": share(max(histogram.values()), n)},
        "days_above_the_mean": sum(value > m["mean"] for value in series),
        "claim": claim_days(series, claim),
        "bands": bands,
    }


def busiest_days(log: DailyLog, benchmark: Poisson, how_many: int) -> tuple[list[dict], dict]:
    """The busiest days by type, and the share of push events on them against the rest of the log."""
    series, day, push, n, total = log.series, log.day, log.type_series["push"], log.n, log.total
    order = sorted(range(n), key=lambda index: (-series[index], index))[:how_many]
    busiest = []
    for index in order:
        tail = benchmark.p(series[index])
        busiest.append({"day": day[index].isoformat(), "weekday": WEEKDAYS[day[index].weekday()], "events": series[index],
                        "by_type": {kind: log.type_series[kind][index] for kind in log.types},
                        "push_share": share(push[index], series[index]),
                        "poisson_probability_of_a_day_at_least_this_busy": scientific(tail),
                        "union_bound_over_all_calendar_days": scientific(n * tail)})
    top_events, top_push = sum(series[index] for index in order), sum(push[index] for index in order)
    all_push = sum(push)
    check("the busiest days are in decreasing order and no other day is busier",
          [series[index] for index in order] == sorted(series, reverse=True)[:len(order)])
    return busiest, {"on_the_busiest_days": share(top_push, top_events),
                     "on_all_other_days": share(all_push - top_push, total - top_events),
                     "in_the_whole_log": share(all_push, total)}


def anti_pattern_section(log: DailyLog, record: dict, rule: dict) -> dict:
    """The pattern record's threshold applied to the producer's runs per day and to the push events per day."""
    series, push, n = log.series, log.type_series["push"], log.n
    threshold = rule["runs_per_day_more_than"]
    check("the pattern record's detection sentence still holds the threshold used here",
          rule["must_appear_in_detection"] in record["detection"])
    seen = [(date.fromisoformat(record[key]) - log.first).days for key in ("first_seen", "last_seen")]
    if not all(0 <= index < n for index in seen):
        raise ValueError("the pattern record's dates lie outside the log")
    after = range(seen[1] + 1, n)
    return {
        "record": {key: record[key] for key in ("pattern_id", "detection", "occurrence_count", "first_seen", "last_seen",
                                                "status", "resolution")},
        "threshold_runs_per_day": threshold,
        "note": "Each archived file is one run of the producer workflow, so a day's event count is that workflow's "
                "run count. Push events are the cause the record names; they are not the duplicate runs it describes.",
        "events_on_first_seen_and_last_seen": [series[index] for index in seen],
        "push_events_on_first_seen_and_last_seen": [push[index] for index in seen],
        "days_with_more_producer_runs_than_the_threshold": sum(value > threshold for value in series),
        "of_which_after_last_seen": sum(series[index] > threshold for index in after),
        "days_with_more_push_events_than_the_threshold": sum(value > threshold for value in push),
        "of_which_after_last_seen_push": sum(push[index] > threshold for index in after),
        "push_events_after_last_seen": sum(push[index] for index in after),
    }


def day_class(log: DailyLog, indices: list[int]) -> dict:
    own = [log.series[index] for index in indices]
    return {"days": len(own), "events": sum(own), "share_of_events": share(sum(own), log.total),
            "mean": number(Fraction(sum(own), len(own))), "days_without_event": own.count(0),
            "days_with_a_discussion_created": sum(log.type_series["discussion_created"][index] > 0 for index in indices),
            "maximum": max(own)}


def calendar_section(log: DailyLog, crons: list[str]) -> dict:
    """One-event days and their hour, weekdays against weekends, and the scheduled workflow's cron lines."""
    series, day, by_day, n = log.series, log.day, log.by_day, log.n
    single = [index for index in range(n) if series[index] == 1]
    single_types = {kind: sum(by_day[index][0][1] == kind for index in single) for kind in log.types}
    clock = [index for index in single if by_day[index][0][1] == "discussion_created"]
    clock_times = sorted(by_day[index][0][0].strftime("%H:%M") for index in clock)
    weekday = [index for index in range(n) if day[index].weekday() < 5]
    weekend = [index for index in range(n) if day[index].weekday() >= 5]
    empty = [index for index in range(n) if series[index] == 0]
    calendar = {
        "single_event_days": {"days": len(single), "by_type": {kind: value for kind, value in single_types.items() if value},
                              "single_discussion_created": {
                                  "days": len(clock), "on_monday_to_friday": sum(day[index].weekday() < 5 for index in clock),
                                  "earliest_time_utc": clock_times[0], "latest_time_utc": clock_times[-1],
                                  "between_13_00_and_16_59_utc": sum("13:00" <= value <= "16:59" for value in clock_times)}},
        "scheduled_workflow": parse_schedule(crons),
        "monday_to_friday": day_class(log, weekday),
        "saturday_and_sunday": day_class(log, weekend),
        "days_without_event": {"days": len(empty), "on_saturday_or_sunday": sum(day[index].weekday() >= 5 for index in empty),
                               "on_monday_to_friday": [f"{day[index].isoformat()} {WEEKDAYS[day[index].weekday()]}"
                                                       for index in empty if day[index].weekday() < 5]},
    }
    check("weekday and weekend days partition the days and the events; single-event day types add up",
          (len(weekday) + len(weekend), calendar["monday_to_friday"]["events"] + calendar["saturday_and_sunday"]["events"],
           sum(single_types.values())) == (n, log.total, len(single)))
    return calendar


def composition_section(log: DailyLog, snapshot: dict, scenarios: dict, benchmark: Poisson) -> dict:
    busiest, push_share = busiest_days(log, benchmark, scenarios["poisson_benchmark"]["busiest_days"])
    anti_pattern = anti_pattern_section(log, snapshot["anti_pattern_record"], scenarios["anti_pattern_rule"])
    calendar = calendar_section(log, snapshot["scheduled_discussion_workflow"]["cron_utc"])
    return {
        "kind": "computed from the event types",
        "by_type": {kind: {"events": sum(counts), "share": share(sum(counts), log.total),
                           "days_with_at_least_one": sum(value > 0 for value in counts),
                           "busiest_day": max(counts),
                           "index_of_dispersion": number(moments(counts)["index"])}
                    for kind, counts in log.type_series.items()},
        "busiest_days": busiest,
        "push_share": push_share,
        "anti_pattern": anti_pattern,
        "calendar": calendar,
    }


def windows_section(log: DailyLog, spec: dict) -> dict:
    """Blocks of consecutive days; the one-day block must give the daily figures again."""
    windows = [window_report(log.series, length, spec["tolerance_percent"], spec["growth_factor"],
                             spec["index_band_standard_deviations"]) for length in [1] + spec["days"]]
    for window in windows:
        if window["window_days"] == 1:
            del window["totals"]
    check("a one-day window reproduces the daily index of dispersion",
          windows[0]["index_of_dispersion"] == number(log.moments["index"]) and windows[0]["n"] == log.n)
    return {"kind": "computed; blocks of consecutive days counted from the first day",
            "tolerance_percent": spec["tolerance_percent"], "growth_factor": spec["growth_factor"],
            "index_band_standard_deviations": spec["index_band_standard_deviations"], "by_length": windows}


def day_boundary_section(log: DailyLog, offsets: list[int], claim: dict) -> dict:
    """The same events with the day boundary moved by a few hours."""
    boundary = []
    for offset in offsets:
        shifted_first, shifted = daily_series(log.events, offset)
        own = moments(shifted)
        boundary.append({"offset_hours": offset, "first_day": shifted_first.isoformat(), "calendar_days": own["n"],
                         "days_without_event": shifted.count(0), "median": quantile(shifted, 50), "busiest_day": max(shifted),
                         "index_of_dispersion": round(float(own["index"]), DECIMALS["ratio"]),
                         "days_inside_the_claimed_band": claim_days(shifted, claim)["days_inside_the_band"]["exact"]})
    check("day boundary: offset 0 reproduces the daily series",
          (boundary[0]["offset_hours"], boundary[0]["calendar_days"], boundary[0]["days_without_event"],
           boundary[0]["busiest_day"], boundary[0]["index_of_dispersion"])
          == (0, log.n, log.n - log.active, max(log.series), round(float(log.moments["index"]), DECIMALS["ratio"])))
    return {"kind": "computed; the same events with the day boundary moved", "by_offset": boundary}


def uncertainty_section(log: DailyLog, week: dict) -> dict:
    """Three standard errors of the mean per calendar day: Poisson, daily variance, 7-day blocks."""
    m, n = log.moments, log.n
    week_moments = moments(week["totals"])
    se_poisson, se_days = root(m["mean"] / n), root(m["variance"] / n)
    se_weeks = root(week_moments["variance"] / week_moments["n"]) / 7
    check("standard error ratio squared equals the index of dispersion",
          abs((se_days / se_poisson) ** 2 - float(m["index"])) < 1e-9)
    return {
        "kind": "computed; each line is one standard error of the mean per calendar day",
        "mean": number(m["mean"]),
        "if_days_were_poisson": round(se_poisson, DECIMALS["ratio"]),
        "from_the_sample_variance_of_days": round(se_days, DECIMALS["ratio"]),
        "from_the_sample_variance_of_7_day_blocks": round(se_weeks, DECIMALS["ratio"]),
        "ratio_days_to_poisson": round(se_days / se_poisson, DECIMALS["ratio"]),
        "ratio_blocks_to_poisson": round(se_weeks / se_poisson, DECIMALS["ratio"]),
        "note": "The second line treats days as independent, which the growth of the index with the window length "
                "contradicts; the third uses 17 blocks, two of which hold the bursts. Neither is a precise interval.",
    }


def split_episodes(burst: list[int], gap: int) -> list[list[int]]:
    """Burst days (as day numbers) grouped into episodes: neighbours in a group are at most `gap` days apart."""
    episodes: list[list[int]] = []
    for index in burst:
        if episodes and index - episodes[-1][-1] <= gap:
            episodes[-1].append(index)
        else:
            episodes.append([index])
    return episodes


def planning_section(log: DailyLog, scenarios: dict, poisson: dict, bands: list[dict]) -> dict:
    """Figures a plan can use in place of the mean: shares of days, quantiles, burst days and episodes."""
    series, day, n = log.series, log.day, log.n
    burst_from, level = poisson["burst_day_from"], poisson["quantile_level_percent"]
    typical, gap = scenarios["typical_day_max_events"], scenarios["episode_gap_days"]
    burst = [index for index in range(n) if series[index] >= burst_from]
    episodes = split_episodes(burst, gap)
    steps = [later - earlier for earlier, later in zip(burst, burst[1:])]
    inside_gaps = [step for step in steps if step <= gap]
    between_gaps = [step for step in steps if step > gap]
    check("episodes hold every burst day once", sum(len(episode) for episode in episodes) == len(burst) == bands[-1]["days"])
    return {
        "kind": "computed from the daily counts",
        "share_of_days_without_event": share(series.count(0), n),
        "share_of_days_with_exactly_one_event": share(series.count(1), n),
        "share_of_days_with_at_most_the_typical_maximum": share(sum(value <= typical for value in series), n),
        "typical_day_max_events": typical,
        "quantiles_nearest_rank": {str(q): quantile(series, q) for q in scenarios["quantile_levels_percent"]},
        "maximum": max(series),
        "burst_days": {"definition": f"a day with at least {burst_from} events, above the {level}% quantile of the "
                                     "Poisson benchmark", "days": share(len(burst), n),
                       "events": sum(series[index] for index in burst),
                       "smallest_and_largest_count": [min(series[index] for index in burst), max(series[index] for index in burst)]},
        "episodes": {"rule": f"burst days at most {gap} days apart belong to one episode", "count": len(episodes),
                     "list": [{"first_burst_day": day[episode[0]].isoformat(), "last_burst_day": day[episode[-1]].isoformat(),
                               "burst_days": len(episode), "events_on_burst_days": sum(series[index] for index in episode)}
                              for episode in episodes],
                     "largest_gap_inside_an_episode_days": max(inside_gaps) if inside_gaps else None,
                     "smallest_gap_between_episodes_days": min(between_gaps) if between_gaps else None},
    }


def exercises_section(log: DailyLog, benchmark: Poisson, poisson: dict, week: dict, horizon: int) -> dict:
    """Intermediate values that the lesson's worked answers show."""
    series, n, total, active, m = log.series, log.n, log.total, log.active, log.moments
    square_of_total_over_n = Fraction(total * total, n)
    return {
        "kind": "intermediate values of the lesson's worked answers",
        "exercise_1": {"mean_per_calendar_day": number(m["mean"]), "mean_per_active_day": number(Fraction(total, active)),
                       "active_over_calendar_mean": number(Fraction(n, active)), "horizon_days": horizon,
                       "events_expected_from_the_calendar_mean": number(horizon * m["mean"]),
                       "events_expected_from_the_active_mean": number(Fraction(horizon * total, active))},
        "exercise_2": {"sum_of_counts": total, "sum_of_squared_counts": m["squares"],
                       "square_of_the_sum_over_n": number(square_of_total_over_n),
                       "sum_of_squared_deviations": number(m["squares"] - square_of_total_over_n),
                       "sample_variance": number(m["variance"]), "index_of_dispersion": number(m["index"])}
                      | dispersion_scale(n, m["index"]),
        "exercise_3": {"probability_of_no_event": poisson["days"]["no_event"]["probability"]["value"],
                       "expected_days_without_event": poisson["days"]["no_event"]["expected_days"],
                       "observed_over_expected_days_without_event":
                           round(float(Fraction(series.count(0)) / (n * benchmark.p(0, 0))), DECIMALS["count"]),
                       "expected_days_with_exactly_one_event": poisson["days"]["exactly_one_event"]["expected_days"],
                       "observed_over_expected_days_with_exactly_one_event":
                           round(float(Fraction(series.count(1)) / (n * benchmark.p(1, 1))), DECIMALS["count"])},
        "exercise_5": {"weekly_totals_sorted": sorted(week["totals"]), "mean_week": week["mean"], "median_week": week["median"],
                       "tolerance_band": week["tolerance_band"],
                       "weeks_inside_the_band": week["windows_within_tolerance_of_the_mean"]["exact"],
                       "index_daily": number(m["index"]), "index_weekly": week["index_of_dispersion"],
                       "standard_deviation_of_the_weekly_index_under_poisson":
                           week["standard_deviation_of_the_index_under_poisson"],
                       "index_band_for_a_constant_rate": week["index_band_for_a_constant_rate"]},
    }


def deleted_triggers_section(log: DailyLog, scenarios: dict, busiest: list[dict]) -> dict:
    """Sensitivity: the daily counts once the trigger files deleted without being archived are added back."""
    settings, deleted = scenarios["poisson_benchmark"], scenarios["deleted_triggers"]["files_by_day"]
    with_them, by_day = list(log.series), {}
    for day_text, files in deleted.items():
        index = (date.fromisoformat(day_text) - log.first).days
        if not 0 <= index < log.n or files < 1:
            raise ValueError("a deleted trigger file must be dated inside the log")
        with_them[index] += files
        by_day[day_text] = {"archived_events": log.series[index], "deleted_files": files,
                            "events_with_them": with_them[index]}
    m = moments(with_them)
    check("deleted triggers: the log with them holds the archived events plus the deleted files on the same calendar days",
          (m["total"], m["n"]) == (log.total + sum(deleted.values()), log.n))
    benchmark = checked_poisson(m["mean"], settings["series_terms"], "log with the deleted triggers")
    burst_from = benchmark.quantile(settings["burst_day_level_percent"]) + 1
    burst = [index for index, value in enumerate(with_them) if value >= burst_from]
    top = [row["events"] for row in busiest]
    return {
        "kind": "sensitivity to an input of scenarios.json: trigger files deleted without being archived, reported by "
                "PSY-009 from the repository history and not read by this fixture",
        "deleted_files": sum(deleted.values()),
        "by_day": by_day,
        "deleted_files_on_the_busiest_days": sum(deleted.get(row["day"], 0) for row in busiest),
        "busiest_days_unchanged": sorted(with_them, reverse=True)[:len(top)] == top,
        "events_with_them": m["total"],
        "mean_per_calendar_day": number(m["mean"]),
        "sample_variance": number(m["variance"]),
        "index_of_dispersion": number(m["index"]),
        "burst_day_from": burst_from,
        "burst_days": len(burst),
        "episodes": len(split_episodes(burst, scenarios["episode_gap_days"])),
    }


def analyze(snapshot: dict, scenarios: dict) -> dict:
    """Build results.json: one function per section, called in the order of the file."""
    if scenarios["rounding"] != {f"{key}_decimals": value for key, value in DECIMALS.items()}:
        raise ValueError("scenarios.json rounding does not match analyze.py")
    settings, claim = scenarios["poisson_benchmark"], scenarios["claimed_rate"]
    level = settings["burst_day_level_percent"]
    hand_computed_case(settings["series_terms"])
    log = DailyLog(load_events(snapshot))
    observed = observed_section(log, snapshot)
    histogram = day_histogram(log)
    benchmark = checked_poisson(log.moments["mean"], settings["series_terms"], "observed log")
    poisson = poisson_section(log, benchmark, claim, level)
    bands = day_bands(log, benchmark, scenarios["typical_day_max_events"], poisson["burst_day_from"])
    composition = composition_section(log, snapshot, scenarios, benchmark)
    windows = windows_section(log, scenarios["windows"])
    week = next(window for window in windows["by_length"] if window["window_days"] == 7)
    boundary = day_boundary_section(log, scenarios["day_definition"]["offsets_hours"], claim)
    uncertainty = uncertainty_section(log, week)
    planning = planning_section(log, scenarios, poisson, bands)
    exercises = exercises_section(log, benchmark, poisson, week, scenarios["horizon_days"])
    controls = control_logs(log.total, log.n, benchmark, claim, level, scenarios["controls"])
    transfer = transfer_task(scenarios["transfer_task"], settings["series_terms"])
    deleted = deleted_triggers_section(log, scenarios, composition["busiest_days"])
    return {
        "module_id": snapshot["module_id"],
        "rounding": "ratios, probabilities, means, variances and indices to 6 decimals; percentages and expected numbers "
                    "of days to 2 decimals; 'exact' is the unrounded fraction; very small probabilities are given as "
                    "mantissa (2 decimals) and power of ten",
        "variance_convention": f"{scenarios['variance']['estimator']}, divisor {scenarios['variance']['divisor']}, everywhere",
        "source": source_section(snapshot),
        "observed": observed,
        "daily_counts": daily_counts_section(log, claim, histogram, bands),
        "poisson_benchmark": poisson,
        "composition": composition,
        "windows": windows,
        "day_boundary": boundary,
        "uncertainty_of_the_mean": uncertainty,
        "planning": planning,
        "lesson_exercises": exercises,
        "negative_controls": controls,
        "transfer_task": transfer,
        "deleted_triggers": deleted,
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
