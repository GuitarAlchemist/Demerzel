#!/usr/bin/env python3
"""PSY-024 analysis: how many actors the recorded activity names, and how concentrated it is.

Reads only observed-input.json (written by extract.py, identities already replaced by labels) and scenarios.json
(assumptions and imaginary ensembles), never the repository, and writes results.json. Shares and indices are exact
fractions, rounded only when written; the simulation uses random.Random(seed).random(), +, * and one division.

Run from the repository root:
    python -I -B scripts/streeling_fixtures/psychohistory/psy-024/analyze.py
    python -I -B scripts/streeling_fixtures/psychohistory/psy-024/analyze.py --check
"""

from __future__ import annotations

import argparse
import copy
import json
import math
import random
import sys
from fractions import Fraction
from pathlib import Path

# This program lives under scripts/ (CONTRIBUTING.md: no executable code outside scripts/); its data stays
# under state/streeling/fixtures/. FIXTURE_FILE is the path the program would have next to that data.
FIXTURE_FILE = (Path(__file__).resolve().parents[4]
                / "state/streeling/fixtures/psychohistory/psy-024" / Path(__file__).name)

HERE = FIXTURE_FILE.parent
DECIMALS = {"share": 6, "index": 6, "effective_number": 4, "percent": 2, "spread": 4, "simulated_ratio": 4,
            "simulated_number": 2}
HALF = Fraction(1, 2)
CHECKS: dict[str, int] = {}  # self-check -> times evaluated


def check(name: str, condition: bool, detail: str = "") -> None:
    """A self-check that can fail: abort instead of writing a wrong result."""
    if not condition:
        raise AssertionError(f"self-check failed: {name}" + (f" ({detail})" if detail else ""))
    CHECKS[name] = CHECKS.get(name, 0) + 1


def rnd(value, kind: str) -> float:
    """Round an exact fraction (or a float) half to even at the stated decimals."""
    if isinstance(value, Fraction):
        return float(round(value, DECIMALS[kind]))
    return round(value, DECIMALS[kind]) + 0.0


def measures(counts: list[int]) -> dict:
    """Shares, concentration index, effective number and half-coverage count of a list of event counts."""
    ordered = sorted(counts, reverse=True)
    total = sum(ordered)
    check("measures: every actor has at least one event", bool(ordered) and ordered[-1] > 0)
    shares = [Fraction(count, total) for count in ordered]
    check("measures: the shares sum to 1", sum(shares) == 1)
    index = sum(share * share for share in shares)
    check("measures: 1/k <= H <= 1 for k actors", Fraction(1, len(shares)) <= index <= 1)
    running, cover = Fraction(0), 0
    for share in shares:
        running += share
        cover += 1
        if running > HALF:
            break
    return {"actors": len(ordered), "events": total, "largest_count": ordered[0],
            "largest_share_percent": rnd(shares[0] * 100, "percent"),
            "sum_of_squared_counts": sum(count * count for count in ordered), "squared_total": total * total,
            "concentration_index": rnd(index, "index"), "effective_number": rnd(1 / index, "effective_number"),
            "relative_spread": rnd(math.sqrt(index), "spread"), "half_coverage_count": cover,
            "_index": index, "_number": 1 / index}


