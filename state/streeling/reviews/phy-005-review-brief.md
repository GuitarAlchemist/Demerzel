# PHY-005 exact-source review brief

Status: **open review request**. Subject approval, fluent-language approval, learner evidence, and publication readback do not exist for this package. This brief does not issue a review receipt.


## Frozen source target

Demerzel source commit `6531ae9a0eb76f9402790f2b1b600c21330dfb66`. These are review targets, not approval receipts.

| Artifact path | Git blob |
|---|---|
| `state/streeling/courses/physics/en/phy-005-sheet-thickness-and-scene-units.md` | `24704663e5178e05c404c69207c8459de2282f4e` |
| `state/streeling/courses/physics/fr/phy-005-sheet-thickness-and-scene-units.fr.md` | `c4e31e22b9f60aceb325b7a066a8152edbe2248c` |
| `state/streeling/courses/physics/es/phy-005-sheet-thickness-and-scene-units.es.md` | `dd187dee0a0506312bc2f447eb801e7c46d273cf` |
| `state/streeling/fixtures/physics/phy-005/scenarios.json` | `5b27b9674aef8e09461f250cc624cf6c7c703f3d` |
| `state/streeling/fixtures/physics/phy-005/README.md` | `c2a0a97248483e3961499cd7ea5141befd6ec6cb` |
| `state/streeling/course-productions/cp-physics-2026-10-21-005.json` | `bea3e53acc859478999819a435821f196d6284e7` |
| `state/streeling/research-cycles/physics-2026-10-21-005.json` | `e279e0a41b78d3383301157e1a3ae702830c54b3` |
| `state/streeling/reviews/phy-005-learner-task.md` | `b2911d3f0b5e8ba74f1ca8d35aa28a2212fe45e9` |

## Review identity

The frozen source table binds the integrated Demerzel commit and locale blobs. Record the full commit, exact path, locale blob, reviewer identifier/pseudonym, UTC time, review kind, findings, and verdict. A subsequent content edit requires explicit review of the changed blob.

Intended source files:

- `state/streeling/courses/physics/en/phy-005-sheet-thickness-and-scene-units.md`
- `state/streeling/courses/physics/fr/phy-005-sheet-thickness-and-scene-units.fr.md`
- `state/streeling/courses/physics/es/phy-005-sheet-thickness-and-scene-units.es.md`

The production record is `state/streeling/course-productions/cp-physics-2026-10-21-005.json`; its translation, review, and publish completion flags are false. PT/IT/DE remain absent. The [fixture README](../fixtures/physics/phy-005/README.md) gives exact source commands and verification limits.

## Subject review

Inspect IX commit `d7c22fdd6a62becb66b9d7246ea85850e7c55854`: [lib.rs](https://github.com/GuitarAlchemist/ix/blob/d7c22fdd6a62becb66b9d7246ea85850e7c55854/crates/ix-origami/src/lib.rs), [thickness.rs](https://github.com/GuitarAlchemist/ix/blob/d7c22fdd6a62becb66b9d7246ea85850e7c55854/crates/ix-origami/src/thickness.rs), and [existing tests](https://github.com/GuitarAlchemist/ix/blob/d7c22fdd6a62becb66b9d7246ea85850e7c55854/crates/ix-origami/tests/thickness.rs). Verify the following independently:

1. Full thickness is in crease-pattern units. `stack` multiplies caller-provided `t` by the dimensionless counts. Powers-of-two normalization supports absolute tolerances and supplies no measured length or scene-unit declaration.
2. For the stated 150 mm unit-square crane with 0.4 mm stock, the existing test asserts `ply=28`, exact `levels=36`, 59 face-level entries, and no undetermined pairs. Derived heights are `28×0.4=11.2 mm` and `36×0.4=14.4 mm`, with corresponding coordinate heights `0.0746666667` and `0.096`.
3. `heights_scale_with_the_thickness` compares 0.25 and 0.5, doubles heights, and leaves face levels unchanged. Those values test algebra, not material measurement. The coordinating agent reported `cargo test -p ix-origami --test thickness` at unchanged pinned HEAD: 11 passed, 0 failed, reported 2026-10-21T20:47:52Z. This is a focused existing-target replay, not the full suite.
4. Recompute all six JSON cases. Distinguish changing stock, sheet width, all physical lengths, coordinate encoding, and proposed scene scale. For `u=1`, the reference width/thickness/rigid extent in scene units are `0.15/0.0004/0.0144`. The deliberate wrong inputs introduce factors 150 and 1000. A coordinate thickness alone cannot identify the physical stock.
5. Review the illustrative lower-surface convention carefully: 36 levels have base indices 0–35; level 35 begins at `35t`, and the last slab ends at `36t`. This is proposed placement, not an IX mesh. `face_levels` is one order-respecting assignment, not canonical placement evidence.
6. Challenge the model boundary: a positive-thickness cycle refuses the parallel-panel interpretation; a missing cyclic height is not zero. Incomplete order yields a lower bound and no face-level assignment. Neither local flat-state checks nor an exact parallel-panel height proves a motion path, thick-sheet feasibility, engine import, or DLSS support.

## Language and learning review

Fluent FR and ES reviewers should compare the full explanation and all five answered exercises with the bound EN blob. Preserve the distinct 28/36 readings, 150/1000 mistakes, full-versus-half thickness, coordinate/physical/scene mapping, 35t/36t extent, zero-versus-absent height, lower-bound qualification, and proposed integration status. All locale copies are drafts; AI parity inspection cannot supply human or native-language approval.

Give the [separate transfer task](phy-005-learner-task.md) without answer blocks. Retain an unedited response, prior knowledge, elapsed time, requested help, confusion, corrections, and any later retest. Reviewer key for its new scenario:

- Ruler `a=200/2=100 mm/cp`; thickness `0.006 cp=0.6 mm=0.006 scene units` with `u=10`. Ply extent `0.168 cp=16.8 mm=0.168 scene units`; rigid extent `0.216 cp=21.6 mm=0.216 scene units`. Sheet width is 2 scene units. Independent rigid paths: `36×0.006×100×10/1000` and `36×0.6×10/1000` both yield 0.216.
- Mistaken `0.6 cp` means 60 mm stock, 100 times too thick. Repair to `0.006 cp`.
- Illustrative lower surface of level 35 is 21 mm or 0.21 scene units; full extent is 21.6 mm or 0.216 scene units. These placements are not exports.
- At 400 mm width and unchanged 0.6 mm stock, `a=200`, `t_cp=0.003`, coordinate heights halve to 0.084/0.108, while physical extents stay 16.8/21.6 mm. Doubling physical width and stock to 1.2 mm preserves initial coordinate thickness/heights and doubles physical extents to 33.6/43.2 mm.
- A valid handoff identifies source evidence separately from assumed dimensions and proposed scene settings, rejects normalization as physical measurement, preserves absent-versus-zero height, and limits claims to this model.

Score five criteria 0–2: unit ruler and complete conversion table; wrong-input diagnosis; offset/extent distinction; both resizing interpretations; evidence and model boundaries. Provisional pass is at least 8/10 with no uncorrected factor-of-1000 error. This rubric is proposed and has not been calibrated through a learner trial. One learner's success would show bounded transfer, not population-wide educational effectiveness.

## Publication boundary

Keep review and publish false until actual applicable human review and learner evidence exist. Bind accepted source before Learn synchronization; anonymously read back intended pages and exact source links after publication. Neither a local draft nor this review request establishes public access. A changed blob requires renewed review scope.
