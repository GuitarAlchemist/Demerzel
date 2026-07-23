# Galactic Protocol follow-ups — evidence-first ledger ratification

**Date:** 2026-07-21 (deepened same day)
**Status:** COMPLETE (2026-07-23) — all slices landed. A: staleness investigation shipped (`docs/research/2026-07-21-staleness-downstream-verdict.md` + fix #814). B: spec v1.4.1 crisp-channel exemption. C: ratified via #817 + review-fix commit 58aa82b (schema additive-only + CI-validated fixture + SINGLE-HOST ADVISORY label + changelog waiver). §0 resolved as (a) adopt-whole; the bridge's constitutional question (CL-817-12) adjudicated in CONTRIBUTING.md (scripts/ tooling exception). Prior status line kept below for provenance.
**Status (superseded):** owner decision recorded — option (a), adopt the bridge as a stacked follow-up to PR #813
**Provenance:** two-subagent audit (spec survey + usage audit) → PR #813 (v1.3.0 status-honesty) → this plan → 4-agent deepening panel (2 researchers, 2 reviewers) + 2 documented learnings.

## Enhancement Summary

**Deepened on:** 2026-07-21
**Sections enhanced:** all 3 slices + new §0 (reality reconciliation) + sequencing
**Agents used:** ledger/schema researcher, submodule-freshness researcher, code-simplicity-reviewer (8 findings), architecture-strategist (6 findings). Learnings applied: `docs/solutions/agentic/2026-06-22-pocock-harness-afk.md` (queue-not-loop), `docs/solutions/harness/2026-07-20-powershell-native-exit-codes.md` (fail-loud).

### Key changes vs. the draft
1. **Slice 3 build is CUT.** `.github/workflows/submodule-notify.yml` already computes behind-counts per consumer, sends `demerzel-updated` repository_dispatch, and files issues at >5 behind — green, ran 4× today. Consumers are stale *despite* a working alert channel. Slice 3 is now a zero-code investigation of the dead downstream. (Simplicity F2; confirms the `check-existing-guards-before-building` lesson.)
2. **Slice 2 shrinks to a surgical edit.** The status table is already honest post-#813; the one real contradiction is spec L258 ("crisp messages must pass schema validation") × L247 ("Directives | Always crisp"). No new status vocabulary, no prose-format spec for a dormant channel. (Simplicity F3/F4; arch F5 caveat on serialization kept.)
3. **Slice 1 is renamed "ratification" and re-grounded.** A Codex-session tracer-bullet (the "galactic live session bridge") already authored `schemas/contracts/session-claim.schema.json` and a v1.4.0 spec amendment declaring the ledger IMPLEMENTED — bypassing this plan's evidence gate. §0 records the explicit owner decision to adopt it. (Simplicity F1, arch F1.)
4. **Acceptance hardened against theater.** CI can never see `~/.agents/` — the draft's "validator green against the real ledger" was vacuously satisfiable. Fix: committed sanitized fixture validated unconditionally, live-ledger check as local bonus; longer-term, the observer-model evidence snapshot (arch F2ii). (Simplicity F5.)
5. **Ordering semantics corrected from research:** "latest wins" must be file-position order, never timestamp comparison (clock skew across sessions); records must be small single-write lines; readers tolerate a torn last line; schema evolution is additive-only with per-line `schema_version`.

### Conflict adjudicated
Simplicity F2 (cut Slice 3) vs. architecture F4 (build sibling producer): **simplicity wins on the facts** — the guard exists; architecture's reviewer didn't check for `submodule-notify.yml`. Architecture's sibling-producer design (separate `scripts/submodule_age.py` + own workflow + state_glob proof, NOT an `ecosystem_freshness.py` fold-in) is preserved below as the pre-researched implementation path **iff** the investigation concludes a new guard is warranted.

---

## §0 — OWNER DECISION FIRST: bridge reconciliation

**Owner decision (2026-07-21): option (a), Adopt.** Keep the tested bridge as the named single-host consumer, rebase it onto the final PR #813 head, and publish it as a separate stacked PR. The evidence-gate waiver must remain explicit in the v1.4.0 changelog; no bridge changes belong in PR #808.

The adopted bridge was authored by a Codex session ("Reflective Architect" lane, per `docs/design/2026-07-21-galactic-live-session-bridge.md`): `scripts/galactic_bridge.py` (+hook, installer, tests), `schemas/contracts/session-claim.schema.json`, and a v1.4.0 amendment to `contracts/galactic-protocol.md` declaring "Local session coordination: IMPLEMENTED". It is ledger-aware and keeps runtime traffic out of the repo, but it consumed this plan's version number, pre-implemented Slice 1's deliverables, and bypassed the evidence gate (unmeetable before 2026-07-23).

Options (pick one before any slice starts):
- **(a) Adopt:** review + commit the bridge as the v1.4.0 amendment; Slice 1 below becomes ratification of its schema; the bridge is the named consumer (arch F6 — this makes Slice 1 genuinely vertical).
- **(b) Defer:** stash/branch the bridge work; the gate stands; Slice 1 proceeds on 2026-07-23+ as originally scoped, taking v1.4.0.
- **(c) Split:** commit only `session-claim.schema.json` + a scoped-down spec row now (satisfying Slice 1 early with the gate waived explicitly), leave the MCP/hook/installer machinery for its own reviewed PR.

Whatever is chosen: the spec row must be scope-labeled **IMPLEMENTED — SINGLE-HOST ADVISORY** with multi-host sync normatively out of scope (arch F2i), and the gate's bypass (if any) recorded in the changelog rationale — never silently.

## Preconditions (arch F3)

1. **PR #813 merged** — the compliance-report gate in `validate_governance.py` is the pattern Slice 1's validator extends and doesn't exist on master yet; #813 also owns the spec file all later edits serialize behind.
2. **§0 decided** — Slices 1 and 2 both edit `contracts/galactic-protocol.md`; version numbering (v1.4.0 vs v1.5.0) depends on the bridge decision.

## Slice A (was Slice 3) — Investigate the dead staleness downstream. Zero code.

**Question:** consumers sit 2–3.5 months stale despite `submodule-notify.yml` alerting on every master push. Where does the signal die?

- **Work:** (1) check each consumer (ga/tars/ix) for a `repository_dispatch` handler for `demerzel-updated` — present? enabled? last run?; (2) list staleness issues filed by the notifier — open? closed-unactioned?; (3) deliver a one-page verdict: either "the embed is delivery — here is the broken hop to fix" or "the embed is not delivery — strike the claim from the spec (doc-only follow-up)".
- **Named consumer of the verdict (simplicity F7):** the repo owner, at the next governance review; deadline 2026-07-28. The verdict feeds the spec's delivery claim — it cannot sit unread by design.
- **Acceptance:** the verdict doc exists with per-consumer evidence (handler status + issue disposition), and names the single next action.

### Research Insights (pre-researched path, used ONLY if the verdict is "guard needed")
- Read pins remotely via Contents API (`GET /repos/{o}/{r}/contents/governance/demerzel` → `type: "submodule"`, `sha`), pinned to each consumer's default branch via `?ref=`; no clone needed.
- One compare call (`GET .../compare/{pin}...master`) yields both `behind_by` and both commit dates; **alert on date-lag** (commit-count conflates volume with significance), keep `behind_by` as human color; treat `ahead/diverged` as a distinct config-error anomaly.
- Dependabot (`dependabot-git_submodules`) and Renovate both exist but are **auto-remediators** — they open bump PRs and have no alert-only mode (Dependabot #11802 has even deleted submodules); they don't fit the observe-first constraint.
- Architecture: sibling producer `scripts/submodule_age.py` + own scheduled workflow emitting a `state/` report, registered as a normal loop in `loop-health.yml` with a `state_glob` proof. NOT a fourth adapter inside `ecosystem_freshness.py` — loop-liveness and governance-currency are different invariants with different remediation owners, and the alternative needs a `schemas/loop-health.schema.json` change (blocked path, human-gated).
- Fail-loud (per the swallowed-exit-code learning): any API failure → `AdapterError`-style exit 2, never "assume fresh"; unreadable consumer repo = error, not skip.

## Slice B (was Slice 2) — One-sentence spec correction

- **Work:** amend the L247×L258 contradiction: directives are exempted from the "crisp ⇒ schema-validated" rule while their row is DRAFT — NO EMITTER (one sentence), and append the revival criterion to the existing row: "revive the JSON form when a directive requires machine parsing by a consumer repo" (one line). Own version bump; serialized behind #813 and the §0 landing.
- **Cut from draft:** RETIRED-UNTIL-NEEDED vocabulary (invents states for zero behavioral difference); prose-format documentation (dormant channel, no consumer — the LOLLI trap this plan exists to avoid).
- **Acceptance:** grep of the spec finds no enforcement claim about directives that reality contradicts; changelog entry present; `directive.schema.json` untouched.

## Slice C (was Slice 1) — Ledger ratification (gated or §0-waived)

- **Gate, stated plainly (simplicity F8):** the collision-evidence condition is already met (mergerisk archive-conflict flag); what remains is the calendar: ≥3 sessions across ≥3 days ⇒ earliest 2026-07-23 — unless §0(a)/(c) explicitly waives it in the changelog.
- **Work:** ratify (or author, under §0(b)) `schemas/contracts/session-claim.schema.json` against all real ledger lines (46+ at deepening time); spec row per §0; extend `validate_governance.py` following the #813 gate pattern.
- **Schema constraints from research (bake into the schema's own description fields):**
  - Ordering: latest-line-wins = **file byte order**, never timestamp comparison; `ts` is advisory/human-facing (clock skew across sessions makes timestamp-LWW wrong).
  - Writers: one line per single append-mode write, records small (<4 KB) — NTFS gives no interleaving guarantee above sector size; readers skip a trailing line that fails to parse (in-flight append).
  - Evolution: additive-only; per-line `schema_version`; `additionalProperties: true`; `required` only for fields present in **all** real lines; status values as enum-with-escape (`anyOf: [enum, string]`) — 46 lines is too small a sample to freeze an enum (overfitting).
  - Liveness (queue-not-loop learning + research F3): the ledger stays a claim journal, not a task queue or lock server — but note in the spec that stale-claim hygiene (heartbeat/force-release with an audit line) is a known open issue, deferred until it actually bites.
- **Acceptance (hardened, simplicity F5/F6):**
  - [ ] Committed sanitized fixture (last N real lines) validated **unconditionally** in CI; live-`~/.agents/` validation as local bonus path.
  - [ ] Spec row scope-labeled IMPLEMENTED — SINGLE-HOST ADVISORY, with the named consumer (the bridge under §0(a), else the fleet sessions themselves).
  - [ ] (moved to non-goals): "zero new message types without instances" — standing constraint, not a criterion.
- **Follow-up (not this slice, arch F2ii):** observer-model evidence snapshot — a local hook commits line-count + hash + last-N sanitized rows into `state/`, giving CI a verifiable artifact of the out-of-repo ledger, mirroring the compliance-report pattern.

## Sequencing

`#813 merge` → `§0 decision` → **A** (investigation, deadline 07-28) → **B** (doc-only) → **C** (2026-07-23+ or §0-waived). Slices touching `.github/`/`schemas/` expect the fail-closed risk-report gate — human merge review is the design, not an obstacle.

## Non-goals (standing)

- No new message types without pre-existing instances.
- No lock server, task queue, or daemon around the ledger.
- No auto-remediation of consumer staleness in any slice.
- The five DRAFT — NO EMITTER message types stay untouched.

## References

- Append atomicity/torn lines: nullprogram.com/blog/2016/08/03, nblumhardt.com/2016/08/atomic-shared-log-file-writes
- Ordering/HLC vs timestamp-LWW: oneuptime.com/blog/post/2026-01-30-event-ordering-in-microservices/view
- Event versioning: event-driven.io/en/simple_events_versioning_patterns
- Schema inference without overfitting: grammarware.net/text/2025/jsonschema.pdf; ceur-ws.org/Vol-3941/BENEVOL2024_TECH_paper14.pdf
- Pave the cowpaths: w3.org/html/wg/wiki/ProposedDesignPrinciples
- Contents/Compare API: docs.github.com/en/rest/repos/contents; docs.github.com/en/rest/commits/commits
- Dependabot submodules (remediator, #11802): github.com/dependabot/dependabot-core
