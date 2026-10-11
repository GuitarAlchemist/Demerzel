---
module_id: cs-006-ixql-pipeline-composition
department: computer-science
course: Compose IXQL Stages With Explicit Evidence Boundaries
level: intermediate
prerequisites: ["cs-005-agent-handoff-evidence-contract"]
estimated_duration: "35 minutes"
produced_by: codex-project-pilot
research_cycle: computer-science-2026-10-11-006
version: "0.1.0"
---

# Compose IXQL Stages With Explicit Evidence Boundaries

> **Department of Computer Science** | Intermediate | 35 minutes | English draft; subject and learner review pending

## Objectives

You will read a checked-in IXQL pipeline as a sequence of stage contracts, name each stage's input, output, and possible external effect, and propose a falsifiable check at a branch boundary. The project question is practical: **how can GA, Demerzel, IX, and TARS agents discuss one research-to-course workflow without mistaking a declared stage for an executed result?**

## 1. Read the composition that exists

Demerzel's [IXQL grammar at `0220ca8`](https://github.com/GuitarAlchemist/Demerzel/blob/0220ca84a25f59973bd6b9236cc00b7f68631a50/grammars/sci-ml-pipelines.ebnf) describes pipeline stages and flow. In its MCP-orchestration section, `identifier <- mcp_step` binds a result, `→` chains steps, `parallel(...)` groups tool invocations, and `when` introduces a guard. Its I/O section names operations such as `ix.io.read`, `ix.io.write`, and `ix.io.append`. These are source-language constructs; they do not establish that any particular pipeline executed.

