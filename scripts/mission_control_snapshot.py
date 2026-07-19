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

_SCHEMA_PATH = Path(__file__).resolve().parents[1] / "schemas" / "progress-snapshot.schema.json"

_READY_LABELS = ("ready-for-agent", "ready-for-human")


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


def _dashboard(issues_by_status, pull_requests):
    open_prs = [p for p in pull_requests if str(p.get("state", "open")).lower() == "open"]
    return {
        "open_prs": len(open_prs),
        "merged_prs": sum(1 for p in pull_requests if str(p.get("state", "")).lower() == "merged"),
        "draft_prs": sum(1 for p in open_prs if p.get("draft")),
        "review_queue": sum(1 for p in open_prs if not p.get("draft")),
        "issues_by_status": issues_by_status,
    }


def build_snapshot(data):
    """Compute a progress snapshot dict from an issues/PRs fixture."""
    issues = data.get("issues", [])
    statuses = [classify_issue(issue) for issue in issues]

    by_status = {}
    for status in statuses:
        by_status[status] = by_status.get(status, 0) + 1

    total = len(issues)
    completed = by_status.get("done", 0)
    blocked = by_status.get("blocked", 0)
    executable = by_status.get("executable", 0)
    percent = round(100.0 * completed / total, 1) if total else 0.0

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
