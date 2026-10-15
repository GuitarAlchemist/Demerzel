#!/usr/bin/env python3
"""PSY-021 analysis: which conservation statements about the trigger log can be checked.

Reads observed-input.json (the trigger folders at the pinned commit, the add
and delete records of their Git history, and the quoted sentences) and
scenarios.json (hand-written ledgers, assumptions, the learner task), never
the repository, and writes results.json.

One function, audit(), compares a listing of files with a history of
additions and deletions. It is applied to the observed data, to five
hand-written cases whose answers were fixed in advance, to the observed data
with one error planted, and to the learner task: a balance that holds on the
observed data comes from the detector that fires on the planted errors.

Every number is a count or a ratio of two counts; no random number is drawn.

Run from the repository root:
    python -I -B scripts/streeling_fixtures/psychohistory/psy-021/analyze.py
    python -I -B scripts/streeling_fixtures/psychohistory/psy-021/analyze.py --check
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path

# This program lives under scripts/ (CONTRIBUTING.md: no executable code outside scripts/); its data stays
# under state/streeling/fixtures/. FIXTURE_FILE is the path the program would have next to that data.
FIXTURE_FILE = (Path(__file__).resolve().parents[4]
                / "state/streeling/fixtures/psychohistory/psy-021" / Path(__file__).name)

HERE = FIXTURE_FILE.parent
PERCENT_DECIMALS = 2
RECORD = re.compile(r"^([+-])([a-z]+)@(\d+)$")
STAMP_LENGTH = len("2026-03-20T13-04-07Z")  # an event's file name is <stamp>-<type>
CHECKS: dict[str, int] = {}  # self-check -> times evaluated
# Why three balances between the files and the history cannot fail on a verified clone.
TELESCOPING = ("files against history, which are not separate records: Git stores snapshots and derives additions and "
               "deletions by comparing consecutive ones, and the files are the last snapshot")


def check(name: str, condition: bool, detail: str = "") -> None:
    """A self-check that can fail: abort instead of writing a wrong result."""
    if not condition:
        raise AssertionError(f"self-check failed: {name}" + (f" ({detail})" if detail else ""))
    CHECKS[name] = CHECKS.get(name, 0) + 1


def pct(part: int, whole: int) -> float:
    return round(100 * part / whole, PERCENT_DECIMALS)


def tally(values: list) -> dict:
    return dict(sorted(Counter(values).items()))


def event_type(name: str) -> str:
    """The type an event's file name carries; one name writes it with a hyphen where its JSON has an underscore."""
    return name[STAMP_LENGTH + 1:].replace("-", "_")


def parse_rows(rows: list[str]) -> dict[str, list[tuple[str, str, int]]]:
    """History rows '<name> +folder@n -folder@n ...' -> {name: [(sign, folder, n)]}, commits ascending."""
    events: dict[str, list[tuple[str, str, int]]] = {}
    for row in rows:
        name, *records = row.split(" ")
        parsed = [RECORD.match(record) for record in records]
        if name in events or not parsed or not all(parsed):
            raise ValueError(f"malformed or repeated history row: {row!r}")
        events[name] = [(m.group(1), m.group(2), int(m.group(3))) for m in parsed]
        if [n for _, _, n in events[name]] != sorted(n for _, _, n in events[name]):
            raise ValueError(f"records out of commit order: {row!r}")
    return events


def replay(records: list[tuple[str, str, int]]) -> dict:
    """Follow one file name through its records: where it ends up, and what each commit did to it."""
    held: list[str] = []
    out = {"created": 0, "moves": [], "removals": [], "copies": 0, "faults": 0}
    for n in sorted({n for _, _, n in records}):
        deleted = [folder for sign, folder, k in records if k == n and sign == "-"]
        added = [folder for sign, folder, k in records if k == n and sign == "+"]
        before = list(held)
        for folder in deleted:
            if folder in held:
                held.remove(folder)
            else:
                out["faults"] += 1  # deleted from a folder the history never put it in
        for folder in added:
            if folder in held:
                out["faults"] += 1  # added to a folder it is already in
            else:
                held.append(folder)
        pairs = min(len(deleted), len(added))
        if not before and added:
            out["created"] += 1
            out["copies"] += len(added) - 1
        elif added:
            out["moves"] += [(deleted[i], added[i], n) for i in range(pairs)]
            out["copies"] += len(added) - pairs
        if before and not held:
            out["removals"].append((deleted[-1], n))  # gone from every folder: not a move
    return out | {"held": held}


def reconcile(folders: list[str], disk: dict, played: dict) -> dict:
    """Name by name: the folder the history leaves each file in against the folder it is listed in."""
    expected = {folder: [name for name, state in played.items() if folder in state["held"]] for folder in folders}
    missing = [f"{folder}/{name}" for folder in folders for name in expected[folder] if name not in set(disk[folder])]
    unexpected = [f"{folder}/{name}" for folder in folders for name in disk[folder] if name not in set(expected[folder])]
    return {"expected_on_disk": sum(len(names) for names in expected.values()),
            "matched": sum(len(names) for names in expected.values()) - len(missing),
            "expected_but_missing": missing, "on_disk_but_unexpected": unexpected}


