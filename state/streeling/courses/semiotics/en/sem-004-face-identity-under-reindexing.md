---
module_id: sem-004-face-identity-under-reindexing
department: semiotics
course: "Face Identity under Reindexing"
level: intermediate
alchemical_stage: albedo
prerequisites: [sem-001-signs-in-governance]
estimated_duration: "40 minutes"
produced_by: codex-project-pilot
research_cycle: semiotics-2026-10-21-004
version: "0.1.0"
---

# Face Identity under Reindexing

> **Department of Semiotics** | Intermediate | 40 minutes | English draft awaiting review

## Objectives and project decision

A future scene viewer selects face 1 of an origami model. A second agent renumbers the model and reports that face 1 has changed level. Did the material move, did the order change, or did the same number start naming a different face? Answering that question requires interpreting the number before interpreting the geometry.

After this lesson, you can carry a selection through an explicit permutation, invert that mapping, distinguish face identity from level and orientation, and write a bounded cross-agent report. Allow eight minutes for the problem and signs, twelve for the table, ten for transformations, and ten for exercises and transfer. The artifact is a small correspondence table and a defensible handoff, rather than a new identity service.

The project evidence comes from IX commit `d7c22fdd6a62becb66b9d7246ea85850e7c55854`: [controls.rs](https://github.com/GuitarAlchemist/ix/blob/d7c22fdd6a62becb66b9d7246ea85850e7c55854/crates/ix-origami/src/controls.rs), [thickness tests](https://github.com/GuitarAlchemist/ix/blob/d7c22fdd6a62becb66b9d7246ea85850e7c55854/crates/ix-origami/tests/thickness.rs), and [thickness.rs](https://github.com/GuitarAlchemist/ix/blob/d7c22fdd6a62becb66b9d7246ea85850e7c55854/crates/ix-origami/src/thickness.rs). These links pin the inspected source, not the current branch. IX supplies checking and transformation controls here; this lesson demonstrates no Blender export, Godot import, renderer, or persistent selection implementation.

## 1. A face number is a contextual sign

In semiotics, a sign stands for an object under an interpretation. Here `1` is the sign, a particular material face is the intended object, and “look up slot 1 in this model revision” is the interpretation. An array **index** is a programming address within an ordered collection. It should not be confused with the broader semiotic term *index*, a sign connected to what it indicates. Neither use of the word gives the number permanent identity.

A report needs its model revision or transformation context. “Face 1” in the input and “face 1” in the output are two potentially different references. Shape, color, and current stack level may help a human recognize a face, but those properties can coincide across faces or change under a transformation. They do not establish provenance by themselves.

For this lesson, **material identity** means correspondence to the same input face through the particular controlled transformation. It does not solve arbitrary remeshing, splitting, merging, or reconstructing a model from an image. A provenance label such as classroom label A records the correspondence we supplied. Such labels are explicitly synthetic; the inspected IX `Permutation` is a mapping for a transformation, not a universal persistent-ID registry.

### Exercise 1 — Repair a reference

An agent says “Face 1 is wrong after renumbering.” What information is missing? Rewrite it as an inspectable question.

> **Answer:** The input/output model context, correspondence map, and property being compared are missing. A useful question is: “For the synthetic input face 1 (B), using old-to-new map `[2,0,3,1]`, does output face 0 retain input level 2?” This identifies the intended material and the exact comparison; it does not allege an IX defect.

## 2. Work the mapping in its declared direction

`Permutation` documents where each **old** index went. The helper `place` writes an old item into `out[perm[old]]`. Therefore `perm.faces[f]` takes an input face index and returns its output face index. It does not answer which input face now occupies an arbitrary output slot; that requires the inverse.

Use this explicitly **synthetic** four-face example, also recorded in the [fixture](../../../fixtures/semiotics/sem-004/scenarios.json). Its numbers are not crane results, a sampled seed, or a physical thickness experiment.

| Input index | Classroom provenance label | Input level | Output index `p[old]` |
|---:|---|---:|---:|
| 0 | A | 0 | 2 |
| 1 | B | 2 | 0 |
| 2 | C | 1 | 3 |
| 3 | D | 3 | 1 |

The forward map is `p = [2,0,3,1]`. Reading output slots from 0 to 3 gives labels `[B,D,A,C]` and levels `[2,3,0,1]`. The inverse is `q = [1,3,0,2]`: output slot 0 came from input slot 1, and output slot 1 came from input slot 3. Check both directions: `q[p[f]] = f` and `p[q[j]] = j`.

The correct property comparison is `new[p[f]] == old[f]`. For input B, it is `new[0] == old[1]`, so `2 == 2`. Comparing arrays directly produces inequality even though every material retains its value. Reusing the selected integer 1 instead highlights D, whose level is 3. This is a selection error without any corruption of the level calculation.

The inverse is equally useful when a user clicks output slot 3: it identifies input C at slot 2. Writing `new[q[f]]` in the forward comparison mixes domains. With our deliberately non-self-inverse map, input 0 would compare `new[1] = 3` against `old[0] = 0`. A swap-only example can conceal this bug because a swap equals its own inverse.

### Exercise 2 — Carry the selection

Move input selection C through the map. Then trace an output click on slot 1 back to the input. Would keeping integer 2 preserve the original C selection?

> **Answer:** C is input 2, so its output index is `p[2] = 3`, retaining level 1. Output 1 comes from `q[1] = 3`, label D. Keeping integer 2 would select A in the output. The map changes the address while preserving our stipulated material correspondence.

### Exercise 3 — Compare the right objects

Find the first mismatch in a raw comparison of `[0,2,1,3]` and `[2,3,0,1]`. State the four mapped comparisons and check one inverse equation.

> **Answer:** Raw slot 0 mismatches, `0 != 2`. The mapped checks are `new[2]=0`, `new[0]=2`, `new[3]=1`, and `new[1]=3`, matching input slots 0–3 respectively. For example, `q[p[2]] = q[3] = 2`. Raw inequality does not refute the claimed correspondence.

## 3. Preserve relations without confusing their signs

Renumbering also remaps vertices and edges. It rotates each face's vertex list cyclically, preserving its winding; it may swap an edge's endpoints; it shuffles the sequence of `faceOrders` entries. These are distinct operations. Rotating a triangular boundary `[0,1,2]` to `[1,2,0]` changes its starting point. Reversing it to `[0,2,1]` changes winding and is not that same operation. These tiny boundary lists illustrate order conventions, not extracted IX geometry.

In each `faceOrders` triple `[f,g,s]`, `renumber` substitutes `[p[f],p[g],s]` and retains the sign. Our synthetic triple `[1,3,1]` becomes `[0,1,1]`. The sign is interpreted relative to face normals; it should not be promoted to an unconditional global “above” badge without orientation. Shuffling the collection of relations also does not reverse every relation. A list position, an endpoint position, a boundary direction, and a layer-order sign carry different meanings.

In the pinned thickness test, `controls_leave_the_stack_unchanged` runs renumbering seeds 1–5 on the crane. It checks ply 28, rigid level count 36, and, for every input face, `new[perm.faces[f]] == old[f]`. This is concrete evidence for those controls on that fixture. It is not an exhaustive theorem for every fold or transformation.

`face_levels` is one stack witness respecting stated pairs, starting at level zero. The implementation can return no per-face levels when there is a cycle or insufficient order information. A level is therefore neither a unique material identifier nor a canonical description of every admissible stack. Two faces can share a level. Matching aggregate counts alone cannot tell a coordinator that a selection still points to its intended face.

### Exercise 4 — Separate three order operations

A reviewer treats a rotated face boundary, shuffled `faceOrders` entries, and a turned-over model as “array reordering.” Explain why that description loses relevant meaning. Map the synthetic triple `[1,3,1]`.

> **Answer:** Boundary rotation keeps cyclic winding; relation-list shuffling changes enumeration while preserving each relation; turning over changes orientation and the reading of up. They require different checks. The triple becomes `[0,1,1]`: its face references move through p and its relative sign is retained. This alone does not establish a global above relation.

## 4. State the transformation and its evidence boundary

`move_folded` rotates the folded frame in its plane and then translates it, keeping orientations. The pinned test uses angle 0.7 radians and shift `[3,-2]`, asserting equality of the entire returned stack with the baseline. That observation supports this tested rigid motion, not arbitrary scaling, deformation, or remeshing.

`turn_over` reflects folded y coordinates with `y -> -y`. Its documentation says orientations and up both flip, so `faceOrders`, relative to face normals, remain unchanged. The thickness test checks equal ply, ply height, rigid level count, and rigid height. It explicitly does **not** assert which face occupies which level. Reporting unchanged per-face levels after turnover would outrun the evidence. Material correspondence and vertical ordering are separate questions.

A useful handoff names source revision, transformation, mapping direction, selected input and output indices, compared property, and result. If correspondence is unavailable after an arbitrary regeneration, report identity unresolved. Identical aggregate thickness or a familiar silhouette cannot supply the missing mapping. This is a communication requirement for the proposed workflow, not an implemented IX selection protocol.

### Exercise 5 — Design a falsifiable selection trial

Propose a future Godot trial that could disprove correct selection retention after this synthetic renumbering. Include a turnover claim that the existing source does not justify.

> **Answer:** Before transformation, select B at input 1 and record its classroom provenance label, model revision, and map. After applying p, require the highlight and report to name output 0, B, level 2. A highlight on output 1/D falsifies retention even if total levels match. Record raw selection events and screenshots before and after; no trial has been run here. “B keeps the same level after turnover” is unsupported by the pinned aggregate-only turnover assertions.

The proposed trial needs an actual scene adapter and independent observation before anyone claims integration success. The present deliverables are source analysis, a synthetic table, and prepared learner tasks. Human subject review, a learner attempt, fluent-language review, and public publication remain open.
