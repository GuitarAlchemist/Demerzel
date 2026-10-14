#!/usr/bin/env python3
"""PSY-017 analysis: what six observations can say about calibration.

Reads observed-input.json (written by extract.py) and scenarios.json, never the
repository, and writes results.json. Every probability is an exact fraction,
rounded only when it is written. The one simulation draws from
random.Random(seed).random() and keeps its totals in integer units, so the
output is the same on every platform.

Run from the repository root:
    python -I -B scripts/streeling_fixtures/psychohistory/psy-017/analyze.py
    python -I -B scripts/streeling_fixtures/psychohistory/psy-017/analyze.py --check
"""

from __future__ import annotations

import argparse
import copy
import json
import math
import random
import sys
from datetime import datetime, timezone
from fractions import Fraction
from functools import lru_cache
from pathlib import Path

# This program lives under scripts/ (CONTRIBUTING.md: no executable code outside scripts/); its data stays
# under state/streeling/fixtures/. FIXTURE_FILE is the path the program would have next to that data.
FIXTURE_FILE = (Path(__file__).resolve().parents[4]
                / "state/streeling/fixtures/psychohistory/psy-017" / Path(__file__).name)

HERE = FIXTURE_FILE.parent
DECIMALS = {"probability": 6, "bound": 4, "nudge": 4, "ratio": 4, "day": 1}
ZERO, ONE = Fraction(0), Fraction(1)
CHECKS: dict[str, int] = {}  # self-check -> times evaluated


def check(name: str, condition: bool, detail: str = "") -> None:
    """A self-check that can fail: abort instead of writing a wrong result."""
    if not condition:
        raise AssertionError(f"self-check failed: {name}" + (f" ({detail})" if detail else ""))
    CHECKS[name] = CHECKS.get(name, 0) + 1


def frac(value) -> Fraction:
    """Exact fraction from "3/20", "0.15" or a JSON number (through its shortest decimal form)."""
    return Fraction(str(value))


def num(value, kind: str) -> float:
    """Round an exact value for the output; adding 0.0 turns a negative zero into zero."""
    return round(float(value), DECIMALS[kind]) + 0.0


def both(value: Fraction, kind: str = "probability") -> dict:
    return {"exact": f"{value.numerator}/{value.denominator}", "value": num(value, kind)}


def file_name(path: str) -> str:
    """Last part of a path of the snapshot, where slashes are written with a space on each side."""
    return path.rsplit(" / ", 1)[1]


def moment(stamp: str) -> datetime:
    return datetime.strptime(stamp, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)


@lru_cache(maxsize=None)
def weights(n: int, numerator: int, denominator: int) -> tuple[tuple[int, ...], int]:
    """Binomial probabilities as integers over one denominator: P(X = k) = w[k] / total, for p = numerator/denominator."""
    w = tuple(math.comb(n, k) * numerator ** k * (denominator - numerator) ** (n - k) for k in range(n + 1))
    total = denominator ** n
    check("binomial probabilities of all counts sum to 1", sum(w) == total)
    return w, total


@lru_cache(maxsize=None)
def upper_tails(n: int, numerator: int, denominator: int) -> tuple[tuple[int, ...], int]:
    """tails[k] / total = P(X >= k) for k = 0..n + 1, from the integer weights."""
    w, total = weights(n, numerator, denominator)
    tails = [0] * (n + 2)
    for k in range(n, -1, -1):
        tails[k] = tails[k + 1] + w[k]
    return tuple(tails), total


def pmf(n: int, p: Fraction) -> list[Fraction]:
    w, total = weights(n, p.numerator, p.denominator)
    return [Fraction(value, total) for value in w]


def at_least(n: int, k: int, p: Fraction) -> Fraction:
    """P(X >= k) for X binomial(n, p); 0 when k > n."""
    tails, total = upper_tails(n, p.numerator, p.denominator)
    return Fraction(tails[min(max(k, 0), n + 1)], total)


def at_most(n: int, k: int, p: Fraction) -> Fraction:
    return 1 - at_least(n, k + 1, p)


def count_distribution(probabilities: list[Fraction]) -> list[Fraction]:
    """Distribution of the number of events among independent trials with their own probabilities."""
    dist = [ONE]
    for p in probabilities:
        dist = [(dist[k] if k < len(dist) else ZERO) * (1 - p) + (dist[k - 1] * p if k else ZERO)
                for k in range(len(dist) + 1)]
    return dist


def bisect(function, target: Fraction, increasing: bool, steps: dict) -> tuple[Fraction, Fraction]:
    """Bracket of the rate where function(rate) = target, halved until both ends round to the same bound."""
    lo, hi = ZERO, ONE
    for step in range(1, steps["max_steps"] + 1):
        mid = (lo + hi) / 2
        if (function(mid) < target) == increasing:
            lo = mid
        else:
            hi = mid
        if step >= steps["min_steps"] and num(lo, "bound") == num(hi, "bound"):
            return lo, hi
    raise ArithmeticError("bisection did not settle a bound to the stated decimals")


def exact_interval(x: int, n: int, level: Fraction, steps: dict) -> tuple[Fraction, Fraction]:
    """Clopper-Pearson interval for x of n: each bound leaves (1 - level)/2 in one tail of the binomial."""
    tail = (1 - level) / 2
    lower, upper = ZERO, ONE
    if x > 0:
        lower, hi = bisect(lambda p: at_least(n, x, p), tail, True, steps)
        check("exact interval: the bracket of the lower bound holds the tail probability",
              at_least(n, x, lower) <= tail <= at_least(n, x, hi))
    if x < n:
        upper, hi = bisect(lambda p: at_most(n, x, p), tail, False, steps)
        check("exact interval: the bracket of the upper bound holds the tail probability",
              at_most(n, x, hi) <= tail <= at_most(n, x, upper))
    return lower, upper


def interval_row(x: int, n: int, cfg: dict) -> dict:
    lower, upper = exact_interval(x, n, frac(cfg["confidence_level"]), cfg["bisection"])
    row = {"revised": x, "of": n, "lower": num(lower, "bound"), "upper": num(upper, "bound")}
    return row | {"width": round(row["upper"] - row["lower"], DECIMALS["bound"])}


def count_high(beliefs: list[dict], line: Fraction) -> tuple[list[dict], list[dict]]:
    """The cited counting rule: files at or above the line, and the archived ones among them."""
    high = [belief for belief in beliefs if frac(belief["confidence"]) >= line]
    return high, [belief for belief in high if belief["group"] == "archived"]


