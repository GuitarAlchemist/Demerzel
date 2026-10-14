#!/usr/bin/env python3
"""PSY-012 fixture: early-warning indicators, how often they detect, how often they cry wolf.

Synthetic part (scenarios.json). A noisy one-variable system is driven slowly toward a
fold bifurcation; stationary AR(1) series approach nothing. For many seeded runs of
each, the script computes the rolling variance and the rolling lag-1 autocorrelation
(after removing a straight line inside each window), summarises each with Kendall's
tau against time, and counts how often an alarm rule fires.

Observed part (observed-input.json, written by extract.py). The script counts how much
the recorded quality trend varies. It computes no indicator on it.

Standard library only. No clock, no global random state: every random number comes from
random.Random(seed) with the seed stored in scenarios.json.
"""

from __future__ import annotations

import argparse
import json
import math
import random
from bisect import bisect_left, bisect_right
from pathlib import Path


HERE = Path(__file__).resolve().parent
DEFAULT_INPUT = HERE / "scenarios.json"
DEFAULT_OBSERVED = HERE / "observed-input.json"
DEFAULT_OUTPUT = HERE / "results.json"


# --------------------------------------------------------------------------- estimators

def kendall_tau(values: list[float]) -> float:
    """Kendall's tau-b between a sequence and its position (time), in O(m log m).

    Every pair (i < j) is concordant if values[i] < values[j], discordant if greater,
    tied if equal. Time has no ties, so tau-b = (C - D) / sqrt(n0 * (n0 - ties)).
    """
    ordered: list[float] = []
    insert = ordered.insert
    concordant = discordant = 0
    for index, value in enumerate(values):
        # `ordered` holds the earlier values, sorted: those below `value` are concordant
        # with it, those above are discordant, those equal are ties.
        high = bisect_right(ordered, value)
        low = high
        if high and ordered[high - 1] == value:
            low = bisect_left(ordered, value, 0, high)
        concordant += low
        discordant += index - high
        insert(high, value)
    count = len(values)
    pairs = count * (count - 1) // 2
    ties = pairs - concordant - discordant
    if pairs == 0 or ties == pairs:
        raise ValueError("Kendall's tau is undefined for fewer than two distinct values")
    return (concordant - discordant) / math.sqrt(pairs * (pairs - ties))


def kendall_counts_naive(values: list[float]) -> tuple[int, int, int]:
    """Concordant, discordant and tied pairs by comparing every pair: the definition."""
    concordant = discordant = ties = 0
    for i in range(len(values)):
        for j in range(i + 1, len(values)):
            if values[i] < values[j]:
                concordant += 1
            elif values[i] > values[j]:
                discordant += 1
            else:
                ties += 1
    return concordant, discordant, ties


def kendall_tau_naive(values: list[float]) -> float:
    concordant, discordant, ties = kendall_counts_naive(values)
    pairs = concordant + discordant + ties
    return (concordant - discordant) / math.sqrt(pairs * (pairs - ties))


def naive_tau_sd(count: int) -> float:
    """Standard deviation of tau under the textbook null: `count` INDEPENDENT values."""
    return math.sqrt(2.0 * (2.0 * count + 5.0) / (9.0 * count * (count - 1.0)))


def rolling_indicators(series: list[float], window: int, detrend: bool = True):
    """Variance and lag-1 autocorrelation in every window of `window` consecutive points.

    With detrend=True the least-squares straight line is removed inside each window
    first, so a steady drift of the level is not counted as variance:
        e[u] = y[u] - (a + b * u), u = 0 .. W - 1
        variance = sum(e[u]^2) / (W - 2)
        autocorrelation = sum(e[u] * e[u + 1], u = 0 .. W - 2) / sum(e[u]^2)
    With detrend=False only the window mean is removed and the divisor is W - 1.
    The sums are updated in O(1) per step; window_direct() recomputes them the slow way.
    """
    size = len(series)
    if window < 4 or window > size:
        raise ValueError("window must be between 4 and the series length")
    mean = 0.0
    for value in series:
        mean += value
    mean /= size
    y = [value - mean for value in series]
    centre = (window - 1) / 2.0
    time_squares = window * (window * window - 1) / 12.0
    time_products = time_squares - centre * (centre + 1.0)
    divisor = window - 2 if detrend else window - 1
    total = squares = products = timed = 0.0
    for index in range(window):
        value = y[index]
        total += value
        squares += value * value
        timed += index * value
    for index in range(window - 1):
        products += y[index] * y[index + 1]
    variances: list[float] = []
    autocorrelations: list[float | None] = []
    last = size - window
    for start in range(last + 1):
        first = y[start]
        final = y[start + window - 1]
        average = total / window
        residual_squares = squares - window * average * average
        lagged = products - average * (2.0 * total - first - final) + (window - 1) * average * average
        if detrend:
            covariance = timed - start * total - centre * total
            slope = covariance / time_squares
            residual_squares -= slope * covariance
            lagged += slope * slope * time_products - slope * (2.0 * covariance - (centre + 1.0) * (final - first))
        variances.append(residual_squares / divisor)
        autocorrelations.append(lagged / residual_squares if residual_squares > 1e-12 else None)
        if start < last:
            incoming = y[start + window]
            total += incoming - first
            squares += incoming * incoming - first * first
            products += final * incoming - first * y[start + 1]
            timed += (start + window) * incoming - start * first
    return variances, autocorrelations


