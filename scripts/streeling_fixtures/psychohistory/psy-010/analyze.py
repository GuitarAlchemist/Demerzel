#!/usr/bin/env python3
"""PSY-010 analysis: growth curves fitted to the short history of English modules.

Reads observed-input.json (written by extract.py) and scenarios.json, never the
repository, and writes results.json: the daily series, its bursts, least-squares
fits of a line, an exponential and a logistic curve at three cut-off dates, the
date each one gives for the plan's target, a profile over the logistic ceiling,
step descriptions, burst scenarios, negative controls and the transfer task.

The line is solved exactly with fractions. The two-parameter curves use a
coarse grid, Gauss-Newton steps and a Newton polish (see "search" in
scenarios.json); nothing depends on the clock or on the machine.

Run from the repository root:
    python -I scripts/streeling_fixtures/psychohistory/psy-010/analyze.py
    python -I scripts/streeling_fixtures/psychohistory/psy-010/analyze.py --check
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
                / "state/streeling/fixtures/psychohistory/psy-010" / Path(__file__).name)

HERE = FIXTURE_FILE.parent
ROUND: dict[str, int] = {}   # decimals, read from scenarios.json
SEARCH: dict = {}            # search settings and the length of a year, read from scenarios.json
CHECKS: dict[str, int] = {}  # self-check -> times evaluated


def check(name: str, condition: bool, detail: str = "") -> None:
    """A self-check that can fail: abort instead of writing a wrong result."""
    if not condition:
        raise AssertionError(f"self-check failed: {name}" + (f" ({detail})" if detail else ""))
    CHECKS[name] = CHECKS.get(name, 0) + 1


def rnd(value, kind: str) -> float:
    return round(float(value), ROUND[kind + "_decimals"])


def years(days) -> float:
    return rnd(days / SEARCH["days_per_year"], "year")


def sig(value) -> float:
    """Six significant digits, through the correctly rounded decimal formatting of floats."""
    return float(f"{float(value):.{ROUND['significant_digits'] - 1}e}")


def exact(value: Fraction) -> dict:
    return {"exact": f"{value.numerator}/{value.denominator}", "value": sig(value)}


def percent(part, whole) -> float:
    return rnd(100 * Fraction(part) / Fraction(whole), "percent")


# ---------------------------------------------------------------- the series

def parse_moment(stamp: str) -> datetime:
    if len(stamp) != 20 or stamp[10] != "T" or stamp[-1] != "Z":
        raise ValueError(f"unexpected timestamp {stamp!r}")
    return datetime.strptime(stamp, "%Y-%m-%dT%H:%M:%SZ")


def parse_day(stamp: str, hours: int = 0) -> date:
    """The UTC day of a timestamp, or its day on a clock `hours` ahead of UTC."""
    return (parse_moment(stamp) + timedelta(hours=hours)).date()


def daily_counts(rows: list[dict], field: str, first: date, days: int, hours: int = 0) -> list[int]:
    """End-of-day module counts: each commit's net change is booked on its day of `field` (UTC unless `hours`)."""
    change, previous = [0] * days, 0
    for row in rows:
        index = (parse_day(row[field], hours) - first).days
        if not 0 <= index < days:
            raise ValueError(f"{row['commit']}: {field} falls outside the series")
        change[index] += row["modules"] - previous
        previous = row["modules"]
    counts, total = [], 0
    for delta in change:
        total += delta
        counts.append(total)
    return counts


def active_days(counts: list[int]) -> list[int]:
    return [i for i, count in enumerate(counts) if count != (counts[i - 1] if i else 0)]


def find_bursts(counts: list[int], max_gap: int) -> list[dict]:
    groups: list[list[int]] = []
    for day in active_days(counts):
        if groups and day - groups[-1][-1] <= max_gap:
            groups[-1].append(day)
        else:
            groups.append([day])
    return [{"first": g[0], "last": g[-1], "active_days": len(g),
             "before": counts[g[0] - 1] if g[0] else 0, "after": counts[g[-1]]} for g in groups]


# ---------------------------------------------------------------- the fits

class Curve:
    """A fitted curve: its value on a day and the (fractional) day it reaches a level, or None."""

    def __init__(self, value, time_to, parameters: dict, sse, points: int) -> None:
        self.value, self.time_to, self.parameters, self.sse, self.points = value, time_to, parameters, sse, points


def fit_line(ts: list, ys: list) -> tuple[Fraction, Fraction, Fraction]:
    """Ordinary least squares in exact arithmetic: intercept, slope, residual sum of squares."""
    n = len(ts)
    st, sy = sum(ts), sum(ys)
    stt, sty = sum(t * t for t in ts), sum(t * y for t, y in zip(ts, ys))
    slope = Fraction(n * sty - st * sy) / Fraction(n * stt - st * st)
    intercept = Fraction(sy) / n - slope * Fraction(st) / n
    residuals = [y - intercept - slope * t for t, y in zip(ts, ys)]
    check("line: residuals sum to zero and are orthogonal to time (normal equations, exact)",
          sum(residuals) == 0 and sum(t * e for t, e in zip(ts, residuals)) == 0)
    return intercept, slope, sum(e * e for e in residuals)


def line_curve(ts: list[int], ys: list, unit: str) -> Curve:
    intercept, slope, sse = fit_line(ts, ys)
    return Curve(lambda t: float(intercept + slope * t),
                 lambda level: (Fraction(level) - intercept) / slope if slope > 0 else None,
                 {"intercept": exact(intercept), f"slope_per_{unit}": exact(slope)}, sse, len(ts))


def link_exponential(z: float) -> tuple[float, float, float]:
    f = math.exp(z)
    return f, f, f


def link_logistic(ceiling: float):
    def link(z: float) -> tuple[float, float, float]:
        if z >= 0:
            f = ceiling / (1.0 + math.exp(-z))
        else:
            e = math.exp(z)
            f = ceiling * e / (1.0 + e)
        slope = f * (1.0 - f / ceiling)
        return f, slope, slope * (1.0 - 2.0 * f / ceiling)
    return link


def sse_at(link, us: list[float], ys: list, theta: tuple[float, float]) -> float:
    try:
        return math.fsum((y - link(theta[0] + theta[1] * u)[0]) ** 2 for u, y in zip(us, ys))
    except OverflowError:
        return math.inf


def step_sums(link, us, ys, theta, newton: bool) -> tuple[float, float, float, float, float]:
    """Curvature matrix (Gauss-Newton, or half the exact Hessian) and minus half the gradient."""
    a00 = a01 = a11 = g0 = g1 = 0.0
    for u, y in zip(us, ys):
        f, d1, d2 = link(theta[0] + theta[1] * u)
        e = y - f
        w = d1 * d1 - e * d2 if newton else d1 * d1
        a00 += w
        a01 += w * u
        a11 += w * u * u
        g0 += d1 * e
        g1 += d1 * e * u
    return a00, a01, a11, g0, g1


