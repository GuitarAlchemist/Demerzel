#!/usr/bin/env python3
"""The individual governance checks behind scripts/compliance_report.py.

One module per check, so a check can be unit-tested against a fixture without
mocking glob() across five artifact tiers, and so an eighth check is a new file
plus one registry line rather than surgery on a 95-line function:

  persona_yaml_valid          personas/*.persona.yaml parses
  persona_required_fields     P1  required fields present
  persona_behavioral_test     P2  behavioral-test coverage
  persona_semver              P3  persona version is N.N.N
  persona_estimator_pairing   P4  estimator_pairing present and resolvable
  policy_semver               P3  policy version is N.N.N
  schemas_valid_json          S1  schemas/*.schema.json parses
  belief_staleness            B1  beliefs newer than STALE_DAYS

Ordering is part of the contract. Reports are hashed over their serialized form
(compliance_report._attach_integrity), so run_checks() reproduces the original
emission order exactly: YAML-validity for every persona first, then the persona
checks **persona-major** (all of persona A's violations, then all of persona B's
— not all P1s, then all P2s), then policies, schemas, beliefs.

The submodules import each other relatively, so the package keeps one identity
whether it is reached as ``scripts.compliance_checks`` (package mode) or as
``compliance_checks`` (direct execution of scripts/compliance_report.py).
"""
from __future__ import annotations

from pathlib import Path

from . import (belief_staleness, persona_behavioral_test,
               persona_estimator_pairing, persona_required_fields,
               persona_semver, persona_yaml_valid, policy_semver,
               schemas_valid_json)
from ._common import CheckOutcome, MirrorContext, Persona

# Run once per persona, in this order, for each persona in turn.
PERSONA_CHECKS = (
    ("P1-persona-required-fields", persona_required_fields.check),
    ("P2-behavioral-test-coverage", persona_behavioral_test.check),
    ("P3-persona-semver", persona_semver.check),
    ("P4-estimator-pairing", persona_estimator_pairing.check),
)

# Run once per mirror, in this order, after the persona checks.
MIRROR_CHECKS = (
    ("policy-semver", policy_semver.check),
    ("schemas-valid-json", schemas_valid_json.check),
    ("belief-staleness", belief_staleness.check),
)

# Every check and the module that owns it — exactly one module per check.
CHECK_MODULES = {
    "persona-yaml-valid": persona_yaml_valid,
    "P1-persona-required-fields": persona_required_fields,
    "P2-behavioral-test-coverage": persona_behavioral_test,
    "P3-persona-semver": persona_semver,
    "P4-estimator-pairing": persona_estimator_pairing,
    "policy-semver": policy_semver,
    "schemas-valid-json": schemas_valid_json,
    "belief-staleness": belief_staleness,
}

__all__ = ["CHECK_MODULES", "CheckOutcome", "MIRROR_CHECKS", "MirrorContext",
           "PERSONA_CHECKS", "Persona", "build_context", "run_checks"]


def build_context(mirror: Path):
    """Load the persona tier once and assemble what the persona checks read.
    Returns (ctx, violations, counts) — the violations are persona_yaml_valid's."""
    personas, violations = persona_yaml_valid.load_personas(mirror)
    test_blob, test_count = persona_behavioral_test.load_test_blob(mirror)
    ctx = MirrorContext(
        mirror=mirror,
        personas=personas,
        # Declared names only: an unnamed persona contributes None, so nothing
        # can pair with it. This is the original behaviour.
        persona_names=frozenset(p.data.get("name") for p in personas),
        test_blob=test_blob,
    )
    counts = {"personas": len(personas), "behavioral_tests": test_count}
    return ctx, violations, counts


def run_checks(mirror: Path) -> dict:
    """Return {violations: [...], checked: {counts}}. Pure governance checks."""
    ctx, violations, checked = build_context(mirror)

    for persona in ctx.personas:
        for _name, check in PERSONA_CHECKS:
            violations.extend(check(persona, ctx))

    for _name, check in MIRROR_CHECKS:
        outcome = check(ctx)
        violations.extend(outcome.violations)
        checked.update(outcome.counts)

    return {"violations": violations, "checked": checked}