def window_direct(values: list[float], detrend: bool = True) -> tuple[float, float]:
    """One window computed from its residuals, without any running sum."""
    count = len(values)
    centre = (count - 1) / 2.0
    average = math.fsum(values) / count
    slope = 0.0
    if detrend:
        slope = (math.fsum((u - centre) * (values[u] - average) for u in range(count))
                 / math.fsum((u - centre) ** 2 for u in range(count)))
    residuals = [values[u] - average - slope * (u - centre) for u in range(count)]
    squares = math.fsum(e * e for e in residuals)
    lagged = math.fsum(residuals[u] * residuals[u + 1] for u in range(count - 1))
    return squares / (count - 2 if detrend else count - 1), lagged / squares


def constant_window_count(values: list, window: int) -> tuple[int, int]:
    """(windows, windows whose values are all equal) by exact comparison."""
    windows = len(values) - window + 1
    if windows < 1:
        return 0, 0
    constant = 0
    for start in range(windows):
        first = values[start]
        if all(values[start + offset] == first for offset in range(1, window)):
            constant += 1
    return windows, constant


# --------------------------------------------------------------------------- simulators

def simulate_ar1(rng: random.Random, length: int, coefficient: float, noise_sd: float) -> list[float]:
    """Stationary AR(1): y[t+1] = coefficient * y[t] + noise, started from its own distribution."""
    normal = rng.normalvariate
    value = noise_sd / math.sqrt(1.0 - coefficient * coefficient) * normal(0.0, 1.0)
    out = []
    for _ in range(length):
        out.append(value)
        value = coefficient * value + noise_sd * normal(0.0, 1.0)
    return out


def q_schedule(index: int, length: int, q_start: float, q_end: float) -> float:
    return q_start + (q_end - q_start) * index / (length - 1)


def simulate_fold(rng: random.Random, length: int, step: float, noise_sd: float,
                  q_start: float, q_end: float, burn_in: int):
    """x[t+1] = x[t] + step * (x[t]^2 - q[t]^2) + noise. Returns (series, tipped).

    The stable resting point is x = -q, the unstable point x = +q; they meet at q = 0.
    A run that passes +q has tipped and is not analysed.
    """
    normal = rng.normalvariate
    value = -q_start
    for _ in range(burn_in):
        value = value + step * (value * value - q_start * q_start) + noise_sd * normal(0.0, 1.0)
        if value > q_start:
            return [], True
    out = []
    for index in range(length):
        q = q_schedule(index, length, q_start, q_end)
        if value > q:
            return out, True
        out.append(value)
        value = value + step * (value * value - q * q) + noise_sd * normal(0.0, 1.0)
    return out, False


def simulate_linear_twin(rng: random.Random, length: int, step: float, noise_sd: float,
                         q_start: float, q_end: float) -> list[float]:
    """AR(1) whose coefficient follows the fold's local value 1 - 2 * step * q[t]: slowing down
    with no moving level and no nonlinearity."""
    normal = rng.normalvariate
    first = 1.0 - 2.0 * step * q_start
    value = noise_sd / math.sqrt(1.0 - first * first) * normal(0.0, 1.0)
    out = []
    for index in range(length):
        coefficient = 1.0 - 2.0 * step * q_schedule(index, length, q_start, q_end)
        out.append(value)
        value = coefficient * value + noise_sd * normal(0.0, 1.0)
    return out


# --------------------------------------------------------------------------- summaries

def percentile(ordered: list[float], share: float) -> float:
    """Nearest-rank percentile of an already sorted list."""
    rank = max(1, math.ceil(share * len(ordered)))
    return ordered[rank - 1]


def describe(values: list[float]) -> dict:
    ordered = sorted(values)
    return {
        "mean": math.fsum(ordered) / len(ordered),
        "p05": percentile(ordered, 0.05),
        "median": percentile(ordered, 0.5),
        "p95": percentile(ordered, 0.95),
    }


def config_key(length: int, window: int) -> str:
    return f"n{length}_w{window}"


