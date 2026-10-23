# PSY-010 learner task — no answer key

You have read **Exponential, Logistic or Steps? Fitting Growth to a Short History**. Complete this transfer task without opening the course answer blocks. The songbook below is hypothetical: it is not Streeling data and not a forecast.

A band keeps a shared songbook and wants 200 transcribed songs in it. The number of songs at the end of each week, from week 0 to week 9, was:

```text
week    0   1   2   3   4   5   6   7   8   9
songs   6   6   6  15  15  15  15  15  33  36
```

An *active week* is a week whose count differs from the week before; week 0 counts as active. The last burst is weeks 8 and 9. As in the course, a curve "reaches 200" in the first whole week in which its value is at least 199.5.

1. List the active weeks. What share of the 36 songs arrived in the last burst, and in what share of the ten weeks?
2. Fit a least-squares line `songs = a + b × week` to the ten points. Show the sums you used, give a and b, and compute the SSE. In which week does the line reach 200?
3. Least squares gives the exponential `5.110 × exp(0.2139 × week)` and, with the ceiling fixed at 200, the logistic `200 / (1 + exp(−0.2352 × (week − 15.66)))`. Compute the SSE of the exponential and the week in which each of the two curves reaches 200. By what factor do the SSEs of the line and the exponential differ, and how many weeks separate their answers? How long does the logistic take from its midpoint to 199.5, and why does it need that convention at all?
4. Remove the last burst: refit the line to weeks 0 to 7 only. In which week does it now reach 200, and what does it predict for week 9, where 36 songs were observed? How far did the answer to "when do we reach 200" move?
5. The band leader concludes: "The exponential fits best, so its week is our date." Say whether this history can support that conclusion, and write a check that is fixed before any new week is recorded: the curves and their parameters, the week you will look at, what each curve predicts for it, and one result that would show the conclusion to be wrong. Say what your check cannot establish.

Return your calculations, your check and your uncertainty. Write "not assessed" where evidence is absent. The reviewer scores the unedited response separately; this task contains no answers.
