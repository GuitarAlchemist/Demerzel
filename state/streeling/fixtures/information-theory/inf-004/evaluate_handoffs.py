"""Evaluate synthetic handoff cases; never infer a live agent's state."""

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
FIELDS = ("tests_passed", "single_writer", "review_approved")


def evaluate(data: dict) -> dict:
    cases = data["cases"]
    if not cases or len({case["id"] for case in cases}) != len(cases):
        raise ValueError("cases must have distinct IDs")
    costs = data["costs"]
    if set(costs) != {"false_accept", "false_reject"} or any(
        type(value) is not int or value < 0 for value in costs.values()
    ):
        raise ValueError("costs must be nonnegative integers")
    for case in cases:
        if set(case) != {"id", "headline", *FIELDS}:
            raise ValueError("each case needs the same evidence fields")
        if any(type(case[field]) is not bool for field in FIELDS):
            raise ValueError("evidence fields must be booleans")
    if len({case["headline"] for case in cases}) != 1:
        raise ValueError("the lossy headline experiment requires one collision group")

    eligible = [case["id"] for case in cases if all(case[field] for field in FIELDS)]
    ineligible = [case["id"] for case in cases if case["id"] not in eligible]
    accept_all = len(ineligible) * costs["false_accept"] / len(cases)
    reject_all = len(eligible) * costs["false_reject"] / len(cases)
    return {
        "count": len(cases),
        "headline": cases[0]["headline"],
        "eligible": eligible,
        "ineligible": ineligible,
        "accept_all_mean_cost": accept_all,
        "reject_all_mean_cost": reject_all,
        "full_evidence_mean_cost": 0,
    }


def main() -> None:
    data = json.loads((ROOT / "handoff-cases.json").read_text(encoding="utf-8"))
    if data["schema"] != "streeling.handoff-decision-cases/0.1":
        raise ValueError("unexpected fixture schema")
    print(json.dumps(evaluate(data), indent=2))


if __name__ == "__main__":
    main()
