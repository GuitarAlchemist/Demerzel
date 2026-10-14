# PSY-010 bounded review brief

Status: **open**. This is a human-review and learner-trial packet, not an approval receipt and not evidence that any forecast of the course library was made or tested.

## Frozen target and inputs

- English course: `state/streeling/courses/psychohistory/en/psy-010-growth-curves-short-series.md`, Git blob `7d9cc4086be3e9c8a6ef784f06cacabb8d796ba0` (the blob identifies the exact text; `git log --diff-filter=A --format=%H -- state/streeling/courses/psychohistory/en/psy-010-growth-curves-short-series.md` names the commit that added the file).
- Fixture data in `state/streeling/fixtures/psychohistory/psy-010/`, programs in `scripts/streeling_fixtures/psychohistory/psy-010/`:
  - `scripts/streeling_fixtures/psychohistory/psy-010/extract.py`: Git blob `a9f55969ff0d3d93cba9420d68cf4aba3594eb99`
  - `observed-input.json`: Git blob `45d62afd9077dd29359aac11269d86d5b24c0f27`
  - `scenarios.json`: Git blob `eaf58e0eedf64738deb1b92a1091da2547260ff6`
  - `scripts/streeling_fixtures/psychohistory/psy-010/analyze.py`: Git blob `a431fc3c2590b53cf3240efd7417898071f9a99c`
  - `results.json`: Git blob `6de0879d8bd830c32e2bcc1873fa1da52720c963`
  - `README.md`: Git blob `d3b96887a7a390fbb58a91e98563d05d10c032d5`
- Observed source: the Git history of `state/streeling/courses` among the ancestors of Demerzel commit `4b03838800dcd4894f1e026461979bff1d985ca8`, read as commits and trees only: 73 commits, whose ids hash to the SHA-256 recorded in `observed-input.json` under `source`, and the folder's tree id. `extract.py` checks all of them. The target of 525 is the curriculum plan's figure, from a draft specification that is not in the repository: it is an input, not an observation.
- Production record: `state/streeling/course-productions/cp-psychohistory-2026-10-13-010.json`; review and publication flags are false.

A later course edit changes its blob. Review that diff explicitly before extending a verdict to the new source.

## Subject and method review

1. Rerun the fixture from the repository root: `python -I scripts/streeling_fixtures/psychohistory/psy-010/extract.py`, then `analyze.py`, then `analyze.py --check`. `extract.py` needs the full commit history (a blobless clone is enough) and must refuse a shallow clone. Recount independently of the scripts: `git rev-list --count 4b03838800dcd4894f1e026461979bff1d985ca8 -- state/streeling/courses` gives 73, and `git ls-tree -r --name-only` of that folder at the same commit lists 255 paths, of which 68 are `*/en/*.md` files other than README.
2. Check what is counted. A module is a file name; 181 translations, 4 README files plus 2 inside `en/` folders, and the 10 path names of the first 6 commits are left out; 73 additions − 5 removals = 68. Challenge the dating: committer dates in UTC, with one commit whose author date is 1.3 days earlier, which alone moves the line's date by 81 days, and the clock: five other time zones give 10 to 13 active days, still in three bursts. Challenge the sampling: one point per day gives the 174-day pause most of the weight; the lesson reports the fit on the 12 active days only (2033-07-08, 2027-11-09, 2030-12-15) without defending either choice.
3. Recompute the line from the daily series with any tool: intercept 528815/21528 = 24.5641, slope 56723/739128 = 0.0767431, SSE 11,462.4, day 6,514.4 for 524.5. Refit the exponential (24.6004, 0.00257104, SSE 11,100.5) and the logistic with ceiling 525 (rate 0.00272281, midpoint day 1,106.31, SSE 11,130.8) with independent software. The author did so once with SciPy outside the fixture; that run is not part of the record.
4. Challenge the criterion behind "this sample cannot distinguish the three laws": an SSE ratio of 1.033, 3 sign changes of the residuals against 107 for the seeded control, and a two-level staircase at 1,564.1 (7.1 times lower). Is a comparison with a 3-parameter description fair without a penalty for parameters? The lesson leaves that to PSY-022; say whether its wording stays inside what was computed.
5. Recompute three rows of the ceiling profile (69: 11,469.8; 525: 11,130.8; 100,000: 11,100.7) and read the two planted controls (8,751.7 at the planted 525 against 29,596.0 at 550; a spread of 0.4% before the turn). Challenge "no ceiling can be estimated": twelve ceilings were tried, and the claim is about least squares on this series, not about the project.
6. Recompute the cut-off table (2026-04-05: 2028-08-16, 2026-08-02, 2027-04-16; 2026-09-26: 2088-12-21, 2037-10-26, 2062-12-02). The cut-offs come from the 7-day burst rule, under which there are 3 bursts; the number runs from 6 to 2 as the rule goes from 1 to 12 days. Challenge the sentence "a fit that had captured the law would give dates that stop moving as the history grows": can a history of 16 days show that?
7. Check the burst scenarios as arithmetic (21 × 95 = 1,995 days, 13 × 15 = 195, 58 × 175 = 10,150) and confirm that the lesson labels them synthetic. The third burst is still open at the pin, which itself adds a module: its 37 modules are a lower bound, so cases (a) and (b) are upper bounds; check that the lesson and its next check say so. Counting from the pinned date, and treating three bursts as a sample, are assumptions: say whether they are stated clearly enough.
8. Check the sources. The two articles and the book are cited without links; the author compared title, journal, volume and pages with their Crossref records. Locate the plan's figure of 525 (21 departments with 25 courses each) in the draft specification and confirm that the lesson presents it as an input; the repository records 23 departments at the pin, two of them without a course folder.
9. Weigh the objection the lesson raises against itself: that the series records production decisions, not a growth law. The 23 modules of 2 October arrived in 23 one-module commits, 14 of them within two minutes. Does the lesson's conclusion survive it, or should the headline be "the date of 525 is a planning quantity"?
10. Attempt the five exercises before reading their answer blocks. Record ambiguity, missing inputs or arithmetic errors with section references.

