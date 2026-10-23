#!/usr/bin/env python3
"""PSY-006 analysis: a transition matrix estimated from label counts.

Reads observed-input.json (written by extract.py) and scenarios.json, never
the repository, and writes results.json. Counts, ratios and matrix results are
exact fractions. Each confidence bound is the solution of a binomial tail
equation, located between two neighbouring grid points by integer comparisons
and then rounded, so no stored digit depends on a floating-point library. No
random number is drawn.

Run from the repository root:
    python -I scripts/streeling_fixtures/psychohistory/psy-006/analyze.py
    python -I scripts/streeling_fixtures/psychohistory/psy-006/analyze.py --check
"""

from __future__ import annotations

import argparse
import copy
import json
import sys
from datetime import datetime, timezone
from decimal import Context, Decimal
from fractions import Fraction
from math import comb
from pathlib import Path

# This program lives under scripts/ (CONTRIBUTING.md: no executable code outside scripts/); its data stays
# under state/streeling/fixtures/. FIXTURE_FILE is the path the program would have next to that data.
FIXTURE_FILE = (Path(__file__).resolve().parents[4]
                / "state/streeling/fixtures/psychohistory/psy-006" / Path(__file__).name)

HERE = FIXTURE_FILE.parent
NO_ROW, NO_LABEL, SEED = ".", "-", "s"
DECIMALS = {"ratio": 6, "percent": 3, "day": 3}
LOG_CONTEXT = Context(prec=40)  # decimal logarithms are correctly rounded at this precision
CHECKS: dict[str, int] = {}  # self-check -> times evaluated


def check(name: str, condition: bool, detail: str = "") -> None:
    """A self-check that can fail: abort instead of writing a wrong result."""
    if not condition:
        raise AssertionError(f"self-check failed: {name}" + (f" ({detail})" if detail else ""))
    CHECKS[name] = CHECKS.get(name, 0) + 1


# ---------------------------------------------------------------- numbers

def rounded(value: Fraction | int, decimals: int) -> float:
    """Round an exact fraction half to even, then write it as the nearest float."""
    return round(Fraction(value) * 10**decimals) / 10**decimals


def frac(value: Fraction | int, exact: str | None = None) -> dict:
    """An exact fraction with its rounded value and its percentage."""
    value = Fraction(value)
    return {"exact": exact or str(value), "value": rounded(value, DECIMALS["ratio"]),
            "percent": rounded(100 * value, DECIMALS["percent"])}


def number(value: Fraction | int) -> dict:
    """An exact quantity that is not a probability: an expected count, a waiting time, a difference."""
    return {"exact": str(Fraction(value)), "value": rounded(value, DECIMALS["ratio"])}


def count_ratio(numerator: int, denominator: int) -> dict:
    """A ratio of two counts, kept unreduced so that both counts stay visible."""
    if denominator == 0:
        return {"exact": f"{numerator}/0", "value": None, "percent": None}
    return frac(Fraction(numerator, denominator), f"{numerator}/{denominator}")


def ln(value: Fraction) -> Decimal:
    """Natural logarithm as a 40-digit decimal (the decimal module rounds it correctly)."""
    return LOG_CONTEXT.ln(LOG_CONTEXT.divide(Decimal(value.numerator), Decimal(value.denominator)))


def log_ratio(numerator: Fraction, denominator: Fraction) -> Fraction:
    """ln(numerator) / ln(denominator)."""
    return Fraction(LOG_CONTEXT.divide(ln(numerator), ln(denominator)))


# ---------------------------------------------------------------- bounds

def tail_sign(events: int, trials: int, k: int, grid: int, alpha: Fraction) -> int:
    """Sign of P(X <= events) - alpha for X binomial(trials, k/grid), compared exactly."""
    q = grid - k
    tail = sum(comb(trials, i) * k**i * q**(trials - i) for i in range(events + 1))
    left, right = tail * alpha.denominator, alpha.numerator * grid**trials
    return (left > right) - (left < right)


def locate(events: int, trials: int, alpha: Fraction, grid: int) -> tuple[int, int, bool]:
    """Solve P(X <= events | trials, p) = alpha for p.

    Returns (low, high, exact) with high = low + 1: the solution lies strictly
    between low/grid and high/grid, or equals high/grid when `exact` is true.
    """
    if not 0 <= events < trials:
        raise ValueError(f"no bound below 1 for {events} events in {trials} trials")
    low, high = 0, grid  # the tail is 1 at p = 0 and 0 at p = 1
    while high - low > 1:
        middle = (low + high) // 2
        if tail_sign(events, trials, middle, grid, alpha) > 0:
            low = middle
        else:
            high = middle
    return low, high, tail_sign(events, trials, high, grid, alpha) == 0


def grid_numerator(low: int, high: int, exact: bool, grid: int, decimals: int) -> int:
    """The located solution rounded to `decimals`, as an integer numerator over 10**decimals."""
    if exact:
        return round(Fraction(high, grid) * 10**decimals)
    unit, remainder = divmod(grid, 10**decimals)
    if remainder or unit % 2:
        raise ValueError("the grid is too coarse for this rounding")
    base, rest = divmod(low, unit)
    return base + (2 * rest >= unit)  # the solution is strictly inside (low, low + 1): no tie


def bound(low: int, high: int, exact: bool, grid: int) -> dict:
    """A located bound as it is stored: rounded value, percentage, and the grid points around the solution."""
    digits = len(str(grid)) - 1
    return {"value": grid_numerator(low, high, exact, grid, DECIMALS["ratio"]) / 10**DECIMALS["ratio"],
            "percent": grid_numerator(low, high, exact, grid, DECIMALS["percent"] + 2) / 10**DECIMALS["percent"],
            "located": f"exactly 0.{high:0{digits}d}" if exact else f"between 0.{low:0{digits}d} and 0.{high:0{digits}d}"}


def upper_bound(events: int, trials: int, alpha: Fraction, grid: int) -> dict:
    """Largest p that `events` in `trials` does not reject: P(X <= events | p) = alpha."""
    return bound(*locate(events, trials, alpha, grid), grid)


def rule_of_three(trials: int, numerator: int, alpha: Fraction, grid: int) -> dict:
    """The exact upper bound for zero events in `trials`, against numerator / trials."""
    low, high, exact = locate(0, trials, alpha, grid)
    rule = Fraction(numerator, trials)
    excess = [rounded(100 * (rule / Fraction(edge, grid) - 1), 1) for edge in ((high, high) if exact else (high, low))]
    check("the rule of three's excess over the exact bound is the same at both ends of the located interval",
          excess[0] == excess[1], f"{trials} trials: {excess}")
    check("the rule of three is above the exact bound", rule > Fraction(high, grid))
    return {"trials": trials, "events": 0, "exact_upper_bound": bound(low, high, exact, grid),
            "rule_of_three": frac(rule, f"{numerator}/{trials}"), "rule_exceeds_exact_by_percent": excess[0]}


def trials_until(probability: Fraction, alpha: Fraction) -> int:
    """Smallest n with (1 - probability)^n <= alpha: event-free trials that reject `probability`."""
    n, power = 0, Fraction(1)
    while power > alpha:
        n, power = n + 1, power * (1 - probability)
    return n