def diagnosis(result: dict) -> str:
    """What the pattern of holding and failing checks says, in one phrase."""
    names = result["names"]
    items_agree = not (names["expected_but_missing"] or names["on_disk_but_unexpected"] or result["names_in_two_folders"])
    counts_agree = result["open_system"]["holds"] and not result["folders_out_of_balance"]
    if items_agree and result["closed_system"]["holds"]:
        return "nothing left: every file created is listed where the history puts it"
    if items_agree:
        return "files left, and every departure is on record"
    if counts_agree:
        return "offsetting errors: the counts balance and the items do not"
    return "the records do not explain the listing"


def audit(folders: list[str], disk: dict[str, list[str]], rows: list[str]) -> dict:
    """Compare a listing of files per folder with a history of additions and deletions."""
    events = parse_rows(rows)
    played = {name: replay(records) for name, records in events.items()}
    flows = {}
    for folder in folders:
        added = sum(sign == "+" and place == folder for records in events.values() for sign, place, _ in records)
        deleted = sum(sign == "-" and place == folder for records in events.values() for sign, place, _ in records)
        flows[folder] = {"added": added, "deleted": deleted, "added_minus_deleted": added - deleted,
                         "on_disk": len(disk[folder]), "difference": len(disk[folder]) - (added - deleted)}
    listed = [name for folder in folders for name in disk[folder]]
    created = sum(state["created"] for state in played.values())
    removed = [(name, folder, n) for name, state in played.items() for folder, n in state["removals"]]
    moves = tally([f"{a}>{b}" for state in played.values() for a, b, _ in state["moves"]])
    result = {
        "file_names_in_the_history": len(events),
        "created": created,
        "moves": moves,
        "copies_recorded": sum(state["copies"] for state in played.values()),
        "removals_recorded": len(removed),
        "removals_by_folder": tally([folder for _, folder, _ in removed]),
        "inconsistent_records": sum(state["faults"] for state in played.values()),
        "files_on_disk": len(listed),
        "distinct_names_on_disk": len(set(listed)),
        "names_in_two_folders": sorted(name for name, times in Counter(listed).items() if times > 1),
        "flows": flows,
        "folders_out_of_balance": [folder for folder in folders if flows[folder]["difference"] != 0],
        "closed_system": {"created": created, "files_on_disk": len(listed), "difference": created - len(listed),
                          "holds": created == len(listed)},
        "open_system": {"created": created, "files_on_disk_plus_removals": len(listed) + len(removed),
                        "difference": created - len(listed) - len(removed),
                        "holds": created == len(listed) + len(removed)},
        "names": reconcile(folders, disk, played),
        "_events": events, "_played": played, "_removed": removed,
    }
    check("audit: additions minus deletions, summed over the folders, equals created minus removed plus copies",
          sum(flow["added_minus_deleted"] for flow in flows.values())
          == created - len(removed) + result["copies_recorded"] or result["inconsistent_records"] > 0)
    return result | {"reading": diagnosis(result)}


def summary(result: dict) -> dict:
    """The part of an audit that the hand-written cases state in advance."""
    return {"created": result["created"], "files_on_disk": result["files_on_disk"],
            "removals_recorded": result["removals_recorded"],
            "closed_system_difference": result["closed_system"]["difference"],
            "open_system_difference": result["open_system"]["difference"],
            "folders_out_of_balance": result["folders_out_of_balance"],
            "names_in_two_folders": result["names_in_two_folders"],
            "expected_but_missing": result["names"]["expected_but_missing"],
            "on_disk_but_unexpected": result["names"]["on_disk_but_unexpected"]}


def listing(files: dict, folders: list[str]) -> tuple[dict[str, list[str]], list[str]]:
    """Event file names per folder, and the run ids of the files that carry one."""
    disk, run_ids = {}, []
    for folder in folders:
        pairs = [row.split(" ") for row in files["event_files"][folder]]
        disk[folder] = [name for name, _ in pairs]
        run_ids += [run_id for _, run_id in pairs if run_id != "-"]
    return disk, run_ids


def cross_table(folders: list[str], rows: list[tuple[str, str]], labels: dict) -> dict:
    """Counts of (type, place) pairs with both margins; 'place' is a folder or 'removed'."""
    places = [labels.get(folder, folder) for folder in folders] + sorted({p for _, p in rows} - set(folders))
    table = {}
    for kind in sorted({kind for kind, _ in rows}):
        line = {place: sum(1 for k, p in rows if k == kind and labels.get(p, p) == place) for place in places}
        table[kind] = line | {"total": sum(line.values())}
    totals = {place: sum(line[place] for line in table.values()) for place in places}
    check("cross table: the row totals and the column totals both add up to the number of rows",
          sum(line["total"] for line in table.values()) == len(rows) == sum(totals.values()))
    return {"by_type": table, "totals": totals | {"total": len(rows)}}


