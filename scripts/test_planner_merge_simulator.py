import unittest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
import planner_merge_simulator as pms


def _node(nid, status="pending", repo="demerzel", paths=None, evidence=None):
    n = {"node_id": nid, "type": "task", "description": nid,
         "repo": repo, "status": status}
    if paths is not None:
        n["paths"] = paths
    if evidence is not None:
        n["evidence"] = evidence
    return n


def _graph(nodes, edges=None):
    return {"version": "1.0", "graph_id": "g", "nodes": nodes, "edges": edges or []}


class TestMergeOrder(unittest.TestCase):
    def test_merge_order_respects_should_merge_after(self):
        # B should_merge_after A  =>  A merges before B.
        g = _graph([_node("A"), _node("B")],
                   [{"from": "B", "to": "A", "type": "should_merge_after"}])
        order = pms.merge_order(g)
        self.assertLess(order.index("A"), order.index("B"))

    def test_merge_order_deterministic(self):
        g = _graph([_node("A"), _node("B"), _node("C")],
                   [{"from": "C", "to": "A", "type": "should_merge_after"}])
        self.assertEqual(pms.merge_order(g), pms.merge_order(g))


class TestSimulate(unittest.TestCase):
    def test_blocked_when_dependency_not_done(self):
        g = _graph([_node("A", status="pending"), _node("B", status="pending")],
                   [{"from": "B", "to": "A", "type": "depends_on"}])
        st = pms.simulate(g)
        self.assertEqual(st["A"], "ready")     # no deps, not done
        self.assertEqual(st["B"], "blocked")   # dep A not done

    def test_ready_when_dependency_done(self):
        g = _graph([_node("A", status="done"), _node("B", status="pending")],
                   [{"from": "B", "to": "A", "type": "depends_on"}])
        self.assertEqual(pms.simulate(g)["B"], "ready")

    def test_mergeable_when_done_and_no_review(self):
        g = _graph([_node("A", status="done", paths=["a/x"])])
        self.assertEqual(pms.simulate(g)["A"], "mergeable")

    def test_in_review_when_done_and_colliding(self):
        g = _graph([_node("A", status="done", paths=["scripts/x.py"]),
                    _node("B", status="done", paths=["scripts/x.py"])])
        st = pms.simulate(g)
        self.assertEqual(st["A"], "in-review")
        self.assertEqual(st["B"], "in-review")


class TestPlannerReport(unittest.TestCase):
    def test_report_has_all_sections_and_is_deterministic(self):
        g = _graph([_node("A", status="done", evidence=["pr#1"], paths=["docs/a.md"]),
                    _node("B", status="done", paths=["scripts/x.py"]),
                    _node("C", status="done", paths=["scripts/x.py"])])
        r = pms.plan(g)
        for key in ("merge_order", "states", "summary", "assumptions",
                    "risks", "evidence", "next_actions"):
            self.assertIn(key, r)
        self.assertEqual(r["evidence"]["A"], ["pr#1"])         # evidence refs surfaced
        self.assertEqual(r["summary"]["mergeable"], 1)          # A
        self.assertEqual(r["summary"]["in-review"], 2)          # B, C collide
        self.assertEqual(sorted(r["risks"]), ["B", "C"])
        self.assertTrue(any("resolve review" in a for a in r["next_actions"]))
        self.assertEqual(pms.plan(g), pms.plan(g))             # deterministic


if __name__ == "__main__":
    unittest.main()
