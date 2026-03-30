# IXQL UI Composition Language — Design Spec

**Status:** Brainstormed (2026-03-29), ready for implementation
**Origin:** Multi-AI brainstorm (Codex GPT-5.4 + Claude Opus 4.6)
**Pattern name:** Isomorphic Governance

## Core Insight

IXQL is already a governance DOM — CREATE NODE is component instantiation, LINK is data flow, BIND HEALTH is reactive binding. Adding UI composition *completes* the isomorphism. The constitution governs not just AI behavior but what panels can be created, what forms can modify, and what visualizations are permitted.

## Architecture: Three-Layer Hybrid

```
Layer 1: IXQL Grammar Extension (parser)
  CREATE PANEL / CREATE VIZ / CREATE FORM
  SOURCE / PROJECT / PUBLISH / SUBSCRIBE
  GOVERNED BY / LAYOUT / SUBMIT

Layer 2: UI Descriptor Compiler (AST -> WidgetSpec)
  Validates clauses, resolves bindings, emits dependency graph

Layer 3: Registry Runtime (React components)
  PanelRegistry (AG-Grid tables)
  VizRegistry (D3.js charts)
  FormRegistry (MUI forms)
  BindingEngine (TanStack Query + SignalR)
  DashboardContextBus (Zustand/Jotai pub/sub)
```

## Grammar Extension

### CREATE PANEL (AG-Grid)
```ixql
CREATE PANEL "belief-states"
  KIND grid
  TEMPLATE governance.belief-grid
  SOURCE governance.beliefs
  PROJECT {
    id,
    truth_value,
    confidence,
    ageDays: DAYS_SINCE(updated_at)
  }
  REFRESH 30s
  LIVE true
  LAYOUT md:6 lg:4
  GOVERNED BY article=7
  PUBLISH selection AS selectedBelief
```

### CREATE VIZ (D3.js)
```ixql
CREATE VIZ "policy-network"
  KIND force-graph
  TEMPLATE governance.risk-network
  SOURCE governance.relationships
  SUBSCRIBE selectedBelief
  ON UNKNOWN show="investigation-prompt"
  ON CONTRADICTORY show="conflict-resolution" ESCALATE
  LAYOUT md:6 lg:8
```

### CREATE FORM (Material UI)
```ixql
CREATE FORM "belief-update"
  KIND mui-form
  TEMPLATE governance.belief-editor
  FIELDS [
    truth_value: enum("TRUE","FALSE","UNKNOWN","CONTRADICTORY"),
    confidence: slider(0.0, 1.0),
    justification: text(required=true)
  ]
  CONSTRAIN confidence TO [0.0, 1.0]
  REQUIRE justification WHEN delta > 0.2
  TETRAVALENT validation=true
  SUBMIT COMMAND governance.updateBelief
  ON_SUCCESS REFRESH "belief-states", "policy-network"
  GOVERNED BY article=3
```

### Composable Signal Graph
```ixql
-- Linked dashboard: click a node -> table filters -> form pre-fills
CREATE VIZ OrgGraph
  KIND force-graph
  SOURCE governance.relationships
  PUBLISH selection AS selectedNode

CREATE PANEL NodeDetails
  KIND grid
  SOURCE governance.nodeDetails(selectedNode)
  SUBSCRIBE selectedNode

CREATE FORM AssignOwner
  KIND mui-form
  SUBSCRIBE selectedNode
  SUBMIT COMMAND governance.assignOwner
  ON_SUCCESS REFRESH NodeDetails, OrgGraph
```

### Agentic Dashboards (Panels as governance participants)
```ixql
ON VIOLATION IN "compliance-dashboard"
  CREATE NODE type="escalation" severity="high"
  LINK TO source-artifact
  NOTIFY VIA algedonic-channel
```

### Saved Queries as Governance Artifacts
```ixql
SAVE QUERY "daily-compliance-view" AS artifact
  VERSION "1.0.0"
  RATIONALE "Standard compliance dashboard per Article 7"
  REVIEWABLE BY "skeptical-auditor"
```

## Key Differentiators vs Grafana/Retool/Streamlit

