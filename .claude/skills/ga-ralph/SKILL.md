---
name: ga-ralph
description: Execute the GA chatbot Ralph Loop — governed autonomous development of the Guitar Alchemist chatbot (music theory, creation, practice companion)
---

# GA Chatbot Ralph Loop

Execute the Demerzel-initiated governed Ralph Loop for building the Guitar Alchemist chatbot.

## Directive
```
ID:         dir-ga-chatbot-ralph-loop-2026-03-15
Loop ID:    loop-ga-chatbot-functional-2026-03-15
Goal:       Build a fully functional GA chatbot covering music theory teaching,
            creation/experimentation, and practice companion features
Risk:       Medium
Governance: boundary-only
Max:        15 iterations
Worker:     default
Reviewer:   skeptical-auditor
```

## Governance Boundaries
1. All changes must be reversible — use feature branches
2. Must not break existing build or tests — `dotnet build AllProjects.slnx && dotnet test AllProjects.slnx`
3. Must follow ga repo CLAUDE.md coding standards (C# 14, .NET 10, ROP patterns)
4. Must not modify GA's domain core layer without explicit justification
5. Must use existing Ollama/RAG infrastructure, not introduce new AI backends
6. All new code must have tests
7. Experimentation features must have safety constraints

## Success Criteria
- Chatbot responds accurately to music theory questions
- Can suggest chord progressions and harmonic analysis
- Provides practice guidance and exercises
- All tests pass, build clean

## How to Execute

### Step 1: Switch to ga repo
```bash
cd /c/Users/spare/source/repos/ga
```

### Step 2: Start a new Claude Code session there
```bash
claude
```

### Step 3: Give this prompt to start the loop
```
Execute Demerzel governance directive dir-ga-chatbot-ralph-loop-2026-03-15.

This is a governed Ralph Loop (boundary-only mode, max 15 iterations).

GOAL: Make the GA chatbot fully functional — music theory teaching,
creation/experimentation, and practice companion features.

The chatbot already has Ollama + RAG + SignalR infrastructure (see Apps/GaChatbot/
and Apps/ga-server/GaApi/CHATBOT_README.md). Build on what exists.

GOVERNANCE BOUNDARIES:
- Reversible changes only (feature branches)
- Don't break build/tests (dotnet build && dotnet test before each commit)
- Follow CLAUDE.md standards (C# 14, .NET 10, ROP)
- Don't modify domain core layer without justification
- Use existing Ollama/RAG — no new AI backends
- All new code needs tests

ITERATION PROTOCOL:
For each iteration:
1. Identify the next highest-impact feature to add
2. Implement it (follow TDD where possible)
3. Verify: dotnet build && dotnet test
4. Commit with descriptive message
5. Self-review: convergence (am I making progress?), regression (did I break prior work?), drift (am I still on goal?)
6. Decide: SHIP (feature complete, move to next) or REVISE (needs more work)

FEATURES TO BUILD (prioritized):
1. Music theory Q&A — answer questions about scales, chords, intervals, modes
2. Chord progression suggestions — given a key/style, suggest progressions
3. Harmonic analysis — analyze a chord sequence for function and voice leading
4. Practice routines — generate exercises for specific techniques or concepts
5. Scale/mode exploration — explain and demonstrate scales with fretboard context
6. Ear training — interval and chord quality recognition exercises

Start with feature 1. Report progress after each iteration.
```

### Step 4: Monitor convergence
After each iteration, check:
- Is the chatbot responding to music theory questions? (convergence)
- Did previous features break? (regression)
- Are we still building chatbot features? (drift)

If 3 iterations pass without measurable progress → halt and reassess.

## Loop State
Directive: `examples/sample-data/directive-ga-chatbot-loop.json`
Initial state: `examples/sample-data/loop-ga-chatbot-init.json`

## Source
`policies/autonomous-loop-policy.yaml`, `constitutions/demerzel-mandate.md`
