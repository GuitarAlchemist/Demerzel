---
module_id: mus-008-intervals-inversion-compound
department: music
course: Intervals, Inversion and Compound Intervals
level: beginner
alchemical_stage: nigredo
prerequisites: [mus-007-pitch-spelling-enharmonic-identity]
estimated_duration: "45 minutes"
produced_by: claude-code-hand-authored
version: "1.0.0"
---

# Intervals, Inversion and Compound Intervals — Counting Past the Octave

> **Department of Music** | Stage: Nigredo (Beginner) | Estimated duration: 45 minutes

## Objectives

After this lesson, you will be able to:
- Name an interval by its number, counted on the letters, and by its quality, measured in semitones: perfect, major, minor, augmented or diminished
- Invert a simple interval, and explain why the numbers of an interval and its inversion add up to 9 and their semitones to 12
- Name a compound interval such as a major 9th or a perfect 11th, give its semitones, and reduce it to its simple form
- Name the interval between two fretted notes more than an octave apart, from their letters and octave numbers
- Trace where GA computes simple intervals correctly, and where its compound intervals mix two numberings

---

## 1. Number and Quality

An interval has two parts. Its **number** counts letters, both ends included: C to E covers C, D and E, so it is a third, whatever accidentals the two notes carry. Its **quality** comes from the semitones it spans.

The reference is the major scale built on the lower note. Above C, it gives:

| Number | Name | Note above C | Semitones | Quality in the major scale |
|---|---|---|---|---|
| 1 | Unison | C | 0 | Perfect |
| 2 | Second | D | 2 | Major |
| 3 | Third | E | 4 | Major |
| 4 | Fourth | F | 5 | Perfect |
| 5 | Fifth | G | 7 | Perfect |
| 6 | Sixth | A | 9 | Major |
| 7 | Seventh | B | 11 | Major |
| 8 | Octave | C | 12 | Perfect |

The unison, fourth, fifth and octave are **perfect** numbers; the second, third, sixth and seventh are **imperfect** ones. A perfect number is perfect at its reference size, augmented (A) one semitone larger and diminished (d) one semitone smaller. An imperfect number is major (M) at its reference size and minor (m) one semitone smaller; it is augmented one semitone larger than major, and diminished one semitone smaller than minor. Doubly augmented and doubly diminished go one semitone further. There is no major fifth and no perfect third: each number has only its own family of qualities. Counted with every quality from doubly diminished to doubly augmented, the range GA uses, the eight numbers give 44 simple intervals, 5 for each perfect number and 6 for each imperfect one. A few of them are only theoretical, such as the diminished unison, whose upper note would sound below the lower one.

Two intervals with the same semitones can have different names. C to F♯ and C to G♭ both span 6 semitones: the first covers four letters and is an augmented fourth, A4; the second covers five and is a diminished fifth, d5. MUS-007 left a pair of this kind open: D♭ to F and C♯ to F both span four semitones. D♭ to F covers three letters, and four semitones is the reference size of a third, so it is a major third. C♯ to F covers four letters, and four semitones is one less than a perfect fourth, so it is a diminished fourth.

### Practice Exercise

Name the intervals E to B♭ and A to C♯.

> *Solution:* E to B♭ covers five letters, E F G A B, and spans 6 semitones, one less than a perfect fifth: a diminished fifth, d5. A to C♯ covers three letters and spans 4 semitones, the reference size of a third: a major third, M3.

---

## 2. Inversion

To **invert** an interval, move its lower note up an octave, or its upper note down one. C up to E, a major third, becomes E up to C, a minor sixth.

Two sums stay fixed. The numbers add up to 9, not 8, because the note that stays is counted in both intervals: a third and a sixth, 3 + 6 = 9. The semitones add up to 12, an octave: 4 + 8 = 12. The quality changes within its family: major becomes minor and minor becomes major, augmented becomes diminished and diminished becomes augmented, the doubly altered qualities swap in the same way, and perfect stays perfect. The perfect numbers invert into each other, 1 and 8, 4 and 5, and so do the imperfect ones, 2 and 7, 3 and 6. Over all 44 simple intervals, the two sums are always 9 and 12.

| Interval | Semitones | Inversion | Semitones |
|---|---|---|---|
| M3 | 4 | m6 | 8 |
| m2 | 1 | M7 | 11 |
| P4 | 5 | P5 | 7 |
| A4 | 6 | d5 | 6 |

The augmented fourth and the diminished fifth are each other's inversion, and both span 6 semitones, half an octave: the **tritone**.