def refine(link, us: list[float], ys: list, theta: tuple[float, float]) -> tuple[tuple[float, float], float]:
    """Least squares for y ~ link(theta0 + theta1 * u), from a start inside the right basin."""
    start_sse = sse = sse_at(link, us, ys, theta)
    for _ in range(SEARCH["gauss_newton_max_iterations"]):
        a00, a01, a11, g0, g1 = step_sums(link, us, ys, theta, False)
        det = a00 * a11 - a01 * a01
        if det <= 0:
            break
        s0, s1 = (g0 * a11 - g1 * a01) / det, (a00 * g1 - a01 * g0) / det
        for halving in range(SEARCH["step_halvings"]):
            trial = (theta[0] + s0 / 2 ** halving, theta[1] + s1 / 2 ** halving)
            trial_sse = sse_at(link, us, ys, trial)
            if trial_sse < sse:
                theta, sse = trial, trial_sse
                break
        else:
            break
    tolerance = SEARCH["newton_relative_tolerance"]
    for iteration in range(SEARCH["newton_max_iterations"]):
        h00, h01, h11, g0, g1 = step_sums(link, us, ys, theta, True)
        det = h00 * h11 - h01 * h01
        if not (h00 > 0 and det > 0):
            raise ArithmeticError("the Hessian is not positive definite where the Gauss-Newton search stopped")
        s0, s1 = (g0 * h11 - g1 * h01) / det, (h00 * g1 - h01 * g0) / det
        small = abs(s0) <= 1e-4 * max(1.0, abs(theta[0])) and abs(s1) <= 1e-4 * max(abs(theta[1]), 1e-12)
        if iteration == 0 and not small:
            raise ArithmeticError("the Gauss-Newton search stopped far from a stationary point")
        theta = (theta[0] + s0, theta[1] + s1)
        if abs(s0) <= tolerance * max(1.0, abs(theta[0])) and abs(s1) <= tolerance * max(abs(theta[1]), 1e-12):
            break
    else:
        raise ArithmeticError("the Newton polish did not converge")
    sse = sse_at(link, us, ys, theta)
    check("curve fit: residual sum after the search is not above the residual sum at the grid start",
          sse <= start_sse * (1 + 1e-12))
    j0 = j1 = g0 = g1 = 0.0
    for u, y in zip(us, ys):
        f, d1, _ = link(theta[0] + theta[1] * u)
        j0 += d1 * d1
        j1 += d1 * d1 * u * u
        g0 += d1 * (y - f)
        g1 += d1 * (y - f) * u
    if sse > 1e-9 * math.fsum(y * y for y in ys):  # an exact fit leaves no residual direction to test
        limit = SEARCH["gradient_cosine_tolerance"]
        check("curve fit: residuals orthogonal to both columns of the Jacobian (stationary point)",
              abs(g0) <= limit * math.sqrt(j0 * sse) and abs(g1) <= limit * math.sqrt(j1 * sse),
              f"{g0 / math.sqrt(j0 * sse):.2e}, {g1 / math.sqrt(j1 * sse):.2e}")
    return theta, sse


def rate_grid() -> list[float]:
    geometric = SEARCH["rate_grid_geometric"]
    low, high, points = geometric["from"], geometric["to"], geometric["points"]
    return list(SEARCH["rate_grid_fixed"]) + [low * (high / low) ** (k / (points - 1)) for k in range(points)]


def centred(ts: list[int]) -> tuple[float, list[float]]:
    mean = math.fsum(ts) / len(ts)
    return mean, [t - mean for t in ts]


def exponential_curve(ts: list[int], ys: list, unit: str) -> Curve:
    """Least squares in levels for y ~ a * exp(b * t)."""
    mean, us = centred(ts)
    best = None
    for rate in rate_grid():
        weights = [math.exp(rate * u) for u in us]
        amplitude = math.fsum(y * w for y, w in zip(ys, weights)) / math.fsum(w * w for w in weights)
        if amplitude > 0:
            start = (math.log(amplitude), rate)
            start_sse = sse_at(link_exponential, us, ys, start)
            if best is None or start_sse < best[0]:
                best = (start_sse, start)
    if best is None:
        raise ArithmeticError("no positive exponential fits this series")
    (c, r), sse = refine(link_exponential, us, ys, best[1])
    parameters = {f"value_at_{unit}_0": sig(math.exp(c - r * mean)), f"rate_per_{unit}": sig(r),
                  f"doubling_time_{unit}s": rnd(math.log(2) / r, "day") if r > 0 else None}
    return Curve(lambda t: math.exp(c + r * (t - mean)),
                 lambda level: mean + (math.log(level) - c) / r if r > 0 and level > 0 else None,
                 parameters, sse, len(ts))


def logistic_curve(ts: list[int], ys: list, ceiling: float, unit: str) -> Curve:
    """Least squares in levels for y ~ ceiling / (1 + exp(-r * (t - midpoint))), ceiling fixed."""
    mean, us = centred(ts)
    link = link_logistic(float(ceiling))
    low, high = max(0.25 * min(ys), 0.005 * max(ys)), min(2.0 * max(ys), 0.98 * ceiling)
    points = SEARCH["level_grid_points"]
    best = None
    for k in range(points):
        level = low * (high / low) ** (k / (points - 1))
        for rate in rate_grid():
            start = (math.log(level / (ceiling - level)), rate)
            start_sse = sse_at(link, us, ys, start)
            if best is None or start_sse < best[0]:
                best = (start_sse, start)
    (c, r), sse = refine(link, us, ys, best[1])
    parameters = {"ceiling": ceiling, f"rate_per_{unit}": sig(r),
                  f"midpoint_{unit}": sig(mean - c / r) if r > 0 else None,
                  f"value_at_{unit}_0": sig(link(c - r * mean)[0])}

    def time_to(level):
        if not (r > 0 and 0 < level < ceiling):
            return None
        return mean + (math.log(level / (ceiling - level)) - c) / r

    return Curve(lambda t: link(c + r * (t - mean))[0], time_to, parameters, sse, len(ts))


def log_scale_exponential(ts: list[int], ys: list[int]) -> Curve:
    """The spreadsheet 'exponential trendline': a line fitted to ln(y), not least squares on y."""
    logs = [math.log(y) for y in ys]
    n, st = len(ts), sum(ts)
    slope = (n * math.fsum(t * v for t, v in zip(ts, logs)) - st * math.fsum(logs)) / (n * sum(t * t for t in ts) - st * st)
    intercept = math.fsum(logs) / n - slope * st / n
    sse = math.fsum((y - math.exp(intercept + slope * t)) ** 2 for t, y in zip(ts, ys))
    return Curve(lambda t: math.exp(intercept + slope * t),
                 lambda level: (math.log(level) - intercept) / slope if slope > 0 else None,
                 {"value_at_day_0": sig(math.exp(intercept)), "rate_per_day": sig(slope)}, sse, n)


# ---------------------------------------------------------------- describing a fit

