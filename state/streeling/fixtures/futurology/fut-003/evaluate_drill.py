#!/usr/bin/env python3
"""Evaluate a synthetic adapter substitution drill; this grants no real approval."""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path
from statistics import median


DEFAULT_INPUT = Path(__file__).with_name("adapter-drill.json")


def evaluate(source: dict) -> dict:
    required = set(source["required_checks"])
    if not required or len(required) != len(source["required_checks"]):
        raise ValueError("required checks must be a nonempty unique list")
    groups: dict[str, list[dict]] = defaultdict(list)
    seen: set[tuple[str, str]] = set()
    for run in source["runs"]:
        key = (run["adapter"], run["case"])
        if key in seen:
            raise ValueError(f"duplicate adapter/case: {key}")
        seen.add(key)
        if not isinstance(run["minutes"], (int, float)) or run["minutes"] <= 0:
            raise ValueError(f"invalid duration: {key}")
        if not isinstance(run["corrections"], int) or run["corrections"] < 0:
            raise ValueError(f"invalid corrections: {key}")
        missing = sorted(required - set(run["checks"]))
        reasons = []
        if not (run["source"] == run["output_source"] == run["review_source"]):
            reasons.append("source_identity_mismatch")
        if run["review_verdict"] != "approved":
            reasons.append("review_not_approved")
        if missing:
            reasons.append("missing_checks:" + ",".join(missing))
        groups[run["adapter"]].append({
            "case": run["case"],
            "admissible": not reasons,
            "reasons": reasons,
            "minutes": run["minutes"],
            "corrections": run["corrections"],
        })
    if not groups:
        raise ValueError("at least one run is required")
    expected_cases = {row["case"] for row in groups["current"]}
    if not expected_cases:
        raise ValueError("current adapter is required")
    result = {}
    for adapter, rows in sorted(groups.items()):
        same_cases = {row["case"] for row in rows} == expected_cases
        admitted = same_cases and all(row["admissible"] for row in rows)
        result[adapter] = {
            "comparable_cases": same_cases,
            "all_admissible": admitted,
            "admissible_count": sum(row["admissible"] for row in rows),
            "run_count": len(rows),
            "median_minutes_if_admitted": median(row["minutes"] for row in rows) if admitted else None,
            "corrections_if_admitted": sum(row["corrections"] for row in rows) if admitted else None,
            "runs": rows,
        }
    return {"fixture_status": source["status"], "expected_cases": sorted(expected_cases), "adapters": result}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = evaluate(json.loads(args.input.read_text(encoding="utf-8")))
    output = json.dumps(result, indent=2, ensure_ascii=False) + "\n"
    if args.output:
        args.output.write_text(output, encoding="utf-8")
    else:
        print(output, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
