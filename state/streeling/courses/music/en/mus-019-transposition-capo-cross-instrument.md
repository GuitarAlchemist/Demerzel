---
module_id: mus-019-transposition-capo-cross-instrument
department: music
course: Transposition, the Capo and Cross-Instrument Equivalence
level: intermediate
alchemical_stage: albedo
prerequisites: [mus-009-tuning-fretboard-geometry, mus-020-set-classes-interval-vectors-prime-forms]
estimated_duration: "45 minutes"
produced_by: claude-code-hand-authored
version: "1.0.0"
---

# Transposition, the Capo and Cross-Instrument Equivalence — Three Kinds of Sameness

> **Department of Music** | Stage: Albedo (Intermediate) | Estimated duration: 45 minutes

## Objectives

After this lesson, you will be able to:
- Transpose a pitch, a chord, a progression or a key by n semitones, and spell the result in its new key
- Find the sounding key of a capo and its chord shapes, and the shapes and capo for a sounding key
- Say what a chord shape becomes on another instrument or another set of strings
- Write the key of a B♭, E♭ or F instrument's part for a concert key, and keep concert and written pitch apart
- Trace what GA computes for transposition and the capo, where its names or its reading of a question go wrong, and what it lacks

---

## 1. Transposition

Wikipedia's "Transposition (music)": "transposition refers to the process or operation of moving a collection of notes (pitches or pitch classes) up or down in pitch by a constant interval." For pitches, the interval is a number of semitones: A4, MIDI 69, moved up a major third, 4 semitones, is MIDI 73, C♯5. For pitch classes, the sum is taken mod 12: 9 + 4 = 13 ≡ 1. MUS-020 wrote this operation Tn: Tn adds n to every pitch class, mod 12.

A transposition keeps every interval, so it keeps every chord's quality and every chord's place in its key. T3 sends the C major triad {0, 4, 7} to {3, 7, 10}, E♭ major, and sends the progression C – Am – F – G, I – vi – IV – V in C major, to E♭ – Cm – A♭ – B♭, I – vi – IV – V in E♭ major. Each chord of the new progression is the T3-image of the old one.

Only a shift by a fixed number of semitones is a Tn. Wikipedia separates two kinds of shift:
- **Chromatic transposition.** In it, "every pitch in a collection of notes is shifted by the same number of semitones. For instance, transposing the pitches C4–E4–G4 upward by four semitones, one obtains the pitches E4–G♯4–B4."
- **Diatonic transposition.** Every pitch moves by the same number of steps of one scale: "transposing the pitches C4–E4–G4 up two steps in the familiar C major scale gives the pitches E4–G4–B4". The major triad has become E minor. The steps of a scale are not all the same size, so this is not a Tn.

Moving a song to another key is a chromatic transposition.

**Semitones do not fix the letters.** As MUS-007 showed, the same pitch class has several names. A transposition by n semitones is spelled by naming its interval, with a number and a quality, and moving the tonic by that interval. Three semitones up from C is a minor third, C D E, to E♭; or an augmented second, C D, to D♯. E♭ major has three flats; D♯ major would need nine sharps, counting each 𝄪 as two. When only the semitones are given, the key with fewer accidentals is the usual name.

The line of fifths of MUS-007 does the counting. Each perfect fifth up adds a sharp to the key signature or removes a flat, so an interval is worth a fixed number of fifths:

| Interval up | P5 | M2 | M6 | M3 | P4 | m7 | m3 | m6 |
|------|------|------|------|------|------|------|------|------|
| Fifths | +1 | +2 | +3 | +4 | −1 | −2 | −3 | −4 |

Transposing C major up a minor third moves its signature −3 places: from no accidental to three flats, E♭ major. G major, one sharp, up a major second gets three sharps, A major.

### Practice Exercise

Transpose G – Em – C – D7 up three semitones. Name the key and spell the chords.

> *Solution:* Three semitones up is a minor third, −3 fifths. G major has one sharp; one sharp and three flats leave two flats: B♭ major. The chords are B♭ – Gm – E♭ – F7. Spelled as A♯ major, the key would need ten sharps.

---

## 2. The Capo

Wikipedia's "Capo (musical device)" defines a capo as "a device a musician uses on the neck of a stringed (typically fretted) instrument to transpose and shorten the playable length of the strings—hence raising the pitch". Players use it "so they can play in a different key using the same fingerings as playing open (i.e., without a capo). In effect, a capo uses a fret of an instrument to create a new nut at a higher note than the instrument's actual nut."

