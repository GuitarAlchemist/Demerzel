"""Synthetic CYB-017..020 teaching fixtures. Stdlib; no external effects."""
import argparse
import json
import sys


def orbit(start, steps=12):
    values = [start]
    for _ in range(steps):
        x = values[-1]
        values.append(0.5 * x if abs(x) <= 1 else 1.2 * x)
    return values


def backlog(arrivals, forecast=None, cap=8):
    q = 0
    trace = []
    for t, arrival in enumerate(arrivals):
        service = min(cap, forecast[t]) if forecast is not None else (8 if q > 0 else 4)
        q = max(0, q + arrival - service)
        trace.append({"tick": t, "arrival": arrival, "service": service, "queue": q})
    return trace


def propagate(graph, root, generation, deduplicate, limit=12):
    pending = [(root, generation)]
    seen = set()
    applied = []
    while pending and len(applied) < limit:
        repo, gen = pending.pop(0)
        key = (repo, gen)
        if deduplicate and key in seen:
            continue
        seen.add(key)
        applied.append(key)
        pending.extend((dependent, gen) for dependent in graph.get(repo, []))
    return {"applied": applied, "pending": pending, "bounded": not pending}


def validate_tree(parent, children):
    if parent < 0 or any(x < 0 for x in children) or sum(children) > parent:
        raise ValueError("children exceed nonnegative parent envelope")
    return list(children)


def admit_lease(epoch, grant_epoch, cap, spent, request):
    if grant_epoch != epoch or request < 0 or spent + request > cap:
        return False
    return True


def experiments():
    records = []
    small, boundary, large = orbit(0.2), orbit(1), orbit(2)
    records.append({"module_id": "CYB-017", "test_id": "local_global_boundary",
        "inputs": {"starts": [0.2, 1, 2], "steps": 12, "local_multiplier": 0.5, "outer_multiplier": 1.2},
        "expected": {"small_shrinks": True, "boundary_shrinks": True, "global_claim_rejected": True},
        "actual": {"small": small, "boundary": boundary, "large": large},
        "positive_control": abs(small[-1]) < 0.001 and abs(boundary[-1]) < 0.001,
        "negative_control_rejected": not all(abs(orbit(x)[-1]) < abs(x) for x in [0.2, 1, 2])})
    arrivals = [4, 4, 8, 8, 4, 4]
    planned = backlog(arrivals, arrivals)
    reactive = backlog(arrivals)
    bad_forecast = backlog(arrivals, [4] * 6)
    capped = backlog(arrivals, arrivals, cap=6)
    peak = lambda trace: max(x["queue"] for x in trace)
    records.append({"module_id": "CYB-018", "test_id": "known_disturbance_forecast",
        "inputs": {"arrivals": arrivals, "forecast": arrivals, "cap": 8},
        "expected": {"planned_peak": 0, "reactive_peak": 4, "wrong_forecast_peak": 8, "cap6_peak": 4},
        "actual": {"planned": planned, "reactive": reactive, "wrong_forecast": bad_forecast, "cap6": capped},
        "positive_control": peak(planned) == 0 and peak(reactive) == 4,
        "negative_control_rejected": peak(bad_forecast) != 0 and peak(capped) != 0})
    graph = {"A": ["B"], "B": ["A"]}
    bounded = propagate(graph, "A", "g1", True)
    mutant = propagate(graph, "A", "g1", False)
    new_generation = propagate(graph, "A", "g2", True)
    acyclic = propagate({"A": ["B"], "B": ["C"]}, "A", "g1", False)
    records.append({"module_id": "CYB-019", "test_id": "cross_repo_generation_cycle",
        "inputs": {"graph": graph, "generation": "g1", "inspection_limit": 12},
        "expected": {"bounded_applications": 2, "mutant_unbounded": True, "new_generation_applies": 2, "acyclic_applications": 3},
        "actual": {"bounded": bounded, "mutant": mutant, "new_generation": new_generation, "acyclic": acyclic},
        "positive_control": bounded["bounded"] and len(bounded["applied"]) == 2 and acyclic["bounded"] and len(acyclic["applied"]) == 3 and len(new_generation["applied"]) == 2,
        "negative_control_rejected": not mutant["bounded"] and len(mutant["applied"]) == 12})
    branches = validate_tree(10, [4, 6])
    leaves = validate_tree(branches[0], [2, 2]) + validate_tree(branches[1], [3, 3])
    demands = [3, 3, 5, 2]
    served = [min(cap, demand) for cap, demand in zip(leaves, demands)]
    rejects = []
    for parent, children in [(10, [6, 6]), (4, [3, 3]), (10, [-1, 5])]:
        try:
            validate_tree(parent, children)
            rejects.append(False)
        except ValueError:
            rejects.append(True)
    records.append({"module_id": "CYB-020", "test_id": "recursive_envelope_lease",
        "inputs": {"root_cap": 10, "branch_caps": branches, "leaf_caps": leaves, "demands": demands, "epoch": 7},
        "expected": {"served": [2, 2, 3, 2], "total": 9, "bad_allocations_rejected": 3, "stale_lease_rejected": True},
        "actual": {"served": served, "total": sum(served), "bad_allocations_rejected": sum(rejects), "naive_leaf_total": 24},
        "positive_control": sum(served) == 9 and sum(leaves) == 10 and admit_lease(7, 7, 3, 1, 2),
        "negative_control_rejected": all(rejects) and not admit_lease(7, 6, 3, 0, 1) and not admit_lease(7, 7, 3, 2, 2)})
    return records


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    records = experiments()
    passed = all(r["positive_control"] and r["negative_control_rejected"] for r in records)
    result = {"synthetic": True, "passed": passed, "experiments": records}
    print(json.dumps(result, indent=2) if args.json else f"CYB systems: {len(records)} experiments, passed={passed}")
    return 0 if passed else 1


if __name__ == "__main__":
    sys.exit(main())
