---
module_id: cs-009-composing-origami-panel-constraints
department: computer-science
course: "Compose Origami Constraints before Accepting a Rigid Stack"
level: intermediate
prerequisites: [cs-001-thinking-algorithmically, cs-006-ixql-pipeline-composition]
estimated_duration: "40 minutes"
produced_by: codex-project-pilot
research_cycle: computer-science-2026-10-21-009
version: "0.1.0"
---

# Compose Origami Constraints before Accepting a Rigid Stack

> **Department of Computer Science** | Intermediate | 40 minutes | English draft; subject and learner review pending

## Objectives and project question

You will turn flat joints into equivalence classes, preserve directed constraints between those classes, distinguish local overlap tests from a global stacking constraint, and read an incomplete result without inventing a placement. The practical question is: **which result may an agent pass to a future Blender or Godot adapter when IX has checked an origami state?** A visible craft object needs a stated interpretation of the analysis, because one successful check may coexist with a refusal under another model.

The case study is the implemented [IX thickness module](https://github.com/GuitarAlchemist/ix/blob/d7c22fdd6a62becb66b9d7246ea85850e7c55854/crates/ix-origami/src/thickness.rs) and its [integration tests](https://github.com/GuitarAlchemist/ix/blob/d7c22fdd6a62becb66b9d7246ea85850e7c55854/crates/ix-origami/tests/thickness.rs), both pinned to `d7c22fdd6a62becb66b9d7246ea85850e7c55854`. The module reads a material thickness in the crease pattern's coordinate units. It examines one stated flat folded state; it does not plan folding motion or export a scene. The [course fixture](../../../fixtures/computer-science/cs-009/README.md) contains small graph derivations, clearly separated from the actual Rust test results.

## 1. Compose faces into panels first

A face is a polygon in the folded-state description. A panel in this model is a set of faces connected by flat joints that must keep one height. The implementation's `panels` function joins their sets and maps every face to the smallest indexed face in its connected component. That representative is an algorithmic label. It is not a permanent object identifier, and renumbering the input can change it while preserving the represented panel.

Consider faces 0, 1, and 2. Faces 0 and 1 share a flat joint. The stated relations put 2 above 0 and 1 above 2. As a face graph, the lower-to-upper arcs are `0 → 2 → 1`, which has no cycle. If we assign each face its own height, the apparent answer is levels 0, 1, and 2. This violates the model: faces 0 and 1 belong to one rigid panel and cannot take different heights.

After joining the flat-connected faces, the panel map is `[0, 0, 2]`. The two constraints become `panel 0 → panel 2` and `panel 2 → panel 0`. The cycle is now visible. This is a quotient construction: first group objects that must move together, then apply the order constraints to those groups. Checking each part before composition misses the requirement introduced by their shared identity.

### Exercise 1: repair the misleading graph

Use the `pierced-flat-joint` fixture. Give the panel representatives and the two panel arcs. Explain why the face graph's topological order cannot justify a rigid placement. What extra implementation decision would be needed if an adapter wanted a permanent panel ID?

> **Answer:** The representatives are `[0, 0, 2]`; the arcs are `0 → 2` and `2 → 0`. The face order permits two different heights for the same flat-connected panel, so it solves the wrong constraint system. A permanent panel ID would need a declared mapping back to material/source identity across edits or permutations. The minimum-index representative alone provides no such guarantee.

## 2. Local success can coexist with a global refusal

The pinned test `a_weave_passes_the_layer_rules_but_has_no_rigid_stack` constructs four strips. Each overlaps the next in a different corner. Every local overlay cell can have a consistent order, yet the combined statements say strip 0 is above 1, 1 above 2, 2 above 3, and 3 above 0. Using lower-to-upper arcs gives `0 → 3 → 2 → 1 → 0`. No single height per strip satisfies all four inequalities for positive material thickness.

This is distinct from [VC-007](../../visual-computing/en/vc-007-weave-seams-as-scene-contracts.md), whose synthetic checker detects restarted parity at repeated tile boundaries. Here the issue is a cycle across different overlap regions in the existing IX implementation. A texture, a local crossing preview, or a successful base origami analysis cannot settle the global parallel-panel question.

The test asserts that `analyse(&weave()).unwrap().ok` is true. It also checks the optional thickness reading at `t = 0`, a tiny positive `t`, and `t = 0.5`. The graph remains cyclic, but `rigid.refused` is true only for positive `t`. At zero, the implementation still returns `levels`, `height`, and `face_levels` as absent for this cyclic reading. Do not replace an absent rigid height with zero merely because the separate `ply_height` is zero.

### Exercise 2: interpret the zero case

The weave has `ply = 2` and a cyclic panel order. What are `ply_height` and `rigid.refused` at `t = 0` and `t = 0.5`? Does either result provide a rigid face-level assignment?

> **Answer:** At zero, `ply_height = 0` and `rigid.refused = false`; at 0.5, `ply_height = 1` and refusal is true. Both cyclic reports have absent rigid levels, height, and face-level assignment. A zero-thickness non-refusal does not supply the missing witness, and the positive-thickness refusal concerns this parallel-panel model.

## 3. Acyclic constraints support a longest-path calculation

When the panel graph has a topological order, the implementation starts every level at zero. For each directed edge from a lower panel `u` to an upper panel `v`, it updates `level[v] = max(level[v], level[u] + 1)`. Processing in topological order ensures each predecessor's level is available. The highest zero-based level plus one is the chain length in panels. Multiplying by full thickness `t` gives the stack height for a fully determined ordering.

The reported `face_levels` is one witness produced by this recurrence. Other valid stacks can exist; the per-face values are not a canonical labeling of every admissible stack.

The synthetic DAG in the fixture has arcs `P → R`, `Q → R`, and `R → S`. P and Q may share level zero because the example gives no relation requiring separation between them; R must be above both, then S above R. These are abstract graph data, not an exported FOLD geometry or a claim about spatial overlap. Their purpose is to rehearse the recurrence before reading the larger crane test.

### Exercise 3: compute the chain

Assign the four synthetic DAG levels, count the panels in the longest chain, and compute height for `t = 0.2`. Why would reporting only the highest level be an off-by-one error? For comparison, which two counts does the actual crane test distinguish?

> **Answer:** P and Q are 0, R is 1, and S is 2. The chain has three panels, so height is `3 × 0.2 = 0.6` in crease-pattern units. The highest index 2 omits one occupied level. The actual crane test distinguishes maximum local ply 28 from 36 required parallel-panel levels; local occupancy and a chain across regions answer different questions.

## 4. Missing order is part of the result

The implementation counts overlapping face pairs on different panels whose order is unstated. With any such pair, `levels_exact` is false. It reports `max(chain, ply)` as a lower bound and withholds `face_levels`. Acyclic stated constraints alone cannot certify that a proposed placement respects a relation the input never specified.

The pinned `an_unstated_overlap_gives_a_lower_bound` test uses two overlapping sheets with no stated order. It expects one undetermined pair, two levels as a lower bound, and no face-level assignment. A caller must retain the exactness flag with the number. If an agent's summary discards it, a later stage may turn a lower bound into an alleged complete arrangement without anyone making that decision explicitly.

### Exercise 4: preserve uncertainty in a handoff

The synthetic incomplete-order card has chain 2, ply 3, one undetermined pair, and `t = 0.2`. What numerical height can the algorithm report, and how must it be described? Can a scene adapter use it to place every face?

> **Answer:** It reports `max(2, 3) = 3` levels and a height lower bound of 0.6, with `levels_exact = false` and `face_levels = null`. It cannot supply a complete placement. A handoff should preserve the lower-bound label, missing-pair count, source identity, and absent witness rather than promise coordinates derived from an unobserved order.

## 5. Turn the result into an inspectable decision

An agentic composition can carry the base analysis and the rigid reading together. The [pinned design decision](https://github.com/GuitarAlchemist/ix/blob/d7c22fdd6a62becb66b9d7246ea85850e7c55854/docs/adr/0007-origami-thickness-as-parallel-rigid-panels.md) explicitly keeps the thickness reading beside the base verdict. A refusal means no stack under the parallel rigid-panel assumptions. It does not prove that a material object is impossible with tilted panels, modified creases, or other construction methods. Conversely, no refusal proves manufacturability.

For a proposed Godot trial, preserve the source FOLD revision, full-thickness/unit conversion, both analysis results, any cycle witness, exactness, and the face-to-object map. Give a viewer a specific task, such as finding the relation responsible for a refusal. Compare their answer with a plain graph diagram under the same task. This is a proposed transfer experiment; the course records no renderer, export, learner trial, or performance gain. A new DSL would earn its cost only if it improves that task against a simpler typed report and existing checker.

### Exercise 5: decide what to send downstream

A future agent reports “base analysis passed; rigid refusal at positive thickness; cycle faces `[0,3], [3,2], [2,1], [1,0]`.” It proposes labeling the asset “physically impossible” and omitting the cycle because the scene looks plausible. Write a corrected user-facing statement and identify the next evidence needed for a scene demonstration.

> **Answer:** “The stated state passed the base checks, but its stated order has a cycle that prevents a stack of parallel rigid panels at this positive thickness.” Keep the cycle and assumptions. A scene demonstration needs a source-bound import and face-to-object map, an independently checkable display of the cycle, and a recorded viewer task. A screenshot alone cannot establish the graph result, physical impossibility, or learning benefit.

## Replay and limits

Run `cargo test -p ix-origami --test thickness` in IX at the pinned commit. The coordinator replayed all 11 thickness integration tests on 2026-10-21: 11 passed, 0 failed. The fixture README records the source and test blobs. The graph cards are hand-derived teaching data; no additional analyzer or consumer runtime is introduced. Passing those tests supports the described implementation cases, while subject accuracy, fluent translation, learner success, scene import, and anonymous Learn publication remain separate work.
