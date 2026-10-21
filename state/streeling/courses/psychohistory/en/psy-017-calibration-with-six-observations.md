---
module_id: psy-017-calibration-with-six-observations
department: psychohistory
course: "Calibration with Six Observations"
level: intermediate
prerequisites: ["mat-009-estimation-uncertainty-sampling", "psy-004-how-large-is-large"]
estimated_duration: "45 minutes"
produced_by: claude-psychohistory-path
research_cycle: psychohistory-2026-10-13-017
version: "0.1.0"
---

# Calibration with Six Observations

> **Department of Psychohistory** | Intermediate | 45 minutes | English draft; human subject and learner review pending

## Objectives and project question

You will trace a calibration record to the files behind its counts, put an exact interval on a proportion of six, compute how often a calibrated forecaster shows the same count, find the sample size that separates two rates, and follow a correction rule fed six observations at a time. **Project question:** a belief file records that 2 of 6 high-confidence beliefs were later revised and nudges a threshold by −0.1. What can six observations say about calibration?

[PSY-002](psy-002-governance-phase-transitions.md) lists belief skew among six signals of an approaching regime shift; this module asks how much one small count about beliefs can carry. [PSY-004](psy-004-how-large-is-large.md) builds the exact interval reused here, [PSY-016](psy-016-brier-score.md) scores probability forecasts with the Brier score, and [PSY-025](psy-025-capstone-preregistered-forecast.md) uses both.

## 1. Read the record, then recount it

