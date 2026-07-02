#!/usr/bin/env python3
"""
Seldon Schema Validator

Validates the Seldon JSON schemas under `schemas/seldon/` against the JSON Schema Draft 2020-12 meta-schema.
Exits non-zero on any violation. Prints one line per file with OK/FAIL.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path
from jsonschema.validators import Draft202012Validator
from jsonschema.exceptions import ValidationError, SchemaError

REPO = Path(__file__).resolve().parent.parent
SELDON_SCHEMAS_DIR = REPO / "schemas" / "seldon"

def check_seldon_schemas() -> tuple[int, int]:
    """Validate each Seldon schema against Draft 2020-12 meta-schema."""
    ok = bad = 0

    if not SELDON_SCHEMAS_DIR.exists():
        print(f"Directory {SELDON_SCHEMAS_DIR.relative_to(REPO)} does not exist.")
        return 0, 0

    for path in sorted(SELDON_SCHEMAS_DIR.glob("*.schema.json")):
        try:
            schema = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            print(f"FAIL {path.relative_to(REPO)}")
            print(f"  - Invalid JSON: {e}")
            bad += 1
            continue

        try:
            Draft202012Validator.check_schema(schema)
            print(f"OK   {path.relative_to(REPO)}")
            ok += 1
        except SchemaError as e:
            print(f"FAIL {path.relative_to(REPO)}")
            print(f"  - Invalid schema structure: {e.message}")
            bad += 1

    return ok, bad

def main() -> int:
    print("=== Seldon schemas: Draft 2020-12 validation ===")
    s_ok, s_bad = check_seldon_schemas()
    print(f"Result: {s_ok} valid, {s_bad} invalid\n")

    if s_bad:
        print(f"FAILED: {s_bad} violation(s) — see above.")
        return 1
    print("PASSED: all seldon schemas valid.")
    return 0

if __name__ == "__main__":
    sys.exit(main())