#!/usr/bin/env python3
"""Universal ecosystem-freshness monitor — one guard for every producer loop.

`state/quality-trend/` died silently for 64 days because a "no news" feeder is
indistinguishable from a dead one (green != alive). scripts/quality_trend.py got
a dedicated per-loop freshness guard; this generalizes that guard to EVERY
scheduled producer workflow so the board turns red for any dead or silent-green
loop — and stays green (and silent) when they are all healthy.

The registry (.github/loop-health.yml, schema schemas/loop-health.schema.json)
declares, per loop, exactly one of:

  * proof            — how the loop proves liveness (committed state, default-
                       branch git history, or the latest completed scheduled
                       GitHub Actions run and its conclusion).
  * disabled         — intentionally paused for a bounded window (`until`).

Event-triggered producers (#844) have no cron and so cannot be expressed in that
registry at all — an `active` entry requires at least one cron expression, and
the schema is closed to new fields. They are declared in EVENT_PRODUCERS below
and judged against their EVENT SUPPLY rather than a clock: a `pull_request` loop
is only expected to have run when a pull request actually happened. See
_eval_event_producer for the semantics and their stated limit.

Findings and exit codes (a producer with a real problem must fail CI):

  0  every active loop is healthy, newborn (added too recently to have been
     able to produce evidence yet), or bounded-disabled and verified.
  1  at least one: stale, silent_green, unregistered, malformed_proof,
     expired_disable, failed_run, activation_mismatch.
  2  configuration or evidence-adapter failure (registry unreadable / invalid /
     internally inconsistent; a proof adapter's machinery — e.g. git — failed).

This monitor is a MONITOR, not a producer: it lists itself (and the other
freshness guards) under `monitors:` so it never flags itself for coverage.

Deterministic: findings are sorted by workflow name; the committable alert
payload carries only stable fields (no ages/timestamps) so a steady red state
does not churn commits.

stdlib + PyYAML + jsonschema only. No wall-clock is read when --now is given.
"""
from __future__ import annotations

import argparse
import glob as globmod
import json
import os
import sys
from datetime import date, datetime, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import quote, urlencode
from urllib.request import Request, urlopen

import yaml

REPO = Path(__file__).resolve().parent.parent
DEFAULT_REGISTRY = ".github/loop-health.yml"
DEFAULT_WORKFLOWS_DIR = ".github/workflows"
DEFAULT_SCHEMA = "schemas/loop-health.schema.json"
DEFAULT_BRANCH = "master"
ALLOWED_MONITORS = {
    "ecosystem-freshness.yml",
    "demerzel-quality-trend-freshness.yml",
}

# Event-triggered producers (#844). `cross-model-review.yml` is `on:
# pull_request`; it has no cron, so scheduled_workflows() never enumerates it
# and nothing noticed when it stopped producing for a week.
#
# These live in code rather than in .github/loop-health.yml for the same reason
# ALLOWED_MONITORS does: the registry schema is closed (an `active` loop REQUIRES
# >= 1 cron expression, and additionalProperties is false), so an event-triggered
# loop is not expressible there today, and a hardcoded list cannot be extended by
# a producer editing its own workflow file.
#
# `event` is the `on:` key that dispatches the loop; membership is verified
# against the live workflow YAML. `max_stale_days` is BOTH the response
# tolerance and the width of the event-supply window (see _eval_event_producer).
# Only 'pull_request' is supported — the one event this repo actually has a
# producer for. Adding a second event means teaching the supply adapter how to
# date it, which is deliberately not speculated on here.
EVENT_PRODUCERS: dict[str, dict] = {
    "cross-model-review.yml": {"event": "pull_request", "max_stale_days": 3},
}

for _stream in (sys.stdout, sys.stderr):  # Windows consoles default to cp1252.
    if hasattr(_stream, "reconfigure"):
        _stream.reconfigure(encoding="utf-8")

# Finding kinds grouped by the exit code they contribute.
_EXIT2_KINDS = ("config_error", "adapter_error")
_EXIT1_KINDS = (
    "stale",
    "silent_green",
    "unregistered",
    "malformed_proof",
    "expired_disable",
    "failed_run",
    "activation_mismatch",
)
# Everything else (healthy, newborn, disabled) is exit 0.


class ConfigError(Exception):
    """Registry unreadable/invalid/inconsistent — maps to exit 2."""


class AdapterError(Exception):
    """A proof adapter's underlying machinery (e.g. git) failed — exit 2."""


# ---------------------------------------------------------------------------
# git seam (injectable so tests can force API failure / assert the branch ref)
# ---------------------------------------------------------------------------

