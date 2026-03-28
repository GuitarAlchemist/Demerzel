# Fractal Algedonic Architecture — Design Specification

**Date:** 2026-03-28
**Source:** Multi-AI brainstorm (Codex GPT-5.4 + Claude Opus 4.6)
**Status:** Draft — ready for incremental implementation

## Executive Summary

The Prime Radiant's governance visualization should evolve from a passive dashboard into an **active governance engine** where the physics simulation IS the governance mechanism. Five core concepts emerge from cross-model synthesis:

1. **Constitutional Gravity + Governance Charge** — mass = importance, charge = health
2. **Governance Tides (Immunology)** — pain/pleasure waves modulate future sensitivity
3. **Dark Governance Matter** — invisible stabilizer nodes (unfired constraints)
4. **Hexavalent State Rendering** — fix T/P/U/D/F/C visibility gap
5. **Algedonic Lattice + Orbital Compiler** — recursive event fabric with navigable IxQL arcs

## 1. Constitutional Gravity + Governance Charge

### Current State
- `TYPE_SIZE` in ForceRadiant.tsx gives constitutions mass 30, policies 8, tests 4
- Force-directed layout already creates gravitational hierarchy accidentally
- All relationships are attractive (pull toward center)

### Target State
- **Mass** = importance (attraction between all nodes) — unchanged
- **Charge** = health state:
  - Healthy (T/P states) → positive charge → attracts neighbors → stable orbits
  - Unhealthy (F/D/C states) → negative charge → repels neighbors → visual instability
  - Unknown (U) → neutral → drifts
- Contradictory nodes create visible instability in local graph topology
- When contradiction resolves → node snaps back into stable orbit

### Implementation
```typescript
// In ForceRadiant.tsx node rendering
const healthCharge = getNodeCharge(node);
// Modify d3-force charge strength per node
fg.d3Force('charge').strength(node => {
  const base = -TYPE_SIZE[node.type] * 2;
  const health = getHealthCharge(node); // -1 to +1
  return base * (1 + health * 0.5); // unhealthy nodes repel more
});
```

## 2. Governance Tides (Governance Immunology)

### Concept
Pain/pleasure signals don't just fire-and-forget. They accumulate as **immune memory**:
- **Innate immunity** — constitutional articles (always active)
- **Adaptive immunity** — learned remediation patterns from past incidents
- **Inflammation** — heightened sensitivity in recently-hurt areas
- **Autoimmune risk** — system attacking itself when sensitivity is too high

### Signal Packet Schema
```yaml
algedonic_packet:
  scope: string           # node/cluster/system
  severity: enum          # critical/emergency/safety/info
  valence: enum           # pain/pleasure
  confidence: float       # 0.0-1.0
  hexavalent_state: enum  # T/P/U/D/F/C
  repairability: float    # 0.0-1.0 (can this self-heal?)
  time_horizon: duration  # how long until this matters?
  lineage: string[]       # ancestor signal IDs (anti-storm)
  immune_memory: float    # local sensitivity (0=desensitized, 1=inflamed)
```

### Tidal Mechanics
- Each governance region has `tideLevel: float` (-1 to +1)
- Pain events push tide negative (inflammation)
- Pleasure events push tide positive (stabilization)
- Tide decays toward 0 over time (half-life: 7 days)
- Tide modulates escalation thresholds:
  - `effectiveThreshold = baseThreshold * (1 - tideLevel * 0.3)`
  - Inflamed regions escalate at lower thresholds
  - Stable regions absorb more before escalating
- Autoimmune warning when `tideLevel < -0.8` for > 3 consecutive cycles

### Visualization
- Ambient color temperature around planets shifts warm→cool based on tide
- Inflamed regions pulse with a red-shifted halo
- Stable regions glow with steady blue-white

## 3. Dark Governance Matter

### Concept
The system is held together more by what DOESN'T happen than what does. For each policy, count constraints that could fire but haven't. These implicit governance forces are invisible but essential.

### Implementation
- For each policy in the graph, compute `implicitGovernanceScore`:
  - Count defined constraints / trigger conditions
  - Subtract actually-fired signals
  - The remainder = dark matter contribution
- Render as **gravitational lensing** effect:
  - Regions with strong implicit governance appear stable (minimal distortion)
  - Regions with weak implicit governance show spacetime ripples (vulnerability)
  - Toggle "Dark Matter Mode" to see density heatmap overlay
- Expected ratio: ~5:1 (dark:visible), matching cosmological observation

### Shader Effect
```glsl
// Gravitational lensing distortion around stable regions
float darkMatterDensity = texture2D(uDarkMatterMap, vUv).r;
vec2 distortion = (darkMatterDensity - 0.5) * 0.02 * normalize(vUv - vec2(0.5));
vec4 color = texture2D(uSceneTexture, vUv + distortion);
```

## 4. Hexavalent State Fix

### Discovery
`logic/tetravalent-state.schema.json` defines 6 values (T/P/U/D/F/C) but all documentation, visualization, and policy thresholds reference only 4 (T/F/U/C). Two states (P=Probable, D=Doubtful) are invisible.

### Actions Required
1. **Update CLAUDE.md** — change "Tetravalent Logic" to "Hexavalent Logic"
2. **Update visualization** — add P and D rendering:
   - T = solid bright green (verified)
   - P = bright green with subtle pulse (probably true, needs confirmation)
   - U = dim amber with expanding fog (unknown, investigating)
   - D = dim red with contracting fog (probably false, needs refutation)
   - F = solid red (refuted)
   - C = interference pattern / flickering (contradictory)
