#!/usr/bin/env python3
"""PSY-013 analysis: exact intervals and exact tests on four small counts.

Reads observed-input.json (written by extract.py) and scenarios.json, never
the repository, and writes results.json. Every probability is an exact sum
over a finite list of outcomes, computed with fractions; no random number is
drawn.

Run from the repository root:
    python -I scripts/streeling_fixtures/psychohistory/psy-013/analyze.py
    python -I scripts/streeling_fixtures/psychohistory/psy-013/analyze.py --check
"""

from __future__ import annotations

import argparse
import copy
import itertools
import json
import re
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from fractions import Fraction
from math import comb, prod
from pathlib import Path

# This program lives under scripts/ (CONTRIBUTING.md: no executable code outside scripts/); its data stays
# under state/streeling/fixtures/. FIXTURE_FILE is the path the program would have next to that data.
FIXTURE_FILE = (Path(__file__).resolve().parents[4]
                / "state/streeling/fixtures/psychohistory/psy-013" / Path(__file__).name)

HERE = FIXTURE_FILE.parent
DECIMALS = 6
CHECKS: dict[str, int] = {}  # self-check -> times evaluated


def check(name: str, condition: bool, detail: str = "") -> None:
    """A self-check that can fail: abort instead of writing a wrong result."""
    if not condition:
        raise AssertionError(f"self-check failed: {name}" + (f" ({detail})" if detail else ""))
    CHECKS[name] = CHECKS.get(name, 0) + 1


def num(value: Fraction) -> float:
    return round(float(value), DECIMALS)


def exact(value: Fraction) -> dict:
    """A probability or share with its unrounded fraction."""
    return {"exact": str(value), "value": num(value)}


# --- exact binomial interval (Clopper-Pearson) -------------------------------

def binomial_pmf(n: int, k: int, p: Fraction) -> Fraction:
    return comb(n, k) * p ** k * (1 - p) ** (n - k)


def at_least(n: int, k: int, p: Fraction) -> Fraction:
    """P(X >= k) for X ~ Binomial(n, p)."""
    return sum((binomial_pmf(n, j, p) for j in range(k, n + 1)), Fraction(0))


def at_most(n: int, k: int, p: Fraction) -> Fraction:
    """P(X <= k) for X ~ Binomial(n, p)."""
    return sum((binomial_pmf(n, j, p) for j in range(0, k + 1)), Fraction(0))


def bisect(increasing, target: Fraction, steps: int) -> Fraction:
    """The point of [0, 1] where an increasing function reaches the target."""
    low, high = Fraction(0), Fraction(1)
    for _ in range(steps):
        middle = (low + high) / 2
        if increasing(middle) < target:
            low = middle
        else:
            high = middle
    return (low + high) / 2


def exact_interval(k: int, n: int, confidence: Fraction, steps: int) -> tuple[Fraction, Fraction]:
    """Clopper-Pearson interval: the rates p that the count k does not reject.

    Lower bound: the p at which P(X >= k) equals (1 - confidence) / 2.
    Upper bound: the p at which P(X <= k) equals (1 - confidence) / 2.
    """
    half = (1 - confidence) / 2
    lower = Fraction(0) if k == 0 else bisect(lambda p: at_least(n, k, p), half, steps)
    upper = Fraction(1) if k == n else 1 - bisect(lambda q: at_most(n, k, 1 - q), half, steps)
    if k > 0:
        check("interval: the lower bound puts (1 - confidence)/2 on 'this count or more'",
              abs(float(at_least(n, k, lower) - half)) < 1e-12)
    if k < n:
        check("interval: the upper bound puts (1 - confidence)/2 on 'this count or fewer'",
              abs(float(at_most(n, k, upper) - half)) < 1e-12)
    check("interval: lower bound <= observed share <= upper bound", lower <= Fraction(k, n) <= upper)
    return lower, upper


def interval_row(k: int, n: int, confidence: Fraction, steps: int) -> dict:
    lower, upper = exact_interval(k, n, confidence, steps)
    return {"caught": k, "total": n, "share": exact(Fraction(k, n)), "lower": num(lower), "upper": num(upper),
            "width": num(upper - lower)}


# --- exact tests --------------------------------------------------------------

def fisher(x1: int, n1: int, x2: int, n2: int) -> dict:
    """Fisher's exact test for two independent samples, x1 of n1 against x2 of n2.

    With both margins fixed, the count in the first sample is hypergeometric.
    Two-sided: total probability of the tables no more probable than the
    observed one. One-sided ("improvement"): the second sample's share is the
    larger, that is, the first sample holds x1 or fewer of the successes.
    """
    total, successes = n1 + n2, x1 + x2
    support = range(max(0, n1 - (total - successes)), min(n1, successes) + 1)
    denominator = comb(total, n1)
    pmf = {x: Fraction(comb(successes, x) * comb(total - successes, n1 - x), denominator) for x in support}
    check("Fisher: the hypergeometric probabilities sum to 1", sum(pmf.values()) == 1)
    observed = pmf[x1]
    return {
        "table": [[x1, n1 - x1], [x2, n2 - x2]],
        "probability_of_the_observed_table": exact(observed),
        "one_sided_improvement": exact(sum(p for x, p in pmf.items() if x <= x1)),
        "one_sided_decline": exact(sum(p for x, p in pmf.items() if x >= x1)),
        "two_sided": exact(sum(p for p in pmf.values() if p <= observed)),
    }


def sign_test(gained: int, lost: int) -> dict:
    """Exact test for paired yes/no results (the exact form of McNemar's test).

    Only the cases whose result changed carry information. If no real change
    happened, each of them is as likely to have changed one way as the other.
    """
    changed = gained + lost
    if changed == 0:
        return {"gained": 0, "lost": 0, "changed": 0, "one_sided_improvement": exact(Fraction(1)),
                "two_sided": exact(Fraction(1))}
    tail = lambda k: Fraction(sum(comb(changed, j) for j in range(k, changed + 1)), 2 ** changed)  # noqa: E731
    return {"gained": gained, "lost": lost, "changed": changed, "one_sided_improvement": exact(tail(gained)),
            "two_sided": exact(min(Fraction(1), 2 * tail(max(gained, lost))))}


def holm(pvalues: list[Fraction]) -> list[Fraction]:
    """Holm's step-down adjusted p-values, in the order given."""
    order = sorted(range(len(pvalues)), key=lambda index: pvalues[index])
    adjusted, running = [Fraction(0)] * len(pvalues), Fraction(0)
    for rank, index in enumerate(order):
        running = max(running, min(Fraction(1), (len(pvalues) - rank) * pvalues[index]))
        adjusted[index] = running
    return adjusted


def family(counts: list[tuple[int, int]], comparisons: list[dict], alpha: Fraction) -> dict:
    """Fisher tests for a declared family of comparisons, with Bonferroni and Holm."""
    rows, pvalues = [], []
    for comparison in comparisons:
        (x1, n1), (x2, n2) = counts[comparison["from"]], counts[comparison["to"]]
        test = fisher(x1, n1, x2, n2)
        pvalues.append(Fraction(test["two_sided"]["exact"]))
        row = {"name": comparison["name"], "from": f"{x1}/{n1}", "to": f"{x2}/{n2}"}
        row.update(test)
        rows.append(row)
    threshold = alpha / len(comparisons)
    for row, p, adjusted in zip(rows, pvalues, holm(pvalues)):
        row["bonferroni_adjusted"] = num(min(Fraction(1), len(comparisons) * p))
        row["holm_adjusted"] = num(adjusted)
        row["two_sided_below_significance_level"] = p < alpha
        row["two_sided_below_bonferroni_threshold"] = p < threshold
        row["holm_adjusted_below_significance_level"] = adjusted < alpha
        check("Bonferroni: 'p below alpha / m' and 'm x p below alpha' agree",
              (p < threshold) == (min(Fraction(1), len(comparisons) * p) < alpha))
    return {"tests_in_the_family": len(comparisons), "significance_level": exact(alpha),
            "bonferroni_threshold": exact(threshold), "comparisons": rows}


def conditional_tables(sizes: list[int], total: int):
    """Every way to spread `total` successes over groups of the given sizes, with
    its probability when all orderings of the pooled results are equally likely."""
    denominator = comb(sum(sizes), total)
    for counts in itertools.product(*(range(size + 1) for size in sizes)):
        if sum(counts) == total:
            yield counts, Fraction(prod(comb(size, count) for size, count in zip(sizes, counts)), denominator)


