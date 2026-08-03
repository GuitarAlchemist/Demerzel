#!/usr/bin/env python3
"""Tests for Gaia slice 1 — deterministic same-worktree collision detection.

Spec: docs/superpowers/specs/2026-07-30-gaia-semantic-bus-design.md

These use **real git repositories** in temporary directories rather than a faked
git. The whole discriminator is "is this path uncommitted, in this physical
worktree, right now" — a stubbed git would test the stub and prove nothing about
the only question slice 1 asks.

Test order follows the spec's build order: the silence clause first. Branch-level
overlap on this machine measures 58%, so a regression that makes committed
divergence warn does not degrade the signal, it deletes it.
"""

from __future__ import annotations

import json
import os
import sqlite3
import subprocess
import sys
import tempfile
import threading
import time
import unittest
import unittest.mock
from pathlib import Path

try:
    from scripts import gaia_bus
except ModuleNotFoundError:
    import gaia_bus


# ---------------------------------------------------------------- fixtures


def git(cwd, *args):
    result = subprocess.run(["git", "-C", str(cwd), *args],
                            capture_output=True, text=True, check=False)
    if result.returncode != 0:
        raise AssertionError(f"git {' '.join(args)} failed: {result.stderr}")
    return result.stdout.strip()


class Clock:
    """Explicit time. No test may depend on the wall clock."""

    def __init__(self, start=1_000_000.0):
        self.t = start

    def __call__(self):
        return self.t

    def advance(self, seconds):
        self.t += seconds


class RepoFixture:
    """A real git repo with one committed file, plus optional linked worktrees."""

    FILE = "scripts/run_afk_cycle.py"

    def __init__(self, stack, name="demerzel"):
        self.root = Path(tempfile.mkdtemp(prefix=f"gaia-{name}-"))
        stack(self._cleanup)
        git(self.root, "init", "-q", "-b", "master")
        git(self.root, "config", "user.email", "gaia@test.local")
        git(self.root, "config", "user.name", "Gaia Test")
        # A remote is how repo identity is derived; without one, identity falls
        # back to the directory name, which differs per worktree.
        git(self.root, "remote", "add", "origin",
            f"https://github.com/GuitarAlchemist/{name}.git")
        target = self.root / self.FILE
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text("print('original')\n", encoding="utf-8")
        git(self.root, "add", "-A")
        git(self.root, "commit", "-qm", "initial")
        self._worktrees = []

    def worktree(self, slug):
        """A second physical checkout of the same repo, as `git worktree add`."""
        path = Path(tempfile.mkdtemp(prefix=f"gaia-wt-{slug}-"))
        path.rmdir()
        git(self.root, "worktree", "add", "-q", "-b", slug, str(path))
        self._worktrees.append(path)
        return path

    def dirty(self, tree=None, text="print('edited')\n"):
        """Leave uncommitted edits, the way a session mid-work does."""
        (Path(tree or self.root) / self.FILE).write_text(text, encoding="utf-8")

    def commit(self, tree=None, message="edit"):
        tree = Path(tree or self.root)
        git(tree, "add", "-A")
        git(tree, "commit", "-qm", message)

    def _cleanup(self):
        import shutil
        for path in [*self._worktrees, self.root]:
            shutil.rmtree(path, ignore_errors=True)


class GaiaTestCase(unittest.TestCase):
    def setUp(self):
        self.clock = Clock()
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.store_path = Path(directory.name) / "gaia.sqlite3"
        environment = unittest.mock.patch.dict(
            os.environ,
            {"GALACTIC_CLAIMS_PATH": str(Path(directory.name) / "claims.jsonl")})
        environment.start()
        self.addCleanup(environment.stop)
        self.store = gaia_bus.Store(self.store_path, now=self.clock)
        self.addCleanup(self.store.close)

    def repo(self, name="demerzel"):
        return RepoFixture(self.addCleanup, name)

    def check(self, tree, session, lane, path=None):
        """A session's PreToolUse check-and-claim on the standard file."""
        target = Path(tree) / (path or RepoFixture.FILE)
        return self.store.check_and_claim(
            gaia_bus.identify(target), session=session, lane=lane)


# ------------------------------------------ 1. the silence clause (build first)


