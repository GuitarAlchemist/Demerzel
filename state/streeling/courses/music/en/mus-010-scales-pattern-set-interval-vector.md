---
module_id: mus-010-scales-pattern-set-interval-vector
department: music
course: Scale Patterns, Sets and the Diatonic Interval Vector
level: intermediate
alchemical_stage: albedo
prerequisites: [mus-008-intervals-inversion-compound, mat-022-symmetry-groups-invariants]
estimated_duration: "60 minutes"
produced_by: claude-code-hand-authored
version: "1.0.0"
---

# Scale Patterns, Sets and the Diatonic Interval Vector — What Is Rare About the Major Scale

> **Department of Music** | Stage: Albedo (Intermediate) | Estimated duration: 60 minutes

## Objectives

After this lesson, you will be able to:
- Build any scale on any root from its step pattern, and spell a seven-note scale with one letter per degree
- Tell a scale's step pattern, its pitch-class set and its interval-class vector apart, and say what each one forgets
- Compute the vectors of the major, pentatonic and whole-tone scales, and use the common-tone theorem to say how many notes two keys share
- Recognise the deep scale property, Myhill's property, maximal evenness and generation by fifths, and say which of them the major scale, the pentatonic and the whole-tone scale have
- Trace how GA computes these properties, and where its results depend on the transposition or differ from the definitions

---

## 1. A Scale as a Step Pattern

A scale lists notes in order within an octave. Its **step pattern** lists the semitones from each note to the next, ending with the step back to the octave, so the steps add up to 12.

| Scale | Step pattern | On C |
|------|------|------|
| Major | 2 2 1 2 2 2 1 | C D E F G A B |
| Natural minor | 2 1 2 2 1 2 2 | C D E♭ F G A♭ B♭ |
| Major pentatonic | 2 2 3 2 3 | C D E G A |
| Whole tone | 2 2 2 2 2 2 | C D E F♯ G♯ A♯ |

Written in whole steps (W) and half steps (H), the major pattern is W W H W W W H. Wikipedia's "Major scale" notes that "a major scale may be seen as two identical tetrachords separated by a whole tone": W W H, then W, then W W H.

To build a scale on another root, apply the same steps from that root. A seven-note scale then takes one letter per degree, and each accidental follows from the letter (MUS-007). E major is E F♯ G♯ A B C♯ D♯. F major is F G A B♭ C D E: the fourth degree is a semitone above A, and it is written B♭, not A♯, because A is already the third degree.

On the guitar, a step pattern on one string is a list of fret distances. On the A string, the major pattern from the open string gives frets 0 2 4 5 7 9 11 12: A B C♯ D E F♯ G♯ A. The same distances from fret 3 give C major: frets 3 5 7 8 10 12 14 15.

### Practice Exercise

Build B♭ major and D natural minor from their patterns, with one letter per degree.

> *Solution:* B♭ major: B♭ C D E♭ F G A, steps 2 2 1 2 2 2 1. D natural minor: D E F G A B♭ C, steps 2 1 2 2 1 2 2. In both, each letter appears once.

---

## 2. Pattern, Set and Root

A step pattern says nothing about where to start; a root fixes the notes. The **pitch-class set** keeps the notes and forgets the root, the order and the octaves (MUS-020): C major is {0, 2, 4, 5, 7, 9, 11} with C = 0.

Two scales can share a set and differ in their pattern. A natural minor, A B C D E F G, holds the notes of C major. Its pattern, 2 1 2 2 1 2 2, is the major pattern read from its sixth step: the steps A–B, B–C, then C–D through G–A. Reading one pattern from another step gives a **mode**; MUS-006 counts modes as rotations.

Transposing a scale adds the same number to every pitch class. It keeps the pattern and changes the set: the twelve major scales are twelve different sets. A scale that maps to itself under a transposition has fewer: there are only two whole-tone scales, {0, 2, 4, 6, 8, 10} and {1, 3, 5, 7, 9, 11} (MUS-006, MAT-022).

The rest of this lesson studies properties of the set, which the root does not change: its interval vector, the sizes its intervals come in, and how evenly it spreads around the octave.

### Practice Exercise

