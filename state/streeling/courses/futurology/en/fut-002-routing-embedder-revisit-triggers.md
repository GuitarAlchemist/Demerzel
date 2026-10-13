---
module_id: fut-002-routing-embedder-revisit-triggers
department: futurology
course: Revisit Triggers for GA's Routing Embedder
level: early-intermediate
prerequisites: [fut-001-thinking-about-tomorrow]
estimated_duration: "35 minutes"
produced_by: codex-project-pilot
research_cycle: futurology-2026-10-11-002
version: "0.1.0"
---

# When Should GA Revisit Its Routing Embedder?

> **Department of Futurology** | Level: Early intermediate | Estimated duration: 35 minutes | Status: English draft; subject, learner, localization, and publication review pending

## Objectives

After this lesson, you will be able to:

- Separate a historical model choice, its evaluation method, and a future condition that would justify revisiting it.
- Calculate the margin to a stated gate without presenting a small benchmark as a deployment forecast.
- Explain why a model swap needs its own confidence-threshold sweep and why eight out-of-scope prompts provide a coarse rate.
- Write a bounded scenario response: what to measure, which branch it selects, and what observation would falsify the preferred branch.

## The project question

At pinned GA commit [`dc2e74cbd992a298f67efb928b5b3754615e1924`](https://github.com/GuitarAlchemist/ga/tree/dc2e74cbd992a298f67efb928b5b3754615e1924), the chatbot's routing configuration names `bge-large` with `MinConfidence: 0.64`. The [evaluation plan](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/docs/plans/2026-06-16-ml-text-embedder-evaluation-plan.md) describes that routing swap as shipped at its historical date and reversible by reverting two configuration values. It leaves a possible global memory-store swap deferred because that would require separate evidence and a persisted-index migration. The pinned [appsettings file](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/Apps/GaChatbot.Api/appsettings.json) corroborates the routing model and threshold; it is not a live deployment readback.

The useful future question is not “Which model will win next year?” It is: **What new observation would make this particular routing decision worth reopening?** This lesson builds a small trigger ledger from the pinned benchmark and validation record. [FUT-001](fut-001-thinking-about-tomorrow.md) teaches broad horizons and 2×2 scenarios. Here a scenario is a bounded **if measured condition, then next test** branch. It has no invented probability or calendar deadline. The branch can be wrong; the evidence needed to reject it is part of the design.

## 1. Freeze the decision and the two evaluation stages

The [Phase 0 bake-off report](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/state/quality/embedder-bakeoff/bakeoff-latest.md) evaluated 166 in-scope prompts across 16 intents. Its five-fold cosine one-nearest-neighbor result is a **router-mechanism proxy**, not the full production routing stack. It also reports intent silhouette and **single-embed** latency. The numeric [bake-off artifact](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/state/quality/embedder-bakeoff/bakeoff-latest.json) gives `bge-large` p95 latency as `238.27479999454226 ms` and the nomic baseline as `101.44889999355655 ms`. The report chooses a 500 ms p95 budget for the chat path and marks the candidates within it. Passing a single-embed comparison to that budget does not prove a measured end-to-end chat p95.

| Phase 0 model | Proxy cross-validation accuracy | Single-embed p95 | Role in the decision |
|---|---:|---:|---|
| `nomic-embed-text` | 0.644 | 101.449 ms | Prior routing baseline |
| `bge-large` | 0.705 | 238.275 ms | Proxy winner; must face full harness |

The later [Phase 2 validation](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/state/quality/embedder-bakeoff/phase2-validation-2026-06-16.md) ran the full `RoutingEvalHarness` with descriptions, hint boosts, and a confidence threshold. Its accuracy numbers must **not** be subtracted from the Phase 0 proxy numbers as if the tests were the same. On the full harness, the nomic baseline at threshold `0.55` had in-scope accuracy `0.934` and out-of-scope (OOS) decline `0.875`. `bge-large` at the same `0.55` kept in-scope accuracy `0.946` but declined only `0.375` of OOS prompts. After recalibrating to `0.64`, it kept `0.946` in-scope and declined `1.000` of OOS prompts **in that validation run**.

The switch therefore depended on a **pair**, model plus threshold. A new embedder can change the scale of cosine scores, so copying the previous model's threshold can turn unknown prompts into forced routes. The pinned plan says to rerun the per-prompt threshold sweep on future swaps and keep harness and production settings aligned. Neither a higher proxy score nor a copied threshold is enough for promotion.

### Practice exercise 1: calculate the latency margin

Using the numeric Phase 0 artifact, subtract `bge-large`'s single-embed p95 from the report's 500 ms budget. How much slower was its measured single-embed p95 than nomic's? What claim is still unsupported?

> **Answer:** The arithmetic margin is `500 - 238.27479999454226 = 261.72520000545774 ms`, about **261.7 ms**. The difference from nomic is `238.27479999454226 - 101.44889999355655 = 136.8259000009857 ms`, about **136.8 ms**. Both are single-embed comparisons from that fixed run. They do not establish end-to-end chat p95, behavior under a different host or load, or a future latency guarantee.

### Practice exercise 2: compare like with like

How much did full-harness in-scope accuracy rise from nomic at `0.55` to recalibrated `bge-large` at `0.64`? Why is `0.946 - 0.705` the wrong comparison for that question?

> **Answer:** `0.946 - 0.934 = 0.012`, or **1.2 percentage points**, on the full-harness comparison. The `0.705` figure is `bge-large`'s Phase 0 one-nearest-neighbor proxy accuracy, obtained by a different method. Subtracting it from Phase 2 would mix unlike measures and would not give a model improvement.

## 2. Turn the threshold sweep into bounded branches

Start with a recorded baseline and write down **which new measurement changes the action**. Use the pinned in-scope `0.934` as the plan's historical promotion gate. Track OOS decline as a separate guardrail; the Phase 2 report warns that only **eight OOS prompts** were labeled. A one-prompt change moves that rate by `1/8 = 12.5` percentage points. The 500 ms budget was applied to the bake-off's single-embed metric, so a fresh comparable latency measurement belongs in the ledger; a separate end-to-end measurement is needed before promising a chat service level.

| Future branch | Observation to collect | Bounded next action |
|---|---|---|
| **Retain and monitor** | Comparable full-harness in-scope result still clears the historical gate; OOS evidence does not show a stable regression; latency remains within the chosen budget | Keep the routing pair provisionally and expand the labeled OOS set. Record date, corpus, threshold, host, and model version. |
| **Recalibrate** | In-scope accuracy holds but OOS decline falls after a model, prompt-mix, or score-distribution change | Inspect per-prompt scores, sweep thresholds, and re-run the full harness before changing the configured pair. Do not assume the old `0.64` works for a different model. |
| **Compare or roll back** | A comparable run fails the historical in-scope gate, or a fresh measured latency gate fails | Reproduce the result, compare with the prior model under the same conditions, and use the plan's reversible routing configuration if rollback is warranted. |

These are **decision rules for investigation**, not claims that any branch has occurred. OOS evidence should be considered with its sample size and error type rather than a universal threshold copied from eight examples. A new model also needs its own routing and memory scope: the pinned plan deliberately decoupled routing from the persisted memory embedder. Extending a routing win to the memory store would be a different, migration-heavy decision.

### Practice exercise 3: see what calibration changed

In the Phase 2 threshold sweep, what did moving `bge-large` from `T=0.55` to `T=0.64` do to OOS decline and in-scope accuracy? Convert the OOS rates to counts using the report's eight OOS prompts.

> **Answer:** OOS decline moved from `0.375 = 3/8` to `1.000 = 8/8`, a gain of **five declined prompts** or **62.5 percentage points** in that validation sample. In-scope accuracy stayed `0.946`. This does not establish how many future, differently distributed OOS prompts will be declined.

### Practice exercise 4: test an over-tight threshold

At `T=0.72` the sweep reports in-scope `0.934`; at `T=0.75` it reports `0.916`. Which one beats the historical nomic `0.934` in-scope result, and by how much does `0.75` miss it?

> **Answer:** Neither beats `0.934`: `0.72` only **ties** it, while `0.75` is `0.934 - 0.916 = 0.018`, or **1.8 percentage points below** it. Both thresholds report OOS decline `1.000` in the small validation set, showing why OOS success alone is insufficient for a routing decision.

## 3. State the counterargument and falsifier

The strongest counterargument to treating `bge-large` as a durable winner is concrete. Its measured single-embed p95 was about 136.8 ms slower than nomic's in Phase 0. The OOS validation rate came from eight prompts, and the [plan's dated status](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/docs/plans/2026-06-16-ml-text-embedder-evaluation-plan.md#L124-L146) records a **local rerun of 7/8**, not the validation run's 8/8. A decision maker could reasonably favor the cheaper previous model if a fresh, comparable workload shows the measured quality gain is absent or latency cost exceeds the relevant budget. The pinned artifacts do not themselves show that this has happened.

A useful falsifier is therefore a fresh, versioned full-harness result at the actual configured threshold that falls **below the historical 0.934 in-scope gate**, or a comparable measured p95 that exceeds the agreed latency gate. A larger OOS set showing a reproducible decline problem would also force a threshold and candidate comparison. Record the denominator, prompt identities or stable corpus revision, host, and tool versions; otherwise apparent change may be measurement drift. Do not infer a monotonic trend from two runs of eight OOS examples, and do not extrapolate latency linearly from concurrency without measuring it.

### Practice exercise 5: interpret a small denominator

The Phase 2 validation reported OOS decline `8/8`; the later local rerun reported `7/8`. What are the two rates and their difference? Does this establish that routing quality deteriorated after shipping?

> **Answer:** `8/8 = 1.000` and `7/8 = 0.875`, a difference of **0.125**, or **12.5 percentage points**, caused by one prompt out of eight. The records alone do not establish a deterioration trend: they are two dated runs on a very small OOS set, and the lesson has not established identical prompts and conditions. The next useful check is a larger, versioned OOS evaluation alongside the full in-scope harness.

## Limits and project follow-up

This is a historical, revision-bound decision exercise. The pinned configuration is evidence of repository intent, not proof of what a live GA process is serving now. Phase 0 is a routing proxy, Phase 2 is a fuller harness, and neither is a long-term forecast. The eight OOS examples make rates coarse. The 500 ms comparison is based on the reported single-embed measurement against a chosen budget; a chat-path service-level claim requires its own measurement. A future candidate would also need calibration, harness-to-production threshold parity, and a reversible rollout. Nothing here authorizes a global memory re-embedding.

If new evidence arrives, update the trigger ledger before changing the model. A good entry names the observation, its source revision, which branch it selects, a counterargument, and the measurement that could reverse the decision. That creates an auditable future response without pretending to know when or whether the branch will occur. This English lesson is still a draft; subject review, a learner attempt, localization, and publication verification remain pending.

## Pinned sources

- [GA Phase 0 bake-off report and method](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/state/quality/embedder-bakeoff/bakeoff-latest.md) and [numeric results](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/state/quality/embedder-bakeoff/bakeoff-latest.json), both at `dc2e74cbd992a298f67efb928b5b3754615e1924`.
- [GA Phase 2 full-harness threshold sweep](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/state/quality/embedder-bakeoff/phase2-validation-2026-06-16.md), [decision plan](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/docs/plans/2026-06-16-ml-text-embedder-evaluation-plan.md), and [chatbot configuration](https://github.com/GuitarAlchemist/ga/blob/dc2e74cbd992a298f67efb928b5b3754615e1924/Apps/GaChatbot.Api/appsettings.json), at the same commit.