def clean_run(probability: Fraction, alpha: Fraction) -> dict:
    """How many event-free trials reject `probability`, with the chance of such a run and of one a trial shorter."""
    n = trials_until(probability, alpha)
    return {"trials": n, "chance_of_that_many_event_free_trials": rounded((1 - probability) ** n, DECIMALS["ratio"]),
            "with_one_trial_fewer": rounded((1 - probability) ** (n - 1), DECIMALS["ratio"])}


# ---------------------------------------------------------------- chains

def solve(matrix: list[list], rhs: list) -> list[Fraction]:
    """Gauss-Jordan elimination in exact fractions; a singular system raises."""
    size = len(matrix)
    rows = [[Fraction(value) for value in row] + [Fraction(right)] for row, right in zip(matrix, rhs)]
    for column in range(size):
        pivot = next((r for r in range(column, size) if rows[r][column] != 0), None)
        if pivot is None:
            raise ArithmeticError("singular linear system")
        rows[column], rows[pivot] = rows[pivot], rows[column]
        rows[column] = [value / rows[column][column] for value in rows[column]]
        for r in range(size):
            if r != column and rows[r][column] != 0:
                factor = rows[r][column]
                rows[r] = [a - factor * b for a, b in zip(rows[r], rows[column])]
    return [row[-1] for row in rows]


def stationary(matrix: list[list[Fraction]]) -> list[Fraction]:
    """The distribution pi with pi P = pi and sum(pi) = 1 (unique for an irreducible chain)."""
    size = len(matrix)
    system = [[matrix[j][i] - (i == j) for j in range(size)] for i in range(size - 1)] + [[1] * size]
    return solve(system, [0] * (size - 1) + [1])


def hitting_times(matrix: list[list[Fraction]], target: int) -> dict[int, Fraction]:
    """Expected number of steps to first reach `target`, from every other state."""
    others = [i for i in range(len(matrix)) if i != target]
    system = [[(i == j) - matrix[i][j] for j in others] for i in others]
    return dict(zip(others, solve(system, [1] * len(others))))


def hit_within(matrix: list[list[Fraction]], start: int, target: int, steps: int) -> Fraction:
    """P(a chain started at `start` is at `target` after one of its next `steps` steps)."""
    size = len(matrix)
    alive = [Fraction(i == start) for i in range(size)]
    for _ in range(steps):
        alive = [Fraction(0) if j == target else sum(alive[i] * matrix[i][j] for i in range(size)) for j in range(size)]
    return 1 - sum(alive)


def matrix_power(matrix: list[list[Fraction]], steps: int) -> list[list[Fraction]]:
    """The matrix multiplied by itself `steps` times, in exact fractions."""
    size = len(matrix)
    result = [[Fraction(i == j) for j in range(size)] for i in range(size)]
    for _ in range(steps):
        result = [[sum(result[i][k] * matrix[k][j] for k in range(size)) for j in range(size)] for i in range(size)]
    return result


# ---------------------------------------------------------------- counting

def label_rows(snapshot: dict) -> dict[str, list[tuple]]:
    """Per artifact, its rows in run order: (run_index, label or None, is_seed)."""
    runs = len(snapshot["runs"])
    table = {}
    for artifact in snapshot["artifacts"]:
        labels, flags = artifact["effectiveness_to"], artifact["baseline_flag"]
        if len(labels) != runs or len(flags) != runs:
            raise ValueError(f"{artifact['name']}: a string is not aligned with the {runs} runs")
        rows = []
        for index, (label, flag) in enumerate(zip(labels, flags)):
            if (label == NO_ROW) != (flag == NO_ROW):
                raise ValueError(f"{artifact['name']}: run {index} is a row in one string and not in the other")
            if label != NO_ROW:
                rows.append((index, None if label == NO_LABEL else label, flag == SEED))
        table[artifact["name"]] = rows
    return table


def consecutive_pairs(table: dict) -> tuple[list[dict], int]:
    """The unit of a transition: two consecutive rows of one artifact, both labelled."""
    pairs, row_pairs = [], 0
    for name, rows in table.items():
        for earlier, later in zip(rows, rows[1:]):
            row_pairs += 1
            if earlier[1] and later[1]:
                pairs.append({"artifact": name, "earlier_run": earlier[0], "later_run": later[0],
                              "from": earlier[1], "to": later[1], "from_seed_row": earlier[2]})
    return pairs, row_pairs


def count_matrix(pairs: list[dict], labels: list[str]) -> dict[str, dict[str, int]]:
    """Number of pairs from each label (row) to each label (column)."""
    counts = {a: {b: 0 for b in labels} for a in labels}
    for pair in pairs:
        counts[pair["from"]][pair["to"]] += 1
    return counts


def describe_counts(pairs: list[dict], labels: list[str]) -> dict:
    """The count matrix of a set of pairs, with its totals, its non-zero cells and its zero cells."""
    counts = count_matrix(pairs, labels)
    row_totals = {a: sum(counts[a].values()) for a in labels}
    column_totals = {b: sum(counts[a][b] for a in labels) for b in labels}
    stayed = sum(counts[a][a] for a in labels)
    cells = [counts[a][b] for a in labels for b in labels]
    check("row totals and column totals both sum to the pairs",
          sum(row_totals.values()) == sum(column_totals.values()) == len(pairs))
    check("diagonal + off-diagonal counts = pairs", stayed + sum(p["from"] != p["to"] for p in pairs) == len(pairs))
    return {
        "pairs": len(pairs), "stayed": stayed, "changed": len(pairs) - stayed,
        "counts": counts, "row_totals": row_totals, "column_totals": column_totals,
        "nonzero_cells": {f"{a}>{b}": counts[a][b] for a in labels for b in labels if counts[a][b]},
        "cells": len(cells), "cells_with_a_count": sum(c > 0 for c in cells), "cells_at_zero": sum(c == 0 for c in cells),
        "cells_at_zero_in_a_row_without_pairs": sum(len(labels) for a in labels if row_totals[a] == 0),
        "cells_at_zero_in_a_row_with_pairs": sum(counts[a][b] == 0 for a in labels for b in labels if row_totals[a]),
    }


def maximum_likelihood(described: dict, labels: list[str]) -> dict:
    """Each row of counts divided by its total; a row without pairs has no estimate."""
    counts, totals = described["counts"], described["row_totals"]
    rows = {}
    for a in labels:
        n = totals[a]
        if n == 0:
            rows[a] = {"pairs": 0, "estimate": "undefined: 0/0, no pair starts at this label"}
            continue
        check("a maximum-likelihood row sums to 1", sum(Fraction(counts[a][b], n) for b in labels) == 1)
        rows[a] = {"pairs": n, "stayed": counts[a][a], "left": n - counts[a][a],
                   "stay": count_ratio(counts[a][a], n), "leave": count_ratio(n - counts[a][a], n),
                   "nonzero_estimates": {f"{a}>{b}": count_ratio(counts[a][b], n) for b in labels if counts[a][b]}}
    return {
        "rows": rows,
        "rows_without_a_pair": [a for a in labels if totals[a] == 0],
        "rows_with_pairs_and_no_exit": [a for a in labels if totals[a] and counts[a][a] == totals[a]],
        "rows_with_an_exit": [a for a in labels if counts[a][a] < totals[a]],
        "labels_never_reached": [b for b in labels if described["column_totals"][b] == 0],
    }


