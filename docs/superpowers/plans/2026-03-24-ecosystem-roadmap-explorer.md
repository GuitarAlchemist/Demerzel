# Ecosystem Roadmap Explorer — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a React-based ecosystem roadmap explorer with master-detail layout and three visualization modes (rectangular icicle, Poincaré disk, Poincaré ball) rendered via Three.js with WebGPU.

**Architecture:** Component built in ga-react-components, consumed by ga-client as a demo page. Direct Three.js (no R3F) via useEffect+ref for WebGPU compatibility. Jotai atoms for state, MUI for UI chrome, d3.partition() for layout math.

**Tech Stack:** React 18, Three.js r180 (WebGPURenderer), D3 v7, MUI v5, Jotai, TypeScript, Vite

**Spec:** `docs/superpowers/specs/2026-03-24-ecosystem-roadmap-explorer-design.md`

---

## File Structure

```
ga-react-components/src/
  components/EcosystemRoadmap/
    types.ts                        # RoadmapNode, ViewMode, DomainColor types
    roadmapData.ts                  # Hierarchical data tree + helper functions
    hyperbolicMath.ts               # Poincaré disk/ball math, Möbius transforms
    textureUtils.ts                 # Canvas2D text texture generation + cache
    atoms.ts                        # Jotai atoms for selection, view mode, zoom
    NavigationPanel.tsx             # Left panel: search + MUI TreeView
    DetailPanel.tsx                 # Selected node metadata + links
    StatsBar.tsx                    # Clickable stat chips
    Toolbar.tsx                     # View toggle, renderer chip, zoom controls
    IcicleView.ts                  # Rectangular icicle Three.js scene builder
    PoincareDiskView.ts            # 2D hyperbolic Three.js scene builder
    PoincareBallView.ts            # 3D hyperbolic Three.js scene builder
    VisualizationCanvas.tsx         # Three.js renderer wrapper (WebGPU/WebGL)
    EcosystemRoadmapExplorer.tsx    # Main component: master-detail layout
    index.ts                        # Barrel export

  pages/
    EcosystemRoadmapTest.tsx        # Test page for component library (port 5176)

ga-client/src/
  pages/demos/
    EcosystemRoadmapDemo.tsx        # Route wrapper for ga-client (port 5173)
```

---

### Task 1: Types and Data Model

**Files:**
- Create: `ga-react-components/src/components/EcosystemRoadmap/types.ts`
- Create: `ga-react-components/src/components/EcosystemRoadmap/roadmapData.ts`

- [ ] **Step 1: Create types.ts**

```typescript
// C:\Users\spare\source\repos\ga\ReactComponents\ga-react-components\src\components\EcosystemRoadmap\types.ts

export type Domain = 'core' | 'gov' | 'music' | 'sci' | 'human' | 'infra' | 'meta';
export type ViewMode = 'icicle' | 'disk' | 'ball';
export type RendererType = 'webgpu' | 'webgl';
export type NodeStatus = 'active' | 'horizon' | 'in-progress' | 'new';

export const DOMAIN_COLORS: Record<Domain, string> = {
  core: '#f0883e',
  gov: '#4cb050',
  music: '#7289da',
  sci: '#e06c75',
  human: '#c678dd',
  infra: '#56b6c2',
  meta: '#e5c07b',
};

export const DOMAIN_LABELS: Record<Domain, string> = {
  core: 'Core',
  gov: 'Governance',
  music: 'Music',
  sci: 'Science',
  human: 'Human',
  infra: 'Infrastructure',
  meta: 'Meta',
};

export interface RoadmapNode {
  id: string;
  name: string;
  color: string;
  domain: Domain;
  description: string;
  status?: NodeStatus;
  sub?: string;
  url?: string;
  grammarUrl?: string;
  children?: RoadmapNode[];
  _depth?: number;
}

export interface StatItem {
  label: string;
  value: string;
  url: string;
}
```

- [ ] **Step 2: Create roadmapData.ts with the hierarchy**

**Data porting:** Read `C:\tmp\gh-pages\demos\roadmap\index.html` lines 108-218. That file has a JavaScript object tree with `{name, color, desc, sub, url, children}` shape. Transform each node:
- Map `color` hex → `domain` enum using `colorToDomain` lookup (e.g., `#4cb050` → `'gov'`)
- Rename `desc` → `description`
- Add `id` via `assignIds()` (auto-generated kebab-case path)
- Add `grammarUrl` for department nodes (e.g., Guitar Studies → `https://github.com/GuitarAlchemist/Demerzel/blob/master/grammars/music-guitar-technique.ebnf`)
- Add `status` field where applicable ('new' for Audio Eng, 'horizon' for K-Theory, etc.)

Helper functions:

```typescript
// C:\Users\spare\source\repos\ga\ReactComponents\ga-react-components\src\components\EcosystemRoadmap\roadmapData.ts

import { type RoadmapNode, type Domain, DOMAIN_COLORS, type StatItem } from './types';

// Reverse-lookup domain from color hex
const colorToDomain: Record<string, Domain> = Object.fromEntries(
  Object.entries(DOMAIN_COLORS).map(([k, v]) => [v, k as Domain])
);

function assignIds(node: RoadmapNode, parentId: string, depth: number): void {
  const slug = node.name.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/-+$/, '');
  node.id = parentId ? `${parentId}.${slug}` : slug;
  node._depth = depth;
  node.children?.forEach(c => assignIds(c, node.id, depth + 1));
}

// Full tree — ported from gh-pages/demos/roadmap/index.html
export const roadmapTree: RoadmapNode = {
  id: 'guitaralchemist',
  name: 'GuitarAlchemist',
  color: DOMAIN_COLORS.core,
  domain: 'core',
  description: 'AI-native tools for music, ML, and agent governance.',
  url: 'https://github.com/GuitarAlchemist',
  children: [
    // ... (full tree ported from existing data — ~110 nodes)
    // Each node gets: id, name, color, domain, description, status?, sub?, url?, grammarUrl?, children?
  ],
};

// Initialize IDs and depths
assignIds(roadmapTree, '', 0);

// Parent lookup (WeakMap to avoid circular refs)
export const parentMap = new WeakMap<RoadmapNode, RoadmapNode>();
function buildParentMap(node: RoadmapNode): void {
  node.children?.forEach(child => {
    parentMap.set(child, node);
    buildParentMap(child);
  });
}
buildParentMap(roadmapTree);

// Flatten tree to array
export function flattenTree(node: RoadmapNode): RoadmapNode[] {
  const result: RoadmapNode[] = [node];
  node.children?.forEach(c => result.push(...flattenTree(c)));
  return result;
}

// Get ancestors (for breadcrumb)
export function getAncestors(node: RoadmapNode): RoadmapNode[] {
  const path: RoadmapNode[] = [];
  let current: RoadmapNode | undefined = node;
  while (current) {
    path.unshift(current);
    current = parentMap.get(current);
  }
  return path;
}

// Search/filter
export function searchTree(root: RoadmapNode, query: string): Set<string> {
  const q = query.toLowerCase();
  const matches = new Set<string>();
  function walk(node: RoadmapNode): boolean {
    const nameMatch = node.name.toLowerCase().includes(q);
    const descMatch = node.description.toLowerCase().includes(q);
    const childMatch = node.children?.some(c => walk(c)) ?? false;
    if (nameMatch || descMatch || childMatch) {
      matches.add(node.id);
      return true;
    }
    return false;
  }
  walk(root);
  return matches;
}

// Stats bar data
export const STATS: StatItem[] = [
  { label: '7 repos', value: '7', url: 'https://github.com/GuitarAlchemist' },
  { label: '200+ tools', value: '200+', url: 'https://github.com/GuitarAlchemist/tars' },
  { label: '14 personas', value: '14', url: 'https://github.com/GuitarAlchemist/Demerzel/tree/master/personas' },
  { label: '24 policies', value: '24', url: 'https://github.com/GuitarAlchemist/Demerzel/tree/master/policies' },
  { label: '20 grammars', value: '20', url: 'https://github.com/GuitarAlchemist/Demerzel/tree/master/grammars' },
  { label: '15 departments', value: '15', url: 'https://github.com/GuitarAlchemist/Demerzel/tree/master/state/streeling/departments' },
  { label: '6 languages', value: '6', url: 'https://github.com/GuitarAlchemist/Demerzel/tree/master/state/streeling/courses' },
  { label: '45 tests', value: '45', url: 'https://github.com/GuitarAlchemist/Demerzel/tree/master/tests/behavioral' },
];
```

- [ ] **Step 3: Commit**

```bash
cd /c/Users/spare/source/repos/ga
git add ReactComponents/ga-react-components/src/components/EcosystemRoadmap/types.ts ReactComponents/ga-react-components/src/components/EcosystemRoadmap/roadmapData.ts
git commit -m "feat: Add types and data model for EcosystemRoadmap component"
```

---

### Task 2: Hyperbolic Math Utilities

**Files:**
- Create: `ga-react-components/src/components/EcosystemRoadmap/hyperbolicMath.ts`

- [ ] **Step 1: Implement Poincaré math functions**