def files_section(obs: dict, scn: dict, disk: dict, run_ids: list[str]) -> dict:
    """What the files at the pinned commit say on their own, without any history."""
    files, folders, labels = obs["files"], scn["folders"]["order"], scn["folders"]["labels"]
    names = [name for folder in folders for name in disk[folder]]
    keys = sorted({key for shape in files["shapes"] for key in shape["keys"]})
    detail_keys = sorted({key for shape in files["shapes"] for key in shape["details_keys"]})
    hints = scn["lifecycle_key_hints"]["fragments"]
    stated = obs["documents"]["quotes"]
    workflow_shaped = sum(shape["files"] for shape in files["shapes"] if shape["is_the_workflow_shape"])
    return {
        "source": "the files of the pinned commit only; no history",
        "event_files": {labels[folder]: len(disk[folder]) for folder in folders} | {"total": len(names)},
        "by_type_and_folder": cross_table(folders, [(event_type(name), folder) for folder in folders
                                                    for name in disk[folder]], labels),
        "files_that_are_not_events": [f"{folder}/{entry['file']}" for folder in folders
                                      for entry in files["other_files"][folder]],
        "shapes": [{key: shape[key] for key in ("files", "keys", "details_keys", "by_folder", "is_the_workflow_shape")}
                   for shape in files["shapes"]],
        "keys": {"top_level": keys, "inside_details": detail_keys, "hints": hints,
                 "keys_that_could_record_what_became_of_the_event":
                     [key for key in keys + detail_keys if any(hint in key.lower() for hint in hints)]},
        "one_folder_per_file_name": {"file_names": len(names), "distinct": len(set(names)),
                                     "names_in_two_folders": len(names) - len(set(names))},
        "run_ids": {"files_with_a_run_id": len(run_ids), "distinct": len(set(run_ids)),
                    "run_ids_seen_twice": len(run_ids) - len(set(run_ids)),
                    "files_without_a_run_id": len(names) - len(run_ids)},
        "stated_counts": {"orphans_stated_by_the_workflow_file": stated["workflow_orphans_stated"],
                          "orphaned_triggers_stated_by_the_skill_file": stated["skill_orphans_stated"],
                          "archived_files_on_disk": len(disk["archived"]),
                          "both_statements_equal_the_files": stated["workflow_orphans_stated"]
                          == stated["skill_orphans_stated"] == len(disk["archived"]),
                          "event_files_of_the_workflow_shape_on_disk": workflow_shaped,
                          "of_which_outside_the_archive": workflow_shaped - len(disk["archived"])},
        "count_of_files_ever_produced_recorded_at_the_pin": None,
    }


def removal_groups(history: dict, result: dict) -> list[dict]:
    """The deletions that were not moves, grouped by the commit that made them."""
    commits = {entry["n"]: entry for entry in history["other_commits"]}
    groups: dict[int, dict] = {}
    for name, folder, n in result["_removed"]:
        check("removals: every commit that deleted a trigger file is listed in full in the snapshot", n in commits)
        group = groups.setdefault(n, {"commit": commits[n]["commit"], "committed_utc": commits[n]["committed_utc"],
                                      "subject": commits[n]["subject"], "deleted_from": folder, "files": []})
        check("removals: one commit deletes from one folder", group["deleted_from"] == folder)
        group["files"].append(name)
    return [group | {"count": len(group["files"])} for _, group in sorted(groups.items())]


def producer_cross_check(history: dict, result: dict) -> dict:
    """Commit subjects against trees: did each producer commit add one file of the type its subject names?"""
    kind_of = {n: kind for kind, numbers in history["producer_commits"].items() for n in numbers}
    created_by: dict[int, list[str]] = {}
    for name, records in result["_events"].items():
        check("history: the first record of every file name is an addition", records[0][0] == "+")
        created_by.setdefault(records[0][2], []).append(name)
    others = {entry["n"]: entry["subject"] for entry in history["other_commits"]}
    per_type = {}
    for kind, numbers in history["producer_commits"].items():
        made = [name for n in numbers for name in created_by.get(n, [])]
        per_type[kind] = {"producer_commits": len(numbers), "files_they_created": len(made),
                          "files_of_the_type_the_subject_names": sum(event_type(name) == kind for name in made)}
    by_producers = sum(line["files_they_created"] for line in per_type.values())
    return {
        "subject_pattern": history["producer_subject_pattern"],
        "by_type": per_type,
        "producer_commits": len(kind_of),
        "producer_commits_that_created_exactly_one_file": sum(len(created_by.get(n, [])) == 1 for n in kind_of),
        "producer_commits_that_deleted_a_file": len({n for records in result["_events"].values()
                                                     for sign, _, n in records if sign == "-" and n in kind_of}),
        "files_created_by_producer_commits": by_producers,
        "files_created_by_other_commits": [{"file": name, "commit_subject": others[n]}
                                           for n, made in sorted(created_by.items()) if n not in kind_of for name in made],
        "holds": all(line["producer_commits"] == line["files_they_created"] == line["files_of_the_type_the_subject_names"]
                     for line in per_type.values()),
        "_created_by_producers": {name for n in kind_of for name in created_by.get(n, [])},
    }


