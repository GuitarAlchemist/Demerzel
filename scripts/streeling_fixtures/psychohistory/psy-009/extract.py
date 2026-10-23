#!/usr/bin/env python3
"""PSY-009 extract: snapshot the archived trigger log, one row per event.

Reads every file of state/triggers/archived/, and the two files that say what
the triggers were written for (the retired driver's skill file and the
workflow that wrote the triggers), and writes observed-input.json next to
this script. The analysis script reads only that snapshot, so its results do
not move if trigger files are added, archived or removed later.

Fails with a non-zero exit and a message when the folder or a file is
missing, a file has an unexpected name or shape, the folder is not the one of
the pinned commit (file count, Git tree id, manifest digest), or one of the
two design files is not its pinned Git blob.

Run from the repository root:
    python -I scripts/streeling_fixtures/psychohistory/psy-009/extract.py
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

# This program lives under scripts/ (CONTRIBUTING.md: no executable code outside scripts/); its data stays
# under state/streeling/fixtures/. FIXTURE_FILE is the path the program would have next to that data.
FIXTURE_FILE = (Path(__file__).resolve().parents[4]
                / "state/streeling/fixtures/psychohistory/psy-009" / Path(__file__).name)

PINNED_COMMIT = "4b03838800dcd4894f1e026461979bff1d985ca8"
FOLDER = "state/triggers/archived"
# Values at PINNED_COMMIT. The folder holds too many files to pin one blob id
# each, so three values pin it as a whole:
#   the file count;
#   the Git tree id of the folder  (git ls-tree <pin> state/triggers/);
#   the SHA-256 of the lines "<blob id> <path>\n", sorted by path
#   (git ls-tree -r <pin> -- state/triggers/archived | awk '{print $3" "$4}' | sha256sum).
PINNED_FILE_COUNT = 594
PINNED_TREE_ID = "2da37c16496d39c0c9137897c8be2b0c6d6b7978"
PINNED_MANIFEST_SHA256 = "3e33b3e795b977277c52c99d59c48f15ae60f95d28f5524c641d3ec066f10393"

# The two files that describe the consumer the triggers were written for, with
# their Git blob ids at PINNED_COMMIT (git ls-tree <pin> <path>).
SKILL_FILE = ".claude/skills/demerzel-drive/SKILL.md"
WORKFLOW_FILE = ".github/workflows/demerzel-driver-triggers.yml"
PINNED_BLOBS = {
    SKILL_FILE: "4bab3d1e3f34ab525c3710ba3e02a94e7cf3a131",
    WORKFLOW_FILE: "e8406b8fd106cf69f64061e25d51c7c5f57d9581",
}
# What is read from them: (key, file, pattern with one group). Every pattern
# must match exactly once.
DESIGN_PATTERNS = [
    ("queue_depth_max_triggers", SKILL_FILE,
     r"^- Maximum queue depth: \*\*(\d+) triggers\*\* — excess pruned by lowest priority$"),
    ("staleness_hours", SKILL_FILE,
     r"^- Staleness: triggers older than \*\*(\d+) hours\*\* discarded with log entry$"),
    ("deduplication_rule", SKILL_FILE,
     r"^- Deduplication: (same `type` \+ `repo` \+ `ref` → merged, keep most recent)$"),
    ("manual_cycles_run_before_retirement", SKILL_FILE,
     r"ran (\d+) manual cycles in March 2026 and was never\n> scheduled\."),
    ("orphaned_triggers_stated_by_the_skill_file", SKILL_FILE,
     r"its (\d+) orphaned triggers archived under `state/triggers/archived/`"),
    ("workflow_retired_on", WORKFLOW_FILE,
     r"^# RETIRED (\d{4}-\d{2}-\d{2}) — producer for the autonomous driver"),
    ("orphans_stated_by_the_workflow_file", WORKFLOW_FILE,
     r"The driver's consume cycle was never scheduled, so these auto-fired triggers\n# accumulated (\d+) orphans"),
]

FILE_NAME = re.compile(r"^(\d{4}-\d{2}-\d{2}T\d{2}-\d{2}-\d{2}Z)-([a-z_]+)\.trigger\.json$")
TIMESTAMP = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")
TOP_KEYS = {"type", "repo", "ref", "priority", "details", "timestamp"}
DETAIL_KEYS = {"event", "sender", "run_id"}


class ExtractError(Exception):
    """The folder is missing, a file is malformed, or the folder is not the pinned one."""


def git_blob_id(data: bytes) -> str:
    """Blob id Git stores for this content once CRLF is normalised to LF."""
    data = data.replace(b"\r\n", b"\n")
    return hashlib.sha1(b"blob %d\x00" % len(data) + data).hexdigest()


def git_tree_id(entries: list[tuple[str, str]]) -> str:
    """Tree id of a flat folder of regular, non-executable files (mode 100644)."""
    body = b"".join(b"100644 " + name.encode("utf-8") + b"\x00" + bytes.fromhex(blob)
                    for name, blob in sorted(entries, key=lambda entry: entry[0].encode("utf-8")))
    return hashlib.sha1(b"tree %d\x00" % len(body) + body).hexdigest()


def manifest_sha256(entries: list[tuple[str, str]]) -> str:
    """SHA-256 of the lines '<blob id> <repository path>' sorted by path bytes."""
    lines = sorted((f"{FOLDER}/{name}".encode("utf-8"), blob.encode("ascii")) for name, blob in entries)
    return hashlib.sha256(b"".join(blob + b" " + path + b"\n" for path, blob in lines)).hexdigest()


def read_events(root: Path) -> tuple[list[dict], list[tuple[str, str]]]:
    folder = root / FOLDER
    if not folder.is_dir():
        raise ExtractError(f"missing directory: {FOLDER}")
    events, entries = [], []
    for path in sorted(folder.iterdir(), key=lambda p: p.name.encode("utf-8")):
        where = f"{FOLDER}/{path.name}"
        if not path.is_file():
            raise ExtractError(f"{where}: not a regular file")
        name = FILE_NAME.match(path.name)
        if not name:
            raise ExtractError(f"{where}: unexpected file name")
        data = path.read_bytes()
        try:
            record = json.loads(data.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ExtractError(f"{where}: not UTF-8 JSON ({exc})") from exc
        if not isinstance(record, dict) or set(record) != TOP_KEYS:
            raise ExtractError(f"{where}: keys are not {sorted(TOP_KEYS)}")
        details = record["details"]
        if not isinstance(details, dict) or set(details) != DETAIL_KEYS:
            raise ExtractError(f"{where}: details keys are not {sorted(DETAIL_KEYS)}")
        for key in ("type", "repo", "ref", "priority", "timestamp"):
            if not isinstance(record[key], str) or not record[key]:
                raise ExtractError(f"{where}: {key} is not a non-empty string")
        for key in DETAIL_KEYS:
            if not isinstance(details[key], str) or not details[key]:
                raise ExtractError(f"{where}: details.{key} is not a non-empty string")
        timestamp = record["timestamp"]
        if not TIMESTAMP.match(timestamp):
            raise ExtractError(f"{where}: unexpected timestamp {timestamp!r}")
        datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
        if name.group(1) != timestamp.replace(":", "-") or name.group(2) != record["type"]:
            raise ExtractError(f"{where}: the file name does not match the JSON timestamp and type")
        events.append({"timestamp": timestamp, "type": record["type"], "repo": record["repo"], "ref": record["ref"],
                       "sender": details["sender"]})
        entries.append((path.name, git_blob_id(data)))
    if not events:
        raise ExtractError(f"no trigger file in {FOLDER}")
    return events, entries


def read_design(root: Path) -> tuple[dict, list[dict]]:
    """The driver's stated limits and retirement notes, and the blob id of each file read."""
    texts, files = {}, []
    for rel in (SKILL_FILE, WORKFLOW_FILE):
        path = root / rel
        if not path.is_file():
            raise ExtractError(f"missing file: {rel}")
        data = path.read_bytes()
        try:
            texts[rel] = data.decode("utf-8").replace("\r\n", "\n")
        except UnicodeDecodeError as exc:
            raise ExtractError(f"{rel}: not UTF-8 ({exc})") from exc
        files.append({"path": rel, "git_blob": git_blob_id(data)})
    design: dict = {}
    for key, rel, pattern in DESIGN_PATTERNS:
        found = re.findall(pattern, texts[rel], flags=re.MULTILINE)
        if len(found) != 1:
            raise ExtractError(f"{rel}: expected one match for {key}, found {len(found)}")
        design[key] = int(found[0]) if found[0].isdigit() else found[0]
    return design, files


