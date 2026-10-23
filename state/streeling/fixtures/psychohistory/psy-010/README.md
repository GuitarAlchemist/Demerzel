# PSY-010 fixture: growth curves on a short, step-like history

The two programs, `extract.py` and `analyze.py`, live in `scripts/streeling_fixtures/psychohistory/psy-010/` because this repository keeps executable code under `scripts/`; the data files they read and write are in this folder.

Fixture for the lesson `state/streeling/courses/psychohistory/en/psy-010-growth-curves-short-series.md`.
Python 3.9 or later, standard library only. `extract.py` also needs `git` and a clone with the full commit history
(a blobless partial clone is enough).

## Files

| File | Kind | What it is |
|---|---|---|
| `extract.py` | script | Asks git for the commits, among the ancestors of the pinned commit, that touched `state/streeling/courses`, replays the paths they added and deleted, counts the English modules at each commit and writes `observed-input.json`. Reads commits and trees only, never the content of a file. |
| `observed-input.json` | observed | Snapshot at Demerzel commit `4b03838800dcd4894f1e026461979bff1d985ca8`: the git commands, the 73 commits with their committer and author dates, the number of files and of English modules at each, the module names added and removed, the state of the folder at the pin and the names of the department records there. |
| `scenarios.json` | assumed | The plan's target of 525, the conventions (daily sampling, the half-module rule for "reaches", the 7-day burst rule, the other clocks, the two-minute window for the busiest day), the ceilings of the profile, the search settings, the burst scenarios, the seeds and shapes of the negative controls, and the inputs of the learner transfer task. Nothing in it is measured in the repository. |
| `analyze.py` | script | Reads only `observed-input.json` and `scenarios.json`, runs the self-checks and writes `results.json`. |
| `results.json` | computed | Every number used by the lesson, the review brief and the transfer task. |

## Regenerate

From the repository root:

```text
python -I scripts/streeling_fixtures/psychohistory/psy-010/extract.py
python -I scripts/streeling_fixtures/psychohistory/psy-010/analyze.py
python -I scripts/streeling_fixtures/psychohistory/psy-010/analyze.py --check
```

`extract.py` makes eleven git calls; `analyze.py` takes a few seconds. Both write the same bytes on
every run (LF line endings, `indent=2`, insertion-ordered keys). `--check` recomputes the results and compares them
with the saved file, ignoring only CRLF against LF. `extract.py --repo-root <clone>` reads another clone;
`--output` and, for `analyze.py`, `--input` and `--scenarios` redirect the files.

`extract.py` never reads `HEAD`: every command names the pinned commit, so the branch that is checked out does not
matter. It stops with exit code 1 and writes nothing when git is missing, the folder is not a repository, the clone
is shallow, the pinned commit is absent, or the history is not the pinned one. The constants it compares can be
checked by hand:

```text
git rev-list --count 4b03838800dcd4894f1e026461979bff1d985ca8                              1599
git rev-list --count 4b03838800dcd4894f1e026461979bff1d985ca8 -- state/streeling/courses   73
git rev-list --topo-order --reverse 4b03838800dcd4894f1e026461979bff1d985ca8 -- state/streeling/courses | sha256sum
                                    85f15934a53a7561afc81c28ead2122846f62e436983bb74e4a1cdb346877f98
git rev-parse 4b03838800dcd4894f1e026461979bff1d985ca8:state/streeling/courses             fc6abc23bd76b00ae37366ac6d9f70186573dd5d
```

It also refuses a history in which a side branch touched the folder, a listed commit is a merge, or committer
times decrease along the ancestry order, because the series would then not be a single dated line. The file list
rebuilt from the added and deleted paths must equal `git ls-tree` at the first listed commit and at the pin.

## What is counted

