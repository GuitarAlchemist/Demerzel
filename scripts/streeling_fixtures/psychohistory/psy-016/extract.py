#!/usr/bin/env python3
"""PSY-016 extract: snapshot the effectiveness labels of the quality trend.

Reads the five state/quality-trend/*.jsonl files of the pinned commit and
writes observed-input.json next to this script: the run timestamps and, for
each artifact, one label per run. The analysis script reads only that
snapshot, so its results do not move when the nightly feeder appends rows.

Fails with a non-zero exit and a message when a source file is missing, has an
unexpected shape, or is not the file of the pinned commit.

Run from the repository root:
    python -I -B scripts/streeling_fixtures/psychohistory/psy-016/extract.py
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from datetime import datetime
from pathlib import Path

# This program lives under scripts/ (CONTRIBUTING.md: no executable code outside scripts/); its data stays
# under state/streeling/fixtures/. FIXTURE_FILE is the path the program would have next to that data.
FIXTURE_FILE = (Path(__file__).resolve().parents[4]
                / "state/streeling/fixtures/psychohistory/psy-016" / Path(__file__).name)

HERE = FIXTURE_FILE.parent
PINNED_COMMIT = "4b03838800dcd4894f1e026461979bff1d985ca8"
# Git blob ids at PINNED_COMMIT, from `git ls-tree -r <commit> -- state/quality-trend`.
PINNED_BLOBS = {
    "state/quality-trend/2026-05.jsonl": "ab1c35d9948c9bfbb1501b20c39b736d92dc0bb2",
    "state/quality-trend/2026-07.jsonl": "57b303ea2ed56d96010345a2acd508bff248486e",
    "state/quality-trend/2026-08.jsonl": "e2b4462797f1ee06f3188154611de0fdbcc07a23",
    "state/quality-trend/2026-09.jsonl": "9b74c1a34378e3f3941c1c0bb054f5b10fe2b64f",
    "state/quality-trend/2026-10.jsonl": "e64c9c855667f2408e1e4f8c894e1be2722afdd1",
}
TREND_DIR = "state/quality-trend"
LABELS = {"T": "True", "P": "Probable", "U": "Unknown", "D": "Doubtful", "F": "False", "C": "Contradictory"}
TIMESTAMP = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")
NO_ROW, NO_LABEL, SEED = ".", "-", "s"


class ExtractError(Exception):
    """A source file is missing, malformed, or not the pinned one."""


def git_blob_id(data: bytes) -> str:
    """The id Git gives this content, with CRLF normalised to LF as in the repository."""
    data = data.replace(b"\r\n", b"\n")
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()


def data_label(name: str) -> str:
    """An artifact name as a data label: a space on each side of every slash.

    scripts/evolution_metrics.py counts every tracked file that contains an artifact's path as a citation of that
    artifact. The snapshot is a data file about the artifacts, not a citation of them: it holds only labels.
    """
    return " / ".join(name.split("/")).rstrip()


def parse_row(line: str, where: str, month: str) -> dict:
    """One JSONL line as (timestamp, artifact, label, seed flag), or an ExtractError."""
    if not line.strip():
        raise ExtractError(f"{where}: blank line")
    try:
        row = json.loads(line)
    except json.JSONDecodeError as exc:
        raise ExtractError(f"{where}: not JSON ({exc})") from exc
    if not isinstance(row, dict):
        raise ExtractError(f"{where}: not a JSON object")
    for key in ("timestamp", "artifact", "effectiveness_to"):
        if key not in row:
            raise ExtractError(f"{where}: missing key {key!r}")
    timestamp, artifact, label = row["timestamp"], row["artifact"], row["effectiveness_to"]
    if not isinstance(timestamp, str) or not TIMESTAMP.match(timestamp):
        raise ExtractError(f"{where}: unexpected timestamp {timestamp!r}")
    try:
        datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%SZ")
    except ValueError as exc:
        raise ExtractError(f"{where}: {timestamp!r} is not a date") from exc
    if timestamp[:7] != month:
        raise ExtractError(f"{where}: timestamp {timestamp} is not in month file {month}")
    if not isinstance(artifact, str) or not artifact:
        raise ExtractError(f"{where}: unexpected artifact {artifact!r}")
    if label is not None and label not in LABELS:
        raise ExtractError(f"{where}: unexpected effectiveness_to {label!r}")
    if not isinstance(row.get("baseline", False), bool):
        raise ExtractError(f"{where}: unexpected baseline flag {row['baseline']!r}")
    return {"timestamp": timestamp, "artifact": artifact, "label": label, "seed": row.get("baseline", False)}


def read_rows(root: Path) -> tuple[list[dict], list[dict]]:
    """Every row of every month file, in file order, and one entry per file read."""
    trend = root / TREND_DIR
    if not trend.is_dir():
        raise ExtractError(f"missing directory: {TREND_DIR}")
    paths = sorted(trend.glob("*.jsonl"))
    if not paths:
        raise ExtractError(f"no *.jsonl file in {TREND_DIR}")
    rows, files, seen, latest = [], [], set(), ""
    for path in paths:
        rel = path.relative_to(root).as_posix()
        data = path.read_bytes()
        lines = data.decode("utf-8").splitlines()
        for number, line in enumerate(lines, 1):
            where = f"{rel}:{number}"
            row = parse_row(line, where, path.stem)
            if row["timestamp"] < latest:
                raise ExtractError(f"{where}: timestamp {row['timestamp']} is earlier than the row before it")
            latest = row["timestamp"]
            if (row["timestamp"], row["artifact"]) in seen:
                raise ExtractError(f"{where}: second row for {row['artifact']!r} at {row['timestamp']}")
            seen.add((row["timestamp"], row["artifact"]))
            rows.append(row)
        files.append({"path": rel, "git_blob": git_blob_id(data), "rows": len(lines)})
    return rows, files


def drift_report(files: list[dict]) -> list[str]:
    """Differences between the files read and the files of the pinned commit."""
    read = {entry["path"]: entry["git_blob"] for entry in files}
    report = [f"{path} is blob {blob}, pinned {PINNED_BLOBS.get(path, 'nothing: the file is not in the pin')}"
              for path, blob in read.items() if PINNED_BLOBS.get(path) != blob]
    return report + [f"{path} is pinned but was not found" for path in sorted(set(PINNED_BLOBS) - set(read))]


def encode(rows: list[dict]) -> tuple[list[dict], list[dict]]:
    """Runs in time order, and per artifact one character per run for the label and the seed flag."""
    stamps = sorted({row["timestamp"] for row in rows})
    index = {stamp: position for position, stamp in enumerate(stamps)}
    per_run = [0] * len(stamps)
    cells: dict[str, dict[str, list[str]]] = {}
    for row in rows:
        position = index[row["timestamp"]]
        per_run[position] += 1
        own = cells.setdefault(row["artifact"], {"label": [NO_ROW] * len(stamps), "seed": [NO_ROW] * len(stamps)})
        own["label"][position] = row["label"] or NO_LABEL
        own["seed"][position] = SEED if row["seed"] else NO_LABEL
    runs = [{"index": position, "timestamp": stamp, "rows": per_run[position]} for position, stamp in enumerate(stamps)]
    if len({data_label(name) for name in cells}) != len(cells):
        raise ExtractError("two artifact names give the same data label")
    artifacts = []
    for name in sorted(cells):
        labels = "".join(cells[name]["label"])
        artifacts.append({"name": data_label(name), "rows": len(labels) - labels.count(NO_ROW),
                          "first_run_index": len(labels) - len(labels.lstrip(NO_ROW)),
                          "effectiveness_to": labels, "baseline_flag": "".join(cells[name]["seed"])})
    return runs, artifacts


def count_pairs(artifacts: list[dict]) -> dict:
    """Pairs of consecutive rows of one artifact; usable when both rows carry a label."""
    counts = {"row_pairs": 0, "pairs_without_a_label": 0, "usable_pairs": 0, "changed": 0, "unchanged": 0,
              "usable_pairs_from_a_seed_row": 0, "changed_from_a_seed_row": 0}
    for artifact in artifacts:
        rows = [(label, flag) for label, flag in zip(artifact["effectiveness_to"], artifact["baseline_flag"])
                if label != NO_ROW]
        for (earlier, flag), (later, _) in zip(rows, rows[1:]):
            counts["row_pairs"] += 1
            if NO_LABEL in (earlier, later):
                counts["pairs_without_a_label"] += 1
                continue
            counts["usable_pairs"] += 1
            counts["changed" if earlier != later else "unchanged"] += 1
            if flag == SEED:
                counts["usable_pairs_from_a_seed_row"] += 1
                counts["changed_from_a_seed_row"] += earlier != later
    return counts


def build(root: Path, allow_drift: bool) -> dict:
    """The snapshot written to observed-input.json."""
    rows, files = read_rows(root)
    drift = drift_report(files)
    if drift and not allow_drift:
        raise ExtractError("source files are not those of commit " + PINNED_COMMIT + ":\n  " + "\n  ".join(drift)
                           + "\n(--allow-drift snapshots them anyway; the lesson's numbers then no longer apply)")
    runs, artifacts = encode(rows)
    return {
        "schema_version": "0.1.0",
        "module_id": "psy-016-brier-score",
        "kind": "observed",
        "source": {
            "repository": "GuitarAlchemist/Demerzel",
            "commit": None if drift else PINNED_COMMIT,
            "commit_check": ("FAILED: " + "; ".join(drift)) if drift else
                            "every file below has the Git blob id recorded for this commit (CRLF normalised to LF)",
            "files": files,
        },
        "encoding": {
            "runs": "one entry per distinct timestamp, in time order; every row of a run carries that timestamp",
            "artifact names": "data labels: the name of the quality trend with a space on each side of every slash, "
                              "so that this file holds no artifact path as a literal string",
            "artifact strings": "one character per run, aligned with the runs list",
            NO_ROW: "the artifact has no row in that run",
            NO_LABEL: "the row exists and the field is null (for baseline_flag: the flag is absent or false)",
            SEED: "baseline_flag only: the row carries baseline: true (a seed row)",
            "labels": LABELS,
        },
        "counts": {
            "rows": len(rows),
            "files": len(files),
            "runs": len(runs),
            "run_dates_utc": len({run["timestamp"][:10] for run in runs}),
            "artifacts": len(artifacts),
            "rows_flagged_baseline": sum(row["seed"] for row in rows),
            "rows_without_effectiveness_to": sum(row["label"] is None for row in rows),
            "consecutive_pairs": count_pairs(artifacts),
        },
        "runs": runs,
        "artifacts": artifacts,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--repo-root", type=Path, default=HERE.parents[4])
    parser.add_argument("--output", type=Path, default=HERE / "observed-input.json")
    parser.add_argument("--allow-drift", action="store_true",
                        help="snapshot source files that differ from the pinned commit")
    args = parser.parse_args()
    try:
        snapshot = build(args.repo_root, args.allow_drift)
    except (ExtractError, OSError, UnicodeDecodeError) as exc:
        print(f"extract.py: {exc}", file=sys.stderr)
        return 1
    with open(args.output, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(json.dumps(snapshot, ensure_ascii=False, indent=2) + "\n")
    pairs = snapshot["counts"]["consecutive_pairs"]
    print(f"extract.py: {snapshot['counts']['rows']} rows, {snapshot['counts']['runs']} runs, "
          f"{snapshot['counts']['artifacts']} artifacts, {pairs['usable_pairs']} usable pairs, "
          f"{pairs['changed']} changed -> {args.output.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
