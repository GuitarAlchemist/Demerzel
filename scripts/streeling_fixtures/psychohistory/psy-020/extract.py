#!/usr/bin/env python3
"""PSY-020 extract: recount the citation metric on the tree of the pinned commit.

Applies the counting rule of scripts/evolution_metrics.py (every tracked file
that contains one of an artifact's citation paths as a literal string, outside
a few excluded folders) to the files of the pinned commit, and snapshots what
the lesson needs from the quality trend, the evolution records, the anti-LOLLI
policy and the rule that calls a concentration of citations healthy. Writes
observed-input.json next to this script; analyze.py reads only that snapshot.

The list of tracked files and their blob ids comes from `git ls-tree -r <pin>`
(commits and trees only). Each file is read from the working tree and checked
against its pinned blob id; a file that is missing or different there is read
from Git's object store, so the snapshot is that of the pinned commit whatever
the checkout holds. Fails with a non-zero exit when Git cannot list the pinned
tree, when that tree is not the pinned one, when a pinned blob cannot be read,
or when a source has an unexpected shape.

No citation path is written in this program or in its output: the paths are
built from the evolution records at run time and stored with a space on each
side of every slash, so that neither file is counted by the rule it studies.

Run from the repository root:
    python -I -B scripts/streeling_fixtures/psychohistory/psy-020/extract.py
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path

# This program lives under scripts/ (CONTRIBUTING.md: no executable code outside scripts/); its data stays
# under state/streeling/fixtures/. FIXTURE_FILE is the path the program would have next to that data.
FIXTURE_FILE = (Path(__file__).resolve().parents[4]
                / "state/streeling/fixtures/psychohistory/psy-020" / Path(__file__).name)

HERE = FIXTURE_FILE.parent
PINNED_COMMIT = "4b03838800dcd4894f1e026461979bff1d985ca8"
PINNED_TREE = "93a30b4afccee2e2cf7733d6223943ffeca86e86"
# SHA-256 of the lines "<blob id> <path>\n" of `git ls-tree -r <pin>`, sorted by path bytes.
MANIFEST_SHA256 = "156ff20220ab2e92bab0ce7361a47326f10431f6a281446234199e57bd97d2a8"
MANIFEST_FILES = 2062
PRODUCER = "scripts/evolution_metrics.py"
FEEDER = "scripts/quality_trend.py"
POLICY = "policies/anti-lolli-inflation-policy.yaml"
HISTORY = "state/driver/lolli-ergol-history.json"
CORRECTED_RECORD = "state/evolution/2026-04-30-the-sentinel.evolution.json"
POWER_LAW_RULE = "logic/fractal-compounding.md"
# The compounding-metrics policy is itself a citation path: its full path is taken from the evolution records at
# run time (the one citation path with this file name) and written spaced in the output.
METRICS_POLICY = "compounding-metrics-policy.yaml"
EVOLUTION_DIR = "state/evolution"
TREND_DIR = "state/quality-trend"
# The producer's exclusion pathspecs, and what they match when Git reads them without glob magic:
# a literal pathspec matches that path and everything under it; in "**/archived/**" each star also
# matches slashes, so the pathspec matches every path that contains "/archived/".
EXCLUDED = (":!state/evolution", ":!state/quality-trend", ":!**/archived/**", ":!governance-manifest.json")
EXCLUDED_PREFIXES = ("state/evolution", "state/quality-trend", "governance-manifest.json")
EXCLUDED_INFIX = "/archived/"
CORRECTION = ("Correction, 2026-09-13. The first measured citation count (scripts/evolution_metrics.py, #1077) is 0, "
              "which reads as 'nothing uses this spec'. That is true only inside Demerzel: the metric cannot see "
              "sibling repositories.")
# Passages the lesson quotes or links by line: (file, lines with surrounding whitespace removed).
QUOTES = {
    "producer_definition": (PRODUCER, [
        "citation_count  tracked files that mention any of the artifact's citation",
        "paths (`git grep -lF`), excluding the artifact's own files,",
        "archived/, state/evolution/, state/quality-trend/ and the",
        "generated governance-manifest.json."]),
    "producer_citation_paths": (PRODUCER, [
        "Citation paths are the entry's `citation_paths` list when present, else its",
        "`artifact` when that is a tracked path. An explicit empty list marks an",
        "artifact that lives outside this repository (unmeasurable here). Anything",
        "else is reported as unmeasurable and left untouched."]),
    "producer_source_label": (PRODUCER, ['CITATION_SOURCE = "git-grep-v1"']),
    "producer_exclusions": (PRODUCER, ["EXCLUDED = (" + ", ".join(f'"{spec}"' for spec in EXCLUDED) + ")"]),
    "producer_search": (PRODUCER, [
        'for ref in git(root, "grep", "-lF", "-e", p, "--", ".", *EXCLUDED).splitlines():',
        "if ref and not owned_by(ref, paths):",
        "refs.add(ref)"]),
    "producer_count": (PRODUCER, ["return len(refs), last"]),
    "feeder_reads_count": (FEEDER, ['citation = int(metrics.get("citation_count", 0) or 0)']),
    "policy_citations": (POLICY, [
        'citations: "Times an artifact is referenced in decisions, manifests, research, or other artifacts"']),
    "policy_ergol": (POLICY, [
        "ERGOL_n = citations_n + pdca_completions_n + u_to_t_transitions_n + knowledge_transfers_n"]),
    "policy_lolli": (POLICY, ['formula: "LOLLI_n = count(artifacts created in cycle N)"']),
    "policy_ratio": (POLICY, ['formula: "ratio_n = LOLLI_n / max(ERGOL_n, 1)"']),
    "policy_freeze_trigger": (POLICY, ['trigger: "lolli_ergol_ratio > 3.0 for 3 consecutive cycles"']),
    "policy_zero_rule": (POLICY, [
        "zero_citation_window: 14   # days",
        'rule: "Any artifact with 0 citations after 14 days of creation is flagged for deprecation review"']),
    "policy_citation_source": (POLICY, ['- "state/evolution/*.evolution.json — citation_count delta"']),
    "policy_zero_scan": (POLICY, [
        'action: "Scan all artifacts created > 14 days ago; flag any with citation_count = 0"']),
    "policy_healthy": (POLICY, ["healthy:", "max_ratio: 1.5"]),
    "policy_watch": (POLICY, ["watch:", "min_ratio: 1.5", "max_ratio: 2.5"]),
    "policy_warning": (POLICY, ["warning:", "min_ratio: 2.5", "max_ratio: 3.0"]),
    "policy_freeze": (POLICY, ["freeze:", "min_ratio: 3.0", "consecutive_cycles: 3"]),
    "power_law_detection_rule": (POWER_LAW_RULE, [
        "**Detection rule:** If the top 20% of governance artifacts account for more than 60% of citations, a power "
        "law is present. This is healthy — it means compounding is concentrating value where it matters."]),
    "power_law_data": (POWER_LAW_RULE, [
        "Tracked via: `state/evolution/*.evolution.json` citation counts, analyzable by SymPy MCP."]),
    "power_law_integration": (POWER_LAW_RULE, [
        "- State: `state/evolution/*.evolution.json` (citation tracking for power law detection)"]),
    "metrics_policy_rule": (METRICS_POLICY, [
        'rule: "Top 20% of governance artifacts account for > 60% of citations → power law present (healthy)"']),
    "metrics_policy_source": (METRICS_POLICY, [
        'detection_source: "state/evolution/*.evolution.json citation_count fields"']),
    "metrics_policy_share": (METRICS_POLICY, [
        "- name: power_law_health", 'formula: "citation_share of top 20% artifacts"', 'target: "0.60–0.85"',
        'alert: "> 0.90 (fragile concentration)"']),
}
TIMESTAMP = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")
KEYS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


class ExtractError(Exception):
    """A source is missing, malformed, or not the pinned one."""


def spaced(name: str) -> str:
    """A repository path or artifact name as a data label: a space on each side of every slash."""
    return " / ".join(name.split("/")).rstrip()


def git_blob_id(data: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(data)).encode("ascii") + b"\0" + data).hexdigest()


def git(root: Path, *args: str, stdin: bytes | None = None) -> bytes:
    """Runs one read-only git command in the repository and returns its standard output."""
    env = dict(os.environ, GIT_NO_LAZY_FETCH="1")  # a partial clone must not download a missing blob silently
    try:
        done = subprocess.run(["git", *args], cwd=root, input=stdin, capture_output=True, env=env, check=False)
    except OSError as exc:
        raise ExtractError(f"git is needed to list the files of the pinned commit: {exc}") from exc
    if done.returncode != 0:
        raise ExtractError(f"git {' '.join(args)} failed in {root}: {done.stderr.decode('utf-8', 'replace').strip()}")
    return done.stdout


def pinned_manifest(root: Path) -> list[tuple[str, str, str]]:
    """Returns (path, mode, blob id) for every file of the pinned commit, sorted by path bytes."""
    tree = git(root, "rev-parse", "--verify", PINNED_COMMIT + "^{tree}").decode("ascii").strip()
    if tree != PINNED_TREE:
        raise ExtractError(f"commit {PINNED_COMMIT} has tree {tree}, expected {PINNED_TREE}")
    entries = []
    for record in git(root, "ls-tree", "-r", "-z", PINNED_COMMIT).split(b"\0"):
        if not record:
            continue
        meta, path = record.split(b"\t", 1)
        mode, kind, blob = meta.decode("ascii").split()
        if kind != "blob" or mode not in ("100644", "100755"):
            raise ExtractError(f"{path!r}: entry {mode} {kind} is not a regular file; git grep would not search it")
        entries.append((path, mode, blob))
    entries.sort()
    lines = b"".join(blob.encode("ascii") + b" " + path + b"\n" for path, _, blob in entries)
    digest = hashlib.sha256(lines).hexdigest()
    if len(entries) != MANIFEST_FILES or digest != MANIFEST_SHA256:
        raise ExtractError(f"the tree of {PINNED_COMMIT} lists {len(entries)} files with manifest {digest}; "
                           f"expected {MANIFEST_FILES} files and {MANIFEST_SHA256}")
    if any(b" " in path for path, _, _ in entries):
        raise ExtractError("a tracked path contains a space: spaced labels could not be read back")
    return [(path.decode("utf-8"), mode, blob) for path, mode, blob in entries]


def read_git_objects(root: Path, wanted: list[tuple[str, str]]) -> dict[str, bytes]:
    """Reads pinned blobs from Git's object store with one `git cat-file --batch` call."""
    stream = git(root, "cat-file", "--batch", stdin="".join(blob + "\n" for _, blob in wanted).encode("ascii"))
    found, position = {}, 0
    for path, blob in wanted:
        end = stream.find(b"\n", position)
        header = stream[position:end].decode("ascii", "replace").split() if end >= 0 else []
        if len(header) != 3 or header[0] != blob or header[1] != "blob":
            raise ExtractError(f"{path}: the working tree does not hold the pinned blob {blob} and this clone "
                               "cannot supply it; check out or fetch the pinned commit")
        size = int(header[2])
        data = stream[end + 1:end + 1 + size]
        if git_blob_id(data) != blob:
            raise ExtractError(f"{path}: Git returned bytes that are not blob {blob}")
        found[path] = data
        position = end + 1 + size + 1
    return found