```typescript
// C:\Users\spare\source\repos\ga\ReactComponents\ga-react-components\src\components\EcosystemRoadmap\hyperbolicMath.ts

import * as THREE from 'three';

// --- Poincaré Disk (2D) ---

/** Map hierarchy depth to Poincaré disk radius */
export function depthToRadius(depth: number, kappa: number = 0.6): number {
  return Math.tanh(depth * kappa);
}

/** Conformal scale factor at position p (distance from origin) */
export function conformalFactor(r: number): number {
  return 2 / (1 - r * r);
}

/** Visual size of a tile at Poincaré radius r */
export function tileScale(baseSize: number, r: number): number {
  return baseSize * (1 - r * r) / 2;
}

/** 2D Möbius transform: re-center disk on point a (complex number) */
export function mobiusTransform2D(
  z: [number, number],
  a: [number, number]
): [number, number] {
  // T_a(z) = (z - a) / (1 - conj(a) * z)
  const [zr, zi] = z;
  const [ar, ai] = a;
  // z - a
  const nr = zr - ar;
  const ni = zi - ai;
  // 1 - conj(a) * z = 1 - (ar - ai*i)(zr + zi*i) = 1 - (ar*zr + ai*zi) - (ar*zi - ai*zr)i
  const dr = 1 - (ar * zr + ai * zi);
  const di = -(ar * zi - ai * zr);
  // complex division
  const denom = dr * dr + di * di;
  return [(nr * dr + ni * di) / denom, (ni * dr - nr * di) / denom];
}

// --- Poincaré Ball (3D) ---

/** Map hierarchy depth to 3D ball radius */
export function depthToRadius3D(depth: number, kappa: number = 0.5): number {
  return Math.tanh(depth * kappa);
}

/** Distribute N children on a sphere at given radius using Fibonacci spiral */
export function fibonacciSphere(n: number, radius: number): THREE.Vector3[] {
  const points: THREE.Vector3[] = [];
  const goldenAngle = Math.PI * (3 - Math.sqrt(5));
  for (let i = 0; i < n; i++) {
    const y = 1 - (2 * i) / (n - 1 || 1);
    const r = Math.sqrt(1 - y * y);
    const theta = goldenAngle * i;
    points.push(new THREE.Vector3(
      r * Math.cos(theta) * radius,
      y * radius,
      r * Math.sin(theta) * radius
    ));
  }
  return points;
}

/**
 * 3D gyration isometry (re-center Poincaré ball on point a).
 * Ref: Ungar, "Analytic Hyperbolic Geometry"
 *
 * T_a(x) = ((1 + 2<a,x> + |x|²) · a - (1 - |a|²) · x) / (1 + 2<a,x> + |a|²|x|²)
 */
export function gyrationTransform3D(
  x: THREE.Vector3,
  a: THREE.Vector3,
  target?: THREE.Vector3
): THREE.Vector3 {
  const out = target ?? new THREE.Vector3();
  const ax = a.dot(x);
  const x2 = x.lengthSq();
  const a2 = a.lengthSq();
  const denom = 1 + 2 * ax + a2 * x2;
  // numerator = (1 + 2<a,x> + |x|²) * a - (1 - |a|²) * x
  out.copy(a).multiplyScalar(1 + 2 * ax + x2)
    .addScaledVector(x, -(1 - a2));
  out.divideScalar(denom);
  return out;
}

// --- Layout helpers ---

/** Compute 2D positions for children around a parent at given radius */
export function layoutChildren2D(
  count: number,
  parentR: number,
  childDepth: number,
  kappa: number = 0.6
): Array<{ x: number; y: number; r: number }> {
  const r = depthToRadius(childDepth, kappa);
  return Array.from({ length: count }, (_, i) => {
    const theta = (i / count) * 2 * Math.PI - Math.PI / 2;
    return { x: r * Math.cos(theta), y: r * Math.sin(theta), r };
  });
}
```

- [ ] **Step 2: Commit**

```bash
cd /c/Users/spare/source/repos/ga
git add ReactComponents/ga-react-components/src/components/EcosystemRoadmap/hyperbolicMath.ts
git commit -m "feat: Poincaré disk/ball math utilities with Möbius and gyration transforms"
```

---

### Task 3: Texture Utilities and Jotai Atoms

**Files:**
- Create: `ga-react-components/src/components/EcosystemRoadmap/textureUtils.ts`
- Create: `ga-react-components/src/components/EcosystemRoadmap/atoms.ts`

- [ ] **Step 1: Create textureUtils.ts**

```typescript
// C:\Users\spare\source\repos\ga\ReactComponents\ga-react-components\src\components\EcosystemRoadmap\textureUtils.ts

import * as THREE from 'three';

const textureCache = new Map<string, THREE.CanvasTexture>();

export function createTextTexture(
  text: string,
  options: {
    fontSize?: number;
    color?: string;
    bgColor?: string;
    maxWidth?: number;
    subtitle?: string;
    subtitleColor?: string;
  } = {}
): THREE.CanvasTexture {
  const cacheKey = `${text}|${options.fontSize}|${options.color}|${options.subtitle}`;
  if (textureCache.has(cacheKey)) return textureCache.get(cacheKey)!;

  const {
    fontSize = 32,
    color = '#c9d1d9',
    bgColor = 'transparent',
    maxWidth = 512,
    subtitle,
    subtitleColor = '#8b949e',
  } = options;

  const dpr = Math.min(window.devicePixelRatio, 2);
  const canvas = document.createElement('canvas');
  const ctx = canvas.getContext('2d')!;

  // Measure text
  ctx.font = `bold ${fontSize}px -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif`;
  const metrics = ctx.measureText(text);
  const textWidth = Math.min(metrics.width + 24, maxWidth);
  const height = subtitle ? fontSize * 2.5 : fontSize * 1.8;

  canvas.width = textWidth * dpr;
  canvas.height = height * dpr;
  ctx.scale(dpr, dpr);

  // Background
  if (bgColor !== 'transparent') {
    ctx.fillStyle = bgColor;
    ctx.roundRect(0, 0, textWidth, height, 6);
    ctx.fill();
  }

  // Main text
  ctx.font = `bold ${fontSize}px -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif`;
  ctx.fillStyle = color;
  ctx.textAlign = 'center';
  ctx.textBaseline = 'middle';
  ctx.fillText(text, textWidth / 2, subtitle ? height * 0.35 : height / 2, textWidth - 16);

  // Subtitle
  if (subtitle) {
    ctx.font = `${fontSize * 0.6}px -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif`;
    ctx.fillStyle = subtitleColor;
    ctx.fillText(subtitle, textWidth / 2, height * 0.7, textWidth - 16);
  }

  const texture = new THREE.CanvasTexture(canvas);
  texture.minFilter = THREE.LinearFilter;
  texture.magFilter = THREE.LinearFilter;
  textureCache.set(cacheKey, texture);
  return texture;
}

export function clearTextureCache(): void {
  textureCache.forEach(t => t.dispose());
  textureCache.clear();
}
```

