#!/usr/bin/env python3
"""
Demerzel HALT-ALL producer — writes / reads / deletes the cross-repo overseer
halt marker that pauses every /auto-optimize loop across every repo in the
GuitarAlchemist ecosystem (GA, ix, Demerzel, tars).

Implements the producer side of the contract drafted in GA:

  ga/docs/contracts/2026-05-16-overseer-halt-marker.contract.md
  ga/docs/contracts/overseer-halt-marker.schema.json

Consumers (e.g. ga/.claude/skills/auto-optimize/SKILL.md Step 0) read
~/.demerzel/HALT-ALL before each cycle and pause if the marker is present,
valid, and not expired. This script is the operator-facing tool for putting
that marker in place.

Phase 1 deliverable per docs/plans/2026-05-16-arch-demerzel-overseer-extension
-plan.md in GA. No ACP server endpoint yet — Demerzel does not currently
ship an HTTP server; this CLI fills the same role as the planned `POST /halt`
endpoint until that lands.

Usage:

  python scripts/demerzel_halt.py halt --reason "Investigating cost burn"
  python scripts/demerzel_halt.py halt --reason "Mobile freeze" --expires-at 2026-05-19T00:00:00Z
  python scripts/demerzel_halt.py resume
  python scripts/demerzel_halt.py status

Exit codes:

  0  — success (halt set, resumed, or status reported)
  1  — usage error
  2  — schema-validation failure (refuses to write malformed marker)
  3  — IO failure (could not write marker, race against atomic-rename)

Security:

  - Uses atomic write (temp file + os.replace) so consumers never see a
    half-written marker. Respects the "atomic write" obligation in the
    contract.
  - Validates against the contract before writing.
  - Archives the prior marker (if present) to ~/.demerzel/halts/ on resume
    so the audit log (Phase 2) can reconstruct the timeline.
  - Refuses to write markers with `schema_version != 1` (the v0.1 wire
    format).
"""
from __future__ import annotations

import argparse
import getpass
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

SCHEMA_VERSION = 1
DEFAULT_SCOPE = "loops-only"

# Single source of the structural constraints (ADR-0003): the scope enum and the
# reason length live in schemas/halt-all.schema.json, not hardcoded here. This
# Python adapter stays stdlib-only (the halt tool must not depend on jsonschema);
# the PowerShell adapter validates the full schema via Test-Json -Schema.
_SCHEMA = json.loads(
    (Path(__file__).resolve().parent.parent / "schemas" / "halt-all.schema.json").read_text(
        encoding="utf-8"
    )
)
VALID_SCOPES = set(_SCHEMA["properties"]["scope"]["enum"])
_REASON_MAX = _SCHEMA["properties"]["reason"]["maxLength"]


def marker_dir() -> Path:
    return Path.home() / ".demerzel"


def marker_path() -> Path:
    return marker_dir() / "HALT-ALL"


def archive_dir() -> Path:
    return marker_dir() / "halts"


def now_rfc3339() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def validate(marker: dict[str, Any]) -> list[str]:
    """Return a list of validation errors. Empty list means the marker is valid."""
    errors: list[str] = []
    if marker.get("schema_version") != SCHEMA_VERSION:
        errors.append(
            f"schema_version must be {SCHEMA_VERSION}; got {marker.get('schema_version')!r}"
        )
    halted_at = marker.get("halted_at")
    if not isinstance(halted_at, str) or "T" not in halted_at:
        errors.append("halted_at must be an RFC3339 UTC timestamp string")
    reason = marker.get("reason")
    if not isinstance(reason, str) or not (1 <= len(reason) <= _REASON_MAX):
        errors.append(f"reason must be a 1-{_REASON_MAX} character string")
    scope = marker.get("scope", DEFAULT_SCOPE)
    if scope not in VALID_SCOPES:
        errors.append(f"scope must be one of {sorted(VALID_SCOPES)}; got {scope!r}")
    expires_at = marker.get("expires_at")
    if expires_at is not None and not isinstance(expires_at, str):
        errors.append("expires_at must be null or an RFC3339 UTC timestamp string")
    exempt = marker.get("exempt_agents")
    if exempt is not None and not (
        isinstance(exempt, list) and all(isinstance(a, str) for a in exempt)
    ):
        errors.append("exempt_agents must be null or a list of strings")
    return errors


def atomic_write(path: Path, content: str) -> None:
    """Write content atomically: temp file + os.replace. Avoids torn reads."""
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(content, encoding="utf-8")
    os.replace(tmp, path)


