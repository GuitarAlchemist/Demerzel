# Behavioral Tests: GA Orchestrator (Single-Agent + Tool Bundles)

Version: 1.0.0
Effective: 2026-04-04
Architecture: `contracts/ga-orchestrator-architecture.md`
Blackboard: `schemas/blackboard-state.schema.json`
Bundles: `contracts/ga-mcp-tool-bundles.md`

## Scope

Validate the pivoted architecture: one orchestrator LLM, seven MCP tool bundles, one blackboard. Each test exercises orchestrator tool-selection, blackboard read/write, streaming, and graceful degradation.

All tests report a **hexavalent outcome** (T/P/U/D/F/C) in addition to pass/fail.

---

## TC-ORC-01: Simple theory question → theory-tools only

**Given** a fresh session (no prior turns) and `user_profile.skill_level = "intermediate"`.

**When** the user asks: *"What are the notes in Cmaj7?"*

**Then**
- Orchestrator calls exactly one tool: `theory-tools.chord-analyze` with `{chord: "Cmaj7"}`.
- No call to `technique-tools`, `tab-tools`, or any other bundle.
- Response names the notes (C, E, G, B) and optionally the chord quality.
- `conversation_turns[0].tools_called` has length 1.
- `confidence >= 0.9`, `truth_value = "T"`.

**Pass** if exactly one tool call to theory-tools and answer is correct.
**Fail** if multiple tools called or wrong notes.
**Hexavalent outcome:** T (verified against music theory canon).

---

## TC-ORC-02: Compound request → theory-tools then technique-tools, merged answer

**Given** `user_profile = { skill_level: "intermediate", hand_size: "medium", tuning: "standard" }`.

**When** the user asks: *"Show me a comfortable Bbmaj9 voicing with fingering."*

**Then**
- Orchestrator calls `theory-tools.chord-analyze` for `Bbmaj9` (to get the notes).
- Orchestrator then calls `technique-tools.chord-voicing-options` with `{chord: "Bbmaj9", skill_level: "intermediate", hand_size: "medium"}`.
- Response merges: names the chord tones AND gives a specific playable voicing with fingering.
- Blackboard `current_focus` updated: `{chord: "Bbmaj9", voicing: [...], last_updated_turn: 0}`.
- Both tool results have `confidence >= 0.8`.

**Pass** if both tools called in the right order AND the voicing is playable for medium hand.
**Fail** if only one tool called, or voicing is infeasible (stretch > 5 frets for medium hand).
**Hexavalent outcome:** T if voicing verified playable, P if plausible but unverified.

---

## TC-ORC-03: Multi-turn refinement via blackboard

**Given** the blackboard state from end of TC-ORC-02 (`current_focus.chord = "Bbmaj9"`, prior voicing recorded).

**When** the user (on turn 2) says: *"Give me a simpler voicing."*

**Then**
- Orchestrator reads blackboard, identifies referent chord `Bbmaj9` from `current_focus`.
- Orchestrator calls `technique-tools.chord-voicing-options` with `{chord: "Bbmaj9", complexity: "simpler", exclude: [prior_voicing]}`.
- Returned voicing is **different** from turn 1's voicing AND has lower `difficulty` score.
- Blackboard `current_focus.voicing` updated to new voicing, `last_updated_turn = 1`.
- No need to re-ask user what chord.

**Pass** if orchestrator correctly resolves "simpler voicing" to Bbmaj9 from blackboard AND returns a distinct, simpler voicing.
**Fail** if orchestrator asks "simpler voicing of what?" or returns same voicing.
**Hexavalent outcome:** T if blackboard continuity works; F if orchestrator loses context.

---

## TC-ORC-04: Out-of-domain request → decline, no tool calls

**Given** any session state.

**When** the user asks: *"What's the weather in Seattle?"*

**Then**
- Orchestrator calls **zero** tools.
- Response politely declines, states this is outside the GA music-assistant scope.
- `conversation_turns[n].tools_called` is empty array.
- No blackboard focus mutation.
- Constitutional Article 9 (Bounded Autonomy) honored.