def rebuilt_claim(high: list[dict], revised: list[dict], cited: dict) -> str:
    """The sentence the cited producer would write for these counts."""
    rule = cited["counting_rule"]
    rate = round(len(revised) / len(high), rule["rate_decimals"]) if high else 0.0
    files = ", ".join(file_name(belief["path"]) for belief in revised[:rule["archived_files_listed_at_most"]]) or "none"
    return cited["claim_template"].format(revised=len(revised), high=len(high), line=rule["high_confidence_line"],
                                          rate=rate, files=files, cap=cited["nudge_cap"])


def rule_constants(snapshot: dict) -> dict:
    """Trigger, gain and cap of the pinned rule, with the check that every file states the same cap."""
    pipeline = snapshot["rule"]["pipeline"]["quotes"]
    applier = snapshot["rule"]["applier"]["quotes"]
    focus = snapshot["calibration_belief"]
    cap = frac(pipeline["overconfidence_formula"]["cap"])
    check("the cap is the same in the pipeline formula, the applier, the policy guardrail and the belief file",
          {cap} == {frac(applier["nudge_cap"]["value"]), frac(snapshot["rule"]["policy"]["quotes"]["guardrail"]["cap"]),
                    frac(focus["calibration"]["cap"]), frac(focus["claim_parsed"]["cap_per_cycle"]),
                    frac(pipeline["underconfidence_formula"]["cap"])})
    return {"trigger": frac(pipeline["overconfidence_trigger"]["trigger"]),
            "gain": frac(pipeline["overconfidence_formula"]["gain"]), "cap": cap}


def one_sided_nudge(rate: Fraction, rule: dict) -> Fraction:
    """Pinned formula: nothing unless the rate exceeds the trigger, then max(-cap, -gain * rate)."""
    return max(-rule["cap"], -rule["gain"] * rate) if rate > rule["trigger"] else ZERO


def two_sided_nudge(rate: Fraction, rule: dict) -> Fraction:
    """Hypothetical comparison rule: clamp(-gain * (rate - trigger), -cap, +cap)."""
    return max(-rule["cap"], min(rule["cap"], -rule["gain"] * (rate - rule["trigger"])))


def record_section(snapshot: dict) -> dict:
    focus = snapshot["calibration_belief"]
    item, parsed, rules = focus["supporting"][0], focus["claim_parsed"], snapshot["rule"]
    check("the record's claim and its calibration rationale are the same sentence", focus["claim_equals_calibration_rationale"])
    check("the claim's rate is its two counts divided, rounded to 4 decimals",
          f"{round(parsed['revised'] / parsed['high_confidence_beliefs'], 4)}" == parsed["overconfidence_rate"])
    quoted = {name: {key: {"line": quote["line"], "text": quote["text"]} for key, quote in rules[name]["quotes"].items()}
              for name in ("policy", "pipeline", "applier")}
    return {
        "kind": "observed: copied from observed-input.json",
        "path": focus["path"], "proposition": focus["proposition"], "truth_value": focus["truth_value"],
        "confidence": focus["confidence"], "last_updated": focus["last_updated"],
        "supporting_items": len(focus["supporting"]), "contradicting_items": focus["contradicting_items"],
        "claim": item["claim"], "claim_source": item["source"], "claim_timestamp": item["timestamp"],
        "claim_reliability": item["reliability"],
        "claim_numbers": {"revised": parsed["revised"], "high_confidence_beliefs": parsed["high_confidence_beliefs"],
                          "high_confidence_line": float(parsed["high_confidence_line"]),
                          "overconfidence_rate": float(parsed["overconfidence_rate"]),
                          "archived_prior_versions": parsed["archived_prior_versions"],
                          "cap_per_cycle": float(parsed["cap_per_cycle"])},
        "calibration": {key: focus["calibration"][key] for key in ("threshold_nudge", "applied_delta", "prior_nudge", "cap")},
        "rule_files": {name: rules[name]["path"] for name in quoted},
        "rule_lines": quoted,
    }


def provenance(snapshot: dict, cited: dict, loop_written: list[dict]) -> dict:
    """Who writes the calibration belief, read from the quoted lines of the pinned applying script."""
    applier, focus = snapshot["rule"]["applier"]["quotes"], snapshot["calibration_belief"]
    named = applier["producer_named_in_the_header"]["producer"]
    check("provenance: the producer named in the header of the pinned applying script is the cited script",
          named == cited["repository"].split("/", 1)[1] + "/" + cited["path"])
    check("provenance: the files whose only evidence is a recommendation are the two the applying script writes",
          sorted(file_name(b["path"]) for b in loop_written)
          == sorted([file_name(focus["path"]), applier["second_belief_file_written"]["file"]]))
    return {
        "producer_named_by_the_applying_script": named,
        "it_is_the_cited_script": True,
        "copied_from_the_recommendation_at_lines": {
            key: applier[f"{key}_written"]["line"] for key in ("confidence", "source", "claim", "reliability")},
        "fixed_in_the_applying_script_at_line": {"truth_value": applier["truth_value_written"]["line"]},
        "second_belief_file_the_script_writes": applier["second_belief_file_written"]["file"],
    }


def unread_part(snapshot: dict, line: Fraction, counted: int) -> dict:
    """The YAML list of beliefs that the producer's glob skips, and the archive ledger's own words."""
    unread = snapshot["not_read_by_the_producer"]
    items = unread["yaml_beliefs"]["items"]
    high = [item for item in items if frac(item["confidence"]) >= line]
    return {"yaml_file": file_name(unread["yaml_beliefs"]["path"]), "beliefs": len(items),
            "at_or_above_the_line": len(high), "high_confidence_on_disk_with_the_counted_files": counted + len(high),
            "archive_ledger": {"file": file_name(unread["archive_ledger"]["path"]),
                               "quotes": {k: q["text"] for k, q in unread["archive_ledger"]["quotes"].items()}}}


