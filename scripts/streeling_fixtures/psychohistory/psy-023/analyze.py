#!/usr/bin/env python3
"""PSY-023 analysis: how often alarm rules for a plan cry wolf, and how late they notice a slowdown.

Synthetic: reads scenarios.json only, never the repository, and writes results.json.

Weekly output is a count of fair coins (one per draft in work), so every "exact" figure is a count of equally
likely histories divided by a power of two. The recursion carries those counts as whole numbers and the results
as fractions; nothing is approximated before the final rounding. The simulation is a second, independent route:
it draws the same coins from random.Random(seed).random() and counts alarms.

No logarithm, exponential or power of the C library enters the output. The only floating-point functions are
math.sqrt and math.fsum, which are correctly rounded, so results.json is the same on every platform.

Run from the repository root:
    python -I -B scripts/streeling_fixtures/psychohistory/psy-023/analyze.py
    python -I -B scripts/streeling_fixtures/psychohistory/psy-023/analyze.py --check
"""

from __future__ import annotations

import argparse
import json
import math
import random
import sys
from fractions import Fraction
from pathlib import Path

# This program lives under scripts/ (CONTRIBUTING.md: no executable code outside scripts/); its data stays
# under state/streeling/fixtures/. FIXTURE_FILE is the path the program would have next to that data.
FIXTURE_FILE = (Path(__file__).resolve().parents[4]
                / "state/streeling/fixtures/psychohistory/psy-023" / Path(__file__).name)

HERE = FIXTURE_FILE.parent
DECIMALS = {"probability": 6, "weeks": 2, "courses": 4, "score": 2, "cost": 2}
ONES = [bin(value).count("1") for value in range(1024)]  # heads among the bits of a number below 1024
CHECKS: dict[str, int] = {}  # self-check -> times evaluated
AGREEMENT: list[dict] = []  # every comparison of a simulated figure with its exact value


def check(name: str, condition: bool, detail: str = "") -> None:
    """A self-check that can fail: abort instead of writing a wrong result."""
    if not condition:
        raise AssertionError(f"self-check failed: {name}" + (f" ({detail})" if detail else ""))
    CHECKS[name] = CHECKS.get(name, 0) + 1


def rnd(value, kind: str) -> float:
    """Round for storage: a fraction exactly (half to even), a float with round()."""
    if isinstance(value, Fraction):
        return float(round(value, DECIMALS[kind])) + 0.0
    return round(float(value), DECIMALS[kind]) + 0.0


def text(value: Fraction) -> str:
    return f"{value.numerator}/{value.denominator}"


# --- weekly output: equally likely histories ---------------------------------------------------------------

def coin_weeks(drafts: int) -> dict:
    """A week with `drafts` drafts in work: x courses are finished in C(drafts, x) of the 2^drafts coin histories."""
    return {"ways": {x: math.comb(drafts, x) for x in range(drafts + 1)}, "total": 2 ** drafts}


def batch_weeks(batch_drafts: int, one_week_in: int) -> dict:
    """A batch of `batch_drafts` drafts in one week out of `one_week_in`, nothing in the other weeks."""
    ways = {x: math.comb(batch_drafts, x) for x in range(batch_drafts + 1)}
    ways[0] += (one_week_in - 1) * 2 ** batch_drafts
    return {"ways": ways, "total": one_week_in * 2 ** batch_drafts}


def listed_weeks(ways: dict) -> dict:
    """A weekly output given as a table: output -> number of equally likely ways."""
    return {"ways": {int(output): count for output, count in ways.items()}, "total": sum(ways.values())}


def moments(weekly: dict) -> tuple[Fraction, Fraction]:
    """Mean and variance of one week's output."""
    total = weekly["total"]
    mean = Fraction(sum(x * ways for x, ways in weekly["ways"].items()), total)
    square = Fraction(sum(x * x * ways for x, ways in weekly["ways"].items()), total)
    return mean, square - mean * mean


def at_most(weekly: dict, limit: int) -> Fraction:
    """Probability that one week's output is at most `limit`."""
    return Fraction(sum(ways for x, ways in weekly["ways"].items() if x <= limit), weekly["total"])


def behind_at(drafts: int, planned: int, week: int, shortfall: int) -> Fraction:
    """One look at a coin plan: probability that the cumulative shortfall at the end of `week` is at least
    `shortfall`. The cumulative output is the number of heads among drafts * week coins: a binomial tail."""
    flips = drafts * week
    return Fraction(sum(math.comb(flips, heads) for heads in range(planned * week - shortfall + 1)), 2 ** flips)


# --- alarm rules: a move returns the new silent state, or None when the alarm is raised ---------------------

def free_rule(planned: int):
    """No alarm at all: the state is the cumulative shortfall."""
    return lambda state, output, week: state + planned - output


def limit_rule(limit: int):
    """Alarm at the end of a week whose output is at most `limit`."""
    return lambda state, output, week: None if output <= limit else 0


def tolerance_rule(tolerance: int, planned: int):
    """Alarm when the cumulative shortfall is at least `tolerance`."""
    def move(state, output, week):
        shortfall = state + planned - output
        return None if shortfall >= tolerance else shortfall
    return move


def band_rule(limits: list, planned: int):
    """Alarm when the cumulative shortfall at the end of week t is at least limits[t]."""
    def move(state, output, week):
        shortfall = state + planned - output
        return None if shortfall >= limits[week] else shortfall
    return move


def cusum_rule(reference: int, interval: int, planned: int):
    """Page's scheme in its recursive form: C = max(0, C + shortfall - reference), alarm when C >= interval."""
    def move(state, output, week):
        total = max(0, state + planned - output - reference)
        return None if total >= interval else total
    return move


def band_limits(z: Fraction, variance: Fraction, weeks: int) -> list:
    """limits[t] = the smallest whole shortfall that is more than z standard deviations at week t:
    the smallest D with D^2 > z^2 * variance * t, found with whole-number square roots."""
    return [None] + [math.isqrt(math.floor(z * z * variance * week)) + 1 for week in range(1, weeks + 1)]


# --- the exact recursion ------------------------------------------------------------------------------------

def one_week(silent: dict, weekly: dict, move, week: int) -> dict:
    """Histories still silent after one more week: every silent state meets every possible output."""
    after, alarmed = {}, 0
    for state, count in silent.items():
        for output, ways in weekly["ways"].items():
            new = move(state, output, week)
            if new is None:
                alarmed += count * ways
            else:
                after[new] = after.get(new, 0) + count * ways
    check("accounting: histories still silent + histories with an alarm this week = histories silent before x ways",
          sum(after.values()) + alarmed == sum(silent.values()) * weekly["total"])
    return after


def silent_curve(move, weekly: dict, weeks: int, snapshot: int | None = None, hopeless=None) -> tuple[list, dict]:
    """Exact probability that the rule is still silent after week t, for t = 0..weeks.

    Also returns the silent states (state -> number of histories) at week `snapshot`, or at the end.
    `hopeless(state, weeks_left)`, when given, names states from which no alarm can come before the horizon:
    their histories are counted once as silent and no longer followed (the returned states then omit them).
    """
    silent, possible, safe = {0: 1}, 1, 0
    curve, kept = [Fraction(1)], {0: 1}
    for week in range(1, weeks + 1):
        silent = one_week(silent, weekly, move, week)
        possible *= weekly["total"]
        safe *= weekly["total"]
        if hopeless:
            for state in [s for s in silent if hopeless(s, weeks - week)]:
                safe += silent.pop(state)
        curve.append(Fraction(sum(silent.values()) + safe, possible))
        if week == snapshot:
            kept = dict(silent)
    return curve, (kept if snapshot is not None else silent)


def alarm_probability(move, weekly: dict, weeks: int, hopeless=None) -> Fraction:
    """Exact probability of at least one alarm in weeks 1..weeks."""
    return 1 - silent_curve(move, weekly, weeks, hopeless=hopeless)[0][-1]


