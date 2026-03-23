# Governance Markov Simulation Specification

**Version:** 1.0.0
**Date:** 2026-03-22
**Consumer:** `pipelines/governance-markov.ixql`, `state/markov/`
**Depends on:** `ix/crates/memristive-markov`, `policies/anti-lolli-inflation-policy.yaml`

## Overview

This specification defines how the memristive Markov model from ix (`crates/memristive-markov`)
connects to Demerzel's governance state to predict governance health transitions. The memristive
layer gives the model "scar tissue" -- systems that have violated policies before find it harder
to return to healthy states, just as a memristor retains resistance history.

## State Space

The governance system occupies one of four discrete states, mapped to integer indices for the
Markov engine:

| State   | Index | Resilience (R) | LOLLI/ERGOL Ratio | Description                                           |
|---------|-------|----------------|-------------------|-------------------------------------------------------|
| Healthy | 0     | >= 0.9         | < 1.5             | ERGOL outpaces creation; no policy violations          |
| Watch   | 1     | >= 0.7         | 1.5 - 2.5         | Artifact creation accelerating; monitoring required    |
| Warning | 2     | >= 0.5         | 2.5 - 3.0         | One more bad cycle triggers freeze; pre-approval mode  |
| Freeze  | 3     | < 0.5          | > 3.0 for 3 cycles | Creation freeze active; execute-before-create enforced |

### State Classification Rules

A cycle's state is determined by the **worse** of its resilience and ratio classifications:

```
classify(R, ratio, consecutive_high_ratio_cycles):
    if R < 0.5 or (ratio > 3.0 and consecutive_high_ratio_cycles >= 3):
        return Freeze (3)
    if R < 0.7 or ratio > 2.5:
        return Warning (2)
    if R < 0.9 or ratio > 1.5:
        return Watch (1)
    return Healthy (0)
```

## Input Signals Per Cycle

Each governance cycle produces a 5-dimensional observation vector consumed by the model:

| Signal                  | Source                                      | Type    |
|-------------------------|---------------------------------------------|---------|
| ERGOL/LOLLI ratio       | `state/driver/lolli-ergol-history.json`      | float   |
| Resilience score (R)    | `state/resilience/history.json`              | float   |
| Dead binding count      | LOLLI lint (`analyzeLolli()` output)         | integer |
| Conscience signal count | `state/conscience/signals/*.signal.json`     | integer |
| Policy violation count  | Governance audit output                      | integer |

The observation vector is reduced to a single state index via the classification rules above,
then fed to `MemristiveEngine::observe(state_index)`.

## Memristive Layer

The memristive layer is the key differentiator from a plain Markov chain. It models the
*difficulty* of state transitions based on history, using the `ConductanceMatrix` from
ix's memristive-markov crate.

### Conductance Matrix: R[i][j]

For each transition pair (from_state, to_state), the conductance matrix tracks a value
in [g_min, 1.0]:

- **High conductance** (close to 1.0): Transition is easy -- system has frequently traveled this path
- **Low conductance** (close to g_min): Transition is hard -- system rarely or never takes this path

### Strengthening (Hebbian)

When a transition occurs, its conductance is strengthened:

```
g[i][j] += alpha * (1.0 - g[i][j])
```

This means:
- Healthy -> Healthy transitions strengthen over time (virtuous cycle)
- Warning -> Freeze transitions also strengthen if they keep happening (vicious cycle)
- The asymptote at 1.0 prevents runaway

### Decay

Each cycle, all conductances decay toward g_min:

```
g[i][j] = max(g_min, g[i][j] * (1.0 - beta))
```

### Half-Life

The decay rate beta is calibrated so that conductances lose half their excess (above g_min)
in 10 cycles:

```
beta = 1.0 - 0.5^(1/10) ≈ 0.0669
```

This means a violation's "scar" is half-forgotten after 10 governance cycles, but fully
recovering from a deep freeze takes ~30 cycles (3 half-lives).

### Recommended Engine Configuration

```json
{
  "max_order": 3,
  "min_observations": 2,
  "session_alpha": 0.15,
  "session_beta": 0.0669,
  "long_term_alpha": 0.05,
  "long_term_beta": 0.02,
  "g_min": 0.01,
  "consolidation_gamma": 0.3,
  "min_session_observations": 5,
  "fallback": "uniform"
}
```

