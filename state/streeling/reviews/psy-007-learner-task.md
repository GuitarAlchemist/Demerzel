# PSY-007 learner task — no answer key

You have read **Is It a Power Law? Eighteen Citation Counts**. Complete this transfer task without opening the course answer blocks. The registry below is hypothetical: it is not Streeling data and not a measurement of any project.

A plugin registry lists 14 plugins with their download counts for one month:

```text
120  44  31  18  12  9  7  5  5  3  2  1  0  0
```

Its maintainer writes: "downloads follow a power law, as everywhere".

Use the continuous closed forms, which can be computed by hand or with a few lines of code. For the n values at or above a cut `x_min`, write S for the sum of `ln(x / x_min)` and m for their mean:

```text
power law:    alpha = 1 + n / S         standard error = (alpha - 1) / sqrt(n)
              log-likelihood = n ln((alpha - 1) / x_min) - alpha S
exponential:  rate = 1 / (m - x_min)    log-likelihood = n ln(rate) - n
```

1. How many of the 14 values can enter a log-log rank plot or a power-law fit, and what do you do with the others? Name one thing that a straight line on that plot cannot establish.
2. Fit the power law at the cut `x_min = 1`, then at `x_min = 5`. For each cut, state the number of values kept and set aside, the exponent and its standard error.
3. At both cuts, compute the two log-likelihoods and their difference R (power law minus exponential). Which family has the higher likelihood, and is that enough to accept the maintainer's sentence? Give your reason.
4. Assume the exponent stays where you found it. At each cut, how many values at or above the cut would bring the standard error down to 0.1?
5. Write a test plan that is fixed before any new data arrive: the rule for the cut, the number of tail values you ask for, the alternatives you compare, and one result that would falsify "downloads follow a power law". Say what your plan cannot establish.

Return your calculations, your plan and your uncertainty. Write "not assessed" where evidence is absent. The reviewer scores the unedited response separately; this task contains no answers.