def delay_tail(move, slow: dict, at_change: dict, stop_below: Fraction) -> list:
    """P(delay > d) for d = 0, 1, 2, ...: the share of the histories silent at the change that are still silent
    after d slow weeks. Stops once that share is below `stop_below`."""
    silent, possible = dict(at_change), sum(at_change.values())
    tail = [Fraction(1)]
    while tail[-1] >= stop_below:
        silent = one_week(silent, slow, move, 0)
        possible *= slow["total"]
        tail.append(Fraction(sum(silent.values()), possible))
    return tail


def quantile(tail: list, level: Fraction) -> int:
    """Smallest d with P(delay <= d) >= level."""
    return next(d for d, beyond in enumerate(tail) if 1 - beyond >= level)


def run_lengths(move, weekly: dict, states: list) -> dict:
    """Average run length from each silent state: L(s) = 1 + sum over outputs of P(output) * L(next state),
    with L = 0 once the alarm is raised. Solved exactly by elimination on fractions."""
    index = {state: i for i, state in enumerate(states)}
    rows = []
    for state in states:
        row = [Fraction(0)] * len(states) + [Fraction(1)]
        row[index[state]] += 1
        for output, ways in weekly["ways"].items():
            new = move(state, output, 0)
            if new is not None:
                row[index[new]] -= Fraction(ways, weekly["total"])
        rows.append(row)
    for i in range(len(rows)):
        pivot = next(r for r in range(i, len(rows)) if rows[r][i] != 0)
        rows[i], rows[pivot] = rows[pivot], rows[i]
        rows[i] = [value / rows[i][i] for value in rows[i]]
        for r in range(len(rows)):
            if r != i and rows[r][i] != 0:
                rows[r] = [a - rows[r][i] * b for a, b in zip(rows[r], rows[i])]
    return {state: rows[index[state]][-1] for state in states}


def smallest_threshold(alarm, low: int, high: int, target: Fraction) -> int:
    """Smallest whole threshold in [low, high] whose alarm probability is at most the target.
    The probability falls as the threshold rises, so the search halves the range."""
    check("calibration: the top of the search range meets the target", alarm(high) <= target)
    while low < high:
        middle = (low + high) // 2
        if alarm(middle) <= target:
            high = middle
        else:
            low = middle + 1
    return low


# --- sampling error of a simulated share ---------------------------------------------------------------------

def binomial_tails(k: int, n: int, p: float) -> tuple[float, float]:
    """P(X <= k) and P(X >= k) for X ~ Binomial(n, p).

    The probabilities are built outward from the mode with the ratio P(j+1)/P(j) = (n-j)/(j+1) * p/(1-p) and
    then normalised: only + - * / are used. Terms below 1e-25 of the largest are dropped.
    """
    odds = p / (1.0 - p)
    mode = min(n, int((n + 1) * p))
    weights = {mode: 1.0}
    weight, j = 1.0, mode
    while j < n and weight > 1e-25:
        weight = weight * (n - j) / (j + 1) * odds
        j += 1
        weights[j] = weight
    weight, j = 1.0, mode
    while j > 0 and weight > 1e-25:
        weight = weight * j / (n - j + 1) / odds
        j -= 1
        weights[j] = weight
    total = math.fsum(weights.values())
    lower = math.fsum(w for j, w in weights.items() if j <= k) / total
    upper = math.fsum(w for j, w in weights.items() if j >= k) / total
    return lower, upper


def clopper_pearson(k: int, n: int, alpha: float) -> tuple[float, float]:
    """Exact two-sided interval for a share of k in n (the interval PSY-004 builds).

    Lower limit: the p at which P(X >= k) = alpha/2. Upper limit: the p at which P(X <= k) = alpha/2.
    Each is found by 45 halvings of the range from 0 to 1.
    """
    def root(too_low) -> float:
        low, high = 0.0, 1.0
        for _ in range(45):
            middle = (low + high) / 2.0
            if too_low(middle):
                low = middle
            else:
                high = middle
        return (low + high) / 2.0
    lower = 0.0 if k == 0 else root(lambda p: binomial_tails(k, n, p)[1] < alpha / 2.0)
    upper = 1.0 if k == n else root(lambda p: binomial_tails(k, n, p)[0] > alpha / 2.0)
    return lower, upper


def share_row(label: str, count: int, runs: int, exact: Fraction | None, sim: dict) -> dict:
    """A simulated share with its binomial standard error, its exact 95% interval and, where an exact probability
    exists, its distance from that probability in standard errors (computed from the exact probability)."""
    low, high = clopper_pearson(count, runs, 1.0 - float(sim["level"]))
    error = math.sqrt(float(Fraction(count * (runs - count), runs ** 3)))  # sqrt(share * (1 - share) / runs)
    row = {"alarms": count, "runs": runs, "share": rnd(Fraction(count, runs), "probability"),
           "standard_error": rnd(error, "probability"), "interval_95": [rnd(low, "probability"), rnd(high, "probability")]}
    if exact is None:
        return row
    expected = exact * runs
    spread = math.sqrt(float(expected * (1 - exact)))  # standard deviation of the count of alarms
    distance = (count - float(expected)) / spread if spread > 0 else 0.0
    covers = low <= float(exact) <= high
    testable = min(expected, runs - expected) >= sim["needs"]
    AGREEMENT.append({"what": label, "kind": "share", "distance": distance, "covers": covers, "testable": testable})
    row |= {"exact": rnd(exact, "probability"), "standard_errors_from_exact": rnd(distance, "score"),
            "interval_covers_exact": covers}
    return row


def mean_row(label: str, cell: dict, exact: Fraction) -> dict:
    """A simulated mean delay with its standard error and its distance from the exact mean."""
    used, total, squares = cell["used"], cell["sum"], cell["squares"]
    variance = Fraction(used * squares - total * total, used * (used - 1))
    error = math.sqrt(float(variance / used))
    distance = (total / used - float(exact)) / error
    AGREEMENT.append({"what": label, "kind": "mean", "distance": distance, "covers": abs(distance) <= 1.96,
                      "testable": True})
    return {"runs_with_an_earlier_alarm": cell["early"], "runs_silent_at_the_change": used,
            "mean_delay_weeks": rnd(Fraction(total, used), "weeks"), "standard_error": rnd(error, "weeks"),
            "standard_errors_from_exact": rnd(distance, "score")}


# --- the simulation -------------------------------------------------------------------------------------------

def coin_draw(drafts: int):
    """One week of `drafts` fair coins: the top bits of one random() draw, counted."""
    scale = 1 << drafts
    if drafts <= 10:
        return lambda rng: ONES[int(rng.random() * scale)]
    return lambda rng: bin(int(rng.random() * scale)).count("1")


def batch_draw(batch_drafts: int, one_week_in: int):
    inner = coin_draw(batch_drafts)
    return lambda rng: inner(rng) if int(rng.random() * one_week_in) == 0 else 0


def simulate_plan(draw, model: dict, runs: int, seed: int) -> dict:
    """Whole plans without a slowdown. Per run: the first week's output, the lowest weekly output, the highest
    cumulative shortfall, the highest value of Page's sum in its two forms, and the prediction bands crossed.
    Returned as counts of runs."""
    rng = random.Random(seed)
    planned, reference, weeks, bands = model["planned"], model["reference"], model["weeks"], model["band_limits"]
    tally = {"first_week": {}, "lowest": {}, "shortfall": {}, "cusum": {}, "band": [0] * len(bands), "forms_differ": 0}
    for _ in range(runs):
        first = low = None
        shortfall = top = cusum = cusum_top = total = lowest_total = page_top = 0
        crossed = [False] * len(bands)
        for week in range(1, weeks + 1):
            output = draw(rng)
            if week == 1:
                first = low = output
            elif output < low:
                low = output
            shortfall += planned - output
            if shortfall > top:
                top = shortfall
            score = planned - output - reference
            cusum = max(0, cusum + score)  # the recursive form
            if cusum > cusum_top:
                cusum_top = cusum
            total += score  # Page's form: the sum of the scores against its lowest earlier value
            if total - lowest_total > page_top:
                page_top = total - lowest_total
            if total < lowest_total:
                lowest_total = total
            if shortfall >= bands[0][week]:
                for i, limits in enumerate(bands):
                    crossed[i] = crossed[i] or shortfall >= limits[week]
        for key, value in (("first_week", first), ("lowest", low), ("shortfall", top), ("cusum", cusum_top)):
            tally[key][value] = tally[key].get(value, 0) + 1
        tally["forms_differ"] += page_top != cusum_top
        for i, flag in enumerate(crossed):
            tally["band"][i] += flag
    return tally


