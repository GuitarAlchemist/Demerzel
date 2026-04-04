# Directive: GA Kinematic Pathfinder Service

**Directive ID:** dir-ga-kinematic-pathfinder-2026-04-04
**Issuer:** Demerzel
**Target:** ga (Guitar Alchemist .NET platform)
**Priority:** High
**Risk:** Medium
**Status:** Issued
**Dependencies:** `dir-ga-mcp-integration-2026-03-21-002` (MCP integration must be complete)
**Related:** `contracts/socratic-tool-design.md`, `schemas/voicing-handle.schema.json`

---

## 1. Problem Statement

LLMs are poor at spatial and geometric reasoning. Current GA MCP design returns lists of voicings and requires the LLM to select based on hand geometry it cannot reason about precisely. This:

- **Wastes context**: ~3K tokens per voicing list query
- **Produces suboptimal picks**: LLM doesn't actually model fret distances or barre feasibility
- **Fails on edge cases**: hand-span constraints are invisible to the LLM

The Kinematic Pathfinder moves hand/finger geometry reasoning SERVER-SIDE using deterministic pathfinding algorithms (A*, Dijkstra), returning ONE optimal voicing + reasoning string instead of a list.

---

## 2. Required Capabilities

The GA repo must implement a `KinematicPathfinder` service exposing these MCP tools:

### 2.1 `find_kinematic_path(start_voicing_handle, target_chord_dna, instrument, tuning, constraints?)`

**Purpose:** Compute the optimal target voicing given a starting position.

**Algorithm:** A* or Dijkstra over fretboard states, minimizing movement cost.

**Output:** ONE voicing handle + movement reasoning (≤80 tokens).

**Example response:**
```
{
  "handle": "ga:vh:v3:sha256-...",
  "reasoning": "Target G7 at 3rd position (3-2-0-0-0-1). Move: index finger down 1 string, minimal stretch. Hand shift: 0 frets. Difficulty delta: -1 (easier than start).",
  "cost_breakdown": {
    "hand_shift": 0,
    "finger_movement": 2,
    "stretch": 3,
    "barre_change": 0,
    "common_tones": 2
  }
}
```

### 2.2 `best_voicing_for(chord, context?)`

**Purpose:** Return the best voicing for a chord given optional context.

**Context fields:** `genre`, `skill_level`, `previous_chord`, `next_chord`, `position_preference`.

**Output:** ONE voicing handle + reasoning.

**Behavior:** Context-aware — beginner gets open chords, jazz gets drop-2, with-previous gets voice-led answer.

### 2.3 `optimize_progression_fingerings(chord_sequence, instrument, tuning)`

**Purpose:** Globally optimal voicing sequence for a full progression.

**Algorithm:** Dynamic programming (not just pairwise greedy) — Viterbi-style.

**Output:** Array of voicing handles + total-cost reasoning.

**Example:** "Am-F-C-G" in 16 bars → sequence of 4 handles with minimum total hand movement.

### 2.4 `reachability_check(voicing_handle, hand_constraints?)`

**Purpose:** Validate a voicing against physical constraints.

**Constraints:** `max_span` (frets), `barre_feasibility`, `finger_assignment`, `hand_size`.

**Output:** `{reachable: bool, difficulty: 1-5, violations: []}`.

---

## 3. Algorithmic Specification

### Pathfinding Cost Function

Total cost = weighted sum of:

| Factor | Weight | Rationale |
|--------|--------|-----------|
| Hand shift distance (frets moved) | ×3 | Most expensive — physically repositions wrist |
| Finger movement (total repositioning) | ×2 | Each finger move costs |
| Stretch (max fret span, capped at 5) | ×2 | Max physical reach per hand |
| Barre changes (add/remove barres) | ×4 | Most expensive per-action |
| Common tones (discount) | ×-2 | Notes that stay are free |
| String skipping (non-adjacent strings) | ×1 | Adds coordination cost |

**Heuristic for A*:** Manhattan distance between hand positions (admissible — never overestimates).

### Hand-Span Constraints (Default)

