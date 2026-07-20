# Backlog

The queue `supervised-loop` pulls from. It picks **the smallest unchecked entry**,
implements it, runs the oracle (`pwsh scripts/verify.ps1`), emits cycle evidence,
and stops — one slice per cycle, no chaining.

**This file is the ratification gate.** An entry lands here only via a merged PR, so
a human has accepted it before any agent can pick it up. Adding an entry is the
decision; checking it off is just bookkeeping.

**Termination:** the loop is done when there are no unchecked entries. Not "until the
architecture is clean" — that has no fixed point.

## How to use

- Entries are ordered; earlier ones are preconditions for later ones where noted.
- Each entry must fit one cycle: **≤200 lines / ≤10 files** (600 absolute cap).
- `supervised-loop` may only edit `documents`, `scripts/`, `state/`, `.claude/`.
  It cannot touch `policies/`, `constitutions/`, `personas/`, `.github/workflows/`.
- **Do not** delete an entry to skip it. Either do it, or record why not as an ADR so
  future reviews stop re-proposing it (`docs/adr/`).
- 🔒 marks entries that must **not** run unattended — they change the loop's own
  safety gate or lack a regression net. A human drives those.

## Provenance

Candidates from an architecture review of `scripts/` (2026-07-20) using the
`improve-codebase-architecture` vocabulary — module / interface / depth / seam /
locality, with the deletion test applied to each. Ranked by the review; ordering below
follows its precondition chain, not its interest level.

---

## Queue

- [ ] **C1 — Run the Python test suite in the oracle.**
  `scripts/verify.ps1`. ~10 lines, 1 file. **Precondition for everything below.**
  The oracle runs `ConvertFrom-Json` over `*.json` plus one npm test. The 20
  `scripts/test_*.py` modules run **only** in `governance-validate.yml` — so an
  autonomous cycle can gut `demerzel_kit`, `aiw_budget_gate`, or `build_manifest`,
  get a green `verify.ps1`, and commit. Add a `python -m unittest discover -s scripts
  -p 'test_*.py'` block, guarded on `python` being present, failing on non-zero.
  Converts 20 already-written test modules from decorative into load-bearing.
  *Expect pre-existing red tests on first run — that is the finding, not a blocker.*
  *Note: consider extending to Pester (`tests/powershell/`), which C3 depends on.*

- [ ] **C6 — Finish the `demerzel_kit` migration for `compliance_report.py`.**
  `scripts/compliance_report.py`. ~40 lines, 1–2 files. Low risk. Already a declared
  to-do in `CONTEXT.md`. It still carries its own `_now_iso` and `_atomic_write` (a
  hand-rolled duplicate of `kit.atomic_write`), and its docstring cites
  `schemas/contracts/compliance-report.schema.json` while writing with **no
  validation** — the same silent-corruption path `CONTEXT.md` describes for
  `council_emit._write_verdict`. Replace with `kit.write_artifact(..., schema=...)`.
  *Hazard: `write_artifact` raises where `_atomic_write` did not, so a currently
  invalid report will start failing loudly. Run `--dry-run` against ix/tars/ga first
  and confirm the schema matches what `build_report` emits.*

- [ ] **C2 — Add `halt_state()` to `demerzel_kit`, mirroring PowerShell's `Test-HaltAll`.**
  `scripts/demerzel_kit.py`, `run_afk_cycle.py`, `run_ml_feedback_cycle.py`,
  `demerzel_halt.py`. ~60 lines, 4 files + 1 test. Do **after** C1.
  `run_afk_cycle.halt_active()` and `run_ml_feedback_cycle._halt_active()` are
  near-identical 16-line functions that say so in their own docstrings, with a third
  partial copy of the expiry logic in `demerzel_halt.cmd_status`. Neither
  schema-validates the marker (the PowerShell adapter does), and both hardcode the
  path with no seam, so neither is testable. HALT-ALL is described in `CONTEXT.md` as
  "the **only mandatory** cross-repo signal". Return a fact-shape
  `{present, valid, active, reason, marker}`; callers keep their own decisions.
  *Consistent with ADR-0003: `now` stays a per-call parameter, so temporal checks
  remain at point of use.*

