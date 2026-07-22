#!/usr/bin/env python3
"""
Governance validator — evolution-log enum check plus the first Galactic
Protocol contract-instance gate.

Every state/evolution/*.evolution.json validates against the enums in
logic/governance-evolution.schema.json (artifact_type, event.type) — pure
stdlib. Every state/oversight/compliance-reports/*.json validates against
schemas/contracts/compliance-report.schema.json — needs `jsonschema`,
degrades to a printed skip when it is not installed.

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
CONTRACTS_DIR = REPO / "schemas" / "contracts"
REPORTS_DIR = REPO / "state" / "oversight" / "compliance-reports"


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


def check_compliance_reports(reports_dir: Path = REPORTS_DIR) -> tuple[int, int]:
    """Validate compliance-report instances against their contract schema.

    First Galactic Protocol contract-instance gate (galactic-protocol.md
    v1.3.0 §Implementation Status): compliance-report is the only message
    type with a live emitter (scripts/compliance_report.py), so it is the
    only one gated here — no gate without instances to gate.

    Strategy: the contract schema pulls in integrity-fields.schema.json via a
    relative `allOf` $ref that jsonschema won't resolve without a registry, so
    we validate the body schema (allOf stripped) and the integrity-fields
    schema separately — together equivalent to the full contract. Verified
    2026-07-21: all 111 live instances pass BOTH parts (the emitter attaches
    integrity fields even though no receiver verifies them — see the v1.3.0
    status table), so this gate enforces the full contract, not a weakened one.

    Degrades gracefully: `jsonschema` missing -> printed skip (the CI validate
    job installs it); directory absent/empty -> printed note, not a failure
    (instances are gitignored runtime state, present only where the daily
    driver runs).
    """
    try:
        import jsonschema
    except ImportError:
        print("SKIP jsonschema not installed — compliance-report instances not validated")
        return 0, 0

    files = sorted(reports_dir.glob("*.json")) if reports_dir.is_dir() else []
    if not files:
        print("NOTE no compliance-report instances on disk (gitignored runtime state) — nothing to validate")
        return 0, 0

    body = json.loads((CONTRACTS_DIR / "compliance-report.schema.json").read_text(encoding="utf-8"))
    body.pop("allOf", None)  # relative $ref to integrity-fields — validated separately below
    integrity = json.loads((CONTRACTS_DIR / "integrity-fields.schema.json").read_text(encoding="utf-8"))
    body_validator = jsonschema.Draft202012Validator(body)
    integrity_validator = jsonschema.Draft202012Validator(integrity)

    ok = bad = 0
    for path in files:
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError) as exc:
            bad += 1
            print(f"FAIL {path.name}")
            print(f"  - not valid JSON: {exc}")
            continue
        issues = [e.message for e in body_validator.iter_errors(data)]
        issues += [f"integrity: {e.message}" for e in integrity_validator.iter_errors(data)]
        if issues:
            bad += 1
            print(f"FAIL {path.name}")
            for issue in issues:
                print(f"  - {issue}")
        else:
            ok += 1
            print(f"OK   {path.name}")
    return ok, bad


def main() -> int:
    print("=== Evolution log: schema enum validation ===")
    e_ok, e_bad = check_evolution_enums()
    print(f"Result: {e_ok} valid, {e_bad} invalid\n")

    print("=== Compliance reports: contract instance validation ===")
    c_ok, c_bad = check_compliance_reports()
    print(f"Result: {c_ok} valid, {c_bad} invalid\n")

    total_bad = e_bad + c_bad
    if total_bad:
        print(f"FAILED: {total_bad} violation(s) — see above.")
        return 1
    print("PASSED: all checks green.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
