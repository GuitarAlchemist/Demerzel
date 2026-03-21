# External Grammar References

**Date:** 2026-03-21
**Purpose:** Catalog of external grammars, DSLs, and formal languages that Demerzel departments should reference or distill into tars-compatible grammar rules.

For each entry: what it is, specification URL, which Demerzel department would consume it, and how tars could distill it via the grammar pipeline (see `docs/grammar-pipeline.md`).

---

## Music

### MusicXML

- **What:** W3C community standard for music notation interchange. XML-based format representing notes, rests, dynamics, articulations, and layout across parts and measures.
- **Spec:** https://www.w3.org/2021/06/musicxml40/
- **Department:** Music Theory, Guitar Studies
- **Distillation path:** Parse MusicXML schemas to extract structural patterns (measure -> attributes -> note sequences). Distill into `TypedProduction` rules mapping scale/chord patterns from `music-theory.ebnf` to concrete MusicXML output structures. Guitar-specific notation (string/fret attributes) feeds `guitar-technique.ebnf`.

### MEI (Music Encoding Initiative)

- **What:** Scholarly music encoding standard. XML-based like MusicXML but designed for musicological analysis, critical editions, and historical notation. Richer metadata model.
- **Spec:** https://music-encoding.org/guidelines/v5/
- **Department:** Musicology
- **Distillation path:** MEI's analytical markup (harmonic analysis, formal structure annotations) maps directly to `musicology-analysis.ebnf` productions. Distill the `<harm>`, `<analysis>`, and `<annot>` element patterns as behavioral facets for musicological reasoning traces.

### ABC Notation

- **What:** Text-based music notation using ASCII characters. Compact representation popular in folk music communities. Each tune fits in a few lines of text.
- **Spec:** https://abcnotation.com/wiki/abc:standard:v2.1
- **Department:** Music Theory, Guitar Studies
- **Distillation path:** ABC's terse grammar is close to EBNF already (note = pitch + duration + accidental). Parse the ABC standard directly into structural facets. Useful for quick notation in chat/REPL contexts where MusicXML is too verbose.

### LilyPond

- **What:** Music typesetting system with a text-based input language. Produces publication-quality scores. The input syntax is a DSL for music notation.
- **Spec:** https://lilypond.org/doc/v2.24/Documentation/notation/
- **Department:** Music Theory
- **Distillation path:** LilyPond's input grammar defines voice/staff/score hierarchy that maps to `music-theory.ebnf` structural patterns. Distill layout and engraving patterns as a typed facet layer (input: musical structure, output: typeset score).

### MIDI Specification

- **What:** Digital music interface standard. Defines messages for note-on/off, control changes, program changes, and system-exclusive data. Binary protocol, not a text grammar, but the message structure is highly regular.
- **Spec:** https://www.midi.org/specifications-old/item/the-midi-1-0-specification (MIDI 1.0), https://www.midi.org/midi-2-0 (MIDI 2.0)
- **Department:** Music Theory, Acoustics / Physics
- **Distillation path:** Model MIDI message structure as typed productions (NoteOn -> channel * note * velocity). The timing model (ticks, tempo maps) feeds `acoustics-physics.ebnf` temporal reasoning. MIDI 2.0's property exchange protocol could inform governance directive patterns.

---

## Formal Proofs

### Lean 4

- **What:** Dependently typed programming language and interactive theorem prover. Used for formalized mathematics (Mathlib) and verified software.
- **Spec:** https://lean-lang.org/lean4/doc/
- **Department:** Mathematics
- **Distillation path:** Lean's tactic syntax (by, simp, ring, omega) maps to `mathematical-proof.ebnf` proof step patterns. Distill tactic sequences from successful proofs as behavioral facets. The type system's dependent types inform typed facet composition checking.

### Coq Gallina

- **What:** Specification language for the Coq proof assistant. Gallina is the term language; Ltac/Ltac2 are the tactic languages. Mature ecosystem with extensive verified mathematics.
- **Spec:** https://coq.inria.fr/doc/V8.19.1/refman/
- **Department:** Mathematics
- **Distillation path:** Gallina's `Theorem/Proof/Qed` structure directly parallels `mathematical-proof.ebnf` axiom-lemma-theorem-proof structure. Distill proof strategies (induction, case analysis, rewriting) as structural facets. Ltac patterns become behavioral facets for proof automation.

### Agda

- **What:** Dependently typed functional programming language with Unicode support and mixfix operators. More explicit than Lean/Coq -- proofs are programs, no separate tactic language.
- **Spec:** https://agda.readthedocs.io/en/latest/
- **Department:** Mathematics
- **Distillation path:** Agda's explicit proof terms (no tactic hiding) make structural distillation straightforward. Pattern matching on inductive types maps to `mathematical-proof.ebnf` case analysis rules. The termination checker's structural recursion patterns inform behavioral constraints.

---

## Acoustics and Audio

### Faust

