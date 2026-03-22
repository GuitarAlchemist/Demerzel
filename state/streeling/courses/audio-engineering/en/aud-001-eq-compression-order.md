---
module_id: aud-001-eq-compression-order
department: audio-engineering
course: "Compression essentials — ratio, threshold, attack, release"
level: intermediate
prerequisites: []
estimated_duration: "35 minutes"
produced_by: seldon-research-cycle
research_cycle: audio-engineering-2026-03-23-001
version: "1.0.0"
---

# EQ and Compression Order: Why Signal Chain Matters

> **Department of Audio Engineering** | Level: Intermediate | Duration: 35 minutes

## Objectives
- Understand the technical differences between Comp→EQ and EQ→Comp signal chains
- Identify when each order produces better results on vocals
- Apply the EQ→Comp→EQ sandwich technique for maximum control
- Recognize frequency-dependent compression artifacts and how to prevent them

---

## 1. The Core Question

Does it matter whether you compress before or after EQ? **Yes** — measurably so. The order changes how the compressor reacts to frequency content, which affects the naturalness of the dynamics and the clarity of the tone.

The reason is simple: a compressor responds to *level*. If certain frequencies are louder (e.g., proximity effect boosting 100-200 Hz, or sibilance peaking at 4-10 kHz), the compressor reacts to *those frequencies*, not just the overall vocal performance.

---

## 2. Compression Before EQ (Comp→EQ)

```
Vocal → [Compressor] → [EQ] → Mix Bus
```

**What happens:**
- The compressor sees the raw signal — including problematic frequencies
- If sibilance is loud (4-10 kHz peaks), it may trigger compression on those transients
- The compressor "pumps" on problematic frequencies rather than controlling overall dynamics
- EQ afterward shapes the already-compressed signal

**When to use:**
- When the vocal is well-recorded with minimal frequency problems
- When you want the compressor to react to the full, natural signal
- When using gentle compression (2:1 ratio, slow attack) for "glue"

**Risk:** Frequency-dependent pumping. The compressor doesn't know you don't want it reacting to the 200 Hz proximity hump — it just sees level.

---

## 3. EQ Before Compression (EQ→Comp)

```
Vocal → [EQ] → [Compressor] → Mix Bus
```

**What happens:**
- Corrective EQ removes problems first: cut proximity at 200 Hz, tame sibilance at 6 kHz
- The compressor receives a cleaner, more balanced signal
- Compression responds to the *musical performance*, not frequency artifacts
- Result: more natural, transparent compression

**When to use:**
- When the vocal has noticeable frequency problems (proximity, room resonance, harshness)
- When you want the compressor to respond to dynamics, not frequency peaks
- When recording quality is variable

**This is generally the safer default** — fix the frequency problems before asking the compressor to manage dynamics.

---

## 4. The Sandwich: EQ→Comp→EQ

```
Vocal → [Corrective EQ] → [Compressor] → [Tonal EQ] → Mix Bus
```

This is the professional standard for a reason:

1. **First EQ (corrective):** High-pass filter at 80-100 Hz, cut mud at 200-300 Hz, notch room resonances. This is surgical — you're removing problems, not shaping tone.

2. **Compressor:** Now reacts to a clean signal. Set ratio (3:1-4:1 typical for vocals), threshold to catch ~6 dB of gain reduction, medium attack (10-30ms) to preserve transients, medium release (50-100ms).

3. **Second EQ (tonal):** Now shape the sound creatively. Boost air at 10-12 kHz, add presence at 3-5 kHz, warm up the low-mids. This EQ sits after compression, so your boosts won't trigger the compressor.

**Why it works:** Separation of concerns. The corrective EQ prevents compressor artifacts. The compressor manages dynamics on a clean signal. The tonal EQ shapes the final character without affecting dynamics.

---

## 5. Frequency-Dependent Artifacts to Watch For

| Problem | Cause | Fix |
|---------|-------|-----|
| Pumping on plosives | Low-frequency bursts triggering compressor | HPF before compressor (EQ→Comp) |
| Sibilance amplified | Compressor reduces body, sibilance stays | De-esser before compressor, or EQ cut at 6 kHz first |
| Dull after compression | Fast attack squashing transients | Slow attack (15-30ms), or parallel compression |
| Inconsistent tone | Compressor reacting differently to quiet vs loud sections | Use 2 stages of gentle compression instead of 1 heavy stage |

---

## 6. Dynamic EQ: The Modern Alternative

Dynamic EQ combines EQ and compression in one processor. Each EQ band only activates when the frequency exceeds a threshold — like a compressor that only works on specific frequencies.

**Use case:** Sibilance that varies throughout the performance. A static cut at 6 kHz would dull the entire vocal, but a dynamic EQ cut only activates when sibilance exceeds the threshold.

This doesn't replace the Comp→EQ question — it's a specialized tool for frequency-dependent dynamics problems.

---

## Practice Exercise

### Exercise 1: A/B the Order
Take a vocal recording. Set up two parallel chains:
- Chain A: Compressor (4:1, -6 dB GR) → EQ (boost 3 kHz +3 dB, cut 250 Hz -4 dB)
- Chain B: Same EQ → Same Compressor

Listen to both. Where do you hear the difference? Focus on:
- Low-frequency consistency (proximity effect handling)
- Sibilance level
- Overall "naturalness" of the compression

### Exercise 2: Build a Sandwich
Set up: HPF at 100 Hz + cut at 250 Hz → Compressor (3:1) → Presence boost at 4 kHz + Air at 12 kHz. Compare against a single-EQ-then-compress chain.

---

## Key Takeaways
- **Order matters** — the compressor responds to whatever frequencies are loudest in the input
- **EQ→Comp is the safer default** — fix problems before compression for more natural results
- **EQ→Comp→EQ sandwich is the professional standard** — corrective first, tonal last
- **There is no universally "correct" order** — it depends on the recording, genre, and intent
- **Dynamic EQ** is a modern tool for frequency-dependent dynamics problems
- The goal is always: control dynamics without destroying the natural character of the performance

## Further Reading
- Department of Physics: Acoustics — frequency, amplitude, and harmonic relationships
- Department of Music: How timbre perception affects mixing decisions
- Department of Computer Science: DSP algorithms behind EQ and compression
- AES (Audio Engineering Society): Standards for loudness measurement (ITU-R BS.1770)

---
*Produced by Seldon Research Cycle audio-engineering-2026-03-23-001 on 2026-03-23.*
*Research question: Does the order of compression before EQ versus EQ before compression produce measurably different results on vocals?*
*Belief: T (confidence: 0.80)*