def several_groups(counts: list[tuple[int, int]]) -> dict:
    """Exact tests on k groups with the total number of successes fixed.

    Homogeneity (Freeman-Halton): total probability of the tables no more
    probable than the observed one. Trend (exact Cochran-Armitage with scores
    0, 1, 2, ...): the statistic is sum(position x successes).
    """
    caught, sizes = [x for x, _ in counts], [n for _, n in counts]
    total = sum(caught)
    tables = list(conditional_tables(sizes, total))
    check("several groups: the table probabilities sum to 1", sum(p for _, p in tables) == 1)
    observed = next(p for table, p in tables if list(table) == caught)
    score = lambda table: sum(position * count for position, count in enumerate(table))  # noqa: E731
    expected = Fraction(total, sum(sizes)) * sum(position * size for position, size in enumerate(sizes))
    distance = abs(score(caught) - expected)
    return {
        "counts": [f"{x}/{n}" for x, n in counts],
        "pooled_share": exact(Fraction(total, sum(sizes))),
        "tables_enumerated": len(tables),
        "homogeneity_p": exact(sum(p for _, p in tables if p <= observed)),
        "trend_statistic": score(caught),
        "trend_statistic_expected_if_no_trend": exact(expected),
        "trend_p_one_sided_rising": exact(sum(p for table, p in tables if score(table) >= score(caught))),
        "trend_p_two_sided": exact(sum(p for table, p in tables if abs(score(table) - expected) >= distance)),
    }


def familywise(counts: list[tuple[int, int]], comparisons: list[dict], alpha: Fraction) -> dict:
    """How often a family of two-sided Fisher tests on the same counts gives a false positive.

    Null model: the observed total of successes fell at random among all the
    trials (every arrangement equally likely), so no cycle differs from another.
    Each arrangement gives one table of counts; the same counts enter several
    tests, so the tests are not independent.
    """
    sizes, total = [n for _, n in counts], sum(x for x, _ in counts)
    threshold = alpha / len(comparisons)
    cache: dict[tuple[int, int, int, int], Fraction] = {}

    def pvalue(x1: int, n1: int, x2: int, n2: int) -> Fraction:
        key = (x1, n1, x2, n2)
        if key not in cache:
            cache[key] = Fraction(fisher(x1, n1, x2, n2)["two_sided"]["exact"])
        return cache[key]

    mass = any_alpha = any_threshold = Fraction(0)
    single = [Fraction(0)] * len(comparisons)
    for table, probability in conditional_tables(sizes, total):
        pvalues = [pvalue(table[c["from"]], sizes[c["from"]], table[c["to"]], sizes[c["to"]]) for c in comparisons]
        mass += probability
        any_alpha += probability * (min(pvalues) < alpha)
        any_threshold += probability * (min(pvalues) < threshold)
        single = [share + probability * (p < alpha) for share, p in zip(single, pvalues)]
    check("family-wise: the arrangement probabilities sum to 1", mass == 1)
    check("family-wise: Bonferroni keeps the family-wise rate at or below the significance level", any_threshold <= alpha)
    check("family-wise: each exact test alone is at or below its nominal level", all(share <= alpha for share in single))
    check("family-wise: the family's rate is at least that of its largest member and at most their sum",
          max(single) <= any_alpha <= sum(single))
    return {
        "tests_in_the_family": len(comparisons),
        "caught_in_all": total, "trials_in_all": sum(sizes),
        "if_the_tests_were_independent": exact(1 - (1 - alpha) ** len(comparisons)),
        "bonferroni_bound_on_the_uncorrected_family": exact(min(Fraction(1), len(comparisons) * alpha)),
        "each_test_alone_below_significance_level": [{"name": c["name"], "share_of_arrangements": num(share)}
                                                     for c, share in zip(comparisons, single)],
        "at_least_one_below_significance_level": num(any_alpha),
        "bonferroni_threshold": exact(threshold),
        "at_least_one_below_bonferroni_threshold": num(any_threshold),
    }


def binomial_weights(n: int, rate: Fraction) -> tuple[list[int], int]:
    """Binomial(n, rate) probabilities as integers over one common denominator."""
    a, b = rate.numerator, rate.denominator
    weights = [comb(n, k) * a ** k * (b - a) ** (n - k) for k in range(n + 1)]
    check("fixed rate: the binomial probabilities sum to 1", sum(weights) == b ** n)
    return weights, b ** n


def rising_run(n: int, rate: Fraction, observed: list[int]) -> dict:
    """Three independent Binomial(n, rate) counts: how often do they rise?"""
    w, d = binomial_weights(n, rate)
    triples = list(itertools.product(range(n + 1), repeat=3))
    strictly = sum(w[a] * w[b] * w[c] for a, b, c in triples if a < b < c)
    weakly = sum(w[a] * w[b] * w[c] for a, b, c in triples if a <= b <= c)
    falling = sum(w[a] * w[b] * w[c] for a, b, c in triples if a > b > c)
    check("fixed rate: a strict rise is as likely as a strict fall", strictly == falling)
    return {"rate": exact(rate), "strictly_rising": num(Fraction(strictly, d ** 3)),
            "rising_or_level": num(Fraction(weakly, d ** 3)),
            "exactly_the_observed_sequence": num(Fraction(prod(w[k] for k in observed), d ** len(observed)))}


# --- the policy's bands and trend rule ------------------------------------------

def policy_bands(thresholds: list[dict], regimes: list[dict]) -> list[dict]:
    """Bands of R from the policy's thresholds, lowest first, with PSY-002's regime names."""
    parsed = []
    for threshold in thresholds:
        operator, value = threshold["range"].split()
        check("policy: every threshold is '>= x' or '< x'", operator in (">=", "<"))
        parsed.append((operator, Fraction(value), threshold["name"]))
    cuts = sorted((value, name) for operator, value, name in parsed if operator == ">=")
    under = [(value, name) for operator, value, name in parsed if operator == "<"]
    check("policy: one '<' threshold, at the lowest '>=' cut", len(under) == 1 and under[0][0] == cuts[0][0])
    bands = [{"name": under[0][1], "from": Fraction(0), "below": cuts[0][0]}]
    for index, (value, name) in enumerate(cuts):
        bands.append({"name": name, "from": value, "below": cuts[index + 1][0] if index + 1 < len(cuts) else None})
    check("the policy's bands and PSY-002's regimes use the same cut points",
          [(band["from"], band["below"]) for band in bands]
          == [(Fraction(regime["from"]), None if regime["below"] is None else Fraction(regime["below"])) for regime in regimes])
    for band, regime in zip(bands, regimes):
        band["psy_002_regime"] = regime["name"]
    return bands


def band_of(score: Fraction, bands: list[dict]) -> dict:
    return next(band for band in bands if score >= band["from"] and (band["below"] is None or score < band["below"]))


def bands_spanned(lower: Fraction, upper: Fraction, bands: list[dict]) -> list[dict]:
    return [band for band in bands if upper >= band["from"] and (band["below"] is None or lower < band["below"])]


def trend_label(scores: list[Fraction]) -> str:
    """The policy's trend rule, as read in scenarios.json: latest score against the mean of the two before it."""
    previous = scores[:-1][-2:]
    if not previous:
        return "stable"
    mean = sum(previous) / len(previous)
    return "improving" if scores[-1] > mean else "degrading" if scores[-1] < mean else "stable"


def trend_rule_by_chance(n: int, rate: Fraction) -> dict:
    """Independent Binomial(n, rate) cycles: how often does the trend rule say 'improving'?"""
    w, d = binomial_weights(n, rate)
    counts = range(n + 1)
    label = {"improving": 0, "degrading": 0, "stable": 0}
    for a, b, c in itertools.product(counts, repeat=3):
        label["improving" if 2 * c > a + b else "degrading" if 2 * c < a + b else "stable"] += w[a] * w[b] * w[c]
    check("trend rule: the three labels' probabilities sum to 1", sum(label.values()) == d ** 3)
    check("trend rule: counts and shares give the same label",
          all(trend_label([Fraction(a, n), Fraction(b, n), Fraction(c, n)])
              == ("improving" if 2 * c > a + b else "degrading" if 2 * c < a + b else "stable")
              for a, b, c in itertools.product(range(0, n + 1, 3), repeat=3)))
    twice = sum(w[a] * w[b] * w[c] * w[e] for a, b, c, e in itertools.product(counts, repeat=4)
                if 2 * c > a + b and 2 * e > b + c)
    return {"rate": exact(rate), "improving": num(Fraction(label["improving"], d ** 3)),
            "degrading": num(Fraction(label["degrading"], d ** 3)), "stable": num(Fraction(label["stable"], d ** 3)),
            "improving_in_two_cycles_running": num(Fraction(twice, d ** 4))}


# --- the observed history -----------------------------------------------------

def parse_utc(value: str) -> datetime:
    return datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)


