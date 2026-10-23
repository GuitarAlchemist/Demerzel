# PSY-006 learner task — no answer key

You have read **Estimate a Transition Matrix from Observed Counts**. Complete this transfer task without opening the course answer blocks. The status log below is hypothetical: it is not Streeling data and not a forecast.

A platform team gives each service of its fleet one status per week: green, amber or red. Pairing each service's status in one week with its status in the next week gives 463 pairs:

```text
from \ to   green  amber   red   pairs
green         412      6     0     418
amber           5     31     2      38
red             3      0     4       7
```

The team's forecasting tool ships with a stored transition matrix in which every entry is 1/3, annotated "uniform, no observations yet".

1. Estimate the transition matrix from the counts, as fractions and as decimals. Which transitions were never observed?
2. For each transition that was never observed, compute the exact one-sided 95% upper bound on its probability and the rule-of-three shortcut. By what share of the exact bound does the shortcut exceed it in each case? State the assumption on which both rest.
3. Apply add-one smoothing over the three statuses to rows green and red. Compare each smoothed probability of a never-observed transition with its bound from question 2. By how much does smoothing move the probability of staying green, and of staying red? Explain the difference between the two rows.
4. Read the stored matrix as a model. Starting from green, compute the probability of at least one red week within 1, 2 and 5 weeks, the expected number of weeks until the first red, and the long-run share of red weeks. Compute the probability of a red week within 1 and within 2 weeks under your estimate from question 1. How many pairs that start at green, none of them ending in red, reject the stored value for green→red at the 5% level, and does the log hold that many?
5. The team wants to announce: "a green service turns red the following week with probability below 0.5%". Write a plan that is fixed before any new data arrive: the unit of a trial; the number of pairs starting at green, none of them ending in red, that the claim needs in total and beyond the 418 on record (exact, and by the shortcut); the result that would falsify the claim; and what your plan cannot establish.

Return your calculations, your plan and your uncertainty. Write "not assessed" where evidence is absent. The reviewer scores the unedited response separately; this task contains no answers.
