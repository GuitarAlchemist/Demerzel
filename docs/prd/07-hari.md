# PRD: hari -- AGI Research Experiments

**Version:** 1.0 | **Last Updated:** 2026-04-03 | **Status:** Early/Research

---

## Executive Summary

Project Hari is a Rust workspace of 4 crates exploring AGI research directions: Lie algebra-based cognitive lattices, swarm intelligence, and cognition primitives. Named after Hari Seldon from Asimov's Foundation series, it is the most experimental repo in the ecosystem -- a research sandbox for ideas that may eventually feed back into ix (ML) or tars (cognition) if they prove viable.

## Problem Statement

Current AI agent architectures (LLM + tools) lack mathematical foundations for cognitive state representation, multi-agent coordination, and structured reasoning about uncertainty. Hari explores whether Lie algebra (continuous symmetry groups), lattice structures, and swarm dynamics can provide more principled cognitive primitives than ad-hoc prompt engineering.

## Goals & Success Metrics

### P0 (Must-Have)
- **Build clean**: `cargo build --workspace` passes
- **Crate structure sound**: Four crates compile with defined public APIs

### P1 (Should-Have)
- **Lattice operations**: Cognitive state lattice with join/meet/partial-order operations
- **Swarm primitives**: Multi-agent coordination protocols
- **Cognition model**: Basic cognitive state representation and transitions

### P2 (Nice-to-Have)
- **Lie algebra integration**: Continuous state transformations via group actions
- **Hyperlight exploration**: Lightweight isolation for cognitive experiments
- **Bridge to ix/tars**: Successful primitives promoted to production crates

## Key Features (What Exists)

| Crate | Purpose | Key Dependencies |
|-------|---------|-----------------|
| hari-core | Core types and traits | serde, thiserror |
| hari-lattice | Cognitive state lattices, partial orders | nalgebra, petgraph |
| hari-swarm | Multi-agent swarm coordination | tokio, rand |
| hari-cognition | Cognitive state representation | hari-lattice, hari-swarm |

## Architecture

```
Rust Workspace (edition 2021)
  hari-core ──► hari-lattice ──► hari-cognition
                                       ▲
  hari-swarm ──────────────────────────┘

Key Dependencies:
  nalgebra 0.33 (linear algebra / Lie groups)
  petgraph 0.7  (graph structures for lattices)
  tokio 1.0     (async for swarm communication)
  rand 0.9      (stochastic processes)

Version: 0.1.0 (pre-release research)
```

## Current Status

- **Early**: Workspace structure defined, four crates scaffolded
- **Research**: Exploring Lie algebra / DNA-like cognitive architecture concepts
- **No production consumers**: Purely experimental

## Next Steps

1. Implement lattice join/meet operations with nalgebra backing
2. Prototype swarm coordination protocol (message passing + consensus)
3. Define cognitive state transition algebra
4. Evaluate which primitives are mature enough to promote to ix or tars

## Cross-Repo Dependencies

- **Depends on**: Nothing (standalone research)
- **Consumed by**: None yet (research outputs may feed ix or tars)
- **Potential future**: hari-lattice concepts could enrich ix-topo or tars knowledge graph
