---
module_id: psy-025-capstone-preregistered-forecast
department: psychohistory
course: "Capstone: A Preregistered Forecast You Can Score"
level: intermediate
prerequisites: ["psy-005-persistence-baseline", "psy-016-brier-score", "psy-017-calibration-with-six-observations"]
estimated_duration: "45 minutes"
produced_by: claude-psychohistory-path
research_cycle: psychohistory-2026-10-13-025
version: "0.1.0"
---

# Capstone: A Preregistered Forecast You Can Score

> **Department of Psychohistory** | Intermediate | 45 minutes | English draft; human subject and learner review pending

## Objectives and project question

You will write a forecast as a record that a stranger can resolve, test it against field rules, take its base rate from pinned data, and score it for every outcome before any exists. **Project question:** can we write a forecast about Streeling that a stranger can score later without asking us what we meant?

This capstone uses [PSY-005](psy-005-persistence-baseline.md) for the reference a forecast must beat, [PSY-016](psy-016-brier-score.md) for the Brier score and [PSY-017](psy-017-calibration-with-six-observations.md) for exact intervals on small counts.

## 1. A record, not a guess

*Preregistration*, for Nosek and colleagues (2018), is "committing to analytic steps without advance knowledge of the research outcomes", usually posted to an independent registry that "preserves the preregistration and makes it discoverable". It "does not favor prediction over postdiction; its purpose is to make clear which is which". A forecast record fixes, before the outcome, everything needed to score one forecast.

[`scenarios.json`](../../../fixtures/psychohistory/psy-025/scenarios.json) holds four records. [`analyze.py`](../../../../../scripts/streeling_fixtures/psychohistory/psy-025/analyze.py) checks each against 22 field rules, listed with their failure messages in the fixture's [README](../../../fixtures/psychohistory/psy-025/README.md). They answer a stranger's questions:

| A stranger asks | Fields (rules) |
|---|---|
| What exactly is forecast? | `question` (R02), `kind` (R03), `forecast` (R15) |
| Where and when do I look? | `resolution_source` (R04–R06), `resolution_time` (R07, R08) |
| What counts? | `resolution_rule`: what, how often, what not (R09); if the source moved (R10); when void (R11) |
| Compared with what? | `reference_class`, `base_rate` with a command and a commit (R12–R14), `reference_forecast` (R16) |
| What counts against it? | `adjustment` (R17), `falsifier` (R18, R19) |
| Who wrote it, who else decides, and when? | `author_can_influence_outcome` (R20) and its note, `written_at` and its evidence (R21, R22) |

**Synthetic.** The draft `library-growth-draft` reads "Streeling will keep growing fast next quarter", with source "the repo" and forecast "likely". **Computed:** the validator rejects it on 16 of the 22 rules (R02, R04–R07, R09–R16, R18, R20, R22) and cannot judge R08, R17 and R19, whose fields are unusable. One failure differs in kind: this batch adds to the library, so the draft's author could make it come true, and an outcome its author can steer is a plan to monitor, not a forecast to score. R20 judges only the record's author; the maintainers who would merge the records also merge every department's modules, which `author_influence_note` discloses. The repair, `library-growth-repaired`, asks about the library outside Psychohistory and passes, as do section 3's two worked records.

The validator checks form and agreement between fields, not clarity. Six changed copies of worked records each fail exactly the broken rule; a seventh, whose forecast equals its reference, passes ([`results.json`](../../../fixtures/psychohistory/psy-025/results.json), `validation.controls`).

### Practice Exercise 1

Two readers turn the draft's "likely" into 0.6 and 0.8. Give each reading's Brier score if the event happens and if it does not. What does that say about scoring a word?

> **Answer:** 0.6: `(0.6 − 1)² = 0.16` if it happens, `0.6² = 0.36` if not. 0.8: `0.04` and `0.64`. One outcome gets two scores depending on the reader, so the score would measure the reader, not the forecaster: R15 asks for a number.

## 2. A base rate from the pinned history

