#!/usr/bin/env python3
"""PSY-019 analysis: what an average does to forecasters whose errors share a part.

Reads observed-input.json (a description of a setup, written by extract.py) and
scenarios.json (every assumption), never the repository, and writes
results.json. Closed forms are computed in exact fractions and rounded once.
The simulations use only +, -, * and / on IEEE 754 doubles and correctly
rounded square roots, with explicit running totals (never sum() on floats, whose
algorithm changed in Python 3.12), so the file is the same on every platform.

Run from the repository root:
    python -I -B scripts/streeling_fixtures/psychohistory/psy-019/analyze.py
    python -I -B scripts/streeling_fixtures/psychohistory/psy-019/analyze.py --check
"""

from __future__ import annotations

import argparse
import json
import math
import random
import sys
from fractions import Fraction
from itertools import product
from pathlib import Path

# This program lives under scripts/ (CONTRIBUTING.md: no executable code outside scripts/); its data stays
# under state/streeling/fixtures/. FIXTURE_FILE is the path the program would have next to that data.
FIXTURE_FILE = (Path(__file__).resolve().parents[4]
                / "state/streeling/fixtures/psychohistory/psy-019" / Path(__file__).name)

HERE = FIXTURE_FILE.parent
PINNED_COMMIT = "4b03838800dcd4894f1e026461979bff1d985ca8"
SQRT12 = 3.4641016151377544  # the double nearest sqrt(12), written as a literal
DECIMALS = {"exact": 6, "simulated": 4, "difference": 6, "standard_errors": 2, "percent": 2}
CHECKS: dict[str, int] = {}  # self-check -> times evaluated


def check(name: str, condition: bool, detail: str = "") -> None:
    """A self-check that can fail: abort instead of writing a wrong result."""
    if not condition:
        raise AssertionError(f"self-check failed: {name}" + (f" ({detail})" if detail else ""))
    CHECKS[name] = CHECKS.get(name, 0) + 1


def exact(value) -> float:
    """An exact fraction rounded half to even, once, to the stated decimals."""
    return float(round(Fraction(value), DECIMALS["exact"])) + 0.0


def percent(value) -> float:
    return float(round(Fraction(value) * 100, DECIMALS["percent"])) + 0.0


def sim(value: float) -> float:
    """A simulated value or a square root; adding 0.0 turns a negative zero into zero."""
    return round(value, DECIMALS["simulated"]) + 0.0


def small(value: float) -> float:
    """A simulated difference between two neighbouring cells, which 4 decimals would not show."""
    return round(value, DECIMALS["difference"]) + 0.0


def errors_from(value: float) -> float:
    return round(value, DECIMALS["standard_errors"]) + 0.0


def draw(rng: random.Random) -> float:
    """One part of an error: uniform between -sqrt(3) and sqrt(3), so mean 0 and variance 1."""
    return (rng.random() - 0.5) * SQRT12


def mse_of_average(rho: Fraction, k: int, sigma2: Fraction = Fraction(1), bias: Fraction = Fraction(0)) -> Fraction:
    """The closed form: bias^2 + sigma^2 (rho + (1 - rho) / k)."""
    return bias * bias + sigma2 * (rho + (1 - rho) / k)


def worth(rho: Fraction, k: int) -> Fraction:
    """Independent forecasters whose average has the same variance as k forecasters with correlation rho."""
    return Fraction(k) / (1 + (k - 1) * rho)


def quadratic_form(weights: list[Fraction], cov: list[list[Fraction]]) -> Fraction:
    """Variance of a weighted sum: sum over i and j of w_i w_j cov_ij."""
    size = range(len(weights))
    return sum((weights[i] * weights[j] * cov[i][j] for i in size for j in size), Fraction(0))


def minimum_variance_weights(cov: list[list[Fraction]]) -> list[Fraction]:
    """Weights that sum to 1 and minimise the variance: solve cov x = 1 exactly, then divide x by its sum."""
    n = len(cov)
    rows = [list(row) + [Fraction(1)] for row in cov]
    for col in range(n):
        pivot = next(r for r in range(col, n) if rows[r][col] != 0)
        rows[col], rows[pivot] = rows[pivot], rows[col]
        rows[col] = [value / rows[col][col] for value in rows[col]]
        for r in range(n):
            if r != col and rows[r][col] != 0:
                factor = rows[r][col]
                rows[r] = [a - factor * b for a, b in zip(rows[r], rows[col])]
    solution = [row[n] for row in rows]
    total = sum(solution, Fraction(0))
    return [value / total for value in solution]


def estimate(square_sum: float, fourth_sum: float, n: int) -> tuple[float, float]:
    """Mean of n squared errors and the standard error of that mean, from the running totals."""
    mean = square_sum / n
    variance = (fourth_sum - n * mean * mean) / (n - 1)
    return mean, math.sqrt(variance / n)


def platform_guard() -> None:
    info = sys.float_info
    if (info.radix, info.mant_dig, sys.float_repr_style) != (2, 53, "short"):
        raise ArithmeticError("this Python does not use IEEE 754 doubles with shortest-repr formatting")
    check("arithmetic: the literal for sqrt(12) is the correctly rounded square root", SQRT12 == math.sqrt(12.0))
    check("arithmetic: the first draw of seed 1 has the expected bits",
          random.Random(1).random().hex() == "0x1.132d8f91b7584p-3", random.Random(1).random().hex())


def observed_setup(snapshot: dict) -> dict:
    """What the lesson quotes from the snapshot, with its counts made again from the rows."""
    if snapshot["source"]["commit"] != PINNED_COMMIT:
        raise ValueError("observed-input.json is not a snapshot of the pinned commit")
    policy, panel, pair = snapshot["orchestration_policy"], snapshot["tribunal_panel"], snapshot["council"]
    verdicts = snapshot["council_records"]
    rule = policy["cross_validation_rule"]
    settings = {entry["key"]: entry for entry in policy["confidence_calibration"]}
    counts = {
        "confidence_calibration_entries": len(policy["confidence_calibration"]),
        "cross_validation_models": len(rule["models"]),
        "cross_validation_providers": len(set(rule["provider_of_each_model"].values())),
        "tribunal_panel_personas": len({member["persona"] for member in panel["members"]}),
        "pull_request_fields_in_every_persona_prompt": len(panel["pull_request_fields_in_every_persona_prompt"]),
        "member_fields_in_the_persona_prompt": len(panel["member_fields_in_the_persona_prompt"]),
        "lines_that_read_a_persona_score": len(panel["lines_that_read_a_persona_score"]),
        "council_reviewers": len({reviewer["name"] for reviewer in pair["reviewers"]}),
        "verdicts_a_persona_may_return": len(set(panel["verdicts_a_persona_may_return"]["values"])),
        "council_records": len({record["id"] for record in verdicts["records"]}),
        "council_scores": sum(len(record["scores"]) for record in verdicts["records"]),
    }
    by_reviewer: dict[str, list] = {}
    for record in verdicts["records"]:
        for score in record["scores"]:
            by_reviewer.setdefault(score["reviewer"], []).append(score["correctness_score"])
    check("observed: the counts made here from the rows equal those made by extract.py", counts == snapshot["counts"])
    check("observed: the three confidence settings used are numbers between 0 and 1",
          all(0 <= Fraction(settings[key]["number"]) <= 1
              for key in ("single_model", "two_model_agreement", "two_model_disagreement")))
    return {
        "note": "Observed at the pinned commit: three places where the project puts one question to several judges, "
                "and the scores the council has recorded. No persona's answer and no outcome is in the files read; "
                "nothing below measures a correlation.",
        "policy": {"path": policy["path"], "version": policy["version"],
                   "confidence_calibration": {key: {"line": entry["line"], "value": entry["value"],
                                                    "comment": entry["comment"]} for key, entry in settings.items()},
                   "cross_validation_rule": rule},
        "tribunal_panel": {
            "personas": counts["tribunal_panel_personas"],
            "sent_to_every_persona": panel["pull_request_fields_in_every_persona_prompt"],
            "limits_on_what_every_persona_is_sent": panel["limits_on_what_every_persona_is_sent"],
            "different_for_each_persona": panel["member_fields_in_the_persona_prompt"],
            "model_argument_of_the_run": panel["model_argument_of_the_run"],
            "verdicts_a_persona_may_return": panel["verdicts_a_persona_may_return"],
            "score_a_persona_may_return": panel["score_a_persona_may_return"],
            "lines_that_read_a_persona_score": panel["lines_that_read_a_persona_score"],
            "consensus_rule": panel["consensus_rule_named_in_both_files"]},
        "council": {"reviewers": counts["council_reviewers"], "statements": pair["statements"],
                    "confidence_line": pair["confidence_line"]},
        "council_records": {"folder": verdicts["folder"], "verdicts": counts["council_records"],
                            "scores": counts["council_scores"], "scores_by_reviewer": by_reviewer,
                            "keys_naming_an_outcome": verdicts["keys_naming_an_outcome"]},
        "counts": counts,
    }


