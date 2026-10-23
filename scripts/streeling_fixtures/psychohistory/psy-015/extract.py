#!/usr/bin/env python3
"""PSY-015 extract: snapshot what the repository records about beliefs, their holders and their sources.

Reads the Psychohistory department record, the belief files under
state/beliefs/ (current and archived, and the one YAML file next to them), the
two record types the repository defines for an agent's beliefs (belief
snapshot, knowledge state) with their sample files, one audit note, and the
ML-feedback path: the schema of a recommendation message, the integrity fields
such a message carries, and the script that writes two belief files from a
message. It then tests every JSON file under state/ (the course library
state/streeling/ excluded) for the shape of either record type, for the keys
that name a sender or a receiver, and for the ids of the messages the belief
files cite, and writes observed-input.json next to this script. The analysis
script reads only that snapshot.

Fails with a non-zero exit and a message when a source file is missing, has an
unexpected shape, or is not the file of the pinned commit.

Run from the repository root:
    python -I scripts/streeling_fixtures/psychohistory/psy-015/extract.py
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
from pathlib import Path

# This program lives under scripts/ (CONTRIBUTING.md: no executable code outside scripts/); its data stays
# under state/streeling/fixtures/. FIXTURE_FILE is the path the program would have next to that data.
FIXTURE_FILE = (Path(__file__).resolve().parents[4]
                / "state/streeling/fixtures/psychohistory/psy-015" / Path(__file__).name)

PINNED_COMMIT = "4b03838800dcd4894f1e026461979bff1d985ca8"
DEPARTMENT = "state/streeling/departments/psychohistory.department.json"
BELIEF_DIRS = {"current": "state/beliefs", "archived": "state/beliefs/archived"}
YAML_BELIEFS = "state/beliefs/3d-visualization-aesthetics.yaml"
# A model its header names: an evidence source names it when the name occurs anywhere in the source text.
YAML_MODEL_NAMES = ("GPT-4o",)
# The two record types the repository defines for "which agent holds which belief".
RECORD_TYPES = {
    "belief_snapshot": {
        "schema": "schemas/contracts/belief-snapshot.schema.json",
        "samples": ["examples/sample-data/belief-snapshot-tars.json"],
    },
    "knowledge_state": {
        "schema": "logic/knowledge-state.schema.json",
        "samples": ["examples/sample-data/knowledge-state-in-progress.json",
                    "examples/sample-data/knowledge-state-learned.json"],
    },
}
AUDIT = "state/snapshots/2026-07-25-audit-level1.snapshot.json"
AUDIT_CHECK = "audit-1-4-knowledge-state-schema"
# The ML-feedback path: the schema of a recommendation message, the integrity fields every message carries,
# the script that writes belief files from a message, and the folder the messages arrive in.
FEEDBACK_SCHEMA = "schemas/contracts/ml-feedback-recommendation.schema.json"
INTEGRITY_SCHEMA = "schemas/contracts/integrity-fields.schema.json"
FEEDBACK_SCRIPT = "scripts/apply_ml_feedback.py"
FEEDBACK_INBOX = "state/oversight/ml-recommendations"
# What the script must contain for "the belief repeats the message" to hold: each statement once per belief file.
COPY_STATEMENTS = {
    "the evidence source is the message id": "\"source\": f\"ml-feedback-recommendation {doc['message_id']}\",",
    "the evidence claim is the message's rationale": '"claim": doc["recommendation"]["rationale"],',
    "the belief's confidence is the message's confidence": '"confidence": doc["confidence"],',
    "the evaluator written is demerzel": '"evaluated_by": "demerzel",',
}
# The repository's citation counter looks for these paths as literal strings in every tracked file. In the JSON
# written here they are spelled with a space on each side of every slash, so that a data file never counts.
GOVERNED_PATHS = (FEEDBACK_SCRIPT,)
# An evidence source "names a contract message" when its first word is the stem of a schema in this folder.
CONTRACTS_FOLDER, CONTRACT_SUFFIX = "schemas/contracts", ".schema.json"
CONTRACT_FILES = 11
# SHA-256 of the lines "<blob id> <path>\n", sorted by path bytes. Reproduce with:
#   git ls-tree -r <pin> -- schemas/contracts | awk '{print $3" "$4}' | sha256sum
CONTRACTS_MANIFEST_SHA256 = "022a88b77e7193451759883c3c17eb092bc32893372a6a74b3f0ab67757953f6"
# Keys by which the schemas read here name who sent something or who received it: the integrity fields of a
# message, the teacher and the learner of a knowledge state, and the key the feedback script writes.
SENDER_KEYS = ("origin_repo", "origin_agent", "taught_by", "learner", "source_recommendation")
# Every *.json file under SCAN_FOLDER, SCAN_EXCLUDED left out, is tested for the shape of a record type.
SCAN_FOLDER, SCAN_EXCLUDED = "state", "state/streeling"
SCAN_FILES = 722
# Same recipe as above, restricted to those files:
#   git ls-tree -r <pin> -- state | awk '{print $3" "$4}' | grep '\.json$' | grep -v ' state/streeling/' | sha256sum
SCAN_MANIFEST_SHA256 = "15a968afe2bc206e4d1af7e5b167d13413215be090da9980a607d3fca820ac04"
# Git blob ids at PINNED_COMMIT (git ls-tree -r <pin> -- <path>). A blob id is
# sha1(b"blob <size>\0" + content) over the LF-normalised bytes.
PINNED_BLOBS = {
    DEPARTMENT: "67f81dd22dd5c17a6eb41174dd5944475ce2dd6b",
    "schemas/contracts/belief-snapshot.schema.json": "d0f2375fcccdb3fa166571aac518ecb41d15fb0c",
    "examples/sample-data/belief-snapshot-tars.json": "9398211ee99395206037b9fed0d02167571cd863",
    "logic/knowledge-state.schema.json": "25af00539cc73f31e5b118d3ac3509ccb41005ae",
    "examples/sample-data/knowledge-state-in-progress.json": "737a945af379ce68e363546bc7461b61bbf89307",
    "examples/sample-data/knowledge-state-learned.json": "77cb2df4505585fc820edc7fce1fada9502b7e05",
    AUDIT: "bea908790bff871d4b76c23448c53dddd57e7e60",
    "state/beliefs/2026-03-17-behavioral-test-coverage.belief.json": "e3a939adbc63a60032746f1433712ed3d9b55b16",
    "state/beliefs/2026-03-17-demerzel-framework-integrity.belief.json": "daeaceacec87cfde36ddc1358f25c3da03e15608",
    "state/beliefs/2026-03-18-consumer-repo-integration-status.belief.json": "b1cadad26b81e529a8bd8a26c3f5f7a90fcd975f",
    "state/beliefs/2026-07-25-cross-reference-integrity.belief.json": "3c32763a77b41c1c45809abef7571046190b03f9",
    "state/beliefs/2026-07-25-schema-conformance.belief.json": "dc1af29f79532ba4fb6713017e4b292786b8382a",
    "state/beliefs/2026-07-29-afk-backend-adapter.belief.json": "e64466803ae06524f058f3d392c7bcad0e379e60",
    "state/beliefs/confidence-calibration.belief.json": "d49c70d92766bb8ddafc4a77421e663080f77fd0",
    "state/beliefs/remediation-effectiveness.belief.json": "d0347afd888f94026f9971053bb8054ef053a155",
    "state/beliefs/archived/2026-03-17-consumer-repo-integration-status.belief.json": "765a1370f8fadc4dba08857224edb6b1469daab7",
    "state/beliefs/archived/2026-03-17-ga-governance-integration.belief.json": "d0f496d814572325a7ba07ff171a83292e74c583",
    "state/beliefs/archived/2026-03-17-ix-governance-integration.belief.json": "bf556f12baabcad64daaf5389cae4700905c114b",
    "state/beliefs/archived/2026-03-17-tars-governance-integration.belief.json": "83b47c5b58b4363efc6db02fbc55bb49e2b2e197",
    "state/beliefs/archived/slot-blue-health.belief.json": "e1e646c10676d1d26cfe22e092bc6502734d32c2",
    "state/beliefs/archived/slot-green-health.belief.json": "2c38b22117b1e6b666ba53ac916b26b77a080e7e",
    "state/beliefs/archived/visual-displacement-terrain.belief.json": "d844a5ca8684e870ec8ff68e447537a0eaa88869",
    "state/beliefs/archived/visual-earth-clouds.belief.json": "baa0b191aa716a3e8515b6c15dba8036bd6b724c",
    "state/beliefs/archived/visual-earth-snow.belief.json": "d15603a89190687e320921a1b4459dfdaab6321f",
    "state/beliefs/archived/visual-earth-terminator.belief.json": "787b9f6a54fe901ca474aadef0a2f4a6c6f89831",
    "state/beliefs/archived/visual-milky-way-parallax.belief.json": "2c45a8a983af964a23beca4e5ffe0a277d8d9342",
    "state/beliefs/archived/visual-planet-proportions.belief.json": "b702ae2b804251b5f212f522bacfe0bf5e735335",
    "state/beliefs/archived/visual-sun-flare.belief.json": "bb8d104a1f985a971b649e0b02048cd2f09e8d47",
    YAML_BELIEFS: "c239e1041ae51f3e3cb2244f16c9977652f5d214",
    FEEDBACK_SCHEMA: "51b5dbe317d173e5c8e99f867ecdad4e3459e9d8",
    INTEGRITY_SCHEMA: "7ce9baeced930deeac2397e0e01c1b7bc983b8d0",
    FEEDBACK_SCRIPT: "a161edf2ce11ae822562f05e4f4b3f8d8d2e0f81",
}
TRUTH_VALUES = ("T", "P", "U", "D", "F", "C")
PRINCIPLE_COUNTS = re.compile(r"(\d+) personas across (\d+) repos")


class ExtractError(Exception):
    """A source file is missing, malformed, or not the pinned one."""


def git_blob_id(data: bytes) -> str:
    """Blob id Git stores for this content once CRLF is normalised to LF."""
    data = data.replace(b"\r\n", b"\n")
    return hashlib.sha1(b"blob %d\x00" % len(data) + data).hexdigest()


def read_text(root: Path, rel: str) -> tuple[str, str]:
    """A file's text with LF line endings, and its Git blob id."""
    path = root / rel
    if not path.is_file():
        raise ExtractError(f"missing file: {rel}")
    data = path.read_bytes()
    try:
        return data.replace(b"\r\n", b"\n").decode("utf-8"), git_blob_id(data)
    except UnicodeDecodeError as exc:
        raise ExtractError(f"{rel}: not UTF-8 ({exc})") from exc


