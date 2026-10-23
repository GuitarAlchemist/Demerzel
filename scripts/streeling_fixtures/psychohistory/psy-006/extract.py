#!/usr/bin/env python3
"""PSY-006 extract: snapshot the label series and the stored transition models.

Reads the effectiveness label of every row of state/quality-trend/*.jsonl, the
stored governance model (state/markov/transition-matrix.json and
predictions.json), four lines of its specification
(docs/specs/governance-markov-simulation.md) and the seed table of belief
transitions (state/driver/transition-weights.json), and writes
observed-input.json next to this script. The analysis script reads only that
snapshot, so its results do not move when the nightly feeder appends new rows.

Fails with a non-zero exit and a message when a source file is missing, has an
unexpected shape, or is not the file of the pinned commit.

Run from the repository root:
    python -I scripts/streeling_fixtures/psychohistory/psy-006/extract.py
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
                / "state/streeling/fixtures/psychohistory/psy-006" / Path(__file__).name)

PINNED_COMMIT = "4b03838800dcd4894f1e026461979bff1d985ca8"
# Git blob ids at PINNED_COMMIT (git ls-tree). A blob id is
# sha1(b"blob <size>\0" + content) over the LF-normalised bytes.
PINNED_BLOBS = {
    "state/quality-trend/2026-05.jsonl": "ab1c35d9948c9bfbb1501b20c39b736d92dc0bb2",
    "state/quality-trend/2026-07.jsonl": "57b303ea2ed56d96010345a2acd508bff248486e",
    "state/quality-trend/2026-08.jsonl": "e2b4462797f1ee06f3188154611de0fdbcc07a23",
    "state/quality-trend/2026-09.jsonl": "9b74c1a34378e3f3941c1c0bb054f5b10fe2b64f",
    "state/quality-trend/2026-10.jsonl": "e64c9c855667f2408e1e4f8c894e1be2722afdd1",
    "state/markov/transition-matrix.json": "7f217ded0fb4e0d5405a4e265ac13042b44c69a5",
    "state/markov/predictions.json": "1cf8112c920a990a095d372f4d4121a74e073b26",
    "state/driver/transition-weights.json": "a297280a2b9ec0e217595eabd132e38a942ff62f",
    "docs/specs/governance-markov-simulation.md": "95f3e2fc144fa9854a756352b232bf359415b446",
}
TREND_DIR = "state/quality-trend"
MARKOV_DIR = "state/markov"
MATRIX_FILE = "state/markov/transition-matrix.json"
PREDICTIONS_FILE = "state/markov/predictions.json"
WEIGHTS_FILE = "state/driver/transition-weights.json"
SPEC_FILE = "docs/specs/governance-markov-simulation.md"
# The lines of the specification that the analysis and the lesson rely on. Each
# pattern must match exactly one line; its groups are recorded with the line.
SPEC_LINES = {
    "freeze_formula": r"^cycles_to_freeze = log\((0\.5)\) / log\(P\(not_freeze\)\)$",
    "alert_rule": r"^When P\(Freeze\) > (0\.\d+), an alert is emitted with the top recommended intervention\.$",
    "uniform_initialisation": r"^P\(j \| i\) = (0\.25) for all i, j in \{Healthy, Watch, Warning, Freeze\}$",
    "engine_state_path": r"^`engine\.export_state\(\)` and stored at `(state/markov/[a-z-]+\.json)`\. This allows the$",
}
SPEC_STATE_ROW = re.compile(r"^\| (Healthy|Watch|Warning|Freeze) +\| (\d) +\|")
BELIEF_MACHINE = "belief_hexavalent"
# File names in MARKOV_DIR at PINNED_COMMIT. The stored matrix's note points to
# an engine-state.json; the listing records that the folder holds none.
PINNED_MARKOV_LISTING = ["predictions.json", "resistance-matrix.json", "transition-matrix.json"]
ENGINE_STATE_NAME = "engine-state.json"
LABELS = ("T", "P", "U", "D", "F", "C")
LABEL_NAMES = {"T": "True", "P": "Probable", "U": "Unknown", "D": "Doubtful", "F": "False", "C": "Contradictory"}
TIMESTAMP = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")
ARROW = re.compile(r"^([A-Za-z_]+)->([A-Za-z_]+)$")
NO_ROW, NO_LABEL = ".", "-"


class ExtractError(Exception):
    """A source file is missing, malformed, or not the pinned one."""


def git_blob_id(data: bytes) -> str:
    """Blob id Git stores for this content once CRLF is normalised to LF."""
    data = data.replace(b"\r\n", b"\n")
    return hashlib.sha1(b"blob %d\x00" % len(data) + data).hexdigest()


def parse_timestamp(value: str) -> datetime:
    """A feeder timestamp (UTC, to the second) as an aware datetime."""
    return datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)


def is_number(value: object) -> bool:
    """True for an int or a float, not for a bool."""
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def data_label(name: str) -> str:
    """An artifact name as a data label: a space on each side of every slash.

    scripts/evolution_metrics.py counts as a citation of an artifact every tracked file that contains the artifact's
    path as a literal string. A course data file that listed the paths would raise the counts it sits next to, so
    the snapshot never holds a name in its path form.
    """
    return " / ".join(name.split("/")).rstrip()


def read_rows(root: Path) -> tuple[list[dict], list[dict]]:
    """Every quality-trend row, reduced to what a label transition needs."""
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
            for key in ("timestamp", "artifact", "effectiveness_to"):
                if key not in row:
                    raise ExtractError(f"{where}: missing key {key!r}")
            timestamp, artifact, label = row["timestamp"], row["artifact"], row["effectiveness_to"]
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
            if label is not None and label not in LABELS:
                raise ExtractError(f"{where}: unexpected effectiveness_to {label!r}")
            if not isinstance(row.get("baseline", False), bool):
                raise ExtractError(f"{where}: unexpected baseline flag {row['baseline']!r}")
            if (timestamp, artifact) in seen:
                raise ExtractError(f"{where}: second row for {artifact!r} at {timestamp}")
            seen.add((timestamp, artifact))
            rows.append({"file": rel, "line": number, "timestamp": timestamp, "artifact": data_label(artifact),
                         "to": label, "baseline": row.get("baseline", False)})
        files.append({"path": rel, "git_blob": git_blob_id(data), "rows": len(lines)})
    return rows, files


def read_json_object(root: Path, rel: str) -> tuple[dict, dict]:
    """A JSON file that must hold an object, with its entry for the file list (path and Git blob id)."""
    path = root / rel
    if not path.is_file():
        raise ExtractError(f"missing file: {rel}")
    data = path.read_bytes()
    try:
        value = json.loads(data.decode("utf-8"))
    except json.JSONDecodeError as exc:
        raise ExtractError(f"{rel}: not JSON ({exc})") from exc
    if not isinstance(value, dict):
        raise ExtractError(f"{rel}: not a JSON object")
    return value, {"path": rel, "git_blob": git_blob_id(data)}


def stored_governance_model(root: Path) -> tuple[dict, list[dict]]:
    """The stored matrix and its prediction log, with the shape the analysis relies on."""
    matrix_file, matrix_entry = read_json_object(root, MATRIX_FILE)
    states, matrix = matrix_file.get("states"), matrix_file.get("matrix")
    if (not isinstance(states, list) or len(states) < 2 or len(set(states)) != len(states)
            or not all(isinstance(state, str) and state for state in states)):
        raise ExtractError(f"{MATRIX_FILE}: 'states' is not a list of distinct names")
    if (not isinstance(matrix, list) or len(matrix) != len(states)
            or not all(isinstance(row, list) and len(row) == len(states) for row in matrix)):
        raise ExtractError(f"{MATRIX_FILE}: 'matrix' is not {len(states)} rows of {len(states)} entries")
    if not all(is_number(entry) and 0 <= entry <= 1 for row in matrix for entry in row):
        raise ExtractError(f"{MATRIX_FILE}: a matrix entry is not a number between 0 and 1")
    if matrix_file.get("state_indices") != {state: index for index, state in enumerate(states)}:
        raise ExtractError(f"{MATRIX_FILE}: 'state_indices' does not number the states in order")
    for key in ("description", "version", "created", "note"):
        if not isinstance(matrix_file.get(key), str):
            raise ExtractError(f"{MATRIX_FILE}: missing text field {key!r}")

    predictions_file, predictions_entry = read_json_object(root, PREDICTIONS_FILE)
    predictions = predictions_file.get("predictions")
    if not isinstance(predictions, list):
        raise ExtractError(f"{PREDICTIONS_FILE}: 'predictions' is not a list")
    for key in ("description", "version", "created"):
        if not isinstance(predictions_file.get(key), str):
            raise ExtractError(f"{PREDICTIONS_FILE}: missing text field {key!r}")

    folder = root / MARKOV_DIR
    listing = sorted(path.name for path in folder.iterdir())
    model = {
        "transition_matrix": {"path": MATRIX_FILE} | {key: matrix_file[key] for key in
                                                      ("description", "version", "created", "states", "matrix", "note")},
        "predictions": {"path": PREDICTIONS_FILE} | {key: predictions_file[key] for key in
                                                     ("description", "version", "created")}
                       | {"entries": len(predictions), "predictions": predictions},
        "folder": {"path": MARKOV_DIR, "files": listing,
                   "file_named_by_the_matrix_note": ENGINE_STATE_NAME,
                   "note_names_that_file": ENGINE_STATE_NAME in matrix_file["note"],
                   "that_file_is_in_the_folder": ENGINE_STATE_NAME in listing},
    }
    return model, [matrix_entry, predictions_entry]


def governance_spec(root: Path, states: list[str]) -> tuple[dict, dict]:
    """The lines of the specification that say what the stored model is for."""
    path = root / SPEC_FILE
    if not path.is_file():
        raise ExtractError(f"missing file: {SPEC_FILE}")
    data = path.read_bytes()
    lines = data.decode("utf-8").splitlines()
    found = {}
    for name, pattern in SPEC_LINES.items():
        matches = [(number, re.match(pattern, line)) for number, line in enumerate(lines, 1) if re.match(pattern, line)]
        if len(matches) != 1:
            raise ExtractError(f"{SPEC_FILE}: expected one line for {name!r}, found {len(matches)}")
        number, match = matches[0]
        found[name] = {"line": number, "text": match.group(0), "value": match.group(1)}
    table = [(number, SPEC_STATE_ROW.match(line)) for number, line in enumerate(lines, 1) if SPEC_STATE_ROW.match(line)]
    if [(match.group(1), int(match.group(2))) for _, match in table] != [(state, index) for index, state in enumerate(states)]:
        raise ExtractError(f"{SPEC_FILE}: the state table does not list {states} with the indices 0 to {len(states) - 1}")
    spec = {"path": SPEC_FILE, "state_table_lines": [number for number, _ in table]} | found
    return spec, {"path": SPEC_FILE, "git_blob": git_blob_id(data)}


def belief_seed_table(root: Path) -> tuple[dict, dict]:
    """The seed transition weights over the six truth values."""
    weights_file, entry = read_json_object(root, WEIGHTS_FILE)
    machines = weights_file.get("machines")
    if not isinstance(machines, dict) or not isinstance(machines.get(BELIEF_MACHINE), dict):
        raise ExtractError(f"{WEIGHTS_FILE}: no machine {BELIEF_MACHINE!r}")
    machine = machines[BELIEF_MACHINE]
    states, transitions, forbidden = machine.get("states"), machine.get("transitions"), machine.get("forbidden")
    if not isinstance(states, list) or sorted(states) != sorted(LABELS):
        raise ExtractError(f"{WEIGHTS_FILE}: {BELIEF_MACHINE} states are not the six labels {LABELS}")
    if not isinstance(transitions, dict) or not transitions:
        raise ExtractError(f"{WEIGHTS_FILE}: {BELIEF_MACHINE} has no transitions")
    if not isinstance(forbidden, list):
        raise ExtractError(f"{WEIGHTS_FILE}: {BELIEF_MACHINE} 'forbidden' is not a list")
    for name in list(transitions) + forbidden:
        match = ARROW.match(name) if isinstance(name, str) else None
        if not match or match.group(1) not in states or match.group(2) not in states:
            raise ExtractError(f"{WEIGHTS_FILE}: {BELIEF_MACHINE} entry {name!r} is not '<label>-><label>'")
    if not all(is_number(weight) and 0 <= weight <= 1 for weight in transitions.values()):
        raise ExtractError(f"{WEIGHTS_FILE}: a {BELIEF_MACHINE} weight is not a number between 0 and 1")
    for key in ("description", "version", "note"):
        if not isinstance(weights_file.get(key), str):
            raise ExtractError(f"{WEIGHTS_FILE}: missing text field {key!r}")
    if not isinstance(machine.get("note"), str):
        raise ExtractError(f"{WEIGHTS_FILE}: {BELIEF_MACHINE} has no note")
    table = {
        "path": WEIGHTS_FILE, "machine": BELIEF_MACHINE,
        "file_description": weights_file["description"], "file_version": weights_file["version"],
        "file_note": weights_file["note"], "other_machines_in_the_file": sorted(set(machines) - {BELIEF_MACHINE}),
        "states": states, "transitions": transitions, "forbidden": forbidden, "note": machine["note"],
    }
    return table, entry


def read_sources(root: Path) -> tuple[list[dict], dict, dict, list[dict]]:
    """Read the nine pinned files: the trend rows, the stored model with its specification, and the seed table.

    Returns (rows, governance, seed_table, files); each entry of `files` holds a path, a Git blob id and a role.
    """
    rows, files = read_rows(root)
    governance, governance_files = stored_governance_model(root)
    governance["specification"], spec_file = governance_spec(root, governance["transition_matrix"]["states"])
    engine_state = governance["specification"]["engine_state_path"]["value"]
    if engine_state != f"{MARKOV_DIR}/{ENGINE_STATE_NAME}":
        raise ExtractError(f"{SPEC_FILE}: the engine state is stored at {engine_state}, expected {MARKOV_DIR}/{ENGINE_STATE_NAME}")
    seed_table, seed_table_file = belief_seed_table(root)
    for entry in files:
        entry["role"] = "quality trend: one row per artifact and run"
    governance_files[0]["role"] = "stored governance transition matrix"
    governance_files[1]["role"] = "stored governance predictions"
    seed_table_file["role"] = f"seed transition weights; only the machine {BELIEF_MACHINE} is read"
    spec_file["role"] = "specification of the governance model; only the state table and four lines are read"
    return rows, governance, seed_table, files + governance_files + [seed_table_file, spec_file]


def count_pair(previous: dict, row: dict, pairs: dict, transition_counts: dict) -> dict | None:
    """Count one pair of consecutive rows of an artifact; return the label change it holds, if any."""
    pairs["row_pairs"] += 1
    if not (previous["to"] and row["to"]):
        pairs["pairs_without_a_label"] += 1
        return None
    pairs["usable_pairs"] += 1
    pairs["usable_pairs_from_a_seed_row" if previous["baseline"] else "usable_pairs_between_feeder_runs"] += 1
    key = f"{previous['to']}>{row['to']}"
    transition_counts[key] = transition_counts.get(key, 0) + 1
    changed = previous["to"] != row["to"]
    pairs["changed" if changed else "unchanged"] += 1
    if not changed:
        return None
    gap = parse_timestamp(row["timestamp"]) - parse_timestamp(previous["timestamp"])
    return {"from": previous["to"], "to": row["to"],
            "earlier_row": {k: previous[k] for k in ("file", "line", "timestamp", "baseline")},
            "later_row": {k: row[k] for k in ("file", "line", "timestamp", "baseline")},
            "gap_days": round(gap.total_seconds() / 86400, 3)}


def count_pairs(rows: list[dict], runs: list[str]) -> dict:
    """Per artifact, one character per run for its label and for its seed flag; over all artifacts, the pair counts."""
    run_index = {timestamp: index for index, timestamp in enumerate(runs)}
    by_artifact: dict[str, list[dict]] = {}
    for row in rows:
        by_artifact.setdefault(row["artifact"], []).append(row)
    pairs = {"row_pairs": 0, "usable_pairs": 0, "pairs_without_a_label": 0, "changed": 0, "unchanged": 0,
             "usable_pairs_from_a_seed_row": 0, "usable_pairs_between_feeder_runs": 0}
    transition_counts: dict[str, int] = {}
    artifacts, changes = [], []
    for name in sorted(by_artifact):
        series = by_artifact[name]
        cells = {key: [NO_ROW] * len(runs) for key in ("to", "seed")}
        for row in series:
            index = run_index[row["timestamp"]]
            cells["to"][index] = row["to"] or NO_LABEL
            cells["seed"][index] = "s" if row["baseline"] else NO_LABEL
        for previous, row in zip(series, series[1:]):
            change = count_pair(previous, row, pairs, transition_counts)
            if change:
                changes.append({"artifact": name, **change})
        artifacts.append({"name": name, "rows": len(series), "first_run_index": run_index[series[0]["timestamp"]],
                          "effectiveness_to": "".join(cells["to"]), "baseline_flag": "".join(cells["seed"])})
    return {"pairs": pairs, "transition_counts": dict(sorted(transition_counts.items())),
            "artifacts": artifacts, "label_changes": changes}


def drift_from_the_pin(files: list[dict], markov_listing: list[str]) -> list[str]:
    """Every difference from the pinned commit: a blob id, a pinned file that was not read, the folder listing."""
    drift = []
    for entry in files:
        if PINNED_BLOBS.get(entry["path"]) != entry["git_blob"]:
            drift.append(f"{entry['path']} is blob {entry['git_blob']}, pinned {PINNED_BLOBS.get(entry['path'])}")
    drift += [f"{path} is pinned but was not read" for path in sorted(set(PINNED_BLOBS) - {e["path"] for e in files})]
    if markov_listing != PINNED_MARKOV_LISTING:
        drift.append(f"{MARKOV_DIR} holds {markov_listing}, pinned {PINNED_MARKOV_LISTING}")
    return drift


def build(root: Path, allow_drift: bool) -> dict:
    """The snapshot: the sources read and compared with the pin, then the counts, in the key order of the output."""
    rows, governance, seed_table, files = read_sources(root)
    runs = sorted({row["timestamp"] for row in rows})
    counted = count_pairs(rows, runs)
    drift = drift_from_the_pin(files, governance["folder"]["files"])
    if drift and not allow_drift:
        raise ExtractError("source files are not those of commit " + PINNED_COMMIT + ":\n  " + "\n  ".join(drift)
                           + "\n(--allow-drift snapshots them anyway; the lesson's numbers then no longer apply)")
    rows_per_run = {timestamp: 0 for timestamp in runs}
    for row in rows:
        rows_per_run[row["timestamp"]] += 1
    return {
        "schema_version": "0.1.0",
        "module_id": "psy-006-transition-matrix-from-counts",
        "kind": "observed",
        "source": {
            "repository": "GuitarAlchemist/Demerzel",
            "commit": None if drift else PINNED_COMMIT,
            "commit_check": ("FAILED: " + "; ".join(drift)) if drift else
                            "every file below has the Git blob id recorded for this commit (CRLF normalised to LF), "
                            "and the state/markov folder holds the file names recorded for it",
            "files": files,
        },
        "encoding": {
            "runs": "one entry per distinct timestamp, in time order; every row of a run carries that timestamp",
            "artifact names": "data labels: the name recorded in the quality trend, with a space on each side of every "
                              "slash, so that this file holds no artifact path as a literal string",
            "artifact strings": "one character per run, aligned with the runs list",
            NO_ROW: "the artifact has no row in that run",
            NO_LABEL: "the row exists and effectiveness_to is null (for baseline_flag: the flag is absent)",
            "s": "baseline_flag only: the row carries baseline: true (a seed row)",
            "labels": LABEL_NAMES,
            "transition_counts": "'<earlier label>><later label>': number of usable consecutive-row pairs",
        },
        "counts": {
            "rows": len(rows),
            "trend_files": sum(entry["path"].startswith(TREND_DIR + "/") for entry in files),
            "runs": len(runs),
            "artifacts": len(counted["artifacts"]),
            "rows_flagged_baseline": sum(row["baseline"] for row in rows),
            "rows_without_effectiveness_to": sum(row["to"] is None for row in rows),
            "consecutive_pairs": counted["pairs"],
            "transition_counts": counted["transition_counts"],
        },
        "label_changes": counted["label_changes"],
        "runs": [{"index": index, "timestamp": timestamp, "rows": rows_per_run[timestamp]} for index, timestamp in enumerate(runs)],
        "artifacts": counted["artifacts"],
        "stored_governance_model": governance,
        "belief_seed_table": seed_table,
    }


def main() -> int:
    """Write observed-input.json from the repository this file sits in, or from --repo-root."""
    here = FIXTURE_FILE
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
    pairs = snapshot["counts"]["consecutive_pairs"]
    print(f"extract.py: {snapshot['counts']['rows']} rows, {snapshot['counts']['runs']} runs, "
          f"{snapshot['counts']['artifacts']} artifacts, {pairs['usable_pairs']} consecutive pairs, "
          f"{pairs['changed']} changed; {len(snapshot['source']['files'])} pinned files -> {args.output.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