class TestCommittedDivergenceIsSilent(GaiaTestCase):
    """Guard #3, and the spec's second tracer-bullet clause.

    Measured branch-level overlap on this machine is 58%. Warning on it fires on
    the majority of edits and trains the reader to ignore Gaia entirely, so
    silence here is what keeps every other warning readable.
    """

    def test_the_same_path_committed_on_divergent_branches_is_silent(self):
        """The spec's second tracer-bullet clause.

        An earlier version of this test asserted silence while session A never
        claimed anything at all -- so it passed unconditionally, including
        against an implementation that warns loudly on committed divergence.
        Silence has to be observed against a LIVE HOLDER or it proves nothing,
        which is why the precondition below is asserted rather than assumed.

        B's tree is left dirty on purpose: it is what makes this test die if the
        worktree axis is ever dropped from the holder query.
        """
        repo = self.repo()
        other = repo.worktree("issue-873-governor")

        self.store.heartbeat("session-A")
        self.check(other, "session-A", "issue-873-governor")
        repo.dirty(other)
        self.store.confirm(gaia_bus.identify(Path(other) / RepoFixture.FILE),
                           "session-A", "issue-873-governor")
        repo.commit(other)                      # A's work is committed on its branch

        holders = [c["session"] for c in self.store.claims()]
        self.assertIn("session-A", holders,
                      "precondition: A must actually hold a claim, or this test "
                      "asserts silence against an empty store and cannot fail")

        repo.dirty(repo.root)                   # B is mid-edit in the primary tree
        self.assertIsNone(self.check(repo.root, "session-B", "issue-863"),
                          "committed divergence must be git's problem, at merge")

    def test_a_holder_who_commits_stops_colliding(self):
        """Same physical worktree, but the holder's edits landed in a commit.

        Nothing can be silently overwritten any more -- the work is durable and
        git will speak up at merge. The stale claim must be swept, not warned on,
        or every finished lane poisons the file for the rest of the day.
        """
        repo = self.repo()
        self.store.heartbeat("session-A")
        self.assertIsNone(self.check(repo.root, "session-A", "issue-873"))
        repo.dirty(repo.root)
        self.store.confirm(gaia_bus.identify(repo.root / RepoFixture.FILE), "session-A")
        repo.commit(repo.root)                  # A commits -- path is clean again

        self.clock.advance(60)
        self.assertIsNone(self.check(repo.root, "session-B", "issue-863"))

    def test_dirty_in_a_different_worktree_is_silent(self):
        """Two dirty copies in separate trees are separate physical files.

        Neither can overwrite the other; git reconciles them at merge. This was
        the correction that produced commit 48a475b.
        """
        repo = self.repo()
        other = repo.worktree("issue-873-governor")
        self.store.heartbeat("session-A")
        self.assertIsNone(self.check(other, "session-A", "issue-873"))
        repo.dirty(other)
        self.store.confirm(gaia_bus.identify(Path(other) / RepoFixture.FILE), "session-A")

        repo.dirty(repo.root)
        self.assertIsNone(self.check(repo.root, "session-B", "issue-863"),
                          "different physical trees cannot silently overwrite")

    def test_a_different_repo_is_silent(self):
        first, second = self.repo("demerzel"), self.repo("ix")
        self.store.heartbeat("session-A")
        self.check(first.root, "session-A", "issue-873")
        first.dirty(first.root)
        self.store.confirm(gaia_bus.identify(first.root / RepoFixture.FILE), "session-A")

        second.dirty(second.root)
        self.assertIsNone(self.check(second.root, "session-B", "issue-863"))


class TestGitDirtyProbeFailsClosed(GaiaTestCase):
    def test_timeout_is_unknown_not_clean(self):
        repo = self.repo()
        identity = gaia_bus.identify(repo.root / RepoFixture.FILE)
        with unittest.mock.patch(
                "subprocess.run", side_effect=subprocess.TimeoutExpired("git", 2)):
            with self.assertRaises(gaia_bus.GitStateUnknown):
                gaia_bus.path_is_dirty(identity)

    def test_failed_or_malformed_status_is_unknown_not_clean(self):
        repo = self.repo()
        identity = gaia_bus.identify(repo.root / RepoFixture.FILE)
        results = [
            subprocess.CompletedProcess([], 128, stdout="", stderr="index locked"),
            subprocess.CompletedProcess([], 0, stdout="unexpected output\n", stderr=""),
        ]
        for result in results:
            with self.subTest(returncode=result.returncode, stdout=result.stdout):
                with unittest.mock.patch("subprocess.run", return_value=result):
                    with self.assertRaises(gaia_bus.GitStateUnknown):
                        gaia_bus.path_is_dirty(identity)

    def test_unknown_git_state_neither_clears_nor_deletes_the_holder(self):
        repo = self.repo()
        identity = gaia_bus.identify(repo.root / RepoFixture.FILE)
        self.assertIsNone(self.store.check_and_claim(
            identity, "session-A", "lane-a"))
        repo.dirty(repo.root)
        self.store.confirm(identity, "session-A", "lane-a")

        def unknown(_identity):
            raise gaia_bus.GitStateUnknown("status timed out")

        with self.assertRaises(gaia_bus.GitStateUnknown):
            self.store.check_and_claim(
                identity, "session-B", "lane-b", dirty_probe=unknown)

        claims = self.store.claims()
        self.assertEqual(["session-A"], [claim["session"] for claim in claims])
        rate = self.store.fire_rate()
        self.assertEqual(1, rate.checks,
                         "the failed B check must not be recorded as clear")


# --------------------------------------------------- 2. the tracer bullet (#873)


