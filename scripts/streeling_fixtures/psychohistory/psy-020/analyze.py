#!/usr/bin/env python3
"""PSY-020 analysis: what moves a citation count, and what a rewarded proxy does.

Reads observed-input.json (written by extract.py from the pinned commit) and
scenarios.json (assumptions), never the repository, and writes results.json.
The observed sections recount the snapshot through a second code path. The
what-if cases add imaginary files to the observed counts. The effort model and
the reflexive forecast are synthetic: exact enumerations of equally likely
cases, plus one seeded sample.

Every stored number is an integer, or an exact fraction rounded half up to a
stated number of decimals, or a correlation computed with one correctly
rounded square root; no other function of the C math library is used.

No citation path is written here or in results.json: names from the snapshot
stay in their spaced form and are turned back into paths only in memory.

Run from the repository root:
    python -I -B scripts/streeling_fixtures/psychohistory/psy-020/analyze.py
    python -I -B scripts/streeling_fixtures/psychohistory/psy-020/analyze.py --check
"""

from __future__ import annotations

import argparse
import copy
import json
import math
import os
import random
import sys
from datetime import datetime
from fractions import Fraction
from itertools import combinations
from pathlib import Path

# This program lives under scripts/ (CONTRIBUTING.md: no executable code outside scripts/); its data stays
# under state/streeling/fixtures/. FIXTURE_FILE is the path the program would have next to that data.
FIXTURE_FILE = (Path(__file__).resolve().parents[4]
                / "state/streeling/fixtures/psychohistory/psy-020" / Path(__file__).name)

HERE = FIXTURE_FILE.parent
DECIMALS = {"share": 4, "percent": 2, "mean": 4, "correlation": 4}
RELATION = {1: "ahead of", 0: "tied with", -1: "behind"}
CHECKS: dict[str, int] = {}  # self-check -> times evaluated


def check(name: str, condition: bool, detail: str = "") -> None:
    """A self-check that can fail: abort instead of writing a wrong result."""
    if not condition:
        raise AssertionError(f"self-check failed: {name}" + (f" ({detail})" if detail else ""))
    CHECKS[name] = CHECKS.get(name, 0) + 1