def closed_form(grid: dict) -> dict:
    """The table of the lesson: mean squared error of the average of k forecasters, for every rho of the grid."""
    by_rho = {}
    for text in grid["rhos"]:
        rho, rows = Fraction(text), []
        for k in range(1, grid["k_max"] + 1):
            mse = mse_of_average(rho, k)
            row = {"k": k, "mse": exact(mse), "rmse": sim(math.sqrt(float(mse))), "worth": exact(worth(rho, k)),
                   "share_of_one_forecaster_s_mse_removed_percent": percent(1 - mse)}
            if k > 1:
                before = mse_of_average(rho, k - 1)
                check("closed form: one more forecaster lowers the mean squared error by (1 - rho) / (k (k - 1))",
                      before - mse == (1 - rho) / (k * (k - 1)))
                row["drop_from_one_more"] = exact(before - mse)
                row["drop_from_one_more_percent"] = percent((before - mse) / before)
            check("closed form: worth times the mean squared error of the average equals sigma^2", worth(rho, k) * mse == 1)
            rows.append(row)
        check("closed form: one forecaster has a mean squared error of sigma^2 at every rho", mse_of_average(rho, 1) == 1)
        check("closed form: the mean squared error stays above the floor rho sigma^2",
              all(mse_of_average(rho, k) > rho for k in range(1, grid["k_max"] + 1)))
        by_rho[text] = {"floor": exact(rho), "floor_rmse": sim(math.sqrt(float(rho))),
                        "worth_ceiling": None if rho == 0 else exact(1 / rho), "rows": rows}
    check("known answer: rho = 0 gives the independent result sigma^2 / k",
          all(mse_of_average(Fraction(0), k) == Fraction(1, k) for k in range(1, grid["k_max"] + 1)))
    return {
        "formula": "mse of the average of k forecasters = bias^2 + sigma^2 * (rho + (1 - rho) / k); "
                   "worth = k / (1 + (k - 1) * rho); floor = bias^2 + rho * sigma^2; worth ceiling = 1 / rho",
        "unit": "sigma^2 = 1 and bias = 0: every mse is a multiple of one forecaster's mean squared error",
        "share_of_the_removable_part_removed": "1 - 1/k at every rho below 1: (1 - mse) / (1 - rho)",
        "by_rho": by_rho,
    }


def exact_enumeration(cfg: dict, k_max: int) -> dict:
    """Signs instead of draws: every pattern of +1 and -1 is listed, so nothing is sampled."""
    hand = cfg["hand_case"]
    rho, k = Fraction(hand["rho"]), hand["k"]
    alpha, beta = Fraction(3, 5), Fraction(4, 5)
    check("hand-computed case: 0.6 and 0.8 are the exact square roots of rho and 1 - rho",
          alpha * alpha == rho and beta * beta == 1 - rho)
    patterns = []
    for signs in product((1, -1), repeat=k + 1):
        error = alpha * signs[0] + beta * Fraction(sum(signs[1:]), k)
        patterns.append({"common": signs[0], "individual": list(signs[1:]), "error_of_the_average": exact(error),
                         "squared": exact(error * error), "_squared": error * error})
    mse = sum((p["_squared"] for p in patterns), Fraction(0)) / len(patterns)
    check("hand-computed case: two forecasters with rho = 0.36 and sign errors have a mean squared error of 0.68",
          mse == Fraction(hand["expected_mse"]) == mse_of_average(rho, k))
    moments = []
    for size in range(1, k_max + 1):
        count = cc = cross = square = 0
        for signs in product((1, -1), repeat=size + 1):
            total = sum(signs[1:])
            count, cc, cross, square = count + 1, cc + signs[0] * signs[0], cross + signs[0] * total, square + total * total
        check("exact enumeration: over all sign patterns E[C^2] = 1, E[C * mean(I)] = 0 and E[mean(I)^2] = 1/k",
              (Fraction(cc, count), cross, Fraction(square, count * size * size)) == (1, 0, Fraction(1, size)))
        moments.append({"k": size, "sign_patterns": count, "mean_of_c_squared": exact(Fraction(cc, count)),
                        "mean_of_c_times_mean_i": exact(Fraction(cross, count)),
                        "mean_of_mean_i_squared": exact(Fraction(square, count * size * size))})
    return {
        "note": cfg["note"],
        "why_it_settles_the_closed_form": "(sqrt(rho) C + sqrt(1 - rho) mean(I))^2 = rho C^2 + 2 sqrt(rho (1 - rho)) C "
                                          "mean(I) + (1 - rho) mean(I)^2; with the three means below its mean is "
                                          "rho + (1 - rho) / k for every rho",
        "hand_case": {"k": k, "rho": exact(rho), "sqrt_rho": exact(alpha), "sqrt_one_minus_rho": exact(beta),
                      "patterns": patterns, "mse": exact(mse), "closed_form": exact(mse_of_average(rho, k))},
        "moments_by_k": moments,
    }


def simulate_grid(cfg: dict, rhos: list[Fraction], k_max: int) -> dict:
    """Running totals of the squared error of the average (and of its square) for every rho and every k."""
    rng = random.Random(cfg["seed"])
    alphas = [math.sqrt(float(rho)) for rho in rhos]
    betas = [math.sqrt(float(1 - rho)) for rho in rhos]
    spread_ks, ks = cfg["spread_ks"], range(k_max)
    square = [[0.0] * k_max for _ in rhos]
    fourth = [[0.0] * k_max for _ in rhos]
    own = [[0.0] * len(spread_ks) for _ in rhos]  # mean squared error of one forecaster among the first k
    last = [[0.0, 0.0] for _ in rhos]  # what the last forecaster removes, occasion by occasion, and its square
    early = None
    for occasion in range(cfg["occasions"]):
        if occasion == cfg["direct_check"]["occasions"]:
            early = {"square": [row[:] for row in square], "own": [row[:] for row in own]}
        common = draw(rng)
        total = total_squares = 0.0
        means, totals, totals_squares = [], [], []
        for k in ks:
            part = draw(rng)
            total += part
            total_squares += part * part
            means.append(total / (k + 1))
            totals.append(total)
            totals_squares.append(total_squares)
        for r, alpha in enumerate(alphas):
            shared, beta = alpha * common, betas[r]
            row2, row4 = square[r], fourth[r]
            for k in ks:
                error = shared + beta * means[k]  # the average of the first k + 1 errors
                squared = error * error
                row2[k] += squared
                row4[k] += squared * squared
            for j, k in enumerate(spread_ks):
                own[r][j] += (k * shared * shared + 2.0 * shared * beta * totals[k - 1]
                              + beta * beta * totals_squares[k - 1]) / k
            before, after = shared + beta * means[k_max - 2], shared + beta * means[k_max - 1]
            removed = before * before - after * after
            last[r][0] += removed
            last[r][1] += removed * removed
    return {"square": square, "fourth": fourth, "own": own, "last": last, "early": early, "alphas": alphas,
            "betas": betas}


