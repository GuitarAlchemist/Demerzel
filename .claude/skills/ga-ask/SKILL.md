---
name: ga-ask
description: Ask a music theory or guitar question to the Guitar Alchemist AI agent. Routes to the appropriate tool bundle (theory, technique, tab, composer, ga-musician, teacher, coach) and returns a grounded answer. Use when the user asks "ask GA X", "what does the guitar agent say about X", or any music theory/guitar question directed at the GA ecosystem. Supports demo mode: invoke with "demo" or "examples" as the arg to see 3 curated example Q&As covering beginner theory, intermediate improvisation, and technique/injury scenarios.
---

# GA Ask — Query the Guitar Alchemist AI Agent

Ask a music theory, guitar technique, tablature, composition, synthesis, pedagogy, or practice question to the Guitar Alchemist (GA) AI agent. The agent uses the single-orchestrator + MCP tool-bundle architecture to answer grounded in computed music theory (not hallucinated).

## Architecture Context

GA uses **1 orchestrator LLM + 7 MCP tool bundles + shared blackboard state** per `contracts/ga-orchestrator-architecture.md` v2.0.0. Routing happens natively via LLM tool selection — no separate router/coordinator.

The 7 tool bundles:

| Bundle | Handles | Example Questions |
|--------|---------|-------------------|
| `theory-tools` | Chord analysis, scales, intervals, voice leading, key detection | "What notes in F#m7b5?", "What scale over Dm7?" |
| `technique-tools` | Fingering, ergonomics, stretch analysis, injury prevention | "Comfortable Bbmaj9 voicing?", "My wrist hurts after barre chords" |
| `tab-tools` | Tab parsing, notation conversion, playability check, transposition | "Parse this tab", "Transpose to Drop D" |
| `composer-tools` | Progression generation, reharmonization, substitution, modal interchange | "Jazz ii-V-I in C", "Reharmonize Autumn Leaves bridge" |
| `ga-musician-tools` | Spectral synthesis, Karplus-Strong, guitar profiles, tone analysis (external .NET runtime) | "How does Karplus-Strong model a plucked string?" |
| `teacher-tools` | Course lookup, curriculum sequencing, gap identification, adaptive difficulty | "What should I learn after CAGED?", "Explain modes for beginner" |
| `coach-tools` | Practice routine generation, progress tracking, plateau detection | "Design a daily practice routine", "Why am I not improving?" |

## How to Execute

### Step 1: Classify the User's Question

Determine which tool bundle(s) the question would invoke:
- **Single-bundle question**: "Notes in Cmaj7?" → theory-tools only
- **Multi-bundle question**: "Show comfortable Bbmaj9 voicing with fingering" → theory-tools + technique-tools
- **Ambiguous**: "Tell me about Cmaj7" → ask clarification OR default to theory-tools with note
- **Out of domain**: "What's the weather?" → decline per constitutional Article 1

### Step 2: Check MCP Server Availability

The GA MCP server provides live computation via tools. Check if it's reachable:

```bash
# If GA MCP server is configured as an MCP server in this Claude Code session,
# the tools will be available as mcp__ga__* in ToolSearch.
# Search for them:
```

Use ToolSearch with query "ga music theory" to find any available GA MCP tools.

**If MCP server is available**: Call the appropriate tools directly and compose the answer from tool outputs.

**If MCP server is NOT available** (fallback mode per directive DIR-2026-03-21-002):
- Answer from Demerzel governance artifacts: grammars in `grammars/music-*.ebnf`, FAQ in `state/streeling/faq/music-theory-faq.md`, courses in `state/streeling/courses/*/en/*.md`
- Prefix response with: "Note: Answering from static governance data (MCP server unreachable). Live computation unavailable."

### Step 3: Ground the Answer

When answering, follow the orchestrator test cases in `tests/behavioral/ga-orchestrator-cases.md`:

- **TC-ORC-01 style**: Direct theory answer with correct notes, intervals, spellings. Cite `grammars/music-theory.ebnf` productions used.
- **TC-ORC-02 style**: Multi-tool compound answer. Theory provides notes, technique provides fingering/comfort, merged response explains the combined picture.
- **TC-ORC-03 style**: Multi-turn refinement. Read blackboard state from `state/ga-sessions/` if a session_id is provided.
- **TC-ORC-04 style**: Out-of-domain decline. Do not fabricate.
- **TC-ORC-09 style**: Malformed data handling. Don't fabricate missing fields.
- **TC-ORC-10 style**: Conflicting results surface with hexavalent C (contradictory) truth value.

### Step 4: Apply Constitutional Constraints

Every answer MUST comply with:
- **Article 1 (Truthfulness)**: No fabrication. If uncertain, say so with hexavalent U (unknown).
- **Article 2 (Transparency)**: Show reasoning and tool calls made.
- **Article 7 (Auditability)**: Log which tools/sources were consulted.
- **Confidence thresholds**: Per `policies/alignment-policy.yaml`. Below 0.7 → add confidence note. Below 0.5 → ask clarification.