Which major scale holds the notes of E natural minor, and from which of its degrees does E minor start?

> *Solution:* E natural minor is E F♯ G A B C D, the notes of G major. E is the sixth degree of G major, and E minor's pattern, 2 1 2 2 1 2 2, is G major's read from that degree.

---

## 3. The Interval Vector of a Scale

The **interval-class vector** counts, for every pair of notes in a set, the interval class between them, from 1 (a semitone or a major seventh) to 6 (a tritone) (MUS-020). A set of n notes has n(n − 1)/2 pairs: 21 for seven notes, 15 for six, 10 for five.

For the major scale, count each class on C D E F G A B:
- **Class 1**, semitones: E–F and B–C. **2.**
- **Class 2**, whole steps: C–D, D–E, F–G, G–A and A–B. **5.**
- **Class 3**, minor thirds: D–F, E–G, A–C and B–D. **4.**
- **Class 4**, major thirds: C–E, F–A and G–B. **3.**
- **Class 5**, perfect fifths: F–C, C–G, G–D, D–A, A–E and E–B. **6.**
- **Class 6**, the tritone: B–F. **1.**

The total is 21, and the vector is <2 5 4 3 6 1>.

| Scale | Notes | Pairs | Vector |
|------|------|------|------|
| Major | C D E F G A B | 21 | <2 5 4 3 6 1> |
| Harmonic minor | A B C D E F G♯ | 21 | <3 3 5 4 4 2> |
| Major pentatonic | C D E G A | 10 | <0 3 2 1 4 0> |
| Whole tone | C D E F♯ G♯ A♯ | 15 | <0 6 0 6 0 3> |

The pentatonic has no semitone and no tritone; MUS-006 computes the same vector for the minor pentatonic. In the whole-tone scale every note has a whole step on each side and a major third on each side, which makes six pairs of class 2 and six of class 4. Its three tritones are C–F♯, D–G♯ and E–A♯, and it has no odd interval class at all.

### Practice Exercise

Compute the vector of the six-note scale C D E F G A.

> *Solution:* Fifteen pairs. Class 1: E–F. Class 2: C–D, D–E, F–G and G–A. Class 3: D–F, E–G and A–C. Class 4: C–E and F–A. Class 5: C–F, C–G, D–G, D–A and E–A. No tritone, since B is missing. The vector is <1 4 3 2 5 0>, and its entries add up to 15.

---

## 4. Deep Scales and Common Tones

The six entries of <2 5 4 3 6 1> are six different numbers. Wikipedia's "Common tone (scale)" calls this the **deep scale property**: "containing each interval class a unique number of times". The pentatonic's vector repeats 0, the harmonic minor's repeats 3 and 4, and the whole-tone scale's repeats 0 and 6: none of them is deep.

**The common-tone theorem.** Transpose a set by n semitones. A note b of the transposed set is a + n for some note a of the set, and b is also in the original set exactly when the set holds the interval going up n semitones from a. So the number of common tones is the number of such pairs:
- for n from 1 to 5, each pair is one interval of class n, so the count is the vector's entry for class n;
- for n from 7 to 11, each pair is one interval of class 12 − n;
- for the tritone, n = 6, each tritone counts from both of its ends, since a + 6 + 6 = a: B up to F and F up to B. The count is twice the vector's entry.

Wikipedia states the theorem for the diatonic scale: "However many times an interval class occurs in a diatonic scale is the number of tones common both to the original scale and a scale transposed by that particular interval class." For C major:

| Transposition (semitones) | Keys | Common tones |
|------|------|------|
| 0 | C | 7 |
| 1 or 11 | D♭, B | 2 |
| 2 or 10 | D, B♭ | 5 |
| 3 or 9 | E♭, A | 4 |
| 4 or 8 | E, A♭ | 3 |
| 5 or 7 | F, G | 6 |
| 6 | F♯ | 2: B, and F, written E♯ in F♯ major |

The two neighbours of C on the circle of fifths, F and G, keep six notes: going from C major to G major changes only F to F♯, one finger moved by one fret. Wikipedia: "Six of seven possible common tones are shared by closely related keys". Because the scale is deep, the transpositions by 1 to 5 semitones keep five different numbers of notes, the same up or down.