def reach(curve: Curve, level: float, first: date, reference_index: int) -> dict:
    """First whole day on which the curve is at least `level`, counted from day 0 of the series."""
    moment = curve.time_to(level)
    if moment is None:
        return {"level": level, "reached": False, "day": None, "day_index": None, "date": None,
                "days_after_pinned_date": None, "years_after_pinned_date": None}
    index = math.ceil(moment)
    check("reach rule: the curve is at or above the level on the reported day and below it the day before",
          curve.value(index) >= level * (1 - 1e-9) and curve.value(index - 1) < level * (1 + 1e-9),
          f"{curve.value(index - 1)} / {curve.value(index)} against {level}")
    return {"level": level, "reached": True, "day": rnd(moment, "day"), "day_index": index,
            "date": (first + timedelta(days=index)).isoformat() if index <= (date.max - first).days else None,
            "days_after_pinned_date": index - reference_index,
            "years_after_pinned_date": years(index - reference_index)}


def sign_runs(residuals: list) -> dict:
    signs = [e >= 0 for e in residuals]
    changes = sum(a != b for a, b in zip(signs, signs[1:]))
    longest = run = 1
    for a, b in zip(signs, signs[1:]):
        run = run + 1 if a == b else 1
        longest = max(longest, run)
    return {"comparisons": len(signs) - 1, "sign_changes": changes, "longest_run_days": longest,
            "positive_residual_days": sum(signs)}


def describe(curve: Curve, counts: list[int], first: date, pin_index: int, pin_count: int, level: float) -> dict:
    last = len(counts) - 1
    fitted_last = curve.value(last)
    entry = {
        "parameters": curve.parameters,
        "points": curve.points,
        "sse": rnd(curve.sse, "sse"),
        "rmse": rnd(math.sqrt(curve.sse / curve.points), "rmse"),
        "fitted_on_last_day": rnd(fitted_last, "level"),
        "observed_minus_fitted_on_last_day": rnd(counts[last] - fitted_last, "level"),
        "plan": reach(curve, level, first, pin_index),
    }
    if last < pin_index:
        entry["predicted_for_pinned_date"] = rnd(curve.value(pin_index), "level")
        entry["observed_on_pinned_date"] = pin_count
    else:
        entry["residual_signs"] = sign_runs([y - curve.value(t) for t, y in enumerate(counts)])
        entry["catches_up_with_observed_count"] = reach(curve, float(pin_count), first, pin_index)
    return entry


def three_fits(ts: list[int], counts: list[int], ceiling: int) -> dict[str, Curve]:
    return {"line": line_curve(ts, counts, "day"), "exponential": exponential_curve(ts, counts, "day"),
            "logistic": logistic_curve(ts, counts, ceiling, "day")}


# ---------------------------------------------------------------- step descriptions