- [ ] **Step 2: Install jotai in ga-react-components**

```bash
cd /c/Users/spare/source/repos/ga/ReactComponents/ga-react-components
npm install jotai
```

- [ ] **Step 3: Create atoms.ts**

```typescript
// C:\Users\spare\source\repos\ga\ReactComponents\ga-react-components\src\components\EcosystemRoadmap\atoms.ts

import { atom } from 'jotai';
import type { RoadmapNode, ViewMode, RendererType } from './types';

export const selectedNodeAtom = atom<RoadmapNode | null>(null);
export const viewModeAtom = atom<ViewMode>('disk');
export const zoomLevelAtom = atom<number>(1.0);
export const expandedTreeNodesAtom = atom<string[]>([]); // string[] for MUI TreeView compat
export const searchFilterAtom = atom<string>('');
export const rendererTypeAtom = atom<RendererType>('webgpu');
export const panelWidthAtom = atom<number>(280);
```

- [ ] **Step 4: Commit**

```bash
cd /c/Users/spare/source/repos/ga
git add ReactComponents/ga-react-components/src/components/EcosystemRoadmap/textureUtils.ts ReactComponents/ga-react-components/src/components/EcosystemRoadmap/atoms.ts
git commit -m "feat: Text texture cache and Jotai atoms for EcosystemRoadmap"
```

---

### Task 4: Navigation Panel

**Files:**
- Create: `ga-react-components/src/components/EcosystemRoadmap/NavigationPanel.tsx`

- [ ] **Step 1: Install @mui/x-tree-view**

```bash
cd /c/Users/spare/source/repos/ga/ReactComponents/ga-react-components
npm install @mui/x-tree-view
```

- [ ] **Step 2: Implement NavigationPanel**

```typescript
// C:\Users\spare\source\repos\ga\ReactComponents\ga-react-components\src\components\EcosystemRoadmap\NavigationPanel.tsx

import React, { useMemo } from 'react';
import { SimpleTreeView, TreeItem } from '@mui/x-tree-view';
import { TextField, InputAdornment, Box, Typography } from '@mui/material';
import SearchIcon from '@mui/icons-material/Search';
import { useAtom, useAtomValue, useSetAtom } from 'jotai';
import { selectedNodeAtom, expandedTreeNodesAtom, searchFilterAtom, panelWidthAtom } from './atoms';
import { roadmapTree, searchTree } from './roadmapData';
import { DOMAIN_COLORS } from './types';
import type { RoadmapNode } from './types';

interface NavigationPanelProps {
  onNodeSelect?: (node: RoadmapNode) => void;
}

export const NavigationPanel: React.FC<NavigationPanelProps> = ({ onNodeSelect }) => {
  const [expanded, setExpanded] = useAtom(expandedTreeNodesAtom);
  const setSelectedNode = useSetAtom(selectedNodeAtom);
  const [filter, setFilter] = useAtom(searchFilterAtom);
  const width = useAtomValue(panelWidthAtom);

  const visibleIds = useMemo(
    () => (filter ? searchTree(roadmapTree, filter) : null),
    [filter]
  );

  const handleSelect = (_event: React.SyntheticEvent, itemId: string) => {
    // Find node by ID in tree, set atom, fire callback
    const node = findNodeById(roadmapTree, itemId);
    if (node) {
      setSelectedNode(node);
      onNodeSelect?.(node);
    }
  };

  const renderTree = (node: RoadmapNode): React.ReactNode => {
    if (visibleIds && !visibleIds.has(node.id)) return null;
    return (
      <TreeItem
        key={node.id}
        itemId={node.id}
        label={
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 0.5, py: 0.25 }}>
            <Box sx={{
              width: 8, height: 8, borderRadius: '50%',
              bgcolor: node.color, flexShrink: 0,
            }} />
            <Typography variant="body2" noWrap>{node.name}</Typography>
            {node.sub && (
              <Typography variant="caption" sx={{ color: '#8b949e', ml: 0.5 }}>
                {node.sub}
              </Typography>
            )}
          </Box>
        }
      >
        {node.children?.map(renderTree)}
      </TreeItem>
    );
  };

  return (
    <Box sx={{ width, minWidth: 200, maxWidth: 500, overflow: 'auto', bgcolor: '#161b22',
               borderRight: '1px solid #30363d', height: '100%' }}>
      <Box sx={{ p: 1 }}>
        <TextField
          fullWidth size="small" placeholder="Search..."
          value={filter} onChange={(e) => setFilter(e.target.value)}
          InputProps={{
            startAdornment: <InputAdornment position="start"><SearchIcon fontSize="small" /></InputAdornment>,
          }}
          sx={{ '& .MuiOutlinedInput-root': { bgcolor: '#0d1117' } }}
        />
      </Box>
      <SimpleTreeView
        expandedItems={expanded}
        onExpandedItemsChange={(_e, ids) => setExpanded(ids)}
        onSelectedItemsChange={handleSelect}
      >
        {renderTree(roadmapTree)}
      </SimpleTreeView>
    </Box>
  );
};

function findNodeById(node: RoadmapNode, id: string): RoadmapNode | null {
  if (node.id === id) return node;
  for (const child of node.children ?? []) {
    const found = findNodeById(child, id);
    if (found) return found;
  }
  return null;
}
```

