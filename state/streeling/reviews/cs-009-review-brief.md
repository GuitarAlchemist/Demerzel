# CS-009 source-bound subject review

Status: open; no human verdict or learner attempt. The new course and fixture are not yet bound to a Demerzel commit here; the coordinator must record exact course, JSON and README blobs before review.

## Pinned implementation

IX commit `d7c22fdd6a62becb66b9d7246ea85850e7c55854`; implementation blob `43351fe867a83a10ab38113cb86db8633a0112f1`, test blob `3342419488ca7039d8a76e00366f26d5416234b9`. The root replay of `cargo test -p ix-origami --test thickness` passed 11/11 on 2026-10-21. Inspect the actual source, tests and ADR0007, not only that count.

## Claims to challenge

- Explain why unioning faces 0 and 1 turns the synthetic `0 -> 2 -> 1` chain into a panel cycle. Verify the pinned pierced-joint test's scope and direction of its witness pairs.
- Check the weave's successful base analysis alongside positive-thickness rigid refusal. In the cyclic zero-thickness case verify absent `rigid.height`, distinguishing it from zero `ply_height`.
- Derive the synthetic DAG's levels and the incomplete-order lower bound independently. These graph cards do not provide geometry and were not run through IX as FOLD inputs.
- Challenge whether exactness, absent witnesses and scope survive the proposed agent or scene handoff. Minimum-index panel labels and face-level witnesses are not universal persistent/canonical identities.
- Solve all five exercises without answers, and give the separate learner task to an independent learner. Retain raw responses and actual observed transfer behavior.

Record reviewer identity/pseudonym, UTC date, exact reviewed course blob, findings, independent computations, and `approved`, `changes_requested` or `not_assessed`. A static AI review may narrow work but cannot fill a human/learner field. Keep review/publish false until the actual gates are supported. No scene import or manufacturing proof follows from these graph tests; exact-source Learn generation/deployment/readback remains pending.