A module is a path `state/streeling/courses/<department>/en/<name>.md` whose name is not `README.md`. Not counted:
translations (`<department>/<other language>/`), README files, and the ten flat-layout path names of the first six
commits (two of them held the English text of the first two modules before the department folders existed).
Renaming a file counts as one removal and one addition. Department records are the files `state/streeling/departments/<name>.department.json` at the pin, read as names only. Dates are committer dates in UTC; commits that share a
second keep their ancestry order. The author date is recorded only to measure how far it differs.

## Observed, computed, synthetic

- **Observed:** everything in `observed-input.json`; `observed` in `results.json`.
- **Assumed:** `plan` (the target of 525 comes from a draft specification that is not on the master branch).
- **Computed from the observed data:** `series`, `bursts`, `fits`, `comparison`, `sensitivity`, `ceiling_profile`
  and `step_models`. The burst rule, the daily sampling and the half-module rule are conventions from `scenarios.json`.
- **Synthetic:** `burst_scenarios` (the future repeats the observed bursts: an assumption), `negative_controls`
  (seeded series with known answers) and `transfer_task` (a hypothetical songbook).

## Search, tolerance and rounding

The line is solved exactly with fractions. The exponential `a * exp(b * t)` and the logistic
`K / (1 + exp(-r * (t - m)))` with `K` fixed are fitted by least squares on the counts themselves (not on their
logarithms): a coarse grid gives the start, Gauss-Newton steps with step halving run until the residual sum stops
falling, and Newton steps with the exact second derivatives run until both parameters move by less than one part
in 10^12. A fit is rejected unless the residuals are orthogonal to both columns of the Jacobian within a cosine of
10^-9. A "free" ceiling is examined as a profile: the logistic is refitted with `K` fixed at twelve values.

Stored floats are rounded coarsely so that a last-bit difference in `exp` or `log` cannot change a digit: residual
sums to 1 decimal, fitted parameters to 6 significant digits, dates to the day. The saved `results.json` was
reproduced byte for byte under Python 3.9, 3.12 and 3.14 on Windows and under Python 3.14 on Linux.

## Self-checks and negative controls

`analyze.py` aborts instead of writing a result when one of its 39 checks fails; `results.json` lists them under
`checks`. They include a replay of the module names commit by commit, a second code path for the daily series and its UTC row among the other clocks, the
normal equations of every line fit in exact arithmetic, the stationarity test of every curve fit, the recovery of
a planted exponential and of a planted logistic, the dynamic-programming step fit against a brute-force search,
the definition of "reaches" on the day before and on the day itself, and two cases worked by hand:

```text
line through (0,0), (1,1), (2,1):  slope 1/2, intercept 1/6, residual sum 1/6
counts 2, 2, 5, 5, 5, 9:           active days 0, 2, 5; three bursts at a gap of 1 day, one at a gap of 3
```

Two results could pass on nothing. "The residuals change sign 3 times" would be unremarkable if any fit did that:
a seeded line with independent noise, fitted by a line, changes sign 107 times in 206 comparisons. "The ceiling
cannot be estimated" would be empty if the profile never found a ceiling: on a seeded logistic seen past its turn
it finds the planted 525 (residual sum 8,751.7 against 29,596.0 at 550), and on one seen before its turn it is
flat within 0.4%.

## Limits

- Three bursts and two pauses under the 7-day rule; the number of bursts runs from 6 to 2 as the rule goes from 1
  to 12 days. Days that start on five other clocks give 10 to 13 active days and the same three bursts. The last
  burst is still open at the pin, which itself adds a module: its size and span are lower bounds, and the burst
  scenarios that use its size are upper bounds. Every date in `fits` moves by years when one burst or one pause is left out.
- A commit date says when a file reached the history, not when it was written or reviewed; the content of the
  modules is not read, so "module" means a file name and nothing about quality.
- The fits weigh every day equally. `sensitivity` shows three other choices (active days only, logarithm of the
  counts, author dates); none is more correct than the lesson's.
- The burst scenarios and the transfer task are arithmetic on assumptions. Nothing here is a forecast.
