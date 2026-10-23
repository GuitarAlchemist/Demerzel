# PSY-024 fixture: who the recorded activity is attributed to

The two programs, `extract.py` and `analyze.py`, live in `scripts/streeling_fixtures/psychohistory/psy-024/` because this repository keeps executable code under `scripts/`; the data files they read and write are in this folder.

Fixture for the lesson `state/streeling/courses/psychohistory/en/psy-024-the-single-actor.md`.
Python 3.9 or later, standard library only, plus a `git` executable for `extract.py`.

## Files

| File | Kind | What it is |
|---|---|---|
| `extract.py` | script | Reads the trigger folders, seven files that say what the identities are, and the commit history of the pinned commit; replaces every identity by a label; writes `observed-input.json`. |
| `observed-input.json` | observed | Snapshot at Demerzel commit `4b03838800dcd4894f1e026461979bff1d985ca8`: counts per label, never a name. |
| `scenarios.json` | assumed | The imaginary ensembles, the cases that give the deleted files a sender, the simulation's seed, the thresholds of the hypothesis, the assumption behind the bound on the workflow's pushes, the inputs of the exercises and of the learner transfer task. Nothing in it is measured. |
| `analyze.py` | script | Reads only `observed-input.json` and `scenarios.json`, computes the concentration index and the effective number for each record, runs the self-checks and writes `results.json`. |
| `results.json` | computed | Every number used by the lesson, the review brief and the transfer task. |

## Regenerate

From the repository root:

```text
python -I -B scripts/streeling_fixtures/psychohistory/psy-024/extract.py
python -I -B scripts/streeling_fixtures/psychohistory/psy-024/analyze.py
python -I -B scripts/streeling_fixtures/psychohistory/psy-024/analyze.py --check
```

The three commands take about three seconds together. Both scripts write the same bytes on every run (LF line
endings, `indent=2`, insertion-ordered keys; shares and indices to 6 decimals, effective numbers and relative spreads
to 4, percentages to 2). Shares and indices are exact fractions until they are written. The simulation uses
`random.Random(seed).random()`, additions, multiplications and one division; the relative spread uses one correctly
rounded square root. `--check` compares a fresh run with the saved file, ignoring only CRLF against LF.

## No identity is stored

The subject of this module is who did what, so no file of the fixture holds a person's name, an account name, a
handle or an e-mail address. `extract.py` replaces each distinct raw value by a label before anything is written:

| Label | Stands for |
|---|---|
| `account A` | a value of the `sender` field of a trigger file (a platform username) |
| `author A`, `author B` | an author name in the commit history (a string configured in the committing tool) |
| `address A01`, `address A02`, `address B01` | an author e-mail address; the letter is the author's |
| `committer X01` | a committer name that is not also an author name |
| `co-author 01` to `co-author 12` | a name in a `Co-authored-by` trailer; the one trailer name identical to the sender (4 lines) takes the label `account A` instead |
| `domain D01` to `domain D03` | the part of a trailer address after the at sign |

Labels go by descending count; ties are broken by the SHA-256 of the raw value, which is not stored. The word
"automation" enters a label only when the raw name ends in `[bot]`. Two roles are stated because a pinned file lets a
reader verify them without this fixture naming anyone: account A is the only owner listed in `.github/CODEOWNERS`,
which calls that owner the maintainer, and author B is the name that four workflow files configure with
`git config user.name` before they commit. The script compares the strings and stores only the result.

Before it writes, `extract.py` searches its own output for every raw identity string it read (25 of them, the names
in `.mailmap` included) and stops if one is found; a planted string shows that the search can fail. Two strings are exempt because they cannot be told
apart from public names of things: one author string is identical to the repository's name, and one committer string
to the hosting platform's name. `analyze.py` adds a coarser check: no at sign in either input file.

To see the raw values, run the commands below in your own clone. They are public repository data; the fixture simply
does not copy them.

## Git commands

`extract.py` calls git with an argument list (no shell), names the pinned commit in every command and never `HEAD`,
and sets `GIT_NO_LAZY_FETCH=1`, so that a partial clone fails instead of downloading a blob. The commands read commit
objects and trees only (tested with Git 2.45.1):

```text
git rev-parse --is-shallow-repository
git cat-file -e 4b03838800dcd4894f1e026461979bff1d985ca8^{commit}
git rev-list --count 4b03838800dcd4894f1e026461979bff1d985ca8
git log --format=<hash, parents, author name and address, committer name and address, date, subject, Co-authored-by trailers> 4b03838800dcd4894f1e026461979bff1d985ca8
git shortlog -sn 4b03838800dcd4894f1e026461979bff1d985ca8
git log --no-renames --name-status --format=<hash> 4b03838800dcd4894f1e026461979bff1d985ca8 -- state/triggers/
git log --format=<hash, committer date, subject> <last commit with the trigger subject>..4b03838800dcd4894f1e026461979bff1d985ca8 -- .github/workflows/demerzel-driver-triggers.yml
```

