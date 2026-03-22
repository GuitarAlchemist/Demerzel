# Meta-Recognition Engine — Design Specification

**Date:** 2026-03-24
**Status:** Draft
**Scope:** Demerzel (policy, schema, driver integration) + tars (pattern detectors)
**Issue:** #112

## Overview

A RECON sub-phase that detects meta-opportunities: situations where the system should not just fix or build something, but fix or build *the system that fixes or builds things*. The engine scans git history, evolution logs, conscience signals, state artifacts, and cross-repo patterns to produce ranked proposals with confidence scores.

This is second-order cybernetics applied to governance: the observer (Demerzel) observing her own observation process and recognizing when that process itself should change.

## Design Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Where in cycle | RECON Stage 3 (Analyze) sub-phase | Pattern detection requires enriched data from Stages 1-2 |
| Output format | Proposals with FuzzyEnum confidence | Consistent with belief system; enables threshold gating |
| Detector architecture | Independent detectors, shared scoring | Each detector is a pure function; composable and testable |
| Action routing | Proposal → skill mapping | Detectors don't execute; they produce typed proposals for PLAN |
| State persistence | state/meta-recognition/ | Proposals persist across cycles for trend detection |

## The Five Detectors

Each detector scans a specific signal class and produces proposals of a specific type.

### Detector 1: Repetition → MetaFix

**Signal:** The same class of problem recurs across time or repos.

**Inputs:**
- `git log` — commit messages matching `fix:` pattern
- `state/conscience/signals/` — recurring discomfort themes
- `state/conscience/patterns/` — patterns with `occurrence_count > 2`
- `state/manifests/` — tasks of the same category across cycles

**Detection rules:**
- 3+ fix commits with semantically similar descriptions within 30 days
- Conscience pattern with `status: active` and `occurrence_count >= 3`
- Same task category appearing in 3+ consecutive cycle manifests
- Same anti-pattern detected by staleness-detection in 2+ consecutive scans

**Output:**
```yaml
type: metafix
detector: repetition
target: "description of what keeps recurring"
evidence:
  - source: git_log | conscience | manifest | staleness
    detail: "specific evidence"
    timestamp: "ISO-8601"
confidence: 0.0-1.0  # higher = more evidence of repetition
proposed_action: "/demerzel metafix [description]"
proposed_level: 2-4   # suggested minimum metafix level
```

**Confidence calculation:**
- Base: 0.3 (3 occurrences) + 0.1 per additional occurrence (cap 0.9)
- Boost: +0.1 if cross-repo (same pattern in ix + tars or ga)
- Boost: +0.1 if conscience signal exists for same pattern
- Penalty: -0.2 if last occurrence > 14 days ago (may be resolved)

### Detector 2: Template → MetaBuild

**Signal:** Manual creation of artifacts that follow an existing template pattern.

**Inputs:**
- `git log` — commit messages with `feat:` adding new departments, grammars, personas, courses
- File structure analysis — new directories matching existing patterns
- `state/streeling/departments/` — departments created without metabuild
- `grammars/` — grammars created manually vs via metabuild

**Detection rules:**
- New artifact follows >80% structural similarity to an existing artifact of the same type
- Manual creation of something metabuild can already produce (commit lacks "via metabuild")
- 3+ artifacts of the same type created in a session without a factory
- New artifact type that doesn't have a metabuild factory yet but has 3+ instances

**Output:**
```yaml
type: metabuild
detector: template
target: "what should be templatized or factory-produced"
evidence:
  - source: git_log | structure | pattern
    detail: "specific evidence"
    timestamp: "ISO-8601"
confidence: 0.0-1.0
proposed_action: "/demerzel metabuild --{type} [description]"
proposed_factory: "existing factory to use, or 'new' if none exists"
```

**Confidence calculation:**
- Base: 0.4 (structural similarity detected)
- Boost: +0.2 if 3+ instances exist without factory
- Boost: +0.1 per additional instance beyond 3
- Boost: +0.1 if a metabuild factory already exists for this type
- Penalty: -0.2 if instances differ significantly (>30% structural variance)

### Detector 3: Drift → MetaSync

**Signal:** State, artifacts, or cross-repo contracts are diverging from their source of truth.

