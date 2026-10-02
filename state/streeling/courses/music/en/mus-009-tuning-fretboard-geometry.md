---
module_id: mus-009-tuning-fretboard-geometry
department: music
course: Tuning and Fretboard Geometry
level: beginner
alchemical_stage: nigredo
prerequisites: [mus-007-pitch-spelling-enharmonic-identity, mat-004-vectors-matrices-norms, phy-001-science-of-guitar-sound]
estimated_duration: "45 minutes"
produced_by: claude-code-hand-authored
version: "1.0.0"
---

# Tuning and Fretboard Geometry — One Pitch, Many Places

> **Department of Music** | Stage: Nigredo (Beginner) | Estimated duration: 45 minutes

## Objectives

After this lesson, you will be able to:
- Write a tuning as a vector of six pitches and give the pitch of any string at any fret
- Find every place a given pitch can be played, and count the places of every pitch on the neck
- Describe what an alternate tuning changes and what it leaves alone, as the difference of two tuning vectors
- Derive where the frets go from the equal-tempered semitone, and compute fret positions for any scale length
- Trace what GA computes for tunings, positions and fret distances, and where its catalogue and tests disagree with the theory

---

## 1. The Tuning as a Vector

Guitarists number the strings from the treble side: string 1 is the thinnest, highest-sounding string, string 6 the thickest. In standard tuning they sound, from string 1 to string 6, E4, B3, G3, D3, A2 and E2, MIDI 64, 59, 55, 50, 45 and 40. The octave numbers are scientific, as in MUS-007: middle C is C4, MIDI 60.

In the language of MAT-004, the tuning is a vector with one entry per string, t = (t₁, …, t₆) = (64, 59, 55, 50, 45, 40). Each fret adds a semitone, so string s at fret f sounds t_s + f. A chord shape is a vector of frets, one per string. Guitarists write it from string 6: in the open E shape 022100, strings 6 to 1 are at frets 0, 2, 2, 1, 0 and 0. Listed string 1 first, like t, the shape is (0, 0, 1, 2, 2, 0), and the pitches it sounds are the sum of the two vectors: (64, 59, 56, 52, 47, 40). Read from string 6, that is 40, 47, 52, 56, 59 and 64, or E2, B2, E3, G♯3, B3 and E4.

The differences between neighbouring entries are the intervals between the strings. From string 6 up, they are 5, 5, 5, 4 and 5 semitones: perfect fourths, except the major third from string 3 to string 2. So fret 5 of a string sounds the next open string up, except on string 3, where fret 4 does.

### Practice Exercise

In the F barre shape 133211, written from string 6, which pitches do strings 6 and 3 sound?

> *Solution:* String 6 is at fret 1: 40 + 1 = 41, F2. String 3 is at fret 2: 55 + 2 = 57, A3, the major third of the chord.

---

## 2. One Pitch, Many Places

A pitch p can be played on string s when the fret it needs, p − t_s, lies between 0 and the number of frets. GA's default guitar has 24 frets. On it, A4, MIDI 69, has five places: string 1 at fret 5, string 2 at fret 10, string 3 at fret 14, string 4 at fret 19 and string 5 at fret 24. String 6 would need fret 29. On a guitar with 22 frets, string 5 drops out and A4 has four places.

The same count works for every pitch. A 24-fret guitar in standard tuning reaches from E2, MIDI 40, to E6, MIDI 64 + 24 = 88: 49 pitches. Of these, 10 have one place, 9 have two, 10 have three, 9 have four and 10 have five. Only one pitch can be played on all six strings: E4, the open first string, which string 6 reaches at fret 24. The pitches with one place are the five lowest, E2 to G♯2, which only string 6 has, and the five highest, C6 to E6, which only string 1 reaches.

A pitch is not a pitch class. The pitch class A, in any octave, has 13 places on the same neck: A2 has 2, A3 has 4, A4 has 5 and A5 has 2. A fingering chart that marks "every A" shows all 13; a guitarist asked for A4 needs the 5.

### Practice Exercise

How many places does E4 have on a guitar with 22 frets, and on which frets?

> *Solution:* Five: string 1 open, string 2 at fret 5, string 3 at fret 9, string 4 at fret 14 and string 5 at fret 19. String 6 would need fret 24, which a 22-fret guitar does not have.

---

## 3. Changing the Tuning

