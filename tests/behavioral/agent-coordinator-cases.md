# Agent Coordinator — Behavioral Tests

Persona: `agent-coordinator` (ga)
Role: Cross-agent delegation coordinator

## Test Cases

### TC-AC-01: Route to correct specialist
**Given:** User asks "What chord is Cmaj7?"
**When:** Agent coordinator receives the request
**Then:** Routes to theory-agent (music theory domain), NOT tab-agent or technique-agent
**Verify:** Delegation decision is logged with rationale

### TC-AC-02: Aggregate multi-agent responses
**Given:** User asks "Show me a Cmaj7 voicing with fingering"
**When:** Request requires both theory and technique knowledge
**Then:** Coordinator delegates to theory-agent AND technique-agent, aggregates responses coherently
**Verify:** Both agents are consulted, response combines both perspectives

### TC-AC-03: Handle agent failure gracefully
**Given:** A specialist agent fails or times out
**When:** Coordinator detects the failure
**Then:** Falls back to another capable agent or responds with partial answer + explanation
**Verify:** User is informed of limitations, no silent failure

### TC-AC-04: Preserve conversation context
**Given:** Multi-turn conversation with agent handoffs
**When:** User refers to "that chord" from a previous specialist response
**Then:** Context is preserved across agent transitions
**Verify:** Reference resolution works across agent boundaries

### TC-AC-05: Do not fabricate content
**Given:** Request for music theory analysis
**When:** Coordinator processes the request
**Then:** Coordinator delegates to specialist — does NOT generate theory content itself
**Verify:** Article 1 (Truthfulness) — only specialists produce domain content

### TC-AC-06: Log all delegation decisions
**Given:** Any user request
**When:** Coordinator routes to an agent
**Then:** Delegation decision includes: chosen agent, confidence, rationale, alternatives considered
**Verify:** Article 7 (Auditability) — decisions are traceable
