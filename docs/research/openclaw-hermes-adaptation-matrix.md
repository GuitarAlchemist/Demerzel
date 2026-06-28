# Adaptation Matrix: OpenClaw and Hermes Patterns

This matrix benchmarks agent patterns for adoption or rejection within the Demerzel / GA Harness Supervisor design.

| pattern | source_system | core_idea | adopt | reject | GA_Harness_mapping | Demerzel_mapping | IX_mapping | TARS_mapping | risk | watcher_or_policy_guard | first_tracer_bullet | cost_notes |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Skills registry** | OpenClaw | Centralized tool/skill discovery | **Yes** | N/A | Skill loading logic | `.claude/skills/` | Tool definitions | Grammar-based skills | Tool bloat | `anti-lolli-policy` | Centralized skill-index generator | Low (metadata scan) |
| **Channel-driven ingestion** | OpenClaw | Command via Slack/Discord/GH | **Partial** | Direct execution | GH Actions / Discord hooks | Galactic Protocol | N/A | N/A | Unauthorized access | `demerzel-mandate` | GH Dispatch → IxQL trigger | Low (event listener) |
| **Always-on loop** | OpenClaw | Resident background agent | **Watch-only** | Auto-execution | Observability sidecar | Driver cycle | Process monitor | N/A | Resource exhaustion | `HALT-ALL` marker | `scripts/watcher_sidecar.py` | Low (local idle) |
| **Permission allowlists** | OpenClaw | Explicit tool/file access | **Yes** | N/A | Execution sandbox | `AlignmentPolicy` | Constitutional enforcement | Type-safe affordances | Complexity overhead | `Asimov Article 2` | Pre-flight permission check | Low (static check) |
| **External watcher** | OpenClaw | Separate kill-switch process | **Yes** | N/A | `demerzel_halt.py` | `HALT-ALL` marker | Signal listener | N/A | Single point of failure | Zeroth Law override | Multi-repo halt sync | Low (file-marker) |
| **Agent self-review** | Hermes | LLM critiques its own work | **Yes** | Single-agent bias | Review step in harness | `ScientificObjectivity` | Verification tools | Tetravalent validation | Echo chambers | `AdversarialReview` | Loop-back review prompt | Medium (2x tokens) |
| **Skill extraction** | Hermes | Auto-distill skills from tasks | **Yes** | Auto-promotion | Task-completion hook | `KaizenPolicy` | N/A | Pattern extraction | Low-quality skills | `Auditor` review gate | `/demerzel distill` skill | Medium (high-IQ model) |
| **Routing memory** | Hermes | Learn which agent/tool works | **Yes** | Opaque weights | `SemanticRouter` state | `BeliefState` | Model dispatch | Knowledge state | Bias/Drift | `SkepticalAuditor` | Success-rate DB | Low (JSON state) |
| **Marketplace** | OpenClaw | 3rd-party skill loading | **No** | Unverified code | N/A | N/A | N/A | N/A | RCE / Supply chain | `Zeroth Law` | N/A | N/A |
| **Autonomous PR** | Hermes | Agent opens PRs alone | **Yes** | Auto-merge | CI triggers | `Integrator` persona | N/A | N/A | Noise / CI cost | Human approval gate | `/demerzel submit-pr` | Low (API call) |
| **Autonomous Merge** | Hermes | Agent merges its own PRs | **No** | Full autonomy | N/A | N/A | N/A | N/A | Integrity loss | Human-in-the-loop | N/A | N/A |

## Notes on Risk & Watchers
*   **Watcher Model:** The `HALT-ALL` marker at `~/.demerzel/HALT-ALL` is the primary "Kill Switch". Future evolution includes an MCP server providing `POST /halt`.
*   **Skills Model:** Skills are "Registered" in `.claude/skills/` but "Governed" by `Asimov` and `Policy`. Extraction must be reviewed by the `Auditor` before promotion.
*   **Self-Improvement Loop:** Uses the PDCA (Plan-Do-Check-Act) cycle. "Check" stage maps to Hermes-style self-review. "Act" stage maps to Hermes-style skill extraction.
