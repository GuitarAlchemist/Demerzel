# UserPromptSubmit hook — emits an additionalContext nudge when state has drifted
# from the last /digest. Karpathy R1+R4. Silent when digest is fresh.
# Thin decider over DigestState.psm1 (latest path + activity counter).

$ErrorActionPreference = 'SilentlyContinue'

$repoRoot = & git rev-parse --show-toplevel 2>$null
if (-not $repoRoot) { exit 0 }

Import-Module (Join-Path $PSScriptRoot 'DigestState.psm1') -Force

$latest = (Get-DigestPaths -RepoRoot $repoRoot).Latest

$digestAgeMin = $null
if (Test-Path $latest) {
    $digestAgeMin = [int]((Get-Date) - (Get-Item $latest).LastWriteTime).TotalMinutes
}

$mutationCount = Get-Counter -Name activity -RepoRoot $repoRoot

$shouldNudge = $false
$reason = ''
if ($null -eq $digestAgeMin) {
    $shouldNudge = $true
    $reason = "No session digest exists yet. Invoke /digest at your next natural breakpoint."
} elseif ($digestAgeMin -gt 30 -and $mutationCount -gt 10) {
    $shouldNudge = $true
    $reason = "Last digest $digestAgeMin min ago; $mutationCount mutations since. Karpathy R4: task complete != goal achieved — consider /digest to mark success criteria status."
} elseif ($digestAgeMin -gt 90) {
    $shouldNudge = $true
    $reason = "Last digest $digestAgeMin min ago. Session drifting — invoke /digest before the next compaction."
}

if (-not $shouldNudge) { exit 0 }

$payload = @{ additionalContext = "[digest-nudge] $reason" } | ConvertTo-Json -Compress
Write-Output $payload
exit 0
