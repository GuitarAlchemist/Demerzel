#!/usr/bin/env python3
"""Gaia slice 1 — deterministic collision detection between concurrent AI sessions.

Spec: docs/superpowers/specs/2026-07-30-gaia-semantic-bus-design.md

Slice 1 is **brokerless**: hooks write SQLite directly. The daemon is deferred to
slice 2, where the semantic exchange gives it something resident to hold. Nothing
in deterministic collision detection needs a long-lived process that SQLite's WAL
does not already provide, and a daemon would contribute the one failure mode this
codebase keeps getting burned by -- a process that dies quietly and reads green.

A collision is exactly one thing:

    another live session holds uncommitted edits to the same repo-relative path
    in the same PHYSICAL worktree

Everything else is deliberately silent. Two dirty copies in separate worktrees are
separate files and cannot overwrite each other; the same path committed on
divergent branches is git's problem, handled loudly at merge. Branch-level overlap
measures 58% on this machine, so warning on it would delete the signal rather than
degrade it.
"""

from __future__ import annotations

import argparse
import os
import sqlite3
import subprocess
import sys
import time
from contextlib import contextmanager
from dataclasses import dataclass, field
from pathlib import Path

# Lane durations measured 2026-07-30 over 44 lanes: median 30.5 min, p75 45 min,
# p90 864 min, p95 1324 min. Sharply bimodal, so no single TTL works -- 45 min
# expires the overnight tail, 24 h keeps dead claims warm all day. Liveness is
# therefore heartbeat-primary and the TTL is only a crash backstop for the 11%
# of lanes that were never released.
HEARTBEAT_WINDOW_S = 30 * 60        # a session is live iff it heartbeat this recently
CLAIM_TTL_S = 24 * 60 * 60          # > p95 (22.1 h); backstop for sessions that die
PENDING_GRACE_S = 5 * 60            # an edit that never landed stops holding the path

STATE_PENDING = "pending"           # claimed at PreToolUse; the edit is in flight
STATE_DIRTY = "dirty"               # PostToolUse confirmed it; uncommitted work exists

GIT_TIMEOUT_S = 2.0


class GaiaError(RuntimeError):
    """Base for every Gaia failure."""


class BusUnreachable(GaiaError):
    """The store cannot be reached.

    Raised rather than swallowed: a bus that reports "clear" while it is dead is
    worse than no bus, because sessions believe they coordinated. Green must be
    unreachable while dead. The *hook* catches this and lets the edit proceed --
    loud, not obstructive.
    """


# --------------------------------------------------------------------- identity


@dataclass(frozen=True)
class Identity:
    """What makes two edits the same edit.

    `rel_path` and `worktree` are `os.path.normcase`d. On Windows that folds case,
    which is correct -- NTFS treats `Scripts/Run.py` and `scripts/run.py` as one
    file, and so must we. On POSIX normcase is the identity function, so case is
    preserved exactly. The platform difference is the point, not an accident.
    """

    repo: str
    rel_path: str
    worktree: str


@dataclass(frozen=True)
class Collision:
    """A live holder of the path the caller is about to edit."""

    session: str
    lane: str
    state: str
    age_s: float
    identity: Identity = field(compare=False)

    def describe(self) -> str:
        return (f"{self.identity.rel_path} is held by session {self.session} "
                f"(lane {self.lane}) with uncommitted edits, claimed "
                f"{_age(self.age_s)} ago, in the same worktree "
                f"({self.identity.worktree}).")


def _age(seconds: float) -> str:
    seconds = int(seconds)
    if seconds < 60:
        return f"{seconds}s"
    if seconds < 3600:
        return f"{seconds // 60}m"
    return f"{seconds // 3600}h{(seconds % 3600) // 60:02d}m"


def _git(cwd, *args) -> str:
    try:
        result = subprocess.run(["git", "-C", str(cwd), *args], check=False,
                                capture_output=True, text=True, timeout=GIT_TIMEOUT_S)
    except (OSError, subprocess.TimeoutExpired):
        return ""
    return result.stdout.strip() if result.returncode == 0 else ""