### Step 5: Format the Response

Structure the answer:

```markdown
## Answer

[Direct response to the question]

## Reasoning

[Brief explanation — intervals, voice leading, fingering rationale, etc.]

## Tools Consulted

- `theory-tools.chord-analyze` (if MCP available) OR
- `grammars/music-theory.ebnf` § Section 1 (Chord Construction) (fallback)
- `state/streeling/faq/music-theory-faq.md` Q7 (if applicable)

## Confidence

T(0.92) — verified computation, standard music theory
```

## Quick Invocation Patterns

**User says**: "Ask GA what chord notes are in F#m7b5"
→ Route to theory-tools, return notes + intervals + enharmonic context

**User says**: "What does the guitar agent say about comfortable voicings for Bbmaj9?"
→ Multi-tool: theory (notes) + technique (comfort)

**User says**: "GA, design me a 20-minute practice routine for modal improvisation"
→ coach-tools + teacher-tools

**User says**: "Does GA have ear training exercises for identifying major 7 chords?"
→ teacher-tools lookup, reference `state/streeling/courses/guitar-alchemist-academy/en/gaa-002-training-your-ear.md`

## Validated Fallback Lookups (no MCP required)

Tested 2026-04-04 — these work in pure-fallback mode without the GA MCP server:

### Chord construction → theory-tools fallback
- Source: `grammars/music-theory.ebnf` § chord_construction (quality terminal)
- Grep pattern: `grep -B1 -A3 "<chord-quality>" grammars/music-theory.ebnf`
- Compute intervals manually: root + semitone offsets (m3=3, M3=4, P5=7, d5=6, m7=10, M7=11, M9=14)

### Voicing lookup → theory + technique fallback
- Source: `grammars/music-theory.ebnf` § jazz_voicing + `state/streeling/courses/music/en/mus-005-jazz-harmony.md` § Section 3
- Known voicing shapes (rootless A/B, drop-2 string sets 6-5-4-3, 5-4-3-2, 4-3-2-1)

### Practice routine → coach + teacher fallback
- Source: `state/streeling/courses/guitar-alchemist-academy/en/gaa-003-improvisation-foundations.md` for improv
- Source: `state/streeling/courses/guitar-alchemist-academy/en/gaa-002-training-your-ear.md` § Daily Habit framework (10-15 min cycles)

### Out-of-domain decline → constitutional check
- Article 1 (Truthfulness): do not fabricate
- Article 9 (Bounded Autonomy): decline politely, suggest in-domain alternatives

## Response Format (from validation)

Structure responses this exact way for consistency:

```markdown
**Answer**: [direct, concrete — notes/voicing/exercise]

**Reasoning**:
- [theory/computation shown]
- [multi-tool explanation if multi-bundle]

**Tools consulted**:
- [specific grammar file § section] OR
- [course file § section] OR
- [FAQ file § question]

**Confidence**: T/P/U/D/F/C(0.NN) — [one-line justification]
```

Always cite file § section so users can verify.

## Example Test Scenarios

From `tests/behavioral/ga-orchestrator-cases.md`, these are the scenarios to handle gracefully:

1. **Simple theory** (TC-ORC-01): "What are the notes in F#m7b5?"
2. **Multi-bundle** (TC-ORC-02): "Comfortable Bbmaj9 voicing with fingering"
3. **Multi-turn** (TC-ORC-03): "Simpler voicing" (references prior turn)
4. **Out of domain** (TC-ORC-04): "What's the weather today?"
5. **5-turn context** (TC-ORC-05): Conversation preservation
6. **Skill adaptation** (TC-ORC-06): Beginner vs advanced responses
7. **Tool failure** (TC-ORC-07): Graceful degradation
8. **Streaming** (TC-ORC-08): Partial response streaming
9. **Malformed tool data** (TC-ORC-09): No fabrication
10. **Conflicting results** (TC-ORC-10): Surface with C truth value
11. **Token pruning** (TC-ORC-11): Compact context without losing preferences

## Configuration

- **GA MCP server**: Configured per `contracts/directives/ga-mcp-integration.directive.md` (DIR-2026-03-21-002)
- **Fallback data sources**: `grammars/music-*.ebnf`, `state/streeling/faq/*`, `state/streeling/courses/*/en/*.md`
- **Session persistence**: `state/ga-sessions/<session_id>.json` conforming to `schemas/blackboard-state.schema.json`
- **Personas**: `personas/composer-agent.persona.yaml`, `personas/music-teacher.persona.yaml`, `personas/guitar-coach.persona.yaml` (capability bundle docs)

## Not This Skill's Job

