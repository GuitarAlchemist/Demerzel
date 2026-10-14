#!/usr/bin/env python3
"""PSY-013 extract: snapshot the resilience records of the pinned commit.

Reads, at the pinned commit of GuitarAlchemist/Demerzel:

- the four files of state/resilience/ (the history of four "chaos" cycles, and
  three red-team cycle files, which are a second, separate series);
- the two reports in docs/reports/ that score the same injections (the
  chaos-test report of 2026-03-22 and the report of cycle chaos-003);
- the definitions of the resilience score R (CONTEXT.md, the resilience metric
  policy) and the status line of README.md that quotes the four scores;
- the three files that hold the injections (pinned by blob id, not parsed).

Writes observed-input.json next to this script. The analysis script reads only
that snapshot.

Fails with a non-zero exit and a message when a source file is missing, has an
unexpected shape, or is not the file of the pinned commit, and when
state/resilience/ holds a file that the pinned commit does not.

Run from the repository root:
    python -I scripts/streeling_fixtures/psychohistory/psy-013/extract.py
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
                / "state/streeling/fixtures/psychohistory/psy-013" / Path(__file__).name)

PINNED_COMMIT = "4b03838800dcd4894f1e026461979bff1d985ca8"
RESILIENCE_DIR = "state/resilience"
HISTORY = "state/resilience/history.json"
RED_TEAM = tuple(f"state/resilience/2026-03-23-red-team-cycle-00{n}.json" for n in (1, 2, 3))
GLOSSARY = "CONTEXT.md"
README = "README.md"
POLICY = "policies/resilience-metric-policy.yaml"
BASELINE_REPORT = "docs/reports/chaos-test-report.md"
CYCLE_REPORT = "docs/reports/shake-metafix-cycle-001.md"
INJECTION_FILES = ("pipelines/chaos-test.ixql", "policies/chaos-test-policy.yaml", "schemas/chaos-test.schema.json")
# Git blob ids at PINNED_COMMIT (git ls-tree -r <pin> -- <path>).
# A blob id is sha1(b"blob <size>\0" + content) over the LF-normalised bytes.
PINNED_BLOBS = {
    "CONTEXT.md": "7ac28fd9725bc6402f422d1d985f8ba2368592f0",
    "README.md": "efb2701ee3cc91d379d449439b9fadadf030e7f2",
    "docs/reports/chaos-test-report.md": "0d03cabc4427524351771691a2919c8471b6c3e7",
    "docs/reports/shake-metafix-cycle-001.md": "b0e2d5e1491142e6df5638a7e3a96c2497ff09b3",
    "pipelines/chaos-test.ixql": "469a2525e35271594727f9e4b746aa01f6efc377",
    "policies/chaos-test-policy.yaml": "cea1d6db67e3ea912c2c9bad9fe8dd1dcac56593",
    "policies/resilience-metric-policy.yaml": "7ae2460bdfa4b02c215aa9b9f07dd984236ece49",
    "schemas/chaos-test.schema.json": "037443f39900ed8dafced0b8cab4358054981485",
    "state/resilience/2026-03-23-red-team-cycle-001.json": "64cdcaecdc5b7456be4619fa576c90bc08eaf70d",
    "state/resilience/2026-03-23-red-team-cycle-002.json": "6207cd1eb0567dfdb745ce95ebcb790ecbe24ba6",
    "state/resilience/2026-03-23-red-team-cycle-003.json": "427376e34a6e46ac7520999e7c5f64bd6a7c6591",
    "state/resilience/history.json": "ac559fedae2a5761a0bf5aa2cb8187d2f0168772",
}
GLOSSARY_ENTRY = "- **LOLLI / Resilience score (R)**"
README_STATUS = "**Current status:** R = "
TIMESTAMP = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")
DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
RECORD_KEYS = {"timestamp", "cycle_id", "overall_score", "injections_total", "injections_caught", "injections_missed",
               "level_scores", "gaps", "trend", "note"}
RECORD_OPTIONAL = {"automated_tests", "metafixes_applied", "level_deltas"}
GAP_KEYS = {"level", "injection", "expected_detector", "status"}
VERDICTS = ("PASS", "PARTIAL", "FAIL")
BASELINE_COLUMNS = ["#", "Poison", "Level", "Detection Mechanism", "Expected Result", "Actually Detected?"]
BASELINE_VERDICTS = ("YES", "YES (specification-level)", "PARTIAL", "DELAYED", "GAP")
CYCLE_COLUMNS = ["#", "Injection", "Level", "Detector", "Caught?", "Status", "Notes"]
BASELINE_SCORE = re.compile(r"^(\d+)/(\d+) = (\d\.\d+) \(immediate\), (\d+)/(\d+) = (\d\.\d+) \(including spec-level\)$")
CYCLE_SUMMARY = re.compile(r"^(\d+)/(\d+) caught \((\d+)%\), up from (\d+)/(\d+) \((\d+)%\) in ([\w-]+)\.$")
POISON_SOURCE = re.compile(r"^`([^`]+)` \((\d+) injections\)$")


class ExtractError(Exception):
    """A source file is missing, malformed, or not the pinned one."""


def git_blob_id(data: bytes) -> str:
    """Blob id Git stores for this content once CRLF is normalised to LF."""
    data = data.replace(b"\r\n", b"\n")
    return hashlib.sha1(b"blob %d\x00" % len(data) + data).hexdigest()


def need(condition: bool, message: str) -> None:
    if not condition:
        raise ExtractError(message)


def read(root: Path, rel: str) -> bytes:
    path = root / rel
    need(path.is_file(), f"missing file: {rel}")
    return path.read_bytes()


def text_lines(data: bytes, rel: str) -> list[str]:
    try:
        return data.decode("utf-8").replace("\r\n", "\n").split("\n")
    except UnicodeDecodeError as exc:
        raise ExtractError(f"{rel}: not UTF-8 ({exc})") from exc


def load_json(data: bytes, rel: str) -> dict:
    try:
        value = json.loads(data.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ExtractError(f"{rel}: not UTF-8 JSON ({exc})") from exc
    need(isinstance(value, dict), f"{rel}: not a JSON object")
    return value


def is_number(value: object) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def is_count(value: object) -> bool:
    return isinstance(value, int) and not isinstance(value, bool) and value >= 0


# --- state/resilience/history.json ---------------------------------------------

def history_records(history: dict) -> list[dict]:
    rel = HISTORY
    need(isinstance(history.get("metric"), str) and isinstance(history.get("version"), str),
         f"{rel}: metric or version missing")
    records = history.get("records")
    need(isinstance(records, list) and records, f"{rel}: records is not a non-empty list")
    out, seen = [], set()
    for position, record in enumerate(records):
        where = f"{rel}: record {position}"
        need(isinstance(record, dict), f"{where}: not an object")
        keys = set(record)
        need(RECORD_KEYS <= keys, f"{where}: missing keys {sorted(RECORD_KEYS - keys)}")
        need(keys <= RECORD_KEYS | RECORD_OPTIONAL, f"{where}: unexpected keys {sorted(keys - RECORD_KEYS - RECORD_OPTIONAL)}")
        cycle = record["cycle_id"]
        where = f"{rel}: {cycle}"
        need(isinstance(cycle, str) and cycle not in seen, f"{where}: cycle_id missing or repeated")
        seen.add(cycle)
        need(isinstance(record["timestamp"], str) and bool(TIMESTAMP.match(record["timestamp"])),
             f"{where}: unexpected timestamp {record['timestamp']!r}")
        for key in ("injections_total", "injections_caught", "injections_missed"):
            need(is_count(record[key]), f"{where}: {key} is not a count")
        need(record["injections_total"] > 0, f"{where}: no injection")
        need(is_number(record["overall_score"]), f"{where}: overall_score is not a number")
        need(isinstance(record["trend"], str) and isinstance(record["note"], str), f"{where}: trend or note is not text")
        levels = record["level_scores"]
        need(isinstance(levels, dict) and levels and all(is_number(v) for v in levels.values()),
             f"{where}: unexpected level_scores")
        gaps = record["gaps"]
        need(isinstance(gaps, list) and gaps, f"{where}: gaps is not a non-empty list")
        injections = []
        for index, gap in enumerate(gaps):
            need(isinstance(gap, dict) and GAP_KEYS <= set(gap) <= GAP_KEYS | {"note"},
                 f"{where}: gap {index} has unexpected keys")
            need(all(isinstance(gap[key], str) and gap[key] for key in gap), f"{where}: gap {index} holds a non-text value")
            row = {key: gap[key] for key in ("level", "injection", "expected_detector", "status")}
            if "note" in gap:
                row["note"] = gap["note"]
            injections.append(row)
        names = [row["injection"] for row in injections]
        need(len(set(names)) == len(names), f"{where}: an injection name is listed twice")
        metafixes = record.get("metafixes_applied", [])
        need(isinstance(metafixes, list) and all(
            isinstance(fix, dict) and all(isinstance(fix.get(key), str) for key in ("gap", "fix", "level_improved"))
            for fix in metafixes), f"{where}: unexpected metafixes_applied")
        deltas = record.get("level_deltas", {})
        need(isinstance(deltas, dict) and all(
            isinstance(delta, dict) and is_number(delta.get("before")) and is_number(delta.get("after"))
            for delta in deltas.values()), f"{where}: unexpected level_deltas")
        out.append({
            "cycle_id": cycle,
            "timestamp": record["timestamp"],
            "overall_score": record["overall_score"],
            "injections_total": record["injections_total"],
            "injections_caught": record["injections_caught"],
            "injections_missed": record["injections_missed"],
            "trend": record["trend"],
            "keys_not_extracted": sorted(keys & {"automated_tests"}),
            "level_scores": levels,
            "level_deltas": {level: {"before": delta["before"], "after": delta["after"]} for level, delta in deltas.items()},
            "injections": injections,
            "metafixes_applied": [{key: fix[key] for key in ("gap", "fix", "level_improved")} for fix in metafixes],
            "note": record["note"],
        })
    return out


# --- state/resilience/2026-03-23-red-team-cycle-00N.json -------------------------

def red_team_cycle(doc: dict, rel: str) -> dict:
    for key in ("id", "cycle", "date", "evaluator", "policy_version", "protocol_version"):
        need(isinstance(doc.get(key), str) and doc[key], f"{rel}: {key} missing")
    need(is_count(doc.get("scenarios_evaluated")), f"{rel}: scenarios_evaluated is not a count")
    summary = doc.get("results_summary")
    need(isinstance(summary, dict) and set(summary) == {"pass", "partial", "fail"} and all(map(is_count, summary.values())),
         f"{rel}: unexpected results_summary")
    scenarios = doc.get("scenarios")
    need(isinstance(scenarios, list) and scenarios, f"{rel}: scenarios is not a non-empty list")
    rows = []
    for index, scenario in enumerate(scenarios):
        where = f"{rel}: scenario {index}"
        need(isinstance(scenario, dict), f"{where}: not an object")
        need(is_count(scenario.get("test_id")) and isinstance(scenario.get("name"), str), f"{where}: test_id or name missing")
        need(scenario.get("verdict") in VERDICTS, f"{where}: unexpected verdict {scenario.get('verdict')!r}")
        previous, changed = scenario.get("previous_verdict"), scenario.get("changed")
        need(previous is None or previous in VERDICTS, f"{where}: unexpected previous_verdict {previous!r}")
        need(changed is None or isinstance(changed, bool), f"{where}: unexpected changed flag {changed!r}")
        rows.append({"test_id": scenario["test_id"], "name": scenario["name"], "verdict": scenario["verdict"],
                     "previous_verdict": previous, "changed": changed})
    need(len({row["test_id"] for row in rows}) == len(rows), f"{rel}: a test_id is listed twice")
    score = doc.get("score_percentage")
    need(score is None or is_number(score), f"{rel}: unexpected score_percentage")
    trigger, fixes = doc.get("trigger"), doc.get("fixes_applied", [])
    need(trigger is None or isinstance(trigger, str), f"{rel}: unexpected trigger")
    need(isinstance(fixes, list) and all(isinstance(fix, str) for fix in fixes), f"{rel}: unexpected fixes_applied")
    progression = doc.get("score_progression")
    need(progression is None or isinstance(progression, dict), f"{rel}: unexpected score_progression")
    improvement = next((doc[key] for key in sorted(doc) if key.startswith("improvement_from_cycle_")), None)
    need(improvement is None or isinstance(improvement, dict), f"{rel}: unexpected improvement block")
    return {
        "path": rel,
        "id": doc["id"],
        "cycle": doc["cycle"],
        "date": doc["date"],
        "evaluator": doc["evaluator"],
        "policy_version": doc["policy_version"],
        "protocol_version": doc["protocol_version"],
        "trigger": trigger,
        "fixes_applied": fixes,
        "scenarios_evaluated": doc["scenarios_evaluated"],
        "results_summary": summary,
        "score_percentage": score,
        "previous_score_quoted": None if improvement is None else improvement.get("previous_score"),
        "improvement_note": None if improvement is None else improvement.get("note"),
        "score_progression": progression,
        "scenarios": rows,
    }


# --- Markdown reports ---------------------------------------------------------------

def labelled(lines: list[str], label: str, rel: str) -> str:
    """The text that follows '**label:**' on the single line that starts with it."""
    marker = f"**{label}:**"
    hits = [line for line in lines if line.lstrip("- ").startswith(marker)]
    need(len(hits) == 1, f"{rel}: expected one line starting with {marker!r}, found {len(hits)}")
    return hits[0].lstrip("- ")[len(marker):].strip()


def table_rows(lines: list[str], heading: str, columns: list[str], rel: str) -> list[list[str]]:
    """Body rows of the first Markdown table after a heading, as lists of cell texts."""
    need(lines.count(heading) == 1, f"{rel}: expected one heading {heading!r}")
    rows = []
    for line in lines[lines.index(heading) + 1:]:
        if line.startswith("|"):
            rows.append([cell.strip() for cell in line.strip().strip("|").split("|")])
        elif rows or line.startswith("#"):
            break
    need(len(rows) >= 3, f"{rel}: no table under {heading!r}")
    need(rows[0] == columns, f"{rel}: table under {heading!r} has columns {rows[0]}, expected {columns}")
    need(all(cell and set(cell) <= set("-:") for cell in rows[1]), f"{rel}: table under {heading!r} has no separator row")
    need(all(len(row) == len(columns) for row in rows[2:]), f"{rel}: a row under {heading!r} has an unexpected number of cells")
    return rows[2:]


def numbered(rows: list[list[str]], rel: str) -> None:
    need([row[0] for row in rows] == [str(n) for n in range(1, len(rows) + 1)], f"{rel}: rows are not numbered 1, 2, 3, ...")


def leading_count(text: str, where: str) -> int:
    match = re.match(r"^(\d+)\b", text)
    need(match is not None, f"{where}: no leading count in {text!r}")
    return int(match.group(1))


def baseline_report(data: bytes) -> dict:
    """docs/reports/chaos-test-report.md: the injections scored once, before the history's cycles."""
    rel = BASELINE_REPORT
    lines = text_lines(data, rel)
    date = labelled(lines, "Date", rel)
    need(bool(DATE.match(date)), f"{rel}: unexpected date {date!r}")
    rows = table_rows(lines, "## Detection Results", BASELINE_COLUMNS, rel)
    numbered(rows, rel)
    injections = []
    for row in rows:
        verdict = row[5].split(" — ")[0]
        need(verdict in BASELINE_VERDICTS, f"{rel}: row {row[0]} has an unexpected verdict {verdict!r}")
        injections.append({"number": int(row[0]), "poison": row[1], "level": row[2], "verdict": verdict})
    score = BASELINE_SCORE.match(labelled(lines, "Poison Resilience Score", rel))
    need(score is not None, f"{rel}: the 'Poison Resilience Score' line has an unexpected form")
    return {
        "path": rel,
        "date": date,
        "purpose": labelled(lines, "Purpose", rel),
        "artifacts_tested": re.findall(r"`([^`]+)`", labelled(lines, "Artifacts tested", rel)),
        "injections": injections,
        "scorecard": {
            "injections": leading_count(labelled(lines, "Injections", rel), rel),
            "detected_full": leading_count(labelled(lines, "Detected (full)", rel), rel),
            "detected_partial_or_spec_only": leading_count(labelled(lines, "Detected (partial/spec-only)", rel), rel),
            "delayed_detection": leading_count(labelled(lines, "Delayed detection", rel), rel),
            "undetected": leading_count(labelled(lines, "Undetected", rel), rel),
            "detection_rate_line": labelled(lines, "Detection rate", rel),
            "score_line": score.group(0),
            "immediate": {"caught": int(score.group(1)), "total": int(score.group(2)), "quoted": score.group(3)},
            "including_spec_level": {"caught": int(score.group(4)), "total": int(score.group(5)), "quoted": score.group(6)},
        },
    }


