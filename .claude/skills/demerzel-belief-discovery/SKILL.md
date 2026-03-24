---
name: demerzel-belief-discovery
description: Use when onboarding to an unfamiliar codebase, auditing documentation quality, or building a knowledge map of what is known, unknown, dead, or contradictory in a repo. Works on Java/Spring, TypeScript/React, Rust, .NET, YAML governance repos.
---

# Belief-Driven Codebase Discovery

AI doesn't generate docs — it builds **tetravalent beliefs** about the codebase with evidence, then reports what it knows, what it doesn't, and what contradicts itself. The Unknown beliefs ARE the onboarding guide.

## Usage

```
/demerzel belief-discovery [path]                    # Full two-phase run
/demerzel belief-discovery --phase audit [path]      # Phase 1 only (slop audit)
/demerzel belief-discovery --phase discover [path]   # Phase 2 only (belief building)
/demerzel belief-discovery --scope module [name]     # Scope to a module/package
/demerzel belief-discovery --lang java|typescript|rust|csharp|yaml
/demerzel belief-discovery --output report|json|onboarding
```

## Two-Phase Architecture

```
PHASE 1: AUDIT (kill the noise)              PHASE 2: DISCOVER (build beliefs)
  │                                            │
  ├─ Score existing docs for slop              ├─ Walk codebase as day-1 dev
  ├─ Substitution Test on every doc            ├─ Ask questions, not describe structure
  ├─ Flag docs that restate code               ├─ Cross-reference evidence sources
  ├─ Output: "these N docs are slop"           ├─ Assign tetravalent truth values
  │                                            ├─ Score confidence per belief
  └─ USES: /demerzel anti-slop-docs --audit    └─ Output: Belief Report
```

Phase 1 uses the existing `demerzel-anti-slop-docs` skill. Do not duplicate its logic — invoke it.

## Phase 1: Audit

Run `/demerzel anti-slop-docs --audit [path]` on the target codebase. This produces:
- Slop density scores per file
- List of docs to delete (score < 0.4)
- List of docs to rewrite (score 0.4-0.6)

Phase 1 earns credibility: you prove existing docs are bad before generating anything new.

**Gate:** If slop density > 60%, recommend a strip pass before Phase 2. Building beliefs on top of slop docs produces Contradictory beliefs that waste human time.

## Phase 2: Discover — Building Beliefs

### The Day-1 Developer Simulation

Walk the codebase as if you are a new developer on your first day. For every significant artifact (class, module, service, trait, policy, schema), ask these questions:

```
INTENT QUESTIONS (tree-sitter is the eyes, these are the brain):
  1. Why does this exist? What problem triggered its creation?
  2. What breaks if this is deleted?
  3. What's the contract? What are the invariants?
  4. Who calls this and why?
  5. Is this the right abstraction, or is it legacy?

EVIDENCE SOURCES:
  Code structure  → tree-sitter / LSP / static analysis → WHAT exists
  Change history  → git blame, git log                  → WHO, WHEN, WHY (commit msgs)
  Tickets         → Jira API (if available)              → original INTENT
  Wiki            → Confluence API (if available)        → documented DECISIONS
  Tests           → test files referencing artifact      → asserted BEHAVIOR
  Consumers       → import/use/reference graph           → actual DEMAND
```

Tree-sitter is the **eyes** driven by questioning **intent** — not structure-first. Never start by listing classes. Start by asking "why does this module exist?"

### Building a Belief

For each significant artifact, produce a belief tuple:

```yaml
belief:
  subject: "com.example.AuthService"
  proposition: "Centralizes auth because microservices had divergent token validation"
  truth_value: T | F | U | C
  confidence: 0.0-1.0
  evidence:
    supporting:
      - source: "git log (commit abc123, 2024-03-15)"
        claim: "Commit message: 'centralize auth after INC-2341'"
      - source: "Jira INC-2341"
        claim: "Three services had different expiry logic"
    contradicting: []
  questions_remaining:
    - "Is CryptoConfig still using RSA or did they migrate to Ed25519?"
  consumers: ["LoginController", "ApiGateway", "WebSocketHandler"]
  last_meaningful_commit: "2024-11-02"
```