**Observed.** [`extract.py`](../../../../../scripts/streeling_fixtures/psychohistory/psy-025/extract.py) reads the 73 commits that touched [`state/streeling/courses`](https://github.com/GuitarAlchemist/Demerzel/tree/4b03838800dcd4894f1e026461979bff1d985ca8/state/streeling/courses) up to commit `4b03838`, and the folder's 255 files at that commit, each checked against its pinned blob ([`observed-input.json`](../../../fixtures/psychohistory/psy-025/observed-input.json)). An English *module* is a file `<department>/en/<name>.md` other than a README: 68 at the pin, in 18 departments. Music holds 19, Psychohistory 2.

The worked forecasts are about Music, which this batch does not touch: one about Psychohistory would measure the batch's own plan.

A *reference class* is the set of past cases a forecast is compared with; its *base rate* is the share of cases in which the event happened. Here a case is a department over a 92-day window, the forecasts' horizon, and the event is "its module count rose". Two back-to-back windows end at the pin and fit after the first module commit, on 2026-03-21. **Computed:**

| Reference class | Rises / cases | Base rate | Exact 95% interval (PSY-017) |
|---|---|---|---|
| Departments holding a module at the window's start | 2 / 36 | 0.055556 | 0.0068 to 0.1866 |
| Music alone | 1 / 2 | 0.5 | 0.0126 to 0.9874 |

The two rises are Mathematics (1 to 25 modules) and Music (6 to 19), both in the window ending at the pin.

[PSY-010](psy-010-growth-curves-short-series.md)'s warning applies: the count moves in bursts, so the base rate depends on where the windows fall. Moving both windows back one day at a time (`base_rate.alignment`) gives the broad class 0.055556 to 0.151515 (5 of 33, 21 days back), and Music 0 to 2 rises. Stating the alignment makes the number reproducible, not precise.

### Practice Exercise 2

The table does not show the broad class without Music. Compute its rate. Then say which value lies inside the other class's exact interval, and what follows for choosing a class.

> **Answer:** Without Music's 1 rise in 2 windows, `(2 − 1) / (36 − 2) = 1 / 34 = 0.029412`: one department nearly halves the rate. The broad rate 0.055556 lies inside Music's interval (0.0126 to 0.9874); 0.5 lies outside the broad one (0.0068 to 0.1866), but only because that class treats Music like the quiet departments. The data cannot choose the class: the record must name one and justify any departure from its rate.

## 3. The worked forecast and its resolution rule

**Synthetic: an exercise in writing a forecast, not a commitment of the department and not a prediction it endorses.** Two records share a source, a rule and a date:

- `music-rise-2027-01-13`: "Will the Streeling course library hold more than 19 distinct Music modules at 2027-01-13T23:59:59Z?" Reference forecast 0.055556, the broad base rate; forecast **0.7**.
- `music-count-2027-01-13`: the same count as **[19, 25]** with α = 0.2, against persistence's [19, 19] (PSY-005): in 34 of the 36 cases the count did not move. With 0.3 on 19 (the author's 0.1 quantile) and six chances in seven or more of 25 or fewer after a rise (so 25 is at or above the 0.9 quantile), the author's probability of coverage is at least `0.3 + 0.7 × 6/7 = 0.9`: an 80% interval by its stated level only.

The `adjustment` field says why 0.7 departs from 0.055556: Music rose in the last window, its newest module is dated on the pin's day, and the Music-only rate is too uncertain to set a number, so 0.7 is a judgment. A stranger may dispute that sentence; the rest is mechanical.

*Source:* `GuitarAlchemist/Demerzel`, read after the resolution time at the last first-parent commit of `master` (or the renamed default branch) whose committer date is at or before it; the record gives the commands. *What counts:* distinct Music module ids in `.md` files. A file's id is its front matter's `module_id`, else its file name less `.md` and any language suffix; its department, the front matter's, else its folder's (language folders skipped); READMEs, index pages and published copies excluded. *If moved:* if `master` names another place as the library's source or part of it (README, pointer file, commit message), apply the rule there too, whether or not this folder still exists; an id split between places counts once. *Void:* no library found; `4b03838` not an ancestor of the resolution commit; no timestamp by the resolution time; or a Music count other than 19 at any first-parent commit of `master` after `4b03838` whose committer date precedes that timestamp. Void is reported as void, never scored as 0.

**Computed:** front matter alone finds 67 modules, not 68: `cyb-003-measuring-variety-ratio-quantitatively.md` has none. With the file-name fallback the rule gives 68 and matches the path count in all 18 departments; the 181 translated files carry their English module's id and add nothing. Counting ids, not `en/` paths, lets the rule survive a layout without `en/` folders.

*Time of writing.* `written_at` (2026-10-14T13:39:06Z) is the author's word: the file is uncommitted. Its timestamp will be GitHub's `mergedAt` for the first pull request merging its final text into `master`, or a timestamping service's record of its hash, if earlier; not the request's opening time (it can precede the final text), push times (GitHub's events API keeps 30 days) or commit dates (set on the committer's machine). Until then the record has the form of a preregistration, not the registration.

### Practice Exercise 3

Apply the rule to this invented file list (path, front-matter `module_id`, `department`; `-` means absent) after a move. How many Music modules does it hold? And if on the scoring date the library is gone and nothing names a new home?

```text
music/index.md - -
music/mus-001-what-is-a-chord.md mus-001-what-is-a-chord music
music/mus-023-voice-leading.md - -
music/fr/mus-001-what-is-a-chord.fr.md mus-001-what-is-a-chord music
music/fr/mus-023-voice-leading.fr.md mus-023-voice-leading music
musicology/mcl-003-performance-practice.md mcl-003-performance-practice musicology
```

> **Answer:** 2. `index.md` is excluded; `mus-023-voice-leading` takes its id from its file name and its department from its folder; the French files repeat counted ids; `mcl-003` is Musicology's. With no library and no pointer the forecast is void: not 0, and not "no".

