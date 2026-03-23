# Hyperlight Massively Parallel IxQL Scenario Testing

**Version:** 1.0.0
**Date:** 2026-03-22
**Consumer:** `pipelines/hyperlight-orchestrator.ixql`, `pipelines/spectral-optimizer.ixql`
**Depends on:** Hyperlight micro-VM runtime, ix WASM guitar engine, spectral critic
**Issue:** #171

## Overview

This specification defines how IxQL `fan_out` stages map to Hyperlight micro-VMs for
massively parallel parameter sweep execution. Instead of running 8 perturbations sequentially
(or with limited fan_out concurrency), we spawn N=100+ Hyperlight micro-VMs, each executing
one parameter combination in complete isolation. The coordinator collects scores, selects the
best, and optionally narrows the sweep for a subsequent iteration.

The first consumer is `spectral-optimizer.ixql`, which currently fans out 8 perturbation
branches. With Hyperlight, the same pipeline can evaluate 100+ parameter combinations per
iteration, transforming gradient-free hill climbing into a broad grid search with convergence
in fewer iterations.

## Architecture

```
                         +---------------------+
                         |   IxQL Coordinator   |
                         |  (hyperlight-orch.)  |
                         +----------+----------+
                                    |
                    define sweep space + partition
                                    |
                  +-----------------+-----------------+
                  |                 |                 |
           +------+------+  +------+------+   +------+------+
           | Hyperlight  |  | Hyperlight  |   | Hyperlight  |
           |  VM #1      |  |  VM #2      |   |  VM #N      |
           |             |  |             |   |             |
           | WASM engine |  | WASM engine |   | WASM engine |
           | render      |  | render      |   | render      |
           | score       |  | score       |   | score       |
           | return      |  | return      |   | return      |
           +------+------+  +------+------+   +------+------+
                  |                 |                 |
                  +-----------------+-----------------+
                                    |
                         collect + select best
                                    |
                         converged? → stop
                         not converged? → narrow + repeat
```

### VM Lifecycle

Each Hyperlight micro-VM follows a strict lifecycle:

1. **Spawn** (~34ms) -- Hyperlight creates an isolated micro-VM
2. **Load** -- WASM guitar engine module is loaded into the VM
3. **Configure** -- Parameter set is injected (read-only input)
4. **Execute** -- Render audio, compute spectral features, score against reference
5. **Return** -- Score + metadata written to output channel
6. **Die** -- VM is destroyed; no state persists

### Coordinator Responsibilities

The IxQL coordinator (running outside Hyperlight) handles:

- **Sweep definition:** Generate the N parameter combinations from a defined grid or random sample
- **Partitioning:** Assign one parameter set per VM (1:1 mapping, no work sharing)
- **Dispatch:** Spawn N VMs simultaneously via Hyperlight API
- **Collection:** Wait for all N results (with timeout per VM)
- **Selection:** Rank results by realism score, select best
- **Convergence check:** If best score >= threshold or improvement < epsilon, stop
- **Narrowing:** If not converged, shrink the parameter range around the best result and repeat

## Amdahl's Law Analysis

### Current State (spectral-optimizer.ixql)

The existing pipeline has a **serial fraction of ~60%:**

| Phase | Steps | Nature | Time (relative) |
|-------|-------|--------|-----------------|
| Load reference + params | 1-2 | Serial | 5% |
| Initial render + score | 3-5 | Serial | 25% |
| Perturbation fan_out | 6-7 | Parallel (N=8) | 40% |
| Select + gate + write | 8-12 | Serial | 30% |

```
Current speedup (N=8): S = 1 / (0.60 + 0.40/8) = 1 / 0.65 = 1.54x
```

### With Hyperlight (this design)

Hyperlight restructures the pipeline to minimize serial work:

| Phase | Nature | Time (relative) |
|-------|--------|-----------------|
| Define sweep space | Serial | 1% |
| Partition workloads | Serial | 1% |
| Spawn + execute N VMs | Parallel (N=100) | 95% |
| Collect + select best | Serial | 2% |
| Convergence check + write | Serial | 1% |

The serial fraction drops to **~5%** because:
- Reference loading happens once (amortized across iterations)
- Each VM does its own render + analyze + score (no serial scoring bottleneck)
- Selection is O(N) -- trivial compared to rendering

