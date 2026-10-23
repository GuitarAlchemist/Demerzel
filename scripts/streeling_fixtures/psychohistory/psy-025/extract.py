#!/usr/bin/env python3
"""PSY-025 extract: the module history and the pinned library that a forecast about Streeling resolves on.

Two observed inputs, both at the pinned commit:

1. The history of state/streeling/courses, from one `git log --name-status`
   call (commits and trees only, nothing downloaded): the commits that added
   or removed an English module file, with their committer times. The
   analysis takes its base rate from these rows.
2. Every file of state/streeling/courses at the pin, read from the working
   tree, each checked against its pinned Git blob id, and one manifest digest
   over all of them: the path, and the `module_id` and `department` of the
   file's front matter when it has one. The analysis tests the forecast's
   counting rule on these lines.

Fails with a non-zero exit and a message when git is missing, the clone is
shallow, the pinned commit is absent, the history is not the pinned one, a path
has an unexpected shape, or a file differs from its pinned blob (--allow-drift
records the files anyway, with "commit": null for the library).

Run from the repository root:
    python -I -B scripts/streeling_fixtures/psychohistory/psy-025/extract.py
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
                / "state/streeling/fixtures/psychohistory/psy-025" / Path(__file__).name)

PINNED_COMMIT = "4b03838800dcd4894f1e026461979bff1d985ca8"
LIBRARY = "state/streeling/courses"
# Constants of the pinned history and tree (README.md gives the one-line git checks).
EXPECTED_COMMITS_REACHABLE = 1599
EXPECTED_COMMITS_TOUCHING_LIBRARY = 73
# SHA-256 of the 73 commit ids, oldest first, one per line, each ended by "\n".
EXPECTED_COMMIT_LIST_SHA256 = "85f15934a53a7561afc81c28ead2122846f62e436983bb74e4a1cdb346877f98"
# Git tree id of state/streeling/courses at the pin, its file count, and the SHA-256 of the lines
# "<blob id> <path>\n" of those files sorted by path bytes (git ls-tree -r prints them in that order here).
EXPECTED_TREE_AT_PIN = "fc6abc23bd76b00ae37366ac6d9f70186573dd5d"
EXPECTED_FILES_AT_PIN = 255
EXPECTED_MANIFEST_SHA256 = "57f10ef77065c108f5c08bb23a4f0c76b6420b3604f6aeb0a675487abcf9b33e"

SHA = re.compile(r"^[0-9a-f]{40}$")
LANGUAGE = re.compile(r"^[a-z]{2}$")
PREFIX = LIBRARY + "/"
LOG_FORMAT = "%x01%H %ct %P"
KEY_LINE = re.compile(r"^([A-Za-z_][A-Za-z0-9_]*):[ \t]*(.*)$")


class ExtractError(Exception):
    """git is unusable here, the history is not the pinned one, or a source file has an unexpected shape."""


class Git:
    """Runs git with an argument list (no shell) and records each command once."""

    def __init__(self, root: Path) -> None:
        self.root = root
        self.commands: list[str] = []
        # Never download a missing object: the history needs commits and trees only.
        self.env = dict(os.environ, GIT_NO_LAZY_FETCH="1", GIT_TERMINAL_PROMPT="0", LC_ALL="C")

    def run(self, *args: str, record: str | None = None, ok: tuple[int, ...] = (0,)) -> str:
        if record is not None and f"git {record}" not in self.commands:
            self.commands.append(f"git {record}")
        try:
            done = subprocess.run(["git", "-C", str(self.root), *args], capture_output=True, env=self.env, check=False)
        except OSError as exc:
            raise ExtractError(f"cannot run git: {exc}") from exc
        if done.returncode not in ok:
            message = done.stderr.decode("utf-8", "replace").strip().splitlines()
            raise ExtractError(f"git {' '.join(args)} failed (exit {done.returncode}): {message[-1] if message else ''}")
        return done.stdout.decode("utf-8")


def utc(seconds: int) -> str:
    return datetime.fromtimestamp(seconds, tz=timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def module_name(path: str) -> str | None:
    """'department/name' for an English module path (<department>/en/<name>.md, not README.md), else None."""
    if not path.startswith(PREFIX):
        raise ExtractError(f"path outside {LIBRARY}: {path!r}")
    parts = path[len(PREFIX):].split("/")
    if len(parts) == 3 and LANGUAGE.match(parts[1]) and parts[2].endswith(".md"):
        if parts[1] == "en" and parts[2].lower() != "readme.md":
            return f"{parts[0]}/{parts[2][:-3]}"
        return None
    if len(parts) > 3:
        raise ExtractError(f"unexpected path shape under {LIBRARY}: {path!r}")
    return None


def check_clone(git: Git) -> int:
    """Refuses a folder that is not a full-history clone holding the pin; returns the commits reachable from it."""
    if not git.run("rev-parse", "--git-dir", ok=(0, 128)).strip():
        raise ExtractError(f"{git.root} is not a git repository (--repo-root must name a clone of the repository)")
    if git.run("rev-parse", "--is-shallow-repository", record="rev-parse --is-shallow-repository").strip() != "false":
        raise ExtractError("this clone is shallow: the history of the pinned commit is incomplete "
                           "(fetch it with `git fetch --unshallow --filter=blob:none`)")
    kind = git.run("cat-file", "-t", PINNED_COMMIT, record=f"cat-file -t {PINNED_COMMIT}", ok=(0, 128)).strip()
    if kind != "commit":
        raise ExtractError(f"pinned commit {PINNED_COMMIT} is not in this clone")
    return int(git.run("rev-list", "--count", PINNED_COMMIT, record=f"rev-list --count {PINNED_COMMIT}"))


def read_log(git: Git) -> list[dict]:
    """The commits that touch the library, oldest first, each with its committer time, parents and changes."""
    out = git.run("log", "--topo-order", "--reverse", "--no-renames", "--name-status", "-z",
                  f"--format={LOG_FORMAT}", PINNED_COMMIT, "--", LIBRARY,
                  record=f"log --topo-order --reverse --no-renames --name-status -z --format='{LOG_FORMAT}' "
                         f"{PINNED_COMMIT} -- {LIBRARY}")
    tokens = out.split("\0")
    if tokens and tokens[-1] == "":
        tokens.pop()
    commits, index = [], 0
    while index < len(tokens):
        header = tokens[index]
        fields = header[1:].split(" ")
        if not header.startswith("\x01") or len(fields) < 2 or not SHA.match(fields[0]) or not fields[1].isdigit() \
                or not all(SHA.match(parent) for parent in fields[2:]):
            raise ExtractError(f"unexpected commit header in the output of git log: {header[:80]!r}")
        index += 1
        changes = []
        while index < len(tokens) and not tokens[index].startswith("\x01"):
            status = tokens[index].lstrip("\n")
            if status not in ("A", "D", "M", "T") or index + 1 >= len(tokens):
                raise ExtractError(f"{fields[0]}: unexpected change status {status!r} in the output of git log")
            changes.append((status, tokens[index + 1]))
            index += 2
        commits.append({"commit": fields[0], "time": int(fields[1]), "parents": fields[2:], "changes": changes})
    if not commits:
        raise ExtractError(f"git log lists no commit that touches {LIBRARY}")
    return commits


def read_history(git: Git, reachable: int) -> tuple[list[dict], dict]:
    """The listed commits and the facts that identify the history; refuses any history but the pinned one."""
    log = read_log(git)
    ids = [entry["commit"] for entry in log]
    facts = {
        "commits_reachable_from_pin": reachable,
        "commits_touching_library": len(ids),
        "commit_list_sha256": hashlib.sha256("".join(c + "\n" for c in ids).encode("ascii")).hexdigest(),
        "tree_of_library_at_pin": git.run("rev-parse", f"{PINNED_COMMIT}:{LIBRARY}",
                                          record=f"rev-parse {PINNED_COMMIT}:{LIBRARY}").strip(),
    }
    expected = {"commits_reachable_from_pin": EXPECTED_COMMITS_REACHABLE,
                "commits_touching_library": EXPECTED_COMMITS_TOUCHING_LIBRARY,
                "commit_list_sha256": EXPECTED_COMMIT_LIST_SHA256, "tree_of_library_at_pin": EXPECTED_TREE_AT_PIN}
    drift = [f"{key} is {facts[key]}, expected {value}" for key, value in expected.items() if facts[key] != value]
    if drift:
        raise ExtractError("the history read here is not the pinned one (incomplete clone, graft or replace ref?):\n  "
                           + "\n  ".join(drift))
    if ids[-1] != PINNED_COMMIT or any(len(entry["parents"]) != 1 for entry in log):
        raise ExtractError("the listed commits must end at the pin and each have one parent (no merge to replay)")
    times = [entry["time"] for entry in log]
    if any(later < earlier for earlier, later in zip(times, times[1:])):
        raise ExtractError("committer times decrease along the ancestry order: a dated count would be ambiguous")
    return log, facts


def replay(git: Git, log: list[dict]) -> tuple[list[dict], set[str]]:
    """Replays every path change; returns one row per commit that changed the set of English modules."""
    paths: set[str] = set()
    modules: set[str] = set()
    rows = []
    for entry in log:
        for status, path in entry["changes"]:
            if (path in paths) == (status == "A"):
                raise ExtractError(f"{entry['commit']}: status {status} for {path!r}, which is "
                                   f"{'already' if path in paths else 'not'} in the replayed file list")
            if status == "A":
                paths.add(path)
            elif status == "D":
                paths.remove(path)
        now = {name for name in map(module_name, paths) if name is not None}
        if now != modules:
            rows.append({"commit": entry["commit"], "committed_utc": utc(entry["time"]),
                         "added": sorted(now - modules), "removed": sorted(modules - now)})
        modules = now
    listing = git.run("ls-tree", "-r", "-z", "--name-only", PINNED_COMMIT, "--", LIBRARY,
                      record=f"ls-tree -r -z --name-only {PINNED_COMMIT} -- {LIBRARY}")
    if {path for path in listing.split("\0") if path} != paths:
        raise ExtractError("the file list replayed from the commit log differs from the tree stored at the pin")
    return rows, paths


def front_matter(text: str) -> dict:
    """Top-level `key: value` lines between a first line '---' and the next line '---'; {} when there is none."""
    lines = text.split("\n")
    if not lines or lines[0].rstrip("\r") != "---":
        return {}
    keys = {}
    for line in lines[1:]:
        line = line.rstrip("\r")
        if line == "---":
            return keys
        match = KEY_LINE.match(line)
        if match:
            keys[match.group(1)] = match.group(2).strip().strip('"').strip("'")
    raise ExtractError("front matter opened with '---' is never closed")


def blob_id(data: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(data)).encode("ascii") + b"\0" + data).hexdigest()


def read_library(git: Git, allow_drift: bool) -> tuple[list[str], dict]:
    """One line per file of the library at the pin: '<path under the library> <module_id or -> <department or ->'."""
    listing = git.run("ls-tree", "-r", "-z", PINNED_COMMIT, "--", LIBRARY,
                      record=f"ls-tree -r -z {PINNED_COMMIT} -- {LIBRARY}")
    entries = []
    for item in (part for part in listing.split("\0") if part):
        meta, path = item.split("\t", 1)
        mode, kind, blob = meta.split(" ")
        if kind != "blob" or not SHA.match(blob):
            raise ExtractError(f"unexpected tree entry under {LIBRARY}: {item!r}")
        entries.append((path, blob))
    if [path for path, _ in entries] != sorted((path for path, _ in entries), key=lambda p: p.encode("utf-8")):
        raise ExtractError("git ls-tree did not list the files in path-byte order: the manifest command would differ")
    lines, drifted, with_front_matter = [], [], 0
    for path, blob in entries:
        data = (git.root / path).read_bytes()
        if blob_id(data) != blob:
            drifted.append(path)
        keys = front_matter(data.decode("utf-8")) if path.endswith(".md") else {}
        with_front_matter += bool(keys)
        fields = [keys.get("module_id") or "-", keys.get("department") or "-"]
        if any(" " in value for value in fields):
            raise ExtractError(f"{path}: a module_id or department contains a space")
        lines.append(" ".join([path[len(PREFIX):], *fields]))
    if drifted and not allow_drift:
        raise ExtractError(f"{len(drifted)} file(s) differ from their pinned blob, first {drifted[0]} "
                           "(check out the pinned commit, or pass --allow-drift)")
    manifest = hashlib.sha256("".join(f"{blob} {path}\n" for path, blob in entries).encode("utf-8")).hexdigest()
    facts = {"files": len(entries), "manifest_sha256": manifest, "files_with_front_matter": with_front_matter,
             "files_differing_from_their_pinned_blob": len(drifted)}
    if not allow_drift and (len(entries), manifest) != (EXPECTED_FILES_AT_PIN, EXPECTED_MANIFEST_SHA256):
        raise ExtractError(f"library at the pin: {len(entries)} files, manifest {manifest}; expected "
                           f"{EXPECTED_FILES_AT_PIN} files, manifest {EXPECTED_MANIFEST_SHA256}")
    return lines, facts


def source_section(git: Git, facts: dict, library: dict, drift: bool) -> dict:
    return {
        "repository": "GuitarAlchemist/Demerzel",
        "commit": PINNED_COMMIT,
        "library_path": LIBRARY,
        "commands": git.commands,
        "history_objects_read": "commits and trees only; the file contents come from the working tree, checked "
                                "against the blob ids of the pinned tree",
        "history_check": "the pin resolves to a commit of a non-shallow clone; the commits reachable from it, the "
                         "commits that touch the library, the SHA-256 of their ids and the library's tree id equal "
                         "the constants embedded in extract.py; the file list replayed from the log equals the "
                         "pinned tree",
        "manifest_check": "SHA-256 of the lines '<blob id> <path>' of every library file at the pin, sorted by path "
                          "bytes, each ended by a newline; reproduce with: git ls-tree -r " + PINNED_COMMIT + " -- "
                          + LIBRARY + " | awk '{print $3\" \"$4}' | sha256sum",
        **facts,
        "library": {"commit": None if drift and library["files_differing_from_their_pinned_blob"] else PINNED_COMMIT,
                    **library},
    }


def definitions_section() -> dict:
    return {
        "history_rows": "one row per listed commit after which the set of English module paths differs from the "
                        "set after the previous listed commit; 'added' and 'removed' name <department>/<file name "
                        "without .md>; a rename is one removal and one addition",
        "english_module_path": "state/streeling/courses/<department>/en/<name>.md with a file name other than "
                               "README.md (case-insensitive); the history can only count paths, because the "
                               "blobless clone holds no old file contents",
        "committed_utc": "committer date of the commit, in UTC; the listed commits form one line of ancestry and "
                         "their committer times never decrease along it",
        "library_files": "every file under state/streeling/courses at the pin: '<path below that folder> "
                         "<module_id> <department>', the last two from the file's front matter, '-' when absent",
    }


def build(root: Path, allow_drift: bool) -> dict:
    """The snapshot: checks of the clone and of the history, the replay, the library, then the sections."""
    git = Git(root)
    log, facts = read_history(git, check_clone(git))
    rows, paths = replay(git, log)
    lines, library = read_library(git, allow_drift)
    return {
        "schema_version": "0.1.0",
        "module_id": "psy-025-capstone-preregistered-forecast",
        "kind": "observed",
        "source": source_section(git, facts, library, allow_drift),
        "definitions": definitions_section(),
        "counts": {"history_rows": len(rows), "first_listed_commit_utc": utc(log[0]["time"]),
                   "pin_commit_utc": utc(log[-1]["time"]), "files_at_pin": len(paths),
                   "english_module_paths_at_pin": sum(module_name(path) is not None for path in paths)},
        "history": rows,
        "library_files": lines,
    }


def main() -> int:
    here = FIXTURE_FILE
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--repo-root", type=Path, default=here.parents[5],
                        help="a clone of the repository with the full commit history (blobs of the pin checked out)")
    parser.add_argument("--output", type=Path, default=here.with_name("observed-input.json"))
    parser.add_argument("--allow-drift", action="store_true",
                        help="record library files that differ from their pinned blob instead of stopping")
    args = parser.parse_args()
    try:
        snapshot = build(args.repo_root.resolve(), args.allow_drift)
    except (ExtractError, OSError, UnicodeDecodeError, ValueError) as exc:
        print(f"extract.py: {exc}", file=sys.stderr)
        return 1
    args.output.write_bytes((json.dumps(snapshot, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))
    counts = snapshot["counts"]
    print(f"extract.py: {counts['history_rows']} commits changed the English modules from "
          f"{counts['first_listed_commit_utc']} to {counts['pin_commit_utc']}; {counts['files_at_pin']} library "
          f"files at the pin, {counts['english_module_paths_at_pin']} English module paths -> {args.output.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
