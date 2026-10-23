#!/usr/bin/env python3
"""PSY-007 analysis: do eighteen citation counts support a power law?

Reads observed-input.json (written by extract.py) and scenarios.json, never the
repository, and writes results.json:

- the rank-size table and the least-squares line of the log-log rank plot;
- the maximum-likelihood exponent of a discrete power law above each cut x_min,
  next to the continuous closed form, with the Kolmogorov-Smirnov distance;
- the log-likelihoods of a power law, an exponential and a lognormal, all three
  as distributions on the integers x >= x_min, and their pairwise comparison;
- seeded synthetic samples of the same size from each family: the spread of the
  fitted exponent and how often the comparison finds the family that generated
  the sample;
- the specification's own detection rule (a share of citations held by the top
  share of artifacts) and the goodness-of-fit test, on the recorded counts and on
  the hand-typed counts of the last run before git grep.

Run from the repository root:
    python -I scripts/streeling_fixtures/psychohistory/psy-007/analyze.py
    python -I scripts/streeling_fixtures/psychohistory/psy-007/analyze.py --check
"""

from __future__ import annotations

import argparse
import json
import math
import random
import sys
from pathlib import Path

# This program lives under scripts/ (CONTRIBUTING.md: no executable code outside scripts/); its data stays
# under state/streeling/fixtures/. FIXTURE_FILE is the path the program would have next to that data.
FIXTURE_FILE = (Path(__file__).resolve().parents[4]
                / "state/streeling/fixtures/psychohistory/psy-007" / Path(__file__).name)

HERE = FIXTURE_FILE.parent
SQRT2 = math.sqrt(2.0)
LOG_SQRT_2PI = 0.5 * math.log(2.0 * math.pi)
GOLDEN = (math.sqrt(5.0) - 1.0) / 2.0
HEAD = 16  # terms of the zeta sum added one by one before the Euler-Maclaurin tail
NARROW = 1e-5  # below this width (in standard deviations) an interval probability is density x width
NV_MAGIC = 1.7155277699214135  # 4 exp(-1/2) / sqrt(2), constant of the Kinderman-Monahan normal sampler
FAMILIES = ("power_law", "exponential", "lognormal")
PAIRS = (("power_law", "exponential"), ("power_law", "lognormal"), ("exponential", "lognormal"))
DEC = {"exponent": 3, "loglik": 2, "statistic": 3, "p_value": 4, "percent": 1}
CHECKS: dict[str, int] = {}  # self-check -> times evaluated


def check(name: str, condition: bool, detail: str = "") -> None:
    """A self-check that can fail: abort instead of writing a wrong result."""
    if not condition:
        raise AssertionError(f"self-check failed: {name}" + (f" ({detail})" if detail else ""))
    CHECKS[name] = CHECKS.get(name, 0) + 1


def rnd(value, kind: str):
    """Round for storage; None stays None and -0.0 becomes 0.0."""
    if value is None:
        return None
    rounded = round(value, DEC[kind])
    return 0.0 if rounded == 0 else rounded


def share(count: int, total: int) -> dict:
    return {"count": count, "of": total, "percent": rnd(100.0 * count / total, "percent")}


# --------------------------------------------------------------------------- power law

def hurwitz(s: float, q) -> tuple[float, float]:
    """zeta(s, q) = sum over k >= 0 of (q + k)^-s, and its derivative in s (s > 1, q >= 1).

    HEAD terms are summed; the rest is the Euler-Maclaurin tail with three correction terms.
    """
    q = float(q)
    total = dtotal = 0.0
    for k in range(HEAD):
        log_k = math.log(q + k)
        term = math.exp(-s * log_k)
        total += term
        dtotal -= log_k * term
    a = q + HEAD
    log_a = math.log(a)
    power = math.exp(-s * log_a)  # a^-s
    integral = a * power / (s - 1.0)
    p3 = s * (s + 1.0) * (s + 2.0)
    p5 = p3 * (s + 3.0) * (s + 4.0)
    c2 = power / (12.0 * a)
    c3 = c2 / (60.0 * a * a)
    c4 = c3 / (42.0 * a * a)
    total += integral + 0.5 * power + s * c2 - p3 * c3 + p5 * c4
    dp3 = 3.0 * s * s + 6.0 * s + 2.0
    dp5 = p5 * (1.0 / s + 1.0 / (s + 1.0) + 1.0 / (s + 2.0) + 1.0 / (s + 3.0) + 1.0 / (s + 4.0))
    dtotal += (-log_a * integral - integral / (s - 1.0) - 0.5 * log_a * power
               + c2 * (1.0 - s * log_a) - c3 * (dp3 - p3 * log_a) + c4 * (dp5 - p5 * log_a))
    return total, dtotal


def fit_power_law(mean_log: float, x_min: int, bounds: tuple[float, float]):
    """Maximum-likelihood exponent of the discrete power law on x >= x_min.

    Solves -zeta'(alpha, x_min) / zeta(alpha, x_min) = mean of ln x (the model's mean of ln x equals the
    sample's) by the Illinois false-position method in u = 1 / (alpha - 1). Returns None when the likelihood
    has no maximum inside the search bounds (for example when every value equals x_min).
    """
    def score(u: float) -> float:
        zeta, dzeta = hurwitz(1.0 + 1.0 / u, x_min)
        return -dzeta / zeta - mean_log

    u_low, u_high = 1.0 / (bounds[1] - 1.0), 1.0 / (bounds[0] - 1.0)
    f_low, f_high = score(u_low), score(u_high)
    if not f_low < 0.0 < f_high:
        return None
    u, side = u_low, 0
    for _ in range(200):
        u = (u_low * f_high - u_high * f_low) / (f_high - f_low)
        f = score(u)
        if abs(f) <= 1e-13:
            break
        if f < 0.0:
            u_low, f_low = u, f
            if side == -1:
                f_high *= 0.5
            side = -1
        else:
            u_high, f_high = u, f
            if side == 1:
                f_low *= 0.5
            side = 1
    else:
        raise ArithmeticError(f"power-law fit did not converge (mean ln x = {mean_log}, x_min = {x_min})")
    return 1.0 + 1.0 / u


def power_law_logpmf(xs, alpha: float, x_min: int) -> list[float]:
    log_zeta = math.log(hurwitz(alpha, x_min)[0])
    return [-alpha * math.log(x) - log_zeta for x in xs]


def power_law_tail(alpha: float, x_min: int, x) -> float:
    """P(X >= x) for the discrete power law on x >= x_min."""
    return hurwitz(alpha, x)[0] / hurwitz(alpha, x_min)[0]


def ks_power_law(xs, alpha: float, x_min: int) -> float:
    """Kolmogorov-Smirnov distance: the largest gap between the sample's and the model's P(X <= x)."""
    ordered = sorted(xs)
    n = len(ordered)
    zeta = hurwitz(alpha, x_min)[0]
    largest, i = 0.0, 0
    while i < n:
        x, j = ordered[i], i
        while j < n and ordered[j] == x:
            j += 1
        below = 1.0 - hurwitz(alpha, x)[0] / zeta  # model P(X <= x - 1); the sample has i / n there
        up_to = 1.0 - hurwitz(alpha, x + 1)[0] / zeta  # model P(X <= x); the sample has j / n
        largest = max(largest, abs(i / n - below), abs(j / n - up_to))
        i = j
    return largest


def draw_power_law(rng: random.Random, alpha: float, x_min: int) -> int:
    """Exact draw from the discrete power law: Devroye's rejection from a rounded-down Pareto variable."""
    beta = alpha - 1.0

    def h(k) -> float:  # k (1 - (1 + 1/k)^-beta), increasing in k
        t = math.expm1(beta * math.log1p(1.0 / k))
        return k * t / (1.0 + t)

    h_min = h(x_min)
    while True:
        k = math.floor(x_min * (1.0 - rng.random()) ** (-1.0 / beta))
        if rng.random() * h(k) <= h_min:
            return k


# --------------------------------------------------------------------------- exponential

def fit_exponential(xs, x_min: int) -> dict:
    """Discrete exponential (geometric) on x >= x_min; closed-form maximum likelihood."""
    n = len(xs)
    excess = sum(xs) - n * x_min
    if excess == 0:
        return {"mean_excess": 0.0, "log_q": None, "log_1_minus_q": 0.0, "loglik": 0.0}
    m = excess / n
    log_q, log_1_minus_q = -math.log1p(1.0 / m), -math.log1p(m)
    return {"mean_excess": m, "log_q": log_q, "log_1_minus_q": log_1_minus_q,
            "loglik": n * log_1_minus_q + excess * log_q}


