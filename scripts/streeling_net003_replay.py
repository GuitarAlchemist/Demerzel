#!/usr/bin/env python3
"""Replay NET-003's declared lane graph against its pinned advisory selector."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PIN = "ecdc6c27559bb1a11343cfad33687465893e9891"
SOURCE_PATHS = (
    "scripts/aiw_lane_selector.py",
    "state/driver/aiw-worker-lanes.json",
)
EXPECTED = {
    "NORMAL": (22, 9, 5),
    "CONSTRAINED": (21, 8, 4),
    "DRAINING": (21, 8, 4),
    "HALTED": (8, 3, 1),
}


def git_output(*args: str) -> str:
    return subprocess.check_output(
        ["git", "-C", str(ROOT), *args], text=True
    ).strip()


def main() -> int:
    blob_ids = {}
    for path in SOURCE_PATHS:
        pinned = git_output("rev-parse", f"{PIN}:{path}")
        checked_out = git_output("hash-object", str(ROOT / path))
        if checked_out != pinned:
            raise SystemExit(f"{path} differs from the pinned course revision {PIN}")
        blob_ids[path] = pinned

    sys.path.insert(0, str(ROOT / "scripts"))
    from aiw_lane_selector import load_lanes, select_lane

    policy = load_lanes(ROOT / "state/driver/aiw-worker-lanes.json")
    workers = policy["workers"]
    roles = policy["roles"]
    assigned = [
        (worker, role)
        for worker, lane in workers.items()
        for role in [lane["primary"], *lane.get("secondary", [])]
    ]
    if len(assigned) != 22:
        raise SystemExit(f"expected 22 assigned worker-role pairs, got {len(assigned)}")

    modes = {}
    for mode in policy["mode_blocks"]:
        active = []
        primary_count = 0
        for worker, role in assigned:
            request = {
                "worker": worker,
                "requested_role": role,
                "fan_out_mode": mode,
                "subject": "worker_task",
            }
            decision = select_lane(request, policy)["rule_result"]["decision"]
            if decision in ("allow", "recommend"):
                active.append((worker, roles[role]["work_class"]))
                primary_count += role == workers[worker]["primary"]
            elif decision != "block":
                raise SystemExit(f"unexpected assigned-role decision: {request}: {decision}")

        measured = (len(active), len(set(active)), primary_count)
        if measured != EXPECTED[mode]:
            raise SystemExit(f"{mode}: expected {EXPECTED[mode]}, got {measured}")
        modes[mode] = {
            "unblocked_role_paths": measured[0],
            "worker_class_edges": measured[1],
            "unblocked_primary_paths": measured[2],
        }

    controls = {}
    for name, worker, role, mode, expected in (
        ("forbidden_role", "codex", "autonomous_merge_actor", "NORMAL", "block"),
        ("unknown_role", "codex", "role_that_does_not_exist", "NORMAL", "warn"),
        ("unknown_mode", "codex", workers["codex"]["primary"], "UNKNOWN", "escalate"),
    ):
        result = select_lane(
            {
                "worker": worker,
                "requested_role": role,
                "fan_out_mode": mode,
                "subject": "worker_task",
            },
            policy,
        )["rule_result"]
        if result["decision"] != expected:
            raise SystemExit(f"{name}: expected {expected}, got {result['decision']}")
        controls[name] = {
            "decision": result["decision"],
            "reason_codes": result["reason_codes"],
        }

    print(
        json.dumps(
            {
                "source_revision": PIN,
                "source_blobs": blob_ids,
                "assigned_role_pairs": len(assigned),
                "modes": modes,
                "controls": controls,
            },
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