def step_models(counts: list[int], change_points: list[int], first: date) -> dict:
    """Best piecewise-constant fits, exact: costs are integers over one common denominator."""
    n = len(counts)
    sum1, sum2, common = [0], [0], 1
    for index, count in enumerate(counts):
        sum1.append(sum1[-1] + count)
        sum2.append(sum2[-1] + count * count)
        common = common * (index + 1) // math.gcd(common, index + 1)

    def cost(i: int, j: int) -> int:  # residual sum of counts[i:j] around its mean, times `common`
        length, total = j - i, sum1[j] - sum1[i]
        return (length * (sum2[j] - sum2[i]) - total * total) * (common // length)

    most = max(change_points)
    best = [[None] * (n + 1) for _ in range(most + 1)]
    back = [[0] * (n + 1) for _ in range(most + 1)]
    for j in range(1, n + 1):
        best[0][j] = cost(0, j)
    for k in range(1, most + 1):
        for j in range(k + 1, n + 1):
            for i in range(k, j):
                value = best[k - 1][i] + cost(i, j)
                if best[k][j] is None or value < best[k][j]:
                    best[k][j], back[k][j] = value, i
    mean = Fraction(sum1[n], n)
    check("steps: the fit without a change point is the sum of squares around the mean",
          Fraction(best[0][n], common) == sum((count - mean) ** 2 for count in counts))
    brute = min(sum((c - Fraction(sum1[i], i)) ** 2 for c in counts[:i])
                + sum((c - Fraction(sum1[n] - sum1[i], n - i)) ** 2 for c in counts[i:]) for i in range(1, n))
    check("steps: the one-change fit found by dynamic programming equals a brute-force search over every split",
          Fraction(best[1][n], common) == brute)
    check("steps: the residual sum never rises when a change point is added",
          all(best[k][n] <= best[k - 1][n] for k in range(1, most + 1)))
    own = [0] + active_days(counts)[1:] + [n]
    check("steps: a staircase with a change point on every active day reproduces the series exactly",
          sum(cost(i, j) for i, j in zip(own, own[1:])) == 0)
    result = {"change_points_0": {"parameters": 1, "sse": rnd(Fraction(best[0][n], common), "sse"),
                                  "level": rnd(mean, "level")}}
    for k in change_points:
        cuts, j = [], n
        for level in range(k, 0, -1):
            j = back[level][j]
            cuts.append(j)
        cuts.reverse()
        bounds = [0] + cuts + [n]
        result[f"change_points_{k}"] = {
            "parameters": 2 * k + 1,
            "sse": rnd(Fraction(best[k][n], common), "sse"),
            "rmse": rnd(math.sqrt(Fraction(best[k][n], common) / n), "rmse"),
            "change_days": cuts,
            "change_dates": [(first + timedelta(days=c)).isoformat() for c in cuts],
            "levels": [rnd(Fraction(sum1[b] - sum1[a], b - a), "level") for a, b in zip(bounds, bounds[1:])],
        }
    result["change_points_for_an_exact_fit"] = len(own) - 2
    result["raw_one_change_sse"] = Fraction(best[1][n], common)
    return result


# ---------------------------------------------------------------- ceiling profile

def ceiling_profile(counts: list, ceilings: list[int], level: float, first: date, pin_index: int) -> list[dict]:
    ts, rows = list(range(len(counts))), []
    for ceiling in ceilings:
        curve = logistic_curve(ts, counts, ceiling, "day")
        row = {"ceiling": ceiling, "rate_per_day": curve.parameters["rate_per_day"],
               "midpoint_day": curve.parameters["midpoint_day"], "sse": rnd(curve.sse, "sse"),
               "rmse": rnd(math.sqrt(curve.sse / curve.points), "rmse"), "raw_sse": curve.sse}
        if first is not None:
            plan = reach(curve, level, first, pin_index)
            row["plan_date"], row["plan_years_after_pinned_date"] = plan["date"], plan["years_after_pinned_date"]
        rows.append(row)
    return rows


def profile_summary(rows: list[dict]) -> dict:
    raw = [row.pop("raw_sse") for row in rows]
    low, high = min(raw), max(raw)
    return {
        "lowest_sse_at_ceiling": rows[raw.index(low)]["ceiling"],
        "highest_sse_at_ceiling": rows[raw.index(high)]["ceiling"],
        "lowest_sse_is_at_the_largest_ceiling_tried": raw.index(low) == len(raw) - 1,
        "sse_falls_at_every_step_up_in_ceiling": all(b < a for a, b in zip(raw, raw[1:])),
        "highest_sse_over_lowest": rnd(high / low, "rmse"),
        "spread_percent_of_lowest": rnd(100 * (high - low) / low, "percent"),
    }


# ---------------------------------------------------------------- synthetic parts

def noise(seed: int, days: int, half_width: float) -> list[float]:
    generator = random.Random(seed)
    return [half_width * (2.0 * generator.random() - 1.0) for _ in range(days)]


def negative_controls(settings: dict, days: int, observed_changes: int, observed_spread: float) -> dict:
    ts = list(range(days))
    line = settings["noisy_line"]
    ys = [line["intercept"] + line["slope_per_day"] * t + e
          for t, e in zip(ts, noise(line["seed"], days, line["noise_half_width"]))]
    intercept, slope, _ = fit_line(ts, [Fraction(y) for y in ys])
    runs = sign_runs([Fraction(y) - intercept - slope * t for t, y in zip(ts, ys)])
    check("negative control: a line with independent noise changes residual sign at least five times as often "
          "as the observed fits", runs["sign_changes"] >= 5 * observed_changes, str(runs["sign_changes"]))
    result = {"kind": "synthetic: series with known answers, same length as the observed one",
              "noisy_line": {"what": "a line plus independent noise, fitted by a line: residual signs",
                             "fitted_slope_per_day": sig(slope), **runs}}
    for name in ("planted_logistic_past_its_turn", "planted_logistic_before_its_turn"):
        planted = settings[name]
        link = link_logistic(float(planted["ceiling"]))
        ys = [link(planted["rate_per_day"] * (t - planted["midpoint_day"]))[0] + e
              for t, e in zip(ts, noise(planted["seed"], days, planted["noise_half_width"]))]
        rows = ceiling_profile(ys, planted["ceiling_profile"], 0.0, None, 0)
        result[name] = {"what": "a logistic curve with a known ceiling plus independent noise, refitted with the "
                                "ceiling fixed at each value",
                        "planted_ceiling": planted["ceiling"],
                        "planted_value_on_last_day": rnd(link(planted["rate_per_day"] * (days - 1 - planted["midpoint_day"]))[0], "level"),
                        "profile": [{"ceiling": row["ceiling"], "sse": row["sse"]} for row in rows],
                        **profile_summary(rows)}
    past, before = result["planted_logistic_past_its_turn"], result["planted_logistic_before_its_turn"]
    check("negative control: the ceiling profile recovers a planted ceiling once the series has passed its turn",
          past["lowest_sse_at_ceiling"] == past["planted_ceiling"] and past["highest_sse_over_lowest"] > 2)
    check("negative control: the same profile is flat (under 10% spread) when the planted curve is seen before its turn",
          before["spread_percent_of_lowest"] < 10 and observed_spread < 10)
    return result


def known_answers() -> None:
    intercept, slope, sse = fit_line([0, 1, 2], [0, 1, 1])
    check("hand-computed line through (0,0), (1,1), (2,1): slope 1/2, intercept 1/6, residual sum 1/6",
          (intercept, slope, sse) == (Fraction(1, 6), Fraction(1, 2), Fraction(1, 6)))
    line = line_curve([0, 1], [0, 1], "day")
    check("hand-computed reach: the line y = t first rounds to 10 at t = 9.5, so on day 10",
          line.time_to(9.5) == Fraction(19, 2) and math.ceil(line.time_to(9.5)) == 10)
    ts = list(range(41))
    planted = exponential_curve(ts, [3.0 * math.exp(0.05 * t) for t in ts], "day")
    check("planted exponential 3 * exp(0.05 t) is recovered",
          abs(planted.parameters["value_at_day_0"] - 3.0) < 1e-5 and abs(planted.parameters["rate_per_day"] - 0.05) < 1e-7
          and planted.sse < 1e-12)
    ts = list(range(201))
    link = link_logistic(525.0)
    planted = logistic_curve(ts, [link(0.03 * (t - 100))[0] for t in ts], 525, "day")
    check("planted logistic with ceiling 525, rate 0.03 and midpoint day 100 is recovered",
          abs(planted.parameters["rate_per_day"] - 0.03) < 1e-7 and abs(planted.parameters["midpoint_day"] - 100.0) < 1e-4
          and planted.sse < 1e-9)
    check("a logistic curve whose ceiling equals the level never reaches it; with the half-unit margin it does",
          planted.time_to(525.0) is None and planted.time_to(524.5) is not None)
    counts = [2, 2, 5, 5, 5, 9]
    check("hand-computed bursts of 2, 2, 5, 5, 5, 9: active days 0, 2, 5; three bursts at a gap of 1, one at a gap of 3",
          active_days(counts) == [0, 2, 5] and len(find_bursts(counts, 1)) == 3 and len(find_bursts(counts, 3)) == 1)


def transfer_line(ts: list[int], ys: list[int], level: float, unit: str) -> tuple[dict, Curve]:
    """A line of the transfer task, with the sums a learner needs to redo it by hand."""
    intercept, slope, sse = fit_line(ts, ys)
    curve = line_curve(ts, ys, unit)
    moment = curve.time_to(level)
    return {"points": len(ts),
            "sums": {"n": len(ts), "sum_t": sum(ts), "sum_y": sum(ys),
                     "sum_t_squared": sum(t * t for t in ts), "sum_t_y": sum(t * y for t, y in zip(ts, ys))},
            "slope_per_week": exact(slope), "intercept": exact(intercept),
            "sse": {"exact": f"{sse.numerator}/{sse.denominator}", "value": rnd(sse, "sse")},
            "reach_level": level, "reach_week_before_rounding_up": rnd(moment, "level"),
            "reach_week": math.ceil(moment)}, curve


def transfer_exponential(task: dict, ts: list[int], counts: list[int], level: float, line: dict) -> dict:
    """Question 3, exponential: the given parameters are checked against the least-squares fit, then used as given."""
    fitted = exponential_curve(ts, counts, task["unit"])
    given, tolerance = task["exponential_given"], task["given_relative_tolerance"]
    a, b = given["value_at_week_0"], given["rate_per_week"]
    check("transfer task: the given exponential parameters are the least-squares ones, rounded",
          abs(a / fitted.parameters["value_at_week_0"] - 1) <= tolerance
          and abs(b / fitted.parameters["rate_per_week"] - 1) <= tolerance)
    sse = math.fsum((y - a * math.exp(b * t)) ** 2 for t, y in zip(ts, counts))
    moment = math.log(level / a) / b
    return {"given": given, "least_squares_fit": fitted.parameters,
            "sse_from_given": rnd(sse, "sse"),
            "reach_week_before_rounding_up": rnd(moment, "level"), "reach_week": math.ceil(moment),
            "line_sse_over_exponential_sse": rnd(float(Fraction(line["sse"]["exact"])) / sse, "rmse"),
            "weeks_between_line_and_exponential": line["reach_week"] - math.ceil(moment)}


def transfer_logistic(task: dict, ts: list[int], counts: list[int], level: float) -> dict:
    """Question 3, logistic: same treatment, and the time from the midpoint to the reach level."""
    given, tolerance = task["logistic_given"], task["given_relative_tolerance"]
    ceiling, r, midpoint = given["ceiling"], given["rate_per_week"], given["midpoint_week"]
    fitted = logistic_curve(ts, counts, ceiling, task["unit"])
    check("transfer task: the given logistic parameters are the least-squares ones, rounded",
          abs(r / fitted.parameters["rate_per_week"] - 1) <= tolerance
          and abs(midpoint / fitted.parameters["midpoint_week"] - 1) <= tolerance)
    sse = math.fsum((y - ceiling / (1.0 + math.exp(-r * (t - midpoint)))) ** 2 for t, y in zip(ts, counts))
    tail = math.log(level / (ceiling - level)) / r
    return {"given": given, "least_squares_fit": fitted.parameters,
            "sse_from_given": rnd(sse, "sse"),
            "odds_at_reach_level": sig(level / (ceiling - level)),
            "weeks_from_midpoint_to_reach_level": rnd(tail, "level"),
            "reach_week_before_rounding_up": rnd(midpoint + tail, "level"),
            "reach_week": math.ceil(midpoint + tail),
            "reaches_its_ceiling_exactly": False}


def transfer_week_values(task: dict, line: Curve, week: int) -> dict:
    """Question 5: what the three curves say for the week in which the given exponential reaches the target."""
    a, b = task["exponential_given"]["value_at_week_0"], task["exponential_given"]["rate_per_week"]
    given = task["logistic_given"]
    ceiling, r, midpoint = given["ceiling"], given["rate_per_week"], given["midpoint_week"]
    return {"week": week,
            "line": rnd(line.value(week), "level"),
            "exponential_from_given": rnd(a * math.exp(b * week), "level"),
            "logistic_from_given": rnd(ceiling / (1.0 + math.exp(-r * (week - midpoint))), "level"),
            "note": "no single answer to question 5: the review brief says what a sufficient plan contains"}


def transfer_task(task: dict, margin: float) -> dict:
    """The computed answers of the learner task, from the hypothetical inputs in scenarios.json."""
    counts, unit = task["counts_by_week"], task["unit"]
    n, ts, level = len(counts), list(range(len(counts))), task["target"] - margin
    first_burst_week = task["last_burst_first_week"]
    check("transfer task: the stated last burst starts on an active week after a pause",
          first_burst_week in active_days(counts) and first_burst_week - 1 not in active_days(counts))
    arrived = counts[-1] - counts[first_burst_week - 1]
    full, full_curve = transfer_line(ts, counts, level, unit)
    cut, cut_curve = transfer_line(ts[:first_burst_week], counts[:first_burst_week], level, unit)
    cut["predicted_for_last_week"] = rnd(cut_curve.value(n - 1), "level")
    cut["observed_on_last_week"] = counts[-1]
    exponential = transfer_exponential(task, ts, counts, level, full)
    logistic = transfer_logistic(task, ts, counts, level)
    return {
        "note": task["note"],
        "kind": "synthetic: computed from the hypothetical inputs in scenarios.json",
        "q1_series": {"weeks": n, "active_weeks": active_days(counts), "active_week_count": len(active_days(counts)),
                      "last_burst_weeks": [first_burst_week, n - 1], "arrived_in_last_burst": arrived,
                      "final_count": counts[-1], "share_of_final_count_percent": percent(arrived, counts[-1]),
                      "share_of_weeks_percent": percent(n - first_burst_week, n)},
        "q2_line": full,
        "q3_exponential": exponential,
        "q3_logistic": logistic,
        "q4_last_burst_removed": {**cut, "reach_week_moved_by": cut["reach_week"] - full["reach_week"],
                                  "reach_week_ratio": rnd(Fraction(cut["reach_week"], full["reach_week"]), "level")},
        "q5_values_in_the_week_the_exponential_reaches_the_target":
            transfer_week_values(task, full_curve, exponential["reach_week"]),
    }


# ---------------------------------------------------------------- the analysis

ROUNDING_NOTE = ("residual sums (sse) to 1 decimal, root-mean-square errors and ratios of residual sums to 3, "
                 "fitted parameters to 6 significant digits, days and years to 1 decimal, percentages to 1 "
                 "(2 for the profile's distance from the exponential), levels and other quotients to 2; 'exact' "
                 "is the unrounded fraction")


class History:
    """The daily series with the plan's constants: what the sections of results.json read."""

    def __init__(self, counts: list[int], first: date, target: int, level: float, ceiling: int) -> None:
        self.counts, self.first = counts, first
        self.target, self.level, self.ceiling = target, level, ceiling
        self.days, self.pin_index, self.pin_count = len(counts), len(counts) - 1, counts[-1]
        self.active = active_days(counts)

    def day_name(self, index: int) -> str:
        return (self.first + timedelta(days=index)).isoformat()

    def plan_reach(self, curve: Curve) -> dict:
        """When the curve reaches the plan level, counted from the pinned date."""
        return reach(curve, self.level, self.first, self.pin_index)


def configure(scenarios: dict) -> None:
    """Rounding and search settings come from scenarios.json; the tally of self-checks starts empty."""
    ROUND.update({key: value for key, value in scenarios["rounding"].items() if key != "note"})
    SEARCH.update({key: value for key, value in scenarios["search"].items() if key != "note"})
    SEARCH["days_per_year"] = scenarios["calendar"]["days_per_year"]
    CHECKS.clear()


def recount(snapshot: dict) -> tuple[int, int]:
    """Cross-checks of the snapshot: replays the module names commit by commit; returns additions and removals."""
    rows, counts_in, source = snapshot["commits"], snapshot["counts"], snapshot["source"]
    present: set[str] = set()
    for row in rows:
        check("each commit: removed modules were present and added ones were not",
              set(row["removed"]) <= present and not set(row["added"]) & present, row["commit"])
        present = (present - set(row["removed"])) | set(row["added"])
        check("each commit: the replayed module set has the recorded size", len(present) == row["modules"], row["commit"])
        check("each commit: the path classes sum to the files", sum(row["by_class"].values()) == row["files"]
              and row["by_class"]["module"] == row["modules"], row["commit"])
    additions, removals = sum(len(row["added"]) for row in rows), sum(len(row["removed"]) for row in rows)
    check("recount equals extract.py's counts: commits, additions, removals, modules at the pin",
          (len(rows), additions, removals, len(present)) == (counts_in["commits"], counts_in["module_additions"],
                                                             counts_in["module_removals"], counts_in["modules_at_pin"])
          and len(rows) == source["commits_touching_path"])
    check("additions - removals = modules at the pin", additions - removals == rows[-1]["modules"])
    by_department: dict[str, int] = {}
    for module in present:
        by_department[module.split("/")[0]] = by_department.get(module.split("/")[0], 0) + 1
    check("modules per department, recounted from the commit rows, equal extract.py's listing at the pin",
          by_department == snapshot["pin_state"]["modules_by_department"])
    return additions, removals


def daily_series(snapshot: dict, scenarios: dict) -> History:
    """The end-of-day counts by committer date, built along two code paths, with the plan's target and level."""
    rows, plan = snapshot["commits"], scenarios["plan"]
    target = plan["target_modules"]
    check("plan: departments x courses per department = target", plan["departments"] * plan["courses_per_department"] == target)
    level = target - scenarios["reached_rule"]["margin"]
    field = scenarios["series"]["date_field"]
    first, last = parse_day(rows[0][field]), parse_day(rows[-1][field])
    days = (last - first).days + 1
    counts = daily_counts(rows, field, first, days)
    by_last_commit: list = [None] * days
    for row in rows:
        by_last_commit[(parse_day(row[field]) - first).days] = row["modules"]
    for index in range(1, days):
        if by_last_commit[index] is None:
            by_last_commit[index] = by_last_commit[index - 1]
    check("daily series: booking net changes per day equals taking the last commit of each day", counts == by_last_commit)
    check("daily series: the last day holds the modules at the pin", counts[-1] == snapshot["counts"]["modules_at_pin"])
    return History(counts, first, target, level, scenarios["logistic"]["plan_ceiling"])


def observed_section(snapshot: dict, additions: int, removals: int, pin_count: int) -> dict:
    rows, counts_in, source, pin_state = snapshot["commits"], snapshot["counts"], snapshot["source"], snapshot["pin_state"]
    gaps = counts_in["largest_gap_between_author_and_committer_date_seconds"]
    departments = pin_state["modules_by_department"]
    largest = max(sorted(departments), key=lambda name: departments[name])
    return {
        "kind": "observed: counted from observed-input.json",
        "commits_reachable_from_pin": source["commits_reachable_from_pin"],
        "commits_touching_the_folder": len(rows),
        "commits_that_change_the_module_count": counts_in["commits_that_change_the_module_count"],
        "first_commit_utc": counts_in["first_commit_utc"], "last_commit_utc": counts_in["last_commit_utc"],
        "module_additions": additions, "module_removals": removals, "modules_at_pin": pin_count,
        "pairs_of_consecutive_commits_sharing_a_committer_second":
            counts_in["pairs_of_consecutive_commits_sharing_a_committer_second"],
        "commits_with_a_flat_layout_file": sum(row["by_class"]["flat_layout"] > 0 for row in rows),
        "flat_layout_path_names": len(snapshot["history_notes"]["flat_layout_paths"]),
        "files_at_pin": counts_in["files_at_pin"], "files_at_pin_by_class": counts_in["files_at_pin_by_class"],
        "department_folders": pin_state["department_folders_count"],
        "departments_with_a_module": pin_state["departments_with_a_module"],
        "department_records": pin_state["department_records"],
        "department_records_without_a_course_folder": pin_state["department_records_without_a_course_folder"],
        "largest_department": {"name": largest, "modules": departments[largest]},
        "largest_gap_between_author_and_committer_date_days": rnd(gaps / 86400, "level"),
        "commits_whose_author_and_committer_dates_fall_on_different_utc_days":
            counts_in["commits_whose_author_and_committer_dates_fall_on_different_utc_days"],
    }


def plan_section(history: History) -> dict:
    return {"kind": "assumed input (scenarios.json): the curriculum plan's figure", "target_modules": history.target,
            "reach_level": history.level, "modules_at_pin": history.pin_count,
            "remaining": history.target - history.pin_count,
            "share_of_plan_percent": percent(history.pin_count, history.target)}


def by_clock(history: History, rows: list[dict], settings: dict, max_gap: int) -> dict:
    """Active days and bursts when the days start at midnight on other clocks than UTC."""
    field, table = settings["date_field"], []
    for hours in settings["clock_offsets_hours"]:
        first, last = parse_day(rows[0][field], hours), parse_day(rows[-1][field], hours)
        counts = daily_counts(rows, field, first, (last - first).days + 1, hours)
        bursts = find_bursts(counts, max_gap)
        table.append({"utc_offset_hours": hours, "days": len(counts), "active_days": len(active_days(counts)),
                      "bursts": len(bursts), "burst_sizes": burst_sizes(bursts),
                      "last_day_is_active": active_days(counts)[-1] == len(counts) - 1})
    utc = [row for row in table if row["utc_offset_hours"] == 0]
    check("clocks: the UTC row reproduces the daily series and its bursts",
          len(utc) == 1 and utc[0]["active_days"] == len(history.active)
          and utc[0]["burst_sizes"] == burst_sizes(find_bursts(history.counts, max_gap)))
    others = [row for row in table if row["utc_offset_hours"] != 0]
    return {"max_gap_days": max_gap, "rows": table, "other_clocks": len(others),
            "fewest_active_days_on_another_clock": min(row["active_days"] for row in others),
            "most_active_days_on_another_clock": max(row["active_days"] for row in others),
            "same_bursts_on_every_clock": all(row["burst_sizes"] == utc[0]["burst_sizes"] for row in table)}


def busiest_day(history: History, rows: list[dict], settings: dict) -> dict:
    """The day with the largest change, and how close in time the commits that made it were."""
    field, window = settings["date_field"], settings["batch_window_seconds"]
    changes = [count - (history.counts[i - 1] if i else 0) for i, count in enumerate(history.counts)]
    index = changes.index(max(changes))
    previous, commits = 0, []
    for row in rows:
        change, previous = row["modules"] - previous, row["modules"]
        if change and parse_day(row[field]) == history.first + timedelta(days=index):
            commits.append((parse_moment(row[field]), change, row[field]))
    check("busiest day: the changes of its commits add up to the day's change",
          sum(change for _, change, _ in commits) == changes[index])
    times = [moment for moment, _, _ in commits]
    within = [[stamp for moment, _, stamp in commits if 0 <= (moment - start).total_seconds() <= window]
              for start in times]
    best = max(within, key=len)
    return {"date": history.day_name(index), "change": changes[index], "commits_that_change_the_count": len(commits),
            "largest_change_in_one_commit": max(change for _, change, _ in commits),
            "first_commit_utc": commits[0][2], "last_commit_utc": commits[-1][2],
            "span_seconds": int((times[-1] - times[0]).total_seconds()), "window_seconds": window,
            "most_commits_within_the_window": len(best),
            "window_first_commit_utc": best[0], "window_last_commit_utc": best[-1]}


def series_section(history: History, clocks: dict, busiest: dict) -> dict:
    counts, active, days, day_name = history.counts, history.active, history.days, history.day_name
    pauses = [(b - a - 1, a + 1, b - 1) for a, b in zip(active, active[1:])]
    longest_pause = max(pauses)
    series = {
        "kind": "computed from observed-input.json: end-of-day counts by committer date (UTC)",
        "first_day": day_name(0), "last_day": day_name(history.pin_index), "days": days,
        "active_days": len(active), "days_without_change": days - len(active),
        "percent_of_days_without_change": percent(days - len(active), days),
        "change_points": [{"day": i, "date": day_name(i), "count": counts[i],
                           "change": counts[i] - (counts[i - 1] if i else 0)} for i in active],
        "longest_pause": {"days": longest_pause[0], "from": day_name(longest_pause[1]), "to": day_name(longest_pause[2]),
                          "count_throughout": counts[longest_pause[1]]},
        "by_clock": clocks,
        "busiest_day": busiest,
    }
    check("daily series: the changes on the active days sum to the final count",
          sum(point["change"] for point in series["change_points"]) == history.pin_count)
    return series


def burst_sizes(bursts: list[dict]) -> list[int]:
    return [b["after"] - b["before"] for b in bursts]


def burst_intervals(bursts: list[dict]) -> list[int]:
    return [b["first"] - a["first"] for a, b in zip(bursts, bursts[1:])]


def last_burst_open(history: History, bursts: list[dict], max_gap: int) -> bool:
    """True when a module added on the day after the series would still join the last burst."""
    return history.pin_index + 1 - bursts[-1]["last"] <= max_gap


def bursts_section(history: History, rule: dict) -> tuple[dict, list[dict]]:
    """The bursts under the gap rule; also returns them as found, for the cut-offs and the burst scenarios."""
    counts, day_name = history.counts, history.day_name
    bursts = find_bursts(counts, rule["max_gap_days"])
    check("bursts: net modules of the bursts sum to the final count and active days are partitioned",
          sum(burst_sizes(bursts)) == history.pin_count and sum(b["active_days"] for b in bursts) == len(history.active))
    check("bursts: the rule finds at least three bursts, so that two cut-offs exist", len(bursts) >= 3)
    block = {
        "kind": "computed from the daily series under the burst convention in scenarios.json",
        "max_gap_days": rule["max_gap_days"],
        "bursts": [{"first_day": day_name(b["first"]), "last_day": day_name(b["last"]),
                    "span_days": b["last"] - b["first"] + 1, "active_days": b["active_days"],
                    "count_before": b["before"], "count_after": b["after"], "net_modules": size,
                    "share_of_final_count_percent": percent(size, history.pin_count),
                    "ends_on_the_last_day_of_the_series": b["last"] == history.pin_index}
                   for b, size in zip(bursts, burst_sizes(bursts))],
        "start_to_start_intervals_days": burst_intervals(bursts),
        "last_burst_share_of_days_percent": percent(bursts[-1]["last"] - bursts[-1]["first"] + 1, history.days),
        "last_burst_open_at_the_pin": last_burst_open(history, bursts, rule["max_gap_days"]),
        "last_day_a_new_module_would_join_the_last_burst": day_name(bursts[-1]["last"] + rule["max_gap_days"]),
        "number_of_bursts_by_max_gap_days": {str(gap): len(find_bursts(counts, gap)) for gap in rule["alternative_max_gap_days"]},
    }
    return block, bursts


def fits_section(history: History, bursts: list[dict]) -> tuple[dict, dict]:
    """The three fits at three cut-off dates; also returns the fitted curves, by cut-off and by model."""
    cutoffs = [("end_of_previous_burst", bursts[-2]["last"]), ("eve_of_last_burst", bursts[-1]["first"] - 1),
               ("pinned_date", history.pin_index)]
    fits, curves = {}, {}
    for name, index in cutoffs:
        part = history.counts[:index + 1]
        curves[name] = three_fits(list(range(index + 1)), part, history.ceiling)
        fits[name] = {"as_of": history.day_name(index), "days_of_history": index + 1, "count_on_that_day": part[-1],
                      "models": {model: describe(curve, part, history.first, history.pin_index, history.pin_count,
                                                 history.level)
                                 for model, curve in curves[name].items()}}
    check("cut-offs: the two earlier histories end on the same count (nothing was added during the pause)",
          fits["end_of_previous_burst"]["count_on_that_day"] == fits["eve_of_last_burst"]["count_on_that_day"])
    return fits, curves


def pinned_sses(curves: dict) -> dict:
    """Unrounded residual sums of the three fits to the full series."""
    return {model: curve.sse for model, curve in curves["pinned_date"].items()}


def plan_days(fits: dict) -> dict:
    """Day index on which each fit, at each cut-off, reaches the plan level."""
    return {name: {model: entry["plan"]["day_index"] for model, entry in block["models"].items()}
            for name, block in fits.items()}


def logistic_second_half(history: History, logistic: Curve) -> dict:
    """How long the fitted logistic takes from half of its ceiling to the plan level."""
    ceiling, level = history.ceiling, history.level
    half = reach(logistic, ceiling / 2, history.first, history.pin_index)
    tail = float(logistic.time_to(level) - logistic.time_to(ceiling / 2))
    return {
        "half_of_ceiling": ceiling / 2, "half_reached": half,
        "days_from_half_to_plan_level": rnd(tail, "day"),
        "years_from_half_to_plan_level": years(tail),
        "odds_at_plan_level": sig(level / (ceiling - level)),
        "log_of_odds_at_plan_level": sig(math.log(level / (ceiling - level))),
    }


def comparison_section(history: History, fits: dict, curves: dict) -> dict:
    at_pin = fits["pinned_date"]["models"]
    sses = pinned_sses(curves)
    lowest, highest = min(sses, key=lambda m: sses[m]), max(sses, key=lambda m: sses[m])
    reached = plan_days(fits)
    check("every fit at every cut-off reaches the plan level", all(v is not None for d in reached.values() for v in d.values()))
    pin_days = reached["pinned_date"]
    return {
        "kind": "computed: the three least-squares fits to the full daily series",
        "lowest_sse": lowest, "highest_sse": highest,
        "highest_sse_over_lowest": rnd(float(sses[highest]) / float(sses[lowest]), "rmse"),
        "sse_spread_percent_of_lowest": rnd(100 * (float(sses[highest]) - float(sses[lowest])) / float(sses[lowest]), "percent"),
        "plan_date_earliest": min(at_pin, key=lambda m: pin_days[m]), "plan_date_latest": max(at_pin, key=lambda m: pin_days[m]),
        "plan_date_spread_days": max(pin_days.values()) - min(pin_days.values()),
        "plan_date_spread_years": years(max(pin_days.values()) - min(pin_days.values())),
        "sign_changes_of_residuals": {model: at_pin[model]["residual_signs"]["sign_changes"] for model in at_pin},
        "plan_date_moves_when_last_burst_is_removed_years": {
            model: years(reached["eve_of_last_burst"][model] - pin_days[model]) for model in at_pin},
        "plan_date_moves_during_the_pause_years": {
            model: years(reached["eve_of_last_burst"][model] - reached["end_of_previous_burst"][model])
            for model in at_pin},
        "logistic_second_half": logistic_second_half(history, curves["pinned_date"]["logistic"]),
    }


def sensitivity_section(history: History, rows: list[dict], author_field: str, fits: dict, curves: dict) -> dict:
    """Three other reasonable choices on the same data: the spreadsheet exponential, author dates, active days."""
    counts, days, active = history.counts, history.days, history.active
    trendline = log_scale_exponential(list(range(days)), counts)
    check("the least-squares exponential has a residual sum no larger than the log-scale trendline's",
          curves["pinned_date"]["exponential"].sse <= trendline.sse)
    author_counts = daily_counts(rows, author_field, history.first, days)
    author_fits = three_fits(list(range(days)), author_counts, history.ceiling)
    author_plan = {model: history.plan_reach(curve) for model, curve in author_fits.items()}
    sparse_fits = three_fits(active, [counts[i] for i in active], history.ceiling)
    sparse_plan = {model: history.plan_reach(curve) for model, curve in sparse_fits.items()}
    pin_days = plan_days(fits)["pinned_date"]
    return {
        "kind": "computed: three other reasonable choices, same data",
        "fitted_to_the_active_days_only": {
            "points": len(active),
            "plan_dates": {model: entry["date"] for model, entry in sparse_plan.items()},
            "plan_years_after_pinned_date": {model: entry["years_after_pinned_date"] for model, entry in sparse_plan.items()},
        },
        "exponential_fitted_to_log_counts": {
            "parameters": trendline.parameters, "sse_in_modules": rnd(trendline.sse, "sse"),
            "plan": history.plan_reach(trendline)},
        "author_dates_instead_of_committer_dates": {
            "days_on_which_the_series_differs": sum(a != b for a, b in zip(counts, author_counts)),
            "plan_dates": {model: entry["date"] for model, entry in author_plan.items()},
            "plan_date_shift_days": {model: entry["day_index"] - pin_days[model] for model, entry in author_plan.items()},
        },
    }


def profile_section(history: History, ceilings: list[int], fits: dict, curves: dict) -> dict:
    """The logistic refitted with the ceiling fixed at each value, against the exponential as the limit."""
    rows = ceiling_profile(history.counts, ceilings, history.level, history.first, history.pin_index)
    exponential_sse = curves["pinned_date"]["exponential"].sse
    for row in rows:
        row["sse_above_exponential_percent"] = rnd(100 * (row["raw_sse"] - exponential_sse) / exponential_sse, "fine_percent")
    check("limit: the logistic with the largest ceiling tried is within 0.1% of the exponential's residual sum",
          abs(rows[-1]["raw_sse"] / exponential_sse - 1) < 1e-3)
    logistic_sse = fits["pinned_date"]["models"]["logistic"]["sse"]
    check("the plan-ceiling row of the profile is the logistic fit of the comparison",
          any(row["ceiling"] == history.ceiling and row["sse"] == logistic_sse for row in rows))
    summary = profile_summary(rows)  # takes the unrounded sums out of the rows
    return {"kind": "computed: the logistic refitted to the full daily series with the ceiling fixed at each value",
            "exponential_sse": rnd(exponential_sse, "sse"), "rows": rows, **summary}


def steps_section(history: History, change_points: list[int], curves: dict) -> dict:
    steps = {"kind": "computed: exact piecewise-constant fits to the full daily series",
             **step_models(history.counts, change_points, history.first)}
    lowest_curve_sse = min(pinned_sses(curves).values())
    steps["lowest_curve_sse_over_one_change_sse"] = rnd(float(lowest_curve_sse) / float(steps.pop("raw_one_change_sse")), "level")
    return steps


def burst_scenarios_section(history: History, bursts: list[dict], cases_in: dict, max_gap: int) -> dict:
    """The remaining modules delivered by bursts like the observed ones: arithmetic on an assumption."""
    remaining = history.target - history.pin_count
    sizes, intervals = burst_sizes(bursts), burst_intervals(bursts)
    still_open = last_burst_open(history, bursts, max_gap)
    # an open burst can only grow: a size taken from it is a lower bound, so the case's length is an upper bound
    grows = {"mean": still_open, "largest": still_open, "smallest": still_open and sizes[-1] == min(sizes)}
    choices = {"size": {"mean": Fraction(sum(sizes), len(sizes)), "largest": max(sizes), "smallest": min(sizes)},
               "interval": {"mean": Fraction(sum(intervals), len(intervals)), "shortest": min(intervals), "longest": max(intervals)}}
    cases = {}
    for name, case in cases_in.items():
        size, interval = Fraction(choices["size"][case["size"]]), Fraction(choices["interval"][case["interval"]])
        needed = math.ceil(Fraction(remaining) / size)
        wait = math.ceil(needed * interval)
        cases[name] = {"size": rnd(size, "level"), "interval_days": rnd(interval, "level"),
                       "bursts_before_rounding_up": exact(Fraction(remaining) / size), "bursts_needed": needed,
                       "days_after_pinned_date": wait, "years_after_pinned_date": years(wait),
                       "date": history.day_name(history.pin_index + wait),
                       "upper_bound_because_the_last_burst_is_open": grows[case["size"]]}
    return {"kind": "synthetic: arithmetic on the observed bursts under the repetition assumption in scenarios.json",
            "remaining_modules": remaining, "observed_burst_sizes": sizes,
            "observed_start_to_start_intervals_days": intervals, "cases": cases}


def analyze(snapshot: dict, scenarios: dict) -> dict:
    """Every section of results.json, computed in the order of the file; the self-checks run on the way."""
    configure(scenarios)
    known_answers()
    additions, removals = recount(snapshot)
    history = daily_series(snapshot, scenarios)
    clocks = by_clock(history, snapshot["commits"], scenarios["series"], scenarios["bursts"]["max_gap_days"])
    series = series_section(history, clocks, busiest_day(history, snapshot["commits"], scenarios["series"]))
    burst_block, bursts = bursts_section(history, scenarios["bursts"])
    fits, curves = fits_section(history, bursts)
    comparison = comparison_section(history, fits, curves)
    sensitivity = sensitivity_section(history, snapshot["commits"], scenarios["series"]["sensitivity_date_field"], fits, curves)
    profile = profile_section(history, scenarios["logistic"]["ceiling_profile"], fits, curves)
    steps = steps_section(history, scenarios["step_models"]["change_points"], curves)
    burst_scenarios = burst_scenarios_section(history, bursts, scenarios["burst_scenarios"]["cases"],
                                              scenarios["bursts"]["max_gap_days"])
    controls = negative_controls(scenarios["negative_controls"], history.days,
                                 max(comparison["sign_changes_of_residuals"].values()), profile["spread_percent_of_lowest"])
    source = snapshot["source"]
    result = {
        "module_id": snapshot["module_id"],
        "rounding": ROUNDING_NOTE,
        "source": {"repository": source["repository"], "commit": source["commit"], "history_path": source["history_path"],
                   "objects_read": source["objects_read"]},
        "observed": observed_section(snapshot, additions, removals, history.pin_count),
        "plan": plan_section(history),
        "series": series,
        "bursts": burst_block,
        "fits": {"kind": "computed: least squares on the daily counts, at three cut-off dates", **fits},
        "comparison": comparison,
        "sensitivity": sensitivity,
        "ceiling_profile": profile,
        "step_models": steps,
        "burst_scenarios": burst_scenarios,
        "negative_controls": controls,
        "transfer_task": transfer_task(scenarios["transfer_task"], scenarios["reached_rule"]["margin"]),
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
    args.output.write_bytes(text.encode("utf-8"))
    print(f"analyze.py: {len(CHECKS)} self-checks passed -> {args.output.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
