#!/usr/bin/env python3
"""Regression guard for the Epic-to-DAG compiler (#533).

Runs under `python -m unittest discover -s scripts` (no pytest). Covers the
acceptance criteria: dry-run compile, machine-readable output, invalid graphs
rejected with clear errors, and tests over simple / parallel / blocked graphs.
The Sprint-0 input is asserted to reproduce the hand-authored reference graph
from #531 (same nodes + edge set + stages).
"""

from __future__ import annotations

import json
from pathlib import Path
import unittest

from epic_to_dag_compiler import CompileError, compile_epic, validate_graph

REPO_ROOT = Path(__file__).resolve().parents[1]
SPRINT0_INPUT = REPO_ROOT / "examples" / "execution-graph-sprint-0-input.json"
SPRINT0_REFERENCE = REPO_ROOT / "examples" / "execution-graph-sprint-0.json"


def _wp(id_, type_="code", repo="demerzel", desc="work", **kinds):
    node = {"id": id_, "type": type_, "repo": repo, "description": desc}
    node.update(kinds)
    return node


def _epic(work_packages, graph_id="test-graph", **extra):
    epic = {"graph_id": graph_id, "work_packages": work_packages}
    epic.update(extra)
    return epic


def _edge_set(graph):
    return {(e["from"], e["to"], e["type"]) for e in graph["edges"]}


class SimpleGraphTests(unittest.TestCase):
    def test_simple_linear_chain(self):
        epic = _epic([
            _wp("#1", depends_on=["#2"]),
            _wp("#2", depends_on=["#3"]),
            _wp("#3"),
        ])
        graph = compile_epic(epic)
        self.assertEqual(graph["version"], "1.0.0")
        self.assertEqual(len(graph["nodes"]), 3)
        self.assertEqual(_edge_set(graph), {("#1", "#2", "depends_on"), ("#2", "#3", "depends_on")})

    def test_output_is_machine_readable_json(self):
        graph = compile_epic(_epic([_wp("#1")]))
        # round-trips as JSON without loss
        self.assertEqual(json.loads(json.dumps(graph))["graph_id"], "test-graph")


class ParallelGraphTests(unittest.TestCase):
    def test_fanout_parallel_branches(self):
        # one root blocks two independent children
        epic = _epic([
            _wp("#root", blocks=["#a", "#b"]),
            _wp("#a"),
            _wp("#b"),
        ])
        graph = compile_epic(epic)
        self.assertEqual(_edge_set(graph),
                         {("#root", "#a", "blocks"), ("#root", "#b", "blocks")})
        # both branches are valid (acyclic, no dangling)
        self.assertTrue(validate_graph(graph))


class BlockedGraphTests(unittest.TestCase):
    def test_blocks_edge_and_blocked_status(self):
        epic = _epic([
            _wp("#up", blocks=["#down"]),
            _wp("#down", status="blocked"),
        ])
        graph = compile_epic(epic)
        self.assertIn(("#up", "#down", "blocks"), _edge_set(graph))
        down = next(n for n in graph["nodes"] if n["node_id"] == "#down")
        self.assertEqual(down["status"], "blocked")


class RejectionTests(unittest.TestCase):
    def test_cycle_is_rejected(self):
        epic = _epic([
            _wp("#1", depends_on=["#2"]),
            _wp("#2", depends_on=["#1"]),
        ])
        with self.assertRaises(CompileError) as ctx:
            compile_epic(epic)
        self.assertIn("cycle", str(ctx.exception).lower())

    def test_dangling_edge_is_rejected(self):
        epic = _epic([_wp("#1", blocks=["#999"])])
        with self.assertRaises(CompileError) as ctx:
            compile_epic(epic)
        self.assertIn("dangling", str(ctx.exception).lower())

    def test_duplicate_node_id_is_rejected(self):
        epic = _epic([_wp("#1"), _wp("#1", desc="dup")])
        with self.assertRaises(CompileError) as ctx:
            compile_epic(epic)
        self.assertIn("duplicate", str(ctx.exception).lower())

    def test_invalid_type_is_rejected(self):
        epic = _epic([_wp("#1", type_="banana")])
        with self.assertRaises(CompileError) as ctx:
            compile_epic(epic)
        self.assertIn("invalid", str(ctx.exception).lower())

    def test_missing_graph_id_is_rejected(self):
        with self.assertRaises(CompileError):
            compile_epic({"work_packages": [_wp("#1")]})


class Sprint0Tests(unittest.TestCase):
    def test_sprint0_reproduces_reference(self):
        with open(SPRINT0_INPUT, "r", encoding="utf-8") as f:
            epic = json.load(f)
        with open(SPRINT0_REFERENCE, "r", encoding="utf-8") as f:
            reference = json.load(f)

        graph = compile_epic(epic)

        self.assertEqual(graph["version"], reference["version"])
        self.assertEqual(graph["graph_id"], reference["graph_id"])
        self.assertEqual(graph["nodes"], reference["nodes"])
        # edges compared as a set — a graph's edge order is not significant
        self.assertEqual(_edge_set(graph), _edge_set(reference))
        self.assertEqual(graph["review_stages"], reference["review_stages"])
        self.assertEqual(graph["merge_stages"], reference["merge_stages"])
        self.assertEqual(graph["metadata"], reference["metadata"])


if __name__ == "__main__":
    unittest.main()