3. **Update confidence thresholds** — add P/D-specific thresholds:
   - P (>=0.7 confidence): proceed with monitoring
   - D (>=0.3 but <0.5): investigate before acting
4. **Update algedonic routing** — P→T transitions are quiet, D→F transitions may need review

## 5. Algedonic Lattice + Orbital Compiler

### Recursive Event Fabric
Every governance node is a mini-VSM cell:
- S1 = operations (the node's actual function)
- S2 = coordination (sync with siblings)
- S3 = control (monitor health metrics)
- S4 = intelligence (predict future state)
- S5 = identity (constitutional compliance)

Signals route upward only after local S3/S4 attempts absorption.
Algedonic bypass activates when:
- Contradiction on a protected policy
- Accelerating belief collapse (velocity check)
- Cascading schema drift across repos
- Cross-repo deadlock

### IxQL Self-Healing Patterns
```ixql
-- Cybernetic reflex arc
PIPELINE schema_drift_repair
  DETECT drift IN schemas WHERE confidence_delta > 0.2
  CLASSIFY severity USING tars.assess(method: "hexavalent")
  LOCALIZE owner USING personas.resolve(drift.domain)
  SIMULATE fix USING ix.compatibility_check(drift, dependents)
  PATCH IF fix.repairability > 0.7 AND fix.reversible = true
  VERIFY USING tests.behavioral(drift.domain)
  PROMOTE IF residual_contradiction = false
    THEN emit(governance_evolution, fix.pattern)

-- Contradiction splitter
PIPELINE contradiction_handler
  ON state_change TO "C"
  FORK
    BRANCH evidence_for: collect(supporting_evidence)
    BRANCH evidence_against: collect(refuting_evidence)
  ARBITRATE USING weighted_evidence_scoring
  IF resolution THEN emit(belief_crystallization)
  ELSE escalate(algedonic, severity: "emergency")

-- Debounce with hysteresis
PIPELINE algedonic_debounce
  WINDOW 3 consecutive observations
  ESCALATE ONLY IF contradictory_count >= 3
  DOWNGRADE WHEN convergence_score > 0.8 FOR 5 cycles
```

### Orbital Compiler Visualization
- IxQL pipelines compile to visible transfer arcs between nodes
- `DETECT` = origin moon/service
- `CLASSIFY` → `LOCALIZE` = trajectory through S3 control ring
- `SIMULATE` → `PATCH` = transfer orbit to target
- `PROMOTE` = ascent to higher orbital shell (constitutional layer)
- Color: green=repair, amber=investigate, red=escalate

## 6. Semantic Zoom (LOD for Governance)

### Zoom Levels + Action Constraints

| LOD | Camera Distance | Visible | Available Actions |
|-----|----------------|---------|-------------------|
| 0 | > 8 Earth radii | Planet clusters, orbital health, tide color | Galactic Protocol directives only |
| 1 | 3-8 radii | VSM organs (S1-S5 rings), department clusters | Strategic: recon, audit, policy review |
| 2 | 1-3 radii | Individual policies, personas, schemas, IxQL arcs | Tactical: modify thresholds, assign personas |
| 3 | < 1 radius | Evidence tuples, test cases, belief history, hexavalent states | Operational: update evidence, run tests |

### Expansion Rules
- Proximity-driven: nodes expand when camera approaches
- Priority-driven: contradictory nodes expand FIRST (urgent visibility)
- Healthy nodes stay compressed longer (don't waste attention)
- Persistent anchors: a "policy" is traceable whether rendered as glow, edge, district, or document

## 7. Cross-Repo Routing (Galactic Protocol)

### Treaty Gateways
All cross-repo directives pass through explicit gateway services:
```yaml
galactic_directive:
  source_constitution: string
  target_jurisdiction: string
  requested_action: string
  confidence: float
  evidence_bundle: Evidence[]
  rollback_expectation: string
  required_acknowledgment: boolean
  treaty_metadata:
    trust_weight: float
    compatibility_score: float
    constitutional_filter: string[]
```

### Routing Priority
1. Lowest common governance layer first (Integrator, not S5)
2. Only unresolved treaty conflicts reach interplanetary S5 arbitration
3. Visualization: transfer orbits with color encoding (advisory=blue, imperative=gold, contradictory=purple, algedonic=red)

## Non-Obvious Technical Constraints

1. **Recursive alert storms** — lineage IDs + suppression windows + "already seen by ancestor" markers
2. **Tetravalent (hexavalent) breaks dashboards** — C-state can't be red/green; it's BOTH
3. **Cognitive discontinuity** — LOD transitions need persistent identity anchors
4. **Cross-repo causality skew** — failure in ga may originate in ix, amplified by tars; needs event sourcing
5. **Self-healing governance violation** — repairs that silently mutate policy-adjacent artifacts need constitutional scopes

## Attribution

- **Codex (GPT-5.4):** Algedonic Lattice, Orbital Compiler, Treaty Gateways, Governance Tides, IxQL patterns, LOD schemas
- **Claude (Opus 4.6):** Dark Governance Matter, Retrograde Governance, Governance Uncertainty Principle, hexavalent discovery, Constitutional Gravity naming, Signal Archaeology, Belief Half-Life
- **Synthesis:** Governance Immunology framing, Charge model, unified architecture