**Inputs:**
- `state/driver/health-scores.json` — `submodule_currency` and `governance_coverage`
- Cross-repo contract versions vs local copies
- `state/evolution/` — artifact versions vs deployed versions
- `state/beliefs/` — beliefs cited in decisions but not recently validated
- Galactic Protocol compliance reports

**Detection rules:**
- Submodule drift > 5 commits behind
- Contract version mismatch between Demerzel and consumer repo
- Belief cited in last 7 days of decisions but not re-evaluated in 14 days
- Evolution log shows artifact version != deployed version for > 7 days
- README counts/stats differ from actual file counts by > 10%

**Output:**
```yaml
type: metasync
detector: drift
target: "what has drifted and from what source of truth"
evidence:
  - source: health_scores | contracts | beliefs | evolution | readme
    detail: "specific drift measurement"
    timestamp: "ISO-8601"
confidence: 0.0-1.0
proposed_action: "sync command or directive"
drift_magnitude: 0.0-1.0  # normalized distance from source of truth
```

**Confidence calculation:**
- Base: 0.5 (any measurable drift detected)
- Scale: proportional to `drift_magnitude`
- Boost: +0.2 if drift affects decision-making (beliefs, health scores)
- Boost: +0.1 if drift is cross-repo
- Penalty: -0.1 if drift is in low-priority category (weights, low-staleness)

### Detector 4: Dead Code → MetaPrune

**Signal:** Artifacts exist but are unreferenced, unused, or superseded.

**Inputs:**
- Cross-reference analysis: schemas referenced by no policy or persona
- `state/triggers/` — trigger files that were never consumed
- `state/` — state files not read by any skill or driver phase
- `grammars/` — grammars with zero research cycles and zero course production
- `policies/` — policies not referenced in any skill, driver phase, or persona
- `tests/behavioral/` — tests for personas/artifacts that no longer exist

**Detection rules:**
- State file with `last_updated > 60 days` and no references in recent manifests
- Grammar with `cycle_count: 0` and `age > 30 days`
- Policy not referenced by any skill, persona, or driver phase
- Schema not referenced by any JSON file or validation step
- Trigger file in `processing/` older than 7 days (consumed but not cleaned up)
- Evolution log entry for an artifact that no longer exists

**Output:**
```yaml
type: metaprune
detector: dead_code
target: "what appears unused"
evidence:
  - source: cross_reference | age | manifest
    detail: "specific unreferenced artifact"
    timestamp: "ISO-8601"
confidence: 0.0-1.0
proposed_action: "archive or delete"
risk_level: low | medium | high  # based on what the artifact governs
```

**Confidence calculation:**
- Base: 0.3 (unreferenced detected)
- Boost: +0.2 if no references found across all repos
- Boost: +0.2 if artifact age > 60 days with no activity
- Penalty: -0.3 if artifact is constitutional or policy (high risk to prune)
- Penalty: -0.2 if artifact was referenced within last 30 days
- Hard ceiling: 0.7 for any constitutional artifact (always require human confirmation)

### Detector 5: Overlap → MetaMerge

**Signal:** Multiple artifacts serve the same purpose or contain duplicate logic.

**Inputs:**
- `grammars/` — grammars with >50% production overlap
- `policies/` — policies with overlapping `scope` or `applies_to` fields
- `personas/` — personas with >70% capability overlap
- `state/streeling/departments/` — departments with overlapping `research_areas`
- `schemas/` — schemas with structurally identical sub-schemas

**Detection rules:**
- Two grammars sharing >50% of production names (after normalization)
- Two policies with identical `constitutional_basis` and overlapping scope
- Two departments with >60% research area overlap
- Two schemas with identical `properties` blocks (>80% key overlap)
- Two skills with identical pipeline steps (>60% step overlap)

**Output:**
```yaml
type: metamerge
detector: overlap
targets: ["artifact-a", "artifact-b"]
evidence:
  - source: structural_comparison
    detail: "specific overlap measurement"
    overlap_percentage: 0.0-1.0
confidence: 0.0-1.0
proposed_action: "merge into single artifact, or extract shared base"
merge_strategy: absorb | extract_base | federate
```

