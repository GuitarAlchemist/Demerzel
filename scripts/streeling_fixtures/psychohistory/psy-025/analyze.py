#!/usr/bin/env python3
"""PSY-025 analysis: validate forecast records, take their base rate from the pinned history, and score them.

Reads observed-input.json (the module history and the library files at the
pinned commit, written by extract.py) and scenarios.json (the forecast records,
the expected verdicts, invented outcomes and assumptions), never the
repository, and writes results.json. Every probability and score is computed
with exact fractions and rounded only when it is written, so the file is the
same on every platform.

Run from the repository root:
    python -I -B scripts/streeling_fixtures/psychohistory/psy-025/analyze.py
    python -I -B scripts/streeling_fixtures/psychohistory/psy-025/analyze.py --check
"""

from __future__ import annotations

import argparse
import calendar
import copy
import json
import math
import re
import sys
from datetime import datetime
from fractions import Fraction
from pathlib import Path

# This program lives under scripts/ (CONTRIBUTING.md: no executable code outside scripts/); its data stays
# under state/streeling/fixtures/. FIXTURE_FILE is the path the program would have next to that data.
FIXTURE_FILE = (Path(__file__).resolve().parents[4]
                / "state/streeling/fixtures/psychohistory/psy-025" / Path(__file__).name)

