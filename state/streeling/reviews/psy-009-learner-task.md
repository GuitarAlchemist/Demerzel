# PSY-009 learner task — no answer key

You have read **Concentration: When Four Days Hold Half the Events**. Complete this transfer task without opening the course answer blocks. The support desk below is hypothetical: it is not Streeling data and not a forecast.

A support desk counted the tickets opened on each of 14 consecutive days:

```text
day      1  2  3  4  5  6  7  8   9  10  11  12  13  14
tickets  2  1  0  3  2  1  1  2  36  22   9   3   1   1
```

The desk handles at most c tickets a day, oldest first, after the day's arrivals. Tickets that are not handled wait for the next day, and capacity that is not used on a day is lost. A ticket is *late* when it is not handled by the day after it arrives. A ticket still waiting at the end of day 14 is late if it arrived on day 13 or earlier; for a ticket that arrived on day 14 you cannot tell.

1. Rank the days. What share of all tickets falls on the busiest day, on the two busiest and on the three busiest? How many days are needed to reach half of the tickets?
2. Compute the Gini coefficient of the 14 daily counts with the lesson's formula, and the share of the tickets that the quietest half of the days holds. Compute the coefficient again over the 13 days that had at least one ticket, and say why the two values differ.
3. Compute the mean and the median number of tickets per day, then the mean without the busiest day. Which number describes a usual day, and what is the other one good for?
4. Size the desk in two ways: c equal to the mean rounded up, and c equal to the 90th percentile of the daily counts (the value at position `ceil(0.9 × 14)` of the sorted counts). For each, give the tickets handled on the day they arrive, the longest wait of a handled ticket, the tickets still waiting at the end of day 14, and the late tickets. Then find the smallest c that leaves no late ticket.
5. The desk manager says: "We average six tickets a day, so six a day is enough." Write the check you would run on the next 14 days, fixed before they arrive: what you will count, the threshold, and one result that would show the manager right. Say what 14 more days cannot establish.

Return your calculations, your plan and your uncertainty. Write "not assessed" where evidence is absent. The reviewer scores the unedited response separately; this task contains no answers.
