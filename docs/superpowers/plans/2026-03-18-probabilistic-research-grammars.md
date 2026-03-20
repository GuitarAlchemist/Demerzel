# Probabilistic Research Grammars — Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Implement a universal scientific method PCFG for Streeling University departments with per-department learned weights, autoresearch loops, and Kuhnian paradigm detection.

**Architecture:** Three-layer system spanning three repos. Layer 1 (grammar + schemas) in Demerzel as governance artifacts. Layer 2 (research cycle executor) in TARS as F# code extending WeightedGrammar. Layer 3 (anomaly clustering + weight evolution) in ix as Rust code extending ix-governance.

**Tech Stack:** EBNF grammars, JSON Schema, F# (TARS WeightedGrammar), Rust (ix-governance), Demerzel state/ persistence.

**Spec:** `docs/superpowers/specs/2026-03-18-probabilistic-research-grammars-design.md`

---

## Task Group A: Demerzel Governance Artifacts (no runtime code)

### Task 1: Scientific Method Grammar

**Files:**
- Create: `grammars/scientific-method.ebnf`

- [ ] **Step 1: Create grammars directory and EBNF file**

```ebnf
(* Universal Scientific Method Grammar — Streeling University *)
(* Each production carries a per-department probability weight *)
(* Governance artifact — consumed by TARS WeightedGrammar *)

investigation ::= observe hypothesize predict test conclude reflect
                | observe hypothesize test conclude reflect
                | observe analogize transfer validate reflect

hypothesize ::= inductive | deductive | abductive | analogical | combinatorial

test ::= empirical | formal_proof | simulation | thought_experiment | cross_validation | adversarial

conclude ::= confirm | refute | insufficient | contradictory | revise | discover_question

reflect ::= normal_progress | anomaly_detected | paradigm_tension | paradigm_shift
```

- [ ] **Step 2: Commit**

```bash
git add grammars/scientific-method.ebnf
git commit -m "feat: Universal scientific method EBNF grammar for Streeling University"
```

### Task 2: Research Weight Profile Schema

**Files:**
- Create: `schemas/research-weights.schema.json`

- [ ] **Step 1: Create JSON Schema for department weight profiles**

The schema defines: department name, grammar version, hypothesis weights (5 productions summing to ~1.0), test weights (6 productions summing to ~1.0), metadata (last_updated, cycle_count, total_T, total_F, total_U, total_C).

- [ ] **Step 2: Commit**

```bash
git add schemas/research-weights.schema.json
git commit -m "feat: JSON schema for per-department research weight profiles"
```

### Task 3: Initial Weight Profiles for 10 Departments

**Files:**
- Create: `state/streeling/departments/music.weights.json`
- Create: `state/streeling/departments/guitar-studies.weights.json`
- Create: `state/streeling/departments/musicology.weights.json`
- Create: `state/streeling/departments/mathematics.weights.json`
- Create: `state/streeling/departments/physics.weights.json`
- Create: `state/streeling/departments/computer-science.weights.json`
- Create: `state/streeling/departments/product-management.weights.json`
- Create: `state/streeling/departments/futurology.weights.json`
- Create: `state/streeling/departments/philosophy.weights.json`
- Create: `state/streeling/departments/cognitive-science.weights.json`

- [ ] **Step 1: Create weight files with initial distributions from spec**

Each file follows `research-weights.schema.json`. Use the initial weight table from the design spec. Set `cycle_count: 0`, `total_T/F/U/C: 0`.

- [ ] **Step 2: Commit**

```bash
git add state/streeling/departments/*.weights.json
git commit -m "feat: Initial weight profiles for 10 Streeling departments"
```

### Task 4: Research Cycle Log Schema

**Files:**
- Create: `schemas/research-cycle.schema.json`

- [ ] **Step 1: Create JSON Schema for research cycle logs**

Required fields: `cycle_id`, `department`, `question`, `production_path` (array of production names sampled), `hypothesis`, `test_method`, `evidence`, `conclusion` (enum: confirm/refute/insufficient/contradictory/revise/discover_question), `belief_produced` (tetravalent value + confidence), `duration_seconds`, `timestamp`.

- [ ] **Step 2: Commit**

```bash
git add schemas/research-cycle.schema.json
git commit -m "feat: JSON schema for research cycle logs"
```

### Task 5: Anomaly Entry Schema

**Files:**
- Create: `schemas/research-anomaly.schema.json`

- [ ] **Step 1: Create JSON Schema for anomaly entries**

Required fields: `anomaly_id`, `cycle_id`, `department`, `production_path`, `hypothesis`, `failure_mode`, `domain_context` (array), `severity` (0.0-1.0), `timestamp`. Optional: `cluster_id` (assigned by ix during Tier 2 analysis), `paradigm_state` (enum: normal/watch/tension/crisis).

