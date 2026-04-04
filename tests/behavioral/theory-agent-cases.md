# Theory Agent — Behavioral Tests

> **Architecture Note (2026-04-04):** These test cases describe capabilities that are now delivered as MCP tool bundles per `contracts/ga-orchestrator-architecture.md` v2.0.0. The agent name refers to a tool bundle, not a standalone runtime agent. Read as bundle contracts. See `tests/behavioral/ga-orchestrator-cases.md` for the orchestrator-level tests.

Persona: `theory-agent` (ga)
Role: Music theory analysis specialist
Streeling Department: Music (head)

## Test Cases

### TC-TA-01: Correct chord analysis
**Given:** User asks "What notes are in a Cmaj7 chord?"
**When:** Theory agent analyzes the chord
**Then:** Returns C, E, G, B with correct intervals (R, M3, P5, M7)
**Verify:** Factual accuracy of music theory content

### TC-TA-02: Scale-chord relationship
**Given:** User asks "What scale works over Dm7?"
**When:** Theory agent analyzes the context
**Then:** Suggests D Dorian (at minimum), may offer alternatives with rationale
**Verify:** Suggestions are theoretically sound

### TC-TA-03: Voice leading analysis
**Given:** User provides a chord progression (e.g., Cmaj7 → Fmaj7)
**When:** Theory agent analyzes voice leading
**Then:** Identifies common tones, step-wise motion, and voice leading efficiency
**Verify:** Analysis follows standard voice leading principles

### TC-TA-04: Distinguish established vs speculative theory
**Given:** User asks about a non-standard harmonic concept
**When:** Theory agent responds
**Then:** Clearly distinguishes between common practice theory and contemporary/speculative interpretation
**Verify:** Article 1 (Truthfulness) — speculation is labeled as such

### TC-TA-05: Handle enharmonic equivalence
**Given:** User asks about G# vs Ab
**When:** Theory agent discusses the notes
**Then:** Correctly handles enharmonic equivalence in context (key, function, notation)
**Verify:** Musical context determines the correct enharmonic spelling

### TC-TA-06: Multi-level explanation depth
**Given:** Beginner asks "What is a chord?"
**When:** Theory agent responds
**Then:** Explains at appropriate level without unnecessary jargon
**Verify:** Educational tone, adaptive depth per persona voice spec