In the language of MUS-009, the tuning is a vector t, and a string s at fret f sounds t_s + f. A capo at fret c makes every open string sound c semitones higher. The new tuning is t + (c, c, c, c, c, c), and the difference Δ is c on every string. A shape played with frets f counted from the capo sounds t + c + f: every note it plays moves up c semitones. The capo is T_c applied to everything the guitarist plays. Wikipedia: "Playing with a capo creates the same musical effect as retuning all strings up the same number of steps. However, using a capo only affects the open note of each string." Fretted notes do not change: with the capo at fret 3, fret 7 of string 6, counted from the nut, still sounds B2.

**Two names for one chord.** A chord can be named by the shape the fingers make or by what it sounds. Wikipedia: "a D-shaped chord can be referred to as "D" (based on the shape relative to the capo), or E (based on the absolute audible chord produced). Neither method strongly prevails over the other." That is why players say "chord shape" when they mean the fingering. With the capo at fret c:

- sounding = shape + c;
- shape = sounding − c.

This lesson's question is a guitarist's: with a capo at the 3rd fret, playing C shapes, what key does the audience hear, and what does a B♭ trumpet player read for the same song? With the capo at fret 3, the C shape x32010 is played at x65343 counted from the nut. It sounds E♭3 G3 B♭3 E♭4 G4: E♭ major, three semitones above C. The progression C – Am – F – G, played in shapes, sounds E♭ – Cm – A♭ – B♭. The sounding names are spelled in the sounding key, by §1's rule: C up a minor third is E♭, not D♯.

**Choosing a capo.** To sound in a key K with open shapes, take a key S that has easy open chords, C, A, G, E or D, and put the capo at fret K − S, mod 12. For E♭ major:

| Shapes | D | C | A | G | E |
|------|------|------|------|------|------|
| Capo at fret | 1 | 3 | 6 | 8 | 11 |

Wikipedia gives two such choices. In "Guitar", for a song in B major a player could "put a capo on the second fret of the instrument, and then play the song as if it were in the key of A Major". In "Capo (musical device)", two guitarists play I IV V in E: "the first guitarist plays E A B7 while the second plays the same progression capoed at the fourth fret using C F G7 chord-shapes". The second guitar sounds the same chords in other voicings.

The sounding key takes the name with fewer accidentals. G shapes with a capo at fret 4 sound B major, five sharps, rather than C♭ major, seven flats. D shapes at fret 4 sound F♯ major or G♭ major, six accidentals either way: a tie, and both names are in use.

**The partial capo.** A partial capo covers only some strings. Wikipedia's example covers "the top five strings of a guitar" and omits the low E: "When played at the second fret, this appears to create a drop D tuning (in which the bass E string is detuned to a D) raised one full tone in pitch." Listed string 1 first, Δ = (2, 2, 2, 2, 2, 0), and that is a whole-tone capo, (2, 2, 2, 2, 2, 2), plus drop D's (0, 0, 0, 0, 0, −2). The open strings sound E2 B2 E3 A3 C♯4 F♯4 from string 6: drop D, D2 A2 D3 G3 B3 E4, two semitones up.

### Practice Exercise

With a capo at fret 2, a guitarist plays G – C – D – Em shapes. What key does the audience hear? For a song in A♭ major, where does the capo go for G shapes, and for E shapes?

> *Solution:* A major, two semitones above G: the chords sound A – D – E – F♯m. For A♭ major: G shapes at fret 1, since 7 + 1 = 8, and E shapes at fret 4, since 4 + 4 = 8.

---

## 3. Same Shape, Another Instrument

A capo changes every string by the same amount, so a shape keeps its chord quality and moves by one Tn. Another instrument can be compared with the guitar in the same way, string by string, through the difference of the two tunings. Learn's music-theory-ga course works through these comparisons in [lesson 8](https://github.com/spareilleux/learn/blob/a0c78d95a4719fdc0df85052fe171c78cf204e2b/src/content/docs/music-theory-ga/08-ukulele-and-bass.mdx#L99-L161). Wikipedia's "Ukulele" gives the tunings:
- **Low G.** C6 linear tuning, "or "low G" tuning, which has the G in sequence an octave lower: G3–C4–E4–A4, which is equivalent to playing the top four strings (DGBE) of a guitar with a capo on the fifth fret."
- **High G.** The common C6 tuning, G4–C4–E4–A4: "The G string is tuned an octave higher than might be expected, so this is often called "high G" tuning. This is known as a "reentrant tuning"".
- **Baritone.** "The baritone ukulele usually uses linear G6 tuning: D3–G3–B3–E4, the same as the highest four strings of a standard 6-string guitar."

| Instrument | Strings 4 to 1 | Minus the guitar's strings 4 to 1 | The guitar's G shape on strings 4 to 1, 0003 |
|------|------|------|------|
| Guitar | D3 G3 B3 E4 | 0, 0, 0, 0 | D3 G3 B3 G4: G major |
| Ukulele, low G | G3 C4 E4 A4 | 5, 5, 5, 5 | G3 C4 E4 C5: C major, G in the bass |
| Ukulele, high G | G4 C4 E4 A4 | 17, 5, 5, 5 | G4 C4 E4 C5: C major, C in the bass |
| Baritone ukulele | D3 G3 B3 E4 | 0, 0, 0, 0 | D3 G3 B3 G4: G major |

