"""Tests for scripts/demerzel_halt.py marker validation (Candidate 4).

Verifies BOTH validation paths agree with the schema:
  - validate()        — jsonschema when importable (full parity with Test-Json)
  - _validate_stdlib() — the bare-Python fallback the emergency halt relies on

Run: python tests/python/test_demerzel_halt_validate.py   (or via pytest)
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent / "scripts"))
import demerzel_halt as dh  # noqa: E402

VALID = {"schema_version": 1, "halted_at": "2026-06-21T00:00:00Z", "reason": "investigating cost burn"}


def _both(marker):
    """(jsonschema-path errors, stdlib-path errors) for a marker."""
    return dh.validate(marker), dh._validate_stdlib(marker, dh._SCHEMA)


def test_valid_marker_passes_both_paths():
    js, std = _both(VALID)
    assert js == [], js
    assert std == [], std


def test_valid_with_optional_scope_and_expiry():
    m = {**VALID, "scope": "global", "expires_at": "2026-06-22T00:00:00Z"}
    js, std = _both(m)
    assert js == [] and std == [], (js, std)


def test_bad_scope_rejected_by_both():
    js, std = _both({**VALID, "scope": "everything"})
    assert js and std, (js, std)


def test_missing_required_reason_rejected_by_both():
    m = {"schema_version": 1, "halted_at": "2026-06-21T00:00:00Z"}
    js, std = _both(m)
    assert js and std, (js, std)


def test_malformed_timestamp_rejected_by_both():
    # Parity improvement: the old hand-rolled check only required a 'T'.
    js, std = _both({**VALID, "halted_at": "yesterdayTmorning"})
    assert js and std, (js, std)


def test_additional_property_rejected_by_both():
    # Parity improvement: additionalProperties:false now enforced in stdlib too.
    js, std = _both({**VALID, "bogus_field": "x"})
    assert js and std, (js, std)


def test_overlong_reason_rejected_by_both():
    js, std = _both({**VALID, "reason": "x" * 600})
    assert js and std, (js, std)


if __name__ == "__main__":
    failures = 0
    for name, fn in sorted(globals().items()):
        if name.startswith("test_") and callable(fn):
            try:
                fn()
                print(f"PASS {name}")
            except AssertionError as e:
                failures += 1
                print(f"FAIL {name}: {e}")
    print(f"\n{'OK' if not failures else str(failures) + ' FAILED'}")
    sys.exit(1 if failures else 0)