```
Hyperlight speedup (N=100): S = 1 / (0.05 + 0.95/100) = 1 / 0.0595 = 16.8x
Hyperlight speedup (N=1000): S = 1 / (0.05 + 0.95/1000) = 1 / 0.05095 = 19.6x
```

**Theoretical maximum:** 1 / 0.05 = **20x** (as N approaches infinity).

With N=100, we achieve **16.8x speedup** -- 84% of theoretical maximum. Diminishing
returns set in beyond N=100, making it the practical sweet spot.

### Convergence Benefit

Beyond raw speedup per iteration, broader sweeps mean fewer iterations to converge.
The current 8-perturbation hill climber needs ~20 iterations to reach score 0.9.
With 100 parallel evaluations covering a wider parameter space, convergence is
expected in ~5 iterations -- a combined 4x iteration reduction on top of the per-iteration
speedup.

## Security Model

Each Hyperlight micro-VM provides hardware-level isolation:

| Property | Guarantee |
|----------|-----------|
| Memory isolation | Each VM has its own address space; no shared memory between VMs |
| No cross-VM state | VM is destroyed after returning results; no residual state |
| Read-only input | Parameter set is injected as immutable configuration |
| Write-only output | VM can only write to its designated output channel |
| No network access | VMs cannot make network calls; all data is pre-loaded |
| Timeout enforcement | Each VM has a hard timeout; hung VMs are killed |
| No filesystem access | WASM module and reference data are loaded into VM memory at spawn |

This model satisfies **Article 3** (Reversibility) -- a failed VM has no side effects.
It satisfies **Article 9** (Bounded Autonomy) -- each VM operates within strictly
predefined bounds with no ability to exceed its scope.

## Cost Model

### Per-VM Costs

| Phase | Time |
|-------|------|
| Hyperlight VM spawn | ~34ms |
| WASM module load | ~10ms |
| Audio render (2000ms, 44.1kHz) | ~150ms |
| Spectral analysis (STFT) | ~20ms |
| Scoring | ~1ms |
| Result return + teardown | ~5ms |
| **Total per VM** | **~220ms** |

### Sequential vs Parallel

| Approach | N | Wall-clock time per iteration |
|----------|---|-------------------------------|
| Sequential | 8 | 8 x 220ms = 1,760ms |
| Sequential | 100 | 100 x 220ms = 22,000ms |
| Hyperlight parallel | 100 | 34ms spawn + 220ms execute + 10ms collect = ~264ms |

**Result:** 100 parameter evaluations in ~264ms wall-clock (vs 22 seconds sequential).
This is a **~83x** throughput improvement at N=100.

### Resource Constraints

- **Memory:** Each WASM VM requires ~16MB. N=100 VMs = ~1.6GB concurrent memory.
- **CPU cores:** Hyperlight schedules across available cores. Recommended: >= 16 cores
  for N=100 to avoid excessive context switching.
- **Recommended ceiling:** N=256 on a 32-core machine with 8GB available.

## Integration with spectral-optimizer.ixql

The `hyperlight-orchestrator.ixql` pipeline replaces Steps 3-8 of `spectral-optimizer.ixql`:

| spectral-optimizer Step | Hyperlight equivalent |
|-------------------------|----------------------|
| Step 3 (Render) | Absorbed into per-VM execution |
| Step 4 (Spectral analyze) | Absorbed into per-VM execution |
| Step 5 (Score) | Absorbed into per-VM execution |
| Step 6 (fan_out 8 perturbations) | Replaced by fan_out N=100 VMs |
| Step 7 (Re-score) | Absorbed into per-VM execution |
| Step 8 (Select best) | Coordinator collects + ranks |

Steps 1-2 (load reference/params), 9-12 (governance gate, stall detection, write, compound)
remain unchanged and execute in the coordinator.

## Future Extensions

- **Adaptive N:** Start with N=100 in early iterations (broad search), reduce to N=20
  in later iterations (fine-tuning) to save resources.
- **Multi-instrument:** Partition VMs across multiple instruments in a single sweep.
- **Hyperparameter meta-optimization:** Use Hyperlight to sweep optimizer hyperparameters
  (perturbation step sizes, scoring weights) in addition to synthesis parameters.
- **Cross-pipeline reuse:** Any IxQL pipeline with a fan_out stage can be upgraded to
  Hyperlight dispatch by wrapping the fan_out body in a WASM module.
