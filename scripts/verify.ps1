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

if (-not (Get-Command python -ErrorAction SilentlyContinue)) {
    throw 'python is required to run the repository test suite'
}

Push-Location $root
try {
    python -m unittest discover -s scripts -p 'test_*.py'
    Assert-NativeSuccess 'python unit tests'
} finally {
    Pop-Location
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

# ADR-0005 §Decision.4 — the BAML client drift check. The logic lives in its own script
# because CI invokes it too (the `baml-drift` job in governance-validate.yml); until #919
# this was inline here and nothing in CI ran it, so drift reached master unnoticed.
#
# No Assert-NativeSuccess here: that helper reads $LASTEXITCODE, which a .ps1 invoked with
# `&` does not set — it would still hold the exit code of the last NATIVE call above
# (npm test), and pass or fail on the wrong thing. The child throws on drift and
# $ErrorActionPreference = 'Stop' propagates it, which is the check.
& (Join-Path $PSScriptRoot 'check_baml_drift.ps1')