def hours_between(earlier: str, later: str) -> float:
    return (parse_utc(later) - parse_utc(earlier)).total_seconds() / 3600


def half_up(numerator: int, denominator: int, scale: int) -> int:
    """numerator / denominator x scale, rounded to a whole number, halves up, in integer arithmetic."""
    return (2 * scale * numerator + denominator) // (2 * denominator)


def describe_history(records: list[dict], scenarios: dict) -> dict:
    """Recount each cycle from its own detail. Returns facts; asserts nothing."""
    caught_statuses = set(scenarios["caught_statuses"]["statuses"])
    level_keys = {key: value for key, value in scenarios["level_keys"].items() if key != "note"}
    first_names = [row["injection"] for row in records[0]["injections"]]
    cycles = []
    for index, record in enumerate(records):
        rows = record["injections"]
        statuses: dict[str, int] = {}
        per_level: dict[str, int] = {}
        for row in rows:
            statuses[row["status"]] = statuses.get(row["status"], 0) + 1
            per_level[row["level"]] = per_level.get(row["level"], 0) + 1
        implied = sum(Fraction(str(record["level_scores"][level_keys[level]])) * count for level, count in per_level.items())
        by_rule = sum(row["status"] in caught_statuses for row in rows)
        total, caught = record["injections_total"], record["injections_caught"]
        rounded = half_up(caught, total, 100) / 100
        cycles.append({
            "cycle_id": record["cycle_id"],
            "timestamp": record["timestamp"],
            "hours_since_previous_cycle": None if index == 0 else hours_between(records[index - 1]["timestamp"], record["timestamp"]),
            "recorded": {"injections_total": total, "injections_caught": caught,
                         "injections_missed": record["injections_missed"], "overall_score": record["overall_score"],
                         "trend": record["trend"]},
            "caught_plus_missed_equals_total": caught + record["injections_missed"] == total,
            "injection_rows": len(rows),
            "share_caught": exact(Fraction(caught, total)),
            "share_rounded_to_2_decimals": rounded,
            "recorded_score_is_the_rounded_share": rounded == record["overall_score"],
            "status_counts": statuses,
            "caught_by_status_rule": by_rule,
            "caught_implied_by_level_scores": exact(implied),
            "injections_per_level": per_level,
            "levels": len(record["level_scores"]),
            "levels_scored_1": sum(score == 1 for score in record["level_scores"].values()),
            "levels_scored_between_0_and_1": sorted(level for level, score in record["level_scores"].items() if 0 < score < 1),
            "distinct_expected_detectors": len({row["expected_detector"] for row in rows}),
            "expected_detectors_that_name_analyzeLolli": sum("analyzeLolli" in row["expected_detector"] for row in rows),
            "status_rule_reproduces_recorded_count": by_rule == caught,
            "level_scores_reproduce_recorded_count": implied == caught,
            "metafixes_recorded": len(record["metafixes_applied"]),
        })
    names = [sorted(row["injection"] for row in record["injections"]) for record in records]
    levels_of = [{row["injection"]: row["level"] for row in record["injections"]} for record in records]
    return {
        "cycles": cycles,
        "injection_set": {
            "names_identical_in_all_cycles": all(listing == names[0] for listing in names),
            "levels_identical_in_all_cycles": all(mapping == levels_of[0] for mapping in levels_of),
            "listed_in_the_same_order_in_all_cycles":
                all([row["injection"] for row in record["injections"]] == first_names for record in records),
            "injections": [{"position_in_first_cycle": position, "level": row["level"], "injection": row["injection"]}
                           for position, row in enumerate(records[0]["injections"], 1)],
        },
    }


def status_rules(records: list[dict], which: list[int]) -> list[dict]:
    """Every set of status labels that, counted as 'caught', reproduces the recorded
    caught count of the cycles listed in `which`."""
    labels = []
    for record in records:
        for row in record["injections"]:
            if row["status"] not in labels:
                labels.append(row["status"])
    rules = []
    for size in range(len(labels) + 1):
        for subset in itertools.combinations(labels, size):
            counts = [sum(row["status"] in subset for row in record["injections"]) for record in records]
            if all(counts[index] == records[index]["injections_caught"] for index in which):
                rules.append({"statuses_counted_as_caught": list(subset), "caught_per_cycle": counts})
    return rules


def transitions(records: list[dict], earlier: int, later: int, caught_statuses: set[str]) -> dict:
    """Per injection, caught or missed in two cycles (paired data)."""
    first_position = {row["injection"]: position for position, row in enumerate(records[0]["injections"], 1)}
    before = {row["injection"]: row["status"] in caught_statuses for row in records[earlier]["injections"]}
    gained, lost, both, neither = [], [], 0, 0
    for row in records[later]["injections"]:
        now, was = row["status"] in caught_statuses, before[row["injection"]]
        entry = {"position_in_first_cycle": first_position[row["injection"]], "level": row["level"],
                 "injection": row["injection"]}
        if now and not was:
            gained.append(entry)
        elif was and not now:
            lost.append(entry)
        elif now:
            both += 1
        else:
            neither += 1
    return {"caught_in_both": both, "missed_in_both": neither, "missed_then_caught": gained, "caught_then_missed": lost}


def fix_targets(records: list[dict], caught_statuses: set[str]) -> list[dict]:
    """What each record says was changed before it, next to the injections whose status changed."""
    first = [row["injection"] for row in records[0]["injections"]]
    out = []
    for index in range(1, len(records)):
        record = records[index]
        step = transitions(records, index - 1, index, caught_statuses)
        changed = step["missed_then_caught"] + step["caught_then_missed"]
        text = " ".join([record["note"]] + [fix["fix"] for fix in record["metafixes_applied"]])
        numbers = sorted({int(number) for number in re.findall(r"injection #(\d+)", text)})
        improved = sorted({fix["level_improved"] for fix in record["metafixes_applied"]})
        out.append({
            "cycle_id": record["cycle_id"],
            "metafixes_recorded": len(record["metafixes_applied"]),
            "levels_named_by_the_metafixes": improved,
            "levels_of_the_injections_whose_status_changed": sorted({entry["level"] for entry in changed}),
            "injection_numbers_named_in_the_record": numbers,
            "injections_at_those_positions_in_the_first_cycle": [first[number - 1] for number in numbers],
            "injections_whose_status_changed": [entry["injection"] for entry in changed],
            "note": record["note"],
        })
    return out


def held_out(reference: tuple[int, int], sizes: list[int], alpha: Fraction) -> list[dict]:
    """Imaginary fresh sets compared with a reference count by a two-sided Fisher test."""
    out = []
    for size in sizes:
        below = [k for k in range(size + 1) if Fraction(k, size) < Fraction(*reference)]
        pvalues = {k: Fraction(fisher(reference[0], reference[1], k, size)["two_sided"]["exact"]) for k in range(size + 1)}
        differing = [k for k in below if pvalues[k] < alpha]
        largest = max(differing) if differing else None
        above = [k for k in range(size + 1) if Fraction(k, size) > Fraction(*reference) and pvalues[k] < alpha]
        row = {"held_out_size": size,
               "largest_caught_count_that_differs": largest,
               "its_share": None if largest is None else exact(Fraction(largest, size)),
               "its_two_sided_p": None if largest is None else num(pvalues[largest]),
               "two_sided_p_one_count_higher": None if largest is None else num(pvalues[largest + 1]),
               "a_higher_share_can_differ": bool(above)}
        if size == reference[1]:
            row["two_sided_p_by_caught_count"] = {str(k): num(pvalues[k]) for k in range(size + 1)}
        out.append(row)
    return out


def all_caught_needed(bands: list[dict], confidence: Fraction, steps: int) -> list[dict]:
    """Smallest fresh set that, caught in full, puts the interval's lower bound at or above each band's lower cut."""
    half = (1 - confidence) / 2
    out = []
    for band in bands:
        cut = band["from"]
        if cut == 0:
            continue
        size = 1
        while cut ** size > half:
            size += 1
        check("zero misses: the exact interval agrees with the closed form on the smallest sufficient size",
              exact_interval(size, size, confidence, steps)[0] >= cut
              and (size == 1 or exact_interval(size - 1, size - 1, confidence, steps)[0] < cut))
        out.append({"band": band["name"], "lower_cut": exact(cut), "smallest_set_caught_in_full": size,
                    "cut_to_that_power": num(cut ** size), "cut_to_one_power_less": num(cut ** (size - 1))})
    return out


# --- the analysis choices and the recounted history ---------------------------

