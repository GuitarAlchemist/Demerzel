# INF-003 bounded review brief

Status: **open**. This packet requests human IX/information-theory subject review, fluent-language checks, and a learner trial. It is not an IX batch result or a publication receipt.

## Frozen source set

At Demerzel commit `f339e8b551414de8750945a55c15181096c6abf7`, [`inf-003-verdict-distribution-drift.md`](https://github.com/GuitarAlchemist/Demerzel/blob/f339e8b551414de8750945a55c15181096c6abf7/state/streeling/courses/information-theory/en/inf-003-verdict-distribution-drift.md) and its five localizations have these Git blobs:

| Locale | Git blob |
|---|---|
| EN | `67a4861000a74c1889f3782018a7447f5bfc5b18` |
| ES | `efe1b0c2ede9bdad2810a6d16feb8c16a0fffd7b` |
| PT | `ca9623bc15639bdae2655fe78551c2a7cbeef000` |
| FR | `2e65b476632af280e5af85a512e5519d5dfd5000` |
| IT | `04976f17eca42220605a11bb7793652313f31ae8` |
| DE | `08315488958eae4e8b35194953342923b1301db6` |

The production record is `state/streeling/course-productions/cp-information-theory-2026-10-11-003.json`, with review and publish false. The [independent AI subject and translation preflight](inf-003-subject-preflight-2026-10-11.md) reported a corrected witness-cap precision issue and no remaining static finding in its scope; it is not human approval. A changed source blob needs new diff review.

## Subject and method review

1. Read the pinned IX `ix-petri/src/analysis.rs` and `ix-math/src/inference.rs` at `bd1336b7c4045e427dcdbe80b102790e45da5ce1`. Confirm `holds`, `fails`, and `unknown` retain different meanings for the **same** `deadlock_free` property and that the lesson does not pool unrelated properties or treat `unknown` as a pass. Check the deadlock witness cap: `Fails` can occur with no serialized witness when `max_reported_deadlocks=0`.
2. Recompute the **synthetic** ten-net fixture: baseline `[8,0,2]`, candidate `[6,2,2]`, normalized `p=[0.8,0,0.2]`, `q=[0.6,0.2,0.2]`, and midpoint `[0.7,0.1,0.2]`. `KL(p||q)=0.23014565796142483` nats; reverse KL has a positive candidate-fails entry against baseline zero and errors in IX. `JS(p,q)=0.07648207115762617` nats, symmetric and finite. Check natural-log units and the stated `ln(2)` bound.
3. Challenge the operational inference. A divergence over category counts loses net identity and batch size; `[80,0,20]` versus `[8,0,2]` normalizes identically. Confirm that the proposed `0.05`-nat threshold is invented and can only trigger investigation, not prove regression. Check fixed analyzer revision, property, limits, category order, paired net IDs, truncation reason, and witnesses before accepting a changed-verdict claim.
4. Attempt all five course exercises before reading their answers. Inspect any paraphrase of the IX math function for unsafe assumptions about positive infinity; the lesson requires finite counts in its protocol.

## Language and learner review

Ask fluent reviewers to compare each localization with the pinned EN blob, especially `[holds,fails,unknown]` order, `0.23014565796142483` and `0.07648207115762617` **nats**, KL direction, JS symmetry, witness-cap caveat, and synthetic limits. AI parity triage is not fluent-language approval.

Give [`inf-003-learner-task.md`](inf-003-learner-task.md) without this brief or course answer blocks. Record math/IX background, elapsed time, unedited response, confusion, and revision/retest. The transfer table uses eight invented nets per row: `p=[0.75,0.25,0]`, `q=[0.5,0.25,0.25]`, midpoint `[0.625,0.25,0.125]`. `KL(q||p)` encounters candidate `unknown=0.25` against baseline zero. JS is `0.09922809353917371` nats; an invented `0.08`-nat rule would request inspection only. Score five criteria 0–2: (1) aligned vectors and midpoint; (2) KL support/direction; (3) JS calculation and units; (4) no regression inference from histogram alone; (5) paired net/limit/witness follow-up. Provisional pass: at least 8/10, to revisit after an actual trial. No learner result exists.

## Verdict and publication boundary

Record reviewer identifier or pseudonym, UTC date, exact locale blob, review kind (`subject`, `language`, or `learner`), evidence, findings, and `approved`, `changes_requested`, or `not_assessed`. The draft exact-source receipt contract in Demerzel PR #1211 has a separate human schema gate. This brief cannot issue a receipt.

Keep review and publish false until real verdicts and learner evidence exist. After accepted source integration, import Learn and anonymously read back the intended pages and source revision. A local generated page is not public publication.
