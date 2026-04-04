---
module_id: mus-006-the-scale-universe
department: music
course: Foundations of Music Theory
level: intermediate
alchemical_stage: albedo
prerequisites:
  - mus-001-what-is-a-chord
estimated_duration: "45 minutes"
produced_by: music
version: "1.0.0"
---

# The Scale Universe: 4,096 Possibilities From 12 Notes

> **Department of Music** | Stage: Albedo (Intermediate) | Duration: 45 minutes

## Learning Objectives

After completing this course, you will be able to:

- Represent any scale as a 12-bit binary number and convert it to a decimal integer
- Explain why there are exactly 4,096 mathematically possible scales in 12-tone equal temperament
- Compute the modes of any scale using circular left shifts (bit rotations)
- Distinguish between the total count (4,096) and the count under various equivalences (prime forms, Forte classes)
- Apply Zeitler's criteria to filter the universe down to "musically real" scales
- Compute interval vectors, brightness, and symmetry properties from a scale's integer
- Map any scale integer to fretboard positions on guitar
- Relate scale-space to the OPTIC-K equivalence relations used in music set theory

---

## 1. The Chromatic Alphabet

Western music uses twelve pitch classes per octave. A **pitch class** is a note regardless of which octave it appears in — all the C's on a piano belong to the same pitch class.

The twelve pitch classes, numbered 0 through 11:

| Pitch Class | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 |
|-------------|---|---|---|---|---|---|---|---|---|---|----|----|
| Note Name | C | C#/Db | D | D#/Eb | E | F | F#/Gb | G | G#/Ab | A | A#/Bb | B |

Now think of a scale as a **choice**: for each of the twelve pitch classes, either it is **in** the scale (1) or **out** (0). That gives us a 12-bit binary number — twelve independent yes/no decisions.

**How many possible choices?** Two options for each of twelve positions:

$$ 2^{12} = 4096 $$

Exactly 4,096 mathematically possible scales exist in 12-tone equal temperament. This includes the empty scale (all zeros), the chromatic scale (all ones), all single-note "scales," all traditional scales, and every weird collection in between.

This is the **scale universe**. Its size is finite, knowable, and surprisingly small — a number a computer can enumerate in microseconds.

---

## 2. A Scale IS a Number

Here is the key reframing: **every scale is an integer between 0 and 4095**.

### The Bit Mapping

Assign each pitch class a bit position:

| Bit | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 |
|-----|---|---|---|---|---|---|---|---|---|---|----|----|
| Pitch Class | C | C# | D | D# | E | F | F# | G | G# | A | A# | B |
| Place Value | 1 | 2 | 4 | 8 | 16 | 32 | 64 | 128 | 256 | 512 | 1024 | 2048 |

To convert a scale to an integer, mark each note as 1 and sum the place values.

### Example: The Major Scale

The **C major scale** contains the notes C, D, E, F, G, A, B — pitch classes 0, 2, 4, 5, 7, 9, 11.

Binary (reading from bit 11 down to bit 0):

```
Bit:     11 10  9  8  7  6  5  4  3  2  1  0
Note:     B  Bb  A  Ab G  Gb F  E  Eb D  Db C
In scale:  1  0  1  0  1  0  1  1  0  1  0  1
```

As decimal:

$$ 1 + 4 + 16 + 32 + 128 + 512 + 2048 = 2741 $$

**C major = 2741.**

Every major scale has the same **intervallic structure**, so regardless of root, the pattern (2-2-1-2-2-2-1 semitone steps) defines major. The integer 2741 is the C-rooted representation. Rooted on other notes, the pattern rotates.

### Example: The Minor Pentatonic Scale

The **C minor pentatonic** scale contains C, Eb, F, G, Bb — pitch classes 0, 3, 5, 7, 10.

Binary:

```
Bit:     11 10  9  8  7  6  5  4  3  2  1  0
In scale:  0  1  0  0  1  0  1  0  1  0  0  1
```

As decimal:

$$ 1 + 8 + 32 + 128 + 1024 = 1193 $$

**C minor pentatonic = 1193.**

### Why This Matters