HERE = FIXTURE_FILE.parent
DECIMALS = {"probability": 6, "score": 6, "interval": 4, "day": 3}
STAMP_FORMAT = "%Y-%m-%dT%H:%M:%SZ"
UTC_STAMP = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")
REPOSITORY = re.compile(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$")
HEX40 = re.compile(r"^[0-9a-f]{40}$")
LANGUAGE = re.compile(r"^[a-z]{2}$")
LANGUAGE_SUFFIX = re.compile(r"\.[a-z]{2}$")
DAY = 86400
BISECTION_STEPS = 48
RULES = {
    "R01": "id: missing or not unique",
    "R02": "question: not phrased as a question",
    "R03": "kind: must be 'probability' or 'interval'",
    "R04": "resolution_source: no repository named as owner/name",
    "R05": "resolution_source: no branch named",
    "R06": "resolution_source: does not say which commit is read",
    "R07": "resolution_time: not a UTC timestamp",
    "R08": "resolution_time: not later than written_at",
    "R09": "resolution_rule: does not say what counts, how often, and what does not",
    "R10": "resolution_rule: no rule for a moved or renamed source",
    "R11": "resolution_rule: no condition under which the forecast is void",
    "R12": "reference_class: missing",
    "R13": "base_rate: missing, or not a count of events among trials",
    "R14": "base_rate: no command and pinned commit to recompute it",
    "R15": "forecast: not a number the score can use (a probability from 0 to 1, or lower <= upper with "
           "0 < coverage < 1)",
    "R16": "reference_forecast: missing, of another form, or not the base rate",
    "R17": "adjustment: the forecast departs from its reference without a stated reason",
    "R18": "falsifier: no statement of the outcome that counts against the forecast",
    "R19": "falsifier: the stated outcomes are not those where the forecast scores worse than its reference",
    "R20": "author_can_influence_outcome: true or not stated (an outcome the record's author can steer is a plan "
           "to monitor, not a forecast to score)",
    "R21": "written_at: not a UTC timestamp",
    "R22": "written_at_evidence: does not say what, beyond the author's word, dates the record",
}
CHECKS: dict[str, int] = {}  # self-check -> times evaluated


def check(name: str, condition: bool, detail: str = "") -> None:
    """A self-check that can fail: abort instead of writing a wrong result."""
    if not condition:
        raise AssertionError(f"self-check failed: {name}" + (f" ({detail})" if detail else ""))
    CHECKS[name] = CHECKS.get(name, 0) + 1


def fix(value: Fraction | int, kind: str) -> float | int:
    """Exact rounding half away from zero to the stated decimals; integers stay integers."""
    if isinstance(value, int):
        return value
    scale = 10 ** DECIMALS[kind]
    scaled = abs(Fraction(value)) * scale
    whole = math.floor(scaled + Fraction(1, 2))
    return float(Fraction(whole if value >= 0 else -whole, scale)) + 0.0


def exact(number) -> Fraction:
    """A JSON number as the fraction its decimal text denotes (0.7 is 7/10, not the nearest double)."""
    return Fraction(str(number))


def seconds(stamp: str) -> int:
    return calendar.timegm(datetime.strptime(stamp, STAMP_FORMAT).timetuple())


def _format_utc(value: int) -> str:
    """Seconds since the Unix epoch as a UTC timestamp, by integer arithmetic only."""
    days, rest = divmod(value, DAY)
    date = datetime.fromordinal(datetime(1970, 1, 1).toordinal() + days)
    return f"{date:%Y-%m-%d}T{rest // 3600:02d}:{rest % 3600 // 60:02d}:{rest % 60:02d}Z"


# ---------------------------------------------------------------- counting rule

def parse_library_line(line: str) -> dict:
    path, module_id, department = line.split(" ")
    return {"path": path, "module_id": None if module_id == "-" else module_id,
            "department": None if department == "-" else department}


def rule_identity(entry: dict) -> tuple[str, str] | None:
    """(department, module id) of one file under the forecasts' counting rule; None when the file is excluded."""
    parts = entry["path"].split("/")
    name = parts[-1]
    if not name.endswith(".md") or name.lower() in ("readme.md", "index.md"):
        return None
    folder = next((part for part in reversed(parts[:-1]) if not LANGUAGE.match(part)), None)
    department = entry["department"] or folder
    if department is None:
        return None
    module_id = entry["module_id"] or LANGUAGE_SUFFIX.sub("", name[:-3])
    return department, module_id


def count_by_rule(entries: list[dict]) -> dict[str, int]:
    ids: dict[str, set[str]] = {}
    for entry in entries:
        identity = rule_identity(entry)
        if identity is not None:
            ids.setdefault(identity[0], set()).add(identity[1])
    return {department: len(ids[department]) for department in sorted(ids)}


def english_path(entry: dict) -> tuple[str, str] | None:
    """(department, name) for <department>/en/<name>.md, README.md excluded: the history's definition."""
    parts = entry["path"].split("/")
    if len(parts) == 3 and parts[1] == "en" and parts[2].endswith(".md") and parts[2].lower() != "readme.md":
        return parts[0], parts[2][:-3]
    return None


def count_by_path(entries: list[dict]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for entry in entries:
        found = english_path(entry)
        if found is not None:
            counts[found[0]] = counts.get(found[0], 0) + 1
    return {department: counts[department] for department in sorted(counts)}


def count_front_matter_only(entries: list[dict]) -> dict[str, int]:
    """The rule without its fallback: only files whose front matter names both a module_id and a department."""
    ids: dict[str, set[str]] = {}
    for entry in entries:
        if entry["module_id"] and entry["department"] and rule_identity(entry) is not None:
            ids.setdefault(entry["department"], set()).add(entry["module_id"])
    return {department: len(ids[department]) for department in sorted(ids)}


# ---------------------------------------------------------------- history and base rate

def history_events(obs: dict) -> list[tuple[int, str, int]]:
    """(time, department, +1 or -1) for every module added to or removed from an English folder."""
    events = []
    for row in obs["history"]:
        when = seconds(row["committed_utc"])
        events += [(when, name.split("/")[0], 1) for name in row["added"]]
        events += [(when, name.split("/")[0], -1) for name in row["removed"]]
    return events


def counts_at(events: list[tuple[int, str, int]], moment: int) -> dict[str, int]:
    counts: dict[str, int] = {}
    for when, department, step in events:
        if when <= moment:
            counts[department] = counts.get(department, 0) + step
    return counts


def window_classes(events: list, windows: list[tuple[int, int]]) -> dict:
    """Events and trials of the three reference classes over the given (start, end] windows."""
    broad = {"events": 0, "trials": 0, "rose": []}
    music = {"events": 0, "trials": 0}
    library = {"events": 0, "trials": 0}
    for start, end in windows:
        before, after = counts_at(events, start), counts_at(events, end)
        for department in sorted(before):
            if before[department] >= 1:
                broad["trials"] += 1
                if after.get(department, 0) > before[department]:
                    broad["events"] += 1
                    broad["rose"].append({"window_end_utc": _format_utc(end), "department": department,
                                          "count_at_start": before[department], "count_at_end": after[department]})
        if before.get("music", 0) >= 1:
            music["trials"] += 1
            music["events"] += after.get("music", 0) > before["music"]
        outside = [sum(c for d, c in table.items() if d != "psychohistory") for table in (before, after)]
        if outside[0] >= 1:
            library["trials"] += 1
            library["events"] += outside[1] > outside[0]
    return {"broad": broad, "music": music, "library_outside_psychohistory": library}


def binomial_tail(events: int, trials: int, rate: Fraction, upper: bool) -> Fraction:
    """P(X >= events) when upper, else P(X <= events), for X ~ Binomial(trials, rate), exactly."""
    ks = range(events, trials + 1) if upper else range(0, events + 1)
    return sum((math.comb(trials, k) * rate ** k * (1 - rate) ** (trials - k) for k in ks), Fraction(0))


def exact_interval(events: int, trials: int, level: Fraction = Fraction(95, 100)) -> dict:
    """Clopper-Pearson interval by bisection on exact binomial tails (PSY-017's construction)."""
    tail = (1 - level) / 2

    def solve(upper_tail: bool) -> float:
        low, high = Fraction(0), Fraction(1)
        for _ in range(BISECTION_STEPS):
            middle = (low + high) / 2
            value = binomial_tail(events, trials, middle, upper_tail)
            # P(X >= k) rises with the rate; P(X <= k) falls with it.
            if (value < tail) == upper_tail:
                low = middle
            else:
                high = middle
        check("exact interval: both ends of the final bisection bracket round to the same 4 decimals",
              fix(low, "interval") == fix(high, "interval"), f"{events}/{trials}")
        return fix((low + high) / 2, "interval")

    lower = 0.0 if events == 0 else solve(True)
    upper = 1.0 if events == trials else solve(False)
    return {"events": events, "trials": trials, "rate": fix(Fraction(events, trials), "probability"),
            "exact_95_interval": [lower, upper]}


def window_list(end: int, length: int, count: int) -> list[tuple[int, int]]:
    """Back-to-back (start, end] windows, oldest first, the last one ending at `end`."""
    return [(end - (i + 1) * length, end - i * length) for i in reversed(range(count))]


def alignment_table(events: list, pin: int, first: int, length: int, count: int, step: int) -> list[dict]:
    rows, k = [], 0
    while pin - k * step - count * length >= first:
        classes = window_classes(events, window_list(pin - k * step, length, count))
        rows.append({"days_before_pin": k, "broad_events": classes["broad"]["events"],
                     "broad_trials": classes["broad"]["trials"], "music_events": classes["music"]["events"],
                     "library_events": classes["library_outside_psychohistory"]["events"]})
        k += 1
    return rows


def base_rate_section(obs: dict, cfg: dict) -> dict:
    events = history_events(obs)
    pin, first = seconds(obs["counts"]["pin_commit_utc"]), seconds(obs["history"][0]["committed_utc"])
    length, step = cfg["window_days"] * DAY, cfg["alignment_step_days"] * DAY
    count = (pin - first) // length
    windows = window_list(pin, length, count)
    classes = window_classes(events, windows)
    times = sorted({when for when, _, _ in events})
    boundaries = [start for start, _ in windows] + [pin]
    nearest = [{"boundary_utc": _format_utc(b),
                "days_to_nearest_module_change": fix(Fraction(min(abs(t - b) for t in times if t != b), DAY), "day")}
               for b in boundaries[:-1]]
    table = alignment_table(events, pin, first, length, count, step)
    rates = sorted({Fraction(row["broad_events"], row["broad_trials"]) for row in table})
    below = exact(cfg["hypothesis_rate_below"])
    planted = events + [((windows[0][0] + windows[0][1]) // 2, "music", 1)]
    control = window_classes(planted, windows)
    check("negative control: a planted Music addition in the older window moves all three classes by one",
          (control["broad"]["events"], control["music"]["events"],
           control["library_outside_psychohistory"]["events"])
          == (classes["broad"]["events"] + 1, classes["music"]["events"] + 1,
              classes["library_outside_psychohistory"]["events"] + 1))
    check("alignment table: its first row is the alignment the records use", table[0]["broad_events"]
          == classes["broad"]["events"] and table[0]["broad_trials"] == classes["broad"]["trials"])
    return {
        "window_days": cfg["window_days"], "windows": [{"start_utc": _format_utc(s), "end_utc": _format_utc(e)}
                                                       for s, e in windows],
        "first_module_commit_utc": _format_utc(first),
        "classes": {
            "broad": {**exact_interval(classes["broad"]["events"], classes["broad"]["trials"]),
                      "rose": classes["broad"]["rose"]},
            "music_only": exact_interval(classes["music"]["events"], classes["music"]["trials"]),
            "library_outside_psychohistory": exact_interval(classes["library_outside_psychohistory"]["events"],
                                                            classes["library_outside_psychohistory"]["trials"])},
        "boundaries": nearest,
        "alignment": {"rows": table, "broad_rate_min": fix(rates[0], "probability"),
                      "broad_rate_max": fix(rates[-1], "probability"),
                      "days_before_pin_of_the_max": [row["days_before_pin"] for row in table
                                                     if Fraction(row["broad_events"], row["broad_trials"]) == rates[-1]],
                      "hypothesis_rate_below": cfg["hypothesis_rate_below"],
                      "days_before_pin_below_it": [row["days_before_pin"] for row in table
                                                   if Fraction(row["broad_events"], row["broad_trials"]) < below]},
        "negative_control_planted_music_addition": {"broad_events": control["broad"]["events"],
                                                    "music_events": control["music"]["events"],
                                                    "library_events": control["library_outside_psychohistory"]["events"]},
        "_classes": classes,
    }


# ---------------------------------------------------------------- the pinned library

def observed_section(obs: dict) -> dict:
    entries = [parse_library_line(line) for line in obs["library_files"]]
    by_rule, by_path, front_only = count_by_rule(entries), count_by_path(entries), count_front_matter_only(entries)
    replayed = {d: c for d, c in counts_at(history_events(obs), seconds(obs["counts"]["pin_commit_utc"])).items() if c}
    check("cross-check: the history replayed to the pin gives the per-department counts of the pinned tree",
          replayed == by_path, f"{replayed} against {by_path}")
    check("cross-check: the counting rule equals the English path count in every department", by_rule == by_path)
    no_front = sorted(e["path"] for e in entries if english_path(e) and not (e["module_id"] and e["department"]))
    english_ids = {rule_identity(e) for e in entries if english_path(e)}
    translations = [e for e in entries if rule_identity(e) and not english_path(e)]
    orphans = sorted(e["path"] for e in translations if rule_identity(e) not in english_ids)
    check("translations: every translated file carries the module id of an English module of its department",
          not orphans, f"{orphans[:3]}")
    planted = parse_library_line("music/fr/mus-099-planted.fr.md mus-099-planted music")
    check("negative control: a planted French file without an English module is found as an orphan",
          rule_identity(planted) not in english_ids and count_by_rule(entries + [planted])["music"] == by_rule["music"] + 1)
    total = {name: sum(table.values()) for name, table in
             (("rule", by_rule), ("english_paths", by_path), ("front_matter_only", front_only))}
    return {
        "library_files": len(entries),
        "english_module_paths": total["english_paths"],
        "translated_files_counted_once_with_their_english_module": len(translations),
        "translated_files_without_an_english_module": len(orphans),
        "negative_control_planted_orphan": {"found_as_orphan": rule_identity(planted) not in english_ids,
                                            "music_count_with_it": count_by_rule(entries + [planted])["music"]},
        "modules_by_rule": total["rule"],
        "modules_with_front_matter_only": total["front_matter_only"],
        "english_modules_without_front_matter": no_front,
        "departments_with_a_module": len(by_rule),
        "music": {"rule": by_rule.get("music", 0), "english_paths": by_path.get("music", 0),
                  "front_matter_only": front_only.get("music", 0)},
        "psychohistory": by_rule.get("psychohistory", 0),
        "outside_psychohistory": total["rule"] - by_rule.get("psychohistory", 0),
        "modules_by_department": by_rule,
    }


# ---------------------------------------------------------------- validator

def field(record: dict, dotted: str):
    value = record
    for key in dotted.split("."):
        if not isinstance(value, dict) or key not in value:
            return None
        value = value[key]
    return value


def text(value) -> bool:
    return isinstance(value, str) and value.strip() != ""


def number(value) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def parsed_stamp(value) -> int | None:
    if not (isinstance(value, str) and UTC_STAMP.match(value)):
        return None
    try:
        return seconds(value)
    except ValueError:
        return None


def forecast_form(kind, forecast) -> bool:
    if not isinstance(forecast, dict):
        return False
    if kind == "probability":
        return number(forecast.get("p")) and 0 <= forecast["p"] <= 1
    values = [forecast.get(key) for key in ("lower", "upper", "coverage")]
    return all(number(v) for v in values) and values[0] <= values[1] and 0 < values[2] < 1


def brier(p, outcome: int) -> Fraction:
    return (exact(p) - outcome) ** 2


def skill(mine: Fraction, ref: Fraction) -> float | None:
    """PSY-016's skill, 1 - BS / BS_ref on the same outcomes; undefined (None) when the reference makes no error."""
    return None if ref == 0 else fix(1 - mine / ref, "score")


def interval_score(lower, upper, coverage, x: int) -> Fraction:
    """Gneiting and Raftery (2007), eq. 43: width, plus 2/alpha times the distance by which x misses the interval."""
    lower, upper, alpha = exact(lower), exact(upper), 1 - exact(coverage)
    return (upper - lower) + 2 / alpha * max(lower - x, 0) + 2 / alpha * max(x - upper, 0)


def outcome_domain(kind: str, forecast: dict, reference: dict) -> range:
    """Probability: 0 and 1. Interval: counts 0 .. max(upper) + 2; beyond both intervals the difference of the two
    scores no longer depends on x, so this range shows every outcome at which the comparison can change."""
    if kind == "probability":
        return range(0, 2)
    return range(0, int(max(forecast["upper"], reference["upper"])) + 3)


def score(kind: str, forecast: dict, x: int) -> Fraction:
    if kind == "probability":
        return brier(forecast["p"], x)
    return interval_score(forecast["lower"], forecast["upper"], forecast["coverage"], x)


def worse_outcomes(kind: str, forecast: dict, reference: dict) -> list[int]:
    return [x for x in outcome_domain(kind, forecast, reference) if score(kind, forecast, x) > score(kind, reference, x)]


def stated_outcomes(ranges, domain: range) -> list[int] | None:
    if not isinstance(ranges, list) or not all(isinstance(r, list) and len(r) == 2 for r in ranges):
        return None
    chosen = set()
    for low, high in ranges:
        if not isinstance(low, int) or not (high is None or isinstance(high, int)):
            return None
        chosen |= {x for x in domain if low <= x and (high is None or x <= high)}
    return sorted(chosen)


def source_rules(record: dict, seen: set) -> list[tuple[str, bool]]:
    rule = record.get("resolution_rule")
    return [
        ("R01", text(record.get("id")) and record["id"] not in seen),
        ("R02", text(record.get("question")) and record["question"].rstrip().endswith("?")),
        ("R03", record.get("kind") in ("probability", "interval")),
        ("R04", text(field(record, "resolution_source.repository"))
         and bool(REPOSITORY.match(record["resolution_source"]["repository"]))),
        ("R05", text(field(record, "resolution_source.branch"))),
        ("R06", text(field(record, "resolution_source.commit_rule"))),
        ("R07", parsed_stamp(record.get("resolution_time")) is not None),
        ("R09", isinstance(rule, dict) and all(text(rule.get(key)) for key in ("counts", "unit", "excluded"))),
        ("R10", text(field(record, "resolution_rule.if_moved"))),
        ("R11", text(field(record, "resolution_rule.void_if"))),
        ("R12", text(record.get("reference_class"))),
    ]


def base_rate_ok(base) -> bool:
    return isinstance(base, dict) and all(isinstance(base.get(k), int) and not isinstance(base.get(k), bool)
                                          for k in ("events", "trials")) and 0 <= base["events"] <= base["trials"] \
        and base["trials"] >= 1


def forecast_rules(record: dict) -> tuple[list[tuple[str, bool]], list[str]]:
    """R13 to R19; also the rules that cannot be judged because a field they compare is unusable."""
    kind, base = record.get("kind"), record.get("base_rate")
    forecast, reference, falsifier = record.get("forecast"), record.get("reference_forecast"), record.get("falsifier")
    results = [("R13", base_rate_ok(base)),
               ("R14", isinstance(base, dict) and text(base.get("command")) and bool(HEX40.match(str(base.get("commit")))))]
    skipped = []
    if kind not in ("probability", "interval"):
        return results + [("R18", isinstance(falsifier, dict) and text(falsifier.get("statement")))], \
            ["R15", "R16", "R17", "R19"]
    usable, ref_usable = forecast_form(kind, forecast), forecast_form(kind, reference)
    same = ref_usable
    if ref_usable and kind == "probability" and base_rate_ok(base):
        same = exact(reference["p"]) == exact(fix(Fraction(base["events"], base["trials"]), "probability"))
    if ref_usable and kind == "interval" and usable:
        same = exact(reference["coverage"]) == exact(forecast["coverage"])
    results += [("R15", usable), ("R16", bool(same))]
    if usable and ref_usable:
        keys = ("p",) if kind == "probability" else ("lower", "upper", "coverage")
        departs = any(exact(forecast[k]) != exact(reference[k]) for k in keys)
        results.append(("R17", not departs or text(record.get("adjustment"))))
    else:
        skipped.append("R17")
    results.append(("R18", isinstance(falsifier, dict) and text(falsifier.get("statement"))))
    if usable and ref_usable and same and isinstance(falsifier, dict):
        domain = outcome_domain(kind, forecast, reference)
        results.append(("R19", stated_outcomes(falsifier.get("outcomes"), domain) == worse_outcomes(kind, forecast, reference)))
    else:
        skipped.append("R19")
    return results, skipped


def validate(record: dict, seen: set) -> dict:
    results = source_rules(record, seen)
    written, resolves = parsed_stamp(record.get("written_at")), parsed_stamp(record.get("resolution_time"))
    skipped = []
    if written is not None and resolves is not None:
        results.append(("R08", resolves > written))
    else:
        skipped.append("R08")
    more, not_judged = forecast_rules(record)
    results += more + [("R20", record.get("author_can_influence_outcome") is False),
                       ("R21", written is not None), ("R22", text(record.get("written_at_evidence")))]
    skipped += not_judged
    failed = sorted(rule for rule, passed in results if not passed)
    check("validator: every rule is either judged once or reported as not judged",
          sorted([rule for rule, _ in results] + skipped) == sorted(RULES))
    return {"passes": not failed, "failed": failed, "messages": [RULES[rule] for rule in failed],
            "not_judged": sorted(skipped)}


def apply_change(record: dict, change: str, value) -> dict:
    copied = copy.deepcopy(record)
    paths = change.split("+")
    for path, item in zip(paths, value if len(paths) > 1 else [value]):
        target = copied
        keys = path.split(".")
        for key in keys[:-1]:
            target = target[key]
        target[keys[-1]] = item
    return copied


def validation_section(scenarios: dict) -> dict:
    records, expected = scenarios["records"], scenarios["expected_validation"]
    seen, verdicts = set(), {}
    for record in records:
        verdicts[record["id"]] = validate(record, seen)
        seen.add(record["id"])
        check("known answer: the validator fails exactly the rules expected for each record",
              verdicts[record["id"]]["failed"] == expected[record["id"]], f"{record['id']}: {verdicts[record['id']]}")
    by_id = {record["id"]: record for record in records}
    controls = []
    for case in scenarios["validator_controls"]["cases"]:
        verdict = validate(apply_change(by_id[case["record"]], case["change"], case["value"]), set())
        check("negative control: a changed copy of a worked record fails exactly the expected rules",
              verdict["failed"] == case["expected"], f"{case['change']}: {verdict['failed']}")
        controls.append({"record": case["record"], "change": case["change"], "failed": verdict["failed"]})
    return {"rules": RULES, "records": verdicts, "controls": controls}


# ---------------------------------------------------------------- scoring

def probability_scores(record: dict, outcomes: list[int]) -> dict:
    p, r = record["forecast"]["p"], record["reference_forecast"]["p"]
    rows = []
    for o in outcomes:
        mine, ref = brier(p, o), brier(r, o)
        check("Brier scores lie between 0 and 1", 0 <= mine <= 1 and 0 <= ref <= 1)
        rows.append({"outcome": o, "brier": fix(mine, "score"), "reference_brier": fix(ref, "score"),
                     "skill_against_reference": skill(mine, ref),
                     "worse_than_reference": mine > ref})
    return {"p": p, "reference_p": r, "outcomes": rows,
            "falsifying_outcomes": worse_outcomes("probability", record["forecast"], record["reference_forecast"])}


def interval_scores(record: dict, outcomes: list[int]) -> dict:
    f, ref = record["forecast"], record["reference_forecast"]
    rows = []
    for x in outcomes:
        mine = interval_score(f["lower"], f["upper"], f["coverage"], x)
        covered = f["lower"] <= x <= f["upper"]
        check("interval score: equals the width when the interval covers, exceeds it when it misses",
              (mine == f["upper"] - f["lower"]) == covered and mine >= f["upper"] - f["lower"])
        rows.append({"outcome": x, "covered": covered, "interval_score": fix(mine, "score"),
                     "reference_interval_score": fix(interval_score(ref["lower"], ref["upper"], ref["coverage"], x),
                                                     "score")})
    worse = worse_outcomes("interval", f, ref)
    return {"interval": [f["lower"], f["upper"]], "coverage": f["coverage"],
            "penalty_per_unit_outside": fix(2 / (1 - exact(f["coverage"])), "score"),
            "reference_interval": [ref["lower"], ref["upper"]], "outcomes": rows,
            "falsifying_outcomes": {"from": worse[0], "to": worse[-1], "count": len(worse),
                                    "contiguous": worse == list(range(worse[0], worse[-1] + 1))}}


def author_coverage(count: dict, rise: dict) -> dict:
    """The worked interval's coverage under its author's beliefs: the mass left on 19, plus the rest times the
    stated chance of the upper end or less if the count rises."""
    beliefs = count["author_beliefs"]
    stays = exact(beliefs["p_count_stays_19"])
    given = Fraction(*beliefs["p_at_most_upper_if_it_rises_at_least"])
    check("records: the interval's beliefs agree with the probability record (0.3 on 19 = 1 - 0.7, lower end 19)",
          stays == 1 - exact(rise["forecast"]["p"]) and count["forecast"]["lower"] == rise["value_at_writing"]["value"])
    return {"p_count_stays_19": fix(stays, "probability"),
            "p_at_most_upper_if_it_rises_at_least": fix(given, "probability"),
            "coverage_at_least": fix(stays + (1 - stays) * given, "probability"),
            "nominal_coverage": count["forecast"]["coverage"]}


def scoring_section(scenarios: dict, observed: dict, base: dict) -> dict:
    records = {record["id"]: record for record in scenarios["records"]}
    invented = scenarios["invented_outcomes"]
    rise, count = records["music-rise-2027-01-13"], records["music-count-2027-01-13"]
    repaired = records["library-growth-repaired"]
    broad, library = base["_classes"]["broad"], base["_classes"]["library_outside_psychohistory"]
    check("records: the worked records state the base rate computed from the history",
          all((r["base_rate"]["events"], r["base_rate"]["trials"]) == (broad["events"], broad["trials"])
              for r in (rise, count))
          and (repaired["base_rate"]["events"], repaired["base_rate"]["trials"]) == (library["events"], library["trials"]))
    check("records: the value at writing is the rule's count at the pin",
          rise["value_at_writing"]["value"] == count["value_at_writing"]["value"] == observed["music"]["rule"]
          and repaired["value_at_writing"]["value"] == observed["outside_psychohistory"])
    unchanged = Fraction(broad["trials"] - broad["events"], broad["trials"])
    alpha = 1 - exact(count["reference_forecast"]["coverage"])
    check("reference interval: the share of windows without change reaches 1 - alpha/2, so both reference "
          "quantiles are 'no change'", unchanged >= 1 - alpha / 2)
    check("hand-computed case: Brier(0.7, outcome 0) = 0.49 and the alpha = 0.2 interval score of [19, 25] at 28 is "
          "6 + 10 x 3 = 36", brier(0.7, 0) == Fraction(49, 100) and interval_score(19, 25, 0.8, 28) == 36)
    check("negative control: skill is undefined when the reference makes no error (a base rate of 0 events "
          "meeting outcome 0), and defined otherwise",
          skill(brier(0.7, 0), brier(0, 0)) is None and skill(brier(0.7, 0), brier(0.5, 0)) == -0.96)
    coverage = scenarios["coverage_scale"]
    tail = binomial_tail(coverage["covered_at_most"], coverage["intervals"], exact(coverage["coverage"]), False)
    return {
        "note": "Outcomes below are INVENTED (both possible outcomes for the probability record, five invented "
                "counts for the interval record); the real outcomes are unknown until 2027-01-13T23:59:59Z.",
        "music_rise": probability_scores(rise, invented["music-rise-2027-01-13"]),
        "music_count": interval_scores(count, invented["music-count-2027-01-13"]),
        "music_count_coverage_under_author_beliefs": author_coverage(count, rise),
        "library_growth_repaired": probability_scores(repaired, [0, 1]),
        "reference_interval_check": {"share_of_windows_without_change": fix(unchanged, "probability"),
                                     "one_minus_half_alpha": fix(1 - alpha / 2, "probability")},
        "coverage_scale": {"intervals": coverage["intervals"], "coverage": coverage["coverage"],
                           "covered_at_most": coverage["covered_at_most"], "probability": fix(tail, "probability")},
    }


# ---------------------------------------------------------------- exercises, transfer task

def exercises_section(scenarios: dict, base: dict, scoring: dict) -> dict:
    verbal = scenarios["verbal_probability"]
    layouts = []
    for case in scenarios["hypothetical_layouts"]["cases"]:
        counted = count_by_rule([parse_library_line(line) for line in case["files"]]).get(case["department"], 0)
        check("known answer: the counting rule gives the expected count on each invented layout",
              counted == case["expected_count"], case["id"])
        layouts.append({"id": case["id"], "count": counted})
    classes = base["classes"]
    broad, music = classes["broad"], classes["music_only"]
    inside = {"broad_rate_inside_music_interval": music["exact_95_interval"][0] <= broad["rate"] <= music["exact_95_interval"][1],
              "music_rate_inside_broad_interval": broad["exact_95_interval"][0] <= music["rate"] <= broad["exact_95_interval"][1]}
    picked = [row for row in scoring["music_count"]["outcomes"] if row["outcome"] in (18, 28)]
    # Music's two windows are among the broad class's (both require a module at the window's start).
    without = {"events": broad["events"] - music["events"], "trials": broad["trials"] - music["trials"]}
    without["rate"] = fix(Fraction(without["events"], without["trials"]), "probability")
    return {
        "exercise_1": {"word": verbal["word"], "readings": [
            {"p": p, "brier_if_it_happens": fix(brier(p, 1), "score"), "brier_if_not": fix(brier(p, 0), "score")}
            for p in verbal["readings"]]},
        "exercise_2": {"broad": {k: broad[k] for k in ("events", "trials", "rate", "exact_95_interval")},
                       "music_only": music, "broad_without_music": without, **inside},
        "exercise_3": {"layouts": layouts},
        "exercise_4": {"outcomes": picked},
        "exercise_5": scoring["library_growth_repaired"],
    }


def transfer_task(task: dict) -> dict:
    verdict = validate(task["draft_record"], set())
    check("known answer: the transfer draft fails exactly the expected rules", verdict["failed"] == task["expected_failures"])
    base = task["draft_record"]["base_rate"]
    interval = exact_interval(base["events"], base["trials"])
    p, r = task["draft_record"]["forecast"]["p"], task["draft_record"]["reference_forecast"]["p"]
    rows = [{"outcome": o, "brier": fix(brier(p, o), "score"), "reference_brier": fix(brier(r, o), "score"),
             "skill_against_reference": skill(brier(p, o), brier(r, o))} for o in (0, 1)]
    f, ref = task["interval"], task["reference_interval"]
    scores = [{"outcome": x, "covered": f["lower"] <= x <= f["upper"],
               "interval_score": fix(interval_score(f["lower"], f["upper"], f["coverage"], x), "score"),
               "reference_interval_score": fix(interval_score(ref["lower"], ref["upper"], ref["coverage"], x), "score")}
              for x in task["invented_outcomes"]]
    worse = worse_outcomes("interval", f, ref)
    return {
        "note": task["note"],
        "q1_validator": {"failed": verdict["failed"], "messages": verdict["messages"], "not_judged": verdict["not_judged"]},
        "q2_base_rate": {**interval, "forecast_p": p,
                         "forecast_inside_interval": interval["exact_95_interval"][0] <= p <= interval["exact_95_interval"][1]},
        "q3_brier": {"p": p, "reference_p": r, "outcomes": rows,
                     "falsifying_outcomes": worse_outcomes("probability", {"p": p}, {"p": r})},
        "q4_interval": {"interval": [f["lower"], f["upper"]], "coverage": f["coverage"],
                        "penalty_per_unit_outside": fix(2 / (1 - exact(f["coverage"])), "score"),
                        "outcomes": scores, "covered": sum(row["covered"] for row in scores)},
        "q5_falsifier": {"interval_scores_worse_than_reference_for_counts": {"from": worse[0], "to": worse[-1],
                                                                             "count": len(worse)}},
    }


def known_answers(cfg: dict) -> dict:
    two = exact_interval(cfg["two_of_six"]["events"], cfg["two_of_six"]["trials"])
    check("known answer: the exact interval for 2 of 6 equals PSY-017's", two["exact_95_interval"]
          == [cfg["two_of_six"]["lower"], cfg["two_of_six"]["upper"]], f"{two}")
    one = exact_interval(cfg["one_of_two"]["events"], cfg["one_of_two"]["trials"])
    root = math.sqrt(0.975)  # correctly rounded by IEEE 754
    check("known answer: the exact interval for 1 of 2 is [1 - sqrt(0.975), sqrt(0.975)]",
          one["exact_95_interval"] == [round(1 - root, 4), round(root, 4)], f"{one}")
    return {"two_of_six": two["exact_95_interval"], "one_of_two": one["exact_95_interval"]}


def strip_private(value):
    if isinstance(value, dict):
        return {key: strip_private(item) for key, item in value.items() if not key.startswith("_")}
    if isinstance(value, list):
        return [strip_private(item) for item in value]
    return value


def analyze(obs: dict, scenarios: dict) -> dict:
    rounding = {f"{key}_decimals": value for key, value in DECIMALS.items()}
    if scenarios["rounding"] != rounding:
        raise ValueError("scenarios.json rounding does not match analyze.py")
    if obs["source"]["library"]["commit"] is None:
        raise ValueError("observed-input.json was written with --allow-drift: the lesson's numbers do not apply")
    observed = observed_section(obs)
    base = base_rate_section(obs, scenarios["base_rate_windows"])
    validation = validation_section(scenarios)
    scoring = scoring_section(scenarios, observed, base)
    return strip_private({
        "module_id": scenarios["module_id"],
        "kind": "observed counts at Demerzel commit " + obs["source"]["commit"] + " (observed, base_rate); "
                "hand-written records and INVENTED outcomes (validation, scoring, exercises, transfer_task)",
        "rounding": "probabilities and rates to 6 decimals, scores to 6 decimals, interval ends to 4 decimals, days "
                    "to 3 decimals; exact fractions until then, rounded half away from zero",
        "observed": observed,
        "base_rate": base,
        "known_answers": known_answers(scenarios["known_answers"]),
        "validation": validation,
        "scoring": scoring,
        "exercises": exercises_section(scenarios, base, scoring),
        "transfer_task": transfer_task(scenarios["transfer_task"]),
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
    except (AssertionError, KeyError, ValueError, TypeError, OSError) as exc:
        print(f"analyze.py: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 1
    text_out = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.check:
        try:
            saved = args.output.read_bytes()
        except OSError as exc:
            print(f"analyze.py: cannot read {args.output}: {exc}", file=sys.stderr)
            return 1
        same = saved.replace(b"\r\n", b"\n") == text_out.encode("utf-8")
        print(f"analyze.py: {args.output.name} {'matches' if same else 'DIFFERS FROM'} a fresh run "
              f"({len(CHECKS)} self-checks passed)")
        return 0 if same else 1
    args.output.write_bytes(text_out.encode("utf-8"))
    print(f"analyze.py: {len(CHECKS)} self-checks passed -> {args.output.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
