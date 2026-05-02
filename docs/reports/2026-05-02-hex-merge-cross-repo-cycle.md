# Compounding Cycle — Hex-Merge Cross-Repo — 2026-05-02

> Hari and ix-fuzzy converged on `governance/demerzel/logic/hex-merge.md` from opposite directions: Hari ported the spec into a new module, ix-fuzzy already shipped it months ago. Today both implementations agree byte-for-byte on a shared 7-fixture corpus including the content-derived synthesis ids that pin associativity. This is the "graduation path" promotion-candidate pattern from the 04-30 cycle, executed end-to-end.

## What this cycle delivered

| Repo | Commit(s) | Surface |
|---|---|---|
| **Demerzel** | `c28d402` | `docs/prd/07-hari.md` v2.0 — refresh from "Early/Research, no consumers" to "library-stable, 159 tests, graduation path" with explicit framing of Hari as a parallel implementation of the hex-merge spec ix-fuzzy already shipped. Three named graduation candidates: hex-merge conformance, `TrustedHexObservation`, forward reasoning over claim_keys. |
| **hari** | `3ee010f` | `crates/hari-lattice/src/merge.rs` — faithful port of `ix-fuzzy::observations`. Same Belnap-extended weight table, same content-derived synthesis ids, same staleness budget K=5, same uniform fallback. 6 proof-obligation tests + 10 functional tests. |
| **hari** | `f3231fb` | `fixtures/hex-merge/{01..07}_*.json` + `crates/hari-lattice/tests/hex_merge_conformance.rs` + single-letter wire-format adapter on `merge::HexObservation::variant`. Conformance corpus with `expected.contradictions[].diagnosis_id` pins on the strongest associativity claim. |
| **ix** | `3f68500` | `crates/ix-fuzzy/tests/{fixtures/hex-merge/*,hex_merge_conformance.rs}` — IX-side mirror of the same corpus, parallel test against `ix_fuzzy::observations::merge`. Both runners pick up new fixtures automatically; no test code changes when corpus grows. |
| **ix** | `21c120c, 891c0f3, 3af8d81` | Pre-existing CI clippy debt cleared (manual_range_contains, manual_strip, unnecessary_sort_by) + parity allowlist bumped for the `ix_voicings_payload` tool added by `1d9bad2`. Stable CI gates green; nightly clippy + session_log_wiring tests remain red on unrelated active feature work. |

## Promotion candidates (evidence-based)

| Artifact | Evidence | Recommendation |
|---|---|---|
| **Cross-repo conformance corpus pattern** (`fixtures/hex-merge/*.json` + parallel test in each consumer repo) | First time we have a hand-checked input/output corpus that proves byte-equality between two implementations of a Demerzel spec. The strongest pin — content-derived `diagnosis_id` strings — survived the round-trip without alignment work. The fixture format is JSON with `input.observations[]` + `expected.{observations_count, contradictions[], distribution{T,P,U,D,F,C}, escalation_triggered}`. Both implementations pass on 7 fixtures covering Belnap pairs (T+F, P+D), meta-conflict cross-aspect, staleness, dedup, empty. | **Promote pattern → policy.** Any future Demerzel spec with multiple implementations (e.g. tetravalent merge, fuzzy ops, escalation gates) should ship with this kind of fixture corpus. Suggested home: `Demerzel/fixtures/<spec>/` so all consumers read from one source via submodule. Today the corpus is duplicated in `hari/fixtures/hex-merge/` and `ix/crates/ix-fuzzy/tests/fixtures/hex-merge/` — drift risk is real. |
| **Per-PRD graduation path framing** (the "differentiated features as candidates" section in `prd/07-hari.md` v2.0) | The v1.0 PRD said Hari was "Early/Research, no consumers"; v2.0 frames the same code as "library-stable + parallel-to-ix-fuzzy + three named graduation candidates." Same code, different posture. The framing forces an honest answer to "is this duplicating ix work or contributing differentiated value?" — and surfaces concrete differentiated features (trust-weighted observations, forward reasoning, derivation provenance) that ix-fuzzy explicitly doesn't have. | **Promote pattern → policy.** Other parallel-implementation surfaces in the ecosystem (sentrux ↔ ix-code-*, tars belief graph ↔ hari-lattice) deserve the same v2 treatment. The format: explicit list of differentiated features + graduation criteria for each. |
| **Surgical wire-format adapter** (`mod hex_letter` in `hari-lattice::merge`) | Hari's `HexValue` serializes as `"True"/"Probable"/...` (long-form); Demerzel's `hexavalent-state.schema.json` and `ix-types::Hexavalent` use `"T"/"P"/...`. Rather than rename across the workspace and break ~6 existing fixture files, the merge module uses `#[serde(with = "hex_letter")]` on its `variant` field only. Existing consumers untouched; cross-repo wire format compatible at the merge boundary. | **Maintain as anti-pattern-avoiding-template.** When a wire format must align with a cross-repo schema but the rest of the codebase uses a different serialization, surgical `#[serde(with = ...)]` is the correct surface area, not a workspace-wide rename. |