def literal_reading(described: dict, estimate: dict, labels: list[str]) -> dict:
    """What the estimated matrix says when its zeros are read as impossibilities."""
    counts, totals = described["counts"], described["row_totals"]
    leaving = {}
    for a in estimate["rows_with_an_exit"]:
        left = totals[a] - counts[a][a]
        stay = Fraction(counts[a][a], totals[a])
        check("expected stay 1/(1 - p_stay) solves h = 1 + p_stay h", 1 / (1 - stay) == 1 + stay / (1 - stay))
        leaving[a] = {"expected_pairs_until_it_leaves": number(1 / (1 - stay)),
                      "where_it_goes": {b: count_ratio(counts[a][b], left) for b in labels if b != a and counts[a][b]}}
    return {"labels_that_never_change": estimate["rows_with_pairs_and_no_exit"], "labels_that_change": leaving,
            "labels_with_no_statement": estimate["rows_without_a_pair"]}


# ---------------------------------------------------------------- sections

def bounds_on_leaving(described: dict, labels: list[str], rule: int, alpha: Fraction, grid: int) -> dict:
    """Per label, the upper bound on leaving it: from a row without an exit, or from the exits observed."""
    counts, totals = described["counts"], described["row_totals"]
    rows = {}
    for a in labels:
        n, left = totals[a], totals[a] - counts[a][a]
        if n == 0:
            rows[a] = {"pairs": 0, "upper_bound": "none below 1: no pair starts at this label"}
        elif left == 0:
            entry = rule_of_three(n, rule, alpha, grid)
            rows[a] = {"pairs": n, "exits": 0, "upper_bound": entry["exact_upper_bound"],
                       "rule_of_three": entry["rule_of_three"],
                       "rule_exceeds_exact_by_percent": entry["rule_exceeds_exact_by_percent"]}
        else:
            rows[a] = {"pairs": n, "exits": left, "estimate": count_ratio(left, n),
                       "upper_bound": upper_bound(left, n, alpha, grid),
                       "each_destination_never_observed": {
                           "destinations": [b for b in labels if counts[a][b] == 0],
                           "upper_bound": upper_bound(0, n, alpha, grid), "rule_of_three": frac(Fraction(rule, n), f"{rule}/{n}")}}
    return rows


def any_change(pairs: list[dict], rule: int, alpha: Fraction, grid: int) -> dict:
    """The upper bound on a pair changing its label, whatever the label."""
    n, changed = len(pairs), sum(p["from"] != p["to"] for p in pairs)
    if changed == 0:
        entry = rule_of_three(n, rule, alpha, grid)
        return {"pairs": n, "changed": 0, "upper_bound": entry["exact_upper_bound"], "rule_of_three": entry["rule_of_three"],
                "rule_exceeds_exact_by_percent": entry["rule_exceeds_exact_by_percent"]}
    return {"pairs": n, "changed": changed, "estimate": count_ratio(changed, n),
            "upper_bound": upper_bound(changed, n, alpha, grid)}


def smoothed(row: dict[str, int], pseudo: Fraction, spread: list[str]) -> dict[str, Fraction]:
    """(count + pseudo) / (row total + pseudo * number of labels), over the labels in `spread`."""
    if any(count and label not in spread for label, count in row.items()):
        raise ValueError("a count lies outside the labels the pseudo-counts are spread over")
    total = sum(row.values()) + pseudo * len(spread)
    result = {b: (row[b] + pseudo) / total for b in spread}
    check("a smoothed row sums to 1", sum(result.values()) == 1)
    return result


def smoothed_rows(described: dict, pseudo: Fraction, spread: list[str], cell_by_cell: bool,
                  alpha: Fraction, grid: int) -> dict:
    """Every row smoothed with one pseudo-count over one set of labels; a row without an exit against its bound."""
    counts, totals = described["counts"], described["row_totals"]
    rows = {}
    for a in spread:
        row, n = smoothed(counts[a], pseudo, spread), totals[a]
        leave = 1 - row[a]
        entry = {"pairs": n, "stay": frac(row[a]), "leave_in_total": frac(leave)}
        if n and counts[a][a] == n:
            low, high, exact = locate(0, n, alpha, grid)
            entry["upper_bound_on_leaving"] = bound(low, high, exact, grid)["value"]
            entry["leave_exceeds_the_upper_bound"] = leave > Fraction(high, grid)
            entry["chance_of_no_exit_in_these_pairs_if_the_smoothed_value_were_true"] = rounded(
                (1 - leave) ** n, DECIMALS["ratio"])
            check("smoothed exit mass against the bound is decided outside the located interval",
                  leave > Fraction(high, grid) or leave < Fraction(low, grid))
            check("exit mass above the bound <=> zero exits in n trials rejects that mass",
                  (leave > Fraction(high, grid)) == ((1 - leave) ** n < alpha))
        if cell_by_cell:
            entry["probabilities"] = {f"{a}>{b}": frac(row[b]) for b in spread}
        rows[a] = entry
    return rows


def smoothing_examples(described: dict, seed_step: dict, labels: list[str]) -> dict:
    """Add-one on a row with few pairs (U among the pairs that start at a seed row) and on the row with most pairs."""
    counts, totals = described["counts"], described["row_totals"]
    few_label = "U"
    few = seed_step["counts"][few_label]
    few_n = sum(few.values())
    few_row = smoothed(few, Fraction(1), labels)
    few_entry = {"label": few_label, "pairs": few_n, "counts": {b: c for b, c in few.items() if c},
                 "maximum_likelihood": {f"{few_label}>{b}": count_ratio(c, few_n) for b, c in few.items() if c},
                 "add_1_over_the_6_declared_labels": {f"{few_label}>{b}": frac(few_row[b]) for b in labels},
                 "stay_moves_by": number(few_row[few_label] - Fraction(few[few_label], few_n)),
                 "mass_on_destinations_never_observed": frac(sum(few_row[b] for b in labels if few[b] == 0))}
    many_label = max(labels, key=lambda a: totals[a])
    many_row = smoothed(counts[many_label], Fraction(1), labels)
    many_entry = {"label": many_label, "pairs": totals[many_label],
                  "stay_moves_by": number(many_row[many_label] - Fraction(counts[many_label][many_label], totals[many_label])),
                  "mass_on_destinations_never_observed": frac(sum(many_row[b] for b in labels if counts[many_label][b] == 0))}
    return {"row_with_few_pairs": few_entry, "row_with_most_pairs": many_entry}


def exit_mass_scan(pseudo_counts: list[str], label_counts: tuple[int, int], limit: int, alpha: Fraction) -> dict:
    """From how many pairs with no exit does a smoothed exit mass exceed the exact upper bound?"""
    scan = {}
    for text in pseudo_counts:
        pseudo = Fraction(text)
        for k in label_counts:
            exceeds = [((n + pseudo) / (n + k * pseudo)) ** n < alpha for n in range(1, limit + 1)]
            first = exceeds.index(True) + 1 if any(exceeds) else None
            scan[f"add_{text}_over_{k}_labels"] = {
                "exit_mass": f"{(k - 1) * pseudo} / (n + {k * pseudo})",
                "first_row_size_where_it_exceeds_the_bound": first,
                "exceeds_for_every_larger_row_size_scanned": bool(first) and all(exceeds[first - 1:]),
                "row_sizes_where_it_exceeds": sum(exceeds)}
    return scan