def read_json(root: Path, rel: str) -> tuple[object, str]:
    """A JSON file's value, and its Git blob id."""
    text, blob = read_text(root, rel)
    try:
        return json.loads(text), blob
    except json.JSONDecodeError as exc:
        raise ExtractError(f"{rel}: not JSON ({exc})") from exc


def read_object(root: Path, rel: str) -> tuple[dict, str]:
    """A JSON file that must hold an object, and its Git blob id."""
    value, blob = read_json(root, rel)
    if not isinstance(value, dict):
        raise ExtractError(f"{rel}: not a JSON object")
    return value, blob


def spaced(text: str) -> str:
    """Data-label spelling: a space on each side of every slash (see GOVERNED_PATHS)."""
    return " / ".join(text.split("/")).rstrip()


def key_names(value: object, found: set[str]) -> set[str]:
    """Every key name used anywhere in a JSON value."""
    if isinstance(value, dict):
        for key, item in value.items():
            found.add(key)
            key_names(item, found)
    elif isinstance(value, list):
        for item in value:
            key_names(item, found)
    return found


def values_of(value: object, wanted: str, found: list) -> list:
    """Every value stored under the key `wanted`, anywhere in a JSON value."""
    if isinstance(value, dict):
        for key, item in value.items():
            if key == wanted:
                found.append(item)
            values_of(item, wanted, found)
    elif isinstance(value, list):
        for item in value:
            values_of(item, wanted, found)
    return found


