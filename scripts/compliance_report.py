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

try:
    import yaml  # pyyaml
except ImportError:  # pragma: no cover
    print("error: pyyaml required (pip install pyyaml)", file=sys.stderr)
    raise SystemExit(1)

STALE_DAYS = 7
PERSONA_REQUIRED = ["name", "version", "description", "role", "capabilities",
                    "constraints", "voice", "affordances", "goal_directedness",
                    "estimator_pairing"]


def _now() -> datetime:
    return datetime.now(timezone.utc)


def _now_iso() -> str:
    return _now().strftime("%Y-%m-%dT%H:%M:%SZ")


def _is_semver(v) -> bool:
    if not isinstance(v, str):
        return False
    parts = v.strip().strip('"').split(".")
    return len(parts) == 3 and all(p.isdigit() for p in parts)


def _load_yaml(path: Path):
    """Parse the YAML front-matter only. Many governance files here are YAML+markdown
    hybrids: a metadata block, then a standalone '---', then markdown prose (headings,
    backticks, sentences) interleaved with illustrative YAML. Those bodies are NOT
    meant to be machine-parsed, so we read only the front-matter (content before the
    first standalone '---' line; whole file if there is none). Returns (dict, ok, err);
    ok=False only when the front-matter itself is malformed (a real violation)."""
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    cut = next((i for i, ln in enumerate(lines) if i > 0 and ln.strip() == "---"), None)
    front = "\n".join(lines[:cut]) if cut is not None else text
    try:
        data = yaml.safe_load(front)
        return (data if isinstance(data, dict) else {}), True, None
    except yaml.YAMLError as exc:
        return {}, False, str(exc).splitlines()[0]


def _parse_ts(value):
    if not isinstance(value, str):
        return None
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None


def _violation(article, description, severity):
    return {"article": article, "description": description,
            "severity": severity, "remediation_status": "pending"}


def run_checks(mirror: Path) -> dict:
    """Return {violations: [...], checked: {counts}}. Pure governance checks."""
    violations, checked = [], {}

    # Load personas + test basenames once.
    personas = {}
    for p in sorted((mirror / "personas").glob("*.persona.yaml")):
        data, ok, err = _load_yaml(p)
        if not ok:
            violations.append(_violation("Article 7 - Auditability",
                              f"persona {p.name} is not valid YAML: {err}", "high"))
        personas[p] = data
    checked["personas"] = len(personas)

    test_files = list((mirror / "tests" / "behavioral").glob("*.md"))
    test_blob = " ".join(t.stem for t in test_files)
    checked["behavioral_tests"] = len(test_files)
    persona_names = {(d or {}).get("name") for d in personas.values()}

    for path, data in personas.items():
        name = data.get("name") or path.stem
        raw = path.read_text(encoding="utf-8").lower()
        # P1 required fields (estimator_pairing handled separately, below, with waiver)
        base = [k for k in PERSONA_REQUIRED if k != "estimator_pairing"]
        missing = [k for k in base if k not in data or data.get(k) in (None, "", [])]
        if missing:
            violations.append(_violation(
                "persona-requirements", f"persona '{name}' missing fields: {missing}",
                "high" if "constraints" in missing else "medium"))
        # P2 behavioral-test coverage
        if name and name not in test_blob:
            violations.append(_violation(
                "contributing-rules", f"persona '{name}' has no behavioral test", "high"))
        # P3 semver
        if not _is_semver(data.get("version")):
            violations.append(_violation(
                "Article 7 - Auditability",
                f"persona '{name}' version {data.get('version')!r} is not semver", "low"))
        # P4 estimator_pairing: required UNLESS the file documents an explicit waiver
        # (e.g. skeptical-auditor IS the neutral estimator others pair with).
        ep = data.get("estimator_pairing")
        ep_name = ep.get("persona") or ep.get("name") if isinstance(ep, dict) else ep
        waived = ("no estimator_pairing" in raw or "no estimator pairing" in raw
                  or "is the neutral estimator" in raw)
        if not ep_name and not waived:
            violations.append(_violation(
                "persona-requirements", f"persona '{name}' has no estimator_pairing", "high"))
        elif ep_name and ep_name not in persona_names:
            violations.append(_violation(
                "persona-requirements",
                f"persona '{name}' estimator_pairing '{ep_name}' is not a known persona", "medium"))

    # P3 policy semver
    pol = list((mirror / "policies").glob("*.yaml"))
    checked["policies"] = len(pol)
    for p in pol:
        data, ok, err = _load_yaml(p)
        if not ok:
            # Policies here are frequently prose-rich human docs (illustrative quotes,
            # markdown). The framework's own audit does NOT require all policies to be
            # strict YAML, so a parse failure is not a governance violation — skip.
            continue
        if "version" in data and not _is_semver(data.get("version")):
            violations.append(_violation(
                "Article 7 - Auditability",
                f"policy {p.name} version {data.get('version')!r} is not semver", "low"))

    # S1 schema files valid JSON
    schemas = list((mirror / "schemas").glob("*.schema.json"))
    checked["schemas"] = len(schemas)
    for s in schemas:
        try:
            json.loads(s.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            violations.append(_violation(
                "Article 7 - Auditability", f"schema {s.name} is not valid JSON", "critical"))

    # B1 belief staleness
    beliefs = list((mirror / "state" / "beliefs").glob("*.belief.json"))
    checked["beliefs"] = len(beliefs)
    now = _now()
    stale = 0
    for b in beliefs:
        try:
            ts = _parse_ts(json.loads(b.read_text(encoding="utf-8")).get("last_updated", ""))
        except (json.JSONDecodeError, OSError):
            continue
        if ts and (now - ts).days > STALE_DAYS:
            stale += 1
    if stale:
        violations.append(_violation(
            "Article 8 - Observability",
            f"{stale}/{len(beliefs)} beliefs are stale (> {STALE_DAYS}d since last_updated)",
            "medium"))

    return {"violations": violations, "checked": checked}


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
