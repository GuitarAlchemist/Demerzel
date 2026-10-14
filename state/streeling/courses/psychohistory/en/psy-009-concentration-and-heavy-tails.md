---
module_id: psy-009-concentration-and-heavy-tails
department: psychohistory
course: "Concentration: When Four Days Hold Half the Events"
level: intermediate
prerequisites: ["psy-008-bursts-are-not-rates"]
estimated_duration: "40 minutes"
produced_by: claude-psychohistory-path
research_cycle: psychohistory-2026-10-13-009
version: "0.1.0"
---

# Concentration: When Four Days Hold Half the Events

> **Department of Psychohistory** | Intermediate | 40 minutes | English draft; human subject and learner review pending

## Objectives and project question

You will rank the days of an event log, measure how unequally they share the events (top-k shares, Lorenz curve, Gini coefficient), compare a mean with a median, and test a capacity plan sized on the mean against one sized on a quantile. **Project question:** how much of the trigger activity sits in the few busiest days, and what does that do to an average-based capacity plan?

[PSY-002](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/state/streeling/courses/psychohistory/en/psy-002-governance-phase-transitions.md) reads a doubled signal rate, a count divided by a time window, as a sign of a coming transition. A rate is a mean, and this module measures how much of a mean a few days can carry. [PSY-008](psy-008-bursts-are-not-rates.md) sets the same daily counts against a Poisson benchmark; [PSY-007](psy-007-power-law-or-not.md) and PSY-022 fit distributions.

## 1. Rank the days and add from the top