def fixed(value: Fraction | int, kind: str) -> float:
    """Rounds an exact value half up to the decimals stated for its kind."""
    scale = 10 ** DECIMALS[kind]
    scaled = Fraction(value) * scale
    return ((2 * scaled.numerator + scaled.denominator) // (2 * scaled.denominator)) / scale


def percent(change: int | Fraction, base: int | Fraction) -> float | None:
    """A change as a percentage of its base; None when the base is 0."""
    return fixed(Fraction(100 * change, 1) / base, "percent") if base else None


def unspaced(label: str) -> str:
    """Turns a spaced data label back into the path it stands for (in memory only)."""
    return "/".join(part.strip() for part in label.split("/"))


def exclusion_test(pathspecs: list[str]):
    """Returns a function that says whether a path is excluded by pathspecs of the producer's two forms."""
    prefixes, infixes = [], []
    for spec in pathspecs:
        body = spec[2:]
        if not spec.startswith(":!") or (("*" in body) != (body.startswith("**/") and body.endswith("/**"))):
            raise ValueError(f"exclusion pathspec of an unknown form: {spec}")
        (infixes if "*" in body else prefixes).append("/" + body[3:-3] + "/" if "*" in body else body)
    return lambda path: (any(path == p or path.startswith(p + "/") for p in prefixes)
                         or any(infix in path for infix in infixes))


def owned_by(ref: str, paths: list[str]) -> bool:
    """The producer's test: the file is one of the artifact's citation paths, or lies under one."""
    return any(ref == p.rstrip("/") or ref.startswith(p.rstrip("/") + "/") for p in paths)


def classify(path: str, content: str, paths: list[str], is_excluded) -> str:
    """Says why the counting rule counts a file for an artifact, or why it does not."""
    if is_excluded(path):
        return "not counted: the file is in an excluded folder"
    if owned_by(path, paths):
        return "not counted: the file is the artifact's own"
    if not any(p in content for p in paths):
        return "not counted: no citation path appears as a literal string"
    return "counted"


def relation(x: int, y: int) -> int:
    return (x > y) - (x < y)


def order_changes(before: dict[str, int], after: dict[str, int]) -> list[str]:
    """The pairs whose order relation (ahead of, tied with, behind) differs between two sets of counts."""
    return [f"{i} {RELATION[relation(before[i], before[j])]} {j} -> {RELATION[relation(after[i], after[j])]}"
            for i, j in combinations(sorted(before), 2)
            if relation(before[i], before[j]) != relation(after[i], after[j])]


def ranking(counts: dict[str, int], names: dict[str, str]) -> list[dict]:
    """Counts from the largest down; equal counts share a rank (1, 2, 2, 4)."""
    ordered = sorted(counts, key=lambda key: (-counts[key], key))
    return [{"rank": 1 + sum(counts[other] > counts[key] for other in counts), "key": key, "name": names[key],
             "count": counts[key]} for key in ordered]


def measurable(observed: dict) -> list[dict]:
    return [artifact for artifact in observed["artifacts"] if artifact["measurable"]]


def recount_from_table(observed: dict) -> dict[str, set[str]]:
    """Second code path: for each measurable artifact, the files of the table that the rule counts."""
    path_of = {p["key"]: unspaced(p["path"]) for p in observed["citation_paths"]}
    table = {unspaced(label): keys for label, keys in observed["files_containing_a_path"].items()}
    refs = {}
    for artifact in measurable(observed):
        paths = [path_of[key] for key in artifact["path_keys"]]
        refs[artifact["key"]] = {name for name, keys in table.items()
                                 if set(keys) & set(artifact["path_keys"]) and not owned_by(name, paths)}
    return refs


def rule_section(observed: dict) -> dict:
    """Returns the 'observed_rule' section: what the producer counts, where it says so, and on how many files."""
    quotes, scan = observed["quoted_passages"], observed["scan"]
    users = {}
    for artifact in measurable(observed):
        for key in artifact["path_keys"]:
            users.setdefault(key, []).append(artifact["key"])
    check("each listed citation path belongs to one distinct path", sum(map(len, users.values()))
          == scan["citation_paths_listed"] and len(users) == scan["distinct_citation_paths"])
    check("tracked files = files excluded + files searched",
          scan["tracked_files"] == scan["files_excluded_by_the_pathspecs"] + scan["files_searched"])
    label = {p["key"]: p["path"] for p in observed["citation_paths"]}
    return {
        "producer": observed["producer_rule"]["script"],
        "definition": " ".join(quotes["producer_definition"]["text"]),
        "definition_lines": [quotes["producer_definition"]["first_line"], quotes["producer_definition"]["last_line"]],
        "search_lines": [quotes["producer_search"]["first_line"], quotes["producer_search"]["last_line"]],
        "exclusion_line": quotes["producer_exclusions"]["first_line"],
        "exclusion_pathspecs": observed["producer_rule"]["exclusion_pathspecs"],
        "feeder_line_that_copies_the_count": quotes["feeder_reads_count"]["first_line"],
        "tracked_files": scan["tracked_files"],
        "files_excluded": scan["files_excluded_by_the_pathspecs"],
        "files_searched": scan["files_searched"],
        "evolution_records": len(observed["artifacts"]),
        "measurable_artifacts": len(measurable(observed)),
        "unmeasurable_artifacts": [
            {"artifact": a["artifact"], "recorded_citation_count": a["recorded"]["citation_count"],
             "citation_source": a["recorded"]["citation_source"], "reason": a["unmeasurable_reason"]}
            for a in observed["artifacts"] if not a["measurable"]],
        "citation_paths_listed": scan["citation_paths_listed"],
        "distinct_citation_paths": scan["distinct_citation_paths"],
        "paths_shared_by_two_artifacts": [{"path": label[key], "artifacts": keys}
                                          for key, keys in sorted(users.items()) if len(keys) > 1],
    }


def counts_section(observed: dict, refs: dict[str, set[str]]) -> dict:
    """Returns the 'observed_counts' section: recorded count against recount, for each measurable artifact."""
    rows = []
    for artifact in measurable(observed):
        check("recount from the file table = recount made by extract.py",
              len(refs[artifact["key"]]) == artifact["recount"]["files"], artifact["artifact"])
        rows.append({"key": artifact["key"], "artifact": artifact["artifact"],
                     "citation_paths": artifact["citation_paths"],
                     "recorded_citation_count": artifact["recorded"]["citation_count"],
                     "recount": len(refs[artifact["key"]])})
    counts = {row["key"]: row["recount"] for row in rows}
    files = set().union(*refs.values())
    pairs = len(counts) * (len(counts) - 1) // 2
    check("pairs counted by artifact = pairs counted by file",
          sum(counts.values()) == sum(sum(name in found for found in refs.values()) for name in files))
    return {
        "artifacts": rows,
        "recounts_equal_to_the_recorded_count": sum(r["recount"] == r["recorded_citation_count"] for r in rows),
        "of_measurable_artifacts": len(rows),
        "sum_of_counts": sum(counts.values()),
        "counted_files": len(files),
        "counts_per_counted_file": fixed(Fraction(sum(counts.values()), len(files)), "mean"),
        "files_containing_a_path": len(observed["files_containing_a_path"]),
        "files_containing_only_their_own_artifacts_path": len(observed["files_containing_a_path"]) - len(files),
        "ranking": ranking(counts, {row["key"]: row["artifact"] for row in rows}),
        "pairs_of_artifacts": pairs,
        "tied_pairs": sum(counts[i] == counts[j] for i, j in combinations(sorted(counts), 2)),
    }


def tally(values) -> dict[str, int]:
    """Counts equal values; keys in descending order of count, then by name."""
    counts: dict[str, int] = {}
    for value in values:
        counts[str(value)] = counts.get(str(value), 0) + 1
    return dict(sorted(counts.items(), key=lambda item: (-item[1], item[0])))


def course_files(per_file: dict[str, list[str]], total_pairs: int) -> dict:
    """Returns the counted files that are course lessons, and how many counts are a translation of a counted lesson."""
    lessons: dict[tuple[str, str], dict[str, list[str]]] = {}
    for name, keys in per_file.items():
        parts = name.split("/")
        if parts[:3] != ["state", "streeling", "courses"]:
            continue
        check("a course file is courses/<department>/<language>/<lesson>.md", len(parts) == 6 and parts[5].endswith(".md"))
        language, stem = parts[4], parts[5][:-3]
        stem = stem[:-len(language) - 1] if stem.endswith("." + language) else stem
        lessons.setdefault((parts[3], stem), {})[language] = keys
    pairs = sum(len(keys) for versions in lessons.values() for keys in versions.values())
    english = sum(len(versions.get("en", [])) for versions in lessons.values())
    check("every counted translation has its English lesson counted for the same artifacts",
          all(keys == versions.get("en") for versions in lessons.values() for keys in versions.values()))
    return {
        "files": sum(len(versions) for versions in lessons.values()),
        "lessons": len(lessons),
        "files_by_language_folder": tally(language for versions in lessons.values() for language in versions),
        "counts_from_course_files": pairs,
        "counts_from_english_lessons": english,
        "counts_from_translations": pairs - english,
        "translations_as_percent_of_all_counts": percent(pairs - english, total_pairs),
        "artifacts_counted_in_a_course_file": sorted({key for v in lessons.values() for keys in v.values() for key in keys}),
    }


def mentions_section(observed: dict, refs: dict[str, set[str]]) -> dict:
    """Returns the 'observed_mentions' section: which files are counted, and how many artifacts each one names."""
    per_file: dict[str, list[str]] = {}
    for key in sorted(refs):
        for name in refs[key]:
            per_file.setdefault(name, []).append(key)
    by_artifacts = {str(n): sum(len(keys) == n for keys in per_file.values())
                    for n in sorted({len(keys) for keys in per_file.values()})}
    paths_in = {unspaced(label): len(keys) for label, keys in observed["files_containing_a_path"].items()}
    most = max(sorted(paths_in), key=lambda name: paths_in[name])
    total = sum(len(keys) for keys in per_file.values())
    check("files by number of artifacts sum to the counted files and to the counts",
          sum(by_artifacts.values()) == len(per_file)
          and sum(int(n) * files for n, files in by_artifacts.items()) == total)
    extensions = tally(os.path.splitext(name.rsplit("/", 1)[-1])[1] or "(no extension)" for name in per_file)
    folders = tally(name.split("/")[0] if "/" in name else "(repository root)" for name in per_file)
    check("extensions and top folders each cover every counted file",
          sum(extensions.values()) == len(per_file) == sum(folders.values()))
    two_or_more = sum(len(keys) > 1 for keys in per_file.values())
    return {
        "counted_files": len(per_file),
        "counted_files_by_number_of_artifacts": by_artifacts,
        "counted_files_naming_two_or_more_artifacts": two_or_more,
        "share_naming_two_or_more_artifacts": fixed(Fraction(two_or_more, len(per_file)), "share"),
        "files_by_number_of_distinct_paths": {str(n): sum(v == n for v in paths_in.values())
                                              for n in sorted(set(paths_in.values()))},
        "most_paths_in_one_file": paths_in[most],
        "file_with_the_most_paths": " / ".join(most.split("/")),
        "counted_files_by_extension": extensions,
        "markdown_share_of_counted_files": fixed(Fraction(extensions.get(".md", 0), len(per_file)), "share"),
        "counted_files_by_top_folder": folders,
        "course_files": course_files(per_file, total),
    }


def trend_section(observed: dict) -> dict:
    """Returns the 'observed_trend_rows' section: the rows of the log with a non-zero delta_citations."""
    trend = observed["quality_trend"]
    rows = trend["rows_with_a_non_zero_delta_citations"]
    runs = sorted({row["run"] for row in rows})
    first = [row for row in rows if row["previous_row"] != "count"]
    check("a row without an earlier count records its whole count as the change",
          all(row["delta_citations"] == row["citation_count"] for row in first))
    check("a row with an earlier count records the difference",
          all(row["delta_citations"] == row["citation_count"] - row["previous_count"]
              for row in rows if row["previous_row"] == "count"))
    return {
        "rows_in_the_log": trend["rows"], "runs": trend["runs"], "artifacts": trend["artifacts"],
        "rows_with_a_non_zero_delta_citations": len(rows),
        "of_which_the_artifact_had_no_earlier_count": len(first),
        "of_which_the_artifact_had_an_earlier_count": len(rows) - len(first),
        "by_run": [{"run": run, "rows": sum(row["run"] == run for row in rows),
                    "deltas": sorted({row["delta_citations"] for row in rows if row["run"] == run})} for run in runs],
        "list": [{"run": row["run"], "artifact": row["artifact"], "delta_citations": row["delta_citations"],
                  "earlier_count": row["previous_count"]} for row in rows],
        "cause": "none is attributed here: a count says that the number of files moved, not why",
        "latest_run": trend["latest_run"],
    }


def decision_section(observed: dict) -> dict:
    """Returns the 'observed_decision_rules' section: where the pinned repository ties the count to a decision."""
    policy, quotes = observed["policy"], observed["quoted_passages"]
    latest = datetime.strptime(observed["quality_trend"]["latest_run"]["timestamp"], "%Y-%m-%dT%H:%M:%SZ")
    zero = [a for a in measurable(observed) if a["recount"]["files"] == 0]
    cycles = policy["history_cycles"]
    for cycle in cycles:
        check("the recorded ratio is LOLLI / ERGOL to two decimals",
              fixed(Fraction(cycle["lolli_count"], cycle["ergol_count"]), "percent") == cycle["ratio"])
    names = ("policy_citations", "policy_ergol", "policy_lolli", "policy_ratio", "policy_freeze_trigger",
             "policy_zero_rule", "policy_citation_source", "policy_zero_scan")
    return {
        "policy": policy["file"],
        "quoted_lines": {name[len("policy_"):]: {"lines": [quotes[name]["first_line"], quotes[name]["last_line"]],
                                                "text": quotes[name]["text"]} for name in names},
        "ratio_bands": policy["ratio_bands"],
        "zero_citation_window_days": policy["zero_citation_window_days"],
        "history_file": policy["history_file"],
        "history_cycles_recorded": len(cycles),
        "history_cycles": cycles,
        "measurable_artifacts_with_a_count_of_zero": [
            {"key": a["key"], "artifact": a["artifact"], "created_at": a["created_at"],
             "days_from_creation_to_the_latest_run":
                 (latest - datetime.strptime(a["created_at"], "%Y-%m-%dT%H:%M:%SZ")).days,
             "deprecation_candidate_in_its_record": a["recorded"]["deprecation_candidate"]} for a in zero],
        "correction_note": observed["correction_note"],
    }


def toy_section(cfg: dict, pathspecs: list[str]) -> dict:
    """Returns the 'toy_rule' section: the counting rule applied to an invented tree."""
    is_excluded = exclusion_test(pathspecs)
    verdicts = [{"key": f["key"], "path": f["path"], "what": f["what"],
                 "verdict": classify(f["path"], f["content"], cfg["citation_paths"], is_excluded)} for f in cfg["files"]]
    counted = [v["key"] for v in verdicts if v["verdict"] == "counted"]
    check("toy tree, counted by hand: files a, g and h", counted == ["a", "g", "h"])
    user = cfg["the_only_file_that_uses_the_rule"]
    return {
        "kind": "synthetic: an invented tree, counted with the producer's rule",
        "citation_paths": cfg["citation_paths"],
        "files": verdicts,
        "count": len(counted),
        "counted_files": counted,
        "the_only_file_that_uses_the_rule": user,
        "is_that_file_counted": user in counted,
    }


def add_files(counts: dict[str, int], artifacts: list[dict], path_keys: str, files: int = 1) -> dict[str, int]:
    """Counts after adding tracked, non-excluded files that each contain the given citation paths."""
    return {a["key"]: counts[a["key"]] + files * bool(set(a["path_keys"]) & set(path_keys)) for a in artifacts}


def every_path_case(counts: dict[str, int], artifacts: list[dict], all_keys: str, files: int) -> dict:
    """Returns the effect of `files` added files that each list every distinct citation path."""
    after = add_files(counts, artifacts, all_keys, files)
    before_sum, after_sum = sum(counts.values()), sum(after.values())
    check("a file listing every path raises the sum by one per measurable artifact",
          after_sum - before_sum == files * len(artifacts))
    check("adding the same number to every count changes no order relation", not order_changes(counts, after))
    top = max(sorted(counts), key=lambda key: counts[key])
    low = min((key for key in sorted(counts) if counts[key] > 0), key=lambda key: counts[key])
    return {
        "files_added": files,
        "distinct_paths_in_each_file": len(all_keys),
        "counts_raised": sum(after[key] > counts[key] for key in counts),
        "raise_per_count": files,
        "sum_before": before_sum, "sum_after": after_sum,
        "sum_change_percent": percent(after_sum - before_sum, before_sum),
        "mean_count_before": fixed(Fraction(before_sum, len(artifacts)), "mean"),
        "mean_count_after": fixed(Fraction(after_sum, len(artifacts)), "mean"),
        "order_relations_changed": len(order_changes(counts, after)),
        "largest_count": {"key": top, "before": counts[top], "after": after[top],
                          "change_percent": percent(after[top] - counts[top], counts[top])},
        "smallest_non_zero_count": {"key": low, "before": counts[low], "after": after[low],
                                    "change_percent": percent(after[low] - counts[low], counts[low])},
        "counts_of_zero_before": sum(value == 0 for value in counts.values()),
        "counts_of_zero_after": sum(value == 0 for value in after.values()),
        "counts_after": after,
    }


def one_path_cases(counts: dict[str, int], artifacts: list[dict], paths: list[dict]) -> dict:
    """Returns the effect of one added file that names a single citation path, for each distinct path in turn."""
    rows = []
    for path in paths:
        after = add_files(counts, artifacts, path["key"])
        changes = order_changes(counts, after)
        rows.append({"path_key": path["key"], "path": path["path"],
                     "counts_raised": [key for key in sorted(counts) if after[key] > counts[key]],
                     "order_relations_changed": len(changes), "changes": changes})
    check("single-path files raise as many counts in all as there are listed citation paths",
          sum(len(row["counts_raised"]) for row in rows) == sum(len(a["path_keys"]) for a in artifacts))
    return {
        "distinct_paths": len(rows),
        "paths_that_raise_one_count": sum(len(row["counts_raised"]) == 1 for row in rows),
        "paths_that_raise_two_counts": sum(len(row["counts_raised"]) == 2 for row in rows),
        "paths_that_change_an_order_relation": sum(row["order_relations_changed"] > 0 for row in rows),
        "by_path": rows,
    }


def files_needed(counts: dict[str, int]) -> dict:
    """Returns how many single-path files an artifact needs to pass the next count above its own."""
    rows = []
    for key in sorted(counts, key=lambda k: (-counts[k], k)):
        higher = [value for value in counts.values() if value > counts[key]]
        rows.append({"key": key, "count": counts[key], "next_count_above": min(higher) if higher else None,
                     "files_to_pass_it": min(higher) - counts[key] + 1 if higher else None})
    needed = [row["files_to_pass_it"] for row in rows if row["files_to_pass_it"] is not None]
    return {
        "by_artifact": rows,
        "fewest_files_that_reverse_a_strict_order": min(needed),
        "artifacts_for_which_that_many_files_suffice": [r["key"] for r in rows if r["files_to_pass_it"] == min(needed)],
        "files_for_the_lowest_count_to_pass_the_highest": max(counts.values()) - min(counts.values()) + 1,
    }


def ratio_band(ratio: Fraction, bands: dict) -> str:
    if ratio > Fraction(str(bands["freeze_from"])):
        return "above the freeze ratio"
    if ratio > Fraction(str(bands["warning_from"])):
        return "warning"
    return "watch" if ratio > Fraction(str(bands["watch_from"])) else "healthy"


def policy_cycles(cases: list[dict], raised_per_catalogue: int, bands: dict) -> list[dict]:
    """Returns the policy's ratio for each imaginary cycle, under the reading stated in scenarios.json."""
    rows = []
    for case in cases:
        catalogues = case["catalogue_files_listing_every_path"]
        lolli, citations = case["new_artifacts"] + catalogues, catalogues * raised_per_catalogue
        ratio = Fraction(lolli, max(citations, 1))
        rows.append({"key": case["key"], "files_created": lolli, "summed_change_of_citation_count": citations,
                     "ratio": fixed(ratio, "share"), "ratio_as_a_fraction": f"{lolli}/{max(citations, 1)}",
                     "band": ratio_band(ratio, bands)})
    return rows


def what_if_section(observed: dict, counts: dict[str, int], cfg: dict) -> dict:
    """Returns the 'what_if' section: imaginary files added to the observed counts."""
    artifacts, paths = measurable(observed), observed["citation_paths"]
    all_keys = "".join(p["key"] for p in paths)
    by_files = {str(n): every_path_case(counts, artifacts, all_keys, n) for n in cfg["files_listing_every_path"]}
    planted = observed["scan"]["controls"]["file_listing_every_path"]
    check("the one-file case equals the planted file counted by extract.py on the pinned tree",
          (by_files["1"]["counts_raised"], by_files["1"]["sum_after"] - by_files["1"]["sum_before"])
          == (planted["counts_raised"], planted["sum_of_raises"]) and planted["largest_raise"] == 1)
    several = cfg["one_path_in_several_files"]
    key = next(p["key"] for p in paths if p["path"] == several["path"])
    after = add_files(counts, artifacts, key, several["files"])
    changes = order_changes(counts, after)
    raised = [k for k in sorted(counts) if after[k] > counts[k]]
    return {
        "kind": "synthetic additions to observed counts: none of these files exists",
        "files_listing_every_path": by_files,
        "one_file_naming_one_path": one_path_cases(counts, artifacts, paths),
        "one_path_in_several_files": {
            "path": several["path"], "files_added": several["files"], "why": several["why"],
            "counts_raised": raised, "before": [counts[k] for k in raised], "after": [after[k] for k in raised],
            "sum_after": sum(after.values()), "order_relations_changed": len(changes), "changes": changes},
        "single_path_files_needed": files_needed(counts),
        "policy_reading": cfg["policy_reading"],
        "policy_cycles": policy_cycles(cfg["policy_cycles"], by_files["1"]["counts_raised"],
                                       observed["policy"]["ratio_bands"]),
    }


def top_share(values: list[int], top: int) -> Fraction:
    """The share of the summed counts held by the `top` largest counts."""
    return Fraction(sum(sorted(values, reverse=True)[:top]), sum(values))


def files_to_cross(recorded: dict[str, int], movable: list[str], top: int, limit: Fraction, cap: int) -> int:
    """Fewest added files, each naming the paths of the movable artifacts, after which the top share exceeds limit."""
    for files in range(cap + 1):
        if top_share([v + files * (k in movable) for k, v in recorded.items()], top) > limit:
            return files
    raise ValueError(f"no number of files up to {cap} brings the share above {limit}")


def power_law_reading(recorded: dict[str, int], movable_names: set[str], top: int, limit: Fraction,
                      cap: int, paths: dict[str, int]) -> dict:
    """One reading of 'the top 20% of artifacts': its share at the pin and the synthetic files that flip it."""
    leaders = sorted(recorded, key=lambda k: (-recorded[k], k))[:top]
    movable = [k for k in leaders if k in movable_names]
    total, held = sum(recorded.values()), sum(recorded[k] for k in leaders)
    files = files_to_cross(recorded, movable, top, limit, cap)
    closed = math.floor((limit * total - held) / ((1 - limit) * len(movable))) + 1
    check("the fewest files that flip the verdict equal the closed form", files == max(closed, 0))
    shifted = {k: v + files * (k in movable) for k, v in recorded.items()}
    fewer = {k: v + (files - 1) * (k in movable) for k, v in recorded.items()}
    catalogue = [v + (k in movable_names) for k, v in recorded.items()]
    return {
        "top_artifacts": top, "leaders": leaders, "their_counts": [recorded[k] for k in leaders],
        "sum_of_their_counts": held, "share": fixed(Fraction(held, total), "share"),
        "share_percent": percent(held, total), "above_the_rule": Fraction(held, total) > limit,
        "measurable_leaders": len(movable), "paths_named_by_each_added_file": sum(paths[k] for k in movable),
        "files_naming_those_paths_to_pass_the_rule": files,
        "share_after_those_files": fixed(top_share(list(shifted.values()), top), "share"),
        "share_with_one_file_fewer": fixed(top_share(list(fewer.values()), top), "share"),
        "share_after_one_catalogue_of_every_path": fixed(top_share(catalogue, top), "share"),
    }


def power_law_section(observed: dict, cfg: dict) -> dict:
    """Returns the 'power_law_rule' section: the project's 'healthy' concentration rule applied to the counts."""
    rule, quotes = observed["power_law_rule"], observed["quoted_passages"]
    recorded = {a["artifact"]: a["recorded"]["citation_count"] for a in observed["artifacts"]}
    check("the rule's population sums to the latest run of the quality trend",
          sum(recorded.values()) == observed["quality_trend"]["latest_run"]["sum_of_citation_counts"])
    exact = Fraction(len(recorded) * rule["top_percent"], 100)
    limit = Fraction(rule["share_above_percent"], 100)
    movable = {a["artifact"] for a in measurable(observed)}
    paths = {a["artifact"]: len(a["citation_paths"]) for a in observed["artifacts"]}
    tops = {"floor": math.floor(exact), "ceil": math.ceil(exact)}
    lines = {name: [quotes[name]["first_line"], quotes[name]["last_line"]] for name in (
        "power_law_detection_rule", "power_law_data", "power_law_integration", "metrics_policy_rule",
        "metrics_policy_source", "metrics_policy_share")}
    return {
        "kind": "observed rule, shares computed from the recorded counts, synthetic added files",
        "rule": rule,
        "quoted_lines": lines,
        "artifacts": len(recorded), "sum_of_counts": sum(recorded.values()),
        "top_percent_of_artifacts": f"{exact.numerator}/{exact.denominator}" if exact.denominator > 1 else str(exact),
        "reading_note": cfg["note"],
        "readings": {name: power_law_reading(recorded, movable, tops[name], limit, cfg["files_cap"], paths)
                     for name in cfg["readings"]},
    }


def correlation(pairs: list[tuple[int, int]]) -> float | None:
    """Pearson correlation of integer pairs, from exact sums and one square root; None when one side is constant."""
    n = len(pairs)
    sx, sy = sum(x for x, _ in pairs), sum(y for _, y in pairs)
    cov = n * sum(x * y for x, y in pairs) - sx * sy
    vx, vy = n * sum(x * x for x, _ in pairs) - sx * sx, n * sum(y * y for _, y in pairs) - sy * sy
    if vx == 0 or vy == 0:
        return None
    value = cov / math.sqrt(vx * vy)
    check("a correlation lies between -1 and 1", -1.0 <= value <= 1.0)
    return round(value, DECIMALS["correlation"]) + 0.0


def agent_outcome(work: int, inflation: int, error: int, weight: Fraction) -> tuple[int, int, bool]:
    """(proxy, value, inflates) for one agent: it inflates when weight x inflation yield > work yield."""
    inflates = weight * inflation > work
    return (inflation if inflates else work) + error, 0 if inflates else work, inflates


def effort_summary(agents: list[tuple[int, int, int]], weight: Fraction, high: int) -> dict:
    """Returns levels and correlation of proxy and value for a list of (work yield, inflation yield, error)."""
    outcomes = [agent_outcome(a, g, e, weight) for a, g, e in agents]
    n, inflating = len(outcomes), sum(o[2] for o in outcomes)
    proxy, value = sum(o[0] for o in outcomes), sum(o[1] for o in outcomes)
    gained = sum(g for (a, g, e), o in zip(agents, outcomes) if o[2])
    check("sum of proxies = sum of values + sum of inflation + sum of errors",
          proxy == value + gained + sum(e for _, _, e in agents))
    top = [o for o in outcomes if o[0] >= high]
    return {
        "reward_weight_on_the_proxy": str(weight),
        "cases": n,
        "cases_that_inflate": inflating,
        "share_of_effort_on_inflation": fixed(Fraction(inflating, n), "share"),
        "mean_proxy": fixed(Fraction(proxy, n), "mean"),
        "mean_value": fixed(Fraction(value, n), "mean"),
        "correlation_of_proxy_and_value": correlation([(o[0], o[1]) for o in outcomes]),
        "cases_with_a_high_proxy": len(top),
        "of_which_value_is_zero": sum(o[1] == 0 for o in top),
        "lowest_value_among_them": min((o[1] for o in top), default=None),
    }


def effort_means(agents: list[tuple[int, int, int]], weight: Fraction) -> tuple[Fraction, Fraction]:
    """Exact mean proxy and mean value, before rounding."""
    outcomes = [agent_outcome(a, g, e, weight) for a, g, e in agents]
    return Fraction(sum(o[0] for o in outcomes), len(outcomes)), Fraction(sum(o[1] for o in outcomes), len(outcomes))


def effort_grid(cfg: dict) -> list[tuple[int, int, int]]:
    """Every equally likely combination of work yield, inflation yield and proxy error."""
    return [(a, g, e) for a in cfg["work_yields"] for g in cfg["inflation_yields"] for e in cfg["proxy_errors"]]


def effort_sample(cfg: dict) -> list[tuple[int, int, int]]:
    """Seeded agents: three uniform draws each, mapped to a level by floor(u x number of levels)."""
    rng = random.Random(cfg["sample"]["seed"])
    def pick(levels: list[int]) -> int:
        return levels[min(len(levels) - 1, int(rng.random() * len(levels)))]
    return [(pick(cfg["work_yields"]), pick(cfg["inflation_yields"]), pick(cfg["proxy_errors"]))
            for _ in range(cfg["sample"]["agents"])]


def closed_form_check(cfg: dict, summary: dict) -> None:
    """With yields 1..n and all reward on the proxy: n(n-1)/2 kinds inflate, mean value (n+1)(2n+1)/6n, mean proxy (n+1)(4n-1)/6n."""
    n = len(cfg["work_yields"])
    if cfg["work_yields"] != list(range(1, n + 1)) or cfg["inflation_yields"] != cfg["work_yields"] \
            or sum(cfg["proxy_errors"]) != 0:
        return
    errors = len(cfg["proxy_errors"])
    check("all reward on the proxy: the enumeration equals the closed forms for yields 1..n",
          summary["cases_that_inflate"] == errors * n * (n - 1) // 2
          and summary["mean_value"] == fixed(Fraction((n + 1) * (2 * n + 1), 6 * n), "mean")
          and summary["mean_proxy"] == fixed(Fraction((n + 1) * (4 * n - 1), 6 * n), "mean"))


def effort_section(cfg: dict) -> dict:
    """Returns the 'effort_model' section: exact enumeration for each reward weight, then one seeded sample."""
    weights = [Fraction(num, den) for num, den in cfg["reward_weights_on_the_proxy"]]
    grid, sample = effort_grid(cfg), effort_sample(cfg)
    exact = [effort_summary(grid, weight, cfg["high_proxy_from"]) for weight in weights]
    for weight, summary in zip(weights, exact):
        check("no reward on the proxy: nobody inflates", weight != 0 or summary["cases_that_inflate"] == 0)
        if weight == 1:
            closed_form_check(cfg, summary)
    (proxy_0, value_0), (proxy_1, value_1) = effort_means(grid, weights[0]), effort_means(grid, weights[-1])
    worked = cfg.get("worked_agent")
    out = {
        "kind": "synthetic: assumed agents, nothing measured in the repository",
        "rule": "reward = (1 - w) x value + w x proxy; an agent inflates when w x inflation yield > work yield",
        "kinds_of_agent": len(cfg["work_yields"]) * len(cfg["inflation_yields"]),
        "proxy_errors": cfg["proxy_errors"],
        "high_proxy_from": cfg["high_proxy_from"],
        "exact": exact,
        "from_the_first_weight_to_the_last": {
            "weights": [str(weights[0]), str(weights[-1])],
            "mean_proxy_change": fixed(proxy_1 - proxy_0, "mean"),
            "mean_proxy_change_percent": percent(proxy_1 - proxy_0, proxy_0),
            "mean_value_change": fixed(value_1 - value_0, "mean"),
            "mean_value_change_percent": percent(value_1 - value_0, value_0)},
        "sample": {"seed": cfg["sample"]["seed"], "agents": cfg["sample"]["agents"],
                   "by_weight": [effort_summary(sample, weight, cfg["high_proxy_from"]) for weight in weights]},
    }
    if worked:
        out["worked_agent"] = [
            dict(zip(("proxy_without_error", "value", "inflates"),
                     agent_outcome(worked["work_yield"], worked["inflation_yield"], 0, weight)),
                 reward_weight_on_the_proxy=str(weight), work_yield=worked["work_yield"],
                 inflation_yield=worked["inflation_yield"]) for weight in weights]
    return out


def forecast_case(baseline: int, case: dict, rounds: int) -> dict:
    """Returns one published forecast: outcome = baseline + self_mentions + reaction x (forecast - baseline)."""
    mentions, reaction = case["self_mentions"], Fraction(*case["reaction"])
    forecast, rows = Fraction(baseline), []
    for number in range(1, rounds + 1):
        outcome = baseline + mentions + reaction * (forecast - baseline)
        check("round t of a revised forecast misses by self_mentions x reaction^(t-1)",
              outcome - forecast == mentions * reaction ** (number - 1))
        rows.append({"round": number, "forecast": fixed(forecast, "mean"), "outcome": fixed(outcome, "mean"),
                     "error": fixed(outcome - forecast, "mean")})
        forecast = outcome
    consistent = None if reaction == 1 else baseline + Fraction(mentions) / (1 - reaction)
    if consistent is not None:
        check("the self-consistent forecast is its own outcome",
              baseline + mentions + reaction * (consistent - baseline) == consistent)
    return {
        "key": case["key"], "self_mentions": mentions, "reaction": str(reaction),
        "outcome_of_forecasting_the_baseline": rows[0]["outcome"], "its_error": rows[0]["error"],
        "self_consistent_forecast": None if consistent is None else fixed(consistent, "mean"),
        "self_consistent_forecast_as_a_fraction": None if consistent is None else str(consistent),
        "forecast_revised_to_the_last_outcome": rows,
    }


def forecast_section(cfg: dict, counts: dict[str, int], names: dict[str, str]) -> dict:
    """Returns the 'reflexive_forecast' section, starting from one observed count."""
    key = next(k for k, name in names.items() if name == cfg["baseline_artifact"])
    return {
        "kind": "synthetic: assumed reactions to a published forecast, starting from one observed count",
        "formula": "outcome = baseline + self_mentions + reaction x (forecast - baseline)",
        "baseline": {"artifact": cfg["baseline_artifact"], "key": key, "count": counts[key]},
        "cases": [forecast_case(counts[key], case, cfg["rounds"]) for case in cfg["cases"]],
    }


def hypothesis_section(what_if: dict, effort: dict, cfg: dict) -> dict:
    """Returns the three parts of the hypothesis recorded before these cases were run, each with its verdict."""
    one, single = what_if["files_listing_every_path"]["1"], what_if["one_file_naming_one_path"]
    first, last = effort["exact"][0], effort["exact"][-1]
    limit = cfg["correlation_below_when_the_reward_is_all_proxy"]
    parts = {
        "one_file_listing_every_path_raises_each_count_by_1_and_changes_no_order":
            one["counts_raised"] == len(one["counts_after"]) and one["raise_per_count"] == 1
            and one["order_relations_changed"] == 0,
        "a_single_path_file_changes_an_order_relation_for_some_paths":
            0 < single["paths_that_change_an_order_relation"],
        "rewarding_the_proxy_raises_it_lowers_value_and_brings_their_correlation_below_the_threshold":
            last["mean_proxy"] > first["mean_proxy"] and last["mean_value"] < first["mean_value"]
            and last["correlation_of_proxy_and_value"] < limit,
    }
    return {"correlation_threshold": limit, "parts": parts, "all_parts_hold": all(parts.values())}


def controls_section(observed: dict, counts: dict[str, int], scenarios: dict) -> dict:
    """Returns the 'negative_controls' section: planted changes that the checks must notice."""
    cfg, toy = scenarios["negative_controls"], scenarios["toy_rule"]
    names = {a["key"]: a["artifact"] for a in measurable(observed)}
    key_of = {name: key for key, name in names.items()}
    damaged = copy.deepcopy(observed)
    target = next(a for a in measurable(damaged) if a["artifact"] == cfg["drop_one_file_of_artifact"])
    victim = sorted(label for label, keys in damaged["files_containing_a_path"].items()
                    if set(keys) & set(target["path_keys"]))[0]
    del damaged["files_containing_a_path"][victim]
    recount = len(recount_from_table(damaged)[target["key"]])
    first, second = (key_of[name] for name in cfg["swap_counts_of"])
    swapped = dict(counts, **{first: counts[second], second: counts[first]})
    planted = copy.deepcopy(toy)
    control = planted["negative_control"]
    for item in planted["files"]:
        if item["key"] == control["file"]:
            item["content"] = item["content"].replace(control["replace"], control["with"])
    toy_after = toy_section_count(planted, observed["producer_rule"]["exclusion_pathspecs"])
    scan = observed["scan"]["controls"]
    check("the planted changes are noticed", recount == target["recount"]["files"] - 1
          and order_changes(counts, swapped) and toy_after == 2)
    return {
        "one_file_removed_from_the_table": {"artifact": target["artifact"], "recount_before": target["recount"]["files"],
                                            "recount_after": recount, "noticed": recount != target["recount"]["files"]},
        "two_counts_swapped": {"artifacts": cfg["swap_counts_of"],
                               "order_relations_changed": len(order_changes(counts, swapped))},
        "no_file_added": {"order_relations_changed": len(order_changes(counts, dict(counts)))},
        "toy_tree_with_one_mention_spaced": {"file": control["file"], "count_before": 3, "count_after": toy_after},
        "planted_by_extract_on_the_pinned_tree": {
            "file_listing_every_path_in_an_excluded_folder": scan["same_file_in_an_excluded_folder"]["counts_raised"],
            "file_listing_every_path_under_an_archived_folder": scan["same_file_under_an_archived_folder"]["counts_raised"],
            "file_listing_every_spaced_label": scan["file_listing_every_spaced_label"]["counts_raised"],
            "pinned_files_containing_a_spaced_label": scan["pinned_files_containing_a_spaced_label"]},
    }


def toy_section_count(cfg: dict, pathspecs: list[str]) -> int:
    is_excluded = exclusion_test(pathspecs)
    return sum(classify(f["path"], f["content"], cfg["citation_paths"], is_excluded) == "counted" for f in cfg["files"])


def transfer_links(task: dict) -> dict:
    """Returns the transfer task's counting answers: the four pages, the index page, the two single links."""
    is_excluded = exclusion_test(task["exclusion_pathspecs"])
    books = task["handbooks"]
    asked = next(b for b in books if b["key"] == task["question_about_handbook"])
    verdicts = [{"key": p["key"], "path": p["path"],
                 "verdict": classify(p["path"], p["content"], [asked["address"]], is_excluded)} for p in task["pages"]]
    counts = {b["key"]: b["links"] for b in books}
    pages = task["index_pages_listing_every_address"]
    indexed = {key: value + pages for key, value in counts.items()}
    top = max(sorted(counts), key=lambda key: counts[key])
    low = min((key for key in sorted(counts) if counts[key] > 0), key=lambda key: counts[key])
    single = task["pages_linking_one_handbook"]
    linked = dict(counts, **{single["handbook"]: counts[single["handbook"]] + single["pages"]})
    return {
        "question_1": {"handbook": asked["key"], "pages": verdicts,
                       "pages_counted": [v["key"] for v in verdicts if v["verdict"] == "counted"],
                       "the_only_page_that_uses_the_handbook": task["the_only_page_that_uses_the_handbook"]},
        "question_2": {
            "sum_before": sum(counts.values()), "sum_after_one_index_page": sum(indexed.values()),
            "sum_change_percent": percent(sum(indexed.values()) - sum(counts.values()), sum(counts.values())),
            "counts_after_one_index_page": indexed,
            "largest_count_change_percent": percent(pages, counts[top]),
            "smallest_non_zero_count_change_percent": percent(pages, counts[low]),
            "order_relations_changed_by_the_index_page": len(order_changes(counts, indexed)),
            "pairs_of_handbooks": len(counts) * (len(counts) - 1) // 2,
            "counts_after_pages_linking_one_handbook": linked,
            "order_relations_changed_by_those_pages": order_changes(counts, linked),
            "handbooks_with_0_links_before": [k for k in counts if counts[k] == 0],
            "handbooks_with_0_links_after_one_index_page": [k for k in indexed if indexed[k] == 0]},
    }


def transfer_section(task: dict) -> dict:
    """Returns the 'transfer_task' section: the expected answers of the learner task, from its own inputs."""
    links = transfer_links(task)
    rule = task["ratio_rule"]
    with_index = Fraction(rule["new_pages"] + task["index_pages_listing_every_address"],
                          max(rule["new_links_without_the_index_page"]
                              + task["index_pages_listing_every_address"] * len(task["handbooks"]), 1))
    without = Fraction(rule["new_pages"], max(rule["new_links_without_the_index_page"], 1))
    links["question_2"]["ratio_without_the_index_page"] = fixed(without, "share")
    links["question_2"]["ratio_with_the_index_page"] = fixed(with_index, "share")
    links["question_2"]["frozen_without_the_index_page"] = without > rule["freeze_above"]
    links["question_2"]["frozen_with_the_index_page"] = with_index > rule["freeze_above"]
    model = task["effort_model"]
    weights = [Fraction(num, den) for num, den in model["reward_weights_on_the_proxy"]]
    summaries = [effort_summary(effort_grid(model), weight, model["high_proxy_from"]) for weight in weights]
    closed_form_check(model, summaries[-1])
    base = next(b["links"] for b in task["handbooks"] if b["key"] == task["forecast"]["handbook"])
    return {
        "kind": "synthetic: a hypothetical wiki defined in scenarios.json, not Streeling data",
        **links,
        "question_3": {"kinds_of_agent": len(model["work_yields"]) * len(model["inflation_yields"]),
                       "high_proxy_from": model["high_proxy_from"], "by_weight": summaries},
        "question_4": {"baseline": base, **forecast_case(base, dict(task["forecast"], key="east_forecast"),
                                                        task["forecast"]["rounds"])},
        "question_5": "no single answer: see the review brief",
    }


def analyze(observed: dict, scenarios: dict) -> dict:
    rounding = {f"{kind}_decimals": places for kind, places in DECIMALS.items()}
    if scenarios["rounding"] != rounding:
        raise ValueError("scenarios.json rounding does not match analyze.py")
    refs = recount_from_table(observed)
    counts = {key: len(found) for key, found in refs.items()}
    names = {a["key"]: a["artifact"] for a in measurable(observed)}
    rule = rule_section(observed)
    counted = counts_section(observed, refs)
    mentions = mentions_section(observed, refs)
    trend = trend_section(observed)
    decisions = decision_section(observed)
    toy = toy_section(scenarios["toy_rule"], observed["producer_rule"]["exclusion_pathspecs"])
    what_if = what_if_section(observed, counts, scenarios["what_if"])
    power_law = power_law_section(observed, scenarios["power_law_rule"])
    effort = effort_section(scenarios["effort_model"])
    forecast = forecast_section(scenarios["reflexive_forecast"], counts, names)
    hypothesis = hypothesis_section(what_if, effort, scenarios["hypothesis"])
    controls = controls_section(observed, counts, scenarios)
    transfer = transfer_section(scenarios["transfer_task"])
    return {
        "schema_version": "0.1.0",
        "module_id": scenarios["module_id"],
        "observed_input": {"commit": observed["source"]["commit"],
                           "manifest_sha256": observed["source"]["manifest"]["sha256"]},
        "label_convention": "artifact names, citation paths and file paths taken from the snapshot keep a space on "
                            "each side of every slash, so that this file is not counted by the rule it studies",
        "rounding": "shares, means and correlations to 4 decimals, percentages to 2; exact fractions are rounded half up",
        "observed_rule": rule,
        "observed_counts": counted,
        "observed_mentions": mentions,
        "observed_trend_rows": trend,
        "observed_decision_rules": decisions,
        "toy_rule": toy,
        "what_if": what_if,
        "power_law_rule": power_law,
        "effort_model": effort,
        "reflexive_forecast": forecast,
        "hypothesis_parts": hypothesis,
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
        observed = json.loads(args.input.read_text(encoding="utf-8"))
        result = analyze(observed, json.loads(args.scenarios.read_text(encoding="utf-8")))
        text = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
        literal = [p["key"] for p in observed["citation_paths"] if unspaced(p["path"]) in text]
        if literal:
            raise ValueError(f"results would contain citation paths literally (keys {literal})")
    except (AssertionError, ArithmeticError, KeyError, StopIteration, ValueError, OSError) as exc:
        print(f"analyze.py: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 1
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
