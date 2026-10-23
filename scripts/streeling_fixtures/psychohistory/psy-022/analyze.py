#!/usr/bin/env python3
"""PSY-022 analysis: three count models for the daily trigger counts, compared by likelihood, AIC and BIC.

Reads observed-input.json (written by extract.py) and scenarios.json, never the
repository, and writes results.json. Every float comes from +, -, * and / on
IEEE 754 doubles and from correctly rounded square roots; logarithms and the
error function are the short series below, and sums of floats are plain loops.
So no value from the C math library enters the output, and the file is the
same on every platform and Python version.

Run from the repository root:
    python -I -B scripts/streeling_fixtures/psychohistory/psy-022/analyze.py
    python -I -B scripts/streeling_fixtures/psychohistory/psy-022/analyze.py --check
"""

from __future__ import annotations

import argparse
import json
import math
import random
import sys
from bisect import bisect_right
from datetime import date, timedelta
from pathlib import Path

# This program lives under scripts/ (CONTRIBUTING.md: no executable code outside scripts/); its data stays
# under state/streeling/fixtures/. FIXTURE_FILE is the path the program would have next to that data.
FIXTURE_FILE = (Path(__file__).resolve().parents[4]
                / "state/streeling/fixtures/psychohistory/psy-022" / Path(__file__).name)

HERE = FIXTURE_FILE.parent
LN2 = 0.6931471805599453  # the double nearest ln 2, written as a literal
SQRT_HALF = 0.7071067811865476  # the double nearest sqrt(1/2)
TWO_OVER_SQRT_PI = 1.1283791670955126  # the double nearest 2 / sqrt(pi)
INV_PHI = 0.6180339887498949  # the double nearest (sqrt(5) - 1) / 2
MODEL_KEYS = ("poisson", "geometric", "negative_binomial")
PARAMETERS = {"poisson": 1, "geometric": 1, "negative_binomial": 2}
DECIMALS = {"log_likelihood": 3, "criterion": 3, "parameter": 6, "share": 4, "expected_days": 2, "autocorrelation": 4,
            "ratio": 2}
# Bit patterns computed with the functions of this script on CPython 3.14 (Windows, x86-64).
# A platform whose arithmetic or generator differs stops here instead of writing different numbers.
FINGERPRINT = {"ln10": "0x1.26bb1bbb55515p+1", "ln119": "0x1.31dd28c89d652p+2", "draw": "0x1.ea9a6b7a123e0p-1"}
CHECKS: dict[str, int] = {}  # self-check -> times evaluated
LN_FACTORIALS = [0.0, 0.0]  # ln(k!) for k = 0, 1, ...; extended on demand


def check(name: str, condition: bool, detail: str = "") -> None:
    """A self-check that can fail: abort instead of writing a wrong result."""
    if not condition:
        raise AssertionError(f"self-check failed: {name}" + (f" ({detail})" if detail else ""))
    CHECKS[name] = CHECKS.get(name, 0) + 1


def rnd(x: float, kind: str) -> float:
    """Round to the stated decimals; adding 0.0 turns a negative zero into zero."""
    return round(x, DECIMALS[kind]) + 0.0


def sig3(x: float) -> float:
    """Round to 3 significant digits with Python's own correctly rounded formatting."""
    return float(f"{x:.2e}")


def add_up(values) -> float:
    """Left-to-right sum of floats (the built-in sum changed its algorithm in Python 3.12)."""
    total = 0.0
    for value in values:
        total += value
    return total


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


def ln_factorial(k: int) -> float:
    while len(LN_FACTORIALS) <= k:
        LN_FACTORIALS.append(LN_FACTORIALS[-1] + ln(float(len(LN_FACTORIALS))))
    return LN_FACTORIALS[k]


def chi_square_tail(c: float) -> float:
    """P(chi-square with 1 degree of freedom > c) = 1 - erf(sqrt(c / 2)), from the power series of erf."""
    x = math.sqrt(c / 2.0)  # square root: correctly rounded by IEEE 754
    term = total = x
    for n in range(1, 80):
        term *= -x * x / n
        total += term / (2 * n + 1)
    return 1.0 - TWO_OVER_SQRT_PI * total


def platform_guard() -> None:
    info = sys.float_info
    if (info.radix, info.mant_dig, sys.float_repr_style) != (2, 53, "short"):
        raise ArithmeticError("this Python does not use IEEE 754 doubles with shortest-repr formatting")
    seen = {"ln10": ln(10.0).hex(), "ln119": ln(119.0).hex(), "draw": random.Random(22).random().hex()}
    check("arithmetic fingerprint: two logarithms and one seeded draw have the expected bits", seen == FINGERPRINT,
          f"got {seen}")
    check("series logarithm agrees with math.log within 1e-13 on 4,000 points",
          all(abs(ln(0.001 * k) - math.log(0.001 * k)) < 1e-13 for k in range(1, 4001)))
    check("series chi-square tail agrees with math.erfc within 1e-12 at 2 and at ln 119",
          all(abs(chi_square_tail(c) - math.erfc(math.sqrt(c / 2.0))) < 1e-12 for c in (2.0, ln(119.0))))
    check("ln(1) = 0 and ln(1/2) = -ln 2 exactly", (ln(1.0), ln(0.5)) == (0.0, -LN2))


def tally(counts: list[int]) -> dict:
    """What the three likelihoods need from a sample: sums, the frequency table, days with a count above j."""
    days = len(counts)
    freq: dict[int, int] = {}
    for x in counts:
        freq[x] = freq.get(x, 0) + 1
    above, remaining = [], days
    for j in range(max(counts)):
        remaining -= freq.get(j, 0)
        above.append(remaining)
    return {"n": days, "total": sum(counts), "sum_sq": sum(x * x for x in counts), "max": max(counts),
            "freq": dict(sorted(freq.items())), "above": above,
            "ln_factorials": add_up(freq[x] * ln_factorial(x) for x in sorted(freq))}


def loglik_poisson(t: dict, lam: float) -> float:
    return t["total"] * ln(lam) - t["n"] * lam - t["ln_factorials"]


def loglik_geometric(t: dict, q: float) -> float:
    return t["n"] * ln(1.0 - q) + t["total"] * ln(q)


def loglik_negbin(t: dict, r: float, mu: float) -> float:
    rising = add_up(days * ln(r + j) for j, days in enumerate(t["above"]))
    return rising - t["ln_factorials"] + t["n"] * r * ln(r / (r + mu)) + t["total"] * ln(mu / (r + mu))


def score(t: dict, r: float) -> float:
    """d(log L)/dr of the negative binomial with mu at the sample mean."""
    return add_up(days / (r + j) for j, days in enumerate(t["above"])) - t["n"] * ln(1.0 + t["total"] / (t["n"] * r))


