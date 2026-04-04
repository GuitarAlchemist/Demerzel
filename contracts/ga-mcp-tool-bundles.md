# GA MCP Tool Bundles

Version: 1.0.0
Effective: 2026-04-04
Parent: `contracts/ga-orchestrator-architecture.md`

## Purpose

Specify the seven MCP tool bundles that the GA orchestrator LLM invokes. Each bundle wraps one music domain. Tool bundles have no private state; blackboard is read-only shared state accessible to all bundles. They receive arguments, optionally read the blackboard, and return structured results.

The orchestrator chooses bundles via **natural LLM tool-selection** driven by the tool descriptions below. No custom router.

## Bundle Invocation Contract

All tools share this envelope:

```json
{
  "bundle": "theory-tools",
  "tool": "chord-analyze",
  "arguments": { ... },
  "session_id": "uuid",
  "blackboard_read_keys": ["user_profile.skill_level", "current_focus.chord"]
}
```

All tool results share:

```json
{
  "status": "success|error|partial|timeout",
  "data": { ... },
  "confidence": 0.0-1.0,
  "truth_value": "T|P|U|D|F|C",
  "duration_ms": 123,
  "fallback_hint": "optional human-readable suggestion"
}
```

## Selection Heuristics (for the orchestrator)

- **Pure harmony/theory question** → `theory-tools` only
- **Playability / fingering / fretboard** → `technique-tools`
- **Tab input/output** → `tab-tools`
- **Generate music** → `composer-tools` (usually chained with `theory-tools` for validation, `technique-tools` for playability)
- **Audio in/out, spectral** → `ga-musician-tools`
- **Lesson/curriculum/assessment** → `teacher-tools`
- **Practice plan/goal/progress** → `coach-tools`
- **Out-of-domain** → decline, call no tools

When multiple domains apply, the orchestrator calls tools **in parallel** if independent, **sequentially** if one result feeds another (e.g., theory answer → technique feasibility check).

---

## Bundle 1: `theory-tools`

**Description (orchestrator-facing):** "Harmonic and melodic theory authority. Use for chord analysis, scale/mode info, key detection, voice leading, interval calculations, and functional harmony questions. Do NOT use for playability, tab, or audio."

| Tool | When to Invoke | Inputs | Outputs |
|------|----------------|--------|---------|
| `chord-analyze` | User names a chord or asks what a symbol means | `{chord: string, key?: string}` | `{quality, root, extensions, function, notes[]}` |
| `chord-function` | User asks "what role does this chord play" | `{chord, key}` | `{function: "I"\|"ii"\|"V"\|..., tendency}` |
| `scale-info` | User asks about a scale, mode, or its degrees | `{scale: string}` | `{degrees[], intervals[], modes[], characteristic_notes[]}` |
| `interval-calculate` | User asks about distance between notes | `{from: string, to: string}` | `{interval, inversion, consonance}` |
| `voice-leading-check` | Composer flow, or user asks about smooth motion | `{from_chord, to_chord}` | `{score, issues[], suggested_fixes[]}` |
| `key-detect` | User provides chords/notes and asks the key | `{chords[] \| notes[]}` | `{key, confidence, alternatives[]}` |
| `mode-identify` | User asks "what mode is this" | `{notes[] \| chords[]}` | `{mode, parent_scale, confidence}` |

**Fallback:** If a symbol cannot be parsed, return `status: "error"` with `fallback_hint: "Could not parse chord symbol '...'. Try forms like 'Cmaj7', 'F#m7b5'."`

---

## Bundle 2: `technique-tools`

**Description:** "Physical guitar technique and fretboard authority. Use for fingering feasibility, voicing options, stretch analysis, barre chords, and hand-position transitions. Reads `user_profile.hand_size` and `user_profile.tuning` from blackboard. Do NOT use for pure theory or audio."

