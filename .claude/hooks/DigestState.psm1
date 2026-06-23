# DigestState.psm1 — the deep module behind the session-digest hooks
# (Candidate 1, /improve-codebase-architecture 2026-06-21).
#
# Mirrors scripts/DomainGate.psm1 (#352): the eight digest hooks used to each
# re-derive the same primitives — the state/digests path, YAML escaping, git
# facts, counter I/O, and a late-bound validation call. Those all live here now,
# once. Hooks become thin DECIDERS ("is it stale?  then call Write-Digest").
#
# Interface (small): Get-DigestPaths / Format-Yaml / Format-YamlId /
# Get-RepoFacts / Get-Counter / Step-Counter / Reset-Counter / Test-Digest /
# Write-Digest. Everything else is implementation.
#
# Validation seam (ADR-0003): Write-Digest validates the OBJECT it constructs
# (hashtable -> ConvertTo-Json -> Test-Json -SchemaFile) so the rules come from
# the schema, not hand-coded here. Test-Digest does the same for an existing
# file's top-level scalars. Pure PowerShell has no YAML parser, so deep nested
# validation (success_criteria items) stays in the CI Python gate; the write
# path validates the full object because we build it typed in memory.

Set-StrictMode -Off

# Counter logical-name -> on-disk filename. Names kept for back-compat so an
# in-flight session's existing counters are not orphaned.
$script:CounterFiles = @{
    activity   = '.activity-counter'   # staleness nudge
    mid        = '.activity-count'     # mid-session auto-digest gate
    correction = '.correction-counter' # /correct throttle
}

# Kind -> schema file (relative to repo root).
$script:SchemaFiles = @{
    digest    = 'docs/contracts/digest-schema.json'
    rationale = 'docs/contracts/pr-rationale-schema.json'
}

function Resolve-RepoRoot {
    param([string]$RepoRoot)
    if ($RepoRoot) { return $RepoRoot }
    $top = & git rev-parse --show-toplevel 2>$null
    if ($top) { return $top }
    # Fallback: module lives in <root>/.claude/hooks
    Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
}

function Get-DigestPaths {
    # The single home for every session-digest path. Callers ask here instead of
    # joining 'state/digests' themselves.
    param([string]$RepoRoot)
    $root = Resolve-RepoRoot $RepoRoot
    $dir  = Join-Path $root 'state/digests'
    [pscustomobject]@{
        RepoRoot          = $root
        DigestDir         = $dir
        ArchiveDir        = Join-Path $dir 'archive'
        Latest            = Join-Path $dir 'latest.md'
        ActivityCounter   = Join-Path $dir $script:CounterFiles.activity
        MidCounter        = Join-Path $dir $script:CounterFiles.mid
        CorrectionCounter = Join-Path $dir $script:CounterFiles.correction
    }
}

function Format-Yaml {
    # Single-line, length-capped, single-quote-escaped YAML scalar (was the
    # copy-pasted Get-SafeYaml). Returns the literal 'null' for empty input.
    param([string]$Value, [int]$MaxLen = 200)
    if ($null -eq $Value -or $Value -eq '') { return 'null' }
    $cleaned = ($Value -replace '[\r\n]', ' ')
    if ($cleaned.Length -gt $MaxLen) { $cleaned = $cleaned.Substring(0, $MaxLen) + '...' }
    "'$($cleaned -replace "'", "''")'"
}

function Format-YamlId {
    # Filename-safe identifier (was the copy-pasted Get-SafeId).
    param([string]$Value, [string]$Fallback = 'unknown', [int]$MaxLen = 64)
    if (-not $Value) { return $Fallback }
    $cleaned = $Value -replace '[\r\n\t]', ''
    if ($cleaned.Length -gt $MaxLen) { $cleaned = $cleaned.Substring(0, $MaxLen) }
    if ($cleaned -match '^[A-Za-z0-9._\-]+$') { return $cleaned }
    $Fallback
}