def read_pinned_files(root: Path, manifest: list[tuple[str, str, str]]) -> tuple[dict[str, bytes], dict[str, int]]:
    """Returns the pinned bytes of every file: from the working tree when it holds the pinned blob, else from Git."""
    content, elsewhere = {}, []
    for path, _, blob in manifest:
        try:
            data = (root / path).read_bytes()
        except OSError:
            data = None
        if data is not None and git_blob_id(data) == blob:
            content[path] = data
        else:
            elsewhere.append((path, blob))
    if elsewhere:
        content.update(read_git_objects(root, elsewhere))
    return content, {"working_tree": len(manifest) - len(elsewhere), "git_objects": len(elsewhere)}


def excluded(path: str) -> bool:
    """True when one of the producer's four exclusion pathspecs matches the path."""
    return any(path == prefix or path.startswith(prefix + "/") for prefix in EXCLUDED_PREFIXES) or EXCLUDED_INFIX in path


def owned_by(ref: str, paths: list[str]) -> bool:
    """The producer's own test: the file is one of the artifact's citation paths, or lies under one."""
    return any(ref == p.rstrip("/") or ref.startswith(p.rstrip("/") + "/") for p in paths)


def is_tracked(path: str, tracked: list[str]) -> bool:
    """What `git ls-files -- <path>` answers: the path is a tracked file or a folder that holds one."""
    path = path.rstrip("/")
    return any(name == path or name.startswith(path + "/") for name in tracked)


