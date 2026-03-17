# Live MCP Chatbot Design — GA Discussion Q&A via Real-Time Domain Computation

**Date:** 2026-03-17
**Status:** Draft
**Issue:** #27
**Approach:** Replace hardcoded YAML lookup tables with live MCP tool calls to the GA server

## Overview

The GA chatbot workflow (`.github/workflows/ga-chatbot-discussions.yml`) currently answers music theory questions using static, hardcoded lookup tables embedded in shell script. This produces correct but limited answers — only 6 topics (scales, chords, intervals, modes, progressions, circle of fifths) with fixed content that cannot handle specific queries like "What notes are in Db Lydian?" or "Show me a Cmaj9 voicing on guitar."

The GA MCP server already exposes 10+ tools (`ga_scale`, `ga_chord`, `ga_interval`, `ga_fretboard`, `ga_voicing`, `ga_dsl`, `ga_chat`, etc.) that can compute answers to any music theory question dynamically. This spec defines how to route Discussion questions to those tools and format the results, while preserving the governance trace.

### Goals

1. Answer any music theory question, not just 6 hardcoded topics
2. Return computed results (actual notes, actual chord tones) rather than static reference tables
3. Handle specific queries: "What is the 7th mode of melodic minor?", "Spell an Fdim7 chord", "Show Gmaj7 fretboard positions"
4. Preserve the existing agentic trace and governance compliance footer
5. Graceful fallback when the MCP server is unavailable

### Non-Goals

- Building a conversational chatbot (this remains single-turn Q&A on Discussions)
- Running the GA MCP server inside GitHub Actions (it runs externally)
- Replacing the GA chatbot's Ollama/RAG infrastructure (that is a separate Ralph Loop concern)

## 1. Architecture

### Current Flow

```
Discussion created → grep question for keywords → select hardcoded answer block → post comment
```

### Proposed Flow

```
Discussion created
  → Extract question text (title + body)
  → Route question to one or more GA MCP tools
  → Call tool(s) via Claude API with MCP server configuration
  → Format tool output as markdown
  → Append governance trace
  → Post comment
```

### Tool Invocation Strategy

The workflow runs in GitHub Actions (ubuntu-latest). There are two viable approaches for calling MCP tools:

**Option A: Claude API with MCP server connection (recommended)**

Use the Anthropic API with the `mcp_servers` parameter to connect Claude to the GA MCP server at runtime. Claude handles the question routing natively — no manual dispatch logic needed.

```yaml
- name: Answer via Claude + MCP
  env:
    ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
    GA_MCP_URL: ${{ secrets.GA_MCP_URL }}
  run: |
    RESPONSE=$(curl -s https://api.anthropic.com/v1/messages \
      -H "x-api-key: $ANTHROPIC_API_KEY" \
      -H "content-type: application/json" \
      -H "anthropic-version: 2025-01-01" \
      -d '{
        "model": "claude-sonnet-4-20250514",
        "max_tokens": 2048,
        "system": "You are Seldon, the Guitar Alchemist music theory assistant. Answer music theory questions using the GA MCP tools available to you. Format responses as clear markdown with tables where appropriate. Do not fabricate — only report what the tools compute.",
        "tools": [...],
        "messages": [{"role": "user", "content": "'"$QUESTION"'"}]
      }')
```

This approach delegates question-to-tool routing to Claude, which already understands tool descriptions and can compose multi-tool answers. No manual regex dispatch needed.

**Option B: Direct MCP tool calls via HTTP**

Call the GA MCP server's HTTP/SSE endpoint directly from the workflow using `curl`. This requires manual question-to-tool routing logic but avoids the Anthropic API cost.

```yaml
- name: Call GA MCP directly
  run: |
    RESULT=$(curl -s "$GA_MCP_URL/tools/ga_scale" \
      -d '{"root": "C", "type": "major"}')
```

**Recommendation:** Option A. Claude's natural language understanding eliminates the fragile regex-based routing that the current implementation suffers from. The cost per Discussion question is negligible (one API call every few hours at most). Option B can serve as the fallback path.

## 2. Question Routing

