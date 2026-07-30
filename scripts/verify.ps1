$ErrorActionPreference = 'Stop'

$root = Split-Path -Parent $PSScriptRoot

Get-ChildItem -LiteralPath $root -Recurse -File -Include *.json |
    Where-Object { $_.FullName -notmatch '\\node_modules\\|\\.git\\' } |
    # -AsHashtable: npm lockfiles legitimately use "" as the root package key.
    # That is valid JSON, but ConvertFrom-Json rejects an empty-string property
    # name unless it deserializes to a hashtable - which made the repo oracle
    # fail on a well-formed file. Parsing is still the check; only the target
    # type changes.
    ForEach-Object { Get-Content -LiteralPath $_.FullName -Raw | ConvertFrom-Json -AsHashtable | Out-Null }

# $ErrorActionPreference = 'Stop' does NOT cover native command exit codes
# ($PSNativeCommandUseErrorActionPreference is False here), so every native
# call below must be checked explicitly or its failure is silently discarded.
function Assert-NativeSuccess([string]$what) {
    if ($LASTEXITCODE -ne 0) {
        throw "$what failed with exit code $LASTEXITCODE"
    }
}

if (Test-Path -LiteralPath (Join-Path $root 'tree-sitter-ixql/package.json')) {
    Push-Location (Join-Path $root 'tree-sitter-ixql')
    try {
        if (Test-Path -LiteralPath 'package-lock.json') {
            npm ci
            Assert-NativeSuccess 'npm ci'
        } else {
            npm install
            Assert-NativeSuccess 'npm install'
        }
        npm test
        Assert-NativeSuccess 'npm test'
    } finally {
        Pop-Location
    }
}

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
# NOTE: this check is NOT wired to CI — no workflow invokes verify.ps1 (#919). It fires
# only when a human or the supervised loop runs this script. Drift has already reached
# master once behind that gap; do not read a passing local run as a CI guarantee.
if (Test-Path -LiteralPath (Join-Path $root 'baml_src')) {
    Push-Location $root
    try {
        npx --yes @boundaryml/baml generate
        Assert-NativeSuccess 'npx @boundaryml/baml generate'

        # `git status --porcelain` reports a file whose only difference is its line
        # endings, so on a Windows checkout (autocrlf) a CORRECT regenerate looks like
        # 7 changed files when exactly 1 changed. Compare content instead: `git diff`
        # applies the same normalisation git would on commit. Verified 2026-07-30 —
        # porcelain said 7, diff said 1, and the 1 was the real change.
        $drift = git diff --name-only -- baml_client
        $untracked = git ls-files --others --exclude-standard -- baml_client
        if ($drift -or $untracked) {
            Write-Host ($drift + $untracked)
            throw "baml_client/ is out of date with baml_src/. Run 'npx --yes @boundaryml/baml generate' and commit the result."
        }
    } finally {
        Pop-Location
    }
}