### Truth Value Assignment Rules

| Truth Value | Condition | Confidence Range |
|-------------|-----------|-----------------|
| **T** (True) | 2+ independent sources agree, no contradictions | 0.7 - 1.0 |
| **F** (False) | Evidence of death: 0 consumers, 0 recent commits, deprecated markers | 0.7 - 1.0 |
| **U** (Unknown) | Code exists but intent unclear: no commit context, no docs, no tickets | 0.0 - 0.5 |
| **C** (Contradictory) | Sources disagree: docs say X, code does Y, or Jira says Z | 0.3 - 0.7 |

**Confidence scoring:**

```
base_confidence = 0.3 (code exists, we can read it)

+0.2  git blame provides meaningful commit message (not "fix" or "update")
+0.15 Jira/ticket linked with business context
+0.15 Tests assert specific behavior (not just "it compiles")
+0.1  Wiki/Confluence documents the decision
+0.1  Multiple consumers actively importing/using
-0.2  Last commit > 1 year ago (staleness penalty)
-0.15 Contradictory evidence found between any two sources
-0.1  Single-author, no review (bus factor = 1)
```

Cap at 1.0. Apply belief-currency-policy decay rates for staleness.

### Confidence Thresholds (from Demerzel governance)

- >= 0.9: Belief is solid — include in onboarding as fact
- >= 0.7: Belief is likely — include with note about evidence
- >= 0.5: Belief needs confirmation — flag for human review
- >= 0.3: Belief is weak — escalate, do not present as knowledge
- < 0.3: Do not act on this belief — mark U and surface as gap

## Output: Belief Report

### Format

```markdown
# Belief Report: {repo-name}
Generated: {date}
Artifacts scanned: {count}
Phase 1 slop density: {percentage}

## T — What We Know (with evidence chains)

### {Module/Package Name}
| Artifact | Proposition | Confidence | Key Evidence |
|----------|-------------|------------|--------------|
| AuthService | Centralizes auth after INC-2341 | 0.85 | git + Jira + 3 consumers |
| TokenStore | Redis-backed, fail-closed | 0.90 | code + tests assert fail-closed |

## F — What's Dead (LOLLI remediation candidates)

| Artifact | Evidence of Death | Last Activity | Action |
|----------|------------------|---------------|--------|
| LegacyAdapter | 0 consumers, 0 imports, deprecated marker | 2023-06-15 | DELETE |
| OldAuthMiddleware | Replaced by AuthService (see commit def456) | 2024-01-10 | DELETE |

→ Feed these to `/demerzel lolli-remediate` for scoring and ranked actions.

## U — What Nobody Knows (THE REAL GAPS)

These are the gold. Each Unknown is a question no source could answer.

| Artifact | Unanswered Question | Suggested Human | Why It Matters |
|----------|-------------------|-----------------|----------------|
| CryptoConfig | Why RSA and not Ed25519? Was this a deliberate choice? | @alice (git blame) | Security implications |
| RateLimiter | What are the actual limits? No config, no docs, no tests. | @bob (last author) | Production risk |
| EventBus | Is this used in prod or just dev? No integration tests. | Team lead | Dead code or critical infra? |

**Onboarding action:** A new dev should ask these questions on day 1. The answers become T beliefs.

## C — Contradictions (escalate to humans)

| Artifact | Source A Says | Source B Says | Severity |
|----------|--------------|---------------|----------|
| UserService | Confluence: "stateless, no caching" | Code: Redis cache on getUserById | HIGH — behavior differs from docs |
| PaymentGateway | Jira PROJ-456: "Stripe only" | Code: also has PayPal adapter | MEDIUM — scope creep or intentional? |

**Escalation:** Each C belief needs a human to resolve. The resolution becomes a T or F belief.
```

### Onboarding Mode (`--output onboarding`)

Restructures the report as a guided walkthrough for new developers:

```markdown
# Day 1 Onboarding: {repo-name}

## Start Here (highest-confidence T beliefs)
These are the things we're sure about. Read these first.
{Top 10 T beliefs sorted by consumer count — most-connected first}

## Ask These Questions (U beliefs, sorted by impact)
Nobody documented these. Your job on day 1 is to get answers.
{U beliefs with suggested humans to ask}

## Watch Out (C beliefs)
The docs and code disagree here. Don't trust either until resolved.
{C beliefs with both sides presented}

## Ignore These (F beliefs)
Dead code. Don't waste time reading it.
{F beliefs — things to skip}
```