def first_alarms(rng, model: dict, lists: dict, max_weeks: int) -> dict:
    """One run with the slowdown: the week of the first alarm of every listed rule (thresholds ascending).
    The run goes on, past the end of the plan if need be, until every rule has fired."""
    limits, tolerances, intervals = lists["limit"], lists["tolerance"], lists["cusum"]
    planned, reference, change = model["planned"], model["reference"], model["change"]
    draws = (model["draw"], model["slow_draw"])
    fired = {"limit": [None] * len(limits), "tolerance": [], "cusum": [], "page": []}
    waiting = len(limits)
    shortfall = cusum = total = lowest_total = week = 0
    while waiting or len(fired["tolerance"]) < len(tolerances) or len(fired["page"]) < len(intervals) \
            or len(fired["cusum"]) < len(intervals):
        week += 1
        if week > max_weeks:
            raise ArithmeticError(f"a simulated run was still silent after {max_weeks} weeks")
        output = draws[week >= change](rng)
        for i, limit in enumerate(limits):
            if fired["limit"][i] is None and output <= limit:
                fired["limit"][i] = week
                waiting -= 1
        shortfall += planned - output
        while len(fired["tolerance"]) < len(tolerances) and shortfall >= tolerances[len(fired["tolerance"])]:
            fired["tolerance"].append(week)
        score = planned - output - reference
        cusum = max(0, cusum + score)
        while len(fired["cusum"]) < len(intervals) and cusum >= intervals[len(fired["cusum"])]:
            fired["cusum"].append(week)
        total += score
        while len(fired["page"]) < len(intervals) and total - lowest_total >= intervals[len(fired["page"])]:
            fired["page"].append(week)
        lowest_total = min(lowest_total, total)
    return fired


def simulate_slowdown(model: dict, lists: dict, runs: int, seed: int, max_weeks: int) -> dict:
    """Runs with the slowdown. Per rule and threshold: runs with an alarm before the slowdown (set aside), and the
    count, sum and sum of squares of the delays of the others."""
    rng = random.Random(seed)
    stats = {kind: [{"early": 0, "used": 0, "sum": 0, "squares": 0} for _ in thresholds]
             for kind, thresholds in lists.items()}
    differ = 0
    for _ in range(runs):
        fired = first_alarms(rng, model, lists, max_weeks)
        differ += fired["page"] != fired["cusum"]
        for kind in lists:
            for cell, week in zip(stats[kind], fired[kind]):
                delay = week - model["change"] + 1
                if delay < 1:
                    cell["early"] += 1
                else:
                    cell["used"] += 1
                    cell["sum"] += delay
                    cell["squares"] += delay * delay
    stats["forms_differ"] = differ
    return stats


def at_least(tally: dict, threshold: int) -> int:
    """Runs whose recorded highest value reached the threshold."""
    return sum(count for value, count in tally.items() if value >= threshold)


# --- the model and its exact figures ------------------------------------------------------------------------

def build_model(sc: dict) -> dict:
    plan, rules, slow, sim = sc["plan"], sc["rules"], sc["slowdown"], sc["simulation"]
    planned, drafts = plan["planned_weekly_output"], sc["weekly_output"]["drafts_in_work"]
    total = plan["departments"] * plan["courses_per_department"]
    on_plan = coin_weeks(drafts)
    mean, variance = moments(on_plan)
    if mean != planned or total % planned:
        raise ValueError("the planned weekly output must be the mean output and divide the planned total")
    z_values = [Fraction(z) for z in rules["prediction_band"]["z_values"]]
    if z_values != sorted(z_values):
        raise ValueError("the z values of the prediction band must ascend")
    return {
        "planned": planned, "total": total, "weeks": total // planned, "drafts": drafts, "on_plan": on_plan,
        "variance": variance, "slow_drafts": slow["drafts_in_work"], "slow": coin_weeks(slow["drafts_in_work"]),
        "change": slow["first_slow_week"], "reference": rules["cumulative_sum"]["reference_value"],
        "limits": rules["weekly_limit"]["limits"], "z_values": z_values,
        "band_limits": [band_limits(z, variance, max(sc["horizons_tabulated"])) for z in z_values],
        "target": Fraction(sc["calibration"]["false_alarm_probability_at_most"]),
        "stop_below": Fraction(sc["delay"]["stop_below"]), "quantile": Fraction(sc["delay"]["quantile"]),
        "horizons": sc["horizons_tabulated"], "draw": coin_draw(drafts), "slow_draw": coin_draw(slow["drafts_in_work"]),
        "sim": {"level": Fraction(sim["interval_level"]), "needs": sim["agreement_needs_expected_runs"]},
    }


def performance(model: dict, move, change: int | None = None, slow: dict | None = None) -> dict:
    """Exact figures for one rule: probability of an alarm by each tabulated week on plan, and the delay after a
    slowdown that starts in week `change` (as fractions)."""
    change = change or model["change"]
    weeks = max(model["weeks"], change - 1)
    curve, at_change = silent_curve(move, model["on_plan"], weeks, snapshot=change - 1)
    tail = delay_tail(move, slow or model["slow"], at_change, model["stop_below"])
    left = model["weeks"] - change + 1  # slow weeks before the plan ends
    return {"alarm_by": {t: 1 - curve[t] for t in model["horizons"] if t <= weeks},
            "silent_at_change": curve[change - 1], "mean_delay": sum(tail, Fraction(0)),
            "delay_quantile": quantile(tail, model["quantile"]),
            "unflagged_at_plan_end": tail[left] if left < len(tail) else Fraction(0)}


def exact_figures(model: dict, sc: dict) -> dict:
    """Calibrate the two cumulative rules, then compute the exact figures of every tabulated threshold."""
    planned, reference, rules = model["planned"], model["reference"], sc["rules"]
    makers = {"tolerance": lambda c: tolerance_rule(c, planned), "cusum": lambda h: cusum_rule(reference, h, planned)}
    figures = {"calibrated": {}, "one_lower": {}}
    for kind, section in (("tolerance", "tolerance"), ("cusum", "cumulative_sum")):
        cache: dict[int, Fraction] = {}

        def alarm(threshold: int, kind=kind, cache=cache) -> Fraction:
            if threshold not in cache:
                cache[threshold] = alarm_probability(makers[kind](threshold), model["on_plan"], model["weeks"])
            return cache[threshold]
        best = smallest_threshold(alarm, *rules[section]["search_range"], model["target"])
        check("calibration: the threshold found meets the target and the next lower one does not",
              alarm(best) <= model["target"] < alarm(best - 1), f"{kind} {best}")
        figures["calibrated"][kind], figures["one_lower"][kind] = best, alarm(best - 1)
        wanted = sorted(set(rules[section]["tabulated"]) | {best})
        if kind == "cusum":
            wanted = sorted(set(wanted) | set(range(1, max(wanted) + 1)))
        figures[kind] = {threshold: performance(model, makers[kind](threshold)) for threshold in wanted}
        check("calibration: the search and the table give the same probability",
              figures[kind][best]["alarm_by"][model["weeks"]] == alarm(best))
    figures["limit"] = {limit: performance(model, limit_rule(limit)) for limit in model["limits"]}
    return figures


