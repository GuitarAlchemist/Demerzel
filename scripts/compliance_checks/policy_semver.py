#!/usr/bin/env python3
"""Check P3 (policy tier): a policy that declares a version declares N.N.N.

Policies here are frequently prose-rich human docs (illustrative quotes,
markdown). The framework's own audit does NOT require all policies to be strict
YAML, so a parse failure is not a governance violation — those files are skipped.
"""
from __future__ import annotations

from ._common import CheckOutcome, MirrorContext, is_semver, load_front_matter, violation

ARTICLE = "Article 7 - Auditability"


def check(ctx: MirrorContext) -> CheckOutcome:
    violations = []
    policies = list((ctx.mirror / "policies").glob("*.yaml"))
    for path in policies:
        data, ok, _err = load_front_matter(path)
        if not ok:
            continue
        if "version" in data and not is_semver(data.get("version")):
            violations.append(violation(
                ARTICLE,
                f"policy {path.name} version {data.get('version')!r} is not semver",
                "low"))
    return CheckOutcome(violations=violations, counts={"policies": len(policies)})
