# Discord Bot Test Report

**Date:** 2026-03-22
**Tester:** Claude Code (agent)
**Bot version:** demerzel-bot 1.0.0
**Bot status:** Running (PID 376400)
**Model:** claude-sonnet-4-20250514

## Executive Summary

The Discord bot is live with 4 personas, 9 music tools, and VexFlow rendering across 6 channels. Code analysis confirms solid architecture for guitar use cases. However, **automated testing via the Discord MCP plugin is blocked** because the bot ignores messages from bot accounts (`message.author.bot` check in `shouldRespond()`). All test messages sent via MCP were received by Discord but never processed by demerzel-bot.

This report provides a code-level capability assessment, documents the blocking issue, and recommends fixes.

## Test Execution

### Test 1: "What are the modes of the major scale?"

- **Sent to:** #music-lab (channel 1485339432780435709)
- **Message ID:** 1485387814865731706
- **Persona detected:** `ga` (keyword "mode" triggers GA persona at line 93 of bot.js)
- **Bot response:** NONE — message ignored due to bot-author check
- **Expected behavior:** GA persona responds with all 7 modes (Ionian through Locrian), likely with fretboard context

### Tests 2-5: Not sent

Remaining tests were not sent after confirming the bot-ignores-bots blocker on Test 1. The planned tests were:

| # | Query | Expected Persona | Expected Tools |
|---|-------|-----------------|----------------|
| 2 | "Show me a ii-V-I progression in Bb" | ga | `analyze_progression`, `render_chords` |
| 3 | "What scales work over a dominant 7th chord?" | ga | `suggest_scale` |
| 4 | "Explain the CAGED system" | ga | none (text-only) |
| 5 | "What's the difference between Dorian and Aeolian?" | ga | none (text-only) |

## Blocking Issue

**Root cause:** `bot.js:216` — `if (message.author.bot) return false;`

The Discord MCP plugin sends messages as a bot account. The demerzel-bot correctly ignores bot messages to prevent loops, but this also blocks automated testing from Claude Code agents.

**Impact:** Cannot validate bot response quality, tool invocation, VexFlow rendering, or persona routing through automated means.

**Recommended fix:** Add a test mode or allowlist:

```javascript
// Option A: Environment variable for test mode
if (message.author.bot && !process.env.ALLOW_TEST_BOTS) return false;

// Option B: Allowlist specific bot IDs
const ALLOWED_BOTS = (process.env.ALLOWED_BOT_IDS || '').split(',');
if (message.author.bot && !ALLOWED_BOTS.includes(message.author.id)) return false;
```

## Code-Level Capability Assessment

### Persona Routing (bot.js:57-104)