def default_git_runner(args: list[str], cwd: Path) -> str:
    """Run `git <args>` in cwd, returning stdout. Raises AdapterError on failure."""
    import subprocess

    proc = subprocess.run(
        ["git", *args],
        cwd=str(cwd),
        capture_output=True,
        text=True,
    )
    if proc.returncode != 0:
        raise AdapterError(
            f"git {' '.join(args)} failed ({proc.returncode}): "
            f"{proc.stderr.strip() or proc.stdout.strip()}"
        )
    return proc.stdout


def default_actions_runner(
    workflow: str,
    repository: str,
    default_branch: str,
    token: str,
) -> dict | None:
    """Return the latest completed scheduled run for a workflow.

    The seam is injectable in tests. The production request is read-only and
    authenticates only with the workflow's existing GITHUB_TOKEN.
    """
    if not repository or "/" not in repository:
        raise AdapterError(
            "workflow_run proof requires GITHUB_REPOSITORY (owner/repo)"
        )
    if not token:
        raise AdapterError("workflow_run proof requires the existing GITHUB_TOKEN")
    params = urlencode({
        "event": "schedule",
        "branch": default_branch,
        "status": "completed",
        "per_page": 1,
    })
    endpoint = (
        "https://api.github.com/repos/"
        f"{quote(repository, safe='/')}/actions/workflows/"
        f"{quote(workflow, safe='')}/runs?{params}"
    )
    request = Request(endpoint, headers={
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {token}",
        "X-GitHub-Api-Version": "2022-11-28",
        "User-Agent": "demerzel-ecosystem-freshness",
    })
    try:
        with urlopen(request, timeout=20) as response:
            payload = json.load(response)
    except HTTPError as exc:
        raise AdapterError(
            f"GitHub Actions API returned HTTP {exc.code} for {workflow}"
        ) from exc
    except (URLError, TimeoutError, json.JSONDecodeError) as exc:
        raise AdapterError(
            f"GitHub Actions API failed for {workflow}: {type(exc).__name__}"
        ) from exc
    runs = payload.get("workflow_runs") if isinstance(payload, dict) else None
    if not isinstance(runs, list):
        raise AdapterError(
            f"GitHub Actions API returned malformed run data for {workflow}"
        )
    return runs[0] if runs else None


def _github_get(endpoint: str, token: str, what: str):
    """Read-only authenticated GET against the GitHub API. Raises AdapterError."""
    request = Request(endpoint, headers={
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {token}",
        "X-GitHub-Api-Version": "2022-11-28",
        "User-Agent": "demerzel-ecosystem-freshness",
    })
    try:
        with urlopen(request, timeout=20) as response:
            return json.load(response)
    except HTTPError as exc:
        raise AdapterError(
            f"GitHub API returned HTTP {exc.code} for {what}"
        ) from exc
    except (URLError, TimeoutError, json.JSONDecodeError) as exc:
        raise AdapterError(
            f"GitHub API failed for {what}: {type(exc).__name__}"
        ) from exc


def default_event_supply_runner(
    workflow: str,
    event: str,
    repository: str,
    token: str,
) -> tuple[str | None, dict | None]:
    """Return (newest triggering event ISO timestamp, latest completed run).

    Two reads, one seam, so tests inject a single stub:

      * event supply — the newest pull request CREATED on the repo. `created_at`
        is used, not `updated_at`: the `opened` activity type dispatches
        unconditionally, so a PR created inside the window is *proof* that a run
        was due. `updated_at` also bumps on comments and label edits, which are
        not triggers, and would demand runs that were never owed (a guard that
        cries wolf is worse than none). The cost is that a window containing
        only `synchronize` pushes reads as quiet — under-claiming, not
        over-claiming.
      * latest completed run of `workflow` for that event, on ANY branch. There
        is deliberately no branch filter: a `pull_request` run is attributed to
        the PR's head branch, so filtering on the default branch would find
        nothing and every healthy loop would read as dead.
    """
    if not repository or "/" not in repository:
        raise AdapterError(
            "event-supply proof requires GITHUB_REPOSITORY (owner/repo)"
        )
    if not token:
        raise AdapterError("event-supply proof requires the existing GITHUB_TOKEN")
    if event != "pull_request":
        raise AdapterError(f"no event-supply adapter for event {event!r}")

    repo_path = quote(repository, safe="/")
    pulls = _github_get(
        f"https://api.github.com/repos/{repo_path}/pulls?"
        + urlencode({
            "state": "all",
            "sort": "created",
            "direction": "desc",
            "per_page": 1,
        }),
        token,
        f"{event} supply on {repository}",
    )
    if not isinstance(pulls, list):
        raise AdapterError(f"GitHub API returned malformed pull data for {repository}")
    newest_event = None
    if pulls and isinstance(pulls[0], dict):
        newest_event = pulls[0].get("created_at")

    payload = _github_get(
        f"https://api.github.com/repos/{repo_path}/actions/workflows/"
        f"{quote(workflow, safe='')}/runs?"
        + urlencode({"event": event, "status": "completed", "per_page": 1}),
        token,
        f"{workflow} runs",
    )
    runs = payload.get("workflow_runs") if isinstance(payload, dict) else None
    if not isinstance(runs, list):
        raise AdapterError(
            f"GitHub Actions API returned malformed run data for {workflow}"
        )
    return newest_event, (runs[0] if runs else None)