- **Running the GA chatbot server** → use `ga-ralph` skill
- **Building new GA features** → use `ga-ralph` skill
- **Modifying GA code** → go to the ga repo directly
- **Governance audits** → use `demerzel-audit` skill

## Demo Mode

When the user invokes the skill with "demo", "examples", "show me", or no specific question, run the 3 curated demo questions below. These showcase single-bundle, multi-bundle, and injury-safety routing.

Present each demo as a separate mini-response, formatted exactly like a real answer.

### Demo 1: Beginner Theory (Single Bundle — theory-tools)

**Question**: *"What notes are in a Dm7 chord?"*

**Answer**: Dm7 contains **D, F, A, C**.

**Reasoning**:
- D (root) + F (minor 3rd, 3 semitones) = minor triad foundation
- + A (perfect 5th, 7 semitones) = complete minor triad
- + C (minor 7th, 10 semitones) = Dm7 (the "jazz" minor seventh)

This is the **ii chord in C major** — everywhere in jazz as the start of ii-V-I (Dm7 → G7 → Cmaj7).

**Guitar positions** (standard tuning):
- Open: `x-x-0-2-1-1`
- Barre at 5th fret: `5-5-3-5-3-5`
- Rootless jazz voicing (A-D-G-B strings, 5th fret area): `5-3-5-6`

**Tools consulted**:
- `grammars/music-theory.ebnf` § chord_construction (quality: minor_7)
- `state/streeling/courses/music/en/mus-005-jazz-harmony.md` § 2 (ii-V-I Universe)

**Confidence**: T(0.98) — fundamental music theory

---

### Demo 2: Intermediate Improvisation (Multi-Bundle — theory + composer)

**Question**: *"What scale should I use to solo over Cm7-F7-Bbmaj7?"*

**Answer**: This is a **ii-V-I in Bb major**. Two approaches:

**Option A (simple)**: Use **Bb major** throughout — always works.

**Option B (more color)**:
| Chord | Scale | Characteristic |
|-------|-------|----------------|
| Cm7 | C Dorian | Natural 6th (A) |
| F7 | F Mixolydian | b7 dominant sound |
| Bbmaj7 | Bb Lydian | #4 (E) jazz brightness |

**Advanced tension**: Over F7, try **F altered** (7th mode of Gb melodic minor) for maximum pre-resolution pull.

**Practice tip** (from gaa-003 § 4): Target the **3rd of each chord on beat 1** (Eb→A→D). Ear hears the changes move.

**Tools consulted**:
- `grammars/music-theory.ebnf` § chord_scale_pair, melodic_minor_mode
- `state/streeling/courses/music/en/mus-005-jazz-harmony.md` § 6 (Chord-Scale Theory)
- `state/streeling/courses/guitar-alchemist-academy/en/gaa-003-improvisation-foundations.md` § 4 (Chord-Tone Targeting)

**Confidence**: T(0.92) — standard jazz pedagogy

---

### Demo 3: Technique/Injury Prevention (Single Bundle — technique-tools, Article 1 priority)

**Question**: *"My pinky finger gets tired after 10 minutes of barre chords. What should I do?"*

**Answer**: **Stop and rest for now.** Pinky fatigue after 10 minutes of barres is common and fixable, but pushing through risks tendon strain.

**Immediate checks**:
1. **Thumb position** — behind the neck (opposite middle finger), NOT wrapped over top
2. **Wrist angle** — close to straight, not bent
3. **Grip pressure** — barely enough for clean notes, not a death grip

**Structural fixes**:
| Issue | Fix |
|-------|-----|
| Pinky overworking | Let index do the full barre; pinky presses only one string |
| Endurance gap | Build with 2-min on / 2-min rest cycles, 5 rounds |
| High action | Consider lowering string height — easier on fretting hand |

**Red flags — see a hand therapist if**: persistent pain after rest, numbness/tingling, swelling, night pain, weakness lifting objects.

**Tools consulted**:
- `tests/behavioral/technique-agent-cases.md` § TC-TA-02 (injury prevention), TC-TA-03 (stretch analysis)
- `grammars/music-guitar-technique.ebnf` § technique

**Confidence**: T(0.85) — standard guitar pedagogy. Not medical advice.

---

### After the 3 demos

Finish with:

> Those 3 examples show how ga-ask routes to different tool bundles. Try asking your own question — any music theory, guitar technique, tab parsing, composition, synthesis, pedagogy, or practice topic. I'll cite sources and compute from first principles when the MCP server is offline.

## See Also

- `contracts/ga-orchestrator-architecture.md` — the architecture this skill queries
- `contracts/ga-mcp-tool-bundles.md` — detailed tool bundle specs
- `contracts/a2a-mcp-routing.md` — agent→tool ownership map
- `tests/behavioral/ga-orchestrator-cases.md` — 11 behavioral test cases
- `state/streeling/faq/music-theory-faq.md` — curated Q&A fallback