function Get-RepoFacts {
    # The git/gh facts every writer needs, fetched once. Tests inject these
    # instead (Write-Digest -RepoFacts @{...}) so they never shell out.
    param([string]$RepoRoot)
    $root = Resolve-RepoRoot $RepoRoot
    $openPr = $null
    if (Get-Command gh -ErrorAction SilentlyContinue) {
        $prJson = & gh pr view --json number 2>$null
        if ($prJson) { try { $openPr = "#$(($prJson | ConvertFrom-Json).number)" } catch {} }
    }
    [pscustomobject]@{
        Branch      = (& git -C $root rev-parse --abbrev-ref HEAD 2>$null)
        HeadSha     = (& git -C $root rev-parse --short HEAD 2>$null)
        HeadSubject = (& git -C $root log -1 --format='%s' 2>$null)
        OpenPr      = $openPr
    }
}

function Resolve-CounterPath {
    param([Parameter(Mandatory)][string]$Name, [string]$RepoRoot)
    if (-not $script:CounterFiles.ContainsKey($Name)) {
        throw "Unknown counter '$Name' (expected: $($script:CounterFiles.Keys -join ', '))"
    }
    Join-Path (Get-DigestPaths -RepoRoot $RepoRoot).DigestDir $script:CounterFiles[$Name]
}

function Get-Counter {
    param([Parameter(Mandatory)][string]$Name, [string]$RepoRoot)
    $path = Resolve-CounterPath -Name $Name -RepoRoot $RepoRoot
    if (Test-Path $path) {
        $raw = (Get-Content $path -Raw).Trim()
        if ($raw -match '^\d+$') { return [int]$raw }
    }
    0
}

function Step-Counter {
    # Increment, persist, return the new value.
    param([Parameter(Mandatory)][string]$Name, [string]$RepoRoot)
    $path = Resolve-CounterPath -Name $Name -RepoRoot $RepoRoot
    New-Item -ItemType Directory -Path (Split-Path -Parent $path) -Force | Out-Null
    $next = (Get-Counter -Name $Name -RepoRoot $RepoRoot) + 1
    Set-Content -Path $path -Value $next -Encoding UTF8
    $next
}

function Reset-Counter {
    param([Parameter(Mandatory)][string]$Name, [string]$RepoRoot)
    $path = Resolve-CounterPath -Name $Name -RepoRoot $RepoRoot
    if (Test-Path $path) { Set-Content -Path $path -Value 0 -Encoding UTF8 }
}

function ConvertTo-FrontmatterYaml {
    # Render an [ordered] field map to YAML frontmatter lines. Handles the only
    # nested shape we emit: success_criteria (array of {criterion,status,evidence}).
    param([Parameter(Mandatory)][System.Collections.Specialized.OrderedDictionary]$Fields)
    $lines = @('---')
    foreach ($entry in $Fields.GetEnumerator()) {
        $k = $entry.Key; $v = $entry.Value
        if ($k -eq 'success_criteria') {
            $lines += 'success_criteria:'
            foreach ($c in $v) {
                $lines += "  - criterion: $(Format-Yaml ([string]$c.criterion) 300)"
                $lines += "    status: $([string]$c.status)"
                $ev = if ($null -ne $c.evidence) { Format-Yaml ([string]$c.evidence) 300 } else { 'null' }
                $lines += "    evidence: $ev"
            }
            continue
        }
        if ($null -eq $v) { $lines += "${k}: null"; continue }
        if ($v -is [int]) { $lines += "${k}: $v"; continue }
        $s = [string]$v
        # Distinguish an empty string (valid string scalar) from $null above —
        # Format-Yaml maps '' to the literal null, which would re-parse as null.
        if ($s -eq '') { $lines += "${k}: ''"; continue }
        $lines += "${k}: $(Format-Yaml $s)"
    }
    $lines += '---'
    $lines -join "`n"
}