### With Option A (Claude API)

No explicit routing logic needed. The system prompt instructs Claude to use the available GA tools. Claude sees tool descriptions from the MCP server and selects the appropriate one(s).

Tool descriptions from the capability registry (`schemas/capability-registry.json`):

| Tool | Domain | Handles Questions Like |
|------|--------|----------------------|
| `ga_scale` | music-theory | "What notes in D Dorian?", "Show me Bb melodic minor" |
| `ga_chord` | music-theory | "What's in a Cmaj7?", "Spell Fdim7" |
| `ga_chord_atonal` | music-theory | Atonal chord analysis, pitch-class sets |
| `ga_interval` | music-theory | "What interval is C to Ab?", "How many semitones in a tritone?" |
| `ga_fretboard` | fretboard | "Show C major on the fretboard", "Fretboard diagram for Am pentatonic" |
| `ga_voicing` | fretboard | "Guitar voicing for Gmaj7", "Open chord shapes" |
| `ga_dsl` | dsl | Complex multi-step music theory expressions |
| `ga_chat` | chat | General music theory conversation, questions that span multiple domains |

### With Option B (Direct, Fallback)

If the Claude API path fails, fall back to a simplified direct routing table:

```bash
route_question() {
  local q="$1"
  case "$q" in
    *scale*|*mode*|*dorian*|*lydian*|*phrygian*|*mixolydian*|*aeolian*|*locrian*|*ionian*|*pentatonic*)
      echo "ga_scale" ;;
    *chord*|*triad*|*seventh*|*dominant*|*diminished*|*augmented*|*sus*)
      echo "ga_chord" ;;
    *interval*|*semitone*|*half.step*|*whole.step*)
      echo "ga_interval" ;;
    *fretboard*|*fret*|*position*|*fingering*)
      echo "ga_fretboard" ;;
    *voicing*|*open.chord*|*barre*)
      echo "ga_voicing" ;;
    *)
      echo "ga_chat" ;;
  esac
}
```

This is intentionally coarse — `ga_chat` catches everything the specific tools do not match, serving as a general-purpose fallback within the MCP server itself.

## 3. Response Formatting

### Tool Output to Markdown

GA MCP tools return structured JSON. The workflow must convert this to readable markdown for the Discussion comment.

**Formatting rules:**

1. **Note lists** become inline sequences: `C D E F G A B`
2. **Chord tones** become tables with formula + notes + intervals
3. **Fretboard diagrams** render as code blocks (ASCII fretboard)
4. **Intervals** become a single-row table: interval name, semitones, quality
5. **Multi-tool responses** (from Claude) arrive as pre-formatted text — use directly

**Template for Claude system prompt (Option A):**

```
Format your response as GitHub-flavored markdown suitable for a Discussion comment.
Use tables for structured data. Use code blocks for fretboard diagrams.
Start with a ## heading naming the topic.
Keep responses concise but complete — this is reference material, not a tutorial.
End with a tip or related concept suggestion using a blockquote.
```

**Formatting function for direct calls (Option B):**

```bash
format_scale_response() {
  local json="$1"
  local root=$(echo "$json" | jq -r '.root')
  local type=$(echo "$json" | jq -r '.type')
  local notes=$(echo "$json" | jq -r '.notes | join(" ")')
  local formula=$(echo "$json" | jq -r '.formula // empty')

  cat <<EOF
## $root $type Scale

**Notes:** $notes
**Formula:** $formula

> Ask a follow-up question to explore chords built from this scale!
EOF
}
```

## 4. Fallback Strategy

Three-tier fallback for resilience:

### Tier 1: Claude API + MCP (primary)

Claude connects to the GA MCP server, routes the question, calls tools, formats the answer. This is the happy path.

**Failure detection:** HTTP status != 200, or response contains no tool results, or timeout after 30 seconds.

### Tier 2: Direct MCP tool call (first fallback)

If the Claude API is unavailable (rate limit, outage, missing key), call the GA MCP server directly using the bash routing function from Section 2. Format the raw JSON response using the bash formatting functions from Section 3.

**Failure detection:** MCP server returns HTTP error or connection timeout after 10 seconds.

