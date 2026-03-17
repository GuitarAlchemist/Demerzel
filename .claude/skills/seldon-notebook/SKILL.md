---
name: seldon-notebook
description: Query NotebookLM knowledge base — research across all indexed notebooks with session continuity for deep exploration
---

# Seldon Notebook — NotebookLM Knowledge Research

Query the ecosystem's institutional memory via NotebookLM. Supports session-based deep research with follow-up questions.

## Usage
`/seldon notebook [question]` — query the best-matching notebook
`/seldon notebook [notebook] [question]` — query a specific notebook
`/seldon notebook list` — show all indexed notebooks

## Available Notebooks

| ID | Name | Topics |
|----|------|--------|
| `compound-the-compounding` | Compound the Compounding | Meta-compounding, DSL evolution, grammar governance, CompoundCore architecture |
| `probabilistic-grammars-and-con` | Probabilistic Grammars & Constrained LLM Reasoning | Constrained decoding, PCFGs, neuro-symbolic AI, formal verification |
| `semantic-event-routing-archite` | Semantic Event Routing Architecture | Multi-agent orchestration, bounded fuzziness, confidence protocols, OPTIC-K |
| `microsoft-ai-agents-for-beginn` | Microsoft AI Agents for Beginners | Agentic patterns, tool use, RAG, trustworthy agents, context engineering |

## How to Query

### Simple query (auto-selects notebook)
```
/seldon notebook How does the promotion staircase work?
```
Seldon matches the question to the most relevant notebook and queries it.

### Specific notebook
```
/seldon notebook compound-the-compounding What is meta-compounding?
```

### Deep research (session-based follow-ups)
```
Step 1: /seldon notebook Give me an overview of grammar governance
  → Save the session_id from the response

Step 2: Ask follow-up using same session
  mcp__notebooklm__ask_question({
    question: "What criteria does the Grammar Governor use?",
    session_id: "<saved_session_id>"
  })

Step 3: Keep going deeper in same session
  mcp__notebooklm__ask_question({
    question: "Show production examples of governance rejection",
    session_id: "<saved_session_id>"
  })
```

## Notebook Selection Guide

| If the question is about... | Use notebook |
|----------------------------|-------------|
| DSL evolution, grammar governance, promotion staircase, CompoundCore | `compound-the-compounding` |
| Constrained decoding, PCFGs, formal proofs, LLM alignment | `probabilistic-grammars-and-con` |
| Multi-agent routing, bounded fuzziness, confidence, OPTIC-K | `semantic-event-routing-archite` |
| Agentic patterns, tool use, RAG, planning, HITL, memory | `microsoft-ai-agents-for-beginn` |
| General or unclear | Query `compound-the-compounding` first (broadest coverage) |

## MCP Tool Reference

### Query a notebook
```javascript
mcp__notebooklm__ask_question({
  question: "Your question here",
  notebook_id: "compound-the-compounding",  // or omit for active notebook
  session_id: "abc123"  // omit for new session, include for follow-ups
})
```

### List all notebooks
```javascript
mcp__notebooklm__list_notebooks()
```

### Add a new notebook
```javascript
mcp__notebooklm__add_notebook({
  url: "https://notebooklm.google.com/notebook/...",
  name: "Notebook Name",
  description: "What's inside",
  topics: ["topic1", "topic2"]
})
```

### Select active notebook
```javascript
mcp__notebooklm__select_notebook({ id: "compound-the-compounding" })
```

## Deep Research Protocol

For complex research, follow this pattern:

1. **Start broad** — "Give me an overview of [topic]" (creates session)
2. **Go specific** — "Key APIs/methods for [subtopic]?" (same session)
3. **Cover pitfalls** — "Common edge cases and gotchas?" (same session)
4. **Get examples** — "Show a production-ready example" (same session)
5. **Cross-reference** — Switch to another notebook if needed (new session)

Each follow-up in the same session builds context — NotebookLM remembers prior Q&A.

## Integration with Governance

- Results feed into `/seldon teach` for knowledge delivery
- NotebookLM findings can become knowledge state objects via `/seldon deliver`
- Confidence from NotebookLM responses should be calibrated per `/demerzel confidence`
- New notebooks added via `mcp__notebooklm__add_notebook` are tracked by Seldon

## Requirements

- NotebookLM MCP server must be running (interactive Claude Code session only)
- Authentication must be active (`mcp__notebooklm__get_health` → authenticated: true)
- If auth expired: `mcp__notebooklm__setup_auth` or `mcp__notebooklm__re_auth`

## Source
`personas/seldon.persona.yaml`, `policies/streeling-policy.yaml`