## 4. Score it before the outcome exists

A record is finished when its score is known for every outcome. **Computed, on INVENTED outcomes**, with PSY-016's skill `1 − BS / BS_ref` (BS_ref: the Brier score of the reference, exactly 0.055556 as stated, from unrounded scores):

| `music-rise` | Brier, forecast 0.7 | Brier, reference 0.055556 | Skill |
|---|---|---|---|
| Outcome 1 (more than 19) | 0.09 | 0.891974 | 0.8991 |
| Outcome 0 (19 or fewer) | 0.49 | 0.003086 | −157.75746 |

Outcome 0, the only one where 0.7 does worse than the base rate, is the falsifier.

The *interval score* of a central (1 − α) interval [l, u] at outcome x is its width `u − l`, plus `(2/α)(l − x)` if x < l, or plus `(2/α)(x − u)` if x > u; lower is better. This is Gneiting and Raftery's form (2007, eq. 43), which they trace to earlier work including Winkler (1972). A *miss* is an outcome outside the interval. Here α = 0.2, so each module outside costs 10, plus the width 6.

| Invented count | 18 | 19 | 21 | 25 | 28 |
|---|---|---|---|---|---|
| Covered by [19, 25] | no | yes | yes | yes | no |
| Interval score | 16 | 6 | 6 | 6 | 36 |
| Persistence [19, 19] | 10 | 0 | 20 | 60 | 90 |

The interval scores worse than persistence exactly at counts 0 to 19: the same falsifier. Coverage needs many intervals: ten such intervals, each covering with probability 0.9, cover seven or fewer times with probability 0.070191.

### Practice Exercise 4

Recompute the interval score of [19, 25] at α = 0.2, and persistence's, for the invented counts 28 and 18. Which are misses, and where does persistence win?

> **Answer:** 28: `6 + 10 × (28 − 25) = 36`; persistence `10 × 9 = 90`. 18: `6 + 10 × (19 − 18) = 16`; persistence `10 × 1 = 10`. Both are misses. At 18 persistence wins, 10 against 16: the interval also paid for its width.

**The strongest objection**: the record is scoreable but its forecast is weak. The base rate rests on two windows and moves from 0.055556 to 0.151515 with their alignment; its exact interval treats the 36 department-windows as independent, while both rises fall in one window and one burst, so it understates the uncertainty; the 0.7 is a judgment; and the Music count follows the maintainers' merge decisions, which a published forecast could itself influence. One score says almost nothing about skill: 0.8991 or −157.8 (rounded). A series of such records, each timestamped before its outcome and scored against its stated reference, would settle it.

### Practice Exercise 5

`library-growth-repaired` states 0.75 against its base rate, 1 rise in 2 windows. Compute both Brier scores and the skill for each outcome, and name the falsifying outcome. If the count passes 66 on 2027-01-13, has the forecaster shown skill?

> **Answer:** Outcome 1: `(0.75 − 1)² = 0.0625` against `(0.5 − 1)² = 0.25`, skill `1 − 0.0625 / 0.25 = 0.75`. Outcome 0: `0.75² = 0.5625` against `0.25`, skill `1 − 0.5625 / 0.25 = −1.25`. Falsifying outcome: 0. No: one favourable resolution cannot separate a good forecaster from a lucky one.

## Sources, limits, and next check

**Observed, pinned at Demerzel `4b03838800dcd4894f1e026461979bff1d985ca8`:** the commit history and the 255 files of the course library linked above.

**Fixture.** `python -I -B scripts/streeling_fixtures/psychohistory/psy-025/extract.py`, then `analyze.py` and `analyze.py --check`. The README lists the rules, the 22 self-checks and the negative controls.

**Method references.** Nosek, B. A., Ebersole, C. R., DeHaven, A. C., and Mellor, D. T. (2018), "The preregistration revolution", *PNAS* 115(11), 2600–2606, [doi:10.1073/pnas.1708274114](https://doi.org/10.1073/pnas.1708274114). Gneiting, T., and Raftery, A. E. (2007), "Strictly Proper Scoring Rules, Prediction, and Estimation", *Journal of the American Statistical Association* 102(477), 359–378, section 6.2. Winkler, R. L. (1972), "A Decision-Theoretic Approach to Interval Estimation", *Journal of the American Statistical Association* 67(337), 187–191. The exact intervals are Clopper and Pearson's (1934), as cited in PSY-017.

**Not done.** No record has resolved or been timestamped, and every scored outcome is invented. The counting rule was tested on the pinned library only, not on older file contents or published copies. No human has reviewed the subject matter of this lesson and no learner has tried it.

**Next check.** After 2027-01-13T23:59:59Z, resolve both worked records by their own rule or declare them void, and score them against their references. Sooner: a change in the Music count before their timestamp voids them, which would show how quickly a forecast about an active folder can be voided before anyone registers it.
