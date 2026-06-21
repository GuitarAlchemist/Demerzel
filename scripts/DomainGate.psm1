# DomainGate.psm1 — shared domain-gate facts (candidate 4, issue #352).
#
# Reads loop/halt state ONCE and returns FACTS; callers (dev-process-overseer.ps1,
# supervised-loop-preflight.ps1) decide their own verdict. The protected-paths
# list, the HALT-ALL read, its schema validation (Test-Json against the single
# source schemas/halt-all.schema.json — ADR-0003), and the expiry check all live
# here, in one place, instead of being re-coded per gate script.

$script:ProtectedPaths = @('policies/', 'constitutions/', 'personas/', '.github/workflows/')

function Get-ProtectedPaths {
    # The single source of which paths a loop must not touch.
    $script:ProtectedPaths
}

function Test-HaltAll {
    # Returns the HALT-ALL facts. Halt is ACTIVE iff the marker exists and has not
    # expired (there is no 'active' field). An unreadable/invalid marker fails safe
    # to Active = $true.
    param(
        [Parameter(Mandatory)][string]$RepoRoot,
        [string]$HaltAllPath = (Join-Path $HOME '.demerzel/HALT-ALL')
    )
    if (-not (Test-Path -LiteralPath $HaltAllPath)) {
        return [pscustomobject]@{ Present = $false; Valid = $true; Active = $false; Reason = $null; Errors = $null; Marker = $null }
    }

    $raw = Get-Content -LiteralPath $HaltAllPath -Raw
    $schemaFile = Join-Path $RepoRoot 'schemas/halt-all.schema.json'
    $valid = $true
    $errors = $null
    try {
        $null = Test-Json -Json $raw -SchemaFile $schemaFile -ErrorAction Stop
    } catch {
        $valid = $false
        $errors = $_.Exception.Message
    }
    if (-not $valid) {
        return [pscustomobject]@{ Present = $true; Valid = $false; Active = $true; Reason = 'halt_all_invalid'; Errors = $errors; Marker = $null }
    }

    $marker = $raw | ConvertFrom-Json
    $active = $true
    if ($marker.expires_at) {
        try {
            $exp = [datetimeoffset]::Parse($marker.expires_at).UtcDateTime
            if ([datetime]::UtcNow -gt $exp) { $active = $false }
        } catch {
            # Unparseable expiry: keep Active = $true (fail safe).
        }
    }
    return [pscustomobject]@{ Present = $true; Valid = $true; Active = $active; Reason = $marker.reason; Errors = $null; Marker = $marker }
}

function Test-ProtectedDirty {
    # Returns the protected path-prefixes that have uncommitted edits (empty = clean).
    param([Parameter(Mandatory)][string]$RepoRoot)
    $dirty = (git -C $RepoRoot status --porcelain=v1 2>$null) -split "`n" | Where-Object { $_ -ne '' }
    $hits = foreach ($line in $dirty) {
        $path = ($line -replace '^...').Trim()
        foreach ($pat in $script:ProtectedPaths) {
            if ($path -like "$pat*") { $pat }
        }
    }
    @($hits | Select-Object -Unique)
}

function Get-DomainGateState {
    # The deep read: gather all loop-gate facts for a domain in one call.
    param(
        [string]$RepoRoot = (Split-Path -Parent $PSScriptRoot),
        [string]$Domain = 'demerzel-harness',
        [string]$HaltAllPath = (Join-Path $HOME '.demerzel/HALT-ALL')
    )
    [pscustomobject]@{
        Domain           = $Domain
        HaltAll          = (Test-HaltAll -RepoRoot $RepoRoot -HaltAllPath $HaltAllPath)
        ProtectedDirty   = (Test-ProtectedDirty -RepoRoot $RepoRoot)
        StopMarker       = (Test-Path -LiteralPath (Join-Path $RepoRoot '.STOP'))
        DomainStopMarker = (Test-Path -LiteralPath (Join-Path $RepoRoot "state/quality/$Domain/.STOP"))
        GlobalHalt       = (Test-Path -LiteralPath (Join-Path $RepoRoot 'state/.loop-halted'))
    }
}

Export-ModuleMember -Function Get-DomainGateState, Get-ProtectedPaths, Test-HaltAll, Test-ProtectedDirty
