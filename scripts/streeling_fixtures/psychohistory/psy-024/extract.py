#!/usr/bin/env python3
"""PSY-024 extract: who the recorded activity is attributed to, with every identity replaced by a label.

Reads, at the pinned commit of the Demerzel repository:
  - every file of state/triggers/archived/ and the files left in state/triggers/ (sender and repo of each event);
  - the trigger workflow as it stands at the pin (a later version than the ones that wrote the trigger files),
    three other workflows that commit under the same identity, .github/CODEOWNERS, .mailmap and AGENTS.md (what
    the pinned files say about the identities);
  - the commit history reachable from the pin, with git commands that read commits and trees only, including the
    commits that changed the trigger workflow after the last commit with the trigger subject.
Writes observed-input.json next to this script. The analysis script reads only that snapshot.

No sender, author name, committer name, co-author name, handle or e-mail address is written. Each distinct value
becomes a label ("account A", "author B", "co-author 03"), assigned by descending count, ties broken by the SHA-256
of the value, which is not stored; a co-author name identical to a sender takes that account's label. The script
stops if one of the raw strings, the names of the mailmap included, appears in its own output.

Fails with a non-zero exit and a message when a file is missing or malformed, when the trigger archive is not the
folder of the pinned commit (file count, Git tree id, manifest digest), when another file is not its pinned Git
blob, when git or the pinned commit is missing, when the clone is shallow, or when the commit count differs.

Run from the repository root:
    python -I -B scripts/streeling_fixtures/psychohistory/psy-024/extract.py
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

# This program lives under scripts/ (CONTRIBUTING.md: no executable code outside scripts/); its data stays
# under state/streeling/fixtures/. FIXTURE_FILE is the path the program would have next to that data.
FIXTURE_FILE = (Path(__file__).resolve().parents[4]
                / "state/streeling/fixtures/psychohistory/psy-024" / Path(__file__).name)

PINNED_COMMIT = "4b03838800dcd4894f1e026461979bff1d985ca8"
PINNED_COMMITS = 1599  # git rev-list --count <pin>
REPOSITORY = "GuitarAlchemist/Demerzel"
HOSTING_DOMAIN = "github.com"

ARCHIVE = "state/triggers/archived"
TOP = "state/triggers"
# The archive holds too many files to pin one blob id each, so three values pin it as a whole:
#   the file count; the Git tree id of the folder (git ls-tree <pin> state/triggers/);
#   the SHA-256 of the lines "<blob id> <path>\n" sorted by path
#   (git ls-tree -r <pin> -- state/triggers/archived | awk '{print $3" "$4}' | sha256sum).
PINNED_FILE_COUNT = 594
PINNED_TREE_ID = "2da37c16496d39c0c9137897c8be2b0c6d6b7978"
PINNED_MANIFEST_SHA256 = "3e33b3e795b977277c52c99d59c48f15ae60f95d28f5524c641d3ec066f10393"

# Every other file of state/triggers/ at the pin, with its Git blob id (git ls-tree -r <pin> -- state/triggers/).
TOP_FILES = {
    ".gitkeep": "e69de29bb2d1d6434b8b29ae775ad8c2e48c5391",
    "2026-05-01T05-00-00Z-research-followup.trigger.json": "b6206807df8b895723e2914f0528003ce7551426",
    "2026-07-17T14-54-08Z-discussion_created.trigger.json": "9d1fc781548ec959961643332e861b86963187bf",
    "2026-07-17T15-21-56Z-discussion_created.trigger.json": "84e06bf723e7da0c0cc7dbdb454bf9140c429756",
    "2026-07-18T15-05-00Z-discussion_created.trigger.json": "db453ffa6e00541b98f6b692710ca5032edd4d5f",
    "2026-07-18T17-31-32Z-issue_opened.trigger.json": "c3e96d6391410bcee407d0b487fb44efa2e4f062",
    "2026-07-18T17-31-38Z-issue_opened.trigger.json": "ea9f99ca3fd8118ce276daf79cc97c5e0a8f957e",
    "2026-07-18T17-31-42Z-issue_opened.trigger.json": "49aad8bc89f56e0f75a8b028b501c90cb8376cdc",
    "2026-07-18T17-31-50Z-discussion_created.trigger.json": "4ee30bb676b452db9948cdd1b79c8ea9b0f7af66",
    "2026-07-18T17-31-57Z-discussion_created.trigger.json": "7ab7e26e08e9360e38f2702c3ceba9868a7beeb0",
    "processing/.gitkeep": "e69de29bb2d1d6434b8b29ae775ad8c2e48c5391",
    "scheduled-research-team.trigger.json": "9d2288fc7d331bb53ab6436c0bed37a7054d1130",
}
# Files that say what the identities are, with their Git blob ids at the pin (git ls-tree <pin> <path>).
TRIGGER_WORKFLOW = ".github/workflows/demerzel-driver-triggers.yml"
OTHER_WORKFLOWS = [
    ".github/workflows/demerzel-quality-trend-freshness.yml",
    ".github/workflows/demerzel-quality-trend.yml",
    ".github/workflows/ecosystem-freshness.yml",
]
CODEOWNERS = ".github/CODEOWNERS"
MAILMAP = ".mailmap"
AGENT_TEAM = "AGENTS.md"
PINNED_BLOBS = {
    TRIGGER_WORKFLOW: "e8406b8fd106cf69f64061e25d51c7c5f57d9581",
    OTHER_WORKFLOWS[0]: "f7f1247606358ab29b5b85dc91df44036579b2c8",
    OTHER_WORKFLOWS[1]: "6bc80481e68522f0e8f201c6f2404c211f23fc20",
    OTHER_WORKFLOWS[2]: "5ab0362ea5fdad0bf481aebdcda652fc93f2904f",
    CODEOWNERS: "9a1fd4ec46fb7f12871001dbd0cc9e7cbb1b34c2",
    MAILMAP: "e78f70e161f121cd90bf1b6b05ff5115a7cf57a6",
    AGENT_TEAM: "6a0dfd5fb2cfa983a6640eb2a7097e71e4e51cd9",
}
# What is read from the trigger workflow: (key, pattern with one group). Each must match exactly once.
WORKFLOW_PATTERNS = [
    ("sender_expression", r'^\s*"sender": "\$\{\{ (github\.actor) \}\}",?$'),
    ("repo_expression", r'^\s*"repo": "\$\{\{ (github\.event\.repository\.name) \}\}",?$'),
    ("commit_message", r'git commit -m "(trigger: \$\{\{ steps\.trigger\.outputs\.type \}\} from '
                       r'\$\{\{ github\.event\.repository\.name \}\} \[skip ci\])"$'),
    ("retired_on", r"^# RETIRED (\d{4}-\d{2}-\d{2}) "),
]
IDENTITY_LINE = re.compile(r'^\s*git config user\.name "([^"]+)"$', re.MULTILINE)
EVENT_NAME = re.compile(r'"\$\{\{ github\.event_name \}\}" = "([a-z_]+)"')
ROLE_ROW = re.compile(r"^\| \*\*[A-Za-z]+\*\*(?: \(lead\))? \| `personas/[a-z-]+\.persona\.yaml` \|", re.MULTILINE)
MAILMAP_LINE = re.compile(r"^(?P<n1>[^<]*)<(?P<e1>[^<>]+)>(?:\s*(?P<n2>[^<]*)<(?P<e2>[^<>]+)>)?$")

FILE_NAME = re.compile(r"^(\d{4}-\d{2}-\d{2}T\d{2}-\d{2}-\d{2}Z)-([a-z_]+)\.trigger\.json$")
ANY_TRIGGER_NAME = re.compile(r"^(.+?)-([a-z_-]+)\.trigger\.json$")
TIMESTAMP = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")
TOP_KEYS = {"type", "repo", "ref", "priority", "details", "timestamp"}
DETAIL_KEYS = {"event", "sender", "run_id"}
TRIGGER_SUBJECT = re.compile(r"^trigger: ([a-z_]+) from (\S+)(?: \[skip ci\])?$")
PULL_REQUEST_SUBJECT = re.compile(r"\(#\d+\)$")
TRAILER = re.compile(r"^(.*?)\s*<([^<>@\s]+)@([^<>@\s]+)>$")
LOG_FORMAT = ("%x1e%H%x1f%P%x1f%an%x1f%ae%x1f%cn%x1f%ce%x1f%cI%x1f%s%x1f"
              "%(trailers:key=Co-authored-by,valueonly,separator=%x1d)")
NAME_STATUS_FORMAT = "%x1e%H%x1f"
VERSION_FORMAT = "%x1e%H%x1f%cI%x1f%s"


class ExtractError(Exception):
    """A source is missing or malformed, or it is not the one of the pinned commit."""


def git_blob_id(data: bytes) -> str:
    """Blob id Git stores for this content once CRLF is normalised to LF."""
    data = data.replace(b"\r\n", b"\n")
    return hashlib.sha1(b"blob %d\x00" % len(data) + data).hexdigest()


def git_tree_id(entries: list[tuple[str, str]]) -> str:
    """Tree id of a flat folder of regular, non-executable files (mode 100644)."""
    body = b"".join(b"100644 " + name.encode("utf-8") + b"\x00" + bytes.fromhex(blob)
                    for name, blob in sorted(entries, key=lambda entry: entry[0].encode("utf-8")))
    return hashlib.sha1(b"tree %d\x00" % len(body) + body).hexdigest()


def manifest_sha256(entries: list[tuple[str, str]]) -> str:
    """SHA-256 of the lines '<blob id> <repository path>' sorted by path bytes."""
    lines = sorted((f"{ARCHIVE}/{name}".encode("utf-8"), blob.encode("ascii")) for name, blob in entries)
    return hashlib.sha256(b"".join(blob + b" " + path + b"\n" for path, blob in lines)).hexdigest()


def tally(values: list) -> dict:
    return {value: values.count(value) for value in sorted(set(values))}


def letters(index: int) -> str:
    """0 -> A, 25 -> Z, 26 -> AA."""
    text = ""
    index += 1
    while index:
        index, rest = divmod(index - 1, 26)
        text = chr(65 + rest) + text
    return text


def label_values(counts: dict[str, int], template: str, numbered: bool = False) -> dict[str, str]:
    """Raw value -> label, by descending count; ties by the SHA-256 of the value, which is never stored."""
    ordered = sorted(counts, key=lambda value: (-counts[value], hashlib.sha256(value.encode("utf-8")).hexdigest()))
    labels = {}
    for index, value in enumerate(ordered):
        mark = f"{index + 1:02d}" if numbered else letters(index)
        suffix = " (automation: the name ends in [bot])" if value.endswith("[bot]") else ""
        labels[value] = template.format(mark) + suffix
    return labels


def read_pinned(root: Path, rel: str, pinned: str, drift: list[str]) -> bytes:
    path = root / rel
    if not path.is_file():
        raise ExtractError(f"missing file: {rel}")
    data = path.read_bytes()
    if git_blob_id(data) != pinned:
        drift.append(f"{rel} is blob {git_blob_id(data)}, pinned {pinned}")
    return data


def as_text(rel: str, data: bytes) -> str:
    try:
        return data.decode("utf-8").replace("\r\n", "\n")
    except UnicodeDecodeError as exc:
        raise ExtractError(f"{rel}: not UTF-8 ({exc})") from exc


def as_json(rel: str, data: bytes) -> dict:
    try:
        record = json.loads(data.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ExtractError(f"{rel}: not UTF-8 JSON ({exc})") from exc
    if not isinstance(record, dict):
        raise ExtractError(f"{rel}: not a JSON object")
    return record


def workflow_event(where: str, record: dict) -> dict:
    """The fields of one event written by the trigger workflow, after checking its shape."""
    if set(record) != TOP_KEYS:
        raise ExtractError(f"{where}: keys are not {sorted(TOP_KEYS)}")
    details = record["details"]
    if not isinstance(details, dict) or set(details) != DETAIL_KEYS:
        raise ExtractError(f"{where}: details keys are not {sorted(DETAIL_KEYS)}")
    for key in ("type", "repo", "ref", "priority", "timestamp"):
        if not isinstance(record[key], str) or not record[key]:
            raise ExtractError(f"{where}: {key} is not a non-empty string")
    for key in DETAIL_KEYS:
        if not isinstance(details[key], str) or not details[key]:
            raise ExtractError(f"{where}: details.{key} is not a non-empty string")
    if not TIMESTAMP.match(record["timestamp"]):
        raise ExtractError(f"{where}: unexpected timestamp {record['timestamp']!r}")
    datetime.strptime(record["timestamp"], "%Y-%m-%dT%H:%M:%SZ")
    name = FILE_NAME.match(where.rsplit("/", 1)[1])
    if not name or name.group(1) != record["timestamp"].replace(":", "-") or name.group(2) != record["type"]:
        raise ExtractError(f"{where}: the file name does not match the JSON timestamp and type")
    return {"file": name.group(0), "timestamp": record["timestamp"], "type": record["type"], "repo": record["repo"],
            "event": details["event"], "sender": details["sender"]}


def read_archive(root: Path, drift: list[str]) -> tuple[list[dict], dict]:
    """Every archived event (raw sender included) and the three values that pin the folder."""
    folder = root / ARCHIVE
    if not folder.is_dir():
        raise ExtractError(f"missing directory: {ARCHIVE}")
    events, entries = [], []
    for path in sorted(folder.iterdir(), key=lambda p: p.name.encode("utf-8")):
        where = f"{ARCHIVE}/{path.name}"
        if not path.is_file():
            raise ExtractError(f"{where}: not a regular file")
        data = path.read_bytes()
        events.append(workflow_event(where, as_json(where, data)))
        entries.append((path.name, git_blob_id(data)))
    if not events:
        raise ExtractError(f"no trigger file in {ARCHIVE}")
    tree_id, manifest = git_tree_id(entries), manifest_sha256(entries)
    if len(entries) != PINNED_FILE_COUNT:
        drift.append(f"{ARCHIVE}: {len(entries)} files, pinned {PINNED_FILE_COUNT}")
    if tree_id != PINNED_TREE_ID:
        drift.append(f"{ARCHIVE}: Git tree id {tree_id}, pinned {PINNED_TREE_ID}")
    if manifest != PINNED_MANIFEST_SHA256:
        drift.append(f"{ARCHIVE}: manifest SHA-256 {manifest}, pinned {PINNED_MANIFEST_SHA256}")
    return events, {"files": len(entries), "git_tree_id": tree_id, "manifest_sha256": manifest}


def read_top_folder(root: Path, drift: list[str]) -> list[dict]:
    """The files of state/triggers/ outside the archive: what each is and, when it has one, its raw sender."""
    top = root / TOP
    found = sorted(p.name for p in top.iterdir() if p.is_file())
    if (top / "processing").is_dir():
        found += sorted(f"processing/{p.name}" for p in (top / "processing").iterdir())
    if set(found) != set(TOP_FILES):
        drift.append(f"{TOP}: files outside the archive are {sorted(found)}, pinned {sorted(TOP_FILES)}")
    rows = []
    for name in sorted(TOP_FILES):
        where = f"{TOP}/{name}"
        data = read_pinned(root, where, TOP_FILES[name], drift)
        if name.endswith(".gitkeep"):
            rows.append({"file": name, "kind": "empty placeholder"})
            continue
        record = as_json(where, data)
        details = record.get("details")
        if set(record) == TOP_KEYS:
            rows.append(workflow_event(where, record) | {"file": name, "kind": "event written by the trigger workflow"})
        elif "type" in record and isinstance(details, dict) and "sender" not in details:
            rows.append({"file": name, "kind": "trigger of another shape, without a sender field",
                         "type": record["type"], "repo": record.get("repo")})
        elif "type" not in record and "sender" not in json.dumps(record):
            rows.append({"file": name, "kind": "a schedule definition: no event type, no sender, no repo"})
        else:
            raise ExtractError(f"{where}: unexpected shape")
    return rows


def read_workflows(root: Path, drift: list[str]) -> tuple[dict, str]:
    """What the trigger workflow writes into an event, and the commit identity it configures (returned apart)."""
    text = as_text(TRIGGER_WORKFLOW, read_pinned(root, TRIGGER_WORKFLOW, PINNED_BLOBS[TRIGGER_WORKFLOW], drift))
    facts: dict = {"file": TRIGGER_WORKFLOW}
    for key, pattern in WORKFLOW_PATTERNS:
        found = list(re.finditer(pattern, text, flags=re.MULTILINE))
        if len(found) != 1:
            raise ExtractError(f"{TRIGGER_WORKFLOW}: expected one match for {key}, found {len(found)}")
        facts[key] = found[0].group(1)
        facts[f"{key}_line"] = text.count("\n", 0, found[0].start(1)) + 1
    facts["event_names_handled"] = EVENT_NAME.findall(text)
    if facts["event_names_handled"] != ["push", "issues", "workflow_run", "discussion"]:
        raise ExtractError(f"{TRIGGER_WORKFLOW}: unexpected event names {facts['event_names_handled']}")
    identities, lines = [], []
    for rel in [TRIGGER_WORKFLOW, *OTHER_WORKFLOWS]:
        body = text if rel == TRIGGER_WORKFLOW else as_text(rel, read_pinned(root, rel, PINNED_BLOBS[rel], drift))
        found = list(IDENTITY_LINE.finditer(body))
        if len(found) != 1:
            raise ExtractError(f"{rel}: expected one 'git config user.name' line, found {len(found)}")
        identities.append(found[0].group(1))
        lines.append({"file": rel, "line": body.count("\n", 0, found[0].start(1)) + 1})
    if len(set(identities)) != 1:
        raise ExtractError("the four workflows do not configure the same commit identity")
    facts["commit_identity_lines"] = lines
    return facts, identities[0]


def read_codeowners(root: Path, drift: list[str]) -> dict:
    """Rule lines of the CODEOWNERS file; the raw owners stay in memory under '_owners'."""
    text = as_text(CODEOWNERS, read_pinned(root, CODEOWNERS, PINNED_BLOBS[CODEOWNERS], drift))
    rules = [line.split() for line in text.split("\n") if line.strip() and not line.lstrip().startswith("#")]
    if not rules or any(len(rule) < 2 or not all(token.startswith("@") for token in rule[1:]) for rule in rules):
        raise ExtractError(f"{CODEOWNERS}: a rule line is not '<pattern> @owner ...'")
    owners = {token for rule in rules for token in rule[1:]}
    maintainers = set(re.findall(r"^# Maintainer: (@\S+?)\.?$", text, flags=re.MULTILINE))
    return {"file": CODEOWNERS, "rule_lines": len(rules), "distinct_owners": len(owners),
            "maintainer_comment_lines": len(maintainers), "_owners": owners, "_maintainers": maintainers}


def read_mailmap(root: Path, drift: list[str]) -> tuple[dict, set[str]]:
    """(commit name or None, commit e-mail) -> canonical e-mail, lower case, as gitmailmap defines the four forms;
    and the names the file writes, kept only to be searched for in the output."""
    text = as_text(MAILMAP, read_pinned(root, MAILMAP, PINNED_BLOBS[MAILMAP], drift))
    mapping: dict = {}
    names: set[str] = set()
    for line in text.split("\n"):
        line = line.split("#", 1)[0].strip()
        if not line:
            continue
        entry = MAILMAP_LINE.match(line)
        if not entry:
            raise ExtractError(f"{MAILMAP}: unexpected line shape")
        names |= {name.strip() for name in (entry.group("n1"), entry.group("n2")) if name and name.strip()}
        if entry.group("e2") is None:
            mapping[(None, entry.group("e1").lower())] = entry.group("e1").lower()
        else:
            mapping[(entry.group("n2").strip() or None, entry.group("e2").lower())] = entry.group("e1").lower()
    if not mapping:
        raise ExtractError(f"{MAILMAP}: no entry")
    return mapping, names


def count_agent_roles(root: Path, drift: list[str]) -> int:
    text = as_text(AGENT_TEAM, read_pinned(root, AGENT_TEAM, PINNED_BLOBS[AGENT_TEAM], drift))
    rows = ROLE_ROW.findall(text)
    if not rows:
        raise ExtractError(f"{AGENT_TEAM}: no role row found in the roles table")
    return len(rows)


def git(root: Path, *args: str) -> str:
    """Run one read-only git command; GIT_NO_LAZY_FETCH makes a partial clone fail instead of downloading a blob."""
    env = dict(os.environ, GIT_NO_LAZY_FETCH="1", GIT_TERMINAL_PROMPT="0", LC_ALL="C")
    try:
        done = subprocess.run(["git", "-C", str(root), "-c", "core.quotepath=false", *args],
                              capture_output=True, env=env, check=False)
    except OSError as exc:
        raise ExtractError(f"cannot run git: {exc}") from exc
    if done.returncode != 0:
        raise ExtractError(f"git {' '.join(args[:2])} failed: {done.stderr.decode('utf-8', 'replace').strip()[:300]}")
    return done.stdout.decode("utf-8")


def read_commits(root: Path, drift: list[str]) -> list[dict]:
    """One dict per commit reachable from the pin, newest first, raw identities included."""
    if git(root, "rev-parse", "--is-shallow-repository").strip() != "false":
        raise ExtractError("the clone is shallow: the commit history of the pin is not available")
    git(root, "cat-file", "-e", PINNED_COMMIT + "^{commit}")
    count = int(git(root, "rev-list", "--count", PINNED_COMMIT).strip())
    if count != PINNED_COMMITS:
        drift.append(f"{count} commits reachable from the pin, expected {PINNED_COMMITS}")
    commits = []
    for record in git(root, "log", "--format=" + LOG_FORMAT, PINNED_COMMIT).split("\x1e")[1:]:
        fields = record.rstrip("\n").split("\x1f")
        if len(fields) != 9:
            raise ExtractError(f"git log: a record has {len(fields)} fields, expected 9")
        commit, parents, name, mail, committer, committer_mail, date, subject, trailers = fields
        stamp = date[:-1] + "+00:00" if date.endswith("Z") else date  # fromisoformat reads "Z" only from Python 3.11
        moment = datetime.fromisoformat(stamp).astimezone(timezone.utc)
        commits.append({"commit": commit, "parents": len(parents.split()), "author": name, "address": mail.lower(),
                        "committer": committer, "committer_address": committer_mail.lower(),
                        "day": moment.date().isoformat(), "time": moment.strftime("%Y-%m-%dT%H:%M:%SZ"),
                        "subject": subject, "trailers": [t.strip() for t in trailers.split("\x1d") if t.strip()]})
    if len(commits) != count or len({c["commit"] for c in commits}) != count:
        raise ExtractError(f"git log returned {len(commits)} commits, rev-list counted {count}")
    by_name = sorted(tally([c["author"] for c in commits]).values(), reverse=True)
    lines = git(root, "shortlog", "-sn", PINNED_COMMIT).split("\n")
    shortlog = [int(line.split("\t")[0]) for line in lines if line.strip()]
    if shortlog != by_name:
        raise ExtractError(f"git shortlog -sn counts {shortlog} differ from the author-name counts {by_name}")
    return commits


def read_trigger_history(root: Path) -> list[tuple[str, str, str]]:
    """(commit, status, path) for every addition or deletion under state/triggers/, newest commit first."""
    out = git(root, "log", "--no-renames", "--name-status", "--format=" + NAME_STATUS_FORMAT, PINNED_COMMIT,
              "--", TOP + "/")
    changes = []
    for record in out.split("\x1e")[1:]:
        commit, _, rest = record.partition("\x1f")
        for line in rest.split("\n"):
            if not line.strip():
                continue
            status, _, path = line.partition("\t")
            if status not in ("A", "D", "M"):
                raise ExtractError(f"git log --name-status: unexpected status {status!r}")
            changes.append((commit, status, path))
    if not changes:
        raise ExtractError("git log found no change under state/triggers/")
    return changes


def label_commits(commits: list[dict], workflow_identity: str, mailmap: dict) -> tuple[dict, dict]:
    """Labels for author names, addresses and committers, and the counts the analysis needs."""
    authors = label_values(tally([c["author"] for c in commits]), "author {}")
    if workflow_identity not in authors:
        raise ExtractError("no commit is authored under the identity the trigger workflow configures")
    addresses: dict = {}
    for name, label in authors.items():
        mails = tally([c["address"] for c in commits if c["author"] == name])
        addresses |= {(name, mail): tag for mail, tag in
                      label_values(mails, "address " + label.split()[1] + "{}", numbered=True).items()}
    others = tally([c["committer"] for c in commits if c["committer"] not in authors])
    committers = dict(authors) | label_values(others, "committer X{}", numbered=True)
    labels = {"authors": authors, "addresses": addresses, "committers": committers}
    canonical = {name: len({mailmap.get((name, mail), mailmap.get((None, mail), mail))
                            for (owner, mail) in addresses if owner == name}) for name in authors}
    table = {
        "by_author": {authors[n]: k for n, k in sorted(tally([c["author"] for c in commits]).items(),
                                                       key=lambda item: authors[item[0]])},
        "by_author_address": {tag: sum(c["author"] == name and c["address"] == mail for c in commits)
                              for (name, mail), tag in sorted(addresses.items(), key=lambda item: item[1])},
        "identities_per_author_after_the_mailmap": {authors[n]: canonical[n] for n in sorted(authors, key=authors.get)},
        "author_configured_by_the_four_workflows": authors[workflow_identity],
        "committers": [
            {"committer": tag, "commits": sum(c["committer"] == name for c in commits),
             "also_an_author_string": name in authors,
             "addresses_all_no_reply_at_the_hosting_domain": all(
                 c["committer_address"].split("@") == ["noreply", HOSTING_DOMAIN]
                 for c in commits if c["committer"] == name)}
            for name, tag in sorted(committers.items(), key=lambda item: item[1])],
    }
    return labels, table


def commit_groups(commits: list[dict], labels: dict) -> list[dict]:
    """Commits counted by author, address, committer, class of subject, merge or not, and co-author trailers."""
    keys = []
    for c in commits:
        subject = ("trigger workflow template" if TRIGGER_SUBJECT.match(c["subject"]) else
                   "ends with a pull request number" if PULL_REQUEST_SUBJECT.search(c["subject"]) else "other")
        keys.append((labels["authors"][c["author"]], labels["addresses"][(c["author"], c["address"])],
                     labels["committers"][c["committer"]], subject, c["parents"] > 1, len(c["trailers"])))
    return [{"author": k[0], "address": k[1], "committer": k[2], "subject": k[3], "merge": k[4],
             "co_author_trailers": k[5], "commits": keys.count(k)} for k in sorted(set(keys))]


def summarise_trailers(commits: list[dict], labels: dict, senders: dict) -> dict:
    """Co-author trailers: one row per distinct trailer name, labelled; names and addresses are not written.

    A trailer name identical to a trigger sender takes that account's label, as a committer that is also an author
    string keeps the author label; the other names are numbered.
    """
    parsed = []
    for c in commits:
        for value in c["trailers"]:
            found = TRAILER.match(value)
            if not found:
                raise ExtractError("a Co-authored-by trailer is not 'name <local@domain>'")
            parsed.append((c, found.group(1), found.group(2).lower(), found.group(3).lower()))
    counts = tally([name for _, name, _, _ in parsed])
    names = {name: senders[name] for name in counts if name in senders}
    names |= label_values({n: k for n, k in counts.items() if n not in senders}, "co-author {}", numbered=True)
    domains = label_values(tally([domain for _, _, _, domain in parsed]), "domain D{}", numbered=True)
    labels["co_authors"] = names
    rows = []
    for name, tag in sorted(names.items(), key=lambda item: item[1]):
        mine = [(c, local, domain) for c, other, local, domain in parsed if other == name]
        rows.append({"co_author": tag, "trailer_lines": len(mine), "commits": len({c["commit"] for c, _, _ in mine}),
                     "name_ends_with_bot": name.endswith("[bot]"), "also_an_author_string": name in labels["authors"],
                     "same_string_as_a_trigger_sender": name in senders,
                     "address_is_no_reply": all(local == "noreply" for _, local, _ in mine),
                     "address_domains": sorted({domains[domain] for _, _, domain in mine})})
    with_trailer = [c for c in commits if c["trailers"]]
    return {
        "commits_with_at_least_one_trailer": len(with_trailer),
        "by_author": tally([labels["authors"][c["author"]] for c in with_trailer]),
        "by_number_of_trailers": {str(n): k for n, k in tally([len(c["trailers"]) for c in with_trailer]).items()},
        "trailer_lines": len(parsed),
        "distinct_trailer_names": len(names),
        "lines_with_a_no_reply_address_by_domain": tally([domains[domain] for _, _, local, domain in parsed
                                                          if local == "noreply"]),
        "lines_whose_name_ends_with_bot": sum(name.endswith("[bot]") for _, name, _, _ in parsed),
        "lines_whose_name_is_a_trigger_sender": sum(name in senders for _, name, _, _ in parsed),
        "co_authors": rows,
    }


def trigger_file_history(changes: list, commits: list[dict], labels: dict, at_pin: dict, identity: str,
                         schedules: set[str]) -> dict:
    """Every trigger file the history ever held: who added it, and what became of the ones absent at the pin.

    identity is the raw author string the trigger workflow configures; at_pin maps each trigger file present at
    the pin to its (type, repo), or to None when the workflow did not write it; schedules names the trigger files
    that define a schedule and record no event.
    """
    by_commit = {c["commit"]: c for c in commits}
    names = sorted({path.rsplit("/", 1)[1] for _, _, path in changes if path.endswith(".trigger.json")})
    events = [name for name in names if name not in schedules]
    rows, written, mismatches = [], [], 0
    for name in names:
        mine = [(commit, status, path) for commit, status, path in changes if path.rsplit("/", 1)[1] == name]
        first = [commit for commit, status, path in mine if status == "A" and path == f"{TOP}/{name}"]
        if len(first) != 1:
            raise ExtractError(f"{name}: added {len(first)} times directly under {TOP}/, expected once")
        added = by_commit[first[0]]
        subject = TRIGGER_SUBJECT.match(added["subject"])
        by_workflow = bool(subject) and added["author"] == identity
        written.append(by_workflow)
        if name in at_pin:
            if by_workflow:
                mismatches += (subject.group(1), subject.group(2)) != at_pin[name]
            continue
        if mine[0][1] != "D":
            raise ExtractError(f"{name}: absent at the pin but its last change is not a deletion")
        rows.append({"file": name, "colon_in_the_file_name": ":" in name,
                     "type_in_the_file_name": ANY_TRIGGER_NAME.match(name).group(2),
                     "added_by": labels["authors"][added["author"]], "added_with_the_trigger_subject": by_workflow,
                     "type_in_the_subject": subject.group(1) if by_workflow else None,
                     "repo_in_the_subject": subject.group(2) if by_workflow else None,
                     "subject_when_not_the_trigger_template": None if by_workflow else added["subject"],
                     "passed_through_processing": any(path.startswith(f"{TOP}/processing/") for _, _, path in mine),
                     "ever_in_the_archive": any(path.startswith(f"{ARCHIVE}/") for _, _, path in mine),
                     "removed_in_commit": mine[0][0][:7],
                     "removed_by": labels["authors"][by_commit[mine[0][0]]["author"]]})
    trigger_commits = [c for c in commits if TRIGGER_SUBJECT.match(c["subject"])]
    adds = tally([commit for commit, status, path in changes
                  if status == "A" and path.endswith(".trigger.json") and path.count("/") == TOP.count("/") + 1])
    return {
        "trigger_json_files_ever_added": len(names),
        "schedule_definitions": len(schedules & set(names)),
        "trigger_events_ever_added": len(events),
        "events_present_at_the_pin": sum(name in at_pin for name in events),
        "absent_at_the_pin": len(rows),
        "written_by_the_trigger_workflow": {
            "ever": sum(written), "absent_at_the_pin": sum(row["added_with_the_trigger_subject"] for row in rows)},
        "commits_with_the_trigger_subject": {
            "commits": len(trigger_commits),
            "by_author": tally([labels["authors"][c["author"]] for c in trigger_commits]),
            "adding_exactly_one_trigger_file": sum(adds.get(c["commit"], 0) == 1 for c in trigger_commits),
            "by_type_in_the_subject": tally([TRIGGER_SUBJECT.match(c["subject"]).group(1) for c in trigger_commits]),
            "by_repo_in_the_subject": tally([TRIGGER_SUBJECT.match(c["subject"]).group(2) for c in trigger_commits])},
        "subject_against_file_content": {
            "files_compared": sum(1 for name, flag in zip(names, written) if flag and name in at_pin),
            "type_or_repo_mismatches": mismatches},
        "absent_files": rows,
    }


def producer_versions(root: Path, commits: list[dict]) -> dict:
    """The changes to the trigger workflow that the last commit with the trigger subject does not contain."""
    trigger = [c for c in commits if TRIGGER_SUBJECT.match(c["subject"])]
    last = max(trigger, key=lambda c: c["time"])
    out = git(root, "log", "--format=" + VERSION_FORMAT, f"{last['commit']}..{PINNED_COMMIT}", "--", TRIGGER_WORKFLOW)
    later = []
    for record in out.split("\x1e")[1:]:
        commit, date, subject = record.rstrip("\n").split("\x1f")
        stamp = date[:-1] + "+00:00" if date.endswith("Z") else date
        later.append({"commit": commit, "day": datetime.fromisoformat(stamp).astimezone(timezone.utc).date().isoformat(),
                      "subject": subject})
    return {"last_commit_with_the_trigger_subject": last["commit"], "its_time_utc": last["time"],
            "trigger_subjects_ending_with_skip_ci": sum(c["subject"].endswith("[skip ci]") for c in trigger),
            "later_changes_to_the_workflow_file": later}


def plant_wrong_subject(commits: list[dict], changes: list, at_pin: dict) -> list[dict]:
    """Negative control: a copy in which the commit that added one surviving event names another type and repo."""
    target = next(commit for commit, status, path in reversed(changes)
                  if status == "A" and path.count("/") == TOP.count("/") + 1 and at_pin.get(path.rsplit("/", 1)[1]))
    return [dict(c, subject="trigger: planted from Elsewhere") if c["commit"] == target else c for c in commits]


def raw_identity_strings(events, top_rows, commits, owners, mailmap, mailmap_names, workflow_identity) -> set[str]:
    """Every identity string read from the sources, the names of the mailmap included: none may appear in the output."""
    raw = {e["sender"] for e in events} | {r["sender"] for r in top_rows if "sender" in r}
    raw |= {token for owner in owners for token in (owner, owner.lstrip("@"))} | {workflow_identity}
    for c in commits:
        raw |= {c["author"], c["address"], c["committer"], c["committer_address"]}
        for value in c["trailers"]:
            found = TRAILER.match(value)
            raw |= {found.group(1), f"{found.group(2)}@{found.group(3)}".lower()}
    raw |= {mail for _, mail in mailmap} | set(mailmap.values()) | mailmap_names
    return {value for value in raw if value}


def leak_check(text: str, raw: set[str]) -> dict:
    """Count the raw identity strings found in the output; two are public names of things, not of accounts."""
    exempt = {value for value in raw if value in (REPOSITORY.split("/")[1], "GitHub")}
    wanted = sorted(raw - exempt)
    planted = text + "\n" + wanted[0]
    return {"identity_strings_checked": len(wanted), "found_in_this_file": sum(value in text for value in wanted),
            "found_after_planting_one_of_them": sum(value in planted for value in wanted) > 0,
            "exempt_strings": len(exempt),
            "exempt_reason": "an author or committer string identical to the repository's name or to the hosting "
                             "platform's name cannot be told apart from that name; the labels still replace it"}


def trigger_section(events: list[dict], top_rows: list[dict], senders: dict, workflow: dict, roles: int) -> dict:
    top = [({k: v for k, v in row.items() if k not in ("sender", "timestamp", "event")}
            | ({"sender": senders[row["sender"]]} if "sender" in row else {})) for row in top_rows]
    days = sorted(e["timestamp"][:10] for e in events)
    return {
        "archived": {
            "events": len(events), "first_day": days[0], "last_day": days[-1],
            "keys": sorted(TOP_KEYS), "details_keys": sorted(DETAIL_KEYS),
            "by_type": tally([e["type"] for e in events]),
            "by_sender": tally([senders[e["sender"]] for e in events]),
            "by_repo": tally([e["repo"] for e in events]),
            "by_type_and_event_name": tally([f"{e['type']} <- {e['event']}" for e in events])},
        "outside_the_archive": {
            "files": top,
            "events_written_by_the_trigger_workflow": sum(r["kind"].startswith("event written") for r in top),
            "by_sender": tally([r["sender"] for r in top if "sender" in r]),
            "by_repo": tally([r["repo"] for r in top if "sender" in r])},
        "producer": workflow,
        "agent_roles_defined_in_the_agent_team_file": {"file": AGENT_TEAM, "role_rows": roles},
    }


def source_section(archive_pin: dict, drift: list[str], first_day: str, last_day: str, last_trigger: str) -> dict:
    return {
        "repository": REPOSITORY,
        "commit": None if drift else PINNED_COMMIT,
        "commit_check": ("FAILED: " + "; ".join(drift)) if drift else
                        "the archive has the file count, Git tree id and manifest digest recorded for this commit; every "
                        "other file read has its recorded Git blob id (CRLF normalised to LF); the commit resolves and "
                        "the number of commits reachable from it is the recorded one",
        "trigger_archive": archive_pin | {
            "folder": ARCHIVE,
            "git_tree_id_command": f"git ls-tree {PINNED_COMMIT} {TOP}/",
            "manifest_rule": "SHA-256 of the lines '<blob id> <repository path>\\n', one per file, sorted by path bytes",
            "manifest_command": f"git ls-tree -r {PINNED_COMMIT} -- {ARCHIVE} | awk '{{print $3\" \"$4}}' | sha256sum"},
        "files": [{"path": f"{TOP}/{name}", "git_blob": blob} for name, blob in sorted(TOP_FILES.items())]
                 + [{"path": path, "git_blob": blob} for path, blob in PINNED_BLOBS.items()],
        "git_history": {
            "commits_read": PINNED_COMMITS, "first_commit_day_utc": first_day, "last_commit_day_utc": last_day,
            "reads": "commit objects and trees only; no file content of an earlier commit",
            "commands": [
                "git rev-parse --is-shallow-repository",
                f"git cat-file -e {PINNED_COMMIT}^{{commit}}",
                f"git rev-list --count {PINNED_COMMIT}",
                f"git log --format={LOG_FORMAT} {PINNED_COMMIT}",
                f"git shortlog -sn {PINNED_COMMIT}",
                f"git log --no-renames --name-status --format={NAME_STATUS_FORMAT} {PINNED_COMMIT} -- {TOP}/",
                f"git log --format={VERSION_FORMAT} {last_trigger}..{PINNED_COMMIT} -- {TRIGGER_WORKFLOW}"]},
    }


LABEL_RULE = {
    "rule": "each distinct raw value is replaced by a label before anything is written; labels go by descending count, "
            "ties by the SHA-256 of the value, which is not stored",
    "account": "the sender field of a trigger file (a platform username)",
    "author": "the author name of a commit (a string configured in the committing tool)",
    "address": "the author e-mail address of a commit; 'address A01' is the most frequent address of author A",
    "committer": "the committer name of a commit; a committer that is also an author string keeps the author label",
    "co-author": "the name in a Co-authored-by trailer of a commit message; a name identical to a trigger sender takes "
                 "that account's label",
    "domain": "the part of a trailer address after the at sign",
    "automation": "written in a label only when the raw name ends in [bot]",
}


def build(root: Path, allow_drift: bool) -> dict:
    drift: list[str] = []
    events, archive_pin = read_archive(root, drift)
    top_rows = read_top_folder(root, drift)
    workflow, workflow_identity = read_workflows(root, drift)
    owners = read_codeowners(root, drift)
    mailmap, mailmap_names = read_mailmap(root, drift)
    roles = count_agent_roles(root, drift)
    commits = read_commits(root, drift)
    changes = read_trigger_history(root)
    if drift and not allow_drift:
        raise ExtractError(f"the sources are not those of commit {PINNED_COMMIT}:\n  " + "\n  ".join(drift)
                           + "\n(--allow-drift snapshots them anyway; the lesson's numbers then no longer apply)")
    workflow["versions"] = producer_versions(root, commits)
    with_sender = events + [row for row in top_rows if "sender" in row]
    senders = label_values(tally([e["sender"] for e in with_sender]), "account {}")
    labels, commit_table = label_commits(commits, workflow_identity, mailmap)
    at_pin = {e["file"]: (e["type"], e["repo"]) for e in with_sender}
    at_pin |= {row["file"]: None for row in top_rows if row["file"].endswith(".trigger.json") and "sender" not in row}
    schedules = {row["file"] for row in top_rows if row["kind"].startswith("a schedule definition")}
    history = trigger_file_history(changes, commits, labels, at_pin, workflow_identity, schedules)
    history["subject_against_file_content"]["mismatches_after_planting_one_wrong_subject"] = trigger_file_history(
        changes, plant_wrong_subject(commits, changes, at_pin), labels, at_pin, workflow_identity, schedules
    )["subject_against_file_content"]["type_or_repo_mismatches"]
    snapshot = {
        "schema_version": "0.1.0",
        "module_id": "psy-024-the-single-actor",
        "kind": "observed",
        "source": source_section(archive_pin, drift, min(c["day"] for c in commits), max(c["day"] for c in commits),
                                 workflow["versions"]["last_commit_with_the_trigger_subject"]),
        "labels": LABEL_RULE,
        "trigger_log": trigger_section(events, top_rows, senders, workflow, roles),
        "ownership": {k: v for k, v in owners.items() if not k.startswith("_")} | {
            "the_only_owner_is_the_sender_of_every_event": owners["_owners"] == {"@" + s for s in senders},
            "the_maintainer_comment_names_that_owner": owners["_maintainers"] == owners["_owners"],
            "label_of_that_account": sorted(senders.values())[0] if len(senders) == 1 else None},
        "commit_log": {"commits": len(commits), "merge_commits": sum(c["parents"] > 1 for c in commits)}
                      | commit_table | {
            "mailmap": {"file": MAILMAP, "entries": len(mailmap)},
            "groups": commit_groups(commits, labels),
            "co_author_trailers": summarise_trailers(commits, labels, senders)},
        "trigger_file_history": history,
    }
    raw = raw_identity_strings(events, top_rows, commits, owners["_owners"], mailmap, mailmap_names, workflow_identity)
    check = leak_check(json.dumps(snapshot, ensure_ascii=False, indent=2), raw)
    if check["found_in_this_file"] or not check["found_after_planting_one_of_them"]:
        raise ExtractError("an identity string would be written to the output, or the check for it does not work")
    snapshot["identity_check"] = check
    return snapshot


def main() -> int:
    here = FIXTURE_FILE
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--repo-root", type=Path, default=here.parents[5])
    parser.add_argument("--output", type=Path, default=here.with_name("observed-input.json"))
    parser.add_argument("--allow-drift", action="store_true",
                        help="snapshot sources that differ from the pinned commit")
    args = parser.parse_args()
    try:
        snapshot = build(args.repo_root, args.allow_drift)
    except (ExtractError, OSError) as exc:
        print(f"extract.py: {exc}", file=sys.stderr)
        return 1
    text = json.dumps(snapshot, ensure_ascii=False, indent=2) + "\n"
    args.output.write_bytes(text.encode("utf-8"))
    log = snapshot["trigger_log"]["archived"]
    print(f"extract.py: {log['events']} archived events, {len(log['by_sender'])} sender label(s); "
          f"{snapshot['commit_log']['commits']} commits, {len(snapshot['commit_log']['by_author'])} author labels "
          f"-> {args.output.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