@dataclass
class Setup:
    """What every section needs: the choices of scenarios.json and the history as recounted."""
    confidence: Fraction
    alpha: Fraction
    steps: int                # bisection steps of the exact interval
    caught_statuses: set      # status labels counted as caught
    records: list             # the history's records, as extracted
    red_team: list            # the three red-team cycle files, as extracted
    definitions: dict         # glossary entry, metric policy, README status line
    comparisons: list         # the declared family of comparisons
    smaller: list             # the same family without one comparison
    cycles: list              # one recounted row per record (describe_history)
    injection_set: dict
    counts: list              # (caught, total) per cycle, as recorded
    total: int                # injections per cycle
    last: int                 # index of the last cycle


def setup(snapshot: dict, scenarios: dict) -> Setup:
    """Read the analysis choices and recount the history. Asserts nothing."""
    if scenarios["rounding"]["probability_decimals"] != DECIMALS:
        raise ValueError("scenarios.json rounding does not match analyze.py")
    records = snapshot["history"]["records"]
    comparisons = scenarios["test_family"]["comparisons"]
    facts = describe_history(records, scenarios)
    counts = [(cycle["recorded"]["injections_caught"], cycle["recorded"]["injections_total"]) for cycle in facts["cycles"]]
    return Setup(
        confidence=Fraction(scenarios["confidence_level"]), alpha=Fraction(scenarios["significance_level"]),
        steps=scenarios["interval_bisection_steps"], caught_statuses=set(scenarios["caught_statuses"]["statuses"]),
        records=records, red_team=snapshot["red_team_cycles"], definitions=snapshot["definitions"],
        comparisons=comparisons,
        smaller=[c for c in comparisons if c["name"] in scenarios["test_family"]["smaller_family"]["comparisons"]],
        cycles=facts["cycles"], injection_set=facts["injection_set"], counts=counts, total=counts[0][1],
        last=len(records) - 1)


# --- the two reports ----------------------------------------------------------------

def baseline_report(snapshot: dict, s: Setup) -> dict:
    """observed.baseline_report: the chaos-test report dated like the first cycle, cross-checked against the history."""
    records, first, total = s.records, s.records[0]["injections"], s.total
    baseline = snapshot["reports"]["baseline"]
    card = baseline["scorecard"]
    verdicts: dict[str, int] = {}
    for row in baseline["injections"]:
        verdicts[row["verdict"]] = verdicts.get(row["verdict"], 0) + 1
    check("baseline report: its table reproduces its scorecard",
          (verdicts.get("YES", 0), verdicts.get("PARTIAL", 0) + verdicts.get("YES (specification-level)", 0),
           verdicts.get("DELAYED", 0), verdicts.get("GAP", 0), sum(verdicts.values()))
          == (card["detected_full"], card["detected_partial_or_spec_only"], card["delayed_detection"], card["undetected"],
              card["injections"]))
    check("baseline report: its two scores are 'full' and 'full + partial or spec-only' over the injections",
          (card["immediate"]["caught"], card["including_spec_level"]["caught"])
          == (card["detected_full"], card["detected_full"] + card["detected_partial_or_spec_only"])
          and card["immediate"]["total"] == card["including_spec_level"]["total"] == card["injections"])
    check("baseline report: its quoted decimals are its fractions rounded to two decimals",
          all(f"{half_up(card[key]['caught'], card[key]['total'], 100) / 100:.2f}" == card[key]["quoted"]
              for key in ("immediate", "including_spec_level")))
    check("baseline report: one row per injection of the history, numbered in the order of the first cycle",
          len(baseline["injections"]) == len(first)
          and all(row["level"].lower() == first[row["number"] - 1]["level"].lower() for row in baseline["injections"]))
    check("baseline report: it names the three injection files that extract.py pinned",
          sorted(baseline["artifacts_tested"]) == sorted(snapshot["source"]["injection_files_pinned_but_not_parsed"]))
    return {
        "path": baseline["path"], "date": baseline["date"], "purpose": baseline["purpose"],
        "injection_files": baseline["artifacts_tested"],
        "verdict_counts": verdicts,
        "scorecard": card,
        "first_history_cycle": {"cycle_id": records[0]["cycle_id"], "timestamp": records[0]["timestamp"],
                                "recorded_caught": records[0]["injections_caught"]},
        "three_scores_of_the_same_set_on_that_date": [
            {"source": "history, first cycle", "caught": records[0]["injections_caught"], "total": total},
            {"source": "chaos-test report, 'immediate'", "caught": card["immediate"]["caught"], "total": total},
            {"source": "chaos-test report, 'including spec-level'", "caught": card["including_spec_level"]["caught"],
             "total": total},
        ],
        "intervals": {"immediate": interval_row(card["immediate"]["caught"], total, s.confidence, s.steps),
                      "including_spec_level": interval_row(card["including_spec_level"]["caught"], total, s.confidence,
                                                           s.steps)},
    }


def cycle_report(snapshot: dict, s: Setup) -> dict:
    """observed.cycle_report: the report of one later cycle, which states the rule for 'caught', against the history."""
    first = s.records[0]["injections"]
    by_id = {record["cycle_id"]: record for record in s.records}
    detail = snapshot["reports"]["cycle"]
    check("cycle report: its cycle is one of the history's", detail["cycle_id"] in by_id)
    record = by_id[detail["cycle_id"]]
    status_in_history = {row["injection"]: row["status"] for row in record["injections"]}
    check("cycle report: one row per injection, with the level and status the history records for that cycle",
          len(detail["injections"]) == len(first)
          and all(row["level"].lower() == first[row["number"] - 1]["level"].lower()
                  and row["status"] == status_in_history[first[row["number"] - 1]["injection"]]
                  for row in detail["injections"]))
    yes = sorted({row["status"] for row in detail["injections"] if row["caught"] == "YES"})
    no = sorted({row["status"] for row in detail["injections"] if row["caught"] == "NO"})
    check("cycle report: 'Caught? YES' for exactly the statuses that scenarios.json counts as caught",
          set(yes) == s.caught_statuses and not set(yes) & set(no))
    summary = detail["summary"]
    previous = by_id[summary["previous_cycle_id"]]
    check("cycle report: its summary counts are the history's recorded counts",
          (summary["caught"], summary["total"]) == (record["injections_caught"], record["injections_total"])
          and (summary["previous_caught"], summary["previous_total"])
          == (previous["injections_caught"], previous["injections_total"])
          and sum(row["caught"] == "YES" for row in detail["injections"]) == summary["caught"])
    check("cycle report: its poison source is one of the pinned injection files, with the history's injection count",
          detail["poison_source"]["path"] in snapshot["source"]["injection_files_pinned_but_not_parsed"]
          and detail["poison_source"]["injections"] == record["injections_total"])
    quoted = re.search(r"the score is (\d\.\d+)", detail["automated_only_statement"])
    check("cycle report: the automated-only statement quotes a score", quoted is not None)
    automated = sum(row["status"] == "automated" for row in detail["injections"])
    total = record["injections_total"]
    return {
        "path": detail["path"], "date": detail["date"], "cycle_id": detail["cycle_id"],
        "poison_source": detail["poison_source"],
        "statuses_marked_caught": yes, "statuses_marked_not_caught": no,
        "summary_line": summary["line"],
        "policy_enforceable_definition": detail["policy_enforceable_definition"],
        "automated_only_statement": detail["automated_only_statement"],
        "automated_only_score_quoted": quoted.group(1),
        "rows_with_status_automated": automated,
        "automated_only_share_recounted": exact(Fraction(automated, total)),
        "automated_only_share_recounted_rounded_to_2_decimals": half_up(automated, total, 100) / 100,
        "quoted_score_equals_the_recount": float(quoted.group(1)) == half_up(automated, total, 100) / 100,
    }


# --- cases worked by hand, and negative controls ------------------------------------

def hand_computed_cases(scenarios: dict) -> None:
    """Check the test functions against the cases worked by hand in scenarios.json."""
    cases = scenarios["hand_computed_cases"]
    tea = cases["tea_tasting"]
    (a, b), (c, d) = tea["table"]
    result = fisher(a, a + b, c, c + d)
    check("hand-computed case: Fisher's tea-tasting table gives 17/70 one-sided and 34/70 two-sided",
          (result["one_sided_decline"]["exact"], result["two_sided"]["exact"]) == (tea["one_sided"], tea["two_sided"]))
    step = cases["first_step"]
    (a, b), (c, d) = step["table"]
    result = fisher(a, a + b, c, c + d)
    check("hand-computed case: 0 of 11 against 7 of 11 gives C(15,11)/C(22,11) one-sided, twice that two-sided",
          Fraction(result["one_sided_improvement"]["exact"]) == Fraction(step["one_sided"]) == Fraction(comb(15, 11), comb(22, 11))
          and Fraction(result["two_sided"]["exact"]) == 2 * Fraction(step["one_sided"]))
    check("hand-computed case: Holm on (0.01, 0.04, 0.03) gives (0.03, 0.06, 0.06)",
          holm([Fraction(1, 100), Fraction(4, 100), Fraction(3, 100)]) == [Fraction(3, 100), Fraction(6, 100), Fraction(6, 100)])
    check("hand-computed case: sign test, 7 changes all one way, gives 1/128 one-sided and 1/64 two-sided",
          (sign_test(7, 0)["one_sided_improvement"]["exact"], sign_test(7, 0)["two_sided"]["exact"]) == ("1/128", "1/64"))
    for case in scenarios["trend_rule"]["hand_computed_cases"]:
        check("hand-computed case: the trend rule on the short series of scenarios.json",
              trend_label([Fraction(score) for score in case["scores"]]) == case["label"])


