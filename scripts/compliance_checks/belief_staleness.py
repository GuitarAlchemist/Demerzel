#!/usr/bin/env python3
"""Check B1: beliefs have been touched within STALE_DAYS.

Unreadable or unparseable belief files are skipped rather than reported — this
check is about staleness, and a corrupt belief is a different concern. All stale
beliefs collapse into a single violation carrying the count.
"""
from __future__ import annotations

import json
from datetime import datetime, timezone

from ._common import CheckOutcome, MirrorContext, violation

ARTICLE = "Article 8 - Observability"
STALE_DAYS = 7


def parse_ts(value):
    if not isinstance(value, str):
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None


def check(ctx: MirrorContext) -> CheckOutcome:
    violations = []
    beliefs = list((ctx.mirror / "state" / "beliefs").glob("*.belief.json"))
    now = datetime.now(timezone.utc)
    stale = 0
    for path in beliefs:
        try:
            ts = parse_ts(json.loads(path.read_text(encoding="utf-8")).get("last_updated", ""))
        except (json.JSONDecodeError, OSError):
            continue
        if ts and (now - ts).days > STALE_DAYS:
            stale += 1
    if stale:
        violations.append(violation(
            ARTICLE,
            f"{stale}/{len(beliefs)} beliefs are stale (> {STALE_DAYS}d since last_updated)",
            "medium"))
    return CheckOutcome(violations=violations, counts={"beliefs": len(beliefs)})