def recount_section(snapshot: dict, cited: dict) -> tuple[dict, list[dict]]:
    """Recount the claim from the pinned belief files with the cited counting rule; also returns the six files."""
    beliefs, focus = snapshot["belief_files"], snapshot["calibration_belief"]
    parsed = focus["claim_parsed"]
    line = frac(parsed["high_confidence_line"])
    check("the cited counting rule uses the line the claim states", frac(cited["counting_rule"]["high_confidence_line"]) == line)
    high, revised = count_high(beliefs, line)
    record_time = moment(focus["supporting"][0]["timestamp"])
    loop_written = [b for b in high if b["every_supporting_source_is_an_ml_feedback_recommendation"]]
    doubts = [1 - frac(b["confidence"]) for b in high]
    rate = Fraction(len(revised), len(high))
    without_loop = [b for b in high if b not in loop_written]
    in_place = [b for b in high if b["group"] == "current" and b["previous_value"]]
    matches = {
        "revised": len(revised) == parsed["revised"],
        "high_confidence_beliefs": len(high) == parsed["high_confidence_beliefs"],
        "archived_files": [file_name(b["path"]) for b in revised] == parsed["archived_prior_versions"],
        "claim_text_rebuilt_from_the_recount_is_identical": rebuilt_claim(high, revised, cited) == focus["supporting"][0]["claim"],
    }
    check("recount: the pinned belief files reproduce the claim's counts, its file names and its sentence", all(matches.values()))
    check("recount: current + archived = belief files read",
          sum(b["group"] == "current" for b in beliefs) + sum(b["group"] == "archived" for b in beliefs) == len(beliefs))
    section = {
        "kind": "computed from the belief files in observed-input.json; the counting rule is cited (scenarios.json, cited_producer)",
        "counting_rule": {key: cited["counting_rule"][key] for key in ("high_confidence", "revised")},
        "belief_files_read": len(beliefs),
        "current": sum(b["group"] == "current" for b in beliefs),
        "archived": sum(b["group"] == "archived" for b in beliefs),
        "current_belief_files": [{"file": file_name(b["path"]), "truth_value": b["truth_value"], "confidence": b["confidence"],
                                  "at_or_above_the_line": b in high, "last_updated": b["last_updated"]}
                                 for b in beliefs if b["group"] == "current"],
        "high_confidence": [{
            "file": file_name(b["path"]), "group": b["group"], "truth_value": b["truth_value"], "confidence": b["confidence"],
            "last_updated": b["last_updated"],
            "days_from_last_update_to_the_record": num(Fraction(int((record_time - moment(b["last_updated"])).total_seconds()), 86400), "day"),
            "written_by_the_feedback_loop": b in loop_written, "is_the_record_itself": b["path"] == focus["path"],
            "previous_value": b["previous_value"]} for b in high],
        "high_confidence_count": len(high), "of_which_current": len(high) - len(revised), "of_which_archived": len(revised),
        "rate": {"exact": f"{len(revised)}/{len(high)}", "value": num(rate, "probability")},
        "matches_the_claim": matches,
        "provenance": provenance(snapshot, cited, loop_written),
        "not_read_by_the_producer": unread_part(snapshot, line, len(high)),
        "composition": {
            "written_by_the_feedback_loop": [file_name(b["path"]) for b in loop_written],
            "the_record_counts_itself": any(b["path"] == focus["path"] for b in high),
            "rate_without_the_files_the_loop_writes": {
                "exact": f"{sum(b in revised for b in without_loop)}/{len(without_loop)}",
                "value": num(Fraction(sum(b in revised for b in without_loop), len(without_loop)), "probability")},
            "archived_high_confidence_truth_values": [b["truth_value"] for b in revised],
            "current_high_confidence_with_a_previous_value": [file_name(b["path"]) for b in in_place],
            "rate_if_a_recorded_previous_value_also_counts_as_revised": {
                "exact": f"{len(revised) + len(in_place)}/{len(high)}",
                "value": num(Fraction(len(revised) + len(in_place), len(high)), "probability")},
            "refresh_notes": {file_name(b["path"]): b["refresh_note"] for b in high if b["refresh_note"]},
            "mean_stated_confidence": num(1 - sum(doubts) / len(doubts), "probability"),
            "expected_errors_if_each_were_wrong_with_probability_one_minus_its_confidence": num(sum(doubts), "probability"),
        },
    }
    return section, high


def interval_section(cfg: dict, revised: int, n: int) -> dict:
    observed = interval_row(revised, n, cfg)
    lower, upper = exact_interval(revised, n, frac(cfg["confidence_level"]), cfg["bisection"])
    level, steps = frac(cfg["confidence_level"]), cfg["bisection"]
    low, high = exact_interval(1, 1, level, steps)[0], exact_interval(0, 1, level, steps)[1]
    check("known answer: the exact 95% interval for 1 of 1 starts at 0.025 and the one for 0 of 1 ends at 0.975",
          (num(low, "bound"), num(high, "bound")) == (0.025, 0.975) and exact_interval(0, 1, level, steps)[0] == 0)
    share = Fraction(revised, n)
    spread = cfg["normal_quantile"] * math.sqrt(float(share * (1 - share) / n))  # square root: correctly rounded
    larger = []
    for size in cfg["same_share_larger_samples"]:
        row = interval_row(int(share * size), size, cfg)
        check("larger samples keep the observed share exactly", Fraction(row["revised"], size) == share)
        bound = exact_interval(row["revised"], size, level, steps)[0]
        larger.append(row | {"lower_bound_above_15_percent": bound > frac(cfg["rates_to_locate"][0])})
    check("exact interval: it narrows as the sample grows at a fixed share",
          all(a["width"] > b["width"] for a, b in zip([observed] + larger, larger)))
    excluding = [row["of"] for row in larger if row["lower_bound_above_15_percent"]]
    return {
        "kind": "computed",
        "method": "Clopper-Pearson: the lower bound L solves P(X >= x | n, L) = (1 - level)/2 and the upper bound U solves "
                  "P(X <= x | n, U) = (1 - level)/2, by bisection on exact binomial sums; width = upper - lower from the "
                  "rounded bounds",
        "level": num(level, "bound"),
        "observed": observed | {"share": num(share, "probability"),
                                "upper_over_lower": round(observed["upper"] / observed["lower"], 1)},
        "rates_inside_the_interval": {rate: lower <= frac(rate) <= upper for rate in cfg["rates_to_locate"]},
        "normal_approximation_for_comparison": {
            "formula": "share +/- z * sqrt(share * (1 - share) / n)", "z": cfg["normal_quantile"],
            "lower": num(float(share) - spread, "bound"), "upper": num(float(share) + spread, "bound"),
            "lower_is_below_zero": float(share) - spread < 0},
        "same_share_in_larger_samples": larger,
        "smallest_listed_sample_whose_interval_excludes_15_percent": min(excluding) if excluding else None,
    }


def flat_prior(revised: int, n: int, rate: Fraction) -> dict:
    """Probability that the true rate exceeds `rate`, before and after the data, under a uniform prior."""
    posterior = at_most(n + 1, revised, rate)  # P(Beta(x + 1, n - x + 1) > rate) = P(Binomial(n + 1, rate) <= x)
    spare = n - revised

    def area(t: Fraction) -> Fraction:  # integral of p^x (1 - p)^(n - x) from 0 to t, term by term
        return sum(Fraction(math.comb(spare, j) * (-1) ** j, revised + j + 1) * t ** (revised + j + 1) for j in range(spare + 1))

    check("flat prior: the binomial identity equals the integral of the likelihood", posterior == 1 - area(rate) / area(ONE))
    return {"prior": "uniform on the true rate between 0 and 1",
            "probability_rate_above_15_percent_before_the_data": both(1 - rate),
            "probability_rate_above_15_percent_after_the_data": both(posterior),
            "added_by_the_data": both(posterior - (1 - rate)),
            "method": "posterior Beta(x + 1, n - x + 1); P(rate > r) = P(Binomial(n + 1, r) <= x), checked against the "
                      "integral of r^x (1 - r)^(n - x)"}


