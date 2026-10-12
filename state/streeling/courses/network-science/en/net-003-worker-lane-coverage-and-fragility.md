---
module_id: net-003-worker-lane-coverage-and-fragility
department: network-science
course: "Measure Worker-Lane Coverage Under a Mode Cut"
level: intermediate
prerequisites: [net-002-capability-graphs-and-projections]
estimated_duration: "35 minutes"
produced_by: codex-project-pilot
research_cycle: network-science-2026-10-11-003
version: "0.1.0"
---

# Measure Worker-Lane Coverage Under a Mode Cut

> **Department of Network Science** | Intermediate | 35 minutes | English draft; review and publication pending

## Objectives and project question

You will build a worker-to-work-class graph from a pinned Demerzel lane policy, measure coverage and the effect of removing one worker, then test where the graph loses information about individual roles and decision outcomes. **Project question:** if the advisory fan-out mode changes or a worker lane becomes unavailable, which *declared work classes* still have a named route? The answer can help choose a lane or identify a review question. It cannot establish that any worker is online, authorized to act, or has completed work.

[NET-002](net-002-capability-graphs-and-projections.md) connects *repositories* to shared capability-family labels. This lesson instead connects *workers* to assigned roles and their work classes. Its edges come from [Demerzel's worker-lane policy at commit `ecdc6c2`](https://github.com/GuitarAlchemist/Demerzel/blob/ecdc6c27559bb1a11343cfad33687465893e9891/state/driver/aiw-worker-lanes.json) and are filtered by a requested mode. No MCP route or live staffing state enters this graph.

## 1. Define the graph before measuring it

The pinned policy declares five workers, `jules`, `claude`, `gemini`, `codex`, and `augment`, each with one `primary` role, a list of `secondary` roles, and a separate `forbidden` list ([worker definitions](https://github.com/GuitarAlchemist/Demerzel/blob/ecdc6c27559bb1a11343cfad33687465893e9891/state/driver/aiw-worker-lanes.json#L54-L79)). Every named role maps to a `work_class` ([role definitions](https://github.com/GuitarAlchemist/Demerzel/blob/ecdc6c27559bb1a11343cfad33687465893e9891/state/driver/aiw-worker-lanes.json#L19-L51)). The policy describes itself as **advisory/dry-run**. It is a routing proposal, not a receipt for actual work.

Construct a three-layer directed graph `worker → assigned role → work class`. Draw the first edge only for a worker's *primary or secondary* role; do not turn a forbidden role into a route. Draw the second edge using the role's `work_class`. For a requested mode, hide paths whose work class appears in [`mode_blocks`](https://github.com/GuitarAlchemist/Demerzel/blob/ecdc6c27559bb1a11343cfad33687465893e9891/state/driver/aiw-worker-lanes.json#L81-L86). A worker-class edge exists in the two-layer projection when at least one surviving assigned-role path connects them. Multiple roles of the same class count as **one** worker-class edge. We count *distinct worker choices for a class*, not worker capacity or number of completed tasks.

This is deliberately narrower than the policy's full `work_classes` dictionary. It lists 13 names, including forbidden actions, but only five work classes occur in any primary or secondary assignment: `fix`, `groom`, `navigate`, `net_new_feature`, and `review`. Call that set `A`. For comparison across modes, define **coverage** `C(m) = |{c in A: degree_m(c) > 0}| / |A|`. Define **redundant-class count** `R(m) = |{c in A: degree_m(c) >= 2}|`. These are descriptive graph metrics. They do not say that two named workers are interchangeable for the same role.

### Practice exercise 1: avoid double-counting roles

In NORMAL mode, `claude` has `draft_to_ready_helper`, `test_author`, and `review_feedback_applier`, all mapped to `fix`, plus `builder_fixer` mapped to `net_new_feature` and `lightweight_groomer` mapped to `groom`. What is `claude`'s degree in the worker-class projection, and how many assigned-role paths does it have? Why do the answers differ?

> **Answer:** Its projected degree is **3**: `fix`, `net_new_feature`, and `groom`. It has **5** assigned-role paths, one primary and four secondary. Three distinct `fix` roles collapse into one worker-class edge. Counting the five roles as five alternative workers would falsely inflate class redundancy.

## 2. Measure a mode cut

Reading the pinned primary and secondary assignments yields the following projected graph. A `1` means at least one assigned-role path survives that mode's class block. The table shows NORMAL before any mode cut:

| Worker | `fix` | `groom` | `navigate` | `net_new_feature` | `review` |
|---|---:|---:|---:|---:|---:|
| `jules` | 0 | 1 | 0 | 0 | 1 |
| `claude` | 1 | 1 | 0 | 1 | 0 |
| `gemini` | 0 | 0 | 0 | 0 | 1 |
| `codex` | 1 | 0 | 0 | 0 | 1 |
| `augment` | 0 | 0 | 1 | 0 | 0 |

The matrix has **9** worker-class edges. Its class degrees are `fix:2`, `groom:2`, `navigate:1`, `net_new_feature:1`, `review:3`. Thus `C(NORMAL)=5/5` and `R(NORMAL)=3`. The pinned mode policy blocks `net_new_feature` and `broad_architecture` in CONSTRAINED, and those plus `workflow_policy_change` in DRAINING. Because only `net_new_feature` among these has an assigned path, **both** modes leave 8 edges and four covered classes: `C=4/5`, `R=3`. HALTED blocks `fix`, `groom`, and `navigate` as well, while `review` is absent from its block list. It leaves three worker-class edges, all to `review`: `C(HALTED)=1/5`, `R(HALTED)=1`. That last ratio is not a green light for operations in a halted system; it merely describes the surviving review declarations under this filter.

### Practice exercise 2: compute the cut, not an outage

In DRAINING, which NORMAL worker-class edge disappears, what are `C` and `R`, and does the calculation prove that a Claude agent actually stopped working?

> **Answer:** Only `claude → net_new_feature` disappears, because that is the sole assigned edge of the blocked class. Eight of the nine projected edges remain; four of the five assigned classes remain covered, so `C=4/5`, and `fix`, `groom`, and `review` still have degree at least two, so `R=3`. This is a policy-graph cut, not evidence about a running Claude agent or a real dispatch.

## 3. Test single-worker fragility

For a mode `m` and removed worker `w`, define `L_m(w)` as the number of classes covered before removal but uncovered afterward. Recompute degrees after deleting `w` and its assigned-role paths. In DRAINING, `augment` is the only worker with a `navigate` edge; removing it changes `navigate`'s degree from 1 to 0, so `L_DRAINING(augment)=1` and coverage falls from `4/5` to `3/5`. Removing any of the other four workers loses **zero entire classes**: their surviving classes have another named worker. This is a vertex-deletion sensitivity check, not a prediction of failure probability. A worker can be unavailable for reasons not recorded in this JSON, and a different worker sharing a *class* might not have the exact role needed for a task.

The difference between class redundancy and role redundancy matters. `review` has three worker neighbors in DRAINING, yet `gemini`'s primary `read_only_critic`, `jules`'s secondary `architecture_summarizer`, and `codex`'s secondary review roles are different assignments. The graph says a broad review-class route remains after losing one worker. It does not say that every requested review role has three substitutes. An escalation or reassignment may still be necessary.

### Practice exercise 3: remove a vertex

Compare removing `augment` with removing `codex` from the DRAINING graph. State the lost classes and the resulting coverage in each case. Can the graph alone tell whether the replacement review notes would be equally good?

> **Answer:** Removing `augment` loses `navigate` and leaves `fix`, `groom`, and `review`, so coverage is `3/5`. Removing `codex` loses no whole class: `claude` still has `fix`, and `jules` and `gemini` still have `review`; coverage stays `4/5`. Neither result measures quality, permissions, exact-role equivalence, availability, or task completion.

## 4. Keep selector semantics alongside the graph

The pinned [advisory lane selector](https://github.com/GuitarAlchemist/Demerzel/blob/ecdc6c27559bb1a11343cfad33687465893e9891/scripts/aiw_lane_selector.py#L1-L19) consumes the policy. It checks an unknown worker, an unknown mode, a worker's forbidden roles, whether a requested role is assigned to that worker, and then whether the role's class is blocked ([decision order](https://github.com/GuitarAlchemist/Demerzel/blob/ecdc6c27559bb1a11343cfad33687465893e9891/scripts/aiw_lane_selector.py#L77-L154)). A primary assigned role in an unblocked class yields `allow`; a secondary yields `recommend`, not `allow`. A forbidden role yields `block` **before** the selector even tests role membership. A role absent from the lane yields `warn`. A mode-blocked assigned role yields `block` with a backpressure reason code. These are responses constructed by code, not permissions to mutate state. The script says exit code 0 means **evaluated**, while the decision is in the JSON payload; an input/policy error can exit 2.

For example, in DRAINING, `claude`'s primary `builder_fixer` maps to blocked `net_new_feature`, while its secondary `test_author` maps to unblocked `fix`. The selector source predicts `block` for the first request and `recommend` for the second. That does **not** mean a `test_author` can fulfill a feature-building task; the requested role and expected output must still match the work. `codex`'s `autonomous_merge_actor` is explicitly forbidden, so its request predicts `block` even if one were to change the mode. No edge in the projected graph licenses a merge.

### Practice exercise 4: distinguish paths from decisions

In DRAINING, predict the selector's decision for `(claude, builder_fixer)`, `(claude, test_author)`, and `(codex, autonomous_merge_actor)`. Why would recording only the projected worker-class graph lose information needed for the last request?

> **Answer:** The first is `block` because `net_new_feature` is mode-blocked; the second is `recommend` because `test_author` is an unblocked *secondary* `fix` role; the third is `block` because `autonomous_merge_actor` is in `codex`'s forbidden list. The projection contains primary/secondary class reachability but does not encode forbidden-role membership or the selector's check order. A missing merge edge must not be treated as a mere unknown-role warning or as permission.

## 5. Make the metric falsifiable

The counts above were recomputed from the **pinned JSON** by expanding each worker's primary and secondary roles, mapping them to work classes, filtering `mode_blocks`, and deduplicating `(worker, class)` pairs. To check the *selector interpretation* separately, propose a small offline replay against that same pinned script and policy: enumerate the 22 assigned `(worker, role)` pairs in each of the four modes; classify `allow` and `recommend` as unblocked assigned paths and `block` as mode-cut paths. The source predicts 22 active role paths in NORMAL, 21 in CONSTRAINED and DRAINING, and 8 in HALTED. Their projected worker-class edge counts should be 9, 8, 8, and 3. The number of surviving **primary** paths should be 5, 4, 4, and 1. These are predictions from the checked-in policy and selector, not results of a replay performed for this lesson.

Store the selector JSON for each request with the pinned SHA and compare decisions rather than process exit codes. Include at least one forbidden request, one unknown role, and one unknown mode as separate control cases; none belongs among the 22 assigned pairs. A discrepancy between predicted and observed decisions would falsify the assumed path rule or reveal drift in the replayed source. Agreement would validate this bounded model for the tested revision; it would not establish live scheduling, worker health, or correct human governance.

### Practice exercise 5: design the replay oracle

Suppose the replay yields exit code 0 for `(claude, builder_fixer, DRAINING)` and a JSON decision of `block`. A teammate counts that as an active path because the process succeeded. What is the correct classification? Give one count whose disagreement with the predictions above would falsify this lesson's graph extraction.

> **Answer:** It is a **blocked assigned-role path**. Exit code 0 says the advisory request was evaluated, not allowed. The replay should find 21 unblocked assigned-role paths in DRAINING and 8 distinct worker-class edges after projection; observing, for example, 22 unblocked paths or 9 projected edges with the pinned policy and script would falsify the extraction. It would not by itself prove a production incident.

## Evidence and limits

- The [lane policy](https://github.com/GuitarAlchemist/Demerzel/blob/ecdc6c27559bb1a11343cfad33687465893e9891/state/driver/aiw-worker-lanes.json) and [selector](https://github.com/GuitarAlchemist/Demerzel/blob/ecdc6c27559bb1a11343cfad33687465893e9891/scripts/aiw_lane_selector.py) are pinned to Demerzel commit `ecdc6c27559bb1a11343cfad33687465893e9891`. The counts are a reproducible calculation from that JSON, not a measurement of active agents. The replay in §5 is proposed and was not run for this lesson.
- The graph collapses distinct assigned roles into work classes. It excludes forbidden roles from its paths and does not encode the selector's full decision order, inputs, or authority. `allow` and `recommend` are advisory payload values; neither is a completion receipt.
- Worker deletion and mode cuts are sensitivity experiments on a static declared graph. Before making an operational routing claim, inspect current policy revision, the actual request and decision payload, worker presence and permissions, and the task artifact or receipt. Subject review, learner attempts, translation, Learn sync/build, and anonymous public readback remain open.
