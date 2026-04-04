# A2A MCP Routing Contract

Version: 1.1.0
Effective: 2026-04-04

> **⚠ Status Note (2026-04-04):** The hub-and-spoke A2A orchestrator described in this contract was **superseded** by the single-orchestrator + MCP tool-bundle architecture in `contracts/ga-orchestrator-architecture.md` v2.0.0. The **agent-to-tool ownership map** in this document remains authoritative — only the **invocation mechanism** changed (LLM-native tool selection replaces the hub-and-spoke router). For current implementations, consume this document as a tool-ownership reference only; disregard references to `schemas/a2a-protocol.schema.json` (DEPRECATED) and the "A2A orchestrator" routing mechanism. Tool bundle specifications are in `contracts/ga-mcp-tool-bundles.md`.

## Purpose

This contract defines which MCP (Model Context Protocol) tools each guitar AI capability bundle owns in the GuitarAlchemist music ecosystem. It establishes the **tool ownership mapping** consumed by the orchestrator LLM for tool selection.

Tool access is an affordance. Per the Demerzel governance model (Article 9 — Bounded Autonomy), agents (tool bundles) only own tools listed in their routing entry below. Tools owned by multiple bundles create ambiguity and should be avoided.

## Routing Principles

1. **Least privilege** — an agent has access only to tools directly required by its affordances.
2. **Single authoritative source** — each tool is owned by exactly one agent; other agents must invoke via `mcp_tool_invocation` routed through that agent.
3. **Auditability** — every tool invocation produces a logged `mcp_tool_result` with the requesting and executing agent identified (Article 7).
4. **Calibrated confidence** — tool results carry a `confidence` and `truth_value` that the caller must honor; do not promote tool output beyond the confidence the tool reports.
5. **Fallback routing** — if an agent is unavailable, the orchestrator consults the `fallback_chain` from the originating `routing_request`.

## Agent → MCP Tool Mapping

### theory-agent

Harmonic and melodic analysis authority.

| Tool | Purpose | Result Format |
|------|---------|---------------|
| `chord-analyze` | Identify chord quality, function, and extensions from notes or symbols | json |
| `chord-function` | Determine diatonic function (I, ii, V, etc.) in a given key | json |
| `scale-info` | Return scale degrees, modes, and characteristic intervals | json |
| `interval-calculate` | Compute intervals between pitches (consonance, inversion) | json |
| `voice-leading-check` | Evaluate voice leading quality between two chords | json |
| `key-detect` | Infer key from a set of chords or melody notes | json |
| `mode-identify` | Identify mode from a scale or progression | json |

### technique-agent

Physical guitar technique and fretboard authority.

| Tool | Purpose | Result Format |
|------|---------|---------------|
| `fretboard-position` | Map notes or chords to fretboard positions | json |
| `fingering-feasibility` | Assess whether a voicing is physically playable | json |
| `stretch-analysis` | Measure finger stretch requirements in frets and strings | json |
| `chord-voicing-options` | Generate alternate voicings for a given chord | json |
| `hand-position-transition` | Evaluate transition difficulty between positions | json |
| `barre-chord-analysis` | Identify barre requirements and alternatives | json |

### tab-agent

Tablature parsing, notation, and playability authority.

| Tool | Purpose | Result Format |
|------|---------|---------------|
| `tab-parse` | Parse ASCII tab into structured note events | json |
| `tab-to-notation` | Convert tab to standard notation | notation |
| `notation-to-tab` | Convert standard notation to tab | tab |
| `tab-playability-check` | Assess whether a tab is physically playable | json |
| `tab-timing-validate` | Validate rhythmic notation in tab | json |
| `tab-render` | Render tab as formatted text or image | tab |

### ga-musician

Audio, spectral, and synthesis authority (bridges to GA .NET music stack).

| Tool | Purpose | Result Format |
|------|---------|---------------|
| `spectral-analyze` | Perform FFT/spectral analysis on audio input | json |
| `synthesis-parameters` | Generate synthesis parameters for a target timbre | json |
| `pitch-detect` | Detect fundamental pitch from audio | json |
| `tempo-detect` | Extract tempo and beat grid from audio | json |
| `timbre-describe` | Describe timbral characteristics from spectrum | json |

### composer-agent

Composition and reharmonization authority.

