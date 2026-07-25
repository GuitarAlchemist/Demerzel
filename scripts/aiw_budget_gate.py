#!/usr/bin/env python3
"""Fail-closed budget preflight for one AIW provider invocation."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import math
import os
from pathlib import Path
import sys
import time
from typing import Any

import demerzel_kit


REPO_ROOT = Path(__file__).resolve().parents[1]
POLICY_PATH = REPO_ROOT / "state" / "driver" / "aiw-budget-policy.json"
LEDGER_PATH = REPO_ROOT / ".octo" / "aiw-budget-ledger.json"
CYCLE_LEDGER_PATH = REPO_ROOT / ".octo" / "aiw-cycle-ledger.json"
APPROVAL_PATH = REPO_ROOT / ".octo" / "aiw-approval.json"
RECEIPT_PATH = REPO_ROOT / ".octo" / "aiw-receipt.json"


def _load(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as stream:
        value = json.load(stream)
    if not isinstance(value, dict):
        raise ValueError(f"{path}: expected a JSON object")
    return value


class PolicyInvalid(ValueError):
    """The budget policy file itself is malformed or out of bounds.

    Distinct from an ordinary budget block. "We are out of budget" and "the file
    that decides the budget is broken" need opposite responses — the first is the
    gate working, the second is the gate being unable to work — and collapsing
    both into one reason code leaves an operator unable to tell them apart (#794).

    Subclasses ValueError so main()'s existing exit-2 mapping is unchanged.
    """


def load_policy(path: Path | None = None) -> dict[str, Any]:
    """Load the budget policy and validate it against its schema, fail-closed.

    The policy decides how much real money a cycle may spend and arrives as an
    ordinary PR diff, so an unrecognized or out-of-bounds key must be a load
    error rather than a silent no-op. Every failure is raised as ValueError so
    main() maps it to exit 2 (invalid) rather than exit 1 (governed block).
    """
    # An absent or unparseable policy file is the same class of failure as one
    # that fails schema validation: the gate cannot establish what it may spend.
    try:
        policy = _load(POLICY_PATH if path is None else path)
    except (OSError, json.JSONDecodeError, ValueError) as error:
        raise PolicyInvalid(f"policy could not be loaded: {error}") from error
    try:
        import jsonschema  # noqa: PLC0415 — optional dependency, imported lazily
    except ImportError as error:
        # demerzel_kit.validate() degrades to a warning when jsonschema is
        # absent. That is right for a reporting emitter and wrong for a spend
        # gate, so this caller refuses instead.
        raise PolicyInvalid(
            "jsonschema is required to validate the AIW budget policy") from error
    try:
        demerzel_kit.validate(policy, "aiw-budget-policy")
    except jsonschema.ValidationError as error:
        # json_path locates the offending key. Without it the message alone
        # ("True was expected") names neither field nor provider, which is not
        # enough to find the key in a 7-provider file under time pressure.
        raise PolicyInvalid(
            f"policy is invalid at {error.json_path}: {error.message}") from error

    # JSON Schema cannot express these cross-references within one document.
    ids = [provider["id"] for provider in policy["providers"]]
    duplicates = {name for name in ids if ids.count(name) > 1}
    if duplicates:
        raise PolicyInvalid(f"policy declares duplicate provider ids: {sorted(duplicates)}")
    undeclared = [name for name in policy["selection_order"] if name not in ids]
    if undeclared:
        raise PolicyInvalid(f"selection_order names undeclared providers: {undeclared}")
    return policy


def _number(request: dict[str, Any], name: str) -> float:
    value = request.get(name, 0)
    if (isinstance(value, bool) or not isinstance(value, (int, float))
            or not math.isfinite(value) or value < 0):
        raise ValueError(f"{name} must be a non-negative number")
    return float(value)


def _cap(request: dict[str, Any], name: str, policy_default: Any) -> float:
    """Allow a job to tighten policy caps, never widen them."""
    default = _number({name: policy_default}, name)
    if name not in request:
        return default
    value = _number(request, name)
    if value > default:
        raise ValueError(f"{name} cannot exceed policy default")
    return value


def _required_number(value: dict[str, Any], name: str) -> float:
    if name not in value:
        raise ValueError(f"{name} is required")
    return _number(value, name)


def _required_string(value: dict[str, Any], name: str) -> str:
    item = value.get(name)
    if not isinstance(item, str) or not item.strip():
        raise ValueError(f"{name} is required")
    return item


def _timestamp(value: dict[str, Any], name: str) -> str:
    item = _required_string(value, name)
    try:
        datetime.fromisoformat(item.replace("Z", "+00:00"))
    except ValueError as error:
        raise ValueError(f"{name} must be an ISO-8601 timestamp") from error
    return item


def _request_sha256(request: dict[str, Any]) -> str:
    """Bind authority and receipts to the provider request, not cycle aggregates."""
    if "manual_approval" in request:
        raise ValueError("manual_approval is not accepted in provider requests")
    bound = {key: value for key, value in request.items()
             if key not in {"cycle_spend_usd", "cycle_active_packets"}}
    payload = json.dumps(bound, sort_keys=True, separators=(",", ":"),
                         ensure_ascii=False, allow_nan=False).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def _provider(policy: dict[str, Any], provider_id: Any) -> dict[str, Any]:
    if not isinstance(provider_id, str) or not provider_id:
        raise ValueError("provider is required")
    providers = policy.get("providers")
    if not isinstance(providers, list):
        raise ValueError("policy.providers must be a list")
    provider = next((item for item in providers
                     if isinstance(item, dict) and item.get("id") == provider_id), None)
    if provider is None:
        raise ValueError(f"provider is not allowlisted: {provider_id}")
    return provider


def _is_metered(provider: dict[str, Any]) -> bool:
    """Metered providers bill real money and require a trusted receipt."""
    return provider.get("tier") == "metered-cloud"


def _validate_approval(approval: dict[str, Any] | None, request: dict[str, Any],
                       request_sha256: str) -> bool:
    if approval is None:
        return False
    expected = {
        "schema_version": "1.0",
        "kind": "human-approval",
        "decision": "approve",
        "job_id": request.get("job_id"),
        "provider": request.get("provider"),
        "request_sha256": request_sha256,
    }
    for name, value in expected.items():
        if approval.get(name) != value:
            raise ValueError(f"approval {name} does not match the request")
    _required_string(approval, "approval_id")
    _required_string(approval, "approver")
    _timestamp(approval, "approved_at")
    return True


def _validate_receipt(policy: dict[str, Any], receipt: dict[str, Any],
                      reservation: dict[str, Any]) -> tuple[str, float]:
    provider = _provider(policy, reservation.get("provider"))
    expected = {
        "schema_version": "1.0",
        "kind": "provider-receipt",
        "job_id": reservation.get("job_id"),
        "provider": reservation.get("provider"),
        "request_sha256": reservation.get("request_sha256"),
        "issuer": provider.get("trusted_receipt_issuer"),
    }
    for name, value in expected.items():
        if value is None or receipt.get(name) != value:
            raise ValueError(f"receipt {name} is not trusted for the reservation")
    receipt_id = _required_string(receipt, "receipt_id")
    _timestamp(receipt, "observed_at")
    actual_cost = _required_number(receipt, "actual_cost_usd")
    return receipt_id, actual_cost


def _lock(path: Path):
    """Acquire a short-lived cross-process lock; fail closed if contended."""
    lock_path = Path(f"{path}.lock")
    lock_path.parent.mkdir(parents=True, exist_ok=True)
    for _ in range(40):
        try:
            descriptor = os.open(lock_path, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
            os.close(descriptor)
            return lock_path
        except FileExistsError:
            time.sleep(0.05)
    raise ValueError("cycle ledger is busy")


def _read_cycle(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {"reserved_cost_usd": 0.0, "actual_cost_usd": 0.0,
                "active_packets": 0, "reservations": {}}
    value = _load(path)
    for name in ("reserved_cost_usd", "actual_cost_usd", "active_packets"):
        _required_number(value, name)
    reservations = value.get("reservations", {})
    if not isinstance(reservations, dict):
        raise ValueError("cycle ledger reservations must be an object")
    reserved = sum(_required_number(item, "estimated_cost_usd")
                   for item in reservations.values()
                   if isinstance(item, dict))
    if len(reservations) != sum(isinstance(item, dict) for item in reservations.values()):
        raise ValueError("cycle ledger reservation entries must be objects")
    if not math.isclose(reserved, value["reserved_cost_usd"], rel_tol=0, abs_tol=1e-9):
        raise ValueError("cycle ledger reserved cost does not match reservations")
    if value["active_packets"] != len(reservations):
        raise ValueError("cycle ledger active packet count does not match reservations")
    return value


def reserve(policy: dict[str, Any], request: dict[str, Any], cycle_path: Path,
            approval: dict[str, Any] | None = None) -> dict[str, Any]:
    """Atomically reserve cycle capacity before the provider is invoked."""
    job_id = request.get("job_id")
    if not isinstance(job_id, str) or not job_id:
        raise ValueError("job_id is required for a cycle reservation")
    request_sha256 = _request_sha256(request)
    provider_id = request.get("provider")
    lock_path = _lock(cycle_path)
    try:
        cycle = _read_cycle(cycle_path)
        reservations = cycle["reservations"]
        if job_id in reservations:
            reservation = reservations[job_id]
            # Reused job ids must carry the identical provider + request
            # fingerprint; a changed request cannot inherit an old grant.
            if (reservation.get("request_sha256") != request_sha256
                    or reservation.get("provider") != provider_id):
                raise ValueError(
                    f"job_id {job_id} reused with a different request fingerprint")
            return {"schema_version": "1.0", "job_id": job_id,
                    "provider": provider_id, "decision": "allow",
                    "reasons": [], "reservation_reused": True,
                    "request_sha256": request_sha256,
                    "budget": {"estimated_cost_usd": reservation["estimated_cost_usd"]}}
        result = evaluate(policy, {**request,
                                   "cycle_spend_usd": (cycle["reserved_cost_usd"]
                                                        + cycle["actual_cost_usd"]),
                                   "cycle_active_packets": cycle["active_packets"]},
                          approval=approval)
        if result["decision"] == "allow":
            estimate = result["budget"]["estimated_cost_usd"]
            reservations[job_id] = {
                "estimated_cost_usd": estimate,
                "provider": provider_id,
                "request_sha256": request_sha256,
                "max_cost_usd": result["budget"]["max_cost_usd"],
                "metered": _is_metered(_provider(policy, provider_id)),
            }
            cycle["reserved_cost_usd"] += estimate
            cycle["active_packets"] += 1
            cycle_path.parent.mkdir(parents=True, exist_ok=True)
            cycle_path.write_text(json.dumps(cycle, indent=2, sort_keys=True,
                                             allow_nan=False) + "\n", encoding="utf-8")
        return result
    finally:
        lock_path.unlink(missing_ok=True)


def note_release_failure(cycle_path: Path, job_id: str, error: str) -> bool:
    """Record that a release was attempted and swallowed, leaving a reservation open.

    The caller's ``except Exception`` around release is deliberate — a
    reconciliation hiccup must never break the loop — but the consequence is that
    reservations silently stop clearing while the cycle ledger keeps counting them
    as committed spend, and ``max_parallel_packets`` fills with reservations that
    will never clear. Fail-closed in the money direction, but a liveness failure:
    the cycle wedges quietly rather than stopping loudly (#794).

    Writing the swallow down makes that state detectable afterwards. Returns True
    if the note was recorded. Never raises: a failure to record a failure must not
    become a second failure.
    """
    try:
        lock_path = _lock(cycle_path)
    except ValueError:
        return False
    try:
        cycle = _read_cycle(cycle_path)
        notes = cycle.setdefault("release_failures", [])
        if not isinstance(notes, list):
            return False
        notes.append({
            "job_id": job_id,
            "error": str(error)[:200],
            "at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
            "reservation_open": job_id in cycle.get("reservations", {}),
        })
        cycle_path.write_text(json.dumps(cycle, indent=2, sort_keys=True,
                                         allow_nan=False) + "\n", encoding="utf-8")
        return True
    except Exception:  # noqa: BLE001 — recording is best-effort by construction
        return False
    finally:
        lock_path.unlink(missing_ok=True)


def release(cycle_path: Path, job_id: str, actual_cost_usd: float,
            policy: dict[str, Any] | None = None,
            receipt: dict[str, Any] | None = None) -> dict[str, Any]:
    """Release a reservation and reconcile the trusted provider receipt.

    Metered providers must supply a trusted receipt whose actual cost matches
    the released amount; spend over the reservation's admitted cap is recorded
    truthfully but returned as a blocking ``over_budget`` decision.
    """
    if not job_id:
        raise ValueError("job_id is required for release")
    if actual_cost_usd is None or not math.isfinite(actual_cost_usd) or actual_cost_usd < 0:
        raise ValueError("actual_cost_usd must be a non-negative number")
    lock_path = _lock(cycle_path)
    try:
        cycle = _read_cycle(cycle_path)
        reservation = cycle["reservations"].get(job_id)
        if reservation is None:
            raise ValueError(f"no reservation for job: {job_id}")

        reasons: list[str] = []
        receipt_id: str | None = None
        actual = actual_cost_usd
        if reservation.get("metered"):
            if receipt is None:
                raise ValueError(
                    "a trusted provider receipt is required to release a metered job")
            if policy is None:
                raise ValueError("policy is required to validate a metered receipt")
            receipt_id, receipt_actual = _validate_receipt(
                policy, receipt, {**reservation, "job_id": job_id})
            if not math.isclose(receipt_actual, actual_cost_usd, rel_tol=0, abs_tol=1e-9):
                raise ValueError(
                    "receipt actual_cost_usd does not match the released amount")
            actual = receipt_actual
            cap = reservation.get("max_cost_usd")
            if cap is not None and actual > cap:
                reasons.append("actual_cost_cap_exceeded")

        cycle["reservations"].pop(job_id)
        cycle["reserved_cost_usd"] -= reservation["estimated_cost_usd"]
        cycle["active_packets"] -= 1
        cycle["actual_cost_usd"] = cycle.get("actual_cost_usd", 0) + actual
        cycle_path.write_text(json.dumps(cycle, indent=2, sort_keys=True,
                                         allow_nan=False) + "\n", encoding="utf-8")
        result = {"decision": "over_budget" if reasons else "released",
                  "job_id": job_id, "actual_cost_usd": actual, "reasons": reasons}
        if receipt_id is not None:
            result["receipt_id"] = receipt_id
        return result
    finally:
        lock_path.unlink(missing_ok=True)


def _bind_canonical(name: str, supplied: Path, canonical: Path) -> Path:
    """Pin a runtime path to this repository, never the caller's directory.

    The policy and ledgers are governance state; a caller cannot redirect them
    to an attacker-controlled file by passing a different path.
    """
    if supplied.resolve() != canonical.resolve():
        raise ValueError(f"{name} must be {canonical}")
    return canonical.resolve()


def evaluate(policy: dict[str, Any], request: dict[str, Any],
             approval: dict[str, Any] | None = None) -> dict[str, Any]:
    provider_id = request.get("provider")
    provider = _provider(policy, provider_id)

    defaults = policy.get("defaults")
    cycle = policy.get("cycle")
    if not isinstance(defaults, dict) or not isinstance(cycle, dict):
        raise ValueError("policy.defaults and policy.cycle are required")
    cycle_max_cost = _required_number(cycle, "max_cost_usd")
    cycle_max_parallel = _required_number(cycle, "max_parallel_packets")

    estimated_cost = _number(request, "estimated_cost_usd")
    cycle_spend = _number(request, "cycle_spend_usd")
    tokens = _number(request, "estimated_total_tokens")
    calls = _number(request, "estimated_model_calls")
    retries = _number(request, "estimated_retries")
    runner_minutes = _number(request, "estimated_runner_minutes")
    active_packets = _number(request, "cycle_active_packets")

    # Fingerprint and approval bind authority to this exact request; compute
    # after the numeric fields are validated so bad inputs fail with clear
    # messages rather than a JSON-serialization error.
    request_sha256 = _request_sha256(request)
    manual_approval = _validate_approval(approval, request, request_sha256)

    reasons: list[str] = []
    max_cost = _cap(request, "max_cost_usd", defaults["max_cost_usd"])
    max_tokens = _cap(request, "max_total_tokens", defaults["max_total_tokens"])
    max_calls = _cap(request, "max_model_calls", defaults["max_model_calls"])
    max_retries = _cap(request, "max_retries", defaults["max_retries"])
    max_runner = _cap(request, "max_runner_minutes", defaults["max_runner_minutes"])
    approval_threshold = _cap(
        request, "approval_required_above_usd", defaults["approval_required_above_usd"])

    if estimated_cost > max_cost:
        reasons.append("job_cost_cap_exceeded")
    if cycle_spend + estimated_cost > cycle_max_cost:
        reasons.append("cycle_cost_cap_exceeded")
    if tokens > max_tokens:
        reasons.append("token_cap_exceeded")
    if calls > max_calls:
        reasons.append("model_call_cap_exceeded")
    if retries > max_retries:
        reasons.append("retry_cap_exceeded")
    if runner_minutes > max_runner:
        reasons.append("runner_minutes_cap_exceeded")
    if active_packets >= cycle_max_parallel:
        reasons.append("parallel_packet_cap_exceeded")
    if provider.get("requires_manual_approval") is True and not manual_approval:
        reasons.append("provider_requires_manual_approval")
    if estimated_cost > approval_threshold and not manual_approval:
        reasons.append("approval_threshold_exceeded")

    return {
        "schema_version": "1.0",
        "job_id": request.get("job_id", "unidentified"),
        "provider": provider_id,
        "tier": provider.get("tier"),
        "request_sha256": request_sha256,
        "decision": "allow" if not reasons else "block",
        "reasons": reasons,
        "budget": {
            "estimated_cost_usd": estimated_cost,
            "cycle_spend_usd": cycle_spend,
            "estimated_total_tokens": int(tokens),
            "estimated_model_calls": int(calls),
            "estimated_retries": int(retries),
            "estimated_runner_minutes": runner_minutes,
            "max_cost_usd": max_cost,
            "max_total_tokens": max_tokens,
            "max_model_calls": max_calls,
            "max_retries": max_retries,
            "max_runner_minutes": max_runner,
        },
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--policy", type=Path, default=POLICY_PATH)
    parser.add_argument("--request", type=Path)
    parser.add_argument("--ledger", type=Path, default=LEDGER_PATH)
    parser.add_argument("--cycle-ledger", type=Path, default=CYCLE_LEDGER_PATH)
    parser.add_argument("--approval", type=Path, default=APPROVAL_PATH)
    parser.add_argument("--receipt", type=Path, default=RECEIPT_PATH)
    parser.add_argument("--release-job")
    parser.add_argument("--actual-cost-usd", type=float)
    args = parser.parse_args(argv)
    try:
        # Policy and ledgers are pinned to canonical repository paths; the
        # caller may pass them explicitly but cannot redirect them elsewhere.
        _bind_canonical("--policy", args.policy, POLICY_PATH)
        _bind_canonical("--ledger", args.ledger, LEDGER_PATH)
        _bind_canonical("--cycle-ledger", args.cycle_ledger, CYCLE_LEDGER_PATH)
        _bind_canonical("--approval", args.approval, APPROVAL_PATH)
        _bind_canonical("--receipt", args.receipt, RECEIPT_PATH)
        policy = load_policy(POLICY_PATH)
        if args.release_job:
            if args.actual_cost_usd is None:
                raise ValueError("--actual-cost-usd is required with --release-job")
            receipt = _load(RECEIPT_PATH) if RECEIPT_PATH.exists() else None
            result = release(CYCLE_LEDGER_PATH, args.release_job, args.actual_cost_usd,
                             policy=policy, receipt=receipt)
        else:
            if args.request is None:
                raise ValueError("--request is required to reserve a job")
            approval = _load(APPROVAL_PATH) if APPROVAL_PATH.exists() else None
            result = reserve(policy, _load(args.request), CYCLE_LEDGER_PATH,
                             approval=approval)
        LEDGER_PATH.parent.mkdir(parents=True, exist_ok=True)
        LEDGER_PATH.write_text(json.dumps(result, indent=2, sort_keys=True,
                                          allow_nan=False) + "\n",
                               encoding="utf-8")
    except (OSError, ValueError, KeyError, TypeError, json.JSONDecodeError) as error:
        print(f"aiw budget gate: {error}", file=sys.stderr)
        return 2
    print(f"{result['decision'].upper()}: {LEDGER_PATH}")
    return 0 if result["decision"] in {"allow", "released"} else 1


if __name__ == "__main__":
    raise SystemExit(main())