def simulation_section(raw: dict, grid: dict, cfg: dict, limit: float) -> dict:
    """Simulated against closed form, cell by cell, in units of the simulation's own standard error."""
    n, by_rho, largest, within, control = cfg["occasions"], {}, 0.0, 0, []
    for r, text in enumerate(grid["rhos"]):
        rho, rows = Fraction(text), []
        for k in range(1, grid["k_max"] + 1):
            mean, error = estimate(raw["square"][r][k - 1], raw["fourth"][r][k - 1], n)
            formula = mse_of_average(rho, k)
            distance = (mean - float(formula)) / error
            largest, within = max(largest, abs(distance)), within + (abs(distance) <= limit)
            row = {"k": k, "closed_form": exact(formula), "simulated": sim(mean), "standard_error": sim(error),
                   "standard_errors_from_the_closed_form": errors_from(distance)}
            if rho > 0 and k > 1:
                wrong = (mean - 1.0 / k) / error
                control.append(abs(wrong))
                row["standard_errors_from_the_independent_formula"] = errors_from(wrong)
            rows.append(row)
        by_rho[text] = rows
    cells = len(grid["rhos"]) * grid["k_max"]
    return {
        "seed": cfg["seed"], "occasions": n, "draw_order": cfg["draw_order"],
        "standard_error": "of the simulated mean squared error: sqrt(sample variance of the squared errors / occasions)",
        "cells": cells, "standard_errors_limit": limit, "cells_within_the_limit": within,
        "largest_distance_in_standard_errors": errors_from(largest),
        "independent_formula_control": {
            "note": "The same test applied to a formula known to be wrong when rho > 0: sigma^2 / k.",
            "cells": len(control), "cells_rejected": sum(distance > limit for distance in control),
            "smallest_distance_in_standard_errors": errors_from(min(control))},
        "by_rho": by_rho,
    }


def last_forecaster(raw: dict, grid: dict, cfg: dict, limit: float) -> dict:
    """What the last forecaster removes: the same occasions with k_max - 1 and with k_max forecasters, in pairs."""
    n, k, rows = cfg["occasions"], grid["k_max"], {}
    for r, text in enumerate(grid["rhos"]):
        rho = Fraction(text)
        mean, error = estimate(raw["last"][r][0], raw["last"][r][1], n)
        formula = (1 - rho) / (k * (k - 1))
        before = raw["square"][r][k - 2] / n
        rows[text] = {"closed_form": exact(formula), "simulated": small(mean), "standard_error": small(error),
                      "standard_errors_from_the_closed_form": errors_from((mean - float(formula)) / error),
                      "within_the_limit": abs((mean - float(formula)) / error) <= limit,
                      "standard_errors_from_zero": errors_from(mean / error),
                      "closed_form_percent_of_the_mse_before": percent(formula / mse_of_average(rho, k - 1)),
                      "simulated_percent_of_the_simulated_mse_before":
                          round(100.0 * mean / before, DECIMALS["percent"]) + 0.0}
        if rho > 0:
            rows[text]["standard_errors_from_the_independent_drop"] = errors_from((mean - 1.0 / (k * (k - 1))) / error)
    return {"note": "The squared error of the average of the first k - 1 forecasters minus that of the first k, on each "
                    "occasion; its mean estimates the drop far more sharply than the difference of two cells of the "
                    "table, because both use the same draws.",
            "from_k": k - 1, "to_k": k, "formula": "drop = sigma^2 (1 - rho) / (k (k - 1))",
            "independent_drop": exact(Fraction(1, k * (k - 1))), "by_rho": rows}


def direct_check(cfg: dict, raw: dict, k_max: int) -> dict:
    """The first occasions again, one error at a time: the fast path, the spread identity and a planted fault."""
    rng = random.Random(cfg["seed"])
    count, spread_ks, tolerance = cfg["direct_check"]["occasions"], cfg["spread_ks"], cfg["direct_check"]["tolerance"]
    square = [[0.0] * k_max for _ in raw["alphas"]]
    own = [[0.0] * len(spread_ks) for _ in raw["alphas"]]
    identities = violations = planted = detected = 0
    for _ in range(count):
        common = draw(rng)
        parts = [draw(rng) for _ in range(k_max)]
        for r, alpha in enumerate(raw["alphas"]):
            errors = [alpha * common + raw["betas"][r] * part for part in parts]
            total, averages = 0.0, []
            for k, error in enumerate(errors, start=1):
                total += error
                averages.append(total / k)
                square[r][k - 1] += averages[-1] * averages[-1]
            for j, k in enumerate(spread_ks):
                mean_square = spread = stale = 0.0
                for error in errors[:k]:
                    mean_square += error * error / k
                    spread += (error - averages[k - 1]) * (error - averages[k - 1]) / k
                    stale += (error - averages[k - 2]) * (error - averages[k - 2]) / k
                own[r][j] += mean_square
                identities += 1
                violations += abs(averages[k - 1] * averages[k - 1] - (mean_square - spread)) > 1e-12
                planted += 1
                detected += abs(averages[k - 2] * averages[k - 2] - (mean_square - stale)) > 1e-12
    gap = max(abs(a - b) for fast, slow in ((raw["early"]["square"], square), (raw["early"]["own"], own))
              for row_fast, row_slow in zip(fast, slow) for a, b in zip(row_fast, row_slow))
    check("direct check: the fast path equals errors built and averaged one by one on the first occasions",
          gap < tolerance, f"largest gap {gap}")
    check("accounting identity: squared error of the average = mean squared error of the forecasters - their spread",
          violations == 0, f"{violations} violations")
    check("negative control: the identity fails when the average of one forecaster too few is used",
          detected > 0.99 * planted, f"{detected} of {planted}")
    return {"occasions": count, "totals_compared": (k_max + len(spread_ks)) * len(raw["alphas"]),
            "largest_gap_between_the_two_paths_is_below": tolerance,
            "identity": {"statement": "(error of the average)^2 = mean of the squared errors of the k forecasters "
                                      "- mean of the squared distances of their forecasts from the average",
                         "cases_checked": identities, "violations_above_1e-12": violations},
            "stale_average_control": {"cases": planted, "detected": detected}}