function Test-SchemaObject {
    # Validate an in-memory field map against a Kind's schema. Returns
    # {Valid,Errors}. The rules live in the schema (ADR-0003), not here.
    param(
        [Parameter(Mandatory)]$Fields,
        [Parameter(Mandatory)][string]$Kind,
        [Parameter(Mandatory)][string]$RepoRoot
    )
    $schemaFile = Join-Path $RepoRoot $script:SchemaFiles[$Kind]
    if (-not (Test-Path $schemaFile)) {
        return [pscustomobject]@{ Valid = $false; Errors = "schema not found: $schemaFile" }
    }
    $json = $Fields | ConvertTo-Json -Depth 6
    try {
        # Test-Json signals schema failure two ways: a $false return AND/OR a
        # non-terminating error. -ErrorAction Stop promotes the error to a throw,
        # but some mismatches only flip the boolean — so honor BOTH. The discarded
        # boolean was reporting bad digests as Valid=$true (octo review finding).
        $ok = Test-Json -Json $json -SchemaFile $schemaFile -ErrorAction Stop
        if ($ok) {
            [pscustomobject]@{ Valid = $true; Errors = $null }
        } else {
            [pscustomobject]@{ Valid = $false; Errors = 'schema validation failed (Test-Json returned $false)' }
        }
    } catch {
        [pscustomobject]@{ Valid = $false; Errors = $_.Exception.Message }
    }
}

function Test-Digest {
    # Validate an existing digest/rationale file's top-level scalars against its
    # schema. Replaces digest-validate.ps1's hand-coded rules (Candidate 4 digest
    # half). Deep nested fields (success_criteria items) are validated by CI.
    param([Parameter(Mandatory)][string]$Path, [string]$RepoRoot, [string]$Kind)
    $root = Resolve-RepoRoot $RepoRoot
    if (-not (Test-Path $Path)) {
        return [pscustomobject]@{ Valid = $false; Errors = "file not found: $Path" }
    }
    if (-not $Kind) {
        $Kind = if ((Split-Path -Leaf $Path) -like 'pr-*') { 'rationale' } else { 'digest' }
    }
    $content = Get-Content $Path -Raw
    if ($content -notmatch '(?s)^---\r?\n(.*?)\r?\n---') {
        return [pscustomobject]@{ Valid = $false; Errors = "missing or malformed YAML frontmatter in $Path" }
    }
    $fields = [ordered]@{}
    foreach ($line in ($matches[1] -split "`r?`n")) {
        # Top-level, non-empty scalars only (leading-space/container lines skipped).
        if ($line -match '^([\w_]+):[ \t]+(\S.*?)[ \t]*$') {
            $key = $matches[1]; $val = $matches[2]
            if ($val -match "^'(.*)'$") { $val = ($matches[1] -replace "''", "'") }
            if ($val -eq 'null') { $fields[$key] = $null }
            elseif ($key -in @('schema_version', 'mutations_since_last') -and $val -match '^\d+$') { $fields[$key] = [int]$val }
            else { $fields[$key] = $val }
        }
    }
    Test-SchemaObject -Fields $fields -Kind $Kind -RepoRoot $root
}

