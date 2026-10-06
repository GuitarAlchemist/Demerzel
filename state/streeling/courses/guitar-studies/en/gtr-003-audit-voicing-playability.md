---
module_id: gtr-003-audit-voicing-playability
department: guitar-studies
course: Audit a Voicing Playability Claim
level: intermediate
prerequisites: ["gtr-001-the-fretboard-map", "gtr-002-caged-geometry", "gaa-004-choose-a-useful-voicing"]
estimated_duration: "45 minutes"
produced_by: codex-project-pilot
research_cycle: guitar-studies-2026-10-05-003
version: "0.1.0"
---

# Audit a Voicing Playability Claim

> **Department of Guitar Studies** | Intermediate | 45 minutes | Draft: musician, subject, and localization review pending

## Objectives

You will compute a simple stretch measure, distinguish GA's two barre
predicates, find a counterexample to a universal comfort claim, and design a
small playing test that adds the missing human evidence.

## 1. A number is only as good as its definition

Use the three C-major [teaching shapes](../../../fixtures/guitar-studies/gtr-003/voicing-comparison.json)
from GAA-004: open `x 3 2 0 1 0`, A-form `x 3 5 5 5 3`, and E-form
`8 10 10 9 8 8`. They are hand-checked examples, not recorded GA output.
Each has **positive-fret span 2**: ignore muted `-1` and open `0` strings,
then subtract the smallest positive fret from the largest. That makes the
three forms equal under one measure, although they occupy different parts of
the neck and ask different things of the hand.

At [GA commit `dc2e74c`](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/Apps/ga-server/GaApi/Services/VoicingComfortService.cs),
`VoicingComfortService.ComputeStretch` uses this positive-fret-number span and
sorts candidates by it. This is a useful geometric indicator, not a measure
of millimeters, hand size, required pressure, or pain. The separate
[`VoicingPhysicalAnalyzer`](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/Common/GA.Domain.Services/Fretboard/Voicings/Analysis/VoicingPhysicalAnalyzer.cs)
uses physical fret distance as one input to its difficulty score. Therefore
comfort order and difficulty order can differ.

### Practice exercise 1

Compute the positive-fret span of the A-form and E-form C. Does equal span
prove equal stretch in millimeters or equal effort?

> **Answer:** A-form: `5 - 3 = 2`; E-form: `10 - 8 = 2`. Equal fret-number
> spans do not prove equal physical distances, and neither value measures the
> finger arrangement or the player's effort.

## 2. Read both barre rules

The analyzer's `BarreRequired` heuristic looks for **three adjacent strings
at the same positive fret**. In the A-form C, strings 4, 3, and 2 are all at
fret 5, so this heuristic is true. In the E-form C, fret 8 occurs on strings
6, 2, and 1, but never on three adjacent strings, so the heuristic is false.
That says what a pattern detector sees, not which fingering a guitarist must
use.

The comfort service applies a different `IsFullBarre` predicate when
`excludeFullBarre` is true: at least four fretted strings must share the
lowest positive fret. The A-form's lowest fret 3 occurs twice; the E-form's
lowest fret 8 occurs three times. Neither teaching shape meets that predicate.
An E-form major chord is commonly fingered with a full barre, so this is a
counterexample to interpreting `excludeFullBarre` as “all barre fingerings
removed.” Both predicates are documented in the [fixture record](../../../fixtures/guitar-studies/gtr-003/README.md).

### Practice exercise 2

For each of the A-form and E-form C, predict `BarreRequired` and whether
`excludeFullBarre: true` would reject it **if GA returned that exact fret
array**. Why must you include the condition in your answer?

> **Answer:** A-form: `BarreRequired = true`; comfort's full-barre predicate
> is false. E-form: `BarreRequired = false`; comfort's full-barre predicate is
> also false. Both would remain under this filter. The condition matters
> because this fixture does not prove GA's generator returns either array.

## 3. Audit a model claim against a guitarist

GA's difficulty score combines physical fret distance, a barre heuristic,
the presence of open strings, and the count of distinct fretted positions;
it caps the result at 10. Its labels are computed from related thresholds.
These fields can help screen candidates, but the inspected code does not
measure a player's reach, hand condition, pain, technique, instrument setup,
or how clearly the notes sound. Even “Beginner” is a model category, not a
medical or pedagogical guarantee.

Try each shape slowly if you have a guitar. Pluck the intended strings one
at a time, then strum. Record `clean notes / attempted notes`, how you
fingered the shape, whether you could release and return to it, and any
discomfort. Stop if it hurts. A partner with a different hand or experience
level may obtain a different result. A single player trial can challenge a
universal claim but cannot establish population-wide playability.

### Practice exercise 3

The service reports a low score for one shape, but your third string buzzes
and you cannot switch to it on the beat. What can you conclude?

> **Answer:** The score was a computed indicator for this candidate. In this
> trial it did not predict clean execution or the required transition for
> this player and tempo. Record the context and try another shape; do not
> rewrite the model's result as a universal judgment.

## 4. Make the improvement loop testable

If an agent proposes a new playability weight, first pin a GA revision and a
small corpus of chord queries. Keep the same tuning and filter settings,
record the old and new rank orders, and ask guitarists to test a sample of
shapes in a stated musical task. Check both improvements and regressions:
did more top-ranked shapes play cleanly, and did the change hide useful
alternatives? A higher correlation on one player is not a reason to call the
model solved. The review should preserve the trial records and counterexamples.

### Practice exercise 4

An agent proposes to merge `BarreRequired` and `IsFullBarre` into one Boolean.
What evidence is missing before that change?

> **Answer:** Define which question the Boolean must answer, then test both
> heuristics against actual fingerings, player observations, and existing
> service contracts. The A-form and E-form counterexamples show that the
> predicates already disagree; replacing them without measuring callers
> could change filters and hide useful voicings.

## Key takeaways

- A fret-number span, a physical-distance score, and a player's experience
  answer different questions.
- GA's two barre predicates are not interchangeable; name the predicate when
  explaining a result.
- A computed playability indicator is a proposal to test with a guitarist in
  context, not proof of universal comfort.

## Evidence and limits

The [fixture record](../../../fixtures/guitar-studies/gtr-003/README.md)
pins GA source and focused tests. The test run used an existing binary; no
fresh GA build, live generator capture for these three shapes, or musician
trial has yet validated this lesson. Subject and localization review are also
pending. Keep the course in draft status until those observations exist.
