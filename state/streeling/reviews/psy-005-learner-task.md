# PSY-005 learner task — no answer key

You have read **Persistence First: The Baseline a Governance Forecast Must Beat**. Complete this transfer task without opening the course answer blocks. The registry below is hypothetical: it is not Streeling data and not a forecast.

An operations team keeps a registry of 25 runbooks. Every week it writes one row per runbook with a status label: green, amber or red. Twenty runbooks have 26 weekly rows each, four have 21 rows each, and one has 23 rows. In one runbook's history, a single row in the middle (neither its first nor its last) has no label. Among the pairs of consecutive rows that both carry a label, 12 show a changed label.

Three models were evaluated on exactly those pairs. Each either repeats the previous label or announces a change; whenever a model announced a change that really happened, it also named the new label correctly.

- **Mirror** never announced a change.
- **Sentinel** announced 30 changes; 9 of them happened.
- **Scout** announced 10 changes; 6 of them happened.

1. How many forecasts does the registry contain? Show the accounting from rows to usable pairs, then give the persistence accuracy and the base rate of change.
2. For each model, count its errors and compute its accuracy.
3. Compute each model's skill score against persistence. Which model's accuracy carries no information beyond the baseline, and why?
4. For Sentinel and Scout, give the share of changes that was announced and the share of alarms that were false. A missed change costs the team ten times as much as a false alarm: which forecast, persistence included, is cheapest? Compare that ranking with the ranking by accuracy.
5. Scout's vendor claims that it "beats doing nothing". Write a test plan that is fixed before any new data arrive: the unit of a forecast, the baseline, the evaluation window, the score, and one result that would falsify the claim. Say what your plan cannot establish.

Return your calculations, your plan and your uncertainty. Write "not assessed" where evidence is absent. The reviewer scores the unedited response separately; this task contains no answers.
