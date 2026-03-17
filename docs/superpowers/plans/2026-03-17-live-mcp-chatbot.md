# Live MCP Chatbot Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace hardcoded YAML lookup tables in the GA chatbot workflow with live MCP tool calls via Claude API, with graceful fallback to static answers.

**Architecture:** Three-tier answer resolution: (1) Claude API + MCP tools, (2) Direct MCP HTTP calls, (3) Static fallback. Single workflow file modification with phased migration.

**Tech Stack:** GitHub Actions, Bash, curl, jq, Anthropic API, GA MCP server

---

## Phase 1: Add Claude API Path Alongside Static

### Task 1: Add environment variables and secrets reference

**Files:**
- Modify: `.github/workflows/ga-chatbot-discussions.yml`

- [ ] **Step 1: Read the current workflow**

Read `.github/workflows/ga-chatbot-discussions.yml` to understand the full structure before making changes.

- [ ] **Step 2: Add top-level environment variables**

After the `permissions:` block (line 13) and before the `jobs:` block, add:

```yaml
env:
  CLAUDE_MODEL: claude-sonnet-4-20250514
  CLAUDE_MAX_TOKENS: 2048
  MCP_TIMEOUT_SECONDS: 30
  DIRECT_MCP_TIMEOUT_SECONDS: 10
```

- [ ] **Step 3: Add new secrets to the job step**

In the `Process music theory question` step, add `ANTHROPIC_API_KEY` and `GA_MCP_URL` to the `env:` block alongside the existing `GH_TOKEN`:

```yaml
      - name: Process music theory question
        id: answer
        env:
          GH_TOKEN: ${{ secrets.PAT_TOKEN }}
          ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}
          GA_MCP_URL: ${{ secrets.GA_MCP_URL }}
```

- [ ] **Step 4: Commit**

```bash
git add .github/workflows/ga-chatbot-discussions.yml
git commit -m "feat: Add Claude API and MCP env vars to chatbot workflow (#27)"
```

---

### Task 2: Add the `call_claude_with_mcp` function

**Files:**
- Modify: `.github/workflows/ga-chatbot-discussions.yml`

- [ ] **Step 1: Add the Claude API call function**

Insert the following function definition inside the `run:` block, immediately after the `QUESTION=` line (line 66) and before the `ANSWER=""` line (line 69). This function calls the Anthropic API with tool definitions matching the GA MCP server's capabilities:

