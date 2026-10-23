# PSY-011 learner task — no answer key

You have read **Measurement Change or System Change? Rebaselines in the Quality Trend**. Complete this transfer task without opening the course answer blocks. The log below is hypothetical: it is not Streeling data and not a forecast.

A software team logs, once a week for 12 weeks, the number of open defect reports in each of five components. At first the numbers are tallied by hand. From week 7 on, four components are counted by a query on the issue tracker; `vendor-sdk` stays hand-tallied. The `plugins` component enters the log in week 4. Every row records the `source` of its count.

| Component | Counts, week by week | Source |
|---|---|---|
| `parser` | weeks 1 to 12: 4, 4, 4, 4, 4, 4, 19, 19, 19, 21, 21, 21 | `hand-tally` in weeks 1 to 6, `tracker-query-v1` from week 7 |
| `renderer` | weeks 1 to 12: 7, 7, 7, 7, 8, 8, 12, 12, 12, 12, 12, 12 | `hand-tally` in weeks 1 to 6, `tracker-query-v1` from week 7 |
| `storage` | weeks 1 to 12: 2, 2, 2, 2, 2, 2, 15, 15, 15, 15, 18, 18 | `hand-tally` in weeks 1 to 6, `tracker-query-v1` from week 7 |
| `plugins` | weeks 4 to 12: 3, 3, 3, 1, 1, 1, 1, 1, 1 | `hand-tally` in weeks 4 to 6, `tracker-query-v1` from week 7 |
| `vendor-sdk` | weeks 1 to 12: 9 every week | `hand-tally` every week |

The log writes two more fields with the rule of the lesson's feeder. `rebaseline` is true, and `delta` is 0, when the row's source differs from the source of the component's previous row. Otherwise `delta` is the count minus the previous count (0 when the component has no previous row).

1. Which rows does the log flag `rebaseline`? List every row with a non-zero `delta` and say, for each, whether it is a first count or a change between two rows of the same source.
2. For each component, give the count before and after the change of source and the step. Give the total over the five components in week 6 and in week 7, the step of the total, the ratio of the two totals, and the sum of `delta` in week 7.
3. Count the rows whose count differs from the component's previous row, and split them into "at the change of source" and "same source". The total grew between week 1 and week 12: split that growth into first counts of components added later, steps at the change of source, and same-source steps. What share of the growth was measured like for like?
4. Take the week-to-week step of the total, from week 2 on. A step is flagged when it differs from the mean of all earlier steps (at least 3 of them) by more than 2 population standard deviations of those steps. Is the step of week 7 flagged? The step of week 11? Then build the series of same-source steps only, with first counts and steps at the change of source set to 0: is its week-11 step flagged? Show the mean and the standard deviation each time.
5. A manager writes: "Defects more than doubled in week 7: that week's release broke quality." Say what you would check before accepting or rejecting the sentence, name one observation that would falsify the reading "only the instrument changed", and describe one change of instrument that this log's `rebaseline` flag could never show.

Return your calculations, your reasoning and your uncertainty. Write "not assessed" where evidence is absent. The reviewer scores the unedited response separately; this task contains no answers.