def run_simulations(model: dict, sc: dict, figures: dict) -> dict:
    sim, burst = sc["simulation"], sc["bursty_output"]
    lists = {"limit": model["limits"], "tolerance": sorted(figures["tolerance"]),
             "cusum": sorted(set(sc["rules"]["cumulative_sum"]["tabulated"]) | {figures["calibrated"]["cusum"]})}
    return {
        "lists": lists,
        "plan": simulate_plan(model["draw"], model, sim["on_plan"]["runs"], sim["on_plan"]["seed"]),
        "slow": simulate_slowdown(model, lists, sim["slowdown"]["runs"], sim["slowdown"]["seed"],
                                  sim["slowdown"]["max_weeks"]),
        "burst": simulate_plan(batch_draw(burst["batch_drafts"], burst["one_week_in"]), model,
                               sim["bursty"]["runs"], sim["bursty"]["seed"]),
    }


# --- sections of results.json ---------------------------------------------------------------------------------

def plan_section(model: dict, sc: dict) -> dict:
    mean_slow, variance_slow = moments(model["slow"])
    deviation = math.sqrt(float(model["variance"]))
    return {
        "note": sc["plan"]["note"],
        "departments": sc["plan"]["departments"], "courses_per_department": sc["plan"]["courses_per_department"],
        "courses_planned": model["total"], "planned_weekly_output": model["planned"], "weeks": model["weeks"],
        "on_plan_week": {"drafts_in_work": model["drafts"], "histories": model["on_plan"]["total"],
                         "ways_by_output": {str(x): ways for x, ways in model["on_plan"]["ways"].items()},
                         "mean": rnd(Fraction(model["planned"]), "courses"), "variance": text(model["variance"]),
                         "standard_deviation": rnd(deviation, "courses")},
        "slow_week": {"drafts_in_work": model["slow_drafts"], "histories": model["slow"]["total"],
                      "ways_by_output": {str(x): ways for x, ways in model["slow"]["ways"].items()},
                      "mean": rnd(mean_slow, "courses"), "variance": text(variance_slow),
                      "share_of_planned_output": rnd(mean_slow / model["planned"], "courses"),
                      "courses_lost_per_week": rnd(model["planned"] - mean_slow, "courses"),
                      "first_slow_week": model["change"], "slow_weeks_inside_the_plan": model["weeks"] - model["change"] + 1},
        "cumulative_standard_deviation_by_week": {
            str(t): rnd(math.sqrt(float(model["variance"] * t)), "courses")
            for t in sorted(set(sc["rules"]["prediction_band"]["single_look_weeks"]) | {sc["worked_examples"]["band_week"]})},
    }


def single_look_section(model: dict, sc: dict, sims: dict) -> dict:
    """One look, no simulation needed: a count of coin histories. The simulation is then checked against it."""
    band, runs = sc["rules"]["prediction_band"], sc["simulation"]["on_plan"]["runs"]
    weekly = []
    for limit in model["limits"]:
        chance = at_most(model["on_plan"], limit)
        count = at_least({-x: n for x, n in sims["plan"]["first_week"].items()}, -limit)
        weekly.append({"limit": limit, "histories": int(chance * model["on_plan"]["total"]),
                       "out_of": model["on_plan"]["total"], "probability": rnd(chance, "probability"),
                       "simulated_first_week": share_row(f"first week, output <= {limit}", count, runs, chance, model["sim"])})
    bands = []
    for z, limits in zip(model["z_values"], model["band_limits"]):
        looks = [behind_at(model["drafts"], model["planned"], t, limits[t]) for t in range(1, model["weeks"] + 1)]
        bands.append({"z": text(z), "by_week": [{"week": t, "band_width_courses": rnd(float(z) * math.sqrt(float(model["variance"] * t)), "courses"),
                                                   "alarm_from_shortfall": limits[t], "probability": rnd(looks[t - 1], "probability")}
                                                  for t in band["single_look_weeks"]],
                      "lowest_single_look": rnd(min(looks), "probability"), "highest_single_look": rnd(max(looks), "probability"),
                      "_looks": looks})
    week = band["single_look_weeks"][2]
    _, states = silent_curve(free_rule(model["planned"]), model["on_plan"], week)
    recount = Fraction(at_least(states, model["band_limits"][0][week]), model["on_plan"]["total"] ** week)
    check("known answer: the recursion without an alarm reproduces the binomial tail of one look",
          recount == behind_at(model["drafts"], model["planned"], week, model["band_limits"][0][week]))
    normal = band["normal_tail_beyond_two_standard_deviations"]
    check("quoted constant: the normal tail beyond 2 standard deviations", abs(0.5 * math.erfc(math.sqrt(2.0)) - normal) < 1e-5)
    return {"definition": "Probability that a rule fires at ONE week-end chosen in advance, on plan. Counted exactly; "
                          "the simulated share is the same event in the first week of each simulated plan.",
            "weekly_limit": weekly, "prediction_band": bands, "normal_tail_beyond_two_standard_deviations": normal}


def needed_weekly_chance(target: Fraction, weeks: int) -> float:
    """The per-week alarm probability a at which 1 - (1 - a)^weeks equals the target, by 60 halvings
    (the power is a product of `weeks` factors, so no library power function is used)."""
    low, high = 0.0, 1.0
    for _ in range(60):
        middle = (low + high) / 2.0
        silent = 1.0
        for _ in range(weeks):
            silent *= 1.0 - middle
        if 1.0 - silent < float(target):
            low = middle
        else:
            high = middle
    return (low + high) / 2.0


def weekly_limit_section(model: dict, sc: dict, figures: dict, sims: dict) -> dict:
    """The weekly limit: independent looks, so everything has a closed form that the recursion must match."""
    weeks, runs = model["weeks"], sc["simulation"]["on_plan"]["runs"]
    rows = []
    for i, limit in enumerate(model["limits"]):
        chance, slow_chance, facts = at_most(model["on_plan"], limit), at_most(model["slow"], limit), figures["limit"][limit]
        closed = {t: 1 - (1 - chance) ** t for t in facts["alarm_by"]}
        check("known answer: the recursion equals 1 - (1 - a)^T for the weekly limit", closed == facts["alarm_by"])
        check("known answer: the mean delay of the weekly limit is 1 / (chance of a slow week at or under the limit)",
              abs(facts["mean_delay"] - 1 / slow_chance) < Fraction(1, 10 ** 12))
        count = at_least({-x: n for x, n in sims["plan"]["lowest"].items()}, -limit)
        rows.append({
            "limit": limit, "alarm_chance_per_week_on_plan": text(chance),
            "average_run_length_on_plan_weeks": rnd(1 / chance, "weeks"),
            "alarm_by_week": {str(t): rnd(p, "probability") for t, p in closed.items()},
            "simulated_plan": share_row(f"weekly limit {limit}, plan", count, runs, closed[weeks], model["sim"]),
            "alarm_chance_per_slow_week": text(slow_chance), "mean_delay_weeks": rnd(1 / slow_chance, "weeks"),
            "delay_not_exceeded_in_90_percent": facts["delay_quantile"],
            "unflagged_at_plan_end": rnd(facts["unflagged_at_plan_end"], "probability"),
            "simulated_delay": mean_row(f"weekly limit {limit}, delay", sims["slow"]["limit"][i], facts["mean_delay"]),
        })
    needed = needed_weekly_chance(model["target"], weeks)
    strictest = at_most(model["on_plan"], 0)
    return {"formula": "P(at least one alarm in T weeks) = 1 - (1 - a)^T, a = alarm chance of one on-plan week; "
                       "average run length = 1 / a; mean delay = 1 / (alarm chance of one slow week)",
            "rows": rows,
            "per_week_chance_needed_for_the_target": {"target": text(model["target"]), "weeks": weeks,
                                                      "chance": rnd(needed, "probability"),
                                                      "strictest_limit_chance": rnd(strictest, "probability"),
                                                      "reachable_with_a_weekly_limit": float(strictest) <= needed}}


