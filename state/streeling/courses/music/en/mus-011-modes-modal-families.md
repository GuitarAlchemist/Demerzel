---
module_id: mus-011-modes-modal-families
department: music
course: Modes and Modal Families
level: intermediate
alchemical_stage: albedo
prerequisites: [mus-010-scales-pattern-set-interval-vector, mus-020-set-classes-interval-vectors-prime-forms]
estimated_duration: "60 minutes"
produced_by: claude-code-hand-authored
version: "1.0.0"
---

# Modes and Modal Families — Rotation Versus a Shared Interval Vector

> **Department of Music** | Stage: Albedo (Intermediate) | Estimated duration: 60 minutes

## Objectives

After this lesson, you will be able to:
- Build the modes of a scale by rotating its step pattern, and name the seven modes of the major scale
- Tell relative modes, which keep the notes and change the tonic, from parallel modes, which keep the tonic and change the notes, and play both on the guitar
- Count the distinct modes of a scale, including the scales of limited transposition
- Explain why two scales with the same interval-class vector need not be modes of each other: mirror images and the Z-relation
- Trace how GA builds its modal families, and read what Learn's lab has already measured

---

## 1. Modes as Rotations

MUS-010 described a scale by its step pattern. Reading the same pattern from another step gives a **mode**. Wikipedia's "Mode (music)" puts it this way: "Modern Western modes use the same set of notes as the major scale, in the same order, but starting from one of its seven degrees in turn as a tonic, and so present a different sequence of whole and half steps."

| Mode | Step pattern | On its degree of C major |
|------|------|------|
| Ionian | 2 2 1 2 2 2 1 | C D E F G A B |
| Dorian | 2 1 2 2 2 1 2 | D E F G A B C |
| Phrygian | 1 2 2 2 1 2 2 | E F G A B C D |
| Lydian | 2 2 2 1 2 2 1 | F G A B C D E |
| Mixolydian | 2 2 1 2 2 1 2 | G A B C D E F |
| Aeolian | 2 1 2 2 1 2 2 | A B C D E F G |
| Locrian | 1 2 2 1 2 2 2 | B C D E F G A |

Each pattern is the one above it with its first step moved to the end: a **rotation**. A mode is fixed by its pattern, not by its notes: "transposition preserves mode", so D Dorian, C Dorian and F♯ Dorian are all Dorian. Ionian is the major scale and Aeolian the natural minor.

Any scale has modes in the same sense. "Other heptatonic scales also have seven modes each", and Wikipedia gives the example of melodic minor harmony, "based on the seven rotations of the ascending melodic minor scale".

### Practice Exercise

Write the step pattern of the fourth mode of the major pentatonic, 2 2 3 2 3, and spell it on C.

> *Solution:* The fourth mode starts with the pattern's fourth step: 2 3 2 2 3. On C, the steps 2, 3, 2 and 2 reach D, F, G and A, and the last step of 3 returns to C: C D F G A. It is the major pentatonic C D E G A read from G, its fourth note, and moved to C.

---

## 2. Relative and Parallel Modes

Modes can be compared in two ways.

**Relative modes keep the notes.** D Dorian and G Mixolydian are both played on the white notes: D Dorian is C major read from D, G Mixolydian is C major read from G. Wikipedia's "Relative key" says the same of a major key and its relative minor: they "share all of the same notes but are arranged in a different order of whole steps and half steps".

**Parallel modes keep the tonic.** C Dorian and C Mixolydian both start on C, but their notes differ. Wikipedia's "Parallel key" calls a major and a minor scale with "the same starting note (tonic)" parallel keys. The seven parallel modes on C borrow the notes of seven different major scales:

| Mode on C | Notes | Notes of | Lowered from Lydian |
|------|------|------|------|
| C Lydian | C D E F♯ G A B | G major | none |
| C Ionian | C D E F G A B | C major | 4 |
| C Mixolydian | C D E F G A B♭ | F major | 4, 7 |
| C Dorian | C D E♭ F G A B♭ | B♭ major | 4, 7, 3 |
| C Aeolian | C D E♭ F G A♭ B♭ | E♭ major | 4, 7, 3, 6 |
| C Phrygian | C D♭ E♭ F G A♭ B♭ | A♭ major | 4, 7, 3, 6, 2 |
| C Locrian | C D♭ E♭ F G♭ A♭ B♭ | D♭ major | 4, 7, 3, 6, 2, 5 |