# ---------------------------------------------------------------------------
# time helpers
# ---------------------------------------------------------------------------

def _parse_iso(value: str | None) -> datetime | None:
    if not value:
        return None
    try:
        dt = datetime.fromisoformat(value.strip().replace("Z", "+00:00"))
    except (ValueError, AttributeError):
        return None
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt


def _age_days(newest: datetime, now: datetime) -> float:
    return (now - newest).total_seconds() / 86400.0


# ---------------------------------------------------------------------------
# workflow enumeration (which scheduled producers exist on disk)
# ---------------------------------------------------------------------------

def _on_block(doc: dict):
    """`on:` parses to the YAML 1.1 boolean True under PyYAML, so look under both."""
    if not isinstance(doc, dict):
        return None
    on = doc.get("on")
    if on is None:
        on = doc.get(True)
    return on


def _schedule_block(doc: dict):
    on = _on_block(doc)
    if isinstance(on, dict):
        return on.get("schedule")
    return None


def scheduled_workflows(workflows_dir: Path) -> list[str]:
    """Bare filenames of every workflow that has at least one cron schedule."""
    found: list[str] = []
    for path in sorted(workflows_dir.glob("*.yml")) + sorted(
        workflows_dir.glob("*.yaml")
    ):
        try:
            doc = yaml.safe_load(path.read_text(encoding="utf-8"))
        except yaml.YAMLError:
            continue
        sched = _schedule_block(doc)
        if isinstance(sched, list) and any(
            isinstance(e, dict) and e.get("cron") for e in sched
        ):
            found.append(path.name)
    return sorted(found)


def workflow_crons(workflows_dir: Path, workflow: str) -> list[str] | None:
    """Return configured cron expressions, or None when the file is absent."""
    path = workflows_dir / workflow
    if not path.exists():
        return None
    try:
        doc = yaml.safe_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        raise ConfigError(f"{workflow}: workflow YAML is invalid: {exc}") from exc
    sched = _schedule_block(doc)
    if not isinstance(sched, list):
        return []
    return sorted(
        entry["cron"]
        for entry in sched
        if isinstance(entry, dict) and isinstance(entry.get("cron"), str)
    )


def workflow_events(workflows_dir: Path, workflow: str) -> set[str] | None:
    """Trigger names under `on:`, or None when the workflow file is absent.

    Handles all three YAML shapes GitHub accepts: mapping (`on: {pull_request:
    ...}`), sequence (`on: [push, pull_request]`), and scalar (`on: push`).
    """
    path = workflows_dir / workflow
    if not path.exists():
        return None
    try:
        doc = yaml.safe_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        raise ConfigError(f"{workflow}: workflow YAML is invalid: {exc}") from exc
    on = _on_block(doc)
    if isinstance(on, dict):
        return {str(k) for k in on}
    if isinstance(on, list):
        return {str(k) for k in on}
    if isinstance(on, str):
        return {on}
    return set()


def workflow_added_at(
    workflow: str,
    workflows_dir: Path,
    repo_root: Path,
    default_branch: str,
    git_runner,
) -> datetime | None:
    """When the workflow file was last ADDED to the default branch, or None.

    Returns None whenever birth cannot be *proven* — git unavailable, the
    workflows dir sits outside the repo, or the file has never been committed
    to the default branch. Callers must not suppress anything on None: an
    unprovable birth date is not evidence of youth.

    The newest add-commit wins, not the oldest. A workflow that was deleted and
    re-added (or renamed — git records a rename as an add at the new path, and
    GitHub Actions likewise starts its run history over) is a new producer with
    a new run history, so its clock restarts at the latest addition.
    """
    try:
        rel = os.path.relpath(workflows_dir / workflow, repo_root)
    except ValueError:  # different drives on Windows
        return None
    rel = rel.replace(os.sep, "/")
    if rel.startswith("../"):
        return None
    try:
        out = git_runner(
            ["log", "--diff-filter=A", "--format=%cI", default_branch, "--", rel],
            repo_root,
        )
    except AdapterError:
        return None
    for line in out.splitlines():
        line = line.strip()
        if line:
            return _parse_iso(line)
    return None