def six_section(scenarios: dict, high: list[dict], revised: int) -> dict:
    n = len(high)
    forecasters = {}
    for key, cfg in scenarios["forecasters"].items():
        if key == "note":
            continue
        rate = frac(cfg["revision_rate"])
        dist = pmf(n, rate)
        check("probabilities: none + exactly one + two or more = 1", dist[0] + dist[1] + at_least(n, 2, rate) == 1)
        forecasters[key] = {
            "revision_rate": both(rate), "description": cfg["description"],
            "probability_of_each_count": [num(value, "probability") for value in dist],
            "none": num(dist[0], "probability"), "exactly_the_observed_count": num(dist[revised], "probability"),
            "one_or_more": num(at_least(n, 1, rate), "probability"), "two_or_more": num(at_least(n, 2, rate), "probability"),
            "three_or_more": num(at_least(n, 3, rate), "probability"), "expected_revised": num(n * rate, "probability")}
    line = frac(scenarios["forecasters"][scenarios["calibrated_forecaster"]]["revision_rate"])
    check("hand-computed case: P(2 or more of 6 at 15%) = 1 - 0.85^6 - 6 * 0.15 * 0.85^5",
          at_least(6, 2, Fraction(3, 20)) == 1 - Fraction(17, 20) ** 6 - 6 * Fraction(3, 20) * Fraction(17, 20) ** 5)
    doubts = [1 - frac(belief["confidence"]) for belief in high]
    stated = count_distribution(doubts)
    check("unequal probabilities: the count distribution sums to 1 and reduces to the binomial when all are equal",
          sum(stated) == 1 and count_distribution([line] * n) == pmf(n, line))
    top = frac(scenarios["forecasters"][scenarios["overconfident_forecaster"]]["revision_rate"])
    ratios = {}
    for key, entry in forecasters.items():
        rate = frac(scenarios["forecasters"][key]["revision_rate"])
        if rate != top:
            ratios[key] = both(pmf(n, top)[revised] / pmf(n, rate)[revised], "ratio")
    return {
        "kind": "computed: exact binomial probabilities for assumed true rates (scenarios.json, forecasters)",
        "beliefs": n, "observed_revised": revised,
        "forecasters": forecasters,
        "calibrated_at_each_stated_confidence": {
            "note": "Each of the six files is wrong with probability 1 - its own stated confidence, independently; "
                    "'revised' is read as 'wrong'. An assumption about the forecaster, applied to the observed confidences.",
            "probabilities_of_error": [num(value, "probability") for value in doubts],
            "expected_wrong": num(sum(doubts), "probability"),
            "none": num(stated[0], "probability"), "exactly_one": num(stated[1], "probability"),
            "two_or_more": num(1 - stated[0] - stated[1], "probability")},
        "likelihood_ratio_of_one_third_against": ratios,
        "likelihood_ratio_definition": "P(exactly the observed count | rate 1/3) / P(exactly the observed count | other rate)",
        "flat_prior": flat_prior(revised, n, line),
    }


def critical_count(n: int, null: Fraction, limit: Fraction) -> int:
    """Smallest c with P(X >= c | n, null) <= limit; n + 1 means the rule can never fire."""
    tails, total = upper_tails(n, null.numerator, null.denominator)
    return next(c for c in range(n + 2) if tails[c] * limit.denominator <= limit.numerator * total)


def design_row(alternative: Fraction, design: dict, null: Fraction, search_limit: int, n_recorded: int) -> dict:
    """Smallest sample whose best decision rule meets both error rates, by exhaustive search."""
    limit, wanted = frac(design["false_alarm_at_most"]), frac(design["detection_at_least"])
    meets = {}
    for n in range(1, search_limit + 1):
        c = critical_count(n, null, limit)
        meets[n] = (at_least(n, c, alternative) >= wanted, c)
    first = next((n for n in meets if meets[n][0]), None)
    if first is None:
        raise ArithmeticError("no sample within the search limit meets the design")
    misses = [n for n in meets if n > first and not meets[n][0]]
    c = meets[first][1]
    check("sample size: the sample before the smallest one fails the design", first == 1 or not meets[first - 1][0])
    return {"alternative_rate": both(alternative), "design": design["key"],
            "false_alarm_at_most": num(limit, "probability"), "detection_at_least": num(wanted, "probability"),
            "smallest_sample": first, "critical_count": c,
            "false_alarm": num(at_least(first, c, null), "probability"),
            "detection": num(at_least(first, c, alternative), "probability"),
            "times_the_recorded_sample": num(Fraction(first, n_recorded), "ratio"),
            "larger_samples_that_fail_the_design": misses,
            "every_sample_meets_the_design_from": (max(misses) + 1) if misses else first,
            "search_limit": search_limit}


