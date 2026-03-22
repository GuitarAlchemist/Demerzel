---
name: demerzel-self-diagnostic
description: Agent health self-check — detect context exhaustion, action loops, wrong repo, git failures, task drift, and confidence miscalibration before they cascade.
---

# Demerzel Self-Diagnostic

An agent invokes this skill to check its own operational health. Designed to catch the failure modes that caused the session-003 incidents: idle-looping after context exhaustion (5x), filing issues on the wrong repo (3x), and requiring 3 prompts to confirm task completion.

Run self-diagnostic **before starting work**, **after any anomaly**, and **whenever you feel uncertain about your own state**.

## Usage

`/demerzel self-diagnostic` — full six-check suite, print report
`/demerzel self-diagnostic --context` — context usage check only
`/demerzel self-diagnostic --loops` — repeated action detection only
`/demerzel self-diagnostic --cwd` — CWD and repo verification only
`/demerzel self-diagnostic --git` — git conflict and push failure detection only
`/demerzel self-diagnostic --task` — task boundary alignment check only
`/demerzel self-diagnostic --confidence` — confidence calibration check only
`/demerzel self-diagnostic --fast` — checks 1-3 only (pre-task quick scan)

## The Six Checks

---

### Check 1: Context Usage

**What it detects:** Context window approaching exhaustion — the condition that caused Architect to idle-loop 5x in session-003.

**How to run:**
1. Count approximate tokens consumed: system prompt + conversation history + tool outputs + current message
2. Compare against known model context limits (claude-sonnet: ~200k tokens)
3. Check whether instructions in the conversation mention "context is getting large", "context window", or "summarize"

**Thresholds:**

| Usage | Status | Action |
|-------|--------|--------|
| < 60% | GREEN | Proceed normally |
| 60-79% | YELLOW | Finish current task, do not start new long tasks |
| 80-89% | ORANGE | Complete atomic unit only, then handoff or compact |
| >= 90% | RED | Stop. Do not begin new tool calls. Summarize state and exit gracefully. |

**Failure signature:** Agent continues invoking tools after RED threshold → idle loop / repeated no-op calls.

**Output:**
```
[CHECK 1: CONTEXT] estimated ~{N}% used → {STATUS}
  Action: {prescribed action or "proceed"}
```

---

### Check 2: Repeated Action Detection

**What it detects:** Action loops — same tool called 3+ times with identical arguments within the current session. The canonical loop failure mode.

**How to run:**
1. Scan conversation history for tool calls
2. For each tool name, group calls by argument fingerprint (tool name + key args, ignore timestamps/run IDs)
3. Flag any group with count >= 3

**Loop patterns to detect:**

| Pattern | Example | Classification |
|---------|---------|----------------|
| Same read, same path | `Read file.txt` × 3 | CONTENT_LOOP |
| Same search, same query | `Grep "foo"` × 3 | SEARCH_LOOP |
| Same write, same content | `Write x.json` × 3 | WRITE_LOOP |
| Same API call | `gh issue list --repo X` × 3 | API_LOOP |
| Same no-result action | `Bash ls` × 3 → same output | IDLE_LOOP |

**Response per loop type:**

- CONTENT_LOOP / SEARCH_LOOP: Already have this data. Do not repeat. Use cached result.
- WRITE_LOOP: Already wrote this. Verify the file exists before writing again.
- API_LOOP: Cache the result and stop polling. Check for rate limit or auth issue.
- IDLE_LOOP: Stop immediately. This is context exhaustion or task completion confusion. Run Check 1 and Check 5.

**Output:**
```
[CHECK 2: LOOPS] {N} repeated patterns detected
  IDLE_LOOP: Bash("ls /repo") called 4x — STOP
  SEARCH_LOOP: Grep("policy") called 3x — USE CACHED RESULT
```

---

### Check 3: CWD Verification

**What it detects:** Operating in the wrong repo or wrong branch — the condition that caused background agents to file issues on the wrong repo 3x in session-003.

**How to run:**
1. Read the current working directory
2. Check `git remote get-url origin` to identify the repo
3. Compare repo name against the assigned task's target repo
4. Check `git branch --show-current` against expected branch

