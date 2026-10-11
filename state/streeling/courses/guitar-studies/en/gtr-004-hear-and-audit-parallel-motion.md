---
module_id: gtr-004-hear-and-audit-parallel-motion
department: guitar-studies
course: "Hear and Audit Parallel Motion on Two Guitar Strings"
level: intermediate
alchemical_stage: albedo
prerequisites: [gtr-003-audit-voicing-playability]
estimated_duration: "35 minutes"
produced_by: codex-project-pilot
research_cycle: guitar-studies-2026-10-11-004
version: "0.1.0"
---

# Hear and Audit Parallel Motion on Two Guitar Strings

> **Department of Guitar Studies** | Level: Intermediate | Stage: Albedo | Duration: 35 minutes | English draft awaiting review

## Objectives

After this lesson, you will be able to map a small two-string guitar fixture to pitches, predict when GA's progression analyzer reports parallel fifths, distinguish that report from a judgment about sound or comfort, and run a repeatable playing trial. You will also identify a case the string-matching algorithm does not assess.

## The project question

[GAA-004](../../guitar-alchemist-academy/en/gaa-004-choose-a-useful-voicing.md) teaches how to inspect one candidate voicing; [GTR-003](gtr-003-audit-voicing-playability.md) separates fret geometry from a player's comfort. A progression adds another question: **What changes between two successive voicings?** GA's pinned [`ProgressionVoiceLeadingAnalyzer`](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/Common/GA.Domain.Services/Fretboard/Voicings/Analysis/ProgressionVoiceLeadingAnalyzer.cs) detects a defined pattern of parallel perfect fifths or octaves between string-matched played notes. Its [`ProgressionVoiceLeadingReport`](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/Common/GA.Domain.Services/Fretboard/Voicings/Analysis/ProgressionVoiceLeadingReport.cs) records issues and exposes flags. These links and the remaining GA sources pin commit `dc2e74cbd992a298f67efb928b5b3754615e1924`.

The code can answer whether its own conditions are met. It cannot hear a player's articulation, infer an independent musical voice that switches strings, or decide whether parallel motion is desirable in a genre. This lesson uses a **new synthetic fret fixture** built from GA's [default guitar tuning](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/Common/GA.Domain.Core/Instruments/Tuning.cs), not a captured generator response. The fixture is physically possible to fret and pluck, but nobody's execution is claimed here. Its predicted report is derived from the pinned source, not measured from a running analyzer.

## 1. Define the strings and the notes

GA's default tuning is `E2 A2 D3 G3 B3 E4`, listed from low to high in `Tuning.Default`; string numbers in the analyzer count the other way, from 1 at the high E to 6 at the low E. Our pair uses **string 4**, open D3, and **string 3**, open G3. In MIDI-note arithmetic, D3 is 50 and G3 is 55. A positive fret raises that open pitch by one semitone per fret. We will sound only these two strings and mute the others.

| Dyad | String 4 (D string) | String 3 (G string) | Purpose |
|---|---|---|---|
| A | fret 2: E3, MIDI 52 | fret 4: B3, MIDI 59 | starting pair |
| B | fret 4: F♯3, MIDI 54 | fret 6: C♯4, MIDI 61 | both voices rise |
| C | fret 4: F♯3, MIDI 54 | fret 2: A3, MIDI 57 | voices move in opposite directions |

These are **dyads**, not claims that GA has generated a named chord progression. Write both fret numbers and both pitches in any trial record. A bare name such as “A to B” will not let someone reproduce the exercise if the table is separated from it. If your guitar is not in GA's default tuning, retune safely or calculate a new fixture and state the actual open-string pitches; the answer key below assumes D3 and G3.

### Exercise 1 — Convert frets into pitches

Starting with D3 = MIDI 50 and G3 = MIDI 55, calculate the two notes of A and B. Which string is higher in pitch in each dyad?

