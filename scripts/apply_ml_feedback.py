#!/usr/bin/env python3
"""
Demerzel apply_ml_feedback — the *governor* half of the ML-governance feedback
loop. The companion producer (ix/scripts/confidence_calibrator.py) emits
ml-feedback-recommendation documents into state/oversight/ml-recommendations/;
this script is Demerzel applying them within her constitutional guardrails.

It executes, in plain Python, the governance steps that pipelines/
ml-feedback-loop.ixql §2-§6 describe but that no IxQL runtime exists to run:

  §2 Constitutional safety gate  — integrity (content_hash) check, drop
                                    modify_constitution/override_policy, require
                                    confidence >= 0.7 and constitutional_check.passed
  §3 Governance gate             — confidence >= 0.8 to proceed (else escalate)
  §4 Apply or escalate           — confidence >= 0.85 & low/med risk -> apply
                                    autonomously (bounded); else queue for human
  §6 Persist and log             — run summary + evolution-log append

"Apply" for a threshold_adjustment means writing a bounded nudge into
state/beliefs/confidence-calibration.belief.json (a hexavalent belief that
conforms to logic/tetravalent-state.schema.json). The nudge is hard-clamped to
+/- 0.10 (policy guardrail) and the prior value is recorded for reversibility
(Article 3). Every applied update carries its rationale (Article 2).

This is the Demerzel-side analogue of scripts/demerzel_halt.py: a governed,
operator-/loop-runnable action script that fills the role the (absent) IxQL
executor would otherwise play. It does NOT add governance *policy*; it enforces
the policy already written in YAML.

Usage:
  python scripts/apply_ml_feedback.py            # process the inbox
  python scripts/apply_ml_feedback.py --dry-run  # report decisions, write nothing

Exit codes:
  0  inbox processed (0+ applied, 0+ escalated)
  1  usage / IO error
  2  a recommendation failed integrity/required-field validation (still processes
     the rest; non-zero signals at least one rejection)
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

NUDGE_CAP = 0.10
MAX_RECONS_PER_DAY = 3   # §3b / policy guardrail
CONF_PROCEED = 0.70      # §2
CONF_GOVERNANCE = 0.80   # §3
CONF_AUTO_APPLY = 0.85   # §4
FORBIDDEN_TYPES = {"modify_constitution", "override_policy"}
# types with an autonomous applier (all bounded/reversible)
APPLICABLE_TYPES = {"threshold_adjustment", "proactive_recon", "pattern_report",
                    "strategy_change"}
REQUIRED = ["pipeline_id", "recommendation_type", "recommendation", "confidence",
            "evidence", "constitutional_check", "timestamp",
            "message_id", "origin_repo", "content_hash", "hash_algorithm"]


def _now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _verify_integrity(doc: dict) -> tuple[bool, str]:
    """Recompute the content_hash over the payload minus integrity fields and
    compare — the anti-tamper guard from integrity-fields.schema.json."""
    integrity_keys = {"message_id", "origin_repo", "origin_agent",
                      "content_hash", "hash_algorithm"}
    payload = {k: v for k, v in doc.items() if k not in integrity_keys}
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    expected = hashlib.sha256(canonical).hexdigest()
    if doc.get("hash_algorithm") != "sha256":
        return False, f"unexpected hash_algorithm {doc.get('hash_algorithm')!r}"
    if doc.get("content_hash") != expected:
        return False, "content_hash mismatch (tampered or malformed)"
    return True, "ok"


def _validate(doc: dict) -> tuple[bool, str]:
    missing = [k for k in REQUIRED if k not in doc]
    if missing:
        return False, f"missing required fields: {missing}"
    return _verify_integrity(doc)


def _gate(doc: dict) -> tuple[str, str]:
    """Return (decision, reason): 'apply' | 'escalate' | 'reject'."""
    rtype = doc["recommendation_type"]
    conf = doc["confidence"]
    cc = doc.get("constitutional_check", {})

    # §2 constitutional safety gate
    if rtype in FORBIDDEN_TYPES:
        return "reject", f"recommendation_type {rtype} touches constitution/policy — forbidden"
    if not cc.get("passed") is True:
        return "reject", "constitutional_check.passed is not true"
    if conf < CONF_PROCEED:
        return "reject", f"confidence {conf} < {CONF_PROCEED} (Article 6: act only on reliable signals)"

    # §3 governance gate
    if conf < CONF_GOVERNANCE:
        return "escalate", f"confidence {conf} < governance gate {CONF_GOVERNANCE}"

    # §4 bounded autonomous apply (calibration nudge / proactive recon = low risk)
    if rtype not in APPLICABLE_TYPES:
        return "escalate", f"no autonomous applier for type {rtype} — defer to human"
    if conf < CONF_AUTO_APPLY:
        return "escalate", f"confidence {conf} < auto-apply {CONF_AUTO_APPLY}"
    return "apply", f"confidence {conf} >= {CONF_AUTO_APPLY}, low-risk {rtype}"


def _atomic_write(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    with tmp.open("w", encoding="utf-8") as fh:
        json.dump(data, fh, indent=2)
        fh.write("\n")
    os.replace(tmp, path)


def _apply_nudge(root: Path, doc: dict, dry: bool) -> dict:
    """Write the bounded threshold nudge into the calibration belief. Returns the
    applied delta record (prior -> new) for the evolution log / reversibility."""
    params = doc["recommendation"].get("parameters", {})
    raw = float(params.get("threshold_nudge", 0.0))
    nudge = max(-NUDGE_CAP, min(NUDGE_CAP, raw))  # hard clamp (Article 9)

    belief_path = root / "state" / "beliefs" / "confidence-calibration.belief.json"
    prior = 0.0
    if belief_path.is_file():
        try:
            prior = float(json.loads(belief_path.read_text(encoding="utf-8"))
                          .get("calibration", {}).get("threshold_nudge", 0.0))
        except (json.JSONDecodeError, OSError, ValueError):
            prior = 0.0
    new_total = max(-NUDGE_CAP, min(NUDGE_CAP, round(prior + nudge, 4)))

    belief = {
        "proposition": "Demerzel's confidence-assignment threshold is calibrated against "
                       "the observed overconfidence-then-revision rate in her belief states.",
        "truth_value": "P",  # Probable: evidence leans true, magnitude still small-N
        "confidence": doc["confidence"],
        "evidence": {
            "supporting": [{
                "source": f"ml-feedback-recommendation {doc['message_id']}",
                "claim": doc["recommendation"]["rationale"],
                "timestamp": doc["timestamp"],
                "reliability": doc["confidence"],
            }],
            "contradicting": [],
        },
        "last_updated": _now_iso(),
        "evaluated_by": "demerzel",
        "calibration": {
            "threshold_nudge": new_total,
            "applied_delta": round(new_total - prior, 4),
            "prior_nudge": prior,                # Article 3: reversibility
            "cap": NUDGE_CAP,
            "source_recommendation": doc["message_id"],
            "rationale": doc["recommendation"]["rationale"],  # Article 2: self-explaining
        },
    }
    if not dry:
        _atomic_write(belief_path, belief)
    return {"prior_nudge": prior, "new_nudge": new_total,
            "applied_delta": round(new_total - prior, 4), "belief": str(belief_path)}


def _apply_recon_schedule(root: Path, doc: dict, dry: bool) -> dict:
    """Schedule proactive reconnaissance for the recommendation's targets, capped
    at MAX_RECONS_PER_DAY (Article 9 bound). Recon is a read/investigate action —
    inherently reversible — so the bounded apply is appropriate. Appends to a
    dated queue rather than overwriting, so multiple cycles accumulate safely."""
    params = doc["recommendation"].get("parameters", {})
    targets = list(params.get("recon_targets", []))[:MAX_RECONS_PER_DAY]  # hard cap

    date = _now_iso()[:10]
    queue_path = root / "state" / "oversight" / f"scheduled-recons-{date}.json"
    queue = {"date": date, "max_per_day": MAX_RECONS_PER_DAY, "recons": []}
    if queue_path.is_file():
        try:
            queue = json.loads(queue_path.read_text(encoding="utf-8"))
            queue.setdefault("recons", [])
        except (json.JSONDecodeError, OSError):
            pass
    already = {r.get("target") for r in queue["recons"]}
    remaining = max(0, MAX_RECONS_PER_DAY - len(queue["recons"]))
    scheduled = []
    for t in targets:
        if remaining <= 0:
            break
        if t in already:
            continue
        queue["recons"].append({
            "target": t, "status": "scheduled",
            "source_recommendation": doc["message_id"],
            "rationale": doc["recommendation"]["rationale"],  # Art.2 self-explaining
            "scheduled_at": _now_iso(),
        })
        scheduled.append(t)
        remaining -= 1
    if not dry:
        _atomic_write(queue_path, queue)
    return {"scheduled": scheduled, "skipped_over_cap": targets[len(scheduled):],
            "queue": str(queue_path), "day_total": len(queue["recons"])}


def _apply_policy_review_request(root: Path, doc: dict, dry: bool) -> dict:
    """File NON-BINDING policy-review requests for systemic patterns. Per the
    violation_pattern_detector policy guardrail ("Cannot auto-create policies —
    only recommends"), this NEVER edits a file under policies/ — it only queues a
    request for a human to review. That makes it bounded + reversible, so it is
    eligible for autonomous apply. Note: ml-feedback-loop.ixql §3c uses a stricter
    `systemic_patterns.count >= 2` trigger; the policy text ("systemic patterns
    trigger policy review") sets no count, so we file for >= 1 and record the
    count for the operator — flagged in the PR as a threshold to reconcile."""
    params = doc["recommendation"].get("parameters", {})
    systemic = params.get("systemic_patterns", [])
    emerging = params.get("emerging_risks", [])

    queue_path = root / "state" / "oversight" / "policy-review-requests.json"
    queue = {"requests": []}
    if queue_path.is_file():
        try:
            queue = json.loads(queue_path.read_text(encoding="utf-8"))
            queue.setdefault("requests", [])
        except (json.JSONDecodeError, OSError):
            pass
    existing = {r.get("pattern_type") for r in queue["requests"] if r.get("status") == "review-requested"}
    filed = []
    for pat in systemic:
        key = pat.get("type")
        if key in existing:
            continue
        queue["requests"].append({
            "pattern_type": key,
            "repos": pat.get("repos", []),
            "max_severity": pat.get("max_severity"),
            "root_cause_hypothesis": pat.get("root_cause_hypothesis"),
            "status": "review-requested",          # advisory — NOT an applied policy change
            "binding": False,
            "source_recommendation": doc["message_id"],
            "filed_at": _now_iso(),
        })
        filed.append(key)
    if not dry:
        _atomic_write(queue_path, queue)
    return {"filed_review_requests": filed, "systemic_count": len(systemic),
            "emerging_risks": len(emerging), "policies_modified": 0,  # invariant: never
            "queue": str(queue_path)}


def _apply_remediation_rates(root: Path, doc: dict, dry: bool) -> dict:
    """Record observed remediation-strategy success rates into the remediation-
    effectiveness belief (ml-feedback-loop.ixql §3d). This is OBSERVATIONAL: it
    stores evidence (success rates) and keeps recommended escalation changes as
    *advisory* — it NEVER downgrades a risk classification autonomously, per the
    policy guardrail ("Cannot downgrade high-risk gaps without human approval").
    Prior value recorded for reversibility (Art.3)."""
    params = doc["recommendation"].get("parameters", {})
    rates = params.get("success_rates_by_strategy", {})
    escalations = params.get("recommended_escalation_changes", [])

    belief_path = root / "state" / "beliefs" / "remediation-effectiveness.belief.json"
    prior = {}
    if belief_path.is_file():
        try:
            prior = json.loads(belief_path.read_text(encoding="utf-8")).get("strategy_success_rates", {})
        except (json.JSONDecodeError, OSError):
            prior = {}

    belief = {
        "proposition": "Remediation-strategy effectiveness is tracked from PDCA outcomes; "
                       "fragile strategies stay human-gated.",
        "truth_value": "P",
        "confidence": doc["confidence"],
        "evidence": {
            "supporting": [{
                "source": f"ml-feedback-recommendation {doc['message_id']}",
                "claim": doc["recommendation"]["rationale"],
                "timestamp": doc["timestamp"],
                "reliability": doc["confidence"],
            }],
            "contradicting": [],
        },
        "last_updated": _now_iso(),
        "evaluated_by": "demerzel",
        "strategy_success_rates": rates,
        "prior_strategy_success_rates": prior,                 # Art.3 reversibility
        "advisory_escalation_changes": escalations,            # NOT applied — human-gated
        "risk_classes_modified": 0,                            # invariant: never autonomous
        "source_recommendation": doc["message_id"],
    }
    if not dry:
        _atomic_write(belief_path, belief)
    return {"strategies_recorded": list(rates), "advisory_escalations": len(escalations),
            "risk_classes_modified": 0, "belief": str(belief_path)}


# type -> applier; gate guarantees only APPLICABLE_TYPES reach 'apply'
_APPLIERS = {
    "threshold_adjustment": _apply_nudge,
    "proactive_recon": _apply_recon_schedule,
    "pattern_report": _apply_policy_review_request,
    "strategy_change": _apply_remediation_rates,
}


def _append_evolution(root: Path, event: dict, dry: bool) -> None:
    path = root / "state" / "evolution" / "ml-feedback-loop.evolution.json"
    log = {"artifact": "ml-feedback-loop", "events": []}
    if path.is_file():
        try:
            log = json.loads(path.read_text(encoding="utf-8"))
            log.setdefault("events", [])
        except (json.JSONDecodeError, OSError):
            pass
    log["events"].append(event)
    if not dry:
        _atomic_write(path, log)


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description="Demerzel ML-feedback applier (governor)")
    root = Path(__file__).resolve().parents[1]  # repos/Demerzel
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args(argv)

    inbox = root / "state" / "oversight" / "ml-recommendations"
    pending = sorted(p for p in inbox.glob("*.json")) if inbox.is_dir() else []
    if not pending:
        print(f"inbox empty ({inbox}) — nothing to apply.")
        return 0

    applied, escalated, rejected = [], [], []
    for p in pending:
        try:
            doc = json.loads(p.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError) as exc:
            print(f"REJECT {p.name}: unreadable ({exc})", file=sys.stderr)
            rejected.append({"file": p.name, "reason": str(exc)})
            continue

        ok, why = _validate(doc)
        if not ok:
            print(f"REJECT {p.name}: {why}", file=sys.stderr)
            rejected.append({"file": p.name, "message_id": doc.get("message_id"), "reason": why})
            continue

        decision, reason = _gate(doc)
        print(f"{decision.upper():8} {p.name}: {reason}")

        if decision == "reject":
            rejected.append({"message_id": doc["message_id"], "reason": reason})
            evt = {"event": "ml_recommendation_rejected", "timestamp": _now_iso(),
                   "message_id": doc["message_id"], "reason": reason}
        elif decision == "escalate":
            escalated.append({"message_id": doc["message_id"], "reason": reason,
                              "recommendation": doc["recommendation"]})
            evt = {"event": "ml_recommendation_escalated", "timestamp": _now_iso(),
                   "message_id": doc["message_id"], "reason": reason}
        else:  # apply — dispatch on type (gate ensures an applier exists)
            delta = _APPLIERS[doc["recommendation_type"]](root, doc, args.dry_run)
            applied.append({"message_id": doc["message_id"],
                            "type": doc["recommendation_type"], **delta})
            evt = {"event": "ml_recommendation_applied", "timestamp": _now_iso(),
                   "message_id": doc["message_id"],
                   "recommendation_type": doc["recommendation_type"], "metrics": delta}
        _append_evolution(root, evt, args.dry_run)

        # §step: mark processed by moving out of the inbox (no 'status' field in schema)
        if not args.dry_run and decision != "reject":
            dest = inbox / "processed"
            dest.mkdir(parents=True, exist_ok=True)
            os.replace(p, dest / p.name)

    # §4 escalations -> human review queue
    if escalated:
        q = root / "state" / "oversight" / "pending-human-review.json"
        payload = {"updated_at": _now_iso(), "queued": escalated}
        if not args.dry_run:
            _atomic_write(q, payload)
        print(f"queued {len(escalated)} for human review -> {q}")

    # §6 run summary
    summary = {
        "run_at": _now_iso(),
        "results_in": len(pending),
        "applied": len(applied),
        "escalated": len(escalated),
        "rejected": len(rejected),
        "applied_detail": applied,
    }
    date = _now_iso()[:10]
    if not args.dry_run:
        _atomic_write(root / "state" / "oversight" / f"ml-feedback-loop-{date}.json", summary)
    print(f"\nsummary: {json.dumps(summary, indent=2)}")

    return 2 if rejected else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