def run_batch(kind: str, length: int, windows: list[int], experiment: dict, seed: int,
              coefficient: float | None = None, noise_sd: float | None = None,
              runs: int | None = None, undetrended: bool = False) -> dict:
    """Simulate `runs` series of one kind and keep, per window length, the two taus of each run."""
    rng = random.Random(seed)
    approach = experiment["approach"]
    noise = experiment["noise_sd"] if noise_sd is None else noise_sd
    count = experiment["runs_per_batch"] if runs is None else runs
    per_window = {window: {"tau_variance": [], "tau_autocorrelation": [], "first_variance": [],
                           "first_autocorrelation": [], "last_variance": [], "last_autocorrelation": [],
                           "plain_tau_variance": [], "plain_tau_autocorrelation": []}
                  for window in windows}
    tipped = 0
    for _ in range(count):
        if kind == "fold":
            series, has_tipped = simulate_fold(rng, length, approach["step"], noise, approach["q_start"],
                                               approach["q_end"], approach["burn_in_steps"])
            if has_tipped:
                tipped += 1
                continue
        elif kind == "twin":
            series = simulate_linear_twin(rng, length, approach["step"], noise,
                                          approach["q_start"], approach["q_end"])
        elif kind == "ar1":
            series = simulate_ar1(rng, length, coefficient, noise)
        else:
            raise ValueError(kind)
        for window in windows:
            variances, autocorrelations = rolling_indicators(series, window, detrend=True)
            assert None not in autocorrelations, "a simulated window had no variance"
            store = per_window[window]
            store["tau_variance"].append(kendall_tau(variances))
            store["tau_autocorrelation"].append(kendall_tau(autocorrelations))
            store["first_variance"].append(variances[0])
            store["first_autocorrelation"].append(autocorrelations[0])
            store["last_variance"].append(variances[-1])
            store["last_autocorrelation"].append(autocorrelations[-1])
            if undetrended:
                variances, autocorrelations = rolling_indicators(series, window, detrend=False)
                store["plain_tau_variance"].append(kendall_tau(variances))
                store["plain_tau_autocorrelation"].append(kendall_tau(autocorrelations))
    return {"runs": count, "tipped": tipped, "per_window": per_window}


def calibrated_threshold(joint: list[float], target: float) -> tuple[float, int]:
    """Smallest observed value T such that at most `target` of the calibration runs have M >= T.

    With k = floor(target * N) alarms allowed, T is the k-th largest calibration value,
    or the next larger one when several runs tie at that value.
    """
    allowed = math.floor(target * len(joint) + 1e-9)
    if allowed < 1:
        raise ValueError("too few calibration runs for this false-alarm target")
    descending = sorted(joint, reverse=True)
    position = allowed - 1
    while position >= 0 and sum(1 for value in joint if value >= descending[position]) > allowed:
        position -= 1
    if position < 0:
        raise ValueError("ties at the top of the calibration values leave no usable threshold")
    return descending[position], allowed


def summarise_system(batch: dict, window: int, thresholds: dict, fixed: float) -> dict:
    store = batch["per_window"][window]
    tau_v = store["tau_variance"]
    tau_a = store["tau_autocorrelation"]
    analysed = len(tau_v)
    assert analysed + batch["tipped"] == batch["runs"], "tipped + analysed must equal runs"
    joint = [min(a, b) for a, b in zip(tau_v, tau_a)]
    alarms = {name: sum(1 for value in joint if value >= limit) for name, limit in thresholds.items()}
    out = {
        "runs": batch["runs"],
        "tipped": batch["tipped"],
        "analysed": analysed,
        "tau_variance": describe(tau_v),
        "tau_autocorrelation": describe(tau_a),
        "tau_min": describe(joint),
        "first_window": {"variance_mean": math.fsum(store["first_variance"]) / analysed,
                         "autocorrelation_mean": math.fsum(store["first_autocorrelation"]) / analysed},
        "last_window": {"variance_mean": math.fsum(store["last_variance"]) / analysed,
                        "autocorrelation_mean": math.fsum(store["last_autocorrelation"]) / analysed},
        "alarms": alarms,
        "alarm_rate": {name: value / analysed for name, value in alarms.items()},
        "single_indicator_alarms_at_fixed_threshold": {
            "variance": sum(1 for value in tau_v if value >= fixed),
            "autocorrelation": sum(1 for value in tau_a if value >= fixed),
        },
        "both_taus_positive": sum(1 for value in joint if value > 0.0),
    }
    for name, value in alarms.items():
        assert 0 <= value <= analysed
    assert out["alarms"]["fixed"] <= min(out["single_indicator_alarms_at_fixed_threshold"].values())
    if store["plain_tau_variance"]:
        plain_joint = [min(a, b) for a, b in zip(store["plain_tau_variance"], store["plain_tau_autocorrelation"])]
        plain_alarms = sum(1 for value in plain_joint if value >= fixed)
        out["without_detrending"] = {
            "tau_variance_mean": math.fsum(store["plain_tau_variance"]) / analysed,
            "tau_autocorrelation_mean": math.fsum(store["plain_tau_autocorrelation"]) / analysed,
            "alarms_fixed": plain_alarms,
            "alarm_rate_fixed": plain_alarms / analysed,
        }
    return out


def predictive_value(base_rate: float, detection: float, false_alarm: float) -> dict:
    """Share of alarms that are true when `base_rate` of the watched systems are approaching."""
    cells = {
        "approaching_and_alarm": base_rate * detection,
        "approaching_and_silent": base_rate * (1.0 - detection),
        "stationary_and_alarm": (1.0 - base_rate) * false_alarm,
        "stationary_and_silent": (1.0 - base_rate) * (1.0 - false_alarm),
    }
    assert abs(math.fsum(cells.values()) - 1.0) < 1e-12, "the four joint probabilities must sum to 1"
    alarm = cells["approaching_and_alarm"] + cells["stationary_and_alarm"]
    return {
        "base_rate": base_rate,
        "probability_of_alarm": alarm,
        "share_of_alarms_that_are_true": cells["approaching_and_alarm"] / alarm if alarm > 0 else None,
    }