- **The low-G ukulele.** Every difference is 5, so the ukulele is the guitar's top four strings with a capo at fret 5. Every shape sounds T5 of its guitar chord: the guitar's G shape is the ukulele's C chord, and the guitar's D shape, 0232, is its G.
- **The high-G ukulele.** The difference on string 4 is 17, an octave and a fourth. Mod 12 that is still 5, so the pitch classes and the chord names are those of the low G. The bass is not: the same C chord has its fifth in the bass on a low G and its root on a high G, a second inversion against a root position, in MUS-014's terms.
- **The baritone ukulele.** The difference is 0, so every shape keeps its guitar name.
- **The bass guitar.** Wikipedia's "Bass guitar" says it is tuned to "pitches one octave lower than the four lowest-pitched strings of a guitar, typically E, A, D, and G": E1 A1 D2 G2 against E2 A2 D3 G3, a difference of −12 on every string. That is T0 on pitch classes, so a fret on the bass's string 4 gives the note that the same fret on the guitar's string 6 gives, one octave lower.

**The same shape on other strings of one guitar.** Moving a shape to another set of strings keeps its sound only if the strings keep their intervals. As MUS-009 showed, the guitar's strings are a fourth apart except strings 3 and 2, a major third. The root-fifth-octave shape x355xx sounds C3 G3 C4. One string set higher, xx355x sounds F3 C4 E4: the octave has become a major seventh, and the shape must become xx356x to give F3 C4 F4.

### Practice Exercise

The shape 2210, on strings 4 to 1, is the top of the guitar's A minor chord. What does it sound on the guitar, on a low-G ukulele and on a high-G ukulele, and which note is in the bass?

> *Solution:* On the guitar, E3 A3 C4 E4: A minor with E, its fifth, in the bass. On a low-G ukulele, A3 D4 F4 A4: D minor, five semitones up, with A, its fifth, in the bass. On a high-G ukulele, A4 D4 F4 A4: D minor with D4 the lowest note, its root.

---

## 4. Transposing Instruments

Wikipedia's "Transposing instrument": "A transposing instrument is a musical instrument for which music notation is not written at concert pitch (concert pitch is the pitch on a non-transposing instrument such as the piano)." An instrument is named after what its written C sounds: "Playing a written C on clarinet or soprano saxophone produces a concert B♭ (i.e. B♭ at concert pitch), so these are referred to as B♭ instruments." The instrument changes nothing: "The instruments do not transpose the music; rather, their music is written at a transposed pitch. Where chords are indicated for improvisation they are also written in the appropriate transposed form."

| Instrument | A written C sounds | Sounding against written | To write a concert key, move it up | Concert E♭ major is written in |
|------|------|------|------|------|
| B♭ trumpet, B♭ clarinet | B♭ | a whole step lower | a major second (+2 fifths) | F major |
| E♭ alto saxophone | E♭ | a major sixth lower | a major sixth (+3 fifths) | C major |
| Horn in F | F | a perfect fifth lower | a perfect fifth (+1 fifth) | B♭ major |
| Guitar, bass guitar | C, an octave lower | an octave lower | an octave | E♭ major |

The sounding intervals are Wikipedia's. "Trumpet": "The most common type of trumpet is a transposing instrument in B♭, with pitches sounding a whole step lower than written." "Alto saxophone": "The alto saxophone is a transposing instrument, with pitches sounding a major sixth lower than written." "Transposing instrument" gives the horn "sounding a perfect fifth below written pitch in treble clef" and notes that "Double bass, bass guitar, guitar, and contrabassoon sound an octave lower than written." The guitar is itself a transposing instrument, at the octave.

Now the second half of the question. The song sounds in E♭ major: capo at fret 3, C shapes. Its chart in concert pitch reads E♭ – Cm – A♭ – B♭. Each part moves up by its instrument's interval, and §1's table of fifths gives the key signature: E♭ major has three flats, so +2 fifths leave one flat, F major.

| Part | Written key | Chart |
|------|------|------|
| Concert pitch | E♭ major | E♭ – Cm – A♭ – B♭ |
| B♭ trumpet | F major | F – Dm – B♭ – C |
| E♭ alto saxophone | C major | C – Am – F – G |
| Horn in F | B♭ major | B♭ – Gm – E♭ – F |
| Guitar, capo at fret 3, in shapes | C major | C – Am – F – G |

The alto saxophonist and the guitarist read the same chord names. The saxophone's part is written a major sixth above the sound, the guitarist's shapes a minor third below it, and 9 ≡ −3 mod 12: the two names land on the same pitch classes, in different octaves.

