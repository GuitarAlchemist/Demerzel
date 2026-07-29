# Contributing to Demerzel

Thank you for contributing to Demerzel — an AI governance framework. Before submitting anything, please read this guide. It is short and worth your time.

---

## What Demerzel Is (and Is Not)

Demerzel contains **no runtime code**. It is a collection of governance artifacts:

- Personas (`personas/`) — YAML
- Constitutions (`constitutions/`) — Markdown
- Policies (`policies/`) — YAML
- Schemas (`schemas/`) — JSON Schema
- Behavioral tests (`tests/behavioral/`) — Markdown
- Contracts (`contracts/`) — Markdown + JSON Schema
- IxQL pipelines (`pipelines/`) — EBNF / IxQL
- Skills (`.claude/skills/<name>/SKILL.md`) — Markdown
- Examples, templates, docs — Markdown + JSON

**Do not add executable code** (Python, TypeScript, Rust, etc.) outside `scripts/`. If you need a script to support governance work, raise an issue first.

**The `scripts/` exception (owner adjudication, 2026-07-23 — CL-817-12):** `scripts/` is the sanctioned home for governance *tooling*: emitters, linters, validators, CI gates, orchestrators, and local coordination transports (e.g. the Galactic live-session bridge). This codifies long-standing practice (~58 scripts referenced by CI and CLAUDE.md at adjudication time). The boundary is purpose, not language: a script must serve the governance of artifacts in this repo or the fleet sessions working on it — Demerzel still ships no product/runtime code, and nothing in `scripts/` may become a dependency of a consumer repo's runtime. Tooling that outgrows this (a long-running service, a product feature, a consumer-facing library) moves to a sibling repo, with Demerzel keeping only the contract and behavioral tests.

---

## Contribution Rules

### Schemas first

Every new artifact type must have a JSON Schema in `schemas/`. Validate your artifact against the schema before submitting.

```bash
# Example validation (Node.js ajv-cli or similar)
ajv validate -s schemas/persona.schema.json -d personas/my-new-persona.yaml
```

### Every persona needs a behavioral test

If you add or modify a persona in `personas/`, you must add or update a corresponding test suite in `tests/behavioral/`. No persona ships without tests.

### Constitutions are append-only

Articles in `constitutions/` may be added or amended, but **removals require explicit written justification** in the PR description. This is not a bureaucratic rule — it is constitutional integrity.

### Source material must be transformed, never copied raw

Anything in `sources/` (transcripts, papers, chat logs, external corpora) must be
distilled into a canonical repo format — a doc, policy, schema, or test — rather
than vendored verbatim. Raw dumps rot, bloat the repo, and carry no governance
provenance. Capture the source wherever you like while working; commit only the
transform, and cite what it came from.

### Every policy carries versioning with explicit rationale

A policy in `policies/` states its version and *why* it changed. A version bump
with no rationale makes the governance history unauditable — the artifact records
what the rule became but not what evidence moved it.

### Conventional commits

Use the conventional commit format. Commit often — at least once per completed task.

```
feat:   new artifact or capability
fix:    correction to an existing artifact
test:   behavioral test additions or changes
docs:   documentation only
chore:  maintenance, formatting, schema bumps
```

Multi-line commits use HEREDOC:

```bash
git commit -m "$(cat <<'EOF'
feat: Add skeptical-auditor persona v1.0.0

Adds the skeptical-auditor persona with full behavioral test suite.
Resolves #42.
EOF
)"
```

### No secrets, ever

Never commit tokens, API keys, credentials, or `.env` files. Bot tokens and secrets belong in `.env` (which is gitignored). See [SECURITY.md](SECURITY.md).

---

## File Placement

| Artifact | Location |
|----------|----------|
| Personas | `personas/<name>.persona.yaml` |
| Behavioral tests | `tests/behavioral/<name>.test.md` |
| Policies | `policies/<name>.policy.yaml` |
| Constitutions | `constitutions/<name>.constitution.md` |
| JSON Schemas | `schemas/<name>.schema.json` |
| IxQL pipelines | `pipelines/<name>.ixql` |
| Skills | `.claude/skills/<name>/SKILL.md` |
| Contracts | `contracts/<name>.contract.md` |
| Docs | `docs/<name>.md` |

---

## Persona Requirements

Every persona MUST include these fields (see `schemas/persona.schema.json`):

- `name` — kebab-case (`^[a-z][a-z0-9-]*$`)
- `version` — semver (`1.0.0`)
- `description` — max 200 characters
- `role`
- `capabilities`
- `constraints`
- `voice` — with `tone`, `verbosity`, and `style`
- `affordances`
- `goal_directedness` — one of: `none`, `task-scoped`, `session-scoped`, `governance-scoped`
- `estimator_pairing` — typically `skeptical-auditor`

---

## Pull Request Checklist

Before opening a PR, confirm:

- [ ] Artifacts validated against their schemas
- [ ] Behavioral tests added or updated (if persona changed)
- [ ] No runtime code introduced
- [ ] No secrets committed
- [ ] Conventional commit messages used
- [ ] Constitutional implications noted (which article does this touch?)

---

## Questions?

Open an issue. If you are uncertain about a contribution, open a **draft PR** and ask for feedback before putting in significant effort.

See also: [CONTEXT.md](CONTEXT.md) for the domain glossary and constitutional
hierarchy. [CLAUDE.md](CLAUDE.md) is a short index that points at both.