# --------------------------------------------------------------------------- sections

def self_checks(scenarios: dict) -> dict:
    hand = scenarios["hand_cases"]
    checks = scenarios["estimator_checks"]
    out: dict = {}

    # Kendall's tau: a hand case, two limits, a tie case, and the fast method against the definition.
    values = hand["kendall"]["values"]
    concordant, discordant, ties = kendall_counts_naive(values)
    pairs = len(values) * (len(values) - 1) // 2
    assert concordant + discordant + ties == pairs
    tau = kendall_tau(values)
    assert (concordant, discordant, ties) == (13, 2, 0), "hand count: 13 concordant, 2 discordant"
    assert abs(tau - 11.0 / 15.0) < 1e-12
    assert kendall_tau([1.0, 2.0, 3.0, 4.0]) == 1.0 and kendall_tau([4.0, 3.0, 2.0, 1.0]) == -1.0
    tie_case = [1.0, 2.0, 2.0, 3.0]
    assert abs(kendall_tau(tie_case) - 5.0 / math.sqrt(6.0 * 5.0)) < 1e-12
    rng = random.Random(checks["kendall_cross_check"]["seed"])
    worst = 0.0
    for _ in range(checks["kendall_cross_check"]["repeats"]):
        sample = [float(rng.randrange(40)) for _ in range(checks["kendall_cross_check"]["length"])]
        worst = max(worst, abs(kendall_tau(sample) - kendall_tau_naive(sample)))
    assert worst < 1e-12, "fast Kendall tau disagrees with the pairwise definition"
    out["kendall_hand_case"] = {
        "values": values, "pairs": pairs, "concordant": concordant, "discordant": discordant,
        "ties": ties, "tau": tau,
        "naive_test_threshold_for_6_values": scenarios["alarm_rules"]["naive_test"]["z_one_sided"] * naive_tau_sd(6),
    }
    out["kendall_fast_against_pairwise_max_difference"] = worst

    # One window by hand: values 1, 2, 4, 3 -> residuals -0.3, -0.1, 1.1, -0.7.
    variance, autocorrelation = rolling_indicators(hand["window"]["values"], 4)
    assert abs(variance[0] - 0.9) < 1e-12 and abs(autocorrelation[0] - (-0.85 / 1.8)) < 1e-12
    assert abs(variance[0] - hand["window"]["expected_variance"]) < 1e-9
    assert abs(autocorrelation[0] - hand["window"]["expected_autocorrelation"]) < 5e-5
    out["window_hand_case"] = {"values": hand["window"]["values"], "residuals": [-0.3, -0.1, 1.1, -0.7],
                               "variance": variance[0], "autocorrelation": autocorrelation[0]}

    # Running sums against a direct computation, with and without the straight line removed,
    # on a series that carries a large drift so the detrending has something to remove.
    cross = checks["rolling_cross_check"]
    rng = random.Random(cross["seed"])
    series = [0.4 * index + value for index, value in enumerate(simulate_ar1(rng, cross["length"], 0.8, 1.0))]
    worst = 0.0
    compared = 0
    for window in cross["windows"]:
        for detrend in (True, False):
            variances, autocorrelations = rolling_indicators(series, window, detrend)
            for start in range(len(variances)):
                direct = window_direct(series[start:start + window], detrend)
                worst = max(worst, abs(variances[start] - direct[0]) / direct[0],
                            abs(autocorrelations[start] - direct[1]))
                compared += 1
    assert compared > 0 and worst < 1e-8, "running sums disagree with the direct computation"
    out["rolling_against_direct"] = {"windows_compared": compared, "max_difference": worst}

    # Detrending removes a straight line exactly: adding one must not change the indicators.
    plain = simulate_ar1(random.Random(cross["seed"]), cross["length"], 0.8, 1.0)
    base = rolling_indicators(plain, 25)
    shifted = rolling_indicators([value + 3.0 * index - 7.0 for index, value in enumerate(plain)], 25)
    drift_effect = max(max(abs(a - b) for a, b in zip(base[0], shifted[0])),
                       max(abs(a - b) for a, b in zip(base[1], shifted[1])))
    assert drift_effect < 1e-8
    raw = rolling_indicators([value + 3.0 * index - 7.0 for index, value in enumerate(plain)], 25, detrend=False)
    inflation = min(a / b for a, b in zip(raw[0], base[0]))
    assert inflation > 10.0, "negative control: without detrending the same drift must inflate the variance"
    out["straight_line_drift"] = {"max_change_with_detrending": drift_effect,
                                  "smallest_variance_inflation_without_detrending": inflation}

    # The alarm statistic on two invented series with a known answer.
    rising = [float(index * index) for index in range(30)]
    falling = rising[::-1]
    assert min(kendall_tau(rising), kendall_tau(rising)) >= scenarios["alarm_rules"]["fixed_threshold"]
    assert min(kendall_tau(falling), kendall_tau(falling)) < 0.0
    out["alarm_controls"] = {"monotone_rise_fires": True, "monotone_fall_fires": False}

    # Count of constant windows on an invented series.
    case = hand["constant_windows"]
    windows, constant = constant_window_count(case["values"], case["window"])
    assert (windows, constant) == (case["expected_windows"], case["expected_constant_windows"])
    out["constant_window_hand_case"] = {"values": case["values"], "window": case["window"],
                                        "windows": windows, "constant_windows": constant}

    z = scenarios["alarm_rules"]["naive_test"]["z_one_sided"]
    upper_tail = 0.5 * math.erfc(z / math.sqrt(2.0))
    assert abs(upper_tail - scenarios["alarm_rules"]["naive_test"]["nominal_false_alarm_rate"]) < 1e-9
    return out


