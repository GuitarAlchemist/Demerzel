# Ecosystem Roadmap Explorer — Design Spec

**Date:** 2026-03-24
**Status:** Draft
**Location:** ga-react-components (component) + ga-client (page route)

## Summary

Replace the standalone D3.js Poincare Ball roadmap (gh-pages/demos/roadmap/) with a React component in the ga ecosystem. The new component provides a master-detail layout with three visualization modes: rectangular zoomable icicle, Poincare disk (2D hyperbolic), and Poincare ball (3D hyperbolic). Rendered via Three.js with WebGPU primary / WebGL fallback.

## Goals

1. **Master-detail layout** — collapsible navigation tree on left, visualization + detail panel on right
2. **Three visualization modes** — rectangular icicle, circular Poincare disk, 3D Poincare ball
3. **WebGPU-first rendering** — Three.js WebGPURenderer with automatic WebGL fallback
4. **Bidirectional sync** — click tree → animate viz; click viz → expand tree
5. **Clickable everything** — stats, departments, grammars, courses all link to GitHub
6. **Mouse wheel zoom** with zoom level indicator

## Non-Goals

- Replacing other gh-pages demos (separate effort)
- Real-time data fetching (data is embedded/imported)
- Mobile-first design (desktop-primary, responsive as bonus)

## Architecture

### Component Hierarchy

```
EcosystemRoadmapExplorer (page)
├── NavigationPanel (left, 280px resizable)
│   ├── SearchFilter
│   └── HierarchyTree (MUI TreeView)
│       └── TreeNode (recursive, color-coded, status dots)
├── MainPanel (right, flex-grow)
│   ├── Toolbar
│   │   ├── ViewToggle (Icicle | Disk | Ball)
│   │   ├── RendererChip (WebGPU ✓ / WebGL)
│   │   └── ZoomControls (± buttons + level indicator)
│   ├── VisualizationCanvas (Three.js ref)
│   │   ├── IcicleView
│   │   ├── PoincareDiskView
│   │   └── PoincareBallView
│   ├── DetailPanel
│   │   ├── NodeInfo (name, description, domain, status)
│   │   ├── NodeLinks (grammar ↗, GitHub ↗, courses)
│   │   └── NodeChildren (quick list of children with counts)
│   └── StatsBar (clickable stat chips)
└── RoadmapDataProvider (context — shared selection state)
```

### State Management

```typescript
// Jotai atoms (consistent with ga-client patterns)
const selectedNodeAtom = atom<RoadmapNode | null>(null);
const viewModeAtom = atom<'icicle' | 'disk' | 'ball'>('disk');
const zoomLevelAtom = atom<number>(1.0);
const expandedTreeNodesAtom = atom<Set<string>>(new Set());
const searchFilterAtom = atom<string>('');
const rendererTypeAtom = atom<'webgpu' | 'webgl'>('webgpu');
```

### Data Model

Reuse existing hierarchical data from the current roadmap, extended with link metadata:

```typescript
interface RoadmapNode {
  id: string;              // kebab-case path: "streeling-univ.guitar-studies.gtr-001"
  name: string;
  color: string;           // domain color
  domain: 'core' | 'gov' | 'music' | 'sci' | 'human' | 'infra' | 'meta';
  description: string;
  status?: 'active' | 'horizon' | 'in-progress' | 'new';
  sub?: string;            // subtitle badge ("11 Articles", "T 0.98")
  url?: string;            // GitHub link
  grammarUrl?: string;     // link to .ebnf file
  children?: RoadmapNode[];
  // Computed by layout engine — use WeakMap for parent lookups to avoid circular refs
  _depth?: number;
}

// Parent lookup via WeakMap (avoids circular references that break serialization/devtools)
// const parentMap = new WeakMap<RoadmapNode, RoadmapNode>();
```

## Visualization Modes

### 1. Rectangular Icicle

- Layout: `d3.partition()` computes (x0, y0, x1, y1) in [0,1] range
- Coordinate mapping: [0,1] → world space [-10, 10] on X, [-6, 6] on Y (aspect-adjusted)
- Camera: **OrthographicCamera** looking down -Z axis (no orbit, no parallax — clean icicle)
- Z-offset: `0.01 * depth` purely for rendering order, not visual depth
- Rendering: Three.js PlaneGeometry per tile, positioned in XY space
- Zoom: click a tile → animate camera frustum to fill that tile's children; breadcrumb to go back
- Text: Canvas texture per tile (node name + subtitle)
- Color: domain color with opacity gradient by depth

### 2. Poincare Disk (2D hyperbolic)

- Same as current Poincare Ball visualization but rendered in Three.js
- Tiles positioned using Poincare disk model: `r_hyperbolic = tanh(depth * scale)`
- Inner nodes get proportionally more area; outer nodes compress toward boundary
- Boundary circle visible with subtle grid lines (latitude/longitude from current impl)
- Click node → Mobius transformation re-centers that node, children spread out
- Mouse wheel → zoom adjusts the Poincare metric scale factor

