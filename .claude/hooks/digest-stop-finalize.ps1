# Stop hook — writes a finalize digest if /digest hasn't run in the last 10 min.
# Karpathy R4: every session boundary is a goal-driven checkpoint.
# Thin decider over DigestState.psm1.

$ErrorActionPreference = 'SilentlyContinue'

$repoRoot = & git rev-parse --show-toplevel 2>$null
if (-not $repoRoot) { exit 0 }

Import-Module (Join-Path $PSScriptRoot 'DigestState.psm1') -Force

$latest = (Get-DigestPaths -RepoRoot $repoRoot).Latest
if (Test-Path $latest) {
    $age = (Get-Date) - (Get-Item $latest).LastWriteTime
    if ($age.TotalMinutes -lt 10) { exit 0 }
}

$facts = Get-RepoFacts -RepoRoot $repoRoot
$prLine = if ($facts.OpenPr) { "**Open PR:** $($facts.OpenPr)`n" } else { '' }

$body = @"
# Session digest (Stop-hook finalize — /digest not invoked in last 10 min)

**Branch:** $($facts.Branch) @ $($facts.HeadSha) — $($facts.HeadSubject)
$prLine
## Model-driven sections

_Session ended without a recent ``/digest``. Next session: re-orient from
``git log`` + open PR. Prior digests (if any) are in ``state/digests/archive/``._
"@

$null = Write-Digest -Kind digest -RepoRoot $repoRoot -RepoFacts $facts `
    -Trigger 'stop-hook-finalize' -SessionId 'stop-finalize' -ArchiveLabel 'stop' -Body $body
exit 0
