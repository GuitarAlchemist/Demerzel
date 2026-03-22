# Hyperlight Micro-VM Research: ix Pipeline Sandboxing

**Cycle:** hyperlight-ix-sandboxing-2026-03-22
**Issue:** #101
**Researcher:** Seldon (knowledge transfer specialist)
**Belief:** T (True), confidence: 0.78
**Date:** 2026-03-22

---

## Research Question

Can Hyperlight micro-VMs sandbox individual Forge pipeline steps in ix, providing
Article 3 (Reversibility) guarantees by isolating each step in its own VM with no
side-effect leakage?

---

## What Is Hyperlight?

Hyperlight is a CNCF Sandbox project (Microsoft, 2024) providing **lightweight virtual
machine isolation for short-running functions** without a full operating system or kernel.

Key architectural properties:
- No OS kernel inside the VM — bare vCPU + mapped memory only
- Hypervisor-native isolation: KVM (Linux), mshv (Azure Linux), WHP (Windows 11 / Server 2022+)
- Guest binaries are PE (Windows) or ELF (Linux) — no container runtime, no libc required
- Capability-based security: guests may only call host functions **explicitly registered** by the host
- Designed for sub-100ms (ideally sub-10ms) isolation of untrusted compute

---

## Actual Benchmark Numbers

The task description estimated "1-2ms" sandbox creation. Benchmarks from the official
Hyperlight repository (`src/hyperlight_host/benches/benchmarks.rs`, Criterion, release build,
Linux KVM) show:

| Sandbox size | Heap | Creation latency |
|---|---|---|
| Default | ~16MB | ~34-35ms |
| Small | 8MB | ~33ms |
| Medium | 64MB | ~36ms |
| Large | 256MB | ~38ms |

**The 1-2ms figure is incorrect for sandbox creation.** It may refer to guest function
*call overhead* (microseconds) once a sandbox is already initialized, not initialization
itself. Microsoft documentation notes sandbox creation as "fast" relative to full VMs
(seconds) — the comparison class is container startup, not native function calls.

**Implication for ix:** If Forge pipeline steps are long-running (>100ms of work), the
~35ms overhead is acceptable (10-25% overhead). For sub-millisecond pipeline steps, it is
prohibitive. Step granularity must be designed around this constraint.

---

## Rust Host API Pattern

The Hyperlight Rust API (`hyperlight_host` crate) follows an **evolve** pattern:

```rust
use hyperlight_host::{
    GuestBinary, UninitializedSandbox, MultiUseSandbox, SandboxRunOptions,
};

// 1. Create uninitialized sandbox (this is where the ~35ms is spent)
let mut uninit = UninitializedSandbox::new(
    GuestBinary::FilePath(guest_binary_path),
    None,  // optional SandboxRunOptions
)?;

// 2. Register host functions the guest is allowed to call
uninit.register("HostLog", |msg: String| -> Result<(), Error> {
    tracing::info!(msg);
    Ok(())
})?;

uninit.register("HostEmitMetric", |key: String, val: f64| -> Result<(), Error> {
    metrics::emit(key, val);
    Ok(())
})?;

// 3. Evolve to multi-use sandbox (callable state)
let mut sandbox: MultiUseSandbox = uninit.evolve()?;

// 4. Call guest functions (microsecond overhead per call)
let result = sandbox.call::<i32>("RunPipelineStep", input_bytes)?;

// 5. VM is dropped when sandbox goes out of scope — no cleanup needed
```

**Guest languages: Rust and C only.** No WebAssembly, no JavaScript, no Python. Guest
code must be compiled to a native binary that runs without OS system calls.

---

## Feasibility Assessment for ix Forge Pipeline

### What Hyperlight Provides

| Guarantee | Provided? | Notes |
|---|---|---|
| Memory isolation | Yes | Each sandbox has its own address space |
| No filesystem access | Yes (by default) | Guest cannot open files; host must proxy |
| No network access | Yes (by default) | Guest cannot make syscalls |
| Capability-based host calls | Yes | Host registers only safe functions |
| Reversibility (Article 3) | **Yes** | VM destruction = complete rollback, no residue |
| Determinism | Yes | No ambient state leaks between runs |
| Rust-native integration | Yes | First-class Rust crate, ergonomic API |

### What Hyperlight Does NOT Provide

| Gap | Impact |
|---|---|
| Guest must be Rust or C | Pipeline step logic must be compiled, not scripted |
| No shared memory between steps | Inter-step data must pass through host serialization |
| ~35ms init cost per step | Fine for heavy steps; prohibitive for lightweight ops |
| No filesystem in guest | Forge steps that read/write files need host proxy functions |
| Windows WHP support | Requires Windows 11 or Server 2022+ — older Windows unsupported |

### Article 3 (Reversibility) Alignment

Hyperlight is an exceptionally strong fit for Article 3:

> **Article 3: Prefer actions that can be undone.**

Each pipeline step runs in a VM that is **destroyed after the step completes**. Any
mutations the guest makes to its own memory are gone. The host controls what side effects
escape via registered functions — making side-effect surfaces explicit and auditable.

This is a stronger reversibility guarantee than:
- Docker containers (filesystem layers persist)
- Process isolation (shared memory segments can leak)
- Thread isolation (global state is shared)

---

## Prototype Architecture for ix

### Concept: Forge-in-VM

Each Forge pipeline step (`ForgeStep`) becomes a compiled guest binary. ix's host process
manages the sandbox lifecycle:

```
ix host process
├── ForgeRunner
│   ├── load_guest_binary(step_type) → GuestBinary
│   ├── create_sandbox() → UninitializedSandbox   [~35ms]
│   ├── register_host_fns()                        [<1ms]
│   │   ├── emit_belief(belief_json)
│   │   ├── emit_metric(key, value)
│   │   ├── log(level, message)
│   │   └── read_input_chunk(offset, len) → bytes
│   ├── evolve() → MultiUseSandbox               [<1ms]
│   ├── call("RunStep", input_bytes) → output     [step time]
│   └── drop(sandbox)                             [instant cleanup]
```

### Guest Binary Interface

```rust
// Compiled as hyperlight guest (no std, no OS)
#[no_mangle]
pub extern "C" fn RunStep(input_ptr: *const u8, input_len: usize) -> i32 {
    let input = unsafe { slice::from_raw_parts(input_ptr, input_len) };
    let step_input: StepInput = bincode::deserialize(input)?;

    // Process using only registered host calls
    host_log("info", "step starting");
    let result = process(step_input);
    host_emit_belief(&result.belief_json);

    0 // success
}
```

### Pipeline Composition

```ixql
-- IxQL representation of sandboxed pipeline
FORGE_PIPELINE "melody-analysis" {
  isolation: hyperlight,
  steps: [
    STEP "pitch-extract" { binary: "forge-pitch-extract.elf" },
    STEP "interval-classify" { binary: "forge-interval-classify.elf" },
    STEP "pattern-detect" { binary: "forge-pattern-detect.elf" }
  ],
  reversibility: full  -- each step VM-isolated, no state escapes
} -> BELIEF_STATE "analysis/{run_id}"
```

---

## Integration Path

### Phase 1 — Feasibility Spike (1-2 weeks)
1. Add `hyperlight-host` to ix Cargo.toml
2. Compile one existing Forge step (e.g., pitch extraction) as a Hyperlight guest
3. Benchmark actual step latency including sandbox init overhead
4. Verify memory limits are compatible with ix's data volumes

### Phase 2 — Host Integration (2-3 weeks)
5. Build `ForgeRunner` struct with sandbox lifecycle management
6. Define host function registry (belief emission, metrics, logging)
7. Add serialization layer (bincode or flatbuffers) for inter-step data

### Phase 3 — IxQL Pipeline Integration (1-2 weeks)
8. Add `isolation: hyperlight` field to IxQL FORGE_PIPELINE expression
9. IxQL executor spawns `ForgeRunner` per step
10. Cycle logs record isolation mode and reversibility guarantee

---

## Key Risks

| Risk | Severity | Mitigation |
|---|---|---|
| ~35ms overhead per step | Medium | Batch work inside steps; don't over-fragment |
| Guest Rust/C only | Low | ix Forge steps are already Rust |
| WHP Windows version requirement | Low | ix targets Linux/Azure primarily |
| Guest binary compilation complexity | Medium | Establish guest SDK with shared types |
| Hyperlight CNCF Sandbox status | Low | CNCF Sandbox = early adoption risk; Microsoft-backed |

---

## Cross-Model Validation

| Source | Finding | Agreement |
|---|---|---|
| Hyperlight GitHub repository (primary) | Sandbox init ~34-35ms (Criterion benchmarks); Rust/C guests; capability-based | Authoritative |
| Hyperlight execution details doc | No OS kernel; bare vCPU + shared memory; PE/ELF binaries | Confirms primary |
| Hyperlight benchmarking doc | Daily benchmarks tracked; regression detection per release | Confirms primary |
| Task description estimate ("1-2ms") | Contradicts measured benchmark data | **Corrected** |

Belief: **T (True)**, confidence: **0.78**

- Hyperlight is technically feasible for ix Forge step isolation
- Article 3 (Reversibility) guarantee is strong — VM destruction = complete rollback
- The 1-2ms latency claim in the task description is incorrect; actual is ~35ms for init
- Rust-native integration is first-class with ergonomic `hyperlight_host` crate
- Confidence below 0.85 because: (1) no ix-specific prototype built yet, (2) Hyperlight is
  CNCF Sandbox status (early-stage), (3) actual per-step overhead in music domain workloads
  not measured

---

## Recommendation

**Proceed with Phase 1 spike in ix.** Hyperlight's isolation model is an excellent fit for
ix Forge pipeline governance:

- Capability-based host registration = explicit side-effect audit surface
- VM destruction on step completion = strongest available reversibility guarantee
- Rust-native = no FFI friction for ix's existing codebase
- IxQL can express isolation mode as a typed pipeline property

The ~35ms initialization cost is manageable if pipeline steps are granular enough to
represent meaningful units of work (>100ms execution time). Fine-grained sub-millisecond
steps should remain in-process.

---

## IxQL Finding

```ixql
-- Research finding: Can Hyperlight micro-VMs sandbox ix Forge pipeline steps?
-- Belief: T, confidence: 0.78, cycle: hyperlight-ix-sandboxing-2026-03-22
RESEARCH_FINDING {
  department: "data-visualization",
  question: "Can Hyperlight micro-VMs provide Article 3 (Reversibility) isolation for ix Forge pipeline steps?",
  conclusion: "Yes — Hyperlight provides VM-level isolation with ~35ms init cost (not 1-2ms as claimed). Rust-native API. Guest limited to Rust/C. Article 3 strongly satisfied: VM destruction = complete rollback.",
  evidence: [
    "Hyperlight Criterion benchmarks: sandbox creation ~34-35ms (release, Linux KVM)",
    "Capability-based host function registration = explicit side-effect surface",
    "UninitializedSandbox.evolve() pattern is ergonomic Rust API",
    "CNCF Sandbox project, Microsoft-backed, KVM/mshv/WHP hypervisor support"
  ],
  belief: { value: "T", confidence: 0.78 },
  course_produced: false,
  grammar_evolved: false
} -> KNOWLEDGE_STATE "data-visualization/findings/hyperlight-ix-sandboxing-2026-03-22"
```
