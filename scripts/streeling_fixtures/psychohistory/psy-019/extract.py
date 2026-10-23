#!/usr/bin/env python3
"""PSY-019 extract: snapshot how the project gives several judges one question, and what it does with their answers.

Reads four files as text: the multi-model orchestration policy (its confidence
calibration block and its cross-validation rule), the tribunal-panel script
(who is asked, what every persona is sent, the score each may return and what
the script does with it), the workflow that runs the panel (its --model
argument) and the council script (the two reviewers it pairs, what its
docstring says about them, and the line that turns their scores into one
confidence); then the council's records in state/council (the scores it wrote).
Writes observed-input.json next to this script. The analysis script reads only
that snapshot, never the repository.

None of these files holds an answer of a persona or an outcome: this snapshot
describes a setup, plus a few council scores. It cannot give a correlation
between the judges' errors.

Fails with a non-zero exit and a message when a source file is missing, has an
unexpected shape, or is not the file of the pinned commit.

Run from the repository root:
    python -I -B scripts/streeling_fixtures/psychohistory/psy-019/extract.py
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
                / "state/streeling/fixtures/psychohistory/psy-019" / Path(__file__).name)

PINNED_COMMIT = "4b03838800dcd4894f1e026461979bff1d985ca8"
POLICY = "policies/multi-model-orchestration-policy.yaml"
PANEL_SCRIPT = ".claude/workflows/demerzel-tribunal-panel.js"
PANEL_WORKFLOW = ".github/workflows/tribunal-panel.yml"
COUNCIL_SCRIPT = "scripts/council_emit.py"
# Git blob ids at PINNED_COMMIT (git ls-tree -r <commit> -- <path>). A blob id
# is sha1(b"blob <size>\0" + content) over the LF-normalised bytes.
PINNED_BLOBS = {
    POLICY: "226185cf13f84ac0101449f7b2677e989d975d57",
    PANEL_SCRIPT: "1220c569a31660ccdece9aac6d6585b467ec6978",
    PANEL_WORKFLOW: "028c00516d88a84978b2213a0b2755159b74812c",
    COUNCIL_SCRIPT: "4db8e22fb3998735eb850cdd1578a88aa6ebba46",
    "state/council/council-2026-06-24-001.json": "ae91b323f3a9fc3ce694d2f2810dfb1d7b4da236",
    "state/council/council-2026-06-24-002.json": "d0343151fcb968d6758b22caac3488e1c25b9f99",
    "state/council/council-2026-06-24-003.json": "cbf44c50a750f49b3b1bcf5f6d7e9c1f8c1d0426",
    "state/council/council-2026-06-24-004.json": "988bbf9e5b9533f6f0309dd412b0375734c1d76a",
    "state/council/council-2026-06-24-005.json": "11a0b34648dd5418bc53a00bb4fac0d492614afd",
}
COUNCIL_RECORDS = "state/council"
# The policy: YAML read as text (the standard library has no YAML parser).
TOP_LEVEL = {key: re.compile(rf'^{key}:[ \t]*"?([^"\s#]+)"?[ \t]*$', re.MULTILINE) for key in ("name", "version")}
CALIBRATION_ENTRY = re.compile(r"^  ([a-z_]+): (.*?)(?:\s+# (.*))?$")
CALIBRATION_NUMBER = re.compile(r"^(?:(max) )?([+-]?\d+(?:\.\d+)?)$")
CALIBRATION_KEYS = ("single_model", "two_model_agreement", "two_model_disagreement")
RULE_NAME = "cross-validation"
RULE_HEADER = re.compile(r"^  - name: (\S+)$")
RULE_FIELD = re.compile(r"^    ([a-z_]+): (.+)$")
REGISTRY_MODEL = re.compile(r"^  ([a-z-]+):$")
REGISTRY_PROVIDER = re.compile(r"^    provider: (\S+)$")
# The tribunal panel: a JavaScript workflow, read as text.
PANEL_LIST = re.compile(r"^const PANEL = \[\n(.*?)^\]$", re.MULTILINE | re.DOTALL)
PANEL_MEMBER = re.compile(r"^  \{ persona: '([a-z-]+)', role: '([a-z_]+)', concern: '[^']+' \},$")
PANEL_PROMPTS = re.compile(r"^const reviews = await parallel\(\n(.*?)^const panel = ", re.MULTILINE | re.DOTALL)
PANEL_REQUIRED = re.compile(r"^const PERSONA_SCHEMA = \{\n  type: 'object',\n  required: \[([^\]]+)\],$", re.MULTILINE)
PANEL_SCORE = re.compile(r"^    score: \{ type: '([a-z]+)', description: '([^']+)' \},$")
PANEL_VERDICT = re.compile(r"^    verdict: \{ type: 'string', enum: \[([^\]]+)\] \},$")
PANEL_LIMITS = {
    "characters_of_the_body": re.compile(r"\(ctx\.body \|\| ''\)\.slice\(0, (\d+)\)"),
    "changed_files": re.compile(r"ctx\.files\.slice\(0, (\d+)\)"),
    "characters_of_the_diff": re.compile(r"\(ctx\.diff_excerpt \|\| ''\)\.slice\(0, (\d+)\)"),
}
PANEL_MODEL = re.compile(r"^ +claude_args: '--model (\S+) ", re.MULTILINE)
PANEL_CONSENSUS = "strictest-wins"
# The council: a Python script whose docstring describes its two reviewers, read as text.
COUNCIL_REVIEWER = re.compile(r"^  (reviewer_[a-z]) — ")
COUNCIL_PHRASES = (
    "deliberately heterogeneous",
    "A cross-model reviewer",
    "genuinely different model from reviewer_a's static analyzer",
    "lifts the single-model confidence cap honestly",
    "Chairman synthesis is strictest-wins",
    "is the MIN of the reviewers'",
)
COUNCIL_CONFIDENCE = re.compile(r"^    confidence = round\(min\(scores\), \d+\)$")


class ExtractError(Exception):
    """A source file is missing, malformed, or not the pinned one."""


def spaced(path: str) -> str:
    """A policy path as a data label: a space on each side of every slash (see the README)."""
    return " / ".join(path.split("/"))


def git_blob_id(data: bytes) -> str:
    """Blob id Git stores for this content once CRLF is normalised to LF."""
    data = data.replace(b"\r\n", b"\n")
    return hashlib.sha1(b"blob %d\x00" % len(data) + data).hexdigest()


def read_text(root: Path, rel: str) -> tuple[str, str]:
    path = root / rel
    if not path.is_file():
        raise ExtractError(f"missing file: {rel}")
    data = path.read_bytes()
    try:
        return data.decode("utf-8").replace("\r\n", "\n"), git_blob_id(data)
    except UnicodeDecodeError as exc:
        raise ExtractError(f"{rel}: not UTF-8 ({exc})") from exc


def one_match(pattern: re.Pattern, text: str, rel: str, what: str) -> str:
    found = pattern.findall(text)
    if len(found) != 1:
        raise ExtractError(f"{rel}: {what} found {len(found)} times, expected once")
    return found[0]


def top_level_block(lines: list[str], header: str, rel: str) -> list[tuple[int, str]]:
    """The numbered lines under a top-level 'header:' line, up to the next line that starts in column one."""
    starts = [index for index, line in enumerate(lines) if line == header + ":"]
    if len(starts) != 1:
        raise ExtractError(f"{rel}: top-level '{header}:' found {len(starts)} times, expected once")
    block = []
    for index in range(starts[0] + 1, len(lines)):
        if lines[index] and not lines[index].startswith(" "):
            break
        if lines[index]:
            block.append((index + 1, lines[index]))
    if not block:
        raise ExtractError(f"{rel}: the '{header}:' block is empty")
    return block


def calibration_entries(lines: list[str]) -> list[dict]:
    entries = []
    for number, line in top_level_block(lines, "confidence_calibration", POLICY):
        entry = CALIBRATION_ENTRY.match(line)
        value = CALIBRATION_NUMBER.match(entry.group(2)) if entry else None
        if not value:
            raise ExtractError(f"{POLICY}: line {number} is not 'key: [max ]number  # comment': {line!r}")
        entries.append({"line": number, "key": entry.group(1), "value": entry.group(2),
                        "qualifier": value.group(1), "number": value.group(2), "comment": entry.group(3)})
    keys = [entry["key"] for entry in entries]
    if len(set(keys)) != len(keys) or any(key not in keys for key in CALIBRATION_KEYS):
        raise ExtractError(f"{POLICY}: confidence_calibration repeats a key or lacks one of {CALIBRATION_KEYS}")
    return entries


def cross_validation_rule(lines: list[str]) -> dict:
    """The orchestration rule named 'cross-validation' and the provider of each model it names."""
    rule, inside = {}, False
    for number, line in top_level_block(lines, "orchestration_rules", POLICY):
        header = RULE_HEADER.match(line)
        if header:
            inside = header.group(1) == RULE_NAME
            if inside and rule:
                raise ExtractError(f"{POLICY}: two orchestration rules are named {RULE_NAME!r}")
            if inside:
                rule["line"] = number
        elif inside and RULE_FIELD.match(line):
            key, value = RULE_FIELD.match(line).groups()
            rule[key] = value
    if sorted(rule) != ["description", "line", "models", "threshold"]:
        raise ExtractError(f"{POLICY}: rule {RULE_NAME!r} has the fields {sorted(rule)}, expected description, "
                           "models and threshold")
    models = re.fullmatch(r"\[([a-z-]+(?:, [a-z-]+)+)\]", rule["models"])
    if not models:
        raise ExtractError(f"{POLICY}: rule {RULE_NAME!r} does not list two or more models: {rule['models']!r}")
    providers, current = {}, None
    for _, line in top_level_block(lines, "model_registry", POLICY):
        if REGISTRY_MODEL.match(line):
            current = REGISTRY_MODEL.match(line).group(1)
        elif REGISTRY_PROVIDER.match(line) and current:
            providers[current] = REGISTRY_PROVIDER.match(line).group(1)
    names = models.group(1).split(", ")
    if len(set(names)) != len(names) or any(name not in providers for name in names):
        raise ExtractError(f"{POLICY}: rule {RULE_NAME!r} repeats a model or names one without a provider: {names}")
    return {"line": rule["line"], "name": RULE_NAME, "description": rule["description"], "models": names,
            "threshold": rule["threshold"], "provider_of_each_model": {name: providers[name] for name in names}}


def orchestration_policy(root: Path) -> tuple[dict, dict]:
    text, blob = read_text(root, POLICY)
    lines = text.split("\n")
    policy = {
        "path": spaced(POLICY),
        "name": one_match(TOP_LEVEL["name"], text, POLICY, "a top-level 'name:' line"),
        "version": one_match(TOP_LEVEL["version"], text, POLICY, "a top-level 'version:' line"),
        "what_is_read": "the name and version lines, every line of the confidence_calibration block, and the "
                        "orchestration rule named cross-validation with the provider that the model registry gives "
                        "for each model it names; nothing else",
        "confidence_calibration": calibration_entries(lines),
        "cross_validation_rule": cross_validation_rule(lines),
    }
    return policy, {"path": spaced(POLICY), "git_blob": blob}


def panel_score(script: str) -> tuple[dict, list[dict]]:
    """The score a persona may return, and every line of the script that reads one."""
    lines = script.split("\n")
    declared = [(index + 1, PANEL_SCORE.match(line)) for index, line in enumerate(lines) if PANEL_SCORE.match(line)]
    if len(declared) != 1:
        raise ExtractError(f"{PANEL_SCRIPT}: the persona schema declares a score {len(declared)} times, expected once")
    required = re.findall(r"'([a-z_]+)'", one_match(PANEL_REQUIRED, script, PANEL_SCRIPT, "the persona schema's "
                                                                                          "required list"))
    number, match = declared[0]
    field = {"line": number, "type": match.group(1), "description": match.group(2), "required": "score" in required}
    readers = [{"line": index + 1, "text": line.strip()} for index, line in enumerate(lines) if ".score" in line]
    if not readers:
        raise ExtractError(f"{PANEL_SCRIPT}: no line reads a persona's score")
    return field, readers


def panel_verdicts(script: str) -> dict:
    """The values a persona's verdict may take, from the persona schema."""
    found = [(index + 1, PANEL_VERDICT.match(line)) for index, line in enumerate(script.split("\n"))
             if PANEL_VERDICT.match(line)]
    if len(found) != 1:
        raise ExtractError(f"{PANEL_SCRIPT}: the persona schema declares a verdict {len(found)} times, expected once")
    values = re.findall(r"'([a-z_]+)'", found[0][1].group(1))
    if len(values) < 2 or len(set(values)) != len(values):
        raise ExtractError(f"{PANEL_SCRIPT}: the verdict enum is not a list of distinct values: {values}")
    return {"line": found[0][0], "values": values}


