"""Evaluate bounded teaching cards; this does not inspect GitHub releases."""

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
FIELDS = ("implementation", "runtime", "meaning", "human_review")


def evaluate(card: dict, required_targets: list[str]) -> dict:
    if set(card["targets"]) != set(required_targets):
        raise ValueError("card must cover every required target exactly once")
    gaps = []
    for target in required_targets:
        values = card["targets"][target]
        if set(values) != set(FIELDS) or any(type(values[field]) is not bool for field in FIELDS):
            raise ValueError(f"invalid evidence fields for {target}")
        gaps.extend(f"{target}.{field}" for field in FIELDS if not values[field])
    for field in ("contract_replay", "artifact_hashes", "published_tag"):
        if type(card[field]) is not bool:
            raise ValueError(f"invalid {field}")
    gaps.extend(field for field in ("contract_replay", "artifact_hashes") if not card[field])
    if not card["targets"]["godot"]["meaning"] and card["targets"]["godot"]["runtime"]:
        decision = "reject_candidate"
    elif gaps:
        decision = "hold_for_evidence"
    else:
        decision = "release_candidate"
    return {
        "id": card["id"],
        "kind": card["kind"],
        "decision": decision,
        "missing": gaps,
        "published": card["published_tag"],
    }


def main() -> None:
    fixture = json.loads((ROOT / "release-cards.json").read_text(encoding="utf-8"))
    assert fixture["schema"] == "streeling.release-cards/0.1"
    assert fixture["required_targets"] == ["comfyui", "blender", "godot"]
    print(json.dumps([evaluate(card, fixture["required_targets"]) for card in fixture["cards"]], indent=2))


if __name__ == "__main__":
    main()
