---
module_id: mus-013-root-bass-pitch-class-set
department: music
course: Root, Bass and Pitch-Class Set
level: intermediate
alchemical_stage: albedo
prerequisites: [mus-012-chord-formulas-essential-tones-doubling, mus-020-set-classes-interval-vectors-prime-forms]
estimated_duration: "45 minutes"
produced_by: claude-code-hand-authored
version: "1.0.0"
---

# Root, Bass and Pitch-Class Set — One Set, Several Names

> **Department of Music** | Stage: Albedo (Intermediate) | Estimated duration: 45 minutes

## Objectives

After this lesson, you will be able to:
- Tell a chord's root, its bass and its pitch-class set apart, and say which of them a chord symbol, a slash and a voicing each fix
- Find every root that reads a set as a named chord, and recognise the sets that have more than one: sixth and seventh chords, sus2 and sus4, the augmented triad, the diminished seventh
- Choose between the readings by the bass, the harmony and the resolution, and write the choice as a slash chord when the bass is not the root
- Trace how GA gives each pitch-class set one name without looking at the bass, and where that name drops a tone or a spelling

---

## 1. Three Things in a Chord Name

A chord played on a guitar has three properties, and a chord name mixes them together.

- **The pitch-class set** is the chord's notes with octaves and doublings removed (MUS-020). The shape x32010 sounds C3 E3 G3 C4 E4, and its set is {C, E, G}, or {0, 4, 7} with C = 0.
- **The bass** is the lowest note that sounds: C3 in x32010. It belongs to the voicing, not to the set.
- **The root** is the note the chord is named after. For a chord built in thirds, Wikipedia's "Root (chord)" gives the method: "reorganize the pitches as a stack of thirds and then identify the lowest note in the stack." C E G is a stack of thirds on C, so its root is C, wherever C sounds.

The root need not be the bass. With the root in the bass, a chord is in root position; with another chord tone in the bass, it is in an inversion, an inversion of the chord rather than of an interval as in MUS-008. A **slash chord** writes the bass after a slash: C/E is a C major triad with E in the bass. Wikipedia's "Slash chord" adds that the slash "does not indicate 'or'". Three voicings of C major share one set:

| Shape | Notes, string 6 first | Set | Bass | Root | Symbol |
|------|------|------|------|------|------|
| x32010 | C3 E3 G3 C4 E4 | {0, 4, 7} | C | C | C |
| 032010 | E2 C3 E3 G3 C4 E4 | {0, 4, 7} | E | C | C/E |
| 332010 | G2 C3 E3 G3 C4 E4 | {0, 4, 7} | G | C | C/G |

A chord symbol fixes a root and a set. A slash adds the bass. A voicing adds octaves and doublings, and may leave tones out (MUS-012).

### Practice Exercise

Give the set, the bass, the root and the symbol of 2x0232.

> *Solution:* 2x0232 sounds F♯2 D3 A3 D4 F♯4. The set is {D, F♯, A}, or {2, 6, 9}, and the bass is F♯. The root is D, since D F♯ A is a stack of thirds on D. The symbol is D/F♯, the middle chord of the walkdown G – D/F♯ – Em that Wikipedia's "Slash chord" gives as an example.

---

## 2. One Set, Several Roots

Stacking thirds finds a single root for a triad or a seventh chord with no gap in its stack, unless the stack closes the octave: the augmented triad and the diminished seventh are stacks of thirds from any of their notes, as the third point below shows. Some sets can be read from more than one of their notes, and each reading is correct. A C E G is a stack of thirds on A, so it is the minor seventh chord Am7. It is also a C major triad with A added a sixth above C, so it is C6. Wikipedia's "Sixth chord" says of C6: "Because it is also an A minor seventh chord in first inversion, it is tonally ambiguous. Identifying the root depends on context."