def observed_senders(obs: dict) -> dict:
    log, own = obs["trigger_log"], obs["ownership"]
    archived, outside = log["archived"], log["outside_the_archive"]
    for part in ("by_type", "by_sender", "by_repo", "by_type_and_event_name"):
        check("accounting: every tally of the archived events sums to the number of events",
              sum(archived[part].values()) == archived["events"])
    check("accounting: the events outside the archive have one sender and one repo each",
          sum(outside["by_sender"].values()) == sum(outside["by_repo"].values())
          == outside["events_written_by_the_trigger_workflow"])
    readable: dict[str, int] = {}
    for tally in (archived["by_sender"], outside["by_sender"]):
        for label, count in tally.items():
            readable[label] = readable.get(label, 0) + count
    repos = sorted(set(archived["by_repo"]) | set(outside["by_repo"]))
    keys = archived["keys"] + ["details." + key for key in archived["details_keys"]]
    wanted = ("persona", "agent", "session", "model", "role")
    without = [row for row in outside["files"] if row["file"].endswith(".json") and "sender" not in row]
    return {
        "kind": "observed: counts of labels in observed-input.json",
        "archived": {"events": archived["events"], "first_day": archived["first_day"], "last_day": archived["last_day"],
                     "by_sender": archived["by_sender"], "by_repo": archived["by_repo"], "by_type": archived["by_type"],
                     "senders": measures(list(archived["by_sender"].values()))},
        "with_a_readable_sender": {"archived": archived["events"],
                                   "outside_the_archive": outside["events_written_by_the_trigger_workflow"],
                                   "total": sum(readable.values()), "by_sender": readable, "repos": repos,
                                   "senders": measures(list(readable.values()))},
        "trigger_files_at_the_pin_without_a_sender": [{"file": row["file"], "kind": row["kind"]} for row in without],
        "what_the_fields_record": {
            "event_keys": keys,
            "keys_naming_a_persona_agent_session_model_or_role": [k for k in keys if any(w in k for w in wanted)],
            "sender_is": log["producer"]["sender_expression"], "repo_is": log["producer"]["repo_expression"],
            "event_names_the_workflow_handles": log["producer"]["event_names_handled"],
            "event_names_seen_in_the_archive": sorted({k.split(" <- ")[1] for k in archived["by_type_and_event_name"]}),
            "agent_roles_defined_in_the_agent_team_file": log["agent_roles_defined_in_the_agent_team_file"]["role_rows"]},
        "ownership_file": {"rule_lines": own["rule_lines"], "distinct_owners": own["distinct_owners"],
                           "the_only_owner_is_the_sender_of_every_event": own["the_only_owner_is_the_sender_of_every_event"],
                           "the_maintainer_comment_names_that_owner": own["the_maintainer_comment_names_that_owner"]},
    }


def survivor_accounting(obs: dict) -> dict:
    """Trigger events ever added against those present at the pin.

    The first check is a partition of one list of names: it holds by construction and only guards this code. The
    checks that follow compare the history with the files, or a commit subject with a file, and could fail.
    """
    log, history = obs["trigger_log"], obs["trigger_file_history"]
    archived, outside = log["archived"], log["outside_the_archive"]
    absent = history["absent_files"]
    by_workflow = [row for row in absent if row["added_with_the_trigger_subject"]]
    at_pin = archived["events"] + sum(row["file"].endswith(".trigger.json") and not row["kind"].startswith("a schedule")
                                      for row in outside["files"])
    subjects = history["commits_with_the_trigger_subject"]
    check("partition: trigger files ever added = events + schedule definitions, events = present at the pin + absent",
          history["trigger_json_files_ever_added"] == history["trigger_events_ever_added"] + history["schedule_definitions"]
          and history["trigger_events_ever_added"] == history["events_present_at_the_pin"] + history["absent_at_the_pin"]
          and history["absent_at_the_pin"] == len(absent))
    check("cross-check: the events present at the pin by the history = the event files read at the pin",
          history["events_present_at_the_pin"] == at_pin)
    check("accounting: files written by the workflow = archived + left outside the archive + absent",
          history["written_by_the_trigger_workflow"]["ever"]
          == archived["events"] + outside["events_written_by_the_trigger_workflow"] + len(by_workflow))
    check("accounting: one commit with the trigger subject per file written by the workflow",
          subjects["commits"] == subjects["adding_exactly_one_trigger_file"]
          == history["written_by_the_trigger_workflow"]["ever"] == sum(subjects["by_type_in_the_subject"].values()))
    for kind, count in subjects["by_type_in_the_subject"].items():
        left = sum(row.get("type") == kind and "sender" in row for row in outside["files"])
        gone = sum(row["type_in_the_subject"] == kind for row in by_workflow)
        check("accounting: per type, subjects = archived + left outside the archive + absent",
              count == archived["by_type"].get(kind, 0) + left + gone, kind)
    compared = history["subject_against_file_content"]
    check("cross-check: the commit subject names the type and repo of every surviving workflow-written file",
          compared["type_or_repo_mismatches"] == 0 and compared["files_compared"]
          == archived["events"] + outside["events_written_by_the_trigger_workflow"])
    check("negative control: a planted wrong subject is counted as a mismatch",
          compared["mismatches_after_planting_one_wrong_subject"] == 1)
    return {
        "trigger_events_ever_added": history["trigger_events_ever_added"],
        "trigger_json_files_ever_added": history["trigger_json_files_ever_added"],
        "schedule_definitions": history["schedule_definitions"],
        "events_present_at_the_pin": history["events_present_at_the_pin"],
        "absent_at_the_pin": len(absent),
        "written_by_the_trigger_workflow": {
            "ever": history["written_by_the_trigger_workflow"]["ever"], "archived": archived["events"],
            "left_outside_the_archive": outside["events_written_by_the_trigger_workflow"], "absent": len(by_workflow),
            "archived_percent": rnd(Fraction(archived["events"], history["written_by_the_trigger_workflow"]["ever"]) * 100,
                                    "percent")},
        "absent_files": {
            "added_by": {label: sum(row["added_by"] == label for row in absent)
                         for label in sorted({row["added_by"] for row in absent})},
            "removed_by": {label: sum(row["removed_by"] == label for row in absent)
                           for label in sorted({row["removed_by"] for row in absent})},
            "removed_in_commit": {commit: sum(row["removed_in_commit"] == commit for row in absent)
                                  for commit in sorted({row["removed_in_commit"] for row in absent})},
            "with_a_colon_in_the_file_name": sum(row["colon_in_the_file_name"] for row in absent),
            "passed_through_processing": sum(row["passed_through_processing"] for row in absent),
            "ever_in_the_archive": sum(row["ever_in_the_archive"] for row in absent),
            "type_in_the_subject": {kind: sum(row["type_in_the_subject"] == kind for row in by_workflow)
                                    for kind in sorted({row["type_in_the_subject"] for row in by_workflow})},
            "repo_in_the_subject": {repo: sum(row["repo_in_the_subject"] == repo for row in by_workflow)
                                    for repo in sorted({row["repo_in_the_subject"] for row in by_workflow})},
            "not_written_by_the_workflow": [
                {"file": row["file"], "type_in_the_file_name": row["type_in_the_file_name"], "added_by": row["added_by"],
                 "subject_of_the_commit_that_added_it": row["subject_when_not_the_trigger_template"]}
                for row in absent if not row["added_with_the_trigger_subject"]],
            "sender_readable_from_commits_and_trees": 0},
        "subject_against_file_content": compared,
    }


