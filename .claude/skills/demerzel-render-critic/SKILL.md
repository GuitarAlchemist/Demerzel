---
name: demerzel-render-critic
description: Visual perception loop — detect errors, screenshot, score, and iteratively fix AI-generated UI components until ship-ready.
---

# Demerzel Render Critic — Close the Perception Loop

AI writes code blind. This skill gives it eyes. Run the render critic to detect console errors, capture screenshots, score visual quality, and iteratively fix until the component is ship-ready.

## Usage

`/demerzel render-critic [component-path]` — run the full perception loop on a component

**Examples:**

```
/demerzel render-critic src/components/Dashboard.tsx
/demerzel render-critic src/pages/demos/SpectralAnalyzer.tsx
```

## Requirements

- **Chrome DevTools MCP** — reads console errors, warnings, React error boundaries
- **Vite dev server** — must be running (`npm run dev` or equivalent)
- **Windows MCP** — captures browser viewport screenshots for visual scoring

## Pipeline

```
Step 1: Start dev server (if not running)
    ↓ verify Vite responds on localhost
Step 2: Open the target component page in browser
    ↓ navigate to route that renders the component
Step 3: Read Chrome DevTools console
    ↓ extract errors and warnings
Step 4: Classify errors (parallel)
    ├── Syntax errors → auto-fix (confidence 0.95)
    ├── Runtime errors → classify + fix (confidence 0.80)
    ├── Render errors → check mount lifecycle (confidence 0.70)
    └── Layout errors → fix stylesheet (confidence 0.75)
Step 5: Apply fixes, re-render, re-check
    ↓ loop until error-free (max 5 iterations)
Step 6: Screenshot via Windows MCP
    ↓ capture browser viewport
Step 7: Score visual quality
    ├── Layout fidelity (35%)
    ├── Color contrast / WCAG (25%)
    ├── Responsiveness (20%)
    └── Component completeness (20%)
Step 8: Governance gate (score >= 0.7)
    ↓ fail → Step 9 (suggest fixes)
    ↓ pass → Step 10 (ship check)
Step 9: Suggest visual fixes per dimension
    ↓ return to Step 5 with suggestions
Step 10: Ship-ready check
    ↓ score >= 0.9 for 2 consecutive renders → SHIP
Step 11: Compound
    ↓ harvest error patterns → Seldon
```

## Steps (Detailed)

### 1. Start Dev Server

Verify Vite dev server is running. If not, start it:

```
Check: curl http://localhost:5173 (or configured port)
If down: npm run dev (background)
Wait: until server responds (max 30s)
```

### 2. Open Component Page

Navigate the browser to the route that renders the target component. If the component is not routed, create a temporary demo page.

### 3. Read DevTools Console

Use Chrome DevTools MCP to read all console output since page load:

```
Filter: level = "error" or level = "warning"
Extract: message, source file, line, column, stack trace
```

### 4. Classify and Fix Errors

For each error, classify into one of 4 categories and propose a fix:

| Category | Confidence | Strategy |
|----------|-----------|----------|
| Syntax | 0.95 | Deterministic fix — missing brackets, typos |
| Runtime | 0.80 | Analyze stack trace, fix data flow |
| Render | 0.70 | Check lifecycle hooks, providers, boundaries |
| Layout | 0.75 | Fix CSS imports, module resolution |

### 5. Iterative Fix Loop

Apply the highest-confidence fix first. Re-render via HMR. Re-read console. Repeat until clean or max 5 iterations reached.

**Explain each fix:** Before applying, state what the error is, why the fix works, and what confidence level justifies autonomous action.

### 6. Screenshot Capture

Once error-free, capture the browser viewport using Windows MCP Screenshot tool. This is the serial bottleneck (~200ms per Amdahl's analysis).

### 7. Visual Quality Scoring

Score the screenshot across 4 dimensions:

- **Layout fidelity (35%):** Components positioned correctly, proper spacing, grid alignment
- **Color contrast (25%):** WCAG AA compliance — 4.5:1 for normal text, 3:1 for large text
- **Responsiveness (20%):** No overflow, proper reflow, adequate touch targets
- **Component completeness (20%):** All expected elements present, no placeholder text

### 8-9. Quality Gate and Suggestions

If overall score < 0.7, provide specific suggestions per failing dimension. Each suggestion maps to a concrete CSS or JSX change.

### 10. Ship-Ready Verdict

Score >= 0.9 for 2 consecutive renders → mark as SHIP. Single high score is not sufficient — prevents false positives from lucky renders.

### 11. Compound

Harvest error patterns and fix templates for Seldon knowledge base. Common errors become prevention rules; successful fixes become auto-fix templates.

## Governance

- **Article 2 (Transparency):** Every fix is explained before applying. Score breakdown is always shown.
- **Article 6 (Escalation):** Errors that cannot be auto-fixed after 5 iterations escalate to human.
- **Article 7 (Auditability):** Every iteration logged — error, fix applied, result.
- **Article 8 (Observability):** Visual quality score is an observable metric.
- **Article 9 (Bounded Autonomy):** Max 5 fix iterations. Must explain each fix. Ship requires 2 consecutive high scores.

## State

```
state/render-critic/
  consecutive-high.json   — tracks consecutive >= 0.9 scores
  ship-ready.json         — latest ship verdict
  error-patterns.json     — harvested error → fix patterns
```

## Anti-Patterns

- **Infinite fix loop:** Max 5 iterations enforced. If hit, problem is structural — escalate.
- **Scoring without fixing errors:** Error-free render is a prerequisite. Never score a broken page.
- **Single-render ship verdict:** Requires 2 consecutive high scores. One lucky render is not sufficient.
- **Fix without explanation:** Every applied fix must state what, why, and at what confidence.
