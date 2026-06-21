# PostToolUse hook (matcher: Edit|Write|Bash) — increments mutation counters and
# writes a mid-session digest when an activity/time threshold is hit, so we
# survive crashes/network drops without waiting for Stop or PreCompact (Cherny).
# Thin decider over DigestState.psm1 (counters, git facts, validated write, and
# the mid-counter reset all live in the module).

$ErrorActionPreference = 'SilentlyContinue'

$repoRoot = & git rev-parse --show-toplevel 2>$null
if (-not $repoRoot) { exit 0 }

Import-Module (Join-Path $PSScriptRoot 'DigestState.psm1') -Force

# Staleness-nudge counter (reset only by a real /digest) + mid-session gate counter.
$null     = Step-Counter -Name activity -RepoRoot $repoRoot
$midCount = Step-Counter -Name mid -RepoRoot $repoRoot

# Thresholds: N=20 mutations OR M=30 minutes since last digest (with >=3 mutations).
$thresholdCount = 20
$thresholdMin   = 30
if ($env:DEMERZEL_DIGEST_MID_COUNT -and $env:DEMERZEL_DIGEST_MID_COUNT -match '^\d+$') { $thresholdCount = [int]$env:DEMERZEL_DIGEST_MID_COUNT }
if ($env:DEMERZEL_DIGEST_MID_MIN   -and $env:DEMERZEL_DIGEST_MID_MIN   -match '^\d+$') { $thresholdMin   = [int]$env:DEMERZEL_DIGEST_MID_MIN }

$latest = (Get-DigestPaths -RepoRoot $repoRoot).Latest
$ageMin = 99999
if (Test-Path $latest) { $ageMin = [int]((Get-Date) - (Get-Item $latest).LastWriteTime).TotalMinutes }

$shouldWrite = ($midCount -ge $thresholdCount) -or ($ageMin -ge $thresholdMin -and $midCount -ge 3)
if (-not $shouldWrite) { exit 0 }

$body = @"
# Session digest (mid-session auto — activity threshold reached)

## Model-driven sections

_Auto-written by digest-activity-tracker after $midCount mutations / ${ageMin}m since last digest.
Invoke ``/digest`` at your next natural breakpoint to populate **Next action**,
**In-flight**, **Live hypotheses**, **Open questions**, **Do NOT carry forward**,
and **Success criteria**._
"@

# Write-Digest rotates the prior latest and resets the mid counter on this trigger.
$null = Write-Digest -Kind digest -RepoRoot $repoRoot `
    -Trigger 'activity-tracker-mid-session' -SessionId 'mid-session-auto' `
    -MutationsSinceLast $midCount -ArchiveLabel 'pre-mid' -Body $body
exit 0