# ---------------------------------------------------------------------------
# proof adapters
# ---------------------------------------------------------------------------

def _iter_timestamps(path: Path, field: str):
    """Yield ISO timestamp strings from a committed JSON or JSONL state file.

    Raises ConfigError-free; a genuinely unparseable file yields the sentinel
    ('__malformed__',) so the caller can distinguish "bad evidence" from "no
    timestamp field".
    """
    text = path.read_text(encoding="utf-8")
    stripped = text.strip()
    if not stripped:
        return
    # Try whole-file JSON first (object or array); fall back to JSONL.
    try:
        doc = json.loads(stripped)
    except json.JSONDecodeError:
        malformed = True
        for line in text.splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError:
                continue
            malformed = False
            if isinstance(row, dict) and row.get(field):
                yield row[field]
        if malformed:
            yield "__malformed__"
        return
    records = doc if isinstance(doc, list) else [doc]
    for row in records:
        if isinstance(row, dict) and row.get(field):
            yield row[field]


def _eval_state_glob(proof: dict, now: datetime, repo_root: Path) -> tuple[str, str]:
    glob_pat = proof.get("glob")
    field = proof.get("timestamp_field")
    if not glob_pat or not field:
        raise ConfigError("state_glob proof requires 'glob' and 'timestamp_field'")
    max_days = float(proof["max_stale_days"])

    matches = sorted(
        globmod.glob(str(repo_root / glob_pat), recursive=True)
    )
    if not matches:
        return ("silent_green", "no committed evidence matches "
                f"`{glob_pat}` (loop cannot prove it is alive)")

    newest: datetime | None = None
    saw_malformed = False
    for m in matches:
        for raw in _iter_timestamps(Path(m), field):
            if raw == "__malformed__":
                saw_malformed = True
                continue
            dt = _parse_iso(raw)
            if dt and (newest is None or dt > newest):
                newest = dt

    if newest is None:
        if saw_malformed:
            return ("malformed_proof", f"`{glob_pat}` matched files that are not "
                    "parseable JSON/JSONL")
        return ("malformed_proof", f"`{glob_pat}` matched files but none carry a "
                f"parseable `{field}` timestamp")

    age = _age_days(newest, now)
    if age > max_days:
        return ("stale", f"newest `{glob_pat}` evidence is {age:.1f}d old "
                f"(threshold {max_days:g}d)")
    return ("healthy", f"fresh: newest evidence {age:.1f}d old "
            f"(threshold {max_days:g}d)")


def _eval_git_log(
    proof: dict,
    now: datetime,
    repo_root: Path,
    default_branch: str,
    git_runner,
) -> tuple[str, str]:
    path = proof.get("path")
    if not path:
        raise ConfigError("git_log proof requires 'path'")
    max_days = float(proof["max_stale_days"])

    # Default-branch evidence: judge freshness from the default branch's history,
    # not the working tree, so running on any branch reflects production reality.
    out = git_runner(
        ["log", "-1", "--format=%cI", default_branch, "--", path], repo_root
    )
    iso = out.strip()
    if not iso:
        return ("silent_green", f"no commit on `{default_branch}` has ever "
                f"touched `{path}` (loop cannot prove it is alive)")
    newest = _parse_iso(iso)
    if newest is None:
        raise AdapterError(f"git returned an unparseable commit date: {iso!r}")
    age = _age_days(newest, now)
    if age > max_days:
        return ("stale", f"last commit touching `{path}` on `{default_branch}` "
                f"is {age:.1f}d old (threshold {max_days:g}d)")
    return ("healthy", f"fresh: last commit {age:.1f}d old "
            f"(threshold {max_days:g}d)")


def _eval_workflow_run(
    proof: dict,
    workflow: str,
    now: datetime,
    repository: str,
    default_branch: str,
    token: str,
    actions_runner,
) -> tuple[str, str]:
    """Prove a scheduled loop through its latest completed Actions run."""
    max_days = float(proof["max_stale_days"])
    run = actions_runner(workflow, repository, default_branch, token)
    if run is None:
        return (
            "silent_green",
            "no completed scheduled GitHub Actions run exists on the default branch",
        )
    if not isinstance(run, dict):
        raise AdapterError(f"workflow-run adapter returned invalid data for {workflow}")
    conclusion = run.get("conclusion")
    url = run.get("html_url") or "(no run URL)"
    if conclusion != "success":
        return (
            "failed_run",
            f"latest completed scheduled run concluded {conclusion!r}: {url}",
        )
    newest = _parse_iso(run.get("run_started_at") or run.get("created_at"))
    if newest is None:
        return (
            "malformed_proof",
            "latest completed scheduled run has no parseable start timestamp",
        )
    age = _age_days(newest, now)
    if age > max_days:
        return (
            "stale",
            f"latest successful scheduled run is {age:.1f}d old "
            f"(threshold {max_days:g}d): {url}",
        )
    return (
        "healthy",
        f"latest scheduled run succeeded {age:.1f}d ago "
        f"(threshold {max_days:g}d): {url}",
    )