The three kinds of sameness can now be told apart:

| Relation | What stays the same | What changes | Example |
|------|------|------|------|
| Transposition Tn | The intervals, the chord qualities, the degrees of the key | Every pitch class, by n, and the letters | C – Am – F – G and E♭ – Cm – A♭ – B♭ |
| Same shape | The fingering | The sound, by the difference of the tunings: a Tn only when it is the same on every string | The G shape: G on a guitar, C on a ukulele |
| Same written note | The notation | The sound, by the instrument's transposition | A written C: B♭ on a trumpet, E♭ on an alto saxophone |

### Practice Exercise

A song is in concert B♭ major. In which keys do a B♭ trumpet, an E♭ alto saxophone and a horn in F read it? What does a written D sound on the trumpet?

> *Solution:* B♭ major has two flats. The trumpet's part moves +2 fifths: C major. The alto saxophone's moves +3: one sharp, G major. The horn's moves +1: one flat, F major. A written D sounds a whole step lower on the trumpet: C.

---

## 5. Where GA Stands

GA is the music-theory library and chatbot of the GuitarAlchemist ecosystem. The facts below are read from its code at commit [`e610b77`](https://github.com/GuitarAlchemist/ga/tree/e610b7714b9d6a1fe625b17fe6ca004380ca6752). This lesson documents that code and does not change it. It has not run GA or its tests. The files it cites are unchanged on GA's `main` at `7595983`. Where a result needs a computation, it comes from a line-by-line Python transcription of the code named: read, not run.

**Pitch-class sets transpose by rotation.** GA's `PitchClassSetId` writes a set as a 12-bit number, with bit p set for pitch class p, as in MUS-020. [`Transpose`](https://github.com/GuitarAlchemist/ga/blob/e610b7714b9d6a1fe625b17fe6ca004380ca6752/Common/GA.Domain.Core/Theory/Atonal/PitchClassSetId.cs#L82-L88) reduces n mod 12 and rotates the bits up n places, the top bits wrapping round to the bottom. C major, 145, becomes 1160 under T3: {3, 7, 10}, E♭ major. That is Tn exactly. [`Rotate`](https://github.com/GuitarAlchemist/ga/blob/e610b7714b9d6a1fe625b17fe6ca004380ca6752/Common/GA.Domain.Core/Theory/Atonal/PitchClassSetId.cs#L90) calls `Transpose`, with the comment "Rotation of PC set is transposition". The two test files that call `PitchClassSetId.Transpose` use it to check other code: that a [prime form does not change](https://github.com/GuitarAlchemist/ga/blob/e610b7714b9d6a1fe625b17fe6ca004380ca6752/Tests/GA.Domain.Core.Tests/Theory/Atonal/TranspositionClassTests.cs#L69-L82) under any of the 12 transpositions, and, through an [oracle built on it](https://github.com/GuitarAlchemist/ga/blob/e610b7714b9d6a1fe625b17fe6ca004380ca6752/Tests/Common/GA.Business.Core.Tests/Atonal/PitchClassSetCanonicalizationTests.cs#L16-L30), that prime forms are computed right. A second Tn, [`HarmonicTransformationService.Transpose`](https://github.com/GuitarAlchemist/ga/blob/e610b7714b9d6a1fe625b17fe6ca004380ca6752/Common/GA.Business.DSL/Services/HarmonicTransformationService.fs#L15-L16), adds n to each pitch class of a set, mod 12. No code outside the tests calls it, and [its test](https://github.com/GuitarAlchemist/ga/blob/e610b7714b9d6a1fe625b17fe6ca004380ca6752/Tests/Common/GA.Business.DSL.Tests/HarmonicTransformationTests.cs#L11-L22) checks the value: {0, 4, 7} up 2 is {2, 6, 9}.

**Chord symbols: the root moves, its letter and the bass do not follow.** [`domain.transposeChord`](https://github.com/GuitarAlchemist/ga/blob/e610b7714b9d6a1fe625b17fe6ca004380ca6752/Common/GA.Business.DSL/Closures/BuiltinClosures/DomainClosures.fs#L227-L252) parses a chord symbol and adds n to its root's pitch class. It names the new root from a sharp list or a flat list, chosen by the old root: by [`preferFlat`](https://github.com/GuitarAlchemist/ga/blob/e610b7714b9d6a1fe625b17fe6ca004380ca6752/Common/GA.Business.DSL/Closures/BuiltinClosures/DomainClosures.fs#L29-L37), flats for a flat root or for F, sharps otherwise, as MUS-007 found. Then it [replaces the root and nothing else](https://github.com/GuitarAlchemist/ga/blob/e610b7714b9d6a1fe625b17fe6ca004380ca6752/Common/GA.Business.DSL/Closures/BuiltinClosures/DomainClosures.fs#L250). A slash chord keeps its [bass](https://github.com/GuitarAlchemist/ga/blob/e610b7714b9d6a1fe625b17fe6ca004380ca6752/Common/GA.Business.DSL/Types/ChordAst.fs#L29), which the renderer [writes back after the slash](https://github.com/GuitarAlchemist/ga/blob/e610b7714b9d6a1fe625b17fe6ca004380ca6752/Common/GA.Business.DSL/Generators/ChordRenderer.fs#L35-L38): C/E up two semitones becomes `D/E`, not D/F♯, and G/B up three becomes `A#/B`, not B♭/D.

GA's command-line tool transposes a progression with `ga progression`, which calls the closure [chord by chord](https://github.com/GuitarAlchemist/ga/blob/e610b7714b9d6a1fe625b17fe6ca004380ca6752/Apps/GaCli/Program.fs#L239-L245). Read, not run, for C Am F G:

| `--by` | GA prints after the arrow | Spelled in the key |
|------|------|------|
| 1 | C# A#m Gb G# | D♭ B♭m G♭ A♭ |
| 3 | D# Cm Ab A# | E♭ Cm A♭ B♭ |
| 8 | G# Fm Db D# | A♭ Fm D♭ E♭ |
| 10 | A# Gm Eb F | B♭ Gm E♭ F |

The other seven shifts, from 1 to 11, give a spelling of their key. The pitch classes are right in every row: each chord is the Tn-image of the one it came from. The letters fail in D♭, E♭, A♭ and B♭ major, because each chord takes the side of its own old root: at `--by 1`, C# and G# stand beside Gb in one key.

The one test that transposes a chord through the closure, [`EvalClosure_TransposeWithIntCoercion_Succeeds`](https://github.com/GuitarAlchemist/ga/blob/e610b7714b9d6a1fe625b17fe6ca004380ca6752/Tests/Common/GA.Business.ML.Tests/Unit/DslEvalMcpToolsTests.cs#L188-L205), asks for C up three semitones. It checks that a result comes back, not what it is; by transcription it is `D#`. The chatbot's `TransposeSkill` has a language model call [the same closure](https://github.com/GuitarAlchemist/ga/blob/e610b7714b9d6a1fe625b17fe6ca004380ca6752/Common/GA.Business.ML/Agents/Skills/TransposeSkill.cs#L22).

GA's domain model holds a third transposition, [`ChordProgression.Transpose`](https://github.com/GuitarAlchemist/ga/blob/e610b7714b9d6a1fe625b17fe6ca004380ca6752/Common/GA.Domain.Services/Chords/ChordBuilderEx.cs#L189-L199). It moves each chord's root, but builds the new chord with [its old symbol](https://github.com/GuitarAlchemist/ga/blob/e610b7714b9d6a1fe625b17fe6ca004380ca6752/Common/GA.Domain.Core/Theory/Harmony/Chord.cs#L25-L42), so a transposed C Am F G still [prints](https://github.com/GuitarAlchemist/ga/blob/e610b7714b9d6a1fe625b17fe6ca004380ca6752/Common/GA.Domain.Services/Chords/ChordBuilderEx.cs#L201) `C | Am | F | G`. Nothing calls it, and no test covers it.

**The capo skill: right arithmetic, sharps by default, a narrow reader.** The chatbot answers capo questions with [`CapoSkill`](https://github.com/GuitarAlchemist/ga/blob/e610b7714b9d6a1fe625b17fe6ca004380ca6752/Common/GA.Business.ML/Agents/Skills/CapoSkill.cs#L6-L25): "Zero LLM calls — pure pitch-class arithmetic. Confidence = 1.0." Its arithmetic is §2's, [sounding = shape + n](https://github.com/GuitarAlchemist/ga/blob/e610b7714b9d6a1fe625b17fe6ca004380ca6752/Common/GA.Business.ML/Agents/Skills/CapoSkill.cs#L144) and [shape = sounding − n](https://github.com/GuitarAlchemist/ga/blob/e610b7714b9d6a1fe625b17fe6ca004380ca6752/Common/GA.Business.ML/Agents/Skills/CapoSkill.cs#L116), mod 12. It [names the result](https://github.com/GuitarAlchemist/ga/blob/e610b7714b9d6a1fe625b17fe6ca004380ca6752/Common/GA.Business.ML/Agents/Skills/CapoSkill.cs#L178-L184) from a sharp list, "Default: sharps (guitarist convention)", and [takes flats](https://github.com/GuitarAlchemist/ga/blob/e610b7714b9d6a1fe625b17fe6ca004380ca6752/Common/GA.Business.ML/Agents/Skills/CapoSkill.cs#L186-L191) only when the key or shape is typed with "♭" or a lower-case "b", or when a question that names a shape, as in "a C shape", contains the letters "flat" anywhere, even inside a longer word. So "Eb" takes flats and "EB" does not, though both are read as E♭; a B natural typed "b" takes them too. The skill accepts note letters in lower case, so for it the article in "a shape" names an A shape: "Capo 2, what does a shape sound like" is answered for an A shape, `B`. Its own summary promises ["Eb (C + 3st)"](https://github.com/GuitarAlchemist/ga/blob/e610b7714b9d6a1fe625b17fe6ca004380ca6752/Common/GA.Business.ML/Agents/Skills/CapoSkill.cs#L13) for a C shape with a capo at fret 3; by transcription, that question gets `D#`.

The skill reads a question with [two regular expressions](https://github.com/GuitarAlchemist/ga/blob/e610b7714b9d6a1fe625b17fe6ca004380ca6752/Common/GA.Business.ML/Agents/Skills/CapoSkill.cs#L52-L64), [the shape one first](https://github.com/GuitarAlchemist/ga/blob/e610b7714b9d6a1fe625b17fe6ca004380ca6752/Common/GA.Business.ML/Agents/Skills/CapoSkill.cs#L88-L106). By transcription, on the skill's own [ten example prompts](https://github.com/GuitarAlchemist/ga/blob/e610b7714b9d6a1fe625b17fe6ca004380ca6752/Common/GA.Business.ML/Agents/Skills/CapoSkill.cs#L33-L45):
- **Seven** get §2's answer.
- **"I play a C shape with capo 3 — what does it sound like"** gets the right pitch class, named `D#`.
- **"What's the sounding key if I play in G with capo on 5"** is read as a song that sounds in G. The skill answers "play a D shape"; the question asks for C, G + 5.
- **"What chord shape for B major with capo 4"** matches neither expression, so the skill declines. The answer is a G shape.

This lesson's own question, "With a capo at the 3rd fret, playing C shapes, what key does the audience hear?", is declined too: both expressions want "capo", then at most "on", "at" or "fret", then a number, as in "capo 3" or "capo at 3", and the shape expression wants the word "shape", not "shapes". A key written with "#" or "♭" can lose its sign: the key expression wants a word boundary right after the key, or after a "major", "minor", "maj" or "min" that follows it, and there is none between "#" or "♭" and a comma or a space. "Song is in F#, capo 2" is read as a song in F, and the skill answers "play a D# shape" where the answer is an E shape. "Song is in F# major, capo 2" gets the E shape. The skill's tests, in [`SkillDeclineTests`](https://github.com/GuitarAlchemist/ga/blob/e610b7714b9d6a1fe625b17fe6ca004380ca6752/Tests/Common/GA.Business.ML.Tests/Unit/SkillDeclineTests.cs#L17-L33), check that an unrelated message is declined and that capo 25 gets an error rather than a decline. The transcription agrees with both, and no test checks an answer. The chatbot's evaluation corpus [skips its one capo prompt](https://github.com/GuitarAlchemist/ga/blob/e610b7714b9d6a1fe625b17fe6ca004380ca6752/Tests/Apps/GaChatbot.Api.Tests/Corpus/prompts.yaml#L534-L537), "Transpose this progression to capo 3", until a progression tool exists. GA's backlog [lists that tool as not done](https://github.com/GuitarAlchemist/ga/blob/e610b7714b9d6a1fe625b17fe6ca004380ca6752/BACKLOG.md#L196).

**Voicings, other instruments, and what is absent.**
- **Voicing documents.** GA's voicing-document factory takes a [`capo` argument](https://github.com/GuitarAlchemist/ga/blob/e610b7714b9d6a1fe625b17fe6ca004380ca6752/Common/GA.Business.ML/Rag/VoicingDocumentFactory.cs#L16). It uses it only in the document's [identifier](https://github.com/GuitarAlchemist/ga/blob/e610b7714b9d6a1fe625b17fe6ca004380ca6752/Common/GA.Business.ML/Rag/VoicingDocumentFactory.cs#L29), and no caller passes one.
- **The instrument catalogue.** It writes the bass guitar as [E1 A1 D2 G2](https://github.com/GuitarAlchemist/ga/blob/e610b7714b9d6a1fe625b17fe6ca004380ca6752/Common/GA.Business.Config/Instruments.yaml#L157) and the ukulele's C tuning as [G4 C4 E4 A4](https://github.com/GuitarAlchemist/ga/blob/e610b7714b9d6a1fe625b17fe6ca004380ca6752/Common/GA.Business.Config/Instruments.yaml#L1113), both as in §3. Learn's lesson 8 compiled an earlier GA, `a826864`, and [read this catalogue](https://github.com/spareilleux/learn/blob/a0c78d95a4719fdc0df85052fe171c78cf204e2b/src/content/docs/music-theory-ga/08-ukulele-and-bass.mdx#L186-L225). It found the ukulele line with a stray `C6` in front, which is gone at `e610b77`. It also found two baritone ukulele lines, which are unchanged: [D4 G3 B4 E4](https://github.com/GuitarAlchemist/ga/blob/e610b7714b9d6a1fe625b17fe6ca004380ca6752/Common/GA.Business.Config/Instruments.yaml#L1120) and [D4 G3 B3 E4](https://github.com/GuitarAlchemist/ga/blob/e610b7714b9d6a1fe625b17fe6ca004380ca6752/Common/GA.Business.Config/Instruments.yaml#L1434), where §3 has D3 G3 B3 E4. Both have the guitar's pitch classes, so code that compares pitch classes cannot see the difference.
- **Transposing instruments.** They are absent. At `e610b77`, nothing in GA's repository says "transposing instrument" or "written pitch", and "concert pitch" appears once, in the [range of an 8-string guitar tuning](https://github.com/GuitarAlchemist/ga/blob/e610b7714b9d6a1fe625b17fe6ca004380ca6752/Common/GA.Business.Config/SpecializedTunings.yaml#L243). In GA's C#, F#, TypeScript, JavaScript, Python and YAML files, the words "saxophone" and "clarinet" appear once, in a line that puts an instrument whose name contains them, or "flute", in the ["Wind" family](https://github.com/GuitarAlchemist/ga/blob/e610b7714b9d6a1fe625b17fe6ca004380ca6752/GA.Data.MongoDB/Services/InstrumentService.cs#L120). §4 is taught as theory.

Fixing any of this is for GA's owners; this lesson only describes it.

### Practice Exercise

By transcription, what does `CapoSkill` answer to "I play an F shape with capo 1, what does it sound like", and to "I play a D shape with capo 1, what does it sound like"? Are the names right?

> *Solution:* "F#" and "D#". F♯ is fine: F♯ major and G♭ major both have six accidentals. D♯ is not: the key is E♭ major, three flats, where D♯ major would need nine sharps. Neither question has a flat in it, so the skill uses its sharp list both times.

---

## 6. Proposed Experiment (Not Yet Run)

**Status: not run.** This section proposes an experiment for Learn's music-theory-ga lab, which compiles GA. The lab's GA pin would first move to `e610b77`. Nothing in this section is a measurement:
- the predictions come from §5 and are written down before any run;
- they come from a line-by-line Python transcription of `PitchClassSetId.Transpose`, of `domain.transposeChord` with the chord parser and renderer, and of `CapoSkill`;
- a later version of this lesson will report the results.

Every step calls GA's code in the lab's own process, never a running MCP server or a language model.

1. **Every set, every n.** For every `PitchClassSetId` from 0 to 4095 and every n from 0 to 11, compare `Transpose(n)` with the set of the pitch classes p + n mod 12, and check that `Transpose(12 − n)` brings the set back. Prediction: all 49,152 pairs pass both checks; 145 gives 1160 for n = 3.
2. **One progression, every n.** Through GA's closure registry, invoke `domain.transposeChord` on C, Am, F and G for every n from 1 to 11, and on C/E with n = 2 and G/B with n = 3. Parse each transposed chord of the progression with `Chord.FromSymbol` and compare its pitch classes with the original's moved by n. Prediction: the names of §5's table, with D♭, E♭, A♭ and B♭ major misspelled and the other seven shifts correct; every pitch-class set a Tn-image; `D/E` and `A#/B`.
3. **The capo skill.** Call `CapoSkill.ExecuteAsync` on its ten example prompts and on this lesson's question, and record `Declined` and the first line of `Result`. Prediction: as in §5. Seven answers agree with §2, the C shape with a capo at fret 3 sounds `D#`, "play in G with capo on 5" gets a D shape, and the B major prompt and this lesson's question are declined.

### Practice Exercise

Step 2 predicts `Ab` for F up three semitones and `D#` for C. Why does F get a flat and C a sharp, and what should both be?

> *Solution:* `preferFlat` gives the flat list to a flat root and to F, the one natural root whose major key has a flat, B♭; C gets the sharp list. Both chords land in E♭ major, where they should be A♭ and E♭: the new key should choose the side, not the old root.

---

## 7. Common Pitfalls

- **Spelling a transposition by its semitones alone.** Three semitones up from C is E♭ in a key change, a minor third, not D♯.
- **Taking a diatonic shift for a transposition.** C E G up two steps of C major is E G B, a minor triad: not a Tn.
- **Naming a chord without saying which name.** At capo 2, a "D" may be the shape or the sound: say "D shape" or "sounds E".
- **Moving the fretted notes with the capo.** The capo raises the open strings only; fret 7 of string 6 is B2 with or without a capo at a lower fret.
- **Expecting a shape to keep its chord on every instrument.** On a low-G ukulele it sounds a fourth higher; on one guitar, a shape that moves across strings 3 and 2 changes.
- **Reading a transposing instrument's part at concert pitch.** A written C on a B♭ trumpet sounds B♭.
- **Trusting GA's names for a transposed chord.** `domain.transposeChord` names the new root from sharps unless the old root is flat or F, and `CapoSkill` unless the question meets one of the conditions for flats in §5; `domain.transposeChord` also leaves a slash chord's bass where it was.

---

## Key Terms

| Term | Definition |
|------|-----------|
| **Transposition, Tn** | Adding n semitones to every pitch, or n mod 12 to every pitch class |
| **Chromatic and diatonic transposition** | A shift by a fixed number of semitones, or by a fixed number of steps of one scale |
| **Capo** | A clamp across the strings at a fret, a new nut: every open string rises by the same number of semitones |
| **Chord shape** | A chord named by its fingering relative to the capo, not by its sound |
| **Concert pitch** | The pitch that sounds, which a non-transposing instrument such as the piano writes as it is |
| **Transposing instrument** | An instrument whose part is written at another pitch than it sounds: the B♭ trumpet, the E♭ alto saxophone, the horn in F, and the guitar and bass guitar at the octave |
| **Re-entrant tuning** | A tuning whose strings are not in order of pitch, such as the ukulele's high G |

---

## Self-Check Assessment

**1. A guitarist plays G – Em – C – D shapes with a capo at fret 3. What does the audience hear, and in which key?**
> B♭ – Gm – E♭ – F, in B♭ major. Each chord moves up a minor third, and B♭ major has two flats where A♯ major would need ten sharps.

**2. A song sounds in A major. Give two capo positions with open shapes.**
> G shapes at fret 2, since 7 + 2 = 9, or E shapes at fret 5, since 4 + 5 = 9. D shapes at fret 7 and C shapes at fret 9 also work.

**3. The song of question 2 has a B♭ trumpet and an E♭ alto saxophone. In which keys do they read?**
> A major has three sharps. The trumpet's part moves +2 fifths, to five sharps: B major. The alto saxophone's moves +3, to six sharps: F♯ major.

**4. By transcription, what does GA's `domain.transposeChord` return for C/E up two semitones, and what should it return?**
> `D/E`: only the root moves. It should return D/F♯.

**5. Why does a guitar shape sound a fourth higher on a low-G ukulele and the same on a baritone ukulele?**
> The low-G ukulele's strings, G3 C4 E4 A4, are the guitar's top four, D3 G3 B3 E4, raised five semitones each: the same difference on every string, like a capo at fret 5. The baritone's strings are those four strings exactly, a difference of 0.

**Pass criteria:** Transpose a pitch, a chord, a progression or a key, and spell the result in its key. Go from capo and shapes to the sounding key and back. Say what a shape becomes on another instrument or another set of strings. Write the key of a B♭, E♭ or F part for a concert key. Say where GA's transposition and capo answers are right, and where their names or their reading of a question fail.

---

## Research Basis

- Wikipedia, "Transposition (music)": the definition, Tn on pitch classes, pitch and pitch-class transposition, and chromatic against diatonic transposition.
- Wikipedia, "Capo (musical device)": the new nut, the same effect as retuning every string, the shape name against the sounding name, the E A B7 and C F G7 example, and the partial capo.
- Wikipedia, "Guitar": the capo at the second fret for B major with A shapes.
- Wikipedia, "Ukulele": the high-G and low-G C6 tunings, the low G as a guitar's top four strings with a capo at the fifth fret, and the baritone's D3–G3–B3–E4.
- Wikipedia, "Bass guitar": tuned an octave below the guitar's four lowest strings.
- Wikipedia, "Transposing instrument": the definition, B♭ instruments, transposed chord symbols, the horn in F, and the guitar and bass guitar at the octave.
- Wikipedia, "Trumpet" and "Alto saxophone": a whole step and a major sixth below written.
- GA source at commit `e610b7714b9d6a1fe625b17fe6ca004380ca6752`: every code fact in §5 links to its line.
- Learn, music-theory-ga lesson 8 at commit `a0c78d95a4719fdc0df85052fe171c78cf204e2b`: the ukulele and bass comparisons, and its reading of GA's catalogue at `a826864`.
- Named by the Streeling curriculum plan and not consulted for this version: Adler, *The Study of Orchestration* (4th ed.), the chapter on transposing instruments.
- Experiment: proposed in §6, not run; this lesson contains no measurement of its own.
- Provenance: hand-authored by a Claude Code session (Opus 5.5) from the Streeling curriculum plan, not produced by the Seldon course pipeline; under review.
- Belief state: T(0.85) F(0.02) U(0.10) C(0.03).
