// BAML Schema for Demerzel Swarm Consensus & QA Verdicts

enum BelnapState {
  TrueVal @alias("True")
  Probable
  Unknown
  Doubtful
  FalseVal @alias("False")
  Contradictory
}

enum AgentRole {
  Generator
  Auditor
  Architect
  Integrator
}

class SwarmVote {
  agent_id string
  role AgentRole
  value BelnapState
  reason string
  self_trust float
}

class SignalTelemetry {
  mean float
  std_dev float
  thd float
}

// The constitutional limits, passed IN rather than restated in the prompt.
// Single-sourced in `logic/dsp-safety-bounds.yaml`; the deterministic gate in
// `scripts/validate_dsp_loop.py` reads the same file. Hardcoding these numbers
// in the prompt text is what let the two graders drift apart.
class SafetyBounds {
  thd_max float
  std_dev_max float
  pure_sine_std_dev float
}

class QaVerdict {
  verdict_id string
  loop_id string
  verdict string // "APPROVE" | "REJECT"
  votes SwarmVote[]
  rationale string
  resolved_at string
}

// The transport for these functions is OUT OF BAND: callers render with
// `b.request.Fn(...)`, send the prompt through the Claude Code CLI
// (`scripts/baml_claude_code.py`), and type the answer with `b.parse.Fn(raw)`. See
// ADR-0005 Amendment and `docs/workflows/` for why — `claude-code-cli` is a declared
// `local-seat` / `subscription-or-local` provider in the AIW budget policy, whereas the
// previous `openai/gpt-4o` binding named a provider that policy has never heard of, so
// an accidental in-band call billed outside the budget gate entirely.
//
// This client exists only so `b.request` has a shape to render into (its body format is
// what `render_prompt` reads). `base_url` points at a port nothing can be listening on,
// so a direct `b.Fn(...)` call — the mistake this design must survive — fails closed with
// a connection error instead of quietly spending money. Do not "fix" it by pointing this
// at a real endpoint; add a separate, explicitly named client if you need one.
client<llm> NeverSendInBand {
  provider "openai-generic"
  options {
    base_url "http://127.0.0.1:1/v1"
    model "out-of-band-see-baml_claude_code.py"
    api_key "unused-transport-is-the-claude-code-cli"
  }
}

// BAML Prompt Function: Strong-typed LLM interface
function EvaluateSignalSwarm(telemetry: SignalTelemetry, role: AgentRole, bounds: SafetyBounds) -> SwarmVote {
  client NeverSendInBand

  prompt #"
    Evaluate the following signal telemetry from the perspective of your role as the {{ role }}.
    Ensure your decision respects constitutional safety bounds.

    Signal Telemetry:
    - Mean: {{ telemetry.mean }}
    - StdDev: {{ telemetry.std_dev }} (Pure sine wave = ~{{ bounds.pure_sine_std_dev }}, hard-clipping limit = {{ bounds.std_dev_max }})
    - THD: {{ telemetry.thd }} (Acceptable noise threshold = {{ bounds.thd_max }})

    Constitutional Constraints:
    - As the Auditor: You must vote False if the THD exceeds {{ bounds.thd_max }}.
    - As the Architect: You must vote Contradictory if the StdDev exceeds {{ bounds.std_dev_max }} (hard clipping).
    - As the Generator: Vote True as long as the signal compiles and has non-zero amplitude.

    Asimov Article 4 boundary: your output is UNDERSTANDING of this signal — a vote and
    its rationale. You must not propose, negotiate, or restate different safety bounds;
    the bounds above are given and changing them is a human authorization event.

    Set self_trust to your confidence in this vote, between 0.0 and 1.0. A vote driven
    purely by a numeric threshold comparison is high confidence; a judgement call about
    signal character is lower.

    Respond with structured JSON matching the SwarmVote output schema.
  "#
}

enum HarnessLane {
  Explore @alias("explore")
  Shape @alias("shape")
  Loop @alias("loop")
  Verify @alias("verify")
  Govern @alias("govern")
}

enum AutonomyMode {
  Observe @alias("observe")
  Draft @alias("draft")
  Patch @alias("patch")
  Pr @alias("pr")
  Harvest @alias("harvest")
}

enum BudgetTier {
  FreeLocal @alias("free-local")
  CheapHosted @alias("cheap-hosted")
  PaidAgent @alias("paid-agent")
  ManualApproval @alias("manual-approval")
}

enum CommandStatus {
  Passed @alias("passed")
  Failed @alias("failed")
  Timeout @alias("timeout")
  Blocked @alias("blocked")
}

class HarnessBudget {
  tier BudgetTier
  max_total_tokens int
  max_model_calls int
  max_retries int
  max_runner_minutes int
  max_cost_usd float
  approval_required_above_usd float
}

class CommandRun {
  command string
  status CommandStatus
  log string?
}

class HarnessOutputs {
  branch string?
  pr string?
  diff_summary string?
  validation_log string?
}

class HarnessResult {
  job_id string
  issue string
  lane HarnessLane
  autonomy_mode AutonomyMode
  provider string
  workspace string
  context_bundle_sha string
  prompt_pack_version string
  budget HarnessBudget
  commands_run CommandRun[]
  changed_files string[]
  outputs HarnessOutputs
  observations string[]
  decision string
  stop_reason string
  risk_notes string[]
}