| Feature | Grafana/Retool | IXQL |
|---------|---------------|------|
| Governance | External auth layer | `GOVERNED BY article=N` in grammar |
| Data states | Boolean (loaded/empty) | Tetravalent (T/F/U/C) |
| Panels | Passive displays | Agentic — issue commands on violations |
| Validation | Manual per-form | Constitution-derived constraints |
| Queries | Ephemeral | Versioned governance artifacts |
| Layout priority | UX preference | Constitutional hierarchy |

## Tetravalent Rendering

| Standard UI | Tetravalent UI |
|---|---|
| visible / hidden | visible / hidden / data-uncertain / data-contradictory |
| valid / invalid | valid / invalid / insufficient-evidence / conflicting-inputs |
| loaded / empty | loaded / empty / stale-unknown / multi-source-conflict |

```ixql
CREATE VIZ "belief-trend"
  ON UNKNOWN show="investigation-prompt"
  ON CONTRADICTORY show="conflict-resolution" ESCALATE
```

## Named Concepts

- **Isomorphic Governance** — rules, data, queries, and UI are all expressions of the same constitutional structure
- **Constitutional DOM (GovDOM)** — IXQL as a governance document object model
- **Tetravalent Rendering** — UI states beyond boolean, matching T/F/U/C logic
- **Agentic Dashboards** — panels that act on governance violations, not just display them
- **Visual Service Mesh** — PanelRegistry as service mesh (interfaces, health, routing, discovery)

## WidgetSpec Type (compiler output)

```typescript
type WidgetSpec = PanelSpec | VizSpec | FormSpec;

interface PanelSpec {
  id: string;
  kind: 'grid';
  template?: string;
  source: DataBindingSpec;
  project?: ProjectionSpec;
  layout: ResponsiveLayoutSpec;
  governedBy?: number[];    // article numbers
  publish?: { signal: string; as: string };
  subscribe?: string[];
  refresh?: number;         // ms
  live?: boolean;           // SignalR upgrade
}

interface DataBindingSpec {
  provider: string;         // registered query provider
  params?: Record<string, unknown>;
  dependsOn?: string[];     // signal names from other widgets
}

interface ResponsiveLayoutSpec {
  xs?: LayoutSlot;
  sm?: LayoutSlot;
  md?: LayoutSlot;
  lg?: LayoutSlot;
  xl?: LayoutSlot;
}

interface LayoutSlot {
  col: number;
  row?: number;
  h?: number;
}
```

## Registry Entry Schema

```typescript
interface RegistryEntry {
  kind: 'grid' | 'force-graph' | 'timeline' | 'chord' | 'mui-form';
  template: string;
  version: string;
  propSchema: JsonSchema;          // validates IXQL WITH clauses
  dataContract: string;            // expected data shape
  capabilities: string[];          // ['pagination','serverSort','rowSelection','csvExport']
  supports: {
    publish: boolean;
    subscribe: boolean;
    tetravalent: boolean;
    governedBy: boolean;
  };
}
```

## Implementation Plan

### Phase 1: AG-Grid proof-of-concept — IMPLEMENTED (2026-03-29)

**Files created/modified:**
- `IxqlControlParser.ts` — added `CreateGridPanelCommand` type, `parseCreateGridPanel()`, tokenizer extended for `{}:` structural chars
- `IxqlWidgetSpec.ts` — **NEW** — `PanelSpec`, `DataBindingSpec`, `ProjectionSpec`, `CompiledProjectionField`, `ResponsiveLayoutSpec` types + `compileGridPanel()` compiler + `applyProjection()` runtime + whitelisted pure functions (DAYS_SINCE, FORMAT_PERCENT, COALESCE, UPPERCASE)
- `IxqlGridPanel.tsx` — **NEW** — AG-Grid Community wrapper with auto-generated ColDefs, tetravalent cell renderer (T/F/U/C color-coded dots), confidence bar renderer (0.0-1.0), governed-by article badges, PUBLISH row selection, SUBSCRIBE signal reactivity, REFRESH polling
- `DashboardSignalBus.ts` — **NEW** — cross-widget signal bus with throttled publish (50ms debounce), `useSignal()`, `useSignals()`, `usePublish()` hooks
- `PanelRegistry.ts` — added 'grid' icon to ICON_CATALOG
- `ForceRadiant.tsx` — wired `create-grid-panel` command dispatch, `gridPanelSpecsRef` storage, `IxqlGridPanel` rendering in panel switch
- `index.ts` — exported all new types and components

