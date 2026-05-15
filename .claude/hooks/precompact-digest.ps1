# PreCompact hook — archives state/digests/latest.md and writes a metadata-only
# fallback if /digest wasn't invoked before compaction.

$ErrorActionPreference = 'SilentlyContinue'
$WarningPreference     = 'SilentlyContinue'

$repoRoot = & git rev-parse --show-toplevel 2>$null
if (-not $repoRoot) { exit 0 }

$digestDir = Join-Path $repoRoot 'state/digests'
$archDir   = Join-Path $digestDir 'archive'
$latest    = Join-Path $digestDir 'latest.md'
New-Item -ItemType Directory -Path $digestDir, $archDir -Force | Out-Null

$sessionId = 'unknown'
try {
    $stdinRaw = [Console]::In.ReadToEnd()
    if ($stdinRaw) {
        $payload = $stdinRaw | ConvertFrom-Json
        if ($payload.session_id) { $sessionId = $payload.session_id }
    }
} catch {}

$ts     = (Get-Date).ToUniversalTime().ToString('yyyy-MM-ddTHH:mm:ssZ')
$tsFile = (Get-Date).ToUniversalTime().ToString('yyyy-MM-ddTHH-mm-ssZ')

if (Test-Path $latest) {
    Copy-Item $latest (Join-Path $archDir "$tsFile-$sessionId.md") -Force
    $age = (Get-Date) - (Get-Item $latest).LastWriteTime
    if ($age.TotalMinutes -lt 30) { exit 0 }
}

$branch   = & git -C $repoRoot rev-parse --abbrev-ref HEAD 2>$null
$headSha  = & git -C $repoRoot rev-parse --short HEAD 2>$null
$headSubj = & git -C $repoRoot log -1 --format='%s' 2>$null

$openPr = $null
if (Get-Command gh -ErrorAction SilentlyContinue) {
    $prJson = & gh pr view --json number 2>$null
    if ($prJson) {
        try { $openPr = "#$(($prJson | ConvertFrom-Json).number)" } catch {}
    }
}
$prLine = if ($openPr) { "**Open PR:** $openPr`n" } else { '' }

$digest = @"
---
schema_version: 1
session_id: $sessionId
written_at: $ts
trigger: precompact-hook-fallback
branch: $branch
head_sha: $headSha
head_subject: $headSubj
open_pr: $openPr
---

# Session digest (fallback — /digest was not invoked before compaction)

**Branch:** $branch @ $headSha — $headSubj
$prLine
## Model-driven sections

_No ``/digest`` invocation was captured before this compaction. Re-orient from
``git log`` and the open PR. Invoke ``/digest`` mid-session to populate the
**Next action**, **In-flight**, **Live hypotheses**, **Open questions**, and
**Do NOT carry forward** sections before the next compaction event._
"@

Set-Content -Path $latest -Value $digest -Encoding UTF8
exit 0
