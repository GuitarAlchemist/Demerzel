#!/usr/bin/env python3
"""PSY-004 analysis: how wide an aggregate of 14 is, and what a shared cause does to it.

Reads observed-input.json (written by extract.py) and scenarios.json, never
the repository, and writes results.json. Six parts: the department's claim
against what the snapshot holds (observed); exact binomial intervals for
independent agents (computed from assumed inputs); agents whose answers share
a cause (synthetic: exact mixture, formula and seeded simulation); a second
generating model with the same correlation; the length of the decision log
that would measure the correlation; and the same sizing for a group as small
as the tribunal panel that the snapshot describes.

Run from the repository root:
    python -I scripts/streeling_fixtures/psychohistory/psy-004/analyze.py
    python -I scripts/streeling_fixtures/psychohistory/psy-004/analyze.py --check
"""

from __future__ import annotations

import argparse
import json
import math
import random
import statistics
import sys
from fractions import Fraction
from pathlib import Path

# This program lives under scripts/ (CONTRIBUTING.md: no executable code outside scripts/); its data stays
# under state/streeling/fixtures/. FIXTURE_FILE is the path the program would have next to that data.
FIXTURE_FILE = (Path(__file__).resolve().parents[4]
                / "state/streeling/fixtures/psychohistory/psy-004" / Path(__file__).name)

HERE = FIXTURE_FILE.parent
DECIMALS = {"probability": 6, "size": 3, "z_score": 2}
TIE_MARGIN = 1e-6  # in units of the last stored digit
DECISION_MARGIN = 1e-9
CHECKS: dict[str, int] = {}  # self-check -> times evaluated


def check(name: str, condition: bool, detail: str = "") -> None:
    """A self-check that can fail: abort instead of writing a wrong result."""
    if not condition:
        raise AssertionError(f"self-check failed: {name}" + (f" ({detail})" if detail else ""))
    CHECKS[name] = CHECKS.get(name, 0) + 1


def rounded(value, kind: str) -> float:
    """Round for storage. An exact fraction is rounded exactly (half to even). A float is refused
    when it is so close to a rounding boundary that the last bits of a library function (log, pow)
    on another platform could change a stored digit."""
    if isinstance(value, Fraction):
        return float(round(value, DECIMALS[kind])) + 0.0
    value = float(value)
    scaled = abs(value) * 10 ** DECIMALS[kind]
    check("no stored number lies within 1e-6 of a rounding boundary, in units of its last digit",
          abs(scaled - math.floor(scaled) - 0.5) > TIE_MARGIN, f"{value!r} at {DECIMALS[kind]} decimals")
    return round(value, DECIMALS[kind]) + 0.0


def prob(value) -> float:
    return rounded(value, "probability")


def size(value) -> float:
    return rounded(value, "size")


def zscore(value) -> float:
    return rounded(value, "z_score")


def below(left: float, right: float) -> bool:
    """left < right, refusing a comparison that the last bits of a float could decide."""
    check("no comparison between two computed numbers is decided by less than 1e-9",
          abs(left - right) > DECISION_MARGIN, f"{left!r} against {right!r}")
    return left < right


# --- the binomial distribution, by summation ---------------------------------

def binomial_pmf(n: int, p: float) -> list[float]:
    """P(X = k) for k = 0..n, X ~ Binomial(n, p).

    Built from the mode outward with the ratio P(k+1)/P(k) = (n-k)/(k+1) * p/(1-p),
    then normalised. Only + - * / are used (no log, exp or gamma function), so the
    values are the same on every IEEE-754 platform; terms far from the mode
    underflow to 0 without harm.
    """
    if p <= 0.0:
        return [1.0] + [0.0] * n
    if p >= 1.0:
        return [0.0] * n + [1.0]
    odds = p / (1.0 - p)
    mode = min(n, int((n + 1) * p))
    weights = [0.0] * (n + 1)
    weights[mode] = 1.0
    for k in range(mode, n):
        weights[k + 1] = weights[k] * (n - k) / (k + 1) * odds
    for k in range(mode, 0, -1):
        weights[k - 1] = weights[k] * k / (n - k + 1) / odds
    total = math.fsum(weights)
    return [weight / total for weight in weights]


def upper_tail(k: int, n: int, p: float) -> float:
    """P(X >= k)."""
    return math.fsum(binomial_pmf(n, p)[k:])


def lower_tail(k: int, n: int, p: float) -> float:
    """P(X <= k)."""
    return math.fsum(binomial_pmf(n, p)[:k + 1])


def bisect_increasing(function) -> float:
    """Root in (0, 1) of an increasing function, halving until two neighbouring floats remain."""
    low, high = 0.0, 1.0
    while True:
        middle = (low + high) / 2.0
        if middle <= low or middle >= high:
            return middle
        if function(middle) < 0.0:
            low = middle
        else:
            high = middle


def clopper_pearson(k: int, n: int, alpha: float) -> tuple[float, float]:
    """Exact two-sided interval for a proportion after k yes among n independent answers.

    Lower bound: the p at which P(X >= k) = alpha/2. Upper bound: the p at which
    P(X <= k) = alpha/2. By definition the lower bound is 0 when k = 0 and the
    upper bound is 1 when k = n.
    """
    lower = 0.0 if k == 0 else bisect_increasing(lambda p: upper_tail(k, n, p) - alpha / 2.0)
    upper = 1.0 if k == n else bisect_increasing(lambda p: alpha / 2.0 - lower_tail(k, n, p))
    return lower, upper


def interval_row(k: int, n: int, alpha: float) -> dict:
    lower, upper = clopper_pearson(k, n, alpha)
    check("an exact interval contains the observed share", lower <= k / n <= upper)
    return {"agents": n, "yes": k, "share": prob(Fraction(k, n)), "lower": prob(lower), "upper": prob(upper),
            "width": prob(upper - lower)}


# --- agents that share a cause ------------------------------------------------

def shared_cause(rho: Fraction, p: Fraction) -> dict:
    """The copy model: probability of copying the shared signal, and each agent's yes probability given the signal."""
    copy = math.sqrt(float(rho))
    alone = (1.0 - copy) * float(p)
    return {"copy": copy, "yes_if_signal_yes": copy + alone, "yes_if_signal_no": alone}


def count_pmf(n: int, rho: Fraction, p: Fraction) -> list[float]:
    """Copy model: exact distribution of the number of yes among n agents, a mixture of two binomials."""
    model = shared_cause(rho, p)
    high, low = binomial_pmf(n, model["yes_if_signal_yes"]), binomial_pmf(n, model["yes_if_signal_no"])
    weight = float(p)
    return [weight * a + (1.0 - weight) * b for a, b in zip(high, low)]


def beta_binomial_pmf(n: int, rho: Fraction, p: Fraction) -> list[Fraction]:
    """Second model: every agent says yes with a shared probability q ~ Beta(a, b). Exact fractions,
    from the ratio P(k+1)/P(k) = (n-k)/(k+1) * (a+k)/(b+n-k-1)."""
    a, b = p * (1 - rho) / rho, (1 - p) * (1 - rho) / rho
    weights = [Fraction(1)]
    for k in range(n):
        weights.append(weights[-1] * (n - k) * (a + k) / ((k + 1) * (b + n - k - 1)))
    total = sum(weights)
    return [weight / total for weight in weights]


def share_moments(pmf: list[float]) -> tuple[float, float, float]:
    """Mean, variance and fourth central moment of the share k/n."""
    n = len(pmf) - 1
    mean = math.fsum(k / n * q for k, q in enumerate(pmf))
    deviations = [k / n - mean for k in range(n + 1)]
    variance = math.fsum(d * d * q for d, q in zip(deviations, pmf))
    fourth = math.fsum(d * d * d * d * q for d, q in zip(deviations, pmf))
    return mean, variance, fourth


def design_effect(n: int, rho: Fraction) -> Fraction:
    return 1 + (n - 1) * rho


def effective_size(n: int, rho: Fraction) -> Fraction:
    return Fraction(n) / design_effect(n, rho)


