#!/usr/bin/env python3
"""PSY-022 extract: snapshot the archived trigger log as one count per calendar day.

Reads every file of state/triggers/archived/ (the JSON timestamp and type,
cross-checked with the file name), counts the events of each UTC calendar day
from the first to the last day, empty days included, and writes
observed-input.json next to this script. The analysis script reads only that
snapshot.

Fails with a non-zero exit and a message when the folder is missing, a file
has an unexpected shape, or the folder is not the one of the pinned commit.
The folder holds 594 files, so it is pinned by one manifest digest, its file
count and its Git tree id, not by 594 embedded blob ids.

Run from the repository root:
    python -I -B scripts/streeling_fixtures/psychohistory/psy-022/extract.py
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from datetime import date, datetime, timedelta
from pathlib import Path

# This program lives under scripts/ (CONTRIBUTING.md: no executable code outside scripts/); its data stays
# under state/streeling/fixtures/. FIXTURE_FILE is the path the program would have next to that data.
FIXTURE_FILE = (Path(__file__).resolve().parents[4]
                / "state/streeling/fixtures/psychohistory/psy-022" / Path(__file__).name)

HERE = FIXTURE_FILE.parent
PINNED_COMMIT = "4b03838800dcd4894f1e026461979bff1d985ca8"
TRIGGER_DIR = "state/triggers/archived"
# git ls-tree -r <pin> -- state/triggers/archived | awk '{print $3" "$4}' | sha256sum
# git ls-tree <pin> state/triggers/   (the line of the `archived` tree)
PINNED_FOLDER = {
    "files": 594,
    "git_tree": "2da37c16496d39c0c9137897c8be2b0c6d6b7978",
    "manifest_sha256": "3e33b3e795b977277c52c99d59c48f15ae60f95d28f5524c641d3ec066f10393",
}
FILE_NAME = re.compile(r"^(\d{4}-\d{2}-\d{2})T(\d{2})-(\d{2})-(\d{2})Z-([a-z_]+)\.trigger\.json$")
EVENT_KEYS = {"type", "repo", "ref", "priority", "details", "timestamp"}
DETAIL_KEYS = {"event", "sender", "run_id"}


class ExtractError(Exception):
    """The trigger folder is missing, malformed, or not the pinned one."""


def git_blob_id(data: bytes) -> str:
    """Blob id Git stores for this content once CRLF is normalised to LF."""
    data = data.replace(b"\r\n", b"\n")
    return hashlib.sha1(b"blob %d\x00" % len(data) + data).hexdigest()


def git_tree_id(entries: list[tuple[str, str]]) -> str:
    """Tree id of a folder that holds only regular, non-executable files."""
    body = b"".join(b"100644 " + name.encode("utf-8") + b"\x00" + bytes.fromhex(blob) for name, blob in entries)
    return hashlib.sha1(b"tree %d\x00" % len(body) + body).hexdigest()


def read_event(path: Path, where: str) -> tuple[str, str, str]:
    """One trigger file -> (UTC timestamp, type, Git blob id), after checking its shape against its name."""
    match = FILE_NAME.match(path.name)
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
    day, hour, minute, second, kind = match.groups()
    stamp = f"{day}T{hour}:{minute}:{second}Z"
    try:
        datetime.strptime(stamp, "%Y-%m-%dT%H:%M:%SZ")
    except ValueError as exc:
        raise ExtractError(f"{where}: file name does not hold a valid time ({exc})") from exc
    if event["timestamp"] != stamp or event["type"] != kind:
        raise ExtractError(f"{where}: JSON timestamp or type ({event['timestamp']!r}, {event['type']!r}) "
                           "differs from the file name")
    return stamp, kind, git_blob_id(data)


def read_folder(root: Path) -> tuple[list[tuple[str, str]], dict]:
    """Every archived trigger -> [(timestamp, type)], plus the folder's file count, Git tree id and manifest digest."""
    folder = root / TRIGGER_DIR
    if not folder.is_dir():
        raise ExtractError(f"missing directory: {TRIGGER_DIR}")
    names = sorted((path.name for path in folder.iterdir()), key=lambda name: name.encode("utf-8"))
    if not names:
        raise ExtractError(f"no file in {TRIGGER_DIR}")
    events, entries = [], []
    for name in names:
        stamp, kind, blob = read_event(folder / name, f"{TRIGGER_DIR}/{name}")
        events.append((stamp, kind))
        entries.append((name, blob))
    manifest = "".join(f"{blob} {TRIGGER_DIR}/{name}\n" for name, blob in entries)
    folder_ids = {"files": len(entries), "git_tree": git_tree_id(entries),
                  "manifest_sha256": hashlib.sha256(manifest.encode("utf-8")).hexdigest()}
    return events, folder_ids


