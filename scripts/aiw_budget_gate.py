#!/usr/bin/env python3
"""Fail-closed budget preflight for one AIW provider invocation."""

from __future__ import annotations

import argparse
import json
import math
import os
from pathlib import Path
import sys
import time
from typing import Any


def _load(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as stream:
        value = json.load(stream)
    if not isinstance(value, dict):
        raise ValueError(f"{path}: expected a JSON object")
    return value


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


def _lock(path: Path):
    """Acquire a short-lived cross-process lock; fail closed if contended."""
    lock_path = Path(f"{path}.lock")
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
        return {"reserved_cost_usd": 0.0, "active_packets": 0, "reservations": {}}
    value = _load(path)
    for name in ("reserved_cost_usd", "active_packets"):
        _number(value, name)
    reservations = value.get("reservations", {})
    if not isinstance(reservations, dict):
        raise ValueError("cycle ledger reservations must be an object")
    return value


def reserve(policy: dict[str, Any], request: dict[str, Any], cycle_path: Path) -> dict[str, Any]:
    """Atomically reserve cycle capacity before the provider is invoked."""
    job_id = request.get("job_id")
    if not isinstance(job_id, str) or not job_id:
        raise ValueError("job_id is required for a cycle reservation")
    lock_path = _lock(cycle_path)
    try:
        cycle = _read_cycle(cycle_path)
        reservations = cycle["reservations"]
        if job_id in reservations:
            result = evaluate(policy, {**request,
                                       "cycle_spend_usd": cycle["reserved_cost_usd"],
                                       "cycle_active_packets": cycle["active_packets"]})
            result["reservation_reused"] = True
            return result
        result = evaluate(policy, {**request,
                                   "cycle_spend_usd": cycle["reserved_cost_usd"],
                                   "cycle_active_packets": cycle["active_packets"]})
        if result["decision"] == "allow":
            estimate = result["budget"]["estimated_cost_usd"]
            reservations[job_id] = {"estimated_cost_usd": estimate}
            cycle["reserved_cost_usd"] += estimate
            cycle["active_packets"] += 1
            cycle_path.parent.mkdir(parents=True, exist_ok=True)
            cycle_path.write_text(json.dumps(cycle, indent=2, sort_keys=True,
                                             allow_nan=False) + "\n", encoding="utf-8")
        return result
    finally:
        lock_path.unlink(missing_ok=True)


def release(cycle_path: Path, job_id: str, actual_cost_usd: float) -> dict[str, Any]:
    """Release a reservation and record the provider receipt when available."""
    if not job_id:
        raise ValueError("job_id is required for release")
    if not math.isfinite(actual_cost_usd) or actual_cost_usd < 0:
        raise ValueError("actual_cost_usd must be a non-negative number")
    lock_path = _lock(cycle_path)
    try:
        cycle = _read_cycle(cycle_path)
        reservation = cycle["reservations"].pop(job_id, None)
        if reservation is None:
            raise ValueError(f"no reservation for job: {job_id}")
        cycle["reserved_cost_usd"] -= reservation["estimated_cost_usd"]
        cycle["active_packets"] -= 1
        cycle["actual_cost_usd"] = cycle.get("actual_cost_usd", 0) + actual_cost_usd
        cycle_path.write_text(json.dumps(cycle, indent=2, sort_keys=True,
                                         allow_nan=False) + "\n", encoding="utf-8")
        return {"decision": "released", "job_id": job_id,
                "actual_cost_usd": actual_cost_usd}
    finally:
        lock_path.unlink(missing_ok=True)


def evaluate(policy: dict[str, Any], request: dict[str, Any]) -> dict[str, Any]:
    provider_id = request.get("provider")
    if not isinstance(provider_id, str) or not provider_id:
        raise ValueError("provider is required")
    providers = policy.get("providers")
    if not isinstance(providers, list):
        raise ValueError("policy.providers must be a list")
    provider = next((item for item in providers
                     if isinstance(item, dict) and item.get("id") == provider_id), None)
    if provider is None:
        raise ValueError(f"provider is not allowlisted: {provider_id}")

    defaults = policy.get("defaults")
    cycle = policy.get("cycle")
    if not isinstance(defaults, dict) or not isinstance(cycle, dict):
        raise ValueError("policy.defaults and policy.cycle are required")

    estimated_cost = _number(request, "estimated_cost_usd")
    cycle_spend = _number(request, "cycle_spend_usd")
    tokens = _number(request, "estimated_total_tokens")
    calls = _number(request, "estimated_model_calls")
    retries = _number(request, "estimated_retries")
    runner_minutes = _number(request, "estimated_runner_minutes")
    active_packets = _number(request, "cycle_active_packets")
    manual_approval = request.get("manual_approval") is True

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
    if cycle_spend + estimated_cost > float(cycle["max_cost_usd"]):
        reasons.append("cycle_cost_cap_exceeded")
    if tokens > max_tokens:
        reasons.append("token_cap_exceeded")
    if calls > max_calls:
        reasons.append("model_call_cap_exceeded")
    if retries > max_retries:
        reasons.append("retry_cap_exceeded")
    if runner_minutes > max_runner:
        reasons.append("runner_minutes_cap_exceeded")
    if active_packets >= float(cycle["max_parallel_packets"]):
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
    parser.add_argument("--policy", required=True, type=Path)
    parser.add_argument("--request", required=True, type=Path)
    parser.add_argument("--ledger", required=True, type=Path)
    parser.add_argument("--cycle-ledger", required=True, type=Path)
    parser.add_argument("--release-job")
    parser.add_argument("--actual-cost-usd", type=float)
    args = parser.parse_args(argv)
    try:
        if args.release_job:
            if args.actual_cost_usd is None:
                raise ValueError("--actual-cost-usd is required with --release-job")
            result = release(args.cycle_ledger, args.release_job, args.actual_cost_usd)
        else:
            result = reserve(_load(args.policy), _load(args.request), args.cycle_ledger)
        args.ledger.parent.mkdir(parents=True, exist_ok=True)
        args.ledger.write_text(json.dumps(result, indent=2, sort_keys=True,
                                          allow_nan=False) + "\n",
                               encoding="utf-8")
    except (OSError, ValueError, json.JSONDecodeError) as error:
        print(f"aiw budget gate: {error}", file=sys.stderr)
        return 2
    print(f"{result['decision'].upper()}: {args.ledger}")
    return 0 if result["decision"] == "allow" else 1


if __name__ == "__main__":
    raise SystemExit(main())