**Observed.** A *belief file* in `state/beliefs/` holds a proposition, a truth value (T true, P probable, U unknown, D doubtful, F false, C contradictory) and a `confidence` between 0 and 1. At commit `4b03838` the folder holds eight `*.belief.json` files (plus a YAML list of 19 beliefs, 9 at 0.85 or more, that the producer's glob skips) and [`archived/`](https://github.com/GuitarAlchemist/Demerzel/tree/4b03838800dcd4894f1e026461979bff1d985ca8/state/beliefs/archived) thirteen more. This lesson rests on one, [`confidence-calibration.belief.json`](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/state/beliefs/confidence-calibration.belief.json). Its proposition says that the governance agent's "confidence-assignment threshold is calibrated against the observed overconfidence-then-revision rate in her belief states." Truth value P, confidence 0.92, one supporting item, none contradicting. That item's claim, in full:

```text
2 of 6 high-confidence beliefs (>= 0.85) were later revised (overconfidence_rate=0.3333). Revisions evidenced by archived prior versions: 2026-03-17-consumer-repo-integration-status.belief.json, 2026-03-17-ga-governance-integration.belief.json. Nudge magnitude capped at +/-0.1/cycle per ml-governance-feedback-policy.
```

A `calibration` block stores `threshold_nudge` −0.1, `applied_delta` 0.0, `prior_nudge` −0.1 and `cap` 0.1. The file does not say which six beliefs were counted, which threshold the nudge moves, or whether a revised belief was wrong.

**Where the record comes from.** The governance agent did not compute these numbers: its *applying script*, [`scripts/apply_ml_feedback.py`, lines 130–154](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/scripts/apply_ml_feedback.py#L130-L154), writes the belief with a fixed proposition and a fixed label P (commented "Probable: evidence leans true, magnitude still small-N") and copies the confidence, the claim and the claim's reliability from a recommendation document, which a producer in another repository (`ix/scripts/confidence_calibrator.py`, named in the script's header) computes from these same belief files.

Three pinned files state the rule. The [policy](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/policies/ml-governance-feedback-policy.yaml#L57) defines the rate as "Proportion of high-confidence beliefs that were later revised". The [pipeline specification](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/pipelines/ml-feedback-loop.ixql#L41) recommends a change when the rate exceeds 0.15, of size `max(-0.1, -1 * overconfidence_rate * 0.5)`. The applying script (line 128) adds that nudge to the stored total and clamps the total to ±0.10.

**Computed.** That producer ([`confidence_calibrator.py`](https://github.com/GuitarAlchemist/ix/blob/6418fcc69012108af266544ec4cf5a931a8f78e8/scripts/confidence_calibrator.py), read at ix commit `6418fcc`, outside the fixture) counts by this rule: every belief file, current or archived, with confidence at least 0.85 is "high-confidence", and the archived ones among them are "revised". [`extract.py`](../../../../../scripts/streeling_fixtures/psychohistory/psy-017/extract.py) snapshots the 21 pinned belief files into [`observed-input.json`](../../../fixtures/psychohistory/psy-017/observed-input.json), and [`analyze.py`](../../../../../scripts/streeling_fixtures/psychohistory/psy-017/analyze.py) applies that rule to them:

| Belief file | Truth value | Confidence | Group |
|---|---|---|---|
| `2026-03-18-consumer-repo-integration-status` | P | 0.85 | current |
| `2026-07-25-schema-conformance` | T | 0.95 | current |
| `confidence-calibration` | P | 0.92 | current |
| `remediation-effectiveness` | P | 0.90 | current |
| `2026-03-17-consumer-repo-integration-status` | F | 0.90 | archived: revised |
| `2026-03-17-ga-governance-integration` | F | 0.85 | archived: revised |

Four current files and two archived ones make six, the two archived ones are those the claim names, and the sentence rebuilt from the recount is identical to the recorded one ([`results.json`](../../../fixtures/psychohistory/psy-017/results.json), `recount`): one computation reproduced, not a second source. The four other current files hold 0.80 or 0.82, the eleven other archived files 0.5 or 0, and the YAML file's nine are never counted.

The record counts itself: its own 0.92 puts it among them. It and `remediation-effectiveness` are both written by the applying script, their confidences copied from recommendations; without those two the same rule gives 2 of 4. Nor were the six last updated at comparable times: the two archived ones 209.7 and 209.6 days before the record, the four current ones 31.5, 30.5, 0 and 0 days before it.

### Practice Exercise 1

From the recorded rate and `prior_nudge`, reproduce `threshold_nudge` and `applied_delta` with the two pinned formulas.

> **Answer:** `−0.5 × 2/6 = −0.1667`, which the formula caps at −0.1. Stored total: `−0.1 + (−0.1) = −0.2`, clamped to −0.1, so `threshold_nudge = −0.1` and `applied_delta = −0.1 − (−0.1) = 0.0`. The total already stood at its limit: this run changed nothing.

## 2. What a count of six allows

A forecaster is *calibrated* when, among statements made with confidence c, a share c turns out true. This lesson adds a reading of its own, which the repository does not state: every revision is an error. Beliefs held at 0.85 or more should then be revised at most 15% of the time; the pipeline's trigger is that same 0.15.

Treat the six as independent trials with one unknown revision rate. The *exact 95% interval* (two-sided; Clopper and Pearson; PSY-004 shows the construction) keeps every rate under which the observed count falls in neither 2.5% tail. **Computed:** for 2 of 6 it runs from **0.0433 to 0.7772**, and it contains 15%, 10% and 5%.

How often does a forecaster whose rate is known show two or more revisions among six? **Computed under assumed rates** ([`scenarios.json`](../../../fixtures/psychohistory/psy-017/scenarios.json)), percentages rounded to two decimals:

| Assumed forecaster | True revision rate | P(2 or more of 6) |
|---|---|---|
| Calibrated at 0.95 | 5% | 3.28% |
| Calibrated at 0.90 | 10% | 11.43% |
| Calibrated at 0.85 | 15% | 22.35% |
| As recorded | one third | 64.88% |

A forecaster calibrated exactly at the line shows the recorded count, or worse, more than one time in five. The *likelihood ratio* compares the probability of exactly 2 of 6 under two rates: 0.329218 at one third against 0.176177 at 15%, a ratio of 1.87. **This sample cannot distinguish a calibrated forecaster from an overconfident one.**

### Practice Exercise 2

Compute the probability of two or more revisions among six for a true rate of 15%.

> **Answer:** `P(0) = 0.85^6 = 0.377150` and `P(1) = 6 × 0.15 × 0.85^5 = 0.399335`, so `P(2 or more) = 1 − 0.377150 − 0.399335 = 0.2235` to four decimals.

### Practice Exercise 3

A colleague says: "One third is more than twice 15%, so the forecaster is clearly overconfident." Is that supported, refuted or left undecided by the record? Give two numbers.

> **Answer:** Undecided. The exact interval, 0.0433 to 0.7772, contains 15% and even 5%, and exactly 2 of 6 is only 1.87 times as probable at one third as at 15%.

## 3. How many observations would separate 15% from 33%

Take a rule: "call the forecaster overconfident when c or more of n beliefs are revised". Its *false alarm* rate is the probability that a calibrated forecaster (15%) triggers it; its *detection* rate, the probability that an overconfident one (one third) does. **Computed** for n = 6:

| Rule | False alarm | Detection |
|---|---|---|
| 1 or more of 6 | 62.29% | 91.22% |
| 2 or more of 6 | 22.35% | 64.88% |
| 3 or more of 6 | 4.73% | 31.96% |

Keeping false alarms under 5% means waiting for three revisions, and that rule misses an overconfident forecaster 68.04% of the time. The recorded count, 2, does not reach it. The pinned rule fires from the table's first row: one revision among six, a rate of 0.1667, is above the trigger.

`analyze.py` searches every n up to 400 with exact binomial sums. The smallest sample with a false alarm of at most 5% and a detection of at least 80% is **33** ("9 or more of 33": 4.95% and 82.12%), which is 5.5 times the six. If the true rate were 25% instead of one third, the same design would need 101.

### Practice Exercise 4

Assume, only to get a scale, that high-confidence beliefs keep being recorded at the pace of the six: six in the 209.7 days between the earliest of them and the record. How many days after the earliest of the six would the 33rd arrive, and how many after the record?

> **Answer:** `33 × 209.7 / 6 ≈ 1,153` days after the earliest, so `27 × 209.7 / 6 ≈ 944` days, about 2.6 years, after the record. The pace is an assumption: the dates are last updates, not creation dates.

## 4. A correction rule fed six observations

**Computed from the pinned rule.** With six beliefs per cycle, no revision leaves the stored total alone, one moves it by −0.0833 and two or more by −0.1. A forecaster calibrated at 15% is nudged down in 62.29% of cycles, one at 5% in 26.49%, an overconfident one in 91.22%. Nothing recorded moves it up: the specification's upward branch needs an "underconfidence rate", and the belief file holds none.

**Synthetic.** Give the rule its best case, a fresh and independent six on every cycle, and follow the stored total exactly (a seeded simulation of 20,000 runs agrees within 0.0073):

| After | Calibrated (15%): total at −0.1 | Overconfident (one third): total at −0.1 |
|---|---|---|
| 1 cycle | 22.35% | 64.88% |
| 4 cycles | 89.41% | 99.92% |
| 13 cycles | 99.9954% | 100.00% |

The policy schedules this calibration weekly, so 13 cycles are one quarter. By then both forecasters sit at −0.1: the stored value is where the rule ends for either, and is no evidence about which one is present.

**Observed.** The recorded run is not that best case. `prior_nudge` is −0.1 and `applied_delta` is 0.0, and the two revisions it cites were last updated on 2026-03-17: this run re-read old evidence.

**What "revised" measures.** Both archived beliefs carry F: on 2026-03-17 they judged, at 0.90 and 0.85, that an integration step had not happened. The [current belief on that subject](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/state/beliefs/2026-03-18-consumer-repo-integration-status.belief.json) cites work dated 2026-03-18. The pinned files show verdicts overtaken by events, and the folder's [`SUPERSEDED.md`](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/state/beliefs/archived/SUPERSEDED.md) says archived beliefs "are retired, not deleted"; nothing records that either verdict was wrong when written. In the other direction, that current belief's `refresh_note` records "T -> F" on 2026-09-12 and "F -> P" on 2026-09-13, edited in place, which a count of archived files cannot see. Counting it gives 3 of 6.

**The record's own confidence.** The producer (cited, outside the pin) sets it by `min(0.92, 0.70 + 0.02 × belief files read)`. With 21 files that is the cap, 0.92: the formula uses neither the 2 nor the 6, and from eight files on it reaches 0.85, the line (`CONF_AUTO_APPLY`) below which the applying script escalates a recommendation instead of applying it. So the 0.92 is not a judgment of how well the claim is supported, and section 2 says what it cannot mean: six observations support no statement about the revision rate narrower than "between 4% and 78%" at 95% confidence.

**The strongest objection to this reading** is Bayesian. With a uniform prior on the rate, the probability that it exceeds 15% is 0.926235 after 2 of 6. But that prior already gives 0.85 before any data, so the six observations add 0.076; and the objection inherits the count's defects. What would settle it: an outcome, right or wrong at a fixed delay, for at least 33 high-confidence beliefs that the applying script does not write.

### Practice Exercise 5

(a) For the calibrated forecaster of the table, compute the probability that the stored total is still 0 after 4 cycles. (b) Should a stored −0.1 be read as evidence of overconfidence? State your criterion.

> **Answer:** (a) No revision in four samples of six: `0.377150^4 = 0.020233`, about 2%. (b) No. An observation is evidence for one hypothesis over another only if it is clearly more probable under the first. After 4 cycles a total of −0.1 has probability 99.92% for the overconfident forecaster and 89.41% for the calibrated one, a ratio of `0.9992 / 0.8941 = 1.12`; after 13 cycles the ratio is 1.00. Both forecasters are synthetic.

## Sources, limits, and next check

**Observed, pinned at Demerzel `4b03838800dcd4894f1e026461979bff1d985ca8`:** the calibration belief, the twenty other belief files, the YAML belief list, the archive's `SUPERSEDED.md`, the policy, the pipeline specification and the applying script linked above.

**Fixture.** The [README](../../../fixtures/psychohistory/psy-017/README.md) gives the commands, the 32 self-checks and the negative controls.

**Method references.** Clopper, C. J., and Pearson, E. S. (1934), "The Use of Confidence or Fiducial Limits Illustrated in the Case of the Binomial", *Biometrika* 26(4), 404–413, [doi:10.1093/biomet/26.4.404](https://doi.org/10.1093/biomet/26.4.404). Lichtenstein, S., Fischhoff, B., and Phillips, L. D. (1982), "Calibration of probabilities: The state of the art to 1980", in Kahneman, D., Slovic, P., and Tversky, A. (eds.), *Judgment under Uncertainty: Heuristics and Biases*, Cambridge University Press, 306–334.

**Not done.** The Git history of the calibration belief was not read, so the number of cycles already applied is unknown. Whether any process reads the stored nudge and moves a threshold was not traced. The recommendation document the belief cites is a runtime file the repository does not keep, and which version of the ix producer wrote it is not recorded. Every probability assumes independent beliefs with one rate, which the six are not; the figures are a best case for the data. No human has reviewed the subject matter of this lesson and no learner has tried it.

**Next check.** Read the history of `state/beliefs/` to count the cycles and see whether the six ever changed. If every cycle re-read the same two archived files, the conclusion sharpens from "six observations cannot decide" to "one count of six, applied many times".