### Practice Exercise

Invert a minor seventh and an augmented second.

> *Solution:* A minor seventh, 10 semitones, inverts to a major second, 2 semitones: 7 + 2 = 9 and 10 + 2 = 12. An augmented second, 3 semitones, inverts to a diminished seventh, 9 semitones.

---

## 3. Compound Intervals

An interval whose number is greater than 8 is **compound**: it covers more than an octave of letters. Add an octave to a simple interval and its number grows by 7, not 8, for the same reason as in §2: the octave's top note is counted twice, as the last letter of the octave and as the first of the interval above it. A second above an octave is a 9th, 8 + 2 − 1, and a third above an octave a 10th. The semitones grow by 12, and the quality does not change. To find the **simple form** of a compound interval, take 7 off the number and 12 off the semitones.

| Compound number | Simple form | Major or perfect semitones |
|---|---|---|
| 9 | 2 | 14 |
| 10 | 3 | 16 |
| 11 | 4 | 17 |
| 12 | 5 | 19 |
| 13 | 6 | 21 |
| 14 | 7 | 23 |
| 15 | 8 | 24 |

The 11th, 12th and 15th are perfect, like the fourth, fifth and octave they come from; the others are major or minor. The 15th spans two octaves, 15 = 8 + 8 − 1, and is also called a **double octave**.

Chord symbols name the notes stacked above the seventh by compound numbers: the 9 of C9 is D, the second degree of C major an octave up, and the 11 and 13 of C11 and C13 are F and A. In a voicing the note may sound in any octave; the number names its degree above the root.

### Practice Exercise

Give the simple form of a major 10th and of a perfect 12th, and the semitones of a minor 9th.

> *Solution:* A major 10th, 16 semitones, reduces to a major third, 4 semitones; a perfect 12th, 19, to a perfect fifth, 7. A minor 9th spans 13 semitones: a minor second, 1, plus an octave.

---

## 4. On the Fretboard

On a guitar in standard tuning, the open strings are E2, A2, D3, G3, B3 and E4, MIDI 40, 45, 50, 55, 59 and 64, and each fret adds a semitone, as Learn's [lesson 1](https://github.com/spareilleux/learn/blob/6c78aad43cb932323cf74933b4fb36121e5cb9a3/src/content/docs/music-theory-ga/01-notes-and-the-fretboard.mdx) checks. A chord shape often spans more than an octave. In x32033, a C chord with an added ninth, Cadd9, the fifth string at fret 3 sounds C3, MIDI 48, and the second string at fret 3 sounds D4, MIDI 62.

Two subtractions name the interval. The semitones are the difference of the MIDI numbers: 62 − 48 = 14. The number counts letters across the octaves: with the letters numbered from C = 0 to B = 6, it is 7 × (difference of the octave numbers) + (difference of the letters) + 1. For C3 to D4 that gives 7 × 1 + 1 + 1 = 9. A ninth is major at 14 semitones, a major second plus an octave, so C3 to D4 is a major 9th: the added ninth that names the chord.

| Shape | Lower note | Upper note | Semitones | Interval |
|---|---|---|---|---|
| Cadd9, x32033 | C3, string 5, fret 3 | D4, string 2, fret 3 | 14 | M9 |
| Cadd9, x32033 | C3, string 5, fret 3 | G4, string 1, fret 3 | 19 | P12 |
| E, 022100 | E2, string 6, open | G♯3, string 3, fret 1 | 16 | M10 |
| Asus4, x02230 | A2, string 5, open | D4, string 2, fret 3 | 17 | P11 |

The open E shape puts its third, G♯3, a 10th above the bass, and the suspended fourth of Asus4, D4, sounds an 11th above its bass. Reducing each to its simple form gives the chord-tone names: the third, the fourth, and for Cadd9 the second and the fifth.

### Practice Exercise

In the open G shape 320003, name the intervals from the low G, string 6 at fret 3, to the open B string and to the high G, string 1 at fret 3.

> *Solution:* The low G is G2, MIDI 43. The open B string is B3, MIDI 59: 16 semitones, and 7 × 1 + (6 − 4) + 1 = 10, a major 10th. The high G is G4, MIDI 67: 24 semitones, and 7 × 2 + 0 + 1 = 15, a perfect 15th, a double octave.

---

## 5. Where GA Stands

