#!/usr/bin/env python3
"""Critical-path analysis over a compiled execution graph (Planner #535).

Consumes an execution graph as emitted by ``epic_to_dag_compiler.compile_epic``
(``{nodes, edges}``) and computes the longest precedence chain — the sequence of
work packages that sets the minimum completion time for the epic.

Precedence semantics (only execution-gating edges count):
  - ``depends_on`` A->B : B must finish before A  (precedence B -> A)
  - ``blocks``      A->B : A must finish before B  (precedence A -> B)
  - ``reviews`` / ``should_merge_after`` : review/merge ordering, NOT execution
    gates, so they are ignored here.

Pure and deterministic (ties broken lexicographically); it never mutates its
input. The graph is assumed acyclic (the compiler's ``validate_graph`` guarantees
it); a defensive cycle check still fails closed rather than recursing forever.

The Planner only *recommends* — this emits analysis, never commands (#529
guardrail). Run as a CLI for a dry-run report.
"""
from __future__ import annotations

import argparse
import json
import sys
from typing import Any


# Map an edge to its (predecessor, successor) execution-precedence pair, or None
# when the edge does not gate execution.
_PRECEDENCE = {
    "depends_on": lambda e: (e["to"], e["from"]),
    "blocks": lambda e: (e["from"], e["to"]),
}


def _precedence(graph: dict[str, Any]):
    """Return (node_ids, successors, in_degree) for the execution-precedence DAG."""
    node_ids = [n["node_id"] for n in graph.get("nodes", [])]
    known = set(node_ids)
    succ: dict[str, list[str]] = {nid: [] for nid in node_ids}
    indeg: dict[str, int] = {nid: 0 for nid in node_ids}
    for edge in graph.get("edges", []):
        convert = _PRECEDENCE.get(edge.get("type"))
        if convert is None:
            continue
        pred, node = convert(edge)
        if pred in known and node in known:
            succ[pred].append(node)
            indeg[node] += 1
    return node_ids, succ, indeg


def critical_path(graph: dict[str, Any]) -> dict[str, Any]:
    """Longest execution-precedence chain through the graph.

    Returns ``{"path": [node_id, ...], "length": int, "bottlenecks": [...]}``.
    ``bottlenecks`` are critical-path nodes that fan out to (or in from) more than
    one package — the points where the schedule is most sensitive.
    """
    node_ids, succ, indeg = _precedence(graph)
    memo: dict[str, list[str]] = {}
    on_stack: set[str] = set()

    def longest_from(node: str) -> list[str]:
        if node in memo:
            return memo[node]
        if node in on_stack:  # defensive: a cycle slipped past validation
            raise ValueError(f"cycle through node {node!r}")
        on_stack.add(node)
        best: list[str] = [node]
        for nxt in succ[node]:
            candidate = [node] + longest_from(nxt)
            if len(candidate) > len(best) or (
                    len(candidate) == len(best) and candidate < best):
                best = candidate
        on_stack.discard(node)
        memo[node] = best
        return best

    best_path: list[str] = []
    for nid in node_ids:
        chain = longest_from(nid)
        if len(chain) > len(best_path) or (
                len(chain) == len(best_path) and chain < best_path):
            best_path = chain

    bottlenecks = [n for n in best_path if len(succ[n]) > 1 or indeg[n] > 1]
    return {"path": best_path, "length": len(best_path), "bottlenecks": bottlenecks}


def annotate(graph: dict[str, Any]) -> dict[str, Any]:
    """Return a copy of ``graph`` with each node stamped ``critical_path: bool``."""
    on_path = set(critical_path(graph)["path"])
    nodes = [{**n, "critical_path": n["node_id"] in on_path}
             for n in graph.get("nodes", [])]
    return {**graph, "nodes": nodes}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Critical-path analysis over an execution graph (dry-run, #535)")
    parser.add_argument("--graph", required=True, help="path to a compiled graph JSON")
    parser.add_argument("--out", help="write annotated graph here (default: report to stdout)")
    args = parser.parse_args(argv)
    try:
        with open(args.graph, encoding="utf-8") as stream:
            graph = json.load(stream)
        result = critical_path(graph)
        if args.out:
            with open(args.out, "w", encoding="utf-8") as stream:
                json.dump(annotate(graph), stream, indent=2)
                stream.write("\n")
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as error:
        print(f"critical-path: {error}", file=sys.stderr)
        return 2
    print(f"critical path ({result['length']}): {' -> '.join(result['path'])}")
    if result["bottlenecks"]:
        print(f"bottlenecks: {', '.join(result['bottlenecks'])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
