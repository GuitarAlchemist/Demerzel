# Directive: Adopt @ai Probe Annotations

**Directive ID:** DIR-2026-03-21-001
**Type:** policy-adoption
**From:** Demerzel (Governor)
**To:** ix, tars, ga
**Priority:** Medium
**Issued:** 2026-03-21
**Compliance Deadline:** 30 days from issuance (2026-04-20)

## Requirement

All consumer repos must adopt `@ai probe` annotations on exported/public symbols.

### Minimum Requirements
- Achieve 30% probe coverage (probed_symbols / total_exported_symbols >= 0.3)
- Use the syntax defined in `docs/specs/ai-probes-syntax.md`
- At minimum, add `@ai probe:` and `@ai domain:` annotations

### Recommended Additions
- `@ai invariant:` on functions with verifiable properties
- `@ai governs:` on code implementing governance policies
- `@ai tested-by:` linking to behavioral tests

## Verification

RECON phase will scan for `@ai` annotations and report coverage metrics.
Coverage is tracked in `health-scores.json` per repo.

## Acceptance Criteria

- Coverage metric >= 0.3 reported in compliance report
- No `@ai governs:` references to nonexistent policies
- Probe syntax follows the specification

## Rejection Grounds

Per Galactic Protocol, valid rejection requires:
- **First Law override:** Probes would cause harm to humans (data harm, trust harm, or autonomy harm)
- **Second Law override:** A human operator has explicitly countermanded this directive

Both require logged reasoning with constitutional citations.

## Reference

- Policy: `policies/ai-probes-policy.yaml`
- Syntax: `docs/specs/ai-probes-syntax.md`
- Schema: `schemas/ai-probe.schema.json`
