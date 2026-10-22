# CS-009 bounded AI learner dry-run — raw first response

This is an AI learner dry-run, not a review approval or a human learning trial. I have general graph-theory prior competence, including equivalence classes, directed cycles, topological orders and longest paths in a DAG. I do not claim prior independent knowledge of the pinned IX thickness implementation.

UTC start: 2026-10-21T23:53:25.235Z
UTC end: 2026-10-21T23:54:39.507Z

Files read, in full:
- `C:\tmp\streeling-craft-dryrun-20261021-r1\cs-009\lesson.md`
- `C:\tmp\streeling-craft-dryrun-20261021-r1\cs-009\task.md`

Assistance: the supplied lesson and task, plus the coordinator's additional unseen transfer prompt. No other files, original courses, fixtures, answer keys, review briefs, other learner responses, memory or external sources were consulted. No implementation or test was executed. Pinned citations below are reproduced from the lesson and were not independently inspected.

Initial confidence: no genuine pre-lesson measurement was captured, because the lesson and task were read together. Retrospectively, my general graph-theory prior would already make me highly confident that local checks alone cannot establish a global rigid stack; that is a report of prior competence, not a measured learning gain.

The following is my first response, preserved without a later revision. It gives concise worked derivations and task answers.

## 1. Flat-joint composition

The flat joint makes faces 0 and 1 one panel. With the lesson's smallest-index representative convention, the panels are `{0,1}` represented by 0 and `{2}` represented by 2. The face-to-panel map is `[0,0,2]`.

The lower-to-upper face arcs `0 -> 2` and `2 -> 1` become panel arcs `0 -> 2` and `2 -> 0`. This is a directed cycle.

The face graph itself has the topological order `0,2,1`, but assigning three distinct heights would violate the required equality `h0 = h1`. For positive full thickness t, the panel constraints require `h2 >= h0 + t` and `h0 >= h2 + t`, which cannot both hold. Therefore distinct face heights do not solve the stated rigid-panel model.

If an adapter needs a permanent panel ID, it needs an explicit stable identity and remapping policy; the minimum face index is only a representative and can change after renumbering.

## 2. Cyclic weave at zero and positive thickness

The panel graph is cyclic at both thicknesses. The separate ply calculation uses `ply_height = ply * t`, with ply 2.

| Field | t = 0 | t = 0.5 |
|---|---:|---:|
| `ply_height` | 0 | 1 |
| `rigid.refused` | false | true |
| rigid `levels` | absent | absent |
| rigid `height` | absent | absent |
| rigid `face_levels` | absent | absent |

At zero thickness, `refused = false` does not supply a rigid placement. In the described implementation the cyclic graph still prevents a returned level/height witness. In particular, the zero `ply_height` must not be substituted for the absent rigid `height`. At positive thickness the cycle makes the parallel rigid-panel stack infeasible. Neither report provides a rigid face-level assignment.

## 3. DAG arithmetic, units and indices

Starting all levels at zero and applying the lower-to-upper constraints gives:

- P: 0
- Q: 0
- R: 1
- S: 2

The longest chain is P-R-S or Q-R-S and contains three panels. At full material thickness 0.2, the reported stack height is `3 * 0.2 = 0.6`.

The highest zero-based level is 2; the number of panels in that chain is 3. Multiplying the highest index by thickness would give 0.4 and omit one panel's full thickness. P and Q may share level zero under these stated abstract constraints; this does not establish that any particular geometry permits that placement.

Thickness and height use the crease pattern's coordinate units. The result is 0.6 of those units, not automatically 0.6 mm. A scene adapter needs an explicit unit conversion. These graph values are a witness under the stated constraints, not canonical levels for every valid arrangement.

## 4. Incomplete overlap order

The algorithm can report `max(chain, ply) = max(2,3) = 3` levels as a lower bound. It must preserve `levels_exact = false`, one undetermined overlapping pair, and absent `face_levels`.

Task 4 itself does not specify thickness. In general, the numerical height bound is `3 * t`. Using the lesson's associated incomplete-order card at t = 0.2 gives a height lower bound of 0.6 coordinate units. This is not a complete arrangement or a guarantee that a completion exists.

A scene must not use that bound to place every face as if an assignment had been returned. The missing order needs to be supplied or otherwise resolved and checked, and an actual assignment must be available before the scene claims to display a validated stack. Acyclic stated constraints alone do not settle the omitted relation.

## 5. Transfer correction and scene interaction

Corrected user-facing statement:

“The face-order graph is acyclic, but that alone does not establish a rigid stack. First preserve and apply the flat-joint face-to-panel map, then check the directed constraints between panels. A cycle after that composition rules out a stack at positive thickness under the parallel rigid-panel assumptions. An acyclic result must also retain missing-order information and any exactness flag. These checks do not establish physical manufacturability.”