def consumption(scn: dict, obs: dict, result: dict, producers: dict) -> dict:
    """Files deleted from the folder the driver's rule empties after processing, against everything else."""
    exit_folder = scn["folders"]["designed_exit"]
    consumed = [name for name, folder, _ in result["_removed"] if folder == exit_folder]
    by_producer = [name for name in consumed if name in producers["_created_by_producers"]]
    created, made = result["created"], producers["files_created_by_producer_commits"]
    stated = obs["documents"]["quotes"]["workflow_orphans_stated"]
    return {
        "rule_quoted_from_the_skill_file": obs["documents"]["quotes"]["skill_consumption_rule"],
        "definition": f"consumed = deleted from {exit_folder}/, the folder that rule empties after processing; "
                      "the files themselves carry no record of processing",
        "manual_cycles_stated_by_the_skill_file": obs["documents"]["quotes"]["skill_manual_cycles_stated"],
        "consumed": len(consumed),
        "consumed_created_by_the_producer": len(by_producer),
        "never_consumed": created - len(consumed),
        "created_by_the_producer": made,
        "created_by_the_producer_never_consumed": made - len(by_producer),
        "orphans_stated_by_the_workflow_file": stated,
        "never_consumed_minus_stated": created - len(consumed) - stated,
        "producer_never_consumed_minus_stated": made - len(by_producer) - stated,
    }


def archive_sweep(history: dict, result: dict, folders: list[str]) -> dict:
    """The commit that moved the most files into the archive: what was pending before it, what it left behind."""
    arrivals = Counter(n for records in result["_events"].values() for sign, folder, n in records
                       if sign == "+" and folder == "archived")
    n_star = max(arrivals, key=lambda n: (arrivals[n], -n))
    before = [name for name, records in result["_events"].items()
              if folders[0] in replay([record for record in records if record[2] < n_star])["held"]]
    moved = [name for name in before if ("+", "archived", n_star) in result["_events"][name]]
    commit = next(entry for entry in history["other_commits"] if entry["n"] == n_star)
    return {"commit": commit["commit"], "committed_utc": commit["committed_utc"], "subject": commit["subject"],
            "parents": commit["parents"], "commits_that_added_files_to_the_archive": len(arrivals),
            "pending_just_before": len(before), "moved_to_the_archive": len(moved),
            "left_pending": len(before) - len(moved), "left_pending_files": sorted(set(before) - set(moved))}


def history_section(obs: dict, scn: dict, result: dict) -> dict:
    """What the add and delete records of the Git history say, and how they compare with the files."""
    history, folders, labels = obs["history"], scn["folders"]["order"], scn["folders"]["labels"]
    recount = {sign: tally([folder for row in history["events"] + history["other_files"]
                            for record in row.split(" ")[1:] if record[0] == sign
                            for folder in [RECORD.match(record).group(2)]]) for sign in "+-"}
    check("history: the rows carry exactly the A and D records that extract.py counted",
          recount["+"] == dict(sorted(history["raw_records"]["A"].items()))
          and recount["-"] == dict(sorted(history["raw_records"]["D"].items())))
    played, created = result["_played"], result["created"]
    fate = [(event_type(name), state["held"][0] if state["held"] else "removed") for name, state in played.items()]
    fates = Counter(place for _, place in fate)
    producers = producer_cross_check(history, result)
    removed = result["_removed"]
    return {
        "source": history["source"],
        "commits": {key: history[key] for key in ("commits_reachable_from_the_pin", "commits_on_the_first_parent_chain",
                                                  "commits_read")}
                   | {"producer_commits": producers["producer_commits"], "other_commits": len(history["other_commits"])},
        "paths_ever_added": history["paths_ever_added"],
        "raw_records": {"added": recount["+"], "deleted": recount["-"],
                        "added_total": sum(recount["+"].values()), "deleted_total": sum(recount["-"].values())},
        "created": created,
        "file_names_created_more_than_once": sum(state["created"] > 1 for state in played.values()),
        "flows": {labels[folder]: result["flows"][folder] for folder in folders},
        "moves": result["moves"],
        "fates": {"created": created} | {labels[folder]: fates[folder] for folder in folders}
                 | {"removed": fates["removed"]},
        "fates_percent_of_created": {labels[folder]: pct(fates[folder], created) for folder in folders}
                                    | {"removed": pct(fates["removed"], created)},
        "fates_by_type": cross_table(folders, fate, labels),
        "removals": removal_groups(history, result),
        "removed_by_folder": {labels[folder]: count for folder, count in result["removals_by_folder"].items()},
        "removed_by_day_in_the_file_name": tally([name[:10] for name, _, _ in removed]),
        "removed_by_type": tally([event_type(name) for name, _, _ in removed]),
        "producer_cross_check": producers,
        "consumption": consumption(scn, obs, result, producers),
        "archive_sweep": archive_sweep(history, result, folders),
    }


