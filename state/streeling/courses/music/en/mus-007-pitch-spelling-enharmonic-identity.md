---
module_id: mus-007-pitch-spelling-enharmonic-identity
department: music
course: Pitch, Spelling and Enharmonic Identity
level: beginner
alchemical_stage: nigredo
prerequisites: [mus-001-what-is-a-chord]
estimated_duration: "45 minutes"
produced_by: claude-code-hand-authored
version: "1.0.0"
---

# Pitch, Spelling and Enharmonic Identity — One Sound, Several Names

> **Department of Music** | Stage: Nigredo (Beginner) | Estimated duration: 45 minutes

## Objectives

After this lesson, you will be able to:
- Tell a pitch, a pitch class and a note name apart, and give the octave and MIDI number of a spelled pitch such as C♭4 or B♯3
- List the 35 note names with at most a double accidental, place them on the line of fifths, and explain why G♯/A♭ is the only pitch class with two of them
- Spell the seven notes of any of the 30 major and minor keys with one letter per degree, and explain why the sharps and flats of two enharmonic keys add up to 12
- Spell the triads of D♭ major and of C♯ major, which a guitarist plays on the same frets
- Trace where GA keeps a note's spelling, and where it reduces a note to a pitch class and names it again from a list

---

## 1. Pitch, Pitch Class and Note Name

A note can be described at three levels, and each forgets something the one before it keeps.

A **pitch** is a sound at a definite height. MIDI numbers pitches by semitone: middle C, C4, is 60, and C♯4 is 61. A **pitch class** forgets the octave: every C is pitch class 0, numbered from C = 0 to B = 11, as MUS-002 does. A **note name** is a letter from C to B with an accidental: none (♮), ♯ or ♭ to move it one semitone up or down, 𝄪 or 𝄫 to move it two.

On an equal-tempered instrument, two names for the same pitch, such as C♯ and D♭, are **enharmonic**: they are the same key on a piano and the same fret on a guitar. The name is not a property of the sound. It records which letter, and so which degree of a scale, the note fills.

The octave number belongs to the letter, not to the sound. Scientific pitch notation starts every octave at C, so the C♭ written in octave 4 is C♭4, and it sounds as B3, MIDI 59; B♯3 sounds as C4, MIDI 60. In general, MIDI = 12 × (octave + 1) + the letter's pitch class + the accidental's value, from −2 for 𝄫 to +2 for 𝄪: C♯4 and D♭4 are both 61, E♯4 is 65 and F♭4 is 64.

### Practice Exercise

Give the MIDI number of B♯4 and of C♭5, and the natural note each sounds as.

> *Solution:* B♯4 is 12 × 5 + 11 + 1 = 72, the sound of C5. C♭5 is 12 × 6 + 0 − 1 = 71, the sound of B4. Both names cross the boundary between B and C, so each has the octave number of its letter, not of its sound.

---

## 2. The 35 Names and the Line of Fifths

Seven letters and five accidentals, 𝄫, ♭, ♮, ♯ and 𝄪, give 35 names. They cover the 12 pitch classes unevenly:

| Pitch class | Names |
|---|---|
| 0 | D𝄫, C, B♯ |
| 1 | D♭, C♯, B𝄪 |
| 2 | E𝄫, D, C𝄪 |
| 3 | F𝄫, E♭, D♯ |
| 4 | F♭, E, D𝄪 |
| 5 | G𝄫, F, E♯ |
| 6 | G♭, F♯, E𝄪 |
| 7 | A𝄫, G, F𝄪 |
| 8 | A♭, G♯ |
| 9 | B𝄫, A, G𝄪 |
| 10 | C𝄫, B♭, A♯ |
| 11 | C♭, B, A𝄪 |

Eleven pitch classes have three names. Pitch class 8 has two: only G and A lie within two semitones of it, and the next letters out, F and B, are three semitones away, one more than a double accidental can reach.

The **line of fifths** explains the count. Write the names a perfect fifth apart: … B♭ F C G D A E B F♯ C♯ G♯ … Unlike the circle of fifths, the line never closes: after B comes F♯, not F. Number the places from C = 0, so that G is 1, F is −1 and F♯ is 6. Every seven places add a sharp, and a name's pitch class is 7 times its place, mod 12, that is, the remainder after dividing by 12: G♯, at 8, gives 56, which is 8. The 35 names fill the 35 consecutive places from F𝄫 to B𝄪. Twelve fifths make seven octaves, so names twelve places apart share a pitch class: C at 0, B♯ at 12, D𝄫 at −12. A segment of 35 places, 2 × 12 + 11, holds three names for 11 pitch classes and two for the last one, A♭ and G♯.

