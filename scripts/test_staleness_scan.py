import contextlib
import io
import json
import os
import subprocess
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

try:
    from scripts import staleness_scan as s
except ModuleNotFoundError:  # `unittest discover -s scripts` imports top-level tests.
    import staleness_scan as s

NOW = datetime(2026, 9, 13, tzinfo=timezone.utc)

CATEGORIES = [
    {"category": "conscience_signals", "path": "state/conscience/signals/*.signal.json",
     "max_staleness_days": 3, "priority": "critical", "refresh_action": "Process signal"},
    {"category": "conscience_regrets", "path": "state/conscience/regrets/*.regret.json",
     "max_staleness_days": 7, "priority": "medium", "refresh_action": "Archive or escalate"},
    {"category": "evolution_log", "path": "state/evolution/*.evolution.json",
     "max_staleness_days": 14, "priority": "medium", "refresh_action": "Re-assess"},
    {"category": "intuition_signals", "path": "state/intuition/*.json",
     "max_staleness_days": 7, "priority": "medium", "refresh_action": "Validate"},
    {"category": "pdca_cycles", "path": "state/pdca/*.pdca.json",
     "max_staleness_days": 14, "priority": "high", "refresh_action": "Advance PDCA"},
    {"category": "department_weights", "path": "state/streeling/departments/*.weights.json",
     "max_staleness_days": 30, "priority": "low", "refresh_action": "Research cycle"},
    {"category": "grammar_weights", "path": "state/streeling/departments/*.weights.json",
     "max_staleness_days": 30, "priority": "low", "refresh_action": "Research cycle"},
]


def git(root, *args, date=None):
    env = dict(os.environ)
    if date is not None:
        env["GIT_AUTHOR_DATE"] = env["GIT_COMMITTER_DATE"] = date.isoformat()
    subprocess.run(["git", "-c", "user.name=t", "-c", "user.email=t@t", "-c", "commit.gpgsign=false", *args],
                   cwd=root, env=env, check=True, capture_output=True)