def tribunal_panel(root: Path) -> tuple[dict, list[dict]]:
    """The workflow that puts one pull request to several personas: who, with what, and what becomes of the scores."""
    script, script_blob = read_text(root, PANEL_SCRIPT)
    workflow, workflow_blob = read_text(root, PANEL_WORKFLOW)
    members = []
    for line in one_match(PANEL_LIST, script, PANEL_SCRIPT, "the PANEL list").splitlines():
        member = PANEL_MEMBER.match(line)
        if not member:
            raise ExtractError(f"{PANEL_SCRIPT}: a line of the PANEL list is not a persona entry: {line!r}")
        members.append({"persona": member.group(1), "role": member.group(2)})
    if not members or len({member["persona"] for member in members}) != len(members):
        raise ExtractError(f"{PANEL_SCRIPT}: the PANEL list is empty or names a persona twice")
    prompts = one_match(PANEL_PROMPTS, script, PANEL_SCRIPT, "the block that dispatches the personas")
    given = sorted(set(re.findall(r"\bctx\.([a-z_]+)", prompts)))
    differing = sorted(set(re.findall(r"\$\{member\.([a-z_]+)\}", prompts)))
    if not given or not differing:
        raise ExtractError(f"{PANEL_SCRIPT}: the persona prompt names no pull-request field or no member field")
    limits = {name: int(one_match(pattern, prompts, PANEL_SCRIPT, f"the limit on the {name.replace('_', ' ')}"))
              for name, pattern in PANEL_LIMITS.items()}
    if PANEL_CONSENSUS not in script or PANEL_CONSENSUS not in workflow:
        raise ExtractError(f"{PANEL_SCRIPT}, {PANEL_WORKFLOW}: the consensus rule {PANEL_CONSENSUS!r} is not named")
    score, readers = panel_score(script)
    panel = {
        "script": PANEL_SCRIPT,
        "workflow": PANEL_WORKFLOW,
        "what_is_read": "from the script: the PANEL list, the names interpolated into the prompt sent to each persona "
                        "with the three limits on their length, the verdict and score fields of the persona schema and every line "
                        "that contains '.score'; from the workflow: the --model argument of the run. Neither file "
                        "was executed, and neither holds an answer of a persona.",
        "members": members,
        "pull_request_fields_in_every_persona_prompt": given,
        "member_fields_in_the_persona_prompt": differing,
        "limits_on_what_every_persona_is_sent": limits,
        "verdicts_a_persona_may_return": panel_verdicts(script),
        "score_a_persona_may_return": score,
        "lines_that_read_a_persona_score": readers,
        "consensus_rule_named_in_both_files": PANEL_CONSENSUS,
        "model_argument_of_the_run": one_match(PANEL_MODEL, workflow, PANEL_WORKFLOW, "claude_args with --model"),
    }
    return panel, [{"path": PANEL_SCRIPT, "git_blob": script_blob}, {"path": PANEL_WORKFLOW, "git_blob": workflow_blob}]


