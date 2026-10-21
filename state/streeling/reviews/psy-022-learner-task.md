# PSY-022 learner task — no answer key

You have read **Competing Explanations: Comparing Models on Small Data**. Complete this transfer task without opening the course answer blocks. The help desk below is hypothetical: it is not Streeling data and not a forecast.

A small help desk counted the tickets opened on each of 14 consecutive days:

```text
day      1  2  3  4  5  6  7  8  9 10 11 12 13 14
tickets  0  0  1  0  6  8  5  0  1  0  0  1  6  0
```

Its manager wants to staff the desk from a model of the daily count and asks you to compare the same three candidates as the course: Poisson, geometric and negative binomial, each treating the days as independent draws. A colleague has already run the one-parameter search for the negative binomial: r = 0.393065, μ = 2, log L = −25.517.

1. Compute the maximum-likelihood λ of the Poisson and q of the geometric from their closed forms, then the two log-likelihoods. Show the sums you need.
2. Explain why the negative binomial's log-likelihood cannot be lower than the geometric one on any data, and what r below 1 says about the shape of the fitted distribution.
3. Compute AIC and BIC for the three models (ln 14 = 2.639057). Which model does each criterion rank first? Read each runner-up's difference on the scale the course cites for that criterion, and say what you would report to the manager.
4. Compute the lag-1 autocorrelation of the 14 counts. What do the three candidates assume about it, and what does your value change in the reading of question 3?
5. The manager proposes to write "tickets follow a negative binomial distribution" into the staffing plan. Write a check, fixed before new data arrive, that could falsify that sentence or replace it with a better one: what you would collect, which models you would compare and how, and one result that would make you drop the sentence. Say what your check cannot establish.

Return your calculations, your check and your uncertainty. Write "not assessed" where evidence is absent. The reviewer scores the unedited response separately; this task contains no answers.