def survivor_bounds(observed: int, absent: int, cases: list[dict]) -> dict:
    """The sender index if the absent files are given senders by assumption."""
    out = {}
    for case in cases:
        counts = {"each_from_a_different_new_sender": [observed] + [1] * absent,
                  "all_from_one_new_sender": [observed, absent],
                  "all_from_the_observed_sender": [observed + absent]}[case["key"]]
        out[case["key"]] = measures(counts)
    # Of all assignments, one new sender per file gives the largest N: a sender with one event adds 1 to the sum of
    # squared counts, the least an event can add. The check below compares only the listed cases.
    spread = out["each_from_a_different_new_sender"]["_number"]
    check("bound: of the listed assignments of the absent files, one new sender per file gives the largest effective "
          "number", all(spread >= item["_number"] for item in out.values()))
    return {"events_with_the_observed_sender": observed, "absent_files": absent, "events": observed + absent,
            "smallest_share_of_the_observed_sender_percent": rnd(Fraction(observed, observed + absent) * 100, "percent"),
            "cases": out}


def survivor_set(obs: dict, cfg: dict, senders: dict) -> dict:
    accounting = survivor_accounting(obs)
    absent = accounting["absent_at_the_pin"]
    return accounting | {
        "kind": "observed accounting from commits and trees; the cases are assumptions that bound the index",
        "note": cfg["note"],
        "archive_plus_the_absent_files": survivor_bounds(senders["archived"]["events"], absent, cfg["cases"]),
        "every_readable_event_plus_the_absent_files": survivor_bounds(senders["with_a_readable_sender"]["total"], absent,
                                                                     cfg["cases"]),
    }


