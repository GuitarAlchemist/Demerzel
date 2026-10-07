"""Offline teaching fixtures for CYB-021--025; not a runtime controller."""
import argparse
import copy
import datetime
import hashlib
import json
import math
import pathlib
import platform
import sys


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()).hexdigest()


def budget_trace(costs, estimates, cap=3, credits=9, deadline=6):
    """Reserve worst-case duration and credits before admitting a single action."""
    if cap <= 0 or credits < 0 or deadline < 0 or len(costs) != len(estimates):
        raise ValueError("invalid budget")
    used, spent, elapsed = 0, 0, 0
    trace = []
    for cost, duration in zip(costs, estimates):
        if cost <= 0 or duration <= 0:
            raise ValueError("estimates must be positive")
        reasons = []
        if used + 1 > cap:
            reasons.append("attempt_cap")
        if spent + cost > credits:
            reasons.append("credit_cap")
        if elapsed + duration > deadline:
            reasons.append("deadline")
        if reasons:
            trace.append({"admitted": False, "reasons": reasons})
            break
        used, spent, elapsed = used + 1, spent + cost, elapsed + duration
        trace.append({"admitted": True, "attempts": used, "credits": spent, "time": elapsed})
    return {"attempts": used, "credits": spent, "time": elapsed, "trace": trace}


def assess_progress(previous, candidate, target_version="v1"):
    """External measurement, not a candidate's self-report, defines progress."""
    if candidate["target"] != target_version:
        return "target_changed"
    if candidate["validated_revision"] != candidate["revision"]:
        return "stale_validation"
    if not isinstance(candidate["residual"], (int, float)) or not math.isfinite(candidate["residual"]) or candidate["residual"] < 0:
        return "invalid_measurement"
    if candidate["revision"] <= previous["revision"]:
        return "stale_revision"
    if candidate["residual"] > previous["residual"]:
        return "regression"
    if candidate["residual"] == previous["residual"]:
        return "stall"
    if candidate["artifact"] == previous["artifact"]:
        return "unexplained_measurement"
    return "complete" if candidate["residual"] == 0 else "progress"


def make_chain(artifact, request="exercise-job", generation=2):
    chain = []
    artifact_hash = digest(artifact)
    previous = "ROOT"
    for index, stage in enumerate(("submitted", "accepted", "completed", "verified")):
        entry = {"index": index, "stage": stage, "request": request, "generation": generation,
                 "artifact": artifact_hash, "previous": previous, "verification_passed": stage == "verified"}
        entry["hash"] = digest(entry)
        previous = entry["hash"]
        chain.append(entry)
    return chain


def verify_chain(chain, artifact, request="exercise-job", generation=2):
    if len(chain) != 4:
        return False
    previous = "ROOT"
    for index, stage in enumerate(("submitted", "accepted", "completed", "verified")):
        row = dict(chain[index])
        observed_hash = row.pop("hash", None)
        if row.get("index") != index or row.get("stage") != stage:
            return False
        if row.get("request") != request or row.get("generation") != generation:
            return False
        if row.get("artifact") != digest(artifact) or row.get("previous") != previous:
            return False
        if observed_hash != digest(row):
            return False
        previous = observed_hash
    return chain[-1]["verification_passed"] is True


def audit_audio(samples, gain, receipt):
    """Test numerical signal integrity only; return no perceptual success claim."""
    if not samples or not math.isfinite(gain) or any(not math.isfinite(x) for x in samples):
        return {"mechanical": "rejected", "reason": "invalid_numbers", "perceptual": "not_tested"}
    output = [x * gain for x in samples]
    if any(not math.isfinite(x) for x in output):
        return {"mechanical": "rejected", "reason": "nonfinite_output", "perceptual": "not_tested"}
    expected = {"input": digest(samples), "configuration": digest({"gain": gain}), "output": digest(output)}
    if receipt != expected:
        return {"mechanical": "rejected", "reason": "provenance_mismatch", "perceptual": "not_tested"}
    peak = max(abs(x) for x in output)
    rms = math.sqrt(sum(x * x for x in output) / len(output))
    return {"mechanical": "accepted" if peak <= 1 else "rejected",
            "reason": "within_peak_bound" if peak <= 1 else "peak_exceeds_bound",
            "peak": peak, "rms": rms, "perceptual": "not_tested"}


def audio_receipt(samples, gain):
    return {"input": digest(samples), "configuration": digest({"gain": gain}), "output": digest([x * gain for x in samples])}


