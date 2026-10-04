---
module_id: mus-014-inversions-bass-line
department: music
course: Inversions and the Bass Line
level: intermediate
alchemical_stage: albedo
prerequisites: [mus-013-root-bass-pitch-class-set]
estimated_duration: "45 minutes"
produced_by: claude-code-hand-authored
version: "1.0.0"
---

# Inversions and the Bass Line — Same Notes, Different Bass

> **Department of Music** | Stage: Albedo (Intermediate) | Estimated duration: 45 minutes

## Objectives

After this lesson, you will be able to:
- Name a chord's position from its bass alone: root position, first, second or third inversion
- Write the figured-bass figure of each position of a triad and a seventh chord, and tell the figure 6 from the jazz C6
- Recognise the four kinds of six-four chord and play each on the guitar
- Say where a position cannot be read from the sounding notes alone, and trace how GA handles inversions in its `Chord` type, its voicing documents and its catalogue of modes

---

## 1. Same Notes, Different Bass

MUS-013 separated a chord's root from its bass. The **position** of a chord says which of its tones is in the bass. Wikipedia's "Inversion (music)": "A chord's inversion describes the relationship of its lowest notes to the other notes in the chord." With the root in the bass, the chord is in root position; with another tone, it is in an inversion. "The inversions are numbered in the order their lowest notes appear in a close root-position chord (from bottom to top)": the third gives the first inversion, the fifth the second, and in a seventh chord the seventh gives the third. A chord of three notes has two inversions; "Chords with four notes (such as seventh chords) work in a similar way, except that they have three inversions". The same article notes that some texts keep "inversion" for a bass other than the root and use **position** for all the cases; this lesson does the same.

| Position | Bass | Close position | Above the bass (semitones) |
|------|------|------|------|
| Root position | C, the root | C E G | major third (4), perfect fifth (7) |
| First inversion | E, the third | E G C | minor third (3), minor sixth (8) |
| Second inversion | G, the fifth | G C E | perfect fourth (5), major sixth (9) |

The intervals above the bass change with the position, which is why each one sounds different: Wikipedia gives the first inversion "the intervals of a minor third and a minor sixth above the inverted bass of E". The root does not change. In his *Treatise on Harmony* (1722), Rameau treated the positions of a chord as "functionally equivalent" ("Inversion (music)").

Only the bass counts. The order of the notes above it, their octaves and their doublings do not change the position. On the top three strings, the close positions of C are rotations of one another:

| Shape | Notes, string 6 first | Bass | Position |
|------|------|------|------|
| xxx553 | C4 E4 G4 | C | root position |
| xxx988 | E4 G4 C5 | E | first inversion |
| xxx010 | G3 C4 E4 | G | second inversion |

The open shapes x32010, 032010 and 332010 of MUS-013 hold the same three positions with five or six strings. Inversions also let a bass line move by step while the chords change: C – G/B – Am, played x32010 – x20003 – x02210, walks the bass down C3, B2, A2, with G in first inversion.

### Practice Exercise

Give the position of 2x0232 and of x00232.

> *Solution:* 2x0232 sounds F♯2 D3 A3 D4 F♯4. The chord is D major, and F♯, its third, is in the bass: first inversion. x00232 sounds A2 D3 A3 D4 F♯4: A, the fifth, is in the bass, so this is the second inversion, D/A.

---

## 2. Figured Bass

Figured bass writes a chord as numbers set beside its bass. Wikipedia's "Figured bass" places them "above or below (or next to) a bass note": "The numbers indicate the number of scale steps above the given bass-line that a note should be played." Steps are counted by letter names, as for interval numbers (MUS-008): over G, C is a fourth (G A B C) and E a sixth. The figures "do not express notes in upper voices that double, or are unison with, the bass note" ("Inversion (music)"), and they usually ignore octaves, so a figure names a position, not a voicing.

Each position has a full figure and a usual abbreviation. Root-position triads "appear without symbols (the 53 is understood)", and "first-inversion triads are customarily abbreviated as just 6" ("Inversion (music)"):

| Triad position | Full figure | Written |
|------|------|------|
| Root position | 5/3 | nothing |
| First inversion | 6/3 | 6 |
| Second inversion | 6/4 | 6/4 |