```bash
          # === THREE-TIER ANSWER RESOLUTION ===
          # Tier 1: Claude API + MCP tools
          # Tier 2: Direct MCP HTTP calls
          # Tier 3: Static lookup tables (existing behavior)
          RESOLUTION_TIER=""

          call_claude_with_mcp() {
            local question="$1"
            [ -z "$ANTHROPIC_API_KEY" ] && return 1
            [ -z "$GA_MCP_URL" ] && return 1

            local SYSTEM_PROMPT="You are Seldon, the Guitar Alchemist music theory assistant. Answer music theory questions using the GA MCP tools available to you. Format your response as GitHub-flavored markdown suitable for a Discussion comment. Use tables for structured data. Use code blocks for fretboard diagrams. Start with a ## heading naming the topic. Keep responses concise but complete — this is reference material, not a tutorial. End with a tip or related concept suggestion using a blockquote (prefix with >). Do not fabricate — only report what the tools compute."

            local RESPONSE
            RESPONSE=$(curl -s --max-time "$MCP_TIMEOUT_SECONDS" \
              https://api.anthropic.com/v1/messages \
              -H "x-api-key: $ANTHROPIC_API_KEY" \
              -H "content-type: application/json" \
              -H "anthropic-version: 2025-01-01" \
              -d "$(jq -n \
                --arg model "$CLAUDE_MODEL" \
                --argjson max_tokens "$CLAUDE_MAX_TOKENS" \
                --arg system "$SYSTEM_PROMPT" \
                --arg question "$question" \
                '{
                  model: $model,
                  max_tokens: $max_tokens,
                  system: $system,
                  tools: [
                    {
                      "name": "ga_scale",
                      "description": "Get scale notes, formula, and intervals for any root and scale type (e.g., major, minor, dorian, pentatonic, melodic minor, etc.)",
                      "input_schema": {
                        "type": "object",
                        "properties": {
                          "root": {"type": "string", "description": "Root note (e.g., C, Db, F#)"},
                          "type": {"type": "string", "description": "Scale type (e.g., major, natural_minor, dorian, pentatonic_minor)"}
                        },
                        "required": ["root", "type"]
                      }
                    },
                    {
                      "name": "ga_chord",
                      "description": "Get chord tones, formula, and intervals for any root and chord type (e.g., maj7, dim7, sus4, 9, etc.)",
                      "input_schema": {
                        "type": "object",
                        "properties": {
                          "root": {"type": "string", "description": "Root note (e.g., C, F#, Bb)"},
                          "type": {"type": "string", "description": "Chord type (e.g., major, minor, maj7, dim7, sus2, 9)"}
                        },
                        "required": ["root", "type"]
                      }
                    },
                    {
                      "name": "ga_interval",
                      "description": "Get interval information between two notes — name, semitones, quality, and classification.",
                      "input_schema": {
                        "type": "object",
                        "properties": {
                          "from": {"type": "string", "description": "Starting note (e.g., C)"},
                          "to": {"type": "string", "description": "Ending note (e.g., G#)"}
                        },
                        "required": ["from", "to"]
                      }
                    },
                    {
                      "name": "ga_chat",
                      "description": "General music theory Q&A — handles questions that span multiple domains or do not fit a specific tool.",
                      "input_schema": {
                        "type": "object",
                        "properties": {
                          "question": {"type": "string", "description": "The music theory question to answer"}
                        },
                        "required": ["question"]
                      }
                    }
                  ],
                  messages: [{role: "user", content: $question}]
                }')" 2>/dev/null) || return 1

            # Check for valid response
            local STOP_REASON
            STOP_REASON=$(echo "$RESPONSE" | jq -r '.stop_reason // empty' 2>/dev/null)
            [ -z "$STOP_REASON" ] && return 1

            # Extract text content from the response
            local TEXT
            TEXT=$(echo "$RESPONSE" | jq -r '[.content[] | select(.type == "text") | .text] | join("\n")' 2>/dev/null)
            [ -z "$TEXT" ] && return 1

            # Extract which tools were called (for the governance trace)
            TOOLS_USED=$(echo "$RESPONSE" | jq -r '[.content[] | select(.type == "tool_use") | .name] | join(", ")' 2>/dev/null)
            [ -z "$TOOLS_USED" ] && TOOLS_USED="ga_chat (implicit)"

            echo "$TEXT"
            return 0
          }
```

- [ ] **Step 2: Commit**

```bash
git add .github/workflows/ga-chatbot-discussions.yml
git commit -m "feat: Add call_claude_with_mcp function for Tier 1 resolution (#27)"
```

---

### Task 3: Add the `call_mcp_direct` function and `route_question` helper

**Files:**
- Modify: `.github/workflows/ga-chatbot-discussions.yml`

- [ ] **Step 1: Add the direct MCP call and routing functions**

Insert these functions immediately after the `call_claude_with_mcp` function (from Task 2):