def citation_paths(entry: dict, tracked: list[str]) -> tuple[list[str] | None, str | None, str | None]:
    """The producer's citation_paths(): (paths, where they come from, reason when the entry cannot be measured)."""
    if "citation_paths" in entry:
        paths = entry["citation_paths"]
        if not isinstance(paths, list) or not all(isinstance(p, str) and p for p in paths):
            raise ExtractError(f"unexpected citation_paths for {entry.get('artifact')!r}")
        if not paths:
            return None, "citation_paths", "citation_paths is empty (the producer's mark for an artifact outside this repository)"
        if not all(is_tracked(p, tracked) for p in paths):
            return None, "citation_paths", "a citation path is not tracked"
        return paths, "citation_paths", None
    if is_tracked(entry["artifact"], tracked):
        return [entry["artifact"]], "artifact", None
    return None, "artifact", "artifact is not a tracked path and no citation_paths given"


def read_records(content: dict[str, bytes], tracked: list[str]) -> list[dict]:
    """Returns the evolution records in the producer's order, each with its citation paths."""
    records = []
    for path in sorted(content):
        if not (path.startswith(EVOLUTION_DIR + "/") and path.endswith(".evolution.json") and path.count("/") == 2):
            continue
        entry = json.loads(content[path].decode("utf-8"))
        metrics = entry.get("metrics") if isinstance(entry, dict) else None
        if not isinstance(metrics, dict) or not isinstance(entry.get("artifact"), str) \
                or type(metrics.get("citation_count")) is not int:
            raise ExtractError(f"{path}: no artifact name or no integer metrics.citation_count")
        paths, origin, reason = citation_paths(entry, tracked)
        for p in paths or []:
            if " " in p or spaced(p) == p or "/".join(part.strip() for part in spaced(p).split("/")) != p:
                raise ExtractError(f"{path}: a citation path cannot be written as a spaced label and read back")
        records.append({"file": path, "entry": entry, "paths": paths, "origin": origin, "reason": reason})
    if not records:
        raise ExtractError(f"no *.evolution.json file in {EVOLUTION_DIR}")
    return records


