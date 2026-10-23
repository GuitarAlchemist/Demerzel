#!/usr/bin/env python3
"""PSY-004 extract: snapshot the department's claim and what the repository holds.

Reads the Psychohistory department record, the persona files, the council
verdicts and their schema, and the two files that define the tribunal panel,
and writes observed-input.json next to this script. The analysis script reads
only that snapshot, never the repository.

Fails with a non-zero exit and a message when a source file is missing, has an
unexpected shape, or is not the file of the pinned commit, or when the folder
of tribunal verdicts, absent from the pinned commit, holds a file.

Run from the repository root:
    python -I scripts/streeling_fixtures/psychohistory/psy-004/extract.py
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
                / "state/streeling/fixtures/psychohistory/psy-004" / Path(__file__).name)

PINNED_COMMIT = "4b03838800dcd4894f1e026461979bff1d985ca8"
DEPARTMENT_RECORD = "state/streeling/departments/psychohistory.department.json"
PERSONA_DIR, PERSONA_SUFFIX = "personas", ".persona.yaml"
COUNCIL_DIR, COUNCIL_PATTERN, COUNCIL_IGNORED = "state/council", "council-*.json", {".gitkeep"}
COUNCIL_SCHEMA = "schemas/council-verdict.schema.json"
PANEL_WORKFLOW = ".github/workflows/tribunal-panel.yml"
PANEL_SCRIPT = ".claude/workflows/demerzel-tribunal-panel.js"
# Git blob ids at PINNED_COMMIT (git ls-tree -r <commit> -- <path>). A blob id
# is sha1(b"blob <size>\0" + content) over the LF-normalised bytes.
PINNED_BLOBS = {
    DEPARTMENT_RECORD: "67f81dd22dd5c17a6eb41174dd5944475ce2dd6b",
    "personas/communal-steward.persona.yaml": "63c5c4de7af972119b117b91fa17595f50624511",
    "personas/composer-agent.persona.yaml": "f8a1ebce9fc2cd96728abd491e367f9e03325dd7",
    "personas/convolution-agent.persona.yaml": "260c9f114ebfdd02f17217ffa008d5b94561ab91",
    "personas/critical-theorist.persona.yaml": "f4b78a186ff5fdd9b4070ec0001623a2181b9c1d",
    "personas/default.persona.yaml": "49eecb534dcdd3b015561fa845d283f1b77eedf1",
    "personas/demerzel.persona.yaml": "34588423860befb59eea9be070c9f79540e402e9",
    "personas/guitar-coach.persona.yaml": "5e9714182c4961d04fc961149b1ba8cc385d002f",
    "personas/kaizen-optimizer.persona.yaml": "f2d9e1b60d622f132909c9d15634c71fa0c582d0",
    "personas/music-teacher.persona.yaml": "078f85f81fd5197a1bd50793a4dd9b4b4419cbac",
    "personas/rational-administrator.persona.yaml": "ec64ba7a63e28dd3eff441eb326da27ff362c547",
    "personas/recovery-agent.persona.yaml": "40a8c51d60badb4e5dc376fc65fd5a47bb99295c",
    "personas/reflective-architect.persona.yaml": "567dd9e5057b002a40541a571cc2d11864311f30",
    "personas/seldon.persona.yaml": "11d92ac84883e5378a709350bf6636f0e1d7a3d5",
    "personas/skeptical-auditor.persona.yaml": "b967591c40c9d15c234fc4d021e51fcca83ae6b7",
    "personas/system-integrator.persona.yaml": "8dafc7a50f17d74d820aaf2dca6b84dda770a96b",
    "personas/validator-reflector.persona.yaml": "29d8599eeaafcdbded8e4730de254fda6980ef06",
    "personas/virtuous-leader.persona.yaml": "1a5a1520e33d730aa5d155b247bd526292c7c067",
    "state/council/council-2026-06-24-001.json": "ae91b323f3a9fc3ce694d2f2810dfb1d7b4da236",
    "state/council/council-2026-06-24-002.json": "d0343151fcb968d6758b22caac3488e1c25b9f99",
    "state/council/council-2026-06-24-003.json": "cbf44c50a750f49b3b1bcf5f6d7e9c1f8c1d0426",
    "state/council/council-2026-06-24-004.json": "988bbf9e5b9533f6f0309dd412b0375734c1d76a",
    "state/council/council-2026-06-24-005.json": "11a0b34648dd5418bc53a00bb4fac0d492614afd",
    COUNCIL_SCHEMA: "4e5d19fadc068e9f3c097e951d4733aa9da2929f",
    PANEL_WORKFLOW: "028c00516d88a84978b2213a0b2755159b74812c",
    PANEL_SCRIPT: "1220c569a31660ccdece9aac6d6585b467ec6978",
}
STATED = re.compile(r"\b(\d+) personas across (\d+) repos\b")
TOP_LEVEL = {key: re.compile(rf'^{key}:[ \t]*"?([^"\s#]+)"?[ \t]*$', re.MULTILINE) for key in ("name", "version")}
TOP_LEVEL_KEY = re.compile(r"^([A-Za-z_][A-Za-z0-9_]*):", re.MULTILINE)
TIMESTAMP = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")
# The tribunal panel: a JavaScript workflow, read as text.
PANEL_LIST = re.compile(r"^const PANEL = \[\n(.*?)^\]$", re.MULTILINE | re.DOTALL)
PANEL_MEMBER = re.compile(r"^  \{ persona: '([a-z-]+)', role: '([a-z_]+)', concern: '[^']+' \},$")
PANEL_ANSWERS = re.compile(r"^const PERSONA_SCHEMA = \{\n.*?^    verdict: \{ type: 'string', enum: \[([^\]]+)\] \},$",
                           re.MULTILINE | re.DOTALL)
PANEL_PROMPTS = re.compile(r"^const reviews = await parallel\(\n(.*?)^const panel = ", re.MULTILINE | re.DOTALL)
PANEL_VERDICT_FOLDER = re.compile(r"^const VERDICT_ROOT = '([a-z/]+)'$", re.MULTILINE)
PANEL_MODEL = re.compile(r"^ +claude_args: '--model (\S+) ", re.MULTILINE)
# The comment in the workflow's permissions block that sits directly above the permission it explains.
PANEL_RUN_NOTE = re.compile(r"^permissions:\n(?:  [a-z-]+: [a-z]+\n)*((?:  # .*\n)+)  (id-token: write)$", re.MULTILINE)
PANEL_RUN_NOTE_SAYS = "this lane silently never produced a verdict"
PANEL_CONSENSUS = "strictest-wins"
# Lists of the verdict that the script builds with one entry per panel member, and how each is declared and stored.
PANEL_VERDICT_LISTS = {"evidence": ("const evidence = panel.map(", "\n  evidence,\n"),
                       "reviewer_chain": ("const reviewerChain = panel.map(", "\n  reviewer_chain: reviewerChain,\n")}


class ExtractError(Exception):
    """A source file is missing, malformed, or not the pinned one."""


def git_blob_id(data: bytes) -> str:
    """Blob id Git stores for this content once CRLF is normalised to LF."""
    data = data.replace(b"\r\n", b"\n")
    return hashlib.sha1(b"blob %d\x00" % len(data) + data).hexdigest()


def read_file(root: Path, rel: str) -> bytes:
    path = root / rel
    if not path.is_file():
        raise ExtractError(f"missing file: {rel}")
    return path.read_bytes()


def read_json(root: Path, rel: str) -> tuple[dict, str]:
    data = read_file(root, rel)
    try:
        record = json.loads(data.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ExtractError(f"{rel}: not UTF-8 JSON ({exc})") from exc
    if not isinstance(record, dict):
        raise ExtractError(f"{rel}: not a JSON object")
    return record, git_blob_id(data)


def department_record(root: Path) -> tuple[dict, dict]:
    record, blob = read_json(root, DEPARTMENT_RECORD)
    principle, repos = record.get("key_principle"), record.get("consumer_repos")
    if record.get("department") != "psychohistory":
        raise ExtractError(f"{DEPARTMENT_RECORD}: department is {record.get('department')!r}")
    if not isinstance(principle, str):
        raise ExtractError(f"{DEPARTMENT_RECORD}: key_principle is not a string")
    stated = STATED.findall(principle)
    if len(stated) != 1:
        raise ExtractError(f"{DEPARTMENT_RECORD}: key_principle states '<n> personas across <m> repos' "
                           f"{len(stated)} times, expected once")
    if (not isinstance(repos, list) or not repos or len(set(repos)) != len(repos)
            or not all(isinstance(repo, str) and repo for repo in repos)):
        raise ExtractError(f"{DEPARTMENT_RECORD}: consumer_repos is not a list of distinct names")
    for key in ("full_name", "head_persona", "established"):
        if not isinstance(record.get(key), str):
            raise ExtractError(f"{DEPARTMENT_RECORD}: {key} is not a string")
    extracted = {
        "path": DEPARTMENT_RECORD,
        "full_name": record["full_name"],
        "established": record["established"],
        "head_persona": record["head_persona"],
        "key_principle": principle,
        "stated_personas": int(stated[0][0]),
        "stated_repos": int(stated[0][1]),
        "consumer_repos": repos,
    }
    return extracted, {"path": DEPARTMENT_RECORD, "git_blob": blob}


def persona_files(root: Path) -> tuple[list[dict], dict, list[dict]]:
    folder = root / PERSONA_DIR
    if not folder.is_dir():
        raise ExtractError(f"missing directory: {PERSONA_DIR}")
    personas, keys, files = [], {}, []
    for path in sorted(folder.iterdir(), key=lambda entry: entry.name):
        rel = f"{PERSONA_DIR}/{path.name}"
        if not path.is_file() or not path.name.endswith(PERSONA_SUFFIX):
            raise ExtractError(f"{rel}: unexpected entry, {PERSONA_DIR}/ should hold *{PERSONA_SUFFIX} files only")
        data = path.read_bytes()
        try:
            text = data.decode("utf-8").replace("\r\n", "\n")
        except UnicodeDecodeError as exc:
            raise ExtractError(f"{rel}: not UTF-8 ({exc})") from exc
        fields = {}
        for key, pattern in TOP_LEVEL.items():
            found = pattern.findall(text)
            if len(found) != 1:
                raise ExtractError(f"{rel}: {len(found)} top-level '{key}:' lines, expected one")
            fields[key] = found[0]
        stem = path.name[:-len(PERSONA_SUFFIX)]
        if fields["name"] != stem:
            raise ExtractError(f"{rel}: name {fields['name']!r} differs from the file name")
        for key in sorted(set(TOP_LEVEL_KEY.findall(text))):
            keys[key] = keys.get(key, 0) + 1
        personas.append({"path": rel, "name": fields["name"], "version": fields["version"]})
        files.append({"path": rel, "git_blob": git_blob_id(data)})
    if not personas:
        raise ExtractError(f"no *{PERSONA_SUFFIX} file in {PERSONA_DIR}")
    return personas, dict(sorted(keys.items())), files


def council_schema(root: Path) -> tuple[dict, dict]:
    """What the schema allows a council verdict to hold: how many reviews, by which roles, with which answers."""
    schema, blob = read_json(root, COUNCIL_SCHEMA)
    try:
        reviews = schema["properties"]["reviews"]
        review = reviews["items"]["properties"]
        limits = {"min_reviews_per_verdict": reviews["minItems"], "max_reviews_per_verdict": reviews["maxItems"],
                  "reviewer_roles": review["reviewer"]["enum"],
                  "constitutional_alignment_values": review["constitutional_alignment"]["enum"]}
    except (KeyError, TypeError) as exc:
        raise ExtractError(f"{COUNCIL_SCHEMA}: no reviews limits or enums where expected ({exc!r})") from exc
    if (not all(isinstance(limits[key], int) for key in ("min_reviews_per_verdict", "max_reviews_per_verdict"))
            or not all(isinstance(limits[key], list) and limits[key] and all(isinstance(v, str) for v in limits[key])
                       for key in ("reviewer_roles", "constitutional_alignment_values"))):
        raise ExtractError(f"{COUNCIL_SCHEMA}: reviews limits are not integers or enums are not lists of strings")
    return {"path": COUNCIL_SCHEMA} | limits, {"path": COUNCIL_SCHEMA, "git_blob": blob}


def council_verdicts(root: Path, schema: dict) -> tuple[list[dict], list[dict]]:
    folder = root / COUNCIL_DIR
    if not folder.is_dir():
        raise ExtractError(f"missing directory: {COUNCIL_DIR}")
    verdicts, files = [], []
    for path in sorted(folder.iterdir(), key=lambda entry: entry.name):
        rel = f"{COUNCIL_DIR}/{path.name}"
        if path.name in COUNCIL_IGNORED:
            continue
        if not path.is_file() or not path.match(COUNCIL_PATTERN):
            raise ExtractError(f"{rel}: unexpected entry, {COUNCIL_DIR}/ should hold {COUNCIL_PATTERN} files only")
        record, blob = read_json(root, rel)
        reviews = record.get("reviews")
        for key in ("verdict_id", "task_id", "timestamp", "verdict"):
            if not isinstance(record.get(key), str) or not record[key]:
                raise ExtractError(f"{rel}: {key} is missing or not a string")
        if not TIMESTAMP.match(record["timestamp"]):
            raise ExtractError(f"{rel}: timestamp {record['timestamp']!r} is not YYYY-MM-DDTHH:MM:SSZ")
        if (not isinstance(reviews, list)
                or not schema["min_reviews_per_verdict"] <= len(reviews) <= schema["max_reviews_per_verdict"]):
            raise ExtractError(f"{rel}: reviews is not a list of the size the schema allows")
        rows = []
        for review in reviews:
            if (not isinstance(review, dict) or review.get("reviewer") not in schema["reviewer_roles"]
                    or review.get("constitutional_alignment") not in schema["constitutional_alignment_values"]):
                raise ExtractError(f"{rel}: a review lacks a reviewer role or a constitutional_alignment the schema allows")
            rows.append({"reviewer": review["reviewer"], "constitutional_alignment": review["constitutional_alignment"]})
        if len({row["reviewer"] for row in rows}) != len(rows):
            raise ExtractError(f"{rel}: the same reviewer appears twice")
        verdicts.append({"path": rel, "verdict_id": record["verdict_id"], "task_id": record["task_id"],
                         "timestamp": record["timestamp"], "verdict": record["verdict"], "reviews": rows})
        files.append({"path": rel, "git_blob": blob})
    if not verdicts:
        raise ExtractError(f"no {COUNCIL_PATTERN} file in {COUNCIL_DIR}")
    return verdicts, files


def read_text(root: Path, rel: str) -> tuple[str, str]:
    data = read_file(root, rel)
    try:
        return data.decode("utf-8").replace("\r\n", "\n"), git_blob_id(data)
    except UnicodeDecodeError as exc:
        raise ExtractError(f"{rel}: not UTF-8 ({exc})") from exc


def one_match(pattern: re.Pattern, text: str, rel: str, what: str) -> str:
    found = pattern.findall(text)
    if len(found) != 1:
        raise ExtractError(f"{rel}: {what} found {len(found)} times, expected once")
    return found[0]


def run_note(workflow: str) -> tuple[str, str]:
    """The workflow's own comment on how its runs failed, joined into one line, and the permission it explains."""
    found = PANEL_RUN_NOTE.findall(workflow)
    if len(found) != 1:
        raise ExtractError(f"{PANEL_WORKFLOW}: the comment above id-token: write found {len(found)} times, expected once")
    block, permission = found[0]
    note = " ".join(line[len("  # "):] for line in block.splitlines())
    if PANEL_RUN_NOTE_SAYS not in note:
        raise ExtractError(f"{PANEL_WORKFLOW}: the comment above {permission} no longer says {PANEL_RUN_NOTE_SAYS!r}")
    return note, permission