def council(root: Path) -> tuple[dict, dict]:
    """The council of two reviewers: who they are, what the docstring says of them, and how one confidence is made."""
    text, blob = read_text(root, COUNCIL_SCRIPT)
    lines = text.split("\n")
    reviewers = [{"line": index + 1, "name": COUNCIL_REVIEWER.match(line).group(1)}
                 for index, line in enumerate(lines) if COUNCIL_REVIEWER.match(line)]
    if len(reviewers) < 2 or len({reviewer["name"] for reviewer in reviewers}) != len(reviewers):
        raise ExtractError(f"{COUNCIL_SCRIPT}: the docstring does not describe two or more distinct reviewers")
    statements = []
    for phrase in COUNCIL_PHRASES:
        found = [index for index, line in enumerate(lines) if phrase in line]
        if len(found) != 1:
            raise ExtractError(f"{COUNCIL_SCRIPT}: {phrase!r} found on {len(found)} lines, expected one")
        statements.append({"line": found[0] + 1, "phrase": phrase, "text": lines[found[0]].strip()})
    confidence = [index for index, line in enumerate(lines) if COUNCIL_CONFIDENCE.match(line)]
    if len(confidence) != 1:
        raise ExtractError(f"{COUNCIL_SCRIPT}: the line that computes the council's confidence was found "
                           f"{len(confidence)} times, expected once")
    return {
        "script": COUNCIL_SCRIPT,
        "what_is_read": "the docstring lines that introduce the reviewers, six phrases of the docstring (each must be "
                        "on exactly one line, which is kept whole), and the line that computes the council's "
                        "confidence. The script was not executed and holds no review.",
        "reviewers": reviewers,
        "statements": statements,
        "confidence_line": {"line": confidence[0] + 1, "text": lines[confidence[0]].strip()},
    }, {"path": COUNCIL_SCRIPT, "git_blob": blob}


