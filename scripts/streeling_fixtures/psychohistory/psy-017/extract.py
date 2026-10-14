#!/usr/bin/env python3
"""PSY-017 extract: snapshot the calibration belief and what it rests on.

Reads state/beliefs/confidence-calibration.belief.json, the other belief files
of state/beliefs/ and state/beliefs/archived/, and the three files that state
the nudge rule (the feedback policy, the pipeline specification and the script
that applies a recommendation), and writes observed-input.json next to this
script. The analysis script reads only that snapshot.

Fails with a non-zero exit and a message when a source file is missing, has an
unexpected shape, or is not the file of the pinned commit, and when a belief
folder holds a *.belief.json file that the pinned commit does not have.

Run from the repository root:
    python -I -B scripts/streeling_fixtures/psychohistory/psy-017/extract.py
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
                / "state/streeling/fixtures/psychohistory/psy-017" / Path(__file__).name)

PINNED_COMMIT = "4b03838800dcd4894f1e026461979bff1d985ca8"
BELIEFS, ARCHIVED = "state/beliefs", "state/beliefs/archived"
FOCUS = f"{BELIEFS}/confidence-calibration.belief.json"
POLICY = "policies/ml-governance-feedback-policy.yaml"
PIPELINE = "pipelines/ml-feedback-loop.ixql"
APPLIER = "scripts/apply_ml_feedback.py"
# Two files of the belief folders that the producer's *.belief.json glob does not read.
YAML_BELIEFS = f"{BELIEFS}/3d-visualization-aesthetics.yaml"
LEDGER = f"{ARCHIVED}/SUPERSEDED.md"
# Git blob ids at PINNED_COMMIT (git ls-tree). A blob id is
# sha1(b"blob <size>\0" + content) over the LF-normalised bytes.
PINNED_BLOBS = {
    f"{BELIEFS}/2026-03-17-behavioral-test-coverage.belief.json": "e3a939adbc63a60032746f1433712ed3d9b55b16",
    f"{BELIEFS}/2026-03-17-demerzel-framework-integrity.belief.json": "daeaceacec87cfde36ddc1358f25c3da03e15608",
    f"{BELIEFS}/2026-03-18-consumer-repo-integration-status.belief.json": "b1cadad26b81e529a8bd8a26c3f5f7a90fcd975f",
    f"{BELIEFS}/2026-07-25-cross-reference-integrity.belief.json": "3c32763a77b41c1c45809abef7571046190b03f9",
    f"{BELIEFS}/2026-07-25-schema-conformance.belief.json": "dc1af29f79532ba4fb6713017e4b292786b8382a",
    f"{BELIEFS}/2026-07-29-afk-backend-adapter.belief.json": "e64466803ae06524f058f3d392c7bcad0e379e60",
    FOCUS: "d49c70d92766bb8ddafc4a77421e663080f77fd0",
    f"{BELIEFS}/remediation-effectiveness.belief.json": "d0347afd888f94026f9971053bb8054ef053a155",
    f"{ARCHIVED}/2026-03-17-consumer-repo-integration-status.belief.json": "765a1370f8fadc4dba08857224edb6b1469daab7",
    f"{ARCHIVED}/2026-03-17-ga-governance-integration.belief.json": "d0f496d814572325a7ba07ff171a83292e74c583",
    f"{ARCHIVED}/2026-03-17-ix-governance-integration.belief.json": "bf556f12baabcad64daaf5389cae4700905c114b",
    f"{ARCHIVED}/2026-03-17-tars-governance-integration.belief.json": "83b47c5b58b4363efc6db02fbc55bb49e2b2e197",
    f"{ARCHIVED}/slot-blue-health.belief.json": "e1e646c10676d1d26cfe22e092bc6502734d32c2",
    f"{ARCHIVED}/slot-green-health.belief.json": "2c38b22117b1e6b666ba53ac916b26b77a080e7e",
    f"{ARCHIVED}/visual-displacement-terrain.belief.json": "d844a5ca8684e870ec8ff68e447537a0eaa88869",
    f"{ARCHIVED}/visual-earth-clouds.belief.json": "baa0b191aa716a3e8515b6c15dba8036bd6b724c",
    f"{ARCHIVED}/visual-earth-snow.belief.json": "d15603a89190687e320921a1b4459dfdaab6321f",
    f"{ARCHIVED}/visual-earth-terminator.belief.json": "787b9f6a54fe901ca474aadef0a2f4a6c6f89831",
    f"{ARCHIVED}/visual-milky-way-parallax.belief.json": "2c45a8a983af964a23beca4e5ffe0a277d8d9342",
    f"{ARCHIVED}/visual-planet-proportions.belief.json": "b702ae2b804251b5f212f522bacfe0bf5e735335",
    f"{ARCHIVED}/visual-sun-flare.belief.json": "bb8d104a1f985a971b649e0b02048cd2f09e8d47",
    POLICY: "40d14b0010d054fcddf08d5f6cafccc0dd98e5f5",
    PIPELINE: "9accc1feb81db2ffcafd5d36494b2457a7fd3994",
    APPLIER: "a161edf2ce11ae822562f05e4f4b3f8d8d2e0f81",
    YAML_BELIEFS: "c239e1041ae51f3e3cb2244f16c9977652f5d214",
    LEDGER: "2acfe58fde7380836921f3a50ee24464e0589f0b",
}
LABELS = ("T", "P", "U", "D", "F", "C")
CLAIM = re.compile(
    r"^(?P<revised>\d+) of (?P<high>\d+) high-confidence beliefs \(>= (?P<line>[0-9.]+)\) were later revised "
    r"\(overconfidence_rate=(?P<rate>[0-9.]+)\)\. Revisions evidenced by archived prior versions: (?P<files>.+?)\. "
    r"Nudge magnitude capped at \+/-(?P<cap>[0-9.]+)/cycle per ml-governance-feedback-policy\.$")
FEEDBACK_SOURCE = "ml-feedback-recommendation "
# Lines of the three rule files that the lesson quotes: key -> (pattern, capture names).
POLICY_BLOCK = "  confidence_calibrator:"
POLICY_LINES = {
    "overconfidence_rate": (r'^\s*- overconfidence_rate: "(?P<definition>[^"]+)"$', ("definition",)),
    "underconfidence_rate": (r'^\s*- underconfidence_rate: "(?P<definition>[^"]+)"$', ("definition",)),
    "action": (r"^\s*action: (?P<value>.+)$", ("value",)),
    "frequency": (r"^\s*frequency: (?P<value>\w+)$", ("value",)),
    "guardrail": (r"^\s*guardrail: Threshold adjustments cannot exceed \+/- (?P<cap>[0-9.]+) per cycle$", ("cap",)),
}
PIPELINE_LINES = {
    "overconfidence_trigger": (r"filter\(r\.overconfidence_rate > (?P<trigger>[0-9.]+)\)", ("trigger",)),
    "overconfidence_formula": (r'formula: "max\(-(?P<cap>[0-9.]+), -1 \* overconfidence_rate \* (?P<gain>[0-9.]+)\)"',
                               ("cap", "gain")),
    "underconfidence_trigger": (r"filter\(r\.underconfidence_rate > (?P<trigger>[0-9.]+)\)", ("trigger",)),
    "underconfidence_formula": (r'formula: "min\((?P<cap>[0-9.]+), underconfidence_rate \* (?P<gain>[0-9.]+)\)"',
                                ("cap", "gain")),
}
APPLIER_BLOCK = "def _apply_nudge("
APPLIER_CONSTANTS = {
    "producer_named_in_the_header": (r"The companion producer \((?P<producer>[^)]+)\) emits$", ("producer",)),
    "nudge_cap": (r"^NUDGE_CAP = (?P<value>[0-9.]+)\b", ("value",)),
    "auto_apply_confidence": (r"^CONF_AUTO_APPLY = (?P<value>[0-9.]+)\b", ("value",)),
}
APPLIER_LINES = {
    "clamp_of_one_nudge": (r"^\s*nudge = max\(-NUDGE_CAP, min\(NUDGE_CAP, raw\)\)", ()),
    "clamp_of_the_running_total": (r"^\s*new_total = max\(-NUDGE_CAP, min\(NUDGE_CAP, round\(prior \+ nudge, 4\)\)\)$", ()),
    "truth_value_written": (r'^\s*"truth_value": "P",\s+# (?P<comment>.+)$', ("comment",)),
    "confidence_written": (r'^\s*"confidence": doc\["confidence"\],$', ()),
    "source_written": (r'^\s*"source": f"ml-feedback-recommendation \{doc\[\'message_id\'\]\}",$', ()),
    "claim_written": (r'^\s*"claim": doc\["recommendation"\]\["rationale"\],$', ()),
    "reliability_written": (r'^\s*"reliability": doc\["confidence"\],$', ()),
    "applied_delta_written": (r'^\s*"applied_delta": round\(new_total - prior, 4\),$', ()),
}


# The same script writes a second belief file from a recommendation; the lesson counts it among the six.
SECOND_BLOCK = "def _apply_remediation_rates("
SECOND_LINES = {
    "second_belief_file_written": (r'belief_path = root / "state" / "beliefs" / "(?P<file>[^"]+)"$', ("file",)),
    "second_confidence_written": (r'^\s*"confidence": doc\["confidence"\],$', ()),
    "second_source_written": (r'^\s*"source": f"ml-feedback-recommendation \{doc\[\'message_id\'\]\}",$', ()),
}


LEDGER_LINES = {
    "retired_not_deleted": (r"^Beliefs in this directory are retired, not deleted\.", ()),
    "placeholders": (r"^Nine placeholder belief scaffolds were archived here", ()),
}
YAML_ITEM = re.compile(r"^  - id: (?P<id>\S+)$")
YAML_FIELDS = {"truth_value": re.compile(r"^    truth_value: (?P<value>[A-Z])$"),
               "confidence": re.compile(r"^    confidence: (?P<value>[0-9.]+)$")}


class ExtractError(Exception):
    """A source file is missing, malformed, or not the pinned one."""


def label(text: str) -> str:
    """A repository path as a data label: a space on each side of every slash (the README says why)."""
    return " / ".join(part.strip() for part in text.split("/"))


def git_blob_id(data: bytes) -> str:
    """Blob id Git stores for this content once CRLF is normalised to LF."""
    data = data.replace(b"\r\n", b"\n")
    return hashlib.sha1(b"blob %d\x00" % len(data) + data).hexdigest()


def read_source(root: Path, rel: str, files: list[dict], role: str) -> bytes:
    path = root / rel
    if not path.is_file():
        raise ExtractError(f"missing file: {rel}")
    data = path.read_bytes()
    files.append({"path": rel, "git_blob": git_blob_id(data), "role": role})
    return data


def belief_paths(root: Path) -> dict[str, list[str]]:
    """The *.belief.json files of the two folders, as the producer of the record lists them (sorted by name)."""
    found = {}
    for folder in (BELIEFS, ARCHIVED):
        if not (root / folder).is_dir():
            raise ExtractError(f"missing directory: {folder}")
        found[folder] = [f"{folder}/{path.name}" for path in sorted((root / folder).glob("*.belief.json"))]
    return found


def read_belief(rel: str, data: bytes, group: str) -> dict:
    try:
        belief = json.loads(data.decode("utf-8"))
    except json.JSONDecodeError as exc:
        raise ExtractError(f"{rel}: not JSON ({exc})") from exc
    if not isinstance(belief, dict):
        raise ExtractError(f"{rel}: not a JSON object")
    for key in ("proposition", "truth_value", "confidence", "evidence", "last_updated", "evaluated_by"):
        if key not in belief:
            raise ExtractError(f"{rel}: missing key {key!r}")
    confidence, evidence = belief["confidence"], belief["evidence"]
    if isinstance(confidence, bool) or not isinstance(confidence, (int, float)) or not 0 <= confidence <= 1:
        raise ExtractError(f"{rel}: unexpected confidence {confidence!r}")
    if belief["truth_value"] not in LABELS:
        raise ExtractError(f"{rel}: unexpected truth_value {belief['truth_value']!r}")
    if not isinstance(evidence, dict) or not all(isinstance(evidence.get(k), list) for k in ("supporting", "contradicting")):
        raise ExtractError(f"{rel}: evidence is not an object with supporting and contradicting lists")
    sources = [item.get("source", "") for item in evidence["supporting"] if isinstance(item, dict)]
    return {
        "path": label(rel), "group": group, "proposition": label(belief["proposition"]), "truth_value": belief["truth_value"],
        "confidence": confidence, "last_updated": belief["last_updated"], "evaluated_by": belief["evaluated_by"],
        "supporting_items": len(evidence["supporting"]), "contradicting_items": len(evidence["contradicting"]),
        "resolved_contradictions": len(belief.get("resolved_contradictions", [])),
        "every_supporting_source_is_an_ml_feedback_recommendation":
            bool(sources) and all(source.startswith(FEEDBACK_SOURCE) for source in sources),
        "previous_value": belief.get("previous_value"), "refresh_note": belief.get("refresh_note"),
    }


def focus_record(rel: str, data: bytes) -> dict:
    """The calibration belief, with the sentence it rests on split into its numbers."""
    belief = json.loads(data.decode("utf-8"))
    supporting, calibration = belief["evidence"]["supporting"], belief.get("calibration")
    if len(supporting) != 1 or not all(key in supporting[0] for key in ("source", "claim", "timestamp", "reliability")):
        raise ExtractError(f"{rel}: expected one supporting item with source, claim, timestamp and reliability")
    wanted = ("threshold_nudge", "applied_delta", "prior_nudge", "cap", "source_recommendation", "rationale")
    if not isinstance(calibration, dict) or list(calibration) != list(wanted):
        raise ExtractError(f"{rel}: calibration block does not have the keys {wanted}")
    match = CLAIM.match(supporting[0]["claim"])
    if not match:
        raise ExtractError(f"{rel}: the supporting claim does not have the expected wording")
    return {
        "path": label(rel), "proposition": belief["proposition"], "truth_value": belief["truth_value"],
        "confidence": belief["confidence"], "last_updated": belief["last_updated"], "evaluated_by": belief["evaluated_by"],
        "supporting": [{key: supporting[0][key] for key in ("source", "claim", "timestamp", "reliability")}],
        "contradicting_items": len(belief["evidence"]["contradicting"]),
        "calibration": calibration,
        "claim_equals_calibration_rationale": supporting[0]["claim"] == calibration["rationale"],
        "claim_parsed": {
            "revised": int(match["revised"]), "high_confidence_beliefs": int(match["high"]),
            "high_confidence_line": match["line"], "overconfidence_rate": match["rate"],
            "archived_prior_versions": match["files"].split(", "), "cap_per_cycle": match["cap"]},
    }


def quote_lines(rel: str, lines: list[str], wanted: dict, first: int = 0, stop: int | None = None) -> dict:
    """For each key, the single line of lines[first:stop] that matches its pattern: number, text and captures."""
    quotes = {}
    for key, (pattern, names) in wanted.items():
        regex = re.compile(pattern)
        hits = [(number, line) for number, line in enumerate(lines[first:stop], first + 1) if regex.search(line)]
        if len(hits) != 1:
            raise ExtractError(f"{rel}: expected one line for {key!r}, found {len(hits)}")
        number, line = hits[0]
        match = regex.search(line)
        quotes[key] = {"line": number, "text": line.strip()} | {name: match[name] for name in names}
    return quotes


def block(rel: str, lines: list[str], header: str, next_prefix: re.Pattern) -> tuple[int, int]:
    """Index range of the block that starts at the line `header` and ends before the next line matching next_prefix."""
    starts = [index for index, line in enumerate(lines) if line.startswith(header)]
    if len(starts) != 1:
        raise ExtractError(f"{rel}: expected one line starting with {header!r}, found {len(starts)}")
    start = starts[0]
    stop = next((index for index in range(start + 1, len(lines)) if next_prefix.match(lines[index])), len(lines))
    return start, stop


def rule_files(root: Path, files: list[dict]) -> dict:
    policy = read_source(root, POLICY, files, "policy that defines the rate and caps the adjustment").decode("utf-8").splitlines()
    pipeline = read_source(root, PIPELINE, files, "pipeline specification with the trigger and the formula").decode("utf-8").splitlines()
    applier = read_source(root, APPLIER, files, "script that writes the calibration belief").decode("utf-8").splitlines()
    first, stop = block(POLICY, policy, POLICY_BLOCK, re.compile(r"^  \S"))
    oversight = {"human_oversight": (r"^\s*- Human oversight of the feedback loop is required at least (?P<value>\w+)$",
                                     ("value",))}
    start, end = block(APPLIER, applier, APPLIER_BLOCK, re.compile(r"^def "))
    second = block(APPLIER, applier, SECOND_BLOCK, re.compile(r"^(def |# |_)"))
    return {
        "policy": {"path": label(POLICY), "block": POLICY_BLOCK.strip(),
                   "quotes": quote_lines(POLICY, policy, POLICY_LINES, first, stop) | quote_lines(POLICY, policy, oversight)},
        "pipeline": {"path": label(PIPELINE), "quotes": quote_lines(PIPELINE, pipeline, PIPELINE_LINES)},
        "applier": {"path": label(APPLIER), "function": APPLIER_BLOCK.rstrip("("),
                    "quotes": quote_lines(APPLIER, applier, APPLIER_CONSTANTS)
                    | quote_lines(APPLIER, applier, APPLIER_LINES, start, end)
                    | quote_lines(APPLIER, applier, SECOND_LINES, *second)},
    }


def yaml_beliefs(rel: str, text: str) -> list[dict]:
    """Id, truth value and confidence of each item of a YAML list of beliefs, read line by line (no YAML library)."""
    lines, items = text.splitlines(), []
    starts = [index for index, line in enumerate(lines) if YAML_ITEM.match(line)] + [len(lines)]
    for start, stop in zip(starts, starts[1:]):
        row = {"id": YAML_ITEM.match(lines[start])["id"]}
        for key, regex in YAML_FIELDS.items():
            found = [regex.match(line)["value"] for line in lines[start:stop] if regex.match(line)]
            if len(found) != 1:
                raise ExtractError(f"{rel}: item {row['id']} has {len(found)} {key} lines")
            row[key] = found[0] if key == "truth_value" else float(found[0])
        if row["truth_value"] not in LABELS or not 0 <= row["confidence"] <= 1:
            raise ExtractError(f"{rel}: item {row['id']} has an unexpected truth value or confidence")
        items.append(row)
    if not items:
        raise ExtractError(f"{rel}: no belief items found")
    return items


def unread_files(root: Path, files: list[dict]) -> dict:
    yaml_text = read_source(root, YAML_BELIEFS, files, "YAML list of beliefs, not read by the producer").decode("utf-8")
    ledger = read_source(root, LEDGER, files, "ledger of the archived folder, not a belief file").decode("utf-8")
    return {
        "note": "Files of the two belief folders that the producer's *.belief.json glob does not read.",
        "yaml_beliefs": {"path": label(YAML_BELIEFS), "items": yaml_beliefs(YAML_BELIEFS, yaml_text)},
        "archive_ledger": {"path": label(LEDGER), "quotes": quote_lines(LEDGER, ledger.splitlines(), LEDGER_LINES)},
    }


def drift_report(files: list[dict], on_disk: dict[str, list[str]]) -> list[str]:
    """Every way the files read differ from the pinned commit; empty when they are the pinned ones."""
    drift = [f"{entry['path']} is blob {entry['git_blob']}, pinned {PINNED_BLOBS.get(entry['path'])}"
             for entry in files if PINNED_BLOBS.get(entry["path"]) != entry["git_blob"]]
    read = {entry["path"] for entry in files}
    drift += [f"{path} is pinned but was not read" for path in sorted(set(PINNED_BLOBS) - read)]
    for folder, paths in on_disk.items():
        pinned = sorted(path for path in PINNED_BLOBS if path.rsplit("/", 1)[0] == folder and path.endswith(".belief.json"))
        if paths != pinned:
            drift.append(f"{folder} holds {len(paths)} *.belief.json files, the pinned commit has {len(pinned)}")
    return drift


def build(root: Path, allow_drift: bool) -> dict:
    files: list[dict] = []
    on_disk = belief_paths(root)
    beliefs, focus = [], None
    for folder, group in ((BELIEFS, "current"), (ARCHIVED, "archived")):
        for rel in on_disk[folder]:
            data = read_source(root, rel, files, f"{group} belief file")
            beliefs.append(read_belief(rel, data, group))
            if rel == FOCUS:
                focus = focus_record(rel, data)
    if focus is None:
        raise ExtractError(f"missing file: {FOCUS}")
    rules = rule_files(root, files)
    unread = unread_files(root, files)
    drift = drift_report(files, on_disk)
    if drift and not allow_drift:
        raise ExtractError("source files are not those of commit " + PINNED_COMMIT + ":\n  " + "\n  ".join(drift)
                           + "\n(--allow-drift snapshots them anyway; the lesson's numbers then no longer apply)")
    return {
        "schema_version": "0.1.0",
        "module_id": "psy-017-calibration-with-six-observations",
        "kind": "observed",
        "source": {
            "repository": "GuitarAlchemist/Demerzel",
            "commit": None if drift else PINNED_COMMIT,
            "commit_check": ("FAILED: " + "; ".join(drift)) if drift else
                            "every file below has the Git blob id recorded for this commit (CRLF normalised to LF), and "
                            "the two belief folders hold no other *.belief.json file",
            "path_format": "repository paths are written with a space on each side of every slash",
            "belief_files_per_folder": {label(folder): len(paths) for folder, paths in on_disk.items()},
            "files": [dict(entry, path=label(entry["path"])) for entry in files],
        },
        "calibration_belief": focus,
        "belief_files": beliefs,
        "rule": rules,
        "not_read_by_the_producer": unread,
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
    except (ExtractError, OSError, UnicodeDecodeError, json.JSONDecodeError, KeyError, TypeError) as exc:
        print(f"extract.py: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 1
    text = json.dumps(snapshot, ensure_ascii=False, indent=2) + "\n"
    args.output.write_bytes(text.encode("utf-8"))
    parsed = snapshot["calibration_belief"]["claim_parsed"]
    print(f"extract.py: {len(snapshot['belief_files'])} belief files, claim {parsed['revised']} of "
          f"{parsed['high_confidence_beliefs']}, {len(snapshot['source']['files'])} pinned files -> {args.output.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
