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
is only expected to have run when a pull request actually happened. Supply is
bounded below by a declared per-event ACTIVATION CUTOFF, because changing a
workflow's trigger does not replay the events that predate it, and closing a pull
request does not discharge an obligation its head never had a run for. See
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
from datetime import date, datetime, timedelta, timezone
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
# `event` and `activities` describe the exact `on:` dispatch surface; both are
# verified against live workflow YAML. `max_stale_days` is the response
# tolerance for an observed but uncorrelated obligation (see _eval_event_producer).
# The secured workflow from #935 uses `pull_request_target`; the legacy branch
# uses `pull_request`. Exactly one must be active, and both share the same PR/head
# supply adapter.
#
# `activation` is the ACTIVATION CUTOFF per event: the instant from which this
# monitor may infer an obligation for that event. It exists because changing a
# workflow's trigger does not synthesize `opened`/`synchronize` events for heads
# that already exist — a head pushed before `pull_request_target` was ever
# configured cannot have a `pull_request_target` run, and demanding one invents a
# retroactive obligation the producer never owed. It is deliberately NOT derived
# from the workflow file's creation (or last-modified) date: a file's git history
# says when text changed, not when GitHub began dispatching that event, and
# committer dates are author-controlled anyway.
#
# The source of truth is the activation decision itself, recorded here by the
# human who activates enforcement, and every PR head observed before it is
# explicitly waived as pre-cutover. It doubles as the relevant-history boundary
# for retrieval, so the supply adapter never walks the whole PR archive.
#
#   pull_request         2026-08-03T00:00:00Z — the instant per-head obligation
#     enforcement is activated. #844's event-supply binding has never run on the
#     default branch (its commit is part of this change), so no head observed
#     before activation has a recorded obligation and none may be inferred.
#
#   pull_request_target  None — GuitarAlchemist/Demerzel PR #935 performs the
#     trigger migration and has not merged, so the cutover instant does not exist
#     yet. `None` is not a hole: _eval_event_producer raises ConfigError (exit 2)
#     if this event is ever the ACTIVE one without a cutoff, so the board goes red
#     rather than fabricating obligations for pre-cutover heads. Whoever merges
#     #935 replaces this None with that merge commit's instant on the default
#     branch, in the same change that flips the trigger.
EVENT_PRODUCERS: dict[str, dict] = {
    "cross-model-review.yml": {
        "events": ["pull_request", "pull_request_target"],
        "activities": ["opened", "synchronize"],
        "max_stale_days": 3,
        "activation": {
            "pull_request": "2026-08-03T00:00:00Z",
            "pull_request_target": None,
        },
    },
}

# Hard pagination ceilings for the event-supply adapter. Retrieval that has not
# reached the activation cutoff within this many pages is INCOMPLETE, and
# incomplete retrieval must never be read as "no run exists" — it raises
# AdapterError (exit 2) instead. 100 items/page.
_MAX_SUPPLY_PAGES = 20

# Hard REQUEST ceiling for one event-supply evaluation (#963). The activation
# cutoff is immutable, so the set of pull requests "updated since the cutoff"
# only ever grows, and the adapter spends roughly two requests per pull request
# in it. Measured read-only against GuitarAlchemist/Demerzel on the activation
# day: 11 obligations, 22 requests, ~11s. At the repository's observed velocity
# (~112 pull requests touched per 30 days) that reaches GITHUB_TOKEN's 1,000
# requests/hour/repository primary rate limit within months, where it would
# surface as an opaque mid-retrieval HTTP 403.
#
# This budget is ~27x the measured baseline and ~60% of the hourly token
# allowance: high enough that no plausible month of activity trips it, low
# enough to fire FIRST, as a legible "retrieval is no longer affordable" alarm
# naming this constant, instead of the rate limiter firing illegibly.
#
# It bounds COST, never the obligation set: exceeding it raises AdapterError
# (exit 2) exactly like _MAX_SUPPLY_PAGES, because retrieval that stopped early
# is incomplete, and incomplete retrieval must never be read as absence. Note
# what this deliberately does NOT do — it does not narrow the retrieval window
# to keep the cost down. An obligation the monitor stops retrieving is an
# obligation it silently forgets. For why the sliding retrieval floor proposed
# in #963 cannot supply this bound without durable carry-forward state, see
# `docs/architecture/event-supply-retrieval-bound.md`.
_MAX_SUPPLY_REQUESTS = 600

