---
name: demerzel-perception-loop
description: Phase 3 visual perception loop — generate UI targets, diff against actual renders, and auto-fix iteratively until convergence.
---

# Demerzel Perception Loop — Target-Driven Visual Convergence

Phase 1 (render-critic) gave the AI eyes — it can see what it built. Phase 3 gives the AI a blueprint — it knows what it *should* have built, and closes the gap automatically.

The perception loop generates a reference target from a natural-language UI description, screenshots the actual render, computes pixel-level and semantic similarity, identifies discrepancies, generates fixes, and re-renders until the actual converges on the target.

## Usage

`/demerzel perception-loop [component-path] --target [description|image-path]`

**Examples:**

```
/demerzel perception-loop src/components/Dashboard.tsx --target "dark theme dashboard with 3-column grid, left sidebar nav, header with breadcrumbs"
/demerzel perception-loop src/pages/demos/Spectrum.tsx --target refs/spectrum-mockup.png
/demerzel perception-loop src/components/Card.tsx --target "minimal card with rounded corners, subtle shadow, 16px padding, sans-serif typography"
```

## Requirements

- **Chrome DevTools MCP** — reads console errors, DOM state
- **Vite dev server** — must be running for HMR reload
- **Windows MCP** — captures browser viewport screenshots
- **Render Critic skill** — Phase 1 prerequisite (error-free render before perception scoring)

## Pipeline

```
Phase A: Target Generation
    Step 1: Parse target specification
        ↓ natural-language description OR reference image path
    Step 2: Generate reference representation
        ├── Text target → structured UI spec (layout tree + style tokens)
        └── Image target → load reference image directly
    Step 3: Decompose into scorable dimensions
        ↓ extract: layout structure, color palette, typography, spacing, component inventory

Phase B: Baseline Capture (delegates to render-critic Steps 1-6)
    Step 4: Ensure error-free render
        ↓ run render-critic error loop (max 5 iterations)
    Step 5: Screenshot actual render
        ↓ capture via Windows MCP

Phase C: Perception Diff
    Step 6: Structural comparison
        ├── Layout diff — expected vs actual component hierarchy
        ├── Color diff — palette extraction and distance (CIEDE2000)
        ├── Typography diff — font family, size, weight, line-height
        ├── Spacing diff — margin/padding measurements vs target
        └── Component inventory — missing/extra/misplaced elements
    Step 7: Compute similarity scores
        ↓ per-dimension scores + weighted aggregate

Phase D: Auto-Fix Loop
    Step 8: Rank discrepancies by impact
        ↓ highest-weight dimension failures first
    Step 9: Generate targeted fix
        ├── Layout mismatch → adjust grid/flex/position CSS
        ├── Color mismatch → update color values, CSS variables
        ├── Typography mismatch → fix font-family, size, weight
        ├── Spacing mismatch → adjust margin/padding values
        └── Missing component → generate JSX stub
    Step 10: Apply fix → HMR reload → re-screenshot → re-score
        ↓ return to Step 6

Phase E: Convergence Gate
    Step 11: Check convergence criteria
        ↓ converged → Step 12
        ↓ not converged AND iterations < max → Step 8
        ↓ not converged AND iterations = max → Step 13
    Step 12: Ship verdict
        ↓ similarity >= 0.85 for 2 consecutive iterations → CONVERGED
    Step 13: Escalation
        ↓ report best score achieved + remaining discrepancies → human

Phase F: Compound
    Step 14: Harvest patterns
        ↓ target→fix mappings → Seldon knowledge base
        ↓ convergence velocity → optimize future fix ordering
```

## Steps (Detailed)

### Step 1: Parse Target Specification

Accept one of two target forms:

| Form | Input | Output |
|------|-------|--------|
| Natural language | `--target "dark dashboard with sidebar"` | Structured UI spec |
| Reference image | `--target refs/mockup.png` | Reference image for direct comparison |

For natural-language targets, extract a structured spec:

```yaml
target_spec:
  layout:
    type: grid|flex|stack
    columns: N
    regions: [header, sidebar, main, footer]
  colors:
    background: dark|light|custom
    primary: color description
    accent: color description
  typography:
    family: sans-serif|serif|mono
    scale: compact|normal|spacious
  spacing:
    density: tight|normal|relaxed
    unit: px value
  components:
    - name: component description
      location: region
      required: true|false
```

### Step 2: Generate Reference Representation

