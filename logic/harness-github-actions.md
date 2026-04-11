# Harness Adapter Projection — GitHub Actions

**Status:** Version 1.0, 2026-04-11.
**Scope:** Projection rules for GitHub Actions workflow run
summaries into `HexObservation` records.
**Implementation:** `ix/crates/ix-harness-github-actions`.
**Tier:** Tier 0 for first-party repos (we control the workflow
definitions). Becomes Tier 3 when consuming workflow runs from
external repos — blocked on the signature layer for that use case.
**Companion:** `harness-cargo.md` and `harness-clippy.md`
(sibling evidential adapters).

## Why GitHub Actions needs its own adapter

GitHub Actions is the CI substrate for most of our repos. A
workflow run produces:

- Per-job pass/fail status
- Per-step duration and exit codes
- Aggregate run conclusion (success / failure / cancelled / etc.)

These signals are structurally similar to cargo test events —
discrete pass/fail outcomes — but they operate at a higher
abstraction level (jobs ~ test suites, runs ~ full project
health). An Actions-specific adapter makes the distinction
explicit in the claim_key vocabulary.

## Input shape

The adapter accepts a single workflow run summary JSON. The
canonical source is the GitHub REST API:

```text
GET /repos/{owner}/{repo}/actions/runs/{run_id}
```

Relevant fields:

```json
{
  "id": 123456789,
  "name": "CI",
  "head_branch": "main",
  "head_sha": "abc123",
  "status": "completed",
  "conclusion": "success" | "failure" | "cancelled" | "skipped" | "timed_out" | null,
  "workflow_id": 42,
  "run_number": 100,
  "run_attempt": 1,
  "jobs_url": "https://api.github.com/.../jobs",
  "created_at": "2026-04-11T12:00:00Z",
  "updated_at": "2026-04-11T12:05:00Z"
}
```

And the per-job data (fetched separately via `jobs_url`):

```json
{
  "jobs": [
    {
      "id": 111,
      "name": "build",
      "status": "completed",
      "conclusion": "success",
      "started_at": "...",
      "completed_at": "...",
      "steps": [
        { "name": "Checkout", "status": "completed", "conclusion": "success", "number": 1, "started_at": "...", "completed_at": "..." }
      ]
    }
  ]
}
```

**For MVP, the adapter accepts a combined JSON shape** with both
the run summary and the jobs array inline:

```json
{
  "run": { /* workflow run fields */ },
  "jobs": [ /* per-job objects */ ]
}
```

Callers assemble this from two API calls. A future enhancement
could fetch from the API directly, but that ties the adapter to
a specific HTTP client / auth model; keeping it offline is
simpler and matches the cargo/clippy pattern.

## Output shape

All observations carry:
- `source = "github-actions"`
- `diagnosis_id = sha256(input)`
- `round` — caller-supplied

## Rules

### Rule 1 — Run-level reliability baseline

Emit one observation on `<workflow_name>_run::reliable`:

| `run.conclusion` | Variant | Weight |
|---|---|---|
| `success` | T | 0.9 |
| `failure` | F | 1.0 |
| `cancelled` | U | 0.4 |
| `skipped` | U | 0.3 |
| `timed_out` | F | 0.9 |
| `startup_failure` | F | 1.0 |
| null / missing / unknown | U | 0.3 |

The claim_key uses the workflow name (sanitized) so workflows
for different pipelines don't collide.

### Rule 2 — Per-job value observations

For each job with `status == "completed"`:

| `job.conclusion` | claim_key | Variant | Weight |
|---|---|---|---|
| `success` | `ci_job:<job_name>::valuable` | T | 0.85 |
| `failure` | `ci_job:<job_name>::valuable` | F | 1.0 |
| `cancelled` | `ci_job:<job_name>::valuable` | U | 0.4 |
| `skipped` | skipped (no observation) | — | — |
| `timed_out` | `ci_job:<job_name>::timely` | F | 0.9 |

