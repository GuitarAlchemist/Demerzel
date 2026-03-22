# Discord Bot Test Report — Guitar Use Cases

**Date:** 2026-03-22 (updated 2026-03-22)
**Tester:** discord-tester agent (demerzel-sprint-2)
**Bot version:** demerzel-bot 1.0.0
**Model:** claude-sonnet-4-20250514
**Channel tested:** #music-lab (1485339432780435709)

## Executive Summary

The Discord bot is live with 4 personas (GA, Demerzel, Seldon, BS Detector), 9 music tools, and VexFlow rendering across 6 channels. **Automated testing via the Discord MCP plugin is blocked** because the MCP plugin sends messages as the bot account, and the bot correctly ignores its own messages (`message.author.bot` check). All test messages appear as "me" in channel history.

This report provides:
1. Confirmation of the blocker with test evidence
2. Code-level capability assessment for each guitar use case
3. Observations from real user interactions in channel history
4. Actionable gaps and recommendations

## Test Execution Log

### Test 1: "What are the modes of the major scale?"

- **Sent to:** #music-lab (message ID: 1485388431159853157)
- **Persona routing:** `ga` — keyword "mode" matches at `bot.js:93`
- **Bot response:** NONE — message author is bot; filtered at `bot.js:216`
- **Expected behavior:** GA persona lists all 7 modes (Ionian, Dorian, Phrygian, Lydian, Mixolydian, Aeolian, Locrian) with interval formulas, fretboard context, and characteristic notes. System prompt covers modes via CAGED and genre sections.

### Tests 2-5: Planned but not sent

After confirming the bot-ignores-bots blocker, remaining tests were analyzed at code level only.

| # | Query | Persona | Key Tools | System Prompt Coverage |
|---|-------|---------|-----------|----------------------|
| 2 | "Show me a ii-V-I progression in Bb" | ga | `analyze_progression`, `render_chords` | Explicit ii-V-I section with voice leading (context.js:131-132). VexFlow has Bbmaj7, Cm7, F7 voicings. Auto-render would trigger on 3+ chord names in response. |
| 3 | "What scales work over a dominant 7th chord?" | ga | `suggest_scale` | Mixolydian, blues scale, altered dominant, bebop scale all in system prompt. Jazz genre section covers chord-tone soloing over dom7. |
| 4 | "Explain the CAGED system" | ga | none (text) | Dedicated CAGED section (context.js:123). Links shapes to chord tones and scale patterns. Example: A minor pentatonic box 1 aligns with E-shape Am at fret 5. |
| 5 | "What's the difference between Dorian and Aeolian?" | ga | none (text) | Both modes referenced in system prompt. Dorian mentioned in modal interchange section; Aeolian implicit as natural minor. Claude's base knowledge handles this well. |

## Blocking Issue

**Root cause:** `bot.js:216` — `if (message.author.bot) return false;`

The Discord MCP plugin sends messages using the bot's own Discord token. The bot correctly ignores bot-authored messages to prevent response loops. This is **correct production behavior** but blocks automated testing.