| Tool | When to Invoke | Inputs | Outputs |
|------|----------------|--------|---------|
| `fretboard-position` | Map notes to fretboard | `{notes[], tuning?}` | `{positions: [{string, fret}]}` |
| `fingering-feasibility` | Validate a voicing is playable | `{voicing[], hand_size?}` | `{playable: bool, difficulty, issues[]}` |
| `stretch-analysis` | Assess stretch | `{voicing[], hand_size?}` | `{max_stretch_frets, strain_score}` |
| `chord-voicing-options` | User wants voicings for a chord | `{chord, skill_level?, tuning?, complexity?, exclude?}` | `{voicings: [{fingering, difficulty, fret_range}]}` |
| `hand-position-transition` | Moving between positions | `{from_position, to_position}` | `{difficulty, smooth: bool, intermediate_positions[]}` |
| `barre-chord-analysis` | User asks about barre chords | `{chord, shape?}` | `{barre_required, alternatives[], difficulty}` |

**Fallback:** If voicing is unplayable for stated hand size, suggest 2–3 simpler alternatives.

---

## Bundle 3: `tab-tools`

**Description:** "Tablature parsing, rendering, and conversion. Use when user provides ASCII tab, asks for a tab to be rendered, or wants tab↔notation conversion. Do NOT use for generating new music (use composer-tools)."

| Tool | When to Invoke | Inputs | Outputs |
|------|----------------|--------|---------|
| `tab-parse` | User pastes ASCII tab | `{ascii_tab: string}` | `{events: [{string, fret, duration, tie?}]}` |
| `tab-to-notation` | Convert tab to staff notation | `{tab_events[]}` | `{musicxml: string}` |
| `notation-to-tab` | Convert staff to tab | `{musicxml, tuning?}` | `{ascii_tab: string}` |
| `tab-playability-check` | Validate tab is playable | `{tab_events[]}` | `{playable: bool, problems[]}` |
| `tab-timing-validate` | Check rhythmic correctness | `{tab_events[]}` | `{valid: bool, timing_issues[]}` |
| `tab-render` | Pretty-print tab | `{tab_events[], width?}` | `{rendered: string}` |

**Fallback:** If ASCII is ambiguous, return best-effort parse with `truth_value: "P"` and flag ambiguous measures.

---

## Bundle 4: `composer-tools`

**Description:** "Composition and reharmonization. Use when user asks to generate progressions, melodies, bass lines, or reharmonize. Often chain with theory-tools (validation) and technique-tools (playability)."

| Tool | When to Invoke | Inputs | Outputs |
|------|----------------|--------|---------|
| `progression-generate` | "Give me a progression in..." | `{key, mode?, style?, length?, mood?}` | `{progression[], rationale}` |
| `reharmonize` | User has progression, wants variation | `{progression[], technique?}` | `{reharmonized[], changes_made[]}` |
| `substitution-suggest` | "What can replace this chord" | `{chord, key, context?}` | `{substitutions: [{chord, type, effect}]}` |
| `melody-generate` | "Write a melody over..." | `{progression[], style?, range?}` | `{melody_notes[], rhythm[]}` |
| `bass-line-generate` | "Give me a bass line" | `{progression[], style?}` | `{bass_notes[], rhythm[]}` |
| `modal-interchange-suggest` | "What borrowed chords fit" | `{key, mode}` | `{borrowed_chords[], from_mode}` |

**Fallback:** If style is unknown, default to "common practice" and flag assumption in `fallback_hint`.

---

## Bundle 5: `ga-musician-tools`

**Description:** "Audio, spectral, synthesis bridge to the GA .NET music stack. Use when user provides audio or asks about timbre, pitch, tempo, or spectral content. Do NOT use for written music analysis."

**External Runtime Adapter**: Unlike the other 6 bundles (which are pure-function reasoning tools), `ga-musician-tools` wraps the external .NET audio synthesis stack (GA.Business.ML + Karplus-Strong engine). This bundle has different semantics:
- **Latency budget**: up to 5s for spectral analysis, 2s for synthesis (vs 500ms for reasoning tools)
- **Failure mode**: network/IPC failures possible (reasoning tools only fail on malformed input)
- **Async**: may return partial results streamed over time
- **Stateless in MCP interface, but backed by a stateful DSP service**