def share_variance(n: int, rho: Fraction, p: Fraction) -> Fraction:
    return p * (1 - p) / n * design_effect(n, rho)


def within_tolerance(pmf: list[float], p: Fraction, tolerance: Fraction) -> float:
    n = len(pmf) - 1
    return math.fsum(q for k, q in enumerate(pmf) if abs(Fraction(k, n) - p) <= tolerance)


def central_range(pmf: list[float], alpha: float) -> tuple[int, int]:
    """Smallest count with P(X <= k) > alpha/2 and largest count with P(X >= k) > alpha/2."""
    n = len(pmf) - 1
    low = next(k for k in range(n + 1) if below(alpha / 2.0, math.fsum(pmf[:k + 1])))
    high = next(k for k in range(n, -1, -1) if below(alpha / 2.0, math.fsum(pmf[k:])))
    return low, high


def agreeing(pmf: list, yes: int) -> list:
    """The probabilities of the counts in which at least `yes` agents give the same answer."""
    n = len(pmf) - 1
    return [q for k, q in enumerate(pmf) if k >= yes or k <= n - yes]


def simulate(n: int, rho: Fraction, p: Fraction, occasions: int, seed: int) -> list[int]:
    """Number of yes on each occasion, drawn from the copy model."""
    rng = random.Random(seed)
    copy, yes = math.sqrt(float(rho)), float(p)
    counts = []
    for _ in range(occasions):
        signal = rng.random() < yes
        count = 0
        for _agent in range(n):
            if rng.random() < copy:
                count += signal
            else:
                count += rng.random() < yes
        counts.append(count)
    return counts


def simulated_statistics(histogram: list[int]) -> dict:
    n, occasions = len(histogram) - 1, sum(histogram)
    mean = sum(k * h for k, h in enumerate(histogram)) / (occasions * n)
    variance = math.fsum(h * (k / n - mean) * (k / n - mean) for k, h in enumerate(histogram)) / (occasions - 1)
    both_yes = sum(k * (k - 1) * h for k, h in enumerate(histogram)) / (occasions * n * (n - 1))
    return {"mean": mean, "variance": variance, "correlation": (both_yes - mean * mean) / (mean * (1.0 - mean)),
            "unanimous": (histogram[0] + histogram[n]) / occasions}


def correlation_estimate(counts: list[int], n: int):
    """Moment estimate of the pairwise correlation from the yes counts of a log, as an exact fraction:
    (share of agent pairs that both say yes - mean^2) / (mean * (1 - mean)). None when every answer is alike."""
    occasions = len(counts)
    mean = Fraction(sum(counts), occasions * n)
    if mean in (0, 1):
        return None
    both_yes = Fraction(sum(k * (k - 1) for k in counts), occasions * n * (n - 1))
    return (both_yes - mean * mean) / (mean * (1 - mean))


def percentile(ordered: list, q: Fraction):
    """Smallest value with at least the share q of the list at or below it."""
    return ordered[max(0, math.ceil(q * len(ordered)) - 1)]


# --- sections of the result ----------------------------------------------------

def persona_named_reviews(verdicts: list[dict], names: list[str]) -> int:
    return sum(review["reviewer"] in names for verdict in verdicts for review in verdict["reviews"])


def recount(snapshot: dict) -> dict:
    """The group of cross-checks on the snapshot: its rows are counted again here, compared with the counts that
    extract.py stored, and checked for shape. Returns what was counted."""
    record, counts, schema = snapshot["department_record"], snapshot["counts"], snapshot["council_schema"]
    personas = snapshot["persona_files"]["files"]
    names = [persona["name"] for persona in personas]
    verdicts = snapshot["council_verdicts"]["verdicts"]
    reviews = [review for verdict in verdicts for review in verdict["reviews"]]
    paired = [verdict for verdict in verdicts if len(verdict["reviews"]) >= 2]
    alike = sum(len({review["constitutional_alignment"] for review in verdict["reviews"]}) == 1 for verdict in paired)
    largest = max(len(verdict["reviews"]) for verdict in verdicts)
    named = persona_named_reviews(verdicts, names)
    check("recount of persona files, consumer repos and council records equals extract.py's counts",
          (len(personas), len(record["consumer_repos"]), len(verdicts), len(reviews), len(paired), alike, largest, named)
          == (counts["persona_files"], counts["consumer_repos"], counts["council_verdicts"], counts["council_reviews"],
              counts["council_verdicts_with_two_or_more_reviews"], counts["council_of_those_with_all_reviews_alike"],
              counts["council_largest_number_of_reviews"], counts["council_reviews_whose_reviewer_is_a_persona_name"]))
    check("persona names are distinct", len(set(names)) == len(names))
    persona_keys = snapshot["persona_files"]["top_level_keys_and_the_number_of_files_that_have_them"]
    check("every persona file has a name, a version and a role among its top-level keys, and no key is counted "
          "in more files than exist",
          all(persona_keys.get(key) == len(personas) for key in ("name", "version", "role"))
          and all(0 < count <= len(personas) for count in persona_keys.values()))
    panel = snapshot["tribunal_panel"]
    members = [member["persona"] for member in panel["members"]]
    with_a_file = sum(member in names for member in members)
    check("recount of the tribunal panel equals extract.py's counts",
          (len(members), with_a_file, len(panel["answers_a_persona_may_return"]), len(panel["verdict_files"]))
          == (counts["tribunal_panel_personas"], counts["tribunal_panel_personas_with_a_persona_file"],
              counts["tribunal_panel_answers_a_persona_may_return"], counts["tribunal_panel_verdict_files"]))
    check("the personas of the tribunal panel are distinct and each has a persona file",
          len(set(members)) == len(members) == with_a_file)
    check("the folder searched for tribunal verdicts lies in a folder that exists, and the snapshot holds no "
          "tribunal verdict: the council reviews are the only recorded answers",
          panel["verdict_folder_parent_exists"] and not panel["verdict_files"])
    check("the workflow's comment on failed runs, which the lesson quotes, says that the lane never produced a verdict",
          "this lane silently never produced a verdict" in panel["note_on_failed_runs_in_the_workflow"])
    check("every counted source file is listed with a blob id",
          len(snapshot["source"]["files"]) == 1 + len(personas) + len(verdicts) + 1 + 2
          and all(len(entry["git_blob"]) == 40 for entry in snapshot["source"]["files"]))
    check("no council verdict holds more reviews than its schema allows", largest <= schema["max_reviews_per_verdict"])
    return {"names": names, "verdicts": verdicts, "reviews": reviews, "paired": paired, "alike": alike,
            "largest": largest, "named": named, "members": members, "with_a_file": with_a_file}


def answers_by_role(reviews: list[dict], schema: dict) -> dict:
    """For each reviewer role of the schema: its reviews, and how many gave each answer."""
    by_role = {}
    for role in schema["reviewer_roles"]:
        answers = [review["constitutional_alignment"] for review in reviews if review["reviewer"] == role]
        by_role[role] = {"reviews": len(answers)} | {value: answers.count(value)
                                                     for value in schema["constitutional_alignment_values"]}
    check("the reviews per role and per answer add up to the reviews",
          sum(row["reviews"] for row in by_role.values()) == len(reviews)
          and all(sum(row.values()) == 2 * row["reviews"] for row in by_role.values()))
    return by_role


def planted_review_control(record: dict, verdicts: list[dict], names: list[str], named: int) -> dict:
    """Negative control: "no review names a persona" must not pass on nothing."""
    planted = json.loads(json.dumps(verdicts))
    planted[0]["reviews"][0]["reviewer"] = record["head_persona"]
    planted_named = persona_named_reviews(planted, names)
    check("negative control: a planted review by a persona is counted", planted_named == named + 1)
    return {"what_is_planted": f"the first review's reviewer replaced by the head persona, {record['head_persona']}",
            "reviews_whose_reviewer_is_a_persona_name": named,
            "with_the_planted_review": planted_named}


