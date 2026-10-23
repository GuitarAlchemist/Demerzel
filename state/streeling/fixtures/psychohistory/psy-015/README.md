# PSY-015 fixture: one stochastic SIR run against the deterministic curve

The two programs, `extract.py` and `analyze.py`, live in `scripts/streeling_fixtures/psychohistory/psy-015/` because this repository keeps executable code under `scripts/`; the data files they read and write are in this folder.

Fixture for the lesson `state/streeling/courses/psychohistory/en/psy-015-belief-contagion-small-population.md`.
Python 3.9 or later, standard library only.

## Files

| File | Kind | What it is |
|---|---|---|
| `extract.py` | script | Reads 32 files one by one: the Psychohistory department record, the 21 belief files under `state/beliefs/` (8 current, 13 archived) and the YAML file next to them, the schemas and sample files of the two record types designed to hold an agent's beliefs (belief snapshot, knowledge state), the schema of the recommendation message that two belief files cite, the integrity fields every message must carry, the script that applies such a message, and one audit note. Tests every JSON file under `state/` (without `state/streeling/`) for the shape of either record type and for a key that would name a sender; checks every Git blob id; writes `observed-input.json`. |
| `observed-input.json` | observed | Snapshot at Demerzel commit `4b03838800dcd4894f1e026461979bff1d985ca8`: the department's research area on beliefs and its key principle, one row per belief file (proposition, truth value, confidence, evaluator, evidence sources, contract messages named), the counts of the YAML file, the path a recommendation takes into a belief file, the two record types with their sample files, and the results of the shape test and of the sender-key scan on 722 JSON files. |
| `scenarios.json` | assumed | The SIR model and its vocabulary, the two population sizes (14 and 1,400), the three reproduction numbers (4/5, 6/5, 3), the number of runs and the six seeds, the analysis choices (cut, band, bins, hump rule, agreement test), the hand-computed case, the six things a transmission record needs, the holder and scaffold rules, and the inputs of the learner transfer task. Nothing in it is measured in the repository. |
| `analyze.py` | script | Reads only `observed-input.json` and `scenarios.json`. Computes the deterministic curve and its final size, the exact final-size distribution of the stochastic model, 10,000 seeded runs per case, the comparison between them, and the transfer-task answers; recounts the observed part; runs the self-checks; writes `results.json`. |
| `results.json` | computed | Every number used by the lesson, the review brief and the transfer task. |

In the two JSON outputs the path of a governed file and the belief propositions are written with a space on each
side of every slash (`scripts / apply_ml_feedback.py`), because the repository counts as a citation every tracked
file that holds the path of a governed file as a literal string, and a data file must not move that count.

## Regenerate

From the repository root:

```text
python -I -B scripts/streeling_fixtures/psychohistory/psy-015/extract.py
python -I -B scripts/streeling_fixtures/psychohistory/psy-015/analyze.py
python -I -B scripts/streeling_fixtures/psychohistory/psy-015/analyze.py --check
```

`extract.py` takes under a second and `analyze.py` a few seconds. Both write the same bytes on every run (LF line
endings, `indent=2`, insertion-ordered keys). `--check` recomputes the results and compares them with the saved file,
ignoring only CRLF against LF, because a Windows checkout with `core.autocrlf=true` stores CRLF in the working tree.

`extract.py` stops with exit code 1 when a source file is missing or has an unexpected shape, when one of the 32
files it reads one by one is not the blob of the pinned commit, or when one of the two folders it lists differs from
the pin: the 722 JSON files under `state/` (without `state/streeling/`) and the 11 schemas of `schemas/contracts/`.
Each folder has one manifest digest, the SHA-256 of the lines `<blob id> <path>`, which can be reproduced without the
script:

```text
git ls-tree -r 4b03838800dcd4894f1e026461979bff1d985ca8 -- state | awk '{print $3" "$4}' | grep '\.json$' | grep -v ' state/streeling/' | sha256sum
git ls-tree -r 4b03838800dcd4894f1e026461979bff1d985ca8 -- schemas/contracts | awk '{print $3" "$4}' | sha256sum
```

