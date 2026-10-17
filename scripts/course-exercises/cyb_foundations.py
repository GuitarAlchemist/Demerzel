"""Synthetic CYB-004..008 exercises. Stdlib only, no live interfaces or writes."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import math
from pathlib import Path
import platform


def scalar_loop(gain, steps=10, disturbances=None, open_loop=False):
    """x[k+1]=x[k]+u[k]+d[k]; a unit-gain discrete integrator."""
    disturbances = disturbances or {}
    state, planned = 0.0, 0.0
    trace = [state]
    for tick in range(steps):
        measured = planned if open_loop else state
        control = gain * (10.0 - measured)
        state += control + disturbances.get(tick, 0.0)
        planned += control
        trace.append(state)
    return trace


def contract_error(measurement, target, now=100, max_age=5):
    """Validate scope/phase/unit/time BEFORE arithmetic, then compute target-y."""
    for key in ("scope", "phase", "unit"):
        if measurement[key] != target[key]:
            raise ValueError("incompatible " + key)
    if not (0 <= now - measurement["observed_at"] <= max_age):
        raise ValueError("stale or future sample")
    if not math.isfinite(measurement["value"]):
        raise ValueError("nonfinite sample")
    return target["value"] - measurement["value"]


def delayed_loop(gain, delay, steps=60):
    """Known zero history; measurement y[k]=x[k-delay], not x[k]."""
    state = [0.0]
    for tick in range(steps):
        measured = state[tick - delay] if tick >= delay else 0.0
        state.append(state[-1] + gain * (1.0 - measured))
    return state


def relay(values, high=6, low=2, initial=False, reset_each_tick=False):
    """Inclusive thresholds are this fixture's explicit contract."""
    if not low < high:
        raise ValueError("require low < high")
    active, states = initial, []
    for value in values:
        if reset_each_tick:
            active = False
        if not active and value >= high:
            active = True
        elif active and value <= low:
            active = False
        states.append(active)
    return states


def deadband_action(error, width=2, emergency=False):
    """Teaching gate: pass full error outside the band; emergency bypass."""
    if width < 0:
        raise ValueError("negative width")
    if emergency:
        return "escalate"
    return 0 if abs(error) <= width else error


def switches(states, initial=False):
    previous, count = initial, 0
    for state in states:
        count += state != previous
        previous = state
    return count


