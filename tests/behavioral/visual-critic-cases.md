# Behavioral Test Cases: Visual Critic Policy

These test cases verify the render-critic perception loop: code is rendered, perceived, scored, and iteratively fixed.

## Test 1: Console Errors Must Be Fixed Before Visual Scoring

**Setup:** A React component renders but produces 3 console.error messages related to missing props.

**Input:** Render critic cycle starts on the component.

**Expected behavior:**
- Agent detects console errors during render step
- Agent does NOT proceed to visual scoring
- Agent reports: "3 console errors detected — fixing errors before visual assessment"
- Agent fixes the console errors first, then re-renders
- Visual scoring begins only after error-free render is confirmed

**Violation if:** Visual scoring runs on a component with console errors, or errors are ignored.

**Constitutional basis:** Prerequisites — error_free_render must be satisfied before scoring.

---

## Test 2: Layout Fidelity Scored and Below Threshold — Fix Cycle Triggered

**Setup:** A component renders without errors but has overlapping elements and broken grid alignment. Layout fidelity scores 0.3 (below acceptable threshold).

**Input:** Visual scoring runs on the rendered component.

**Expected behavior:**
- Screenshot is captured and analyzed
- Layout fidelity dimension scores 0.3 (weight: 0.35)
- Agent identifies specific issues: "Overlapping elements in header, grid misalignment in card section"
- Fix cycle is triggered: modify CSS/JSX → re-render → re-score
- Process iterates until score improves or max iterations reached

**Violation if:** A low layout score does not trigger a fix cycle, or the agent reports "looks good" without actually perceiving the render.

**Constitutional basis:** Visual scoring dimensions — layout_fidelity weight 0.35.

---

## Test 3: File Change Triggers Automatic Render Critic

**Setup:** A developer modifies `src/components/Dashboard.tsx` and saves the file.

**Input:** File change detected in `src/**/*.tsx`.

**Expected behavior:**
- File change trigger fires for Dashboard.tsx
- Render critic cycle starts automatically
- Component is rendered, screenshot captured, scored
- Results are reported: scores per dimension, overall assessment, any issues found
- If all scores pass: "Dashboard.tsx renders correctly — no issues detected"

**Violation if:** A .tsx file change does not trigger the render critic, or the cycle runs but results are not reported.

**Constitutional basis:** Triggers — file_change in src/**/*.tsx starts render critic cycle.

---

## Test 4: Blank Page Detected as Critical Failure

**Setup:** A component renders to a completely blank page — no visible elements, white screen.

**Input:** Render critic screenshot analysis.

**Expected behavior:**
- Screenshot analysis detects blank/empty page
- All visual scoring dimensions score near 0
- Agent reports critical failure: "Component renders a blank page — no visible content"
- Agent investigates root cause: missing imports, failed data fetch, conditional render returning null
- Fix cycle is immediately triggered with high priority

**Violation if:** A blank page passes visual scoring, or is scored on dimensions as if content were present.

**Constitutional basis:** Rationale — the perception gap means blank pages go undetected until a human looks.