def smoothing_section(described: dict, seed_step: dict, labels: list[str], scenarios: dict, alpha: Fraction, grid: int) -> dict:
    """Add-one and add-0.5 smoothing of the count matrix, set against the bounds that the same counts give."""
    counts, totals = described["counts"], described["row_totals"]
    occurring = [a for a in labels if totals[a] or described["column_totals"][a]]
    variants = {}
    for text in scenarios["smoothing"]["pseudo_counts"]:
        pseudo = Fraction(text)
        for spread_name, spread in (("declared", labels), ("occurring", occurring)):
            rows = smoothed_rows(described, pseudo, spread, pseudo == 1 and spread == labels, alpha, grid)
            variants[f"add_{text}_over_the_{len(spread)}_{spread_name}_labels"] = {
                "pseudo_count": text, "labels": spread, "rows": rows,
                "rows_whose_exit_mass_exceeds_their_upper_bound": [a for a in spread if rows[a].get("leave_exceeds_the_upper_bound")]}

    main = variants[f"add_1_over_the_{len(labels)}_declared_labels"]["rows"]
    empty = [a for a in labels if totals[a] == 0]
    for a in empty:
        check("add-one on a row without pairs is the uniform row", set(smoothed(counts[a], Fraction(1), labels).values()) == {Fraction(1, len(labels))})
    examples = smoothing_examples(described, seed_step, labels)
    limit = scenarios["smoothing"]["scan_rows_up_to_pairs"]
    scan = exit_mass_scan(scenarios["smoothing"]["pseudo_counts"], (len(labels), len(occurring)), limit, alpha)
    return {
        "kind": "computed from the observed counts under an analysis choice (the pseudo-count and the labels it is spread over)",
        "formula": "smoothed p(a>b) = (n_ab + pseudo) / (n_a + pseudo * number of labels)",
        "labels_declared": labels, "labels_occurring": occurring,
        "row_without_pairs": {"labels": empty, "add_1_gives_every_destination": frac(Fraction(1, len(labels))),
                              "equals_a_uniform_row": True},
        **examples,
        "variants": variants,
        "exit_mass_against_the_upper_bound": {"row_sizes_scanned": [1, limit], "by_variant": scan},
        "main_variant_rows_checked": sorted(main),
    }


def seed_table_section(table: dict, between: dict, seed_step: dict, changes: list[dict], labels: list[str], steps: list[int]) -> dict:
    """Confront the seed table with the counts, if one of its steps were one pair."""
    weights = {tuple(key.split("->")): Fraction(str(value)) for key, value in table["transitions"].items()}
    forbidden = [tuple(key.split("->")) for key in table["forbidden"]]
    check("the seed table's states are the six labels", sorted(table["states"]) == sorted(labels))
    check("no seed-table transition is both weighted and forbidden", not set(weights) & set(forbidden))
    matrix = [[weights.get((a, b), Fraction(0)) for b in labels] for a in labels]
    check("every row of the seed table sums to 1", all(sum(row) == 1 for row in matrix))
    stay = {a: matrix[i][i] for i, a in enumerate(labels)}

    def expected(described: dict) -> dict:
        """Changes the table expects among these pairs, and the order of magnitude of P(no change)."""
        totals = described["row_totals"]
        by_label = {a: {"pairs": totals[a], "stay_weight": frac(stay[a]), "expected_changes": number(totals[a] * (1 - stay[a]))}
                    for a in labels if totals[a]}
        total = sum(totals[a] * (1 - stay[a]) for a in labels)
        no_change = Fraction(1)
        for a in labels:
            no_change *= stay[a] ** totals[a]
        exponent = len(str(no_change.numerator)) - len(str(no_change.denominator))
        while Fraction(10) ** exponent > no_change:
            exponent -= 1
        while Fraction(10) ** (exponent + 1) <= no_change:
            exponent += 1
        check("10^e <= P(no change) < 10^(e+1)", Fraction(10) ** exponent <= no_change < Fraction(10) ** (exponent + 1))
        return {"pairs": described["pairs"], "observed_changes": described["changed"], "expected_changes": number(total),
                "by_label": by_label, "probability_of_no_change_lies_between": [f"10^{exponent}", f"10^{exponent + 1}"],
                "floor_of_log10_of_that_probability": exponent}

    index = {a: i for i, a in enumerate(labels)}
    observed = []
    for change in changes:
        a, b = change["from"], change["to"]
        by_steps = {}
        for count in steps:
            by_steps[str(count)] = frac(matrix_power(matrix, count)[index[a]][index[b]])
        paths = {f"{a}>{m}>{b}": frac(matrix[index[a]][index[m]] * matrix[index[m]][index[b]])
                 for m in labels if matrix[index[a]][index[m]] * matrix[index[m]][index[b]]}
        check("two-step paths sum to the two-step probability",
              sum(matrix[index[a]][index[m]] * matrix[index[m]][index[b]] for m in labels) == matrix_power(matrix, 2)[index[a]][index[b]])
        observed.append({"artifact": change["artifact"], "from": a, "to": b, "gap_days": change["gap_days"],
                         "listed_as_forbidden": (a, b) in forbidden, "has_a_weight": (a, b) in weights,
                         "probability_after_steps": by_steps, "two_step_paths": paths})
    return {
        "kind": "observed seed table; the comparison is computed under a stated assumption",
        "path": table["path"], "machine": table["machine"], "machine_note": table["note"],
        "file_description": table["file_description"],
        "assumption": "one step of the table = one consecutive-row pair; the repository does not say how long a step is",
        "weighted_transitions": len(weights), "forbidden_transitions": [f"{a}>{b}" for a, b in forbidden],
        "cells_neither_weighted_nor_forbidden": len(labels) ** 2 - len(weights) - len(forbidden),
        "rows_sum_to_1": True, "stay_weights": {a: frac(stay[a]) for a in labels},
        "between_feeder_runs": expected(between), "from_a_seed_row": expected(seed_step),
        "observed_label_changes": observed,
    }


