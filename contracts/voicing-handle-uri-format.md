# Voicing Handle URI Format

**Version:** 1.0.0
**Status:** Active
**Department:** Guitar Alchemist / Context Stewardship
**Companion schema:** `schemas/voicing-handle.schema.json`
**Consumed by:** GA MCP server, ga-ask skill, orchestrator, UI hydration layer

---

## 1. Why Content-Addressable?

The GA ecosystem will soon index millions of voicings across 114 instruments and 282 tunings. Returning full voicing objects through MCP tools floods Claude's context window (observed: 17K token leakage from current enumeration tools). Content-addressable handles solve this by:

- **Caching**: deterministic hashes → CDN-cacheable, immutable URLs
- **Reproducibility**: same voicing always → same hash, verifiable across sessions
- **Diffing**: comparing two handles reveals what changed
- **Token reduction**: 15-token handle vs 500-token voicing object (~99% reduction)
- **Client-side hydration**: UI fetches rich visuals without touching LLM context

---

## 2. Four Handle Types

### 2.1 Voicing Handle (`vh`)

**Purpose:** Immutable reference to a concrete voicing.

**URI syntax:** `ga:vh:v{version}:sha256-{64hex}`

**Example:** `ga:vh:v3:sha256-7b91a8c4d2e6f1a3b5c7d9e0f2a4b6c8d0e2f4a6b8c0d2e4f6a8b0c2d4e6f8a0`

**Lifecycle:** Permanent. Same voicing always produces same hash. Safe to embed in documentation, URLs, knowledge bases.

**Hash input:** canonical serialization of `{instrument_id, tuning_id, fret_array, chord_dna_hash, optic_k_version}` (see Section 4 for exact canonicalization rules).

### 2.2 Query Result Handle (`qr`)

**Purpose:** Ephemeral reference to a ranked candidate set from a query.

**URI syntax:** `ga:qr:v{version}:{session_id}:{query_seq}`

**Example:** `ga:qr:v2:sess-12ab:4`

**Lifecycle:** Session-scoped. Default TTL 3600s. Enables iterative refinement without re-running query.

**Use case:** `FindVoicingSets(chord_dna, ...)` returns a qr handle. Later calls like `RefineVoicingSet(qr_handle, add_constraints=...)` produce new qr handles without the LLM seeing the underlying voicing list.

### 2.3 Morphology Handle (`mh`)

**Purpose:** Intermediate representation — chord DNA projected into a tuning's fretboard morphology space, BEFORE full voicing realization.

**URI syntax:** `ga:mh:v{version}:tuning-{hash}:chorddna-{hash}`

**Example:** `ga:mh:v1:tuning-5d2a8f:chorddna-a91f4c`

**Lifecycle:** Deterministic and cacheable (like vh). Maps to the 25% MORPHOLOGY layer of OPTIC-K.

**Use case:** `project_chord_to_tuning(chord_dna, tuning)` returns mh handle. `realize_morphology(mh_handle, constraints)` produces concrete voicings on demand. Splits computation: chord DNA (reusable) vs fretboard projection (per-tuning).

### 2.4 View Handle (`view`)

**Purpose:** Field projection of an existing handle. Same underlying object, different field mask. No mutation.

**URI syntax:** `ga:view:v{version}:{parent_handle_id}?fields={comma_list}`

**Example:** `ga:view:v1:qr-12ab-4?fields=fretspan,bass,topnote`

**Lifecycle:** Inherits from parent. Resolves same underlying data with a projection applied.

**Use case:** Drill-in without fetching full object. Tools return a short view handle with only the 3 fields needed for the current decision.

---

## 3. URI Syntax (ABNF Grammar)

```abnf
handle       = "ga:" type ":v" version ":" handle-body
type         = "vh" / "qr" / "mh" / "view"
version      = 1*DIGIT

; Voicing Handle body
vh-body      = "sha256-" 64HEXDIG

; Query Result Handle body
qr-body      = session-id ":" query-seq
session-id   = 4*32(ALPHA / DIGIT / "-")
query-seq    = 1*DIGIT

; Morphology Handle body
mh-body      = "tuning-" 6*HEXDIG ":chorddna-" 6*HEXDIG

; View Handle body
view-body    = parent-id "?fields=" field-list
parent-id    = 1*(ALPHA / DIGIT / "-")
field-list   = field-name *("," field-name)
field-name   = lowercase-alpha *(lowercase-alpha / DIGIT / "_")
```

---

## 4. Hash Computation (Voicing Handle)

Canonical input for `ga:vh:v3`:

```json
{
  "instrument_id": "guitar",
  "tuning_id": "standard",
  "fret_array": [null, 3, 2, 0, 1, 0],
  "chord_dna_hash": "a91f4c",
  "optic_k_version": 2
}
```

- Serialize with sorted keys, no whitespace, UTF-8
- SHA-256 → hex, lowercase
- `null` in `fret_array` means muted string
- Non-negative integers are fret positions (0 = open)