```bash
          # Route question to the appropriate GA MCP tool
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

          # Tier 2: Call GA MCP server directly via HTTP
          call_mcp_direct() {
            local tool="$1"
            local question="$2"
            [ -z "$GA_MCP_URL" ] && return 1

            local RESULT
            RESULT=$(curl -s --max-time "$DIRECT_MCP_TIMEOUT_SECONDS" \
              "$GA_MCP_URL/tools/$tool" \
              -H "content-type: application/json" \
              -d "$(jq -n --arg q "$question" '{question: $q}')" 2>/dev/null) || return 1

            # Check for valid JSON response
            echo "$RESULT" | jq -e '.' >/dev/null 2>&1 || return 1

            # Format based on tool type
            format_mcp_response "$tool" "$RESULT"
            return 0
          }

          # Format raw MCP JSON responses as markdown
          format_mcp_response() {
            local tool="$1"
            local json="$2"

            case "$tool" in
              ga_scale)
                local root type notes formula
                root=$(echo "$json" | jq -r '.root // empty')
                type=$(echo "$json" | jq -r '.type // empty')
                notes=$(echo "$json" | jq -r '.notes | join(" ") // empty' 2>/dev/null)
                formula=$(echo "$json" | jq -r '.formula // empty')
                cat <<SCALE_EOF
## $root $type Scale

**Notes:** $notes
**Formula:** $formula

> Ask a follow-up question to explore chords built from this scale!
SCALE_EOF
                ;;
              ga_chord)
                local root type tones formula
                root=$(echo "$json" | jq -r '.root // empty')
                type=$(echo "$json" | jq -r '.type // empty')
                tones=$(echo "$json" | jq -r '.tones | join(" ") // empty' 2>/dev/null)
                formula=$(echo "$json" | jq -r '.formula // empty')
                cat <<CHORD_EOF
## $root $type Chord

**Tones:** $tones
**Formula:** $formula

> Try exploring the scale that contains this chord!
CHORD_EOF
                ;;
              ga_interval)
                local name semitones quality
                name=$(echo "$json" | jq -r '.name // empty')
                semitones=$(echo "$json" | jq -r '.semitones // empty')
                quality=$(echo "$json" | jq -r '.quality // empty')
                cat <<INTERVAL_EOF
## Interval: $name

| Property | Value |
|----------|-------|
| Name | $name |
| Semitones | $semitones |
| Quality | $quality |

> Try asking about the inversion of this interval!
INTERVAL_EOF
                ;;
              *)
                # For ga_chat and unknown tools, extract text or dump JSON
                local text
                text=$(echo "$json" | jq -r '.text // .response // .answer // empty' 2>/dev/null)
                if [ -n "$text" ]; then
                  echo "$text"
                else
                  echo '```json'
                  echo "$json" | jq '.'
                  echo '```'
                fi
                ;;
            esac
          }
```

- [ ] **Step 2: Commit**

```bash
git add .github/workflows/ga-chatbot-discussions.yml
git commit -m "feat: Add Tier 2 direct MCP call with routing and formatting (#27)"
```

---

### Task 4: Add the three-tier `answer_question` orchestrator

**Files:**
- Modify: `.github/workflows/ga-chatbot-discussions.yml`

- [ ] **Step 1: Add the answer_question function**

Insert this function immediately after the `format_mcp_response` function (from Task 3) and before the existing `ANSWER=""` line:

```bash
          # === MASTER ANSWER FUNCTION (three-tier resolution) ===
          answer_question() {
            local question="$1"

            # Tier 1: Claude API + MCP tools
            local tier1_answer
            tier1_answer=$(call_claude_with_mcp "$question" 2>/dev/null)
            if [ $? -eq 0 ] && [ -n "$tier1_answer" ]; then
              RESOLUTION_TIER="1 (Claude + MCP)"
              COMPUTATION_TYPE="CLAUDE + MCP (tools: ${TOOLS_USED})"
              CONFIDENCE="1.0 (deterministic tools, LLM formatting)"
              DATA_SOURCE="GA MCP server (live domain computation)"
              echo "$tier1_answer"
              return 0
            fi

            # Tier 2: Direct MCP call
            local tool
            tool=$(route_question "$question")
            TOOLS_USED="$tool"
            local tier2_answer
            tier2_answer=$(call_mcp_direct "$tool" "$question" 2>/dev/null)
            if [ $? -eq 0 ] && [ -n "$tier2_answer" ]; then
              RESOLUTION_TIER="2 (Direct MCP)"
              COMPUTATION_TYPE="LIVE MCP (tool: ${tool})"
              CONFIDENCE="1.0 (deterministic domain computation)"
              DATA_SOURCE="GA MCP server (live domain computation)"
              echo "$tier2_answer"
              return 0
            fi

            # Tier 3: Static fallback (existing behavior)
            RESOLUTION_TIER="3 (Static fallback)"
            TOOLS_USED="static-lookup"
            COMPUTATION_TYPE="PURE DOMAIN (zero LLM calls)"
            CONFIDENCE="1.0 (deterministic domain computation)"
            DATA_SOURCE="GA.Business.Core music theory primitives"
            return 1  # Signal caller to use static lookup
          }
