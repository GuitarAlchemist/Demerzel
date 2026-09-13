import contextlib
import io
import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path

try:
    from scripts import evolution_metrics as em
except ModuleNotFoundError:  # `unittest discover -s scripts` imports top-level tests.
    import evolution_metrics as em


class Repo:
    def __init__(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        self.git("init", "-q")

    def close(self):
        self._tmp.cleanup()

    def git(self, *args, date=None):
        env = dict(os.environ)
        if date:
            env["GIT_AUTHOR_DATE"] = env["GIT_COMMITTER_DATE"] = date
        subprocess.run(["git", "-c", "user.name=t", "-c", "user.email=t@t", "-c", "commit.gpgsign=false", *args],
                       cwd=self.root, env=env, check=True, capture_output=True)

    def write(self, rel, text):
        p = self.root / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text, encoding="utf-8")

    def commit(self, date="2026-09-01T12:00:00+00:00", *rels):
        self.git("add", *(rels or ["-A"]))
        self.git("commit", "-q", "-m", "c", date=date)

    def entry(self, stem, **fields):
        data = {"artifact": "policies/a.yaml",
                "metrics": {"citation_count": 3, "violation_count": 2, "compliance_rate": 0.5,
                            "last_cited": "2026-03-17T20:00:00Z"},
                "assessment": {"effectiveness": {"truth_value": "T"}}}
        data.update(fields)
        rel = f"state/evolution/{stem}.evolution.json"
        self.write(rel, json.dumps(data, indent=2) + "\n")
        return rel


class Fixture(unittest.TestCase):
    def setUp(self):
        self.repo = Repo()
        self.addCleanup(self.repo.close)
        r = self.repo
        r.write("policies/a.yaml", "name: a\nsee: policies/a.yaml\n")  # the artifact names itself
        r.write("docs/one.md", "uses policies/a.yaml\n")
        r.write("docs/two.md", "also policies/a.yaml and policies/a.yaml\n")  # one file, counted once
        r.write("docs/archived/old.md", "policies/a.yaml\n")
        r.write("governance-manifest.json", '["policies/a.yaml"]\n')
        r.write("state/quality-trend/2026-09.jsonl", '{"artifact": "policies/a.yaml"}\n')
        r.write("scripts/tool/main.py", "# scripts/tool/ helper\n")
        r.write("scripts/tool/other.py", "# see scripts/tool/\n")
        r.write("docs/tool.md", "scripts/tool/\n")
        r.commit()
        self.repo.entry("x")
        r.commit("2026-09-02T00:00:00+00:00")

    def load(self, rel):
        return json.loads((self.repo.root / rel).read_text(encoding="utf-8"))


