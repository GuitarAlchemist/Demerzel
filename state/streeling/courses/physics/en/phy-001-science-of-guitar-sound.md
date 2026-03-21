---
module_id: phy-001-science-of-guitar-sound
department: physics
course: Acoustics and Wave Physics
level: beginner
alchemical_stage: nigredo
prerequisites: []
estimated_duration: "25 minutes"
produced_by: physics
version: "1.0.0"
---

# The Science of Guitar Sound

> **Department of Physics** | Stage: Nigredo (Beginner) | Duration: 25 minutes

## Objectives

After this lesson, you will be able to:
- Explain how a guitar string vibrates to produce sound (standing waves)
- Describe the harmonic series and why it gives each instrument its unique timbre
- Understand how the guitar body amplifies sound through resonance
- Connect fret placement to frequency ratios using basic physics

---

## 1. String Vibration — Standing Waves

When you pluck a guitar string, it does not just wobble randomly. It vibrates in a very specific pattern called a **standing wave**.

A standing wave occurs when a wave bounces back and forth between two fixed endpoints — in this case, the nut and the saddle (or a fret and the saddle). The reflected waves interfere with each other, and only certain vibration patterns survive. These surviving patterns are the ones where the string length is an exact number of half-wavelengths.

**The fundamental frequency** is the simplest pattern: the entire string swings back and forth as one arc, with maximum displacement in the middle and zero displacement at the endpoints (called **nodes**).

The fundamental frequency depends on three things:

```
f = (1 / 2L) * sqrt(T / mu)
```

Where:
- **L** = vibrating length of the string
- **T** = tension (how tightly the string is pulled)
- **mu** = linear mass density (mass per unit length — thicker strings have more)

This formula explains everything about guitar string behavior:
- **Shorter string** (pressing a fret) → higher pitch
- **Tighter string** (tuning up) → higher pitch
- **Thicker string** (low E vs high E) → lower pitch

### Practice Exercise

Try this on your guitar: pluck an open string, then press the same string at the 12th fret and pluck again. The 12th fret halves the string length (L becomes L/2), which doubles the frequency — you hear exactly one octave higher. Now compare the open low E string (thick) to the open high E string (thin). Same note name, two octaves apart — the difference is the mass density (mu).

---

## 2. The Harmonic Series — Why a Guitar Sounds Like a Guitar

When you pluck a string, it does not just vibrate at the fundamental frequency. It simultaneously vibrates at **all integer multiples** of the fundamental. These are the **harmonics** (also called **overtones** or **partials**).

| Harmonic | Frequency | Musical Interval | Nodes on String |
|----------|-----------|-----------------|-----------------|
| 1st (fundamental) | f | Root | 2 (endpoints only) |
| 2nd | 2f | Octave | 3 |
| 3rd | 3f | Octave + perfect 5th | 4 |
| 4th | 4f | Two octaves | 5 |
| 5th | 5f | Two octaves + major 3rd | 6 |
| 6th | 6f | Two octaves + perfect 5th | 7 |

The sound you hear is **all of these frequencies combined**. Your ear perceives the fundamental as "the pitch," but the relative loudness of each harmonic shapes the **timbre** — the tonal color that makes a guitar sound different from a piano, even when they play the same note.

This is why a guitar sounds like a guitar: its string material, body shape, and pick position create a specific harmonic recipe. Pluck near the bridge and you emphasize higher harmonics (bright, twangy). Pluck near the neck and you suppress them (warm, mellow).

### Practice Exercise

You can isolate individual harmonics on guitar. Lightly touch the string directly over the 12th fret (do not press down — just touch) and pluck. You will hear the 2nd harmonic: a clear, bell-like tone one octave above the open string. Try the same at the 7th fret (3rd harmonic — an octave plus a fifth above) and the 5th fret (4th harmonic — two octaves above). You are forcing the string to vibrate in specific patterns by creating a node at your fingertip.

---

## 3. Resonance — How the Body Amplifies Sound

A vibrating string alone is nearly silent. Hold an electric guitar unplugged and strum — you can barely hear it across a room. The string needs help to push enough air to reach your ears.

That help comes from **resonance**. When you pluck a string on an acoustic guitar:

1. The string vibrates at its fundamental and harmonics
2. The vibration travels through the saddle into the **bridge**
3. The bridge is glued to the **top (soundboard)** of the guitar body
4. The soundboard is a large, thin, flexible surface that vibrates sympathetically — it is the speaker cone of the acoustic guitar
5. The vibrating soundboard pushes air inside the body cavity, which resonates through the **sound hole**

The body acts as a **resonant cavity**. It has its own natural frequencies determined by its shape, size, and material. When the string's frequencies align with the body's resonant frequencies, those frequencies are amplified more strongly.

This is why different guitars sound different even with the same strings. A dreadnought body (large, wide) emphasizes lower frequencies. A parlor guitar (small body) sounds brighter. The wood species, bracing pattern, and body depth all tune the resonance profile.

**Key concept:** Resonance is not "making it louder across the board." It is **selective amplification** — certain frequencies are boosted more than others, which shapes the guitar's unique voice.