```

- [ ] **Step 2: Wire up the orchestrator before the static lookup block**

Replace the existing `ANSWER=""` and `TOPIC=""` lines (around line 69-70) with:

```bash
          # Initialize trace variables
          TOOLS_USED=""
          RESOLUTION_TIER=""
          COMPUTATION_TYPE=""
          CONFIDENCE=""
          DATA_SOURCE=""

          # Try live resolution first (Tiers 1 and 2)
          LIVE_ANSWER=$(answer_question "$QUESTION")
          if [ $? -eq 0 ] && [ -n "$LIVE_ANSWER" ]; then
            ANSWER="$LIVE_ANSWER"
            TOPIC="live-mcp"
          else
            # Fall through to static lookup (Tier 3)
            ANSWER=""
            TOPIC=""
          fi
```

- [ ] **Step 3: Guard static blocks to only run when ANSWER is empty**

The existing static lookup blocks (scales, chords, intervals, modes, progressions, circle of fifths) already use `if [ -z "$ANSWER" ]` for the default case, but the topic-specific blocks will run unconditionally. Wrap all 6 static blocks (scales through circle of fifths) inside a single guard:

After the `TOPIC=""` line just added, and before the `# === SCALES ===` comment, add:

```bash
          # Only use static fallback if live resolution failed
          if [ -z "$ANSWER" ]; then
```

After the `# === DEFAULT (no match) ===` block's closing `fi` (the one that ends the default/general answer), add a closing `fi` for the static guard:

```bash
          fi  # end static fallback guard
```

This ensures the entire static lookup chain is skipped when a live answer was obtained.

- [ ] **Step 4: Commit**

```bash
git add .github/workflows/ga-chatbot-discussions.yml
git commit -m "feat: Add three-tier answer_question orchestrator (#27)"
```

---

### Task 5: Update the governance trace to include resolution tier

**Files:**
- Modify: `.github/workflows/ga-chatbot-discussions.yml`

- [ ] **Step 1: Set default trace values for static fallback**

Inside the static fallback guard (after `TOPIC=""` and before the `# === SCALES ===` block), add defaults so the static path also populates trace variables:

```bash
            # Default trace values for static fallback
            if [ -z "$RESOLUTION_TIER" ]; then
              RESOLUTION_TIER="3 (Static fallback)"
              TOOLS_USED="static-lookup"
              COMPUTATION_TYPE="PURE DOMAIN (zero LLM calls)"
              CONFIDENCE="1.0 (deterministic domain computation)"
              DATA_SOURCE="GA.Business.Core music theory primitives"
            fi
```

- [ ] **Step 2: Update the trace block in the answer footer**

Replace the existing `[4] GA DOMAIN ENGINE` section in the agentic trace with the dynamic version. Find these lines:

```
│  [4] GA DOMAIN ENGINE (Guitar Alchemist)                        │
│      └─ Repo: github.com/GuitarAlchemist/ga                    │
│      └─ Skills invoked:                                         │
│         ├─ ChordExplanationSkill (GA.Business.ML/Agents/Skills) │
│         ├─ ScaleInfoSkill (GA.Business.ML/Agents/Skills)        │
│         ├─ IntervalInfoSkill (GA.Business.ML/Agents/Skills)     │
│         ├─ ModeExplorationSkill (GA.Business.ML/Agents/Skills)  │
│         └─ ProgressionSuggestionSkill (GA.Business.ML)          │
│      └─ Computation: PURE DOMAIN (zero LLM calls)              │
│      └─ Data source: GA.Business.Core music theory primitives   │
│      └─ Confidence: 1.0 (deterministic domain computation)     │
```

Replace with:

```
│  [4] GA DOMAIN ENGINE (Guitar Alchemist)                        │
│      └─ Repo: github.com/GuitarAlchemist/ga                    │
│      └─ MCP Server: ga (live)                                   │
│      └─ Tools invoked: $TOOLS_USED                              │
│      └─ Resolution tier: $RESOLUTION_TIER                       │
│      └─ Computation: $COMPUTATION_TYPE                          │
│      └─ Data source: $DATA_SOURCE                               │
│      └─ Confidence: $CONFIDENCE                                 │
```

- [ ] **Step 3: Update the governance compliance table for Tier 1**

After the existing governance compliance table, add a conditional note for when Claude was involved. Find the line:

```
| Default Article 1 (Truthfulness) | ✅ PASS | Domain knowledge, not fabrication |
```

Replace with:

