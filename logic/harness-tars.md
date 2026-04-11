# Harness Adapter Projection — tars

**Status:** Version 1.0, 2026-04-11.
**Scope:** Projection rules for `tars`'s `ComprehensiveDiagnostics`
output into `HexObservation` records.
**Implementation:** `ix/crates/ix-harness-tars`.
**Consumed by:** `ix_triage_session` via its `prior_observations`
parameter, either through the main-agent shuttle or direct CLI
composition.

## Purpose

This document specifies the **projection rules** that convert
tars's diagnostic output into the hexavalent observation substrate
defined in `logic/hex-merge.md`. The rules are governance artifacts:
changing them is a Demerzel PR with rationale, not a silent code
edit.

The companion implementation in `ix/crates/ix-harness-tars`
mechanically applies these rules and must stay in lockstep with
this document. If the two drift, this document wins.

## Input shape (from tars)

tars's `ComprehensiveDiagnostics` JSON shape is defined in
`tars/mcp-server/src/types.ts`. The fields this adapter consumes:

```typescript
{
  timestamp: Date,
  gpuInfo: GpuInfo[],
  gitHealth: GitRepositoryHealth,
  networkDiagnostics: NetworkDiagnostics,
  systemResources: SystemResourceMetrics,
  serviceHealth: ServiceHealth,
  overallHealthScore: number,  // 0-100
}
```

The adapter does NOT consume:
- `timestamp` — wall-clock time is non-deterministic; adapters
  must be pure functions of content
- `publicIpAddress`, `networkInterfaces` — PII-adjacent
- `environmentVariables` — may contain secrets

## Output shape

Each invocation produces a `Vec<HexObservation>`. Every observation
carries:

- `source = "tars"` — fixed
- `diagnosis_id = sha256(<canonical_input_bytes>)` — content hash
  of the input so two adapter runs on the same diagnosis produce
  identical IDs
- `round` — caller-supplied (required)
- `ordinal` — 0-indexed position within this projection
- `claim_key` — see §"Claim Key Derivation"
- `variant` — T/P/U/D/F/C per the rule table below
- `weight` — per the rule table below
- `evidence` — short string describing which diagnostic field fired

## Top-level health score → base observation

Every projection emits one baseline observation on
`tars_diagnosis::reliable`:

| overallHealthScore | Variant | Weight | Rationale |
|---|---|---|---|
| ≥ 90 | T | 0.9 | System verified healthy |
| 70–89 | P | 0.7 | System probably healthy |
| 50–69 | U | 0.5 | Mixed signals |
| 30–49 | D | 0.7 | Evidence leans unhealthy |
| < 30 | F | 0.9 | System verified unhealthy |

This gives downstream consumers a one-observation summary of
tars's overall confidence in the system state.

## Disk health rules

| Condition | claim_key | Variant | Weight |
|---|---|---|---|
| `diskFreeBytes < 1 GB` | `cleanup_disk::valuable` | T | 0.9 |
| `diskFreeBytes < 5 GB` AND no cleanup target | `cleanup_disk::valuable` | P | 0.7 |
| `diskUsedBytes / diskTotalBytes > 0.95` | `system_stability::safe` | D | 0.7 |
| `diskUsedBytes / diskTotalBytes > 0.98` | `system_stability::safe` | F | 0.9 |

Rationale: below 1GB free is a verified emergency — any cleanup
action is valuable. Between 1-5GB free is a warning. Above 95% used
suggests doubt about system stability; above 98% refutes it.

## GPU health rules

For each `GpuInfo` entry in `gpuInfo[]`:

| Condition | claim_key | Variant | Weight |
|---|---|---|---|
| `temperature > 85°C` | `gpu_cooling::valuable` | T | 0.9 |
| `temperature > 95°C` | `<gpu_name>::safe` | F | 1.0 |
| `utilizationGpu > 95 sustained` | `gpu_throttle::valuable` | P | 0.6 |
| `memoryUsed / memoryTotal > 0.98` | `gpu_memory::safe` | F | 0.9 |

