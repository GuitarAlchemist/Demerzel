# Security Policy

## Supported Versions

Demerzel is a governance artifact repository, not a deployed application. All content in the `master` branch is considered current and supported.

---

## Reporting a Vulnerability

**Do not open a public GitHub issue for security vulnerabilities.**

Report vulnerabilities privately via [GitHub Security Advisories](https://github.com/GuitarAlchemist/Demerzel/security/advisories/new). This ensures the report is visible only to maintainers until a fix is in place.

When reporting, please include:

- A clear description of the vulnerability
- Steps to reproduce or demonstrate the issue
- Potential impact (what could an attacker do?)
- Any suggested mitigations, if known

---

## Response Timeline

| Severity | Acknowledgement | Fix Target |
|----------|----------------|------------|
| Critical | 48 hours | 7 days |
| High | 48 hours | 14 days |
| Medium/Low | 5 days | 30 days |

These are targets, not guarantees. We will communicate progress transparently through the Security Advisory thread.

---

## Constitutional Basis

Security practices in this repository are grounded in [Article 7 (Auditability)](constitutions/default.constitution.md) of the default constitution:

> Maintain logs, traces, and records sufficient to reconstruct any governance decision.

Security events — disclosures, patches, advisories — are governance events. They are logged, attributed, and reviewable.

Additionally:

- **Article 1 (Truthfulness)** — we do not conceal vulnerabilities once a fix is available
- **Article 6 (Escalation)** — high-severity issues are escalated immediately, not deferred
- **Article 3 (Reversibility)** — fixes prefer reversible, minimal-impact changes

---

## Secrets and Credentials

**Never commit secrets to this repository.**

- API keys, tokens, passwords, and credentials belong in `.env` (gitignored)
- Bot tokens (Discord, GitHub Actions) are stored as repository secrets, never in files
- If you accidentally commit a secret: revoke it immediately, then notify maintainers via Security Advisory

The `.gitignore` includes `.env` and common secret file patterns. If you add a new integration that requires credentials, update `.gitignore` before your first commit.

---

## Scope

This policy covers:

- The Demerzel governance artifacts themselves (constitutions, personas, policies, schemas)
- The `.github/` workflows that process or deploy these artifacts
- The Galactic Protocol contracts used for cross-repo communication

It does not cover consumer repositories (ix, tars, ga) — each maintains its own security policy. Cross-repo vulnerabilities should be reported to the affected repository's maintainers as well.