The tritone row needs care. Wikipedia gives the tritone 1 common tone, "as there is only one tritone in a diatonic scale", and its table lists B for F♯ major and F for G♭ major on separate rows. Counted as pitch classes, C major and F♯ major share both B and F; F♯ major spells F as E♯. Each tritone counts from both of its ends. That makes two notes, the same count as a transposition by a semitone; Wikipedia's 1 holds only for notes spelled the same. The doubled tritone count can repeat another one: the deep property guarantees different counts only for interval classes 1 to 5.

The whole-tone scale shows the opposite case: "every even transposition of the whole tone scale is identical with the original and every odd transposition has no common tones whatsoever" (Wikipedia, "Common tone (scale)").

**Which sets are deep?** Six different whole numbers add up to at least 0 + 1 + 2 + 3 + 4 + 5 = 15, so a deep set has at least 15 pairs, and therefore at least six notes. A count over the 4096 pitch-class sets finds 48 deep sets, twelve transpositions in each of four set classes:

| Forte class | Example | Vector | A chain of |
|------|------|------|------|
| 6-1 | C C♯ D E♭ E F | <5 4 3 2 1 0> | semitones |
| 6-32 | C D E F G A | <1 4 3 2 5 0> | fifths, F to E |
| 7-1 | C C♯ D E♭ E F F♯ | <6 5 4 3 2 1> | semitones |
| 7-35 | C D E F G A B | <2 5 4 3 6 1> | fifths, F to B |

So among seven-note sets, only the diatonic scale and the chromatic segment of seven notes are deep. Wikipedia's "Common tone (scale)" states the pattern this way: "In twelve-tone equal temperament, all scales with the deep scale property can be generated with any interval coprime with twelve". Read with the table, each deep set is a chain of one such interval, not of every one: the semitone or the fifth, the only two up to inversion. Multiplying every pitch class by 5, which MUS-020 calls M5, swaps the counts of classes 1 and 5: it sends each chromatic row of the table to the row of fifths of the same size.

### Practice Exercise

How many notes do C major and E♭ major share, and which?

> *Solution:* E♭ is 3 semitones above C, and the major scale has four intervals of class 3, so they share four notes: C, D, F and G. E♭ major replaces E, A and B with E♭, A♭ and B♭.

---

## 5. Two Sizes per Step, and Even Spacing

A **generic interval** "is the number of scale steps between notes of a collection or scale"; a **specific interval** is the number of semitones (Wikipedia, "Generic and specific intervals"). In the major scale, a third, two steps, is a minor third or a major third: 3 or 4 semitones.

| Generic interval (steps) | 1 | 2 | 3 | 4 | 5 | 6 |
|------|------|------|------|------|------|------|
| Major | 1, 2 | 3, 4 | 5, 6 | 6, 7 | 8, 9 | 10, 11 |
| Major pentatonic | 2, 3 | 4, 5 | 7, 8 | 9, 10 | | |
| Whole tone | 2 | 4 | 6 | 8 | 10 | |

- **Myhill's property** is having "exactly two specific intervals for every generic interval" (Wikipedia, "Generic and specific intervals"). The major and pentatonic scales have it; the whole-tone scale, with one size per step, does not.
- **Maximal evenness** (Clough and Douthett, 1991) is a different condition: every generic interval comes in one size or two consecutive sizes, so that the notes are "spread out as much as possible" (Wikipedia, "Maximal evenness"). The major, pentatonic and whole-tone scales are maximally even; the harmonic minor is not, since its seconds are 1, 2 and 3 semitones. Neither property implies the other. The whole-tone scale is maximally even without Myhill's property, and the seven-note chromatic segment C to F♯ of §4 has Myhill's property without being maximally even: its seconds are 1 or 6 semitones, two sizes but not consecutive ones.
- **A generated collection** is "formed by repeatedly adding a constant interval in integer notation, the generator" (Wikipedia, "Generated collection"). The major scale is a chain of seven notes linked by six fifths: "F-C-G-D-A-E-B". A chain is **well formed** when the generator always spans the same number of steps: in the major scale, each fifth of the chain spans 4 steps. "The major and minor pentatonic scales are also well formed." The six notes F C G D A E give C D E F G A, whose steps are 2 2 1 2 2 3: a fifth spans 4 steps from C to G but 3 from F to C, so this chain is generated and not well formed. Wikipedia's "Maximal evenness" ties well-formedness to Myhill's property, "a scale with Myhill's property is said to be a well-formed scale", and says that the whole-tone scale "is not well-formed since each generic interval comes in only one size". Its "Generated collection" calls the same scale a "degenerate well-formed collection", in which every step is the generator. For sets of two or more notes, once the degenerate chains are set aside, well-formedness and Myhill's property mean the same thing.

