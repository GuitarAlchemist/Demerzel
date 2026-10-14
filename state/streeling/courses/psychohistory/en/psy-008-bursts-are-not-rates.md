---
module_id: psy-008-bursts-are-not-rates
department: psychohistory
course: "Bursts Are Not Rates: Event Arrivals in the Trigger Log"
level: intermediate
prerequisites: ["psy-002-governance-phase-transitions", "mat-009-estimation-uncertainty-sampling"]
estimated_duration: "40 minutes"
produced_by: claude-psychohistory-path
research_cycle: psychohistory-2026-10-13-008
version: "0.1.0"
---

# Bursts Are Not Rates: Event Arrivals in the Trigger Log

> **Department of Psychohistory** | Intermediate | 40 minutes | English draft; human subject and learner review pending

## Objectives and project question

You will turn an event log into counts per calendar day, compare them with what a constant rate would produce, measure the gap with the index of dispersion, and replace a misleading mean with figures a plan can use. **Project question:** the archived trigger log holds 594 events over 119 calendar days, 100 of them active. Is an average of "about five events a day" a usable description for planning?

[PSY-002](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/state/streeling/courses/psychohistory/en/psy-002-governance-phase-transitions.md) reads a doubling of the rate of conscience signals over three cycles as a sign that a transition is near (its fifth signal). A rate is a mean; this module asks what a mean says about a log whose events come in bursts. [PSY-009](psy-009-concentration-and-heavy-tails.md) measures the same log's concentration, [PSY-022](psy-022-competing-explanations.md) compares count models on it, and [PSY-024](psy-024-the-single-actor.md) asks who sent the events.

## 1. Count per calendar day, empty days included

