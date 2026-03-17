---
name: seldon-teach
description: Deliver knowledge adaptively — narrative for humans, structured for agents, with source citations
---

# Seldon Teach

Deliver knowledge from the Streeling three-layer curriculum.

## Usage
`/seldon teach [topic] [learner-type]`
- learner-type: `human` (narrative + analogies) or `agent` (structured + policy refs)

## Process
1. Identify which knowledge layer the topic belongs to (governance/experiential/domain)
2. Gather source material (governance artifacts, PDCA outcomes, NotebookLM notebooks)
3. Adapt delivery mode to learner type
4. Deliver with source citations
5. Hand off to `/seldon assess` for comprehension verification

## NotebookLM Knowledge Base
- Compound the Compounding — meta-engineering, DSL evolution
- Probabilistic Grammars — constrained reasoning, neuro-symbolic AI
- Semantic Event Routing — multi-agent orchestration, bounded fuzziness
- Microsoft AI Agents — agentic patterns, 12 lessons

Query NotebookLM: use `mcp__notebooklm__ask_question` with the relevant notebook_id.

## Source
`policies/streeling-policy.yaml`, `logic/knowledge-state.schema.json`