def exponential_logpmf(xs, fit: dict, x_min: int) -> list[float]:
    if fit["log_q"] is None:
        return [0.0 for _ in xs]
    return [fit["log_1_minus_q"] + (x - x_min) * fit["log_q"] for x in xs]


def draw_exponential(rng: random.Random, mean: float, x_min: int) -> int:
    log_q = -math.log1p(1.0 / (mean - x_min))
    return x_min + math.floor(math.log(1.0 - rng.random()) / log_q)


# --------------------------------------------------------------------------- lognormal

def normal_between(a: float, b: float) -> float:
    """Phi(b) - Phi(a) for a < b, computed in the tail where the two terms are small."""
    if a > 0.0:
        return 0.5 * (math.erfc(a / SQRT2) - math.erfc(b / SQRT2))
    if b < 0.0:
        return 0.5 * (math.erfc(-b / SQRT2) - math.erfc(-a / SQRT2))
    return 0.5 * (math.erf(b / SQRT2) - math.erf(a / SQRT2))


def normal_density(z: float) -> float:
    return math.exp(-0.5 * z * z - LOG_SQRT_2PI)


def lognormal_intervals(xs) -> list[tuple]:
    """For each count x: ln x and the width of (ln(x - 1), ln x]; width None for x = 1, where the interval is (0, 1]."""
    return [(math.log(x), None if x == 1 else -math.log1p(-1.0 / x)) for x in xs]


def lognormal_terms(a: float, b: float, intervals):
    """Log-likelihood, gradient and Hessian of the rounded-up lognormal in (a, b) = (mu / sigma, 1 / sigma).

    P(X = x) = Phi(b ln x - a) - Phi(b ln(x - 1) - a). In these coordinates the log-likelihood is concave.
    Also returns the per-observation log-probabilities. Returns None when a probability underflows.
    """
    ga = gb = haa = hab = hbb = 0.0
    logs = []
    for high, width in intervals:
        zb = b * high - a
        if width is None:
            p = 0.5 * math.erfc(-zb / SQRT2)
            fb = normal_density(zb)
            da, db = -fb, high * fb
            daa, dab, dbb = -zb * fb, high * zb * fb, -high * high * zb * fb
        elif b * width < NARROW:
            mid = high - 0.5 * width
            m = b * mid - a
            logs.append(-0.5 * m * m - LOG_SQRT_2PI + math.log(b * width))
            ga += m
            gb += 1.0 / b - m * mid
            haa -= 1.0
            hab += mid
            hbb -= mid * mid + 1.0 / (b * b)
            continue
        else:
            low = high - width
            za = zb - b * width
            p = normal_between(za, zb)
            fa, fb = normal_density(za), normal_density(zb)
            da, db = fa - fb, high * fb - low * fa
            daa = za * fa - zb * fb
            dab = high * zb * fb - low * za * fa
            dbb = low * low * za * fa - high * high * zb * fb
        if p <= 0.0:
            return None
        logs.append(math.log(p))
        ra, rb = da / p, db / p
        ga += ra
        gb += rb
        haa += daa / p - ra * ra
        hab += dab / p - ra * rb
        hbb += dbb / p - rb * rb
    return math.fsum(logs), ga, gb, haa, hab, hbb, logs


def fit_lognormal(xs) -> dict:
    """Maximum likelihood of the rounded-up lognormal by damped Newton steps in (mu / sigma, 1 / sigma)."""
    intervals = lognormal_intervals(xs)
    centres = [math.log(x - 0.5) for x in xs]
    n = len(xs)
    mean = math.fsum(centres) / n
    sd = max(math.sqrt(math.fsum((c - mean) ** 2 for c in centres) / n), 0.25)
    a, b = mean / sd, 1.0 / sd
    current = lognormal_terms(a, b, intervals)
    converged, steps = False, 0
    while current is not None and steps < 200:
        loglik, ga, gb, haa, hab, hbb, _ = current
        det = haa * hbb - hab * hab
        if haa < 0.0 and det > 0.0:
            sa, sb = (hab * gb - hbb * ga) / det, (hab * ga - haa * gb) / det
        else:  # not strictly concave here (flat direction): a plain gradient step
            scale = 1.0 / max(abs(haa), abs(hbb), 1.0)
            sa, sb = ga * scale, gb * scale
        gain = ga * sa + gb * sb  # expected gain in log-likelihood is gain / 2
        if gain < 1e-9:
            converged = True
            break
        step, accepted = 1.0, None
        while step > 1e-10:
            trial = lognormal_terms(a + step * sa, b + step * sb, intervals) if b + step * sb > 0.0 else None
            if trial is not None and trial[0] >= loglik + 1e-4 * step * gain:
                accepted = trial
                break
            step *= 0.5
        if accepted is None:
            break
        a, b, current = a + step * sa, b + step * sb, accepted
        steps += 1
    if current is None:
        raise ArithmeticError("lognormal fit: a probability underflowed at the starting point")
    return {"mu": a / b, "sigma": 1.0 / b, "loglik": current[0], "logpmf": current[6],
            "converged": converged, "newton_steps": steps}


def draw_lognormal(rng: random.Random, mu: float, sigma: float) -> int:
    """A lognormal variable rounded up; the normal draw is Kinderman-Monahan, written out to stay version-proof."""
    while True:
        u1, u2 = rng.random(), 1.0 - rng.random()
        z = NV_MAGIC * (u1 - 0.5) / u2
        if z * z / 4.0 <= -math.log(u2):
            return max(1, math.ceil(math.exp(mu + sigma * z)))


def golden_max(function, low: float, high: float, tolerance: float = 1e-7) -> tuple[float, float]:
    c, d = high - GOLDEN * (high - low), low + GOLDEN * (high - low)
    fc, fd = function(c), function(d)
    while high - low > tolerance:
        if fc < fd:
            low, c, fc = c, d, fd
            d = low + GOLDEN * (high - low)
            fd = function(d)
        else:
            high, d, fd = d, c, fc
            c = high - GOLDEN * (high - low)
            fc = function(c)
    x = 0.5 * (low + high)
    return x, function(x)


def lognormal_by_search(xs, nearest: bool) -> dict:
    """Slow cross-check: nested golden-section search over (mu, sigma).

    nearest=False: the rounded-up lognormal fitted by fit_lognormal.
    nearest=True: the other common discretisation, rounding to the nearest integer and conditioning on
    x >= 1: p(x) = [F(x + 1/2) - F(x - 1/2)] / [1 - F(1/2)].
    """
    def loglik(mu: float, sigma: float) -> float:
        logs = []
        for x in xs:
            if nearest:
                low, high = (math.log(x - 0.5) - mu) / sigma, (math.log(x + 0.5) - mu) / sigma
                p = normal_between(low, high)
            elif x == 1:
                p = 0.5 * math.erfc(mu / sigma / SQRT2)
            else:
                p = normal_between((math.log(x - 1) - mu) / sigma, (math.log(x) - mu) / sigma)
            if p <= 0.0:
                return -1e300
            logs.append(math.log(p))
        total = math.fsum(logs)
        if nearest:
            total -= len(xs) * math.log(0.5 * math.erfc((math.log(0.5) - mu) / sigma / SQRT2))
        return total

    best_mu = {}

    def profile(sigma: float) -> float:
        mu, value = golden_max(lambda m: loglik(m, sigma), -5.0, 10.0)
        best_mu[sigma] = mu
        return value

    sigma, value = golden_max(profile, 0.1, 6.0)
    return {"mu": best_mu[sigma], "sigma": sigma, "loglik": value}


# --------------------------------------------------------------------------- comparisons

def rank_line(values) -> dict:
    """Least-squares line of log10(count) on log10(rank) over the positive counts, largest first."""
    positive = sorted((v for v in values if v > 0), reverse=True)
    n = len(positive)
    u = [math.log10(rank) for rank in range(1, n + 1)]
    v = [math.log10(x) for x in positive]
    mean_u, mean_v = math.fsum(u) / n, math.fsum(v) / n
    suu = math.fsum((x - mean_u) ** 2 for x in u)
    svv = math.fsum((y - mean_v) ** 2 for y in v)
    suv = math.fsum((x - mean_u) * (y - mean_v) for x, y in zip(u, v))
    if svv == 0.0:
        return {"points": n, "slope": 0.0, "intercept": mean_v, "r_squared": None, "exponent_implied": None}
    slope = suv / suu
    return {"points": n, "slope": slope, "intercept": mean_v - slope * mean_u,
            "r_squared": suv * suv / (suu * svv), "exponent_implied": 1.0 - 1.0 / slope if slope < 0.0 else None}