def council_part(counts: dict, schema: dict, found: dict, by_role: dict) -> dict:
    verdicts, reviews, paired, alike = found["verdicts"], found["reviews"], found["paired"], found["alike"]
    return {
        "what_it_is": "state/council/: verdicts of a council of reviewer roles on a pull request; each review "
                      "answers pass or fail under constitutional_alignment",
        "verdicts": len(verdicts),
        "distinct_tasks": sorted({verdict["task_id"] for verdict in verdicts}),
        "utc_dates": sorted({verdict["timestamp"][:10] for verdict in verdicts}),
        "first_timestamp": min(verdict["timestamp"] for verdict in verdicts),
        "last_timestamp": max(verdict["timestamp"] for verdict in verdicts),
        "reviews": len(reviews),
        "reviewer_roles": sorted({review["reviewer"] for review in reviews}),
        "reviews_whose_reviewer_is_a_persona_name": found["named"],
        "schema_max_reviews_per_verdict": schema["max_reviews_per_verdict"],
        "verdicts_by_number_of_reviews": counts["council_verdicts_by_number_of_reviews"],
        "largest_number_of_reviews_on_one_verdict": found["largest"],
        "answers_by_reviewer_role": by_role,
        "verdicts_with_two_reviews": len(paired),
        "of_those_both_reviews_alike": alike,
        "of_those_reviews_differ": len(paired) - alike,
    }


def panel_part(record: dict, panel: dict, members: list[str], with_a_file: int) -> dict:
    return {
        "what_it_is": "a workflow that sends one pull request to several personas and asks each for one of a "
                      "few answers; this fixture read its two files as text and did not run it; a comment in the "
                      "workflow file reports failed runs and no verdict",
        "script": panel["script"],
        "workflow": panel["workflow"],
        "personas": len(members),
        "persona_names": members,
        "personas_with_a_persona_file": with_a_file,
        "stated_personas_minus_panel_personas": record["stated_personas"] - len(members),
        "answers_a_persona_may_return": panel["answers_a_persona_may_return"],
        "consensus_rule_named_in_both_files": panel["consensus_rule_named_in_both_files"],
        "pull_request_fields_in_every_persona_prompt": panel["pull_request_fields_in_every_persona_prompt"],
        "member_fields_in_the_persona_prompt": panel["member_fields_in_the_persona_prompt"],
        "model_argument_of_the_run": panel["model_argument_of_the_run"],
        "note_on_failed_runs_in_the_workflow": panel["note_on_failed_runs_in_the_workflow"],
        "permission_the_note_explains_granted_below_it": panel["permission_the_note_explains_granted_below_it"],
        "verdict_lists_with_one_entry_per_panel_member": panel["verdict_lists_with_one_entry_per_panel_member"],
        "verdict_folder": panel["verdict_folder"],
        "verdict_folder_exists": panel["verdict_folder_exists"],
        "verdict_files": len(panel["verdict_files"]),
    }


def observed_section(snapshot: dict) -> tuple[dict, dict]:
    """Section `observed`: the record's claim against what the snapshot holds, and the planted-review control."""
    record, counts, schema = snapshot["department_record"], snapshot["counts"], snapshot["council_schema"]
    personas = snapshot["persona_files"]["files"]
    persona_keys = snapshot["persona_files"]["top_level_keys_and_the_number_of_files_that_have_them"]
    found = recount(snapshot)
    names, largest, members = found["names"], found["largest"], found["members"]
    by_role = answers_by_role(found["reviews"], schema)
    control = planted_review_control(record, found["verdicts"], names, found["named"])
    section = {
        "kind": "observed: copied or counted from observed-input.json",
        "key_principle": record["key_principle"],
        "established": record["established"],
        "stated_personas": record["stated_personas"],
        "persona_files": len(personas),
        "persona_files_minus_stated_personas": len(personas) - record["stated_personas"],
        "persona_names": names,
        "persona_file_top_level_keys": sorted(persona_keys),
        "stated_repos": record["stated_repos"],
        "consumer_repos": record["consumer_repos"],
        "consumer_repo_count": len(record["consumer_repos"]),
        "consumer_repos_minus_stated_repos": len(record["consumer_repos"]) - record["stated_repos"],
        "council": council_part(counts, schema, found, by_role),
        "tribunal_panel": panel_part(record, snapshot["tribunal_panel"], members, found["with_a_file"]),
        "largest_recorded_group_answering_one_question": largest,
        "stated_personas_minus_that_group": record["stated_personas"] - largest,
        "largest_group_a_workflow_in_the_snapshot_would_ask_one_question": len(members),
        "scope_note": "extract.py reads no file in which the stated number of personas answer one question; this "
                      "describes the snapshot and is not an audit of every file in the repository",
    }
    return section, control


def half_yes_rows(sizes: list[int], share: Fraction, alpha: float, z: float) -> list[dict]:
    """The width table: the exact interval when the stated share of each group says yes."""
    half = []
    for n in sizes:
        yes = share * n
        check("the width table's observed share gives a whole number of agents", yes.denominator == 1)
        row = interval_row(int(yes), n, alpha)
        row["sd_of_the_share"] = prob(math.sqrt(float(share * (1 - share) / n)))
        row["width_normal_approximation"] = prob(2.0 * z * math.sqrt(float(share * (1 - share) / n)))
        half.append(row)
    check("the exact interval narrows as the group grows", all(a["width"] > b["width"] for a, b in zip(half, half[1:])))
    for row in half:
        row["width_at_the_smallest_group_over_this_width"] = size(half[0]["width"] / row["width"])
        row["square_root_of_the_size_ratio"] = size(math.sqrt(row["agents"] / half[0]["agents"]))
    return half


def all_yes_rows(sizes: list[int], alpha: float) -> list[dict]:
    """The exact interval when every agent says yes, and when none does, against the closed forms."""
    unanimous = []
    for n in sizes:
        row = interval_row(n, n, alpha)
        closed = (alpha / 2.0) ** (1.0 / n)
        check("all-yes lower bound equals the closed form (alpha/2)^(1/n)", abs(row["lower"] - closed) < 1e-6,
              f"n={n}")
        zero_upper = clopper_pearson(0, n, alpha)[1]
        check("no-yes upper bound equals the closed form 1 - (alpha/2)^(1/n)", abs(zero_upper - (1.0 - closed)) < 1e-9,
              f"n={n}")
        row["lower_closed_form"] = prob(closed)
        row["no_yes_upper"] = prob(zero_upper)
        unanimous.append(row)
    return unanimous


def unanimous_group_needed(target_bound: Fraction, alpha: float) -> dict:
    """The smallest unanimous group whose lower bound reaches the target: by search, and by the closed form."""
    quotient = math.log(alpha / 2.0) / math.log(float(target_bound))
    agents = 1
    while below(clopper_pearson(agents, agents, alpha)[0], float(target_bound)):
        agents += 1
    check("the search for a unanimous group agrees with the closed form log(alpha/2) / log(bound), rounded up",
          agents == math.ceil(quotient) and agents > 1)
    return {"target_lower_bound": float(target_bound), "agents_needed_before_rounding_up": size(quotient),
            "agents_needed": agents, "lower_bound_there": prob(clopper_pearson(agents, agents, alpha)[0]),
            "lower_bound_one_agent_fewer": prob(clopper_pearson(agents - 1, agents - 1, alpha)[0])}


