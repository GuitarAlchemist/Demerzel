---
module_id: mus-005-jazz-harmony
department: music
course: Jazz Harmony for Guitar
level: intermediate-to-advanced
alchemical_stage: citrinitas
prerequisites:
  - mus-001-what-is-a-chord
  - mus-003-functional-harmony
  - gtr-002-caged-geometry
estimated_duration: "3 hours"
produced_by: music
version: "1.0.0"
---

# Jazz Harmony for Guitar: From ii-V-I to Coltrane Changes

> **Department of Music** | Stage: Citrinitas (Intermediate-to-Advanced) | Duration: 3 hours

## Learning Objectives

After completing this course, you will be able to:

- Read and interpret any jazz chord symbol, including extensions, alterations, and slash notation
- Identify ii-V-I progressions in major and minor keys within standard jazz repertoire
- Voice lead through chord changes using shell voicings, drop-2, and drop-3 forms
- Apply guide-tone voice leading to connect chords smoothly
- Employ tritone substitution, diminished substitution, and backdoor dominant techniques
- Associate appropriate scales with chord qualities using chord-scale theory
- Construct quartal voicings and upper-structure triads for modern jazz sonority
- Analyze and apply Coltrane's symmetric major-third substitution cycle

---

## 1. Jazz Chord Symbol Literacy

Jazz chord symbols are a compressed notation language. Unlike classical figured bass, they encode quality, extensions, alterations, and bass notes in a single compact symbol. Reading them fluently is a prerequisite for everything that follows.

### Anatomy of a Chord Symbol

Every jazz chord symbol has up to four components:

```
Root  +  Quality  +  Extensions/Alterations  +  Slash Bass
 C        maj           9#11                      /E
```

**Root:** Any letter A through G, optionally with # or b.

**Quality** encodes the triad and seventh:

| Symbol | Meaning | Third | Seventh |
|--------|---------|-------|---------|
| (nothing) or `maj` | Major triad | Major 3rd | — |
| `m` or `min` or `-` | Minor triad | Minor 3rd | — |
| `7` | Dominant seventh | Major 3rd | Minor 7th |
| `maj7` or `M7` or triangle | Major seventh | Major 3rd | Major 7th |
| `m7` or `min7` or `-7` | Minor seventh | Minor 3rd | Minor 7th |
| `m7b5` or half-diminished | Half-diminished | Minor 3rd | Minor 7th (b5) |
| `dim7` or `o7` | Diminished seventh | Minor 3rd | Diminished 7th |

**Extensions** add upper chord tones (9, 11, 13). The highest number implies all odd-numbered tones below it:

- `Cmaj9` = C E G B D (implies the 7th is present)
- `Cmaj13` = C E G B D (F#) A (implies 9 and 7; the 11 is typically #11 in a major context)

**Alterations** modify specific tones:

- `#11` — raised 11th (avoids clash with major 3rd)
- `b9`, `#9` — lowered or raised 9th
- `b13` — lowered 13th (enharmonic to #5)
- `alt` — shorthand for dominant with b9, #9, #11/b5, b13/#5

### The C7 vs Cmaj7 Ambiguity

This trips up every beginner:

- **C7** = C E G **Bb** (dominant seventh — the default "7" is a minor seventh interval)
- **Cmaj7** = C E G **B** (major seventh — the "maj" qualifier raises the seventh)

The bare "7" always means dominant. You must write "maj7" to get a major seventh. This convention is a historical artifact from blues and early jazz where dominant sevenths were the default sound.

### Slash Chords

`C/E` means "C major chord with E in the bass." The note after the slash is the bass note, not necessarily a chord tone. Common uses:

- Inversions: `C/E` (first inversion), `C/G` (second inversion)
- Polychords implied: `Db/C` = Db triad over C bass (creates a Cmaj7#11 sound)
- Pedal tones: `Dm7/G` = creates a G11 sound without stating G as root

### Practice Exercise

Read the following chord symbols and spell out the notes. Do not use your instrument — work from the symbol alone:

1. `Fmaj9#11`
2. `Bb7alt`
3. `Ebm11`
4. `Ab13`
5. `Dm7b5`
6. `G7#9/Db` (what substitution does this imply?)

Answers:
1. F A C E G B (F major with major 7th, 9th, #11th)
2. Bb D Ab B/Cb Eb/D# Gb (dominant with all altered upper extensions)
3. Eb Gb Bb Db F Ab (minor 7th with 11th)
4. Ab C Eb Gb Bb Db F (dominant 7th with 9th, 11th implicit, 13th)
5. D F Ab C (minor triad with flatted 5th and minor 7th)
6. G B D F A#/Bb over Db bass — the Db bass implies tritone substitution of G7

---

## 2. The ii-V-I Universe

The ii-V-I progression is the gravitational center of jazz harmony. Understanding it is like understanding sentences in a language — once you hear them, you hear them everywhere.

### Major ii-V-I

In C major:

```
  Dm7    →    G7    →    Cmaj7
  ii7         V7         Imaj7
```

Why does this work? Each chord resolves to the next by the strongest root motion in tonal music — descending fifths (D→G→C). The voice leading is equally powerful: the 3rd of Dm7 (F) resolves down to the 3rd of G7 (B is not F, but the 7th of Dm7, C, becomes the 7th relationship). More precisely:

- The **7th of ii** (C) steps down to the **3rd of V** (B)
- The **3rd of V** (B) steps up to the **root of I** (C)
- The **7th of V** (F) steps down to the **3rd of I** (E)

This stepwise chromatic pull creates an irresistible sense of resolution.

### Minor ii-V-i

In C minor:

```
  Dm7b5  →    G7alt   →    Cm(maj7) or Cm7
  ii-half      V7alt        i
```

The half-diminished ii provides the minor-key color. The altered dominant (G7alt) contains both b9 (Ab) and b13 (Eb), which are the b6 and b3 of C minor — the very notes that define the minor key.

### Extended ii-V Chains

Jazz tunes often chain ii-V's across multiple keys without resolving:

```
  Em7  A7  |  Dm7  G7  |  Cmaj7
  ii   V      ii   V      I
  (of D)      (of C)      (arrived)
```

The turnaround — the last bars of a form that lead back to the top — is the most common extended chain:

```
  Cmaj7  Am7  |  Dm7  G7  ||  (back to Cmaj7)
  I      vi      ii   V        I
```

### Practice Exercise

Here is the chord progression to **"All The Things You Are"** (Kern/Hammerstein). Circle every ii-V-I (major or minor). Mark whether each resolves or is left hanging:

```
Fm7   | Bbm7   | Eb7    | Abmaj7 |
Dbmaj7| Dm7    | G7     | Cmaj7  |
Cm7   | Fm7    | Bb7    | Ebmaj7 |
Abmaj7| Am7    | D7     | Gmaj7  |
Am7   | D7     | Gmaj7  |        |
F#m7  | B7     | Emaj7  | C7alt  |
Fm7   | Bbm7   | Eb7    | Abmaj7 |
Dbmaj7| Dbm7   | Cm7    | Bdim7  |
Bbm7  | Eb7    | Abmaj7 |        |
```

You should find at least six ii-V-I progressions in three different keys, plus several ii-V's that resolve deceptively or chain into the next key area.

---

## 3. Jazz Guitar Voicings

Pianists can voice chords with ten fingers across five octaves. Guitarists have six strings and four fretting fingers. This constraint is actually a gift — it forces economical voicings that cut through an ensemble and voice lead beautifully.

### Shell Voicings (Root + 3rd + 7th)

The root, 3rd, and 7th are the **essential tones** that define a chord's quality and function. The 5th is almost always omitted (it adds no harmonic information unless altered).

**Root on 6th string:**

```
Dm7:        G7:         Cmaj7:
e ----      e ----      e ----
B ----      B ----      B ----
G ----      G ----      G ----
D ----      D ----      D ----
A --5--     A ----      A --3--
E --x--     E --3--     E --x--
   1 b3 b7     1 3 b7      1 3 7
```

(Actual fret positions depend on root location; the concept is root-3rd-7th on adjacent strings.)

**Root on 5th string:**

Shells on the 5th string keep the voicing in a comfortable middle register. The 3rd and 7th fall on strings 4 and 3, leaving the top strings available for melody or extensions.

### Drop-2 Voicings

Take a close-position four-note chord and "drop" the second-highest note down an octave. This spreads the voicing across four adjacent strings — perfect for guitar.

**Close position Cmaj7:** B-E-G-C (top to bottom: C-G-E-B in ascending order, then rearrange with second from top dropped)

**Drop-2 Cmaj7 (string set 5-4-3-2):**

```
e ----
B --0-- (B, the 7th)
G --0-- (G, the 5th)
D --2-- (E, the 3rd — dropped from close position)
A --3-- (C, the root)
E ----
```

Drop-2 voicings exist on four string sets:

| String Set | Range | Best For |
|-----------|-------|----------|
| 6-5-4-3 | Low | Comping in a duo or walking bass context |
| 5-4-3-2 | Middle | Standard comping range |
| 4-3-2-1 | High | Melodic comping, chord melody |

Each chord quality (maj7, m7, 7, m7b5) has four inversions per string set, giving you 48 drop-2 voicings to internalize (4 qualities x 4 inversions x 3 string sets).

### Drop-3 Voicings

Drop the third-highest note of a close voicing down an octave. This creates a wider spread with a gap between the bass note and the upper cluster. Drop-3 voicings span five strings (skip one string in the middle).

**String sets for drop-3:** 6-4-3-2 and 5-3-2-1.

Drop-3 voicings are darker and more orchestral. Joe Pass used them extensively for chord melody.

### Freddie Green Voicings

The Count Basie rhythm guitar approach: four-to-the-bar quarter notes, one voicing per beat, almost always on strings 6-4-3 (or 5-4-3). Only three notes — root (or shell bass note), 3rd, 7th. Strummed with a quick, percussive attack that dies immediately. The guitar becomes a pitched drum.

### Wes Montgomery / George Benson Octave Technique

Not a voicing technique in the harmonic sense, but essential jazz guitar vocabulary. Single-note lines doubled an octave apart (strings 6+4, 5+3, or 4+2), with the intervening string muted by the fretting finger. Creates a thick, horn-like tone.

### Practice Exercise

Voice lead the following ii-V-I in C major using drop-2 voicings on string set 5-4-3-2. Your goal: minimal finger movement between chords. Write out the fret positions for each chord:

```
Dm7  →  G7  →  Cmaj7
```

Rule: the 7th of one chord should resolve by step to the 3rd (or nearby tone) of the next chord. Find two different inversions that achieve this smooth connection.

---

## 4. Guide Tones and Voice Leading

### The Guide-Tone Principle

The **3rd** and **7th** of each chord are called **guide tones** because they:

1. **Define quality:** The 3rd tells you major vs minor. The 7th tells you dominant vs major vs minor.
2. **Create motion:** When chords change, the guide tones move by half step or whole step — the smallest, smoothest possible intervals.

The central miracle of ii-V-I voice leading:

```
Chord:    Dm7    G7     Cmaj7
3rd:       F  →   B  →   E
7th:       C  →   F  →   B
```

Notice:
- The **7th of Dm7 (C)** drops a half step to become the **3rd of G7 (B)**
- The **3rd of Dm7 (F)** stays put to become the **7th of G7 (F)**
- The **7th of G7 (F)** drops a half step to become the **3rd of Cmaj7 (E)**
- The **3rd of G7 (B)** stays put to become the **7th of Cmaj7 (B)**

The guide tones **exchange roles**: the 3rd of one chord becomes the 7th of the next, and vice versa. This creates a two-voice counterpoint that descends chromatically: C-B, F-E.

### Barry Harris Two-Note Comping

Barry Harris taught that you can comp through an entire tune with **just the 3rd and 7th** of each chord — two notes on the middle strings. This strips harmony to its essence and trains your ear to hear function without the crutch of full voicings.

### Building a Guide-Tone Line

A guide-tone line is a single melodic line that traces the smoothest path through a chord progression by following the 3rd or 7th of each chord. When one resolves down, follow it. When one stays, hold it.

For a solo guitar arrangement, the guide-tone line becomes the inner voice around which you build fuller voicings above and below.

### Practice Exercise

Write a guide-tone line (just 3rds and 7ths, choosing whichever moves most smoothly) through the A section of **Rhythm Changes** in Bb:

```
Bbmaj7 | G7    | Cm7   | F7    |
Dm7    | G7    | Cm7   | F7    |
```

Start on the 3rd of Bbmaj7 (D). At each chord change, move to the nearest guide tone (3rd or 7th) of the new chord. Your line should move by half step or whole step at most. Write out the resulting eight-note line.

---

## 5. Substitution Techniques

Substitution is the art of replacing one chord with another that serves a similar harmonic function but creates different color. Jazz is built on layers of substitution applied to simple underlying progressions.

### Tritone Substitution — The Deep Dive

The tritone sub replaces a dominant 7th chord with another dominant 7th chord whose root is a tritone (b5) away.

**G7 → Db7** (both resolve to C)

Why does this work? The **guide tones are shared:**

```
G7:   B (3rd)  F (7th)
Db7:  F (3rd)  Cb/B (7th)
```

The 3rd and 7th simply swap roles. The resolution to Cmaj7 works identically because F→E and B→C (or Cb→C) in both cases. What changes is the bass motion: instead of G→C (descending fifth), you get Db→C (chromatic descent) — a sleeker, more modern sound.

**Application in ii-V-I:**

```
Original:    Dm7  | G7    | Cmaj7
Tritone sub: Dm7  | Db7   | Cmaj7
With ii:     Abm7 | Db7   | Cmaj7  (Abm7 is the related ii of Db7)
```

### Diminished Substitution

A diminished 7th chord can substitute for a dominant 7th chord a half step below any of its four notes (because dim7 is symmetric — every note is a minor third from the next).

**Bdim7 can substitute for:** C7, Eb7, Gb7, or A7 (dominant chords rooted a half step above each diminished chord tone: B, D, F, Ab).

### Passing Diminished Chords

A diminished chord can connect two diatonic chords whose roots are a whole step apart:

```
Cmaj7 | C#dim7 | Dm7
I       #Idim7   ii
```

The bass line (C-C#-D) creates a chromatic walk-up. The C#dim7 acts as a rootless A7b9 (A-C#-E-G-Bb → without A: C#-E-G-Bb).

### Backdoor Dominant (bVII7 → I)

Instead of the standard V7→I resolution, jazz uses **bVII7→I**:

```
Standard: G7  → Cmaj7  (V → I)
Backdoor: Bb7 → Cmaj7  (bVII → I)
```

The bVII7 approaches the tonic from a whole step below. The resolution works because Bb7 contains D and Ab, which resolve to C and G (or E) by step. The sound is warm, unexpected, and avoids the obvious dominant pull.

The **related ii** of the backdoor dominant: Fm7 → Bb7 → Cmaj7.

### Practice Exercise

Reharmonize the bridge of **Rhythm Changes** using substitution techniques. The original bridge is:

```
D7  | D7  | G7  | G7  |
C7  | C7  | F7  | F7  |
```

Apply these substitutions:
1. Add a related ii before each dominant
2. Apply tritone subs to alternating dominants
3. Try a diminished passing chord between D7 and G7

Write out your reharmonized 8-bar bridge. There is no single correct answer — the goal is to create smooth voice leading while adding harmonic color.

---

## 6. Chord-Scale Theory

Chord-scale theory assigns a scale to each chord, providing a pool of melody notes that are consonant with that harmony. It is the standard jazz pedagogy for improvisation, though it has important limitations.

### The Core Assignments

| Chord Quality | Scale | Source | Avoid Notes |
|--------------|-------|--------|-------------|
| **Imaj7** | Ionian (major) | Major scale | 4 (F in C) |
| **Imaj7#11** | Lydian | Melodic minor on 4th degree | None |
| **ii-7** | Dorian | Major scale from 2nd degree | None (b6 adds color) |
| **V7** (resolving) | Mixolydian | Major scale from 5th degree | 4 (but usable as passing tone) |
| **V7#11** | Lydian Dominant | Melodic minor from 4th degree | None |
| **V7alt** | Altered | Melodic minor from 7th degree | None |
| **ii-7b5** | Locrian | Major scale from 7th degree | 2 (natural 9) — or use Locrian #2 |
| **i-7** | Dorian | — | — |
| **bVII7** (backdoor) | Lydian Dominant | — | — |
| **dim7** | Diminished (half-whole) | Symmetric | — |

### The Melodic Minor Mother Scale

The **melodic minor** scale (ascending form: 1 2 b3 4 5 6 7) is the jazz musician's Swiss Army knife. Its modes generate the scales for most altered and extended dominant situations:

| Mode | Degree | Name | Used For |
|------|--------|------|----------|
| 1st | Root | Melodic minor | Minor-major 7th chords |
| 2nd | 2nd degree | Dorian b2 (Phrygian #6) | sus(b9) chords |
| 3rd | 3rd degree | Lydian Augmented | maj7#5 chords |
| 4th | 4th degree | Lydian Dominant | 7#11 chords, tritone subs |
| 5th | 5th degree | Mixolydian b6 | V7 resolving to minor |
| 6th | 6th degree | Locrian #2 (Aeolian b5) | Half-diminished chords |
| 7th | 7th degree | Altered (Super Locrian) | V7alt chords |

### Avoid Notes — What They Are and Are Not

An **avoid note** is a scale degree that creates a minor 9th (b9 interval) against a chord tone when sustained. It does not mean "never play this note" — it means do not rest on it or emphasize it. As a passing tone or chromatic approach, any note is fair game.

Example: Over Cmaj7, the note F (4th degree) creates a half step (minor 9th) against E (the 3rd). Sustaining F against E produces dissonance. But F as a passing tone between E and G is perfectly natural.

### Limitations of Chord-Scale Theory

Chord-scale theory is a map, not the territory:

- It works best for slow-moving harmony where each chord lasts long enough to establish a scale
- Over fast-moving ii-V-I's, experienced players think in terms of **voice leading** and **target notes**, not scales
- The greatest jazz improvisers (Parker, Coltrane, Shorter) transcend scale-based thinking by using **chromatic approach**, **enclosures**, and **motivic development**
- Chord-scale theory says nothing about rhythm, phrasing, or storytelling — the elements that actually make a solo compelling

### Practice Exercise

For each chord in the following progression, name the chord-scale and spell out the notes. Identify any avoid notes:

```
Cmaj7 | Dm7 | G7alt | Cm(maj7) |
```

Then play through the progression on guitar, improvising a simple melody that uses only the chord tones and one or two scale tones per chord. Notice how the guide tones (3rds and 7ths) create the strongest melodic connections.

---

## 7. Quartal Harmony and Upper Structures

### Quartal Voicings

Traditional harmony stacks **thirds**. Quartal harmony stacks **fourths**. The sound is open, ambiguous, and modern — it avoids the strong major/minor pull of tertian harmony.

**McCoy Tyner's approach:** Over a D Dorian vamp, stack perfect fourths from various degrees of the scale:

```
From D: D - G - C - F     (stacked 4ths)
From E: E - A - D - G     (stacked 4ths)
From G: G - C - F - Bb    (stacked 4ths — includes b6, outside Dorian)
```

These voicings can be moved around within the mode, creating a shimmering, non-functional harmonic landscape. The individual voicings do not "resolve" — they float.

### The "So What" Voicing

From Miles Davis's landmark recording (1959). The voicing for D Dorian:

```
E - A - D - G - B
```

This is three stacked fourths (E-A-D-G) topped with a major third (G-B). It defines the modal jazz sound. Transposed up a half step for the bridge (Eb Dorian): F-Bb-Eb-Ab-C.

On guitar, the So What voicing is typically played as:

```
e --7-- (B)
B --8-- (G)
G --7-- (D)
D --7-- (A)
A --7-- (E)
E ----
```

### Upper-Structure Triads

An upper-structure triad is a simple major or minor triad superimposed over a dominant 7th chord, creating rich extensions and alterations without complex chord symbols.

Over **C7**, various upper-structure triads produce:

| Upper Triad | Notes (over C-E-Bb) | Extensions Created |
|-------------|---------------------|-------------------|
| D major | D F# A | 9, #11, 13 — the Lydian Dominant sound |
| Eb major | Eb G Bb | #9, 5, b7 — the "Hendrix chord" extensions |
| Ab major | Ab C Eb | b13, root, #9 — the Altered sound |
| F# major | F# A# C# | #11, b7(enh), b9 — extreme altered |
| Bb major | Bb D F | b7, 9, 11 — the sus/11 sound |

The beauty of upper structures is that you play a **simple triad** — something your hands already know — while the bass player provides the root and seventh. The combination produces sophisticated harmony from simple ingredients.

### Practice Exercise

Build quartal voicings from every degree of D Dorian (D E F G A B C) on string set 4-3-2-1. Stack three perfect fourths from each starting note. Write out the four notes of each voicing and identify the resulting chord quality (some will be familiar tertian chords in disguise).

Then: over a C7 vamp, play D major triad, Ab major triad, and Eb major triad shapes in the upper register while a bass note of C sustains. Listen to how each upper structure changes the color of the dominant chord.

---

## 8. Coltrane Changes

### The Symmetric Major-Third Division

In 1959, John Coltrane introduced a substitution system that divides the octave into three equal parts (major thirds): **B - G - Eb** (or equivalently, any three notes a major third apart). This creates three tonal centers equidistant from each other.

The cycle: Starting from any key, move down a major third, then down another major third, arriving back where you started:

```
C → Ab → E → C  (descending major thirds)
or equivalently:
C → E → Ab → C  (ascending major thirds)
```

### Giant Steps Analysis

**"Giant Steps"** (Coltrane, 1960) is the definitive application. The entire composition cycles through three key centers a major third apart:

```
Bmaj7 D7 | Gmaj7 Bb7 | Ebmaj7 | Am7 D7  |
Gmaj7 Bb7| Ebmaj7 F#7| Bmaj7  | Fm7 Bb7 |
Ebmaj7   | Am7 D7    | Gmaj7  | C#m7 F#7|
Bmaj7    | Fm7 Bb7   | Ebmaj7 | C#m7 F#7|
```

The three key centers are **B, G, and Eb** — each a major third from the last. Every arrival at a new key is preceded by its V7 (and sometimes ii-V).

The harmonic rhythm is blistering: two chords per measure at a fast tempo, with key centers changing every one or two beats. This is why "Giant Steps" was considered almost unplayable when first recorded — the sidemen had to navigate three keys in the space where one would normally suffice.

### Countdown as Reharmonized Tune Up

**"Countdown"** demonstrates how Coltrane Changes work as a reharmonization technique. The original tune is "Tune Up" by Miles Davis:

```
Tune Up:   Em7  | A7   | Dmaj7 | Dmaj7 |
Countdown: Em7  | F7 Bbmaj7 | Db7 Gbmaj7 | A7 Dmaj7 |
```

Coltrane replaces the simple ii-V-I with a chain of V-I's descending by major thirds:

- From the target (Dmaj7), he backs up through the major-third cycle: Dmaj7 ← Gbmaj7 ← Bbmaj7
- Each key center is preceded by its V7: A7→D, Db7→Gb, F7→Bb
- The result: three ii-V-I resolutions compressed into four bars

### The Geometry

The Coltrane cycle is a **triangle inscribed in the circle of fifths** — three points equidistant on the twelve-tone clock face. Where traditional jazz harmony moves around the circle by fifths (adjacent steps), Coltrane leaps across it by major thirds (every four steps).

```
       C
   F       G
 Bb           D
  Eb         A
    Ab     E
       B(Db)

Triangle 1: C - E - Ab
Triangle 2: D - F# - Bb
Triangle 3: Eb - G - B  ← Giant Steps triangle
Triangle 4: F - A - Db
```

There are only four distinct major-third triangles. Each divides the twelve tones into three groups of four.

### Applying Coltrane Changes to Any ii-V-I

To reharmonize a ii-V-I using the Coltrane cycle:

1. Identify the target key (the I chord)
2. Find the two other keys a major third away
3. Insert V7→I for each key center, starting from the furthest and working back

**Example — reharmonize Dm7-G7-Cmaj7:**

```
Original:  Dm7     | G7      | Cmaj7   |
Coltrane:  Dm7 Eb7 | Abmaj7 B7 | Emaj7 G7 | Cmaj7 |
```

Or more compactly:

```
Dm7 | Eb7 Abmaj7 | B7 Emaj7 | Cmaj7 |
```

### Practice Exercise

1. Write out the three major-third key centers for a ii-V-I in **F major** (target: Fmaj7).
2. Reharmonize `Gm7 | C7 | Fmaj7` using the Coltrane cycle, inserting V7→I pairs for each key center.
3. Play through your reharmonization slowly on guitar, using shell voicings. Focus on the bass motion — it should move in a pattern of descending major thirds connected by ascending half steps (the V7 roots).

---

## Standards Reference Table

The following jazz standards are referenced throughout this course as study material:

| Standard | Composer | Key Concepts | Why Study It |
|----------|----------|-------------|--------------|
| **Autumn Leaves** | Kosma/Mercer | ii-V-I in major and relative minor | The perfect first jazz tune — two ii-V-Is in related keys |
| **All The Things You Are** | Kern/Hammerstein | Chained ii-V-Is through four key centers | The most harmonically rich standard in the repertoire |
| **Rhythm Changes** | Gershwin (I Got Rhythm) | Turnarounds, bridge dominants, substitution playground | The second most common jazz form after blues |
| **Stella by Starlight** | Young | ii-V chains, modal mixture, deceptive resolution | Tests your ability to track rapidly shifting key centers |
| **Giant Steps** | Coltrane | Major-third symmetric division, Coltrane Changes | The ultimate harmonic obstacle course |
| **So What** | Davis | Modal jazz, quartal voicings, Dorian vamp | The birth of modal jazz — two chords, infinite possibilities |

These tunes form a core vocabulary. A jazz guitarist who can voice lead, comp, and solo through all six of these has covered the essential harmonic landscape of the tradition.

---

## Key Terms

| Term | Definition |
|------|-----------|
| **ii-V-I** | The fundamental jazz chord progression: supertonic seventh, dominant seventh, tonic — built on descending-fifth root motion |
| **Shell voicing** | A minimal voicing containing only root, 3rd, and 7th of a chord |
| **Drop-2 voicing** | A close-position voicing rearranged by dropping the second-highest note down an octave |
| **Guide tones** | The 3rd and 7th of a chord — the tones that define its quality and drive voice leading |
| **Tritone substitution** | Replacing a dominant 7th with another dominant 7th whose root is a tritone away (shared guide tones) |
| **Backdoor dominant** | Resolution to the tonic from bVII7 instead of V7 |
| **Chord-scale theory** | The practice of assigning a parent scale to each chord quality for improvisation |
| **Avoid note** | A scale degree that creates a minor 9th against a chord tone when sustained |
| **Melodic minor** | The jazz minor "mother scale" (1 2 b3 4 5 6 7) whose modes generate altered and extended dominant scales |
| **Quartal voicing** | A chord built by stacking perfect fourths rather than thirds |
| **Upper-structure triad** | A major or minor triad superimposed over a dominant 7th to create extensions |
| **Coltrane Changes** | A reharmonization technique dividing the octave into three key centers a major third apart |
| **Voice leading** | The art of connecting chords through minimal melodic motion in each voice |
| **Extensions** | Chord tones beyond the 7th: 9th, 11th, 13th |
| **Alterations** | Chromatically raised or lowered extensions: b9, #9, #11, b13 |

---

## Self-Check Assessment

**1. Spell out the notes of a Dm7b5 chord and name the scale most commonly associated with it.**
> D F Ab C. The scale is Locrian (D Eb F G Ab Bb C) or Locrian #2 (D E F G Ab Bb C, the 6th mode of melodic minor).

**2. In a ii-V-I in Bb major, what are the three chords? Show how the guide tones of the ii chord connect to those of the V chord.**
> Cm7 - F7 - Bbmaj7. The 7th of Cm7 (Bb) descends to the 3rd of F7 (A). The 3rd of Cm7 (Eb) becomes the 7th of F7 (Eb). Guide tones exchange roles.

**3. What is the tritone substitute for G7, and why does the substitution work?**
> Db7. It works because G7 and Db7 share the same guide tones: B/Cb and F, with their roles as 3rd and 7th swapped. Both resolve to Cmaj7 with the same voice-leading motion.

**4. Name the three key centers in Giant Steps and the geometric relationship between them.**
> B, G, and Eb. They are equidistant on the chromatic circle, each a major third apart, forming an equilateral triangle on the circle of fifths.

**5. Build a quartal voicing starting on A using stacked perfect fourths (four notes). What familiar chord does this voicing resemble?**
> A - D - G - C. This is an Am7(11) or equivalently a C/A voicing. The quartal stack contains the notes of Am7 (A C G) plus D (the 11th), but without the tertian ordering.

**Pass criteria:** Identify all ii-V-I progressions in an unfamiliar lead sheet, voice lead through them using at least two voicing types, apply one substitution technique, and explain the voice-leading rationale for each chord connection.

---

## Research Basis

- The ii-V-I as the foundational jazz progression is documented across all major jazz pedagogy texts and is the most statistically common progression in the Great American Songbook
- Chord-scale theory originates primarily from the Berklee/NEC pedagogical tradition formalized by George Russell (Lydian Chromatic Concept, 1953) and systematized by Jamey Aebersold, Jerry Coker, and Mark Levine
- Coltrane Changes analysis draws from Lewis Porter's biography and Demsey's 1991 dissertation on Coltrane's symmetric harmony
- Guide-tone voice leading and Barry Harris's harmonic pedagogy represent the orally transmitted tradition of bebop harmony
- Drop-2 and drop-3 voicing systems codified by Ted Greene, Mick Goodrick, and the Berklee guitar department
- Sources: Levine, *The Jazz Theory Book* (1995); Goodrick, *The Advancing Guitarist* and *Almanac of Guitar Voice Leading* (1987/2011); Aebersold Play-Along series; Porter, *John Coltrane: His Life and Music* (1998)
- Belief state: T(0.80) F(0.05) U(0.10) C(0.05)
