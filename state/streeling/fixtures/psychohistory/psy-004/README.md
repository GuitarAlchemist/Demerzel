# PSY-004 fixture: an aggregate of fourteen, with and without a shared cause

The two programs, `extract.py` and `analyze.py`, live in `scripts/streeling_fixtures/psychohistory/psy-004/` because this repository keeps executable code under `scripts/`; the data files they read and write are in this folder.

Fixture for the lesson `state/streeling/courses/psychohistory/en/psy-004-how-large-is-large.md`.
Python 3.9 or later, standard library only. Random numbers come from `random.Random(seed)` with the eight seeds stored
in `scenarios.json` (one per correlation for each of the two simulations).

## Files

| File | Kind | What it is |
|---|---|---|
| `extract.py` | script | Reads the Psychohistory department record, the 17 persona files, the 5 council verdicts, the council verdict schema and the two files that define the tribunal panel, checks their shape and their Git blob ids, looks for tribunal verdicts, and writes `observed-input.json`. |
| `observed-input.json` | observed | Snapshot at Demerzel commit `4b03838800dcd4894f1e026461979bff1d985ca8`: the record's key principle and consumer repos, each persona file's name, version and top-level key names, each council review's reviewer role and pass/fail answer, the schema's limit on reviews per verdict, the tribunal panel (its 5 personas, the answers each may return, what every persona is sent, the `--model` argument of the run, the workflow's comment on failed runs, and the 0 verdict files found), and the counts made by `extract.py`. |
| `scenarios.json` | assumed | Group sizes, the confidence level, the shared-cause model and its correlations, the simulation size and seeds, the second model, the log lengths of the measurement plan, the sizing for a group of the panel's size, the imaginary cases and the inputs of the learner transfer task. Nothing in it is measured in the repository. |
| `analyze.py` | script | Reads only `observed-input.json` and `scenarios.json`, runs the self-checks and writes `results.json`. |
| `results.json` | computed | Every number used by the lesson, the review brief and the transfer task. |

## Regenerate

From the repository root:

```text
python -I -B scripts/streeling_fixtures/psychohistory/psy-004/extract.py
python -I -B scripts/streeling_fixtures/psychohistory/psy-004/analyze.py
python -I -B scripts/streeling_fixtures/psychohistory/psy-004/analyze.py --check
```

`extract.py` takes under a second and `analyze.py` a few seconds. `analyze.py` writes the same bytes on every run (LF
line endings, `indent=2`, insertion-ordered keys; probabilities, shares, variances and interval bounds rounded to
6 decimals, sizes and ratios to 3, differences in standard errors to 2). `--check` recomputes the results and
compares them with the saved file, ignoring only CRLF against LF.

`extract.py` stops with exit code 1 when a source file is missing, when `personas/` or `state/council/` holds an
unexpected entry, when a record lacks a key, when a line of the panel's list cannot be read, when a file is not the
blob of the pinned commit (a new persona file is enough), or when `state/quality/verdicts/` holds a file (the pinned
commit has no such folder). `--allow-drift` snapshots the newer files anyway and records `"commit": null`; the
lesson's numbers then no longer apply, and `analyze.py` refuses a snapshot that holds a tribunal verdict, because it
would not read it.

## Observed, computed, synthetic

- **Observed:** everything in `observed-input.json`, and `observed` in `results.json` (recounted from the snapshot
  through a second code path).
- **Computed from assumed inputs:** `independent_agents` (exact Clopper-Pearson intervals, by summing binomial terms
  and bisecting), the formulas for the design effect and the effective sample size in `shared_cause`, and
  `imaginary_cases.precision_target.exact_binomial_check` (the exact binomial share of occasions on which 1 to 1,000
  independent agents land within 5 points of 0.5, against the 385 of the normal approximation).
- **Synthetic:** `shared_cause` (the copy model: its exact distribution as a mixture of two binomials, and a seeded
  simulation of 50,000 occasions per correlation), `second_model` (a beta-binomial model with the same correlations,
  in exact fractions), `measurement_plan` (the simulated occasions cut into logs of 20 and of 100),
  `tribunal_panel_sizing` (the copy model, a second seeded simulation of 200,000 occasions per correlation and the
  same logs, for 5 agents), `imaginary_cases` and `transfer_task`. Observed numbers enter these sections in two
  places: `shared_cause.stated_personas_against_persona_files` evaluates the assumed model at 14 and at 17 agents,
  and `tribunal_panel_sizing` takes its group size, 5, from the panel in the snapshot. Nothing else in them is
  observed.

## Self-checks

`analyze.py` aborts instead of writing a result when one of its 64 checks fails; `results.json` lists them under
`checks` with the number of times each was evaluated. They include:

- hand-computed cases: 1 yes of 2 gives the interval `1 - sqrt(0.975)` to `sqrt(0.975)`; the recurrence reproduces
  `C(14, k) / 2^14`; 14 agents at correlation 0.3 are worth `14 / 4.9 = 20/7`; two agents who always agree give a
  correlation estimate of 1, two who never agree, -1; five agents at p = 1/2 all agree with probability
  `(1 + 10 rho + 5 rho^2) / 16`; 20 independent agents at p = 1/2 land within 5 points on
  `(C(20, 9) + C(20, 10) + C(20, 11)) / 2^20` of occasions, and the exact share at 385 agents equals the sum of
  the binomial terms computed by recurrence;
- closed forms: the all-yes lower bound `0.025^(1/n)`, the no-yes upper bound, and the size of the unanimous group
  that reaches a lower bound of 0.95;
- known answers: correlation 0 reproduces the binomial variance `p(1-p)/n`; the second model at correlation 1/3
  gives each of the 15 counts the probability 1/15; in both models the variance of the share equals
  `p(1-p)/n * (1 + (n-1) rho)` (to 1e-12 for the first, exactly for the second);
- coverage: the exact interval for 14 agents contains the yes probability at least 95% of the time at each of 99
  grid points;
- simulation against exact values: mean, variance and four tail shares within 4 standard errors, for each seed of
  the 14-agent simulation; mean, variance and the share of unanimous occasions for each seed of the 5-agent one;
- the snapshot: every count of `extract.py` is recounted, the panel's 5 personas each have a persona file, the
  folder searched for tribunal verdicts lies in a folder that exists, and the workflow's comment on failed runs,
  which the lesson quotes, still says that the lane never produced a verdict;
- platform safety: no stored float lies within 1e-6 of a rounding boundary (in units of its last digit), and no
  comparison between computed numbers is decided by less than 1e-9. Exact fractions are rounded exactly.

Three results could pass on nothing; each has a negative control recorded under `negative_controls`: a planted
review by a persona moves the count of such reviews from 0 to 1; the Wald interval fails the coverage test that the
exact interval passes (97 of 99 grid points below 95%); a simulation with correlation 0.3 scored against correlation
0 is rejected by the agreement test (644 standard errors).

The results were compared byte for byte between CPython 3.9, 3.12 and 3.14 on Windows and CPython 3.14 on Linux
(glibc) when the fixture was written.

## Limits

- No file in the snapshot records a decision by a persona. The persona files' top-level keys are listed (16 names
  such as `role`, `capabilities`, `constraints` and `voice`); their values are not read. The council verdicts are 9
  reviews by two reviewer roles on one pull request; they are counted, not modelled.
