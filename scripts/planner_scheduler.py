#!/usr/bin/env python3
"""Parallel work scheduler and review planner over an execution graph (#539).

Turns a compiled execution graph (``epic_to_dag_compiler.compile_epic``) into a
safe, deterministic execution plan by composing the two prior Planner slices:

  - dependency **levels** (Kahn layering over precedence edges): each level is the
    set of packages whose predecessors have all completed, i.e. dependency-ready
    together (reuses planner_critical_path's precedence — #535);
  - within a level, packages are dependency-independent but may still collide, so
    the **collision graph** (planner_collision_detector — #536) is greedily
    coloured into parallel **batches**: two packages that collide never share a
    batch, non-colliding packages run in parallel.

Review planning: any package involved in a collision receives a review stage (a
human decides the sequencing/merge), reported in recommended-review order.

Deterministic (sorted + greedy) and explainable; never mutates input; recommends
only (#529 guardrail). Run as a CLI for a dry-run plan.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))
import planner_collision_detector as pcd  # noqa: E402
import planner_critical_path as pcp  # noqa: E402


def _levels(graph: dict[str, Any]) -> list[list[str]]:
    """Kahn layering over execution precedence: level i = nodes at dependency
    depth i. Reuses the single precedence definition from planner_critical_path."""
    node_ids, succ, indeg = pcp._precedence(graph)
    remaining = dict(indeg)
    ready = sorted(n for n in node_ids if remaining[n] == 0)
    levels: list[list[str]] = []
    placed = 0
    while ready:
        levels.append(list(ready))
        placed += len(ready)
        nxt: list[str] = []
        for node in ready:
            for succ_node in succ[node]:
                remaining[succ_node] -= 1
                if remaining[succ_node] == 0:
                    nxt.append(succ_node)
        ready = sorted(nxt)
    if placed != len(node_ids):  # defensive: a cycle would strand nodes
        raise ValueError("graph is not acyclic; cannot schedule")
    return levels


def _collision_pairs(graph: dict[str, Any]) -> set[frozenset[str]]:
    return {frozenset((c["a"], c["b"]))
            for c in pcd.detect_collisions(graph)["collisions"]}


def _batches(level: list[str], collisions: set[frozenset[str]]) -> list[list[str]]:
    """Greedy graph colouring: colliding nodes get different colours (batches)."""
    colour: dict[str, int] = {}
    for node in sorted(level):
        blocked = {colour[other] for other in level
                   if other in colour and frozenset((node, other)) in collisions}
        chosen = 0
        while chosen in blocked:
            chosen += 1
        colour[node] = chosen
    grouped: dict[int, list[str]] = {}
    for node in level:
        grouped.setdefault(colour[node], []).append(node)
    return [sorted(grouped[c]) for c in sorted(grouped)]


def schedule(graph: dict[str, Any]) -> dict[str, Any]:
    """Return a deterministic parallel execution + review plan.

    ``waves``: dependency levels, each ``{level, batches}`` where every batch is a
    set of packages safe to run in parallel. ``execution_order``: a flattened
    deterministic order. ``review_required`` / ``review_order``: collision-involved
    packages needing a review stage. ``critical_path``: the schedule-critical chain.
    """
    levels = _levels(graph)
    collisions = _collision_pairs(graph)
    waves: list[dict[str, Any]] = []
    execution_order: list[str] = []
    for depth, level in enumerate(levels):
        batches = _batches(level, collisions)
        waves.append({"level": depth, "batches": batches})
        for batch in batches:
            execution_order.extend(batch)

    involved = sorted({n for pair in collisions for n in pair})
    order_index = {n: i for i, n in enumerate(execution_order)}
    review_order = sorted(involved, key=lambda n: order_index.get(n, len(order_index)))
    return {
        "waves": waves,
        "execution_order": execution_order,
        "review_required": involved,
        "review_order": review_order,
        "critical_path": pcp.critical_path(graph)["path"],
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Parallel scheduler + review planner over an execution graph (dry-run, #539)")
    parser.add_argument("--graph", required=True, help="path to a compiled graph JSON")
    args = parser.parse_args(argv)
    try:
        with open(args.graph, encoding="utf-8") as stream:
            graph = json.load(stream)
        plan = schedule(graph)
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as error:
        print(f"scheduler: {error}", file=sys.stderr)
        return 2
    for wave in plan["waves"]:
        lanes = " | ".join("[" + ", ".join(b) + "]" for b in wave["batches"])
        print(f"wave {wave['level']}: {lanes}")
    if plan["review_required"]:
        print("review stages: " + ", ".join(plan["review_order"]))
    print("critical path: " + " -> ".join(plan["critical_path"]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
