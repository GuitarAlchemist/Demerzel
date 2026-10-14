---
module_id: psy-011-measurement-change-or-system-change
department: psychohistory
course: "Measurement Change or System Change? Rebaselines in the Quality Trend"
level: intermediate
prerequisites: ["psy-002-governance-phase-transitions", "psy-005-persistence-baseline"]
estimated_duration: "40 minutes"
produced_by: claude-psychohistory-path
research_cycle: psychohistory-2026-10-13-011
version: "0.1.0"
---

# Measurement Change or System Change? Rebaselines in the Quality Trend

> **Department of Psychohistory** | Intermediate | 40 minutes | English draft; human subject and learner review pending

## Objectives and project question

You will read how a number is produced before reading its series, find a change of instrument in a log, sort every jump into "measurement starts", "instrument changes" or "same instrument", and show what an alarm rule does when the three are mixed. **Project question:** the quality trend has rows flagged `rebaseline` and a `citation_source` field that appears part-way through; which jumps in the series are the instrument changing rather than the system?

[PSY-002](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/state/streeling/courses/psychohistory/en/psy-002-governance-phase-transitions.md) reads a fast change in a governance indicator as a sign of an approaching regime shift. That reading assumes the indicator was produced the same way before and after; this module tests the assumption on the citation column of the log that [PSY-005](psy-005-persistence-baseline.md) introduced. [PSY-012](psy-012-early-warning-false-alarms.md) covers early-warning indicators.

## 1. Read the instrument before the series

An *instrument* is the whole procedure that turns the world into a recorded number: who or what counts, what is counted, and where. A *system change* is a change in the thing counted.

