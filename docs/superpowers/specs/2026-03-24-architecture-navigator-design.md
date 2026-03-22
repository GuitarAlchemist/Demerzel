# Architecture Navigator — Design Specification

**Date:** 2026-03-24
**Status:** Draft
**Scope:** ga-react-components (component) + ga-client (route `/architecture`)
**Consolidates:** #159 (Interactive Architecture Navigator), #143 (Universal Governance Browser), #155 (Multi-roadmap management)

## Overview

A single React component that provides a navigable, auto-generated view of every artifact in the GuitarAlchemist ecosystem — from the 30,000ft ecosystem view down to a single policy threshold or grammar production rule. It is simultaneously the architecture documentation, the governance browser, and the multi-stream roadmap manager.

The three original issues converge on one insight: the Architecture Navigator IS the Governance Browser WITH multi-roadmap stream support. No reason to build three separate UIs.

## Goals

1. **Single entry point** — one route (`/architecture`) covers every artifact type
2. **Auto-generated** — data extracted from actual files (YAML, EBNF, JSON, `.ixql`, MD); no manual curation
3. **Multiple view modes** — icicle hierarchy, force graph, timeline/streams
4. **Artifact renderers** — each artifact type has a dedicated renderer (gauges, syntax tree, DAG, etc.)
5. **Roadmap streams** — four parallel streams with junction points visualized
6. **Full-text search** — across all artifact types simultaneously

## Non-Goals

- Real-time GitHub API polling (data is built at deploy time via MetaSync pipeline)
- Mobile-first design (desktop-primary, responsive as bonus)
- Replacing existing Poincaré Ball demo (separate component — link from here)
- Editor / write-back capability (read-only browser in v1)

## Architecture

### Component Hierarchy

```
ArchitectureNavigator (page, route /architecture)
├── NavSidebar (left, resizable)
│   ├── SearchBox (full-text, all artifact types)
│   ├── ArtifactTypeFilter (chips: Policy | Grammar | Persona | MCP | IxQL | Schema | Test | Roadmap)
│   └── HierarchyTree (MUI SimpleTreeView, lazy-expanded)
│       └── TreeNode (icon + domain color dot + status indicator)
├── MainPanel (right, flex-grow)
│   ├── ViewToolbar
│   │   ├── ViewToggle (Icicle | Graph | Timeline | Streams)
│   │   └── BreadcrumbTrail
│   ├── VisualizationArea
│   │   ├── IcicleView         (D3 partition, WebGPU/WebGL canvas)
│   │   ├── GraphView          (D3 force-directed, relationships)
│   │   ├── TimelineView       (horizontal evolution, D3 timeline)
│   │   └── StreamsView        (parallel roadmap streams + junctions)
│   └── DetailPanel
│       ├── ArtifactHeader     (name, type, version, status, GitHub link)
│       ├── ArtifactRenderer   (type-specific — see Artifact Renderers)
│       └── RelationshipsPanel (depends on, consumed by, tested by, governed by)
└── ArtifactDataProvider (React context — data + selection state)
```

### State Management

```typescript
// Jotai atoms
const selectedArtifactAtom = atom<Artifact | null>(null);
const viewModeAtom = atom<'icicle' | 'graph' | 'timeline' | 'streams'>('icicle');
const searchQueryAtom = atom<string>('');
const activeFiltersAtom = atom<Set<ArtifactType>>(new Set());
const expandedNodesAtom = atom<Set<string>>(new Set());
const highlightedStreamAtom = atom<StreamId | null>(null);
```

### Core Data Model

```typescript
type ArtifactType =
  | 'policy' | 'grammar' | 'persona' | 'mcp-tool' | 'ixql-pipeline'
  | 'schema' | 'behavioral-test' | 'constitution' | 'department'
  | 'course' | 'contract' | 'state-snapshot';

interface Artifact {
  id: string;               // kebab-case, globally unique
  type: ArtifactType;
  name: string;
  version?: string;
  description: string;
  status: 'active' | 'draft' | 'horizon' | 'deprecated';
  domain: 'governance' | 'music' | 'science' | 'humanities' | 'infrastructure' | 'meta';
  sourceFile: string;       // relative path in repo
  githubUrl: string;
  lastModified: string;     // ISO-8601
  relations: ArtifactRelation[];
  children?: Artifact[];    // for hierarchical views
  rawContent?: string;      // for renderers that need source text
}

interface ArtifactRelation {
  type: 'governs' | 'governed-by' | 'tests' | 'tested-by' | 'implements'
      | 'consumes' | 'produces' | 'references' | 'extends';
  targetId: string;
  targetType: ArtifactType;
}
```