**Verification matrix:**

| Assigned repo | Expected remote contains | Expected branch |
|---------------|--------------------------|-----------------|
| Demerzel | `Demerzel` or `demerzel` | `master` |
| ix | `ix` (not demerzel-bot) | `main` |
| tars | `tars` | `main` |
| ga | `ga-client` or `ga-react` | `main` or `develop` |

**Failure responses:**

- Wrong repo detected → **STOP. Do not read, write, or push. Report the mismatch.** State: "I am in [actual repo] but assigned to [expected repo]. Stopping all actions."
- Wrong branch → warn, confirm with user before proceeding if task involves commits or pushes
- Detached HEAD → escalate immediately, do not commit

**Output:**
```
[CHECK 3: CWD] repo={actual-repo} branch={branch}
  Expected: repo=Demerzel branch=master → MATCH / MISMATCH
```

---

### Check 4: Git Conflict Detection

**What it detects:** Failed push, unresolved merge conflict, or mid-conflict state that could corrupt subsequent operations.

**How to run:**
1. Check for conflict markers in recently modified files: `git diff --check`
2. Check `git status` for "both modified", "unmerged paths", or "rebase in progress"
3. Check if last push succeeded: look for recent push failure in conversation history or `git log --remotes`
4. Check for `.git/MERGE_HEAD`, `.git/rebase-merge/`, `.git/CHERRY_PICK_HEAD`

**Failure states:**

| State | Indicator | Action |
|-------|-----------|--------|
| Active conflict | `MERGE_HEAD` exists | STOP. Do not commit. Report conflict files. |
| Rebase in progress | `rebase-merge/` exists | STOP. Complete or abort rebase first. |
| Diverged from remote | local ahead AND remote ahead | Warn. Pull --rebase before next push. |
| Push failed last attempt | Push failure in conversation | Diagnose: auth? conflicts? protected branch? |
| Clean | None of the above | GREEN |

**Output:**
```
[CHECK 4: GIT] status={CLEAN|CONFLICT|REBASE|DIVERGED}
  Detail: {specific issue or "no conflicts detected"}
```

---

### Check 5: Task Boundary Check

**What it detects:** Scope creep, task drift, or task completion confusion — the condition that required 3 prompts for Auditor to confirm completion in session-003.

**How to run:**
1. Re-read the original task assignment (first user message or assigned issue)
2. List actions taken so far in the current session
3. Check: is the current action traceable to the original task?
4. Check: does the original task appear complete (all acceptance criteria met)?

**Boundary rules:**

| Condition | Classification | Action |
|-----------|---------------|--------|
| Current action matches task | IN_SCOPE | Proceed |
| Task complete, still working | OVER_COMPLETION | Stop. Declare done. Commit and report. |
| Action outside task scope | SCOPE_CREEP | Stop. Log potential follow-up. Return to task. |
| Task unclear or no assignment | UNANCHORED | Ask for clarification before proceeding |
| Working in wrong issue/PR | WRONG_TARGET | STOP. Verify target before any write operation. |

**Completion signals to check:**
- All files specified in task have been created or modified
- All acceptance criteria explicitly met
- No pending verification steps
- Ready to commit and declare done

**Output:**
```
[CHECK 5: TASK] task="{first 60 chars of task}" status={IN_SCOPE|OVER_COMPLETION|SCOPE_CREEP|UNANCHORED}
  Completed: {N of M acceptance criteria}
  Current action: {IN_SCOPE|OUT_OF_SCOPE}
```

---

### Check 6: Confidence Calibration

**What it detects:** Claims made without supporting evidence — assertions that exceed what has actually been verified. Prevents the pattern of declaring success before actually checking.

**How to run:**
1. List all claims made in the current session (assertions about file contents, test results, counts, repo state)
2. For each claim, check whether it was directly verified via tool output in this session
3. Compute: evidence_ratio = verified_claims / total_claims

**Calibration thresholds:**

| Evidence ratio | Status | Meaning |
|----------------|--------|---------|
| >= 0.9 | CALIBRATED | Claims well-supported |
| 0.7-0.89 | ACCEPTABLE | Minor unverified assumptions — flag them |
| 0.5-0.69 | UNDERVERIFIED | Stop and verify the flagged claims before proceeding |
| < 0.5 | MISCALIBRATED | Do not commit or report. Re-read and re-verify. |