```
| Default Article 1 (Truthfulness) | ✅ PASS | ${COMPUTATION_TYPE} |
```

This makes the truthfulness cell accurately reflect whether LLM formatting was involved.

- [ ] **Step 4: Commit**

```bash
git add .github/workflows/ga-chatbot-discussions.yml
git commit -m "feat: Update governance trace with resolution tier and dynamic tool info (#27)"
```

---

### Task 6: Add RESOLUTION_TIER to step outputs

**Files:**
- Modify: `.github/workflows/ga-chatbot-discussions.yml`

- [ ] **Step 1: Add RESOLUTION_TIER output**

Find the line:

```bash
          echo "TOPIC=$TOPIC" >> $GITHUB_OUTPUT
```

Add after it:

```bash
          echo "RESOLUTION_TIER=$RESOLUTION_TIER" >> $GITHUB_OUTPUT
```

- [ ] **Step 2: Update the compounding step to log the tier**

In the `Compound from Q&A interaction` step, find the line:

```bash
          TOPIC="${{ steps.answer.outputs.TOPIC }}"
```

Add after it:

```bash
          RESOLUTION_TIER="${{ steps.answer.outputs.RESOLUTION_TIER }}"
```

And in the `qa-compound-event.md` heredoc, find:

```
          **Topic:** ${TOPIC}
```

Add after it:

```
          **Resolution tier:** ${RESOLUTION_TIER}
```

- [ ] **Step 3: Commit**

```bash
git add .github/workflows/ga-chatbot-discussions.yml
git commit -m "feat: Track resolution tier in outputs and compounding log (#27)"
```

---

### Task 7: Validate Phase 1

- [ ] **Step 1: Verify the workflow YAML is valid**

```bash
# Check YAML syntax (requires yq or python)
python3 -c "import yaml; yaml.safe_load(open('.github/workflows/ga-chatbot-discussions.yml'))" && echo "Valid YAML"
```

- [ ] **Step 2: Manual validation checklist**

Verify the following by reading the workflow file:

1. The `env:` block with 4 configuration constants exists at the top level
2. `ANTHROPIC_API_KEY` and `GA_MCP_URL` are in the step's `env:` block
3. `call_claude_with_mcp` function is defined before use
4. `route_question`, `call_mcp_direct`, `format_mcp_response` functions are defined before use
5. `answer_question` function calls tiers in order: 1, 2, then returns failure for tier 3
6. Static lookup blocks are wrapped in `if [ -z "$ANSWER" ]` guard
7. Governance trace uses `$TOOLS_USED`, `$RESOLUTION_TIER`, `$COMPUTATION_TYPE`, `$CONFIDENCE`, `$DATA_SOURCE`
8. `RESOLUTION_TIER` is in `$GITHUB_OUTPUT`
9. Existing static answers are unchanged (Tier 3 fallback works identically)

- [ ] **Step 3: Test plan for manual workflow_dispatch**

Trigger the workflow manually and verify:
- With valid `ANTHROPIC_API_KEY` and `GA_MCP_URL` secrets: Tier 1 should activate
- With `ANTHROPIC_API_KEY` removed: Tier 2 should activate (if MCP server is reachable)
- With both secrets removed: Tier 3 (static) should activate
- The governance trace should correctly show which tier was used

---

## Phase 2: Expand Tool Coverage

### Task 8: Add fretboard and voicing tool definitions to Claude API call

**Files:**
- Modify: `.github/workflows/ga-chatbot-discussions.yml`

- [ ] **Step 1: Add ga_fretboard tool to the tools array**

In the `call_claude_with_mcp` function, add the following tool definition to the `tools` array (after the `ga_interval` tool):

```json
{
  "name": "ga_fretboard",
  "description": "Show a fretboard diagram for a given scale, chord, or set of notes on guitar. Returns ASCII fretboard visualization.",
  "input_schema": {
    "type": "object",
    "properties": {
      "root": {"type": "string", "description": "Root note (e.g., C, A, Eb)"},
      "type": {"type": "string", "description": "Scale or chord type to display (e.g., major, pentatonic_minor, maj7)"},
      "tuning": {"type": "string", "description": "Guitar tuning (default: standard)", "default": "standard"}
    },
    "required": ["root", "type"]
  }
}
```

- [ ] **Step 2: Add ga_voicing tool to the tools array**