class TestTracerBullet(GaiaTestCase):
    """The #873 collision, replayed. Slice 1 is not done until this passes.

    GIVEN A holds uncommitted edits to scripts/run_afk_cycle.py
    WHEN  B is about to edit the same path in the same physical worktree
    THEN  B's PreToolUse receives a collision naming A, its lane, and the age
    """

    def setUp(self):
        super().setUp()
        self.repo_fixture = self.repo()
        self.store.heartbeat("session-A")
        self.assertIsNone(
            self.check(self.repo_fixture.root, "session-A", "issue-873-governor"),
            "a clear path must not warn")
        self.repo_fixture.dirty(self.repo_fixture.root)
        self.store.confirm(
            gaia_bus.identify(self.repo_fixture.root / RepoFixture.FILE), "session-A")

    def test_b_is_warned_before_its_edit_runs(self):
        self.clock.advance(14 * 60)
        collision = self.check(self.repo_fixture.root, "session-B",
                               "issue-863-spend-attribution")

        self.assertIsNotNone(collision, "the #873 collision must be caught")
        self.assertEqual("session-A", collision.session)
        self.assertEqual("issue-873-governor", collision.lane)
        self.assertEqual(14 * 60, collision.age_s)

    def test_the_warning_names_what_a_human_needs_to_act(self):
        """A warning that omits who, what and how old is one nobody can act on."""
        self.clock.advance(14 * 60)
        text = self.check(self.repo_fixture.root, "session-B", "issue-863").describe()
        for needle in ("session-A", "issue-873-governor", "run_afk_cycle.py", "14m"):
            self.assertIn(needle, text)

    def test_a_session_does_not_collide_with_itself(self):
        """Re-editing your own file is the normal case, not a collision."""
        self.assertIsNone(self.check(self.repo_fixture.root, "session-A",
                                     "issue-873-governor"))

    def test_an_untouched_path_in_the_same_tree_is_clear(self):
        self.assertIsNone(self.check(self.repo_fixture.root, "session-B", "issue-863",
                                     path="CONTEXT.md"))

    def test_second_edit_cycle_reclaims_before_the_new_edit_lands(self):
        """A's new PreToolUse must replace its old dirty-cycle state atomically.

        A committed its first edit, so the physical file is clean. On the next
        PreToolUse, A owns an in-flight second edit even though PostToolUse has
        not made the file dirty yet. B must collide with that pending claim;
        treating A's row as the old dirty claim lets B observe clean Git state,
        delete A, and enter the same check-then-edit race Gaia exists to close.
        """
        self.repo_fixture.commit(self.repo_fixture.root, "first edit complete")
        self.clock.advance(60)

        self.assertIsNone(self.check(self.repo_fixture.root, "session-A",
                                     "issue-873-second-edit"))
        collision = self.check(self.repo_fixture.root, "session-B", "issue-863")

        self.assertIsNotNone(collision)
        self.assertEqual("session-A", collision.session)
        self.assertEqual("issue-873-second-edit", collision.lane)
        self.assertEqual(gaia_bus.STATE_PENDING, collision.state)
        self.assertEqual(0, collision.age_s)


# ------------------------------------------------------------- 3. claim liveness


class TestLiveness(GaiaTestCase):
    """Heartbeat-primary, TTL as crash backstop.

    Lane durations are bimodal (median 30.5 min, p90 864 min), so no fixed TTL
    works: 45 min expires the tail, 24 h cries wolf all day. Measurement chose
    the mechanism, not just the number.
    """

    def setUp(self):
        super().setUp()
        self.repo_fixture = self.repo()
        self.store.heartbeat("session-A")
        self.check(self.repo_fixture.root, "session-A", "issue-873")
        self.repo_fixture.dirty(self.repo_fixture.root)
        self.store.confirm(
            gaia_bus.identify(self.repo_fixture.root / RepoFixture.FILE), "session-A")

    def test_a_silent_but_still_dirty_session_keeps_holding_its_claim(self):
        """Heartbeat expiry cannot erase uncommitted work still on disk."""
        self.clock.advance(gaia_bus.HEARTBEAT_WINDOW_S + 1)
        self.assertIsNotNone(
            self.check(self.repo_fixture.root, "session-B", "issue-863"))

    def test_a_heartbeating_session_keeps_holding_through_the_long_tail(self):
        """p90 is 14.4 h. A fixed 45-minute TTL would drop these on the floor."""
        for _ in range(20):
            self.clock.advance(gaia_bus.HEARTBEAT_WINDOW_S - 60)
            self.store.heartbeat("session-A")
        self.assertGreater(self.clock() - 1_000_000.0, 4 * 60 * 60)
        self.assertIsNotNone(self.check(self.repo_fixture.root, "session-B", "issue-863"))

    def test_a_live_session_is_not_expired_by_a_fixed_claim_ttl(self):
        """Heartbeat is authority; elapsed claim age cannot revoke a live owner."""
        while self.clock() - 1_000_000.0 < 24 * 60 * 60 + 1:
            self.clock.advance(60)
            self.store.heartbeat("session-A")
        self.assertIsNotNone(
            self.check(self.repo_fixture.root, "session-B", "issue-863"))

    def test_a_stale_clean_lane_self_heals(self):
        """A dead lane stops holding once Git proves its work is durable."""
        self.repo_fixture.commit(self.repo_fixture.root, "abandoned work preserved")
        self.clock.advance(gaia_bus.HEARTBEAT_WINDOW_S + 1)
        self.assertIsNone(self.check(self.repo_fixture.root, "session-B", "issue-863"))

    def test_session_end_releases_every_claim_the_session_holds(self):
        self.store.release_session("session-A")
        self.assertIsNone(self.check(self.repo_fixture.root, "session-B", "issue-863"))

    def test_a_session_may_release_only_its_own_claims(self):
        """Safety boundary: no session may evict another's claim."""
        self.store.release_session("session-B")
        self.assertIsNotNone(self.check(self.repo_fixture.root, "session-C", "issue-863"))


# ------------------------------------------------------------------- 4. guards


