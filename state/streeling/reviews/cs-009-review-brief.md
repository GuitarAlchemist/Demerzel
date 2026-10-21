# CS-009 source-bound subject review

Status: open; no human verdict or learner attempt. The frozen source table binds the course, fixture, records and learner task. Record reviewer, date and findings against those exact blobs.


## Frozen source target

Demerzel source commit `6531ae9a0eb76f9402790f2b1b600c21330dfb66`. These are review targets, not approval receipts.

| Artifact path | Git blob |
|---|---|
| `state/streeling/courses/computer-science/en/cs-009-composing-origami-panel-constraints.md` | `ce0c8f77db223f1a4a00966d536c585a956974b1` |
| `state/streeling/courses/computer-science/fr/cs-009-composing-origami-panel-constraints.fr.md` | `3ddb0c4bda020b37bdbd7c1250db28c23ea477ab` |
| `state/streeling/courses/computer-science/es/cs-009-composing-origami-panel-constraints.es.md` | `9d7e4a01778df2954ddb55d709f09140862b6002` |
| `state/streeling/fixtures/computer-science/cs-009/scenarios.json` | `1ec24ea50a199b85c1d48ea37880ae9191f4ed85` |
| `state/streeling/fixtures/computer-science/cs-009/README.md` | `f42417fe4e733efd8fbab2431dd6573b9d3f00bf` |
| `state/streeling/course-productions/cp-computer-science-2026-10-21-009.json` | `6e61185dd86cd9d6aa558d324d220b6c4540886a` |
| `state/streeling/research-cycles/computer-science-2026-10-21-009.json` | `fe5d53c2f6e54d564c7327a871c79738ffe9b88d` |
| `state/streeling/reviews/cs-009-learner-task.md` | `0db478482245debafa21addaebdfb8d34eaa3962` |

## Pinned implementation

IX commit `d7c22fdd6a62becb66b9d7246ea85850e7c55854`; implementation blob `43351fe867a83a10ab38113cb86db8633a0112f1`, test blob `3342419488ca7039d8a76e00366f26d5416234b9`. The root replay of `cargo test -p ix-origami --test thickness` passed 11/11 on 2026-10-21. Inspect the actual source, tests and ADR0007, not only that count.

## Claims to challenge

- Explain why unioning faces 0 and 1 turns the synthetic `0 -> 2 -> 1` chain into a panel cycle. Verify the pinned pierced-joint test's scope and direction of its witness pairs.
- Check the weave's successful base analysis alongside positive-thickness rigid refusal. In the cyclic zero-thickness case verify absent `rigid.height`, distinguishing it from zero `ply_height`.
- Derive the synthetic DAG's levels and the incomplete-order lower bound independently. These graph cards do not provide geometry and were not run through IX as FOLD inputs.
- Challenge whether exactness, absent witnesses and scope survive the proposed agent or scene handoff. Minimum-index panel labels and face-level witnesses are not universal persistent/canonical identities.
- Solve all five exercises without answers, and give the separate learner task to an independent learner. Retain raw responses and actual observed transfer behavior.

Record reviewer identity/pseudonym, UTC date, exact reviewed course blob, findings, independent computations, and `approved`, `changes_requested` or `not_assessed`. A static AI review may narrow work but cannot fill a human/learner field. Keep review/publish false until the actual gates are supported. No scene import or manufacturing proof follows from these graph tests; exact-source Learn generation/deployment/readback remains pending.
