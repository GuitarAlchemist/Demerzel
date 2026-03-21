# Directive: NotebookLM Knowledge Base Expansion

**Directive ID:** DIR-2026-03-21-005
**Type:** knowledge-expansion
**From:** Seldon (Chancellor, Streeling University)
**To:** All repos (Demerzel, ix, tars, ga)
**Priority:** Medium
**Issued:** 2026-03-21
**Compliance Deadline:** Ongoing

## Context

Issue #15 requests expanding Seldon's NotebookLM knowledge base. Currently 4 notebooks exist:
1. Compound the Compounding (meta-engineering)
2. Probabilistic Grammars (constrained LLM reasoning)
3. Semantic Event Routing (multi-agent orchestration)
4. Microsoft AI Agents for Beginners (agentic patterns)

## Proposed New Notebooks

### Notebook 5: Demerzel Governance Framework
**Source material:**
- `constitutions/` — Asimov + default constitution + mandate
- `policies/` — All 20 policies (including new fuzzy, probes, multilingual)
- `logic/` — Tetravalent logic + fuzzy membership specs
- `schemas/` — All governance schemas
- `docs/specs/` — Design specs (Batch B, probes syntax, etc.)

**Topics:** Constitution hierarchy, tetravalent logic, fuzzy membership, proto-conscience, pre-mortems, alignment, governance audit
**Use cases:** Teaching governance to new agents, constitutional compliance checking, policy reference

### Notebook 6: Guitar Alchemist Music Theory
**Source material:**
- GA repo music domain classes and documentation
- Guitar Alchemist Academy curriculum
- World Music & Languages department content
- Savoir sans Frontières curriculum references

**Topics:** Music theory, chord construction, scales, modes, fretboard geometry, world guitar traditions
**Use cases:** Teaching music theory via chatbot, answering guitar questions, curriculum delivery

### Notebook 7: TARS Grammar & Reasoning
**Source material:**
- TARS grammar specs (state-machines.ebnf, scientific-method.ebnf)
- TARS F# source documentation
- Research weights and department specs
- Grammar-constrained generation docs

**Topics:** F# reasoning, weighted grammars, research cycles, belief state management, grammar distillation
**Use cases:** Understanding TARS architecture, grammar governance decisions, research cycle design

### Notebook 8: ix ML & Rust Algorithms
**Source material:**
- ix crate documentation (memristive-markov, ix-dashboard, ix-governance)
- Rust ML patterns and algorithms
- MCP tool specifications
- ix-music design specs (OPTIC/K planned)

**Topics:** Rust ML, memristive memory, Markov models, MCP tools, governance dashboard
**Use cases:** ML pipeline design, algorithm reference, MCP tool integration

### Notebook 9: Logotron & Foundational Logic
**Source material:**
- Jean-Pierre Petit's Logotron (mathematical logic)
- Savoir sans Frontières collection references
- Fuzzy membership spec connections
- Pre-mortem logotron check design

**Topics:** Mathematical logic, Gödel numbering, incompleteness theorem, formal proofs, paradoxes
**Use cases:** Teaching logic foundations, understanding tetravalent logic roots, Logotron check reasoning

### Notebook 10: Frederik Pohl's Heechee & AI Personhood
**Source material:**
- Gateway series concepts (Robinette Broadhead, AI personas, The Grid)
- Persona architecture design docs
- Futurology department research on AI personhood

**Topics:** AI personas, digital identity, legal personhood, The Grid, governance delegation
**Use cases:** Futurology research, persona philosophy, identity theory discussions

## How to Create

For each notebook:
1. Go to notebooklm.google.com → New notebook
2. Upload relevant source files or paste content
3. Set sharing to "Anyone with the link"
4. Copy the URL
5. Run `/seldon notebook` to add it to the library via `add_notebook` tool

## Integration

- Seldon uses notebooks for grounded, source-cited answers
- Each notebook maps to 1-2 Streeling departments
- Notebooks should be refreshed when governance artifacts change significantly
- Per streeling-policy.yaml, knowledge should be layered: governance, experiential, domain

## Reference

- Issue: GuitarAlchemist/Demerzel#15
- Streeling policy: policies/streeling-policy.yaml
- Current notebooks: 4 (compound, grammars, routing, agents)
- Target: 10 notebooks covering full ecosystem
