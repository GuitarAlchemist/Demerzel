#!/usr/bin/env python3
"""PSY-008 extract: snapshot the archived trigger log as one row per event.

Reads every file of state/triggers/archived/ (timestamp and type), the
project's push-triggered-spam pattern record and two workflow files, and
writes observed-input.json next to this script. The analysis script reads
only that snapshot.

Fails with a non-zero exit and a message when a source file is missing, has
an unexpected shape, or is not the file of the pinned commit. The trigger
folder holds 594 files, so it is pinned by one manifest digest and by its Git
tree id, not by 594 embedded blob ids.

Run from the repository root:
    python -I scripts/streeling_fixtures/psychohistory/psy-008/extract.py
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from datetime import date, datetime
from pathlib import Path

# This program lives under scripts/ (CONTRIBUTING.md: no executable code outside scripts/); its data stays
# under state/streeling/fixtures/. FIXTURE_FILE is the path the program would have next to that data.
FIXTURE_FILE = (Path(__file__).resolve().parents[4]
                / "state/streeling/fixtures/psychohistory/psy-008" / Path(__file__).name)

PINNED_COMMIT = "4b03838800dcd4894f1e026461979bff1d985ca8"
TRIGGER_DIR = "state/triggers/archived"
# git ls-tree -r <pin> -- state/triggers/archived | awk '{print $3" "$4}' | sha256sum
# git ls-tree <pin> state/triggers/   (the line of the `archived` tree)
PINNED_FOLDER = {
    "files": 594,
    "git_tree": "2da37c16496d39c0c9137897c8be2b0c6d6b7978",
    "manifest_sha256": "3e33b3e795b977277c52c99d59c48f15ae60f95d28f5524c641d3ec066f10393",
}
PATTERN = "state/patterns/anti-pattern-003-push-triggered-spam.pattern.json"
PRODUCER = ".github/workflows/demerzel-driver-triggers.yml"
SCHEDULED = ".github/workflows/streeling-daily.yml"
# Git blob ids at PINNED_COMMIT (git ls-tree). A blob id is
# sha1(b"blob <size>\0" + content) over the LF-normalised bytes.
PINNED_BLOBS = {
    PATTERN: "c0ac065fffa12ad74353a1d1f2b475a06b6081bc",
    PRODUCER: "e8406b8fd106cf69f64061e25d51c7c5f57d9581",
    SCHEDULED: "45641b43997fb9d615b06e467c4c290593dc9ab4",
}
FILE_NAME = re.compile(r"^(\d{4}-\d{2}-\d{2})T(\d{2})-(\d{2})-(\d{2})Z-([a-z_]+)\.trigger\.json$")
EVENT_KEYS = {"type", "repo", "ref", "priority", "details", "timestamp"}
DETAIL_KEYS = {"event", "sender", "run_id"}
PATTERN_KEYS = ("pattern_id", "name", "description", "detection", "action", "evidence", "occurrence_count",
                "first_seen", "last_seen", "status", "resolution")


class ExtractError(Exception):
    """A source file is missing, malformed, or not the pinned one."""


def git_blob_id(data: bytes) -> str:
    """Blob id Git stores for this content once CRLF is normalised to LF."""
    data = data.replace(b"\r\n", b"\n")
    return hashlib.sha1(b"blob %d\x00" % len(data) + data).hexdigest()


def git_tree_id(entries: list[tuple[str, str]]) -> str:
    """Tree id of a folder that holds only regular, non-executable files."""
    body = b"".join(b"100644 " + name.encode("utf-8") + b"\x00" + bytes.fromhex(blob) for name, blob in entries)
    return hashlib.sha1(b"tree %d\x00" % len(body) + body).hexdigest()


def read_pinned(root: Path, rel: str) -> tuple[str, dict]:
    path = root / rel
    if not path.is_file():
        raise ExtractError(f"missing file: {rel}")
    data = path.read_bytes()
    return data.decode("utf-8"), {"path": rel, "git_blob": git_blob_id(data)}


def read_events(root: Path) -> tuple[list[dict], dict]:
    folder = root / TRIGGER_DIR
    if not folder.is_dir():
        raise ExtractError(f"missing directory: {TRIGGER_DIR}")
    names = sorted((path.name for path in folder.iterdir()), key=lambda name: name.encode("utf-8"))
    if not names:
        raise ExtractError(f"no file in {TRIGGER_DIR}")
    events, entries = [], []
    for name in names:
        where = f"{TRIGGER_DIR}/{name}"
        path = folder / name
        match = FILE_NAME.match(name)
        if not path.is_file() or not match:
            raise ExtractError(f"{where}: not a file named <timestamp>-<type>.trigger.json")
        data = path.read_bytes()
        try:
            event = json.loads(data.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise ExtractError(f"{where}: not UTF-8 JSON ({exc})") from exc
        if not isinstance(event, dict) or set(event) != EVENT_KEYS:
            raise ExtractError(f"{where}: keys differ from {sorted(EVENT_KEYS)}")
        details = event["details"]
        if not isinstance(details, dict) or set(details) != DETAIL_KEYS:
            raise ExtractError(f"{where}: details keys differ from {sorted(DETAIL_KEYS)}")
        values = [event[key] for key in sorted(EVENT_KEYS - {"details"})] + [details[key] for key in sorted(DETAIL_KEYS)]
        if not all(isinstance(value, str) and value for value in values):
            raise ExtractError(f"{where}: a field is not a non-empty string")
        day, hour, minute, second, kind = match.groups()
        stamp = f"{day}T{hour}:{minute}:{second}Z"
        try:
            datetime.strptime(stamp, "%Y-%m-%dT%H:%M:%SZ")
        except ValueError as exc:
            raise ExtractError(f"{where}: file name does not hold a valid time ({exc})") from exc
        if event["timestamp"] != stamp or event["type"] != kind:
            raise ExtractError(f"{where}: JSON timestamp or type ({event['timestamp']}, {event['type']}) "
                               "differs from the file name")
        entries.append((name, git_blob_id(data)))
        events.append({"timestamp": stamp, "type": kind, "repo": event["repo"], "sender": details["sender"],
                       "run_id": details["run_id"]})
    manifest = "".join(f"{blob} {TRIGGER_DIR}/{name}\n" for name, blob in entries)
    folder_ids = {"files": len(entries), "git_tree": git_tree_id(entries),
                  "manifest_sha256": hashlib.sha256(manifest.encode("utf-8")).hexdigest()}
    return events, folder_ids


def pattern_record(text: str) -> dict:
    record = json.loads(text)
    if not isinstance(record, dict) or any(key not in record for key in PATTERN_KEYS):
        raise ExtractError(f"{PATTERN}: a key of {PATTERN_KEYS} is missing")
    for key in ("first_seen", "last_seen"):
        date.fromisoformat(record[key])
    if not isinstance(record["evidence"], list) or not isinstance(record["occurrence_count"], int):
        raise ExtractError(f"{PATTERN}: unexpected evidence or occurrence_count")
    return {key: record[key] for key in PATTERN_KEYS}


def producer_workflow(text: str) -> dict:
    """What the workflow that wrote the trigger files says about itself."""
    retired = re.search(r"^# RETIRED (\d{4}-\d{2}-\d{2})", text, re.MULTILINE)
    orphans = re.search(r"accumulated (\d+) orphans", text)
    types = re.findall(r'echo "type=([^"]+)" >> \$GITHUB_OUTPUT', text)
    if not retired or not orphans or not types or "state/triggers/${TIMESTAMP}-" not in text:
        raise ExtractError(f"{PRODUCER}: retirement comment, orphan count, type list or file name template not found")
    return {"retired_on": retired.group(1), "orphaned_triggers_stated_in_comment": int(orphans.group(1)),
            "trigger_types_it_can_write": types,
            "file_name_template": "state/triggers/${TIMESTAMP}-<type>.trigger.json, one file per workflow run"}


def scheduled_workflow(text: str) -> dict:
    crons = re.findall(r"^\s*- cron: '([^']+)'", text, re.MULTILINE)
    if not crons or "post_discussion.sh" not in text:
        raise ExtractError(f"{SCHEDULED}: cron schedule or post_discussion.sh call not found")
    return {"cron_utc": crons, "calls_post_discussion_script": True}


def build(root: Path, allow_drift: bool) -> dict:
    events, folder_ids = read_events(root)
    texts, files = {}, []
    for rel in (PATTERN, PRODUCER, SCHEDULED):
        texts[rel], entry = read_pinned(root, rel)
        files.append(entry)

    drift = [f"{TRIGGER_DIR}: {key} is {folder_ids[key]}, pinned {PINNED_FOLDER[key]}"
             for key in PINNED_FOLDER if folder_ids[key] != PINNED_FOLDER[key]]
    drift += [f"{entry['path']} is blob {entry['git_blob']}, pinned {PINNED_BLOBS[entry['path']]}"
              for entry in files if entry["git_blob"] != PINNED_BLOBS[entry["path"]]]
    if drift and not allow_drift:
        raise ExtractError("source files are not those of commit " + PINNED_COMMIT + ":\n  " + "\n  ".join(drift)
                           + "\n(--allow-drift snapshots them anyway; the lesson's numbers then no longer apply)")

    events.sort(key=lambda event: (event["timestamp"], event["type"]))
    days = sorted({event["timestamp"][:10] for event in events})
    first, last = date.fromisoformat(days[0]), date.fromisoformat(days[-1])
    by_type: dict[str, int] = {}
    for event in events:
        by_type[event["type"]] = by_type.get(event["type"], 0) + 1
    return {
        "schema_version": "0.1.0",
        "module_id": "psy-008-bursts-are-not-rates",
        "kind": "observed",
        "source": {
            "repository": "GuitarAlchemist/Demerzel",
            "commit": None if drift else PINNED_COMMIT,
            "commit_check": ("FAILED: " + "; ".join(drift)) if drift else
                            "the trigger folder has the file count, Git tree id and manifest digest recorded for this "
                            "commit, and each file below has its Git blob id (CRLF normalised to LF)",
            "trigger_folder": {"path": TRIGGER_DIR} | folder_ids | {
                "manifest": "SHA-256 of the lines '<blob id> <path>' (repository-relative path, sorted by path "
                            "bytes, each ended by a line feed)",
                "reproduce_manifest": f"git ls-tree -r {PINNED_COMMIT} -- {TRIGGER_DIR} | "
                                      "awk '{print $3\" \"$4}' | sha256sum",
                "reproduce_git_tree": f"git ls-tree {PINNED_COMMIT} state/triggers/",
            },
            "files": files,
        },
        "encoding": {
            "events": "one string per archived trigger file, '<JSON timestamp, UTC> <type>', in time order",
            "day": "the UTC date of the timestamp; calendar days run from the first to the last day, both included",
            "checked_in_every_file": "six keys (type, repo, ref, priority, details, timestamp); details holds event, "
                                     "sender, run_id; the file name's timestamp and type equal the JSON fields",
        },
        "counts": {
            "events": len(events),
            "first_event": events[0]["timestamp"],
            "last_event": events[-1]["timestamp"],
            "first_day": days[0],
            "last_day": days[-1],
            "calendar_days": (last - first).days + 1,
            "active_days": len(days),
            "days_without_event": (last - first).days + 1 - len(days),
            "by_type": dict(sorted(by_type.items(), key=lambda item: (-item[1], item[0]))),
            "distinct_timestamps": len({event["timestamp"] for event in events}),
            "distinct_run_ids": len({event["run_id"] for event in events}),
            "distinct_senders": len({event["sender"] for event in events}),
            "distinct_repos": len({event["repo"] for event in events}),
        },
        "anti_pattern_record": pattern_record(texts[PATTERN]),
        "producer_workflow": producer_workflow(texts[PRODUCER]),
        "scheduled_discussion_workflow": scheduled_workflow(texts[SCHEDULED]),
        "events": [f"{event['timestamp']} {event['type']}" for event in events],
    }


def main() -> int:
    here = FIXTURE_FILE
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--repo-root", type=Path, default=here.parents[5])
    parser.add_argument("--output", type=Path, default=here.with_name("observed-input.json"))
    parser.add_argument("--allow-drift", action="store_true",
                        help="snapshot source files that differ from the pinned commit")
    args = parser.parse_args()
    try:
        snapshot = build(args.repo_root, args.allow_drift)
    except (ExtractError, OSError, UnicodeDecodeError, ValueError) as exc:
        print(f"extract.py: {exc}", file=sys.stderr)
        return 1
    text = json.dumps(snapshot, ensure_ascii=False, indent=2) + "\n"
    args.output.write_bytes(text.encode("utf-8"))
    counts = snapshot["counts"]
    print(f"extract.py: {counts['events']} events on {counts['active_days']} of {counts['calendar_days']} calendar "
          f"days ({counts['first_day']} to {counts['last_day']}) -> {args.output.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