def checked_claims(scn: dict, files: dict, history: dict, result: dict) -> list[tuple]:
    """(id, kind, statement, where the two sides come from, left side, right side, holds) for C1 to C9."""
    labels, order = scn["folders"]["labels"], scn["folders"]["order"]
    on_disk = [result["flows"][folder]["on_disk"] for folder in order]
    by_flow = [result["flows"][folder]["added_minus_deleted"] for folder in order]
    names, cross, ids = result["names"], history["producer_cross_check"], files["run_ids"]
    stated, one = files["stated_counts"], files["one_folder_per_file_name"]
    type_total = sum(line["total"] for line in files["by_type_and_folder"]["by_type"].values())
    return [
        ("C1", "by_construction", "the counts by type add up to the number of event files on disk",
         "files, one count", type_total, files["event_files"]["total"], type_total == files["event_files"]["total"]),
        ("C2", "auditable", "no file name is in two folders", "files, three folders",
         one["distinct"], one["file_names"], one["names_in_two_folders"] == 0),
        ("C3", "auditable", "no run id appears in two files", "files",
         ids["distinct"], ids["files_with_a_run_id"], ids["run_ids_seen_twice"] == 0),
        ("C4", "auditable", "the archive holds the number of files that the workflow file and the skill file state",
         "files against two documents", stated["archived_files_on_disk"],
         [stated["orphans_stated_by_the_workflow_file"], stated["orphaned_triggers_stated_by_the_skill_file"]],
         stated["both_statements_equal_the_files"]),
        ("C5", "by_construction", "in each folder, files on disk = files added - files deleted ("
         + ", ".join(labels[folder] for folder in order) + ")", TELESCOPING,
         on_disk, by_flow, not result["folders_out_of_balance"]),
        ("C6", "by_construction", "name by name, each file is in the folder the history leaves it in",
         TELESCOPING, names["matched"], names["expected_on_disk"],
         not (names["expected_but_missing"] or names["on_disk_but_unexpected"])),
        ("C7", "auditable", "closed system: files created = files archived + pending + in processing",
         "history against files", result["closed_system"]["created"], result["closed_system"]["files_on_disk"],
         result["closed_system"]["holds"]),
        ("C8", "by_construction", "open system: files created = files on disk + files deleted without being moved",
         TELESCOPING, result["open_system"]["created"],
         result["open_system"]["files_on_disk_plus_removals"], result["open_system"]["holds"]),
        ("C9", "auditable", "each producer commit created one file of the type its subject names",
         "history: commit subjects against trees; one workflow step writes both from one variable, so the check "
         "can fail (a stray file in a producer commit) but is not an independent count",
         cross["files_created_by_producer_commits"],
         cross["producer_commits"], cross["holds"]),
    ]


def claims_section(scn: dict, files: dict, history: dict, result: dict) -> dict:
    """Each statement with the kind this module gives it, its two sides, and whether it holds."""
    rows = [{"id": cid, "kind": kind, "statement": text, "sides_come_from": source, "left": left, "right": right,
             "holds": holds} for cid, kind, text, source, left, right, holds in checked_claims(scn, files, history, result)]
    for row in rows:
        sides = row["right"] if row["id"] == "C4" else [row["right"]]
        check("claims: 'holds' agrees with the two sides shown", row["holds"] == all(row["left"] == side for side in sides))
    rows += [
        {"id": "C10", "kind": "not_recorded", "statement": "every archived trigger was processed",
         "missing_record": "no key of any event file records processing, an outcome or an archival time",
         "keys_found": files["keys"]["keys_that_could_record_what_became_of_the_event"], "holds": None},
        {"id": "C11", "kind": "not_recorded", "statement": "every firing of the producer became a committed file",
         "missing_record": "the repository holds no list of the workflow's runs; a file the workflow wrote and "
                           "could not push never reached a commit", "holds": None},
        {"id": "C12", "kind": "analogy", "statement": "learning momentum p_L is conserved",
         "missing_record": "no value of p_L is recorded in the file the policy names for it", "holds": None},
    ]
    return {"kinds": scn["claim_kinds"], "claims": rows, "count_by_kind": tally([row["kind"] for row in rows]),
            "auditable_that_hold": sum(row["holds"] is True and row["kind"] == "auditable" for row in rows),
            "auditable_that_fail": [row["id"] for row in rows if row["holds"] is False]}


def testable_version(cfg: dict) -> dict:
    """Synthetic: three versions of the momentum claim on one imaginary series, and what each one forbids."""
    cycles, tolerance = cfg["cycles"], cfg["tolerance"]
    values = [cycle["beliefs_gained"] - cycle["beliefs_lost"] for cycle in cycles]  # cycles_elapsed = 1

    def reading(change: int) -> str:
        return "stable" if abs(change) <= tolerance else ("growing" if change > 0 else "declining")

    steps = [{"from_cycle": a["cycle"], "to_cycle": b["cycle"], "change": y - x, "label": reading(y - x),
              "compound_ran_at_all_levels_in_both": a["compound_ran_at_all_levels"] and b["compound_ran_at_all_levels"]}
             for (a, x), (b, y) in zip(zip(cycles, values), zip(cycles[1:], values[1:]))]
    eligible = [step for step in steps if step["compound_ran_at_all_levels_in_both"]]
    against = [step for step in eligible if step["label"] == "declining"]
    outcomes = {"falls": -1 - tolerance, "stays": 0, "rises": 1 + tolerance}
    forbids = {"conservation": [name for name, change in outcomes.items() if reading(change) != "stable"],
               "conditional": [name for name, change in outcomes.items() if reading(change) == "declining"],
               "reading_rule": [name for name, change in outcomes.items()
                                if reading(change) not in ("stable", "growing", "declining")]}
    check("testable version: the three outcomes of a step are told apart", len({reading(c) for c in outcomes.values()}) == 3)
    return {
        "kind": "synthetic: an imaginary series; no value of p_L exists in the repository",
        "formula": "p_L of a cycle = beliefs_gained - beliefs_lost (cycles_elapsed = 1)",
        "p_l_by_cycle": {str(cycle["cycle"]): value for cycle, value in zip(cycles, values)},
        "steps": steps,
        "versions": cfg["versions"],
        "outcomes_of_a_step_that_each_version_forbids": forbids,
        "conservation": {"steps": len(steps), "steps_where_p_l_changes": sum(s["label"] != "stable" for s in steps),
                         "holds_on_this_series": all(s["label"] == "stable" for s in steps)},
        "conditional": {"steps_between_two_cycles_with_the_compound_phase_at_all_levels": len(eligible),
                        "contradicting_steps": [f"{s['from_cycle']} to {s['to_cycle']}" for s in against],
                        "holds_on_this_series": not against},
        "reading_rule": {"steps": len(steps), "labels": tally([s["label"] for s in steps]),
                         "steps_that_contradict_it": 0, "could_any_series_contradict_it": bool(forbids["reading_rule"])},
    }


