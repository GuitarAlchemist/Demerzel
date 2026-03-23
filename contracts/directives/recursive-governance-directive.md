# Directive: Adopt Recursive Self-Governance Kit

**Directive ID:** DIR-2026-03-22-001
**Type:** compliance-requirement
**From:** Demerzel (Governor)
**To:** ix, tars, ga
**Priority:** High
**Issued:** 2026-03-22
**Compliance Deadline:** 30 days from issuance (2026-04-21)

## Constitutional Authority

- **Article 0 (Zeroth Law):** Governance integrity -- recursive governance prevents silent degradation of subsystem alignment
- **Article 8 (Observability):** Each repo must expose its own governance health metrics
- **Article 9 (Bounded Autonomy):** Local governance defines explicit operational bounds per repo domain

## Requirement

All consumer repos (ix, tars, ga) must adopt the recursive self-governance kit, establishing local S1-S5 governance subsystems federated under Demerzel.

### What To Do

1. Run `/demerzel bootstrap-governance [repo]` or manually copy `templates/recursive-governance-kit/`
2. Create `governance/` directory with constitution, policies, state, and tests
3. Customize local constitution with at least one repo-specific article (Article 12+)
4. Configure Galactic Protocol connection (S3 -> Demerzel S2)
5. Set up algedonic channel (local S5 -> Demerzel S5)
6. Pass all six adoption test cases in `governance-adoption-cases.md`
7. Submit compliance report

### Per-Repo Minimum Local Articles

Each repo must define at least these domain-specific articles:

**ix (Rust ML forge):**
- Article 12: ML Model Safety -- models require validation pipeline approval before deployment
- Article 13: Training Data Governance -- data provenance must be tracked and auditable

**tars (F# reasoning):**
- Article 12: Reasoning Integrity -- inference chains must be traceable and falsifiable
- Article 13: Belief State Hygiene -- beliefs must have evidence and staleness tracking

**ga (.NET music):**
- Article 12: Content Safety -- generated audio must not contain harmful or unauthorized content
- Article 13: Attribution Integrity -- generated content must respect source attribution

## Acceptance Criteria

- `governance/constitution.md` exists and inherits Asimov Articles 0-5
- `governance/state/beliefs/`, `governance/state/pdca/`, `governance/state/conscience/` directories exist
- At least one local policy exists in `governance/policies/`
- CLAUDE.md contains governance integration snippet with Galactic Protocol section
- Algedonic channel thresholds are configured
- All six governance-adoption-cases.md tests pass
- Compliance report submitted to Demerzel

## Verification

Demerzel will verify adoption via reconnaissance request (Tier 2 scan):
- Check for `governance/` directory structure
- Validate constitution inheritance chain
- Confirm Galactic Protocol connection is active
- Verify algedonic channel is configured

## Rejection Grounds

Per Galactic Protocol, valid rejection requires:
- **First Law override:** Governance kit adoption would cause harm to humans (data harm, trust harm, or autonomy harm)
- **Second Law override:** A human operator has explicitly countermanded this directive

Both require logged reasoning with constitutional citations.

## Reference

- Kit: `templates/recursive-governance-kit/`
- Skill: `/demerzel bootstrap-governance`
- VSM theory: `state/streeling/courses/cybernetics/en/CYB-001-vsm-ai-governance-mapping.md`
- Galactic Protocol: `contracts/galactic-protocol.md`
- Issue: https://github.com/GuitarAlchemist/Demerzel/issues/167
