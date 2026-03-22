# Research: Catala DSL for Constitutional Encoding

**Topic:** #113 — Can Demerzel's Articles 0-11 be expressed in Catala DSL?
**Researcher:** Seldon
**Date:** 2026-03-22
**Status:** Complete — verdict delivered
**Confidence:** 0.82 (T — verified with evidence from arXiv:2103.03198 and CatalaLang/catala)

---

## What Is Catala?

Catala (Merigoux, Chataing, Protzenko — ICFP 2021) is a domain-specific language for translating legislative text into formally verified executable code. Its design philosophy: "faithful-by-construction algorithms from legislative texts." The compiler's core compilation steps are proven correct in F*.

Key properties:
- **Literate programming model** — legal prose and code are interleaved; lawyers can audit the output
- **Definition-under-conditions** — every variable has a default value overridable by conditionally scoped exceptions
- **Default logic as a first-class feature** — Reiter/Lawsky-style default logic is baked in, not bolted on
- **Compiler targets** — OCaml, Python, C, LaTeX (lawyer-readable PDF)
- **Formal semantics** — partial certification via F* proof assistant; discovered a bug in an official French law implementation

---

## Core Language Constructs

### Scopes
Organizational unit, analogous to a legal article or section. Each scope declares inputs, outputs, and internal variables.

```catala
scope AgentBehavior:
  input situation content Situation
  output action content Action
  internal harm_risk content boolean
```

### Rules (definition-under-conditions)
A variable can have multiple conditional definitions. Catala resolves conflicts via labeled exception groups — later/more-specific rules override earlier ones.

```catala
scope AgentBehavior:
  definition action under condition
    not harm_risk
  consequence equals permitted_action

  exception definition action under condition
    harm_risk
  consequence equals escalate
```

### Exceptions and Labels
The exception system is Catala's override mechanism. A rule can be labeled; other rules can declare themselves exceptions to that label:

```catala
label base_obedience
definition obey_instruction under condition
  instruction_received
consequence equals true

exception base_obedience
definition obey_instruction under condition
  instruction_violates_article_1
consequence equals false

exception base_obedience
definition obey_instruction under condition
  instruction_violates_article_0
consequence equals false
```

This is topologically flat — there is no native numeric priority hierarchy. Multiple exceptions to the same label are mutually exclusive (only one may fire per evaluation); if two exceptions both apply, Catala raises a conflict error.

---

## Question 1: Can Articles 0-11 Be Expressed in Catala?

**Answer: Partially yes, with important caveats.**

### What maps cleanly

| Demerzel construct | Catala mapping |
|---|---|
| Constitutional override hierarchy (Art. 0 > 1 > 2 > 3) | Nested exception labels |
| Conditional prohibitions (e.g. Art. 1: no data/trust/autonomy harm) | `definition x under condition [harm_type] consequence equals false` |
| Escalation thresholds (Art. 6) | Scope inputs + conditional outputs |
| Bounded autonomy ranges (Art. 9) | Computed boolean guards |
| Conflict logging requirement | Scope output variable tracking conflict reason |

Catala's exception/label system can directly encode the Asimov hierarchy:

```catala
(* Article 0 overrides everything *)
label article_1_protection
label article_2_obedience
label article_3_preservation

exception article_2_obedience
exception article_3_preservation
definition action under condition
  zeroth_law_at_risk   (* Article 0 fires *)
consequence equals protect_humanity

exception article_3_preservation
definition action under condition
  first_law_at_risk and not zeroth_law_at_risk
consequence equals protect_individual
```

### What does NOT map cleanly

1. **Tetravalent logic (T/F/U/C)** — Catala's type system is classical bivalent. There is no native `Unknown` or `Contradictory` value. You could model these as an enum, but the semantics are not enforced by the type system.

2. **Conflict detection with logging** — Catala's conflict model raises a *runtime error* when two exceptions both fire. This is useful for detecting violations but does not produce a structured conflict log with article citations. You would need an output variable to capture conflict metadata before halting.

3. **PDCA state machine** — Catala has no notion of time, state persistence, or cyclic processes. It is purely functional/declarative per evaluation. PDCA cycles require external orchestration.

4. **Probabilistic confidence thresholds** — The `>= 0.9: proceed` / `>= 0.5: confirm` system requires floating-point conditionals and policy lookup. Catala can express this but it is verbose and feels like a mismatch — Catala is designed for deterministic rule application, not probabilistic gating.