They must print `15a968afe2bc206e4d1af7e5b167d13413215be090da9980a607d3fca820ac04` and
`022a88b77e7193451759883c3c17eb092bc32893372a6a74b3f0ab67757953f6`. `--allow-drift` snapshots other data anyway and
records `"commit": null`; `analyze.py` then refuses the snapshot.

## Observed, synthetic, analogy

- **Observed:** `observed` in `results.json` (the department record's wording, the belief files, their evaluators and
  their sources, the two record types, the counts of the two scans). `analyze.py` only recounts it.
- **Synthetic:** `cases`, `summary`, `branching_process`, `several_initial_holders` and `transfer_task`. The
  population sizes, the reproduction numbers and the single initial holder are assumptions.
- **Analogy:** the whole model. "Susceptible", "infected" and "recovered" are epidemiological terms applied to a
  belief; no file read here records a holder passing a belief on to another agent.

## What the snapshot holds about the source of a belief

- **Two belief files name a message as their source.** `confidence-calibration` and `remediation-effectiveness`, two
  of the 8 current files, each have one evidence item whose source is `ml-feedback-recommendation <message id>`, and
  repeat that id under `source_recommendation`. The applying script (`FEEDBACK_SCRIPT` in `extract.py`) writes exactly
  these two files: it copies the message's rationale into the evidence claim and the message's confidence into the
  belief, and writes the evaluator `demerzel` itself. `extract.py` stops unless each of those four statements occurs
  once per belief file written, and `analyze.py` checks that the files citing a recommendation are those the script
  writes.
- **The sender is described, not read.** The message's schema says "A recommendation from an ix ML pipeline to
  Demerzel for governance improvement" and the script's docstring names a producer in the ix repository. The two
  messages are not in this repository: the folder the docstring names holds no JSON file, and each message id occurs
  in one JSON file under `state/`, the belief file that cites it. The keys that would name the sender (`origin_repo`,
  `origin_agent`, required in every message) are therefore out of reach.
- **No other file names a sender.** Of the 722 JSON files, none holds a key `origin_repo`, `origin_agent`,
  `taught_by` or `learner`; the same scan finds such a key in two sample files.
- **One holder has beliefs.** The 12 belief files with content are all evaluated by Demerzel; the other 9 (7 from
  `visual-critic-loop`, 2 from `ga-build-system`) have no evidence item, truth value U and confidence 0. So "no
  proposition under two holders" (0 of 21) could not have come out otherwise.
- **A YAML file sits next to the belief files.** It has 19 entries and 49 evidence items from 39 distinct sources
  (10 of them name `GPT-4o`) and no evaluator. `extract.py` reads it as text and only counts.

These are two adoptions from a document, one hop each. Nothing read here holds a second hop, the order in which
agents came to hold a belief, or an agent that was exposed and did not adopt, so no rate can be estimated.

## The stochastic model and why no time is drawn

With `S` susceptible agents, `I` holders and `N` agents in all, a new adoption happens at rate `beta * S * I / N` and
a holder stops transmitting at rate `gamma * I`. The next event is therefore an adoption with probability
`R0 * S / (R0 * S + N)`, where `R0 = beta / gamma`, whatever `I` is. The final size (how many agents ever held the
belief) depends only on that sequence of events, so each run follows this *embedded jump chain* and never draws a
waiting time. With `R0 = a/b`, a step draws one integer below `a*S + b*N` with `random.Random(seed).randrange` and is
an adoption when the integer is below `a*S`: no floating-point number enters a run. The author obtained the same
bytes under Python 3.9, 3.12 and 3.14 on Windows and under Python 3.14 on Linux.

The same chain gives the exact distribution by summing probabilities level by level (`final_size_distribution`): with
`fractions.Fraction` for 14 agents, with floats for 1,400 (additions, multiplications and divisions only). The only
results that pass through the C library are the roots of the final-size equation and of the fixed-holding-time
contrast (`exp`); they are stored to 4 decimals (2 for agents) and the script aborts if one of them lies within 1e-6
of a rounding boundary.

