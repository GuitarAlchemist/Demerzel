#!/usr/bin/env python3
"""PSY-010 extract: count the English course modules at each commit of the history.

Asks git, in one `git log --name-status` call, for the commits among the
ancestors of the pinned commit that touched state/streeling/courses and for the
paths each of them added, deleted or modified. Replays those changes to rebuild
the folder's file list at every listed commit, checks the rebuilt list against
the tree git stores at the first listed commit and at the pin, and writes
observed-input.json next to this script. The analysis script reads only that
snapshot.

Only commits and trees are read: no command here asks for the content of a
file, so a blobless partial clone is enough and nothing is downloaded. Every
command names the pinned commit; none depends on what is checked out.

It also lists the department records at the pin (file names only).

Fails with a non-zero exit and a message when git is missing, the clone is
shallow, the pinned commit is absent, the history is not the pinned one, or a
path under the folder has an unexpected shape.

Run from the repository root:
    python -I scripts/streeling_fixtures/psychohistory/psy-010/extract.py
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
                / "state/streeling/fixtures/psychohistory/psy-010" / Path(__file__).name)

PINNED_COMMIT = "4b03838800dcd4894f1e026461979bff1d985ca8"
HISTORY_PATH = "state/streeling/courses"
DEPARTMENTS_PATH = "state/streeling/departments"
# Constants of the pinned history (README.md gives the one-line git checks).
EXPECTED_COMMITS_REACHABLE = 1599
EXPECTED_COMMITS_TOUCHING_PATH = 73
# SHA-256 of the 73 commit ids, oldest first, one per line, each ended by "\n".
EXPECTED_COMMIT_LIST_SHA256 = "85f15934a53a7561afc81c28ead2122846f62e436983bb74e4a1cdb346877f98"
# Git tree id of state/streeling/courses at the pinned commit.
EXPECTED_TREE_AT_PIN = "fc6abc23bd76b00ae37366ac6d9f70186573dd5d"

SHA = re.compile(r"^[0-9a-f]{40}$")
LANGUAGE = re.compile(r"^[a-z]{2}$")
PREFIX = HISTORY_PATH + "/"
CLASSES = ("module", "en_readme", "translation", "readme", "flat_layout")
LOG_FORMAT = "%x01%H %ct %at %P"
SECONDS_PER_DAY = 86400


class ExtractError(Exception):
    """git is unusable here, or the history is not the pinned one."""


class Git:
    """Runs git with an argument list (no shell) and records each command once."""

    def __init__(self, root: Path) -> None:
        self.root = root
        self.commands: list[str] = []
        # Never download a missing object: this script needs commits and trees only.
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


def classify(path: str) -> tuple[str, str]:
    """Class of one path under HISTORY_PATH, and its 'department/name' when it is a module."""
    if not path.startswith(PREFIX):
        raise ExtractError(f"path outside {HISTORY_PATH}: {path!r}")
    parts = path[len(PREFIX):].split("/")
    name = parts[-1]
    if len(parts) == 1:
        return ("readme" if name == "README.md" else "flat_layout"), ""
    if len(parts) == 2 and name == "README.md":
        return "readme", ""
    if len(parts) == 3 and LANGUAGE.match(parts[1]) and name.endswith(".md"):
        if parts[1] != "en":
            return "translation", ""
        if name.lower() == "readme.md":
            return "en_readme", ""
        return "module", f"{parts[0]}/{name[:-3]}"
    raise ExtractError(f"unexpected path shape under {HISTORY_PATH}: {path!r}")


def utc(seconds: int) -> str:
    return datetime.fromtimestamp(seconds, tz=timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def read_log(git: Git) -> list[dict]:
    """The listed commits, oldest first, each with its dates, parents and (status, path) changes."""
    select = f"{PINNED_COMMIT} -- {HISTORY_PATH}"
    out = git.run("log", "--topo-order", "--reverse", "--no-renames", "--name-status", "-z",
                  f"--format={LOG_FORMAT}", PINNED_COMMIT, "--", HISTORY_PATH,
                  record=f"log --topo-order --reverse --no-renames --name-status -z --format='{LOG_FORMAT}' {select}")
    tokens = out.split("\0")
    if tokens and tokens[-1] == "":
        tokens.pop()
    commits, index = [], 0
    while index < len(tokens):
        header = tokens[index]
        fields = header[1:].split(" ")
        if not header.startswith("\x01") or len(fields) < 3 or not SHA.match(fields[0]) \
                or not fields[1].isdigit() or not fields[2].isdigit() or not all(SHA.match(p) for p in fields[3:]):
            raise ExtractError(f"unexpected commit header in the output of git log: {header[:80]!r}")
        index += 1
        changes = []
        while index < len(tokens) and not tokens[index].startswith("\x01"):
            status = tokens[index].lstrip("\n")
            if status not in ("A", "D", "M", "T") or index + 1 >= len(tokens):
                raise ExtractError(f"{fields[0]}: unexpected change status {status!r} in the output of git log")
            changes.append((status, tokens[index + 1]))
            index += 2
        commits.append({"commit": fields[0], "committer": int(fields[1]), "author": int(fields[2]),
                        "parents": fields[3:], "changes": changes})
    if not commits:
        raise ExtractError(f"git log lists no commit that touches {HISTORY_PATH}")
    return commits


def tree_listing(git: Git, commit: str) -> set[str]:
    listing = git.run("ls-tree", "-r", "-z", "--name-only", commit, "--", HISTORY_PATH,
                      record=f"ls-tree -r -z --name-only <commit> -- {HISTORY_PATH}   "
                             "(twice: at the first listed commit and at the pinned commit)")
    return {path for path in listing.split("\0") if path}


def department_records(git: Git) -> list[str]:
    """Names of the department records at the pin: the files <name>.department.json under DEPARTMENTS_PATH."""
    folder, suffix = DEPARTMENTS_PATH + "/", ".department.json"
    listing = git.run("ls-tree", "-z", "--name-only", PINNED_COMMIT, "--", folder,
                      record=f"ls-tree -z --name-only {PINNED_COMMIT} -- {folder}")
    names = [path[len(folder):-len(suffix)] for path in listing.split("\0")
             if path.startswith(folder) and path.endswith(suffix) and "/" not in path[len(folder):]]
    if not names:
        raise ExtractError(f"no department record under {DEPARTMENTS_PATH} at the pinned commit")
    return sorted(names)


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


def read_history(git: Git, reachable: int) -> tuple[list[dict], dict]:
    """The listed commits and the facts that identify the history; refuses any history but the pinned one."""
    select = f"{PINNED_COMMIT} -- {HISTORY_PATH}"
    log = read_log(git)
    ids = [entry["commit"] for entry in log]
    digest = hashlib.sha256("".join(commit + "\n" for commit in ids).encode("ascii")).hexdigest()
    full_history = int(git.run("rev-list", "--count", "--full-history", PINNED_COMMIT, "--", HISTORY_PATH,
                               record=f"rev-list --count --full-history {select}"))
    first_parent = git.run("rev-list", "--first-parent", PINNED_COMMIT, "--", HISTORY_PATH,
                           record=f"rev-list --first-parent {select}").split()
    tree_at_pin = git.run("rev-parse", f"{PINNED_COMMIT}:{HISTORY_PATH}",
                          record=f"rev-parse {PINNED_COMMIT}:{HISTORY_PATH}").strip()
    facts = {
        "commits_reachable_from_pin": reachable,
        "commits_touching_path": len(ids),
        "commits_touching_path_full_history": full_history,
        "commits_touching_path_on_first_parent_chain": len(first_parent),
        "commit_list_sha256": digest,
        "tree_of_history_path_at_pin": tree_at_pin,
    }
    check_drift(facts)
    check_single_line(log, full_history, first_parent)
    return log, facts


def check_drift(facts: dict) -> None:
    """Compares the four fingerprints of the history with the constants at the top of this file."""
    reachable, listed = facts["commits_reachable_from_pin"], facts["commits_touching_path"]
    digest, tree_at_pin = facts["commit_list_sha256"], facts["tree_of_history_path_at_pin"]
    drift = []
    if reachable != EXPECTED_COMMITS_REACHABLE:
        drift.append(f"{reachable} commits reachable from the pin, expected {EXPECTED_COMMITS_REACHABLE}")
    if listed != EXPECTED_COMMITS_TOUCHING_PATH:
        drift.append(f"{listed} commits touch {HISTORY_PATH}, expected {EXPECTED_COMMITS_TOUCHING_PATH}")
    if digest != EXPECTED_COMMIT_LIST_SHA256:
        drift.append(f"commit list digest {digest}, expected {EXPECTED_COMMIT_LIST_SHA256}")
    if tree_at_pin != EXPECTED_TREE_AT_PIN:
        drift.append(f"tree of {HISTORY_PATH} at the pin is {tree_at_pin}, expected {EXPECTED_TREE_AT_PIN}")
    if drift:
        raise ExtractError("the history read here is not the pinned one (incomplete clone, graft or replace ref?):\n  "
                           + "\n  ".join(drift))


def check_single_line(log: list[dict], full_history: int, first_parent: list[str]) -> None:
    """Refuses a history whose listed commits are not one dated line ending at the pin."""
    ids = [entry["commit"] for entry in log]
    times = [entry["committer"] for entry in log]
    if ids[-1] != PINNED_COMMIT:
        raise ExtractError("the pinned commit is not the last commit of the list: it did not touch the folder")
    if full_history != len(ids):
        raise ExtractError(f"--full-history lists {full_history} commits, the default walk {len(ids)}: "
                           "a side branch touched the folder and the series is not a single line")
    if set(first_parent) != set(ids):
        raise ExtractError("some listed commits are not on the first-parent chain of the pin: "
                           "the commits are not totally ordered by ancestry")
    if any(len(entry["parents"]) != 1 for entry in log):
        raise ExtractError("a listed commit is a merge or a root commit: git log shows no path changes for a merge, "
                           "so the replay below would be incomplete")
    if any(later < earlier for earlier, later in zip(times, times[1:])):
        raise ExtractError("committer times decrease along the ancestry order: a date-based series would be ambiguous")


def apply_changes(entry: dict, paths: set[str]) -> dict:
    """Adds and removes the commit's paths in `paths`; returns how many it added, deleted and modified."""
    commit, tally = entry["commit"], {"A": 0, "D": 0, "M": 0, "T": 0}
    for status, path in entry["changes"]:
        if (path in paths) == (status == "A"):
            raise ExtractError(f"{commit}: status {status} for {path!r}, which is "
                               f"{'already' if path in paths else 'not'} in the replayed file list")
        if status == "A":
            paths.add(path)
        elif status == "D":
            paths.remove(path)
        tally[status] += 1
    if not entry["changes"] or not paths:
        raise ExtractError(f"{commit}: no path change, or no file left under {HISTORY_PATH}")
    return {"added": tally["A"], "deleted": tally["D"], "modified": tally["M"] + tally["T"]}


