# Meta-Compounding Cycle — Corrective Pass — 2026-04-30

> Discussion #242 produced a static inventory because the evolution log was 27 days stale. This is the retroactive compound across Demerzel + ix + hari for the missing window.

## What broke in #242

The compound cycle reads `state/evolution/*.json` as its primary input. Last entry was dated **2026-04-03**. In the intervening 27 days:

- **Demerzel:** 47 commits — harness engineering thesis, Sentinel spec, hex-merge rules, Path C synthesis, multi-model orchestration v1.1.0, governance consumption map, LLM Wiki ingest protocol.
- **ix:** 60+ commits — ix-autoresearch crate (Phases 1-7), sentrux (5th federation peer), OPTIC-K v4→v1.8, Forte set-class catalog, ix-quality-trend, ix-embedding-diagnostics, ix-bracelet, deterministic control-flow hooks (harness engineering consumer).
- **hari:** 24 commits — Subjective Logic promoted to first-class, Lie demoted to opt-in, belief propagation Phase 8, derivation provenance, trust-aware swarm Phase 4.

None of this was visible to the cycle. **The skill operated correctly on stale data; it did not detect that the data was stale.** That is the structural bug.

## Promotion candidates (evidence-based)

| Artifact | Evidence | Recommendation |
|---|---|---|
| **harness-engineering** (`docs/governance/harness-engineering-direction.md`) | Demerzel proposed it (3ec5110), specified four adapters (cargo, clippy, github-actions, ga), shipped signature layer v0.1. ix consumed it within 12 days: deterministic control-flow hooks (5699d6c), sentrux as 5th federation peer (fbcc247), regression gate (f3c5e31). Cross-repo propose→consume loop closed faster than memristive-markov. | **Promote pattern → policy.** Strongest cross-repo signal in 6 weeks. |
| **autonomous-loop-policy v1.1.0** | ix-autoresearch is the largest concrete consumer to date — 7 phases, MCP-exposed via `ix_autoresearch_run`, JSONL-logged, validation harness, honest negative-result reporting on Phase 7. Demonstrates the policy's "ship + measure" clause. | **Maintain + amend.** Add evaluator-in-the-loop refinement (see proposals). |
| **multi-AI brainstorm methodology** | Validated again in Path C synthesis (116cb5e), multi-LLM code review fix cycle (03ba899 — 7 findings from Codex+Gemini+Claude). Pattern is now standard practice, not experimental. | **Maintain.** Already operational. |

## Deprecation candidates

| Artifact | Evidence | Recommendation |
|---|---|---|
| `state/beliefs/visual-*.belief.json` (10 entries) | All from 2026-04-03 visual session. None updated since. Visual work has shifted to ix-driven 8K textures + GLB assets per session memories — these beliefs are likely stale. | **Investigate.** Audit each for current truth value. Don't auto-deprecate. |
| `logic/governance-evolution.schema.json` (in current form) | Schema enums (`artifact_type`, `event.type`) no longer match real usage. Real entries use `meta`, `capability`, `compounding_cycle`, `pattern_detected`, `governance_concept_created` — none are in the schema enum. | **Amend.** Schema should follow reality. See proposal C. |

## Calibration assessment

Reviewed three high-confidence assessments from the 04-03 cycle:

- **Visual governance T at 0.88** → still T. Continued cross-cited in session memories. Calibrated correctly.
- **Multi-AI brainstorm effectiveness T at 0.88** → still T. Path C synthesis + multi-LLM code review extended the validation. Calibrated correctly.
- **Compounding-cycle effectiveness T at 0.88** → **demoted to C at 0.78**. Discussion #242 surfaced the failure mode; the metric was over-confident because it didn't track input-freshness as a separate dimension.

**Lesson:** confidence on a process should decompose into (correctness given inputs) × (input-quality given environment). The 04-03 entry conflated them.

## Effectiveness summary

| Artifact | Effectiveness | Confidence | Recommendation |
|---|---|---|---|
| harness-engineering | T | 0.86 | promote |
| autonomous-loop-policy (via ix-autoresearch) | T | 0.82 | promote |
| tetravalent-state schema (vs hari Subjective Logic) | C | 0.78 | investigate |
| The Sentinel spec | U | 0.50 | investigate (needs behavioral test) |
| compounding-cycle (this skill) | C | 0.78 | investigate (needs freshness check) |
| visual-governance | T | 0.88 | maintain |

## Proposed improvements (PDCA)

### Proposal A — harvest→compound cron pair (proactive Kaizen)

- **Plan:** Wire the harvest skill and compound skill as a single scheduled pair so they cannot drift apart. Harvest writes fresh state/evolution; compound reads it immediately.
- **Do:** `CronCreate("17 13 * * 5", "/demerzel harvest")` then `CronCreate("47 13 * * 5", "/demerzel compound")` — already in the skill doc but not actually scheduled.
- **Check:** Detect successive compound runs producing identical inventory.
- **Act:** If the pair drifts, investigate why harvest didn't run.

### Proposal B — input-freshness check in step 1 (proactive Kaizen)

