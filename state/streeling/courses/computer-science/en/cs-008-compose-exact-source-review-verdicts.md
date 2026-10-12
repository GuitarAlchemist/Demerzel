---
module_id: cs-008-compose-exact-source-review-verdicts
department: computer-science
course: Compose Exact-Source Review Verdicts
level: intermediate
prerequisites: ["cs-005-agent-handoff-evidence-contract", "cs-007-typed-agent-evidence-and-backpressure"]
estimated_duration: "45 minutes"
produced_by: codex-project-pilot
research_cycle: computer-science-2026-10-12-008
version: "0.1.0"
---

# Compose Exact-Source Review Verdicts

> **Department of Computer Science** | Intermediate | 45 minutes | English draft; subject and learner review pending

## Objectives and project question

You will derive a review status from a source revision and a bounded human verdict, identify which edits invalidate which verdicts, and separate a generated badge from authorization to publish. **Project question:** how can Streeling show useful review evidence for hundreds of courses without allowing a stale or automated verdict to masquerade as human approval? The exercise uses a real draft contract and a real, locally tested Learn generator. Both are in draft pull requests; neither establishes a completed human review or public deployment.

The need is concrete. [AUD-001's review brief](https://github.com/GuitarAlchemist/Demerzel/blob/2e1766e524e4e7900b380823006a8192cf6aa493/state/streeling/reviews/aud-001-review-brief.md) pins an English audio course and five translated Git blobs. It asks a subject reviewer to check the DSP claims and answers, fluent readers to check each translation, and a learner to attempt an answer-free task. A static preflight is useful but does not do any of those human jobs. The user has said they will designate a reviewer; this lesson has no review result to report.

## 1. Give each claim its own evidence

The proposed [Demerzel receipt schema at `5d7c1d1`](https://github.com/GuitarAlchemist/Demerzel/blob/5d7c1d1bd9972fe9d6d2e7a90ab3cdddabb8ed44/schemas/streeling-review-receipt.schema.json) records one `module_id`, `locale`, `kind`, `source_blob`, `reviewed_commit`, `reviewer`, `reviewed_at`, `verdict`, and `evidence`. The allowed kinds are `subject`, `language`, and `learner`; the allowed verdicts are `approved`, `changes_requested`, and `not_assessed`. A subject receipt binds the English file. A language receipt binds both its translated file and `source_english_blob`, the English text against which the translation was checked. One receipt is one bounded assertion, not a certificate for the whole course. The [receipt guide](https://github.com/GuitarAlchemist/Demerzel/blob/5d7c1d1bd9972fe9d6d2e7a90ab3cdddabb8ed44/state/streeling/review-receipts/README.md) explicitly says that the directory contains no approval receipt yet.

Git identifies a file's *content* by its blob hash. For a pinned commit `C`, `git rev-parse C:state/streeling/courses/audio-engineering/en/aud-001-eq-compression-order.md` yields the English blob at that commit. `reviewed_commit` is an audit pointer; `source_blob` says which bytes the reviewer judged. Matching a hash does not authenticate the reviewer, prove the evidence link was inspected, or turn an AI preflight into a human review. Those are separate governance checks.

Consider the following **synthetic** table; `E1`, `E2`, `F1`, and `F2` stand for distinct 40-character Git blob hashes, not actual AUD-001 values.

| Artifact | English blob | French blob | Receipt |
|---|---|---|---|
| Source revision A | `E1` | `F1` | none |
| English subject review | `E1` | — | `approved` |
| French language review | `E1` | `F1` | `approved` |
| French learner task | — | `F1` | `not_assessed` |

The French page at revision A has a matching approved English subject receipt and a matching approved French language receipt. Its learner result is **not assessed**. This is still a teaching fixture: the actual schema requires real SHA-1 hex values and review metadata. A valid JSON shape alone would not prove any real person approved those claims.

### Practice exercise 1

Can the two `approved` records in the table be collapsed into one `course_approved: true` flag? State one concrete failure that such a flag would hide.

> **Answer:** No. The subject record covers the English content; the language record covers the French rendering against that English content. A single flag would hide that the learner task remains `not_assessed`, and it could remain true after only the French text changes. It also cannot authenticate a reviewer. Keep the claims distinct and bind each to its source bytes.

## 2. Compose predicates, then keep the verdict

The [Learn review helper at `02fc08c`](https://github.com/spareilleux/learn/blob/02fc08c8f73e017412d1a623415ac4ab08645eb0/scripts/streeling-review-status.mjs) reads course blob IDs from `git ls-tree` at the imported source commit. Its core match is small: the receipt's `source_blob` must equal the relevant file blob, and a language receipt's `source_english_blob` must also equal the current English blob. For a matching receipt, it also checks that `reviewed_commit` contains the claimed file blobs at their named paths. It returns the *matching receipt*, not a Boolean. A `changes_requested` receipt can therefore be displayed without counting as approval. An unmatched old receipt yields a pending display for that claim. Learn's [sync tests at the same commit](https://github.com/spareilleux/learn/blob/02fc08c8f73e017412d1a623415ac4ab08645eb0/scripts/tests/sync-streeling.test.mjs) cover the no-receipt, exact-match, stale-English, stale-translation, wrong-locale, changes-requested, malformed-receipt, and contradictory-commit cases.

For discussion, write the composition as predicates. This notation describes the draft helper; it is not IXQL syntax:

```text
match_subject  = receipt.kind == subject
                 && receipt.locale == en
                 && receipt.source_blob == current_english_blob
match_language = receipt.kind == language
                 && receipt.locale == page_locale
                 && receipt.source_blob == current_translation_blob
                 && receipt.source_english_blob == current_english_blob
approved_claim = matching_receipt != null
                 && matching_receipt.verdict == approved
```

This makes the dependencies visible. A language verdict depends on two sources, while an English subject verdict depends on one. The helper also validates field shape, filename, UTC timestamp, allowed values, and the reviewed commit's relevant file blobs before generating pages. A malformed or contradictory matching receipt fails the import rather than being silently ignored. This commit check came from dogfooding this very lesson: the first draft checked only the commit's syntax, allowing its audit pointer to contradict the claimed blob. Validation still cannot authenticate a person; a repository reviewer must inspect the claimed identity and evidence. The draft receipt contract is subject to a separate human review gate because it touches `schemas/`.

### Practice exercise 2

At revision A, which of the three claims in the table count as approved? If the French learner receipt changes from `not_assessed` to `changes_requested` without a learner retest, does the approved count increase?

> **Answer:** The English subject and French language claims match their blobs and carry `approved`; the learner claim matches but is `not_assessed`. Changing its verdict to `changes_requested` does not increase the approved count. It would report an outstanding learner finding, not a successful task. In a real review, changing the record also needs a genuine reviewer decision and evidence.

## 3. Revisions invalidate only the claims they touch

Suppose revision B edits the English course to `E2` and leaves the French file at `F1`. The old subject receipt names `E1`, so it no longer matches. The French language receipt still names `F1`, but its `source_english_blob` is `E1`, so it no longer matches either. The learner receipt, which concerns the unchanged French page `F1`, still matches and still says `not_assessed`. If only French changes to `F2` while English remains `E1`, the English subject receipt remains applicable; the French language and learner receipts tied to `F1` no longer match. This is a dependency calculation, not a decision that the new text is bad. A reviewer can inspect the new diff and issue a new verdict.

Run the calculation with real bytes when reviewing a course:

```text
git rev-parse <source-commit>:state/streeling/courses/<department>/en/<module-id>.md
git rev-parse <source-commit>:state/streeling/courses/<department>/fr/<module-id>.fr.md
```

Use a *commit SHA* and the actual course path, then compare the outputs with the receipt. The pinned AUD-001 brief provides real paths and blob IDs for a bounded pilot. Do not use the strings `E1` and `F1` as command arguments; they are placeholders. A source edit after a review can keep the meaning unchanged, but an agent cannot silently carry approval to the new blob. The human reviewer decides whether the diff warrants a fresh full review or a narrower extension.

### Practice exercise 3

From revision A, compute the three displayed statuses after (a) only English changes to `E2`, and (b) only French changes to `F2`. Say why `reviewed_commit` by itself is insufficient for either calculation.

> **Answer:** (a) Subject pending, French language pending, French learner `not_assessed`; the unchanged `F1` learner receipt still matches. (b) English subject approved, French language pending, French learner pending. A commit identifies a tree, not which file bytes a particular verdict covered. The relevant blob IDs and, for a translation, the English dependency determine applicability. The Learn helper matches those blobs; it does not treat any newer commit as automatically approved.

## 4. Keep publication as a separate effect

The draft [Learn sync implementation](https://github.com/spareilleux/learn/blob/02fc08c8f73e017412d1a623415ac4ab08645eb0/scripts/sync-streeling.mjs) renders separate subject, language, and learner statuses on generated pages and counts only matching `approved` receipts in overviews. A local build of the preceding commit generated 1,603 pages and displayed pending review for AUD-001 in English, French, and Spanish; the later commit's focused sync tests passed after the reviewed-commit guard was added. These checks do not prove that a human reviewed AUD-001, that every translated course was checked, or that the public site serves the build.

Treat publication as a separate transition with its own checks: approved human evidence for the intended claims, reviewed and merged source, a generated site from the chosen source commit, deployment, then anonymous readback of the intended page and source revision. If one of those checks is absent, keep the course's `review.completed` or `publish.completed` flag false as appropriate. A badge derived from a receipt is a view of evidence, not authority to merge or deploy. This separation is useful to an agentic workflow because it gives each agent a small, auditable function: inspect a source, record a verdict, calculate applicability, render status, and verify public output. It also supplies a reason to hold a downstream publication step when an upstream claim is unresolved. That last policy is a design proposal until enforced by a tested pipeline.

### Practice exercise 4

A generated French page says “translation approved” from a matching receipt, but the English subject review is pending. May an agent mark the whole course reviewed and published? Which evidence is missing?

> **Answer:** No. The language receipt covers only French rendering against its English source; it does not approve the English audio or computer-science content. The matching subject verdict is missing. Publication also needs a reviewed source integration, deployment, and anonymous readback for the chosen revision. The displayed translation status is accurate for its narrow claim but cannot authorize the wider transition.

### Practice exercise 5

A file named `aud-001.en.subject.json` has a current `source_blob` and `verdict: "approved"`, but an extra unknown field makes it invalid under the draft schema. A teammate suggests ignoring that file and showing all existing badges. What should the draft sync do, and what test would catch accidental partial output?

> **Answer:** Reject the import before writing generated pages. The Learn helper rejects unknown fields, and its sync test puts an invalid receipt in a fixture, expects an error, and checks that the previous lock file is unchanged. Ignoring malformed evidence could make stale output look fresh; generating some pages before failure could leave a mixed revision. A passing test establishes this behavior only for the tested draft implementation, not for a deployed public site.

## Sources, limits, and next check

The project sources are the [AUD-001 bounded review brief](https://github.com/GuitarAlchemist/Demerzel/blob/2e1766e524e4e7900b380823006a8192cf6aa493/state/streeling/reviews/aud-001-review-brief.md), [draft Demerzel schema](https://github.com/GuitarAlchemist/Demerzel/blob/5d7c1d1bd9972fe9d6d2e7a90ab3cdddabb8ed44/schemas/streeling-review-receipt.schema.json), [draft Learn helper](https://github.com/spareilleux/learn/blob/02fc08c8f73e017412d1a623415ac4ab08645eb0/scripts/streeling-review-status.mjs), and [Learn fixture test](https://github.com/spareilleux/learn/blob/02fc08c8f73e017412d1a623415ac4ab08645eb0/scripts/tests/sync-streeling.test.mjs). The receipt contract is in Demerzel draft PR #1211, the generator in Learn draft PR #170, and this course in Demerzel draft PR #1207. The review schema's shape cannot authenticate a human; the local tests cannot establish site deployment. No human verdict, learner attempt, translation of this course, or public readback is recorded here. The next useful check is the designated AUD-001 subject reviewer filling one exact-source verdict with cited findings, followed by a learner attempt and an anonymous page readback after an authorized release.