def spread_section(raw: dict, grid: dict, cfg: dict) -> dict:
    """How far the forecasters are from one another, next to how far their average is from the outcome."""
    n, rows = cfg["occasions"], []
    for r, text in enumerate(grid["rhos"]):
        rho = Fraction(text)
        for j, k in enumerate(cfg["spread_ks"]):
            expected = (1 - rho) * Fraction(k - 1, k)
            own, average = raw["own"][r][j] / n, raw["square"][r][k - 1] / n
            check("spread: the closed forms obey the identity sigma^2 = mse of the average + expected spread",
                  mse_of_average(rho, k) + expected == 1)
            rows.append({
                "rho": exact(rho), "k": k,
                "expected_spread": exact(expected), "simulated_spread": sim(own - average),
                "typical_distance_between_a_forecast_and_the_average": sim(math.sqrt(float(expected))),
                "mse_of_the_average": exact(mse_of_average(rho, k)),
                "typical_error_of_the_average": sim(math.sqrt(float(mse_of_average(rho, k)))),
                "simulated_mse_of_one_forecaster": sim(own),
                "rho_recovered_from_scored_forecasts": sim(1.0 - (k / (k - 1)) * (own - average) / own)})
    return {
        "definition": "spread = mean over the k forecasters of (forecast - average of the k forecasts)^2; it needs "
                      "no outcome. expected spread = sigma^2 (1 - rho) (k - 1) / k: the common part cancels.",
        "recovery": "rho recovered = 1 - (k / (k - 1)) * spread / mean squared error of one forecaster, which needs "
                    "the outcomes; here from all the simulated occasions",
        "simulated_spread_is": "the simulated mean squared error of one forecaster minus that of the average",
        "rows": rows,
    }


def shared_bias(cfg: dict, limit: float) -> dict:
    """Every forecaster is off by the same amount on every occasion: each error is built and averaged directly."""
    rng = random.Random(cfg["seed"])
    rho, bias, ks, n = Fraction(cfg["rho"]), Fraction(cfg["bias"]), cfg["ks"], cfg["occasions"]
    alpha, beta, offset = math.sqrt(float(rho)), math.sqrt(float(1 - rho)), float(bias)
    first, square, fourth = [0.0] * len(ks), [0.0] * len(ks), [0.0] * len(ks)
    for _ in range(n):
        common = draw(rng)
        errors = [offset + alpha * common + beta * draw(rng) for _ in range(max(ks))]
        for j, k in enumerate(ks):
            total = 0.0
            for error in errors[:k]:
                total += error
            average = total / k
            first[j] += average
            square[j] += average * average
            fourth[j] += average * average * average * average
    rows = []
    for j, k in enumerate(ks):
        mean, error = estimate(square[j], fourth[j], n)
        formula, variance = mse_of_average(rho, k, bias=bias), mse_of_average(rho, k)
        check("shared bias: the closed form with a bias exceeds the one without by bias^2 at every k",
              formula - variance == bias * bias)
        rows.append({"k": k, "closed_form": exact(formula), "bias_squared": exact(bias * bias),
                     "variance_of_the_average": exact(variance), "bias_share_of_the_mse_percent": percent(bias * bias / formula),
                     "simulated": sim(mean), "standard_error": sim(error),
                     "standard_errors_from_the_closed_form": errors_from((mean - float(formula)) / error),
                     "within_the_limit": abs((mean - float(formula)) / error) <= limit,
                     "simulated_mean_error_of_the_average": sim(first[j] / n)})
    return {"seed": cfg["seed"], "occasions": n, "rho": exact(rho), "bias": exact(bias),
            "formula": "mse = bias^2 + sigma^2 (rho + (1 - rho) / k)", "floor": exact(bias * bias + rho),
            "floor_once_the_bias_is_subtracted": exact(rho), "rows": rows}


def newcomer_covariance(n: int, rho: Fraction, link: Fraction) -> list[list[Fraction]]:
    """n panel members with pairwise correlation rho, then one newcomer with correlation link to each (sigma = 1)."""
    cov = [[Fraction(1) if i == j else rho for j in range(n)] + [link] for i in range(n)]
    return cov + [[link] * n + [Fraction(1)]]


def newcomer_row(n: int, rho: Fraction, link: Fraction) -> dict:
    """Closed forms for a panel of n plus one newcomer: equal weights, and the weights that minimise the variance."""
    cov = newcomer_covariance(n, rho, link)
    panel = mse_of_average(rho, n)
    equal = quadratic_form([Fraction(1, n + 1)] * (n + 1), cov)
    weight = (panel - link) / (panel + 1 - 2 * link)
    best = (panel - link * link) / (panel + 1 - 2 * link)
    solved = minimum_variance_weights(cov)
    check("weights: the two-estimator formula equals the exact solution of the full system of weights",
          solved[-1] == weight and all(w == (1 - weight) / n for w in solved[:-1]) and quadratic_form(solved, cov) == best)
    check("weights: the best weights sum to 1 and do at least as well as equal weights",
          sum(solved, Fraction(0)) == 1 and best <= equal)
    return {"correlation_with_a_panel_member": exact(link), "mse_of_the_panel_alone": exact(panel),
            "equal_weights": {"weight_of_the_newcomer": exact(Fraction(1, n + 1)), "mse": exact(equal),
                              "drop_percent": percent((panel - equal) / panel), "worth": exact(1 / equal)},
            "best_weights": {"weight_of_the_newcomer": exact(weight), "mse": exact(best),
                             "drop_percent": percent((panel - best) / panel), "worth": exact(1 / best)},
            "_equal": equal, "_best": best, "_weight": weight}


def newcomer_closed(cfg: dict, grid: dict) -> dict:
    n, context, model = cfg["panel_size"], Fraction(cfg["context_share"]), Fraction(cfg["model_share"])
    rho, kinds = context + model, {}
    for kind in cfg["kinds"]:
        link = context * kind["shares_context"] + model * kind["shares_model"]
        kinds[kind["key"]] = {"shares_context": kind["shares_context"], "shares_model": kind["shares_model"]} \
            | newcomer_row(n, rho, link)
    same = kinds["same_model_same_context"]
    check("known answer: a newcomer of the panel's own kind gives the closed form for one more forecaster, and "
          "equal weights are then the best weights",
          same["_equal"] == same["_best"] == mse_of_average(rho, n + 1) and same["_weight"] == Fraction(1, n + 1))
    outsider = kinds["other_model_own_context"]
    check("known answer: independent sources add their worth", 1 / outsider["_best"] == worth(rho, n) + 1)
    by_rho = {}
    for text in grid["rhos"]:
        row = newcomer_row(n, Fraction(text), Fraction(0))
        by_rho[text] = {"thirteen_alone": row["mse_of_the_panel_alone"],
                        "fourteen_of_the_same_source": exact(mse_of_average(Fraction(text), n + 1)),
                        "thirteen_plus_one_independent_equal_weights": row["equal_weights"],
                        "thirteen_plus_one_independent_best_weights": row["best_weights"]}
    return {
        "note": cfg["note"], "error": cfg["error"], "panel_size": n, "context_share": exact(context),
        "model_share": exact(model), "panel_correlation": exact(rho),
        "formulas": "equal weights: every forecast weighs 1 / (n + 1). best weights (Bates and Granger): with v the "
                    "mse of the panel's average and c the newcomer's correlation with a panel member, weight of the "
                    "newcomer = (v - c) / (v + 1 - 2 c) and mse = (v - c^2) / (v + 1 - 2 c); each panel member "
                    "weighs (1 - weight) / n. drop_percent is the fall of the mse from the panel alone; "
                    "worth = 1 / mse.",
        "kinds": kinds,
        "one_independent_newcomer_by_rho": by_rho,
    }