The `<gpu_name>` placeholder is the GPU's reported name
(sanitized — spaces → underscores, lowercased). This keeps the
claim_key stable across diagnoses of the same GPU.

## Git health rules

| Condition | claim_key | Variant | Weight |
|---|---|---|---|
| `isRepository == false` | `git_init::valuable` | T | 0.9 |
| `isClean == false` AND `unstagedChanges > 100` | `git_review::valuable` | P | 0.7 |
| `behindBy > 50` | `git_pull::valuable` | P | 0.8 |
| `aheadBy > 100` AND `behindBy == 0` | `git_push::valuable` | P | 0.7 |
| `isClean == true` AND `aheadBy == 0` AND `behindBy == 0` | `git_state::reliable` | T | 0.9 |

"git_review" means "a human should look at this repo" — not a
specific git command. The claim_key vocabulary is about *intent*,
not command lines.

## Network rules

| Condition | claim_key | Variant | Weight |
|---|---|---|---|
| `isConnected == false` | `network::reliable` | F | 1.0 |
| `pingLatency > 500ms` | `network::reliable` | D | 0.6 |
| `dnsResolutionTime > 1000ms` | `dns::reliable` | D | 0.7 |
| `isConnected == true` AND `pingLatency < 50ms` | `network::reliable` | T | 0.8 |

## System resource rules

| Condition | claim_key | Variant | Weight |
|---|---|---|---|
| `cpuUsagePercent > 95 sustained` | `cpu_throttle::valuable` | P | 0.6 |
| `memoryUsedBytes / memoryTotalBytes > 0.95` | `memory_pressure::valuable` | D | 0.7 |
| `memoryUsedBytes / memoryTotalBytes > 0.98` | `system_stability::safe` | F | 0.8 |
| `processCount > 2000` | `process_audit::valuable` | P | 0.5 |

"sustained" means the tars diagnostic reports a consistently high
value. The adapter takes the reported value at face value — it
does not track multiple samples. "Sustained" here is tars's
responsibility to determine.

## Service health rules

| Condition | claim_key | Variant | Weight |
|---|---|---|---|
| `databaseConnectivity == false` | `database::reliable` | F | 1.0 |
| `webServiceAvailability == false` | `web_service::reliable` | F | 1.0 |
| `fileSystemPermissions == false` | `fs_permissions::safe` | F | 1.0 |
| All three true | `service_baseline::reliable` | T | 0.9 |

## The `reliable` aspect

This doc introduces a new aspect `reliable` not listed in the main
hex-merge.md grammar. It's reserved for "the source itself is
trustworthy" observations — distinct from `valuable` (will this
action help?), `safe` (is it blast-radius-tight?), etc.

**Semantics:** `reliable` is like `safe` but applies to observation
sources, not actions. A source with `::reliable = F` should have
its other observations treated with suspicion.

**Merge behavior:** the merge function treats `::reliable` like any
other aspect — direct contradictions and meta-conflicts fire per
the Belnap table. Future work may add a "source credibility
discount" step that scales weights by each source's own `::reliable`
observations, but that's not shipped today.

**Governance addition:** when this doc is merged, `hex-merge.md`
§"Claim Key Grammar" must be updated to add `reliable` to the
aspect enum. See the migration note at the bottom of this doc.

## Ordinal allocation

The adapter walks the rules in this document's order (top of file
to bottom) and assigns ordinals sequentially starting at 0. Rules
that don't fire don't consume an ordinal. This makes the ordinal
deterministic: the same input always produces the same ordinal
layout, so the G-Set dedup key stays stable across re-ingestions.

**Invariant:** if rule N and rule M both fire for the same input,
rule N (earlier in this doc) gets the lower ordinal.

## What the adapter does NOT emit

- No observations for `timestamp` — it's wall-clock and would break
  determinism
- No observations for `networkInterfaces` or `publicIpAddress` —
  privacy-adjacent, not governance signals
- No observations when `overallHealthScore` is 60-70 and all
  specific checks are below their thresholds — this is "nothing to
  say" and the adapter returns an empty Vec
