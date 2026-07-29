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

# ADR-0005 §Decision.4 — regenerate the BAML clients and fail on drift.
#
# The three client trees are COMMITTED (sibling repos copy or reference them, and a
# Rust/TypeScript consumer cannot run `baml generate` as part of its own build), so
# they are derived-but-tracked artifacts. That only stays honest if CI diffs them:
# without this check a `.baml` edit merges with stale clients and the typed contract
# silently stops matching the schema. Same discipline as governance-manifest.json.
if (Test-Path -LiteralPath (Join-Path $root 'baml_src')) {
    Push-Location $root
    try {
        npx --yes @boundaryml/baml generate
        Assert-NativeSuccess 'npx @boundaryml/baml generate'

        $drift = git status --porcelain -- baml_client clients
        if ($drift) {
            Write-Host $drift
            throw "BAML clients are out of date with baml_src/. Run 'npx --yes @boundaryml/baml generate' and commit the result."
        }
    } finally {
        Pop-Location
    }
}
