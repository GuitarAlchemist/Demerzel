# state/learning/

**Status: no files have ever been produced here.** This directory is declared by two
different specifications, neither of which has a working producer. Both are recorded
below so the next reader does not mistake either for something that runs.

## 1. Recursive-learning eval artifacts (declared by policy)

`policies/recursive-learning-eval-policy.yaml` §state declares this directory as the
home of:

| file | purpose |
|---|---|
| `meta-metrics.json` | the five meta-metrics (learning acceleration, teaching improvement, knowledge retention, transfer efficiency, meta false-positive rate) |
| `eval-input-{yyyy-mm}.json` | monthly self-evaluation input |
| `eval-grades-{yyyy-mm}.json` | graded results |
| `eval-diagnosis-{yyyy-mm}.json` | diagnosed anti-patterns |
| `eval-proposals-{yyyy-mm}.json` | improvement proposals (each requires `article_4_check`) |
| `eval-report-{yyyy-mm}.json` | monthly report |
| `meta-eval-{yyyy-q}.json` | quarterly depth-2 meta-evaluation |

**None of these exist and nothing computes them.** No script references
`meta-metrics`, and no workflow schedules the monthly `self_evaluation_cycle`. The
`article_4_check` boundary IS now enforceable — `schemas/recursive-learning-eval.schema.json`
constrains proposals and `scripts/test_recursive_learning_eval_schema.py` tests it — but
enforcement only bites once something emits a proposal. The policy says this plainly:
*"Until an executor exists the policy constrains nothing at runtime."*

Note that `tests/behavioral/recursive-learning-eval-cases.md` asserts results are
*"stored in state/learning/meta-metrics.json"*. Behavioral tests are prose counted by
`governance-manifest.json`, not executed, so that case passes by existing. Do not read
its presence as evidence the computation works.

## 2. Learning journal (declared by a skill that is not in tree)

The prior contents of this file described epistemic learning records named
`YYYY-MM-DD-<short-slug>.learning.json`, produced by a `demerzel:meta-brainstorm` skill
and grounded in the Epistemic Constitution's E-0..E-9 articles.

Two corrections to that description:

- The skill was cited as `.agent/skills/demerzel-meta-brainstorm/SKILL.md`. **No such
  file exists anywhere in this repository**, so the schema it pointed to is unavailable.
- The constitution was cited as `governance/demerzel/constitutions/epistemic.constitution.md`.
  That is a path from a different repository layout. The real location is
  [`constitutions/epistemic.constitution.md`](../../constitutions/epistemic.constitution.md),
  which does define E-0 through E-9.

## If you are about to build something here

Pick **one** of the two specifications and delete the other from its source, rather than
leaving a directory with two owners and no output. The smallest honest first step is a
single producer for `knowledge_retention` — it is the only metric whose inputs already
exist, since beliefs in `state/beliefs/` carry hexavalent truth values and timestamps.
Per the LOLLI rule, do not add more declared artifacts here until one is actually emitted.
