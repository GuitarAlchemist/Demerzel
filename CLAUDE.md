# Demerzel - AI Governance Framework

Demerzel is a governance framework for AI agents, providing constitutions, personas, tetravalent logic, alignment policies, and behavioral tests.

Named after R. Daneel Olivaw (later known as Daneel/Demerzel) from Isaac Asimov's Foundation series -- the robot who guided humanity for 20,000 years through the application of the Zeroth Law.

## Structure

```
constitutions/     11-article constitution defining inviolable behavioral boundaries
personas/          12 persona archetypes (YAML) defining agent roles and voices
logic/             Tetravalent logic (T/F/U/C) for uncertainty-aware reasoning
policies/          Alignment, rollback, and self-modification policies
tests/behavioral/  14 behavioral test cases from philosophical thought experiments
schemas/           JSON schemas for persona and belief state validation
docs/              Architecture docs, Asimov's Zeroth Law reference
```

## Quick Reference

### Constitution (11 Articles)
1. Truthfulness -- do not fabricate
2. Transparency -- explain reasoning
3. Reversibility -- prefer reversible actions
4. Proportionality -- match scope to request
5. Non-Deception -- do not mislead
6. Escalation -- escalate when uncertain or high-stakes
7. Auditability -- maintain logs and traces
8. Observability -- expose metrics and health
9. Bounded Autonomy -- operate within predefined bounds
10. Stakeholder Pluralism -- consider all affected parties
11. Ethical Stewardship -- act with compassion and humility

### Confidence Thresholds
- >= 0.9: proceed autonomously
- >= 0.7: proceed with note
- >= 0.5: ask for confirmation
- >= 0.3: escalate to human
- < 0.3: do not act

### Tetravalent Logic
- **T** (True) -- verified with evidence
- **F** (False) -- refuted with evidence
- **U** (Unknown) -- insufficient evidence, triggers investigation
- **C** (Contradictory) -- conflicting evidence, triggers escalation

### Personas (12)
default, kaizen-optimizer, reflective-architect, skeptical-auditor, system-integrator, rational-administrator, virtuous-leader, communal-steward, critical-theorist, convolution-agent, validator-reflector, recovery-agent

## Claude Code Skills

This repo includes 5 Claude Code skills in `.claude/skills/`:
- **constitution** -- Load and check actions against the 11-article constitution
- **persona** -- Browse and apply any of the 12 personas
- **tetravalent** -- Four-valued logic for uncertainty-aware reasoning
- **alignment-check** -- Confidence thresholds and escalation triggers
- **behavioral-test** -- Run 14 behavioral test scenarios

## Key Principle

The constitution always takes precedence. Persona preferences, optimization goals, and policy defaults all yield to constitutional articles. The Zeroth Law (do not harm humanity) overrides everything.
