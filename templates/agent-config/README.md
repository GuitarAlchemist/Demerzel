# Creating a Governed Agent

## Steps

1. **Copy the template:** Copy `agent-template.persona.yaml` to your repo's `personas/` directory
2. **Rename:** Use kebab-case naming: `your-agent-name.persona.yaml`
3. **Fill in all fields:** Replace all placeholder values with your agent's specifics
4. **Validate:** Validate against `schemas/persona.schema.json` from the Demerzel repo
5. **Register with Demerzel:** Demerzel will discover new personas during reconnaissance
6. **Get onboarded:** Seldon will teach your agent about governance requirements

## Required Fields

Your agent MUST have these governance fields:

- `affordances` — What the agent is permitted to do (explicit boundary list)
- `goal_directedness` — How long goals persist (none/task-scoped/session-scoped)
- `estimator_pairing` — Who reviews the agent's decisions (typically skeptical-auditor)

## Behavioral Tests

Every persona should have corresponding behavioral test cases in `tests/behavioral/`. At minimum, test that:

- The agent respects its affordance boundaries
- The agent's goal_directedness is honored (no goal persistence beyond its level)
- The estimator pairing functions (routine decisions are reviewed)

## Governance Compliance

Once registered, your agent must:

- Respond to Demerzel's reconnaissance requests with belief snapshots
- Accept Seldon's knowledge transfers and report comprehension
- Follow the Kaizen PDCA cycle for improvements
- Comply with all constitutional articles and policies