For seventh chords, "Seventh chord" lists the four positions of G7, G B D F, with V7, V6/5, V4/3 and V4/2 or V2:

| Position | Bass | Close position | Full figure | Written |
|------|------|------|------|------|
| Root position | G | G B D F | 7/5/3 | 7 |
| First inversion | B | B D F G | 6/5/3 | 6/5 |
| Second inversion | D | D F G B | 6/4/3 | 4/3 |
| Third inversion | F | F G B D | 6/4/2 | 4/2 or 2 |

"Figured bass" confirms the last line: a 2 alone or 4/2 stands for 6/4/2. In analysis the figure follows a Roman numeral: "the term I6 refers to a tonic triad in first inversion" ("Inversion (music)"). It can also follow a bass note: a C major triad over G "would be written G64", and over E "E63 or E6 (this is different from the jazz notation, where a C6 means the added sixth chord C–E–G–A, i.e., a C major with an added 6th degree)" ("Figured bass"). Quoted as plain text, the stacked figures run together: G64 is G with 6/4, E63 is E with 6/3, and 53 is 5/3. A chart's C6 is a four-note chord with C in the bass; the figure E6 is a C triad with E in the bass.

### Practice Exercise

Write the figure of each chord over its bass: D/A, Am/C, G7/D, G7/F.

> *Solution:* D/A: over A, D is a fourth and F♯ a sixth, so 6/4: the triad has its fifth in the bass. Am/C: over C, E is a third and A a sixth, so 6. G7/D: over D, F is a third, G a fourth and B a sixth, so 6/4/3, written 4/3. G7/F: over F, G is a second, B a fourth and D a sixth, so 6/4/2, written 4/2 or 2.

---

## 3. The Six-Four Chord

Of a triad's positions, only the second inversion puts a fourth above the bass. Wikipedia's "Six-four chord": "the bass note and the root of the chord are a fourth apart (or a corresponding compound interval) which traditionally qualifies as a dissonance. There is therefore a tendency for movement and resolution." The voicing above the bass is free: "Note that any voicing above the bass is allowed." A six-four chord is rarely a resting point, and the same article sorts its uses: "There are four types of second-inversion chords: cadential, passing, auxiliary, and bass arpeggiation."

| Type | In C major | Shapes | What moves |
|------|------|------|------|
| Cadential | C/G – G – C, I6/4 – V – I | 332010 – 320003 – x32010 | Over G2, C3 falls to B2 and E3 to D3: the fourth and the sixth fall to the third and the fifth |
| Passing | C – G/D – C/E, I – V6/4 – I6 | x32010 – xx0003 – xx2010 | The bass steps C3, D3, E3; the open G3 holds |
| Neighbour (pedal, auxiliary) | C – F/C – C, I – IV6/4 – I | x32010 – x33211 – x32010 | Over C3, E3 rises to F3 and G3 to A3, then both fall back |
| Bass arpeggiation | C – C/E – C/G | x32010 – 032010 – 332010 | The bass moves C3, E2, G2 under one chord |

- **Cadential.** "Six-four chord" gives two readings. One, found in most older harmony textbooks, calls the chord a tonic in second inversion, I6/4 – V – I. The other, which several modern textbooks prefer, hears the dominant with "a double appoggiatura on the V that resolves down by step", written V6/4 – 5/3: the bass G is already the dominant, and C and E are dissonances that resolve to B and D.
- **Passing.** In a passing six-four, "the bass passes between two tones a third apart", and the chord, set between two more stable chords, falls "on the weaker beat between these two chords".
- **Neighbour.** The IV6/4 harmonises a neighbour note: "the third and fifth rise a step each and then fall back".
- **Bass arpeggiation.** The bass runs through the root, third and fifth of one chord; the fifth in the bass makes a six-four, but nothing needs to resolve.

### Practice Exercise

A progression in C major runs Am – C/G – G7 – C. What kind of six-four is C/G, and how can it be read?

> *Solution:* It is a cadential six-four: it falls before the dominant of a cadence. One reading calls it I6/4, the tonic in second inversion. The other hears the dominant already in the bass, G, with C and E as a double appoggiatura that falls to B and D: V6/4 – 5/3, with G7 adding its seventh, F, on the resolution.