Read in this order, the parent keys step down the circle of fifths, from one sharp to five flats. Wikipedia's "Mode (music)" describes the same sequence: "each mode has one more lowered interval relative to the tonic than the mode preceding it".

**On the guitar.** In open position, with standard tuning, the notes of C major lie on frets 0 to 3. D Dorian starts on the open D string and climbs to D on the second string, fret 3: D E F G A B C D. G Mixolydian starts on the sixth string, fret 3, and climbs to the open G string: G A B C D E F G. Both come from the same open-position shape of C major, on frets 0 to 3: they are relative modes, the same set read from two tonics. What makes them sound different is the note you start and end on, and the chords you play under it.

### Practice Exercise

Which major scale holds the notes of E Phrygian, and which holds the notes of C Phrygian?

> *Solution:* E Phrygian is C major read from E, its third degree. C Phrygian starts on C with the same pattern, 1 2 2 2 1 2 2: C D♭ E♭ F G A♭ B♭, the notes of A♭ major, whose third degree is C.

---

## 3. How Many Modes?

A scale of n notes has n rotations, but two rotations can give the same pattern. Wikipedia: "The number of possible modes for any intervallic set is dictated by the pattern of intervals in the scale." The diminished scale "has only two distinct modes", and the article goes on: "The chromatic and whole-tone scales, each containing only steps of uniform size, have only a single mode each, as any rotation of the sequence results in the same sequence."

The whole-tone and diminished scales are two of Messiaen's **modes of limited transposition**: scales that "may be transposed to all twelve notes of the chromatic scale, but at least two of these transpositions must result in the same pitch classes" (Wikipedia, "Modes of limited transposition"). The whole-tone scale "has two transpositions and one mode"; the octatonic scale, the diminished scale, "has three transpositions, like the diminished 7th chord, and two modes". The augmented scale of the table below meets the same definition, but Messiaen did not list it: the same article calls it a truncated form of his third mode.

The two counts are tied. A mode on C is a transposition of the scale, chosen to contain C, read from C. A scale with t different transpositions and n notes places n × t notes on the 12 pitch classes, the same number on each, so n × t / 12 of its transpositions contain C:

| Scale | Notes n | Transpositions t | Modes n × t / 12 |
|------|------|------|------|
| Major | 7 | 12 | 7 |
| Harmonic minor | 7 | 12 | 7 |
| Major pentatonic | 5 | 12 | 5 |
| Whole tone | 6 | 2 | 1 |
| Augmented, C E♭ E G G♯ B | 6 | 4 | 2 |
| Octatonic | 8 | 3 | 2 |
| Chromatic | 12 | 1 | 1 |

MUS-006 counts the same rotations, and Learn's music-theory-ga lesson 12 studies these scales in GA.

### Practice Exercise

The augmented scale's pattern is 3 1 3 1 3 1. How many distinct modes does it have, and what are their patterns?

> *Solution:* Two: 3 1 3 1 3 1 and 1 3 1 3 1 3. Every rotation by two steps gives the same pattern back. It has four transpositions, and 6 × 4 / 12 = 2.

---

## 4. Same Vector, Different Family

Rotations keep a scale's set, up to transposition, so the modes of one scale all share its interval-class vector (MUS-010, MUS-020). The converse fails: two scales can share a vector without being modes of each other.

**Mirror images.** C harmonic minor, C D E♭ F G A♭ B, has the pattern 2 1 2 2 1 3 1. C harmonic major, C D E F G A♭ B, has 2 2 1 2 1 3 1. Wikipedia's "Harmonic major scale" describes it as a major scale with a lowered sixth, and adds: "Its upper tetrachord is the same as that of the harmonic minor scale." Both have the vector <3 3 5 4 4 2>. The seven rotations of harmonic minor's pattern are:

2 1 2 2 1 3 1, 1 2 2 1 3 1 2, 2 2 1 3 1 2 1, 2 1 3 1 2 1 2, 1 3 1 2 1 2 2, 3 1 2 1 2 2 1, 1 2 1 2 2 1 3

