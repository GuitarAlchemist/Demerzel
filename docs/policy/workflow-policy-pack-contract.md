# Workflow Policy Pack Contract

Date: 2026-07-01

Status: draft / advisory

## Purpose

Define how `.github` workflow mechanisms may consume Demerzel-owned policy semantics without embedding policy authority inside `.github`.

## Core split

```text
.github  = mechanism
Demerzel = policy
```

`.github` may run checks, upload reports, and expose reusable workflow contracts.

Demerzel owns what findings mean for lifecycle transitions, review modes, human gates, promotion gates, and blocking behavior.

## Contract sketch

```json
{
  "policy_pack_id": "demerzel-methodology-policy-v1",
  "version": "0.1-draft",
  "owner": "GuitarAlchemist.Demerzel.Policy.Methodology",
  "applies_to": ["issue", "pull_request", "abstraction_candidate"],
  "signals_consumed": [
    "missing-business-value",
    "missing-hierarchy",
    "missing-scope-boundary",
    "missing-evidence",
    "unclear-review-mode"
  ],
  "recommendations_emitted": [
    "keep-shaping",
    "ready-for-fast-review",
    "needs-focused-review",
    "decision-gate-required",
    "do-not-promote"
  ],
  "safe_default": "keep-shaping",
  "human_authority_required_for": [
    "strict-blocking",
    "org-wide-promotion",
    "policy-version-bump",
    "governance-critical-change"
  ]
}
```

## Non-goals

```text
Do not run GitHub Actions from Demerzel.
Do not parse GitHub event payloads here.
Do not duplicate .github workflow mechanics.
Do not hide raw evidence behind policy summaries.
```

## Promotion rule

A `.github` workflow finding can become a Demerzel policy gate only when:

```text
pilot evidence exists
false positives are measured
IX metric exists or is planned
human decision authority is preserved
rollback path exists
```

## Related

- GuitarAlchemist/.github#28
- GuitarAlchemist/.github#30
- GuitarAlchemist/.github/VERSIONED_IMPORT_POLICY.md
- #588
- #592
