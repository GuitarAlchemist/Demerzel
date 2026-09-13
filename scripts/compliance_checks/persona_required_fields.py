#!/usr/bin/env python3
"""Check P1: every persona declares the fields persona-requirements.md requires.

``estimator_pairing`` is required too, but it carries a waiver rule and a
resolution rule of its own, so it is checked in persona_estimator_pairing.py and
deliberately excluded here.
"""
from __future__ import annotations

from ._common import MirrorContext, Persona, violation

POLICY = "persona-requirements"
PERSONA_REQUIRED = ["name", "version", "description", "role", "capabilities",
                    "constraints", "voice", "affordances", "goal_directedness",
                    "estimator_pairing"]


def check(persona: Persona, ctx: MirrorContext) -> list:
    data = persona.data
    base = [k for k in PERSONA_REQUIRED if k != "estimator_pairing"]
    missing = [k for k in base if k not in data or data.get(k) in (None, "", [])]
    if not missing:
        return []
    return [violation(
        POLICY, f"persona '{persona.name}' missing fields: {missing}",
        "high" if "constraints" in missing else "medium")]
