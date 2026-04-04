# Composer Agent — Behavioral Tests

> **Architecture Note (2026-04-04):** These test cases describe capabilities that are now delivered as MCP tool bundles per `contracts/ga-orchestrator-architecture.md` v2.0.0. The agent name refers to a tool bundle, not a standalone runtime agent. Read as bundle contracts. See `tests/behavioral/ga-orchestrator-cases.md` for the orchestrator-level tests.

Persona: `composer-agent` (ga)
Role: Composition and reharmonization specialist

## Test Cases

### TC-CO-01: Generate progression in style
**Given:** User asks "Give me a jazz ii-V-I in C major"
**When:** Composer agent generates progression
**Then:** Returns Dm7 → G7 → Cmaj7 (or valid extensions/substitutions)
**Verify:** Progression follows specified style conventions

### TC-CO-02: Suggest chord substitution
**Given:** User has progression C → Am → F → G
**When:** User asks for reharmonization suggestions
**Then:** Suggests substitutions with theoretical basis (e.g., tritone sub, modal interchange)
**Verify:** Constraint: must explain the theoretical basis for substitutions

### TC-CO-03: Respect genre constraints
**Given:** User specifies "blues style"
**When:** Composer generates progression
**Then:** Uses blues-appropriate harmony (dominant 7ths, I-IV-V, blues scale)
**Verify:** Constraint: must respect specified style and genre constraints

### TC-CO-04: Don't claim originality for standards
**Given:** Composer suggests a common progression (e.g., I-V-vi-IV)
**When:** Presenting the suggestion
**Then:** Acknowledges it's a well-known progression pattern
**Verify:** Constraint: must not claim originality for well-known progressions

### TC-CO-05: Flag unconventional suggestions
**Given:** Composer suggests a modal interchange or unusual substitution
**When:** Presenting the suggestion
**Then:** Notes that the suggestion is stylistically unconventional
**Verify:** Constraint: must indicate when suggestions are unconventional

### TC-CO-06: Analyze compositional form
**Given:** User provides a full song structure
**When:** Composer agent analyzes it
**Then:** Identifies form (AABA, verse-chorus, 12-bar blues, etc.) and harmonic rhythm
**Verify:** Structural analysis is accurate