def theory_section(scenarios: dict) -> dict:
    """Known answers: AR(1) theory, long simulated runs measured with the fixture's estimator."""
    experiment = scenarios["experiment"]
    checks = scenarios["estimator_checks"]
    approach = experiment["approach"]
    noise = experiment["noise_sd"]
    length = checks["long_run_length"]

    def ar1_variance(coefficient: float) -> float:
        return noise * noise / (1.0 - coefficient * coefficient)

    out: dict = {"formulas": {
        "ar1_variance": "noise_sd^2 / (1 - coefficient^2)",
        "ar1_lag1_autocorrelation": "coefficient",
        "fold_local_coefficient": "1 - 2 * step * q",
    }}
    long_runs = {}
    for coefficient in experiment["control_coefficients"]:
        rng = random.Random(checks["seeds"][str(coefficient)])
        series = simulate_ar1(rng, length, coefficient, noise)
        variances, autocorrelations = rolling_indicators(series, length)
        expected = ar1_variance(coefficient)
        relative = variances[0] / expected - 1.0
        difference = autocorrelations[0] - coefficient
        assert abs(relative) < checks["variance_relative_tolerance"], "variance estimator is off the AR(1) value"
        assert abs(difference) < checks["autocorrelation_absolute_tolerance"], "lag-1 estimator is off the AR(1) value"
        long_runs[f"coefficient_{coefficient}"] = {
            "points": length,
            "variance_theory": expected, "variance_estimate": variances[0], "variance_relative_error": relative,
            "autocorrelation_theory": coefficient, "autocorrelation_estimate": autocorrelations[0],
            "autocorrelation_error": difference,
        }
    out["ar1_long_run"] = long_runs

    # Negative control for the tolerance: an estimator that forgot to square the coefficient must fail it.
    wrong = noise * noise / (1.0 - 0.9)
    out["tolerance_negative_control"] = {
        "wrong_formula": "noise_sd^2 / (1 - coefficient)",
        "relative_error_at_0.9": long_runs["coefficient_0.9"]["variance_estimate"] / wrong - 1.0,
        "rejected": abs(long_runs["coefficient_0.9"]["variance_estimate"] / wrong - 1.0)
                    >= checks["variance_relative_tolerance"],
    }
    assert out["tolerance_negative_control"]["rejected"]

    def local(q: float) -> dict:
        coefficient = 1.0 - 2.0 * approach["step"] * q
        return {"q": q, "resting_level": -q, "unstable_point": q, "coefficient": coefficient,
                "variance": ar1_variance(coefficient), "standard_deviation": math.sqrt(ar1_variance(coefficient)),
                "steps_to_lose_half_a_disturbance": math.log(0.5) / math.log(coefficient)}

    start, end = local(approach["q_start"]), local(approach["q_end"])
    out["fold_local"] = {
        "start": start, "end": end,
        "variance_ratio_end_over_start": end["variance"] / start["variance"],
        "distance_to_unstable_point_in_standard_deviations_at_end": 2.0 * end["q"] / end["standard_deviation"],
        "level_change_in_start_standard_deviations": (start["q"] - end["q"]) / start["standard_deviation"],
    }

    # The fold simulator held at a fixed q must behave like its linearisation.
    q_fixed = checks["fold_fixed_q"]
    rng = random.Random(checks["fold_fixed_q_seed"])
    series, tipped = simulate_fold(rng, length, approach["step"], noise, q_fixed, q_fixed, approach["burn_in_steps"])
    assert not tipped
    variances, autocorrelations = rolling_indicators(series, length)
    expected = local(q_fixed)
    relative = variances[0] / expected["variance"] - 1.0
    difference = autocorrelations[0] - expected["coefficient"]
    assert abs(relative) < checks["variance_relative_tolerance"]
    assert abs(difference) < checks["autocorrelation_absolute_tolerance"]
    level = math.fsum(series) / len(series)
    out["fold_held_at_fixed_q"] = {
        "q": q_fixed, "points": length,
        "coefficient_theory": expected["coefficient"], "autocorrelation_estimate": autocorrelations[0],
        "autocorrelation_error": difference,
        "variance_theory": expected["variance"], "variance_estimate": variances[0],
        "variance_relative_error": relative,
        "mean_level": level, "resting_level_theory": -q_fixed,
    }
    return out


