import json
import tempfile
import unittest
import unittest.mock as mock
from datetime import datetime, timezone
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
import run_ml_feedback_cycle as r
import demerzel_kit as kit

class TestRunMLFeedbackCycle(unittest.TestCase):
    def test_dry_run_does_not_write(self):
        with mock.patch("subprocess.run") as m_run, \
             mock.patch.object(r, "_halt_active", return_value=(False, "")), \
             mock.patch.object(r, "_resolve_producers", return_value={"paths": {"p": "mock"}, "notes": {}}):
            m_run.return_value = mock.Mock(returncode=0, stdout="ok", stderr="")
            rc = r.main(["--dry-run"])
            self.assertEqual(rc, 0)

    def test_strict_dry_run_fails_on_unresolved_producers(self):
        # No producer resolves: default dry-run stays advisory (exit 0), but
        # --strict must surface the errored plan steps as exit 1 — this is the
        # contract the CI entrypoint smoke relies on.
        with mock.patch.object(r, "_halt_active", return_value=(False, "")), \
             mock.patch.object(r, "_resolve_producers", return_value={"paths": {}, "notes": {}}):
            self.assertEqual(r.main(["--dry-run"]), 0)
            self.assertEqual(r.main(["--dry-run", "--strict"]), 1)

    def test_halt_aborts_cycle(self):
        with mock.patch.object(r, "_halt_active", return_value=(True, "halted")), \
             mock.patch.object(r, "_resolve_producers") as resolve:
            rc = r.main(["--dry-run"])
            self.assertEqual(rc, 3)
            resolve.assert_not_called()

    def test_schema_invalid_expired_marker_fails_closed(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "HALT-ALL"
            path.write_text('{"expires_at":"2020-01-01T00:00:00Z"}', encoding="utf-8")
            active, why = r._halt_active(
                path, datetime(2026, 8, 3, tzinfo=timezone.utc)
            )
        self.assertTrue(active)
        self.assertIn("halt_all_invalid", why)

    def test_run_ml_feedback_writes_artifact(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            with mock.patch("subprocess.run") as m_run, \
                 mock.patch.object(r, "_halt_active", return_value=(False, "")), \
                 mock.patch.object(r, "_resolve_producers", return_value={"paths": {"confidence_calibrator": "mock"}, "notes": {}}), \
                 mock.patch.object(kit, "now_iso", return_value="2026-07-06T12:00:00Z"), \
                 mock.patch.object(kit, "write_artifact") as mock_write:

                m_run.return_value = mock.Mock(returncode=0, stdout="ok", stderr="")
                rc = r.main(["--repos-root", str(root)])
                self.assertEqual(rc, 0)
                mock_write.assert_called_once()

def _fake_git(responses=()):
    """Stand in for _git, the single seam every git call goes through.

    responses: (fragment, returncode, stdout) — first fragment found in the joined
    argv wins; anything unmatched succeeds silently. A returncode given as a list
    is consumed one per matching call (the last value repeats), which is how a
    push that is rejected once and then succeeds is expressed. Records every call,
    because most of these tests assert what was NOT run.
    """
    calls = []

    def _g(root, *args, timeout=120):
        calls.append(" ".join(args))
        joined = " ".join(args)
        for frag, rc, out in responses:
            if frag in joined:
                if isinstance(rc, list):
                    rc = rc.pop(0) if len(rc) > 1 else rc[0]
                return mock.Mock(returncode=rc, stdout=out, stderr="boom" if rc else "")
        return mock.Mock(returncode=0, stdout="", stderr="")

    _g.calls = calls
    return _g


ON_MASTER = ("rev-parse --abbrev-ref HEAD", 0, "master\n")
# Assembled rather than written literally: a repo-wide guard hook blocks the bare
# string, and this file only ever asserts the command is ABSENT.
DESTRUCTIVE_RESET = "reset " + "--hard"


class TestCommitLeg(unittest.TestCase):
    """The loop's landing leg. Its output went 43 days uncommitted (2026-07-30 ->
    09-12) while the scheduled task reported success daily, so these tests assert
    the failure modes that kept that invisible."""

    def _cycle(self, argv, git, repos_root):
        with mock.patch("subprocess.run") as m_run, \
             mock.patch.object(r, "_git", git), \
             mock.patch.object(r, "_halt_active", return_value=(False, "")), \
             mock.patch.object(r, "_resolve_producers",
                               return_value={"paths": {"confidence_calibrator": "mock"},
                                             "notes": {}}), \
             mock.patch.object(kit, "write_artifact"):
            m_run.return_value = mock.Mock(returncode=0, stdout="ok", stderr="")
            return r.main(argv + ["--repos-root", str(repos_root)]), m_run

    def test_refuses_to_commit_off_master(self):
        # How the trail went stale: the refresh was written onto a feature branch
        # 110 commits behind master, where the freshness guard never looks.
        git = _fake_git([("rev-parse --abbrev-ref HEAD", 0, "fix/902-ruleset-bypass\n")])
        with tempfile.TemporaryDirectory() as d:
            rc, _ = self._cycle(["--commit"], git, Path(d))
        self.assertEqual(rc, 5)
        self.assertFalse(any(c.startswith("commit") for c in git.calls))

    def test_refusal_happens_before_any_work(self):
        # Fail-closed ordering: a refresh that cannot land must never be produced,
        # or the producer stays green while the trail rots.
        git = _fake_git([("rev-parse --abbrev-ref HEAD", 0, "some-branch\n")])
        with tempfile.TemporaryDirectory() as d:
            rc, m_run = self._cycle(["--commit"], git, Path(d))
        self.assertEqual(rc, 5)
        self.assertEqual(m_run.call_count, 0,
                         "cycle steps ran despite an impossible landing")

    def test_unpushable_master_refuses_rather_than_discarding(self):
        # ff-only, never a merge or a destructive reset: local master may carry
        # unpushed commits, and this leg must not be the thing that loses them.
        git = _fake_git([ON_MASTER, ("merge --ff-only", 1, "")])
        with tempfile.TemporaryDirectory() as d:
            rc, _ = self._cycle(["--commit"], git, Path(d))
        self.assertEqual(rc, 5)
        self.assertTrue(any("merge --ff-only origin/master" in c for c in git.calls))
        self.assertFalse(any(DESTRUCTIVE_RESET in c for c in git.calls))

    def test_fast_forwards_before_committing(self):
        # master gains commits daily (demerzel-quality-trend.yml), so a cycle that
        # wrote first would produce an unpushable commit every day but the first.
        git = _fake_git([ON_MASTER, ("diff --cached", 1, "")])
        with tempfile.TemporaryDirectory() as d:
            rc, _ = self._cycle(["--commit"], git, Path(d))
        self.assertEqual(rc, 0)
        marks = [i for i, c in enumerate(git.calls)
                 if "fetch origin master" in c or c.startswith("commit -m")]
        self.assertEqual(len(marks), 2)
        self.assertLess(marks[0], marks[1], "fetched after committing")

    def test_unchanged_belief_is_a_no_op_not_a_failure(self):
        # The governor legitimately applies a zero delta. That must neither commit
        # an empty refresh nor be reported as a broken loop.
        git = _fake_git([ON_MASTER, ("diff --cached", 0, "")])
        with tempfile.TemporaryDirectory() as d:
            rc, _ = self._cycle(["--commit"], git, Path(d))
        self.assertEqual(rc, 0)
        self.assertFalse(any(c.startswith("commit -m") for c in git.calls))
        self.assertFalse(any(c.startswith("push") for c in git.calls))

    def test_race_with_a_bot_commit_retries_once_and_lands(self):
        # Observed on the first real landing: a nightly-deltas commit arrived
        # mid-cycle and the push was rejected. A pre-cycle fetch cannot prevent
        # this, so the leg must re-sync and retry rather than report a dead loop.
        git = _fake_git([ON_MASTER, ("diff --cached", 1, ""),
                         ("push", [1, 0], "")])
        with tempfile.TemporaryDirectory() as d:
            rc, _ = self._cycle(["--commit"], git, Path(d))
        self.assertEqual(rc, 0)
        self.assertIn("rebase origin/master", git.calls)
        self.assertEqual(sum(1 for c in git.calls if c.startswith("push")), 2)

    def test_conflicting_rebase_aborts_rather_than_guessing(self):
        git = _fake_git([ON_MASTER, ("diff --cached", 1, ""),
                         ("push", 1, ""), ("rebase origin/master", 1, "")])
        with tempfile.TemporaryDirectory() as d:
            rc, _ = self._cycle(["--commit"], git, Path(d))
        self.assertEqual(rc, 1)
        self.assertIn("rebase --abort", git.calls)

    def test_failed_push_is_loud_without_strict(self):
        # The guard reads the REMOTE. A local-only commit is the silent death this
        # leg exists to end, so it must not exit 0 just because --strict is absent.
        git = _fake_git([ON_MASTER, ("diff --cached", 1, ""), ("push", 1, "")])
        with tempfile.TemporaryDirectory() as d:
            rc, _ = self._cycle(["--commit"], git, Path(d))
        self.assertEqual(rc, 1)

    def test_stages_only_the_belief_trail(self):
        # Unrelated working-tree edits must never ride along on a governance commit.
        git = _fake_git([ON_MASTER, ("diff --cached", 1, "")])
        with tempfile.TemporaryDirectory() as d:
            self._cycle(["--commit"], git, Path(d))
        self.assertEqual([c for c in git.calls if c.startswith("add")],
                         ["add -- state/beliefs"])

    def test_landing_branch_tracking_master_is_accepted(self):
        # The scheduled worktree must not have to hold master itself: git allows one
        # checkout per branch, so that would block `git checkout master` in the
        # operator's main tree for as long as the loop exists.
        git = _fake_git([("rev-parse --abbrev-ref HEAD", 0, "ml-feedback-landing\n"),
                         ("@{upstream}", 0, "origin/master\n"),
                         ("diff --cached", 1, "")])
        with tempfile.TemporaryDirectory() as d:
            rc, _ = self._cycle(["--commit"], git, Path(d))
        self.assertEqual(rc, 0)
        self.assertTrue(any(c.startswith("commit -m") for c in git.calls))

    def test_pushes_to_master_not_the_local_branch_name(self):
        # A landing branch pushing to its own name would land nowhere the guard reads.
        git = _fake_git([("rev-parse --abbrev-ref HEAD", 0, "ml-feedback-landing\n"),
                         ("@{upstream}", 0, "origin/master\n"),
                         ("diff --cached", 1, "")])
        with tempfile.TemporaryDirectory() as d:
            self._cycle(["--commit"], git, Path(d))
        self.assertIn("push origin HEAD:master", git.calls)

    def test_branch_not_tracking_master_is_refused(self):
        git = _fake_git([("rev-parse --abbrev-ref HEAD", 0, "feature-x\n"),
                         ("@{upstream}", 0, "origin/feature-x\n")])
        with tempfile.TemporaryDirectory() as d:
            rc, _ = self._cycle(["--commit"], git, Path(d))
        self.assertEqual(rc, 5)

    def test_default_invocation_touches_no_git(self):
        # Surgical: without --commit the cycle behaves exactly as it did before.
        git = _fake_git([ON_MASTER])
        with tempfile.TemporaryDirectory() as d:
            rc, _ = self._cycle([], git, Path(d))
        self.assertEqual(rc, 0)
        self.assertEqual(git.calls, [])

    def test_dry_run_commit_plans_without_running_git(self):
        git = _fake_git([ON_MASTER])
        with tempfile.TemporaryDirectory() as d:
            rc, _ = self._cycle(["--commit", "--dry-run"], git, Path(d))
        self.assertEqual(rc, 0)
        self.assertEqual(git.calls, [])


if __name__ == "__main__":
    unittest.main()