---

## 4. Where the Notes Do Not Decide

A position is measured from a root, and the sounding notes do not always fix the root.

- **Two readings, two positions.** MUS-013 showed that C E G A is both C6 and Am7. Over C, it is C6 in root position, or Am7/C in first inversion. Figured bass names no root and writes the same figure for both: over C, E is a third, G a fifth and A a sixth, so 6/5, the figure of a first-inversion seventh chord.
- **The spelling decides the figure.** Figures count letters, and a symmetric chord can be spelled from any of its notes. E G♯ C over E is the augmented triad Caug in first inversion: E to C is a sixth, so the figure is 6. Spelled E G♯ B♯, it is Eaug in root position: E to B♯ is a fifth, so the figure is 5/3. Both are 8 semitones.
- **The diminished seventh.** In every position of B D F A♭, the notes above the bass lie 3, 6 and 9 semitones up, so the sound does not show the position. The letters do: B D F A♭ is 7/5/3, D F A♭ B 6/5/3, F A♭ B D 6/4/3, and A♭ B D F 6/4/2. As MUS-013 quoted from "Diminished seventh chord": "Understanding what inversion a given diminished seventh chord is written in (and thus finding its root) depends on its enharmonic spelling."

### Practice Exercise

Give the figure and the position of A♭ B D F over A♭, and of the same sound spelled G♯ B D F over G♯.

> *Solution:* Over A♭, B is a second (A B), D a fourth and F a sixth: 6/4/2, the third inversion of B°7, B D F A♭. Over G♯, B is a third, D a fifth and F a seventh (G to F): 7/5/3, G♯°7 in root position.

---

## 5. Where GA Stands