def negative_controls(records: list[dict], scenarios: dict, base: dict) -> dict:
    """Plant a defect in a copy of the history and confirm each counter sees it."""
    caught_statuses = set(scenarios["caught_statuses"]["statuses"])
    last = len(records) - 1

    planted = copy.deepcopy(records)
    victim = next(row for row in planted[last]["injections"] if row["status"] in caught_statuses)
    victim["status"] = scenarios["imaginary_cases"]["one_regression"]["new_status"]
    regressed = transitions(planted, last - 1, last, caught_statuses)
    check("negative control: an injection marked missed again is counted as caught-then-missed",
          len(regressed["caught_then_missed"]) == base["lost_in_last_step"] + 1)

    renamed = copy.deepcopy(records)
    renamed[2]["injections"][0]["injection"] += " (renamed)"
    renamed_facts = describe_history(renamed, scenarios)["injection_set"]
    check("negative control: one renamed injection breaks 'names identical in all cycles'",
          base["names_identical"] and not renamed_facts["names_identical_in_all_cycles"])

    consistent = copy.deepcopy(records)
    consistent[1]["injections_caught"] = base["cycle_2_caught_by_status_rule"]
    rules_before = status_rules(records, list(range(len(records))))
    rules_after = status_rules(consistent, list(range(len(records))))
    check("negative control: the search for a status rule finds one when the recorded count allows it",
          len(rules_before) == 0 and len(rules_after) >= 1)

    rescored = copy.deepcopy(records)
    rescored[1]["overall_score"] = 0.7
    check("negative control: a score that is not the rounded share is reported",
          not describe_history(rescored, scenarios)["cycles"][1]["recorded_score_is_the_rounded_share"])

    lowered = [Fraction(str(record["overall_score"])) for record in records]
    lowered[last] = lowered[last - 1] - Fraction(1, 10)
    check("negative control: a last score below the two before it is not labelled 'improving'",
          base["last_trend_label"] == "improving" and trend_label(lowered) == "degrading")
    return {
        "regression_planted_in": {"cycle_id": records[last]["cycle_id"], "injection": victim["injection"]},
        "caught_then_missed_in_the_last_step_before_and_after": [base["lost_in_last_step"], len(regressed["caught_then_missed"])],
        "names_identical_before_and_after_renaming_one_injection":
            [base["names_identical"], renamed_facts["names_identical_in_all_cycles"]],
        "status_rules_found_before_and_after_setting_cycle_2_to_its_status_count": [len(rules_before), len(rules_after)],
        "planted_score_reported_as_inconsistent": True,
        "trend_label_of_the_last_cycle_before_and_after_lowering_its_score": [base["last_trend_label"], trend_label(lowered)],
    }


# --- the transfer task: the red-team series ------------------------------------

def recount_red_team(cycles: list[dict]) -> list[dict]:
    """Per red-team cycle: the verdict counts of its scenario list next to those of its own summary."""
    recount = []
    for cycle in cycles:
        listed = {"pass": 0, "partial": 0, "fail": 0}
        for row in cycle["scenarios"]:
            listed[row["verdict"].lower()] += 1
        total = cycle["scenarios_evaluated"]
        summary = cycle["results_summary"]
        recount.append({
            "cycle": cycle["cycle"], "id": cycle["id"], "evaluator": cycle["evaluator"],
            "scenarios_evaluated": total, "scenario_rows": len(cycle["scenarios"]),
            "summary_counts": summary, "counts_in_the_scenario_list": listed,
            "summary_matches_the_list": summary == listed,
            "score_percentage_recorded": cycle["score_percentage"],
            "pass_share_from_summary": exact(Fraction(summary["pass"], total)),
            "pass_percent_from_summary_rounded": half_up(summary["pass"], total, 100),
            "pass_share_from_list": exact(Fraction(listed["pass"], total)),
            "pass_percent_from_list_rounded": half_up(listed["pass"], total, 100),
            "trigger": cycle["trigger"], "fixes_applied_listed": len(cycle["fixes_applied"]),
        })
    check("transfer: every cycle lists as many scenarios as it says it evaluated",
          all(row["scenario_rows"] == row["scenarios_evaluated"] for row in recount))
    check("transfer: summary counts add up to the scenarios evaluated",
          all(sum(row["summary_counts"].values()) == row["scenarios_evaluated"] for row in recount))
    return recount


def transfer_readings(recount: list[dict], source: str, task: dict, confidence: Fraction, alpha: Fraction,
                      steps: int) -> dict:
    """Questions 2, 3 and 5 of the learner task from one source of PASS counts: the lists or the summaries."""
    pairs = [(row[source]["pass"], row["scenarios_evaluated"]) for row in recount]
    intervals = []
    for row, (k, n) in zip(recount, pairs):
        entry = {"cycle": row["cycle"]}
        entry.update(interval_row(k, n, confidence, steps))
        intervals.append(entry)
    return {
        "pass_counts": [f"{k}/{n}" for k, n in pairs],
        "q2_intervals": intervals,
        "q2_first_and_last_intervals_overlap": intervals[0]["upper"] >= intervals[-1]["lower"],
        "q3_tests": family(pairs, task["comparisons"], alpha),
        "q3_three_cycles_together": several_groups(pairs),
        "q5_held_out_sets_against_the_last_cycle": held_out(pairs[-1], task["held_out_sizes"], alpha),
    }


def transfer_paired(cycles: list[dict], comparison: dict, success: str, threshold: Fraction) -> dict:
    """Question 4: the scenarios that gained or lost the success verdict between two cycles, with the sign test."""
    before = {row["test_id"]: row["verdict"] == success for row in cycles[comparison["from"]]["scenarios"]}
    after = cycles[comparison["to"]]["scenarios"]
    gained = [row["test_id"] for row in after if row["verdict"] == success and not before[row["test_id"]]]
    lost = [row["test_id"] for row in after if row["verdict"] != success and before[row["test_id"]]]
    out = {"test_ids_that_gained_the_verdict": gained, "test_ids_that_lost_the_verdict": lost}
    out.update(sign_test(len(gained), len(lost)))
    out["two_sided_below_bonferroni_threshold"] = Fraction(out["two_sided"]["exact"]) < threshold
    return out


def transfer_task(cycles: list[dict], task: dict, confidence: Fraction, alpha: Fraction, steps: int) -> dict:
    """transfer_task: the expected answers of the learner task, from the three red-team cycle files."""
    names = [{row["test_id"]: row["name"] for row in cycle["scenarios"]} for cycle in cycles]
    recount = recount_red_team(cycles)
    progression = cycles[-1]["score_progression"]
    quoted = [progression[f"cycle_{cycle['cycle']}"]["score"] for cycle in cycles]
    check("transfer: the recorded percentages are the summary pass shares, rounded",
          quoted == [row["pass_percent_from_summary_rounded"] for row in recount])
    previous_mismatch = 0
    for earlier, later in zip(cycles, cycles[1:]):
        before = {row["test_id"]: row["verdict"] for row in earlier["scenarios"]}
        previous_mismatch += sum(row["previous_verdict"] != before[row["test_id"]] for row in later["scenarios"])
    by_source = {source: transfer_readings(recount, source, task, confidence, alpha, steps)
                 for source in ("summary_counts", "counts_in_the_scenario_list")}
    threshold = alpha / len(task["comparisons"])
    return {
        "note": task["note"],
        "kind": "observed inputs (the three red-team cycle files at the pinned commit), computed answers",
        "expected_counts": task["expected_counts"],
        "verdict_table": [{"test_id": test_id, "name": names[0][test_id],
                           "verdicts": [next(row["verdict"] for row in cycle["scenarios"] if row["test_id"] == test_id)
                                        for cycle in cycles]}
                          for test_id in sorted(names[0])],
        "q1_recount": {
            "cycles": recount,
            "scenario_ids_and_names_identical_in_all_cycles": all(mapping == names[0] for mapping in names),
            "distinct_evaluators": len({cycle["evaluator"] for cycle in cycles}),
            "percentages_quoted_by_the_last_file": quoted,
            "previous_verdict_fields_that_differ_from_the_previous_file": previous_mismatch,
        },
        "expected_from_the_scenario_lists": by_source["counts_in_the_scenario_list"],
        "alternative_from_the_files_own_summaries": by_source["summary_counts"],
        "q2_interval_if_every_scenario_passed": interval_row(recount[-1]["scenarios_evaluated"],
                                                             recount[-1]["scenarios_evaluated"], confidence, steps),
        "q4_paired_from_the_scenario_lists": {comparison["name"]: transfer_paired(cycles, comparison, task["success_verdict"],
                                                                                  threshold)
                                              for comparison in task["comparisons"]},
        "q4_what_the_files_say_changed_between_cycles": [
            {"cycle": cycle["cycle"], "trigger": cycle["trigger"], "fixes_applied": cycle["fixes_applied"]}
            for cycle in cycles[1:]],
    }