def negbin_root(t: dict, lower: float, upper: float, tolerance: float) -> tuple:
    """The r at which the score is zero, by bisection on the geometric mean: (r, bisections, status)."""
    n, total = t["n"], t["total"]
    if n * t["sum_sq"] - total * total <= n * total:  # variance (divisor n) <= mean, in integers
        return None, 0, "poisson_limit"
    if score(t, upper) > 0.0:
        return upper, 0, "upper_bound"
    if not score(t, lower) > 0.0:
        raise ArithmeticError(f"the score is not positive at the lower bound {lower}")
    lo, hi, steps = lower, upper, 0
    while hi / lo - 1.0 > tolerance:
        mid = math.sqrt(lo * hi)
        if score(t, mid) > 0.0:
            lo = mid
        else:
            hi = mid
        steps += 1
    return math.sqrt(lo * hi), steps, "interior"


def fit_all(t: dict, bisection: dict) -> dict:
    """Maximum-likelihood fit of the three candidates to one sample (unrounded)."""
    n, total = t["n"], t["total"]
    mean = total / n
    if total == 0:  # every day empty: each model puts probability 1 on the sample
        return {"poisson": {"lambda": 0.0, "loglik": 0.0}, "geometric": {"q": 0.0, "loglik": 0.0},
                "negative_binomial": {"r": None, "mu": 0.0, "loglik": 0.0, "status": "poisson_limit", "bisections": 0}}
    q = total / (n + total)
    poisson = loglik_poisson(t, mean)
    r, steps, status = negbin_root(t, bisection["lower"], bisection["upper"], bisection["relative_tolerance"])
    return {"poisson": {"lambda": mean, "loglik": poisson},
            "geometric": {"q": q, "loglik": loglik_geometric(t, q)},
            "negative_binomial": {"r": r, "mu": mean, "status": status, "bisections": steps,
                                  "loglik": poisson if r is None else loglik_negbin(t, r, mean)}}


def choose(logliks: dict, penalty: float) -> str:
    """Model with the lowest (free parameters * penalty - 2 log L); 'tie' when the two lowest are equal."""
    scores = sorted((PARAMETERS[key] * penalty - 2.0 * logliks[key], key) for key in MODEL_KEYS)
    return "tie" if scores[0][0] == scores[1][0] else scores[0][1]


def golden_max(objective, lo: float, hi: float, tolerance: float) -> tuple[float, int]:
    """Golden-section search for the maximum of a function with one peak on [lo, hi]: (argmax, steps)."""
    a, b = lo, hi
    c, d = b - INV_PHI * (b - a), a + INV_PHI * (b - a)
    fc, fd = objective(c), objective(d)
    steps = 0
    while b - a > tolerance:
        if fc > fd:
            b, d, fd = d, c, fc
            c = b - INV_PHI * (b - a)
            fc = objective(c)
        else:
            a, c, fc = c, d, fd
            d = a + INV_PHI * (b - a)
            fd = objective(d)
        steps += 1
    return (a + b) / 2.0, steps


def pmf_table(key: str, fit: dict, tail: float, at_least: int = 0) -> list[float]:
    """P(0), P(1), ... of a fitted model, from the ratio P(k + 1) / P(k) and normalised by their sum.

    The table stops once a term is below `tail` times the running sum, and not before the index `at_least`; with
    `at_least` set, also not before a term is below `tail` times the term at `at_least`, so that the tail beyond a
    very improbable count is summed too.
    """
    if key == "negative_binomial" and fit["r"] is None:
        key, fit = "poisson", {"lambda": fit["mu"]}
    if key == "poisson":
        def ratio(k: int) -> float:
            return fit["lambda"] / (k + 1)
    elif key == "geometric":
        def ratio(k: int) -> float:
            return fit["q"]
    else:
        odds = fit["mu"] / (fit["r"] + fit["mu"])

        def ratio(k: int) -> float:
            return (k + fit["r"]) / (k + 1) * odds
    terms, running, k = [1.0], 1.0, 0
    while k < at_least or not (ratio(k) < 1.0
                               and terms[-1] < tail * (min(running, terms[at_least]) if at_least else running)):
        terms.append(terms[-1] * ratio(k))
        running += terms[-1]
        k += 1
    return [term / running for term in terms]


def cdf_table(pmf: list[float]) -> list[float]:
    cdf, running = [], 0.0
    for p in pmf:
        running += p
        cdf.append(running)
    cdf[-1] = 1.0
    return cdf


def draw_series(rng: random.Random, cdf: list[float], days: int, copy_probability: float = 0.0) -> list[int]:
    """Independent draws by inverting the cumulative distribution; a day may instead repeat the day before."""
    series: list[int] = []
    for _ in range(days):
        if series and copy_probability > 0.0 and rng.random() < copy_probability:
            series.append(series[-1])
        else:
            series.append(bisect_right(cdf, rng.random()))
    return series


def shuffled(rng: random.Random, values: list) -> list:
    """Fisher-Yates shuffle driven by rng.random() only."""
    out = list(values)
    for i in range(len(out) - 1, 0, -1):
        j = min(int(rng.random() * (i + 1)), i)
        out[i], out[j] = out[j], out[i]
    return out


def lag1_parts(values: list[int]) -> tuple[int, int]:
    """Numerator and denominator of the lag-1 autocorrelation, as exact integers (each scaled by n squared)."""
    n, total = len(values), sum(values)
    centred = [n * value - total for value in values]
    return sum(a * b for a, b in zip(centred, centred[1:])), sum(c * c for c in centred)


def double_ranks(values: list[int]) -> list[int]:
    """Twice the average rank of each value (an integer), ties sharing their mean rank."""
    order = sorted(range(len(values)), key=lambda i: values[i])
    ranks, i = [0] * len(values), 0
    while i < len(order):
        j = i
        while j + 1 < len(order) and values[order[j + 1]] == values[order[i]]:
            j += 1
        for k in range(i, j + 1):
            ranks[order[k]] = i + j + 2  # twice the mean of the ranks i + 1 .. j + 1
        i = j + 1
    return ranks


def median(values: list) -> float:
    ordered = sorted(values)
    half = len(ordered) // 2
    return ordered[half] if len(ordered) % 2 else (ordered[half - 1] + ordered[half]) / 2