class TestGuardPathNormalizationIsLoadBearing(GaiaTestCase):
    """Guard #1, restated after the worktree correction.

    The spec's original form -- "disable normalization and the cross-worktree
    collision is missed" -- was neutralised by commit 48a475b, which made
    cross-worktree overlap deliberately silent. Normalization is still
    load-bearing, but for a different reason: harnesses spell the same file
    differently (absolute vs relative, backslash vs forward slash, drive-letter
    case). Key on the raw string and the detector misses a real same-tree
    collision while passing every test written with one spelling.
    """

    def _spellings(self, root):
        """Two spellings of ONE file that differ as raw strings on EVERY platform.

        The `..` round trip is the load-bearing choice. A backslash-vs-slash pair
        differs only on Windows, so a mutation test built on it would silently
        pass on POSIX no matter what the implementation did.
        """
        native = str(Path(root) / RepoFixture.FILE)
        detour = os.path.join(str(root), "scripts", os.pardir, "scripts",
                              "run_afk_cycle.py")
        assert native != detour, "the two spellings must differ as raw strings"
        return native, detour

    def test_every_spelling_of_one_file_is_one_identity(self):
        repo = self.repo()
        native, detour = self._spellings(repo.root)
        spellings = [native, detour, native.replace("\\", "/")]
        identities = {gaia_bus.identify(s) for s in spellings}
        self.assertEqual(1, len(identities), f"spellings diverged: {identities}")

    def test_a_symlinked_route_to_one_file_is_one_identity(self):
        """Isolates what `realpath` carries that `abspath` does not.

        Mutating `realpath` away and keeping `abspath` SURVIVES every other test
        here, because abspath already collapses `..` and normcase already folds
        Windows case. Symlink resolution is the only remaining job, and it is a
        real route on this machine: worktrees live under paths that may be
        symlinked, and macOS /tmp is itself a link. Without this the mutation
        record for guard #1 would be overstating what the guard proves.
        """
        repo = self.repo()
        link = Path(tempfile.mkdtemp(prefix="gaia-link-")) / "linked-root"
        try:
            os.symlink(str(repo.root), str(link), target_is_directory=True)
        except (OSError, NotImplementedError, AttributeError) as error:
            self.skipTest(f"symlinks not permitted here: {error}")
        self.addCleanup(lambda: __import__("shutil").rmtree(link.parent,
                                                            ignore_errors=True))
        direct = gaia_bus.identify(Path(repo.root) / RepoFixture.FILE)
        through_link = gaia_bus.identify(link / RepoFixture.FILE)
        self.assertEqual(direct, through_link,
                         "a symlinked route to one file must be one identity, or "
                         "two sessions reaching it differently never collide")

    def test_identity_is_repo_relative_not_absolute(self):
        repo = self.repo()
        identity = gaia_bus.identify(Path(repo.root) / RepoFixture.FILE)
        self.assertEqual("scripts/run_afk_cycle.py", identity.rel_path)
        self.assertEqual("demerzel", identity.repo)

    def test_disabling_normalization_makes_the_collision_disappear(self):
        """The mutation, isolated to the one axis it claims to test.

        An earlier version blanked BOTH `rel_path` and `worktree`. That was
        confounded: an empty worktree alone makes `path_is_dirty` return False,
        which sweeps the holder's claim and yields silence no matter how the path
        is spelled. The mutant died without the spelling ever mattering, so the
        guard was no stronger than the decorative version it replaced.

        Here the worktree stays CORRECT and only the path normalization is
        disabled, so silence can only come from the two spellings failing to
        resolve to one identity.
        """
        repo = self.repo()
        native, detour = self._spellings(repo.root)
        worktree = gaia_bus.identify(native).worktree

        def claim_and_check(identify, store_name):
            # A fresh store per run rather than wiping a shared one: the
            # production class should not carry a method that exists for tests.
            store = gaia_bus.Store(self.store_path.parent / store_name, now=self.clock)
            self.addCleanup(store.close)
            store.heartbeat("session-A")
            store.check_and_claim(identify(native), "session-A", "issue-873")
            repo.dirty(repo.root)
            store.confirm(identify(native), "session-A", "issue-873")
            return store.check_and_claim(identify(detour), "session-B", "issue-863")

        self.assertIsNotNone(claim_and_check(gaia_bus.identify, "normalized.sqlite3"),
                             "normalized identity must catch the collision")

        def spelling_only_mutant(path):
            # Worktree preserved; ONLY the path key is de-normalized.
            return gaia_bus.Identity(repo="demerzel", rel_path=str(path),
                                     worktree=worktree)

        self.assertIsNone(claim_and_check(spelling_only_mutant, "mutant.sqlite3"),
                          "MUTATION SURVIVED: path normalization is not "
                          "load-bearing, so two harnesses spelling one file "
                          "differently would collide undetected in production")


class TestGuardStoreUnreachable(GaiaTestCase):
    """Guard #2. Green-while-dead must be unreachable.

    Slice 1 is brokerless, so "daemon down" is an unusable SQLite file. The
    requirement carries forward unchanged when the daemon lands in slice 2.
    """

    def test_an_unusable_store_raises_rather_than_reporting_clear(self):
        blocked = Path(tempfile.mkdtemp(prefix="gaia-blocked-"))
        self.addCleanup(lambda: __import__("shutil").rmtree(blocked, ignore_errors=True))
        # A directory where the database file belongs: open() cannot succeed.
        (blocked / "gaia.sqlite3").mkdir()
        with self.assertRaises(gaia_bus.BusUnreachable):
            gaia_bus.Store(blocked / "gaia.sqlite3").heartbeat("session-A")

    def test_a_corrupt_store_raises_rather_than_reporting_clear(self):
        self.store.close()
        self.store_path.write_bytes(b"this is not a sqlite database" * 100)
        with self.assertRaises(gaia_bus.BusUnreachable):
            gaia_bus.Store(self.store_path).heartbeat("session-A")

    def test_the_hook_degrades_to_a_visible_warning_and_never_blocks(self):
        """The other half of the split: the TOOL errors, the HOOK must not.

        A coordination nicety that stops a session from editing is worse than
        the collision it prevents -- but it must say so out loud, or a dead bus
        reads exactly like a quiet one.
        """
        import gaia_hook
        blocked = Path(tempfile.mkdtemp(prefix="gaia-blocked-"))
        self.addCleanup(lambda: __import__("shutil").rmtree(blocked, ignore_errors=True))
        (blocked / "gaia.sqlite3").mkdir()

        output = gaia_hook.pre_tool_use(
            {"tool_input": {"file_path": str(self.repo().root / RepoFixture.FILE)},
             "session_id": "session-B"},
            store_path=blocked / "gaia.sqlite3", budget_s=5.0)

        self.assertTrue(output["continue"], "a hook must never block an edit")
        self.assertIn("unreachable", output["systemMessage"].lower())


