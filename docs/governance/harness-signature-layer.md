# Harness Signature Layer — Design Doc

**Status:** Design, version 0.1, 2026-04-11. **Not yet implemented.**
**Scope:** Specifies the cryptographic signing, verification, and
key-management layer that unlocks Tier 1+ harness adapters.
**Blocks:** `ix-harness-ga`, `ix-harness-github-actions`, and all
external-source adapters.
**Depends on:** Phase 1 Path C (shipped), harness engineering
governance direction (`docs/governance/harness-engineering.md`).

## Why this document exists

Today, `HexObservation` records are trusted by their `source`
field at face value. An observation with `source: "tars"` is
accepted as coming from tars because we wrote tars and nobody
else can write to our SessionLogs. This is the **Tier 0 trust
model**: trust by construction, not by cryptography.

Tier 0 is fine for first-party adapters where we control the
binary, the invocation, the filesystem, and the log. It falls
apart the moment any of those is shared with a producer we
don't fully trust:

- An adapter running on shared CI infrastructure can be forged
  by anyone with write access to the runner's filesystem
- An external webhook producer can claim any source string
- A compromised first-party binary can produce observations
  indistinguishable from authentic ones

The governance direction (`harness-engineering.md`) commits
Demerzel to a four-tier trust model where Tier 1+ requires
signed observations. **This document specifies what signing
means, how it's applied, how keys are managed, and what
happens when a key is compromised.**

## The five components

| # | Component | Purpose |
|---|---|---|
| 1 | Canonical serialization | Deterministic byte form of an observation for signing |
| 2 | Detached signatures | Per-observation signatures carried alongside the observation |
| 3 | Key registry | Public keys bound to source identities |
| 4 | Verification step | Added to the merge function to drop unsigned observations from tiers that require signing |
| 5 | Key rotation + revocation | Operational lifecycle for compromised or expired keys |

Each is described below with enough detail for a future session
to implement without re-deriving the design.

## 1. Canonical serialization

A signed observation must hash to the same bytes regardless of
which library serialized it, which field order the producer
used, which JSON whitespace the emitter preferred. Canonical
serialization solves this.

**Format:** a fixed-field-order JSON subset with no whitespace:

```text
{"claim_key":"<value>","diagnosis_id":"<value>","evidence":<value or null>,"ordinal":<u32>,"round":<u32>,"source":"<value>","variant":"<letter>","weight":<float>}
```

**Rules:**
- Fields are listed in alphabetical order (not the declaration
  order in the Rust enum)
- Strings use the JSON escaping rules with no optional whitespace
- Floats use `serde_json`'s default format (no trailing zeros)
- `evidence: null` is rendered literally as `null`; omitted
  `evidence` rounds to the same canonical form as `None`
- No trailing newline, no BOM, no comments

**Example canonical form for an observation:**

```text
{"claim_key":"ix_stats::valuable","diagnosis_id":"abc123","evidence":"ok","ordinal":42,"round":3,"source":"cargo","variant":"T","weight":0.9}
```

**Implementation sketch:**

```rust
pub fn canonical_form(obs: &HexObservation) -> String {
    let map = serde_json::json!({
        "claim_key": obs.claim_key,
        "diagnosis_id": obs.diagnosis_id,
        "evidence": obs.evidence,
        "ordinal": obs.ordinal,
        "round": obs.round,
        "source": obs.source,
        "variant": variant_letter(obs.variant),
        "weight": obs.weight,
    });
    // serde_json preserves object key insertion order since 1.0.
    // We insert in alphabetical order above. The output is
    // deterministic.
    serde_json::to_string(&map).unwrap()
}
```

**Known risk:** float representation is not bit-exactly
deterministic across platforms in corner cases. Mitigation:
require all weights to be multiples of 0.01 (weight resolution
is 100 buckets over [0, 1]). This matches the granularity the
Belnap table already uses and sidesteps float-printing drift.

## 2. Detached signatures

A signature is a separate byte string alongside each observation.
The wire format extends `SessionEvent::ObservationAdded` with an
optional `signature` field:

```rust
ObservationAdded {
    ordinal: u64,
    source: String,
    diagnosis_id: String,
    round: u32,
    claim_key: String,
    variant: Hexavalent,
    weight: f64,
    evidence: Option<String>,
    // NEW: optional detached signature.
    #[serde(default)]
    signature: Option<Signature>,
}

pub struct Signature {
    pub algorithm: SignatureAlgorithm,
    pub key_id: String,    // fingerprint of the public key, hex
    pub bytes: String,     // base64-encoded signature bytes
}

pub enum SignatureAlgorithm {
    Ed25519,
    EcdsaP256,
    // Extension point for future algorithms.
}
```

**Signing algorithm:** Ed25519 by default. 32-byte public key,
64-byte signature, fast to verify, no parameter choices. The
enum exists to allow ECDSA-P256 for environments that can't do
Ed25519 (rare, but documented as an escape hatch).