- The tribunal panel is described from the text of its two files, by regular expressions written for those files at
  the pinned commit; this fixture did not run it. A comment in the workflow file, stored in `observed-input.json`,
  says that the workflow was "observed failing on every sibling-pr-opened dispatch" and that "this lane silently
  never produced a verdict" without the `id-token: write` permission. The file grants that permission at the pin,
  and nothing in the files read shows a successful run: no verdict is stored at the pin. How the run's `--model`
  argument reaches each persona was not established. "0 verdict files" describes the checkout that `extract.py`
  reads; a verdict kept only as a workflow artifact on GitHub would not be seen.
- `tribunal_panel_sizing` reduces the panel's three answers to two and treats its five personas as exchangeable,
  although the script gives each a concern of its own. Only the group size comes from the repository.
- The two generating models, the yes probability of 0.5 and the correlations 0, 0.1, 0.3 and 0.6 are assumptions.
  The design effect and the effective sample size depend only on the pairwise correlation; the tail probabilities
  (unanimity, coverage of the interval that assumes independence) depend on the model, as `second_model` shows.
- Agents are exchangeable: one yes probability and one pairwise correlation for all. Real agents need not be.
- The thresholds and detection shares of `measurement_plan` come from 2,500 (or 500) simulated logs per
  correlation, those of `tribunal_panel_sizing` from 10,000 (or 2,000). They carry that sampling noise, and the
  noise of a threshold that is itself estimated: each share is also stored for the two halves of its logs, each
  half with its own threshold, and the halves differ by up to 0.0144 for 14 agents and 0.031 for 5. A first
  version of the panel sizing, on 50,000 occasions, gave 40.3% where 200,000 occasions give 36.1% (5 agents, logs
  of 20, correlation 0.1). All of them hold at a yes probability of 0.5.
- The number of persona files at the commit that added the department record (14) was read from Git history and is
  not part of this fixture.