def _eval_event_producer(
    workflow: str,
    spec: dict,
    now: datetime,
    repo_root: Path,
    workflows_dir: Path,
    default_branch: str,
    git_runner,
    event_supply_runner,
    repository: str,
    token: str,
) -> tuple[str, str]:
    """Prove an event-triggered loop against its EVENT SUPPLY, not a clock.

    An event-triggered loop has no cadence, so "overdue" is undefined in the
    abstract — inventing a pseudo-cron for it would be a fabricated oracle. The
    honest observable is conditional:

        a `pull_request` loop is expected to have run only when a pull request
        actually happened.

    So `max_stale_days` does double duty as the width of the supply window and
    the response tolerance:

      * newest triggering event older than the window  -> QUIET. Nothing was
        owed, so the guard says nothing. This is the "quiet but healthy" arm; a
        repo with no PRs this week must not turn the board red.
      * event inside the window, no completed run ever -> silent_green (red),
        subject to the same newborn grace as #850.
      * event inside the window, newest completed run older than the window
        -> stale (red). This is the #844 shape: events kept arriving, the loop
        stopped answering, and nothing enumerated it.
      * newest completed run did not conclude 'success' -> failed_run (red),
        matching _eval_workflow_run. For a PR loop this self-clears on the next
        PR, so a one-off flake fades while a persistently broken loop stays red.

    LIMIT, stated plainly: this proves the loop was DISPATCHED and did not fail,
    not that its output was VALID. The specific #844 incident (runs green,
    review body a placeholder) is only caught here via the run conclusion, which
    exists because #840 made that failure loud. Asserting the artifact itself
    needs per-workflow proof declarations in the registry — see the report.
    """
    event = spec["event"]
    max_days = float(spec["max_stale_days"])

    actual_events = workflow_events(workflows_dir, workflow)
    if actual_events is None:
        return ("activation_mismatch",
                "declared event-triggered producer workflow is missing")
    if event not in actual_events:
        return ("activation_mismatch",
                f"declared as an `{event}` producer but the workflow's `on:` "
                f"triggers are {sorted(actual_events)}")

    newest_event_iso, run = event_supply_runner(workflow, event, repository, token)
    newest_event = _parse_iso(newest_event_iso)
    if newest_event is None or _age_days(newest_event, now) > max_days:
        return ("healthy",
                f"quiet: no `{event}` event within the last {max_days:g}d, so no "
                "run was owed (event-triggered loops are judged by event supply, "
                "not by a clock)")
    event_age = _age_days(newest_event, now)

    if run is None:
        kind, detail = ("silent_green",
                        f"a `{event}` event arrived {event_age:.1f}d ago but the "
                        "workflow has no completed run at all")
        return _apply_newborn_grace(
            kind, detail, workflow, max_days, now, repo_root, workflows_dir,
            default_branch, git_runner,
        )
    if not isinstance(run, dict):
        raise AdapterError(f"event-supply adapter returned invalid run data for {workflow}")

    conclusion = run.get("conclusion")
    url = run.get("html_url") or "(no run URL)"
    if conclusion != "success":
        return ("failed_run",
                f"newest completed `{event}` run concluded {conclusion!r}: {url}")

    newest_run = _parse_iso(run.get("run_started_at") or run.get("created_at"))
    if newest_run is None:
        return ("malformed_proof",
                f"newest completed `{event}` run has no parseable start timestamp")
    run_age = _age_days(newest_run, now)
    if run_age > max_days:
        return ("stale",
                f"a `{event}` event arrived {event_age:.1f}d ago but the newest "
                f"completed run is {run_age:.1f}d old (threshold {max_days:g}d): "
                f"{url}")
    return ("healthy",
            f"answering `{event}` supply: newest event {event_age:.1f}d ago, "
            f"newest successful run {run_age:.1f}d ago (threshold {max_days:g}d): "
            f"{url}")


# ---------------------------------------------------------------------------
# per-loop evaluation
# ---------------------------------------------------------------------------

