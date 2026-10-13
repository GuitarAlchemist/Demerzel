# PM-004 bounded review brief

Status: **open**. This packet is a request for human subject and learner review, not a verdict.

## Exact source under review

- Course: [`pm-004-craft-extension-release-decision.md`](https://github.com/GuitarAlchemist/Demerzel/blob/e92147807675155b77fe694ee94f1938842b10ae/state/streeling/courses/product-management/en/pm-004-craft-extension-release-decision.md) at Demerzel commit `e92147807675155b77fe694ee94f1938842b10ae`, Git blob `1ddd44e2695254cea1940e9b64c2a9677c18920e`.
- Fixture: `state/streeling/fixtures/product-management/pm-004/` at Demerzel commit `54e84c2c2060fc75977e469bf2a74e7cef18a4e4`.
- Pinned project source references: Demerzel `861b6b1891ef7017c22269d5ec6be4c50953040c` for CS-004, VC-005, and VC-007; GA `dc2e74cbd992a298f67efb928b5b3754615e1924` for the parked Godot plan; Learn `93d424f872a576ba8bbcd3dd44c9733292373654` for the GLB cleanup script and expected sample report.
- Production record: `state/streeling/course-productions/cp-product-management-2026-10-12-004.json`; review and publication flags are false. English is the only declared language.

If the course or fixture blobs change, inspect the diff and rerun the checks before extending a verdict.

## Subject and artifact checks

1. Reproduce the four fixture decisions with `python state/streeling/fixtures/product-management/pm-004/evaluate_release.py`. Inspect the JSON and script: a runtime Godot candidate with false meaning must be rejected; missing review must hold; even the all-pass synthetic card has no published tag. Challenge the evaluator with a missing target and a non-boolean gate; each should fail validation.
2. Check each source-linked statement at the pinned revision. In particular, CS-004's local GA bridge and load/save workflow must not be described as audio improvement; VC-005's checked-in Blender report must not become a craft-feature or Godot runtime verdict; VC-007's Python checker must not become an imported scene; the parked GA plan must remain a plan.
3. Check that the four per-target gate meanings are relevant to the stated user task, and that release candidacy cannot be read as a GitHub release. Ask whether independent target releases are safer or more useful than one bundle; record the actual user journey and contract replay needed for a bundled claim.
4. Solve all five course exercises without their answer blocks. Record any claim that lacks a source, any compatibility, license, accessibility, security, or installer omission that matters to release decision, and any target gate that needs a more precise observable oracle.

## Answer-free learner trial

Give [`pm-004-learner-task.md`](pm-004-learner-task.md) without this brief or the course answers. Preserve the unedited answers, target-app experience, time, consulted sources, and confusion. The transfer card is not one of the fixture's four cards. Expected sequence: reject the candidate while `godot.meaning=false` after a runtime trial; after that is repaired, hold for `blender.runtime=false`; after both are evidenced and the other booleans remain true, call it a release candidate, never an existing GitHub release because `published_tag=false`. Have the learner name a target-specific semantic test and one cross-tool hash handoff. Score five criteria from 0 to 2: evidence classification, hard-gate ordering, target-specific test, release/publication boundary, and reproducible handoff. A provisional 8/10 is only a trial rubric, not an observed learner outcome.

## Verdict boundary

Record reviewer identity or pseudonym, UTC date, exact integrated course blob, review scope, independently reproduced evidence, findings, and `approved`, `changes_requested`, or `not_assessed`. The draft exact-source receipt contract in Demerzel PR #1211 requires separate human schema review. Do not infer approval from this packet, AI feedback, or fixture output. Leave review and publish flags false until actual reviews, language checks, Learn build, deployment, and anonymous public readback are complete.
