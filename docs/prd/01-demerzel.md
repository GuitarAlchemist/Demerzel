# PRD: Demerzel -- AI Governance Framework

**Version:** 1.0 | **Last Updated:** 2026-04-03 | **Status:** Active

---

## Executive Summary

Demerzel is a specification-only governance framework for AI agents, providing constitutions, personas, policies, behavioral tests, and cross-repo communication contracts. It contains no runtime code -- only YAML, Markdown, and JSON Schema artifacts that consumer repos (ix, tars, ga) adopt via git submodule. Named after Asimov's R. Daneel Olivaw, it enforces a constitutional hierarchy rooted in the Laws of Robotics.

## Problem Statement

AI coding agents operating across multiple repositories need consistent behavioral guardrails, confidence thresholds, and escalation policies. Without a shared governance layer, each repo reinvents alignment rules, personas drift between repos, and there is no auditable trail of agent decision-making.

## Goals & Success Metrics

### P0 (Must-Have)
- **Constitutional coverage**: Every consumer repo integrates the Asimov + default constitution hierarchy
- **Persona validation**: 100% of persona files pass JSON Schema validation (42 schemas exist)
- **Behavioral test coverage**: Every persona has at least one behavioral test (111 test suites, 200+ cases)

### P1 (Should-Have)
- **Policy adoption**: All 44 policies referenced by at least one consumer repo
- **Cross-repo compliance**: Galactic Protocol directives produce compliance reports within 24h
- **Hexavalent logic adoption**: tars and ix use T/P/U/D/F/C for belief states

### P2 (Nice-to-Have)
- **Case law accumulation**: Constitutional cases build precedent for edge-case governance decisions
- **Standing orders**: Persistent governance directives that survive session boundaries

## Key Features (What Exists)

| Feature | Artifacts | Count |
|---------|-----------|-------|
| Constitutions | Asimov (Articles 0-5) + Default (Articles 1-11) + Mandate + Harm Taxonomy | 4 |
| Personas | YAML archetypes defining agent roles and voices | 14 |
| Policies | YAML policies covering alignment, kaizen, conscience, etc. | 44 |
| Behavioral Tests | Thought experiment test suites | 111 suites, 200+ cases |
| JSON Schemas | Validation schemas for all artifact types | 42 |
| Galactic Protocol | Cross-repo communication contracts | 1 spec + schemas |
| Logic System | Hexavalent (T/P/U/D/F/C) + PDCA + knowledge state | 3 systems |
| Persistent State | Beliefs, evolution, conscience, intuition, streeling | 9 state categories |

## Architecture

```
Constitution Hierarchy:
  asimov.constitution.md (root)
    ├── demerzel-mandate.md (enforcer)
    └── default.constitution.md (operational)
         └── policies/*.yaml (44 policies)
              └── personas/*.persona.yaml (14 personas)

Confidence Thresholds:
  >= 0.9 → autonomous  |  >= 0.7 → proceed with note
  >= 0.5 → confirm     |  >= 0.3 → escalate  |  < 0.3 → halt
```

## Current Status

- **Mature**: Constitutions, personas, policies, schemas, behavioral tests
- **Active**: Case law system, standing orders, compounding metrics
- **Growing**: Galactic Protocol adoption across consumer repos

## Next Steps

1. Increase constitutional case law corpus for edge-case precedent
2. Automate compliance report collection from consumer repos
3. Schema versioning strategy for backward-compatible evolution

## Cross-Repo Dependencies

- **Consumed by**: ix (submodule), tars (submodule), ga (submodule)
- **Depends on**: Nothing (root of the governance hierarchy)
- **Communication**: Galactic Protocol directives out, compliance reports in
