# Craft courses: bounded AI dry-run and migration rehearsal

Status: local evidence and a revised learner handout. Human subject, fluent-language and learner approval remain pending. No course-production gate changed.

## Inputs and exposure

The coordinator dispatched three fresh AI agents with no inherited conversation. Each was restricted to a scratch English lesson and its separate task sheet, plus one new transfer question. The source was Demerzel `edc8c86f9b4b380d9310d396ebffee8d39fd528c`; `manifest.json` binds the original lesson/task Git blobs and the redacted lesson hashes. All five explicit single-line `Answer` blocks were removed from each lesson. Explanations and worked examples in the lesson body remained available.

Each agent had general prior mathematical competence and read the lesson before answering. No pretest was administered. This is an answer-block-redacted, lesson-exposed AI calculation trial, not evidence of novice learning, retained learning or human transfer. Source links could be cited from the lesson but were not independently inspected by the agents. Their raw first responses are archived byte for byte, with response SHA-256 hashes in the manifest.

| Course | Actual agent-recorded UTC interval on 2026-10-21 | Raw response |
|---|---|---|
| PHY-005 | 23:53:02–23:54:21 | [Unedited response](phy-005-response.md) |
| SEM-004 | 23:53:10–23:54:22.349 | [Unedited response](sem-004-response.md) |
| CS-009 | 23:53:25.235–23:54:39.507 | [Unedited response](cs-009-response.md) |

These intervals describe AI execution, not the courses' advertised human study durations. No feedback or retest occurred before the responses were preserved.

## Coordinator assessment

The coordinator independently checked the submitted arithmetic and reasoning against the handouts. This assessment is from the same serving-model family; it is not an external subject verdict. SEM-004 and CS-009 use their existing provisional five-dimension, 0–2 rubrics. PHY-005 has no calibrated numeric rubric, so its result is reported by task.

### PHY-005

All five handout tasks were mathematically correct within the stated assumptions:

1. The ruler is 100 mm/coordinate unit; full thickness is 0.006 coordinate unit. Local-ply and rigid heights are respectively 16.8 mm/0.168 scene unit and 21.6 mm/0.216 scene unit. Both conversion paths agree.
2. Passing coordinate thickness 0.6 describes 60 mm stock, a factor-100 error; the repair is 0.006.
3. Level-35 lower surface is 21 mm/0.21 scene unit, distinct from the complete 21.6 mm/0.216 extent.
4. Doubling sheet width with fixed stock halves coordinate heights and preserves physical heights. Doubling width and stock preserves coordinate heights and doubles physical heights.
5. The handoff preserves the source-inspection limit, proposed scene scale, absent-result semantics and lack of physical/export evidence.

The additional 300 mm/3-coordinate-unit, 0.45 mm, 12-level case gave `t=0.0045`, extent 5.4 mm/0.54 scene unit, and level-11 offset 4.95 mm/0.495 scene unit at 100 scene units/metre. Those values are correct. Internal normalization versus the external physical ruler remains an integration question, not a defect established by this trial.

### SEM-004

Provisional task scores: map/inverse arithmetic 2; selection provenance 2; mapped property comparison 2; order/sign distinctions 2; falsifiable transfer and uncertainty 2. Total: **10/10 for this AI response under the uncalibrated rubric**.

The submitted output labels `[W,U,X,V]`, levels `[3,2,1,0]`, inverse `[2,0,3,1]`, transported selection 2/X, backward click 2/W and relation `[2,1,-1]` are correct. The response does not infer persistent IDs or per-face turnover invariance from aggregate assertions.

For the new two-stage map, `q[p[i]]=[2,3,1,0,4]`, final labels `[M,L,J,K,N]` and original K at final slot 3 are correct. The coordinator's extra prompt ambiguously said “those maps”; the response explicitly considered both `p` versus `q` and `p` versus the composition. A later prompt should name the pair and index domains. That prompt ambiguity was not in the source lesson.

### CS-009

