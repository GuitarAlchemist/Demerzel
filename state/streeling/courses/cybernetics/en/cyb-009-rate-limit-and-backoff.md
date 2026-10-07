---
module_id: cyb-009-rate-limit-and-backoff
department: cybernetics
course: "Operational feedback: admission and retry timing"
level: intermediate
prerequisites: [cyb-002-active-dampening-cross-repo-oscillation]
estimated_duration: "40 minutes"
produced_by: codex-local-authoring
research_cycle: null
pipeline_id: streeling-cyb-20261007
version: "1.0.0"
status: local_draft
---

# Rate Limits and Backoff: Two Different Clocks

> **Cybernetics** | Intermediate | 40 minutes | Provisional CYB-009

## Objectives

- Calculate admission times under a minimum-spacing rule.
- Compose that rule with capped exponential failure backoff and a server wait.
- Reject retries that exceed an attempt budget or deadline.
- Explain why slower retries do not resolve uncertain execution outcomes.

CYB-002 introduces rate limiting and exponential backoff as coordination mechanisms. Here we implement their distinct contracts. A rate limit constrains admitted work even when every attempt succeeds. Backoff changes retry timing after failure. Neither establishes permission to repeat an effect. The synthetic worker in this lesson performs no network operations; seconds are numbers, and a schedule is evidence of a timing rule, not measured service capacity.

## 1. Admission belongs to the shared resource

Our teaching resource permits one admission every three seconds, with no accumulated burst credit. If an attempt starts at time zero, the next start cannot precede time three. This differs from a token bucket that might allow several initial starts. State the precise limit before choosing a name: “four per twelve seconds” does not by itself specify whether four simultaneous starts are legal.

The controller checks the resource gate before each attempt, including retries. A retry queue bypassing that gate can overwhelm a resource even when the original queue is perfectly limited. Conversely, applying the gate only to failures leaves successful high-volume clients unbounded. In a shared implementation, admission must serialize across all clients using that resource. The fixture models one client only and does not claim distributed enforcement.

### Practice exercise and worked correction

Three tasks become ready at times 0, 1 and 2. What are their earliest starts with the stated gate, assuming instantaneous work and FIFO ordering?

**Correction:** 0, 3 and 6. Readiness is not admission. The second waits two seconds; the third waits four. Starting 0, 1, 2 would satisfy neither the three-second interval nor the intended resource protection. Long-running work would require an additional concurrency limit; start spacing alone does not cap simultaneous work.

## 2. Failure backoff composes with admission

Let consecutive failure count be k, starting at one after the first failed attempt. Define the teaching backoff as min(8, 2^k) seconds. Combine constraints by taking the latest eligible time:

```text
candidate = max(last_start + 3,
                response_received + min(8, 2^k),
                response_received + server_wait)
```

This is pseudocode for the actual `next_attempt` function. Admission spacing is measured from the previous start; failure backoff and a delay-seconds server wait are measured from receipt of the response. Assume instantaneous responses for the baseline: failures at starts 0, 3 and 7 make subsequent starts 3, 7 and 15. The first gate is controlled by admission, the next by four-second backoff, then eight-second backoff. Taking the minimum would violate whichever constraint is larger. A real response can arrive later than its request, so the two clock origins must stay distinct.

A server's HTTP `Retry-After` can express a date or nonnegative delay in seconds. Our input is already normalized delay-seconds; parsing dates and clock skew are outside this fixture. [RFC 9110 §10.2.3](https://www.rfc-editor.org/rfc/rfc9110.html#name-retry-after) defines that field. Do not infer that every failure carries it.

### Practice exercise and worked correction

At start 3, failure count two gives backoff four. The server requests ten seconds and its response arrives immediately at time 3. What is the next candidate? What if the operation deadline is 12? Repeat with the response arriving at time 5 and a deadline of 14.

**Correction:** With immediate receipt, max(6, 7, 13) = 13; deadline 12 makes that candidate inadmissible. With receipt at time 5, max(6, 9, 15) = 15; deadline 14 also denies admission. Reusing the request-start origin would incorrectly allow time 13. Reducing the server wait to fit the deadline would violate the declared contract. Record deadline exhaustion rather than silently extending the deadline.

