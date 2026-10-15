# PSY-025 learner task — no answer key

You have read **Capstone: A Preregistered Forecast You Can Score**. Complete this transfer task without opening the course answer blocks. The registry below is hypothetical: it is not Streeling data, not observed, and not a forecast.

A team keeps a plugin registry in the repository `example-org/plugin-registry`, folder `plugins/`. A forecaster drafts this record, with the fields of the lesson's records (the commit id is invented):

```text
id                    plugins-rise-2027-q1
question              Will the plugin registry list more than 12 plugins at the end of the first quarter of 2027?
kind                  probability
resolution_source     repository example-org/plugin-registry; branch main; location plugins/;
                      commit_rule "the last commit of main at or before resolution_time"
resolution_time       end of Q1 2027
resolution_rule       counts "plugin manifests in plugins/"; unit "one per plugin name";
                      excluded "templates and examples";
                      if_moved "count in the folder that the registry's README names"; void_if (empty)
reference_class       registry-quarters of comparable registries: 40 quarters
base_rate             3 events in 40 trials; commit 0123456789abcdef0123456789abcdef01234567; command (empty)
forecast              p = 0.4
reference_forecast    p = 0.075
adjustment            the maintainers announced a plugin contest
falsifier             statement "no new plugin by the resolution time"; outcomes [[0, 0]]
author_can_influence_outcome   (not stated)
written_at            2026-12-20T10:00:00Z
written_at_evidence   pull request opened on the registry; the hosting service records the time
```

1. Check the record against the 22 field rules listed in the fixture README. Which rules does it fail, which can you not judge, and what would you write to repair each failure?
2. Compute the base rate and its exact 95% interval (Clopper–Pearson, as in PSY-017; a few lines of code are fine). Does the forecast 0.4 lie inside that interval, and what must the `adjustment` field therefore carry?
3. For each outcome (more than 12 plugins, or not), compute the Brier score of the forecast and of the reference, and the skill against the reference. Which outcome falsifies the departure from the base rate?
4. The forecaster adds a central 90% interval for the number of plugins, [12, 16], against the persistence interval [12, 12]. For the invented counts 10, 12, 15 and 19, compute both interval scores and say which counts are misses. How many of the four does the interval cover?
5. Give, as a range of counts, the outcomes at which the interval scores worse than persistence. Then write a `void_if` clause and an `if_moved` clause that a stranger could apply if the registry moved to another repository, and say what your repaired record still cannot establish about the forecaster.

Return your calculations, the repaired fields and your uncertainty. Write "not assessed" where evidence is absent. The reviewer scores the unedited response separately; this task contains no answers.
