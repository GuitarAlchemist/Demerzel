[CmdletBinding()]
param(
    [string]$Threshold = "40",
    [string]$ClaudeDirectory = (Join-Path ([Environment]::GetFolderPath("UserProfile")) ".claude")
)

$ErrorActionPreference = "Stop"
$hookSource = Join-Path $PSScriptRoot "claude_compaction_hook.py"
$querySource = Join-Path $PSScriptRoot "query_compaction_telemetry.py"
$hookDirectory = Join-Path $ClaudeDirectory "hooks"
$hookTarget = Join-Path $hookDirectory "fleet_compaction_hook.py"
$queryTarget = Join-Path $hookDirectory "query_compaction_telemetry.py"
$settingsPath = Join-Path $ClaudeDirectory "settings.json"

if (-not (Test-Path -LiteralPath $hookSource)) {
    throw "Hook source not found: $hookSource"
}

New-Item -ItemType Directory -Path $hookDirectory -Force | Out-Null
Copy-Item -LiteralPath $hookSource -Destination $hookTarget -Force
Copy-Item -LiteralPath $querySource -Destination $queryTarget -Force

if (Test-Path -LiteralPath $settingsPath) {
    $settings = Get-Content -LiteralPath $settingsPath -Raw | ConvertFrom-Json
    $stamp = Get-Date -Format "yyyyMMdd-HHmmss"
    Copy-Item -LiteralPath $settingsPath -Destination "$settingsPath.pre-fleet-compact-$stamp.bak" -Force
} else {
    $settings = [pscustomobject]@{}
}

if (-not $settings.PSObject.Properties["env"]) {
    $settings | Add-Member -NotePropertyName env -NotePropertyValue ([pscustomobject]@{})
}
$settings.env | Add-Member -NotePropertyName CLAUDE_AUTOCOMPACT_PCT_OVERRIDE -NotePropertyValue $Threshold -Force
$settings.env.PSObject.Properties.Remove("CLAUDE_CODE_AUTOCOMPACT_PCT_OVERRIDE")

if (-not $settings.PSObject.Properties["hooks"]) {
    $settings | Add-Member -NotePropertyName hooks -NotePropertyValue ([pscustomobject]@{})
}

$escapedHook = $hookTarget.Replace("\", "/")
$command = "python `"$escapedHook`""

function Add-FleetHook {
    param(
        [Parameter(Mandatory)][string]$EventName,
        [Parameter(Mandatory)][string]$Matcher
    )

    $entry = [pscustomobject]@{
        matcher = $Matcher
        hooks = @(
            [pscustomobject]@{
                type = "command"
                command = $command
                timeout = 10
            }
        )
    }
    $property = $settings.hooks.PSObject.Properties[$EventName]
    $current = if ($property) { @($property.Value) } else { @() }
    $current = @($current | Where-Object {
        $commands = @($_.hooks | ForEach-Object { $_.command })
        $commands -notcontains $command
    })
    $settings.hooks | Add-Member -NotePropertyName $EventName -NotePropertyValue @($current + $entry) -Force
}

Add-FleetHook -EventName "PreCompact" -Matcher "auto|manual"
Add-FleetHook -EventName "PostCompact" -Matcher "auto|manual"
Add-FleetHook -EventName "SessionStart" -Matcher "compact"

$settings | ConvertTo-Json -Depth 100 | Set-Content -LiteralPath $settingsPath -Encoding utf8
Get-Content -LiteralPath $settingsPath -Raw | ConvertFrom-Json | Out-Null

$smokeLog = Join-Path $hookDirectory "fleet_compaction_smoke.jsonl"
$smokeLock = "$smokeLog.lock"
Remove-Item -LiteralPath $smokeLog, $smokeLock -Force -ErrorAction SilentlyContinue
$previousLog = [Environment]::GetEnvironmentVariable("CLAUDE_FLEET_COMPACTION_LOG", "Process")
try {
    [Environment]::SetEnvironmentVariable("CLAUDE_FLEET_COMPACTION_LOG", $smokeLog, "Process")
    $payload = [pscustomobject]@{
        hook_event_name = "PostCompact"
        session_id = "fleet-install-smoke"
        cwd = $PSScriptRoot
        trigger = "manual"
        transcript_path = "private-smoke-transcript"
        compact_summary = "private smoke summary"
    } | ConvertTo-Json -Compress
    $payload | & python $hookTarget
    if ($LASTEXITCODE -ne 0 -or -not (Test-Path -LiteralPath $smokeLog)) {
        throw "Installed hook smoke test failed"
    }
    $smokeMetrics = & python $queryTarget --log-path $smokeLog | ConvertFrom-Json
    if ($LASTEXITCODE -ne 0 -or @($smokeMetrics).Count -ne 1) {
        throw "Installed DuckDB telemetry query smoke test failed"
    }
} finally {
    [Environment]::SetEnvironmentVariable("CLAUDE_FLEET_COMPACTION_LOG", $previousLog, "Process")
    Remove-Item -LiteralPath $smokeLog, $smokeLock -Force -ErrorAction SilentlyContinue
}

[pscustomobject]@{
    settings = $settingsPath
    hook = $hookTarget
    query = $queryTarget
    threshold = $Threshold
    events = @("PreCompact", "PostCompact", "SessionStart:compact")
    smoke_test = "passed"
} | ConvertTo-Json -Depth 4