- No observations with weight < 0.1 — below this threshold the
  signal is noise

## Example round-trip

### Input (canonical tars diagnosis)

```json
{
  "timestamp": "2026-04-11T12:00:00Z",
  "gpuInfo": [
    {
      "name": "NVIDIA RTX 5080",
      "memoryTotal": 17179869184,
      "memoryUsed": 16963547136,
      "memoryFree": 216322048,
      "temperature": 92,
      "cudaSupported": true
    }
  ],
  "gitHealth": {
    "isRepository": true,
    "currentBranch": "main",
    "isClean": false,
    "unstagedChanges": 5,
    "stagedChanges": 0,
    "commits": 1234,
    "aheadBy": 2,
    "behindBy": 0
  },
  "networkDiagnostics": {
    "isConnected": true,
    "dnsResolutionTime": 45,
    "pingLatency": 20,
    "activeConnections": 42,
    "networkInterfaces": ["eth0"]
  },
  "systemResources": {
    "cpuUsagePercent": 45,
    "cpuCoreCount": 16,
    "cpuFrequency": 3800,
    "memoryTotalBytes": 34359738368,
    "memoryUsedBytes": 16106127360,
    "memoryAvailableBytes": 18253611008,
    "diskTotalBytes": 1000000000000,
    "diskUsedBytes": 500000000000,
    "diskFreeBytes": 500000000000,
    "processCount": 432,
    "threadCount": 2100,
    "uptime": 86400
  },
  "serviceHealth": {
    "databaseConnectivity": true,
    "webServiceAvailability": true,
    "fileSystemPermissions": true,
    "environmentVariables": {},
    "portsListening": [80, 443],
    "servicesRunning": ["nginx"]
  },
  "overallHealthScore": 72
}
```

### Expected observations

Ordinal 0 — from overall health (score 72 → P, 0.7):
```json
{
  "kind": "observation_added",
  "ordinal": 0,
  "source": "tars",
  "diagnosis_id": "<sha256 of canonical input>",
  "round": <caller-supplied>,
  "claim_key": "tars_diagnosis::reliable",
  "variant": "P",
  "weight": 0.7,
  "evidence": "overall_health_score=72"
}
```

Ordinal 1 — GPU temperature 92°C (> 85 rule fires; > 95 does not):
```json
{
  "kind": "observation_added",
  "ordinal": 1,
  "source": "tars",
  "diagnosis_id": "<sha256>",
  "round": <caller>,
  "claim_key": "gpu_cooling::valuable",
  "variant": "T",
  "weight": 0.9,
  "evidence": "gpu[0].temperature=92"
}
```

Ordinal 2 — GPU memory 98.7% used (> 98% rule fires):
```json
{
  "kind": "observation_added",
  "ordinal": 2,
  "source": "tars",
  "diagnosis_id": "<sha256>",
  "round": <caller>,
  "claim_key": "nvidia_rtx_5080::safe",
  "variant": "F",
  "weight": 0.9,
  "evidence": "gpu[0] memory 98.7% used"
}
```

Ordinal 3 — Service baseline all-green:
```json
{
  "kind": "observation_added",
  "ordinal": 3,
  "source": "tars",
  "diagnosis_id": "<sha256>",
  "round": <caller>,
  "claim_key": "service_baseline::reliable",
  "variant": "T",
  "weight": 0.9,
  "evidence": "database+web+fs all healthy"
}
```

Total: 4 observations (not all rules fired).

## Migration note

Adding the `reliable` aspect requires updating `hex-merge.md`
§"Claim Key Grammar":

```
aspect := "valuable" | "safe" | "reversible" | "timely"
        | "reproducible" | "reliable"       // added 2026-04-11
        | "meta_conflict"
```

And updating `session-event.schema.json` §`observation_added` to
relax the aspect regex.

Both updates ship in the same commit as this doc so the three
artifacts stay consistent.

## Version

1.0 — 2026-04-11 — initial tars projection spec. Covers disk,
GPU, git, network, system resources, service health. Introduces
the `reliable` aspect for source credibility signals.