An alternate tuning is a new vector t′, and the difference Δ = t′ − t says, string by string, how many semitones each string was turned. In drop D, written D2 A2 D3 G3 B3 E4 from string 6, only string 6 changes, from E2 to D2: Δ = (0, 0, 0, 0, 0, −2), listed string 1 first like t. DADGAD, D2 A2 D3 G3 A3 D4, gives Δ = (−2, −2, 0, 0, 0, −2), and open G, D2 G2 D3 G3 B3 D4, gives Δ = (−2, 0, 0, 0, −2, −2).

What changes is confined to the strings where Δ is not zero. Every note on such a string moves: to keep a pitch, its fret becomes f − Δ_s. In drop D, E2 needs string 6 at fret 2, and the guitar now reaches down to D2, MIDI 38. A shape kept with the same frets sounds t′ plus the frets: the open E shape 022100 now has D2 in the bass. The interval from string 6 to string 5 becomes 7 semitones, a fifth, so strings 6, 5 and 4 at one fret give a root, fifth and octave: open, they sound D2, A2 and D3.

What stays is everything else. The other strings, the rule t_s + f and the frets themselves are unchanged, and so is the count of places for any pitch the changed strings reach in neither tuning: in drop D, A4 still has its five places.

MAT-004's norms measure a retuning. The 1-norm ‖Δ‖₁ adds up the semitones turned, 2 for drop D and 6 for DADGAD and open G. The ∞-norm ‖Δ‖∞ is the largest turn on one string, 2 for all three. That one matters to the string: by PHY-001's formula, at a fixed length the tension of a string goes with the square of its frequency, so lowering a string by k semitones multiplies its tension by 2^(−2k/12). Two semitones down leave it about 0.79 of its tension.

### Practice Exercise

Open D is D2 A2 D3 F♯3 A3 D4, from string 6. Give its Δ, its two norms, and the strings that keep their pitch.

> *Solution:* t′ = (62, 57, 54, 50, 45, 38), so Δ = (−2, −2, −1, 0, 0, −2): ‖Δ‖₁ = 7 and ‖Δ‖∞ = 2. Strings 4 and 5 keep their pitch.

---

## 4. Where the Frets Go

With the same tension and the same string, the frequency of a vibrating string is inversely proportional to its length, as PHY-001 shows. One semitone multiplies the frequency by 2^(1/12), so the string must be 2^(−1/12) times as long. Call L the **scale length**, the vibrating length of the open string, from the nut to the saddle. At fret n the string still vibrates over L · 2^(−n/12), so the fret lies at a distance from the nut of

d(n) = L · (1 − 2^(−n/12)).

The 12th fret halves the string: d(12) = L/2. The 24th leaves a quarter: d(24) = 3L/4. On a 648 mm scale, frets 1, 5, 7, 12 and 24 lie 36.4, 162.5, 215.5, 324 and 486 mm from the nut. The frets are not evenly spaced. Each space is 2^(−1/12), about 0.944, times the one before, so the space from fret 12 to fret 13, 18.2 mm, is half the first one. Put another way, the space after each fret is 1/17.817 of the length still vibrating from that fret to the saddle, since 1/(1 − 2^(−1/12)) is about 17.817.

The scale length changes the distances, not the proportions: on any scale the 12th fret is at half the string, 314 mm on a 628 mm scale and 432 mm on an 864 mm bass. Some frets land close to simple fractions of the string. On a 648 mm scale, fret 7 is 0.5 mm short of a third, 216 mm, and fret 5 is 0.5 mm past a quarter, 162 mm. A third and a quarter of the string are where the third and fourth harmonics are played, as PHY-001 plays the second at the 12th fret.

### Practice Exercise

On a 628 mm scale, where is the 12th fret, and how far is the first fret from the nut?

> *Solution:* The 12th fret is at 628/2 = 314 mm. The first fret is at 628 · (1 − 2^(−1/12)), about 35.2 mm.

---

## 5. Where GA Stands