class TestGuardConcurrency(GaiaTestCase):
    """Guard #5 -- the race the tracer bullet cannot see.

    Check-at-Pre / publish-at-Post leaves a window where A and B both read
    "clear" and both edit. A *sequential* test passes against that broken
    implementation, so this one runs genuinely concurrent callers with no
    serialisation between them and asserts exactly one clear verdict.

    Mutation-verified, because a race test that has never been seen red is the
    least trustworthy kind of green:

    - claiming at PostToolUse instead of PreToolUse (the real bug): kills this
      class AND the tracer bullet -- 4 failures.
    - BEGIN DEFERRED alone: EQUIVALENT, not surviving. The heartbeat and sweep
      are writes, so the lock is taken before the read either way.
    - BEGIN DEFERRED plus both writes moved after the read (a genuinely
      lock-free section): killed 6 runs out of 6.

    An earlier attempt added a test seam to `check_and_claim` to hold every
    caller inside the critical section at once. It caught neither real mutant --
    it measures exclusivity at the seam's position, not atomicity of read and
    write -- so it was deleted rather than kept for the look of rigour.
    """

    THREADS = 8

    def test_exactly_one_of_eight_racing_sessions_gets_a_clear_verdict(self):
        repo = self.repo()
        target = Path(repo.root) / RepoFixture.FILE
        identity = gaia_bus.identify(target)
        barrier = threading.Barrier(self.THREADS)
        verdicts = [None] * self.THREADS
        errors = []

        def racer(index):
            # Its own connection, as a separate process would have.
            store = gaia_bus.Store(self.store_path, now=self.clock)
            try:
                session = f"session-{index}"
                store.heartbeat(session)
                barrier.wait(timeout=30)          # no serialisation past here
                verdicts[index] = store.check_and_claim(identity, session, f"lane-{index}")
            except Exception as error:             # noqa: BLE001 - surfaced below
                errors.append(error)
            finally:
                store.close()

        threads = [threading.Thread(target=racer, args=(i,)) for i in range(self.THREADS)]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join(timeout=60)

        self.assertEqual([], errors, "racing callers must not error")
        clear = [i for i, v in enumerate(verdicts) if v is None]
        self.assertEqual(
            1, len(clear),
            f"exactly one session may win the claim; {len(clear)} got a clear "
            f"verdict. More than one means check and claim are not atomic.")

    def test_the_winner_is_the_session_every_loser_is_told_about(self):
        """A warning naming a session that did not win is worse than none."""
        repo = self.repo()
        identity = gaia_bus.identify(Path(repo.root) / RepoFixture.FILE)
        barrier = threading.Barrier(self.THREADS)
        verdicts = [None] * self.THREADS

        def racer(index):
            store = gaia_bus.Store(self.store_path, now=self.clock)
            try:
                store.heartbeat(f"session-{index}")
                barrier.wait(timeout=30)
                verdicts[index] = store.check_and_claim(
                    identity, f"session-{index}", f"lane-{index}")
            finally:
                store.close()

        threads = [threading.Thread(target=racer, args=(i,)) for i in range(self.THREADS)]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join(timeout=60)

        winner = next(f"session-{i}" for i, v in enumerate(verdicts) if v is None)
        named = {v.session for v in verdicts if v is not None}
        self.assertEqual({winner}, named)


class TestGuardBypassHonesty(GaiaTestCase):
    """Guard #6. The coverage gap is real and permanent; assert it.

    Hooks only see mutations routed through Edit/Write. Shell redirection,
    `sed`, formatters, IDE saves and inline scripts are invisible. The session
    that wrote the spec appended test code with `cat >>` and wrote files from
    inline Python -- neither would have produced a claim. Asserting the gap
    keeps it visible instead of letting it become false confidence.
    """

    def test_a_file_mutated_outside_edit_write_produces_no_claim(self):
        repo = self.repo()
        target = Path(repo.root) / RepoFixture.FILE
        self.store.heartbeat("session-A")

        # Exactly the bypass the spec calls out: shell redirection, no hook.
        subprocess.run(f'echo "# appended" >> "{target}"',
                       shell=True, check=True, capture_output=True)
        self.assertTrue(gaia_bus.path_is_dirty(gaia_bus.identify(target)),
                        "the bypass must really have dirtied the file")

        self.assertEqual([], self.store.claims(),
                         "no hook fired, so no claim exists -- this is the "
                         "permanent coverage gap, asserted rather than assumed")
        self.assertIsNone(self.check(repo.root, "session-B", "issue-863"),
                          "Gaia cannot see what never passed through a hook")


class TestGuardBaseRateInstrumentation(GaiaTestCase):
    """Guard #4. The same-worktree fire rate is what the open decision needs.

    The spec ships warn-only because the measured 0% is off-axis: it keys on
    worktree basename and so is blind to two sessions inside one tree, which is
    the only case slice 1 treats as a collision. Slice 1 must therefore measure
    its own rate, or the warn-vs-block question stays undecidable forever.
    """

    def test_every_check_is_recorded_with_its_verdict(self):
        repo = self.repo()
        self.store.heartbeat("session-A")
        self.check(repo.root, "session-A", "issue-873")
        repo.dirty(repo.root)
        self.store.confirm(gaia_bus.identify(repo.root / RepoFixture.FILE), "session-A")
        self.check(repo.root, "session-B", "issue-863")
        self.check(repo.root, "session-B", "issue-863", path="CONTEXT.md")

        rate = self.store.fire_rate()
        self.assertEqual(3, rate.checks)
        self.assertEqual(1, rate.collisions)


