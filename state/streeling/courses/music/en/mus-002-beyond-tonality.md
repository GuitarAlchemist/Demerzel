---
module_id: mus-002-beyond-tonality
department: music
course: "Foundations of Music Theory"
level: intermediate
alchemical_stage: albedo
prerequisites:
  - mus-001-what-is-a-chord
estimated_duration: "45 minutes"
produced_by: music
version: "1.0.0"
---

# Beyond Tonality: Post-Tonal Theory for Guitarists

> **Department of Music** | Stage: Albedo (Intermediate) | Duration: 45 minutes

## Objectives

After this lesson, you will be able to:
- Explain the historical dissolution of common-practice tonality and the emergence of atonality
- Translate pitches into pitch-class integer notation and compute normal and prime forms
- Construct interval vectors and identify set classes using Forte numbers
- Derive the four row forms of a twelve-tone row and understand the 12x12 matrix
- Analyze free atonal music through pitch centricity, motivic cells, and registral distribution
- Apply post-tonal thinking to modern guitar repertoire and your own composition/improvisation
- Recognize how set theory provides a bridge back to jazz voicing analysis

---

## 1. The End of Common Practice

For roughly 300 years — from Bach through Brahms — Western art music operated within a shared system called **common-practice tonality**. This system had a clear grammar: a tonic center, functional harmony (tonic-subdominant-dominant), and melodic organization around diatonic scales. Every chord had a role; every note had a destination.

By the late 19th century, composers began stretching this grammar until it snapped. Wagner's opera *Tristan und Isolde* (1859) opens with a chord — the famous "Tristan chord" (F-B-D#-G#) — that refuses to resolve in any traditional way. For several hours of music, Wagner defers the expected tonic resolution, keeping the listener suspended in chromatic ambiguity. The opera ends with resolution, but the message was clear: tonal function could be delayed, weakened, and eventually dissolved.

Debussy, Mahler, Strauss, and Scriabin continued this chromatic expansion. Chords became so laden with non-chord tones, altered extensions, and parallel motion that the underlying tonal skeleton disappeared. By the early 1900s, the question became unavoidable: if chords no longer need to resolve, and if keys are no longer binding, what remains?

**Schoenberg's Emancipation of Dissonance:**

Arnold Schoenberg answered the question with a radical claim in 1908: **dissonance does not need to resolve**. In traditional theory, consonance was "natural" and dissonance was a deviation that must be corrected. Schoenberg argued this was a historical convention, not an acoustic law. Dissonance and consonance are not opposites — they are points on a continuum, and composers should be free to use any sonority as a stable event.

This emancipation of dissonance broke the last constraint of tonality. Schoenberg's *Three Piano Pieces, Op. 11* (1909) is often cited as the first "atonal" work. No key signature. No resolution to a tonic. Pitches organized by motivic and registral logic rather than functional harmony.

**Two Paths: Free Atonality vs. Serialism:**

After emancipation, composers diverged along two paths:

- **Free atonality:** Intuitive, motivic, non-systematized. Pitches chosen by ear and structural logic. Schoenberg (1908-1920), Berg, early Webern, Varese, Ives. The composer's ear is the only authority.
- **Serialism (twelve-tone technique):** A systematic method Schoenberg developed in 1921 to organize atonal pitch material. Each composition is based on an ordered row of all 12 pitch classes, manipulated through specific operations. The system replaced the tonal grammar with a new one.

Both paths share the same foundation: the 12 equal-tempered pitch classes are treated as a democratic set, with no note privileged over any other. This is the starting point of post-tonal theory.

---

## 2. Pitch-Class Integer Notation

