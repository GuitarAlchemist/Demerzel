# PRD: ga-react-components -- React Frontend & Prime Radiant

**Version:** 1.0 | **Last Updated:** 2026-04-03 | **Status:** Active

---

## Executive Summary

ga-react-components is a shared React component library and the home of Prime Radiant -- a 3D governance visualization built with React Three Fiber and Three.js. It provides ~49 UI components spanning music theory (fretboard, chord diagrams, VexFlow), governance dashboards (belief heatmaps, compliance rivers, case law), and a 3D solar system visualization. Consumed by the ga-client app and accessible via HTTP API on port 5176.

## Problem Statement

The GuitarAlchemist ecosystem generates governance state, music theory data, and agent activity across multiple repos. Without a unified visual layer, this data remains opaque -- beliefs, compliance status, agent presence, and music theory concepts lack spatial representation. The Prime Radiant provides a 3D "command center" where governance and music theory converge.

## Goals & Success Metrics

### P0 (Must-Have)
- **Component library builds cleanly**: `npm run build` and `npm run lint` pass
- **Prime Radiant renders**: 3D solar system with governance overlays functional at 30+ FPS
- **API connectivity**: SignalR hub and REST/GraphQL connections to ga-server operational

### P1 (Should-Have)
- **Playwright E2E coverage**: Critical user paths tested
- **GIS layer integration**: NASA GIBS satellite tiles on planet surfaces
- **Agent presence**: Real-time multi-agent activity visualization

### P2 (Nice-to-Have)
- **TSL/WebGPU shaders**: Advanced visual effects (Moebius, caustics, volumetrics)
- **IXQL visualization**: D3-based query result rendering
- **Mobile performance**: Responsive 3D at acceptable frame rates

## Key Features (What Exists)

| Category | Components | Examples |
|----------|-----------|----------|
| Prime Radiant 3D | Solar system, GIS layers, governance overlays | Planet surfaces, belief weather, compliance rivers |
| Governance UI | Dashboards, panels, monitors | AlgedonicPanel, BeliefHeatmap, CICDPanel, CodeTribunal |
| Music Theory | Fretboard, chords, notation | FretboardGrid, FretDiagram, VexFlow, DiatonicChordTable |
| Agent/Chat | Chat widget, agent panels | GAChatPanel, AgentPresence, BrainstormPanel |
| Data Viz | Grids, graphs, charts | AG Grid, D3, Recharts, ReactFlow, 3D Force Graph |
| DSL/Code | Editors, IXQL | Monaco Editor, DSL components, Atonal analysis |

## Architecture

```
Tech Stack:
  React 18 + TypeScript strict + Vite
  Three.js 0.180 + React Three Fiber + Drei
  MUI 5 + AG Grid + D3 + Recharts + ReactFlow
  SignalR (real-time) + Axios (REST) + Jotai (state)

Build:
  npm run dev    → Vite dev server
  npm run build  → Production bundle (consumed by ga-client)
  npm run test   → Playwright E2E

Component Structure:
  src/components/<Feature>/<Component>.tsx
  src/components/PrimeRadiant/  (3D visualization, ~40+ files)
  src/hooks/                    (custom hooks)
```

## Current Status

- **Mature**: Fretboard components, chat panel, basic Prime Radiant
- **Active**: Governance dashboards, IXQL UI, shader effects (TSL/GLSL)
- **Experimental**: WebGPU renderer, Godot bridge

## Next Steps

1. Stabilize TSL shader pipeline (requires WebGPURenderer, not WebGL)
2. Remote QA pipeline with FPS metrics collection
3. IXQL full stack: parser, compiler, engine, renderers
4. Godot embed bridge for Prime Radiant hybrid rendering

## Cross-Repo Dependencies

- **Depends on**: ga (GaApi for REST/GraphQL/SignalR), Demerzel (governance state schemas)
- **Consumed by**: ga-client (production bundle), ga-godot (Prime Radiant API on port 5176)
- **Data sources**: MongoDB (via ga-server), NASA GIBS (satellite tiles)