GA is the music-theory library and chatbot of the GuitarAlchemist ecosystem. The facts below are read from its code at commit [`5c3a52a`](https://github.com/GuitarAlchemist/ga/tree/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26); this lesson documents that code and does not change it, and it has not run GA or its tests. The files it cites are unchanged on GA's `main` at `8fe33f8`. Learn's music-theory-ga [lesson 1](https://github.com/spareilleux/learn/blob/6c78aad43cb932323cf74933b4fb36121e5cb9a3/src/content/docs/music-theory-ga/01-notes-and-the-fretboard.mdx) compiles an earlier version of GA, `a826864`, and checks its simple intervals. The other numbers below come from a line-by-line Python transcription of the GA code named.

**`Interval.Simple` is right.** [`Interval.Simple`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Primitives/Intervals/Interval.Diatonic.Simple.cs#L28) computes its semitones as the [reference size](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Primitives/Intervals/SimpleIntervalSize.cs#L85) of its number plus the [accidental of its quality](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Primitives/Intervals/IntervalQuality.cs#L127), with one table for perfect numbers and one for imperfect numbers, as in §1. [`ToInverse`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Primitives/Intervals/Interval.Diatonic.Simple.cs#L43) takes [9 minus the number](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Primitives/Intervals/SimpleIntervalSize.cs#L136) and [negates the quality](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Primitives/Intervals/IntervalQuality.cs#L115), whose values run from −3 for doubly diminished to 3 for doubly augmented, so major and minor swap, and so do augmented and diminished. By transcription, all 44 simple intervals get the semitones of §1, and each inverts as in §2, with sums of 9 and 12. Learn's lesson 1 checks [eight intervals](https://github.com/spareilleux/learn/blob/6c78aad43cb932323cf74933b4fb36121e5cb9a3/code/music-theory-ga/expected/l1.txt#L27) named by [`GetInterval`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Primitives/Extensions/NoteExtensions.cs#L104) from two note names, from C–E to E–C, and the inversion of [M3 into m6](https://github.com/spareilleux/learn/blob/6c78aad43cb932323cf74933b4fb36121e5cb9a3/code/music-theory-ga/expected/l1.txt#L37). `NoteExtensions.cs` and `IntervalQuality.cs` have not changed since `a826864`, nor have the semitone table and `ToInverse` of `SimpleIntervalSize`, so those checks still apply at `5c3a52a`. `GetInterval` takes notes without octaves, so it always returns a simple interval: of C3 and D4 it sees only C and D, a major second. It also [reduces the semitones mod 12](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Primitives/Extensions/NoteExtensions.cs#L110) and falls back on [perfect](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Primitives/Extensions/NoteExtensions.cs#L42) or [major](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Primitives/Extensions/NoteExtensions.cs#L55) when the difference falls outside its table, so C to B♯, an augmented seventh of 12 semitones, comes out M7.

One gap concerns parsing. [`Interval.Simple.TryParse`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Primitives/Intervals/Interval.Diatonic.Simple.cs#L77) accepts any quality letter before any number, so "M5" parses as a major fifth, which §1 rules out. Asked for its semitones, that interval throws an `InvalidOperationException` from the [table of perfect accidentals](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Primitives/Intervals/IntervalQuality.cs#L142).

**Compound intervals mix two numberings.** [`CompoundIntervalSize`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Primitives/Intervals/CompoundIntervalSize.cs#L15) holds the numbers 9 to 16 and names them Ninth to Fifteenth, then [DoubleOctave](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Primitives/Intervals/CompoundIntervalSize.cs#L188) for 16. Its parts disagree on what a number means:

- Its [semitone table](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Primitives/Intervals/CompoundIntervalSize.cs#L145) gives 9 → 12, 10 → 14, 11 → 16, 12 → 17, 13 → 19, 14 → 21, 15 → 23 and 16 → 24. That is the table of §3 moved up one number: each number gets the semitones of the number below it, 12, an octave, for a ninth, and 24, a double octave, for 16.
- [`ToSimple`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Primitives/Intervals/CompoundIntervalSize.cs#L47) subtracts 8, in the same shifted numbering: a ninth reduces to 1, a unison, not to a second.
- [`SimpleIntervalSize.ToCompound`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Primitives/Intervals/SimpleIntervalSize.cs#L125) adds 7, as §3 does. A round trip through `ToCompound` and `ToSimple` therefore returns the number below its start, from a second, through 9, to 1, up to an octave, through 15, to 7. A unison's `ToCompound` would be 8, which is out of range, and throws an `ArgumentOutOfRangeException`.
- Its [consonance](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Primitives/Intervals/CompoundIntervalSize.cs#L129) calls 11, 12 and 16 perfect: 11 and 12 as in §3, then 16 where §3 has 15.
- Its summary calls the numbers ["Between 9 and 16 semitones"](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Primitives/Intervals/CompoundIntervalSize.cs#L4) and gives the example ["9 = Octave + Second (9 semitones)"](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Primitives/Intervals/CompoundIntervalSize.cs#L12). Nine counts letters; a minor or major ninth spans 13 or 14 semitones.

[`Interval.Compound`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Primitives/Intervals/Interval.Diatonic.Compound.cs#L31) adds its quality's accidental to that table. By transcription, its M9 therefore spans 12 semitones, m9 11, M10 14, P11 16, P12 17 and M13 19: one semitone short for the 11th, two for the others. Of its 11 named intervals, from m9 to [P15](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Primitives/Intervals/Interval.Diatonic.Compound.cs#L132), only P15 comes out right, at 24 semitones, because it is built on the size 16, and so it prints as "P16". Parsing "P15" gives the size 15, which the consonance calls imperfect, and that interval throws an `InvalidOperationException` when asked for its semitones. Built by `ToCompound` from the 44 simple intervals of §1, no compound interval gets its textbook semitones: 38 come out one or two short, the 5 unisons throw in `ToCompound`, and the compound of P8 throws when asked for its semitones. The right values are also in GA: its [`Semitones`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Primitives/Intervals/Semitones.cs#L36) type defines MajorNinth as 14, PerfectEleventh as 17 and MajorThirteenth as 21.

**Who reads these values.** [`ScaleModeCompoundInterval.ToSimple`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Primitives/Intervals/ScaleModeCompoundInterval.cs#L15) is the only caller of `ToSimple`, and no GA code calls it. `ScaleMode` builds a [compound interval](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Tonal/Modes/ScaleMode.cs#L207) for each even number of a mode, 2, 4 and 6, in its `SimpleAndCompoundIntervals` property, which no GA code names. GA's MongoDB [interval sync](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/GA.Data.MongoDB/Services/DocumentServices/IntervalSyncService.cs#L34) stores each compound size with the table's semitones, 12 for 9. GA's tests parse compound names, such as "b9" into [m9](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Tests/Common/GA.Business.Core.Tests/IntervalTests.cs#L181), check that "13" is [not read as a third](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Tests/GA.Domain.Core.Tests/Primitives/IntervalParsingTests.cs#L53), and check that a fourth's `ToCompound` is [11](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Tests/Common/GA.Core.Tests/Collections/ValueObjectMemoizationTests.cs#L175). No test asks a compound interval for its semitones, and none calls `ToSimple`.

Fixing any of this is for GA's owners; this lesson only describes it.

### Practice Exercise

By transcription, GA's `Interval.Compound.P11` spans 16 semitones. Which interval of §4 spans 16 semitones, and what should P11 span?

> *Solution:* The major 10th from E2 to G♯3. A perfect 11th spans 17: a perfect fourth, 5, plus an octave. GA reads the size 11 in a table moved up one number, where 16 belongs to the 10th.

---

## 6. Proposed Experiment (Not Yet Run)

**Status: not run.** This section proposes an experiment for Learn's music-theory-ga lab, which compiles GA; the lab's GA pin would first move to `5c3a52a`. Nothing in it is a measurement. The predictions come from the transcription of §5 and are written down before any run; a later version of this lesson will report the results. Every step calls GA's types in the lab's own process, never a running MCP server or a language model.

1. **Simple intervals.** Build the 44 simple intervals of §1 and read their semitones. Prediction: all 44 match §1.
2. **Inversion.** Invert each of them with `ToInverse`. Prediction: in all 44 cases the numbers add up to 9 and the semitones to 12.
3. **Round trip.** For each of the 8 simple sizes, call `ToCompound`, then `ToSimple`. Prediction: the unison throws an `ArgumentOutOfRangeException`, and the 7 others come back one number lower, the octave as a seventh.
4. **Named compound intervals.** Read the semitones of the 11 named compound intervals, from m9 to P15. Prediction: 10 differ from §3; only P15, printed "P16", has its 24.
5. **Compound from simple.** Call `ToCompound` on the 44 simple intervals and compare each result's semitones with the simple interval's plus 12. Prediction: none match; 38 are one or two short, 5 throw in `ToCompound`, and the compound of P8 throws when asked for its semitones.
6. **Parsing.** Parse "P15", "15" and "M5" with `Interval.Diatonic.Parse`, which tries a simple interval first, then a compound one. Prediction: all three parse; "15" gives M15, 23 semitones, and the other two throw an `InvalidOperationException` when asked for their semitones.

### Practice Exercise

Step 3 predicts that a round trip from a third returns a second. Which change to `ToSimple` would make the 7 round trips return their start, and which other parts of `CompoundIntervalSize` would it then contradict?

> *Solution:* `ToSimple` would subtract 7, the inverse of `ToCompound`. The rest of the type would still follow the shifted numbering. The semitone table would have to move down one number, to 9 → 14 up to 15 → 24, and the perfect sizes would have to become 11, 12 and 15. The size 16, which `ToSimple` would now send to 9, outside the simple range, would have to go, with `DoubleOctave` and the `P15` built on it moving to 15.

---

## 7. Common Pitfalls

- **Counting semitones for the number.** C to E spans four semitones, but it covers three letters: it is a third.
- **Naming an interval from its semitones alone.** C–F♯ and C–G♭ both span 6 semitones; the first is A4, the second d5.
- **Major fifths and perfect thirds.** The 1, 4, 5 and 8 are perfect, augmented or diminished; the 2, 3, 6 and 7 are major, minor, augmented or diminished.
- **Inversions that add up to 8.** The numbers of an interval and its inversion add up to 9.
- **Adding 8 for an octave.** A second plus an octave is a 9th, and two octaves make a 15th.
- **Forgetting the octave of a compound interval.** In Cadd9, D4 lies 14 semitones above C3, not 2.
- **Reading a compound size from GA's table.** At `5c3a52a`, `CompoundIntervalSize` counts 12 semitones for a 9th, where `Semitones.MajorNinth` counts 14.

---

## Key Terms

| Term | Definition |
|------|-----------|
| **Interval number** | The count of letters an interval covers, both ends included: C to E is a third |
| **Quality** | Perfect, major, minor, augmented or diminished, set by the semitones against the major scale of the lower note |
| **Perfect number** | The unison, fourth, fifth and octave, and their compounds: perfect, augmented or diminished |
| **Imperfect number** | The second, third, sixth and seventh, and their compounds: major, minor, augmented or diminished |
| **Inversion** | The interval left when the lower note moves up an octave; the numbers add up to 9 and the semitones to 12 |
| **Compound interval** | An interval whose number is greater than 8: 7 more in number and 12 more in semitones than its simple form |
| **Tritone** | An interval of 6 semitones: the augmented fourth or the diminished fifth |

---

## Self-Check Assessment

**1. Give the inversion of a major third, with both sums.**
> A minor sixth: 3 + 6 = 9, and 4 + 8 = 12 semitones.

**2. What is the simple form of a major 10th?**
> A major third: 10 − 7 = 3, and 16 − 12 = 4 semitones.

**3. On a standard-tuned guitar, how many semitones lie between the open fifth string and the second string at fret 3, and what is the interval?**
> A2 is MIDI 45 and D4 is 62: 17 semitones, a perfect 11th, the fourth of Asus4 above its bass.

**4. By transcription, GA's [`Interval.Compound.M9`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Primitives/Intervals/Interval.Diatonic.Compound.cs#L123) spans 12 semitones. What should it span, and where does 12 come from?**
> 14: a major second, 2, plus an octave. The [`CompoundIntervalSize`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Primitives/Intervals/CompoundIntervalSize.cs#L145) table gives each number the semitones of the number below it, and 12 is the octave's.

**Pass criteria:** Name any simple or compound interval from its letters and semitones; invert a simple interval, with sums of 9 and 12; reduce a compound interval to its simple form; name the interval between two fretted notes from their octave numbers; and tell GA's correct simple intervals from its shifted compound table.

---

## Research Basis

- E. Aldwell, C. Schachter and A. Cadwallader, *Harmony and Voice Leading*, Cengage, 2019: intervals, their qualities, inversion and compound intervals
- W. Piston, *Harmony*, revised by M. DeVoto, W. W. Norton, 1987: scales and intervals
- GA source at commit `5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26`: every code fact in §5 links to its line
- Learn, music-theory-ga lesson 1 and its expected output at commit `6c78aad43cb932323cf74933b4fb36121e5cb9a3`: the compiled checks of GA's simple intervals quoted in §5
- Experiment: proposed in §6, not run; this lesson contains no measurement of its own
- Provenance: hand-authored by a Claude Code session (Opus 5.5) from the Streeling curriculum plan, not produced by the Seldon course pipeline; under review
- Belief state: T(0.85) F(0.02) U(0.10) C(0.03)
