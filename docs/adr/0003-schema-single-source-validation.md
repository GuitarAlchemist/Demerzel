# 3. Schema as the single source of structural validation

- Status: Accepted
- Date: 2026-06-20
- Deciders: Stephane Pareilleux
- Source: `/improve-codebase-architecture` review + `/grilling` session (2026-06-20)

## Context

Validation rules are re-coded per caller and per language. The HALT-ALL marker is validated
twice — `scripts/demerzel_halt.py` (Python) and `scripts/dev-process-overseer.ps1`
(PowerShell) — with the schema-version, scope-enum, and required-field rules hand-written in
each. Digest frontmatter is validated in three places (`digest-validate.ps1`,
`karpathy-cherny-discipline.yml`, and the schema file). Meanwhile `schemas/persona.schema.json`
exists but is **never used** by any validator.

In the `/codebase-design` vocabulary: the validators are **shallow** adapters that re-state
rules the schema already expresses, and the **seam** (where the rule lives) is duplicated
instead of shared. Two adapters over the same rule (Python + PowerShell for the halt marker)
prove the seam is **real**, not hypothetical.

## Decision

Make a JSON Schema the **single source of all structural validation rules** — types, enums,
required fields. Two thin per-language adapters read it:

- Python: `jsonschema` (already used in `scripts/qa_tribunal_emit.py`).
- PowerShell: `Test-Json -Schema` (native in PowerShell 7).

The schema file *is* the seam. `persona.schema.json` is wired into the manifest's validate
step (ADR-0001) instead of sitting unused.

Validation is split three ways by what each rule actually needs:

- **Structural** (types/enums/required) → the schema, read by both adapters.
- **Relational** ("this citation resolves to a real article," "this persona has a test") →
  folded into the manifest generator (ADR-0001), which harvests edges and fails CI on
  dangling ones. No separate validator.
- **Temporal / operational** ("`expires_at` is in the future," "this digest is fresh now")
  → stays at the **point of use**. "Now" is inherently per-call; these were never a
  duplicated *rule*, just the same question asked at genuinely different instants.

The one remaining temporal duplication — the overseer and the preflight both re-reading and
expiry-checking HALT-ALL — is resolved by the `Get-DomainGateState` deep module (a separate
follow-on), not by the schema.

## Consequences

- **Locality**: change a structural rule in the schema, once; both languages follow.
- **Interface shrinks**: callers cross one seam, `validate(artifact, schema)`.
- The three-way split pinpoints the real bug: the halt marker's *structural* part was
  wrongly duplicated (collapses into the schema), while its *expiry* check legitimately
  lives wherever the marker is read.
- `persona.schema.json` finally earns its keep.

## Alternatives considered

- **One unified validator owning structural + relational + temporal.** Rejected: relational
  checks already belong to the manifest, and temporal checks are inherently per-call —
  forcing them into one module would make it shallow-but-wide and presumptuous about "now."
- **Keep per-language hand-coded validators, accept the duplication.** Rejected: the halt
  marker is the proof the duplication drifts; the schema is readable by both runtimes, so the
  shared seam costs little.

## Update (2026-06-21)

The original `demerzel_halt.py` adapter was deliberately **stdlib-only** and re-implemented
the field checks in Python (harvesting only the enum/length values from the schema). That
left it a *looser* subset than the PowerShell `Test-Json` adapter — no `pattern`,
`additionalProperties`, or `required`-list enforcement — so the two adapters could still
diverge. We now validate with **`jsonschema` when it is importable** (full parity with
`Test-Json`) and fall back to a **stdlib generic schema-subset check** only when the package
is absent. The fallback is retained because the halt tool is the cross-repo emergency brake
and must run on a bare-Python machine without `pip install`. `scripts/requirements-halt.txt`
declares `jsonschema` so CI always takes the strong path. This refines — does not reverse —
the "schema is the single source" decision: the rules still live only in the schema; both
runtimes now enforce all of them.