function Write-Digest {
    # The composite verb. Resolves paths, fetches repo facts (or takes injected
    # ones), escapes values, rotates latest->archive (digest kind), validates the
    # constructed object against the schema, writes, and auto-resets counters by
    # trigger. Fail-open: the file is always written (session continuity beats a
    # validation quirk); the returned result carries Valid/Errors.
    [CmdletBinding()]
    param(
        [Parameter(Mandatory)][ValidateSet('digest', 'rationale')][string]$Kind,
        [string]$RepoRoot,
        $RepoFacts,
        [string]$Body,
        [string]$BodyFile,
        # digest kind
        [string]$Trigger = 'auto-write-routine',
        [string]$SessionId,
        [string]$OpenPr,
        [Nullable[int]]$MutationsSinceLast,
        [string]$LastModelUpdate,
        [string]$SuccessCriteriaJson,
        [string]$ArchiveLabel,
        # rationale kind
        [string]$PrNumber,
        [string]$Title,
        [string]$DiffShortstat
    )

    $paths = Get-DigestPaths -RepoRoot $RepoRoot
    $root  = $paths.RepoRoot
    New-Item -ItemType Directory -Path $paths.DigestDir, $paths.ArchiveDir -Force | Out-Null

    if (-not $RepoFacts) { $RepoFacts = Get-RepoFacts -RepoRoot $root }
    if ($BodyFile) {
        # A caller that passed -BodyFile but whose path does not resolve (e.g. a
        # relative path from a non-root working dir) must fail loudly — silently
        # proceeding would overwrite the digest with an empty body. Fail-open
        # covers validation quirks, NOT a missing input file (octo review finding).
        if (-not (Test-Path $BodyFile)) {
            throw "BodyFile not found: $BodyFile (cwd: $((Get-Location).Path)). Refusing to write a digest with an empty body."
        }
        $Body = Get-Content $BodyFile -Raw
    }

    $tsIso  = (Get-Date).ToUniversalTime().ToString('yyyy-MM-ddTHH:mm:ssZ')
    $tsFile = (Get-Date).ToUniversalTime().ToString('yyyy-MM-ddTHH-mm-ssZ')

    $fields = [ordered]@{}
    if ($Kind -eq 'digest') {
        $fields['schema_version'] = 1
        $fields['session_id']     = if ($SessionId) { $SessionId } else { 'unknown' }
        $fields['written_at']     = $tsIso
        $fields['trigger']        = $Trigger
        $fields['branch']         = [string]$RepoFacts.Branch
        $fields['head_sha']       = [string]$RepoFacts.HeadSha
        $fields['head_subject']   = [string]$RepoFacts.HeadSubject
        if ($OpenPr) { $fields['open_pr'] = $OpenPr } elseif ($RepoFacts.OpenPr) { $fields['open_pr'] = [string]$RepoFacts.OpenPr } else { $fields['open_pr'] = $null }
        if ($LastModelUpdate) { $fields['last_model_update'] = $LastModelUpdate }
        if ($null -ne $MutationsSinceLast) { $fields['mutations_since_last'] = [int]$MutationsSinceLast }
        if ($SuccessCriteriaJson) {
            # Surface parse failures instead of swallowing them — an empty catch
            # silently dropped the whole success_criteria block on any quoting slip
            # (octo review finding). Fail-open: warn but still write the digest.
            try { $fields['success_criteria'] = @($SuccessCriteriaJson | ConvertFrom-Json) }
            catch { Write-Warning "success_criteria JSON invalid — block dropped: $($_.Exception.Message)" }
        }
        $target = $paths.Latest
        if (Test-Path $target) {
            $label = if ($ArchiveLabel) { Format-YamlId $ArchiveLabel } else { Format-YamlId $Trigger }
            Copy-Item $target (Join-Path $paths.ArchiveDir "$tsFile-$label.md") -Force
        }
    }
    else {
        $slug = ($Title.ToLowerInvariant() -replace '[^a-z0-9]+', '-').Trim('-')
        if ($slug.Length -gt 40) { $slug = $slug.Substring(0, 40).Trim('-') }
        if (-not $slug) { $slug = 'untitled' }
        $fields['schema_version'] = 1
        $fields['trigger']        = 'pr-rationale-capture'
        $fields['captured_at']    = $tsIso
        $fields['branch']         = [string]$RepoFacts.Branch
        $fields['pr_number']      = if ($PrNumber) { [string]$PrNumber } else { 'unknown' }
        $fields['diff_shortstat'] = [string]$DiffShortstat
        $target = Join-Path $paths.DigestDir "pr-$($fields['pr_number'])-$slug.md"
    }

    $check = Test-SchemaObject -Fields $fields -Kind $Kind -RepoRoot $root

    $frontmatter = ConvertTo-FrontmatterYaml -Fields $fields
    $bodyText = if ($Body) { $Body.TrimStart("`r", "`n") } else { '' }
    Set-Content -Path $target -Value "$frontmatter`n`n$bodyText" -Encoding UTF8

    if (-not $check.Valid) {
        Write-Warning "Write-Digest: schema validation failed for $target — $($check.Errors)"
    }

    # Auto-reset counters by trigger (digest kind only).
    if ($Kind -eq 'digest') {
        switch ($Trigger) {
            'digest-skill'                 { Reset-Counter -Name activity -RepoRoot $root; Reset-Counter -Name mid -RepoRoot $root }
            'activity-tracker-mid-session' { Reset-Counter -Name mid -RepoRoot $root }
        }
    }

    [pscustomobject]@{ Path = $target; Valid = $check.Valid; Errors = $check.Errors; Written = $true }
}

Export-ModuleMember -Function Get-DigestPaths, Format-Yaml, Format-YamlId, Get-RepoFacts,
    Get-Counter, Step-Counter, Reset-Counter, Test-Digest, Write-Digest
