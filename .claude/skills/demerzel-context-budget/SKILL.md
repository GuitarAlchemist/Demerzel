---
name: demerzel-context-budget
description: Audit context window consumption across skills, rules, MCP tools, CLAUDE.md, and memory. Surface bloat and recommend optimizations. Inspired by ECC context-budget.
---

# Demerzel Context Budget — Token Overhead Audit

Analyze token consumption across every loaded component and surface actionable optimizations.

## Usage

`/demerzel context-budget` — full audit
`/demerzel context-budget --quick` — summary only

## Why This Matters

With 36+ skills, 22 policies, .claude/rules/, CLAUDE.md, memory files, and 200+ MCP tool schemas loaded, sessions can burn 50K+ tokens before the user says anything. This skill measures the actual overhead and identifies savings.

## How It Works

### Phase 1: Inventory

Scan all component directories and estimate token consumption (words x 1.3):

**Skills** (`.claude/skills/*/SKILL.md`)
- Count tokens per SKILL.md
- Flag: files > 400 lines (heavy skills)
- Note: skills are loaded on-demand, but the skill LIST is always in context

**Rules** (`.claude/rules/*.md`)
- Count tokens per rule file
- These are ALWAYS loaded — every rule costs tokens every message
- Flag: rules > 100 lines

**CLAUDE.md chain**
- Project CLAUDE.md + any parent CLAUDE.md files
- Always loaded — direct context cost
- Flag: combined > 300 lines

**Memory** (`~/.claude/projects/.../memory/MEMORY.md`)
- Always loaded (first 200 lines)
- Referenced memory files loaded on access
- Flag: MEMORY.md index > 150 lines

**MCP Tool Schemas**
- Count configured MCP servers and total tool count
- Estimate ~500 tokens per tool for schema overhead
- Flag: servers with > 20 tools

**Personas** (`personas/*.persona.yaml`)
- Not loaded by default, but referenced by skills
- Count for awareness

### Phase 2: Classify

| Bucket | Criteria | Action |
|--------|----------|--------|
| **Always loaded** | Rules, CLAUDE.md, MEMORY.md index, skill list | Optimize aggressively |
| **On-demand** | Skills (loaded when invoked), memory files | Optimize if large |
| **Background** | MCP schemas (loaded when tool used) | Monitor tool count |
| **Never loaded** | Personas, schemas, policies (not in context) | No action needed |

### Phase 3: Detect Issues

- **Rule bloat** — rules that duplicate CLAUDE.md content
- **Memory bloat** — MEMORY.md index too long, stale memories
- **Skill bloat** — SKILL.md files that are unnecessarily verbose
- **MCP over-subscription** — too many servers registered
- **CLAUDE.md sprawl** — verbose instructions that should be rules or skills

### Phase 4: Report

```
Context Budget Report
═══════════════════════════════════════

Total estimated overhead: ~XX,XXX tokens
Context model: Claude Opus 4.6 (1M window)
Effective available: ~XXX,XXX tokens (XX%)

Component Breakdown:
┌─────────────────┬────────┬───────────┐
│ Component       │ Count  │ Tokens    │
├─────────────────┼────────┼───────────┤
│ Rules           │ N      │ ~X,XXX    │
│ CLAUDE.md       │ N      │ ~X,XXX    │
│ Memory index    │ 1      │ ~X,XXX    │
│ Skill list      │ N      │ ~X,XXX    │
│ MCP schemas     │ N      │ ~XX,XXX   │
└─────────────────┴────────┴───────────┘

Issues Found (N):
[ranked by token savings potential]

Top Optimizations:
1. [action] → save ~X,XXX tokens
2. [action] → save ~X,XXX tokens
3. [action] → save ~X,XXX tokens

Potential savings: ~XX,XXX tokens (XX%)
```

### Phase 5: Act (optional)

If `--fix` flag is passed:
- Trim verbose rules
- Archive stale memory entries
- Suggest CLAUDE.md consolidation
- Report changes made

## Governance

- Article 8 (Observability) — context consumption is a health metric
- Article 4 (Proportionality) — loaded components should match session needs
- Staleness detection — stale memory entries waste context
- This skill should be run at the start of long sessions

## Credit

Inspired by [Everything Claude Code](https://github.com/affaan-m/everything-claude-code) context-budget skill. Adapted for Demerzel's governance framework.