def tally(values: list[str]) -> dict[str, int]:
    return {value: values.count(value) for value in sorted(set(values))}


def spaced(path: str) -> str:
    """A repository path with a space on each side of every slash.

    The repository counts, for each governed file, the tracked files that contain its path as a literal string. A data
    file must not add to that count, so observed-input.json carries the paths of the design files in this form.
    """
    return " / ".join(path.split("/"))


def drift_from_the_pin(pins: dict, design_files: list[dict]) -> list[str]:
    """Every difference between what was read and what PINNED_COMMIT holds; empty when there is none."""
    drift = []
    if pins["files"] != PINNED_FILE_COUNT:
        drift.append(f"{pins['files']} files, pinned {PINNED_FILE_COUNT}")
    if pins["git_tree_id"] != PINNED_TREE_ID:
        drift.append(f"Git tree id {pins['git_tree_id']}, pinned {PINNED_TREE_ID}")
    if pins["manifest_sha256"] != PINNED_MANIFEST_SHA256:
        drift.append(f"manifest SHA-256 {pins['manifest_sha256']}, pinned {PINNED_MANIFEST_SHA256}")
    for entry in design_files:
        if entry["git_blob"] != PINNED_BLOBS[entry["path"]]:
            drift.append(f"{entry['path']} is blob {entry['git_blob']}, pinned {PINNED_BLOBS[entry['path']]}")
    return drift