class MeasureTests(Fixture):
    def test_counts_referencing_files_excluding_self_archived_generated_and_state(self):
        entry = self.load("state/evolution/x.evolution.json")
        status, _ = em.update_entry(self.repo.root, entry)
        self.assertEqual(status, em.CHANGED)
        self.assertEqual(entry["metrics"]["citation_count"], 2)  # docs/one.md, docs/two.md
        self.assertEqual(entry["metrics"]["citation_source"], em.CITATION_SOURCE)

    def test_files_inside_a_directory_artifact_are_its_own(self):
        count, _ = em.measure(self.repo.root, ["scripts/tool/"])
        self.assertEqual(count, 1)  # docs/tool.md only

    def test_citation_paths_union_counts_each_file_once(self):
        self.repo.write("docs/both.md", "policies/a.yaml and scripts/tool/\n")
        self.repo.commit("2026-09-03T00:00:00+00:00")
        count, _ = em.measure(self.repo.root, ["policies/a.yaml", "scripts/tool/"])
        self.assertEqual(count, 4)  # one.md, two.md, tool.md, both.md

    def test_last_cited_is_newest_mention_change_in_utc(self):
        self.repo.write("docs/three.md", "policies/a.yaml\n")
        self.repo.commit("2026-09-05T02:30:00+02:00")
        self.repo.write("docs/unrelated.md", "nothing\n")
        self.repo.commit("2026-09-06T00:00:00+00:00")  # later, but no mention change
        entry = self.load("state/evolution/x.evolution.json")
        em.update_entry(self.repo.root, entry)
        self.assertEqual(entry["metrics"]["last_cited"], "2026-09-05T00:30:00Z")

    def test_last_cited_is_newest_across_all_citation_paths(self):
        self.repo.write("docs/later.md", "scripts/tool/\n")
        self.repo.commit("2026-09-07T00:00:00+00:00")
        for paths in (["policies/a.yaml", "scripts/tool/"], ["scripts/tool/", "policies/a.yaml"]):
            with self.subTest(order=paths):
                entry = {"artifact": "z", "citation_paths": paths, "metrics": {}}
                em.update_entry(self.repo.root, entry)
                self.assertEqual(entry["metrics"]["last_cited"], "2026-09-07T00:00:00Z")

    def test_never_mentioned_artifact_gets_zero_and_null_last_cited(self):
        self.repo.write("policies/lonely.yaml", "name: lonely\n")
        self.repo.commit("2026-09-03T00:00:00+00:00")
        entry = {"artifact": "policies/lonely.yaml", "metrics": {"citation_count": 5, "last_cited": "2026-04-29T00:00:00Z"}}
        em.update_entry(self.repo.root, entry)
        self.assertEqual((entry["metrics"]["citation_count"], entry["metrics"]["last_cited"]), (0, None))

    def test_judgment_fields_are_never_touched(self):
        entry = self.load("state/evolution/x.evolution.json")
        em.update_entry(self.repo.root, entry)
        self.assertEqual((entry["metrics"]["violation_count"], entry["metrics"]["compliance_rate"]), (2, 0.5))
        self.assertEqual(entry["assessment"], {"effectiveness": {"truth_value": "T"}})

    def test_unmeasurable_entries_are_left_untouched(self):
        cases = {
            "empty list": {"artifact": "crates/x (ix)", "citation_paths": []},
            "no path": {"artifact": "ml-feedback-loop"},
            "untracked citation path": {"artifact": "y", "citation_paths": ["policies/a.yaml", "docs/gone.md"]},
        }
        for name, entry in cases.items():
            with self.subTest(name):
                entry["metrics"] = {"citation_count": 7}
                before = json.dumps(entry)
                status, note = em.update_entry(self.repo.root, entry)
                self.assertEqual(status, em.UNMEASURABLE)
                self.assertTrue(note)
                self.assertEqual(json.dumps(entry), before)

    def test_citation_paths_override_a_tracked_artifact(self):
        entry = {"artifact": "policies/a.yaml", "citation_paths": ["scripts/tool/"], "metrics": {}}
        em.update_entry(self.repo.root, entry)
        self.assertEqual(entry["metrics"]["citation_count"], 1)


class MainTests(Fixture):
    def run_main(self, *extra):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            code = em.main(["--root", str(self.repo.root), *extra])
        return code, out.getvalue()

    def test_check_reports_without_writing(self):
        rel = self.repo.root / "state/evolution/x.evolution.json"
        before = rel.read_bytes()
        code, out = self.run_main("--check")
        self.assertEqual(code, 1)
        self.assertIn("would update", out)
        self.assertEqual(rel.read_bytes(), before)

    def test_write_then_rerun_is_a_no_op(self):
        rel = self.repo.root / "state/evolution/x.evolution.json"
        self.assertEqual(self.run_main()[0], 0)
        after_first = rel.read_bytes()
        self.assertEqual(json.loads(after_first)["metrics"]["citation_count"], 2)
        code, out = self.run_main("--check")
        self.assertEqual(code, 0)
        self.assertIn("0 changed", out)
        self.assertEqual(rel.read_bytes(), after_first)


if __name__ == "__main__":
    unittest.main()
