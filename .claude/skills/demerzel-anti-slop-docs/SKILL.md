---
name: demerzel-anti-slop-docs
description: Use when generating documentation from code structure (tree-sitter, LSP, static analysis). Prevents AI slop — docs that restate what code already says. Enforces intention over description.
---

# Anti-Slop Documentation Generator

AI doc generators produce slop: "This class represents a User" on a class named `User`. This skill enforces **articulation over description** — every doc must answer WHY, not WHAT.

## Usage

```
/demerzel anti-slop-docs [path or module]
/demerzel anti-slop-docs --mode intention|dependency-map|contract
/demerzel anti-slop-docs --lang java|typescript|rust|yaml
/demerzel anti-slop-docs --audit [path]          -- score existing docs for slop
/demerzel anti-slop-docs --strip [path]           -- remove docs that fail the 5-second rule
```

## The Core Rule

**If a senior dev could infer it in 5 seconds by reading the code, the doc is slop. Delete it.**

```
CODE STRUCTURE (tree-sitter / LSP / static analysis)
  |
  v
QUESTION GENERATION (not description generation)
  |  "Why does this exist?"
  |  "What breaks if deleted?"
  |  "What's the contract? What are the invariants?"
  |  "Who calls this and why?"
  |
  v
CROSS-REFERENCE
  |  git blame -> who wrote it, when, PR context
  |  call graph -> who consumes it, what depends on it
  |  test coverage -> what behaviors are asserted
  |
  v
SLOP DETECTION (bs-decode applied to docs)
  |  Restates signature? -> SLOP
  |  Restates field types? -> SLOP
  |  Could apply to any class? -> SLOP (specificity test)
  |  Adds nothing beyond 5-second scan? -> SLOP
  |
  v
OUTPUT (intention-doc | dependency-map | contract-spec)
```

## Slop Anti-Patterns

These patterns are ALWAYS slop. Detect and reject them:

| Anti-Pattern | Example | Why It's Slop |
|---|---|---|
| **Signature restating** | "This method takes a String name and returns a User" | The signature already says this |
| **Type narration** | "This field stores the user's email address" (on `String email`) | The type + name say this |
| **Class-name expansion** | "This class represents a User" | The class name says this |
| **Constructor narration** | "Creates a new instance of UserService" | Every constructor does this |
| **Getter/setter docs** | "Gets the name" / "Sets the name" | The method name says this |
| **Generic purpose** | "This service handles user-related operations" | Could be on any service |
| **Tautological** | "The UserRepository provides repository functionality for Users" | Zero information added |

**The Substitution Test:** Replace the subject with any other class/method/field. If the doc still makes sense, it's slop. (Same as bs-decode specificity test.)

## What Good Docs Look Like

### Instead of Description, Answer Questions

**Bad (slop):**
```java
/**
 * Service class that handles user authentication.
 * This class provides methods for login, logout, and token refresh.
 */
public class AuthService { ... }
```

**Good (intention):**
```java
/**
 * WHY: Centralizes auth because 3 microservices were each implementing
 * their own token validation with subtly different expiry logic (see incident INC-2341).
 *
 * CONTRACT: Tokens are JWTs with 15-min expiry. Refresh tokens last 7 days.
 * If the token store (Redis) is down, all auth fails closed (no silent bypass).
 *
 * BREAKS IF DELETED: LoginController, ApiGateway, and WebSocket handler
 * all depend on this. No fallback exists.
 */
public class AuthService { ... }
```

### Language-Specific Patterns

#### Java Beans / Spring Services
- Skip: field docs, getter/setter docs, constructor docs, `@Autowired` narration
- Document: WHY this bean exists (not what it does), what invariants it maintains, what breaks without it
- Key question: "Why is this a separate service and not part of [adjacent service]?"

#### TypeScript / React Components
- Skip: prop type descriptions, "renders a button" on `<Button>`
- Document: WHY this component exists separately from its parent, what state it owns vs. receives, edge cases in re-render behavior
- Key question: "Why isn't this inlined in the parent component?"

