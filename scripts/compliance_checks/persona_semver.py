#!/usr/bin/env python3
"""Check P3 (persona tier): a persona's declared version is N.N.N."""
from __future__ import annotations

from ._common import MirrorContext, Persona, is_semver, violation

ARTICLE = "Article 7 - Auditability"


def check(persona: Persona, ctx: MirrorContext) -> list:
    name, data = persona.name, persona.data
    if is_semver(data.get("version")):
        return []
    return [violation(
        ARTICLE,
        f"persona '{name}' version {data.get('version')!r} is not semver", "low")]