The pinned [research-to-course example](https://github.com/GuitarAlchemist/Demerzel/blob/0220ca84a25f59973bd6b9236cc00b7f68631a50/examples/ixql/research-to-course.ixql) begins with department and weight reads, selects a department, loads context, samples a question, investigates, assesses a conclusion, and conditionally writes a course. It later writes a research-cycle log and describes compounding. Read the arrows as **intended dependency flow**: the next stage needs a result from the previous one. Read `ix.io.read(...)`, `write(...)`, and `ix.io.append(...)` as declared effects at boundaries. A grammar sample, model response, or file write could fail; the notation alone does not show the outcome.

For human discussion, annotate three real lines from the example:

```ixql
departments <- ix.io.read("state/streeling/departments/*.department.json")
question <- dept_context
  → tars.grammar.sample(grammar: dept_context.grammar, weights: dept_context.weights, pattern: "investigation")
  → tars.formulate_question(research_area: department.research_areas)
course <- when conclusion.conclude == "confirm":
  investigation → tars.produce_course(...) → tars.validate_schema(...) → write(...)
```

The shortened arguments above are an **explanatory excerpt**, not a runnable replacement for the checked-in file. The first line declares a file read. The middle chain declares a question derived from loaded context. The last branch declares course production only for a `confirm` conclusion, with a write after validation. The example itself says the course path and schema; follow its full lines for those exact values.

### Practice exercise 1

In the first line, what is bound to `departments`, and what evidence would prove the read succeeded in a real run? Does the line itself supply that evidence?

> **Answer:** It binds the declared result of reading department JSON files matching the path. A real run would need a trace or receipt showing the resolved paths, input revisions or hashes, success or failure, and returned shape. The line describes the read but supplies none of that runtime evidence.

## 2. Give every stage an input and an output

An agent handoff is clearer when it carries a small stage card. The table below is a **teaching annotation of the example**, not a new IXQL type system or syntax:

| Stage | Required input | Proposed output to inspect | Declared effect or uncertainty |
|---|---|---|---|
| Department selection | department and weight files | selected department plus scoring inputs | file reads; selection may fail if files are absent or malformed |
| Question formation | department grammar, weights, existing course list | question with its source context | context reads and TARS calls; duplication avoidance is declared, not proven |
| Investigation | question | source findings and cross-validation result | model/MCP calls; one unavailable source must be recorded |
| Conclusion | investigation evidence | `conclude`, belief, confidence | branch decision; thresholds in this example are proposals to inspect |
| Course production | confirming conclusion and investigation | validated draft course | conditional write to Streeling; no review or publication follows automatically |
| Cycle record | conclusion, reflection, course, grammar proposal | research-cycle JSON | file write; a path string is not a persisted receipt |

This annotation gives cooperating agents a shared vocabulary. The producer can say “I produced a question from these inputs” and point to its evidence. The receiver can check that the question, context, and revision match before launching the investigation. Explicit unknowns let the receiver stop at the failed seam instead of repeating every earlier stage. For any stage, record **source revision, input identity, output identity, status, effects attempted, and the next action**. This is a suggested communication envelope in ordinary prose or a receipt; the inspected grammar does not define these fields as an IXQL construct.

### Practice exercise 2

The checked-in example uses `dept_context <- parallel(...)` to read a department file, weights, grammar, and existing English courses. Can `question <- dept_context → tars.grammar.sample(...)` be treated as independently complete if the grammar read failed?

> **Answer:** No. The question stage names `dept_context.grammar` as an input. A failed grammar read leaves a required input unavailable. Report the failed read and leave the question unresolved, or rerun from a verified context. Do not infer a valid sample from the presence of the `question <-` line.

### Practice exercise 3

Classify these operations from the example as externally observable effects or proposed transformations: `ix.io.read`, `tars.grammar.sample`, `tars.cross_validate`, `write(course path, markdown)`, and `ix.io.append(grammar path, new_production)`. Which may change repository bytes?

> **Answer:** `ix.io.read` is an external read effect; `tars.grammar.sample` and `tars.cross_validate` are tool or model calls whose behavior and outputs require observations, so this lesson does not call them pure. `write` and `ix.io.append` are declared write effects that may change repository bytes. A successful sample or validation does not imply either write occurred.

## 3. Put a falsifier at the branch

The example says `course <- when conclusion.conclude == "confirm": ... → write(...)`. Here is a **fixed reasoning fixture**, not a report of an actual IXQL run:

```text
input: conclusion = { conclude: "refute", belief: "F", confidence: 0.81 }
pre-run course path: absent
expected stage result: no course draft produced; no course-path write
observable check for a test harness: compare file existence and write trace before/after
```

This fixture makes the branch claim falsifiable. If the harness records a course-path write for that input, the branch rule or implementation failed. If no file appears, that supports this one case only; it does not establish that confirmation, validation, translation, or review works. Preserve the input and effect trace so a second agent can reproduce the conclusion. The `confirm` threshold and generated course quality are separate questions.

### Practice exercise 4

For the fixed `refute` fixture, give the expected output and one observation that would falsify the branch rule. Would an empty course variable by itself prove that the write did not occur?

> **Answer:** Expected: no produced course and no course-path write. A trace showing `write(...)` was called, or a new file at that path attributable to the run, would falsify the rule. An empty variable alone is insufficient because an effect could have happened before a later failure; inspect the write trace and filesystem state.

## 4. Communicate what was checked

The repository's pinned [JavaScript validator](https://github.com/GuitarAlchemist/Demerzel/blob/0220ca84a25f59973bd6b9236cc00b7f68631a50/scripts/ixql-validate.js) calls itself a minimal structural validator, not a full parser. It tokenizes the `pipelines/` files, collects bindings and gate names, and reports issues. A clean validator report can support a narrow source-shape claim. It cannot prove that a TARS call resolved, that a course was written, or that the course passed learner review. The [IXQL UI composition specification](https://github.com/GuitarAlchemist/Demerzel/blob/0220ca84a25f59973bd6b9236cc00b7f68631a50/docs/ixql-ui-composition-spec.md) is marked brainstormed and ready for implementation; this lesson makes no editor or UI execution claim.

When handing the pipeline to another agent, send a stage card with the pinned file and revision, exact stage, input artifact identities, observed result or explicit unknown, any write receipt, and a bounded next action. [CS-005](cs-005-agent-handoff-evidence-contract.md) develops the general handoff contract. Here the additional discipline is to keep dependencies and effects visible at each IXQL stage. A source example, parse result, runtime trace, reviewed lesson, and published page are different artifacts with different evidence requirements.

### Practice exercise 5

An agent reports “`research-to-course.ixql` passed `scripts/ixql-validate.js`, so the new Streeling lesson is published.” Correct the claim and name the next two checks.

> **Answer:** The supported claim is at most that the validator found no structural issue in the files it scanned. Its script scans `pipelines/`, while `research-to-course.ixql` lives in `examples/ixql/`, so this command does not even establish a check of that example unless another explicit invocation did. Next, verify the exact example with an appropriate parser or test and a pinned revision; then inspect a real execution receipt and the course-production review and publication records before claiming delivery. A source declaration cannot fill those records.

## Sources and limits

The grammar, example, validator, and UI specification are pinned to Demerzel commit `0220ca84a25f59973bd6b9236cc00b7f68631a50`. This lesson checks their source text and uses a synthetic branch fixture; it does not run IXQL, test an IX editor, observe the IX executor, or validate the example as executable. The example's five-language translation and automatic course-write path describe intended flow; they are not evidence that this CS-006 draft was translated, reviewed, or published. Subject accuracy, learner task success, and localization remain open.
