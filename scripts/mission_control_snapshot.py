#!/usr/bin/env python3
"""Mission Control progress snapshot generator (Epic #547, slice S0 #742).

Read-only tracer-bullet: reads a GitHub issues/PRs snapshot (an offline fixture,
so CI is deterministic and never calls live GitHub) and computes a
`progress_snapshot` conforming to schemas/progress-snapshot.schema.json — the
counts (#547 Progress Engine) plus a Level 1 execution dashboard. Emits
machine-readable JSON and an optional Markdown summary.

MVP is read-only / dry-run: it never mutates issues or PRs. Fields owned by later
slices (critical_path/eta — S3 #746; risks/recommendations — S4 #749) are emitted
empty so those slices extend the snapshot without a schema change.

Stdlib + `jsonschema` only.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import jsonschema

from streeling_event_store import EventStore

_REPO_ROOT = Path(__file__).resolve().parents[1]
_SCHEMA_PATH = _REPO_ROOT / "schemas" / "progress-snapshot.schema.json"
_CAPABILITY_MAP_PATH = _REPO_ROOT / "state" / "driver" / "mission-control-capability-map.json"
# The Streeling event store (#545) is the telemetry source. In MVP this is the
# committed sample; in production it is the live append-only log.
_EVENTS_PATH = _REPO_ROOT / "fixtures" / "streeling" / "engineering-events-sample.jsonl"

_READY_LABELS = ("ready-for-agent", "ready-for-human")

# Workers reported in telemetry (schema worker enum minus "unknown"), fixed order.
_TELEMETRY_WORKERS = ("claude", "jules", "gemini", "codex", "augment", "github-actions", "human")
# Level 3 metrics that are NOT derivable from visible GitHub/Streeling activity
# today — reported as unmeasured rather than guessed (#745 non-goal).
_UNMEASURED = ("average_latency", "accepted_findings", "false_positives", "human_rescue_rate", "cost")


def classify_issue(issue):
    """Map a GitHub issue to an execution-node status.

    done (closed) / blocked (a 'blocked' label) / executable (ready + open) /
    planned (open, not yet ready). Blocked takes precedence over ready.
    """
    state = str(issue.get("state", "open")).lower()
    labels = [str(label).lower() for label in issue.get("labels", [])]
    if state == "closed":
        return "done"
    if any("blocked" in label for label in labels):
        return "blocked"
    if any(label in _READY_LABELS for label in labels):
        return "executable"
    return "planned"


def _counts(statuses):
    """Return (total, completed, blocked, executable, percent) for a status list."""
    total = len(statuses)
    completed = sum(1 for s in statuses if s == "done")
    blocked = sum(1 for s in statuses if s == "blocked")
    executable = sum(1 for s in statuses if s == "executable")
    percent = round(100.0 * completed / total, 1) if total else 0.0
    return total, completed, blocked, executable, percent


def load_capability_map(path=None):
    with open(Path(path) if path else _CAPABILITY_MAP_PATH, "r", encoding="utf-8") as f:
        return json.load(f)["capabilities"]


def capability_progress(issues, capability_map):
    """Per-capability progress. An issue counts toward a capability if it carries
    ANY of that capability's labels; an issue may count toward several. Capability
    order follows the map (stable output). Capabilities with no matching issue
    report 0/0 = 0%% rather than being dropped."""
    rows = []
    for capability, labels in capability_map.items():
        label_set = {label.lower() for label in labels}
        statuses = [
            classify_issue(issue)
            for issue in issues
            if label_set & {str(l).lower() for l in issue.get("labels", [])}
        ]
        total, completed, blocked, executable, percent = _counts(statuses)
        rows.append({
            "capability": capability,
            "total_nodes": total,
            "completed_nodes": completed,
            "blocked_nodes": blocked,
            "executable_nodes": executable,
            "percent_complete": percent,
        })
    return rows


def load_events(path=None):
    """Read engineering events through the #545 Streeling store reader. Empty if
    the log does not exist."""
    return list(EventStore(Path(path) if path else _EVENTS_PATH).read_all())


def agent_telemetry(events):
    """Per-worker visible activity from the Streeling event stream. Reports every
    known worker (0s if idle); unmeasurable Level 3 metrics are null/unmeasured,
    never guessed."""
    rows = []
    for worker in _TELEMETRY_WORKERS:
        mine = [e for e in events if e.get("worker") == worker]

        def _action(evt):
            return (evt.get("metadata") or {}).get("action")

        prs_opened = sum(1 for e in mine if e.get("event_type") == "pr" and _action(e) == "opened")
        prs_merged = sum(1 for e in mine if e.get("event_type") == "pr" and _action(e) == "merged")
        reviews = sum(1 for e in mine if e.get("event_type") == "review")
        comments = sum(1 for e in mine if e.get("event_type") == "comment")
        workflow_runs = sum(1 for e in mine if e.get("event_type") == "workflow")
        workflow_successes = sum(
            1 for e in mine if e.get("event_type") == "workflow" and e.get("severity") == "success"
        )
        ci_rate = round(workflow_successes / workflow_runs, 2) if workflow_runs else None

        rows.append({
            "worker": worker,
            "prs_opened": prs_opened,
            "prs_merged": prs_merged,
            "reviews": reviews,
            "comments": comments,
            "workflow_runs": workflow_runs,
            "workflow_successes": workflow_successes,
            "ci_success_rate": ci_rate,
            "unmeasured": list(_UNMEASURED),
        })
    return rows


def _dashboard(issues_by_status, pull_requests):
    open_prs = [p for p in pull_requests if str(p.get("state", "open")).lower() == "open"]
    return {
        "open_prs": len(open_prs),
        "merged_prs": sum(1 for p in pull_requests if str(p.get("state", "")).lower() == "merged"),
        "draft_prs": sum(1 for p in open_prs if p.get("draft")),
        "review_queue": sum(1 for p in open_prs if not p.get("draft")),
        "issues_by_status": issues_by_status,
    }


def build_snapshot(data, capability_map=None, events=None):
    """Compute a progress snapshot dict from an issues/PRs fixture."""
    issues = data.get("issues", [])
    statuses = [classify_issue(issue) for issue in issues]

    by_status = {}
    for status in statuses:
        by_status[status] = by_status.get(status, 0) + 1

    total, completed, blocked, executable, percent = _counts(statuses)

    if capability_map is None:
        capability_map = load_capability_map()
    if events is None:
        events = load_events()

    snapshot = {
        "snapshot_id": data.get("snapshot_id", "progress-snapshot"),
        "observed_at": data["observed_at"],
        "roadmap": data.get("roadmap", ""),
        "milestone": data.get("milestone"),
        "sprint": data.get("sprint"),
        "total_nodes": total,
        "completed_nodes": completed,
        "blocked_nodes": blocked,
        "executable_nodes": executable,
        "percent_complete": percent,
        "dashboard": _dashboard(by_status, data.get("pull_requests", [])),
        "capabilities": capability_progress(issues, capability_map),
        "agent_telemetry": agent_telemetry(events),
        # Owned by later slices — emitted empty in S0.
        "critical_path": [],
        "eta": None,
        "eta_confidence": 0.0,
        "risks": [],
        "recommendations": [],
    }
    validate_snapshot(snapshot)
    return snapshot


def validate_snapshot(snapshot):
    with open(_SCHEMA_PATH, "r", encoding="utf-8") as f:
        schema = json.load(f)
    jsonschema.validate(snapshot, schema)
    return True


def render_markdown(snapshot):
    """Render a human-readable Markdown summary of a snapshot."""
    d = snapshot.get("dashboard", {})
    by_status = d.get("issues_by_status", {})
    lines = [
        f"# Mission Control — {snapshot.get('sprint') or snapshot.get('roadmap', 'Progress')}",
        "",
        f"_Snapshot `{snapshot['snapshot_id']}` observed at {snapshot['observed_at']} (read-only)_",
        "",
        f"**{snapshot['percent_complete']}% complete** "
        f"— {snapshot['completed_nodes']}/{snapshot['total_nodes']} done, "
        f"{snapshot['blocked_nodes']} blocked, {snapshot['executable_nodes']} executable",
        "",
        "| Metric | Value |",
        "|---|---|",
        f"| Milestone | {snapshot.get('milestone') or '—'} |",
        f"| Total nodes | {snapshot['total_nodes']} |",
        f"| Done | {by_status.get('done', 0)} |",
        f"| Blocked | {by_status.get('blocked', 0)} |",
        f"| Executable | {by_status.get('executable', 0)} |",
        f"| Planned | {by_status.get('planned', 0)} |",
        f"| Open PRs | {d.get('open_prs', 0)} (review queue {d.get('review_queue', 0)}, draft {d.get('draft_prs', 0)}) |",
        f"| Merged PRs | {d.get('merged_prs', 0)} |",
    ]

    active = [c for c in snapshot.get("capabilities", []) if c["total_nodes"] > 0]
    if active:
        lines += ["", "## Capability progress", "", "| Capability | Complete | Done / Total |", "|---|---|---|"]
        for cap in active:
            lines.append(
                f"| {cap['capability']} | {cap['percent_complete']}% | "
                f"{cap['completed_nodes']}/{cap['total_nodes']} |"
            )

    def _active_worker(t):
        return t["prs_opened"] or t["prs_merged"] or t["reviews"] or t["comments"] or t["workflow_runs"]

    telemetry = [t for t in snapshot.get("agent_telemetry", []) if _active_worker(t)]
    if telemetry:
        lines += ["", "## Agent telemetry", "",
                  "| Worker | PRs opened | PRs merged | Reviews | CI success |", "|---|---|---|---|---|"]
        for t in telemetry:
            ci = "—" if t["ci_success_rate"] is None else f"{int(t['ci_success_rate'] * 100)}%"
            lines.append(
                f"| {t['worker']} | {t['prs_opened']} | {t['prs_merged']} | {t['reviews']} | {ci} |"
            )
        lines += ["", f"_Not yet measurable: {', '.join(_UNMEASURED)}._"]

    return "\n".join(lines) + "\n"


def main(argv=None):
    parser = argparse.ArgumentParser(description="Mission Control progress snapshot (read-only, #742)")
    parser.add_argument("--input", required=True, help="path to an issues/PRs snapshot fixture JSON")
    parser.add_argument("--out", help="write the snapshot JSON here (default: stdout)")
    parser.add_argument("--markdown", help="also write a Markdown summary here")
    args = parser.parse_args(argv)

    try:
        with open(args.input, "r", encoding="utf-8") as f:
            data = json.load(f)
        snapshot = build_snapshot(data)
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as exc:
        print(json.dumps({"error": str(exc)}), file=sys.stderr)
        return 2

    text = json.dumps(snapshot, indent=2)
    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(text + "\n")
        print(f"wrote {args.out} ({snapshot['percent_complete']}% complete)")
    else:
        print(text)

    if args.markdown:
        with open(args.markdown, "w", encoding="utf-8") as f:
            f.write(render_markdown(snapshot))
        print(f"wrote {args.markdown}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
