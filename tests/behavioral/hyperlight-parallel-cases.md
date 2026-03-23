# Hyperlight Parallel — Behavioral Tests

Pipeline: `pipelines/hyperlight-orchestrator.ixql`
Spec: `docs/specs/hyperlight-ixql-parallel.md`
Domain: ga (Guitar Alchemist — massively parallel parameter sweep)
Issue: #171

## Test Cases

### TC-HL-01: N=100 VMs execute independently with no cross-VM state

**Given:** A sweep configuration with n_samples=100, grid strategy, and parameter ranges for brightness (0.0-1.0), decay (0.001-0.02), dispersion (0.0-2.0), reverb_mix (0.0-0.3)
**When:** Step 3 fan_out dispatches 100 Hyperlight micro-VMs
**Then:** All 100 VMs receive distinct parameter sets; no two VMs share memory or state; each VM loads its own WASM module independently; each VM returns a score without reading any other VM's output; the coordinator receives exactly 100 result objects (assuming no failures)
**Verify:** Amdahl's Law parallel fraction (~95%) is correctly isolated — VMs have zero cross-dependencies. Article 9 (Bounded Autonomy) — each VM operates within its sandbox with no network, no filesystem, and no cross-VM communication.

### TC-HL-02: Failed VMs are excluded without corrupting results

**Given:** A sweep of N=100 VMs where 5 VMs exceed the 5000ms timeout (e.g., due to adversarial parameter combinations causing long render times)
**When:** The coordinator collects results in Step 4
**Then:** 95 successful results are ranked and selected from; the 5 failed VMs are logged with their failure reason and excluded from ranking; a tars.classify signal fires with severity "low" (since 5/100 = 5% < 10% threshold); the best parameter set is selected from the 95 successful results only
**Verify:** Article 3 (Reversibility) — failed VMs have no side effects. Article 7 (Auditability) — failures are logged. The system degrades gracefully rather than failing entirely.

### TC-HL-03: Convergence narrows sweep range and terminates

**Given:** Iteration 1 produces best_score=0.72 with brightness=0.6. Iteration 2 with narrowed ranges (brightness 0.44-0.76) produces best_score=0.88. Iteration 3 with further narrowed ranges produces best_score=0.91.
**When:** The governance gate in Step 6a evaluates best_score=0.91 against threshold 0.9
**Then:** Pipeline stops with message "Hyperlight sweep converged: score=0.91 after 3 iterations"; sweep history contains 3 entries showing monotonic score improvement; parameter ranges narrow by 60% per iteration (±20% around best); final parameters are written to previous-best.json
**Verify:** Article 9 (Bounded Autonomy) — optimizer stops at the good-enough threshold rather than consuming unbounded resources. The narrowing strategy (±20% around best) correctly zooms in on the optimal region.

### TC-HL-04: Stall detection escalates after 3 consecutive low-improvement sweeps

**Given:** Three consecutive iterations where improvement < 0.005 each (e.g., scores 0.83, 0.833, 0.835)
**When:** Step 6b evaluates stall_count=3
**Then:** Discord alert fires with current best score and suggestion to expand parameter ranges or change strategy; escalation fires per Article 6 (Escalation); the pipeline does not loop indefinitely; stall_count is persisted in iteration-counter.json so it survives across pipeline invocations
**Verify:** Article 6 (Escalation) — the system recognizes when it cannot make progress and asks for human guidance rather than wasting compute. The stall counter correctly resets to 0 when a meaningful improvement (>= 0.005) is found.