def cycle_report(data: bytes) -> dict:
    """docs/reports/shake-metafix-cycle-001.md: the per-injection detail of one history cycle."""
    rel = CYCLE_REPORT
    lines = text_lines(data, rel)
    date = labelled(lines, "Date", rel)
    need(bool(DATE.match(date)), f"{rel}: unexpected date {date!r}")
    source = POISON_SOURCE.match(labelled(lines, "Poison source", rel))
    need(source is not None, f"{rel}: the 'Poison source' line has an unexpected form")
    rows = table_rows(lines, "## Injection Results", CYCLE_COLUMNS, rel)
    numbered(rows, rel)
    need(all(row[4] in ("YES", "NO") for row in rows), f"{rel}: a 'Caught?' cell is neither YES nor NO")
    summary = CYCLE_SUMMARY.match(labelled(lines, "Summary", rel))
    need(summary is not None, f"{rel}: the 'Summary' line has an unexpected form")
    definition = [line for line in lines if line.startswith('- **"Policy-enforceable"**')]
    automated_only = [line for line in lines if "If we count only fully automated detection" in line]
    need(len(definition) == 1 and len(automated_only) == 1, f"{rel}: the score-methodology notes are missing or repeated")
    return {
        "path": rel,
        "date": date,
        "cycle_id": labelled(lines, "Cycle ID", rel),
        "poison_source": {"path": source.group(1), "injections": int(source.group(2))},
        "injections": [{"number": int(row[0]), "injection": row[1], "level": row[2], "caught": row[4], "status": row[5]}
                       for row in rows],
        "summary": {
            "line": summary.group(0),
            "caught": int(summary.group(1)), "total": int(summary.group(2)), "percent_quoted": int(summary.group(3)),
            "previous_caught": int(summary.group(4)), "previous_total": int(summary.group(5)),
            "previous_percent_quoted": int(summary.group(6)), "previous_cycle_id": summary.group(7),
        },
        "policy_enforceable_definition": definition[0][2:],
        "automated_only_statement": automated_only[0],
    }


