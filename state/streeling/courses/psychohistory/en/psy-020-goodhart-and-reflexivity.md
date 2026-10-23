---
module_id: psy-020-goodhart-and-reflexivity
department: psychohistory
course: "When the Measure Becomes the Target: Citations as a Proxy"
level: intermediate
prerequisites: ["psy-001-intro-fractal-compounding", "psy-011-measurement-change-or-system-change"]
estimated_duration: "40 minutes"
produced_by: claude-psychohistory-path
research_cycle: psychohistory-2026-10-13-020
version: "0.1.0"
---

# When the Measure Becomes the Target: Citations as a Proxy

> **Department of Psychohistory** | Intermediate | 40 minutes | English draft; human subject and learner review pending

## Objectives and project question

You will read a counting rule and say what it cannot see, compute what one added file does to the counts, state when rewarding a proxy degrades it, and correct a forecast that moves its target. **Project question:** the quality trend counts citations with `git grep`; what happens to such a proxy once agents know it is watched?

A *proxy* is measured in place of a *target* that cannot be. [PSY-001](psy-001-intro-fractal-compounding.md) contrasts LOLLI, "artifact count without regard to quality", with ERGOL, "real productive capacity", and lists "Citations per artifact" as the ERGOL to optimise. [PSY-011](psy-011-measurement-change-or-system-change.md) asks whether the instrument changed; here it is fixed, and the question is what the measured can do to it. Nobody in the project has been observed inflating this count: the subject is a mechanism and when it bites.

## 1. What the count can see