def _nearest_existing_dir(path: str) -> str | None:
    """The directory to run git in.

    A Write can name a file that does not exist yet, and its parent directory may
    not exist either, so walk up until something does.
    """
    candidate = Path(os.path.abspath(path)).parent
    while True:
        if candidate.is_dir():
            return str(candidate)
        if candidate.parent == candidate:
            return None
        candidate = candidate.parent


def identify(path) -> Identity | None:
    """Normalize an absolute or relative path to `(repo, rel_path, worktree)`.

    Returns None when the path is not inside a git repository -- Gaia has nothing
    to say about files it cannot place.

    This is the highest-risk detail in the design. Harnesses spell the same file
    differently (absolute vs relative, backslash vs forward slash, drive-letter
    case), and keying on the raw string means the detector never fires once while
    passing every test written with a single spelling. Guard #1 mutates this
    function and requires the tracer bullet to fail.
    """
    raw = os.fspath(path)
    probe = _nearest_existing_dir(raw)
    if probe is None:
        return None
    top = _git(probe, "rev-parse", "--show-toplevel")
    if not top:
        return None

    worktree = os.path.normcase(os.path.realpath(top))
    absolute = os.path.normcase(os.path.realpath(os.path.abspath(raw)))
    try:
        relative = os.path.relpath(absolute, worktree)
    except ValueError:                      # different drive on Windows
        return None
    if relative == os.pardir or relative.startswith(os.pardir + os.sep):
        return None

    return Identity(repo=_repo_name(probe, top),
                    rel_path=relative.replace(os.sep, "/"),
                    worktree=worktree)


def _repo_name(cwd: str, toplevel: str) -> str:
    """Repo identity from the remote, so every worktree agrees on the name.

    Falling back to the directory name would give each of this machine's 47
    worktrees a different repo id, which silently disables cross-checking.
    """
    remote = _git(cwd, "config", "--get", "remote.origin.url")
    if remote:
        tail = remote.rstrip("/").rsplit("/", 1)[-1].rsplit(":", 1)[-1]
        name = tail.removesuffix(".git")
        if name:
            return name.lower()
    return Path(toplevel).name.lower()


def path_is_dirty(identity: Identity) -> bool:
    """Does this worktree hold uncommitted changes to this path?

    Untracked counts: a newly written file is uncommitted work like any other.
    An unreadable worktree reports clean, which errs toward silence -- a false
    negative here costs a missed warning, a false positive costs the signal.
    """
    if not identity.worktree:
        return False
    output = _git(identity.worktree, "status", "--porcelain", "--", identity.rel_path)
    return bool(output.strip())


# ------------------------------------------------------------------------ store


@dataclass(frozen=True)
class FireRate:
    """Guard #4 -- the same-worktree rate the warn-vs-block decision needs.

    The spec's measured 0% is off-axis: it keys on worktree basename and is
    structurally blind to two sessions inside one tree, which is the only case
    slice 1 treats as a collision. Slice 1 measures its own rate or the question
    stays undecidable.
    """

    checks: int
    collisions: int
    unresolved: int = 0

    @property
    def ratio(self) -> float | None:
        """None, not 0.0, when nothing has been checked. 0/0 is unknown."""
        return None if self.checks == 0 else self.collisions / self.checks


SCHEMA = """
CREATE TABLE IF NOT EXISTS sessions (
    session      TEXT PRIMARY KEY,
    heartbeat_at REAL NOT NULL
);
CREATE TABLE IF NOT EXISTS claims (
    repo       TEXT NOT NULL,
    rel_path   TEXT NOT NULL,
    worktree   TEXT NOT NULL,
    session    TEXT NOT NULL,
    lane       TEXT NOT NULL,
    state      TEXT NOT NULL,
    claimed_at REAL NOT NULL,
    PRIMARY KEY (repo, rel_path, worktree, session)
);
CREATE TABLE IF NOT EXISTS checks (
    at       REAL NOT NULL,
    repo     TEXT NOT NULL,
    rel_path TEXT NOT NULL,
    worktree TEXT NOT NULL,
    session  TEXT NOT NULL,
    verdict  TEXT NOT NULL
);
"""