def synthetic_ensembles(cfg: dict) -> dict:
    out = {}
    for item in cfg["ensembles"]:
        out[item["key"]] = {"label": item["label"], "counts": item["counts"]} | measures(item["counts"])
    equal = out["equal_14"]
    check("known answer: k equal actors give H = 1/k and N = k",
          equal["_index"] == Fraction(1, equal["actors"]) and equal["_number"] == equal["actors"])
    check("known answer: one actor gives H = 1 and N = 1", out["single_actor"]["_number"] == 1)
    harmonic = out["harmonic_14"]["counts"]
    check("synthetic input: in the harmonic ensemble, count x rank is constant",
          len({count * rank for rank, count in enumerate(harmonic, start=1)}) == 1)
    halving = out["halving_14"]["counts"]
    check("synthetic input: in the halving ensemble, each count is half the one before",
          all(a == 2 * b for a, b in zip(halving, halving[1:])))
    dominant = out["dominant_14"]["counts"]
    check("synthetic input: the dominant actor holds exactly 90%", Fraction(dominant[0], sum(dominant)) == Fraction(9, 10))
    return {"kind": "synthetic: imaginary ensembles, to give the index a scale", "note": cfg["note"], "ensembles": out}


def aggregate_simulation(cfg: dict, ensembles: dict) -> dict:
    """Synthetic check that the variance of a share-weighted average of independent actors is H times one actor's."""
    rows = {}
    for position, (key, item) in enumerate(ensembles["ensembles"].items()):
        total = sum(item["counts"])
        shares = [count / total for count in item["counts"]]
        rng = random.Random(cfg["seed"] + position)
        squares = 0.0
        for _ in range(cfg["occasions"]):
            aggregate = 0.0
            for share in shares:
                aggregate += share * rng.random()
            squares += (aggregate - 0.5) * (aggregate - 0.5)
        ratio = squares / cfg["occasions"] * 12.0  # variance of the aggregate over 1/12, the variance of one draw
        theory = float(item["_index"])
        check(f"simulation: the variance ratio is within {cfg['relative_tolerance']} (relative) of H",
              abs(ratio / theory - 1.0) < cfg["relative_tolerance"], f"{key}: {ratio} against {theory}")
        rows[key] = {"actors": item["actors"], "concentration_index": item["concentration_index"],
                     "simulated_variance_ratio": rnd(ratio, "simulated_ratio"),
                     "effective_number": item["effective_number"],
                     "simulated_effective_number": rnd(1.0 / ratio, "simulated_number"),
                     "relative_spread": item["relative_spread"],
                     "simulated_relative_spread": rnd(math.sqrt(ratio), "spread")}
    return {"kind": "synthetic: seeded simulation of independent actors", "note": cfg["note"], "seed": cfg["seed"],
            "occasions": cfg["occasions"], "generator": cfg["generator"], "variance_estimate": cfg["variance_estimate"],
            "by_ensemble": rows}


def group_sum(groups: list[dict], **where) -> int:
    """Commits in the groups whose fields equal the given values (a callable value is a test)."""
    return sum(g["commits"] for g in groups
               if all(test(g[key]) if callable(test) else g[key] == test for key, test in where.items()))


def commit_readings(log: dict) -> dict:
    """The same commits counted under different definitions of an identity."""
    groups, by_author = log["groups"], log["by_author"]
    workflow = log["author_configured_by_the_four_workflows"]
    template = "trigger workflow template"
    check("accounting: commit groups, authors, addresses and committers each sum to the commits read",
          group_sum(groups) == sum(by_author.values()) == sum(log["by_author_address"].values())
          == sum(row["commits"] for row in log["committers"]) == log["commits"])
    for label, count in by_author.items():
        letter = label.split()[1]  # "author A" owns "address A01", "address A02", ...
        check("accounting: an author's addresses sum to the author's commits",
              count == sum(n for tag, n in log["by_author_address"].items() if tag.split()[1].rstrip("0123456789") == letter))
    check("accounting: every commit with the trigger subject is by the author the workflows configure",
          group_sum(groups, subject=template) == group_sum(groups, subject=template, author=workflow) > 0)
    without = {label: count - group_sum(groups, author=label, subject=template) for label, count in by_author.items()}
    check("mailmap: every author string is one identity once the mailmap is applied",
          set(log["identities_per_author_after_the_mailmap"].values()) == {1})
    return {
        "by_author_string": {"counts": by_author} | measures(list(by_author.values())),
        "by_author_address": {"counts": log["by_author_address"]} | measures(list(log["by_author_address"].values())),
        "by_author_string_after_the_mailmap": {
            "identities_per_author_string": log["identities_per_author_after_the_mailmap"],
            "mailmap_entries": log["mailmap"]["entries"]} | measures(list(by_author.values())),
        "without_the_commits_that_carry_the_trigger_subject": {
            "commits_set_aside": group_sum(groups, subject=template),
            "percent_of_the_commits_of_the_author_the_workflows_configure":
                rnd(Fraction(group_sum(groups, subject=template), by_author[workflow]) * 100, "percent"),
            "counts": without} | measures(list(without.values())),
        "without_the_author_the_workflows_configure": {
            "commits_set_aside": by_author[workflow],
            "counts": {k: v for k, v in by_author.items() if k != workflow}}
            | measures([v for k, v in by_author.items() if k != workflow]),
    }


