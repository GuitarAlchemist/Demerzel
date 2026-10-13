# Streeling batch 15: evidence-dependent and craft-to-scene drafts

Date: 2026-10-12. Source evidence head: Demerzel `bd040bca74bee8e8f54987724d5c7b6614a7d3bd`. This is an engineering receipt, not a subject, language, learner, or publication approval.

## Source and local checks

| Item | Observation | Boundary |
|---|---|---|
| NET-003 | Five AI-drafted translations align with the offline selector replay; production translation phase is complete. `python scripts/streeling_net003_replay.py` matched pinned selector/policy blobs, four mode counts, and three controls. Course preflight passed. | Fluent review and live routing evidence are absent. |
| NET-004 | New 1,639-word English draft with five answered exercises; production preflight passed. Independent AI adversarial review found a one-edge graph-cut error, a circular learner gate, and an overstated research method. Source now uses an explicit AND prerequisite, an optional accessible prepublication pilot, and `thought_experiment`. | Proposed semantic backpressure and DSL notation have no runtime or baseline comparison. Human review remains false. |
| VC-005 | New 1,766-word English draft with five answered craft-to-scene exercises; production preflight passed. It pins Learn's GLB cleanup script, checker, and expected report at `93d424f872a576ba8bbcd3dd44c9733292373654`. | The expected sample report is checked-in reference data, not a fresh Blender/Godot or craft-asset run. Human review remains false. |
| Learn preview | `node scripts/sync-streeling.mjs --source <clean Demerzel checkout> --out <isolated directory>` at `bd040bc` generated 21 department directories, 110 EN / 80 FR / 80 ES modules; NET-003, NET-004, and VC-005 output pages carry the source SHA and rewritten source/receipt links. | The isolated output was not committed, built, deployed, or read back publicly. |
| Demerzel CI | Governance validation, unit tests, backlog-facts, BAML drift, risk report, and CodeQL checks passed at `bd040bc`. `detect-and-review` failed before content review with `llm_call: API error: invalid x-api-key`. | Failed review is an unavailable verdict, not acceptance or rejection of course content. |

The source reporter at `bd040bc` found 21 course directories, 23 department records, 110 English drafts, 109 distinct core codes in slots 001–025, 416 core slots remaining under the provisional 21-directory denominator, 23 six-language source sets, and zero approved pipeline reviews. Issue #1209 holds the denominator decision.

## Dogfooding result: the zero-filter contract

VC-005 originally proposed `--min-part 0` to preserve a small intentional knot. Inspecting Learn's pinned `remove_small_parts()` showed that the zero path returned `[]`, while its `run()` caller unpacks `(removed, loose)`. The defect also existed on Learn main `3f4de745f56e81f237159997473253546d7f6d64`. A focused source-level call of the baseline function raised `ValueError: not enough values to unpack (expected 2, got 0)`; the same call against the one-line fix returned `([], 0)` for zero and a negative fraction. Draft [Learn PR #168](https://github.com/spareilleux/learn/pull/168) contains that change. The VC-005 exercise now uses `--min-part 0.001`, whose 0.1% threshold is below its synthetic 20-face feature in a 5,140-face mesh. No Blender executable was available on this host, so the full cleanup path remains untested here.

The useful loop was: write a concrete project exercise, test the exact command and return contract, correct the lesson, isolate the code fix, and retain both source and test limits. For future craft assets, a `feature -> transformation -> preservation check` declaration is only a candidate. Compare it against the existing pipeline plus an external manifest and human checklist before adding a DSL or gate. A real Godot trial must version an asset, run Blender, import into the scene, save raw captures, and measure feature recognition and frame cost under fixed settings.

## Remaining gates

The AUD-001 human reviewer has not yet been named. The 21-versus-23 department denominator is unresolved. NET-004 and VC-005 need human subject and learner review, translations, a Learn build, accepted source, deployment, and anonymous public readback. Learn PR #168 needs a Blender runtime check before its fix is claimed end-to-end. Demerzel PR #1207 and the separate Cybernetics PR #1195 remain drafts; neither should be described as published content.