def observed_section(observed: dict, counts: list[int], t: dict) -> dict:
    declared, days = observed["counts"], list(observed["daily_counts"])
    first = date.fromisoformat(days[0])
    check("calendar: the snapshot's days are consecutive calendar days from the first to the last",
          days == [(first + timedelta(days=i)).isoformat() for i in range(len(days))]
          and (days[0], days[-1]) == (declared["first_day"], declared["last_day"]))
    check("recount: days, events, active and empty days equal the counts made by extract.py",
          (t["n"], t["total"], t["n"] - t["freq"].get(0, 0), t["freq"].get(0, 0))
          == (declared["calendar_days"], declared["events"], declared["active_days"], declared["days_without_event"]))
    check("accounting: the frequency table accounts for every day and every event",
          sum(t["freq"].values()) == t["n"] and sum(x * days_ for x, days_ in t["freq"].items()) == t["total"])
    check("accounting: events by type sum to the events", sum(declared["by_type"].values()) == t["total"])
    n, total = t["n"], t["total"]
    spread = n * t["sum_sq"] - total * total  # n squared times the variance with divisor n
    return {
        "kind": "observed (the snapshot written by extract.py) and counts computed from it",
        "source": {"repository": observed["source"]["repository"], "commit": observed["source"]["commit"],
                   "trigger_folder": {key: observed["source"]["trigger_folder"][key]
                                      for key in ("path", "files", "git_tree", "manifest_sha256")}},
        "first_day": days[0], "last_day": days[-1], "calendar_days": n, "events": total,
        "active_days": declared["active_days"], "days_without_event": declared["days_without_event"],
        "sum_of_squared_counts": t["sum_sq"],
        "mean_per_calendar_day": rnd(total / n, "parameter"),
        "median_day": median(counts), "largest_day": t["max"],
        "variance_divisor_n": rnd(spread / (n * n), "parameter"),
        "variance_divisor_n_minus_1": rnd(spread / (n * (n - 1)), "parameter"),
        "variance_exceeds_the_mean": spread > n * total,
        "days_by_count": {str(x): days_ for x, days_ in t["freq"].items()},
    }


def criteria_table(logliks: dict, days: int) -> dict:
    """Rounded log-likelihood, AIC and BIC per model, and each criterion's difference from its lowest value."""
    ln_days = ln(float(days))
    rows = {}
    for key in MODEL_KEYS:
        loglik = rnd(logliks[key], "log_likelihood")
        rows[key] = {"free_parameters": PARAMETERS[key], "log_likelihood": loglik,
                     "aic": rnd(2 * PARAMETERS[key] - 2 * loglik, "criterion"),
                     "bic": rnd(PARAMETERS[key] * ln_days - 2 * loglik, "criterion")}
    selected = {}
    for name, penalty in (("aic", 2.0), ("bic", ln_days)):
        best = min(rows[key][name] for key in MODEL_KEYS)
        for key in MODEL_KEYS:
            rows[key][f"{name}_minus_lowest"] = rnd(rows[key][name] - best, "criterion")
        lowest = [key for key in MODEL_KEYS if rows[key][name] == best]
        selected[name] = lowest[0] if len(lowest) == 1 else "tie"
        check("criteria: the rounded table selects the same model as the unrounded log-likelihoods",
              selected[name] == choose(logliks, penalty))
    return {"days": days, "ln_days": rnd(ln_days, "parameter"),
            "formulas": {"aic": "2 k - 2 log L", "bic": "k ln(days) - 2 log L", "k": "free parameters",
                         "computed_from": "the log-likelihood rounded to 3 decimals"},
            "models": rows, "lowest_aic": selected["aic"], "lowest_bic": selected["bic"]}


def fits_section(t: dict, fits: dict, models: list[dict]) -> dict:
    check("candidates: scenarios.json lists the three models with the parameter counts used here",
          {model["key"]: model["free_parameters"] for model in models} == PARAMETERS)
    nb = fits["negative_binomial"]
    check("observed fit: the negative binomial search ended inside its bracket", nb["status"] == "interior")
    table = criteria_table({key: fits[key]["loglik"] for key in MODEL_KEYS}, t["n"])
    rows = table["models"]
    check("ordering: the negative binomial maximum is at least the geometric and the Poisson maxima, which it contains",
          nb["loglik"] >= fits["geometric"]["loglik"] and nb["loglik"] >= fits["poisson"]["loglik"])
    estimates = {
        "poisson": {"lambda": rnd(fits["poisson"]["lambda"], "parameter")},
        "geometric": {"q": rnd(fits["geometric"]["q"], "parameter"), "q_exact": f"{t['total']}/{t['n'] + t['total']}"},
        "negative_binomial": {"r": rnd(nb["r"], "parameter"), "mu": rnd(nb["mu"], "parameter"),
                              "r_over_r_plus_mu": rnd(nb["r"] / (nb["r"] + nb["mu"]), "parameter"),
                              "variance_implied_mu_plus_mu_squared_over_r":
                                  rnd(nb["mu"] + nb["mu"] * nb["mu"] / nb["r"], "parameter")},
    }
    for model in models:
        rows[model["key"]] = {"name": model["name"], "probability": model["probability"],
                              "log_likelihood_formula": model["log_likelihood"], "maximum": model["maximum"],
                              "estimates": estimates[model["key"]]} | rows[model["key"]]
    gain = {"negative_binomial_over_geometric": rnd(2 * (rows["negative_binomial"]["log_likelihood"]
                                                         - rows["geometric"]["log_likelihood"]), "criterion"),
            "geometric_over_poisson": rnd(2 * (rows["geometric"]["log_likelihood"]
                                               - rows["poisson"]["log_likelihood"]), "criterion"),
            "negative_binomial_over_poisson": rnd(2 * (rows["negative_binomial"]["log_likelihood"]
                                                       - rows["poisson"]["log_likelihood"]), "criterion")}
    return {"kind": "computed from the observed daily counts", **table,
            "log_likelihood_gap_between_best_and_poisson":
                rnd(rows["negative_binomial"]["log_likelihood"] - rows["poisson"]["log_likelihood"], "log_likelihood"),
            "twice_the_log_likelihood_gain": gain}


def closed_form_checks(t: dict, cfg: dict, fits: dict) -> dict:
    """Known answers: a numeric maximiser must land on the two closed forms from every starting interval."""
    golden, out = cfg["golden_section"], {}
    cases = (("poisson", "lambda", lambda value: loglik_poisson(t, value)),
             ("geometric", "q", lambda value: loglik_geometric(t, value)))
    for key, name, objective in cases:
        exact, runs = fits[key][name], []
        for lo, hi in golden[f"{key}_{name}_intervals"]:
            found, steps = golden_max(objective, lo, hi, golden["interval_tolerance"])
            check(f"known answer: the numeric maximiser returns the closed-form {name} within "
                  f"{cfg['agreement_tolerance']} from every starting interval", abs(found - exact) < cfg["agreement_tolerance"],
                  f"[{lo}, {hi}] -> {found} against {exact}")
            runs.append({"start": [lo, hi], "steps": steps, "found": rnd(found, "parameter")})
        out[key] = {"parameter": name, "closed_form": rnd(exact, "parameter"), "numeric_maximiser": runs,
                    "all_within_agreement_tolerance": True}
    return out


def score_grid(t: dict, grid: dict) -> dict:
    """Sign of the score on a geometric grid of r: one change of sign means one maximum on the grid."""
    factor = math.sqrt(math.sqrt(math.sqrt(2.0)))  # 2^(1/8), by three correctly rounded square roots
    r, points, changes, bracket, previous = grid["from"], 0, 0, None, None
    while r <= grid["to"]:
        positive = score(t, r) > 0.0
        if previous is not None and positive != previous[1]:
            changes += 1
            bracket = [rnd(previous[0], "parameter"), rnd(r, "parameter")]
        previous = (r, positive)
        points += 1
        r *= factor
    check("one maximum: the score changes sign exactly once on the grid, from positive to negative",
          changes == 1 and previous[1] is False)
    return {"from": grid["from"], "to": grid["to"], "step_factor": "2^(1/8)", "points": points,
            "sign_changes_of_the_score": changes, "sign_change_between": bracket}


