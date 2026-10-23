# PSY-014 learner task — no answer key

You have read **Prediction Horizons: How Fast Small Errors Grow**. Complete this transfer task without opening the course answer blocks. The simulator below is hypothetical: it is not Streeling data and not a forecast.

A delivery team owns a deterministic simulator of its backlog. The state is the backlog as a share of capacity, a number between 0 and 1, and one step is one week. To learn how the simulator treats small errors, the team runs it twice from two starts that differ by 1e-8, under two configurations:

- **Calm:** after 40 weeks the two runs differ by 2.5e-11.
- **Busy:** after 50 weeks the two runs differ by 4e-4.

Today's backlog is known to within 1e-3. The team calls a forecast usable as long as it is within 0.05 of what the simulator would give from the exact start.

1. For each configuration, estimate the Lyapunov exponent per week from the two gaps, and say whether errors shrink or grow.
2. In the busy configuration, how many weeks does an error take to double, and how many weeks of horizon does one more decimal digit of precision buy?
3. In the busy configuration, compute the horizon for today's precision of 1e-3, then for a backlog measured to 1e-6. In the calm configuration, how large is an initial error of 1e-3 after 104 weeks, and what does that mean for the horizon?
4. The team wants a busy-configuration forecast that stays usable for two years (104 weeks). Which initial error would that need, how many decimal places is that, and how many more digits than today's measurement? Say whether you would ask for that precision or change the way the forecast is used, and why.
5. A manager concludes: "the simulator shows that our real backlog cannot be forecast more than about 18 weeks ahead." Write a plan that could support or falsify this claim about the real process: what to record, how to score it, and one result that would falsify the claim. Say what your plan cannot establish.

Return your calculations, your plan and your uncertainty. Write "not assessed" where evidence is absent. The reviewer scores the unedited response separately; this task contains no answers.
