#!/usr/bin/env python3
"""File/path collision detector over a compiled execution graph (Planner #536).

Detects work packages that cannot safely run in parallel. Consumes an execution
graph from ``epic_to_dag_compiler.compile_epic`` (``{nodes, edges}``).

Grounding: real work packages today declare ``repo`` + dependency edges but no
file paths, so the always-available signals are **repo** and **execution
precedence**:

  - packages already ordered by a ``depends_on`` / ``blocks`` chain never collide
    in parallel (they are sequenced);
  - concurrent packages in *different* repos are parallel-safe;
  - concurrent packages in the *same* repo are a collision risk.

When a package additionally declares ``paths`` (node-level ``paths`` or
``metadata.paths`` / ``metadata.likely_touched_paths``), the same-repo risk is
refined per #536's acceptance criteria: same file -> high, same path-cluster ->
medium, disjoint or docs-vs-code -> low. Undeclared paths fail safe to medium.

Pure, deterministic, non-mutating. The Planner only recommends (#529 guardrail).
"""
from __future__ import annotations

import argparse
import json
import sys
from itertools import combinations
from typing import Any

HIGH, MEDIUM, LOW = "high", "medium", "low"

# Same execution-precedence semantics as planner_critical_path (#535): a package
# that must finish before another is that other's predecessor.
_PRECEDENCE = {
    "depends_on": lambda e: (e["to"], e["from"]),
    "blocks": lambda e: (e["from"], e["to"]),
}


def _reachability(graph: dict[str, Any]):
    """Return (node_ids, reach) where reach[u] is every node u precedes."""
    node_ids = [n["node_id"] for n in graph.get("nodes", [])]
    known = set(node_ids)
    succ: dict[str, set[str]] = {nid: set() for nid in node_ids}
    for edge in graph.get("edges", []):
        convert = _PRECEDENCE.get(edge.get("type"))
        if convert is None:
            continue
        pred, node = convert(edge)
        if pred in known and node in known:
            succ[pred].add(node)

    reach: dict[str, set[str]] = {}
    walking: set[str] = set()

    def descend(u: str) -> set[str]:
        if u in reach:
            return reach[u]
        if u in walking:  # defensive: a cycle slipped past validation
            raise ValueError(f"cycle through node {u!r}")
        walking.add(u)
        acc: set[str] = set()
        for v in succ[u]:
            acc.add(v)
            acc |= descend(v)
        walking.discard(u)
        reach[u] = acc
        return acc

    for nid in node_ids:
        descend(nid)
    return node_ids, reach


def _paths(node: dict[str, Any]) -> list[str]:
    raw = node.get("paths")
    if raw is None:
        meta = node.get("metadata") or {}
        raw = meta.get("paths") or meta.get("likely_touched_paths")
    return [str(p) for p in raw] if isinstance(raw, list) else []


def _cluster(path: str) -> str:
    """A path's cluster key: its top two *directory* segments (filename dropped)."""
    dirs = [seg for seg in path.split("/") if seg][:-1]
    return "/".join(dirs[:2])


def _is_docs(paths: list[str]) -> bool:
    return bool(paths) and all(p.startswith("docs/") or p.endswith(".md") for p in paths)


def _score(a_node: dict[str, Any], b_node: dict[str, Any]) -> tuple[str, str]:
    """Risk + reason for two same-repo, concurrent packages."""
    pa, pb = _paths(a_node), _paths(b_node)
    if not pa or not pb:
        return MEDIUM, "same repo, concurrent, paths undeclared"
    if set(pa) & set(pb):
        return HIGH, "same repo, overlapping file(s)"
    if {_cluster(p) for p in pa} & {_cluster(p) for p in pb}:
        return MEDIUM, "same repo, shared path cluster"
    if _is_docs(pa) != _is_docs(pb):
        return LOW, "same repo, docs-only vs code-only areas"
    return LOW, "same repo, disjoint paths"


def detect_collisions(graph: dict[str, Any]) -> dict[str, Any]:
    """Return ``{"collisions": [...], "parallel_safe": bool}``.

    Each collision is ``{a, b, risk, reason, recommendation}`` and only high/medium
    risks are reported (low-risk pairs are parallel-safe). ``parallel_safe`` is
    True iff no high/medium collision exists.
    """
    node_ids, reach = _reachability(graph)
    by_id = {n["node_id"]: n for n in graph.get("nodes", [])}
    collisions: list[dict[str, Any]] = []
    for a, b in combinations(sorted(node_ids), 2):
        if b in reach.get(a, set()) or a in reach.get(b, set()):
            continue  # already sequenced by a dependency chain
        na, nb = by_id[a], by_id[b]
        if na["repo"] != nb["repo"]:
            continue  # different repos never share files
        risk, reason = _score(na, nb)
        if risk in (HIGH, MEDIUM):
            collisions.append({
                "a": a, "b": b, "risk": risk, "reason": reason,
                "recommendation": f"serialize: run {a} before {b}",
            })
    return {"collisions": collisions, "parallel_safe": not collisions}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="File/path collision detector over an execution graph (dry-run, #536)")
    parser.add_argument("--graph", required=True, help="path to a compiled graph JSON")
    args = parser.parse_args(argv)
    try:
        with open(args.graph, encoding="utf-8") as stream:
            graph = json.load(stream)
        report = detect_collisions(graph)
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as error:
        print(f"collision-detector: {error}", file=sys.stderr)
        return 2
    if report["parallel_safe"]:
        print("parallel-safe: no same-repo concurrent collisions")
        return 0
    for c in report["collisions"]:
        print(f"[{c['risk']}] {c['a']} <> {c['b']}: {c['reason']} -> {c['recommendation']}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