## Answer-free learner trial

Give [`psy-010-learner-task.md`](psy-010-learner-task.md) without this brief or the course answer blocks. Record prior experience with regression and curve fitting, elapsed time, the unedited response, confusion, and any lesson revision followed by retest.

Expected answers, copied from `results.json` under `transfer_task` (a hypothetical songbook, computed from `scenarios.json`):

- Question 1: active weeks 0, 3, 8 and 9 (4 of 10). The last burst added `36 − 15 = 21` songs, 58.3% of the 36, in 2 of the 10 weeks (20.0%).
- Question 2: sums n = 10, Σt = 45, Σy = 162, Σt² = 285, Σty = 981; slope 168/55 = 3.05455 and intercept 27/11 = 2.45455; SSE 12312/55 = 223.9. `(199.5 − 2.45455) / 3.05455 = 64.51`, so week 65.
- Question 3: exponential SSE 137.6; `ln(199.5 / 5.110) / 0.2139 = 17.13`, so week 18. Logistic: `ln(399) / 0.2352 = 25.46` weeks from its midpoint, `15.66 + 25.46 = 41.12`, so week 42 (its SSE, if computed, is 143.7). The SSEs differ by a factor of 1.627 and the answers of the line and the exponential by 47 weeks. A logistic curve approaches its ceiling of 200 and never equals it, so "reaches 200" has no answer without a convention such as 199.5.
- Question 4: sums n = 8, Σt = 28, Σy = 93, Σt² = 140, Σty = 393; slope 45/28 = 1.60714 and intercept 6; SSE 1215/28 = 43.4. `(199.5 − 6) / 1.60714 = 120.4`, so week 121. For week 9 it predicts 20.46 against 36 observed. The answer moved by 56 weeks, from 121 to 65 (a factor of 1.86), because of two weeks of data.
- Question 5 has no single answer. A sufficient response says that ten points with four active weeks cannot support the conclusion (the SSE gap is a factor of 1.627 on residuals that come in runs, and one burst moved the line's answer by 56 weeks); fixes the three curves with their parameters, a week and the predictions for it before any new data (for week 18: line 57.44, exponential 240.18, logistic 126.84); names a result that contradicts the leader, for example a count at week 18 nearer the line's value than the exponential's; and says that one more burst can imitate any of the curves, and that nothing here concerns Streeling.

Score five criteria 0–2: (1) the active weeks and the concentration of growth in the last burst; (2) the least-squares line with its sums, its SSE and its week under the 199.5 convention; (3) the SSE and the weeks of the exponential and the logistic, the ratio and the gap, and why a logistic needs a convention; (4) the refit without the last burst, its failed prediction for week 9 and the size of the move; (5) a judgment that the history cannot decide, with a check fixed in advance and a falsifier, and the hypothetical songbook kept apart from Streeling evidence. A proposed pilot pass is at least 8/10 without presenting any fitted date as a forecast; evaluate this threshold after an actual learner trial. No result exists yet.

## Verdict and publication boundary

No verdict exists. When one is given, record reviewer identifier or pseudonym, UTC date, course blob, kind (`subject` or `learner`), evidence, findings, and `approved`, `changes_requested`, or `not_assessed`. When this brief was written (2026-10-13), there was no translation of PSY-010 and no learner had attempted the task.

Keep the review and publish flags false until actual verdicts and learner evidence are recorded. After accepted source integration, the page still has to be generated, deployed and read back anonymously with its source SHA before anyone calls PSY-010 published.
