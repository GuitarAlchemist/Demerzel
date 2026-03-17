---
name: seldon-deliver
description: Package and deliver cross-repo knowledge — wrap learnings as knowledge packages for the Galactic Protocol
---

# Seldon Deliver

Package experiential and domain knowledge for cross-repo delivery via the Galactic Protocol.

## Usage
`/seldon deliver [finding] [target-repos]`

## Process
1. Classify the finding by knowledge layer (governance/experiential/domain)
2. Create a knowledge package per `schemas/contracts/knowledge-package.schema.json`
3. Set delivery_mode based on target learner type
4. Set source reference (artifact, pdca_cycle, five_whys, or reconnaissance)
5. Deliver via Galactic Protocol to target repos

## When to Use
- PDCA cycle completed with useful outcome → share with other repos
- 5 Whys found root cause applicable elsewhere → share finding
- Reconnaissance discovered pattern → share as governance knowledge
- New domain technique learned → share with adjacent domains

## Cross-Repo Relevance Check
Before delivering, assess: would this knowledge help agents in the target repo?
- ix finding about ML tool patterns → relevant to tars (reasoning) and ga (chatbot)
- ga music theory insight → probably NOT relevant to ix
- Governance finding → relevant to ALL repos

## Source
`policies/streeling-policy.yaml`, `schemas/contracts/knowledge-package.schema.json`, `contracts/galactic-protocol.md`
