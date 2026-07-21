import unittest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
import planner_critical_path as pcp


def _graph(nodes, edges):
    """A minimal execution graph valid against the compiler's node/edge shape."""
    return {
        "version": "1.0",
        "graph_id": "g-test",
        "nodes": [{"node_id": n, "type": "task", "description": n,
                   "repo": "demerzel", "status": "pending"} for n in nodes],
        "edges": edges,
    }


class TestCriticalPath(unittest.TestCase):
    def test_simple_chain(self):
        # C depends_on B, B depends_on A  =>  execution order A -> B -> C
        g = _graph(["A", "B", "C"], [
            {"from": "C", "to": "B", "type": "depends_on"},
            {"from": "B", "to": "A", "type": "depends_on"},
        ])
        cp = pcp.critical_path(g)
        self.assertEqual(cp["path"], ["A", "B", "C"])
        self.assertEqual(cp["length"], 3)

    def test_parallel_branches_pick_the_longest(self):
        # ROOT blocks A and X; A blocks B blocks C (len 4);  X blocks Y (len 3).
        g = _graph(["ROOT", "A", "B", "C", "X", "Y"], [
            {"from": "ROOT", "to": "A", "type": "blocks"},
            {"from": "ROOT", "to": "X", "type": "blocks"},
            {"from": "A", "to": "B", "type": "blocks"},
            {"from": "B", "to": "C", "type": "blocks"},
            {"from": "X", "to": "Y", "type": "blocks"},
        ])
        cp = pcp.critical_path(g)
        self.assertEqual(cp["path"], ["ROOT", "A", "B", "C"])
        self.assertEqual(cp["length"], 4)
        self.assertIn("ROOT", cp["bottlenecks"])   # ROOT fans out to two branches

    def test_blocks_and_depends_on_agree_on_direction(self):
        # depends_on and blocks expressing the same B-before-A precedence.
        g_dep = _graph(["A", "B"], [{"from": "A", "to": "B", "type": "depends_on"}])
        g_blk = _graph(["A", "B"], [{"from": "B", "to": "A", "type": "blocks"}])
        self.assertEqual(pcp.critical_path(g_dep)["path"], ["B", "A"])
        self.assertEqual(pcp.critical_path(g_blk)["path"], ["B", "A"])

    def test_review_and_merge_edges_do_not_gate_execution(self):
        # Only a review/merge edge -> no execution precedence -> path length 1.
        g = _graph(["A", "B"], [
            {"from": "A", "to": "B", "type": "reviews"},
            {"from": "A", "to": "B", "type": "should_merge_after"},
        ])
        cp = pcp.critical_path(g)
        self.assertEqual(cp["length"], 1)

    def test_annotate_marks_only_critical_nodes(self):
        g = _graph(["ROOT", "A", "B", "C", "X", "Y"], [
            {"from": "ROOT", "to": "A", "type": "blocks"},
            {"from": "ROOT", "to": "X", "type": "blocks"},
            {"from": "A", "to": "B", "type": "blocks"},
            {"from": "B", "to": "C", "type": "blocks"},
            {"from": "X", "to": "Y", "type": "blocks"},
        ])
        marked = {n["node_id"]: n["critical_path"] for n in pcp.annotate(g)["nodes"]}
        self.assertTrue(all(marked[n] for n in ("ROOT", "A", "B", "C")))
        self.assertFalse(marked["Y"])
        # annotate must not mutate the caller's graph
        self.assertNotIn("critical_path", g["nodes"][0])

    def test_deterministic_tie_break(self):
        # Two equal-length chains -> lexicographically smallest path, stably.
        g = _graph(["A", "B", "M", "N"], [
            {"from": "B", "to": "A", "type": "depends_on"},   # A -> B
            {"from": "N", "to": "M", "type": "depends_on"},   # M -> N
        ])
        self.assertEqual(pcp.critical_path(g)["path"],
                         pcp.critical_path(g)["path"])        # stable
        self.assertEqual(pcp.critical_path(g)["path"], ["A", "B"])


if __name__ == "__main__":
    unittest.main()