def calendar_and_counts(events: list[dict]) -> tuple[list[str], list[int]]:
    """Every calendar day from the first event to the last, and the events on each (0 for a day without any)."""
    timestamps = [event["timestamp"] for event in events]
    if timestamps != sorted(timestamps):
        raise ExtractError("events are not in time order when sorted by file name")
    per_day: dict[str, int] = {}
    for timestamp in timestamps:
        per_day[timestamp[:10]] = per_day.get(timestamp[:10], 0) + 1
    first, last = date.fromisoformat(min(per_day)), date.fromisoformat(max(per_day))
    calendar = [(first + timedelta(days=offset)).isoformat() for offset in range((last - first).days + 1)]
    values = [per_day.get(day, 0) for day in calendar]
    if sum(values) != len(events):
        raise ExtractError("daily counts do not sum to the number of events")
    return calendar, values


def source_section(pins: dict, design_files: list[dict], drift: list[str]) -> dict:
    return {
        "repository": "GuitarAlchemist/Demerzel",
        "commit": None if drift else PINNED_COMMIT,
        "commit_check": ("FAILED: " + "; ".join(drift)) if drift else
                        "the folder has the file count, the Git tree id and the manifest digest recorded for this "
                        "commit, and the two design files have their recorded Git blob ids (CRLF normalised to LF)",
        "folder": FOLDER,
        "files": pins["files"],
        "git_tree_id": pins["git_tree_id"],
        "git_tree_id_rule": "sha1 of the Git tree object rebuilt from the file names and blob ids, every file "
                            "taken as mode 100644; blob id = sha1(b'blob <size>\\0' + bytes), CRLF normalised to LF",
        "git_tree_id_command": f"git ls-tree {PINNED_COMMIT} state/triggers/",
        "manifest_sha256": pins["manifest_sha256"],
        "manifest_rule": "SHA-256 of the lines '<blob id> <repository path>\\n', one per file, sorted by path bytes",
        "manifest_command": f"git ls-tree -r {PINNED_COMMIT} -- {FOLDER} | awk '{{print $3\" \"$4}}' | sha256sum",
        "not_read": "state/triggers/ also holds trigger files that were never archived, a file of another shape "
                    "and an empty processing/ folder; this snapshot covers the archived folder only",
        "design_files": [{"path": spaced(entry["path"]), "git_blob": entry["git_blob"]} for entry in design_files],
    }