def council_records(root: Path) -> tuple[dict, list[dict]]:
    """The verdicts the council has written: who scored what, and whether any record names an outcome."""
    folder = root / COUNCIL_RECORDS
    paths = sorted(folder.glob("council-*.json")) if folder.is_dir() else []
    if not paths:
        raise ExtractError(f"{COUNCIL_RECORDS}: no council-*.json record")
    records, files, keys, review_keys = [], [], set(), set()
    for path in paths:
        rel = f"{COUNCIL_RECORDS}/{path.name}"
        text, blob = read_text(root, rel)
        try:
            data = json.loads(text)
            scores = [{"reviewer": review["reviewer"], "correctness_score": review["correctness_score"]}
                      for review in data["reviews"]]
            records.append({"id": data["verdict_id"], "scores": scores, "verdict": data["verdict"],
                            "post_council_confidence": data["post_council_confidence"]})
            review_keys |= {key for review in data["reviews"] for key in review}
        except (ValueError, KeyError, TypeError) as exc:
            raise ExtractError(f"{rel}: not a council verdict ({exc})") from exc
        keys |= set(data)
        files.append({"path": rel, "git_blob": blob})
    return {
        "folder": COUNCIL_RECORDS,
        "what_is_read": "every council-*.json record: its id, each reviewer's correctness_score, the verdict and the "
                        "council's confidence, and the names of all keys, top level and per review",
        "records": records,
        "top_level_keys": sorted(keys),
        "review_keys": sorted(review_keys),
        "keys_naming_an_outcome": sorted(key for key in keys | review_keys if "outcome" in key.lower()),
    }, files


