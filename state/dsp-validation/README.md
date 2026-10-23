# DSP Validation Records

Audit trail for `scripts/validate_dsp_loop.py` — one record per run (Asimov Article 7,
Auditability; policy `recursive-learning-eval`).

## File Naming

```
dsp-validation-{run_id}.json      # run_id is a compact UTC timestamp, e.g. 20260729T042317Z
```

## Why this exists

The loop's only prior persistence was `.tmp/dsp_validation/parameter_cache.json`: a single
`safe_distortion` float, in a gitignored scratch directory, with no timestamp, no bounds
provenance, and no record of which cycles were actually run. It was simultaneously the
performance cache *and* a silent control input for the next run's search space — so a
parameter the loop discovered on its own altered its own future behavior with no trace.

These records separate the two concerns. The cache stays a convenience; the record is the
evidence.

## Governance fields

| Field | Meaning |
|---|---|
| `recursion_depth` | Always `0` — this is base validation, not learning evaluation. Schema rejects `> 2`. |
| `article_4_check` | Always `understanding`. The loop measures and proposes; it never rewrites `logic/dsp-safety-bounds.yaml`. |
| `requires_authorization` | Always `true`. A validated parameter is a proposal until a human enacts it. |
| `warm_started` | Whether `--use-cached-bounds` authorized the previous run's value to narrow the search. |
| `cached_value_seen` | The cached value the run observed, *whether or not it was enacted*. Makes the Article 9 boundary auditable: `cached_value_seen` set with `warm_started: false` is the compliant default. |
| `validated_this_run` | `null` unless a cycle in **this** run passed consensus. Never seeded from cache. |
| `aborted_reason` | `compilation_error` / `telemetry_error` / `null`. Any non-null value means nothing was validated and the run exits non-zero. |

## Tracked?

The JSON records are gitignored, following the precedent set by
`state/oversight/ml-recommendations/` — reproducible runtime I/O produced fresh each run,
not canonical governance state. This README is tracked as the seam documentation.
