# PSY-015 learner task — no answer key

You have read **Belief Contagion in a Small Population**. Complete this transfer task without opening the course answer blocks. The team below is hypothetical: it is not Streeling data and not a forecast.

A support team has 4 people. One of them comes to believe that a product is about to be discontinued. Use the model and the vocabulary of the lesson: a person who holds the belief brings it up with colleagues picked at random at a rate of 0.5 conversations per day, and stops bringing it up at a rate of 0.25 per day (after 4 days on average). A colleague who hears it for the first time adopts it at once, and nobody adopts it twice.

1. Compute R0, and R0 × S/N at the start. Is the belief above the threshold when it starts? After how many adoptions does the deterministic number of holders stop increasing?
2. With the jump chain, compute the probability that the first event is an adoption, the probability that the belief is never passed on, and the probability that exactly 2 people ever hold it.
3. Work out the whole distribution of the final size (1, 2, 3 or 4 people) by following every sequence of events. Give its mean, its most likely and its least likely value, and say whether it has one hump or two.
4. Solve the final-size equation `1 - z = s0 * exp(-R0 * z)` for this team (a few lines of code, or repeated substitution starting from z = 0.5) and convert z into a number of people. What is the probability that a run ends at one of the two whole numbers around that value? Compare the probability that at most 2 people ever hold the belief with the branching-process value. Then suppose 3 people hold the belief at the start: compare the branching value with the exact probability that the fourth person never adopts it, and explain the gap.
5. The team lead reads the deterministic result as "nearly everyone will end up believing it". Write what you would record, for this belief and the next few, to test that reading; fix in advance one result that would count against the contagion model itself; and say what one team and one belief cannot establish.

Return your calculations, your plan and your uncertainty. Write "not assessed" where evidence is absent. The reviewer scores the unedited response separately; this task contains no answers.
