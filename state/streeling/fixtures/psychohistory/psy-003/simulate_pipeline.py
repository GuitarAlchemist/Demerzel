#!/usr/bin/env python3
"""Run a bounded synthetic draft-review-publication queue exercise."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


DEFAULT_INPUT = Path(__file__).with_name("pipeline-scenarios.json")


def simulate(scenario: dict) -> dict:
    arrivals = scenario["new_review_ready_per_week"]
    review_caps = scenario["accepted_review_capacity_per_week"]
    publish_caps = scenario["publication_capacity_per_week"]
    if not arrivals or len({len(arrivals), len(review_caps), len(publish_caps)}) != 1:
        raise ValueError("weekly arrays must have the same nonzero length")
    values = [scenario["initial_review_queue"], scenario["initial_publication_queue"],
              *arrivals, *review_caps, *publish_caps]
    if any(not isinstance(value, int) or value < 0 for value in values):
        raise ValueError("queues, arrivals, and capacities must be nonnegative integers")

    review_queue = scenario["initial_review_queue"]
    publication_queue = scenario["initial_publication_queue"]
    accepted_total = 0
    published_total = 0
    weeks = []
    for index, (new_ready, review_cap, publish_cap) in enumerate(zip(arrivals, review_caps, publish_caps), 1):
        review_queue += new_ready
        accepted = min(review_queue, review_cap)
        review_queue -= accepted
        accepted_total += accepted
        publication_queue += accepted
        published = min(publication_queue, publish_cap)
        publication_queue -= published
        published_total += published
        weeks.append({
            "week": index,
            "new_review_ready": new_ready,
            "accepted": accepted,
            "published": published,
            "waiting_review": review_queue,
            "waiting_publication": publication_queue,
            "accepted_total": accepted_total,
            "published_total": published_total,
        })
    return {"weeks": weeks, "final": weeks[-1]}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output", type=Path, help="write deterministic JSON results")
    args = parser.parse_args()
    source = json.loads(args.input.read_text(encoding="utf-8"))
    result = {
        "observed_snapshot_commit": source["observed_snapshot_commit"],
        "simulation_limits": source["simulation_limits"],
        "scenarios": {name: simulate(scenario) for name, scenario in source["scenarios"].items()},
    }
    output = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.write_text(output, encoding="utf-8")
    else:
        print(output, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
