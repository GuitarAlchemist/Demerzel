#!/usr/bin/env python3
"""Check P2: every persona is covered by a behavioral test.

Coverage is a substring match of the persona name against the joined stems of
tests/behavioral/*.md — the same loose match the original run_checks() used, so
a test file named ``<persona>-cases.md`` counts.
"""
from __future__ import annotations

from pathlib import Path

from ._common import MirrorContext, Persona, violation

POLICY = "contributing-rules"


def load_test_blob(mirror: Path):
    """Return (blob, count) for mirror/tests/behavioral/*.md."""
    test_files = list((mirror / "tests" / "behavioral").glob("*.md"))
    return " ".join(t.stem for t in test_files), len(test_files)


def check(persona: Persona, ctx: MirrorContext) -> list:
    if persona.name and persona.name not in ctx.test_blob:
        return [violation(
            POLICY, f"persona '{persona.name}' has no behavioral test", "high")]
    return []