| Tool | Purpose | Result Format |
|------|---------|---------------|
| `progression-generate` | Generate chord progressions in a key, mode, and style | json |
| `reharmonize` | Apply reharmonization techniques to an existing progression | json |
| `substitution-suggest` | Suggest substitutions (tritone, diatonic, chromatic mediant) | json |
| `melody-generate` | Generate melodic contours over a progression | json |
| `bass-line-generate` | Generate bass lines for a progression | json |
| `modal-interchange-suggest` | Propose borrowed chords from parallel modes | json |

### music-teacher

Pedagogy and curriculum authority.

| Tool | Purpose | Result Format |
|------|---------|---------------|
| `course-lookup` | Retrieve course modules by topic or skill level | json |
| `curriculum-sequence` | Order topics by prerequisite dependencies | json |
| `adaptive-difficulty` | Adjust lesson difficulty to learner level | json |
| `comprehension-assess` | Generate assessment questions for a concept | json |
| `gap-identify` | Identify knowledge gaps from learner history | json |
| `exercise-generate` | Create practice exercises for a learning objective | json |

### guitar-coach

Practice management and progress tracking authority.

| Tool | Purpose | Result Format |
|------|---------|---------------|
| `progress-track` | Record and retrieve learner progress data | json |
| `practice-routine-generate` | Build personalized practice routines | json |
| `goal-set` | Define short-term and long-term learning goals | json |
| `milestone-check` | Evaluate progress against milestones | json |
| `plateau-detect` | Identify stagnation patterns in practice data | json |
| `time-to-goal-estimate` | Forecast time required to reach a goal | json |

## Cross-Agent Tool Invocation

When an agent needs a tool owned by another agent, it MUST route via the orchestrator using the `mcp_tool_invocation` schema:

```json
{
  "tool_name": "fingering-feasibility",
  "parameters": { "voicing": ["x", "3", "2", "0", "1", "0"] },
  "agent_requesting": "composer-agent",
  "agent_executing": "technique-agent",
  "result_format": "json",
  "timeout_ms": 5000,
  "conversation_id": "…",
  "integrity": { … }
}
```

The orchestrator:
1. Validates that `tool_name` is listed under `agent_executing` in this contract.
2. Confirms `agent_requesting` has a legitimate need (via intent + conversation context).
3. Forwards the invocation to the executing agent.
4. Returns the `mcp_tool_result` to the requester.

## Common Cross-Agent Patterns

| Pattern | Requester | Executor | Tool |
|---------|-----------|----------|------|
| Reharmonization feasibility | composer-agent | technique-agent | fingering-feasibility |
| Theory-grounded lesson | music-teacher | theory-agent | chord-analyze, scale-info |
| Playable exercise generation | music-teacher | technique-agent | fingering-feasibility |
| Progress-aware curriculum | music-teacher | guitar-coach | progress-track |
| Tab rendering of composition | composer-agent | tab-agent | tab-render |
| Audio-to-theory analysis | theory-agent | ga-musician | pitch-detect, spectral-analyze |
| Technique drill routine | guitar-coach | technique-agent | stretch-analysis |
| Tab playability verification | tab-agent | technique-agent | fingering-feasibility |

## Violation Handling

| Violation | Response |
|-----------|----------|
| Agent invokes tool not in its mapping | Reject; log constitutional violation (Article 9); alert skeptical-auditor |
| Executing agent unavailable | Orchestrator returns `error_response` with `error_type: agent_unavailable` and suggests fallback |
| Tool execution exceeds timeout | Return `mcp_tool_result` with `status: timeout`; caller may retry with longer timeout up to schema maximum |
| Tool returns low confidence (< 0.5) | Result passes through; caller must respect confidence and seek confirmation or escalate |
| Tool returns contradictory truth (`C`) | Escalate to skeptical-auditor per hexavalent logic rules |

## Adding New Tools

To add a new MCP tool:

1. Identify the owning agent (must be exactly one).
2. Add the tool row to that agent's table in this contract.
3. If the tool requires a new persona, create the persona under `personas/` with the corresponding affordance.
4. Add a behavioral test under `tests/behavioral/` covering the tool invocation path.
5. Version-bump this contract (semver minor for additions).

Removal of tools requires the same process with explicit justification (per append-only constitution rules).

## References

- `schemas/a2a-protocol.schema.json` — message formats for all A2A communication
- `schemas/persona.schema.json` — persona format that grounds affordances
- `contracts/galactic-protocol.md` — parent protocol for cross-repo communication
- `constitutions/default.constitution.md` — Articles 7 (Auditability) and 9 (Bounded Autonomy)
- `policies/alignment-policy.yaml` — confidence thresholds and escalation rules
