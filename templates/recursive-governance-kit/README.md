# Recursive Self-Governance Kit

Version: 1.0.0
Issued: 2026-03-22

## Purpose

This kit bootstraps recursive governance in consumer repos (ix, tars, ga). Per VSM (Viable System Model), every viable system must contain viable subsystems. This kit gives each repo its own S1-S5 while federating up to Demerzel's governance.

## Architecture

```
Your repo/
  governance/
    constitution.md          -- inherits Asimov, adds repo-specific articles
    policies/
      local-policy-template.yaml  -- template for repo-specific policies
    state/
      beliefs/               -- local tetravalent belief states
      pdca/                  -- local PDCA cycle tracking
      conscience/            -- local conscience signals
    tests/behavioral/
      governance-adoption-cases.md  -- validates kit adoption
  CLAUDE.md                  -- updated with governance integration snippet
```

## VSM Mapping

| VSM System | Repo-Level Role | Demerzel-Level Role |
|-----------|----------------|---------------------|
| S1 (Operations) | Repo agents executing tasks | -- |
| S2 (Coordination) | Local policy enforcement | Receives local S3 reports |
| S3 (Control) | Local governance audit | Reports to Demerzel S2 via Galactic Protocol |
| S4 (Intelligence) | Local reconnaissance + learning | Feeds Seldon knowledge transfer |
| S5 (Policy) | Local constitution (inherits Asimov) | Demerzel Asimov constitution (root authority) |

## Adoption Steps

1. **Copy** this kit's contents into your repo under `governance/`
2. **Customize** `constitution.md` -- add repo-specific articles (12+) while preserving Asimov inheritance
3. **Configure** Galactic Protocol connection -- set repo identity in constitution preamble
4. **Set up** algedonic channel -- conscience signals feed up to Demerzel S5
5. **Run** initial governance audit using `governance-adoption-cases.md` tests

Or use the skill: `/demerzel bootstrap-governance [repo]`

## Federation Model

This is **federation, not duplication**:
- The Asimov constitution (Articles 0-5) is inherited by reference, never copied
- Local constitutions extend with repo-specific articles numbered 12+
- Local policies operate subordinate to Demerzel policies
- Local S3 reports to Demerzel S2 via Galactic Protocol directives and compliance reports
- Local conscience signals are algedonic -- they propagate upward when thresholds are crossed

## Algedonic Channel

Consumer repos generate conscience signals (discomfort, regret, anticipatory warnings). When a signal exceeds the local threshold:

1. Signal is logged locally in `state/conscience/`
2. If severity >= `high`, signal is packaged as a Galactic Protocol compliance report
3. Report is sent to Demerzel with `type: algedonic-alert`
4. Demerzel S5 evaluates and may issue follow-up directives

## Files in This Kit

| File | Purpose |
|------|---------|
| `README.md` | This file -- adoption guide |
| `constitution.md` | Template constitution inheriting Asimov |
| `policies/local-policy-template.yaml` | Template for repo-specific policies |
| `state/beliefs/.gitkeep` | Belief state directory |
| `state/pdca/.gitkeep` | PDCA cycle directory |
| `state/conscience/.gitkeep` | Conscience signal directory |
| `tests/behavioral/governance-adoption-cases.md` | Adoption validation tests |
| `CLAUDE.md.snippet` | Governance integration for repo CLAUDE.md |

## References

- [Asimov Constitution](../../constitutions/asimov.constitution.md)
- [Galactic Protocol](../../contracts/galactic-protocol.md)
- [VSM Course CYB-001](../../state/streeling/courses/cybernetics/en/CYB-001-vsm-ai-governance-mapping.md)
- [Demerzel Mandate](../../constitutions/demerzel-mandate.md)