#### Rust Structs / Traits
- Skip: field type narration, "implements Display for X"
- Document: WHY this type exists (what invariant does it encode?), unsafe contracts, lifetime relationships
- Key question: "What does the type system NOT enforce that this doc must?"

#### YAML / JSON Governance Artifacts
- Skip: field descriptions that match the schema
- Document: WHY this value was chosen, what changes if you modify it, governance rationale
- Key question: "What decision does this configuration encode?"

## Output Modes

### 1. Intention Docs (`--mode intention`)

For each symbol, generate:

```
WHY:    Why does this exist? What problem triggered its creation?
BREAKS: What breaks if this is deleted or changed?
CONTRACT: What are the invariants? What does it promise callers?
HISTORY: (from git blame) Who created it, when, PR context if available
```

### 2. Dependency Maps (`--mode dependency-map`)

```
[Symbol] AuthService
  CALLED BY:
    - LoginController.authenticate() -- login flow
    - ApiGateway.validateToken()     -- every API request
    - WebSocketHandler.onConnect()   -- real-time connections
  DEPENDS ON:
    - TokenStore (Redis)             -- CRITICAL: no fallback
    - UserRepository                 -- user lookup
    - CryptoConfig                   -- signing keys
  IF DELETED:
    - 3 callers break immediately
    - No alternative auth path exists
    - Severity: CRITICAL
```

### 3. Contract Specs (`--mode contract`)

```
[Contract] AuthService.validateToken(token: String) -> AuthResult

  PRECONDITIONS:
    - token is non-null, non-empty
    - TokenStore (Redis) is reachable
  POSTCONDITIONS:
    - Returns AuthResult.valid(userId) if token is valid and not expired
    - Returns AuthResult.expired() if token was valid but expired
    - Returns AuthResult.invalid() for all other cases (never throws)
  INVARIANTS:
    - A valid token always resolves to exactly one userId
    - Expired tokens are never treated as valid (fail closed)
  SIDE EFFECTS:
    - Logs auth attempts to audit trail (async, non-blocking)
```

## Audit Mode (`--audit`)

Score existing docs for slop density. Uses bs-decode weights adapted for code docs:

| Test | Weight | What It Measures |
|---|---|---|
| Substitution | 0.25 | Could this doc apply to any other symbol? |
| 5-Second Rule | 0.25 | Could a senior dev infer this from the code alone? |
| Information Delta | 0.20 | What does the doc add beyond the signature + type? |
| Question Answering | 0.15 | Does it answer WHY, BREAKS, or CONTRACT? |
| Specificity | 0.15 | Does it name specific callers, incidents, or constraints? |

**Scoring:**
- **Clean** (> 0.8): Doc adds real value
- **Mild slop** (0.6-0.8): Some useful content buried in narration
- **Moderate slop** (0.4-0.6): More restating than informing
- **Heavy slop** (0.2-0.4): Almost entirely redundant with code
- **Pure slop** (< 0.2): Delete it; negative value (misleads into thinking docs exist)

## Strip Mode (`--strip`)

Remove docs that score below Moderate. For each stripped doc, output:

```
STRIPPED: UserService.java line 12-18
  REASON: Scored 0.15 (pure slop) — restates class name and field types
  ACTION: Deleted. The code is the documentation.
  SUGGESTION: If docs are needed here, answer: "Why is user management
              a separate service from ProfileService?"
```

## The Fundamental Principle

**Code tells you WHAT. Docs must tell you WHY.**

If a doc doesn't tell you WHY, it's noise. Noise is worse than silence because it:
1. Creates maintenance burden (docs drift from code)
2. Trains developers to ignore docs (cry wolf)
3. Gives false confidence ("we have documentation")
4. Consumes attention that could go to actual understanding

**No doc is better than a slop doc.**

## Governance

- **Article 1 (Truthfulness):** Slop docs are a form of fabrication — they present the appearance of documentation without the substance
- **Article 5 (Non-Deception):** "We have documentation" is deceptive if the docs are slop
- **BS Decode integration:** All generated docs are self-checked against the bs-decode pipeline before output
- **Completeness Instinct:** The goal is not 100% doc coverage — it's 100% intention coverage on the things that matter
