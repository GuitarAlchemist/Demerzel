#!/usr/bin/env python3
"""Primitives shared by the individual compliance checks.

This module holds no check of its own — only the violation constructor, the
front-matter reader, the semver predicate, and the small value types each check
receives. Every check lives in its own module next to this one.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

import yaml  # pyyaml


def violation(article: str, description: str, severity: str) -> dict:
    """Build one violations[] entry. The shape is part of the report schema
    (schemas/contracts/compliance-report.schema.json) — do not change it."""
    return {"article": article, "description": description,
            "severity": severity, "remediation_status": "pending"}


def load_front_matter(path: Path):
    """Parse the YAML front-matter only. Many governance files here are YAML+markdown
    hybrids: a metadata block, then a standalone '---', then markdown prose (headings,
    backticks, sentences) interleaved with illustrative YAML. Those bodies are NOT
    meant to be machine-parsed, so we read only the front-matter (content before the
    first standalone '---' line; whole file if there is none). Returns (dict, ok, err);
    ok=False only when the front-matter itself is malformed (a real violation)."""
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    cut = next((i for i, ln in enumerate(lines) if i > 0 and ln.strip() == "---"), None)
    front = "\n".join(lines[:cut]) if cut is not None else text
    try:
        data = yaml.safe_load(front)
        return (data if isinstance(data, dict) else {}), True, None
    except yaml.YAMLError as exc:
        return {}, False, str(exc).splitlines()[0]


def is_semver(v) -> bool:
    if not isinstance(v, str):
        return False
    parts = v.strip().strip('"').split(".")
    return len(parts) == 3 and all(p.isdigit() for p in parts)


@dataclass(frozen=True)
class Persona:
    """One persona file plus the front-matter parsed out of it. ``name`` is the
    declared name, falling back to the file stem when there is none."""
    path: Path
    data: dict
    name: str


@dataclass(frozen=True)
class MirrorContext:
    """Everything the checks read that is cheaper to gather once than per check:
    the mirror root, the loaded personas in file order, the set of *declared*
    persona names (which deliberately includes None for unnamed personas, so an
    estimator_pairing can never resolve against a missing name), and the joined
    behavioral-test stems that P2 substring-matches against."""
    mirror: Path
    personas: tuple = ()
    persona_names: frozenset = frozenset()
    test_blob: str = ""


@dataclass(frozen=True)
class CheckOutcome:
    """What a mirror-level check returns: its violations, plus the artifact
    counts it is the authority for (they land in the report's `checked` block)."""
    violations: list = field(default_factory=list)
    counts: dict = field(default_factory=dict)
