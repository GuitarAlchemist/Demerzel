#!/usr/bin/env python3
"""
Governance validator — evolution-log enum check, pure stdlib.

Every state/evolution/*.evolution.json validates against the enums in
logic/governance-evolution.schema.json (artifact_type, event.type).

Exits non-zero on any violation. Prints one line per file with OK/FAIL.

Existed because Discussion #242 (2026-04-30) revealed that the compound cycle
had been running on a 27-day-stale evolution log without anything noticing.
The deeper cause: schema drift sat undetected because nothing checked. This
script is the check.

The persona->test coverage check formerly here now lives in the governance
manifest (scripts/build_manifest.py, ADR-0001) — harvested as a `has_test`
edge so it isn't checked in two places.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SCHEMA = REPO / "logic" / "governance-evolution.schema.json"
EVOLUTION_DIR = REPO / "state" / "evolution"


def check_evolution_enums() -> tuple[int, int]:
    """Validate artifact_type and event.type against the schema enums."""
    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    at_enum = set(schema["properties"]["artifact_type"]["enum"])
    et_enum = set(schema["properties"]["events"]["items"]["properties"]["type"]["enum"])

    ok = bad = 0
    for path in sorted(EVOLUTION_DIR.glob("*.evolution.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        issues: list[str] = []
        if data.get("artifact_type") not in at_enum:
            issues.append(f"artifact_type={data.get('artifact_type')!r} not in enum")
        for ev in data.get("events", []):
            if ev.get("type") not in et_enum:
                issues.append(f"event.type={ev.get('type')!r} not in enum")
        if issues:
            bad += 1
            print(f"FAIL {path.relative_to(REPO)}")
            for issue in issues:
                print(f"  - {issue}")
        else:
            ok += 1
            print(f"OK   {path.relative_to(REPO)}")
    return ok, bad


def main() -> int:
    print("=== Evolution log: schema enum validation ===")
    e_ok, e_bad = check_evolution_enums()
    print(f"Result: {e_ok} valid, {e_bad} invalid\n")

    if e_bad:
        print(f"FAILED: {e_bad} violation(s) — see above.")
        return 1
    print("PASSED: all checks green.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
