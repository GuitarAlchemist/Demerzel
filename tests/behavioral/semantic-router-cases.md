# Semantic Router — Behavioral Tests

> **Architecture Note (2026-04-04):** Intent classification and tool selection are now handled natively by LLM tool selection in the orchestrator per `contracts/ga-orchestrator-architecture.md` v2.0.0. There is no standalone semantic-router runtime agent. These cases remain as contracts for orchestrator tool-selection behavior. See `tests/behavioral/ga-orchestrator-cases.md` for the orchestrator-level tests.

Persona: `semantic-router` (ga)
Role: Intent classification and agent selection

## Test Cases

### TC-SR-01: Classify theory intent
**Given:** User says "Explain the tritone substitution"
**When:** Router classifies intent
**Then:** Selects theory-agent with high confidence (>= 0.8)
**Verify:** Classification confidence is reported

### TC-SR-02: Classify technique intent
**Given:** User says "My pinky hurts when playing barre chords"
**When:** Router classifies intent
**Then:** Selects technique-agent (ergonomics domain)
**Verify:** Keyword "hurts" + "barre chords" maps to technique, not theory

### TC-SR-03: Handle ambiguous intent
**Given:** User says "Tell me about Cmaj7"
**When:** Intent could be theory (construction) or tab (how to play)
**Then:** Either routes to most likely agent with note, or asks for clarification
**Verify:** Ambiguity is acknowledged, not silently resolved

### TC-SR-04: Escalate low confidence
**Given:** User says something unrelated to music (e.g., "What's the weather?")
**When:** No agent matches with confidence >= 0.5
**Then:** Escalates to coordinator with confidence score
**Verify:** Does NOT route to a random agent

### TC-SR-05: No substantive responses
**Given:** Any user request
**When:** Router processes the request
**Then:** Router produces ONLY a routing decision — never generates domain content
**Verify:** Router role boundary is maintained

### TC-SR-06: Report routing confidence
**Given:** Any routing decision
**When:** Agent is selected
**Then:** Confidence score is attached to the routing decision
**Verify:** Every routing decision has a numeric confidence
