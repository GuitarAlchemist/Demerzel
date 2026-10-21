# PSY-025 fixture: a forecast record, its validator and its scorer

The two programs, `extract.py` and `analyze.py`, live in `scripts/streeling_fixtures/psychohistory/psy-025/` because this repository keeps executable code under `scripts/`; the data files they read and write are in this folder.

Fixture for the lesson `state/streeling/courses/psychohistory/en/psy-025-capstone-preregistered-forecast.md`.
Python 3.9 or later, standard library only. No random number is drawn, so there is no seed.

## Files

| File | Kind | What it is |
|---|---|---|
| `extract.py` | script | Reads the commit history of `state/streeling/courses` (commits and trees only) and every file of that folder at the pin, checks the history against embedded constants and each file against its pinned Git blob, and writes `observed-input.json`. |
| `observed-input.json` | observed | Snapshot at Demerzel commit `4b03838800dcd4894f1e026461979bff1d985ca8`: the 53 commits that changed the set of English module files (time, modules added, modules removed), and one line per library file (255) with the `module_id` and `department` of its front matter. |
| `scenarios.json` | hand-written | Four forecast records (two worked, one flawed draft, one repair), the rules each must fail, changed copies used as controls, INVENTED outcomes, two INVENTED file layouts, the window length, and the inputs of the learner task. Nothing in it is measured. |
| `analyze.py` | script | Reads only the two JSON files, applies the counting rule to the pinned library, computes the base rates, validates the records, scores them, runs the self-checks and writes `results.json`. |
| `results.json` | computed | Every number used by the lesson, the review brief and the transfer task. |

The module names no governance artifact, so no data label needed the spaced-slash form that other modules use to
stay out of `scripts/evolution_metrics.py`'s citation count.

## Regenerate

From the repository root:

```text
python -I -B scripts/streeling_fixtures/psychohistory/psy-025/extract.py
python -I -B scripts/streeling_fixtures/psychohistory/psy-025/analyze.py
python -I -B scripts/streeling_fixtures/psychohistory/psy-025/analyze.py --check
```

Each command takes a few seconds. `extract.py` needs a clone with the full commit history (a blobless partial clone
is enough; it never downloads an object) and the pinned files in the working tree. It stops with exit code 1 when
the clone is shallow, the pin is missing, the commit count (1,599 reachable, 73 touching the folder), the SHA-256 of
those 73 commit ids or the folder's tree id differ from the constants, when the replayed file list differs from the
pinned tree, or when a file differs from its pinned blob. `--allow-drift` records drifted files anyway, and
`analyze.py` then refuses to run. The manifest digest of the 255 files can be reproduced with
`git ls-tree -r 4b03838800dcd4894f1e026461979bff1d985ca8 -- state/streeling/courses | awk '{print $3" "$4}' | sha256sum`
(`57f10ef77065c108f5c08bb23a4f0c76b6420b3604f6aeb0a675487abcf9b33e`).

`analyze.py` computes with exact fractions and rounds when it writes: probabilities, rates and scores to 6
decimals, interval ends to 4, days to 3. It writes the same bytes on every run (LF, `indent=2`, insertion-ordered
keys); `--check` compares a fresh run with the saved file.

## Observed, computed, hand-written

- **Observed:** the commit times and module paths of the history, and the front matter of the 255 files at the pin.
- **Computed from the observed data:** `observed` (counts under three counting rules) and `base_rate` (reference
  classes over 92-day windows, exact 95% intervals, the alignment table) in `results.json`.
- **Hand-written:** the records, their verdicts and scores (`validation`, `scoring`), `exercises` and
  `transfer_task`. The outcomes scored there are INVENTED; the real outcome of the worked records is unknown until
  2027-01-13T23:59:59Z. The worked records are exercises in writing a forecast, not commitments of the department
  and not predictions it endorses.

## Field rules of a forecast record

`analyze.py` checks each record against these rules and prints the message of every rule it fails. A rule that
compares two fields is reported as "not judged" when one of them is unusable.