def manifest_of(root: Path, paths: list[str]) -> str:
    """SHA-256 of the lines '<blob id> <path>' for these files, in the order given."""
    digest = hashlib.sha256()
    for rel in paths:
        digest.update(f"{read_text(root, rel)[1]} {rel}\n".encode("utf-8"))
    return digest.hexdigest()


def mentions_of_belief(entries: object, where: str) -> list[dict]:
    """The entries of a list of the department record that mention 'belief', with their position."""
    if not isinstance(entries, list) or not all(isinstance(entry, str) for entry in entries):
        raise ExtractError(f"{DEPARTMENT}: {where} is not a list of strings")
    return [{"position": position, "of": len(entries), "text": entry}
            for position, entry in enumerate(entries, 1) if "belief" in entry.lower()]


def department_record(root: Path) -> tuple[dict, dict]:
    """What the department record says about beliefs and about the number of personas."""
    record, blob = read_object(root, DEPARTMENT)
    for key in ("department", "head_persona", "research_areas", "curriculum", "consumer_repos", "key_principle"):
        if key not in record:
            raise ExtractError(f"{DEPARTMENT}: missing key {key!r}")
    principle = record["key_principle"]
    counts = PRINCIPLE_COUNTS.search(principle) if isinstance(principle, str) else None
    if counts is None:
        raise ExtractError(f"{DEPARTMENT}: key_principle no longer says '<n> personas across <m> repos'")
    areas = mentions_of_belief(record["research_areas"], "research_areas")
    if not areas:
        raise ExtractError(f"{DEPARTMENT}: no research area mentions belief")
    return {
        "path": DEPARTMENT,
        "department": record["department"],
        "head_persona": record["head_persona"],
        "research_areas": len(record["research_areas"]),
        "research_areas_that_mention_belief": areas,
        "curriculum_entries": len(record["curriculum"]),
        "curriculum_entries_that_mention_belief": mentions_of_belief(record["curriculum"], "curriculum"),
        "key_principle": principle,
        "personas_in_key_principle": int(counts.group(1)),
        "repos_in_key_principle": int(counts.group(2)),
        "consumer_repos": record["consumer_repos"],
    }, {"path": DEPARTMENT, "git_blob": blob, "role": "department record"}


