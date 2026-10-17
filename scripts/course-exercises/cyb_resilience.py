"""Synthetic, deterministic Cybernetics exercises CYB-013..016; stdlib only.

Run from any cwd: python <absolute-path>/cyb_resilience.py --json
No service calls, files modified, threads, sleeps, or actual agent control.
"""
import argparse
import hashlib
import json
import platform
from datetime import datetime, timezone
from pathlib import Path


class Breaker:
    """Serialized consecutive-failure policy with one logical probe."""
    def __init__(self, threshold=2, cooldown=3):
        self.threshold, self.cooldown = threshold, cooldown
        self.state, self.failures, self.until = "closed", 0, None
        self.probe_inflight = False

    def allow(self, tick):
        if self.state == "open":
            if tick < self.until:
                return False
            self.state = "half_open"
        if self.state == "half_open":
            if self.probe_inflight:
                return False
            self.probe_inflight = True
        return True

    def record(self, tick, success):
        if self.state == "half_open":
            if not self.probe_inflight:
                raise ValueError("no admitted probe")
            self.probe_inflight = False
            if success:
                self.state, self.failures, self.until = "closed", 0, None
            else:
                self.state, self.until = "open", tick + self.cooldown
            return
        if self.state != "closed":
            raise ValueError("record for suppressed request")
        self.failures = 0 if success else self.failures + 1
        if self.failures >= self.threshold:
            self.state, self.until = "open", tick + self.cooldown


def breaker_test():
    breaker = Breaker()
    outcomes = [(0, False), (1, False), (2, True), (3, True),
                (4, False), (5, True), (7, True), (8, True)]
    trace = []
    for tick, success in outcomes:
        admitted = breaker.allow(tick)
        if admitted:
            breaker.record(tick, success)
        trace.append([tick, admitted, breaker.state])
    expected = [[0, True, "closed"], [1, True, "open"],
                [2, False, "open"], [3, False, "open"],
                [4, True, "open"], [5, False, "open"],
                [7, True, "closed"], [8, True, "closed"]]
    probe = Breaker()
    for tick in (0, 1):
        assert probe.allow(tick)
        probe.record(tick, False)
    first, second = probe.allow(4), probe.allow(4)
    reset = Breaker()
    for tick, success in [(0, False), (1, True), (2, False)]:
        assert reset.allow(tick)
        reset.record(tick, success)
    # Execute mutant: timer expiry closes directly, removing the probe budget.
    class TimerClosesMutant(Breaker):
        def allow(self, tick):
            if self.state == "open" and tick >= self.until:
                self.state, self.failures = "closed", 0
            return super().allow(tick)

    mutant = TimerClosesMutant()
    for tick in (0, 1):
        assert mutant.allow(tick)
        mutant.record(tick, False)
    mutant_admitted_at_4 = sum(mutant.allow(4) for _ in range(5))
    assert trace == expected and (first, second) == (True, False)
    assert reset.state == "closed" and reset.failures == 1
    assert mutant_admitted_at_4 == 5
    return {"module": "CYB-013", "test_id": "breaker_probe_budget",
            "inputs": {"threshold": 2, "cooldown_ticks": 3, "outcomes": outcomes},
            "expected": expected, "actual": trace,
            "positive_control": {"success_resets_counter": True,
                                 "only_one_probe_admitted": [first, second]},
            "negative_control_rejected": mutant_admitted_at_4 > int(first),
            "negative_control": {"mutant": "timer_closes_without_probe", "calls_at_tick_4": 5}}


def queue_trace(arrivals, service, capacity=None):
    queued = completed = rejected = 0
    trace = []
    for tick, incoming in enumerate(arrivals):
        accepted = incoming if capacity is None else min(incoming, capacity - queued)
        rejected += incoming - accepted
        before_service = queued + accepted
        served = min(before_service, service)
        queued, completed = before_service - served, completed + served
        assert sum(arrivals[:tick + 1]) == completed + queued + rejected
        trace.append({"tick": tick, "incoming": incoming, "accepted": accepted,
                      "before_service": before_service, "served": served,
                      "queued": queued, "rejected_total": rejected})
    return trace, completed, rejected


def queue_test():
    arrivals = [3, 3, 3, 0, 0]
    trace, completed, rejected = queue_trace(arrivals, 2, 4)
    actual = {"queue_after_service": [r["queued"] for r in trace],
              "completed": completed, "rejected": rejected,
              "peak_before_service": max(r["before_service"] for r in trace)}
    expected = {"queue_after_service": [1, 2, 2, 0, 0], "completed": 8,
                "rejected": 1, "peak_before_service": 4}
    unbounded, _, _ = queue_trace(arrivals, 2)
    stable, stable_completed, stable_rejected = queue_trace([2] * 5, 2, 4)
    # Mutant clipping hides the rejected item rather than accounting for it.
    mutant_total = completed + trace[-1]["queued"]
    assert actual == expected
    assert all(r["queued"] == 0 for r in stable) and stable_completed == 10
    assert stable_rejected == 0
    assert max(r["before_service"] for r in unbounded) == 5
    return {"module": "CYB-014", "test_id": "queue_conservation_and_admission",
            "inputs": {"arrivals": arrivals, "service_per_tick": 2, "capacity": 4,
                       "ordering": "admit_then_serve"}, "expected": expected,
            "actual": actual, "trace": trace,
            "positive_control": {"balanced_arrivals_complete": stable_completed,
                                 "rejected": stable_rejected},
            "negative_control_rejected": mutant_total != sum(arrivals),
            "negative_control": {"mutant": "silent_drop_accounting", "claimed_total": mutant_total,
                                 "incoming_total": sum(arrivals),
                                 "unbounded_peak": 5}}


