#!/usr/bin/env python3
"""PSY-015 analysis: one stochastic SIR run against the deterministic epidemic curve.

Reads observed-input.json (written by extract.py) and scenarios.json, never
the repository, and writes results.json. The epidemic part is synthetic: an
SIR model applied to a belief by analogy, with assumed rates. Each run of the
stochastic model follows the embedded jump chain (which event happens next)
with integer draws from random.Random(seed); no waiting time is drawn, because
the final size does not depend on it.

Run from the repository root:
    python -I scripts/streeling_fixtures/psychohistory/psy-015/analyze.py
    python -I scripts/streeling_fixtures/psychohistory/psy-015/analyze.py --check
"""

from __future__ import annotations

import argparse
import copy
import json
import math
import random
import sys
from fractions import Fraction
from pathlib import Path

# This program lives under scripts/ (CONTRIBUTING.md: no executable code outside scripts/); its data stays
# under state/streeling/fixtures/. FIXTURE_FILE is the path the program would have next to that data.
FIXTURE_FILE = (Path(__file__).resolve().parents[4]
                / "state/streeling/fixtures/psychohistory/psy-015" / Path(__file__).name)

HERE = FIXTURE_FILE.parent
DECIMALS = {"share": 4, "mean": 2, "agents": 2, "time": 2, "standard_error": 2}
SMALL_POPULATION = 100  # up to this size: exact fractions, and one stored value per final size
CHECKS: dict[str, int] = {}  # self-check -> times evaluated


def check(name: str, condition: bool, detail: str = "") -> None:
    """A self-check that can fail: abort instead of writing a wrong result."""
    if not condition:
        raise AssertionError(f"self-check failed: {name}" + (f" ({detail})" if detail else ""))
    CHECKS[name] = CHECKS.get(name, 0) + 1


def fraction(spec: dict) -> Fraction:
    return Fraction(spec["numerator"], spec["denominator"])


def exact(value: Fraction, decimals: int = DECIMALS["share"]) -> dict:
    return {"exact": str(value), "value": round(float(value), decimals)}


def libm_round(value: float, decimals: int, what: str) -> float:
    """Round a float that went through exp(): refuse one so close to a rounding boundary that a last-bit
    difference between C libraries could change the stored digit."""
    scaled = value * 10 ** decimals
    check("no value computed with exp() lies within 1e-6 of a rounding boundary",
          abs(scaled - math.floor(scaled) - 0.5) > 1e-6, what)
    return round(value, decimals)


# ---------------------------------------------------------------- deterministic model

def final_size_equation(r0: float, s0: float, steps: int) -> float:
    """Root z in [0, 1) of 1 - z = s0 * exp(-r0 * z), by bisection: the share that ever holds the belief."""
    low, high = 0.0, 1.0
    for _ in range(steps):
        middle = (low + high) / 2
        if 1 - middle - s0 * math.exp(-r0 * middle) > 0:
            low = middle
        else:
            high = middle
    return (low + high) / 2


def curve(r0: float, s0: float, i0: float, settings: dict) -> dict:
    """Integrate ds = -r0*s*i, di = r0*s*i - i, dr = i with RK4 until fewer than a given share still hold."""
    per_unit = settings["steps_per_time_unit"]
    h = 1 / per_unit
    s, i, r, step = s0, i0, 0.0, 0
    peak, peak_step = i0, 0
    while i >= settings["stop_when_holders_share_below"]:
        if step >= settings["max_time_units"] * per_unit:
            raise ArithmeticError("the deterministic curve did not die out within max_time_units")
        k1s, k1i = -r0 * s * i, r0 * s * i - i
        s2, i2 = s + h / 2 * k1s, i + h / 2 * k1i
        k2s, k2i = -r0 * s2 * i2, r0 * s2 * i2 - i2
        s3, i3 = s + h / 2 * k2s, i + h / 2 * k2i
        k3s, k3i = -r0 * s3 * i3, r0 * s3 * i3 - i3
        s4, i4 = s + h * k3s, i + h * k3i
        k4s, k4i = -r0 * s4 * i4, r0 * s4 * i4 - i4
        r += h / 6 * (i + 2 * i2 + 2 * i3 + i4)
        s += h / 6 * (k1s + 2 * k2s + 2 * k3s + k4s)
        i += h / 6 * (k1i + 2 * k2i + 2 * k3i + k4i)
        step += 1
        if i > peak:
            peak, peak_step = i, step
    check("deterministic curve: susceptible + holders + former holders stays 1", abs(s + i + r - 1) < 1e-9)
    return {"final_share": 1 - s, "peak_share": peak, "peak_time": peak_step / per_unit, "time_units": step / per_unit}