def band_section(model: dict, sc: dict, looks: list, sims: dict) -> dict:
    """The prediction band checked every week: dependent looks, no closed form, an exact recursion."""
    weeks, runs = model["weeks"], sc["simulation"]["on_plan"]["runs"]
    rows = []
    for i, (z, limits) in enumerate(zip(model["z_values"], model["band_limits"])):
        curve, _ = silent_curve(band_rule(limits, model["planned"]), model["on_plan"], max(model["horizons"]))
        alarm, single = 1 - curve[weeks], looks[i]
        check("bounds: largest single look <= P(at least one alarm) <= sum of the single looks",
              max(single) <= alarm <= sum(single))
        rows.append({"z": text(z), "alarm_by_week": {str(t): rnd(1 - curve[t], "probability") for t in model["horizons"]},
                     "largest_single_look": rnd(max(single), "probability"),
                     "sum_of_single_looks": rnd(sum(single), "probability"),
                     "alarm_over_largest_single_look": rnd(alarm / max(single), "score"),
                     "simulated_plan": share_row(f"band z = {text(z)}, plan", sims["plan"]["band"][i], runs, alarm, model["sim"])})
    return {"definition": "Alarm at the first week-end at which the cumulative shortfall is more than z standard "
                          "deviations of the on-plan cumulative output. The looks share their history, so "
                          "1 - (1 - a)^T does not apply; the sum of the single looks is only an upper bound.",
            "rows": rows}


def rule_row(model: dict, label: str, threshold: int, facts: dict, plan_count: int, cell: dict, runs: int) -> dict:
    """One threshold of a cumulative rule: exact figures next to the simulated ones."""
    weeks = model["weeks"]
    return {
        "threshold": threshold, "calibrated": threshold == model["calibrated"][label],
        "alarm_by_week": {str(t): rnd(p, "probability") for t, p in facts["alarm_by"].items()},
        "simulated_plan": share_row(f"{label} {threshold}, plan", plan_count, runs, facts["alarm_by"][weeks], model["sim"]),
        "silent_at_the_change": rnd(facts["silent_at_change"], "probability"),
        "mean_delay_weeks": rnd(facts["mean_delay"], "weeks"),
        "delay_not_exceeded_in_90_percent": facts["delay_quantile"],
        "unflagged_at_plan_end": rnd(facts["unflagged_at_plan_end"], "probability"),
        "simulated_delay": mean_row(f"{label} {threshold}, delay", cell, facts["mean_delay"]),
    }


def tolerance_section(model: dict, sc: dict, figures: dict, sims: dict) -> dict:
    runs, best = sc["simulation"]["on_plan"]["runs"], figures["calibrated"]["tolerance"]
    rows = [rule_row(model, "tolerance", c, figures["tolerance"][c], at_least(sims["plan"]["shortfall"], c),
                     sims["slow"]["tolerance"][i], runs) for i, c in enumerate(sims["lists"]["tolerance"])]
    check("the table holds the calibrated threshold", sum(row["calibrated"] for row in rows) == 1)
    long_run = max(model["horizons"])
    move = tolerance_rule(best, model["planned"])

    def hopeless(state: int, weeks_left: int) -> bool:
        """The shortfall rises by at most the planned output in a week."""
        return state + model["planned"] * weeks_left < best
    longer = alarm_probability(move, model["on_plan"], long_run, hopeless=hopeless)
    alarm = figures["tolerance"][best]["alarm_by"][model["weeks"]]
    check("pruning: dropping states that can no longer fire leaves the alarm probability unchanged",
          alarm_probability(move, model["on_plan"], model["weeks"], hopeless=hopeless) == alarm)
    looks = [behind_at(model["drafts"], model["planned"], t, best) for t in range(1, model["weeks"] + 1)]
    check("bounds: last single look <= P(at least one alarm) <= sum of the single looks", looks[-1] <= alarm <= sum(looks))
    return {"definition": sc["rules"]["tolerance"]["note"],
            "calibrated_tolerance": best,
            "calibrated_in_weeks_of_planned_output": rnd(Fraction(best, model["planned"]), "courses"),
            "calibrated_in_final_standard_deviations": rnd(best / math.sqrt(float(model["variance"] * model["weeks"])), "courses"),
            "alarm_one_course_lower": rnd(figures["one_lower"]["tolerance"], "probability"),
            "calibrated_single_look_in_the_last_week": rnd(looks[-1], "probability"),
            "calibrated_alarm_over_that_single_look": rnd(alarm / looks[-1], "score"),
            "calibrated_alarm_by_a_longer_plan": {"weeks": long_run, "probability": rnd(longer, "probability")},
            "rows": rows}


def cusum_section(model: dict, sc: dict, figures: dict, sims: dict) -> dict:
    runs, best, reference = sc["simulation"]["on_plan"]["runs"], figures["calibrated"]["cusum"], model["reference"]
    rows = []
    for i, h in enumerate(sims["lists"]["cusum"]):
        move, states = cusum_rule(reference, h, model["planned"]), list(range(h))
        on_plan, slow = run_lengths(move, model["on_plan"], states), run_lengths(move, model["slow"], states)
        row = rule_row(model, "cusum", h, figures["cusum"][h], at_least(sims["plan"]["cusum"], h),
                       sims["slow"]["cusum"][i], runs)
        row |= {"average_run_length_on_plan_weeks": rnd(on_plan[0], "weeks"),
                "average_run_length_after_the_slowdown_from_zero_weeks": rnd(slow[0], "weeks")}
        rows.append(row)
        _, at_change = silent_curve(move, model["on_plan"], model["change"] - 1)
        weighted = sum(count * slow[state] for state, count in at_change.items()) / sum(at_change.values())
        check("two exact routes: the mean delay from the week-by-week recursion equals the one from run lengths",
              abs(weighted - figures["cusum"][h]["mean_delay"]) < Fraction(1, 10 ** 12), f"interval {h}")
    long_run = max(model["horizons"])
    longer = alarm_probability(cusum_rule(reference, best, model["planned"]), model["on_plan"], long_run)
    return {"definition": sc["rules"]["cumulative_sum"]["note"],
            "recursion": "C(0) = 0; C(t) = max(0, C(t-1) + planned - output(t) - reference_value); alarm when C(t) >= decision interval",
            "reference_value": reference, "calibrated_decision_interval": best,
            "alarm_one_lower": rnd(figures["one_lower"]["cusum"], "probability"),
            "calibrated_alarm_by_a_longer_plan": {"weeks": long_run, "probability": rnd(longer, "probability")},
            "rows": rows}


def calibrated_moves(model: dict) -> dict:
    planned, best = model["planned"], model["calibrated"]
    return {"tolerance": tolerance_rule(best["tolerance"], planned),
            "cumulative_sum": cusum_rule(model["reference"], best["cusum"], planned)}


def change_week_section(model: dict, sc: dict) -> dict:
    """The same slowdown starting earlier or later: what the two calibrated rules remember."""
    weeks, best = model["weeks"], model["calibrated"]
    out = {"definition": "Exact, for the two calibrated rules. Delay = slow weeks seen when the alarm comes, among "
                         "runs silent when the slowdown starts.",
           "thresholds": {"tolerance": best["tolerance"], "cumulative_sum": best["cusum"]}}
    for name, move in calibrated_moves(model).items():
        rows = []
        for change in sorted(set(sc["slowdown"]["other_first_slow_weeks"]) | {model["change"]}):
            facts = performance(model, move, change)
            rows.append({"first_slow_week": change, "silent_at_the_change": rnd(facts["silent_at_change"], "probability"),
                         "mean_delay_weeks": rnd(facts["mean_delay"], "weeks"),
                         "delay_not_exceeded_in_90_percent": facts["delay_quantile"],
                         "slow_weeks_inside_the_plan": weeks - change + 1,
                         "unflagged_at_plan_end": rnd(facts["unflagged_at_plan_end"], "probability")})
        out[name] = rows
    return out