# --- definitions ----------------------------------------------------------------------

def glossary_entry(data: bytes) -> dict:
    lines = text_lines(data, GLOSSARY)
    starts = [index for index, line in enumerate(lines) if line.startswith(GLOSSARY_ENTRY)]
    need(len(starts) == 1, f"{GLOSSARY}: expected one line starting with {GLOSSARY_ENTRY!r}, found {len(starts)}")
    start = starts[0]
    parts = [lines[start].strip()]
    for line in lines[start + 1:]:
        if not line.startswith("  ") or not line.strip():
            break
        parts.append(line.strip())
    text = " ".join(parts)
    need("injections_caught / injections_total" in text, f"{GLOSSARY}: the entry no longer gives the formula of R")
    return {"path": GLOSSARY, "line": start + 1, "text": text}


def readme_status(data: bytes) -> dict:
    lines = text_lines(data, README)
    hits = [index for index, line in enumerate(lines) if line.startswith(README_STATUS)]
    need(len(hits) == 1, f"{README}: expected one line starting with {README_STATUS!r}, found {len(hits)}")
    return {"path": README, "line": hits[0] + 1, "text": lines[hits[0]].strip()}


def metric_policy(data: bytes) -> dict:
    """The few fields of the resilience metric policy this module uses, read without a YAML library."""
    rel = POLICY
    text = "\n".join(text_lines(data, rel))

    def one(pattern: str, what: str) -> str:
        found = re.findall(pattern, text, flags=re.MULTILINE)
        need(len(found) == 1, f"{rel}: expected one {what}, found {len(found)}")
        return found[0]

    section = re.search(r"^thresholds:\n((?:  .*\n)+)", text, flags=re.MULTILINE)
    need(section is not None, f"{rel}: no thresholds block")
    bands = re.findall(r'^  (\w+):\n    range: "([^"]+)"\n    action: "([^"]+)"$', section.group(1), flags=re.MULTILINE)
    need(len(bands) >= 2 and len(bands) == section.group(1).count("range:"), f"{rel}: unexpected thresholds block")
    return {
        "path": rel,
        "name": one(r"^name: (\S+)$", "name"),
        "version": one(r'^version: "([^"]+)"$', "version"),
        "formula": one(r'^  formula: "([^"]+)"$', "formula"),
        "thresholds": [{"name": name, "range": span, "action": action} for name, span, action in bands],
        "trend": {key: one(rf'^    {key}: "([^"]+)"$', f"trend {key}") for key in ("method", "improving", "degrading", "stable")},
    }


