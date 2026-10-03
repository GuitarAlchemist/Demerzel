---
module_id: mus-012-chord-formulas-essential-tones-doubling
department: music
course: Chord Formulas, Essential Tones and Doubling
level: intermediate
alchemical_stage: albedo
prerequisites: [mus-001-what-is-a-chord, mus-008-intervals-inversion-compound]
estimated_duration: "45 minutes"
produced_by: claude-code-hand-authored
version: "1.0.0"
---

# Chord Formulas, Essential Tones and Doubling — What a Chord Can Lose

> **Department of Music** | Stage: Albedo (Intermediate) | Estimated duration: 45 minutes

## Objectives

After this lesson, you will be able to:
- Write a chord formula as degrees and as semitones above the root, up to the thirteenth
- Tell a chord's essential tones, the ones its name depends on, from the optional ones, and drop tones from an extended chord in the usual order
- Count the doublings of a guitar voicing, and say which tones are usually doubled
- Fit a thirteenth chord on six strings and justify the choice
- Trace what GA stores about formulas, essential tones and doubling, and what it never reports

---

## 1. The Formula of a Chord

A chord formula lists the chord's tones as degrees above its root, numbered as in the major scale of the root: 1 is the root, 3 the major third, 5 the perfect fifth, 7 the major seventh. A flat or a sharp lowers or raises the degree by a semitone, so ♭3 is the minor third and ♭7 the minor seventh. Each degree is an interval above the root (MUS-008), and an interval has a number of semitones:

| Symbol on C | Formula | Semitones above the root | Notes |
|------|---------|------|------|
| C | 1 3 5 | 0 4 7 | C E G |
| Cm | 1 ♭3 5 | 0 3 7 | C E♭ G |
| Cdim | 1 ♭3 ♭5 | 0 3 6 | C E♭ G♭ |
| Caug | 1 3 ♯5 | 0 4 8 | C E G♯ |
| C7 | 1 3 5 ♭7 | 0 4 7 10 | C E G B♭ |
| Cmaj7 | 1 3 5 7 | 0 4 7 11 | C E G B |
| Cm7 | 1 ♭3 5 ♭7 | 0 3 7 10 | C E♭ G B♭ |
| Cm7♭5 | 1 ♭3 ♭5 ♭7 | 0 3 6 10 | C E♭ G♭ B♭ |
| Cdim7 | 1 ♭3 ♭5 𝄫7 | 0 3 6 9 | C E♭ G♭ B𝄫 |
| C9 | 1 3 5 ♭7 9 | 0 4 7 10 14 | C E G B♭ D |
| C11 | 1 3 5 ♭7 9 11 | 0 4 7 10 14 17 | C E G B♭ D F |
| C13 | 1 3 5 ♭7 9 11 13 | 0 4 7 10 14 17 21 | C E G B♭ D F A |

Past the seventh the degrees are compound intervals, as in MUS-008: the 9 is a major ninth, 14 semitones, the 2 an octave up; the 11 is a perfect eleventh, 17, the 4 an octave up; the 13 a major thirteenth, 21, the 6 an octave up. A chord named 9, 11 or 13 contains, by convention, the tones of the stack of thirds below its number: C13 is the dominant seventh C E G B♭ with D, F and A on top. Each letter appears once, and seven letters are all the letters there are. On G, the formula 1 3 5 ♭7 9 11 13 gives G B D F A C E, the seven notes of C major.

### Practice Exercise

Spell Fmaj9 and D13 from their formulas.

> *Solution:* Fmaj9 is 1 3 5 7 9: F A C E G. D13 is 1 3 5 ♭7 9 11 13: D F♯ A C E G B.

---

## 2. Essential and Optional Tones

A tone is **essential** when leaving it out changes the chord's name, and **optional** when the name survives without it. The formula does not say which is which; the names do.