class Coordinator:
    """Single-threaded event model; a real concurrent system needs atomic storage."""
    def __init__(self):
        self.pending = ["r1", "r2", "r3"]
        self.active = {}
        self.done = set()
        self.epochs = {}
        self.history = []

    def invariant(self):
        pending, active = set(self.pending), set(self.active)
        return (len(self.pending) == len(pending) and not (pending & active or pending & self.done or active & self.done)
                and pending | active | self.done == {"r1", "r2", "r3"}
                and len(self.active) <= 2
                and len({v[0] for v in self.active.values()}) == len(self.active))

    def apply(self, action, request, worker, epoch):
        outcome = "ignored"
        if action == "assign":
            next_epoch = self.epochs.get(request, 0) + 1
            if (request in self.pending and len(self.active) < 2
                    and worker not in [v[0] for v in self.active.values()] and epoch == next_epoch):
                self.pending.remove(request)
                self.active[request] = (worker, epoch)
                self.epochs[request] = epoch
                outcome = "assigned"
        elif action in ("fail", "complete") and self.active.get(request) == (worker, epoch):
            del self.active[request]
            if action == "fail":
                self.pending.append(request)
                outcome = "requeued"
            else:
                self.done.add(request)
                outcome = "completed"
        if not self.invariant():
            raise AssertionError("coordination invariant broken")
        self.history.append({"event": [action, request, worker, epoch], "outcome": outcome,
                             "pending": list(self.pending), "active": copy.deepcopy(self.active), "done": sorted(self.done)})
        return outcome


def record(module, test_id, inputs, expected, actual, positive, negative):
    passed = actual == expected and positive and negative
    return {"module": module, "test_id": test_id, "synthetic": True, "inputs": inputs,
            "expected": expected, "actual": actual, "positive_control": positive,
            "negative_control_rejected": negative, "passed": passed}