def commit_attribution(log: dict) -> dict:
    """What the author field leaves out: who created the commit, squash-style subjects and co-author trailers."""
    groups, trailers = log["groups"], log["co_author_trailers"]
    main = max(log["by_author"], key=log["by_author"].get)
    platform = [row["committer"] for row in log["committers"]
                if not row["also_an_author_string"] and row["addresses_all_no_reply_at_the_hosting_domain"]]
    check("committers: exactly one committer string never authors and uses a no-reply address at the hosting domain",
          len(platform) == 1)
    numbered = "ends with a pull request number"
    lines = sum(row["trailer_lines"] for row in trailers["co_authors"])
    check("accounting: trailer lines = sum over co-author labels = sum over commits of their trailer count",
          lines == trailers["trailer_lines"] == sum(g["co_author_trailers"] * g["commits"] for g in groups))
    check("accounting: commits with a trailer agree between the groups and the trailer summary",
          group_sum(groups, co_author_trailers=lambda n: n > 0) == trailers["commits_with_at_least_one_trailer"]
          == sum(trailers["by_author"].values()))
    no_reply = sum(trailers["lines_with_a_no_reply_address_by_domain"].values())
    bots = trailers["lines_whose_name_ends_with_bot"]
    sender_lines = trailers["lines_whose_name_is_a_trigger_sender"]
    check("accounting: the trailer lines that name a trigger sender have no no-reply address and no [bot] name",
          sender_lines == sum(row["trailer_lines"] for row in trailers["co_authors"] if row["same_string_as_a_trigger_sender"]
                              and not row["address_is_no_reply"] and not row["name_ends_with_bot"]))
    addresses = {tag: {"commits": count,
                       "created_by_the_platform_committer": group_sum(groups, address=tag, committer=platform[0])}
                 for tag, count in log["by_author_address"].items()
                 if tag.split()[1].rstrip("0123456789") == main.split()[1]}
    share = Fraction(trailers["by_author"].get(main, 0), log["by_author"][main])
    return {
        "main_author": main,
        "committers": log["committers"],
        "platform_committer": {
            "label": platform[0], "commits": group_sum(groups, committer=platform[0]),
            "authors_of_those_commits": sorted({g["author"] for g in groups if g["committer"] == platform[0]})},
        "addresses_of_the_main_author": addresses,
        "merge_commits": group_sum(groups, merge=True),
        "subjects_ending_with_a_pull_request_number": {
            "commits": group_sum(groups, subject=numbered),
            "by_author": {label: group_sum(groups, subject=numbered, author=label) for label in log["by_author"]},
            "created_by_the_platform_committer": group_sum(groups, subject=numbered, committer=platform[0]),
            "with_a_co_author_trailer": group_sum(groups, subject=numbered, co_author_trailers=lambda n: n > 0)},
        "co_author_trailers": {
            "commits_with_at_least_one": trailers["commits_with_at_least_one_trailer"],
            "by_author": trailers["by_author"],
            "percent_of_the_main_author_commits": rnd(share * 100, "percent"),
            "commits_with_two": group_sum(groups, co_author_trailers=2),
            "trailer_lines": lines,
            "distinct_names": trailers["distinct_trailer_names"],
            "lines_with_a_no_reply_address": no_reply,
            "domains_of_the_no_reply_addresses": len(trailers["lines_with_a_no_reply_address_by_domain"]),
            "names_with_a_no_reply_address": sum(row["address_is_no_reply"] for row in trailers["co_authors"]),
            "lines_whose_name_ends_with_bot": bots,
            "lines_whose_name_is_a_trigger_sender": sender_lines,
            "label_of_that_sender": sorted(row["co_author"] for row in trailers["co_authors"]
                                           if row["same_string_as_a_trigger_sender"]),
            "other_lines": lines - no_reply - bots - sender_lines,
            "names_that_are_also_an_author_string": sum(row["also_an_author_string"] for row in trailers["co_authors"])},
    }