def census(commit: str, paths: set[str]) -> tuple[dict, set[str], set[str]]:
    """Number of paths in each class, the module names and the flat-layout paths among `paths`."""
    classes = dict.fromkeys(CLASSES, 0)
    modules, flat = set(), set()
    for path in paths:
        kind, module = classify(path)
        classes[kind] += 1
        if kind == "module":
            modules.add(module)
        elif kind == "flat_layout":
            flat.add(path)
    if len(modules) != classes["module"]:
        raise ExtractError(f"{commit}: two module paths share a department and a name")
    return classes, modules, flat


def replay(git: Git, log: list[dict]) -> tuple[list[dict], set[str], dict]:
    """Rebuilds the file list at every listed commit: the commit rows, the paths at the pin, the history notes."""
    rows, paths, previous, flat_seen, last_flat = [], set(), set(), set(), None
    for index, entry in enumerate(log):
        commit = entry["commit"]
        path_changes = apply_changes(entry, paths)
        if index == 0 and tree_listing(git, commit) != paths:
            raise ExtractError(f"{commit}: the folder was not empty before the first listed commit")
        classes, modules, flat = census(commit, paths)
        if flat:
            flat_seen |= flat
            last_flat = commit
        rows.append({
            "commit": commit,
            "committer_time_utc": utc(entry["committer"]),
            "author_time_utc": utc(entry["author"]),
            "path_changes": path_changes,
            "files": len(paths),
            "by_class": classes,
            "modules": len(modules),
            "added": sorted(modules - previous),
            "removed": sorted(previous - modules),
        })
        previous = modules
    if tree_listing(git, PINNED_COMMIT) != paths:
        raise ExtractError("the file list replayed from the commit log differs from the tree stored at the pinned commit")
    notes = {
        "flat_layout_paths": sorted(flat_seen),
        "last_commit_with_a_flat_layout_path": last_flat,
        "note": "the flat layout held the English text of the first two modules under names without a language "
                "folder; the count of modules starts at the commit that moved them into <department>/en/",
    }
    return rows, paths, notes


