# PSY-020 fixture: a citation count that cannot tell use from mention

The two programs, `extract.py` and `analyze.py`, live in `scripts/streeling_fixtures/psychohistory/psy-020/` because this repository keeps executable code under `scripts/`; the data files they read and write are in this folder.

Fixture for the lesson `state/streeling/courses/psychohistory/en/psy-020-goodhart-and-reflexivity.md`.
Python 3.9 or later, standard library only. `extract.py` also needs the `git` command; `analyze.py` does not.

## Files

| File | Kind | What it is |
|---|---|---|
| `extract.py` | script | Lists the 2,062 files of Demerzel commit `4b03838800dcd4894f1e026461979bff1d985ca8`, reads their pinned bytes, applies the counting rule of `scripts/evolution_metrics.py` to them and writes `observed-input.json`. |
| `observed-input.json` | observed | The snapshot: the 19 citation paths, the 18 evolution records with their recorded and recounted `citation_count`, the 202 files that contain a citation path (with the paths each contains, as letters), the rows of the quality trend whose `delta_citations` is not 0, the quoted lines of the producer, the feeder, the anti-LOLLI policy, the power-law detection rule and the compounding-metrics policy with their line numbers, and four planted controls. |
| `scenarios.json` | assumed | Written by hand: the toy tree of Exercise 1, the what-if additions, the readings of the power-law rule, the effort model (yields, reward weights, seed), the reflexive forecast, the threshold of the hypothesis and the inputs of the learner transfer task. Nothing in it is measured in the repository. |
| `analyze.py` | script | Reads only `observed-input.json` and `scenarios.json`, recounts every count from the file table, runs the self-checks and writes `results.json`. |
| `results.json` | computed | Every number used by the lesson, the review brief and the transfer task. |

Artifact names, citation paths and the paths of the files found by the search are written with a space on each side
of every slash (`policies / alignment-policy.yaml`): `scripts/evolution_metrics.py` counts every tracked file that
contains an artifact's path as a citation of that artifact, and a data file about the artifacts is not one. For the
same reason neither program contains a citation path: `extract.py` builds them from the evolution records at run
time, `analyze.py` removes the spaces in memory only, and both refuse to write an output that contains one. The
compounding-metrics policy is both a file read by name and a citation path: `extract.py` takes its path from the
evolution records and writes it spaced, in `source` as everywhere else.

## Regenerate

From the repository root:

```text
python -I -B scripts/streeling_fixtures/psychohistory/psy-020/extract.py
python -I -B scripts/streeling_fixtures/psychohistory/psy-020/analyze.py
python -I -B scripts/streeling_fixtures/psychohistory/psy-020/analyze.py --check
```

Each program finishes in a few seconds. Both write the same bytes on every run (LF line
endings, `indent=2`, insertion-ordered keys; shares, means and correlations rounded to 4 decimals, percentages to 2,
from exact fractions rounded half up). `--check` recomputes the results and compares them with the saved file,
ignoring only CRLF against LF.

**How the pinned files are read.** The counting rule searches every tracked file, so the source is the whole tree
and not a handful of files. `extract.py` embeds one manifest digest instead of 2,062 blob ids: the SHA-256 of the
lines `<blob id> <path>`, which a reviewer reproduces with

```text
git ls-tree -r 4b03838800dcd4894f1e026461979bff1d985ca8 | awk '{print $3" "$4}' | sha256sum
```

It also embeds the Git tree id of the commit, and both are recorded in `observed-input.json` under `source` with the
blob ids of the 29 files read by name. Each file is read from the working tree and its blob id recomputed from its
bytes; a file that is missing or different there (a later checkout, a regenerated backlog) is read from Git's object
store by its pinned blob id. The snapshot is therefore that of the pinned commit whatever the checkout holds, and
there is no `--allow-drift` option. `extract.py` stops with exit code 1 when Git is absent or cannot list the pinned
commit, when the tree id or the manifest differs, when a pinned blob cannot be read (a partial clone is not allowed
to download it silently), when a record or a trend row has an unexpected shape, or when a quoted line is no longer
found exactly once.

