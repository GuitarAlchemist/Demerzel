# Tool Gateway

## Concept

The Tool Gateway is a future architectural component designed to decouple Demerzel and her planners from specific, hard-coded tool implementations. Instead of requesting a specific tool (e.g., `ix_search`), agents request a **capability** (e.g., `search`).

The Tool Gateway acts as an intelligent proxy, routing the request to the most appropriate implementation based on:

-   **Capability Fit**: Which tool best satisfies the request?
-   **Permissions**: Does the requesting agent have authority to use this tool?
-   **Cost**: Which tool is the most cost-effective for this specific query?
-   **Risk**: Is the tool's operation safe within the current context?

## Architecture

```text
Demerzel / Planner
  │
  ▼
Tool Gateway (Routing logic, policy enforcement)
  │
  ├─▶ GitHub MCP (Issues, PRs, Discussions)
  ├─▶ Google Drive MCP (Docs, Sheets)
  ├─▶ Ollama (Local LLM)
  ├─▶ DuckDB (Local Analytics)
  ├─▶ Docker/Kubernetes (Compute)
  └─▶ Local Scripts (Custom tools)
```

## Benefits

1.  **Flexibility**: New tools can be added or swapped without modifying the core agents.
2.  **Centralized Governance**: Tool access policies, rate limits, and cost caps are enforced in one place.
3.  **Optimization**: The gateway can choose between a paid LLM tool and a local deterministic tool transparently.
4.  **Auditability**: Every tool invocation is logged with its rationale and outcome.

## Implementation Path (Future)

1.  **Capability Mapping**: Define a formal schema for capabilities and map existing MCP tools to them (extending `schemas/capability-registry.json`).
2.  **Policy Engine**: Implement a policy engine within the gateway to evaluate risk and cost per invocation.
3.  **Discovery API**: Provide an API for agents to discover available capabilities and their associated constraints.
4.  **Routing Implementation**: Implement the actual routing logic that dispatches requests to the underlying MCP servers or local scripts.

## Non-Goals

-   The Tool Gateway is *not* a replacement for the MCP protocol; it is a management layer *above* it.
-   It does not grant tool access without an explicit governance policy.