## Deprecation candidates

| Artifact | Evidence | Recommendation |
|---|---|---|
| `prd/07-hari.md` v1.0 architecture diagram | Was wrong even at v1.0 ship time: showed `hari-core → hari-lattice → hari-cognition` with `hari-swarm → hari-cognition`. Real dependency graph is `hari-lattice → hari-cognition → hari-swarm → hari-core`. The PRD was never updated as the workspace evolved. | **Already corrected** in v2.0. Leave as a calibration data point: PRD freshness drifts faster than expected; `prd-staleness-check` would have caught this. |
| Hari's claim of "the substrate for IX" (in older `ROADMAP.md` framing) | IX shipped its own `Hexavalent` + `ix-fuzzy::observations` independently. IX's `governance/demerzel/docs/prd/07-hari.md` v1.0 explicitly described Hari as "no production consumers." The substrate ambition was already a parallel implementation by 2026-04 — it just hadn't been named that way. | **Already reframed** in PRD v2.0 (graduation path replaces substrate ambition). Cycle should record this as the resolution of an unresolved-but-not-acknowledged duplication. |

## What surprised us (anti-patterns to log)

1. **IX submodule pointing at a feature branch.** The Demerzel submodule in `ix/governance/demerzel` was checked out at `r3-registry-check-ci`, not `master`. My first PRD edit landed in the submodule clone on the wrong branch; had to revert + apply on standalone Demerzel/master. **Lesson**: when editing canonical Demerzel content, always edit standalone Demerzel/master and let downstream submodule pointers update via submodule-bump PR. Don't edit the IX-side checkout in place.

2. **`gh` token expiration silently swapped CI watching to unauthenticated 60/hr quota.** Mid-cycle, `gh run watch` started failing with "rate limit exceeded" — the user's gh token had expired and gh fell back to unauthenticated requests without warning. Re-auth via `gh auth login` restored normal quota. **Lesson**: when CI checks start rate-limiting suddenly, check `gh auth status` first — token expiration looks like quota exhaustion.

3. **Moving CI baseline during cleanup.** While I was fixing pre-existing clippy errors in IX, the user landed two more commits (`4f2ce3b`, `209c9f4`, `1d9bad2`) that added new code with new clippy regressions and a parity-test count drift. Each of my pushes triggered CI, which surfaced the next layer of failures one-at-a-time (clippy aborts at first error). I ended up making 4 sequential commits to reach test-failure depth where the work crossed from "mechanical clippy fix" into "in-flight feature debugging" and I stopped. **Lesson**: when starting a pre-existing-CI-cleanup task, ask whether main is being actively pushed to in parallel. If yes, expect serialized whack-a-mole and budget for it, or coordinate a freeze.

4. **`gh run watch --exit-status` exit code can disagree with `gh run view` conclusion.** Saw `gh run watch` exit 0 on a failed run. Always confirm with `gh run view <id> --json conclusion` before declaring victory. Reported as observation; not actionable.

## Calibration

| Prior claim (source) | New evidence | Calibration |
|---|---|---|
| Hari's "no production consumers" (PRD v1.0, 2026-04-03) | Still T as of 2026-05-02 — but reframed as "graduation candidates pending" rather than "research dead end." | T stays T; the meaning-around-T sharpened. |
| Hari's hex-merge would be a "small tractable" task (my own claim earlier in this session) | Roughly accurate — ~700 LOC + 16 tests landed in one sitting; conformance corpus + cross-repo mirror added another ~500 LOC. Total elapsed ~2 hours of focused work from kickoff to byte-equal proof. | T at 0.85. |
| "Cross-repo byte-equal fixture suite" (PRD v2.0 P2) | Delivered today. Same 7 fixtures verified on both runners. Strongest pin (`diagnosis_id`) confirmed. | T at 0.95. |
| `compounding-cycle` skill effectiveness (04-30 cycle: C at 0.78, "needs freshness check") | Today's micro-cycle was hand-authored; didn't exercise the skill. Calibration unchanged. | C at 0.78. |

## Effectiveness summary

