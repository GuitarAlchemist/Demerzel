#!/usr/bin/env python3
"""Local Galactic Protocol session bridge and dependency-free MCP server.

The bridge gives otherwise isolated top-level Codex sessions a shared,
append-only coordination ledger. Runtime state defaults to the user's local app
data directory so sessions rooted in different repositories can all reach it.
"""

from __future__ import annotations

import argparse
import contextlib
import hashlib
import json
import os
from pathlib import Path
import re
import sys
import tempfile
import time
from datetime import datetime, timedelta, timezone
from typing import Any, Iterator
import uuid


INTEGRITY_FIELDS = {
    "message_id",
    "origin_repo",
    "origin_agent",
    "timestamp",
    "content_hash",
    "hash_algorithm",
}
SESSION_TTL_MINUTES = 15
MAX_MESSAGE_CHARS = 4_000
NAME_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,127}$")


class BridgeError(ValueError):
    """A safe, user-facing bridge error."""


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def isoformat(value: datetime) -> str:
    return value.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def parse_time(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def default_state_root() -> Path:
    override = os.environ.get("GALACTIC_STATE_ROOT")
    if override:
        return Path(override).expanduser().resolve()
    local_app_data = os.environ.get("LOCALAPPDATA")
    if local_app_data:
        return Path(local_app_data) / "Demerzel" / "galactic-protocol"
    return Path(tempfile.gettempdir()) / "demerzel-galactic-protocol"


def default_claims_path() -> Path:
    override = os.environ.get("GALACTIC_CLAIMS_PATH")
    if override:
        return Path(override).expanduser().resolve()
    return Path.home() / ".agents" / "claims.jsonl"


def canonical_payload(event: dict[str, Any]) -> bytes:
    payload = {key: value for key, value in event.items() if key not in INTEGRITY_FIELDS}
    return json.dumps(
        payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode("utf-8")


def content_hash(event: dict[str, Any]) -> str:
    return hashlib.sha256(canonical_payload(event)).hexdigest()


def verify_event(event: dict[str, Any]) -> tuple[bool, str | None]:
    missing = sorted(INTEGRITY_FIELDS - event.keys())
    if missing:
        return False, f"missing integrity fields: {', '.join(missing)}"
    if event.get("hash_algorithm") != "sha256":
        return False, "unsupported hash algorithm"
    if event.get("content_hash") != content_hash(event):
        return False, "content hash mismatch"
    try:
        uuid.UUID(str(event["message_id"]))
        parse_time(str(event["timestamp"]))
    except (ValueError, TypeError) as exc:
        return False, f"invalid integrity metadata: {exc}"
    return True, None


def _safe_name(value: str, field: str) -> str:
    value = value.strip()
    if not NAME_RE.fullmatch(value):
        raise BridgeError(f"{field} must match {NAME_RE.pattern}")
    return value


@contextlib.contextmanager
def _file_lock(path: Path, timeout_seconds: float = 5.0) -> Iterator[None]:
    """Take a one-byte advisory lock on Windows or POSIX."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a+b") as handle:
        handle.seek(0, os.SEEK_END)
        if handle.tell() == 0:
            handle.write(b"0")
            handle.flush()
        handle.seek(0)
        deadline = time.monotonic() + timeout_seconds
        if os.name == "nt":
            import msvcrt

            while True:
                try:
                    handle.seek(0)
                    msvcrt.locking(handle.fileno(), msvcrt.LK_NBLCK, 1)
                    break
                except OSError:
                    if time.monotonic() >= deadline:
                        raise BridgeError("timed out acquiring the Galactic ledger lock")
                    time.sleep(0.025)
            try:
                yield
            finally:
                handle.seek(0)
                msvcrt.locking(handle.fileno(), msvcrt.LK_UNLCK, 1)
        else:
            import fcntl

            while True:
                try:
                    fcntl.flock(handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
                    break
                except BlockingIOError:
                    if time.monotonic() >= deadline:
                        raise BridgeError("timed out acquiring the Galactic ledger lock")
                    time.sleep(0.025)
            try:
                yield
            finally:
                fcntl.flock(handle.fileno(), fcntl.LOCK_UN)


class Ledger:
    def __init__(self, root: Path | None = None, claims_path: Path | None = None) -> None:
        self.root = (root or default_state_root()).resolve()
        self.events_path = self.root / "events.jsonl"
        self.lock_path = self.root / "events.lock"
        self.claims_path = (
            claims_path
            or ((root / "claims.jsonl") if root is not None else default_claims_path())
        ).resolve()
        self.claims_lock_path = self.claims_path.with_suffix(".lock")

    def _load_unlocked(self) -> tuple[list[dict[str, Any]], list[str]]:
        events: list[dict[str, Any]] = []
        errors: list[str] = []
        if not self.events_path.exists():
            return events, errors
        with self.events_path.open("r", encoding="utf-8") as handle:
            for line_number, line in enumerate(handle, start=1):
                if not line.strip():
                    continue
                try:
                    event = json.loads(line)
                    if not isinstance(event, dict):
                        raise ValueError("row is not an object")
                    valid, reason = verify_event(event)
                    if not valid:
                        raise ValueError(reason)
                    events.append(event)
                except (json.JSONDecodeError, ValueError, TypeError) as exc:
                    errors.append(f"line {line_number}: {exc}")
        return events, errors

    def load(self) -> tuple[list[dict[str, Any]], list[str]]:
        with _file_lock(self.lock_path):
            return self._load_unlocked()

    def _make_event(
        self,
        event_type: str,
        origin_repo: str,
        origin_agent: str,
        now: datetime,
        **fields: Any,
    ) -> dict[str, Any]:
        event: dict[str, Any] = {
            "protocol": "galactic.session-coordination/v0.1",
            "event_type": event_type,
            **fields,
            "message_id": str(uuid.uuid4()),
            "origin_repo": _safe_name(origin_repo.lower(), "origin_repo"),
            "origin_agent": _safe_name(origin_agent.lower(), "origin_agent"),
            "timestamp": isoformat(now),
            "hash_algorithm": "sha256",
        }
        event["content_hash"] = content_hash(event)
        return event

    def _append_unlocked(self, event: dict[str, Any]) -> None:
        self.root.mkdir(parents=True, exist_ok=True)
        row = json.dumps(event, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
        with self.events_path.open("a", encoding="utf-8", newline="\n") as handle:
            handle.write(row + "\n")
            handle.flush()
            os.fsync(handle.fileno())

    @staticmethod
    def _sessions(events: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
        sessions: dict[str, dict[str, Any]] = {}
        for event in events:
            if event.get("event_type") not in {"session.started", "session.heartbeat"}:
                continue
            session_id = str(event.get("session_id", ""))
            if not session_id:
                continue
            previous = sessions.get(session_id, {})
            sessions[session_id] = {
                **previous,
                "session_id": session_id,
                "repo": event["origin_repo"],
                "agent": event["origin_agent"],
                "cwd": event.get("cwd", previous.get("cwd", "")),
                "branch": event.get("branch", previous.get("branch", "")),
                "lane": event.get("lane", previous.get("lane", "")),
                "model": event.get("model", previous.get("model", "")),
                "last_seen": event["timestamp"],
            }
        return sessions

    def _load_claim_rows(self) -> tuple[list[dict[str, Any]], list[str]]:
        rows: list[dict[str, Any]] = []
        errors: list[str] = []
        if not self.claims_path.exists():
            return rows, errors
        with self.claims_path.open("r", encoding="utf-8") as handle:
            for line_number, line in enumerate(handle, start=1):
                if not line.strip():
                    continue
                try:
                    row = json.loads(line)
                    required = {"ts", "repo", "lane", "status", "session", "evidence"}
                    missing = sorted(required - row.keys())
                    if missing:
                        raise ValueError(f"missing fields: {', '.join(missing)}")
                    for field in ("ts", "repo", "lane", "status", "session"):
                        if not isinstance(row[field], str):
                            raise ValueError(f"{field} must be a string")
                    parse_time(str(row["ts"]))
                    _safe_name(row["repo"], "repo")
                    _safe_name(row["lane"], "lane")
                    _safe_name(row["session"], "session")
                    if row["status"] not in {"claimed", "done", "released", "in-progress"}:
                        raise ValueError(f"invalid status: {row['status']}")
                    if row["evidence"] is not None and not isinstance(row["evidence"], str):
                        raise ValueError("evidence must be a string or null")
                    if "note" in row and not isinstance(row["note"], str):
                        raise ValueError("note must be a string")
                    rows.append(row)
                except (json.JSONDecodeError, ValueError, TypeError) as exc:
                    errors.append(f"line {line_number}: {exc}")
        return rows, errors

    @staticmethod
    def _latest_claim_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
        latest: dict[tuple[str, str], dict[str, Any]] = {}
        for row in rows:
            latest[(str(row["repo"]).lower(), str(row["lane"]))] = row
        return sorted(latest.values(), key=lambda row: (row["repo"], row["lane"]))

    def _append_claim_row(self, row: dict[str, Any]) -> None:
        self.claims_path.parent.mkdir(parents=True, exist_ok=True)
        encoded = json.dumps(row, separators=(",", ":"), ensure_ascii=False)
        with self.claims_path.open("a", encoding="utf-8", newline="\n") as handle:
            handle.write(encoded + "\n")
            handle.flush()
            os.fsync(handle.fileno())

    def register(
        self,
        session_id: str,
        repo: str,
        cwd: str,
        branch: str = "",
        lane: str = "",
        agent: str = "codex-desktop",
        model: str = "",
        now: datetime | None = None,
    ) -> dict[str, Any]:
        now = now or utc_now()
        session_id = _safe_name(session_id, "session_id")
        with _file_lock(self.lock_path):
            events, _ = self._load_unlocked()
            event_type = "session.heartbeat" if session_id in self._sessions(events) else "session.started"
            event = self._make_event(
                event_type,
                repo,
                agent,
                now,
                session_id=session_id,
                cwd=str(cwd),
                branch=str(branch),
                lane=str(lane or branch or "default"),
                model=str(model),
            )
            self._append_unlocked(event)
        return event

    def heartbeat(
        self,
        session_id: str,
        repo: str,
        cwd: str,
        branch: str = "",
        lane: str = "",
        agent: str = "codex-desktop",
        model: str = "",
        now: datetime | None = None,
    ) -> dict[str, Any]:
        return self.register(session_id, repo, cwd, branch, lane, agent, model, now)

    def status(self, now: datetime | None = None, include_stale: bool = True) -> dict[str, Any]:
        now = now or utc_now()
        events, errors = self.load()
        sessions = list(self._sessions(events).values())
        for session in sessions:
            age = now - parse_time(session["last_seen"])
            session["active"] = age <= timedelta(minutes=SESSION_TTL_MINUTES)
            session["age_seconds"] = max(0, int(age.total_seconds()))
        if not include_stale:
            sessions = [session for session in sessions if session["active"]]
        sessions.sort(key=lambda item: (not item["active"], item["repo"], item["session_id"]))
        claim_rows, claim_errors = self._load_claim_rows()
        latest_claims = self._latest_claim_rows(claim_rows)
        return {
            "state_root": str(self.root),
            "claims_path": str(self.claims_path),
            "sessions": sessions,
            "claims": [
                row for row in latest_claims if row["status"] in {"claimed", "in-progress"}
            ],
            "claim_history_latest": latest_claims,
            "integrity_errors": errors,
            "claim_errors": claim_errors,
            "event_count": len(events),
        }

    def claim(
        self,
        session_id: str,
        repo: str,
        lane: str,
        note: str = "",
        now: datetime | None = None,
    ) -> dict[str, Any]:
        now = now or utc_now()
        session_id = _safe_name(session_id, "session_id")
        repo = _safe_name(repo.lower(), "repo")
        lane = _safe_name(lane, "lane")
        with _file_lock(self.claims_lock_path):
            claim_rows, _ = self._load_claim_rows()
            for existing in self._latest_claim_rows(claim_rows):
                active = existing["status"] in {"claimed", "in-progress"}
                overlaps = existing["repo"].lower() == repo and (
                    existing["lane"] == lane or existing["lane"] == "all" or lane == "all"
                )
                if active and overlaps and existing["session"] != session_id:
                    raise BridgeError(
                        f"claim conflict: {repo}/{lane} is held by "
                        f"{existing['session']} (latest status {existing['status']} at {existing['ts']})"
                    )
            row = {
                "ts": isoformat(now),
                "repo": repo,
                "lane": lane,
                "status": "claimed",
                "session": session_id,
                "evidence": None,
                "note": note.strip()[:500],
            }
            self._append_claim_row(row)
        return row

    def update_claim(
        self,
        session_id: str,
        repo: str,
        lane: str,
        status: str,
        evidence: str | None = None,
        note: str = "",
        now: datetime | None = None,
    ) -> dict[str, Any]:
        now = now or utc_now()
        session_id = _safe_name(session_id, "session_id")
        repo = _safe_name(repo.lower(), "repo")
        lane = _safe_name(lane, "lane")
        if status not in {"in-progress", "done", "released"}:
            raise BridgeError("status must be in-progress, done, or released")
        with _file_lock(self.claims_lock_path):
            claim_rows, _ = self._load_claim_rows()
            current = next(
                (
                    row
                    for row in self._latest_claim_rows(claim_rows)
                    if row["repo"].lower() == repo and row["lane"] == lane
                ),
                None,
            )
            if not current:
                raise BridgeError("claim lane does not exist")
            if current["session"] != session_id:
                raise BridgeError("a claim may only be updated by its owning session")
            row = {
                "ts": isoformat(now),
                "repo": repo,
                "lane": lane,
                "status": status,
                "session": session_id,
                "evidence": evidence,
                "note": note.strip()[:500],
            }
            self._append_claim_row(row)
        return row

    def send(
        self,
        session_id: str,
        body: str,
        to_session: str | None = None,
        to_repo: str | None = None,
        subject: str = "coordination",
        priority: str = "normal",
        agent: str = "codex-desktop",
        now: datetime | None = None,
    ) -> dict[str, Any]:
        now = now or utc_now()
        body = body.strip()
        if not body:
            raise BridgeError("message body cannot be empty")
        if len(body) > MAX_MESSAGE_CHARS:
            raise BridgeError(f"message body exceeds {MAX_MESSAGE_CHARS} characters")
        if bool(to_session) == bool(to_repo):
            raise BridgeError("provide exactly one of to_session or to_repo")
        if priority not in {"low", "normal", "high", "critical"}:
            raise BridgeError("priority must be low, normal, high, or critical")
        with _file_lock(self.lock_path):
            events, _ = self._load_unlocked()
            session = self._sessions(events).get(session_id)
            if not session:
                raise BridgeError("session is not registered")
            event = self._make_event(
                "message.sent",
                session["repo"],
                agent,
                now,
                session_id=session_id,
                to_session=_safe_name(to_session, "to_session") if to_session else None,
                to_repo=_safe_name(to_repo.lower(), "to_repo") if to_repo else None,
                subject=subject.strip()[:160] or "coordination",
                priority=priority,
                body=body,
            )
            self._append_unlocked(event)
        return event

    @staticmethod
    def _message_state(
        events: list[dict[str, Any]], session_id: str
    ) -> tuple[list[dict[str, Any]], set[str], set[str]]:
        sessions = Ledger._sessions(events)
        session = sessions.get(session_id)
        if not session:
            raise BridgeError("session is not registered")
        messages = [
            event
            for event in events
            if event.get("event_type") == "message.sent"
            and (event.get("to_session") == session_id or event.get("to_repo") == session["repo"])
            and event.get("session_id") != session_id
        ]
        delivered = {
            str(event.get("referenced_message_id"))
            for event in events
            if event.get("event_type") == "message.delivered" and event.get("session_id") == session_id
        }
        acknowledged = {
            str(event.get("referenced_message_id"))
            for event in events
            if event.get("event_type") == "message.acknowledged" and event.get("session_id") == session_id
        }
        return messages, delivered, acknowledged

    def inbox(
        self,
        session_id: str,
        include_delivered: bool = True,
        include_acknowledged: bool = False,
    ) -> dict[str, Any]:
        events, errors = self.load()
        messages, delivered, acknowledged = self._message_state(events, session_id)
        result = []
        for event in messages:
            message_id = event["message_id"]
            if not include_acknowledged and message_id in acknowledged:
                continue
            if not include_delivered and message_id in delivered:
                continue
            result.append(
                {
                    "message_id": message_id,
                    "from_session": event["session_id"],
                    "from_repo": event["origin_repo"],
                    "to_session": event.get("to_session"),
                    "to_repo": event.get("to_repo"),
                    "subject": event["subject"],
                    "priority": event["priority"],
                    "body": event["body"],
                    "sent_at": event["timestamp"],
                    "delivered": message_id in delivered,
                    "acknowledged": message_id in acknowledged,
                }
            )
        result.sort(key=lambda item: item["sent_at"])
        return {"session_id": session_id, "messages": result, "integrity_errors": errors}

    def deliver_pending(
        self,
        session_id: str,
        agent: str = "codex-desktop",
        now: datetime | None = None,
    ) -> list[dict[str, Any]]:
        now = now or utc_now()
        with _file_lock(self.lock_path):
            events, _ = self._load_unlocked()
            session = self._sessions(events).get(session_id)
            if not session:
                raise BridgeError("session is not registered")
            messages, delivered, acknowledged = self._message_state(events, session_id)
            pending = [
                event
                for event in messages
                if event["message_id"] not in delivered and event["message_id"] not in acknowledged
            ]
            for message in pending:
                event = self._make_event(
                    "message.delivered",
                    session["repo"],
                    agent,
                    now,
                    session_id=session_id,
                    referenced_message_id=message["message_id"],
                )
                self._append_unlocked(event)
        return pending

    def acknowledge(
        self,
        session_id: str,
        message_id: str,
        agent: str = "codex-desktop",
        now: datetime | None = None,
    ) -> dict[str, Any]:
        now = now or utc_now()
        with _file_lock(self.lock_path):
            events, _ = self._load_unlocked()
            session = self._sessions(events).get(session_id)
            if not session:
                raise BridgeError("session is not registered")
            messages, _, acknowledged = self._message_state(events, session_id)
            if message_id not in {event["message_id"] for event in messages}:
                raise BridgeError("message is not addressed to this session")
            if message_id in acknowledged:
                raise BridgeError("message is already acknowledged")
            event = self._make_event(
                "message.acknowledged",
                session["repo"],
                agent,
                now,
                session_id=session_id,
                referenced_message_id=message_id,
            )
            self._append_unlocked(event)
        return event


TOOLS: list[dict[str, Any]] = [
    {
        "name": "galactic_status",
        "description": "List live/stale desktop sessions and active repo/lane claims.",
        "inputSchema": {
            "type": "object",
            "properties": {"include_stale": {"type": "boolean", "default": True}},
            "additionalProperties": False,
        },
        "annotations": {"readOnlyHint": True, "openWorldHint": False},
    },
    {
        "name": "galactic_claim",
        "description": "Append a claimed row to the shared ~/.agents repo/lane ledger.",
        "inputSchema": {
            "type": "object",
            "required": ["session_id", "repo", "lane"],
            "properties": {
                "session_id": {"type": "string"},
                "repo": {"type": "string"},
                "lane": {"type": "string"},
                "note": {"type": "string", "maxLength": 500},
            },
            "additionalProperties": False,
        },
        "annotations": {"readOnlyHint": False, "openWorldHint": False, "destructiveHint": False},
    },
    {
        "name": "galactic_claim_update",
        "description": "Append an in-progress, done, or released row for a claim owned by this session.",
        "inputSchema": {
            "type": "object",
            "required": ["session_id", "repo", "lane", "status"],
            "properties": {
                "session_id": {"type": "string"},
                "repo": {"type": "string"},
                "lane": {"type": "string"},
                "status": {"type": "string", "enum": ["in-progress", "done", "released"]},
                "evidence": {"type": ["string", "null"]},
                "note": {"type": "string", "maxLength": 500},
            },
            "additionalProperties": False,
        },
        "annotations": {"readOnlyHint": False, "openWorldHint": False, "destructiveHint": False},
    },
    {
        "name": "galactic_send",
        "description": "Send an integrity-protected coordination message to one session or repo inbox.",
        "inputSchema": {
            "type": "object",
            "required": ["session_id", "body"],
            "properties": {
                "session_id": {"type": "string"},
                "to_session": {"type": "string"},
                "to_repo": {"type": "string"},
                "subject": {"type": "string", "maxLength": 160, "default": "coordination"},
                "priority": {"type": "string", "enum": ["low", "normal", "high", "critical"], "default": "normal"},
                "body": {"type": "string", "maxLength": MAX_MESSAGE_CHARS},
            },
            "additionalProperties": False,
        },
        "annotations": {"readOnlyHint": False, "openWorldHint": False, "destructiveHint": False},
    },
    {
        "name": "galactic_inbox",
        "description": "Read messages addressed to this session or its repository.",
        "inputSchema": {
            "type": "object",
            "required": ["session_id"],
            "properties": {
                "session_id": {"type": "string"},
                "include_delivered": {"type": "boolean", "default": True},
                "include_acknowledged": {"type": "boolean", "default": False},
            },
            "additionalProperties": False,
        },
        "annotations": {"readOnlyHint": True, "openWorldHint": False},
    },
    {
        "name": "galactic_ack",
        "description": "Acknowledge one message addressed to this session or repo.",
        "inputSchema": {
            "type": "object",
            "required": ["session_id", "message_id"],
            "properties": {"session_id": {"type": "string"}, "message_id": {"type": "string"}},
            "additionalProperties": False,
        },
        "annotations": {"readOnlyHint": False, "openWorldHint": False, "destructiveHint": False},
    },
]


def call_tool(ledger: Ledger, name: str, arguments: dict[str, Any]) -> dict[str, Any]:
    if name == "galactic_status":
        return ledger.status(include_stale=arguments.get("include_stale", True))
    if name == "galactic_claim":
        return ledger.claim(**arguments)
    if name == "galactic_claim_update":
        return ledger.update_claim(**arguments)
    if name == "galactic_send":
        return ledger.send(**arguments)
    if name == "galactic_inbox":
        return ledger.inbox(**arguments)
    if name == "galactic_ack":
        return ledger.acknowledge(
            session_id=arguments["session_id"], message_id=arguments["message_id"]
        )
    raise BridgeError(f"unknown tool: {name}")


def dispatch_mcp(ledger: Ledger, request: dict[str, Any]) -> dict[str, Any] | None:
    request_id = request.get("id")
    method = request.get("method")
    if request_id is None:
        return None
    try:
        if method == "initialize":
            requested = request.get("params", {}).get("protocolVersion", "2025-06-18")
            result: Any = {
                "protocolVersion": requested,
                "capabilities": {"tools": {"listChanged": False}},
                "serverInfo": {"name": "demerzel-galactic-bridge", "version": "0.1.0"},
            }
        elif method == "ping":
            result = {}
        elif method == "tools/list":
            result = {"tools": TOOLS}
        elif method == "tools/call":
            params = request.get("params", {})
            value = call_tool(ledger, params.get("name", ""), params.get("arguments", {}))
            result = {
                "content": [{"type": "text", "text": json.dumps(value, indent=2, ensure_ascii=False)}],
                "structuredContent": value,
                "isError": False,
            }
        elif method == "shutdown":
            result = None
        else:
            return {
                "jsonrpc": "2.0",
                "id": request_id,
                "error": {"code": -32601, "message": f"method not found: {method}"},
            }
        return {"jsonrpc": "2.0", "id": request_id, "result": result}
    except (BridgeError, TypeError, KeyError) as exc:
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "error": {"code": -32602, "message": str(exc)},
        }
    except Exception as exc:  # keep the stdio server alive, without leaking a traceback
        return {
            "jsonrpc": "2.0",
            "id": request_id,
            "error": {"code": -32603, "message": f"internal bridge error: {type(exc).__name__}"},
        }


def serve(ledger: Ledger) -> int:
    for raw_line in sys.stdin.buffer:
        if not raw_line.strip():
            continue
        try:
            request = json.loads(raw_line)
            response = dispatch_mcp(ledger, request)
        except json.JSONDecodeError as exc:
            response = {
                "jsonrpc": "2.0",
                "id": None,
                "error": {"code": -32700, "message": f"parse error: {exc.msg}"},
            }
        if response is not None:
            sys.stdout.write(json.dumps(response, separators=(",", ":"), ensure_ascii=False) + "\n")
            sys.stdout.flush()
    return 0


def cli(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Galactic live session bridge")
    parser.add_argument("--state-root", type=Path, default=None)
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("serve", help="run the stdio MCP server")
    status_parser = subparsers.add_parser("status", help="print current bridge status")
    status_parser.add_argument("--active-only", action="store_true")
    subparsers.add_parser("claims-list", help="print the latest shared claim rows")
    claim_parser = subparsers.add_parser("claim", help="append a shared claimed row")
    claim_parser.add_argument("--session-id", required=True)
    claim_parser.add_argument("--repo", required=True)
    claim_parser.add_argument("--lane", required=True)
    claim_parser.add_argument("--note", default="")
    update_parser = subparsers.add_parser("claim-update", help="append a shared claim status row")
    update_parser.add_argument("--session-id", required=True)
    update_parser.add_argument("--repo", required=True)
    update_parser.add_argument("--lane", required=True)
    update_parser.add_argument("--status", choices=["in-progress", "done", "released"], required=True)
    update_parser.add_argument("--evidence", default=None)
    update_parser.add_argument("--note", default="")
    args = parser.parse_args(argv)
    ledger = Ledger(args.state_root)
    if args.command == "serve":
        return serve(ledger)
    if args.command == "status":
        print(json.dumps(ledger.status(include_stale=not args.active_only), indent=2))
        return 0
    if args.command == "claims-list":
        rows, errors = ledger._load_claim_rows()
        print(json.dumps({"claims_path": str(ledger.claims_path), "latest": ledger._latest_claim_rows(rows), "errors": errors}, indent=2))
        return 0 if not errors else 1
    if args.command == "claim":
        print(json.dumps(ledger.claim(args.session_id, args.repo, args.lane, args.note), indent=2))
        return 0
    if args.command == "claim-update":
        print(json.dumps(ledger.update_claim(args.session_id, args.repo, args.lane, args.status, args.evidence, args.note), indent=2))
        return 0
    return 2


if __name__ == "__main__":
    raise SystemExit(cli())