def contract_schemas(root: Path) -> dict:
    """The message types the repository defines: one schema file each under schemas/contracts/."""
    folder = root / CONTRACTS_FOLDER
    if not folder.is_dir():
        raise ExtractError(f"missing directory: {CONTRACTS_FOLDER}")
    names = sorted((path.name for path in folder.iterdir() if path.is_file()), key=lambda name: name.encode("utf-8"))
    return {
        "folder": CONTRACTS_FOLDER, "files": len(names),
        "manifest_sha256": manifest_of(root, [f"{CONTRACTS_FOLDER}/{name}" for name in names]),
        "manifest_recipe": "git ls-tree -r " + PINNED_COMMIT + " -- " + CONTRACTS_FOLDER
                           + " | awk '{print $3\" \"$4}' | sha256sum",
        "names": [name[:-len(CONTRACT_SUFFIX)] for name in names if name.endswith(CONTRACT_SUFFIX)],
    }


def belief_file(root: Path, rel: str, group: str, contracts: list[str], seen: dict) -> tuple[dict, dict]:
    """One row for a *.belief.json file: its proposition, its evaluator and what its evidence names as a source."""
    belief, blob = read_object(root, rel)
    for key, kind in (("proposition", str), ("truth_value", str), ("confidence", (int, float)),
                      ("evidence", dict), ("last_updated", str), ("evaluated_by", str)):
        if not isinstance(belief.get(key), kind) or isinstance(belief.get(key), bool):
            raise ExtractError(f"{rel}: key {key!r} is missing or has an unexpected type")
    if belief["truth_value"] not in TRUTH_VALUES:
        raise ExtractError(f"{rel}: unexpected truth_value {belief['truth_value']!r}")
    if not 0 <= belief["confidence"] <= 1:
        raise ExtractError(f"{rel}: confidence {belief['confidence']!r} is outside 0..1")
    if not belief["evaluated_by"].strip() or not belief["proposition"].strip():
        raise ExtractError(f"{rel}: empty proposition or evaluated_by")
    items = {}
    for side in ("supporting", "contradicting"):
        items[side] = belief["evidence"].get(side)
        if not isinstance(items[side], list) or not all(isinstance(item, dict) for item in items[side]):
            raise ExtractError(f"{rel}: evidence.{side} is not a list of objects")
    every_item = items["supporting"] + items["contradicting"]
    named = [word for word in (str(item.get("source")).split(" ")[0] for item in every_item) if word in contracts]
    key_names(belief, seen["key_names"])
    seen["propositions"].add(belief["proposition"])
    return {
        "path": rel,
        "group": group,
        "proposition": spaced(belief["proposition"]),
        "truth_value": belief["truth_value"],
        "confidence": belief["confidence"],
        "evaluated_by": belief["evaluated_by"],
        "last_updated": belief["last_updated"],
        "supporting_items": len(items["supporting"]),
        "contradicting_items": len(items["contradicting"]),
        "evidence_sources": sorted({str(item.get("source")) for item in every_item}),
        "items_whose_source_names_a_contract_message": len(named),
        "contract_messages_named": sorted(set(named)),
        "source_recommendation": sorted(str(value) for value in values_of(belief, "source_recommendation", [])),
    }, {"path": rel, "git_blob": blob, "role": f"{group} belief file"}