| Artifact | Effectiveness | Confidence | Recommendation |
|---|---|---|---|
| Hex-merge spec (`logic/hex-merge.md`) | T | 0.92 | maintain (fixture corpus now provides anchored conformance evidence) |
| ix-fuzzy::observations | T | 0.90 | maintain |
| hari-lattice::merge | T | 0.85 | maintain; consider promoting to a sibling crate `hari-merge` if it grows beyond the lattice scope |
| Cross-repo conformance pattern | T | 0.85 | promote (see Proposal A below) |
| PRD v2 graduation-path framing | T | 0.80 | promote (see Proposal B) |
| `TrustedHexObservation` extension | U | 0.50 | investigate — graduation candidate but layering question (merge vs above-merge) is unresolved |
| Wire-`merge` into `hari-core::CognitiveLoop` | U | 0.40 | investigate — same layering question |

## Proposed improvements (PDCA)

### Proposal A — promote `fixtures/hex-merge/` to canonical Demerzel home

- **Plan**: Move the corpus to `Demerzel/fixtures/hex-merge/` so consumers read it via submodule. Both `hari/` and `ix/crates/ix-fuzzy/tests/` then reference the canonical copy rather than maintaining duplicates. Eliminates drift risk.
- **Do**: Demerzel PR adding `fixtures/hex-merge/{01..07}_*.json` + `README.md` (verbatim from existing). Then hari + ix PRs that delete their local copies and either (a) add Demerzel as a submodule for fixture access, or (b) symlink/copy at build time, or (c) keep IX's existing submodule path; hari adds Demerzel as a new submodule.
- **Check**: Adding an 8th fixture only requires one commit (in Demerzel); both downstream conformance tests pick it up via fresh submodule pointer.
- **Act**: If submodule overhead is too high for hari (which has no Demerzel dep today), keep hari's local copy and add a `verify-fixture-parity.sh` CI step that diffs against Demerzel/master.

### Proposal B — apply v2-PRD-with-graduation-candidates to other parallel surfaces

- **Plan**: Audit `Demerzel/docs/prd/*.md` for any PRD that's older than 30 days and ships against a parallel implementation in another repo. Re-frame each as graduation-candidate-aware. Likely candidates: `04-tars.md` (tars belief graph vs hari-lattice; tetravalent vs hexavalent), possibly `05-ga.md` (GA chatbot orchestration vs anything reusable to ix).
- **Do**: One PRD refresh per cycle, prioritized by (last-updated × parallel-impl evidence count).
- **Check**: A PRD refresh is "good" if it surfaces at least one differentiated-feature graduation candidate that wasn't named before.
- **Act**: If the audit finds zero parallel-implementation surfaces beyond hari ↔ ix-fuzzy, this is a single-instance pattern, not policy material. Drop it from compound output.

### Proposal C — `cross-repo-cleanup-coordination` policy (corrective Kaizen)

- **Plan**: When a Claude session is doing pre-existing-CI-cleanup on a repo where the user is actively landing feature commits, expect serialized failures. The session policy should be: surface the moving-baseline situation early, propose a coordination point (freeze, branch, or a stop-after-N-cycles rule), and stop at the first non-mechanical failure rather than continuing past a domain decision.
- **Do**: Add a one-paragraph note to `policies/cross-repo-cleanup.yaml` (does not yet exist) capturing this pattern + the "stop at substantive-not-mechanical" rule.
- **Check**: Future cleanup sessions either land in fewer-than-3 commits or surface an explicit coordination ask in turn 1.
- **Act**: If sessions still bounce off moving baselines repeatedly, the rule is too soft and needs a hard "1 cleanup commit max per session" cap.

## Lessons feeding the evolution log

- **Pattern**: cross-repo conformance corpus + per-implementation parallel test = byte-equality proof without coupling implementations.
- **Pattern**: PRD v2 graduation-path framing surfaces unresolved duplication that v1 hides.
- **Anti-pattern**: editing submodule clones on feature branches.
- **Anti-pattern**: assuming `gh run watch` exit code reflects CI conclusion.
- **Anti-pattern**: cleanup sessions on actively-pushed branches without coordination.
- **Open question**: where should `TrustedHexObservation` sit — at the merge layer (cross-repo concern, wire-format change) or above it (consumer-specific layering)? Needs a cross-repo design conversation, not a refactor.

## Cycle metadata

- **Date**: 2026-05-02
- **Repos touched**: `Demerzel` (1 commit, master), `hari` (2 commits, main), `ix` (4 commits, main)
- **Total commits**: 7
- **Tests added**: 16 unit + 1 integration in hari-lattice; 1 integration in ix-fuzzy. Net +18 tests across the workspace.
- **CI state at end**: hari/main green; Demerzel/master green; ix/main stable-clippy green + stable-build green + parity green; ix nightly-clippy red on pre-existing `ix-demo` debt; ix stable-tests red on session_log_wiring (in-flight feature work, not in scope).
- **Author**: Claude Opus 4.7 (1M context), driving with explicit user authorization for commits and pushes.