def newcomer_simulation(cfg: dict, closed: dict, limit: float) -> dict:
    """The four newcomers on the same seeded occasions; every error is built from its three parts."""
    rng = random.Random(cfg["seed"])
    n, occasions = cfg["panel_size"], cfg["occasions"]
    context, model = Fraction(cfg["context_share"]), Fraction(cfg["model_share"])
    a, m, s = math.sqrt(float(context)), math.sqrt(float(model)), math.sqrt(float(1 - context - model))
    keys = [kind["key"] for kind in cfg["kinds"]]
    flags = [(kind["shares_context"], kind["shares_model"]) for kind in cfg["kinds"]]
    weights = [float(closed["kinds"][key]["_weight"]) for key in keys]
    totals = {key: {"equal": [0.0, 0.0], "best": [0.0, 0.0]} for key in keys}
    alone = [0.0, 0.0]
    for _ in range(occasions):
        contexts, models = (draw(rng), draw(rng)), (draw(rng), draw(rng))
        panel = 0.0
        for _ in range(n):
            panel += a * contexts[0] + m * models[0] + s * draw(rng)
        own = s * draw(rng)
        squared = (panel / n) * (panel / n)
        alone[0] += squared
        alone[1] += squared * squared
        for key, (same_context, same_model), weight in zip(keys, flags, weights):
            newcomer = a * contexts[0 if same_context else 1] + m * models[0 if same_model else 1] + own
            for name, error in (("equal", (panel + newcomer) / (n + 1)),
                                ("best", (1.0 - weight) * (panel / n) + weight * newcomer)):
                squared = error * error
                totals[key][name][0] += squared
                totals[key][name][1] += squared * squared
    rows, within = {}, 0
    for key in keys:
        rows[key] = {}
        for name, formula in (("equal", closed["kinds"][key]["_equal"]), ("best", closed["kinds"][key]["_best"])):
            mean, error = estimate(totals[key][name][0], totals[key][name][1], occasions)
            distance = (mean - float(formula)) / error
            within += abs(distance) <= limit
            rows[key][name + "_weights"] = {"closed_form": exact(formula), "simulated": sim(mean),
                                            "standard_error": sim(error),
                                            "standard_errors_from_the_closed_form": errors_from(distance)}
    mean, error = estimate(alone[0], alone[1], occasions)
    panel_formula = mse_of_average(context + model, n)
    return {"seed": cfg["seed"], "occasions": occasions, "draw_order": cfg["draw_order"],
            "panel_alone": {"closed_form": exact(panel_formula), "simulated": sim(mean), "standard_error": sim(error),
                            "standard_errors_from_the_closed_form": errors_from((mean - float(panel_formula)) / error)},
            "cells": 2 * len(keys), "standard_errors_limit": limit, "cells_within_the_limit": within, "kinds": rows}


def two_judges(p: Fraction, rho: Fraction) -> dict:
    """Joint distribution of 'right' for two judges of accuracy p whose right/wrong outcomes have correlation rho."""
    q = 1 - p
    cells = {"both_right": p * p + rho * p * q, "both_wrong": q * q + rho * p * q, "one_right_one_wrong": 2 * p * q * (1 - rho)}
    check("probabilities: the three cases of two judges sum to 1", sum(cells.values(), Fraction(0)) == 1)
    check("probabilities: each judge is right with probability p and the correlation is rho",
          cells["both_right"] + cells["one_right_one_wrong"] / 2 == p and cells["both_right"] - p * p == rho * p * q)
    check("probabilities: no case of two judges has a negative probability", min(cells.values()) >= 0)
    agree = cells["both_right"] + cells["both_wrong"]
    return cells | {"agree": agree, "right_given_agreement": cells["both_right"] / agree}


def agreement_of_two(snapshot: dict, cfg: dict) -> dict:
    """What agreement between two judges is worth, read against the policy's confidence settings."""
    settings = {entry["key"]: Fraction(entry["number"]) for entry in snapshot["orchestration_policy"]["confidence_calibration"]}
    p, value, split = settings["single_model"], settings["two_model_agreement"], settings["two_model_disagreement"]
    q = 1 - p
    rows = []
    for text in cfg["correlations"]:
        case = two_judges(p, Fraction(text))
        rows.append({"rho": exact(Fraction(text)), "both_right": exact(case["both_right"]),
                     "both_wrong": exact(case["both_wrong"]), "one_right_one_wrong": exact(case["one_right_one_wrong"]),
                     "they_agree": exact(case["agree"]), "right_given_agreement": exact(case["right_given_agreement"]),
                     "gain_over_one_judge": exact(case["right_given_agreement"] - p)})
    check("agreement: its worth falls as the correlation rises, from p^2 / (p^2 + q^2) down to p",
          all(a["right_given_agreement"] > b["right_given_agreement"] for a, b in zip(rows, rows[1:]))
          and two_judges(p, Fraction(0))["right_given_agreement"] == p * p / (p * p + q * q)
          and two_judges(p, Fraction(1))["right_given_agreement"] == p)
    implied = (p * p - value * (p * p + q * q)) / (p * q * (2 * value - 1))
    reachable = 0 <= implied <= 1
    if reachable:
        check("agreement: at the implied correlation, agreement is worth exactly the policy's value",
              two_judges(p, implied)["right_given_agreement"] == value)
    check("agreement: when two equally accurate judges disagree, each is right with probability 1/2",
          two_judges(p, Fraction(0))["one_right_one_wrong"] / 2 / two_judges(p, Fraction(0))["one_right_one_wrong"]
          == Fraction(1, 2))
    odds = math.sqrt(float(value / (1 - value)))
    return {
        "reading": cfg["note"],
        "accuracy_of_each_judge": exact(p), "policy_value_for_agreement": exact(value),
        "policy_value_for_disagreement": exact(split),
        "formula": "right given agreement = (p^2 + rho p q) / (p^2 + q^2 + 2 rho p q), with q = 1 - p",
        "rows": rows,
        "correlation_at_which_agreement_is_worth_the_policy_value": {
            "formula": "rho = (p^2 - v (p^2 + q^2)) / (p q (2 v - 1)), with v the policy's value for agreement",
            "exact": str(implied), "value": exact(implied) if reachable else None, "between_0_and_1": reachable,
            "they_agree": exact(two_judges(p, implied)["agree"]) if reachable else None},
        "right_given_disagreement": {"value": exact(Fraction(1, 2)), "equals_the_policy_value": split == Fraction(1, 2),
                                     "depends_on_rho": False},
        "lowest_accuracy_for_which_independent_judges_reach_the_policy_value": sim(odds / (1.0 + odds)),
    }


