#!/usr/bin/env python3
"""Compare hari substrate verdicts against Demerzel's hand-maintained beliefs.

belief-currency-policy.yaml declares a monthly "audit belief accuracy" item
and (1.1.0) an ``enforcement.substrate_audit`` that implements it by replaying
``state/beliefs/`` through hari's hexavalent substrate:

    hari scripts/demerzel/beliefs_to_trace.py <Demerzel>  -> trace.json
    hari-core replay trace.json                           -> ResearchReplayReport

This script is the comparison half. Given the replay report (its
``final_beliefs`` map of proposition-slug -> hexavalent verdict) and the belief
files, it checks whether each hand-maintained ``truth_value`` still follows from
the recorded evidence, and surfaces every divergence.

The lint (scripts/belief_lint.py) checks PROCESS compliance — did the holder
re-evaluate when dissent arrived? This checks EPISTEMIC compliance — does the
verdict follow from the evidence once the substrate combines it? The lint
deliberately WARNs (not FAILs) on ``dissent-held`` and defers the authoritative
call here: "substrate replay will flag Contradictory".

## What fails the job

Every divergence is surfaced as a ``::warning``. The job exits nonzero ONLY on
the re-evaluation-trigger class the policy names: a hand-maintained AFFIRMATIVE
verdict (``truth_value`` T or P) where the substrate resolves the same evidence
to ``Contradictory``. Rationale:

  - Contradictory is hari's special absorbing class for irreconcilable evidence;
    it sits OUTSIDE the ordered T<D<U<P truth chain (hari CLAUDE.md). A file that
    still asserts True/Probable while the substrate finds the evidence
    irreconcilable is holding false confidence against unresolved dissent — the
    exact failure the 2026-07-20 replay found (behavioral-test-coverage held
    T@0.8 for four months alongside its own contradicting evidence; hari
    docs/research/2026-07-20-demerzel-belief-replay.md).

Divergences that are NOT this class only warn:

  - Within-chain strength differences (hand P vs substrate True, hand T vs
    substrate Probable) agree on polarity and differ only in degree; the v0
    projection mapping is deliberately crude and produces at least one such
    benign artifact (confidence-calibration: hand P -> substrate True, replay
    doc Section 3). Failing CI on a known mapping artifact would cry wolf.
  - A negative/unknown hand verdict (D/F/U) meeting substrate Contradictory is a
    divergence worth re-evaluating but is not FALSE CONFIDENCE, so it warns.
    Promoting these to FAIL is a later ratchet (cf. the lint's --strict-expiry).

Beliefs the projector skipped for lack of evidence have no substrate opinion and
are reported as info, never as a divergence.
"""

import argparse
import json
import sys
from pathlib import Path

# Hexavalent letter (Demerzel belief files) -> full name (hari final_beliefs).
HEX = {
    "T": "True",
    "P": "Probable",
    "U": "Unknown",
    "D": "Doubtful",
    "F": "False",
    "C": "Contradictory",
}

# Affirmative hand verdicts: the holder is asserting the proposition is
# (probably) true. These meeting a substrate Contradictory is the false-confidence
# re-evaluation trigger the policy names.
AFFIRMATIVE = ("T", "P")


def slug(stem: str) -> str:
    """Proposition slug from a belief filename stem.

    MUST match hari scripts/demerzel/beliefs_to_trace.py::slug exactly, so the
    slugs computed here key into the same final_beliefs the projector produced.
    Drops a leading YYYY-MM-DD- date prefix (date is metadata, not identity).
    """
    parts = stem.split("-")
    if len(parts) > 3 and parts[0].isdigit() and parts[1].isdigit() and parts[2].isdigit():
        stem = "-".join(parts[3:])
    return f"demerzel/{stem}"


def classify(hand_letter, substrate_name):
    """Classify one belief given its hand verdict letter and substrate verdict.

    substrate_name is None when the projector emitted no opinion (no evidence).
    Returns one of: "no-opinion", "agree", "trigger", "divergence".
    """
    if substrate_name is None:
        return "no-opinion"
    hand_name = HEX.get(hand_letter, hand_letter)
    if hand_name == substrate_name:
        return "agree"
    if substrate_name == "Contradictory" and hand_letter in AFFIRMATIVE:
        return "trigger"
    return "divergence"