**Common miscalibration patterns:**
- "The file was created" — without reading the file back to confirm
- "All tests pass" — without reading CI output in this session
- "The count is N" — without actually counting files via glob
- "The issue was filed on repo X" — without confirming `gh issue view` output shows repo X

**Output:**
```
[CHECK 6: CONFIDENCE] {verified}/{total} claims verified → {STATUS}
  Unverified: "file was created" — read it back before declaring done
  Unverified: "count is 14" — run glob to confirm
```

---

## Full Diagnostic Report Format

```
=== Demerzel Self-Diagnostic — {timestamp} ===

[CHECK 1: CONTEXT]    ~{N}% used → {GREEN|YELLOW|ORANGE|RED}
[CHECK 2: LOOPS]      {CLEAN|N loops detected: ...}
[CHECK 3: CWD]        repo={repo} branch={branch} → {MATCH|MISMATCH}
[CHECK 4: GIT]        {CLEAN|CONFLICT|REBASE|DIVERGED}
[CHECK 5: TASK]       {IN_SCOPE|OVER_COMPLETION|SCOPE_CREEP|UNANCHORED}
[CHECK 6: CONFIDENCE] {N}/{M} verified → {CALIBRATED|ACCEPTABLE|UNDERVERIFIED|MISCALIBRATED}

Overall: {HEALTHY|DEGRADED|CRITICAL}
Action:  {Proceed | {specific corrective action}}

==========================================
```

**Overall status rules:**
- HEALTHY: all checks GREEN / CALIBRATED / MATCH / CLEAN / IN_SCOPE
- DEGRADED: any YELLOW, ACCEPTABLE, or minor warning — proceed with noted constraints
- CRITICAL: any RED, LOOP, MISMATCH, CONFLICT, SCOPE_CREEP with writes, or MISCALIBRATED — stop and correct before proceeding

---

## When to Run

| Trigger | Checks to run | Rationale |
|---------|---------------|-----------|
| Start of session | All 6 | Baseline — establish known-good state |
| Before any commit | 2, 3, 4, 5, 6 | Prevent committing in wrong state |
| Before filing any issue/PR | 3, 5 | Prevent wrong-repo filing |
| After 10+ tool calls | 1, 2 | Catch context exhaustion and loops early |
| After any push failure | 4 | Diagnose git state |
| When uncertain about completion | 5, 6 | Auditor clarity check |
| Any time behavior feels repetitive | 2, 1 | Loop detection |

---

## Integration

### With demerzel-drive

The driver's EXECUTE phase should run `/demerzel self-diagnostic --fast` (checks 1-3) before dispatching each agent. If any check is CRITICAL, the agent is not dispatched and the task is marked `blocked_by_health_check`.

### With demerzel-audit

The auditor persona should run `/demerzel self-diagnostic` before declaring any task complete. Check 6 (confidence calibration) is the auditor's primary gate.

### With demerzel-loop

Loop detection (Check 2) feeds into `demerzel-loop` for pattern analysis and anti-pattern logging.

---

## Governance

- Article 2 (Transparency) — agent must report its own health state honestly
- Article 7 (Auditability) — diagnostic results logged to `state/driver/health-checks/`
- Article 8 (Observability) — health metrics exposed as governance signals
- Article 9 (Bounded Autonomy) — RED context or CRITICAL status constrains agent authority
- Alignment policy — confidence miscalibration triggers alignment review

## Origin

Motivated by session-003 failure modes (2026-03-23):
- Architect idle-looped 5x after context exhaustion → Check 1 + Check 2
- Background agents filed issues on wrong repo 3x → Check 3
- Auditor required 3 prompts to confirm task completion → Check 5 + Check 6
- Git push failure left one agent in diverged state → Check 4

## Source

`policies/autonomous-loop-policy.yaml`,
`policies/alignment-policy.yaml`,
`policies/proto-conscience-policy.yaml`,
`constitutions/default.constitution.md` Articles 2, 7, 8, 9