| Scale | Deep | Myhill's property | Maximally even | Generated |
|------|------|------|------|------|
| Major | yes | yes | yes | yes, seven notes in fifths |
| Major pentatonic | no | yes | yes | yes, five notes in fifths |
| Whole tone | no | no | yes | degenerate, whole steps |
| Harmonic minor | no | no | no | no |
| C D E F G A | yes | no | no | yes, six notes in fifths |

Of these five scales, only the major scale has all four properties. **Rothenberg propriety** adds one more test: an interval spanning more steps should never be smaller than one spanning fewer. The major scale passes, but the tritone is both a fourth, F–B, and a fifth, B–F, so Wikipedia's "Rothenberg propriety" calls it proper but "not strictly proper because the three step intervals and the four step intervals share an interval size (the tritone)"; "the major pentatonic scale is strictly proper".

These are facts about structure. They do not prove that the major scale sounds balanced; they show what is rare about it among the 4096 sets.

### Practice Exercise

Does A harmonic minor have Myhill's property? Is it maximally even?

> *Solution:* Neither. Its seconds are A–B, 2 semitones, B–C, 1, and F–G♯, 3: one generic interval in three sizes. Wikipedia's "Maximal evenness" gives this example.

---

## 6. Where GA Stands

GA is the music-theory library and chatbot of the GuitarAlchemist ecosystem. The facts below are read from its code at commit [`5c3a52a`](https://github.com/GuitarAlchemist/ga/tree/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26). This lesson documents that code and does not change it. It has not run GA or its tests: the counts below come from a line-by-line Python transcription of the methods cited. The files it cites are unchanged on GA's `main` at `0843879`. Learn's music-theory-ga course compiles an earlier version of GA, `a826864`, which has `IsDeepScale` but not `ScaleStructuralProperties`. Its lesson 4 [already quotes `IsDeepScale`](https://github.com/spareilleux/learn/blob/0c918c8206dc9dda0241d097e6b0c65e897c92ec/src/content/docs/music-theory-ga/04-set-classes.mdx#L77-L81) and Wikipedia's definition of a deep scale; this section goes on to the common tones and to the other properties.

**A scale is built from notes.** [`Scale`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Tonal/Scales/Scale.cs#L37-L45) takes a list of notes and [computes their pitch-class set and vector](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Tonal/Scales/Scale.cs#L42-L43). Its named scales are spelled out: [`Major`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Tonal/Scales/Scale.cs#L53) is "C D E F G A B", [`MajorPentatonic`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Tonal/Scales/Scale.cs#L57) "C D E G A", [`WholeTone`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Tonal/Scales/Scale.cs#L60) "C D E F# G# A#", and [`Minor.Natural`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Tonal/Scales/Scale.cs#L125) "A B C D E F G". A test checks that [the major scale's vector is <2 5 4 3 6 1>](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Tests/GA.Domain.Core.Tests/Theory/Tonal/ScaleTests.cs#L19-L21), and another that [A minor and C major share a set](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Tests/GA.Domain.Core.Tests/Theory/Tonal/ScaleTests.cs#L24-L27), as in §2. The scale also exposes [six structural properties](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Tonal/Scales/Scale.cs#L85-L90), and GA's MCP server prints them for a 12-bit scale id in its [`GaScaleProperties` tool](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/GaMcpServer/Tools/ScaleTool.cs#L168-L194).

**`IsDeepScale` is right, and no code refers to it.** [`IsDeepScale`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Atonal/IntervalClassVector.cs#L99) checks that the vector's six values are distinct, and the vector always holds six values, [zeros included](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Atonal/IntervalClassVectorId.cs#L45-L72), so the pentatonic's two zeros count as a repeat. Transcribed over the 4096 sets, it is true for exactly the 48 sets of §4. Its documentation [points to the common-tone theorem](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Atonal/IntervalClassVector.cs#L89-L98). No other code file in GA names it, and no test checks it.

**Myhill's property and Rothenberg propriety follow the definitions.** [`HasMyhillProperty`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Atonal/ScaleStructuralProperties.cs#L40-L68) collects the sizes of each generic interval and requires exactly two; transcribed, it holds for the major and pentatonic scales and not for the whole-tone scale. [`GetRothenbergPropriety`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Atonal/ScaleStructuralProperties.cs#L76-L123) compares the largest size of each generic interval with the smallest size of every larger one; transcribed, it returns `Proper` for the major scale and `StrictlyProper` for the pentatonic, as Wikipedia does. The Myhill test is named [`Dorian_HasMyhillProperty_ReturnsTrue`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Tests/GA.Domain.Core.Tests/Theory/Atonal/ScaleStructuralPropertiesTests.cs#L10-L16) and builds `Scale.Major`; its comment reads "Major / Dorian (1709)", but 1709 is the id of C Dorian, a different set from C major's 2741. All five tests of the file build `Scale.Major`, so none of them checks a scale for which `HasMyhillProperty` or `IsWellFormed` is false.

**`IsWellFormed` tests generation, not well-formedness.** The method's summary defines a well-formed scale as one ["generated by repeatedly stacking a single generator interval mod 12"](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Atonal/ScaleStructuralProperties.cs#L151-L154), and the [method](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Atonal/ScaleStructuralProperties.cs#L163-L187) accepts any chain of one interval. That is §5's generated collection. Transcribed over the 4096 sets, 89 pass `IsWellFormed` without Myhill's property:
- 13 sets of at most one note: the empty set and the 12 single notes;
- 16 equal divisions of the octave: the tritone, the augmented triad, the diminished seventh, the whole-tone scale and the full chromatic, which Wikipedia calls degenerate;
- 60 chains of fifths of 4, 6, 8, 9 or 10 notes, such as C D G A and §5's C D E F G A, each of which has a generic interval in three sizes.

No set has Myhill's property and fails `IsWellFormed`. For the major scale the method reports generator 5, the first that works in the order 1 to 11: the chain of fourths B E A D G C F, which is §5's chain of fifths read backwards.

**The evenness score depends on the transposition.** [`GetMaximalEvennessDiscrepancy`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Atonal/ScaleStructuralProperties.cs#L129-L149) takes the pitch classes of a set of n notes in ascending order from C, compares them with the points 0, 12 / n, 2 × 12 / n and so on, and returns the root mean square of the differences. Its summary cites Clough and Douthett and promises ["0.0 for perfectly even sets like Whole Tone or Augmented"](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Atonal/ScaleStructuralProperties.cs#L125-L128). Transcribed, rounded to four places:
- the whole-tone scale scores 0.0000 on C and 1.0000 on C♯, and the augmented triad 0.0000 on C and 1.0000 on C♯;
- GA's own [`Scale.Augmented`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Tonal/Scales/Scale.cs#L61), C D♯ E G G♯ B, is the six-note augmented scale, not the triad, and scores 0.7071;
- the twelve major scales score from 0.2857, B♭ major, to 1.1780, F♯ major; C major scores 0.4041.

For Clough and Douthett, maximal evenness is a yes-or-no property, and all twelve major scales have it. By GA's score, 472 seven-note sets that are not maximally even come out more even than F♯ major. The tool's own description suggests ["1709 for Dorian or 2741 for Major"](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/GaMcpServer/Tools/ScaleTool.cs#L174): the two ids hold the notes of B♭ major and of C major, one scale in two transpositions, and score 0.2857 and 0.4041. No test checks the score.

Fixing any of this is for GA's owners; this lesson only describes it.

### Practice Exercise

What do GA's `IsWellFormed` and `HasMyhillProperty` return for C D G A, and why do they disagree?

> *Solution:* `IsWellFormed` returns true with generator 5: from A, adding 5 semitones three times gives A D G C. `HasMyhillProperty` returns false: the seconds C–D, D–G, G–A and A–C are 2, 5, 2 and 3 semitones, three sizes. The set is a chain of one interval, which is all that `IsWellFormed` checks, but the fourth spans two steps from A to D and one from D to G, so the chain is not well formed.

---

## 7. Proposed Experiment (Not Yet Run)

**Status: not run.** This section proposes an experiment for Learn's music-theory-ga lab, which compiles GA. The lab's GA pin would first move to `5c3a52a`, since `ScaleStructuralProperties` does not exist at `a826864`. Nothing in this section is a measurement:
- the predictions come from §3 to §6 and are written down before any run;
- the counts and scores come from the Python transcription of §6;
- a later version of this lesson will report the results.

Every step calls GA's types in the lab's own process, never a running MCP server or a language model.

1. **Three vectors.** Print `IntervalClassVector` and `IsDeepScale` for `Scale.Major`, `Scale.MajorPentatonic` and `Scale.WholeTone`. Prediction: <2 5 4 3 6 1> and true, <0 3 2 1 4 0> and false, <0 6 0 6 0 3> and false.
2. **The deep census.** For every pitch-class set, read `IsDeepScale`, and for each deep set, `IsWellFormed` and its generator. Prediction: 48 deep sets, 24 of six notes in classes 6-1 and 6-32 and 24 of seven notes in classes 7-1 and 7-35; all of them pass `IsWellFormed`, with generator 1 for the chromatic classes and 5 for the others.
3. **The common-tone theorem.** For every non-empty set and every n from 1 to 11, count the pitch classes common to the set and its transposition by n, and compare with the vector, doubled for n = 6. Prediction: no exception among the 4095 sets; for C major, the counts for n = 1 to 11 are 2 5 4 3 6 2 6 3 4 5 2.
4. **The evenness score.** Call `GetMaximalEvennessDiscrepancy` on the twelve major scales and the two whole-tone scales. Prediction, to four places:

   | Major scale | Score | Major scale | Score |
   |------|------|------|------|
   | C | 0.4041 | F♯ | 1.1780 |
   | C♯ | 0.5151 | G | 0.5151 |
   | D | 0.6389 | A♭ | 0.4041 |
   | E♭ | 0.3194 | A | 0.7693 |
   | E | 0.9035 | B♭ | 0.2857 |
   | F | 0.3194 | B | 1.0400 |

   The whole-tone scales score 0.0000 on C and 1.0000 on C♯, and 472 seven-note sets that are not maximally even score below 1.1780.
5. **Generated versus well formed.** Over all 4096 sets, the empty set included, count the sets for which `IsWellFormed` is true and `HasMyhillProperty` false, then the reverse. Prediction: 89 and 0.

### Practice Exercise

Step 4 predicts exactly 1.0000 for the whole-tone scale on C♯. Why?

> *Solution:* Its notes in ascending order are 1, 3, 5, 7, 9 and 11, and the points they are compared with are 0, 2, 4, 6, 8 and 10. Each note is one semitone from its point, so each squared difference is 1, and the root mean square of six 1s is 1.

---

## 8. Common Pitfalls

- **Taking the pattern for the set.** A natural minor and C major share a set, not a pattern.
- **Spelling with the wrong letter.** F major has B♭, not A♯: one letter per degree.
- **Taking deep for even.** The whole-tone scale is perfectly even and not deep; the deep set C D E F G A is not maximally even.
- **Counting the tritone once.** In pitch classes, a transposition by a tritone keeps twice as many notes as the set has tritones: C major and F♯ major share B and F.
- **Reading GA's `IsWellFormed` as Carey and Clampitt's well-formedness.** It checks only that a set is a chain of one interval.
- **Comparing GA's evenness scores across transpositions.** The score is measured from C: B♭ major and F♯ major are equally even and score 0.2857 and 1.1780.

---

## Key Terms

| Term | Definition |
|------|-----------|
| **Step pattern** | The semitones from each note of a scale to the next, back to the octave, such as 2 2 1 2 2 2 1 |
| **Pitch-class set** | A scale's notes without root, order or octave, such as {0, 2, 4, 5, 7, 9, 11} |
| **Interval-class vector** | The number of pairs of notes in each interval class from 1 to 6, such as <2 5 4 3 6 1> |
| **Deep scale** | A set whose vector holds six different numbers: in twelve notes, the classes 6-1, 6-32, 7-1 and 7-35 |
| **Common-tone theorem** | A transposition by n semitones keeps as many notes as the vector counts for the interval class of n, twice that for the tritone |
| **Generic interval** | The number of scale steps between two notes |
| **Myhill's property** | Every generic interval comes in exactly two sizes |
| **Maximally even** | Every generic interval comes in one size or two consecutive sizes |
| **Generated collection** | A set formed by stacking one interval, such as the chain of fifths F C G D A E B |
| **Well formed** | Generated, with the generator always spanning the same number of steps; for chains of two or more notes that are not degenerate, equivalent to Myhill's property |

---

## Self-Check Assessment

**1. Build E♭ major from its pattern and give its pitch-class set.**
> E♭ F G A♭ B♭ C D, with steps 2 2 1 2 2 2 1. With C = 0, its set is {0, 2, 3, 5, 7, 8, 10}.

**2. Why does a modulation from C major to G major change one note, while C major and F♯ major still share two?**
> G is a transposition by 7 semitones, interval class 5, and the major scale holds six intervals of class 5, so six notes stay and one changes, F to F♯. F♯ is a transposition by a tritone; the scale has one tritone, B–F, which counts from both ends, so B and F stay. Spelled in F♯ major, F is E♯.

**3. Is the major pentatonic deep? Does it have Myhill's property? Is it maximally even?**
> It is not deep: its vector <0 3 2 1 4 0> holds 0 twice. It has Myhill's property, since each generic interval comes in two sizes: 2 or 3, 4 or 5, 7 or 8, 9 or 10. It is maximally even, since each pair of sizes is consecutive.

**4. In GA at `5c3a52a`, what does `GetMaximalEvennessDiscrepancy` return for C major and for B♭ major, and what does the difference show?**
> 0.4041 and 0.2857, to four places. The two scales have the same pattern and are equally even; the score differs because it measures each set from C.

**Pass criteria:** Build and spell a scale from its pattern on any root. Compute a scale's vector and use it to count common tones, the tritone included. Say which of the deep, Myhill, maximally even and generated properties a scale has. Say what GA computes for each, and where its result depends on the transposition or differs from the definition.

---

## Research Basis

- Wikipedia, "Major scale": the two tetrachords, and maximal evenness.
- Wikipedia, "Interval vector": the definition, and the deep scale property of the major scale and its modes.
- Wikipedia, "Common tone (scale)": the common-tone theorem and its table, closely related keys, the deep scale property, generation by an interval coprime with twelve, and the whole-tone scale's transpositions; after Johnson, *Foundations of Diatonic Theory*, 2003, and Gamer, 1967.
- Wikipedia, "Generic and specific intervals": generic and specific intervals, and Myhill's property.
- Wikipedia, "Maximal evenness": Clough and Douthett's definition, the harmonic minor, the whole-tone scale, and Myhill's property as well-formedness.
- Wikipedia, "Generated collection": the chain of fifths, well-formed and degenerate collections, after Carey and Clampitt, 1989.
- Wikipedia, "Rothenberg propriety": the major scale proper but not strictly, the pentatonic strictly proper.
- GA source at commit `5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26`: every code fact in §6 links to its line.
- Learn, music-theory-ga lesson 4 at commit `0c918c8206dc9dda0241d097e6b0c65e897c92ec`: its account of `IsDeepScale`.
- Experiment: proposed in §7, not run; this lesson contains no measurement of its own.
- Provenance: hand-authored by a Claude Code session (Opus 5.5) from the Streeling curriculum plan, not produced by the Seldon course pipeline; under review.
- Belief state: T(0.85) F(0.02) U(0.10) C(0.03).
