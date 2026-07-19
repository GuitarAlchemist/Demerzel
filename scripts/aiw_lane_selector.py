#!/usr/bin/env python3
"""AIW advisory lane selector (#737).

The executable consumer for the worker-lane definitions documented in
`docs/workflows/aiw-composite-lanes.md` and made canonical in
`state/driver/aiw-worker-lanes.json`. Given a proposed
{worker, requested_role, fan_out_mode, subject}, it emits a schema-valid
`advisory-decision` (schemas/advisory-decision.schema.json) answering:

  * is `worker` a defined lane?
  * is `requested_role` forbidden for that worker? (the governance boundary)
  * does `requested_role` belong to that worker's lane at all?
  * is the role's work_class allowed in the current fan-out mode?

This is ADVISORY / DRY-RUN. It never mutates any GitHub or filesystem state.
The allow/block outcome is carried in the decision payload, not the exit code:
exit 0 = evaluated (read the decision), exit 2 = could not evaluate (bad input
or missing/invalid lane policy). Stdlib only — no third-party imports.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

_LANES_PATH = Path(__file__).resolve().parents[1] / "state" / "driver" / "aiw-worker-lanes.json"

# Subjects permitted by schemas/advisory-decision.schema.json.
_VALID_SUBJECTS = ("issue", "pull_request", "batch", "worker_task", "execution_episode")

RULE_ID = "LANE-SEL-001"


def load_lanes(path=None):
    """Load and minimally validate the canonical lane policy."""
    lanes_path = Path(path) if path else _LANES_PATH
    with open(lanes_path, "r", encoding="utf-8") as f:
        policy = json.load(f)
    for key in ("roles", "workers", "mode_blocks"):
        if key not in policy:
            raise ValueError(f"lane policy is missing required key '{key}'")
    return policy


def _decision(subject, decision, reason_codes, evidence_refs, next_actions, confidence):
    return {
        "rule_result": {
            "rule_id": RULE_ID,
            "subject": subject,
            "decision": decision,
            "reason_codes": list(reason_codes),
            "evidence_refs": list(evidence_refs),
            "next_actions": list(next_actions),
            "confidence": confidence,
        }
    }


def select_lane(request, policy):
    """Evaluate a lane-assignment request. Returns an advisory-decision dict.

    request keys: worker, requested_role, fan_out_mode, subject.
    """
    worker = request.get("worker")
    role = request.get("requested_role")
    mode = request.get("fan_out_mode")
    subject = request.get("subject", "worker_task")

    # Normalize subject to the schema enum; anything else is a caller error we
    # surface as an escalate rather than silently emitting an invalid decision.
    if subject not in _VALID_SUBJECTS:
        return _decision(
            "worker_task", "escalate",
            ["SCOPE.UNDEFINED"],
            [f"subject={subject!r}"],
            [f"use one of {', '.join(_VALID_SUBJECTS)}"],
            "high",
        )

    workers = policy["workers"]
    roles = policy["roles"]
    mode_blocks = policy["mode_blocks"]

    # 1. Unknown worker lane.
    if worker not in workers:
        return _decision(
            subject, "block",
            ["CAPABILITY.UNAVAILABLE"],
            [f"worker={worker!r}"],
            ["route the task to a defined worker lane (jules, claude, gemini, codex, augment)"],
            "high",
        )
    lane = workers[worker]

    # 2. Unknown fan-out mode.
    if mode not in mode_blocks:
        return _decision(
            subject, "escalate",
            ["SCOPE.UNDEFINED"],
            [f"fan_out_mode={mode!r}"],
            [f"supply a defined mode ({', '.join(mode_blocks.keys())})"],
            "high",
        )

    # 3. Forbidden role for this worker — the governance boundary. Checked before
    #    membership so a forbidden request is always blocked, never merely warned.
    if role in lane.get("forbidden", []):
        return _decision(
            subject, "block",
            ["CAPABILITY.FORBIDDEN_ROLE"],
            [f"worker={worker}", f"forbidden={lane['forbidden']}"],
            [f"reassign to a worker whose lane permits '{role}'; this lane forbids it"],
            "high",
        )

    # 4. Role not part of this worker's lane (neither primary nor secondary).
    lane_roles = [lane["primary"]] + list(lane.get("secondary", []))
    if role not in lane_roles:
        return _decision(
            subject, "warn",
            ["CAPABILITY.MISMATCH"],
            [f"worker={worker}", f"lane_roles={lane_roles}"],
            [f"confirm '{role}' belongs to this worker's lane, or pick a lane role"],
            "medium",
        )

    # 5. Mode gating by the role's work_class.
    role_def = roles.get(role, {})
    work_class = role_def.get("work_class")
    blocked_classes = mode_blocks[mode]
    if work_class in blocked_classes:
        return _decision(
            subject, "block",
            ["SYSTEM.BACKPRESSURE_HIGH", f"WORK_CLASS.{str(work_class).upper()}"],
            [f"fan_out_mode={mode}", f"work_class={work_class}", f"mode_blocks={blocked_classes}"],
            [
                f"defer '{role}' until fan-out returns to a mode that allows '{work_class}' work, "
                "or fall back to a mode-safe secondary role in this lane",
            ],
            "high",
        )

    # 6. Allowed. Primary is a direct match; a secondary role is an advisory fallback.
    is_primary = role == lane["primary"]
    reason = "LANE.PRIMARY_MATCH" if is_primary else "LANE.SECONDARY_FALLBACK"
    outcome = "allow" if is_primary else "recommend"
    expected = role_def.get("expected_output") or "see lane definition"
    return _decision(
        subject, outcome,
        [reason],
        [f"worker={worker}", f"role={role}", f"work_class={work_class}", f"fan_out_mode={mode}"],
        [f"proceed under advisory lane; expected output: {expected}"],
        "high",
    )


def _read_request(args):
    if args.request:
        with open(args.request, "r", encoding="utf-8") as f:
            return json.load(f)
    if not sys.stdin.isatty():
        data = sys.stdin.read().strip()
        if data:
            return json.loads(data)
    raise ValueError("no request provided: pass --request <path> or pipe JSON on stdin")


def main(argv=None):
    parser = argparse.ArgumentParser(description="AIW advisory lane selector (dry-run, #737)")
    parser.add_argument("--request", help="path to a JSON request {worker, requested_role, fan_out_mode, subject}")
    parser.add_argument("--lanes", help="path to the canonical lane policy JSON")
    args = parser.parse_args(argv)

    try:
        policy = load_lanes(args.lanes)
        request = _read_request(args)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(json.dumps({"error": str(exc)}), file=sys.stderr)
        return 2

    decision = select_lane(request, policy)
    print(json.dumps(decision, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