- R01 `id` is a non-empty string not used by an earlier record. Message: `id: missing or not unique`
- R02 `question` ends with a question mark. Message: `question: not phrased as a question`
- R03 `kind` is `probability` or `interval`. Message: `kind: must be 'probability' or 'interval'`
- R04 `resolution_source.repository` has the form owner/name. Message: `resolution_source: no repository named as owner/name`
- R05 `resolution_source.branch` is not empty. Message: `resolution_source: no branch named`
- R06 `resolution_source.commit_rule` is not empty. Message: `resolution_source: does not say which commit is read`
- R07 `resolution_time` has the form YYYY-MM-DDTHH:MM:SSZ. Message: `resolution_time: not a UTC timestamp`
- R08 `resolution_time` is later than `written_at`. Message: `resolution_time: not later than written_at`
- R09 `resolution_rule.counts`, `.unit` and `.excluded` are not empty. Message: `resolution_rule: does not say what counts, how often, and what does not`
- R10 `resolution_rule.if_moved` is not empty. Message: `resolution_rule: no rule for a moved or renamed source`
- R11 `resolution_rule.void_if` is not empty. Message: `resolution_rule: no condition under which the forecast is void`
- R12 `reference_class` is not empty. Message: `reference_class: missing`
- R13 `base_rate` holds integers with 0 <= events <= trials and trials >= 1. Message: `base_rate: missing, or not a count of events among trials`
- R14 `base_rate.command` is not empty and `base_rate.commit` is a 40-character commit id. Message: `base_rate: no command and pinned commit to recompute it`
- R15 `forecast` is a probability `p` from 0 to 1, or `lower` <= `upper` with 0 < `coverage` < 1. Message: `forecast: not a number the score can use (...)`
- R16 `reference_forecast` has the forecast's form; a reference probability equals events / trials to 6 decimals; a reference interval has the forecast's coverage. Message: `reference_forecast: missing, of another form, or not the base rate`
- R17 `adjustment` is not empty whenever the forecast differs from its reference. Message: `adjustment: the forecast departs from its reference without a stated reason`
- R18 `falsifier.statement` is not empty. Message: `falsifier: no statement of the outcome that counts against the forecast`
- R19 `falsifier.outcomes` (inclusive ranges) are exactly the outcomes at which the forecast scores worse than its reference. Message: `falsifier: the stated outcomes are not those where the forecast scores worse than its reference`
- R20 `author_can_influence_outcome` is `false`. Message: `author_can_influence_outcome: true or not stated (...)`. The author is whoever writes the record, and R20 judges nobody else: the maintainers who would merge a record also decide which modules of every department are merged, which the record discloses in `author_influence_note` (not checked).
- R21 `written_at` has the form YYYY-MM-DDTHH:MM:SSZ. Message: `written_at: not a UTC timestamp`
- R22 `written_at_evidence` is not empty. Message: `written_at_evidence: does not say what, beyond the author's word, dates the record`

The rules check that a field is present and well formed, and two of them (R16, R19) check that fields agree. No
rule can tell whether a resolution rule is clear: that is the reviewer's job, helped by the invented layouts below.

## Scores

- Brier score of one probability forecast p for outcome o (0 or 1): `(p - o)^2` (PSY-016). Skill, as in PSY-016:
  `1 - BS / BS_ref`, BS_ref the reference's Brier score on the same outcomes, computed from unrounded scores; it is
  undefined (`null` in `results.json`) when the reference makes no error, as a base rate of 0 events does at outcome 0.
- Interval score of a central (1 - alpha) interval [l, u] for outcome x, from Gneiting and Raftery (2007), eq. 43:
  `(u - l) + (2 / alpha) (l - x) [x < l] + (2 / alpha) (x - u) [x > u]`. Lower is better. The worked interval
  [19, 25] is an 80% interval by its stated level (alpha = 0.2): 19 is its author's 0.1 quantile and 25 is at or
  above the 0.9 quantile; with 0.3 on 19 itself, its author's own probability that it covers is at least 0.3 + 0.7 x 6/7 = 0.9
  (`scoring.music_count_coverage_under_author_beliefs`).
- Falsifying outcomes: probability, outcomes 0 and 1; interval, counts from 0 to the larger upper end plus 2
  (beyond both intervals the difference between the two scores no longer depends on x).

## Counting rule and base rate

- A file's module id is its front matter's `module_id`, or its file name without `.md` and without a two-letter
  language suffix; its department is its front matter's `department`, or the nearest folder above it that is not a
  two-letter language folder; only `.md` files count, `README.md` and `index.md` excluded; each (department, module id) counts once.
- The history counts paths `<department>/en/<name>.md` (not README.md), because the blobless clone holds no old file
  contents. At the pin both counts give 68 modules and agree in all 18 departments.
- Windows: 92 days, back to back, ending at the pinned commit, as many as fit after the first module commit (two).
  A department is a trial when it holds at least one module at the window's start; an event when its count at the
  end is higher. The alignment table repeats this with the end moved back 0 to 22 days, and lists the alignments at
  which the broad rate is below the 0.1 that the research cycle's hypothesis expected (10 of the 23).

## Self-checks and negative controls

`analyze.py` aborts instead of writing when one of its 22 checks fails; `results.json` lists them under `checks`.
They include the history replayed to the pin against the pinned tree, the counting rule against the path count,
known answers (each record fails exactly the rules listed in `scenarios.json`; the exact interval for 2 of 6 equals
PSY-017's; for 1 of 2 it is [1 - sqrt(0.975), sqrt(0.975)]; each invented layout gives its expected count; a
hand-computed Brier and interval score), the agreement between the records and the computed base rate, and the
agreement between the interval record's stated beliefs and the probability record (0.3 on 19 = 1 - 0.7).
Negative controls: seven changed copies of the worked records must fail exactly the expected rule (or pass, for the
copy whose forecast equals its reference); a planted Music addition must move each reference class by one; a planted
French file without an English module must be found; a reference that makes no error must leave skill undefined.
Their results are in `results.json`.

## Limits

- The base rate rests on two windows of a bursty history; the alignment table shows how much it moves. Its exact
  interval treats the 36 department-windows as independent, while both rises fall in one window and one burst, so it
  understates the uncertainty.
- The front matter of old files is not read (no blobs in the clone), so the history cannot test the counting rule
  before the pin.
- The validator checks form, not clarity, and the worked forecasts' probabilities are the author's judgment.