Reference implementation (pseudocode):
```
canonical = json.dumps(input, sort_keys=True, separators=(',', ':'))
hash_hex = sha256(canonical.encode('utf-8')).hexdigest()
handle = f"ga:vh:v3:sha256-{hash_hex}"
```

---

## 5. Client vs Server Responsibilities

### Server (GA MCP + API)

- Generates all handles (LLM never invents handles)
- Maintains qr handle session state
- Resolves handles to concrete voicing data
- Validates handle format on input
- Computes hashes deterministically
- Exposes `/api/render/*` for UI hydration

### Client (ga-ask skill, orchestrator, UI)

- Receives handles from server, never constructs
- Passes handles between tool calls as opaque identifiers
- Optionally fetches visual renderings via `/api/render/*`
- Caches resolved handles locally (immutable = safe to cache forever for vh/mh)
- Honors TTL for qr handles

---

## 6. Backward Compatibility

Version bumps in URI prevent breakage:

- **v1 → v2**: tooling recognizes both, prefers v2
- **v2 → v3**: changes hash input (e.g., adds new field) — vh handles get new hashes
- **Deprecation window**: 6 months minimum between introducing vN+1 and rejecting vN
- **Clients declare supported versions**: `Accept: application/vnd.ga.handle+json; version=3`

---

## 7. Integration with Existing Demerzel Artifacts

- **`schemas/blackboard-state.schema.json`** — `displayed_artifacts[]` items use `vh` handles as `artifact_id`
- **`contracts/ga-orchestrator-architecture.md` v2.0.0** — orchestrator output pipeline emits handles in place of voicing objects
- **`contracts/ga-mcp-tool-bundles.md`** — theory-tools, technique-tools, tab-tools, composer-tools all adopt handle-first responses
- **`contracts/ui-chord-hydration.md`** — `<ChordView id="ga:vh:v3:..."/>` tags reference vh handles
- **`contracts/socratic-tool-design.md`** — Oracle-pattern tools return single vh handle + reasoning
- **`policies/mcp-context-budget.yaml`** — handles count as ~15 tokens each for budget enforcement

---

## 8. Worked Examples

### Example 1: Resolving a chord to a voicing handle

```
LLM: calls resolve_voicing(chord="Cmaj7", instrument="guitar", tuning="standard")
MCP: computes best voicing [null, 3, 2, 0, 1, 0]
MCP: hashes canonical representation → sha256-7b91...
MCP: returns {
  handle: "ga:vh:v3:sha256-7b91...",
  reasoning: "Open-position Cmaj7, beginner-friendly, no barre."
}
LLM context cost: ~35 tokens
```

### Example 2: Query result refinement

```
Turn 1: LLM calls find_voicings(chord_dna="...", constraints={no_barre: true})
        MCP returns: {qr: "ga:qr:v2:sess-12ab:4", count: 42, representatives: [3 vh handles]}

Turn 2: LLM calls refine_voicings(qr="ga:qr:v2:sess-12ab:4", add_constraints={max_fret: 5})
        MCP returns: {qr: "ga:qr:v2:sess-12ab:5", count: 12, representatives: [3 vh handles]}

Total LLM context cost across both turns: ~150 tokens (vs ~5K with dumped voicing lists)
```

### Example 3: View projection for drilling in

```
LLM has: ga:vh:v3:sha256-7b91... (full voicing handle)
LLM needs only fretspan + difficulty for comparison
LLM requests: ga:view:v1:vh-7b91?fields=fretspan,difficulty
MCP returns: {fretspan: 4, difficulty: 2}
LLM context cost: ~20 tokens
```

### Example 4: Morphology diff between tunings

```
Same chord Cmaj7, different tunings:
  Standard:  ga:mh:v1:tuning-5d2a8f:chorddna-a91f4c
  DADGAD:    ga:mh:v1:tuning-8f3b2e:chorddna-a91f4c

LLM calls: compare_morphologies(mh1, mh2)
MCP returns: {
  common_voicings: 3,
  standard_only: 12,
  dadgad_only: 7,
  easier_in: "DADGAD (avg difficulty 2.1 vs 3.4)"
}
LLM context cost: ~40 tokens
```

---

## 9. Security & Privacy

- Handles are public (content-addressable, no auth needed for vh/mh)
- `qr` handles contain session IDs — treat as sensitive, don't leak across users
- Hash pre-images MUST NOT include user PII (use anonymous session IDs)
- Rate limit handle resolution endpoints (100 req/min per client)

---

## 10. Evolution Hooks

- Handle format reviewed quarterly
- New handle types (e.g., `ga:score:v1:...` for scored candidate sets) added via minor version bump
- Deprecated handle types remain resolvable for 6 months
- Index version bumps (`optic_k_version`) may invalidate old vh handles — provide migration tools