def drift_from_the_pin(files: list[dict]) -> list[str]:
    """Every file whose content is not the blob of the pinned commit; empty when all are."""
    pinned = {(spaced(path) if path == POLICY else path): blob for path, blob in PINNED_BLOBS.items()}
    drift = [f"{entry['path']} is blob {entry['git_blob']}, pinned {pinned.get(entry['path'])}"
             for entry in files if pinned.get(entry["path"]) != entry["git_blob"]]
    return drift + [f"{path} is pinned but was not read" for path in sorted(set(pinned) - {e["path"] for e in files})]


def count_rows(policy: dict, panel: dict, pair: dict, verdicts: dict) -> dict:
    """The counts that the lesson quotes. analyze.py makes them again from the rows and compares."""
    rule = policy["cross_validation_rule"]
    return {
        "confidence_calibration_entries": len(policy["confidence_calibration"]),
        "cross_validation_models": len(rule["models"]),
        "cross_validation_providers": len(set(rule["provider_of_each_model"].values())),
        "tribunal_panel_personas": len(panel["members"]),
        "pull_request_fields_in_every_persona_prompt": len(panel["pull_request_fields_in_every_persona_prompt"]),
        "member_fields_in_the_persona_prompt": len(panel["member_fields_in_the_persona_prompt"]),
        "lines_that_read_a_persona_score": len(panel["lines_that_read_a_persona_score"]),
        "council_reviewers": len(pair["reviewers"]),
        "verdicts_a_persona_may_return": len(panel["verdicts_a_persona_may_return"]["values"]),
        "council_records": len(verdicts["records"]),
        "council_scores": sum(len(record["scores"]) for record in verdicts["records"]),
    }