# --- cross-checks that belong to no single section ---------------------------------

def cross_checks(snapshot: dict, scenarios: dict, s: Setup) -> None:
    """Cases worked by hand, closed forms, and the accounting identities of the snapshot."""
    half = (1 - s.confidence) / 2
    hand_computed_cases(scenarios)
    check("closed form: for 0 of n the upper bound is 1 - (alpha/2)^(1/n)",
          abs(float(exact_interval(0, 11, s.confidence, s.steps)[1]) - (1 - float(half) ** (1 / 11))) < 1e-12)
    check("closed form: for n of n the lower bound is (alpha/2)^(1/n)",
          abs(float(exact_interval(11, 11, s.confidence, s.steps)[0]) - float(half) ** (1 / 11)) < 1e-12)
    check("the smaller family is the declared family without one comparison", len(s.smaller) == len(s.comparisons) - 1)
    records, cycles, red_team = s.records, s.cycles, s.red_team
    check("extract.py's counts match the snapshot",
          (len(records), sum(len(record["injections"]) for record in records), len(red_team),
           sum(len(cycle["scenarios"]) for cycle in red_team), len(snapshot["reports"]["baseline"]["injections"]),
           len(snapshot["reports"]["cycle"]["injections"]))
          == tuple(snapshot["counts"][key] for key in ("history_records", "injection_rows", "red_team_cycle_files",
                                                       "scenario_rows", "baseline_report_rows", "cycle_report_rows")))
    check("every cycle: caught + missed = total, and one injection row per injection",
          all(cycle["caught_plus_missed_equals_total"] and cycle["injection_rows"] == cycle["recorded"]["injections_total"]
              for cycle in cycles))
    check("every cycle: the recorded score is caught / total rounded to two decimals",
          all(cycle["recorded_score_is_the_rounded_share"] for cycle in cycles))
    check("every cycle: the per-level injection counts add up to the total",
          all(sum(cycle["injections_per_level"].values()) == cycle["recorded"]["injections_total"] for cycle in cycles))
    check("level_deltas 'before' values equal the previous cycle's level scores",
          all(delta["before"] == records[index - 1]["level_scores"][level]
              for index in range(1, len(records)) for level, delta in records[index]["level_deltas"].items()))
    check("the injection names and their levels are the same in every cycle",
          s.injection_set["names_identical_in_all_cycles"] and s.injection_set["levels_identical_in_all_cycles"])
    check("the glossary and the policy give the same formula for R",
          s.definitions["metric_policy"]["formula"] in s.definitions["glossary"]["text"])
    check("every cycle has the same number of injections", all(n == s.total for _, n in s.counts))


def odd_cycle(s: Setup) -> int:
    """Index of the one cycle whose status labels do not reproduce its recorded count."""
    odd = [index for index, cycle in enumerate(s.cycles) if not cycle["status_rule_reproduces_recorded_count"]]
    check("exactly one cycle's detail fails to reproduce its recorded count, and it is neither the first nor the last",
          len(odd) == 1 and 0 < odd[0] < s.last)
    return odd[0]


# --- the sections of results.json, one function each ---------------------------------

def trend_rule_section(scenarios: dict, s: Setup) -> dict:
    """observed.history.trend_rule: the policy's trend rule applied to the recorded scores."""
    scores = [Fraction(str(cycle["recorded"]["overall_score"])) for cycle in s.cycles]
    labels = [trend_label(scores[:index + 1]) for index in range(len(scores))]
    return {
        "rule": s.definitions["metric_policy"]["trend"],
        "reading": scenarios["trend_rule"]["note"],
        "cycles": [{"cycle_id": cycle["cycle_id"], "recorded_score": cycle["recorded"]["overall_score"],
                    "mean_of_the_earlier_scores_compared": None if index == 0 else num(sum(scores[:index][-2:]) / len(scores[:index][-2:])),
                    "label_by_the_rule": labels[index], "label_recorded": cycle["recorded"]["trend"]}
                   for index, cycle in enumerate(s.cycles)],
        "rule_reproduces_every_recorded_label": labels == [cycle["recorded"]["trend"] for cycle in s.cycles],
    }


def history_section(snapshot: dict, scenarios: dict, s: Setup) -> dict:
    """observed.history: the cycles as recounted, the status rules that fit them, the trend rule, the recorded fixes."""
    records, cycles = s.records, s.cycles
    rules_all = status_rules(records, list(range(len(records))))
    consistent_cycles = [index for index, cycle in enumerate(cycles) if cycle["status_rule_reproduces_recorded_count"]]
    rules_some = status_rules(records, consistent_cycles)
    check("the chosen caught-statuses rule is one of the rules that fit the cycles it is said to fit",
          any(set(rule["statuses_counted_as_caught"]) == s.caught_statuses for rule in rules_some))
    pinned = parse_utc(scenarios["pinned_commit"]["committer_date_utc"])
    return {
        "metric": snapshot["history"]["metric"],
        "cycles": cycles,
        "hours_from_first_to_last_cycle": hours_between(records[0]["timestamp"], records[s.last]["timestamp"]),
        "whole_days_from_the_last_cycle_to_the_pinned_commit":
            (pinned - parse_utc(records[s.last]["timestamp"])).days,
        "injection_set": s.injection_set,
        "levels": len(records[0]["level_scores"]),
        "status_rules": {
            "question": "Which sets of status labels, counted as 'caught', reproduce the recorded caught counts?",
            "labels_seen": sorted({row["status"] for record in records for row in record["injections"]}),
            "rules_reproducing_all_cycles": rules_all,
            "cycles_whose_count_the_chosen_rule_reproduces": [cycles[index]["cycle_id"] for index in consistent_cycles],
            "rules_reproducing_those_cycles": rules_some,
        },
        "trend_rule": trend_rule_section(scenarios, s),
        "what_each_record_says_changed": fix_targets(records, s.caught_statuses),
    }


def observed_section(snapshot: dict, s: Setup, bands: list[dict], history: dict, reports: tuple[dict, dict]) -> dict:
    """observed: what observed-input.json holds, read or recounted."""
    definitions, red_team = s.definitions, s.red_team
    injection_names = {row["injection"] for record in s.records for row in record["injections"]}
    scenario_names = {row["name"] for cycle in red_team for row in cycle["scenarios"]}
    return {
        "kind": "observed: read or recounted from observed-input.json",
        "files_in_the_resilience_folder": snapshot["counts"]["files_in_resilience_folder"],
        "source_files_pinned": len(snapshot["source"]["files"]),
        "definitions": {
            "glossary": definitions["glossary"],
            "policy": {"path": definitions["metric_policy"]["path"], "formula": definitions["metric_policy"]["formula"]},
            "policy_bands": [{"policy_band": band["name"], "psy_002_regime": band["psy_002_regime"],
                              "from": str(band["from"]), "below": None if band["below"] is None else str(band["below"]),
                              "action": next(t["action"] for t in definitions["metric_policy"]["thresholds"]
                                             if t["name"] == band["name"])}
                             for band in bands],
            "readme_status": definitions["readme_status"],
        },
        "history": history,
        "baseline_report": reports[0],
        "cycle_report": reports[1],
        "second_series": {
            "what": "The three red-team cycle files are a separate series, not the detail of the history's cycles.",
            "files": [cycle["path"] for cycle in red_team],
            "ids": [cycle["id"] for cycle in red_team],
            "scenarios_per_cycle": [cycle["scenarios_evaluated"] for cycle in red_team],
            "verdict_scale": ["PASS", "PARTIAL", "FAIL"],
            "history_cycle_ids": [cycle["cycle_id"] for cycle in s.cycles],
            "names_shared_between_injections_and_scenarios": len(injection_names & scenario_names),
        },
    }