def scored_log(cfg: dict, agents: int) -> dict:
    """Logs of scored forecasts cut from seeded occasions: how well each length recovers rho."""
    rng = random.Random(cfg["seed"])
    rhos = [Fraction(text) for text in cfg["rhos"]]
    alphas, betas = [math.sqrt(float(rho)) for rho in rhos], [math.sqrt(float(1 - rho)) for rho in rhos]
    lengths = cfg["occasions_per_log"]
    estimates = {text: {length: [] for length in lengths} for text in cfg["rhos"]}
    for _ in range(cfg["logs"]):
        own, spread = [0.0] * len(rhos), [0.0] * len(rhos)
        for occasion in range(1, max(lengths) + 1):
            common = draw(rng)
            parts = [draw(rng) for _ in range(agents)]
            for r, alpha in enumerate(alphas):
                errors = [alpha * common + betas[r] * part for part in parts]
                total = 0.0
                for error in errors:
                    total += error
                average = total / agents
                for error in errors:
                    own[r] += error * error / agents
                    spread[r] += (error - average) * (error - average) / agents
            if occasion in lengths:
                for r, text in enumerate(cfg["rhos"]):
                    estimates[text][occasion].append(1.0 - (agents / (agents - 1)) * spread[r] / own[r])
    rows = []
    for text in cfg["rhos"]:
        for length in lengths:
            ordered = sorted(estimates[text][length])
            ranks = {f"percentile_{q}": sim(ordered[math.ceil(q * len(ordered) / 100) - 1]) for q in cfg["percentiles"]}
            rows.append({"true_rho": exact(Fraction(text)), "occasions_per_log": length, "logs": len(ordered)} | ranks)
    for a, b in zip(rows, rows[1:]):
        if a["true_rho"] == b["true_rho"]:
            check("scored logs: a longer log gives a narrower range of estimates",
                  b["percentile_95"] - b["percentile_5"] < a["percentile_95"] - a["percentile_5"])
    return {"note": cfg["note"], "agents": agents, "seed": cfg["seed"], "logs": cfg["logs"],
            "percentile_rule": cfg["percentile_rule"], "draw_order": cfg["draw_order"], "rows": rows}


def yes_no_closed(cfg: dict, personas: int) -> dict:
    """Limits when errors are scored against a yes/no outcome: the outcome's unforeseeable part is shared by all."""
    low, high, s = Fraction(cfg["probability_low"]), Fraction(cfg["probability_high"]), Fraction(cfg["forecaster_sd"])
    noise = (low + high) / 2 - (low * low + low * high + high * high) / 3  # E[p (1 - p)], p uniform on [low, high]
    integral = ((high ** 2 / 2 - high ** 3 / 3) - (low ** 2 / 2 - low ** 3 / 3)) / (high - low)
    check("yes/no outcome: E[p (1 - p)] from the moments of p equals the integral of p (1 - p)", noise == integral)
    var = s * s
    by_rho = {}
    for text in cfg["rhos"]:
        rho = Fraction(text)
        by_rho[text] = {
            "correlation_of_two_personas_scored_errors": exact((noise + rho * var) / (noise + var)),
            "estimate_from_the_spread_tends_to": exact((noise + rho * var) / (noise + var)),
            "estimate_against_the_outsider_tends_to": exact(rho),
            "mse_of_the_panel_average": exact(noise + var * (rho + (1 - rho) / personas)),
        }
    return {
        "variance_of_the_unforeseeable_part": exact(noise), "forecaster_variance": exact(var),
        "mse_of_one_forecaster": exact(noise + var),
        "share_of_one_forecaster_s_mse_that_no_forecaster_removes_percent": percent(noise / (noise + var)),
        "by_rho": by_rho,
    }


def sign(rng: random.Random) -> float:
    return 1.0 if rng.random() < 0.5 else -1.0


def add_pull_request(sums: dict, errors: list[float]) -> None:
    """Running sums of one log: per forecaster (personas, then the outsider), and over pairs of personas."""
    k, total, squares = len(errors) - 1, 0.0, 0.0
    for i in range(k + 1):
        sums["m"][i] += errors[i]
        sums["q"][i] += errors[i] * errors[i]
        if i < k:
            total += errors[i]
            squares += errors[i] * errors[i]
    sums["pp"] += (total * total - squares) / 2
    sums["po"] += errors[k] * total
    sums["spread"] += (squares - total * total / k) / k


def yes_no_estimates(sums: dict, n: int, k: int) -> tuple[float, float]:
    """The estimate from the spread and the estimate against the outsider, from the running sums of n pull requests."""
    population, sample, total, squares = 0.0, 0.0, 0.0, 0.0
    for i in range(k):
        centred = sums["q"][i] - sums["m"][i] * sums["m"][i] / n
        population += centred / n
        sample += centred / (n - 1)
        total += sums["m"][i]
        squares += sums["m"][i] * sums["m"][i]
    from_spread = 1.0 - (k / (k - 1)) * (sums["spread"] / n) / (population / k)
    between = (sums["pp"] - (total * total - squares) / 2 / n) / (n - 1) / (k * (k - 1) / 2)
    outside = (sums["po"] - sums["m"][k] * total / n) / (n - 1) / k
    denominator = sample / k - outside
    check("yes/no outcome: the outsider estimate has a non-zero denominator", denominator != 0.0)
    return from_spread, (between - outside) / denominator


def yes_no_logs(cfg: dict, k: int) -> tuple[dict, dict]:
    """Seeded logs of yes/no outcomes; both estimates at each log length, and pooled over every pull request."""
    rng = random.Random(cfg["seed"])
    low = float(Fraction(cfg["probability_low"]))
    width = float(Fraction(cfg["probability_high"]) - Fraction(cfg["probability_low"]))
    s = float(Fraction(cfg["forecaster_sd"]))
    rhos = [Fraction(text) for text in cfg["rhos"]]
    alphas, betas = [s * math.sqrt(float(rho)) for rho in rhos], [s * math.sqrt(float(1 - rho)) for rho in rhos]
    lengths, outside_0_1 = cfg["pull_requests_per_log"], 0
    found = {text: {n: [] for n in lengths} for text in cfg["rhos"]}
    pooled = [{"m": [0.0] * (k + 1), "q": [0.0] * (k + 1), "pp": 0.0, "po": 0.0, "spread": 0.0} for _ in rhos]
    for _ in range(cfg["logs"]):
        sums = [{"m": [0.0] * (k + 1), "q": [0.0] * (k + 1), "pp": 0.0, "po": 0.0, "spread": 0.0} for _ in rhos]
        for n in range(1, max(lengths) + 1):
            p = low + width * rng.random()
            outcome = 1.0 if rng.random() < p else 0.0
            common = sign(rng)
            parts = [sign(rng) for _ in range(k)]
            alone = p + s * sign(rng)
            for r in range(len(rhos)):
                forecasts = [p + alphas[r] * common + betas[r] * part for part in parts] + [alone]
                outside_0_1 += len([f for f in forecasts if not 0.0 <= f <= 1.0])
                add_pull_request(sums[r], [f - outcome for f in forecasts])
            if n in lengths:
                for r, text in enumerate(cfg["rhos"]):
                    found[text][n].append(yes_no_estimates(sums[r], n, k))
        for r in range(len(rhos)):
            for key in ("pp", "po", "spread"):
                pooled[r][key] += sums[r][key]
            for i in range(k + 1):
                pooled[r]["m"][i] += sums[r]["m"][i]
                pooled[r]["q"][i] += sums[r]["q"][i]
    check("yes/no outcome: every forecast lies between 0 and 1, so no forecast was clipped", outside_0_1 == 0)
    total = cfg["logs"] * max(lengths)
    return found, {text: dict(zip(("estimate_from_the_spread", "estimate_against_the_outsider"),
                                  [sim(value) for value in yes_no_estimates(pooled[r], total, k)]))
                   for r, text in enumerate(cfg["rhos"])}


