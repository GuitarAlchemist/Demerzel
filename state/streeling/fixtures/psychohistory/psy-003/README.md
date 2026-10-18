# PSY-003 fixture: review and publication queues

The program, `analyze.py`, lives in `scripts/streeling_fixtures/psychohistory/psy-003/` because this repository keeps executable code under `scripts/`; the data files it reads and writes are in this folder.

Fixture for the lesson `state/streeling/courses/psychohistory/en/psy-003-review-throughput-and-compounding.md`.
Python 3.9 or later, standard library only. The queue model is synthetic: no file of the repository is read, so
there is no `extract.py` and no `observed-input.json`, and no weekly throughput of the project was measured.

The lesson was drafted in the project pilot of Demerzel #1207, with its fixture as `simulate_pipeline.py`,
`pipeline-scenarios.json` and `pipeline-results.json` next to each other. Here the program follows this repository's
layout and gains `--check` and the self-checks below; its arithmetic is unchanged, and the four weeks of both
scenarios in `results.json` are the same numbers as in #1207's `pipeline-results.json`.

## Files

| File | Kind | What it is |
|---|---|---|
| `scenarios.json` | assumed | The two scenarios (12 new review-ready items a week, the weekly review and publication capacities, empty starting queues), the source counts the lesson quotes, the limits of the simulation, the hand-computed figures and the negative control. |
| `analyze.py` | script | Reads only `scenarios.json`, runs both scenarios week by week, runs the self-checks and writes `results.json`. |
| `results.json` | computed | Every week of both scenarios, the negative control and the list of self-checks, with the observed counts and the snapshot commit copied from `scenarios.json`. |

## Regenerate

From the repository root:

```text
python -I -B scripts/streeling_fixtures/psychohistory/psy-003/analyze.py
python -I -B scripts/streeling_fixtures/psychohistory/psy-003/analyze.py --check
```

`--check` recomputes the results and compares them with the saved file, ignoring only CRLF against LF.
`--scenarios` and `--output` name other files.

## The model

For each week, in this order: the new review-ready items join the review queue; review accepts
`min(review queue, review capacity)`; the accepted items join the publication queue; publication takes
`min(publication queue, publication capacity)`. Every completed review is assumed to approve and every accepted item
to be publishable, so the accepted and published counts are upper bounds. Changes requested, rework, rejections and
withdrawals have no state in the model.

Every quantity is a whole number and the only operations are `+`, `-` and `min`, so `results.json` is the same bytes
on every platform. Checked: the same SHA-256 of `results.json` on CPython 3.9.25, 3.12.12 and 3.14.3 under Windows
x86-64 and on CPython 3.14.5 under Linux x86-64 (WSL). Not run on macOS or on an ARM processor.

## Observed, computed, synthetic

- **Observed:** the counts under `observed_source_counts` (21 course directories, the provisional 525 core-course
  target, 113 core codes, nine six-locale and five-answer candidates, four committed review briefs, zero approved
  production-review flags). They come from the review-candidate snapshot and the progress reporter of Demerzel commit
  `3d175ab88b06f6fd06cfa8475b3f7e9be6323a6b`, on the branch of #1207, not from `master`; the snapshot itself was
  computed at commit `793e92bd5a8a97552ed3fee68a3956929c7d0c54`. `analyze.py` copies them from `scenarios.json` into
  `results.json`, with the snapshot commit; it does not recompute them.
- **Synthetic:** every arrival and capacity, and so everything under `scenarios` in `results.json`. The arrival rate
  of 12 review-ready items a week is not the nine observed triage candidates: a candidate is not review-ready.

## Self-checks

`analyze.py` aborts instead of writing a result when one of its checks fails; `results.json` lists them under
`checks`.

- Both conservation identities, every week of both scenarios: initial review queue + new review-ready items =
  accepted + waiting review, and initial publication queue + accepted = published + waiting publication.
- No stage takes more than its capacity, and a stage that takes less than its capacity leaves its queue empty.
- The hand-computed figures below are found.
- **Negative control.** One accepted item is lost between the two queues in week 2 of
  `growing_review_fixed_publication` (the publication queue is one short from then on): the publication identity must
  fail, and `negative_control.identities_hold` must be `false`.

**Hand-computed case.** With 12 new items a week and empty starting queues:

- `flat` (review 4, publication 4 a week): the review queue grows by 8 a week, `8, 16, 24, 32`; 16 accepted and 16
  published in all; nothing waits for publication.
- `growing_review_fixed_publication` (review `4, 8, 16, 32`, publication 4 a week): week 1 accepts 4 of 12 (8 wait);
  week 2 accepts 8 of 20 (12 wait); week 3 accepts 16 of 24 (8 wait); week 4 finds 8 + 12 = 20 and accepts all 20, so
  12 of its 32 places stay idle. Accepted `4, 8, 16, 20`, 48 in all; published 4 a week, 16 in all; 0 waiting review
  and 48 − 16 = 32 waiting publication.

The script must find these figures.