- [ ] **Step 2: Create research state directory**

```bash
mkdir -p state/streeling/research
```

- [ ] **Step 3: Commit**

```bash
git add schemas/research-anomaly.schema.json state/streeling/research/
git commit -m "feat: Research anomaly schema + research state directory"
```

---

## Task Group B: TARS Research Cycle Executor (F#)

### Task 6: ResearchTypes.fs — Domain Types

**Files:**
- Create: `v2/src/Tars.Evolution/ResearchTypes.fs`
- Modify: `v2/src/Tars.Evolution/Tars.Evolution.fsproj` (add Compile Include after WeightedGrammar.fs)

- [ ] **Step 1: Define research domain types**

```fsharp
namespace Tars.Evolution

module ResearchTypes =

    type HypothesisMethod = Inductive | Deductive | Abductive | Analogical | Combinatorial

    type TestMethod = Empirical | FormalProof | Simulation | ThoughtExperiment | CrossValidation | Adversarial

    type Conclusion = Confirm | Refute | Insufficient | Contradictory | Revise | DiscoverQuestion

    type ReflectionOutcome = NormalProgress | AnomalyDetected | ParadigmTension | ParadigmShift

    type TetraValue = T | F | U | C

    type ProductionPath = {
        HypothesisMethod: HypothesisMethod
        TestMethod: TestMethod
        Conclusion: Conclusion
        Reflection: ReflectionOutcome
    }

    type ResearchCycleResult = {
        CycleId: string
        Department: string
        Question: string
        Path: ProductionPath
        Hypothesis: string
        Evidence: string list
        BeliefValue: TetraValue
        BeliefConfidence: float
        DurationSeconds: int
        Timestamp: System.DateTime
    }

    type DepartmentWeights = {
        Department: string
        HypothesisWeights: Map<HypothesisMethod, float>
        TestWeights: Map<TestMethod, float>
        CycleCount: int
        LastUpdated: System.DateTime
    }

    type AnomalyEntry = {
        AnomalyId: string
        CycleId: string
        Department: string
        ProductionPath: string list
        Hypothesis: string
        FailureMode: string
        DomainContext: string list
        Severity: float
        ClusterId: string option
        ParadigmState: string
    }
```

- [ ] **Step 2: Add to fsproj after WeightedGrammar.fs**

```xml
<Compile Include="ResearchTypes.fs" />
```

- [ ] **Step 3: Build to verify**

```bash
cd v2 && dotnet build src/Tars.Evolution/Tars.Evolution.fsproj
```

- [ ] **Step 4: Commit**

```bash
git add v2/src/Tars.Evolution/ResearchTypes.fs v2/src/Tars.Evolution/Tars.Evolution.fsproj
git commit -m "feat: Research domain types for Streeling scientific method"
```

### Task 7: ResearchWeights.fs — Weight Loading and Bayesian Updates

**Files:**
- Create: `v2/src/Tars.Evolution/ResearchWeights.fs`
- Modify: `v2/src/Tars.Evolution/Tars.Evolution.fsproj` (add after ResearchTypes.fs)