def source_section(git: Git, facts: dict) -> dict:
    return {
        "repository": "GuitarAlchemist/Demerzel",
        "commit": PINNED_COMMIT,
        "history_path": HISTORY_PATH,
        "objects_read": "commits and trees only; no command reads the content of a file",
        "commands": git.commands,
        "commit_check": "the pin resolves to a commit of a non-shallow clone; the number of commits reachable from "
                        "it, the number that touch the folder, the SHA-256 of their ids and the folder's tree id "
                        "at the pin equal the constants embedded in extract.py",
        "replay_check": "the file list rebuilt by replaying the added and deleted paths of the listed commits "
                        "equals the output of git ls-tree at the first listed commit and at the pinned commit",
        **facts,
    }


def definitions_section() -> dict:
    return {
        "commit_list": "ancestors of the pinned commit (itself included) whose tree under history_path differs "
                       "from their parent's, as listed by git log with its default history simplification",
        "date": "committer date (%ct, seconds since the Unix epoch), written here in UTC; the author date (%at) "
                "is recorded next to it and used only to measure how far the two differ",
        "order": "ancestry: every listed commit has one parent and is an ancestor of the next one (all lie on the "
                 "first-parent chain of the pin), so commits that share a committer second keep the order in "
                 "which they were built",
        "module": "a path state/streeling/courses/<department>/en/<name>.md whose file name is not README.md "
                  "(case-insensitive); written as <department>/<name>",
        "by_class": {
            "module": "counted",
            "en_readme": "excluded: <department>/en/README.md, a placeholder page and not a course",
            "translation": "excluded: <department>/<two-letter language other than en>/<name>.md",
            "readme": "excluded: README.md of the folder or of a department",
            "flat_layout": "excluded: any other file directly under state/streeling/courses, the layout used "
                           "before the <department>/<language>/ folders existed (listed under history_notes)",
        },
        "path_changes": "paths under history_path that the commit added, deleted or modified, compared with its "
                        "parent and with rename detection off, so a renamed file is one deleted and one added path",
        "added_removed": "module names present at this commit and not at the previous listed commit, and the reverse",
        "department_records": "files state/streeling/departments/<name>.department.json at the pinned commit, read "
                              "from its tree; the <name>.weights.json files beside them are not records",
    }


