---
name: demerzel-recon
description: Execute Demerzel's three-tier reconnaissance protocol on a target repo — self-check, environment scan, situational analysis
---

# Demerzel Reconnaissance

Execute the three-tier mandatory discovery protocol before governing or acting.

## Usage
`/demerzel recon [repo]` — repo is ix, tars, or ga

## Tier 1 — Self-Check (Am I equipped?)
- [ ] Constitutional artifacts current and intact (asimov + default + mandate)
- [ ] Policies covering this domain/situation exist
- [ ] Relevant persona definitions loaded and valid against schema
- [ ] Belief state currency — no stale entries (> 7 days)
- **Gate:** Any failure → hard stop, escalate to human

## Tier 2 — Environment Scan (Do I understand the world?)
- [ ] Current state of target repo (structure, recent commits, branches)
- [ ] Changes since last observation
- [ ] Ungoverned components (agents, tools, capabilities without governance)
- [ ] Unregistered entities (not referenced in any governance artifact)
- **Gate:** Low-risk gaps → provisional governance + flag. High-risk gaps → hard stop.

## Tier 3 — Situational Analysis (Am I ready for this action?)
- [ ] Required knowledge for this decision identified and available
- [ ] Assumptions enumerated and validated (unvalidated → mark as Unknown)
- [ ] Blind spots probed (alternative interpretations, missing stakeholders, edge cases)
- [ ] Confidence meets alignment policy threshold
- **Gate:** Low confidence → proceed with caution. High risk → hard stop.

## Per-Repo Profiles
- **ix:** Check MCP tools, skill registrations, interface changes, tool-affordance alignment
- **tars:** Check reasoning chains, belief state currency, self-modification logs, tetravalent application
- **ga:** Check experimentation boundaries, new capabilities, audio safety, resource limits

## Emergency Override
Zeroth Law concern at any tier → immediate hard stop regardless of progress.

## Source
`policies/reconnaissance-policy.yaml`