- `max_order: 3` -- Consider up to 3 previous states for context (captures short trends)
- `session_alpha: 0.15` -- Moderate strengthening per observation
- `session_beta: 0.0669` -- 10-cycle half-life
- `long_term_alpha: 0.05` -- Slow long-term learning
- `long_term_beta: 0.02` -- Long-term memory decays very slowly (~35 cycle half-life)

## Outputs

### 1. P(next_state | current_state, history)

A probability distribution over the 4 states for the next governance cycle, produced by
`MemristiveEngine::predict()`. Example:

```json
{
  "current_state": "Watch",
  "predictions": {
    "Healthy": 0.35,
    "Watch": 0.40,
    "Warning": 0.20,
    "Freeze": 0.05
  }
}
```

### 2. Predicted Cycles to Freeze

If P(Freeze) is non-trivial, the model estimates how many cycles until freeze becomes likely:

```
cycles_to_freeze = log(0.5) / log(P(not_freeze))
```

This gives the expected number of cycles before cumulative risk exceeds 50%.

### 3. Recommended Intervention

Based on the dominant risk signal in the observation vector:

| Dominant Risk Signal       | Intervention                                             |
|---------------------------|----------------------------------------------------------|
| High LOLLI/ERGOL ratio    | Execute existing artifacts; cite or deprecate            |
| Low resilience score      | Fix detection gaps from resilience history               |
| Rising dead bindings      | Run LOLLI lint; remove dead bindings from pipelines      |
| Rising conscience signals | Review and resolve conscience signals before next cycle   |
| Policy violations         | Governance audit; address violations in next PLAN phase  |

When P(Freeze) > 0.3, an alert is emitted with the top recommended intervention.

## Integration with ix Memristive-Markov

### Rust API Mapping

| Governance Operation       | ix API Call                                    |
|---------------------------|------------------------------------------------|
| Initialize model          | `MemristiveEngine::new(config)`                |
| Load saved state          | `MemristiveEngine::from_state(json)`           |
| Record cycle observation  | `engine.observe(state_index)`                  |
| Get state predictions     | `engine.predict()`                             |
| End-of-session rollup     | `engine.consolidate()`                         |
| Save model state          | `engine.export_state()`                        |
| Inspect model health      | `engine.diagnostics()`                         |

### Data Flow

```
state/resilience/history.json  ─┐
state/driver/lolli-ergol-*.json ─┤
state/conscience/signals/       ─┼─→ [classify] ─→ state_index ─→ engine.observe()
governance-audit output         ─┤                                      │
LOLLI lint output               ─┘                               engine.predict()
                                                                        │
                                                          ┌─────────────┴──────────────┐
                                                          │                            │
                                                state/markov/predictions.json   alert (if P(Freeze)>0.3)
```

### State Persistence

The engine's full state (tensor, conductance matrices, context buffer) is serialized via
`engine.export_state()` and stored at `state/markov/engine-state.json`. This allows the
model to resume across sessions without losing its memristive history.

## Transition Matrix Initialization

Before any observations, the transition matrix starts uniform:

```
P(j | i) = 0.25 for all i, j in {Healthy, Watch, Warning, Freeze}
```

As observations accumulate, the VLMM (Variable-Length Markov Model) inside the engine
learns the actual transition probabilities, and the conductance matrix modulates them
based on path history.

## Validation

The model's predictions are validated retrospectively:

1. After each cycle, compare the previous cycle's predicted state to the actual state
2. Track prediction accuracy over a rolling 10-cycle window
3. If accuracy drops below 0.5 for 5 consecutive cycles, reset the session conductance
   (the model has become miscalibrated) and log a conscience signal

Prediction records are appended to `state/markov/predictions.json` for retrospective analysis.

## Constitutional Basis

- **Article 8 (Observability):** Markov predictions are a first-class governance metric
- **Article 9 (Bounded Autonomy):** Freeze state enforces hard creation boundaries
- **Article 3 (Reversibility):** Model state can be rolled back via `from_state()` to any snapshot
- **Article 6 (Escalation):** P(Freeze) > 0.3 triggers escalation alert