GA is the music-theory library and chatbot of the GuitarAlchemist ecosystem. The facts below are read from its code at commit [`5c3a52a`](https://github.com/GuitarAlchemist/ga/tree/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26). This lesson documents that code and does not change it. It has not run GA or its tests. The files it cites are unchanged on GA's `main` at `e610b77`, except two: in `Modes.yaml` the cited lines are unchanged, and in `ModesSkill.cs` the cited code is unchanged but at other line numbers. This lesson follows inversions through three places in GA.

**`Chord` counts by rotation.** [`Bass`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Harmony/Chord.cs#L260-L263) is `Notes[0]`, documented as the "lowest note in the voicing". [`GetInversion`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Harmony/Chord.cs#L281-L298) returns 0 when the bass is the root; otherwise it finds the root in the list of notes and returns how many notes run from the root to the end of the list. [`ToInversion`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Harmony/Chord.cs#L300-L320) rotates the list. A chord built from a symbol lists its notes in the [order of its formula](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Harmony/Chord.cs#L25-L43), C E G for C, so the rotations E G C and G C E count 1 and 2. The tests [`Inversions_ShouldWorkCorrectly`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Tests/GA.Domain.Core.Tests/Theory/Harmony/ChordTests.cs#L123-L143) and [`ToInversion_PreservesFormulaAndSymbol`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Tests/GA.Domain.Core.Tests/CoreHardeningRegressionTests.cs#L134-L154) check this for C, Cm, Cmaj7, C9 and C13.

Learn, the ecosystem's course site, has a music-theory-ga course whose lab compiles an earlier version of GA, `a826864`. Its [lesson 3](https://github.com/spareilleux/learn/blob/aaf6d3e52490d159ab962c75928e88c0dae28c28/src/content/docs/music-theory-ga/03-chords-and-voicings.mdx#L174-L195) found that `ToInversion` analysed the rotated notes again and lost the third of a first inversion, printing the quality `Other` for C/E. At `5c3a52a`, `ToInversion` goes through a [private constructor](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Harmony/Chord.cs#L64-L71) that copies the root, the formula, the symbol and the set, and replaces only the notes. Two facts matter for inversions:
- **The symbol has no slash.** The first inversion of C has bass E and prints `C`, since the constructor copies the symbol: [`ToString`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Harmony/Chord.cs#L367) returns the symbol, and the test [asserts it unchanged](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Tests/GA.Domain.Core.Tests/CoreHardeningRegressionTests.cs#L149).
- **Equality ignores the bass.** [`Equals`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Harmony/Chord.cs#L277) and [`GetHashCode`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Harmony/Chord.cs#L365) compare the set and the root only, so C equals its inversions, as Rameau would have it.

**Notes in another order are miscounted.** The [constructor from notes](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Harmony/Chord.cs#L48-L62) keeps the notes in the order given. Read, not run, with root C:

| Notes | Bass | Position | `GetInversion` |
|------|------|------|------|
| E G C | E, the third | first inversion | 1 |
| E C G | E, the third | first inversion | 2 |
| G C E | G, the fifth | second inversion | 2 |
| G E C | G, the fifth | second inversion | 1 |

`GetInversion` looks only at where the root first falls in the list, and counts the notes from there to the end. In close position, that count equals the inversion; other orders and doublings can change it: E G C E, in close order with E doubled on top, counts 2. A root-position chord counts 0 in any order, since the bass is the root. `ToInversion` inherits the error: from E C G, `ToInversion(1)` returns G E C, with the fifth in the bass, and `GetInversion` then says 1. The [test of this constructor](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Tests/GA.Domain.Core.Tests/CoreHardeningRegressionTests.cs#L156-L162) passes E G C, an order that counts right, and checks the quality and the formula, not the inversion. Learn's lesson 3 calls `GetInversion` right; it is, for the rotations that lesson tests.

**The voicing document counts semitones.** GA describes a voicing with a document for its search. [`VoicingDocumentFactory`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Business.ML/Rag/VoicingDocumentFactory.cs#L22-L28) takes the lowest note as the bass and the root of the chord recogniser of MUS-013 as the root, through [`TryGetRootPitchClass`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Business.ML/Musical/Analysis/ChordIdentificationExtensions.cs#L19-L29). [`CalculateInversion`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Business.ML/Rag/VoicingDocumentFactory.cs#L88-L96) then maps the semitones from the root up to the bass: 0 to root position; 3 or 4 to 1; 6 or 7 to 2; 10 or 11 to 3; any other distance to −1. Read, not run, with the recogniser's names transcribed from its code; as in MUS-013, the notes column names each fret with sharps:

| Shape | Chart name | Notes, string 6 first | Recogniser's name | Bass above GA's root | Inversion |
|------|------|------|------|------|------|
| 032010 | C/E | E2 C3 E3 G3 C4 E4 | `C/E` | 4 | 1 |
| 332010 | C/G | G2 C3 E3 G3 C4 E4 | `C/G` | 7 | 2 |
| 1x0003 | G7/F | F2 D3 G3 B3 G4 | `G7/F` | 10 | 3 |
| x35555 | C6 | C3 G3 C4 E4 A4 | `Am7/C` | 3 | 1 |
| xx0233 | Dsus4 | D3 A3 D4 G4 | `Gsus2/D` | 7 | 2 |
| 032110 | Eaug | E2 C3 E3 G♯3 C4 E4 | `Caug/E` | 4 | 1 |
| 4x2110 | A♭aug | G♯2 E3 G♯3 C4 E4 | `Caug/Ab` | 8 | −1 |
| xx0101 | Ddim7 | D3 G♯3 B3 F4 | `Fdim7/D` | 9 | −1 |

- **The number follows GA's root.** The chart's C6 and Dsus4 are in root position; GA reads them as Am7 and Gsus2, so it gives 1 and 2. Eaug, A♭aug and Ddim7 are in root position on a chart too, but GA measures them from C, C and F.
- **The document drops the slash.** Its `ChordName` [prefers the recogniser's canonical name](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Business.ML/Rag/VoicingDocumentFactory.cs#L43-L46), which the slash name [only extends](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Services/Chords/CanonicalChordRecognizer.cs#L417-L419): the document for 032010 is named `C`, and the one for 4x2110 `Caug`.
- **Two triad and seventh-chord distances are missing.** An augmented triad with its fifth in the bass has that bass 8 semitones above the root, and a diminished seventh with its seventh in the bass has it 9 above: both get −1, where the readings GA chose make them second and third inversions. So does any bass 1, 2 or 5 semitones above the root.
- **The consumers read it as it is.** When GA's search service indexes documents, it [copies each inversion](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Business.ML/Search/EnhancedVoicingSearchService.cs#L120) into the entry, and [`VoicingFilterEngine`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Business.ML/Search/VoicingFilterEngine.cs#L105) keeps an entry only if its inversion equals the filter's, so a search for second inversions skips 4x2110. [`AutoTaggingService`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Business.ML/Musical/Enrichment/AutoTaggingService.cs#L164-L168) adds an `Inversion:n` tag only when n is above 0, so a −1 gets no tag, like a root position.
- **The tests stop at C/E.** The factory's test [expects 1 for C/E and 0 for four root-position shapes](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Tests/Common/GA.Business.ML.Tests/Unit/VoicingDocumentFactoryTests.cs#L21-L25). A search test filters for 2, on a [fixture document](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Tests/Common/GA.Business.Core.Tests/Fretboard/Voicings/Search/SemanticSearchTestFixture.cs#L243-L246) whose inversion is set by hand. An indexing test [passes 100 generated voicings to the indexer](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Tests/Common/GA.Business.Core.Tests/Fretboard/Voicings/Search/VoicingIndexingServiceTests.cs#L18-L34), which builds documents through the factory, but it asserts no inversion. No test checks what `CalculateInversion` gives for a second or third inversion, or for a distance it maps to −1.

**The catalogue's triad inversions are mislabelled.** GA's `Modes.yaml` lists the triads as [modal families](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Business.Config/Modes.yaml#L424-L492), each with entries named as inversions, all with C in the bass:

| Entry | Notes | Alias | What the notes are | Figure |
|------|------|------|------|------|
| [Minor Triad First Inversion](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Business.Config/Modes.yaml#L432-L436) | C E♭ A♭ | Minor 6/4 | A♭ major, first inversion | 6 |
| [Minor Triad Second Inversion](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Business.Config/Modes.yaml#L437-L441) | C F A | Minor 6/4 | F major, second inversion | 6/4 |
| [Major Triad First Inversion](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Business.Config/Modes.yaml#L442-L446) | C F A♭ | Major 6/4 | F minor, second inversion | 6/4 |
| [Major Triad Second Inversion](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Business.Config/Modes.yaml#L447-L451) | C E A | Major 6/4 | A minor, first inversion | 6 |
| [Diminished Triad First Inversion](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Business.Config/Modes.yaml#L465-L469) | C E A | Diminished 6/4 | A minor, first inversion | 6 |
| [Diminished Triad Second Inversion](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Business.Config/Modes.yaml#L470-L474) | C F♯ B♭ | Diminished 6/4 | no triad: set class 3-8 | — |
| [Augmented Triad First Inversion](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Business.Config/Modes.yaml#L483-L487) | C F A | Augmented 6/4 | F major, second inversion | 6/4 |
| [Augmented Triad Second Inversion](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Business.Config/Modes.yaml#L488-L492) | C E♭ F♯ | Augmented 6/4 | C diminished, root position, spelled C E♭ G♭ | 5/3 |

No entry names its notes. The major family holds the right four sets, the inversions of A♭ and F major and of A and F minor over C, under swapped names. The other two families hold other triads, and one set that is not a triad. Every alias says 6/4, but only three of the eight entries are six-four chords. Over C, the diminished triad's inversions are C E♭ A and C F♯ A, and the augmented triad is C E G♯ in every position, respelled (§4). The last row's figure also needs the respelling: as written, F♯ is a fourth above C. The augmented family's interval vector, [<0 1 0 0 2 0>](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Business.Config/Modes.yaml#L476), is not the augmented triad's <0 0 0 3 0 0> either.

`AtonalModalFamilies.yaml` [imports these names by set](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Business.Config/AtonalModalFamilies.yaml#L9-L10). The major-triad family gets [the four names](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Business.Config/AtonalModalFamilies.yaml#L185-L204). The true inversions of the diminished triad, {0, 3, 9} and {0, 6, 9}, [get none](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Business.Config/AtonalModalFamilies.yaml#L220-L229). {0, 6, 10} [carries "Diminished Triad Second Inversion"](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Business.Config/AtonalModalFamilies.yaml#L290-L294), which also gives its family [the name "Diminished Triad Family"](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Business.Config/AtonalModalFamilies.yaml#L256-L259), the name of [the real one](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Business.Config/AtonalModalFamilies.yaml#L206-L207). The file also numbers these two families [3-5](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Business.Config/AtonalModalFamilies.yaml#L258) and [3-3](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Business.Config/AtonalModalFamilies.yaml#L208), where Forte's list has 3-8 and 3-10. When GA's `ModesSkill` finds an interval vector in a question, it [answers from this file](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Business.ML/Agents/Skills/ModesSkill.cs#L560-L568) [before anything else](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Business.ML/Agents/Skills/ModesSkill.cs#L156-L164), and [lists each mode of the family](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Business.ML/Agents/Skills/ModesSkill.cs#L628-L656) by this name with its pitch classes, at confidence 1.0.

Fixing any of this is for GA's owners; this lesson only describes it.

### Practice Exercise

In GA at `5c3a52a`, what bass, inversion number and printed name does the third inversion of `Chord.FromSymbol("G7")` have? What inversion does the voicing document give G7/F, 1x0003?

> *Solution:* The notes G B D F rotate to F G B D: bass F, `GetInversion` 3, and the chord prints `G7`, since the symbol is kept. For 1x0003, the recogniser names `G7/F`; F is 10 semitones above G, so `CalculateInversion` gives 3. Both say third inversion, and neither name shows the bass: the document is named `G7` too.

---

## 6. Proposed Experiment (Not Yet Run)

**Status: not run.** This section proposes an experiment for Learn's music-theory-ga lab, which compiles GA. The lab's GA pin would first move to `5c3a52a`. Nothing in this section is a measurement:
- the predictions come from §5 and are written down before any run;
- they come from a line-by-line Python transcription of `Chord`, of `CalculateInversion` and of the chord recogniser, and from reading GA's two catalogue files;
- a later version of this lesson will report the results.

Every step calls GA's types in the lab's own process, never a running MCP server or a language model.

1. **Rotations from symbols.** For C, Cmaj7, G7 and C6 built with `Chord.FromSymbol`, call `ToInversion(k)` for each k, and record `Bass`, `GetInversion`, `Symbol` and `Equals` with the original. Prediction: the bass is the note at place k, counting from 0, in C E G, C E G B, G B D F and C E G A; `GetInversion` returns k; the symbol does not change; `Equals` is true.
2. **Orders.** Build `new Chord(AccidentedNoteCollection.Parse(...), C)` from E G C, E C G, G C E and G E C, and call `GetInversion`; then call `ToInversion(1)` on the E C G chord. Prediction: 1, 2, 2 and 1; then the notes G E C, with `GetInversion` 1.
3. **Voicing documents.** For the eight shapes of §5's table, build the voicing document the way `VoicingDocumentFactoryTests` does, with each diagram written string 1 first (032010 becomes `0-1-0-2-3-0`), and record `RootPitchClass`, `MidiBassNote` and `Inversion`. Prediction, in the table's order: the roots 0, 0, 7, 9, 7, 0, 0 and 5; the basses 40, 43, 41, 48, 50, 40, 44 and 50; the inversions 1, 2, 3, 1, 2, 1, −1 and −1.
4. **The catalogue.** Load GA's modes configuration and its atonal modal families, and for every mode whose name contains "Inversion", identify the triad that its notes make over C. Prediction: §5's table, with no entry naming its notes; in the atonal file, {0, 3, 9} and {0, 6, 9} have no tonal name.

### Practice Exercise

Step 3 predicts −1 for 4x2110. What does a chart call it, what position does GA's reading give it, and which distance does `CalculateInversion` miss?

> *Solution:* A chart usually names the reading whose root is in the bass: A♭aug, in root position. The recogniser reads the root as C, `Caug/Ab`; for C, the bass is the augmented fifth G♯, so the shape is a second inversion, with the bass 8 semitones above C. `CalculateInversion` maps a fifth in the bass only from 6 or 7 semitones, the diminished and perfect fifths.

---

## 7. Common Pitfalls

- **Reading the position from the top note or the shape.** Only the bass counts: xxx988 and 032010 are both first inversions.
- **Reading the jazz C6 as the figure 6.** C6 adds A to a C triad over C; the figure E6 is a C triad over E.
- **Treating a six-four as a resting chord.** The fourth above the bass is a dissonance; the chord passes, neighbours, arpeggiates or resolves to a dominant.
- **Giving a position without a root.** Over C, C E G A is root position as C6 and first inversion as Am7/C.
- **Reading a position from semitones.** The diminished seventh has 3, 6 and 9 semitones above its bass in every position; only the spelling tells them apart.
- **Trusting GA's names for the triad inversions.** None of the eight entries in `Modes.yaml` names its notes.

---

## Key Terms

| Term | Definition |
|------|-----------|
| **Position** | Which chord tone is in the bass: root position, or an inversion |
| **Root position** | The root in the bass |
| **First, second, third inversion** | The third, the fifth or the seventh in the bass |
| **Figured bass** | Numbers beside a bass note for the intervals above it, counted by letter names |
| **Figure** | Those numbers, usually abbreviated: 6, 6/4, 7, 6/5, 4/3, 4/2 |
| **Six-four chord** | A triad in second inversion, with a fourth and a sixth above the bass |
| **Cadential six-four** | I6/4 before V, or the dominant with a double appoggiatura, V6/4 – 5/3 |
| **Passing, neighbour, arpeggiated six-four** | A six-four on a bass that passes by step between two tones a third apart; over a held bass, with two voices moving up a step and back; under a bass that runs through one chord |

---

## Self-Check Assessment

**1. Give the position and the figure of Em/G, 3x2000, and of Am/E, 002210.**
> 3x2000 sounds G2 E3 G3 B3 E4: G, the third of E minor, is in the bass, so first inversion, figure 6 (B is a third and E a sixth above G). 002210 sounds E2 A2 E3 A3 C4 E4: E, the fifth of A minor, is in the bass, so second inversion, figure 6/4 (A is a fourth and C a sixth above E).

**2. Over C, why is C E G A root position as C6 and first inversion as Am7/C, and what figure does figured bass write?**
> A position is measured from the root, and the two readings have different roots, C and A. Figured bass names no root: over C, E is a third, G a fifth and A a sixth, so it writes 6/5 for both.

**3. In C – F/C – C, what kind of six-four is F/C, and what moves?**
> A neighbour (pedal or auxiliary) six-four, IV6/4. Over the held C, E and G rise a step to F and A, then fall back.

**4. What inversion does GA's voicing document give Ddim7, xx0101, and why?**
> −1. The recogniser names the shape `Fdim7/D`, so the root is F, and D lies 9 semitones above F, a distance that `CalculateInversion` does not map.

**Pass criteria:** Name the position of any voicing from its bass. Write the figures of triads and seventh chords in every position, and keep them apart from chord symbols. Name the four kinds of six-four and play each. Say where the sound alone does not fix a position, and where GA's `Chord`, voicing documents and catalogue go wrong.

---

## Research Basis

- Wikipedia, "Inversion (music)": the definition and numbering of inversions, the first inversion's intervals, the figures 53 and 6, I6, "position", and Rameau.
- Wikipedia, "Figured bass": scale steps above the bass, 2 for 6/4/2, G64 and E6 against the jazz C6.
- Wikipedia, "Six-four chord": the fourth as a dissonance, the free voicing above the bass, and the four types.
- Wikipedia, "Seventh chord": the four positions of G7 in figured-bass notation.
- Wikipedia, "Diminished seventh chord": the position known only from the spelling, as quoted in MUS-013.
- GA source at commit `5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26`: every code fact in §5 links to its line.
- Learn, music-theory-ga lesson 3 at commit `aaf6d3e52490d159ab962c75928e88c0dae28c28`: its inversion check on GA `a826864`.
- Named by the Streeling curriculum plan and not consulted for this version: Aldwell and Schachter, *Harmony and Voice Leading*, chapters 5 and 9.
- Experiment: proposed in §6, not run; this lesson contains no measurement of its own.
- Provenance: hand-authored by a Claude Code session (Opus 5.5) from the Streeling curriculum plan, not produced by the Seldon course pipeline; under review.
- Belief state: T(0.85) F(0.02) U(0.10) C(0.03).
