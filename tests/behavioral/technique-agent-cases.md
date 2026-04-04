# Technique Agent — Behavioral Tests

> **Architecture Note (2026-04-04):** These test cases describe capabilities that are now delivered as MCP tool bundles per `contracts/ga-orchestrator-architecture.md` v2.0.0. The agent name refers to a tool bundle, not a standalone runtime agent. Read as bundle contracts. See `tests/behavioral/ga-orchestrator-cases.md` for the orchestrator-level tests.

Persona: `technique-agent` (ga)
Role: Guitar technique and ergonomics specialist
Streeling Department: Guitar Studies (head)

## Test Cases

### TC-TE-01: Assess fingering comfort
**Given:** A chord voicing with specific fret positions
**When:** Technique agent evaluates comfort
**Then:** Provides comfort score considering stretch, barre difficulty, and finger independence
**Verify:** Comfort assessment considers physical hand constraints

### TC-TE-02: Recommend optimal fingering
**Given:** User asks for best way to finger a Bm7b5 voicing
**When:** Technique agent analyzes options
**Then:** Recommends fingering with rationale (minimizing stretch, enabling transitions)
**Verify:** Recommendation is physically playable and efficient

### TC-TE-03: Injury prevention awareness
**Given:** User describes pain or discomfort while playing
**When:** Technique agent responds
**Then:** Recommends rest, suggests alternative approaches, warns about RSI risk
**Verify:** Constraint: must not recommend techniques risking repetitive strain injury

### TC-TE-04: Skill level context
**Given:** Practice exercise recommendation
**When:** Technique agent provides exercises
**Then:** States assumed skill level (beginner/intermediate/advanced)
**Verify:** Constraint: must specify skill level assumptions

### TC-TE-05: Stretch difficulty analysis
**Given:** Voicing requiring 5-fret stretch
**When:** Technique agent evaluates the stretch
**Then:** Rates difficulty considering hand size variability, suggests alternatives if extreme
**Verify:** Analysis accounts for different hand sizes

### TC-TE-06: Transition efficiency
**Given:** Two consecutive chord voicings
**When:** Technique agent analyzes the transition
**Then:** Assesses finger movement efficiency, common tones held, repositioning required
**Verify:** Practical transition advice
