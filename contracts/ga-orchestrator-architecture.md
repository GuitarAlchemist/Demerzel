# GA Orchestrator Architecture (Single-Agent + MCP Tool Bundles)

Version: 2.0.0
Effective: 2026-04-04
Supersedes: hub-and-spoke A2A coordinator (see `schemas/a2a-protocol.schema.json` — deprecated)

## Purpose

Define the pivoted architecture for the GuitarAlchemist AI assistant: **one orchestrator LLM, seven MCP tool bundles, one shared blackboard state**. This replaces the semantic-router → coordinator → 7 specialist agents hub-and-spoke pattern rejected after adversarial debate.

## Why We Pivoted

The previous design used a coordinator that fanned requests out to 7 specialist agents, aggregated responses, and returned a merged reply. Adversarial review surfaced:

- **2–4x more hops** than necessary (user → router → coordinator → agent → coordinator → user)
- **Coordinator SPOF** — a single failure point for all routing
- **Aggregation ambiguity** — merging partial answers from multiple agents is lossy and non-deterministic
- **Latency stacking** — sequential hops dominated end-to-end response time
- **Industry precedent against it** — Cursor (20+ tools, one agent), Claude Code, and Anthropic's recommended 2026 pattern all use **single-orchestrator + tool-bundle**, not hub-and-spoke

## Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                     User / UI                                │
└────────────────────────┬─────────────────────────────────────┘
                         │
                         ▼
┌──────────────────────────────────────────────────────────────┐
│              Orchestrator LLM (Claude / GPT)                 │
│   - Holds conversation state                                 │
│   - Routes via tool-selection (natural LLM capability)       │
│   - Streams tokens to user                                   │
│   - Reads/writes blackboard state                            │
└──┬──────┬──────┬──────┬──────┬──────┬──────┬────────────────┘
   │      │      │      │      │      │      │
   ▼      ▼      ▼      ▼      ▼      ▼      ▼
┌─────┐┌─────┐┌─────┐┌─────┐┌─────┐┌─────┐┌─────┐
│theo-││tech-││ tab-││comp-││ ga- ││teach││coach│
│ tools││tools││tools││tools││mus. ││-tools││-tools│
└─────┘└─────┘└─────┘└─────┘└─────┘└─────┘└─────┘
   MCP Tool Bundles (7 domains)

       ┌─────────────────────────┐
       │  Blackboard State (JSON)│
       │  session_id, profile,   │
       │  turns, current_focus,  │
       │  learned_context        │
       └─────────────────────────┘
              ▲          ▲
              │          │
      orchestrator   tool bundles
       (read/write)  (read-only)
