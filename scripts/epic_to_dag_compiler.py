#!/usr/bin/env python3
"""Epic-to-DAG compiler prototype (#533, parent #529).

Converts structured epic/story metadata (epic-input.schema.json) into a Planner
execution graph (execution-graph.schema.json). Dry-run: it validates and emits
machine-readable JSON, and never mutates GitHub or repository state.

Pipeline:
  1. validate the epic input against its contract schema;
  2. extract work packages into WorkNodes;
  3. infer DependencyEdges from each package's per-kind edge fields
     (blocks / depends_on / reviews / should_merge_after);
  4. validate the compiled graph — schema-valid, no dangling edges, and acyclic
     (an execution graph is a DAG); invalid graphs are rejected with a clear
     error and no output.

Stdlib + `jsonschema` only. See docs/contracts/execution-graph.schema.json.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import jsonschema

_CONTRACTS = Path(__file__).resolve().parents[1] / "docs" / "contracts"
_GRAPH_SCHEMA_PATH = _CONTRACTS / "execution-graph.schema.json"
_INPUT_SCHEMA_PATH = _CONTRACTS / "epic-input.schema.json"

GRAPH_VERSION = "1.0.0"
# Fixed order so edge inference is deterministic.
_EDGE_KINDS = ("blocks", "depends_on", "reviews", "should_merge_after")


class CompileError(ValueError):
    """Raised when an epic input or the compiled graph is invalid."""


def _load(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def extract_nodes(epic):
    """Extract work packages into WorkNodes (input order preserved)."""
    nodes = []
    for wp in epic.get("work_packages", []):
        node = {
            "node_id": wp["id"],
            "type": wp["type"],
            "description": wp["description"],
            "repo": wp["repo"],
            "status": wp.get("status", "pending"),
        }
        if "evidence" in wp:
            node["evidence"] = wp["evidence"]
        if "metadata" in wp:
            node["metadata"] = wp["metadata"]
        nodes.append(node)
    return nodes


def infer_edges(epic):
    """Infer DependencyEdges from each package's per-kind edge fields."""
    edges = []
    for wp in epic.get("work_packages", []):
        src = wp["id"]
        for kind in _EDGE_KINDS:
            for target in wp.get(kind, []):
                edges.append({"from": src, "to": target, "type": kind})
    return edges


def _find_cycle(node_ids, edges):
    """Return a cycle path (list of node ids) if the graph has one, else None."""
    adjacency = {nid: [] for nid in node_ids}
    for edge in edges:
        adjacency[edge["from"]].append(edge["to"])

    WHITE, GRAY, BLACK = 0, 1, 2
    color = {nid: WHITE for nid in node_ids}
    path = []

    def visit(u):
        color[u] = GRAY
        path.append(u)
        for v in adjacency[u]:
            if color[v] == GRAY:
                return path[path.index(v):] + [v]
            if color[v] == WHITE:
                found = visit(v)
                if found:
                    return found
        color[u] = BLACK
        path.pop()
        return None

    for nid in node_ids:
        if color[nid] == WHITE:
            found = visit(nid)
            if found:
                return found
    return None


def validate_graph(graph):
    """Validate a compiled graph. Raises CompileError with a clear message."""
    schema = _load(_GRAPH_SCHEMA_PATH)
    try:
        jsonschema.validate(graph, schema)
    except jsonschema.exceptions.ValidationError as exc:
        raise CompileError(f"schema validation failed: {exc.message}")

    node_ids = [n["node_id"] for n in graph["nodes"]]
    id_set = set(node_ids)
    if len(id_set) != len(node_ids):
        dupes = sorted({x for x in node_ids if node_ids.count(x) > 1})
        raise CompileError(f"duplicate node_id(s): {', '.join(dupes)}")

    for edge in graph["edges"]:
        for end in ("from", "to"):
            if edge[end] not in id_set:
                raise CompileError(
                    f"dangling edge {edge['from']} -{edge['type']}-> {edge['to']}: "
                    f"references unknown node {edge[end]!r}"
                )

    cycle = _find_cycle(node_ids, graph["edges"])
    if cycle:
        raise CompileError("dependency cycle detected: " + " -> ".join(cycle))

    return True


def compile_epic(epic, validate=True):
    """Compile an epic input dict into an execution-graph dict."""
    input_schema = _load(_INPUT_SCHEMA_PATH)
    try:
        jsonschema.validate(epic, input_schema)
    except jsonschema.exceptions.ValidationError as exc:
        raise CompileError(f"epic input invalid: {exc.message}")

    graph = {
        "version": GRAPH_VERSION,
        "graph_id": epic["graph_id"],
        "nodes": extract_nodes(epic),
        "edges": infer_edges(epic),
    }
    for passthrough in ("review_stages", "merge_stages", "metadata"):
        if passthrough in epic:
            graph[passthrough] = epic[passthrough]

    if validate:
        validate_graph(graph)
    return graph


def main(argv=None):
    parser = argparse.ArgumentParser(description="Epic-to-DAG compiler (dry-run, #533)")
    parser.add_argument("--epic", required=True, help="path to an epic input JSON file")
    parser.add_argument("--out", help="write the graph JSON here (default: stdout — dry-run)")
    args = parser.parse_args(argv)

    try:
        epic = _load(args.epic)
    except (OSError, json.JSONDecodeError) as exc:
        print(json.dumps({"error": str(exc)}), file=sys.stderr)
        return 2

    try:
        graph = compile_epic(epic)
    except CompileError as exc:
        print(json.dumps({"error": str(exc)}), file=sys.stderr)
        return 1

    text = json.dumps(graph, indent=2)
    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(text + "\n")
        print(f"wrote {args.out} ({len(graph['nodes'])} nodes, {len(graph['edges'])} edges)")
    else:
        print(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