- [ ] **Step 2: Commit**

```bash
cd /c/Users/spare/source/repos/ga
git add ReactComponents/ga-react-components/src/components/EcosystemRoadmap/NavigationPanel.tsx
git commit -m "feat: NavigationPanel with searchable MUI TreeView"
```

---

### Task 5: Detail Panel and Stats Bar

**Files:**
- Create: `ga-react-components/src/components/EcosystemRoadmap/DetailPanel.tsx`
- Create: `ga-react-components/src/components/EcosystemRoadmap/StatsBar.tsx`

- [ ] **Step 1: Implement DetailPanel**

Reads `selectedNodeAtom`. When a node is selected, shows:
- Name + subtitle as Typography h6
- Domain as color-coded MUI Chip
- Description as body2 text
- Grammar link (if `grammarUrl`) as clickable link with ↗ icon
- GitHub link (if `url`) as clickable link
- Children list with status dots and click-to-navigate
- Uses `getAncestors()` for breadcrumb at top

When no node selected: show a placeholder "Select a node to view details"

- [ ] **Step 2: Implement StatsBar**

Row of MUI Chips, each wrapping an `<a>` tag. Data from `STATS` array in roadmapData.ts.
Chips use `onClick` to open URL in new tab. Styled with `variant="outlined"` and the blue accent color `#58a6ff`.

- [ ] **Step 3: Commit**

```bash
cd /c/Users/spare/source/repos/ga
git add ReactComponents/ga-react-components/src/components/EcosystemRoadmap/DetailPanel.tsx ReactComponents/ga-react-components/src/components/EcosystemRoadmap/StatsBar.tsx
git commit -m "feat: DetailPanel and clickable StatsBar for EcosystemRoadmap"
```

---

### Task 6: Toolbar

**Files:**
- Create: `ga-react-components/src/components/EcosystemRoadmap/Toolbar.tsx`

- [ ] **Step 1: Implement Toolbar**

Horizontal bar containing:
- MUI ToggleButtonGroup for ViewMode (`icicle` | `disk` | `ball`) with icons
- RendererType chip showing "WebGPU ✓" (green) or "WebGL" (yellow) — read-only indicator
- Zoom controls: IconButton (-), Typography showing zoom %, IconButton (+)
- Zoom range: 0.25x to 4.0x, step 0.25

Reads/writes: `viewModeAtom`, `zoomLevelAtom`, `rendererTypeAtom`

- [ ] **Step 2: Commit**

```bash
cd /c/Users/spare/source/repos/ga
git add ReactComponents/ga-react-components/src/components/EcosystemRoadmap/Toolbar.tsx
git commit -m "feat: Toolbar with view toggle, renderer chip, zoom controls"
```

---

### Task 7: Icicle View (Three.js Scene Builder)

> **Shared interface for all views (Tasks 7-9):** Each view module exports a factory function returning this interface. Add this to `types.ts`:
>
> ```typescript
> export interface ViewCallbacks {
>   onNodeClick: (node: RoadmapNode) => void;
>   onNodeHover: (node: RoadmapNode | null) => void;
> }
>
> export interface RoadmapView {
>   update: (selected: RoadmapNode | null, zoom: number) => void;
>   handleClick: (raycaster: THREE.Raycaster) => void;
>   handleHover: (raycaster: THREE.Raycaster) => void;
>   dispose: () => void;
> }
>
> // LOD thresholds (shared across views)
> export const LOD_THRESHOLDS = {
>   LABELS_DEPTH_01: 0.5,   // zoom < 0.5: show depth 0-1 only
>   LABELS_DEPTH_02: 1.5,   // zoom < 1.5: show depth 0-2
>   // zoom >= 1.5: show all labels
> } as const;
> ```

**Files:**
- Create: `ga-react-components/src/components/EcosystemRoadmap/IcicleView.ts`

- [ ] **Step 1: Implement IcicleView**

Non-React module that builds/updates a Three.js scene for the rectangular icicle.