Provisional task scores: panel composition 2; cycle/zero interpretation 2; DAG arithmetic 2; incomplete-order handling 2; transfer boundary 2. Total: **10/10 for this AI response under the uncalibrated rubric**.

The response derives the panel cycle, preserves absent rigid fields at zero thickness, calculates DAG levels `[0,0,1,2]` and height 0.6, and distinguishes a three-level lower bound from a placement witness. The new flat-chain case correctly gives panel map `[0,0,0,3]` and cycle `0 -> 3 -> 0`, without treating that as proof of physical impossibility.

The original separate handout's task 4 omitted thickness. The response correctly gave `3*t`, then explicitly qualified its use of the lesson's 0.2 example. [Revision 2](cs-009-learner-task-v2.md) now makes missing thickness intentional: require a symbolic bound and identify the missing input. It has not been retested. The original handout and its frozen review-brief binding are preserved. The agent also noted absent numeric crane counts in the redacted lesson; exercise 3 asks which two kinds of count are distinguished and links the source test, so this observation does not establish an erroneous lesson claim.

## Isolated Learn migration rehearsal

Using Learn migration prototype `1c8aefd9d273f6e09957067990b4780de9dd63f1`, the coordinator copied a clean, detached Demerzel `d89f9e91242c92205d900bf2baea0f55e3de0751` snapshot into a fresh scratch destination, then generated pages from that copied source:

```text
node scripts/streeling-copy-source.mjs --from <clean-d89f9e9> --out <fresh-scratch-root>
node scripts/sync-streeling.mjs --source <fresh-scratch-root> --out <fresh-scratch-root>
```

Both commands exited 0: 394 copied files; 573 non-course relative links pinned to the source revision; 21 departments; 148 EN/108 FR/108 ES pages. This is the full candidate pilot inventory, not a canonical catalog or an increase in reviewed/published courses. The original goal remains 21 departments/525 core courses.

All nine new pages have the expected source/edit paths. A source-level check examined 21 relative references across them: 17 resolve to generated locale files, four refer to English-only CS-006/VC-007 with the explicit localized English-only label. Both dependencies exist in this full candidate copy. PR #197's current smaller copy does not yet contain them.

The initial checker incorrectly resolved links from a Markdown file parent, then incorrectly required a locale-specific source file. Inspection of the existing generator and its tests refuted the suspected generator defect: the intended contract keeps localized URLs and relies on Starlight's English fallback, with a visible label. The existing suites were replayed:

```text
node --test scripts/tests/sync-streeling.test.mjs scripts/tests/streeling-copy-source.test.mjs
16 passed; 0 failed
```

No generator code was changed. No Astro render was performed, so this receipt verifies generated references and the existing test contract, not runtime fallback routes. `migration-rehearsal.json` records these limits and the discarded hypotheses.

After archiving this evidence, `pwsh scripts/verify.ps1` exited 0: 804 Python tests with two skipped, the IXQL grammar checks and BAML source/client parity. A separate integrity check verified all three raw-response byte copies, manifest response hashes and reproducibility of the five-block redactions from the exact Git source. Verifier-generated BAML line-ending changes were confirmed semantically empty and restored. No original course, bound review packet or production status was edited.

The prototype excludes fixtures and production/research/review records. Its `View source` and edit links point to unmerged Learn main paths; non-course links pin a local-only Demerzel commit. Public reachability is not established. This output is not publishable until the source and companion artifacts have an authoritative integration location. Existing Learn worktrees were untouched, and no migration-owner branch, source freeze, deployment or public readback was performed.

## Next use of this evidence

Carry the course sources, dependencies and companion evidence together into the approved migration route. Give the revised handout to a learner with a recorded pre-lesson baseline and a separate later transfer task; preserve first responses before feedback. Obtain actual subject and language verdicts, then generate, render, deploy and read back the exact public course revision. AUD-001's human reviewer remains for the user to designate.

The useful agentic lesson here is concrete: a failing checker is a hypothesis about the product. Check the existing behavior contract before changing the product; archive the rejected hypothesis as well as the successful calculation. A prepared task, a correct AI answer, a generated page and a reviewed published course are separate observations.