def counts_section(events: list[dict], calendar: list[str], values: list[int]) -> dict:
    timestamps = [event["timestamp"] for event in events]
    return {
        "events": len(events),
        "first_day": calendar[0],
        "last_day": calendar[-1],
        "calendar_days": len(calendar),
        "active_days": sum(value > 0 for value in values),
        "empty_days": sum(value == 0 for value in values),
        "by_type": tally([event["type"] for event in events]),
        "distinct_timestamps": len(set(timestamps)),
        "distinct_senders": len({event["sender"] for event in events}),
        "distinct_repos": len({event["repo"] for event in events}),
        "distinct_refs": len({event["ref"] for event in events}),
        "distinct_type_repo_ref_combinations": len({(event["type"], event["repo"], event["ref"]) for event in events}),
        "file_names_that_differ_from_the_json_timestamp_or_type": 0,
    }


def build(root: Path, allow_drift: bool) -> dict:
    events, entries = read_events(root)
    design, design_files = read_design(root)
    pins = {"files": len(entries), "git_tree_id": git_tree_id(entries), "manifest_sha256": manifest_sha256(entries)}
    drift = drift_from_the_pin(pins, design_files)
    if drift and not allow_drift:
        raise ExtractError(f"the sources are not those of commit {PINNED_COMMIT}:\n  " + "\n  ".join(drift)
                           + "\n(--allow-drift snapshots it anyway; the lesson's numbers then no longer apply)")
    calendar, values = calendar_and_counts(events)
    return {
        "schema_version": "0.1.0",
        "module_id": "psy-009-concentration-and-heavy-tails",
        "kind": "observed",
        "source": source_section(pins, design_files, drift),
        "encoding": {
            "events": "one string per file, in file-name order, which is time order: '<JSON timestamp> <type>'",
            "day": "the day of an event is the UTC date of its JSON timestamp",
            "daily_counts.values": "events per calendar day from first_day to last_day inclusive, days without events included",
            "design": "numbers and sentences read from the two design files by the patterns in extract.py; they say "
                      "what the repository states about the consumer of these triggers and are not measurements",
            "source.design_files": "the path of each design file is written with a space on each side of every slash "
                                   "(the README says why); remove the spaces to get the repository path",
        },
        "counts": counts_section(events, calendar, values),
        "design": design,
        "daily_counts": {"first_day": calendar[0], "values": values},
        "events": [f"{event['timestamp']} {event['type']}" for event in events],
    }


def main() -> int:
    here = FIXTURE_FILE
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--repo-root", type=Path, default=here.parents[5])
    parser.add_argument("--output", type=Path, default=here.with_name("observed-input.json"))
    parser.add_argument("--allow-drift", action="store_true",
                        help="snapshot a folder that differs from the pinned commit")
    args = parser.parse_args()
    try:
        snapshot = build(args.repo_root, args.allow_drift)
    except (ExtractError, OSError) as exc:
        print(f"extract.py: {exc}", file=sys.stderr)
        return 1
    text = json.dumps(snapshot, ensure_ascii=False, indent=2) + "\n"
    args.output.write_bytes(text.encode("utf-8"))
    counts = snapshot["counts"]
    print(f"extract.py: {counts['events']} events on {counts['calendar_days']} calendar days "
          f"({counts['active_days']} active, {counts['empty_days']} empty) -> {args.output.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
