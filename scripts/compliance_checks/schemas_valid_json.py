#!/usr/bin/env python3
"""Check S1: every schemas/*.schema.json parses as JSON."""
from __future__ import annotations

import json

from ._common import CheckOutcome, MirrorContext, violation

ARTICLE = "Article 7 - Auditability"


def check(ctx: MirrorContext) -> CheckOutcome:
    violations = []
    schemas = list((ctx.mirror / "schemas").glob("*.schema.json"))
    for path in schemas:
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            violations.append(violation(
                ARTICLE, f"schema {path.name} is not valid JSON", "critical"))
    return CheckOutcome(violations=violations, counts={"schemas": len(schemas)})