def tribunal_panel(root: Path, persona_names: list[str]) -> tuple[dict, list[dict]]:
    """The workflow that puts one question about a pull request to several personas, and the verdicts it has left."""
    script, script_blob = read_text(root, PANEL_SCRIPT)
    workflow, workflow_blob = read_text(root, PANEL_WORKFLOW)
    members = []
    for line in one_match(PANEL_LIST, script, PANEL_SCRIPT, "the PANEL list").splitlines():
        member = PANEL_MEMBER.match(line)
        if not member:
            raise ExtractError(f"{PANEL_SCRIPT}: a line of the PANEL list is not a persona entry: {line!r}")
        members.append({"persona": member.group(1), "role": member.group(2)})
    names = [member["persona"] for member in members]
    if not members or len(set(names)) != len(names):
        raise ExtractError(f"{PANEL_SCRIPT}: the PANEL list is empty or names a persona twice")
    without_file = sorted(set(names) - set(persona_names))
    if without_file:
        raise ExtractError(f"{PANEL_SCRIPT}: panel personas without a persona file: {without_file}")
    answers = re.findall(r"'([a-z_]+)'", one_match(PANEL_ANSWERS, script, PANEL_SCRIPT, "the persona verdict enum"))
    if len(answers) < 2 or len(set(answers)) != len(answers):
        raise ExtractError(f"{PANEL_SCRIPT}: the persona verdict enum is not a list of distinct answers")
    prompts = one_match(PANEL_PROMPTS, script, PANEL_SCRIPT, "the block that dispatches the personas")
    given = sorted(set(re.findall(r"\bctx\.([a-z_]+)", prompts)))
    differing = sorted(set(re.findall(r"\$\{member\.([a-z_]+)\}", prompts)))
    if not given or not differing:
        raise ExtractError(f"{PANEL_SCRIPT}: the persona prompt names no pull-request field or no member field")
    if PANEL_CONSENSUS not in script or PANEL_CONSENSUS not in workflow:
        raise ExtractError(f"{PANEL_SCRIPT}, {PANEL_WORKFLOW}: the consensus rule {PANEL_CONSENSUS!r} is not named")
    for name, fragments in PANEL_VERDICT_LISTS.items():
        if any(script.count(fragment) != 1 for fragment in fragments):
            raise ExtractError(f"{PANEL_SCRIPT}: the verdict's {name} list is not built once from the panel")
    folder = one_match(PANEL_VERDICT_FOLDER, script, PANEL_SCRIPT, "VERDICT_ROOT")
    if folder + "/" not in workflow:
        raise ExtractError(f"{PANEL_WORKFLOW}: does not name the verdict folder {folder}/")
    if not (root / folder).parent.is_dir():
        raise ExtractError(f"missing directory: {folder.rsplit('/', 1)[0]} (the parent of the verdict folder)")
    verdict_files = sorted(path.relative_to(root).as_posix() for path in (root / folder).rglob("*") if path.is_file())
    note, permission = run_note(workflow)
    panel = {
        "script": PANEL_SCRIPT,
        "workflow": PANEL_WORKFLOW,
        "what_is_read": "from the script: the PANEL list, the answers a persona may return, the names interpolated "
                        "into the prompt sent to each persona, the lists of the verdict built with one entry per "
                        "panel member, and the verdict folder; from the workflow: the --model argument of the run, "
                        "and the comment on failed runs above the permission it explains. This fixture executed "
                        "neither file.",
        "members": members,
        "answers_a_persona_may_return": answers,
        "consensus_rule_named_in_both_files": PANEL_CONSENSUS,
        "pull_request_fields_in_every_persona_prompt": given,
        "member_fields_in_the_persona_prompt": differing,
        "model_argument_of_the_run": one_match(PANEL_MODEL, workflow, PANEL_WORKFLOW, "claude_args with --model"),
        "note_on_failed_runs_in_the_workflow": note,
        "permission_the_note_explains_granted_below_it": permission,
        "verdict_lists_with_one_entry_per_panel_member": sorted(PANEL_VERDICT_LISTS),
        "verdict_folder": folder,
        "verdict_folder_parent_exists": True,
        "verdict_folder_exists": (root / folder).is_dir(),
        "verdict_files": verdict_files,
    }
    return panel, [{"path": PANEL_WORKFLOW, "git_blob": workflow_blob}, {"path": PANEL_SCRIPT, "git_blob": script_blob}]


