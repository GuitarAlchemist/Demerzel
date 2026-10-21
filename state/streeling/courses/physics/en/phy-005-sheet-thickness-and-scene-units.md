---
module_id: phy-005-sheet-thickness-and-scene-units
department: physics
course: Sheet Thickness from IX Coordinates to Proposed Scene Units
level: intermediate
prerequisites: [basic-ratios, dimensional-analysis]
estimated_duration: "40 minutes"
produced_by: codex-project-pilot
research_cycle: physics-2026-10-21-005
version: "0.1.0"
---

# Sheet Thickness from IX Coordinates to Proposed Scene Units

> **Physics department** | 40 minutes | EN draft; subject and learner review pending. FR/ES are translation drafts; PT/IT/DE are absent.

## Objectives and project problem

An IX sheet can have coordinates between zero and one while its material thickness is measured in millimetres. A proposed Blender or Godot artifact needs another declared length scale. Carrying the bare number `0.4` through all three representations would turn ordinary paperboard into a sheet 150 times too thick, or turn millimetres into scene metres with a factor-of-1000 error.

After this lesson, you can derive thickness and stack heights in each representation, distinguish ply from parallel-panel levels, diagnose two scaling mistakes, and write an evidence-bounded handoff. Spend about 12 minutes reading the derivations, 18 minutes doing the exercises before revealing their answers, and 10 minutes preparing the transfer task. This lesson concerns geometric length and unit conversion. Guitar excitation velocity belongs to PHY-004; reconstruction of a fold state belongs to the visual-computing sequence.