def negbin_search_checks(t: dict, cfg: dict, fit: dict) -> dict:
    """The fitted r must not depend on the starting bracket, on the method, or on holding mu at the mean."""
    bisection, golden, tolerance = cfg["score_bisection"], cfg["golden_section"], cfg["agreement_tolerance"]
    mean, r_hat = t["total"] / t["n"], fit["r"]
    by_bracket = []
    for lo, hi in [[bisection["lower"], bisection["upper"]]] + bisection["other_starting_brackets"]:
        found, steps, status = negbin_root(t, lo, hi, bisection["relative_tolerance"])
        check(f"starting point: bisection of the score returns the same r within {tolerance} from every bracket",
              status == "interior" and abs(found - r_hat) < tolerance, f"[{lo}, {hi}] -> {found}")
        by_bracket.append({"start": [lo, hi], "bisections": steps, "r": rnd(found, "parameter")})
    by_interval = []
    for lo, hi in golden["negative_binomial_r_intervals"]:
        found, steps = golden_max(lambda r: loglik_negbin(t, r, mean), lo, hi, golden["interval_tolerance"])
        check(f"second method: maximising the log-likelihood directly returns the same r within {tolerance}",
              abs(found - r_hat) < tolerance, f"[{lo}, {hi}] -> {found}")
        by_interval.append({"start": [lo, hi], "steps": steps, "r": rnd(found, "parameter")})
    lo, hi = golden["negative_binomial_mu_interval"]
    mu_found, _ = golden_max(lambda mu: loglik_negbin(t, r_hat, mu), lo, hi, golden["interval_tolerance"])
    check(f"second parameter: at the fitted r the log-likelihood peaks at mu = mean within {tolerance}",
          abs(mu_found - mean) < tolerance, f"{mu_found} against {mean}")
    return {"method": "bisection of the score d(log L)/dr on the geometric mean of the bracket, mu held at the mean",
            "relative_tolerance_on_r": bisection["relative_tolerance"], "agreement_tolerance": tolerance,
            "r": rnd(r_hat, "parameter"), "bisection_from_each_bracket": by_bracket,
            "golden_section_on_the_log_likelihood": {"interval_tolerance": golden["interval_tolerance"],
                                                     "from_each_interval": by_interval},
            "mu_maximising_the_log_likelihood_at_that_r": {"start": [lo, hi], "found": rnd(mu_found, "parameter"),
                                                           "sample_mean": rnd(mean, "parameter")},
            "score_grid": score_grid(t, cfg["score_grid"])}


def limit_and_known_cases(t: dict, cfg: dict, fits: dict) -> dict:
    """The negative binomial at r = 1 and at a very large r, a case worked by hand, and a sample with no finite r."""
    limits, hand, flat = cfg["limit_checks"], cfg["hand_computed_case"], cfg["not_overdispersed_case"]
    mean, big = t["total"] / t["n"], limits["poisson_at_r"]
    at_one = loglik_negbin(t, limits["geometric_at_r"], mean)
    check(f"limit: at r = 1 the negative binomial log-likelihood equals the geometric one within {limits['geometric_tolerance']}",
          abs(at_one - fits["geometric"]["loglik"]) < limits["geometric_tolerance"])
    gap = loglik_negbin(t, big, mean) - fits["poisson"]["loglik"]
    predicted = (t["n"] * t["sum_sq"] - t["total"] ** 2 - t["n"] * t["total"]) / (2 * t["n"] * big)
    check(f"limit: at r = {big:g} the negative binomial log-likelihood exceeds the Poisson one by n (variance - mean) / (2 r) "
          f"within {limits['poisson_relative_tolerance']:.1%}", abs(gap / predicted - 1.0) < limits["poisson_relative_tolerance"],
          f"{gap} against {predicted}")
    small = fit_all(tally(hand["counts"]), cfg["score_bisection"])
    by_hand = {"poisson": rnd(small["poisson"]["loglik"], "parameter"),
               "geometric": rnd(small["geometric"]["loglik"], "parameter"),
               "negative_binomial_at_r_2": rnd(loglik_negbin(tally(hand["counts"]), hand["negative_binomial_r"],
                                                             sum(hand["counts"]) / len(hand["counts"])), "parameter")}
    check("hand-computed case: three days with 0, 1 and 3 events give the three log-likelihoods worked by hand",
          by_hand == hand["expected_log_likelihoods"], f"got {by_hand}")
    level = fit_all(tally(flat["counts"]), cfg["score_bisection"])["negative_binomial"]
    check("known answer: a sample whose variance does not exceed its mean is fitted at the Poisson limit",
          level["status"] == "poisson_limit" and level["r"] is None)
    return {"at_r_1": {"equals_the_geometric_log_likelihood": True, "tolerance": limits["geometric_tolerance"]},
            "at_large_r": {"r": big, "formula": limits["poisson_gap_formula"],
                           "n_times_variance_minus_mean_over_2": rnd(predicted * big, "expected_days"),
                           "gap_matches_the_formula": True, "relative_tolerance": limits["poisson_relative_tolerance"]},
            "hand_computed_case": {"counts": hand["counts"], "working": hand["working"], "log_likelihoods": by_hand,
                                   "expected_by_hand": hand["expected_log_likelihoods"]},
            "not_overdispersed_case": {"counts": flat["counts"], "negative_binomial_fit": level["status"]}}


def optimiser_section(t: dict, cfg: dict, fits: dict) -> dict:
    return {"kind": "computed: checks of the search against known answers and against its own starting point",
            "closed_forms_against_a_numeric_maximiser": closed_form_checks(t, cfg, fits),
            "negative_binomial_search": negbin_search_checks(t, cfg, fits["negative_binomial"]),
            "limits_and_known_cases": limit_and_known_cases(t, cfg, fits)}


