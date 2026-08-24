#!/usr/bin/env python3
"""Check P4: a persona pairs with an estimator, and that estimator exists.

Required UNLESS the file documents an explicit waiver (e.g. skeptical-auditor IS
the neutral estimator others pair with) — which is why this check reads the whole
file, not just the front-matter the other persona checks work from.
"""
from __future__ import annotations

from ._common import MirrorContext, Persona, violation

POLICY = "persona-requirements"
WAIVER_PHRASES = ("no estimator_pairing", "no estimator pairing",
                  "is the neutral estimator")


def check(persona: Persona, ctx: MirrorContext) -> list:
    raw = persona.path.read_text(encoding="utf-8").lower()
    ep = persona.data.get("estimator_pairing")
    ep_name = ep.get("persona") or ep.get("name") if isinstance(ep, dict) else ep
    waived = any(phrase in raw for phrase in WAIVER_PHRASES)
    if not ep_name and not waived:
        return [violation(
            POLICY, f"persona '{persona.name}' has no estimator_pairing", "high")]
    if ep_name and ep_name not in ctx.persona_names:
        return [violation(
            POLICY,
            f"persona '{persona.name}' estimator_pairing '{ep_name}' is not a known persona",
            "medium")]
    return []
