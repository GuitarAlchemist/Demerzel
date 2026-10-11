---
module_id: wml-002-dadgad-layout-and-cultural-claims
department: world-music-languages
course: "World Music & Languages: DADGAD in a GA Tuning Answer"
level: intermediate
alchemical_stage: albedo
prerequisites: [wml-001-guitar-around-the-world]
estimated_duration: "35 minutes"
produced_by: codex-project-pilot
research_cycle: world-music-languages-2026-10-11-002
version: "0.1.0"
---

# DADGAD: Tuning Facts and Cultural Claims

> **Department of World Music & Languages** | Level: Intermediate | Stage: Albedo | Duration: 35 minutes | English draft awaiting review

## Objectives

After this lesson, you will be able to read a six-string tuning in the order a GA skill uses, check its changes from standard tuning, distinguish an open-string pitch collection from a style or performance, and label a source's cultural prose as a claim requiring further evidence. You will also be able to describe what a deterministic lookup establishes without treating its numeric confidence as proof of musical or cultural authority.

## Project question and evidence boundary

A guitarist asks Guitar Alchemist (GA), “What is DADGAD tuning?” GA's pinned [`AlternateTuningsSkill`](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/Common/GA.Business.ML/Agents/Skills/AlternateTuningsSkill.cs) contains a named DADGAD entry and code that formats a string-by-string answer. The entry also offers a “Why use it” sentence connecting the tuning to Celtic and modal folk music and “Indian-flavored playing.” **Which parts of that answer can a guitarist verify from the tuning table, and which parts require musicians, recordings, or historical sources?** This lesson pins GA commit `dc2e74cbd992a298f67efb928b5b3754615e1924` for every code claim.

[WML-001](wml-001-guitar-around-the-world.md) surveys guitar traditions. Here we audit one musician-facing answer. The checked-in code and [test source](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/Tests/Common/GA.Business.ML.Tests/Unit/AlternateTuningsSkillTests.cs) allow a reproducible source reading; they do not provide a recorded DADGAD performance or independent evidence for the listed cultural associations. No GA chatbot session, physical instrument, translation, or listener study was run for this lesson.

## 1. Put the strings in the right order

The skill's remarks explicitly state **low to high**, meaning string 6 through string 1. Its standard-tuning array is `E, A, D, G, B, E`, and its DADGAD array is `D, A, D, G, A, D`. The answer formatter prints the six notes in that order, numbers each row `6 - i`, and labels the first and last rows low and high. This is an ordering convention in this GA skill, not a universal software convention. Reversing the array would keep the letters but give the player incorrect string assignments.

| Guitar string | 6 (low) | 5 | 4 | 3 | 2 | 1 (high) |
|---|---|---|---|---|---|---|
| Standard | E | A | D | G | B | E |
| GA DADGAD entry | D | A | D | G | A | D |
| Change in semitones | −2 | 0 | 0 | 0 | −2 | −2 |

Three strings change relative to the source's standard tuning: string 6 E→D, string 2 B→A, and string 1 E→D. Each drops a whole step, or two semitones; strings 5, 4, and 3 retain their open notes. The table permits a player to verify the *target note names* and differences. It does not measure the player's actual tuning, tell us how much a given string's tension changes, or certify that a particular guitar is safely set up for this tuning. Those are separate practical checks.

In another language, retain both the note sequence and the direction. A translated phrase that accidentally means high to low would change the instruction while preserving every letter. Showing numbered strings beside the sequence reduces that ambiguity. Note naming itself also needs review for the target locale; this English draft does not supply approved French, Spanish, or other-language guitar terminology.

### Exercise 1 — Read the orientation

Using the pinned skill, place `D A D G A D` on strings 6 to 1. What are the low and high open-string notes, and why would presenting the sequence in reverse be misleading?

> **Answer:** Strings 6, 5, 4, 3, 2, 1 are D, A, D, G, A, D respectively. Both outer strings are D. The code orders notes low to high; reversing the sequence changes which note is assigned to each numbered string, even when a symmetrical endpoint makes the first and last letters look reassuring.

### Exercise 2 — Check each change

Compare the source's standard `E A D G B E` with its DADGAD entry. Which strings change, by how many semitones, and which remain the same?

> **Answer:** Strings 6, 2, and 1 each fall two semitones: E→D, B→A, and E→D. Strings 5 A, 4 D, and 3 G are unchanged. The skill's `VsStandard` text says the same, and the row-wise difference follows from the two arrays.

## 2. The open strings explain a sound category, not a culture

Strum the *listed open strings on paper*: D, A, D, G, A, D. Removing duplicates leaves D, G, and A. Relative to D, G is a fourth and A is a fifth; the collection has no F or F♯ third. That supports the skill's compact “open Dsus4” description of the unfretted pitch collection. It does not specify a rhythm, ornament, melody, performer, or cultural setting. A recording could use the tuning while barely sounding its open strings.

The same source includes a separate Open D entry: `D, A, D, F#, A, D`. Relative to DADGAD, only string 3 changes, from G to F♯, a semitone lower. Its distinct open-string notes are D, F♯, and A, the D-major triad. This comparison makes the structural distinction audible in principle and checkable in the file. It does not prove that all music played in either tuning follows a single harmonic vocabulary. Fretted notes, slides, bends, capo placement, and technique can alter the result.

