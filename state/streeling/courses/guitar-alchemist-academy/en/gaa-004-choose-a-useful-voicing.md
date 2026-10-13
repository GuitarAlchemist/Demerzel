---
module_id: gaa-004-choose-a-useful-voicing
department: guitar-alchemist-academy
course: Choose and Play a Useful Voicing from a GA Answer
level: beginner
alchemical_stage: nigredo
prerequisites: ["gaa-001-your-first-chord", "gtr-001-the-fretboard-map"]
estimated_duration: "35 minutes"
produced_by: codex-project-pilot
research_cycle: guitar-alchemist-academy-2026-10-05-004
version: "0.1.0"
---

# Choose and Play a Useful Voicing from a GA Answer

> **Guitar Alchemist Academy** | Beginner | 35 minutes | Draft: musician, subject, and localization review pending

## Objectives

You will read a fret pattern without sounding a muted string, compare two
ways to play the same chord, use GA's difficulty order as a starting point,
and check the result with your fingers and ears before calling it useful.

## 1. Decode one shape before judging it

Ask for **C major**. The [fixed teaching fixture](../../../fixtures/guitar-studies/gtr-003/README.md)
contains three C-major shapes. These were checked by note name; they are **not
captured GA results**. The diagrams here read from string 6 (low E) to string
1 (high E). `x` means do not sound the string; `0` means let it ring open.

```text
String:        6  5  4  3  2  1
Open C:        x  3  2  0  1  0
A-form C:      x  3  5  5  5  3
E-form C:      8 10 10  9  8  8
```

For open C, sound only strings 5 through 1. Their notes are C, E, G, C,
E. The three *pitch classes* C, E, and G define C major; repeating C or E
in another octave changes the voicing, not the chord's basic identity. Before
translating a GA `Frets` array into this diagram, check which end of the array
means the low E string. The fixture declares its own low-to-high order; it
does not establish the service's array order.

### Practice exercise 1

In `x 3 2 0 1 0`, which string must remain silent, which strings are open,
and what three note names make this C major?

> **Answer:** Mute string 6. Strings 3 and 1 are open. The sounding notes are
> C, E, G, C, E, so the distinct note names are C, E, and G.

## 2. Use GA's order as a proposal

At [GA commit `dc2e74c`](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/Apps/ga-server/GaApi/Services/VoicingFilterService.cs),
`GetVoicingsForChordAsync("C")` generates candidates with fret arrays,
difficulty labels and scores, and barre information, then orders the results
by ascending `DifficultyScore`. The [service tests](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/Tests/Apps/GaApi.Tests/Services/VoicingFilterServiceTests.cs)
check that C returns candidates and that their scores are sorted. They do not
promise that the first shape is comfortable for every guitarist, nor that it
matches one of the three teaching shapes above.

Take the first two results from a GA `C` query in a build of that revision.
Write down each fret array, score, whether it uses open strings, and any barre
label. If the available interface omits a field, mark it *not shown*; do not
invent it from the drawing. Translate `-1` as mute and `0` as open. Keep the
query, revision, and instrument tuning with your notes so another learner can
repeat the comparison.

If GA is not running, compare the fixed shapes instead and mark the service
query *not run*. The scores 3 and 5 in the next exercise are hypothetical;
do not attach them to the fixed shapes or claim a GA result.

### Practice exercise 2

If you set `noOpenStrings: true`, may you still expect the open-C teaching
shape to appear? If two GA results have scores 3 and 5, which should you try
first and what does that score **not** establish?

> **Answer:** No: the service filters candidates containing fret `0` when
> `noOpenStrings` is true. Try the score-3 result first as a sensible proposal.
> The score does not measure your hand size, technique, pain, or how the chord
> sounds through your instrument.

## 3. Check the choice on a guitar

Start with open C from the fixture. Place one finger at string 5 fret 3,
one at string 4 fret 2, and one at string 2 fret 1. Pluck strings 5, 4, 3,
2, and 1 separately. If a note buzzes, adjust your finger near the fret
without pressing harder than needed. Then strum only those five strings.
Do not force a stretch or continue through pain.

Next try the A-form C: mute string 6; fret strings 5 and 1 at fret 3 and
strings 4, 3, and 2 at fret 5. You may need a partial barre or a different
fingering. Compare how cleanly the notes ring and how much effort the shape
requires. If this is too hard today, record that observation and stay with
open C. A different voicing is useful only when it fits the music and the
player, not merely because an algorithm returns it.

### Practice exercise 3

Both teaching shapes contain C, E, and G. Record one musical reason and one
physical reason you might choose open C for a slow song. What would make you
choose the A-form instead?

> **Example answer:** Open C lets its open strings ring and is easier for my
> current hand. I might choose the A-form when I need a compact position near
> fret 3 for the next chord, after I can sound every intended note cleanly.
> Another player's tested choice may differ.

## 4. Make a claim that the evidence supports

Separate what the service **computed** from what you **observed**. A compact
practice record is: `C query + GA revision → two returned patterns and scores
→ one played pattern → clean/buzzing notes → effort and musical context →
choice`. The program proposes; the player checks. If you did not run GA or
play a shape, say which step remains untested.

### Practice exercise 4

An agent writes, “GA's first C result is the easiest C chord for everyone.”
Rewrite that statement using only the evidence available from the service.

> **Answer:** “In this GA query, the first result has the lowest computed
> difficulty score among the returned candidates. A guitarist still needs to
> check its tuning, sounding notes, fingering, and comfort.”

## Key takeaways

- A fret array is an instruction for particular strings; `-1` and `0` have
  different meanings.
- Several voicings can contain the same chord notes yet feel and sound
  different.
- GA's ranking is a useful first suggestion. A player makes the final choice
  after playing and listening.

## Evidence and limits

The [fixture and test record](../../../fixtures/guitar-studies/gtr-003/README.md)
pin the inspected GA source and distinguish teaching shapes from service
output. The focused prebuilt GA tests passed, but this lesson has no captured
live GA response, novice play-through, or musician review. Those checks and
localization review are required before treating the draft as verified.
