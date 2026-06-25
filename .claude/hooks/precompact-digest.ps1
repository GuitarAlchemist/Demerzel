# PreCompact hook — archives state/digests/latest.md and writes a metadata-only
# fallback if /digest wasn't invoked before compaction.
# Thin decider over DigestState.psm1 (path resolution, escaping, git facts,
# archive rotation, schema-validated write all live in the module).

$ErrorActionPreference = 'SilentlyContinue'
$WarningPreference     = 'SilentlyContinue'

$repoRoot = & git rev-parse --show-toplevel 2>$null
if (-not $repoRoot) { exit 0 }

Import-Module (Join-Path $PSScriptRoot 'DigestState.psm1') -Force

# Session id from the PreCompact stdin payload (this hook's own concern).
$sessionId = 'unknown'
try {
    $stdinRaw = [Console]::In.ReadToEnd()
    if ($stdinRaw) {
        $payload = $stdinRaw | ConvertFrom-Json
        if ($payload.session_id) { $sessionId = $payload.session_id }
    }
} catch {}
$safeSession = Format-YamlId $sessionId

$paths = Get-DigestPaths -RepoRoot $repoRoot

# If a real /digest ran recently, snapshot it and keep it — do not overwrite.
# (On the stale path below, Write-Digest rotates the prior latest itself.)
if (Test-Path $paths.Latest) {
    $age = (Get-Date) - (Get-Item $paths.Latest).LastWriteTime
    if ($age.TotalMinutes -lt 30) {
        New-Item -ItemType Directory -Path $paths.ArchiveDir -Force | Out-Null
        $tsFile = (Get-Date).ToUniversalTime().ToString('yyyy-MM-ddTHH-mm-ssZ')
        Copy-Item $paths.Latest (Join-Path $paths.ArchiveDir "$tsFile-$safeSession.md") -Force
        exit 0
    }
}

$body = @"
# Session digest (fallback — /digest was not invoked before compaction)

## Model-driven sections

_No ``/digest`` invocation was captured before this compaction. Re-orient from
``git log`` and the open PR. Invoke ``/digest`` mid-session to populate the
**Next action**, **In-flight**, **Live hypotheses**, **Open questions**, and
**Do NOT carry forward** sections before the next compaction event._
"@

$null = Write-Digest -Kind digest -RepoRoot $repoRoot `
    -Trigger 'precompact-hook-fallback' -SessionId $sessionId -ArchiveLabel $safeSession -Body $body
exit 0