## 3. Budgets, jitter and uncertain outcomes

Set a budget of four starts, including the original attempt. The valid sequence 0, 3, 7, 15 consumes it. Backoff saturates at eight seconds; it does not stop retries, so budget and deadline remain independent stopping conditions. A “maximum four retries” setting would instead allow five total starts. Name the counted unit explicitly in configuration and journal.

Many synchronized clients can share identical deterministic retry times. Marc Brooker's [AWS simulation of backoff and jitter](https://aws.amazon.com/blogs/architecture/exponential-backoff-and-jitter/) demonstrates how randomized timing reduces clustered contention in that model. Our deterministic fixture deliberately omits jitter to make arithmetic inspectable. It provides no fleet-performance result. Adding jitter requires rechecking admission and server-wait constraints after selecting a random delay.

Timing also cannot settle a timed-out effect. If a remote write might already have executed, first reconcile its identity and result or use a documented idempotency mechanism. CS-004 already teaches that distinction for an audio experiment; this course adds timing composition, without repeating the audio workflow.

### Practice exercise and worked correction

A timeout follows a submitted write; its outcome is unknown. A backoff timer expires. Is the write now safe to repeat?

**Correction:** No. The timer proves eligibility under a timing rule only. Preserve the logical operation identity and inspect available outcome evidence. An identical payload is not automatically idempotent. An unresolved result can require stopping even though every timing constraint passes.

## 4. Apply the contract to code and try to break it

From any directory, run the package's standard-library solution using its absolute path:

```text
python <package>/scripts/course-exercises/cyb_operations.py --json
```

The path placeholder must be replaced. Test ID `admission_backoff` reports inputs, expected and actual schedule, server wait, delayed response, deadline stop, budget stop and control verdicts. `valid_schedule` checks this fixed teaching sequence's origin zero, at most four starts, finite timestamps, every eligibility gap and the inclusive deadline 40. It rejects [0,1,2,3] and [0,3,6,9], which respects admission but ignores growing failure backoff. It also rejects [0,100], [0,39,40], an empty sequence and a missing timestamp. Returning false when no eligible next time exists avoids comparing a timestamp with `None`; spacing alone cannot enforce a deadline.

### Practice exercise and worked correction

Replace the mental schedule with [0,3,7,14]. Which constraint fails?

**Correction:** The third consecutive failure at time seven requires eight seconds, making fifteen earliest. The seven-second gap passes the resource interval but fails backoff. A validator that checks only adjacent spacing three would miss it. In a scratch copy, change the delay cap to four and predict 0,3,7,11 before running; restore no shared files.

## Assessment, journal and synthesis

Record conceptual belief state and evidence separately from exercise grades. Advance to behavioral assessment only for justified True with confidence >= 0.7; never infer or invent confidence from a score. Adapt teaching for Unknown, investigate Contradictory evidence, and follow the policy's three-attempt limit and escalation requirement if comprehension remains unresolved. These are assessment instructions; no belief transition or escalation has been performed.

Stage one is conceptual: explain admission versus failure count, calculate candidate thirteen, and explain unknown outcome. Award two points each; pass at five of six, with the unknown-outcome answer mandatory. This score is not a fabricated belief-confidence measurement.

Stage two is behavioral: independently change one fixture input, record the predicted schedule first, run it, and preserve a rejected negative case. Award one point for prediction, one for matching trace, one for budget/deadline evidence, and one for rejection explanation; require all four. A grader must observe this work before marking transfer learned, with the policy's bounded reassessment process.

Journal UTC, script hash, parameters, command, exit code, expected versus actual, and any mismatch. Synthesize: the controls demonstrate single-client timing composition and bounded attempts. They do not demonstrate distributed admission, jitter throughput, parser correctness, or safe duplicate effects. Keep these limitations beside the successful trace rather than converting a passing simulation into a production claim.

## Further reading and boundary

Preserve CYB-002 for coordination context and CS-004 for uncertain effect recovery. This provisional local draft has no learner outcome, independent review, translations or publication approval.

## Offline Solution

[Download the offline solution and executable controls](../../../../../scripts/course-exercises/cyb_operations.py).