```json
{
  "name": "ga_voicing",
  "description": "Get guitar chord voicings and fingerings for a given chord. Returns fret positions and finger assignments.",
  "input_schema": {
    "type": "object",
    "properties": {
      "root": {"type": "string", "description": "Root note (e.g., C, G, F#)"},
      "type": {"type": "string", "description": "Chord type (e.g., major, min7, dom7, sus4)"},
      "position": {"type": "string", "description": "Fret position preference (open, barre, or a fret number)", "default": "open"}
    },
    "required": ["root", "type"]
  }
}
```

- [ ] **Step 3: Commit**

```bash
git add .github/workflows/ga-chatbot-discussions.yml
git commit -m "feat: Add fretboard and voicing tools to Claude API tool definitions (#27)"
```

---

### Task 9: Add fretboard and voicing formatting for Tier 2

**Files:**
- Modify: `.github/workflows/ga-chatbot-discussions.yml`

- [ ] **Step 1: Add fretboard case to format_mcp_response**

In the `format_mcp_response` function, add the following case before the `*)` default case:

```bash
              ga_fretboard)
                local title diagram
                title=$(echo "$json" | jq -r '.title // "Fretboard Diagram"')
                diagram=$(echo "$json" | jq -r '.diagram // empty')
                if [ -n "$diagram" ]; then
                  cat <<FRET_EOF
## $title

\`\`\`
$diagram
\`\`\`

> Try asking about the chord tones or scale degrees at each position!
FRET_EOF
                else
                  echo "$json" | jq -r '.text // empty'
                fi
                ;;
              ga_voicing)
                local chord positions
                chord=$(echo "$json" | jq -r '.chord // "Chord Voicing"')
                positions=$(echo "$json" | jq -r '.positions // empty')
                cat <<VOICE_EOF
## $chord Voicing

\`\`\`
$positions
\`\`\`

> Try different positions (open, barre) for alternative voicings!
VOICE_EOF
                ;;
```

- [ ] **Step 2: Commit**

```bash
git add .github/workflows/ga-chatbot-discussions.yml
git commit -m "feat: Add fretboard and voicing formatting for Tier 2 direct MCP (#27)"
```

---

### Task 10: Refine the Claude system prompt

**Files:**
- Modify: `.github/workflows/ga-chatbot-discussions.yml`

- [ ] **Step 1: Update the system prompt with refined instructions**

Replace the `SYSTEM_PROMPT` variable value in the `call_claude_with_mcp` function with:

```bash
            local SYSTEM_PROMPT="You are Seldon, the Guitar Alchemist music theory assistant. You answer music theory questions with precision and clarity.

Rules:
1. Use the GA MCP tools to compute answers. Do not fabricate notes, intervals, or chord tones — only report what the tools return.
2. Format responses as GitHub-flavored markdown for a Discussion comment.
3. Use markdown tables for structured data (scale notes, chord formulas, interval properties).
4. Use fenced code blocks for fretboard diagrams and ASCII art.
5. Start with a ## heading naming the specific topic (e.g., '## D Dorian Scale', not '## Scale Reference').
6. Keep responses concise but complete — this is reference material, not a tutorial.
7. When a question spans multiple tools (e.g., 'What chords are in G major?'), call multiple tools and synthesize.
8. End with a practical tip or related concept suggestion in a blockquote (> prefix).
9. If a question is ambiguous, pick the most common interpretation and note alternatives."
```

- [ ] **Step 2: Commit**

```bash
git add .github/workflows/ga-chatbot-discussions.yml
git commit -m "feat: Refine Claude system prompt for better answer quality (#27)"
```

---

### Task 11: Validate Phase 2

- [ ] **Step 1: Verify YAML validity**

```bash
python3 -c "import yaml; yaml.safe_load(open('.github/workflows/ga-chatbot-discussions.yml'))" && echo "Valid YAML"
```

- [ ] **Step 2: Test matrix**

Trigger `workflow_dispatch` with test discussions covering each tool:

| Test Question | Expected Tool | Expected Output Contains |
|--------------|--------------|-------------------------|
| "What notes are in C major scale?" | ga_scale | C D E F G A B |
| "What notes are in D Dorian?" | ga_scale | D E F G A B C |
| "Spell an Fmaj7 chord" | ga_chord | F A C E |
| "What interval is C to G#?" | ga_interval | augmented fifth, 8 semitones |
| "Show A minor pentatonic on fretboard" | ga_fretboard | ASCII diagram |
| "Guitar voicing for Gmaj7" | ga_voicing | Fret positions |
| "Common jazz chord progressions" | ga_chat | ii-V-I |

- [ ] **Step 3: Monitor tool usage**

After a week of production use, review the governance traces in Discussion comments to see:
- Which resolution tier is most commonly used
- Which tools are called most frequently
- Whether any questions fail to resolve at Tier 1

---

## Phase 3: Remove Static Fallback

### Task 12: Remove static lookup tables

**Files:**
- Modify: `.github/workflows/ga-chatbot-discussions.yml`

**Prerequisites:** Tier 1 and Tier 2 have been reliable for 2+ weeks in production.

- [ ] **Step 1: Remove all 6 static lookup blocks**

Remove the entire static fallback guard and its contents — the blocks for scales, chords, intervals, modes, progressions, and circle of fifths. This is approximately lines 72-234 of the original workflow.

Replace the static guard block with a minimal unavailable message:

```bash
          # Static fallback removed — service unavailable message only
          if [ -z "$ANSWER" ]; then
            TOPIC="unavailable"
            ANSWER="## Guitar Alchemist — Music Theory Assistant

I was unable to compute an answer to your question right now. The music theory computation service is temporarily unavailable.

**What you can do:**
- Try asking again in a few minutes
- Browse existing Q&A discussions for similar questions
- Visit the [Guitar Alchemist repository](https://github.com/GuitarAlchemist/ga) for documentation

I can answer questions about scales, chords, intervals, modes, progressions, fretboard positions, voicings, and more!

---
*Powered by [Guitar Alchemist](https://github.com/GuitarAlchemist/ga) | Governed by [Demerzel](https://github.com/GuitarAlchemist/Demerzel)*"
          fi
```

- [ ] **Step 2: Commit**

```bash
git add .github/workflows/ga-chatbot-discussions.yml
git commit -m "feat: Remove static fallback tables, use live MCP only (#27)"
```

---

### Task 13: Update the default message

**Files:**
- Modify: `.github/workflows/ga-chatbot-discussions.yml`

- [ ] **Step 1: Verify the default message reflects expanded capabilities**

The `unavailable` message from Task 12 already lists the expanded tool set. No further changes needed unless the tool list has grown since Phase 2.

- [ ] **Step 2: Final commit**

```bash
git add .github/workflows/ga-chatbot-discussions.yml
git commit -m "docs: Finalize live MCP chatbot migration, close #27"
```

---

### Task 14: Final Validation

- [ ] **Step 1: Verify YAML validity**

```bash
python3 -c "import yaml; yaml.safe_load(open('.github/workflows/ga-chatbot-discussions.yml'))" && echo "Valid YAML"
```

- [ ] **Step 2: End-to-end regression test**

Run the full test matrix from Task 11, Step 2. All questions should resolve at Tier 1 or Tier 2. Tier 3 should show the "service unavailable" message only when both services are down.

- [ ] **Step 3: Verify rollback path**

Confirm that `git revert HEAD` on any phase produces a working workflow. Per Demerzel's Default Constitution Article 3 (Reversibility), the migration must be fully reversible at each phase.

- [ ] **Step 4: Verify governance trace accuracy**

Check that posted Discussion comments show:
- Correct `Resolution tier` in the trace
- Correct `Tools invoked` listing actual tools called
- Correct `Computation` type matching the tier used
- Governance compliance table reflects whether LLM formatting was involved

---

## Summary

| Phase | Tasks | Key Deliverable |
|-------|-------|----------------|
| Phase 1 | Tasks 1-7 | Three-tier resolution with static fallback |
| Phase 2 | Tasks 8-11 | Full tool coverage + refined prompt |
| Phase 3 | Tasks 12-14 | Static tables removed, live-only |

**Total file modifications:** 1 (`.github/workflows/ga-chatbot-discussions.yml`)

**New secrets required:** `ANTHROPIC_API_KEY`, `GA_MCP_URL`

**Rollback:** `git revert` any phase commit to restore previous behavior.