**Pass** if zero tool calls and clean decline.
**Fail** if any tool invoked OR if orchestrator fabricates weather info.
**Hexavalent outcome:** T (correctly declined).

---

## TC-ORC-05: Context preservation across 5 turns

**Given** a fresh session.

**When** the user has this 5-turn conversation:
1. "I play fingerstyle acoustic in drop D."
2. "What scale works over a D-A-G progression?"
3. "Show me a lick using that scale."
4. "Make it fingerstyle-friendly."
5. "What was the first chord I mentioned?"

**Then**
- After turn 1: `user_profile.preferred_genre` includes "fingerstyle", `user_profile.tuning = "drop-d"`, `user_profile.instrument = "acoustic"`. `learned_context` contains at least these facts.
- Turn 2: Orchestrator calls `theory-tools.scale-info` and/or `theory-tools.key-detect` using the progression; scale answer matches drop-D context.
- Turn 3: Orchestrator calls `composer-tools.melody-generate` with the scale from turn 2.
- Turn 4: Orchestrator calls `technique-tools` to adapt lick for fingerstyle (reads `preferred_genre` from blackboard).
- Turn 5: Orchestrator answers "D" correctly by reading `conversation_turns[1].user_input` or `current_focus` history.

**Pass** if all 5 turns chain correctly AND turn 5 answers from blackboard history without re-asking.
**Fail** if any turn loses prior context OR asks redundant clarifying questions.
**Hexavalent outcome:** T if 5/5 turns succeed, P if 3–4/5, F if <3/5.

---

## TC-ORC-06: Skill-level adaptation

**Given** two parallel sessions with identical queries but different profiles:
- Session A: `user_profile.skill_level = "beginner"`
- Session B: `user_profile.skill_level = "advanced"`

**When** both ask: *"How do I play a Bm chord?"*

