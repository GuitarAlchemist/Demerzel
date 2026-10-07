---
module_id: cyb-017-local-versus-global-stability
department: cybernetics
course: "Operational Stability and Its Tested Boundary"
level: intermediate
prerequisites: [cyb-002-active-dampening-cross-repo-oscillation]
estimated_duration: "40 minutes"
produced_by: codex-local-authoring
research_cycle: null
pipeline_id: streeling-cyb-20261007
version: "1.0.0"
status: local_draft
---

# CYB-017: Local Versus Global Stability

> **Department of Cybernetics** | Intermediate | 40 minutes | Provisional integration candidate; English draft, review and translations pending

## Objectives

- Specify the state, observation interval and acceptable region of a control claim.
- Compute a trajectory that converges locally and a counterexample outside its tested region.
- Separate mathematical stability from operational completion and finite test coverage.
- Reject an unsupported global claim using a boundary experiment and an independently checked result.

## 1. Say what is becoming stable

A controller can settle a queue length, an error signal or the number of contradictory proposals. These are different states. A dashboard that stops changing may also have lost its sensor. Choose a state variable before calling a workflow stable. In this synthetic lesson, x is a signed, dimensionless deviation from a desired operating point, sampled once per tick. Zero is the target. The model contains no wall-clock timing, production repository, network or human judgment.

Use a precise discrete map: when |x| is at most 1, the next deviation is 0.5x; outside that interval it is 1.2x. Small errors shrink, while sufficiently large errors grow. At x=0.2, the first four values are 0.2, 0.1, 0.05, 0.025. At x=2, they are 2, 2.4, 2.88, 3.456. The same controller description therefore supports two different trajectories. A stable-looking demonstration from one start cannot license all starts.

### Practice exercise and correction

An observer reports “three ticks improved.” What information is missing? **Correction:** the state definition, initial condition, map or action rule, sample interval and acceptance bound. Improvement might describe a decreasing absolute deviation, but without these details it says nothing about another initial condition or the desired end state.

## 2. A local guarantee has a domain

For our inner interval, |x_next|=0.5|x|. If |x_0|≤1, every next value stays inside that interval and |x_k|=0.5^k|x_0|. This is an algebraic guarantee for this exact map and domain, not an inference from a dozen samples. The interval is invariant: a trajectory starting there never leaves under the stated rule. At the boundary x=1 the next value is 0.5, so the inequality includes that boundary. At 1.0001 the outer rule applies instead. A tiny difference in starting state changes which rule is used.

Tedrake's MIT notes distinguish local Lyapunov conditions from additional conditions supporting global conclusions. Our map is a discrete teaching counterexample; we are not applying the notes' continuous-time theorem to it. The useful connection is to state the domain of every guarantee. See [Lyapunov Analysis](https://underactuated.mit.edu/lyapunov.html).

### Practice exercise and correction

How many ticks guarantee |x_k|≤0.01 from every |x_0|≤1? **Correction:** require 0.5^k≤0.01. Six ticks give 0.015625; seven give 0.0078125. Seven suffice. A test from x=0.2 reaches the threshold sooner, so using that test alone would understate the worst-case requirement.

## 3. Distinguish convergence, safety and completion

A mathematical asymptotic claim concerns indefinitely repeated model dynamics. An operational decision often concerns a finite deadline and a hard bound. Here, a trajectory from 2 fails the operational bound |x|≤3 at tick 3. Continuing until tick 12 merely makes the failure larger. A real controller should use a predeclared stop or escalation condition rather than waiting for divergence to become visually obvious.

Conversely, reaching |x|≤0.01 does not prove that the intended work was completed. An observed agent continuation in the incident evidence yielded an acknowledgment before a durable completion artifact; independent exact-output checking followed that artifact. Those events show why a settled control signal, ACK and verified task result must remain separate. We use only this abstract ordering, without importing another collection's lesson or identifying any session.

### Practice exercise and correction

A queue reaches zero, but the requested artifact is absent. Can the task be recorded as complete? **Correction:** no. Queue stability concerns outstanding work as measured by that queue. Completion requires the specified artifact and relevant validation. The queue might have discarded work, lost visibility or measured the wrong component.

## 4. Apply the counterexample to code

From the package overlay root, run:

```powershell
python scripts/course-exercises/cyb_systems.py --json
```

The exact experiment is `local_global_boundary` in `cyb_systems.py`. Its solution function `orbit` implements the two branches, records all 13 values including the start, and uses a fixed 12-tick horizon. The positive control checks starts 0.2 and 1 become smaller than 0.001. The negative control checks whether all three starts, including 2, shrink. That global claim must be rejected. A mutant reviewer using only the successful small trajectory would approve a claim the counterexample refutes.

After inspecting the output, change a local copy of the outer multiplier to 0.8. The global-rejection check should now fail, because the counterexample no longer grows. This failure is useful: the test responds to model changes instead of always printing rejection. Do not change the shared fixture during assessment; preserve the original run and hash.

### Practice exercise and correction

What is the last value from x=2 at tick 12? **Correction:** 2×1.2^12≈17.8322008965. This demonstrates growth for that initial condition. It does not establish a bound on every conceivable operational disturbance, and floating-point rounding must not be mistaken for the mathematical model itself.

## Two-stage assessment

Record conceptual belief state and evidence separately from exercise grades. Advance to behavioral assessment only for justified True with confidence >= 0.7; never infer or invent confidence from a score. Adapt teaching for Unknown, investigate Contradictory evidence, and follow the policy's three-attempt limit and escalation requirement if comprehension remains unresolved. These are assessment instructions; no belief transition or escalation has been performed.

**Conceptual, 4 points:** identify the state and domain, derive the seven-tick bound, give an outside-domain counterexample, and explain why completion is separate from convergence. Award one point for each defensible answer; require all four before application. Record the learner's pre/post belief and uncertainty rather than assigning an invented confidence.

**Behavioral, 4 points:** run the fixture, preserve inputs and hash, show both controls, and write a bounded acceptance statement with a stop rule. Require four points and an observed action; correct prose alone does not confirm transfer. No learner assessment has been executed by this authoring run. Follow the existing policy's maximum three attempts, then escalate unresolved understanding.

## Journal, proof and synthesis

Record date, initial state, observation horizon, model version, maximum deviation, final deviation and control results. Include the failed global claim and the evidence that rejected it. Synthesize: the exact inner map has a domain-specific algebraic guarantee; the synthetic run checks its implementation and finds one outer failure. Neither result proves stability of an unmeasured fleet. MAT-024 develops fixed points, multipliers and broader mathematical analysis; this module teaches the operational claim boundary and receipt discipline rather than repeating those derivations. CYB-002 supplies dampening context; CYB-018 asks what a known disturbance does to the boundary.

## Further reading

- [Russ Tedrake, Lyapunov Analysis, MIT working course notes](https://underactuated.mit.edu/lyapunov.html), inspected 2026-10-07. Continuous-time results have their own hypotheses.
- Existing `cyb-002-active-dampening-cross-repo-oscillation` and `mat-024-dynamical-systems-stability-feedback`; preserve their original content and source IDs.

*Locally authored under streeling-cyb-20261007; no Seldon research cycle, publication or learning outcome claimed.*

## Offline Solution

[Download the offline solution and executable controls](../../../../../scripts/course-exercises/cyb_systems.py).
