---
module_id: wml-003-term-preservation-and-cultural-review
department: world-music-languages
course: Audit Guitar Terms Across Six Languages
level: intermediate
prerequisites: ["wml-001-guitar-around-the-world", "wml-002-dadgad-layout-and-cultural-claims"]
estimated_duration: "40 minutes"
produced_by: codex-project-pilot
research_cycle: world-music-languages-2026-10-12-003
version: "0.1.0"
---

# Audit Guitar Terms Across Six Languages

> **Department of World Music & Languages** | Intermediate | 40 minutes | English draft; cultural, language, and learner review pending

## Objectives and project question

You will reproduce a six-language term inventory from exact Git source, distinguish literal spelling from translated meaning, and decide what a machine check can safely say about a culturally specific music lesson. **Project question:** how can Streeling scale guitar-course localization without turning a successful string search into an unsupported claim that every translation is correct or published? This lesson uses one existing course and one deterministic audit. It contains no approved cultural or language verdict.

[WML-001 at Demerzel commit `f5b040a`](https://github.com/GuitarAlchemist/Demerzel/blob/f5b040ae040a5a7f1fe6c3f609f878c00a3a1859/state/streeling/courses/world-music-languages/en/wml-001-guitar-around-the-world.md) surveys several guitar traditions. It has source files in English, French, Spanish, Portuguese, Italian, and German. [WML-002 at the same commit](https://github.com/GuitarAlchemist/Demerzel/blob/f5b040ae040a5a7f1fe6c3f609f878c00a3a1859/state/streeling/courses/world-music-languages/en/wml-002-dadgad-layout-and-cultural-claims.md) shows why a tuning table can establish note names while a cultural association needs a different kind of source. Here we audit a narrower, mechanical question: do seven selected terms from WML-001 appear literally in each of its six source files? Those seven terms are a **teaching sample**, not a complete glossary or a list of required translations.

## 1. Reproduce the lexical inventory

The pinned [term-check script](https://github.com/GuitarAlchemist/Demerzel/blob/882d5284426ea230d08f067f74e1f95ca56fb90d/state/streeling/fixtures/world-music-languages/wml-003/check_terms.py) reads **Git objects** at the full source commit, not whatever files happen to be in a working tree. For each locale it records the file path, Git blob ID, and a case-insensitive literal-presence Boolean for `rasgueado`, `picado`, `alzapúa`, `compás`, `golpe`, `batidas`, and `la pompe`. Its checked-in [JSON receipt](https://github.com/GuitarAlchemist/Demerzel/blob/882d5284426ea230d08f067f74e1f95ca56fb90d/state/streeling/fixtures/world-music-languages/wml-003/term-presence-f5b040a.json) can be reproduced with this command at the Demerzel repository root:

```text
python state/streeling/fixtures/world-music-languages/wml-003/check_terms.py --ref f5b040ae040a5a7f1fe6c3f609f878c00a3a1859
```

The pinned result has **42 term-locale pairs** (`7 × 6`). Forty are exact case-insensitive matches. The two absent literal forms are `fr:alzapúa` and `fr:compás`. The [French WML-001 source at that commit](https://github.com/GuitarAlchemist/Demerzel/blob/f5b040ae040a5a7f1fe6c3f609f878c00a3a1859/state/streeling/courses/world-music-languages/fr/wml-001-guitar-around-the-world.fr.md) instead prints `Alzapua` and `Compas` without accents in its technique list. An earlier loose search for `alzap` and `comp.s` returned six files for both; it hid this exact-spelling difference. That is the dogfooding result behind this lesson.

The script deliberately returns an audit record even when forms are absent. Its optional `--require-exact` flag exits with code 1 for a strict lexical gate. Neither mode calls the French file wrong. A fluent musician may judge an unaccented borrowing acceptable or prefer the source-language spelling; a blind replacement could make prose worse or fail to address a deeper mistranslation. The audit gives the reviewer precise lines to inspect.

### Practice Exercise 1

Compute the total pairs and exact matches from the seven-term, six-language receipt. Name the two missing literal pairs and the two strings that do appear in their French place.

> **Answer:** Seven terms times six files gives 42 pairs. Forty match literally ignoring case. The two absent pairs are French `alzapúa` and French `compás`; the French source uses `Alzapua` and `Compas`. This arithmetic says nothing yet about whether those spellings are acceptable French guitar terminology.

## 2. Preserve the evidence boundary

The current check uses Unicode `casefold()`, so `Rasgueado` matches `rasgueado`, but `Alzapua` does not match `alzapúa`. Accent folding could be added as a **separate** comparison by Unicode decomposition and removal of combining marks. It should not replace the exact-form column: a normalized hit and an exact hit answer different questions. The source term may be a loanword, a proper name, or a word whose accent distinguishes meanings. A terminology policy must be set with appropriate language and musical expertise before making a spelling rule normative.

Literal presence is also weak evidence of coverage. A term can occur only in a glossary while the lesson body omits the underlying concept. A translator can preserve a heading and change the claim below it. Conversely, a sound translation may use a different expression and fail the exact check. To assess meaning, compare the sentence, example, answer, and musical context against the English source; to assess cultural authority, consult musicians or scholarship relevant to the specific tradition. The script does none of that. It does not compare term definitions or check whether a French reader can perform a technique.

WML-001's English flamenco paragraph describes `compás` and then speaks of 12-beat cycles. The lexical audit can confirm whether the word occurs in each file. It cannot establish that the paragraph accurately represents all flamenco practice, nor that a translation preserves the intended nuance. Treat the paragraph as a **course claim to review**, not a fact proved by this lesson's term counts. [WML-002's DADGAD exercise](https://github.com/GuitarAlchemist/Demerzel/blob/f5b040ae040a5a7f1fe6c3f609f878c00a3a1859/state/streeling/courses/world-music-languages/en/wml-002-dadgad-layout-and-cultural-claims.md) applies the same separation to note data and broad cultural prose from a GA skill.

### Practice Exercise 2

If a new checker removes accents before matching, what would its French result be for these two terms? Should its result overwrite the exact-spelling result? Give one reason for each answer.

> **Answer:** It would likely match `Alzapua` to `alzapúa` and `Compas` to `compás`, yielding two additional accent-insensitive hits, provided it applies the same normalization to both strings. It should add a separate normalized column, not overwrite the exact column, because the original mismatch is useful to a reviewer deciding whether source-language spelling matters. Neither comparison determines semantic correctness.

### Practice Exercise 3

The receipt says that a French blob contains `Compas`. A later commit edits that file but leaves the English file unchanged. Can the old receipt prove the new French file still has the term? What two Git values should a reviewer compare before reusing the audit?

> **Answer:** No. The receipt is bound to the French Git blob at `f5b040a`; a later French edit produces a different blob even if the word happens to remain. Compare the old and new French blob IDs and the pinned source commit; rerun the check for the new commit rather than attributing the old audit to it. For translation review, also know which English blob the French version was checked against.

## 3. Compose language review with site publication

The six WML-001 *source* files are one state. The [draft Learn sync code at `02fc08c`](https://github.com/spareilleux/learn/blob/02fc08c8f73e017412d1a623415ac4ab08645eb0/scripts/sync-streeling.mjs) currently generates English, French, and Spanish course pages; an isolated import of Demerzel `f5b040a` reported 113 EN, 80 FR, and 80 ES pages across the site. This is local build-input evidence, not anonymous public readback. Portuguese, Italian, and German WML-001 source files do not by themselves establish that those site routes exist. Even a generated page can still have subject, translation, and learner review pending; a deployment must be inspected separately.

A safe review chain can be expressed as small functions: `read_source(commit, path)` returns bytes and blob; `check_terms(bytes, glossary)` returns lexical observations; `review_meaning(locale_blob, english_blob, evidence)` returns a human verdict; `render_status(receipts, imported_commit)` labels the generated page; `read_public_page(url, expected_commit)` verifies what anonymous readers receive. Each function has a narrower output than “course approved.” The draft [exact-source receipt contract](https://github.com/GuitarAlchemist/Demerzel/blob/5d7c1d1bd9972fe9d6d2e7a90ab3cdddabb8ed44/schemas/streeling-review-receipt.schema.json) requires the translation's blob and its English dependency. It is still under human schema review; this lesson neither creates a receipt nor bypasses it.

### Practice Exercise 4

All seven terms pass an accent-insensitive check in French, but a reviewer has not examined the `compás` paragraph or its exercise. Which status can the agent report: lexical check passed, French meaning approved, or published French lesson? Give the minimum evidence needed for each later status.

> **Answer:** It can report only that the stated lexical check passed for the pinned file. French meaning approval needs a human review of the relevant French and English blobs, the paragraph, examples, and exercises, with a recorded verdict and evidence. Public publication needs an accepted source revision, generated and deployed page, and anonymous readback tied to that revision. Term presence cannot authorize either later step.

### Practice Exercise 5

A planner sees six WML-001 source locales, the local Learn import's three rendered locales, and no review receipt. How many WML-001 locales can it truthfully call human-reviewed? Can it claim six public routes? Identify the next useful check for one French learner.

> **Answer:** Zero locales have a recorded human verdict in this lesson. The source-file count cannot prove six public routes; the local import supports only EN/FR/ES generation and does not prove that even those pages were deployed. For a French learner, first obtain subject and French-language reviews bound to the exact English and French blobs, then give an answer-free task, record the result, deploy the accepted revision, and read the public French page anonymously.

## Sources, limits, and next check

The source data is [WML-001 EN](https://github.com/GuitarAlchemist/Demerzel/blob/f5b040ae040a5a7f1fe6c3f609f878c00a3a1859/state/streeling/courses/world-music-languages/en/wml-001-guitar-around-the-world.md) and [FR](https://github.com/GuitarAlchemist/Demerzel/blob/f5b040ae040a5a7f1fe6c3f609f878c00a3a1859/state/streeling/courses/world-music-languages/fr/wml-001-guitar-around-the-world.fr.md) at `f5b040a`, plus the other four locale blobs named in the reproducible receipt. The script checks literal case-insensitive presence anywhere in a file, using seven selected terms. It cannot judge translation, cultural claims, learner performance, or publication. No fluent-language or subject reviewer has approved this course or WML-001 in this cycle. The next check is a French guitarist and fluent reviewer assessing the two accent differences and the surrounding definitions against the pinned English/French blobs; their findings may justify edits and a fresh exact-source audit.