**Evidence:** Message ID 1485388431159853157 appears in channel history as "me" (the bot's own account), confirming MCP messages use the bot identity.

**Recommended fixes (pick one):**
```javascript
// Option A: Environment variable test mode
if (message.author.bot && !process.env.ALLOW_TEST_BOTS) return false;

// Option B: Allowlist specific bot IDs for testing
const ALLOWED_BOTS = (process.env.ALLOWED_BOT_IDS || '').split(',');
if (message.author.bot && !ALLOWED_BOTS.includes(message.author.id)) return false;
```

## Code-Level Capability Assessment

### Persona Routing (bot.js:57-104)

| Persona | Trigger Keywords | Channel Names | Embed Color |
|---------|-----------------|---------------|-------------|
| **ga** | guitar, chord, scale, tab, fretboard, improvise, progression, reharmonize, optic, practice, song, pentatonic, mode, dorian, mixolydian, voice leading, backing track | music, guitar | Orange #F0883E |
| **seldon** | seldon, teach, learn, course, lesson, academy | seldon, academy, research | Blue #7289DA |
| **demerzel** | demerzel, govern, constitution, policy, audit, conscience | demerzel, governance, dev-ops | Green #4CB050 |
| **bs** | translate this bs, detect bs, generate bs, corporate speak, buzzword | bs-detector, bs | Red #E06C75 |

All 5 guitar test queries would correctly route to the `ga` persona based on keywords: "modes" (Test 1), "progression" (Test 2), "scales"+"chord" (Test 3), "CAGED" triggers no specific keyword but channel name "music-lab" would route to GA via line 94, "Dorian" (Test 5).

**Issue found:** Test 4 ("Explain the CAGED system") — the word "CAGED" is not in the trigger list. In #music-lab it routes correctly via channel name, but in #general it would fall through to demerzel. Recommendation: add "caged" to GA triggers.

### Music Tools (9 total)

| Tool | Produces | Used by Test |
|------|----------|-------------|
| `analyze_chord` | Text (Claude-generated) | — |
| `analyze_progression` | Text (Claude-generated) | Test 2 |
| `suggest_scale` | Text (Claude-generated) | Test 3 |
| `reharmonize` | Text (Claude-generated) | — |
| `parse_tablature` | Text (Claude-generated) | — |
| `optic_analysis` | Text (Claude-generated) | — |
| `practice_routine` | Text (Claude-generated) | — |
| `fretboard_diagram` | **PNG image** (Canvas) | Test 1 (if invoked) |
| `render_chords` | **PNG image** (VexFlow) | Test 2 |

7 of 9 tools are "virtual" — they prompt Claude to generate a response based on the tool call. Only `fretboard_diagram` and `render_chords` produce actual computed output (PNG images).

### VexFlow Rendering (vexRenderer.js)

- **60 chord voicings** defined: 12 major, 11 minor, 12 dom7, 11 min7, 12 maj7
- **Enharmonic normalization**: C#→Db, D#→Eb, G#→Ab, A#→Bb
- **Auto-render**: `tryRenderFromText()` scans GA responses for 3+ qualified chord names and auto-generates staff PNG
- **Dark theme**: GitHub dark background (#161b22), blue notes (#58a6ff), red roots (#e06c75)

**Fretboard gap:** Only 2 scales hardcoded — A minor pentatonic and E minor pentatonic. All other `fretboard_diagram` calls produce an empty fretboard and Claude falls back to ASCII diagrams.

### GA System Prompt Quality (context.js:116-195)

The system prompt is comprehensive and musically accurate:

- **CAGED system**: Explained with chord-shape-to-scale linkage
- **Chord voicings**: Open, barre, jazz drop-2, rootless
- **Progressions**: ii-V-I, rhythm changes, 12-bar blues, minor blues, bossa nova
- **Reharmonization**: Tritone sub, chromatic approach, modal interchange, back-door dominant
- **OPTIC/K**: Voice leading framework with worked Cmaj7→Am7 example
- **Tunings**: Standard, Drop D, DADGAD, Open G
- **Practice**: 3-tier templates (beginner 30min, intermediate 45min, advanced 60min)
- **Genres**: Blues, jazz, rock, flamenco, bossa nova
- **Domain classes**: Chord, Scale, Key, Fretboard, GrothendieckService

**Verdict:** A guitarist asking any of the 5 test queries would receive substantive, accurate answers based on this system prompt.

## Observations from Real User Interactions

### Evidence of Working Bot

1. **#bs-detector**: User "spareilleux" sent "Our analysis suggests significant opportunity exists" → bot replied with 5 embed messages within ~14 seconds (IDs 1485387876370878535 through 1485387900790116392). Content not readable via fetch (embeds show as empty) but response was sent.

2. **#governance**: User "spareilleux" sent "help" → bot replied with help embed (ID 1485345835435823416 + 1485345884286881985).

3. **#music-lab**: User "spareilleux" had a multi-turn conversation about creating a guitar-singularity repo. Bot responded to each message.

4. **Prior session verdict**: "Bot getting 'Cool!' from a guitarist = more ERGOL than all 80+ artifacts combined."

### Embed Fetch Limitation

The Discord MCP `fetch_messages` tool shows embed content as empty strings. This means we cannot programmatically read what the bot actually said. Only message IDs and timestamps are visible for bot responses.

## Gaps and Recommendations

### Critical (blocks testing)

| # | Issue | Fix |
|---|-------|-----|
| 1 | **Bot-ignores-bots** — MCP messages use bot identity | Add `ALLOW_TEST_BOTS` env var (see code above) |
| 2 | **Embed content not fetchable** — Cannot read bot responses programmatically | MCP plugin needs embed content extraction |

### Important (affects guitar UX)

| # | Issue | Fix |
|---|-------|-----|
| 3 | **Fretboard diagram coverage** — Only 2 scales hardcoded | Add 7 modes of C major, blues scales, major pentatonic in common keys |
| 4 | **"CAGED" not in GA triggers** — Would misroute in #general | Add "caged" to keyword list at `bot.js:88-94` |
| 5 | **Multiple tool calls** — Only first tool_use block's follow-up appends text | Accumulate all follow-up texts, don't overwrite |
| 6 | **Virtual tools** — 7 tools don't compute, rely on Claude's knowledge | Add interval computation for `analyze_chord`, scale-chord matching for `suggest_scale` |

### Nice to Have

| # | Issue | Fix |
|---|-------|-----|
| 7 | **Persona prefix** — No way to force persona in cross-channel use | Allow `!ga ...` or `!seldon ...` prefix |
| 8 | **Error return inconsistency** — `generateResponse` returns string or object | Normalize to always return `{ text, attachments }` |

## Per-Query Expected Quality (Code-Based Prediction)

| Query | Quality Prediction | Confidence | Rationale |
|-------|-------------------|------------|-----------|
| Modes of major scale | **High** | 0.9 | Core music theory; system prompt covers modes, CAGED, and modal concepts |
| ii-V-I in Bb | **High** | 0.9 | Explicit ii-V-I section in prompt; VexFlow has Cm7, F7, Bbmaj7; auto-render likely triggers |
| Scales over dom7 | **High** | 0.85 | Mixolydian, altered, bebop all in prompt; `suggest_scale` tool available |
| CAGED system | **High** | 0.9 | Dedicated CAGED section with examples; no tool needed |
| Dorian vs Aeolian | **High** | 0.85 | Modal knowledge in prompt; Claude's base music theory is strong here |

## Verdict

**Architecture: Sound.** The bot correctly routes guitar queries to the GA persona, has 9 relevant tools, and renders chord progressions as staff notation PNGs.

**System prompt: Comprehensive.** All 5 test topics are covered with accurate music theory. A human user would get quality answers.

**Testing: Blocked.** The MCP plugin sends as the bot account, so automated interaction testing is impossible without a code change. The embed fetch limitation compounds this — even if the bot responded, we couldn't read the response content.

**ERGOL assessment:** This test session confirmed the bot is running, identified 2 critical gaps (test mode, embed fetch), 4 important improvements, and validated that the system prompt covers all test topics. The highest-ERGOL next step is having a human run the 5 queries and screenshot the responses.
