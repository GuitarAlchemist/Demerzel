#!/usr/bin/env pwsh
# ADR-0005 §Decision.4 — regenerate the Python BAML client and fail on drift.
#
# `baml_client/` is COMMITTED but derived, so baml_src/ and it can disagree. That only
# stays honest if something diffs them: without this check a `.baml` edit merges with a
# stale client and the typed contract silently stops matching the schema. Same discipline
# as governance-manifest.json.
#
# Scope is `baml_client` only. The Rust and TypeScript trees moved to their consumers on
# 2026-07-30 (ADR-0005 Amendment; CL-817-12) — each consumer generates from the contract
# and diffs its own output.
#
# This lives in its own script, rather than inline in verify.ps1, because it has TWO
# callers: verify.ps1 (human / supervised loop) and the `baml-drift` job in
# governance-validate.yml. Until #919 it had only the first, so the check never ran in CI
# and drift reached master behind the gap. One implementation, two callers — a second copy
# in the workflow would be the next thing to fall out of step with baml_src/.
$ErrorActionPreference = 'Stop'

$root = Split-Path -Parent $PSScriptRoot

if (-not (Test-Path -LiteralPath (Join-Path $root 'baml_src'))) {
    Write-Host 'No baml_src/ — nothing to check.'
    exit 0
}

# $ErrorActionPreference = 'Stop' does NOT cover native command exit codes
# ($PSNativeCommandUseErrorActionPreference is False here), so every native call below
# must be checked explicitly or its failure is silently discarded.
function Assert-NativeSuccess([string]$what) {
    if ($LASTEXITCODE -ne 0) {
        throw "$what failed with exit code $LASTEXITCODE"
    }
}

# Pin the generator to the version baml_src/ declares, rather than floating on
# `@boundaryml/baml` latest. A drift check whose own generator version can change
# underneath it manufactures the drift it is meant to detect: the next BAML release that
# alters codegen output would fail this job on every PR, against a baml_client/ that is
# perfectly in step with its source. Read the pin from baml_project.baml so there is one
# place to bump it. (#919)
$projectFile = Join-Path $root 'baml_src/baml_project.baml'
$version = $null
foreach ($line in Get-Content -LiteralPath $projectFile) {
    $trimmed = $line.Trim()
    if ($trimmed.StartsWith('version ')) {
        $parts = $trimmed.Split('"')
        if ($parts.Count -ge 2) { $version = $parts[1] }
        break
    }
}
if (-not $version) {
    throw "Could not read the generator version from $projectFile. Expected a line like: version `"0.223.0`""
}

Push-Location $root
try {
    Write-Host "Regenerating baml_client/ with @boundaryml/baml@$version"
    npx --yes "@boundaryml/baml@$version" generate
    Assert-NativeSuccess "npx @boundaryml/baml@$version generate"

    # `git status --porcelain` reports a file whose only difference is its line endings,
    # so on a Windows checkout (autocrlf) a CORRECT regenerate looks like 7 changed files
    # when exactly 1 changed. Compare content instead: `git diff` applies the same
    # normalisation git would on commit. Verified 2026-07-30 — porcelain said 7, diff said
    # 1, and the 1 was the real change.
    $drift = git diff --name-only -- baml_client
    $untracked = git ls-files --others --exclude-standard -- baml_client
    if ($drift -or $untracked) {
        Write-Host ($drift + $untracked)
        throw "baml_client/ is out of date with baml_src/. Run 'npx --yes @boundaryml/baml@$version generate' and commit the result."
    }
    Write-Host 'baml_client/ is in step with baml_src/.'
} finally {
    Pop-Location
}