# Timestamps are issued by GitHub but compared against the runner's clock, so a
# genuinely fresh event can read a hair "in the future" under NTP skew. Rejecting
# those as forged would be pure cry-wolf. The tolerance is deliberately tiny
# against a response allowance measured in days: it buys an attacker five minutes
# of an allowance they can already refresh by pushing, while removing a false-red
# that would train people to ignore this guard.
_CLOCK_SKEW_TOLERANCE = timedelta(minutes=5)

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


class _RequestBudget:
    """Requests one event-supply evaluation may spend before failing closed.

    Counting lives here rather than in a module-level total so that the ceiling
    is per-evaluation and testable without network: the unit suite asserts the
    exact request count for a given supply shape.
    """

    def __init__(self, limit: int) -> None:
        self.limit = limit
        self.spent = 0

    def spend(self, what: str) -> None:
        self.spent += 1
        if self.spent > self.limit:
            raise AdapterError(
                f"event-supply retrieval exceeded its {self.limit}-request "
                f"budget at {what}; retrieval is incomplete and cannot be read "
                "as absence. The activation cutoff is immutable by design, so "
                "the pull requests to evaluate only accumulate — bounding this "
                "needs durable carry-forward state, not a narrower window"
            )


def _github_get(endpoint: str, token: str, what: str,
                budget: _RequestBudget | None = None):
    """Read-only authenticated GET against the GitHub API. Raises AdapterError."""
    if budget is not None:
        budget.spend(what)
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


def _collect_relevant_pulls(
    repo_path: str,
    repository: str,
    event: str,
    token: str,
    since: datetime,
    budget: _RequestBudget | None = None,
) -> list[dict]:
    """Pull requests with GitHub-recorded activity at or after `since`.

    `state=all`, not `state=open`. A merged or closed pull request does NOT
    discharge an obligation whose head never got a correlated run: closing a PR
    is not an answer to it, and only a correlated terminal run resolves an
    obligation. Requesting open PRs alone let a merge erase the evidence and the
    monitor turn green — the exact silent-green failure this guard exists for.

    Survival is bounded, not unbounded: `since` is the activation cutoff, so the
    archive is walked back to that instant and no further.

    `updated_at` is used ONLY as this retrieval boundary, never as dispatch
    evidence. Every head push bumps it, so a PR whose head moved after `since`
    can never be paginated away; comments, labels and merges bump it too, which
    is exactly why it is not proof that a dispatch happened.
    """
    pulls: list[dict] = []
    page = 1
    while True:
        pull_page = _github_get(
            f"https://api.github.com/repos/{repo_path}/pulls?"
            + urlencode({
                "state": "all",
                "sort": "updated",
                "direction": "desc",
                "per_page": 100,
                "page": page,
            }),
            token,
            f"{event} supply on {repository} page {page}",
            budget,
        )
        if not isinstance(pull_page, list):
            raise AdapterError(
                f"GitHub API returned malformed pull data for {repository}"
            )
        reached_boundary = False
        for index, entry in enumerate(pull_page):
            if not isinstance(entry, dict):
                raise AdapterError(
                    f"GitHub API returned malformed pull at index {index} for "
                    f"{repository}"
                )
            updated_at = _parse_iso(entry.get("updated_at"))
            if updated_at is None:
                raise AdapterError(
                    f"GitHub API returned malformed pull updated_at for "
                    f"{repository}"
                )
            if updated_at < since:
                reached_boundary = True
                continue
            pulls.append(entry)
        if reached_boundary or len(pull_page) < 100:
            return pulls
        page += 1
        if page > _MAX_SUPPLY_PAGES:
            raise AdapterError(
                f"{event} supply on {repository} did not reach the activation "
                f"cutoff {since.isoformat()} within {_MAX_SUPPLY_PAGES} pages; "
                "retrieval is incomplete and cannot be read as absence"
            )