## Observed, computed, synthetic

- **Observed:** everything in `observed-input.json`. Its counts are a recount made with a reimplementation of the
  producer's rule (literal byte search, the four exclusion pathspecs, the artifact's own files removed); on the
  pinned tree the recount equals the recorded `citation_count` for 16 of 16 measurable artifacts.
- **Computed from the observed data:** `observed_rule`, `observed_counts`, `observed_mentions`,
  `observed_trend_rows` and `observed_decision_rules` in `results.json`, and in `power_law_rule` the share that the
  top 20% of artifacts hold, computed from the recorded `citation_count` of the 18 evolution records (the rule's own
  data source), rounding 3.6 artifacts both down (3) and up (4).
- **Synthetic:** `toy_rule` (an invented tree), `what_if` (files that do not exist, added to the observed counts),
  the added files of `power_law_rule` (the fewest files, each naming the citation paths of the measurable leaders,
  that would take the share above 60%, and one catalogue of every path),
  `effort_model` (assumed agents; 300 enumerated cases, and a sample of 400 drawn with `random.Random(20201013)`),
  `reflexive_forecast` (assumed reactions, starting from one observed count), `hypothesis_parts` and
  `transfer_task` (a hypothetical wiki).

## Self-checks and negative controls

`analyze.py` aborts instead of writing a result when one of its 25 checks fails; `results.json` lists them under
`checks`. They include a second recount of the 16 counts from the file table, the accounting identities (tracked =
excluded + searched; counts by artifact = counts by file; a row's `delta_citations` = its count minus the previous
one; the 18 recorded counts sum to the latest run of the quality trend), the number of files that flips the
detection rule against its closed form, the closed forms of the effort model when the whole reward is on the proxy, the geometric error of a revised
forecast, and a tree counted by hand:

```text
a  docs/index.md             names the path                 counted
b  scripts/check.py          joins "toy" and "rule.yaml"    not counted (and the only file that uses the rule)
c  the rule file itself      names its own path             not counted (own file)
d  state/evolution/toy.json  names the path                 not counted (excluded folder)
e  notes/archived/2025.md    names the path                 not counted (excluded folder)
f  data/labels.json          spaced label                   not counted
g, h  a lesson and its translation                          counted          -> count 3
```

Results that could pass on nothing have a control. `extract.py` plants one file that lists every citation path in
the pinned tree and recounts: 16 counts rise by 1; the same file in an excluded folder, under a folder named
`archived`, or written with spaced labels raises 0 counts, and no pinned file contains a spaced label. `analyze.py`
removes one file from the table (the recount of 44 becomes 43 and no longer equals the record), swaps two counts
(29 order relations change, against 0 when nothing is added) and spaces one mention in the toy tree (3 becomes 2).

## Limits

- A count is a number of files that contain a string. Nothing here classifies a file as a use or a mention of the
  artifact; the lesson says so and names that classification as its next check.
- The recount covers one commit. The history of the counts comes from the quality-trend rows as recorded, and no
  cause is attributed to any change.
- The what-if cases add files to observed counts; none of these files exists. The reading of the policy's ratio in
  `what_if.policy_cycles` is an assumption stated in `scenarios.json`; the lesson does not use it, the review brief
  does.
- The power-law rule says "the top 20% of governance artifacts", and 20% of 18 is 3.6: both whole readings are
  given, and both are below 60% at the pin. Its population keeps the recorded counts of the two artifacts that
  cannot be measured here, as the rule's data source does. The comparison with the counts typed by hand before
  2026-09-13 belongs to PSY-007 and is not computed here.
- The effort model and the reflexive forecast are assumed mechanisms with invented numbers. Nobody's effort was
  observed, and nothing here shows that anyone inflated a count.
- Two artifacts have an empty `citation_paths` list and cannot be measured in this repository; they are listed and
  left out of every recount.