def _apply_newborn_grace(
    kind: str,
    detail: str,
    workflow: str,
    grace_days: float,
    now: datetime,
    repo_root: Path,
    workflows_dir: Path,
    default_branch: str,
    git_runner,
) -> tuple[str, str]:
    """Withhold a no-evidence-ever finding while the loop is still newborn (#850).

    "No evidence ever" is ambiguous: a daily loop with nothing after three days
    is dead, but a monthly loop added eleven days ago has simply not reached its
    first scheduled opportunity — and an event-triggered loop added yesterday
    cannot have answered a pull request opened the day before it existed.
    Alarming on the newborn is a false positive, and a guard that cries wolf is
    one people stop reading, which is exactly how a real dead loop hides.

    The grace window is the loop's OWN max_stale_days, measured from the
    default-branch add-commit. Reasons for that exact boundary:
      * It is already cadence-scaled (35d monthly, 1d for a */15 loop), so no
        cron arithmetic and no second dial to keep in sync with the first.
      * It is the tolerance the loop's author already declared as "longer than
        this without output means dead". A newborn cannot be judged by a softer
        standard than a running loop without inventing a weaker one.
      * It is therefore not over-broad: a missed FIRST run surfaces exactly as
        late as a missed subsequent run already does, no later.
    Silence past that window is proof of death and still turns the board red.
    """
    added = workflow_added_at(
        workflow, workflows_dir, repo_root, default_branch, git_runner
    )
    if added is None:
        return kind, detail
    age = _age_days(added, now)
    if age > grace_days:
        return kind, detail
    return (
        "newborn",
        f"added to `{default_branch}` {age:.1f}d ago and has not yet had a "
        f"full {grace_days:g}d window to produce evidence — "
        f"withheld until then, after which silence is red. Original finding: "
        f"{detail}",
    )

def _evaluate_loop(
    loop: dict,
    now: datetime,
    repo_root: Path,
    workflows_dir: Path,
    default_branch: str,
    git_runner,
    actions_runner,
    repository: str,
    token: str,
    actual_crons: list[str] | None,
) -> tuple[str, str]:
    wf = loop.get("workflow", "<unknown>")
    status = loop.get("status")
    declarations = [
        k for k in ("proof", "disabled")
        if (loop.get(k) is True or isinstance(loop.get(k), dict))
    ]
    if len(declarations) != 1:
        raise ConfigError(
            f"{wf}: must declare exactly one of proof/disabled, "
            f"found {declarations or 'none'}"
        )
    declared = declarations[0]

    if declared == "disabled":
        if status != "disabled":
            raise ConfigError(f"{wf}: has a disabled block but status is {status!r}")
        if actual_crons is None:
            return ("activation_mismatch", "disabled workflow file is missing")
        verification = loop["disabled"].get("verification")
        if verification != "schedule_absent":
            raise ConfigError(
                f"{wf}: disabled.verification must be 'schedule_absent'"
            )
        if actual_crons:
            return (
                "activation_mismatch",
                "registry says disabled but workflow still has cron schedule(s): "
                + ", ".join(actual_crons),
            )
        until_raw = loop["disabled"].get("until")
        try:
            until = date.fromisoformat(until_raw)
        except (TypeError, ValueError):
            raise ConfigError(f"{wf}: disabled.until is not a valid date: {until_raw!r}")
        if now.date() > until:
            return ("expired_disable", f"intentional disable expired on {until} "
                    "(re-evaluate or re-authorize the pause)")
        return ("disabled", f"intentionally disabled through {until}: "
                f"{loop['disabled'].get('reason', '')}".rstrip(": "))

    if status != "active":
        raise ConfigError(
            f"{wf}: status must be 'active' for a {declared} loop, got {status!r}"
        )

    if actual_crons is None:
        return ("activation_mismatch", "active workflow file is missing")
    expected_crons = sorted(loop.get("schedule") or [])
    if not actual_crons:
        return (
            "activation_mismatch",
            "registry says active but workflow has no cron schedule",
        )
    if expected_crons != actual_crons:
        return (
            "activation_mismatch",
            f"registry crons {expected_crons!r} do not match workflow crons "
            f"{actual_crons!r}",
        )

    # proof
    proof = loop["proof"]
    adapter = proof.get("adapter")
    if adapter == "state_glob":
        kind, detail = _eval_state_glob(proof, now, repo_root)
    elif adapter == "git_log":
        kind, detail = _eval_git_log(
            proof, now, repo_root, default_branch, git_runner
        )
    elif adapter == "workflow_run":
        kind, detail = _eval_workflow_run(
            proof,
            wf,
            now,
            repository,
            default_branch,
            token,
            actions_runner,
        )
    else:
        raise ConfigError(f"{wf}: unknown proof adapter {adapter!r}")

    if kind != "silent_green":
        return kind, detail

    # Newborn grace (#850) — rationale lives on _apply_newborn_grace.
    return _apply_newborn_grace(
        kind, detail, wf, float(proof["max_stale_days"]), now, repo_root,
        workflows_dir, default_branch, git_runner,
    )


