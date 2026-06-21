# 1. Derived governance manifest

- Status: Accepted
- Date: 2026-06-20
- Deciders: Stephane Pareilleux
- Source: `/improve-codebase-architecture` review + `/grilling` session (2026-06-20)

## Context

The governance artifact graph — which constitutions, personas, policies, schemas, and
tests exist, and how they reference each other — is restated by hand across five places:
`README.md` counts, `CLAUDE.md` prose ("44 policies"), `AGENTS.md` team table,
`context-map.yaml` (1200+ lines of hand-maintained edges), and `schemas/capability-registry.json`.

These have already drifted: 44≠45 policies (`CLAUDE.md` vs disk), 60≠61 skills, 21≠22
workflows (`README.md` vs disk), and `context-map.yaml` is missing 14 of 45 policies. This
is the signature of an **authored index** that humans cannot keep in sync as the repo grows.

In the `/codebase-design` vocabulary, the five copies are **shallow** — each is a thin,
hand-typed restatement of facts the filesystem already holds. The **deletion test** says:
delete the hand-maintained copies and the complexity vanishes, because the artifacts on
disk are the real source of truth for *existence*.

## Decision

Introduce a **governance manifest** (`governance-manifest.json`) that is **derived**, not
authored. A script (`scripts/build_manifest.py`, joining the existing `scripts/` tooling)
walks the artifact tree and *emits* the manifest. It is never hand-edited.

The manifest is **committed and CI-diffed**: CI runs the generator and fails on any diff
("manifest stale, run the generator"). This is the same drift gate
`karpathy-cherny-discipline.yml` already runs for digests. Committing it lets sibling repos
(ga/ix/tars) and recon read the graph over the filesystem/submodule **without running
Python** — consistent with the cross-repo JSON-on-disk contract pattern, and with the fact
that Demerzel already commits derived state (verdicts, evolution logs).

The hand-maintained **edges** in `context-map.yaml` are deleted; edges are harvested from
the artifacts' own reference fields instead (see ADR-0002).

## Consequences

- **Locality**: "what artifacts exist and how they relate" is defined in one place — the
  filesystem, read mechanically. Fix a fact where it lives; the next build reflects it.
- **Leverage**: README counts, CI invariants, recon, and sibling repos all read one file.
- The README-SYNC markers are *populated* from the manifest rather than hand-typed.
- New CI job: generate + `git diff --exit-code`. No new machinery beyond it.
- Cost: a one-time deletion of `context-map.yaml`'s edge content and migration of any edges
  worth keeping into artifact fields.

## Alternatives considered

- **Promote `context-map.yaml` to an authored canonical** with a schema and a CI conformance
  check. Rejected: it keeps a human in the sync loop, which is the exact failure mode already
  observed. A future reviewer tempted to re-suggest this should read this ADR first.
- **Ephemeral validate-only manifest** (built in CI, never committed). Rejected: sibling
  repos and recon need to read the graph without a build step.
