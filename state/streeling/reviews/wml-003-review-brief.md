# WML-003 bounded review brief

Status: **open**. This brief is a request for human subject, cultural, and learner review; it is not an approval receipt.

## Frozen target

- Course: [`wml-003-term-preservation-and-cultural-review.md`](https://github.com/GuitarAlchemist/Demerzel/blob/89f98c688d7f429332c6d0e219df1f129555efca/state/streeling/courses/world-music-languages/en/wml-003-term-preservation-and-cultural-review.md), Demerzel commit `89f98c688d7f429332c6d0e219df1f129555efca`, Git blob `ca64ee59b1763014e1b9dcc2aec634862ffddfb8`.
- Audit script: Git blob `9731e69e15d04c352519be93c200fa23f9bc0e85`; checked JSON receipt: Git blob `677c202ce5aef7fc71d192d716b146ad0f9211ca` at the same commit.
- WML-001 input sources: Demerzel commit `f5b040ae040a5a7f1fe6c3f609f878c00a3a1859`; the JSON receipt names the six individual input blobs.
- Production record: `state/streeling/course-productions/cp-world-music-languages-2026-10-12-003.json`, with review and publication flags false.

A later course edit changes its blob and needs a new verdict or an explicit reviewer decision on the diff. The audit fixture is an input, not human language evidence.

## Subject and cultural review

1. Re-run the script at its pinned input commit. Check 42 term-locale comparisons, 40 literal matches, and the two French exact-form absences. Confirm that the course describes the `--require-exact` exit code as a lexical signal rather than a translation failure.
2. Inspect the WML-001 English and French technique list and glossary. Decide whether `Alzapua` and `Compas` are acceptable in this context or whether source-language accents should be retained; record the basis for that decision. Do not infer this from the script alone.
3. Check that the lesson does not treat WML-001's cultural descriptions, including its `compás` paragraph, as established by term presence. Flag any unsupported cultural generalization or missing community-specific source.
4. Attempt all five exercises without consulting the answer blocks, then compare each answer. Mark ambiguous wording or any answer that requires knowledge absent from the lesson or pinned files.
5. Check the product boundary: six WML-001 source languages, only EN/FR/ES in the isolated Learn import, no recorded human review, and no new public deployment or anonymous readback.

For each completed review, record reviewer identifier or pseudonym, UTC time, scope (`subject`, one named `language`, or `learner`), the exact relevant blob, evidence, findings with section references, and `approved`, `changes_requested`, or `not_assessed`. A WML-003 subject or learner verdict binds the WML-003 English blob `ca64ee59b1763014e1b9dcc2aec634862ffddfb8`. A separate French-language verdict **for WML-001**, if requested, needs a fluent reviewer and binds WML-001 French blob `09910885147627ec4f840e22e1d8d486600ea5c9` and English blob `34a172aaa9ea90f47e786831b70fcad56bfe31b4`. Do not attach a WML-001 translation verdict to WML-003. The draft receipt contract is in Demerzel PR #1211 and still needs human schema review; do not manufacture a receipt from this brief.

## Answer-free learner trial

Give the learner [`wml-003-learner-task.md`](wml-003-learner-task.md) without this brief or the course answer blocks. Record prior guitar and language experience, time, the response verbatim, confusion, and any lesson change followed by a retest.

Score five items from 0 to 2, for a maximum of 10: (1) correct 42/40/two-absence calculation; (2) identifies the exact input commit and why a later blob needs a new audit; (3) keeps exact spelling separate from meaning and cultural authority; (4) distinguishes six source locales from three locally generated site locales and public deployment; (5) proposes a specific human follow-up instead of self-approving the translation. `8/10` with no false claim of approval is the proposed pilot pass threshold; this threshold itself needs learner-review feedback. No trial has been performed.

Keep `review.completed` and `publish.completed` false until real findings are addressed and recorded. After an accepted revision, import into Learn, build, deploy, and read back the public page anonymously with its source SHA.
