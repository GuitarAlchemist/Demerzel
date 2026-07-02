# Demerzel Advisory Decisions

## Overview
Demerzel Advisory Decisions are the primary output of the GitHub Intelligence Pipeline's governance layer. They provide actionable recommendations based on empirical evidence from Streeling and Seldon.

## Decision Principles
- **Evidence-Based**: Every decision must reference specific Streeling event IDs or Seldon fact IDs.
- **Advisory Nature**: Decisions are recommendations. Demerzel does not automate high-risk actions (like merging or code push) without human-in-the-loop (HITL) approval.
- **Transparency**: The reasons for a decision must be explicitly stated in the `reasons` field.
- **Confidence Calibration**: Every decision includes a confidence score (0 to 1). Decisions with low confidence should trigger human review.

## Decision Types
- **route**: Recommends a specific worker or team for a task based on capability scores and availability.
- **hold**: Recommends pausing a workflow due to CI failures, collision risk, or missing evidence.
- **request_review**: Recommends specific reviewers (human or agent) based on their expertise and historical effectiveness.
- **escalate**: Recommends human intervention when automated logic reaches a contradiction or low-confidence state.
- **recommend_merge**: Signifies that all governance gates (CI, review, policy) have been passed and the PR is ready for human merge.
- **no_action**: Explicitly states that no intervention is currently required.

## Allowed MVP Actions
In the initial implementation, Demerzel's advisory decisions may trigger the following low-risk actions:
- **Produce a report**: Generate a summary of PR health or worker performance.
- **Suggest labels**: Recommend adding or removing labels based on entity state.
- **Suggest reviewer/capability**: Add a comment suggesting a specific reviewer or required capability.
- **Suggest hold-for-CI**: Add a comment suggesting a hold until CI passes.
- **Suggest adversarial review**: Recommend a security or logic review by a specialized worker.
- **Suggest human escalation**: Flag an issue or PR for manual attention.

## Disallowed MVP Actions
To ensure safety and maintain the HITL principle, the following actions are strictly prohibited in the MVP:
- **Auto-merge**: Merging PRs without human approval.
- **Push code**: Directly committing code to a branch.
- **Change branch protection**: Modifying repository security settings.
- **Grant worker permissions**: Elevating access levels for AI workers.
- **Mutate issues/PRs**: Any mutation beyond labeling or commenting without an explicit follow-up policy.