Once you accept that a scale is a number, everything follows:
- You can **enumerate** all scales (count from 0 to 4095)
- You can **compare** scales (integer comparison)
- You can **transform** scales (bit operations: shift, AND, OR, XOR, POPCOUNT)
- You can **search** scales (for specific interval vectors, cardinalities, symmetries)
- You can **store** scales (12 bits instead of a list of notes)

A scale is not a mystical thing. It is a number.

### Practice Exercise

Convert the following three scales to integers using the bit mapping:

1. **C natural minor** (C, D, Eb, F, G, Ab, Bb) — pitch classes 0, 2, 3, 5, 7, 8, 10
2. **C major pentatonic** (C, D, E, G, A) — pitch classes 0, 2, 4, 7, 9
3. **C whole-tone** (C, D, E, F#, G#, A#) — pitch classes 0, 2, 4, 6, 8, 10

Compute each by summing the place values (powers of 2). Check your answers below.

Answers:
1. C natural minor = 1 + 4 + 8 + 32 + 128 + 256 + 1024 = **1453**
2. C major pentatonic = 1 + 4 + 16 + 128 + 512 = **661**
3. C whole-tone = 1 + 4 + 16 + 64 + 256 + 1024 = **1365**

---

## 3. Modes as Rotations

A **mode** is a scale started from a different degree. C Dorian contains the same notes as Bb major, but begins on C. In the integer representation, this is not addition or multiplication — it is a **rotation**.

### The Circular Shift Operation

To find the next mode of a scale:
1. Find the lowest set bit (the root)
2. Remove it, shift the remaining pattern down
3. Wrap the old root around to the top

More precisely, the modal rotation is a **circular left shift** by the distance to the next scale tone. In a 12-bit system, "wrapping around" means bits that shift off the left edge reappear on the right.

### Example: The Modes of Major

The major scale pattern has intervals 2-2-1-2-2-2-1 (seven notes). Its seven modes are generated by rotating to each of the seven scale degrees:

| Mode Name | Starting Degree | Interval Pattern |
|-----------|----------------|------------------|
| Ionian (Major) | 1 | 2-2-1-2-2-2-1 |
| Dorian | 2 | 2-1-2-2-2-1-2 |
| Phrygian | 3 | 1-2-2-2-1-2-2 |
| Lydian | 4 | 2-2-2-1-2-2-1 |
| Mixolydian | 5 | 2-2-1-2-2-1-2 |
| Aeolian (Natural Minor) | 6 | 2-1-2-2-1-2-2 |
| Locrian | 7 | 1-2-2-1-2-2-2 |

These are **not seven different scales.** They are seven rotations of the same underlying pattern. When you play C Dorian on a piano, you are playing the white keys starting from D.

### Computing Rotations as Bit Operations

In pseudocode, to rotate a 12-bit scale integer left by `n` positions:

```
rotate_left(scale, n):
    shifted = (scale << n) & 0xFFF        # shift left, mask to 12 bits
    wrapped = scale >> (12 - n)           # bits that fell off
    return shifted | wrapped               # combine
```

Applied to the major scale (2741), rotating by the correct number of positions produces each mode's integer representation.

### Practice Exercise

Compute the first three modes of the **harmonic minor scale** (C D Eb F G Ab B — intervals 2-1-2-2-1-3-1).

1. Write out the 12-bit binary representation of C harmonic minor
2. Determine how many bits to rotate to get the 2nd mode (Locrian natural 6)
3. Determine how many bits to rotate to get the 3rd mode (Ionian #5)

Hint: the rotation amount equals the number of semitones between the old root and the new root.

Answer sketch:
- C harmonic minor = 2477 (binary: 100110101101)
- Rotate left by 2 semitones (D is 2 semitones above C) → 2nd mode
- Rotate left by 3 semitones (Eb is 3 semitones above C) → 3rd mode

The seven modes of harmonic minor are all rotations of the integer 2477.

---

## 4. How Many Are Really Unique?

We started with **4,096** scales. But many of these are "the same" under different equivalences. How many are truly distinct structures?

### Prime Forms — Ignoring Rotation

Two scales are **modally equivalent** if one is a rotation of the other. A scale's **prime form** is its canonical representative — conventionally, the rotation with the smallest integer value (or the rotation that packs notes toward the beginning).

Under modal equivalence:
- The 7-note major scale family has 7 rotations (7 modes) → 1 prime form
- The 6-note whole-tone scale has only 1 unique rotation (it maps to itself) → 1 prime form
- The 12-note chromatic scale is its own prime form

**Counting prime forms:** Of the 4,096 scales, approximately **352** are structurally unique under rotation. The exact count depends on conventions (whether to include the empty scale, single-note scales, etc.).

### Forte Classes — Ignoring Rotation AND Inversion

In the 1970s, Allen Forte formalized a further equivalence: treating a scale and its **inversion** (mirror image) as the same structure. A scale's inversion reverses its interval pattern.

- **Major scale** (2-2-1-2-2-2-1) inverts to **Phrygian** (1-2-2-2-1-2-2) — wait, that IS a mode of major.
- But most scales have inversions that are NOT in the same modal family.

Under **T/I equivalence** (Transposition + Inversion), Forte identified **224 distinct set classes** for cardinalities 3 through 9. Including all cardinalities from 0 to 12, the total count is slightly higher.

The **Forte number** (e.g., "7-35" for the diatonic/major scale) is a standardized naming system where:
- First number = cardinality (number of notes)
- Second number = ordinal position within that cardinality (sorted by a canonical ordering)

### The Whole-Tone Special Case

The whole-tone scale (C D E F# G# A#) has an interval pattern of 2-2-2-2-2-2. Every rotation produces the identical scale — it has **only one mode**.

Its integer: 1365 (binary 010101010101).

Rotate by any even number of positions: you get back 1365. Rotate by any odd number: you get the other whole-tone scale (2730, binary 101010101010).

Thus there are only **two whole-tone scales** in the entire universe, and they are each other's transposition by a semitone. Under Forte equivalence, both are in the same set class.

### The Counting Hierarchy

| Equivalence | Count | What Is Equated |
|-------------|-------|-----------------|
| None (raw) | 4,096 | All subsets of 12 pitch classes |
| Transposition (T) | ~352 prime forms | Rotations of same pattern |
| Transposition + Inversion (T/I) | 224 Forte classes | Above, plus mirror images |
| T/I + Complementation | ~158 | Above, plus scale+complement pairs |

### Practice Exercise

Convince yourself that the whole-tone scale is "modally invariant":

1. Write C whole-tone in 12-bit binary: 010101010101
2. Rotate left by 2 bits: what do you get?
3. Rotate left by 1 bit: what do you get?
4. Explain why a scale with uniform interval structure (all same step size) has fewer unique modes

Answers:
1. 010101010101 = 1365
2. Rotate left 2: still 010101010101 = 1365 (same scale)
3. Rotate left 1: 101010101010 = 2730 (the other whole-tone scale)
4. A scale with N notes has at most N modes, but if the scale has rotational symmetry (maps to itself under rotation by k semitones where k < 12), it has fewer unique modes. The whole-tone scale has 12/6 = 2 rotational symmetry period, so all rotations produce one of two states.

---

## 5. What Makes a "Real Scale"?

Of the 4,096 mathematical possibilities, most are not useful for music. A scale like `101100000001` (C, Db, Eb, B) is a collection of notes, but no one would call it a scale in the practical sense. How do we filter the universe down to legitimate scales?

### The Zeitler Criteria

William Zeitler, in his exhaustive cataloging work, proposed four criteria for a scale to be "real":

1. **The root is present** — bit 0 must be set. A scale must contain its own tonic. This eliminates 2,048 scales (half the universe).

2. **No gap larger than 4 semitones** — consecutive scale tones cannot be more than a major 3rd apart. A gap of 5+ semitones creates an audible hole that breaks scalar continuity.

3. **Between 5 and 8 notes** — scales outside this range either sound too sparse (to be heard as scalar) or too dense (to be heard as distinct from chromaticism). This is a pragmatic constraint, not a mathematical one.

4. **No cluster longer than 3 consecutive semitones** — four or more chromatic notes in a row create a chromatic cluster that loses scalar character.

Applying all four criteria reduces the 4,096 scales to approximately **1,490 "legitimate" scales**. This is still vastly more than the familiar repertoire of named scales.

### Why These Criteria Are Guidelines, Not Laws

The Zeitler criteria are **heuristics**, not definitions. Counterexamples abound:

- The **chromatic scale** has 12 consecutive semitones (violates criterion 4) — clearly a real scale
- **Single-note "drones"** violate the 5-note minimum — clearly a real musical structure
- **Blues scales** sometimes use gaps of 3 semitones cleverly (minor pentatonic has a gap from Bb to C)
- **Gagaku scales**, microtonal scales, and other non-Western systems do not fit 12-TET at all

The criteria are **culture-specific** — they describe scales that fit European tonal and modal practice. They are a useful filter, not a universal truth.

### Practice Exercise

For each of the following scales, determine which Zeitler criteria (if any) it violates:

1. **C major** (0, 2, 4, 5, 7, 9, 11)
2. **C chromatic** (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11)
3. **A gap scale** (0, 5, 11) — C, F, B
4. **A cluster scale** (0, 1, 2, 3, 4) — C, C#, D, D#, E

Answers:
1. C major: violates none — passes all criteria
2. C chromatic: violates criterion 3 (12 notes, exceeds max of 8) and criterion 4 (12 consecutive semitones)
3. Gap scale: violates criterion 2 (gap from F to B is 6 semitones) and criterion 3 (only 3 notes)
4. Cluster scale: violates criterion 4 (5 consecutive semitones) and criterion 3 (only 5 notes, at the edge)

---

## 6. Scale Properties You Can Compute

Once a scale is an integer, all its musical properties become computable. You do not need to listen — you can analyze the number.

### Interval Vector

An **interval vector** counts how many times each interval class appears in the scale. There are six interval classes (1 through 6 semitones; the tritone is its own inverse, and intervals 7-11 are complements of 1-5).

For the **C major scale** (C D E F G A B):

```
Interval class: 1   2   3   4   5   6
Count:          2   5   4   3   6   1
```

Interval vector: `[2, 5, 4, 3, 6, 1]`

The vector is computed by examining all pairs of scale tones and counting the distance between them (reducing to the range 1-6).

**Why it matters:** The interval vector encodes harmonic potential. Scales with many 3rds and 5ths (interval classes 3, 4, 5) sound consonant and tonal. Scales heavy in interval classes 1 and 6 sound dissonant and unstable.

### Brightness

**Brightness** is the sum of the pitch classes (bit positions set). Higher sums mean the scale's notes are higher in the chromatic circle (more sharps), lower sums mean more flats.

- C major (0, 2, 4, 5, 7, 9, 11): sum = 38
- C Lydian (0, 2, 4, 6, 7, 9, 11): sum = 39 — brighter by one
- C Phrygian (0, 1, 3, 5, 7, 8, 10): sum = 34 — darker

The **Locrian-to-Lydian spectrum** (darkest to brightest modes of major) corresponds to monotonically increasing brightness values. This is a computed property — no ear required.

### Symmetry

A scale has **rotational symmetry** if rotating it by some k semitones produces the same scale. The scale's symmetry order tells you how many distinct transpositions it has.

- **Whole-tone scale:** symmetry at every 2 semitones → only 2 distinct transpositions
- **Diminished (octatonic) scale:** symmetry at every 3 semitones → only 3 distinct transpositions
- **Augmented scale:** symmetry at every 4 semitones → only 4 distinct transpositions
- **Major scale:** no rotational symmetry → all 12 transpositions are distinct

### Chirality

A scale is **chiral** if its inversion (mirror image around pitch class 0) is NOT the same as any rotation of itself. Most scales are chiral. Exceptions include the major scale (whose inversion is the Phrygian mode, which IS a rotation) and symmetric scales.

### Z-Relation

Two scales are **Z-related** if they have the same interval vector but are NOT related by transposition or inversion. They sound similar harmonically but are structurally distinct. Z-related pairs are rare and musically fascinating.

The most famous Z-pair: the **all-interval tetrachord** Z-relation `{0,1,4,6}` and `{0,1,3,7}`, both with interval vector `[1,1,1,1,1,1]`.

### Practice Exercise

Compute the interval vector for the **C minor pentatonic scale** (C Eb F G Bb = pitch classes 0, 3, 5, 7, 10).

Step 1: List all pairs and their distances.
Step 2: Reduce distances to interval classes (distances 7-11 become 12-distance: e.g., 8 semitones → class 4).
Step 3: Count occurrences of each class.

Answer:
Pairs and distances:
- 0-3: 3
- 0-5: 5
- 0-7: 5 (7 reduces to 5)
- 0-10: 2 (10 reduces to 2)
- 3-5: 2
- 3-7: 4
- 3-10: 5 (7 reduces to 5)
- 5-7: 2
- 5-10: 5
- 7-10: 3

Interval class counts:
- Class 1: 0
- Class 2: 3
- Class 3: 2
- Class 4: 1
- Class 5: 4
- Class 6: 0

Interval vector: **[0, 3, 2, 1, 4, 0]**

Note: heavy on class 5 (perfect 4ths/5ths) and absent class 6 (tritone) and class 1 (semitone) — this is why pentatonic scales sound stable and "never wrong."

---

## 7. Exploring Unnamed Scales on Guitar

Music theory textbooks cover perhaps **200 named scales**: major, minor, modes, pentatonics, harmonic and melodic minor and their modes, diminished, whole-tone, blues, bebop scales, a handful of "exotic" (Hungarian, Byzantine, etc.), and the Messiaen modes.

That leaves **approximately 3,800 unnamed scales** that satisfy basic Zeitler criteria. The vast majority of the scale universe is unexplored territory.

### How to Explore

1. **Pick a number** between 1 and 4095 (or use a random generator)
2. **Decode the bits** to find which pitch classes are in the scale
3. **Check Zeitler criteria** — is this scale "reasonable"?
4. **Play it** on your instrument and listen
5. **Note the interval vector** and compare to scales you know

### Fretboard Mapping Formula

To play a scale integer on guitar, you need to map pitch classes to fret positions on each string.

Given:
- Scale integer S
- Open-string pitch classes for standard tuning: E(4), A(9), D(2), G(7), B(11), E(4)
- For each string, compute which frets (0-12) contain a scale note

**Formula:** For each fret f (0 to 12) on a string whose open pitch class is p:

```
pitch_class_at_fret = (p + f) mod 12
is_in_scale = (S >> pitch_class_at_fret) & 1
```

If the result is 1, mark that fret. Repeat for all six strings.

### Example: A Random Scale

Pick scale integer **1749**. Decode:

```
1749 in binary: 011011010101
Pitch classes (reading bits 0-11): 0, 2, 4, 6, 7, 9, 10
Notes from C:                     C, D, E, F#, G, A, Bb
```

This scale has 7 notes, contains C (root is present), maximum gap is 2 semitones, no long clusters — it passes Zeitler criteria.

Interval pattern: 2-2-2-1-2-1-2 (summing to 12).

**This is Mixolydian #11** (or Lydian Dominant, the 4th mode of melodic minor) — a named scale! You just rediscovered it by picking a number.

Try a less-charted number: **2391**. Decode:

```
2391 in binary: 100101010111
Pitch classes: 0, 1, 2, 4, 6, 8, 11
Notes from C: C, C#, D, E, F#, G#, B
```

This satisfies Zeitler (root present, gaps small, 7 notes, short clusters) but is not a commonly named scale. Play it on guitar. Listen. Give it a name.

### The Exploration Protocol

1. Generate 5-10 random scale numbers that pass Zeitler criteria
2. Play each for 30 seconds, listening for emotional character
3. Record your favorites
4. Build simple melodies using each scale's unique intervallic flavor
5. Compare to named scales with similar interval vectors

This is how new music gets discovered. The universe is there; the mapping is mechanical; the musical judgment is yours.

### Practice Exercise

Take the scale integer **1709** (Hungarian-sounding).

1. Convert it to binary and identify the pitch classes
2. Write out the scale starting on C
3. Compute the interval pattern (steps between consecutive notes)
4. Map the scale onto the top two strings of a guitar in standard tuning (1st string = E, 2nd string = B) for frets 0-12

Hint: 1709 = 1024 + 512 + 128 + 32 + 8 + 4 + 1 → bits 0, 2, 3, 5, 7, 9, 10.

---

## 8. Connection to OPTIC-K

Music set theory uses a taxonomy of **equivalence relations** to describe how two note collections might be considered "the same." The mnemonic OPTIC-K captures them all. The scale-integer framework makes these equivalences computable.

### The Six Equivalences

| Letter | Name | Meaning | Operation |
|--------|------|---------|-----------|
| **O** | Octave | Notes in different octaves are equivalent | Reduce to pitch class (mod 12) |
| **P** | Permutation | Order of notes does not matter | Treat as a set |
| **T** | Transposition | Same pattern starting on different root | Modular rotation |
| **I** | Inversion | Mirror image around a pivot | Reverse interval order |
| **C** | Cardinality | Number of distinct pitch classes | POPCOUNT of integer |
| **K** | (Alternate form) | — | Computed from K-net or similar |

(The "K" in OPTIC-K sometimes refers to cardinality equivalence or to a specific Kuusisto/Lewin structure, depending on source.)

### Where Each Equivalence Lives in the Framework

- **O-equivalence:** Built into the model. By reducing notes to pitch classes 0-11, octave information is discarded.
- **P-equivalence:** Built into the model. A 12-bit integer is a set (order-independent) by construction.
- **T-equivalence:** Computed as rotation (circular shift) of the integer.
- **I-equivalence:** Computed as **bit reversal** of the 12-bit integer. Reversing the bits of scale S gives its inverted scale (then rotate to put the root back at bit 0).
- **C-equivalence:** Computed as POPCOUNT — the number of 1 bits.

### The 224 Forte Classes

Under combined T and I equivalence (the standard Forte taxonomy), the 4,096 scales collapse to **224 distinct classes**. These classes form the foundation of 20th-century music set theory.

Each Forte class has a canonical prime form (the lexicographically smallest representative after normalization). Forte's 1973 book **"The Structure of Atonal Music"** tabulates all 224 classes with their interval vectors, symmetries, and Z-relations.

### GA's 216-Dimensional Vector Space

Guitar Alchemist represents scales as feature vectors in a 216-dimensional space. The dimensions encode:

- Cardinality (1 dimension)
- Interval vector (6 dimensions)
- Brightness (1 dimension)
- Modal positions (varies)
- Chord content (varies)
- Guitar-specific playability metrics (varies)
- OPTIC-K equivalence class memberships (varies)

Two scales close in this 216-D space share musical character. The space is navigable: you can move from major toward Lydian by walking in a specific direction; you can find the nearest "unnamed" scale to a named one; you can compute harmonic distances between arbitrary scales.

The scale integer is the **index** into this vector space. Given integer S, GA computes the full 216-dimensional feature vector deterministically.

### The Payoff

The scale universe is:
- **Finite** (4,096 scales)
- **Enumerable** (integers 0 to 4095)
- **Transformable** (bit operations for modes, inversions, complements)
- **Computable** (every property derivable from the integer)
- **Navigable** (distances and neighborhoods in feature space)
- **Mostly unexplored** (only ~200 of ~1,500 legitimate scales are named)

Music theory did not need to be fuzzy. Pitch-class set theory, combined with modern computation, turns scales from folklore into data.

---

## Key Terms

| Term | Definition |
|------|-----------|
| **Pitch class** | A note identity independent of octave (C, C#, D, ... B) |
| **12-TET** | Twelve-tone equal temperament — the standard Western tuning system |
| **Scale integer** | A 12-bit number where each bit indicates presence/absence of a pitch class |
| **Mode** | A rotation of a scale, treating a non-root degree as the new root |
| **Prime form** | The canonical representative of a scale family under equivalence |
| **Forte number** | A standardized label (e.g., 7-35) for a pitch-class set class |
| **Interval vector** | A 6-tuple counting occurrences of each interval class in a scale |
| **Interval class** | An interval reduced modulo octave AND inversion (so 1 and 11 are both class 1, etc. — actually wait, intervals 1-6 and their complements 11-6 collapse to classes 1-6) |
| **Brightness** | The sum of pitch classes in a scale (proxy for sharpness/flatness) |
| **Symmetry (rotational)** | A scale's property of mapping to itself under rotation |
| **Chirality** | A scale's asymmetry under inversion |
| **Z-relation** | Two scales with the same interval vector but unrelated by T or I |
| **Zeitler criteria** | Heuristics for filtering mathematical scales to "musically real" ones |
| **POPCOUNT** | The count of set bits in a binary number (= scale cardinality) |
| **OPTIC-K** | Mnemonic for equivalence relations in music set theory |

---

## Self-Check Assessment

**1. Convert the C Dorian scale (C D Eb F G A Bb) to its pitch-class integer using the bit-mapping convention.**
> Pitch classes: 0, 2, 3, 5, 7, 9, 10. Integer = 1 + 4 + 8 + 32 + 128 + 512 + 1024 = **1709**.

**2. Compute the interval vector for the C whole-tone scale (C D E F# G# A#).**
> Pairs yield only intervals of 2, 4, 6 semitones. Counts: class 1 = 0, class 2 = 6, class 3 = 0, class 4 = 6, class 5 = 0, class 6 = 3. Interval vector: **[0, 6, 0, 6, 0, 3]**.

**3. What is the Forte number for the major scale (diatonic collection), and how many notes does it have?**
> Forte number **7-35**. The first digit (7) indicates cardinality = 7 notes.

**4. Explain why the seven modes of the major scale are NOT seven different scales under transpositional equivalence.**
> All seven modes contain the same seven pitch classes arranged in the same cyclic interval pattern (2-2-1-2-2-2-1). Each mode is a rotation of the others — they share one prime form. Starting the pattern from a different degree does not change the underlying scale structure, only the choice of tonic.

**5. Apply Zeitler filtering to the scale with pitch classes {0, 1, 7}. Which criteria does it pass or fail?**
> Root present (bit 0 set): PASS. Max gap from 1 to 7 is 6 semitones: FAIL (exceeds 4). Cardinality = 3 notes: FAIL (below minimum of 5). No cluster of 4+ semitones: PASS. Net: fails Zeitler as a "legitimate" scale (it is a trichord, not a scale).

**Pass criteria:** Convert any scale (given as pitch classes or note names) to and from its integer representation, compute its interval vector by hand, identify its Forte cardinality, and explain which OPTIC-K equivalences are built into the integer model versus which require additional computation.

---

## Research Basis

- 12-tone equal temperament as the Western tuning standard is empirically documented in piano tuning and orchestral practice since the 19th century
- Pitch-class set theory and the 4,096 scale enumeration originate in Milton Babbitt's combinatorial work (1950s) and were formalized by Allen Forte in *The Structure of Atonal Music* (1973)
- The 224 set classes under T/I equivalence are enumerated and tabulated in Forte (1973) and remain the standard taxonomy
- Zeitler's scale criteria come from William Zeitler's exhaustive cataloging project (*All The Scales*, 2011 and companion website), representing a practical filter on the universe
- Scale geometry and neighborhood relationships are explored in Dmitri Tymoczko's *A Geometry of Music* (2011), which formalizes voice-leading distances between chords and scales
- The 216-dimensional GA feature-space representation is an implementation choice of Guitar Alchemist, extending classical pitch-class set theory with performance and harmonic-function metadata
- OPTIC-K equivalence relations trace to David Lewin's *Generalized Musical Intervals and Transformations* (1987) and subsequent systematization in music theory pedagogy
- Sources: Forte (1973); Tymoczko (2011); Lewin (1987); Rahn, *Basic Atonal Theory* (1980); Zeitler scale catalog (2011)
- Belief state: T(0.85) F(0.03) U(0.08) C(0.04)