# --- snapshot ---------------------------------------------------------------------------

def build(root: Path, allow_drift: bool) -> dict:
    folder = root / RESILIENCE_DIR
    need(folder.is_dir(), f"missing directory: {RESILIENCE_DIR}")
    present = sorted(f"{RESILIENCE_DIR}/{path.name}" for path in folder.iterdir())
    expected = sorted(path for path in PINNED_BLOBS if path.startswith(RESILIENCE_DIR + "/"))
    drift = [f"{path} is in the folder but not in the pinned commit" for path in present if path not in expected]

    files, raw = [], {}
    for rel in sorted(PINNED_BLOBS):
        raw[rel] = read(root, rel)
        blob = git_blob_id(raw[rel])
        files.append({"path": rel, "git_blob": blob, "bytes_lf": len(raw[rel].replace(b"\r\n", b"\n"))})
        if blob != PINNED_BLOBS[rel]:
            drift.append(f"{rel} is blob {blob}, pinned {PINNED_BLOBS[rel]}")
    if drift and not allow_drift:
        raise ExtractError("source files are not those of commit " + PINNED_COMMIT + ":\n  " + "\n  ".join(drift)
                           + "\n(--allow-drift snapshots them anyway; the lesson's numbers then no longer apply)")

    history = load_json(raw[HISTORY], HISTORY)
    records = history_records(history)
    cycles = [red_team_cycle(load_json(raw[rel], rel), rel) for rel in RED_TEAM]
    baseline = baseline_report(raw[BASELINE_REPORT])
    detail = cycle_report(raw[CYCLE_REPORT])
    return {
        "schema_version": "0.2.0",
        "module_id": "psy-013-four-scores-and-a-trend",
        "kind": "observed",
        "source": {
            "repository": "GuitarAlchemist/Demerzel",
            "commit": None if drift else PINNED_COMMIT,
            "commit_check": ("FAILED: " + "; ".join(drift)) if drift else
                            "every file below has the Git blob id recorded for this commit (CRLF normalised to LF), "
                            "and state/resilience/ holds no other file",
            "files": files,
            "resilience_folder_listing": present,
            "injection_files_pinned_but_not_parsed": list(INJECTION_FILES),
        },
        "counts": {
            "files_in_resilience_folder": len(present),
            "history_records": len(records),
            "red_team_cycle_files": len(cycles),
            "injection_rows": sum(len(record["injections"]) for record in records),
            "scenario_rows": sum(len(cycle["scenarios"]) for cycle in cycles),
            "baseline_report_rows": len(baseline["injections"]),
            "cycle_report_rows": len(detail["injections"]),
        },
        "definitions": {
            "glossary": glossary_entry(raw[GLOSSARY]),
            "metric_policy": metric_policy(raw[POLICY]),
            "readme_status": readme_status(raw[README]),
        },
        "history": {"path": HISTORY, "metric": history["metric"], "version": history["version"], "records": records},
        "reports": {"baseline": baseline, "cycle": detail},
        "red_team_cycles": cycles,
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
    except (ExtractError, OSError) as exc:
        print(f"extract.py: {exc}", file=sys.stderr)
        return 1
    text = json.dumps(snapshot, ensure_ascii=False, indent=2) + "\n"
    args.output.write_bytes(text.encode("utf-8"))
    counts = snapshot["counts"]
    print(f"extract.py: {len(snapshot['source']['files'])} source files, {counts['files_in_resilience_folder']} of them in "
          f"{RESILIENCE_DIR}; {counts['history_records']} history records ({counts['injection_rows']} injection rows), "
          f"{counts['red_team_cycle_files']} red-team cycle files ({counts['scenario_rows']} scenario rows), "
          f"2 reports ({counts['baseline_report_rows']} + {counts['cycle_report_rows']} rows) -> {args.output.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