- **What:** Functional audio stream processing DSL. Compiles to C++, WebAssembly, and other targets. Block-diagram algebra for signal processing: sequential (`:` ), parallel (`,`), split (`<:`), merge (`:>`).
- **Spec:** https://faust.grame.fr/doc/manual/
- **Department:** Acoustics / Physics
- **Distillation path:** Faust's block-diagram algebra is a natural typed grammar: each block has input/output signal counts that must compose. Distill the five composition operators as structural facets. Signal processing patterns (filters, oscillators, envelopes) become behavioral facets for `acoustics-physics.ebnf`.

### Csound

- **What:** Sound design and synthesis language. Orchestra/score paradigm: instruments define signal processing, scores define events over time. One of the oldest computer music languages (1985).
- **Spec:** https://csound.com/docs/manual/
- **Department:** Acoustics / Physics
- **Distillation path:** Csound's opcode system (1500+ opcodes) is a rich behavioral catalog. Distill opcode categories (oscillators, filters, granular, spectral) as typed productions. The orchestra/score separation maps to structural facets (instrument definition vs. event scheduling).

### SuperCollider

- **What:** Real-time audio synthesis and algorithmic composition environment. Client/server architecture: sclang (language) communicates with scsynth (audio server) via OSC.
- **Spec:** https://doc.sccode.org/
- **Department:** Acoustics / Physics, Music Theory
- **Distillation path:** SuperCollider's UGen graph model maps to structural facets (DAG of synthesis nodes). Pattern library (Pbind, Pseq, Prand) maps directly to `music-theory.ebnf` compositional patterns. Server command protocol informs MCP tool interaction patterns.

---

## General / Cross-Domain

### JSON Schema

- **What:** Vocabulary for annotating and validating JSON documents. Used extensively in Demerzel for schema validation of personas, beliefs, pipelines, and contracts.
- **Spec:** https://json-schema.org/specification
- **Department:** Core Governance (all departments)
- **Distillation path:** Already integrated. Demerzel schemas in `schemas/` define validation for governance artifacts. tars `GrammarDistill.fs` uses JSON document parsing for low-level shape distillation. Future: distill JSON Schema metapatterns (allOf/oneOf/anyOf compositions) as structural facets for schema evolution.

### GraphQL Schema

- **What:** API query language with a type system for defining data shapes. Schema Definition Language (SDL) declares types, queries, mutations, and subscriptions.
- **Spec:** https://spec.graphql.org/October2021/
- **Department:** Computer Science
- **Distillation path:** GraphQL's type system (object types, interfaces, unions, enums) maps to typed facets for API interaction patterns. Query composition (nested selections, fragments, variables) could inform `algorithms.ebnf` data access patterns. Useful if tars exposes a GraphQL API for governance queries.

### SPARQL

- **What:** RDF query language for semantic web data. Pattern matching on graph triples (subject-predicate-object) with OPTIONAL, UNION, and FILTER clauses.
- **Spec:** https://www.w3.org/TR/sparql11-query/
- **Department:** Research Methods, Musicology
- **Distillation path:** SPARQL's graph pattern matching aligns with `scientific-method.ebnf` hypothesis testing (query as hypothesis, results as evidence). Useful for querying linked open data (e.g., MusicBrainz, Wikidata) in musicological research. Distill query patterns as behavioral facets.

### OpenAPI 3.x

- **What:** REST API specification format. Describes endpoints, parameters, request/response schemas, authentication, and server configuration. Machine-readable API contracts.
- **Spec:** https://spec.openapis.org/oas/v3.1.0
- **Department:** Core Governance, Computer Science
- **Distillation path:** OpenAPI specs define tool interfaces -- directly relevant to MCP tool catalog generation. Distill endpoint patterns (CRUD operations, pagination, error responses) as structural facets. Schema components map to typed facets for API interaction governance.

---

## Distillation Priority Matrix

| Grammar | Urgency | Rationale |
|---------|---------|-----------|
| MusicXML | High | Core interchange format for ga (Guitar Alchemist) domain |
| Lean 4 | High | Enables verified reasoning in mathematical proofs |
| Faust | High | Direct mapping to acoustics grammar, typed composition |
| ABC Notation | Medium | Quick notation for chat/REPL music interactions |
| MEI | Medium | Scholarly analysis aligns with musicology department |
| JSON Schema | Medium | Already partially integrated, deepen metapattern distillation |
| OpenAPI 3.x | Medium | MCP tool catalog generation from API specs |
| LilyPond | Low | Typesetting output, less critical for reasoning |
| Coq Gallina | Low | Complementary to Lean 4, lower priority |
| Agda | Low | Niche, useful for explicit proof extraction |
| MIDI | Low | Binary protocol, structural patterns already well-known |
| Csound | Low | Historical interest, SuperCollider is more modern |
| SuperCollider | Low | Real-time synthesis, less aligned with governance |
| GraphQL | Low | Only relevant if tars exposes a query API |
| SPARQL | Low | Linked data queries, niche use case |

---

## How to Add a New External Grammar Reference

1. Identify the grammar/DSL and its specification URL
2. Determine which Demerzel department(s) would consume it
3. Describe the distillation path: which facets (structural, typed, behavioral) map to which Demerzel EBNF
4. Assess urgency based on current department needs
5. Add the entry to this document following the format above
6. If high priority, create an issue for tars distillation implementation
