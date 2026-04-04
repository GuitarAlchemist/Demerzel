# GuitarAlchemist Ecosystem Overview

**Version:** 1.0 | **Last Updated:** 2026-04-03 | **Owner:** Stephane Pareilleux

---

## Vision

An AI-native software ecosystem where governance, cognition, machine learning, music theory, and 3D visualization work together through cross-repo protocols, enabling governed autonomous agent development.

## Repository Map

```
                          ┌──────────────┐
                          │   Demerzel   │  Governance Framework
                          │ (YAML/MD/JSON)│  Constitutions, Personas, Policies
                          └──────┬───────┘
                                 │ Galactic Protocol (contracts, directives)
            ┌────────────┬───────┼───────┬──────────────┐
            ▼            ▼       ▼       ▼              ▼
      ┌──────────┐ ┌─────────┐ ┌────┐ ┌──────────┐ ┌──────┐
      │    ix    │ │  tars   │ │ ga │ │ ga-godot │ │ hari │
      │  (Rust)  │ │  (F#)   │ │(.NET)│ │ (Godot)  │ │(Rust)│
      │ ML Forge │ │Cognition│ │Music│ │   3D     │ │ AGI  │
      └────┬─────┘ └────┬────┘ └──┬─┘ └─────┬────┘ └──────┘
           │             │         │          │
           └─────────────┼─────────┼──────────┘
                         ▼         ▼
                   ┌─────────────────────┐
                   │ ga-react-components │
                   │  (React/Three.js)   │
                   │  Prime Radiant UI   │
                   └─────────────────────┘
```

## Cross-Repo Communication

| Mechanism | Source | Target | Purpose |
|-----------|--------|--------|---------|
| Galactic Protocol | Demerzel | ix, tars, ga | Governance directives and compliance reports |
| Git Submodule | ix, tars | Demerzel | Shared constitutions, personas, schemas |
| MCP Federation | ix, tars, ga | Each other | Tool invocation (37 ix + tars grammar + ga music) |
| Filesystem Bridges | tars | ga | `~/.tars/promotion/`, `~/.ga/traces/` |
| HTTP API | ga (GaApi) | ga-react-components | REST + GraphQL + SignalR |
| HTTP API | ga-react-components | ga-godot | Prime Radiant control (port 5176) |

## Technology Stack Summary

| Repo | Language | Framework | Runtime |
|------|----------|-----------|---------|
| Demerzel | YAML/MD/JSON | None (spec only) | N/A |
| ix | Rust 1.80+ | ndarray, wgpu, tokio | Native binary |
| tars | F# (.NET 10) | xUnit, FParsec | dotnet |
| ga | C# 14 / F# (.NET 10) | ASP.NET Core, Aspire, HotChocolate | dotnet |
| ga-react-components | TypeScript | React 18, Three.js, Vite, MUI 5 | Node 18+ |
| ga-godot | GDScript/C# | Godot 4.6 | Godot Engine |
| hari | Rust | nalgebra, petgraph, tokio | Native binary |

## Dependency Order (Build Sequence)

1. **Demerzel** (no dependencies -- governance specs only)
2. **ix** (depends on Demerzel submodule)
3. **tars** (depends on Demerzel submodule)
4. **ga** (depends on Demerzel submodule, bridges to tars/ix via MCP)
5. **ga-react-components** (depends on ga API)
6. **ga-godot** (depends on ga-react-components Prime Radiant API)
7. **hari** (standalone research, no production dependencies)