def belief_files(root: Path, contracts: list[str]) -> tuple[list[dict], list[dict], dict, dict]:
    """Every *.belief.json file of the two belief folders, and the names of the other files found there."""
    rows, entries, others = [], [], {}
    seen = {"key_names": set(), "propositions": set()}
    for group, folder in BELIEF_DIRS.items():
        directory = root / folder
        if not directory.is_dir():
            raise ExtractError(f"missing directory: {folder}")
        listing = sorted(path.name for path in directory.iterdir() if path.is_file())
        others[folder] = [name for name in listing if not name.endswith(".belief.json")]
        for name in listing:
            if name.endswith(".belief.json"):
                row, entry = belief_file(root, f"{folder}/{name}", group, contracts, seen)
                rows.append(row)
                entries.append(entry)
    return rows, entries, others, seen


def yaml_belief_file(root: Path) -> tuple[dict, dict]:
    """The one YAML file of state/beliefs/. The standard library has no YAML parser: lines are counted by pattern."""
    text, blob = read_text(root, YAML_BELIEFS)
    lines = text.split("\n")
    header = []
    while len(header) < len(lines) and lines[len(header)].startswith("#"):
        header.append(lines[len(header)][1:].strip())
    sources = [source.strip().strip('"') for source in re.findall(r"(?m)^\s+- source:(.*)$", text)]
    entries = len(re.findall(r"(?m)^\s+- id:", text))
    if not header or not entries or not sources or len(sources) != len(re.findall(r"(?m)^\s+claim:", text)):
        raise ExtractError(f"{YAML_BELIEFS}: no header comment, no '- id:' entry, or sources and claims do not pair")
    tally: dict[str, int] = {}
    for source in sources:
        tally[source] = tally.get(source, 0) + 1
    repeated = sorted(((count, source) for source, count in tally.items() if count > 1), key=lambda pair: (-pair[0], pair[1]))
    return {
        "path": YAML_BELIEFS,
        "read_as": "text: lines counted by pattern ('- id:', '- source:', 'claim:', 'evaluated_by:')",
        "header_comments": header,
        "belief_entries": entries,
        "evidence_items": len(sources),
        "distinct_sources": len(tally),
        "sources_named_more_than_once": {source: count for count, source in repeated},
        "evidence_items_whose_source_names": {name: sum(name in source for source in sources)
                                              for name in YAML_MODEL_NAMES},
        "lines_with_evaluated_by": len(re.findall(r"(?m)^\s*evaluated_by:", text)),
    }, {"path": YAML_BELIEFS, "git_blob": blob, "role": "YAML file in the current belief folder"}


def shapes_of(value: object, required: dict[str, list[str]]) -> list[str]:
    """Record types whose required keys this JSON value holds (or an element of it, when it is a list)."""
    candidates = value if isinstance(value, list) else [value]
    return [name for name, keys in required.items()
            if any(isinstance(item, dict) and all(key in item for key in keys) for item in candidates)]


def sample_row(name: str, rel: str, sample: dict, shapes: list[str]) -> dict:
    """What a sample file of a record type says about its holder, its teacher and the belief before and after."""
    row = {"path": rel, "id": sample["id"], "shape_test": shapes,
           "sender_keys": sorted(set(SENDER_KEYS) & key_names(sample, set()))}
    if name == "belief_snapshot":
        row.update({"repo": sample["repo"], "agent": sample["agent"], "snapshot_at": sample["snapshot_at"],
                    "beliefs": len(sample["beliefs"])})
    else:
        assessment = sample["assessment"]
        row.update({"concept": sample["concept"], "taught_by": sample["taught_by"],
                    "learner": sample["learner"]["identifier"], "created_at": sample.get("created_at"),
                    "truth_value_before": assessment["belief_state_before"]["truth_value"],
                    "truth_value_after": assessment["belief_state_after"]["truth_value"],
                    "outcome": assessment["outcome"]})
    return row


def record_types(root: Path) -> tuple[dict, list[dict], dict[str, list[str]]]:
    """The schemas and sample files of the two record types, each sample checked against the shape test."""
    described, entries, required = {}, [], {}
    for name, spec in RECORD_TYPES.items():
        schema, blob = read_object(root, spec["schema"])
        if (not isinstance(schema.get("required"), list) or not schema["required"]
                or not isinstance(schema.get("properties"), dict)):
            raise ExtractError(f"{spec['schema']}: no 'required' list or no 'properties' object")
        required[name] = schema["required"]
        entries.append({"path": spec["schema"], "git_blob": blob, "role": f"schema of the {name} record type"})
        described[name] = {"schema_path": spec["schema"], "title": schema.get("title"),
                           "description": schema.get("description"), "required_keys": schema["required"],
                           "properties": list(schema["properties"]), "samples": []}
        if name == "knowledge_state":
            teacher = schema["properties"].get("taught_by")
            described[name]["taught_by_default"] = teacher.get("default") if isinstance(teacher, dict) else None
    for name, spec in RECORD_TYPES.items():
        for rel in spec["samples"]:
            sample, blob = read_object(root, rel)
            shapes = shapes_of(sample, required)
            if shapes != [name]:
                raise ExtractError(f"{rel}: expected the shape of a {name} only, the shape test says {shapes}")
            entries.append({"path": rel, "git_blob": blob, "role": f"sample file of the {name} record type"})
            described[name]["samples"].append(sample_row(name, rel, sample, shapes))
    return described, entries, required


