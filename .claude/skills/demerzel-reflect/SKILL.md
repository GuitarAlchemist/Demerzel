---
name: demerzel-reflect
description: "Reflect on external content (LinkedIn posts, articles, repos) — analyze, cross-reference with Demerzel ecosystem, extract lessons, compound learnings."
---

# /demerzel reflect

Analyze external content and extract actionable lessons for the GuitarAlchemist ecosystem.

## Usage

```
/demerzel reflect <url>                    — analyze a single piece of content
/demerzel reflect --batch <file>           — analyze multiple URLs from a file
/demerzel reflect --topic "claude code"    — search and analyze trending content
```

## Process

### 1. FETCH
- WebFetch the URL, extract content as markdown
- Identify: author, platform, date, topic, engagement

### 2. CLASSIFY
- Is this relevant to our domains? (claude-code, ai-agents, governance, devops, ml-ops, music-tech)
- Score relevance 0-1. Skip if < 0.6.

### 3. CROSS-REFERENCE
For each claim or technique in the content, check against our ecosystem:

| Question | How to Check |
|---|---|
| Do we already do this? | Search skills, policies, grammars |
| Do we do it better? | Compare with evidence from our experience |
| Should we adopt this? | ERGOL check — does it have a real consumer? |
| Can we contribute back? | Do we have insights the author lacks? |

### 4. EXTRACT (structured output)

```markdown
## Reflection on: [Title] by [Author]

### We Agree (with citation)
- [Specific point] — maps to our [artifact/principle]

### We Should Steal
- [Specific technique] — consumer: [who benefits], timeline: [when]

### We Could Teach
- [What we know that they don't] — evidence: [our experience]

### We Challenge
- [Claim we'd push back on] — our evidence: [data/experience]

### BS Score
- Specificity: PASS/FAIL
- Falsifiability: PASS/FAIL
- Density: PASS/FAIL
- Commitment: PASS/FAIL
- Verdict: T/U/C
```

### 5. ACTION
- File issues for adoptable techniques (label: continuous-learning)
- Draft response if engagement is warranted
- Post summary to Discord #research
- Update evolution log

### 6. COMPOUND
- Log the reflection in state/evolution/content-intelligence-log.json
- Update department weights if content touches a research area
- If a novel technique is found, create a skill candidate

## Examples

```
/demerzel reflect https://charliehills.substack.com/p/claude-code-beginner-advanced
→ Reflection: 48-skill library, parallel agents, context management
→ We should steal: skill packaging as installable ZIPs
→ We could teach: constitutional governance, ERGOL/LOLLI, meta-tools

/demerzel reflect https://medium.com/@talirezun/from-lab-to-life
→ Reflection: 3-phase methodology, context engineering, hybrid debugging
→ We should steal: production deployment discipline, cost tracking
→ We could teach: governance hierarchy, tetravalent logic, D_c metrics
```

## Integration
- Pipeline: pipelines/content-intelligence.ixql
- Consumed by: Seldon Plan (auto-research), Demerzel Driver (compound phase)
- Posts to: Discord #research channel
- Logs to: state/evolution/content-intelligence-log.json
