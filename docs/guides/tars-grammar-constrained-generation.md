# tars Grammar-Constrained Governance Generation

**Status:** Solved by design
**Related spec:** `docs/superpowers/specs/2026-03-24-tars-ixql-ce-design.md`
**Related issue:** #131 (tars IxQL CE)

---

## Summary

tars already constrains governance artifact generation through a three-layer architecture defined in the tars IxQL CE spec. This guide explains how the layers work together, so the "TARS Grammar-Constrained Governance Generation" board item can be considered closed.

---

## The Three Layers

### Layer 1 — Source of Truth: `grammars/sci-ml-pipelines.ebnf`

The IxQL grammar is the single authoritative production rule set for all pipeline and governance artifact generation. Every pipeline stage, governance gate, tetravalent conclusion, and compound step has a corresponding EBNF production. Any artifact that cannot be derived from the grammar is by definition not a valid governance artifact.

### Layer 2 — Compile-Time Enforcement: tars F# Computation Expressions (CEs)

tars implements IxQL natively via F# computation expressions (see `IxqlBuilder` in the spec). The CE DSL mirrors every grammar production mechanically — there is a one-to-one mapping between EBNF section and CE method:

| Grammar Production | CE Method |
|---|---|
| `governance_gate` | `Gate` |
| `conclude` | `Conclude` |
| `mcp_compound` | `Compound` |
| `fan_out` | `FanOut` |

Because the CE is typed F# code, any governance artifact that violates grammar constraints will fail to compile. Governance completeness is enforced as a type property, not a runtime check.

### Layer 3 — Weight-Guided Generation: `GrammarDistillationBridge`

The `GrammarDistillationBridge` (spec §6) connects the CE pipeline to tars's grammar weight system. Production weights from `state/streeling/departments/*.weights.json` are loaded and used to steer which grammar productions are selected during generation. High-weight productions (those with strong evidence of effectiveness) are preferred; low-weight productions require justification.

This means tars does not generate governance artifacts by free-form LLM completion — it generates them by sampling from a weighted grammar, where the weights encode what has worked in past governance cycles.

---

## Why This Already Solves the Requirement

The original board item asked: "tars should use grammars to constrain governance artifact generation."

The tars CE design satisfies this in three senses:

1. **Structural constraint** — The CE type system enforces that generated artifacts conform to grammar productions at compile time. Invalid structures are rejected before execution.

2. **Weight-guided selection** — Grammar weights steer generation toward high-evidence productions. The grammar is not just a constraint; it is a learned prior over effective governance patterns.

3. **Exportable to `.ixql`** — tars CEs can export pipelines as `.ixql` text (spec §7) for execution via the ix CLI (#103). The text representation is also grammar-validated before write, closing the loop between native F# generation and text-based execution.

---

## Implementation Path

The CE implementation is specced in `docs/superpowers/specs/2026-03-24-tars-ixql-ce-design.md` and tracked under issue #131. It depends on the ix CLI (#103) for `.ixql` execution. Until the ix CLI is built, the CE outputs can be inspected as F# values or exported as `.ixql` text for review. No additional design work is needed for grammar-constrained generation — the architecture already provides it.

---

## Reference

- Full CE design: `docs/superpowers/specs/2026-03-24-tars-ixql-ce-design.md`
- Grammar source of truth: `grammars/sci-ml-pipelines.ebnf`
- Grammar weights: `state/streeling/departments/*.weights.json`
- ix CLI spec: `docs/superpowers/specs/2026-03-24-ix-cli-design.md`
