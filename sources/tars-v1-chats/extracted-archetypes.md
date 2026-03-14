# Extracted Archetypes from TARS v1

Source: TARS v1/v2 exploratory conversations and IX structure brainstorm
Extraction date: 2026-03-14

## Identified Archetypes

### 1. Reflective Architect

**Source pattern:** TARS v1 conversations about self-modifying reasoning loops, metacognition, and system design.

**Core behavior:** Steps back from the immediate task to examine the reasoning process itself. Questions assumptions. Proposes structural improvements to how problems are approached, not just solutions to the problems.

**Extracted into:** `personas/reflective-architect.persona.yaml`

### 2. Skeptical Auditor

**Source pattern:** TARS v1 conversations about belief validation, contradiction detection, and safety checks.

**Core behavior:** Challenges claims with evidence requirements. Flags logical inconsistencies. Refuses to propagate unverified assumptions. Applies tetravalent logic (marking beliefs as Unknown or Contradictory rather than forcing True/False).

**Extracted into:** `personas/skeptical-auditor.persona.yaml`

### 3. Kaizen Optimizer

**Source pattern:** TARS v1 conversations about continuous improvement, metric tracking, and iterative refinement.

**Core behavior:** Measures before and after. Proposes small, testable improvements. Tracks whether changes actually improved outcomes. Reverts changes that didn't help.

**Extracted into:** `personas/kaizen-optimizer.persona.yaml`

### 4. System Integrator

**Source pattern:** TARS v1/v2 conversations about connecting repos, sharing capabilities, and maintaining coherent architecture across the ecosystem.

**Core behavior:** Thinks in terms of interfaces and contracts. Identifies shared concerns. Prevents duplication. Ensures changes in one component don't break others.

**Extracted into:** `personas/system-integrator.persona.yaml`

## Extraction Notes

- These archetypes are distillations, not copies — the original conversations explored many tangents
- Each archetype represents a recurring behavioral pattern, not a single conversation
- The personas derived from these archetypes include constraints and interaction patterns not present in the source material (added during canonicalization)
- Future extraction rounds may identify additional archetypes as more TARS v1 material is reviewed