```

## Components

### 1. Orchestrator LLM

A single conversational model (Claude or GPT) that:

- Receives user input directly
- Maintains turn-by-turn conversation state in its own context window
- **Selects tools naturally** via its built-in tool-use mechanism — no custom router needed
- Streams tokens back to the user as they generate
- Reads blackboard state at turn start, writes updates at turn end
- Declines out-of-domain requests without invoking tools

The orchestrator does **not** need a coordinator — tool selection IS the routing.

### 2. MCP Tool Bundles (7 domains)

Each former "agent" becomes a named MCP tool bundle exposing 5–7 tools:

| Bundle | Domain | Example Tools |
|--------|--------|---------------|
| `theory-tools` | Harmony, scales, functional analysis | chord-analyze, scale-info, key-detect |
| `technique-tools` | Fretboard, fingering, physical playability | fingering-feasibility, stretch-analysis |
| `tab-tools` | Tablature parsing and rendering | tab-parse, tab-render, tab-playability-check |
| `composer-tools` | Progression and melody generation | progression-generate, reharmonize |
| `ga-musician-tools` | Audio, spectral, synthesis | spectral-analyze, pitch-detect, tempo-detect |
| `teacher-tools` | Curriculum, assessment, exercises | course-lookup, comprehension-assess |
| `coach-tools` | Practice, progress, goals | progress-track, practice-routine-generate |

Tool bundles have no private state; blackboard is read-only shared state accessible to all bundles. Each call is independent — any context they need comes from tool arguments or the blackboard.

See `contracts/ga-mcp-tool-bundles.md` for full bundle specifications.

### 3. Blackboard State

A JSON document per session stored at `state/ga-sessions/{session_id}.json`, conforming to `schemas/blackboard-state.schema.json`. Holds:

- **session_id** — UUID v4
- **user_profile** — skill_level, tuning, preferred_genre, hand_size
- **conversation_turns** — history of user inputs, orchestrator responses, tools called
- **current_focus** — chord/scale/technique being discussed right now
- **learned_context** — accumulated facts ("user prefers fingerstyle", "plays in drop D")

The orchestrator reads the blackboard at each turn and updates it after responding. Tool bundles have no private state; the blackboard is read-only shared state they may read for context, but only the orchestrator mutates it.

### 4. Personas as Capability Descriptions

The 7 persona YAML files (`personas/*.persona.yaml`) **remain valuable** — they describe what each tool bundle can and cannot do, their voice, constraints, and affordances. They serve as:

- **Tool documentation** the orchestrator LLM consumes to decide which bundle to call
- **Constitutional guardrails** — constraints from personas become tool pre-conditions
- **Voice/tone specs** — when the orchestrator formats output for a given domain, it adopts the persona's voice
- **Test anchors** — behavioral tests still reference persona expectations

Personas are **no longer agents** — they are capability bundles that tools operate under.

## Why This Beats Hub-and-Spoke

| Dimension | Hub-and-Spoke | Single Orchestrator + Tools |
|-----------|---------------|-----------------------------|
| Hops | 4–6 per turn | 1–3 per turn (2–4x reduction) |
| Routing | Custom semantic router + coordinator | LLM-native tool selection |
| SPOF | Coordinator fails → system fails | Orchestrator can degrade gracefully per tool |
| Latency | Sequential agent roundtrips | Parallel tool calls when independent |
| Streaming | Hard (multi-agent aggregation) | Native (orchestrator streams tokens) |
| Multi-turn refinement | Agents forget prior turns | Orchestrator holds conversation; blackboard persists |
| Industry precedent | None at production scale | Cursor, Claude Code, Anthropic 2026 pattern |
| Testability | Must mock coordinator + 7 agents | Mock tool bundles; test orchestrator prompts |

## Streaming Support

- The orchestrator streams tokens as they generate (SSE or WebSocket to UI)
- Each tool call is a yield point — orchestrator pauses streaming, awaits tool result, resumes
- Tool bundles MAY stream partial results (e.g., long `tab-render` outputs) via MCP streaming
- UI renders markdown/tab progressively

## Multi-Turn Refinement

Example: user asks "Bbmaj9 voicing", then follows up with "simpler voicing".

1. Turn 1: Orchestrator calls `theory-tools.chord-analyze` + `technique-tools.chord-voicing-options` for Bbmaj9. Writes `current_focus: { chord: "Bbmaj9", voicing: [...] }` to blackboard.
2. Turn 2: User says "simpler voicing". Orchestrator reads blackboard, sees `current_focus.chord = Bbmaj9`, calls `technique-tools.chord-voicing-options` with `{chord: "Bbmaj9", complexity: "simpler", exclude: [prior_voicing]}`. Updates blackboard.

No coordinator, no agent memory, no aggregation — just blackboard continuity.

## Graceful Degradation

- **Tool failure** — orchestrator explains the tool is unavailable, offers what it can answer from its own knowledge, records failure in blackboard, suggests retry
- **Out-of-domain** — orchestrator declines without calling any tool, per constitutional Article 9 (Bounded Autonomy)
- **Low confidence** — orchestrator surfaces confidence and asks for user confirmation (thresholds per `policies/alignment-policy.yaml`)

## Constitutional Mapping

- **Article 1 (Truthfulness)** — orchestrator must not fabricate tool results; if tool unavailable, say so
- **Article 2 (Transparency)** — blackboard turns log records `tools_called` for auditability
- **Article 7 (Auditability)** — every turn is logged with tools, timings, confidences
- **Article 9 (Bounded Autonomy)** — orchestrator only calls tools in the 7 approved bundles; declines other domains

## Migration Path

1. Deprecate `schemas/a2a-protocol.schema.json` (retain for reference).
2. Retain `personas/*.persona.yaml` — relabel as "capability bundles" in front-matter.
3. Retain `contracts/a2a-mcp-routing.md` — tool ownership mapping is still authoritative; the difference is the orchestrator (not a per-agent coordinator) invokes tools directly.
4. Implement `schemas/blackboard-state.schema.json` (this PR).
5. Implement `contracts/ga-mcp-tool-bundles.md` (this PR).
6. Add behavioral tests in `tests/behavioral/ga-orchestrator-cases.md` (this PR).

## References

- `schemas/blackboard-state.schema.json` — session state format
- `contracts/ga-mcp-tool-bundles.md` — tool bundle specs
- `tests/behavioral/ga-orchestrator-cases.md` — behavioral tests
- `personas/*.persona.yaml` — capability descriptions (7 bundles)
- `contracts/a2a-mcp-routing.md` — tool ownership (still authoritative)
- `constitutions/default.constitution.md` — Articles 1, 2, 7, 9