class TestClaimsLedgerMirror(GaiaTestCase):
    """The unchanged Galactic lane ledger remains readable by old consumers."""

    def test_a_gaia_lane_lifecycle_is_schema_compatible_and_append_only(self):
        try:
            from scripts import galactic_bridge
        except ModuleNotFoundError:
            import galactic_bridge

        mirror = self.store_path.parent / "claims.jsonl"
        store = gaia_bus.Store(self.store_path.parent / "mirrored.sqlite3",
                               now=self.clock, claims_path=mirror)
        self.addCleanup(store.close)
        repo = self.repo()
        identity = gaia_bus.identify(repo.root / RepoFixture.FILE)

        store.check_and_claim(identity, "session-A", "codex/948-gaia-brokerless")
        repo.dirty(repo.root)
        store.confirm(identity, "session-A", "codex/948-gaia-brokerless")
        store.release_session("session-A")

        rows = [json.loads(line) for line in mirror.read_text(encoding="utf-8").splitlines()]
        self.assertEqual(["claimed", "in-progress", "released"],
                         [row["status"] for row in rows])
        self.assertEqual("scripts/run_afk_cycle.py", rows[0]["evidence"])
        self.assertNotIn("/", rows[0]["lane"],
                         "the unchanged ledger schema rejects branch slashes")

        reader = galactic_bridge.Ledger(
            root=self.store_path.parent / "bridge", claims_path=mirror)
        status = reader.status()
        self.assertEqual([], status["claim_errors"])
        self.assertEqual([], status["claims"],
                         "the legacy reader must observe the final release")

    def test_session_end_releases_a_lane_after_its_file_claim_was_swept(self):
        mirror = self.store_path.parent / "swept-claims.jsonl"
        store = gaia_bus.Store(self.store_path.parent / "swept.sqlite3",
                               now=self.clock, claims_path=mirror)
        self.addCleanup(store.close)
        repo = self.repo()
        identity = gaia_bus.identify(repo.root / RepoFixture.FILE)

        store.check_and_claim(identity, "session-A", "lane-a")
        repo.dirty(repo.root)
        store.confirm(identity, "session-A", "lane-a")
        repo.commit(repo.root, "A finished")
        store.check_and_claim(identity, "session-B", "lane-b")
        self.assertNotIn("session-A", [claim["session"] for claim in store.claims()])

        store.release_session("session-A")

        rows = [json.loads(line) for line in mirror.read_text(encoding="utf-8").splitlines()]
        a_statuses = [row["status"] for row in rows if row["session"] == "session-A"]
        self.assertEqual(["claimed", "in-progress", "released"], a_statuses)


class TestGenericCliAdapter(GaiaTestCase):
    """Codex, Antigravity, and other harnesses can call brokerless CLI verbs."""

    def test_confirm_preserves_the_callers_lane(self):
        repo = self.repo()
        target = repo.root / RepoFixture.FILE
        self.assertEqual(0, gaia_bus.main([
            "--store", str(self.store_path), "check", "--path", str(target),
            "--session", "codex-session", "--lane", "codex-948",
        ]))
        repo.dirty(repo.root)
        self.assertEqual(0, gaia_bus.main([
            "--store", str(self.store_path), "confirm", "--path", str(target),
            "--session", "codex-session", "--lane", "codex-948",
        ]))

        claim = self.store.claims()[0]
        self.assertEqual("dirty", claim["state"])
        self.assertEqual("codex-948", claim["lane"])

    def test_the_fire_rate_of_an_idle_bus_is_zero_not_undefined(self):
        """A detector that has never run must not report a clean bill of health."""
        rate = self.store.fire_rate()
        self.assertEqual(0, rate.checks)
        self.assertIsNone(rate.ratio, "0/0 is unknown, not 0%")


# --------------------------------------------------------------- 5. hook wiring


