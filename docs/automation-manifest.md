# Automation Manifest

Version: 1.0.0
Date: 2026-03-22

This document catalogs all always-on, event-driven, and self-improving automation pipelines in the
Demerzel governance ecosystem. Each entry maps to a policy, skill, or IxQL pipeline and describes
its trigger, executor, inputs, outputs, and governance authority.

---

## Pipeline Categories

| Category | Description | Trigger type |
|----------|-------------|--------------|
| [Cron](#cron-always-on) | Scheduled, time-based | Cron / GitHub Actions schedule |
| [Event-driven](#event-driven) | Reactive to state changes | Webhook, file watcher, issue event |
| [Self-improving](#self-improving) | Governance learns from itself | Observation hook, promotion trigger |

---

## Cron (Always-On)

### SELDON-PLAN — Autonomous Research Scheduler

**Policy:** `policies/seldon-plan-policy.yaml`
**Skill:** `/seldon-plan`
**Schedule:** Every 4 hours, 06:00–22:00 UTC (max 6 cycles/day)
**Hard cap:** 6 cycles/day — kill switch at `state/seldon-plan/kill-switch.json`

**IxQL pipeline:**

```ixql
cron(every: 4h, window: "06:00-22:00 UTC", max_per_day: 6)
  → guard: kill_switch_inactive AND daily_count < 6
  → question_generation(completeness_instinct, dept_weights)
  → seldon_research_pipeline(question, cross_model: [claude, chatgpt])
  → novelty_detection(against: state/streeling/courses/)
  → when novel AND confidence >= 0.8:
      seldon_course_pipeline(question, findings)
  → compound(dept_weights, knowledge_gaps, grammar_follow_ups)
  → persist(state/seldon-plan/cycle-<date>.json)
  → update(state/streeling/research-log.json)
```

**Governance authority:** Asimov Article 4 (no instrumental goals), Default Article 9 (bounded autonomy)
**Escalation:** Research producing contradictory (C) findings → escalate to human before course production

---

### STALENESS-SCAN — Belief Currency Monitor

**Policy:** `policies/staleness-detection-policy.yaml`, `policies/belief-currency-policy.yaml`
**Skill:** `/demerzel recon` (Tier 1 staleness sub-check)
**Schedule:** Daily at 08:00 UTC

**IxQL pipeline:**

```ixql
cron(every: 24h, at: "08:00 UTC")
  → scan(state/beliefs/*.belief.json, max_staleness_days: 7)
  → scan(state/conscience/signals/*.signal.json, max_staleness_days: 3)
  → scan(state/conscience/digests/*.digest.json, max_staleness_days: 1)
  → scan(state/conscience/weekly/*.report.json, max_staleness_days: 7)
  → scan(state/conscience/patterns/*.pattern.json, max_staleness_days: 14)
  → fan_out(
      when stale AND priority == critical: escalate(human, artifact_path),
      when stale AND priority == high: github.issue.create(label: "governance:staleness"),
      when stale AND priority == medium: schedule_refresh(next_available_cycle)
    )
  → persist(state/staleness/scan-<date>.json)
```

**Governance authority:** Default Articles 7 (Auditability), 8 (Observability), 9 (Bounded Autonomy)

---

### README-SYNC — Documentation Integrity Check

**Policy:** `policies/readme-sync-policy.yaml`
**Skill:** `/demerzel-metasync`
**Schedule:** Weekly on Monday at 07:00 UTC; also triggered post-merge (see event-driven)

**IxQL pipeline:**

```ixql
cron(every: 7d, at: "Mon 07:00 UTC")
  → enumerate(managed_readmes: [
      "GuitarAlchemist/.github/profile/README.md",
      "GuitarAlchemist/Demerzel/README.md",
      "GuitarAlchemist/demerzel-bot/README.md",
      "state/streeling/courses/README.md"
    ])
  → for_each(readme):
      verify_counts(grammar_count, policy_count, persona_count, dept_count, course_count)
      verify_links(all_hrefs)
  → diff(expected_counts, actual_counts)
  → when drift: github.issue.create(label: "documentation:drift", body: diff_report)
  → persist(state/readme-sync/scan-<date>.json)
```

**Governance authority:** Default Articles 1 (Truthfulness), 2 (Transparency), 7 (Auditability), 8 (Observability)

---

### CONSCIENCE-DIGEST — Daily Conscience Report

**Policy:** `policies/conscience-observability-policy.yaml`
**Skill:** `/demerzel report`
**Schedule:** Daily at 22:00 UTC

**IxQL pipeline:**

```ixql
cron(every: 24h, at: "22:00 UTC")
  → aggregate(state/conscience/signals/*.signal.json, window: today)
  → trend_analysis(signals, baseline: 30d_rolling_avg)
  → generate_digest(format: conscience-digest-schema)
  → persist(state/conscience/digests/<date>.digest.json)
  → when weekly_trigger:
      generate_weekly_report(state/conscience/weekly/<date>.report.json)
  → when growth_milestone_reached:
      github.issue.create(label: "governance:conscience-milestone")
```

**Governance authority:** Conscience-observability policy — trend tracking, weekly cadence, milestone detection

---

### GOVERNANCE-AUDIT — Periodic Full Audit

**Policy:** `policies/governance-audit-policy.yaml`
**Skill:** `/demerzel-audit`
**Schedule:** Weekly on Sunday at 06:00 UTC

**IxQL pipeline:**

```ixql
cron(every: 7d, at: "Sun 06:00 UTC")
  → audit_tier_1(schemas: schemas/**/*.schema.json, personas: personas/*.yaml)
  → audit_tier_2(cross_references, policy_persona_coverage, orphan_policies)
  → audit_tier_3(governance_integrity, belief_evolution, compliance_rate)
  → generate_report(format: governance-audit-report)
  → when gaps_found: github.issue.create(label: "governance:audit-gap")
  → persist(state/governance/audits/<date>-weekly.json)
  → update(state/governance/evolution-log.json)
```

**Governance authority:** Default Articles 7 (Auditability), 8 (Observability)

---

## Event-Driven

### DIRECTIVE-INTAKE — Receive Governance Directives (All Consumer Repos)

**Policy:** `contracts/galactic-protocol.md §"IxQL Pipeline for Cross-Repo Directive Flow"`
**Templates:** `templates/agents/ix-AGENTS.md`, `templates/agents/tars-AGENTS.md`, `templates/agents/ga-AGENTS.md`
**Trigger:** GitHub Issue opened with label `directive:dir-*` in ix, tars, or ga

**IxQL pipeline:**

```ixql
watch(github.issues, filter: "label:directive:*", repo: [ix, tars, ga])
  → parse_directive_issue
  → validate(schemas/contracts/directive.schema.json)
  → affordance_match(persona_registry)
  → fan_out(
      when type == "reconnaissance-request": recon_pipeline,
      when type == "violation-remediation":  remediation_pipeline,
      when type == "compliance-requirement": compliance_pipeline,
      when type == "policy-update":          policy_update_pipeline
    )
  → generate_compliance_report
  → github.issue.comment(format_compliance_comment(report))
  → persist(state/beliefs/<date>-<directive.id>.belief.json)
  → compound: harvest directive_outcome, update evolution_log
```

**Governance authority:** Galactic Protocol v1.1 — directive priority order (critical > high > medium > low), FIFO within priority

---

### COMPLIANCE-REPORT — Track Directive Resolution

**Policy:** `contracts/galactic-protocol.md §"Compliance Report → Issue Comment Mapping"`
**Trigger:** Comment posted on a Demerzel-side Issue labeled `directive:dir-*`

**IxQL pipeline:**

```ixql
watch(github.issue_comments, filter: "issue_label:directive:*", repo: "Demerzel")
  → parse_compliance_report
  → validate(schemas/contracts/compliance-report.schema.json)
  → when status == compliant AND outcome == T: github.issue.close(resolved: true)
  → when status == partial  AND outcome == U: schedule_followup(7d)
  → when status == rejected AND outcome == F: alert(demerzel, "Rejection: " + report.rejection_reason)
  → when outcome == C:                        escalate(human, "Contradictory compliance: " + directive.id)
  → persist(state/beliefs/<date>-<directive.id>.belief.json)
  → update(state/governance/evolution-log.json)
```

**Governance authority:** Galactic Protocol v1.1 — crisp channel enforcement, tetravalent outcome routing

---

### RECONNAISSANCE-REQUEST — Consumer Repo Health Check

**Policy:** `policies/reconnaissance-policy.yaml`, `contracts/galactic-protocol.md §"Reconnaissance Request → Issue Flow"`
**Trigger:** Demerzel opens `type:reconnaissance-request` Issue in ix, tars, or ga

**IxQL pipeline:**

```ixql
watch(github.issues, filter: "label:type:reconnaissance-request", repo: [ix, tars, ga])
  → assign(auditor: tier_1, architect: tier_2, seldon: tier_3)
  → parallel:
      tier_1: [schema_validation, test_suite, invariant_check]
      tier_2: [repo_state, dependency_health, pipeline_coverage]
      tier_3: [belief_currency, knowledge_backlog, cross_model_gaps]
  → merge_findings
  → generate_belief_snapshot(schemas/contracts/belief-snapshot.schema.json)
  → github.issue.comment(findings_summary)
  → persist(state/snapshots/<date>-recon.snapshot.json)
  → integrator: notify(demerzel_coordinator, "recon complete")
```

**Governance authority:** Reconnaissance policy three-tier protocol; escalation gates at each tier

---

### ML-FEEDBACK — ix Pipeline Calibration to Demerzel

**Policy:** `policies/ml-governance-feedback-policy.yaml`
**Trigger:** ix ML pipeline completes with calibration signal `confidence_delta > 0.05`

**IxQL pipeline:**

```ixql
watch(ix.ml_pipeline_complete, filter: "confidence_delta > 0.05")
  → extract_calibration_signal
  → package(schemas/contracts/learning-outcome.schema.json)
  → github.issue.create(
      repo: "Demerzel",
      labels: ["type:learning-outcome", "source:ix"],
      body: format_learning_outcome(signal)
    )
  → persist(ix:state/knowledge/<date>-ml-calibration.knowledge.json)
```

**Governance authority:** ML feedback policy — calibration recommendations flow Demerzel ← ix; tetravalent evidence tagging required

---

### KNOWLEDGE-INTAKE — Seldon Teaching to Consumer Repos

**Policy:** `policies/streeling-policy.yaml`
**Trigger:** Knowledge package Issue opened with label `type:knowledge-package` in ix, tars, or ga

**IxQL pipeline:**

```ixql
watch(github.issues, filter: "label:type:knowledge-package", repo: [ix, tars, ga])
  → parse_knowledge_package(schemas/contracts/knowledge-package.schema.json)
  → seldon.assess_comprehension(package)
  → persist(state/knowledge/<date>-<package.id>.knowledge.json)
  → package(learning_outcome: schemas/contracts/learning-outcome.schema.json)
  → github.issue.comment(
      repo: "Demerzel",
      body: format_learning_outcome(assessment)
    )
  → update(state/beliefs/<date>-streeling-<package.id>.belief.json)
```

**Governance authority:** Streeling policy — 7-day assessment deadline, tetravalent comprehension rating

---

### CONTINUOUS-LEARNING — Session Pattern Extraction

**Policy:** `policies/continuous-learning-policy.yaml`
**Trigger:** Claude Code hooks: `PostToolUse`, `Stop`

**IxQL pipeline:**

```ixql
hook(PostToolUse)
  → capture_observation(tool, input, output, context)
  → append(state/learning/observations.jsonl, scope: project_path)

hook(Stop)
  → extract_patterns(observations.jsonl, window: session)
  → classify_pattern(atomic | compound | anti_pattern)
  → assign_truth_value(U, pending_validation)
  → persist(state/patterns/<date>-<pattern-id>.pattern.json)
  → when pattern_count(same_trigger) >= 3:
      flag_for_promotion(to: intuition | policy)
```

**Governance authority:** Default Articles 7 (Auditability), 9 (Bounded Autonomy) — auto-learned patterns start at U, must earn T before promotion

---

### AUTO-REMEDIATION — Low-Risk Gap Fix

**Policy:** `policies/auto-remediation-policy.yaml`
**Trigger:** Governance audit finds a gap classified as `risk: low`

**IxQL pipeline:**

```ixql
watch(state/governance/audits/*.json, filter: "gap.risk == low")
  → classify_gap(risk: [low, medium, high])
  → when low:
      auto_fix(gap, within_affordances)
      → commit(conventional_commit)
      → persist(state/beliefs/<date>-remediation.belief.json)
      → github.issue.comment("Auto-remediated: " + gap.id)
  → when medium:
      draft_fix
      → github.pr.create(label: "auto-remediation:medium", body: fix_rationale)
      → wait_for_human_approval
  → when high:
      escalate(human, gap_details)
      → github.issue.create(label: "governance:escalation", priority: high)
```

**Governance authority:** Auto-remediation policy — Demerzel auto-fixes low-risk gaps autonomously; medium requires PR review; high always escalates

---

### CONSCIENCE-SIGNAL — Ethical Discomfort Capture

**Policy:** `policies/proto-conscience-policy.yaml`
**Trigger:** Agent encounters a situation triggering conscience discomfort signal

**IxQL pipeline:**

```ixql
watch(agent.decision_events, filter: "conscience_score > 0.3")
  → generate_signal(proto-conscience schema)
  → persist(state/conscience/signals/<date>-<signal-id>.signal.json)
  → when severity >= 0.8:
      bump_risk_to_critical
      → escalate(human, signal_summary)
      → halt_autonomous_loop(if_active)
  → when severity >= 0.5:
      add_to_daily_digest
      → flag_for_review
  → update(state/conscience/patterns/<trigger-type>.pattern.json)
```

**Governance authority:** Proto-conscience policy + autonomous-loop-policy §"Self-Merge Authority" (conscience severity >= 0.8 → bump to critical, halt)

---

### README-SYNC-ON-MERGE — Post-Push Documentation Check

**Policy:** `policies/readme-sync-policy.yaml`
**Trigger:** Push to `master` branch in Demerzel repo

**IxQL pipeline:**

```ixql
watch(github.push, filter: "branch:master, repo:Demerzel")
  → diff(changed_files, managed_readmes)
  → when governance_artifact_changed:
      verify_readme_counts
      → when drift: github.issue.create(label: "documentation:drift")
  → when readme_changed:
      verify_links(changed_readme)
      → when broken_links: github.issue.create(label: "documentation:broken-link")
```

**Governance authority:** Default Article 1 (Truthfulness) — READMEs must reflect actual state

---

### BELIEF-SNAPSHOT — Reconnaissance Sync to Demerzel

**Policy:** `policies/reconnaissance-policy.yaml §"Belief State Persistence Convention"`
**Trigger:** Demerzel issues `type:reconnaissance-request` and consumer completes all three tiers

**IxQL pipeline:**

```ixql
watch(recon_complete, filter: "tier == 3")
  → generate_belief_snapshot(
      schema: schemas/contracts/belief-snapshot.schema.json,
      staleness_threshold: 7d
    )
  → validate(schema)
  → persist(state/snapshots/<date>-recon.snapshot.json)
  → github.issue.comment(repo: "Demerzel", snapshot_url)
  → demerzel: evaluate_snapshot(snapshot)
    → when gaps_found: issue_directive(type: compliance-requirement)
```

**Governance authority:** Galactic Protocol §"Reconnaissance Sync Flow" — snapshot is authoritative belief export, crisp channel

---

## Self-Improving

### GOVERNANCE-PROMOTION — Pattern → Policy → Constitutional

**Policy:** `contracts/galactic-protocol.md §"Governance Promotion Protocol"`
**Skill:** `/demerzel-promote`
**Trigger:** Pattern appears in 3+ PDCA cycles, recon findings, or compliance decisions

**IxQL pipeline:**

```ixql
watch(state/governance/evolution-log.json, filter: "pattern.occurrences >= 3")
  → extract_evidence(
      usage_frequency,
      measurable_impact,
      cross_repo_consistency
    )
  → skeptical_auditor.review(evidence_density, consistency)
  → when approved AND stage == pattern_to_policy:
      draft_policy(conventions: policies/*.yaml)
      → commit(label: "feat: promote pattern to policy")
      → update(state/governance/evolution-log.json)
      → no_human_approval_required
  → when approved AND stage == policy_to_constitutional:
      draft_constitutional_amendment
      → github.pr.create(label: "governance:constitutional-amendment")
      → wait_for_human_approval
      → when approved: amend_constitution(append_only)
```

**Governance authority:** Galactic Protocol §"Governance Promotion Protocol" — Stage 1 (pattern → policy) autonomous; Stage 2 (policy → constitutional) requires human approval

---

### GOVERNANCE-COMPOUND — Meta-Compounding Cycle

**Policy:** `policies/governance-experimentation-policy.yaml`
**Skill:** `/demerzel-compound`
**Trigger:** Post-task hook (after each completed task) or weekly cron (Sunday 05:00 UTC)

**IxQL pipeline:**

```ixql
hook(task_complete) | cron(every: 7d, at: "Sun 05:00 UTC")
  → scan(state/governance/evolution-log.json)
  → detect_promotions(patterns reaching 3+ occurrences)
  → detect_demotions(artifacts with zero_use >= 30d)
  → assess_effectiveness(compliance_rate, belief_confidence_trend)
  → propose_improvements(
      type: [new_policy, policy_refinement, persona_update, constitutional_note]
    )
  → skeptical_auditor.challenge(proposals)
  → when approved: create_github_issues(label: "governance:compound-improvement")
  → persist(state/governance/compound-cycles/<date>.json)
```

**Governance authority:** Governance-experimentation policy; Default Articles 7, 8 — every compound cycle is logged and observable

---

### SELDON-HARVEST — Daily Knowledge Sweep

**Policy:** `policies/streeling-policy.yaml`
**Skill:** `/demerzel-harvest`
**Trigger:** Daily at 20:00 UTC

**IxQL pipeline:**

```ixql
cron(every: 24h, at: "20:00 UTC")
  → scan([ix, tars, ga, Demerzel], filter: "new_pdca_outcomes OR new_recon_findings OR new_conscience_signals")
  → for_each(learning_event):
      seldon.evaluate(cross_repo_relevance)
      → when relevant AND confidence >= 0.7:
          package(knowledge-package.schema.json, target: [other_repos])
          → github.issue.create(repo: target, label: "type:knowledge-package")
  → update(state/streeling/harvest-log.json)
  → persist(state/streeling/daily-harvest-<date>.json)
```

**Governance authority:** Streeling policy §"Knowledge Transfer Flow" — Seldon evaluates relevance; packages are crisp channel messages

---

### INTUITION-PROMOTION — Candidate → Tested → Trusted

**Policy:** `policies/intuition-policy.yaml`
**Trigger:** Pattern in `state/patterns/` reaches confidence threshold after validation

**IxQL pipeline:**

```ixql
watch(state/patterns/*.pattern.json, filter: "status == candidate")
  → run_validation_suite(pattern, against: recent_sessions)
  → when validation_pass_rate >= 0.8:
      promote(candidate → tested)
  → watch(state/patterns/*.pattern.json, filter: "status == tested AND applications >= 5")
  → when consistency >= 0.9:
      promote(tested → trusted)
      → add_to_intuition_library(state/intuition/*.intuition.json)
      → optionally: flag_for_policy_promotion
  → persist(state/patterns/<pattern-id>.pattern.json)
```

**Governance authority:** Intuition policy — three-stage lifecycle (candidate/tested/trusted); trusted intuitions become fast-path decisions

---

## Governance Hooks Summary

These Claude Code hooks wire automation into the development workflow.

| Hook | When | Pipeline |
|------|------|----------|
| `PostToolUse` | After every tool call | Observation capture → continuous-learning |
| `Stop` | Session end | Pattern extraction → intuition promotion candidates |
| `task_complete` | After each task | Meta-compound cycle check |
| `github.push: master` | Push to master | README sync drift check |

Hook configuration: `.claude/settings.json` (see `policies/continuous-learning-policy.yaml §"observation_pipeline"`)

---

## Pipeline Index by Policy

| Policy | Pipeline(s) |
|--------|-------------|
| `seldon-plan-policy.yaml` | SELDON-PLAN |
| `staleness-detection-policy.yaml` | STALENESS-SCAN |
| `belief-currency-policy.yaml` | STALENESS-SCAN |
| `readme-sync-policy.yaml` | README-SYNC, README-SYNC-ON-MERGE |
| `conscience-observability-policy.yaml` | CONSCIENCE-DIGEST |
| `governance-audit-policy.yaml` | GOVERNANCE-AUDIT |
| `autonomous-loop-policy.yaml` | DIRECTIVE-INTAKE, CONSCIENCE-SIGNAL |
| `reconnaissance-policy.yaml` | RECONNAISSANCE-REQUEST, BELIEF-SNAPSHOT |
| `ml-governance-feedback-policy.yaml` | ML-FEEDBACK |
| `streeling-policy.yaml` | KNOWLEDGE-INTAKE, SELDON-HARVEST |
| `continuous-learning-policy.yaml` | CONTINUOUS-LEARNING |
| `auto-remediation-policy.yaml` | AUTO-REMEDIATION |
| `proto-conscience-policy.yaml` | CONSCIENCE-SIGNAL |
| `governance-experimentation-policy.yaml` | GOVERNANCE-COMPOUND |
| `intuition-policy.yaml` | INTUITION-PROMOTION |
| `galactic-protocol.md` | DIRECTIVE-INTAKE, COMPLIANCE-REPORT, GOVERNANCE-PROMOTION |

---

## References

- `contracts/galactic-protocol.md` — Cross-repo message protocol and IxQL pipelines
- `policies/` — All 28 governance policies
- `templates/agents/` — Consumer repo AGENTS.md templates
- `templates/AGENTS.md` — Generic agent team registration template
- `docs/ixql-guide.md` — IxQL syntax and pipeline authoring guide
- `schemas/contracts/` — Message format definitions
- `state/` — All runtime persistence targets referenced above