def find_hits(content: dict[str, bytes], needles: list[str]) -> dict[str, set[str]]:
    """Returns, for each citation path, the non-excluded files that contain it as a literal string (git grep -lF)."""
    searched = {path: data for path, data in content.items() if not excluded(path)}
    return {needle: {path for path, data in searched.items() if needle.encode("utf-8") in data} for needle in needles}


def count_for(paths: list[str], hits: dict[str, set[str]]) -> set[str]:
    """The producer's measure(): the files that contain any of the paths, minus the artifact's own files."""
    return {ref for p in paths for ref in hits[p] if not owned_by(ref, paths)}


def artifact_rows(records: list[dict], hits: dict[str, set[str]], path_keys: dict[str, str]) -> list[dict]:
    """Returns one row per evolution record: its label, its paths, the recorded metrics and the recount."""
    rows, keys = [], iter(KEYS)
    for record in records:
        entry, paths = record["entry"], record["paths"]
        metrics = entry["metrics"]
        row = {
            "key": next(keys) if paths else None,
            "record": record["file"],
            "artifact": spaced(entry["artifact"]),
            "artifact_type": entry.get("artifact_type"),
            "created_at": entry.get("created_at"),
            "measurable": paths is not None,
            "unmeasurable_reason": record["reason"],
            "citation_paths_from": record["origin"],
            "citation_paths": [spaced(p) for p in paths or []],
            "path_keys": "".join(path_keys[p] for p in paths or []),
            "recorded": {key: metrics.get(key) for key in (
                "citation_count", "citation_source", "last_cited", "promotion_candidate", "deprecation_candidate")},
            "recount": None,
        }
        if paths:
            refs = count_for(paths, hits)
            containing = set().union(*(hits[p] for p in paths))
            row["recount"] = {"files": len(refs),
                              "files_by_path": [len({ref for ref in hits[p] if not owned_by(ref, paths)}) for p in paths],
                              "own_files_containing_a_path": len(containing) - len(refs)}
        rows.append(row)
    return rows