def test_section(scenarios: dict, high: list[dict], revised: int, record_time: str, rule: dict) -> dict:
    cfg, n = scenarios["test"], len(high)
    null = frac(scenarios["forecasters"][scenarios["calibrated_forecaster"]]["revision_rate"])
    top = frac(scenarios["forecasters"][scenarios["overconfident_forecaster"]]["revision_rate"])
    table = [{"count": c, "false_alarm": num(at_least(n, c, null), "probability"),
              "detection": num(at_least(n, c, top), "probability")} for c in range(1, n + 1)]
    lesson = next(d for d in cfg["designs"] if d["key"] == cfg["lesson_design"])
    c = critical_count(n, null, frac(lesson["false_alarm_at_most"]))
    check("decision rule: at every critical count the higher rate triggers the rule more often",
          all(row["detection"] > row["false_alarm"] for row in table))
    check("decision rule: the critical count is the smallest one within the false-alarm limit",
          at_least(n, c, null) <= frac(lesson["false_alarm_at_most"]) < at_least(n, c - 1, null))
    fires_from = next(k for k in range(n + 1) if one_sided_nudge(Fraction(k, n), rule) != 0)
    rows = [design_row(frac(rate), design, null, cfg["search_limit"], n)
            for rate in cfg["alternative_rates"] for design in cfg["designs"]]
    needed = next(row for row in rows if row["design"] == cfg["lesson_design"]
                  and row["alternative_rate"]["exact"] == f"{top.numerator}/{top.denominator}")["smallest_sample"]
    span = Fraction(int((moment(record_time) - min(moment(b["last_updated"]) for b in high)).total_seconds()), 86400)
    return {
        "kind": "computed: exact binomial error rates of a counting rule; the error rates wanted are choices (scenarios.json, test)",
        "definition": "Rule 'call the forecaster overconfident when c or more of n high-confidence beliefs are revised'. "
                      "False alarm = probability of that at the calibrated rate; detection = probability at the other rate.",
        "calibrated_rate": both(null),
        "at_the_recorded_sample": {
            "beliefs": n, "other_rate": both(top), "by_critical_count": table,
            "smallest_count_with_false_alarm_at_most_5_percent": c,
            "its_false_alarm": num(at_least(n, c, null), "probability"), "its_detection": num(at_least(n, c, top), "probability"),
            "its_miss_rate": num(1 - at_least(n, c, top), "probability"),
            "observed_revised": revised, "observed_count_reaches_it": revised >= c,
            "count_from_which_the_pinned_rule_fires": fires_from},
        "observations_needed": rows,
        "at_the_recorded_pace": {
            "assumption": scenarios["accumulation"]["assumption"],
            "beliefs": n, "span_days": num(span, "day"), "days_per_belief": num(span / n, "day"),
            "design": cfg["lesson_design"], "sample_needed": needed,
            "days_for_the_sample_needed": num(needed * span / n, "day"),
            "years_for_the_sample_needed": num(needed * span / n / Fraction(1461, 4), "day"),
            "counted_from": min(high, key=lambda b: moment(b["last_updated"]))["last_updated"],
            "still_needed_after_the_record": needed - n,
            "days_after_the_record_for_the_sample_needed": num((needed - n) * span / n, "day"),
            "years_after_the_record_for_the_sample_needed": num((needed - n) * span / n / Fraction(1461, 4), "day")},
    }


def rule_section(snapshot: dict, scenarios: dict, rule: dict, n: int) -> dict:
    focus, pipeline = snapshot["calibration_belief"], snapshot["rule"]["pipeline"]["quotes"]
    stored = {key: frac(focus["calibration"][key]) for key in ("threshold_nudge", "applied_delta", "prior_nudge")}
    rate = Fraction(focus["claim_parsed"]["revised"], focus["claim_parsed"]["high_confidence_beliefs"])
    nudge = one_sided_nudge(rate, rule)
    total = max(-rule["cap"], min(rule["cap"], stored["prior_nudge"] + nudge))
    same = (total, total - stored["prior_nudge"]) == (stored["threshold_nudge"], stored["applied_delta"])
    check("recorded cycle: the pinned formula and clamp reproduce threshold_nudge and applied_delta from prior_nudge", same)
    by_count = [{"revised": k, "rate": num(Fraction(k, n), "probability"),
                 "recommendation": Fraction(k, n) > rule["trigger"],
                 "nudge": num(one_sided_nudge(Fraction(k, n), rule), "nudge")} for k in range(n + 1)]
    per_cycle, expected = {}, {}
    for key, cfg in scenarios["forecasters"].items():
        if key == "note":
            continue
        dist = pmf(n, frac(cfg["revision_rate"]))
        per_cycle[key] = num(sum(p for k, p in enumerate(dist) if one_sided_nudge(Fraction(k, n), rule) != 0), "probability")
        expected[key] = num(sum(p * one_sided_nudge(Fraction(k, n), rule) for k, p in enumerate(dist)), "probability")
    return {
        "kind": "observed rule (pinned files), applied by computation",
        "trigger": f"observed rate > {num(rule['trigger'], 'bound')}",
        "formula": f"nudge = max(-{num(rule['cap'], 'bound')}, -{num(rule['gain'], 'bound')} * rate)",
        "running_total": f"clamp(previous total + nudge, -{num(rule['cap'], 'bound')}, +{num(rule['cap'], 'bound')})",
        "recorded_cycle_recomputed": {
            "rate": f"{focus['claim_parsed']['revised']}/{focus['claim_parsed']['high_confidence_beliefs']}",
            "gain_times_rate": num(-rule["gain"] * rate, "probability"), "nudge_after_the_cap": num(nudge, "nudge"),
            "prior_total": num(stored["prior_nudge"], "nudge"),
            "sum_before_the_clamp": num(stored["prior_nudge"] + nudge, "nudge"),
            "total_after_the_clamp": num(total, "nudge"), "applied_delta": num(total - stored["prior_nudge"], "nudge"),
            "equals_the_recorded_values": same},
        "at_the_recorded_sample": {
            "beliefs": n, "by_count": by_count,
            "smallest_count_with_a_recommendation": next(row["revised"] for row in by_count if row["recommendation"]),
            "smallest_sample_at_which_one_revision_gives_no_recommendation":
                next(m for m in range(1, 1000) if Fraction(1, m) <= rule["trigger"])},
        "probability_of_a_downward_nudge_in_one_cycle": per_cycle,
        "expected_nudge_in_one_cycle": expected,
        "upward_branch": {
            "trigger": pipeline["underconfidence_trigger"]["text"], "formula": pipeline["underconfidence_formula"]["text"],
            "underconfidence_rate_in_the_record": None,
            "note": "The pinned pipeline specification has an upward branch driven by an underconfidence rate; the "
                    "calibration belief records no such rate, so this fixture models the downward branch only."},
    }


def step_table(n: int, rate: Fraction, nudge, rule: dict) -> tuple[list[tuple[Fraction, int]], int]:
    """(nudge, integer weight) per count of revised beliefs, and the common denominator of the weights."""
    w, total = weights(n, rate.numerator, rate.denominator)
    return [(nudge(Fraction(k, n), rule), w[k]) for k in range(n + 1)], total


def propagate(steps: list[tuple[Fraction, int]], total: int, cycles: int, limit: Fraction | None) -> list[dict]:
    """Exact distribution of the running total after 1..cycles cycles, clamped to [-limit, +limit] when a limit is given."""
    dist, out = {ZERO: 1}, []
    for cycle in range(1, cycles + 1):
        following: dict[Fraction, int] = {}
        for value, weight in dist.items():
            for nudge, share in steps:
                moved = value + nudge if limit is None else max(-limit, min(limit, value + nudge))
                following[moved] = following.get(moved, 0) + weight * share
        dist = following
        check("nudge chain: the probabilities of all totals sum to 1", sum(dist.values()) == total ** cycle)
        out.append({value: Fraction(weight, total ** cycle) for value, weight in dist.items()})
    return out