class Repo:
    """A throwaway git repo whose commits carry chosen dates while every file's mtime is 'now'."""

    def __init__(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        git(self.root, "init", "-q")

    def close(self):
        self._tmp.cleanup()

    def write(self, rel, data):
        p = self.root / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(json.dumps(data), encoding="utf-8")
        return rel

    def commit(self, rel, days_ago, base=NOW):
        git(self.root, "add", rel)
        git(self.root, "commit", "-q", "-m", rel, date=base - timedelta(days=days_ago))


class ScanTests(unittest.TestCase):
    def setUp(self):
        self.repo = Repo()
        self.addCleanup(self.repo.close)

    def committed(self, rel, data, days_ago):
        self.repo.write(rel, data)
        self.repo.commit(rel, days_ago)

    def scan(self, categories=CATEGORIES):
        findings, counts = s.scan(self.repo.root, categories, NOW)
        return {f["file"]: f for f in findings}, counts

    def test_terminal_signal_with_outcome_is_not_reported_however_old(self):
        self.committed("state/conscience/signals/a.signal.json", {"outcome": "RESOLVED"}, 178)
        by_file, counts = self.scan()
        self.assertEqual(by_file, {})
        self.assertEqual(counts[s.TERMINAL], 1)

    def test_signal_without_outcome_is_open_work_and_always_critical(self):
        self.committed("state/conscience/signals/b.signal.json", {"outcome": None}, 2)
        # The classify step makes signals critical by rule, not by the category's declared priority.
        cats = [dict(c, priority="low") if c["category"] == "conscience_signals" else c for c in CATEGORIES]
        f = self.scan(cats)[0]["state/conscience/signals/b.signal.json"]
        self.assertEqual((f["lifecycle"], f["stale"], f["priority"]), (s.OPEN_WORK, False, "critical"))

    def test_open_pdca_flagged_closed_pdca_exempt(self):
        self.committed("state/pdca/example-open.pdca.json", {"cycle_phase": "plan"}, 134)
        self.committed("state/pdca/example-closed.pdca.json", {"cycle_phase": "act", "outcome": "adopted"}, 134)
        by_file, counts = self.scan()
        self.assertNotIn("state/pdca/example-closed.pdca.json", by_file)
        f = by_file["state/pdca/example-open.pdca.json"]
        self.assertEqual((f["lifecycle"], f["stale"], f["days"]), (s.OPEN_WORK, True, 134))
        self.assertEqual((counts[s.TERMINAL], counts[s.OPEN_WORK]), (1, 1))

    def test_resolved_regret_exempt_unresolved_regret_measured(self):
        self.committed("state/conscience/regrets/done.regret.json", {"status": "resolved"}, 100)
        self.committed("state/conscience/regrets/live.regret.json", {"status": "open"}, 100)
        by_file, _ = self.scan()
        self.assertEqual(list(by_file), ["state/conscience/regrets/live.regret.json"])
        self.assertEqual(by_file["state/conscience/regrets/live.regret.json"]["lifecycle"], s.OPEN_WORK)

    def test_evolution_log_aged_by_commit_time_not_fresh_mtime(self):
        rel = "state/evolution/x.evolution.json"
        self.committed(rel, {"artifact": "x"}, 45)
        os.utime(self.repo.root / rel)  # a fresh worktree: mtime is now
        f = self.scan()[0][rel]
        self.assertEqual((f["lifecycle"], f["days"], f["source"], f["stale"]), (s.LIVE_STATE, 45, "last commit", True))

    def test_within_threshold_is_measured_but_not_stale(self):
        self.committed("state/evolution/y.evolution.json", {}, 14)
        f = self.scan()[0]["state/evolution/y.evolution.json"]
        self.assertEqual((f["days"], f["stale"], f["priority"]), (14, False, "medium"))

    def test_priority_escalates_past_twice_the_threshold_only(self):
        self.committed("state/evolution/at-2x.evolution.json", {}, 28)
        self.committed("state/evolution/past-2x.evolution.json", {}, 29)
        by_file, _ = self.scan()
        self.assertEqual(by_file["state/evolution/at-2x.evolution.json"]["priority"], "medium")
        self.assertEqual(by_file["state/evolution/past-2x.evolution.json"]["priority"], "critical")

    def test_candidate_intuition_is_open_work_other_status_live_state(self):
        self.committed("state/intuition/c.json", {"status": "candidate"}, 1)
        self.committed("state/intuition/d.json", {"status": "confirmed"}, 1)
        by_file, _ = self.scan()
        self.assertEqual(by_file["state/intuition/c.json"]["lifecycle"], s.OPEN_WORK)
        self.assertEqual(by_file["state/intuition/d.json"]["lifecycle"], s.LIVE_STATE)

    def test_untracked_file_falls_back_to_last_updated(self):
        rel = self.repo.write("state/evolution/new.evolution.json",
                              {"last_updated": (NOW - timedelta(days=20)).isoformat().replace("+00:00", "Z")})
        f = self.scan()[0][rel]
        self.assertEqual((f["days"], f["source"], f["stale"]), (20, "last_updated", True))

    def test_no_commit_and_no_last_updated_is_reported_not_passed(self):
        rel = self.repo.write("state/evolution/orphan.evolution.json", {})
        f = self.scan()[0][rel]
        self.assertIsNone(f["days"])
        self.assertTrue(f["stale"])

    def test_archived_files_are_never_reached(self):
        self.committed("state/pdca/archived/old.pdca.json", {"cycle_phase": "plan"}, 300)
        by_file, counts = self.scan()
        self.assertEqual(by_file, {})
        self.assertEqual(sum(counts.values()), 0)

    def test_file_matched_by_two_categories_is_counted_once(self):
        self.committed("state/streeling/departments/music.weights.json", {}, 40)
        by_file, counts = self.scan()
        self.assertEqual(len(by_file), 1)
        self.assertEqual(sum(counts.values()), 1)

    def test_dormant_category_is_counted_not_reported(self):
        self.committed("state/pdca/open.pdca.json", {"cycle_phase": "plan"}, 134)
        self.committed("state/evolution/x.evolution.json", {}, 45)
        findings, counts = s.scan(self.repo.root, CATEGORIES, NOW, dormant={"pdca_cycles"})
        self.assertEqual([f["file"] for f in findings], ["state/evolution/x.evolution.json"])
        self.assertEqual((counts[s.DORMANT], counts[s.OPEN_WORK], counts[s.LIVE_STATE]), (1, 0, 1))

    def test_produced_category_is_counted_not_aged(self):
        self.committed("state/evolution/stable.evolution.json", {}, 60)
        self.committed("state/pdca/open.pdca.json", {"cycle_phase": "plan"}, 60)
        cats = [dict(c, freshness_source="producer_run") if c["category"] == "evolution_log" else c
                for c in CATEGORIES]
        findings, counts = s.scan(self.repo.root, cats, NOW)
        self.assertEqual([f["file"] for f in findings], ["state/pdca/open.pdca.json"])
        self.assertEqual((counts[s.PRODUCED], counts[s.OPEN_WORK]), (1, 1))

    def test_category_newest_is_the_youngest_file(self):
        self.committed("state/evolution/a.evolution.json", {}, 40)
        self.committed("state/evolution/b.evolution.json", {}, 16)
        findings, _ = s.scan(self.repo.root, CATEGORIES, NOW)
        self.assertEqual(s.category_newest(findings), {"evolution_log": 16})


class MainTests(unittest.TestCase):
    # main() reads the real clock, so these commits are dated from it, not from NOW.
    def setUp(self):
        self.repo = Repo()
        self.addCleanup(self.repo.close)
        self.now = datetime.now(timezone.utc)
        policy = self.repo.write("policy.json", {"artifact_categories": CATEGORIES})  # JSON is YAML
        self.repo.commit(policy, 0, self.now)
        self.policy = policy

    def run_main(self, root, *extra):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            code = s.main(["--root", str(root), "--policy", self.policy, *extra])
        return code, out.getvalue()

    def test_stale_artifact_warns_and_strict_fails(self):
        rel = "state/pdca/open.pdca.json"
        self.repo.write(rel, {"cycle_phase": "plan"})
        self.repo.commit(rel, 400, self.now)
        code, out = self.run_main(self.repo.root)
        self.assertEqual(code, 0)
        self.assertIn(f"::warning file={rel}::stale open_work (pdca_cycles)", out)
        self.assertIn("1 stale", out)
        self.assertEqual(self.run_main(self.repo.root, "--strict")[0], 1)

    def test_dormant_policy_entry_silences_its_category(self):
        rel = "state/pdca/open.pdca.json"
        self.repo.write(rel, {"cycle_phase": "plan"})
        self.repo.commit(rel, 400, self.now)
        policy = self.repo.write("dormant.json", {"artifact_categories": CATEGORIES,
                                                  "dormant_categories": {"categories": [{"category": "pdca_cycles"}]}})
        self.repo.commit(policy, 0, self.now)
        self.policy = policy
        code, out = self.run_main(self.repo.root, "--strict")
        self.assertEqual(code, 0)
        self.assertNotIn("::warning", out)
        self.assertIn("1 dormant (not reported), 0 produced", out)
        self.assertIn("; 0 stale", out)

    def test_produced_category_names_its_guard(self):
        cats = [dict(c, freshness_source="producer_run", freshness_guard="guard.yml")
                if c["category"] == "evolution_log" else c for c in CATEGORIES]
        policy = self.repo.write("produced.json", {"artifact_categories": cats})
        self.repo.commit(policy, 0, self.now)
        self.policy = policy
        code, out = self.run_main(self.repo.root)
        self.assertEqual(code, 0)
        self.assertIn("evolution_log: freshness is the producer run — see guard.yml", out)

    def test_misspelt_dormant_category_is_an_error_not_a_silent_no_op(self):
        policy = self.repo.write("typo.json", {"artifact_categories": CATEGORIES,
                                               "dormant_categories": {"categories": [{"category": "pdca_cycle"}]}})
        self.repo.commit(policy, 0, self.now)
        self.policy = policy
        code, out = self.run_main(self.repo.root)
        self.assertEqual(code, 2)
        self.assertIn("pdca_cycle", out)

    def test_nothing_stale_passes_strict(self):
        rel = "state/pdca/fresh.pdca.json"
        self.repo.write(rel, {"cycle_phase": "plan"})
        self.repo.commit(rel, 0, self.now)
        code, out = self.run_main(self.repo.root, "--strict")
        self.assertEqual(code, 0)
        self.assertNotIn("::warning", out)

    def test_shallow_clone_refuses_instead_of_reporting_everything_fresh(self):
        rel = "state/pdca/open.pdca.json"
        self.repo.write(rel, {"cycle_phase": "plan"})
        self.repo.commit(rel, 400, self.now)
        self.repo.write("README", {})
        self.repo.commit("README", 0, self.now)
        with tempfile.TemporaryDirectory() as tmp:
            clone = Path(tmp) / "clone"
            subprocess.run(["git", "clone", "-q", "--depth", "1", self.repo.root.as_uri(), str(clone)],
                           check=True, capture_output=True)
            code, out = self.run_main(clone)
        self.assertEqual(code, 2)
        self.assertIn("shallow clone", out)


if __name__ == "__main__":
    unittest.main()