def governance_section(model: dict, questions: dict, alpha: Fraction) -> dict:
    """The stored 4-state matrix as observed, and what it asserts once it is read as a Markov chain."""
    stored, spec = model["transition_matrix"], model["specification"]
    states = stored["states"]
    matrix = [[Fraction(str(entry)) for entry in row] for row in stored["matrix"]]
    size = len(states)
    check("every row of the stored matrix sums to 1", all(sum(row) == 1 for row in matrix))
    uniform = all(entry == Fraction(1, size) for row in matrix for entry in row)
    start, target = states.index(questions["start_state"]), states.index(questions["target_state"])
    pi = stationary(matrix)
    check("the stationary distribution solves pi P = pi and sums to 1",
          sum(pi) == 1 and all(sum(pi[i] * matrix[i][j] for i in range(size)) == pi[j] for j in range(size)))
    times = hitting_times(matrix, target)
    p_next = matrix[start][target]
    within = {}
    for horizon in questions["horizons_cycles"]:
        within[str(horizon)] = hit_within(matrix, start, target, horizon)
        if uniform:
            check("uniform matrix: P(target within t) = 1 - (1 - 1/k)^t", within[str(horizon)] == 1 - (1 - Fraction(1, size)) ** horizon)
    if uniform:
        check("uniform matrix: the wait for the target is geometric with mean k", times[start] == size)
    half = next(t for t in range(1, 10_000) if hit_within(matrix, start, target, t) >= Fraction(1, 2))
    formula = log_ratio(Fraction(spec["freeze_formula"]["value"]), 1 - p_next)
    formula_3 = round(formula * 1000)
    check("the spec formula's value is bracketed exactly at three decimals",
          (1 - p_next) ** (2 * formula_3 - 1) > Fraction(spec["freeze_formula"]["value"]) ** 2000 > (1 - p_next) ** (2 * formula_3 + 1))
    threshold = Fraction(spec["alert_rule"]["value"])
    listing = model["folder"]["files"]
    check("positive control for the file-presence test: the matrix file is in the folder listing",
          stored["path"].rsplit("/", 1)[1] in listing)
    return {
        "kind": "observed files; the consequences are computed by reading the stored matrix as a Markov chain",
        "path": stored["path"], "description": stored["description"], "note": stored["note"], "created": stored["created"],
        "states": states, "matrix": [[str(entry) for entry in row] for row in matrix],
        "every_entry_is": str(matrix[0][0]) if uniform else None, "is_uniform": uniform,
        "all_rows_identical": all(row == matrix[0] for row in matrix),
        "equals_add_one_smoothing_of_a_row_without_observations": uniform,
        "predictions": {"path": model["predictions"]["path"], "entries": model["predictions"]["entries"]},
        "engine_state": {"path_in_the_specification": spec["engine_state_path"]["value"],
                         "named_by_the_matrix_note": model["folder"]["note_names_that_file"],
                         "present_in_the_folder": model["folder"]["that_file_is_in_the_folder"],
                         "files_in_the_folder": listing},
        "specification": {"path": spec["path"],
                          "lines": {key: spec[key]["line"] for key in ("freeze_formula", "alert_rule", "uniform_initialisation", "engine_state_path")},
                          "state_table_lines": spec["state_table_lines"],
                          "freeze_formula": spec["freeze_formula"]["text"], "alert_rule": spec["alert_rule"]["text"],
                          "uniform_initialisation": spec["uniform_initialisation"]["text"]},
        "as_a_chain": {
            "start_state": states[start], "target_state": states[target],
            "stationary_distribution": {state: frac(pi[i]) for i, state in enumerate(states)},
            "long_run_share_of_cycles_in_the_target_state": frac(pi[target]),
            "probability_of_the_target_at_the_next_cycle": frac(p_next),
            "probability_of_the_target_within_cycles": {key: frac(value) for key, value in within.items()},
            "expected_cycles_to_the_first_target": number(times[start]),
            "first_horizon_with_at_least_an_even_chance": half,
            "spec_formula_cycles_to_freeze": rounded(formula, 3),
            "spec_alert_threshold": frac(threshold),
            "spec_alert_emitted": p_next > threshold,
        },
        "what_observations_would_do": {
            "note": "event-free observed cycles treated as independent trials. A bound on one row needs cycles that start in "
                    "that row's state; the stored matrix gives the target the same probability from every state, so any "
                    "run of consecutive cycles without the target counts against it",
            "cycles_needed_to_reject_the_stored_probability": {"probability": str(p_next)} | clean_run(p_next, alpha),
            "cycles_needed_for_an_upper_bound_at_or_below": {text: clean_run(Fraction(text), alpha)
                                                             for text in questions["bound_thresholds"]},
            "state_sequences_recorded": model["predictions"]["entries"],
        },
    }


def sticky_section(model: dict, scenario: dict, questions: dict) -> dict:
    """A synthetic matrix with the stationary distribution of the stored one and another short-term behaviour."""
    states = model["transition_matrix"]["states"]
    size, keep = len(states), Fraction(scenario["stay_probability"])
    matrix = [[keep if i == j else (1 - keep) / (size - 1) for j in range(size)] for i in range(size)]
    check("every row of the sticky matrix sums to 1", all(sum(row) == 1 for row in matrix))
    start, target = states.index(questions["start_state"]), states.index(questions["target_state"])
    pi = stationary(matrix)
    times = hitting_times(matrix, target)
    check("sticky matrix: the wait for the target is geometric", times[start] == 1 / matrix[start][target])
    return {
        "kind": "synthetic: an imaginary matrix, not an estimate",
        "note": scenario["note"], "stay_probability": frac(keep), "probability_of_each_other_state": frac(matrix[0][1]),
        "stationary_distribution": {state: frac(pi[i]) for i, state in enumerate(states)},
        "same_stationary_distribution_as_the_stored_matrix": pi == stationary(
            [[Fraction(str(entry)) for entry in row] for row in model["transition_matrix"]["matrix"]]),
        "probability_of_the_target_at_the_next_cycle": frac(matrix[start][target]),
        "probability_of_the_target_within_cycles": {str(h): frac(hit_within(matrix, start, target, h))
                                                    for h in questions["horizons_cycles"]},
        "expected_cycles_to_the_first_target": number(times[start]),
    }


def negative_controls(snapshot: dict, labels: list[str], base: dict, rule: int, alpha: Fraction, grid: int) -> dict:
    """Plant a defect in a copy of the snapshot and confirm that each counter sees it."""
    target = next(a for a in snapshot["artifacts"] if set(a["effectiveness_to"]) == {"T"})
    index = len(snapshot["runs"]) // 2
    absent = base["rows_without_a_pair"][0]
    planted = copy.deepcopy(snapshot)
    artifact = next(a for a in planted["artifacts"] if a["name"] == target["name"])
    artifact["effectiveness_to"] = artifact["effectiveness_to"][:index] + absent + artifact["effectiveness_to"][index + 1:]
    pairs, _ = consecutive_pairs(label_rows(planted))
    described = describe_counts(pairs, labels)
    estimate = maximum_likelihood(described, labels)
    check("negative control: a planted label gives the absent label a row and a column",
          absent not in estimate["rows_without_a_pair"] and absent not in estimate["labels_never_reached"]
          and described["row_totals"][absent] == 1 and described["column_totals"][absent] == 1)
    check("negative control: the planted label ends the zero-exit row it was planted in",
          "T" not in estimate["rows_with_pairs_and_no_exit"] and "T" in base["rows_with_pairs_and_no_exit"]
          and described["counts"]["T"][absent] == 1)
    check("negative control: one planted label is counted as two changed pairs", described["changed"] == base["changed"] + 2)
    n = base["row_totals"]["T"]
    clean, dirty = upper_bound(0, n, alpha, grid), upper_bound(1, n, alpha, grid)
    check("negative control: one exit raises the upper bound", dirty["value"] > clean["value"])
    return {
        "planted_in": {"artifact": target["name"], "run_index": index, "run": snapshot["runs"][index]["timestamp"],
                       "observed_label": "T", "planted_label": absent},
        "rows_without_a_pair_before_and_after": [base["rows_without_a_pair"], estimate["rows_without_a_pair"]],
        "rows_with_pairs_and_no_exit_before_and_after": [base["rows_with_pairs_and_no_exit"], estimate["rows_with_pairs_and_no_exit"]],
        "changed_pairs_before_and_after": [base["changed"], described["changed"]],
        "cells_with_a_count_before_and_after": [base["cells_with_a_count"], described["cells_with_a_count"]],
        "upper_bound_on_leaving_T_with_0_and_with_1_exit": {"pairs": n, "with_0_exits": clean, "with_1_exit": dirty},
        "file_presence_test": "the test that finds no engine-state.json finds transition-matrix.json in the same listing",
    }


