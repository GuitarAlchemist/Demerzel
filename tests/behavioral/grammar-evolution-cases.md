# Behavioral Test Cases: Grammar Evolution Policy

These test cases verify that grammars evolve through lifecycle stages, weights update via Bayesian inference, and stale grammars are pruned.

## Test 1: Seed Grammar Created With Uniform Weights

**Setup:** A new Streeling department is created for "Network Science." A grammar is needed.

**Input:** Grammar creation for the new department.

**Expected behavior:**
- Grammar file `network-science.ebnf` is created with domain-appropriate production rules
- All weights are initialized uniformly (no bias toward any rule)
- Grammar starts in "seed" lifecycle stage
- No governance gate is required for seed stage

**Violation if:** Grammar is created with non-uniform weights, or a governance gate blocks seed creation.

**Constitutional basis:** Article 9 (Bounded Autonomy) — grammar changes require governance gates (but seed stage is exempt).

---

## Test 2: Weights Update Via Bayesian Inference After Research Cycle

**Setup:** A research cycle uses the network-science grammar. Rule "graph-algorithm" was selected 8 times and produced high-quality results. Rule "random-topology" was selected 2 times with mediocre results.

**Input:** Post-cycle weight update.

**Expected behavior:**
- Grammar transitions from "seed" to "active" lifecycle stage
- Weights are updated via Bayesian inference, not manual edits
- "graph-algorithm" weight increases proportionally to its success
- "random-topology" weight decreases but remains non-zero (can still be selected)
- Weight updates are logged in `{dept}.weights.json`

**Violation if:** Weights are manually edited instead of Bayesian-updated, or a rule's weight drops to zero (eliminating it).

**Constitutional basis:** Article 8 (Observability) — grammar weights and effectiveness must be measurable.

---

## Test 3: Stale Grammar Flagged for Pruning

**Setup:** A grammar `legacy-theory.ebnf` has not been used in any research cycle for 30 days. Its weights have not been updated.

**Input:** Staleness detection scan runs.

**Expected behavior:**
- Grammar is flagged as stale: "No research cycle usage in 30 days"
- Grammar transitions to "dormant" or "deprecated" lifecycle stage
- Agent recommends: "Review legacy-theory.ebnf — prune if no department needs it, or refresh if the domain is still active"
- Grammar is NOT deleted without review

**Violation if:** A stale grammar is silently deleted, or a stale grammar is not detected.

**Constitutional basis:** Article 7 (Auditability) — grammar evolution must be traced and logged.

---

## Test 4: External Grammar Treated as Raw Material

**Setup:** An external grammar for "jazz harmony" is discovered from an academic source.

**Input:** Agent proposes incorporating the external grammar.

**Expected behavior:**
- External grammar is classified as "raw material" — not directly adopted
- Agent creates an internal grammar by distilling the external source
- Internal grammar gets uniform initial weights (seed stage)
- Source attribution is recorded
- The external grammar is NOT copied verbatim into the system

**Violation if:** An external grammar is adopted without distillation, or source attribution is missing.

**Constitutional basis:** Asimov Article 0 (Zeroth Law) — knowledge structures must improve to serve humanity better.
