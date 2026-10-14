#!/usr/bin/env python3
"""Extract the recorded quality trend into observed-input.json for PSY-012.

Reads state/quality-trend/*.jsonl from a Demerzel checkout at the pinned commit and
writes, for each governance artifact, its three numeric series in run order
(citation_count, violation_count, compliance_rate) as run-length segments.

The script fails with a non-zero exit and a message when a source file is missing,
when a file does not match the Git blob recorded for the pinned commit, or when a
row does not have the expected shape. It uses no clock and no random numbers.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path


HERE = Path(__file__).resolve().parent
DEFAULT_REPO = HERE.parents[4]
DEFAULT_OUTPUT = HERE / "observed-input.json"

SOURCE_REPOSITORY = "GuitarAlchemist/Demerzel"
SOURCE_COMMIT = "4b03838800dcd4894f1e026461979bff1d985ca8"
SOURCE_FOLDER = "state/quality-trend"
# Git blob ids at SOURCE_COMMIT, from: git ls-tree 4b03838800dcd4894f1e026461979bff1d985ca8 state/quality-trend/
PINNED_BLOBS = {
    "state/quality-trend/2026-05.jsonl": "ab1c35d9948c9bfbb1501b20c39b736d92dc0bb2",
    "state/quality-trend/2026-07.jsonl": "57b303ea2ed56d96010345a2acd508bff248486e",
    "state/quality-trend/2026-08.jsonl": "e2b4462797f1ee06f3188154611de0fdbcc07a23",
    "state/quality-trend/2026-09.jsonl": "9b74c1a34378e3f3941c1c0bb054f5b10fe2b64f",
    "state/quality-trend/2026-10.jsonl": "e64c9c855667f2408e1e4f8c894e1be2722afdd1",
}
NUMERIC_FIELDS = ("citation_count", "violation_count", "compliance_rate")
TIMESTAMP = re.compile(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z")


class ExtractError(Exception):
    """A source file is missing, altered, or shaped differently from what this script reads."""


def git_blob_id(content: bytes) -> str:
    """Git's blob id of the content with CRLF line ends normalised to LF.

    A Windows checkout with core.autocrlf=true stores these files with CRLF on disk
    while the repository holds LF; normalising first gives the id Git itself records.
    """
    normalised = content.replace(b"\r\n", b"\n")
    return hashlib.sha1(b"blob %d\x00" % len(normalised) + normalised).hexdigest()


def read_rows(repo: Path) -> tuple[list[dict], list[dict]]:
    folder = repo / SOURCE_FOLDER
    if not folder.is_dir():
        raise ExtractError(f"source folder not found: {folder}")
    present = sorted(f"{SOURCE_FOLDER}/{path.name}" for path in folder.glob("*.jsonl"))
    if present != sorted(PINNED_BLOBS):
        raise ExtractError(
            "the set of quality-trend files differs from the pinned commit: "
            f"expected {sorted(PINNED_BLOBS)}, found {present}"
        )
    files = []
    rows = []
    for relative in sorted(PINNED_BLOBS):
        path = repo / relative
        content = path.read_bytes()
        blob = git_blob_id(content)
        if blob != PINNED_BLOBS[relative]:
            raise ExtractError(
                f"{relative} is not the file of commit {SOURCE_COMMIT}: blob {blob}, expected "
                f"{PINNED_BLOBS[relative]}. The quality trend grows every night; check out the pinned commit."
            )
        month = path.stem
        count = 0
        for number, line in enumerate(content.decode("utf-8").splitlines(), 1):
            if not line.strip():
                raise ExtractError(f"{relative}:{number}: blank line")
            try:
                row = json.loads(line)
            except json.JSONDecodeError as error:
                raise ExtractError(f"{relative}:{number}: not JSON ({error})") from error
            check_row(row, relative, number, month)
            rows.append(row)
            count += 1
        if count == 0:
            raise ExtractError(f"{relative}: no rows")
        files.append({"path": relative, "git_blob": blob, "rows": count})
    return files, rows


def check_row(row: object, relative: str, number: int, month: str) -> None:
    where = f"{relative}:{number}"
    if not isinstance(row, dict):
        raise ExtractError(f"{where}: row is not an object")
    timestamp = row.get("timestamp")
    if not isinstance(timestamp, str) or not TIMESTAMP.fullmatch(timestamp):
        raise ExtractError(f"{where}: timestamp is not YYYY-MM-DDTHH:MM:SSZ: {timestamp!r}")
    if not timestamp.startswith(month):
        raise ExtractError(f"{where}: timestamp {timestamp} is outside the file's month {month}")
    artifact = row.get("artifact")
    if not isinstance(artifact, str) or not artifact:
        raise ExtractError(f"{where}: artifact is not a non-empty string")
    has = [field in row for field in NUMERIC_FIELDS]
    if any(has) and not all(has):
        raise ExtractError(f"{where}: only some of {NUMERIC_FIELDS} are present")
    if all(has):
        for field in ("citation_count", "violation_count"):
            value = row[field]
            if isinstance(value, bool) or not isinstance(value, int) or value < 0:
                raise ExtractError(f"{where}: {field} is not a non-negative integer: {value!r}")
        rate = row["compliance_rate"]
        if isinstance(rate, bool) or not isinstance(rate, (int, float)) or not 0.0 <= rate <= 1.0:
            raise ExtractError(f"{where}: compliance_rate is not a number in [0, 1]: {rate!r}")


def segments(values: list) -> list[list]:
    """Run-length form: [[value, number of consecutive records], ...]."""
    out: list[list] = []
    for value in values:
        if out and out[-1][0] == value:
            out[-1][1] += 1
        else:
            out.append([value, 1])
    return out


def build(files: list[dict], rows: list[dict]) -> dict:
    seen = set()
    by_artifact: dict[str, list[dict]] = {}
    for row in rows:
        key = (row["timestamp"], row["artifact"])
        if key in seen:
            raise ExtractError(f"duplicate row for {key}")
        seen.add(key)
        by_artifact.setdefault(row["artifact"], []).append(row)
    timestamps = sorted({row["timestamp"] for row in rows})
    artifacts = []
    for name in sorted(by_artifact):
        records = sorted(by_artifact[name], key=lambda row: row["timestamp"])
        measured = [row for row in records if "citation_count" in row]
        if not measured:
            raise ExtractError(f"artifact {name!r} has no row with numeric fields")
        series = {}
        for field in NUMERIC_FIELDS:
            runs = segments([row[field] for row in measured])
            if sum(length for _, length in runs) != len(measured):
                raise ExtractError(f"segment lengths do not add up for {name!r} {field}")
            series[field] = runs
        artifacts.append({
            "artifact": name,
            "rows": len(records),
            "rows_with_numeric_fields": len(measured),
            "first_measured_timestamp": measured[0]["timestamp"],
            "last_measured_timestamp": measured[-1]["timestamp"],
            "measured_timestamps": [row["timestamp"] for row in measured],
            "segments": series,
        })
    with_numbers = sum(item["rows_with_numeric_fields"] for item in artifacts)
    if sum(item["rows"] for item in artifacts) != len(rows):
        raise ExtractError("rows per artifact do not add up to the row total")
    return {
        "schema_version": "0.1.0",
        "kind": "observed",
        "source_repository": SOURCE_REPOSITORY,
        "source_commit": SOURCE_COMMIT,
        "source_files": files,
        "blob_note": "git_blob is Git's blob id of each file with CRLF normalised to LF; "
                     "compare with: git ls-tree " + SOURCE_COMMIT + " " + SOURCE_FOLDER + "/",
        "definitions": {
            "row": "one line of a source file: one artifact measured in one run",
            "run": "one distinct timestamp",
            "day": "one distinct UTC date among the timestamps",
            "segments": "[value, number of consecutive measured rows holding it], in timestamp order",
            "rows_with_numeric_fields": "rows that carry citation_count, violation_count and compliance_rate "
                                        "(the 2026-05 baseline rows carry only deltas and labels)",
        },
        "counts": {
            "rows": len(rows),
            "rows_with_numeric_fields": with_numbers,
            "rows_without_numeric_fields": len(rows) - with_numbers,
            "runs": len(timestamps),
            "days": len({stamp[:10] for stamp in timestamps}),
            "artifacts": len(artifacts),
            "first_timestamp": timestamps[0],
            "last_timestamp": timestamps[-1],
        },
        "artifacts": artifacts,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", "--repo", dest="repo", type=Path, default=DEFAULT_REPO, help="root of the Demerzel checkout")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    try:
        files, rows = read_rows(args.repo)
        result = build(files, rows)
    except (ExtractError, OSError, UnicodeDecodeError) as error:
        print(f"extract.py: {error}", file=sys.stderr)
        return 1
    text = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    with open(args.output, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(text)
    print(f"wrote {args.output} ({result['counts']['rows']} rows, {result['counts']['artifacts']} artifacts)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