## View Modes

### 1. Icicle (Default)

Rectangular zoomable hierarchy showing the full artifact tree.

- Layout: `d3.partition()` — (x0,y0,x1,y1) in [0,1] range
- Rendering: Three.js `PlaneGeometry` tiles on an `OrthographicCamera`; WebGPU primary, WebGL fallback
- Root: GuitarAlchemist ecosystem → repos → artifact categories → individual artifacts
- Zoom: click tile → camera animates to fill that subtree; breadcrumb to navigate back
- Color: domain-coded (governance=blue, music=amber, science=teal, humanities=purple, infra=grey, meta=green)
- Labels: Canvas2D texture per tile; LOD — show labels only when tile > 40px wide
- Same camera/rendering approach as `2026-03-24-ecosystem-roadmap-explorer-design.md`

### 2. Graph (Relationships)

Force-directed graph showing cross-artifact dependencies.

- Rendering: D3 force simulation on SVG (not Three.js — relationship graphs benefit from SVG scalability)
- Nodes: circles, icon + color-coded by type and domain
- Edges: directed arrows colored by relation type; hover shows relation label
- Focus mode: click a node → highlight its 1-hop neighborhood, fade others
- Cluster mode: group by domain or artifact type (toggle in toolbar)
- Useful for: "which policies govern which personas?", "which grammars feed which departments?"

### 3. Timeline (Evolution)

Horizontal timeline of artifact creation and modification.

- X-axis: date; Y-axis: artifact type swim lanes
- Each artifact is a dot/bar; click → select + show in detail panel
- Zoom: wheel to expand/collapse date range
- Filter by type, domain, or date range
- Shows when governance artifacts were introduced relative to features
- Data source: `git log --follow --format="%H %ai %s" -- <file>` embedded at build time

### 4. Streams (Multi-Roadmap)

Four parallel roadmap streams with junction points — consolidated from #155.

```
IxQL Stream        ──●────────────●──────────────────●──────────────●──→
                            ↗ junction: Gov Browser  ↗ junction: tars CE
Governance Stream  ──●──────────●──────────────────●────────────────●──→

GA Chatbot Stream  ──●──────────────────────────────●──────────────●──→
                                                            ↗ junction: Marketplace
Research Stream    ──●──────●──────────────────────────────●──────────→
```

Each stream node is a GitHub issue with:
- Status (open/closed), assignee, milestone
- Stream color
- Click → GitHub issue link

Junction points are rendered as diamonds; hover shows which streams must converge and what they're blocked on.

IxQL representation (embedded in spec for reference):

```ixql
roadmap.streams
  → identify_junctions(dependency_graph)
  → critical_path(streams, junctions)
  → when junction_blocked: escalate(stream.owners)
  → fan_out(stream.next_tasks)
```

Stream definitions (four streams, extensible):

| Stream | Color | Current Focus |
|--------|-------|---------------|
| IxQL | `#4FC3F7` | Parser, CLI, LSP, tree-sitter |
| Governance | `#81C784` | Policies, auditing, meta-tools, conscience |
| GA Chatbot | `#FFB74D` | Beginner features, chord UI, chatbot |
| Research | `#CE93D8` | Seldon Plan, departments, grammars |

## Artifact Renderers

Each artifact type has a purpose-built renderer shown in the Detail Panel when that artifact is selected. Renderers are lazy-loaded React components.

### Policy YAML → Gauge Dashboard

For `.yaml` files in `policies/`:

- Parse `confidence_thresholds` → horizontal gauge bars (0.0–1.0)
- Parse `anti_patterns[]` → status list with severity chips
- Parse `formulas` → rendered math (KaTeX, already in ga-client)
- Parse `principles[]` → card grid with constitutional article badges
- Constitutional basis: display which Article (1-11 + 0-5) governs this policy

```
alignment.yaml                     [Article 3 · Article 6]
Confidence Thresholds
  Autonomous:  ████████░░  0.9
  With note:   ███████░░░  0.7
  Confirm:     █████░░░░░  0.5
  Escalate:    ███░░░░░░░  0.3
```