For **text targets**: Convert the structured spec into a reference model — not a rendered image, but a scorable set of assertions about what the UI should look like. Each assertion maps to a scoring dimension.

For **image targets**: Load the reference image directly. Extract the same scorable dimensions via visual analysis of the reference.

### Step 3: Decompose into Scorable Dimensions

From either target form, produce a scoring rubric:

```yaml
rubric:
  layout_structure:
    weight: 0.30
    assertions:
      - "3-column grid layout present"
      - "sidebar on left, 250px wide"
      - "header spans full width"
  color_palette:
    weight: 0.25
    assertions:
      - "background is dark (#1a1a2e or similar)"
      - "primary text is light (#e0e0e0 or similar)"
      - "accent color present in interactive elements"
  typography:
    weight: 0.20
    assertions:
      - "sans-serif font family"
      - "heading size >= 24px"
      - "body text 14-16px"
  spacing:
    weight: 0.15
    assertions:
      - "consistent 16px padding in content areas"
      - "8px gap between grid items"
  component_inventory:
    weight: 0.10
    assertions:
      - "navigation links in sidebar"
      - "breadcrumb in header"
      - "data cards in main area"
```

### Steps 4-5: Baseline Capture

Delegate entirely to render-critic. The perception loop does NOT begin scoring until the render is error-free. This is a hard prerequisite — never score a broken page.

```
Invoke: /demerzel render-critic [component-path]
Wait for: error-free render (render-critic Steps 1-5)
Capture: screenshot via Windows MCP (render-critic Step 6)
```

### Step 6: Structural Comparison

Compare the actual screenshot against each rubric assertion:

| Dimension | Method | Metric |
|-----------|--------|--------|
| Layout structure | DOM inspection via DevTools + visual analysis | Assertion pass rate (0-1) |
| Color palette | CSS computed style extraction + screenshot sampling | CIEDE2000 color distance (< 10 = match) |
| Typography | Computed font properties via DevTools | Exact match on family, within 2px on size |
| Spacing | Computed margin/padding via DevTools | Within 4px of target |
| Component inventory | DOM element presence check | Present/absent binary per component |

### Step 7: Compute Similarity Scores

```
dimension_score = assertions_passed / total_assertions  (per dimension)
aggregate_score = sum(dimension_score * dimension_weight)
```

Report format:

```
Perception Loop — Iteration 1
  Layout structure:     0.67  (2/3 assertions passed)
  Color palette:        0.33  (1/3 assertions passed)
  Typography:           1.00  (3/3 assertions passed)
  Spacing:              0.50  (1/2 assertions passed)
  Component inventory:  0.80  (4/5 assertions passed)
  ─────────────────────────────────────
  Aggregate:            0.63  (target: 0.85)

  Top discrepancies:
    1. [color] Background is #ffffff, target is dark (#1a1a2e) — delta: 0.25 weight
    2. [layout] Missing sidebar — delta: 0.10 weight
    3. [spacing] Content padding 8px, target 16px — delta: 0.075 weight
```

### Steps 8-9: Rank and Fix

Order discrepancies by `dimension_weight * (1 - dimension_score)` — fix highest-impact gaps first.

For each fix:

1. **State the discrepancy** — what is wrong and how it differs from target
2. **Propose the fix** — specific CSS/JSX change with confidence level
3. **Apply if confidence >= 0.7** — per governance thresholds
4. **Escalate if confidence < 0.5** — do not guess on low-confidence visual fixes

Fix confidence by type:

| Fix Type | Confidence | Rationale |
|----------|-----------|-----------|
| Color value change | 0.95 | Deterministic — swap one value |
| Spacing adjustment | 0.90 | Deterministic — change margin/padding |
| Font property change | 0.90 | Deterministic — change font-family/size |
| Layout restructure | 0.70 | May affect sibling components |
| Component addition | 0.60 | Requires understanding component API |
| Complex layout rewrite | 0.40 | Structural change — escalate |

### Step 10: Apply-Reload-Rescore Cycle

```
Apply fix → wait for HMR (~500ms) → re-screenshot → re-score
```

Each iteration is logged with:
- Fix applied (file, line, change)
- Before/after scores per dimension
- Aggregate score delta
- Cumulative iteration count

### Step 11: Convergence Criteria

