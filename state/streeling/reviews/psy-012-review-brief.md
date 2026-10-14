# PSY-012 bounded review brief

Status: **open**. This is a human-review and learner-trial packet. It is not an approval receipt, and nothing in it is evidence about how close the GuitarAlchemist governance system is to any transition.

## Frozen target and inputs

- English course: `state/streeling/courses/psychohistory/en/psy-012-early-warning-false-alarms.md`, Git blob `43402bf33c9b53db538fb20094bd18a2589513ce` (the blob identifies the exact text; `git log --diff-filter=A --format=%H -- state/streeling/courses/psychohistory/en/psy-012-early-warning-false-alarms.md` names the commit that added the file).
- Fixture data in `state/streeling/fixtures/psychohistory/psy-012/`, programs in `scripts/streeling_fixtures/psychohistory/psy-012/`:
  - `scripts/streeling_fixtures/psychohistory/psy-012/analyze.py` (analysis script): Git blob `9f59f16de25fb96610330ebcb77239e62a670d54`
  - `scripts/streeling_fixtures/psychohistory/psy-012/extract.py` (observed-data extract): Git blob `22f774c7cda1b179e5c46a3f6ce48c58a2acf164`
  - `scenarios.json` (synthetic assumptions, seeds, transfer inputs): Git blob `cca0b0da59c0b3fb6e5592c458507d495be11907`
  - `observed-input.json` (observed extract): Git blob `368e3bb40d75c7050ba2f3445983310109fd7512`
  - `results.json` (saved results): Git blob `c4f02e9cd8c39adf7ff36dd591897a048dfae8d6`
  - `README.md`: Git blob `23295c76122240e62b25de89472c2cc8fa8949fa`
- Observed source: `state/quality-trend/*.jsonl` at Demerzel commit `4b03838800dcd4894f1e026461979bff1d985ca8`; the five blob ids are recorded in `observed-input.json` → `source_files`.
- Production record: `state/streeling/course-productions/cp-psychohistory-2026-10-13-012.json`; its review and publication flags are false.

A later edit of the course or of a fixture file changes its blob. Review that diff explicitly before extending a verdict to the new source.

## Subject and method review

1. Regenerate. From the repository root at the frozen commit run `python -I scripts/streeling_fixtures/psychohistory/psy-012/extract.py --output <tmp>/observed.json` and `python -I scripts/streeling_fixtures/psychohistory/psy-012/analyze.py --output <tmp>/results.json`, then compare each with the committed file byte for byte. Compare the five `git_blob` values with `git ls-tree 4b03838800dcd4894f1e026461979bff1d985ca8 state/quality-trend/`.
2. Theory. Recompute phi = 1 − 2hq with h = 0.005: 0.5 at q = 50 and 0.9 at q = 10; variance 1 / (1 − phi²): 1.3333 and 5.2632, ratio 3.9474. Check the linearisation of `x² − q²` around `x = −q` yourself. Check the long-run estimates at phi = 0.9 (variance 5.2742, autocorrelation 0.9002) and the fold held at q = 25 (0.7513 against 0.75). Is "8.72 standard deviations from the unstable threshold" enough for the linear reading to hold, and does the lesson say that a closer approach was not simulated?
3. Estimator. By hand: the window 1, 2, 4, 3 has residuals −0.3, −0.1, 1.1, −0.7, variance 0.9 and lag-1 autocorrelation −0.4722; the six values 0.8, 0.5, 1.1, 1.4, 1.2, 1.9 give 13 concordant and 2 discordant pairs, tau 0.7333. Challenge the within-window straight-line detrending and the divisor W − 2. The lesson reports that a 25-point window reads 0.555 for a true 0.9: is the consequence for short windows stated strongly enough?
4. Rates. Recompute at least two table rows from the alarm counts in `results.json` → `simulation.configurations.<row>.systems.<system>.alarms`. For `n100_w50`: 297 of 1,000 approaching runs under the fixed rule; controls 87, 113 and 107 of 1,000. Check that the textbook threshold is 1.645 × sqrt(2(2m + 5) / (9m(m − 1))) with m = n − W + 1 (0.1588 for m = 51), and that the calibrated threshold comes from runs with their own seeds (`calibration` in `scenarios.json`), not from the control runs it is then judged on.
5. Sentences to challenge.
   - "Near 5% false alarms, detection depends on record length": one approach scenario (phi from 0.5 to 0.9) and one noise level support it. Is the limit stated where the claim is made, or only at the end?
   - "the detections come from the slowing down": the evidence is a linear twin within 3.7 percentage points, where the standard error of a difference is at most 2.24 points. Is that enough?
   - "The calibrated threshold is an estimate": 3.1% to 8.0% against a 5% target, where one rate has a standard error of about 0.69 points and the threshold is itself estimated from 1,000 runs. Sampling noise or a real dependence on the control's coefficient?
   - Any sentence that a reader could take as a statement about the project's distance from a regime shift. There should be none; the lesson says the flat record is evidence neither way.
