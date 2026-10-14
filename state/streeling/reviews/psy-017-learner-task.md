# PSY-017 learner task — no answer key

You have read **Calibration with Six Observations**. Complete this transfer task without opening the course answer blocks. The log below is hypothetical: it is not Streeling data and not a forecast.

An incident-review team writes a diagnosis for every outage and attaches a confidence to it. Over the last year, 10 diagnoses were written with a confidence of at least 0.9, and later reviews overturned 3 of them. The team calls itself calibrated if such diagnoses are overturned 10% of the time, and it reads "overturned" as "wrong". A colleague suspects that the true rate is 30%.

After each batch of 10 confident diagnoses the team also runs a correction rule: if the share overturned in the batch exceeds 0.10, the confidence that the team allows itself is lowered by 0.2 times that share, but never by more than 0.05 for one batch. Nothing raises it again, and the total has no limit.

1. Compute the probability of 3 or more overturned diagnoses among 10 for a true rate of 10%, then for 5%. A rate lies inside the exact two-sided 95% interval when the observed count falls in neither 2.5% tail under that rate: is 10% inside? Is 5%? If you write code, give the two bounds of the interval.
2. Compute the probability of exactly 3 overturned among 10 at a true rate of 30% and at 10%, then their ratio. What does the ratio say, and what does it not say?
3. The team wants a rule "call ourselves overconfident when c or more of 10 are overturned" that a calibrated team triggers at most 5% of the time. Find c. How often does that rule miss a team whose true rate is 30%? Does the observed count trigger it?
4. For the correction rule, give the nudge for each count from 0 to 10. For a calibrated team (10%), compute the probability of a nudge in one batch, the probability of at least one nudge in 4 batches and in 13 batches, and the expected nudge per batch. What does the rule do over time to a team that is calibrated?
5. The colleague says: "3 of 10 shows that we are overconfident." Write a plan that is fixed before any new diagnosis is judged: what counts as a confident diagnosis and as overturned, when a diagnosis is judged, the counting rule with its two error rates, and one result that would falsify "the team is calibrated". Say what your plan cannot establish.

Return your calculations, your plan and your uncertainty. Write "not assessed" where evidence is absent. The reviewer scores the unedited response separately; this task contains no answers.