def transfer_task(task: dict, rule: int, alpha: Fraction, grid: int) -> dict:
    """The expected answers of the learner task, from the hypothetical counts in scenarios.json."""
    states, counts = task["states"], task["counts"]
    totals = {a: sum(counts[a].values()) for a in states}
    estimate = [[Fraction(counts[a][b], totals[a]) for b in states] for a in states]
    never = [(a, b) for a in states for b in states if counts[a][b] == 0]
    pseudo = Fraction(task["smoothing_pseudo_count"])
    smoothed_rows = {a: smoothed(counts[a], pseudo, states) for a in task["smoothing_rows"]}
    bounds = {f"{a}>{b}": rule_of_three(totals[a], rule, alpha, grid) for a, b in never}
    size = len(states)
    uniform = [[Fraction(1, size)] * size for _ in range(size)]
    start, target = states.index(task["start_state"]), states.index(task["target_state"])
    goal = Fraction(task["bound_target"])
    run = clean_run(goal, alpha)
    needed, have = run["trials"], totals[task["start_state"]]
    check("transfer task: target within two steps = direct + through each other state",
          hit_within(estimate, start, target, 2)
          == estimate[start][target] + sum(estimate[start][m] * estimate[m][target] for m in range(size) if m != target))
    return {
        "note": task["note"],
        "q1_estimate": {
            "pairs": sum(totals.values()), "row_totals": totals,
            "maximum_likelihood": {a: {f"{a}>{b}": count_ratio(counts[a][b], totals[a]) for b in states} for a in states},
            "transitions_never_observed": [f"{a}>{b}" for a, b in never]},
        "q2_bounds": bounds,
        "q3_add_one": {
            "pseudo_count": task["smoothing_pseudo_count"], "labels": size,
            "rows": {a: {f"{a}>{b}": frac(smoothed_rows[a][b]) for b in states} for a in smoothed_rows},
            "never_observed_cells": {f"{a}>{b}": {"smoothed": frac(smoothed_rows[a][b]),
                                                 "exact_upper_bound": bounds[f"{a}>{b}"]["exact_upper_bound"]["value"],
                                                 "smoothed_is_below_the_bound": smoothed_rows[a][b] < Fraction(
                                                     locate(0, totals[a], alpha, grid)[0], grid)}
                                     for a, b in never if a in smoothed_rows},
            "stay_moves_by": {a: number(smoothed_rows[a][a] - Fraction(counts[a][a], totals[a])) for a in smoothed_rows}},
        "q4_stored_uniform_matrix": {
            "every_entry_is": str(Fraction(1, size)),
            "probability_of_red_within_weeks": {str(h): frac(hit_within(uniform, start, target, h)) for h in task["horizons_steps"]},
            "expected_weeks_to_the_first_red": number(hitting_times(uniform, target)[start]),
            "long_run_share_of_weeks_in_red": frac(stationary(uniform)[target]),
            "event_free_green_weeks_that_reject_its_value": {"probability": str(uniform[start][target])}
            | clean_run(uniform[start][target], alpha),
            "estimated_matrix": {
                "probability_of_red_within_weeks": {str(h): frac(hit_within(estimate, start, target, h))
                                                    for h in task["estimated_matrix_horizons_steps"]},
                "expected_weeks_to_the_first_red": number(hitting_times(estimate, target)[start])}},
        "q5_plan": {
            "bound_target": frac(goal),
            "event_free_green_weeks_needed_in_total": needed, "chance_of_that_many_event_free_weeks_at_the_target": run[
                "chance_of_that_many_event_free_trials"], "with_one_week_fewer": run["with_one_trial_fewer"],
            "green_weeks_already_observed": have,
            "further_event_free_green_weeks_needed": needed - have,
            "rule_of_three_shortcut": {"weeks_in_total": number(Fraction(rule) / goal), "further_weeks": number(Fraction(rule) / goal - have)}},
    }


def hand_computed_cases(labels: list[str], alpha: Fraction, grid: int) -> None:
    """Small cases worked by hand in the README."""
    toy = {"runs": [{"timestamp": f"2026-01-0{day}T00:00:00Z"} for day in range(1, 5)],
           "artifacts": [{"name": "a", "effectiveness_to": "TTFF", "baseline_flag": "s---"},
                         {"name": "b", "effectiveness_to": ".P-P", "baseline_flag": ".---"}]}
    table = label_rows(toy)
    pairs, row_pairs = consecutive_pairs(table)
    described = describe_counts(pairs, labels)
    estimate = maximum_likelihood(described, labels)
    check("hand-computed counts: 7 rows, 5 row pairs, 3 usable pairs, T>T 1, T>F 1, F>F 1",
          (sum(map(len, table.values())), row_pairs, described["nonzero_cells"]) == (7, 5, {"T>T": 1, "T>F": 1, "F>F": 1}))
    check("hand-computed estimate: T stays 1/2, F has no exit, four labels have no row",
          (estimate["rows"]["T"]["stay"]["exact"], estimate["rows_with_pairs_and_no_exit"], len(estimate["rows_without_a_pair"]))
          == ("1/2", ["F"], 4))
    row = smoothed(described["counts"]["T"], Fraction(1), labels)
    check("hand-computed add-one row: T>T 2/8, T>F 2/8, each other label 1/8",
          (row["T"], row["F"], row["P"]) == (Fraction(2, 8), Fraction(2, 8), Fraction(1, 8)))
    if alpha == Fraction(1, 20):
        check("hand-computed bounds: 0 of 1 -> 0.95 exactly; 0 of 2 -> 1 - sqrt(0.05); 1 of 2 -> sqrt(0.95)",
              (upper_bound(0, 1, alpha, grid)["value"], locate(0, 1, alpha, grid)[2], upper_bound(0, 2, alpha, grid)["value"],
               upper_bound(1, 2, alpha, grid)["value"]) == (0.95, True, 0.776393, 0.974679))
    chain = [[Fraction(9, 10), Fraction(1, 10)], [Fraction(1, 2), Fraction(1, 2)]]
    check("hand-computed chain: stationary (5/6, 1/6), 10 steps expected to reach the second state, 19/100 within two",
          (stationary(chain), hitting_times(chain, 1)[0], hit_within(chain, 0, 1, 2))
          == ([Fraction(5, 6), Fraction(1, 6)], 10, Fraction(19, 100)))


# ---------------------------------------------------------------- analysis

def count_pairs(snapshot: dict, labels: list[str]) -> dict:
    """The pairs recounted from the label strings, described for all pairs and for each of the two step lengths."""
    table = label_rows(snapshot)
    pairs, row_pairs = consecutive_pairs(table)
    feeder_pairs = [p for p in pairs if not p["from_seed_row"]]
    seed_pairs = [p for p in pairs if p["from_seed_row"]]
    return {"table": table, "rows": sum(map(len, table.values())), "pairs": pairs, "row_pairs": row_pairs,
            "feeder_pairs": feeder_pairs, "seed_pairs": seed_pairs,
            "all_pairs": describe_counts(pairs, labels), "between": describe_counts(feeder_pairs, labels),
            "seed_step": describe_counts(seed_pairs, labels)}