def default_store_path() -> Path:
    override = os.environ.get("GAIA_STORE")
    if override:
        return Path(override)
    local = os.environ.get("LOCALAPPDATA")
    if local:
        return Path(local) / "Demerzel" / "gaia" / "gaia.sqlite3"
    return Path.home() / ".local" / "state" / "demerzel" / "gaia" / "gaia.sqlite3"


class Store:
    """The working store. Multi-process safe via SQLite WAL.

    Connection is lazy so that constructing a Store never masks an unreachable
    bus as a healthy one -- the failure surfaces on the first real operation.
    """

    def __init__(self, path=None, now=time.time):
        self.path = Path(path) if path is not None else default_store_path()
        self._now = now
        self._conn: sqlite3.Connection | None = None

    # -- lifecycle ---------------------------------------------------------

    def _connect(self) -> sqlite3.Connection:
        if self._conn is not None:
            return self._conn
        conn = None
        try:
            self.path.parent.mkdir(parents=True, exist_ok=True)
            conn = sqlite3.connect(str(self.path), timeout=5.0, isolation_level=None)
            conn.row_factory = sqlite3.Row
            # busy_timeout FIRST. Switching journal mode needs a brief exclusive
            # lock, and without a busy handler already installed, several sessions
            # opening a fresh store at once each get SQLITE_BUSY -- reporting a
            # perfectly healthy bus as unreachable exactly when the most sessions
            # are running. Guard #5 caught this; no sequential test could.
            conn.execute("PRAGMA busy_timeout=5000")
            if str(conn.execute("PRAGMA journal_mode").fetchone()[0]).lower() != "wal":
                try:
                    conn.execute("PRAGMA journal_mode=WAL")
                except sqlite3.OperationalError:
                    # Another connection is mid-setup. WAL is a persistent
                    # property of the file, so it will land; and correctness does
                    # not depend on it -- BEGIN IMMEDIATE plus busy_timeout
                    # serialises writers in rollback-journal mode too. WAL buys
                    # throughput, not atomicity.
                    pass
            conn.executescript(SCHEMA)
        except (sqlite3.Error, OSError) as error:
            if conn is not None:
                conn.close()        # or the file handle outlives the failure
            raise BusUnreachable(f"gaia store at {self.path} is unusable: {error}") from error
        self._conn = conn
        return conn

    def close(self) -> None:
        if self._conn is not None:
            self._conn.close()
            self._conn = None

    @contextmanager
    def _write(self):
        """A genuine write transaction.

        BEGIN IMMEDIATE takes the write lock up front, which is what makes
        check-and-claim atomic ACROSS PROCESSES. Without it two sessions can both
        read "clear" and both claim -- the exact race guard #5 exists to catch,
        and one a sequential test would never see.
        """
        conn = self._connect()
        try:
            conn.execute("BEGIN IMMEDIATE")
        except sqlite3.Error as error:
            raise BusUnreachable(f"gaia store at {self.path} is unusable: {error}") from error
        try:
            yield conn
        except BaseException:
            conn.execute("ROLLBACK")
            raise
        conn.execute("COMMIT")

    # -- operations --------------------------------------------------------

    def heartbeat(self, session: str) -> None:
        """Liveness. Sessions heartbeat for free on ordinary hook traffic."""
        with self._write() as conn:
            self._heartbeat(conn, session)

    def _heartbeat(self, conn, session: str) -> None:
        conn.execute(
            "INSERT INTO sessions (session, heartbeat_at) VALUES (?, ?) "
            "ON CONFLICT(session) DO UPDATE SET heartbeat_at=excluded.heartbeat_at",
            (session, self._now()))

    def check_and_claim(self, identity, session: str, lane: str,
                        dirty_probe=path_is_dirty) -> Collision | None:
        """PreToolUse: report any live holder AND take the claim, atomically.

        Taking the claim at PostToolUse instead would leave the check-then-publish
        race: A checks clear, B checks clear, both edit, neither has published.
        Test-and-set in one transaction closes it.

        The dirty probe shells out to git, so it deliberately runs only when a
        holder exists -- the common path (nothing held) never leaves SQLite.

        Mutation record, because this method's correctness is not self-evident.
        Removing the INSERT below (i.e. claiming at PostToolUse instead) is the
        check-then-publish bug, and it kills 4 tests including the tracer bullet.
        Swapping BEGIN IMMEDIATE for BEGIN DEFERRED alone is *equivalent*, not a
        surviving mutant: the heartbeat and sweep are writes, so the lock is taken
        before the read regardless. Only DEFERRED plus moving both writes after
        the read produces a genuinely lock-free section, and guard #5 kills that
        6 times out of 6. BEGIN IMMEDIATE is what makes the exclusion intentional
        rather than incidental -- do not "simplify" it away.
        """
        if identity is None:
            return None
        with self._write() as conn:
            self._heartbeat(conn, session)
            self._sweep(conn)
            collision = self._first_live_holder(conn, identity, session, dirty_probe)
            now = self._now()
            conn.execute(
                "INSERT INTO claims (repo, rel_path, worktree, session, lane, state, "
                "claimed_at) VALUES (?, ?, ?, ?, ?, ?, ?) "
                "ON CONFLICT(repo, rel_path, worktree, session) "
                "DO UPDATE SET lane=excluded.lane",
                (identity.repo, identity.rel_path, identity.worktree, session, lane,
                 STATE_PENDING, now))
            conn.execute(
                "INSERT INTO checks (at, repo, rel_path, worktree, session, verdict) "
                "VALUES (?, ?, ?, ?, ?, ?)",
                (now, identity.repo, identity.rel_path, identity.worktree, session,
                 "collision" if collision else "clear"))
        return collision

    def _first_live_holder(self, conn, identity, session, dirty_probe):
        """The earliest live holder, sweeping claims that no longer hold anything.

        Ordered by (claimed_at, rowid) so that concurrent callers stamped with the
        same clock still agree on who won -- a warning naming a session that did
        not win is worse than no warning.
        """
        rows = conn.execute(
            "SELECT rowid, session, lane, state, claimed_at FROM claims "
            "WHERE repo=? AND rel_path=? AND worktree=? AND session<>? "
            "ORDER BY claimed_at, rowid",
            (identity.repo, identity.rel_path, identity.worktree, session)).fetchall()

        now = self._now()
        for row in rows:
            age = now - row["claimed_at"]
            expired_pending = row["state"] == STATE_PENDING and age > PENDING_GRACE_S
            if row["state"] == STATE_DIRTY or expired_pending:
                # A holder whose edits are committed (or reverted, or never
                # landed) holds nothing: the work is durable and git speaks up at
                # merge. Sweeping is what keeps every finished lane from
                # poisoning the path for the rest of the day.
                if not dirty_probe(identity):
                    conn.execute(
                        "DELETE FROM claims WHERE repo=? AND rel_path=? AND worktree=? "
                        "AND session=?",
                        (identity.repo, identity.rel_path, identity.worktree,
                         row["session"]))
                    continue
            return Collision(session=row["session"], lane=row["lane"],
                             state=row["state"], age_s=age, identity=identity)
        return None

    def record_unresolved(self, session: str, raw_path: str) -> None:
        """A path Gaia could not place inside any repo.

        Found empirically: a harness that hands over a POSIX-style path on
        Windows (`/c/tmp/...`) resolves to nothing, `identify` returns None, and
        the check silently evaporates. Without this row that harness is
        indistinguishable from a quiet machine -- a blind detector reading green,
        which is the precise failure the predecessor's 354 heartbeats document.
        Counting them makes blindness show up as a number instead of a silence.
        """
        with self._write() as conn:
            conn.execute(
                "INSERT INTO checks (at, repo, rel_path, worktree, session, verdict) "
                "VALUES (?, ?, ?, ?, ?, ?)",
                (self._now(), "", raw_path, "", session, "unresolved"))

    def confirm(self, identity, session: str) -> None:
        """PostToolUse: the edit landed, so the claim now covers real dirty work."""
        if identity is None:
            return
        with self._write() as conn:
            self._heartbeat(conn, session)
            conn.execute(
                "INSERT INTO claims (repo, rel_path, worktree, session, lane, state, "
                "claimed_at) VALUES (?, ?, ?, ?, ?, ?, ?) "
                "ON CONFLICT(repo, rel_path, worktree, session) "
                "DO UPDATE SET state=excluded.state",
                (identity.repo, identity.rel_path, identity.worktree, session,
                 "unknown", STATE_DIRTY, self._now()))

    def release_session(self, session: str) -> None:
        """SessionEnd. A session may release only its own claims."""
        with self._write() as conn:
            conn.execute("DELETE FROM claims WHERE session=?", (session,))
            conn.execute("DELETE FROM sessions WHERE session=?", (session,))

    def _sweep(self, conn) -> None:
        now = self._now()
        conn.execute(
            "DELETE FROM claims WHERE claimed_at <= ? OR session NOT IN "
            "(SELECT session FROM sessions WHERE heartbeat_at > ?)",
            (now - CLAIM_TTL_S, now - HEARTBEAT_WINDOW_S))

    # -- inspection --------------------------------------------------------

    def claims(self) -> list[dict]:
        conn = self._connect()
        return [dict(row) for row in conn.execute(
            "SELECT repo, rel_path, worktree, session, lane, state, claimed_at "
            "FROM claims ORDER BY claimed_at, rowid")]

    def fire_rate(self) -> FireRate:
        conn = self._connect()
        row = conn.execute(
            "SELECT "
            "COALESCE(SUM(CASE WHEN verdict<>'unresolved' THEN 1 ELSE 0 END), 0) "
            "AS checks, "
            "COALESCE(SUM(CASE WHEN verdict='collision' THEN 1 ELSE 0 END), 0) "
            "AS collisions, "
            "COALESCE(SUM(CASE WHEN verdict='unresolved' THEN 1 ELSE 0 END), 0) "
            "AS unresolved FROM checks").fetchone()
        return FireRate(checks=row["checks"], collisions=row["collisions"],
                        unresolved=row["unresolved"])

    def wipe(self) -> None:
        with self._write() as conn:
            for table in ("claims", "sessions", "checks"):
                conn.execute(f"DELETE FROM {table}")