def _collect_target_runs(
    repo_path: str,
    workflow: str,
    event: str,
    token: str,
    since: datetime,
    budget: _RequestBudget | None = None,
) -> list:
    """Every `pull_request_target` run back to the activation cutoff.

    The newest page alone is not enough. `pull_request_target` runs cannot be
    filtered by head SHA (they execute against the trusted BASE commit), so the
    adapter correlates them client-side out of a listing — and a listing capped
    at one page silently drops any valid run beyond the newest 100. Its
    obligation then reads "no run", which is a fabricated alarm indistinguishable
    from a real one.

    Retrieval stops at the relevant-history boundary, and retrieval that cannot
    reach it raises instead of reporting absence.
    """
    runs: list = []
    page = 1
    while True:
        payload = _github_get(
            f"https://api.github.com/repos/{repo_path}/actions/workflows/"
            f"{quote(workflow, safe='')}/runs?"
            + urlencode({"event": event, "per_page": 100, "page": page}),
            token,
            f"{workflow} secured pull-request runs page {page}",
            budget,
        )
        page_runs = (payload.get("workflow_runs")
                     if isinstance(payload, dict) else None)
        if not isinstance(page_runs, list):
            raise AdapterError(
                f"GitHub Actions API returned malformed run data for {workflow}"
            )
        runs.extend(page_runs)
        if len(page_runs) < 100:
            return runs
        oldest = page_runs[-1]
        oldest_at = (
            _parse_iso(oldest.get("created_at") or oldest.get("run_started_at"))
            if isinstance(oldest, dict) else None
        )
        # An unparseable boundary timestamp is not permission to stop early; keep
        # paging and let the ceiling below convert the ambiguity into a failure.
        if oldest_at is not None and oldest_at < since:
            return runs
        page += 1
        if page > _MAX_SUPPLY_PAGES:
            raise AdapterError(
                f"{workflow} `{event}` runs did not reach the activation cutoff "
                f"{since.isoformat()} within {_MAX_SUPPLY_PAGES} pages; retrieval "
                "is incomplete and cannot be read as absence"
            )