```
CONVERGED if:
  aggregate_score >= 0.85 for 2 consecutive iterations

CONTINUE if:
  aggregate_score < 0.85 AND iterations < max_iterations
  AND score_delta > 0.02 (still making progress)

STALLED if:
  score_delta <= 0.02 for 2 consecutive iterations (not improving)
  → escalate even if under max_iterations

EXHAUSTED if:
  iterations >= max_iterations
  → escalate with best-achieved score
```

### Step 12: Ship Verdict

When converged:
- Report final scores per dimension
- Confirm 2 consecutive iterations above threshold
- Mark component as PERCEPTION-VERIFIED in state
- Record target spec + final score for regression testing

### Step 13: Escalation

When stalled or exhausted:
- Report best score achieved and iteration history
- List remaining discrepancies ranked by impact
- Suggest manual fixes for low-confidence items
- Per Article 6 (Escalation) — human decides next steps

### Step 14: Compound

Harvest for Seldon knowledge base:
- **Target-to-fix mappings** — "dark background" target + "#ffffff found" → "set background-color: #1a1a2e"
- **Convergence velocity** — which fix types yield the most score improvement per iteration
- **Common gaps** — frequently failing assertions become prevention rules in MetaBuild

## Scoring Weights

| Dimension | Weight | Rationale |
|-----------|--------|-----------|
| Layout structure | 0.30 | Structural correctness is the foundation |
| Color palette | 0.25 | Color is the most immediately visible quality signal |
| Typography | 0.20 | Readability is critical for usability |
| Spacing | 0.15 | Contributes to polish but less critical than structure |
| Component inventory | 0.10 | Missing components are caught by layout/completeness overlap |

## Convergence Thresholds

| Threshold | Value | Meaning |
|-----------|-------|---------|
| Converged | >= 0.85 (2 consecutive) | Target achieved — ship |
| Acceptable | >= 0.70 | Close enough — minor polish remaining |
| Needs work | >= 0.50 | Significant gaps — continue iterating |
| Far from target | < 0.50 | Major structural differences — likely needs human guidance |

## Iteration Limits

| Parameter | Value | Rationale |
|-----------|-------|-----------|
| Max iterations | 8 | More than render-critic (5) because target convergence is harder |
| Stall detection | 2 iterations with delta <= 0.02 | Stop wasting cycles on diminishing returns |
| Max fixes per iteration | 3 | Apply multiple non-conflicting fixes per cycle for efficiency |

## Governance

- **Article 2 (Transparency):** Target spec, rubric, and per-iteration scores are always shown. Every fix explained.
- **Article 6 (Escalation):** Stalled loops, exhausted iterations, and low-confidence fixes escalate to human.
- **Article 7 (Auditability):** Full iteration log — target, actual, diff, fix, score delta — persisted to state.
- **Article 8 (Observability):** Convergence velocity and per-dimension scores are observable metrics.
- **Article 9 (Bounded Autonomy):** Max 8 iterations. Stall detection at 2. Confidence gates on every fix.
- **Article 4 (Proportionality):** Fixes are scoped to the minimum change needed per discrepancy.

## State

```
state/perception-loop/
  target-spec.json          — current target specification (structured rubric)
  iteration-log.json        — per-iteration scores, fixes applied, deltas
  convergence-history.json  — historical convergence data across components
  verified-components.json  — components that passed perception verification
```

## Relationship to Render Critic

```
render-critic (Phase 1)          perception-loop (Phase 3)
─────────────────────           ──────────────────────────
Fix console errors               Generate target from description
Score visual quality              Diff actual vs target
Ship when score >= 0.9            Converge actual toward target
No reference target               Reference-driven scoring
Reactive (fix what's broken)      Proactive (build toward intent)

Dependency: perception-loop delegates error-fixing to render-critic.
            perception-loop begins AFTER render-critic achieves error-free render.
```

## Anti-Patterns

- **Scoring a broken render:** Never run perception diff on a page with console errors. Delegate to render-critic first.
- **Pixel-perfect obsession:** The target is a description, not a pixel grid. Score semantically — "dark background" means any dark color, not exactly #1a1a2e.
- **Fixing everything at once:** Apply max 3 fixes per iteration. More causes cascading layout shifts that obscure individual fix impact.
- **Ignoring stall detection:** If score stops improving, the remaining gap is likely structural. Do not burn iterations on diminishing returns.
- **Target drift:** The target spec is locked at Step 3. Do not modify the rubric mid-loop based on what the actual render looks like.
- **Skipping render-critic:** Phase 3 extends Phase 1, it does not replace it. The error-free prerequisite is non-negotiable.
