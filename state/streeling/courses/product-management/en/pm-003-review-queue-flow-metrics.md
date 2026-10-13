---
module_id: pm-003-review-queue-flow-metrics
department: product-management
course: "Measure the Streeling Review Queue Without Counting Drafts as Throughput"
level: beginner
prerequisites: [pm-002-release-evidence-gate]
estimated_duration: "30 minutes"
produced_by: codex-project-pilot
research_cycle: product-management-2026-10-11-003
version: "0.1.0"
---

# Measure the Streeling Review Queue Without Counting Drafts as Throughput

> **Department of Product and Project Management** | Level: Beginner | Estimated duration: 30 minutes | Status: English draft; subject, learner, language, and publication gates open

## Objectives

After this lesson, you will be able to:

- Name the unit, boundary, and time window for review work in progress (WIP) and completed-review throughput.
- Use the Streeling source inventory as a dated snapshot without calling its draft count a flow rate.
- Calculate queue balance from a small event ledger and identify measurements the current artifacts cannot supply.

## The project question

The team wants to know whether Streeling's human review queue is growing faster than reviewers can finish courses. A dashboard shows **81 English source modules**. How many reviews were completed last week? The answer is **unknown** from that number. A source count is a stock of files at one revision. Review throughput is a count of modules that crossed an agreed completion boundary during a specified interval. [PM-002](pm-002-release-evidence-gate.md) explains the separate release gates; this lesson measures movement between them.