**Observed, in the pinned code.** A [daily job](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/.github/workflows/demerzel-quality-trend.yml) runs the *feeder*, [`scripts/quality_trend.py`](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/scripts/quality_trend.py), which appends one row per governance *artifact* (a policy, a schema, a skill) to `state/quality-trend/`; one execution is a *run*. A row's `citation_count` is [copied from the artifact's evolution record](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/scripts/quality_trend.py#L75-L76), a JSON file in `state/evolution/`. Since September 2026 a second script, [`scripts/evolution_metrics.py`](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/scripts/evolution_metrics.py), computes that number as the ["tracked files that mention any of the artifact's citation paths (`git grep -lF`)"](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/scripts/evolution_metrics.py#L12-L15) and [stamps the record](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/scripts/evolution_metrics.py#L104-L107) with `citation_source: "git-grep-v1"`. Before that, its docstring says, every metric ["was typed by hand"](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/scripts/evolution_metrics.py#L4-L8) and "nothing updated it afterwards".

The feeder reacts to the stamp in [lines 90 to 92](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/scripts/quality_trend.py#L90-L92) and [line 99](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/scripts/quality_trend.py#L99), where `prev` is the artifact's previous row:

```text
prev = previous.get(artifact, {})
source = metrics.get("citation_source")
rebaseline = bool(prev) and prev.get("citation_source") != source
"delta_citations": 0 if rebaseline else citation - int(prev.get("citation_count", 0) or 0),
```

Three things follow:

1. A *rebaseline* is declared when a previous row exists and its source label differs from the current one; a missing key reads as null.
2. The recorded change, `delta_citations`, is then 0, while [`citation_count` is written as read](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/scripts/quality_trend.py#L96): the jump stays in `citation_count`.
3. With no previous row, or one without a count, the feeder subtracts 0: the "change" is the whole count.

The feeder's docstring gives the intent: ["the jump is a change of measurement, not a change in citations"](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/scripts/quality_trend.py#L14-L18).

**Computed.** [`analyze.py`](../../../../../scripts/streeling_fixtures/psychohistory/psy-011/analyze.py) re-implements this rule on the snapshot that [`extract.py`](../../../../../scripts/streeling_fixtures/psychohistory/psy-011/extract.py) takes. It reproduces `delta_citations` in all 1,537 rows that have a count and all 576 recorded flags, with 0 mismatches.

### Practice Exercise 1

**Synthetic** rows from [`scenarios.json`](../../../fixtures/psychohistory/psy-011/scenarios.json). Give the flag and the `delta_citations` the rule writes: (a) an artifact's first row, count 9; (b) previous row 12 with no source, now 27 from `git-grep-v1`; (c) previous row 6 and now 19, both `git-grep-v1`, after someone added a path to the record's `citation_paths`. Which case is an instrument change the rule cannot see?

> **Answer:** (a) No previous row: no flag, delta 9, a start of measurement recorded as a rise. (b) Flag, delta 0; the step of 15 survives only in `citation_count`. (c) No flag, delta 13, the case the rule cannot see: the list of paths is part of the instrument, but the label did not change, so the edit is recorded as 13 new citations.

## 2. Locate the change in the record

**Observed** in [`observed-input.json`](../../../fixtures/psychohistory/psy-011/observed-input.json): 1,548 rows in 88 runs for 18 artifacts. The first run, stamped 2026-05-01, holds 11 *seed rows* without a count; 87 feeder runs follow. The `citation_source` key is absent from the first 56 runs (972 rows) and present in the last 32. It first appears at 2026-09-13T17:52:14Z, where 16 rows carry `git-grep-v1` and `rebaseline: true`. The other 2 rows have a null source and no flag: their artifacts have an empty `citation_paths` list, which [marks an artifact outside the repository](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/scripts/evolution_metrics.py#L20-L23), and keep their hand-typed 55 and 0. No other row is flagged.

**Computed.** Each of the 16 artifacts held one hand-typed value in every earlier row. That run replaced it:

| Artifact (slashes spaced) | Hand-typed | `git grep` |
|---|---|---|
| `constitutions / asimov.constitution.md` | 5 | 65 |
| `contracts / galactic-protocol.md` | 2 | 43 |
| `policies / alignment-policy.yaml` | 3 | 42 |
| `constitutions / default.constitution.md` | 11 | 47 |
| `skills / demerzel-drive + policies / autonomous-loop-policy v1.1.0` | 1 | 27 |
| `logic / tetravalent-state.schema.json` | 4 | 23 |
| `logic / governance-evolution.schema.json` | 2 | 17 |
| `policies / autonomous-loop-policy.yaml` | 12 | 27 |
| `afk-graduated-self-merge` | 1 | 14 |
| `schemas / loop-state.schema.json` | 3 | 15 |
| `logic / kaizen-pdca-state.schema.json` | 3 | 13 |
| `scripts / afk_backends /` | 0 | 6 |
| `ml-feedback-loop` | 1 | 6 |
| `meta / compounding-cycle` | 4 | 5 |
| `docs / governance / the-sentinel-spec.md` | 1 | 0 |
| `docs / governance / harness-engineering-direction.md` | 8 | 1 |

The steps run from −7 to +60 and the ratio of new to old value from 0 to 27 (undefined for an old value of 0): no single conversion factor links the two instruments.

### Practice Exercise 2

From the table, compute the sum of the 16 counts before and after, and the step. Add the two unflagged artifacts to get the total over all 18 and its ratio. How many counts fell? What did `delta_citations` sum to in that run?

> **Answer:** Before `61`, after `351`, step `351 − 61 = 290`. Over all 18 artifacts: `61 + 55 + 0 = 116` before and `351 + 55 + 0 = 406` after, a ratio of `406 / 116 = 3.5`. Two counts fell (8 to 1 and 1 to 0). Flagged rows have delta 0 and the two others did not move, so `delta_citations` sums to 0 in the run where the total grew by 290.

## 3. Sort every jump

"Rows with a non-zero `delta_citations`" and "rows whose count differs from the previous row" sound like one set. Each holds 20 rows; only 4 are in both. Classifying every row against the artifact's previous row shows why (**computed**, [`results.json`](../../../fixtures/psychohistory/psy-011/results.json)):

| Class of row | Rows | Count changed | Non-zero delta |
|---|---|---|---|
| First count: no earlier count to compare with | 18 | undefined | 16 |
| Instrument change: previous row has another source | 16 | 16 | 0 |
| Same instrument: previous row has the same source | 1,503 | 4 | 4 |

The 16 non-zero deltas of the first class are levels, not changes: 10 follow a seed row, 6 are an artifact's first row, and they sum to 116. That leaves 4 rows, all in the run of 2026-10-03T15:31:16Z, each a step of +2.

Of the 1,503 same-instrument pairs of consecutive rows of one artifact, 1,007 have no source in either row (the hand-typed period and the two outside artifacts) and 0 changes. A number nobody retypes cannot move, so this zero says the instrument was silent, not that the system was still. Under `git-grep-v1`: 496 pairs, and the 4 changes.

The same split applies to the sum over artifacts, which grew from 106 at the first feeder run to 414 at the latest: `308 = 10 + 290 + 8`, that is first counts of artifacts added later, the instrument change, and same-instrument steps. Only the last is *like for like*: same instrument, same set of artifacts.

### Practice Exercise 3

Starting from 1,548 rows and 18 artifacts, derive the number of same-instrument pairs and the share that changed. Then give the share of the total's growth that was measured like for like.

> **Answer:** `1,548 − 18 = 1,530` row pairs. Remove the 11 that start at a seed row and the 16 that cross the change of source: `1,530 − 11 − 16 = 1,503`. Changed: `4 / 1,503 = 0.27%`. Growth: `8 / 308 = 2.60%`; the rest is a new instrument (290) or new artifacts (10).

## 4. Hold the measurement fixed before reading a shift

PSY-002's first signal is a rate of change "exceeding 2 standard deviations from its running mean", stated for its crystallization index, not for citations. As an **analysis choice** stored in `scenarios.json`, apply a rule of that form to the run-to-run step of the citation count summed over artifacts: flag a step that differs from the mean of all earlier steps (at least 3) by more than 2 of their population standard deviations. Feeder runs are 122 seconds to 6.45 days apart; the same rule on steps per day flags the same runs. **Computed** on three versions of the series:

| Series | Flagged steps | The +8 of 2026-10-03 |
|---|---|---|
| Summed `citation_count` | +2 and +8 on 2026-07-29, +290 on 2026-09-13 | not flagged |
| Summed `delta_citations` | +2 and +8 on 2026-07-29 | flagged |
| Same-instrument steps only | none earlier | flagged |

On the raw sum the rule raises three alarms and none is a like-for-like change: two are artifacts entering the sum, one is the new instrument. That one also inflates the running standard deviation, so the only like-for-like step passes unseen. With all earlier steps kept, an instrument change costs twice: a false alarm when it happens, and blindness afterwards. Caution on the last row: after an all-zero history any non-zero step is flagged.

### Practice Exercise 4

At the run of 2026-10-03 the 75 earlier steps have mean 4 and standard deviation 33.2602 in the raw sum, and mean 0.1333 and standard deviation 0.9428 in the summed `delta_citations`. For each series, compute the upper edge of the band (mean plus 2 standard deviations) and the smallest whole step that would be flagged.

> **Answer:** Raw sum: `4 + 2 × 33.2602 = 70.5204`, so +8 is inside the band and the smallest flagged step is 71. Summed deltas: `0.1333 + 2 × 0.9428 = 2.0189`, so +8 is flagged and the smallest flagged step is 3. One instrument change moved the detection threshold from 3 to 71.

**The strongest objection to this reading** is that "same instrument" rests on a label, and Exercise 1(c) shows an instrument change that keeps its label: the four remaining steps could be such a change. The fixture says: the four evolution records share one `last_cited` time, 2026-10-02T20:05:16Z, between the previous run and the run of the step, and two of the four artifacts measure the same path: four rows, at most three independent counts. Read outside the fixture, in Git history up to the pin: the producer script has a single commit, and between the two runs only the daily job's own commit touched `state/evolution/`, so nobody edited the code or a path list; commit [`98625c3`](https://github.com/GuitarAlchemist/Demerzel/commit/98625c317fd3440440bf406bd5302b79271db642), made at that same time, added French and Spanish translations of 13 course modules; and for each citation path of the four artifacts, exactly two files added between the two runs cite it at the pin, the two translations of one lesson. That is consistent with a change in the thing counted, and a small one: three lessons were translated.

### Practice Exercise 5

A dashboard reports "citations up about 3.9 times since July (106 to 414)" as evidence of a regime shift. Accept or reject, state your criterion, and name two records that would make a future shift readable.

> **Answer:** Reject. Criterion: two counts may be compared only if the same instrument produced both, for the same set of artifacts. Of the 308, 290 come from a new instrument and 10 from artifacts added to the sum; 8 pass the criterion, all in one run. Two helpful records: a source label that changes whenever the script, its exclusion list or a `citation_paths` list changes; and, at each change, both instruments run side by side for several runs, so the overlap measures the difference.

## Sources, limits, and next check

**Observed, pinned at Demerzel `4b03838800dcd4894f1e026461979bff1d985ca8`:** the five JSONL files of [`state/quality-trend/`](https://github.com/GuitarAlchemist/Demerzel/tree/4b03838800dcd4894f1e026461979bff1d985ca8/state/quality-trend), the two scripts linked above and the 18 `*.evolution.json` records of [`state/evolution/`](https://github.com/GuitarAlchemist/Demerzel/tree/4b03838800dcd4894f1e026461979bff1d985ca8/state/evolution). The fixture's [README](../../../fixtures/psychohistory/psy-011/README.md) gives the commands, the self-checks and the negative controls.

**Method references.** Shadish, W. R., Cook, T. D., and Campbell, D. T. (2002), *Experimental and Quasi-Experimental Designs for Generalized Causal Inference*, Houghton Mifflin (*instrumentation* as a threat to validity).

**Not done.** The `git grep` count was not recomputed for the runs before 2026-09-13, so nothing here says whether citations moved then. Earlier versions of the feeder were not read. The Git-history statements rest on commands listed in the review brief, not on the fixture. No human has reviewed the subject matter of this lesson and no learner has tried it.

**Next check.** Recompute the `git-grep-v1` count at the commit of every earlier run. One instrument under all 87 feeder runs would show whether anything moved before September; if it did, the conclusion changes from "almost nothing moved" to "the movement was not measured".

**Own footprint.** This module writes artifact names as labels with spaced slashes, so none of its files contains any artifact's citation path: run on them with each path, the literal search of section 1 (`git grep -lF`) finds nothing. PSY-020 takes up the general question.