None of them is 2 2 1 2 1 3 1, so harmonic major is not a mode of harmonic minor. It is its **mirror image**: play harmonic minor's steps downwards from G, 2 1 2 2 1 3 1, and you get G F E D C B A♭, the notes of C harmonic major; G is the starting note that lands on C rather than on a transposition. A mirror image has the same intervals in reverse order, so it has the same vector (MUS-020 calls it an inversion). The major scale, melodic minor, the pentatonic and the whole-tone, augmented, octatonic and chromatic scales of §3 are their own mirror images; harmonic minor, harmonic major and the blues scale are not.

**The Z-relation.** Some sets share a vector without being a transposition or a mirror image of each other. Wikipedia's "Interval vector" gives an example, the smallest there is: "the two sets 4-z15A {0,1,4,6} and 4-z29A {0,1,3,7} have the same interval vector ⟨111111⟩ but one can not transpose and/or invert the one set onto the other." On C, they are C C♯ E F♯ and C C♯ E♭ G.

**Counting a vector's sets.** Take every set that contains C and has a given vector. It holds the modes on C of every scale with that vector:
- the major scale's vector: the seven modes on C of §2, since the major scale is its own mirror image and has no Z-partner;
- harmonic minor's vector: 14 sets, the seven modes on C of harmonic minor and the seven of harmonic major;
- the blues scale's vector: 24 sets, six modes of the blues scale, six of its mirror image, and twelve sets of a class that is Z-related to it.

The count of §3 extends to a whole set class. If a class of n notes has f different sets among its transpositions and their mirror images, n × f / 12 of them contain C. For harmonic minor's class, f = 24 and 7 × 24 / 12 = 14.

### Practice Exercise

Are C harmonic minor and C harmonic major modes of each other?

> *Solution:* No. Harmonic major's pattern, 2 2 1 2 1 3 1, is not among the seven rotations of harmonic minor's pattern. The two scales are mirror images of each other: they share the vector <3 3 5 4 4 2>, but no rotation maps one onto the other.

---

## 5. Where GA Stands

