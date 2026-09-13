# Bounding event-supply retrieval without forgetting obligations

Status: partial — cost fuse shipped, the durable bound is designed but not built.
Issue: [#963](https://github.com/GuitarAlchemist/Demerzel/issues/963).
Follows: [#939](https://github.com/GuitarAlchemist/Demerzel/pull/939) (event-supply
evaluation for `cross-model-review.yml`).

## The problem

`default_event_supply_runner` in `scripts/ecosystem_freshness.py` evaluates the
event-triggered `cross-model-review.yml` loop by enumerating every pull request
updated since the **activation cutoff** and asking, per pull request, whether its
head SHA got a correlated run. The cutoff is immutable by design, so that set only
grows, and so does the request count.

## Measured baseline

Read-only measurement against `GuitarAlchemist/Demerzel` on the activation day
(2026-08-03, cutoff `2026-08-03T00:00:00Z`), issuing only authenticated `GET`s:

| Metric | Value |
|---|---|
| Obligations evaluated | 11 |
| GitHub requests | 22 |
| Wall clock | 10.9 s |
| Cost shape | `1 listing + ~2 requests per pull request` |

Observed velocity, same measurement: 59 pull requests touched in the trailing 7
days, 112 in 30 days, 201 in 90 days (204 in the whole archive).

Extrapolating at ~3.7 newly-relevant pull requests per day, the daily job reaches
GITHUB_TOKEN's 1,000 requests/hour/repository primary rate limit at roughly 500
accumulated pull requests — months, not years — where it would fail as an opaque
mid-retrieval HTTP 403. That is a nearer and less legible failure than the
`_MAX_SUPPLY_PAGES = 20` listing ceiling (~2,000 pull requests) named in the issue.

## Why the proposed formula is unsound

The issue proposes

```text
retrieval_floor = max(activation_cutoff, now - k * max_stale_days)
```

as a hypothesis. Applied to the pull listing, it is silent-green by construction.

The listing is filtered on `updated_at`. An obligation that is never answered —
head pushed, no run, PR then closed or abandoned — stops bumping `updated_at`. Its
verdict is correctly red today and stays red only because retrieval still reaches
it. Under a moving floor it drops out of retrieval on day `k * max_stale_days`, the
supply comes back empty, and the evaluator reports `quiet: no pull_request event
has occurred since the activation cutoff` — exit 0.

Spiked against the real adapter with `k = 3`, `max_stale_days = 3`, on a closed
pull request whose head never ran and whose last activity is 60 days old:

| | current | with retrieval floor |
|---|---|---|
| Obligations retrieved | 1 | 0 |
| Verdict | `silent_green` | `healthy` |
| Exit code | 1 | 0 |

This is exactly the erasure defect the guard was built to catch — the one
`state=all` and the pre-cutoff waiver machinery exist to prevent — reintroduced
through the retrieval boundary instead of the query filter.

`test_unanswered_obligation_survives_beyond_any_moving_horizon` in
`scripts/test_ecosystem_freshness.py` is the executable form of that invariant.
Any future bounding change must keep it green.

## Why no stateless bound exists

The sticky invariant is: an unanswered obligation stays red until a *correlated
terminal run* resolves it, however old it gets, including after closure or merge.

A stateless run knows only what it retrieves. To know an obligation of age `A`
exists, it must page back `A` worth of activity, because every GitHub listing is
ordered by recency. `A` is unbounded, because an unanswered obligation is exactly
the one nothing ever resolves. Therefore bounded retrieval and stickiness are
incompatible *without memory across runs*. Any real bound has to remember what it
stops looking at.

## What shipped here

`_MAX_SUPPLY_REQUESTS = 600` — a per-evaluation request budget. Exceeding it raises
`AdapterError` (exit 2), the same fail-closed doctrine as `_MAX_SUPPLY_PAGES`:
retrieval that stopped early is incomplete, and incomplete retrieval is never read
as absence.

This bounds **cost**, not the obligation set. Nothing is dropped to stay inside it.
It is a fuse, not a fix: it converts a future opaque 403 into a legible alarm that
names the constant and the remedy, roughly 1–2 months before the rate limiter would
fire. It is ~27x the measured baseline and ~60% of the hourly token allowance.

**Consequence to accept deliberately:** if the durable bound below never lands, this
budget turns the board red at ~300 accumulated pull requests. That is the intended
behaviour — a loud, dated deadline rather than a silent slide into rate-limit
failure — but it is a deadline, and the number is a policy choice the owner may
retune.

## Tracer plan for the real bound: a proven watermark

Smallest sound design. One durable timestamp, the *retrieval watermark*, alongside
the immutable activation cutoff:

```text
retrieval_floor = max(activation_cutoff, watermark)
```

The watermark differs from the rejected formula in one decisive way: **it only
advances over history that has been proven clean.** After an evaluation, the
watermark may advance to `now - k * max_stale_days` if and only if every obligation
older than that candidate was resolved in that same run — correlated terminal run,
or explicitly waived as pre-cutoff. If anything older is unresolved, the watermark
does not move, retrieval keeps reaching back to it, and the obligation stays red
for as long as it stays unanswered. History is forgotten only after it is proven to
contain nothing left to answer.

Properties:

- Sticky invariant preserved: forgetting requires proof of resolution.
- Cost bounded in the steady state (a clean repository walks back only
  `k * max_stale_days`), and unbounded only while something is broken — which is
  loud, finite, and self-clearing.
- Activation cutoff untouched: still immutable, still the obligation boundary,
  still the floor the watermark can never precede.
- Tamper direction is visible: advancing the watermark is the dangerous move and it
  lands in git history where it is reviewable. Losing or rewinding it only widens
  retrieval, which is safe.

Open work, deliberately not done in this change:

1. Where the watermark lives (`state/`, committed by the daily job) and its schema.
2. Malformed or missing watermark must fail closed to the activation cutoff, not to
   `now`.
3. Advancement requires the daily freshness job to gain write-and-commit
   permission — a change to `.github/workflows/ecosystem-freshness.yml`, a
   protected path, so it needs human review before implementation.
4. `k` must be justified against the same measured velocity as above, with overlap
   for pagination, delayed runs, and clock skew.