def planted_controls(records: list[dict], hits: dict[str, set[str]], needles: list[str], content: dict) -> dict:
    """Applies the rule to the pinned tree plus one planted file, for four placements of that file."""
    listing = "\n".join(needles).encode("utf-8")
    spaced_listing = "\n".join(spaced(needle) for needle in needles).encode("utf-8")
    cases = {
        "file_listing_every_path": ("zz-planted/every-path.txt", listing),
        "same_file_in_an_excluded_folder": (EVOLUTION_DIR + "/zz-planted.txt", listing),
        "same_file_under_an_archived_folder": ("zz-planted" + EXCLUDED_INFIX + "every-path.txt", listing),
        "file_listing_every_spaced_label": ("zz-planted/every-label.txt", spaced_listing),
    }
    measurable = [record["paths"] for record in records if record["paths"]]
    before = [len(count_for(paths, hits)) for paths in measurable]
    out = {}
    for name, (path, data) in cases.items():
        if path in content:
            raise ExtractError(f"control path {path} exists in the pinned tree")
        planted = {needle: files | ({path} if not excluded(path) and needle.encode("utf-8") in data else set())
                   for needle, files in hits.items()}
        raises = [len(count_for(paths, planted)) - old for paths, old in zip(measurable, before)]
        out[name] = {"counts_raised": sum(r > 0 for r in raises), "largest_raise": max(raises),
                     "sum_of_raises": sum(raises)}
    searched = [data for path, data in content.items() if not excluded(path)]
    out["pinned_files_containing_a_spaced_label"] = sum(
        any(spaced(needle).encode("utf-8") in data for needle in needles) for data in searched)
    return out


def locate(lines: list[str], wanted: list[str], where: str) -> int:
    """Returns the 1-based line number where the wanted lines occur consecutively; exactly one place must match."""
    stripped = [line.strip() for line in lines]
    found = [i for i in range(len(stripped) - len(wanted) + 1) if stripped[i:i + len(wanted)] == wanted]
    if len(found) != 1:
        raise ExtractError(f"{where}: expected one occurrence of {wanted[0]!r}, found {len(found)}")
    return found[0] + 1


def metrics_policy_path(needles: list[str]) -> str:
    """The full path of the compounding-metrics policy: the one citation path that ends with its file name."""
    found = [needle for needle in needles if needle.endswith("/" + METRICS_POLICY)]
    if len(found) != 1:
        raise ExtractError(f"expected one citation path ending with {METRICS_POLICY}, found {len(found)}")
    return found[0]


def quoted_passages(content: dict[str, bytes], metrics_policy: str) -> dict:
    """Returns each quoted passage with the line numbers it has in the pinned file."""
    out = {}
    for name, (source, wanted) in QUOTES.items():
        path = metrics_policy if source == METRICS_POLICY else source
        first = locate(content[path].decode("utf-8").splitlines(), wanted, f"{spaced(path)} ({name})")
        out[name] = {"file": spaced(path) if source == METRICS_POLICY else path, "first_line": first,
                     "last_line": first + len(wanted) - 1, "text": wanted}
    return out