def run_tests():
    results = []
    b = budget_trace([2, 2, 2, 2], [1, 1, 1, 1])
    credit = budget_trace([4, 4, 4], [1, 1, 1])
    time_limit = budget_trace([1, 1], [4, 4])
    invalid = False
    try:
        budget_trace([0], [1])
    except ValueError:
        invalid = True
    actual = {"attempts": b["attempts"], "fourth_rejected": b["trace"][-1]["reasons"],
              "credit_attempts": credit["attempts"], "time_attempts": time_limit["attempts"]}
    expected = {"attempts": 3, "fourth_rejected": ["attempt_cap"], "credit_attempts": 2, "time_attempts": 1}
    mutant_actions = []
    # Deliberately wrong ordering, bounded so the negative fixture cannot hang.
    for candidate in range(10):
        mutant_actions.append(candidate + 1)  # simulated side effect happens first
        if len(mutant_actions) > 3:
            break
    mutant_attempts = len(mutant_actions)
    actual["post_action_mutant_trace"] = mutant_actions
    expected["post_action_mutant_trace"] = [1, 2, 3, 4]
    results.append(record("CYB-021", "budget_admission", {"cap": 3, "credits": 9, "deadline": 6}, expected, actual,
                          b["credits"] == 6, mutant_attempts > b["attempts"] and invalid))

    initial = {"revision": 0, "artifact": "a0", "residual": 10}
    states = [{"revision": i, "validated_revision": i, "artifact": "a" + str(i), "residual": r, "target": "v1"}
              for i, r in enumerate([8, 8, 5, 0], 1)]
    previous, statuses = initial, []
    for state in states:
        status = assess_progress(previous, state)
        statuses.append(status)
        if status in ("progress", "complete"):
            previous = state
    stale = dict(states[0], validated_revision=0)
    changed = dict(states[0], target="v2")
    bogus = dict(states[0], artifact="a0")
    regress = dict(states[0], residual=11)
    negative = (assess_progress(initial, stale) == "stale_validation" and assess_progress(initial, changed) == "target_changed"
                and assess_progress(initial, bogus) == "unexplained_measurement" and assess_progress(initial, regress) == "regression"
                and states[1]["artifact"] != states[0]["artifact"] and statuses[1] == "stall")
    results.append(record("CYB-022", "external_progress", {"residuals": [10, 8, 8, 5, 0], "target": "v1"},
                          ["progress", "stall", "progress", "complete"], statuses, previous["residual"] == 0, negative))

    artifact = {"answer": [2, 4], "checker": "exact-v1"}
    chain = make_chain(artifact)
    tampered = copy.deepcopy(chain)
    tampered[2]["artifact"] = digest({"answer": [9]})
    negative = (not verify_chain(chain[:2], artifact) and not verify_chain(tampered, artifact)
                and not verify_chain(chain, artifact, generation=3)
                and not verify_chain(make_chain(artifact, request="other"), artifact)
                and not verify_chain([chain[1], chain[0], chain[2], chain[3]], artifact)
                and not verify_chain(chain, {"answer": [2, 5], "checker": "exact-v1"}))
    results.append(record("CYB-023", "receipt_chain", {"stages": [r["stage"] for r in chain], "generation": 2},
                          True, verify_chain(chain, artifact), verify_chain(chain, artifact), negative))

    samples = [-0.6, 0.2, 0.6, -0.2]
    good = audit_audio(samples, 0.5, audio_receipt(samples, 0.5))
    clipped = audit_audio(samples, 2, audio_receipt(samples, 2))
    mismatch = audit_audio(samples, 0.5, audio_receipt(samples, 1))
    invalid_audio = audit_audio([float("nan")], 1, {})
    overflow_audio = audit_audio([1e308], 1e308, {})
    actual = {"mechanical": good["mechanical"], "peak": good["peak"], "rms_squared": round(good["rms"] ** 2, 8), "perceptual": good["perceptual"]}
    expected = {"mechanical": "accepted", "peak": 0.3, "rms_squared": 0.05, "perceptual": "not_tested"}
    results.append(record("CYB-024", "audio_audit", {"samples": samples, "gain": 0.5, "peak_limit": 1}, expected, actual,
                          good["mechanical"] == "accepted", clipped["mechanical"] == "rejected"
                          and mismatch["reason"] == "provenance_mismatch" and invalid_audio["reason"] == "invalid_numbers"
                          and overflow_audio["reason"] == "nonfinite_output" and good["perceptual"] != "accepted"))

    c = Coordinator()
    events = [("assign", "r1", "A", 1), ("assign", "r2", "B", 1), ("fail", "r1", "A", 1),
              ("complete", "r2", "B", 1), ("assign", "r1", "B", 2), ("complete", "r1", "A", 1),
              ("complete", "r1", "B", 2), ("complete", "r1", "B", 2), ("assign", "r3", "A", 1),
              ("complete", "r3", "A", 99), ("complete", "r3", "A", 1)]
    outcomes = [c.apply(*e) for e in events]
    busy = Coordinator()
    busy.apply("assign", "r1", "A", 1)
    busy_rejected = busy.apply("assign", "r3", "A", 1) == "ignored" and "r3" in busy.pending
    busy.apply("assign", "r2", "B", 1)
    capacity_rejected = busy.apply("assign", "r3", "C", 1) == "ignored" and len(busy.active) == 2
    actual = {"done": sorted(c.done), "active": len(c.active), "pending": len(c.pending),
              "ignored_disturbances": [outcomes[i] for i in (5, 7, 9)], "invariant": c.invariant(),
              "active_counts": [len(row["active"]) for row in c.history], "done_counts": [len(row["done"]) for row in c.history]}
    expected = {"done": ["r1", "r2", "r3"], "active": 0, "pending": 0,
                "ignored_disturbances": ["ignored", "ignored", "ignored"], "invariant": True,
                "active_counts": [1, 2, 1, 0, 1, 1, 0, 0, 1, 1, 0], "done_counts": [0, 0, 0, 1, 1, 1, 2, 2, 2, 2, 3]}
    mutant = Coordinator()
    mutant.apply("assign", "r1", "A", 1)
    mutant.apply("fail", "r1", "A", 1)
    mutant.apply("assign", "r1", "B", 2)
    stale_rejected = mutant.apply("complete", "r1", "A", 1) == "ignored" and "r1" in mutant.active
    results.append(record("CYB-025", "disturbance_capstone", {"events": events, "capacity": 2, "conserved_requests": 3},
                          expected, actual, all(r["outcome"] in ("assigned", "completed", "requeued", "ignored") for r in c.history),
                          stale_rejected and busy_rejected and capacity_rejected and outcomes[9] == "ignored" and outcomes[7] == "ignored"))
    return results


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--receipt", type=pathlib.Path, help="Save this offline execution's local evidence")
    args = parser.parse_args()
    results = run_tests()
    output = {"suite": "cyb_governed_loops", "synthetic_only": True, "records": results, "passed": all(r["passed"] for r in results)}
    if args.receipt:
        output["execution"] = {"utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
                               "runtime": "Python " + platform.python_version(), "platform": platform.system(),
                               "script_sha256": hashlib.sha256(pathlib.Path(__file__).read_bytes()).hexdigest(),
                               "command": ["python", "<package>/scripts/course-exercises/cyb_governed_loops.py", "--json", "--receipt", "<package>/evidence/group_governed_loops.json"],
                               "arbitrary_cwd": pathlib.Path.cwd().resolve() != pathlib.Path(__file__).parent.resolve(),
                               "exit_code": 0 if output["passed"] else 1}
        args.receipt.parent.mkdir(parents=True, exist_ok=True)
        args.receipt.write_text(json.dumps(output, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    if args.json:
        print(json.dumps(output, indent=2, allow_nan=False))
    else:
        for r in results:
            print(r["module"], r["test_id"], "PASS" if r["passed"] else "FAIL")
    return 0 if output["passed"] else 1


if __name__ == "__main__":
    sys.exit(main())