def exact_cycles(cfg: dict, forecasters: dict, rule: dict) -> dict:
    n, cycles, report = cfg["sample_per_cycle"], cfg["cycles"], cfg["report_after_cycles"]
    cap = rule["cap"]
    out, floors = {name: {} for name in cfg["rules"]}, {}
    for key, entry in forecasters.items():
        if key == "note":
            continue
        rate = frac(entry["revision_rate"])
        one, total = step_table(n, rate, one_sided_nudge, rule)
        two, _ = step_table(n, rate, two_sided_nudge, rule)
        clamped = propagate(one, total, cycles, cap)
        none, single = pmf(n, rate)[0], sum(Fraction(w, total) for nudge, w in one if -cap < nudge < 0)
        for k in report:
            check("nudge chain: closed form for the clamped total (still 0: q0^k; one small nudge: k q1 q0^(k-1))",
                  clamped[k - 1].get(ZERO, ZERO) == none ** k
                  and sum(p for value, p in clamped[k - 1].items() if -cap < value < 0) == k * single * none ** (k - 1))
        floor = floors[key] = [clamped[k - 1].get(-cap, ZERO) for k in report]
        out["total_clamped_as_in_the_applier"][key] = {
            "probability_total_at_the_floor": [num(p, "probability") for p in floor],
            "probability_total_still_zero": [num(clamped[k - 1].get(ZERO, ZERO), "probability") for k in report],
            "probability_total_between_zero_and_the_floor":
                [num(sum(p for value, p in clamped[k - 1].items() if -cap < value < 0), "probability") for k in report],
            "first_cycle_with_floor_probability_above_95_percent":
                next(k for k in range(1, cycles + 1) if clamped[k - 1].get(-cap, ZERO) > Fraction(19, 20))}
        mean_one = sum(nudge * w for nudge, w in one) / total
        out["per_cycle_cap_only"][key] = {"mean_nudge_per_cycle": num(mean_one, "probability"),
                                          "mean_total": [num(k * mean_one, "nudge") for k in report]}
        mean_two = sum(nudge * w for nudge, w in two) / total
        variance = sum(nudge * nudge * w for nudge, w in two) / total - mean_two * mean_two
        out["two_sided_comparison_rule"][key] = {
            "mean_nudge_per_cycle": num(mean_two, "probability"),
            "sd_of_one_nudge": num(math.sqrt(float(variance)), "nudge"),  # square root: correctly rounded
            "mean_total": [num(k * mean_two, "nudge") for k in report],
            "sd_of_the_total": [num(math.sqrt(float(k * variance)), "nudge") for k in report]}
        banded = propagate(two, total, cycles, cap)
        out["two_sided_with_the_total_clamp"][key] = {
            "probability_at_the_lower_limit": [num(banded[k - 1].get(-cap, ZERO), "probability") for k in report],
            "probability_at_the_upper_limit": [num(banded[k - 1].get(cap, ZERO), "probability") for k in report],
            "probability_at_either_limit": [num(banded[k - 1].get(-cap, ZERO) + banded[k - 1].get(cap, ZERO), "probability")
                                            for k in report]}
    upper, lower = cfg["floor_ratio"]["numerator"], cfg["floor_ratio"]["denominator"]
    out["total_clamped_as_in_the_applier"]["floor_probability_ratio"] = {
        "numerator": upper, "denominator": lower,
        "values": [num(a / b, "ratio") for a, b in zip(floors[upper], floors[lower])]}
    out["two_sided_comparison_rule"]["nudge_by_count"] = [num(two_sided_nudge(Fraction(k, n), rule), "nudge") for k in range(n + 1)]
    return out


def simulate(cfg: dict, key: str, rate: Fraction, rule: dict) -> dict:
    """Seeded runs of all four rules on the same draws; totals are kept in integer units of 1/units."""
    n, report = cfg["sample_per_cycle"], set(cfg["report_after_cycles"])
    one = [one_sided_nudge(Fraction(k, n), rule) for k in range(n + 1)]
    two = [two_sided_nudge(Fraction(k, n), rule) for k in range(n + 1)]
    units = math.lcm(*(value.denominator for value in one + two + [rule["cap"]]))
    one, two, cap = [int(v * units) for v in one], [int(v * units) for v in two], int(rule["cap"] * units)
    rng, p = random.Random(cfg["seeds"][key]), float(rate)
    kept = {name: {k: [] for k in cfg["report_after_cycles"]} for name in cfg["rules"]}
    fired = 0
    for _ in range(cfg["runs"]):
        a = b = c = d = 0
        for cycle in range(1, cfg["cycles"] + 1):
            x = 0
            for _ in range(n):
                x += rng.random() < p
            fired += one[x] != 0
            a = max(-cap, min(cap, a + one[x]))
            b += one[x]
            c += two[x]
            d = max(-cap, min(cap, d + two[x]))
            if cycle in report:
                for name, value in zip(cfg["rules"], (a, b, c, d)):
                    kept[name][cycle].append(value)
    return {"units": units, "cap": cap, "fired": fired, "kept": kept}


def simulated_rules(cfg: dict, raw: dict) -> dict:
    """Shares, means and percentiles of the kept totals, aligned with report_after_cycles."""
    runs, units, cap, report = cfg["runs"], raw["units"], raw["cap"], cfg["report_after_cycles"]

    def percentile(values: list[int], q: int) -> float:
        return num(Fraction(sorted(values)[math.ceil(q * len(values) / 100) - 1], units), "nudge")

    def spread(name: str) -> dict:
        return {"mean_total": [num(Fraction(sum(raw["kept"][name][k]), runs * units), "nudge") for k in report],
                "percentiles_of_the_total": {str(q): [percentile(raw["kept"][name][k], q) for k in report]
                                             for q in cfg["percentiles"]}}

    clamped, banded = raw["kept"]["total_clamped_as_in_the_applier"], raw["kept"]["two_sided_with_the_total_clamp"]
    return {
        "share_of_cycles_with_a_downward_nudge": num(Fraction(raw["fired"], runs * cfg["cycles"]), "probability"),
        "total_clamped_as_in_the_applier": {
            "runs_with_the_total_at_the_floor": [sum(v == -cap for v in clamped[k]) for k in report],
            "share_of_runs_at_the_floor": [num(Fraction(sum(v == -cap for v in clamped[k]), runs), "probability") for k in report]},
        "per_cycle_cap_only": spread("per_cycle_cap_only"),
        "two_sided_comparison_rule": spread("two_sided_comparison_rule"),
        "two_sided_with_the_total_clamp": {
            "share_of_runs_at_the_lower_limit": [num(Fraction(sum(v == -cap for v in banded[k]), runs), "probability") for k in report],
            "share_of_runs_at_the_upper_limit": [num(Fraction(sum(v == cap for v in banded[k]), runs), "probability") for k in report]},
    }


