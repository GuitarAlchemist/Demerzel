# Validates a digest/rationale file's frontmatter against its schema.
# Thin wrapper over DigestState's Test-Digest — the rules (required fields,
# trigger enum, types) come from docs/contracts/*-schema.json, not hand-coded
# here (ADR-0003: schema is the single source of structural validation).

param([string]$DigestPath)

$ErrorActionPreference = 'SilentlyContinue'

$repoRoot = & git rev-parse --show-toplevel 2>$null
if (-not $repoRoot) { exit 0 }

Import-Module (Join-Path $PSScriptRoot 'DigestState.psm1') -Force

if (-not $DigestPath) {
    $DigestPath = (Get-DigestPaths -RepoRoot $repoRoot).Latest
}
if (-not (Test-Path $DigestPath)) { exit 0 }

$result = Test-Digest -Path $DigestPath -RepoRoot $repoRoot
if (-not $result.Valid) {
    Write-Error "digest-validate: $($result.Errors)"
    exit 1
}
exit 0