> **Answer:** A gives string 4: `50 + 2 = 52` (E3), string 3: `55 + 4 = 59` (B3). B gives string 4: `50 + 4 = 54` (F♯3), string 3: `55 + 6 = 61` (C♯4). String 3 is higher in both. These calculations assume standard tuning and one semitone per fret; they are not a played observation.

## 2. Compute the source's interval test

The analyzer builds a map from each **played string number** to its supplied MIDI note. It intersects the two maps' string keys. If fewer than two strings occur in both voicings, it returns no issues for that transition. Otherwise it checks each shared string pair. For one pair, it first asks whether both MIDI notes move and have the same direction. Then it computes `abs(noteB - noteA) % 12` before and after. A value of `7` both times produces a `Fifths` issue; a value of `0` both times produces an `Octaves` issue. The `0` class includes octave-equivalent intervals, so its label needs care if the actual notes are unisons.

In A, `59 - 52 = 7` semitones. In B, `61 - 54 = 7`. There is one shared pair, strings 3 and 4, and neither note is muted. This satisfies the interval part of the fifths test. The code's modulo operation means it is checking an interval class, not a complete harmonic or stylistic analysis. The MIDI values must correspond to the actual fret/tuning fixture for the physical exercise, but the analyzer itself uses the supplied MIDI values. That distinction matters because a caller could supply inconsistent positions and notes.

The pinned [unit tests](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/Tests/Common/GA.Business.Core.Tests/Fretboard/Voicings/ProgressionVoiceLeadingAnalyzerTests.cs) cover detected fifths, octaves, contrary and oblique motion, a three-chord progression, and empty or single-item input. Their helper constructs played positions at fret zero with chosen MIDI numbers; these are algorithm fixtures, not examples that necessarily match guitar tuning. This lesson's fret table is a separate, physically consistent teaching fixture. The tests are checked-in source evidence, not a fresh test run for this course.

### Exercise 2 — Check both intervals

Compute the source's interval class for A and B: `abs(string 3 MIDI - string 4 MIDI) % 12`. Would the interval condition alone be enough to flag parallel fifths?

> **Answer:** A is `abs(59 - 52) % 12 = 7`; B is `abs(61 - 54) % 12 = 7`. This satisfies the interval condition. The analyzer must also find the same two played strings in both voicings and verify that both notes moved in the same nonzero direction.

## 3. Compare motion, not just two snapshots

From A to B, string 4 moves `52 → 54`, a rise of two semitones. String 3 moves `59 → 61`, also a rise of two. With two shared strings, both directions positive, and intervals `7 → 7`, the pinned algorithm predicts **one `Fifths` issue**. The report's `HasParallelFifths` would be true and `IsClean` false for a two-voicing progression made from consistent `Voicing` objects matching this table. We have not constructed or executed those objects here; that is a source-derived prediction.

Now compare A to C. String 4 still moves `52 → 54`, but string 3 moves `59 → 57`, a fall of two. The directions disagree, and the target interval is `abs(57 - 54) = 3`. This transition is therefore not a parallel fifth under the detector. It does **not** preserve the same target harmony as B. Do not rank C as musically better merely because it avoids this flag. In actual music, parallel perfect intervals may be intended, and a contrary-motion alternative can change the chord or melody. The exercise asks for the report's classification, not a universal composing rule.

### Exercise 3 — Predict the report for A→B

State both movements and the report's fifths flag for an ordered progression `[A, B]` represented with the table's two played strings and MIDI notes. How many fifth issues can this two-string pair contribute?

> **Answer:** String 4 rises `52 → 54` (+2); string 3 rises `59 → 61` (+2). Both intervals are 7 semitones, so the analyzer predicts `HasParallelFifths = true` and `IsClean = false`. There is one shared string pair, so it contributes one `Fifths` issue.

### Exercise 4 — Predict the alternative carefully

For `[A, C]`, give the directions, final interval, and predicted `IsClean` value. Is C an interchangeable target for B?