class TestHookContract(GaiaTestCase):
    """The hook is the only reason any of this runs without discipline."""

    def setUp(self):
        super().setUp()
        import gaia_hook
        self.hook = gaia_hook
        self.repo_fixture = self.repo()
        self.target = Path(self.repo_fixture.root) / RepoFixture.FILE

    def pre(self, session, path=None):
        return self.hook.pre_tool_use(
            {"tool_input": {"file_path": str(path or self.target)},
             "session_id": session, "cwd": str(self.repo_fixture.root)},
            store_path=self.store_path,
            # Contract tests isolate collision semantics from the independently
            # tested 100 ms timeout policy and its intentional overrun path.
            budget_s=5.0)

    def test_a_clear_path_adds_no_context(self):
        self.assertNotIn("hookSpecificOutput", self.pre("session-A"))

    def test_a_collision_reaches_the_session_as_additional_context(self):
        self.pre("session-A")
        self.repo_fixture.dirty(self.repo_fixture.root)
        self.hook.post_tool_use(
            {"tool_input": {"file_path": str(self.target)}, "session_id": "session-A"},
            store_path=self.store_path)

        output = self.pre("session-B")
        self.assertTrue(output["continue"], "warn-only: never block the edit")
        context = output["hookSpecificOutput"]["additionalContext"]
        self.assertIn("session-A", context)
        self.assertIn("PreToolUse", output["hookSpecificOutput"]["hookEventName"])

    def test_post_tool_fallback_records_the_real_lane(self):
        """A timed-out or newly installed PreToolUse must not erase provenance."""
        self.hook.post_tool_use(
            {"tool_input": {"file_path": str(self.target)},
             "session_id": "session-A"},
            store_path=self.store_path)

        store = gaia_bus.Store(self.store_path)
        self.addCleanup(store.close)
        claim = store.claims()[0]
        self.assertEqual("master", claim["lane"])

    def test_the_warning_is_marked_untrusted_peer_context(self):
        """Safety boundary: another session's lane slug is not an instruction."""
        self.pre("session-A")
        self.repo_fixture.dirty(self.repo_fixture.root)
        self.hook.post_tool_use(
            {"tool_input": {"file_path": str(self.target)}, "session_id": "session-A"},
            store_path=self.store_path)
        context = self.pre("session-B")["hookSpecificOutput"]["additionalContext"]
        self.assertIn("untrusted", context.lower())

    def test_a_tool_call_with_no_file_path_is_ignored(self):
        output = self.hook.pre_tool_use({"tool_input": {"command": "ls"},
                                         "session_id": "session-A"},
                                        store_path=self.store_path)
        self.assertEqual({"continue": True}, output)

    def test_an_unplaceable_path_is_counted_rather_than_silently_dropped(self):
        """Found end-to-end, not by unit test, and it is the design's own trap.

        A harness handing over a POSIX-style path on Windows (`/c/tmp/...`)
        resolves to nothing, so `identify` returns None and the check evaporates.
        Every edit from that harness is uncovered while the bus reports healthy --
        blindness that reads exactly like quiet. Counting it turns a silence into
        a number someone can see.
        """
        self.pre("session-C", path="/c/tmp/definitely-not-a-windows-path/x.py")
        self.assertEqual(1, self.store.fire_rate().unresolved)

    def test_an_unresolved_path_is_not_counted_as_a_clean_check(self):
        """Otherwise blindness would improve the measured fire rate."""
        self.pre("session-C", path="/c/tmp/definitely-not-a-windows-path/x.py")
        self.assertEqual(0, self.store.fire_rate().checks)

    def test_a_path_outside_any_repo_is_ignored(self):
        outside = Path(tempfile.mkdtemp(prefix="gaia-outside-"))
        self.addCleanup(lambda: __import__("shutil").rmtree(outside, ignore_errors=True))
        self.assertEqual({"continue": True},
                         self.pre("session-A", path=outside / "notes.txt"))

    def test_session_start_announces_a_dead_bus(self):
        """Spec: "SessionStart reports the bus as down. Green must be
        unreachable while dead." Without it a session learns nothing until its
        first Edit, and a dead bus reads exactly like a quiet one meanwhile."""
        blocked = Path(tempfile.mkdtemp(prefix="gaia-blocked-"))
        self.addCleanup(lambda: __import__("shutil").rmtree(blocked, ignore_errors=True))
        (blocked / "gaia.sqlite3").mkdir()
        output = self.hook.session_start({"session_id": "session-A"},
                                         store_path=blocked / "gaia.sqlite3")
        self.assertIn("down", output["systemMessage"].lower())
        self.assertIn("unguarded",
                      output["hookSpecificOutput"]["additionalContext"].lower())

    def test_session_start_is_silent_when_the_bus_is_healthy(self):
        """A bus that announces itself every session start gets filtered out."""
        self.assertEqual({"continue": True},
                         self.hook.session_start({"session_id": "session-A"},
                                                 store_path=self.store_path))

    def test_a_heartbeat_keeps_claims_alive_without_any_edit(self):
        """Liveness must not depend on Edit traffic alone.

        A session that edits, then reads and reasons for longer than the
        heartbeat window, would otherwise be swept while its uncommitted work
        still sits in the tree -- a false negative on the exact case slice 1
        exists for. UserPromptSubmit carries this for one cheap call per turn.
        """
        self.assertIn("UserPromptSubmit", self.hook.HANDLERS)
        self.hook.heartbeat({"session_id": "session-A"}, store_path=self.store_path)
        store = gaia_bus.Store(self.store_path)
        self.addCleanup(store.close)
        self.assertEqual([], store.claims())     # a heartbeat claims nothing

    def test_every_tool_activity_is_wired_as_a_heartbeat(self):
        """Read/Bash-heavy turns must not depend on UserPromptSubmit alone."""
        settings = json.loads(
            (Path(__file__).parents[1] / ".claude" / "settings.json")
            .read_text(encoding="utf-8"))
        commands = [
            hook["command"]
            for group in settings["hooks"]["PreToolUse"]
            if group.get("matcher") == ".*"
            for hook in group["hooks"]
        ]
        self.assertTrue(any("gaia_hook.py ToolActivity" in command
                            for command in commands))
        self.assertIs(self.hook.heartbeat, self.hook.HANDLERS["ToolActivity"])

    def test_stop_is_not_wired_to_release(self):
        """`Stop` fires at the end of every TURN, not the session.

        Wiring it to release would drop a session's claims after each reply,
        leaving its uncommitted edits unguarded for the rest of the lane while
        the bus kept reporting healthy -- a no-op that reads green, which is the
        exact failure the predecessor ledger documents.
        """
        self.assertNotIn("Stop", self.hook.HANDLERS)

    def test_session_end_releases_the_sessions_claims(self):
        self.pre("session-A")
        self.repo_fixture.dirty(self.repo_fixture.root)
        self.hook.post_tool_use(
            {"tool_input": {"file_path": str(self.target)}, "session_id": "session-A"},
            store_path=self.store_path)
        self.hook.session_end({"session_id": "session-A"}, store_path=self.store_path)
        self.assertNotIn("hookSpecificOutput", self.pre("session-B"))