def audit_note(root: Path) -> tuple[dict, dict]:
    """The audit check that looked for knowledge-state instances, with its own count and note."""
    audit, blob = read_object(root, AUDIT)
    found = [item for item in audit.get("checks", []) if isinstance(item, dict) and item.get("id") == AUDIT_CHECK]
    if len(found) != 1 or not isinstance(found[0].get("scanned"), int) or not isinstance(found[0].get("note"), str):
        raise ExtractError(f"{AUDIT}: check {AUDIT_CHECK!r} is missing or has an unexpected shape")
    return ({"path": AUDIT, "date": audit.get("date"), "auditor": audit.get("auditor"), "check": AUDIT_CHECK,
             "scanned": found[0]["scanned"], "note": found[0]["note"]},
            {"path": AUDIT, "git_blob": blob, "role": "audit note on knowledge-state instances"})


def feedback_path(root: Path) -> tuple[dict, list[dict]]:
    """The message type that belief files cite, and the script that writes belief files from such a message."""
    schema, schema_blob = read_object(root, FEEDBACK_SCHEMA)
    integrity, integrity_blob = read_object(root, INTEGRITY_SCHEMA)
    referenced = [part.get("$ref") for part in schema.get("allOf", []) if isinstance(part, dict)]
    pipelines = schema.get("properties", {}).get("pipeline_id", {}).get("enum")
    if (Path(INTEGRITY_SCHEMA).name not in referenced or not isinstance(integrity.get("required"), list)
            or not isinstance(schema.get("description"), str) or not isinstance(pipelines, list)):
        raise ExtractError(f"{FEEDBACK_SCHEMA}: no description, no pipeline_id list, or no reference to the integrity fields")
    senders = [key for key in integrity["required"] if key.startswith("origin_")]
    if not senders or not set(senders) <= set(SENDER_KEYS):
        raise ExtractError(f"{INTEGRITY_SCHEMA}: the required origin_ keys {senders} are not all in SENDER_KEYS")
    script, script_blob = read_text(root, FEEDBACK_SCRIPT)
    docstring = re.search(r'"""(.*?)"""', script, re.S)
    written = sorted(set(re.findall(r'"beliefs" / "([^"]+\.belief\.json)"', script)))
    statements = [{"meaning": meaning, "statement": code, "occurrences": script.count(code)}
                  for meaning, code in COPY_STATEMENTS.items()]
    if docstring is None or not written or any(row["occurrences"] != len(written) for row in statements):
        raise ExtractError(f"{FEEDBACK_SCRIPT}: no docstring, no belief file written, or a copying statement "
                           f"does not occur once per belief file written ({written}, {statements})")
    return {
        "message_schema": {"path": FEEDBACK_SCHEMA, "title": schema.get("title"), "description": schema["description"],
                           "pipelines": pipelines, "integrity_fields_required": integrity["required"],
                           "keys_that_name_the_sender": senders},
        "applying_script": {"path": spaced(FEEDBACK_SCRIPT),
                            "first_paragraph_of_its_docstring": " ".join(docstring.group(1).strip().split("\n\n")[0].split()),
                            "belief_files_it_writes": written, "statements": statements},
        "inbox": {"folder": FEEDBACK_INBOX, "exists": (root / FEEDBACK_INBOX).is_dir()},
    }, [{"path": FEEDBACK_SCHEMA, "git_blob": schema_blob, "role": "schema of a recommendation message"},
        {"path": INTEGRITY_SCHEMA, "git_blob": integrity_blob, "role": "integrity fields required in every message"},
        {"path": FEEDBACK_SCRIPT, "git_blob": script_blob, "role": "script that writes belief files from a message"}]


