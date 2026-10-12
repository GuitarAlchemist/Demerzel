"""Evaluate a synthetic plain-weave composition trial without a renderer."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def evaluate(spec: dict) -> dict:
    warp = spec["base_warp"] * spec["warp_tiles"]
    weft = spec["base_weft"] * spec["weft_tiles"]
    if min(warp, weft) < 2 or spec["diameter_mm"] >= spec["spacing_mm"]:
        raise ValueError("invalid sample dimensions or yarn clearance")

    variants = {}
    for variant in spec["variants"]:
        if variant not in {"global-parity", "restarted-tile-parity"}:
            raise ValueError(f"unsupported variant: {variant}")
        crossings = {}
        for y in range(weft):
            for x in range(warp):
                px, py = (x, y) if variant == "global-parity" else (
                    x % spec["base_warp"], y % spec["base_weft"]
                )
                crossings[f"w{x}-f{y}"] = (px + py + spec["phase"]) % 2 == 0
        violations = []
        for y in range(weft):
            for x in range(warp):
                key = f"w{x}-f{y}"
                if x + 1 < warp and crossings[key] == crossings[f"w{x + 1}-f{y}"]:
                    violations.append([key, f"w{x + 1}-f{y}"])
                if y + 1 < weft and crossings[key] == crossings[f"w{x}-f{y + 1}"]:
                    violations.append([key, f"w{x}-f{y + 1}"])
        variants[variant] = {
            "crossing_count": len(crossings),
            "unique_id_count": len(set(crossings)),
            "adjacency_violations": len(violations),
            "violating_pairs": violations,
            "first_row": ["warp" if crossings[f"w{x}-f0"] else "weft" for x in range(warp)],
        }
    return {
        "sample_id": spec["sample_id"],
        "warp_count": warp,
        "weft_count": weft,
        "spacing_to_diameter_ratio": spec["spacing_mm"] / spec["diameter_mm"],
        "variants": variants,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, default=Path(__file__).with_name("weave-trial.json"))
    args = parser.parse_args()
    print(json.dumps(evaluate(json.loads(args.input.read_text(encoding="utf-8"))), indent=2))