| Notes | Set | Readings |
|------|------|------|
| C E G A | {0, 4, 7, 9} | C6, Am7 |
| C E♭ G A | {0, 3, 7, 9} | Cm6, Am7♭5 |
| C D G | {0, 2, 7} | Csus2, Gsus4 |
| C E G♯ | {0, 4, 8} | Caug, Eaug, A♭aug |
| C E♭ G♭ A | {0, 3, 6, 9} | Cdim7, E♭dim7, G♭dim7, Adim7 |

Each reading spells the notes its own way. As Eaug, the C of the fourth row is B♯; as A♭aug, the G♯ is A♭, which gives Wikipedia's own example of an augmented triad, A♭–C–E ("Augmented triad").

- **Sixth and seventh chords.** C6 and Am7 share a set, and so do Cm6 and Am7♭5. Wikipedia's "Sixth chord" lists more names for C E♭ G A: it "might be written as Cm6, F9, F9 (no root), Am7♭5, B7♭9, A♭Maj7♭9, or Balt". One of these is a slip: B7♭9 is B D♯ F♯ A C, with F♯ and no G, so it does not hold the set.
- **Suspended chords.** Csus2 is C D G and Gsus4 is G C D: the same three notes. For a suspended chord, "Root (chord)" says to "identify the triad that has been modified and then find its root". C D G is a C triad with D in place of E, or a G triad with C in place of B; the set does not say which.
- **Symmetric chords.** The augmented triad divides the octave into three major thirds, 4 + 4 + 4 = 12 semitones, and the diminished seventh into four minor thirds, 3 + 3 + 3 + 3 = 12. Transposing either by one of its own intervals gives the same set back (MUS-020), so each of its notes reads it as the same kind of chord. As sets, there are only four augmented triads and three diminished seventh chords; Wikipedia: "there are only three distinct diminished seventh chords (as opposed to twelve)" ("Diminished seventh chord").

For a diminished seventh chord, the same article points to the written notes: "Understanding what inversion a given diminished seventh chord is written in (and thus finding its root) depends on its enharmonic spelling." A pitch-class set has no spelling (MUS-007): {0, 3, 6, 9} is C E♭ G♭ B𝄫 as Cdim7, and A C E♭ G♭ as Adim7.

### Practice Exercise

Which notes of E G B♭ C♯ can be the root of a diminished seventh chord? Which root does the spelling E G B♭ D♭ point to?

> *Solution:* All four: the set {1, 4, 7, 10} is a stack of minor thirds from any of its notes. Spelled E G B♭ D♭, the stack starts on E: E–G, G–B♭ and B♭–D♭ are minor thirds, and D♭ is a diminished seventh above E, so the chord is Edim7. Spelled with C♯, the stack starts on C♯: C♯ E G B♭, C♯dim7.

---

## 3. Choosing Between Readings

The set gives the candidates. The bass, the harmony and the resolution choose among them.

- **The bass.** A chart usually names the reading whose root is in the bass: A C E G over A is Am7, and over C it is C6. Over any other note, a slash is needed. Am7/C is not wrong: it names the same notes with root A and bass C. Which of the two a chart writes says which root the harmony uses.
- **The harmony.** After G7 in C major, A C E G with C in the bass is the tonic, C6. In G major, between Em and D7, the same notes are the ii7 chord: Am7, written Am7/C if C is in the bass. For C E♭ G A, Wikipedia's "Sixth chord" chooses between Cm6 and F9 by "analysis of the movement of the root, in the presence of dominant-functioning harmonies".
- **The resolution.** "A common suspension is a fourth above the root resolving to the third of the chord" (Wikipedia, "Suspended chord"). D G A that resolves to D F♯ A is Dsus4, not Gsus2 over D. For a diminished seventh chord, "resolution is a better indicator of function than spelling" (Wikipedia, "Diminished seventh chord"): the chord on the leading tone of C, B D F A♭, resolves to the tonic.