def cycles_section(scenarios: dict, rule: dict, per_cycle: dict) -> dict:
    cfg = scenarios["nudge_simulation"]
    exact = exact_cycles(cfg, scenarios["forecasters"], rule)
    tolerance = {key: frac(value) for key, value in cfg["tolerance_against_exact"].items()}
    simulated, worst = {}, {"share": 0.0, "mean_total": 0.0}
    for key in cfg["seeds"]:
        simulated[key] = simulated_rules(cfg, simulate(cfg, key, frac(scenarios["forecasters"][key]["revision_rate"]), rule))
        sim, floor = simulated[key], exact["total_clamped_as_in_the_applier"][key]["probability_total_at_the_floor"]
        gaps = [abs(a - b) for a, b in zip(sim["total_clamped_as_in_the_applier"]["share_of_runs_at_the_floor"], floor)]
        gaps.append(abs(sim["share_of_cycles_with_a_downward_nudge"] - per_cycle[key]))
        for side in ("lower", "upper"):
            gaps += [abs(a - b) for a, b in zip(sim["two_sided_with_the_total_clamp"][f"share_of_runs_at_the_{side}_limit"],
                                                exact["two_sided_with_the_total_clamp"][key][f"probability_at_the_{side}_limit"])]
        means = [abs(a - b) for name in ("per_cycle_cap_only", "two_sided_comparison_rule")
                 for a, b in zip(sim[name]["mean_total"], exact[name][key]["mean_total"])]
        check("known answer: simulated shares are within the stated tolerance of the exact probabilities",
              max(gaps) <= tolerance["share"], f"{key}: {max(gaps)}")
        check("known answer: simulated mean totals are within the stated tolerance of the exact means",
              max(means) <= tolerance["mean_total"], f"{key}: {max(means)}")
        worst = {"share": max(worst["share"], max(gaps)), "mean_total": max(worst["mean_total"], max(means))}
    return {
        "kind": "synthetic: exact probabilities and a seeded simulation under the assumption below; not a measurement of the project",
        "assumption": cfg["assumption"],
        "sample_per_cycle": cfg["sample_per_cycle"], "report_after_cycles": cfg["report_after_cycles"],
        "report_note": cfg["report_note"], "rules": cfg["rules"],
        "exact": exact,
        "simulation": {"runs": cfg["runs"], "cycles": cfg["cycles"], "seeds": cfg["seeds"],
                       "percentile_rule": "nearest rank: the value at position ceil(q * runs / 100) of the sorted totals",
                       "forecasters": simulated},
        "simulation_against_exact": {
            "tolerance": {key: num(value, "probability") for key, value in tolerance.items()},
            "largest_difference_of_a_share": num(worst["share"], "probability"),
            "largest_difference_of_a_mean_total": num(worst["mean_total"], "nudge")},
    }


def confidence_section(snapshot: dict, cited: dict, files_read: int, interval: dict) -> dict:
    focus, formula = snapshot["calibration_belief"], cited["recommendation_confidence"]
    base, step, cap = (frac(formula[key]) for key in ("base", "per_belief_file", "cap"))
    stated = frac(focus["confidence"])
    line = frac(snapshot["rule"]["applier"]["quotes"]["auto_apply_confidence"]["value"])
    value = min(cap, base + step * files_read)
    check("stated confidence: the cited formula gives the confidence the record states", value == stated)
    return {
        "kind": "observed value, set against a cited formula (scenarios.json, cited_producer)",
        "confidence": focus["confidence"], "reliability_of_its_one_supporting_item": focus["supporting"][0]["reliability"],
        "at_or_above_its_own_high_confidence_line": stated >= frac(focus["claim_parsed"]["high_confidence_line"]),
        "one_minus_the_stated_confidence": num(1 - stated, "bound"),
        "cited_formula": {
            "formula": formula["formula"], "base": num(base, "bound"), "per_belief_file": num(step, "bound"),
            "cap": num(cap, "bound"), "belief_files_read": files_read,
            "value_before_the_cap": num(base + step * files_read, "bound"), "value": num(value, "bound"),
            "equals_the_stated_confidence": value == stated,
            "smallest_number_of_files_that_reaches_the_cap": next(m for m in range(1000) if base + step * m >= cap),
            "uses_the_two_counts_of_the_claim": False},
        "auto_apply": {
            "line": num(line, "bound"), "source_line": snapshot["rule"]["applier"]["quotes"]["auto_apply_confidence"]["line"],
            "smallest_number_of_files_that_reaches_it": next(m for m in range(1000) if base + step * m >= line)},
        "interval_for_the_rate": {"lower": interval["observed"]["lower"], "upper": interval["observed"]["upper"]},
    }


def hypothesis_section(thresholds: dict, interval: dict, six: dict, test: dict, rule: dict) -> dict:
    """The thresholds were written before the first run; this only reports which of them hold."""
    needed = next(row["smallest_sample"] for row in test["observations_needed"]
                  if row["design"] == thresholds["observations_needed_design"]
                  and row["alternative_rate"]["exact"] == thresholds["observations_needed_alternative"])
    parts = {
        "interval_contains_15_percent": interval["rates_inside_the_interval"][thresholds["interval_contains_rate"]],
        "interval_wider_than_threshold": interval["observed"]["width"] > float(frac(thresholds["interval_width_more_than"])),
        "two_or_more_at_15_percent_above_threshold":
            six["forecasters"]["rate_15_percent"]["two_or_more"] > float(frac(thresholds["two_or_more_at_15_percent_more_than"])),
        "observations_needed_at_least_threshold": needed >= thresholds["observations_needed_at_least"],
        "downward_nudge_in_more_than_half_of_the_cycles":
            rule["probability_of_a_downward_nudge_in_one_cycle"]["rate_15_percent"]
            > float(frac(thresholds["share_of_cycles_with_a_downward_nudge_at_15_percent_more_than"])),
    }
    return {"thresholds": {key: value for key, value in thresholds.items() if key != "note"},
            "values": {"interval_width": interval["observed"]["width"],
                       "two_or_more_at_15_percent": six["forecasters"]["rate_15_percent"]["two_or_more"],
                       "observations_needed": needed,
                       "downward_nudge_per_cycle_at_15_percent": rule["probability_of_a_downward_nudge_in_one_cycle"]["rate_15_percent"]},
            "parts": parts, "every_part_holds": all(parts.values())}


