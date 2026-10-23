# PSY-006 fixture: a transition matrix from label counts

The two programs, `extract.py` and `analyze.py`, live in `scripts/streeling_fixtures/psychohistory/psy-006/` because this repository keeps executable code under `scripts/`; the data files they read and write are in this folder.

Fixture for the lesson `state/streeling/courses/psychohistory/en/psy-006-transition-matrix-from-counts.md`.
Python 3.9 or later, standard library only (run on Windows under 3.9, 3.12 and 3.14: same bytes). No random number is
drawn, so there is no seed.

## Files

| File | Kind | What it is |
|---|---|---|
| `extract.py` | script | Reads the five `state/quality-trend/*.jsonl` files, `state/markov/transition-matrix.json` and `predictions.json`, the state table and four lines of `docs/specs/governance-markov-simulation.md`, and the `belief_hexavalent` machine of `state/driver/transition-weights.json`; checks their shape and their Git blob ids; writes `observed-input.json`. |
| `observed-input.json` | observed | Snapshot at Demerzel commit `4b03838800dcd4894f1e026461979bff1d985ca8`: the 88 run timestamps; for each of the 18 artifacts two strings with one character per run (`effectiveness_to` and the `baseline` flag); the counts made by `extract.py`; the stored governance matrix, its prediction list, the file names in `state/markov/` and the specification lines; the seed table over the six labels. |
| `scenarios.json` | assumed | Every analysis choice: the confidence level, the grid on which a bound is located, the pseudo-counts, the questions put to the stored matrix, the imaginary "sticky" matrix, the assumption under which the seed table is confronted with the counts, and the inputs of the learner transfer task. Nothing in it is measured in the repository. |
| `analyze.py` | script | Reads only `observed-input.json` and `scenarios.json`, recounts the pairs from the strings, runs the self-checks and writes `results.json`. |
| `results.json` | computed | Every number used by the lesson, the review brief and the transfer task. |

Artifact names are data labels: `extract.py` writes each one with a space on each side of every slash
(`policies / alignment-policy.yaml`), because `scripts/evolution_metrics.py` counts as a citation of an artifact every
tracked file that contains the artifact's path as a literal string, and a data file must not raise those counts.

## Regenerate

From the repository root:

```text
python -I -B scripts/streeling_fixtures/psychohistory/psy-006/extract.py
python -I -B scripts/streeling_fixtures/psychohistory/psy-006/analyze.py
python -I -B scripts/streeling_fixtures/psychohistory/psy-006/analyze.py --check
```

Each command finishes in a few seconds. `analyze.py` writes the same bytes on every run (LF line endings,
`indent=2`, insertion-ordered keys). `--check` recomputes the results and compares them with the saved file, ignoring
only CRLF against LF, because a Windows checkout with `core.autocrlf=true` stores CRLF in the working tree.

`extract.py` stops with exit code 1 when a source file is missing; when a row lacks a key, has an unknown label, a
malformed timestamp or a duplicate (timestamp, artifact); when the stored matrix is not square, the specification
lacks one of the expected lines or the seed table is not over the six labels; and when a source file is not the blob
of the pinned commit or `state/markov/` holds other file names than at the pin (the nightly feeder appends rows, so
this happens on any later checkout). `--allow-drift` snapshots newer data anyway and records `"commit": null`; the
lesson's numbers then no longer apply.

## How the numbers are made

- **Counts and ratios** are integers and exact fractions (`fractions.Fraction`). A stored `value` is the fraction
  rounded half to even to 6 decimals, a `percent` to 3 decimals; `exact` is the unrounded fraction.
- **Bounds.** The upper bound for x events in n trials is the solution p of `P(X <= x | n, p) = 0.05`, the largest
  probability that the count does not reject at the 5% level (one-sided; for x = 0 it is `1 - 0.05^(1/n)`).
  `analyze.py` locates it between two neighbouring points of a grid of 10^9 steps by comparing integers
  (`sum C(n,i) k^i (10^9 - k)^(n-i)` against `10^(9n) / 20`), then rounds. `located` records the two grid points. No
  stored digit of a bound depends on `pow`, `exp` or `log` of a C library.
- **Chains.** Stationary distributions and expected hitting times are linear solves in exact fractions; "within t
  cycles" is t exact matrix-vector products.
- **Two logarithms** come from the `decimal` module at 40 digits, which rounds `ln` correctly: `-ln 0.05`, stored to
  4 decimals, and the specification's `log(0.5) / log(0.75)`, stored to 3 decimals and bracketed by an integer
  comparison (`0.75^4817 > 0.5^2000 > 0.75^4819`).

## Observed, computed, synthetic

