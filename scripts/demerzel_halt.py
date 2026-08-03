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
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import demerzel_kit as kit

SCHEMA_VERSION = 1
DEFAULT_SCOPE = "loops-only"

# Single source of the structural rules (ADR-0003): every constraint lives in
# schemas/halt-all.schema.json. We validate with `jsonschema` when it can be
# imported — full parity with the PowerShell adapter's `Test-Json -Schema` — and
# otherwise fall back to a stdlib generic check that enforces the same constructs
# read from the schema. The fallback exists because this is the cross-repo
# EMERGENCY BRAKE: an operator must be able to halt on a bare-Python machine
# without `pip install`, so a missing package must never block a halt.
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


_TYPE_CHECKS = {
    "object": lambda v: isinstance(v, dict),
    "array": lambda v: isinstance(v, list),
    "string": lambda v: isinstance(v, str),
    "integer": lambda v: isinstance(v, int) and not isinstance(v, bool),
    "number": lambda v: isinstance(v, (int, float)) and not isinstance(v, bool),
    "boolean": lambda v: isinstance(v, bool),
    "null": lambda v: v is None,
}


def _validate_stdlib(instance: Any, schema: dict[str, Any], path: str = "") -> list[str]:
    """Stdlib JSON-Schema subset check (no third-party deps). Covers the
    constructs the marker schema uses: type (incl. unions), required,
    additionalProperties:false, const, enum, min/maxLength, pattern, items."""
    errors: list[str] = []
    where = path.rstrip(".") or "value"
    typ = schema.get("type")
    if typ is not None:
        types = typ if isinstance(typ, list) else [typ]
        if not any(_TYPE_CHECKS.get(t, lambda _v: True)(instance) for t in types):
            return [f"{where}: expected type {typ}, got {type(instance).__name__}"]
    if "const" in schema and instance != schema["const"]:
        errors.append(f"{where}: must equal {schema['const']!r}")
    if "enum" in schema and instance not in schema["enum"]:
        errors.append(f"{where}: must be one of {schema['enum']}")
    if isinstance(instance, str):
        if "minLength" in schema and len(instance) < schema["minLength"]:
            errors.append(f"{where}: shorter than minLength {schema['minLength']}")
        if "maxLength" in schema and len(instance) > schema["maxLength"]:
            errors.append(f"{where}: longer than maxLength {schema['maxLength']}")
        if "pattern" in schema and not re.search(schema["pattern"], instance):
            errors.append(f"{where}: does not match pattern {schema['pattern']}")
    if isinstance(instance, dict):
        props = schema.get("properties", {})
        for req in schema.get("required", []):
            if req not in instance:
                errors.append(f"{path}{req}: required field missing")
        if schema.get("additionalProperties") is False:
            for key in instance:
                if key not in props:
                    errors.append(f"{path}{key}: additional property not allowed")
        for key, subschema in props.items():
            if key in instance and instance[key] is not None:
                errors.extend(_validate_stdlib(instance[key], subschema, f"{path}{key}."))
    if isinstance(instance, list) and "items" in schema:
        for i, item in enumerate(instance):
            errors.extend(_validate_stdlib(item, schema["items"], f"{path}[{i}]."))
    return errors


def validate(marker: dict[str, Any]) -> list[str]:
    """Return a list of validation errors. Empty list means the marker is valid.

    Uses jsonschema (full parity with the PowerShell Test-Json adapter) when it
    is importable; falls back to the stdlib subset check so the emergency halt
    never fails for a missing package."""
    try:
        import jsonschema  # noqa: PLC0415 — optional dependency, imported lazily by design
    except ImportError:
        return _validate_stdlib(marker, _SCHEMA)
    validator = jsonschema.Draft202012Validator(_SCHEMA)
    return [e.message for e in sorted(validator.iter_errors(marker), key=lambda e: list(e.path))]


def cmd_halt(args: argparse.Namespace) -> int:
    marker: dict[str, Any] = {
        "schema_version": SCHEMA_VERSION,
        "halted_at": kit.now_iso(),
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
        kit.atomic_write(marker_path(), json.dumps(marker, indent=2))
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
    state = kit.halt_state(p, datetime.now(timezone.utc))
    if not state["present"]:
        print("Status: NOT halted (no marker present)")
        return 0
    if not state["valid"]:
        print(f"Status: marker present but INVALID ({state['reason']}): "
              f"{state['errors']}", file=sys.stderr)
        return 0
    marker = state["marker"]
    expires = marker.get("expires_at")
    if not state["active"]:
        print(f"Status: marker present but EXPIRED at {expires} (consumers treat as absent)")
        return 0
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