**Observed.** A governance *artifact* (a policy, a constitution, a schema, a skill) has an evolution record listing its *citation paths*. The *producer*, [`scripts/evolution_metrics.py`](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/scripts/evolution_metrics.py), [defines](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/scripts/evolution_metrics.py#L12-L15) `citation_count` as the "tracked files that mention any of the artifact's citation paths (`git grep -lF`)", minus the artifact's own files and [four excluded locations](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/scripts/evolution_metrics.py#L43). [The search](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/scripts/evolution_metrics.py#L80-L82) matches a literal string; [the feeder](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/scripts/quality_trend.py#L76) copies the result into the daily quality trend. A "citation" is a file where a path appears as text.

[`extract.py`](../../../../../scripts/streeling_fixtures/psychohistory/psy-020/extract.py) applies the rule to the 2,062 files of commit `4b03838` and writes [`observed-input.json`](../../../fixtures/psychohistory/psy-020/observed-input.json): 18 records, 16 measurable artifacts (two [marked as living](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/scripts/evolution_metrics.py#L20-L23) outside the repository), 19 distinct citation paths. **Computed:** the recount equals the recorded count for 16 of 16 artifacts. In decreasing order the counts are 65, 47, 45, 44, 29, 29, 23, 17, 15, 14, 13, 6, 6, 5, 1, 0; they sum to 359, supplied by 200 files.

The rule is blind on two sides.

- **Mention without use.** Of the 200 counted files, 123 are Markdown and 9 are Python programs, though a file's type does not tell use from mention; 92 name two or more artifacts. Nine course files, three lessons in three languages, supply 12 of the 359 counts, 8 of them from translations.
- **Use without mention.** One artifact has a count of 0, which its [record](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/state/evolution/2026-04-30-the-sentinel.evolution.json) says "reads as 'nothing uses this spec'", adding: "That is true only inside Demerzel: the metric cannot see sibling repositories."

In the trend, 20 rows have a non-zero `delta_citations` (listed in [`results.json`](../../../fixtures/psychohistory/psy-020/results.json)): 16 first recorded counts and four rises of 2 on 2026-10-03, for `policies / alignment-policy.yaml`, `contracts / galactic-protocol.md` and the two artifacts sharing one policy path. A rise says that files moved, not which or why: no cause is attributed here.

### Practice Exercise 1

Synthetic (`toy_rule` in [`scenarios.json`](../../../fixtures/psychohistory/psy-020/scenarios.json)). An artifact's only citation path is `toy/rule.yaml`. (a) `docs/index.md` lists the path; (b) `scripts/check.py` loads the rule with `os.path.join("toy", "rule.yaml")`; (c) the rule file names its own path; (d) `state/evolution/toy.json` and (e) `notes/archived/2025.md` name it; (f) `data/labels.json` writes `toy / rule.yaml`; (g) a lesson and (h) its translation name it. What is the count, and is the file that uses the rule in it?

> **Answer:** The count is 3: files a, g and h. File c is the artifact's own; d and e are excluded; b and f lack the literal string. So b, the only file that uses the rule, is not counted, while one lesson counts twice.

## 2. One file, sixteen counts

**Synthetic what-if cases on observed counts.** None of these files exists; [`analyze.py`](../../../../../scripts/streeling_fixtures/psychohistory/psy-020/analyze.py) adds them to the pinned counts. An *order relation* says which of two artifacts has the larger count; 16 artifacts form 120 pairs.

| File added | Counts raised | Sum | Order relations changed |
|---|---|---|---|
| A catalogue of all 19 paths | 16, by 1 each | 359 to 375 (+4.46%) | 0 of 120 |
| One file naming one path | 1 (2 for the shared path) | 359 + 1 (or + 2) | at least 1 for 11 of the 19 paths |

The catalogue changes no order, since it adds the same number to every count; in an excluded folder or with spaced labels it raises nothing. It moves the level, and every share or threshold computed from it: the only count of 0 becomes 1. A targeted file hardly moves the sum and reorders neighbours: two single-path files lift any of five artifacts past its upper neighbour.

**A measurement outside this fixture.** The description of pull request [GuitarAlchemist/Demerzel#1217](https://github.com/GuitarAlchemist/Demerzel/pull/1217) records that, under the producer's rule, the data files of this path's first two modules, which merely listed artifact paths, would have raised eleven of the sixteen counts by 4 to 6 on the next nightly run at an earlier head `fb6c317`, and none at `b938cc3`, once names became labels. Not reproducible from the pin, it carries no conclusion here; it is why this lesson spaces its labels.

### Practice Exercise 2

From the sixteen counts: (a) add one catalogue; give the new sum and its relative change. (b) Instead, add one file naming only the path of the artifact at 44. Which order relations change?

> **Answer:** (a) `359 + 16 = 375`, `16 / 359 = 4.46%`; no order relation changes (0 of 120). (b) 44 becomes 45 and ties the artifact at 45: one relation goes from "behind" to "tied".

## 3. When the proxy pays

Goodhart (1975), on monetary targets, as quoted by Manheim and Garrabrant (2018): "any observed statistical regularity will tend to collapse once pressure is placed upon it for control purposes". Campbell (1979), on social indicators, quoted there too: "The more any quantitative social indicator is used for social decision-making, the more subject it will be to corruption pressures and the more apt it will be to distort and corrupt the social processes it is intended to monitor." The title follows Strathern (1997): "When a measure becomes a target, it ceases to be a good measure." Each names a condition, pressure or use for decisions, not a fate.

**Observed: is the count used for decisions?** On paper. The [anti-LOLLI policy](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/policies/anti-lolli-inflation-policy.yaml) computes [`ratio_n = LOLLI_n / max(ERGOL_n, 1)`](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/policies/anti-lolli-inflation-policy.yaml#L69), counts the ["citation_count delta"](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/policies/anti-lolli-inflation-policy.yaml#L305) as ERGOL, [freezes artifact creation](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/policies/anti-lolli-inflation-policy.yaml#L97) when the ratio stays above 3.0 for 3 consecutive cycles; its [history file](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/state/driver/lolli-ergol-history.json) holds one cycle, dated 2026-03-23. A [detection rule](https://github.com/GuitarAlchemist/Demerzel/blob/4b03838800dcd4894f1e026461979bff1d985ca8/logic/fractal-compounding.md#L56) also judges the counts: "If the top 20% of governance artifacts account for more than 60% of citations, a power law is present. This is healthy". `policies / compounding-metrics-policy.yaml` repeats it, takes its data from the records' `citation_count` (lines 117–122) and gives that share a "target" of "0.60–0.85" (lines 219–222). On the counts typed by hand before 2026-09-13, [PSY-007](psy-007-power-law-or-not.md) finds the opposite verdict, which changed when the instrument did. **This sample cannot say whether the count drives any decision today.**

**Synthetic: what pressure would do.** Each assumed agent spends one unit of effort on work (value `a`, which shows one for one in the proxy) or on inflation (`g` proxy points, no value).

```text
proxy  = value + inflation + error
reward = (1 - w) x value + w x proxy
```

Work pays `a` whatever `w` is and inflation pays `w x g`, so an agent inflates when `w x g > a`. `scenarios.json` assumes `a` and `g` from 1 to 10 and an error of -1, 0 or 1: 300 equally likely cases, enumerated exactly.

| Weight `w` of the proxy in the reward | 0 | 1/2 | 1 |
|---|---|---|---|
| Mean proxy | 5.50 | 6.60 | 7.15 |
| Mean real value | 5.50 | 5.10 | 3.85 |
| Correlation of proxy and value | 0.9619 | 0.4374 | 0.2785 |

From `w = 0` to `w = 1` the mean proxy rises by 30% while the mean value falls by 30%: the indicator improves as the thing it stood for shrinks. In the model, the proxy tells less about the value the more it is optimised. The effect needs all three: a reward on the proxy, a way to inflate it, and work that pays less than inflating.

### Practice Exercise 3

The detection rule on all 18 recorded counts (the sixteen above, plus 55 and 0 outside the repository; sum 414). 20% of 18 artifacts is 3.6; take the top 4. (a) Does the rule call the pinned counts healthy? (b) Synthetic: each added file names the citation paths of the three measurable artifacts among the top 4. How many files make the share pass 60%? (c) What does one catalogue of every path do instead? (d) What does (b) say about the verdict?

> **Answer:** (a) `65 + 55 + 47 + 45 = 212`, and `212 / 414 = 51.21%`: no (the top 3 hold 40.34%). (b) Each file adds 3 to both sides: `212 + 3n > 0.6 x (414 + 3n)` gives `1.2n > 36.4`, so `n = 31`, and `305 / 507 = 60.16%` (30 files give 59.92%). (c) It raises the sixteen measurable counts by 1: `215 / 430 = 50.00%`, further from "healthy". (d) Thirty-one files of mentions, with no change of use, would turn the verdict: it judges where paths are written. Nobody has been observed writing such files.

### Practice Exercise 4

Synthetic. An agent's work yields 3 points of value; inflation would yield 8 proxy points. (a) For `w` = 0, 1/2 and 1, does it work or inflate, and what are its value and proxy (error 0)? (b) Above which weight does it switch?

> **Answer:** (a) It inflates when `w x 8 > 3`. At 0 it works: value 3, proxy 3. At 1/2, `4 > 3`: it inflates, value 0, proxy 8; at 1, `8 > 3`, the same. (b) `w x 8 > 3` holds for `w > 3 / 8 = 0.375`. The agent is assumed, not observed.

## 4. Forecasts that move their target

A forecast is *reflexive* when publishing it changes the outcome it predicts. One channel here is mechanical: a forecast of an artifact's count, committed in a file naming the artifact's path, is a counted file.

```text
outcome = baseline + self_mentions + reaction x (forecast - baseline)
```

**Synthetic, from one observed count.** `policies / alignment-policy.yaml` has a count of 44. Forecast 44 outside the repository, with no reaction, and it comes true; commit it in a file naming the path and it fails by construction: the outcome is 45. If readers also add half a mention per point forecast above the baseline (reaction 1/2), the forecast that comes true is 46, and republishing the last outcome misses by 1, 0.5, 0.25, 0.125. Grunberg and Modigliani (1954) gave conditions under which a public forecast can still be correct.

### Practice Exercise 5

Synthetic. Your forecast of the count now at 44 will be committed in a file naming the artifact's path. (a) With no reaction, what becomes of a forecast of 44? (b) With a reaction of 1/2, which forecast equals its outcome? (c) How would you publish to remove the effect, and by what criterion?

> **Answer:** (a) The outcome is `44 + 1 = 45`: an error of 1 made by the forecast itself. (b) `f = 44 + 1 + (f - 44) / 2` gives `f / 2 = 23`, so `f = 46`. (c) Write the artifact as a spaced label, or publish outside the tracked files: `self_mentions` becomes 0 and 44 is its own outcome. Criterion: a forecast must not be an input of what it forecasts.

**The strongest objection to this lesson's reading** is that it faults the count for something its producer never claimed: the docstring promises mentions, and a file that names a policy usually has a reason to. The fixture classifies no file as use or mention, so **this sample cannot distinguish an honest count from an inflated one**, and nothing in it shows that any count was inflated. To settle it, classify the 200 counted files by hand as use (the file loads, tests or enforces the artifact) or mention, and see whether the ranking survives.

**What would detect inflation.** Two signals are computable today: counts supplied per file (16 for a catalogue, at most 7 at the pin) and the share from files restating another, such as translations (8 of 359, 2.23%).

## Sources, limits, and next check

**Observed, pinned at Demerzel `4b03838800dcd4894f1e026461979bff1d985ca8`:** the files linked or named above and the quality trend. The fixture's [README](../../../fixtures/psychohistory/psy-020/README.md) gives the commands, self-checks and negative controls.

**Method references.** Goodhart, C. A. E. (1975), "Problems of Monetary Management: The U.K. Experience", *Papers in Monetary Economics*, vol. I, Reserve Bank of Australia; reprinted in Goodhart (1984), *Monetary Theory and Practice: The UK Experience*, Macmillan, 91–121. Campbell, D. T. (1979), "Assessing the Impact of Planned Social Change", *Evaluation and Program Planning* 2(1), 67–90. Strathern, M. (1997), "'Improving Ratings': Audit in the British University System", *European Review* 5(3), 305–321. Manheim, D., and Garrabrant, S. (2018), "Categorizing Variants of Goodhart's Law", [arXiv:1803.04585](https://arxiv.org/abs/1803.04585). Grunberg, E., and Modigliani, F. (1954), "The Predictability of Social Events", *Journal of Political Economy* 62(6), 465–478.

**Not done.** No agent's effort or motive was observed; both models are assumed. The 200 counted files were not classified. Goodhart's and Campbell's sentences were not checked against the 1975 and 1979 texts; Strathern's was read on page 308 of a scan hosted on gwern.net. No human has reviewed the subject matter of this lesson and no learner has tried it.

**Next check.** The hand classification above. If the ranking by use matches the ranking by count, the conclusion narrows from "the count cannot tell use from mention" to "today it does not need to"; it would still say nothing about a count that has become a reward.