def vuong(first, second) -> dict:
    """Normalised log-likelihood ratio of two fitted families on the same observations (Vuong 1989).

    R = sum of the per-observation differences; p = erfc(|R| / (sqrt(2 n) sd)), two-sided, with sd the
    standard deviation (divisor n) of the differences. A small p says the sign of R is unlikely to be chance.
    """
    n = len(first)
    differences = [x - y for x, y in zip(first, second)]
    ratio = math.fsum(differences)
    mean = ratio / n
    sd = math.sqrt(math.fsum((d - mean) ** 2 for d in differences) / n)
    if sd == 0.0:
        return {"llr": ratio, "sd": 0.0, "p_value": None}
    return {"llr": ratio, "sd": sd, "p_value": math.erfc(abs(ratio) / (math.sqrt(2.0 * n) * sd))}


def outcome(test: dict, pair: tuple[str, str], threshold: float) -> str:
    """Which family of the pair the sign of R favours, and whether the p-value makes that decisive."""
    if test["p_value"] is None or test["llr"] == 0.0:
        return "undefined"
    favoured = pair[0] if test["llr"] > 0.0 else pair[1]
    return f"{favoured}_{'decisive' if test['p_value'] < threshold else 'undecided'}"


def quantile(ordered: list, per_mille: int):
    """Nearest-rank quantile of a sorted list: an observed value, never an interpolation."""
    return ordered[max(0, (per_mille * len(ordered) + 999) // 1000 - 1)]


def spread(values: list, kind: str, low: int = 25, high: int = 975) -> dict:
    ordered = sorted(values)
    return {f"quantile_{low / 10:g}_percent": rnd(quantile(ordered, low), kind),
            "median": rnd(quantile(ordered, 500), kind),
            f"quantile_{high / 10:g}_percent": rnd(quantile(ordered, high), kind)}


def fit_tail(tail, x_min: int, bounds, with_lognormal: bool) -> dict:
    """Fit the families to one tail (all values >= x_min). Unrounded; used for data and for synthetic samples."""
    n = len(tail)
    sum_log = math.fsum(math.log(x) for x in tail)
    fits: dict = {"n": n, "sum_log": sum_log, "logpmf": {}}
    alpha = fit_power_law(sum_log / n, x_min, bounds)
    fits["alpha"] = alpha
    if alpha is not None:
        fits["logpmf"]["power_law"] = power_law_logpmf(tail, alpha, x_min)
    fits["exponential"] = fit_exponential(tail, x_min)
    fits["logpmf"]["exponential"] = exponential_logpmf(tail, fits["exponential"], x_min)
    if with_lognormal:
        fits["lognormal"] = fit_lognormal(tail)
        fits["logpmf"]["lognormal"] = fits["lognormal"]["logpmf"]
    fits["loglik"] = {family: math.fsum(values) for family, values in fits["logpmf"].items()}
    return fits


def pair_tests(fits: dict) -> dict:
    """The normalised ratio for every pair of fitted families: (first, second) -> test, R = first minus second."""
    return {pair: vuong(fits["logpmf"][pair[0]], fits["logpmf"][pair[1]])
            for pair in PAIRS if pair[0] in fits["logpmf"] and pair[1] in fits["logpmf"]}


def pair_name(pair: tuple[str, str]) -> str:
    return f"{pair[0]}_minus_{pair[1]}"


def stored_test(test: dict, pair: tuple[str, str], threshold: float) -> dict:
    p = test["p_value"]
    return {"llr": rnd(test["llr"], "loglik"), "sd_per_observation": rnd(test["sd"], "statistic"),
            "p_value": rnd(p, "p_value"), "p_value_below_0.0001": None if p is None else p < 0.0001,
            "favours": None if test["llr"] == 0.0 else pair[0] if test["llr"] > 0.0 else pair[1],
            "decisive": None if p is None else p < threshold}


# --------------------------------------------------------------------------- the observed counts

def describe_cut(values, x_min: int, bounds, threshold: float) -> dict:
    """Power law against exponential above one cut, discrete and continuous forms."""
    tail = sorted((v for v in values if v >= x_min), reverse=True)
    n = len(tail)
    fits = fit_tail(tail, x_min, bounds, with_lognormal=False)
    alpha = fits["alpha"]
    check("a finite discrete exponent exists for every listed cut", alpha is not None, f"x_min={x_min}")
    sum_log_ratio = math.fsum(math.log(x / x_min) for x in tail)
    alpha_continuous = 1.0 + n / sum_log_ratio
    mean = sum(tail) / n
    rate = 1.0 / (mean - x_min)
    continuous = {"power_law": n * math.log((alpha_continuous - 1.0) / x_min) - alpha_continuous * sum_log_ratio,
                  "exponential": n * math.log(rate) - n}
    step = 1e-4  # Fisher information of the discrete exponent: n times the second derivative of ln zeta
    upper, lower = hurwitz(alpha + step, x_min), hurwitz(alpha - step, x_min)
    information = n * (upper[1] / upper[0] - lower[1] / lower[0]) / (2.0 * step)
    test = pair_tests(fits)[PAIRS[0]]
    largest = tail[0]
    above = power_law_tail(alpha, x_min, largest + 1)
    exp_above = math.exp((largest + 1 - x_min) * fits["exponential"]["log_q"])
    return {
        "x_min": x_min,
        "values_kept": n,
        "values_set_aside": len(values) - n,
        "sum_ln_x": rnd(fits["sum_log"], "statistic"),
        "sum_ln_x_over_x_min": rnd(sum_log_ratio, "statistic"),
        "mean_of_kept_values": rnd(mean, "statistic"),
        "alpha_discrete": rnd(alpha, "exponent"),
        "alpha_continuous": rnd(alpha_continuous, "exponent"),
        "alpha_continuous_minus_discrete": rnd(alpha_continuous - alpha, "exponent"),
        "alpha_half_shift": rnd(1.0 + n / math.fsum(math.log(x / (x_min - 0.5)) for x in tail), "exponent"),
        "standard_error_discrete": rnd(1.0 / math.sqrt(information), "exponent"),
        "standard_error_simple": rnd((alpha_continuous - 1.0) / math.sqrt(n), "exponent"),
        "ks_distance": rnd(ks_power_law(tail, alpha, x_min), "statistic"),
        "loglik_power_law": rnd(fits["loglik"]["power_law"], "loglik"),
        "loglik_exponential": rnd(fits["loglik"]["exponential"], "loglik"),
        "exponential_q": rnd(math.exp(fits["exponential"]["log_q"]), "p_value"),
        "power_law_minus_exponential": stored_test(test, PAIRS[0], threshold),
        "continuous_forms": {
            "loglik_power_law": rnd(continuous["power_law"], "loglik"),
            "loglik_exponential": rnd(continuous["exponential"], "loglik"),
            "exponential_rate": rnd(rate, "p_value"),
            "llr": rnd(continuous["power_law"] - continuous["exponential"], "loglik"),
        },
        "largest_value": largest,
        "power_law_probability_above_largest": rnd(above, "p_value"),
        "power_law_probability_all_kept_values_at_most_largest": rnd((1.0 - above) ** n, "p_value"),
        "exponential_probability_above_largest": rnd(exp_above, "p_value"),
        "exponential_probability_all_kept_values_at_most_largest": rnd((1.0 - exp_above) ** n, "p_value"),
        "_unrounded": {"alpha": alpha, "ks": ks_power_law(tail, alpha, x_min), "mean": mean},
    }


def describe_set(values, bounds, threshold: float) -> dict:
    """Rank plot and three-family comparison over the positive values of one set of counts."""
    positive = sorted((v for v in values if v > 0), reverse=True)
    line = rank_line(values)
    fits = fit_tail(positive, 1, bounds, with_lognormal=True)
    check("the lognormal fit converged on every observed set", fits["lognormal"]["converged"])
    tests = pair_tests(fits)
    ranking = sorted(FAMILIES, key=lambda family: -fits["loglik"][family])
    return {
        "values": len(values), "zeros": len(values) - len(positive), "positive": len(positive),
        "sorted": sorted(values, reverse=True), "sum": sum(values),
        "rank_plot": {"points": line["points"], "slope": rnd(line["slope"], "statistic"),
                      "intercept": rnd(line["intercept"], "statistic"),
                      "r_squared": rnd(line["r_squared"], "statistic"),
                      "exponent_implied_by_slope": rnd(line["exponent_implied"], "exponent")},
        "x_min": 1,
        "power_law": {"alpha": rnd(fits["alpha"], "exponent"), "loglik": rnd(fits["loglik"]["power_law"], "loglik")},
        "exponential": {"mean": rnd(1 + fits["exponential"]["mean_excess"], "statistic"),
                        "q": rnd(math.exp(fits["exponential"]["log_q"]), "p_value"),
                        "loglik": rnd(fits["loglik"]["exponential"], "loglik")},
        "lognormal": {"mu": rnd(fits["lognormal"]["mu"], "exponent"), "sigma": rnd(fits["lognormal"]["sigma"], "exponent"),
                      "loglik": rnd(fits["loglik"]["lognormal"], "loglik")},
        "ranking_by_loglik": ranking,
        "pairs": {pair_name(pair): stored_test(test, pair, threshold) for pair, test in tests.items()},
        "_unrounded": {"fits": fits, "line": line},
    }


# --------------------------------------------------------------------------- synthetic samples

def simulate(draw, replicates: int, size: int, x_min: int, bounds, threshold: float, with_lognormal: bool,
             observed: dict) -> dict:
    """Fit every family to `replicates` synthetic samples of `size` values and tally the outcomes."""
    picks = {family: 0 for family in FAMILIES if with_lognormal or family != "lognormal"} | {"none": 0}
    pairs = {pair: {f"{pair[0]}_decisive": 0, f"{pair[0]}_undecided": 0, f"{pair[1]}_undecided": 0,
                    f"{pair[1]}_decisive": 0, "undefined": 0}
             for pair in PAIRS if with_lognormal or "lognormal" not in pair}
    alphas, r_squared, ks_values = [], [], []
    no_exponent = lognormal_not_converged = max_within = 0
    for _ in range(replicates):
        sample = [draw() for _ in range(size)]
        fits = fit_tail(sample, x_min, bounds, with_lognormal)
        if fits["alpha"] is None:
            no_exponent += 1
            picks["none"] += 1
            continue
        alphas.append(fits["alpha"])
        if with_lognormal:
            lognormal_not_converged += not fits["lognormal"]["converged"]
            r2 = rank_line(sample)["r_squared"]
            if r2 is not None:
                r_squared.append(r2)
        if observed.get("ks") is not None:
            ks_values.append(ks_power_law(sample, fits["alpha"], x_min))
        max_within += max(sample) <= observed["largest"]
        picks[max(fits["loglik"], key=lambda family: fits["loglik"][family])] += 1
        for pair, test in pair_tests(fits).items():
            pairs[pair][outcome(test, pair, threshold)] += 1
    result = {
        "replicates": replicates, "sample_size": size,
        "highest_likelihood": {family: share(count, replicates) for family, count in picks.items()},
        "pairs": {pair_name(pair): tally for pair, tally in pairs.items()},
        "alpha_discrete": spread(alphas, "exponent") | {"samples_without_a_finite_exponent": no_exponent},
        "largest_value_at_most_the_observed_largest": share(max_within, replicates),
    }
    if with_lognormal:
        ordered = sorted(r_squared)
        result["rank_plot_r_squared"] = spread(r_squared, "statistic", 50, 950) | {
            "samples": len(ordered),
            "at_least_the_observed_value": share(sum(v >= observed["r_squared"] for v in ordered), len(ordered)),
        } | {f"at_least_{level}": share(sum(v >= level for v in ordered), len(ordered)) for level in observed["levels"]}
        result["lognormal_fits_not_converged"] = lognormal_not_converged
    if ks_values:
        count = sum(v >= observed["ks"] for v in ks_values)
        result["ks_distance"] = spread(ks_values, "statistic", 50, 950) | {
            "observed": rnd(observed["ks"], "statistic"),
            "samples_at_least_the_observed_distance": share(count, len(ks_values)),
            "goodness_of_fit_p_value": rnd(count / len(ks_values), "p_value"),
        }
    return result


def right_and_wrong(tally: dict, mine: str, other: str) -> dict:
    """Re-express a pair tally from the point of view of the family that generated the samples."""
    total = sum(tally.values())
    return {"sign_right": share(tally[f"{mine}_decisive"] + tally[f"{mine}_undecided"], total),
            "sign_right_and_decisive": share(tally[f"{mine}_decisive"], total),
            "sign_wrong": share(tally[f"{other}_decisive"] + tally[f"{other}_undecided"], total),
            "sign_wrong_and_decisive": share(tally[f"{other}_decisive"], total),
            "undefined": tally["undefined"]}


def check_largest(result: dict, family: str, parameters: dict, x_min: int, largest: int) -> None:
    """Known answer: the share of samples whose largest value stays at or below `largest` has a closed form."""
    if family == "power_law":
        above = power_law_tail(parameters["alpha"], x_min, largest + 1)
    else:
        above = math.exp(-(largest + 1 - x_min) * math.log1p(1.0 / (parameters["mean"] - x_min)))
    exact = (1.0 - above) ** result["sample_size"]
    tally = result["largest_value_at_most_the_observed_largest"]
    tally["exact_probability"] = rnd(exact, "p_value")
    check("the share of samples whose largest value stays within the observed largest matches its closed form",
          abs(tally["count"] / tally["of"] - exact) <= 4.0 * math.sqrt(exact * (1.0 - exact) / tally["of"]) + 1.0 / tally["of"],
          f"{family}, n={result['sample_size']}: {tally['count']}/{tally['of']} against {exact}")


def bootstrap(values, cuts, settings: dict, bounds) -> dict:
    rng = random.Random(settings["seed"])
    n = len(values)
    exponents = {cut: [] for cut in cuts}
    skipped = {cut: 0 for cut in cuts}
    sizes = {cut: [] for cut in cuts}
    for _ in range(settings["replicates"]):
        sample = [values[int(rng.random() * n)] for _ in range(n)]
        for cut in cuts:
            tail = [v for v in sample if v >= cut]
            alpha = fit_power_law(math.fsum(math.log(x) for x in tail) / len(tail), cut, bounds) if len(tail) >= 2 else None
            if alpha is None:
                skipped[cut] += 1
            else:
                exponents[cut].append(alpha)
                sizes[cut].append(len(tail))
    return {
        "kind": "computed: nonparametric bootstrap of the recorded counts",
        "seed": settings["seed"], "replicates": settings["replicates"], "values_drawn_per_replicate": n,
        "by_x_min": [{"x_min": cut, "alpha_discrete": spread(exponents[cut], "exponent"),
                      "values_kept": {"smallest": min(sizes[cut]), "largest": max(sizes[cut])},
                      "replicates_without_a_finite_exponent": skipped[cut]} for cut in cuts],
    }


# --------------------------------------------------------------------------- self-checks and controls

def numeric_checks(bounds) -> None:
    check("zeta(2) = pi^2 / 6", abs(hurwitz(2.0, 1)[0] - math.pi ** 2 / 6.0) < 1e-12)
    check("zeta(4) = pi^4 / 90", abs(hurwitz(4.0, 1)[0] - math.pi ** 4 / 90.0) < 1e-12)
    check("zeta(3) = 1.2020569031595942", abs(hurwitz(3.0, 1)[0] - 1.2020569031595942) < 1e-12)
    check("zeta(2, 3) = pi^2 / 6 - 1 - 1/4", abs(hurwitz(2.0, 3)[0] - (math.pi ** 2 / 6.0 - 1.25)) < 1e-12)
    for s, q in ((1.3, 1), (2.21, 13), (7.6, 44)):
        direct = math.fsum((q + k) ** -s for k in range(20000))
        check("zeta pmf sums to 1: 20,000 terms plus the tail from the next term",
              abs((direct + hurwitz(s, q + 20000)[0]) / hurwitz(s, q)[0] - 1.0) < 1e-12, f"s={s}, q={q}")
        slope = (hurwitz(s + 1e-5, q)[0] - hurwitz(s - 1e-5, q)[0]) / 2e-5
        check("derivative of zeta agrees with a central difference", abs(slope / hurwitz(s, q)[1] - 1.0) < 1e-8)
    # hand case, continuous exponent: tail 2, 4, 8 above x_min = 2 -> sum ln(x / 2) = 3 ln 2 -> alpha = 1 + 1 / ln 2
    hand = 1.0 + 3.0 / math.fsum(math.log(x / 2) for x in (2, 4, 8))
    check("hand case: continuous exponent of 2, 4, 8 above 2 is 1 + 1 / ln 2", abs(hand - (1.0 + 1.0 / math.log(2.0))) < 1e-12)
    # hand case, exponential: 1, 2, 3 above x_min = 1 -> mean excess 1 -> q = 1/2 -> log-likelihood 6 ln(1/2)
    fit = fit_exponential([1, 2, 3], 1)
    check("hand case: exponential fit of 1, 2, 3 has q = 1/2 and log-likelihood 6 ln(1/2)",
          abs(math.exp(fit["log_q"]) - 0.5) < 1e-12 and abs(fit["loglik"] - 6.0 * math.log(0.5)) < 1e-12)
    # hand case, rank line: counts 720 / rank lie exactly on a line of slope -1
    line = rank_line([720, 360, 240, 180, 144, 120])
    check("hand case: counts 720 / rank give slope -1, R squared 1, implied exponent 2",
          abs(line["slope"] + 1.0) < 1e-12 and abs(line["r_squared"] - 1.0) < 1e-12 and abs(line["exponent_implied"] - 2.0) < 1e-12)
    # hand case, normalised ratio: differences 1, 2, 3 -> R = 6, sd = sqrt(2/3), p = erfc(3)
    test = vuong([1.0, 2.0, 3.0], [0.0, 0.0, 0.0])
    check("hand case: differences 1, 2, 3 give R = 6 and p = erfc(3)",
          abs(test["llr"] - 6.0) < 1e-12 and abs(test["p_value"] - math.erfc(3.0)) < 1e-15)
    # the discrete exponent maximises the likelihood, and the model's mean of ln x equals the sample's
    sample = [1, 1, 1, 2, 1, 3, 1, 5]
    mean_log = math.fsum(math.log(x) for x in sample) / len(sample)
    alpha = fit_power_law(mean_log, 1, bounds)

    def loglik(value: float) -> float:
        return math.fsum(power_law_logpmf(sample, value, 1))

    check("the fitted exponent beats its neighbours", loglik(alpha) > loglik(alpha + 1e-3) and loglik(alpha) > loglik(alpha - 1e-3))
    model_mean = math.fsum(math.log(k) * k ** -alpha for k in range(1, 200000)) / hurwitz(alpha, 1)[0]
    check("at the fitted exponent the model's mean of ln x is the sample's (sum over 200,000 terms)",
          abs(model_mean - mean_log) < 1e-5, f"{model_mean} vs {mean_log}")
    check("no finite exponent when every value equals x_min", fit_power_law(math.log(13), 13, bounds) is None)
    # Kolmogorov-Smirnov distance against a brute-force scan of every integer
    alpha, sample = 2.0, [1, 1, 2, 5, 9]
    zeta = hurwitz(alpha, 1)[0]
    brute, model = 0.0, 0.0
    for x in range(1, 12):
        brute = max(brute, abs(sum(v < x for v in sample) / 5 - model))
        model += x ** -alpha / zeta
        brute = max(brute, abs(sum(v <= x for v in sample) / 5 - model))
    check("Kolmogorov-Smirnov distance agrees with a scan of every integer", abs(ks_power_law(sample, alpha, 1) - brute) < 1e-12)
    # lognormal: probabilities sum to 1, derivatives agree with differences in all three branches
    mu, sigma = 2.78, 1.16
    total = math.fsum(math.exp(v) for v in lognormal_terms(mu / sigma, 1.0 / sigma, lognormal_intervals(range(1, 5001)))[6])
    check("rounded-up lognormal probabilities sum to 1 with the tail above 5,000",
          abs(total + 0.5 * math.erfc((math.log(5000) - mu) / sigma / SQRT2) - 1.0) < 1e-9)
    intervals = lognormal_intervals([1, 2, 7, 60, 10 ** 9, 10 ** 30])
    a, b, h = 1.1, 0.4, 1e-5
    base = lognormal_terms(a, b, intervals)
    up_a, down_a = lognormal_terms(a + h, b, intervals), lognormal_terms(a - h, b, intervals)
    up_b, down_b = lognormal_terms(a, b + h, intervals), lognormal_terms(a, b - h, intervals)
    numeric = ((up_a[0] - down_a[0]) / (2 * h), (up_b[0] - down_b[0]) / (2 * h), (up_a[1] - down_a[1]) / (2 * h),
               (up_b[1] - down_b[1]) / (2 * h), (up_b[2] - down_b[2]) / (2 * h))
    check("lognormal gradient and Hessian agree with central differences",
          all(abs(x - y) <= 1e-6 * max(1.0, abs(y)) for x, y in zip(numeric, base[1:6])), f"{numeric} vs {base[1:6]}")


def sampler_checks(settings: dict) -> dict:
    """Compare each sampler's frequencies with its probability formula (four standard errors allowed)."""
    rng = random.Random(settings["seed"])
    draws = settings["draws"]
    report = {"seed": settings["seed"], "draws_per_sampler": draws}

    def within(count: int, p: float) -> bool:
        return abs(count / draws - p) <= 4.0 * math.sqrt(p * (1.0 - p) / draws)

    alpha, x_min = settings["power_law"]["alpha"], settings["power_law"]["x_min"]
    sample = [draw_power_law(rng, alpha, x_min) for _ in range(draws)]
    zeta = hurwitz(alpha, x_min)[0]
    rows = []
    for x in (x_min, x_min + 1, x_min + 5):
        p = x ** -alpha / zeta
        rows.append({"x": x, "drawn": sample.count(x), "probability": rnd(p, "p_value")})
        check("power-law sampler matches its probabilities", within(sample.count(x), p), f"x={x}")
    p = power_law_tail(alpha, x_min, 50)
    rows.append({"x": "50 or more", "drawn": sum(v >= 50 for v in sample), "probability": rnd(p, "p_value")})
    check("power-law sampler matches its probabilities", within(sum(v >= 50 for v in sample), p), "x>=50")
    report["power_law"] = settings["power_law"] | {"frequencies": rows}

    mean, x_min = settings["exponential"]["mean"], settings["exponential"]["x_min"]
    sample = [draw_exponential(rng, mean, x_min) for _ in range(draws)]
    q = (mean - x_min) / (mean - x_min + 1.0)
    rows = []
    for x in (x_min, x_min + 3):
        p = (1.0 - q) * q ** (x - x_min)
        rows.append({"x": x, "drawn": sample.count(x), "probability": rnd(p, "p_value")})
        check("exponential sampler matches its probabilities", within(sample.count(x), p), f"x={x}")
    report["exponential"] = settings["exponential"] | {"frequencies": rows}

    mu, sigma = settings["lognormal"]["mu"], settings["lognormal"]["sigma"]
    sample = [draw_lognormal(rng, mu, sigma) for _ in range(draws)]
    rows = []
    for x in (1, 3, 10):
        p = math.exp(lognormal_terms(mu / sigma, 1.0 / sigma, lognormal_intervals([x]))[0])
        rows.append({"x": x, "drawn": sample.count(x), "probability": rnd(p, "p_value")})
        check("lognormal sampler matches its probabilities", within(sample.count(x), p), f"x={x}")
    report["lognormal"] = settings["lognormal"] | {"frequencies": rows}
    return report


# --------------------------------------------------------------------------- transfer task

def transfer_task(settings: dict, bounds: tuple, threshold: float) -> dict:
    """Closed-form answers for the learner task (continuous forms, computable by hand), and the discrete fits."""
    values = settings["downloads"]
    ordered = sorted(values, reverse=True)
    positive = [v for v in ordered if v > 0]
    ties = sorted({v for v in positive if positive.count(v) > 1}, reverse=True)
    cuts = []
    for x_min in settings["x_min_values"]:
        tail = [v for v in ordered if v >= x_min]
        n = len(tail)
        sum_log_ratio = math.fsum(math.log(x / x_min) for x in tail)
        alpha = 1.0 + n / sum_log_ratio
        mean = sum(tail) / n
        rate = 1.0 / (mean - x_min)
        loglik_power = n * math.log((alpha - 1.0) / x_min) - alpha * sum_log_ratio
        loglik_exp = n * math.log(rate) - n
        needed = ((alpha - 1.0) / settings["standard_error_target"]) ** 2
        fits = fit_tail(tail, x_min, bounds, with_lognormal=False)
        cuts.append({
            "x_min": x_min, "values_kept": n, "values_set_aside": len(values) - n,
            "sum_ln_x_over_x_min": rnd(sum_log_ratio, "statistic"),
            "alpha_continuous": rnd(alpha, "exponent"),
            "standard_error_simple": rnd((alpha - 1.0) / math.sqrt(n), "exponent"),
            "sum_of_kept_values": sum(tail), "mean_of_kept_values": rnd(mean, "statistic"),
            "exponential_rate": rnd(rate, "p_value"),
            "loglik_power_law_continuous": rnd(loglik_power, "loglik"),
            "loglik_exponential_continuous": rnd(loglik_exp, "loglik"),
            "llr_power_law_minus_exponential": rnd(loglik_power - loglik_exp, "loglik"),
            "family_with_the_higher_likelihood": "power_law" if loglik_power > loglik_exp else "exponential",
            "values_needed_for_the_standard_error_target_before_rounding_up": rnd(needed, "statistic"),
            "values_needed_for_the_standard_error_target": math.ceil(needed),
            "discrete_forms": {
                "alpha_discrete": rnd(fits["alpha"], "exponent"),
                "loglik_power_law": rnd(fits["loglik"]["power_law"], "loglik"),
                "loglik_exponential": rnd(fits["loglik"]["exponential"], "loglik"),
                "power_law_minus_exponential": stored_test(pair_tests(fits)[PAIRS[0]], PAIRS[0], threshold),
            },
        })
    check("transfer task: kept plus set-aside values add up", all(c["values_kept"] + c["values_set_aside"] == len(values) for c in cuts))
    return {
        "kind": "synthetic: hypothetical registry from scenarios.json, continuous closed forms, with the discrete fits "
                "of the lesson under discrete_forms",
        "formulas": {
            "alpha": "1 + n / sum of ln(x / x_min)",
            "standard_error": "(alpha - 1) / sqrt(n)",
            "exponential_rate": "1 / (mean - x_min)",
            "loglik_power_law": "n ln((alpha - 1) / x_min) - alpha * sum of ln(x / x_min)",
            "loglik_exponential": "n ln(rate) - n",
        },
        "values": len(values), "sorted": ordered, "zeros": len(values) - len(positive), "positive": len(positive),
        "tied_positive_values": ties, "standard_error_target": settings["standard_error_target"],
        "by_x_min": cuts,
    }


# --------------------------------------------------------------------------- the analysis

OTHER_OF = {"power_law": "exponential", "exponential": "power_law"}


def strip(node):
    """Drop the unrounded working values before writing."""
    if isinstance(node, dict):
        return {key: strip(value) for key, value in node.items() if not key.startswith("_")}
    if isinstance(node, list):
        return [strip(value) for value in node]
    return node


def observed_counts(snapshot: dict, bounds: tuple, threshold: float) -> dict:
    """The recorded counts: the rank table, the counts not measured by git grep, and the three sets that are fitted."""
    entries = snapshot["citation_counts"]
    recorded = [entry["citation_count"] for entry in entries]
    measured = [entry["citation_count"] for entry in entries if entry["citation_source"] is not None]
    before = [entry["count_before_git_grep"] for entry in entries]
    check("every count is a non-negative integer", all(isinstance(v, int) and not isinstance(v, bool) and v >= 0
                                                       for v in recorded + before))
    check("the snapshot holds one count per artifact", len({entry["artifact"] for entry in entries}) == len(entries))
    order = sorted(range(len(entries)), key=lambda i: (-recorded[i], i))
    rank_size = [{"rank": rank, "artifact": entries[i]["artifact"], "citation_count": recorded[i],
                  "measured_by_git_grep": entries[i]["citation_source"] is not None,
                  "tied": recorded.count(recorded[i]) > 1}
                 for rank, i in enumerate(order, 1)]
    not_measured = [{"artifact": entry["artifact"], "citation_count": entry["citation_count"],
                     "count_before_git_grep": entry["count_before_git_grep"], "citation_paths": entry["citation_paths"]}
                    for entry in entries if entry["citation_source"] is None]
    check("measured and unmeasured counts are all the counts", len(measured) + len(not_measured) == len(recorded))
    check("a count without a citation source has no citation path and kept its hand-typed value",
          all(not entry["citation_paths"] and entry["citation_count"] == entry["count_before_git_grep"] for entry in not_measured))

    sets = {"recorded": describe_set(recorded, bounds, threshold),
            "measured_by_git_grep": describe_set(measured, bounds, threshold),
            "before_git_grep": describe_set(before, bounds, threshold)}
    fitted = sets["recorded"]
    check("zeros plus positive counts are all the counts", all(s["zeros"] + s["positive"] == s["values"] for s in sets.values()))
    check("the rank plot uses the positive counts only", all(s["rank_plot"]["points"] == s["positive"] for s in sets.values()))
    check("the rank table sums to the total", sum(row["citation_count"] for row in rank_size) == fitted["sum"])
    check("the three families are fitted to the same values",
          all(len(v) == fitted["positive"] for v in fitted["_unrounded"]["fits"]["logpmf"].values()))
    return {"recorded": recorded, "measured": measured, "before": before, "rank_size": rank_size,
            "not_measured": not_measured, "sets": sets, "fitted": fitted,
            "positive": sorted((v for v in recorded if v > 0), reverse=True)}


def cut_table(counts: dict, settings: dict, bounds: tuple, threshold: float) -> dict:
    """One power-law fit per listed cut, the cut with the smallest distance, and the tail cut."""
    recorded, positive, fitted = counts["recorded"], counts["positive"], counts["fitted"]
    listed = [x for x in sorted(set(positive)) if sum(v >= x for v in positive) >= settings["min_tail_listed"]]
    cuts = [describe_cut(recorded, x_min, bounds, threshold) for x_min in listed]
    check("the cut at 1 keeps every positive count", cuts[0]["x_min"] == 1 and cuts[0]["values_kept"] == fitted["positive"])
    check("the cut table and the three-family fit agree at x_min = 1",
          cuts[0]["alpha_discrete"] == fitted["power_law"]["alpha"] and cuts[0]["loglik_power_law"] == fitted["power_law"]["loglik"]
          and cuts[0]["loglik_exponential"] == fitted["exponential"]["loglik"])
    eligible = [cut for cut in cuts if cut["values_kept"] >= settings["min_tail_for_tail_cut"]]
    return {"cuts": cuts, "primary": cuts[0],
            "by_ks": min(cuts, key=lambda cut: cut["_unrounded"]["ks"]),
            "tail_cut": min(eligible, key=lambda cut: cut["_unrounded"]["ks"])}


def lognormal_rounded_to_nearest(counts: dict) -> dict:
    """Check the Newton fit against a search, then fit the other common discretisation of the lognormal."""
    positive = counts["positive"]
    search = lognormal_by_search(positive, nearest=False)
    newton = counts["fitted"]["_unrounded"]["fits"]["lognormal"]
    check("the Newton fit of the lognormal agrees with a nested golden-section search",
          abs(search["loglik"] - newton["loglik"]) < 1e-6 and abs(search["mu"] - newton["mu"]) < 1e-3
          and abs(search["sigma"] - newton["sigma"]) < 1e-3, f"{search} vs {newton['mu']}, {newton['sigma']}, {newton['loglik']}")
    nearest = lognormal_by_search(positive, nearest=True)
    return {
        "definition": "p(x) = [F(x + 1/2) - F(x - 1/2)] / [1 - F(1/2)], fitted by nested golden-section search",
        "mu": rnd(nearest["mu"], "loglik"), "sigma": rnd(nearest["sigma"], "loglik"),
        "loglik": rnd(nearest["loglik"], "loglik"),
        "loglik_minus_rounded_up": rnd(nearest["loglik"] - newton["loglik"], "loglik"),
    }


def sampler(family: str, rng: random.Random, parameters: dict, x_min: int):
    """A function that draws one value of the family from the generator's own random stream."""
    if family == "power_law":
        return lambda: draw_power_law(rng, parameters["alpha"], x_min)
    if family == "exponential":
        return lambda: draw_exponential(rng, parameters["mean"], x_min)
    return lambda: draw_lognormal(rng, parameters["mu"], parameters["sigma"])


def simulate_all_positive(block: dict, counts: dict, primary: dict, levels: list, bounds: tuple, threshold: float) -> dict:
    """Samples of as many values as there are positive counts, drawn from each fitted family."""
    fitted, positive = counts["fitted"], counts["positive"]
    generators = block["generators"]
    fits = fitted["_unrounded"]["fits"]
    check("generator parameters are the fitted values rounded to 2 decimals",
          abs(generators["power_law"]["alpha"] - fits["alpha"]) <= 0.005
          and abs(generators["lognormal"]["mu"] - fits["lognormal"]["mu"]) <= 0.005
          and abs(generators["lognormal"]["sigma"] - fits["lognormal"]["sigma"]) <= 0.005
          and generators["exponential"]["mean"] == 1 + fits["exponential"]["mean_excess"]
          and block["sample_size"] == fitted["positive"] and block["x_min"] == 1)
    observed = {"largest": positive[0], "r_squared": fitted["_unrounded"]["line"]["r_squared"], "levels": levels}
    all_positive = {}
    for family in FAMILIES:
        parameters = generators[family]
        draw = sampler(family, random.Random(parameters["seed"]), parameters, block["x_min"])
        context = observed | {"ks": primary["_unrounded"]["ks"] if family == "power_law" else None}
        result = simulate(draw, block["replicates"], block["sample_size"], block["x_min"], bounds, threshold, True, context)
        check("every synthetic sample is assigned to one family or to none",
              sum(entry["count"] for entry in result["highest_likelihood"].values()) == block["replicates"])
        check("every pairwise tally covers all samples with a finite exponent",
              all(sum(pair.values()) == block["replicates"] - result["alpha_discrete"]["samples_without_a_finite_exponent"]
                  for pair in result["pairs"].values()))
        result["generator"] = {"family": family} | parameters
        result["generator_has_the_highest_likelihood"] = result["highest_likelihood"][family]
        result["power_law_against_exponential_for_this_generator"] = (
            right_and_wrong(result["pairs"]["power_law_minus_exponential"], family, OTHER_OF[family])
            if family in OTHER_OF else None)
        if family in OTHER_OF:
            check_largest(result, family, parameters, block["x_min"], positive[0])
        all_positive[family] = result
    return all_positive


def simulate_tails(block: dict, tail_cut: dict, bounds: tuple, threshold: float) -> list:
    """Tails above the tail cut, drawn from a power law and from an exponential, at each sample size."""
    generators = block["generators"]
    check("the tail simulation uses the tail cut and its fitted values",
          block["x_min"] == tail_cut["x_min"] and block["sample_sizes"][0] == tail_cut["values_kept"]
          and abs(generators["power_law"]["alpha"] - tail_cut["_unrounded"]["alpha"]) <= 0.005
          and generators["exponential"]["mean"] == tail_cut["_unrounded"]["mean"])
    tail_runs = []
    for family in ("power_law", "exponential"):
        parameters = generators[family]
        draw = sampler(family, random.Random(parameters["seed"]), parameters, block["x_min"])
        for size in block["sample_sizes"]:
            context = {"largest": tail_cut["largest_value"],
                       "ks": tail_cut["_unrounded"]["ks"] if family == "power_law" and size == tail_cut["values_kept"] else None}
            result = simulate(draw, block["replicates"], size, block["x_min"], bounds, threshold, False, context)
            tally = result.pop("pairs")["power_law_minus_exponential"]
            result.pop("highest_likelihood")
            check_largest(result, family, parameters, block["x_min"], tail_cut["largest_value"])
            tail_runs.append({"generator": {"family": family} | parameters} | result
                             | {"power_law_against_exponential": right_and_wrong(tally, family, OTHER_OF[family])})
    control = [run for run in tail_runs if run["sample_size"] == block["sample_sizes"][-1]]
    check("known-answer control: at the largest sample size the median exponent of power-law samples is within 0.1 of the truth",
          abs(control[0]["alpha_discrete"]["median"] - generators["power_law"]["alpha"]) < 0.1)
    check("known-answer control: at the largest sample size the comparison finds the generator in at least 95% of samples",
          all(run["power_law_against_exponential"]["sign_right"]["percent"] >= 95.0 for run in control))
    return tail_runs


def goodness_of_fit_before(block: dict, counts: dict, bounds: tuple, threshold: float) -> dict:
    """The goodness-of-fit test of the recorded counts, run on the hand-typed counts of the last run before git grep."""
    fits = counts["sets"]["before_git_grep"]["_unrounded"]["fits"]
    positive = sorted((v for v in counts["before"] if v > 0), reverse=True)
    check("the generator for the hand-typed counts is their fitted exponent rounded to 2 decimals",
          abs(block["alpha"] - fits["alpha"]) <= 0.005 and block["sample_size"] == len(positive) and block["x_min"] == 1)
    observed = {"largest": positive[0], "ks": ks_power_law(positive, fits["alpha"], block["x_min"])}
    draw = sampler("power_law", random.Random(block["seed"]), block, block["x_min"])
    result = simulate(draw, block["replicates"], block["sample_size"], block["x_min"], bounds, threshold, False, observed)
    return {"kind": "synthetic reference distribution for an observed distance, as in goodness_of_fit",
            "x_min": block["x_min"], "values": len(positive),
            "generator": {"family": "power_law", "seed": block["seed"], "alpha": block["alpha"]}} | result["ks_distance"]


def share_rule(rule: dict, counts: dict) -> dict:
    """The specification's detection rule: do the largest counts of the top share of artifacts exceed a share of citations?"""
    top, above = rule["top_percent_of_artifacts"], rule["more_than_percent_of_citations"]

    def present(values: list, k: int) -> bool:
        return 100 * sum(sorted(values, reverse=True)[:k]) > above * sum(values)

    check("share rule, hand case: 2 of 10 artifacts holding 61 of 100 citations pass, holding 60 of 100 do not",
          top == 20 and present([31, 30] + [5] * 7 + [4], 2) and not present([30, 30] + [5] * 8, 2))

    def apply(values: list) -> dict:
        ordered = sorted(values, reverse=True)
        n, total = len(ordered), sum(ordered)
        sizes = sorted({n * top // 100, -(-n * top // 100)})  # the top share rounded down and up to whole artifacts
        verdicts = {present(ordered, k) for k in sizes}
        return {"artifacts": n, "citations": total, "artifacts_in_the_top_share": rnd(n * top / 100, "statistic")} | {
            f"largest_{k}": share(sum(ordered[:k]), total) for k in sizes} | {
            "power_law_present_by_this_rule": verdicts.pop() if len(verdicts) == 1 else None}

    return {"kind": "computed: the detection rule of the specification applied to two sets of counts",
            "rule": rule,
            "note": "the top share of artifacts is rarely a whole number of artifacts: the rule is applied to the "
                    "count rounded down and rounded up, and gives a verdict only when both agree",
            "recorded": apply(counts["recorded"]), "before_git_grep": apply(counts["before"])}


def negative_controls(snapshot: dict, counts: dict, cuts: list, all_positive: dict, tail_gof: dict) -> dict:
    """Results that could pass on nothing, next to the same procedure where it must not return nothing."""
    mentions = snapshot["power_law_mentions"]
    power_law_top = {family: all_positive[family]["highest_likelihood"]["power_law"] for family in FAMILIES}
    check("control: the power law has the highest likelihood in some power-law samples", power_law_top["power_law"]["count"] > 0)
    check("control: the goodness-of-fit counter moves on the tail",
          tail_gof["samples_at_least_the_observed_distance"]["count"] > 0)
    check("control: the search that finds no power law in the lessons finds some in the department record",
          len(mentions["department_record"]["strings"]) > 0)
    check("every listed cut accounts for all the counts",
          all(c["values_kept"] + c["values_set_aside"] == len(counts["recorded"]) for c in cuts))
    return {
        "kind": "results that could be empty by construction, shown next to a case where the same procedure returns something",
        "no_exponential_or_lognormal_sample_has_the_power_law_on_top": {
            "samples_with_the_power_law_on_top_by_generator": power_law_top,
            "control": "the same rule puts the power law on top in the power-law samples counted here",
        },
        "no_power_law_sample_is_as_far_from_its_fit_as_the_recorded_counts": {
            "all_positive_counts": all_positive["power_law"]["ks_distance"]["samples_at_least_the_observed_distance"],
            "control_tail": tail_gof["samples_at_least_the_observed_distance"],
        },
        "the_comparison_does_not_always_favour_the_exponential": {
            "power_law_samples_where_the_sign_favours_the_power_law":
                all_positive["power_law"]["power_law_against_exponential_for_this_generator"]["sign_right"],
            "hand_typed_counts_llr_power_law_minus_exponential":
                counts["sets"]["before_git_grep"]["pairs"]["power_law_minus_exponential"]["llr"],
        },
        "no_line_of_the_published_lessons_mentions_a_power_law": {
            "lines_matching_by_lesson": {entry["path"]: entry["lines_matching"] for entry in mentions["published_lessons"]},
            "control_strings_matching_in_the_department_record": len(mentions["department_record"]["strings"]),
        },
    }


def observed_report(snapshot: dict, counts: dict) -> dict:
    """The observed section of the results."""
    fitted, positive, measured = counts["fitted"], counts["positive"], counts["measured"]
    return {
        "kind": "observed: copied or counted from observed-input.json",
        "run": snapshot["quality_trend"]["latest_run"],
        "counts": len(counts["recorded"]), "zeros": fitted["zeros"], "positive": fitted["positive"], "sum": fitted["sum"],
        "largest": positive[0], "second_largest": positive[1],
        "tied_positive_values": sorted({v for v in positive if positive.count(v) > 1}, reverse=True),
        "rank_size": counts["rank_size"],
        "measured_by_git_grep": {"counts": len(measured), "zeros": measured.count(0),
                                 "positive": sum(v > 0 for v in measured)},
        "not_measured_by_git_grep": counts["not_measured"],
        "shared_citation_paths": snapshot["shared_citation_paths"],
        "before_git_grep": {"run": snapshot["quality_trend"]["last_run_before_git_grep_counts"]["timestamp"],
                            "sorted": sorted(counts["before"], reverse=True)},
        "power_law_mentions": snapshot["power_law_mentions"],
        "psy_001_compounding_dimension": snapshot["psy_001_compounding_dimension"],
        "specification_rule": snapshot["specification_rule"],
    }


def power_law_fit_report(scenarios: dict, bounds: tuple, table: dict) -> dict:
    """The power-law section of the results: one row per cut and the two selected cuts."""
    settings = scenarios["power_law_fit"]
    cuts, by_ks, tail_cut = table["cuts"], table["by_ks"], table["tail_cut"]
    return {
        "kind": "computed",
        "form": scenarios["families"]["power_law"],
        "search_bounds": list(bounds),
        "primary_x_min": settings["primary_x_min"],
        "by_x_min": cuts,
        "smallest_ks_distance": {"rule": "the listed cut with the smallest Kolmogorov-Smirnov distance",
                                 "x_min": by_ks["x_min"], "values_kept": by_ks["values_kept"],
                                 "alpha_discrete": by_ks["alpha_discrete"], "ks_distance": by_ks["ks_distance"]},
        "tail_cut": {"rule": settings["tail_cut_rule"], "min_values": settings["min_tail_for_tail_cut"],
                     "x_min": tail_cut["x_min"], "values_kept": tail_cut["values_kept"],
                     "alpha_discrete": tail_cut["alpha_discrete"], "ks_distance": tail_cut["ks_distance"]},
        "alpha_discrete_range_over_listed_cuts": [min(c["alpha_discrete"] for c in cuts), max(c["alpha_discrete"] for c in cuts)],
    }


def simulation_report(block: dict, counts: dict, all_positive: dict) -> dict:
    """The section on synthetic samples of all positive counts, with the tallies across generators."""
    fitted = counts["fitted"]
    on_top = sum(all_positive[family]["highest_likelihood"][family]["count"] for family in FAMILIES)
    top_observed = fitted["ranking_by_loglik"][0]
    return {
        "kind": "synthetic: seeded samples from the three fitted families",
        "note": block["note"],
        "observed_r_squared": fitted["rank_plot"]["r_squared"], "observed_largest": counts["positive"][0],
        "generator_has_the_highest_likelihood_overall": share(on_top, len(FAMILIES) * block["replicates"]),
        "family_on_top_for_the_recorded_counts": top_observed,
        "samples_with_that_family_on_top_by_generator": {
            family: all_positive[family]["highest_likelihood"][top_observed] for family in FAMILIES},
        "by_generator": all_positive,
    }


def analyze(snapshot: dict, scenarios: dict) -> dict:
    DEC.update({key[:-len("_decimals")]: value for key, value in scenarios["rounding"].items() if key.endswith("_decimals")})
    settings = scenarios["power_law_fit"]
    bounds = (settings["alpha_search_from"], settings["alpha_search_to"])
    threshold = scenarios["decisive_p_value"]
    numeric_checks(bounds)

    counts = observed_counts(snapshot, bounds, threshold)
    fitted, sets = counts["fitted"], counts["sets"]
    table = cut_table(counts, settings, bounds, threshold)
    tail_cut = table["tail_cut"]
    nearest = lognormal_rounded_to_nearest(counts)
    all_positive = simulate_all_positive(scenarios["simulation_all_positive"], counts, table["primary"],
                                         scenarios["rank_plot"]["r_squared_thresholds"], bounds, threshold)
    tail_runs = simulate_tails(scenarios["simulation_tail"], tail_cut, bounds, threshold)
    tail_gof = next(run for run in tail_runs if "ks_distance" in run)["ks_distance"]
    boot = bootstrap(counts["recorded"], [1, tail_cut["x_min"]], scenarios["bootstrap"], bounds)
    controls = negative_controls(snapshot, counts, table["cuts"], all_positive, tail_gof)
    before_gof = goodness_of_fit_before(scenarios["goodness_of_fit_before_git_grep"], counts, bounds, threshold)

    return strip({
        "module_id": snapshot["module_id"],
        "rounding": "exponents to %d decimals, log-likelihoods to %d, slopes, R squared and distances to %d, "
                    "probabilities and p-values to %d, percentages to %d; quantiles are observed values (nearest rank)"
                    % (DEC["exponent"], DEC["loglik"], DEC["statistic"], DEC["p_value"], DEC["percent"]),
        "source": {"repository": snapshot["source"]["repository"], "commit": snapshot["source"]["commit"],
                   "files_read_by_extract": len(snapshot["source"]["files"]),
                   "run": snapshot["quality_trend"]["latest_run"]["timestamp"]},
        "observed": observed_report(snapshot, counts),
        "share_rule": share_rule(snapshot["specification_rule"]["detection_rule"], counts),
        "rank_plot": {
            "kind": "computed",
            "definition": "least-squares line of log10(count) on log10(rank), positive counts only, largest first, "
                          "tied counts on consecutive ranks; exponent implied by the slope = 1 + 1 / |slope|",
            "zeros_that_cannot_be_plotted": fitted["zeros"],
        } | fitted["rank_plot"],
        "power_law_fit": power_law_fit_report(scenarios, bounds, table),
        "families_on_all_positive_counts": {
            "kind": "computed",
            "definitions": scenarios["families"],
            "decisive_p_value": threshold,
        } | {key: fitted[key] for key in ("x_min", "positive", "power_law", "exponential", "lognormal", "ranking_by_loglik", "pairs")} | {
            "lognormal_rounded_to_nearest_instead": nearest,
        },
        "goodness_of_fit": {
            "kind": "synthetic reference distribution for an observed distance",
            "method": "Kolmogorov-Smirnov distance of the recorded counts to their fitted power law, compared with the "
                      "distances of synthetic power-law samples of the same size, each refitted; x_min is held fixed",
            "rule": "a power law is ruled out when p <= %s" % threshold,
            "all_positive_counts": {"x_min": 1, "values": fitted["positive"]} | all_positive["power_law"]["ks_distance"],
            "tail": {"x_min": tail_cut["x_min"], "values": tail_cut["values_kept"]} | tail_gof,
        },
        "bootstrap": boot,
        "simulation_all_positive": simulation_report(scenarios["simulation_all_positive"], counts, all_positive),
        "simulation_tail": {
            "kind": "synthetic: seeded tails above the tail cut",
            "note": scenarios["simulation_tail"]["note"],
            "x_min": scenarios["simulation_tail"]["x_min"], "decisive_p_value": threshold,
            "runs": tail_runs,
        },
        "sensitivity": {
            "kind": "computed: the same fit on two other sets of counts",
            "measured_by_git_grep": {"what": "the latest run without the two hand-entered counts"} | sets["measured_by_git_grep"],
            "before_git_grep": {"what": "the same artifacts in the last run before the counts were measured with git grep "
                                        "(hand-typed counts)"} | sets["before_git_grep"] | {"goodness_of_fit": before_gof},
        },
        "negative_controls": controls,
        "sampler_checks": sampler_checks(scenarios["sampler_checks"]),
        "transfer_task": transfer_task(scenarios["transfer_task"], bounds, threshold),
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
