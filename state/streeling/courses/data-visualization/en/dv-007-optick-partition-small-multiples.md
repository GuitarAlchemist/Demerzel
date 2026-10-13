---
module_id: dv-007-optick-partition-small-multiples
department: data-visualization
course: Small Multiples for OPTIC-K Partition Diagnostics
level: intermediate
prerequisites: [dv-001-observed-degraded-stale-quality, dv-006-position-length-area-comparisons]
estimated_duration: "35 minutes"
produced_by: codex-project-pilot
research_cycle: data-visualization-2026-10-11-007
version: "0.1.0"
---

# Small Multiples for OPTIC-K Partition Diagnostics

> **Department of Data Visualization** | Level: Intermediate | Estimated duration: 35 minutes | Status: English draft; subject, learner, localization, and publication review pending

## Objectives

After this lesson, you will be able to:

- Decide when small multiples help compare the **same diagnostic measure** across OPTIC-K partitions.
- Keep scales, baseline, sample, and classifier fixed across panels while labeling each partition's role and dimension.
- Distinguish a diagnostic's compact-vector offsets from the schema's raw-vector offsets.
- Explain why instrument predictability does not test transposition invariance or musical retrieval quality.

## The project question

A GA engineer wants to inspect instrument information in the OPTIC-K embedding. At pinned GA revision [`dc2e74c`](https://github.com/GuitarAlchemist/ga/tree/dc2e74cbd992a298f67efb928b5b3754615e1924), the [June 25, 2026 embedding diagnostic](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/state/quality/embeddings/2026-06-25.json) records a classifier's instrument-prediction accuracy for six partitions. Should a dashboard show one ranked “partition quality” bar chart, six tiny charts, or a single overall score?

Choose **six aligned small multiples** for this narrow comparison: one panel per tested partition, each showing the same instrument-classification accuracy on a 0–100% scale, with the **33.33% balanced three-class chance baseline** repeated. The fixed diagnostic sampled 12,000 items, 4,000 per instrument, used five folds, and names a 30-tree random forest of maximum depth 10. Those method fields belong in the common caption. Each panel needs the partition name, dimension, schema role, observed mean, and the diagnostic's own hypothesis/status labels. A table should carry the exact values.

The [canonical `EmbeddingSchema.cs` registry](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/Common/GA.Business.ML/Embeddings/EmbeddingSchema.cs) declares `Version = OPTIC-K-v1.8` and `TotalDimension = 240`. Its similarity partitions include STRUCTURE, MORPHOLOGY, CONTEXT, SYMBOLIC, MODAL, and ROOT. That is why these six panels form a coherent set. This is a historical diagnostic of a fixed index, not today's embedding health.

### Practice exercise 1: choose the panel set

Why are six panels preferable to one “embedding quality” score here? Should IDENTITY, SPECTRAL, and HIERARCHY receive blank accuracy panels?

> **Answer:** All six tested similarity partitions have the same instrument-classification measure, so repeated panels permit a like-unit comparison while preserving each partition's different role. A single quality score would combine distinct interpretations. IDENTITY is a hard-filter role and SPECTRAL and HIERARCHY are informational roles in the canonical registry; the fixed diagnostic supplies no classifier rows for them. Do not invent zero-accuracy panels. List them separately as “not measured in this diagnostic” if the full schema must be shown.

## 1. Fix the ruler and show the numbers

Give all six panels the same 0–100% horizontal axis. Put a reference line at the recorded random baseline, **33.33%**, and a dot at each mean accuracy. Do not auto-scale one panel to 30–40% and another to 85–95%: that would make a small difference around chance appear as large as the difference between chance and 90%. Use a direct numeric label, not a color-only “leak” code. The recorded five fold values could appear as small secondary marks, but they are folds from one run, not five independent deployments or a confidence interval.

[DV-006](dv-006-position-length-area-comparisons.md) introduces the shared-scale comparison decision; here the repeated panels apply it to one diagnostic measure.

| Panel | Raw slots in schema | Role | Diagnostic mean | Diagnostic label |
|---|---:|---|---:|---|
| STRUCTURE | 6–29 (24 dims) | Similarity | 50.20% | `likely_leak`; confirmed |
| MORPHOLOGY | 30–53 (24 dims) | Similarity | 90.32% | `by_design`; not confirmed as leak |
| CONTEXT | 54–65 (12 dims) | Similarity | 33.33% | `possible`; not confirmed |
| SYMBOLIC | 66–77 (12 dims) | Similarity | 53.74% | `likely_leak`; confirmed |
| MODAL | 109–148 (40 dims) | Similarity | 48.70% | `possible`; confirmed |
| ROOT | 228–239 (12 dims) | Similarity | 34.98% | `by_design`; not confirmed as leak |

The percentages above are the snapshot's `accuracy_mean` values rounded to two decimal places. The snapshot's notes call accuracy above **0.40** on its balanced three-class problem a “leak confirmed” criterion, but the `by_design` labels matter: MORPHOLOGY is physically tied to an instrument, so its 90.32% must not become the reddest failure panel. Show the diagnostic's recorded `leak_hypothesis` and `leak_confirmed` as text rather than reconstructing an alarm from accuracy alone.

### Practice exercise 2: use the shared baseline

How far above the 33.33% displayed chance baseline are STRUCTURE and CONTEXT, in percentage points? Would a separate y-axis for every panel help this comparison?

> **Answer:** STRUCTURE is `50.20 - 33.33 = 16.87` percentage points above the displayed baseline. CONTEXT is `33.33 - 33.33 = 0.00` percentage points above it at the displayed precision. Separate auto-scaled axes would hide the common magnitude; use the same 0–100% scale and label both values. This arithmetic describes the fixed classifier diagnostic, not a statistical significance test.

## 2. Separate the measurement from the interpretation

Each panel answers **how accurately this particular classifier predicted instrument from this partition's vector**. It does not answer whether the partition is “good.” A physical-realization partition such as MORPHOLOGY is expected to retain instrument information. STRUCTURE's 50.20% and SYMBOLIC's 53.74% are marked as confirmed leaks by the recorded diagnostic; those are investigation leads under its criterion. The six partitions also have different dimensionalities and meanings, so differences in accuracy cannot be assigned to one causal mechanism from this chart. The 83.11% `full_classifier_accuracy` is a separate full-vector result, not a seventh partition to rank alongside these panels.

Use panel annotations for role and recorded hypothesis, perhaps grouped with a thin divider between “by design” and “investigate” interpretations. Keep the numeric position scale unchanged. Color may reinforce the text, but it must not be the only way to tell a diagnostic status. Put the date and method in one common caption to avoid repeating them so often that they crowd out the data.

### Practice exercise 3: reject a false ranking

A reviewer says, “MORPHOLOGY is the worst partition at 90.32%, while CONTEXT is best at 33.33%.” Repair the claim using the schema role and the diagnostic fields.

> **Answer:** The means rank this classifier's ability to infer instrument, not partition quality. MORPHOLOGY represents physical realization and is labeled `by_design` with `leak_confirmed: false` in the fixed artifact; high instrument predictability is expected there. CONTEXT is near the recorded chance baseline and is labeled `possible` with `leak_confirmed: false`, but this alone does not establish useful context encoding or retrieval performance.

## 3. Label which coordinate system the viewer is reading

The canonical schema's raw vector has **240 dimensions**. It places STRUCTURE at raw slots **6–29** and ROOT at **228–239**. The June diagnostic describes an index with `corpus.dims: 124` and reports compact-coordinate `start: 0`, `end: 24`, `dims: 24` for STRUCTURE; ROOT appears at `start: 112`, `end: 124`, `dims: 12`. Those `end` values are exclusive by the recorded `start`, `end`, and `dims` arithmetic. The schema's similarity partitions pack into the 124-dimensional compact view, omitting identity and informational partitions. Label raw and compact coordinates explicitly. Otherwise, a reader may mistake two valid coordinate systems for schema drift.

Do not put raw slot indices on the diagnostic accuracy axis: a slot position is neither a percentage nor a score. If the lesson needs a layout view, use a separate strip with raw ranges and roles; keep the diagnostic's six aligned percentage panels for classifier results.

### Practice exercise 4: map the offsets

The diagnostic says `STRUCTURE start=0, end=24, dims=24`, while the schema says raw slots 6–29. Does that prove the diagnostic used the wrong partition? What would ROOT's compact range be?

> **Answer:** No. The diagnostic describes the compact 124-dimensional index, whose STRUCTURE span is `[0,24)`; the schema's raw STRUCTURE span is slots 6 through 29. ROOT's diagnostic span is `[112,124)` for 12 dimensions, while its raw span is slots 228 through 239. State the coordinate system and end convention next to either layout before comparing offsets.

## 4. Preserve the boundary of the claim

The schema says ROOT was split out in v1.8 to make STRUCTURE match across **voicings of the same pitch-class set**, regardless of octave, voicing, or instrument. It also warns that STRUCTURE as a whole contains pitch-class chroma and is **not transposition-invariant**; only its ICV and cardinality subdimensions have that property. Instrument-classification accuracy does not test either invariance claim. A separate fixed diagnostic result reports 100% average pitch-class-set match among 50 tested queries' top ten, but that retrieval measure is a different task and sample. If shown, it needs its own panel or table and denominator, not a seventh point on the accuracy scale.

The [July 23 quality report](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/docs/quality/README.md) marks its five tracked embedding partition feeds stale: their last real observation was June 25, 28 days before that report. The separate ROOT value is dated June 25 by the pinned diagnostic snapshot, not by a ROOT feed in that report. A small-multiples chart may faithfully depict June 25 while being unsuitable as current operational status. Date the visualization at the source observation and link both the source snapshot and schema revision.

[DV-001](dv-001-observed-degraded-stale-quality.md) explains why a historical observation and a current operational status require different captions.

### Practice exercise 5: write the dashboard caption

Write two sentences for the six-panel chart. Include the pinned date, measure, baseline, and one interpretation limit. Correct this proposed claim: “Low ROOT leakage proves STRUCTURE is transposition-invariant and the live index is healthy.”

> **Answer:** “In GA's June 25, 2026 embedding diagnostic at revision `dc2e74c`, six aligned panels show mean instrument-classification accuracy by similarity partition on a shared 0–100% axis, with the balanced three-class 33.33% chance baseline. The diagnostic's role and leak labels qualify those percentages and it does not test transposition invariance; the July 23 report marks five tracked partition feeds stale, while ROOT is dated by the diagnostic itself, so the plot cannot establish current index health.”

## Key takeaways

- Small multiples work here because all six panels share one diagnostic measure and one scale.
- Preserve each partition's role, dimensions, and recorded interpretation beside its number.
- Raw 240-dimensional schema coordinates and compact 124-dimensional index coordinates serve different layouts.
- Instrument predictability, pitch-class-set retrieval, same-set invariance, and transposition invariance are different questions.
- Date a fixed artifact and expose staleness before readers act on it.

## Project evidence and limits

- Pinned GA [canonical schema](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/Common/GA.Business.ML/Embeddings/EmbeddingSchema.cs), [June 25 embedding diagnostic](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/state/quality/embeddings/2026-06-25.json), and [July 23 quality report](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/docs/quality/README.md). The schema registry and version constants are the authority for this lesson; older prose comments in that file still describe earlier schema layouts.
- The small-multiples layout is a proposed teaching design, not a published GA dashboard. The diagnostic is one fixed run with a particular classifier, balanced sample, and index; it does not establish current behavior or causal sources of instrument information. Human subject review, learner attempt, localization, and public Learn readback are pending.

*Research: `data-visualization-2026-10-11-007`. English draft only; review and publication pending.*