- **Observed:** the labels, timestamps and `baseline` flags; the stored matrix, its note, the empty prediction list
  and the absence of `engine-state.json`; the specification's state table, freeze formula, alert rule and uniform
  initialisation; the weights and the `forbidden` list of the seed table.
- **Computed from the observed data:** `observed`, `count_matrix`, `maximum_likelihood`, `bounds`, the rows of
  `smoothing` (under a chosen pseudo-count), `stored_governance_model.as_a_chain` and `negative_controls` in
  `results.json`.
- **Computed under a stated assumption:** `belief_seed_table.between_feeder_runs` and `.from_a_seed_row` assume that
  one step of the seed table is one consecutive-row pair. The repository does not say how long a step is.
- **Synthetic:** `sticky_alternative` (an imaginary matrix), `bounds.rule_of_three_against_exact` (imaginary sample
  sizes), `stored_governance_model.what_observations_would_do` (cycles nobody has recorded) and `transfer_task` (a
  hypothetical status log).

## Self-checks

`analyze.py` aborts instead of writing a result when one of its 47 checks fails; `results.json` lists them under
`checks`. They include a recount of every count made by `extract.py` through a second code path, the accounting
identities (rows minus artifacts = row pairs; row totals and column totals both sum to the pairs; the two subsets'
matrices add up to the matrix of all pairs), rows of every estimated, smoothed or stored matrix summing to 1, the
stationary distribution satisfying its equation, closed forms for the uniform matrix (`1 - 0.75^t`, a geometric wait
of 4), and cases worked by hand:

```text
runs       1 2 3 4
a   to     T T F F     3 pairs: T>T, T>F, F>F
b   to     . P - P     2 row pairs, both touch the missing label -> 0 usable pairs
rows 7, row pairs 5, usable pairs 3; estimate T>T 1/2, T>F 1/2, F>F 1; P, U, D and C have no row
add-one over six labels, row T: (1+1)/(2+6) = 2/8 to T, 2/8 to F, 1/8 to each other label

0 events in 1 trial: 1 - p = 0.05           -> bound 0.95 (exactly on the grid)
0 events in 2 trials: (1 - p)^2 = 0.05      -> bound 1 - sqrt(0.05) = 0.776393
1 event in 2 trials: 1 - p^2 = 0.05         -> bound sqrt(0.95) = 0.974679

chain [[9/10, 1/10], [1/2, 1/2]]: stationary (5/6, 1/6); 10 steps expected from the first state to the second;
second state within two steps with probability 1 - 0.9^2 = 19/100
```

Three results could pass on nothing: "label D never occurs", "four rows have no exit" and "no `engine-state.json`
in the folder". The negative controls plant one D in the middle of an all-T history in a copy of the snapshot and
confirm that D gets a row and a column, that T leaves the list of rows without an exit, that the changed pairs go from
1 to 3 and that one exit in 775 pairs raises the bound from 0.003858 to 0.006106. The file-presence test that finds
no `engine-state.json` finds `transition-matrix.json` in the same listing.

## Limits

- A bound assumes that the trials it counts are independent and share one probability. The pairs are consecutive
  rows of 18 artifacts over the same runs, and a label changes only when its evolution record is edited, so the
  trials may be fewer than the pairs. Two other trial units give the extremes: `bounds.one_trial_per_run`, where the
  labels of a run change together or not at all (86 steps, bound 3.423% per pair against 0.197%), and
  `bounds.per_artifact_over_the_record`, where an artifact's label is one assessment kept through the record (T: 0 of
  9 artifacts left it, bound 28.313% over the whole record; F and C: one artifact each, bound 95%). The data cannot
  place the truth.
- Bounds are one-sided (PSY-004 and PSY-013 use the two-sided interval, 0.025 in each tail) and computed one row at a
  time; nothing is adjusted for looking at several rows.
- The 1,529 pairs mix two step lengths: 1,518 pairs between feeder runs (gaps of 0.001 to 6.453 days, median 0.999)
  and 11 pairs of 78.5 days from a seed row. The matrices are given for all pairs and for each subset.
- The label alphabet (T, P, U, D, F, C) and the governance states (Healthy, Watch, Warning, Freeze) are different
  state spaces. The specification classifies a governance cycle from a resilience score and a LOLLI/ERGOL ratio
  alone; no label enters that classification.
- The seed table is declared for beliefs and gives no step length; the comparison with the counts holds only under
  the stated assumption.
- No governance state is recorded at the pin and the prediction list is empty, so nothing about the stored 4-state
  matrix is tested. The classifier's inputs were recorded a few times (four resilience scores in
  `state/resilience/history.json`, one ratio in `state/driver/lolli-ergol-history.json`); they were not classified.