> **Answer:** String 4 rises by 2; string 3 falls by 2. C's interval is `57 - 54 = 3` semitones. The source skips opposite-direction pairs, so this two-dyad fixture predicts `IsClean = true`. C differs from B in its upper note and target harmony; it is not an interchangeable musical replacement merely because the detector is clean.

## 4. Play a falsifiable transition

If you have a guitar in standard tuning, sound A using only strings 4 and 3. Pluck each note separately, then together. Move to B and repeat. Use a slow metronome at **60 beats per minute**: play A on one beat, move, then sound B on the next and let it ring for one beat. Make ten A→B attempts. Record the two target pitches (with a tuner or a recording checked note by note), whether each sounded cleanly for the beat, and whether unintended strings rang. Define a successful attempt as **both target notes at the expected pitches and clearly ringing for the full target beat**. Predeclare an 8-of-10 practice threshold; report the observed numerator even if it is below eight. Stop if the hand hurts. This threshold is a classroom criterion, not a GA model score or a validated population norm.

The test can fail: wrong tuning, a muted or buzzing upper note, an unintended third string, or fewer than eight successful target dyads all falsify “I met the stated practice target today.” If a pitch-measuring tool is unavailable, write “pitch not independently checked” and keep the clean-note count separate. No physical attempts have been recorded for this draft. An answer key cannot substitute for the learner's observations. Compare the sound of A→B with A→C as a listening prompt, but do not claim that one must sound better.

## 5. Understand what a clean report omits

The analyzer's issue list only contains patterns it can detect under its string-matching rule. Imagine A followed by a new dyad D played on strings 4 and 2, with string 3 muted. Only string 4 is shared with A. The detector returns no issues before comparing intervals because it needs at least two shared played strings. The report's `IsClean` then means `Issues.Count == 0`, not that the progression has good counterpoint, is easy to play, or has no unwanted sound. A musician might hear a voice continue from string 3 to string 2, but this algorithm does not track such cross-string continuity.

The same distinction applies to a one-chord input. `Analyze` returns a clean report when fewer than two voicings are supplied; there is no transition to examine. An empty issue list should be displayed as “no defined parallel fifth/octave pattern detected in the analyzed string matches,” with the input scope visible. Treat the report as a narrow diagnostic alongside musical judgment, not as a complete voice-leading grade.

### Exercise 5 — Audit the missing comparison

Starting from A on strings 4 and 3, suppose D plays only strings 4 and 2. How many string keys are shared, what does the analyzer return for A→D, and what does that result fail to establish?

> **Answer:** Only string 4 is shared, so there is one common played-string key. The detector returns no issue before evaluating an interval pair, and the resulting report is `IsClean = true`. This does not establish that the sounding voices have no parallel motion across strings, that the transition is comfortable, or that it is musically preferable.

## Evidence, limitations, and next check

The predictions above follow the pinned GA [analyzer](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/Common/GA.Domain.Services/Fretboard/Voicings/Analysis/ProgressionVoiceLeadingAnalyzer.cs), [report](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/Common/GA.Domain.Services/Fretboard/Voicings/Analysis/ProgressionVoiceLeadingReport.cs), [tuning](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/Common/GA.Domain.Core/Instruments/Tuning.cs), and [test source](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/Tests/Common/GA.Business.Core.Tests/Fretboard/Voicings/ProgressionVoiceLeadingAnalyzerTests.cs). The teaching fret arrays and MIDI notes were constructed for this course; they are not captured GA output. No analyzer execution, learner recording, tutor assessment, or fresh C# test run is claimed. The code follows guitar strings as voice identifiers, uses interval classes modulo twelve, and does not measure tone quality, timing, hand effort, or musical fit. A future check should run these exact consistent `Voicing` objects on the pinned build, retain the report, and collect the ten-attempt playing record. Human subject review, learner testing, localization, and publication remain pending.