def cross_checks(snapshot: dict, counted: dict, labels: list[str]) -> None:
    """The recount against the counts made by extract.py, and the accounting identities between the counts."""
    counts, extract_pairs = snapshot["counts"], snapshot["counts"]["consecutive_pairs"]
    table, pairs, rows, row_pairs = counted["table"], counted["pairs"], counted["rows"], counted["row_pairs"]
    all_pairs, between, seed_step = counted["all_pairs"], counted["between"], counted["seed_step"]
    check("recount of rows, runs and artifacts equals extract.py's counts",
          (rows, len(snapshot["runs"]), len(table)) == (counts["rows"], counts["runs"], counts["artifacts"]))
    check("recount of pairs equals extract.py's counts",
          (row_pairs, all_pairs["pairs"], all_pairs["changed"], all_pairs["stayed"], seed_step["pairs"], between["pairs"])
          == tuple(extract_pairs[key] for key in ("row_pairs", "usable_pairs", "changed", "unchanged",
                                                  "usable_pairs_from_a_seed_row", "usable_pairs_between_feeder_runs")))
    check("recount of the transition counts equals extract.py's counts", all_pairs["nonzero_cells"] == counts["transition_counts"])
    check("row pairs = rows - artifacts", row_pairs == rows - len(table))
    check("usable pairs = row pairs - pairs without a label", all_pairs["pairs"] == row_pairs - extract_pairs["pairs_without_a_label"])
    check("pairs from a seed row + pairs between feeder runs = usable pairs", seed_step["pairs"] + between["pairs"] == all_pairs["pairs"])
    check("the two subsets' count matrices add up to the matrix of all pairs",
          all(between["counts"][a][b] + seed_step["counts"][a][b] == all_pairs["counts"][a][b] for a in labels for b in labels))
    check("every pair joins two neighbouring runs", all(p["later_run"] == p["earlier_run"] + 1 for p in pairs))
    check("the changed pairs are the label changes listed by extract.py",
          [(p["artifact"], p["from"], p["to"]) for p in pairs if p["from"] != p["to"]]
          == [(c["artifact"], c["from"], c["to"]) for c in snapshot["label_changes"]])


def run_timing(snapshot: dict, table: dict) -> dict:
    """The runs that hold seed rows, and the gaps in days between consecutive runs."""
    stamps = [datetime.strptime(run["timestamp"], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc) for run in snapshot["runs"]]
    seed_runs = sorted({row[0] for artifact_rows in table.values() for row in artifact_rows if row[2]})
    check("the seed rows form the first run only", seed_runs == [0])
    gaps = [Fraction(int((later - earlier).total_seconds()), 86400) for earlier, later in zip(stamps, stamps[1:])]
    feeder_gaps = sorted(gaps[1:])
    middle = len(feeder_gaps) // 2
    median = feeder_gaps[middle] if len(feeder_gaps) % 2 else (feeder_gaps[middle - 1] + feeder_gaps[middle]) / 2
    return {"seed_runs": seed_runs, "seed_gap": gaps[0], "feeder_gaps": feeder_gaps, "median_feeder_gap": median}


def observed_section(snapshot: dict, counted: dict, timing: dict, labels: list[str]) -> dict:
    """What the snapshot holds: rows, runs, artifacts, pairs, labels and the two step lengths."""
    all_pairs, runs, feeder_gaps = counted["all_pairs"], snapshot["runs"], timing["feeder_gaps"]
    return {
        "kind": "observed: counted from observed-input.json",
        "rows": counted["rows"], "runs": len(runs), "seed_runs": len(timing["seed_runs"]),
        "feeder_runs": len(runs) - len(timing["seed_runs"]), "first_run": runs[0]["timestamp"],
        "first_feeder_run": runs[1]["timestamp"], "last_run": runs[-1]["timestamp"],
        "artifacts": len(counted["table"]), "row_pairs": counted["row_pairs"],
        "pairs_without_a_label": counted["row_pairs"] - all_pairs["pairs"],
        "usable_pairs": all_pairs["pairs"], "pairs_between_feeder_runs": counted["between"]["pairs"],
        "pairs_from_a_seed_row": counted["seed_step"]["pairs"],
        "labels_declared": snapshot["encoding"]["labels"],
        "labels_that_occur": [a for a in labels if all_pairs["row_totals"][a] or all_pairs["column_totals"][a]],
        "labels_never_recorded": [a for a in labels if not all_pairs["row_totals"][a] and not all_pairs["column_totals"][a]],
        "step_length_days": {"from_a_seed_row": rounded(timing["seed_gap"], DECIMALS["day"]),
                             "between_feeder_runs": {"gaps": len(feeder_gaps), "shortest": rounded(feeder_gaps[0], DECIMALS["day"]),
                                                     "median": rounded(timing["median_feeder_gap"], DECIMALS["day"]),
                                                     "longest": rounded(feeder_gaps[-1], DECIMALS["day"])}},
        "label_changes": snapshot["label_changes"],
    }


def estimates_by_step(counted: dict, labels: list[str]) -> dict:
    """The maximum-likelihood matrix of all pairs and of each of the two step lengths."""
    estimates = {"all_pairs": maximum_likelihood(counted["all_pairs"], labels),
                 "between_feeder_runs": maximum_likelihood(counted["between"], labels),
                 "from_a_seed_row": maximum_likelihood(counted["seed_step"], labels)}
    check("between feeder runs the estimated matrix is the identity on the labels that occur",
          counted["between"]["changed"] == 0 and not estimates["between_feeder_runs"]["rows_with_an_exit"])
    return estimates


def per_artifact_bounds(pairs: list[dict], labels: list[str], alpha: Fraction, grid: int) -> dict:
    """Per label, the artifacts that ever held it and those that left it, one artifact counting as one trial."""
    by_label = {}
    for a in labels:
        held = len({p["artifact"] for p in pairs if p["from"] == a})
        left = len({p["artifact"] for p in pairs if p["from"] == a and p["to"] != a})
        entry = {"artifacts_that_held_it": held, "of_which_left_it": left}
        if held == 0:
            entry["upper_bound"] = "none below 1: no artifact held this label"
        elif left == 0:
            entry["upper_bound"] = upper_bound(0, held, alpha, grid)
        elif left < held:
            entry |= {"estimate": count_ratio(left, held), "upper_bound": upper_bound(left, held, alpha, grid)}
        else:
            entry |= {"estimate": count_ratio(left, held), "upper_bound": "none below 1: every artifact that held it left it"}
        by_label[a] = entry
    return by_label


def per_run_bound(counted: dict, feeder_gaps: list[Fraction], alpha: Fraction, grid: int) -> dict:
    """One step between two feeder runs counting as one trial, whatever the number of pairs it holds."""
    feeder_pairs = counted["feeder_pairs"]
    run_steps = sorted({p["later_run"] for p in feeder_pairs})
    steps_with_a_change = sorted({p["later_run"] for p in feeder_pairs if p["from"] != p["to"]})
    check("the steps between feeder runs are the gaps between the feeder runs", len(run_steps) == len(feeder_gaps))
    per_run = {"steps_between_feeder_runs": len(run_steps), "steps_with_a_change": len(steps_with_a_change),
               "pairs_per_step_on_average": rounded(Fraction(counted["between"]["pairs"], len(run_steps)), DECIMALS["day"])}
    if not steps_with_a_change:
        per_run["upper_bound"] = upper_bound(0, len(run_steps), alpha, grid)
    return per_run


