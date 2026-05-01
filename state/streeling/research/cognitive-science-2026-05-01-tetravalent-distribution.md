# Cognitive Science Research Note — Tetravalent State Distribution and Subjective Logic Reframing

**Cycle:** `cognitive-science-2026-05-01-001`
**Department:** Cognitive Science
**Question:** Does Subjective Logic add predictive power over tetravalent T/F/U/C for governance recommendations?
**Conclusion:** Insufficient evidence — but the question is mis-aimed. (Belief: U, confidence 0.7)

## What the data shows

Across 11 evolution entries (`state/evolution/*.evolution.json` as of 2026-05-01):

| Truth value | Count | % | Maps to "investigate"? |
|---|---|---|---|
| T | 7 | 64% | 1 of 7 |
| U | 3 | 27% | 3 of 3 (100%) |
| C | 1 | 9% | 1 of 1 (100%) |
| F | 0 | 0% | — |

Mean confidence: 0.765. All three U entries have confidence ≤ 0.6 — the uncertainty is already encoded in the confidence field, not just in the categorical truth value.

## Where the predictive gap actually lives

Recommendation distribution: `investigate=5, maintain=3, promote=3`. U and C entries deterministically map to `investigate` (4 of 4 cases). The ambiguity lives entirely in T-states:

| T-state entries | Recommendation | Citations | Cross-repo validation |
|---|---|---|---|
| asimov-constitution | maintain | 5 | static |
| default-constitution | maintain | 11 | static |
| alignment-policy | maintain | 3 | static |
| harness-engineering | promote | 8 | yes (ix consumed) |
| ix-autoresearch | promote | 12 | yes (largest consumer) |
| visual-governance | promote | 55 | yes (multi-AI brainstorm cycles) |
| tetravalent-state schema | investigate | 4 | hari demoted Lie, promoted SL |

The pattern is visible: **T → maintain when stable and uncited externally; T → promote when growing and cross-repo validated; T → investigate when contradicted by external evidence.** This is a *trajectory* or *momentum* signal, not an uncertainty signal. Subjective Logic's belief + disbelief + uncertainty + base_rate adds no information here — what's missing is a derivative, not a richer point-estimate.

## Implication for Proposal D

`pdca-subjective-logic-tetravalent-upgrade` (state/pdca/2026-05-01-subjective-logic-tetravalent-upgrade.pdca.json) was framed as: "let SL refine the categorical Unknown state with calibrated uncertainty + base_rate." On the existing 11-entry corpus, this would change zero recommendations because U → investigate is already deterministic.

The reframed proposal: **augment T with a trajectory field, not U with a richer point-estimate.** Concretely, alongside `truth_value: T`, capture `trajectory: ascending | steady | declining` derived from the citation/violation deltas the `demerzel-quality-trend` skill (commit 06cd440) is already collecting nightly. The trajectory field would let `recommendation` be derived rather than hand-picked: ascending T → promote, steady T → maintain, declining T → investigate.

## Sequencing

Hold Proposal D at PDCA plan phase. Wait for the 2026-05-29 quality-trend evaluation (routine `trig_01GvSr7BaL5jHBSdydgcaybH`). Once 4 weeks of trajectory data exist, retro-fit ascending/steady/declining classifications onto the 11 existing T entries and check whether the predicted recommendations match the recorded ones. If the match rate exceeds chance baseline, advance the reframed Proposal D — refining T with trajectory, not U with SL.

This is the methodological lesson hari taught when it demoted Lie in favor of RecencyDecay: **complex priors must beat simple baselines on real data before being adopted.** Subjective Logic's complexity does not earn its place against the simpler "T is heterogeneous, refine the dominant class first" baseline visible in the data.

## Open questions for next cycle

1. Why has F never been observed? Bias toward charitable interpretation, or correct upstream filtering?
2. Does the C state (currently 1 entry) actually mean "contradictory" in the SL sense (high belief + high disbelief + low uncertainty), or is it being used as "complex"?
3. Should the recommendation field be derived (computed from truth_value + trajectory + cross-repo signals) rather than authored, to reduce author bias?

## Citations

- `state/evolution/*.evolution.json` (data, n=11, as of 2026-05-01)
- `state/pdca/2026-05-01-subjective-logic-tetravalent-upgrade.pdca.json` (Proposal D, plan phase)
- `state/pdca/2026-05-01-governance-quality-trend.pdca.json` (Proposal E, do phase, 4-week eval scheduled)
- `state/evolution/2026-04-30-hari-subjective-logic.evolution.json` (the source observation that prompted Proposal D)
- hari commit `e0a8f45` (the demote-Lie methodological precedent)
- Commit `06cd440` (Proposal E shipped)
- Commit `a09e99f` (CI validator, defense-in-depth)