def adequacy_section(t: dict, fits: dict, bins: list[dict], tail: float) -> dict:
    """Days each fitted model expects in each band of daily counts, against the days observed."""
    tables = {key: pmf_table(key, fits[key], tail, t["max"] + 1) for key in MODEL_KEYS}
    mean = t["total"] / t["n"]
    for key, table in tables.items():
        check("probability tables: each fitted distribution sums to 1 and has the sample mean, within 1e-9",
              abs(add_up(table) - 1.0) < 1e-9 and abs(add_up(k * p for k, p in enumerate(table)) - mean) < 1e-9, key)
    rows, covered = [], 0
    for band in bins:
        lo, hi = band["from"], band["to"]
        observed = sum(days for x, days in t["freq"].items() if x >= lo and (hi is None or x <= hi))
        covered += observed
        expected = {}
        for key, table in tables.items():
            share = add_up(table[lo:]) if hi is None else add_up(table[lo:hi + 1])
            expected[key] = rnd(t["n"] * share, "expected_days")
        rows.append({"events_in_the_day": band["label"], "days_observed": observed, "days_expected": expected})
    check("accounting: the bands cover every observed day once", covered == t["n"])
    for key in MODEL_KEYS:
        check("accounting: each model's expected days sum to the calendar days within 0.02",
              abs(add_up(row["days_expected"][key] for row in rows) - t["n"]) <= 0.02, key)
    top = t["max"]
    return {"kind": "computed: an absolute check, where the criteria only rank",
            "definition": "days expected = calendar days x the probability the fitted model gives to the band",
            "bands": rows,
            "largest_observed_day": top,
            "days_expected_at_least_that_busy": {key: sig3(t["n"] * add_up(tables[key][top:])) for key in MODEL_KEYS},
            "probabilities_of_0_and_1": {key: {"p0": rnd(tables[key][0], "parameter"), "p1": rnd(tables[key][1], "parameter")}
                                         for key in MODEL_KEYS}}


def recovery_cell(truth: str, cdf: list[float], days: int, replicates: int, seed: int, search: dict, observed_gain: float,
                  copy_probability: float = 0.0, with_gain: bool = True) -> dict:
    """Draw seeded samples from one generator, refit the three candidates to each, and count what each criterion picks."""
    rng, ln_days = random.Random(seed), ln(float(days))
    picks = {name: dict.fromkeys(MODEL_KEYS + ("tie",), 0) for name in ("aic", "bic")}
    status = {"interior": 0, "poisson_limit": 0, "upper_bound": 0}
    gains, lags = [], []
    for _ in range(replicates):
        series = draw_series(rng, cdf, days, copy_probability)
        fits = fit_all(tally(series), search["score_bisection"])
        logliks = {key: fits[key]["loglik"] for key in MODEL_KEYS}
        picks["aic"][choose(logliks, 2.0)] += 1
        picks["bic"][choose(logliks, ln_days)] += 1
        status[fits["negative_binomial"]["status"]] += 1
        gains.append(2.0 * (logliks["negative_binomial"] - logliks["geometric"]))
        numerator, denominator = lag1_parts(series)
        if denominator:
            lags.append(numerator / denominator)
    for name in picks:
        check("accounting: the picks of a criterion, ties included, sum to the samples", sum(picks[name].values()) == replicates)
    check("accounting: the three outcomes of the negative binomial search sum to the samples", sum(status.values()) == replicates)
    cell = {"days": days, "samples": replicates, "seed": seed}
    for name in ("aic", "bic"):
        cell[name] = picks[name] | {"true_generator_selected": picks[name][truth],
                                    "share": rnd(picks[name][truth] / replicates, "share")}
    cell["negative_binomial_search"] = status
    if with_gain:
        cell["twice_the_gain_of_negative_binomial_over_geometric"] = {
            "median": rnd(median(gains), "criterion"), "largest": rnd(max(gains), "criterion"),
            "samples_at_or_above_the_observed_gain": sum(gain >= observed_gain for gain in gains)}
    cell["median_lag1_autocorrelation_of_the_samples"] = rnd(median(lags), "autocorrelation")
    return cell


def nested_expectation(cell: dict, days: int) -> dict:
    """What large-sample theory gives for the share of geometric samples in which a criterion picks the larger model."""
    out = {"reason": "the geometric is the negative binomial at r = 1; twice the gain in log-likelihood from freeing r then "
                     "behaves as a chi-square with 1 degree of freedom (Wilks 1938), and a criterion picks the larger model "
                     "when that gain exceeds its extra penalty (2 for AIC, ln(days) for BIC)",
           "days": days, "samples": cell["samples"]}
    for name, penalty in (("aic", 2.0), ("bic", ln(float(days)))):
        expected = rnd(chi_square_tail(penalty), "share")
        seeded = rnd(cell[name]["negative_binomial"] / cell["samples"], "share")
        error = rnd(math.sqrt(expected * (1.0 - expected) / cell["samples"]), "share")
        out[f"{name}_picks_negative_binomial"] = {
            "extra_penalty": rnd(penalty, "criterion"), "expected_share": expected, "seeded_share": seeded,
            "standard_error_of_a_share_of_that_many_samples": error,
            "within_two_standard_errors": abs(seeded - expected) <= 2 * error}
    return out


def recovery_section(fits: dict, cfg: dict, search: dict, observed_gain: float) -> dict:
    by_generator = {}
    for key in MODEL_KEYS:
        cdf = cdf_table(pmf_table(key, fits[key], cfg["pmf_tail"]))
        by_generator[key] = [recovery_cell(key, cdf, days, cfg["replicates"], cfg["seeds"][key] * 1000 + days, search,
                                           observed_gain, with_gain=key != "poisson") for days in cfg["days"]]
    full = cfg["days"][-1]
    return {"kind": "synthetic: seeded samples of independent days drawn from each fitted model",
            "note": cfg["note"], "samples_per_cell": cfg["replicates"], "days": cfg["days"],
            "observed_twice_the_gain_of_negative_binomial_over_geometric": observed_gain,
            "by_generator": by_generator,
            "large_sample_expectation_when_the_geometric_is_true": nested_expectation(by_generator["geometric"][-1], full)}


def permutation_test(rng: random.Random, counts: list[int], shuffles: int) -> dict:
    """Lag-1 autocorrelation of the counts and of their ranks, against seeded shuffles of the same days."""
    ranks = double_ranks(counts)
    raw, rank = lag1_parts(counts), lag1_parts(ranks)
    index, raw_null, rank_null = list(range(len(counts))), [], []
    for _ in range(shuffles):
        order = shuffled(rng, index)
        raw_null.append(lag1_parts([counts[i] for i in order])[0])
        rank_null.append(lag1_parts([ranks[i] for i in order])[0])
    raw_null.sort()
    rank_null.sort()

    def summary(observed: tuple[int, int], null: list[int]) -> dict:
        numerator, denominator = observed
        return {"lag1_autocorrelation": rnd(numerator / denominator, "autocorrelation"),
                "shuffles_at_or_above_it": sum(value >= numerator for value in null),
                "shuffled_95th_percentile": rnd(null[math.ceil(0.95 * shuffles) - 1] / denominator, "autocorrelation"),
                "shuffled_99th_percentile": rnd(null[math.ceil(0.99 * shuffles) - 1] / denominator, "autocorrelation"),
                "shuffled_largest": rnd(null[-1] / denominator, "autocorrelation")}
    return {"counts": summary(raw, raw_null), "ranks": summary(rank, rank_null), "_raw_null": raw_null}


