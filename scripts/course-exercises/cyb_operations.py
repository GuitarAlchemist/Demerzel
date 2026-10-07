"""Synthetic, offline CYB-009..012 solutions. No runtime/session integration."""
import argparse
import copy
import hashlib
import json
import math
import platform
from datetime import datetime, timezone
from pathlib import Path


def next_attempt(last, failures, attempts, retry_after=0, deadline=40, response_received=None):
    """Minimum-spacing admission composed with capped failure backoff."""
    if min(last, failures, attempts, retry_after, deadline) < 0:
        raise ValueError("negative clock/count")
    if attempts >= 4:
        return None
    response_received = last if response_received is None else response_received
    if response_received < last:
        raise ValueError("response precedes request")
    candidate = max(last + 3, response_received + min(8, 2 ** min(failures, 3)),
                    response_received + retry_after)
    return candidate if candidate <= deadline else None


def valid_schedule(times):
    # This teaching sequence starts at zero and has a fixed deadline of 40.
    if (not times or len(times) > 4 or times[0] != 0
            or any(not isinstance(t, (int, float)) or not math.isfinite(t)
                   or not 0 <= t <= 40 for t in times)):
        return False
    for k, (a, b) in enumerate(zip(times, times[1:]), 1):
        earliest = next_attempt(a, k, k, deadline=40)
        if earliest is None or b < earliest:
            return False
    return True


def stopped(events, request="R1", epoch=7):
    """Ordered stop evidence; ACK alone never satisfies this contract."""
    stage = 0
    last = -1
    for e in events:
        if e["request"] != request or e["epoch"] != epoch or e["seq"] <= last:
            return False
        last = e["seq"]
        kind = e["kind"]
        if kind == "request" and stage == 0 and e.get("authorized"):
            stage = 1
        elif kind == "admission_closed" and stage == 1:
            stage = 2
        elif kind == "drained" and stage == 2 and e.get("inflight") == 0:
            stage = 3
        elif kind == "checkpoint" and stage == 3 and e.get("durable") and e.get("validated"):
            stage = 4
        elif kind == "stop_ack" and stage == 4:
            stage = 5
        else:
            return False
    return stage == 5


EDGES = {("queued", "running"): "admit", ("running", "draining"): "stop",
         ("draining", "stopped"): "drained", ("running", "done"): "complete",
         ("stopped", "queued"): "resume"}


def transition(state, target, event, generation, event_generation, *, authorized=False,
               inflight=0, lease=False, verified=False):
    if generation != event_generation or inflight < 0:
        raise ValueError("stale generation or invalid count")
    if EDGES.get((state, target)) != event:
        raise ValueError("illegal edge")
    guards = {"admit": authorized and lease,
              "stop": authorized,
              "drained": inflight == 0,
              "complete": inflight == 0 and verified,
              "resume": authorized and inflight == 0}
    if not guards[event]:
        raise ValueError("guard rejected")
    return target, generation + (event == "resume")


def oscillation(values, times=None, deadband=0.5):
    """Declared teaching rule, NOT a statistical stability test."""
    if len(values) < 6 or any(not math.isfinite(v) for v in values):
        raise ValueError("six finite samples required")
    times = list(range(len(values))) if times is None else times
    if len(times) != len(values) or any(not math.isfinite(t) for t in times):
        raise ValueError("invalid clock")
    gaps = [b-a for a, b in zip(times, times[1:])]
    if gaps[0] <= 0 or any(abs(g-gaps[0]) > 1e-9 for g in gaps):
        raise ValueError("uneven sampling: do not infer a reversal rate")
    # In-band samples break a candidate segment instead of vanishing from time.
    segment, best = [], []
    for v in values:
        if abs(v) <= deadband:
            if len(segment) > len(best):
                best = segment
            segment = []
        else:
            segment.append(v)
    if len(segment) > len(best):
        best = segment
    reversals = sum(a*b < 0 for a, b in zip(best, best[1:]))
    span = max(values)-min(values)
    contraction = abs(values[-1])/abs(values[0]) if values[0] else None
    persistent = (len(best) >= 6 and reversals >= 4 and span >= 4
                  and contraction is not None and contraction > 0.5)
    return {"flag": persistent, "reversals": reversals, "span": span,
            "contraction": contraction, "segment_length": len(best)}


def rejects(fn):
    try:
        fn()
    except ValueError:
        return True
    return False


