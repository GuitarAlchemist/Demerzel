---
module_id: vc-007-weave-seams-as-scene-contracts
department: visual-computing
course: "Keep Weave Crossings Correct across a Godot Scene Boundary"
level: intermediate
prerequisites: [vc-005-craft-details-through-blender-to-godot]
estimated_duration: "40 minutes"
produced_by: codex-project-pilot
research_cycle: visual-computing-2026-10-12-007
version: "0.1.0"
---

# Keep Weave Crossings Correct across a Godot Scene Boundary

> **Department of Visual Computing** | Intermediate | 40 minutes | English draft; synthetic crossing fixture, no Godot import, learner trial, human review, or publication

## Objectives and project question

After this lesson, you can distinguish a weave's crossing order from its rendered appearance, find a composition error at a tile seam, give crossings stable identities, and design a Godot scene gate that can reject a visually appealing but incorrect sample. **Project question:** if a woven detail becomes an object in the proposed Godot observatory, how can its over/under structure survive repetition and rendering? This is a deliberately narrow plain-weave model, not a simulation of yarn tension, a textile-history claim, or a finished Godot feature.

[VC-005](vc-005-craft-details-through-blender-to-godot.md) asks whether Blender mesh cleanup might erase a small craft feature. That lesson checks what survives an asset pipeline. Here the failure can happen earlier: a tile may be composed into the wrong pattern before any mesh exists. A [pinned GA Godot integration plan](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/docs/plans/parked/2026-03-28-feat-godot-integration-plan.md) sketches an observatory scene, but its proposed scene is not evidence that this sample has been imported. The [fixture and evaluator](https://github.com/GuitarAlchemist/Demerzel/tree/f23ccae6c049d9066a1be2221c68f3b0bcf48373/state/streeling/fixtures/visual-computing/vc-007) in this course are executable, synthetic, and independent of a renderer.

## 1. Put craft semantics before pixels

The fixture starts with a 3-by-3 crossing tile. A warp thread runs in one declared direction and a weft thread in the other. At global coordinates `(x, y)`, the simplified rule says warp is above weft when `(x + y + phase) % 2 == 0`; otherwise weft is above warp. `phase = 0`. This rule is an abstraction chosen for the exercise. Actual textile structures, materials, and craft practices can be more varied. The contract here is only that the *declared* plain-weave alternation remains true after composition.

The fixture repeats the tile twice in each direction, giving six warp positions, six weft positions, and `6 × 6 = 36` crossings. The pair `(x, y)` gets an ID `w<x>-f<y>`. IDs are global, so `w3-f0` means the same crossing before and after a mesh or scene is generated. Material color, camera position, and apparent thread height may help a viewer, but none can replace that identity and its over/under value. A renderer should receive the validated manifest; it should not invent a new crossing rule from a prompt or shader.

### Exercise 1: name the crossing

Under phase zero, what are the IDs and over/under values at `(2, 0)` and `(3, 0)`? Why must the IDs be assigned before the scene is rendered?

> **Answer:** The IDs are `w2-f0` and `w3-f0`. Since `2 + 0` is even, warp is over at `w2-f0`; since `3 + 0` is odd, weft is over at `w3-f0`. Stable IDs let an import test compare the scene to the source manifest and locate a wrong crossing. A screenshot alone cannot establish which crossing a visible highlight represents.

## 2. Find the seam that a local tile test misses

There are two ways to repeat the base tile. **Global parity** evaluates the rule on the full 6-by-6 coordinates. **Restarted tile parity** evaluates `x % 3` and `y % 3` in each copy. Every 3-by-3 tile is locally alternating under the restarted rule. Because the tile width is odd, however, its last column and the next tile's first column both say warp-over in the first row. The vertical seam has an analogous defect. This is a composition bug, not a texture problem.

Run `python state/streeling/fixtures/visual-computing/vc-007/evaluate_weave.py` from the Demerzel root with the [local trial input](../../../fixtures/visual-computing/vc-007/weave-trial.json). It enumerates all 36 crossings under each rule, checks adjacent pairs horizontally and vertically, and reports exact violating IDs. For the supplied fixture, global parity yields 0 adjacency violations; restarted tile parity yields 12. Six are horizontal seam pairs, six are vertical seam pairs. At the seam intersection two distinct adjacent pairs are reported; the count is of violated *relations*, not faulty pixels or unique crossing IDs. The evaluator also rejects a sample whose yarn diameter is at least its spacing. Its spacing-to-diameter ratio of `5 / 2 = 2.5` is merely an input sanity check; it is not a physical clearance or collision proof.

### Exercise 2: locate the first counterexample

The first row of the restarted result is `warp, weft, warp, warp, weft, warp`. Which adjacent pair fails, and what should the fourth value be under the global rule? Does a correct 3-by-3 preview clear the 6-by-6 sample?

> **Answer:** `w2-f0` and `w3-f0` both say warp-over, so that pair violates alternation. Under global parity, `w3-f0` should say weft-over. A correct local preview does not clear the composed sample because it never inspects the tile boundary.

## 3. Keep identity, semantics, and geometry separate

An export manifest for a scene trial should carry the source-program hash, sample ID, dimensions, physical scale convention, stable crossing IDs, and each over/under value. The provided JSON is a *trial specification*, and the evaluator derives those values; it is not an exported Godot manifest. A future adapter can use this result to build mesh segments or instantiate scene nodes, but the adapter must preserve IDs and values. If a visually correct woven texture has no mapping back to the crossings, reviewers cannot tell whether it follows the program or merely resembles it.

Use three gates. The **semantic gate** checks unique IDs, 36 expected crossings, and zero adjacency violations. The **geometry gate** checks that both threads exist at each crossing, the declared above/below relation is reflected in mesh or scene coordinates, and scale is consistent. The **perception gate** gives a viewer a fixed camera and asks them to identify a crossing and the thread above it. Passing one gate does not imply the others. For example, a manifest may be correct while cylinders intersect or a camera hides the over/under relation. Conversely, a persuasive image may conceal restarted parity at a seam.

### Exercise 3: classify the receipt

A future Godot screenshot looks woven. The manifest has 36 unique IDs and zero adjacency violations. A click on `w3-f0` highlights `w2-f0`, and no mesh-coordinate probe was recorded. Which gates have evidence, and which remain open?

> **Answer:** The manifest supports the semantic gate for this declared pattern. The wrong highlight fails the scene's identity binding, and the missing coordinate probe leaves geometry unassessed. The screenshot alone cannot certify crossing order or viewer comprehension. Fix the mapping, record the above/below coordinates, and rerun the interaction before considering the scene trial successful.

## 4. Compare the rule with a cheaper scene alternative

The proposed Godot object should compete with a simple diagram or text label, not only with an empty scene. If the product purpose is merely to explain a governance dependency, a 2D labeled grid may convey it more reliably than a 3D weave. A 3D sample earns its maintenance cost only if it improves a predeclared learning or inspection task. Hold camera, lighting, labels, task wording, and sample dimensions fixed across the comparison. Preserve the program JSON, derived manifest, import log, raw captures, click traces, and per-learner answers. Record frame time separately; triangle count by itself does not measure comprehension.

A DSL is useful here only if it reduces errors or authoring effort compared with a plain manifest and a small validator. The current fixture demonstrates a compositional invariant and a counterexample, not that a new language should be adopted. Hidden costs include units, IDs across edits, crossing-to-mesh mapping, export validation, accessibility, and explaining how a visible yarn segment represents a semantic relation. A falsifier for the DSL proposal is that an ordinary JSON manifest plus a short validator yields equal correctness and faster authoring in a repeated task.

### Exercise 4: design the comparison

Variant A uses global parity, a fixed camera, and plain material. Variant B restarts parity at each tile, changes the camera, and adds high-contrast colors. Five viewers prefer B. What can be concluded, and what single-variable rerun should come first?

> **Answer:** The preference cannot establish that the seam is correct or that the altered camera or color caused the preference. B has 12 violated adjacent relations in the fixture. First compare the two crossing rules with the same camera, material, labels, and task; keep the validator result and each viewer's crossing answer. Then vary camera or material independently. If the semantic gate is mandatory, B is rejected even if it looks better.

## 5. State a release gate that can fail

Before putting the sample in an observatory scene, require a versioned source program and derived manifest, a Godot import with a stable ID-to-object map, a replayable interaction trace for at least one crossing on each side of a tile seam, and a raw capture with a fixed viewpoint. Decide a learner task and performance ceiling before running it. A sample with an unbound crossing or broken seam fails even when its screenshot looks attractive. A sample with correct topology but worse task comprehension than a 2D baseline should be revised rather than promoted as an educational improvement.

This gate is deliberately stricter than running the Python evaluator. No Godot import, GPU capture, frame-time measurement, or learner comparison is included in this course package. The executable fixture proves only that the two specified rules differ under a declared checker. It cannot prove real cloth behavior or renderer quality. Keep this boundary visible when reporting progress on ComfyUI, Blender, Godot, or a later release.

### Exercise 5: decide from mixed evidence

Suppose an adapter exports all 36 crossing IDs, a Godot self-test confirms zero manifest violations, and a capture is visually clear. A seam click returns the wrong crossing once in ten replays. Three of four learners identify the thread above a target crossing, versus four of four on a labeled 2D diagram; frame time is within budget. Should the 3D sample be accepted under this lesson's gate?

> **Answer:** No. The incorrect click fails the identity-binding requirement, and the small learner trial does not beat the declared 2D baseline. Retain source and output hashes, scene revision, import log, ten raw click traces, captures, individual answers, and frame-time samples. Fix the binding and test the explanation again under the same task. These numbers are hypothetical exercise data, not measured project results.

## Evidence and limits

- The fixture at Demerzel commit `f23ccae6c049d9066a1be2221c68f3b0bcf48373` gives reproducible counts for a synthetic parity rule. It is an educational checker, not a textile simulator or Godot renderer.
- The pinned GA plan motivates a possible observatory use; it does not establish a live scene import for this weave. VC-005 supplies an asset-cleanup question, while this lesson tests composition before export.
- The viewer counts, click error, and frame-time outcome in Exercises 4 and 5 are invented. No human review, learner attempt, translation, scene capture, release, or anonymous public readback is claimed.