def dependence_section(counts: list[int], t: dict, fits: dict, cfg: dict, recovery: dict, search: dict,
                       observed_gain: float) -> dict:
    test = permutation_test(random.Random(cfg["shuffle_seed"]), counts, cfg["shuffles"])
    control_rng = random.Random(cfg["control_seed"])
    reordered = shuffled(control_rng, counts)
    again = fit_all(tally(reordered), search["score_bisection"])
    check("order-blind: the three log-likelihoods of the shuffled days equal those of the days in calendar order",
          reordered != counts and all(again[key]["loglik"] == fits[key]["loglik"] for key in MODEL_KEYS))
    numerator, denominator = lag1_parts(reordered)
    ascending = lag1_parts(sorted(counts))
    controls = {
        "one_shuffled_order_as_if_observed": {
            "lag1_autocorrelation": rnd(numerator / denominator, "autocorrelation"),
            "shuffles_at_or_above_it": sum(value >= numerator for value in test["_raw_null"])},
        "days_sorted_by_count_as_if_observed": {
            "lag1_autocorrelation": rnd(ascending[0] / ascending[1], "autocorrelation"),
            "shuffles_at_or_above_it": sum(value >= ascending[0] for value in test["_raw_null"])}}
    sticky = cfg["sticky_geometric"]
    copy = round(lag1_parts(counts)[0] / lag1_parts(counts)[1], 2)
    cdf = cdf_table(pmf_table("geometric", fits["geometric"], recovery["pmf_tail"]))
    cell = recovery_cell("geometric", cdf, sticky["days"], sticky["replicates"], sticky["seed"], search, observed_gain, copy)
    return {"kind": "computed from the observed order of the days (lag-1 autocorrelation, shuffles) and synthetic "
                    "(the sticky process)",
            "definition": "lag-1 autocorrelation = sum over t of (x_t - mean)(x_t+1 - mean) / sum over t of (x_t - mean)^2; "
                          "the rank version replaces each count by its rank, ties sharing their mean rank",
            "shuffles": cfg["shuffles"], "shuffle_seed": cfg["shuffle_seed"],
            "observed_days": {"counts": test["counts"], "ranks": test["ranks"]},
            "candidates_are_order_blind": {"shuffled_days_give_the_same_three_log_likelihoods": True,
                                           "reason": "each log-likelihood is a sum over days, in any order"},
            "controls": controls,
            "sticky_geometric": {"note": sticky["note"], "copy_probability_rule": sticky["copy_probability_rule"],
                                 "copy_probability": copy} | cell}


def band_label(value: float, scale: dict) -> str:
    for band in scale["bands"]:
        if value >= band["from"] and (band["to"] is None or value <= band["to"]):
            return band["label"]
    return scale["between_bands"]


def scales_section(scales: dict, fits: dict) -> dict:
    """What the two cited rules of thumb say about the observed differences. Neither is a probability of truth."""
    rows = fits["models"]
    readings = {key: {"aic_minus_lowest": rows[key]["aic_minus_lowest"],
                      "aic_reading": band_label(rows[key]["aic_minus_lowest"], scales["aic_difference"]),
                      "bic_minus_lowest": rows[key]["bic_minus_lowest"],
                      "bic_reading": band_label(rows[key]["bic_minus_lowest"], scales["twice_log_bayes_factor"])
                                     + " evidence against it"}
                for key in MODEL_KEYS if key != fits["lowest_aic"]}
    return {"kind": "cited scales applied to the computed differences; the scales are rules of thumb of their authors",
            "note": scales["note"],
            "aic_difference": scales["aic_difference"], "twice_log_bayes_factor": scales["twice_log_bayes_factor"],
            "observed_differences_from_the_lowest": readings}


def hypothesis_section(cfg: dict, fits: dict, recovery: dict, dependence: dict) -> dict:
    """The thresholds were written before the seeded check ran; this only reports which of them hold."""
    rows, full = fits["models"], {key: cells[-1] for key, cells in recovery["by_generator"].items()}
    gap = fits["log_likelihood_gap_between_best_and_poisson"]
    shares = {f"{key}_{name}": full[key][name]["share"] for key in MODEL_KEYS for name in ("aic", "bic")}
    nested = recovery["large_sample_expectation_when_the_geometric_is_true"]
    aic, bic = nested["aic_picks_negative_binomial"], nested["bic_picks_negative_binomial"]
    lag = dependence["observed_days"]["counts"]
    parts = {
        "ranking_is_negative_binomial_geometric_poisson_for_both_criteria":
            all(rows["negative_binomial"][c] < rows["geometric"][c] < rows["poisson"][c] for c in ("aic", "bic")),
        "poisson_trails_the_best_model_by_more_than_1000_log_likelihood_units": {
            "gap": gap, "holds": gap > cfg["poisson_trails_the_best_model_by_more_than_log_likelihood_units"]},
        "negative_binomial_beats_geometric_by_more_than_10": {
            "aic_points": rows["geometric"]["aic_minus_lowest"], "bic_points": rows["geometric"]["bic_minus_lowest"],
            "holds": rows["geometric"]["aic_minus_lowest"] > cfg["negative_binomial_beats_geometric_by_more_than_aic_points"]
                     and rows["geometric"]["bic_minus_lowest"] > cfg["negative_binomial_beats_geometric_by_more_than_bic_points"]},
        "each_criterion_selects_the_true_generator_in_at_least_80_percent_of_samples": {
            "shares_at_the_observed_length": shares,
            "holds": min(shares.values()) >= cfg["true_generator_selected_share_at_least"]},
        "aic_picks_negative_binomial_about_16_percent_when_geometric_is_true": aic | {
            "holds": abs(aic["seeded_share"] - aic["expected_share"])
                     <= cfg["aic_picks_negative_binomial_when_geometric_is_true"]["within"]},
        "bic_picks_negative_binomial_about_3_percent_when_geometric_is_true": bic | {
            "holds": abs(bic["seeded_share"] - bic["expected_share"])
                     <= cfg["bic_picks_negative_binomial_when_geometric_is_true"]["within"]},
        "lag1_autocorrelation_above_0_3_and_outside_the_shuffles": {
            "lag1_autocorrelation": lag["lag1_autocorrelation"], "shuffles_at_or_above_it": lag["shuffles_at_or_above_it"],
            "holds": lag["lag1_autocorrelation"] > cfg["lag1_autocorrelation_above"]
                     and lag["shuffles_at_or_above_it"] <= cfg["share_of_shuffles_reaching_the_observed_lag1_at_most"]
                     * dependence["shuffles"]},
    }
    holds = [value if isinstance(value, bool) else value["holds"] for value in parts.values()]
    return {"kind": "the research cycle's hypothesis, part by part", "note": cfg["note"], "parts": parts,
            "parts_that_hold": sum(holds), "parts_in_all": len(holds), "every_part_holds": all(holds)}


