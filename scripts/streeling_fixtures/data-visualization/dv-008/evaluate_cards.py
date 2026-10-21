"""Summarize the DV-008 synthetic evidence cards; never query live services."""

from __future__ import annotations

import json
from pathlib import Path


FIXTURE = Path(__file__).resolve().parents[4] / "state/streeling/fixtures/data-visualization/dv-008/evidence-cards.json"
FLAGS = ("authored_source", "human_review_approved", "index_source_matches", "module_source_matches", "heading_matches")


def evaluate(path: Path = FIXTURE) -> dict:
    data = json.loads(path.read_text(encoding="utf-8"))
    cards = data["cards"]
    if not cards or len({card["id"] for card in cards}) != len(cards):
        raise ValueError("cards must have unique IDs and cannot be empty")
    for card in cards:
        if any(type(card.get(field)) is not bool for field in FLAGS):
            raise ValueError(f"{card['id']}: evidence flags must be booleans")
        if type(card.get("anonymous_http_status")) is not int or card["anonymous_http_status"] not in (200, 404):
            raise ValueError(f"{card['id']}: expected a 200 or 404 classroom HTTP status")
        if card["human_review_approved"] and not card["authored_source"]:
            raise ValueError(f"{card['id']}: approved review needs authored source")

    rows = []
    for card in cards:
        exact_public = (
            card["anonymous_http_status"] == 200
            and card["index_source_matches"]
            and card["module_source_matches"]
            and card["heading_matches"]
        )
        rows.append({
            "id": card["id"],
            "authored_source": card["authored_source"],
            "human_review_approved": card["human_review_approved"],
            "exact_public_readback": exact_public,
            "all_three_gates": card["authored_source"] and card["human_review_approved"] and exact_public,
        })
    return {
        "scope": data["scope"],
        "source_revision": data["source_revision"],
        "counts": {
            "authored": sum(row["authored_source"] for row in rows),
            "review_approved": sum(row["human_review_approved"] for row in rows),
            "exact_public_readback": sum(row["exact_public_readback"] for row in rows),
            "all_three_gates": sum(row["all_three_gates"] for row in rows),
        },
        "rows": rows,
    }


if __name__ == "__main__":
    print(json.dumps(evaluate(), indent=2))
