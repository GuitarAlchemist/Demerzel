# Pester tests for .claude/hooks/DigestState.psm1 — the first unit-testable seam
# in the hook layer. Exercises Write-Digest through its interface against an
# isolated $TestDrive RepoRoot with injected -RepoFacts (no git, no network).

BeforeAll {
    $repoRoot   = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
    $modulePath = Join-Path $repoRoot '.claude/hooks/DigestState.psm1'
    Import-Module $modulePath -Force

    # Build an isolated repo root that contains the schemas the module reads.
    $script:Root = "$TestDrive/repo"
    New-Item -ItemType Directory -Path "$script:Root/docs/contracts" -Force | Out-Null
    Copy-Item (Join-Path $repoRoot 'docs/contracts/digest-schema.json')       "$script:Root/docs/contracts/" -Force
    Copy-Item (Join-Path $repoRoot 'docs/contracts/pr-rationale-schema.json') "$script:Root/docs/contracts/" -Force

    $script:Facts = [pscustomobject]@{ Branch = 'main'; HeadSha = 'abc1234'; HeadSubject = 'test commit'; OpenPr = $null }
}

Describe 'Format-Yaml' {
    It 'returns null for empty input' { Format-Yaml '' | Should -Be 'null' }
    It 'single-quotes and escapes embedded quotes' { Format-Yaml "it's" | Should -Be "'it''s'" }
    It 'collapses newlines and caps length' {
        (Format-Yaml ("a`nb")) | Should -Be "'a b'"
        (Format-Yaml ('x' * 300) 10) | Should -Match "^'x{10}\.\.\.'$"
    }
}

Describe 'Counters' {
    It 'steps, reads, and resets' {
        Get-Counter -Name activity -RepoRoot $script:Root | Should -Be 0
        Step-Counter -Name activity -RepoRoot $script:Root | Should -Be 1
        Step-Counter -Name activity -RepoRoot $script:Root | Should -Be 2
        Get-Counter -Name activity -RepoRoot $script:Root | Should -Be 2
        Reset-Counter -Name activity -RepoRoot $script:Root
        Get-Counter -Name activity -RepoRoot $script:Root | Should -Be 0
    }
    It 'rejects an unknown counter name' {
        { Step-Counter -Name bogus -RepoRoot $script:Root } | Should -Throw
    }
}

Describe 'Write-Digest -Kind digest' {
    It 'writes a schema-valid digest to latest.md' {
        $r = Write-Digest -Kind digest -RepoRoot $script:Root -RepoFacts $script:Facts `
            -Trigger 'precompact-hook-fallback' -SessionId 'sess-1' -Body '# hello'
        $r.Valid | Should -BeTrue
        $r.Path  | Should -Be (Join-Path $script:Root 'state/digests/latest.md')
        Test-Path $r.Path | Should -BeTrue
        (Get-Content $r.Path -Raw) | Should -Match "trigger: 'precompact-hook-fallback'"
    }

    It 'fails validation on a bad trigger but still writes (fail-open)' {
        $r = Write-Digest -Kind digest -RepoRoot $script:Root -RepoFacts $script:Facts `
            -Trigger 'not-a-real-trigger' -SessionId 'sess-2' -Body 'x' -WarningAction SilentlyContinue
        $r.Valid   | Should -BeFalse
        $r.Written | Should -BeTrue
        Test-Path $r.Path | Should -BeTrue
    }

    It 'accepts mutations_since_last and success_criteria' {
        $sc = '[{"criterion":"build green","status":"pending","evidence":null}]'
        $r = Write-Digest -Kind digest -RepoRoot $script:Root -RepoFacts $script:Facts `
            -Trigger 'activity-tracker-mid-session' -SessionId 'mid' -MutationsSinceLast 7 `
            -SuccessCriteriaJson $sc -Body 'b'
        $r.Valid | Should -BeTrue
        (Get-Content $r.Path -Raw) | Should -Match 'mutations_since_last: 7'
        (Get-Content $r.Path -Raw) | Should -Match 'criterion:'
    }

    It 'rotates the prior latest into archive on overwrite' {
        Write-Digest -Kind digest -RepoRoot $script:Root -RepoFacts $script:Facts -Trigger 'digest-skill' -Body 'first' | Out-Null
        Write-Digest -Kind digest -RepoRoot $script:Root -RepoFacts $script:Facts -Trigger 'digest-skill' -Body 'second' | Out-Null
        (Get-ChildItem "$script:Root/state/digests/archive" -Filter '*.md').Count | Should -BeGreaterThan 0
    }
}

Describe 'Write-Digest counter auto-reset by trigger' {
    It 'digest-skill resets both activity and mid' {
        Step-Counter -Name activity -RepoRoot $script:Root | Out-Null
        Step-Counter -Name mid -RepoRoot $script:Root | Out-Null
        Write-Digest -Kind digest -RepoRoot $script:Root -RepoFacts $script:Facts -Trigger 'digest-skill' -Body 'x' | Out-Null
        Get-Counter -Name activity -RepoRoot $script:Root | Should -Be 0
        Get-Counter -Name mid -RepoRoot $script:Root | Should -Be 0
    }
    It 'activity-tracker-mid-session resets mid only, leaves activity' {
        Step-Counter -Name activity -RepoRoot $script:Root | Out-Null
        Step-Counter -Name mid -RepoRoot $script:Root | Out-Null
        Write-Digest -Kind digest -RepoRoot $script:Root -RepoFacts $script:Facts -Trigger 'activity-tracker-mid-session' -Body 'x' | Out-Null
        Get-Counter -Name mid -RepoRoot $script:Root | Should -Be 0
        Get-Counter -Name activity -RepoRoot $script:Root | Should -BeGreaterThan 0
    }
}

Describe 'Write-Digest -Kind rationale' {
    It 'writes a schema-valid pr-<num>-<slug>.md' {
        $r = Write-Digest -Kind rationale -RepoRoot $script:Root -RepoFacts $script:Facts `
            -PrNumber '123' -Title 'Fix the thing' -DiffShortstat ' 2 files changed' -Body 'rationale'
        $r.Valid | Should -BeTrue
        $r.Path  | Should -Match 'pr-123-fix-the-thing\.md$'
        (Get-Content $r.Path -Raw) | Should -Match "trigger: 'pr-rationale-capture'"
    }
}

Describe 'Test-Digest' {
    It 'validates a freshly written digest' {
        $w = Write-Digest -Kind digest -RepoRoot $script:Root -RepoFacts $script:Facts -Trigger 'digest-skill' -Body 'x'
        (Test-Digest -Path $w.Path -RepoRoot $script:Root).Valid | Should -BeTrue
    }
    It 'rejects a file with no frontmatter' {
        $bad = "$script:Root/state/digests/nofm.md"
        Set-Content -Path $bad -Value 'just a body' -Encoding UTF8
        (Test-Digest -Path $bad -RepoRoot $script:Root).Valid | Should -BeFalse
    }
    It 'infers rationale kind from the pr- filename' {
        $w = Write-Digest -Kind rationale -RepoRoot $script:Root -RepoFacts $script:Facts -PrNumber '9' -Title 'x' -Body 'b'
        (Test-Digest -Path $w.Path -RepoRoot $script:Root).Valid | Should -BeTrue
    }
}