“DADGAD has an open suspended-fourth collection” is a claim derived from note names under common chord labeling. “This guitarist plays authentic music from tradition X” would require evidence about the work, musician, community context, and musical practice. A tuning name alone cannot deliver that conclusion. Even if two recordings used exactly the same open strings, the cultural claims about them could differ.

### Exercise 3 — Compare two open tunings

Give the distinct pitch names in the DADGAD and Open D entries. Which string differs, by how much, and why does the source call their unfretted collections Dsus4 and D major respectively?

> **Answer:** DADGAD has {D, G, A}; Open D has {D, F♯, A}. String 3 changes from G to F♯, one semitone downward. Relative to D, D–G–A gives root, fourth, and fifth without a third, so “Dsus4” describes the open collection. D–F♯–A supplies the major third, so “D major” describes Open D's open collection. Neither label identifies a performed tradition.

## 3. Read the answer's provenance

`ExecuteAsync` tests named tuning patterns before trying a six-note reverse lookup. The DADGAD regular expression matches a contiguous or hyphenated name and maps it to the `dadgad` table key. For a direct named match, `AnswerTuning` prints the low-to-high sequence, string rows, a `VsStandard` explanation, and the entry's `Flavor` under “Why use it.” The successful result sets `Confidence = 1.0f` and returns evidence strings naming the skill and tuning-table lookup.

That confidence value belongs to the returned **lookup response** in this implementation. It is not an independent probability that every sentence in `Flavor` is historically or culturally correct. A single function formats both mechanical note data and prose in one answer; that shared formatting does not give both claim types the same support. The code has no citations alongside the DADGAD `Flavor` field. This lesson therefore reports its cultural language as *what the source says*, not as a verified account of a tradition or musician.

The skill also defines `CanHandle(message) => false` with a comment that it uses semantic routing. That line does not prove that a live chatbot routes a particular user message here. The test file checks named and reverse lookups for some tunings and accidental guards; it does not contain a dedicated DADGAD outcome test. Our DADGAD outputs are source-derived from the table and formatter. Running a pinned skill test for this exact prompt and checking an actual chatbot trace would be separate verification steps.

### Exercise 4 — Interpret confidence narrowly

A source reader sees `Confidence = 1.0f` next to a generated DADGAD answer. What does the code establish about that value, and why can it not validate the sentence about Celtic, modal folk, and “Indian-flavored” playing? Can this source alone prove that the GA chatbot showed the answer to a user?

> **Answer:** `Result` assigns 1.0 to a successful table-lookup response and attaches skill/table evidence. `AnswerTuning` appends the uncited `Flavor` prose to that response; the numeric value does not independently test that prose. `CanHandle` returns false and the lesson has no routing trace, so the source cannot prove a live chatbot displayed this answer.

## 4. Translate a claim without upgrading it

The DADGAD entry's “Why use it” sentence says the tuning is “beloved for Celtic, modal folk, and Indian-flavored playing” and names artists and a recording. Those associations may guide a question, but the code provides no direct recording analysis or cited cultural history for them. The phrase “Indian-flavored” is particularly broad: it does not name a musician, genre, repertoire, region, or technique. It should not become a translated claim that this tuning represents Indian music generally. Similar care applies to the word “Celtic,” which covers more than one musical community and practice.

A useful product caption can separate layers: “GA's alternate-tuning table lists DADGAD as D–A–D–G–A–D, strings 6→1. Its optional description associates that tuning with several styles; those associations have not been checked here.” A musician can act on the specified string notes while seeing the status of the cultural prose. For a localization, preserve the numbered orientation, keep names and tuning symbols accurate, and ask a musician and native-language reviewer to assess words for traditions and techniques. A translation that is fluent but turns “the source associates” into “this is authentic to” changes the claim.

For a particular performance, a stronger cultural statement would need an identified recording or score, context supplied by relevant musicians or scholarship, and an explanation of what features are being compared. No performance was analyzed in this cycle. The tuning table also cannot establish whether a guitar's strings, setup, or player technique make this configuration comfortable. Product guidance should be evaluated on the instrument and with the people it addresses.

### Exercise 5 — Choose defensible copy

Which caption is warranted by the pinned skill? **A:** “GA's DADGAD table lists D–A–D–G–A–D low to high; its descriptive text associates the tuning with Celtic and modal folk and with ‘Indian-flavored’ playing.” **B:** “DADGAD proves this recording is authentic Indian music.” Name one additional check before making a recording-specific cultural statement.

> **Answer:** A accurately attributes the notes and associations to the GA source. B is unsupported: neither the tuning table nor an uncited `Flavor` sentence identifies or analyzes a recording or validates authenticity. Inspect an identified performance with relevant musician or cultural expertise and a stated criterion before making a narrower, recording-specific claim.

## Limits and next check

This lesson is a pinned source reading. It did not execute `AlternateTuningsSkill`, route a chatbot prompt, play a guitar, listen to a recording, or validate cultural history and artist associations. The five exercises test source facts and transparent derivations; they do not measure learning. A next check would add and run a DADGAD named-lookup test on a pinned build, compare a captured answer with its source fields, and separately review cultural copy with relevant musicians and native-language reviewers. Translation, human subject review, learner testing, Learn sync/build, anonymous public readback, and publication remain pending.