def intervals_section(scenarios: dict, s: Setup, bands: list[dict]) -> dict:
    """intervals: one exact interval per cycle from the recorded counts, and the table for every count of that size."""
    intervals = []
    for cycle, (k, n) in zip(s.cycles, s.counts):
        lower, upper = exact_interval(k, n, s.confidence, s.steps)
        row = {"cycle_id": cycle["cycle_id"]}
        row.update(interval_row(k, n, s.confidence, s.steps))
        score = Fraction(str(cycle["recorded"]["overall_score"]))
        inside = bands_spanned(lower, upper, bands)
        row.update({"policy_band_of_the_recorded_score": band_of(score, bands)["name"],
                    "psy_002_regime_of_the_recorded_score": band_of(score, bands)["psy_002_regime"],
                    "policy_bands_inside_the_interval": [band["name"] for band in inside],
                    "psy_002_regimes_inside_the_interval": [band["psy_002_regime"] for band in inside]})
        intervals.append(row)
    total = s.total
    table = [interval_row(k, total, s.confidence, s.steps) for k in range(total + 1)]
    check("interval table: bounds rise with the count",
          all(a["lower"] <= b["lower"] and a["upper"] <= b["upper"] for a, b in zip(table, table[1:])))
    check("interval table: the interval for k mirrors the interval for n - k",
          all(abs(table[k]["lower"] - (1 - table[total - k]["upper"])) < 2 * 10 ** -DECIMALS for k in range(total + 1)))
    overlaps = [{"cycles": [intervals[a]["cycle_id"], intervals[b]["cycle_id"]],
                 "intervals_overlap": intervals[a]["upper"] >= intervals[b]["lower"] and intervals[b]["upper"] >= intervals[a]["lower"]}
                for a, b in itertools.combinations(range(len(intervals)), 2)]
    return {
        "kind": "computed from the recorded counts",
        "method": "Clopper-Pearson exact interval: binomial tails summed with fractions, bounds found by bisection",
        "confidence_level": exact(s.confidence),
        "model": "each injection is an independent trial with one common detection rate, as if the injections were a "
                 "random sample of the defects of interest; an assumption, not a description of how the set was built",
        "cycles": intervals,
        "pairs_of_intervals": overlaps,
        "every_count_of_this_size": table,
        "regime_thresholds_source": scenarios["regime_thresholds"]["source"],
    }


def step_tests_section(s: Setup) -> dict:
    """step_tests: Fisher's exact test for the declared family, for the smaller family and for every pair of cycles."""
    tests = family(s.counts, s.comparisons, s.alpha)
    tests_smaller = family(s.counts, s.smaller, s.alpha)
    all_pairs = []
    for a, b in itertools.combinations(range(len(s.counts)), 2):
        row = {"cycles": [s.cycles[a]["cycle_id"], s.cycles[b]["cycle_id"]]}
        row.update(fisher(*s.counts[a], *s.counts[b]))
        all_pairs.append(row)
    return {
        "kind": "computed from the recorded counts",
        "test": "Fisher's exact test: two independent samples, both margins fixed; two-sided p = total probability of "
                "the tables no more probable than the observed one; one-sided p for the later cycle being higher",
        "family": tests,
        "smaller_family": {"tests_in_the_family": tests_smaller["tests_in_the_family"],
                           "bonferroni_threshold": tests_smaller["bonferroni_threshold"],
                           "comparisons": [{"name": row["name"], "two_sided": row["two_sided"]["value"],
                                            "two_sided_below_bonferroni_threshold": row["two_sided_below_bonferroni_threshold"]}
                                           for row in tests_smaller["comparisons"]]},
        "all_six_pairs": all_pairs,
    }


def multiplicity_section(s: Setup) -> dict:
    """multiplicity: how often each family of tests gives a false positive, by exact enumeration."""
    return {
        "kind": "computed: an exact enumeration, not a simulation",
        "null_model": "the catches recorded in all the cycles fell at random among all the trials, every arrangement "
                      "equally likely; the tests of a family then run on the same table of counts",
        "family": familywise(s.counts, s.comparisons, s.alpha),
        "smaller_family": familywise(s.counts, s.smaller, s.alpha),
    }


def paired_section(s: Setup, step_tests: dict) -> dict:
    """paired: the same injections are scored again, so an exact sign test on those whose result changed."""
    paired = []
    for comparison in s.comparisons:
        step = transitions(s.records, comparison["from"], comparison["to"], s.caught_statuses)
        row = {"name": comparison["name"], "by": "status labels (the rule in scenarios.json)"}
        row.update(step)
        row["sign_test"] = sign_test(len(step["missed_then_caught"]), len(step["caught_then_missed"]))
        paired.append(row)
    check("paired: the four cells of each step add up to the injections",
          all(row["caught_in_both"] + row["missed_in_both"] + len(row["missed_then_caught"]) + len(row["caught_then_missed"])
              == s.total for row in paired))
    check("the first cycle caught nothing, so every injection caught in cycle 2 is a gain whatever the reading",
          s.counts[0][0] == 0)
    first_step_recorded = {"why": "cycle 1 caught nothing, so the recorded 7 of cycle 2 are 7 gains and no loss"}
    first_step_recorded.update(sign_test(s.counts[1][0], 0))
    for threshold_name, threshold in (("two_sided_below_significance_level", s.alpha),
                                      ("two_sided_below_bonferroni_threshold_of_the_family", s.alpha / len(s.comparisons)),
                                      ("two_sided_below_bonferroni_threshold_of_the_smaller_family", s.alpha / len(s.smaller))):
        first_step_recorded[threshold_name] = Fraction(first_step_recorded["two_sided"]["exact"]) < threshold
    return {
        "kind": "computed; the same injections are scored in every cycle, so the results are paired",
        "test": "exact sign test on the injections whose result changed (the exact form of McNemar's test)",
        "bonferroni_threshold_of_the_family": step_tests["family"]["bonferroni_threshold"],
        "bonferroni_threshold_of_the_smaller_family": step_tests["smaller_family"]["bonferroni_threshold"],
        "first_step_from_the_recorded_count": first_step_recorded,
        "steps_from_status_labels": paired,
    }


def one_step_or_three_section(scenarios: dict, s: Setup) -> dict:
    """one_step_or_three: the cycles as independent samples; do the three later ones differ, do they rise?"""
    later = s.counts[1:]
    pooled = Fraction(sum(k for k, _ in later), sum(n for _, n in later))
    rates = [pooled] + [Fraction(rate) for rate in scenarios["fixed_rate_cases"]["rates"]]
    runs = [rising_run(s.total, rate, [k for k, _ in later]) for rate in rates]
    runs[0]["rate_is"] = "the pooled share of the three later cycles"
    by_chance = [trend_rule_by_chance(s.total, rate) for rate in rates]
    by_chance[0]["rate_is"] = "the pooled share of the three later cycles"
    all_four, three_later = several_groups(s.counts), several_groups(later)
    return {
        "kind": "computed from the recorded counts, cycles treated as independent samples",
        "tests": "homogeneity: Freeman-Halton exact test; trend: exact Cochran-Armitage test with scores 0, 1, 2, ...; "
                 "both with the total number caught fixed",
        "all_four_cycles": all_four,
        "three_later_cycles": three_later,
        "three_independent_cycles_under_one_fixed_rate": runs,
        "trend_rule_on_independent_cycles_under_one_fixed_rate": by_chance,
    }


def readings_of_the_odd_cycle(s: Setup, odd: int, tests: dict) -> list[dict]:
    """sensitivity.readings_of_that_cycle: the cycle whose detail does not reproduce its count, read three ways."""
    cycle, total = s.cycles[odd], s.total
    alternatives = []
    for label, value in (("as recorded", s.counts[odd][0]),
                         ("statuses counted as caught", cycle["caught_by_status_rule"]),
                         ("implied by the level scores", Fraction(cycle["caught_implied_by_level_scores"]["exact"]))):
        check("sensitivity: the alternative count is a whole number", Fraction(value).denominator == 1)
        swapped = list(s.counts)
        swapped[odd] = (int(value), total)
        alternative = family(swapped, s.comparisons, s.alpha)
        smaller_threshold = s.alpha / len(s.smaller)
        alternatives.append({
            "reading": label, "caught_in_that_cycle": int(value),
            "interval": interval_row(int(value), total, s.confidence, s.steps),
            "comparisons": [{"name": row["name"], "from": row["from"], "to": row["to"],
                             "two_sided": row["two_sided"]["value"], "bonferroni_adjusted": row["bonferroni_adjusted"],
                             "holm_adjusted": row["holm_adjusted"],
                             "two_sided_below_significance_level": row["two_sided_below_significance_level"],
                             "two_sided_below_bonferroni_threshold": row["two_sided_below_bonferroni_threshold"],
                             "two_sided_below_the_smaller_family_threshold":
                                 Fraction(row["two_sided"]["exact"]) < smaller_threshold}
                            for row in alternative["comparisons"]],
            "three_later_cycles": several_groups(swapped[1:]),
        })
    check("sensitivity: the 'as recorded' reading reproduces the main tests",
          [row["two_sided"] for row in alternatives[0]["comparisons"]]
          == [row["two_sided"]["value"] for row in tests["comparisons"]])
    return alternatives


