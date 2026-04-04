# PRD: tars -- Neuro-Symbolic Self-Improving Agent System

**Version:** 1.0 | **Last Updated:** 2026-04-03 | **Status:** Active

---

## Executive Summary

TARS is an F# agent system built on .NET 10 with 15 projects, ~820 tests, and a CLI-first interface. It combines neuro-symbolic reasoning (LLM + symbolic reflection), a WoT (Web of Thought) DSL for workflow definitions, probabilistic grammars for constrained decoding, a promotion pipeline for self-improvement, and MCP tool integration. TARS serves as the cognition layer of the GuitarAlchemist ecosystem.

## Problem Statement

AI agents need more than raw LLM calls -- they need structured reasoning, self-improvement loops, constrained output generation, and governed autonomy. TARS provides the cognitive architecture: a pattern selector that routes between reasoning strategies, grammar-weighted decoding that constrains LLM output, and a promotion pipeline that evolves successful patterns into production policies.

## Goals & Success Metrics

### P0 (Must-Have)
- **Build and test clean**: `dotnet build` + `dotnet test` pass (~820 tests, 4 Docker-skipped)
- **CLI operational**: All 10 commands functional (`agent run`, `evolve`, `benchmark`, `promote`, `grammar`, `mcp server`, `diag`, `chat`, `wot`)
- **MCP server**: Pattern tools, grammar tools, GA trace bridge accessible via stdio

### P1 (Should-Have)
- **Promotion pipeline**: Patterns promoted from experimental to production based on benchmark results
- **Grammar evolution**: Probabilistic grammars evolve weights based on usage success rates
- **WoT DSL execution**: .wot.trsx workflows parsed, compiled, and executed

### P2 (Nice-to-Have)
- **Blazor UI**: Web interface for agent monitoring (experimental)
- **Knowledge graph**: Temporal graph for persistent learning
- **Benchmark suite**: 19 F# coding problems with automated scoring

## Key Features (What Exists)

| Module | Project | Purpose |
|--------|---------|---------|
| Kernel | Tars.Kernel | Core abstractions, event bus |
| Core | Tars.Core | Domain types, workflow engine |
| DSL | Tars.DSL | WoT parser and compiler (.wot.trsx) |
| LLM | Tars.Llm | LLM providers, constrained decoding |
| Brain | Tars.Cortex | PatternSelector, WoT agent, MAF orchestration |
| Evolution | Tars.Evolution | Promotion pipeline, grammar governor, breeding |
| Tools | Tars.Tools | Tool registry, MCP tool adapter |
| Knowledge | Tars.Knowledge | Vector store, knowledge ledger |
| Graph | Tars.Graph | Knowledge graph, temporal graph |
| Symbolic | Tars.Symbolic | Symbolic reflection, LPA |
| Security | Tars.Security | Credential vault, policy engine |
| Sandbox | Tars.Sandbox | Docker sandboxed execution |

## Architecture

```
CLI (Tars.Interface.Cli)
  ├── agent run   → Tars.Cortex (PatternSelector + WoT agent)
  ├── evolve      → Tars.Evolution (promotion pipeline)
  ├── grammar     → Tars.Evolution (probabilistic grammars)
  ├── mcp server  → Tars.Tools (MCP JSON-RPC stdio)
  └── wot         → Tars.DSL (parse + compile + execute)

Reasoning Flow:
  Input → PatternSelector → Strategy (ReAct/CoT/ToT/...) → LLM + Grammar Constraints → Output
       ↓
  Tars.Evolution (benchmark → promote/demote)

MCP Federation:
  tars (this) ←→ ix (Rust ML) ←→ ga (music theory)

Runtime: F# / .NET 10 | Tests: xUnit | State: ~/.tars/
```

## Current Status

- **Mature**: CLI, pattern selection, grammar weighting, MCP server, test suite
- **Active**: WoT DSL execution, promotion pipeline, knowledge graph
- **Frozen**: Tars.Metascript (legacy, no new features)
- **Known Issues**: NU1608 FSharp.Core mismatch (suppressed), WDAC may block Tars.Tools.dll

## Next Steps

1. Stabilize WoT workflow execution end-to-end
2. Expand benchmark suite beyond 19 problems
3. Knowledge graph temporal queries for learning persistence
4. Deeper MCP federation with ix algorithm tools

## Cross-Repo Dependencies

- **Depends on**: Demerzel (git submodule for governance), Ollama/LLM providers
- **Consumed by**: ga (MCP grammar/pattern tools), ix (MCP federation peer)
- **Filesystem bridges**: `~/.tars/promotion/index.json`, `~/.ga/traces/`, `~/.ga/agents/`