- **The third** decides major or minor: without it, C and Cm are the same two notes. It is essential.
- **The seventh** decides the kind of seventh chord: C7 and Cmaj7 differ only there. It is essential in every seventh chord and in every chord named 9, 11 or 13, since those contain the seventh.
- **The perfect fifth** is the same in C, Cm, C7, Cmaj7 and Cm7: no name depends on it, so it is the first tone to drop. A fifth that is not perfect is essential, since it is what separates Cm7♭5 from Cm7 and Caug from C.
- **The root** names the chord, but a voicing can leave it to someone else: in a band, the bass plays it, and the guitar's voicing is then rootless (MUS-005). Alone, a guitarist keeps it, usually in the bass.
- **The highest extension** is what the number in the symbol announces: a C13 without its A is a C11, a C9 or a C7, depending on what remains. The extensions under it are optional.
- **The natural 11 over a major third** clashes: it lies a semitone above the third, or a minor ninth if it sits above it in a higher octave. In a dominant or major thirteenth chord it is left out, or raised to ♯11, which a symbol must then say (MUS-005). Over a minor third, as in Cm11, the 11 lies a whole tone above the third and stays.

For the dominant thirteenth, Wikipedia's "Thirteenth (interval)" summarises common-practice usage this way, after Benward and Saker: the tones most often present are the root, the 3rd, the 7th and the 13th, with the 5th, the 9th and the 11th "typically omitted". The same article gives the reason for the 11: "It is customary to omit the eleventh on dominant or major thirteenth chords because the eleventh conflicts with the third". For the dominant ninth, Wikipedia's "Ninth chord", again after Benward and Saker, gives the root, 3rd, 7th and 9th, with the 5th "typically omitted". Jazz voicings often go one step further and drop the root and the fifth, "because the root is played by the bass player" ("Extended chord").

### Practice Exercise

Which tones of Cmaj9 can a guitarist accompanying a bassist leave out without changing the chord's name?

> *Solution:* The fifth, G, always, and the root, C, since the bass plays it. E (the third), B (the seventh) and D (the ninth) must stay.

---

## 3. Doubling

A tone is **doubled** when it sounds in more than one octave, or at the same pitch in more than one voice (Wikipedia, "Voicing (music)"); on a guitar, on more than one string. A six-string chord of three tones must double some of them. Reading the common first-position shapes from string 6 in standard tuning, E2 A2 D3 G3 B3 E4 (MUS-009), and counting the strings on each tone:

| Shape | Notes, string 6 first | Root | Third | Fifth |
|------|------|------|------|------|
| E, 022100 | E2 B2 E3 G♯3 B3 E4 | 3 | 1 | 2 |
| Em, 022000 | E2 B2 E3 G3 B3 E4 | 3 | 1 | 2 |
| A, x02220 | A2 E3 A3 C♯4 E4 | 2 | 1 | 2 |
| Am, x02210 | A2 E3 A3 C4 E4 | 2 | 1 | 2 |
| C, x32010 | C3 E3 G3 C4 E4 | 2 | 2 | 1 |
| G, 320003 | G2 B2 D3 G3 B3 G4 | 3 | 2 | 1 |
| D, xx0232 | D3 A3 D4 F♯4 | 2 | 1 | 1 |
| F, 133211 | F2 C3 F3 A3 C4 F4 | 3 | 1 | 2 |

Every shape doubles its root, and six of the eight play their third on one string only. That agrees with the old rule of four-part writing: in a triad, "the root is generally doubled" ("Four-part harmony"). For a dominant seventh chord, "the root may be doubled and the fifth omitted" ("Dominant seventh chord"). The rule has a reason in voice leading, which avoids parallel octaves between any two voices ("Voice leading"). A tone with a strong pull, such as the leading tone, the third of a dominant chord, has one usual resolution, and two voices taking it together would move in parallel octaves; so the leading tone is not doubled. On the guitar, the shape usually decides the doubling: C and G double their thirds because an open string, E4 in C and B3 in G, is the third.

