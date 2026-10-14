#!/usr/bin/env python3
"""PSY-007 extract: snapshot the latest citation counts and what the records say about power laws.

Reads, at the pinned commit:
- state/quality-trend/*.jsonl: the citation_count of every artifact in the
  latest run, and in the last run before the counts were measured with git grep;
- state/evolution/*.evolution.json: the citation paths behind each count;
- the department record and the two published lessons (PSY-001, PSY-002): the
  strings and lines that mention a power law, Pareto or Zipf;
- logic/fractal-compounding.md, which PSY-001 gives as its first source: its
  power-law detection rule and the lines that name the data it applies to.

Writes observed-input.json next to this script. The analysis script reads only
that snapshot, so its results do not move when the nightly feeder appends rows.

Fails with a non-zero exit and a message when a source file is missing, has an
unexpected shape, or is not the file of the pinned commit.

Run from the repository root:
    python -I scripts/streeling_fixtures/psychohistory/psy-007/extract.py
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

# This program lives under scripts/ (CONTRIBUTING.md: no executable code outside scripts/); its data stays
# under state/streeling/fixtures/. FIXTURE_FILE is the path the program would have next to that data.
FIXTURE_FILE = (Path(__file__).resolve().parents[4]
                / "state/streeling/fixtures/psychohistory/psy-007" / Path(__file__).name)

PINNED_COMMIT = "4b03838800dcd4894f1e026461979bff1d985ca8"
# Git blob ids at PINNED_COMMIT (git ls-tree). A blob id is
# sha1(b"blob <size>\0" + content) over the LF-normalised bytes.
PINNED_BLOBS = {
    "state/quality-trend/2026-05.jsonl": "ab1c35d9948c9bfbb1501b20c39b736d92dc0bb2",
    "state/quality-trend/2026-07.jsonl": "57b303ea2ed56d96010345a2acd508bff248486e",
    "state/quality-trend/2026-08.jsonl": "e2b4462797f1ee06f3188154611de0fdbcc07a23",
    "state/quality-trend/2026-09.jsonl": "9b74c1a34378e3f3941c1c0bb054f5b10fe2b64f",
    "state/quality-trend/2026-10.jsonl": "e64c9c855667f2408e1e4f8c894e1be2722afdd1",
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
    "state/streeling/departments/psychohistory.department.json": "67f81dd22dd5c17a6eb41174dd5944475ce2dd6b",
    "state/streeling/courses/psychohistory/en/psy-001-intro-fractal-compounding.md": "e7a8aeb2accc287595829ed672a9d65284c38ffc",
    "state/streeling/courses/psychohistory/en/psy-002-governance-phase-transitions.md": "75867c85b5946ddddab1df93dc7db72b707f1425",
    "logic/fractal-compounding.md": "0d2f259717b203c41eeb247f6d8ee9dec2e8dc62",
}
TREND_DIR = "state/quality-trend"
EVOLUTION_DIR = "state/evolution"
DEPARTMENT = "state/streeling/departments/psychohistory.department.json"
PUBLISHED_LESSONS = (
    "state/streeling/courses/psychohistory/en/psy-001-intro-fractal-compounding.md",
    "state/streeling/courses/psychohistory/en/psy-002-governance-phase-transitions.md",
)
GIT_GREP = "git-grep-v1"
# Case-insensitive; "power law" also matches "power laws", "power-law" its hyphenated form.
TERMS = ("power law", "power-law", "pareto", "zipf")
D_C_FORMULA = "D_c = log(value_ratio) / log(scale_ratio)"
TIMESTAMP = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")
SPECIFICATION = "logic/fractal-compounding.md"
DETECTION_RULE = re.compile(r"^\*\*Detection rule:\*\* (If the top (\d+)% of governance artifacts account for more than "
                            r"(\d+)% of citations, a power law is present\.)")
EVOLUTION_GLOB = "state/evolution/*.evolution.json"
SOURCES_OF_PSY_001 = "- Sources: [Fractal Compounding Spec](../../" + SPECIFICATION + ")"


class ExtractError(Exception):
    """A source file is missing, malformed, or not the pinned one."""


def git_blob_id(data: bytes) -> str:
    """Blob id Git stores for this content once CRLF is normalised to LF."""
    data = data.replace(b"\r\n", b"\n")
    return hashlib.sha1(b"blob %d\x00" % len(data) + data).hexdigest()


def read(root: Path, rel: str, files: dict[str, str]) -> bytes:
    path = root / rel
    if not path.is_file():
        raise ExtractError(f"missing file: {rel}")
    data = path.read_bytes()
    files[rel] = git_blob_id(data)
    return data


def mentions(text: str) -> bool:
    lowered = text.lower()
    return any(term in lowered for term in TERMS)


def label(name: str) -> str:
    """An artifact name or a citation path as a data label: a space on each side of every slash.

    scripts/evolution_metrics.py counts every tracked file that contains an artifact's path as a literal string.
    Written this way, the snapshot is not such a file and does not raise the counts it records.
    """
    return " / ".join(name.split("/")).rstrip()


def read_trend(root: Path, files: dict[str, str]) -> list[dict]:
    trend = root / TREND_DIR
    if not trend.is_dir():
        raise ExtractError(f"missing directory: {TREND_DIR}")
    paths = sorted(trend.glob("*.jsonl"))
    if not paths:
        raise ExtractError(f"no *.jsonl file in {TREND_DIR}")
    rows, seen, previous_timestamp = [], set(), ""
    for path in paths:
        rel = path.relative_to(root).as_posix()
        for number, line in enumerate(read(root, rel, files).decode("utf-8").splitlines(), 1):
            where = f"{rel}:{number}"
            try:
                row = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ExtractError(f"{where}: not JSON ({exc})") from exc
            if not isinstance(row, dict):
                raise ExtractError(f"{where}: not a JSON object")
            timestamp, artifact = row.get("timestamp"), row.get("artifact")
            if not isinstance(timestamp, str) or not TIMESTAMP.match(timestamp):
                raise ExtractError(f"{where}: unexpected timestamp {timestamp!r}")
            if timestamp < previous_timestamp:
                raise ExtractError(f"{where}: timestamp {timestamp} is earlier than the row before it")
            previous_timestamp = timestamp
            if not isinstance(artifact, str) or not artifact:
                raise ExtractError(f"{where}: unexpected artifact {artifact!r}")
            if (timestamp, artifact) in seen:
                raise ExtractError(f"{where}: second row for {artifact!r} at {timestamp}")
            seen.add((timestamp, artifact))
            rows.append({"where": where, "timestamp": timestamp, "artifact": artifact,
                         "has_count": "citation_count" in row, "count": row.get("citation_count"),
                         "source": row.get("citation_source"), "rebaseline": row.get("rebaseline")})
    return rows


def counts_of(run: list[dict], label: str) -> dict[str, int]:
    """artifact -> citation_count for one run; every row must carry a non-negative integer."""
    counts = {}
    for row in run:
        count = row["count"]
        if not row["has_count"] or isinstance(count, bool) or not isinstance(count, int) or count < 0:
            raise ExtractError(f"{row['where']}: {label} has no usable citation_count ({count!r})")
        counts[row["artifact"]] = count
    return counts


def read_evolution(root: Path, files: dict[str, str]) -> dict[str, dict]:
    """artifact -> its evolution record (exactly one record per artifact expected)."""
    folder = root / EVOLUTION_DIR
    if not folder.is_dir():
        raise ExtractError(f"missing directory: {EVOLUTION_DIR}")
    records: dict[str, dict] = {}
    for path in sorted(folder.glob("*.evolution.json")):
        rel = path.relative_to(root).as_posix()
        try:
            record = json.loads(read(root, rel, files).decode("utf-8"))
        except json.JSONDecodeError as exc:
            raise ExtractError(f"{rel}: not JSON ({exc})") from exc
        artifact = record.get("artifact") if isinstance(record, dict) else None
        if not isinstance(artifact, str) or not artifact:
            raise ExtractError(f"{rel}: no artifact name")
        if artifact in records:
            raise ExtractError(f"{rel}: second evolution record for {artifact!r}")
        metrics = record.get("metrics")
        if not isinstance(metrics, dict):
            raise ExtractError(f"{rel}: no metrics object")
        declared = "citation_paths" in record
        paths = record["citation_paths"] if declared else [artifact]
        if not isinstance(paths, list) or not all(isinstance(p, str) and p for p in paths):
            raise ExtractError(f"{rel}: unexpected citation_paths {paths!r}")
        records[artifact] = {"path": rel, "citation_paths": paths, "declared": declared,
                             "count": metrics.get("citation_count"), "source": metrics.get("citation_source")}
    return records


def department_mentions(root: Path, files: dict[str, str]) -> list[dict]:
    """Every string of the department record that mentions a power law, with its JSON path and line."""
    raw = read(root, DEPARTMENT, files).decode("utf-8")
    lines = raw.splitlines()
    found = []

    def walk(node, path):
        if isinstance(node, dict):
            for key, value in node.items():
                walk(value, f"{path}.{key}" if path else key)
        elif isinstance(node, list):
            for index, value in enumerate(node):
                walk(value, f"{path}[{index}]")
        elif isinstance(node, str) and mentions(node):
            encoded = json.dumps(node, ensure_ascii=False)
            hits = [number for number, line in enumerate(lines, 1) if encoded in line]
            if len(hits) != 1:
                raise ExtractError(f"{DEPARTMENT}: {path} is not on exactly one line ({hits})")
            found.append({"json_path": path, "line": hits[0], "text": node})

    walk(json.loads(raw), "")
    by_line = sum(mentions(line) for line in lines)
    if by_line != len(found):
        raise ExtractError(f"{DEPARTMENT}: {len(found)} strings mention a power law but {by_line} lines do")
    return found


def lesson_mentions(root: Path, rel: str, files: dict[str, str]) -> dict:
    lines = read(root, rel, files).decode("utf-8").splitlines()
    matching = [number for number, line in enumerate(lines, 1) if mentions(line)]
    return {"path": rel, "lines": len(lines), "lines_matching": len(matching), "matching_line_numbers": matching}


def trend_runs(root: Path, files: dict[str, str]) -> dict:
    """The runs of the quality trend: the latest one, the first with git-grep counts and the one before it."""
    rows = read_trend(root, files)
    runs: dict[str, list[dict]] = {}
    for row in rows:
        runs.setdefault(row["timestamp"], []).append(row)
    stamps = sorted(runs)
    latest_stamp = stamps[-1]
    latest_run = runs[latest_stamp]
    latest = counts_of(latest_run, "the latest run")
    for row in latest_run:
        if row["source"] is not None and row["source"] != GIT_GREP:
            raise ExtractError(f"{row['where']}: unexpected citation_source {row['source']!r}")

    with_git_grep = [stamp for stamp in stamps if any(row["source"] == GIT_GREP for row in runs[stamp])]
    if not with_git_grep or with_git_grep[0] == stamps[0]:
        raise ExtractError("no run before the first run that carries git-grep-v1 counts")
    first_measured = with_git_grep[0]
    before_stamp = stamps[stamps.index(first_measured) - 1]
    before = counts_of(runs[before_stamp], "the last run before git-grep-v1")
    if set(before) != set(latest):
        raise ExtractError("the last run before git-grep-v1 does not list the artifacts of the latest run")

    same = 0
    for stamp in reversed(stamps):
        run = runs[stamp]
        if all(row["has_count"] for row in run) and {row["artifact"]: row["count"] for row in run} == latest:
            same += 1
        else:
            break

    first_measured_run = runs[first_measured]
    summary = {
        "rows": len(rows),
        "runs": len(stamps),
        "artifacts": len({row["artifact"] for row in rows}),
        "latest_run": {
            "timestamp": latest_stamp,
            "rows": len(latest_run),
            "first_row": latest_run[0]["where"],
            "last_row": latest_run[-1]["where"],
            "consecutive_runs_ending_here_with_these_counts": same,
            "first_of_those_runs": stamps[-same],
        },
        "first_run_with_git_grep_counts": {
            "timestamp": first_measured,
            "rows": len(first_measured_run),
            "rows_with_citation_source_git_grep_v1": sum(row["source"] == GIT_GREP for row in first_measured_run),
            "rows_flagged_rebaseline": sum(row["rebaseline"] is True for row in first_measured_run),
        },
        "last_run_before_git_grep_counts": {"timestamp": before_stamp, "rows": len(runs[before_stamp])},
    }
    return {"latest_run": latest_run, "latest": latest, "before": before, "summary": summary}


def citation_table(root: Path, files: dict[str, str], trend: dict) -> tuple[list[dict], list[dict]]:
    """One entry per artifact of the latest run, checked against its evolution record, and the shared citation paths."""
    latest_run, latest, before = trend["latest_run"], trend["latest"], trend["before"]
    evolution = read_evolution(root, files)
    if set(evolution) != set(latest):
        raise ExtractError("the evolution records and the latest run do not list the same artifacts: "
                           + ", ".join(sorted(set(evolution) ^ set(latest))))
    citation_counts, by_path = [], {}
    for row in latest_run:
        record = evolution[row["artifact"]]
        if record["count"] != row["count"] or record["source"] != row["source"]:
            raise ExtractError(f"{row['where']}: count {row['count']} ({row['source']}) differs from "
                               f"{record['path']}: {record['count']} ({record['source']})")
        if row["source"] == GIT_GREP and not record["citation_paths"]:
            raise ExtractError(f"{record['path']}: measured with git grep but has no citation path")
        if row["source"] is None and record["citation_paths"]:
            raise ExtractError(f"{record['path']}: has citation paths but no citation_source")
        for path in record["citation_paths"]:
            by_path.setdefault(path, []).append(row["artifact"])
        citation_counts.append({
            "artifact": label(row["artifact"]), "citation_count": row["count"], "citation_source": row["source"],
            "row": row["where"], "count_before_git_grep": before[row["artifact"]],
            "evolution_record": record["path"], "citation_paths_declared": record["declared"],
            "citation_paths": [label(path) for path in record["citation_paths"]],
        })
    shared = [{"citation_path": label(path), "artifacts": [label(artifact) for artifact in artifacts],
               "artifacts_that_list_it_in_citation_paths": [label(a) for a in artifacts if evolution[a]["declared"]],
               "artifacts_counted_on_their_own_name": [label(a) for a in artifacts if not evolution[a]["declared"]]}
              for path, artifacts in sorted(by_path.items()) if len(artifacts) > 1]
    return citation_counts, shared


def mentions_and_formula(root: Path, files: dict[str, str]) -> tuple[dict, dict]:
    """Where the department record and the two published lessons mention a power law, and the D_c formula of PSY-001."""
    department = department_mentions(root, files)
    lessons = [lesson_mentions(root, rel, files) for rel in PUBLISHED_LESSONS]
    psy_001 = read(root, PUBLISHED_LESSONS[0], files).decode("utf-8").splitlines()
    formula_lines = [number for number, line in enumerate(psy_001, 1) if line.strip() == D_C_FORMULA]
    if len(formula_lines) != 1:
        raise ExtractError(f"{PUBLISHED_LESSONS[0]}: the D_c formula is on {len(formula_lines)} lines, expected 1")
    found = {
        "terms_searched_case_insensitive": list(TERMS),
        "department_record": {"path": DEPARTMENT, "strings": department},
        "published_lessons": lessons,
        "search_control": "the same search finds %d strings in the department record, so a count of 0 "
                          "in a lesson is not a search that matches nothing" % len(department),
    }
    return found, {"path": PUBLISHED_LESSONS[0], "line": formula_lines[0], "text": D_C_FORMULA}


def specification_rule(root: Path, files: dict[str, str]) -> dict:
    """The power-law detection rule of the specification that PSY-001 gives as its first source, and its data."""
    lines = read(root, SPECIFICATION, files).decode("utf-8").splitlines()
    rules = [(number, DETECTION_RULE.match(line)) for number, line in enumerate(lines, 1) if DETECTION_RULE.match(line)]
    if len(rules) != 1:
        raise ExtractError(f"{SPECIFICATION}: the detection rule is on {len(rules)} lines, expected 1")
    number, match = rules[0]
    data = [{"line": n, "text": line.strip()} for n, line in enumerate(lines, 1) if EVOLUTION_GLOB in line]
    if not data:
        raise ExtractError(f"{SPECIFICATION}: no line names {EVOLUTION_GLOB}")
    psy_001 = read(root, PUBLISHED_LESSONS[0], files).decode("utf-8").splitlines()
    cited = [n for n, line in enumerate(psy_001, 1) if line.startswith(SOURCES_OF_PSY_001)]
    if len(cited) != 1:
        raise ExtractError(f"{PUBLISHED_LESSONS[0]}: the specification opens {len(cited)} Sources lines, expected 1")
    return {
        "path": SPECIFICATION,
        "detection_rule": {"line": number, "text": match.group(1),
                           "top_percent_of_artifacts": int(match.group(2)),
                           "more_than_percent_of_citations": int(match.group(3))},
        "lines_naming_the_evolution_records": data,
        "first_source_of_psy_001": {"path": PUBLISHED_LESSONS[0], "line": cited[0]},
    }


def build(root: Path, allow_drift: bool) -> dict:
    files: dict[str, str] = {}
    trend = trend_runs(root, files)
    citation_counts, shared = citation_table(root, files, trend)
    found, formula = mentions_and_formula(root, files)
    rule = specification_rule(root, files)

    drift = [f"{path} is blob {blob}, pinned {PINNED_BLOBS.get(path)}"
             for path, blob in sorted(files.items()) if PINNED_BLOBS.get(path) != blob]
    drift += [f"{path} is pinned but was not read" for path in sorted(set(PINNED_BLOBS) - set(files))]
    if drift and not allow_drift:
        raise ExtractError("source files are not those of commit " + PINNED_COMMIT + ":\n  " + "\n  ".join(drift)
                           + "\n(--allow-drift snapshots them anyway; the lesson's numbers then no longer apply)")
    return {
        "schema_version": "0.1.0",
        "module_id": "psy-007-power-law-or-not",
        "kind": "observed",
        "labels": "artifact names and citation paths are written with a space on each side of every slash, so that "
                  "this file is not counted as a citation of the artifacts it lists",
        "source": {
            "repository": "GuitarAlchemist/Demerzel",
            "commit": None if drift else PINNED_COMMIT,
            "commit_check": ("FAILED: " + "; ".join(drift)) if drift else
                            "every file below has the Git blob id recorded for this commit (CRLF normalised to LF)",
            "files": [{"path": path, "git_blob": blob} for path, blob in sorted(files.items())],
        },
        "quality_trend": trend["summary"],
        "citation_counts": citation_counts,
        "shared_citation_paths": shared,
        "power_law_mentions": found,
        "psy_001_compounding_dimension": formula,
        "specification_rule": rule,
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
    counts = [entry["citation_count"] for entry in snapshot["citation_counts"]]
    print(f"extract.py: {len(counts)} citation counts from the run of {snapshot['quality_trend']['latest_run']['timestamp']} "
          f"(sum {sum(counts)}, zeros {counts.count(0)}), "
          f"{len(snapshot['power_law_mentions']['department_record']['strings'])} department strings "
          f"-> {args.output.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