The exact format strings are recorded in `observed-input.json` under `source.git_history.commands`. `git shortlog`
is a cross-check: its counts must equal the counts by author name from `git log`. Author names and addresses are read
raw (`%an`, `%ae`); the repository's `.mailmap` is parsed separately, to see how many identities each author string
becomes once it is applied.

`extract.py` exits with code 1 and a message when a file is missing or malformed, when the archive differs from the
pinned folder (594 files, Git tree id, manifest SHA-256, the same three values as the other trigger-log modules), when
another file differs from its pinned Git blob, when git is missing, the clone is shallow or the pin does not resolve,
or when the number of commits reachable from the pin is not 1,599. `--allow-drift` snapshots anyway and records
`"commit": null`; `analyze.py` then refuses the snapshot.

## Observed, computed, synthetic

- **Observed:** everything in `observed-input.json`. In `results.json`: `observed_senders`, the accounting part of
  `survivor_set`, and the counts in `commit_authors`.
- **Computed from the observed counts:** the indices in `observed_senders`, `commit_authors.readings` and
  `records_compared`, and `hypothesis_test`.
- **Computed under an assumption stored in `scenarios.json`:** `workflow_pushes`, the lower bound on the workflow's
  pushes that started no run (613 pushes, 214 `push` triggers ever written, so at least 399, if every run that a push
  started wrote one push trigger).
- **Assumption applied to observed counts:** `survivor_set.archive_plus_the_absent_files` and
  `survivor_set.every_readable_event_plus_the_absent_files` give the twelve deleted files a sender by assumption.
- **Synthetic:** `synthetic_ensembles`, `aggregate_simulation`, `worked_examples.exercise_2`, `exercise_5` and
  `spread_targets`, and `transfer_task` (a hypothetical release tracker).

## Self-checks

`analyze.py` aborts instead of writing a result when one of its 37 checks fails; `results.json` lists them under
`checks`. One is a partition of a single list of names, which holds by construction and only guards the code
(trigger files ever added = 615 events + 1 schedule definition; events = present at the pin + absent). The others
could fail: the events present by the history against the files read at the pin; files written by the workflow =
archived + left outside the archive + absent, in total and per event type; one commit with the trigger subject per
such file; commit groups, authors, addresses and committers each sum to 1,599; trailer lines counted two ways; the
known answers (k equal actors give H = 1/k and N = k; one actor gives 1 and 1); and three cases worked by hand:

```text
counts 3, 1        H = 9/16 + 1/16 = 5/8    N = 8/5    half-coverage count 1
counts 1, 1, 1, 1  H = 4 x 1/16 = 1/4       N = 4      half-coverage count 3
counts 50, 50      H = 1/2                  N = 2      half-coverage count 2 (exactly half is not more than half)
```

Results that could pass on nothing have a negative control, recorded in `results.json`:

- "one sender": moving one archived event to a planted second sender gives two senders and N = 1.0034.
- "0 mismatches between the commit subject and the file" (602 files): one planted wrong subject gives 1 mismatch.
- "no identity string in the output": a planted string is found; a planted at sign is counted.

## Limits

- The record resolves accounts and author strings. It cannot say how many people, sessions or agents acted under
  one of them, and the fixture does not join the two records: a platform username and a commit author string are
  different identifiers.
- The content of the twelve deleted trigger files is not available in a blobless clone; their senders are unknown.
  What is recorded for them comes from commit subjects and trees. Eleven were added by commits with the trigger
  subject; the twelfth, a `self_initiated` trigger and not a repository event, by another commit under author A's
  string, whose subject reports the driver's first autonomous cycle.
- The trigger workflow is read as it stands at the pin. Two changes reached the file after the last commit with the
  trigger subject (`trigger_log.producer.versions` in `observed-input.json`); earlier versions were not read. Its
  commit template ends in `[skip ci]`, which none of the 613 trigger subjects carries.
- A trigger file's name and its commit subject are written from one variable of one workflow step: their agreement
  shows that each run committed only its own file, not that two independent records agree.
- The bound on the workflow's pushes assumes that every run a push started wrote one push trigger; a run that failed
  before its commit would break it.
- "Written by the trigger workflow" means: added by a commit whose author string is the one the workflow configures
  and whose subject fits the workflow's template. Anyone can configure that string; the fixture cannot check that
  each such commit came from a workflow run.
- The classes of commit subject (the trigger template, a subject ending with a pull-request number, other) are
  analysis choices. A subject that ends with a pull-request number is not shown to be a squash merge; 9 of the 279
  are merge commits.
- Co-author trailers are counted as written. Their names are neither classified nor authenticated.
- The synthetic ensembles and the simulation assume independent actors with equal variability. Nothing in them
  measures the project.
