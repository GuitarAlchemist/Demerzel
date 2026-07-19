import unittest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
import planner_collision_detector as pcd


def _node(nid, repo="demerzel", paths=None):
    n = {"node_id": nid, "type": "task", "description": nid,
         "repo": repo, "status": "pending"}
    if paths is not None:
        n["paths"] = paths
    return n


def _graph(nodes, edges=None):
    return {"version": "1.0", "graph_id": "g", "nodes": nodes, "edges": edges or []}


class TestCollisionDetector(unittest.TestCase):
    def test_same_repo_same_file_is_high(self):
        g = _graph([_node("A", paths=["scripts/x.py"]),
                    _node("B", paths=["scripts/x.py"])])
        report = pcd.detect_collisions(g)
        hit = next(c for c in report["collisions"] if {c["a"], c["b"]} == {"A", "B"})
        self.assertEqual(hit["risk"], "high")
        self.assertFalse(report["parallel_safe"])

    def test_same_cluster_different_files_is_medium(self):
        g = _graph([_node("A", paths=["scripts/one.py"]),
                    _node("B", paths=["scripts/two.py"])])
        report = pcd.detect_collisions(g)
        self.assertEqual(report["collisions"][0]["risk"], "medium")

    def test_disjoint_paths_same_repo_are_parallel_safe(self):
        g = _graph([_node("A", paths=["scripts/one.py"]),
                    _node("B", paths=["personas/two.yaml"])])
        self.assertTrue(pcd.detect_collisions(g)["parallel_safe"])

    def test_different_repos_never_collide(self):
        g = _graph([_node("A", repo="ga", paths=["src/x.cs"]),
                    _node("B", repo="ix", paths=["src/x.cs"])])
        self.assertTrue(pcd.detect_collisions(g)["parallel_safe"])

    def test_sequenced_packages_are_not_flagged(self):
        # B depends_on A -> A precedes B -> they never run in parallel.
        g = _graph([_node("A", paths=["scripts/x.py"]),
                    _node("B", paths=["scripts/x.py"])],
                   [{"from": "B", "to": "A", "type": "depends_on"}])
        self.assertTrue(pcd.detect_collisions(g)["parallel_safe"])

    def test_transitively_ordered_not_flagged(self):
        # A -> B -> C via blocks; A and C are transitively sequenced.
        g = _graph([_node("A", paths=["scripts/x.py"]),
                    _node("B", paths=["scripts/y.py"]),
                    _node("C", paths=["scripts/x.py"])],
                   [{"from": "A", "to": "B", "type": "blocks"},
                    {"from": "B", "to": "C", "type": "blocks"}])
        pairs = {frozenset((c["a"], c["b"])) for c in pcd.detect_collisions(g)["collisions"]}
        self.assertNotIn(frozenset(("A", "C")), pairs)

    def test_undeclared_paths_fail_safe_to_medium(self):
        g = _graph([_node("A"), _node("B")])   # same repo, no paths, concurrent
        report = pcd.detect_collisions(g)
        self.assertEqual(report["collisions"][0]["risk"], "medium")
        self.assertIn("undeclared", report["collisions"][0]["reason"])

    def test_docs_vs_code_areas_are_low(self):
        g = _graph([_node("A", paths=["docs/a.md"]),
                    _node("B", paths=["scripts/b.py"])])
        self.assertTrue(pcd.detect_collisions(g)["parallel_safe"])

    def test_review_merge_edges_do_not_sequence(self):
        # reviews/should_merge_after are not execution gates -> still concurrent.
        g = _graph([_node("A", paths=["scripts/x.py"]),
                    _node("B", paths=["scripts/x.py"])],
                   [{"from": "A", "to": "B", "type": "reviews"}])
        self.assertFalse(pcd.detect_collisions(g)["parallel_safe"])


if __name__ == "__main__":
    unittest.main()