def milder_section(model: dict, sc: dict) -> dict:
    """A slowdown the cumulative sum was not tuned for: more drafts stay in work, so less is lost each week."""
    slow = coin_weeks(sc["slowdown"]["milder_drafts_in_work"])
    mean, variance = moments(slow)
    loss = model["planned"] - mean
    out = {"note": "Exact, for the two calibrated rules, slowdown from the same week as in the main tables.",
           "drafts_in_work": sc["slowdown"]["milder_drafts_in_work"], "mean_output": rnd(mean, "courses"),
           "share_of_planned_output": rnd(mean / model["planned"], "courses"), "courses_lost_per_week": rnd(loss, "courses"),
           "mean_weekly_score_of_the_cumulative_sum": rnd(loss - model["reference"], "courses"),
           "first_slow_week": model["change"]}
    for name, move in calibrated_moves(model).items():
        facts = performance(model, move, slow=slow)
        out[name] = {"mean_delay_weeks": rnd(facts["mean_delay"], "weeks"),
                     "delay_not_exceeded_in_90_percent": facts["delay_quantile"],
                     "unflagged_at_plan_end": rnd(facts["unflagged_at_plan_end"], "probability")}
    return out


def bursty_section(model: dict, sc: dict, figures: dict, sims: dict) -> dict:
    """Same mean output, delivered in batches: what the thresholds calibrated on steady output then do."""
    burst, runs, weeks, planned = sc["bursty_output"], sc["simulation"]["bursty"]["runs"], model["weeks"], model["planned"]
    weekly = batch_weeks(burst["batch_drafts"], burst["one_week_in"])
    mean, variance = moments(weekly)
    check("bursty output: the mean weekly output equals the planned one", mean == planned)
    c, h = figures["calibrated"]["tolerance"], figures["calibrated"]["cusum"]
    tolerance = alarm_probability(tolerance_rule(c, planned), weekly, weeks,
                                  hopeless=lambda state, left: state + planned * left < c)
    cusum = alarm_probability(cusum_rule(model["reference"], h, planned), weekly, weeks)
    return {
        "note": burst["note"], "mean": rnd(mean, "courses"), "variance": text(variance),
        "standard_deviation": rnd(math.sqrt(float(variance)), "courses"),
        "variance_over_steady_variance": rnd(variance / model["variance"], "courses"),
        "final_cumulative_standard_deviation": {"steady": rnd(math.sqrt(float(model["variance"] * weeks)), "courses"),
                                                "bursty": rnd(math.sqrt(float(variance * weeks)), "courses")},
        "chance_of_a_week_without_output": rnd(at_most(weekly, 0), "probability"),
        "calibrated_tolerance": {"threshold": c, "alarm_during_the_plan": rnd(tolerance, "probability"),
                                 "simulated": share_row("bursty, tolerance", at_least(sims["burst"]["shortfall"], c), runs, tolerance, model["sim"])},
        "calibrated_cumulative_sum": {"threshold": h, "alarm_during_the_plan": rnd(cusum, "probability"),
                                      "simulated": share_row("bursty, cumulative sum", at_least(sims["burst"]["cusum"], h), runs, cusum, model["sim"])},
    }


def cost_section(model: dict, sc: dict, figures: dict) -> dict:
    """Choosing the decision interval from assumed costs."""
    costs, weeks = sc["costs"], model["weeks"]
    slowdown, per_week = Fraction(costs["probability_of_a_slowdown"]), costs["slow_week_cost_courses"]
    tables = []
    for false_alarm in costs["false_alarm_cost_courses"]:
        rows = []
        for h, facts in sorted(figures["cusum"].items()):
            wolf = (1 - slowdown) * facts["alarm_by"][weeks] * false_alarm
            late = slowdown * facts["mean_delay"] * per_week
            rows.append({"decision_interval": h, "false_alarm_part": rnd(wolf, "cost"), "delay_part": rnd(late, "cost"),
                         "expected_cost_courses": rnd(wolf + late, "cost"), "_cost": wolf + late})
        best = min(rows, key=lambda row: row["_cost"])
        check("costs: the cheapest decision interval lies inside the tabulated range", rows[0] is not best and rows[-1] is not best)
        tables.append({"false_alarm_cost_courses": false_alarm, "cheapest_decision_interval": best["decision_interval"],
                       "cheapest_expected_cost_courses": best["expected_cost_courses"], "rows": rows})
    return {"note": costs["note"], "probability_of_a_slowdown": text(slowdown), "slow_week_cost_courses": per_week,
            "formula": "expected cost = (1 - q) * P(false alarm during the plan) * false-alarm cost + q * mean delay * cost of a slow week",
            "calibrated_decision_interval": figures["calibrated"]["cusum"], "tables": tables}


def hypothesis_test(model: dict, sc: dict, figures: dict) -> dict:
    """The thresholds were written before the first run; this only reports which of them hold."""
    limits, weeks = sc["hypothesis_thresholds"], model["weeks"]
    c, h = figures["calibrated"]["tolerance"], figures["calibrated"]["cusum"]
    weekly = figures["limit"][limits["weekly_limit"]]["alarm_by"][weeks]
    slow_tolerance, slow_cusum = figures["tolerance"][c]["mean_delay"], figures["cusum"][h]["mean_delay"]
    ratio = slow_cusum / slow_tolerance
    low_c, high_c = limits["calibrated_tolerance_between"]
    low_d, high_d = limits["tolerance_mean_delay_between_weeks"]
    low_r, high_r = (Fraction(x) for x in limits["cusum_delay_over_tolerance_delay_between"])
    parts = {
        "1_weekly_limit": {"limit": limits["weekly_limit"], "alarm_during_the_plan": rnd(weekly, "probability"),
                           "expected_more_than": limits["weekly_limit_alarm_probability_more_than"],
                           "holds": weekly > Fraction(limits["weekly_limit_alarm_probability_more_than"])},
        "2_tolerance": {"calibrated_tolerance": c, "expected_between": [low_c, high_c], "tolerance_holds": low_c <= c <= high_c,
                        "mean_delay_weeks": rnd(slow_tolerance, "weeks"), "expected_delay_between": [low_d, high_d],
                        "delay_holds": low_d <= slow_tolerance <= high_d},
        "3_cumulative_sum": {"calibrated_decision_interval": h, "expected_interval": limits["calibrated_decision_interval_expected"],
                             "interval_as_expected": h in limits["calibrated_decision_interval_expected"],
                             "mean_delay_weeks": rnd(slow_cusum, "weeks"), "delay_over_tolerance_delay": rnd(ratio, "courses"),
                             "expected_ratio_between": [text(low_r), text(high_r)], "ratio_holds": low_r <= ratio <= high_r},
    }
    parts["2_tolerance"]["holds"] = parts["2_tolerance"]["tolerance_holds"] and parts["2_tolerance"]["delay_holds"]
    parts["3_cumulative_sum"]["holds"] = parts["3_cumulative_sum"]["ratio_holds"]
    return {"note": limits["note"], "parts": parts, "every_part_holds": all(part["holds"] for part in parts.values())}


def record_paths(outputs: list, planned: int, reference: Fraction) -> tuple[list, list]:
    """Cumulative shortfall and Page's sum after each week of a record."""
    shortfalls, sums, shortfall, total = [], [], 0, Fraction(0)
    for output in outputs:
        shortfall += planned - output
        total = max(Fraction(0), total + planned - output - reference)
        shortfalls.append(shortfall)
        sums.append(total)
    return shortfalls, sums


def first_week(path: list, threshold) -> int | None:
    return next((week for week, value in enumerate(path, 1) if value >= threshold), None)