def default_event_supply_runner(
    workflow: str,
    event: str,
    repository: str,
    token: str,
    activities: tuple[str, ...] = ("opened", "synchronize"),
    since: datetime | None = None,
) -> list[tuple[dict, dict | None]]:
    """Return PR/head dispatch obligations and their exact-head candidate runs.

    Every pull request with activity since the activation cutoff is evaluated —
    open or closed — so neither one healthy PR nor a merge button can mask an
    unanswered one. `updated_at` is deliberately not evidence: comments, labels,
    merges, and other non-dispatch activity all change it. The observable
    obligation is each PR's head SHA. A matching Actions run supplies the
    dispatch time; if no run exists, the head commit date is used only as a hint
    bounded by the GitHub-controlled `[created_at, updated_at]` envelope, because
    the commit date is written by whoever authored the commit. Both configured
    activities remain explicit because current API state cannot soundly
    distinguish an opening head from a synchronized head.
    """
    if not repository or "/" not in repository:
        raise AdapterError(
            "event-supply proof requires GITHUB_REPOSITORY (owner/repo)"
        )
    if not token:
        raise AdapterError("event-supply proof requires the existing GITHUB_TOKEN")
    if event not in {"pull_request", "pull_request_target"}:
        raise AdapterError(f"no event-supply adapter for event {event!r}")
    if not activities or any(activity not in {"opened", "synchronize"}
                             for activity in activities):
        raise AdapterError(
            f"unsupported pull_request activities for event supply: {activities!r}"
        )
    if since is None:
        raise AdapterError(
            f"event-supply proof requires an explicit activation cutoff for "
            f"`{event}`; without one the relevant history has no boundary"
        )

    budget = _RequestBudget(_MAX_SUPPLY_REQUESTS)
    repo_path = quote(repository, safe="/")
    pulls = _collect_relevant_pulls(
        repo_path, repository, event, token, since, budget
    )
    if not pulls:
        return []

    supplies: list[tuple[dict, dict | None]] = []
    target_runs: list | None = None
    if event == "pull_request_target":
        target_runs = _collect_target_runs(
            repo_path, workflow, event, token, since, budget
        )

    for index, pull in enumerate(pulls):
        pull_number = pull.get("number")
        created_at = _parse_iso(pull.get("created_at"))
        updated_at = _parse_iso(pull.get("updated_at"))
        pull_state = pull.get("state")
        head = pull.get("head")
        head_sha = head.get("sha") if isinstance(head, dict) else None
        if (not isinstance(pull_number, int) or isinstance(pull_number, bool)
                or created_at is None or updated_at is None
                or pull_state not in {"open", "closed"}
                or not isinstance(head_sha, str) or not head_sha.strip()):
            raise AdapterError(
                f"GitHub API returned malformed pull at index {index} for "
                f"{repository}: integer number, created_at, updated_at, state, "
                "and head.sha are required"
            )
        # GitHub never records a pull request as updated before it was created.
        # If it appears to, the envelope this adapter bounds author-controlled
        # timestamps against is itself untrustworthy — fail closed.
        if created_at > updated_at:
            raise AdapterError(
                f"GitHub API returned an implausible pull timeline for "
                f"#{pull_number} on {repository}: created_at is newer than "
                "updated_at"
            )

        if target_runs is None:
            payload = _github_get(
                f"https://api.github.com/repos/{repo_path}/actions/workflows/"
                f"{quote(workflow, safe='')}/runs?"
                + urlencode({
                    "event": event,
                    "head_sha": head_sha,
                    "per_page": 1,
                }),
                token,
                f"{workflow} runs for {head_sha}",
                budget,
            )
            runs = payload.get("workflow_runs") if isinstance(payload, dict) else None
            if not isinstance(runs, list):
                raise AdapterError(
                    f"GitHub Actions API returned malformed run data for {workflow}"
                )
            run = runs[0] if runs else None
        else:
            run = next((candidate for candidate in target_runs
                        if isinstance(candidate, dict)
                        and isinstance(candidate.get("pull_requests"), list)
                        and any(
                            isinstance(identity, dict)
                            and identity.get("number") == pull_number
                            and isinstance(identity.get("head"), dict)
                            and identity["head"].get("sha") == head_sha
                            for identity in candidate["pull_requests"]
                        )), None)

        malformed_reason: str | None = None
        if run is None:
            commit = _github_get(
                f"https://api.github.com/repos/{repo_path}/commits/"
                f"{quote(head_sha, safe='')}",
                token,
                f"head commit {head_sha}",
                budget,
            )
            commit_data = commit.get("commit") if isinstance(commit, dict) else None
            committer = (commit_data.get("committer")
                         if isinstance(commit_data, dict) else None)
            commit_at_raw = (committer.get("date")
                             if isinstance(committer, dict) else None)
            commit_at = _parse_iso(commit_at_raw)
            if commit_at is None:
                raise AdapterError(
                    f"GitHub API returned malformed head commit time for {head_sha}"
                )
            # The committer date is written by whoever produced the commit, so it
            # is NOT the authority for allowance aging. Dating an obligation from
            # `2099-01-01` would hold it "pending" for decades and silence this
            # guard for as long as the PR author likes.
            #
            # The GitHub-controlled envelope for when this head became the PR
            # head is [created_at, updated_at]: the obligation cannot predate the
            # pull request, and a head push always bumps updated_at. Inside that
            # envelope the commit date is a useful refinement — it distinguishes a
            # head pushed an hour ago from the day the PR was opened. Outside it,
            # on the late side, it is not evidence but a forged clock, and forged
            # evidence is reported as malformed proof (red) rather than clamped
            # and believed.
            if commit_at > updated_at:
                malformed_reason = (
                    f"head commit date {commit_at_raw!r} is newer than the pull "
                    f"request's GitHub-recorded last activity "
                    f"({pull.get('updated_at')!r}); an author-controlled commit "
                    "date cannot extend the response allowance"
                )
                occurred_at = updated_at
            else:
                occurred_at = max(created_at, commit_at)
        else:
            if not isinstance(run, dict):
                raise AdapterError(
                    f"GitHub Actions API returned malformed first run for {workflow}"
                )
            occurred_at_raw = run.get("created_at") or run.get("run_started_at")
            occurred_at = _parse_iso(occurred_at_raw)
            if occurred_at is None:
                raise AdapterError(
                    f"GitHub Actions API returned malformed run time for {workflow}"
                )
            if run.get("pull_requests") == []:
                associated_pulls = _github_get(
                    f"https://api.github.com/repos/{repo_path}/commits/"
                    f"{quote(head_sha, safe='')}/pulls",
                    token,
                    f"pull requests associated with {head_sha}",
                    budget,
                )
                if not isinstance(associated_pulls, list):
                    raise AdapterError(
                        f"GitHub API returned malformed commit pull data for {head_sha}"
                    )
                run = dict(run)
                run["associated_pull_requests"] = associated_pulls

        obligation = {
            "activities": list(activities),
            "occurred_at": occurred_at.isoformat(),
            "pull_number": pull_number,
            "head_sha": head_sha,
            "pull_state": pull_state,
        }
        if malformed_reason:
            obligation["malformed_reason"] = malformed_reason
        supplies.append((obligation, run))
    return supplies


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