def deterministic(n: int, r0: Fraction, holders: int, scenarios: dict) -> tuple[dict, float]:
    s0, i0 = Fraction(n - holders, n), Fraction(holders, n)
    rate = float(r0)
    root = final_size_equation(rate, float(s0), scenarios["final_size_equation"]["bisection_steps"])
    check("final-size equation: the bisection root satisfies it",
          abs(1 - root - float(s0) * math.exp(-rate * root)) < 1e-12)
    path = curve(rate, float(s0), float(i0), scenarios["deterministic_curve"])
    check("known answer: the integrated curve ends at the root of the final-size equation",
          abs(path["final_share"] - root) < 1e-6, f"{path['final_share']} against {root}")
    if r0 * s0 > 1:
        closed_form = float(i0) + float(s0) - (1 + math.log(rate * float(s0))) / rate
        check("known answer: the curve's peak equals i0 + s0 - (1 + ln(R0*s0)) / R0", abs(path["peak_share"] - closed_form) < 1e-4)
    else:
        check("at or below the threshold the curve never rises above its start", path["peak_time"] == 0)
    limit = final_size_equation(rate, 1.0, scenarios["final_size_equation"]["bisection_steps"])
    threshold = n / r0  # susceptible agents below which holders decline
    return {
        "initial_reproduction_number": exact(r0 * s0),
        "holders_rise_while_susceptible_agents_exceed": exact(threshold, DECIMALS["agents"]),
        "adoptions_before_holders_stop_rising": max(0, n - holders - math.floor(threshold)),
        "final_share": libm_round(root, DECIMALS["share"], "final share"),
        "final_agents": libm_round(root * n, DECIMALS["agents"], "final agents"),
        "curve_final_share": round(path["final_share"], DECIMALS["share"]),
        "curve_peak_holders_share": round(path["peak_share"], DECIMALS["share"]),
        "curve_peak_holders_agents": round(path["peak_share"] * n, DECIMALS["agents"]),
        "curve_peak_time": round(path["peak_time"], DECIMALS["time"]),
        "large_population_limit_final_share": libm_round(limit, DECIMALS["share"], "limit final share"),
    }, root * n


# ---------------------------------------------------------------- stochastic model

def final_size_distribution(n: int, a: int, b: int, holders: int, use_fractions: bool) -> list:
    """Probability of each final size (index = agents that ever held the belief), R0 = a/b.

    Walks the embedded jump chain level by level. With s susceptible agents the next event is an adoption with
    probability a*s / (a*s + b*n), otherwise a holder stops transmitting; the number of holders does not enter.
    """
    zero, one = (Fraction(0), Fraction(1)) if use_fractions else (0.0, 1.0)
    reach = [zero] * (n + 2)  # reach[i]: probability of standing at this level with i holders
    reach[holders] = one
    result = [zero] * (n + 1)
    for s in range(n - holders, -1, -1):
        adopt = Fraction(a * s, a * s + b * n) if use_fractions else a * s / (a * s + b * n)
        stop = 1 - adopt
        below = [zero] * (n + 2)
        for i in range(n - s, 0, -1):
            mass = reach[i]
            if not mass:
                continue
            if i == 1:
                result[n - s] += mass * stop
            else:
                reach[i - 1] += mass * stop
            if s:
                below[i + 1] += mass * adopt
        reach = below
    return result


def simulate_final_size(n: int, a: int, b: int, holders: int, rng: random.Random) -> int:
    """One run of the jump chain: how many agents ever held the belief."""
    s, i, bn = n - holders, holders, b * n
    draw = rng.randrange
    while i:
        adoption_weight = a * s
        if draw(adoption_weight + bn) < adoption_weight:
            s -= 1
            i += 1
        else:
            i -= 1
    return n - s


