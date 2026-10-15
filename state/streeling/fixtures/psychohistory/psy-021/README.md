# PSY-021 fixture: conservation statements on the trigger log

The two programs, `extract.py` and `analyze.py`, live in `scripts/streeling_fixtures/psychohistory/psy-021/` because this repository keeps executable code under `scripts/`; the data files they read and write are in this folder.

Fixture for the lesson `state/streeling/courses/psychohistory/en/psy-021-conservation-claims.md`.
Python 3.9 or later, standard library only; `extract.py` also runs `git` (read-only commands). No random number is
drawn, so there is no seed.

## Files

| File | Kind | What it is |
|---|---|---|
| `extract.py` | script | Reads every file under `state/triggers/`, the add and delete records of that folder in the Git history of the pinned commit, and single sentences of five pinned files; checks shapes, Git tree ids, blob ids and commit counts; writes `observed-input.json`. |
| `observed-input.json` | observed | Snapshot at Demerzel commit `4b03838800dcd4894f1e026461979bff1d985ca8`, in three parts that are kept apart: `files` (603 event files by folder, one row each), `history` (615 event file names with their add and delete records, 623 commits) and `documents` (the quoted sentences). |
| `scenarios.json` | assumed | The four labels given to a statement, the author's reading of what Noether's theorem needs, five hand-written ledgers of eight imaginary events with the answers fixed in advance, an imaginary series of p_L, and the learner task (a parcel depot). Nothing in it is measured in the repository. |
| `analyze.py` | script | Reads only `observed-input.json` and `scenarios.json`. One function, `audit()`, compares a listing with a history of additions and deletions; it is applied to the observed log, to the hand-written cases, to the observed log with one planted error, and to the learner task. Writes `results.json`. |
| `results.json` | computed | Every number used by the lesson, the review brief and the transfer task. |

## Regenerate

From the repository root:

```text
python -I -B scripts/streeling_fixtures/psychohistory/psy-021/extract.py
python -I -B scripts/streeling_fixtures/psychohistory/psy-021/analyze.py
python -I -B scripts/streeling_fixtures/psychohistory/psy-021/analyze.py --check
```

`extract.py` takes a few seconds (six `git` commands and about 610 small files); `analyze.py` takes less than a
second and writes the same bytes on every run (LF line endings, `indent=2`, insertion-ordered keys; the only
non-integers are percentages of the files created, rounded to 2 decimals). `--check` recomputes the results and compares them with
the saved file, ignoring only CRLF against LF.

`extract.py` stops with exit code 1 when a trigger file has an unexpected name or shape, when `state/triggers/` is
not the folder of the pinned commit (Git tree ids of the folder and of its two sub-folders, file count and manifest
digest of `archived/`), when one of the five quoted files is not its pinned Git blob or a quoted sentence is not
found exactly once, when `git` is missing, when the pinned commit is not in the clone, when the clone is shallow,
or when the history has another number of commits than the pin (1,599 reachable, 1,528 on the first-parent chain,
623 of those touching the folder). `--allow-drift` snapshots anyway and records `"commit": null`; `analyze.py` then
refuses the snapshot.

The history is read with `git log --first-parent -m --no-renames --name-status` at the pinned commit (the exact
commands are in `observed-input.json` under `history.commands`). These commands need commits and trees only;
`extract.py` sets `GIT_NO_LAZY_FETCH=1`, so that in a partial clone a command that wanted an old file's content
would fail instead of downloading it.

## Observed, computed, synthetic

- **Observed, files at the pin:** `files` in `observed-input.json`; `files_at_the_pin` in `results.json`.
- **Observed, Git history up to the pin:** `history` in `observed-input.json`; `history_to_the_pin` in
  `results.json`. "Consumed" there means "deleted from `processing/`": it is a reading of the driver's own rule and of
  two commit subjects, because no file records processing.