def power_law_section(quotes: dict, metrics_policy: str) -> dict:
    """Returns the numbers of the rule that calls a concentration of citations healthy, read from the quoted lines."""
    rule = re.search(r"top (\d+)% of governance artifacts account for more than (\d+)% of citations",
                     quotes["power_law_detection_rule"]["text"][0])
    policy = re.search(r"Top (\d+)% of governance artifacts account for > (\d+)% of citations",
                       quotes["metrics_policy_rule"]["text"][0])
    share = quotes["metrics_policy_share"]["text"]
    target = re.fullmatch(r'target: "([0-9.]+)–([0-9.]+)"', share[2])
    alert = re.fullmatch(r'alert: "> ([0-9.]+) \(fragile concentration\)"', share[3])
    if not (rule and policy and target and alert) or rule.groups() != policy.groups():
        raise ExtractError("the two statements of the power-law rule do not give the same thresholds")
    return {"rule_file": POWER_LAW_RULE, "policy_file": spaced(metrics_policy),
            "top_percent": int(rule.group(1)), "share_above_percent": int(rule.group(2)),
            "policy_target_share": [float(target.group(1)), float(target.group(2))],
            "policy_alert_above_share": float(alert.group(1)),
            "population": "the citation_count of every evolution record (detection_source of the policy)"}


def read_trend(content: dict[str, bytes]) -> list[dict]:
    """Returns every row of the quality trend in file order, after checking its shape."""
    rows, seen = [], set()
    for path in sorted(p for p in content if p.startswith(TREND_DIR + "/") and p.endswith(".jsonl")):
        for number, line in enumerate(content[path].decode("utf-8").splitlines(), 1):
            where = f"{path}:{number}"
            row = json.loads(line)
            if not isinstance(row, dict) or not isinstance(row.get("artifact"), str) \
                    or not isinstance(row.get("timestamp"), str) or not TIMESTAMP.match(row["timestamp"]):
                raise ExtractError(f"{where}: no artifact or no UTC timestamp")
            if type(row.get("delta_citations")) is not int or type(row.get("citation_count", 0)) is not int:
                raise ExtractError(f"{where}: delta_citations or citation_count is not an integer")
            if "citation_count" not in row and row["delta_citations"] != 0:
                raise ExtractError(f"{where}: a non-zero delta_citations without a citation_count")
            if (row["timestamp"], row["artifact"]) in seen:
                raise ExtractError(f"{where}: second row for {row['artifact']!r} at {row['timestamp']}")
            seen.add((row["timestamp"], row["artifact"]))
            rows.append(row)
    if not rows:
        raise ExtractError(f"no row in {TREND_DIR}")
    return rows


def trend_section(rows: list[dict], artifacts: list[dict]) -> dict:
    """Returns the counts of the log, its rows with a non-zero delta_citations, and its latest run."""
    previous, non_zero = {}, []
    for row in sorted(rows, key=lambda r: r["timestamp"]):
        before = previous.get(row["artifact"])
        if row.get("delta_citations"):
            non_zero.append({
                "run": row["timestamp"], "artifact": spaced(row["artifact"]), "delta_citations": row["delta_citations"],
                "citation_count": row["citation_count"],
                "previous_row": "none" if before is None else "no count" if "citation_count" not in before else "count",
                "previous_count": (before or {}).get("citation_count"),
                "citation_source": row.get("citation_source"), "rebaseline": row.get("rebaseline", False)})
        previous[row["artifact"]] = row
    latest = max(row["timestamp"] for row in rows)
    latest_counts = {spaced(row["artifact"]): row["citation_count"] for row in rows if row["timestamp"] == latest}
    recorded = {a["artifact"]: a["recorded"]["citation_count"] for a in artifacts}
    return {
        "rows": len(rows), "runs": len({row["timestamp"] for row in rows}),
        "artifacts": len({row["artifact"] for row in rows}),
        "rows_with_a_citation_count": sum("citation_count" in row for row in rows),
        "rows_with_a_non_zero_delta_citations": non_zero,
        "latest_run": {"timestamp": latest, "rows": len(latest_counts),
                       "sum_of_citation_counts": sum(latest_counts.values()),
                       "equal_to_the_evolution_records": latest_counts == recorded},
    }