def experiments():
    times = [0]
    for k in range(1, 4):
        times.append(next_attempt(times[-1], k, k))
    a = {"times": times, "server_wait": next_attempt(3, 2, 2, retry_after=10),
         "deadline_stop": next_attempt(3, 2, 2, retry_after=10, deadline=12),
         "budget_stop": next_attempt(15, 4, 4),
         "delayed_response_wait": next_attempt(3, 2, 2, retry_after=10, response_received=5),
         "delayed_deadline_stop": next_attempt(3, 2, 2, retry_after=10, deadline=14, response_received=5),
         "backwards_response_rejected": rejects(lambda: next_attempt(3, 2, 2, response_received=2))}
    expected_a = {"times": [0, 3, 7, 15], "server_wait": 13,
                  "deadline_stop": None, "budget_stop": None,
                  "delayed_response_wait": 15, "delayed_deadline_stop": None,
                  "backwards_response_rejected": True}
    p_a = a == expected_a and valid_schedule(times)
    n_a = (not valid_schedule([0, 100]) and not valid_schedule([0, 39, 40])
           and not valid_schedule([0, None]) and not valid_schedule([0, float('nan')])
           and not valid_schedule([]) and not valid_schedule([1, 4])
           and not valid_schedule([0, 1, 2, 3]) and not valid_schedule([0, 3, 6, 9])
           and 3 + 10 < a["delayed_response_wait"])  # start-origin mutant retries too early
    e = [{"request": "R1", "epoch": 7, "seq": i, "kind": kind, **details}
         for i, (kind, details) in enumerate([
             ("request", {"authorized": True}), ("admission_closed", {}),
             ("drained", {"inflight": 0}),
             ("checkpoint", {"durable": True, "validated": True}),
             ("stop_ack", {})], 1)]
    stale = copy.deepcopy(e); stale[-1]["epoch"] = 6
    busy = copy.deepcopy(e); busy[2]["inflight"] = 1
    late = e + [{"request": "R1", "epoch": 7, "seq": 6, "kind": "admitted_work"}]
    bad_hash = copy.deepcopy(e); bad_hash[3]["validated"] = False
    a_b = {"complete_chain": stopped(e), "ack_only": stopped(e[-1:]),
           "stale": stopped(stale), "busy": stopped(busy),
           "late_work": stopped(late), "unvalidated_checkpoint": stopped(bad_hash)}
    expected_b = {"complete_chain": True, "ack_only": False, "stale": False,
                  "busy": False, "late_work": False, "unvalidated_checkpoint": False}
    p_b = a_b == expected_b
    # Mutant accepts any acknowledgement, even before admission closure.
    n_b = any(x["kind"] == "stop_ack" for x in e[-1:]) and not stopped(e[-1:])
    state, gen = "queued", 3
    path = [state]
    for target, event, kwargs in [("running", "admit", {"authorized": True, "lease": True}),
                                  ("draining", "stop", {"authorized": True}),
                                  ("stopped", "drained", {}),
                                  ("queued", "resume", {"authorized": True})]:
        state, gen = transition(state, target, event, gen, gen, **kwargs)
        path.append(state)
    negatives = {
        "skip_to_done": rejects(lambda: transition("queued", "done", "complete", 3, 3, verified=True)),
        "busy_drain": rejects(lambda: transition("draining", "stopped", "drained", 3, 3, inflight=1)),
        "stale_completion": rejects(lambda: transition("running", "done", "complete", 4, 3, verified=True)),
        "unauthorized_resume": rejects(lambda: transition("stopped", "queued", "resume", 3, 3)),
        "unverified_completion": rejects(lambda: transition("running", "done", "complete", 3, 3)),
        "done_restart": rejects(lambda: transition("done", "queued", "resume", 3, 3, authorized=True))}
    a_c = {"path": path, "generation": gen, "negative_cases": negatives,
           "verified_done": transition("running", "done", "complete", 4, 4, verified=True)}
    expected_c = {"path": ["queued", "running", "draining", "stopped", "queued"],
                  "generation": 4, "negative_cases": {k: True for k in negatives},
                  "verified_done": ("done", 4)}
    p_c = a_c == expected_c
    n_c = all(negatives.values())  # permissive-edge/generation mutants fail these cases
    signals = {"persistent": [4, -4, 4, -4, 4, -4],
               "damped": [8, -4, 2, -1, .5, -.25],
               "noise": [.1, -.1, .1, -.1, .1, -.1],
               "drift": [1, 2, 3, 4, 5, 6],
               "positive_sawtooth": [1, 5, 1, 5, 1, 5]}
    metrics = {k: oscillation(v) for k, v in signals.items()}
    a_d = {"flags": {k: v["flag"] for k, v in metrics.items()},
           "persistent_reversals": metrics["persistent"]["reversals"],
           "uneven_rejected": rejects(lambda: oscillation(signals["persistent"], [0, 1, 2, 4, 5, 6]))}
    expected_d = {"flags": {k: k == "persistent" for k in signals},
                  "persistent_reversals": 5, "uneven_rejected": True}
    p_d = a_d == expected_d
    # Mutant counting only signed crossings calls tiny alternating noise oscillation.
    n_d = sum(a*b < 0 for a, b in zip(signals["noise"], signals["noise"][1:])) >= 4 and not a_d["flags"]["noise"]
    return [
        {"module": "CYB-009", "test_id": "admission_backoff", "inputs": {"spacing": 3, "base": 2, "cap": 8, "budget": 4}, "expected": expected_a, "actual": a, "positive_control": p_a, "negative_control_rejected": n_a},
        {"module": "CYB-010", "test_id": "ordered_stop_evidence", "inputs": e, "expected": expected_b, "actual": a_b, "positive_control": p_b, "negative_control_rejected": n_b},
        {"module": "CYB-011", "test_id": "guarded_lane_graph", "inputs": {"initial": "queued", "generation": 3}, "expected": expected_c, "actual": a_c, "positive_control": p_c, "negative_control_rejected": n_c},
        {"module": "CYB-012", "test_id": "windowed_error_reversals", "inputs": signals, "expected": expected_d, "actual": a_d, "metrics": metrics, "positive_control": p_d, "negative_control_rejected": n_d}]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    rows = experiments()
    result = {"synthetic": True, "utc": datetime.now(timezone.utc).isoformat(),
              "runtime": platform.python_version(),
              "sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              "command": "python <package>/overlay/scripts/course-exercises/cyb_operations.py --json",
              "experiments": rows,
              "passed": all(r["positive_control"] and r["negative_control_rejected"] for r in rows)}
    print(json.dumps(result, indent=2) if args.json else result["passed"])
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