**Signature input:** the canonical form from §1. The signer
computes `sign(private_key, canonical_form_bytes)`.

**Signature verification:** the merge function computes
`verify(public_key, canonical_form_bytes, signature.bytes)`.

**Why detached rather than inline:** keeping the signature
separate from the content means adapters that don't sign still
produce a valid observation (the signature field is `None`);
consumers that don't verify still read the content fine.
Gradual adoption is possible.

## 3. Key registry

A public key registry binds source identities to public keys.

**File:** `demerzel/schemas/harness-source-keys.json`

**Shape:**

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://github.com/GuitarAlchemist/Demerzel/schemas/harness-source-keys",
  "version": 1,
  "sources": {
    "ga": {
      "tier": 1,
      "require_signing": true,
      "active_keys": [
        {
          "key_id": "<hex fingerprint>",
          "algorithm": "ed25519",
          "public_key_base64": "<32 bytes>",
          "valid_from": "2026-04-11T00:00:00Z",
          "valid_until": "2027-04-11T00:00:00Z",
          "notes": "initial ga signing key"
        }
      ],
      "revoked_keys": []
    },
    "github-actions": {
      "tier": 3,
      "require_signing": true,
      "active_keys": [],
      "revoked_keys": []
    }
  }
}
```

**Rules:**
- `tier` is 0, 1, 2, or 3 matching the four-tier model
- `require_signing` defaults to true for Tier 1+, false for Tier 0
- `active_keys` is the set of currently valid keys for this source
- `revoked_keys` is the set of compromised or rotated-out keys;
  observations signed by a revoked key are rejected even if the
  signature verifies cryptographically
- Multiple active keys support rolling key rotation (sign with
  the new key, accept either until the old one is revoked)

**Authority:** the key registry is a Demerzel governance
artifact. Adding or revoking a key is a PR. This is deliberate
friction — key rotation is infrequent and deserves review.

## 4. Verification step in the merge function

`ix-fuzzy::observations::merge` gains a new stage between step
1 (deduplication) and step 3 (contradiction synthesis):

```
Step 1.5: Signature verification
    For each observation in the deduplicated set:
        lookup tier requirements for obs.source in the key registry
        if source requires signing:
            if obs.signature is None:
                drop this observation (log via event sink)
                continue
            lookup key_id in active_keys
            if not found:
                drop this observation (unknown key)
                continue
            if key is in revoked_keys:
                drop this observation (revoked)
                continue
            compute canonical_form(obs)
            verify signature.bytes against public_key on canonical_form
            if verification fails:
                drop this observation (bad signature)
                continue
        else:
            (Tier 0 — no signing required)
            accept as-is
