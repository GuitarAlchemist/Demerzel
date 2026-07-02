# Benchmark: OpenClaw and Hermes Patterns for GA Harness

This document evaluates the agentic architectures of OpenClaw and Hermes, extracting reusable control-plane principles for the Guitar Alchemist (GA) Harness and Demerzel Supervisor.

## 1. What should the GA Harness adopt from OpenClaw-style architectures?

The GA Harness should adopt OpenClaw's strong boundary definition and predictability mechanisms:
*   **Explicit Permission Allowlists:** Agents should run in constrained environments where access to the filesystem, network, and execution runtime is explicitly defined, not implicitly granted.
*   **Skills / Tools Registry:** A central, versioned registry of tools prevents agents from hallucinating capabilities and provides a unified interface for policy enforcement.
*   **External Watcher / Kill-Switch:** A dedicated out-of-band process capable of deterministically halting runaway agent behavior is critical for safe autonomous operation.
*   **Channel-Driven Command Ingestion:** Using distinct, structured channels or queues for incoming requests provides better throttling and prioritization than open webhooks or unrestrained loops.

## 2. What should it reject or avoid?

The GA Harness must reject patterns that bypass safety and trust boundaries:
*   **Marketplace / Third-Party Skill Loading without Trust Models:** Dynamically loading community skills introduces unacceptable supply-chain risks. All skills must go through a formal PR and human review process before adoption.
*   **Implicit Trust / Broad Permissions:** The "allow all local access" model is fundamentally unsafe for agentic environments.
*   **Untethered Autonomous Merges:** Agents must never unilaterally merge their own work to production branches (like `master`).

## 3. What should the GA Harness adopt from Hermes-style self-improving agents?

Hermes excels in iterative refinement and capability expansion. The GA Harness should adopt:
*   **Routing Memory Based on Observed Outcomes:** Learning which agent or capability yields the best result for a specific task type (via Seldon's Markov/state-space models) improves efficiency over time.
*   **Skill Extraction after Successful Tasks:** Observing a successful manual or semi-autonomous workflow and proposing it as a new reusable skill (via an automated draft PR).
*   **Autonomous PR Creation:** Allowing the agent to formalize its work into a standard GitHub Pull Request ensures it enters the existing human-in-the-loop review pipeline.
*   **Agent Self-Review (as a pre-flight check):** Having agents critique their own initial drafts to catch obvious errors before submitting for human or adversarial review.

## 4. What should it reject or sandbox?

Self-improvement mechanisms must be strictly sandboxed to prevent unverified behavioral drift:
*   **Always-On Local Agent Loops:** Infinite loops seeking work without bounded constraints violate the "Queue, not loop" Pocock doctrine. Tasks should be discrete, trigger-based (`.trigger.json`), and bounded.
*   **Self-Approval for Merges:** A self-critique does not substitute for an independent adversarial or human review. Agents cannot approve their own PRs.
*   **Auto-Loading Unreviewed Skills:** Extracted skills must be submitted as code (PR) and undergo review. They cannot become active in the runtime instantly.

## 5. How do these patterns affect Demerzel #477 adversarial review policy?

Demerzel #477 defines the independent adversarial review policy. The patterns evaluated here reinforce and expand that policy:
*   **Independence:** The agent that authors the code (e.g., using Hermes-style PR creation) cannot be the same agent (or use the same capability model) that performs the adversarial review.
*   **Policy Gates:** The adversarial review becomes a formal policy gate in the lifecycle. The watcher/kill-switch model acts as a secondary failsafe if the review policy is bypassed or fails.
*   **Self-Critique as Input, Not Output:** Hermes-style self-review becomes a required *pre-condition* before adversarial review #477 is requested, reducing the load on the adversarial tier.

## 6. How do these patterns map to IX, TARS, and the future Supervisor?

*   **IX (Optimize):** Adopts the constrained execution runtime and permission allowlists for running MCP tools. It enforces the sandboxing of any ML capabilities invoked during a task.
*   **TARS (Validate):** Maps to the adversarial review and skill validation. Any extracted skill or self-improving behavior must pass TARS's grammar and theoretical validation.
*   **Demerzel Supervisor:** Acts as the external watcher, command ingestion queue, and routing memory. It enforces the kill-switch, maintains the capability registry, and orchestrates the routing based on Hermes-style memory and OpenClaw-style boundaries.

## Key Sub-Models

### Watcher / Kill-Switch Model
The watcher is an out-of-band daemon independent of the main agent loop. It monitors runtime metrics, token usage, and policy adherence. It uses a deterministic, OS-level signal (e.g., cross-repo halt marker `~/.demerzel/HALT-ALL`) to pause or kill agent processes instantly. This aligns with Demerzel's `demerzel_halt.py` mechanism.

### Skills Model
Skills are explicit, versioned, and registered in a central registry (`schemas/capability-registry.json`). They define their own permission boundaries. They are invoked as "procedures" rather than abstract "abilities" to prevent context window bloat, adhering to the Pocock doctrine.

### Self-Improvement Loop
Self-improvement is framed as *proposal generation*, not direct behavioral mutation. When an agent successfully completes a novel task, a background process extracts the pattern and submits a draft PR containing a new skill definition. The loop is closed only when a human reviews and merges the PR.

### Cost Notes
*   **Free/Local Feasibility:** The watcher daemon, command queues, registry lookups, and routing memory updates are deterministic and can run entirely locally at zero LLM cost.
*   **Paid Justification:** Paid API calls are reserved for the actual heavy reasoning tasks (Hermes-style synthesis or complex tool execution) and the rigorous adversarial review phase, adhering to the Seldon Token Economics model.

## Tracer Bullets (Future Implementation)

1.  **Tracer Bullet 1 (Queue & Watcher):** Implement a simple local watcher script that monitors a `.trigger.json` queue and forcefully halts execution if a synthetic "runaway" condition is detected.
2.  **Tracer Bullet 2 (Explicit Registry):** Create a minimal script that parses a mock capability registry and rejects a tool execution request if the requested tool is not explicitly allowed for that task type.
3.  **Tracer Bullet 3 (Skill Extraction PR):** Build a small prompt pipeline that takes a successful transcript log and generates a mocked markdown file and JSON schema for a proposed new skill.