def refit(counts: list, search: dict) -> dict:
    """Fit the three candidates to a modified series and return the row fields shared by the sensitivity checks."""
    t = tally(counts)
    raw = fit_all(t, search["score_bisection"])
    check("sensitivity: the negative binomial search ended inside its bracket",
          raw["negative_binomial"]["status"] == "interior")
    table = criteria_table({key: raw[key]["loglik"] for key in MODEL_KEYS}, t["n"])
    models = table["models"]
    return {
        "days": t["n"], "events": t["total"], "ln_days": table["ln_days"],
        "negative_binomial_r": rnd(raw["negative_binomial"]["r"], "parameter"),
        "log_likelihood": {key: models[key]["log_likelihood"] for key in MODEL_KEYS},
        "aic": {key: models[key]["aic"] for key in MODEL_KEYS},
        "bic": {key: models[key]["bic"] for key in MODEL_KEYS},
        "geometric_minus_negative_binomial": {
            name: rnd(models["geometric"][name] - models["negative_binomial"][name], "criterion") for name in ("aic", "bic")},
        "poisson_minus_negative_binomial": {
            name: rnd(models["poisson"][name] - models["negative_binomial"][name], "criterion") for name in ("aic", "bic")},
        "lowest_aic": table["lowest_aic"], "lowest_bic": table["lowest_bic"]}


def deleted_triggers_row(observed: dict, cfg: dict, search: dict) -> dict:
    """Add back the trigger files known to have been deleted without being archived (a borrowed count)."""
    extra = cfg["extra_events_by_day"]
    check("sensitivity: every day with deleted triggers is a day of the snapshot",
          all(day in observed["daily_counts"] for day in extra))
    counts = [count + extra.get(day, 0) for day, count in observed["daily_counts"].items()]
    row = {"kind": "computed from the observed daily counts plus a borrowed count", "note": cfg["note"],
           "extra_events_by_day": extra, "events_added": sum(extra.values())}
    row.update(refit(counts, search))
    return row


def sensitivity_section(observed: dict, cfg: dict, search: dict, fits: dict) -> dict:
    """Refit after leaving out the busiest days: how much of the ranking do a few days carry?"""
    by_day = sorted(observed["daily_counts"].items(), key=lambda item: (-item[1], item[0]))
    rows = []
    for left_out in cfg["busiest_days_left_out"]:
        check("sensitivity: every day left out is strictly busier than every day kept",
              left_out == 0 or by_day[left_out - 1][1] > by_day[left_out][1])
        row = {"busiest_days_left_out": left_out,
               "days_left_out": sorted(day for day, _ in by_day[:left_out]),
               "smallest_count_left_out": by_day[left_out - 1][1] if left_out else None}
        row.update(refit([count for _, count in by_day[left_out:]], search))
        rows.append(row)
    check("sensitivity: with no day left out the row repeats the main fit",
          rows[0]["busiest_days_left_out"] == 0
          and rows[0]["log_likelihood"] == {key: fits["models"][key]["log_likelihood"] for key in MODEL_KEYS})
    return {"kind": "computed from the observed daily counts, refitted without their busiest days",
            "note": cfg["note"], "rows": rows,
            "with_deleted_triggers_added_back": deleted_triggers_row(observed, cfg["deleted_triggers"], search)}


def exercise_3(spec: dict, recovery: dict, scale: dict) -> dict:
    """A short log on which BIC prefers the geometric: how often does that happen under each generator?"""
    index, samples = recovery["days"].index(spec["days"]), recovery["samples_per_cell"]
    picks = {key: recovery["by_generator"][key][index]["bic"]["geometric"] for key in ("geometric", "negative_binomial")}
    shares = {key: rnd(count / samples, "share") for key, count in picks.items()}
    return {"note": spec["note"], "days": spec["days"], "samples": samples,
            "bic_difference_in_favour_of_the_geometric": spec["bic_difference_in_favour_of_the_geometric"],
            "reading_on_the_cited_scale": band_label(spec["bic_difference_in_favour_of_the_geometric"], scale),
            "bic_picks_geometric_when_geometric_is_true": {"samples": picks["geometric"], "share": shares["geometric"]},
            "bic_picks_geometric_when_negative_binomial_is_true": {"samples": picks["negative_binomial"],
                                                                   "share": shares["negative_binomial"]},
            "ratio_of_the_two_shares": rnd(shares["geometric"] / shares["negative_binomial"], "ratio")}


def worked_examples(cfg: dict, t: dict, fits_raw: dict, fits: dict, adequacy: dict, recovery: dict, sensitivity: dict,
                    scales: dict) -> dict:
    """Intermediate values of the lesson's five exercises, so that each answer can be checked against this file."""
    n, total = t["n"], t["total"]
    q = fits_raw["geometric"]["q"]
    ln_one_minus_q, ln_q = rnd(ln(1.0 - q), "parameter"), rnd(ln(q), "parameter")
    by_hand = rnd(n * ln_one_minus_q + total * ln_q, "log_likelihood")
    check("worked example: the geometric log-likelihood rebuilt from two rounded logarithms equals the fitted one",
          by_hand == fits["models"]["geometric"]["log_likelihood"])
    rows = fits["models"]
    nb = adequacy["probabilities_of_0_and_1"]["negative_binomial"]
    band = {row["events_in_the_day"]: row for row in adequacy["bands"]}
    left_out = cfg["exercise_4"]["busiest_days_left_out"]
    row = next(row for row in sensitivity["rows"] if row["busiest_days_left_out"] == left_out)
    return {
        "exercise_1": {"days": n, "events": total, "lambda": rows["poisson"]["estimates"]["lambda"],
                       "q_exact": f"{total}/{n + total}", "q": rows["geometric"]["estimates"]["q"],
                       "ln_one_minus_q": ln_one_minus_q, "ln_q": ln_q,
                       "days_times_ln_one_minus_q": rnd(n * ln_one_minus_q, "log_likelihood"),
                       "events_times_ln_q": rnd(total * ln_q, "log_likelihood"),
                       "geometric_log_likelihood_by_hand": by_hand,
                       "geometric_log_likelihood_of_the_fit": rows["geometric"]["log_likelihood"]},
        "exercise_2": {"ln_days": fits["ln_days"],
                       "models": {key: {name: rows[key][name] for name in
                                        ("free_parameters", "log_likelihood", "aic", "bic", "aic_minus_lowest", "bic_minus_lowest")}
                                  for key in MODEL_KEYS}},
        "exercise_3": exercise_3(cfg["exercise_3"], recovery, scales["twice_log_bayes_factor"]),
        "exercise_4": {key: row[key] for key in ("busiest_days_left_out", "days", "ln_days", "log_likelihood", "aic", "bic",
                                                 "geometric_minus_negative_binomial", "lowest_aic", "lowest_bic")},
        "exercise_5": {"days": n, "p0": nb["p0"], "p1": nb["p1"],
                       "empty_days_expected": band["0"]["days_expected"]["negative_binomial"],
                       "empty_days_observed": band["0"]["days_observed"],
                       "one_event_days_expected": band["1"]["days_expected"]["negative_binomial"],
                       "one_event_days_observed": band["1"]["days_observed"]},
    }