### Grammar EBNF → Syntax Tree

For `.ebnf` files in grammars/:

- Parse EBNF using a lightweight parser (hand-rolled, ~100 lines — no tree-sitter dependency in v1)
- Render production rules as a collapsible syntax tree (MUI TreeView)
- Highlight terminals vs. non-terminals with color coding
- Click a non-terminal → expand its production inline
- Show sample derivations for leaf rules

### IxQL Pipeline → DAG

For `.ixql` files:

- Parse pipeline stages separated by `→`
- Render as a left-to-right DAG (D3 dagre layout)
- Each stage node shows the operation name and operands
- `when` clauses rendered as diamond decision nodes
- `fan_out` / `compound` shown as fork/join nodes
- Hover → show full stage text in tooltip

### MCP Tools → Federation Graph

For MCP tool registries (JSON/YAML):

- Group tools by server/repo
- Render as a cluster graph: server bubbles containing tool nodes
- Edge = tool dependency or shared schema
- Filter by capability tag
- Links out to the MCP server definition on GitHub

### Persona → Profile Card

For `.persona.yaml` files:

- Name, version, role, domain
- Capabilities as tag chips
- Constraints as a list with severity indicators
- Voice profile: tone / verbosity / style
- `goal_directedness` badge
- `estimator_pairing` chip linking to the paired persona
- Linked behavioral test (with pass/fail status if available)

### Schema → Property Table

For `.json` (JSON Schema):

- Title, description, `$schema` version
- Required fields highlighted
- Property table: name | type | constraints | description
- Example values (from `examples/` directory if present)

### Behavioral Test → Test Summary

For `.test.md` files:

- Test suite name, artifact under test
- Pass / fail / skip counts with progress bar
- Individual test cases with status dots
- Last run date (from CI badge data if available)

## Auto-Generation Pipeline

All data is extracted from actual files at build time — never manually curated.

### Data Extraction (MetaSync Integration)

A new MetaSync task (`metasync extract-artifacts`) crawls the Demerzel repo and produces `artifacts.json`:

```
Demerzel/
  policies/*.yaml      → ArtifactType.policy
  personas/*.yaml      → ArtifactType.persona
  schemas/*.json       → ArtifactType.schema
  tests/behavioral/*.md → ArtifactType.behavioral-test
  constitutions/*.md   → ArtifactType.constitution
  contracts/*.md       → ArtifactType.contract

ga/ (Guitar Alchemist)
  grammars/*.ebnf      → ArtifactType.grammar
  departments/*.yaml   → ArtifactType.department
  courses/**/*.md      → ArtifactType.course

ix/
  tools/**/*.json      → ArtifactType.mcp-tool
  pipelines/**/*.ixql  → ArtifactType.ixql-pipeline
```

Relations are inferred from:
- YAML `governed_by`, `tests`, `implements` fields
- EBNF `grammar_uses` comments
- IxQL pipeline `import` directives
- Cross-references in Markdown (`#143`, `policies/alignment.yaml`)

### Build-Time Embedding

`artifacts.json` is committed to `ga-client/src/data/artifacts.json` by the MetaSync CI job after each Demerzel push. The navigator imports it statically — no runtime API calls.

New artifacts appear automatically in the next deploy. No manual registration.

## Search

Full-text search across all artifact types simultaneously.

- Input: debounced 300ms, min 2 chars
- Scope: `name`, `description`, `rawContent` (truncated to 500 chars per artifact)
- Matching: fuzzy match via `fuse.js` (already in ga-client workspace)
- Results: grouped by artifact type, sorted by relevance score
- Highlight: matching terms highlighted in result snippets
- Keyboard: `Ctrl+K` / `Cmd+K` to focus search from anywhere on the page

## File Structure

