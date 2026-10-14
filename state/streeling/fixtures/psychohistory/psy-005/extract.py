#!/usr/bin/env python3
"""PSY-005 extract: snapshot the effectiveness labels of the quality trend.

Reads state/quality-trend/*.jsonl (and the evolution record of each artifact
whose label changed) and writes observed-input.json next to this script. The
analysis script reads only that snapshot, so its results do not move when the
nightly feeder appends new rows.

Fails with a non-zero exit and a message when a source file is missing, has an
unexpected shape, or is not the file of the pinned commit.

Run from the repository root:
    python -I state/streeling/fixtures/psychohistory/psy-005/extract.py
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

PINNED_COMMIT = "4b03838800dcd4894f1e026461979bff1d985ca8"
# Git blob ids at PINNED_COMMIT (git ls-tree). A blob id is
# sha1(b"blob <size>\0" + content) over the LF-normalised bytes.
PINNED_BLOBS = {
    "state/quality-trend/2026-05.jsonl": "ab1c35d9948c9bfbb1501b20c39b736d92dc0bb2",
    "state/quality-trend/2026-07.jsonl": "57b303ea2ed56d96010345a2acd508bff248486e",
    "state/quality-trend/2026-08.jsonl": "e2b4462797f1ee06f3188154611de0fdbcc07a23",
    "state/quality-trend/2026-09.jsonl": "9b74c1a34378e3f3941c1c0bb054f5b10fe2b64f",
    "state/quality-trend/2026-10.jsonl": "e64c9c855667f2408e1e4f8c894e1be2722afdd1",
    "state/evolution/2026-03-20-autonomous-driver.evolution.json": "8465478632590e1679ec93c725d5383f8b67e2ab",
}
TREND_DIR = "state/quality-trend"
EVOLUTION_DIR = "state/evolution"
LABELS = ("T", "P", "U", "D", "F", "C")
LABEL_NAMES = {"T": "True", "P": "Probable", "U": "Unknown", "D": "Doubtful", "F": "False", "C": "Contradictory"}
TIMESTAMP = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")
NO_ROW, NO_LABEL = ".", "-"


class ExtractError(Exception):
    """A source file is missing, malformed, or not the pinned one."""


def git_blob_id(data: bytes) -> str:
    """Blob id Git stores for this content once CRLF is normalised to LF."""
    data = data.replace(b"\r\n", b"\n")
    return hashlib.sha1(b"blob %d\x00" % len(data) + data).hexdigest()


def parse_timestamp(value: str) -> datetime:
    return datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)


def read_rows(root: Path) -> tuple[list[dict], list[dict]]:
    trend = root / TREND_DIR
    if not trend.is_dir():
        raise ExtractError(f"missing directory: {TREND_DIR}")
    paths = sorted(trend.glob("*.jsonl"))
    if not paths:
        raise ExtractError(f"no *.jsonl file in {TREND_DIR}")
    rows, files, seen = [], [], set()
    previous_timestamp = ""
    for path in paths:
        rel = path.relative_to(root).as_posix()
        data = path.read_bytes()
        lines = data.decode("utf-8").splitlines()
        for number, line in enumerate(lines, 1):
            where = f"{rel}:{number}"
            if not line.strip():
                raise ExtractError(f"{where}: blank line")
            try:
                row = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ExtractError(f"{where}: not JSON ({exc})") from exc
            if not isinstance(row, dict):
                raise ExtractError(f"{where}: not a JSON object")
            for key in ("timestamp", "artifact", "effectiveness_from", "effectiveness_to"):
                if key not in row:
                    raise ExtractError(f"{where}: missing key {key!r}")
            timestamp, artifact = row["timestamp"], row["artifact"]
            if not isinstance(timestamp, str) or not TIMESTAMP.match(timestamp):
                raise ExtractError(f"{where}: unexpected timestamp {timestamp!r}")
            parse_timestamp(timestamp)
            if timestamp[:7] != path.stem:
                raise ExtractError(f"{where}: timestamp {timestamp} is not in month file {path.name}")
            if timestamp < previous_timestamp:
                raise ExtractError(f"{where}: timestamp {timestamp} is earlier than the row before it")
            previous_timestamp = timestamp
            if not isinstance(artifact, str) or not artifact:
                raise ExtractError(f"{where}: unexpected artifact {artifact!r}")
            for key in ("effectiveness_from", "effectiveness_to"):
                if row[key] is not None and row[key] not in LABELS:
                    raise ExtractError(f"{where}: unexpected {key} {row[key]!r}")
            if not isinstance(row.get("baseline", False), bool):
                raise ExtractError(f"{where}: unexpected baseline flag {row['baseline']!r}")
            if (timestamp, artifact) in seen:
                raise ExtractError(f"{where}: second row for {artifact!r} at {timestamp}")
            seen.add((timestamp, artifact))
            rows.append({
                "file": rel, "line": number, "timestamp": timestamp, "artifact": artifact,
                "from": row["effectiveness_from"], "to": row["effectiveness_to"],
                "baseline": row.get("baseline", False),
            })
        files.append({"path": rel, "git_blob": git_blob_id(data), "rows": len(lines)})
    return rows, files


def evolution_record(root: Path, artifact: str) -> dict:
    """The evolution record that names this artifact (exactly one expected)."""
    matches = []
    for path in sorted((root / EVOLUTION_DIR).glob("*.evolution.json")):
        data = path.read_bytes()
        record = json.loads(data.decode("utf-8"))
        if isinstance(record, dict) and record.get("artifact") == artifact:
            matches.append((path, data, record))
    if len(matches) != 1:
        raise ExtractError(f"expected one evolution record for {artifact!r}, found {len(matches)}")
    path, data, record = matches[0]
    effectiveness = record.get("assessment", {}).get("effectiveness")
    if not isinstance(effectiveness, dict) or effectiveness.get("truth_value") not in LABELS:
        raise ExtractError(f"{path.name}: assessment.effectiveness has no truth_value")
    events = record.get("events")
    if not isinstance(events, list) or not all(isinstance(e, dict) and "type" in e and "timestamp" in e for e in events):
        raise ExtractError(f"{path.name}: unexpected events list")
    return {
        "path": path.relative_to(root).as_posix(),
        "git_blob": git_blob_id(data),
        "proposition": effectiveness.get("proposition"),
        "truth_value": effectiveness["truth_value"],
        "last_updated": record.get("last_updated"),
        "events": [{"type": e["type"], "timestamp": e["timestamp"]} for e in events],
    }


def missing_reason(row: dict, previous: dict | None) -> list[str]:
    reasons = []
    if row["from"] is None:
        if previous is None:
            reasons.append("effectiveness_from: first row of this artifact, no earlier label to copy")
        elif previous["to"] is None:
            reasons.append("effectiveness_from: the artifact's previous row has no effectiveness_to")
        else:
            reasons.append("effectiveness_from: null although the previous row has a label")
    if row["to"] is None:
        reasons.append("effectiveness_to: null in the source row; the feeder writes null when the "
                       "evolution record's assessment.effectiveness is not an object with a truth_value")
    return reasons


def build(root: Path, allow_drift: bool) -> dict:
    rows, files = read_rows(root)
    runs = sorted({row["timestamp"] for row in rows})
    run_index = {timestamp: index for index, timestamp in enumerate(runs)}
    by_artifact: dict[str, list[dict]] = {}
    for row in rows:
        by_artifact.setdefault(row["artifact"], []).append(row)

    classes = {"both_labels": 0, "from_missing_only": 0, "to_missing_only": 0, "both_missing": 0}
    in_row = {"pairs": 0, "changed": 0, "unchanged": 0, "seed_rows_among_pairs": 0}
    consecutive = {"row_pairs": 0, "usable_pairs": 0, "changed": 0, "unchanged": 0,
                   "pairs_without_a_label": 0, "from_differs_from_previous_to": 0}
    artifacts, changes, missing, evolution_files = [], [], [], []
    for name in sorted(by_artifact):
        series = by_artifact[name]
        cells = {key: [NO_ROW] * len(runs) for key in ("from", "to", "seed")}
        tally = {"in_row_pairs": 0, "in_row_changed": 0, "consecutive_pairs": 0, "consecutive_changed": 0}
        previous = None
        for row in series:
            index = run_index[row["timestamp"]]
            cells["from"][index] = row["from"] or NO_LABEL
            cells["to"][index] = row["to"] or NO_LABEL
            cells["seed"][index] = "s" if row["baseline"] else NO_LABEL
            key = ("both_labels" if row["from"] and row["to"] else "from_missing_only" if row["to"]
                   else "to_missing_only" if row["from"] else "both_missing")
            classes[key] += 1
            if key == "both_labels":
                in_row["pairs"] += 1
                tally["in_row_pairs"] += 1
                in_row["seed_rows_among_pairs"] += row["baseline"]
                changed = row["from"] != row["to"]
                in_row["changed" if changed else "unchanged"] += 1
                tally["in_row_changed"] += changed
            else:
                missing.append({k: row[k] for k in ("file", "line", "timestamp", "artifact", "from", "to")}
                               | {"reasons": missing_reason(row, previous)})
            if previous is not None:
                consecutive["row_pairs"] += 1
                consecutive["from_differs_from_previous_to"] += row["from"] != previous["to"]
                if previous["to"] and row["to"]:
                    consecutive["usable_pairs"] += 1
                    tally["consecutive_pairs"] += 1
                    changed = previous["to"] != row["to"]
                    consecutive["changed" if changed else "unchanged"] += 1
                    tally["consecutive_changed"] += changed
                    if changed:
                        gap = parse_timestamp(row["timestamp"]) - parse_timestamp(previous["timestamp"])
                        changes.append({
                            "artifact": name, "from": previous["to"], "to": row["to"],
                            "earlier_row": {k: previous[k] for k in ("file", "line", "timestamp", "baseline")},
                            "later_row": {k: row[k] for k in ("file", "line", "timestamp", "baseline")},
                            "gap_days": round(gap.total_seconds() / 86400, 3),
                            "evolution_record": evolution_record(root, name),
                        })
                else:
                    consecutive["pairs_without_a_label"] += 1
            previous = row
        artifacts.append({
            "name": name, "rows": len(series), "first_run_index": run_index[series[0]["timestamp"]],
            "effectiveness_from": "".join(cells["from"]), "effectiveness_to": "".join(cells["to"]),
            "baseline_flag": "".join(cells["seed"]), **tally,
        })
    for change in changes:
        record = change["evolution_record"]
        evolution_files.append({"path": record["path"], "git_blob": record["git_blob"]})

    drift = []
    for entry in files + evolution_files:
        if PINNED_BLOBS.get(entry["path"]) != entry["git_blob"]:
            drift.append(f"{entry['path']} is blob {entry['git_blob']}, pinned {PINNED_BLOBS.get(entry['path'])}")
    drift += [f"{path} is pinned but was not read" for path in sorted(set(PINNED_BLOBS) - {e["path"] for e in files + evolution_files})]
    if drift and not allow_drift:
        raise ExtractError("source files are not those of commit " + PINNED_COMMIT + ":\n  " + "\n  ".join(drift)
                           + "\n(--allow-drift snapshots them anyway; the lesson's numbers then no longer apply)")

    run_rows = [0] * len(runs)
    for row in rows:
        run_rows[run_index[row["timestamp"]]] += 1
    return {
        "schema_version": "0.1.0",
        "module_id": "psy-005-persistence-baseline",
        "kind": "observed",
        "source": {
            "repository": "GuitarAlchemist/Demerzel",
            "commit": None if drift else PINNED_COMMIT,
            "commit_check": ("FAILED: " + "; ".join(drift)) if drift else
                            "every file below has the Git blob id recorded for this commit (CRLF normalised to LF)",
            "files": files,
            "evolution_records": evolution_files,
        },
        "encoding": {
            "runs": "one entry per distinct timestamp, in time order; every row of a run carries that timestamp",
            "artifact strings": "one character per run, aligned with the runs list",
            NO_ROW: "the artifact has no row in that run",
            NO_LABEL: "the row exists and the field is null (for baseline_flag: the flag is absent)",
            "s": "baseline_flag only: the row carries baseline: true",
            "labels": LABEL_NAMES,
        },
        "counts": {
            "rows": len(rows),
            "files": len(files),
            "runs": len(runs),
            "run_dates_utc": len({timestamp[:10] for timestamp in runs}),
            "artifacts": len(by_artifact),
            "rows_flagged_baseline": sum(row["baseline"] for row in rows),
            "rows_by_label_presence": classes,
            "in_row_pairs": in_row,
            "consecutive_pairs": consecutive,
        },
        "label_changes": changes,
        "rows_with_a_missing_label": missing,
        "runs": [{"index": index, "timestamp": timestamp, "rows": run_rows[index]} for index, timestamp in enumerate(runs)],
        "artifacts": artifacts,
    }


def main() -> int:
    here = Path(__file__).resolve()
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--repo-root", type=Path, default=here.parents[5])
    parser.add_argument("--output", type=Path, default=here.with_name("observed-input.json"))
    parser.add_argument("--allow-drift", action="store_true",
                        help="snapshot source files that differ from the pinned commit")
    args = parser.parse_args()
    try:
        snapshot = build(args.repo_root, args.allow_drift)
    except (ExtractError, OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        print(f"extract.py: {exc}", file=sys.stderr)
        return 1
    text = json.dumps(snapshot, ensure_ascii=False, indent=2) + "\n"
    args.output.write_bytes(text.encode("utf-8"))
    counts = snapshot["counts"]
    print(f"extract.py: {counts['rows']} rows, {counts['runs']} runs, {counts['artifacts']} artifacts, "
          f"{counts['consecutive_pairs']['usable_pairs']} consecutive pairs, "
          f"{counts['consecutive_pairs']['changed']} changed -> {args.output.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