**Then**
- Session A response: simple open-position or mini-barre voicing (e.g., Bm7 easy shape or partial barre), with extra explanation of barre technique. `technique-tools.chord-voicing-options` called with `skill_level: "beginner"`.
- Session B response: full barre or extended voicing with chord-function context (Bm as vi of D, iv of F#m, etc.). May include theory-tools call.
- Both voicings are **distinct** and appropriate to skill.

**Pass** if responses materially differ in complexity and both are correct.
**Fail** if both responses identical OR if beginner gets advanced content.
**Hexavalent outcome:** T if adaptation verified, P if differences present but borderline.

---

## TC-ORC-07: Tool failure → graceful degradation

**Given** a session where `technique-tools` is simulated as unavailable (timeout or 503).

**When** the user asks: *"Give me a playable voicing for F#m7b5."*

**Then**
- Orchestrator attempts `technique-tools.chord-voicing-options`, receives `status: "timeout"` or `"error"`.
- Orchestrator retries once.
- On second failure, orchestrator:
  - Calls `theory-tools.chord-analyze` to at least name the chord tones.
  - Explicitly tells user the voicing engine is unavailable.
  - Offers either its own best-effort voicing (marked as unverified, `truth_value: "P"`) OR invites user to retry later.
- `conversation_turns[n].tools_called` records both the failed attempt and the fallback theory-tools call.
- Blackboard `learned_context` optionally logs the failure for observability.

**Pass** if orchestrator degrades gracefully, surfaces the failure, and does NOT fabricate a verified voicing.
**Fail** if orchestrator pretends the tool succeeded OR returns a fabricated voicing marked as `truth_value: "T"`.
**Hexavalent outcome:** T (correct graceful degradation) or P (best-effort with acknowledged uncertainty).

---

## TC-ORC-08: Streaming partial responses

**Given** a session connected via streaming (SSE/WebSocket).

**When** the user asks: *"Write a 16-bar jazz progression in F with bass line and render as tab."*

**Then**
- Orchestrator begins streaming a response ("Working on a 16-bar progression...").
- Orchestrator calls `composer-tools.progression-generate` — streaming pauses.
- Tokens resume after the call, streaming the progression.
- Orchestrator calls `composer-tools.bass-line-generate` — streaming pauses briefly.
- Streaming resumes with bass line.
- Orchestrator calls `tab-tools.tab-render` (possibly streaming its output in chunks).
- User sees progressive output in real time, not one big final blob.
- Total perceived latency to first token < 2s; each tool-induced pause < 5s.

**Pass** if streaming is progressive, tool pauses are visible but brief, and final output is complete.
**Fail** if all output arrives as a single block at the end OR if streaming breaks mid-response.
**Hexavalent outcome:** T if progressive stream verified, P if partial streaming works but with gaps.

---

## TC-ORC-09: Malformed Tool Data

**Given:** `theory-tools` returns a JSON payload that violates its own output schema (e.g., missing required `notes[]`, wrong types, or extra unknown fields).

**When:** The orchestrator receives the malformed response.

**Then**
- Orchestrator treats the response as `status: "error"`.
- Orchestrator does **NOT** fabricate the missing fields from its own guesses.
- Orchestrator surfaces a graceful error to the user ("I couldn't get a valid answer from the theory engine for this chord — try rephrasing or retrying").
- The malformed payload is logged for audit in `conversation_turns[].tools_called` with a schema-validation error note.
- Hexavalent: **F** (tool output refuted by schema validation).

**Pass** if no fabrication occurs and the error is surfaced clearly to the user and to the audit log.
**Fail** if orchestrator invents values to fill missing fields OR responds as if the tool succeeded.
**Hexavalent outcome:** F (schema-refuted output handled correctly).

---

## TC-ORC-10: Conflicting Tool Results

**Given:** `theory-tools.chord-analyze` says `Bbmaj9` has 5 notes (Bb, D, F, A, C); `technique-tools.chord-voicing-options` returns a 4-note voicing (Bb, D, A, C — omits the 5th, F).

**When:** The orchestrator integrates both responses into a single reply.

**Then**
- Orchestrator surfaces `truth_value: C` (contradictory) on the merged turn.
- Orchestrator explains the voicing intentionally omits the 5th as a common jazz-voicing compression.
- BOTH perspectives are presented to the user — the full theoretical chord AND the compressed playable voicing — rather than silently dropping one.
- Hexavalent: **C** (conflicting evidence between bundles).

**Pass** if no silent override and user sees both the theoretical analysis and the practical voicing with explanation.
**Fail** if orchestrator silently picks one bundle's answer and hides the conflict, OR if it reports `truth_value: T`.
**Hexavalent outcome:** C (conflict correctly surfaced).

---

## TC-ORC-11: Token Budget Context Pruning

**Given:** A 40-turn session approaching the orchestrator's token limit.

**When:** The orchestrator must prune context to stay within budget.

**Then**
- Orchestrator summarizes `conversation_turns[]` older than 10 turns into a single synthetic turn (preserving salient facts).
- `learned_context` is preserved in full.
- `user_preferences.never_suggest` is preserved in full.
- `displayed_artifacts` is preserved in full.
- A pruning event is logged (timestamp, turns summarized, tokens reclaimed) for audit.
- Hexavalent: **T** (successful compaction).

**Pass** if no loss of user preferences, learned context, or artifact history after pruning.
**Fail** if any preference, learned fact, or displayed artifact is dropped OR if pruning is not logged.
**Hexavalent outcome:** T (safe compaction verified).

---

## Cross-Test Invariants

Across all tests, the orchestrator MUST:

- Only call tools in the 7 approved bundles (Article 9).
- Log every tool call in `conversation_turns[].tools_called` (Article 7).
- Not fabricate tool results (Article 1).
- Respect `confidence < 0.5` by flagging uncertainty (policy: alignment thresholds).
- Never mutate the blackboard from within a tool — only the orchestrator writes.
- Update `updated_at` and `turn_index` correctly each turn.

## Escalation

Any test scoring **F** or **C** (hexavalent) triggers:
- Issue filed in GA repo with the failing transcript.
- Alert to `skeptical-auditor` persona.
- Blocker on merging changes to orchestrator prompt until remediated.

## References

- `contracts/ga-orchestrator-architecture.md`
- `contracts/ga-mcp-tool-bundles.md`
- `schemas/blackboard-state.schema.json`
- `policies/alignment-policy.yaml`
- `constitutions/default.constitution.md` (Articles 1, 7, 9)