def policy_section(content: dict[str, bytes], quotes: dict) -> dict:
    """Returns the numbers of the anti-LOLLI policy the lesson uses, read from the quoted lines."""
    def number(name: str, line: int) -> float:
        return float(quotes[name]["text"][line].split(":")[1].split("#")[0])
    history = json.loads(content[HISTORY].decode("utf-8"))
    if not isinstance(history, list) or not all(isinstance(cycle, dict) for cycle in history):
        raise ExtractError(f"{HISTORY}: expected a list of cycles")
    return {
        "file": POLICY,
        "zero_citation_window_days": int(number("policy_zero_rule", 0)),
        "ratio_bands": {"healthy_below": number("policy_healthy", 1),
                        "watch_from": number("policy_watch", 1), "watch_to": number("policy_watch", 2),
                        "warning_from": number("policy_warning", 1), "warning_to": number("policy_warning", 2),
                        "freeze_from": number("policy_freeze", 1),
                        "freeze_after_consecutive_cycles": int(number("policy_freeze", 2))},
        "history_file": HISTORY,
        "history_cycles": [{"cycle": c.get("cycle"), "timestamp": c.get("timestamp"), "method": c.get("method"),
                            "lolli_count": c.get("lolli_count"), "ergol_count": c.get("ergol_count"),
                            "ratio": c.get("ratio"), "ratio_status": c.get("ratio_status"),
                            "artifacts_deleted": c.get("actions", {}).get("deleted"),
                            "deleted_artifacts_listed": len(c.get("deleted_artifacts", []))} for c in history],
    }


def correction_note(content: dict[str, bytes]) -> dict:
    """Returns the note in which one evolution record corrects a reading of its own count of 0."""
    entry = json.loads(content[CORRECTED_RECORD].decode("utf-8"))
    events = [e for e in entry.get("events", []) if str(e.get("context", "")).startswith(CORRECTION)]
    if len(events) != 1:
        raise ExtractError(f"{CORRECTED_RECORD}: expected one event starting with the quoted correction")
    return {"record": CORRECTED_RECORD, "artifact": spaced(entry["artifact"]), "event_type": events[0]["type"],
            "event_timestamp": events[0]["timestamp"], "quote": CORRECTION,
            "quote_is": "the first sentences of the event's context; the rest of the context is not copied"}


def source_section(manifest: list[tuple[str, str, str]], records: list[dict], content: dict,
                   metrics_policy: str) -> dict:
    """Returns the 'source' section: the pinned commit, its manifest, and the blob id of every file read by name."""
    blob = {path: blob_id for path, _, blob_id in manifest}
    trend = sorted(p for p in content if p.startswith(TREND_DIR + "/") and p.endswith(".jsonl"))
    named = ([(PRODUCER, "the producer of citation_count"), (FEEDER, "the feeder of the quality trend"),
              (POLICY, "the policy that reads the count"), (HISTORY, "the policy's history file"),
              (POWER_LAW_RULE, "the rule that calls a concentration of citations healthy"),
              (metrics_policy, "the policy that sets a target for that concentration (a citation path, written spaced)")]
             + [(record["file"], "evolution record") for record in records]
             + [(path, "quality-trend rows") for path in trend])
    modes = sorted({mode for _, mode, _ in manifest})
    return {
        "repository": "GuitarAlchemist/Demerzel",
        "commit": PINNED_COMMIT,
        "tree": PINNED_TREE,
        "commit_check": "git ls-tree -r <commit> gave the manifest below, and every byte searched has the blob id "
                        "that manifest records for its path",
        "manifest": {"command": f"git ls-tree -r {PINNED_COMMIT}", "files": len(manifest),
                     "files_by_mode": {mode: sum(m == mode for _, m, _ in manifest) for mode in modes},
                     "sha256": MANIFEST_SHA256,
                     "sha256_of": "the lines '<blob id> <path>' sorted by path bytes, each ended by a line feed"},
        "files": [{"path": spaced(path) if path == metrics_policy else path, "git_blob": blob[path], "role": role}
                  for path, role in named],
    }


