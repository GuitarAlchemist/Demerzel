# PSY-013 fixture: four resilience scores, exact intervals and exact tests

The two programs, `extract.py` and `analyze.py`, live in `scripts/streeling_fixtures/psychohistory/psy-013/` because this repository keeps executable code under `scripts/`; the data files they read and write are in this folder.

Fixture for the lesson `state/streeling/courses/psychohistory/en/psy-013-four-scores-and-a-trend.md`.
Python 3.9 or later, standard library only. No random number is drawn, so there is no seed: every probability is an
exact sum over a finite list of outcomes, computed with `fractions.Fraction` and rounded to 6 decimals when stored.

## Files

| File | Kind | What it is |
|---|---|---|
| `extract.py` | script | Reads twelve files of the pinned commit, checks their shape and their Git blob ids, and writes `observed-input.json`. |
| `observed-input.json` | observed | Snapshot at Demerzel commit `4b03838800dcd4894f1e026461979bff1d985ca8`: the four records of `state/resilience/history.json` (44 injection rows with level, name, expected detector, status and notes), the 42 scenario verdicts of the three red-team cycle files, the per-injection tables and scorecards of two reports in `docs/reports/`, and the definitions of R (glossary entry, metric policy thresholds and trend rule, README status line). |
| `scenarios.json` | assumed and cited | Confidence and significance levels, the family of comparisons, the rule that turns status labels into "caught", the reading of the trend rule, assumed fixed rates, PSY-002's regime names (cited), the imaginary held-out sets, the hand-computed cases and the choices of the learner transfer task. Nothing in it is measured in the repository. |
| `analyze.py` | script | Reads only `observed-input.json` and `scenarios.json`, recounts every cycle from its own detail, runs the self-checks and writes `results.json`. |
| `results.json` | computed | Every number used by the lesson, the review brief and the transfer task. |

## Regenerate

From the repository root:

```text
python -I scripts/streeling_fixtures/psychohistory/psy-013/extract.py
python -I scripts/streeling_fixtures/psychohistory/psy-013/analyze.py
python -I scripts/streeling_fixtures/psychohistory/psy-013/analyze.py --check
```

Each command finishes in a few seconds. `analyze.py` writes the same bytes on every run (LF line endings, `indent=2`,
insertion-ordered keys). `--check` recomputes the results and compares them with the saved file, ignoring only CRLF
against LF. Add `-B` to keep Python from writing a `__pycache__` folder.

`extract.py` stops with exit code 1 when a source file is missing, when a record, a table or a labelled line has an
unexpected shape, when a file is not the blob of the pinned commit, or when `state/resilience/` holds a file that the
pinned commit does not. `--allow-drift` snapshots newer files anyway and records `"commit": null`; the lesson's numbers
then no longer apply. The metric policy is YAML and is read with regular expressions on the few fields used (formula,
thresholds, trend rule), because the standard library has no YAML parser.

## Sources read by `extract.py`

- `state/resilience/history.json` and the three `state/resilience/2026-03-23-red-team-cycle-00N.json` files: the whole
  folder at the pin. The red-team files are a second series (14 scenarios graded PASS, PARTIAL or FAIL), not the detail
  of the history's cycles.
- `docs/reports/chaos-test-report.md` (dated 2026-03-22) and `docs/reports/shake-metafix-cycle-001.md` (cycle
  `chaos-003`): the two reports that score the same eleven injections one by one.
- `CONTEXT.md` (glossary entry for R), `policies/resilience-metric-policy.yaml` (formula, thresholds, trend rule) and
  `README.md` (the status line that quotes the four scores).
- `pipelines/chaos-test.ixql`, `policies/chaos-test-policy.yaml`, `schemas/chaos-test.schema.json`: the files that hold
  the injections. They are pinned by blob id and not parsed.

## Observed, computed, synthetic

- **Observed:** `observed` in `results.json` (cycles, status counts, injection names, what each record says was
  changed, the two reports, the definitions, the second series).