```

**Drops are silent at the math level but loud at the audit
level.** Every dropped observation emits a new `SessionEvent`
variant — `ObservationRejected` — that carries the reason code
and the offending observation's dedup key. Downstream audit
tools can grep for these to find integrity events.

**Why drop rather than fail the merge:** one bad observation
shouldn't cascade into a merge failure for every other producer.
The merge function's job is to produce a best-effort merged
state from trusted inputs; untrusted inputs get silently filtered
and logged for later review.

## 5. Key rotation + revocation

**Rotation:** a source wants to change keys. Workflow:

1. Generate new keypair
2. Demerzel PR adding the new public key to `active_keys`
3. PR merges; both old and new keys are valid
4. Producer cuts over to signing with the new key
5. After N days (configurable per source, default 7), second
   Demerzel PR moves the old key to `revoked_keys`
6. Any observation still signed by the old key is dropped

**Revocation (compromise response):** a key is known or
suspected to be leaked. Workflow:

1. Immediate Demerzel PR moving the key to `revoked_keys` with
   an `emergency: true` flag
2. PR bypasses normal review queue (emergency label triggers
   fast-track)
3. All consumers refresh the registry on their next merge call
4. Observations signed by the revoked key are rejected from that
   point forward
5. Retroactive rejection: the merge function can optionally
   re-validate past observations against the current registry;
   any previously-accepted observations signed by the now-
   revoked key are re-classified as tainted
6. Tainted observations are downgraded — their variant becomes
   U (unknown) and their weight becomes 0.1, preserving the
   historical record without letting them influence decisions

**The compromise playbook** lives at
`demerzel/docs/governance/harness-compromise-playbook.md`
(to be written alongside the first Tier 1+ adapter). It
documents:
- Who can trigger a revocation PR
- How fast-track review works
- How to notify active consumers of a revocation
- How to investigate the scope of a compromise (what claims
  did the bad key sign?)
- How to remediate (what governance decisions were influenced
  by the compromised observations?)

## Implementation order

When this design is implemented, ship in this order:

### Phase A — Foundation (2-3 days)

1. **New crate `ix-harness-signing`** with:
   - `canonical_form(&HexObservation) -> String`
   - `sign(private_key, &HexObservation) -> Signature`
   - `verify(public_key, &HexObservation, &Signature) -> Result<(), Error>`
   - Ed25519 implementation (via `ed25519-dalek`)
   - Unit tests covering canonical-form determinism, sign-verify
     round trip, cross-platform byte equality
2. **Demerzel schema**: `schemas/harness-source-keys.json` with
   JSON Schema validation
3. **Demerzel doc**: `docs/governance/harness-compromise-playbook.md`

### Phase B — Integration (1-2 days)

4. **Extend `SessionEvent::ObservationAdded`** with the optional
   `signature` field (backward-compat for unsigned observations)
5. **Add `SessionEvent::ObservationRejected`** variant for audit
   of dropped observations
6. **Update `ix-fuzzy::observations::merge`** to call the
   verification step when present; drop-and-emit-rejection on
   failure
7. **Extend the G-Set dedup key** to include the signature key_id
   (so two observations with the same content but different
   keys are treated as distinct — useful during rotation windows)

### Phase C — First Tier 1 adapter (1 day)

8. **`ix-harness-ga` crate** using the signing crate — sign
   every emitted observation with ga's private key
9. **ga key** added to `harness-source-keys.json` via Demerzel PR
10. **End-to-end integration test**: ga → ix triage, verifying
    both the accept path (valid sig) and the reject path
    (tampered content)

### Phase D — Migration (incremental)

11. **Update ix-harness-tars and ix-harness-cargo** to optionally
    sign their observations (backward-compat: unsigned still
    works for Tier 0)
12. **Update the merge function** to tighten Tier 0's policy
    over time: eventually even Tier 0 adapters should sign, even
    though it's not required, for defense in depth

**Total:** ~5-7 days of focused work. Not blocked by anything;
can start whenever.

## What this design does NOT cover

Explicit non-goals:

- **Encryption.** Observations are not secret — they're audit
  records. Only authenticity matters. If we ever need encrypted
  observations, that's a separate layer on top of signing.
- **Quantum resistance.** Ed25519 is not post-quantum secure.
  If large-scale quantum computing becomes a real threat, the
  `SignatureAlgorithm` enum is the extension point — add a
  post-quantum variant and run both algorithms in parallel
  during migration. Scoped out of this document.
- **Rotating the master registry itself.** Who signs the
  `harness-source-keys.json` file? Deferred to when we have
  multi-org governance. For a single-org deployment the Git
  history on the Demerzel repo IS the integrity trail.
- **Hardware security modules.** First-party producers can hold
  keys in files. If we ever onboard sources requiring HSM-backed
  keys, the `Signature` struct's `key_id` field is opaque enough
  to cover HSM-managed keys without wire-format changes.
- **Rate limiting.** The signature layer doesn't protect against
  a compromised-but-not-yet-revoked key flooding the merge with
  authentic-looking but malicious observations. Rate limiting
  is a separate governance primitive (candidate: tie into the
  existing `ix-loop-detect` circuit breaker with per-source
  windows).

## Open questions for the next design session

1. **Should the canonical form use CBOR or similar binary
   format** instead of JSON? Binary is faster to sign/verify,
   but JSON is debuggable by inspection. Leaning JSON for now.

2. **Where does the private key live** on a first-party adapter
   host? Environment variable? File with restricted perms? OS
   keychain? Probably per-platform, with a trait for pluggable
   key storage.

3. **Should we sign the diagnosis_id separately** (a content
   hash of the native input) so consumers can verify the adapter
   faithfully processed its input? This would require the
   adapter to include the native input in the signed payload,
   which doubles the wire size. Probably not worth it — trust
   the adapter to compute diagnosis_id honestly, or don't use
   the adapter.

4. **How does signature verification interact with the flywheel
   trace export?** Traces are persisted JSONL; do we re-verify
   on re-ingestion? Probably yes, using the key registry active
   at re-ingestion time (NOT the time the trace was written).
   This catches retroactive revocations.

5. **What's the key format for storing private keys on disk?**
   PEM? Raw bytes? JWK? Probably PEM for compatibility with
   existing tooling, with a clear "this is a signing key, not
   a TLS key" header comment.

## Why this is the right direction

Three justifications, in order of load-bearingness:

1. **It's the minimum work to unlock Tier 1+ adapters.**
   Without signing, we're permanently stuck at Tier 0. That
   means harness engineering only works for code we wrote
   ourselves, which misses most of the value.

2. **The crypto is commodity.** Ed25519 via `ed25519-dalek` is
   a single dep with a well-reviewed API. No novel crypto
   design. The hard parts are canonical serialization (boring)
   and key management (process, not code).

3. **It composes with what exists.** The signature field is
   optional, the verification step is additive, the key
   registry is a new file that doesn't touch anything else.
   No refactoring of the CRDT merge, no changes to the
   SessionLog wire format beyond the new optional field.

## Version

0.1 — 2026-04-11 — initial design. Covers canonical form,
detached signatures, key registry, verification step, rotation
+ revocation. Implementation not started. Compromise playbook
not written (will be written alongside first Tier 1 adapter).