- **Plan:** Before step 1 reads `state/evolution/`, compare its newest mtime to (a) `git log --since=<latest-mtime>` in this repo and (b) sibling repos under `~/source/repos/`. If new commits exist but no matching evolution entries, emit a `stale-state` warning and fall back to harvesting from git log + memory + sibling git logs.
- **Do:** Edit `.claude/skills/demerzel-compound/SKILL.md` to add Step 0 — Liveness Check; update the harvest script to also scan sibling repos.
- **Check:** Re-run the cycle; output should not be a static inventory.
- **Act:** This very report is the manual execution of the proposed self-healing path.

### Proposal C — schema follows reality (proactive Kaizen)

- **Plan:** Update `logic/governance-evolution.schema.json` to extend `artifact_type` with `[meta, capability]` and `event.type` with `[compounding_cycle, pattern_detected, governance_concept_created, cross_repo_validation, kaizen_proposal, gap_identified, violated]`.
- **Do:** Edit schema; add migration note that records the legacy enums vs the new superset.
- **Check:** Run a JSON-schema validator across all `state/evolution/*.json` — all should now validate.
- **Act:** If new event types emerge organically, repeat the schema-follows-reality cycle (do not gatekeep usage on schema rigidity).

### Proposal D — Subjective Logic upgrade for tetravalent's "U" (innovative Kaizen, requires human approval)

- **Plan:** hari's Subjective Logic opinions (belief + disbelief + uncertainty + base rate) carry calibrated uncertainty rather than the categorical `U`. Demerzel's tetravalent state currently flattens "Unknown" into a single bucket; SL would let us say "U with 0.7 base rate, 0.3 uncertainty" instead of just "U".
- **Do:** Smallest testable change — add an optional `subjective_logic` block to `tetravalent-state.schema.json`; let new entries opt in; do not migrate legacy entries.
- **Check:** Compare predictive power of `U` vs `U+SL` over the next 3 cycles.
- **Act:** If SL adds no signal over plain `U`, demote it (the same way hari demoted Lie). Apply hari's discipline to ourselves.

### Proposal E — port ix-quality-trend as governance-quality-trend (proactive Kaizen)

- **Plan:** ix-quality-trend (652de21) emits a structured nightly health artifact for GA quality. The dual for governance: nightly per-artifact effectiveness deltas, plotted over time, surfaces drift before it accumulates.
- **Do:** New skill `demerzel-quality-trend` that runs `state/evolution/*` deltas as a JSONL stream. Keep it small — 50 lines of skill, no new schema.
- **Check:** After 2 weeks, the trend file should show whether artifacts are accelerating or stagnating.
- **Act:** Expensive artifacts that stagnate become deprecation candidates automatically.

## Cross-repo leverage map

| ix/hari evolution | Demerzel leverage |
|---|---|
| ix `sentrux` 5th federation peer (realtime structural sensor) | Add governance-signals as a 6th federation peer — Demerzel's beliefs + violations as a live stream alongside ix structural data. |
| ix `ix-embedding-diagnostics` (leak detection, cluster stability) | Apply to belief embeddings — detect when `state/beliefs/` entries become degenerate or contradictory in latent space. Wire as proposal D's measurement substrate. |
| ix `ix-autoresearch` MCP tool | Streeling research questions can be driven by `ix_autoresearch_run` — autonomous question selection, edit-eval-iterate, JSONL provenance. Direct Galactic Protocol contract opportunity. |
| ix `ix-quality-trend` nightly pipeline | Proposal E: governance-quality-trend, port of the same pattern. |
| hari Subjective Logic first-class | Proposal D: upgrade tetravalent `U` with calibrated uncertainty + base rate. |
| hari Phase 8 belief propagation + provenance | Demerzel `state/beliefs/*` should carry provenance chains. Schema extension. |
| hari Phase 4 trust-aware swarm + AgentVote | Formalise Demerzel's skeptical-auditor + producer pairing as trust-weighted voting. New policy candidate. |
| hari "demote Lie" moment | Methodological lesson: stress-test our own complex constructs against simple baselines. Apply specifically to tetravalent and to the compounding-cycle skill itself. |

## State written this cycle

- 4 new evolution entries (`2026-04-30-{harness-engineering,ix-autoresearch,hari-subjective-logic,the-sentinel}.evolution.json`)
- 1 updated entry (`2026-03-18-compounding-cycle.evolution.json` — 4 new events including the failure-mode admission)
- 0 belief updates (deferred — needs Proposal B's harvest+freshness pass first)
- 0 PDCA records persisted yet (proposals A-E above are candidates, not yet committed to `state/pdca/`)

## What remains for the next cycle

1. Persist proposals A-E as PDCA records in `state/pdca/`.
2. Run `/demerzel harvest` properly and compare its output to this manual reconstruction.
3. Audit the 10 stale `visual-*.belief.json` entries.
4. Wire the The Sentinel behavioral test before the next cycle so it can leave the `U` state.
5. If Proposal C is accepted, re-validate all 11 evolution files against the updated schema.
