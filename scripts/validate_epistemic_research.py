#!/usr/bin/env python3
"""Validate Gaia epistemic research proposals without executing their probes."""

from __future__ import annotations

import copy
from datetime import datetime
import hashlib
import json
from pathlib import Path
import sys
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "schemas" / "contracts" / "epistemic-research-proposal.schema.json"
MASS_KEYS = ("T", "P", "U", "D", "F", "C")


def canonical_body(proposal: dict[str, Any]) -> bytes:
    body = copy.deepcopy(proposal)
    body.pop("proposalId", None)
    body.pop("revision", None)
    return json.dumps(
        body,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode("utf-8")


def validate_proposal(proposal: dict[str, Any]) -> list[str]:
    try:
        import jsonschema
    except ImportError:
        return ["DEPENDENCY_MISSING: jsonschema is required for proposal validation"]

    schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
    validator = jsonschema.Draft202012Validator(
        schema,
        format_checker=jsonschema.FormatChecker(),
    )
    issues = sorted(
        (error.json_path, error.message) for error in validator.iter_errors(proposal)
    )
    messages = [f"{path}: {message}" for path, message in issues]
    if messages:
        return messages

    hypothesis_ids = [item["id"] for item in proposal["hypotheses"]]
    if len(set(hypothesis_ids)) != len(hypothesis_ids):
        messages.append("hypothesis ids must be unique")
    uncertainty = proposal["uncertainty"]
    if sum(uncertainty[key] for key in MASS_KEYS) != 1_000_000:
        messages.append("uncertainty T/P/U/D/F/C must sum to exactly 1000000 ppm")

    digest = proposal["revision"]["digest"]
    if proposal["proposalId"] != f"erp-{digest}":
        messages.append("proposalId must equal erp-<revision.digest>")
    expected = hashlib.sha256(canonical_body(proposal)).hexdigest()
    if digest != expected:
        messages.append("revision.digest does not match canonical proposal body")

    created = datetime.fromisoformat(proposal["createdAt"].replace("Z", "+00:00"))
    expires = datetime.fromisoformat(proposal["expiresAt"].replace("Z", "+00:00"))
    if expires <= created:
        messages.append("expiresAt must be later than createdAt")
    return messages


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: validate_epistemic_research.py <proposal.json>", file=sys.stderr)
        return 2
    path = Path(argv[1])
    try:
        proposal = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        print(f"FAIL {path}: {error}")
        return 1
    issues = validate_proposal(proposal)
    if issues:
        print(f"FAIL {path}")
        for issue in issues:
            print(f"  - {issue}")
        return 1
    print(f"OK   {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