# ---------------------------------------------------------------------------
# top-level evaluation
# ---------------------------------------------------------------------------

def evaluate(
    registry: dict,
    *,
    now: datetime,
    workflows_dir: Path,
    repo_root: Path,
    git_runner=default_git_runner,
    actions_runner=default_actions_runner,
    event_supply_runner=default_event_supply_runner,
    event_producers: dict | None = None,
    repository: str = "",
    token: str = "",
) -> list[dict]:
    """Return findings (one per producer/loop), sorted by workflow name.

    Never reads wall-clock (caller supplies `now`). Adapter/config failures are
    turned into config_error/adapter_error findings rather than exceptions, so a
    single bad entry still yields a complete, deterministic report.
    """
    monitors = set(registry.get("monitors") or [])
    default_branch = registry.get("default_branch") or DEFAULT_BRANCH
    loops = registry.get("loops") or []
    if event_producers is None:
        event_producers = EVENT_PRODUCERS

    registered: dict[str, dict] = {}
    findings: list[dict] = []
    for wf in sorted(monitors):
        if wf not in ALLOWED_MONITORS:
            findings.append({
                "workflow": wf,
                "kind": "config_error",
                "detail": "workflow is not an approved freshness monitor and "
                          "cannot be excluded from producer coverage",
            })
            continue
        try:
            crons = workflow_crons(workflows_dir, wf)
        except ConfigError as exc:
            findings.append({
                "workflow": wf,
                "kind": "config_error",
                "detail": str(exc),
            })
            continue
        if not crons:
            findings.append({
                "workflow": wf,
                "kind": "activation_mismatch",
                "detail": "registered monitor is missing or has no cron schedule",
            })
    for loop in loops:
        wf = loop.get("workflow", "<unknown>")
        if wf in monitors:
            findings.append({
                "workflow": wf,
                "kind": "config_error",
                "detail": "workflow cannot be both a monitor and a producer",
            })
            continue
        if wf in registered:
            findings.append({
                "workflow": wf,
                "kind": "config_error",
                "detail": "duplicate registry entry",
            })
            continue
        registered[wf] = loop
        try:
            crons = workflow_crons(workflows_dir, wf)
            kind, detail = _evaluate_loop(
                loop,
                now,
                repo_root,
                workflows_dir,
                default_branch,
                git_runner,
                actions_runner,
                repository,
                token,
                crons,
            )
        except AdapterError as exc:
            kind, detail = "adapter_error", str(exc)
        except ConfigError as exc:
            kind, detail = "config_error", str(exc)
        findings.append({"workflow": wf, "kind": kind, "detail": detail})

    # Event-triggered producers (#844): no cron, so scheduled_workflows() below
    # cannot see them and the registry cannot express them. Evaluated from the
    # in-code declaration against live event supply.
    for wf in sorted(event_producers):
        if wf in monitors or wf in registered:
            findings.append({
                "workflow": wf,
                "kind": "config_error",
                "detail": "workflow is declared as an event-triggered producer "
                          "and also registered as a monitor or scheduled loop",
            })
            continue
        try:
            kind, detail = _eval_event_producer(
                wf,
                event_producers[wf],
                now,
                repo_root,
                workflows_dir,
                default_branch,
                git_runner,
                event_supply_runner,
                repository,
                token,
            )
        except AdapterError as exc:
            kind, detail = "adapter_error", str(exc)
        except ConfigError as exc:
            kind, detail = "config_error", str(exc)
        findings.append({"workflow": wf, "kind": kind, "detail": detail})

    # Coverage: every scheduled producer (not a monitor) must be registered.
    for wf in scheduled_workflows(workflows_dir):
        if wf in monitors or wf in registered:
            continue
        findings.append({
            "workflow": wf,
            "kind": "unregistered",
            "detail": "scheduled producer workflow is not in the loop-health "
                      "registry (add a proof or bounded disabled entry)",
        })

    findings.sort(key=lambda f: (f["workflow"], f["kind"]))
    return findings


def exit_code(findings: list[dict]) -> int:
    kinds = {f["kind"] for f in findings}
    if kinds & set(_EXIT2_KINDS):
        return 2
    if kinds & set(_EXIT1_KINDS):
        return 1
    return 0


def stable_alert(findings: list[dict]) -> list[dict]:
    """Committable payload: only the problem findings, stripped of the volatile
    ages/timestamps in `detail`, so a steady red state does not churn commits."""
    problems = [
        {"workflow": f["workflow"], "kind": f["kind"]}
        for f in findings
        if f["kind"] in _EXIT1_KINDS or f["kind"] in _EXIT2_KINDS
    ]
    problems.sort(key=lambda f: (f["workflow"], f["kind"]))
    return problems