def momentum_section(obs: dict, scn: dict) -> dict:
    """The quoted claim, where the repository says it is tracked, what is there, and a synthetic testable version."""
    quotes, tracked = obs["documents"]["quotes"], obs["documents"]["tracking_file"]
    hints = scn["momentum_key_hints"]["fragments"]
    candidates = [key for key in tracked["keys_of_each_entry"] if any(hint in key.lower() for hint in hints)]
    conditions = scn["noether_requirements"]["conditions"]
    return {
        "quoted_from_psy_001": {key: quotes[f"psy_001_{key}"] for key in ("theorem_as_stated", "claim", "formula", "behaviour")},
        "levels_named_by_psy_001": {"count": len(quotes["psy_001_levels"]), "names": quotes["psy_001_levels"]},
        "quoted_from_the_policy": {"tracking": quotes["policy_tracking"],
                                   "conservation_check": {key: quotes[f"policy_check_{key}"]
                                                          for key in ("stable", "growing", "declining")}},
        "tracking_file": tracked | {"hints": hints, "fields_that_could_hold_p_l": candidates,
                                    "values_of_p_l_recorded": len(candidates) * len(tracked["entries"])},
        "what_noether_s_theorem_needs": {"note": scn["noether_requirements"]["note"], "conditions": conditions,
                                         "conditions_stated": len(conditions),
                                         "conditions_met": sum(c["met_in_psy_001"] for c in conditions)},
        "testable_version": testable_version(scn["testable_version"]),
    }


def synthetic_section(scn: dict) -> dict:
    """The five hand-written cases: the audit must return what was written by hand before it ran."""
    folders, cases = scn["folders"]["order"], {}
    for name, case in scn["synthetic_ledgers"]["cases"].items():
        result = audit(folders, case["disk"], case["history"])
        check(f"hand-written case '{name}': the audit returns the answer written in scenarios.json",
              summary(result) == case["expected_by_hand"], f"got {summary(result)}")
        cases[name] = {"description": case["description"]} | summary(result) | {
            "closed_system_holds": result["closed_system"]["holds"], "open_system_holds": result["open_system"]["holds"],
            "every_folder_balances": not result["folders_out_of_balance"],
            "every_item_is_where_the_history_puts_it": not (result["names"]["expected_but_missing"]
                                                              or result["names"]["on_disk_but_unexpected"]
                                                              or result["names_in_two_folders"]),
            "reading": result["reading"]}
    check("hand-written cases: the five cases receive four different readings and only the clean one balances everywhere",
          len({case["reading"] for case in cases.values()}) == 4
          and [n for n, c in cases.items() if c["closed_system_holds"] and c["every_item_is_where_the_history_puts_it"]] == ["clean"])
    return {"kind": "synthetic: eight imaginary events; nothing here is measured in the repository",
            "note": scn["synthetic_ledgers"]["note"], "cases": cases}


