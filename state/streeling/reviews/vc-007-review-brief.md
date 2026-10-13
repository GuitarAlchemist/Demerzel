# VC-007 bounded review brief

Status: **open**. This packet requests subject, Godot-scene, and learner review; it is not an approval receipt.

## Frozen target and evidence

- English course: [`vc-007-weave-seams-as-scene-contracts.md`](https://github.com/GuitarAlchemist/Demerzel/blob/250209a3257f138f7096511e4e86cab234cb20a5/state/streeling/courses/visual-computing/en/vc-007-weave-seams-as-scene-contracts.md), Demerzel commit `250209a3257f138f7096511e4e86cab234cb20a5`, Git blob `a231700a0f08877759f35367ae4d68fcc3f291b9`.
- Synthetic input and evaluator: `state/streeling/fixtures/visual-computing/vc-007/` at Demerzel commit `f23ccae6c049d9066a1be2221c68f3b0bcf48373`.
- Production record: `state/streeling/course-productions/cp-visual-computing-2026-10-12-007.json`. Review and publish flags remain false; English is the only declared language.

A later course edit changes its blob. Inspect that diff before extending a verdict.

## Subject and implementation review

1. Run `python state/streeling/fixtures/visual-computing/vc-007/evaluate_weave.py`. Confirm 6-by-6, 36 unique crossing IDs per variant, 0 global-parity adjacency violations, and 12 restarted-tile violations. Confirm the first seam pair is `w2-f0` to `w3-f0`. Challenge the evaluator with a changed odd/even base and with diameter at least spacing; record whether the stated invariant and rejection behavior still hold.
2. Check that the course presents `(x+y+phase)%2` as a *declared teaching model*, not a general description of textile practice. Review the distinction between 12 broken adjacency relations, crossing count, and damaged mesh pixels. Inspect the claimed six horizontal and six vertical seam relations.
3. Confirm that the pinned GA Godot plan is only a proposed scene path. A future renderer test must preserve crossing IDs, source hash, over/under values, coordinate convention, and a replayable click mapping. No local Python result constitutes a Godot import or a visual quality result.
4. Challenge the proposed acceptance gate against a 2D labeled-grid baseline. Ask whether a JSON manifest and small validator would serve as well as a new DSL. Record accessibility, real-world weaving, geometry, and scene-cost omissions as findings if the wording overstates them.
5. Solve all five course exercises before reading their answer blocks. Quote the exact section and source blob for any incorrect answer or misleading claim.

## Answer-free learner trial

Give [`vc-007-learner-task.md`](vc-007-learner-task.md) without this brief or the course answers. Preserve unedited answers, relevant programming/textile/Godot background, elapsed time, and confusion. A reviewer can also ask the learner to run the pinned evaluator, then explain why it does not prove scene correctness.

The transfer case uses a 3-by-2 base repeated twice in each direction: 6 by 4 gives 24 crossings. Global parity has zero adjacency violations. Restarting local parity at each tile yields four horizontal seam violations at the `w2`/`w3` boundary, one per row, and zero vertical seam violations because the base height is even. Score five criteria from 0 to 2: (1) dimensions and counts; (2) correct seam diagnosis; (3) stable ID and manifest reasoning; (4) separation of semantic, geometry, and perception gates; (5) an explicit 2D baseline and rejection rule. A provisional pass is 8/10; revise it after an actual trial. These are answer-key expectations, not observed learner results.

## Verdict and publication boundary

Record reviewer identifier or pseudonym, UTC date, exact course blob, review kind, evidence, findings, and `approved`, `changes_requested`, or `not_assessed`. The exact-source receipt contract in Demerzel PR #1211 still needs human schema review. Do not infer approval from this packet.

Keep review and publish flags false until actual verdicts and learner evidence are recorded. After source integration, sync Learn from an accepted full commit and anonymously read back the public page at that source. A local preview is not publication.
