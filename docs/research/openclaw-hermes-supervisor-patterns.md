# Research: OpenClaw and Hermes Patterns for the GA Harness

**Status:** Research / Draft
**Date:** 2026-06-20
**Related Issues:** #475, #477
**Area:** Agent Governance / Supervisor Design

## Executive Summary

This research benchmarks OpenClaw-style and Hermes-style agent patterns against the Guitar Alchemist (GA) Harness and the Demerzel Supervisor design. We evaluate reusable control-plane principles for agent skills, orchestration, safety, and self-improvement without cloning either project or introducing external dependencies.

## Pattern Analysis

### 1. OpenClaw-style Patterns (Control-Plane & Safety)

OpenClaw emphasizes a robust, always-on orchestration layer with explicit permission boundaries.

*   **Always-on local agent loop:** OpenClaw patterns suggest a daemon-like process that listens for events.
    *   *Supervisor Implication:* The GA Harness should adopt the *monitoring* aspect of the always-on loop but reject autonomous execution without human-in-the-loop (HITL) gates.
*   **External watcher / kill-switch:** A separate process that can halt the agent ecosystem.
    *   *Supervisor Implication:* This aligns perfectly with Demerzel's `HALT-ALL` marker. We should extend this to support granular "soft-halts" and per-agent suspension.
*   **Explicit permission allowlists:** Granular control over tool use and file system access.
    *   *Supervisor Implication:* Demerzel already uses policies and constitutions. We should adopt the pattern of *explicit capability registration* where tools must be declared in the persona and verified against a policy allowlist.

### 2. Hermes-style Patterns (Self-Improvement & Memory)

Hermes focuses on self-improving agents that learn from successful outcomes and refine their own skills.

*   **Skill extraction after successful tasks:** Identifying reusable patterns from a solved problem and formalizing them as a skill.
    *   *Supervisor Implication:* This is a high-value adaptation. Successful PDCA cycles should trigger a "Skill Extraction" stage where a sub-agent (e.g., Seldon) drafts a new `.claude/skills/` entry.
*   **Routing memory based on observed outcomes:** Using historical performance data to choose the best agent or tool for a task.
    *   *Supervisor Implication:* Maps to Demerzel's "Belief State" and "Routing Memory". We should adopt outcome-aware routing in the `SemanticRouter`.
*   **Agent self-review / Adversarial review:** Using a secondary agent to critique the primary agent's work.
    *   *Supervisor Implication:* Directly supports Demerzel #477. We should formalize the "Adversarial Auditor" persona to perform zero-trust reviews.

## Implications for Demerzel #477 (Adversarial Review)

Adopting these patterns strengthens the adversarial review policy by:
1.  **Isolating the Auditor:** The Auditor must run in a separate sandbox (Hermes pattern) with no write access to the primary agent's state.
2.  **Evidence-based Verdicts:** Reviewers must provide evidence from the "Routing Memory" to justify rejection.
3.  **Recursive Improvement:** The review process itself should be subject to a self-improvement loop (skill extraction for better auditing).

## Future Supervisor Mapping

*   **IX (Rust ML):** Enforces hard constitutional gates on tool calls. Adopts OpenClaw allowlists.
*   **TARS (F# Validator):** Implements the Hermes self-review loop using tetravalent logic.
*   **GA (Harness):** Provides the "Channel-driven command ingestion" (e.g., GitHub Actions, CLI) and coordinates the "Always-on" monitoring state.

## Tracer Bullets for Implementation

1.  **Tracer 1: Always-On Observability Sidecar.** A lightweight Python script that monitors `state/` changes and updates a local "Supervisor Health" dashboard without interfering with active agents.
2.  **Tracer 2: Skill-Extraction Hook.** A PostToolUse hook that, upon detecting a successful complex task completion, prompts the user to "Distill this solution into a skill".
3.  **Tracer 3: Granular Kill-Switch.** Enhancing `demerzel_halt.py` to support `halt --agent <name>` or `halt --repo <repo>`, allowing partial ecosystem operation during incident response.

## Cost Notes

*   **Free/Local Feasibility:** Most orchestration and pattern matching (Skill Extraction) can be performed by local models (e.g., Llama 3, Phi-3) or cheap "Haiku-tier" APIs.
*   **Paid Model Justification:** High-stakes "Adversarial Review" and final "Skill Refinement" justify the use of Frontier models (Opus/Sonnet) to ensure governance integrity.