def workflow_event_activities(
    workflows_dir: Path,
    workflow: str,
    event: str,
) -> set[str] | None:
    """Explicit activity types configured for a mapped workflow event."""
    path = workflows_dir / workflow
    if not path.exists():
        return None
    try:
        doc = yaml.safe_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        raise ConfigError(f"{workflow}: workflow YAML is invalid: {exc}") from exc
    on = _on_block(doc)
    config = on.get(event) if isinstance(on, dict) else None
    if not isinstance(config, dict):
        return set()
    activities = config.get("types")
    if not isinstance(activities, list):
        return set()
    return {str(activity) for activity in activities}


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

    Each sampled pull request contributes its PR/head identity, so one answered
    PR cannot mask another unanswered one — and closing or merging a PR does not
    discharge its obligation, because a merge is not an answer. Opening and
    synchronize stay explicit as a candidate activity set: generic `updated_at`
    is not dispatch evidence. A run answers only when both its PR number and head
    SHA match; a newer global run for another PR is irrelevant. Queued,
    in-progress, absent, or mismatched runs remain pending within
    `max_stale_days` and turn red only after that response allowance. A
    correlated completed failure is red at once.

    Obligations are bounded below by the event's ACTIVATION CUTOFF (declared in
    EVENT_PRODUCERS). Heads observed before it are explicitly waived: changing a
    workflow's trigger does not synthesize `opened`/`synchronize` events for
    heads that already exist, so demanding a run for them would manufacture
    alarms no producer could ever answer. An event that is active on disk with no
    declared cutoff is a ConfigError, not a free pass.

    LIMIT, stated plainly: this proves the loop was DISPATCHED and did not fail,
    not that its output was VALID. The specific #844 incident (runs green,
    review body a placeholder) is only caught here via the run conclusion, which
    exists because #840 made that failure loud. Asserting the artifact itself
    needs per-workflow proof declarations in the registry — see the report.
    """
    max_days = float(spec["max_stale_days"])

    actual_events = workflow_events(workflows_dir, workflow)
    if actual_events is None:
        return ("activation_mismatch",
                "declared event-triggered producer workflow is missing")
    declared_events = set(spec.get("events") or [])
    supported_events = {"pull_request", "pull_request_target"}
    if (not declared_events or not declared_events <= supported_events):
        raise ConfigError(
            f"{workflow}: event producer has invalid pull-request event candidates"
        )
    active_events = declared_events & actual_events
    if len(active_events) != 1:
        return ("activation_mismatch",
                f"expected exactly one of {sorted(declared_events)} but the "
                f"workflow's `on:` triggers are {sorted(actual_events)}")
    event = next(iter(active_events))

    configured_activities = workflow_event_activities(
        workflows_dir, workflow, event
    )
    declared_activities = set(spec.get("activities") or [])
    if not declared_activities:
        raise ConfigError(
            f"{workflow}: event producer must declare pull_request activities"
        )
    if configured_activities != declared_activities:
        return (
            "activation_mismatch",
            f"declared `{event}` activities {sorted(declared_activities)} do not "
            f"match workflow activities {sorted(configured_activities or [])}",
        )

    # Activation cutoff for the SELECTED event. Absent or unusable is fail-closed:
    # inferring obligations from an unknown activation instant is exactly the
    # retroactive-obligation defect this boundary exists to prevent.
    activation = spec.get("activation")
    if not isinstance(activation, dict) or event not in activation:
        raise ConfigError(
            f"{workflow}: no activation cutoff is declared for `{event}`; an "
            "event-triggered producer cannot be judged without the instant from "
            "which it began owing runs"
        )
    cutoff_raw = activation[event]
    cutoff = _parse_iso(cutoff_raw) if isinstance(cutoff_raw, str) else None
    if cutoff is None:
        raise ConfigError(
            f"{workflow}: `{event}` is the active trigger but its activation "
            f"cutoff is {cutoff_raw!r}. Changing a trigger does not synthesize "
            "past events, so obligations must not be inferred before the instant "
            "the trigger went live on the default branch. Record that instant "
            "(or waive the event) in EVENT_PRODUCERS before this producer can be "
            "judged"
        )
    if cutoff > now:
        raise ConfigError(
            f"{workflow}: `{event}` activation cutoff {cutoff.isoformat()} is in "
            "the future, which would waive every obligation and leave this guard "
            "reading green while blind"
        )

    supplies = event_supply_runner(
        workflow,
        event,
        repository,
        token,
        tuple(sorted(declared_activities)),
        cutoff,
    )
    if not isinstance(supplies, list):
        raise AdapterError(
            f"event-supply adapter returned invalid obligation collection for {workflow}"
        )
    if not supplies:
        return ("healthy",
                f"quiet: no `{event}` event has occurred since the "
                f"{cutoff.isoformat()} activation cutoff, so no run was owed "
                "(event-triggered loops are judged by event supply, not by a clock)")

    results: list[tuple[str, str]] = []
    waived = 0
    for item in supplies:
        if not isinstance(item, (list, tuple)) or len(item) != 2:
            results.append((
                "malformed_proof",
                f"`{event}` supply contains a malformed obligation/run pair",
            ))
            continue
        obligation, run = item
        if not isinstance(obligation, dict):
            results.append((
                "malformed_proof",
                f"`{event}` supply contains a non-object obligation",
            ))
            continue

        activities = obligation.get("activities")
        pull_number = obligation.get("pull_number")
        head_sha = obligation.get("head_sha")
        occurred_at = _parse_iso(obligation.get("occurred_at"))
        if (not isinstance(activities, list)
                or not activities
                or any(not isinstance(activity, str) for activity in activities)
                or set(activities) != declared_activities
                or not isinstance(pull_number, int) or isinstance(pull_number, bool)
                or not isinstance(head_sha, str) or not head_sha
                or occurred_at is None):
            results.append((
                "malformed_proof",
                f"latest `{event}` obligation has invalid activities, pull "
                "identity, head SHA, or timestamp",
            ))
            continue

        activity_label = "/".join(sorted(declared_activities))
        pull_state = obligation.get("pull_state")
        state_label = (
            f" ({pull_state})" if pull_state in {"open", "closed"} else ""
        )
        obligation_label = (
            f"PR #{pull_number}{state_label} `{activity_label}` at {head_sha[:12]}"
        )

        # A monitor cannot have observed an event that has not happened yet. A
        # future observation time is a broken or forged clock, and believing it
        # would grant an allowance that never expires.
        if occurred_at > now + _CLOCK_SKEW_TOLERANCE:
            results.append((
                "malformed_proof",
                f"{obligation_label} claims an observation time of "
                f"{obligation.get('occurred_at')!r}, which is in the future; a "
                "timestamp the monitor cannot have observed is not proof",
            ))
            continue

        # Pre-cutover head: explicitly waived, never silently dropped. The count
        # is reported in the summary so a waiver can be audited rather than
        # mistaken for an absence of pull requests.
        if occurred_at < cutoff:
            waived += 1
            continue

        # Evidence the adapter could retrieve but not trust (see
        # default_event_supply_runner) is red, not clamped-and-believed.
        malformed_reason = obligation.get("malformed_reason")
        if malformed_reason:
            results.append((
                "malformed_proof",
                f"{obligation_label} has untrustworthy timing evidence: "
                f"{malformed_reason}",
            ))
            continue

        event_age = _age_days(occurred_at, now)
        if run is None:
            if event_age <= max_days:
                results.append((
                    "pending",
                    f"{obligation_label} has no run yet but is only "
                    f"{event_age:.1f}d old (allowance {max_days:g}d)",
                ))
                continue
            kind, detail = _apply_newborn_grace(
                "silent_green",
                f"{obligation_label} has no run after {event_age:.1f}d "
                f"(allowance {max_days:g}d)",
                workflow, max_days, now, repo_root, workflows_dir,
                default_branch, git_runner,
            )
            results.append((kind, detail))
            continue
        if not isinstance(run, dict):
            results.append((
                "malformed_proof",
                f"{obligation_label} candidate run is not an object",
            ))
            continue

        run_head_sha = run.get("head_sha")
        run_pulls = run.get("pull_requests")
        associated_pulls = run.get("associated_pull_requests", [])
        identity_pulls = (
            [*run_pulls, *associated_pulls]
            if isinstance(run_pulls, list) and isinstance(associated_pulls, list)
            else None
        )
        valid_identities = (
            identity_pulls is not None
            and all(
                isinstance(run_pull, dict)
                and isinstance(run_pull.get("number"), int)
                and not isinstance(run_pull.get("number"), bool)
                and (
                    "head" not in run_pull
                    or (
                        isinstance(run_pull.get("head"), dict)
                        and isinstance(run_pull["head"].get("sha"), str)
                        and bool(run_pull["head"]["sha"])
                    )
                )
                for run_pull in identity_pulls
            )
        )
        if (not isinstance(run_head_sha, str) or not run_head_sha
                or identity_pulls is None or not valid_identities):
            results.append((
                "malformed_proof",
                f"{obligation_label} candidate run has malformed PR/head identity",
            ))
            continue

        correlated = any(
            run_pull["number"] == pull_number
            and (
                run_head_sha == head_sha
                or (
                    isinstance(run_pull.get("head"), dict)
                    and run_pull["head"].get("sha") == head_sha
                )
            )
            for run_pull in identity_pulls
        )
        status = run.get("status")
        if status not in {"queued", "in_progress", "completed"}:
            results.append((
                "malformed_proof",
                f"{obligation_label} candidate run has invalid status {status!r}",
            ))
            continue
        url = run.get("html_url") or "(no run URL)"

        if not correlated:
            kind = "pending" if event_age <= max_days else "stale"
            results.append((
                kind,
                f"{obligation_label} has no correlated run after {event_age:.1f}d "
                f"(allowance {max_days:g}d); candidate belongs to another PR/head: "
                f"{url}",
            ))
            continue
        if status in {"queued", "in_progress"}:
            kind = "pending" if event_age <= max_days else "stale"
            results.append((
                kind,
                f"{obligation_label} run is {status} after {event_age:.1f}d "
                f"(allowance {max_days:g}d): {url}",
            ))
            continue

        run_started = _parse_iso(run.get("run_started_at") or run.get("created_at"))
        if run_started is None:
            results.append((
                "malformed_proof",
                f"{obligation_label} completed run has no parseable timestamp",
            ))
            continue
        conclusion = run.get("conclusion")
        if conclusion != "success":
            results.append((
                "failed_run",
                f"{obligation_label} run concluded {conclusion!r}: {url}",
            ))
            continue
        results.append((
            "healthy",
            f"{obligation_label} has a correlated successful run "
            f"({_age_days(run_started, now):.1f}d ago): {url}",
        ))

    waiver_note = (
        f" ({waived} pre-cutoff obligation(s) waived at {cutoff.isoformat()})"
        if waived else ""
    )
    if not results:
        return ("healthy",
                f"quiet: every observed `{event}` obligation{waiver_note} "
                "predates the activation cutoff and is explicitly waived — "
                "changing a trigger does not synthesize past events")

    priority = {
        "malformed_proof": 4,
        "failed_run": 3,
        "stale": 3,
        "silent_green": 3,
        "pending": 1,
        "newborn": 0,
        "healthy": 0,
    }
    kind, detail = max(results, key=lambda result: priority.get(result[0], 5))
    return kind, f"evaluated {len(results)} PR obligation(s){waiver_note}: {detail}"


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