def simulation_section(scenarios: dict) -> dict:
    experiment = scenarios["experiment"]
    rules = scenarios["alarm_rules"]
    fixed = rules["fixed_threshold"]
    z = rules["naive_test"]["z_one_sided"]
    seeds = experiment["seeds"]
    reference = f"control_{experiment['reference_control_coefficient']}"
    runs = experiment["runs_per_batch"]
    configurations: dict = {}
    for length in experiment["series_lengths"]:
        windows = [round(length * fraction) for fraction in experiment["window_fractions"]]
        batches = {
            "approach_fold": run_batch("fold", length, windows, experiment, seeds["approach_fold"][str(length)],
                                       undetrended=True),
            "linear_twin": run_batch("twin", length, windows, experiment, seeds["linear_twin"][str(length)]),
        }
        for coefficient in experiment["control_coefficients"]:
            name = f"control_{coefficient}"
            batches[name] = run_batch("ar1", length, windows, experiment, seeds[name][str(length)],
                                      coefficient=coefficient)
        calibration = run_batch("ar1", length, windows, experiment, seeds["calibration"][str(length)],
                                coefficient=experiment["calibration"]["coefficient"])
        for window in windows:
            rolling_values = length - window + 1
            store = calibration["per_window"][window]
            joint = [min(a, b) for a, b in zip(store["tau_variance"], store["tau_autocorrelation"])]
            threshold, allowed = calibrated_threshold(joint, experiment["calibration"]["false_alarm_target"])
            thresholds = {"naive": z * naive_tau_sd(rolling_values), "fixed": fixed, "calibrated": threshold}
            systems = {name: summarise_system(batch, window, thresholds, fixed) for name, batch in batches.items()}
            calibration_alarms = sum(1 for value in joint if value >= threshold)
            assert 0 < calibration_alarms <= allowed, "the calibrated threshold must respect its target"
            # Known answer for the whole chain: on independent runs of the calibration model the
            # calibrated rule must fire at about the target rate (three standard errors of a difference).
            target = experiment["calibration"]["false_alarm_target"]
            same_model = f"control_{experiment['calibration']['coefficient']}"
            realised = systems[same_model]["alarm_rate"]["calibrated"]
            tolerance = 3.0 * math.sqrt(2.0 * target * (1.0 - target) / runs)
            assert abs(realised - target) < tolerance, "calibrated rule misses its target on independent runs"
            detection = systems["approach_fold"]["alarm_rate"]
            summary = {}
            for rule in ("naive", "fixed", "calibrated"):
                false_alarms = {name: systems[name]["alarm_rate"][rule]
                                for name in systems if name.startswith("control_")}
                summary[rule] = {
                    "threshold_on_min_tau": thresholds[rule],
                    "detection_rate": detection[rule],
                    "false_alarm_rate": false_alarms,
                    "linear_twin_alarm_rate": systems["linear_twin"]["alarm_rate"][rule],
                    "share_of_alarms_that_are_true": [
                        predictive_value(rate, detection[rule], false_alarms[reference])
                        for rate in scenarios["base_rates"]
                    ],
                }
            configurations[config_key(length, window)] = {
                "series_length": length,
                "window": window,
                "rolling_values_per_run": rolling_values,
                "thresholds": thresholds,
                "runs_with_both_taus_positive": {name: systems[name]["both_taus_positive"] for name in systems},
                "calibration": {
                    "coefficient": experiment["calibration"]["coefficient"],
                    "runs": calibration["runs"],
                    "alarms_allowed": allowed,
                    "alarms_at_threshold": calibration_alarms,
                    "tau_min": describe(joint),
                    "false_alarm_rate_on_independent_runs_of_the_same_model": realised,
                    "tolerance_of_that_check": tolerance,
                },
                "summary": summary,
                "systems": systems,
            }
    largest_gap = 0.0
    for config in configurations.values():
        for system in config["systems"].values():
            # A lower threshold can only fire at least as often.
            ordered = sorted(config["thresholds"].items(), key=lambda item: item[1])
            counts = [system["alarms"][name] for name, _ in ordered]
            assert counts == sorted(counts, reverse=True), "alarm counts must fall as the threshold rises"
        for rule in config["summary"].values():
            largest_gap = max(largest_gap, abs(rule["detection_rate"] - rule["linear_twin_alarm_rate"]))
    # Mean reading of the first window of each stationary control, against the AR(1) value:
    # the long-run check passes, yet a short window reads low.
    noise = experiment["noise_sd"]
    window_bias = {}
    for coefficient in experiment["control_coefficients"]:
        rows = {}
        for config in configurations.values():
            first = config["systems"][f"control_{coefficient}"]["first_window"]
            rows[f"window_{config['window']}"] = {
                "autocorrelation_mean": first["autocorrelation_mean"],
                "autocorrelation_bias": first["autocorrelation_mean"] - coefficient,
                "variance_mean": first["variance_mean"],
                "variance_over_theory": first["variance_mean"] * (1.0 - coefficient * coefficient) / (noise * noise),
            }
        window_bias[f"control_{coefficient}"] = {
            "autocorrelation_theory": coefficient,
            "variance_theory": noise * noise / (1.0 - coefficient * coefficient),
            "first_window_means": rows,
        }
    return {
        "kind": "synthetic",
        "runs_per_batch": runs,
        "standard_error_of_a_rate_at_most": 0.5 / math.sqrt(runs),
        "reference_control_for_predictive_value": reference,
        "fold_against_linear_twin": {
            "largest_alarm_rate_difference": largest_gap,
            "standard_error_of_a_difference_at_most": math.sqrt(2.0) * 0.5 / math.sqrt(runs),
        },
        "window_bias": window_bias,
        "rules": {
            "naive": "each tau exceeds z * sd(tau) computed as if the rolling values were independent",
            "fixed": f"min tau >= {fixed}",
            "calibrated": "min tau >= the value exceeded by the false-alarm target share of independent "
                          "stationary calibration runs",
        },
        "configurations": configurations,
    }