# -------------------------------------------------------------------------- cli


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Gaia slice 1 collision detection")
    parser.add_argument("--store", default=None)
    sub = parser.add_subparsers(dest="verb", required=True)

    check = sub.add_parser("check", help="check-and-claim a path (PreToolUse)")
    check.add_argument("--path", required=True)
    check.add_argument("--session", required=True)
    check.add_argument("--lane", default="unknown")

    confirm = sub.add_parser("confirm", help="confirm an edit landed (PostToolUse)")
    confirm.add_argument("--path", required=True)
    confirm.add_argument("--session", required=True)

    beat = sub.add_parser("heartbeat")
    beat.add_argument("--session", required=True)

    release = sub.add_parser("release", help="release a session's claims (SessionEnd)")
    release.add_argument("--session", required=True)

    sub.add_parser("status", help="live claims and the measured fire rate")

    args = parser.parse_args(argv)
    store = Store(args.store)

    try:
        if args.verb == "check":
            collision = store.check_and_claim(identify(args.path), args.session, args.lane)
            if collision:
                print(collision.describe())
            return 0
        if args.verb == "confirm":
            store.confirm(identify(args.path), args.session)
            return 0
        if args.verb == "heartbeat":
            store.heartbeat(args.session)
            return 0
        if args.verb == "release":
            store.release_session(args.session)
            return 0

        rate = store.fire_rate()
        for claim in store.claims():
            print(f"{claim['session']:<24} {claim['lane']:<24} "
                  f"{claim['state']:<8} {claim['repo']}/{claim['rel_path']}")
        share = "unknown (nothing checked)" if rate.ratio is None else f"{rate.ratio:.2%}"
        print(f"\nchecks={rate.checks} collisions={rate.collisions} fire_rate={share}")
        return 0
    except BusUnreachable as error:
        print(f"gaia: {error}", file=sys.stderr)
        return 2
    finally:
        store.close()


if __name__ == "__main__":
    raise SystemExit(main())