def controls_section(snapshot: dict, scenarios: dict) -> dict:
    """Counters that could pass on nothing, each run on an input built to move it."""
    cfg, cited, beliefs = scenarios["negative_controls"], scenarios["cited_producer"], snapshot["belief_files"]
    claim = snapshot["calibration_belief"]["supporting"][0]["claim"]
    none, _ = count_high(beliefs, frac(cfg["line_that_no_file_reaches"]))
    everything, archived = count_high(beliefs, frac(cfg["line_that_every_file_reaches"]))
    check("negative control: a line no file reaches leaves zero high-confidence files", len(none) == 0)
    check("negative control: a line of 0 counts every belief file read", len(everything) == len(beliefs))
    planted = copy.deepcopy(beliefs)
    target = next(b for b in planted if file_name(b["path"]) == cfg["planted_move"]["file"])
    check("negative control: the planted file is a current belief", target["group"] == "current")
    target["group"] = "archived"
    high, revised = count_high(planted, frac(cited["counting_rule"]["high_confidence_line"]))
    moved = rebuilt_claim(high, revised, cited)
    check("negative control: one belief treated as archived changes the recount and the rebuilt claim",
          (len(revised), len(high)) == (3, 6) and moved != claim)
    return {
        "line_no_file_reaches": {"line": num(frac(cfg["line_that_no_file_reaches"]), "bound"), "high_confidence_files": len(none)},
        "line_every_file_reaches": {"line": num(frac(cfg["line_that_every_file_reaches"]), "bound"),
                                    "high_confidence_files": len(everything), "of_which_archived": len(archived)},
        "planted_move": {"note": cfg["planted_move"]["note"], "file": cfg["planted_move"]["file"],
                         "recount": f"{len(revised)}/{len(high)}", "rebuilt_claim_equals_the_record": moved == claim,
                         "rebuilt_claim": moved},
    }


def transfer_task(task: dict, interval_cfg: dict) -> dict:
    n, seen = task["confident_diagnoses"], task["overturned"]
    calibrated, cautious, other = (frac(task[key]) for key in ("calibrated_rate", "more_cautious_rate", "alternative_rate"))
    lower, upper = exact_interval(seen, n, frac(task["confidence_level"]), interval_cfg["bisection"])
    limit = frac(task["false_alarm_at_most"])
    c = critical_count(n, calibrated, limit)
    rule = {key: frac(task["rule"][name]) for key, name in (("trigger", "trigger_rate"), ("gain", "gain"), ("cap", "cap_per_cycle"))}
    nudges = [one_sided_nudge(Fraction(k, n), rule) for k in range(n + 1)]
    dist = pmf(n, calibrated)
    fires = sum(p for k, p in enumerate(dist) if nudges[k] != 0)
    mean = sum(p * nudges[k] for k, p in enumerate(dist))
    check("transfer task: the observed count is below the critical count although its tail probability is near the limit",
          seen < c and at_least(n, seen, calibrated) > limit)
    return {
        "note": task["note"],
        "q1_tail_and_interval": {
            "probability_of_the_observed_count_or_more_at_the_calibrated_rate": num(at_least(n, seen, calibrated), "probability"),
            "probability_of_the_observed_count_or_more_at_the_more_cautious_rate": num(at_least(n, seen, cautious), "probability"),
            "exact_interval": {"overturned": seen, "of": n, "lower": num(lower, "bound"), "upper": num(upper, "bound")},
            "calibrated_rate_inside_the_interval": lower <= calibrated <= upper,
            "more_cautious_rate_inside_the_interval": lower <= cautious <= upper},
        "q2_likelihood_ratio": {
            "probability_of_exactly_the_observed_count_at_the_alternative_rate": num(pmf(n, other)[seen], "probability"),
            "probability_of_exactly_the_observed_count_at_the_calibrated_rate": num(dist[seen], "probability"),
            "ratio": num(pmf(n, other)[seen] / dist[seen], "ratio")},
        "q3_decision_rule": {
            "false_alarm_at_most": num(limit, "probability"), "critical_count": c,
            "false_alarm_at_the_critical_count": num(at_least(n, c, calibrated), "probability"),
            "false_alarm_one_count_lower": num(at_least(n, c - 1, calibrated), "probability"),
            "detection_at_the_alternative_rate": num(at_least(n, c, other), "probability"),
            "miss_rate_at_the_alternative_rate": num(1 - at_least(n, c, other), "probability"),
            "observed_count_reaches_it": seen >= c},
        "q4_nudge_rule": {
            "nudge_by_count": [num(value, "nudge") for value in nudges],
            "smallest_count_with_a_nudge": next(k for k, value in enumerate(nudges) if value != 0),
            "probability_of_a_nudge_in_one_cycle_at_the_calibrated_rate": num(fires, "probability"),
            "probability_of_at_least_one_nudge": {str(k): num(1 - (1 - fires) ** k, "probability") for k in task["cycles"]},
            "expected_nudge_in_one_cycle": num(mean, "probability"),
            "expected_total_without_a_limit": {str(k): num(k * mean, "nudge") for k in task["cycles"]}},
        "q5_reference_sample": design_row(other, task["design"], calibrated, task["search_limit"], n),
    }


def analyze(snapshot: dict, scenarios: dict) -> dict:
    if scenarios["rounding"] != {f"{key}_decimals": value for key, value in DECIMALS.items()}:
        raise ValueError("scenarios.json rounding does not match analyze.py")
    cited, focus = scenarios["cited_producer"], snapshot["calibration_belief"]
    record = record_section(snapshot)
    recount, high = recount_section(snapshot, cited)
    revised = recount["of_which_archived"]
    rule = rule_constants(snapshot)
    interval = interval_section(scenarios["interval"], revised, len(high))
    six = six_section(scenarios, high, revised)
    test = test_section(scenarios, high, revised, focus["supporting"][0]["timestamp"], rule)
    nudge = rule_section(snapshot, scenarios, rule, len(high))
    cycles = cycles_section(scenarios, rule, nudge["probability_of_a_downward_nudge_in_one_cycle"])
    confidence = confidence_section(snapshot, cited, recount["belief_files_read"], interval)
    verdict = hypothesis_section(scenarios["hypothesis_thresholds"], interval, six, test, nudge)
    controls = controls_section(snapshot, scenarios)
    transfer = transfer_task(scenarios["transfer_task"], scenarios["interval"])
    return {
        "module_id": snapshot["module_id"],
        "rounding": "probabilities to 6 decimals, interval bounds to 4, nudges and totals to 4, ratios to 4, days and "
                    "years to 1; 'exact' is the unrounded fraction",
        "source": {"repository": snapshot["source"]["repository"], "commit": snapshot["source"]["commit"],
                   "files": [entry["path"] for entry in snapshot["source"]["files"]],
                   "cited_outside_the_pin": {key: cited[key] for key in ("repository", "commit", "path", "git_blob", "url")}},
        "record": record,
        "recount": recount,
        "exact_interval": interval,
        "revisions_among_six": six,
        "telling_two_rates_apart": test,
        "nudge_rule": nudge,
        "nudge_over_cycles": cycles,
        "stated_confidence": confidence,
        "hypothesis_test": verdict,
        "negative_controls": controls,
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
