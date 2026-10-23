# Streeling course fixtures: programs

Programs that produce the reproducible evidence of Streeling course modules. They live here because `CONTRIBUTING.md`
keeps executable code under `scripts/`. The data they read and write stays with the course material:

| Programs | Data |
|---|---|
| `scripts/streeling_fixtures/<department>/<module>/` | `state/streeling/fixtures/<department>/<module>/` |

Each module folder holds `analyze.py` and, when the module uses observed repository data, `extract.py`. The data
folder holds `scenarios.json`, `results.json`, `README.md` and, with an extract, `observed-input.json`. The data
folder's `README.md` documents the module's inputs, self-checks and limits.

## Running one

From the repository root, Python 3.9 or later, standard library only:

```text
python -I -B scripts/streeling_fixtures/psychohistory/psy-005/analyze.py --check
```

- `analyze.py` recomputes `results.json` from `scenarios.json` and, where present, `observed-input.json`. `--check`
  compares a fresh run with the saved file and writes nothing; `--output <file>` writes elsewhere.
- `extract.py` rereads the observed files and rewrites `observed-input.json`. It pins each source by Git blob id and
  refuses to run when a source has changed since the module was written, which is the expected outcome once a nightly
  job has appended rows. `analyze.py` reads only the saved snapshot, so it keeps working.

Before a module is merged its programs are rerun on Windows and on Linux, on Python 3.9, 3.12 and 3.14, and the saved
bytes must not change. macOS has not been tried.

## What CI checks

`scripts/test_streeling_fixtures.py` runs with the other `scripts/` unit tests. It checks that every program compiles
and that its data folder holds the files above. It does not rerun the analyses, some of which take half a minute. To
rerun them all:

```text
STREELING_FIXTURE_CHECK=1 python -m unittest discover -s scripts -p 'test_streeling_fixtures.py'
```

The programs find the repository root from their own location instead of importing `demerzel_kit`: they are run with
`python -I`, which keeps `scripts/` off the import path, so that a result depends on nothing but the program and its
data.
