---
module_id: gtr-002-caged-geometry
department: guitar-studies
course: "Fretboard layout and CAGED system"
level: intermediate
prerequisites: [gtr-001-the-fretboard-map]
estimated_duration: "45 minutes"
produced_by: seldon-research-cycle
research_cycle: guitar-studies-2026-03-23-001
version: "1.0.0"
---

# CAGED Geometry: Why Five Shapes Rule the Fretboard

> **Department of Guitar Studies** | Level: Intermediate | Duration: 45 minutes

## Objectives
- Understand why exactly 5 open chord shapes tile the entire fretboard
- Derive the CAGED system from observation of open chord intervallic structure
- Demonstrate that CAGED is a mathematical consequence of standard tuning, not an arbitrary system
- Apply moveable barre chord forms to navigate any major chord across the neck

---

## 1. The Five Open Shapes

Every guitarist learns these five open major chords early on. Each has a distinct geometric fingerprint:

### C Shape
```
x 3 2 0 1 0    Strings: 5-4-3-2-1
  R 3 5 R 3    Intervals: Root-M3-P5-Root-M3
```

### A Shape
```
x 0 2 2 2 0    Strings: 5-4-3-2-1
  R 5 R 3 5    Intervals: Root-P5-Root-M3-P5
```

### G Shape
```
3 2 0 0 0 3    Strings: 6-5-4-3-2-1
R 3 5 R 3 R    Intervals: Root-M3-P5-Root-M3-Root
```

### E Shape
```
0 2 2 1 0 0    Strings: 6-5-4-3-2-1
R 5 R 3 5 R    Intervals: Root-P5-Root-M3-P5-Root
```

### D Shape
```
x x 0 2 3 2    Strings: 4-3-2-1
  R 5 R 3      Intervals: Root-P5-Root-M3
```

**Key observation:** Every shape contains only three pitch classes: Root, Major 3rd, and Perfect 5th. The differences are in *voicing* -- which octave each note appears in and which strings carry them.

---

## 2. The Slide Test

Here is the central insight: if you maintain the *finger geometry* of any open chord but slide it up the neck, the intervallic relationships are preserved. The barre finger replaces the nut.

**E shape at fret 0:** E major (open)
**E shape at fret 1:** F major (F barre chord)
**E shape at fret 3:** G major
**E shape at fret 5:** A major

This works because the interval between each pair of adjacent strings is fixed by the tuning. Moving all fingers by the same number of frets transposes every note by the same interval.

This is not a pedagogical trick -- it is a *geometric theorem* about the fretboard.

---

## 3. Why Exactly Five Shapes?

Standard tuning (E-A-D-G-B-E) creates a specific interval pattern between strings:

```
String:    6    5    4    3    2    1
Note:      E    A    D    G    B    E
Interval:    P4   P4   P4   M3   P4
```

The 4th-4th-4th-3rd-4th pattern creates exactly **five distinct regions** where open chord shapes can be formed. Each shape occupies a different span of frets and strings.

The five shapes interlock like puzzle pieces:

```
Fret:  0    3    5    7    8    10   12
       |--E--|--D--|--C--|--A--|--G--|--E--|
       (shapes shown for key of E major)
```

Moving through C-A-G-E-D order walks you up the neck, with each shape's root connecting to the next shape's highest note. This is the **CAGED sequence** -- a cyclic path through all five voicing regions.

---

## 4. Is CAGED the Only Ordering?

The five shapes form a **cycle**, so any starting point gives a valid sequence:

- **CAGED** (most common)
- **AGEDC** (starting from A)
- **GEDCA** (starting from G)
- **EDCAG** (starting from E)
- **DCAGE** (starting from D)

The name "CAGED" is mnemonic convenience. The underlying 5-shape cycle is structurally determined. All orderings describe the same fretboard tiling.

---

## 5. Tuning Dependence

CAGED is specific to standard tuning. Change the tuning, and the shapes change:

- **All-fourths tuning** (E-A-D-G-C-F): The M3 irregularity between strings 3-2 disappears. Chord shapes become more uniform but different from CAGED.
- **Open G tuning** (D-G-D-G-B-D): Open strings already form a chord, creating a completely different shape system.
- **Drop D** (D-A-D-G-B-E): Only the lowest string changes, preserving most CAGED shapes but altering the E and G shapes on the bass strings.

This proves CAGED is *derived from* standard tuning's geometry, not imposed on it.

---

## Practice Exercise

### Exercise 1: Shape Identification
Play a C major chord using all five CAGED shapes. Start with the open C shape, then find the A shape (fret 3), G shape (fret 5), E shape (fret 8), and D shape (fret 10).

### Exercise 2: Shape Connection
Pick any two adjacent CAGED shapes. Find the notes they share on the same strings. These shared notes are your "pivot points" for moving between shapes.

### Exercise 3: One String, Five Shapes
On string 2 alone, play the note C in each of the five CAGED positions. Notice how each shape places C on a different fret of that string.

---

## Key Takeaways
- The CAGED system is **discovered, not invented** -- it's a structural consequence of standard tuning geometry
- Exactly **5 shapes** tile the fretboard because of the 4th-4th-4th-3rd-4th tuning pattern
- Each shape preserves its intervallic structure when barred and moved -- this is a geometric theorem, not a pedagogical shortcut
- The "CAGED" name is one of 5 equivalent cyclic orderings
- Different tunings produce different shape systems, confirming CAGED is tuning-derived

## Further Reading
- [GTR-001: The Fretboard Map](gtr-001-the-fretboard-map.md) -- prerequisite
- Department of Music: Tuning systems and temperament
- Department of Physics: Acoustics of string vibration and harmonics
- Department of Mathematics: Group theory and fretboard symmetry

---
*Produced by Seldon Research Cycle guitar-studies-2026-03-23-001 on 2026-03-23.*
*Research question: Do common open chord voicings share structural patterns that predict their moveable barre chord forms?*
*Belief: T (confidence: 0.85)*