**Confidence calculation:**
- Base: 0.3 (any overlap detected)
- Scale: proportional to `overlap_percentage`
- Boost: +0.2 if both artifacts are in the same domain
- Penalty: -0.2 if artifacts serve different consumer repos
- Penalty: -0.3 if one artifact is constitutional
- Hard ceiling: 0.6 for cross-repo merges (always require human confirmation)

## Proposal Schema

All detectors produce proposals conforming to `schemas/meta-recognition-proposal.schema.json`:

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://github.com/GuitarAlchemist/Demerzel/schemas/meta-recognition-proposal",
  "title": "Meta-Recognition Proposal",
  "description": "A proposal from the meta-recognition engine for a systemic improvement",
  "type": "object",
  "required": ["proposal_id", "type", "detector", "target", "evidence", "confidence", "proposed_action", "timestamp"],
  "properties": {
    "proposal_id": {
      "type": "string",
      "pattern": "^mrp-[0-9]{3}-[a-z0-9-]+$",
      "description": "Unique proposal ID: mrp-NNN-slug"
    },
    "type": {
      "type": "string",
      "enum": ["metafix", "metabuild", "metasync", "metaprune", "metamerge"],
      "description": "Which meta-skill should handle this proposal"
    },
    "detector": {
      "type": "string",
      "enum": ["repetition", "template", "drift", "dead_code", "overlap"],
      "description": "Which detector produced this proposal"
    },
    "target": {
      "type": "string",
      "description": "What the proposal is about"
    },
    "targets": {
      "type": "array",
      "items": { "type": "string" },
      "description": "Multiple targets (for metamerge)"
    },
    "evidence": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["source", "detail"],
        "properties": {
          "source": { "type": "string" },
          "detail": { "type": "string" },
          "timestamp": { "type": "string", "format": "date-time" }
        }
      },
      "minItems": 1,
      "description": "Evidence supporting this proposal"
    },
    "confidence": {
      "type": "number",
      "minimum": 0.0,
      "maximum": 1.0,
      "description": "Confidence score — applies standard thresholds from alignment-policy"
    },
    "proposed_action": {
      "type": "string",
      "description": "Suggested skill invocation or action"
    },
    "risk_level": {
      "type": "string",
      "enum": ["low", "medium", "high", "critical"],
      "description": "Risk of acting on this proposal"
    },
    "timestamp": {
      "type": "string",
      "format": "date-time"
    },
    "cycle_id": {
      "type": "string",
      "description": "Which driver cycle produced this proposal"
    },
    "status": {
      "type": "string",
      "enum": ["proposed", "accepted", "rejected", "deferred", "executed"],
      "default": "proposed"
    },
    "resolution": {
      "type": "string",
      "description": "What happened when this proposal was acted on"
    }
  }
}
```

## Integration with Driver Cycle

### RECON Phase Integration

The meta-recognition engine runs as **Stage 3b** within RECON, after the standard Stage 3 (Analyze):

```
RECON
  Stage 1: Gather        → raw data
  Stage 2: Enrich        → health scores
  Stage 3: Analyze       → governance drift, anomalies, blind spots
  Stage 3b: Meta-Recognize → meta-opportunities (THIS ENGINE)
  Stage 4: Surface       → situation report (now includes meta-proposals)
```

### PLAN Phase Integration

Meta-recognition proposals are added to the work manifest during PLAN:

1. Filter proposals by confidence threshold (standard alignment thresholds)
2. Sort by confidence descending, then by risk ascending
3. >= 0.9 confidence → auto-schedule in current cycle
4. >= 0.7 confidence → schedule with note in manifest
5. >= 0.5 confidence → include in manifest as "suggested" (human decides)
6. < 0.5 confidence → log only, do not schedule

### EXECUTE Phase

Accepted proposals route to their corresponding skill:
- `metafix` → `/demerzel metafix [target]`
- `metabuild` → `/demerzel metabuild [target]`
- `metasync` → (new skill, see Task #3 / Issue #111)
- `metaprune` → (new skill, to be designed)
- `metamerge` → (new skill, to be designed)

### COMPOUND Phase

After execution, the engine feeds back:
- Did the proposal resolve the detected pattern?
- Should the detector's confidence weights be adjusted?
- Did false positives occur? (adjust penalty terms)
- Did the proposal reveal new patterns? (feed to next cycle)

## State Directory

```
state/meta-recognition/
  proposals/               # Active proposals
    mrp-001-slug.json
  archive/                 # Resolved/rejected proposals
    mrp-000-slug.json
  detector-weights.json    # Learned detector accuracy weights
  summary.json             # Running counts and accuracy stats
