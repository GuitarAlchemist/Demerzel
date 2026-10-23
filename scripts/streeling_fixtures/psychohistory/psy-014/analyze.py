#!/usr/bin/env python3
"""PSY-014 analysis: how fast small errors grow in the logistic map.

Synthetic: reads scenarios.json only, never the repository, and writes
results.json. Every float comes from +, -, * and / on IEEE 754 doubles (plus
one correctly rounded square root); logarithms and exponentials are the short
series below, so no value from the C math library enters the output and the
file is the same on every platform. A high-precision comparison on Python
integers shows which results belong to the map and which to that arithmetic.

Run from the repository root:
    python -I -B scripts/streeling_fixtures/psychohistory/psy-014/analyze.py
    python -I -B scripts/streeling_fixtures/psychohistory/psy-014/analyze.py --check
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
                / "state/streeling/fixtures/psychohistory/psy-014" / Path(__file__).name)

HERE = FIXTURE_FILE.parent
LN2 = 0.6931471805599453  # the double nearest ln 2, written as a literal
SQRT_HALF = 0.7071067811865476  # the double nearest sqrt(1/2), written as a literal
SPACING = math.ldexp(1.0, -53)  # distance between neighbouring doubles from 1/2 to 1
WIDE_BITS = 1024  # high-precision runs: a state is a whole number of 2^-WIDE_BITS, held in a Python integer
WIDE_ONE = 1 << WIDE_BITS
DECIMALS = {"exponent": 6, "steps": 2, "share": 4, "ratio": 4, "state": 6}
GAP_DIGITS = 3
# Bit patterns computed with the functions of this script on CPython 3.14 (Windows, x86-64).
# A platform whose arithmetic differs stops here instead of writing different numbers.
FINGERPRINT = {"orbit": "0x1.fbffe3a42c0e0p-1", "ln10": "0x1.26bb1bbb55515p+1", "exp": "0x1.6c7fd1fb73484p-1"}
CHECKS: dict[str, int] = {}  # self-check -> times evaluated


def check(name: str, condition: bool, detail: str = "") -> None:
    """A self-check that can fail: abort instead of writing a wrong result."""
    if not condition:
        raise AssertionError(f"self-check failed: {name}" + (f" ({detail})" if detail else ""))
    CHECKS[name] = CHECKS.get(name, 0) + 1


def rnd(x: float, kind: str) -> float:
    """Round to the stated decimals; adding 0.0 turns a negative zero into zero."""
    return round(x, DECIMALS[kind]) + 0.0


def sig(x: float, digits: int = GAP_DIGITS) -> float:
    """Round to significant digits with Python's own correctly rounded formatting."""
    return float(f"{x:.{digits - 1}e}")


def ln(x: float) -> float:
    """Natural logarithm: ln x = e ln 2 + 2 (z + z^3/3 + z^5/5 + ...), with x = m 2^e and z = (m - 1)/(m + 1)."""
    if not x > 0.0:
        raise ValueError(f"logarithm of a number that is not positive: {x!r}")
    m, e = math.frexp(x)  # exact: 0.5 <= m < 1
    if m < SQRT_HALF:
        m, e = m * 2.0, e - 1  # exact; keeps |z| below 0.172
    z = (m - 1.0) / (m + 1.0)
    z2 = z * z
    term = total = z
    for k in range(3, 31, 2):  # the first neglected term is below 1e-23 |z|
        term *= z2
        total += term / k
    return e * LN2 + 2.0 * total


def exp(x: float) -> float:
    """Exponential: e^x = 2^k (1 + t + t^2/2! + ...), with k the integer nearest x / ln 2 and t = x - k ln 2."""
    k = math.floor(x / LN2 + 0.5)
    t = x - k * LN2
    term = total = 1.0
    for n in range(1, 21):
        term *= t / n
        total += term
    return math.ldexp(total, k)  # exact scaling by a power of two


def step(r: float, x: float) -> float:
    return r * x * (1.0 - x)


def settle(r: float, x: float, steps: int) -> float:
    for _ in range(steps):
        x = r * x * (1.0 - x)
    return x