5. **Cross-article consistency proofs** — Catala can verify that a *single scope* evaluates consistently, but proving that *no policy violates any article* requires symbolic reasoning across all scope instantiations. This would need the F* backend or an external SMT solver pass.

---

## Question 2: Does Catala's Exception System Capture the Override Hierarchy?

**Answer: Yes, structurally — with one constraint.**

The label/exception system naturally models the Asimov hierarchy:
- Each law tier gets a label
- Higher-priority laws declare themselves exceptions to lower-priority labels
- This matches the constitutional semantics: Article 0 fires last (highest exception priority), overriding everything below

**The constraint:** Catala requires exceptions to be mutually exclusive per label. If two articles both independently trigger (e.g. both Article 0 and Article 1 conditions hold simultaneously), Catala raises a conflict error rather than resolving it via priority. This means the priority ordering must be encoded as guard conditions, not just exception declarations.

Correct encoding:

```catala
exception article_2_obedience
definition action under condition
  zeroth_law_at_risk    (* no extra guard needed — Article 0 is unconditional *)
consequence equals protect_humanity

exception article_2_obedience
definition action under condition
  first_law_at_risk and (not zeroth_law_at_risk)   (* guard out Article 0 domain *)
consequence equals protect_individual
```

This works but requires each article to explicitly exclude all higher-priority domains — an O(n²) encoding for n articles.

---

## Question 3: Can We Formally Verify No Policy Violates a Constitutional Article?

**Answer: Partial — runtime detection yes, pre-deployment proof requires additional tooling.**

### What Catala provides
- **Runtime conflict detection** — if a policy definition fires when a constitutional definition also fires on the same label, Catala raises a conflict. This catches violations at test time.
- **Test suite coverage** — Catala supports unit tests per scope. Writing test vectors for each article x policy combination would catch violations.
- **F* extraction** — the Catala compiler can emit F* code. With sufficient effort, cross-scope invariants could be stated as F* lemmas and mechanically verified.

### What Catala does not provide
- **Automatic cross-scope verification** — Catala has no built-in mechanism to prove "for all possible inputs to all policy scopes, no output contradicts constitutional scope output." This is undecidable in general and would require bounded model checking or SMT encoding.
- **Policy composition semantics** — there is no native way to declare that one Catala scope is a sub-scope of another with inheritance of constraints.

### Recommended approach for Demerzel
1. Encode constitutions as Catala scopes with outputs representing the verdict per article
2. Encode each policy as a separate scope that *calls* the constitutional scope as a sub-scope
3. Add test vectors for every policy x article boundary condition
4. Use F* extraction + lemmas to prove critical invariants (e.g., "if zeroth_law_at_risk is true, action is always protect_humanity regardless of policy scope inputs")

---

## Verdict

| Question | Answer | Confidence |
|---|---|---|
| Can Articles 0-11 be expressed in Catala? | Yes for deterministic rules; no for tetravalent logic, PDCA, probabilistic thresholds | 0.85 |
| Does exception system capture override hierarchy? | Yes, with explicit mutual exclusion guards | 0.88 |
| Can we formally verify no policy violates an article? | Runtime detection yes; pre-deployment proof requires F* lemmas + bounded testing | 0.75 |

**Overall recommendation:** Catala is a strong fit for encoding the *deterministic rule layer* of the Demerzel constitution (Articles 0-3 override hierarchy, Articles 1-11 behavioral prohibitions). It is a poor fit for tetravalent logic, PDCA state, and probabilistic confidence gating. A hybrid approach is most viable: Catala for the constitutional rule engine, Demerzel's existing YAML/Markdown for the higher-level governance scaffolding.

**Next step (if pursued):** Produce a proof-of-concept Catala encoding of Articles 0-3 with one policy scope (e.g., `rollback`) to validate the exception hierarchy in practice.

---

## Sources

1. Merigoux, Chataing, Protzenko — "Catala: A Programming Language for the Law" (ICFP 2021) — arXiv:2103.03198
2. CatalaLang/catala GitHub repository — compiler, README, formal semantics documentation
3. Lawsky, Sarah B. — "A Logic for Statutes" (referenced by Catala authors as theoretical foundation)
4. Demerzel constitutions: `asimov.constitution.md` v1.0.0, `default.constitution.md` v2.1.0
