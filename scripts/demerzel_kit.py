#!/usr/bin/env python3
"""
Demerzel emitter kit — the shared substrate for the scripts/ layer.

Demerzel has no runtime app; the scripts/ emitters (council_emit, qa_tribunal_emit,
run_afk_cycle, apply_ml_feedback, compliance_report, run_ml_feedback_cycle) ARE the
operational code. Each was re-deriving the same four primitives: a UTC provenance
stamp (`_now_iso`, ×7), a crash-safe write (`atomic_write`, ×6), ad-hoc schema
validation (or none), and a `gh` subprocess wrapper (×3, with three different error
contracts). None of the gh/filesystem calls were an overridable seam, which is why
only 2 of 12 scripts had tests.

This module is the Python sibling of the PowerShell `DigestState.psm1` deep module
and the `llm_call.sh` / `post_discussion.sh` shell seams: one small interface that
owns those primitives once, with the `gh` runner as an injectable seam so the
emitters become testable through their interface.

Interface:
  now_iso()                         -> str          # the one true UTC stamp
  atomic_write(path, content)       -> None         # temp-file + os.replace
  validate(data, schema)            -> None         # raises on invalid; degrades if jsonschema absent
  halt_state(path, now)             -> dict         # schema-backed, fail-closed HALT-ALL facts
  write_artifact(path, data, schema=...) -> Path    # validate (optional) then atomic-write JSON
  gh_json(args, *, run=...)         -> dict|list|None
  gh_text(args, *, ok_nonzero=..., run=...) -> str|None

Design notes:
  * write_artifact does NOT inject timestamps. Domain artifacts carry their own
    semantically-named ones (`timestamp`, `halted_at`, `decided_at`) and several
    schemas set `additionalProperties: false`, so a generic envelope stamp would
    fail validation. Stamp with now_iso() in the caller.
  * validate() lazily imports jsonschema (optional dependency, matching
    demerzel_halt.py) and degrades to a stderr warning when it is absent, so an
    emitter still runs in a stdlib-only environment.
  * The `run` parameter on gh_json/gh_text is the test seam: pass a fake callable
    that returns a CompletedProcess-shaped object. Callers may also patch
    `demerzel_kit.gh_json` / `gh_text` directly.

Stdlib only at import time (jsonschema is imported lazily inside validate()).
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_DIR = ROOT / "schemas"


def now_iso() -> str:
    """UTC RFC3339 stamp, 'YYYY-MM-DDTHH:MM:SSZ'. The single timestamp helper the
    scripts/ emitters share (was copy-pasted as `_now_iso` / `now_rfc3339` ×7)."""
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def atomic_write(path: Path, content: str) -> None:
    """Write `content` atomically: temp file + os.replace, so a crash mid-write
    never leaves a torn artifact on disk. Promoted from demerzel_halt.py, which
    held the canonical copy."""
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(content, encoding="utf-8")
    os.replace(tmp, path)


def validate(data: object, schema: str) -> None:
    """Validate `data` against `schemas/<schema>.schema.json`. Raises
    jsonschema.ValidationError on invalid data.

    `schema` is a path under schemas/ without the `.schema.json` suffix, e.g.
    "council-verdict" or "contracts/qa-verdict".

    jsonschema is imported lazily (optional dependency, matching demerzel_halt.py).
    When it is absent the check degrades to a stderr warning and returns, so an
    emitter still runs in a stdlib-only environment — validation is enforced
    wherever jsonschema is installed (CI, the governor env)."""
    try:
        import jsonschema  # noqa: PLC0415 — optional dependency, imported lazily by design
    except ImportError:
        print(f"warn: jsonschema absent; skipped validation against {schema}",
              file=sys.stderr)
        return
    spec = json.loads((SCHEMA_DIR / f"{schema}.schema.json").read_text(encoding="utf-8"))
    jsonschema.validate(data, spec)


def halt_state(path: Path, now: datetime) -> dict:
    """Return authoritative facts for one HALT-ALL marker.

    Unlike the optional validation used by ordinary emitters, a present halt
    marker must be validated. Unreadable data, schema failures, and an absent
    jsonschema dependency all fail closed as an active halt. ``now`` is supplied
    by the caller so expiry remains deterministic and evaluated at point of use.
    """
    try:
        marker = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return {"present": False, "valid": True, "active": False,
                "reason": None, "errors": None, "marker": None}
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        return {"present": True, "valid": False, "active": True,
                "reason": "halt_all_unreadable", "errors": str(exc), "marker": None}

    try:
        import jsonschema  # noqa: PLC0415 — mandatory only when a halt marker exists
    except ImportError as exc:
        return {"present": True, "valid": False, "active": True,
                "reason": "halt_all_validation_unavailable", "errors": str(exc),
                "marker": None}

    try:
        spec = json.loads(
            (SCHEMA_DIR / "halt-all.schema.json").read_text(encoding="utf-8")
        )
        jsonschema.validate(marker, spec)
    except (OSError, UnicodeError, json.JSONDecodeError, jsonschema.ValidationError,
            jsonschema.SchemaError) as exc:
        return {"present": True, "valid": False, "active": True,
                "reason": "halt_all_invalid", "errors": str(exc), "marker": None}

    active = True
    errors = None
    expires_at = marker.get("expires_at")
    if expires_at:
        try:
            expiry = datetime.fromisoformat(expires_at.replace("Z", "+00:00"))
            active = not now > expiry
        except (TypeError, ValueError) as exc:
            # The schema constrains the representation but a calendar-invalid
            # timestamp can still match its regex. Keep the halt active.
            errors = str(exc)

    return {"present": True, "valid": True, "active": active,
            "reason": marker["reason"], "errors": errors, "marker": marker}


def write_artifact(path: Path, data: object, *, schema: str | None = None) -> Path:
    """Emit a governance artifact: validate against `schema` (if given), then
    atomic-write as pretty JSON with a trailing newline. The single seam through
    which the scripts/ emitters reach disk.

    Raises before writing if validation fails — invalid JSON never lands on disk
    (the gap that previously let a read-time consumer choke on it). Does not stamp
    timestamps; see the module docstring."""
    if schema is not None:
        validate(data, schema)
    atomic_write(path, json.dumps(data, indent=2) + "\n")
    return path


def gh_json(args: list[str], *, run=subprocess.run) -> dict | list | None:
    """Run `gh <args>` and parse stdout as JSON. Returns None on any failure
    (non-zero exit, unavailable gh, non-JSON output) after a stderr warning — the
    non-raising contract the emitters expect.

    `run` is the injectable test seam."""
    try:
        p = run(["gh", *args], capture_output=True, text=True, timeout=60)
    except (OSError, subprocess.TimeoutExpired) as exc:
        print(f"warn: gh {' '.join(args)} unavailable: {exc}", file=sys.stderr)
        return None
    if p.returncode != 0:
        print(f"warn: gh {' '.join(args)} failed: {p.stderr.strip()[:160]}", file=sys.stderr)
        return None
    try:
        return json.loads(p.stdout or "null")
    except json.JSONDecodeError as exc:
        print(f"warn: gh {' '.join(args)} non-JSON: {exc}", file=sys.stderr)
        return None


def gh_text(args: list[str], *, ok_nonzero: bool = False, run=subprocess.run) -> str | None:
    """Run `gh <args>` and return stdout as text. Returns None on failure.

    ok_nonzero=True keeps stdout even when gh exits non-zero — e.g. `gh pr checks`
    exits non-zero when a check has failed, but the check table is still valid
    output that the caller needs to parse.

    `run` is the injectable test seam."""
    try:
        p = run(["gh", *args], capture_output=True, text=True, timeout=60)
    except (OSError, subprocess.TimeoutExpired) as exc:
        print(f"warn: gh {' '.join(args)} unavailable: {exc}", file=sys.stderr)
        return None
    if p.returncode != 0 and not ok_nonzero:
        print(f"warn: gh {' '.join(args)} failed: {p.stderr.strip()[:160]}", file=sys.stderr)
        return None
    return p.stdout or ""
