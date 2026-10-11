---
module_id: cyb-004-live-lane-admission-feedback
department: cybernetics
course: Live-Lane Admission as Bounded Feedback
level: intermediate
prerequisites: [cyb-002-active-dampening-cross-repo-oscillation, cyb-003-measuring-variety-ratio-quantitatively]
estimated_duration: "35 minutes"
produced_by: codex-project-pilot
research_cycle: cybernetics-2026-10-11-004
version: "0.1.0"
---

# Which Signal Should Close Gaia's Lane Admission Loop?

> **Department of Cybernetics** | Level: Intermediate | Estimated duration: 35 minutes | Status: English draft; subject, learner, localization, and publication review pending

## Objectives

After this lesson, you will be able to:

- Identify the sensed state, limit, comparison, and admission action in Gaia's lane registration path.
- Explain why a bus actor's stale timestamp does not by itself free a still-running peer surface's lane slot.
- Calculate the result of fixed positive and negative test fixtures at the default and experimental limits.
- State which control claim the deterministic tests support and which live-agent performance claim remains unmeasured.

## The project question

Gaia coordinates agent lanes through a bus and a peer surface tool. A coordinator sees four registered lanes whose bus actors have gone quiet. The peer tool still reports four surfaces as `running`. Should a fifth lane register on the default path? At pinned Gaia commit [`c94df3f5a53cd9f472e8a97b656dc23d7c940389`](https://github.com/GuitarAlchemist/gaia/tree/c94df3f5a53cd9f472e8a97b656dc23d7c940389), the answer is **no**: the [registration script](https://github.com/GuitarAlchemist/gaia/blob/c94df3f5a53cd9f472e8a97b656dc23d7c940389/scripts/wmux-lanes.mjs#L159-L212) counts registered lane actors whose peer surfaces are still reported running. It does not count only actors with recent bus activity. The [test fixture](https://github.com/GuitarAlchemist/gaia/blob/c94df3f5a53cd9f472e8a97b656dc23d7c940389/tests/wmux-adapter.test.mjs#L158-L191) makes this case deterministic by aging bus events and keeping the peer surfaces running.

This is a compact cybernetic case: a controller observes a variable, compares it with a limit, and either admits or refuses a requested change. The **choice of observed variable** determines whether the feedback is useful. A bus message's age is a signal about bus contact; it is not the same observation as a peer surface's running state. A running surface, in turn, does not prove its agent is making productive progress. This lesson tests the admission rule, not that stronger productivity claim.

[CYB-001](cyb-001-vsm-ai-governance-mapping.md) maps a broad governance model. [CYB-002](cyb-002-active-dampening-cross-repo-oscillation.md) proposes dampening mechanisms for cross-repo oscillation. [CYB-003](cyb-003-measuring-variety-ratio-quantitatively.md) separates configured state labels from measured regulatory capacity. CYB-004 narrows the view to one implemented Gaia gate, its feedback input, and a paired negative control. A limit is not automatically a queue, retry system, or measure of throughput.

## 1. Define the sensor and the controlled action

The [lane policy](https://github.com/GuitarAlchemist/gaia/blob/c94df3f5a53cd9f472e8a97b656dc23d7c940389/src/lanes.mjs#L21-L87) sets `DEFAULT_MAX_LIVE_LANES = 4`. Its `admitLane({ live, limit })` rejects when `live >= limit`, otherwise returns the next admitted position. The registration script first gets peer agents with `status === 'running'`, then builds a set of their surface IDs. It separately replays the bus log to find registered `wmux-lane` actors by surface ID. `liveBefore` is the number of surface IDs **in both sets**: registered on the bus and currently reported running by the peer. As the script considers unregistered running peer surfaces, it calls `admitLane` and increases the planned live count.

| Element | Pinned implementation | Meaning in this lesson |
|---|---|---|
| Sensor input | Peer-reported running surface IDs, intersected with registered bus lane IDs | Current **reported presence** of registered lanes |
| Reference value | Four supported live lanes by default | Admission limit for this workspace path |
| Comparator | `live >= limit` | Is there room for another lane? |
| Action | Plan registration or throw `LaneLimitError` | Admit or refuse; no automatic waiting queue |
| Recorded output | `liveBefore`, `laneLimit`, `plan`, and applied registrations | A receipt that can be checked against the fixture |

The command is a registration check, not a continuously running controller. A refusal blocks this call; the code shown does not schedule the request for later. The script defaults to a dry run unless `--apply` is passed. Its count depends on what the peer tool reports at that point and on its match with durable bus registrations. If either source is wrong or stale, the decision can be wrong even though the comparison arithmetic is correct.

### Practice exercise 1: apply the default cap

Four different running peer surfaces are already registered as bus lanes. A fifth running, unregistered surface is presented to `register --apply`, with no experimental option. What are `liveBefore` and the result? Does the command silently register only four of five?

> **Answer:** `liveBefore = 4`; the default `limit = 4`; `4 >= 4` makes `admitLane` throw before admitting the fifth. The [four-then-fifth test](https://github.com/GuitarAlchemist/gaia/blob/c94df3f5a53cd9f472e8a97b656dc23d7c940389/tests/wmux-adapter.test.mjs#L116-L139) expects a refusal and confirms only four bus lane actors afterward. It explicitly rejects silent truncation as the intended behavior.

## 2. A quiet bus actor is not a free slot

Gaia's bus can mark an actor `stale` when the actor has not spoken recently. The [regression test](https://github.com/GuitarAlchemist/gaia/blob/c94df3f5a53cd9f472e8a97b656dc23d7c940389/tests/wmux-adapter.test.mjs#L143-L191) ages bus events by ten minutes and appends a fresh Gaia heartbeat. That creates four lane actors that are stale **on the bus** while the fake peer-state fixture still reports all four surfaces running. The test then asks the registration command to recount. It expects `liveBefore = 4` and a fifth-lane refusal.

Why make the two clocks disagree? The script comments identify the prior defect: an earlier count used recent bus status. Since the product does not heartbeat each lane actor, a still-running lane could stop counting after the bus's 30-second stale window. Then lanes five through eight could be admitted on the default path. The correction uses peer-reported running surfaces for the lane cap. It preserves the useful distinction between **bus reachability** and **surface presence**. It does not establish that the surface's agent is actively working, responsive, or safe to interrupt.

### Practice exercise 2: classify the conflicting signals

In the fixed stale-bus test, four bus lane actors are `stale`, but all four matching peer surfaces are `running`. A fifth running surface appears. What count controls admission, and which observation would be wrong to substitute for that count?

> **Answer:** The intersection still contains four registered running surfaces, so `liveBefore = 4` and the fifth is refused at the default limit. Counting only bus actors with recent activity would incorrectly produce zero or fewer than four in this fixture. Bus staleness describes recent contact with the bus; it does not show that the peer surface exited.

## 3. The negative control: exited surfaces release capacity

A safe cap must also avoid becoming permanent. The bus event log is append-only, so a lane actor may remain in the log after its peer surface exits. If Gaia counted every actor ever registered, four historical registrations would block all future work. The [negative-control test](https://github.com/GuitarAlchemist/gaia/blob/c94df3f5a53cd9f472e8a97b656dc23d7c940389/tests/wmux-adapter.test.mjs#L215-L240) starts with four registered lanes. Its next fake peer snapshot reports lanes 1 and 2 still running, lanes 3 and 4 exited, and new lanes 5 and 6 running. The command reports `liveBefore = 2` and registers two new lanes. A further new lane 7 is refused: the live count is back at four.

Together, the stale-bus and exited-surface cases put pressure on **both sides** of the rule. The first prevents false free capacity; the second prevents false permanent saturation. Neither test measures actual throughput. Both use controlled peer-state and bus-log fixtures, which are good for a deterministic admission contract and insufficient for claims about mixed real-agent load.

### Practice exercise 3: free only the exited slots

After lanes 3 and 4 exit in that fixture, how many previously registered lanes count as live? How many of new lanes 5 and 6 can register at the default cap? What happens when lane 7 is added without another exit?

> **Answer:** Only lanes 1 and 2 still have running peer surfaces, so `liveBefore = 2`. Both new lanes 5 and 6 register, returning the live count to four. A later unregistered lane 7 would be the fifth live lane and is refused. Historical bus records for exited lanes do not consume the current cap.

## 4. Experimental limits are labels, not evidence upgrades

The policy distinguishes a supported default from an explicit experiment. The pinned [scale note](https://github.com/GuitarAlchemist/gaia/blob/c94df3f5a53cd9f472e8a97b656dc23d7c940389/docs/scale-and-lanes.md) calls four lanes supported by this product's acceptance run. Six is the next validation target and eight is unproven with real Claude/Codex lanes. The code refuses a requested limit above four unless `--experimental-lanes` is provided, and it refuses above eight even with that flag. The flag records operator acceptance of an unproven range; it does not transform synthetic writer probes into real-agent throughput evidence.

The [experimental-limit tests](https://github.com/GuitarAlchemist/gaia/blob/c94df3f5a53cd9f472e8a97b656dc23d7c940389/tests/wmux-adapter.test.mjs#L242-L267) exercise both edges. A request for six without the flag fails. Six with the flag registers in the deterministic fixture and marks the limit experimental. Nine with the flag fails because it exceeds the hard experimental ceiling. Another regression fixture puts eight running surfaces in the fake peer state after the original four bus actors become stale; the default registration still refuses at lane five, so waiting out a timestamp cannot silently unlock eight.

### Practice exercise 4: choose the allowed request

For otherwise identical six-surface fixtures, compare `--max-lanes 6 --apply` with `--max-lanes 6 --experimental-lanes --apply`. Then evaluate `--max-lanes 9 --experimental-lanes --apply`. Which requests pass policy, and what does passing say about real-client validation?

> **Answer:** Six without the experimental flag is refused. Six with the flag is allowed by policy and labeled experimental in the test output. Nine is refused even with the flag because the ceiling is eight. Successful six-lane registration in this fixture does **not** prove real Claude/Codex performance at six; the policy and scale note say that validation is still missing.

## 5. Counterargument, falsifier, and measurement boundary

The strongest counterargument to counting peer-reported `running` surfaces is that running is a coarse signal. A surface may be idle, hung, or inaccurately reported by the peer tool. Refusing a fifth lane can leave useful execution capacity unused. But treating bus silence as an automatic slot release was demonstrably unsafe for the stated cap: a lane can think without calling the bus. A better controller would need a separately tested way to determine whether a lane is truly releasable, with receipts for handoff, termination, or recovery. This lesson does not invent that mechanism.

The rule has clear falsifiers. Under the fixed conditions of four registered peer-running surfaces and the default limit, an applied fifth registration would contradict the intended contract. Under the paired negative control, an exited peer surface continuing to consume one of the four slots would also contradict it. In real operation, record the peer snapshot, matching bus surface IDs, requested limit, experimental flag, registration receipt, and time. Then separately measure queue delay, throughput, per-call latency, lock contention, and failures under **real mixed Claude/Codex lanes** before raising a supported limit. The scale note says the existing identical-Node-worker probes establish log integrity and replay behavior, not those real-client performance properties or recovery from a wedged lock.

### Practice exercise 5: reject a false default-path success

A deterministic fixture reports eight peer surfaces running, of which four are already registered bus lanes. All four bus actors are stale. The command requests default `register --apply`, without `--max-lanes` or `--experimental-lanes`. At which proposed new lane must planning stop, and how many registered lanes should remain in the test's status readback?

> **Answer:** The four already registered peer-running surfaces make `liveBefore = 4`. The first new surface would be lane 5, so planning stops at that admission check and refuses the command. The [eight-surface regression test](https://github.com/GuitarAlchemist/gaia/blob/c94df3f5a53cd9f472e8a97b656dc23d7c940389/tests/wmux-adapter.test.mjs#L193-L213) expects four registered lanes afterward, not eight. Bus staleness does not grant an experimental limit.

## Sources and limits

- [Gaia `src/lanes.mjs`](https://github.com/GuitarAlchemist/gaia/blob/c94df3f5a53cd9f472e8a97b656dc23d7c940389/src/lanes.mjs), [registration script](https://github.com/GuitarAlchemist/gaia/blob/c94df3f5a53cd9f472e8a97b656dc23d7c940389/scripts/wmux-lanes.mjs), [deterministic adapter tests](https://github.com/GuitarAlchemist/gaia/blob/c94df3f5a53cd9f472e8a97b656dc23d7c940389/tests/wmux-adapter.test.mjs), and [scale evidence note](https://github.com/GuitarAlchemist/gaia/blob/c94df3f5a53cd9f472e8a97b656dc23d7c940389/docs/scale-and-lanes.md), all pinned to `c94df3f5a53cd9f472e8a97b656dc23d7c940389`.
- Source inspection supports the implemented admission rule and the test fixture's expected results. These tests were not rerun for this lesson. No live wmux surfaces were inspected or controlled, no real mixed-agent load was measured, and no learner or subject review has occurred. The English draft has not been localized or published.