def transfer_task(task: dict, search: dict, scales: dict) -> dict:
    """Expected answers of the learner's transfer task, from inputs that differ from the lesson's."""
    counts = task["counts"]
    t = tally(counts)
    raw = fit_all(t, search["score_bisection"])
    table = criteria_table({key: raw[key]["loglik"] for key in MODEL_KEYS}, t["n"])
    rows = table["models"]
    numerator, denominator = lag1_parts(counts)
    n, mean = t["n"], t["total"] / t["n"]
    by_hand = task["worked_by_hand"]
    check("transfer task: the two sums behind the lag-1 autocorrelation equal the sums worked by hand",
          (denominator, numerator) == (n * n * by_hand["sum_of_squared_deviations"],
                                       n * n * by_hand["sum_of_products_of_neighbouring_deviations"]))
    nb = raw["negative_binomial"]
    check("transfer task: the negative binomial search ended inside its bracket", nb["status"] == "interior")
    runner_up = {name: min(rows[key][f"{name}_minus_lowest"] for key in MODEL_KEYS if rows[key][f"{name}_minus_lowest"] > 0)
                 for name in ("aic", "bic")}
    return {
        "note": task["note"], "unit": task["unit"], "counts": counts,
        "q1_closed_forms": {"days": n, "events": t["total"], "mean": rnd(mean, "parameter"),
                            "poisson_lambda": rnd(raw["poisson"]["lambda"], "parameter"),
                            "geometric_q": rnd(raw["geometric"]["q"], "parameter"),
                            "geometric_q_exact": f"{t['total']}/{n + t['total']}",
                            "sum_of_ln_factorials": rnd(t["ln_factorials"], "parameter"),
                            "poisson_log_likelihood": rows["poisson"]["log_likelihood"],
                            "geometric_log_likelihood": rows["geometric"]["log_likelihood"]},
        "q2_given_negative_binomial": {"r": rnd(nb["r"], "parameter"), "mu": rnd(nb["mu"], "parameter"),
                                       "log_likelihood": rows["negative_binomial"]["log_likelihood"]},
        "q3_criteria": {"ln_days": table["ln_days"],
                        "models": {key: {name: rows[key][name] for name in ("free_parameters", "aic", "bic", "aic_minus_lowest",
                                                                             "bic_minus_lowest")} for key in MODEL_KEYS},
                        "lowest_aic": table["lowest_aic"], "lowest_bic": table["lowest_bic"],
                        "criteria_agree": table["lowest_aic"] == table["lowest_bic"],
                        "runner_up_aic_difference": runner_up["aic"],
                        "runner_up_aic_reading": band_label(runner_up["aic"], scales["aic_difference"]),
                        "runner_up_bic_difference": runner_up["bic"],
                        "runner_up_bic_reading": band_label(runner_up["bic"], scales["twice_log_bayes_factor"])},
        "q4_order": {"sum_of_squared_deviations": rnd(denominator / (n * n), "parameter"),
                     "sum_of_products_of_neighbouring_deviations": rnd(numerator / (n * n), "parameter"),
                     "lag1_autocorrelation": rnd(numerator / denominator, "autocorrelation"),
                     "candidates_use_the_order": False},
    }


def negative_controls(search: dict, dependence: dict) -> dict:
    """Results that could pass on nothing, each run once on an input where the answer is known."""
    empty = fit_all(tally([0] * 10), search["score_bisection"])
    logliks = {key: empty[key]["loglik"] for key in MODEL_KEYS}
    picks = {"aic": choose(logliks, 2.0), "bic": choose(logliks, ln(10.0))}
    check("negative control: ten empty days give a tie between the two one-parameter models, and the tie is reported",
          picks == {"aic": "tie", "bic": "tie"})
    controls = dependence["controls"]
    shuffles = dependence["shuffles"]
    check("negative control: a shuffled order is unremarkable among the shuffles, and the sorted days beat every shuffle",
          controls["one_shuffled_order_as_if_observed"]["shuffles_at_or_above_it"] > 0.05 * shuffles
          and controls["days_sorted_by_count_as_if_observed"]["shuffles_at_or_above_it"] == 0)
    return {"ten_empty_days": {"log_likelihoods": logliks, "picked_by_aic": picks["aic"], "picked_by_bic": picks["bic"]},
            "lag1_test_on_known_orders": controls}


def strip_private(value):
    if isinstance(value, dict):
        return {key: strip_private(item) for key, item in value.items() if not key.startswith("_")}
    if isinstance(value, list):
        return [strip_private(item) for item in value]
    return value


def analyze(observed: dict, scenarios: dict) -> dict:
    rounding = {f"{key}_decimals": value for key, value in DECIMALS.items()}
    if {key: value for key, value in scenarios["rounding"].items() if key != "note"} != rounding:
        raise ValueError("scenarios.json rounding does not match analyze.py")
    platform_guard()
    search = scenarios["search"]
    counts = list(observed["daily_counts"].values())
    t = tally(counts)
    seen = observed_section(observed, counts, t)
    raw = fit_all(t, search["score_bisection"])
    fits = fits_section(t, raw, scenarios["candidates"]["models"])
    optimiser = optimiser_section(t, search, raw)
    adequacy = adequacy_section(t, raw, scenarios["adequacy_bins"], scenarios["recovery"]["pmf_tail"])
    gain = fits["twice_the_log_likelihood_gain"]["negative_binomial_over_geometric"]
    recovery = recovery_section(raw, scenarios["recovery"], search, gain)
    dependence = dependence_section(counts, t, raw, scenarios["dependence"], scenarios["recovery"], search, gain)
    scales = scales_section(scenarios["cited_scales"], fits)
    sensitivity = sensitivity_section(observed, scenarios["sensitivity"], search, fits)
    controls = negative_controls(search, dependence)
    worked = worked_examples(scenarios["worked_examples"], t, raw, fits, adequacy, recovery, sensitivity,
                             scenarios["cited_scales"])
    transfer = transfer_task(scenarios["transfer_task"], search, scenarios["cited_scales"])
    verdict = hypothesis_section(scenarios["hypothesis_thresholds"], fits, recovery, dependence)
    return strip_private({
        "module_id": scenarios["module_id"],
        "kind": "observed daily counts (observed), fits and criteria computed from them (fits, optimiser, adequacy, "
                "cited_scales, sensitivity, the first half of dependence) and seeded samples from assumed generators "
                "(recovery, the sticky process, transfer_task)",
        "rounding": "log-likelihoods, AIC, BIC and their differences to 3 decimals; parameters and probabilities to 6; "
                    "shares of samples and autocorrelations to 4; expected days and ratios of shares to 2; tiny expected "
                    "days to 3 significant digits. " + scenarios["rounding"]["note"],
        "arithmetic": "IEEE 754 doubles with +, -, * and /, plus correctly rounded square roots; ln and the chi-square "
                      "tail are series built from those operations; random.Random(seed).random() supplies every draw",
        "observed": seen,
        "fits": fits,
        "optimiser": optimiser,
        "adequacy": adequacy,
        "cited_scales": scales,
        "sensitivity": sensitivity,
        "recovery": recovery,
        "dependence": dependence,
        "hypothesis_test": verdict,
        "worked_examples": worked,
        "negative_controls": controls,
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