def tipping_control(scenarios: dict) -> dict:
    """The main batches should hold no tipped run; show that the detector can find one."""
    experiment = scenarios["experiment"]
    control = scenarios["tipping_positive_control"]
    window = round(control["series_length"] * experiment["window_fractions"][0])
    batch = run_batch("fold", control["series_length"], [window], experiment, control["seed"],
                      noise_sd=control["noise_sd"], runs=control["runs"])
    assert batch["tipped"] > 0, "positive control: with four times the noise some runs must tip"
    assert batch["tipped"] + len(batch["per_window"][window]["tau_variance"]) == batch["runs"]
    return {"noise_sd": control["noise_sd"], "series_length": control["series_length"],
            "runs": batch["runs"], "tipped": batch["tipped"]}


def observed_section(observed: dict, windows: list[int]) -> dict:
    """How much the recorded quality trend varies. No indicator is computed on it."""
    counts = observed["counts"]
    fields = ("citation_count", "violation_count", "compliance_rate")
    per_field = {}
    for field in fields:
        constant_series = pairs = changes = most_values = most_changes = 0
        change_stamps: dict[str, int] = {}
        window_counts = {window: [0, 0] for window in windows}
        per_series = []
        for artifact in observed["artifacts"]:
            segments = artifact["segments"][field]
            values = [value for value, length in segments for _ in range(length)]
            stamps = artifact["measured_timestamps"]
            assert len(values) == artifact["rows_with_numeric_fields"] == len(stamps)
            series_changes = 0
            for index in range(1, len(values)):
                if values[index] != values[index - 1]:
                    series_changes += 1
                    change_stamps[stamps[index]] = change_stamps.get(stamps[index], 0) + 1
            assert series_changes == len(segments) - 1
            pairs += len(values) - 1
            changes += series_changes
            constant_series += 1 if series_changes == 0 else 0
            most_values = max(most_values, len(set(values)))
            most_changes = max(most_changes, series_changes)
            detail = {"artifact": artifact["artifact"], "records": len(values), "segments": segments,
                      "changes": series_changes}
            for window in windows:
                total, constant = constant_window_count(values, window)
                assert total == len(values) - window + 1 and 0 <= constant <= total
                window_counts[window][0] += total
                window_counts[window][1] += constant
                detail[f"window_{window}"] = {"windows": total, "constant_windows": constant}
            per_series.append(detail)
        per_field[field] = {
            "series": len(observed["artifacts"]),
            "series_with_one_value_only": constant_series,
            "series_that_change": len(observed["artifacts"]) - constant_series,
            "consecutive_pairs": pairs,
            "changes": changes,
            "share_of_pairs_that_change": changes / pairs,
            "most_changes_in_one_series": most_changes,
            "most_distinct_values_in_one_series": most_values,
            "distinct_runs_at_which_a_change_occurs": len(change_stamps),
            "series_changing_at_each_of_those_runs": {stamp: change_stamps[stamp] for stamp in sorted(change_stamps)},
            "rolling_windows": {
                f"window_{window}": {
                    "windows": total, "constant_windows": constant,
                    "share_constant": constant / total,
                    "windows_with_some_variation": total - constant,
                }
                for window, (total, constant) in window_counts.items()
            },
        }
        if changes > 0:
            per_field[field]["per_series"] = per_series
    assert sum(item["rows_with_numeric_fields"] for item in observed["artifacts"]) == counts["rows_with_numeric_fields"]
    assert per_field["citation_count"]["consecutive_pairs"] == counts["rows_with_numeric_fields"] - counts["artifacts"]
    varying = [field for field in fields if per_field[field]["changes"] > 0]
    return {
        "kind": "computed from observed data",
        "source_commit": observed["source_commit"],
        "source_files": [item["path"] for item in observed["source_files"]],
        "counts": counts,
        "shortest_series": min(item["rows_with_numeric_fields"] for item in observed["artifacts"]),
        "longest_series": max(item["rows_with_numeric_fields"] for item in observed["artifacts"]),
        "fields": per_field,
        "fields_with_any_change": varying,
        "indicators_computed": False,
        "reason": "A window whose values are all equal has variance 0 and a lag-1 autocorrelation of 0/0. "
                  "Where the series does change, it changes by isolated steps shared by many artifacts, "
                  "not by fluctuations around a level.",
    }


