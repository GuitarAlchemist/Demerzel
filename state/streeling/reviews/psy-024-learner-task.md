# PSY-024 learner task — no answer key

You have read **The Single Actor: When One Sender Is the Whole Ensemble**. Complete this transfer task without opening the course answer blocks. The release tracker below is hypothetical: it is not Streeling data and it describes no real project.

A release tracker records one event each time an account publishes a release note, comments on a release or tags a build. Each event has one field about who acted, `actor`, which holds the name of the account the platform authenticated. The tracker kept 500 events from five accounts:

| Account | Events |
|---|---|
| P | 300 |
| Q | 100 |
| R | 50 |
| S | 30 |
| T | 20 |

The name of account Q ends in `[bot]`, and Q writes one event for each release note that the other accounts publish. A clean-up script deleted 40 further events before anyone read them; nothing says which accounts they came from.

1. Compute each account's share of the events, the concentration index H, the effective number of actors N and the half-coverage count. Show the sum of squared counts.
2. A colleague argues that Q is automation and must be set aside before counting actors. Recompute H and N without Q. Does setting Q aside bring the tracker closer to "many independent actors" or further from it? Say what the decision to set Q aside depends on, and when it has to be made.
3. Bound N for the 540 events that existed before the clean-up: compute it if all 40 deleted events came from P, and again if each came from a different account that is not in the table. Can any other assignment of the 40 events give an N outside that range? Give your reason.
4. Suppose that a quantity is averaged over the events, each account weighing in by its share, and that the five accounts behave independently with the same variability. Compute the relative spread of that average and compare it with the spread for five equal accounts. What would you check in the tracker before using either number?
5. A report built on this tracker states that "release activity follows a stable law across a broad community of contributors". Say what the tracker can and cannot support: what the `actor` field resolves, one result that would falsify "a broad community" if you could collect it, and the data you would ask for so that an effective number over people or agents could be computed.

Return your calculations, your reasoning and your uncertainty. Write "not assessed" where evidence is absent. The reviewer scores the unedited response separately; this task contains no answers.