class TestBaseRateTool(GaiaTestCase):
    """Guard #4's instrument. Tested because an unproven measurement tool that
    reports a comfortable number is worse than no measurement at all."""

    def setUp(self):
        super().setUp()
        try:
            from scripts import gaia_base_rate
        except ModuleNotFoundError:
            import gaia_base_rate
        self.tool = gaia_base_rate

    def test_it_finds_dirty_paths_in_every_worktree(self):
        repo = self.repo()
        other = repo.worktree("lane-a")
        repo.dirty(repo.root)
        repo.dirty(other)
        trees = self.tool.worktrees(repo.root)
        self.assertEqual(2, len(trees))

    def test_the_same_path_dirty_in_two_worktrees_is_counted_as_overlap(self):
        """Axis C must be able to report non-zero, or its zero proves nothing.

        A measurement that cannot fail is not a measurement.
        """
        repo = self.repo()
        other = repo.worktree("lane-a")
        repo.dirty(repo.root)
        repo.dirty(other)
        overlap = self.tool.cross_worktree_overlap(self.tool.worktrees(repo.root))
        self.assertEqual(1, overlap.overlapping)
        self.assertEqual(1.0, overlap.ratio)

    def test_different_paths_in_two_worktrees_are_not_overlap(self):
        repo = self.repo()
        other = repo.worktree("lane-a")
        repo.dirty(repo.root)
        (Path(other) / "CONTEXT.md").write_text("notes\n", encoding="utf-8")
        overlap = self.tool.cross_worktree_overlap(self.tool.worktrees(repo.root))
        self.assertEqual(0, overlap.overlapping)

    def test_a_clean_machine_reports_no_files_rather_than_dividing_by_zero(self):
        repo = self.repo()
        overlap = self.tool.cross_worktree_overlap(self.tool.worktrees(repo.root))
        self.assertEqual(0, overlap.files)
        self.assertIsNone(overlap.ratio)

    def test_unknown_same_worktree_coverage_fails_closed(self):
        repo = self.repo()
        result = self.tool.main([
            "--repo", str(repo.root), "--store", str(self.store_path),
            "--window-days", "0",
        ])
        self.assertEqual(1, result)

    def test_unresolved_paths_fail_even_when_some_checks_succeeded(self):
        repo = self.repo()
        self.check(repo.root, "session-A", "issue-948")
        self.store.record_unresolved("session-B", "/foreign/path.py")

        result = self.tool.main([
            "--repo", str(repo.root), "--store", str(self.store_path),
            "--window-days", "0",
        ])
        self.assertEqual(1, result)

    def test_same_worktree_alarm_rate_above_the_declared_ceiling_fails(self):
        repo = self.repo()
        identity = gaia_bus.identify(repo.root / RepoFixture.FILE)
        self.check(repo.root, "session-A", "issue-948")
        repo.dirty(repo.root)
        self.store.confirm(identity, "session-A", "issue-948")
        self.check(repo.root, "session-B", "issue-949")

        result = self.tool.main([
            "--repo", str(repo.root), "--store", str(self.store_path),
            "--window-days", "0", "--max-same-worktree-rate", "0.1",
        ])
        self.assertEqual(1, result)


class TestLatencyBudget(GaiaTestCase):
    """The hook honours the approved 100 ms ceiling without false green."""

    def setUp(self):
        super().setUp()
        import gaia_hook
        self.hook = gaia_hook
        self.repo_fixture = self.repo()

    def test_an_exhausted_budget_proceeds_loudly_rather_than_waiting(self):
        with unittest.mock.patch.object(
                self.hook, "_within_budget", return_value=(False, None, None)):
            output = self.hook.pre_tool_use(
                {"tool_input": {
                    "file_path": str(self.repo_fixture.root / RepoFixture.FILE)},
                 "session_id": "session-B"},
                store_path=self.store_path, budget_s=0.0)
        self.assertTrue(output["continue"], "past the budget the edit proceeds")
        self.assertIn("unguarded", output["systemMessage"].lower(),
                      "a dropped claim must never look like a clear check")

    def test_the_default_budget_matches_the_approved_ceiling(self):
        self.assertEqual(0.1, self.hook.DEFAULT_BUDGET_S)

    def test_an_overrun_drops_the_claim_in_a_real_hook_process(self):
        """Must run as a SUBPROCESS, and that is the whole finding.

        In this long-lived test process the abandoned worker survives the join
        and does eventually land its claim, so an in-process assertion would
        report a comfortable falsehood. A real hook is a process that exits the
        moment it prints, which kills the daemon worker mid-flight -- so an
        over-budget check publishes NOTHING and the check-then-publish window
        reopens for that edit. A real hole, bounded by ~6x headroom rather than
        closed, and asserted here so it cannot quietly get worse.
        """
        target = Path(self.repo_fixture.root) / RepoFixture.FILE
        payload = json.dumps({"tool_input": {"file_path": str(target)},
                              "session_id": "session-A"})
        environment = {**os.environ, "GAIA_BUDGET_S": "0.000001",
                       "GAIA_STORE": str(self.store_path)}
        result = subprocess.run(
            [sys.executable, str(Path(__file__).with_name("gaia_hook.py")),
             "PreToolUse"],
            input=payload, capture_output=True, text=True, env=environment,
            timeout=60)

        output = json.loads(result.stdout)
        self.assertTrue(output["continue"],
                        "an over-budget hook still must not block the edit")
        self.assertIn("unguarded", output["systemMessage"].lower())
        store = gaia_bus.Store(self.store_path)
        self.addCleanup(store.close)
        self.assertEqual([], store.claims(),
                         "an over-budget check must not be believed to have claimed")

    def test_a_garbage_budget_override_falls_back_rather_than_crashing(self):
        with unittest.mock.patch.dict(os.environ, {"GAIA_BUDGET_S": "soon"}):
            self.assertEqual(self.hook.DEFAULT_BUDGET_S, self.hook.check_budget_s())


if __name__ == "__main__":
    unittest.main()
