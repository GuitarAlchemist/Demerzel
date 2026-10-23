# Epistemic Research Proposal Tracer Plan

Status: implemented on isolated branches; pending independent Standards and Spec review.

## Problem

Gaia needs a bounded way to admit a knowledge gap, formulate competing explanations, and request a falsifiable research probe without hallucinating certainty or acquiring execution authority. Demerzel needs to validate that proposal without becoming a hidden orchestrator.

## Constraints

- Preserve the six Gaia bus verbs: `register`, `send`, `inbox`, `ack`, `heartbeat`, and `handoff`.
- Proposals are advisory data. They cannot authorize execution, spend, routing, installation, publication, or mutation.
- Every proposal is content-addressed, deterministic, replayable, and provenance-bearing.
- Paid cost is zero in this tracer.
- Gaia is not represented as a Galactic Protocol `origin_repo` until that protocol explicitly supports it.

## Design It Twice

Three seams were compared before implementation:

1. **Selected: pure constructor plus pure validator.** Gaia builds and verifies a proposal; Demerzel validates its schema and semantic invariants. Transport remains ordinary `send` payload text.
2. **Rejected: inquiry state machine.** It duplicated WorkGraph lifecycle and introduced new authority-bearing state before the proposal contract was understood.
3. **Rejected: one-call research orchestrator.** It hid effects, budgets, and execution boundaries behind a convenient API.

The selected seam is the smallest deep module: it hides canonicalization and validation while exposing no I/O or mutation.

## Contract invariants

- At least two hypotheses, exactly one explicit null, and a falsifier for every hypothesis.
- One declared negative control.
- Integer parts-per-million uncertainty over `T/P/U/D/F/C`, summing exactly to 1,000,000.
- Immutable evidence references and SHA-256 content identity.
- `authority.mode = advisory`, `executionAuthorized = false`, no requested authority, and zero maximum cost.
- Vocabulary identity and version are explicit.

## Ontology boundary

The tracer uses a versioned bounded vocabulary and competency questions. It does not introduce OWL, BFO, or a global ontology. Revisit RDF/SHACL only when cross-tool inference, constraint exchange, or ontology alignment is demonstrated by a concrete failing use case.

## TDD and verification

The implementation began with failing tests for the missing modules. Negative controls cover single-hypothesis proposals, missing nulls/falsifiers/controls, malformed uncertainty mass, ambiguous cost, authority widening, unhashed provenance, and content tampering. Full repository verification and an independent dual-axis review are required before merge.

## Rollout and reversibility

The changes live on isolated branches in Gaia and Demerzel. No installation, runtime activation, push, or publication is authorized. Reverting the two commits removes the tracer without migrating durable state. A later implementation must remain advisory until separately authorized and verified.

## Success criteria

- Gaia constructs and round-trips a deterministic proposal without performing effects.
- Demerzel rejects every declared negative control and accepts the valid fixture.
- Existing test suites remain green.
- Independent Standards and Spec reviews approve both repository changes.
