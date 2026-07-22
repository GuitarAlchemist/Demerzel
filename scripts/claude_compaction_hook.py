#!/usr/bin/env python3
"""Privacy-safe Claude Code compaction telemetry hook.

The hook records lifecycle metadata, hashes sensitive strings, and never stores
the compacted summary or transcript contents. The JSONL output is designed for
direct ingestion by DuckDB/IX.
"""

from __future__ import annotations

from contextlib import contextmanager
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
from typing import Any, Iterator


SCHEMA_VERSION = "1.0.0"
SUPPORTED_KEY = "CLAUDE_AUTOCOMPACT_PCT_OVERRIDE"
OBSOLETE_KEY = "CLAUDE_CODE_AUTOCOMPACT_PCT_OVERRIDE"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def sha256_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def _git(cwd: Path, *args: str) -> str:
    try:
        result = subprocess.run(
            ["git", "-C", str(cwd), *args],
            check=False,
            capture_output=True,
            text=True,
            timeout=2,
        )
        return result.stdout.strip() if result.returncode == 0 else ""
    except (OSError, subprocess.TimeoutExpired):
        return ""


def repository_identity(cwd: Path) -> tuple[str, str, Path]:
    root_text = _git(cwd, "rev-parse", "--show-toplevel")
    root = Path(root_text) if root_text else cwd
    remote = _git(cwd, "config", "--get", "remote.origin.url")
    repo = root.name
    if remote:
        repo = remote.rstrip("/").rsplit("/", 1)[-1].rsplit(":", 1)[-1]
        repo = repo.removesuffix(".git") or root.name
    branch = _git(cwd, "branch", "--show-current") or "detached"
    return repo.lower(), branch, root


def project_setting_status(root: Path) -> str:
    settings = root / ".claude" / "settings.json"
    if not settings.exists():
        return "inherited"
    try:
        data = json.loads(settings.read_text(encoding="utf-8-sig"))
    except (OSError, json.JSONDecodeError):
        return "invalid-json"
    env = data.get("env") if isinstance(data, dict) else None
    if not isinstance(env, dict):
        return "inherited"
    if SUPPORTED_KEY in env:
        return "supported"
    if OBSOLETE_KEY in env:
        return "obsolete-key"
    return "inherited"


@contextmanager
def file_lock(path: Path) -> Iterator[None]:
    path.parent.mkdir(parents=True, exist_ok=True)
    handle = path.open("a+b")
    try:
        if os.name == "nt":
            import msvcrt

            handle.seek(0, os.SEEK_END)
            if handle.tell() == 0:
                handle.write(b"0")
                handle.flush()
            handle.seek(0)
            msvcrt.locking(handle.fileno(), msvcrt.LK_LOCK, 1)
        else:
            import fcntl

            fcntl.flock(handle.fileno(), fcntl.LOCK_EX)
        yield
    finally:
        if os.name == "nt":
            handle.seek(0)
            msvcrt.locking(handle.fileno(), msvcrt.LK_UNLCK, 1)
        else:
            import fcntl

            fcntl.flock(handle.fileno(), fcntl.LOCK_UN)
        handle.close()


def build_event(payload: dict[str, Any]) -> dict[str, Any] | None:
    hook_name = str(payload.get("hook_event_name", ""))
    source = str(payload.get("source", ""))
    if hook_name == "PreCompact":
        event_name = "pre_compact"
    elif hook_name == "PostCompact":
        event_name = "post_compact"
    elif hook_name == "SessionStart" and source == "compact":
        event_name = "session_rehydrated"
    else:
        return None

    cwd = Path(str(payload.get("cwd") or os.getcwd())).resolve()
    repo, branch, root = repository_identity(cwd)
    transcript = str(payload.get("transcript_path", ""))
    summary = str(payload.get("compact_summary", ""))
    row: dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "ts": utc_now(),
        "event": event_name,
        "session_id": str(payload.get("session_id", "unknown"))[:160],
        "repo": repo[:160],
        "branch": branch[:240],
        "trigger": str(payload.get("trigger", ""))[:32] or None,
        "source": source[:32] or None,
        "project_setting": project_setting_status(root),
        "transcript_path_sha256": sha256_text(transcript) if transcript else None,
        "summary_chars": len(summary) if summary else None,
        "summary_sha256": sha256_text(summary) if summary else None,
    }
    return row


def append_event(path: Path, row: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    encoded = json.dumps(row, sort_keys=True, separators=(",", ":")) + "\n"
    with file_lock(path.with_suffix(path.suffix + ".lock")):
        with path.open("a", encoding="utf-8", newline="\n") as handle:
            handle.write(encoded)
            handle.flush()
            os.fsync(handle.fileno())


def handle(payload: dict[str, Any], log_path: Path | None = None) -> dict[str, Any] | None:
    row = build_event(payload)
    if row is None:
        return None
    target = log_path or Path(
        os.environ.get(
            "CLAUDE_FLEET_COMPACTION_LOG",
            str(Path.home() / ".agents" / "compaction-events.jsonl"),
        )
    )
    append_event(target, row)
    return row


def main() -> int:
    try:
        payload = json.load(sys.stdin)
        row = handle(payload)
        if row and row["event"] == "session_rehydrated":
            sys.stdout.write(
                "Fleet recovery: read state/digests/latest.md when present and "
                "check ~/.agents/claims.jsonl before resuming implementation.\n"
            )
    except Exception as exc:  # Hook must never block a Claude session.
        sys.stderr.write(f"fleet compaction telemetry unavailable: {exc}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
