#!/usr/bin/env python3
"""Merge planner and dry-run execution simulator over an execution graph (#540).

The Planner MVP finale: given a compiled execution graph, produce a deterministic
merge order and a dry-run simulation of where every work package sits in its
lifecycle, then assemble a PlannerReport.

Composes the earlier slices:
  - execution precedence + critical path (planner_critical_path, #535);
  - collision-driven review stages (planner_scheduler, #539, which itself uses
    the collision detector, #536).

Merge precedence = execution dependencies (``depends_on`` / ``blocks``) PLUS
explicit ``should_merge_after`` edges. States are computed from each node's
``status`` (default ``pending``) plus dependency completion and review needs:

  - ``blocked``    : an execution predecessor is not yet done;
  - ``ready``      : dependencies done, the package itself not yet done;
  - ``in-review``  : done, but flagged for a review stage that is unresolved;
  - ``mergeable``  : done and reviewed (or no review needed).

Deterministic, non-mutating, recommend-only (#529 guardrail). CLI dry-run report.
"""
from __future__ import annotations

import argparse
import heapq
import json
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))
import planner_critical_path as pcp  # noqa: E402
import planner_scheduler as ps  # noqa: E402

_DONE = {"done", "complete", "completed", "merged"}

# Merge precedence: 'value' must land before 'key-source'.
_MERGE_PRECEDENCE = {
    "depends_on": lambda e: (e["to"], e["from"]),
    "blocks": lambda e: (e["from"], e["to"]),
    "should_merge_after": lambda e: (e["to"], e["from"]),
}


def merge_order(graph: dict[str, Any]) -> list[str]:
    """Deterministic merge order over execution + should_merge_after precedence."""
    node_ids = [n["node_id"] for n in graph.get("nodes", [])]
    known = set(node_ids)
    succ: dict[str, set[str]] = {nid: set() for nid in node_ids}
    indeg: dict[str, int] = {nid: 0 for nid in node_ids}
    for edge in graph.get("edges", []):
        convert = _MERGE_PRECEDENCE.get(edge.get("type"))
        if convert is None:
            continue
        pred, node = convert(edge)
        if pred in known and node in known and node not in succ[pred]:
            succ[pred].add(node)
            indeg[node] += 1

    heap = [nid for nid in node_ids if indeg[nid] == 0]
    heapq.heapify(heap)
    order: list[str] = []
    while heap:
        node = heapq.heappop(heap)
        order.append(node)
        for nxt in sorted(succ[node]):
            indeg[nxt] -= 1
            if indeg[nxt] == 0:
                heapq.heappush(heap, nxt)
    if len(order) != len(node_ids):
        raise ValueError("merge graph is not acyclic")
    return order


def simulate(graph: dict[str, Any]) -> dict[str, str]:
    """Return {node_id: state} for the current snapshot."""
    node_ids, succ, _ = pcp._precedence(graph)
    preds: dict[str, set[str]] = {nid: set() for nid in node_ids}
    for pred, nexts in succ.items():
        for node in nexts:
            preds[node].add(pred)
    by_id = {n["node_id"]: n for n in graph.get("nodes", [])}
    review = set(ps.schedule(graph)["review_required"])

    def done(nid: str) -> bool:
        return by_id[nid].get("status", "pending") in _DONE

    states: dict[str, str] = {}
    for nid in node_ids:
        if not all(done(p) for p in preds[nid]):
            states[nid] = "blocked"
        elif not done(nid):
            states[nid] = "ready"
        elif nid in review:
            states[nid] = "in-review"
        else:
            states[nid] = "mergeable"
    return states


def plan(graph: dict[str, Any]) -> dict[str, Any]:
    """Assemble the PlannerReport: merge order, per-node states, summary,
    assumptions, risks, evidence references, and recommended next actions."""
    order = merge_order(graph)
    states = simulate(graph)
    review = ps.schedule(graph)["review_required"]
    summary = {state: sum(1 for v in states.values() if v == state)
               for state in ("ready", "blocked", "in-review", "mergeable")}
    evidence = {n["node_id"]: n["evidence"]
                for n in graph.get("nodes", []) if n.get("evidence")}

    def in_state(state: str) -> list[str]:
        return [nid for nid in order if states[nid] == state]

    next_actions: list[str] = []
    if in_state("mergeable"):
        next_actions.append("merge (in order): " + ", ".join(in_state("mergeable")))
    if in_state("in-review"):
        next_actions.append("resolve review stages: " + ", ".join(in_state("in-review")))
    if in_state("blocked"):
        next_actions.append("unblock by completing dependencies: "
                            + ", ".join(in_state("blocked")))

    return {
        "merge_order": order,
        "states": states,
        "summary": summary,
        "assumptions": [
            "node status is read from the graph (default 'pending'); a review stage "
            "is treated as unresolved until approved",
            "merge precedence = execution dependencies + should_merge_after edges",
        ],
        "risks": review,
        "evidence": evidence,
        "next_actions": next_actions,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Merge planner + dry-run simulator over an execution graph (#540)")
    parser.add_argument("--graph", required=True, help="path to a compiled graph JSON")
    parser.add_argument("--out", help="write the PlannerReport JSON here (default: stdout summary)")
    args = parser.parse_args(argv)
    try:
        with open(args.graph, encoding="utf-8") as stream:
            graph = json.load(stream)
        report = plan(graph)
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as error:
        print(f"merge-simulator: {error}", file=sys.stderr)
        return 2
    if args.out:
        with open(args.out, "w", encoding="utf-8") as stream:
            json.dump(report, stream, indent=2)
            stream.write("\n")
    print("merge order: " + " -> ".join(report["merge_order"]))
    print("states: " + ", ".join(f"{k}={v}" for k, v in report["summary"].items()))
    for action in report["next_actions"]:
        print("next: " + action)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
