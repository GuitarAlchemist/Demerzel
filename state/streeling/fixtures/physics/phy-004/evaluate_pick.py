#!/usr/bin/env python3
"""Deterministic arithmetic for PHY-004; not a GA audio render."""

from __future__ import annotations

import json
import math
from pathlib import Path


def clamp(value: float, lower: float, upper: float) -> float:
    return min(upper, max(lower, value))


def pick_parameters(sample_rate: float, frequency: float, velocity: float) -> dict:
    """Mirror the selected GA excite formulas for positive, in-range inputs."""
    rate = max(sample_rate, 1.0)
    f = max(frequency, 20.0)
    vel = clamp(velocity, 0.0, 1.0)
    length = max(2, math.floor(rate / f))
    exact_length = rate / f
    fractional_delay = clamp(exact_length - length, 0.0, 0.999)
    pick_ratio = min(clamp(0.18 + 0.60 * (1.0 - vel), 0.1, 0.85), 0.95)
    # Rust's round() chooses away from zero on half values; all inputs here are positive.
    pick_offset = max(1, min(length - 1, math.floor(length * pick_ratio + 0.5)))
    pluck_mix = clamp(0.15 + 0.35 * vel, 0.05, 0.7)
    return {
        "velocity": vel,
        "buffer_len": length,
        "fractional_delay": fractional_delay,
        "pick_ratio": pick_ratio,
        "pick_offset": pick_offset,
        "pick_position": pick_offset / length,
        "pluck_mix": pluck_mix,
    }


def shape_at(index: int, length: int, pick_offset: int) -> float:
    """GA's pre-noise envelope at one active delay-buffer index."""
    position = index / length
    pick_position = pick_offset / length
    return clamp(1.0 - abs(position - pick_position) * 2.5, 0.0, 1.0)


def main() -> None:
    spec = json.loads(Path(__file__).with_name("velocity-pick-cases.json").read_text(encoding="utf-8"))
    rows = []
    for case in spec["cases"]:
        row = pick_parameters(spec["sample_rate_hz"], spec["note_hz"], case["velocity"])
        assert row["buffer_len"] == case["expected_buffer_len"]
        assert row["pick_offset"] == case["expected_pick_offset"]
        assert math.isclose(row["pluck_mix"], case["expected_pluck_mix"], abs_tol=1e-12)
        assert shape_at(row["pick_offset"], row["buffer_len"], row["pick_offset"]) == 1.0
        assert 0 <= row["fractional_delay"] < 1
        rows.append(row)
    assert len({row["pick_offset"] for row in rows}) == len(rows), "velocity-only-gain model unexpectedly matched"
    assert rows[0]["pick_offset"] > rows[1]["pick_offset"] > rows[2]["pick_offset"]
    assert rows[0]["pluck_mix"] < rows[1]["pluck_mix"] < rows[2]["pluck_mix"]
    print(json.dumps({"scope": "selected source-formula simulation; no WAV or listening evidence", "cases": rows}, indent=2))


if __name__ == "__main__":
    main()