| Tool | When to Invoke | Inputs | Outputs |
|------|----------------|--------|---------|
| `spectral-analyze` | Audio input provided | `{audio_ref}` | `{spectrum, peaks[], centroid}` |
| `synthesis-parameters` | "Make it sound like X" | `{target_timbre}` | `{synth_params}` |
| `pitch-detect` | Extract pitch from audio | `{audio_ref}` | `{pitch_hz, note, confidence}` |
| `tempo-detect` | Extract tempo/beat | `{audio_ref}` | `{bpm, beat_grid[]}` |
| `timbre-describe` | Describe tone | `{spectrum}` | `{descriptors[]}` |

**Fallback:** If audio is missing or unreadable, return `error` and suggest file-format requirements.

---

## Bundle 6: `teacher-tools`

**Description:** "Pedagogy, curriculum, assessment. Use when user wants to learn a concept, asks for a lesson, needs an exercise, or requests an assessment. Reads `user_profile.skill_level` from blackboard."

| Tool | When to Invoke | Inputs | Outputs |
|------|----------------|--------|---------|
| `course-lookup` | "Is there a course on X" | `{topic, skill_level?}` | `{modules[]}` |
| `curriculum-sequence` | "What should I learn first" | `{topics[], skill_level}` | `{ordered_sequence[], prereqs}` |
| `adaptive-difficulty` | Adjust a lesson to learner | `{lesson, skill_level}` | `{adapted_lesson}` |
| `comprehension-assess` | "Quiz me on X" | `{concept, skill_level}` | `{questions[], rubric}` |
| `gap-identify` | Find what user doesn't know | `{topic, user_history}` | `{gaps[]}` |
| `exercise-generate` | "Give me an exercise for X" | `{objective, skill_level, duration?}` | `{exercise, instructions, success_criteria}` |

**Fallback:** If topic is out of syllabus, return `status: "partial"` with closest available topic.

---

## Bundle 7: `coach-tools`

**Description:** "Practice management, goal-setting, progress tracking. Use when user wants a practice routine, sets a goal, asks about progress, or mentions a plateau."

| Tool | When to Invoke | Inputs | Outputs |
|------|----------------|--------|---------|
| `progress-track` | Record/retrieve progress | `{user_id, metric?, period?}` | `{progress_data[]}` |
| `practice-routine-generate` | "Build me a practice plan" | `{goals[], duration_min, skill_level}` | `{routine: {segments[]}}` |
| `goal-set` | "I want to learn X in Y weeks" | `{goal, timeframe}` | `{goal_record, milestones[]}` |
| `milestone-check` | "Am I on track" | `{goal_id}` | `{status, percent_complete, next_milestone}` |
| `plateau-detect` | Identify stagnation | `{user_history}` | `{plateau: bool, duration, suggestions[]}` |
| `time-to-goal-estimate` | Forecast completion | `{goal_id, current_progress}` | `{estimated_weeks, confidence}` |

**Fallback:** If user history is empty, propose a baseline assessment first.

---

## Blackboard Access Policy

- Tool bundles MAY read `user_profile` and `current_focus` to personalize responses.
- Tool bundles MUST NOT write to the blackboard — only the orchestrator mutates state.
- Any arguments normally drawn from blackboard (e.g., `tuning`, `skill_level`) MAY be overridden by explicit tool arguments.

## Failure & Degradation

| Situation | Orchestrator Behavior |
|-----------|-----------------------|
| Tool returns `error` | Explain, offer partial answer from own knowledge, log in blackboard |
| Tool returns `timeout` | Retry once with longer timeout; if still failing, proceed without it |
| Tool returns `truth_value: C` | Surface the contradiction to user; escalate if blocking |
| Tool returns `confidence < 0.5` | Mark response as tentative; invite user confirmation |
| Out-of-domain request | Decline without calling tools |

## Versioning

Bundle tool signatures are semver-stable. Adding tools = minor bump. Removing or changing signatures = major bump with deprecation window.

## References

- `contracts/ga-orchestrator-architecture.md` — overall architecture
- `schemas/blackboard-state.schema.json` — session state
- `contracts/a2a-mcp-routing.md` — tool ownership mapping (authoritative)
- `personas/*.persona.yaml` — capability bundle descriptions