Rationale: a cancelled job is low-signal (human intervention);
a skipped job is zero-signal. A timed-out job is more
informative than a plain failure because it tells us about
*time* rather than *correctness*.

### Rule 3 — Slow job timely flag

For each job, if `completed_at - started_at > 600 seconds`
(10 minutes), emit an additional observation:

- `ci_job:<job_name>::timely = D, weight 0.6`

Rationale: a slow job isn't wrong, but it drags the feedback
loop. Same logic as cargo's slow-test rule.

### Rule 4 — Step failures

For each step where `conclusion == "failure"`:

- `ci_step:<job_name>/<step_name>::valuable = F, weight 0.9`

This provides finer-grained signal than the job-level observation
for post-mortem analysis. Weight is slightly lower than the job-
level weight because the step event is subsumed by the job's
failure — we don't want to double-count.

## What the adapter does NOT emit

- No observations for `status == "queued"` or `"in_progress"`
  (not terminal)
- No observations for step counts / durations beyond the slow
  flag (would be noise)
- No observations for `run.actor`, `head_sha`, or any PII-
  adjacent fields
- No observations for artifact sizes / download counts
- No observations for workflow_dispatch inputs or environment
  secrets (obvious privacy)

## Sanitization

- Workflow names and job names may contain spaces, punctuation,
  and unicode. The adapter sanitizes to lowercase ASCII
  alphanumerics + underscores for claim_key embedding.
- Step names can contain `::` — we use `rfind` on the claim_key
  anyway, so step names pass through untouched.

## Worked example

Input:

```json
{
  "run": {
    "name": "CI",
    "conclusion": "failure",
    "run_number": 100
  },
  "jobs": [
    {
      "name": "build",
      "status": "completed",
      "conclusion": "success",
      "started_at": "2026-04-11T12:00:00Z",
      "completed_at": "2026-04-11T12:02:00Z",
      "steps": []
    },
    {
      "name": "test",
      "status": "completed",
      "conclusion": "failure",
      "started_at": "2026-04-11T12:02:10Z",
      "completed_at": "2026-04-11T12:14:30Z",
      "steps": [
        { "name": "Run tests", "conclusion": "failure" }
      ]
    }
  ]
}
```

Expected observations:

```jsonl
{"kind":"observation_added","ordinal":0,"source":"github-actions","claim_key":"ci_run::reliable","variant":"F","weight":1.0,...}
{"kind":"observation_added","ordinal":1,"source":"github-actions","claim_key":"ci_job:build::valuable","variant":"T","weight":0.85,...}
{"kind":"observation_added","ordinal":2,"source":"github-actions","claim_key":"ci_job:test::valuable","variant":"F","weight":1.0,...}
{"kind":"observation_added","ordinal":3,"source":"github-actions","claim_key":"ci_job:test::timely","variant":"D","weight":0.6,...}
{"kind":"observation_added","ordinal":4,"source":"github-actions","claim_key":"ci_step:test/run_tests::valuable","variant":"F","weight":0.9,...}
```

Note: the `ci_run` claim uses the sanitized workflow name as the
target, so a repo running multiple workflows gets distinct
reliable observations.

## Tier implications

**First-party (own repo):** Tier 0. We control the workflow
definitions and the token used to fetch run data. No signing
required.

**Second-party (upstream dependency's CI runs):** Tier 2. The
adapter is still first-party (we wrote it), but we're consuming
output from a workflow we don't control. Needs the signature
layer — specifically, the adapter should sign observations on
behalf of the upstream source after validating the input came
from the real GitHub API (token-authenticated fetch).

**External (untrusted webhook payloads):** Tier 3. Full signing
+ verification. Out of scope until the signature layer ships.

## Version

1.0 — 2026-04-11 — initial GitHub Actions projection spec.
Run-level reliability, per-job value, slow-job timely, and
step-level failure granularity. Combined run+jobs input shape
for MVP; API-direct fetch deferred.
