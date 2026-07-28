#!/usr/bin/env python3
"""Emit per-artifact governance-health deltas as JSONL (the `do` phase of
skills/demerzel-quality-trend). Deterministic, zero-judgment, append-only.

Reads state/evolution/*.evolution.json, compares each artifact's current
metrics against its previous emitted line, and appends one line per artifact
to state/quality-trend/<YYYY-MM>.jsonl.

NOTE ON SCHEMA: the skill's example line stores only delta_* fields. A delta
cannot be recomputed from a stored delta, so each line here also carries the
absolute counts (citation_count / violation_count / compliance_rate) that the
next run reads back as its baseline. The schema stays flat and greppable.

Constraints (from the skill): read-only w.r.t. evolution/ and beliefs/;
append-only w.r.t. its own JSONL; makes no proposals; targets < 5s.
"""
from __future__ import annotations

import argparse
import glob
import json
import os
from datetime import datetime, timezone


def _iso_to_dt(value: str | None) -> datetime | None:
    if not value:
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None


def _load_previous(out_dir: str) -> dict[str, dict]:
    """Last emitted line per artifact, across all monthly files (chronological)."""
    previous: dict[str, dict] = {}
    for path in sorted(glob.glob(os.path.join(out_dir, "*.jsonl"))):
        with open(path, encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if not line:
                    continue
                try:
                    row = json.loads(line)
                except json.JSONDecodeError:
                    continue
                artifact = row.get("artifact")
                if artifact:
                    previous[artifact] = row
    return previous


def build_rows(evolution_dir: str, out_dir: str,
               now: datetime) -> tuple[list[dict], list[str]]:
    """Return (rows, skips). Each record is parsed in isolation: a record that
    raises is counted as a skip (its filename recorded) and the run continues,
    so one malformed record can never take down the whole feeder."""
    previous = _load_previous(out_dir)
    rows: list[dict] = []
    skips: list[str] = []
    for path in sorted(glob.glob(os.path.join(evolution_dir, "*.evolution.json"))):
        try:
            with open(path, encoding="utf-8") as fh:
                data = json.load(fh)
            artifact = data.get("artifact")
            if not artifact:
                continue
            metrics = data.get("metrics", {})
            citation = int(metrics.get("citation_count", 0) or 0)
            violation = int(metrics.get("violation_count", 0) or 0)
            compliance = float(metrics.get("compliance_rate", 0.0) or 0.0)
            # effectiveness may be a dict (canonical) or a free-text string
            # (legacy shape); only a dict carries a truth_value.
            effectiveness = data.get("assessment", {}).get("effectiveness")
            eff_to = (effectiveness.get("truth_value")
                      if isinstance(effectiveness, dict) else None)

            # age since last_cited, falling back to created_at
            anchor = _iso_to_dt(metrics.get("last_cited")) or _iso_to_dt(
                data.get("created_at"))
            age_days = (now - anchor).days if anchor else None

            prev = previous.get(artifact, {})
            rows.append({
                "timestamp": now.strftime("%Y-%m-%dT%H:%M:%SZ"),
                "artifact": artifact,
                "citation_count": citation,
                "violation_count": violation,
                "compliance_rate": round(compliance, 4),
                "delta_citations": citation - int(prev.get("citation_count", 0) or 0),
                "delta_violations": violation - int(prev.get("violation_count", 0) or 0),
                "delta_compliance": round(
                    compliance - float(prev.get("compliance_rate", 0.0) or 0.0), 4),
                "age_days": age_days,
                "effectiveness_from": prev.get("effectiveness_to"),
                "effectiveness_to": eff_to,
            })
        except Exception as exc:  # noqa: BLE001 — isolate, don't crash the feeder
            skips.append(f"{os.path.basename(path)}: {type(exc).__name__}: {exc}")
    return rows, skips


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--evolution-dir", default="state/evolution")
    ap.add_argument("--out-dir", default="state/quality-trend")
    ap.add_argument("--now", default=None,
                    help="ISO8601 override for the run timestamp (testing)")
    ap.add_argument("--dry-run", action="store_true",
                    help="print rows to stdout, do not append")
    args = ap.parse_args()

    now = _iso_to_dt(args.now) or datetime.now(timezone.utc)
    rows, skips = build_rows(args.evolution_dir, args.out_dir, now)

    if args.dry_run:
        for row in rows:
            print(json.dumps(row))
        _report_skips(skips)
        return 0

    os.makedirs(args.out_dir, exist_ok=True)
    out_path = os.path.join(args.out_dir, f"{now:%Y-%m}.jsonl")
    with open(out_path, "a", encoding="utf-8") as fh:
        for row in rows:
            fh.write(json.dumps(row) + "\n")
    print(f"quality-trend: appended {len(rows)} rows to {out_path}")
    _report_skips(skips)
    return 0


def _report_skips(skips: list[str]) -> None:
    """Report skipped records as data, not silence: a row count that drops
    without explanation is indistinguishable from a quiet loop."""
    if not skips:
        return
    print(f"quality-trend: skipped {len(skips)} malformed record(s):")
    for skip in skips:
        print(f"  - {skip}")


if __name__ == "__main__":
    raise SystemExit(main())