def commit_authors(obs: dict) -> dict:
    log = obs["commit_log"]
    history = obs["source"]["git_history"]
    return {"kind": "observed counts of labels from the commit history; indices computed",
            "commits": log["commits"], "first_commit_day_utc": history["first_commit_day_utc"],
            "last_commit_day_utc": history["last_commit_day_utc"],
            "author_the_workflows_configure": log["author_configured_by_the_four_workflows"],
            "readings": commit_readings(log)} | commit_attribution(log)


def workflow_pushes(obs: dict, cfg: dict) -> dict:
    """How many of the workflow's own pushes can have started a run, under the assumption in scenarios.json."""
    subjects = obs["trigger_file_history"]["commits_with_the_trigger_subject"]
    versions = obs["trigger_log"]["producer"]["versions"]
    pushes, push_triggers = subjects["commits"], subjects["by_type_in_the_subject"]["push"]
    check("bound: the workflow pushed more commits than push triggers were ever written", pushes > push_triggers)
    return {
        "kind": "observed counts; the bound rests on the assumption below",
        "assumption": cfg["assumption"],
        "commits_pushed_by_the_workflow": pushes,
        "push_triggers_ever_written": push_triggers,
        "workflow_pushes_that_started_no_run_at_least": pushes - push_triggers,
        "trigger_subjects_ending_with_skip_ci": versions["trigger_subjects_ending_with_skip_ci"],
        "last_commit_with_the_trigger_subject": versions["last_commit_with_the_trigger_subject"],
        "later_changes_to_the_workflow_file": versions["later_changes_to_the_workflow_file"],
    }


def records_compared(senders: dict, survivors: dict, commits: dict) -> list[dict]:
    """One row per record and per definition of an identity: the table of the lesson."""
    def row(record: str, identity: str, measured: dict) -> dict:
        return {"record": record, "an_identity_is": identity, "identities": measured["actors"], "events": measured["events"],
                "largest_share_percent": measured["largest_share_percent"],
                "concentration_index": measured["concentration_index"], "effective_number": measured["effective_number"],
                "half_coverage_count": measured["half_coverage_count"]}
    worst = survivors["archive_plus_the_absent_files"]["cases"]["each_from_a_different_new_sender"]
    readings = commits["readings"]
    return [
        row("trigger archive", "the sender field", senders["archived"]["senders"]),
        row("trigger archive and the absent files, each given a new sender (assumption)", "the sender field", worst),
        row("commits", "the author string", readings["by_author_string"]),
        row("commits", "the author address", readings["by_author_address"]),
        row("commits without those that carry the trigger subject", "the author string",
            readings["without_the_commits_that_carry_the_trigger_subject"]),
    ]


def hypothesis_test(thresholds: dict, survivors: dict, commits: dict) -> dict:
    """The thresholds were fixed before this script existed; this only reports which parts hold."""
    cases = {**survivors["archive_plus_the_absent_files"]["cases"]}
    wide = survivors["every_readable_event_plus_the_absent_files"]["cases"]
    senders = max(max(item["_number"] for item in cases.values()), max(item["_number"] for item in wide.values()))
    authors = commits["readings"]["by_author_string"]["_number"]
    filtered = commits["readings"]["without_the_commits_that_carry_the_trigger_subject"]["_number"]
    limit_1 = Fraction(str(thresholds["effective_senders_with_the_absent_files_at_most"]))
    limit_2 = Fraction(str(thresholds["effective_commit_authors_at_most"]))
    return {
        "thresholds": {k: v for k, v in thresholds.items() if k != "note"},
        "part_1_senders": {"largest_effective_number_over_all_cases": rnd(senders, "effective_number"),
                           "holds": senders <= limit_1},
        "part_2_commit_authors": {
            "effective_number_by_author_string": rnd(authors, "effective_number"), "holds": authors <= limit_2,
            "after_setting_aside_the_trigger_subject_commits": rnd(filtered, "effective_number"),
            "that_reading_was_chosen_after_seeing_the_counts": True},
        "every_part_holds": senders <= limit_1 and authors <= limit_2,
    }