def sync_alert(alert_path: Path, findings: list[dict]) -> None:
    """Persist stable red state, or remove it after verified recovery."""
    problems = stable_alert(findings)
    if problems:
        alert_path.parent.mkdir(parents=True, exist_ok=True)
        payload = {"alert": "ecosystem-freshness", "problems": problems}
        alert_path.write_text(
            json.dumps(payload, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
    elif alert_path.exists():
        alert_path.unlink()


# ---------------------------------------------------------------------------
# registry loading + schema validation
# ---------------------------------------------------------------------------

def load_registry(registry_path: Path, schema_path: Path) -> dict:
    if not registry_path.exists():
        raise ConfigError(f"registry not found: {registry_path}")
    try:
        registry = yaml.safe_load(registry_path.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        raise ConfigError(f"registry is not valid YAML: {exc}")
    if not isinstance(registry, dict):
        raise ConfigError("registry must be a mapping")

    if schema_path.exists():
        try:
            import jsonschema
        except ImportError:  # pragma: no cover - jsonschema is a declared dep
            raise ConfigError("jsonschema is required to validate the registry")
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        errors = sorted(
            jsonschema.Draft7Validator(schema).iter_errors(registry), key=str
        )
        if errors:
            loc = "/".join(str(x) for x in errors[0].path) or "(root)"
            raise ConfigError(
                f"registry fails schema at [{loc}]: {errors[0].message}"
            )
    return registry


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def _render_summary(findings: list[dict], code: int) -> str:
    lines = []
    problems = [f for f in findings if f["kind"] in _EXIT1_KINDS + _EXIT2_KINDS]
    if code == 0:
        lines.append(
            f"ecosystem-freshness: OK — {len(findings)} loops healthy or "
            "bounded-disabled"
        )
    else:
        lines.append(f"### 🔴 ecosystem-freshness: {len(problems)} problem loop(s)")
        for f in problems:
            lines.append(f"- **{f['workflow']}** — {f['kind']}: {f['detail']}")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--repo-root", default=str(REPO))
    ap.add_argument("--registry", default=None,
                    help=f"registry path (default <repo>/{DEFAULT_REGISTRY})")
    ap.add_argument("--schema", default=None,
                    help=f"schema path (default <repo>/{DEFAULT_SCHEMA})")
    ap.add_argument("--workflows-dir", default=None,
                    help=f"workflows dir (default <repo>/{DEFAULT_WORKFLOWS_DIR})")
    ap.add_argument("--default-branch", default=None,
                    help="override the registry's default_branch (git_log evidence)")
    ap.add_argument("--now", default=None,
                    help="ISO-8601 override for the evaluation instant (testing)")
    ap.add_argument("--json", action="store_true",
                    help="print the full findings report as JSON to stdout")
    ap.add_argument("--alert-file", default=None,
                    help="write the stable problem payload here on failure, "
                         "remove it on success (for commit-on-change guards)")
    args = ap.parse_args(argv)

    repo_root = Path(args.repo_root).resolve()
    registry_path = Path(args.registry) if args.registry else repo_root / DEFAULT_REGISTRY
    schema_path = Path(args.schema) if args.schema else repo_root / DEFAULT_SCHEMA
    workflows_dir = (
        Path(args.workflows_dir) if args.workflows_dir
        else repo_root / DEFAULT_WORKFLOWS_DIR
    )
    now = _parse_iso(args.now) or datetime.now(timezone.utc)

    try:
        registry = load_registry(registry_path, schema_path)
        if args.default_branch:
            registry = {**registry, "default_branch": args.default_branch}
        findings = evaluate(
            registry,
            now=now,
            workflows_dir=workflows_dir,
            repo_root=repo_root,
            repository=os.environ.get("GITHUB_REPOSITORY", ""),
            token=os.environ.get("GITHUB_TOKEN", ""),
        )
    except ConfigError as exc:
        print(f"ecosystem-freshness: CONFIG ERROR — {exc}", file=sys.stderr)
        return 2

    code = exit_code(findings)

    if args.json:
        print(json.dumps({"exit_code": code, "findings": findings}, indent=2))

    summary = _render_summary(findings, code)
    print(summary, file=sys.stderr)
    step_summary = os.environ.get("GITHUB_STEP_SUMMARY")
    if step_summary:
        with open(step_summary, "a", encoding="utf-8") as fh:
            fh.write(summary + "\n")

    if args.alert_file:
        sync_alert(Path(args.alert_file), findings)

    return code


if __name__ == "__main__":
    raise SystemExit(main())
