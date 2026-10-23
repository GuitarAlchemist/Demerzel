#!/usr/bin/env python3
"""PSY-018 extract: snapshot the citation counts of the quality trend.

Reads state/quality-trend/*.jsonl and the one line of scripts/quality_trend.py
that defines delta_citations, checks that the two scripts the lesson quotes
are those of the pinned commit, and writes observed-input.json next to this
script. The analysis script reads only that snapshot, so its results do not
move when the nightly feeder appends new rows.

Fails with a non-zero exit and a message when a source file is missing, has an
unexpected shape, or is not the file of the pinned commit.

Run from the repository root:
    python -I scripts/streeling_fixtures/psychohistory/psy-018/extract.py
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

# This program lives under scripts/ (CONTRIBUTING.md: no executable code outside scripts/); its data stays
# under state/streeling/fixtures/. FIXTURE_FILE is the path the program would have next to that data.
FIXTURE_FILE = (Path(__file__).resolve().parents[4]
                / "state/streeling/fixtures/psychohistory/psy-018" / Path(__file__).name)

HERE = FIXTURE_FILE.parent
PINNED_COMMIT = "4b03838800dcd4894f1e026461979bff1d985ca8"
# Git blob ids at PINNED_COMMIT (git ls-tree). A blob id is
# sha1(b"blob <size>\0" + content) over the LF-normalised bytes.
PINNED_BLOBS = {
    "state/quality-trend/2026-05.jsonl": "ab1c35d9948c9bfbb1501b20c39b736d92dc0bb2",
    "state/quality-trend/2026-07.jsonl": "57b303ea2ed56d96010345a2acd508bff248486e",
    "state/quality-trend/2026-08.jsonl": "e2b4462797f1ee06f3188154611de0fdbcc07a23",
    "state/quality-trend/2026-09.jsonl": "9b74c1a34378e3f3941c1c0bb054f5b10fe2b64f",
    "state/quality-trend/2026-10.jsonl": "e64c9c855667f2408e1e4f8c894e1be2722afdd1",
    "scripts/quality_trend.py": "6180a21d72e1c4f4c89197e701e202dce079b5a8",
    "scripts/evolution_metrics.py": "024da5615525dbd351265dfdb2f9040485e77b7f",
}
TREND_DIR = "state/quality-trend"
FEEDER = "scripts/quality_trend.py"
# Scripts the lesson quotes: their blob ids are checked, and only FEEDER_RULE_LINE of the feeder is read.
CONTEXT_FILES = (FEEDER, "scripts/evolution_metrics.py")
FEEDER_RULE_LINE = 99
FEEDER_RULE = '"delta_citations": 0 if rebaseline else citation - int(prev.get("citation_count", 0) or 0),'
SOURCES = {None: "n", "git-grep-v1": "g"}  # citation_source values -> one-character code
TIMESTAMP = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")
NO_ROW, ABSENT = ".", "-"


class ExtractError(Exception):
    """A source file is missing, malformed, or not the pinned one."""


def git_blob_id(data: bytes) -> str:
    """Blob id Git stores for this content once CRLF is normalised to LF."""
    data = data.replace(b"\r\n", b"\n")
    return hashlib.sha1(b"blob %d\x00" % len(data) + data).hexdigest()


def is_count(value: object) -> bool:
    return isinstance(value, int) and not isinstance(value, bool)


def label(name: str) -> str:
    """An artifact name as a data label: a space on each side of every slash.

    scripts/evolution_metrics.py counts each tracked file that contains an artifact's path as one citation of it.
    Written as labels, the names in the snapshot and in the results cannot raise the counts this module studies.
    """
    return " / ".join(name.split("/")).rstrip()


def check_row(row: object, where: str, month: str) -> dict:
    """Validate one JSONL row and keep the five fields this module uses."""
    if not isinstance(row, dict):
        raise ExtractError(f"{where}: not a JSON object")
    for key in ("timestamp", "artifact", "delta_citations"):
        if key not in row:
            raise ExtractError(f"{where}: missing key {key!r}")
    timestamp, artifact = row["timestamp"], row["artifact"]
    if not isinstance(timestamp, str) or not TIMESTAMP.match(timestamp):
        raise ExtractError(f"{where}: unexpected timestamp {timestamp!r}")
    datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
    if timestamp[:7] != month:
        raise ExtractError(f"{where}: timestamp {timestamp} is not in month file {month}.jsonl")
    if not isinstance(artifact, str) or not artifact:
        raise ExtractError(f"{where}: unexpected artifact {artifact!r}")
    count = row.get("citation_count")
    if count is not None and not (is_count(count) and count >= 0):
        raise ExtractError(f"{where}: unexpected citation_count {count!r}")
    if not is_count(row["delta_citations"]):
        raise ExtractError(f"{where}: unexpected delta_citations {row['delta_citations']!r}")
    for key in ("baseline", "rebaseline"):
        if not isinstance(row.get(key, False), bool):
            raise ExtractError(f"{where}: unexpected {key} flag {row[key]!r}")
    if (count is None) != row.get("baseline", False):
        raise ExtractError(f"{where}: a row lacks citation_count exactly when it is flagged baseline; not here")
    if "citation_source" in row and row["citation_source"] not in SOURCES:
        raise ExtractError(f"{where}: unexpected citation_source {row['citation_source']!r}")
    return {
        "timestamp": timestamp, "artifact": label(artifact), "count": count, "delta": row["delta_citations"],
        "seed": row.get("baseline", False),
        "rebaseline": "r" if row.get("rebaseline") else ("f" if "rebaseline" in row else ABSENT),
        "source": SOURCES[row["citation_source"]] if "citation_source" in row else ABSENT,
    }


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
                row = check_row(json.loads(line), where, path.stem)
            except json.JSONDecodeError as exc:
                raise ExtractError(f"{where}: not JSON ({exc})") from exc
            if row["timestamp"] < previous_timestamp:
                raise ExtractError(f"{where}: timestamp {row['timestamp']} is earlier than the row before it")
            previous_timestamp = row["timestamp"]
            if (row["timestamp"], row["artifact"]) in seen:
                raise ExtractError(f"{where}: second row for {row['artifact']!r} at {row['timestamp']}")
            seen.add((row["timestamp"], row["artifact"]))
            rows.append(row)
        files.append({"path": rel, "git_blob": git_blob_id(data), "rows": len(lines)})
    return rows, files


def read_context(root: Path) -> tuple[list[dict], dict]:
    """Blob ids of the quoted scripts, and the feeder line that defines delta_citations, checked word for word."""
    entries, rule = [], {}
    for rel in CONTEXT_FILES:
        path = root / rel
        if not path.is_file():
            raise ExtractError(f"missing file: {rel}")
        data = path.read_bytes()
        entries.append({"path": rel, "git_blob": git_blob_id(data)})
        if rel == FEEDER:
            lines = data.decode("utf-8").splitlines()
            text = lines[FEEDER_RULE_LINE - 1].strip() if len(lines) >= FEEDER_RULE_LINE else ""
            if text != FEEDER_RULE:
                raise ExtractError(f"{FEEDER}:{FEEDER_RULE_LINE}: expected the delta_citations rule, found {text!r}")
            rule = {"path": FEEDER, "line": FEEDER_RULE_LINE, "text": text}
    return entries, rule


def check_pins(files: list[dict], allow_drift: bool) -> list[str]:
    drift = [f"{entry['path']} is blob {entry['git_blob']}, pinned {PINNED_BLOBS.get(entry['path'])}"
             for entry in files if PINNED_BLOBS.get(entry["path"]) != entry["git_blob"]]
    drift += [f"{path} is pinned but was not read" for path in sorted(set(PINNED_BLOBS) - {e["path"] for e in files})]
    if drift and not allow_drift:
        raise ExtractError("source files are not those of commit " + PINNED_COMMIT + ":\n  " + "\n  ".join(drift)
                           + "\n(--allow-drift snapshots them anyway; the lesson's numbers then no longer apply)")
    return drift


def encode_artifacts(rows: list[dict], runs: list[str]) -> tuple[list[dict], dict]:
    """One entry per artifact with run-aligned strings, and the counts of pairs of consecutive rows."""
    run_index = {timestamp: index for index, timestamp in enumerate(runs)}
    by_artifact: dict[str, list[dict]] = {}
    for row in rows:
        by_artifact.setdefault(row["artifact"], []).append(row)
    pairs = {"pairs_of_consecutive_rows_with_a_count": 0, "count_changed": 0, "count_unchanged": 0,
             "count_changed_by_utc_date": {}, "pairs_ending_at_a_rebaseline_row": 0}
    artifacts = []
    for name in sorted(by_artifact):
        series = by_artifact[name]
        indices = [run_index[row["timestamp"]] for row in series]
        if indices != list(range(indices[0], indices[0] + len(indices))):
            raise ExtractError(f"{name!r}: its rows skip a run; the run-aligned encoding assumes none is skipped")
        cells = {key: [NO_ROW] * len(runs) for key in ("count", "delta", "seed", "rebaseline", "source")}
        previous = None
        for index, row in zip(indices, series):
            cells["count"][index] = ABSENT if row["count"] is None else str(row["count"])
            cells["delta"][index] = str(row["delta"])
            cells["seed"][index] = "s" if row["seed"] else ABSENT
            cells["rebaseline"][index] = row["rebaseline"]
            cells["source"][index] = row["source"]
            if previous is not None and previous["count"] is not None and row["count"] is not None:
                pairs["pairs_of_consecutive_rows_with_a_count"] += 1
                changed = previous["count"] != row["count"]
                pairs["count_changed" if changed else "count_unchanged"] += 1
                pairs["pairs_ending_at_a_rebaseline_row"] += row["rebaseline"] == "r"
                if changed:
                    date = row["timestamp"][:10]
                    pairs["count_changed_by_utc_date"][date] = pairs["count_changed_by_utc_date"].get(date, 0) + 1
            previous = row
        artifacts.append({
            "name": name, "rows": len(series), "first_run_index": indices[0],
            "citation_count": " ".join(cells["count"]), "delta_citations": " ".join(cells["delta"]),
            "baseline_flag": "".join(cells["seed"]), "rebaseline_flag": "".join(cells["rebaseline"]),
            "citation_source": "".join(cells["source"]),
        })
    return artifacts, pairs


def count_rows(rows: list[dict], runs: list[str]) -> dict:
    nonzero = [row for row in rows if row["delta"] != 0]
    by_date: dict[str, int] = {}
    for row in nonzero:
        by_date[row["timestamp"][:10]] = by_date.get(row["timestamp"][:10], 0) + 1
    return {
        "rows": len(rows),
        "runs": len(runs),
        "run_dates_utc": len({timestamp[:10] for timestamp in runs}),
        "artifacts": len({row["artifact"] for row in rows}),
        "rows_flagged_baseline": sum(row["seed"] for row in rows),
        "rows_with_a_citation_count": sum(row["count"] is not None for row in rows),
        "rows_flagged_rebaseline": sum(row["rebaseline"] == "r" for row in rows),
        "rows_by_citation_source": {"key_absent": sum(row["source"] == ABSENT for row in rows),
                                    "null": sum(row["source"] == "n" for row in rows),
                                    "git-grep-v1": sum(row["source"] == "g" for row in rows)},
        "rows_with_a_nonzero_delta_citations": len(nonzero),
        "rows_with_a_nonzero_delta_citations_by_utc_date": by_date,
    }


def build(root: Path, allow_drift: bool) -> dict:
    rows, files = read_rows(root)
    context_files, feeder_rule = read_context(root)
    drift = check_pins(files + context_files, allow_drift)
    runs = sorted({row["timestamp"] for row in rows})
    artifacts, pairs = encode_artifacts(rows, runs)
    run_rows = {timestamp: 0 for timestamp in runs}
    for row in rows:
        run_rows[row["timestamp"]] += 1
    return {
        "schema_version": "0.1.0",
        "module_id": "psy-018-backtesting-without-leakage",
        "kind": "observed",
        "source": {
            "repository": "GuitarAlchemist/Demerzel",
            "commit": None if drift else PINNED_COMMIT,
            "commit_check": ("FAILED: " + "; ".join(drift)) if drift else
                            "every file below has the Git blob id recorded for this commit (CRLF normalised to LF)",
            "files": files,
            "context_files": context_files,
        },
        "feeder_rule": feeder_rule,
        "encoding": {
            "runs": "one entry per distinct timestamp, in time order; every row of a run carries that timestamp",
            "citation_count and delta_citations": "one token per run, separated by one space, aligned with the runs list",
            "flag strings": "one character per run, aligned with the runs list",
            NO_ROW: "the artifact has no row in that run",
            ABSENT: "the row exists and the key is absent (citation_count: the row has no count)",
            "s": "baseline_flag: the row carries baseline: true (a seed row)",
            "r": "rebaseline_flag: rebaseline is true",
            "f": "rebaseline_flag: rebaseline is false",
            "n": "citation_source: the key is present and null",
            "g": "citation_source: git-grep-v1",
        },
        "counts": count_rows(rows, runs) | {"files": len(files), "consecutive_rows": pairs},
        "runs": [{"index": index, "timestamp": timestamp, "rows": run_rows[timestamp]}
                 for index, timestamp in enumerate(runs)],
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
    text = json.dumps(snapshot, ensure_ascii=False, indent=2) + "\n"
    args.output.write_bytes(text.encode("utf-8"))
    counts = snapshot["counts"]
    print(f"extract.py: {counts['rows']} rows, {counts['runs']} runs, {counts['artifacts']} artifacts, "
          f"{counts['consecutive_rows']['pairs_of_consecutive_rows_with_a_count']} pairs of consecutive rows, "
          f"{counts['consecutive_rows']['count_changed']} with a changed count -> {args.output.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