def worked_examples(cfg: dict, survivors: dict, ensembles: dict, commits: dict) -> dict:
    ex5 = cfg["exercise_5"]
    counts = ex5["counts"]
    grown = [counts[0]] + [count * ex5["small_actors_multiplied_by"] for count in counts[1:]]
    first, second = measures(counts), measures(grown)
    need = ex5["criterion_effective_number_at_least"]
    targets = []
    for text in cfg["spread_targets"]["targets"]:
        target = Fraction(text)
        needed = 1 / (target * target)
        check("worked example: the number of actors for a target spread is a whole number", needed.denominator == 1)
        targets.append({"relative_spread": text, "equal_independent_actors_needed": int(needed)})
    equal = ensembles["ensembles"]["equal_14"]
    return {
        "exercise_1": survivors["archive_plus_the_absent_files"],
        "exercise_2": {"counts": cfg["exercise_2"]["counts"]} | measures(cfg["exercise_2"]["counts"]),
        "exercise_3": {"relative_spread_of_14_equal_independent_actors": equal["relative_spread"]},
        "exercise_4": {"by_author_string": commits["readings"]["by_author_string"],
                       "without_the_commits_that_carry_the_trigger_subject":
                           commits["readings"]["without_the_commits_that_carry_the_trigger_subject"]},
        "exercise_5": {
            "criterion_effective_number_at_least": need,
            "as_logged": {"counts": counts} | first | {"meets_the_criterion": first["_number"] >= need},
            "small_actors_multiplied": {"factor": ex5["small_actors_multiplied_by"], "counts": grown} | second
                                       | {"meets_the_criterion": second["_number"] >= need},
            "equal_actors_would_give": len(counts)},
        "spread_targets": targets,
    }


def negative_controls(cfg: dict, obs: dict, texts: dict[str, str]) -> dict:
    moved = cfg["events_moved_to_a_second_sender"]
    planted = copy.deepcopy(obs["trigger_log"]["archived"]["by_sender"])
    label = next(iter(planted))
    planted[label] -= moved
    planted["planted second sender"] = moved
    before = measures(list(obs["trigger_log"]["archived"]["by_sender"].values()))
    after = measures(list(planted.values()))
    check("negative control: moving one event to a second sender raises the count of senders and the effective number",
          before["actors"] == 1 and after["actors"] == 2 and after["_number"] > before["_number"] == 1)
    hand = []
    for case in cfg["hand_computed_cases"]:
        got = measures(case["counts"])
        check("hand-computed case: index, effective number and half-coverage count",
              (got["_index"], got["_number"], got["half_coverage_count"])
              == (Fraction(case["concentration_index"]), Fraction(case["effective_number"]), case["half_coverage_count"]),
              str(case["counts"]))
        hand.append({"counts": case["counts"], "concentration_index": case["concentration_index"],
                     "effective_number": case["effective_number"], "half_coverage_count": got["half_coverage_count"]})
    signs = {name: text.count("@") for name, text in texts.items()}
    planted_signs = (texts["observed-input.json"] + "@").count("@")
    check("identities: no at sign (no e-mail address, no handle) in the two input files", sum(signs.values()) == 0)
    check("negative control: an at sign planted in a copy of the input is counted", planted_signs == 1)
    identity = obs["identity_check"]
    check("identities: extract.py found none of the raw identity strings in its output, and its check can fail",
          identity["found_in_this_file"] == 0 and identity["found_after_planting_one_of_them"] is True)
    return {
        "one_event_moved_to_a_second_sender": {"senders_before": before["actors"], "senders_after": after["actors"],
                                               "effective_number_before": before["effective_number"],
                                               "effective_number_after": after["effective_number"]},
        "hand_computed_cases": hand,
        "at_signs_in_the_input_files": signs,
        "at_signs_after_planting_one": planted_signs,
        "identity_check_of_the_extract": identity,
    }