def cost_exercise(model: dict, sc: dict, figures: dict) -> dict:
    """Two decision intervals compared on cost. The rows and the first tie use the rounded figures of the tables, so
    that the answer can be checked by hand; the second tie uses the exact figures."""
    cfg, costs, weeks = sc["worked_examples"]["cost_exercise"], sc["costs"], model["weeks"]
    slowdown, per_week, price = Fraction(costs["probability_of_a_slowdown"]), costs["slow_week_cost_courses"], cfg["false_alarm_cost_courses"]
    wolf, late, rows = {}, {}, []
    for h in cfg["decision_intervals"]:
        wolf[h] = Fraction(str(rnd(figures["cusum"][h]["alarm_by"][weeks], "probability")))
        late[h] = Fraction(str(rnd(figures["cusum"][h]["mean_delay"], "weeks")))
        rows.append({"decision_interval": h, "false_alarm_probability": float(wolf[h]), "mean_delay_weeks": float(late[h]),
                     "expected_cost_courses": rnd((1 - slowdown) * wolf[h] * price + slowdown * late[h] * per_week, "cost")})
    low, high = cfg["decision_intervals"]

    def tie(alarm: dict, delay: dict) -> Fraction:
        return slowdown * per_week * (delay[high] - delay[low]) / ((1 - slowdown) * (alarm[low] - alarm[high]))
    exact_alarm = {h: figures["cusum"][h]["alarm_by"][weeks] for h in (low, high)}
    exact_delay = {h: figures["cusum"][h]["mean_delay"] for h in (low, high)}
    return {"false_alarm_cost_courses": price, "rows": rows,
            "false_alarm_cost_at_which_they_tie_from_the_rounded_table": rnd(tie(wolf, late), "cost"),
            "false_alarm_cost_at_which_they_tie_from_exact_figures": rnd(tie(exact_alarm, exact_delay), "cost"),
            "cheaper_below_the_tie": low, "cheaper_above_the_tie": high}


def worked_examples(model: dict, sc: dict, figures: dict) -> dict:
    """Figures the lesson's exercises show and that no other section holds."""
    cfg, planned, weeks = sc["worked_examples"], model["planned"], model["weeks"]
    c, h = figures["calibrated"]["tolerance"], figures["calibrated"]["cusum"]
    week = cfg["band_week"]
    deviation = math.sqrt(float(model["variance"] * week))
    limit = model["band_limits"][0][week]
    shortfalls, sums = record_paths(cfg["record"], planned, Fraction(model["reference"]))
    fired_c, fired_h = first_week(shortfalls, c), first_week(sums, h)
    slow_from = cfg["record_first_slow_week"]
    loss = planned - moments(model["slow"])[0]
    claim = cfg["claim_week"]
    return {
        "exercise_1": {"week": week, "planned_total": planned * week, "variance": text(model["variance"] * week),
                       "standard_deviation": rnd(deviation, "courses"), "two_standard_deviations": rnd(2 * deviation, "courses"),
                       "alarm_from_shortfall": limit, "alarm_at_or_below_total": planned * week - limit,
                       "probability_of_one_look": rnd(behind_at(model["drafts"], planned, week, limit), "probability")},
        "exercise_2": {"target_over_weeks": rnd(model["target"] / weeks, "probability")},
        "exercise_4": {"week": claim, "alarm_from_shortfall": model["band_limits"][0][claim],
                       "probability_of_that_one_look": rnd(behind_at(model["drafts"], planned, claim, model["band_limits"][0][claim]),
                                                           "probability")},
        "exercise_5": cost_exercise(model, sc, figures),
        "exercise_3": {"record": cfg["record"], "weekly_shortfall": [planned - x for x in cfg["record"]],
                       "cumulative_shortfall": shortfalls, "weekly_score": [planned - x - model["reference"] for x in cfg["record"]],
                       "cumulative_sum": [int(value) for value in sums], "tolerance": c, "decision_interval": h,
                       "tolerance_fires_in_week": fired_c, "cumulative_sum_fires_in_week": fired_h,
                       "first_slow_week": slow_from,
                       "slow_weeks_seen_by_the_cumulative_sum": None if fired_h is None else fired_h - slow_from + 1,
                       "shortfall_still_missing_for_the_tolerance": c - shortfalls[-1],
                       "further_weeks_at_the_slow_rate": rnd(Fraction(c - shortfalls[-1]) / loss, "weeks")},
    }


def controls(model: dict, sc: dict, figures: dict, sims: dict) -> dict:
    """Hand-computed cases, a closed form for the crossing probability, and comparisons that must fail."""
    hand, walk, bound = (sc["hand_cases"][key] for key in ("two_drafts", "one_step_walk", "zero_alarms_bound"))
    weekly, planned, weeks = coin_weeks(hand["drafts_in_work"]), hand["planned_weekly_output"], hand["weeks"]
    tolerance = alarm_probability(tolerance_rule(hand["tolerance"], planned), weekly, weeks)
    cusum = alarm_probability(cusum_rule(hand["cusum_reference_value"], hand["cusum_decision_interval"], planned), weekly, weeks)
    check("hand-computed case: 2 drafts, tolerance 2, 3 weeks gives 8 of 64 histories",
          tolerance == Fraction(hand["expected_tolerance_alarm"]))
    check("hand-computed case: 2 drafts, Page's sum with reference 0 and interval 2, 3 weeks gives 9 of 64 histories",
          cusum == Fraction(hand["expected_cusum_alarm"]))
    steps, level = walk["steps"], walk["level"]
    coin = coin_weeks(1)
    crossing = alarm_probability(lambda state, output, week: None if state + 1 - 2 * output >= level else state + 1 - 2 * output,
                                 coin, steps)
    ends = lambda least: Fraction(sum(math.comb(steps, tails) for tails in range(steps + 1) if steps - 2 * tails >= least), 2 ** steps)  # noqa: E731
    check("known answer: the recursion reproduces the reflection principle for a walk of single steps",
          crossing == ends(level) + ends(level + 1))
    upper = clopper_pearson(0, bound["runs"], 0.05)[1]
    silent = 1.0
    for _ in range(bound["runs"]):
        silent *= 1.0 - upper
    check("known answer: with 0 alarms in n runs the upper limit u of the exact interval solves (1 - u)^n = 0.025",
          abs(silent - 0.025) < 1e-9)
    c, runs = figures["calibrated"]["tolerance"], sc["simulation"]["on_plan"]["runs"]
    offset = sc["negative_controls"]["tolerance_offset"]
    wrong = alarm_probability(tolerance_rule(c - offset, model["planned"]), model["on_plan"], model["weeks"])
    count = at_least(sims["plan"]["shortfall"], c)
    distance = (count - float(wrong * runs)) / math.sqrt(float(wrong * runs * (1 - wrong)))
    limit = sc["simulation"]["agreement_within_standard_errors"]
    check("negative control: the simulation is told apart from the exact value of a tolerance two courses lower",
          abs(distance) > limit, f"{distance}")
    plan_fired, slow_runs = at_least(sims["plan"]["cusum"], figures["calibrated"]["cusum"]), sc["simulation"]["slowdown"]["runs"]
    check("Page's two forms: the same highest value in every on-plan run and the same alarm weeks in every slowdown run",
          sims["plan"]["forms_differ"] == 0 and sims["slow"]["forms_differ"] == 0 and plan_fired > 0)
    histories = weekly["total"] ** weeks
    return {
        "hand_computed_case": {"note": hand["note"], "histories": histories,
                               "histories_with_a_tolerance_alarm": int(tolerance * histories),
                               "histories_with_a_cumulative_sum_alarm": int(cusum * histories)},
        "reflection_principle": {"note": walk["note"], "steps": steps, "level": level, "recursion": text(crossing),
                                 "closed_form": text(ends(level) + ends(level + 1)), "single_look_at_the_end": text(ends(level))},
        "zero_alarms_interval": {"runs": bound["runs"], "upper_limit": rnd(upper, "probability")},
        "wrong_tolerance": {"simulated_tolerance": c, "compared_with_exact_tolerance": c - offset,
                            "exact_probability_of_the_wrong_tolerance": rnd(wrong, "probability"),
                            "standard_errors_apart": rnd(distance, "score"), "told_apart": abs(distance) > limit},
        "pages_two_forms": {"on_plan_runs_compared": runs, "on_plan_runs_where_they_differ": sims["plan"]["forms_differ"],
                            "on_plan_runs_with_an_alarm_at_the_calibrated_interval": plan_fired,
                            "slowdown_runs_compared": slow_runs, "slowdown_runs_where_an_alarm_week_differs": sims["slow"]["forms_differ"]},
    }


