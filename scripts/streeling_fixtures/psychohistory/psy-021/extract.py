#!/usr/bin/env python3
"""PSY-021 extract: the trigger folders at the pin, their Git history, and the sentences the lesson quotes.

Three kinds of source, kept apart in observed-input.json:

  files      every file under state/triggers/ in the working tree, pinned as a
             whole by the Git tree id of that folder (and, for archived/, by
             the manifest digest that PSY-008 and PSY-009 also use);
  history    the add and delete records of state/triggers/ along the
             first-parent chain of the pinned commit, read with git log.
             Commits and trees only: no file content of an old commit is read;
  documents  five pinned files from which single sentences or keys are quoted.

The analysis script reads only the snapshot, so its results do not move when
trigger files are added, archived or removed later.

Fails with a non-zero exit and a message when a file or folder is missing or
has an unexpected shape, when the folder is not the one of the pinned commit,
when a quoted file is not its pinned Git blob, when git is missing, when the
pinned commit does not resolve, or when the history is shallow or has another
number of commits than the pin.

Run from the repository root:
    python -I -B scripts/streeling_fixtures/psychohistory/psy-021/extract.py
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

# This program lives under scripts/ (CONTRIBUTING.md: no executable code outside scripts/); its data stays
# under state/streeling/fixtures/. FIXTURE_FILE is the path the program would have next to that data.
FIXTURE_FILE = (Path(__file__).resolve().parents[4]
                / "state/streeling/fixtures/psychohistory/psy-021" / Path(__file__).name)

PINNED_COMMIT = "4b03838800dcd4894f1e026461979bff1d985ca8"
TRIGGERS = "state/triggers"
FOLDERS = {"top": TRIGGERS, "processing": TRIGGERS + "/processing", "archived": TRIGGERS + "/archived"}
# Values at PINNED_COMMIT. One tree id pins the whole folder, sub-folders included:
#   git ls-tree <pin> state/            -> the tree id of state/triggers
#   git ls-tree <pin> state/triggers/   -> the tree ids of archived and processing
# The manifest digest of archived/ is the one shared with PSY-008 and PSY-009:
#   git ls-tree -r <pin> -- state/triggers/archived | awk '{print $3" "$4}' | sha256sum
PINNED_TREES = {
    "top": "730a511ffc201099dde488f8d42efbd12cc92387",
    "processing": "d564d0bc3dd917926892c55e3706cc116d5b165e",
    "archived": "2da37c16496d39c0c9137897c8be2b0c6d6b7978",
}
PINNED_ARCHIVED_FILES = 594
PINNED_ARCHIVED_MANIFEST_SHA256 = "3e33b3e795b977277c52c99d59c48f15ae60f95d28f5524c641d3ec066f10393"
# History at PINNED_COMMIT: git rev-list --count <pin>; the same with --first-parent;
# and with --first-parent <pin> -- state/triggers/.
PINNED_HISTORY = {"commits_reachable_from_the_pin": 1599, "commits_on_the_first_parent_chain": 1528,
                  "commits_read": 623}

# The five quoted files with their Git blob ids at PINNED_COMMIT (git ls-tree <pin> <path>).
LESSON_001 = "state/streeling/courses/psychohistory/en/psy-001-intro-fractal-compounding.md"
POLICY = "policies/compounding-metrics-policy.yaml"
HEALTH = "state/driver/health-scores.json"
WORKFLOW = ".github/workflows/demerzel-driver-triggers.yml"
SKILL = ".claude/skills/demerzel-drive/SKILL.md"
PINNED_BLOBS = {
    LESSON_001: "e7a8aeb2accc287595829ed672a9d65284c38ffc",
    POLICY: "24563e01d0d49909c9b6a41ac51c67a6a6117e48",
    HEALTH: "60038905bb9f52f592c8022cb33c3d3dd26886b7",
    WORKFLOW: "e8406b8fd106cf69f64061e25d51c7c5f57d9581",
    SKILL: "4bab3d1e3f34ab525c3710ba3e02a94e7cf3a131",
}
GOVERNED = (POLICY, SKILL)  # written with spaced slashes in the snapshot: see label()
# What is read from them: (key, file, pattern with one group). Every pattern must match exactly once.
QUOTES = [
    ("psy_001_theorem_as_stated", LESSON_001,
     r"we learn \*\*Noether's theorem\*\*: (every continuous symmetry of a system has a corresponding conserved quantity)\.$"),
    ("psy_001_claim", LESSON_001,
     r"^(In fractal compounding, the symmetry is \*\*scale invariance\*\* — the compound operation has the same shape "
     r"at every level\. The conserved quantity is \*\*learning momentum \(p_L\)\*\*):$"),
    ("psy_001_formula", LESSON_001, r"^(p_L = \(beliefs_gained_T - beliefs_lost_T\) / cycles_elapsed)$"),
    ("psy_001_behaviour", LESSON_001,
     r"^(If your compounding process is consistent \(symmetric across scales\), p_L stays constant or grows\.) "),
    ("policy_tracking", POLICY, r'^  tracking: "(state/driver/health-scores\.json trend fields)"$'),
    ("policy_check_stable", POLICY, r'^    stable: "(p_L constant across 3 cycles — symmetry preserved)"$'),
    ("policy_check_growing", POLICY, r'^    growing: "(p_L increasing — healthy compounding)"$'),
    ("policy_check_declining", POLICY, r'^    declining: "(p_L decreasing — symmetry broken; investigate root cause)"$'),
    ("workflow_retired_on", WORKFLOW, r"^# RETIRED (\d{4}-\d{2}-\d{2}) — producer for the autonomous driver"),
    ("workflow_orphans_stated", WORKFLOW, r"^# accumulated (\d+) orphans \(now under state/triggers/archived/\)\."),
    ("skill_manual_cycles_stated", SKILL, r"ran (\d+) manual cycles in March 2026 and was never$"),
    ("skill_orphans_stated", SKILL, r"its (\d+) orphaned triggers archived under `state/triggers/archived/`"),
    ("skill_consumption_rule", SKILL,
     r"^(On WAKE: move triggers to `state/triggers/processing/` before reading, delete after processing\.) "),
]
LEVEL_ROW = r"^\| (\d) \| (\w+) \| .+ \|$"  # the rows of PSY-001's table of compounding levels

EVENT_NAME = re.compile(r"^(\d{4}-\d{2}-\d{2}T\d{2}-\d{2}-\d{2}Z)-([a-z_-]+)\.trigger\.json$")
HISTORY_EVENT_NAME = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}[-:]\d{2}[-:]\d{2}Z-[a-z_-]+\.trigger\.json$")
OTHER_FILES = {"top": [".gitkeep", "scheduled-research-team.trigger.json"], "processing": [".gitkeep"], "archived": []}
SUFFIX = ".trigger.json"
TIMESTAMP = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")
WORKFLOW_KEYS = ["details", "priority", "ref", "repo", "timestamp", "type"]
WORKFLOW_DETAIL_KEYS = ["event", "run_id", "sender"]
PRODUCER_SUBJECT = r"^trigger: ([a-z_]+) from \S+( \[skip ci\])?$"
LOG_FORMAT = "%x00%H%x09%ct%x09%P%x09%s"
GIT_COMMANDS = {
    "pin_resolves": ["rev-parse", "--verify", "--quiet", PINNED_COMMIT + "^{commit}"],
    "is_shallow": ["rev-parse", "--is-shallow-repository"],
    "commits_reachable_from_the_pin": ["rev-list", "--count", PINNED_COMMIT],
    "commits_on_the_first_parent_chain": ["rev-list", "--count", "--first-parent", PINNED_COMMIT],
    "records": ["-c", "core.quotepath=off", "log", "--first-parent", "-m", "--no-renames", "--no-show-signature",
                "--name-status", "--format=" + LOG_FORMAT, PINNED_COMMIT, "--", TRIGGERS + "/"],
    "paths_ever_added_in_any_ancestor": ["-c", "core.quotepath=off", "log", "--full-history", "-m", "--no-renames",
                                         "--no-show-signature", "--diff-filter=A", "--name-only", "--format=",
                                         PINNED_COMMIT, "--", TRIGGERS + "/"],
}


class ExtractError(Exception):
    """A source is missing, malformed, or not the one of the pinned commit."""


def label(path: str) -> str:
    """A governed file's path as a data label: a space on each side of every slash.

    scripts/evolution_metrics.py counts every tracked file that contains a governed artifact's path as a citation of
    it; a data file must not be one. The programs and the lesson, which really read the file, name it once.
    """
    return " / ".join(path.split("/")) if path in GOVERNED else path


def git_blob_id(data: bytes) -> str:
    """Blob id Git stores for this content once CRLF is normalised to LF."""
    data = data.replace(b"\r\n", b"\n")
    return hashlib.sha1(b"blob %d\x00" % len(data) + data).hexdigest()


def git_tree_id(entries: list[tuple[str, str, str]]) -> str:
    """Tree id of a folder from (mode, name, object id); Git sorts a sub-folder as if its name ended with '/'."""
    ordered = sorted(entries, key=lambda e: (e[1] + ("/" if e[0] == "40000" else "")).encode("utf-8"))
    body = b"".join(f"{mode} {name}".encode("utf-8") + b"\x00" + bytes.fromhex(oid) for mode, name, oid in ordered)
    return hashlib.sha1(b"tree %d\x00" % len(body) + body).hexdigest()


def manifest_sha256(folder: str, blobs: list[tuple[str, str]]) -> str:
    """SHA-256 of the lines '<blob id> <repository path>' sorted by path bytes."""
    lines = sorted((f"{folder}/{name}".encode("utf-8"), blob.encode("ascii")) for name, blob in blobs)
    return hashlib.sha256(b"".join(blob + b" " + path + b"\n" for path, blob in lines)).hexdigest()


def load_json(data: bytes, where: str) -> dict:
    try:
        record = json.loads(data.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ExtractError(f"{where}: not UTF-8 JSON ({exc})") from exc
    if not isinstance(record, dict):
        raise ExtractError(f"{where}: not a JSON object")
    return record


def event_row(record: dict, stem: str, where: str) -> dict:
    """One event file: its row '<file name without .trigger.json> <run id or ->' and its shape."""
    for key in ("type", "timestamp"):
        if not isinstance(record.get(key), str) or not record[key]:
            raise ExtractError(f"{where}: {key} is not a non-empty string")
    if not TIMESTAMP.match(record["timestamp"]) or not isinstance(record.get("details"), dict):
        raise ExtractError(f"{where}: unexpected timestamp or details")
    datetime.strptime(record["timestamp"], "%Y-%m-%dT%H:%M:%SZ")
    details = record["details"]
    expected = record["timestamp"].replace(":", "-") + "-" + record["type"]
    if stem.replace("-", "_") != expected.replace("-", "_"):
        raise ExtractError(f"{where}: the file name does not carry the JSON timestamp and type")
    run_id = details.get("run_id", "-")
    if not isinstance(run_id, str) or not re.match(r"^(\d+|-)$", run_id):
        raise ExtractError(f"{where}: unexpected run_id {run_id!r}")
    return {"row": f"{stem} {run_id}", "keys": sorted(record), "details_keys": sorted(details),
            "name_equals_json": stem == expected, "json_type": record["type"]}


def read_folder(root: Path, key: str) -> dict:
    """Every file of one trigger folder: event rows, other files, and the entries its Git tree id is built from."""
    folder = root / FOLDERS[key]
    if not folder.is_dir():
        raise ExtractError(f"missing directory: {FOLDERS[key]}")
    events, others, entries = [], [], []
    for path in sorted(folder.iterdir(), key=lambda p: p.name.encode("utf-8")):
        where = f"{FOLDERS[key]}/{path.name}"
        if path.is_dir():
            if key != "top" or path.name not in ("processing", "archived"):
                raise ExtractError(f"{where}: unexpected sub-folder")
            continue
        data = path.read_bytes()
        entries.append(("100644", path.name, git_blob_id(data)))
        name = EVENT_NAME.match(path.name)
        if name:
            events.append(event_row(load_json(data, where), path.name[:-len(SUFFIX)], where) | {"file": path.name})
        elif path.name in OTHER_FILES[key]:
            keys = sorted(load_json(data, where)) if path.name.endswith(".json") else None
            if keys is not None and ("type" in keys or "timestamp" in keys):
                raise ExtractError(f"{where}: carries an event's keys under a name that is not an event's")
            others.append({"file": path.name, "bytes": len(data.replace(b"\r\n", b"\n")), "keys": keys})
        else:
            raise ExtractError(f"{where}: unexpected file name")
    return {"events": events, "others": others, "entries": entries}


def read_files(root: Path) -> tuple[dict, list[str]]:
    """The three folders, their tree ids and manifest digest, and what differs from the pinned commit."""
    folders = {key: read_folder(root, key) for key in ("processing", "archived", "top")}
    trees = {key: git_tree_id(folders[key]["entries"]) for key in ("processing", "archived")}
    trees["top"] = git_tree_id(folders["top"]["entries"] + [("40000", key, trees[key]) for key in ("processing", "archived")])
    manifest = manifest_sha256(FOLDERS["archived"], [(name, blob) for _, name, blob in folders["archived"]["entries"]])
    drift = [f"{FOLDERS[key]}: Git tree id {trees[key]}, pinned {PINNED_TREES[key]}"
             for key in ("top", "processing", "archived") if trees[key] != PINNED_TREES[key]]
    if len(folders["archived"]["entries"]) != PINNED_ARCHIVED_FILES:
        drift.append(f"{FOLDERS['archived']}: {len(folders['archived']['entries'])} files, pinned {PINNED_ARCHIVED_FILES}")
    if manifest != PINNED_ARCHIVED_MANIFEST_SHA256:
        drift.append(f"{FOLDERS['archived']}: manifest SHA-256 {manifest}, pinned {PINNED_ARCHIVED_MANIFEST_SHA256}")
    return {"folders": folders, "trees": trees, "manifest": manifest}, drift


def shapes(folders: dict) -> list[dict]:
    """The distinct key sets of the event files, with the number of files that have each."""
    found: dict[str, dict] = {}
    for key in ("top", "processing", "archived"):
        for event in folders[key]["events"]:
            signature = json.dumps([event["keys"], event["details_keys"]])
            entry = found.setdefault(signature, {"files": 0, "keys": event["keys"], "details_keys": event["details_keys"],
                                                 "by_folder": {}, "first_file": f"{key}/{event['file']}"})
            entry["files"] += 1
            entry["by_folder"][key] = entry["by_folder"].get(key, 0) + 1
    ordered = sorted(found.values(), key=lambda entry: (-entry["files"], entry["first_file"]))
    for entry in ordered:
        entry["is_the_workflow_shape"] = (entry["keys"], entry["details_keys"]) == (WORKFLOW_KEYS, WORKFLOW_DETAIL_KEYS)
    return ordered


def files_section(read: dict) -> dict:
    folders = read["folders"]
    events = [event for key in ("top", "processing", "archived") for event in folders[key]["events"]]
    return {
        "source": "the working tree, verified against the pinned commit by the three Git tree ids below",
        "git_tree_ids": {FOLDERS[key]: read["trees"][key] for key in ("top", "processing", "archived")},
        "git_tree_id_rule": "sha1 of the Git tree object rebuilt from the entries of the folder: every file as mode "
                            "100644 with blob id sha1(b'blob <size>\\0' + bytes), CRLF normalised to LF, and the two "
                            "sub-folders of state/triggers as mode 40000 with their own tree ids",
        "git_tree_id_commands": [f"git ls-tree {PINNED_COMMIT} state/", f"git ls-tree {PINNED_COMMIT} state/triggers/"],
        "archived_files": len(folders["archived"]["entries"]),
        "archived_manifest_sha256": read["manifest"],
        "archived_manifest_command": f"git ls-tree -r {PINNED_COMMIT} -- {FOLDERS['archived']} | "
                                     "awk '{print $3\" \"$4}' | sha256sum",
        "event_files": {key: [event["row"] for event in folders[key]["events"]] for key in ("top", "processing", "archived")},
        "other_files": {key: folders[key]["others"] for key in ("top", "processing", "archived")},
        "shapes": shapes(folders),
        "name_checks": {
            "event_files": len(events),
            "file_name_equals_json_timestamp_and_type": sum(event["name_equals_json"] for event in events),
            "file_name_equals_them_once_hyphens_and_underscores_are_treated_alike": len(events),
            "exceptions": [{"file": event["file"], "json_type": event["json_type"]}
                           for event in events if not event["name_equals_json"]],
        },
    }


def read_documents(root: Path) -> tuple[dict, list[str]]:
    """Sentences and keys quoted from the five pinned files, and what differs from the pinned commit."""
    texts, files, drift = {}, [], []
    for rel, pinned in PINNED_BLOBS.items():
        path = root / rel
        if not path.is_file():
            raise ExtractError(f"missing file: {rel}")
        data = path.read_bytes()
        try:
            texts[rel] = data.decode("utf-8").replace("\r\n", "\n")
        except UnicodeDecodeError as exc:
            raise ExtractError(f"{rel}: not UTF-8 ({exc})") from exc
        blob = git_blob_id(data)
        files.append({"path": label(rel), "git_blob": blob})
        if blob != pinned:
            drift.append(f"{rel} is blob {blob}, pinned {pinned}")
    quotes: dict = {}
    for key, rel, pattern in QUOTES:
        found = re.findall(pattern, texts[rel], flags=re.MULTILINE)
        if len(found) != 1:
            raise ExtractError(f"{rel}: expected one match for {key}, found {len(found)}")
        quotes[key] = int(found[0]) if found[0].isdigit() else found[0]
    levels = re.findall(LEVEL_ROW, texts[LESSON_001], flags=re.MULTILINE)
    if [int(number) for number, _ in levels] != list(range(len(levels))) or not levels:
        raise ExtractError(f"{LESSON_001}: the table of compounding levels has an unexpected shape")
    quotes["psy_001_levels"] = [name for _, name in levels]
    health = load_json(texts[HEALTH].encode("utf-8"), HEALTH)
    if not all(isinstance(entry, dict) for entry in health.values()):
        raise ExtractError(f"{HEALTH}: an entry is not an object")
    tracked = {"entries": sorted(health), "keys_of_each_entry": sorted({key for entry in health.values() for key in entry}),
               "trend_values": sorted({str(entry.get("trend")) for entry in health.values()}),
               "numeric_fields": sorted({key for entry in health.values() for key, value in entry.items()
                                         if isinstance(value, (int, float)) and not isinstance(value, bool)})}
    return {"files": files, "quotes": quotes, "tracking_file": tracked}, drift


def git(root: Path, args: list[str]) -> str:
    """Run one git command (argument list, no shell, no download of missing objects) and return its output."""
    env = dict(os.environ, GIT_TERMINAL_PROMPT="0", GIT_NO_LAZY_FETCH="1")
    try:
        done = subprocess.run(["git", "-C", str(root), *args], capture_output=True, check=False, env=env, timeout=120)
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise ExtractError(f"cannot run git {args[0]}: {exc}") from exc
    if done.returncode != 0:
        detail = done.stderr.decode("utf-8", "replace").strip() or f"exit {done.returncode}"
        raise ExtractError(f"git {' '.join(args)} failed: {detail}")
    return done.stdout.decode("utf-8")


def split_path(path: str) -> tuple[str, str]:
    """state/triggers/<name> -> ('top', name); state/triggers/<folder>/<name> -> (folder, name)."""
    if not path.startswith(TRIGGERS + "/"):
        raise ExtractError(f"history: a record outside {TRIGGERS}: {path}")
    parts = path[len(TRIGGERS) + 1:].split("/")
    if len(parts) == 1:
        return "top", parts[0]
    if len(parts) != 2 or parts[0] not in ("processing", "archived"):
        raise ExtractError(f"history: unexpected path {path}")
    return parts[0], parts[1]


def read_log(root: Path) -> list[dict]:
    """The commits of the first-parent chain that touch state/triggers/, oldest first, with their A and D records."""
    commits = []
    for chunk in git(root, GIT_COMMANDS["records"]).split("\x00")[1:]:
        head, _, body = chunk.partition("\n")
        commit, seconds, parents, subject = head.split("\t", 3)
        records = []
        for line in body.split("\n"):
            if not line.strip():
                continue
            status, _, path = line.partition("\t")
            if status not in ("A", "D"):
                raise ExtractError(f"history: commit {commit[:10]} has a record of status {status!r} ({path})")
            records.append((status, *split_path(path)))
        if not records:
            raise ExtractError(f"history: commit {commit[:10]} has no record")
        commits.append({"commit": commit, "seconds": int(seconds), "parents": len(parents.split()),
                        "subject": subject, "records": records})
    if len({entry["commit"] for entry in commits}) != len(commits):
        raise ExtractError("history: git listed a commit twice (a merge compared with more than its first parent)")
    commits.reverse()
    return commits


def history_rows(commits: list[dict]) -> tuple[list[str], list[str]]:
    """One row per file name, in order of first appearance: '<name> <record> <record> ...'.

    A record is +<folder>@<n> (added) or -<folder>@<n> (deleted), n being the commit's position in the list (from 1).
    Within one commit the deletions come first. Event names lose their .trigger.json suffix; other names keep theirs.
    """
    by_name: dict[str, list[str]] = {}
    for number, entry in enumerate(commits, 1):
        for status in ("D", "A"):
            for found, folder, name in entry["records"]:
                if found == status:
                    by_name.setdefault(name, []).append(("-" if status == "D" else "+") + f"{folder}@{number}")
    events = [f"{name[:-len(SUFFIX)]} {' '.join(records)}" for name, records in by_name.items()
              if HISTORY_EVENT_NAME.match(name)]
    others = [f"{name} {' '.join(records)}" for name, records in by_name.items() if not HISTORY_EVENT_NAME.match(name)]
    return events, others


def commit_tables(commits: list[dict]) -> tuple[dict, list[dict]]:
    """Producer commits by the type their subject names, and the full detail of every other commit."""
    producers: dict[str, list[int]] = {}
    others = []
    for number, entry in enumerate(commits, 1):
        subject = re.match(PRODUCER_SUBJECT, entry["subject"])
        if subject:
            producers.setdefault(subject.group(1), []).append(number)
            continue
        when = datetime.fromtimestamp(entry["seconds"], timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        others.append({"n": number, "commit": entry["commit"], "committed_utc": when, "parents": entry["parents"],
                       "subject": entry["subject"],
                       "records": {status: sum(found == status for found, _, _ in entry["records"]) for status in "AD"}})
    return {kind: producers[kind] for kind in sorted(producers)}, others


def read_history(root: Path) -> tuple[dict, list[str]]:
    """The add and delete records of the trigger folders, and what differs from the pinned history."""
    try:
        git(root, GIT_COMMANDS["pin_resolves"])
    except ExtractError as exc:
        raise ExtractError(f"the pinned commit {PINNED_COMMIT} is not in this clone ({exc})") from exc
    if git(root, GIT_COMMANDS["is_shallow"]).strip() != "false":
        raise ExtractError("this clone is shallow: the history of state/triggers/ cannot be read (git fetch --unshallow)")
    commits = read_log(root)
    counts = {key: int(git(root, GIT_COMMANDS[key]).strip())
              for key in ("commits_reachable_from_the_pin", "commits_on_the_first_parent_chain")}
    counts["commits_read"] = len(commits)
    drift = [f"history: {key} is {counts[key]}, pinned {value}" for key, value in PINNED_HISTORY.items()
             if counts[key] != value]
    raw = {status: {} for status in "AD"}
    for entry in commits:
        for status, folder, _ in entry["records"]:
            raw[status][folder] = raw[status].get(folder, 0) + 1
    on_chain = {f"{FOLDERS[folder]}/{name}" for entry in commits for status, folder, name in entry["records"] if status == "A"}
    anywhere = {line for line in git(root, GIT_COMMANDS["paths_ever_added_in_any_ancestor"]).split("\n") if line.strip()}
    events, others = history_rows(commits)
    producers, other_commits = commit_tables(commits)
    return {
        "source": "git log at the pinned commit: commits and trees only, no file content of an old commit",
        "commands": {key: "git " + " ".join(args) for key, args in GIT_COMMANDS.items()},
        **counts,
        "first_parent_chain": "the commits reached from the pin by following each commit's first parent: the successive "
                              "states of the main branch. A merge appears once, compared with its first parent.",
        "raw_records": raw,
        "paths_ever_added": {"on_the_first_parent_chain": len(on_chain), "in_any_ancestor_of_the_pin": len(anywhere),
                             "only_outside_the_first_parent_chain": sorted(anywhere - on_chain)},
        "producer_subject_pattern": PRODUCER_SUBJECT,
        "producer_commits": producers,
        "other_commits": other_commits,
        "events": events,
        "other_files": others,
    }, drift


def encoding_section() -> dict:
    return {
        "files.event_files": "per folder, one string per event file in file-name order: '<file name without "
                             ".trigger.json> <details.run_id, or - when the file has none>'",
        "history.events": "one string per event file name that ever existed under state/triggers/ on the first-parent "
                          "chain, in order of first appearance: '<file name without .trigger.json> <record> ...'. A "
                          "record is +<folder>@<n> (added to the folder by commit n) or -<folder>@<n> (deleted from "
                          "it); within one commit the deletions are listed first. Git was told not to pair a "
                          "deletion with an addition (--no-renames), so a move is one of each in the same commit.",
        "history.other_files": "the same for the three files that are not events",
        "history.n": "position of a commit among the commits_read, oldest first, from 1",
        "history.producer_commits": "for each type named by a subject that matches producer_subject_pattern, the n of "
                                    "those commits; every other commit is listed in full under other_commits",
        "folder": "top = state/triggers itself, processing and archived = its two sub-folders",
        "governed_paths": "the paths of the driver's skill file and of the compounding-metrics policy are written "
                          "with a space on each side of every slash, so that this data file is not counted as a "
                          "citation of those two governed artifacts by scripts/evolution_metrics.py",
    }


def build(root: Path, allow_drift: bool) -> dict:
    files, drift = read_files(root)
    documents, document_drift = read_documents(root)
    history, history_drift = read_history(root)
    drift += document_drift + history_drift
    if drift and not allow_drift:
        raise ExtractError(f"the sources are not those of commit {PINNED_COMMIT}:\n  " + "\n  ".join(drift)
                           + "\n(--allow-drift snapshots them anyway; the lesson's numbers then no longer apply)")
    return {
        "schema_version": "0.1.0",
        "module_id": "psy-021-conservation-claims",
        "kind": "observed",
        "source": {
            "repository": "GuitarAlchemist/Demerzel",
            "commit": None if drift else PINNED_COMMIT,
            "commit_check": ("FAILED: " + "; ".join(drift)) if drift else
                            "the trigger folders have the Git tree ids and the manifest digest recorded for this "
                            "commit, the five quoted files have their recorded Git blob ids (CRLF normalised to LF), "
                            "and the history has the recorded numbers of commits",
        },
        "encoding": encoding_section(),
        "files": files_section(files),
        "history": history,
        "documents": documents,
    }


def main() -> int:
    here = FIXTURE_FILE
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--repo-root", type=Path, default=here.parents[5])
    parser.add_argument("--output", type=Path, default=here.with_name("observed-input.json"))
    parser.add_argument("--allow-drift", action="store_true",
                        help="snapshot sources that differ from the pinned commit")
    args = parser.parse_args()
    try:
        snapshot = build(args.repo_root, args.allow_drift)
    except (ExtractError, OSError) as exc:
        print(f"extract.py: {exc}", file=sys.stderr)
        return 1
    text = json.dumps(snapshot, ensure_ascii=False, indent=2) + "\n"
    args.output.write_bytes(text.encode("utf-8"))
    files, history = snapshot["files"], snapshot["history"]
    on_disk = sum(len(rows) for rows in files["event_files"].values())
    print(f"extract.py: {on_disk} event files on disk, {len(history['events'])} event file names in "
          f"{history['commits_read']} commits -> {args.output.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