GA is the music-theory library and chatbot of the GuitarAlchemist ecosystem. The facts below are read from its code at commit [`5c3a52a`](https://github.com/GuitarAlchemist/ga/tree/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26). This lesson documents that code and does not change it. It has not run GA or its tests: the counts below come from a Python reimplementation of the methods cited. The files it cites are unchanged on GA's `main` at `0843879`.

Learn's music-theory-ga course compiles an earlier version of GA, `a826864`, and its lessons have already measured GA's modal families. `ModalFamily.cs` is the same file at both commits, and so are the lines of the `PitchClassSet` members used below. The code they call did change in between: caches and lookup tables were added, the twelve-note vector <12 12 12 12 12 6> got a special decoding, and code for parsing, normal forms and keys changed, which building the families does not use. The reimplementation also finds every count Learn measured. So those measurements still describe GA's code. This section summarises them, links to them, and adds a census of every family.

**GA's tonal modes are rotations.** [`MajorScaleMode`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Tonal/Modes/Diatonic/MajorScaleMode.cs#L16) passes `Scale.Major` to its base class, which keeps it as the [`ParentScale`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Tonal/Modes/ScaleMode.cs#L27-L34) and builds each mode's notes by [rotating the parent's notes](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Tonal/Modes/ScaleMode.cs#L127-L135). These are §2's relative modes: a test checks that [the seven modes start on C, D, E, F, G, A and B](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Tests/GA.Domain.Core.Tests/Theory/Tonal/ScaleModeTests.cs#L21-L40). Another test, [`AllModes_ShareParentScaleIntervalClassVector`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Tests/GA.Domain.Core.Tests/Theory/Tonal/ScaleModeTests.cs#L62-L71), says that "every rotation of the diatonic scale has the same interval-class vector", but it reads `mode.ParentScale.IntervalClassVector`, which is the vector of `Scale.Major` for all seven modes, and compares it with the constant `IntervalClassVector.Major`: the same check, seven times. Reading the modes' own notes would not help, since relative modes share one set; the claim about rotations needs the modes moved to C, as in §2's table, and this test does not do that.

**GA's modal families group sets by vector.** A [`ModalFamily`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Atonal/ModalFamily.cs#L9-L13) is a ["Group of pitch class sets representing a scale that share the same interval vector"](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Atonal/ModalFamily.cs#L10). GA [builds the families](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Atonal/ModalFamily.cs#L114-L129) from every set that contains 0, grouped by number of notes and then by vector: §4's count. Its members are therefore parallel modes on C, and the major family is the seven sets of §2's table. GA lists its sets [in id order](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Atonal/PitchClassSetId.cs#L19-L20), a set's id being its 12-bit number (MUS-020), and the [grouping](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Atonal/ModalFamily.cs#L119-L120) keeps that order. So the first member and the [`PrimeMode`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Atonal/ModalFamily.cs#L51) of the major family is C Locrian, id 1387. [`ModeIndex`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Atonal/PitchClassSet.cs#L106-L117) is a set's place in that list, and `FamilySize` the list's length; `ModeIndex` is 5 for C Ionian and 6 for C Lydian, not a degree. Learn's lesson 13 shows that it is −1 for a set without C ([lesson 13](https://github.com/spareilleux/learn/blob/9e03205191de8602d1833e171aecff832ea9cb14/src/content/docs/music-theory-ga/13-extended-and-altered-chords.mdx#L355)).

**What Learn has measured.** Compiled at `a826864`:
- GA's harmonic minor family has 14 members and its blues family 24 ([lesson 2](https://github.com/spareilleux/learn/blob/9e03205191de8602d1833e171aecff832ea9cb14/src/content/docs/music-theory-ga/02-scales-and-modes.mdx#L236-L256)), §4's counts;
- the major triad's family has 6, the dominant seventh's 8 and the all-interval tetrachord's 16 ([lesson 4](https://github.com/spareilleux/learn/blob/9e03205191de8602d1833e171aecff832ea9cb14/src/content/docs/music-theory-ga/04-set-classes.mdx#L184-L196));
- `UnifiedModeService.RankByBrightness` ranks 14 scales for the family of harmonic minor ([lesson 11](https://github.com/spareilleux/learn/blob/9e03205191de8602d1833e171aecff832ea9cb14/src/content/docs/music-theory-ga/11-modes-in-depth.mdx#L211-L229));
- `IsMonomodal`, whose doc comment gives "Whole Tone, Diminished" as examples, is false for the octatonic scale, the diminished scale, since its family has two members, and true for the diminished seventh chord ([lesson 12](https://github.com/spareilleux/learn/blob/9e03205191de8602d1833e171aecff832ea9cb14/src/content/docs/music-theory-ga/12-symmetry-and-limited-transposition.mdx#L254)).

GA's catalog generated from these families, `AtonalModalFamilies.yaml`, files the vector <3 3 5 4 4 2> as ["Harmonic Major Family"](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Business.Config/AtonalModalFamilies.yaml#L6446-L6452), with a `DistinctModeCount` of 14, by §4 the modes on C of two scales, and two tonal subfamilies, harmonic major and harmonic minor. Learn's lesson 12 reads the file's `IsSymmetric` field ([lesson 12](https://github.com/spareilleux/learn/blob/9e03205191de8602d1833e171aecff832ea9cb14/src/content/docs/music-theory-ga/12-symmetry-and-limited-transposition.mdx#L260)).

**Every family, by transcription.** Over GA's 200 families, the transcription finds:

| Kind of family | Families | Sets |
|------|------|------|
| Only rotations of the first member | 75 | 398 |
| Also mirror images, no Z-partner | 102 | 1218 |
| A Z-related class | 23 | 432 |

So 125 of the 200 families, holding 1650 of the 2048 sets that contain C, are not families of modes. The doc comment of [`IsMultimodal`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Atonal/PitchClassSet.cs#L181-L184) speaks of "a family with multiple distinct rotations (e.g. Diatonic, Harmonic Minor)", but seven of harmonic minor's fourteen members are not its rotations. [`IsZRelated`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Common/GA.Domain.Core/Theory/Atonal/PitchClassSet.cs#L196-L211) looks for a member that is not among the first member's 24 transpositions and inversions, so it flags the 23 Z families and accepts the 102 mirror families.

**What the tests check.** Compiled tests check that a scale's own set lies in its family ([`ScaleModalMetadataTests`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Tests/Common/GA.Business.Core.Tests/Tonal/ScaleModalMetadataTests.cs#L8-L32)), that `IsZRelated` agrees with the Z marks of Forte's catalog up to six notes ([`CanonicalForteCatalogTests`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Tests/Common/GA.Business.Core.Tests/Atonal/CanonicalForteCatalogTests.cs#L81-L90)), and that the major family has seven members, through `UnifiedModeService.EnumerateRotations` ([`UnifiedModeEdgeCaseTests`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Tests/Common/GA.Business.Core.Tests/Unified/UnifiedModeEdgeCaseTests.cs#L227-L240)). None of them lists the sets a family should hold. The test that did is removed from its project, with two others ([`ModalFamilyScaleModeFactoryTests`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Tests/Common/GA.Business.Core.Tests/GA.Business.Core.Tests.csproj#L50), [`ModalFamilyTests` and `ModalFamilyScaleModeTests`](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Tests/Common/GA.Business.Core.Tests/GA.Business.Core.Tests.csproj#L69-L70)). That test, `ModalFamilyTests`, [expects seven members](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Tests/Common/GA.Business.Core.Tests/Tonal/ModalFamilyTests.cs#L90-L92), then [looks for](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Tests/Common/GA.Business.Core.Tests/Tonal/ModalFamilyTests.cs#L103-L109) the seven relative modes it lists, [C D E F G A B through B C D E F G A](https://github.com/GuitarAlchemist/ga/blob/5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26/Tests/Common/GA.Business.Core.Tests/Tonal/ModalFamilyTests.cs#L59-L69). As sets, these are one set, C major's, so the test never looks for C Dorian or the other members of §2's table.

Fixing any of this is for GA's owners; this lesson only describes it.

### Practice Exercise

GA's `FamilySize` for C harmonic minor is 14. How many of those 14 sets are modes of the harmonic minor scale, and what are the others?

> *Solution:* Seven: the transpositions of harmonic minor that contain C, read from C. The other seven are the modes on C of harmonic major, its mirror image, which shares the vector <3 3 5 4 4 2>.

---

## 6. Proposed Experiment (Not Yet Run)

**Status: not run.** This section proposes an experiment for Learn's music-theory-ga lab, which compiles GA at `a826864`. Its pin need not move: as §5 explains, the code that builds the families is the same at `5c3a52a`, up to caches and one decoding special case. Nothing in this section is a measurement:
- the predictions come from §3 to §5 and are written down before any run;
- the counts and ids, including the counts by number of notes in step 1, come from the Python reimplementation of §5;
- a later version of this lesson will report the results.

Every step calls GA's types in the lab's own process, never a running MCP server or a language model.

1. **The census.** Count `ModalFamily.Items` and their members by number of notes. Prediction: 200 families holding 2048 sets; by number of notes from 1 to 12, 1, 6, 12, 28, 35, 35, 35, 28, 12, 6, 1 and 1 families.
2. **Rotations or not.** For each family, test every member against the twelve transpositions of the first member, then against its mirror images. Prediction: 75 families of rotations only, 102 with mirror images and no Z-partner, 23 with a Z-related class; 1650 of the 2048 sets lie in the 125 mixed families.
3. **`IsZRelated`.** Read it for every set that contains C. Prediction: true for the 432 sets of the 23 Z families, false for the other 1616.
4. **The controls.** Print the major family and the harmonic minor family. Prediction: the major family holds the ids 1387, 1451, 1453, 1709, 1717, 2741 and 2773, with `PrimeMode` 1387, C Locrian; the harmonic minor family holds 14 sets, seven transpositions of C harmonic minor and seven of C harmonic major.

### Practice Exercise

Step 1 predicts 35 families of seven notes and 35 of five. Why are the two counts equal?

> *Solution:* A family of n notes is one vector shared by sets of n notes. Taking complements matches the sets of 7 notes one to one with the sets of 5, and two sets of 7 notes share a vector exactly when their complements do (MUS-020's complement theorem). So the two cardinalities have the same number of vectors, and the same number of families.

---

## 7. Common Pitfalls

- **Mixing relative and parallel modes.** D Dorian has the notes of C major; C Dorian has the notes of B♭ major.
- **Counting modes by notes for a symmetric scale.** The octatonic scale has eight notes and two modes.
- **Taking a shared vector for a shared family.** Harmonic major has harmonic minor's vector and is not one of its modes.
- **Taking a mirror image for a rotation.** A mirror image reverses the pattern; a rotation only moves its start.
- **Reading GA's `ModalFamily` as the modes of one scale.** It holds every set containing C with the vector, mirror images and Z-partners included.
- **Reading GA's `ModeIndex` as a degree.** It is a place in a list sorted by id: C Locrian is 0, C Ionian 5.

---

## Key Terms

| Term | Definition |
|------|-----------|
| **Mode** | A scale's step pattern read from another of its steps: a rotation |
| **Relative modes** | Modes that share the same notes and differ in tonic, such as D Dorian and G Mixolydian |
| **Parallel modes** | Modes that share the same tonic and differ in notes, such as C Dorian and C Mixolydian |
| **Mode of limited transposition** | A scale with fewer than twelve different transpositions, and so fewer modes than notes |
| **Mirror image** | A scale with the same steps in reverse order; it shares the vector, and is a mode only if the scale is its own mirror image |
| **Z-relation** | Two sets with the same vector that are neither transpositions nor mirror images of each other |
| **Modal family** | The modes of one scale: its rotations |
| **GA's `ModalFamily`** | Every set containing C with a given vector: the modes of several scales when mirror images or Z-partners share it |

---

## Self-Check Assessment

**1. Write the step pattern of the Lydian mode and spell F Lydian and C Lydian.**
> 2 2 2 1 2 2 1. F Lydian is F G A B C D E, the notes of C major. C Lydian is C D E F♯ G A B, the notes of G major.

**2. Play D Dorian and G Mixolydian in open position. Why do both fit in the same shape?**
> Both are C major read from another tonic: they are relative modes with the same set. Only the starting note, and the chords under it, change.

**3. How many distinct modes do the whole-tone scale and the octatonic scale have, and why?**
> One and two. The whole-tone pattern is a single repeated step, so every rotation gives it back; the octatonic pattern alternates two steps, so it has two distinct rotations. With n notes and t transpositions, n × t / 12 gives 6 × 2 / 12 = 1 and 8 × 3 / 12 = 2.

**4. In GA at `5c3a52a`, why does the modal family of C harmonic minor have 14 members, and which kind of family of §5 is it?**
> GA groups every set containing C by vector, and harmonic major, the mirror image of harmonic minor, has the same vector. The family holds the seven modes on C of each scale: it is one of the 102 families with mirror images and no Z-partner.

**Pass criteria:** Build and name the modes of a scale from its pattern. Tell relative from parallel modes and play both. Count a scale's modes, symmetric scales included. Explain why a shared vector does not make two scales modes of each other. Say what GA's `ModalFamily` contains, and how it differs from a family of modes.

---

## Research Basis

- Wikipedia, "Mode (music)": the modern diatonic modes, transposition and mode, the sequence along the circle of fifths, the seven modes of other seven-note scales, and the number of distinct modes.
- Wikipedia, "Modes of limited transposition": Messiaen's definition, and the transpositions and modes of the whole-tone and octatonic scales.
- Wikipedia, "Relative key" and "Parallel key": the two relations, for major and minor keys.
- Wikipedia, "Harmonic major scale": the lowered sixth, and the upper tetrachord shared with harmonic minor.
- Wikipedia, "Interval vector": the Z-relation and the sets 4-z15A and 4-z29A.
- GA source at commit `5c3a52ab40d0d433f8f68dbbd0590f70c8d8cf26`: every code fact in §5 links to its line.
- Learn, music-theory-ga lessons 2, 4, 11, 12 and 13 at commit `9e03205191de8602d1833e171aecff832ea9cb14`: their measurements of GA's modal families at `a826864`.
- Experiment: proposed in §6, not run; this lesson contains no measurement of its own.
- Provenance: hand-authored by a Claude Code session (Opus 5.5) from the Streeling curriculum plan, not produced by the Seldon course pipeline; under review.
- Belief state: T(0.85) F(0.02) U(0.10) C(0.03).