def drift_from_the_pin(files: list[dict], panel: dict) -> list[str]:
    """Every way in which what was read differs from the pinned commit; empty when nothing does."""
    drift = [f"{entry['path']} is blob {entry['git_blob']}, pinned {PINNED_BLOBS.get(entry['path'])}"
             for entry in files if PINNED_BLOBS.get(entry["path"]) != entry["git_blob"]]
    drift += [f"{path} is pinned but was not read" for path in sorted(set(PINNED_BLOBS) - {e["path"] for e in files})]
    if panel["verdict_files"]:
        drift.append(f"{panel['verdict_folder']} holds {len(panel['verdict_files'])} file(s); the pinned commit has "
                     "no such folder")
    return drift


def count_rows(department: dict, personas: list[dict], schema: dict, verdicts: list[dict], panel: dict) -> dict:
    """The counts that the lesson quotes. analyze.py makes them again from the rows and compares."""
    names = [persona["name"] for persona in personas]
    reviews = [review for verdict in verdicts for review in verdict["reviews"]]
    paired = [verdict for verdict in verdicts if len(verdict["reviews"]) >= 2]
    sizes = sorted({len(verdict["reviews"]) for verdict in verdicts})
    return {
        "stated_personas": department["stated_personas"],
        "persona_files": len(personas),
        "persona_files_minus_stated_personas": len(personas) - department["stated_personas"],
        "head_persona_has_a_file": department["head_persona"] in names,
        "stated_repos": department["stated_repos"],
        "consumer_repos": len(department["consumer_repos"]),
        "consumer_repos_minus_stated_repos": len(department["consumer_repos"]) - department["stated_repos"],
        "council_verdicts": len(verdicts),
        "council_tasks": len({verdict["task_id"] for verdict in verdicts}),
        "council_utc_dates": len({verdict["timestamp"][:10] for verdict in verdicts}),
        "council_reviews": len(reviews),
        "council_reviewer_roles": sorted({review["reviewer"] for review in reviews}),
        "council_reviews_whose_reviewer_is_a_persona_name": sum(review["reviewer"] in names for review in reviews),
        "council_verdicts_by_number_of_reviews": {str(size): sum(len(v["reviews"]) == size for v in verdicts)
                                                  for size in sizes},
        "council_largest_number_of_reviews": sizes[-1],
        "council_schema_max_reviews": schema["max_reviews_per_verdict"],
        "council_verdicts_with_two_or_more_reviews": len(paired),
        "council_of_those_with_all_reviews_alike": sum(
            len({review["constitutional_alignment"] for review in verdict["reviews"]}) == 1 for verdict in paired),
        "tribunal_panel_personas": len(panel["members"]),
        "tribunal_panel_personas_with_a_persona_file": sum(m["persona"] in names for m in panel["members"]),
        "tribunal_panel_answers_a_persona_may_return": len(panel["answers_a_persona_may_return"]),
        "tribunal_panel_verdict_files": len(panel["verdict_files"]),
    }


