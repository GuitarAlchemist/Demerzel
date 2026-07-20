---
category: harness
date: 2026-07-20
topic: PowerShell discards native command exit codes, so the repo oracle passed while its only test failed
source: PR #778, issues #780 / #782
---

# The oracle exited 0 while its only executable test exited 1

## Symptom

`pwsh -NoProfile -File scripts/verify.ps1` reported success. Its npm leg printed
`No language found` and returned 1. The two facts coexisted for roughly two months
and nothing noticed.

```
$ npm test
> tree-sitter test
No language found
NPM_TEST_EXIT=1

$ pwsh -NoProfile -File scripts/verify.ps1 > out.txt 2>&1; echo "VERIFY_EXIT=$?"
VERIFY_EXIT=0
```

## Root cause

`$ErrorActionPreference = 'Stop'` does **not** cover native command exit codes.
That is governed by a separate setting:

```
$PSNativeCommandUseErrorActionPreference   ->   False
```

`verify.ps1` called `npm ci` and `npm test` bare and never tested `$LASTEXITCODE`,
so a non-zero exit was discarded. The script's only remaining assertion was
"every JSON file parses."

Measured on pwsh 7.5.8. The default for that preference has varied across
PowerShell versions, so do not assume it from memory — print it.

## Solution

Check `$LASTEXITCODE` explicitly after every native call. A shared helper keeps
it honest, because the failure mode is *forgetting* rather than getting it wrong:

```powershell
# $ErrorActionPreference = 'Stop' does NOT cover native command exit codes
# ($PSNativeCommandUseErrorActionPreference is False here), so every native
# call below must be checked explicitly or its failure is silently discarded.
function Assert-NativeSuccess([string]$what) {
    if ($LASTEXITCODE -ne 0) {
        throw "$what failed with exit code $LASTEXITCODE"
    }
}

npm ci
Assert-NativeSuccess 'npm ci'
npm test
Assert-NativeSuccess 'npm test'
```

Merged in #778. Verified: the oracle now exits 1, naming the failing command.

## Failed attempts and a diagnostic trap

**Measuring the exit code through a pipe reports the wrong process.** The first
measurement looked green:

```bash
pwsh -File scripts/verify.ps1 | tail -5; echo $?     # reports tail's status: 0
```

`$?` after a pipeline is the *last element's* status. Re-measured without the
pipe, the true exit was 1. A reviewer later made the same class of error one
level up — reading the wrapper script's exit code as the leg's exit code.

**Capture the exit code immediately, from a non-piped invocation**, or use
`${PIPESTATUS[0]}`.

## What the fix exposed

Making the oracle honest did not make it green. It surfaced a real defect that
had been hidden the whole time: the grammar cannot generate at all.

```
$ npx tree-sitter generate
Unresolved conflict for symbol sequence:  'stdin'  •  'csv'  …
exit 1
```

Three causes compounded, and all three were required:

1. `package.json`'s `test` script is `tree-sitter test` with **no `generate`
   step**, so a failed generate never blocked the test.
2. `tree-sitter-ixql/src/` had never existed and was not gitignored — never
   generated, never committed, never missed.
3. The swallowed exit code hid the resulting failure.

Tracked in #780.

## Prevention

- **Never add a bare native call to a PowerShell script.** Route it through a
  helper that throws on non-zero.
- **Print `$PSNativeCommandUseErrorActionPreference`** rather than assuming it.
- **Do not make a failing leg conditional to get green.** The tempting fix here
  was to skip the npm block when `tree-sitter-ixql/` is absent — that
  reintroduces the vacuous pass under a new name. A red oracle for a real reason
  is the goal state.
- **Pair a status-producing artifact with something that recomputes it.** A
  related finding (#782): `state/quality/demerzel-harness/last.json` recorded
  `"oracle_status": "ok"` from a hand-written commit dated two months before the
  breakage, and the overseer reported green from it. Deriving the status from an
  actual run, and expiring the artifact, are two independent fixes and both are
  needed.

## The pattern this belongs to

Four instances surfaced in one session, all the same shape — **a failure
presenting as an ordinary success signal**:

| Instance | Silent signal | Reality |
|---|---|---|
| Repo oracle (#778) | exit 0 | only executable test failing |
| Overseer (#782) | `oracle_status: ok` | derived from a 2-month-stale literal |
| Budget gate (#794) | governed `block` | invalid policy, indistinguishable from a real denial |
| CI ideation loop (#798) | ran green for months | `\| head -N` began SIGPIPE-ing once the backlog exceeded N |

The generalisable rule: **when a check reports success, ask what it would do if
the thing it checks were broken.** If the answer is "the same thing," it is not a
check. Each of these passed a green CI run while asserting nothing.

## Related

- #778 — the fix
- #780 — the grammar defect it exposed
- #782 — status artifact never recomputed
- #794 — same shape in the budget gate's AFK path
- #798 — same shape in a GitHub Actions loop (`pipefail` + `head`)
