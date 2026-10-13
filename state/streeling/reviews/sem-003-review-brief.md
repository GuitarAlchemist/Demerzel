# SEM-003 bounded review brief

Status: **open**. This packet requests human semiotics/agent-governance subject review, fluent-language checks, and a learner trial. It is not an approval receipt or proof that evidence-scoped handoffs improve coordination.

## Frozen source set

At Demerzel commit `f339e8b551414de8750945a55c15181096c6abf7`, [`sem-003-status-signs-and-evidence.md`](https://github.com/GuitarAlchemist/Demerzel/blob/f339e8b551414de8750945a55c15181096c6abf7/state/streeling/courses/semiotics/en/sem-003-status-signs-and-evidence.md) and its five localizations have these Git blobs:

| Locale | Git blob |
|---|---|
| EN | `40ed2d23a61ec34ba3d2ab2fff6765daed2f9b12` |
| ES | `034981fd4f4284e04e42f3d55ecb104e58c0ef0f` |
| PT | `4a876240b846417d05c36a012dcca4d04579744a` |
| FR | `3955b49d77101e234201b21dfb1a4e144f9fab64` |
| IT | `186af8a9eef0c7b0a20743cca14f6538a4e4eb5c` |
| DE | `0391ec537f71512e372903f20a7752491cb6577e` |

The production record is `state/streeling/course-productions/cp-semiotics-2026-10-12-003.json`, with review and publish false. The [independent AI subject and translation preflight](sem-003-subject-preflight-2026-10-12.md) corrected an overstrong research conclusion and reported no remaining static finding in its stated scope; it is not human approval. A later edit changes the target blob and needs explicit diff review.

## Subject and method review

1. Inspect the pinned SEM-002 production record, bounded AI source-review note, production schema, progress reporter, preflight, and dated public baseline at Demerzel `c453a91d1c4d913af72c28779eff826659c1d654`. Check that the course accurately separates a **sign** (status word or badge) from its object (specific event, source, verdict, or public route).
2. Confirm that `draft`, `ready`, `reviewed`, and `published` in the lesson are communication claims, not invented enum states. The pinned production schema permits `in_progress`, `review_pending`, `published`, `rejected`, and `failed`. A bounded AI “no findings” note may coexist with `review.completed=false`; neither authenticates a human verdict.
3. Challenge the synthetic `status: published` with `publish.completed: false` example against the pinned schema and preflight. The course claims the schema lacks a cross-field implication and the preflight's relevant status rule applies only to `in_progress`. The example is not a claim that a contradictory record was committed or that a public page exists.
4. Revisit the dated DV-001 local generation versus anonymous 404. A locally generated page and a failed public GET describe different surfaces at that observation time. A future 200 response still needs a matching content/source revision. Do not transfer that historical 404 into a current SEM-003 site claim without a fresh readback.
5. Attempt all five exercises before reading their answers. Look for an unsupported promotion from source existence or schema pass to “reviewed” or “published,” and for any claim that the proposed evidence-chain handoff has already improved human/agent behavior. A controlled handoff/learner test remains unrun.

## Language and learner review

Ask fluent reviewers to compare each locale with the pinned EN blob, especially status enum names, the `in_progress` record, the AI preflight's narrow scope, the synthetic published/false contradiction, and the dated 404. AI semantic parity is not fluent approval.

Give [`sem-003-learner-task.md`](sem-003-learner-task.md) without this brief or the course answers. Record prior experience with release and agent handoffs, elapsed time, unedited response, confusion, and revision/retest. The transfer case has an English source at revision `A`, a bounded automated check, a local page, an anonymous 404, no human receipt, and `review.completed=false`/`publish.completed=false`; a later edit produces revision `B`. A defensible message names the draft and bounded check at A, rejects “human reviewed” and “public,” and requests checking B before carrying the old check forward. Score five criteria 0–2: (1) status referents and precise words; (2) bounded check versus human review; (3) local versus anonymous public evidence; (4) stale source revision handling; (5) actionable handoff with missing gates. Provisional pass: at least 8/10, to revisit after an actual learner trial. No learner result exists.

## Verdict and publication boundary

Record reviewer identifier or pseudonym, UTC date, exact locale blob, review kind (`subject`, `language`, or `learner`), evidence, findings, and `approved`, `changes_requested`, or `not_assessed`. The draft exact-source receipt contract in Demerzel PR #1211 has a separate human schema gate. This packet cannot issue a receipt.

Keep review and publish false until real verdicts and learner evidence exist. After accepted source integration, import Learn and anonymously read back the intended pages with their source revision. A local build is not publication.
