[CmdletBinding()]
param(
    [switch]$SkipMcp,
    [switch]$SkipHooks
)

$ErrorActionPreference = 'Stop'

$galacticRepoRoot = Split-Path -Parent $PSScriptRoot
$galacticSourceBridgePath = Join-Path $PSScriptRoot 'galactic_bridge.py'
$galacticSourceHookPath = Join-Path $PSScriptRoot 'galactic_hook.py'
$galacticCodexRoot = if ($env:CODEX_HOME) {
    $env:CODEX_HOME
} else {
    Join-Path ([Environment]::GetFolderPath('UserProfile')) '.codex'
}
$galacticHooksPath = Join-Path $galacticCodexRoot 'hooks.json'
$galacticInstallRoot = Join-Path $galacticCodexRoot 'galactic'
$galacticBridgePath = Join-Path $galacticInstallRoot 'galactic_bridge.py'
$galacticHookPath = Join-Path $galacticInstallRoot 'galactic_hook.py'

if (-not (Test-Path -LiteralPath $galacticSourceBridgePath)) {
    throw "Bridge script not found: $galacticSourceBridgePath"
}
if (-not (Test-Path -LiteralPath $galacticSourceHookPath)) {
    throw "Hook script not found: $galacticSourceHookPath"
}

python -m py_compile $galacticSourceBridgePath $galacticSourceHookPath
if ($LASTEXITCODE -ne 0) {
    throw 'Galactic bridge Python preflight failed.'
}

if (-not ($SkipMcp -and $SkipHooks)) {
    New-Item -ItemType Directory -Force -Path $galacticInstallRoot | Out-Null
    Copy-Item -LiteralPath $galacticSourceBridgePath -Destination $galacticBridgePath -Force
    Copy-Item -LiteralPath $galacticSourceHookPath -Destination $galacticHookPath -Force
}

if (-not $SkipMcp) {
    $existingMcp = & codex mcp get galactic --json 2>$null
    if ($LASTEXITCODE -eq 0 -and $existingMcp) {
        & codex mcp remove galactic | Out-Null
        if ($LASTEXITCODE -ne 0) {
            throw 'Could not replace the existing galactic MCP registration.'
        }
    }

    & codex mcp add galactic -- python $galacticBridgePath serve | Out-Null
    if ($LASTEXITCODE -ne 0) {
        throw 'Could not register the galactic MCP server.'
    }
}

if (-not $SkipHooks) {
    New-Item -ItemType Directory -Force -Path $galacticCodexRoot | Out-Null

    if (Test-Path -LiteralPath $galacticHooksPath) {
        $timestamp = Get-Date -Format 'yyyyMMdd-HHmmss'
        $backupPath = Join-Path $galacticCodexRoot "hooks.json.$timestamp.bak"
        Copy-Item -LiteralPath $galacticHooksPath -Destination $backupPath
        $hookDocument = Get-Content -Raw -LiteralPath $galacticHooksPath | ConvertFrom-Json -AsHashtable
    } else {
        $hookDocument = @{
            description = 'User-level Codex lifecycle hooks.'
            hooks = @{}
        }
    }

    if (-not $hookDocument.ContainsKey('hooks') -or $null -eq $hookDocument.hooks) {
        $hookDocument.hooks = @{}
    }

    $events = @('SessionStart', 'UserPromptSubmit', 'PostToolUse')
    foreach ($eventName in $events) {
        $retainedGroups = @()
        if ($hookDocument.hooks.ContainsKey($eventName)) {
            foreach ($group in @($hookDocument.hooks[$eventName])) {
                $retainedHandlers = @()
                foreach ($handler in @($group.hooks)) {
                    $commandText = "$(if ($handler.command) { $handler.command }) $(if ($handler.commandWindows) { $handler.commandWindows })"
                    if ($commandText -notmatch 'galactic_hook\.py') {
                        $retainedHandlers += $handler
                    }
                }
                if ($retainedHandlers.Count -gt 0) {
                    $group.hooks = $retainedHandlers
                    $retainedGroups += $group
                }
            }
        }
        $hookDocument.hooks[$eventName] = $retainedGroups
    }

    $quotedHookPath = '"' + $galacticHookPath + '"'
    $baseHandler = @{
        type = 'command'
        command = "python $quotedHookPath"
        commandWindows = "python $quotedHookPath"
        timeout = 10
        statusMessage = 'Checking Galactic inbox'
    }

    $hookDocument.hooks.SessionStart += @{
        matcher = 'startup|resume|clear|compact'
        hooks = @($baseHandler.Clone())
    }
    $hookDocument.hooks.UserPromptSubmit += @{
        hooks = @($baseHandler.Clone())
    }
    $hookDocument.hooks.PostToolUse += @{
        matcher = 'Bash|apply_patch|Agent|update_plan'
        hooks = @($baseHandler.Clone())
    }

    $serializedHooks = $hookDocument | ConvertTo-Json -Depth 30
    Set-Content -LiteralPath $galacticHooksPath -Value $serializedHooks -Encoding utf8
}

if (-not $SkipMcp) {
    $registered = & codex mcp get galactic --json
    if ($LASTEXITCODE -ne 0 -or -not $registered) {
        throw 'Galactic MCP verification failed.'
    }
}

if (-not $SkipMcp) {
    $probeOutput = & python $galacticBridgePath status
    if ($LASTEXITCODE -ne 0 -or -not $probeOutput) {
        throw 'Galactic runtime ledger probe failed.'
    }
}

Write-Host "Galactic bridge installed from $galacticRepoRoot"
Write-Host "Runtime ledger: $([Environment]::GetEnvironmentVariable('LOCALAPPDATA'))\Demerzel\galactic-protocol"
Write-Host "Shared claims: $([Environment]::GetFolderPath('UserProfile'))\.agents\claims.jsonl"
if (-not $SkipHooks) {
    Write-Host "Hooks: $galacticHooksPath"
    Write-Host 'Open /hooks in Codex to review and trust the new hook hash, then start a new chat.'
}