def scan_state(root: Path, required: dict[str, list[str]], message_ids: list[str]) -> dict:
    """Test every JSON file under state/ (course library excluded): record shapes, sender keys, cited message ids."""
    folder = root / SCAN_FOLDER
    if not folder.is_dir():
        raise ExtractError(f"missing directory: {SCAN_FOLDER}")
    paths = []
    for current, folders, files in os.walk(folder):
        rel_dir = Path(current).relative_to(root).as_posix()
        folders[:] = [name for name in folders if f"{rel_dir}/{name}" != SCAN_EXCLUDED]
        paths += [f"{rel_dir}/{name}" for name in files if name.endswith(".json")]
    paths.sort(key=lambda rel: rel.encode("utf-8"))
    manifest = hashlib.sha256()
    found = {name: [] for name in required}
    with_key = {key: [] for key in SENDER_KEYS}
    with_id = {message_id: [] for message_id in message_ids}
    for rel in paths:
        value, blob = read_json(root, rel)
        manifest.update(f"{blob} {rel}\n".encode("utf-8"))
        for name in shapes_of(value, required):
            found[name].append(rel)
        names, dumped = key_names(value, set()), json.dumps(value)
        for key in SENDER_KEYS:
            if key in names:
                with_key[key].append(rel)
        for message_id in message_ids:
            if message_id in dumped:
                with_id[message_id].append(rel)
    return {
        "folder": SCAN_FOLDER, "excluded": SCAN_EXCLUDED, "pattern": "*.json", "files": len(paths),
        "manifest_sha256": manifest.hexdigest(),
        "manifest_recipe": "git ls-tree -r " + PINNED_COMMIT + " -- state | awk '{print $3\" \"$4}' | grep '\\.json$' "
                           "| grep -v ' state/streeling/' | sha256sum",
        "shape_test": "a JSON object (or an element of a top-level list) that holds every key the record type's "
                      "schema lists under 'required'",
        "files_with_the_shape": found,
        "state_knowledge_folder_exists": (root / "state/knowledge").exists(),
        "files_with_a_sender_key": with_key,
        "files_that_hold_a_cited_message_id": with_id,
        "json_files_in_the_recommendation_inbox": [rel for rel in paths if rel.startswith(FEEDBACK_INBOX + "/")],
    }


def drift_report(files: list[dict], scan: dict, contracts: dict) -> list[str]:
    """Every difference between what was read and what the pinned commit holds."""
    drift = [f"{entry['path']} is blob {entry['git_blob']}, pinned {PINNED_BLOBS.get(entry['path'], 'nothing: not in the pinned list')}"
             for entry in files if PINNED_BLOBS.get(entry["path"]) != entry["git_blob"]]
    drift += [f"{path} is pinned but was not found" for path in sorted(set(PINNED_BLOBS) - {entry["path"] for entry in files})]
    if (scan["files"], scan["manifest_sha256"]) != (SCAN_FILES, SCAN_MANIFEST_SHA256):
        drift.append(f"{SCAN_FOLDER}/ (without {SCAN_EXCLUDED}/) holds {scan['files']} JSON files with manifest "
                     f"{scan['manifest_sha256']}, pinned {SCAN_FILES} files with manifest {SCAN_MANIFEST_SHA256}")
    if (contracts["files"], contracts["manifest_sha256"]) != (CONTRACT_FILES, CONTRACTS_MANIFEST_SHA256):
        drift.append(f"{CONTRACTS_FOLDER}/ holds {contracts['files']} files with manifest {contracts['manifest_sha256']}, "
                     f"pinned {CONTRACT_FILES} files with manifest {CONTRACTS_MANIFEST_SHA256}")
    return drift


def counts_of(files: list[dict], beliefs: list[dict], others: dict, seen: dict, scan: dict, contracts: dict) -> dict:
    """The counts section: how many files were read, and how many belief files name a contract message."""
    citing = [row for row in beliefs if row["contract_messages_named"]]
    kinds = sorted({kind for row in citing for kind in row["contract_messages_named"]})
    return {
        "files_read_one_by_one": len(files),
        "belief_files": {group: sum(row["group"] == group for row in beliefs) for group in BELIEF_DIRS},
        "other_files_in_the_belief_folders": others,
        "distinct_propositions": len(seen["propositions"]),
        "contract_schemas": len(contracts["names"]),
        "belief_files_whose_evidence_names_a_contract_message": {
            group: sum(row["group"] == group for row in citing) for group in BELIEF_DIRS},
        "belief_files_by_contract_message_named": {
            kind: sum(kind in row["contract_messages_named"] for row in citing) for kind in kinds},
        "json_files_tested_for_a_record_shape": scan["files"],
    }