def to_wide(x: float) -> int:
    """The double x as a whole number of 2^-WIDE_BITS: exact, or an error."""
    numerator, denominator = x.as_integer_ratio()
    if WIDE_ONE % denominator:
        raise ArithmeticError(f"{x!r} is not a whole number of 2^-{WIDE_BITS}")
    return numerator * (WIDE_ONE // denominator)


def wide_map(r: float):
    """One step of the map on such integers, for the exact value of the double r: exact products, one truncation."""
    numerator, denominator = r.as_integer_ratio()
    shift = WIDE_BITS + denominator.bit_length() - 1  # the denominator of a double is a power of two

    def wide_step(x: int) -> int:
        return (numerator * x * (WIDE_ONE - x)) >> shift

    return wide_step


def wide_error_bound(steps: int) -> float:
    """Largest distance between a wide run and the exact orbit of its starting double after `steps` steps.

    For states between 0 and 1 and r <= 4, one step multiplies an earlier error by at most 4 and truncates by less
    than one unit of 2^-WIDE_BITS, so the errors add up to less than (4^steps - 1) / 3 units.
    """
    return (4 ** steps - 1) / (3 * WIDE_ONE)


def seeded_starts(r: float, cfg: dict) -> list[float]:
    """Starting points on the attractor: seeded draws, each iterated settle_steps times."""
    rng = random.Random(cfg["seed"])
    starts = [settle(r, 0.1 + 0.8 * rng.random(), cfg["settle_steps"]) for _ in range(cfg["count"])]
    if not all(0.0 < x < 1.0 for x in starts):
        raise ArithmeticError(f"r = {r}: a starting point left the open interval (0, 1)")
    return starts


def lyapunov_blocks(r: float, x: float, blocks: int, block_steps: int) -> list[float]:
    """Block averages of ln|f'(x)| along one orbit: the derivative at the current state, then one step."""
    averages = []
    for _ in range(blocks):
        total = 0.0
        for _ in range(block_steps):
            slope = abs(r * (1.0 - 2.0 * x))
            if slope == 0.0:
                raise ArithmeticError(f"r = {r}: the orbit hit x = 1/2, where the derivative is 0")
            total += ln(slope)
            x = r * x * (1.0 - x)
        averages.append(total / block_steps)
    return averages


def known_exponent(label: str | None, r: float) -> float | None:
    if label is None:
        return None
    if label == "ln|2 - r|":
        return ln(abs(2.0 - r))
    if label == "0.5 * ln|4 + 2r - r^2|":
        return 0.5 * ln(abs(4.0 + 2.0 * r - r * r))
    if label == "ln 2":
        return LN2
    raise ValueError(f"unknown closed form for an exponent: {label!r}")


def settled_values(r: float, points: list[float], exponent: float, listed_at_most: int) -> dict | None:
    """Where the settled starting points are only a few numbers: each number, how many starts hold it, the size of
    the map's slope there, and how far one step and two steps of the map move it."""
    distinct = sorted(set(points))
    if len(distinct) > listed_at_most:
        return None
    slopes = [abs(r * (1.0 - 2.0 * x)) for x in distinct]
    product = 1.0
    for slope in slopes:
        product *= slope
    check("settled values: the product of the slope sizes at the n distinct values is e^(n * exponent), within 1e-9",
          abs(product - exp(len(distinct) * exponent)) < 1e-9, f"r = {r}: {product}")
    spread = distinct[-1] - distinct[0]
    out = {"values": [{"value": x, "starting_points": points.count(x), "slope_size": rnd(slope, "ratio")}
                      for x, slope in zip(distinct, slopes)],
           "product_of_the_slope_sizes": rnd(product, "ratio"),
           "largest_minus_smallest": sig(spread),
           "one_step_moves_a_value_by_at_most": sig(max(abs(step(r, x) - x) for x in distinct)),
           "two_steps_move_a_value_by_at_most": sig(max(abs(step(r, step(r, x)) - x) for x in distinct))}
    if spread < 1000 * SPACING:
        out["largest_minus_smallest_in_spacings_of_doubles"] = spread / SPACING  # exact: a division by a power of two
    return out


def perturbed(x: float, error: float) -> float:
    """The second run's start: moved toward the middle so that it stays inside the interval."""
    return x + error if x < 0.5 else x - error


def first_crossings(r: float, x: float, y: float, tolerances: list[float], max_steps: int) -> tuple[list, float]:
    """Steps until |x - y| first reaches each tolerance (ascending order); None where it never does.

    Also returns the gap at the last step that was run.
    """
    found: list = [None] * len(tolerances)
    index, gap = 0, abs(x - y)
    for n in range(1, max_steps + 1):
        x = r * x * (1.0 - x)
        y = r * y * (1.0 - y)
        gap = abs(x - y)
        while index < len(tolerances) and gap >= tolerances[index]:
            found[index] = n
            index += 1
        if index == len(tolerances) or gap == 0.0:  # two identical states stay identical
            break
    return found, gap


def summary(values: list[int]) -> dict:
    """Mean (rounded half up to 2 decimals from the exact integer total, which is kept), median, min and max."""
    if not values:
        return {"total": 0, "mean": None, "median": None, "min": None, "max": None}
    ordered = sorted(values)
    n, total = len(ordered), sum(ordered)
    median = ordered[n // 2] if n % 2 else (ordered[n // 2 - 1] + ordered[n // 2]) / 2
    return {"total": total, "mean": ((200 * total + n) // (2 * n)) / 100, "median": median,
            "min": ordered[0], "max": ordered[-1]}


def platform_guard() -> None:
    info = sys.float_info
    if (info.radix, info.mant_dig, sys.float_repr_style) != (2, 53, "short"):
        raise ArithmeticError("this Python does not use IEEE 754 doubles with shortest-repr formatting")
    seen = {"orbit": settle(4.0, 0.3, 50).hex(), "ln10": ln(10.0).hex(), "exp": exp(-0.3398).hex()}
    check("arithmetic fingerprint: an orbit, a logarithm and an exponential have the expected bits", seen == FINGERPRINT,
          f"got {seen}")
    grid = [0.001 * k for k in range(1, 4001)]
    check("series logarithm agrees with math.log within 1e-13 on 4,000 points",
          all(abs(ln(x) - math.log(x)) < 1e-13 for x in grid))
    check("series exponential agrees with math.exp within 1e-13 (relative) on 4,000 points",
          all(abs(exp(x - 25.0) / math.exp(x - 25.0) - 1.0) < 1e-13 for x in (0.0125 * k for k in range(4000))))
    check("ln(1) = 0, ln(1/2) = -ln 2 and exp(0) = 1 exactly", (ln(1.0), ln(0.5), exp(0.0)) == (0.0, -LN2, 1.0))


def regime_exponents(regimes: list[dict], cfg: dict, starts: dict, listed_at_most: int) -> dict:
    orbit, cited = cfg["long_orbit"], cfg["cited_comparison"]
    settings = cited["settings"]
    if (orbit["start"], orbit["discard_steps"], orbit["block_steps"]) != (
            settings["start"], settings["discard_steps"], settings["average_steps"]):
        raise ValueError("the first block of the long orbit must use the settings of the cited comparison")
    out = {}
    for regime in regimes:
        key, r = regime["key"], regime["r"]
        blocks = lyapunov_blocks(r, settle(r, orbit["start"], orbit["discard_steps"]), orbit["blocks"], orbit["block_steps"])
        estimate = sum(blocks) / len(blocks)
        spread = sum((b - estimate) * (b - estimate) for b in blocks) / (len(blocks) - 1)
        standard_error = math.sqrt(spread / len(blocks))  # square root: correctly rounded by IEEE 754
        known = known_exponent(regime["known_exponent"], r)
        if known is not None:
            tolerance = cfg["known_value_tolerance"][key]
            check(f"known answer: the exponent estimate at r = {r} is within {tolerance} of {regime['known_exponent']}",
                  abs(estimate - known) < tolerance, f"{estimate} against {known}")
        first_block = rnd(blocks[0], "exponent")
        quoted = cited["values_quoted_from_the_source"][str(r)]
        check("cited comparison: the first block (MAT-024's settings) equals the value MAT-024 prints, to 6 decimals",
              first_block == quoted, f"r = {r}: {first_block} against {quoted}")
        used = estimate if known is None else known
        points = starts[key]
        out[key] = {
            "r": r,
            "expected_attractor": regime["expected_attractor"],
            "starting_points": {"count": len(points), "distinct_values": len(set(points)),
                                "min": rnd(min(points), "state"), "max": rnd(max(points), "state"),
                                "settled_values": settled_values(r, points, used, listed_at_most)},
            "exponent_estimate": rnd(estimate, "exponent"),
            "estimate_steps": orbit["blocks"] * orbit["block_steps"],
            "estimate_blocks": {"blocks": len(blocks), "block_steps": orbit["block_steps"],
                                "min": rnd(min(blocks), "exponent"), "max": rnd(max(blocks), "exponent"),
                                "standard_error_of_the_estimate": rnd(standard_error, "exponent")},
            "exponent_known_formula": regime["known_exponent"],
            "exponent_known": None if known is None else rnd(known, "exponent"),
            "estimate_minus_known": None if known is None else rnd(estimate - known, "exponent"),
            "exponent_used": rnd(used, "exponent"),
            "exponent_used_is": "the estimate" if known is None else "the known value",
            "growth_factor_per_step": rnd(exp(used), "ratio"),
            "reading": "errors shrink" if used < 0 else "errors grow",
            "first_block_against_mat_024": {"first_block_estimate": first_block, "value_printed_in_mat_024": quoted},
            "_used": used,
        }
    return out


def gap_table(regimes: list[dict], cfg: dict, starts: dict) -> dict:
    error, wanted, rule = cfg["initial_error"], cfg["steps"], cfg["exponent_from_median_gaps"]
    if wanted[0] != 0 or wanted != sorted(wanted):
        raise ValueError("the tabulated steps must start at 0 and ascend")
    floor = rule["floor_in_spacings"] * SPACING
    by_regime, estimates = {}, []
    for regime in regimes:
        key, r = regime["key"], regime["r"]
        xs = list(starts[key])
        ys = [perturbed(x, error) for x in xs]
        medians, largest, identical, raw = [], [], [], {}
        for n in range(max(wanted) + 1):
            if n in wanted:
                raw[n] = [abs(a - b) for a, b in zip(xs, ys)]
                gaps = sorted(raw[n])
                half = len(gaps) // 2
                median = gaps[half] if len(gaps) % 2 else (gaps[half - 1] + gaps[half]) / 2
                medians.append(sig(median))
                largest.append(sig(gaps[-1]))
                identical.append(sum(gap == 0.0 for gap in gaps))
            xs = [r * x * (1.0 - x) for x in xs]
            ys = [r * y * (1.0 - y) for y in ys]
        by_regime[key] = {"r": r, "median_gap": medians, "largest_gap": largest, "pairs_with_identical_states": identical}
        usable = []
        for n, gap in zip(wanted[1:], medians[1:]):
            if not floor <= gap < rule["small_gap_limit"]:
                break
            usable.append(n)
        check("gap table: every regime has a usable later step for the exponent estimate", bool(usable))
        to_step = usable[-1]
        later = medians[wanted.index(to_step)]
        check("gap table: no pair has identical states at the step used for the exponent estimate", min(raw[to_step]) > 0.0)
        mean_log = sum(ln(b / a) for a, b in zip(raw[0], raw[to_step])) / len(raw[0])
        estimates.append({"regime": key, "r": r, "from_step": 0, "to_step": to_step, "earlier_gap": medians[0],
                          "later_gap": later, "ln_gap_ratio": rnd(ln(later / medians[0]), "ratio"),
                          "exponent": rnd(ln(later / medians[0]) / to_step, "ratio"),
                          "exponent_from_the_mean_of_ln_gap_ratios_of_all_pairs": rnd(mean_log / to_step, "ratio")})
    return {"definition": "Each starting point is run twice, the second run initial_error away; the gap is the absolute "
                          "difference between the two runs at the same step. Gaps are rounded to 3 significant digits.",
            "initial_error": error, "pairs": len(next(iter(starts.values()))), "steps": wanted, "by_regime": by_regime,
            "exponent_from_median_gaps": {
                "formula": "exponent = ln(later_gap / earlier_gap) / (to_step - from_step), from the rounded median gaps "
                           "above; the last field of each estimate averages ln(gap ratio) over the pairs instead, "
                           "from the unrounded gaps",
                "rule": rule["rule"], "small_gap_limit": rule["small_gap_limit"],
                "floor": {"spacings_of_doubles": rule["floor_in_spacings"], "value": sig(floor)},
                "estimates": estimates}}


def contraction(regime: dict, starts: list[float], cfg: dict, exponent: float) -> dict:
    """Where the exponent is negative: steps until an error has shrunk from initial_error to below target_error."""
    r, initial, target = regime["r"], cfg["initial_error"], cfg["target_error"]
    counts, growth, first_factors = [], 0.0, set()
    for x in starts:
        y = perturbed(x, initial)
        first = abs(x - y)
        for n in range(1, cfg["max_steps"] + 1):
            x = r * x * (1.0 - x)
            y = r * y * (1.0 - y)
            gap = abs(x - y)
            growth = max(growth, gap / first)
            if n == 1:
                first_factors.add(rnd(gap / first, "ratio"))
            if gap < target:
                counts.append(n)
                break
    check("contraction: every pair in a regime with a negative exponent falls below the target error",
          len(counts) == len(starts))
    formula = ln(target / initial) / exponent
    return {"r": r, "initial_error": initial, "target_error": target, "pairs": len(starts),
            "steps_formula": "ln(target_error / initial_error) / exponent",
            "steps_before_rounding_up": rnd(formula, "steps"), "steps_rounded_up": math.ceil(formula),
            "steps_measured": summary(counts),
            "gap_after_one_step_in_units_of_the_initial_gap": sorted(first_factors),
            "largest_gap_after_the_start_in_units_of_the_initial_gap": rnd(growth, "ratio")}


def horizon_tables(regimes: list[dict], cfg: dict, starts: dict, exponents: dict, realized_tolerance: float) -> dict:
    errors, tolerances, cap = cfg["initial_errors"], cfg["tolerances"], cfg["max_steps"]
    if tolerances != sorted(tolerances) or errors != sorted(errors, reverse=True):
        raise ValueError("tolerances must ascend and initial errors must descend")
    digits = ln(errors[0] / errors[-1]) / ln(10.0)
    if abs(digits - round(digits)) > 1e-9:
        raise ValueError("the first and last initial errors must differ by a whole number of decimal digits")
    digits = round(digits)
    by_regime, worst_realized = {}, 0.0
    for regime in regimes:
        key, r = regime["key"], regime["r"]
        exponent = exponents[key]["_used"]
        rows, final_gaps = [], []
        for error in errors:
            worst_realized = max(worst_realized, max(abs(abs(x - perturbed(x, error)) / error - 1.0) for x in starts[key]))
            runs = [first_crossings(r, x, perturbed(x, error), tolerances, cap) for x in starts[key]]
            final_gaps.extend(run[1] for run in runs)
            check("ordering: no pair reaches a looser tolerance before a tighter one",
                  all(a is None or (b is not None and b <= a) for run in runs for b, a in zip(run[0], run[0][1:])))
            for index, tolerance in enumerate(tolerances):
                reached = [run[0][index] for run in runs if run[0][index] is not None]
                never = sum(run[0][index] is None for run in runs)
                check("accounting: pairs reaching a tolerance + pairs not reaching it = pairs", len(reached) + never == len(runs))
                row = {"tolerance": tolerance, "initial_error": error, "pairs": len(runs),
                       "pairs_reaching_the_tolerance": len(reached), "pairs_not_reaching_it": never,
                       "steps": summary(reached), "_steps": reached}
                if exponent > 0:
                    row["formula_steps"] = rnd(ln(tolerance / error) / exponent, "steps")
                    row["mean_minus_formula"] = (None if not reached else
                                                 rnd(row["steps"]["mean"] - row["formula_steps"], "steps"))
                rows.append(row)
        entry = {"r": r, "exponent_used": rnd(exponent, "exponent"), "rows": rows}
        if exponent > 0:
            check("chaotic regime: every pair reaches every tolerance within the step limit",
                  all(row["pairs_not_reaching_it"] == 0 for row in rows))
            entry["steps_per_decimal_digit_formula"] = rnd(ln(10.0) / exponent, "steps")
            entry["steps_per_decimal_digit_measured"] = {}
            for tolerance in tolerances:
                means = [row["steps"]["mean"] for row in rows if row["tolerance"] == tolerance]
                check("chaotic regime: the mean horizon grows each time the initial error shrinks",
                      all(a < b for a, b in zip(means, means[1:])))
                entry["steps_per_decimal_digit_measured"][str(tolerance)] = {
                    "from_initial_error": errors[0], "to_initial_error": errors[-1], "decimal_digits_gained": digits,
                    "mean_steps_gained": rnd(means[-1] - means[0], "steps"),
                    "steps_per_digit": rnd((means[-1] - means[0]) / digits, "steps")}
        else:
            entry["pairs_reaching_any_tolerance"] = sum(row["pairs_reaching_the_tolerance"] for row in rows)
            entry["largest_gap_at_the_last_step"] = sig(max(final_gaps))
            entry["pairs_ending_with_identical_states"] = sum(gap == 0.0 for gap in final_gaps)
            entry["pair_runs"] = len(final_gaps)
            entry["pair_error_and_tolerance_combinations"] = len(final_gaps) * len(tolerances)
            entry["distinct_pair_error_and_tolerance_combinations"] = len(
                {(x, error, tolerance) for x in starts[key] for error in errors for tolerance in tolerances})
        by_regime[key] = entry
    check(f"initial errors: every realized starting gap is within {realized_tolerance} (relative) of the stated error",
          worst_realized < realized_tolerance, f"worst {worst_realized}")
    return {"definition": "Horizon of a pair = the first step at which its two runs differ by at least the tolerance. "
                          "formula_steps = ln(tolerance / initial_error) / exponent. mean_minus_formula and steps_per_digit "
                          "are computed from the rounded figures of this table, so that they can be checked by hand.",
            "max_steps": cap, "tolerances": tolerances, "initial_errors": errors,
            "largest_relative_deviation_of_a_realized_starting_gap": sig(worst_realized),
            "by_regime": by_regime}


def hypothesis_test(horizon: dict, thresholds: dict, lesson_tolerance: float) -> dict:
    """The thresholds were written before the first run; this only reports which of them hold."""
    chaotic, calm = {}, {}
    for key, entry in horizon["by_regime"].items():
        if "steps_per_decimal_digit_formula" not in entry:
            calm[key] = entry["pairs_reaching_any_tolerance"]
            continue
        slope = entry["steps_per_decimal_digit_measured"][str(lesson_tolerance)]["steps_per_digit"]
        offsets = [row["mean_minus_formula"] for row in entry["rows"] if row["tolerance"] == lesson_tolerance]
        ratio = slope / entry["steps_per_decimal_digit_formula"]
        chaotic[key] = {
            "steps_per_digit_measured_over_formula": rnd(ratio, "ratio"),
            "slope_within_threshold": abs(ratio - 1.0) <= thresholds["steps_per_digit_within_fraction_of_formula"],
            "offset_min": min(offsets), "offset_max": max(offsets),
            "offset_within_threshold": max(abs(o) for o in offsets) <= thresholds["offset_from_formula_at_most_steps"],
            "offset_range": rnd(max(offsets) - min(offsets), "steps"),
            "offset_range_within_threshold": max(offsets) - min(offsets) < thresholds["offset_varies_by_less_than_steps"]}
    supported = (all(v["slope_within_threshold"] and v["offset_within_threshold"] and v["offset_range_within_threshold"]
                     for v in chaotic.values()) and all(count == 0 for count in calm.values()))
    return {"thresholds": {k: v for k, v in thresholds.items() if k != "note"}, "tolerance": lesson_tolerance,
            "chaotic_regimes": chaotic, "pairs_reaching_a_tolerance_where_the_exponent_is_negative": calm,
            "every_part_holds": supported}


def double_precision(regimes: list[dict], cfg: dict, starts: dict, exponents: dict) -> dict:
    tolerance, cap, bound = cfg["tolerance"], cfg["max_steps"], cfg["first_difference_at_most_spacings"]
    forms = {}
    for regime in regimes:
        key, r = regime["key"], regime["r"]
        exponent = exponents[key]["_used"]
        if exponent <= 0:
            continue
        counts, first_steps, first_sizes = [], [], []
        for start in starts[key]:
            a = b = start
            differed = False
            for n in range(1, cap + 1):
                a = r * a * (1.0 - a)
                b = r * b - r * b * b
                gap = abs(a - b)
                if gap > 0.0 and not differed:
                    differed = True
                    first_steps.append(n)
                    first_sizes.append(gap / SPACING)  # exact: a division by a power of two
                if gap >= tolerance:
                    counts.append(n)
                    break
        check("two forms: every pair of runs separates within the step limit", len(counts) == len(starts[key]))
        check(f"two forms: the first difference between the two runs is at most {bound} spacings of doubles",
              max(first_sizes) <= bound, f"largest {max(first_sizes)}")
        forms[key] = {"r": r, "pairs": len(starts[key]),
                      "first_step_with_a_difference": {k: v for k, v in summary(first_steps).items() if k != "total"},
                      "largest_first_difference_in_spacings_of_doubles": max(first_sizes),
                      "steps_until_the_two_forms_differ_by_the_tolerance": summary(counts),
                      "formula_steps_for_an_initial_error_of_one_spacing": rnd(ln(tolerance / SPACING) / exponent, "steps")}
    wanted = cfg["wanted_horizon"]
    exponent = exponents[wanted["regime"]]["_used"]
    required = wanted["tolerance"] * exp(-exponent * wanted["steps"])
    return {
        "spacing_of_doubles_between_one_half_and_one": {"exact": "2^-53", "value": sig(SPACING),
                                                         "decimal_digits": rnd(-ln(SPACING) / ln(10.0), "steps")},
        "two_forms_of_the_same_map": {"forms": cfg["two_forms"], "tolerance": tolerance, "by_regime": forms},
        "wanted_horizon": {
            "regime": wanted["regime"], "r": exponents[wanted["regime"]]["r"], "steps": wanted["steps"],
            "tolerance": wanted["tolerance"], "exponent_used": rnd(exponent, "exponent"),
            "formula": "required initial error = tolerance * e^(-exponent * steps)",
            "required_initial_error": sig(required),
            "required_decimal_digits": rnd(-ln(required) / ln(10.0), "steps"),
            "achievable_with_a_double": required >= SPACING,
            "longest_formula_horizon_with_a_double": rnd(ln(wanted["tolerance"] / SPACING) / exponent, "steps")},
    }


def beyond_the_horizon(cfg: dict, regimes: list[dict], starts: dict, horizon_cfg: dict) -> dict:
    regime = next(item for item in regimes if item["key"] == cfg["regime"])
    r, threshold, steps = regime["r"], cfg["threshold"], cfg["steps"]
    x, y = cfg["start"], cfg["start"] + cfg["second_start_offset"]
    crossing = first_crossings(r, x, y, [horizon_cfg["lesson_tolerance"]], horizon_cfg["max_steps"])[0][0]
    below_x = below_y = above_x = above_y = 0
    snapshot = None
    for n in range(steps):
        if n == cfg["compare_states_at_step"]:
            snapshot = (x, y)
        below_x += x < threshold
        below_y += y < threshold
        above_x += x >= threshold
        above_y += y >= threshold
        x = r * x * (1.0 - x)
        y = r * y * (1.0 - y)
    check("accounting: steps below the threshold + steps at or above it = steps",
          below_x + above_x == steps and below_y + above_y == steps)
    known = Fraction(cfg["known_share"])
    for count in (below_x, below_y):
        check("known answer: at r = 4 the share of steps below 0.25 is within 0.01 of 1/3",
              abs(Fraction(count, steps) - known) < Fraction(str(cfg["known_share_tolerance"])))
    short = cfg["short_runs"]
    shares = []
    for start in starts[cfg["regime"]][:short["starts_used"]]:
        below = 0
        for _ in range(short["steps"]):
            below += start < threshold
            start = r * start * (1.0 - start)
        shares.append(below / short["steps"])
    return {
        "r": r, "first_start": cfg["start"], "second_start": cfg["start"] + cfg["second_start_offset"],
        "initial_error": cfg["second_start_offset"],
        "first_step_at_which_the_two_runs_differ_by_the_lesson_tolerance": crossing,
        "states_at_step": {"step": cfg["compare_states_at_step"], "first_run": rnd(snapshot[0], "state"),
                           "second_run": rnd(snapshot[1], "state"), "gap": rnd(abs(snapshot[0] - snapshot[1]), "state")},
        "share_of_steps_below_threshold": {
            "threshold": threshold, "steps": steps, "first_run_count": below_x, "second_run_count": below_y,
            "first_run": rnd(below_x / steps, "share"), "second_run": rnd(below_y / steps, "share"),
            "known_value": {"exact": cfg["known_share"], "value": rnd(float(known), "share"),
                            "reason": cfg["known_share_reason"]}},
        "short_runs": {"count": len(shares), "steps": short["steps"], "share_min": rnd(min(shares), "share"),
                       "share_max": rnd(max(shares), "share")},
    }


def wide_gap_table(regimes: list[dict], cfg: dict, starts: dict, exponents: dict, gaps: dict, agreement: dict) -> dict:
    """The gap table again where the exponent is negative: there the gaps fall below the spacing of doubles."""
    error, wanted = cfg["initial_error"], cfg["steps"]
    spacings, fraction = agreement["where_the_median_gap_in_doubles_is_at_least_spacings"], agreement["within_fraction"]
    out = {}
    for regime in regimes:
        key, r = regime["key"], regime["r"]
        exponent = exponents[key]["_used"]
        if exponent >= 0:
            continue
        wide_step, runs = wide_map(r), {}
        for start in set(starts[key]):  # pairs with the same start are the same run
            x, y, row = to_wide(start), to_wide(perturbed(start, error)), []
            for n in range(max(wanted) + 1):
                if n in wanted:
                    row.append(abs(x - y))
                x, y = wide_step(x), wide_step(y)
            runs[start] = row
        medians = []
        for index in range(len(wanted)):
            ordered = sorted(runs[start][index] for start in starts[key])
            half = len(ordered) // 2
            twice = 2 * ordered[half] if len(ordered) % 2 else ordered[half - 1] + ordered[half]
            medians.append(sig(twice / (2 * WIDE_ONE)))
        in_doubles = gaps["by_regime"][key]["median_gap"]
        compared = [(a, b) for a, b in zip(in_doubles, medians) if a >= spacings * SPACING]
        check(f"high precision: a median gap of at least {spacings} spacings in doubles is within {fraction} "
              "(relative) of the high-precision one", len(compared) > 1 and all(abs(a / b - 1.0) < fraction for a, b in compared))
        out[key] = {"r": r, "pairs": len(starts[key]), "distinct_pairs": len(runs), "steps": wanted,
                    "median_gap": medians, "median_gap_in_doubles": in_doubles,
                    "growth_law": [sig(error * exp(exponent * n)) for n in wanted],
                    "steps_compared_with_the_doubles": len(compared)}
    return out


def wide_beyond(cfg: dict, regimes: list[dict], tolerance: float) -> dict:
    """The two runs of beyond_the_horizon again: where the high-precision runs separate, where each double run leaves
    the high-precision run of its own start, and the states at the compared step in each arithmetic."""
    regime = next(item for item in regimes if item["key"] == cfg["regime"])
    r, at, limit = regime["r"], cfg["compare_states_at_step"], to_wide(tolerance)
    starts = [cfg["start"], cfg["start"] + cfg["second_start_offset"]]
    wide_step, wide = wide_map(r), [to_wide(x) for x in starts]
    first, second = list(starts), list(starts)  # the two forms of the map, in doubles
    crossing, leaves = None, [None, None]
    for n in range(1, at + 1):
        wide = [wide_step(x) for x in wide]
        first = [r * x * (1.0 - x) for x in first]
        second = [r * x - r * x * x for x in second]
        if crossing is None and abs(wide[0] - wide[1]) >= limit:
            crossing = n
        for index in (0, 1):
            if leaves[index] is None and abs(to_wide(first[index]) - wide[index]) >= limit:
                leaves[index] = n
    check("high precision: before the compared step, the two runs separate and each double run leaves its own",
          crossing is not None and None not in leaves, f"{crossing}, {leaves}")
    return {
        "r": r, "first_start": starts[0], "second_start": starts[1],
        "starts": "the same two doubles as in beyond_the_horizon, converted exactly",
        "first_step_at_which_the_two_runs_differ_by_the_lesson_tolerance": crossing,
        "first_step_at_which_the_double_run_is_the_lesson_tolerance_from_the_run_of_its_own_start":
            {"first_run": leaves[0], "second_run": leaves[1]},
        "states_at_step": {
            "step": at,
            "high_precision": {"first_run": rnd(wide[0] / WIDE_ONE, "state"), "second_run": rnd(wide[1] / WIDE_ONE, "state")},
            "in_doubles": {"form": "r * x * (1 - x)", "first_run": rnd(first[0], "state"),
                           "second_run": rnd(first[1], "state")},
            "in_doubles_with_the_other_form": {"form": "r * x - r * x * x", "first_run": rnd(second[0], "state"),
                                               "second_run": rnd(second[1], "state")}},
    }


def wide_horizons(regimes: list[dict], cfg: dict, starts: dict, exponents: dict, horizon: dict, cap: int) -> dict:
    """The horizons of the lesson's tolerance again, and how long a double run follows the high-precision run."""
    tolerance = cfg["lesson_tolerance"]
    limit, out = to_wide(tolerance), {}
    for regime in regimes:
        key, r = regime["key"], regime["r"]
        if exponents[key]["_used"] <= 0:
            continue
        wide_step, rows = wide_map(r), []
        for row in horizon["by_regime"][key]["rows"]:
            if row["tolerance"] != tolerance:
                continue
            counts = []
            for start in starts[key]:
                x, y = to_wide(start), to_wide(perturbed(start, row["initial_error"]))
                for n in range(1, cap + 1):
                    x, y = wide_step(x), wide_step(y)
                    if abs(x - y) >= limit:
                        counts.append(n)
                        break
            check("high precision: every pair of a chaotic regime reaches the tolerance within the step limit",
                  len(counts) == len(starts[key]) == len(row["_steps"]))
            moved = [abs(a - b) for a, b in zip(counts, row["_steps"])]
            rows.append({"initial_error": row["initial_error"], "pairs": len(counts), "steps": summary(counts),
                         "mean_steps_in_doubles": row["steps"]["mean"],
                         "pairs_whose_horizon_differs_from_the_double_runs": sum(d > 0 for d in moved),
                         "largest_difference_in_steps": max(moved)})
        follows = []
        for start in starts[key]:
            x, w = start, to_wide(start)
            for n in range(1, cap + 1):
                x, w = r * x * (1.0 - x), wide_step(w)
                if abs(to_wide(x) - w) >= limit:
                    follows.append(n)
                    break
        check("high precision: every double run leaves the high-precision run of its start within the step limit",
              len(follows) == len(starts[key]))
        digits = horizon["by_regime"][key]["steps_per_decimal_digit_measured"][str(tolerance)]["decimal_digits_gained"]
        gained = rows[-1]["steps"]["mean"] - rows[0]["steps"]["mean"]
        out[key] = {"r": r, "tolerance": tolerance, "rows": rows,
                    "horizons": sum(item["pairs"] for item in rows),
                    "horizons_that_differ_from_the_double_runs":
                        sum(item["pairs_whose_horizon_differs_from_the_double_runs"] for item in rows),
                    "largest_difference_in_steps": max(item["largest_difference_in_steps"] for item in rows),
                    "largest_difference_between_the_two_means": rnd(max(
                        abs(item["steps"]["mean"] - item["mean_steps_in_doubles"]) for item in rows), "steps"),
                    "mean_steps_gained": rnd(gained, "steps"), "decimal_digits_gained": digits,
                    "steps_per_digit": rnd(gained / digits, "steps"),
                    "steps_until_a_double_run_is_the_tolerance_from_the_run_of_its_own_start": summary(follows)}
    return out


def high_precision(scenarios: dict, starts: dict, exponents: dict, gaps: dict, horizon: dict) -> dict:
    cfg, regimes, hand = scenarios["high_precision"], scenarios["regimes"], scenarios["negative_controls"]["hand_computed_case"]
    cap = cfg["max_steps"]
    if cfg["bits"] != WIDE_BITS or any(not 0.0 < regime["r"] <= 4.0 for regime in regimes):
        raise ValueError("the high-precision runs need the stated number of bits and 0 < r <= 4")
    if max(scenarios["gap_table"]["steps"]) > cap or scenarios["beyond_the_horizon"]["compare_states_at_step"] > cap:
        raise ValueError("a high-precision run would be longer than max_steps")
    bound = wide_error_bound(cap)
    check(f"high precision: the error bound after {cap} steps is below {cfg['error_bound_must_stay_below']}",
          bound < cfg["error_bound_must_stay_below"], f"{bound}")
    h = math.ldexp(1.0, hand["error_power_of_two"])  # 4 (3/4 - h) (1/4 + h) = 3/4 + 2h - 4h^2, exact in doubles too
    wide_step = wide_map(hand["r"])
    check("high precision: known answer, one step from 3/4 - 2^-10 at r = 4 is exactly 3/4 + 2^-9 - 2^-18, and 3/4 stays",
          wide_step(to_wide(hand["start"] - h)) == to_wide(hand["start"] + 2.0 * h - 4.0 * h * h)
          == to_wide(step(hand["r"], hand["start"] - h)) and wide_step(to_wide(hand["start"])) == to_wide(hand["start"]))
    return {
        "arithmetic": f"Python integers: a state is a whole number of 2^-{WIDE_BITS} (about {WIDE_BITS * 30103 // 100000} "
                      "decimal digits); one step is r * x * (1 - x) with exact products and one truncation, for the exact "
                      "value of the double r and from the same starting doubles as the other sections",
        "bits": WIDE_BITS, "max_steps": cap,
        "error_bound": {"formula": "(4^steps - 1) / 3 * 2^-bits: one step multiplies an earlier error by at most 4 and "
                                   "truncates by less than 2^-bits",
                        "steps": cap, "value": sig(bound)},
        "gap_table_where_the_exponent_is_negative": wide_gap_table(
            regimes, scenarios["gap_table"], starts, exponents, gaps, cfg["agreement_with_doubles"]),
        "beyond_the_horizon": wide_beyond(scenarios["beyond_the_horizon"], regimes, scenarios["horizon"]["lesson_tolerance"]),
        "horizon": wide_horizons(regimes, scenarios["horizon"], starts, exponents, horizon, cap),
    }


def negative_controls(cfg: dict, regimes: list[dict], starts: dict, horizon: dict, horizon_cfg: dict) -> dict:
    hand = cfg["hand_computed_case"]
    error = math.ldexp(1.0, hand["error_power_of_two"])
    tolerances = sorted(float(key) for key in hand["expected_first_step_at_or_above"])
    x, y = hand["start"], perturbed(hand["start"], error)
    found = first_crossings(hand["r"], x, y, tolerances, 100)[0]
    expected = [hand["expected_first_step_at_or_above"][str(t)] for t in tolerances]
    check("hand-computed case: r = 4, runs at 0.75 and 0.75 - 2^-10 differ by 0.01 at step 4 and by 0.1 at step 7",
          found == expected, f"got {found}")
    gaps = [rnd(abs(x - y), "state")]
    for _ in range(hand["steps_listed"]):
        x, y = step(hand["r"], x), step(hand["r"], y)
        gaps.append(rnd(abs(x - y), "state"))
    check("hand-computed case: the first run stays exactly on the fixed point 0.75", x == hand["start"])

    phase = cfg["phase_error"]
    regime = next(item for item in regimes if item["key"] == phase["regime"])
    r = regime["r"]
    x = starts[phase["regime"]][0]
    y = step(r, x)  # the other point of the cycle
    first_gap = abs(x - y)
    crossing = first_crossings(r, x, y, [horizon_cfg["lesson_tolerance"]], horizon_cfg["max_steps"])[0][0]
    for _ in range(phase["check_steps"]):
        x, y = step(r, x), step(r, y)
    check("negative control: the crossing detector fires in the two-cycle regime when the error is a phase error",
          crossing == 1 and abs(x - y) >= horizon_cfg["lesson_tolerance"])
    check("negative control: the zero count of the two-cycle regime comes from the same detector",
          horizon["by_regime"][phase["regime"]]["pairs_reaching_any_tolerance"] == 0)
    reached = {key: sum(row["pairs_reaching_the_tolerance"] for row in entry["rows"])
               for key, entry in horizon["by_regime"].items()}
    runs = {key: sum(row["pairs"] for row in entry["rows"]) for key, entry in horizon["by_regime"].items()}
    return {
        "hand_computed_case": {"r": hand["r"], "first_run": hand["start"], "second_run": perturbed(hand["start"], error),
                               "gap_at_steps_0_to_7": gaps, "tolerances": tolerances, "first_step_at_or_above": found,
                               "expected_by_hand": expected},
        "detector_counts_by_regime": {key: {"pair_and_tolerance_combinations": runs[key], "reached": reached[key]}
                                      for key in reached},
        "phase_error_in_the_two_cycle": {
            "note": phase["note"], "r": r, "initial_gap": sig(first_gap),
            "first_step_at_or_above_the_lesson_tolerance": crossing,
            "gap_after_steps": {"steps": phase["check_steps"], "gap": sig(abs(x - y))}},
    }


def re_measured(r: float, starts: list[float], error: float, tolerance: float, span: int, interval: int) -> int:
    """Forecasts that stay within the tolerance at every step of the span when the state is measured again every
    `interval` steps: at each measurement the forecast run restarts from the true state with a fresh error."""
    kept = 0
    for x in starts:
        y = perturbed(x, error)
        for n in range(1, span + 1):
            x = r * x * (1.0 - x)
            y = r * y * (1.0 - y)
            if abs(x - y) >= tolerance:
                break
            if n % interval == 0:
                y = perturbed(x, error)
        else:
            kept += 1
    return kept


def exercise_5(ex5: dict, exponents: dict, horizon: dict, starts: dict) -> dict:
    """Measure better once (option A) or measure again every k steps (option B), for a forecast over a wanted span."""
    r, exponent = exponents[ex5["regime"]]["r"], exponents[ex5["regime"]]["_used"]
    tolerance, span, wanted = ex5["tolerance"], ex5["wanted_span_steps"], ex5["wanted_share_of_forecasts"]
    rows = {(row["tolerance"], row["initial_error"]): row for row in horizon["by_regime"][ex5["regime"]]["rows"]}
    row_a, row_b = rows[(tolerance, ex5["option_a_initial_error"])], rows[(tolerance, ex5["option_b_initial_error"])]
    interval, pairs, shortest = ex5["option_b_re_measure_every"], row_b["pairs"], row_b["steps"]["min"]
    check("worked example: the re-measuring interval is the formula horizon of option B rounded down",
          interval == math.floor(ln(tolerance / ex5["option_b_initial_error"]) / exponent))
    by_interval = []
    for k in ex5["intervals_tabulated"]:
        one = sum(s > k for s in row_b["_steps"])
        check("worked example: over a span of one interval, the re-measured forecasts are the pairs that last the interval",
              re_measured(r, starts[ex5["regime"]], ex5["option_b_initial_error"], tolerance, k, k) == one)
        whole = re_measured(r, starts[ex5["regime"]], ex5["option_b_initial_error"], tolerance, span, k)
        by_interval.append({"interval_steps": k, "pairs_within_tolerance_through_the_interval": one,
                            "share": rnd(one / pairs, "share"), "measurements_over_the_wanted_span": math.ceil(span / k),
                            "forecasts_within_tolerance_through_the_wanted_span": whole,
                            "share_through_the_wanted_span": rnd(whole / pairs, "share")})
    counts = [item["pairs_within_tolerance_through_the_interval"] for item in by_interval]
    check("worked example: fewer pairs stay within tolerance as the interval grows",
          all(a >= b for a, b in zip(counts, counts[1:])) and counts[0] <= pairs)
    check("worked example: all pairs stay within tolerance for fewer steps than the shortest horizon",
          sum(s > shortest - 1 for s in row_b["_steps"]) == pairs and sum(s > shortest for s in row_b["_steps"]) < pairs)
    check("worked example: no more forecasts last the whole span than pairs last one interval",
          all(item["forecasts_within_tolerance_through_the_wanted_span"] <= item["pairs_within_tolerance_through_the_interval"]
              for item in by_interval))
    one_ok = [item["interval_steps"] for item in by_interval if item["share"] >= wanted]
    span_ok = [item["interval_steps"] for item in by_interval if item["share_through_the_wanted_span"] >= wanted]
    return {
        "r": r, "tolerance": tolerance, "wanted_span_steps": span,
        "option_a": {"initial_error": ex5["option_a_initial_error"], "formula_steps": row_a["formula_steps"],
                     "measured_mean_steps": row_a["steps"]["mean"], "measured_max_steps": row_a["steps"]["max"],
                     "pairs": row_a["pairs"],
                     "pairs_within_tolerance_through_the_wanted_span": sum(s > span for s in row_a["_steps"])},
        "option_b": {"initial_error": ex5["option_b_initial_error"], "formula_steps": row_b["formula_steps"],
                     "measured_mean_steps": row_b["steps"]["mean"], "measured_min_steps": shortest,
                     "measured_max_steps": row_b["steps"]["max"], "re_measure_every": interval, "pairs": pairs,
                     "definition": "A pair stays within tolerance through an interval of k steps when its horizon (first "
                                   "step at or above the tolerance) is later than k. A forecast stays within tolerance "
                                   "through the wanted span when the gap is below the tolerance at every step of it, the "
                                   "forecast run restarting from the true state with a fresh initial error every k steps.",
                     "by_interval": by_interval,
                     "wanted_share_of_forecasts": wanted,
                     "longest_interval_with_the_wanted_share_through_one_interval": max(one_ok) if one_ok else None,
                     "longest_interval_with_the_wanted_share_through_the_wanted_span": max(span_ok) if span_ok else None,
                     "measurements_over_the_wanted_span_at_that_interval":
                         None if not span_ok else math.ceil(span / max(span_ok)),
                     "longest_interval_that_keeps_every_pair": shortest - 1},
    }


def worked_examples(cfg: dict, exponents: dict, gaps: dict, shrink: dict, horizon: dict, precision: dict,
                    starts: dict) -> dict:
    stable = shrink["stable_fixed_point"]
    table = gaps["by_regime"]["stable_fixed_point"]["median_gap"]

    ex3 = cfg["exercise_3"]
    given = round(exponents[ex3["regime"]]["_used"], ex3["exponent_decimals_given"])
    per_digit = ln(10.0) / given
    digits = ln(ex3["initial_error"] / ex3["improved_initial_error"]) / ln(10.0)
    rows3 = {(row["tolerance"], row["initial_error"]): row for row in horizon["by_regime"][ex3["regime"]]["rows"]}
    first = ln(ex3["tolerance"] / ex3["initial_error"]) / given
    second = ln(ex3["tolerance"] / ex3["improved_initial_error"]) / given
    check("worked example: the horizon gained equals digits gained times steps per digit",
          abs((second - first) - digits * per_digit) < 1e-9)
    return {
        "exercise_1": {
            "r": stable["r"], "factor_per_step": exponents["stable_fixed_point"]["growth_factor_per_step"],
            "factor_over_ten_steps_from_the_gap_table": rnd(table[1] / table[0], "ratio"),
            "initial_error": stable["initial_error"], "target_error": stable["target_error"],
            "steps_before_rounding_up": stable["steps_before_rounding_up"], "steps_rounded_up": stable["steps_rounded_up"],
            "steps_measured_min": stable["steps_measured"]["min"], "steps_measured_max": stable["steps_measured"]["max"]},
        "exercise_2": {"estimates": [item for item in gaps["exponent_from_median_gaps"]["estimates"]
                                     if item["regime"] in ("chaotic_r4", "periodic_two_cycle")]},
        "exercise_3": {
            "r": exponents[ex3["regime"]]["r"], "exponent_given": given, "tolerance": ex3["tolerance"],
            "initial_error": ex3["initial_error"], "formula_steps": rnd(first, "steps"),
            "measured_mean_steps": rows3[(ex3["tolerance"], ex3["initial_error"])]["steps"]["mean"],
            "improved_initial_error": ex3["improved_initial_error"], "decimal_digits_gained": round(digits),
            "steps_per_decimal_digit": rnd(per_digit, "steps"),
            "steps_gained": rnd(second - first, "steps"),
            "steps_gained_over_formula_steps": rnd((second - first) / first, "ratio"),
            "formula_steps_improved": rnd(second, "steps"),
            "measured_mean_steps_improved": rows3[(ex3["tolerance"], ex3["improved_initial_error"])]["steps"]["mean"]},
        "exercise_4": precision["wanted_horizon"] | {
            "decimal_digits_of_a_double": precision["spacing_of_doubles_between_one_half_and_one"]["decimal_digits"]},
        "exercise_5": exercise_5(cfg["exercise_5"], exponents, horizon, starts),
    }


def transfer_task(task: dict) -> dict:
    tolerance, wanted = task["tolerance"], task["wanted_horizon_steps"]
    measured, improved = task["initial_error_measured"], task["initial_error_improved"]
    configurations, exponents = {}, {}
    for name, cfg in task["configurations"].items():
        log_ratio = ln(cfg["later_gap"] / cfg["initial_gap"])
        exponent = exponents[name] = log_ratio / cfg["steps_between"]
        configurations[name] = {
            "initial_gap": cfg["initial_gap"], "later_gap": cfg["later_gap"], "steps_between": cfg["steps_between"],
            "ln_gap_ratio": rnd(log_ratio, "ratio"), "exponent_per_step": rnd(exponent, "exponent"),
            "growth_factor_per_step": rnd(exp(exponent), "ratio"),
            "reading": "errors shrink" if exponent < 0 else "errors grow"}
    check("transfer task: one configuration shrinks errors and the other grows them",
          exponents["calm"] < 0 < exponents["busy"])
    busy, calm = exponents["busy"], exponents["calm"]
    per_digit = ln(10.0) / busy
    first = ln(tolerance / measured) / busy
    second = ln(tolerance / improved) / busy
    digits = ln(measured / improved) / ln(10.0)
    check("transfer task: the horizon gained equals digits gained times steps per digit",
          abs((second - first) - digits * per_digit) < 1e-9)
    required = tolerance * exp(-busy * wanted)
    places = -ln(required) / ln(10.0)
    check("transfer task: the required error reproduces the wanted horizon",
          abs(ln(tolerance / required) / busy - wanted) < 1e-9)
    return {
        "note": task["note"], "time_unit": task["time_unit"],
        "q1_exponents": configurations,
        "q2_busy_rates": {"steps_for_an_error_to_double": rnd(LN2 / busy, "steps"),
                          "steps_per_decimal_digit": rnd(per_digit, "steps")},
        "q3_horizons": {
            "tolerance": tolerance,
            "busy": {"initial_error": measured, "horizon_steps": rnd(first, "steps"),
                     "improved_initial_error": improved, "decimal_digits_gained": round(digits),
                     "horizon_steps_improved": rnd(second, "steps"),
                     "steps_gained": rnd(second - first, "steps")},
            "calm": {"initial_error": measured, "error_after_the_wanted_horizon": sig(measured * exp(calm * wanted)),
                     "reading": "the error shrinks, so no horizon limits the forecast"}},
        "q4_wanted_horizon": {
            "steps": wanted, "required_initial_error": sig(required),
            "required_decimal_places_before_rounding_up": rnd(places, "steps"), "required_decimal_places": math.ceil(places),
            "decimal_places_of_the_measured_start": round(-ln(measured) / ln(10.0)),
            "extra_digits_before_rounding_up": rnd((wanted - first) / per_digit, "steps"),
            "extra_digits_needed": math.ceil((wanted - first) / per_digit)},
    }


def strip_private(value):
    if isinstance(value, dict):
        return {key: strip_private(item) for key, item in value.items() if not key.startswith("_")}
    if isinstance(value, list):
        return [strip_private(item) for item in value]
    return value


def analyze(scenarios: dict) -> dict:
    rounding = {f"{key}_decimals": value for key, value in DECIMALS.items()} | {"gap_significant_digits": GAP_DIGITS}
    if scenarios["rounding"] != rounding:
        raise ValueError("scenarios.json rounding does not match analyze.py")
    platform_guard()
    regimes = scenarios["regimes"]
    starts = {regime["key"]: seeded_starts(regime["r"], scenarios["starting_points"]) for regime in regimes}
    exponents = regime_exponents(regimes, scenarios["lyapunov"], starts,
                                 scenarios["starting_points"]["list_settled_values_when_at_most"])
    gaps = gap_table(regimes, scenarios["gap_table"], starts)
    shrink = {regime["key"]: contraction(regime, starts[regime["key"]], scenarios["contraction"], exponents[regime["key"]]["_used"])
              for regime in regimes if exponents[regime["key"]]["_used"] < 0}
    horizon = horizon_tables(regimes, scenarios["horizon"], starts, exponents, scenarios["realized_error_tolerance"])
    for key, entry in horizon["by_regime"].items():
        if exponents[key]["_used"] < 0:
            check("negative exponent: no pair reaches a tolerance, and every gap ends below the stated floor",
                  entry["pairs_reaching_any_tolerance"] == 0
                  and entry["largest_gap_at_the_last_step"] < scenarios["horizon"]["indistinguishable_below"])
    precision = double_precision(regimes, scenarios["double_precision"], starts, exponents)
    beyond = beyond_the_horizon(scenarios["beyond_the_horizon"], regimes, starts, scenarios["horizon"])
    wide = high_precision(scenarios, starts, exponents, gaps, horizon)
    controls = negative_controls(scenarios["negative_controls"], regimes, starts, horizon, scenarios["horizon"])
    worked = worked_examples(scenarios["worked_examples"], exponents, gaps, shrink, horizon, precision, starts)
    transfer = transfer_task(scenarios["transfer_task"])
    verdict = hypothesis_test(horizon, scenarios["hypothesis_thresholds"], scenarios["horizon"]["lesson_tolerance"])
    return strip_private({
        "module_id": scenarios["module_id"],
        "kind": "synthetic: every number below comes from the logistic map and the assumptions in scenarios.json; "
                "nothing is measured in the Demerzel repository",
        "rounding": "exponents to 6 decimals, step counts and digits to 2 decimals, shares and ratios to 4 decimals, "
                    "states to 6 decimals, gaps and required errors to 3 significant digits; a mean of step counts is "
                    "rounded half up from the integer total stored next to it",
        "arithmetic": "IEEE 754 doubles with +, -, * and / only, plus one correctly rounded square root; ln and exp are "
                      "series built from those operations; random.Random(seed).random() supplies the starting points; "
                      "the section high_precision repeats some runs on Python integers",
        "map": scenarios["map"],
        "starting_points": {key: scenarios["starting_points"][key] for key in ("seed", "count", "draw", "settle_steps")},
        "perturbation_rule": scenarios["perturbation_rule"],
        "regimes": exponents,
        "lyapunov_settings": {"long_orbit": scenarios["lyapunov"]["long_orbit"],
                              "cited_comparison_source": scenarios["lyapunov"]["cited_comparison"]["source"],
                              "cited_comparison_settings": scenarios["lyapunov"]["cited_comparison"]["settings"]},
        "gap_table": gaps,
        "contraction": shrink,
        "horizon": horizon,
        "double_precision": precision,
        "beyond_the_horizon": beyond,
        "high_precision": wide,
        "hypothesis_test": verdict,
        "worked_examples": worked,
        "negative_controls": controls,
        "transfer_task": transfer,
        "checks": [{"check": name, "times_evaluated": times, "passed": True} for name, times in CHECKS.items()],
    })


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--scenarios", type=Path, default=HERE / "scenarios.json")
    parser.add_argument("--output", type=Path, default=HERE / "results.json")
    parser.add_argument("--check", action="store_true",
                        help="recompute and compare with the output file instead of writing it")
    args = parser.parse_args()
    CHECKS.clear()
    try:
        result = analyze(json.loads(args.scenarios.read_text(encoding="utf-8")))
    except (AssertionError, ArithmeticError, KeyError, ValueError, OSError) as exc:
        print(f"analyze.py: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 1
    text = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.check:
        try:
            saved = args.output.read_bytes()
        except OSError as exc:
            print(f"analyze.py: cannot read {args.output}: {exc}", file=sys.stderr)
            return 1
        same = saved.replace(b"\r\n", b"\n") == text.encode("utf-8")
        print(f"analyze.py: {args.output.name} {'matches' if same else 'DIFFERS FROM'} a fresh run "
              f"({len(CHECKS)} self-checks passed)")
        return 0 if same else 1
    args.output.write_bytes(text.encode("utf-8"))
    print(f"analyze.py: {len(CHECKS)} self-checks passed -> {args.output.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