def cmd_halt(args: argparse.Namespace) -> int:
    marker: dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "halted_at": now_rfc3339(),
        "halted_by": args.halted_by or f"demerzel-cli:{getpass.getuser()}",
        "reason": args.reason,
        "scope": args.scope,
        "expires_at": args.expires_at,
        "exempt_agents": args.exempt_agents or [],
    }
    if args.incident_url or args.issue_ref:
        marker["links"] = {}
        if args.incident_url:
            marker["links"]["incident_url"] = args.incident_url
        if args.issue_ref:
            marker["links"]["issue_ref"] = args.issue_ref

    errors = validate(marker)
    if errors:
        print("[FAIL] Marker validation failed:", file=sys.stderr)
        for e in errors:
            print(f"  - {e}", file=sys.stderr)
        return 2

    try:
        atomic_write(marker_path(), json.dumps(marker, indent=2))
    except OSError as exc:
        print(f"[FAIL] Could not write marker: {exc}", file=sys.stderr)
        return 3

    print(f"[OK] HALT-ALL written to {marker_path()}")
    print(f"  reason: {marker['reason']}")
    print(f"  halted_by: {marker['halted_by']}")
    if marker["expires_at"]:
        print(f"  expires_at: {marker['expires_at']}")
    if marker["exempt_agents"]:
        print(f"  exempt_agents: {marker['exempt_agents']}")
    return 0


def cmd_resume(_args: argparse.Namespace) -> int:
    p = marker_path()
    if not p.exists():
        print("No HALT-ALL marker is currently set. Nothing to resume.")
        return 0
    try:
        prior = p.read_text(encoding="utf-8")
    except OSError as exc:
        print(f"[FAIL] Could not read existing marker: {exc}", file=sys.stderr)
        return 3
    archive_dir().mkdir(parents=True, exist_ok=True)
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H-%M-%SZ")
    archive_path = archive_dir() / f"{stamp}-resumed.json"
    try:
        archive_path.write_text(prior, encoding="utf-8")
        p.unlink()
    except OSError as exc:
        print(f"[FAIL] Could not archive + remove marker: {exc}", file=sys.stderr)
        return 3
    print(f"[OK] HALT-ALL lifted. Prior marker archived to {archive_path}")
    return 0


def cmd_status(_args: argparse.Namespace) -> int:
    p = marker_path()
    if not p.exists():
        print("Status: NOT halted (no marker present)")
        return 0
    try:
        marker = json.loads(p.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"Status: marker present but UNREADABLE — {exc}", file=sys.stderr)
        return 0
    errors = validate(marker)
    if errors:
        print("Status: marker present but INVALID:")
        for e in errors:
            print(f"  - {e}")
        return 0
    expires = marker.get("expires_at")
    if expires:
        try:
            exp_dt = datetime.fromisoformat(expires.replace("Z", "+00:00"))
            if exp_dt < datetime.now(timezone.utc):
                print(f"Status: marker present but EXPIRED at {expires} (consumers treat as absent)")
                return 0
        except ValueError:
            pass
    print("Status: HALTED")
    print(f"  halted_at: {marker.get('halted_at')}")
    print(f"  halted_by: {marker.get('halted_by')}")
    print(f"  reason: {marker.get('reason')}")
    print(f"  scope: {marker.get('scope', DEFAULT_SCOPE)}")
    if expires:
        print(f"  expires_at: {expires}")
    if marker.get("exempt_agents"):
        print(f"  exempt_agents: {marker['exempt_agents']}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description="Demerzel HALT-ALL producer — pause every /auto-optimize loop across the ecosystem."
    )
    sub = p.add_subparsers(dest="cmd", required=True)

    halt = sub.add_parser("halt", help="Write the HALT-ALL marker.")
    halt.add_argument("--reason", required=True, help="Human-readable reason (1-500 chars).")
    halt.add_argument("--halted-by", default=None, help="Override the halted_by identifier.")
    halt.add_argument("--scope", default=DEFAULT_SCOPE, choices=sorted(VALID_SCOPES))
    halt.add_argument("--expires-at", default=None, help="RFC3339 UTC timestamp after which the halt lifts.")
    halt.add_argument("--exempt-agents", nargs="*", default=None, help="Agent IDs allowed to ignore this halt.")
    halt.add_argument("--incident-url", default=None, help="Optional URL for incident tracking.")
    halt.add_argument("--issue-ref", default=None, help="Optional issue reference (e.g. 'ga#999').")
    halt.set_defaults(func=cmd_halt)

    resume = sub.add_parser("resume", help="Remove the HALT-ALL marker.")
    resume.set_defaults(func=cmd_resume)

    status = sub.add_parser("status", help="Report whether HALT-ALL is currently in effect.")
    status.set_defaults(func=cmd_status)

    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