- **Observed, quoted:** `documents` (PSY-001, the compounding-metrics policy, the file that policy names for
  tracking, the producer workflow, the driver's skill file). The paths are constants at the top of `extract.py`.
- **Computed:** `audit_of_the_observed_log` and the numbers of `claims`.
- **The author's judgement, labelled as such:** the kind given to each statement in `claims` and the three
  conditions under `learning_momentum.what_noether_s_theorem_needs`.
- **Synthetic:** `synthetic_controls` (eight imaginary events), `learning_momentum.testable_version` (six imaginary
  cycles) and `transfer_task` (a hypothetical parcel depot).

In the three JSON files the paths of the driver's skill file and of the compounding-metrics policy are written with
a space on each side of every slash: `scripts/evolution_metrics.py` counts every tracked file that contains a
governed artifact's path as a citation of it, and a data file must not be one.

## Self-checks and negative controls

`analyze.py` aborts instead of writing a result when one of its 21 checks fails; `results.json` lists them under
`checks`. They include a recount of the A and D records that `extract.py` counted, the margins of the two cross
tables, and the five hand-written cases, for example:

```text
history   e1..e6: +top, then -top +archived at commit 10     e7, e8: +top
listing   top: e7 e8        archived: e1 e3 e4 e5 e6 e7       (e2 lost, e7 copied)
answer    8 created, 8 listed, 0 removals on record: every count balances;
          e2 is expected and missing, e7 is listed in two folders
```

Several observed results are zeros that could pass on nothing (no file name in two folders, no repeated run id, no
folder out of balance). Four negative controls change a copy of the snapshot in one place and confirm that the
matching counter moves: a file dropped from the archive listing (archive balance 0 to -1, the file named as
missing), a pending file copied into the archive listing (names in two folders 0 to 1), a repeated run id (0 to 1),
and one deletion record erased from the history (removals on record 12 to 11, open-system difference 0 to 1).

## Recount without the scripts

```text
git ls-tree -r 4b03838800dcd4894f1e026461979bff1d985ca8 -- state/triggers/archived | wc -l          594
git ls-tree 4b03838800dcd4894f1e026461979bff1d985ca8 state/triggers/ | grep -c 'Z-'                 9
git log --first-parent -m --no-renames --name-status --format= 4b03838800dcd4894f1e026461979bff1d985ca8 -- state/triggers/ | grep -c '^A'      1217
(the same with '^D')                                                                                611
git log --first-parent --format=%s 4b03838800dcd4894f1e026461979bff1d985ca8 | grep -c '^trigger: '   613
```

1,217 additions are 615 created event files + 594 arrivals in `archived/` + 5 in `processing/` + 3 files that are
not events; 611 deletions are 599 moves + 12 removals.

## Limits

- "Created" means "committed on the main branch". A file that the producer workflow wrote and could not push never
  reached a commit; the repository holds no list of the workflow's runs.
- The balances between the files and the history (per folder, name by name, and the open-system identity) hold by
  construction: Git derives additions and deletions from consecutive snapshots, and the files are the last
  snapshot. They check that the history was read completely, not that the trigger system lost nothing.
- The producer workflow is quoted at the pin, a later version than the ones that wrote the triggers: it was edited
  after the last trigger commit (`git log --format='%h %cI %s' 4b03838800dcd4894f1e026461979bff1d985ca8 --
  .github/workflows/demerzel-driver-triggers.yml`), and its commit template ends with `[skip ci]`, which none of the
  613 producer subjects carries. Earlier versions were not read.
- Claim C9 (each producer commit added one file of the type its subject names) can fail, but the subject and the
  file name are written by one workflow step from one variable: it is not an independent count.
- Why a file was deleted is known only from the subject line of the deleting commit. The content of deleted files
  was not read (it would have to be downloaded from an old commit), so their type and date come from their names.
- The classification of statements and the reading of Noether's theorem are judgements about texts.
- `observed-input.json` is about 100 KB: the name-by-name comparison needs one row per event on each side.