Doubling is a property of the voicing, not of the chord: C x32010 and C x35553 are the same chord, C E G, with doublings 2, 2, 1 and 2, 1, 2.

### Practice Exercise

Count the doublings of the A-shape barre chord x35553, C major at fret 3.

> *Solution:* From string 5: C3, G3, C4, E4, G4. The root sounds twice, the third once, the fifth twice.

---

## 4. A Thirteenth Chord on Six Strings

G13 has seven tones and the guitar six strings, so at least one tone must go. Following §2, the fifth and the 11th go first: D adds nothing to the name, and C clashes with B. What is left, G B F A E, is five tones, and a common shape plays exactly those: **3x3455**. From string 6:

| String | Fret | Note | Degree |
|------|------|------|------|
| 6 | 3 | G2 | 1 |
| 5 | x | — | — |
| 4 | 3 | F3 | ♭7 |
| 3 | 4 | B3 | 3 |
| 2 | 5 | E4 | 13 |
| 1 | 5 | A4 | 9 |

It holds the root in the bass, the two guide tones F and B in the middle, and the 13 and the 9 on top, with no doubling, within three frets. Without its top string, 3x345x drops the 9 as well and is still G13: root, ♭7, 3 and 13, the four tones Wikipedia lists first. The same article, after Capone, notes that "to make the chord more playable [on guitar], thirteenth chords often omit the fifth and the ninth". Remove the E as well and the chord is G7.

### Practice Exercise

A guitarist plays 3x3455 with a bassist who plays G. Which note could the guitarist leave out next, and what would remain?

> *Solution:* The root, G2: xx3455 plays F3 B3 E4 A4, the ♭7, 3, 13 and 9, a rootless G13. The guide tones and the 13 are still there.

---

## 5. Where GA Stands