```typescript
// Interface
export interface ViewCallbacks {
  onNodeClick: (node: RoadmapNode) => void;
  onNodeHover: (node: RoadmapNode | null) => void;
}

export function createIcicleView(
  scene: THREE.Scene,
  camera: THREE.OrthographicCamera,
  root: RoadmapNode,
  callbacks: ViewCallbacks
): {
  update: (selected: RoadmapNode | null, zoom: number) => void;
  handleClick: (raycaster: THREE.Raycaster) => void;
  handleHover: (raycaster: THREE.Raycaster) => void;
  dispose: () => void;
};
```

Implementation:
- Uses `d3.hierarchy()` + `d3.partition()` to compute tile positions
- Creates `THREE.Group` with one `THREE.Mesh` (PlaneGeometry) per node
- Each mesh has `userData.node` reference for raycaster hit detection
- Material: `MeshBasicMaterial` with domain color, opacity by depth (1.0 → 0.6)
- Text: `createTextTexture()` applied as second mesh (sprite) centered on each tile
- Camera: OrthographicCamera, no controls. Zoom via frustum adjustment.
- Click a tile: animate camera frustum to fill that tile's subtree (tween via lerp in update loop)
- LOD: hide text sprites below threshold based on zoom level

- [ ] **Step 2: Commit**

```bash
cd /c/Users/spare/source/repos/ga
git add ReactComponents/ga-react-components/src/components/EcosystemRoadmap/IcicleView.ts
git commit -m "feat: IcicleView — rectangular zoomable icicle via d3.partition + Three.js"
```

---

### Task 8: Poincaré Disk View

**Files:**
- Create: `ga-react-components/src/components/EcosystemRoadmap/PoincareDiskView.ts`

- [ ] **Step 1: Implement PoincareDiskView**

Same interface as IcicleView but renders the 2D Poincaré disk:

- Port the existing sphere background (latitude/longitude lines) from current roadmap
- Renders as Three.js scene on XY plane with PerspectiveCamera looking down -Z
- No OrbitControls — pan only (drag to pan, wheel to zoom)
- Nodes positioned via `depthToRadius()` + angular distribution
- Node meshes: small circles (CircleGeometry) with domain color + glow
- Edges: thin lines from parent to child
- Click node: animated Möbius re-centering via `mobiusTransform2D()`
- Boundary circle: `RingGeometry` at r=1.0 with subtle stroke

- [ ] **Step 2: Commit**

```bash
cd /c/Users/spare/source/repos/ga
git add ReactComponents/ga-react-components/src/components/EcosystemRoadmap/PoincareDiskView.ts
git commit -m "feat: PoincareDiskView — 2D hyperbolic layout with Möbius re-centering"
```

---

### Task 9: Poincaré Ball View

**Files:**
- Create: `ga-react-components/src/components/EcosystemRoadmap/PoincareBallView.ts`

- [ ] **Step 1: Implement PoincareBallView**

3D version:
- PerspectiveCamera with OrbitControls (from `three/examples/jsm/controls/OrbitControls.js`)
- Translucent sphere shell: `SphereGeometry` with `MeshPhysicalMaterial` (transmission, roughness)
- Wireframe overlay: second sphere with wireframe material for grid lines
- Nodes positioned via `depthToRadius3D()` + `fibonacciSphere()` for child distribution
- Node meshes: small `SphereGeometry` or billboard `PlaneGeometry` with sprite material
- Edges: `BufferGeometry` lines from parent to child positions
- Click node: animated gyration re-centering via `gyrationTransform3D()`
- All node positions tween smoothly on re-center (~60 frames)
- Text: billboard sprites (always face camera) with LOD visibility

- [ ] **Step 2: Commit**

```bash
cd /c/Users/spare/source/repos/ga
git add ReactComponents/ga-react-components/src/components/EcosystemRoadmap/PoincareBallView.ts
git commit -m "feat: PoincareBallView — 3D hyperbolic layout with gyration transforms"
```

---

### Task 10: Visualization Canvas (Three.js Wrapper)

**Files:**
- Create: `ga-react-components/src/components/EcosystemRoadmap/VisualizationCanvas.tsx`

- [ ] **Step 1: Implement VisualizationCanvas**

React component wrapping the Three.js renderer:

```typescript
interface VisualizationCanvasProps {
  onNodeClick: (node: RoadmapNode) => void;
  onNodeHover: (node: RoadmapNode | null) => void;
}
```

Implementation:
- `useRef<HTMLCanvasElement>` for the canvas element
- `useEffect` for renderer initialization:
  1. Try `new THREE.WebGPURenderer({ canvas })` + `await renderer.init()`
  2. Fallback to `new THREE.WebGLRenderer({ canvas })`
  3. Set `rendererTypeAtom` accordingly
- `useEffect` for view switching based on `viewModeAtom`:
  - Dispose old view, create new one (createIcicleView / createPoincareDiskView / createPoincareBallView)
  - 300ms crossfade: set scene opacity to 0, swap, fade to 1
