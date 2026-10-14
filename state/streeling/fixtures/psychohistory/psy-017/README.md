# PSY-017 fixture: calibration with six observations

The two programs, `extract.py` and `analyze.py`, live in `scripts/streeling_fixtures/psychohistory/psy-017/` because this repository keeps executable code under `scripts/`; the data files they read and write are in this folder.

Fixture for the lesson `state/streeling/courses/psychohistory/en/psy-017-calibration-with-six-observations.md`.
Python 3.9 or later, standard library only. Two seeds, stored in `scenarios.json`, drive the one simulation.

## Files

| File | Kind | What it is |
|---|---|---|
| `extract.py` | script | Reads the calibration belief, the 21 `*.belief.json` files of `state/beliefs/` and `state/beliefs/archived/`, the three files that state the nudge rule, and the two other files of those folders (the YAML list `3d-visualization-aesthetics.yaml` and the archive's `SUPERSEDED.md`); checks their shape and the Git blob ids of all 26; writes `observed-input.json`. |
| `observed-input.json` | observed | Snapshot at Demerzel commit `4b03838800dcd4894f1e026461979bff1d985ca8`: the calibration belief with its claim split into numbers, one row per belief file (truth value, confidence, last update), and the quoted lines of the policy, the pipeline specification and the applier script, with line numbers; the truth value and confidence of each belief in the YAML list, and two quoted lines of `SUPERSEDED.md`. |
| `scenarios.json` | assumed and cited | The assumed revision rates, the error rates of the decision rule, the simulation settings and seeds, the thresholds of the hypothesis, the inputs of the learner transfer task, and the counting rule and confidence formula **cited** from a script in another repository. Nothing in it is measured in the Demerzel repository. |
| `analyze.py` | script | Reads only `observed-input.json` and `scenarios.json`, runs the self-checks and writes `results.json`. |
| `results.json` | computed | Every number used by the lesson, the review brief and the transfer task. |

## Regenerate

From the repository root:

```text
python -I -B scripts/streeling_fixtures/psychohistory/psy-017/extract.py
python -I -B scripts/streeling_fixtures/psychohistory/psy-017/analyze.py
python -I -B scripts/streeling_fixtures/psychohistory/psy-017/analyze.py --check
```

`extract.py` takes under a second and `analyze.py` about three. `analyze.py` writes the same bytes on every run (LF
line endings, `indent=2`, insertion-ordered keys; probabilities rounded to 6 decimals, interval bounds, nudges and
ratios to 4, days and years to 1). `--check` recomputes the results and compares them with the saved file, ignoring
only CRLF against LF.

`extract.py` reads the 26 files from the tree of the pinned commit in Git's object store (it needs `git`), so any
clone that holds that commit gives the same snapshot, whatever its working tree holds: the applying script rewrites
the calibration belief each time it applies a threshold recommendation, so a later working tree is likely to differ.
It stops with exit code 1 when the clone does not hold the commit, when a source file is missing, when a belief file
lacks a key or holds an unexpected truth value or confidence, when the claim or one of the quoted rule lines no longer
has the expected wording, when a file is not the blob recorded for the pinned commit, or when one of the two belief
folders holds a `*.belief.json` file that the pinned commit does not have. `--allow-drift` reads the working tree
instead, snapshots newer files anyway and records `"commit": null`; the lesson's numbers then no longer apply, and
`analyze.py` refuses any snapshot whose commit is not the pinned one.

## Paths in the data files

In the three JSON files every path of this repository is written with a space on each side of each slash
(`state / beliefs / archived / ...`), and so are the slashes inside the propositions copied from the other belief
files. The repository's metrics producer sets a governance artifact's citation count to the number of tracked files
that contain its path as a literal string; written this way, a data file is never counted as a citation of the
pipeline specification or of the applying script that this fixture reads. `extract.py` converts when it writes the
snapshot and checks blob ids against the real paths; the source lines it quotes stay verbatim.

## Observed, computed, cited, synthetic

- **Observed:** everything in `observed-input.json`; in `results.json`, the section `record` and the file rows of
  `recount`.
- **Computed from the observed data:** `recount` (the claim's 2 and 6 recounted from the belief files),
  `exact_interval`, `nudge_rule.recorded_cycle_recomputed`,
  `negative_controls`, and
  `recount.not_read_by_the_producer`: the YAML list holds 19 beliefs, 9 at confidence 0.85 or more, which the
  producer's `*.belief.json` glob never counts (with them, 15 high-confidence beliefs would be on disk).
- **Cited, outside the pin:** the counting rule ("high-confidence" = every belief file, current or archived, with
  confidence at least 0.85; "revised" = the archived ones among them), the template of the claim and the formula
  `min(0.92, 0.70 + 0.02 x belief files read)` for the recommendation's confidence. They come from
  `scripts/confidence_calibrator.py` of the repository GuitarAlchemist/ix, read at commit
  `6418fcc69012108af266544ec4cf5a931a8f78e8` (Git blob `e875b4ce0831060b14029e71016dfe0acbc0fef2`). The fixture does
  not read that repository. What it can establish is narrower: applied to the pinned Demerzel files, the cited rule
  and template rebuild the recorded claim character for character, and the cited formula gives the recorded 0.92.
  The pinned applying script names that producer in its header (line 4) and copies the recommendation's confidence,
  rationale and message id into the belief (lines 134 to 140; the label P is fixed at line 133). The calibration
  belief is therefore a record of the producer's computation, not an assessment made in this repository, and the
  recount is that computation reproduced, not a second source. The same script writes a second belief file the same
  way (line 256), which is one of the six.
- **Computed under assumed rates:** `revisions_among_six`, `telling_two_rates_apart`, and the per-cycle
  probabilities of `nudge_rule`; `telling_two_rates_apart.at_the_recorded_pace` assumes that the six's pace holds
  and counts days both from the earliest of the six (2026-03-17) and from the record. The rates (15%, 10%, 5%, one third) and the wanted error rates are choices. The row
  `calibrated_at_each_stated_confidence` reads each file's confidence as a forecaster's own; two of the six are
  copied from recommendations, so the lesson does not use it.
- **Synthetic:** `nudge_over_cycles` (a forecaster with a fixed true rate who supplies six fresh beliefs per cycle;
  two of the four rules are hypothetical) and `transfer_task` (a hypothetical incident-review log).

## Method

- Binomial probabilities are exact: integers over a common denominator, turned into `fractions.Fraction`. No value of
  `pow`, `exp`, `log` or `lgamma` enters the output; two square roots (correctly rounded by IEEE 754) are stored to
  4 decimals.
- The exact (Clopper-Pearson) interval is found by bisection on the exact binomial tail, continued until both ends of
  the bracket round to the same 4 decimals, so the stored bound is the correctly rounded one.
- Sample size: for each n up to 400, the rule "c or more of n" with the smallest c whose false-alarm probability is
  within the limit; n qualifies when that rule's detection probability reaches the target. Because counts are whole
  numbers, a larger n can fail after a smaller one passes; both the smallest n and the n from which every sample up to
  400 passes are stored.
- The running total of the nudge is followed exactly (a small Markov chain over the possible totals) and by a seeded
  simulation of 20,000 runs of 52 cycles per forecaster, six `random.Random(seed).random()` draws per cycle. Totals
  are kept as integers in units of 1/120.

## Self-checks

`analyze.py` aborts instead of writing a result when one of its 32 checks fails; `results.json` lists them under
`checks`. Among them:

- the recount reproduces the claim's two counts, its two file names and its whole sentence;
- the producer named in the header of the pinned applying script is the script cited in `scenarios.json`, and the
  two belief files whose only evidence is a recommendation are the two that script writes;
- the pinned formula and clamp reproduce `threshold_nudge` and `applied_delta` from `prior_nudge`;
- the cap is the same number in the pipeline formula, the applier, the policy guardrail and the belief file;
- probabilities sum to 1 for every binomial used and at every cycle of the chain;
- a hand-computed case, `P(2 or more of 6 at 15%) = 1 - 0.85^6 - 6 x 0.15 x 0.85^5 = 0.223516`;
- known answers for the interval (1 of 1 starts at 0.025, 0 of 1 ends at 0.975) and for the chain (the total is
  still 0 after k cycles with probability `q0^k`);
- the flat-prior probability computed twice, by a binomial identity and by integrating the likelihood;
- the simulation against the exact chain (largest difference of a share 0.007234, tolerance 0.015).

Three results could pass on nothing; each has a negative control stored under `negative_controls`. A line that no
file reaches (0.96) leaves 0 high-confidence files, and a line of 0 counts all 21, so the counter is not stuck at 6.
Treating one current belief as archived changes the recount to 3 of 6 and the rebuilt sentence no longer equals the
record, so the "identical sentence" check can fail.

## Limits

- One record, one moment: the snapshot holds the belief files as they stood at the pinned commit. Earlier versions of
  the calibration belief, and the recommendation document it cites (a runtime file the repository ignores), are not
  part of the fixture.
- The counting rule is cited from another repository. The fixture shows that it reproduces the record; it does not
  show which version of that script ran. By that rule, the 19 beliefs of the YAML list are outside the count.
- "Calibrated" is the lesson's reading: revisions are treated as errors and a forecaster who states confidence c is
  wrong on a share 1 - c of such statements. The repository does not record whether a revised belief was wrong.
- Every probability assumes independent beliefs with one common rate. The six files are not that (two are written by
  the applying script from recommendations, and one shares its name, apart from the date, with an archived one), so the binomial figures are a
  best case for the data.
- The simulation feeds the rule six fresh beliefs per cycle. The recorded loop re-reads the same files; nothing here
  measures how the project's threshold moved over time.