Slash chords also serve arrangers. Wikipedia's "Slash chord" writes F/D for a Dm7, so that a beginner can play an F triad over D, and B°7/G for G7♭9. Both write a set as a familiar chord over a bass: F/D is D F A C, and B°7/G is G B D F A♭.

### Practice Exercise

A chart in C major ends Dm7 – G7 – ?, and the last chord is played x35555. Name it.

> *Solution:* x35555 sounds C3 G3 C4 E4 A4: the set {C, E, G, A} with C in the bass. After G7, the cadence lands on the tonic C, so the chord is C6. Am7/C names the same notes but puts the root on A.

---

## 4. Guitar Shapes With Two Names

Many common shapes hold one of the sets of §2 or a transposition of it. The chart name follows the bass and the usual resolution; the other readings need a slash.

| Shape | Notes, string 6 first | Chart name | Set | Other readings |
|------|------|------|------|------|
| x02010 | A2 E3 G3 C4 E4 | Am7 | {A, C, E, G} | C6/A |
| x35555 | C3 G3 C4 E4 A4 | C6 | {A, C, E, G} | Am7/C |
| xx0233 | D3 A3 D4 G4 | Dsus4 | {D, G, A} | Gsus2/D |
| x02230 | A2 E3 A3 D4 E4 | Asus4 | {A, D, E} | Dsus2/A |
| xx0230 | D3 A3 D4 E4 | Dsus2 | {A, D, E} | Asus4/D |
| 022200 | E2 B2 E3 A3 B3 E4 | Esus4 | {E, A, B} | Asus2/E |
| xx0101 | D3 G♯3 B3 F4 | Ddim7 | {D, F, G♯, B} | Fdim7/D, G♯dim7/D, Bdim7/D |
| 032110 | E2 C3 E3 G♯3 C4 E4 | Eaug | {E, G♯, C} | Caug/E, A♭aug/E |

The notes column names each fret with sharps; it is not the chord's spelling. As Ddim7, xx0101 is spelled D F A♭ C♭, and as Eaug, 032110 is spelled E G♯ B♯.

Two shapes, x02230 and xx0230, hold the same set {A, D, E}: only the bass and the resolution separate Asus4 from Dsus2. Each sus4 shape resolves by one fret: xx0233 to D xx0232 (G4 falls to F♯4), x02230 to A x02220 (D4 to C♯4), and 022200 to E 022100 (A3 to G♯3). The last two rows hold symmetric sets that Wikipedia uses as examples. The set of xx0101 is that of G♯dim7, "G♯–B–D–F", which "Diminished seventh chord" says is "enharmonically equivalent to three other inverted diminished chords"; the set of 032110 is that of A♭+, A♭–C–E, the example that opens "Augmented triad".

### Practice Exercise

Name 3x0013 as a chart would, and give the other reading of its set.

> *Solution:* 3x0013 sounds G2 D3 G3 C4 G4: the set {G, C, D} with G in the bass. A chart names it Gsus4, since the C usually falls to B and gives G. The same set is Csus2, written over this bass Csus2/G.

---

## 5. Where GA Stands