**Observed.** Until it was retired on 2026-07-18, a [workflow](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/.github/workflows/demerzel-driver-triggers.yml) wrote one *trigger file* per repository event. [`state/triggers/archived/`](https://github.com/GuitarAlchemist/Demerzel/tree/4b03838800dcd4894f1e026461979bff1d985ca8/state/triggers/archived) holds 594 of them, of three types: pushes, opened issues and created discussions. [`extract.py`](../../../../../scripts/streeling_fixtures/psychohistory/psy-009/extract.py) snapshots the folder into [`observed-input.json`](../../../fixtures/psychohistory/psy-009/observed-input.json). The day of an event is the UTC date of its timestamp. The log runs from 2026-03-20 to 2026-07-16: **119** calendar days, **100** with at least one event and **19** with none.

**Computed** by [`analyze.py`](../../../../../scripts/streeling_fixtures/psychohistory/psy-009/analyze.py) into [`results.json`](../../../fixtures/psychohistory/psy-009/results.json), percentages rounded to two decimals. Sort the days from busiest to quietest and add from the top: a *top-k share* is the part of all events that falls on the k busiest days.

The four busiest days hold 286 of the 594 events, 48.15%: nearly half, not the half of this module's title; passing half takes a fifth day. The four days are two pairs of neighbours, 21–22 March (169 events) and 27–28 June (117), 97 days apart (22 March to 27 June), each inside one of PSY-008's two *episodes* (burst days at most 7 days apart). The share depends on where a day starts: on the 24 clocks from UTC−11 to UTC+12 it lies between 48.15% (UTC, the lowest) and 55.05%, at or above half on 15 of them.

### Practice Exercise 1

The ten busiest days hold 109, 72, 60, 45, 26, 24, 20, 20, 20 and 19 events, out of 594. Compute the share of the busiest day, of the four busiest and of the ten busiest, and the number of days needed to pass half.

> **Answer:** `109 / 594 = 18.35%`. `109 + 72 + 60 + 45 = 286` and `286 / 594 = 48.15%`. The ten sum to 415: `415 / 594 = 69.87%`. Half of 594 is 297; four days give 286 and five give `286 + 26 = 312`, so five days (52.53%).

## 2. The Lorenz curve and the Gini coefficient

The *Lorenz curve* shows every k at once: sort the days from quietest to busiest and plot the cumulative share of days against the cumulative share of events. Equal days would give the diagonal. **Computed:** the quietest half of the days (60 of 119) holds 41 events, 6.90%; the quietest 90% (108 days) holds 27.10%.

The *Gini coefficient* G condenses the curve into one number, twice the area between the diagonal and the curve. With the n daily counts sorted in increasing order and T their total:

```text
G = sum over i of (2i - n - 1) * x_i / (n * T)        x_1 <= x_2 <= ... <= x_n
all days equal          -> G = 0
one day holds them all  -> G = (n - 1) / n            118/119 = 0.9916 for this log
```

The fixture asserts both limits. **Computed:** G = 0.7789 over the 119 calendar days and 0.7369 over the 100 active days alone: the empty days are not what makes it high.

Zero is the wrong yardstick for that figure: chance alone makes days unequal. **Synthetic.** [`scenarios.json`](../../../fixtures/psychohistory/psy-009/scenarios.json) defines 2,000 control logs of 594 events, each event placed on one of 119 days drawn uniformly at random.

| Measure | Observed log | 2,000 synthetic logs: median (lowest to highest) |
|---|---|---|
| Events on the four busiest days | 286 | 41 (34 to 52) |
| Days needed to pass half | 5 | 40 (36 to 44) |
| Gini coefficient | 0.7789 | 0.2468 (0.1958 to 0.2995) |

No synthetic log reaches the observed value on any row: chance placement gives a Gini coefficient near 0.25, not 0.

### Practice Exercise 2

A five-day log has daily counts 0, 1, 1, 2, 6. Compute its Gini coefficient, then again over its four active days only.

> **Answer:** n = 5 and T = 10; the weights `2i − n − 1` are −4, −2, 0, 2, 4, the sum is `0 − 2 + 0 + 4 + 24 = 26`, and `G = 26 / 50 = 0.52`. Over 1, 1, 2, 6 the weights are −3, −1, 1, 3: `−3 − 1 + 2 + 18 = 16` and `G = 16 / 40 = 0.40`. Dropping an empty day lowers G although no event moved: say which days were counted.

### Practice Exercise 3

Two imaginary logs each hold 594 events on 119 days. In log A the four busiest days hold 42 events and G = 0.25; in log B, 89 events and G = 0.45. Classify each against the synthetic logs and against the observed log.

> **Answer:** A lies inside the synthetic range on both measures (34 to 52 events; 0.1958 to 0.2995): it is consistent with chance placement. B lies above every synthetic log on both, yet far below the observed one: `89 / 286 = 31.12%` of its top-four events, and 0.45 against 0.7789. The range comes from a finite batch, not from a bound.

## 3. Mean, median, and a mean that does not settle

**Computed.** The mean is `594 / 119 = 4.99` events per calendar day. The median, the middle value of the sorted counts (the mean of the two middle values when their number is even), is 1: 63 days hold exactly one event, and 100 of the 119 days are at or below the mean, which does not describe a usual day.

In a concentrated log a few days carry the mean, and it moves with them. Without the busiest day it falls from 4.99 to 4.11 (−17.66%); without the four busiest, to 2.68 (−46.34%). The median stays at 1. In the synthetic logs the same removal moves the mean by 2.21% at most.

The same instability appears in time: read at the end of March (12 days), April, May and June, then on the last day, the mean so far was 17.67, 5.88, 3.97, 5.14 and 4.99; the median was 4.5, then 1 four times.

Informally, counts are *heavy-tailed* when values far above the usual one are common enough to carry a large part of the total; a sample mean then depends on whether the sample caught one. That description fits these counts. The formal definition concerns how slowly the tail decays, and 119 days cannot test it: two episodes can produce such figures without any heavy tail.

### Practice Exercise 4

Recompute the mean without the busiest day, then without the four busiest. Which number would you report for "a usual day", and what is the mean still good for?

> **Answer:** `(594 − 109) / 118 = 485 / 118 = 4.11` and `(594 − 286) / 115 = 308 / 115 = 2.68`. Report the median, 1, for a usual day; it moves in neither case. The mean remains the right number for totals: `4.99 × 119` gives back the 594 events, rounding aside.

## 4. Size a plan on the mean, then on a quantile

**Observed.** The triggers were written for an autonomous driver whose [skill file](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/.claude/skills/demerzel-drive/SKILL.md) says it "ran 3 manual cycles in March 2026 and was never scheduled". The same file sets two limits: at most 50 triggers in the queue, and triggers older than 72 hours discarded. The archived triggers were never consumed, so nothing below is a measurement.

**Synthetic.** Assume a consumer that handles at most c events a day, oldest first; the rest wait, and unused capacity is lost. An event is *late* when it is not handled within 3 days of its arrival day (the 72-hour limit at one-day resolution). The p-th *percentile* is the value at position `ceil(p × n / 100)` of the sorted counts (nearest rank, the rule of PSY-008's quantiles).

| Plan | c per day | Late events | Longest wait |
|---|---|---|---|
| Mean, rounded up | 5 | 489 | 33 days |
| 90th percentile | 8 | 393 | 20 days |
| 95th percentile | 24 | 49 | 6 days |
| Smallest sufficient c | 34 | 0 | 3 days |
| 99th percentile | 72 | 0 | 1 day |

The mean plan offers `5 × 119 = 595` slots for 594 events and looks sufficient. It handles 440 and leaves 154 waiting at the end, because capacity left idle in quiet weeks cannot be carried into a busy one; its backlog peaks at 205 events, more than four times the design's queue limit of 50.

Part of that failure belongs to a plan with no slack, not to concentration: in 1,919 of the 2,000 synthetic logs a capacity of 5 also leaves late events (81 in the median log). But there the smallest sufficient capacity is 5 to 7 a day, and the 95th percentile (8 to 11) never leaves a late event. Concentration changes the price of the remedy: 34 a day, 6.81 times the mean.

Every plan in the table is sized in hindsight, on the 119 days it is run on, and an upper percentile settles no better than the mean: read at the end of May the 95th was 8, not 24, and a capacity of 8 from 1 June leaves 199 late events on the 46 days left. With fewer than 100 days read, the 99th percentile is the busiest day so far.

### Practice Exercise 5

Your criterion is the design's: no late event. Which percentile plan in the table meets it? Compute the capacity that the smallest sufficient plan offers over the log, and the share that is used.

> **Answer:** In hindsight, only the 99th percentile; the 95th leaves 49 late events and a longest wait of 6 days. The smallest sufficient capacity is 34 a day: `34 × 119 = 4,046` slots, of which `594 / 4,046 = 14.68%` are used and `100 − 14.68 = 85.32%` stand idle. Decide by the tolerance and the cost of idle capacity, not by the mean. The rule is assumed and the sizes are read after the fact: an arrival pattern, not a consumer, and no recipe for the next 119 days.

**The strongest objection to this lesson's reading** is that a trigger file is not a unit of work. The same skill file merges triggers that share type, repo and ref, and all 594 share one repo and one ref: a driver waking once a day (an assumed cadence) would have received 132 merged triggers, at most 3 a day, with a Gini coefficient of 0.3287. On that reading the concentration describes how often the producer fired, not how much work arrived. Second, the top-four share rests on two episodes: **this sample cannot distinguish a process with an episode every few months from two unrelated incidents.** A record of the work done per trigger would settle the first point; a longer event stream, the second.

## Sources, limits, and next check

**Observed, pinned at Demerzel `4b03838800dcd4894f1e026461979bff1d985ca8`:** the 594 trigger files, the workflow and the skill file linked above. `extract.py` refuses to run when the folder or a design file differs from its pin.

**Fixture.** The [README](../../../fixtures/psychohistory/psy-009/README.md) gives the commands, the cases worked by hand, the 41 self-checks and the negative controls.

**Read outside the fixture.** `git log --diff-filter=D` at the pin lists 12 trigger files deleted without being archived: seven dated 2026-03-20, five of them removed from `processing/` by the commit of [driver cycle 002](https://github.com/GuitarAlchemist/Demerzel/commit/2b752a763e490aa090cf32ee992cb923a6d1bc24), and five dated 2026-06-30, dropped by commit [`a2c1ef0`](https://github.com/GuitarAlchemist/Demerzel/commit/a2c1ef01d2470ca737b89e005eddc8aa78fa7583). One of the twelve is a `self_initiated` trigger, not a repository event. None falls on one of the four busiest days, which with all twelve counted would hold `286 / (594 + 12) = 47.19%`.

**Method references.** Lorenz, M. O. (1905), "Methods of Measuring the Concentration of Wealth", *Publications of the American Statistical Association* 9(70), 209–219, doi:10.2307/2276207. Ceriani, L., and Verme, P. (2012), "The origins of the Gini index: extracts from Variabilità e Mutabilità (1912) by Corrado Gini", *The Journal of Economic Inequality* 10(3), 421–443, doi:10.1007/s10888-011-9188-x. Hyndman, R. J., and Fan, Y. (1996), "Sample Quantiles in Statistical Packages", *The American Statistician* 50(4), 361–365.

**Not done.** No distribution was fitted and no tail law tested. The capacity rule is assumed and uses arrival counts only: no handling time, priority or deduplication. The plans are sized in hindsight: four earlier readings do not test a sizing rule. No human has reviewed the subject matter of this lesson and no learner has tried it.

**Next check.** Apply the same measures to a project event stream that is still growing, such as commits per day. If its Gini coefficient is close to that of chance placement for its own total and days, the concentration found here belongs to the retired producer, not to the project.