- `useEffect` for resize: `ResizeObserver` on canvas container → `renderer.setSize()`
- Animation loop: `renderer.setAnimationLoop(callback)` calling `view.update()`
- Raycaster: `pointermove` → `view.handleHover()`, `click` → `view.handleClick()`
- Mouse wheel: update `zoomLevelAtom`, clamp [0.25, 4.0]
- Canvas element: `role="img"` and `aria-label="Ecosystem roadmap visualization"`
- Cleanup on unmount: dispose renderer, textures, geometries
- Wrap in ErrorBoundary (class component):

```typescript
class VizErrorBoundary extends React.Component<
  { children: React.ReactNode },
  { error: Error | null }
> {
  state = { error: null as Error | null };
  static getDerivedStateFromError(error: Error) { return { error }; }
  render() {
    if (this.state.error) {
      return (
        <Box sx={{ p: 4, textAlign: 'center', color: '#8b949e' }}>
          <Typography>Visualization failed to load.</Typography>
          <Typography variant="caption">{this.state.error.message}</Typography>
        </Box>
      );
    }
    return this.props.children;
  }
}
```

- [ ] **Step 2: Commit**

```bash
cd /c/Users/spare/source/repos/ga
git add ReactComponents/ga-react-components/src/components/EcosystemRoadmap/VisualizationCanvas.tsx
git commit -m "feat: VisualizationCanvas — WebGPU/WebGL renderer with view switching"
```

---

### Task 11: Main Component — EcosystemRoadmapExplorer

**Files:**
- Create: `ga-react-components/src/components/EcosystemRoadmap/EcosystemRoadmapExplorer.tsx`
- Create: `ga-react-components/src/components/EcosystemRoadmap/index.ts`

- [ ] **Step 1: Implement EcosystemRoadmapExplorer**

Master-detail layout using MUI Box with flexbox:

```
<Box display="flex" height="100vh">
  <NavigationPanel />                    {/* width from panelWidthAtom */}
  <Box /* drag divider 4px */ />
  <Box flex={1} display="flex" flexDirection="column">
    <Toolbar />
    <VisualizationCanvas flex={1} />
    <DetailPanel />                      {/* collapsible, ~200px */}
    <StatsBar />
  </Box>
</Box>
```

- Drag divider between panels: `onMouseDown` starts tracking, `onMouseMove` updates `panelWidthAtom`, `onMouseUp` stops. Cursor changes to `col-resize`.
- Bidirectional sync: when `selectedNodeAtom` changes (from tree click), pass to viz. When viz click fires `onNodeClick`, set atom (tree auto-updates).
- Background: `#0d1117` (GitHub dark)

- [ ] **Step 2: Create barrel export index.ts**

```typescript
// Named exports (matching codebase convention — no default exports)
export { EcosystemRoadmapExplorer } from './EcosystemRoadmapExplorer';
export type { RoadmapNode, ViewMode, Domain } from './types';
```

Note: `EcosystemRoadmapExplorer.tsx` must use `export const EcosystemRoadmapExplorer` (named), not `export default`.

- [ ] **Step 3: Commit**

```bash
cd /c/Users/spare/source/repos/ga
git add ReactComponents/ga-react-components/src/components/EcosystemRoadmap/EcosystemRoadmapExplorer.tsx ReactComponents/ga-react-components/src/components/EcosystemRoadmap/index.ts
git commit -m "feat: EcosystemRoadmapExplorer master-detail layout with drag divider"
```

---

### Task 12: Test Page in ga-react-components

**Files:**
- Create: `ga-react-components/src/pages/EcosystemRoadmapTest.tsx`
- Modify: `ga-react-components/src/main.tsx` — add route
- Modify: `ga-react-components/src/pages/TestIndex.tsx` — add entry

- [ ] **Step 1: Create test page**

```typescript
// C:\Users\spare\source\repos\ga\ReactComponents\ga-react-components\src\pages\EcosystemRoadmapTest.tsx

import React from 'react';
import { Container } from '@mui/material';
import { EcosystemRoadmapExplorer } from '../components/EcosystemRoadmap';

const EcosystemRoadmapTest: React.FC = () => {
  return (
    <Container maxWidth={false} disableGutters sx={{ height: '100vh', overflow: 'hidden' }}>
      <EcosystemRoadmapExplorer />
    </Container>
  );
};

export default EcosystemRoadmapTest;
```

- [ ] **Step 2: Add route in main.tsx**

Add import and route following existing pattern:
```typescript
import EcosystemRoadmapTest from './pages/EcosystemRoadmapTest';
// Inside <Routes>:
<Route path="/test/ecosystem-roadmap" element={<App><EcosystemRoadmapTest /></App>} />
```

- [ ] **Step 3: Add entry in TestIndex.tsx**

Add to `testPages` array:
```typescript
{
  id: 'ecosystem-roadmap',
  title: 'Ecosystem Roadmap Explorer',
  description: 'Three-mode roadmap: icicle, Poincaré disk, Poincaré ball (WebGPU)',
  technology: 'Three.js WebGPU, D3, MUI TreeView, Jotai',
  path: '/test/ecosystem-roadmap',
  features: ['WebGPU rendering', 'Hyperbolic geometry', 'Master-detail layout', 'Bidirectional sync'],
  status: 'complete',
}
```

- [ ] **Step 4: Verify it runs**