### Practice Exercise

Name every spelling of pitch class 6, and give the place of each on the line of fifths.

> *Solution:* G♭ at −6, F♯ at 6 and E𝄪 at 18. Each is twelve places from the next, and 7 × −6 = −42, 7 × 6 = 42 and 7 × 18 = 126 are all 6 mod 12: for example, −42 + 48 = 6.

---

## 3. Spelling a Key: One Letter per Degree

A major or natural minor scale uses each of the seven letters exactly once; natural minor is the minor scale with no raised degree, as on the white keys from A to A. A **key signature** lists the letters that carry an accidental: sharps are added in the order F C G D A E B, flats in the order B E A D G C F. With 0 to 7 sharps or flats, there are 15 major keys, from C♭ to C♯, and 15 minor keys, from A♭ minor to A♯ minor. A major and a minor key with the same signature are **relative**: B♭ major and G minor both have two flats.

Spelling a key is then mechanical: start on the tonic, take the next six letters, and add the signature's accidental where it applies. F♯ major has six sharps, F C G D A E, and is spelled F♯ G♯ A♯ B C♯ D♯ E♯. Its seventh degree sounds as F, but the letter F is already the tonic's and the letter E would otherwise be missing, so the degree is E♯. C♭ major, with seven flats, is C♭ D♭ E♭ F♭ G♭ A♭ B♭.

Across the 30 keys, the 210 spelled notes use 21 names: the 7 naturals, the 7 sharps and the 7 flats. No key signature needs a double accidental. In the key spellings, E♯, B♯, C♭ and F♭ appear only in the 8 keys with six or seven accidentals: F♯ and C♯ major, D♯ and A♯ minor, G♭ and C♭ major, and E♭ and A♭ minor.

Three pairs of major keys have the same pitch classes: B and C♭, F♯ and G♭, C♯ and D♭. So do three pairs of minor keys: G♯ and A♭, D♯ and E♭, A♯ and B♭. In each pair the sharps and the flats add up to 12: B major has 5 sharps and C♭ major 7 flats. The two tonics are twelve places apart on the line of fifths (§2), and each place to the right adds a sharp to the signature or removes a flat.

The leading tone of a minor key can leave the signature. Harmonic minor raises the seventh degree by a semitone without changing its letter, so F♯ minor's leading tone is E♯ and C♯ minor's is B♯, and G♯ minor's is F𝄪, D♯ minor's C𝄪 and A♯ minor's G𝄪.

### Practice Exercise

In which major keys is E♯ a scale degree?

> *Solution:* F♯ major (F♯ G♯ A♯ B C♯ D♯ E♯) and C♯ major (C♯ D♯ E♯ F♯ G♯ A♯ B♯). E♯ is the sixth sharp of the order F C G D A E B, so only signatures with six or seven sharps contain it.

---

## 4. Same Frets, Two Spellings

A guitarist reading one chart in D♭ major and another in C♯ major plays the same frets: the two keys have the same seven pitch classes. Every note changes its name:

| Degree | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|---|---|---|---|---|---|---|---|
| D♭ major | D♭ | E♭ | F | G♭ | A♭ | B♭ | C |
| C♯ major | C♯ | D♯ | E♯ | F♯ | G♯ | A♯ | B♯ |

Each letter in the second row is the letter below the one in the first. D♭ major needs 5 flats and C♯ major 7 sharps.

Chords follow the same rule. A triad stacks two thirds, and a third spans three letters, so a triad takes every other letter: the root, the letter two above it and the letter four above it. The tonic triad of D♭ major is D♭ F A♭; that of C♯ major is C♯ E♯ G♯, not C♯ F G♯, which would make the third look like a fourth. Counting semitones, as in MUS-001, finds the frets; the letters give the names. The seven triads built on a key's degrees are its **diatonic** triads, numbered in Roman numerals: upper case for a major triad, lower case for a minor one, and ° for a diminished one, which GA writes dim:

