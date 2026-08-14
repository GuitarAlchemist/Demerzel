# Epistemic Research Proposal v0.1

Status: draft tracer contract. Validation is advisory and authorizes nothing.

## Purpose

Gaia uses this contract when accepted, fresh evidence cannot answer a bounded
question. Demerzel validates the proposal's epistemic and governance shape. It
does not run the proposed probe, select an agent, route work, spend money, or
grant authority.

The envelope travels as `untrusted-text` through Gaia's existing `send` or
`handoff` verb. This contract adds no bus verb and does not make Gaia a Galactic
Protocol participant.

## Bounded vocabulary

- **Epistemic gap**: a typed observation that accepted evidence is missing,
  contradictory, stale, out of distribution, unmapped, control-failing,
  surprising, or beyond a declared capability.
- **Research question**: a question whose answer can discriminate between at
  least two explicit hypotheses.
- **Falsifier**: an observation that would reject one hypothesis.
- **Negative control**: an input expected not to change the result; movement
  invalidates or qualifies the inference.
- **Probe**: a bounded, reversible, zero-paid-cost proposal. A proposal is not
  permission to execute it.
- **Uncertainty mass**: integer parts per million over Demerzel's T/P/U/D/F/C
  states. The semantic validator enforces an exact total of 1,000,000.

Terms are local to the `gaia-epistemic/0.1.0` bounded context. A changed meaning
requires a new vocabulary version; it must not silently reuse an old identifier.

## Competency questions

The vocabulary and schema are adequate only if they can answer:

1. What exact accepted revision exposed the gap?
2. What kind of gap was observed, and about which subject?
3. Which competing hypothesis is the null hypothesis?
4. What observation would falsify each hypothesis?
5. Which negative control can reveal a spurious result?
6. What is the probe's explicit cost unit and upper bound?
7. Does the proposal request or imply execution authority?
8. When does the proposal expire, and which input revision makes it stale?
9. Can an independent implementation reproduce the proposal digest?

## Digest recipe

Remove only `proposalId` and `revision`, recursively sort object keys, preserve
array order, encode compact JSON as UTF-8, and take SHA-256. The complete
proposal uses `proposalId = "erp-" + digest` and records the same digest under
`revision.digest`.

`createdAt` and `expiresAt` use the single canonical form produced by
JavaScript `Date.prototype.toISOString()`: UTC, exactly three fractional-second
digits, and a trailing `Z` (for example `2026-08-14T17:30:00.000Z`). Equivalent
RFC 3339 offsets are intentionally rejected so every conforming implementation
hashes the same timestamp representation.

## Why not OWL/BFO yet

JSON Schema plus semantic validation gives this operational contract closed,
fail-closed checks. OWL's open-world and monotonic reasoning do not model stale
or superseded operational revisions directly, and BFO would introduce a broad
upper ontology before this bounded vocabulary proves a need for cross-domain
inference. Reconsider RDF/SHACL or OWL only after several repos need inference
that typed WorkGraph relations and competency questions cannot express safely.

## Existing Demerzel policy

This contract specializes, rather than duplicates, `reconnaissance-policy.yaml`
and `belief-currency-policy.yaml`: unknowns trigger investigation, stale beliefs
cannot be treated as current, and escalation remains separate from execution.