```bash
cd /c/Users/spare/source/repos/ga/ReactComponents/ga-react-components
npm run dev
# Open http://localhost:5176/test/ecosystem-roadmap
```

- [ ] **Step 5: Commit**

```bash
cd /c/Users/spare/source/repos/ga
git add ReactComponents/ga-react-components/src/pages/EcosystemRoadmapTest.tsx ReactComponents/ga-react-components/src/main.tsx ReactComponents/ga-react-components/src/pages/TestIndex.tsx
git commit -m "feat: EcosystemRoadmap test page with route and index entry"
```

---

### Task 13: Demo Page in ga-client

**Files:**
- Create: `ga-client/src/pages/demos/EcosystemRoadmapDemo.tsx`
- Modify: `ga-client/src/App.tsx` — add route
- Modify: `ga-client/src/pages/DemosIndex.tsx` — add card

- [ ] **Step 1: Create demo page**

```typescript
// C:\Users\spare\source\repos\ga\Apps\ga-client\src\pages\demos\EcosystemRoadmapDemo.tsx

import { Container } from '@mui/material';
import { EcosystemRoadmapExplorer } from 'ga-react-components/src/components/EcosystemRoadmap';

const EcosystemRoadmapDemo = () => {
  return (
    <Container maxWidth={false} disableGutters sx={{ height: 'calc(100vh - 64px)', overflow: 'hidden' }}>
      <EcosystemRoadmapExplorer />
    </Container>
  );
};

export default EcosystemRoadmapDemo;
```

- [ ] **Step 2: Add route in App.tsx**

```typescript
import EcosystemRoadmapDemo from './pages/demos/EcosystemRoadmapDemo';
// In <Routes>:
<Route path="/demos/ecosystem-roadmap" element={<EcosystemRoadmapDemo />} />
```

- [ ] **Step 3: Add card in DemosIndex.tsx**

Add icon import `AccountTree as AccountTreeIcon` and card entry:
```typescript
{
  title: 'Ecosystem Roadmap',
  description: 'Interactive roadmap with icicle, Poincaré disk, and 3D Poincaré ball views. WebGPU-accelerated.',
  icon: <AccountTreeIcon sx={{ fontSize: 48 }} />,
  link: '/demos/ecosystem-roadmap',
  tags: ['Three.js', 'WebGPU', 'Hyperbolic', 'D3'],
  status: 'Available',
  color: '#f0883e',
}
```

- [ ] **Step 4: Verify it runs**

```bash
cd /c/Users/spare/source/repos/ga/Apps/ga-client
npm run dev
# Open http://localhost:5173/demos/ecosystem-roadmap
```

- [ ] **Step 5: Commit**

```bash
cd /c/Users/spare/source/repos/ga
git add Apps/ga-client/src/pages/demos/EcosystemRoadmapDemo.tsx Apps/ga-client/src/App.tsx Apps/ga-client/src/pages/DemosIndex.tsx
git commit -m "feat: EcosystemRoadmap demo page in ga-client with route and card"
```

---

### Task 14: Integration Testing and Polish

**Files:**
- All EcosystemRoadmap files (bug fixes, polish)

- [ ] **Step 1: Test all three view modes**

Open `http://localhost:5176/test/ecosystem-roadmap` and verify:
1. Disk view loads by default — nodes positioned in Poincaré disk
2. Toggle to Icicle — rectangular partition layout appears
3. Toggle to Ball — 3D sphere with orbiting
4. WebGPU/WebGL chip shows correct renderer

- [ ] **Step 2: Test bidirectional sync**

1. Click a node in the tree → viz highlights and animates to it
2. Click a node in the viz → tree expands and highlights it
3. Detail panel updates with correct metadata and links

- [ ] **Step 3: Test zoom and interaction**

1. Mouse wheel zooms in/out — zoom indicator updates
2. Zoom controls (± buttons) work
3. Click stats chips → open correct GitHub URLs in new tab
4. Search filter → tree filters correctly
5. Drag divider → panel resizes, canvas re-renders

- [ ] **Step 4: Fix any issues found, commit specific files**

```bash
cd /c/Users/spare/source/repos/ga
git add ReactComponents/ga-react-components/src/components/EcosystemRoadmap/
git commit -m "fix: Polish EcosystemRoadmap — integration fixes"
```

---

## Summary

| Task | Component | Est. Complexity |
|------|-----------|----------------|
| 1 | Types + Data Model | Low |
| 2 | Hyperbolic Math | Medium |
| 3 | Textures + Atoms | Low |
| 4 | Navigation Panel | Medium |
| 5 | Detail Panel + Stats | Low |
| 6 | Toolbar | Low |
| 7 | Icicle View | High |
| 8 | Poincaré Disk View | High |
| 9 | Poincaré Ball View | High |
| 10 | Visualization Canvas | High |
| 11 | Main Component | Medium |
| 12 | Test Page (components) | Low |
| 13 | Demo Page (client) | Low |
| 14 | Integration + Polish | Medium |

**Critical path:** Tasks 1-3 (foundation) → Tasks 7-9 (views, parallelizable) → Task 10 (canvas) → Task 11 (assembly) → Tasks 12-14 (wiring)