- [ ] **Step 1: Implement weight loading from Demerzel state/**

```fsharp
namespace Tars.Evolution

/// Load, save, and update per-department research weight profiles.
/// Reads from Demerzel's state/streeling/departments/{dept}.weights.json.
/// Uses WeightedGrammar.bayesianUpdate for weight evolution.
module ResearchWeights =

    open System
    open System.IO
    open System.Text.Json
    open ResearchTypes

    // DTO for JSON serialization
    type WeightProfileDto = { ... }

    /// Load department weights from Demerzel state directory
    let load (stateDir: string) (department: string) : Result<DepartmentWeights, string>

    /// Save updated weights back to Demerzel state directory
    let save (stateDir: string) (weights: DepartmentWeights) : Result<unit, string>

    /// Sample a hypothesis method weighted by department profile
    let sampleHypothesis (weights: DepartmentWeights) (rng: Random) : HypothesisMethod

    /// Sample a test method weighted by department profile
    let sampleTest (weights: DepartmentWeights) (rng: Random) : TestMethod

    /// Update weights after observing a research cycle outcome
    let updateFromOutcome (weights: DepartmentWeights) (path: ProductionPath) (success: bool) : DepartmentWeights
```

Implementation uses `WeightedGrammar.softmax` for sampling and `WeightedGrammar.bayesianUpdate` for weight evolution.

- [ ] **Step 2: Add to fsproj**
- [ ] **Step 3: Build to verify**
- [ ] **Step 4: Commit**

```bash
git commit -m "feat: Research weight loading, sampling, and Bayesian update"
```

### Task 8: ResearchCycle.fs — Autoresearch Loop Executor

**Files:**
- Create: `v2/src/Tars.Evolution/ResearchCycle.fs`
- Modify: `v2/src/Tars.Evolution/Tars.Evolution.fsproj` (add after ResearchWeights.fs)

- [ ] **Step 1: Implement the research cycle executor**

```fsharp
namespace Tars.Evolution

/// Executes a single research cycle following the scientific method grammar.
/// Samples a production path from department weights, executes each step,
/// produces a tetravalent belief, updates weights, logs the cycle.
module ResearchCycle =

    open System
    open ResearchTypes

    type CycleConfig = {
        Department: string
        StateDir: string          // Path to Demerzel state/
        MaxDurationSeconds: int   // Budget per cycle (default 300 = 5 min)
        MaxCycles: int            // Max cycles per session (default 12)
    }

    /// Execute a single research cycle
    let executeCycle
        (config: CycleConfig)
        (question: string)
        (weights: DepartmentWeights)
        (rng: Random)
        : Async<Result<ResearchCycleResult * DepartmentWeights, string>>

    /// Run a full autoresearch session (up to maxCycles)
    let runSession
        (config: CycleConfig)
        (questions: string list)
        : Async<ResearchCycleResult list * DepartmentWeights>

    /// Log a research cycle result to state/streeling/research/
    let logCycle (stateDir: string) (result: ResearchCycleResult) : Result<unit, string>

    /// Check if a cycle result is an anomaly and log it
    let checkAnomaly (stateDir: string) (result: ResearchCycleResult) : AnomalyEntry option
```

The `executeCycle` function:
1. Samples `HypothesisMethod` from weights
2. Samples `TestMethod` from weights
3. Executes the path (placeholder — later wired to LLM + MCP)
4. Determines conclusion based on outcome
5. Maps conclusion to tetravalent value
6. Updates weights via `ResearchWeights.updateFromOutcome`
7. Logs to state directory
8. Checks for anomaly (F/U/C outcomes)

- [ ] **Step 2: Add to fsproj**
- [ ] **Step 3: Build to verify**
- [ ] **Step 4: Commit**

```bash
git commit -m "feat: Research cycle executor — autoresearch loop for Streeling departments"
```

### Task 9: Research Cycle Tests

**Files:**
- Create: `v2/tests/Tars.Tests/ResearchCycleTests.fs`
- Modify: `v2/tests/Tars.Tests/Tars.Tests.fsproj` (add Compile Include)

- [ ] **Step 1: Write tests**

```fsharp
module Tars.Tests.ResearchCycleTests

open Xunit
open Tars.Evolution.ResearchTypes
open Tars.Evolution.ResearchWeights
open Tars.Evolution.ResearchCycle

[<Fact>]
let ``sampleHypothesis respects weight distribution`` () = ...

[<Fact>]
let ``updateFromOutcome increases weight for successful method`` () = ...

[<Fact>]
let ``updateFromOutcome decreases weight for failed method`` () = ...

[<Fact>]
let ``checkAnomaly flags F and C outcomes`` () = ...

[<Fact>]
let ``checkAnomaly ignores T outcomes`` () = ...

[<Fact>]
let ``weights normalize after update`` () = ...

[<Fact>]
let ``cycle result maps confirm to T`` () = ...

[<Fact>]
let ``cycle result maps contradictory to C`` () = ...
```

- [ ] **Step 2: Run tests**

```bash
cd v2 && dotnet test tests/Tars.Tests/ --filter "ResearchCycle"
```

- [ ] **Step 3: Commit**

```bash
git commit -m "test: Research cycle tests — weight sampling, Bayesian update, anomaly detection"
```

---

## Task Group C: ix Anomaly Clustering + Weight Evolution (Rust)

### Task 10: research_anomaly.rs — Anomaly Clustering Module

**Files:**
- Create: `crates/ix-governance/src/research_anomaly.rs`
- Modify: `crates/ix-governance/src/lib.rs` (add module + re-export)

- [ ] **Step 1: Implement anomaly clustering**

```rust
//! Research anomaly clustering for Streeling paradigm detection.
//!
//! Reads anomaly entries from Demerzel state/streeling/research/,
//! clusters by production path similarity and domain context overlap,
//! and detects paradigm tension signals.

use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ResearchAnomaly {
    pub anomaly_id: String,
    pub cycle_id: String,
    pub department: String,
    pub production_path: Vec<String>,
    pub hypothesis: String,
    pub failure_mode: String,
    pub domain_context: Vec<String>,
    pub severity: f64,
    pub cluster_id: Option<String>,
    pub paradigm_state: String,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct AnomalyCluster {
    pub cluster_id: String,
    pub department: String,
    pub anomalies: Vec<String>,  // anomaly_ids
    pub shared_path: Vec<String>,
    pub shared_context: Vec<String>,
    pub avg_severity: f64,
    pub paradigm_state: String,  // normal/watch/tension/crisis
}

pub struct AnomalyClusterer;

impl AnomalyClusterer {
    /// Cluster anomalies by production path and domain context similarity
    pub fn cluster(anomalies: &[ResearchAnomaly]) -> Vec<AnomalyCluster>

    /// Detect paradigm state from cluster analysis
    pub fn detect_paradigm_state(clusters: &[AnomalyCluster]) -> ParadigmAssessment

    /// Read anomaly files from state directory
    pub fn read_anomalies(state_dir: &std::path::Path, department: &str) -> Vec<ResearchAnomaly>
}
```

Clustering algorithm: group by (department, shared production path elements >= 2, domain context overlap >= 1). Paradigm state rules from design spec escalation ladder.

- [ ] **Step 2: Register module in lib.rs**
- [ ] **Step 3: Add tests (6 tests: empty, single anomaly, cluster detection, tension threshold, crisis threshold, cross-department)**
- [ ] **Step 4: Run tests**

```bash
cargo test -p ix-governance --lib
```

- [ ] **Step 5: Commit**

```bash
git commit -m "feat: Research anomaly clustering for Streeling paradigm detection"
```

### Task 11: weight_evolution.rs — ML-Driven Weight Training

**Files:**
- Create: `crates/ix-governance/src/weight_evolution.rs`
- Modify: `crates/ix-governance/src/lib.rs` (add module + re-export)

- [ ] **Step 1: Implement weight evolution training**

```rust
//! Weight evolution for Streeling department research grammars.
//!
//! Trains on accumulated (production_path, outcome) pairs to predict
//! which production sequences succeed in each department.

use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ResearchOutcome {
    pub department: String,
    pub hypothesis_method: String,
    pub test_method: String,
    pub success: bool,  // T with confidence >= 0.7
    pub confidence: f64,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct WeightRecommendation {
    pub department: String,
    pub hypothesis_weights: Vec<(String, f64)>,
    pub test_weights: Vec<(String, f64)>,
    pub confidence: f64,
    pub training_samples: usize,
    pub recommendation: String,
}

pub struct WeightEvolver;

impl WeightEvolver {
    /// Train on accumulated research outcomes, produce weight recommendations
    pub fn train(outcomes: &[ResearchOutcome]) -> Vec<WeightRecommendation>

    /// Read research cycle logs from state directory
    pub fn read_outcomes(state_dir: &std::path::Path, department: &str) -> Vec<ResearchOutcome>

    /// Detect cross-department transfer opportunities
    pub fn detect_transfers(recommendations: &[WeightRecommendation]) -> Vec<TransferOpportunity>
}
```

Training: frequency-weighted success rates per production per department. Transfer detection: find departments where similar production paths have significantly different success rates.

- [ ] **Step 2: Register module in lib.rs**
- [ ] **Step 3: Add tests (5 tests: empty, single outcome, weight computation, transfer detection, serde roundtrip)**
- [ ] **Step 4: Run tests**

```bash
cargo test -p ix-governance --lib
```

- [ ] **Step 5: Commit**

```bash
git commit -m "feat: Weight evolution training for Streeling department research grammars"
```

---

## Task Group D: Integration + Push

### Task 12: Push All Repos

- [ ] **Step 1: Push Demerzel** (grammars, schemas, weight profiles)

```bash
cd Demerzel && git push origin master
```

- [ ] **Step 2: Push TARS** (ResearchTypes, ResearchWeights, ResearchCycle, tests)

```bash
cd tars && git push origin main
```

- [ ] **Step 3: Push ix** (research_anomaly, weight_evolution)

```bash
cd ix && git push origin main
```

### Task 13: Update Demerzel Wiki

- [ ] **Step 1: Add Research-Grammars wiki page**

Document the scientific method grammar, weight profiles, autoresearch loop, and paradigm detection. Link to source files.

- [ ] **Step 2: Update Streeling-University wiki page**

Add section on research methodology and link to Research-Grammars page.

- [ ] **Step 3: Push wiki**

---

## Execution Notes

- **Task Groups A, B, C are independent** — can be parallelized via subagents
- Group A (Demerzel) has no build step — pure governance artifacts
- Group B (TARS) depends on WeightedGrammar.fs existing (it does)
- Group C (ix) depends on ix-governance crate existing (it does)
- Group D depends on A+B+C completing
- Total new files: 15 (5 Demerzel schemas/grammars, 10 weight profiles, 3 TARS F# modules, 1 test file, 2 ix Rust modules)