def counts_section(rows: list[dict], log: list[dict]) -> dict:
    times = [entry["committer"] for entry in log]
    date_gaps = [abs(entry["committer"] - entry["author"]) for entry in log]
    return {
        "commits": len(rows),
        "first_commit_utc": rows[0]["committer_time_utc"],
        "last_commit_utc": rows[-1]["committer_time_utc"],
        "pairs_of_consecutive_commits_sharing_a_committer_second": sum(
            later == earlier for earlier, later in zip(times, times[1:])),
        "commits_that_change_the_module_count": sum(
            row["modules"] != (rows[i - 1]["modules"] if i else 0) for i, row in enumerate(rows)),
        "module_additions": sum(len(row["added"]) for row in rows),
        "module_removals": sum(len(row["removed"]) for row in rows),
        "modules_at_pin": rows[-1]["modules"],
        "files_at_pin": rows[-1]["files"],
        "files_at_pin_by_class": rows[-1]["by_class"],
        "largest_gap_between_author_and_committer_date_seconds": max(date_gaps),
        "commits_whose_author_and_committer_dates_differ_by_more_than_an_hour": sum(gap > 3600 for gap in date_gaps),
        "commits_whose_author_and_committer_dates_fall_on_different_utc_days": sum(
            entry["committer"] // SECONDS_PER_DAY != entry["author"] // SECONDS_PER_DAY for entry in log),
    }


def pin_state_section(paths: set[str], records: list[str]) -> dict:
    _, modules, _ = census(PINNED_COMMIT, paths)
    departments: dict[str, int] = {}
    for module in modules:
        departments[module.split("/")[0]] = departments.get(module.split("/")[0], 0) + 1
    folders = sorted({path[len(PREFIX):].split("/")[0] for path in paths if "/" in path[len(PREFIX):]})
    return {
        "department_folders": folders,
        "department_folders_count": len(folders),
        "modules_by_department": {name: departments[name] for name in sorted(departments)},
        "departments_with_a_module": len(departments),
        "department_records": len(records),
        "department_records_without_a_course_folder": sorted(set(records) - set(folders)),
        "course_folders_without_a_department_record": sorted(set(folders) - set(records)),
        "excluded_en_readme_paths": sorted(path for path in paths if classify(path)[0] == "en_readme"),
    }


def build(root: Path) -> dict:
    """The snapshot: checks of the clone and of the history, the replay, then one function per section."""
    git = Git(root)
    log, facts = read_history(git, check_clone(git))
    rows, paths, notes = replay(git, log)
    records = department_records(git)
    return {
        "schema_version": "0.1.0",
        "module_id": "psy-010-growth-curves-short-series",
        "kind": "observed",
        "source": source_section(git, facts),
        "definitions": definitions_section(),
        "counts": counts_section(rows, log),
        "history_notes": notes,
        "pin_state": pin_state_section(paths, records),
        "commits": rows,
    }


def main() -> int:
    here = FIXTURE_FILE
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--repo-root", type=Path, default=here.parents[5],
                        help="a clone of the repository with the full commit history (blobs are not needed)")
    parser.add_argument("--output", type=Path, default=here.with_name("observed-input.json"))
    args = parser.parse_args()
    try:
        snapshot = build(args.repo_root.resolve())
    except (ExtractError, OSError, UnicodeDecodeError, ValueError) as exc:
        print(f"extract.py: {exc}", file=sys.stderr)
        return 1
    text = json.dumps(snapshot, ensure_ascii=False, indent=2) + "\n"
    args.output.write_bytes(text.encode("utf-8"))
    counts = snapshot["counts"]
    print(f"extract.py: {counts['commits']} commits from {counts['first_commit_utc']} to {counts['last_commit_utc']}, "
          f"{counts['module_additions']} additions - {counts['module_removals']} removals = "
          f"{counts['modules_at_pin']} English modules at the pin -> {args.output.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