def yes_no_outcome(cfg: dict, personas: int) -> dict:
    """What a log of scored yes/no forecasts can tell about rho, with and without an outsider."""
    closed = yes_no_closed(cfg, personas)
    found, pooled = yes_no_logs(cfg, personas)
    rows = []
    for text in cfg["rhos"]:
        for n in cfg["pull_requests_per_log"]:
            row = {"true_rho": exact(Fraction(text)), "pull_requests": n, "logs": len(found[text][n])}
            for index, name in enumerate(("estimate_from_the_spread", "estimate_against_the_outsider")):
                ordered = sorted(pair[index] for pair in found[text][n])
                row[name] = {f"percentile_{q}": sim(ordered[math.ceil(q * len(ordered) / 100) - 1])
                             for q in cfg["percentiles"]}
            rows.append(row)
    for a, b in zip(rows, rows[1:]):
        if a["true_rho"] == b["true_rho"]:
            wide = [row["estimate_against_the_outsider"] for row in (a, b)]
            check("yes/no outcome: a longer log gives a narrower range of the outsider estimate",
                  wide[1]["percentile_95"] - wide[1]["percentile_5"] < wide[0]["percentile_95"] - wide[0]["percentile_5"])
    return {"note": cfg["note"], "personas": personas, "outsiders": 1, "seed": cfg["seed"], "logs": cfg["logs"],
            "draw_order": cfg["draw_order"], "estimate_from_the_spread": cfg["estimate_from_the_spread"],
            "estimate_against_the_outsider": cfg["estimate_against_the_outsider"], "closed_form": closed,
            "pooled_over_every_pull_request": pooled, "rows": rows}


def worked_examples(cfg: dict, newcomer: dict, bias_cfg: dict, snapshot: dict) -> dict:
    """The figures of the lesson's five exercises, each from the closed forms."""
    ex2, ex3, ex4 = cfg["exercise_2"], cfg["exercise_3"], cfg["exercise_4"]
    rho2, k2 = Fraction(ex2["rho"]), ex2["k"]
    rho3, panel = Fraction(ex3["rho"]), ex3["panel"]
    row3 = newcomer_row(panel, rho3, Fraction(0))
    check("worked example: one outsider among six equal weights gives (n (1 + (n - 1) rho) + 1) / (n + 1)^2",
          row3["_equal"] == (panel * (1 + (panel - 1) * rho3) + 1) / Fraction((panel + 1) ** 2))
    rho4, bias, k4, doubled = Fraction(ex4["rho"]), Fraction(ex4["bias"]), ex4["k"], ex4["doubled_k"]
    if (ex4["rho"], ex4["bias"]) != (bias_cfg["rho"], bias_cfg["bias"]):
        raise ValueError("exercise 4 must use the rho and the bias of the shared_bias section")
    now, more, unbiased = (mse_of_average(rho4, k4, bias=bias), mse_of_average(rho4, doubled, bias=bias),
                           mse_of_average(rho4, k4))
    p = next(Fraction(entry["number"]) for entry in snapshot["orchestration_policy"]["confidence_calibration"]
             if entry["key"] == "single_model")
    return {
        "exercise_1": {key: kind["correlation_with_a_panel_member"] for key, kind in newcomer["kinds"].items()}
        | {"context_share": newcomer["context_share"], "model_share": newcomer["model_share"]},
        "exercise_2": {
            "k": k2, "rho": exact(rho2), "mse": exact(mse_of_average(rho2, k2)),
            "rmse": sim(math.sqrt(float(mse_of_average(rho2, k2)))),
            "mse_if_independent": exact(mse_of_average(Fraction(0), k2)),
            "rmse_if_independent": sim(math.sqrt(float(mse_of_average(Fraction(0), k2)))),
            "share_of_one_forecaster_s_mse_removed_percent": percent(1 - mse_of_average(rho2, k2)),
            "share_removed_if_independent_percent": percent(1 - mse_of_average(Fraction(0), k2)),
            "floor": exact(rho2), "most_that_averaging_can_remove_percent": percent(1 - rho2),
            "share_of_the_removable_part_removed_percent": percent((1 - mse_of_average(rho2, k2)) / (1 - rho2))},
        "exercise_3": {
            "panel": panel, "rho": exact(rho3), "mse_of_the_panel": row3["mse_of_the_panel_alone"],
            "grow_to": ex3["grow_to"], "mse_grown": exact(mse_of_average(rho3, ex3["grow_to"])),
            "floor_of_the_same_source": exact(rho3),
            "one_independent_newcomer_equal_weights": row3["equal_weights"],
            "one_independent_newcomer_best_weights": row3["best_weights"]},
        "exercise_4": {
            "rho": exact(rho4), "bias": exact(bias), "bias_squared": exact(bias * bias),
            "mse_of_one": exact(mse_of_average(rho4, 1, bias=bias)), "k": k4, "mse": exact(now),
            "bias_share_of_the_mse_percent": percent(bias * bias / now), "floor": exact(bias * bias + rho4),
            "doubled_k": doubled, "mse_doubled": exact(more), "drop_from_doubling_percent": percent((now - more) / now),
            "mse_once_the_bias_is_subtracted": exact(unbiased),
            "drop_from_subtracting_the_bias_percent": percent((now - unbiased) / now)},
        "exercise_5": {
            "accuracy_of_each_judge": exact(p),
            "cases": [{"rho": exact(Fraction(text)), "they_agree": exact(two_judges(p, Fraction(text))["agree"]),
                       "right_given_agreement": exact(two_judges(p, Fraction(text))["right_given_agreement"])}
                      for text in cfg["exercise_5"]["correlations"]]},
    }


def transfer_agreement(n: int, var: Fraction, rho: Fraction, one: Fraction) -> dict:
    """Question 5: what the spread of the estimates holds, and what a shared bias does to an estimate of rho."""
    spread = var * (1 - rho) * (n - 1) / n
    centred = 1 - Fraction(n, n - 1) * spread / var
    check("transfer task: once the bias is subtracted, the spread and one forecaster's variance give rho back",
          centred == rho)
    return {
        "note": "the spread holds neither the common part nor the bias; an estimate of rho that divides by the mean "
                "squared error of one forecaster counts a shared bias as shared error",
        "expected_spread": exact(spread),
        "typical_distance_between_an_estimate_and_the_average": sim(math.sqrt(float(spread))),
        "rho_estimated_with_the_bias_left_in": exact(1 - Fraction(n, n - 1) * spread / one),
        "rho_estimated_once_the_bias_is_subtracted": exact(centred),
    }


def transfer_task(task: dict) -> dict:
    """Expected answers of the learner task, from inputs that differ from the lesson's."""
    n, sd, rho, bias = task["forecasters"], Fraction(task["error_sd"]), Fraction(task["rho"]), Fraction(task["bias"])
    var = sd * sd
    one, team = mse_of_average(rho, 1, var, bias), mse_of_average(rho, n, var, bias)
    team_variance = mse_of_average(rho, n, var)
    targets = []
    for target in task["worth_targets"]:
        reachable = target * rho < 1
        size = math.ceil(target * (1 - rho) / (1 - target * rho)) if reachable else None
        if reachable:
            check("transfer task: the smallest team that is worth the target is found",
                  worth(rho, size) >= target and (size == 1 or worth(rho, size - 1) < target))
        targets.append({"independent_forecasters": target, "reachable": reachable, "smallest_team": size})
    row = newcomer_row(n, rho, Fraction(0))
    ninth = mse_of_average(rho, n + 1, var)
    grown = mse_of_average(rho, task["grow_to"], var, bias)
    return {
        "note": task["note"], "unit": task["unit"],
        "q1_one_and_the_average": {
            "bias_squared": exact(bias * bias), "variance_of_one": exact(var), "mse_of_one": exact(one),
            "rmse_of_one": sim(math.sqrt(float(one))), "forecasters": n, "variance_of_the_average": exact(team_variance),
            "mse_of_the_average": exact(team), "rmse_of_the_average": sim(math.sqrt(float(team)))},
        "q2_floor_and_worth": {
            "variance_floor": exact(rho * var), "mse_floor": exact(bias * bias + rho * var),
            "worth": exact(worth(rho, n)), "worth_ceiling": exact(1 / rho), "targets": targets},
        "q3_a_ninth_forecaster": {
            "note": "variances only: the bias is left aside in this question",
            "variance_of_the_eight": exact(team_variance), "same_source_ninth_variance": exact(ninth),
            "same_source_ninth_drop_percent": percent((team_variance - ninth) / team_variance),
            "independent_ninth_equal_weights_variance": exact(row["_equal"] * var),
            "independent_ninth_equal_weights_drop_percent": row["equal_weights"]["drop_percent"],
            "independent_ninth_best_weight": row["best_weights"]["weight_of_the_newcomer"],
            "independent_ninth_best_weights_variance": exact(row["_best"] * var),
            "independent_ninth_best_weights_drop_percent": row["best_weights"]["drop_percent"]},
        "q4_bias": {
            "bias_share_of_the_average_s_mse_percent": percent(bias * bias / team),
            "grow_to": task["grow_to"], "mse_grown": exact(grown), "drop_from_growing_percent": percent((team - grown) / team),
            "mse_once_the_bias_is_subtracted": exact(team_variance),
            "drop_from_subtracting_the_bias_percent": percent((team - team_variance) / team)},
        "q5_what_agreement_shows": transfer_agreement(n, var, rho, one),
    }


