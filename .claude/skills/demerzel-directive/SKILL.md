---
name: demerzel-directive
description: Issue a Demerzel governance directive via the Galactic Protocol — compliance requirements, policy updates, violation remediations, reconnaissance requests
---

# Demerzel Governance Directive

Issue a formal governance directive from Demerzel to a consumer repo agent.

## Usage
`/demerzel directive [type] [repo]`

## Directive Types
| Type | Purpose | Priority |
|------|---------|----------|
| `compliance-requirement` | Require adherence to a constitutional article or policy | medium-high |
| `policy-update` | Notify of governance artifact changes | medium |
| `violation-remediation` | Require fix for a detected governance violation | high-critical |
| `reconnaissance-request` | Request belief snapshot + compliance report | medium |

## Creating a Directive
1. Identify the governance concern (what needs to happen)
2. Cite the source article (which constitution/policy authorizes this)
3. Classify priority (critical/high/medium/low)
4. Specify target repo (ix/tars/ga) and optionally target agent
5. If `target_agent` is omitted, Demerzel performs affordance matching
6. Write the directive content (what the consumer must do)
7. Format as JSON conforming to `schemas/contracts/directive.schema.json`

## Rejection Rules
Consumer may reject a directive with constitutional justification:
- **First Law override:** Directive would cause harm (data/trust/autonomy harm)
- **Second Law override:** Human operator has explicitly countermanded
Both require logged reasoning with specific constitutional citations.

## Example
See `examples/sample-data/directive-violation-remediation.json`

## Source
`schemas/contracts/directive.schema.json`, `contracts/galactic-protocol.md`