def agreement_summary(sc: dict) -> dict:
    """How the simulated figures sit around the exact ones."""
    limit = sc["simulation"]["agreement_within_standard_errors"]
    testable = [item for item in AGREEMENT if item["testable"]]
    worst = max(testable, key=lambda item: abs(item["distance"]))
    check(f"simulation against exact: every comparable figure is within {limit} standard errors",
          abs(worst["distance"]) <= limit, f"{worst['what']}: {worst['distance']}")
    shares = [item for item in AGREEMENT if item["kind"] == "share"]
    means = [item for item in AGREEMENT if item["kind"] == "mean"]
    return {"note": "The simulation uses three seeded sets of runs, so these comparisons are not independent of one "
                    "another. About 1 comparison in 20 is expected outside its 95% range by chance.",
            "shares_compared": len(shares), "shares_whose_95_interval_covers_the_exact_value": sum(item["covers"] for item in shares),
            "means_compared": len(means), "means_within_1.96_standard_errors": sum(item["covers"] for item in means),
            "comparisons_with_enough_expected_runs": len(testable),
            "largest_distance_in_standard_errors": {"what": worst["what"], "distance": rnd(worst["distance"], "score")},
            "limit_in_standard_errors": limit}


def transfer_task(task: dict) -> dict:
    """Expected answers of the learner task: a small team whose histories can be counted by hand."""
    weekly, slow = listed_weeks(task["weekly_output_ways"]), listed_weeks(task["slow_output_ways"])
    planned, weeks, limit, tolerance = task["planned_weekly_output"], task["weeks"], task["weekly_limit"], task["tolerance"]
    mean, variance = moments(weekly)
    check("transfer task: the planned output is the mean output", mean == planned)
    histories = weekly["total"] ** weeks
    looks = []
    for week in range(1, weeks + 1):
        _, states = silent_curve(free_rule(planned), weekly, week)
        looks.append(Fraction(at_least(states, tolerance), weekly["total"] ** week))
    crossing = alarm_probability(tolerance_rule(tolerance, planned), weekly, weeks)
    check("transfer task: single look <= crossing probability <= sum of the single looks", looks[-1] <= crossing <= sum(looks))
    chance, slow_chance = at_most(weekly, limit), at_most(slow, limit)
    reference = Fraction(task["cusum_reference_value"])
    shortfalls, sums = record_paths(task["record"], planned, reference)
    fired_c, fired_h = first_week(shortfalls, tolerance), first_week(sums, task["cusum_decision_interval"])
    slow_from = task["record_first_slow_week"]
    return {
        "note": task["note"],
        "q1_one_look": {"variance_per_week": text(variance), "weeks": weeks,
                        "standard_deviation_after_the_weeks": rnd(math.sqrt(float(variance * weeks)), "courses"),
                        "histories": histories, "histories_at_least_the_tolerance_behind": int(looks[-1] * histories),
                        "probability": rnd(looks[-1], "probability")},
        "q2_weekly_limit": {"alarm_chance_per_week": text(chance), "average_run_length_weeks": rnd(1 / chance, "weeks"),
                            "alarm_within_the_weeks": text(1 - (1 - chance) ** weeks),
                            "alarm_within_the_weeks_value": rnd(1 - (1 - chance) ** weeks, "probability"),
                            "long_horizon_weeks": task["long_horizon_weeks"],
                            "alarm_within_the_long_horizon": rnd(1 - (1 - chance) ** task["long_horizon_weeks"], "probability"),
                            "alarm_chance_per_slow_week": text(slow_chance), "mean_delay_weeks": rnd(1 / slow_chance, "weeks")},
        "q3_tolerance": {"tolerance": tolerance, "histories": histories, "histories_with_an_alarm": int(crossing * histories),
                         "probability": rnd(crossing, "probability"),
                         "single_looks_by_week": [text(look) for look in looks],
                         "sum_of_single_looks": rnd(sum(looks), "probability"),
                         "single_look_in_the_last_week": rnd(looks[-1], "probability")},
        "q4_record": {"record": task["record"], "cumulative_shortfall": shortfalls,
                      "cumulative_sum": [rnd(value, "courses") for value in sums],
                      "reference_value": text(reference), "decision_interval": task["cusum_decision_interval"],
                      "tolerance_fires_in_week": fired_c, "cumulative_sum_fires_in_week": fired_h,
                      "first_slow_week": slow_from, "slow_weeks_seen_by_the_tolerance": fired_c - slow_from + 1,
                      "slow_weeks_seen_by_the_cumulative_sum": fired_h - slow_from + 1,
                      "lowest_cumulative_shortfall": min(shortfalls)},
    }


def strip_private(value):
    if isinstance(value, dict):
        return {key: strip_private(item) for key, item in value.items() if not key.startswith("_")}
    if isinstance(value, list):
        return [strip_private(item) for item in value]
    return value


def analyze(sc: dict) -> dict:
    if sc["rounding"] != {f"{key}_decimals": value for key, value in DECIMALS.items()}:
        raise ValueError("scenarios.json rounding does not match analyze.py")
    model = build_model(sc)
    figures = exact_figures(model, sc)
    model["calibrated"] = figures["calibrated"]
    sims = run_simulations(model, sc, figures)
    single = single_look_section(model, sc, sims)
    looks = [band["_looks"] for band in single["prediction_band"]]
    results = {
        "module_id": sc["module_id"],
        "kind": "synthetic: every number below comes from the assumptions in scenarios.json; nothing is measured in "
                "the Demerzel repository, and no weekly output of the project was read",
        "rounding": "probabilities to 6 decimals, weeks and costs to 2, courses and ratios to 4, distances in standard "
                    "errors to 2; exact fractions are rounded half to even",
        "arithmetic": "exact figures are counts of equally likely coin histories (whole numbers and fractions); the "
                      "simulation draws from random.Random(seed).random(); floats come from + - * /, math.sqrt and math.fsum",
        "plan": plan_section(model, sc),
        "simulation": sc["simulation"],
        "single_look": single,
        "weekly_limit": weekly_limit_section(model, sc, figures, sims),
        "prediction_band_every_week": band_section(model, sc, looks, sims),
        "tolerance": tolerance_section(model, sc, figures, sims),
        "cumulative_sum": cusum_section(model, sc, figures, sims),
        "change_week": change_week_section(model, sc),
        "milder_slowdown": milder_section(model, sc),
        "bursty_output": bursty_section(model, sc, figures, sims),
        "costs": cost_section(model, sc, figures),
        "hypothesis_test": hypothesis_test(model, sc, figures),
    }
    results["worked_examples"] = worked_examples(model, sc, figures)
    results["controls"] = controls(model, sc, figures, sims)
    results["simulation_against_exact"] = agreement_summary(sc)
    results["transfer_task"] = transfer_task(sc["transfer_task"])
    results["checks"] = [{"check": name, "times_evaluated": times, "passed": True} for name, times in CHECKS.items()]
    return strip_private(results)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--scenarios", type=Path, default=HERE / "scenarios.json")
    parser.add_argument("--output", type=Path, default=HERE / "results.json")
    parser.add_argument("--check", action="store_true",
                        help="recompute and compare with the output file instead of writing it")
    args = parser.parse_args()
    CHECKS.clear()
    AGREEMENT.clear()
    try:
        result = analyze(json.loads(args.scenarios.read_text(encoding="utf-8")))
    except (AssertionError, ArithmeticError, KeyError, ValueError, OSError) as exc:
        print(f"analyze.py: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 1
    payload = (json.dumps(result, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    if args.check:
        try:
            saved = args.output.read_bytes()
        except OSError as exc:
            print(f"analyze.py: cannot read {args.output}: {exc}", file=sys.stderr)
            return 1
        same = saved.replace(b"\r\n", b"\n") == payload
        print(f"analyze.py: {args.output.name} {'matches' if same else 'DIFFERS FROM'} a fresh run "
              f"({len(CHECKS)} self-checks passed)")
        return 0 if same else 1
    args.output.write_bytes(payload)
    print(f"analyze.py: {len(CHECKS)} self-checks passed -> {args.output.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
