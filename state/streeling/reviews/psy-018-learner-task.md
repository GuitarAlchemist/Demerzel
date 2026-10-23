# PSY-018 learner task — no answer key

You have read **Backtesting Without Leakage**. Complete this transfer task without opening the course answer blocks. The wiki below is hypothetical: it is not Streeling data and not a forecast.

A documentation team counts, once a week, the pages of its wiki that link to each of three documents. The counting procedure stayed the same during the eight weeks below.

| Document | Week 1 | Week 2 | Week 3 | Week 4 | Week 5 | Week 6 | Week 7 | Week 8 |
|---|---|---|---|---|---|---|---|---|
| handbook | 10 | 10 | 10 | 10 | 10 | 13 | 13 | 13 |
| glossary | 7 | 7 | 7 | 7 | 7 | 7 | 7 | 7 |
| style-guide | 4 | 4 | 4 | 4 | 4 | 7 | 7 | 7 |

The team's export also carries a column `change`: the week's count minus the previous week's count.

A forecast looks one week ahead and needs two earlier weeks of its series, so week 3 is the first target. The three methods are those of the lesson: persistence, mean so far, drift.

1. How many forecasts do the three series offer under a rolling origin? How many counts differ from the previous week's count, in how many distinct weeks, and how many series never vary?
2. For the handbook, give the absolute error of each method for each target week from 3 to 8. Then give each method's total absolute error, its MAE and its relative MAE against persistence.
3. Still for the handbook: what is the scale at the origin of the forecast of week 6, and at the origin of the forecast of week 7? Give each method's scaled error for week 7. For which of the three series is no scaled error defined at all, and why?
4. A colleague fits a level (the mean of the training weeks) to the handbook and reports its MAE on two test weeks. Compute that MAE (a) with weeks 7 and 8 as test weeks and the level from weeks 1 to 6; (b) with the same test weeks and the level from all eight weeks; (c) with weeks 3 and 7 as test weeks and the level from the other six. A second colleague forecasts "last week's count + this week's `change`" under the rolling origin: compare its MAE with that of persistence. For (b), for (c) and for the `change` forecast, name what entered the forecast although it was not yet recorded at the origin, and give the change of the reported error in percent: (b) and (c) against (a), the `change` forecast against persistence.
5. The team writes: "persistence beat drift on two series out of two". How many independent events support that sentence, and why? Then write a test plan, fixed before any new week arrives, for the claim "persistence is the best of the three methods on these counts": the unit of a forecast, what each forecast may use, the score, and one result that would falsify the claim. Say what your plan cannot establish.

Return your calculations, your plan and your uncertainty. Write "not assessed" where evidence is absent. The reviewer scores the unedited response separately; this task contains no answers.
