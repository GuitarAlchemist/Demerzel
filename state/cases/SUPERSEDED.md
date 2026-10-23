# state/cases — ARCHIVED / SUPERSEDED (2026-07-20)

**What it was:** the state directory for the constitutional case-law loop —
`index.json` was to accumulate adjudicated governance "cases" and standing
orders (schemas landed in `479b4ea`, 2026-04-03, "constitutional case law
schemas and state directory").

**When it died:** never lived. `index.json` has stood empty since it was
created — `cases: []`, `standing_orders: []`, every stat `0`
(`last_updated: 2026-03-31`). No case was ever adjudicated into it.

**Why archived:** hari #29 loop audit ("kill or archive-with-verdict"). The
loop was built schema-first with no producer (nothing writes cases) and no
consumer (no script, workflow, or policy reads `state/cases/`) — verified
2026-07-20. It is an empty scaffold asserting nothing.

**Superseded by:** nothing re-owns case-law adjudication today. Governance
decisions that do get recorded flow through GitHub Discussions
(constitutional-proposal template) and the audit-trailed
`state/evolution/*.evolution.json` cycle summaries. If constitutional
case-law is revived, per loop doctrine (hari #29) it must land with its
producer (an adjudicator that writes cases) AND its gating consumer in the
same change. Until then, treat `index.json` as inert.
