# PreToolUse guard — enforces Demerzel's two deterministic prohibitions.
#
# Rules that CAN be enforced should not merely be stated in CLAUDE.md: prose only
# lowers the probability of a violation while spending instruction budget, whereas
# a hook prevents it. This replaces the prose rules `no-runtime-code.md` and the
# push half of `commit-style.md` (removed 2026-07-19).
#
# Contract: Claude Code pipes a JSON event on stdin. Exit 0 allows the call;
# exit 2 BLOCKS it and feeds stderr back to the model, which then self-corrects.
# Fail OPEN on any internal error - a broken guard must never wedge the session.

$ErrorActionPreference = 'Stop'

function Deny([string]$message) {
    [Console]::Error.WriteLine($message)
    exit 2
}

try {
    $raw = [Console]::In.ReadToEnd()
    if ([string]::IsNullOrWhiteSpace($raw)) { exit 0 }
    $evt = $raw | ConvertFrom-Json

    # NB: do not name these $input / $event - both are PowerShell automatic
    # variables, and assigning to them silently yields an empty value.
    $tool = [string]$evt.tool_name
    $toolInput = $evt.tool_input

    # --- Rule 1: never push to the default branch -------------------------------
    # Worktree branches are cut from master, so an unqualified `git push` can land
    # commits directly on it. Require an explicit branch and a PR.
    if ($tool -eq 'Bash') {
        $cmd = [string]$toolInput.command
        if ($cmd -and $cmd -match 'git\s+push') {
            $isDefault = $cmd -match 'git\s+push\s+\S+\s+(HEAD:)?(master|main)\b' -or
                         $cmd -match 'git\s+push\s+(--force\S*\s+)?(origin\s+)?(master|main)\b'

            # A bare `git push` names no branch, so it targets whatever is checked
            # out - the exact way commits land on master by accident. Resolve the
            # current branch and block only if it really is the default one.
            if (-not $isDefault -and $cmd -notmatch 'git\s+push\s+\S') {
                try {
                    $branch = (& git rev-parse --abbrev-ref HEAD 2>$null | Select-Object -First 1)
                    if ($branch -and $branch.Trim() -in @('master', 'main')) { $isDefault = $true }
                } catch { }
            }

            if ($isDefault) {
                Deny (@(
                    "BLOCKED: direct push to the default branch.",
                    "Demerzel ships through reviewed PRs - master is never pushed to directly.",
                    "Push your working branch instead, then open a PR:",
                    "  git push -u origin <your-branch>",
                    "  gh pr create --base master"
                ) -join "`n")
            }
        }
    }

    # --- Rule 2: no runtime code outside the harness ----------------------------
    # Demerzel holds governance artifacts only. `scripts/` and `.github/` are the
    # documented exception (CI/harness tooling); `.claude/hooks/` holds hooks.
    if ($tool -in @('Write', 'Edit', 'NotebookEdit')) {
        $path = [string]$toolInput.file_path
        if ($path) {
            $normalized = ($path -replace '\\', '/')
            $runtimeExt = @('.py', '.ts', '.tsx', '.js', '.jsx', '.cs', '.fs', '.rs', '.go', '.rb', '.java')
            $ext = [System.IO.Path]::GetExtension($normalized).ToLowerInvariant()
            if ($runtimeExt -contains $ext) {
                $allowed = $normalized -match '/(scripts|\.github|\.claude)/' -or
                           $normalized -match '^(scripts|\.github|\.claude)/'
                if (-not $allowed) {
                    Deny (@(
                        "BLOCKED: runtime code outside the harness directories.",
                        "Demerzel contains NO runtime code - only governance artifacts",
                        "(personas, constitutions, policies, schemas, contracts, tests, docs).",
                        "If this really is harness/CI tooling, put it in scripts/ or .github/.",
                        "Otherwise express it as a governance artifact instead.",
                        "  attempted: $normalized"
                    ) -join "`n")
                }
            }
        }
    }
}
catch {
    # Never wedge the session on a guard bug.
    exit 0
}

exit 0