def readings_of_the_first_cycle(snapshot: dict, s: Setup, tests: dict) -> list[dict]:
    """sensitivity.readings_of_the_first_cycle: the baseline as scored by the chaos-test report of the same date."""
    card = snapshot["reports"]["baseline"]["scorecard"]
    baselines = []
    for label, value in (("history, first cycle", s.counts[0][0]),
                         ("chaos-test report, 'immediate'", card["immediate"]["caught"]),
                         ("chaos-test report, 'including spec-level'", card["including_spec_level"]["caught"])):
        row = {"baseline": label, "caught": value, "total": s.total}
        for name, index in (("against_cycle_2", 1), ("against_cycle_4", s.last)):
            test = fisher(value, s.total, *s.counts[index])
            p = Fraction(test["two_sided"]["exact"])
            row[name] = {"table": test["table"], "two_sided": test["two_sided"],
                         "two_sided_below_significance_level": p < s.alpha,
                         "two_sided_below_bonferroni_threshold": p < s.alpha / len(s.comparisons)}
        baselines.append(row)
    check("sensitivity: the history's own baseline reproduces the main tests",
          (baselines[0]["against_cycle_2"]["two_sided"], baselines[0]["against_cycle_4"]["two_sided"])
          == (tests["comparisons"][0]["two_sided"], tests["comparisons"][3]["two_sided"]))
    return baselines


def levels_as_units(s: Setup) -> dict:
    """sensitivity.levels_as_units: the same tests with levels as the unit, since injections of one level moved together."""
    level_counts = [(cycle["levels_scored_1"], cycle["levels"]) for cycle in s.cycles]
    by_level = {
        "why": "Level scores are 0 or 1 in every cycle but one, so injections of one level were caught or missed "
               "together; counting levels scored 1.0 is the coarsest reading of how many independent results exist.",
        "levels_scored_1_per_cycle": [f"{k}/{n}" for k, n in level_counts],
    }
    by_level.update(family(level_counts, s.comparisons, s.alpha))
    return by_level


def sensitivity_section(snapshot: dict, s: Setup, odd: int, tests: dict) -> dict:
    """sensitivity: how the tests move with the count of one cycle, with the baseline and with the unit."""
    return {
        "kind": "computed",
        "cycle_with_inconsistent_detail": s.cycles[odd]["cycle_id"],
        "readings_of_that_cycle": readings_of_the_odd_cycle(s, odd, tests),
        "readings_of_the_first_cycle": readings_of_the_first_cycle(snapshot, s, tests),
        "levels_as_units": levels_as_units(s),
    }


def synthetic_section(scenarios: dict, s: Setup, bands: list[dict], all_caught: dict) -> dict:
    """synthetic: an imaginary fifth cycle and imaginary held-out sets, defined in scenarios.json."""
    cases = scenarios["imaginary_cases"]
    fresh_sets = held_out(s.counts[s.last], cases["held_out_sets"]["sizes"], s.alpha)
    return {
        "kind": "synthetic: imaginary cycles and injection sets, defined in scenarios.json",
        "all_caught_on_the_reused_set": {
            "description": cases["all_caught_on_the_reused_set"]["description"],
            "interval_if_it_were_a_fresh_sample": all_caught,
            "policy_band_of_its_lower_bound": band_of(exact_interval(s.total, s.total, s.confidence, s.steps)[0], bands)["name"],
        },
        "all_caught_needed_for_each_band": all_caught_needed(bands, s.confidence, s.steps),
        "held_out_sets": {"description": cases["held_out_sets"]["description"],
                          "reference": f"{s.counts[s.last][0]}/{s.counts[s.last][1]} (last recorded cycle)",
                          "sets": fresh_sets},
    }


def worked_answers_section(s: Setup, all_caught: dict, intervals: list[dict], first_test: dict) -> dict:
    """worked_answers: the intermediate values that the lesson's exercise answers show."""
    counts, total = s.counts, s.total
    check("worked answers: the lower bound for n of n and the upper bound for 0 of n add up to 1",
          abs(all_caught["lower"] + intervals[0]["upper"] - 1) < 2 * 10 ** -DECIMALS)
    return {
        "kind": "intermediate values shown in the lesson's exercise answers",
        "half_of_one_minus_confidence": exact((1 - s.confidence) / 2),
        "that_value_to_the_power_one_over_n": {"n": total, "value": all_caught["lower"]},
        "upper_bound_for_0_of_n": intervals[0]["upper"],
        "lower_bound_for_n_of_n": all_caught["lower"],
        "first_step_fisher": {"caught_in_both_cycles_together": counts[0][0] + counts[1][0], "trials_together": 2 * total,
                              "ways_to_place_the_first_cycle_among_the_missed": comb(2 * total - counts[1][0], total),
                              "ways_to_place_the_first_cycle": comb(2 * total, total),
                              "one_sided": first_test["one_sided_improvement"], "two_sided": first_test["two_sided"]},
        "sign_test_powers_of_one_half": {str(k): exact(Fraction(1, 2 ** k)) for k in (1, 2, 6, 7, 9)},
        "thresholds": {"significance_level": exact(s.alpha), "family_of_4": exact(s.alpha / 4),
                       "family_of_3": exact(s.alpha / 3)},
    }


# --- main analysis ------------------------------------------------------------

def analyze(snapshot: dict, scenarios: dict) -> dict:
    """Compute every section of results.json.

    The calls below run in the order in which the self-checks are first evaluated, which results.json records
    under `checks`; the returned dictionary fixes the order of the sections. Keep both when adding a section.
    """
    s = setup(snapshot, scenarios)
    cross_checks(snapshot, scenarios, s)
    bands = policy_bands(s.definitions["metric_policy"]["thresholds"], scenarios["regime_thresholds"]["regimes"])
    reports = (baseline_report(snapshot, s), cycle_report(snapshot, s))
    history = history_section(snapshot, scenarios, s)
    intervals = intervals_section(scenarios, s, bands)
    step_tests = step_tests_section(s)
    one_step_or_three = one_step_or_three_section(scenarios, s)
    odd = odd_cycle(s)
    sensitivity = sensitivity_section(snapshot, s, odd, step_tests["family"])
    paired = paired_section(s, step_tests)
    all_caught = interval_row(s.total, s.total, s.confidence, s.steps)
    controls = negative_controls(s.records, scenarios, {
        "lost_in_last_step": len(paired["steps_from_status_labels"][2]["caught_then_missed"]),
        "names_identical": s.injection_set["names_identical_in_all_cycles"],
        "cycle_2_caught_by_status_rule": s.cycles[odd]["caught_by_status_rule"],
        "last_trend_label": history["trend_rule"]["cycles"][s.last]["label_by_the_rule"],
    })
    transfer = transfer_task(s.red_team, scenarios["transfer_task"], s.confidence, s.alpha, s.steps)
    worked = worked_answers_section(s, all_caught, intervals["cycles"], step_tests["family"]["comparisons"][0])
    multiplicity = multiplicity_section(s)
    synthetic = synthetic_section(scenarios, s, bands, all_caught)
    return {
        "module_id": snapshot["module_id"],
        "rounding": "probabilities, p-values, shares and interval bounds to 6 decimals; 'exact' is the unrounded fraction",
        "source": {"repository": snapshot["source"]["repository"], "commit": snapshot["source"]["commit"],
                   "files": [entry["path"] for entry in snapshot["source"]["files"]]},
        "observed": observed_section(snapshot, s, bands, history, reports),
        "intervals": intervals,
        "step_tests": step_tests,
        "multiplicity": multiplicity,
        "paired": paired,
        "one_step_or_three": one_step_or_three,
        "sensitivity": sensitivity,
        "synthetic": synthetic,
        "negative_controls": controls,
        "worked_answers": worked,
        "transfer_task": transfer,
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
    except (AssertionError, ArithmeticError, KeyError, IndexError, StopIteration, ValueError, OSError) as exc:
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