- **Computed from the observed counts:** `intervals`, `step_tests`, `multiplicity`, `paired`, `one_step_or_three`,
  `sensitivity`, `negative_controls`, `worked_answers`, and `transfer_task` (the red-team series).
- **Synthetic:** `synthetic` (a fifth cycle and held-out injection sets that do not exist) and the assumed fixed
  rates in `one_step_or_three`.
- **Cited:** PSY-002's regime names in `scenarios.json`, and the committer date of the pinned commit, used once to
  count the days since the last cycle.

## Methods

- Interval: Clopper-Pearson, binomial tails summed with fractions, each bound found by 60 bisection steps.
- Two counts: Fisher's exact test with both margins fixed. The two-sided p-value is the total probability of the
  tables no more probable than the observed one; the one-sided value is also stored.
- Several counts: the same conditional distribution over all tables with the observed total (Freeman-Halton test of
  one common rate; exact Cochran-Armitage trend test with scores 0, 1, 2, ...).
- Paired results: exact sign test on the injections whose result changed (the exact form of McNemar's test).
- Multiple comparisons: Bonferroni and Holm adjustments for a family of four comparisons declared in
  `scenarios.json`, and for the same family without "first against last". `multiplicity` enumerates every way to
  place the recorded catches among the trials and counts how often the family gives at least one p-value below the
  threshold, which accounts for the tests sharing counts.

## Self-checks

`analyze.py` aborts instead of writing a result when one of its 63 checks fails; `results.json` lists them under
`checks` with the number of times each was evaluated. They include accounting identities (caught + missed = total,
per-level counts add up, every probability list sums to 1), cross-checks between files (the report of `chaos-003`
has the statuses and counts of the history; the chaos-test report's table reproduces its scorecard), closed forms
(`1 - 0.025^(1/n)` for 0 of n), bounds (Bonferroni keeps the enumerated family-wise rate at or below 0.05), and cases
worked by hand:

```text
Fisher's tea-tasting table, 3 of 4 right:      17/70 one-sided, 34/70 two-sided
0 of 11 against 7 of 11:                       C(15,11) / C(22,11) = 1365 / 705432 one-sided, twice that two-sided
Holm on (0.01, 0.04, 0.03):                    (0.03, 0.06, 0.06)
sign test, 7 changes all one way:              1/128 one-sided, 1/64 two-sided
trend rule on (0, 0.64, 0.73, 0.60):           degrading
```

Four results could pass on nothing: "the injection names are identical in all cycles", "no injection went from
caught back to missed", "no set of status labels reproduces all four recorded counts" and "every recorded score is
the rounded share". `negative_controls` plants a renamed injection, a regression, a corrected count and a wrong score
in copies of the history and confirms that each counter moves; a fifth control lowers the last score and confirms
that the trend rule stops saying "improving".

## Limits

- The fixture reads the project's records of the cycles. It runs no detector and replays no injection. The parser the
  records name is in this repository, at `tools/ixql-parser/IxqlParser/Parser.fs`: at the pinned commit it defines
  `analyzeLolli`, `detectOrphanedBranches`, `detectUnreachable` and `validateTeachTargets`, the four functions of the
  `expected_detector` fields. It was not built or run here, and `extract.py` does not pin it. What the records place
  in another repository is the multi-file scanner that the two injections no cycle catches (L0, L1) would need.
- The binomial model behind every interval and test treats the eleven injections as independent draws with one
  detection rate. They were written by hand, several share a detector, and from the second cycle on they were scored
  after fixes aimed at them. `sensitivity` shows how the conclusions move with the unit (levels), with the count of
  the second cycle (7 recorded, 6 by status, 5 by level scores) and with the baseline (0, 5 or 9 of 11).
- The rule "caught = automated or policy-enforceable" is stated by the report of `chaos-003` only. For the other
  cycles it is an analysis choice, and it does not reproduce the recorded count of `chaos-002`.
- The reading of the trend rule for a cycle with fewer than two predecessors is this fixture's, not the policy's.
- The family of four comparisons was fixed before any p-value was computed and after the four scores had been read.
  The smaller family of three was added once the p-values were known, to show that the count of comparisons decides
  the paired reading of the first step.