Post-tonal theory needs a notation that treats the 12 pitch classes as equivalent and abstract. Traditional letter names (C, D, E...) are convenient but tied to tonal baggage — enharmonic spellings (C# vs. Db) suggest different tonal meanings that are irrelevant in post-tonal analysis.

The solution: **integer notation**. Assign an integer to each pitch class:

| Pitch | Integer |
|-------|---------|
| C     | 0       |
| C#/Db | 1       |
| D     | 2       |
| D#/Eb | 3       |
| E     | 4       |
| F     | 5       |
| F#/Gb | 6       |
| G     | 7       |
| G#/Ab | 8       |
| A     | 9       |
| A#/Bb | 10 (t)  |
| B     | 11 (e)  |

**Octave Equivalence:** In pitch-class space, all Cs are "the same" — there is no middle C vs. low C. The integer 0 represents the class of all Cs at all octaves. A set of pitches becomes a set of integers modulo 12.

**Enharmonic Equivalence:** C# and Db are the same pitch class (1). Post-tonal analysis discards the tonal distinction because there is no key context to justify it.

**Normal Form:**

Given a set of pitches, the **normal form** is the most compact ordering of the set. To find it:

1. Arrange the pitch classes in ascending order around the chromatic circle.
2. Consider each rotation of the set.
3. Choose the rotation with the smallest span from first to last element.
4. If multiple rotations tie, choose the one most packed toward the left (smallest second element, then third, etc.).

**Example:** The set {E, G#, C} = {4, 8, 0}. Rotations (as intervals from first to last around the circle):
- 0, 4, 8: span = 8
- 4, 8, 0: span = 8 (but 0 means "0 + 12 = 12", so span = 12 - 4 = 8)
- 8, 0, 4: span = 8

All rotations are symmetric (it is an augmented triad). By convention, we choose {0, 4, 8}.

**Prime Form:**

The **prime form** is the most abstract representation of a set class — it removes distinctions of transposition AND inversion. To find the prime form:

1. Compute the normal form.
2. Compute the inversion's normal form (invert the set around 0 by negating each element mod 12, then normalize).
3. Choose whichever of the two is more left-packed.
4. Transpose so that the first element is 0.

Prime forms are written in square brackets: [0,3,7] for the minor triad, [0,4,7] for the major triad.

**Wait — are major and minor triads different set classes?** Yes, but their prime forms are related by inversion: [0,3,7] (minor) inverts to [0,4,7] (major). In Forte's classification, both belong to set class **3-11**, because the system considers inversion-equivalent sets as one class. In practice: [0,3,7] is the canonical prime form for the 3-11 set class.

### Practice Exercise

The open strings of a guitar (standard tuning) are E-A-D-G-B-E. Converting to pitch-class integers:
- E = 4
- A = 9
- D = 2
- G = 7
- B = 11

Treating the open strings as a set (ignoring the octave doubling of E): {2, 4, 7, 9, 11}.

Your task:
1. Arrange these in ascending order.
2. Determine the normal form.
3. Compute the prime form.

**Answer walkthrough:**
- Ascending: {2, 4, 7, 9, 11}
- Rotations and spans:
  - (2, 4, 7, 9, 11): span = 11 - 2 = 9
  - (4, 7, 9, 11, 2+12=14): span = 14 - 4 = 10
  - (7, 9, 11, 14, 16): span = 9
  - (9, 11, 14, 16, 19): span = 10
  - (11, 14, 16, 19, 21): span = 10
- Tied rotations: (2,4,7,9,11) and (7,9,11,2,4). Compare second elements: 4 vs. 9. Choose 4. Normal form: {2, 4, 7, 9, 11}.
- Transpose to start at 0: subtract 2 from each → {0, 2, 5, 7, 9}.
- Check inversion: invert {0,2,5,7,9} → {0,-2,-5,-7,-9} mod 12 = {0, 10, 7, 5, 3}. Reorder: {0, 3, 5, 7, 10}. This is more left-packed than {0,2,5,7,9}? Compare: second elements 2 vs. 3 — {0,2,5,7,9} wins (2 < 3).
- **Prime form: [0,2,5,7,9]** — this is set class 5-35, the **pentatonic/diatonic subset** (the anhemitonic pentatonic scale). The guitar's open strings form a pentatonic set class.

---

## 3. Interval Vectors and Set Classes

Beyond pitch content, post-tonal analysis cares about **interval content** — which intervals are present in a set, and how many of each. This is captured by the **interval vector**.

**Interval Class (ic):**

In post-tonal theory, intervals are classified 0 through 6 (there are only 7 interval classes because interval classes are symmetric around the tritone):

| ic | Semitones | Example |
|----|-----------|---------|
| 0  | unison/octave | C-C |
| 1  | minor 2nd / major 7th | C-Db / C-B |
| 2  | major 2nd / minor 7th | C-D / C-Bb |
| 3  | minor 3rd / major 6th | C-Eb / C-A |
| 4  | major 3rd / minor 6th | C-E / C-Ab |
| 5  | perfect 4th / perfect 5th | C-F / C-G |
| 6  | tritone | C-F# |

A minor 2nd (1 semitone) and a major 7th (11 semitones) are the same interval class because they are inversions of each other.

**Building the Interval Vector:**

The interval vector is a 6-element list counting how many of each interval class (ic1 through ic6) appear between all pairs of notes in a set.

**Example — C Major Triad {0, 4, 7}:**
- Pairs: (0,4), (0,7), (4,7)
- Intervals: 4-0=4 (ic4), 7-0=7 (ic5), 7-4=3 (ic3)
- Count: ic1=0, ic2=0, ic3=1, ic4=1, ic5=1, ic6=0
- **Interval vector: [001110]**

Notice: the major triad and the minor triad share the same interval vector [001110] because they are inversionally related. This is why they belong to the same set class: **3-11**.

**Forte Numbers:**

Allen Forte (1973) cataloged every possible set class from 3 to 9 notes and assigned each a number. The format is **cardinality-ordinal**:

- **3-11:** The 11th set class of cardinality 3 — the major/minor triad.
- **3-12:** The augmented triad [0,4,8], interval vector [000300].
- **4-20:** The major 7th chord [0,1,5,8], interval vector [101220].
- **3-1:** The chromatic trichord [0,1,2], interval vector [210000].
- **6-Z28 / 6-Z49:** Z-related hexachords (see below).

The ordinal numbers reflect an ordering Forte chose based on interval content, roughly from most compact (lowest ordinals) to most dispersed.

**Z-Relations:**

Some distinct set classes share the same interval vector despite having different pitch contents and not being related by transposition or inversion. These are called **Z-related** sets. Forte marked them with a Z prefix. The most famous example: set classes 4-Z15 and 4-Z29 both have interval vector [111111] (the "all-interval tetrachord"), but they are genuinely different sets. Z-relations fascinated Elliott Carter and Milton Babbitt because they represent a deep symmetry in interval space.

### Practice Exercise

Compute the interval vector for **Esus4** on the guitar. Esus4 consists of E, A, B — pitch classes {4, 9, 11}.

**Walkthrough:**
- Pairs and intervals:
  - (4, 9): 9 - 4 = 5 → ic5
  - (4, 11): 11 - 4 = 7 → ic5 (because ic = min(7, 12-7) = 5)
  - (9, 11): 11 - 9 = 2 → ic2
- Count: ic1=0, ic2=1, ic3=0, ic4=0, ic5=2, ic6=0
- **Interval vector: [010020]**

This set class contains one major-2nd interval and two perfect-4th/5th intervals. Its prime form is [0,2,7], set class **3-9**. This is the quartal trichord — a sound central to jazz voicings (e.g., McCoy Tyner's left-hand comping) and 20th-century orchestral writing (Copland, Hindemith).

---

## 4. Twelve-Tone Rows and Serial Operations

Schoenberg's twelve-tone method (1921) organized atonal pitch material through an **ordered row** — a specific sequence containing all 12 pitch classes, each appearing exactly once. The row serves as the composition's genetic code; every melody, harmony, and counterpoint derives from it.

**The Four Row Forms:**

Given a **prime row (P0)** — the original ordering — three transformations generate three related row forms:

1. **Prime (P):** The original row.
2. **Retrograde (R):** The row played backwards (last note first).
3. **Inversion (I):** Each interval of the original row flipped in direction. If P goes up a minor 3rd, I goes down a minor 3rd.
4. **Retrograde Inversion (RI):** The inversion played backwards.

Each form can be **transposed** to start on any of the 12 pitch classes, yielding **48 total row forms** (4 operations × 12 transpositions).

**Example — Simple Row:**

Let P0 = [0, 1, 3, 2, 5, 4, 7, 6, 9, 8, 11, 10] (a fabricated row).

- **R0:** Reverse P0 → [10, 11, 8, 9, 6, 7, 4, 5, 2, 3, 1, 0]
- **I0:** Invert around 0. For each element x in P0, compute (0 - x) mod 12:
  - P0: [0, 1, 3, 2, 5, 4, 7, 6, 9, 8, 11, 10]
  - I0: [0, 11, 9, 10, 7, 8, 5, 6, 3, 4, 1, 2]
- **RI0:** Reverse I0 → [2, 1, 4, 3, 6, 5, 8, 7, 10, 9, 11, 0]

**Transposition:** To create P3 (prime form starting on pitch class 3), add 3 to each element of P0 (mod 12): [3, 4, 6, 5, 8, 7, 10, 9, 0, 11, 2, 1].

**The 12x12 Matrix:**

A twelve-tone matrix is a compact way to display all 48 row forms:

- **Rows** (left to right) are the 12 transpositions of P, labeled P0 through P11 by their first pitch class.
- **Rows read right to left** are retrogrades (R0 through R11).
- **Columns** (top to bottom) are the 12 transpositions of I, labeled by their first pitch class.
- **Columns read bottom to top** are retrograde inversions.

To construct the matrix:
1. Write P0 across the top row.
2. Write I0 down the left column (the inversion of P0, starting on the same first note).
3. Each subsequent row is P0 transposed so its first note matches the leftmost column.

**Combinatoriality:**

Some rows have a special property called **combinatoriality**: if you split the row into two hexachords (first 6 notes, last 6 notes), a particular transposition of I produces hexachords that together with P's hexachords form two complete aggregates (all 12 pitch classes in each half). Schoenberg exploited combinatoriality extensively because it allows simultaneous statement of P and I without pitch-class repetition — a kind of twelve-tone counterpoint that preserves the atonal ideal of non-privilege.

### Practice Exercise

Given **P0 = [7, 10, 8, 0, 5, 2, 4, 9, 11, 1, 3, 6]** (the opening of Webern's *Concerto, Op. 24* reordered for this exercise):

1. Derive **R0** by reversing P0.
2. Derive **I0** by computing (7 - x + 7) mod 12 for each element — equivalently, invert around the first note. A simpler method: compute (2 × 7 - x) mod 12 for each x in P0, which reflects each note around the pitch class 7.
3. Derive **RI0** by reversing I0.

**Walkthrough:**

- **R0:** [6, 3, 1, 11, 9, 4, 2, 5, 0, 8, 10, 7]

- **I0** (inversion around 7, formula (14 - x) mod 12):
  - 7 → (14-7) mod 12 = 7
  - 10 → (14-10) mod 12 = 4
  - 8 → (14-8) mod 12 = 6
  - 0 → (14-0) mod 12 = 2
  - 5 → (14-5) mod 12 = 9
  - 2 → (14-2) mod 12 = 0
  - 4 → (14-4) mod 12 = 10
  - 9 → (14-9) mod 12 = 5
  - 11 → (14-11) mod 12 = 3
  - 1 → (14-1) mod 12 = 1
  - 3 → (14-3) mod 12 = 11
  - 6 → (14-6) mod 12 = 8
  - **I0: [7, 4, 6, 2, 9, 0, 10, 5, 3, 1, 11, 8]**

- **RI0:** Reverse I0 → [8, 11, 1, 3, 5, 10, 0, 9, 2, 6, 4, 7]

Verify each row contains each pitch class 0-11 exactly once.

---

## 5. Free Atonality

Not all atonal music is serial. **Free atonality** — the music of Schoenberg (1908-1920), early Berg, early Webern, and many later composers — organizes pitches without the systematic constraints of twelve-tone rows. Instead, it relies on intuitive principles:

**Pitch Centricity (Without Tonality):**

Even without a tonic, certain pitches can gain structural prominence through:
- **Repetition:** A pitch that recurs throughout a piece becomes a reference point.
- **Register:** A pitch consistently placed in an extreme register (very high or very low) acquires emphasis.
- **Rhythm:** A pitch assigned to strong beats or long durations stands out.
- **Timbre:** A pitch consistently presented by a distinctive instrument becomes memorable.

This is **pitch centricity**: the emergence of focal pitches without the functional apparatus of tonality. The pitch is central not because it is "the tonic" but because the composer has structurally emphasized it.

**Motivic Cells:**

Free atonal music typically relies on small pitch-class sets — **motivic cells** — as its structural DNA. A cell is a 3- to 5-note set class that appears throughout a piece in various transpositions, inversions, and voicings. Webern's *Five Pieces for Orchestra, Op. 10* uses only a handful of set classes across its entire duration; the economy is astonishing.

The cell functions like a Wagnerian leitmotif but at the pitch-class level rather than the melodic level. The listener hears coherence without being able to articulate why.

**Set-Class Progressions:**

A sequence of set classes across a piece can create large-scale structural motion. For example, a piece might begin with small, chromatic set classes (3-1 [0,1,2]) and gradually expand to larger, more diatonic set classes (5-35 [0,2,4,7,9]). Or vice versa: a journey from consonance to dissonance, or from tension to release, without relying on tonal cadence.

**Registral Distribution:**

In atonal music, register often carries structural meaning. Webern was famous for distributing the notes of a single chord or melodic line across extreme registers — a phenomenon called **Klangfarbenmelodie** (tone-color melody). The result: the listener perceives the piece as much through space and timbre as through pitch. Post-tonal analysis must consider where notes are placed, not just which pitch classes appear.

**Berg's Tonal Echoes:**

Alban Berg occupies a fascinating middle ground. His works (e.g., *Violin Concerto*) use twelve-tone rows that contain tonal subsets — triads, dominant sevenths, diatonic fragments. The result is atonal music that repeatedly evokes tonal memory without ever committing to a key. Berg's music is a lesson that "atonal" does not mean "anti-tonal" — it can mean "tonal in pieces, but not in grammar."

---

## 6. Guitar Applications and Repertoire

Post-tonal techniques are not abstract exercises — they have a rich presence in the modern guitar repertoire and in improvisational practice.

**Henze — *Royal Winter Music* (1976):**

Hans Werner Henze's two sonatas on characters from Shakespeare are among the most important atonal works in the guitar repertoire. *Royal Winter Music I* contains six movements (Gloucester, Romeo and Juliet, Ariel, Ophelia, Touchstone, Oberon). Each character is portrayed through a unique pitch-class vocabulary — a small set of motivic cells developed throughout the movement. The sonata is atonal but gestural: recognizable as character portraits even without tonal centers.

**Britten — *Nocturnal after John Dowland, Op. 70* (1963):**

Britten's masterpiece for solo guitar takes a theme by the Renaissance composer John Dowland and subjects it to eight variations of increasing distance from tonality. The early variations feel unsettled but recognizable; middle variations dissolve into free atonal textures; the final variation (a passacaglia) returns to tonal clarity. The piece is a journey through post-tonal techniques that resolves back into common-practice harmony — a reconciliation rather than a rejection.

**Building an Atonal Etude — Practical Method:**

Here is a process for composing a short atonal guitar etude using a trichord cell:

1. **Choose a trichord cell.** Example: set class 3-3 [0,1,4] — a chromatic cluster plus a third. In pitches: C, C#, E.
2. **Map it to CAGED positions.** Find [0,1,4] transpositions that fall naturally under each of the five CAGED shapes. At position V (5th fret): A, Bb, C#. At position III: G, Ab, B. And so on.
3. **Compose phrases that cycle through positions.** Each phrase states the cell in one position, then transitions to the next. The cell's identity is preserved while the fretboard location shifts.
4. **Vary register, dynamics, articulation.** Apply free-atonal registral distribution: play some cells compressed, others spread across two octaves.
5. **Use inversion and retrograde.** State [0,1,4], then its inversion [0,3,4], then its retrograde, then retrograde-inversion. Motivic development via serial operations.

This method produces music that is atonal, coherent, and specifically guitaristic — the fretboard geometry shapes the musical form.

**Improvisation Applications:**

Jazz guitarists (e.g., Ben Monder, Kurt Rosenwinkel, Mary Halvorson) frequently use atonal techniques in their improvisations: trichord cells, interval vectors as sonority guides, quartal and chromatic voicings. Understanding set theory equips the improviser to move consciously between tonal and post-tonal languages, treating them as a unified spectrum rather than opposed systems.

---

## 7. Bridging Back

Post-tonal theory is not a rejection of tonal theory — it is a generalization. The tools developed for atonal analysis illuminate tonal music in new ways, and they provide a bridge between traditions that might otherwise seem incompatible.

**Set Theory as a Tool for Jazz Voicing Analysis:**

Jazz harmony is notoriously complex: extensions, alterations, polychords, upper-structure triads. Traditional tonal analysis struggles to describe a chord like **G7alt(b9,#9,b13)**. But set-class analysis reduces it to a pitch-class set and identifies its set class directly. The chord above has pitch classes {7, 11, 5, 9, 10, 3}; its prime form is a specific hexachord whose interval vector characterizes its sonority.

This gives jazz theorists a language that cuts across chord-symbol conventions. Two chords with different chord symbols might belong to the same set class and therefore share the same interval content. Two chords with similar symbols might belong to different set classes. Set theory reveals the actual sonority underneath the notation.

**Interval Vectors as Sonority Measures:**

The interval vector quantifies a chord's "color." A chord with many ic3s and ic4s (thirds) sounds tertian. A chord dominated by ic5s sounds quartal. A chord with many ic2s and ic6s sounds dense and dissonant. By reading a chord's interval vector, you can predict its sonic character without even hearing it.

This is immediately useful for guitarists: when choosing a voicing for an ambiguous chord, you can select the voicing whose interval vector matches the sonority you want — open and quartal, dense and chromatic, or somewhere in between.

**OPTIC/K and Pitch-Class Equivalence:**

In neo-Riemannian and transformational theory, voice-leading equivalences are described by the **OPTIC** relations:
- **O**ctave equivalence: two pitches an octave apart are the same.
- **P**ermutation: reordering within an octave does not change identity.
- **T**ransposition: two chords related by a single interval are equivalent.
- **I**nversion: mirror-image chords are equivalent.
- **C**ardinality: doublings do not count.

These are exactly the principles of pitch-class set theory, expressed slightly differently. OPTIC makes explicit that set theory is not exotic — it is the formalization of how musicians have always heard equivalences (a C major chord is "the same" whether voiced C-E-G or G-C-E or C-E-G-C).

The **K** relation adds a further layer (considering equivalence up to set-class membership). Together, OPTIC and K provide a mathematical framework that unifies tonal voice-leading analysis with post-tonal set theory. The two traditions are not opposed — they are two dialects of the same underlying language.

---

## Key Terms

| Term | Definition |
|------|-----------|
| **Common-practice tonality** | The harmonic system of Western art music from roughly 1600-1900, based on functional harmony and key centers |
| **Emancipation of dissonance** | Schoenberg's 1908 claim that dissonant sonorities need not resolve to consonance |
| **Atonality** | Music organized without a tonal center or key |
| **Free atonality** | Atonal music organized intuitively through motivic cells, registral distribution, and pitch centricity |
| **Serialism (twelve-tone)** | Systematic organization of atonal music based on an ordered row of 12 pitch classes |
| **Pitch class** | An equivalence class of pitches related by octave (e.g., all Cs belong to pitch class 0) |
| **Integer notation** | Representation of pitch classes by integers 0-11 |
| **Normal form** | The most compact ordering of a pitch-class set |
| **Prime form** | The canonical representative of a set class, including inversional equivalence, transposed to start at 0 |
| **Interval class (ic)** | An equivalence class of intervals (0-6) where inversion-related intervals are grouped together |
| **Interval vector** | A 6-element list counting occurrences of each interval class in a set |
| **Set class** | A group of pitch-class sets related by transposition and inversion, labeled by Forte number |
| **Forte number** | Allen Forte's catalog label for a set class, formatted as cardinality-ordinal (e.g., 3-11) |
| **Z-relation** | The relationship between distinct set classes that share the same interval vector |
| **Prime/Retrograde/Inversion/Retrograde-Inversion (P/R/I/RI)** | The four serial operations applied to a twelve-tone row |
| **Combinatoriality** | Property of certain rows whose hexachords combine with transposed forms to produce aggregates |
| **Pitch centricity** | Structural emphasis of certain pitches in atonal music without tonal function |
| **Motivic cell** | A small pitch-class set used as structural DNA throughout an atonal composition |

---

## Self-Check Assessment

**1. What did Schoenberg mean by "the emancipation of dissonance," and why was it a historical turning point?**
> Schoenberg claimed in 1908 that dissonant sonorities do not need to resolve to consonances — that the distinction between consonance and dissonance is historical convention, not an acoustic law. It was a turning point because it removed the last constraint of common-practice tonality (the obligation to resolve tension), opening the door to atonal composition where any sonority could stand as a stable structural event.

**2. Compute the prime form of the set {D, F, A, C} (a D minor 7th chord). Show the normal form and one inversion check.**
> Pitch classes: {2, 5, 9, 0} → ascending {0, 2, 5, 9}. Rotations and spans:
> - (0, 2, 5, 9): span = 9
> - (2, 5, 9, 0+12=12): span = 10
> - (5, 9, 12, 14): span = 9
> - (9, 12, 14, 17): span = 8 — smallest!
> Normal form: {9, 0, 2, 5}. Transpose to start at 0: subtract 9 → {0, 3, 5, 8}. Inversion: {0, -3, -5, -8} mod 12 = {0, 9, 7, 4} → reorder {0, 4, 7, 9}. Compare {0,3,5,8} vs {0,4,7,9}: second element 3 < 4, so {0,3,5,8} is more left-packed.
> **Prime form: [0,3,5,8]** — set class 4-26, the minor 7th / minor-triad-plus-7 sonority.

**3. Given P0 = [0, 1, 4, 9, 5, 11, 2, 7, 6, 10, 3, 8], derive I0 (inversion starting on 0). Show the formula used.**
> Formula: I0[k] = (0 - P0[k]) mod 12 = (-P0[k]) mod 12.
> - 0 → 0
> - 1 → 11
> - 4 → 8
> - 9 → 3
> - 5 → 7
> - 11 → 1
> - 2 → 10
> - 7 → 5
> - 6 → 6
> - 10 → 2
> - 3 → 9
> - 8 → 4
> **I0: [0, 11, 8, 3, 7, 1, 10, 5, 6, 2, 9, 4]**

**4. What is a Z-relation, and why is it significant in post-tonal theory?**
> A Z-relation is the property shared by two distinct set classes that have identical interval vectors but are not related by transposition or inversion. It is significant because it reveals that interval content (what intervals are present) does not uniquely determine set-class identity (what pitch configurations produce those intervals). Z-related sets sound very similar in sonority but are structurally distinct, a deep symmetry exploited by composers like Elliott Carter and Milton Babbitt.

**5. How does set-theory analysis provide a bridge between post-tonal music and jazz harmony?**
> Set theory abstracts chords into pitch-class sets and set classes, cutting through the conventions of chord symbols. A complex jazz altered-dominant chord can be identified by its set class and characterized by its interval vector, revealing its underlying sonority in a way that chord symbols obscure. This lets jazz analysts compare voicings across apparently different chord qualities, recognize shared sonorities, and understand atonal and jazz languages as dialects of the same pitch-class framework rather than opposed systems.

**Pass criteria:** Compute the prime form of a given 4-5 note chord, derive I0 and R0 from a given P0, and explain the structural function of a motivic cell in a free atonal context.

---

## Research Basis

- Pitch-class set theory formalized by Allen Forte in *The Structure of Atonal Music* (1973); Forte numbers remain the standard cataloging system
- Joseph N. Straus's *Introduction to Post-Tonal Theory* (4th ed., 2016) is the standard pedagogical text and source for normal/prime form algorithms
- George Perle's *Serial Composition and Atonality* (6th ed., 1991) provides historical and analytical grounding for twelve-tone technique
- Neo-Riemannian theory and OPTIC relations extend set theory toward voice-leading analysis (Cohn, 2012; Tymoczko, *A Geometry of Music*, 2011)
- Guitar repertoire references: Henze *Royal Winter Music I & II*; Britten *Nocturnal Op. 70*; Takemitsu *All in Twilight*; Ginastera *Sonata Op. 47*
- Schoenberg's own writings (*Style and Idea*, 1950) document the emancipation of dissonance in his own words
- Sources: Forte 1973, Straus 2016, Perle 1991, Tymoczko 2011, Cohn 2012, Schoenberg 1950
- Belief state: T(0.85) F(0.03) U(0.08) C(0.04)
