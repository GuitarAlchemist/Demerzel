#!/usr/bin/env python3
"""Universal ecosystem-freshness monitor — one guard for every scheduled loop.

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

Findings and exit codes (a producer with a real problem must fail CI):

  0  every active loop is healthy; disabled entries are bounded and verified.
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
# Everything else (healthy, disabled) is exit 0.


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

def _schedule_block(doc: dict):
    """`on:` parses to the YAML 1.1 boolean True under PyYAML, so look under both."""
    if not isinstance(doc, dict):
        return None
    on = doc.get("on")
    if on is None:
        on = doc.get(True)
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


# ---------------------------------------------------------------------------
# per-loop evaluation
# ---------------------------------------------------------------------------

def _evaluate_loop(
    loop: dict,
    now: datetime,
    repo_root: Path,
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
        return _eval_state_glob(proof, now, repo_root)
    if adapter == "git_log":
        return _eval_git_log(proof, now, repo_root, default_branch, git_runner)
    if adapter == "workflow_run":
        return _eval_workflow_run(
            proof,
            wf,
            now,
            repository,
            default_branch,
            token,
            actions_runner,
        )
    raise ConfigError(f"{wf}: unknown proof adapter {adapter!r}")


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
