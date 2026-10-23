# PSY-008 learner task — no answer key

You have read **Bursts Are Not Rates: Event Arrivals in the Trigger Log**. Complete this transfer task without opening the course answer blocks. The log below is hypothetical: it is not Streeling data and not a forecast.

A small team runs a service that receives webhooks. Over four weeks, Monday to Sunday, it counted the webhooks received on each of the 28 days:

```text
week 1    1   1   2   1   1   0   0
week 2    1   2   1   3   1   0   0
week 3    2  16  24  17   1   0   1
week 4    1   2   2   3   1   0   0
```

The team lead sums this up as "about three webhooks a day".

1. Count the events, the days with at least one event and the empty days. Give the mean per calendar day and the mean per active day. On how many days does the count lie within one event of the lead's figure (2, 3 or 4)?
2. Compute the sample variance of the 28 daily counts (divisor n − 1) and their index of dispersion. Under a constant rate the index has a standard deviation of about `sqrt(2 / (n − 1))`: how many of those standard deviations above 1 is the index you found?
3. Use a Poisson distribution with the observed mean as the benchmark. How many empty days and how many one-event days does it expect in 28 days, and how many does the log hold? What is the benchmark's 99% quantile (the smallest count k for which the probability of at most k events reaches 0.99)? How many days of the log exceed it, and how many would the benchmark expect?
4. Compute the four weekly totals, their mean, their median (nearest rank: the second smallest of four), their sample variance and their index of dispersion. How many weeks lie within 20% of the weekly mean? Is the weekly index smaller or larger than the daily one, and what does that tell you about the busy days?
5. The lead replies that arrivals "will settle at three a day". Write a check that is fixed before the next four weeks of counts arrive: what you will count, the benchmark, and one result that would falsify the lead's claim. Then say what the four weeks above cannot tell you, and which figures you would report to the team in place of the mean.

Return your calculations, your plan and your uncertainty. Write "not assessed" where evidence is absent. The reviewer scores the unedited response separately; this task contains no answers.