def build(root: Path) -> tuple[dict, dict[str, int]]:
    """Returns the snapshot written to observed-input.json and where each pinned file was read from."""
    manifest = pinned_manifest(root)
    content, read_from = read_pinned_files(root, manifest)
    tracked = [path for path, _, _ in manifest]
    records = read_records(content, tracked)
    needles = list(dict.fromkeys(p for record in records for p in record["paths"] or []))
    path_keys = {needle: KEYS[i].lower() for i, needle in enumerate(needles)}
    hits = find_hits(content, needles)
    artifacts = artifact_rows(records, hits, path_keys)
    files_with_a_path = sorted(set().union(*hits.values()))
    metrics_policy = metrics_policy_path(needles)
    quotes = quoted_passages(content, metrics_policy)
    snapshot = {
        "schema_version": "0.1.0",
        "module_id": "psy-020-goodhart-and-reflexivity",
        "kind": "observed",
        "label_convention": "Artifact names, citation paths and the paths of files found by the search are data "
                            "labels, written with a space on each side of every slash: a tracked file that "
                            "contained them literally would be counted as a citation by the rule studied here. "
                            "The paths under 'source' and 'quoted_passages' are files this fixture reads by name; "
                            "the one among them that is a citation path (the compounding-metrics policy) is "
                            "written spaced too.",
        "source": source_section(manifest, records, content, metrics_policy),
        "producer_rule": {
            "script": PRODUCER,
            "exclusion_pathspecs": list(EXCLUDED),
            "reimplemented_as": "a file is searched when its path is not one of state/evolution, "
                                "state/quality-trend, governance-manifest.json, does not lie under one of them and "
                                "does not contain '/archived/'; it is counted for an artifact when its bytes contain "
                                "one of the artifact's citation paths and it is not that path or a file under it",
        },
        "scan": {
            "tracked_files": len(manifest),
            "files_excluded_by_the_pathspecs": sum(excluded(path) for path in tracked),
            "files_searched": sum(not excluded(path) for path in tracked),
            "bytes_searched": sum(len(data) for path, data in content.items() if not excluded(path)),
            "citation_paths_listed": sum(len(record["paths"] or []) for record in records),
            "distinct_citation_paths": len(needles),
            "files_containing_a_path": len(files_with_a_path),
            "controls": planted_controls(records, hits, needles, content),
        },
        "citation_paths": [{"key": path_keys[needle], "path": spaced(needle), "files_containing_it": len(hits[needle])}
                           for needle in needles],
        "artifacts": artifacts,
        "files_containing_a_path": {
            spaced(path): "".join(path_keys[needle] for needle in needles if path in hits[needle])
            for path in files_with_a_path},
        "quality_trend": trend_section(read_trend(content), artifacts),
        "quoted_passages": quotes,
        "policy": policy_section(content, quotes),
        "power_law_rule": power_law_section(quotes, metrics_policy),
        "correction_note": correction_note(content),
    }
    return snapshot, read_from


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--repo-root", type=Path, default=HERE.parents[4])
    parser.add_argument("--output", type=Path, default=HERE / "observed-input.json")
    args = parser.parse_args()
    try:
        snapshot, read_from = build(args.repo_root.resolve())
        text = json.dumps(snapshot, ensure_ascii=False, indent=2) + "\n"
        literal = [p["key"] for p in snapshot["citation_paths"]
                   if "/".join(part.strip() for part in p["path"].split("/")) in text]
        if literal:
            raise ExtractError(f"the snapshot would contain citation paths literally (keys {literal})")
    except (ExtractError, OSError, UnicodeDecodeError, KeyError, ValueError) as exc:
        print(f"extract.py: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 1
    args.output.write_bytes(text.encode("utf-8"))
    scan = snapshot["scan"]
    counted = sum(a["recount"]["files"] for a in snapshot["artifacts"] if a["measurable"])
    print(f"extract.py: {scan['tracked_files']} files at the pin ({read_from['working_tree']} read from the working "
          f"tree, {read_from['git_objects']} from Git objects), {scan['distinct_citation_paths']} citation paths, "
          f"{counted} counted file-artifact pairs -> {args.output.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