### 3. Poincare Ball (3D hyperbolic)

- Tiles mapped inside a translucent unit sphere
- Position: 3D Poincare ball coordinates `(x, y, z)` where `|p| < 1`
- Depth maps to radial distance from center: `r = tanh(depth * k)`
- Each tile is a small 3D panel (PlaneGeometry) oriented to face camera (billboard) or face outward from center
- Translucent sphere shell rendered as wireframe + glass material
- OrbitControls for rotation around the ball
- Click node → animated re-centering (3D gyration isometry — see Key Formulas)
- Inner nodes are larger, outer nodes shrink — the signature of negative curvature

### Camera Per Mode

| Mode | Camera | Controls |
|------|--------|----------|
| Icicle | OrthographicCamera | Pan + wheel zoom (no orbit) |
| Disk | PerspectiveCamera, fixed Z | Pan + wheel zoom (no orbit) |
| Ball | PerspectiveCamera | OrbitControls (rotate, zoom, pan) |

On mode switch: fade out (150ms) → swap camera + layout → fade in (150ms). No cross-morph animation in v1 — the coordinate systems are too different for meaningful interpolation. v2 enhancement.

### Transition Between Modes

- Shared node IDs maintain selection state across modes
- Mode switch: 300ms crossfade (fade out old, fade in new)
- Selected node preserved — new mode opens focused on the same node

## Rendering Pipeline

### WebGPU Primary

```typescript
async function createRenderer(canvas: HTMLCanvasElement) {
  if (navigator.gpu) {
    const renderer = new THREE.WebGPURenderer({ canvas, antialias: true });
    await renderer.init();
    return { renderer, type: 'webgpu' };
  }
  // Fallback
  return {
    renderer: new THREE.WebGLRenderer({ canvas, antialias: true }),
    type: 'webgl'
  };
}
```

- No React Three Fiber — direct Three.js via useEffect + ref (consistent with ga WebGPU experiments)
- Animation loop via `renderer.setAnimationLoop()`
- Resize handler updates renderer + camera aspect

### Text Rendering

- Canvas2D textures for tile labels (proven pattern in codebase)
- Textures generated once at max resolution, cached by node ID
- LOD visibility thresholds (not regeneration):
  - Zoom < 0.5: depth 0-1 labels only
  - Zoom 0.5-1.5: depth 0-2 labels
  - Zoom > 1.5: all labels visible
- High-DPI: `canvas.width = textWidth * devicePixelRatio`

### Interaction

- Raycaster for click/hover detection on tiles
- Mouse wheel: `wheel` event → adjust zoom atom → camera dolly / metric scale
- Hover: highlight tile + show detail in DetailPanel (no tooltip overlay needed — detail panel serves this role)

## Navigation Panel

### Tree Structure

```
▼ GuitarAlchemist                    ●
  ▼ Constitution (11 Articles)       ● gov
    ▶ Asimov Laws (Art 0-5)          ● gov
    ▶ Operational Ethics (Art 1-11)  ● gov
    ── Fuzzy Enum/DU                 ○ SPEC
    ── BS Detector                   ● v2
    ── Staleness                     ○ POLICY
    ...
  ▼ Streeling Univ. (15 Depts)      ● music
    ▼ Guitar Studies                 ● music
      ── GTR-001                     ●
      ── GTR-002                     ●
      ── Satriani Grammar           ● ADVANCED
    ▶ Music                          ● music
    ▶ Audio Eng.                     ◐ NEW
    ...
```

- Panel width controlled by a 4px drag divider; on drag, update `panelWidthAtom`
- `ResizeObserver` on canvas container triggers `renderer.setSize()` on panel resize
- MUI SimpleTreeView (MUI v5 `TreeView`) with custom TreeItem rendering
- Domain color dot before each node name
- Status indicators: ● active, ○ spec/policy, ◐ new/in-progress, ◌ horizon
- Subtitle badges inline (dimmed)
- Search box filters tree in real-time (fuzzy match on name + description)
- Clicking a tree node:
  1. Sets `selectedNodeAtom`
  2. Visualization animates to focus on that node
  3. Detail panel updates

## Detail Panel

When a node is selected, shows:

| Field | Content |
|-------|---------|
| Name | Node name + subtitle badge |
| Domain | Color-coded chip |
| Description | Full description text |
| Grammar | Link to .ebnf file on GitHub (if applicable) |
| Courses | Count + language badges (EN, ES, FR, PT, IT, DE) |
| Research | Cycle count + status |
| Children | Quick list with status dots |
| GitHub | Direct link to source |

## Stats Bar (Clickable)

Bottom of the main panel. Each stat is a clickable chip:

