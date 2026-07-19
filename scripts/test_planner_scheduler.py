import unittest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
import planner_scheduler as ps


def _node(nid, repo="demerzel", paths=None):
    n = {"node_id": nid, "type": "task", "description": nid,
         "repo": repo, "status": "pending"}
    if paths is not None:
        n["paths"] = paths
    return n


def _graph(nodes, edges=None):
    return {"version": "1.0", "graph_id": "g", "nodes": nodes, "edges": edges or []}


def _batch_of(waves, level, nid):
    for i, b in enumerate(waves[level]["batches"]):
        if nid in b:
            return i
    return None


class TestScheduler(unittest.TestCase):
    def test_colliding_nodes_are_not_in_the_same_batch(self):
        # A,B,C independent, same repo. A & B touch the same file (collide); C disjoint.
        g = _graph([_node("A", paths=["scripts/x.py"]),
                    _node("B", paths=["scripts/x.py"]),
                    _node("C", paths=["personas/c.yaml"])])
        sched = ps.schedule(g)
        self.assertEqual(len(sched["waves"]), 1)                 # all dependency-ready
        wave0 = sched["waves"][0]["batches"]
        self.assertNotEqual(_batch_of(sched["waves"], 0, "A"),
                            _batch_of(sched["waves"], 0, "B"))   # collision splits them
        self.assertEqual(_batch_of(sched["waves"], 0, "A"),
                         _batch_of(sched["waves"], 0, "C"))      # disjoint -> parallel

    def test_dependency_chain_forms_waves(self):
        # C depends_on B, B depends_on A  =>  three dependency levels.
        g = _graph([_node("A"), _node("B"), _node("C")], [
            {"from": "C", "to": "B", "type": "depends_on"},
            {"from": "B", "to": "A", "type": "depends_on"},
        ])
        sched = ps.schedule(g)
        self.assertEqual([w["batches"] for w in sched["waves"]],
                         [[["A"]], [["B"]], [["C"]]])
        self.assertEqual(sched["execution_order"], ["A", "B", "C"])

    def test_independent_disjoint_nodes_run_in_one_batch(self):
        g = _graph([_node("A", paths=["a/x"]), _node("B", paths=["b/y"]),
                    _node("C", paths=["c/z"])])
        sched = ps.schedule(g)
        self.assertEqual(sched["waves"], [{"level": 0, "batches": [["A", "B", "C"]]}])

    def test_collision_nodes_get_review_stages(self):
        g = _graph([_node("A", paths=["scripts/x.py"]),
                    _node("B", paths=["scripts/x.py"])])
        sched = ps.schedule(g)
        self.assertEqual(sched["review_required"], ["A", "B"])
        self.assertEqual(sched["review_order"], ["A", "B"])

    def test_no_collisions_means_no_review(self):
        g = _graph([_node("A", repo="ga", paths=["s/x"]),
                    _node("B", repo="ix", paths=["s/x"])])   # different repos
        self.assertEqual(ps.schedule(g)["review_required"], [])

    def test_precedence_respected_and_deterministic(self):
        g = _graph([_node("A"), _node("B"), _node("C")], [
            {"from": "A", "to": "B", "type": "blocks"},   # A before B
            {"from": "A", "to": "C", "type": "blocks"},   # A before C
        ])
        first, second = ps.schedule(g), ps.schedule(g)
        self.assertEqual(first, second)                            # deterministic
        order = first["execution_order"]
        self.assertLess(order.index("A"), order.index("B"))        # precedence held
        self.assertLess(order.index("A"), order.index("C"))


if __name__ == "__main__":
    unittest.main()