def build(root: Path, allow_drift: bool) -> dict:
    """Read every source, refuse what is not the pinned commit, and assemble the snapshot."""
    policy, policy_file = orchestration_policy(root)
    panel, panel_files = tribunal_panel(root)
    pair, pair_file = council(root)
    verdicts, verdict_files = council_records(root)
    files = [policy_file] + panel_files + [pair_file] + verdict_files
    drift = drift_from_the_pin(files)
    if drift and not allow_drift:
        raise ExtractError("source files are not those of commit " + PINNED_COMMIT + ":\n  " + "\n  ".join(drift)
                           + "\n(--allow-drift snapshots them anyway; the lesson's numbers then no longer apply)")
    return {
        "schema_version": "0.1.0",
        "module_id": "psy-019-combining-correlated-forecasters",
        "kind": "observed: a description of a setup. No persona's answer and no outcome is in the files read, and the "
                "council's records hold a few reviewer scores without outcomes, so nothing here measures a "
                "correlation between agents.",
        "source": {
            "repository": "GuitarAlchemist/Demerzel",
            "commit": None if drift else PINNED_COMMIT,
            "commit_check": ("FAILED: " + "; ".join(drift)) if drift else
                            "every file below has the Git blob id recorded for this commit (CRLF normalised to LF)",
            "path_note": "The policy's path is a data label here: it is written with a space on each side of the "
                         "slash, so that this file is not counted as a citation of a governance artifact.",
            "files": files,
        },
        "orchestration_policy": policy,
        "tribunal_panel": panel,
        "council": pair,
        "council_records": verdicts,
        "counts": count_rows(policy, panel, pair, verdicts),
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
    print(f"extract.py: {counts['confidence_calibration_entries']} confidence settings, a cross-validation rule over "
          f"{counts['cross_validation_models']} models, a panel of {counts['tribunal_panel_personas']} personas whose "
          f"score is read on {counts['lines_that_read_a_persona_score']} line(s), a council of "
          f"{counts['council_reviewers']} reviewers with {counts['council_records']} verdicts and "
          f"{counts['council_scores']} scores -> {args.output.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
