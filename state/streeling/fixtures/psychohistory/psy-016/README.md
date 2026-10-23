# PSY-016 fixture: Brier and logarithmic scores on the effectiveness-label pairs

The two programs, `extract.py` and `analyze.py`, live in `scripts/streeling_fixtures/psychohistory/psy-016/` because this repository keeps executable code under `scripts/`; the data files they read and write are in this folder.

Fixture for the lesson `state/streeling/courses/psychohistory/en/psy-016-brier-score.md`.
Python 3.9 or later, standard library only.

## Files

| File | Kind | What it is |
|---|---|---|
| `extract.py` | script | Reads the five `state/quality-trend/*.jsonl` files, checks their shape and their Git blob ids against Demerzel commit `4b03838800dcd4894f1e026461979bff1d985ca8`, and writes `observed-input.json`. |
| `observed-input.json` | observed | The 88 run timestamps and, for each of the 18 artifacts, two strings with one character per run (`effectiveness_to` and the `baseline` flag), plus the counts made by `extract.py`. |
| `scenarios.json` | assumed | The imaginary forecasters (the probability each states), the thresholds of the hypothesis, the inputs of the lesson's exercises, the assumed true probabilities and seeds of the proper-scoring demonstration, and the hypothetical release log of the learner task. Nothing in it is measured in the repository. |
| `analyze.py` | script | Reads only `observed-input.json` and `scenarios.json`, rebuilds the pairs, scores every forecaster, runs the self-checks and writes `results.json`. |
| `results.json` | computed | Every number used by the lesson, the review brief and the transfer task. |

Artifact names are written with a space on each side of every slash (`policies / alignment-policy.yaml`):
`scripts/evolution_metrics.py` counts every tracked file that contains an artifact's path as a citation of that
artifact, and a data file about the artifacts is not one.

## Regenerate

From the repository root:

```text
python -I -B scripts/streeling_fixtures/psychohistory/psy-016/extract.py
python -I -B scripts/streeling_fixtures/psychohistory/psy-016/analyze.py
python -I -B scripts/streeling_fixtures/psychohistory/psy-016/analyze.py --check
```

Each command finishes in about a second. Both scripts write the same bytes on every run (LF line endings, `indent=2`,
insertion-ordered keys). `--check` recomputes the results and compares them with the saved file, ignoring only CRLF
against LF.

`extract.py` stops with exit code 1 when a source file is missing, when a row lacks a key, has an unknown label, a
malformed timestamp or a duplicate (timestamp, artifact), or when a file is not the blob of the pinned commit (the
nightly feeder appends rows, so this happens on any later checkout). `--allow-drift` snapshots newer data anyway and
records `"commit": null`; the lesson's numbers then no longer apply.

## Observed, computed, synthetic

- **Observed:** the labels, timestamps and `baseline` flags in `observed-input.json`; in `results.json`, the section
  `observed` (1,548 rows, 18 artifacts, 1,529 usable pairs, 1 changed; 11 pairs from a seed row, 1,518 between feeder
  runs).
- **Synthetic forecasters, computed scores:** nobody issued a forecast for these pairs. `scores`, `one_pair`,
  `hypothesis_check` and exercises 1, 2, 3 and 5 of `worked_examples` score imaginary forecasters, defined in
  `scenarios.json` by the probability they state, on the observed outcomes. `base_rate` and `long_step_hedge` use
  hindsight and are flagged `uses_hindsight`.
- **Synthetic:** `proper_scoring` (assumed true probabilities 0.3 and 0.02, closed-form expectations and 20,000
  seeded draws each), exercise 4 and `transfer_task` (a hypothetical release log).

## Rounding and platforms

Brier scores, sums of squared errors, shares and skills are computed as exact fractions (`fractions.Fraction`) and
stored twice: `exact` (the fraction) and `value` or `percent` (rounded: Brier scores to 9 decimals, sums, skills and
expected scores to 6, percentages to 2, days to 3). The simulation draws with `random.Random(seed).random()` and keeps
only the integer count of events. The only values that depend on the C library are natural logarithms; each is stored
to 6 decimals after a self-check that it lies more than 0.000001 of a last-digit unit away from a rounding boundary,
so a last-bit difference between platforms cannot change a stored digit. An infinite logarithmic score is stored as
`null` with `"infinite": true`.

## Self-checks

`analyze.py` aborts instead of writing a result when one of its 30 checks fails; `results.json` lists them under
`checks`. They include a recount of `extract.py`'s counts through a second code path, the path's shared facts at the
pinned commit, the identity `Brier score = (p - base rate)^2 + base rate (1 - base rate)` for every constant
forecaster on every subset, additivity of the squared errors over the two subsets, the equality of the Brier score
when the complementary event is scored with `1 - p`, a brute-force check of the "changed pairs needed" thresholds,
the closed form of the expected Brier score, and a case worked by hand:

```text
pairs      1    2    3    4
outcome    1    0    0    0        base rate 1/4, reference Brier score 1/4 x 3/4 = 3/16
stated     0.5  0.5  0    0
squared    0.25 0.25 0    0        sum 1/2, Brier score 1/8, skill 1 - (1/8)/(3/16) = 1/3
-ln        ln 2 ln 2 0    0        logarithmic score 2 ln 2 / 4 = 0.346574
```

A forecast equal to the outcome scores 0 under both rules; its opposite scores a Brier score of 1 and an infinite
logarithmic score.

Two results could pass on nothing: "0 changes between feeder runs" and the Brier score of 0 that follows for `never`
there. The negative control plants one flipped label in a copy of the snapshot (`constitutions / asimov.constitution.md`,
run index 44, T to D) and confirms that the counters move: changed pairs 1 to 3 on all pairs and 0 to 2 between
feeder runs, `never`'s Brier score between feeder runs 0 to 2/1,518, and its logarithmic score there from 0 to
infinite. In the proper-scoring section the same test that finds the lowest expected Brier score at the true
probability finds the lowest expected absolute error somewhere else, which is the control for that test.

## Limits

- The snapshot keeps `effectiveness_to`, timestamps and the `baseline` flag only.
- One label change in 1,529 pairs: every score, share, skill and ranking that involves it rests on a single event.
- The forecasters are imaginary and were defined after the outcomes were known. No forecast was issued in advance,
  and no model was trained or run.
- The pairs are 18 artifacts read repeatedly, not independent trials; no sampling uncertainty is attached to any
  score.
- The simulation illustrates two closed forms. It says nothing about the project.
