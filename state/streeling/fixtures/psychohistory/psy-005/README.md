# PSY-005 fixture: the persistence baseline on effectiveness labels

The two programs, `extract.py` and `analyze.py`, live in `scripts/streeling_fixtures/psychohistory/psy-005/` because this repository keeps executable code under `scripts/`; the data files they read and write are in this folder.

Fixture for the lesson `state/streeling/courses/psychohistory/en/psy-005-persistence-baseline.md`.
Python 3, standard library only. No random number is drawn, so there is no seed.

## Files

| File | Kind | What it is |
|---|---|---|
| `extract.py` | script | Reads `state/quality-trend/*.jsonl` and the evolution record of each artifact whose label changed, checks their shape and their Git blob ids, and writes `observed-input.json`. |
| `observed-input.json` | observed | Snapshot at Demerzel commit `4b03838800dcd4894f1e026461979bff1d985ca8`: the 88 run timestamps, and for each of the 18 artifacts three strings with one character per run (`effectiveness_from`, `effectiveness_to`, the `baseline` flag), plus the counts made by `extract.py`. |
| `scenarios.json` | assumed and cited | The four imaginary forecasters, the cost ratios, the extrapolation targets, Finley's 1884 table (cited) and the inputs of the learner transfer task. Nothing in it is measured in the repository. |
| `analyze.py` | script | Reads only `observed-input.json` and `scenarios.json`, recounts everything from the strings, runs the self-checks and writes `results.json`. |
| `results.json` | computed | Every number used by the lesson, the review brief and the transfer task. |

Artifact names are written with a space on each side of every slash (`policies / alignment-policy.yaml`):
`scripts/evolution_metrics.py` counts every tracked file that contains an artifact's path as a citation of that
artifact, and a data file about the artifacts is not one.

## Regenerate

From the repository root:

```text
python -I scripts/streeling_fixtures/psychohistory/psy-005/extract.py
python -I scripts/streeling_fixtures/psychohistory/psy-005/analyze.py
python -I scripts/streeling_fixtures/psychohistory/psy-005/analyze.py --check
```

Each command finishes in about a second. `analyze.py` writes the same bytes on every run (LF line endings, `indent=2`,
insertion-ordered keys, ratios rounded to 6 decimals, percentages to 2, days to 3). `--check` recomputes the results
and compares them with the saved file, ignoring only CRLF against LF, because a Windows checkout with
`core.autocrlf=true` stores CRLF in the working tree.

`extract.py` stops with exit code 1 when a source file is missing, when a row lacks a key, has an unknown label, a
malformed timestamp or a duplicate (timestamp, artifact), or when a source file is not the blob of the pinned commit
(the nightly feeder appends rows, so this happens on any later checkout). `--allow-drift` snapshots newer data anyway
and records `"commit": null`; the lesson's numbers then no longer apply.

## Observed, computed, synthetic

- **Observed:** the labels, timestamps and `baseline` flags in `observed-input.json`, and the event list of
  `state/evolution/2026-03-20-autonomous-driver.evolution.json`.
- **Computed from the observed data:** `observed`, `forecast_unit`, `persistence`, `constant_label_forecasts`,
  `per_artifact`, `per_run` and `negative_controls` in `results.json`.
- **Synthetic:** `skill.candidates` and `skill.weighted_cost` (imaginary forecasters scored on the observed pairs),
  `extrapolation` (a constant-rate assumption) and `transfer_task` (a hypothetical registry).
- **Cited:** `cited_example_finley_1884`, from the table published by the WWRP/WGNE Joint Working Group on Forecast
  Verification Research.

## Self-checks

`analyze.py` aborts instead of writing a result when one of its 26 checks fails; `results.json` lists them under
`checks`. They include a recount of every count made by `extract.py` through a second code path, the accounting
identities (rows minus artifacts = row pairs; changed + unchanged = usable pairs; per-artifact, per-run and
per-horizon sums = totals; label shares sum to 1), the identity between the two forms of the skill score, and a case
worked by hand:

```text
runs       1 2 3 4
a   to     T T F F     3 pairs: T-T, T-F, F-F -> 1 changed
b   to     . P - P     2 row pairs, both touch the missing label -> 0 usable pairs
rows 7, row pairs 5, usable pairs 3, changed 1, persistence accuracy 2/3
```

Two results could pass on nothing: "0 changes between feeder runs" and "0 rows whose `effectiveness_from` differs
from the previous `effectiveness_to`". The negative controls plant one flipped label in a copy of the snapshot and
confirm that both counters move (changed pairs 1 to 3, between feeder runs 0 to 2, mismatches 0 to 1), then blank
one label and confirm that two usable pairs disappear (1,529 to 1,527).

## Limits

- The snapshot keeps labels, timestamps and the `baseline` flag only; citation counts and rebaseline flags are left
  to other modules.
- The reason a label is missing is derived from the row's position and from reading `scripts/quality_trend.py`; the
  content of the evolution records at earlier commits is not part of the fixture.
- One label change in 1,529 pairs: every ratio that involves it rests on a single event.
- The imaginary forecasters are defined by their error counts. No model was trained or run.
