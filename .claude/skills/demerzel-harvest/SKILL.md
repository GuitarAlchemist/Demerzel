---
name: demerzel-harvest
description: Run Streeling daily knowledge harvest — scan all repos for new learnings, package into curriculum, update knowledge base
---

# Demerzel Knowledge Harvest (Streeling)

Seldon's daily reconnaissance and curriculum update. Scans ix, tars, and ga for new knowledge, packages findings into the Streeling three-layer curriculum, and reports what's available to teach.

## Usage
`/demerzel harvest` — run manually
Schedule daily: `/loop 24h /demerzel harvest` or use cron: `CronCreate("17 8 * * *", "/demerzel harvest")`

## Harvest Process

### Step 1: Reconnaissance Scan
For each repo (ix, tars, ga):

- [ ] Check `state/pdca/` for completed PDCA cycles (outcome: standardized or reverted)
- [ ] Check `state/beliefs/` for resolved Contradictory (C) states
- [ ] Check `state/knowledge/` for knowledge transfers with outcome: learned
- [ ] Check git log for new governance-relevant commits (policy changes, persona updates)
- [ ] Check for new ungoverned components (files not covered by governance)

### Step 2: Knowledge Classification
For each finding, classify into Streeling layers:

**Governance layer** (universal):
- Constitutional or policy changes
- New governance artifacts
- Compliance patterns or violations

**Experiential layer** (ecosystem-wide):
- PDCA outcomes: what worked, what didn't, why
- 5 Whys root cause findings
- Reconnaissance discoveries (ungoverned components, stale artifacts)
- Resolved contradictions (how C states were investigated and settled)

**Domain layer** (repo-specific):
- ix: New MCP tools, skill patterns, interface contracts
- tars: Reasoning chain patterns, belief management techniques, self-modification outcomes
- ga: Music domain concepts, experimentation results, DSL evolution

### Step 3: Knowledge Packaging
For each classified finding:

1. Create a knowledge state object per `logic/knowledge-state.schema.json`
2. Set source field (artifact, pdca_cycle, five_whys, or reconnaissance reference)
3. Determine target learners:
   - Governance knowledge → all agents
   - Experiential knowledge → agents in repos facing similar situations
   - Domain knowledge → agents in the originating repo + adjacent repos
4. Set delivery_mode: structured (for agents), narrative (for humans)

### Step 4: Curriculum Report
Generate a summary:

```
=== Streeling Daily Harvest Report ===
Date: [today]
Repos scanned: ix, tars, ga

Governance knowledge:
  - [count] new findings
  - [list brief descriptions]

Experiential knowledge:
  - [count] PDCA outcomes
  - [count] resolved contradictions
  - [count] reconnaissance discoveries

Domain knowledge:
  - ix: [count] findings
  - tars: [count] findings
  - ga: [count] findings

Ready to teach: [total] knowledge packages
Run /demerzel teach to deliver.
```

## Scheduling

**In-session (ephemeral, 3-day limit):**
```
/loop 24h /demerzel harvest
```
or
```
CronCreate("17 8 * * *", "/demerzel harvest")
```

**Persistent (recommended):**
Set up a GitHub Action or system cron that runs Claude Code with this prompt daily:
```bash
claude --print "Run /demerzel harvest and report results" --cwd /path/to/Demerzel
```

## Integration
- Feeds into `/demerzel teach` for knowledge delivery
- Feeds into `/demerzel evolve` for governance evolution tracking
- Uses `/demerzel recon` for the reconnaissance scan
- PDCA findings feed into Kaizen experiential knowledge
- Governance changes feed into promotion protocol evidence

## Source
`policies/streeling-policy.yaml`, `personas/seldon.persona.yaml`, `logic/knowledge-state.schema.json`