6. Observed section. Recount from `observed-input.json`: 1,548 rows, 18 artifacts, 88 runs, 83 days; `compliance_rate` and `violation_count` with 0 changes in 1,519 consecutive pairs; `citation_count` with 20 changes, 16 series at 2026-09-13T17:52:14Z and 4 at 2026-10-03T15:31:16Z; 689 constant windows of 25 runs out of 1,105. Confirm that the script computes no variance, autocorrelation or tau on project data, and that the lesson leaves the nature of the two steps to PSY-011.
7. References. Check author, year, title, venue and DOI of the four citations, and that each is used for what it says. The M rule (the smaller of two taus) and the within-window detrending are the fixture's own simplifications: no sentence should attribute them to Dakos et al.
8. Exercises. Attempt the five exercises before reading their answer blocks. Record ambiguity, missing inputs or arithmetic errors with section references.

## Answer-free learner trial

Give [`psy-012-learner-task.md`](psy-012-learner-task.md) without this brief and without the course answer blocks. Record the learner's prior experience with time series and probability, the elapsed time, the unedited response, points of confusion, and any lesson revision followed by a retest.

Expected answers, copied from `results.json` → `transfer_task` (inputs in `scenarios.json` → `transfer_task`):

1. Far (q = 20): phi 0.2, variance 0.2604, standard deviation 0.5103. Near (q = 2.5): phi 0.9, variance 1.3158, standard deviation 1.1471. The variance grows by a factor of 5.0526.
2. 21 pairs in each list. Variance: 16 concordant, 5 discordant, tau 0.5238. Autocorrelation: 18 concordant, 3 discordant, tau 0.7143. M = 0.5238, at or above 0.5: the alarm fires.
3. Detection rate 0.46, false-alarm rate 0.06. With a base rate of 0.05 the probability of an alarm is 0.08 and the share of true alarms is 0.2875.
4. First series: 41 rolling values; the textbook standard deviation of tau is 0.1086 and the threshold 0.1786. Expected reason: neighbouring windows share 19 of their 20 points, so the 41 values are far from independent and the threshold is too low. Second series: 25 windows, 15 of them constant (0.6), 10 with some variation; in a constant window the variance is 0 and the lag-1 autocorrelation is 0 / 0, undefined. Expected decision: do not compute the indicators, because the only variation is two steps.
5. Open answer, scored with the rubric: a plan and a falsifier.

Score five criteria from 0 to 2 each:

1. Local theory: phi, variance and ratio correct, with the noise variance in the numerator.
2. Trend statistic: correct pair counts, both taus, M, and the alarm decision.
3. Rates and base rate: detection and false-alarm rates kept apart, and the share of true alarms computed from the base rate rather than read off the detection rate.
4. Preconditions: the overlap of rolling windows named as the reason the textbook threshold is too low, and constant windows recognised as giving undefined indicators, not low ones.
5. Plan and falsifier: variation checked before any indicator, instrument held fixed, a rule and a stationary control fixed in advance with a stated false-alarm rate, an outcome that would withdraw the alarm, and no synthetic rate presented as a measurement of a project.

A proposed pilot pass is at least 8 of 10 with a non-zero score on criterion 5; evaluate this threshold after an actual learner trial. No trial has taken place and no result exists.

## Verdict and publication boundary

No verdict exists. When a review happens, record the reviewer's identifier or pseudonym, the UTC date, the course blob, the kind (`subject` or `learner`), the evidence, the findings, and `approved`, `changes_requested` or `not_assessed`. There is no translation of PSY-012 to approve.

Keep the review and publish flags false until actual verdicts and learner evidence are recorded. This packet, the fixture's passing self-checks and the byte-identical reruns are not a review and not a publication.
