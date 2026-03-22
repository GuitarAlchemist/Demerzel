# Music Theory FAQ — Seed Document

**Source:** Guitar Alchemist Discord bot Q&A (live since 2026-03-23)
**Maintained by:** Seldon Plan harvesting (future Q&A will extend this file)
**Department:** Music, Guitar Studies, Musicology
**Status:** Initial seed — will grow with each Discord Q&A harvest cycle

---

## Chord Analysis

**Q: How do I identify what chord this is from a set of notes?**
A: Stack the notes in thirds (root, third, fifth, seventh, etc.) and check the intervals. A major triad is root + major 3rd + perfect 5th. A minor triad is root + minor 3rd + perfect 5th. If the stack has 4 notes, you likely have a seventh chord — check whether the 7th is major (11 semitones from root) or minor (10 semitones) to distinguish Maj7 from dominant 7.

**Q: What is OPTIC/K and how does it relate to chords?**
A: OPTIC/K stands for Octave, Permutation, Transposition, Inversion, Cardinality (and optionally K for enharmonic equivalence). These are the transformations under which two chord voicings are considered equivalent. Under OPTIC equivalence, C major in root position and C major in first inversion are the same chord type. This framework underlies the Guitar Alchemist fretboard geometry — chords are equivalence classes, not fixed fingerings.

**Q: What is a chord inversion?**
A: An inversion places a chord member other than the root in the bass. First inversion = third in bass; second inversion = fifth in bass; third inversion (seventh chords only) = seventh in bass. Inversions change the voicing's weight and voice-leading options without changing the chord's harmonic identity.

---

## Reharmonization

**Q: How do I reharmonize a melody note?**
A: Any chord that contains the melody note (or treats it as a stable tension) can substitute. Common approaches: (1) diatonic substitution — replace I with iii or vi, which share two common tones; (2) tritone substitution — replace a dominant 7th with the dominant 7th whose root is a tritone away; (3) modal interchange — borrow a chord from the parallel minor/major; (4) secondary dominant — insert V/x before x to create temporary tonicization.

**Q: What is tritone substitution and why does it work?**
A: In a dominant 7th chord (e.g., G7: G–B–D–F), the tritone is between the 3rd (B) and 7th (F). The only other dominant 7th chord sharing this tritone is Db7 (Db–F–Ab–Cb), where B=Cb and F=E#. Because the tritone resolves the same way, Db7 can substitute for G7 resolving to C. The bass moves by semitone rather than a fifth — smoother voice leading.

**Q: What is modal interchange (borrowed chords)?**
A: Modal interchange borrows chords from a parallel mode. In C major, borrowing from C minor gives access to iv (Fm), bVII (Bb), bVI (Ab), and bIII (Eb). These chords add color without leaving the tonic center. The most common borrowed chord is iv — in C major, Fm creates a bittersweet pull before returning to I.

---

## Scales

**Q: What is the difference between a scale and a mode?**
A: A scale is a collection of pitches ordered by step. A mode is a rotation of that scale starting from a different degree. The major scale has 7 modes (Ionian, Dorian, Phrygian, Lydian, Mixolydian, Aeolian, Locrian). Each mode has the same pitch collection as the parent scale but a different tonal center and characteristic interval pattern.

**Q: How do I choose a scale for improvising over a chord?**
A: Match the scale's characteristic tones to the chord's extensions. Over Cmaj7: C Ionian or C Lydian (raised 4th adds sparkle). Over Dm7: D Dorian (raised 6th, characteristic of minor ii). Over G7: G Mixolydian or G altered (b9, #9, b13 for tension). Over Cm7: C Dorian or C Aeolian. The key principle: avoid the scale's avoid notes (half-step above a chord tone on a strong beat).

**Q: What makes the pentatonic scale so universal?**
A: The major pentatonic (1–2–3–5–6) and minor pentatonic (1–b3–4–5–b7) omit the notes most likely to clash (the 4th and 7th in major; the 2nd and b6 in minor). The remaining notes are stable and widely spaced, making it easy to land anywhere in the scale and sound consonant. This is why pentatonics work across blues, rock, country, and many world music traditions.

---

## Fretboard Geometry (CAGED)

**Q: What is the CAGED system?**
A: CAGED names the 5 open chord shapes (C, A, G, E, D) that tile the fretboard through barre transposition. Each shape covers a contiguous region of the neck. Together, the 5 shapes account for the entire fretboard with no gaps. Knowing CAGED means knowing where every chord voicing of a given root lives across all positions.

**Q: How does CAGED relate to scales?**
A: Each CAGED shape has a corresponding pentatonic and diatonic scale pattern that fits inside it. Connecting the scale patterns to the chord shapes shows which scale tones are emphasised in each position and where chord tones land under each finger, enabling melodic phrasing that outlines harmony.

---

## VexTab and Notation

**Q: What is VexTab?**
A: VexTab is a text-based music notation language that renders to standard notation and tablature in the browser via VexFlow. Guitar Alchemist uses VexTab to display chord diagrams, fretboard maps, and scale patterns inline in course content. A VexTab stave is declared with `tabstave`, notes are written as `notes`, and fret positions are given as `N/string` (e.g., `5/4` = 5th fret, 4th string).

**Q: How do I notate a chord voicing in VexTab?**
A: Use parentheses to group simultaneous notes: `(5/4.5/3.5/2.3/1)` renders a chord. Each note is `fret/string`. Strings are numbered 1 (high e) to 6 (low E) in VexTab convention.

---

## Harmony and Voice Leading

**Q: What are the basic rules of voice leading?**
A: (1) Prefer contrary or oblique motion between voices over parallel motion. (2) Avoid parallel fifths and octaves between any two voices — these erase independence. (3) Move each voice by the smallest interval available. (4) Resolve tendency tones: the leading tone resolves up by semitone; the 7th of a chord resolves down by step. (5) Keep the bass and soprano voices from crossing.

**Q: What is a ii–V–I and why is it so common?**
A: The ii–V–I is the strongest harmonic motion in tonal music. ii (supertonic minor 7th) has subdominant function and prepares V. V (dominant 7th) contains the leading tone and tritone — maximum tension seeking resolution. I (tonic) resolves all tensions. In jazz, the ii–V–I is the foundational progression; most jazz standards can be analysed as a series of ii–V–I motions in various keys.

---

## Harvesting Note

This FAQ was seeded on 2026-03-23 from observed Discord question patterns. Future Q&A harvested by the Seldon Plan research cycle will be appended here and promoted to Streeling University course content when a topic cluster reaches sufficient depth.

Topics with growing question volume that may warrant dedicated courses: reharmonization techniques, fretboard geometry beyond CAGED, modal harmony, jazz chord extensions, world music tuning systems.