def hypothesis_test(thresholds: dict, simulation: dict, closed: dict, newcomer: dict, lone: dict, bias: dict,
                    last: dict) -> dict:
    """The thresholds were written before the first run; this only reports which of them hold."""
    rho = thresholds["rho_for_the_claims"]
    if exact(Fraction(rho)) != newcomer["panel_correlation"]:
        raise ValueError("the hypothesis and the newcomer section must use the same rho")
    fourteenth = closed["by_rho"][rho]["rows"][newcomer["panel_size"]]["drop_from_one_more_percent"]
    simulated = last["by_rho"][rho]["simulated_percent_of_the_simulated_mse_before"]
    if (last["from_k"], last["to_k"]) != (newcomer["panel_size"], newcomer["panel_size"] + 1):
        raise ValueError("the last forecaster of the grid must be the newcomer's fourteenth")
    outsider = newcomer["kinds"]["other_model_own_context"]["equal_weights"]["drop_percent"]
    control = simulation["independent_formula_control"]
    parts = {
        "simulation_within_the_limit_in_every_cell": simulation["cells_within_the_limit"] == simulation["cells"],
        "independent_formula_rejected_in_every_cell_with_rho_above_0": control["cells_rejected"] == control["cells"],
        "fourteenth_same_source_drop_below_threshold":
            max(fourteenth, simulated) < thresholds["fourteenth_same_source_gain_below_percent"],
        "simulated_drop_from_the_fourteenth_within_the_limit_at_every_rho":
            all(row["within_the_limit"] for row in last["by_rho"].values()),
        "independent_newcomer_drop_above_threshold":
            outsider > thresholds["independent_newcomer_equal_weight_gain_above_percent"],
        "newcomer_simulation_within_the_limit_in_every_cell": lone["cells_within_the_limit"] == lone["cells"],
        "shared_bias_adds_bias_squared_at_every_k": all(row["within_the_limit"] for row in bias["rows"]),
    }
    return {"thresholds": {key: value for key, value in thresholds.items() if key != "note"},
            "largest_distance_in_standard_errors": simulation["largest_distance_in_standard_errors"],
            "fourteenth_same_source_drop_percent": fourteenth,
            "fourteenth_same_source_drop_percent_simulated": simulated,
            "independent_newcomer_equal_weight_drop_percent": outsider,
            "parts": parts, "every_part_holds": all(parts.values())}


def strip_private(value):
    if isinstance(value, dict):
        return {key: strip_private(item) for key, item in value.items() if not key.startswith("_")}
    if isinstance(value, list):
        return [strip_private(item) for item in value]
    return value


def analyze(snapshot: dict, scenarios: dict) -> dict:
    rounding = {f"{key}_decimals": value for key, value in DECIMALS.items()}
    if scenarios["rounding"] != rounding:
        raise ValueError("scenarios.json rounding does not match analyze.py")
    platform_guard()
    grid, sim_cfg = scenarios["grid"], scenarios["simulation"]
    limit = scenarios["hypothesis_thresholds"]["standard_errors_limit"]
    observed = observed_setup(snapshot)
    closed = closed_form(grid)
    enumeration = exact_enumeration(scenarios["exact_enumeration"], grid["k_max"])
    raw = simulate_grid(sim_cfg, [Fraction(text) for text in grid["rhos"]], grid["k_max"])
    simulation = simulation_section(raw, grid, sim_cfg, limit)
    fourteenth = last_forecaster(raw, grid, sim_cfg, limit)
    direct = direct_check(sim_cfg, raw, grid["k_max"])
    spread = spread_section(raw, grid, sim_cfg)
    bias = shared_bias(scenarios["shared_bias"], limit)
    newcomer = newcomer_closed(scenarios["newcomer"], grid)
    lone = newcomer_simulation(scenarios["newcomer"], newcomer, limit)
    agreement = agreement_of_two(snapshot, scenarios["agreement_of_two"])
    logs = scored_log(scenarios["scored_log"], observed["counts"]["tribunal_panel_personas"])
    yes_no = yes_no_outcome(scenarios["yes_no_outcome"], observed["counts"]["tribunal_panel_personas"])
    worked = worked_examples(scenarios["worked_examples"], newcomer, scenarios["shared_bias"], snapshot)
    transfer = transfer_task(scenarios["transfer_task"])
    verdict = hypothesis_test(scenarios["hypothesis_thresholds"], simulation, closed, newcomer, lone, bias, fourteenth)
    return strip_private({
        "module_id": scenarios["module_id"],
        "kind": "synthetic, except observed_setup: every other number comes from the error model and the assumptions "
                "in scenarios.json; nothing measures a correlation between the project's agents",
        "rounding": "closed forms are exact fractions rounded half to even to 6 decimals (percentages to 2); simulated "
                    "values, standard errors and square roots to 4 decimals (6 in last_forecaster, whose "
                    "differences are small); distances in standard errors to 2 decimals, computed before rounding",
        "source": snapshot["source"],
        "observed_setup": observed,
        "error_model": scenarios["error_model"],
        "closed_form": closed,
        "exact_enumeration": enumeration,
        "simulation": simulation,
        "last_forecaster": fourteenth,
        "direct_check": direct,
        "spread": spread,
        "shared_bias": bias,
        "newcomer": newcomer,
        "newcomer_simulation": lone,
        "agreement_of_two": agreement,
        "scored_log": logs,
        "yes_no_outcome": yes_no,
        "hypothesis_test": verdict,
        "worked_examples": worked,
        "transfer_task": transfer,
        "checks": [{"check": name, "times_evaluated": times, "passed": True} for name, times in CHECKS.items()],
    })


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--input", type=Path, default=HERE / "observed-input.json")
    parser.add_argument("--scenarios", type=Path, default=HERE / "scenarios.json")
    parser.add_argument("--output", type=Path, default=HERE / "results.json")
    parser.add_argument("--check", action="store_true",
                        help="recompute and compare with the output file instead of writing it")
    args = parser.parse_args()
    CHECKS.clear()
    try:
        result = analyze(json.loads(args.input.read_text(encoding="utf-8")),
                         json.loads(args.scenarios.read_text(encoding="utf-8")))
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