```

### detector-weights.json

Tracks detector reliability over time:

```json
{
  "detectors": {
    "repetition": {
      "proposals_generated": 0,
      "proposals_accepted": 0,
      "proposals_executed": 0,
      "false_positive_rate": 0.0,
      "confidence_calibration": 1.0
    },
    "template": { "...": "same structure" },
    "drift": { "...": "same structure" },
    "dead_code": { "...": "same structure" },
    "overlap": { "...": "same structure" }
  },
  "last_updated": "ISO-8601"
}
```

The `confidence_calibration` factor multiplies the raw confidence score. Starts at 1.0. Adjusted by COMPOUND phase: +0.05 for accurate proposals, -0.1 for false positives. Clamped to [0.5, 1.5].

## Cybernetic Analysis

This engine is a second-order cybernetic system:

| Cybernetic Concept | Mapping |
|-------------------|---------|
| Observer | Meta-recognition engine |
| Observed | The governance system itself (detectors observe detectors) |
| Feedback loop | COMPOUND → detector-weights → next cycle confidence |
| Homeostasis | Confidence calibration keeps proposals within useful range |
| Requisite variety | Five detectors cover five distinct meta-opportunity classes |
| Autopoiesis | Engine proposals can improve the engine itself (metafix on detector logic) |
| VSM System 3* | Sporadic audit function — not running constantly, but checking periodically |

### Fixed Point

The engine can detect problems with itself:
- Repetition detector finds the engine keeps proposing the same thing → MetaFix the detector
- Template detector notices detector code follows a pattern → MetaBuild a detector factory
- Drift detector notices detector-weights.json is stale → MetaSync
- Dead code detector finds a detector with zero accepted proposals → MetaPrune the detector
- Overlap detector finds two detectors producing identical proposals → MetaMerge

This self-referential capability is the defining characteristic of second-order cybernetics.

## Constitutional Basis

- **Article 7 (Auditability)** — all proposals logged with evidence chains
- **Article 8 (Observability)** — detector accuracy is a governance metric
- **Article 9 (Bounded Autonomy)** — confidence thresholds gate execution
- **Article 11 (Ethical Stewardship)** — systemic improvement over point fixes
- **Zeroth Law** — meta-recognition prevents governance decay that could harm the ecosystem

## Behavioral Tests

Tests should cover:

1. **Repetition detection** — given 3+ similar fix commits, detector produces metafix proposal
2. **Template detection** — given manually created department, detector proposes metabuild
3. **Drift detection** — given stale belief cited in recent decision, detector proposes metasync
4. **Dead code detection** — given unreferenced schema, detector proposes metaprune
5. **Overlap detection** — given two grammars with >50% shared productions, proposes metamerge
6. **Confidence thresholds** — proposals below 0.5 are not scheduled
7. **Self-reference** — engine can produce proposals about its own detectors
8. **False positive learning** — rejected proposal reduces detector confidence calibration
9. **Cross-repo signals** — drift detected across Demerzel + consumer repo boosts confidence
10. **Constitutional guard** — proposals affecting constitutional artifacts capped at 0.7

## Dependencies

- Requires RECON Stages 1-2 data (health scores, git history)
- Requires `state/conscience/` signals and patterns
- Requires `state/evolution/` logs
- MetaSync skill (#111) needed for drift proposals to execute
- MetaPrune and MetaMerge skills need to be designed (new issues)

## Open Questions

1. Should the engine run every cycle or only when triggered (e.g., after N commits)?
   - **Recommendation:** Every cycle, but with a cooldown per detector (no re-proposal within 3 cycles if rejected)
2. Should proposals require human approval below a certain confidence?
   - **Recommendation:** Yes, standard alignment thresholds apply (< 0.5 = confirm, < 0.3 = escalate)
3. How should cross-cycle proposal deduplication work?
   - **Recommendation:** Hash evidence fingerprint; if >80% evidence overlap with existing proposal, boost existing confidence rather than creating duplicate
