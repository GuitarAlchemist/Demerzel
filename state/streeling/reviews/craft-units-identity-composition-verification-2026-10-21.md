# Craft course slice: units, identity and composition

Status: source drafts verified; human subject, fluent-language and learner reviews pending. No release, scene import or public publication is claimed.

## Source scope

Content and review-packet head: Demerzel `d89f9e91242c92205d900bf2baea0f55e3de0751`, compared with prior pilot head `93ab280e2ad4baa39e2823c8b6343ba8528576c8`. This report is a later evidence-only addition. Three new packages contain EN/FR/ES drafts, five answered exercises per locale, hand-derived JSON scenarios, a replay README, an answer-free learner task and exact-source review brief:

| Package | Project question | Evidence boundary |
|---|---|---|
| PHY-005 | How should IX crease-pattern thickness become physical and proposed scene lengths? | Pinned 28-ply/36-level crane assertions, dimensional derivations; no exporter or material test |
| SEM-004 | How does a face selection retain meaning after renumbering? | Pinned old-to-new controls and a synthetic inverse-map table; no persistent-ID or Godot selection implementation |
| CS-009 | Why must flat-connected faces be composed before checking stack constraints? | Pinned panel quotient/cycle/lower-bound implementation and hand-derived graph traces; no manufacturing proof |

Each review brief binds eight artifacts to content commit `6531ae9a0eb76f9402790f2b1b600c21330dfb66`. All 24 bound blobs still match the reviewed head. A bound packet is a review target, not an approval.

## Authoritative checks

- All three targeted `scripts/streeling_course_preflight.py` runs passed: production/research schemas, metadata, declared locale presence, English word counts, five answered exercises and unfinished review/publication flags.
- `pwsh scripts/verify.ps1` passed at content head `d89f9e9`: 804 Python tests with 2 skipped, ten IXQL grammar cases and BAML source/client parity. Verifier-only generated line-ending changes were restored afterward; course content was unchanged.
- In IX at `d7c22fdd6a62becb66b9d7246ea85850e7c55854`, the coordinator replayed `cargo test -p ix-origami --test thickness`: 11 passed, 0 failed. That checkout's source/test blobs match the course references. This scoped replay does not prove an engine import or physical construction.
- Independent arithmetic checks reproduced 60 physical conversion values, both permutation compositions and label/level transport, panel-cycle and DAG/lower-bound calculations. All nine locales have five exercise/answer pairs, all 21 relative links in those texts resolve, and all 24 review bindings match their sources.

No runtime code changed. Existing IX tests were reused without modification; arithmetic, local-link and source-identity checks are the evidence for these course/data edits. No new executable analyzer or duplicate product API was added.

## Static review and its limits

A separately dispatched adversarial reader inspected the three English lessons, fixtures, records, review packets, pinned IX implementation/tests and FR/ES mathematical qualifiers. It independently recomputed the 60 physical values and the permutation/graph examples, and returned **zero findings**. The coordinator's manual diff scan also found no content defect. This is a same-serving-family static preflight, not a human, learner or fluent-language approval.

The attempted Claude cross-model job returned terminal `done` with exit 0, but its verified result read found no artifact (exit 1). No Claude verdict or different-model corroboration is claimed. Execution policy then rejected the exact recursive cleanup of that terminal job folder; no alternate deletion was attempted. The CE lifecycle receipt is therefore **degraded**, and the terminal diagnostic folder remains local.

Code review: skipped (ce-code-review unavailable)

This line records the formal workflow fallback: cleanup policy prevented a completed CE lifecycle receipt. The explicit manual diff scan and collected static adversarial preflight above support retaining a reviewable draft source slice. They do not clear any production review flag or authorize publication.

## Learn generation

The unchanged Learn generator ran through `npm run sync:streeling -- --source <clean-d89f9e9-checkout> --out <isolated-preview>` and imported 21 departments, 148 English files and 108 French/108 Spanish files. The nine new generated pages each have the expected source heading as title and an exact `d89f9e9` source link. This was generation only: no Astro render, deployment or anonymous public readback was performed for this slice.

The strict source guard first rejected ignored Python caches under `state/streeling` after verification. Recursive cache cleanup was rejected by execution policy, so the caches were preserved and generation used a fresh detached checkout at the exact content commit. Existing Learn worktrees and their unrelated edits were preserved. This dogfooding result favors keeping a reproducible source snapshot available for generation; no timing comparison or general performance improvement was measured.

## Goal inventory and remaining gates

At `d89f9e9`, the inventory has **147 distinct core English course codes of 525**, 378 remaining, plus optional CYB-026 (148 English source files total). There are 23 modules with all six active-language files and **zero pipeline review approvals**. PHY-005, SEM-004 and CS-009 have EN/FR/ES drafts; PT/IT/DE remain absent. File counts and static preflight do not prove usefulness to a learner or publication.

Keep the goal active. Obtain the actual source-bound subject and language verdicts, raw learner responses and observed transfer, finish the required localization, then synchronize the reviewed source through Learn, deploy, and perform anonymous exact-source readback. The user will designate AUD-001's human reviewer; this slice does not fill that pending role.

## Integration changed before push

The pre-push read found Demerzel PR #1207 closed, unmerged, at `93ab280` on 2026-10-21T20:52:21Z. The owner's closing comment identifies the planned course-source move to Learn and keeps the pilot branch. The new local slice was not pushed to that closed PR and no replacement Demerzel PR was opened. Learn #197 is still a draft source-migration prototype; its body says fixtures and production/review records are outside that draft. This slice is preserved locally while the authoritative migration plan and integration point are checked. The 147 count above is a candidate-branch inventory, not the canonical or deployed catalog. A newly added IX Research department elsewhere does not silently expand the original 21-department/525-course goal.
