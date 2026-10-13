# FUT-003 bounded review brief

Status: **open**. This packet invites human subject review and a learner trial; it is not an approval receipt.

## Frozen source and fixture

- English course: [`fut-003-agent-substitution-readiness-drill.md`](https://github.com/GuitarAlchemist/Demerzel/blob/c94eae19edc60388b23db5d311b67644bd77178d/state/streeling/courses/futurology/en/fut-003-agent-substitution-readiness-drill.md), Demerzel commit `c94eae19edc60388b23db5d311b67644bd77178d`, Git blob `7ebfe049996ac0457aad4cd1f791db777d21a9dd`.
- Synthetic fixture, evaluator, and result: `state/streeling/fixtures/futurology/fut-003/` at Demerzel commit `789239053dfeca9f044d2f893a3f277cb4ed9d8d`.
- Production record: `state/streeling/course-productions/cp-futurology-2026-10-12-003.json`; review and publish flags are false. No translations are declared.

If the English source changes, review its diff and new blob before carrying a verdict forward.

## Subject and method review

1. Re-run `python state/streeling/fixtures/futurology/fut-003/evaluate_drill.py` and compare with `adapter-results.json`. Confirm that `current` and `portable` pass 3/3 with synthetic medians 40 and 32 minutes; `fast` passes 1/3 and `shortcut` 0/3.
2. Inspect each hard gate: matching input/output/review target; `approved` fixture label; and `build`, `targeted_test`, `public_readback`. Look for any sentence treating these fixture strings as real Git blobs, authenticated human approval, or an anonymous network readback.
3. Examine the proposed composable stage notation. Is it clear that this is a teaching sketch rather than an implemented DSL? Does the lesson preserve the distinction between an agent-generated claim and an independently recorded human verdict?
4. Challenge the claim that the same three tasks make candidate agents comparable. What adapter-specific setup, task difficulty, reviewer time, correction time, cost, and environment evidence would a real trial require? Are the trigger and rejection criterion predeclared and falsifiable?
5. Attempt the five exercises before reading their answer blocks. Check the source mismatch, missing readback, median arithmetic, draft-versus-public outcome, and limited decision for `portable`.

## Answer-free learner trial

Give [`fut-003-learner-task.md`](fut-003-learner-task.md) without the course answers or this brief. Record prior agent-workflow experience, elapsed time, unedited response, confusion, and any revision followed by retest.

The transfer case has `nova` runs D/E/F. D has a pending review; E lacks `targeted_test`; F passes all synthetic gates. Expected admissible count: **1/3**. A whole-adapter median should not be used because two cases fail hard gates, even though all three have times. Score five criteria 0–2: (1) gate application per case; (2) no misleading aggregate speed claim; (3) exact-source and independent human provenance; (4) real-trial trigger and falsifier; (5) explicit synthetic-versus-live distinction. A proposed pilot pass is at least 8/10 without treating the fixture as human approval or site evidence. Confirm that threshold after an actual trial; no learner result exists yet.

## Verdict and publication boundary

Record reviewer identifier or pseudonym, UTC date, exact course blob, review kind (`subject` or `learner`), evidence, findings, and `approved`, `changes_requested`, or `not_assessed`. The draft exact-source receipt contract in Demerzel PR #1211 still needs human schema review. This brief cannot issue such a receipt.

Keep review and publish flags false until genuine review and learner results are recorded. After accepted source integration, generate Learn and anonymously read back the page at its intended source revision. A local import is not a public readback.