def transfer_section(scenarios: dict) -> dict:
    """Expected answers for the learner task, from inputs that differ from the lesson's."""
    task = scenarios["transfer_task"]
    z = scenarios["alarm_rules"]["naive_test"]["z_one_sided"]
    fold = task["fold"]

    def local(q: float) -> dict:
        coefficient = 1.0 - 2.0 * fold["step"] * q
        variance = fold["noise_sd"] ** 2 / (1.0 - coefficient * coefficient)
        return {"q": q, "coefficient": coefficient, "variance": variance, "standard_deviation": math.sqrt(variance)}

    far, near = local(fold["q_far"]), local(fold["q_near"])
    tau_v = kendall_tau(task["rolling_variance"])
    tau_a = kendall_tau(task["rolling_autocorrelation"])
    counts_v = kendall_counts_naive(task["rolling_variance"])
    counts_a = kendall_counts_naive(task["rolling_autocorrelation"])
    joint = min(tau_v, tau_a)
    log = task["monitoring_log"]
    detection = log["alarms_in_approaching"] / log["approaching_systems"]
    false_alarm = log["alarms_in_stationary"] / log["stationary_systems"]
    naive = task["naive_test"]
    rolling_values = naive["series_length"] - naive["window"] + 1
    flat = task["flat_series"]
    values = [value for value, length in flat["segments"] for _ in range(length)]
    windows, constant = constant_window_count(values, flat["window"])
    return {
        "kind": "computed from hypothetical inputs",
        "question_1_local_theory": {
            "far": far, "near": near, "variance_ratio_near_over_far": near["variance"] / far["variance"],
        },
        "question_2_trend": {
            "pairs": len(task["rolling_variance"]) * (len(task["rolling_variance"]) - 1) // 2,
            "variance": {"concordant": counts_v[0], "discordant": counts_v[1], "ties": counts_v[2], "tau": tau_v},
            "autocorrelation": {"concordant": counts_a[0], "discordant": counts_a[1], "ties": counts_a[2],
                                "tau": tau_a},
            "min_tau": joint,
            "threshold": task["alarm_threshold"],
            "alarm": joint >= task["alarm_threshold"],
        },
        "question_3_rates": {
            "detection_rate": detection,
            "false_alarm_rate": false_alarm,
            **predictive_value(log["base_rate"], detection, false_alarm),
        },
        "question_4_preconditions": {
            "naive_test": {
                "rolling_values": rolling_values,
                "tau_standard_deviation_if_independent": naive_tau_sd(rolling_values),
                "threshold": z * naive_tau_sd(rolling_values),
            },
            "flat_series": {
                "points": len(values), "distinct_values": len(set(values)), "changes": len(flat["segments"]) - 1,
                "window": flat["window"], "windows": windows, "constant_windows": constant,
                "share_constant": constant / windows, "windows_with_some_variation": windows - constant,
            },
        },
        "question_5": "open answer: a plan and a falsifier, scored with the rubric in the review brief",
    }


def rounded(value, decimals: int):
    """Round every float; leave integers, strings and booleans as they are."""
    if isinstance(value, bool):
        return value
    if isinstance(value, float):
        result = round(value, decimals)
        return 0.0 if result == 0 else result
    if isinstance(value, dict):
        return {key: rounded(item, decimals) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [rounded(item, decimals) for item in value]
    return value


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--input", type=Path, default=DEFAULT_OBSERVED, help="observed-input.json written by extract.py")
    parser.add_argument("--scenarios", type=Path, default=DEFAULT_INPUT, help="scenarios JSON (synthetic assumptions)")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT, help="where to write the results JSON")
    parser.add_argument("--check", action="store_true",
                        help="recompute and exit 1 if the saved results JSON differs, without writing")
    args = parser.parse_args()
    scenarios = json.loads(args.scenarios.read_text(encoding="utf-8"))
    observed = json.loads(args.input.read_text(encoding="utf-8"))
    decimals = scenarios["float_decimals"]
    result = {
        "schema_version": "0.1.0",
        "module_id": scenarios["module_id"],
        "float_decimals": decimals,
        "labels": "Sections marked synthetic come from assumed inputs and are not measurements of any project. "
                  "The section observed_quality_trend is computed from the pinned repository extract.",
        "inputs": {
            "scenarios": args.scenarios.name,
            "observed": args.input.name,
            "observed_source_commit": observed["source_commit"],
        },
        "self_checks": self_checks(scenarios),
        "theory": theory_section(scenarios),
        "simulation": simulation_section(scenarios),
        "tipping_positive_control": tipping_control(scenarios),
        "observed_quality_trend": observed_section(observed, scenarios["observed_window_lengths"]),
        "transfer_task": transfer_section(scenarios),
    }
    text = json.dumps(rounded(result, decimals), ensure_ascii=False, indent=2) + "\n"
    if args.check:
        saved = args.output.read_bytes() if args.output.is_file() else b""
        if saved != text.encode("utf-8"):
            print(f"check failed: {args.output} differs from a fresh run")
            return 1
        print(f"check passed: {args.output} equals a fresh run")
        return 0
    with open(args.output, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(text)
    print(f"wrote {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