| Persona | Trigger Keywords | Channel Triggers | Color |
|---------|-----------------|------------------|-------|
| **ga** (Guitar Alchemist) | guitar, chord, scale, tab, fretboard, improvise, progression, reharmonize, optic, practice, song, pentatonic, mode, dorian, mixolydian, voice leading, backing track | music, guitar | Orange (#F0883E) |
| **seldon** (Teacher) | seldon, teach, learn, course, lesson, academy, music, theory | seldon, academy, research | Blue (#7289DA) |
| **demerzel** (Governance) | demerzel, govern, constitution, policy, audit, conscience | demerzel, governance, dev-ops | Green (#4CB050) |
| **bs** (BS Detector) | translate this bs, detect bs, generate bs, corporate speak, buzzword | bs-detector, bs | Red (#E06C75) |

**Assessment:** Routing logic is keyword-based and reasonable. The GA persona has the richest trigger set (17 keywords). Potential issue: "mode" is a common English word that could cause false positives in non-music channels, but channel-based fallback to demerzel mitigates this.

### Music Tools (context.js:197-317) — 9 Tools

| Tool | Input | Purpose | Rendering |
|------|-------|---------|-----------|
| `analyze_chord` | chord name, optional key | Chord intervals, quality, function | Text only |
| `analyze_progression` | progression string, optional key | Roman numerals, cadences, reharmonization | Text only |
| `suggest_scale` | context, optional style | Scale suggestions with rationale | Text only |
| `reharmonize` | progression, style, complexity | Substitution techniques | Text only |
| `parse_tablature` | ASCII tab | Pattern identification | Text only |
| `optic_analysis` | chord_a, chord_b, or progression | Voice leading analysis | Text only |
| `practice_routine` | level, focus, minutes | Structured practice plan | Text only |
| `fretboard_diagram` | type, name, optional position | Scale/chord on fretboard | **PNG image** |
| `render_chords` | chord array, optional title | Staff notation | **PNG image** |

**Assessment:** Good tool coverage. Two tools produce PNG images via VexFlow/Canvas. The remaining 7 are "virtual" tools — Claude generates the response based on the tool call context rather than executing real computation. This is a valid pattern but means the quality depends entirely on Claude's music theory knowledge in the system prompt.

### VexFlow Rendering (vexRenderer.js)

- **Chord voicings:** 60 chords defined (12 major triads, 11 minor triads, 12 dom7, 11 min7, 12 maj7)
- **Enharmonic normalization:** C#/Db, D#/Eb, G#/Ab, A# /Bb mappings
- **Fretboard diagrams:** Only A minor pentatonic and E minor pentatonic have hardcoded positions (lines 374-397). All other scales fall back to empty fretboard (Claude provides ASCII instead)
- **Auto-render:** `tryRenderFromText()` scans GA responses for 3+ chord names and auto-generates a staff PNG
- **Dark theme:** Background #161b22 (GitHub dark), notes in #58a6ff (blue) and #e06c75 (red for roots)

**Assessment:** The rendering is production-quality for supported chords. The fretboard diagram tool has a major gap — only 2 scales are hardcoded. For the test query "Show me A minor pentatonic", it would render correctly. For anything else (C major scale, Dorian mode, etc.), it would produce an empty fretboard and Claude would fall back to ASCII.

### System Prompt Quality (context.js:116-195)

The GA system prompt is comprehensive and musically accurate:

- CAGED system explanation with practical examples
- 6 chord voicing examples (open, barre, jazz drop-2)
- ii-V-I, rhythm changes, 12-bar blues, bossa nova progressions
- Reharmonization techniques (tritone sub, chromatic approach, modal interchange, back-door dominant)
- OPTIC/K voice leading framework with worked example
- 4 guitar tunings with cultural context
- 3-tier practice templates (beginner/intermediate/advanced)
- 5 genre knowledge blocks (blues, jazz, rock, flamenco, bossa nova)
- GA domain classes reference (Chord, Scale, Key, Fretboard, GrothendieckService)

**Assessment:** This is a strong system prompt. A musician asking any of the 5 test questions would get substantive, accurate answers. The prompt covers modes, ii-V-I progressions, dominant chord scales, CAGED, and modal differences — all test topics.

### Conversation History (bot.js:42-55)

- 10-message sliding window per channel
- Pairs removed from oldest (user+assistant)
- No persistence across bot restarts

**Assessment:** Adequate for short conversations. No cross-channel context, which is correct for persona isolation.

## Observations from Existing Channel History

### Evidence of Prior Human Interaction

- **#music-lab:** User "spareilleux" interacted with bot ("I'm ready!", "You said create a guitar singularity repo, no?"). Bot responded with embeds (content not visible in plain-text fetch but messages were sent).
- **#governance:** User "spareilleux" sent "help" and received the help embed response.
- **Previous session assessment:** "Bot getting 'Cool!' from a guitarist = more ERGOL than all 80+ artifacts combined."

This confirms the bot does respond to human users and has been validated by at least one real user.

## Gaps and Recommendations

### Critical

1. **Bot-ignores-bots blocker** — Add test mode or allowlist so automated testing is possible (see fix above)
2. **Fretboard diagram coverage** — Only 2 scales hardcoded (A minor pentatonic, E minor pentatonic). Add at least the 7 modes of C major, blues scales in common keys, and major pentatonic patterns

### Important

3. **Embed content not fetchable** — The Discord MCP fetch_messages tool shows embed bodies as empty. This prevents reading bot responses programmatically. The MCP plugin may need embed content support.
4. **Tool results are simulated** — 7 of 9 tools don't compute anything; they prompt Claude to generate a response. This works but means results vary between calls. Consider adding actual computation for `analyze_chord` (interval calculation) and `suggest_scale` (scale-chord matching).

### Nice to Have

5. **Error handling on API failure** — The `generateResponse` function catches errors but returns a string or object inconsistently (line 207 returns string, line 203 returns object). The `splitMessage` call at line 307 handles both, but this should be normalized.
6. **Multiple tool calls** — The bot only handles the first `tool_use` block in a response (the for loop at line 138 processes sequentially but the follow-up overwrites rather than appends). If Claude calls both `analyze_progression` and `render_chords` in one response, only the last tool's follow-up text is captured.
7. **Channel-based persona override** — Consider allowing users to force a persona with a prefix (e.g., `!ga What key is this in?`) to override channel-based routing.

## Verdict

The bot architecture is sound. The GA persona system prompt is comprehensive and musically accurate. VexFlow rendering works for supported chords. The main blocker for automated testing is the bot-ignores-bots behavior, which is correct for production but needs a test bypass. For real guitar use cases from human users, the bot should perform well based on code analysis and the evidence of prior successful interactions.

**ERGOL score for this test session:** Low — we confirmed the bot is running and identified real issues, but could not validate actual response quality due to the bot-author blocker. The highest-value next step is to have a human user run the 5 test queries and capture the responses.