**Grammar implemented:**
```ixql
CREATE PANEL "id" KIND grid
  TEMPLATE governance.belief-grid     -- optional
  SOURCE governance.beliefs           -- required
  WHERE confidence > 0.5              -- optional
  PROJECT { id, truth_value, confidence, ageDays: DAYS_SINCE(updated_at) }
  REFRESH 30s
  LIVE true
  LAYOUT md:6 lg:4
  GOVERNED BY article=7
  PUBLISH selection AS selectedBelief
  SUBSCRIBE selectedNode
```

**Deviations from spec:**
- Used DataFetcher polling instead of TanStack Query (consistent with existing DynamicPanel pattern)
- LIVE true parsed but SignalR upgrade deferred (flag stored in PanelSpec, ready for wiring)
- Signal bus uses vanilla store + useSyncExternalStore instead of Zustand (no new dependency)

### Phase 1b: PIPE Transforms — IMPLEMENTED (2026-03-30)

**Files created/modified:**
- `IxqlControlParser.ts` — PipeStep union type (7 step kinds), AggregateSpec, parsePipeStep()
- `IxqlPipeEngine.ts` — **NEW** — executePipeline() with FILTER/SORT/LIMIT/SKIP/DISTINCT/FLATTEN/GROUP BY
- `IxqlWidgetSpec.ts` — PipelineSpec type, pipeline field on PanelSpec
- `IxqlGridPanel.tsx` — pipeline execution between fetch and projection, PIPE badge, hexavalent cell rendering

**Grammar:**
```ixql
CREATE PANEL "summary" KIND grid
  SOURCE governance.beliefs
  PIPE FILTER truth_value = T
  PIPE GROUP BY evaluated_by COUNT SUM(confidence) AVG(confidence)
  PIPE SORT count DESC
  PIPE LIMIT 10
  PROJECT { evaluated_by, count, avg_confidence }
```

**Security fixes from architecture review:**
- Cross-origin URL restriction (same-origin only)
- `~` operator uses indexOf instead of RegExp (no ReDoS)
- PipeStep discriminant unified to `type` (was `kind`)
- useSignals stabilized with timestamp-based change detection
- graphContext passed to resolve() for graph:// sources

### Phase 2: D3 visualizations
1. Add `CREATE VIZ` to parser
2. Create `IxqlVizPanel.tsx` with D3 force-graph, timeline, chord renderers
3. Wire PUBLISH/SUBSCRIBE signal bus (already built in Phase 1)
4. Demo: linked grid + force-graph

### Phase 3: MUI forms + governance
1. Add `CREATE FORM` to parser
2. Create `IxqlFormPanel.tsx` with MUI form generation
3. Implement `GOVERNED BY` clause — constitutional validation
4. Implement `HEXAVALENT validation` — six-state form logic (T/P/U/D/F/C)
5. Demo: belief editor with constitutional constraints

### Phase 4: Agentic dashboards
1. Add `ON VIOLATION` reactive triggers
2. Panels issue IXQL commands via PR Control API
3. Saved queries as governance artifacts in `state/`

## Security Constraints

- NO arbitrary JS expressions in IXQL
- NO dynamic imports from IXQL strings
- NO raw HTML cell renderers — registry templates only
- Whitelisted pure functions only: DAYS_SINCE, FORMAT_PERCENT, COALESCE
- JSON-schema validated props via registry
- Registry-only template resolution
- AG-Grid cell renderers from trusted templates, never IXQL

## Bundle Size Strategy

- Lazy-load widget families by kind: `React.lazy(() => import('./IxqlGridPanel'))`
- D3 imported modularly (d3-scale, d3-force, d3-selection)
- AG-Grid Community only (enterprise features gated)
- MUI tree-shaken per-component

## Performance Constraints

- Separate Three.js scene graph from panel graph (different update cadences)
- Virtualize large grids (AG-Grid handles this natively)
- Throttle cross-widget PUBLISH/SUBSCRIBE broadcasts
- Workerize D3 force simulations for large graphs
- Keep WebGL context count low (SVG/Canvas for 2D viz, not separate WebGL)