def build(root: Path, allow_drift: bool) -> dict:
    """Read every source, refuse a source that is not the pinned one, and assemble the snapshot."""
    department, department_entry = department_record(root)
    types, type_entries, required = record_types(root)
    audit, audit_entry = audit_note(root)
    contracts = contract_schemas(root)
    beliefs, belief_entries, others, seen = belief_files(root, contracts["names"])
    yaml_file, yaml_entry = yaml_belief_file(root)
    feedback, feedback_entries = feedback_path(root)
    files = [department_entry] + type_entries + [audit_entry] + belief_entries + [yaml_entry] + feedback_entries
    scan = scan_state(root, required, sorted({value for row in beliefs for value in row["source_recommendation"]}))
    drift = drift_report(files, scan, contracts)
    if drift and not allow_drift:
        raise ExtractError("source files are not those of commit " + PINNED_COMMIT + ":\n  " + "\n  ".join(drift)
                           + "\n(--allow-drift snapshots them anyway; the lesson's numbers then no longer apply)")
    return {
        "schema_version": "0.2.0",
        "module_id": "psy-015-belief-contagion-small-population",
        "kind": "observed",
        "source": {
            "repository": "GuitarAlchemist/Demerzel",
            "commit": None if drift else PINNED_COMMIT,
            "commit_check": ("FAILED: " + "; ".join(drift)) if drift else
                            "every file below has the Git blob id recorded for this commit (CRLF normalised to LF), the "
                            "two belief folders hold no *.belief.json file outside this list, and the two listed "
                            "folders have the pinned file count and manifest digest",
            "slash_note": "The path of a governed file and the belief propositions are written with a space on each "
                          "side of every slash: the repository counts as a citation every tracked file that holds "
                          "the path of a governed file as a literal string, and a data file must not move that count.",
            "files": [dict(entry, path=spaced(entry["path"])) if entry["path"] in GOVERNED_PATHS else entry
                      for entry in files],
            "scanned_folder": {key: scan[key] for key in ("folder", "excluded", "pattern", "files", "manifest_sha256",
                                                          "manifest_recipe")},
            "contract_schemas_folder": {key: contracts[key] for key in ("folder", "files", "manifest_sha256",
                                                                        "manifest_recipe")},
        },
        "counts": counts_of(files, beliefs, others, seen, scan, contracts),
        "department_record": department,
        "belief_files": beliefs,
        "key_names_used_in_the_belief_files": sorted(seen["key_names"]),
        "yaml_belief_file": yaml_file,
        "contract_schema_names": contracts["names"],
        "feedback_path": feedback,
        "record_types": types,
        "record_shape_scan": {key: scan[key] for key in ("shape_test", "files_with_the_shape",
                                                         "state_knowledge_folder_exists")},
        "sender_scan": {
            "keys": list(SENDER_KEYS),
            "files_with_a_sender_key": scan["files_with_a_sender_key"],
            "files_that_hold_a_cited_message_id": scan["files_that_hold_a_cited_message_id"],
            "json_files_in_the_recommendation_inbox": scan["json_files_in_the_recommendation_inbox"],
        },
        "audit_note": audit,
    }


def main() -> int:
    """Write observed-input.json next to this script (or to --output); exit 1 with a message on any refusal."""
    here = FIXTURE_FILE
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--repo-root", type=Path, default=here.parents[5])
    parser.add_argument("--output", type=Path, default=here.with_name("observed-input.json"))
    parser.add_argument("--allow-drift", action="store_true",
                        help="snapshot source files that differ from the pinned commit")
    args = parser.parse_args()
    try:
        snapshot = build(args.repo_root.resolve(), args.allow_drift)
    except (ExtractError, OSError, KeyError, TypeError) as exc:
        print(f"extract.py: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 1
    text = json.dumps(snapshot, ensure_ascii=False, indent=2) + "\n"
    args.output.write_bytes(text.encode("utf-8"))
    counts = snapshot["counts"]
    citing = sum(counts["belief_files_whose_evidence_names_a_contract_message"].values())
    print(f"extract.py: {counts['files_read_one_by_one']} files read one by one "
          f"({counts['belief_files']['current']} current and {counts['belief_files']['archived']} archived belief files, "
          f"{citing} of which name a contract message as a source), "
          f"{counts['json_files_tested_for_a_record_shape']} JSON files tested for a record shape -> {args.output.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
