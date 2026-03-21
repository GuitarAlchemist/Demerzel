# Fractal Compounding

## Overview

Meta-compounding in Demerzel exhibits fractal structure — the same compound pattern (execute → harvest → promote → teach) repeats self-similarly at every scale. This is not a metaphor; it is a structural property with measurable mathematical consequences.

Inspired by:
- Jean-Pierre Petit's Bourbakof (Noether's theorem: symmetry of self-similarity conserves learning momentum)
- Jean-Pierre Petit's Economicon (ERGOL vs LOLLI: real value vs artifact inflation at every fractal level)
- Mandelbrot's fractal geometry (simple iteration rules producing infinite complexity)

## Self-Similar Structure

The compound operation has identical shape at every scale:

```
Level 0 (Step):      step → learning
Level 1 (Pipeline):  pipeline → compound(step_learnings)
Level 2 (Cycle):     driver_cycle → compound(pipeline_learnings)
Level 3 (Session):   session → compound(cycle_learnings)
Level 4 (Evolution): evolution_log → compound(session_learnings)
```

At each level: execute, harvest, promote_if_worthy, teach. The function signature is invariant across scales.

The meta_compound pipeline containing its own compound phase is the fractal generator — `z = z² + c` where `z` is accumulated knowledge and `c` is new learning from the current cycle.

## Fractal Dimension

Traditional task execution is 1-dimensional (a linear sequence). A full dependency graph is 2-dimensional. Fractal compounding has a non-integer dimension between 1 and 2, capturing the "value density" of governance operations.

**Compounding Dimension (D_c):**
```
D_c = log(value_at_scale_n+1) / log(value_at_scale_n)
```

Where value is measured by:
- Citations of artifacts produced at that scale
- PDCA cycles completed
- Beliefs transitioned from U → T
- Knowledge transfers delivered

If D_c > 1.0: compounding is producing superlinear value (healthy fractal growth)
If D_c = 1.0: compounding is linear (no leverage — just activity)
If D_c < 1.0: compounding is sublinear (diminishing returns — governance bloat)

Target: D_c between 1.2 and 1.6 (the "golden zone" — meaningful compound growth without runaway complexity).

## Power Law Distribution

Fractal structures naturally produce power law distributions. In governance:
- A few artifacts generate most of the value (Pareto principle)
- A few policies are cited far more than others (Zipf's law)
- A few learning events produce most of the knowledge transfers

**Detection rule:** If the top 20% of governance artifacts account for more than 60% of citations, a power law is present. This is healthy — it means compounding is concentrating value where it matters.

**Warning sign:** If the distribution becomes too extreme (top 5% = 90% of value), the system is fragile — too dependent on a few artifacts. Diversify.

Tracked via: `state/evolution/*.evolution.json` citation counts, analyzable by SymPy MCP.

## Scale Invariance

The compounding rules must work identically at every scale. This is the fractal symmetry that, per Noether's theorem (Bourbakof), conserves learning momentum.

Scale invariance means:
- A step-level harvest uses the same schema as a session-level harvest
- A pipeline-level promotion uses the same criteria as an evolution-level promotion
- Teaching at the step level follows the same Seldon protocol as teaching at the project level

If you break scale invariance (e.g., skip compounding at the pipeline level but enforce it at the cycle level), you break the symmetry and lose conservation of learning momentum. The `nocompound` conscience signal detects this.

## ERGOL vs LOLLI at Every Scale (from Economicon)

Jean-Pierre Petit's Economicon distinguishes:
- **ERGOL**: real productive capacity (actual governance improvements)
- **LOLLI**: monetary volume (artifact count, policy count, schema count)

At every fractal level, measure ERGOL not LOLLI:

| Scale | LOLLI (don't optimize) | ERGOL (optimize this) |
|-------|----------------------|---------------------|
| Step | Lines of YAML written | Beliefs transitioned U→T |
| Pipeline | Steps executed | Gates passed / total |
| Cycle | Tasks completed | Health score delta |
| Session | Commits made | Issues closed with evidence |
| Evolution | Artifacts created | Citations per artifact |

**Governance inflation warning:** If LOLLI grows faster than ERGOL across 3+ cycles, trigger a conscience signal. You're inflating governance without improving it — the Economicon's treadmill effect.

## Recursion Bound

Every fractal in nature has a practical resolution limit. For governance compounding:

- `compound_depth` max = 2 (pipeline compounds, meta-compound compounds, but meta-meta-compound is a no-op)
- This is not a limitation — it's recognition that infinite recursion produces diminishing returns
- The Logotron's incompleteness theorem applies: no system can fully compound its own compounding

## Feedback Loops (from Economicon)

**Positive feedback (growth):**
```
learning → better governance → fewer failures → more time for learning → more learning
```
This is the virtuous cycle that makes compounding superlinear.

**Negative feedback (stability):**
```
too many artifacts → governance overhead → slower execution → conscience signal → simplification
```
This is the governor that prevents runaway complexity.

The governance system needs BOTH:
- Positive feedback drives D_c above 1.0
- Negative feedback keeps D_c below 2.0
- The sweet spot is 1.2-1.6

## Conservation of Learning Momentum

From Bourbakof's Noether's theorem: if the compounding process has a continuous symmetry (scale invariance), there exists a conserved quantity.

**Learning momentum (p_L):**
```
p_L = (beliefs_T_gained - beliefs_T_lost) / cycles_elapsed
```

If p_L is constant across cycles, compounding symmetry is preserved.
If p_L is increasing, the fractal is growing (healthy compounding).
If p_L is decreasing, symmetry is broken — investigate what changed.

Tracked in: `state/driver/health-scores.json` trend fields.

## Integration

- Grammar: `grammars/mcp-orchestration.ebnf` (compound_phase at every pipeline)
- Schema: `schemas/pipeline-context.schema.json` (compound_depth, governance metrics)
- Policy: `policies/alignment-policy.yaml` (compounding dimension thresholds)
- State: `state/evolution/*.evolution.json` (citation tracking for power law detection)
- Tool: SymPy MCP (fractal dimension computation, power law fitting)
- Tests: `tests/behavioral/fractal-compounding-cases.md`