class Ledger:
    """Single-process atomic boundary: receipt and effect become visible together.

    This models an atomic storage contract; it does NOT implement durable storage.
    """
    def __init__(self):
        self.receipts = {}
        self.effects = 0

    def execute(self, key, payload, lose_reply=False):
        if key in self.receipts:
            original, result = self.receipts[key]
            if original != payload:
                raise ValueError("same key, changed intent")
        else:
            self.effects += 1
            result = {"artifact": "synthetic-result", "effect_number": self.effects}
            self.receipts[key] = (payload, result)
        if lose_reply:
            raise TimeoutError("reply lost after modeled commit")
        return result


def recovery_test():
    ledger = Ledger()
    try:
        ledger.execute("logical-17", {"amount": 10}, lose_reply=True)
        raise AssertionError("timeout was not injected")
    except TimeoutError:
        pass
    observed = ledger.receipts["logical-17"][1]
    replayed = ledger.execute("logical-17", {"amount": 10})
    changed_intent_rejected = False
    try:
        ledger.execute("logical-17", {"amount": 11})
    except ValueError:
        changed_intent_rejected = True
    mutant = Ledger()
    try:
        mutant.execute("attempt-1", {"amount": 10}, lose_reply=True)
    except TimeoutError:
        pass
    mutant.execute("attempt-2", {"amount": 10})
    actual = {"effects": ledger.effects, "recovered_equals_replayed": observed == replayed,
              "changed_intent_rejected": changed_intent_rejected}
    expected = {"effects": 1, "recovered_equals_replayed": True, "changed_intent_rejected": True}
    assert actual == expected and mutant.effects == 2
    return {"module": "CYB-015", "test_id": "lost_reply_same_logical_key",
            "inputs": {"logical_key": "logical-17", "payload": {"amount": 10},
                       "failure_point": "after_atomic_commit_before_reply"},
            "expected": expected, "actual": actual,
            "positive_control": {"same_key_returns_existing_result": observed == replayed},
            "negative_control_rejected": mutant.effects != 1,
            "negative_control": {"mutant": "new_key_for_each_attempt", "effects": mutant.effects}}


PLACES = ("ready", "running", "done", "free")
NET = {"start": ((1, 0, 0, 1), (0, 1, 0, 0)),
       "finish": ((0, 1, 0, 0), (0, 0, 1, 1))}


def fire(marking, transition):
    pre, post = NET[transition]
    if any(value < needed for value, needed in zip(marking, pre)):
        raise ValueError("transition not enabled")
    return tuple(value - needed + added for value, needed, added in zip(marking, pre, post))


def observed_step(before, name, after):
    try:
        return fire(before, name) == after
    except ValueError:
        return False


def petri_test():
    initial = (1, 0, 0, 1)
    running = fire(initial, "start")
    done = fire(running, "finish")
    trace = [initial, running, done]
    expected = [(1, 0, 0, 1), (0, 1, 0, 0), (0, 0, 1, 1)]
    valid = observed_step(initial, "start", running) and observed_step(running, "finish", done)
    skip_rejected = not observed_step(initial, "finish", done)
    wrong_after = (0, 0, 1, 0)  # Mutant forgets to release the capacity token.
    missing_release_rejected = not observed_step(running, "finish", wrong_after)
    assert all(m[0] + m[1] + m[2] == 1 and m[1] + m[3] == 1 for m in trace)
    # Two proposals share version 0. Only one may commit its token consumption.
    version, committed = 0, 0
    for expected_version in (0, 0):
        if expected_version == version:
            version, committed = version + 1, committed + 1
    assert trace == expected and valid and skip_rejected and missing_release_rejected
    assert committed == 1
    return {"module": "CYB-016", "test_id": "observed_firing_with_resource_token",
            "inputs": {"places": PLACES, "initial": initial, "net": NET},
            "expected": expected, "actual": trace,
            "positive_control": {"valid_observed_trace": valid, "stale_proposals_committed": committed},
            "negative_control_rejected": skip_rejected and missing_release_rejected,
            "negative_control": {"finish_without_start_rejected": skip_rejected,
                                 "missing_release_rejected": missing_release_rejected,
                                 "wrong_after": wrong_after}}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    records = [breaker_test(), queue_test(), recovery_test(), petri_test()]
    receipt = {"schema": "streeling.course-exercise/1", "group": "resilience",
               "utc": datetime.now(timezone.utc).isoformat(),
               "runtime": platform.python_version(), "synthetic": True,
               "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
               "command": "python scripts/course-exercises/cyb_resilience.py --json",
               "outcome": "pass", "records": records}
    print(json.dumps(receipt, indent=2) if args.json else "PASS CYB-013..016 (four synthetic controls)")


if __name__ == "__main__":
    main()