GA is the music-theory library and chatbot of the GuitarAlchemist ecosystem. The facts below are read from its code at commit [`5c3a52a`](https://github.com/GuitarAlchemist/ga/tree/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26). This lesson documents that code and does not change it. It has not run GA or its tests. The files it cites are unchanged on GA's `main` at `ba3b9ac`. Learn, the ecosystem's course site, has a music-theory-ga course whose lessons compile an earlier version of GA, `a826864`; the recogniser's files have changed since. Its lesson 3 [names a shape](https://github.com/spareilleux/learn/blob/89dc3e64d392cdc36844b03719880484d823b4d7/src/content/docs/music-theory-ga/03-chords-and-voicings.mdx#L240) by trying the bass first, as a chart does, and asks GA's catalogue for the intervals measured from the bass. This lesson follows GA's chord recogniser, which chooses the root itself.

**GA names a pitch-class set without its bass.** [`CanonicalChordRecognizer.Identify`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Services/Chords/CanonicalChordRecognizer.cs#L26-L39) takes a set and an optional bass. Its comment says that ["Everything except the slash suffix is a function of the pitch-class set alone"](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Services/Chords/CanonicalChordRecognizer.cs#L30-L31), and the method keeps [one answer per set](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Services/Chords/CanonicalChordRecognizer.cs#L34). For three pitch classes or more:
- every note of the set is tried as the root against every pattern of the catalogue, and a pattern may [miss one interval and add one](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Services/Chords/CanonicalChordRecognizer.cs#L153-L166);
- the candidates are [ranked](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Services/Chords/CanonicalChordRecognizer.cs#L178-L183) by distance (missing plus extra intervals), then by having nothing missing, then by the pattern's priority (lower number first), then by a [root-commonness score](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Services/Chords/CanonicalChordRecognizer.cs#L362-L377): C scores 0, G and F 1, D and B♭ 2, A and E♭ 3, and so on;
- ["the bass note must NOT influence which pattern wins"](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Services/Chords/CanonicalChordRecognizer.cs#L171-L173);
- a bass that differs from the root is added afterwards as a [slash suffix](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Services/Chords/CanonicalChordRecognizer.cs#L35-L38).

A test runs [all 4096 sets with each of the 12 basses](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Tests/Common/GA.Business.Core.Tests/Chords/CanonicalChordRecognizerCacheTests.cs#L24-L46) and checks that the bass changes nothing but the suffix. GA's voicing analyser passes the voicing's [lowest note as the bass](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Services/Fretboard/Voicings/Analysis/VoicingHarmonicAnalyzer.cs#L12-L17) and keeps [the name with its suffix](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Services/Fretboard/Voicings/Analysis/VoicingHarmonicAnalyzer.cs#L72-L80) as the voicing's chord name.

**A C E G is always Am7.** Minor-7 has [priority 5](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Harmony/CanonicalChordPatternCatalog.cs#L63) and major-6 [priority 10](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Harmony/CanonicalChordPatternCatalog.cs#L55). Both readings are exact, so Am7 wins whatever the bass, and the C6 shape x35555 is named `Am7/C`. The round-trip test's list of exclusions says so: ["major-6 [0,4,7,9] ≡ minor-7 at root 9 (priority 5 beats 10)"](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Tests/Common/GA.Business.Core.Tests/Voicings/ChordRecognitionRoundTripTests.cs#L39). Its golden corpus expects [Am7 for x02010](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Tests/Common/GA.Business.Core.Tests/Voicings/ChordRecognitionRoundTripTests.cs#L424-L426). The recogniser cannot give the C6 of §3's cadence.

**Ties go to the commoner root.** sus2 and sus4 both have [priority 8](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Harmony/CanonicalChordPatternCatalog.cs#L51-L52), so between two readings of a sus set the root-commonness score decides. G scores 1 and D 2, so Dsus4 xx0233 is named `Gsus2/D`. The golden corpus [expects Gsus2](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Tests/Common/GA.Business.Core.Tests/Voicings/ChordRecognitionRoundTripTests.cs#L451-L456), and its comment explains the choice as sus4 at D "(prio 8)" against sus2 at G "(prio 7)". The catalogue gives both 8: the root score breaks the tie, not the priority. The same comment says that the guitarist's "Dsus4" is "recovered" as `Gsus2/D`; that is the other reading of §4's table, not the chart name. Csus4 and Dsus2 [come out as charted](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Tests/Common/GA.Business.Core.Tests/Voicings/ChordRecognitionRoundTripTests.cs#L443-L449), because C scores lower than F and D lower than A. The diminished seventh has [priority 7](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Harmony/CanonicalChordPatternCatalog.cs#L66) at each of its four roots, and the augmented triad [priority 3](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Harmony/CanonicalChordPatternCatalog.cs#L50) at each of its three, so the root score alone names them.

**Names are spelled with flats.** Roots and slash suffixes come from one [list of twelve names](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Services/Chords/CanonicalChordRecognizer.cs#L379-L383), C, Db, D, Eb, E, F, Gb, G, Ab, A, Bb, B, which also builds the [suffixes](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Services/Chords/CanonicalChordRecognizer.cs#L51-L52). An F♯ minor chord is `Gbm`, and the walkdown's D/F♯ is `D/Gb`. The recogniser works on pitch classes, which carry no spelling (MUS-007), so the clue that Wikipedia gives for a diminished seventh's root is not available to it.

**One name hides the ninth.** The catalogue lists the set C D E G A twice: as [major-6-add-9, priority 12](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Harmony/CanonicalChordPatternCatalog.cs#L57), and as [6-9, priority 54](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Harmony/CanonicalChordPatternCatalog.cs#L111). Its remarks call the two names [synonyms](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Harmony/CanonicalChordPatternCatalog.cs#L166-L168). The suffix builder has a case for ["6-9"](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Services/Chords/CanonicalChordRecognizer.cs#L281) but none for major-6-add-9. That pattern gets its [quality, extension and alterations](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Services/Chords/CanonicalChordRecognizer.cs#L293) in a row: nothing for major, "6" for the sixth, and nothing for "add9", an [alteration that prints as nothing](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Services/Chords/CanonicalChordRecognizer.cs#L307). Read, not run: C D E G A has five exact readings, C major-6-add-9, D 9-sus4, D dominant-11, C 6-9 and E quartal-5. The first has the lowest priority, so the recogniser names the set `C6`. Minor-6-add-9 likewise turns C D E♭ G A into `Cm6`. Since A C E G is Am7, a `C6` from the recogniser is never the C6 of §2: it holds a ninth. The round-trip test checks each pattern's name, distance, root and exact flag, [but not the name it prints](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Tests/Common/GA.Business.Core.Tests/Voicings/ChordRecognitionRoundTripTests.cs#L134-L142), so it passes.

**The test's symmetric example is not symmetric.** The list of exclusions says that ["dominant-7-sharp-5 [0,4,8,10] is T4-symmetric — multiple roots, same set"](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Tests/Common/GA.Business.Core.Tests/Voicings/ChordRecognitionRoundTripTests.cs#L43). Transposed by 4 semitones, C E G♯ B♭ becomes E G♯ C D, a different set. Its only exact readings are at C, under two names for the same intervals, [augmented-7](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Harmony/CanonicalChordPatternCatalog.cs#L68) and [dominant-7-sharp-5](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Harmony/CanonicalChordPatternCatalog.cs#L95). The round trip returns augmented-7, priority 8 before 30, and the exclusion holds for that reason. The catalogue's four-note chords do hold two symmetric sets: the diminished seventh of §2, and [dominant-7-b5](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Harmony/CanonicalChordPatternCatalog.cs#L94), C E G♭ B♭, which a transposition by a tritone maps to itself: C7♭5 is also G♭7♭5.

**Unmatched sets get a Forte name and no root.** A set that no pattern fits within one missing and one extra interval is named by its [Forte number](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Services/Chords/CanonicalChordRecognizer.cs#L320-L356), with no root, and [only a pattern match](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Services/Chords/CanonicalChordRecognizer.cs#L43-L44) can carry a slash suffix. For such a set, GA's voicing analyser [stores the bass as the voicing's root](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Services/Fretboard/Voicings/Analysis/VoicingHarmonicAnalyzer.cs#L84), written by [`PitchClass.ToString`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Atonal/PitchClass.cs#L83-L88) as a number, with T for 10 and E for 11, where a matched set stores a note name. The chord name is unaffected. MUS-020 covers Forte's catalogue.

Fixing any of this is for GA's owners; this lesson only describes it.

### Practice Exercise

By GA's ranking, what does `Identify` return for C D G with G in the bass, and for E G♯ C with E in the bass?

> *Solution:* For C D G, Csus2 and Gsus4 are both exact at priority 8, and C scores 0 against G's 1, so the root is C. G is not the root, so the name is `Csus2/G`. For E G♯ C, Caug, Eaug and Abaug are exact at priority 3; C scores 0, E and A♭ 4, so the name is `Caug/E`.

---

## 6. Proposed Experiment (Not Yet Run)

**Status: not run.** This section proposes an experiment for Learn's music-theory-ga lab, which compiles GA. The lab's GA pin would first move to `5c3a52a`. Nothing in this section is a measurement:
- the predictions come from §2 to §5 and are written down before any run;
- the names and counts come from a line-by-line Python transcription of the recogniser and its pattern catalogue;
- a later version of this lesson will report the results.

Every step calls GA's types in the lab's own process, never a running MCP server or a language model.

1. **The bass changes only the suffix.** For the eight shapes of §4 and four more, call `Identify` with the set alone, then with the shape's bass. Prediction:

   | Shape | Without the bass | With the bass |
   |------|------|------|
   | x02010 | Am7 | Am7 |
   | x35555 | Am7 | Am7/C |
   | xx0233 | Gsus2 | Gsus2/D |
   | x02230 | Dsus2 | Dsus2/A |
   | xx0230 | Dsus2 | Dsus2 |
   | 022200 | Asus2 | Asus2/E |
   | xx0101 | Fdim7 | Fdim7/D |
   | 032110 | Caug | Caug/E |
   | 3x0013 | Csus2 | Csus2/G |
   | x03221 | Faug | Faug/A |
   | 244222 | Gbm | Gbm |
   | 2x0232 | D | D/Gb |

2. **The census.** For each of the 4096 sets, call `Identify` and record `MatchDistance`. For each set of three pitch classes or more, count the roots at which some pattern of the catalogue matches exactly. Prediction:
   - of the 4017 sets of three pitch classes or more, 484 match exactly, 1644 at distance 1 and 648 at distance 2, and 1241 fall back to a Forte name;
   - the only four-note sets that fall back are the six transpositions of C D♭ G♭ G;
   - 124 sets have exact readings at two roots or more. Up to transposition they are 15: the sus2 set, the 7sus4 set, the 7sus2 set, m7♭5, m7, 7♭5, the augmented triad, the diminished seventh, 7♭9♯9, the 6/9 set, m11, 7♭9♯11, and the augmented, whole-tone and octatonic scales.
3. **The sixth chords.** Count the sets whose name ends in `6` but not `m6`, and those whose name ends in `m6`, and check each for the ninth above its root; count the names that end in `6/9`. Prediction: 48 and 60 sets, every one with its ninth, and no set named 6/9 or m6/9. A C E G is named Am7, and C E♭ G A Am7b5.
4. **The symmetric example.** Identify C E G♯ B♭ and its transposition by 4 semitones, then C E G♭ B♭ and its transposition by 6. Prediction: `Caug7` and `Eaug7`, two different sets; `C7b5` both times, one set.

### Practice Exercise

Step 2 predicts 124 sets with exact readings at two roots or more, from 15 sets up to transposition. Why do the augmented triad and the diminished seventh account for only 4 and 3 sets, where A C E G and its transpositions account for 12?

> *Solution:* A set that maps to itself under a transposition has fewer distinct transpositions. The augmented triad maps to itself by 4 semitones, so it has 12 / 3 = 4 transpositions; the diminished seventh maps to itself by 3 semitones, so it has 12 / 4 = 3. A C E G maps to itself under no transposition but T0, so it has 12.

---

## 7. Common Pitfalls

- **Taking the bass for the root.** C/E has root C; the bass is a property of the voicing.
- **Reading the slash as "or".** C/E means a C chord over E.
- **Calling one reading wrong.** C6 and Am7/C are the same notes; the harmony decides which root to name.
- **Naming a diminished seventh by its set.** Each of its notes can be the root; the spelling and the resolution decide.
- **Trusting GA's `C6`.** From the recogniser, it holds a ninth: it is a 6/9 chord.
- **Taking GA's slash name for the chart name.** `Gsus2/D` is the other reading of Dsus4, chosen by GA's root-commonness score.

---

## Key Terms

| Term | Definition |
|------|-----------|
| **Pitch-class set** | A chord's notes with octaves and doublings removed, such as {0, 4, 7} |
| **Bass** | The lowest note that sounds; a property of the voicing |
| **Root** | The note a chord is named after; for a chord in thirds, the lowest note of the stack of thirds |
| **Inversion** | A voicing of a chord with a chord tone other than the root in the bass |
| **Slash chord** | A chord symbol followed by its bass, such as C/E |
| **Reading** | A root and a chord type that together give exactly a set: C6 and Am7 are two readings of A C E G |
| **Symmetric chord** | A chord whose set maps to itself under a transposition other than T0, such as the augmented triad and the diminished seventh |
| **Root commonness** | GA's tie-break between equally good readings: C first, then G and F, then D and B♭, and so on |

---

## Self-Check Assessment

**1. Give the set, the bass and the two readings of 8x798x, and the name a chart would write after G7 in C major.**
> 8x798x sounds C3 A3 E4 G4: the set {C, E, G, A}, with C in the bass. The readings are C6 and Am7, written over this bass C6 and Am7/C. After G7 in C major, the chart writes C6.

**2. Why can any note of a diminished seventh chord be its root, and what tells the root in written music?**
> Its four notes divide the octave into four minor thirds, so the set is the same stack of minor thirds from each of them. The spelling tells the root, where the written stack of thirds starts, and the resolution tells the function.

**3. Why does GA name Asus4 x02230 `Dsus2/A`?**
> Its set {A, D, E} is exactly Asus4 and exactly Dsus2. Both patterns have priority 8, and the root-commonness score prefers D (2) to A (3). A, the bass, is not that root, so GA adds `/A`.

**4. In GA at `5c3a52a`, what does a `C6` from the recogniser contain, and why?**
> C, D, E, G and A, the ninth included. GA names the 6/9 set by its pattern major-6-add-9, whose "add9" prints as nothing. The plain C6, A C E G, is always Am7.

**Pass criteria:** Tell the root, the bass and the set apart in any voicing. List the readings of a set, including the symmetric ones. Choose a reading by the bass, the harmony and the resolution, and write it as a slash chord when needed. Say how GA names a set, and where its name differs from a chart's.

---

## Research Basis

- Wikipedia, "Root (chord)": the stack-of-thirds method and the root of a suspended chord.
- Wikipedia, "Slash chord": the slash, which "does not indicate 'or'", the walkdown, and arrangers' slash chords.
- Wikipedia, "Sixth chord": C6 as Am7 in first inversion, and the names of C E♭ G A.
- Wikipedia, "Suspended chord": the fourth resolving to the third.
- Wikipedia, "Diminished seventh chord": the three distinct chords, the root by spelling, and resolution over spelling.
- Wikipedia, "Augmented triad": A♭+ spelled A♭–C–E.
- GA source at commit `5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26`: every code fact in §5 links to its line.
- Learn, music-theory-ga lesson 3 at commit `89dc3e64d392cdc36844b03719880484d823b4d7`: how its lab names a shape.
- Experiment: proposed in §6, not run; this lesson contains no measurement of its own.
- Provenance: hand-authored by a Claude Code session (Opus 5.5) from the Streeling curriculum plan, not produced by the Seldon course pipeline; under review.
- Belief state: T(0.85) F(0.02) U(0.10) C(0.03).