def audit(beliefs, final_beliefs):
    """Pure core: compare hand verdicts against substrate verdicts.

    beliefs: iterable of (filename, truth_value) pairs. filename is the belief
             file name (e.g. "2026-03-17-behavioral-test-coverage.belief.json").
    final_beliefs: the replay report's {slug: hexavalent-name} map.

    Returns a list of record dicts, sorted by filename, each with keys
    file, slug, hand, substrate (None if no opinion), and status.
    """
    records = []
    for filename, tv in beliefs:
        stem = filename[: -len(".belief.json")] if filename.endswith(".belief.json") else filename
        s = slug(stem)
        substrate = final_beliefs.get(s)
        records.append(
            {
                "file": filename,
                "slug": s,
                "hand": tv,
                "substrate": substrate,
                "status": classify(tv, substrate),
            }
        )
    records.sort(key=lambda r: r["file"])
    return records


def _load_beliefs(beliefs_dir):
    out = []
    # glob (not rglob) deliberately skips archived/ — archived beliefs are
    # expected to be stale and are not re-evaluation targets.
    for f in sorted(Path(beliefs_dir).glob("*.belief.json")):
        try:
            d = json.loads(f.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError) as e:
            print(f"::warning file={f}::could not read belief file: {e}")
            continue
        out.append((f.name, d.get("truth_value")))
    return out


def main(argv=None):
    ap = argparse.ArgumentParser(description="Substrate audit: compare hari verdicts vs hand beliefs.")
    ap.add_argument("--report", required=True, help="hari-core replay ResearchReplayReport JSON (or - for stdin)")
    ap.add_argument("--beliefs-dir", default="state/beliefs")
    args = ap.parse_args(argv)

    report_text = sys.stdin.read() if args.report == "-" else Path(args.report).read_text(encoding="utf-8")
    try:
        report = json.loads(report_text)
    except json.JSONDecodeError as e:
        print(f"::error::replay report is not valid JSON: {e}")
        return 2
    final_beliefs = report.get("final_beliefs")
    if not isinstance(final_beliefs, dict):
        print("::error::replay report has no final_beliefs map — did hari-core replay run?")
        return 2

    beliefs = _load_beliefs(args.beliefs_dir)
    if not beliefs:
        print(f"::error::no belief files found under {args.beliefs_dir}")
        return 2

    records = audit(beliefs, final_beliefs)

    triggers = [r for r in records if r["status"] == "trigger"]
    divergences = [r for r in records if r["status"] == "divergence"]

    for r in triggers + divergences:
        kind = "re-evaluation trigger" if r["status"] == "trigger" else "divergence"
        print(
            f"::warning file={args.beliefs_dir}/{r['file']}::"
            f"substrate audit {kind}: hand-maintained {r['hand']} "
            f"({HEX.get(r['hand'], r['hand'])}) but substrate resolves evidence to "
            f"{r['substrate']} [{r['slug']}]"
        )

    for r in records:
        if r["status"] == "no-opinion":
            print(f"::notice file={args.beliefs_dir}/{r['file']}::no substrate opinion (projector skipped — no evidence) [{r['slug']}]")

    n_agree = sum(1 for r in records if r["status"] == "agree")
    n_noop = sum(1 for r in records if r["status"] == "no-opinion")
    print(
        f"substrate_audit: {len(records)} beliefs — {n_agree} agree, "
        f"{len(divergences)} divergence(WARN), {len(triggers)} re-evaluation-trigger(FAIL), "
        f"{n_noop} no-opinion"
    )

    if triggers:
        names = ", ".join(r["slug"] for r in triggers)
        print(
            f"::error::{len(triggers)} belief(s) hold an affirmative verdict the substrate "
            f"resolves Contradictory — re-evaluate per belief-currency-policy substrate_audit: {names}"
        )
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