def experiments():
    records = []
    closed = scalar_loop(.5, disturbances={4: -4.0})
    opened = scalar_loop(.5, disturbances={4: -4.0}, open_loop=True)
    nominal = scalar_loop(.5)
    wrong_sign = scalar_loop(-.5, disturbances={4: -4.0})
    expected = {"closed_final": 9.865234375, "open_final": 5.990234375,
                "nominal_final": 9.990234375}
    actual = {"closed_final": closed[-1], "open_final": opened[-1],
              "nominal_final": nominal[-1]}
    records.append(dict(module="CYB-004", test_id="loop-disturbance",
        inputs={"target": 10, "gain": .5, "steps": 10, "disturbance": {"4": -4}},
        expected=expected, actual=actual,
        traces={"closed": closed, "open": opened, "wrong_sign": wrong_sign},
        positive_control=actual == expected,
        negative_control_rejected=abs(10-wrong_sign[-1]) > 10,
        criterion="exact traces plus wrong-sign error exceeds initial error"))

    target = dict(scope="cybernetics", phase="authored_validated", unit="courses", value=25)
    sample = dict(scope="cybernetics", phase="authored_validated", unit="courses",
                  value=3, observed_at=98)
    rejected = []
    for key, value in [("scope", "guitar-studies"), ("phase", "catalog_positions"),
                       ("unit", "milliseconds"), ("observed_at", 90),
                       ("observed_at", 101), ("value", float("nan"))]:
        try:
            contract_error(dict(sample, **{key: value}), target)
        except ValueError:
            rejected.append(key + ":" + str(value))
    catalog = dict(sample, phase="catalog_positions", value=575)
    naive_error = target["value"] - catalog["value"]
    records.append(dict(module="CYB-005", test_id="signal-contract",
        inputs={"target": target, "sample": sample, "now": 100, "max_age": 5},
        expected={"error": 22, "rejections": 6},
        actual={"error": contract_error(sample, target), "rejections": len(rejected)},
        rejected_cases=rejected, mutant_catalog_error=naive_error,
        positive_control=contract_error(sample, target) == 22,
        negative_control_rejected=len(rejected) == 6 and naive_error == -550,
        criterion="reject incompatible observations before arithmetic"))

    immediate = delayed_loop(.8, 0)
    delayed = delayed_loop(.8, 2)
    cautious = delayed_loop(.2, 2)
    actual = {"immediate_error": abs(1-immediate[-1]),
              "delayed_error": abs(1-delayed[-1]),
              "cautious_error": abs(1-cautious[-1]),
              "full_delay_ms": 400, "observation_age_ms": 300}
    records.append(dict(module="CYB-006", test_id="delay-gain-counterexample",
        inputs={"target": 1, "steps": 60, "delays": [0, 2], "gains": [.8, .2],
                "timeline_ms": {"command": 0, "observed": 100, "received": 400}},
        expected={"immediate_error_below": .001, "cautious_error_below": .001,
                  "delayed_error_above": 1, "full_delay_ms": 400}, actual=actual,
        traces={"immediate_first_9": immediate[:9], "delayed_first_9": delayed[:9],
                "cautious_first_9": cautious[:9]},
        positive_control=actual["immediate_error"] < .001 and actual["cautious_error"] < .001,
        negative_control_rejected=actual["delayed_error"] > 1,
        criterion="same gain failing under delay is a bounded counterexample, not a general tuning rule"))

    values = [1, 5, 6, 5, 6, 5, 2, 3, 6, 2]
    expected = [False, False, True, True, True, True, False, False, True, False]
    states = relay(values)
    mutant = relay(values, reset_each_tick=True)
    invalid_rejected = False
    try:
        relay(values, high=2, low=6)
    except ValueError:
        invalid_rejected = True
    records.append(dict(module="CYB-007", test_id="hysteresis-memory",
        inputs={"values": values, "high": 6, "low": 2, "initial": False},
        expected={"states": expected, "switches": 4},
        actual={"states": states, "switches": switches(states)},
        mutant={"states": mutant, "switches": switches(mutant)},
        same_input_different_history={"off_then_4": relay([4], initial=False),
                                      "on_then_4": relay([4], initial=True)},
        positive_control=states == expected and switches(states) == 4,
        negative_control_rejected=mutant != expected and switches(mutant) == 6 and invalid_rejected,
        criterion="memory retained between samples; invalid threshold order rejected"))

    noise = [-2, 2, -1, 1, 0]
    residuals = noise + [3, -3, 6]
    action = [deadband_action(e) for e in residuals]
    expected = [0, 0, 0, 0, 0, 3, -3, 6]
    zero_width = [deadband_action(e, width=0) for e in noise]
    hidden_fault = deadband_action(6, width=10)
    bypass = deadband_action(1, width=2, emergency=True)
    records.append(dict(module="CYB-008", test_id="deadband-budget",
        inputs={"error_ms": residuals, "width_ms": 2, "allowed_residual_ms": 5},
        expected={"actions": expected, "emergency": "escalate"},
        actual={"actions": action, "emergency": bypass},
        mutants={"zero_width_noise_actions": zero_width, "width_10_fault_action": hidden_fault},
        positive_control=action == expected and bypass == "escalate",
        negative_control_rejected=sum(a != 0 for a in zero_width) == 4 and hidden_fault == 0,
        criterion="quiet noise plus visible out-of-budget fault, emergency bypass preserved"))
    return records


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    results = experiments()
    passed = all(r["positive_control"] and r["negative_control_rejected"] for r in results)
    receipt = dict(schema="streeling.synthetic-course-experiments/1", group="foundations",
        utc=datetime.now(timezone.utc).isoformat(), runtime=platform.python_version(),
        platform=platform.system(), source_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        command="python <package>/scripts/course-exercises/cyb_foundations.py --json",
        synthetic=True, live_calls=0, outcome="passed" if passed else "failed", records=results)
    print(json.dumps(receipt, indent=2, allow_nan=False) if args.json else
          "foundations: " + receipt["outcome"] + " (5 experiments, positive and mutant controls)")
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
