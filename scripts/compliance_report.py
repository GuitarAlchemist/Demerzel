#!/usr/bin/env python3
"""
Demerzel compliance_report — emits a REAL Galactic-Protocol compliance report for
a consumer repo (ix | tars | ga) by running governance checks against that repo's
governance/demerzel/ mirror.

This fills the declared-but-unfulfilled compliance-report seam (galactic-protocol
.md §17/§42, schemas/contracts/compliance-report.schema.json): the contract and
templates describe consumer->Demerzel compliance reporting, but nothing emits
instances (0 on disk). Without that corpus, the §3c violation_pattern_detector
has nothing to cluster. This is the harvest source.

Placement choice (slice 1): a single parameterized runner here in Demerzel/
scripts, reading the consumer mirrors Demerzel already has on disk — the
pragmatic single-home option. If we later want strict "consumer self-reports"
fidelity, the same checks move into each consumer repo.

Checks (real, mechanical — the runnable subset of governance-audit.ixql L1-L2):
  P1 persona field conformance   (persona-requirements.md: required keys present)
  P2 behavioral-test coverage    (every persona has a tests/behavioral/*.md)
  P3 semver validity             (persona/policy version is N.N.N)
  P4 estimator_pairing resolves  (points at an existing persona)
  S1 schema files are valid JSON
  B1 belief staleness            (last_updated older than 7 days)

Each check lives in its own module under scripts/compliance_checks/, which also
owns run_checks() and the order the checks run in. This file keeps the report:
severity rollup, schema shape, integrity fields, atomic write, CLI.

Each failure becomes a violations[] entry mapped to a constitutional article /
contributing rule, with a severity. overall_status is derived from the worst
severity present. The report carries integrity fields with origin_repo = the
consumer (the report is *about*/from that repo).

Usage:
  python scripts/compliance_report.py --repo ix
  python scripts/compliance_report.py --repo tars --repos-root /path/to/repos
  python scripts/compliance_report.py --repo ix --dry-run

Exit codes:
  0  report emitted (consumer compliant OR with violations — both are valid reports)
  1  usage / IO error (e.g. consumer mirror not found)
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import uuid
from datetime import datetime, timedelta, timezone
from pathlib import Path

# The checks parse governance YAML; importing pyyaml here too keeps the CLI's
# fail-fast message, which reads better than an ImportError traceback.
try:
    import yaml  # noqa: F401
except ImportError:  # pragma: no cover
    print("error: pyyaml required (pip install pyyaml)", file=sys.stderr)
    raise SystemExit(1)

try:  # package mode: `import scripts.compliance_report`
    from .compliance_checks import run_checks
except ImportError:  # direct script: `python scripts/compliance_report.py`
    from compliance_checks import run_checks


def _now() -> datetime:
    return datetime.now(timezone.utc)


def _now_iso() -> str:
    return _now().strftime("%Y-%m-%dT%H:%M:%SZ")


def build_report(repo: str, result: dict, period_days: int) -> dict:
    violations = result["violations"]
    sev = {v["severity"] for v in violations}
    if {"critical", "high"} & sev:
        overall = "non-compliant"
    elif violations:
        overall = "partial"
    else:
        overall = "compliant"

    def _status(hit):  # compliant unless a violation touched this area
        return "violation" if hit else "compliant"

    arts = {v["article"] for v in violations}
    payload = {
        "id": f"cr-{repo}-{_now_iso()[:10].replace('-', '')}",
        "repo": repo,
        "agent": "compliance-reporter",
        "reporting_period": {
            "from": (_now() - timedelta(days=period_days)).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "to": _now_iso(),
        },
        "constitutional_compliance": [
            {"article": "Article 7 - Auditability", "status": _status("Article 7 - Auditability" in arts)},
            {"article": "Article 8 - Observability", "status": _status("Article 8 - Observability" in arts)},
        ],
        "policy_compliance": [
            {"policy": "persona-requirements", "status": _status("persona-requirements" in arts)},
            {"policy": "contributing-rules", "status": _status("contributing-rules" in arts)},
        ],
        "violations": violations,
        "overall_status": overall,
        "reported_at": _now_iso(),
        "channel": "crisp",
    }
    return payload


def _attach_integrity(payload: dict, repo: str) -> dict:
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    doc = dict(payload)
    doc.update({
        "message_id": str(uuid.uuid4()),
        "origin_repo": repo,
        "origin_agent": "compliance-reporter",
        "content_hash": hashlib.sha256(canonical).hexdigest(),
        "hash_algorithm": "sha256",
        "timestamp": payload["reported_at"],
    })
    return doc


def _atomic_write(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    with tmp.open("w", encoding="utf-8") as fh:
        json.dump(data, fh, indent=2)
        fh.write("\n")
    os.replace(tmp, path)


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description="Demerzel compliance-report producer")
    demerzel_root = Path(__file__).resolve().parents[1]
    ap.add_argument("--repo", required=True, choices=["ix", "tars", "ga"])
    ap.add_argument("--repos-root", type=Path, default=demerzel_root.parent)
    ap.add_argument("--demerzel-root", type=Path, default=demerzel_root)
    ap.add_argument("--period-days", type=int, default=30)
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args(argv)

    mirror = (args.repos_root / args.repo / "governance" / "demerzel").resolve()
    if not (mirror / "personas").is_dir():
        print(f"error: no governance mirror at {mirror}", file=sys.stderr)
        return 1

    result = run_checks(mirror)
    print(f"checked {args.repo}: {json.dumps(result['checked'])}", file=sys.stderr)
    print(f"violations: {len(result['violations'])}", file=sys.stderr)
    for v in result["violations"]:
        print(f"  [{v['severity']}] {v['article']}: {v['description']}", file=sys.stderr)

    doc = _attach_integrity(build_report(args.repo, result, args.period_days), args.repo)
    out = (args.demerzel_root / "state" / "oversight" / "compliance-reports"
           / f"{doc['id']}-{doc['message_id'][:8]}.json")

    if args.dry_run:
        print(json.dumps(doc, indent=2))
        print(f"\n[dry-run] would write -> {out}", file=sys.stderr)
        return 0
    try:
        _atomic_write(out, doc)
    except OSError as exc:
        print(f"error: could not write report: {exc}", file=sys.stderr)
        return 1
    print(f"wrote compliance report ({doc['overall_status']}, "
          f"{len(result['violations'])} violations) -> {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