### Practice Exercise

If you have an acoustic guitar, try this: press your ear against the back of the body while someone else plucks a single string. You will feel the entire body vibrating. Now tap the soundboard gently in different spots — you will hear different pitches. These are the body's own resonant frequencies. Every guitar is a collaboration between string and body.

---

## 4. Frets and Frequency Ratios

Here is where physics meets music theory most directly. The frets on a guitar are not placed at equal distances — they get closer together as you move toward the body. Why?

Each fret raises the pitch by one semitone. In **equal temperament** (the standard tuning system), each semitone multiplies the frequency by the same ratio:

```
r = 2^(1/12) ≈ 1.05946
```

This means each fret shortens the vibrating string by a factor of *r*. Since frets are placed based on a geometric (not arithmetic) progression, the spacing decreases as you go higher.

Some musically important fret positions and their frequency ratios:

| Fret | Frequency Ratio | Musical Interval | String Length Fraction |
|------|----------------|-----------------|----------------------|
| 0 (open) | 1:1 | Unison | 1 |
| 5 | 2^(5/12) ≈ 1.335 | Perfect 4th | ~3/4 |
| 7 | 2^(7/12) ≈ 1.498 | Perfect 5th | ~2/3 |
| 12 | 2^(12/12) = 2 | Octave | 1/2 |

Notice the perfect fifth at fret 7: the frequency ratio is very close to 3/2 (1.5). The perfect fourth at fret 5 is close to 4/3 (1.333). These simple ratios are why these intervals sound consonant — the same physics that governs the harmonic series governs the intervals we find pleasing.

Equal temperament slightly adjusts these ratios to make all keys sound equally good — a compromise. In pure (just) intonation, a perfect fifth would be exactly 3/2, but then some keys would sound terrible. The guitar's fixed frets commit it to equal temperament.

### Practice Exercise

Measure the distance from the nut to the 12th fret on your guitar, then measure from the 12th fret to the saddle. They should be almost exactly equal — confirming that the 12th fret halves the string length, doubling the frequency (one octave). Now measure nut to fret 7: it should be roughly 2/3 of the total string length, matching the 3:2 ratio of a perfect fifth.

---

## 5. Putting It All Together

Every sound you hear from a guitar is the result of these four physics concepts working together:

1. **Standing waves** determine which frequencies the string can produce
2. **The harmonic series** shapes the timbre by blending multiple simultaneous frequencies
3. **Resonance** in the body selectively amplifies those frequencies to audible volume
4. **Frequency ratios** from equal temperament determine the musical intervals between fretted notes

When you play a chord, each string produces its own fundamental and harmonics. The body resonates with all of them simultaneously. Your ear receives a complex wave containing dozens of frequencies and somehow perceives it as "a C major chord." The physics is extraordinary. The fact that humans perceive it as music is even more so.

---

## Key Terms

| Term | Definition |
|------|-----------|
| **Standing wave** | A vibration pattern that remains stationary, with fixed nodes and antinodes |
| **Fundamental frequency** | The lowest frequency at which a string vibrates — perceived as the pitch |
| **Harmonic (overtone)** | An integer multiple of the fundamental frequency |
| **Timbre** | The tonal quality that distinguishes one instrument from another playing the same note |
| **Node** | A point on a standing wave that remains stationary (zero displacement) |
| **Resonance** | The amplification of sound when a vibrating object drives another object at its natural frequency |
| **Equal temperament** | Tuning system where each semitone has an equal frequency ratio of 2^(1/12) |

---

## Self-Check Assessment

**1. What three physical properties of a string determine its fundamental frequency?**
> Length (L), tension (T), and linear mass density (mu). The formula is f = (1/2L) * sqrt(T/mu).

**2. Why does a guitar sound different from a piano playing the same note at the same volume?**
> They have different harmonic profiles — the relative loudness of each overtone differs, producing a different timbre. The guitar body, string material, and plucking method create a unique harmonic recipe.

**3. What happens when you lightly touch a string at the 12th fret and pluck?**
> You create a node at the midpoint, forcing the string to vibrate in its 2nd harmonic. The fundamental is suppressed and you hear a pure tone one octave higher.

**4. Why do frets get closer together as you move up the neck?**
> Fret spacing follows a geometric progression (each fret multiplies frequency by 2^(1/12)). Since each fret removes a constant fraction of the remaining string length rather than a constant distance, the spacing decreases.

**Pass criteria:** Explain how standing waves produce guitar sound, identify at least three harmonics in the series, and connect fret position to frequency ratio.

---

## Research Basis

- String vibration follows the wave equation; standing waves are its boundary-value solutions
- The harmonic series is a direct consequence of the physics of vibrating strings
- Guitar body resonance has been extensively studied via modal analysis
- Equal temperament uses 2^(1/12) spacing, a mathematical compromise formalized in the 16th-18th centuries
- Sources: Acoustics and wave physics consensus, Streeling Department of Physics curriculum
- Belief state: T(0.93) F(0.01) U(0.04) C(0.02)