| Degree | I | ii | iii | IV | V | vi | vii° |
|---|---|---|---|---|---|---|---|
| D♭ major | D♭ F A♭ | E♭ G♭ B♭ | F A♭ C | G♭ B♭ D♭ | A♭ C E♭ | B♭ D♭ F | C E♭ G♭ |
| C♯ major | C♯ E♯ G♯ | D♯ F♯ A♯ | E♯ G♯ B♯ | F♯ A♯ C♯ | G♯ B♯ D♯ | A♯ C♯ E♯ | B♯ D♯ F♯ |

An interval's number comes from its letters, as Learn's [lesson 1](https://github.com/spareilleux/learn/blob/6c78aad43cb932323cf74933b4fb36121e5cb9a3/src/content/docs/music-theory-ga/01-notes-and-the-fretboard.mdx) shows: D♭ to F covers three letters, a third; C♯ to F covers four, a fourth, although both span four semitones. Interval qualities are left to a later module, MUS-008.

### Practice Exercise

A chart in D♭ major reads D♭ – B♭m – G♭ – A♭ – Fm – E♭m – A♭ – D♭. Rewrite it in C♯ major, on the same frets.

> *Solution:* The chart is I – vi – IV – V – iii – ii – V – I. In C♯ major it reads C♯ – A♯m – F♯ – G♯ – E♯m – D♯m – G♯ – C♯. Every root moves to the letter below, so Fm becomes E♯m: F is not a degree of C♯ major, whose third degree is E♯.

---

## 5. Where GA Stands

GA is the music-theory library and chatbot of the GuitarAlchemist ecosystem. The facts below are read from its code at commit [`5c3a52a`](https://github.com/GuitarAlchemist/ga/tree/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26); this lesson documents that code and does not change it, and it has not run GA or its tests. The files it cites are unchanged on GA's `main` at `8fe33f8`. Learn's music-theory-ga lessons [1](https://github.com/spareilleux/learn/blob/6c78aad43cb932323cf74933b4fb36121e5cb9a3/src/content/docs/music-theory-ga/01-notes-and-the-fretboard.mdx) and [5](https://github.com/spareilleux/learn/blob/6c78aad43cb932323cf74933b4fb36121e5cb9a3/src/content/docs/music-theory-ga/05-keys-and-the-circle-of-fifths.mdx) compile an earlier version of GA, `a826864`, and check its note names and key spellings. The other numbers below come from a line-by-line Python transcription of the GA code named.

**Notes keep their spelling.** GA's [`Note`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Primitives/Notes/Note.cs#L17) union has key notes, which hold a letter and an accidental, and a [`Note.Chromatic`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Primitives/Notes/Note.cs#L82) case that keeps only the pitch class. As key notes, C♯ and D♭ are different values: enharmonic notes ["share a pitch class but are not equal"](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Primitives/Notes/Note.cs#L27). [`Note.Accidented.TryParse`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Primitives/Notes/Note.cs#L330) reads all 35 names of §2, written with ♯, ♭, 𝄪 and 𝄫 or with #, b, ## and bb, but its accidental parser [lists no ♯♯](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Primitives/Notes/Accidental.cs#L147) and no ♭♭, which `Note.Sharp` and `Note.Flat` accept through their own [accidental patterns](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Primitives/Notes/SharpAccidental.cs#L64). Learn's lesson 1 checks [eight spellings](https://github.com/spareilleux/learn/blob/6c78aad43cb932323cf74933b4fb36121e5cb9a3/code/music-theory-ga/expected/l1.txt#L16), from C♯ to F𝄪, against their pitch classes. The `Pitch` records follow §1: counted from the C that starts the octave, ["Cb4 is -1 (B3) and B#3 is 12 (C4)"](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Primitives/Notes/Pitch.cs#L46).

**Keys spell one letter per degree.** [`Key.GetNotes`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Tonal/Key.cs#L82) takes the tonic, then the next six letters, each sharpened or flattened when the [key signature](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Tonal/KeySignature.cs#L76) names it, with sharps added from F by fifths and flats from B by fourths. That is §3's rule. GA's tests check the spelling of all 15 major keys, up to [C♯ major](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Tests/Common/GA.Business.Core.Tests/Tonal/MajorKeyTests.cs#L22), and all 15 minor keys, up to [A♯ minor](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Tests/Common/GA.Business.Core.Tests/Tonal/MinorKeyTests.cs#L22). Learn's lesson 5 found the textbook spelling for the [15 signatures](https://github.com/spareilleux/learn/blob/6c78aad43cb932323cf74933b4fb36121e5cb9a3/code/music-theory-ga/expected/l5.txt#L3) and for [eight keys](https://github.com/spareilleux/learn/blob/6c78aad43cb932323cf74933b4fb36121e5cb9a3/code/music-theory-ga/expected/l5.txt#L21), and neither `GetNotes` nor `KeySignature` has changed since `a826864`.

**Chord tones from letters.** [`ChordSpelling.Spell`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Business.ML/Agents/Mcp/ChordSpelling.cs#L52) first moves the root's letter up by the chord's letter steps, then adds the accidental that reaches the target pitch class, as §4 does. Its tests check, for example, that the [minor third of B♭ is D♭](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Tests/Common/GA.Business.ML.Tests/Unit/ChordSpellingTests.cs#L30), not C♯. The MCP chord tool [calls it](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Business.ML/Agents/Mcp/ChordMcpTools.cs#L62), and so does the chatbot's [chord skill](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Business.ML/Agents/Skills/ChordInfoSkill.cs#L291). By transcription, given each triad's spelled root, it spells all 210 diatonic triads of the 30 keys with the textbook letters, E♯m in C♯ major included.

**Where a pitch class is named from a list.** Other parts of GA reduce a note to its pitch class and name it again from a list of 12 names, one list with sharps and one with flats. Neither list holds E♯, B♯, C♭, F♭ or a double accidental.

- [`EnharmonicNamingService`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Services/Chords/EnharmonicNamingService.cs#L11) keeps a [sharp list](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Services/Chords/EnharmonicNamingService.cs#L120) and a [flat list](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Services/Chords/EnharmonicNamingService.cs#L141). Its `GetEnharmonicEquivalents` method, documented as ["Gets all enharmonic equivalents for a chord"](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Services/Chords/EnharmonicNamingService.cs#L48), returns at most two names per pitch class, 17 of the 35. Its [`DetermineContextFromKey`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Services/Chords/EnharmonicNamingService.cs#L225) takes the key's tonic as a pitch class and never reads its `isMajor` parameter. Tonic 0 or 9 counts as natural, so A major and C minor do; 1, 6 and 11 are tested as sharp keys before flat keys, so D♭, G♭ and C♭ major count as sharp keys, as do G and D minor, tonics 7 and 2; and 8, 3 and 10 count as flat keys, so G♯, D♯ and A♯ minor do. Against the key signature, it is wrong for these 10 of the 30 keys. No code calls it, and no GA test names the service.
- [`KeyAwareChordNamingService`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Services/Chords/KeyAwareChordNamingService.cs#L295) takes the side from the key signature, which is right, then [names a root](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Services/Chords/KeyAwareChordNamingService.cs#L302) from those lists through `EnharmonicNamingService.AnalyzeEnharmonicChoices`. By transcription, pitch class 5 in C♯ major comes out F, and pitch class 11 in G♭ major B. Over the 210 degrees of the 30 keys, 12 come out misspelled, all in the 8 keys of §3 that use E♯, B♯, C♭ or F♭.

**The F# closures.** GA's F# layer chooses between its two lists from the root's own accidental: the [flat list](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Business.DSL/Closures/BuiltinClosures/DomainClosures.fs#L31) when the root has a flat or is F, the sharp list otherwise. [`domain.diatonicChords`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Business.DSL/Closures/BuiltinClosures/DomainClosures.fs#L274) applies that choice to the key's tonic. By transcription:

| Key | Chords returned | Misspelled |
|---|---|---|
| C♯ major | C#, D#m, Fm, F#, G#, A#m, Cdim | Fm for E♯m, Cdim for B♯° |
| G♭ major | Gb, Abm, Bbm, B, Db, Ebm, Fdim | B for C♭ |
| D minor | Dm, Edim, F, Gm, Am, A#, C | A# for B♭ |
| C minor | Cm, Ddim, D#, Fm, Gm, G#, A# | D#, G#, A# for E♭, A♭, B♭ |

Over the 30 keys, 18 of the 210 chords are misspelled, in 11 keys: the 8 of §3, and D, G and C minor, whose tonics carry no flat. [`domain.relativeKey`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Business.DSL/Closures/BuiltinClosures/DomainClosures.fs#L329) makes the same choice and, by transcription, answers A# major for G minor, D# major for C minor and B major for A♭ minor. [`domain.transposeChord`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Business.DSL/Closures/BuiltinClosures/DomainClosures.fs#L248) keeps the old root's side: G up three semitones becomes A#. A semitone count does not fix the letter, but A♯ major would need ten sharps, counting each 𝄪 as two, where B♭ major has two flats.

These closures answer GA's MCP tools [`GaDiatonicChords`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/GaMcpServer/Tools/GaDslTool.cs#L179) and [`GaRelativeKey`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/GaMcpServer/Tools/GaDslTool.cs#L188), and the chatbot's [`DiatonicChordsSkill`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Business.ML/Agents/Skills/DiatonicChordsSkill.cs#L22). The skill's description says it uses the closure so that enharmonic ["spelling is correct in less-common keys (Gb major, F# minor)"](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Business.ML/Agents/Skills/DiatonicChordsSkill.cs#L32). F♯ minor is right. G♭ major is one of the 11 keys, and the skill's [instructions](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/skills/diatonic-chords/SKILL.md#L26) give "Gb major returns Cm, not B#m", although G♭ major has neither a C nor a B♯: its fourth degree is C♭, which the closure names B. The correct spelling is already in GA, in `Key.Notes` and `ChordSpelling.Spell`; the closures do not call either.

**A name is read under a convention.** In set notation, T and E stand for 10 and 11. [`PitchClass.TryParse`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Atonal/PitchClass.cs#L258) reads T and E that way before it tries note names, so "E" is pitch class 11, not the note E, 4. Its [remarks](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Atonal/PitchClass.cs#L232) list both readings, and [a test](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Tests/GA.Domain.Core.Tests/Theory/Atonal/PitchClassTests.cs#L130) pins "E" to 11. GA's `TryGetRootPitchClass` reads a recognized chord root with `Note.Accidented.TryParse` instead, and its [remark](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Business.ML/Musical/Analysis/ChordIdentificationExtensions.cs#L17) still says that this method reads "A" as 10, which only `TryParseSetNotation` now does; `TryParse` reads "A" as the note, 9.

Fixing any of this is for GA's owners; this lesson only describes it.

### Practice Exercise

By transcription, `domain.diatonicChords` returns C♭ major as B, Dbm, Ebm, E, Gb, Abm, Bbdim. Respell it, and say why even the tonic changes.

> *Solution:* C♭, D♭m, E♭m, F♭, G♭, A♭m, B♭°. The closure reads "Cb" as pitch class 11, then names 11 from its flat list, where 11 is B: the letter C is lost before any name is chosen. F♭, pitch class 4, comes out E in the same way.

---

## 6. Proposed Experiment (Not Yet Run)

**Status: not run.** This section proposes an experiment for Learn's music-theory-ga lab, which compiles GA; the lab's GA pin would first move to `5c3a52a`. Nothing in it is a measurement. The predictions come from the transcription of §5 and are written down before any run; a later version of this lesson will report the results. Every step calls GA's types or closures in the lab's own process, never a running MCP server or a language model.

1. **The 35 names.** Parse the 35 names of §2 with `Note.Accidented.TryParse` and tabulate their pitch classes. Prediction: all 35 parse; 11 pitch classes get three names and pitch class 8 two.
2. **The 30 keys.** Spell the 30 keys through `Key.Notes`. Prediction: 7 distinct letters in every key, 21 distinct names over the 210 notes, and the textbook spelling everywhere.
3. **Octaves.** Compute the MIDI numbers of C♭4, B♯3, E♯4 and F♭4 through `Pitch`. Prediction: 59, 60, 65 and 64.
4. **The diatonic closure.** Invoke `domain.diatonicChords` for the 30 keys and compare each chord's root with `Key.Notes`. Prediction: 18 of the 210 chords differ, in 11 keys.
5. **The relative-key closure.** Invoke `domain.relativeKey` for the 30 keys. Prediction: 3 answers differ, for G minor, C minor and A♭ minor.
6. **The naming service.** For each of the 210 notes, call `EnharmonicNamingService.AnalyzeEnharmonicChoices` with the context of the key's signature; then call `DetermineContextFromKey` with each key's tonic. Prediction: 12 names differ, in 8 keys, and 10 of the 30 contexts disagree with the signature.
7. **Chord tones.** Call `ChordSpelling.Spell`, which is internal to GA.Business.ML, by reflection on the 210 diatonic triads. Prediction: all 210 match `Key.Notes`.

### Practice Exercise

Step 4 predicts 18 differences. What would the closure have to do for the prediction to become 0, and what kind of input could still not be spelled?

> *Solution:* It would have to spell from letters, as `Key.Notes` and `ChordSpelling.Spell` do, instead of naming pitch classes from a list. Given a spelled tonic, nothing is ambiguous: "Db" and "C#" name different keys. A tonic given only as a pitch class, such as 1, cannot say whether the key is D♭ or C♯ major.

---

## 7. Common Pitfalls

- **Calling C♯ and D♭ the same note.** They share a pitch class, a piano key and a fret, not a name or a scale degree.
- **Writing F in F♯ major.** Each letter appears once in a key, so the seventh degree is E♯.
- **Spelling a chord from semitones.** A triad takes every other letter: E♯m, not Fm, is the iii chord of C♯ major.
- **Reading the octave from the sound.** B♯3 sounds as C4, but its octave number follows the letter B.
- **Forgetting the leading tone of a sharp minor key.** G♯ minor's raised seventh is F𝄪.
- **Naming notes from a list of 12.** A sharp list and a flat list hold 17 of the 35 names, and none of the four that 8 keys need.
- **Taking a key's tonic as a pitch class.** Pitch class 1 is the tonic of D♭ major, with 5 flats, and of C♯ major, with 7 sharps.

---

## Key Terms

| Term | Definition |
|------|-----------|
| **Pitch** | A sound at a definite height, such as C4, MIDI 60 |
| **Pitch class** | A pitch without its octave, numbered from C = 0 to B = 11 |
| **Note name** | A letter from C to B with an accidental: 𝄫, ♭, ♮, ♯ or 𝄪 |
| **Enharmonic** | Said of two names, or two keys, with the same pitch classes, such as C♯ and D♭ |
| **Line of fifths** | The note names a perfect fifth apart, in a line that never closes: … F C G D A E B F♯ C♯ … |
| **Key signature** | The letters that carry a sharp (added from F, by fifths) or a flat (added from B, by fourths) in a key |
| **Leading tone** | The seventh degree a semitone below the tonic; in a minor key, the raised seventh of harmonic minor |

---

## Self-Check Assessment

**1. How many names with at most a double accidental does pitch class 6 have? Name them.**
> Three: G♭, F♯ and E𝄪. They sit twelve places apart on the line of fifths.

**2. What is the MIDI number of C♭4, and which natural note does it sound as?**
> 59, the sound of B3. The octave number follows the letter C, so C♭4 lies one semitone below C4.

**3. Spell the natural minor scale of A♭ minor.**
> A♭ B♭ C♭ D♭ E♭ F♭ G♭: seven flats, one letter per degree.

**4. GA's [`domain.relativeKey`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Business.DSL/Closures/BuiltinClosures/DomainClosures.fs#L329) answers A# major for G minor. What is the relative major, and why does the closure misspell it?**
> B♭ major. The closure names the relative tonic, pitch class 10, from its sharp list, because the tonic G carries no flat and is not F.

**Pass criteria:** Tell a pitch, a pitch class and a note name apart; give a spelled pitch's octave and MIDI number; list the names of a pitch class from the line of fifths; spell any of the 30 keys, and the triads of two enharmonic keys, with one letter per degree; and tell GA's letter-based spelling from its pitch-class lists.

---

## Research Basis

- D. Temperley, "The Line of Fifths", *Music Analysis* 19(3), 2000, 289–319: spelled pitches placed on a line of fifths rather than a circle
- E. Gould, *Behind Bars*, Faber Music, 2011: accidentals and the notation of pitch
- E. Aldwell, C. Schachter and A. Cadwallader, *Harmony and Voice Leading*, Cengage, 2019: scales, key signatures and the spelling of triads
- GA source at commit `5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26`: every code fact in §5 links to its line
- Learn, music-theory-ga lessons 1 and 5 and their expected output at commit `6c78aad43cb932323cf74933b4fb36121e5cb9a3`: the compiled checks of GA's note names and key spellings quoted in §5
- Experiment: proposed in §6, not run; this lesson contains no measurement of its own
- Provenance: hand-authored by a Claude Code session (Opus 5.5) from the Streeling curriculum plan, not produced by the Seldon course pipeline; under review
- Belief state: T(0.85) F(0.02) U(0.10) C(0.03)