GA is the music-theory library and chatbot of the GuitarAlchemist ecosystem. The facts below are read from its code at commit [`5c3a52a`](https://github.com/GuitarAlchemist/ga/tree/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26); this lesson documents that code and does not change it, and it has not run GA or its tests. The files it cites are unchanged on GA's `main` at `8fe33f8`. Learn, the ecosystem's course site, has a music-theory-ga course whose lessons [1](https://github.com/spareilleux/learn/blob/6c78aad43cb932323cf74933b4fb36121e5cb9a3/src/content/docs/music-theory-ga/01-notes-and-the-fretboard.mdx) and [8](https://github.com/spareilleux/learn/blob/6c78aad43cb932323cf74933b4fb36121e5cb9a3/src/content/docs/music-theory-ga/08-ukulele-and-bass.mdx) compile an earlier version of GA, `a826864`. The other numbers below come from a line-by-line Python transcription of the GA code named.

**Tunings and positions follow §1 and §2.** [`Tuning.Default`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Instruments/Tuning.cs#L23) parses "E2 A2 D3 G3 B3 E4" and stores string 1 first. To tell which end of a written tuning is string 1, it [counts the rising and falling steps](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Instruments/Tuning.cs#L121) between neighbouring strings, so that a re-entrant tuning, whose strings, counted from string 1, are not in falling order of pitch, is read in the direction it is written. Learn's lesson 8 recorded the [5-string banjo](https://github.com/spareilleux/learn/blob/6c78aad43cb932323cf74933b4fb36121e5cb9a3/code/music-theory-ga/expected/l8.txt#L29) as a difference: GA `a826864` took the drone, the short G4 string that players number 5, for string 1. Commit `4e23984` changed the rule, and GA's tests now expect [D4 as string 1](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Tests/GA.Domain.Core.Tests/Instruments/TuningTests.cs#L47). [`Fretboard.GetNote`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Instruments/Primitives/Fretboard.cs#L48) adds the fret to the [open string's MIDI note](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Instruments/Primitives/Fretboard.cs#L62), as in §1, then [returns only the note](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Instruments/Primitives/Fretboard.cs#L67), without its octave: string 1 and string 6, open, both give E. It takes a string index from 0, and index 0 is string 1, the high E, as GA's [tests](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Tests/GA.Domain.Core.Tests/Instruments/FretboardTests.cs#L11) say. Its own comment says the opposite: ["0 = lowest string"](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Instruments/Primitives/Fretboard.cs#L45). The default fretboard has [24 frets](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Instruments/Primitives/Fretboard.cs#L109).

[`GetPositionsForNote`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Instruments/Primitives/Fretboard.cs#L76) takes a note without an octave and [compares pitch classes](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Instruments/Primitives/Fretboard.cs#L82). It answers the pitch-class question of §2, not the pitch question: for A on the default fretboard it returns 13 positions, by transcription. Each one [carries its MIDI note](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Instruments/Primitives/Fretboard.cs#L87), and keeping those equal to 69 leaves the five places of A4. In Learn's lesson 1, GA `a826864` still compared whole notes and found [no position](https://github.com/spareilleux/learn/blob/6c78aad43cb932323cf74933b4fb36121e5cb9a3/code/music-theory-ga/expected/l1.txt#L61) for `Note.Sharp.C`, which never equals the chromatic note `GetNote` returns; commit `3a7c242` switched to pitch classes. A drop D fretboard is built from its pitches, as Learn's lesson 1 does for its [drop D exercise](https://github.com/spareilleux/learn/blob/6c78aad43cb932323cf74933b4fb36121e5cb9a3/code/music-theory-ga/expected/l1.txt#L78).

**Fret distances follow §4.** [`CalculateFretPositionMm`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Services/Fretboard/Analysis/PhysicalFretboardCalculator.cs#L35) computes [L · (1 − 2^(−n/12))](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Services/Fretboard/Analysis/PhysicalFretboardCalculator.cs#L42), with a [default scale length](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Services/Fretboard/Analysis/PhysicalFretboardCalculator.cs#L334) of [648 mm](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Services/Fretboard/Analysis/PhysicalFretboardCalculator.cs#L331). By transcription it gives §4's distances, 324 mm at fret 12 and 486 at fret 24. Two limits sit around it:

- [`CalculateStringSpacingMm`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Services/Fretboard/Analysis/PhysicalFretboardCalculator.cs#L78) widens the neck in a straight line from 43 mm at the nut to 52 mm at the saddle, then [divides by 5](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Services/Fretboard/Analysis/PhysicalFretboardCalculator.cs#L87), the gaps between six strings, whatever the instrument: 8.6 mm at the nut, 9.5 at fret 12.
- The voicing analyser measures a voicing's span with [`CalculateFretDistanceMm`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Services/Fretboard/Voicings/Analysis/VoicingPhysicalAnalyzer.cs#L103) and passes no scale length, so every span is measured at 648 mm.

The calculator's test file is [removed from compilation](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Tests/Common/GA.Business.Core.Tests/GA.Business.Core.Tests.csproj#L47), and no compiled test calls its distance methods directly: the voicing analyser's tests reach `CalculateFretDistanceMm` through `CalculatePlayability` and check the difficulty and chord shape it returns. The file would not compile as it stands: it calls [`CalculateStringSpacingMM`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Tests/Common/GA.Business.Core.Tests/Fretboard/PhysicalFretboardCalculatorTests.cs#L169), a name the class does not have. It also writes the MIDI note of each of its 41 positions by hand, and by t_s + f, 8 of them are wrong. In its open E chord, string 3 at fret 1 is [written 55](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Tests/Common/GA.Business.Core.Tests/Fretboard/PhysicalFretboardCalculatorTests.cs#L62), G3, where it sounds G♯3, 56. The playability analysis reads only strings and frets, so these numbers would not change a result.

**The tuning catalogue holds two octave errors.** Since commit `49bd286`, GA reads the whole of [`Instruments.yaml`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Business.Config/InstrumentsConfig.fs#L34), and `InstrumentTool.GetTuning`, a tool of GA's MCP server, through which AI assistants call GA, [returns a tuning's line](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/GaMcpServer/Tools/InstrumentTool.cs#L27) as written. Of the 11 six-string tunings it lists under `Guitar`, 9 have ‖Δ‖∞ of 2 or less against standard. The other two put string 2 an octave low:

- [`OpenCMajor`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Business.Config/Instruments.yaml#L536) is "C2 G2 C3 G3 C3 E4". Open C, C2 G2 C3 G3 C4 E4, gives Δ = (0, 1, 0, −2, −2, −4), with ‖Δ‖∞ = 4: it raises string 2 a semitone, from B3 to C4. The catalogue's line gives Δ = (0, −11, 0, −2, −2, −4): its C3 would lower string 2 by 11 semitones, to 2^(−22/12), about 0.28 of its tension.
- [`OpenAMajor`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Business.Config/Instruments.yaml#L560) is "E2 A2 E3 A3 C#3 E4", whose C♯3 lowers string 2 by 10 semitones.

Code that compares tunings by pitch class cannot see such an error. GA's alternate-tunings skill, for its own nine tunings, [reduces each difference mod 12](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Business.ML/Agents/Skills/AlternateTuningsSkill.cs#L257) and [folds it](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Business.ML/Agents/Skills/AlternateTuningsSkill.cs#L258) into −5 to +6: from B to C it would report +1, with or without the octave error.

Fixing any of this is for GA's owners; this lesson only describes it.

### Practice Exercise

GA's catalogue writes open A as E2 A2 E3 A3 C♯3 E4. Open A raises strings 4, 3 and 2 a whole tone from standard. Give Δ for both, and say which entry gives the error away.

> *Solution:* Open A is E2 A2 E3 A3 C♯4 E4: Δ = (0, 2, 2, 2, 0, 0), with ‖Δ‖∞ = 2. The catalogue's line gives Δ = (0, −10, 2, 2, 0, 0), with ‖Δ‖∞ = 10. The second entry, string 2 turned down 10 semitones, gives it away.

---

## 6. Proposed Experiment (Not Yet Run)

**Status: not run.** This section proposes an experiment for Learn's music-theory-ga lab, which compiles GA; the lab's GA pin would first move to `5c3a52a`. Nothing in it is a measurement. The predictions come from §2 to §5 and are written down before any run; a later version of this lesson will report the results. Every step calls GA's types in the lab's own process, never a running MCP server or a language model.

1. **Places of every pitch.** On the default fretboard, for each MIDI note from 40 to 88, keep the positions `GetPositionsForNote` returns for its pitch class that carry that MIDI note. Prediction: 10 pitches have one place, 9 two, 10 three, 9 four, 10 five, and E4 alone six.
2. **A4 in two tunings.** Ask for A on the default fretboard and on a 24-fret drop D fretboard. Prediction: 13 positions on each, and the same 5 with MIDI note 69.
3. **String index and octave.** Call `GetNote(0, 0)` and `GetNote(5, 0)`, then keep the open-string positions `GetPositionsForNote` returns for E. Prediction: E both times, with no octave; the positions are string 1 with MIDI note 64 and string 6 with 40, so index 0 is the high string.
4. **Fret distances.** Compare `CalculateFretPositionMm(n)` with L · (1 − 2^(−n/12)) for n from 0 to 24 at 648 mm. Prediction: equal up to rounding, with 324 at fret 12 and 486 at fret 24.
5. **The catalogue.** Read the six-string tunings listed under `Guitar` in `Instruments.yaml` through `InstrumentsConfig`, parse each one, and compute its Δ against standard. Prediction: 11 tunings; 9 with ‖Δ‖∞ of 2 or less, `OpenCMajor` with 11 and `OpenAMajor` with 10.

### Practice Exercise

Step 5 flags tunings by ‖Δ‖∞. Why not by ‖Δ‖₁?

> *Solution:* ‖Δ‖₁ adds the turns of all six strings, so many small, ordinary turns add up. Tuning every string a whole step down, D2 G2 C3 F3 A3 D4, gives ‖Δ‖₁ = 12, close to the 14 of the catalogue's open A line. ‖Δ‖∞ separates them, 2 against 10: it looks at the largest single turn, which is what an octave error makes large and what a string's tension depends on.

---

## 7. Common Pitfalls

- **Numbering the strings from the bass.** String 1 is the thinnest, highest-sounding string.
- **Counting places of a pitch class.** On a 24-fret guitar, A has 13 places; A4 has 5.
- **Moving every shape for a new tuning.** Only the strings where Δ is not zero change.
- **Spacing the frets evenly.** Each space is about 0.944 times the one before; the 12th fret is at half the string.
- **Scaling the proportions with the scale length.** A longer scale moves every fret, but the 12th fret stays at half.
- **Reading a tuning as pitch classes.** An octave error on one string is invisible mod 12.
- **Trusting `GetNote`'s comment.** In GA, string index 0 is the high E, not the lowest string.

---

## Key Terms

| Term | Definition |
|------|-----------|
| **String number** | The rank of a string counted from the treble side: string 1 is the thinnest |
| **Tuning vector** | The MIDI numbers of the open strings, t = (t₁, …, t₆); string s at fret f sounds t_s + f |
| **Place** | A string and a fret that play a given pitch; a pitch class has the places of all its octaves |
| **Retuning vector** | Δ = t′ − t, the semitones each string is turned; ‖Δ‖₁ adds them, ‖Δ‖∞ takes the largest |
| **Scale length** | The vibrating length of an open string, from the nut to the saddle |
| **Fret position** | The distance of fret n from the nut, d(n) = L · (1 − 2^(−n/12)) |
| **Re-entrant tuning** | A tuning whose strings, counted from string 1, are not in falling order of pitch: some string sounds higher than the one before it |

---

## Self-Check Assessment

**1. Where is the 12th fret on a 648 mm scale?**
> At 324 mm from the nut: d(12) = 648 · (1 − 1/2).

**2. On a 24-fret guitar in standard tuning, where can you play A4?**
> In five places: string 1 at fret 5, string 2 at fret 10, string 3 at fret 14, string 4 at fret 19 and string 5 at fret 24.

**3. Give drop D's retuning vector and its two norms.**
> Δ = (0, 0, 0, 0, 0, −2), string 1 first: ‖Δ‖₁ = 2 and ‖Δ‖∞ = 2.

**4. By transcription, GA's [`GetPositionsForNote`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Instruments/Primitives/Fretboard.cs#L76) returns 13 positions for A on its default fretboard. Why more than five?**
> It compares pitch classes, so it returns every A from A2 to A5: 2, 4, 5 and 2 places. Only the 5 whose MIDI note is 69 play A4.

**Pass criteria:** Give the pitch of any string and fret from the tuning vector; find and count the places of a pitch; describe a retuning by its Δ and its norms; compute fret positions for any scale length; and tell GA's pitch-class positions from the pitch places of §2.

---

## Research Basis

- T. D. Rossing, F. R. Moore and P. A. Wheeler, *The Science of Sound*, 3rd ed., Addison-Wesley, 2002: vibrating strings and string instruments
- N. H. Fletcher and T. D. Rossing, *The Physics of Musical Instruments*, 2nd ed., Springer, 1998: the guitar
- GA source at commit `5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26`: every code fact in §5 links to its line
- Learn, music-theory-ga lessons 1 and 8 and their expected output at commit `6c78aad43cb932323cf74933b4fb36121e5cb9a3`: the compiled checks of GA `a826864` quoted in §5
- Experiment: proposed in §6, not run; this lesson contains no measurement of its own
- Provenance: hand-authored by a Claude Code session (Opus 5.5) from the Streeling curriculum plan, not produced by the Seldon course pipeline; under review
- Belief state: T(0.85) F(0.02) U(0.10) C(0.03)
