# Conversation Hygiene Policy

## Overview
This policy establishes standards for communication and evidence within the GuitarAlchemist ecosystem. It aims to reduce noise, ensure the durability of evidence, and maintain a high signal-to-noise ratio in GitHub issues and pull requests.

## Noise Metrics
Seldon tracks conversation noise using the following metrics:
- **Repetitive Bot Comments**: Multiple comments from the same bot with redundant information.
- **Oversized Comments**: Comments exceeding a reasonable length (e.g., >2000 words) without clear structure.
- **Actionless Content**: Comments that do not contribute to the resolution of the task or provide relevant evidence.
- **Duplicate Status Reports**: Multiple CI/CD or status reports where one consolidated "sticky" comment would suffice.

## Durable Evidence Standards
All claims and findings must be backed by durable evidence.
- **Durable System Memory**: Primary evidence must be stored in stable repository paths (e.g., `state/quality/`, `docs/audits/`) or as workflow artifacts.
- **External Link Policy**:
    - Links to external AI sessions or transient logs are considered **non-durable**.
    - Every non-durable link must have a **durable twin**: a summary or snapshot of the critical evidence stored within the repository.
    - Broken or auth-required external links without a durable summary are flagged as high-risk.

## Recommended Practices
- **Sticky Comment Consolidation**: Bots and workflows should prefer updating a single "sticky" comment per PR rather than creating multiple new comments.
- **Stable Evidence Links**: Comments should link to stable repo paths for long-lived evidence.
- **Actionable Summaries**: Giant logs or complex data should be accompanied by a concise, actionable summary in the comment.

## Enforcement
Demerzel monitors conversation hygiene and may take the following advisory actions:
- **Noise Scoring**: Assign a noise score to PRs and repositories.
- **Consolidation Requests**: Suggest that a bot or workflow switch to a sticky comment model.
- **Deduction in Reliability Score**: Workers that frequently produce non-durable evidence or high noise will see a reduction in their `worker_capability_fact` reliability score.
- **Human Escalation**: Significant breaches of hygiene (e.g., "bot storms") trigger immediate human notification.