One supporting pinned test, as described by the supplied lesson, is `a_weave_passes_the_layer_rules_but_has_no_rigid_stack` in [IX thickness integration tests at d7c22fdd6a62becb66b9d7246ea85850e7c55854](https://github.com/GuitarAlchemist/ix/blob/d7c22fdd6a62becb66b9d7246ea85850e7c55854/crates/ix-origami/tests/thickness.rs). The lesson reports that the base analysis passes while the positive-thickness rigid reading refuses. I have not inspected that source or replayed that test.

For the lesson's proposed asset statement, I would say:

“Base analysis passed. At positive material thickness, the rigid-panel reading refuses this stack because the lower-to-upper relations contain the cycle 0 -> 3 -> 2 -> 1 -> 0. This is a refusal under the parallel rigid-panel model; it does not determine whether another physical construction method is possible.”

A falsifiable downstream scene interaction: load one fixed source FOLD revision together with its face-to-object map, flat-joint panel map, thickness and unit conversion, base verdict, rigid verdict, cycle witness and exactness information. Ask a viewer to identify the closing lower-to-upper relation of the displayed cycle. On selecting each witness edge, the scene must highlight the corresponding mapped faces/panels and direction. For `0 -> 3 -> 2 -> 1 -> 0`, the viewer should be able to select `1 -> 0` as the closing edge when starting at 0 and following that sequence. A wrong mapping, reversed direction, missing edge, or fabricated successful placement fails the demonstration. The same task can be attempted with a plain directed graph diagram as a comparison; no advantage is assumed.

The next needed evidence is a working importer/adapter with verifiable mappings and report readback, followed by observed performance on that stated interaction. The lesson itself does not provide such an implementation or a learner trial.

## Additional unseen transfer

Input: faces 0, 1 and 2 are connected transitively by flat joints `0--1` and `1--2`; face 3 is separate. Lower-to-upper face arcs are `0 -> 3` and `3 -> 2`.

At face level the directed graph is acyclic: `0,3,2` is a valid ordering of the constrained faces, and face 1 is unconstrained by the directed arcs. A face-only assignment such as h0 = 0, h3 = t and h2 = 2t satisfies those two arcs for positive t, but violates the equality imposed by the flat joints.

After composing the flat-connected faces, the panels are `{0,1,2}` represented by 0 and `{3}` represented by 3. The map is `[0,0,0,3]`. The arcs become `panel 0 -> panel 3` and `panel 3 -> panel 0`, a two-panel cycle. Transitive flat connectivity is essential: faces 0 and 2 must share a height even without a direct flat joint between them.

For positive full thickness t, the quotient requires `h3 >= hA + t` and `hA >= h3 + t`, where A is `{0,1,2}`. These imply `hA >= hA + 2t`, which is impossible for t > 0. Thus there is no single-height parallel rigid-panel stack satisfying this input at positive thickness, under the lesson's model. The face DAG does not justify acceptance.

This does not prove physical manufacturing impossible. It does not evaluate tilted panels, changed creases, flexibility, alternative assembly, folding motion, material behavior or other construction methods. Nor do these abstract graph data supply geometry, a base-analysis result, local ply, or a scene export. I cannot infer those quantities from the transfer prompt.

## Experience, uncertainty and final confidence

The most consequential distinction is between a false refusal flag at zero thickness and an actual returned placement: the absent rigid fields must remain absent. A second consequential distinction is between a lower bound on levels and a face-level assignment.

Specific ambiguities or limits:

- Initial confidence was requested only after the materials had already been read; the retrospective statement above cannot establish learning gain.
- Task 4 omits thickness, so I stated a general expression and explicitly borrowed t = 0.2 only from the lesson's associated card.
- “Longest-path levels” are zero-based indices, while the reported level count and height use the panel count. Keeping those names distinct matters.
- The supplied lesson does not state numeric crane-test counts, so I cannot independently answer the lesson exercise's crane comparison numerically. Its general distinction is chain count versus local ply; the actual values require reading the pinned test, which this dry-run forbids.
- The pinned test claims and implementation behavior are lesson-supplied evidence, not independently verified evidence from this run.
- The additional transfer case has no geometry, so graph infeasibility under the specified model is the available conclusion; no broader physical conclusion follows.

Corrections: none made after the first response. Retest: none. No self-score is recorded, following the coordinator's explicit dry-run boundary despite the task sheet's scoring request. No review approval, human learning result, manufacturability result or practical transfer success is claimed.

Final confidence: high in the panel-composition and graph/arithmetic answers within the supplied model, supported by explicit maps, arcs, inequalities and unit accounting. Confidence in the stated IX behavior is conditional on the lesson being accurate because I did not inspect its citations or run code. Confidence in downstream scene behavior or human learning is unestablished because neither was observed.