The branching value `1/R0` belongs to this model, not to every model with the same mean: an exponential holding time
makes the number of agents one holder converts geometric. With a fixed holding time of the same mean that number
would be Poisson and the process would die out with the smallest root of `q = exp(R0 * (q - 1))`: 0.0595 instead of
0.3333 at R0 = 3, and 0.6863 instead of 0.8333 at R0 = 1.2. `results.json` stores both; no run uses a fixed holding
time.

## Self-checks

`analyze.py` aborts instead of writing a result when a check fails. `results.json` lists all 42 under `checks`, with
the number of times each was evaluated; the list below is a selection:

- probabilities that sum to 1 (exactly with fractions, within 1e-9 with floats), simulated counts that sum to the
  runs, zones and bins that sum to the runs;
- the closed form `b*N / (a*(N-1) + b*N)` for the probability that the first holder stops before anyone adopts;
- two known answers for the deterministic curve: the Runge-Kutta integration must end within 1e-6 of the root of the
  final-size equation `1 - z = s0 * exp(-R0 * z)`, and its peak must equal `i0 + s0 - (1 + ln(R0*s0)) / R0`;
- the simulated counts and mean against the exact distribution, within 4.5 standard errors in every case;
- the branching-process fixed point `q = 1 / (1 + R0 * (1 - q))` against `min(1, 1/R0)`, and a fixed holding time
  that never makes dying out more likely than an exponential one;
- the observed part recounted from the rows of the snapshot: belief files by group, distinct propositions, files
  with content plus scaffolds, files that name a contract message;
- a case worked by hand:

```text
three agents, R0 = 1, one initial holder: P(adoption with S susceptible) = S / (S + 3)
S = 2: adoption 2/5, stop 3/5          S = 1: adoption 1/4, stop 3/4
final size 1: the first holder stops at once                      3/5
final size 2: one adoption, then two stops with S = 1             2/5 * 3/4 * 3/4 = 9/40
final size 3: one adoption, then a second one with 2 or 1 holders 2/5 * (1/4 + 3/4 * 1/4) = 7/40
```

Four results could pass on nothing, so each has a control recorded in `results.json`:

- "no proposition is recorded for two holders" (0): a planted second holder of one proposition is counted (0 to 1).
  The control shows that the counter works, not that the zero is informative: with one holder that has beliefs it
  could not have been anything else;
- "no JSON file under `state/` has the shape of a belief snapshot or of a knowledge state" (0 of 722): the same test
  recognises the three sample files, each as its own record type only (`extract.py` stops otherwise);
- "no JSON file under `state/` has a key naming a teacher, a learner or a message's sender (`origin_repo`,
  `origin_agent`)" (0 of 722): the same scan
  finds such a key in a sample file;
- "the simulation agrees with the exact distribution": counts simulated at R0 = 3 are rejected against the exact
  R0 = 1.2 distribution (333.29 standard errors against a limit of 4.5).

## Limits

- Nothing here measures how beliefs move between the project's agents. The reproduction numbers are assumed.
- The model mixes agents uniformly, gives every holder the same exponential holding time and lets nobody adopt twice.
- The two recommendation messages could not be read. That they came from another repository's pipeline rests on the
  schema's description and the script's docstring; and a pipeline that analyses Demerzel's own records is not a
  persona.
- The two scans read JSON files under `state/` only: apart from the one YAML belief file, YAML, Markdown and other
  folders are not searched, and a transmission recorded with another shape or other keys would not be found.
- The holder of a belief file is read from `evaluated_by` up to the first `/`, and an empty scaffold is a belief file
  with no evidence item, truth value U and confidence 0; both rules are interpretations.
- "Early fade-out" needs a cut. It is one tenth of the population (1 agent of 14, 140 of 1,400); two other cuts are
  reported, and at 14 agents the answer depends on the cut.
- The 10,000 runs per case carry sampling error (about half a percentage point on a share near 30%); the exact
  probabilities stored next to them do not.