Our source boundary is IX commit `d7c22fdd6a62becb66b9d7246ea85850e7c55854`: [`thickness.rs`](https://github.com/GuitarAlchemist/ix/blob/d7c22fdd6a62becb66b9d7246ea85850e7c55854/crates/ix-origami/src/thickness.rs), its [existing tests](https://github.com/GuitarAlchemist/ix/blob/d7c22fdd6a62becb66b9d7246ea85850e7c55854/crates/ix-origami/tests/thickness.rs), and [`lib.rs`](https://github.com/GuitarAlchemist/ix/blob/d7c22fdd6a62becb66b9d7246ea85850e7c55854/crates/ix-origami/src/lib.rs). We inspected those definitions and assertions. The coordinating agent ran the focused thickness test target at unchanged pinned IX HEAD: 11 passed, 0 failed; this is not an entire-suite result. The [arithmetic fixture](../../../fixtures/physics/phy-005/scenarios.json) supplies modeled examples, with reproduction instructions in its [README](../../../fixtures/physics/phy-005/README.md).

## 1. Declare a ruler before converting a coordinate

Let `C` be the sheet width expressed in crease-pattern coordinate units, `W` its assumed physical width in mm, and `h` the full material thickness in mm. Define `a=W/C`, in mm per coordinate unit. Then:

```text
x_mm = x_cp × a
t_cp = h/a = h × C/W
H_mm = H_cp × a
```

The subscript identifies a representation; it does not claim IX stores physical metadata. The width `W` is an external assumption supplied for this worked example. A unit-square file alone does not tell us whether the real sheet is 150 mm or 300 mm wide. Thickness is the full thickness, not a half-thickness or a face count.

The crane test explicitly describes 0.4 mm paperboard on a 150 mm sheet whose crease pattern is the unit square. Therefore `C=1`, `W=150`, `a=150`, and `t_cp=0.4/150=0.0026666667`. Checking the round trip gives `0.0026666667 × 150 ≈ 0.4 mm`. Keep the fraction until the final display to avoid rounding drift.

`lib.rs` describes rescaling coordinates by powers of two before absolute-tolerance checks: the crease pattern becomes between one and two across. That is numerical conditioning. It is neither a declaration of metres nor a measurement of the sheet. `stack(ctx,t)` uses the caller's `t` unchanged in its reported multiplications; it cannot infer `W` or silently convert a supplied `0.4 mm`. Keep an explicit external mapping for the coordinate representation you intend to carry onward.

### Practice exercise 1: repair the thickness input

A handoff for the test's unit-square crane labels `t=0.4` as “0.4 mm.” Calculate the required `t_cp`, the physical thickness represented by the mistaken value, and the error factor.

> **Answer:** `t_cp=0.4/150=0.0026666667`. With `a=150 mm/cp`, the mistaken `0.4 cp` means `60 mm`. Its ratio to the intended thickness is `60/0.4=150`. Replace the number and state the mapping; relabeling the existing number does not perform a conversion.

## 2. Keep the two stack readings separate

The implementation computes `ply` as the maximum number of faces in an overlay cell. Its height is `ply_height=ply × t`. This reading allows a face to occupy different heights in different cells, as a draping sheet could. It is a lower bound for stacks retaining the stated planar positions.

For parallel rigid panels, faces connected by flat joints share a panel. A directed edge connects a lower panel to an upper panel for a stated overlapping pair. With an acyclic order and all overlapping panel pairs determined, `levels` is the longest chain and `height=levels × t` is the least height under this restricted interpretation. With missing orders, the reported level count is a lower bound; `levels_exact=false` and `face_levels` is absent. A count is dimensionless, while a height carries the same units as `t`.

The existing crane test asserts `ply=28`, exact rigid `levels=36`, no undetermined pairs, and 59 face-level entries respecting the stated order. It supplies a chain of 36 faces. These are assertions about that fixture and interpretation, not a universal crane specification. Apply both formulas:

```text
ply height:   28 × (0.4/150) = 0.0746666667 cp = 11.2 mm
rigid height: 36 × (0.4/150) = 0.096 cp        = 14.4 mm
```

An illustrative placement using lower surfaces `z_k=k×t` has its highest lower surface at `35t` for 36 occupied levels. The top of that last slab is `36t`. This explains the difference between a surface offset and full stack extent; it is a proposed drawing convention, not exported IX geometry.

### Practice exercise 2: distinguish offset from extent

The scene brief says “crane thickness is 28 layers, so the rigid stack is 11.2 mm; the highest rigid level is 35, so its height is 35t.” Correct both statements using the test's assumptions.

> **Answer:** The 28-ply reading gives 11.2 mm. The parallel rigid reading has 36 exact levels and full extent `36×0.4=14.4 mm`. Under the proposed lower-surface convention, level 35 starts at `35×0.4=14.0 mm` and ends at 14.4 mm. An integer level index is not the count of occupied levels.

## 3. Derive a future scene scale explicitly

Suppose a future artifact chooses `u=1 scene unit per metre`. This is a teaching choice, not a verified Blender or Godot configuration. The conversion is `b=u/1000` scene units per mm, hence `x_scene=x_cp×a×b`. Apply the same multiplier to every length that belongs to the same geometry, including thickness and computed heights.

For the reference sheet, one coordinate unit maps to `150/1000=0.15` scene units. Thus `t_scene=(0.4/150)×0.15=0.0004`, the ply height is `0.0112`, and the rigid height is `0.0144`. The independent physical path gives `14.4 mm × (1/1000)=0.0144 scene units`. Agreement between the paths checks the arithmetic, not an import pipeline.

If a separate pedagogical preview instead chooses `u=100 scene units per metre`, every scene length becomes 100 times larger. The sheet width becomes 15 scene units and the rigid height becomes 1.44. Physical thickness remains 0.4 mm. A scale choice changes the representation, not the material.

### Practice exercise 3: find a factor-of-1000 mistake

A proposed metre-scale scene uses sheet width `0.15`, thickness `0.4`, and rigid height `14.4`. Calculate the correct two smaller lengths and show a ratio that detects the mismatch without depending on the scene scale.

> **Answer:** Thickness should be `0.0004` and rigid height `0.0144` scene units. Both supplied values are 1000 times too large. The correct ratios are `thickness/width=0.4/150≈0.0026666667` and `rigid height/width=14.4/150=0.096`. The erroneous scene has ratios about 2.6667 and 96. A consistent uniform scale preserves these dimensionless ratios.

## 4. Change one assumption at a time

Changing material and resizing geometry answer different questions. On the same 150 mm sheet, doubling thickness to 0.8 mm doubles `t_cp`, both heights, and their scene lengths. It does not change the input's face order. The existing `heights_scale_with_the_thickness` test compares `t=0.25` and `0.5`, asserts doubled heights, and asserts unchanged face levels. Those numbers test algebra; they are not measurements of paperboard.

Keeping 0.4 mm stock but using a 300 mm sheet halves `t_cp` for a unit-square representation. The physical heights remain 11.2 and 14.4 mm for the same stated combinatorial configuration. Conversely, doubling every physical length, including stock thickness, preserves `t_cp` and doubles physical heights. State which of these transformations you mean by “scale up.”

Re-encoding the same 150 mm sheet with `C=2` gives `a=75 mm/cp` and `t_cp=0.0053333333`; the rigid height becomes `0.192 cp`. Multiplying by 75 restores 14.4 mm. This is a dimensional derivation for a consistently re-encoded representation, not a new observed IX run.

### Practice exercise 4: compare three edits

Starting from the reference, calculate `t_cp` and rigid height in mm for: A, thickness 0.8 mm at width 150 mm and `C=1`; B, thickness 0.4 mm at width 300 mm and `C=1`; C, the original physical sheet represented with `C=2`. Assume the same exact 36-level order.

> **Answer:** A: `t_cp=0.8/150≈0.0053333333`, height `36×0.8=28.8 mm`. B: `t_cp=0.4/300≈0.0013333333`, height 14.4 mm. C: `t_cp=0.4×2/150≈0.0053333333`, height 14.4 mm. A and C share a coordinate thickness but describe different physical assumptions. Coordinate values require their ruler.

## 5. State what a converted height establishes

The checker reads one stated flat folded state. `lib.rs` says its local checks do not prove global flat-foldability and do not compute a layer order. `thickness.rs` restricts its rigid interpretation to parallel panels, each at one height. A cycle refuses that interpretation for positive `t`; at zero thickness it is reported without refusal. A missing rigid height in a cycle is not a measured zero.

Even an exact acyclic height does not prove a physically realizable thick fold: actual hinges, contact, bending, and a motion path are outside this calculation. The source explicitly notes that tilted boards may escape a parallel-panel refusal and that exact thick crease contact raises another limitation. This course produces no exporter, mesh, collider, dynamic fold simulation, material test, or live Blender/Godot/DLSS integration.

### Practice exercise 5: write the handoff claim

Write three sentences for a future visual-artifact author using the reference result: one about evidence, one about the scene mapping, and one about an unresolved physical or integration claim.

> **Answer:** “At pinned IX commit `d7c22fdd6a62becb66b9d7246ea85850e7c55854`, inspected crane-test assertions specify 28 plies and 36 exact parallel-panel levels for `t=0.4/150`; the coordinator also reports 11 focused thickness tests passed at that unchanged revision. Assuming a 150 mm sheet and one scene unit per metre, derived ply and rigid extents are 0.0112 and 0.0144 scene units. These conversions establish neither physical foldability nor a working Blender/Godot import.” Include the fixture link when transferring this claim.

## Transfer and review

Complete the separate [answer-free learner task](../../../reviews/phy-005-learner-task.md) with a new physical width and scene scale. A reviewer should inspect the pinned source, recompute conversions, and check language parity through the [review brief](../../../reviews/phy-005-review-brief.md). No learner attempt, fluent-language approval, or publication readback is recorded. The finished artifact here is a draft lesson and arithmetic packet; its proposed benefit remains testable through a real learner's unassisted transfer.