| Stat | Links to |
|------|----------|
| 7 repos | GitHub org page |
| 200+ tools | MCP federation demo |
| 14 personas | Personas directory on GitHub |
| 24 policies | Policies directory on GitHub |
| 20 grammars | Grammar tree demo or grammars/ on GitHub |
| 15 departments | Streeling demo |
| 6 languages | Courses directory on GitHub |
| 45 behavioral tests | Tests directory on GitHub |

## File Structure

```
ga-react-components/src/
  components/EcosystemRoadmap/
    EcosystemRoadmapExplorer.tsx    # Main component
    NavigationPanel.tsx              # Left panel with tree
    VisualizationCanvas.tsx          # Three.js renderer wrapper
    IcicleView.ts                   # Icicle layout + rendering
    PoincareDiskView.ts             # 2D hyperbolic layout
    PoincareBallView.ts             # 3D hyperbolic layout
    DetailPanel.tsx                  # Right-side detail view
    StatsBar.tsx                     # Clickable stats chips
    Toolbar.tsx                      # View toggle, zoom, renderer chip
    roadmapData.ts                   # Hierarchical data + types
    hyperbolicMath.ts                # Mobius transforms, tanh mapping
    textureUtils.ts                  # Canvas text texture generation
    types.ts                         # RoadmapNode, ViewMode, etc.

ga-client/src/
  pages/demos/EcosystemRoadmapDemo.tsx  # Route wrapper
  # + route in App.tsx
  # + card in DemosIndex.tsx
```

## Key Formulas

### Poincare Disk Mapping

For a node at hierarchy depth `d` with angular position `theta`:

```
r_disk = tanh(d * kappa)     // kappa controls spread, typically 0.5-1.0
x = r_disk * cos(theta)
y = r_disk * sin(theta)
```

### Mobius Transform (Re-centering)

To re-center the disk on point `a` (complex):

```
T_a(z) = (z - a) / (1 - conj(a) * z)
```

This maps `a` to the origin while preserving the hyperbolic metric.

### 3D Poincare Ball Positioning

Node positions in R^3:

```
r_ball = tanh(d * kappa)
x = r_ball * sin(phi) * cos(theta)
y = r_ball * sin(phi) * sin(theta)
z = r_ball * cos(phi)
```

Where `phi` distributes children across latitude and `theta` across longitude.

### 3D Gyration Isometry (Re-centering in Ball Model)

To re-center the Poincare ball on point `a` in R^3 (ref: Ungar, "Analytic Hyperbolic Geometry"):

```
T_a(x) = ((1 + 2*dot(a,x) + |x|^2) * a - (1 - |a|^2) * x)
         / (1 + 2*dot(a,x) + |a|^2 * |x|^2)
```

Where `dot(a,x)` is the Euclidean inner product. This is the 3D analogue of the 2D Mobius
transform and preserves the hyperbolic metric of the ball model. Implementation should use
`THREE.Vector3` operations for numerical stability.

### Hyperbolic Tile Scaling

Apparent tile size at position `p` (distance from origin):

```
scale(p) = 2 / (1 - |p|^2)    // conformal factor (Poincare metric)
visual_size = base_size / scale(p)
```

Tiles near the boundary shrink proportionally to `(1 - |p|^2)` — the visual signature of
negative curvature. The effect is rapid but polynomial, not exponential.

## Dependencies

**New:**
- None required — Three.js, D3.js, MUI TreeView, Jotai all already in the workspace

**Existing (already in ga-react-components or ga-client):**
- `three` (r180) — 3D rendering
- `d3` (v7.8.5) — partition layout computation
- `@mui/material` — TreeView, Chips, ToggleButtonGroup
- `jotai` — state management

## Accessibility

- MUI TreeView provides keyboard navigation (Tab, Arrow keys, Enter) and ARIA labels out of the box
- The tree + detail panel serve as the accessible alternative to the Three.js canvas
- Three.js canvas has `role="img"` and `aria-label` describing the current view and selected node
- All clickable stats/links are standard `<a>` or `<button>` elements with proper focus styles

## Error Handling

- Wrap `VisualizationCanvas` in a React error boundary
- Show loading spinner during async `WebGPURenderer.init()`
- If both WebGPU and WebGL fail: render tree + detail panel only (no canvas), show info chip
- Feature-detect `navigator.gpu` before attempting WebGPU

## Testing

- Behavioral test in Demerzel: `tests/behavioral/data-visualization-roadmap.test.md`
- Component tests: Vitest for data transforms, Playwright for interaction
- Visual regression: screenshot comparison of each view mode

## Migration Path

1. Build component in ga-react-components
2. Add route + card in ga-client
3. Update gh-pages roadmap to redirect to ga-client deployment (or keep as legacy)
4. Update all internal links pointing to `/demos/roadmap/`
