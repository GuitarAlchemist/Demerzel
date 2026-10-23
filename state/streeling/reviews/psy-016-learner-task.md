# PSY-016 learner task — no answer key

You have read **Probability Forecasts and the Brier Score**. Complete this transfer task without opening the course answer blocks. The release log below is hypothetical: it is not Streeling data and not a forecast.

A platform team logs 400 software releases. The event is "the release is rolled back within a day"; it happened for 12 of the 400. Four forecasters stated a probability of rollback before each release:

- **Never** always stated 0.
- **Cautious** always stated 0.1.
- **Coin** always stated 0.5.
- **Watcher** flagged 20 releases and stated 0.4 for each of them; 8 of those were rolled back. It stated 0.01 for the other 380, of which 4 were rolled back.

A fifth line, **Climate**, was added afterwards as a reference: 0.03 on every release, the share that turned out to be rolled back.

1. Compute the sum of squared errors and the Brier score of Never, Climate, Cautious and Coin.
2. For each of those four, what share of the squared error comes from the 12 rolled-back releases? Compute the Brier skill of Never and of Cautious against Climate. Which of the five lines could not have been stated in advance, and why does that matter for a skill score?
3. Compute Watcher's Brier score and its skill against Climate. Then compute the logarithmic score (natural logarithm) of Watcher and of Climate, and give Never's. Rank the five lines under each score and name the one whose rank differs most.
4. A team lead believes the next release has a 0.25 chance of being rolled back. Compute her expected Brier score and her expected absolute error `|p − o|` if she states 0.25, and if she states 0. Which rule is proper, and what does the other one reward?
5. Watcher's vendor claims that its flags "carry real information". Write a test plan that is fixed before any new release: the event and how it is resolved, the score, the reference forecast and where its probability comes from, how many releases or rollbacks you want before scoring, and one result that would falsify the claim. Say what your plan cannot establish.

Return your calculations, your plan and your uncertainty. Write "not assessed" where evidence is absent. The reviewer scores the unedited response separately; this task contains no answers.
