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

## State Maintenance (MANDATORY)

Recon is not read-only. Every scan MUST update Demerzel's persistent state:

### Before Scanning
1. Read existing beliefs from `state/beliefs/` — check for staleness (> 7 days)
2. Read last recon snapshot from `state/snapshots/` for the target repo (if exists)
3. Compare: what changed since last observation?

### After Scanning
1. **Update or create beliefs** in `state/beliefs/` for every proposition assessed:
   - New findings → new belief file (T/F/U/C with evidence)
   - Changed findings → update existing belief's truth_value, confidence, evidence
   - Stale beliefs → re-evaluate or mark as Unknown
2. **Write recon snapshot** to `state/snapshots/{date}-{repo}-recon.snapshot.json`
3. **Update evolution log** in `state/evolution/` if any governance artifact's effectiveness was assessed
4. **Update oversight** in `state/oversight/` with per-repo compliance status

### File Naming
- Beliefs: `state/beliefs/{date}-{short-description}.belief.json`
- Snapshots: `state/snapshots/{date}-{repo}-recon.snapshot.json`
- Evolution: `state/evolution/{date}-{artifact-name}.evolution.json`

### Staleness Protocol
If any belief in `state/beliefs/` has `last_updated` older than 7 days:
- Flag it in Tier 1 output
- Re-evaluate during this scan if possible
- If cannot re-evaluate → keep but mark confidence -= 0.2

### Schema Compliance
- Beliefs: `logic/tetravalent-state.schema.json`
- Evolution: `logic/governance-evolution.schema.json`
- Snapshots: `schemas/contracts/belief-snapshot.schema.json`

## Source
`policies/reconnaissance-policy.yaml`
