#!/usr/bin/env python3
"""Compare explicit pitch-class equivalences in a small teaching fixture."""

from __future__ import annotations

import argparse
import json
from itertools import combinations
from math import sqrt
from pathlib import Path


DEFAULT_INPUT = Path(__file__).with_name("voicing-cases.json")


def pcs(notes: list[int]) -> tuple[int, ...]:
    if not notes or any(not isinstance(n, int) or not 0 <= n <= 127 for n in notes):
        raise ValueError("each case needs MIDI notes in [0, 127]")
    return tuple(sorted({note % 12 for note in notes}))


def icv(pitch_classes: tuple[int, ...]) -> list[int]:
    counts = [0] * 6
    for a, b in combinations(pitch_classes, 2):
        distance = (b - a) % 12
        counts[min(distance, 12 - distance) - 1] += 1
    return counts


def chroma_cosine(left: tuple[int, ...], right: tuple[int, ...]) -> float:
    return len(set(left) & set(right)) / sqrt(len(left) * len(right))


def is_transposition(left: tuple[int, ...], right: tuple[int, ...]) -> bool:
    return any({(pc + offset) % 12 for pc in left} == set(right) for offset in range(12))


def is_inversion_or_transposition(left: tuple[int, ...], right: tuple[int, ...]) -> bool:
    return is_transposition(left, right) or any(
        {(-pc + offset) % 12 for pc in left} == set(right) for offset in range(12)
    )


def evaluate(source: dict) -> dict:
    cases = source["cases"]
    by_id = {case["id"]: case for case in cases}
    if len(by_id) != len(cases):
        raise ValueError("case ids must be unique")
    for case in cases:
        if not isinstance(case["declared_root_pc"], int) or not 0 <= case["declared_root_pc"] < 12:
            raise ValueError("declared root pitch class must be in [0, 11]")
    rows = []
    for left_id, right_id in source["comparisons"]:
        left, right = by_id[left_id], by_id[right_id]
        left_pcs, right_pcs = pcs(left["midi"]), pcs(right["midi"])
        left_icv, right_icv = icv(left_pcs), icv(right_pcs)
        rows.append({
            "pair": [left_id, right_id],
            "same_midi_note_multiset": sorted(left["midi"]) == sorted(right["midi"]),
            "left_pitch_classes": list(left_pcs),
            "right_pitch_classes": list(right_pcs),
            "same_pitch_class_set": left_pcs == right_pcs,
            "same_declared_root_pc": left["declared_root_pc"] == right["declared_root_pc"],
            "left_icv": left_icv,
            "right_icv": right_icv,
            "same_icv": left_icv == right_icv,
            "related_by_transposition": is_transposition(left_pcs, right_pcs),
            "related_by_transposition_or_inversion": is_inversion_or_transposition(left_pcs, right_pcs),
            "toy_binary_chroma_cosine": round(chroma_cosine(left_pcs, right_pcs), 6),
        })
    return {"scope": source["scope"], "comparisons": rows}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = evaluate(json.loads(args.input.read_text(encoding="utf-8")))
    output = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.write_text(output, encoding="utf-8")
    else:
        print(output, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
