#!/usr/bin/env python3
"""Fail-closed budget preflight for one AIW provider invocation."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from typing import Any


def _load(path: Path) -> dict[str, Any]:
    with path.open(encoding="utf-8") as stream:
        value = json.load(stream)
    if not isinstance(value, dict):
        raise ValueError(f"{path}: expected a JSON object")
    return value


def _number(request: dict[str, Any], name: str) -> float:
    value = request.get(name, 0)
    if isinstance(value, bool) or not isinstance(value, (int, float)) or value < 0:
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
    args = parser.parse_args(argv)
    try:
        result = evaluate(_load(args.policy), _load(args.request))
        args.ledger.parent.mkdir(parents=True, exist_ok=True)
        args.ledger.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n",
                               encoding="utf-8")
    except (OSError, ValueError, json.JSONDecodeError) as error:
        print(f"aiw budget gate: {error}", file=sys.stderr)
        return 2
    print(f"{result['decision'].upper()}: {args.ledger}")
    return 0 if result["decision"] == "allow" else 1


if __name__ == "__main__":
    raise SystemExit(main())