**Observed.** Until it was retired on 2026-07-18, the workflow [`demerzel-driver-triggers.yml`](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/.github/workflows/demerzel-driver-triggers.yml) wrote one JSON file, a *trigger*, for each push to the main branch, issue opened or reopened, discussion created, or failed run of four other workflows. [`state/triggers/archived/`](https://github.com/GuitarAlchemist/Demerzel/tree/4b03838800dcd4894f1e026461979bff1d985ca8/state/triggers/archived) holds 594 of them, stamped from 2026-03-20 to 2026-07-16, of three types only: 252 `discussion_created`, 207 `push` and 135 `issue_opened`. [`extract.py`](../../../../../scripts/streeling_fixtures/psychohistory/psy-008/extract.py) reads all 594 at commit `4b03838`, refuses a folder that differs from its pinned digest, and writes one row per event into [`observed-input.json`](../../../fixtures/psychohistory/psy-008/observed-input.json). The few trigger files [outside the archive](https://github.com/GuitarAlchemist/Demerzel/tree/4b03838800dcd4894f1e026461979bff1d985ca8/state/triggers) are left out.

A *day* is the UTC date of a trigger's timestamp. From the first day to the last there are **119** calendar days: **100** *active* days with at least one event and **19** empty ones. A rate counts events over elapsed time, so the empty days stay in the series.

```text
mean per calendar day = 594 / 119 = 4.99
mean per active day   = 594 / 100 = 5.94
```

**Computed** by [`analyze.py`](../../../../../scripts/streeling_fixtures/psychohistory/psy-008/analyze.py) into [`results.json`](../../../fixtures/psychohistory/psy-008/results.json):

| Events in the day | Days | Events |
|---|---|---|
| 0 | 19 | 0 |
| 1 to 2 | 76 | 89 |
| 3 to 11 | 13 | 72 |
| 12 or more | 11 | 433 |

The most common day has exactly 1 event: 63 days, 52.94%. Exactly 5 events occurred on 2 days, and 4, 5 or 6 events on 4 days, 3.36% of the days. "About five a day" describes almost no day.

### Practice Exercise 1

Compute both means. A colleague budgets the next 30 calendar days by multiplying the active-day mean by 30. What does that give, what does the calendar-day mean give, and what went wrong?

> **Answer:** `594 / 119 = 4.99` and `594 / 100 = 5.94`. At the calendar mean, `30 × 594 / 119 = 149.75` events; at the active-day mean, `30 × 5.94 = 178.2`, which is `119 / 100 = 1.19` times the calendar figure: the active-day mean drops the 19 empty days from the denominator, but the next 30 days will contain empty days too.

## 2. The Poisson benchmark and the index of dispersion

If events arrive independently of each other at a constant rate (a *Poisson process*), the count in a day follows a Poisson distribution, whose variance equals its mean. The *index of dispersion* D compares the two:

```text
Poisson probability  P(k events) = mean^k × exp(−mean) / k!
sample variance      s² = (Σx² − (Σx)² / n) / (n − 1)
index of dispersion  D  = s² / mean
```

This module uses the sample variance, with divisor n − 1, everywhere. D near 1 is what a constant rate gives; D below 1 means counts more regular than chance (a daily clock gives 0); D above 1 is *overdispersion*: quiet stretches and bursts. Under a Poisson process `(n − 1) × D` is approximately chi-square with n − 1 degrees of freedom, so D has a standard deviation of about `sqrt(2 / (n − 1))`, here 0.13 (Cox and Lewis 1966).

**Computed.** The daily counts give s² = 198.52 and D = 39.77, about 298 of those standard deviations above 1. The benchmark is the Poisson distribution with the observed mean, 594/119:

| Kind of day | Benchmark probability | Expected in 119 days | Observed |
|---|---|---|---|
| no event | 0.68% | 0.81 | 19 |
| exactly 1 event | 3.39% | 4.04 | 63 |
| 4, 5 or 6 events | 49.72% | 59.17 | 4 |
| 12 or more (benchmark's 99% quantile: 11) | 0.54% | 0.64 | 11 |

The 99% quantile is the smallest k with P(0) + … + P(k) ≥ 0.99. Call the 11 days above it *burst days*. The busiest, 2026-03-22, holds 109 events; the benchmark gives a day at least that busy a probability of 6.32 × 10⁻¹⁰³. Such a figure means that the benchmark is the wrong description, not that something nearly impossible happened.

**Synthetic controls.** The same code returns D = 0.0017 for 594 events spread evenly over 119 days and D = 1.23, within chance of 1, for a seeded log with each event on a uniformly drawn day. All three logs share the mean 4.99: the mean cannot tell them apart.

### Practice Exercise 2

With n = 119, Σx = 594 and Σx² = 26,390, compute s² and D, then say how many standard deviations D lies above 1.

> **Answer:** `(Σx)² / n = 352,836 / 119 = 2,965.01`, so `s² = (26,390 − 2,965.01) / 118 = 23,424.99 / 118 = 198.52` and `D = 198.517 / 4.9916 = 39.77`. With `sqrt(2 / 118) = 0.1302`, `(39.77 − 1) / 0.1302 = 297.8` standard deviations: a constant rate is not a candidate.

### Practice Exercise 3

Compute the benchmark's P(0) and P(1), the expected numbers of such days in 119, and compare with the log.

> **Answer:** `exp(−4.9916) = 0.006795` and `119 × 0.006795 = 0.81` empty days expected against 19 observed, 23.5 times more. `4.9916 × 0.006795 = 0.03392` and `119 × 0.03392 = 4.04` one-event days expected against 63 observed, 15.6 times more. The log has too many empty, one-event and burst days, and lacks the middle: the days that resemble the mean.

## 3. What the days are made of

**Computed from the event types.**

*A clock.* Of the 63 one-event days, 58 hold a single `discussion_created`, stamped between 13:51 and 16:09 UTC, 56 of them on weekdays. Of the 85 weekdays, 81 have at least one `discussion_created`. That is consistent with a scheduled job; one candidate, [`streeling-daily.yml`](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/.github/workflows/streeling-daily.yml), runs Monday to Friday at 13:17 UTC and posts discussions. A trigger does not record which discussion it saw, so the attribution is an inference.

*Weekends are empty or busy.* Of the 19 empty days, 15 are Saturdays or Sundays; so are the four busiest days, whose bursts are of more than one kind:

| Day | Events | `push` | `issue_opened` | `discussion_created` |
|---|---|---|---|---|
| 2026-03-22, Sunday | 109 | 32 | 38 | 39 |
| 2026-06-28, Sunday | 72 | 4 | 34 | 34 |
| 2026-03-21, Saturday | 60 | 41 | 6 | 13 |
| 2026-06-27, Saturday | 45 | 0 | 21 | 24 |

**Observed.** The project's record [`anti-pattern-003-push-triggered-spam`](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/state/patterns/anti-pattern-003-push-triggered-spam.pattern.json) describes workflows that "trigger on every push to master, causing duplicate runs when a session has many commits". It dates the pattern to 2026-03-21 and 03-22 (2 occurrences), detects it with "Workflow runs > 3 in a single day for the same workflow", and reports a fix to one workflow on 03-22.

**Computed.** The log is consistent with the record on those two days: 41 and 32 `push` events. But pushes are 77 of the 286 events of the four busiest days, 26.92%, below their share of the whole log (207 of 594, 34.85%).

Each archived file is one run of the producer, which is meant to run once per event. Applied literally to it, the record's threshold is passed on 21 days, 18 of them after 03-22. Note the rule's form: a threshold on a daily count, not an average.

### Practice Exercise 4

Classify three days: (a) 2026-03-21, 60 events of which 41 `push`; (b) 2026-06-27, 45 events, no `push`; (c) 2026-04-07, a Tuesday with one `discussion_created` at 13:54 UTC. Which does the push-triggered-spam record describe, and which would its rule flag?

> **Answer:** (a) Described and flagged: a push burst on a date the record names, and 60 > 3. (b) Flagged, since 45 > 3, but not described: no push at all, the burst is 21 issues and 24 discussions. (c) Neither: one run, at the hour of a weekday schedule. Three patterns sit behind one mean; a fix aimed at pushes would not have touched (b).

## 4. Longer windows do not rescue the mean

A natural repair is to plan per week and let the bursts average out. Cut the 119 days into 17 blocks of 7 days from the first day:

```text
176 38 8 13 7 5 14 6 15 6 6 6 8 63 204 11 8
```

**Computed.** The mean block holds 34.94 events, the median block 8 (the 50% quantile; by *nearest rank*, the level-p quantile is the k-th smallest of n values, k = p × n rounded up). D for blocks is 104.41, larger than for days; a Poisson process would give about 1 at every window length. An index that grows with the window means that busy days come in runs: the 11 burst days form two *episodes* (burst days at most 7 days apart count as one episode, an analysis choice), three days between 03-21 and 03-27 and eight between 06-21 and 07-02, 86 days apart.

The block total at least doubled on 4 of the 16 steps between neighbouring blocks, so a doubling rule of PSY-002's kind needs a baseline that knows about bursts. The mean itself is poorly known: its standard error, `sqrt(variance / n)`, would be 0.20 with the benchmark's variance (the mean), and is 1.29 with s² and 2.09 from the blocks, `sqrt(s²_blocks / 17) / 7`. Nor does the result hang on UTC midnight: with the day boundary moved by 6, 12 or 18 hours, D lies between 47.58 and 64.09 and the median stays at 1.

**What to plan with instead** (computed): empty days, 15.97%; days with at most 2 events, 79.83%; median 1, 90% quantile 8, 95% quantile 24, maximum 109; burst days, 11 of 119, in two episodes. PSY-009 sizes a plan on such a quantile.

**The strongest objection to this reading**: for a total over a long horizon the mean rate is the right quantity whatever the dispersion, since expected total = rate × time. That holds only if the coming months resemble these 17 weeks, and even then the rate is 4.99 with a standard error near 2.09, because 11 burst days carry 433 of the 594 events. **This sample cannot distinguish a process that bursts every few months from one that burst twice for unrelated reasons.** The next check would settle it.

### Practice Exercise 5

A teammate proposes "about 35 events a week, give or take 20%". How many of the 17 blocks fall inside that band? State a criterion for accepting a mean as a planning description, and apply it.

> **Answer:** 20% around 34.94 is 27.95 to 41.93; one block of 17 (38 events) lies inside, and the median block holds 8. Criterion: accept the mean when the counts scatter around it as a constant rate would, with D within two standard deviations of 1 at the window you plan on. For 17 blocks `sqrt(2 / 16) = 0.35`, so D should lie between 0.29 and 1.71; it is 104.41. Reject the mean; plan with the empty share, the median and the burst episodes.

## Sources, limits, and next check

**Observed, pinned at Demerzel `4b03838800dcd4894f1e026461979bff1d985ca8`:** the 594 archived trigger files (Git tree `2da37c16496d39c0c9137897c8be2b0c6d6b7978`; manifest digest in `observed-input.json`), the pattern record and the two workflow files linked above.

**Fixture.** [`scenarios.json`](../../../fixtures/psychohistory/psy-008/scenarios.json) holds the analysis choices; the [README](../../../fixtures/psychohistory/psy-008/README.md) gives the commands, the self-checks and the controls.

**Method references.** Cox, D. R., and Lewis, P. A. W. (1966), *The Statistical Analysis of Series of Events*, Methuen (the index of dispersion and its test). Barabási, A.-L. (2005), "The origin of bursts and heavy tails in human dynamics", *Nature* 435, 207–211 (times between events, not analysed here).

**Limits and what was not done.** One repository and 119 days, the working life of one producer workflow; two episodes cannot say how often bursts occur. A timestamp is when the producer wrote the file. Twelve trigger files were deleted from the repository without being archived (seven dated 2026-03-20, five dated 2026-06-30, none on the four busiest days); PSY-009 counts them, and with them the mean would be 5.09 and D 39.40. Whether overlapping runs lost others was not checked. No count model was fitted (PSY-022), no concentration measure computed (PSY-009), no cause of a burst established. No human has reviewed the subject matter of this lesson and no learner has tried it.

**Next check.** Count pushes, issues and discussions per day from GitHub's own event history over a longer span, with the cause of each burst day. If bursts recur with a stable spacing and size, a weekday clock plus episodes becomes a usable plan; if not, the honest plan is a threshold alarm, not a forecast.