## Language-Specific Discovery Patterns

### Java / Spring

```
Artifacts:  @Service, @Controller, @Component, @Repository, @Configuration beans
Consumers:  @Autowired, @Inject, constructor injection, XML bean refs
Intent:     Jira ticket in commit message, @author tag, package-info.java
Questions:  "Why is this a separate service?" "What Spring profile activates this?"
Watch for:  Interfaces with exactly 1 impl (unnecessary abstraction signal)
```

### TypeScript / React

```
Artifacts:  Exported components, hooks, services, utils, pages, API routes
Consumers:  import statements, route registrations, lazy-load references
Intent:     PR descriptions, linked issues, JSDoc @see tags
Questions:  "Why isn't this inlined in the parent?" "What state does this own vs receive?"
Watch for:  Re-exported barrels that obscure actual usage, prop-drilling chains
```

### Rust

```
Artifacts:  pub structs, traits, impl blocks, modules, exported functions
Consumers:  use statements, mod declarations, Cargo.toml dependencies
Intent:     doc comments with # Examples, commit messages, //! module docs
Questions:  "What does the type system NOT enforce?" "Why unsafe here?"
Watch for:  pub(crate) items with 0 cross-module users, unused trait impls
```

### .NET / C#

```
Artifacts:  Controllers, services, interfaces, DbContext, middleware, hosted services
Consumers:  using statements, DI registration in Startup/Program, [Route] attributes
Intent:     XML doc comments, linked Azure DevOps items, PR descriptions
Questions:  "Why is this middleware ordered here?" "What happens if this hosted service fails?"
Watch for:  IFoo/Foo pairs with 1 impl (ceremony without value), unused DI registrations
```

### YAML / Governance (Demerzel-style)

```
Artifacts:  Personas, policies, schemas, contracts, grammars, templates, translations
Consumers:  Cross-references in other YAML/MD/JSON, schema $ref, test suites
Intent:     Policy rationale field, constitutional_basis, version history
Questions:  "What decision does this config encode?" "Who consumes this artifact?"
Watch for:  Policies with 0 citations, schemas with 0 validators, personas with 0 tests
```

## Integration Points

- **Phase 1** delegates to `demerzel-anti-slop-docs` for slop scoring
- **F beliefs** feed into `demerzel-lolli-remediate` for ranked deletion/consolidation
- **Tetravalent logic** from `logic/tetravalent-logic.md` defines truth value semantics
- **Belief currency** from `policies/belief-currency-policy.yaml` defines staleness decay
- **Confidence thresholds** from Demerzel governance gate all actions

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Starting with code structure instead of questions | Tree-sitter is eyes, not brain. Ask "why?" before "what?" |
| Treating all U beliefs as problems | U beliefs are gold — they surface real gaps. Celebrate them. |
| Collapsing U to F silently | Unknown is not False. "We don't know" is different from "it's dead." |
| Building beliefs from slop docs | Run Phase 1 first. Slop docs produce C beliefs that waste time. |
| Ignoring git blame dates | A file untouched for 2 years with 0 consumers is F, not U. |
| Presenting C beliefs without both sides | Always show what each source claims. Let humans resolve. |
| Skipping confidence scoring | Every belief needs a number. "Probably true" is not governance. |

## Governance

- **Article 1 (Truthfulness):** Beliefs must reflect evidence, not assumptions
- **Article 2 (Transparency):** Evidence chains are mandatory — no belief without sources
- **Article 5 (Non-Deception):** U and C beliefs must be surfaced, never hidden
- **Article 6 (Escalation):** C beliefs are escalated to humans for resolution
- **Article 7 (Auditability):** Full evidence chain for every truth value assignment
- **Article 8 (Observability):** Belief counts by truth value are tracked metrics
- **Tetravalent Logic:** Never collapse U or C to binary — they demand different responses
- **Belief Currency Policy:** Beliefs decay over time; staleness triggers re-evaluation