def every_count_rows(small: int, bounds: list[tuple[float, float]]) -> list[dict]:
    """The exact interval for each possible number of yes in the smallest group."""
    every = [{"yes": k, "share": prob(Fraction(k, small)), "lower": prob(low), "upper": prob(high),
              "width": prob(high - low)} for k, (low, high) in enumerate(bounds)]
    check("the intervals for k and n - k mirror each other",
          all(abs(bounds[k][0] - (1.0 - bounds[small - k][1])) < 1e-9 for k in range(small + 1)))
    check("the exact interval is widest at one half", max(every, key=lambda row: row["width"])["yes"] == small // 2)
    return every


def normal_approximation_targets(settings: dict, share: Fraction, small: int, z: float) -> list[dict]:
    """Group sizes that the normal approximation asks for, for each target half-width."""
    targets = []
    for text in settings["half_width_targets"]:
        target = Fraction(text)
        needed = z * z * float(share * (1 - share) / (target * target))
        targets.append({"half_width": float(target), "sd_of_the_share_needed": prob(float(target) / z),
                        "agents_needed_before_rounding_up": size(needed), "agents_needed": math.ceil(needed),
                        "times_the_smallest_group": size(Fraction(math.ceil(needed), small))})
    return targets


def exact_width_search(settings: dict, share: Fraction, alpha: float, z: float) -> dict:
    """From the normal approximation's size upwards, the first even group whose exact interval is narrow enough."""
    search = Fraction(settings["exact_search_half_width"])
    start = math.ceil(z * z * float(share * (1 - share) / (search * search)))
    n = start + start % 2
    width = interval_row(n // 2, n, alpha)["width"]
    check("the exact interval is wider than the normal approximation at the approximation's size", width > 2 * search)
    steps = 0
    while width > 2 * search:
        previous = width
        n, steps = n + 2, steps + 1
        width = interval_row(n // 2, n, alpha)["width"]
    return {"half_width": float(search), "normal_approximation_size_rounded_up_to_even": start + start % 2,
            "first_even_group_above_it_with_an_exact_width_within_target": n, "exact_width_there": width,
            "exact_width_two_agents_fewer": previous, "even_sizes_tried_above_the_approximation": steps}


def coverage_on_the_grid(grid: dict, small: int, bounds: list[tuple[float, float]], alpha: float,
                         z: float) -> tuple[dict, dict]:
    """How often the exact interval contains the yes probability, at each grid point; and, as a negative control,
    the Wald interval through the same test."""
    first, last, step = (Fraction(grid[key]) for key in ("from", "to", "step"))
    points = [first + i * step for i in range(int((last - first) / step) + 1)]
    coverage = {"exact": [], "wald": []}
    for point in points:
        value = float(point)
        pmf = binomial_pmf(small, value)
        coverage["exact"].append(math.fsum(q for k, q in enumerate(pmf)
                                           if not below(value, bounds[k][0]) and not below(bounds[k][1], value)))
        covered = []
        for k, q in enumerate(pmf):
            share_k = k / small
            reach = z * math.sqrt(share_k * (1.0 - share_k) / small)
            if not below(value, share_k - reach) and not below(share_k + reach, value):
                covered.append(q)
        coverage["wald"].append(math.fsum(covered))
    worst = {name: min(range(len(points)), key=lambda i: (values[i], i)) for name, values in coverage.items()}
    level = 1.0 - alpha
    check("the exact interval covers the yes probability at least 95% of the time at every grid point",
          not any(below(value, level) for value in coverage["exact"]))
    check("negative control: the same coverage test rejects the Wald interval",
          below(coverage["wald"][worst["wald"]], level))
    summary = {
        "agents": small, "grid_points": len(points), "grid": [float(first), float(last), float(step)],
        "lowest_coverage": prob(coverage["exact"][worst["exact"]]),
        "at_yes_probability": float(points[worst["exact"]]),
    }
    control = {"what_is_tested": "the Wald interval, share +/- z * sqrt(share * (1 - share) / n), put through the "
                                 "coverage test that the exact interval passes",
               "agents": small, "grid_points": len(points),
               "wald_lowest_coverage": prob(coverage["wald"][worst["wald"]]),
               "wald_lowest_coverage_at_yes_probability": float(points[worst["wald"]]),
               "wald_grid_points_below_the_nominal_level": sum(value < level for value in coverage["wald"]),
               "exact_grid_points_below_the_nominal_level": sum(value < level for value in coverage["exact"])}
    return summary, control


def independent_section(scenarios: dict, alpha: float, z: float) -> tuple[dict, dict, list[tuple[float, float]]]:
    """Section `independent_agents`: exact intervals for agents that answer independently; also returns the
    Wald-interval control and the exact interval of every count of the smallest group."""
    sizes = scenarios["group_sizes"]
    settings = scenarios["independent_agents"]
    share = Fraction(settings["observed_share_for_the_width_table"])
    half = half_yes_rows(sizes, share, alpha, z)
    unanimous = all_yes_rows(sizes, alpha)
    unanimous_target = unanimous_group_needed(Fraction(settings["all_yes_target_lower_bound"]), alpha)
    small = sizes[0]
    bounds = [clopper_pearson(k, small, alpha) for k in range(small + 1)]
    every = every_count_rows(small, bounds)
    targets = normal_approximation_targets(settings, share, small, z)
    exact_search = exact_width_search(settings, share, alpha, z)
    coverage, control = coverage_on_the_grid(settings["coverage_grid"], small, bounds, alpha, z)
    section = {
        "kind": "computed from assumed inputs: agents that answer independently with one yes probability",
        "confidence_level": 1.0 - alpha,
        "normal_quantile_z": prob(z),
        "half_yes": half,
        "all_yes": unanimous,
        "all_yes_group_needed_for_a_lower_bound": unanimous_target,
        "every_count_of_the_smallest_group": every,
        "agents_needed_normal_approximation": targets,
        "agents_needed_exact_search": exact_search,
        "coverage_of_the_exact_interval": coverage,
    }
    return section, control, bounds


def correlation_row(text: str, rho: Fraction, p: Fraction, sizes: list[int], tolerance: Fraction) -> dict:
    """One correlation of the copy model at every group size: the formulas against the exact mixture."""
    parts = shared_cause(rho, p)
    both_yes = (float(p) * parts["yes_if_signal_yes"] * parts["yes_if_signal_yes"]
                + (1.0 - float(p)) * parts["yes_if_signal_no"] * parts["yes_if_signal_no"])
    check("the copy model gives two agents the stated correlation",
          abs((both_yes - float(p * p)) / float(p * (1 - p)) - float(rho)) < 1e-12, f"rho={text}")
    rows = []
    for n in sizes:
        pmf = count_pmf(n, rho, p)
        mean, variance, _ = share_moments(pmf)
        formula = share_variance(n, rho, p)
        check("the count distribution sums to 1", abs(math.fsum(pmf) - 1.0) < 1e-12, f"n={n} rho={text}")
        check("every agent says yes with the stated probability", abs(mean - float(p)) < 1e-12, f"n={n} rho={text}")
        check("variance of the share: the exact mixture equals p(1-p)/n * (1 + (n-1) rho)",
              abs(variance - float(formula)) < 1e-12, f"n={n} rho={text}")
        rows.append({"agents": n, "design_effect": size(design_effect(n, rho)),
                     "effective_sample_size": size(effective_size(n, rho)),
                     "variance_of_the_share": prob(formula), "sd_of_the_share": prob(math.sqrt(float(formula))),
                     "probability_share_within_tolerance": prob(within_tolerance(pmf, p, tolerance)),
                     "probability_all_agents_agree": prob(pmf[0] + pmf[n])})
    if rho == 0:
        check("known answer: rho = 0 reproduces the binomial variance p(1-p)/n",
              all(share_variance(n, rho, p) == p * (1 - p) / n and effective_size(n, rho) == n for n in sizes))
    return {
        "pairwise_correlation": float(rho), "copy_probability": prob(parts["copy"]),
        "yes_probability_if_the_shared_signal_is_yes": prob(parts["yes_if_signal_yes"]),
        "yes_probability_if_the_shared_signal_is_no": prob(parts["yes_if_signal_no"]),
        "by_group_size": rows,
        "limit_for_a_very_large_group": {
            "effective_sample_size": None if rho == 0 else size(1 / rho),
            "sd_of_the_share": prob(math.sqrt(float(rho * p * (1 - p))))},
    }


def simulation_scores(stats: dict, exact: dict, fourth: float, p: Fraction, occasions: int) -> dict:
    """Simulated minus exact, in standard errors of the simulated value, for the mean, the variance and four shares."""
    variance = exact["variance_of_the_share"]
    errors = {"mean": math.sqrt(variance / occasions),
              "variance": math.sqrt((fourth - variance * variance) / occasions)}
    for key in ("all_agents_agree", "naive_interval_covers", "at_least_claimed_yes", "at_least_claimed_agree"):
        errors[key] = math.sqrt(exact[key] * (1.0 - exact[key]) / occasions)
    scores = {"mean": (stats["mean"] - float(p)) / errors["mean"],
              "variance": (stats["variance"] - variance) / errors["variance"],
              "all_agents_agree": (stats["unanimous"] - exact["all_agents_agree"]) / errors["all_agents_agree"]}
    for key in ("naive_interval_covers", "at_least_claimed_yes", "at_least_claimed_agree"):
        scores[key] = (stats[key] - exact[key]) / errors[key]
    return scores


def group_row(text: str, rho: Fraction, p: Fraction, alpha: float, covers: list[bool], yes: int,
              sim: dict) -> tuple[dict, dict, list[int]]:
    """The simulated group at one correlation: exact values, the seeded simulation, and their agreement.
    Returns the row of the result, the unrounded exact values and the simulated yes counts."""
    small, occasions, limit = sim["agents"], sim["occasions"], sim["agreement_tolerance_in_standard_errors"]
    pmf = count_pmf(small, rho, p)
    _, variance, fourth = share_moments(pmf)
    low, high = central_range(pmf, alpha)
    exact = {"variance_of_the_share": variance, "all_agents_agree": pmf[0] + pmf[small],
             "naive_interval_covers": math.fsum(q for k, q in enumerate(pmf) if covers[k]),
             "at_least_claimed_yes": math.fsum(pmf[yes:]),
             "at_least_claimed_agree": math.fsum(agreeing(pmf, yes))}
    counts = simulate(small, rho, p, occasions, sim["seeds"][text])
    histogram = [counts.count(k) for k in range(small + 1)]
    check("every simulated occasion is counted once", sum(histogram) == occasions == len(counts))
    stats = simulated_statistics(histogram)
    stats["naive_interval_covers"] = sum(h for k, h in enumerate(histogram) if covers[k]) / occasions
    stats["at_least_claimed_yes"] = sum(histogram[yes:]) / occasions
    stats["at_least_claimed_agree"] = sum(agreeing(histogram, yes)) / occasions
    scores = simulation_scores(stats, exact, fourth, p, occasions)
    check(f"simulation agrees with the exact values within {limit} standard errors",
          all(abs(score) < limit for score in scores.values()),
          f"rho={text} " + ", ".join(f"{key} z={score:.2f}" for key, score in scores.items()))
    row = {
        "pairwise_correlation": float(rho),
        "design_effect": size(design_effect(small, rho)),
        "effective_sample_size": size(effective_size(small, rho)),
        "exact": {
            "variance_of_the_share": prob(variance), "sd_of_the_share": prob(math.sqrt(variance)),
            "probability_all_agents_agree": prob(exact["all_agents_agree"]),
            "probability_all_agents_say_yes": prob(pmf[small]),
            "central_95_percent_range_of_the_yes_count": [low, high],
            "probability_inside_that_range": prob(math.fsum(pmf[low:high + 1])),
            "probability_the_independence_interval_contains_the_yes_probability": prob(exact["naive_interval_covers"]),
            f"probability_of_at_least_{yes}_yes": prob(exact["at_least_claimed_yes"]),
            f"probability_at_least_{yes}_agents_give_the_same_answer": prob(exact["at_least_claimed_agree"]),
        },
        "simulated": {
            "seed": sim["seeds"][text], "occasions": occasions,
            "mean_share": prob(stats["mean"]), "variance_of_the_share": prob(stats["variance"]),
            "variance_over_the_independent_variance": size(stats["variance"] / float(p * (1 - p) / small)),
            "estimated_pairwise_correlation": prob(stats["correlation"]),
            "share_of_occasions_all_agents_agree": prob(stats["unanimous"]),
            "share_of_occasions_the_independence_interval_contains_the_yes_probability":
                prob(stats["naive_interval_covers"]),
            f"share_of_occasions_with_at_least_{yes}_yes": prob(stats["at_least_claimed_yes"]),
            f"share_of_occasions_at_least_{yes}_agents_give_the_same_answer": prob(stats["at_least_claimed_agree"]),
        },
        "simulated_minus_exact_in_standard_errors": {key: zscore(score) for key, score in scores.items()},
    }
    return row, exact, counts


def wrong_correlation_control(model: dict, claim: dict, sim: dict, p: Fraction, counts_by_correlation: dict) -> dict:
    """Negative control: the agreement test must reject a simulation scored against the wrong correlation."""
    small, occasions, limit = sim["agents"], sim["occasions"], sim["agreement_tolerance_in_standard_errors"]
    wrong_text, right_text = model["pairwise_correlations"][0], claim["pairwise_correlation"]
    check("the negative control compares two different correlations", wrong_text != right_text)
    _, wrong_variance, wrong_fourth = share_moments(count_pmf(small, Fraction(wrong_text), p))
    right_counts = counts_by_correlation[right_text]
    simulated_variance = simulated_statistics([right_counts.count(k) for k in range(small + 1)])["variance"]
    wrong_score = ((simulated_variance - wrong_variance)
                   / math.sqrt((wrong_fourth - wrong_variance * wrong_variance) / occasions))
    check("negative control: a simulation scored against the wrong correlation is rejected", abs(wrong_score) >= limit)
    return {"simulated_with_pairwise_correlation": float(Fraction(right_text)),
            "scored_against_pairwise_correlation": float(Fraction(wrong_text)),
            "variance_difference_in_standard_errors": zscore(wrong_score),
            "tolerance_in_standard_errors": limit, "passes_the_agreement_test": abs(wrong_score) < limit}


def stated_against_files(stated: int, held: int, rhos: list[Fraction], p: Fraction) -> dict:
    """The assumed model at the record's group size and at the observed number of persona files."""
    return {
        "kind": "computed: the record's group size and the observed number of persona files, in the assumed model",
        "stated_personas": stated, "persona_files": held,
        "by_correlation": [{
            "pairwise_correlation": float(rho),
            "effective_sample_size_with_the_stated_personas": size(effective_size(stated, rho)),
            "effective_sample_size_with_the_persona_files": size(effective_size(held, rho)),
            "sd_of_the_share_with_the_stated_personas": prob(math.sqrt(float(share_variance(stated, rho, p)))),
            "sd_of_the_share_with_the_persona_files": prob(math.sqrt(float(share_variance(held, rho, p)))),
        } for rho in rhos],
    }


def shared_section(snapshot: dict, scenarios: dict, alpha: float,
                   bounds: list[tuple[float, float]]) -> tuple[dict, dict, dict, dict]:
    """Section `shared_cause`: the copy model at every correlation; also returns the wrong-correlation control,
    the simulated yes counts and the unrounded exact values, by correlation."""
    model = scenarios["shared_cause_model"]
    sim = scenarios["simulation"]
    sizes = scenarios["group_sizes"]
    p, tolerance = Fraction(model["yes_probability"]), Fraction(model["tolerance_around_the_yes_probability"])
    rhos = [Fraction(text) for text in model["pairwise_correlations"]]
    small = sim["agents"]
    stated, held = snapshot["department_record"]["stated_personas"], snapshot["counts"]["persona_files"]
    check("the simulated group is the smallest group of the tables and the number of personas the record states",
          small == sizes[0] == len(bounds) - 1 == stated)
    covers = [not below(float(p), low) and not below(high, float(p)) for low, high in bounds]
    claim = scenarios["imaginary_cases"]["dashboard_claim"]

    by_correlation, aggregate, counts_by_correlation, exact_by_correlation = [], [], {}, {}
    for text, rho in zip(model["pairwise_correlations"], rhos):
        by_correlation.append(correlation_row(text, rho, p, sizes, tolerance))
        row, exact_by_correlation[text], counts_by_correlation[text] = group_row(
            text, rho, p, alpha, covers, claim["yes"], sim)
        aggregate.append(row)

    check("the independence interval covers at least 95% when the agents are independent",
          aggregate[0]["exact"]["probability_the_independence_interval_contains_the_yes_probability"] >= 1.0 - alpha)
    check("more correlation means fewer effective agents",
          all(a["effective_sample_size"] > b["effective_sample_size"] for a, b in zip(aggregate, aggregate[1:])))
    control = wrong_correlation_control(model, claim, sim, p, counts_by_correlation)

    section = {
        "kind": "synthetic: an assumed generating model, its exact distribution, a formula and a seeded simulation",
        "model": model["note"],
        "yes_probability": float(p),
        "tolerance_around_the_yes_probability": float(tolerance),
        "formulas": {
            "design_effect": "1 + (n - 1) * rho",
            "effective_sample_size": "n / (1 + (n - 1) * rho), which tends to 1 / rho as n grows",
            "variance_of_the_share": "p * (1 - p) / n * (1 + (n - 1) * rho), which tends to rho * p * (1 - p)",
        },
        "by_correlation": by_correlation,
        "group_of_14": {"agents": small, "independence_interval_contains_the_yes_probability_for_yes_counts":
                        [k for k, inside in enumerate(covers) if inside], "by_correlation": aggregate},
        "stated_personas_against_persona_files": stated_against_files(stated, held, rhos, p),
    }
    return section, control, counts_by_correlation, exact_by_correlation


def second_model_section(scenarios: dict, alpha: float, bounds: list[tuple[float, float]]) -> dict:
    """Section `second_model`: a beta-binomial model with the same correlations, to show what depends on the model."""
    second = scenarios["second_model"]
    n, p = second["agents"], Fraction(scenarios["shared_cause_model"]["yes_probability"])
    yes = scenarios["imaginary_cases"]["dashboard_claim"]["yes"]
    check("the second model is evaluated on the group whose intervals were computed", n == len(bounds) - 1)
    check("known answer: the second model at rho = 1/3 and p = 1/2 gives every count the probability 1/(n+1)",
          beta_binomial_pmf(n, Fraction(1, 3), Fraction(1, 2)) == [Fraction(1, n + 1)] * (n + 1))
    covers = [not below(float(p), low) and not below(high, float(p)) for low, high in bounds]
    rows = []
    for text in second["pairwise_correlations"]:
        rho = Fraction(text)
        check("the second model is evaluated at correlations the first model also uses",
              text in scenarios["shared_cause_model"]["pairwise_correlations"] and rho > 0)
        pmf = beta_binomial_pmf(n, rho, p)
        mean = sum(Fraction(k, n) * q for k, q in enumerate(pmf))
        variance = sum((Fraction(k, n) - mean) ** 2 * q for k, q in enumerate(pmf))
        check("second model, exactly: probabilities sum to 1, the mean share is p and the variance of the share "
              "is p(1-p)/n * (1 + (n-1) rho)", (sum(pmf), mean, variance) == (1, p, share_variance(n, rho, p)))
        first = count_pmf(n, rho, p)
        low, high = central_range([float(q) for q in pmf], alpha)
        values = {"probability_all_agents_agree": (pmf[0] + pmf[n], first[0] + first[n]),
                  "probability_the_independence_interval_contains_the_yes_probability":
                      (sum(q for k, q in enumerate(pmf) if covers[k]),
                       math.fsum(q for k, q in enumerate(first) if covers[k])),
                  f"probability_of_at_least_{yes}_yes": (sum(pmf[yes:]), math.fsum(first[yes:])),
                  f"probability_at_least_{yes}_agents_give_the_same_answer":
                      (sum(agreeing(pmf, yes)), math.fsum(agreeing(first, yes)))}
        rows.append({
            "pairwise_correlation": float(rho),
            "beta_parameters_a_and_b": [size(p * (1 - rho) / rho), size((1 - p) * (1 - rho) / rho)],
            "variance_of_the_share": prob(variance), "sd_of_the_share": prob(math.sqrt(float(variance))),
            "central_95_percent_range_of_the_yes_count": [low, high],
            "second_model": {key: prob(pair[0]) for key, pair in values.items()},
            "first_model": {key: prob(pair[1]) for key, pair in values.items()},
            "second_over_first": {key: size(float(pair[0]) / pair[1]) for key, pair in values.items()},
        })
    return {
        "kind": "synthetic: a second assumed generating model with the same pairwise correlations, in exact fractions",
        "model": second["note"],
        "agents": n,
        "yes_probability": float(p),
        "what_is_the_same_by_construction": "the mean share and the variance of the share, hence the design effect "
                                            "and the effective sample size",
        "by_correlation": rows,
    }


def detection_rows(n: int, occasions: int, texts: list[str], plan: dict, counts_by_correlation: dict) -> list[dict]:
    """Cut each correlation's simulated occasions into logs, estimate the correlation in each log, and count the
    logs whose estimate exceeds the threshold set by the logs simulated without a shared cause. The same count is
    repeated in each half of the logs, with that half's own threshold, to show how much one seeded run can move."""
    rate = Fraction(plan["false_alarm_rate"])
    check("the measurement plan's reference is the simulation without a shared cause", Fraction(texts[0]) == 0)
    rows = []
    for length in plan["occasions_per_log"]:
        logs = occasions // length
        half = logs // 2
        check("the logs of a simulation split into two halves of equal size", logs == 2 * half and half > 0)
        halves = [slice(0, half), slice(half, logs)]
        estimates, in_order = {}, {}
        for text in texts:
            counts = counts_by_correlation[text]
            check("the simulated occasions fill whole logs", len(counts) == occasions and occasions % length == 0)
            values = [correlation_estimate(counts[i * length:(i + 1) * length], n) for i in range(logs)]
            check("every simulated log gives an estimate of the correlation", None not in values)
            estimates[text], in_order[text] = sorted(values), values
        threshold = percentile(estimates[texts[0]], 1 - rate)
        half_thresholds = [percentile(sorted(in_order[texts[0]][part]), 1 - rate) for part in halves]
        by_correlation, spread = [], Fraction(0)
        for text in texts:
            above = sum(value > threshold for value in estimates[text])
            in_halves = [Fraction(sum(value > limit for value in in_order[text][part]), half)
                         for part, limit in zip(halves, half_thresholds)]
            spread = max(spread, abs(in_halves[0] - in_halves[1]))
            by_correlation.append({
                "pairwise_correlation": float(Fraction(text)),
                "estimate_percentiles": {q: prob(percentile(estimates[text], Fraction(q)))
                                         for q in plan["report_percentiles"]},
                "logs_above_the_threshold": above,
                "share_of_logs_above_the_threshold": prob(Fraction(above, logs)),
                "share_above_its_own_threshold_in_each_half_of_the_logs": [prob(share) for share in in_halves],
            })
        check("at most the stated share of the logs without a shared cause exceed the threshold",
              by_correlation[0]["logs_above_the_threshold"] <= rate * logs)
        check("a larger correlation exceeds the threshold at least as often",
              all(a["logs_above_the_threshold"] <= b["logs_above_the_threshold"]
                  for a, b in zip(by_correlation, by_correlation[1:])))
        rows.append({"occasions_per_log": length, "answers_per_log": length * n, "logs_per_correlation": logs,
                     "threshold_on_the_estimate": prob(threshold),
                     "threshold_in_each_half_of_the_logs": [prob(limit) for limit in half_thresholds],
                     "largest_difference_between_the_shares_of_the_two_halves": prob(spread),
                     "by_correlation": by_correlation})
    return rows


def measurement_section(scenarios: dict, counts_by_correlation: dict) -> dict:
    """Section `measurement_plan`: how long a log of the simulated group must be before it shows a shared cause."""
    plan, sim = scenarios["measurement_plan"], scenarios["simulation"]
    texts = scenarios["shared_cause_model"]["pairwise_correlations"]
    check("hand-computed case: two agents who always agree give an estimate of 1, who never agree, -1",
          (correlation_estimate([2, 0], 2), correlation_estimate([1, 1], 2), correlation_estimate([2, 2], 2))
          == (1, -1, None))
    return {
        "kind": "synthetic: the simulated occasions of the copy model, cut into logs of a given length",
        "note": plan["note"],
        "estimator": "(share of agent pairs that both say yes - mean^2) / (mean * (1 - mean)), over the occasions "
                     "of one log, where mean is the share of yes among all its answers",
        "agents": sim["agents"],
        "false_alarm_rate": float(Fraction(plan["false_alarm_rate"])),
        "by_log_length": detection_rows(sim["agents"], sim["occasions"], texts, plan, counts_by_correlation),
    }


def panel_section(snapshot: dict, scenarios: dict, alpha: float) -> dict:
    """The assumed model at the size of the tribunal panel: what five answers are worth, and how long a log of
    panel verdicts would have to be before it showed a shared cause."""
    sizing, model, plan = scenarios["panel_sizing"], scenarios["shared_cause_model"], scenarios["measurement_plan"]
    texts, p = model["pairwise_correlations"], Fraction(model["yes_probability"])
    n, occasions, seeds = sizing["agents"], sizing["occasions"], sizing["seeds"]
    limit = scenarios["simulation"]["agreement_tolerance_in_standard_errors"]
    check("the sized group has the number of personas of the tribunal panel in the snapshot",
          n == snapshot["counts"]["tribunal_panel_personas"])
    check("the panel's simulation has one seed per correlation, none shared with the main simulation",
          sorted(seeds) == sorted(texts) and len(set(seeds.values())) == len(texts)
          and not set(seeds.values()) & set(scenarios["simulation"]["seeds"].values()))
    lower = clopper_pearson(n, n, alpha)[0]
    check("panel: the all-yes lower bound equals the closed form (alpha/2)^(1/n)",
          abs(lower - (alpha / 2.0) ** (1.0 / n)) < 1e-9)
    rows, counts_by_correlation = [], {}
    for text in texts:
        rho = Fraction(text)
        pmf = count_pmf(n, rho, p)
        mean, variance, fourth = share_moments(pmf)
        check("panel: the exact mixture has mean p and variance p(1-p)/n * (1 + (n-1) rho)",
              abs(mean - float(p)) < 1e-12 and abs(variance - float(share_variance(n, rho, p))) < 1e-12, f"rho={text}")
        counts = simulate(n, rho, p, occasions, seeds[text])
        counts_by_correlation[text] = counts
        histogram = [counts.count(k) for k in range(n + 1)]
        check("every simulated occasion is counted once", sum(histogram) == occasions == len(counts))
        stats = simulated_statistics(histogram)
        agree = pmf[0] + pmf[n]
        check("hand-computed case: five agents at p = 1/2 all agree with probability (1 + 10 rho + 5 rho^2) / 16",
              (n, p) != (5, Fraction(1, 2)) or abs(agree - float((1 + 10 * rho + 5 * rho * rho) / 16)) < 1e-12,
              f"rho={text}")
        scores = {"mean": (stats["mean"] - float(p)) / math.sqrt(variance / occasions),
                  "variance": (stats["variance"] - variance) / math.sqrt((fourth - variance * variance) / occasions),
                  "all_agents_agree": (stats["unanimous"] - agree) / math.sqrt(agree * (1.0 - agree) / occasions)}
        check(f"panel: simulation agrees with the exact values within {limit} standard errors",
              all(abs(score) < limit for score in scores.values()),
              f"rho={text} " + ", ".join(f"{key} z={score:.2f}" for key, score in scores.items()))
        rows.append({
            "pairwise_correlation": float(rho),
            "design_effect": size(design_effect(n, rho)),
            "effective_sample_size": size(effective_size(n, rho)),
            "sd_of_the_share": prob(math.sqrt(variance)),
            "probability_all_agents_agree": prob(agree),
            "simulated": {"seed": seeds[text], "occasions": occasions,
                          "variance_over_the_independent_variance": size(stats["variance"] / float(p * (1 - p) / n)),
                          "share_of_occasions_all_agents_agree": prob(stats["unanimous"])},
            "simulated_minus_exact_in_standard_errors": {key: zscore(score) for key, score in scores.items()},
        })
    return {
        "kind": "synthetic: the assumed copy model at the size of the tribunal panel found in the snapshot; this "
                "fixture did not run the panel and read no answer of a persona",
        "note": sizing["note"],
        "agents": n,
        "yes_probability": float(p),
        "lower_bound_of_the_exact_interval_if_all_agents_say_yes": prob(lower),
        "by_correlation": rows,
        "measurement_plan": {
            "false_alarm_rate": float(Fraction(plan["false_alarm_rate"])),
            "by_log_length": detection_rows(n, occasions, texts, plan, counts_by_correlation),
        },
    }


def band_share(n: int, p: Fraction, half_width: Fraction) -> Fraction:
    """Exact probability that the share of yes among n independent agents lies within half_width of p (inclusive)."""
    low, high = max(math.ceil((p - half_width) * n), 0), min(math.floor((p + half_width) * n), n)
    yes, no = p.numerator, p.denominator - p.numerator
    return Fraction(sum(math.comb(n, k) * yes ** k * no ** (n - k) for k in range(low, high + 1)), p.denominator ** n)


def exact_band_check(needed: int, p: Fraction, half_width: Fraction, level: Fraction, up_to: int) -> dict:
    """The normal approximation's group size against the exact binomial share of occasions within the half-width,
    and the group sizes at which that exact share reaches the target, from 1 to `up_to` agents."""
    check("hand-computed case: 20 independent agents at p = 1/2 fall within 5 points on "
          "(C(20, 9) + C(20, 10) + C(20, 11)) / 2^20 of occasions",
          band_share(20, Fraction(1, 2), Fraction(1, 20)) == Fraction(167960 + 184756 + 167960, 2 ** 20))
    check("the exact share within the half-width equals the summed binomial terms at the approximation's size",
          abs(float(band_share(needed, p, half_width))
              - within_tolerance(binomial_pmf(needed, float(p)), p, half_width)) < 1e-9)
    shares = {n: band_share(n, p, half_width) for n in range(1, up_to + 1)}
    check("the exact scan ends at a group size whose share reaches the target",
          up_to > needed + 1 and shares[up_to] >= level)
    stays = up_to
    while stays > 1 and shares[stays - 1] >= level:
        stays -= 1
    first = min(n for n, share in shares.items() if share >= level)
    return {
        "target_share_of_occasions": float(level),
        "exact_share_of_occasions_within_the_half_width": [{"agents": n, "share": prob(shares[n])}
                                                           for n in (needed - 1, needed, needed + 1)],
        "smallest_group_whose_exact_share_reaches_the_target": first,
        "smallest_group_from_which_every_exact_share_reaches_the_target": stays,
        "groups_between_those_two_whose_exact_share_falls_short": sum(shares[n] < level for n in range(first, stays)),
        "exact_shares_computed_up_to_agents": up_to,
    }


def imaginary_section(scenarios: dict, alpha: float, z: float, independent: dict, shared: dict,
                      exact_by_correlation: dict) -> dict:
    """Section `imaginary_cases`: the cases the lesson discusses, from values computed by the earlier sections."""
    cases = scenarios["imaginary_cases"]
    p = Fraction(scenarios["shared_cause_model"]["yes_probability"])
    group = cases["unanimous_group"]["agents"]
    all_yes = next(row for row in independent["all_yes"] if row["agents"] == group)

    claim = cases["dashboard_claim"]
    rho = Fraction(claim["pairwise_correlation"])
    n, yes = claim["agents"], claim["yes"]
    row = next(r for r in independent["every_count_of_the_smallest_group"] if r["yes"] == yes)
    one_sided, either_way = f"probability_of_at_least_{yes}_yes", f"probability_at_least_{yes}_agents_give_the_same_answer"
    tails = {key: {str(entry["pairwise_correlation"]): entry["exact"][key]
                   for entry in shared["group_of_14"]["by_correlation"]} for key in (one_sided, either_way)}
    check("hand-computed case: n = 14 and rho = 0.3 give 14 / 4.9 = 20/7 effective agents",
          effective_size(14, Fraction("0.3")) == Fraction(20, 7))
    independent_text = scenarios["shared_cause_model"]["pairwise_correlations"][0]
    check("the dashboard claim is compared with the independent case", Fraction(independent_text) == 0)
    times = (exact_by_correlation[claim["pairwise_correlation"]]["at_least_claimed_agree"]
             / exact_by_correlation[independent_text]["at_least_claimed_agree"])

    target = cases["precision_target"]
    half_width, target_rho = Fraction(target["half_width"]), Fraction(target["pairwise_correlation"])
    needed = z * z * float(p * (1 - p) / (half_width * half_width))
    ceiling = 1 / target_rho
    floor = math.sqrt(float(target_rho * p * (1 - p)))
    exact = exact_band_check(math.ceil(needed), p, half_width, Fraction(scenarios["confidence_level"]),
                             target["exact_check_up_to_agents"])
    return {
        "kind": "synthetic: cases the lesson discusses; none was observed",
        "unanimous_group": {"description": cases["unanimous_group"]["description"], "agents": group,
                            "lower": all_yes["lower"], "upper": all_yes["upper"]},
        "dashboard_claim": {
            "description": claim["description"], "agents": n, "yes": yes, "share": row["share"],
            "independence_interval": [row["lower"], row["upper"]],
            "pairwise_correlation": float(rho), "design_effect": size(design_effect(n, rho)),
            "effective_sample_size": size(effective_size(n, rho)),
            "sd_inflation_factor_sqrt_design_effect": size(math.sqrt(float(design_effect(n, rho)))),
            "yes_probability_under_which_the_tails_are_computed": float(p),
            one_sided: tails[one_sided],
            either_way: tails[either_way],
            "times_more_likely_than_under_independence_from_unrounded_probabilities": size(times),
        },
        "precision_target": {
            "description": target["description"], "half_width": float(half_width),
            "independent_agents_needed_before_rounding_up": size(needed), "independent_agents_needed": math.ceil(needed),
            "independent_agents_needed_is_from": "the normal approximation",
            "exact_binomial_check": exact,
            "sd_of_the_share_needed": prob(float(half_width) / z),
            "pairwise_correlation": float(target_rho), "effective_sample_size_ceiling": size(ceiling),
            "sd_of_the_share_floor": prob(floor),
            "reachable_by_adding_agents": bool(ceiling > needed),
        },
    }


def transfer_task(task: dict, alpha: float) -> dict:
    """Section `transfer_task`: the expected answers of the learner task, from its own inputs."""
    n, p, rho = task["reviewers"], Fraction(task["approval_probability"]), Fraction(task["pairwise_correlation"])
    target = Fraction(task["target_sd_of_the_share"])
    needed = p * (1 - p) / (target * target)
    all_yes_lower = clopper_pearson(n, n, alpha)[0]
    check("transfer task: all-yes lower bound equals the closed form", abs(all_yes_lower - (alpha / 2.0) ** (1.0 / n)) < 1e-9)
    boards = [{"reviewers": size_, "design_effect": size(design_effect(size_, rho)),
               "effective_sample_size": size(effective_size(size_, rho)),
               "sd_of_the_share": prob(math.sqrt(float(share_variance(size_, rho, p))))}
              for size_ in [n] + task["larger_boards"]]
    ceiling = 1 / rho
    parts = shared_cause(rho, p)
    pmf = count_pmf(n, rho, p)
    independent_all = float(p ** n)
    check("transfer task: the mixture's all-approve probability equals p*q1^n + (1-p)*q0^n",
          abs(pmf[n] - (float(p) * parts["yes_if_signal_yes"] ** n + float(1 - p) * parts["yes_if_signal_no"] ** n)) < 1e-12)
    check("transfer task, hand-computed: 20 reviewers at rho = 0.25 are worth 80/23, copying 0.5, yes 0.9 or 0.4",
          (n, rho) != (20, Fraction(1, 4)) or (effective_size(n, rho) == Fraction(80, 23) and parts["copy"] == 0.5
                                               and abs(parts["yes_if_signal_yes"] - 0.9) < 1e-12
                                               and abs(parts["yes_if_signal_no"] - 0.4) < 1e-12))
    return {
        "note": task["note"],
        "q1_independent_board": {
            "reviewers": n, "approval_probability": float(p),
            "sd_of_the_share": prob(math.sqrt(float(p * (1 - p) / n))),
            "target_sd_of_the_share": float(target),
            "independent_reviewers_needed": size(needed),
            "all_approve_lower_bound_95": prob(all_yes_lower),
        },
        "q2_shared_briefing": {"pairwise_correlation": float(rho)} | boards[0],
        "q3_larger_boards": {
            "boards": boards[1:], "effective_sample_size_ceiling": size(ceiling),
            "sd_of_the_share_floor": prob(math.sqrt(float(rho * p * (1 - p)))),
            "effective_sample_size_needed_for_the_target": size(needed),
            "target_reachable_by_adding_reviewers": bool(ceiling > needed),
        },
        "q4_unanimous_vote": {
            "copy_probability": prob(parts["copy"]),
            "approval_probability_if_the_briefing_says_approve": prob(parts["yes_if_signal_yes"]),
            "approval_probability_if_the_briefing_says_reject": prob(parts["yes_if_signal_no"]),
            "probability_all_approve_if_independent": prob(independent_all),
            "probability_all_approve_with_the_shared_briefing": prob(pmf[n]),
            "ratio": size(pmf[n] / independent_all),
        },
    }


def analyze(snapshot: dict, scenarios: dict) -> dict:
    """Run every section in order and assemble results.json; any failed self-check aborts before a result exists."""
    if scenarios["rounding"] != {f"{key}_decimals": value for key, value in DECIMALS.items()}:
        raise ValueError("scenarios.json rounding does not match analyze.py")
    if snapshot["module_id"] != scenarios["module_id"]:
        raise ValueError("observed-input.json and scenarios.json belong to different modules")
    alpha = float(1 - Fraction(scenarios["confidence_level"]))
    z = statistics.NormalDist().inv_cdf(1.0 - alpha / 2.0)

    check("hand-computed case: 1 yes of 2 gives the interval 1 - sqrt(0.975) to sqrt(0.975)",
          all(abs(a - b) < 1e-12 for a, b in zip(clopper_pearson(1, 2, 0.05), (1.0 - math.sqrt(0.975), math.sqrt(0.975)))))
    check("the binomial distribution by recurrence equals C(14, k) / 2^14",
          all(abs(q - math.comb(14, k) / 2 ** 14) < 1e-15 for k, q in enumerate(binomial_pmf(14, 0.5))))
    check("the binomial distribution sums to 1 for 10,000 agents", abs(math.fsum(binomial_pmf(10000, 0.3)) - 1.0) < 1e-12)

    observed, persona_control = observed_section(snapshot)
    independent, wald_control, bounds = independent_section(scenarios, alpha, z)
    shared, simulation_control, counts_by_correlation, exact_by_correlation = shared_section(
        snapshot, scenarios, alpha, bounds)
    second = second_model_section(scenarios, alpha, bounds)
    measurement = measurement_section(scenarios, counts_by_correlation)
    panel = panel_section(snapshot, scenarios, alpha)
    imaginary = imaginary_section(scenarios, alpha, z, independent, shared, exact_by_correlation)
    transfer = transfer_task(scenarios["transfer_task"], alpha)
    return {
        "module_id": snapshot["module_id"],
        "rounding": "probabilities, shares, variances and interval bounds to 6 decimals; group sizes, effective "
                    "sizes and ratios to 3 decimals; differences in standard errors to 2 decimals",
        "source": {"repository": snapshot["source"]["repository"], "commit": snapshot["source"]["commit"],
                   "files": [entry["path"] for entry in snapshot["source"]["files"]]},
        "observed": observed,
        "independent_agents": independent,
        "shared_cause": shared,
        "second_model": second,
        "measurement_plan": measurement,
        "tribunal_panel_sizing": panel,
        "imaginary_cases": imaginary,
        "negative_controls": {
            "kind": "each control feeds a test something it must reject or count, and records that it did",
            "count_of_reviews_by_a_persona_with_one_planted": persona_control,
            "coverage_test_on_the_wald_interval": wald_control,
            "agreement_test_on_a_simulation_with_the_wrong_correlation": simulation_control,
        },
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