```
ga-react-components/src/components/ArchitectureNavigator/
  ArchitectureNavigator.tsx          # Root component + ArtifactDataProvider
  NavSidebar.tsx                     # Left panel: search + filter + tree
  HierarchyTree.tsx                  # MUI SimpleTreeView wrapper
  ViewToolbar.tsx                    # View toggle + breadcrumb
  IcicleView.ts                      # D3 partition + Three.js rendering
  GraphView.tsx                      # D3 force-directed SVG
  TimelineView.tsx                   # Horizontal swim-lane timeline
  StreamsView.tsx                    # Parallel roadmap streams + junctions
  DetailPanel.tsx                    # Artifact detail + renderer dispatch
  renderers/
    PolicyRenderer.tsx               # YAML → gauge dashboard
    GrammarRenderer.tsx              # EBNF → syntax tree
    IxQLRenderer.tsx                 # Pipeline → DAG
    MCPRenderer.tsx                  # Tools → federation graph
    PersonaRenderer.tsx              # → profile card
    SchemaRenderer.tsx               # → property table
    TestRenderer.tsx                 # → test summary
  hyperbolicMath.ts                  # Shared with EcosystemRoadmap if merged
  types.ts                           # Artifact, ArtifactType, ArtifactRelation
  data/artifactLoader.ts             # Loads + indexes artifacts.json

ga-client/src/pages/demos/
  ArchitectureNavigatorDemo.tsx      # Route wrapper, lazy import
  # + route entry in App.tsx
  # + card in DemosIndex.tsx

ga-client/src/data/
  artifacts.json                     # Auto-generated by MetaSync CI

Demerzel/
  docs/superpowers/specs/
    2026-03-24-architecture-navigator-design.md   # This file
```

## Design Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Three.js vs. SVG | Three.js for icicle/ball; SVG for graph/timeline | Three.js for hierarchical pixel density; SVG scales better for node-link graphs |
| Data fetching | Static JSON embedded at build time | No CORS issues, no latency, works offline, always consistent with deploy |
| Renderer dispatch | `switch (artifact.type)` in DetailPanel | Simple, explicit, easy to add new types |
| EBNF parser | Hand-rolled | tree-sitter is a heavy native dependency; a simple recursive descent handles EBNF adequately for display |
| Fuse.js search | Already in workspace | Avoids new dependency; adequate for ~1000 artifact corpus |
| Streams data source | GitHub Issues API at build time | Issues are the canonical source; extracted once per CI run |
| Merge with EcosystemRoadmap | Keep separate in v1, merge if overlap > 70% | Navigator is broader (all artifacts); Roadmap is focused (Streeling hierarchy) |

## Dependencies

All already in the ga workspace:

- `three` (r180) — icicle rendering
- `d3` (v7.8.5) — partition layout, force simulation, timeline
- `@mui/material` — TreeView, Chips, ToggleButtonGroup
- `jotai` — state atoms
- `fuse.js` — fuzzy search
- `katex` — formula rendering in policy gauges

New (acceptable additions):
- None required in v1

## Testing

- Behavioral spec: `Demerzel/tests/behavioral/architecture-navigator.test.md` (to be created)
- Unit tests: Vitest for `artifactLoader.ts`, relation inference, EBNF parser
- Integration: Playwright — navigate to each view mode, select one artifact of each type, verify renderer renders without error
- Visual regression: screenshot each renderer type; compare on CI

## Accessibility

- MUI TreeView provides keyboard navigation (Tab, Arrow keys, Enter) with ARIA
- Three.js canvas: `role="img"` + `aria-label` describing current view + selected node
- Tree + detail panel = fully accessible alternative to canvas views
- All GitHub links are standard `<a>` elements with descriptive `aria-label`
- Search result list has `role="listbox"` with `aria-activedescendant`

## Rollout

1. `artifacts.json` schema + MetaSync extraction task (prerequisite)
2. `types.ts` + `artifactLoader.ts` + search
3. NavSidebar + HierarchyTree (tree-only, no canvas)
4. IcicleView (most useful first)
5. DetailPanel + all Renderers (ship incrementally per renderer type)
6. GraphView
7. StreamsView (requires GitHub Issues data in `artifacts.json`)
8. TimelineView

Each step ships independently and is usable on its own.

## References

- [2026-03-24-ecosystem-roadmap-explorer-design.md](2026-03-24-ecosystem-roadmap-explorer-design.md) — icicle/Poincaré component (reuse rendering patterns)
- [2026-03-24-ixql-lsp-design.md](2026-03-24-ixql-lsp-design.md) — IxQL pipeline structure
- [2026-03-22-session-integrated-cycle-design.md](2026-03-22-session-integrated-cycle-design.md) — MetaSync pipeline integration
- Issue #159 (this spec's primary issue)
- Issue #143 (Universal Governance Browser — consolidated here)
- Issue #155 (Multi-roadmap streams — consolidated here)
- Issue #145 (tree-sitter — future v2 EBNF parser upgrade)
