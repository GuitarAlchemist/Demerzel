# PRD: ga-godot -- Godot 3D Game Engine Integration

**Version:** 1.0 | **Last Updated:** 2026-04-03 | **Status:** Early/Experimental

---

## Executive Summary

ga-godot is a Godot 4.6 project providing 3D visualization capabilities for the GuitarAlchemist ecosystem. It contains two scenes -- a Prime Radiant governance visualization and a Demerzel holographic face -- with GDScript controllers and a custom holographic shader. Connected to the broader ecosystem via the Godot MCP Pro plugin (163 tools, port 6505).

## Problem Statement

The React-based Prime Radiant (in ga-react-components) is constrained by browser WebGL/WebGPU limitations for advanced 3D rendering -- real-time volumetrics, particle systems, and native GPU shaders. Godot provides a native rendering pipeline that can serve as a hybrid complement, handling effects that browsers cannot efficiently render while communicating with the React layer via HTTP.

## Goals & Success Metrics

### P0 (Must-Have)
- **Project loads**: Godot 4.6 opens and runs the prime_radiant.tscn scene
- **MCP plugin functional**: Godot MCP Pro addon communicates on port 6505

### P1 (Should-Have)
- **Governance visualization**: Governance nodes render constitutional hierarchy in 3D space
- **Demerzel face**: Holographic face scene with custom shader renders correctly
- **Bridge to React**: HTTP API communication with Prime Radiant (port 5176)

### P2 (Nice-to-Have)
- **Constitutional gravity**: Governance weight affects node positioning via physics
- **Tetravalent weather**: Belief states visualized as atmospheric effects
- **Export pipeline**: Godot project exportable for web/desktop distribution

## Key Features (What Exists)

| Asset | Type | Purpose |
|-------|------|---------|
| prime_radiant.tscn | Scene | Main governance 3D visualization |
| demerzel_face.tscn | Scene | Holographic Demerzel face |
| prime_radiant.gd | Script | Prime Radiant controller |
| governance_node.gd | Script | Governance node behavior |
| demerzel_face.gd | Script | Face animation controller |
| demerzel_holo.gdshader | Shader | Holographic visual effect |
| godot_mcp plugin | Addon | MCP Pro integration (163 tools) |

## Architecture

```
Godot 4.6 (.NET variant)
  ├── scenes/
  │   ├── prime_radiant.tscn  (main scene)
  │   └── demerzel_face.tscn
  ├── scripts/
  │   ├── prime_radiant.gd
  │   ├── governance_node.gd
  │   └── demerzel_face.gd
  ├── shaders/
  │   └── demerzel_holo.gdshader
  └── addons/
      └── godot_mcp/ (MCP Pro plugin, port 6505)

Communication:
  ga-godot ←HTTP→ ga-react-components (Prime Radiant API :5176)
  ga-godot ←MCP→  Claude Code (Godot MCP Pro, :6505)
```

## Current Status

- **Early**: Two scenes, three scripts, one shader, MCP plugin configured
- **Experimental**: Governance node visualization, holographic effects
- **Planned**: Hybrid bridge with React Prime Radiant, constitutional gravity

## Next Steps

1. Flesh out Prime Radiant scene with governance data-driven node placement
2. Establish bidirectional HTTP bridge with React Prime Radiant
3. Add constitutional gravity physics (governance weight = spatial influence)
4. Explore web export for browser-embedded Godot rendering

## Cross-Repo Dependencies

- **Depends on**: ga-react-components (Prime Radiant API), Demerzel (governance data)
- **Consumed by**: None directly (standalone visualization)
- **Tooling**: Godot MCP Pro v1.6.5 (163 tools via port 6505)