def build(root: Path, allow_drift: bool) -> dict:
    """Read every source, refuse what is not the pinned commit, and assemble the snapshot."""
    department, department_file = department_record(root)
    personas, persona_keys, persona_blobs = persona_files(root)
    schema, schema_file = council_schema(root)
    verdicts, council_blobs = council_verdicts(root, schema)
    panel, panel_files = tribunal_panel(root, [persona["name"] for persona in personas])
    files = [department_file] + persona_blobs + council_blobs + [schema_file] + panel_files
    drift = drift_from_the_pin(files, panel)
    if drift and not allow_drift:
        raise ExtractError("source files are not those of commit " + PINNED_COMMIT + ":\n  " + "\n  ".join(drift)
                           + "\n(--allow-drift snapshots them anyway; the lesson's numbers then no longer apply)")
    return {
        "schema_version": "0.1.0",
        "module_id": "psy-004-how-large-is-large",
        "kind": "observed",
        "source": {
            "repository": "GuitarAlchemist/Demerzel",
            "commit": None if drift else PINNED_COMMIT,
            "commit_check": ("FAILED: " + "; ".join(drift)) if drift else
                            "every file below has the Git blob id recorded for this commit (CRLF normalised to LF)",
            "files": files,
        },
        "department_record": department,
        "persona_files": {
            "folder": PERSONA_DIR,
            "pattern": "*" + PERSONA_SUFFIX,
            "what_is_read": "the top-level name and version lines of each file, and the names of its top-level "
                            "keys; not the values of the other keys",
            "top_level_keys_and_the_number_of_files_that_have_them": persona_keys,
            "files": personas,
        },
        "council_schema": schema,
        "council_verdicts": {
            "folder": COUNCIL_DIR,
            "pattern": COUNCIL_PATTERN,
            "what_is_read": "per verdict: the task, the verdict, and each review's reviewer role and pass/fail "
                            "constitutional_alignment",
            "verdicts": verdicts,
        },
        "tribunal_panel": panel,
        "counts": count_rows(department, personas, schema, verdicts, panel),
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
    print(f"extract.py: record states {counts['stated_personas']} personas across {counts['stated_repos']} repos; "
          f"{counts['persona_files']} persona files, {counts['consumer_repos']} consumer repos, "
          f"{counts['council_verdicts']} council verdicts with at most {counts['council_largest_number_of_reviews']} "
          f"reviews, a tribunal panel of {counts['tribunal_panel_personas']} personas with "
          f"{counts['tribunal_panel_verdict_files']} verdict files -> {args.output.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
