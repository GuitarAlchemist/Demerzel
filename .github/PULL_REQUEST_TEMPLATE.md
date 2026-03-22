## What Changed and Why

<!-- Describe what artifacts were added, modified, or removed, and why.
     Link to the issue this resolves: "Resolves #NNN" -->

Resolves #

---

## ERGOL: Who Benefits?

> ERGOL = End-user, Role, Goal, Object, Location/Timeline

- **Consumer(s):** <!-- ix / tars / ga / all / other -->
- **Agent role:** <!-- e.g. skeptical-auditor, curriculum-designer -->
- **Goal enabled:** <!-- what can an agent do now that it couldn't before? -->

---

## Constitutional Alignment

Which article(s) of the [default constitution](../constitutions/default.constitution.md) does this PR touch or support?

- [ ] Article 1 — Truthfulness
- [ ] Article 2 — Transparency
- [ ] Article 3 — Reversibility
- [ ] Article 4 — Proportionality
- [ ] Article 5 — Non-Deception
- [ ] Article 6 — Escalation
- [ ] Article 7 — Auditability
- [ ] Article 8 — Observability
- [ ] Article 9 — Bounded Autonomy
- [ ] Article 10 — Stakeholder Pluralism
- [ ] Article 11 — Ethical Stewardship

---

## Tests

- [ ] Behavioral test added or updated in `tests/behavioral/` (required for persona changes)
- [ ] Schema validation passes (required for new artifact types)
- [ ] No runtime code introduced
- [ ] No secrets committed

---

## MetaSync

Does this PR change artifact counts that appear in `README.md` or `CLAUDE.md`?

- [ ] No count changes
- [ ] Yes — I have updated the relevant counts in README.md / CLAUDE.md

Does this PR add a new artifact type that needs a schema?

- [ ] No new artifact type
- [ ] Yes — schema added at `schemas/<name>.schema.json`

---

## Checklist

- [ ] Conventional commit messages (`feat:` / `fix:` / `test:` / `docs:`)
- [ ] Artifacts placed in the correct directory (see [CONTRIBUTING.md](../CONTRIBUTING.md))
- [ ] Constitution amendments include written justification (if any articles were removed or weakened)
- [ ] Cross-repo impact noted (if ix, tars, or ga need to update their templates)