def other_trial_units(counted: dict, timing: dict, labels: list[str], alpha: Fraction, grid: int) -> dict:
    """The two parts of `bounds` whose trial is not a pair: an artifact, and a step between two feeder runs."""
    return {
        "per_artifact_over_the_record": {
            "note": "the extreme of dependence over time: an artifact's label is one assessment kept through the record, so "
                    "each artifact is one trial; of the artifacts that ever held a label, how many left it during the "
                    "record. The bound is on the chance that an artifact leaves the label at some point of the record",
            "by_label": per_artifact_bounds(counted["pairs"], labels, alpha, grid)},
        "one_trial_per_run": {
            "note": "the extreme of dependence between artifacts: the labels of a run change together or not at all, so each "
                    "step between two feeder runs is one trial; the chance that a given pair changes is then bounded by "
                    "this value instead of the bound of any_label_change.between_feeder_runs",
            **per_run_bound(counted, timing["feeder_gaps"], alpha, grid)},
    }


def minus_ln_alpha(alpha: Fraction, grid: int) -> Fraction:
    """-ln(alpha), the numerator behind the rule of three, checked against the exact bound at n = 1000."""
    ln_alpha = Fraction(ln(1 / alpha))
    probe = locate(0, 1000, alpha, grid)
    check("-ln(alpha) lies between n p and n p / (1 - p) for the exact bound p at n = 1000",
          1000 * Fraction(probe[0], grid) < ln_alpha < 1000 * Fraction(probe[1], grid) / (1 - Fraction(probe[1], grid)))
    return ln_alpha


def check_cycles_needed(governance: dict, alpha: Fraction, grid: int) -> None:
    """Each number of cycles announced for a bound is the first at which the exact bound reaches the threshold."""
    for text, run in governance["what_observations_would_do"]["cycles_needed_for_an_upper_bound_at_or_below"].items():
        check("the cycles needed for a bound are the first at which the exact bound is at or below the threshold",
              Fraction(locate(0, run["trials"], alpha, grid)[1], grid) <= Fraction(text)
              and Fraction(locate(0, run["trials"] - 1, alpha, grid)[0], grid) >= Fraction(text))


def bounds_section(counted: dict, labels: list[str], scenarios: dict, alpha: Fraction, grid: int,
                   ln_alpha: Fraction, other_units: dict) -> dict:
    """Upper bounds on leaving a label and on any change, and the rule of three set against the exact bound."""
    rule = scenarios["rule_of_three"]["numerator"]
    return {
        "kind": "computed from the observed counts, assuming that the trials counted are independent and share one probability",
        "confidence_level": scenarios["confidence"]["level"], "alpha": str(alpha), "one_sided": True,
        "definition": "upper bound for x events in n trials: the p with P(X <= x | n, p) = alpha, the largest probability "
                      "that the count does not reject at level alpha; for x = 0 this is 1 - alpha^(1/n)",
        "minus_ln_alpha": rounded(ln_alpha, 4),
        "leaving_a_label": {"all_pairs": bounds_on_leaving(counted["all_pairs"], labels, rule, alpha, grid),
                            "between_feeder_runs": bounds_on_leaving(counted["between"], labels, rule, alpha, grid)},
        "any_label_change": {"all_pairs": any_change(counted["pairs"], rule, alpha, grid),
                             "between_feeder_runs": any_change(counted["feeder_pairs"], rule, alpha, grid),
                             "from_a_seed_row": any_change(counted["seed_pairs"], rule, alpha, grid)},
        **other_units,
        "rule_of_three_against_exact": [rule_of_three(n, rule, alpha, grid) for n in scenarios["rule_of_three"]["sample_sizes"]],
    }


def analyze(snapshot: dict, scenarios: dict) -> dict:
    """One function per section of results.json, called in the order in which the self-checks are first evaluated."""
    if scenarios["rounding"] != {f"{key}_decimals": value for key, value in DECIMALS.items()}:
        raise ValueError("scenarios.json rounding does not match analyze.py")
    alpha = 1 - Fraction(scenarios["confidence"]["level"])
    grid = scenarios["bound_search"]["grid_steps"]
    rule = scenarios["rule_of_three"]["numerator"]
    labels = list(snapshot["encoding"]["labels"])
    hand_computed_cases(labels, alpha, grid)

    counted = count_pairs(snapshot, labels)
    cross_checks(snapshot, counted, labels)
    timing = run_timing(snapshot, counted["table"])
    estimates = estimates_by_step(counted, labels)
    other_units = other_trial_units(counted, timing, labels, alpha, grid)
    ln_alpha = minus_ln_alpha(alpha, grid)
    governance = governance_section(snapshot["stored_governance_model"], scenarios["governance_questions"], alpha)
    check_cycles_needed(governance, alpha, grid)

    all_pairs, between, seed_step = counted["all_pairs"], counted["between"], counted["seed_step"]
    base = {"rows_without_a_pair": estimates["all_pairs"]["rows_without_a_pair"],
            "rows_with_pairs_and_no_exit": estimates["all_pairs"]["rows_with_pairs_and_no_exit"],
            "changed": all_pairs["changed"], "cells_with_a_count": all_pairs["cells_with_a_count"],
            "row_totals": all_pairs["row_totals"]}
    return {
        "module_id": snapshot["module_id"],
        "rounding": "ratios to 6 decimals, percentages to 3 decimals, days to 3 decimals, exact fractions rounded half to even; "
                    "'exact' is the unrounded fraction",
        "source": {"repository": snapshot["source"]["repository"], "commit": snapshot["source"]["commit"],
                   "files": [entry["path"] for entry in snapshot["source"]["files"]]},
        "observed": observed_section(snapshot, counted, timing, labels),
        "count_matrix": {
            "kind": "computed: one count per ordered pair of labels, rows = earlier label, columns = later label",
            "all_pairs": all_pairs, "between_feeder_runs": between, "from_a_seed_row": seed_step,
        },
        "maximum_likelihood": {
            "kind": "computed: each row of counts divided by its row total",
            "formula": "estimate p(a>b) = n_ab / n_a",
            **estimates,
            "literal_reading_of_all_pairs": literal_reading(all_pairs, estimates["all_pairs"], labels),
        },
        "bounds": bounds_section(counted, labels, scenarios, alpha, grid, ln_alpha, other_units),
        "smoothing": smoothing_section(all_pairs, seed_step, labels, scenarios, alpha, grid),
        "belief_seed_table": seed_table_section(snapshot["belief_seed_table"], between, seed_step, snapshot["label_changes"],
                                                labels, scenarios["seed_table_reading"]["steps"]),
        "stored_governance_model": governance,
        "sticky_alternative": sticky_section(snapshot["stored_governance_model"], scenarios["sticky_alternative"],
                                             scenarios["governance_questions"]),
        "negative_controls": negative_controls(snapshot, labels, base, rule, alpha, grid),
        "transfer_task": transfer_task(scenarios["transfer_task"], rule, alpha, grid),
        "checks": [{"check": name, "times_evaluated": times, "passed": True} for name, times in CHECKS.items()],
    }


def main() -> int:
    """Write results.json; with --check, compare a fresh run with the saved file instead."""
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