def transfer_task(task: dict) -> dict:
    counts = task["counts"]
    everyone = measures(list(counts.values()))
    people = {name: count for name, count in counts.items() if name != task["automation_account"]}
    without = measures(list(people.values()))
    top = max(counts, key=counts.get)
    deleted = task["deleted_events"]
    cases = {
        "all_from_the_largest_account": measures([count + deleted * (name == top) for name, count in counts.items()]),
        "each_from_a_different_new_account": measures(list(counts.values()) + [1] * deleted),
    }
    check("transfer task: the listed cases are the ones computed",
          [case["key"] for case in task["deleted_cases"]] == list(cases))
    check("transfer task: setting the automation account aside lowers the effective number",
          without["_number"] < everyone["_number"])
    check("transfer task: the two cases bracket the effective number of the surviving log",
          cases["all_from_the_largest_account"]["_number"] < everyone["_number"]
          < cases["each_from_a_different_new_account"]["_number"])
    equal = task["equal_actors_for_comparison"]
    return {
        "note": task["note"],
        "q1_index": {"counts": counts, "shares": {name: rnd(Fraction(count, everyone["events"]), "share")
                                                  for name, count in counts.items()}} | everyone,
        "q2_without_the_automation_account": {"set_aside": task["automation_account"], "counts": people} | without,
        "q3_deleted_events": {"deleted": deleted, "events": everyone["events"] + deleted, "cases": cases},
        "q4_spread": {"relative_spread": everyone["relative_spread"], "equal_actors": equal,
                      "relative_spread_of_equal_actors": rnd(math.sqrt(Fraction(1, equal)), "spread"),
                      "effective_number": everyone["effective_number"]},
    }


def strip_private(value):
    if isinstance(value, dict):
        return {key: strip_private(item) for key, item in value.items() if not key.startswith("_")}
    if isinstance(value, list):
        return [strip_private(item) for item in value]
    return value


def analyze(obs: dict, scenarios: dict, texts: dict[str, str]) -> dict:
    if scenarios["rounding"] != {f"{key}_decimals": value for key, value in DECIMALS.items()}:
        raise ValueError("scenarios.json rounding does not match analyze.py")
    if obs["module_id"] != scenarios["module_id"] or obs["source"]["commit"] is None:
        raise ValueError("observed-input.json is not the snapshot of the pinned commit for this module")
    senders = observed_senders(obs)
    survivors = survivor_set(obs, scenarios["absent_file_cases"], senders)
    ensembles = synthetic_ensembles(scenarios["synthetic_ensembles"])
    simulation = aggregate_simulation(scenarios["aggregate_simulation"], ensembles)
    commits = commit_authors(obs)
    pushes = workflow_pushes(obs, scenarios["workflow_pushes"])
    compared = records_compared(senders, survivors, commits)
    verdict = hypothesis_test(scenarios["hypothesis_thresholds"], survivors, commits)
    worked = worked_examples(scenarios["worked_examples"], survivors, ensembles, commits)
    controls = negative_controls(scenarios["negative_controls"], obs, texts)
    transfer = transfer_task(scenarios["transfer_task"])
    return strip_private({
        "module_id": scenarios["module_id"],
        "source_commit": obs["source"]["commit"],
        "rounding": "shares and concentration indices to 6 decimals, effective numbers and relative spreads to 4, "
                    "percentages to 2, simulated variance ratios to 4 and simulated effective numbers to 2; exact "
                    "fractions are rounded half to even",
        "definitions": scenarios["definitions"],
        "observed_senders": senders,
        "survivor_set": survivors,
        "synthetic_ensembles": ensembles,
        "aggregate_simulation": simulation,
        "commit_authors": commits,
        "workflow_pushes": pushes,
        "records_compared": compared,
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
        texts = {"observed-input.json": args.input.read_text(encoding="utf-8"),
                 "scenarios.json": args.scenarios.read_text(encoding="utf-8")}
        result = analyze(json.loads(texts["observed-input.json"]), json.loads(texts["scenarios.json"]), texts)
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
