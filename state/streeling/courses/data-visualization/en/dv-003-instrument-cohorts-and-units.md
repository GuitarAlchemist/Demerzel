---
module_id: dv-003-instrument-cohorts-and-units
department: data-visualization
course: Compare Instrument Cohorts Without Hiding Their Sizes
level: beginner
prerequisites: [dv-002-denominators-and-test-populations]
estimated_duration: "30 minutes"
produced_by: codex-project-pilot
research_cycle: data-visualization-2026-10-11-003
version: "0.1.0"
---

# Compare Instrument Cohorts Without Hiding Their Sizes

> **Department of Data Visualization** | Level: Beginner | Estimated duration: 30 minutes | Status: review and localization pending

## Objectives

After this lesson, you will be able to:

- Report guitar, bass, and ukulele corpus sizes without hiding the smaller groups.
- Identify whether a metric counts voicings, pitch-class sets, or one representative per instrument.
- Explain the scope of GA's cross-instrument consistency result without turning it into a per-instrument quality claim.
- Design a comparison that distinguishes observed results from measurements GA has not recorded.

## The project question

The [GA voicing analysis snapshot from July 23, 2026](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/state/quality/voicing-analysis/2026-07-23.json), pinned to commit [`dc2e74c`](https://github.com/GuitarAlchemist/ga/tree/dc2e74cbd992a298f67efb928b5b3754615e1924), reports a corpus of 313,047 voicings and a 100% cross-instrument consistency metric. A dashboard reader asks, “Does this prove equally good chord naming on guitar, bass, and ukulele?” The answer depends on what each number counts.

| Corpus cohort | Voicings | Share of all voicings |
|---|---:|---:|
| Guitar | 297,910 | 95.16% |
| Bass | 7,795 | 2.49% |
| Ukulele | 7,342 | 2.35% |
| **Total** | **313,047** | **100.00%** |

These are historical audit counts, not a live catalog or a user population. The proportions are calculated from the snapshot's `Corpus` fields and rounded to two decimals.

### Practice exercise

Check the total and write a chart caption that makes the imbalance visible.

> **Answer:** `297,910 + 7,795 + 7,342 = 313,047`. A defensible caption is “Historical GA voicing audit: 313,047 generated voicings; guitar contributes 95.16%, bass 2.49%, and ukulele 2.35%.”

## 1. A cohort count is not an error rate

A cohort is the group being compared. Here the `Corpus` section counts voicings by instrument. A bar chart can compare those **sizes**. It cannot compare per-instrument musical naming accuracy because the snapshot has no independently judged correct-name label for each voicing. The same file reports global `UnknownChordName.Count: 0` and `NullChordName.Count: 0`. Since the three instrument counts partition this audited corpus, zero overall implies zero null or unknown names in each cohort for this run. It does not establish that every non-null name is musically correct.

If the chart uses a percentage axis, say whether it is a share of all voicings or a within-instrument rate. “Bass: 2.49%” is a corpus share; “bass naming error rate: 2.49%” would be an invented claim. A small cohort also needs its raw count beside any future rate. A single error among 7,342 ukulele voicings would move its rate more than a single error among 297,910 guitar voicings.

### Practice exercise

A dashboard labels three bars “Guitar quality 95.16%, bass quality 2.49%, ukulele quality 2.35%.” What is wrong, and what can the bars legitimately show?

> **Answer:** The numbers are shares of the audited corpus, not quality scores. Relabel the bars “share of voicings” and show 297,910, 7,795, and 7,342. The audit supports zero null or unknown names in each cohort, but a broader correctness claim needs independently judged labels.

## 2. The consistency metric counts shared sets

The same snapshot reports `CrossInstrumentConsistency.SharedSets: 793` and `Consistent: 793`. Its 100% value is `793 / 793` **shared pitch-class sets**, not `313,047 / 313,047` voicings. In the [pinned audit implementation](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/Demos/VoicingAnalysisAudit/Program.cs), the audit keeps the first seen canonical chord name per instrument for a pitch-class mask, selects masks seen on at least two instruments, and checks whether those retained names agree. The code uses the canonical name where available because a voicing-specific slash bass may legitimately differ across instruments.

That is a useful **cross-instrument naming consistency check for retained representatives**. It is narrower than “every voicing was named correctly” or “all three instruments have equal error rates.” A chart must not put the 793-set numerator on the 313,047-voicing denominator. Also, the file does not break the 793 sets into guitar–bass, guitar–ukulele, bass–ukulele, or all-three groups, so pairwise rates cannot be read from it.

### Practice exercise

Assess the headline “100% of 313,047 voicings agree across all three instruments.” Replace it with a supported statement.

> **Answer:** The headline changes the unit and implies all three instruments participate in every comparison. A supported statement is “The audit found matching retained canonical names for all 793 pitch-class sets observed on at least two instruments.” Add that it uses the first seen name per instrument and does not measure all voicings pairwise.

## 3. Give the reader two views and two denominators

Use one display for the corpus composition: a horizontal bar for each instrument, with exact voicing counts and shares. Use another display for the consistency test: “793 / 793 shared pitch-class sets consistent (100%).” Place the method note next to the second result, not in a hidden tooltip. A table is an accessible alternative to both charts.

Avoid a single green “100% quality” badge. It would blend a set-level agreement check with per-voicing completeness metrics and could conceal the 38-to-1 guitar-to-bass corpus size difference. The two views answer different questions: “What did the audit include?” and “What did this particular agreement check find?” Neither says how easy a voicing is to play or whether a guitarist likes its sound.

### Practice exercise

Write a two-line text alternative for these displays. Include both denominators and one limitation.

> **Answer:** “The historical audit contains 297,910 guitar, 7,795 bass, and 7,342 ukulele voicings. Retained names agree for 793 of 793 pitch-class sets seen on at least two instruments; the snapshot does not measure independently reviewed musical naming correctness by instrument.”

## 4. Design the next useful measurement

To compare **musical naming correctness** fairly by instrument, a future evaluation would record `instrument`, `voicing_id`, `pitch_class_mask`, `canonical_name`, an independently reviewed reference label, a match verdict, and the audit/corpus revision for each evaluated result. Then divide each instrument's mismatches by its own number of **reviewed** voicings, not by all generated voicings unless all were reviewed. Report uncertainty or at least exact counts for small cohorts. For matched cross-instrument comparisons, retain every relevant observation rather than only the first name for each mask and instrument; define in advance whether the unit is a voicing, a set, or an instrument pair.

This is a proposed measurement contract, not a claim that GA already emits those reviewed labels. Keep it separate from the historical snapshot. The global zero null/unknown counts are useful and do apply to each cohort in this exhaustive partition; they still do not test whether a non-null name is correct or whether a voicing is playable, useful, or pleasant to hear.

### Practice exercise

Propose one field and one denominator needed for a bass-specific **musical naming mismatch** rate. State one question that rate still would not answer.

> **Answer:** Record a reviewed reference name and match verdict for each evaluated bass voicing; divide mismatches by the number of **reviewed bass voicings**. The historical corpus has 7,795 bass voicings, but that is the denominator only if all 7,795 receive a review. The mismatch rate would not determine whether bassists consider the shapes playable or useful.

## Key takeaways

- Show instrument cohort sizes before comparing outcomes.
- Name the unit of analysis beside every numerator and denominator.
- `793 / 793` shared sets is not a per-voicing or per-instrument accuracy rate.
- The audit retains one canonical name per instrument and pitch-class mask for this consistency check.
- Keep inferred zero null/unknown counts separate from unmeasured musical naming correctness.

## Further reading and project evidence

- GA [historical voicing-analysis snapshot](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/state/quality/voicing-analysis/2026-07-23.json) and [pinned audit implementation](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/Demos/VoicingAnalysisAudit/Program.cs).
- [DV-002](dv-002-denominators-and-test-populations.md) for weighted aggregation and cohort changes.

*Research: `data-visualization-2026-10-11-003`. Subject review, learner exercise, localization, and public verification are pending.*
