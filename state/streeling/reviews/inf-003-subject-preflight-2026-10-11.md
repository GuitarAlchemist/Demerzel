# INF-003 independent AI subject preflight — 2026-10-11

An independent Codex agent that did not author INF-003 checked the English draft, its research and production JSON, pinned IX Petri and divergence source at `bd1336b7c4045e427dcdbe80b102790e45da5ce1`, and five answered exercises. This is a static source and arithmetic review, not a real analyzer or DuckDB run, human subject approval, learner trial, or publication receipt.

The review found one P3 precision issue: a `Fails` deadlock-freedom verdict need not serialize a witness when `max_reported_deadlocks` is zero. The lesson, exercise answer, and research record now state that limit and require a positive cap for witness review. The same reviewer retested the correction and reported no remaining finding in that scope. It independently recomputed `KL(p||q)=0.23014565796142483` and `JS(p,q)=0.07648207115762617` nats for the explicitly synthetic ten-net table. All five answers and ten pinned IX links checked out; both JSON schemas and the focused course preflight passed with 1,720 English words and review/publish flags false.

No actual IX analyzer batch, DuckDB query, subject reviewer, learner, fluent-language reviewer, or public Learn readback is represented by this preflight.

## AI localization parity follow-up

FR, ES, PT, IT, and DE source drafts were added after the English preflight. A separate independent AI reviewer compared all five with English and found no actionable discrepancy in the five answered exercises, vectors, KL/JS values and units, the `max_reported_deadlocks` caveat, the synthetic-versus-deployed boundary, or the pending-review labels. Pinned source URL sets and module identities match; local links resolve. This is semantic parity triage, not fluent native-language approval.
