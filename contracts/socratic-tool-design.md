# Socratic Tool Design Pattern

**Version:** 1.0.0
**Status:** Active
**Department:** Guitar Alchemist / Context Stewardship
**Applies to:** All MCP tools in the GA ecosystem

---

## 1. The Paradox

**More data returned = less capability.**

Every token a tool spends on enumeration is a token stolen from the LLM's reasoning capacity. The current `GetAvailableInstruments()` tool returning 114 instrument names is not a feature — it's a design failure. The tool should have decided something on the caller's behalf.

Tools that dump lists treat the LLM as if it were a human scrolling through a UI. But Claude doesn't scroll. Claude reasons over what's present. A catalog in context is a confession that the tool couldn't decide.

**Socratic Tools** invert this: tools refuse to list. Instead, they return questions, disambiguations, or computed answers. The payload IS the next turn.

---

## 2. The Three Core Patterns

### Pattern A: Resolution Pattern (Tools That Refuse to List)

Replace `list_X()` with `resolve_X(hint)`. Returns ONE item + a short disambiguation prompt if ambiguous.

**Before:**
```
GetAvailableInstruments()
→ Baglama, Bajo, Balalaika, Bandola, Bandolim, Bandora, Bandurria, Banjo,
  Banjolin, Banjourine, BaritoneGuitar, BassGuitar, Bordonua, Bouzouki...
  [114 total]
Token cost: ~2,000
```

**After:**
```
resolve_instrument(hint="guitar")
→ "Guitar (6-string, Standard tuning). Narrow with: 'baritone', 'bass',
   '7-string', 'acoustic', 'nylon', or specify tuning like 'DADGAD'."
Token cost: ~50
```

**Ambiguous hint:**
```
resolve_instrument(hint="balalaika")
→ "Balalaika Prima (3-string, E4-E4-A4 tuning).
   Alternatives: Alto, Bass, Contrabass, Piccolo, Sekunda."
Token cost: ~40
```

The tool does the winnowing Claude would otherwise do with 114 rows in context.

### Pattern B: Socratic Pattern (Response-as-Question)

Tool returns a question + 2-3 narrowing options. The payload is the next turn.

**Before:**
```
GetChordVoicings(chord="Cmaj7")
→ [50 voicings × 6 strings × metadata]
Token cost: ~3,000
```

**After:**
```
suggest_voicing(chord="Cmaj7")
→ "I can suggest Cmaj7 voicings. Need:
   (a) beginner-friendly open-position,
   (b) jazz drop-2 shells,
   (c) close-voiced chord-melody?"
Token cost: ~40
```

Claude's next tool call is already scoped. Progressive disclosure AS dialogue, not pagination.

### Pattern C: Oracle Pattern (Compute, Don't Return)

Tool returns the answer to the question the caller would have asked next. ONE voicing + reasoning, not a ranked list.

**Before:**
```
GetChordVoicings(chord="G7", context="after Cmaj7")
→ [50 voicings sorted by voice-leading score]
LLM then picks — wastes context on 49 it won't use.
Token cost: ~3,000 + LLM processing
```

**After:**
```
best_voicing_for(chord="G7", previous="Cmaj7", instrument="guitar")
→ {
    handle: "ga:vh:v3:sha256-...",
    reasoning: "G7 at 3rd position (3-2-0-0-0-1). Voice-leading:
                E→F (minor 2nd), B→D (minor 3rd), shared G/B with Cmaj7.
                Minimal hand shift: index slides down 1 string."
  }
Token cost: ~80 (including handle)
```

The tool absorbs the selection logic. The LLM gets a decision, not raw material.

---

## 3. Anti-Patterns (What to Avoid)

- **`GetAllX()` tools** — catalogs are confessions
- **Paginated dumps** — still dumps, spread across calls (same total context cost)
- **"Top 10" lists** without explicit user filter
- **Metadata envelopes** — `{result: {data: {items: [...]}}}` pads every response
- **Enumeration without actionable next step** — if Claude can't immediately use the list, don't send it

---

## 4. Naming Conventions

| Pattern | Prefixes | Examples |
|---------|---------|----------|
| Resolution | `resolve_`, `identify_`, `narrow_` | `resolve_instrument`, `identify_chord`, `narrow_tuning` |
| Socratic | `suggest_`, `propose_`, `recommend_` | `suggest_voicing`, `propose_progression`, `recommend_exercise` |
| Oracle | `best_X_for`, `next_X_after`, `optimal_X_given` | `best_voicing_for`, `next_chord_after`, `optimal_fingering_given` |

---

## 5. Token Budget Enforcement

Every Socratic tool declares its `budget_class`:

| Tool type | Max tokens | Example |
|-----------|-----------|---------|
| **Resolution** | 120 | `resolve_instrument(hint)` |
| **Socratic** | 100 | `suggest_voicing(chord)` |
| **Oracle** | 250 | `best_voicing_for(chord, context)` |
| **Lookup** | 80 | `get_chord_notes(symbol)` |
| **Analysis** | 500 | `analyze_progression(chords)` |
| **Search** | 800 | `find_similar_voicings(handle)` |

Budgets enforced server-side: responses exceeding budget are truncated with explicit hint ("... N more items. Use {narrow_tool} to filter.").

---

## 6. Conversion Guide: Retrofitting Existing Tools

The GA MCP server has multiple leaky enumeration tools. Planned rewrites:

| Current (leaky) | Socratic replacement | Savings |
|-----------------|---------------------|---------|
| `GetAvailableScales()` → 100+ | `resolve_scale(hint)` | 2K → 120 tokens |
| `GetAvailableModes()` → 150+ | `resolve_mode(hint)` + `suggest_mode_for(chord)` | 3K → 200 |
| `GetSetClasses(cardinality)` → 224 | `find_set_class(properties)` | 8K → 100 |
| `GetAvailableInstruments()` → 114 | `resolve_instrument(hint)` | 2K → 120 |
| `GetAvailableTunings(instr)` → N | `default_tuning(instrument)` + `narrow_tuning(hint)` | 500 → 120 |
| `GaListClosures()` → 30+ | `find_closure(purpose)` + `get_closure_schema(name)` | 4K → 150 |

---

## 7. When NOT to Use Socratic

Keep enumeration tools alongside Socratic ones for these cases:

- **User explicitly requests "list all X"** — respect direct intent
- **Debugging/inspection contexts** — devs need raw lists
- **UI populating dropdowns** — different consumer (browser)
- **Exhaustive analysis** — "compare all 7 modes" needs all 7

**Solution:** expose both. Default to Socratic (`resolve_instrument(hint)`). Offer enumeration (`list_instruments(filter)`) when justified.

---

## 8. Worked Example: Full Conversation Flow

### Scenario: Beginner wants to play a song on bass

**Turn 1 — User:** "Help me play this song on bass"

**Agent reasoning:** Need to resolve which bass first.

**Tool call:** `resolve_instrument(hint="bass")`

**Response:** "Bass Guitar (4-string, EADG). Alternatives: 5-string, fretless, upright bass."
*Token cost: ~30*

**Turn 2 — User:** "4-string is fine"

**Tool call:** `resolve_song(title="...")` → handle
**Tool call:** `suggest_arrangement(song_handle, instrument="bass_4")`

**Response:** "For bass, you can play: (a) root notes only (easiest), (b) root-5 pattern (classic), (c) walking line (advanced)."
*Token cost: ~40*

**Turn 3 — User:** "Walking line please"

**Tool call:** `best_walking_line(from="Am7", to="D7", instrument="bass_4", difficulty="intermediate")`

**Response:**
```
Walking line: A → C → E → A (ascending, then D)
Handle: ga:vh:v3:sha256-...
Reasoning: Chord tones on beats 1,3; passing tones on 2,4.
           Stays in 5-8th fret box for smooth position.
```
*Token cost: ~80*

**Total conversation context used: ~400 tokens**

**Compare to leaky design:**
- List 114 instruments: 2,000 tokens
- List 50 bass voicings for Am7: 3,000 tokens
- List 50 walking lines: 5,000 tokens
- **Total: ~15,000 tokens** — 37× more

---

## 9. Integration with Demerzel Artifacts

- **`contracts/ga-mcp-tool-bundles.md`** — 7 tool bundles adopt Socratic patterns
- **`schemas/voicing-handle.schema.json`** — Oracle tools return `vh` handles
- **`contracts/ui-chord-hydration.md`** — Socratic responses use handle tags for visuals
- **`policies/mcp-context-budget.yaml`** — budgets enforced per tool type
- **`contracts/directives/ga-kinematic-pathfinder.directive.md`** — pathfinder implements Oracle pattern

---

## 10. Governance Enforcement

Every new MCP tool MUST declare at registration:

```yaml
name: resolve_instrument
budget_class: resolution
max_tokens: 120
pattern: socratic
rationale: "Replaces GetAvailableInstruments enumeration dump"
```

Tools violating their budget class in production are flagged for redesign per `policies/mcp-context-budget.yaml`.

---

## Appendix: Named Concepts

This pattern doc relies on three concepts from `policies/mcp-context-budget.yaml`:

- **The Demerzel Threshold** — point where retrieved data displaces reasoning
- **The Chrome Tax** — context cost of scaffolding (metadata, cursors, wrappers)
- **The Oracle Inversion** — return the resolution of the implicit question

Socratic Tools are the practical antidote to all three.
