# SEM-004 source-bound review brief

Status: **open**. This is a review request, not a verdict. The frozen source table binds the EN/FR/ES sources, fixture, production/research records and learner handout. No source approval is claimed. Record reviewer identity or pseudonym and UTC date; later content changes require a diff review.


## Frozen source target

Demerzel source commit `6531ae9a0eb76f9402790f2b1b600c21330dfb66`. These are review targets, not approval receipts.

| Artifact path | Git blob |
|---|---|
| `state/streeling/courses/semiotics/en/sem-004-face-identity-under-reindexing.md` | `f7229fcc56d94a1b38bd972808bfe22caca9fe4f` |
| `state/streeling/courses/semiotics/fr/sem-004-face-identity-under-reindexing.fr.md` | `792249d85cdbbb85b03b56ae0a0d1020627863cb` |
| `state/streeling/courses/semiotics/es/sem-004-face-identity-under-reindexing.es.md` | `db7417bd91f9eed21decf0478d9d914ec4ebc08f` |
| `state/streeling/fixtures/semiotics/sem-004/scenarios.json` | `5962841857324ddda50845487da1586e2b187cad` |
| `state/streeling/fixtures/semiotics/sem-004/README.md` | `d53f945d9722dbc587dabd77bdef8d5481f09235` |
| `state/streeling/course-productions/cp-semiotics-2026-10-21-004.json` | `8053584474b6091c150ae65af779ccb54b892f58` |
| `state/streeling/research-cycles/semiotics-2026-10-21-004.json` | `94984ae7eaf8c070198fb54614ab8c25c507468b` |
| `state/streeling/reviews/sem-004-learner-task.md` | `6ee1f8bdfb4234cd236fd1d14bc729190ae32b55` |

## Evidence to challenge

1. Inspect IX commit `d7c22fdd6a62becb66b9d7246ea85850e7c55854`, `crates/ix-origami/src/controls.rs`, blob `29e73655fdbcb14e08c06520c9773950ce0b6407`. Confirm old-to-new map direction, out[perm[old]] placement, remapped vertices/edges/faces, cyclic face boundary rotation without winding reversal, random endpoint swaps, shuffled relation entries and preserved relative signs. Challenge any implied universal persistent identity claim.
2. Inspect the same revision's `tests/thickness.rs`, blob `3342419488ca7039d8a76e00366f26d5416234b9`. Reproduce the exact assertions for crane seeds 1–5, mapped per-face comparisons, tested rigid motion and aggregate-only turnover. Replay commands are in the fixture README. The coordinator reported the thickness target's 11 passing tests at that HEAD; this brief itself is not a test receipt.
3. Inspect `src/thickness.rs`, blob `43351fe867a83a10ab38113cb86db8633a0112f1`. Confirm optional `face_levels`, level-zero convention and one stack witness rather than unique material identity or a canonical assignment across every admissible stack.
4. Independently derive the synthetic table's inverse, both compositions, forward label/level placement, all mapped and wrong-direction comparisons, stale selection and transformed triple. Verify that the JSON expectations match those derivations. The fixture is neither measured IX output nor an executable geometry model.
5. Solve all five exercises before consulting their answers. Check pedagogical progression, 40-minute estimate and whether the Godot selection trial is falsifiable and clearly proposed. Compare FR/ES against English, especially old/new domains, winding, relative signs, witness versus canonical state, and turnover limits. Fluent-language review remains a separate real task.

## Learner and decision gates

Use `sem-004-learner-task.md` without lesson answer blocks. Preserve the raw response, actual time, prior experience, sources, confusion and any retest. Apply its five-dimension rubric independently; no successful attempt is pre-recorded. Ask a subject reviewer whether the correspondence analysis is correct and useful for future scene selections and cross-agent reports.

Record exact reviewed blobs, findings, scope and a real reviewer verdict. Keep production review and publish false until the required subject verdict, learner response, fluent-language review, Learn synchronization, deployment and anonymous exact-source public readback exist. PT/IT/DE are absent, so translation remains incomplete even though EN/FR/ES drafts exist. No Blender exporter, Godot adapter, renderer, runtime behavior or public content was produced by this package.
