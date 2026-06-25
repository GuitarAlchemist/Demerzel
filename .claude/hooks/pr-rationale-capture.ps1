# PostToolUse(matcher=Bash) hook — Enhancement 3 (Cherny PR rationale capture).
# When a Bash invocation runs `gh pr create`, snapshot the title + body + diff
# stats to state/digests/pr-<num>-<slug>.md so the rationale survives later edits.
# Extraction stays here (its real complexity); the write goes through DigestState.

$ErrorActionPreference = 'SilentlyContinue'

$repoRoot = & git rev-parse --show-toplevel 2>$null
if (-not $repoRoot) { exit 0 }

Import-Module (Join-Path $PSScriptRoot 'DigestState.psm1') -Force

# Read PostToolUse JSON payload from stdin: {tool_input: {command}, tool_response: {output}}
$cmd = ''
$output = ''
try {
    $stdinRaw = [Console]::In.ReadToEnd()
    if (-not $stdinRaw) { exit 0 }
    $payload = $stdinRaw | ConvertFrom-Json
    if ($payload.tool_input -and $payload.tool_input.command) { $cmd = $payload.tool_input.command }
    if ($payload.tool_response) {
        if ($payload.tool_response.output) { $output = $payload.tool_response.output }
        elseif ($payload.tool_response -is [string]) { $output = $payload.tool_response }
    }
} catch { exit 0 }

if (-not $cmd) { exit 0 }
if ($cmd -notmatch 'gh\s+pr\s+create') { exit 0 }

# Extract --title "..." or --title '...'
$title = ''
$mTitle = [regex]::Match($cmd, '--title\s+(?:"([^"]*)"|''([^'']*)'')')
if ($mTitle.Success) {
    $title = if ($mTitle.Groups[1].Value) { $mTitle.Groups[1].Value } else { $mTitle.Groups[2].Value }
}

# Extract --body "..." or --body '...' (best-effort — heredoc bodies show as $(cat ...))
$body = ''
$mBody = [regex]::Match($cmd, '--body\s+(?:"([\s\S]*?)"(?=\s|$)|''([\s\S]*?)''(?=\s|$))')
if ($mBody.Success) {
    $body = if ($mBody.Groups[1].Value) { $mBody.Groups[1].Value } else { $mBody.Groups[2].Value }
}

# Extract PR number from gh CLI output URL (https://github.com/x/y/pull/123)
$prNum = 'unknown'
$mPr = [regex]::Match($output, 'pull/(\d+)')
if ($mPr.Success) { $prNum = $mPr.Groups[1].Value }

$shortStat = & git -C $repoRoot diff --shortstat HEAD~1 2>$null
if (-not $shortStat) { $shortStat = '' }

$mdBody = @"
# PR #$prNum — $title

## Title

$title

## Body

$body
"@

$null = Write-Digest -Kind rationale -RepoRoot $repoRoot `
    -PrNumber $prNum -Title $title -DiffShortstat $shortStat -Body $mdBody
exit 0