def negative_controls(obs: dict, scn: dict, disk: dict, run_ids: list[str], base: dict) -> dict:
    """Plant one error at a time in a copy of the observed data and confirm that the matching check moves."""
    folders, rows = scn["folders"]["order"], obs["history"]["events"]
    lost = {folder: list(names) for folder, names in disk.items()}
    dropped = lost["archived"].pop()
    after_loss = audit(folders, lost, rows)
    check("negative control: a file dropped from the archive listing unbalances that folder and is named as missing",
          after_loss["folders_out_of_balance"] == ["archived"] and not after_loss["open_system"]["holds"]
          and after_loss["names"]["expected_but_missing"] == [f"archived/{dropped}"])
    copied = {folder: list(names) for folder, names in disk.items()}
    copied["archived"].append(copied["top"][0])
    after_copy = audit(folders, copied, rows)
    check("negative control: a pending file copied into the archive listing is seen in two folders",
          after_copy["names_in_two_folders"] == [disk["top"][0]] and not base["names_in_two_folders"])
    repeated = run_ids[:-1] + run_ids[:1]
    check("negative control: a repeated run id is counted", len(repeated) - len(set(repeated)) == 1
          and len(run_ids) == len(set(run_ids)))
    target = next(i for i, row in enumerate(rows) if row.split(" ")[-1].startswith("-"))
    erased = rows[:target] + [rows[target].rsplit(" ", 1)[0]] + rows[target + 1:]
    after_erasure = audit(folders, disk, erased)
    check("negative control: with one deletion record erased from the history, the open-system identity fails",
          base["open_system"]["holds"] and not after_erasure["open_system"]["holds"]
          and after_erasure["removals_recorded"] == base["removals_recorded"] - 1)
    return {
        "note": "Each control changes a copy of the observed snapshot in one place; the observed results are untouched.",
        "file_dropped_from_the_archive_listing": {
            "file": dropped, "archived_difference_before_and_after": [base["flows"]["archived"]["difference"],
                                                                      after_loss["flows"]["archived"]["difference"]],
            "open_system_difference_before_and_after": [base["open_system"]["difference"],
                                                        after_loss["open_system"]["difference"]],
            "expected_but_missing_after": after_loss["names"]["expected_but_missing"], "reading_after": after_loss["reading"]},
        "pending_file_copied_into_the_archive_listing": {
            "file": disk["top"][0], "names_in_two_folders_before_and_after": [len(base["names_in_two_folders"]),
                                                                              len(after_copy["names_in_two_folders"])],
            "reading_after": after_copy["reading"]},
        "run_id_repeated": {"run_ids_seen_twice_before_and_after": [len(run_ids) - len(set(run_ids)),
                                                                    len(repeated) - len(set(repeated))]},
        "deletion_record_erased_from_the_history": {
            "row_before": rows[target], "row_after": erased[target],
            "removals_recorded_before_and_after": [base["removals_recorded"], after_erasure["removals_recorded"]],
            "open_system_difference_before_and_after": [base["open_system"]["difference"],
                                                        after_erasure["open_system"]["difference"]],
            "folders_out_of_balance_after": after_erasure["folders_out_of_balance"], "reading_after": after_erasure["reading"]},
    }


def worked_examples(scn: dict, files: dict, history: dict, claims: dict, momentum: dict, synthetic: dict) -> dict:
    """The numbers the five exercises use, gathered so that each answer can be checked against one place."""
    labels, (top, middle, last) = scn["folders"]["labels"], scn["folders"]["order"]
    stated, by_type = files["stated_counts"], files["by_type_and_folder"]["by_type"]
    statement = {row["id"]: {"statement": row["statement"], "kind": row["kind"]} for row in claims["claims"]}
    fates, use, moves = history["fates"], history["consumption"], history["moves"]
    leaving = {"moved_to_processing": moves[f"{top}>{middle}"], "moved_to_the_archive": moves[f"{top}>{last}"],
               "deleted_outright": history["removed_by_folder"][labels[top]]}
    check("worked example 3: the deletions from the pending folder are the moves out of it and the outright deletions",
          sum(leaving.values()) == history["flows"][labels[top]]["deleted"])
    columns = {name: [case["closed_system_difference"], case["open_system_difference"],
                      len(case["folders_out_of_balance"]),
                      len(case["expected_but_missing"]) + len(case["on_disk_but_unexpected"])]
               for name, case in synthetic["cases"].items()}
    version = momentum["testable_version"]
    return {
        "exercise_1": {"event_files": files["event_files"],
                       "totals_by_type": {kind: line["total"] for kind, line in by_type.items()},
                       "sum_of_the_totals_by_type": sum(line["total"] for line in by_type.values()),
                       "archived_by_type": {kind: line[labels[last]] for kind, line in by_type.items()},
                       "sum_of_the_archived_by_type": sum(line[labels[last]] for line in by_type.values()),
                       "archived_count_stated_by_two_documents": [stated["orphans_stated_by_the_workflow_file"],
                                                                  stated["orphaned_triggers_stated_by_the_skill_file"]]},
        "exercise_2": {"statements": {letter: statement[cid] for letter, cid in zip("abcd", ("C3", "C10", "C1", "C12"))},
                       "run_ids": files["run_ids"]},
        "exercise_3": {"deleted_from_pending": history["flows"][labels[top]]["deleted"], "made_of": leaving,
                       "deleted_outright_by_commit": [group["count"] for group in history["removals"]
                                                      if group["deleted_from"] == top],
                       "created": fates["created"], "on_disk_total": files["event_files"]["total"],
                       "closed_system_difference": fates["created"] - files["event_files"]["total"],
                       "archived_percent_of_created": history["fates_percent_of_created"][labels[last]]},
        "exercise_4": {"columns": ["created minus listed", "the same minus the removals on record",
                                   "folders out of balance", "items missing or unexpected"],
                       "by_case": columns,
                       "cases_whose_first_three_columns_are_zero": [name for name, row in columns.items()
                                                                    if row[:3] == [0, 0, 0]],
                       "readings": {name: case["reading"] for name, case in synthetic["cases"].items()}},
        "exercise_5": {"p_l_by_cycle": version["p_l_by_cycle"],
                       "labels_of_the_steps": [step["label"] for step in version["steps"]],
                       "steps_where_p_l_changes": version["conservation"]["steps_where_p_l_changes"],
                       "eligible_steps": [f"{step['from_cycle']} to {step['to_cycle']}" for step in version["steps"]
                                          if step["compound_ran_at_all_levels_in_both"]],
                       "contradicting_steps": version["conditional"]["contradicting_steps"],
                       "outcomes_forbidden": {name: len(outcomes) for name, outcomes
                                              in version["outcomes_of_a_step_that_each_version_forbids"].items()}},
        "orphans": {"stated": use["orphans_stated_by_the_workflow_file"], "never_consumed": use["never_consumed"],
                    "never_consumed_written_by_the_producer": use["created_by_the_producer_never_consumed"],
                    "made_of": {"archived": fates["archived"], "pending": fates["pending"],
                                "removed_without_being_consumed": fates["removed"] - use["consumed"]}},
    }