### Tier 3: Static lookup tables (last resort)

If the MCP server is also unavailable, fall back to the current hardcoded answers. These remain in the workflow as a constant block, but are only used when both Tier 1 and Tier 2 fail.

**Implementation:**

```bash
answer_question() {
  local question="$1"

  # Tier 1: Claude API + MCP
  ANSWER=$(call_claude_with_mcp "$question" 2>/dev/null) && { echo "$ANSWER"; return 0; }

  # Tier 2: Direct MCP
  TOOL=$(route_question "$question")
  ANSWER=$(call_mcp_direct "$TOOL" "$question" 2>/dev/null) && { echo "$ANSWER"; return 0; }

  # Tier 3: Static fallback
  ANSWER=$(static_lookup "$question")
  echo "$ANSWER"
}
```

The governance trace records which tier was used, so the provenance chain remains accurate.

## 5. Governance Trace

The existing agentic trace footer must be preserved and updated to reflect live computation.

### Changes to the Trace

| Trace Field | Static (current) | Live MCP (proposed) |
|-------------|------------------|---------------------|
| `[4] GA DOMAIN ENGINE` — Skills invoked | Hardcoded list of all skills | Actual tool(s) called (e.g., `ga_scale`) |
| `[4] GA DOMAIN ENGINE` — Computation | "PURE DOMAIN (zero LLM calls)" | "LIVE MCP (tool: ga_scale)" or "CLAUDE + MCP (tools: ga_scale, ga_chord)" |
| `[4] GA DOMAIN ENGINE` — Confidence | Always 1.0 | 1.0 for deterministic tools, 0.9 for `ga_chat` |
| `[4] GA DOMAIN ENGINE` — Data source | "GA.Business.Core music theory primitives" | "GA MCP server (live computation)" |
| Fallback tier | Not tracked | New field: "Resolution tier: 1 (Claude+MCP) / 2 (Direct MCP) / 3 (Static)" |

### Updated Trace Block

```
│  [4] GA DOMAIN ENGINE (Guitar Alchemist)                        │
│      └─ Repo: github.com/GuitarAlchemist/ga                    │
│      └─ MCP Server: ga (live)                                   │
│      └─ Tools invoked: ${TOOLS_USED}                            │
│      └─ Resolution tier: ${TIER}                                │
│      └─ Computation: ${COMPUTATION_TYPE}                        │
│      └─ Confidence: ${CONFIDENCE}                               │
│      └─ Data source: GA MCP server (live domain computation)    │
```

### Governance Compliance Table

No changes needed — the same constitutional checks apply. Live computation is still deterministic domain knowledge (not LLM generation), so Article 1 (Truthfulness) and Article 5 (Non-Deception) remain PASS.

Exception: When Tier 1 (Claude API) is used, the response includes LLM-formatted text. The trace should note this:

```
| Default Article 1 (Truthfulness) | PASS | Tool output is deterministic; formatting is LLM |
```

## 6. Migration Path

### Phase 1: Add Claude API path alongside static (Week 1)

- Add `ANTHROPIC_API_KEY` and `GA_MCP_URL` as repository secrets
- Implement the three-tier `answer_question()` function
- Keep all static lookup tables in place as Tier 3 fallback
- Add a `RESOLUTION_TIER` output to track which path was used
- Update the governance trace to include the tier

**Validation:** Run workflow_dispatch manually with test questions. Verify Tier 1 produces correct answers. Verify Tier 3 fallback works when secrets are missing.

### Phase 2: Expand tool coverage (Week 2)

- Test against the full range of questions the Discussion channel receives
- Add `ga_fretboard` and `ga_voicing` formatting (these produce diagram output)
- Refine the Claude system prompt based on answer quality
- Monitor which tools get called most frequently (via the trace)

### Phase 3: Remove static fallback (Week 3+)

- Once Tier 1 and Tier 2 have proven reliable over 2+ weeks of production use, remove the static lookup tables
- Keep a minimal static "service unavailable" message as the final fallback
- Update the default (no-match) message to reflect the expanded capabilities

### Rollback

