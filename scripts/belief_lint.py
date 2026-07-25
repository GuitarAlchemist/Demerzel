#!/usr/bin/env python3
"""Mechanical enforcement of belief-currency-policy.yaml over state/beliefs/.

The policy has asserted since 2026-03-17 that "stale beliefs are worse
than no beliefs" and that stale beliefs require mandatory re-evaluation —
with no mechanism attached. On 2026-07-20 a machine replay of these files
through hari's substrate (GuitarAlchemist/hari `scripts/demerzel/
beliefs_to_trace.py`, docs/research/2026-07-20-demerzel-belief-replay.md)
found a belief that had held True @ 0.8 for four months while carrying
its own contradicting evidence. This lint is the tripwire that makes the
policy's existing rules self-enforcing (loop-doctrine: the writer IS the
CI check; see hari docs/research/2026-07-20-compounding-strategy.md).

Checks (per belief file `state/beliefs/*.belief.json`, `archived/` skipped):

  FAIL  unaddressed-contradiction : truth_value T/P while a contradicting
        evidence item is newer than last_updated — the holder has not
        re-evaluated since the dissent arrived.
  FAIL  assertion-without-evidence: truth_value other than U with zero
        evidence items.
  WARN  overconfident-with-dissent: confidence >= 0.85 alongside ANY
        contradicting evidence (acknowledged dissent should cost
        confidence; cf. overconfidence_rate in confidence-calibration).
  WARN  expired                  : last_updated older than the policy's
        14-day expiry while truth_value is not U. (--strict-expiry
        promotes to FAIL — the policy's own rule, ratcheted in later so
        first wiring is not disruptive.)

Exit nonzero on any FAIL. Deeper (substrate-grade) checking — temporal
ordering, hexavalent combine semantics — is the hari replay above; run
it as the policy's monthly "audit belief accuracy" job.
"""

import argparse
import json
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

EXPIRY_DAYS = 14  # belief-currency-policy staleness_rules.thresholds.expired


def parse_ts(s):
    if not s:
        return None
    try:
        return datetime.fromisoformat(str(s).replace("Z", "+00:00"))
    except ValueError:
        return None


def lint_file(path, now, strict_expiry):
    fails, warns = [], []
    d = json.loads(path.read_text(encoding="utf-8"))
    tv = d.get("truth_value")
    conf = d.get("confidence")
    last = parse_ts(d.get("last_updated"))
    ev = d.get("evidence") or {}
    supporting = ev.get("supporting") or []
    contradicting = ev.get("contradicting") or []

    if tv and tv != "U" and not supporting and not contradicting:
        fails.append(f"assertion-without-evidence: {tv}@{conf} with empty evidence")

    if tv in ("T", "P") and contradicting:
        newest_dissent = max(
            (parse_ts(e.get("timestamp")) for e in contradicting), key=lambda t: t or datetime.min.replace(tzinfo=timezone.utc)
        )
        if newest_dissent and (last is None or newest_dissent > last):
            fails.append(
                f"unaddressed-contradiction: {tv}@{conf} but contradicting evidence "
                f"({newest_dissent.date()}) is newer than last_updated "
                f"({last.date() if last else 'absent'}) — re-evaluate"
            )
        if isinstance(conf, (int, float)) and conf >= 0.85:
            warns.append(f"overconfident-with-dissent: {conf} with {len(contradicting)} contradicting item(s)")
        else:
            # Acknowledged-but-unresolved dissent: last_updated shows the
            # holder looked, yet the verdict still conflicts with standing
            # contradicting evidence. Process-compliant; epistemically the
            # hexavalent substrate replay resolves this Contradictory
            # (hari docs/research/2026-07-20-demerzel-belief-replay.md).
            # WARN here; the substrate replay is the authoritative check.
            warns.append(
                f"dissent-held: {tv}@{conf} with {len(contradicting)} standing "
                f"contradicting item(s) — substrate replay will flag Contradictory"
            )

    if tv and tv != "U" and last and (now - last) > timedelta(days=EXPIRY_DAYS):
        msg = f"expired: {tv}@{conf} last_updated {last.date()} ({(now - last).days}d ago; policy expiry {EXPIRY_DAYS}d)"
        (fails if strict_expiry else warns).append(msg)

    return fails, warns


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--beliefs-dir", default="state/beliefs")
    ap.add_argument("--strict-expiry", action="store_true")
    args = ap.parse_args()

    now = datetime.now(timezone.utc)
    beliefs = sorted(Path(args.beliefs_dir).glob("*.belief.json"))
    if not beliefs:
        print(f"::error::no belief files found under {args.beliefs_dir}")
        return 2

    n_fail = n_warn = 0
    for f in beliefs:
        fails, warns = lint_file(f, now, args.strict_expiry)
        for m in fails:
            print(f"::error file={f}::{m}")
            n_fail += 1
        for m in warns:
            print(f"::warning file={f}::{m}")
            n_warn += 1

    print(f"belief_lint: {len(beliefs)} beliefs, {n_fail} FAIL, {n_warn} WARN")
    return 1 if n_fail else 0


if __name__ == "__main__":
    raise SystemExit(main())
