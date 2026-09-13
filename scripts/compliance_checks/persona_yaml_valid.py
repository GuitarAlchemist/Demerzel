#!/usr/bin/env python3
"""Check: every personas/*.persona.yaml has parseable YAML front-matter.

Also the loader for the persona tier — the persona checks all need the parsed
front-matter, and parsing it is exactly what this check does, so it is done once
here and handed on. A persona whose front-matter is malformed still flows through
the remaining persona checks with an empty ``data``, which is what the original
run_checks() did.
"""
from __future__ import annotations

from pathlib import Path

from ._common import Persona, load_front_matter, violation

ARTICLE = "Article 7 - Auditability"


def load_persona(path: Path):
    """Return (Persona, violations) for a single persona file. ``name`` falls
    back to the file stem so an unnamed or unparseable persona is still
    identifiable in the checks that report on it."""
    data, ok, err = load_front_matter(path)
    violations = [] if ok else [violation(
        ARTICLE, f"persona {path.name} is not valid YAML: {err}", "high")]
    return Persona(path=path, data=data, name=data.get("name") or path.stem), violations


def load_personas(mirror: Path):
    """Return (personas, violations) for mirror/personas/*.persona.yaml, in
    sorted file order. Every YAML violation is collected before any other check
    runs, matching the original emission order."""
    personas, violations = [], []
    for path in sorted((mirror / "personas").glob("*.persona.yaml")):
        persona, persona_violations = load_persona(path)
        violations.extend(persona_violations)
        personas.append(persona)
    return tuple(personas), violations