- [ ] **C4a — Give `aiw_budget_gate` a public assembly entry point.**
  `scripts/aiw_budget_gate.py`, `scripts/run_afk_cycle.py`. ~80 lines, 3 files.
  The gate hides real depth (O_EXCL locking, ledger invariants, request
  fingerprinting, receipt binding) but leaks it back out: the only in-process caller
  must invoke the **private** `budget._load(budget.POLICY_PATH)` plus a module
  constant, twice per issue, re-reading the same file. `main()` is the only code that
  knows the correct assembly and is reachable only as a subprocess — which is why
  `run_afk_cycle` catches bare `Exception` and invents a reason code
  (`budget_preflight_error`) the gate never emits. Add `open_gate(...)` /
  `reserve_request` / `release_job`; promote `_request_sha256` to public.
  *Do not refactor `_lock` in this slice — a crash between acquire and the `finally`
  wedges the ledger, and that path is untested.*

- [ ] 🔒 **C3a — Make `supervised-loop-preflight.ps1` consume `Get-DomainGateState`.**
  `scripts/supervised-loop-preflight.ps1`, `scripts/DomainGate.psm1`. ~40 lines.
  **Human-driven — this is the loop's own safety gate.**
  `Get-DomainGateState` is a genuinely deep module with **zero callers**: both the
  overseer and preflight `Import-Module` it and then reach past it to leaf helpers.
  `CONTEXT.md` claims these are "thin deciders that weigh those facts themselves" —
  they are not. Worse, the two scripts read protected paths from **different sources**
  (`baseline.json` vs `$script:ProtectedPaths`) and nothing checks they agree.
  Start with preflight (the safest slice), single-sourcing on `Get-ProtectedPaths`.
  *Blocked on: C1 extended to run Pester. There is no `DomainGate.Tests.ps1` and no
  overseer test at all, so today this refactor has no regression net.*

- [ ] 🔒 **C5a — Thread a `root` seam through `build_manifest.py` (part 1 of 4).**
  `scripts/build_manifest.py`. ~80 lines. **Human-driven.**
  ADR-0001's keystone — the derived manifest every README count, CI invariant and
  sibling repo reads — is 545 lines with **no test file**, because `REPO` is a module
  global all 9 harvesters reach for directly. There is no `root` parameter anywhere,
  so no seam to test against a fixture. Introduce `root: Path` (defaulting to `REPO`)
  through `harvest_inventory` + `_first_yaml_doc`.
  *Stop rule: this slice must produce a **byte-identical** `governance-manifest.json`.
  A non-empty diff means stop and escalate. Remaining parts (validators, fixture
  tests, README-parser dedupe) are separate entries once this lands.*

---

## Deliberately not queued

- **`council_emit` vs `.github/scripts/llm_call.sh` provider drift.** Real and
  confirmed — the two have already diverged on model ids (shell pins
  `claude-sonnet-4`/`gemini-2.0-flash`, Python pins `claude-opus-4-8`/
  `gemini-2.5-flash`) and on error contracts. But the shell half lives under
  `.github/`, at or past the loop's edit boundary. Needs a human and a plan, not a
  cycle.
- **Possible dead modules** — `aiw_lane_selector.py`, `aiw_prompt_pack.py`,
  `poincare_roadmap.py`, `seldon_intelligence_dry_run.py`,
  `streeling_tracer_bullet.py`, `planner_*.py` have no production callers (tests and
  docs only). This is a `/demerzel evolve` question, not a refactor — and
  cleanup candidates are usually false positives until verified against docs and
  consumer counts.
- **17 scripts recomputing the repo root** two different ways despite `kit.ROOT`.
  Too small to spend a cycle on; fold into whichever entry touches the file.
