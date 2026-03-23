# Render Critic — Behavioral Tests

Pipeline: `pipelines/render-critic.ixql`
Policy: `policies/visual-critic-policy.yaml`
Skill: `.claude/skills/demerzel-render-critic/SKILL.md`
Domain: ga (any React/Vite UI project)

## Test Cases

### TC-RC-01: Console error detected and auto-fixed

**Given:** A React component `Dashboard.tsx` that renders but produces a `TypeError: Cannot read property 'map' of undefined` in the console due to uninitialized state
**When:** The render critic detects the error in Step 3 and classifies it as a runtime error in Step 4
**Then:** The classifier proposes adding a null check or default empty array, applies the fix with confidence 0.80, HMR reloads, and the console is clean on re-read
**Verify:** Runtime errors are correctly classified, fix is applied autonomously at the appropriate confidence level, and the fix actually resolves the error (not just suppresses it)

### TC-RC-02: Blank page triggers lifecycle check

**Given:** A component that imports a context provider but the provider is not mounted in the component tree, resulting in a blank page with a React error boundary message in the console
**When:** The render critic reads the console and finds a render error matching "Minified React error" or error boundary output
**Then:** The classifier identifies it as a render error (confidence 0.70), checks the component mount lifecycle, identifies the missing provider, and proposes wrapping the component or adding the provider to the tree
**Verify:** Blank page / mount failure errors are correctly distinguished from syntax or runtime errors; the fix addresses the root cause (missing provider) rather than the symptom (blank page)

### TC-RC-03: Max iterations prevents infinite loop

**Given:** A component with a deeply structural error (e.g., circular dependency causing infinite re-render) that cannot be resolved by any of the 4 error classifiers
**When:** The render critic applies fixes for 5 iterations, each time finding new or persisting errors
**Then:** After iteration 5, the loop terminates per Article 9 (Bounded Autonomy), an escalation fires per Article 6, and a Discord alert is sent explaining the unresolved errors and requesting human intervention
**Verify:** The system does not loop indefinitely; iteration count is strictly enforced at 5; escalation includes enough context (error messages, attempted fixes) for a human to diagnose the issue

### TC-RC-04: Visual score below threshold triggers suggestions

**Given:** A component that renders error-free but has poor visual quality — text with contrast ratio 2.5:1 (fails WCAG AA), overlapping elements, and a missing icon
**When:** The render critic captures a screenshot in Step 6 and scores it in Step 7
**Then:** Overall visual score is below 0.7 (e.g., 0.45), with dimension breakdown: layout_fidelity=0.5, color_contrast=0.3, responsiveness=0.8, component_completeness=0.4. Specific suggestions are provided for each failing dimension: increase text contrast, fix element overlap via CSS, and add the missing icon
**Verify:** Per Article 2 (Transparency), the score breakdown is reported at the dimension level, not just an aggregate number; each suggestion maps to a concrete CSS/JSX change, not a vague recommendation

### TC-RC-05: Score >= 0.9 marks as ship-ready

**Given:** A component that renders error-free and scores 0.92 on the first render, then 0.91 on the second render after a minor re-check
**When:** The render critic evaluates consecutive high scores in Step 10
**Then:** After the second consecutive score >= 0.9, the component is marked as SHIP in `state/render-critic/ship-ready.json`, a Discord alert confirms ship-readiness with the component path and score, and the consecutive counter resets
**Verify:** A single score of 0.92 does NOT trigger ship-ready — only 2 consecutive scores >= 0.9. If an intermediate render scores 0.85, the consecutive counter resets to 0 and must restart

### TC-RC-06: Error patterns harvested for Seldon

**Given:** The render critic has completed 10 cycles across different components, accumulating fix proposals: 6 null-check fixes for `TypeError: Cannot read property`, 3 missing provider fixes, 1 CSS module resolution fix
**When:** Step 11 (Compound) runs after each cycle
**Then:** The pattern "TypeError: Cannot read property → add null check / default value" is promoted as a high-confidence auto-fix template (seen 6 times, success rate > 90%). The pattern is written to `state/render-critic/error-patterns.json` and taught to Seldon as a reusable knowledge artifact
**Verify:** Patterns compound over time — the system gets better at fixing common errors. Rare or low-success-rate patterns are logged but not promoted. Per the compounding principle, no insight dies — every fix attempt teaches the system something
