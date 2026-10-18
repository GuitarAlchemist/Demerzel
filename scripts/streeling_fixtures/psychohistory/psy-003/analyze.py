#!/usr/bin/env python3
"""PSY-003 analysis: a review queue and a publication queue through four synthetic weeks.

Synthetic: reads scenarios.json only, never the repository, and writes results.json.

Each week the new review-ready items join the review queue; review accepts at most its capacity; accepted items join
the publication queue; publication takes at most its capacity. Every quantity is a whole number and the only
operations are +, - and min, so results.json is the same bytes on every platform.

Run from the repository root:
    python -I -B scripts/streeling_fixtures/psychohistory/psy-003/analyze.py
    python -I -B scripts/streeling_fixtures/psychohistory/psy-003/analyze.py --check
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

# This program lives under scripts/ (CONTRIBUTING.md: no executable code outside scripts/); its data stays
# under state/streeling/fixtures/. FIXTURE_FILE is the path the program would have next to that data.
FIXTURE_FILE = (Path(__file__).resolve().parents[4]
                / "state/streeling/fixtures/psychohistory/psy-003" / Path(__file__).name)

HERE = FIXTURE_FILE.parent
CHECKS: dict[str, int] = {}  # self-check -> times evaluated


def check(name: str, condition: bool, detail: str = "") -> None:
    """Record a passed self-check, or abort the run."""
    if not condition:
        raise AssertionError(f"self-check failed: {name}" + (f" ({detail})" if detail else ""))
    CHECKS[name] = CHECKS.get(name, 0) + 1


def simulate(scenario: dict) -> dict:
    arrivals = scenario["new_review_ready_per_week"]
    review_caps = scenario["accepted_review_capacity_per_week"]
    publish_caps = scenario["publication_capacity_per_week"]
    if not arrivals or len({len(arrivals), len(review_caps), len(publish_caps)}) != 1:
        raise ValueError("weekly arrays must have the same nonzero length")
    values = [scenario["initial_review_queue"], scenario["initial_publication_queue"],
              *arrivals, *review_caps, *publish_caps]
    if any(not isinstance(value, int) or isinstance(value, bool) or value < 0 for value in values):
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


def identities_hold(scenario: dict, weeks: list[dict]) -> bool:
    """Week by week: initial review queue + new ready = accepted + waiting review, and initial publication queue +
    accepted = published + waiting publication. An item can only leave a queue by moving to the next stage."""
    arrived = 0
    for week in weeks:
        arrived += week["new_review_ready"]
        if scenario["initial_review_queue"] + arrived != week["accepted_total"] + week["waiting_review"]:
            return False
        if (scenario["initial_publication_queue"] + week["accepted_total"]
                != week["published_total"] + week["waiting_publication"]):
            return False
    return True


def self_check(name: str, scenario: dict, result: dict) -> None:
    weeks = result["weeks"]
    check("both conservation identities hold every week", identities_hold(scenario, weeks), name)
    caps = zip(weeks, scenario["accepted_review_capacity_per_week"], scenario["publication_capacity_per_week"])
    for week, review_cap, publish_cap in caps:
        check("no stage takes more than its capacity",
              week["accepted"] <= review_cap and week["published"] <= publish_cap, f"{name} week {week['week']}")
        # A stage leaves capacity idle only when nothing is waiting for it.
        check("a stage under capacity leaves its queue empty",
              (week["accepted"] == review_cap or week["waiting_review"] == 0)
              and (week["published"] == publish_cap or week["waiting_publication"] == 0),
              f"{name} week {week['week']}")


def hand_computed(expected: dict, results: dict) -> None:
    for name, figures in expected.items():
        weeks = results[name]["weeks"]
        final = results[name]["final"]
        for key, values in figures.items():
            if key.endswith("_by_week"):
                found = [week[key[: -len("_by_week")]] for week in weeks]
            else:
                found = final[key]
            check("the hand-computed figures are found", found == values, f"{name} {key}: {found} != {values}")


def negative_control(control: dict, scenarios: dict, results: dict) -> dict:
    """Lose items between the two queues in one week: the identities must notice."""
    name, week_no, lost = control["scenario"], control["week"], control["items_lost"]
    weeks = json.loads(json.dumps(results[name]["weeks"]))
    for week in weeks[week_no - 1:]:
        week["waiting_publication"] -= lost
    detected = not identities_hold(scenarios[name], weeks)
    check("negative control: items lost between the queues break an identity", detected,
          f"{lost} item(s) lost in week {week_no} of {name}")
    return {"scenario": name, "week": week_no, "items_lost": lost, "identities_hold": not detected}


def analyze(source: dict) -> dict:
    scenarios = source["scenarios"]
    results = {name: simulate(scenario) for name, scenario in scenarios.items()}
    for name, scenario in scenarios.items():
        self_check(name, scenario, results[name])
    hand_computed(source["hand_computed"], results)
    control = negative_control(source["negative_control"], scenarios, results)
    return {
        "observed_snapshot_commit": source["observed_snapshot_commit"],
        "simulation_limits": source["simulation_limits"],
        "scenarios": results,
        "negative_control": control,
        "checks": [{"check": name, "times_evaluated": times, "passed": True} for name, times in CHECKS.items()],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--scenarios", type=Path, default=HERE / "scenarios.json")
    parser.add_argument("--output", type=Path, default=HERE / "results.json")
    parser.add_argument("--check", action="store_true",
                        help="recompute and compare with the output file instead of writing it")
    args = parser.parse_args()
    CHECKS.clear()
    try:
        result = analyze(json.loads(args.scenarios.read_text(encoding="utf-8")))
    except (AssertionError, KeyError, TypeError, ValueError, OSError) as exc:
        print(f"analyze.py: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 1
    payload = (json.dumps(result, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    if args.check:
        try:
            saved = args.output.read_bytes()
        except OSError as exc:
            print(f"analyze.py: cannot read {args.output}: {exc}", file=sys.stderr)
            return 1
        same = saved.replace(b"\r\n", b"\n") == payload
        print(f"analyze.py: {args.output.name} {'matches' if same else 'DIFFERS FROM'} a fresh run "
              f"({len(CHECKS)} self-checks passed)")
        return 0 if same else 1
    args.output.write_bytes(payload)
    print(f"analyze.py: {len(CHECKS)} self-checks passed -> {args.output.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
