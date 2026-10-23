#!/usr/bin/env python3
"""PSY-011 extract: snapshot the citation counts of the quality trend and how they are produced.

Reads state/quality-trend/*.jsonl (the citation counts, their deltas, the
citation_source field and the rebaseline flag), the two scripts that produce
them (the lines the lesson quotes) and the evolution record of each artifact
(its citation paths and last_cited), and writes observed-input.json next to
this script. The analysis script reads only that snapshot, so its results do
not move when the nightly feeder appends new rows. Artifact names and citation
paths are written as labels (a space on each side of every slash): see label().

Fails with a non-zero exit and a message when a source file is missing, has an
unexpected shape, or is not the file of the pinned commit.

Run from the repository root:
    python -I scripts/streeling_fixtures/psychohistory/psy-011/extract.py
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
                / "state/streeling/fixtures/psychohistory/psy-011" / Path(__file__).name)

PINNED_COMMIT = "4b03838800dcd4894f1e026461979bff1d985ca8"
# Git blob ids at PINNED_COMMIT (git ls-tree -r <commit> -- <path>). A blob id
# is sha1(b"blob <size>\0" + content) over the LF-normalised bytes.
PINNED_BLOBS = {
    "state/quality-trend/2026-05.jsonl": "ab1c35d9948c9bfbb1501b20c39b736d92dc0bb2",
    "state/quality-trend/2026-07.jsonl": "57b303ea2ed56d96010345a2acd508bff248486e",
    "state/quality-trend/2026-08.jsonl": "e2b4462797f1ee06f3188154611de0fdbcc07a23",
    "state/quality-trend/2026-09.jsonl": "9b74c1a34378e3f3941c1c0bb054f5b10fe2b64f",
    "state/quality-trend/2026-10.jsonl": "e64c9c855667f2408e1e4f8c894e1be2722afdd1",
    "scripts/quality_trend.py": "6180a21d72e1c4f4c89197e701e202dce079b5a8",
    "scripts/evolution_metrics.py": "024da5615525dbd351265dfdb2f9040485e77b7f",
    "state/evolution/2026-03-17-alignment-policy.evolution.json": "c8dbaeda5c8bf1b8fe063f9828c86e39df718a9d",
    "state/evolution/2026-03-17-asimov-constitution.evolution.json": "7c7915e2bd167b2959cfa32ee69632b12273fe57",
    "state/evolution/2026-03-17-default-constitution.evolution.json": "589a32f81d53181a64eec9a62e15777ba3d39010",
    "state/evolution/2026-03-18-compounding-cycle.evolution.json": "ce24deb5744ae454cb40c9f80fddf237d313d9bf",
    "state/evolution/2026-03-20-autonomous-driver.evolution.json": "8465478632590e1679ec93c725d5383f8b67e2ab",
    "state/evolution/2026-03-20-memristive-markov.evolution.json": "32686dbbc6c42df9bb19a7e8afec99cdd63b5a58",
    "state/evolution/2026-04-03-visual-governance.evolution.json": "5df5099a57099363c4e317dafe0dcac495ac0005",
    "state/evolution/2026-04-30-hari-subjective-logic.evolution.json": "979b7a14153c94134d8cf65770f2d027132a2850",
    "state/evolution/2026-04-30-harness-engineering.evolution.json": "8ff229fd4b018cbbee5f84034907c6ce607371d2",
    "state/evolution/2026-04-30-ix-autoresearch.evolution.json": "ef399e0139f95ed407906a7246065e39158a2ea3",
    "state/evolution/2026-04-30-the-sentinel.evolution.json": "ce0702627a6c588b0e53751bdb7d3384c57b381b",
    "state/evolution/2026-06-21-ml-feedback-loop.evolution.json": "0c0bdf6c1853d92c6878bc2caee732ac092507ad",
    "state/evolution/2026-06-24-afk-self-merge.evolution.json": "c996d0b573bfe50de90e2f9a51e65c4d073f43ab",
    "state/evolution/2026-07-23-galactic-v1.3-ratification.evolution.json": "7184c7d18ddd23ae1dfc7e71a1860cf7b4bc02d4",
    "state/evolution/2026-07-25-governance-evolution-schema.evolution.json": "4b2340c05df5428c58801d59c22b9b0a8ad09610",
    "state/evolution/2026-07-25-kaizen-pdca-schema.evolution.json": "967b0654efc0ee9d679ff8a0363cc309dccd3065",
    "state/evolution/2026-07-25-loop-state-schema.evolution.json": "1e1c7958fa9ad25f3d67f5e87aa339dbf107cfa4",
    "state/evolution/2026-07-29-afk-backend-adapter.evolution.json": "006f862a2a2a6025a7435c4c9a3b53b854ba773e",
}
TREND_DIR = "state/quality-trend"
EVOLUTION_DIR = "state/evolution"
# The lines the lesson quotes: (path, first line, last line, {line: text it must contain}).
# The fragments are checked even with --allow-drift: a snapshot whose code no
# longer says this cannot carry the lesson's reading of a rebaseline.
CODE_QUOTES = (
    ("scripts/quality_trend.py", 14, 18, {
        14: "REBASELINE: each line records the metrics' citation_source.",
        17: "rebaseline: true and delta_citations 0"}),
    ("scripts/quality_trend.py", 75, 76, {
        76: 'citation = int(metrics.get("citation_count", 0) or 0)'}),
    ("scripts/quality_trend.py", 90, 92, {
        90: "prev = previous.get(artifact, {})",
        91: 'source = metrics.get("citation_source")',
        92: 'rebaseline = bool(prev) and prev.get("citation_source") != source'}),
    ("scripts/quality_trend.py", 96, 96, {
        96: '"citation_count": citation,'}),
    ("scripts/quality_trend.py", 99, 99, {
        99: '"delta_citations": 0 if rebaseline else citation - int(prev.get("citation_count", 0) or 0),'}),
    ("scripts/quality_trend.py", 106, 107, {
        106: '"citation_source": source,',
        107: '"rebaseline": rebaseline,'}),
    ("scripts/evolution_metrics.py", 4, 8, {
        4: "Until 2026-09 every evolution metric was typed by hand",
        7: "The hand counts were also not measurements"}),
    ("scripts/evolution_metrics.py", 12, 15, {
        12: "citation_count  tracked files that mention any of the artifact's citation",
        13: "`git grep -lF`"}),
    ("scripts/evolution_metrics.py", 20, 23, {
        20: "Citation paths are the entry's `citation_paths` list when present",
        21: "An explicit empty list marks an"}),
    ("scripts/evolution_metrics.py", 26, 27, {
        26: "It stamps metrics.citation_source so quality_trend.py",
        27: "can mark the first computed value as a rebaseline instead of a real jump."}),
    ("scripts/evolution_metrics.py", 42, 43, {
        42: 'CITATION_SOURCE = "git-grep-v1"',
        43: "EXCLUDED = ("}),
    ("scripts/evolution_metrics.py", 80, 82, {
        80: 'git(root, "grep", "-lF", "-e", p, "--", ".", *EXCLUDED)',
        81: "not owned_by(ref, paths)"}),
    ("scripts/evolution_metrics.py", 104, 107, {
        104: '"citation_source": CITATION_SOURCE',
        107: "metrics.update(new)"}),
)
TIMESTAMP = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")
NO_ROW, ABSENT, NULL = ".", "-", "n"
SOURCE_LETTERS = "abcdefghij"


class ExtractError(Exception):
    """A source file is missing, malformed, or not the pinned one."""


def git_blob_id(data: bytes) -> str:
    """Blob id Git stores for this content once CRLF is normalised to LF."""
    data = data.replace(b"\r\n", b"\n")
    return hashlib.sha1(b"blob %d\x00" % len(data) + data).hexdigest()


def is_count(value: object) -> bool:
    return isinstance(value, int) and not isinstance(value, bool)


def label(name: str) -> str:
    """An artifact name or a citation path as a data label: a space on each side of every slash.

    scripts/evolution_metrics.py counts every tracked file that contains one of an artifact's citation paths as
    a literal string. Written this way, the snapshot is not such a file and does not raise the counts it records.
    Every name goes through this one function, whether it is a plain path or not: a name without a slash is
    unchanged, and a trailing slash stays as " /".
    """
    return " / ".join(name.split("/")).rstrip()


def read_bytes(root: Path, rel: str) -> bytes:
    path = root / rel
    if not path.is_file():
        raise ExtractError(f"missing file: {rel}")
    return path.read_bytes()


def read_rows(root: Path) -> tuple[list[dict], list[dict]]:
    """Every row of the quality trend with the fields the lesson uses, and one entry per file read."""
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
            for key in ("timestamp", "artifact", "delta_citations"):
                if key not in row:
                    raise ExtractError(f"{where}: missing key {key!r}")
            timestamp, artifact = row["timestamp"], row["artifact"]
            if not isinstance(timestamp, str) or not TIMESTAMP.match(timestamp):
                raise ExtractError(f"{where}: unexpected timestamp {timestamp!r}")
            datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
            if timestamp[:7] != path.stem:
                raise ExtractError(f"{where}: timestamp {timestamp} is not in month file {path.name}")
            if timestamp < previous_timestamp:
                raise ExtractError(f"{where}: timestamp {timestamp} is earlier than the row before it")
            previous_timestamp = timestamp
            if not isinstance(artifact, str) or not artifact:
                raise ExtractError(f"{where}: unexpected artifact {artifact!r}")
            if (timestamp, artifact) in seen:
                raise ExtractError(f"{where}: second row for {artifact!r} at {timestamp}")
            seen.add((timestamp, artifact))
            if not is_count(row["delta_citations"]):
                raise ExtractError(f"{where}: unexpected delta_citations {row['delta_citations']!r}")
            baseline = row.get("baseline", False)
            if not isinstance(baseline, bool):
                raise ExtractError(f"{where}: unexpected baseline flag {baseline!r}")
            has_count = "citation_count" in row
            if has_count and (not is_count(row["citation_count"]) or row["citation_count"] < 0):
                raise ExtractError(f"{where}: unexpected citation_count {row['citation_count']!r}")
            if not has_count and not baseline:
                raise ExtractError(f"{where}: no citation_count in a row that is not flagged baseline")
            has_source = "citation_source" in row
            if has_source != ("rebaseline" in row):
                raise ExtractError(f"{where}: citation_source and rebaseline are not present together")
            source = row.get("citation_source")
            if source is not None and (not isinstance(source, str) or not source):
                raise ExtractError(f"{where}: unexpected citation_source {source!r}")
            if has_source and not isinstance(row["rebaseline"], bool):
                raise ExtractError(f"{where}: unexpected rebaseline flag {row['rebaseline']!r}")
            # "artifact" is what the snapshot shows; "source_name" stays in memory, to keep the artifacts in the
            # order of their names in the repository and to find their evolution records.
            rows.append({
                "file": rel, "line": number, "timestamp": timestamp, "artifact": label(artifact),
                "source_name": artifact,
                "count": row["citation_count"] if has_count else None, "delta": row["delta_citations"],
                "has_source": has_source, "source": source,
                "rebaseline": row["rebaseline"] if has_source else None, "baseline": baseline,
            })
        files.append({"path": rel, "git_blob": git_blob_id(data), "rows": len(lines)})
    return rows, files


def read_code(root: Path) -> tuple[list[dict], list[dict]]:
    """The quoted line ranges of the two scripts, with a check of what they say."""
    scripts, quotes, cache = [], [], {}
    for rel, first, last, fragments in CODE_QUOTES:
        if rel not in cache:
            data = read_bytes(root, rel)
            cache[rel] = data.decode("utf-8").splitlines()
            scripts.append({"path": rel, "git_blob": git_blob_id(data), "lines": len(cache[rel])})
        lines = cache[rel]
        if last > len(lines):
            raise ExtractError(f"{rel}: has {len(lines)} lines, the lesson quotes lines {first}-{last}")
        for number, fragment in fragments.items():
            if fragment not in lines[number - 1]:
                raise ExtractError(f"{rel}:{number}: expected to read {fragment!r}, found {lines[number - 1].strip()!r}")
        quotes.append({"path": rel, "first_line": first, "last_line": last, "text": lines[first - 1:last]})
    return scripts, quotes


def read_evolution(root: Path, artifacts: set[str]) -> tuple[dict[str, dict], list[dict]]:
    """One evolution record per artifact of the trend: its citation paths and metrics."""
    folder = root / EVOLUTION_DIR
    if not folder.is_dir():
        raise ExtractError(f"missing directory: {EVOLUTION_DIR}")
    records, files = {}, []
    for path in sorted(folder.glob("*.evolution.json")):
        rel = path.relative_to(root).as_posix()
        data = path.read_bytes()
        try:
            record = json.loads(data.decode("utf-8"))
        except json.JSONDecodeError as exc:
            raise ExtractError(f"{rel}: not JSON ({exc})") from exc
        if not isinstance(record, dict) or not isinstance(record.get("artifact"), str):
            raise ExtractError(f"{rel}: no artifact name")
        name, metrics = record["artifact"], record.get("metrics")
        if name not in artifacts:
            raise ExtractError(f"{rel}: artifact {name!r} has no row in the quality trend")
        if name in records:
            raise ExtractError(f"{rel}: second evolution record for {name!r}")
        if not isinstance(metrics, dict) or not is_count(metrics.get("citation_count")):
            raise ExtractError(f"{rel}: metrics.citation_count is not an integer")
        paths = record.get("citation_paths")
        if paths is not None and not (isinstance(paths, list) and all(isinstance(p, str) and p for p in paths)):
            raise ExtractError(f"{rel}: unexpected citation_paths {paths!r}")
        source, last_cited = metrics.get("citation_source"), metrics.get("last_cited")
        if source is not None and (not isinstance(source, str) or not source):
            raise ExtractError(f"{rel}: unexpected metrics.citation_source {source!r}")
        if last_cited is not None and not (isinstance(last_cited, str) and TIMESTAMP.match(last_cited)):
            raise ExtractError(f"{rel}: unexpected metrics.last_cited {last_cited!r}")
        records[name] = {"path": rel, "citation_paths": None if paths is None else [label(p) for p in paths],
                         "citation_count": metrics["citation_count"], "citation_source": source,
                         "last_cited": last_cited}
        files.append({"path": rel, "git_blob": git_blob_id(data)})
    missing = sorted(artifacts - set(records))
    if missing:
        raise ExtractError(f"no evolution record for: {', '.join(missing)}")
    return records, files


def source_letters(rows: list[dict]) -> dict[str, str]:
    """citation_source value -> the letter that stands for it in the snapshot, in order of first appearance."""
    letters: dict[str, str] = {}
    for row in rows:
        if row["source"] is not None and row["source"] not in letters:
            if len(letters) == len(SOURCE_LETTERS):
                raise ExtractError("more distinct citation_source values than this snapshot can encode")
            letters[row["source"]] = SOURCE_LETTERS[len(letters)]
    return letters


def artifact_entry(series: list[dict], run_index: dict[str, int], letters: dict[str, str], record: dict) -> dict:
    """One artifact of the snapshot: five columns aligned with the runs, and its evolution record."""
    cells = {key: [NO_ROW] * len(run_index) for key in ("count", "delta", "source", "rebaseline", "seed")}
    for row in series:
        index = run_index[row["timestamp"]]
        cells["count"][index] = ABSENT if row["count"] is None else str(row["count"])
        cells["delta"][index] = str(row["delta"])
        cells["source"][index] = (ABSENT if not row["has_source"] else NULL if row["source"] is None
                                  else letters[row["source"]])
        cells["rebaseline"][index] = ABSENT if row["rebaseline"] is None else "t" if row["rebaseline"] else "f"
        cells["seed"][index] = "s" if row["baseline"] else ABSENT
    return {
        "name": series[0]["artifact"], "rows": len(series), "first_run_index": run_index[series[0]["timestamp"]],
        "citation_count": " ".join(cells["count"]), "delta_citations": " ".join(cells["delta"]),
        "citation_source": "".join(cells["source"]), "rebaseline": "".join(cells["rebaseline"]),
        "baseline_flag": "".join(cells["seed"]), "evolution_record": record,
    }


def source_drift(entries: list[dict]) -> list[str]:
    """One message per file read that is not its pinned blob, and per pinned file that was not read."""
    drift = []
    for entry in entries:
        if PINNED_BLOBS.get(entry["path"]) != entry["git_blob"]:
            drift.append(f"{entry['path']} is blob {entry['git_blob']}, pinned {PINNED_BLOBS.get(entry['path'])}")
    drift += [f"{path} is pinned but was not read" for path in sorted(set(PINNED_BLOBS) - {e["path"] for e in entries})]
    return drift


def source_section(files: list[dict], scripts: list[dict], evolution_files: list[dict], drift: list[str]) -> dict:
    """The 'source' section: the files read, and the pinned commit unless one of them drifted from it."""
    return {
        "repository": "GuitarAlchemist/Demerzel",
        "commit": None if drift else PINNED_COMMIT,
        "commit_check": ("FAILED: " + "; ".join(drift)) if drift else
                        "every file below has the Git blob id recorded for this commit (CRLF normalised to LF)",
        "files": files,
        "scripts": scripts,
        "evolution_records": evolution_files,
    }


def encoding_section(letters: dict[str, str]) -> dict:
    """The 'encoding' section: how to read the runs list and the per-artifact columns."""
    return {
        "runs": "one entry per distinct timestamp, in time order; every row of a run carries that timestamp",
        "citation_count, delta_citations": "one token per run, separated by single spaces, aligned with the runs list",
        "citation_source, rebaseline, baseline_flag": "one character per run, aligned with the runs list",
        NO_ROW: "the artifact has no row in that run",
        ABSENT: "the row exists and does not have the key (for baseline_flag: the flag is absent)",
        NULL: "citation_source only: the key is present and its value is null",
        "t, f": "rebaseline only: true, false",
        "s": "baseline_flag only: the row carries baseline: true",
        "citation_source_values": {letter: value for value, letter in letters.items()},
    }


def counts_section(rows: list[dict], files: list[dict], runs: list[str], artifacts: int, records: int,
                   letters: dict[str, str]) -> dict:
    """The 'counts' section: what analyze.py recounts from the columns through a second code path."""
    by_source = {"key absent": 0, "null": 0} | {value: 0 for value in letters}
    by_flag = {"key absent": 0, "true": 0, "false": 0}
    for row in rows:
        by_source["key absent" if not row["has_source"] else "null" if row["source"] is None else row["source"]] += 1
        by_flag["key absent" if row["rebaseline"] is None else "true" if row["rebaseline"] else "false"] += 1
    return {
        "rows": len(rows),
        "files": len(files),
        "runs": len(runs),
        "run_dates_utc": len({timestamp[:10] for timestamp in runs}),
        "artifacts": artifacts,
        "evolution_records": records,
        "rows_flagged_baseline": sum(row["baseline"] for row in rows),
        "rows_without_citation_count": sum(row["count"] is None for row in rows),
        "rows_by_citation_source": by_source,
        "rows_by_rebaseline_flag": by_flag,
        "rows_with_nonzero_delta_citations": sum(row["delta"] != 0 for row in rows),
    }


def run_entries(rows: list[dict], run_index: dict[str, int]) -> list[dict]:
    """One entry per run in time order: its index, its timestamp and its number of rows."""
    run_rows = [0] * len(run_index)
    for row in rows:
        run_rows[run_index[row["timestamp"]]] += 1
    return [{"index": index, "timestamp": timestamp, "rows": run_rows[index]} for timestamp, index in run_index.items()]


def build(root: Path, allow_drift: bool) -> dict:
    """The snapshot written to observed-input.json; raises ExtractError on a source that is not the pinned one."""
    rows, files = read_rows(root)
    scripts, quotes = read_code(root)
    runs = sorted({row["timestamp"] for row in rows})
    run_index = {timestamp: index for index, timestamp in enumerate(runs)}
    by_artifact: dict[str, list[dict]] = {}
    for row in rows:
        by_artifact.setdefault(row["source_name"], []).append(row)
    if len({series[0]["artifact"] for series in by_artifact.values()}) != len(by_artifact):
        raise ExtractError("two artifact names give the same label")
    records, evolution_files = read_evolution(root, set(by_artifact))
    letters = source_letters(rows)
    drift = source_drift(files + scripts + evolution_files)
    if drift and not allow_drift:
        raise ExtractError("source files are not those of commit " + PINNED_COMMIT + ":\n  " + "\n  ".join(drift)
                           + "\n(--allow-drift snapshots them anyway; the lesson's numbers then no longer apply)")
    return {
        "schema_version": "0.1.0",
        "module_id": "psy-011-measurement-change-or-system-change",
        "kind": "observed",
        "labels": "artifact names and citation paths are written with a space on each side of every slash, so that "
                  "this file is not counted as a citation of the artifacts it lists",
        "source": source_section(files, scripts, evolution_files, drift),
        "encoding": encoding_section(letters),
        "counts": counts_section(rows, files, runs, len(by_artifact), len(records), letters),
        "code_quotes": quotes,
        "runs": run_entries(rows, run_index),
        "artifacts": [artifact_entry(by_artifact[name], run_index, letters, records[name])
                      for name in sorted(by_artifact)],
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
    except (ExtractError, OSError, UnicodeDecodeError) as exc:
        print(f"extract.py: {exc}", file=sys.stderr)
        return 1
    text = json.dumps(snapshot, ensure_ascii=False, indent=2) + "\n"
    args.output.write_bytes(text.encode("utf-8"))
    counts = snapshot["counts"]
    print(f"extract.py: {counts['rows']} rows, {counts['runs']} runs, {counts['artifacts']} artifacts, "
          f"{counts['rows_by_rebaseline_flag']['true']} rebaseline rows, "
          f"{counts['rows_with_nonzero_delta_citations']} non-zero delta_citations -> {args.output.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