GA is the music-theory library and chatbot of the GuitarAlchemist ecosystem. The facts below are read from its code at commit [`5c3a52a`](https://github.com/GuitarAlchemist/ga/tree/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26). This lesson documents that code and does not change it. It has not run GA or its tests. The files it cites are unchanged on GA's `main` at `6b8b8bd`. Learn, the ecosystem's course site, has a music-theory-ga course whose lessons compile an earlier version of GA, `a826864`.

**A formula interval can be marked optional or doubled. No code marks one doubled, and only builder methods that nothing calls mark one optional.** [`ChordFormulaInterval`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Harmony/ChordFormulaInterval.cs#L12-L17) takes three more arguments beside the interval and its function:
- `isEssential`, true by default;
- `isTypicallyDoubled`, false by default;
- a voice-leading tendency, `Stable` by default.

The class comment's example calls the major third ["essential, typically doubled"](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Harmony/ChordFormulaInterval.cs#L9). The four-part rule of §3 doubles the root instead.

The formula factories pass only the interval and its function:
- [`FromSemitones`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Harmony/ChordFormula.cs#L137-L153);
- both [`FromIntervalNames`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Harmony/ChordFormula.cs#L159-L186);
- [`ChordTemplateFactory.CreateModalChordFormula`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Services/Chords/ChordTemplateFactory.cs#L429-L433), which builds every chord [the data tool exports](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Tools/GaDataCLI/Program.cs#L262);
- [`Chord.AnalyzeChordFormula`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Harmony/Chord.cs#L322-L342), which computes a chord's formula from its notes.

Every interval they build is therefore essential, and none is doubled.

Only [`ChordBuilder.WithInterval`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Services/Chords/ChordBuilder.cs#L38-L52) takes an `isEssential` argument. The only calls that pass false are five in `ChordBuilderEx`:
- the quartal, quintal and secundal stacks ([L55](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Services/Chords/ChordBuilderEx.cs#L55), [L71](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Services/Chords/ChordBuilderEx.cs#L71), [L87](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Services/Chords/ChordBuilderEx.cs#L87));
- the custom voicing ([L127](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Services/Chords/ChordBuilderEx.cs#L127));
- the polychord ([L156](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Services/Chords/ChordBuilderEx.cs#L156)).

No code outside those two files calls `ChordBuilder`. [`EssentialIntervals` and `OptionalIntervals`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Harmony/ChordFormula.cs#L93-L100) have no caller.

Besides the polychord builder, which [copies it](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Services/Chords/ChordBuilderEx.cs#L146), and the uncalled properties above, `IsEssential` is read in two places:
- the interval's [`ToString`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Harmony/ChordFormulaInterval.cs#L67-L72);
- the [chord export](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Tools/GaDataCLI/Program.cs#L292-L297) of GA's data tool.

In the exported file committed to GA, [`all-chords.json`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Data/Export/all-chords.json), all 87,624 intervals of its 25,900 chords say `"IsEssential": true` (counted in the file). The tool's README shows a C major triad whose [fifth is `false`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Tools/GaDataCLI/README.md#L79-L90). That is the answer of §2, which the code does not give.

**Altered tensions are labelled as roots.** [`ChordFunctionExtensions.FromSemitones`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Harmony/ChordFunctionExtensions.cs#L13-L22) maps:
- 2 and 14 to the ninth;
- 5 and 17 to the eleventh;
- 9 and 21 to the thirteenth;
- every value it does not list to `Root`, including 13 (♭9), 15 (♯9), 18 (♯11) and 20 (♭13).

This affects the symbol parser's formulas:
- its "Altered Dominant", 4 7 10 13 15 ([`ChordSymbolParser.cs#L176-L177`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Services/Chords/Parsing/ChordSymbolParser.cs#L176-L177)), holds two intervals labelled `Root`;
- its ♭9, ♯9, ♯11 and ♭13 formulas ([L181-L188](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Services/Chords/Parsing/ChordSymbolParser.cs#L181-L188)) hold one each.

[`ChordDegree`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Harmony/ChordFormulaInterval.cs#L52-L62) gives each of them degree 1. A rule that dropped tones by function could not tell these tensions from the root.

**GA gives three answers for the thirteenth chord.**
- **`Chord.FromSymbol`** reads the symbol "13" as [4 7 10 14 17 21](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Harmony/Chord.cs#L203), the full stack of §1 with its 11, and so does [`ChordSymbolParser`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Services/Chords/Parsing/ChordSymbolParser.cs#L162-L163). A test expects C13 to [spell C E G B♭ D F A](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Tests/GA.Domain.Core.Tests/Theory/Harmony/ChordTests.cs#L288).
- **The chord recogniser's** dominant-13 pattern, [0 2 4 7 9 10](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Harmony/CanonicalChordPatternCatalog.cs#L88), has no 11 and keeps the fifth and the ninth. A match may [miss one tone and add one](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Services/Chords/CanonicalChordRecognizer.cs#L160-L162). At equal distance, the ranking [prefers a candidate with nothing missing](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Services/Chords/CanonicalChordRecognizer.cs#L178-L183): an omitted tone counts against a name more than an added one.
- **GA's configuration file `AdvancedHarmony.yaml`** says ["Often omit 11th to avoid dissonance"](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Business.Config/AdvancedHarmony.yaml#L32-L38). It gives G13 as G B F A E, the five notes of §4's 3x3455. Under ninth chords, the same file lists [G13 with all seven notes](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Business.Config/AdvancedHarmony.yaml#L14-L16).

Code reads that file in two places:
- [`SymbolicTagRegistry`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Business.Config/Configuration/SymbolicTagRegistry.cs#L94) registers its [`Name` and `Id` values](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Business.Config/Configuration/SymbolicTagRegistry.cs#L142-L147) as tags;
- [`YamlKnowledgeLoader`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Business.Config/YamlKnowledgeLoader.fs#L131-L140) flattens each entry to text for a [MongoDB knowledge sync](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/GA.Data.MongoDB/Services/DocumentServices/YamlKnowledgeSyncService.cs#L25).

Neither builds a chord from the file's notes.

**A voicing's doublings and omissions are slots no code fills.** GA's voicing analysis carries a [`ToneInventory`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Business.Core/Analysis/Voicings/ToneInventory.cs#L3) of `Tones`, `HasGuideTones`, `OmittedTones` and `DoubledTones`. Its only producer fills it with [`new ToneInventory([], false, [], [])`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Services/Fretboard/Voicings/Analysis/VoicingAnalyzer.cs#L155). GA's architecture decision record 0004 lists that line [among the placeholders](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/docs/adr/0004-musical-voicing-analysis-stays-wide.md#L16-L17) and calls them ["unfilled pipeline slots"](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/docs/adr/0004-musical-voicing-analysis-stays-wide.md#L26-L27). With GA `a826864`, Learn's lesson 14 counted 711 analyses, [none with guide tones or omitted tones](https://github.com/spareilleux/learn/blob/89dc3e64d392cdc36844b03719880484d823b4d7/code/music-theory-ga/expected/l16.txt#L141).

Downstream, nothing can recover them:
- the voicing document [copies the slots](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Business.ML/Rag/VoicingDocumentFactory.cs#L51-L58);
- the ["Shell" tag](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Business.ML/Musical/Enrichment/AutoTaggingService.cs#L106-L115) needs guide tones and a missing fifth;
- the harmonic analyser [sets `IsRootless` to false](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Services/Fretboard/Voicings/Analysis/VoicingHarmonicAnalyzer.cs#L40-L42) for every voicing.

As a result, no voicing GA indexes gets that "Shell" tag, and none is marked rootless. The physical analyser has a tag of its own, `shell-voicing`, [added](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Services/Fretboard/Voicings/Analysis/VoicingPhysicalAnalyzer.cs#L209) to any voicing [played on three or four strings](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Services/Fretboard/Voicings/Analysis/VoicingPhysicalAnalyzer.cs#L126-L128), whatever its tones: D xx0232, a plain triad, gets it, and 3x3455 does not. `Chord.AnalyzeChordFormula` also [folds every note to an interval mod 12 and drops repeats](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Harmony/Chord.cs#L328-L331), so the formula it computes keeps no doubling.

**OPTIC-K counts doublings, but with weight zero.** GA's voicing embedding is [OPTIC-K](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Business.ML/Embeddings/EmbeddingSchema.cs#L98), a vector of numbers GA's voicing search compares. Its EXTENSIONS partition holds doubling dimensions:
- 80, the [doubling ratio](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Business.ML/Embeddings/EmbeddingSchema.cs#L495-L500), (N − distinct pitch classes) / N;
- 81, [root doubled](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Business.ML/Embeddings/EmbeddingSchema.cs#L502-L507);
- 91 and 92, third and fifth doubled;
- 95, root omitted.

The partition has [weight 0.00 and role `Info`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Business.ML/Embeddings/EmbeddingSchema.cs#L127), ["excluded from similarity"](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Business.ML/Embeddings/EmbeddingSchema.cs#L17-L18): voicing search ignores every one of these dimensions.

The generator takes N from the voicing's [MIDI notes](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Business.ML/Embeddings/MusicalEmbeddingGenerator.cs#L207-L211). It takes its [counts](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Business.ML/Embeddings/MusicalEmbeddingGenerator.cs#L237-L243) from the document's pitch classes. The document factory fills those from the voicing's [pitch-class set](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Business.ML/Rag/VoicingDocumentFactory.cs#L82), a [sorted set](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Atonal/PitchClassSet.cs#L37) that holds each pitch class once.

Read, not run, the dimensions behave as follows:
- dimension 80 sees doubling: (5 − 3) / 5 = 0.4 for C x32010;
- a pitch class in a set is never there twice, so dimensions 81 and 92 stay at 0;
- dimension 91 [counts the minor and the major third together](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Business.ML/Embeddings/MusicalEmbeddingGenerator.cs#L300-L306), so it turns to 1 only for a voicing that holds both, such as a ♯9 chord, where nothing is doubled.

Fixing any of this is for GA's owners; this lesson only describes it.

### Practice Exercise

By the generator's formula, what does dimension 80 give for G 320003 and for D xx0232? What would dimension 81 give for each if the pitch classes kept their repeats?

> *Solution:* G 320003 sounds 6 notes on 3 pitch classes: (6 − 3) / 6 = 0.5. D xx0232 sounds 4 notes on 3 pitch classes: (4 − 3) / 4 = 0.25. With repeats, the root counts 3 in G and 2 in D, so dimension 81 would be 1 for both. From a set, it is 0 for both.

---

## 6. Proposed Experiment (Not Yet Run)

**Status: not run.** This section proposes an experiment for Learn's music-theory-ga lab, which compiles GA. The lab's GA pin would first move to `5c3a52a`, and its sparse checkout of GA would add GA.Business.ML for step 4. Nothing in this section is a measurement:
- the predictions come from §2 to §5 and are written down before any run;
- the chord names in steps 2 and 3 come from a line-by-line Python transcription of the recogniser and its pattern catalogue;
- a later version of this lesson will report the results.

Every step calls GA's types in the lab's own process, never a running MCP server or a language model.

1. **Formula flags.** For every symbol in `Chord.FromSymbol`'s table and every formula of `ChordSymbolParser`, count the intervals with `IsEssential` false or `IsTypicallyDoubled` true. Then print the `Function` and `ChordDegree` of the 13, 15, 18 and 20 semitone intervals. Prediction: no interval is optional and none is doubled. The four tensions read `Root`, degree 1.
2. **The thirteenth both ways.** Spell `Chord.FromSymbol("C13")` and `Chord.FromSymbol("G13")`, then pass each set of notes to `CanonicalChordRecognizer.Identify`. Prediction: C E G B♭ D F A and G B D F A C E, named Gm11 and Dm11. Every candidate at distance 1 has nothing missing, and minor-11, at priority 20, ranks before dominant-13, at priority 25.
3. **3x3455 and its reductions.** Identify the pitch classes of 3x3455, 3x345x, xx3455 and 3x34xx, with their bass notes. Prediction:
   - 3x3455 is A7sus2 with slash suffix /G. G13 is a candidate at distance 1, but it is missing its fifth, while A7sus2 only adds F;
   - 3x345x is Em/G;
   - xx3455 is Asus2/F;
   - 3x34xx is G7(shell), an exact match.
4. **Doubling dimensions.** For the eight first-position shapes of §3 and x35553, build the voicing document and its OPTIC-K vector through GA's analyser, document factory and embedding generator. Record dimensions 80, 81, 91, 92 and 95 and the `ToneInventory`. Prediction:
   - dimension 80 is 0.5 for E, Em, G and F, 0.4 for A, Am, C and x35553, and 0.25 for D;
   - dimensions 81, 91, 92 and 95 are 0 for all nine;
   - every inventory is empty.

### Practice Exercise

Step 3 predicts A7sus2 for 3x3455. Which notes of G B F A E does that name read as the root, the 2, the 5 and the ♭7, and which note is extra?

> *Solution:* A is the root, B the 2, E the 5 and G the ♭7: A7sus2 is A B E G. F, a minor sixth above A, is the extra note. To read G13, GA would need D, the fifth, which the voicing leaves out on purpose (§2). GA counts that omission against G13 more than the extra F against A7sus2.

---

## 7. Common Pitfalls

- **Reading a formula as a voicing.** A formula lists which tones a chord has. It says nothing about how often each sounds or in which octave.
- **Dropping the third to make room.** The third decides major or minor. Drop the fifth first.
- **Dropping an altered fifth.** Without its G♭, Cm7♭5 is a Cm7 with no fifth.
- **Keeping the natural 11 over a major third.** Leave it out, or raise it to ♯11 and say so in the symbol.
- **Doubling the leading tone.** Its single resolution, doubled, makes parallel octaves.
- **Counting doublings on a pitch-class set.** A set holds each pitch class once, so a doubling count on a set is always zero.
- **Trusting `IsEssential` in GA's data.** Every interval of every exported chord says true.

---

## Key Terms

| Term | Definition |
|------|-----------|
| **Chord formula** | The chord's tones as degrees above its root, such as 1 3 5 ♭7; each degree is an interval with a number of semitones |
| **Essential tone** | A tone whose omission changes the chord's name: the third, the seventh, an altered fifth, the highest extension |
| **Optional tone** | A tone the name survives without: first of all the perfect fifth, then the root when a bassist plays it, and the extensions below the highest |
| **Extension** | A tone past the seventh: the 9, 11 or 13, a compound interval above the root |
| **Doubling** | A tone sounding on more than one string, at the same pitch or in another octave |
| **Guide tones** | The third and the seventh, which tell the chord's quality |
| **Rootless voicing** | A voicing without the root, left to the bass |
| **Shell voicing** | Root, third and seventh only, as in GA's shell-7 pattern [0 4 10](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Harmony/CanonicalChordPatternCatalog.cs#L132) |

---

## Self-Check Assessment

**1. Write the formula and semitones of Cm11, and say which tone a guitarist drops first.**
> 1 ♭3 5 ♭7 9 11, or 0 3 7 10 14 17: C E♭ G B♭ D F. The fifth, G, goes first. The 11 can stay, a whole tone above the minor third.

**2. Count the doublings of Em 022000. Which tone sounds only once?**
> E2 B2 E3 G3 B3 E4: the root sounds three times, the fifth twice and the third, G3, once.

**3. Why does 3x3455 leave out D and C from G13?**
> D is the perfect fifth, which no name depends on. C is the natural 11, a semitone above the third B, which clashes in a dominant chord.

**4. In GA at `5c3a52a`, what does the chord export say about the fifth of a C major triad, and why?**
> `"IsEssential": true`, like every interval in the file. The formula factories never pass the flag, so its default holds.

**Pass criteria:** Write and spell any chord formula up to the thirteenth. Name its essential tones and drop the others in order. Count the doublings of a guitar voicing. Justify a six-string voicing of an extended chord. Tell what GA stores about essential and doubled tones from what it computes.

---

## Research Basis

- B. Benward and M. Saker, *Music in Theory and Practice*, vol. II, 8th ed., McGraw-Hill, 2009, pp. 183–184: the usual tones of V9 and V13, as quoted in Wikipedia's "Ninth chord" and "Thirteenth (interval)".
- Wikipedia, "Thirteenth (interval)": the thirteenth chord, the omitted 11, and the guitar's omitted fifth and ninth.
- Wikipedia, "Ninth chord": the usual tones of V9.
- Wikipedia, "Extended chord": the omitted fifth, and the root left to the bass in jazz.
- Wikipedia, "Voicing (music)": doubling.
- Wikipedia, "Four-part harmony": the doubled root of a triad.
- Wikipedia, "Dominant seventh chord": the doubled root and omitted fifth.
- Wikipedia, "Voice leading": parallel octaves.
- GA source at commit `5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26`: every code fact in §5 links to its line.
- Learn, music-theory-ga lesson 14's expected output at commit `89dc3e64d392cdc36844b03719880484d823b4d7`: the 711 analyses of GA `a826864` quoted in §5.
- Experiment: proposed in §6, not run; this lesson contains no measurement of its own.
- Provenance: hand-authored by a Claude Code session (Opus 5.5) from the Streeling curriculum plan, not produced by the Seldon course pipeline; under review.
- Belief state: T(0.85) F(0.02) U(0.10) C(0.03).