Use the [Demerzel progress script](../../../../../scripts/streeling_course_progress.py) and [curriculum's dated inventory](../../../../../docs/specs/streeling-project-curriculum-2026-10-04.md) as the project case. In a clean source-tree snapshot at Demerzel commit `0220ca84a25f59973bd6b9236cc00b7f68631a50` on October 11, 2026, `python scripts/streeling_course_progress.py` reported **81** authored EN modules across **21** course directories, **16** modules with all active-language files, and **0** modules with an approved production-record review. The script also found **23** department definition records. These counts are tied to that revision and directory-based scope; rerunning on a later checkout can change them.

The curriculum records **78** EN source modules across 21 directories at an earlier October 11 pilot state. The difference, `81 - 78 = 3`, is a **net change in source inventory across those observations**. It is not three completed reviews. Even an unchanged denominator would not reveal whether files were added, removed, renamed, or revised between snapshots.

### Practice exercise 1: label the units

A status card says “78 → 81 modules on October 11, so throughput was 3 courses.” Repair the card using the exact unit and missing boundary.

> **Answer:** “The English source inventory rose by a net three module files between the two dated observations.” It cannot say review throughput: neither number counts an approval event within a defined window. The earlier 78 is a dated curriculum observation; 81 is the pinned `0220ca8` script snapshot.

## 1. Define the queue before counting it

For this exercise, count **one module ID once**, even when its course has six translations or several review tasks. Entry occurs when a coordinator records the module as ready for review and assigns its review work. Exit occurs when its required subject, fluent-language, and learner findings are resolved and an approved production review is recorded, or when the coordinator explicitly withdraws it. A returned draft stays in WIP until one of those exits; otherwise a rework loop could make the queue look smaller without reducing unfinished work. Record the module ID, entry time, exit time, exit reason, and source revision in an event ledger.

The current [progress script](../../../../../scripts/streeling_course_progress.py) scans source files and production JSON. Its `authored_en` count includes English Markdown modules. Its `pipeline_review_approved` signal requires `review.completed: true` **and** `verdict: approved` in a matching production record. It does not reconstruct when a review entered or left a queue. At the pinned `0220ca8` snapshot, the 12 production records contain one `review_pending` status, for [DV-001](../../../course-productions/cp-data-visualization-2026-10-04-001.json), and eleven `in_progress` statuses. That single `review_pending` record is a **status proxy**, not a measured queue census: there is no required entry event, ownership timestamp, or guarantee that all review-ready drafts already have records.

The [DV-001 review brief](../../../reviews/dv-001-review-brief.md) demonstrates the distinction. It says the human subject, fluent-language, and learner gates remain open. Its bounded AI checks and the six language drafts make review work visible but do not complete those gates. A module with open work can be valuable source content while contributing zero approved-review completions.

### Practice exercise 2: read the snapshot honestly

At `0220ca8`, the script reports 81 authored EN, 16 active-language-complete, and 0 approved production reviews; the status scan finds one `review_pending` module. Which of these is verified WIP, and which is weekly throughput?

> **Answer:** None is a verified review-queue WIP census or weekly throughput. The one `review_pending` module is a record-status proxy at one revision. The 81 and 16 count source-file states, and 0 counts approved modules at that snapshot. Without event times and a consistent queue-entry rule, no weekly arrival or completion rate follows.

## 2. Count movement with an explicit window

The following ledger is a **synthetic teaching fixture**, not an observed Streeling history. Its window is `[2026-10-05 00:00 UTC, 2026-10-12 00:00 UTC)`: start included, end excluded, exactly seven days. At the start, modules A and B are in review WIP. A module remains in WIP during requested revisions. The ledger uses five distinct module IDs; a module may appear in more than one event.

| Time (UTC) | Module | Event | Review WIP effect |
|---|---|---|---:|
| Oct 6, 09:00 | C | Ready for review; enters queue | +1 |
| Oct 7, 16:00 | A | Required reviews approved; exits | -1 |
| Oct 8, 11:00 | D | English draft authored; no review entry | 0 |
| Oct 9, 14:00 | B | Returned for correction; stays assigned | 0 |
| Oct 10, 12:00 | E | Ready for review; enters queue | +1 |
| Oct 11, 18:00 | C | Explicitly withdrawn; exits | -1 |

Opening WIP is 2. Two entries, one approved exit, and one withdrawal give closing WIP `2 + 2 - 1 - 1 = 2`: B and E. **Completed-review throughput is one module per seven-day window**, A. C's withdrawal is an exit for queue balance but not a completed review. D's new draft is an authoring event, not a review arrival. Do not mix this fixture's counts with the actual 81-module snapshot.

### Practice exercise 3: reconcile the queue

Using only the synthetic ledger, calculate closing review WIP and list its IDs. Would moving B to “needs revision” outside the review board change the unfinished work?

> **Answer:** Closing WIP is `2 opening + 2 entries - 1 approval - 1 withdrawal = 2`, comprising B and E. Relabeling B would not finish it. Under this lesson's queue rule it remains WIP while correction is requested; a different board rule must be declared before comparing counts.

### Practice exercise 4: calculate completed flow

For the fixture's seven-day window, report approved-review completions, withdrawals, and authored drafts separately. What happens if a dashboard treats every exit as “reviews shipped”?

> **Answer:** One approved-review completion (A), one withdrawal (C), and one authored draft without review entry (D) are recorded. Calling both exits “reviews shipped” would report two and overstate approved-review throughput by one. The ledger does not record public Learn publication at all.

## 3. Expose missing times and scope changes

Lead time needs both a module's queue-entry and approved-exit timestamps. A's entry preceded the fixture window but its exact time is unspecified, so its review lead time cannot be calculated. At the closing instant, E has been in this defined queue for **36 hours**, from October 10 at 12:00 UTC to October 12 at 00:00 UTC. B's age is unknown because its entry time is not supplied. Do not average one known age with an unknown age or silently assign B the window start.

For real Streeling work, save an immutable event ledger before charting arrival rate, completed-review throughput, age, or lead time. Pin a source revision, use the same module-ID unit and entry/exit rule throughout a comparison, and report the UTC interval. Keep subject, language, learner, Learn build, and public-readback stages separate if their queues have different owners. A `timestamp` on a production JSON record says when that record was last written; it does not by itself identify a transition time. The [dated public baseline](../../../reviews/public-baseline-2026-10-11.md) concerns anonymous Learn access, not review flow.

### Practice exercise 5: write a usable dashboard caption

Write two sentences using the pinned `0220ca8` project snapshot and the synthetic fixture without presenting the fixture as an observed team result. Include one next measurement action.

> **Answer:** “At Demerzel `0220ca8`, the source scan found 81 English modules and zero modules with an approved production review; one record had `review_pending` status, but this is not a timed queue census. In a separate synthetic seven-day ledger, review WIP closes at two and approved-review throughput is one; to measure Streeling's real flow, record module-level review entry, approved exit, and withdrawal events with UTC timestamps and stable rules.”

## Key takeaways

- Source inventory and localization coverage are stocks. A review completion rate requires dated transition events and a declared window.
- Queue balance counts arrivals and all exits; completed-review throughput counts only approved exits under this lesson's rule.
- A status field and last-written timestamp are useful triage signals, but they cannot reconstruct historical WIP, lead time, or throughput.

## Project evidence and limits

- Demerzel commit `0220ca84a25f59973bd6b9236cc00b7f68631a50`: [progress script](../../../../../scripts/streeling_course_progress.py), [dated curriculum inventory](../../../../../docs/specs/streeling-project-curriculum-2026-10-04.md), [DV-001 production record](../../../course-productions/cp-data-visualization-2026-10-04-001.json), and [open review brief](../../../reviews/dv-001-review-brief.md). The clean-tree script output and production-record scan described above were observed for that commit; a later working tree may differ.
- The six-event A–E ledger is invented for arithmetic practice. It supplies no evidence about actual Streeling reviewers, cycle time, or publication.
- PM-003 remains an English draft. Human subject review, a learner attempt, fluent localizations, Learn sync/build, and anonymous public readback have not been completed.