def transfer_task(scn: dict) -> dict:
    """Expected answers of the learner task: the same audit on a hypothetical parcel depot."""
    task = scn["transfer_task"]
    folders, result = task["folders"], audit(task["folders"], task["disk"], task["history"])
    flows = result["flows"]
    check("transfer task: the open-system identity holds although two places are out of balance",
          result["open_system"]["holds"] and len(result["folders_out_of_balance"]) == 2)
    return {
        "note": task["note"],
        "q1_flows": {folder: {key: flows[folder][key] for key in ("added", "deleted", "added_minus_deleted")}
                     for folder in folders},
        "q2_totals": {"registered": result["created"], "counted_this_morning": result["files_on_disk"],
                      "closed_system_difference": result["closed_system"]["difference"],
                      "closed_system_holds": result["closed_system"]["holds"],
                      "departures_on_record": result["removals_recorded"],
                      "open_system_difference": result["open_system"]["difference"],
                      "open_system_holds": result["open_system"]["holds"]},
        "q3_places": {folder: {"expected": flows[folder]["added_minus_deleted"], "counted": flows[folder]["on_disk"],
                               "difference": flows[folder]["difference"]} for folder in folders}
                     | {"places_out_of_balance": result["folders_out_of_balance"]},
        "q4_items": {"expected_but_missing": result["names"]["expected_but_missing"],
                     "counted_but_unexpected": result["names"]["on_disk_but_unexpected"],
                     "counted_in_two_places": result["names_in_two_folders"], "reading": result["reading"]},
        "q5": {"statement": task["statement_to_label"], "kind": "analogy", "criterion": scn["claim_kinds"]["analogy"],
               "has_a_single_answer": False},
    }


def strip_private(value):
    if isinstance(value, dict):
        return {key: strip_private(item) for key, item in value.items() if not key.startswith("_")}
    if isinstance(value, list):
        return [strip_private(item) for item in value]
    return value


def analyze(obs: dict, scn: dict) -> dict:
    if scn["rounding"] != {"percent_decimals": PERCENT_DECIMALS}:
        raise ValueError("scenarios.json rounding does not match analyze.py")
    if obs["source"]["commit"] is None:
        raise ValueError("observed-input.json was written with --allow-drift: it is not the pinned snapshot")
    folders = scn["folders"]["order"]
    disk, run_ids = listing(obs["files"], folders)
    result = audit(folders, disk, obs["history"]["events"])
    check("observed history: no record deletes a file from a folder it is not in, or adds one where it already is",
          result["inconsistent_records"] == 0)
    files = files_section(obs, scn, disk, run_ids)
    history = history_section(obs, scn, result)
    claims = claims_section(scn, files, history, result)
    momentum = momentum_section(obs, scn)
    synthetic = synthetic_section(scn)
    controls = negative_controls(obs, scn, disk, run_ids, result)
    worked = worked_examples(scn, files, history, claims, momentum, synthetic)
    transfer = transfer_task(scn)
    return strip_private({
        "module_id": scn["module_id"],
        "rounding": "percentages to 2 decimals; everything else is a count",
        "source": {"repository": obs["source"]["repository"], "commit": obs["source"]["commit"],
                   "files": obs["files"]["source"], "history": obs["history"]["source"],
                   "documents": [entry["path"] for entry in obs["documents"]["files"]]},
        "files_at_the_pin": files,
        "history_to_the_pin": history,
        "audit_of_the_observed_log": {key: result[key] for key in (
            "file_names_in_the_history", "created", "copies_recorded", "removals_recorded", "inconsistent_records",
            "files_on_disk", "distinct_names_on_disk", "names_in_two_folders", "folders_out_of_balance",
            "closed_system", "open_system", "names", "reading")} | {
            "why_the_balances_hold": "The per-folder balances, the name-by-name match and the open-system identity "
                                     "compare " + TELESCOPING + ". They confirm that the history was read completely "
                                     "and correctly; they are not evidence about the trigger system. The closed-system "
                                     "identity is: it compares what ever existed with what exists now."},
        "claims": claims,
        "learning_momentum": momentum,
        "synthetic_controls": synthetic,
        "negative_controls": controls,
        "worked_examples": worked,
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
    except (AssertionError, KeyError, ValueError, OSError) as exc:
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