At any phase, the workflow can be reverted to the previous commit. All changes are in a single file (the workflow YAML), so rollback is a one-commit revert. Per Demerzel's reversibility policy (Default Constitution Article 3), the migration is designed to be fully reversible at each phase.

## 7. Testing Approach

### Unit Testing (pre-merge)

Since this is a GitHub Actions workflow (shell script), formal unit tests are not applicable. Instead:

1. **Manual workflow_dispatch tests** — trigger the workflow with `workflow_dispatch` and verify answers for each topic category
2. **Test matrix** — a set of representative questions covering each GA MCP tool:

| Question | Expected Tool | Expected Output Contains |
|----------|--------------|-------------------------|
| "What notes are in C major scale?" | ga_scale | C D E F G A B |
| "What notes are in D Dorian?" | ga_scale | D E F G A B C |
| "Spell an Fmaj7 chord" | ga_chord | F A C E |
| "What interval is C to G#?" | ga_interval | augmented fifth, 8 semitones |
| "Show A minor pentatonic on fretboard" | ga_fretboard | ASCII diagram |
| "What is a tritone?" | ga_interval or ga_chat | 6 semitones, augmented 4th |
| "Common jazz chord progressions" | ga_chat | ii-V-I |

3. **Fallback verification** — temporarily remove API keys and verify Tier 2 and Tier 3 activate correctly

### Integration Testing (post-merge)

1. **Create test Discussions** in the Q&A category with various question types
2. **Verify the posted comment** contains correct computed answers (not static tables)
3. **Verify the governance trace** correctly identifies the tools used and resolution tier
4. **Verify the compounding step** still creates knowledge state entries

### Regression Testing

1. **Existing question types** (scales, chords, intervals, modes, progressions, circle of fifths) must still produce correct answers
2. **Bot-created discussion filtering** must still work (skip titles starting with bot prefixes)
3. **Poll mode** (scheduled trigger for unanswered questions) must still function
4. **Governance trace format** must remain parseable by any downstream consumers

## 8. Secrets and Configuration

New repository secrets required:

| Secret | Purpose | Required For |
|--------|---------|-------------|
| `ANTHROPIC_API_KEY` | Claude API authentication | Tier 1 (Claude + MCP) |
| `GA_MCP_URL` | GA MCP server endpoint URL | Tier 1 and Tier 2 |

Existing secrets retained:

| Secret | Purpose |
|--------|---------|
| `PAT_TOKEN` | GitHub API for posting Discussion comments |

### Configuration Constants (in workflow)

```yaml
env:
  CLAUDE_MODEL: claude-sonnet-4-20250514
  CLAUDE_MAX_TOKENS: 2048
  MCP_TIMEOUT_SECONDS: 30
  DIRECT_MCP_TIMEOUT_SECONDS: 10
```

## 9. Relationship to Ralph Loop Directive

The directive `directive-ga-chatbot-loop.json` (issued 2026-03-15) calls for a Ralph Loop to build the GA chatbot's full functionality within the `ga` repository itself — Ollama, RAG, SignalR infrastructure.

This spec is complementary, not overlapping:

- **This spec** connects the Demerzel Discussion workflow to the GA MCP server (Demerzel repo change)
- **The Ralph Loop** builds the GA chatbot's internal capabilities (GA repo change)
- **Intersection:** As the Ralph Loop adds more tools to the GA MCP server, this workflow automatically gains access to them — no Demerzel-side changes needed

The loop initialization state (`loop-ga-chatbot-init.json`) is at iteration 0. This spec can proceed independently.

## 10. Open Questions

1. **MCP server availability** — Is the GA MCP server running continuously, or does it need to be started on demand? If on-demand, the workflow may need to start it (adds complexity and latency).
2. **Authentication** — Does the GA MCP server require authentication? If so, add credentials to secrets.
3. **Rate limits** — The Anthropic API has rate limits. At the current Discussion volume (a few per day), this is not a concern, but should be monitored.
4. **Tool output schema stability** — Are the GA MCP tool response schemas stable, or do they change frequently? If unstable, the formatting functions in Tier 2 may break.