def daily_counts(events: list[tuple[str, str]]) -> dict[str, int]:
    """Events per UTC calendar day from the first to the last day, both included; an empty day counts 0."""
    per_day: dict[str, int] = {}
    for stamp, _ in events:
        per_day[stamp[:10]] = per_day.get(stamp[:10], 0) + 1
    first, last = date.fromisoformat(min(per_day)), date.fromisoformat(max(per_day))
    days = [first + timedelta(days=offset) for offset in range((last - first).days + 1)]
    return {day.isoformat(): per_day.get(day.isoformat(), 0) for day in days}


def source_section(folder_ids: dict, drift: list[str]) -> dict:
    return {
        "repository": "GuitarAlchemist/Demerzel",
        "commit": None if drift else PINNED_COMMIT,
        "commit_check": ("FAILED: " + "; ".join(drift)) if drift else
                        "the trigger folder has the file count, Git tree id and manifest digest recorded for this "
                        "commit (blob ids computed with CRLF normalised to LF)",
        "trigger_folder": {"path": TRIGGER_DIR} | folder_ids | {
            "manifest": "SHA-256 of the lines '<blob id> <path>' (repository-relative path, sorted by path bytes, "
                        "each ended by a line feed)",
            "reproduce_manifest": f"git ls-tree -r {PINNED_COMMIT} -- {TRIGGER_DIR} | "
                                  "awk '{print $3\" \"$4}' | sha256sum",
            "reproduce_git_tree": f"git ls-tree {PINNED_COMMIT} state/triggers/",
        },
    }


def build(root: Path, allow_drift: bool) -> dict:
    events, folder_ids = read_folder(root)
    drift = [f"{TRIGGER_DIR}: {key} is {folder_ids[key]}, pinned {PINNED_FOLDER[key]}"
             for key in PINNED_FOLDER if folder_ids[key] != PINNED_FOLDER[key]]
    if drift and not allow_drift:
        raise ExtractError("the trigger folder is not that of commit " + PINNED_COMMIT + ":\n  " + "\n  ".join(drift)
                           + "\n(--allow-drift snapshots it anyway; the lesson's numbers then no longer apply)")
    events.sort()
    per_day = daily_counts(events)
    by_type: dict[str, int] = {}
    for _, kind in events:
        by_type[kind] = by_type.get(kind, 0) + 1
    busiest = sorted(per_day.items(), key=lambda item: (-item[1], item[0]))[:4]
    return {
        "schema_version": "0.1.0",
        "module_id": "psy-022-competing-explanations",
        "kind": "observed",
        "source": source_section(folder_ids, drift),
        "encoding": {
            "day": "the UTC date of a trigger's JSON timestamp; calendar days run from the first to the last day, "
                   "both included, and a day without a trigger file counts 0",
            "daily_counts": "calendar day -> number of archived trigger files stamped on that day, in calendar order",
            "checked_in_every_file": "six keys (type, repo, ref, priority, details, timestamp); details holds event, "
                                     "sender, run_id; the file name's timestamp and type equal the JSON fields",
            "not_kept": "the events themselves: this module analyses the daily counts only",
        },
        "counts": {
            "events": len(events),
            "first_event": events[0][0],
            "last_event": events[-1][0],
            "first_day": min(per_day),
            "last_day": max(per_day),
            "calendar_days": len(per_day),
            "active_days": sum(count > 0 for count in per_day.values()),
            "days_without_event": sum(count == 0 for count in per_day.values()),
            "by_type": dict(sorted(by_type.items(), key=lambda item: (-item[1], item[0]))),
            "busiest_days": [{"day": day, "events": count} for day, count in busiest],
        },
        "daily_counts": per_day,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--repo-root", type=Path, default=HERE.parents[4])
    parser.add_argument("--output", type=Path, default=HERE / "observed-input.json")
    parser.add_argument("--allow-drift", action="store_true",
                        help="snapshot a trigger folder that differs from the pinned commit")
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