def percentile(ordered: list[int], percent: int) -> int:
    """Nearest-rank percentile of a sorted list."""
    return ordered[(percent * len(ordered) + 99) // 100 - 1]


def humps(probability: list, factor: Fraction) -> dict:
    """Apply the hump rule of scenarios.json to an exact distribution (index = final size)."""
    sizes = range(1, len(probability))
    best_left, left = 0, {}
    for size in sizes:
        left[size] = best_left
        best_left = max(best_left, probability[size])
    best_right, valleys = 0, []
    for size in reversed(sizes):
        if probability[size] < factor * left[size] and probability[size] < factor * best_right:
            valleys.append(size)
        best_right = max(best_right, probability[size])
    most_likely = max(sizes, key=lambda size: (probability[size], -size))
    if not valleys:
        return {"humps": 1, "most_likely_size": most_likely}
    valley = min(valleys, key=lambda size: (probability[size], size))
    upper = max(range(valley + 1, len(probability)), key=lambda size: (probability[size], -size))
    lower = max(range(1, valley), key=lambda size: (probability[size], -size))
    return {"humps": 2, "most_likely_size": most_likely, "lower_hump_most_likely_size": lower,
            "valley_size": valley, "upper_hump_most_likely_size": upper}


def agreement(cells: list[tuple[str, int, float]], runs: int, mean_gap: float, rule: dict) -> dict:
    """Simulated counts against exact probabilities, in binomial standard errors."""
    largest, tested, rare, rare_off, worst = 0.0, 0, 0, 0, ""
    for label, observed, probability in cells:
        expected = runs * probability
        if min(expected, runs - expected) >= rule["min_expected"]:
            gap = abs(observed - expected) / math.sqrt(expected * (1 - probability))
            tested += 1
            if gap > largest:
                largest, worst = gap, label
        else:
            rare += 1
            rare_off += abs(observed - expected) > rule["rare_cell_tolerance"]
    return {"cells_tested": tested, "largest_gap_in_standard_errors": largest, "largest_gap_at_sizes": worst,
            "rare_cells": rare, "rare_cells_beyond_tolerance": rare_off, "mean_gap_in_standard_errors": mean_gap,
            "within_limit": (largest <= rule["max_standard_errors"] and rare_off == 0
                             and abs(mean_gap) <= rule["max_standard_errors"])}


def stored_agreement(result: dict) -> dict:
    return {key: (round(value, DECIMALS["standard_error"]) if isinstance(value, float) else value)
            for key, value in result.items()}


def exact_law(n: int, a: int, b: int, holders: int, small: bool) -> tuple[list, Fraction]:
    """Exact final-size probabilities of the jump chain, and the probability that the belief is never passed on."""
    probability = final_size_distribution(n, a, b, holders, use_fractions=small)
    total = sum(probability)
    check("exact final-size probabilities sum to 1", total == 1 if small else abs(total - 1) < 1e-9, str(total))
    never = Fraction(b * n, a * (n - holders) + b * n)
    check("exact probability of final size 1 equals b*N / (a*(N-1) + b*N)",
          probability[1] == never if small else abs(probability[1] - float(never)) < 1e-12)
    if small:
        as_floats = final_size_distribution(n, a, b, holders, use_fractions=False)
        check("the float version of the exact calculation matches the fraction version",
              all(abs(x - float(y)) < 1e-12 for x, y in zip(as_floats, probability)))
    return probability, never


def simulate(n: int, a: int, b: int, holders: int, seed: int, runs: int) -> tuple[list[int], list[int]]:
    """Seeded runs of the jump chain: the final sizes in run order, and the number of runs at each size."""
    rng = random.Random(seed)
    sizes = [simulate_final_size(n, a, b, holders, rng) for _ in range(runs)]
    check("every simulated final size lies between the initial holders and the population",
          all(holders <= size <= n for size in sizes))
    counts = [0] * (n + 1)
    for size in sizes:
        counts[size] += 1
    check("simulated counts sum to the runs", sum(counts) == runs)
    return sizes, counts


def share_bins(n: int, counts: list[int], probability: list, reading: dict, runs: int) -> tuple[list[dict], list[int]]:
    """Runs and exact probability by share of the population reached; also returns each bin's largest size."""
    uppers = [n * spec["numerator"] // spec["denominator"] for spec in reading["population_share_bins_upper"]]
    check("population-share bins end at the whole population and increase", uppers[-1] == n and uppers == sorted(set(uppers)))
    bins, lower = [], 1
    for upper in uppers:
        bins.append({"sizes": f"{lower}-{upper}" if upper > lower else str(lower),
                     "simulated_runs": sum(counts[lower:upper + 1]),
                     "exact_probability": round(float(sum(probability[lower:upper + 1])), DECIMALS["share"])})
        lower = upper + 1
    check("bin counts sum to the runs", sum(row["simulated_runs"] for row in bins) == runs)
    return bins, uppers


def fade_out(n: int, ordered: list[int], counts: list[int], probability: list, reading: dict) -> tuple[dict, dict]:
    """Runs at or below the early fade-out cut (and at two other cuts), and what the runs above the cut look like."""
    cut = n * reading["early_fade_out_cut_share"]["numerator"] // reading["early_fade_out_cut_share"]["denominator"]
    cuts = [cut] + [n * spec["numerator"] // spec["denominator"] for spec in reading["other_cut_shares"]]
    rows = [{"at_most_agents": size, "simulated_runs": sum(counts[:size + 1]),
             "exact_probability": round(float(sum(probability[:size + 1])), DECIMALS["share"])} for size in cuts]
    above = [size for size in ordered if size > cut]
    below = [size for size in ordered if size <= cut]
    check("runs at or below the cut + runs above it = runs", len(above) + len(below) == len(ordered))
    return ({"cut_agents": cut, "rule": "final size at or below the cut", "cuts": rows},
            {"simulated_runs": len(above),
             "largest_size_at_or_below_the_cut": below[-1] if below else None,
             "smallest_size_above_the_cut": above[0] if above else None,
             "percentiles": {f"p{percent}": percentile(above, percent) for percent in reading["percentiles"]} if above else None})


def near_the_curve(n: int, deterministic_agents: float, counts: list[int], probability: list, reading: dict) -> dict:
    """Runs whose final size lies within the stated band around the deterministic final size."""
    band = n * fraction(reading["near_the_curve_band_share"])
    low_edge, high_edge = deterministic_agents - float(band), deterministic_agents + float(band)
    check("the band around the deterministic final size does not end within 1e-6 of a whole agent",
          all(abs(edge - round(edge)) > 1e-6 for edge in (low_edge, high_edge)))
    smallest, largest = max(1, math.ceil(low_edge)), min(n, math.floor(high_edge))
    return {"band_agents": exact(band, DECIMALS["agents"]), "smallest_size": smallest, "largest_size": largest,
            "simulated_runs": sum(counts[smallest:largest + 1]),
            "exact_probability": round(float(sum(probability[smallest:largest + 1])), DECIMALS["share"])}


def agreement_cells(n: int, counts: list[int], probability: list, bins: list[dict], uppers: list[int]) -> list[tuple]:
    """Cells of the agreement test: every size for a small population, otherwise sizes 1 to 5 and the share bins."""
    if n <= SMALL_POPULATION:
        return [(str(size), counts[size], float(probability[size])) for size in range(1, n + 1)]
    cells = [(str(size), counts[size], probability[size]) for size in range(1, 6)]
    return cells + [(row["sizes"], row["simulated_runs"], sum(probability[low:high + 1]))
                    for row, low, high in zip(bins, [1] + [upper + 1 for upper in uppers[:-1]], uppers)]


def distribution_shape(probability: list, reading: dict) -> dict:
    """Humps of the exact distribution, with the probability of each size the hump rule names."""
    shape = humps(probability, fraction(reading["hump_rule"]["valley_factor"]))
    for key in ("most_likely_size", "lower_hump_most_likely_size", "valley_size", "upper_hump_most_likely_size"):
        if key in shape:
            shape[key.replace("_size", "_probability")] = round(float(probability[shape[key]]), DECIMALS["share"])
    return shape


def add_tables_by_size(case: dict, n: int, counts: list[int], probability: list, exact_mean: Fraction) -> None:
    """For a small population, store the whole table: one probability and one count of runs per final size."""
    case["exact"]["probability_by_final_size"] = [round(float(p), DECIMALS["share"]) for p in probability[1:]]
    case["simulated"]["runs_by_final_size"] = counts[1:]
    case["simulated"]["cumulative_runs_by_final_size"] = [sum(counts[:size + 1]) for size in range(1, n + 1)]
    middle = sorted({math.floor(float(exact_mean)), math.ceil(float(exact_mean))})
    case["simulated"]["runs_at_the_whole_sizes_around_the_exact_mean"] = {
        "sizes": middle, "simulated_runs": sum(counts[size] for size in middle)}


def run_case(population: dict, number: dict, scenarios: dict) -> tuple[dict, dict]:
    """One case (a population size and a reproduction number): deterministic curve, exact law and seeded runs."""
    n, holders = population["agents"], scenarios["initial_holders"]
    a, b = number["numerator"], number["denominator"]
    r0 = Fraction(a, b)
    reading, simulation = scenarios["reading"], scenarios["simulation"]
    runs = simulation["runs_per_case"]
    seed = simulation["seeds"][population["label"]][number["label"]]

    model, deterministic_agents = deterministic(n, r0, holders, scenarios)
    probability, never = exact_law(n, a, b, holders, small=n <= SMALL_POPULATION)
    exact_mean = sum(size * p for size, p in enumerate(probability))
    exact_variance = sum(size * size * p for size, p in enumerate(probability)) - exact_mean ** 2
    sizes, counts = simulate(n, a, b, holders, seed, runs)
    ordered = sorted(sizes)
    simulated_mean = sum(sizes) / runs
    bins, uppers = share_bins(n, counts, probability, reading, runs)
    early, above_the_cut = fade_out(n, ordered, counts, probability, reading)
    near = near_the_curve(n, deterministic_agents, counts, probability, reading)
    cells = agreement_cells(n, counts, probability, bins, uppers)
    mean_gap = (simulated_mean - float(exact_mean)) / math.sqrt(float(exact_variance) / runs)
    agree = agreement(cells, runs, mean_gap, scenarios["agreement_test"])
    check("simulated counts and mean agree with the exact distribution within the stated standard errors",
          agree["within_limit"], f"{population['label']} {number['label']}: {agree}")
    case = {
        "population": n,
        "population_label": population["label"],
        "reproduction_number": {"label": number["label"]} | exact(r0),
        "initial_holders": holders,
        "first_event": {"is_an_adoption": exact(1 - never), "is_the_holder_stopping_so_the_belief_is_never_passed_on": exact(never)},
        "deterministic": model,
        "exact": {"mean_final_size": round(float(exact_mean), DECIMALS["mean"])} | distribution_shape(probability, reading),
        "simulated": {
            "seed": seed, "runs": runs,
            "first_runs": sizes[:simulation["first_runs_listed"]],
            "mean_final_size": round(simulated_mean, DECIMALS["mean"]),
            "most_frequent_size": max(range(1, n + 1), key=lambda size: (counts[size], -size)),
            "percentiles": {f"p{percent}": percentile(ordered, percent) for percent in reading["percentiles"]},
            "runs_never_passed_on": counts[1],
            "runs_reaching_everyone": counts[n],
        },
        "by_population_share": bins,
        "early_fade_out": early,
        "runs_above_the_cut": above_the_cut,
        "near_the_deterministic_final_size": near,
        "agreement_with_exact": stored_agreement(agree),
    }
    if n <= SMALL_POPULATION:
        add_tables_by_size(case, n, counts, probability, exact_mean)
    return case, {"counts": counts, "probability": probability, "cells": cells, "runs": runs, "mean_gap": mean_gap}


# ---------------------------------------------------------------- side calculations

def branching(number: dict, scenarios: dict) -> dict:
    """Early phase as a branching process: each holder converts a geometric number of others, mean R0.

    The number is geometric because the holding time is exponential. With a fixed holding time of the same mean
    it would be Poisson, and the process would die out with the smallest root of q = exp(R0 * (q - 1)): that
    value is stored as a contrast, no run uses it.
    """
    r0 = fraction(number)
    extinction = min(Fraction(1), 1 / r0)
    q = 0.0
    for _ in range(5000):  # smallest fixed point of q = 1 / (1 + R0 * (1 - q)), reached from below
        q = 1 / (1 + float(r0) * (1 - q))
    if r0 != 1:
        check("branching process: the iterated fixed point equals min(1, 1/R0)", abs(q - float(extinction)) < 1e-9)
    row = {"reproduction_number": {"label": number["label"]} | exact(r0), "probability_of_dying_out": exact(extinction)}
    if r0 < 1:
        row["mean_total_size"] = exact(1 / (1 - r0), DECIMALS["mean"])
    # q = exp(R0 * (q - 1)) is the final-size equation with z = 1 - q and everybody susceptible at the start.
    fixed = 1 - final_size_equation(float(r0), 1.0, scenarios["final_size_equation"]["bisection_steps"])
    check("branching process: a fixed holding time never makes dying out more likely than an exponential one",
          fixed <= float(extinction) + 1e-12, f"{fixed} against {extinction}")
    row["probability_of_dying_out_with_a_fixed_holding_time"] = libm_round(fixed, DECIMALS["share"], "fixed holding time")
    return row


def several_holders(scenarios: dict) -> dict:
    spec = scenarios["several_initial_holders"]
    n = next(p["agents"] for p in scenarios["populations"] if p["label"] == spec["population"])
    number = next(r for r in scenarios["reproduction_numbers"] if r["label"] == spec["reproduction_number"])
    cut_share = fraction(scenarios["reading"]["early_fade_out_cut_share"])
    cut = math.floor(n * cut_share)
    rows = []
    for holders in spec["initial_holders"]:
        probability = final_size_distribution(n, number["numerator"], number["denominator"], holders, use_fractions=False)
        check("exact final-size probabilities sum to 1 (several initial holders)", abs(sum(probability) - 1) < 1e-9)
        rows.append({"initial_holders": holders,
                     "exact_probability_of_final_size_at_most_cut": round(sum(probability[:cut + 1]), DECIMALS["share"]),
                     "branching_value": exact((1 / fraction(number)) ** holders)})
    check("more initial holders never raise the probability of an early fade-out",
          all(x["exact_probability_of_final_size_at_most_cut"] >= y["exact_probability_of_final_size_at_most_cut"]
              for x, y in zip(rows, rows[1:])))
    return {"kind": "synthetic: exact calculation on the jump chain, no simulation", "population": n,
            "reproduction_number": exact(fraction(number)), "cut_agents": cut, "rows": rows}


def hand_computed_case(case: dict) -> None:
    number = case["reproduction_number"]
    probability = final_size_distribution(case["agents"], number["numerator"], number["denominator"],
                                          case["initial_holders"], use_fractions=True)
    check("hand-computed case: three agents at R0 = 1 give 3/5, 9/40 and 7/40",
          {str(size): str(p) for size, p in enumerate(probability) if size} == case["expected_probability_by_final_size"])


def holder(row: dict) -> str:
    """Holder of a belief file under the holder rule of scenarios.json."""
    return row["evaluated_by"].split("/")[0]


def shared(rows: list[dict]) -> int:
    """Propositions recorded for two or more holders."""
    holders_of: dict[str, set[str]] = {}
    for row in rows:
        holders_of.setdefault(row["proposition"], set()).add(holder(row))
    return sum(len(group) >= 2 for group in holders_of.values())


def belief_file_counts(snapshot: dict, scenarios: dict) -> tuple[dict, dict]:
    """The belief files by group and holder, and whether any proposition is recorded for two holders."""
    beliefs = snapshot["belief_files"]
    groups = {}
    for group in ("current", "archived"):
        rows = [row for row in beliefs if row["group"] == group]
        tally: dict[str, int] = {}
        raw: dict[str, int] = {}
        for row in rows:
            tally[holder(row)] = tally.get(holder(row), 0) + 1
            raw[row["evaluated_by"]] = raw.get(row["evaluated_by"], 0) + 1
        groups[group] = {"files": len(rows), "files_by_holder": dict(sorted(tally.items())),
                         "files_by_evaluated_by_value": dict(sorted(raw.items())),
                         "files_without_any_evidence_item": sum(
                             row["supporting_items"] + row["contradicting_items"] == 0 for row in rows)}
        check("files by holder sum to the files of the group", sum(tally.values()) == len(rows) == sum(raw.values()))
    check("belief files recounted by group equal extract.py's counts",
          {group: groups[group]["files"] for group in groups} == snapshot["counts"]["belief_files"])
    planted = copy.deepcopy(beliefs) + [dict(beliefs[0], evaluated_by="planted-agent/control")]
    check("negative control: a planted second holder of one proposition is counted", shared(planted) == shared(beliefs) + 1)
    check("distinct propositions recounted from the rows equal extract.py's count on the unaltered text",
          len({row["proposition"] for row in beliefs}) == snapshot["counts"]["distinct_propositions"])
    return {
        "holder_rule": scenarios["holder_rule"],
        "current": groups["current"], "archived": groups["archived"],
        "total": len(beliefs),
        "distinct_propositions": len({row["proposition"] for row in beliefs}),
        "distinct_holders": sorted({holder(row) for row in beliefs}),
        "propositions_recorded_for_two_or_more_holders": shared(beliefs),
        "content": files_with_content(beliefs, scenarios),
        "key_names_used": snapshot["key_names_used_in_the_belief_files"],
    }, {"propositions_with_two_holders_before_and_after_planting_one": [shared(beliefs), shared(planted)]}


def files_with_content(beliefs: list[dict], scenarios: dict) -> dict:
    """Belief files that say something against empty scaffolds, and whether two holders could share a proposition."""
    def tally(rows: list[dict]) -> dict:
        found: dict[str, int] = {}
        for row in rows:
            found[holder(row)] = found.get(holder(row), 0) + 1
        return dict(sorted(found.items()))

    scaffolds = [row for row in beliefs if row["supporting_items"] + row["contradicting_items"] == 0
                 and row["truth_value"] == "U" and row["confidence"] == 0]
    filled = [row for row in beliefs if row not in scaffolds]
    check("belief files with content + empty scaffolds = belief files", len(filled) + len(scaffolds) == len(beliefs))
    check("every belief file with content has at least one evidence item",
          all(row["supporting_items"] + row["contradicting_items"] > 0 for row in filled))
    return {
        "scaffold_rule": scenarios["scaffold_rule"],
        "files_with_content": len(filled), "files_with_content_by_holder": tally(filled),
        "empty_scaffolds": len(scaffolds), "empty_scaffolds_by_holder": tally(scaffolds),
        "holders_with_content": sorted(tally(filled)),
        "a_proposition_under_two_holders_was_possible": len(tally(filled)) >= 2,
    }


def belief_sources(snapshot: dict) -> dict:
    """What the belief files name as a source: a message of a contract type, or text written by the evaluator."""
    beliefs, feedback, scan = snapshot["belief_files"], snapshot["feedback_path"], snapshot["sender_scan"]
    citing = [row for row in beliefs if row["contract_messages_named"]]
    by_group = {group: sum(row["group"] == group for row in citing) for group in ("current", "archived")}
    check("belief files that name a contract message, recounted, equal extract.py's count",
          by_group == snapshot["counts"]["belief_files_whose_evidence_names_a_contract_message"])
    check("the belief files that cite a recommendation are exactly those the applying script writes",
          sorted(row["path"].rsplit("/", 1)[1] for row in citing) == feedback["applying_script"]["belief_files_it_writes"])
    check("a citing belief file has one evidence item, whose source is the contract name and the id under source_recommendation",
          all(row["evidence_sources"] == [f"{row['contract_messages_named'][0]} {row['source_recommendation'][0]}"]
              and row["supporting_items"] + row["contradicting_items"] == 1 for row in citing))
    ids = scan["files_that_hold_a_cited_message_id"]
    check("each cited message id occurs in one JSON file under state/: the belief file that cites it",
          sorted(path for paths in ids.values() for path in paths) == sorted(row["path"] for row in citing)
          and all(len(paths) == 1 for paths in ids.values()))
    samples = [sample for kind in snapshot["record_types"].values() for sample in kind["samples"]]
    check("positive control: the sender-key scan finds such a key in a sample file",
          any(sample["sender_keys"] for sample in samples))
    keys = {key: len(paths) for key, paths in scan["files_with_a_sender_key"].items()}
    yaml_file = snapshot["yaml_belief_file"]
    return {
        "evidence_items": sum(row["supporting_items"] + row["contradicting_items"] for row in beliefs),
        "evidence_items_whose_source_names_a_contract_message": sum(
            row["items_whose_source_names_a_contract_message"] for row in beliefs),
        "belief_files_whose_evidence_names_a_contract_message": by_group,
        "belief_files_by_contract_message_named": snapshot["counts"]["belief_files_by_contract_message_named"],
        "those_files": sorted(row["path"].rsplit("/", 1)[1] for row in citing),
        "their_holders": sorted({holder(row) for row in citing}),
        "contract_schemas": snapshot["counts"]["contract_schemas"],
        "recommendation": {
            "message_schema_description": feedback["message_schema"]["description"],
            "applying_script": feedback["applying_script"]["path"],
            "applying_script_docstring": feedback["applying_script"]["first_paragraph_of_its_docstring"],
            "belief_files_the_script_writes": feedback["applying_script"]["belief_files_it_writes"],
            "what_the_script_copies_from_the_message": [row["meaning"] for row in feedback["applying_script"]["statements"]],
            "keys_that_would_name_the_sender": feedback["message_schema"]["keys_that_name_the_sender"],
            "recommendation_documents_among_the_json_files_under_state": len(scan["json_files_in_the_recommendation_inbox"]),
            "other_json_files_that_hold_a_cited_message_id": sum(len(paths) for paths in ids.values()) - len(citing),
        },
        "json_files_under_state_by_sender_key": keys,
        "hits_for_the_keys_other_than_source_recommendation": sum(
            count for key, count in keys.items() if key != "source_recommendation"),
        "sample_files_with_a_sender_key": sum(bool(sample["sender_keys"]) for sample in samples),
        "yaml_belief_file": {key: yaml_file[key] for key in (
            "path", "belief_entries", "evidence_items", "distinct_sources", "sources_named_more_than_once",
            "evidence_items_whose_source_names", "lines_with_evaluated_by")},
    }


def record_type_counts(snapshot: dict, scenarios: dict) -> tuple[dict, list[dict]]:
    """The two record types the repository defines for an agent's beliefs, against what a transmission record needs."""
    types = snapshot["record_types"]
    scan = snapshot["record_shape_scan"]["files_with_the_shape"]
    check("positive control: the shape test recognised every sample file as its own record type only",
          all(sample["shape_test"] == [name] for name, kind in types.items() for sample in kind["samples"])
          and all(kind["samples"] for kind in types.values()))
    needs = []
    for need in scenarios["transmission_record"]["needs"]:
        for name in types:
            check("each key named in scenarios.json for a transmission record exists in that record type's schema",
                  need[name] is None or need[name] in types[name]["properties"], f"{name}.{need[name]}")
        needs.append(need)
    record_types = {name: {"schema": kind["schema_path"], "title": kind["title"], "required_keys": kind["required_keys"],
                           "sample_files": len(kind["samples"]),
                           "files_with_this_shape_under_state": len(scan[name]),
                           "needs_with_a_key": sum(need[name] is not None for need in needs),
                           "of_which_covered_only_in_part": sum(name in need.get("in_part", {}) for need in needs),
                           "needs": len(needs)}
                    for name, kind in types.items()}
    check("a need covered in part names a key of that record type",
          all(need[name] is not None for need in needs for name in need.get("in_part", {})))
    knowledge = types["knowledge_state"]
    record_types["knowledge_state"]["sample_beliefs_before_and_after"] = sorted(
        f"{sample['outcome']}: {sample['truth_value_before']} -> {sample['truth_value_after']}" for sample in knowledge["samples"])
    record_types["knowledge_state"]["samples_taught_without_a_change_of_belief"] = sum(
        sample["truth_value_before"] == sample["truth_value_after"] for sample in knowledge["samples"])
    record_types["knowledge_state"]["taught_by_default"] = knowledge["taught_by_default"]
    record_types["knowledge_state"]["sample_teachers_and_learners"] = sorted(
        {f"{sample['taught_by']} -> {sample['learner']}" for sample in knowledge["samples"]})
    record_types["knowledge_state"]["every_sample_teacher_and_the_default_are_the_department_head"] = all(
        teacher == snapshot["department_record"]["head_persona"] for teacher in
        [knowledge["taught_by_default"]] + [sample["taught_by"] for sample in knowledge["samples"]])
    return record_types, needs


def observed_context(snapshot: dict, scenarios: dict) -> tuple[dict, dict]:
    """The 'observed' section: what the snapshot of the pinned commit records about beliefs and their holders."""
    department = snapshot["department_record"]
    check("the department record names exactly one research area about beliefs",
          len(department["research_areas_that_mention_belief"]) == 1)
    belief_files, control = belief_file_counts(snapshot, scenarios)
    record_types, needs = record_type_counts(snapshot, scenarios)
    sources = belief_sources(snapshot)
    return {
        "kind": "observed: read from observed-input.json, a snapshot of the pinned commit",
        "department": {
            "research_area": department["research_areas_that_mention_belief"][0],
            "head_persona": department["head_persona"],
            "key_principle": department["key_principle"],
            "personas_in_key_principle": department["personas_in_key_principle"],
            "repos_in_key_principle": department["repos_in_key_principle"],
        },
        "belief_files": belief_files,
        "sources": sources,
        "record_types": record_types,
        "json_files_under_state_tested_for_a_record_shape": snapshot["counts"]["json_files_tested_for_a_record_shape"],
        "state_knowledge_folder_exists": snapshot["record_shape_scan"]["state_knowledge_folder_exists"],
        "audit_note": snapshot["audit_note"],
        "transmission_record_needs": needs,
    }, control


def transfer_task(task: dict, scenarios: dict) -> dict:
    n, holders = task["people"], task["initial_holders"]
    beta, gamma = fraction(task["passing_on_rate_per_day"]), fraction(task["stops_repeating_rate_per_day"])
    r0 = beta / gamma
    a, b = r0.numerator, r0.denominator
    s0 = Fraction(n - holders, n)
    probability = final_size_distribution(n, a, b, holders, use_fractions=True)
    check("transfer task: exact probabilities sum to 1", sum(probability) == 1)
    stop_first = Fraction(b * n, a * (n - holders) + b * n)
    stop_second = Fraction(b * n, a * (n - holders - 1) + b * n)
    exactly_two = (1 - stop_first) * stop_second ** 2
    check("transfer task: adoption then two stops gives the probability of final size 2", exactly_two == probability[2])
    root = final_size_equation(float(r0), float(s0), scenarios["final_size_equation"]["bisection_steps"])
    agents = root * n
    around = sorted({math.floor(agents), math.ceil(agents)})
    mean = sum(size * p for size, p in enumerate(probability))
    shape = humps(probability, fraction(scenarios["reading"]["hump_rule"]["valley_factor"]))
    threshold = n / r0
    several = task["initial_holders_alternative"]
    with_several = final_size_distribution(n, a, b, several, use_fractions=True)
    check("transfer task: exact probabilities sum to 1 with several initial holders",
          sum(with_several) == 1 and not any(with_several[:several]))
    return {
        "note": task["note"],
        "inputs": {"people": n, "initial_holders": holders, "passing_on_rate_per_day": str(beta),
                   "stops_repeating_rate_per_day": str(gamma)},
        "q1_threshold": {
            "reproduction_number": exact(r0),
            "mean_days_of_repeating": exact(1 / gamma, DECIMALS["mean"]),
            "initial_reproduction_number": exact(r0 * s0),
            "above_the_threshold_at_the_start": r0 * s0 > 1,
            "holders_rise_while_unaware_people_exceed": exact(threshold, DECIMALS["agents"]),
            "adoptions_before_holders_stop_rising": max(0, n - holders - math.floor(threshold)),
        },
        "q2_first_events": {
            "first_event_is_an_adoption": exact(1 - stop_first),
            "never_passed_on": exact(stop_first),
            "a_holder_stops_when_two_people_are_unaware": exact(stop_second),
            "final_size_exactly_two": exact(exactly_two),
        },
        "q3_distribution": {
            "probability_by_final_size": {str(size): exact(p) for size, p in enumerate(probability) if size},
            "mean_final_size": exact(mean, DECIMALS["mean"]),
            "least_likely_size": min(range(1, n + 1), key=lambda size: (probability[size], size)),
        } | shape,
        "q4_deterministic_and_branching": {
            "final_share": libm_round(root, DECIMALS["share"], "transfer final share"),
            "final_people": libm_round(agents, DECIMALS["agents"], "transfer final people"),
            "whole_sizes_around_it": around,
            "exact_probability_of_those_sizes": exact(sum(probability[size] for size in around)),
            "exact_probability_of_final_size_at_most_two": exact(probability[1] + probability[2]),
            "branching_probability_of_dying_out": exact(min(Fraction(1), 1 / r0)),
            "with_several_initial_holders": {
                "initial_holders": several,
                "branching_probability_of_dying_out": exact(min(Fraction(1), 1 / r0) ** several),
                "exact_probability_that_nobody_else_adopts": exact(with_several[several])},
        },
        "q5_plan": "No single answer: a record to keep, a rule fixed in advance, one result that would falsify the claim, "
                   "and what one team and one rumour cannot establish.",
    }


def wrong_number_control(kept: dict, scenarios: dict) -> dict:
    """Negative control: the agreement test must reject counts simulated with another reproduction number."""
    right = kept[("fourteen_agents", "well_above_threshold")]
    wrong = kept[("fourteen_agents", "just_above_threshold")]
    crossed = agreement([(label, observed_count, float(p)) for (label, observed_count, _), p
                         in zip(right["cells"], wrong["probability"][1:])],
                        right["runs"], 0.0, scenarios["agreement_test"])
    check("negative control: counts simulated at R0 = 3 fail the agreement test against the exact R0 = 1.2 distribution",
          not crossed["within_limit"])
    return {"simulated_with": "fourteen_agents, well_above_threshold",
            "compared_with_the_exact_distribution_of": "fourteen_agents, just_above_threshold",
            "limit_in_standard_errors": scenarios["agreement_test"]["max_standard_errors"],
            "largest_gap_in_standard_errors": round(crossed["largest_gap_in_standard_errors"], DECIMALS["standard_error"]),
            "passes": crossed["within_limit"]}


def summary_rows(cases: list[dict]) -> list[dict]:
    """One row per case, copied from 'cases', with the runs split into three zones of the population."""
    summary = []
    for case in cases:
        runs = case["simulated"]["runs"]
        summary.append({
            "population": case["population"], "reproduction_number": case["reproduction_number"]["exact"],
            "deterministic_final_agents": case["deterministic"]["final_agents"],
            "deterministic_final_share": case["deterministic"]["final_share"],
            "simulated_mean_final_size": case["simulated"]["mean_final_size"],
            "simulated_runs_near_the_deterministic_final_size": case["near_the_deterministic_final_size"]["simulated_runs"],
            "simulated_runs_at_or_below_a_tenth_of_the_population": case["early_fade_out"]["cuts"][0]["simulated_runs"],
            "simulated_runs_between_a_tenth_and_nine_tenths": sum(row["simulated_runs"] for row in case["by_population_share"][1:-1]),
            "simulated_runs_above_nine_tenths": case["by_population_share"][-1]["simulated_runs"],
            "runs": runs,
            "humps_of_the_exact_distribution": case["exact"]["humps"],
        })
        check("summary: the three population-share zones sum to the runs",
              summary[-1]["simulated_runs_at_or_below_a_tenth_of_the_population"]
              + summary[-1]["simulated_runs_between_a_tenth_and_nine_tenths"]
              + summary[-1]["simulated_runs_above_nine_tenths"] == runs)
    return summary


def analyze(snapshot: dict, scenarios: dict) -> dict:
    """Orchestrator: one function per section of results.json, in the order the self-checks are recorded."""
    if scenarios["rounding"] != {f"{key}_decimals": value for key, value in DECIMALS.items()}:
        raise ValueError("scenarios.json rounding does not match analyze.py")
    if snapshot["source"]["commit"] is None:
        raise ValueError("observed-input.json was written with --allow-drift: it is not the pinned snapshot")
    hand_computed_case(scenarios["hand_computed_case"])
    observed, observed_control = observed_context(snapshot, scenarios)

    cases, kept = [], {}
    for population in scenarios["populations"]:
        for number in scenarios["reproduction_numbers"]:
            case, raw = run_case(population, number, scenarios)
            cases.append(case)
            kept[(population["label"], number["label"])] = raw
    check("the population in scenarios.json labelled fourteen_agents is the persona count of the department record",
          scenarios["populations"][0]["agents"] == observed["department"]["personas_in_key_principle"])
    crossed = wrong_number_control(kept, scenarios)
    summary = summary_rows(cases)

    return {
        "module_id": snapshot["module_id"],
        "rounding": "shares and probabilities to 4 decimals; means, agents, times and standard errors to 2 decimals; "
                    "'exact' is the unrounded fraction; counts are integers",
        "source": {"repository": snapshot["source"]["repository"], "commit": snapshot["source"]["commit"],
                   "slash_note": snapshot["source"]["slash_note"],
                   "files_read_one_by_one": [entry["path"] for entry in snapshot["source"]["files"]],
                   "scanned_folder": snapshot["source"]["scanned_folder"],
                   "contract_schemas_folder": snapshot["source"]["contract_schemas_folder"]},
        "observed": observed,
        "model": {"kind": "analogy: an epidemic model applied to a belief, with assumed rates; untested on the project"}
                 | {key: scenarios["model"][key] for key in ("name", "states", "reproduction_number", "time_unit", "jump_chain")},
        "cases": {"kind": "synthetic: deterministic curve, exact jump-chain calculation and seeded simulation", "rows": cases},
        "summary": {"kind": "synthetic: one row per case, copied from 'cases'", "rows": summary},
        "branching_process": {"kind": "synthetic: large-population approximation of the first generations",
                              "offspring": scenarios["branching_process"]["offspring"],
                              "rows": [branching(number, scenarios) for number in scenarios["reproduction_numbers"]]},
        "several_initial_holders": several_holders(scenarios),
        "negative_controls": {"agreement_test_on_a_wrong_reproduction_number": crossed} | observed_control,
        "transfer_task": transfer_task(scenarios["transfer_task"], scenarios),
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