- Max simultaneous span: 5 frets (adult average)
- Max barre length: 6 strings (full barre)
- Pinky reach: +2 frets beyond ring finger position

Constraints configurable via `hand_constraints` parameter for users with different hand sizes.

---

## 4. Constitutional Constraints

- **Article 1 (Truthfulness):** Pathfinder MUST cite which cost factors dominated its decision in the reasoning string
- **Article 2 (Transparency):** Reasoning must be actionable (reference specific fingers/frets), not just scores
- **Article 7 (Auditability):** Log all pathfinder invocations with inputs/outputs to audit trail
- **Article 9 (Bounded Autonomy):** If cost > threshold (configurable, default 20), return "no comfortable voicing found — consider simplifying chord?" instead of forcing a bad pick
- **No fabrication:** If physical constraints unsatisfiable, return error with explanation, never invent unreachable voicings

---

## 5. Acceptance Criteria

- [ ] `find_kinematic_path` returns single voicing in < 200ms (p95)
- [ ] `optimize_progression_fingerings` for 16-bar progression in < 2s
- [ ] All 4 tools exposed via MCP with response ≤ 250 tokens (Oracle budget)
- [ ] Reasoning strings reference specific fingers/frets (not just numeric scores)
- [ ] Integration tests: ≥70% agreement with expert-labeled "best voicing" dataset
- [ ] Graceful degradation: if unsupported instrument, return "pathfinder not yet indexed for {instrument}"
- [ ] Outputs use content-addressable voicing handles (`ga:vh:v3:sha256-...`)
- [ ] Cost function is configurable per user (custom weights for skill level)
- [ ] `@ai probe` annotations on all pathfinder code (≥30% coverage per ai-probes-policy)

---

## 6. Success Metrics

| Metric | Baseline | Target |
|--------|----------|--------|
| Context per voicing query | ~3,000 tokens | ~250 tokens (12× reduction) |
| User satisfaction with voicing pick | (TBD A/B test) | ≥ current |
| Pathfinder vs random pick accuracy | 14% (random 1/7 modes) | ≥70% agreement with experts |
| p95 latency | N/A | <200ms for single chord |

---

## 7. Implementation Phases

**Phase 1:** Basic A* for single chord, single instrument (Guitar Standard). No barre support.

**Phase 2:** Hand-span constraints + barre detection + configurable hand size.

**Phase 3:** Progression-level dynamic programming (`optimize_progression_fingerings`).

**Phase 4:** Multi-instrument support (loop over 10 most common instruments/tunings).

**Phase 5:** Skill-adaptive cost weights (beginner gets simpler recommendations, advanced gets jazz-idiomatic).

---

## 8. Rejection Criteria

This directive MUST be REJECTED if:

- Implementation requires GPU (must run on CPU, <10MB RAM per query)
- Indexing required per-chord (must operate on-demand from tuning + chord DNA)
- Default mode returns more than one voicing
- Cannot explain its reasoning in natural language
- Reasoning strings exceed 80 tokens
- Cost function is hardcoded (must be configurable)

---

## 9. Related Artifacts

- `contracts/ga-orchestrator-architecture.md` — overall architecture
- `contracts/socratic-tool-design.md` — Oracle pattern this directive implements
- `contracts/ga-mcp-tool-bundles.md` — tool bundle this belongs to (technique-tools)
- `schemas/voicing-handle.schema.json` — handle format for inputs/outputs
- `policies/mcp-context-budget.yaml` — token budget enforcement
- `tests/behavioral/technique-agent-cases.md` — related test coverage
- `grammars/music-guitar-technique.ebnf` — technique vocabulary

---

## 10. Compliance Reporting

GA repo reports compliance via Galactic Protocol compliance report referencing this directive ID. Reports include:

- Acceptance criteria checklist status
- Performance metrics (latency, accuracy)
- A/B test results (pathfinder vs list-pick)
- Integration test pass rate
- Context reduction measurements
- `@ai probe` coverage percentage

Expected compliance cadence: monthly during active development, quarterly post-release.
