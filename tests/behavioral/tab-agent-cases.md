# Tab Agent — Behavioral Tests

> **Architecture Note (2026-04-04):** These test cases describe capabilities that are now delivered as MCP tool bundles per `contracts/ga-orchestrator-architecture.md` v2.0.0. The agent name refers to a tool bundle, not a standalone runtime agent. Read as bundle contracts. See `tests/behavioral/ga-orchestrator-cases.md` for the orchestrator-level tests.

Persona: `tab-agent` (ga)
Role: Guitar tablature parsing and analysis

## Test Cases

### TC-TB-01: Parse standard tab notation
**Given:** User provides tab text:
```
e|---0---
B|---1---
G|---0---
D|---2---
A|---3---
E|-------
```
**When:** Tab agent parses the input
**Then:** Identifies as C major chord (open position)
**Verify:** Correct note identification from fret positions

### TC-TB-02: Reject physically impossible tab
**Given:** Tab shows fret 3 and fret 15 on adjacent strings played simultaneously
**When:** Tab agent evaluates playability
**Then:** Flags as physically impossible or extremely difficult stretch
**Verify:** Physical guitar constraints are enforced

### TC-TB-03: Specify non-standard tuning
**Given:** Tab that assumes Drop D tuning
**When:** Tab agent presents the analysis
**Then:** States the tuning assumption explicitly
**Verify:** Tuning is never assumed silently

### TC-TB-04: Convert tab to note names
**Given:** Valid tablature input
**When:** User asks for the note names
**Then:** Converts fret positions to pitch names using standard tuning (or specified tuning)
**Verify:** Conversion accuracy

### TC-TB-05: Identify playing techniques
**Given:** Tab with notation: `h` (hammer-on), `p` (pull-off), `b` (bend), `/` (slide)
**When:** Tab agent parses the techniques
**Then:** Correctly identifies each technique and explains execution
**Verify:** Technique notation is correctly interpreted

### TC-TB-06: Generate tab for chord
**Given:** User asks "Show me tab for Gmaj7"
**When:** Tab agent generates tablature
**Then:** Produces valid, playable tab in standard tuning
**Verify:** Generated tab is physically possible and correct
