# AFK Agent + Harness Doctrine Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Close the missing "implement" step in Demerzel's existing autonomous machinery: a labelled GitHub issue → an away-from-keyboard agent running headless Claude Code inside a Docker sandbox → a branch + PR that the existing review gates handle; plus reconcile `CLAUDE.md` doctrine with Matt Pocock's harness philosophy.

**Architecture:** A stdlib-only Python **governor** in Demerzel (`scripts/run_afk_cycle.py`, modeled on the working `run_ml_feedback_cycle.py`) reads the `agent-implement` issue queue, honors HALT, classifies risk, and invokes an **agent-agnostic sandcastle harness** living *outside* Demerzel (`../afk-harness/`). The harness runs `claudeCode` in a Docker sandbox against a bind-mount of the target repo, producing a branch + commits; the governor pushes the branch, opens a PR linked to the issue, and writes loop-state + audit. Self-merge is left to the existing gates/human (deferred automation).

**Tech Stack:** Python 3.12 (stdlib only) for the governor + tests; TypeScript / Node + `@ai-hero/sandcastle` + Docker for the harness; `gh` CLI for issues/PRs; existing `agent-blackbox.yml` + `cross-model-review.yml` for review.

## Global Constraints

- Governor and its tests are **Python stdlib-only** (no pip deps) — mirrors `scripts/demerzel_halt.py`. Tests use `unittest`, run via `python -m unittest`.
- The sandcastle harness lives **outside Demerzel** at `../afk-harness/` (sibling of the repo) — Demerzel stays spec-only per `.claude/rules/no-runtime-code.md`. Never add `package.json`/`node_modules` inside Demerzel.
- Sandbox backend = **Podman** (rootless, daemonless — no Docker Desktop app). The governor preflight runs `podman machine start` idempotently so a host reboot needs no manual step. Docker/WSL backends are deferred.
- Agent model = `claude-opus-4-8`, effort `medium` (matches current ecosystem default; agent-agnostic — no model-specific tuning).
- **HALT** (`~/.demerzel/HALT-ALL`) is honored as the first action of every cycle; halted → exit 3, no work.
- **No edits to `constitutions/` or `policies/`.** Issues that would touch them classify as `critical` → the agent never implements them; it comments "needs human pre-approval" and skips.
- Loop-state files validate against `schemas/loop-state.schema.json` (`loop_id` pattern `^loop-\d{4}-\d{2}-\d{2}-\d{3}$`; `repo` enum includes `demerzel`).
- Cycle audit summaries go to `state/oversight/` (atomic temp+replace), **never** `state/evolution/` (that schema rejects run-logs — broke CI in #373/#375).
- Conventional commits; every commit message ends with `Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>`. Work stays on branch `feat/afk-agent-harness-doctrine` (already created). Do not push unless the executor is told to.
- Authorization trace: every AFK action references the originating issue number (Default Constitution Art. 7 auditability).

---

## File Structure

**In Demerzel (spec + governance + governor):**
- Create: `scripts/run_afk_cycle.py` — the governor (stdlib only)
- Create: `scripts/test_run_afk_cycle.py` — unittest suite for governor pure functions
- Create: `prompts/afk-implement.prompt.md` — operating instructions fed to headless Claude Code (procedure; never auto-loaded)
- Create: `docs/agents/afk-agent.md` — behavioral spec for the AFK agent
- Modify: `docs/agents/triage-labels.md` — add `agent-implement` label semantics
- Modify: `CLAUDE.md` — add "Harness doctrine (Pocock delta)" section
- Create: `state/loops/.gitkeep`, `state/oversight/.gitkeep` (if absent)
- Create: `docs/solutions/agentic/2026-06-22-pocock-harness-afk.md` — /learnings capture

**Outside Demerzel (runtime harness):**
- Create: `../afk-harness/package.json`
- Create: `../afk-harness/.sandcastle/main.ts` (scaffolded by `init`, then adapted into the CLI wrapper)
- Create: `../afk-harness/.sandcastle/Dockerfile` (from `init` / `build-image`)
- Create: `../afk-harness/README.md`

---

## Task 1: Reconcile CLAUDE.md doctrine (Deliverable 1)

Pure documentation. Independently reviewable; no test cycle.

**Files:**
- Modify: `CLAUDE.md` (append a new section before "## Session-learned rules")
- Create: `docs/solutions/agentic/2026-06-22-pocock-harness-afk.md`

**Interfaces:**
- Produces: the doctrine section other tasks reference for the "queue not loop" and "procedures vs abilities" framing. No code symbols.

- [ ] **Step 1: Add the Harness doctrine section to CLAUDE.md**

Insert this block immediately before the line `## Session-learned rules`:

```markdown
## Harness doctrine (Pocock delta, 2026-06-22)

From the Matt Pocock × David Ondrej transcript (`sources/chats/matt-pocock-david-ondrej-agentic-workflow.md`). Reconciles with the Karpathy 4 Rules and Cherny patterns above — **agree = keep, diverge = adjust**.

- **Harness ≈ model (50/50), stay agent-agnostic.** Optimize the harness (prompts, skills, codebase, sandbox) as much as the model, and don't over-fit to one model. A codebase that's *easy to change* lets a *cheaper* model do the same work. Optimize **AX (Agent Experience)** the way you optimize DX. *(New — extends `project_harness_engineering_direction`.)*
- **Queue, not loop.** A backlog of scoped tasks with human-in-the-loop checkpoints pushed as far right as safe beats an infinite Ralph loop. Our queue already exists: `demerzel-driver-triggers.yml` → `state/triggers/*.trigger.json`. *(Adjusts the Ralph-loop framing in `policies/autonomous-loop-policy.yaml`, which already models this via triggers.)*
- **Procedures over abilities.** Skills the user/governor invokes ("procedures") keep their descriptions out of the context window; model-invoked "abilities" leak a description each. Prefer procedures; keep user-only skills from auto-loading. *(Tension with superpowers' "model-in-control" — we document the tension rather than remove superpowers.)*
- **Delete → observe → layer back.** Periodically strip skills/MCP/instructions to a blank slate, watch the bare agent, then re-add only procedures you choose. `demerzel-context-budget` is the tool for this.
- **Review the system, not just the code.** "If someone keeps stealing your bike, buy a lock." Reinforces our existing `metafix` + ml-feedback loop — no change, cited for convergence.
- **Strategic > tactical (Ousterhout).** AI ate tactical programming; be the strategic delegator. Converges with Karpathy R1 (think first) + R4 (goal-driven) — keep.
```

- [ ] **Step 2: Write the /learnings capture**

Create `docs/solutions/agentic/2026-06-22-pocock-harness-afk.md`:

```markdown
---
category: agentic
date: 2026-06-22
topic: Pocock harness philosophy + AFK agents
source: sources/chats/matt-pocock-david-ondrej-agentic-workflow.md
---

# Surprises from the Pocock × Ondrej transcript

- **"Queue, not loop."** Matt explicitly deflates the Ralph-loop hype as "mostly
  nonsensical." Real AFK work is a task queue (GitHub issues + labels) with
  HITL checkpoints pushed rightward — which is exactly what
  `demerzel-driver-triggers.yml` + `demerzel-autofix.yml` already are. We were
  ~70% of the way to an AFK system without naming it.
- **Abilities leak context.** Every model-invokable skill spends context window
  on its description, every session. Procedures (user-invoked) don't. This is a
  concrete cost argument for the `demerzel-context-budget` discipline.
- **A cheaper model + better harness == a smarter model + worse harness.** "How
  do you optimize token spend? Have a codebase that's easier to change." Guardrails
  reduce the tokens an agent spends banging its head against the wall.
- **Sandbox is non-negotiable for AFK.** Un-sandboxed agents "randomly delete your
  home directory or exfiltrate env vars." Hence Docker for the AFK harness.
- **Closing advice:** delete every skill/MCP/CLAUDE.md, observe the bare agent,
  then layer back only chosen procedures.
```

- [ ] **Step 3: Commit**

```bash
git add CLAUDE.md docs/solutions/agentic/2026-06-22-pocock-harness-afk.md
git commit -m "$(cat <<'EOF'
docs(doctrine): reconcile CLAUDE.md with Pocock harness philosophy

Adds a "Harness doctrine (Pocock delta)" section reconciling Matt Pocock's
queue-not-loop, procedures-over-abilities, harness=model, and delete-the-bloat
principles against the existing Karpathy/Cherny doctrine (agree=keep,
diverge=adjust). Captures surprises via /learnings.

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>
EOF
)"
```

---

## Task 2: AFK operating-instructions prompt

The procedure fed to headless Claude Code inside the sandbox. Pure content; no test.

**Files:**
- Create: `prompts/afk-implement.prompt.md`

**Interfaces:**
- Produces: a prompt file with `{{ISSUE_NUMBER}}`, `{{ISSUE_TITLE}}`, `{{ISSUE_BODY}}` placeholders that the harness fills via sandcastle's `promptArgs`. The governor (Task 4) and harness (Task 6) both reference this path.

- [ ] **Step 1: Write the prompt file**

Create `prompts/afk-implement.prompt.md`:

```markdown
You are an away-from-keyboard implementation agent for the Demerzel governance
repository. You are running headless inside a Docker sandbox with a checkout of
the repo at the current working directory.

## Your task
Implement GitHub issue #{{ISSUE_NUMBER}}: "{{ISSUE_TITLE}}"

Issue body:
{{ISSUE_BODY}}

## Rules (non-negotiable)
1. SCOPE: change only what this issue asks for. No refactoring of adjacent code,
   no unrelated style fixes (Karpathy R3 — surgical changes).
2. SIMPLICITY: the minimum change that satisfies the issue (Karpathy R2).
3. FORBIDDEN: do NOT edit anything under `constitutions/` or `policies/`. If the
   issue requires that, STOP, make no commits, and write a single line to stdout:
   `BLOCKED: requires constitution/policy change — needs human pre-approval`.
4. NO RUNTIME CODE: Demerzel holds only governance artifacts (YAML/MD/JSON/schemas/
   tests). Do not add executable application code.

## Definition of done
1. Make the change.
2. Run the oracle: `python scripts/validate_governance.py`. It must exit 0.
3. If it fails, fix your change until it passes (max 5 attempts), or emit
   `BLOCKED: oracle failing — <reason>` and stop without committing.
4. Commit with a conventional-commit message referencing the issue:
   `<type>(<scope>): <summary> (#{{ISSUE_NUMBER}})` and the trailer
   `Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>`.
5. When done, print: `<promise>COMPLETE</promise>`.
```

- [ ] **Step 2: Commit**

```bash
git add prompts/afk-implement.prompt.md
git commit -m "$(cat <<'EOF'
feat(afk): operating-instructions prompt for the AFK implement agent

Procedure fed to headless Claude Code in the sandbox: scope/simplicity rules,
constitution/policy guardrail, oracle gate (validate_governance.py), and a
COMPLETE completion signal. Referenced by the governor + harness.

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>
EOF
)"
```

---

## Task 3: Label semantics + AFK behavioral spec

Documentation that defines the queue's entry point and the agent's contract.

**Files:**
- Modify: `docs/agents/triage-labels.md`
- Create: `docs/agents/afk-agent.md`

**Interfaces:**
- Produces: the canonical `agent-implement` label name used by the governor's `gh issue list --label agent-implement` query in Task 4.

- [ ] **Step 1: Add the label to triage-labels.md**

Append to `docs/agents/triage-labels.md`:

```markdown
## AFK execution labels

- **`agent-implement`** — Authorizes the AFK agent (`scripts/run_afk_cycle.py`)
  to implement this issue away-from-keyboard inside a Docker sandbox and open a
  PR. Apply only to issues that are well-scoped and non-critical. The agent
  refuses (and comments) if implementing would require editing
  `constitutions/` or `policies/`.
```

- [ ] **Step 2: Write the behavioral spec**

Create `docs/agents/afk-agent.md`:

```markdown
# AFK Agent

The AFK ("away from keyboard") agent is the *implement* step of Demerzel's task
queue. It connects the existing trigger/triage queue to the existing PR review
gates.

## Contract
- **Trigger:** an open GitHub issue labelled `agent-implement`.
- **Authorization:** the issue itself (pre-authorized domain work per
  `policies/autonomous-loop-policy.yaml` → `github_issue`). Governance edits are
  always-pre-authorized governance work.
- **Execution:** `scripts/run_afk_cycle.py` (governor) → `../afk-harness`
  (sandcastle + Docker) runs headless Claude Code with
  `prompts/afk-implement.prompt.md`.
- **Output:** a branch `agent/issue-<n>` + a PR linked to the issue.
- **Review:** the existing `agent-blackbox.yml` + `cross-model-review.yml`
  workflows. Merge is human/gate-decided (self-merge automation deferred).

## Risk gating (from autonomous-loop-policy.yaml)
- `critical` (touches constitutions/policies): never implemented; agent comments
  "needs human pre-approval" and skips.
- `high`/`medium`/`low`: implemented; PR opened for review.

## Safety
- Docker sandbox: no host file damage / env exfiltration.
- HALT (`~/.demerzel/HALT-ALL`) honored before any work.
- Every action traces to the issue number (audit).

## Deferred (graduation steps)
Self-hosted Actions runner (event-driven), parallel sandboxes, self-merge
automation, ga/ix/tars rollout, video+TTS PR walkthroughs.
```

- [ ] **Step 3: Commit**

```bash
git add docs/agents/triage-labels.md docs/agents/afk-agent.md
git commit -m "$(cat <<'EOF'
docs(afk): agent-implement label + AFK agent behavioral spec

Defines the queue entry point (agent-implement label) and the AFK agent's
contract, risk gating, safety, and deferred graduation steps.

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>
EOF
)"
```

---

## Task 4: Governor — pure functions (TDD)

The testable core: HALT detection, risk classification, queue filtering, loop-state construction. Stdlib only.

**Files:**
- Create: `scripts/run_afk_cycle.py`
- Test: `scripts/test_run_afk_cycle.py`

**Interfaces:**
- Produces (consumed by Task 7's live path):
  - `halt_active() -> tuple[bool, str]`
  - `classify_risk(issue: dict) -> tuple[str, str]` — returns `(risk, governance_mode)` where risk ∈ {low,medium,high,critical}, mode ∈ {boundary-only, per-iteration}
  - `is_eligible(issue: dict) -> bool` — True unless risk == "critical"
  - `build_loop_state(issue: dict, seq: int, risk: str, mode: str, today: str) -> dict` — a dict valid against `schemas/loop-state.schema.json`
  - `main(argv: list[str]) -> int`

- [ ] **Step 1: Write the failing test**

Create `scripts/test_run_afk_cycle.py`:

```python
import unittest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
import run_afk_cycle as g


class TestClassifyRisk(unittest.TestCase):
    def test_constitution_is_critical(self):
        issue = {"title": "Update Asimov constitution Article 4",
                 "body": "edit constitutions/asimov.constitution.md",
                 "labels": [{"name": "agent-implement"}]}
        risk, mode = g.classify_risk(issue)
        self.assertEqual(risk, "critical")
        self.assertEqual(mode, "per-iteration")

    def test_policy_is_critical(self):
        issue = {"title": "Refine alignment policy", "body": "tweak policies/alignment-policy.yaml",
                 "labels": []}
        self.assertEqual(g.classify_risk(issue)[0], "critical")

    def test_schema_migration_is_high(self):
        issue = {"title": "Schema migration for personas", "body": "migrate schema",
                 "labels": []}
        risk, mode = g.classify_risk(issue)
        self.assertEqual(risk, "high")
        self.assertEqual(mode, "per-iteration")

    def test_persona_is_medium(self):
        issue = {"title": "Update skeptical-auditor persona voice", "body": "persona tweak",
                 "labels": []}
        self.assertEqual(g.classify_risk(issue)[0], "medium")

    def test_docs_is_low(self):
        issue = {"title": "Fix typo in README", "body": "documentation typo", "labels": []}
        risk, mode = g.classify_risk(issue)
        self.assertEqual(risk, "low")
        self.assertEqual(mode, "boundary-only")


class TestEligibility(unittest.TestCase):
    def test_critical_not_eligible(self):
        self.assertFalse(g.is_eligible({"title": "edit constitutions/x", "body": "", "labels": []}))

    def test_low_eligible(self):
        self.assertTrue(g.is_eligible({"title": "fix docs typo", "body": "", "labels": []}))


class TestLoopState(unittest.TestCase):
    def test_loop_id_pattern_and_required_fields(self):
        issue = {"number": 42, "title": "Fix docs typo", "body": "x", "labels": []}
        st = g.build_loop_state(issue, seq=1, risk="low", mode="boundary-only", today="2026-06-22")
        self.assertRegex(st["loop_id"], r"^loop-\d{4}-\d{2}-\d{2}-\d{3}$")
        for key in ("loop_id", "goal", "repo", "risk", "governance_mode", "status", "iterations"):
            self.assertIn(key, st)
        self.assertEqual(st["repo"], "demerzel")
        self.assertIn("#42", st["goal"])


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run the test to verify it fails**

Run: `python -m unittest scripts.test_run_afk_cycle -v`
Expected: FAIL — `ModuleNotFoundError: No module named 'run_afk_cycle'` (file not created yet).

- [ ] **Step 3: Write the minimal implementation**

Create `scripts/run_afk_cycle.py`:

```python
#!/usr/bin/env python3
"""
Demerzel run_afk_cycle — the AFK implement-lane governor.

Reads the `agent-implement` GitHub issue queue, honors HALT, classifies risk per
policies/autonomous-loop-policy.yaml, and for each eligible (non-critical) issue
invokes the agent-agnostic sandcastle harness (../afk-harness) which runs headless
Claude Code in a Docker sandbox to produce a branch + commits. The governor then
pushes the branch, opens a PR linked to the issue, and records loop-state + audit.
Critical issues (constitution/policy) are skipped with a "needs human pre-approval"
comment. Merge is left to existing review gates (self-merge automation deferred).

Usage:
  python scripts/run_afk_cycle.py --dry-run     # classify + plan, no sandbox/push/PR
  python scripts/run_afk_cycle.py               # run one cycle (live)

Exit codes:
  0  cycle ran (any mix of implemented/skipped/no-op)
  1  usage / environment error
  3  aborted: HALT-ALL marker in effect
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]            # repos/Demerzel
HARNESS_DIR = ROOT.parent / "afk-harness"             # sibling, outside Demerzel
PROMPT_FILE = ROOT / "prompts" / "afk-implement.prompt.md"
LABEL = "agent-implement"
REPO_SLUG = "GuitarAlchemist/Demerzel"

CRITICAL_PATHS = ("constitution", "policies/", "policy")
HIGH_KEYWORDS = ("schema migration", "migrate schema", "cross-repo", "infrastructure")
MEDIUM_KEYWORDS = ("persona", "refactor", "schema")
LOW_KEYWORDS = ("doc", "documentation", "typo", "comment", "test", "config")


def _now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def halt_active() -> tuple[bool, str]:
    """Mirror run_ml_feedback_cycle: ~/.demerzel/HALT-ALL present and not expired."""
    marker = Path.home() / ".demerzel" / "HALT-ALL"
    if not marker.is_file():
        return False, ""
    try:
        data = json.loads(marker.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return True, "HALT-ALL present but unreadable — treating as halted (fail-safe)"
    exp = data.get("expires_at")
    if exp:
        try:
            if datetime.fromisoformat(exp.replace("Z", "+00:00")) < datetime.now(timezone.utc):
                return False, ""
        except ValueError:
            pass
    return True, f"HALT-ALL in effect (reason: {data.get('reason', 'n/a')})"


def _haystack(issue: dict) -> str:
    labels = " ".join(l.get("name", "") for l in issue.get("labels", []))
    return f"{issue.get('title', '')} {issue.get('body', '')} {labels}".lower()


def classify_risk(issue: dict) -> tuple[str, str]:
    """Return (risk, governance_mode). Conservative: any constitution/policy hint
    is critical; schema-migration/cross-repo is high; persona/refactor is medium;
    docs/tests/config is low; unknown defaults to medium (standard governance)."""
    h = _haystack(issue)
    if any(k in h for k in CRITICAL_PATHS):
        return "critical", "per-iteration"
    if any(k in h for k in HIGH_KEYWORDS):
        return "high", "per-iteration"
    if any(k in h for k in LOW_KEYWORDS) and not any(k in h for k in MEDIUM_KEYWORDS):
        return "low", "boundary-only"
    if any(k in h for k in MEDIUM_KEYWORDS):
        return "medium", "boundary-only"
    return "medium", "boundary-only"


def is_eligible(issue: dict) -> bool:
    """Eligible for AFK implementation unless critical (constitution/policy)."""
    return classify_risk(issue)[0] != "critical"


def build_loop_state(issue: dict, seq: int, risk: str, mode: str, today: str) -> dict:
    """A dict valid against schemas/loop-state.schema.json."""
    return {
        "loop_id": f"loop-{today}-{seq:03d}",
        "goal": f"AFK-implement issue #{issue.get('number')}: {issue.get('title', '')}",
        "repo": "demerzel",
        "risk": risk,
        "governance_mode": mode,
        "status": "running",
        "iterations": [],
        "stall_count": 0,
        "authorization_artifact": f"github_issue:#{issue.get('number')}",
        "started_at": _now_iso(),
        "max_iterations": 10,
    }


def _gh_queue(dry: bool) -> list[dict]:
    """Fetch open agent-implement issues via gh. Returns [] on any failure."""
    try:
        p = subprocess.run(
            ["gh", "issue", "list", "--repo", REPO_SLUG, "--label", LABEL,
             "--state", "open", "--json", "number,title,body,labels", "--limit", "20"],
            capture_output=True, text=True, timeout=60)
        if p.returncode != 0:
            print(f"warn: gh issue list failed: {p.stderr.strip()[:160]}", file=sys.stderr)
            return []
        return json.loads(p.stdout or "[]")
    except (OSError, subprocess.TimeoutExpired, json.JSONDecodeError) as exc:
        print(f"warn: gh queue unavailable: {exc}", file=sys.stderr)
        return []


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description="Demerzel AFK implement-lane governor")
    ap.add_argument("--dry-run", action="store_true",
                    help="classify + plan + write loop-state, but do not invoke the "
                         "sandbox, push, or open PRs")
    args = ap.parse_args(argv)

    halted, why = halt_active()
    if halted:
        print(f"ABORT: {why}", file=sys.stderr)
        return 3

    today = _now_iso()[:10]
    issues = _gh_queue(args.dry_run)
    decisions = []
    for seq, issue in enumerate(issues, start=1):
        risk, mode = classify_risk(issue)
        eligible = is_eligible(issue)
        state = build_loop_state(issue, seq, risk, mode, today)
        decision = {"issue": issue.get("number"), "title": issue.get("title"),
                    "risk": risk, "mode": mode, "eligible": eligible,
                    "action": "implement" if eligible else "skip:needs-human-preapproval"}
        if not args.dry_run:
            loops_dir = ROOT / "state" / "loops"
            loops_dir.mkdir(parents=True, exist_ok=True)
            (loops_dir / f"{state['loop_id']}.loop.json").write_text(
                json.dumps(state, indent=2) + "\n", encoding="utf-8")
        decisions.append(decision)

    summary = {"cycle_at": _now_iso(), "dry_run": args.dry_run, "halted": False,
               "queue_size": len(issues), "decisions": decisions,
               "tally": {"implement": sum(1 for d in decisions if d["action"] == "implement"),
                         "skipped": sum(1 for d in decisions if d["action"].startswith("skip"))}}
    if not args.dry_run:
        out = ROOT / "state" / "oversight" / f"afk-cycle-{today}.json"
        out.parent.mkdir(parents=True, exist_ok=True)
        tmp = out.with_suffix(".json.tmp")
        tmp.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
        os.replace(tmp, out)

    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
```

- [ ] **Step 4: Run the test to verify it passes**

Run: `python -m unittest scripts.test_run_afk_cycle -v`
Expected: PASS — all 8 tests OK.

- [ ] **Step 5: Verify dry-run executes without side effects**

Run: `python scripts/run_afk_cycle.py --dry-run`
Expected: prints a JSON summary with `"dry_run": true`. If no `gh` auth / no labelled issues, `queue_size` is 0 and `decisions` is `[]` (no error). No files written under `state/`.

- [ ] **Step 6: Commit**

```bash
git add scripts/run_afk_cycle.py scripts/test_run_afk_cycle.py
git commit -m "$(cat <<'EOF'
feat(afk): governor with HALT, risk classification, dry-run (TDD)

scripts/run_afk_cycle.py reads the agent-implement queue, honors the HALT-ALL
marker, classifies risk per autonomous-loop-policy (critical=constitution/policy
never implemented), and emits loop-state + oversight audit. Pure functions
covered by stdlib unittest; --dry-run has no side effects.

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>
EOF
)"
```

---

## Task 5: Sandcastle harness (outside Demerzel)

The runtime that runs headless Claude Code in a Docker sandbox. Integration-tested (build image + trivial run), not unit-tested.

**Files:**
- Create: `../afk-harness/package.json`
- Create: `../afk-harness/.sandcastle/main.ts` (scaffolded then adapted)
- Create: `../afk-harness/.sandcastle/Dockerfile`
- Create: `../afk-harness/README.md`

**Interfaces:**
- Consumes: `prompts/afk-implement.prompt.md` (copied/mounted at run time), env `ANTHROPIC_API_KEY`, env `GH_TOKEN` (least-privilege).
- Produces: a CLI `npx tsx .sandcastle/main.ts --repo <path> --issue <n> --title <t> --body <b>` that prints one JSON line `{"branch": "...", "commits": [...], "blocked": false|"<reason>"}` to stdout. Task 7's live path parses this.

- [ ] **Step 1a: Ensure Podman is installed and the machine is running**

Podman is the sandbox backend (daemonless; no Docker Desktop). If `podman --version`
fails, install it once (Windows, winget): `winget install -e --id RedHat.Podman --accept-source-agreements --accept-package-agreements` (may require a new shell for PATH, and the machine init needs WSL2). Then initialize and start the VM:
```bash
podman machine init    # one-time; downloads a CoreOS image (skip if a machine already exists)
podman machine start   # idempotent-ish: errors with "already running" if up — that's fine
podman run --rm hello-world   # smoke: confirms the sandbox can run a container
```
Expected: `hello-world` runs and exits cleanly. If install needs admin elevation, run the winget command in an elevated shell (the controller will hand it to the human via `! <cmd>` if it cannot self-install).

- [ ] **Step 1b: Scaffold the project**

Run (from the parent of Demerzel):
```bash
mkdir -p ../afk-harness && cd ../afk-harness
npm init -y
npm install --save-dev @ai-hero/sandcastle tsx typescript
npx @ai-hero/sandcastle init
```
Expected: `.sandcastle/` directory created with a `main.ts`, a `Dockerfile`, and a sample prompt.

- [ ] **Step 2: Build the Podman sandbox image**

Run: `npx @ai-hero/sandcastle podman build-image`
Expected: a local image (default tag per the generated Dockerfile/Containerfile, e.g. `sandcastle:local`) builds successfully. Confirm with `podman images | grep sandcastle`. (Podman reads the same `Dockerfile` sandcastle's `init` generates.)

- [ ] **Step 3: Replace `.sandcastle/main.ts` with the CLI wrapper**

Overwrite `.sandcastle/main.ts`:

```typescript
import { run, claudeCode } from "@ai-hero/sandcastle";
import { podman } from "@ai-hero/sandcastle/sandboxes/podman";
import { parseArgs } from "node:util";

const { values } = parseArgs({
  options: {
    repo: { type: "string" },
    issue: { type: "string" },
    title: { type: "string" },
    body: { type: "string", default: "" },
  },
});

if (!values.repo || !values.issue || !values.title) {
  console.error("usage: tsx main.ts --repo <path> --issue <n> --title <t> [--body <b>]");
  process.exit(1);
}

const promptFile = `${values.repo}/prompts/afk-implement.prompt.md`;

const result = await run({
  agent: claudeCode("claude-opus-4-8", { effort: "medium" }),
  sandbox: podman({ imageName: "sandcastle:local" }),
  cwd: values.repo,
  promptFile,
  promptArgs: {
    ISSUE_NUMBER: values.issue,
    ISSUE_TITLE: values.title,
    ISSUE_BODY: values.body ?? "",
  },
  branchStrategy: { type: "branch", branch: `agent/issue-${values.issue}` },
  maxIterations: 5,
  completionSignal: "<promise>COMPLETE</promise>",
  name: `afk-issue-${values.issue}`,
});

const blockedLine = result.stdout
  .split("\n")
  .find((l) => l.startsWith("BLOCKED:"));

console.log(JSON.stringify({
  branch: result.branch,
  commits: result.commits.map((c) => c.sha),
  blocked: blockedLine ? blockedLine.replace("BLOCKED:", "").trim() : false,
}));
```

> Note: if `init` generated a different import path or `run()` field name, adapt
> to the installed package's actual API (check `node_modules/@ai-hero/sandcastle`
> types). The fields above match the documented `RunOptions`/`RunResult`.

- [ ] **Step 4: Write the README**

Create `../afk-harness/README.md`:

```markdown
# afk-harness

Agent-agnostic AFK (away-from-keyboard) harness. Runs headless Claude Code inside
a Docker sandbox against a checkout of a target repo, producing a branch + commits.
Driven by Demerzel's `scripts/run_afk_cycle.py` governor. Reusable by ga/ix/tars.

## Setup
    npm install
    npx @ai-hero/sandcastle podman build-image   # builds sandcastle:local

## Run (one issue)
    ANTHROPIC_API_KEY=... npx tsx .sandcastle/main.ts \
      --repo ../Demerzel --issue 123 --title "Fix typo" --body "..."

Prints one JSON line: {"branch","commits","blocked"}.

## Why it lives outside Demerzel
Demerzel is spec-only (no runtime code). This harness is the runtime; it stays a
sibling so Demerzel keeps its no-runtime-code invariant.
```

- [ ] **Step 5: Integration smoke test (trivial prompt)**

Create a throwaway test issue locally and run against the Demerzel checkout with a
benign issue (e.g. "add a blank line to README.md"):
```bash
ANTHROPIC_API_KEY=$ANTHROPIC_API_KEY npx tsx .sandcastle/main.ts \
  --repo ../Demerzel --issue 0 --title "smoke: append trailing newline to README.md" \
  --body "Append a single trailing newline to README.md. Trivial."
```
Expected: JSON line with a non-empty `branch` (`agent/issue-0`) and ≥1 commit sha; `blocked: false`. Verify in Demerzel: `git -C ../Demerzel branch --list 'agent/issue-0'` shows the branch. Then clean up: `git -C ../Demerzel branch -D agent/issue-0`.

- [ ] **Step 6: Commit (in the harness repo / dir)**

```bash
cd ../afk-harness
git init -q 2>/dev/null || true
git add package.json .sandcastle/main.ts .sandcastle/Dockerfile README.md
git commit -m "$(cat <<'EOF'
feat: sandcastle AFK harness (Docker) — headless Claude Code per issue

Agent-agnostic CLI wrapper: run --repo --issue --title --body -> branch+commits
via sandcastle docker sandbox. Prints {branch,commits,blocked} JSON. Lives
outside Demerzel to preserve its no-runtime-code invariant.

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>
EOF
)"
```

---

## Task 6: Wire governor → harness (live path)

Connects the tested governor to the smoke-tested harness, adds branch push + PR creation. Integration-tested against one real issue in Task 7.

**Files:**
- Modify: `scripts/run_afk_cycle.py` (add `_invoke_harness`, `_open_pr`, and the live branch in `main`)
- Test: `scripts/test_run_afk_cycle.py` (add a test that the live helpers are not called under `--dry-run`)

**Interfaces:**
- Consumes: harness CLI from Task 5 (`{"branch","commits","blocked"}` JSON), `classify_risk`/`build_loop_state` from Task 4.
- Produces: `_invoke_harness(issue) -> dict`, `_open_pr(issue, branch) -> str` (returns PR URL).

- [ ] **Step 1: Write the failing test**

Add to `scripts/test_run_afk_cycle.py`:

```python
class TestDryRunNoLiveCalls(unittest.TestCase):
    def test_dry_run_does_not_invoke_harness(self):
        import unittest.mock as mock
        with mock.patch.object(g, "_gh_queue", return_value=[
                 {"number": 7, "title": "fix docs typo", "body": "x", "labels": []}]), \
             mock.patch.object(g, "_invoke_harness") as inv, \
             mock.patch.object(g, "_open_pr") as pr:
            rc = g.main(["--dry-run"])
        self.assertEqual(rc, 0)
        inv.assert_not_called()
        pr.assert_not_called()
```

- [ ] **Step 2: Run the test to verify it fails**

Run: `python -m unittest scripts.test_run_afk_cycle.TestDryRunNoLiveCalls -v`
Expected: FAIL — `AttributeError: module 'run_afk_cycle' has no attribute '_invoke_harness'`.

- [ ] **Step 3: Add the live helpers and wire them in**

In `scripts/run_afk_cycle.py`, add these functions above `main`:

```python
def _invoke_harness(issue: dict) -> dict:
    """Run the sandcastle harness for one issue. Returns {branch,commits,blocked}."""
    cmd = ["npx", "tsx", str(HARNESS_DIR / ".sandcastle" / "main.ts"),
           "--repo", str(ROOT), "--issue", str(issue.get("number")),
           "--title", issue.get("title", ""), "--body", issue.get("body", "")]
    p = subprocess.run(cmd, cwd=str(HARNESS_DIR), capture_output=True, text=True, timeout=1800)
    if p.returncode != 0:
        return {"branch": None, "commits": [], "blocked": f"harness exit {p.returncode}: {p.stderr.strip()[:200]}"}
    last = [l for l in p.stdout.strip().splitlines() if l.strip().startswith("{")]
    if not last:
        return {"branch": None, "commits": [], "blocked": "harness produced no JSON result"}
    return json.loads(last[-1])


def _ensure_podman() -> tuple[bool, str]:
    """Restart-robustness: make sure the Podman machine is up before sandboxing.
    Idempotent — 'already running' is success. Returns (ok, note)."""
    try:
        chk = subprocess.run(["podman", "machine", "list", "--format", "{{.Running}}"],
                             capture_output=True, text=True, timeout=30)
    except (OSError, subprocess.TimeoutExpired) as exc:
        return False, f"podman not available: {exc}"
    if chk.returncode == 0 and "true" in chk.stdout.lower():
        return True, "podman machine already running"
    start = subprocess.run(["podman", "machine", "start"],
                           capture_output=True, text=True, timeout=180)
    if start.returncode == 0 or "already running" in (start.stderr + start.stdout).lower():
        return True, "podman machine started"
    return False, f"podman machine start failed: {start.stderr.strip()[:160]}"


def _open_pr(issue: dict, branch: str) -> str:
    """Push the branch and open a PR linked to the issue. Returns the PR URL."""
    num = issue.get("number")
    subprocess.run(["git", "-C", str(ROOT), "push", "-u", "origin", branch],
                   capture_output=True, text=True, timeout=120, check=True)
    p = subprocess.run(
        ["gh", "pr", "create", "--repo", REPO_SLUG, "--head", branch,
         "--title", f"AFK: {issue.get('title', '')} (#{num})",
         "--body", f"Implements #{num} via the AFK agent.\n\nReview gates: agent-blackbox + cross-model-review.\nCloses #{num}"],
        capture_output=True, text=True, timeout=120)
    return p.stdout.strip() if p.returncode == 0 else f"pr-create-failed: {p.stderr.strip()[:160]}"
```

Then, inside `main`'s loop, replace the `if not args.dry_run:` block with:

```python
        if not args.dry_run:
            loops_dir = ROOT / "state" / "loops"
            loops_dir.mkdir(parents=True, exist_ok=True)
            if eligible:
                ok, pnote = _ensure_podman()   # restart-robustness preflight (idempotent)
                if not ok:
                    decision["action"] = f"blocked:{pnote}"
                    state["status"] = "halted"
                    state["halt_reason"] = pnote
                    (loops_dir / f"{state['loop_id']}.loop.json").write_text(
                        json.dumps(state, indent=2) + "\n", encoding="utf-8")
                    decisions.append(decision)
                    continue
                hr = _invoke_harness(issue)
                if hr.get("blocked"):
                    decision["action"] = f"blocked:{hr['blocked']}"
                    state["status"] = "halted"
                    state["halt_reason"] = str(hr["blocked"])
                elif hr.get("branch"):
                    decision["pr"] = _open_pr(issue, hr["branch"])
                    decision["branch"] = hr["branch"]
                    state["iterations"].append({
                        "iteration": 1, "timestamp": _now_iso(),
                        "action": f"opened PR for #{issue.get('number')}",
                        "outcome": "progress", "governance_decision": None})
                    state["status"] = "completed"
            else:
                _comment_needs_preapproval(issue)
                state["status"] = "halted"
                state["halt_reason"] = "critical: needs human pre-approval"
            (loops_dir / f"{state['loop_id']}.loop.json").write_text(
                json.dumps(state, indent=2) + "\n", encoding="utf-8")
```

And add the comment helper above `main`:

```python
def _comment_needs_preapproval(issue: dict) -> None:
    subprocess.run(
        ["gh", "issue", "comment", str(issue.get("number")), "--repo", REPO_SLUG,
         "--body", "🤖 AFK agent: this issue classifies as **critical** "
                   "(touches constitutions/policies) and will not be auto-implemented. "
                   "It needs human pre-approval per autonomous-loop-policy."],
        capture_output=True, text=True, timeout=60)
```

- [ ] **Step 4: Run the tests to verify they pass**

Run: `python -m unittest scripts.test_run_afk_cycle -v`
Expected: PASS — all tests, including `TestDryRunNoLiveCalls`.

- [ ] **Step 5: Commit**

```bash
git add scripts/run_afk_cycle.py scripts/test_run_afk_cycle.py
git commit -m "$(cat <<'EOF'
feat(afk): wire governor to sandcastle harness + PR creation

Live path: eligible issue -> _invoke_harness (sandcastle/Docker) -> push branch
-> gh pr create -> loop-state completed. Critical issues get a needs-preapproval
comment. Dry-run still makes zero live calls (tested).

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>
EOF
)"
```

---

## Task 7: End-to-end tracer bullet (proof of done)

Prove the whole slice on one real low-risk Demerzel issue.

**Files:** none (operational verification)

**Interfaces:** Consumes everything above.

- [ ] **Step 1: Create a real low-risk issue**

Run:
```bash
gh issue create --repo GuitarAlchemist/Demerzel \
  --title "AFK smoke: add a one-line note to docs/agents/afk-agent.md" \
  --body "Append a single line under the Contract section noting the agent was first proven on 2026-06-22. Trivial, low-risk docs change." \
  --label agent-implement
```
Note the issue number `<N>`.

- [ ] **Step 2: Dry-run to confirm classification**

Run: `python scripts/run_afk_cycle.py --dry-run`
Expected: the summary lists issue `<N>` with `"risk": "low"`, `"eligible": true`, `"action": "implement"`.

- [ ] **Step 3: Live run**

Ensure `ANTHROPIC_API_KEY` and a least-privilege `GH_TOKEN` are in the environment, HALT is clear (`python scripts/demerzel_halt.py status` → NOT halted), then:
Run: `python scripts/run_afk_cycle.py`
Expected: summary shows `"action": "implement"` and a `"pr"` URL for issue `<N>`; `state/loops/loop-2026-06-22-001.loop.json` exists with `"status": "completed"`; `state/oversight/afk-cycle-2026-06-22.json` exists.

- [ ] **Step 4: Verify the PR and gates**

Run: `gh pr view <pr-url> --repo GuitarAlchemist/Demerzel`
Expected: PR open from `agent/issue-<N>`, contains the one-line docs change, links issue `<N>`, and the `agent-blackbox` + `cross-model-review` checks are running/passed.

- [ ] **Step 5: Record the proof**

Append to `docs/agents/afk-agent.md` under Contract: a line "First proven end-to-end on 2026-06-22 (issue #<N>, PR <url>)." Commit:
```bash
git add docs/agents/afk-agent.md
git commit -m "$(cat <<'EOF'
docs(afk): record first end-to-end AFK proof (tracer bullet green)

Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>
EOF
)"
```

- [ ] **Step 6: Done check**

The tracer bullet is complete when: the PR for issue `<N>` was opened by the governor via the Docker-sandboxed agent, passed `validate_governance.py` inside the sandbox, and the existing review gates ran on it. Until this step is green, the harness is not "done" (harness-before-harvest).

---

## Self-Review

**Spec coverage:**
- Deliverable 1 (absorb + reconcile doctrine) → Task 1 ✓
- AFK harness outside Demerzel (§4.1.1) → Task 5 ✓
- Governor `run_afk_cycle.py` (§4.1.2) → Tasks 4, 6 ✓
- Operating-instructions procedure (§4.1.3) → Task 2 ✓ (as a prompt file — refinement noted: a prompt file is invoked-only, achieving the no-context-leak goal more directly than a skill flag)
- Governance spec + label (§4.1.4) → Task 3 ✓
- Review gate reuse (§4.1.5) → Tasks 3, 6, 7 (no new gate built) ✓
- Data flow (§4.2) → Tasks 4–7 ✓
- Safety/policy compliance (§4.3): HALT (Task 4), Docker sandbox (Task 5), critical-skip (Tasks 4/6), audit to state/oversight (Task 4) ✓
- Testing/proof (§4.4): dry-run (Task 4), one real issue e2e (Task 7) ✓
- Deferred items (§4.5): self-hosted runner, parallelism, self-merge automation, ga/ix/tars, video/TTS — none implemented; documented in Task 3 spec ✓

**Placeholder scan:** No "TBD"/"add error handling"/"similar to Task N". The one `<N>` token in Task 7 is an operational runtime value (the created issue number), not an unspecified plan detail. The sandcastle import-path caveat in Task 5 Step 3 is an explicit adapt-to-installed-API instruction, not a placeholder.

**Type consistency:** `classify_risk -> (risk, mode)`, `is_eligible`, `build_loop_state`, `halt_active`, `_gh_queue`, `_invoke_harness -> {branch,commits,blocked}`, `_open_pr -> url`, `_comment_needs_preapproval` are defined once (Tasks 4/6) and used consistently. Harness CLI flags (`--repo/--issue/--title/--body`) and its JSON output match between Task 5 (producer) and Task 6 (`_invoke_harness` consumer). Loop-state keys match `schemas/loop-state.schema.json`.
