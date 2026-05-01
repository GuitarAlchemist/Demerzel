#!/usr/bin/env python3
"""
Governance validator — two structural checks, pure stdlib.

(1) Every state/evolution/*.evolution.json validates against the enums in
    logic/governance-evolution.schema.json (artifact_type, event.type).
(2) Every personas/*.persona.yaml has a matching tests/behavioral/<name>-cases.md.

Exits non-zero on any violation. Prints one line per file with OK/FAIL.

Existed because Discussion #242 (2026-04-30) revealed that the compound cycle
had been running on a 27-day-stale evolution log without anything noticing.
The deeper cause: schema drift sat undetected because nothing checked. This
script is the check.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SCHEMA = REPO / "logic" / "governance-evolution.schema.json"
EVOLUTION_DIR = REPO / "state" / "evolution"
PERSONAS_DIR = REPO / "personas"
TESTS_DIR = REPO / "tests" / "behavioral"


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


def check_personas_have_tests() -> tuple[int, int]:
    """Every persona must have a behavioral test file. CLAUDE.md persona-requirements rule."""
    test_files = {p.stem for p in TESTS_DIR.glob("*-cases.md")}
    ok = bad = 0
    for persona_path in sorted(PERSONAS_DIR.glob("*.persona.yaml")):
        name = persona_path.name.removesuffix(".persona.yaml")
        expected = f"{name}-cases"
        if expected in test_files:
            ok += 1
            print(f"OK   personas/{persona_path.name} -> tests/behavioral/{expected}.md")
        else:
            bad += 1
            print(f"FAIL personas/{persona_path.name} -> missing tests/behavioral/{expected}.md")
    return ok, bad


def main() -> int:
    print("=== Evolution log: schema enum validation ===")
    e_ok, e_bad = check_evolution_enums()
    print(f"Result: {e_ok} valid, {e_bad} invalid\n")

    print("=== Personas: behavioral test coverage ===")
    p_ok, p_bad = check_personas_have_tests()
    print(f"Result: {p_ok} covered, {p_bad} missing\n")

    total_bad = e_bad + p_bad
    if total_bad:
        print(f"FAILED: {total_bad} violation(s) — see above.")
        return 1
    print("PASSED: all checks green.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
