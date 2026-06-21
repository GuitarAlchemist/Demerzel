# Supervised Autonomous Loop Preflight (Demerzel)
#
# Deterministic gate that runs BEFORE the supervised-loop skill enters
# its cycle on the Demerzel governance repo. Exits 0 if the repo is safe
# to loop, 1 otherwise. Always prints a final line of the form
# `LOOP_READY=true|false reason=<code>` followed by a one-line reason.
#
# Mirrors the hard refusals in .claude/skills/supervised-loop/SKILL.md
# and the producer-reviewer / fresh-evaluator / cross-vendor-review /
# rewrite-budget patterns documented in docs/review-independence.md.

[CmdletBinding()]
param(
    [int]$OverseerMaxAgeHours = 24,
    [string]$OverseerPath = "state/governance/dev-process-overseer.json",
    [string]$RiskPolicyPath = "agent-blackbox.policy.json",
    [string]$BaselinePath = "state/quality/demerzel-harness/baseline.json",
    [string]$StopMarkerPath = ".STOP",
    [string]$DomainStopPath = "state/quality/demerzel-harness/.STOP",
    [string]$GlobalHaltMarkerPath = "state/.loop-halted",
    [string]$HaltAllPath = "$HOME/.demerzel/HALT-ALL",
    [int]$MaxLinesPerCycle = 600,
    [int]$MaxFilesPerCycle = 10
)

$ErrorActionPreference = 'Stop'

$root = Split-Path -Parent $PSScriptRoot
Set-Location -LiteralPath $root

# Shared domain-gate facts: HALT-ALL read + schema-validate + expiry, and the
# single source of protected paths (candidate 4 / #352).
Import-Module (Join-Path $PSScriptRoot 'DomainGate.psm1') -Force

function Emit-Result {
    param(
        [Parameter(Mandatory = $true)][bool]$Ready,
        [Parameter(Mandatory = $true)][string]$Reason
    )

    $verdict = if ($Ready) { 'true' } else { 'false' }
    Write-Host "LOOP_READY=$verdict reason=$Reason"
    if ($Ready) { exit 0 } else { exit 1 }
}

Write-Host "[preflight] supervised-loop preflight starting (Demerzel)"
Write-Host "[preflight] root: $root"

# 1. Risk policy still exists and parses (load-bearing for the oracle).
$riskPolicyFull = Join-Path $root $RiskPolicyPath
if (-not (Test-Path -LiteralPath $riskPolicyFull)) {
    Emit-Result -Ready:$false -Reason "risk_policy_missing"
}
try {
    Get-Content -LiteralPath $riskPolicyFull -Raw | ConvertFrom-Json | Out-Null
} catch {
    Emit-Result -Ready:$false -Reason "risk_policy_invalid_json"
}

# 2. Harness baseline.
$baselineFull = Join-Path $root $BaselinePath
if (-not (Test-Path -LiteralPath $baselineFull)) {
    Emit-Result -Ready:$false -Reason "baseline_missing"
}

# 3. Halt markers (global, domain, HALT-ALL).
if (Test-Path -LiteralPath (Join-Path $root $StopMarkerPath)) {
    Emit-Result -Ready:$false -Reason "stop_marker_present"
}
if (Test-Path -LiteralPath (Join-Path $root $DomainStopPath)) {
    Emit-Result -Ready:$false -Reason "domain_stop_marker_present"
}
if (Test-Path -LiteralPath (Join-Path $root $GlobalHaltMarkerPath)) {
    Emit-Result -Ready:$false -Reason "global_loop_halted"
}
# HALT-ALL: presence + non-expiry = active (no 'active' field). Schema-validated;
# an invalid marker fails safe to active. Single implementation in DomainGate.psm1.
$haltAll = Test-HaltAll -RepoRoot $root -HaltAllPath $HaltAllPath
if ($haltAll.Active) {
    $code = if (-not $haltAll.Valid) { "halt_all_invalid" } else { "halt_all_active" }
    Emit-Result -Ready:$false -Reason $code
}

# 4. Overseer freshness + workflowMode.
$overseerFull = Join-Path $root $OverseerPath
if (-not (Test-Path -LiteralPath $overseerFull)) {
    Emit-Result -Ready:$false -Reason "overseer_missing"
}
try {
    $overseer = Get-Content -LiteralPath $overseerFull -Raw | ConvertFrom-Json
} catch {
    Emit-Result -Ready:$false -Reason "overseer_invalid_json"
}
if ($overseer.workflowMode -ne 'loop-eligible') {
    Emit-Result -Ready:$false -Reason "overseer_workflow_mode_$($overseer.workflowMode)"
}
$emittedAt = [datetime]::Parse($overseer.emittedAt)
$ageHours = ((Get-Date) - $emittedAt).TotalHours
if ($ageHours -gt $OverseerMaxAgeHours) {
    Emit-Result -Ready:$false -Reason "overseer_stale_${ageHours}h"
}

# 5. Worktree must not have edits to protected paths (list lives in DomainGate.psm1).
$protectedDirty = Test-ProtectedDirty -RepoRoot $root
if ($protectedDirty.Count -gt 0) {
    Emit-Result -Ready:$false -Reason "protected_path_dirty_$($protectedDirty[0])"
}

# 6. Rewrite budget (informational; cycle enforces lines_changed).
Write-Host "[preflight] rewrite_budget: max_lines=$MaxLinesPerCycle max_files=$MaxFilesPerCycle"

Write-Host "[preflight] all gates pass"
Emit-Result -Ready:$true -Reason "all_gates_pass"
