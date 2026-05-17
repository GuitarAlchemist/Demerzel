$ErrorActionPreference = 'Stop'

$root = Split-Path -Parent $PSScriptRoot

Get-ChildItem -LiteralPath $root -Recurse -File -Include *.json |
    Where-Object { $_.FullName -notmatch '\\node_modules\\|\\.git\\' } |
    ForEach-Object { Get-Content -LiteralPath $_.FullName -Raw | ConvertFrom-Json | Out-Null }

if (Test-Path -LiteralPath (Join-Path $root 'tree-sitter-ixql/package.json')) {
    Push-Location (Join-Path $root 'tree-sitter-ixql')
    try {
        if (Test-Path -LiteralPath 'package-lock.json') {
            npm ci
        } else {
            npm install
        }
        npm test
    } finally {
        Pop-Location
    }
}
