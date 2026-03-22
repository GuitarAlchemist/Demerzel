# AI-Native Software Engineering at Intrado

*A thesis for engineering leadership — March 2026*

---

## Executive Summary

Intrado processes 410 million 911 transactions per year across 6,000+ PSAPs. The software behind those transactions was built by humans writing code, humans reviewing code, and humans testing code. That model worked for 45 years.

It will not work for the next five.

NG911 is multiplying complexity — multimedia streams, IoT device calls (projected 33% of emergency calls by end of 2026), real-time AI translation across dozens of languages, and cloud migration of mission-critical infrastructure. Meanwhile, every major competitor is deploying AI into their engineering pipelines. Axon acquired Prepared (an AI-powered 911 platform) in October 2025. The question is not whether AI changes how we build emergency services software. The question is whether we lead that change or react to it.

This document lays out what AI-native software engineering looks like, why it matters specifically for life-safety systems, what it costs, what it risks, and what to do Monday morning.

---

## 1. The Problem: Faster Coding Is Not the Answer

Most organizations adopt AI by giving developers a code-completion tool and calling it transformation. Here is what that actually produces:

| What they measure | What actually happens |
|---|---|
| 100 PRs merged this week | 12 PRs that users noticed |
| 500 tests passing | 30 tests that catch real bugs |
| Velocity up 40% | Customer satisfaction unchanged |
| 20 features shipped | 3 features customers asked for |

This is Amdahl's Law applied to software. Coding is roughly 30% of delivery. If you make coding infinitely fast, maximum total speedup is 1.43x — because the other 70% (requirements, review, testing, deployment, compliance) still takes the same time. You built the wrong thing faster.

**For Intrado specifically:** We likely have thousands of tests across our product lines. More tests do not mean more safety. What matters is whether those tests cover actual failure modes — call routing failures under load, location accuracy degradation, failover scenarios during network partitions. AI can generate 500 tests in an hour. But if none of them simulate a real PSAP failover, they are activity, not safety.

**So what?** Code acceleration alone is a trap. The opportunity is using AI across the entire delivery pipeline — requirements validation, architecture review, compliance checking, test design, deployment monitoring — not just code generation.

**What do we do Monday?** Audit one product line. Map the actual delivery pipeline end to end. Measure where time is spent. The bottleneck is almost certainly not "writing code."

---

## 2. What AI-Native Actually Means

"AI-assisted" means a developer uses Copilot to autocomplete functions. "AI-native" means AI is a first-class participant in the engineering process — with defined roles, clear boundaries, and governance.

### The Multi-Model Approach

No single AI model is best at everything. The most effective approach uses different models for different strengths:

| Model | Role | Why |
|---|---|---|
| Claude (Opus) | Architecture, governance, synthesis, writing | Strongest at reasoning about complex systems and maintaining context across large codebases |
| GPT | Second opinions, enterprise pattern matching | Different training data catches blind spots Claude misses |
| Gemini | Research breadth, documentation analysis | Google's model excels at synthesizing across large document sets |
| Codex / Claude Code | Execution — writing, testing, deploying code | Purpose-built for code generation and tooling |

This is not theoretical. In experimental use across a multi-repo engineering ecosystem, multi-model orchestration consistently caught issues that single-model approaches missed. One model's confident wrong answer is another model's obvious red flag.

**For Intrado:** A compliance review that runs the same NENA i3 specification through two independent models will catch interpretation errors that a single model would present with false confidence. This is the same principle as independent verification in aviation — two pilots, two readings of the same instrument.

**So what?** Single-model AI is a tool. Multi-model AI is a team. The cost difference is marginal. The error-detection improvement is significant.

**What do we do Monday?** Pick one compliance-checking workflow. Run it through two models independently. Compare where they disagree. That disagreement set is where your current process has hidden risk.

---

## 3. Governance Makes AI More Productive, Not Less

The instinct with AI is to minimize guardrails to maximize speed. In life-safety software, this instinct is exactly wrong.

### The Constitutional Hierarchy

Effective AI governance mirrors how we already think about Intrado's obligations, just made explicit and enforceable:

```
Level 0: Immutable Laws (never violate)
  → Never drop a 911 call
  → Never misroute an emergency
  → Never expose caller data
  → Always fail to a human operator

Level 1: Operational Ethics (always follow)
  → Explain your reasoning (auditability)
  → Prefer reversible actions
  → Escalate when uncertain

Level 2: Policies (usually follow)
  → Code style, testing standards, deployment procedures

Level 3: Preferences (follow when convenient)
  → Agent-specific behaviors, formatting, verbosity
```

Higher levels always override lower levels. An AI agent that finds a clever optimization that might drop calls under edge conditions is constitutionally blocked from deploying it — no human review needed for that rejection.

### Confidence-Based Escalation

Instead of binary "AI decides" or "human decides," use a confidence spectrum:

| Confidence | Action | Example |
|---|---|---|
| >= 0.9 | Proceed autonomously | Formatting fix, dependency update with passing tests |
| >= 0.7 | Proceed with note to team | Refactoring with full test coverage |
| >= 0.5 | Ask for confirmation | API change, new integration |
| >= 0.3 | Escalate to human | Anything touching call routing logic |
| < 0.3 | Do not act | Insufficient understanding, stop and report |

**For Intrado:** This maps directly to our criticality tiers. Text-to-911 processing (high volume, lower per-transaction criticality) can tolerate higher AI autonomy. Core call routing (every failure is a potential life-safety incident) requires lower thresholds and mandatory human review.

**So what?** Governance is not overhead. It is the mechanism that lets AI move fast on low-risk work *because* it is provably constrained on high-risk work. Without governance, you either restrict AI everywhere (slow) or trust it everywhere (dangerous).

**What do we do Monday?** Classify one product's codebase into criticality tiers. Define which tiers AI can modify autonomously, which need human review, and which are AI-excluded. This classification exercise alone will clarify your risk model.

---

## 4. Handling Uncertainty in Life-Safety Systems

Standard software engineering treats everything as true or false. Tests pass or fail. Features are done or not done. This works for most software. It does not work for emergency services.

### Four-Valued Logic for 911

When a 911 call comes in with location data, four things can be true:

- **True (T):** Location verified by multiple sources (GPS + cell tower + ALI database). Route with confidence.
- **False (F):** Location data is demonstrably wrong (coordinates in the ocean for a land-based call). Flag and escalate.
- **Unknown (U):** Insufficient data to determine location. This is NOT "probably fine." This triggers mandatory human intervention.
- **Contradictory (C):** GPS says one location, cell tower says another, ALI says a third. Conflicting evidence. Escalate immediately with all sources visible.

The critical insight: **Unknown is not a failure state. It is an information state that demands a specific response.** Most software treats "I don't know" as an error. Life-safety software must treat "I don't know" as a first-class condition with its own handling path.

**For Intrado:** Every system that makes routing decisions should distinguish between "I'm confident this is right," "I'm confident this is wrong," "I don't have enough information," and "my information sources contradict each other." Each state has a different correct response. Collapsing them into pass/fail is how silent failures happen.

**So what?** Four-valued logic is not academic. It is a concrete engineering pattern that prevents the specific class of failures that kill people — the ones where the system guessed instead of escalating.

**What do we do Monday?** Review one call routing decision point. Map its current logic. Identify where it treats "unknown" as "true" by default. That is your highest-priority fix.

---

## 5. Concrete Intrado Applications

Here are four places where AI-native engineering delivers measurable value, ordered from lowest risk to highest impact.

### Tier 1: Test Intelligence (Start Here)

**Problem:** Thousands of tests exist. Unknown percentage cover real failure modes.
**AI Application:** Analyze existing test suites against actual incident reports and production failure patterns. Identify gaps where real failures occurred but no test would have caught them.
**Metric:** Percentage of past-year production incidents that would have been caught by the current test suite. Target: identify and fill gaps to reach 80%.
**Risk:** Low. Read-only analysis of existing artifacts.

### Tier 2: Compliance Automation

**Problem:** NENA i3 compliance, FCC mandates, and state-level 911 requirements require manual review of specifications against implementation.
**AI Application:** Automated compliance checking — parse regulatory requirements, map them to code paths, flag gaps. Intrado already deploys AI-based text translation for Text-2-911 in Columbus, OH. The same multi-language AI capability that translates caller messages can be applied to translating compliance requirements into test cases.
**Metric:** Time from regulation change to verified compliance. Current: weeks to months. Target: days.
**Risk:** Medium. AI assists but humans certify. Misinterpreted requirements caught by dual-model review.

### Tier 3: Incident Response Acceleration

**Problem:** When a production incident occurs in call routing, engineers need to understand complex system interactions under time pressure.
**AI Application:** Incident response agent that correlates logs, identifies affected PSAPs, traces call paths, and presents a structured situation report within minutes of alert.
**Metric:** Mean time to understand (not resolve — understand) an incident. Target: 50% reduction.
**Risk:** Medium. AI provides analysis, humans make decisions. Wrong analysis is caught by the same engineering review that exists today.

### Tier 4: NG911 Migration Tooling

**Problem:** Migrating 1,000+ networks from legacy to NG911 is a multi-year effort with high per-migration engineering cost.
**AI Application:** Migration analysis agents that assess each network's current state, generate migration plans, identify risk factors, and produce test scenarios specific to that network's configuration.
**Metric:** Engineering hours per migration. Target: 40% reduction in assessment and planning phase.
**Risk:** Higher. Must include mandatory human review of every migration plan. AI accelerates preparation, not execution.

**So what?** Start with Tier 1. It is lowest risk, requires no code changes, and immediately reveals the gap between "tests we have" and "safety we need."

**What do we do Monday?** Pull the last 12 months of production incidents for one product line. List the top 10. For each: does an existing test cover this failure mode? The answer builds the business case.

---

## 6. Measuring Real Value (ERGOL vs LOLLI)

AI teams naturally optimize for output volume. This is the single biggest risk of AI adoption — not that AI produces bad code, but that it produces enormous quantities of code that nobody needed.

### The ERGOL/LOLLI Framework

**ERGOL** (real fuel): Metrics that measure value delivered to users and the business.
**LOLLI** (inflated currency): Metrics that look impressive but correlate poorly with outcomes.

| LOLLI (Do Not Optimize For) | ERGOL (Optimize For) |
|---|---|
| Lines of code written | Call delivery success rate |
| PRs merged per week | Location accuracy improvement |
| Test count | Production incidents prevented |
| Story points completed | Mean time to dispatch (reduction) |
| Features shipped | PSAP operator satisfaction score |
| AI-generated suggestions accepted | Compliance gap closure rate |

In experimental use with AI agent teams, a single session produced 80+ artifacts. Honest assessment: only 15% were validated by a real user. The 85% looked productive. They were not. They were LOLLI.

### The Anti-LOLLI Checklist

Before any AI-generated artifact enters a pipeline:

1. **Who will use this today?** Not "eventually" — today.
2. **Can we validate it right now?** Run it, test it, show it to a user.
3. **Does something similar already exist?** Extend, don't duplicate.
4. **What is the ERGOL metric?** How will we know it delivered value?
5. **Would deleting this hurt anyone?** If no, it is LOLLI.

**For Intrado:** The ERGOL metrics are built into our domain. Call delivery success rate, location accuracy, failover time, mean time to dispatch — these are not abstract. They are measured. They are audited. They are regulated. AI adoption should move these numbers. If AI adoption moves "velocity" but not these numbers, it is LOLLI.

**So what?** Measure what matters. AI will produce more output. More output is not more value unless it moves the metrics that our customers (PSAPs) and regulators (FCC, NENA) actually care about.

**What do we do Monday?** Define three ERGOL metrics for the first product line where AI is adopted. Post them on the team dashboard. Review them weekly. If they are not moving after 90 days, the AI adoption is not working — regardless of how productive it feels.

---

## 7. The Factory-of-Factories Pattern

The highest-leverage use of AI is not building things. It is building systems that build things.

### Example: Test Generation

**Level 0 (manual):** Engineer writes tests by hand.
**Level 1 (AI-assisted):** AI generates tests from prompts.
**Level 2 (AI-native):** AI generates tests from production incident patterns automatically.
**Level 3 (factory-of-factories):** AI builds the test-generation pipeline that learns from new incidents and continuously produces better tests without human prompts.

Each level multiplies output, but also multiplies risk if ungoverned. A test factory that optimizes for count produces thousands of passing tests that cover nothing. A governed test factory that optimizes for failure-mode coverage produces fewer tests that catch real problems.

### Applying This to Intrado

| System | Factory-of-Factories Approach |
|---|---|
| Compliance | Build a pipeline that reads regulatory changes and generates compliance test cases, not individual compliance checks |
| Migration | Build a migration analysis framework that learns from completed migrations, not individual migration plans |
| Monitoring | Build an alert correlation system that improves its models from each incident, not individual alert rules |

**So what?** The compounding returns come from building the system, not the output. One good pipeline running for a year outproduces a hundred one-off AI tasks.

**What do we do Monday?** Identify one repetitive engineering task (likely compliance checking or migration assessment). Instead of using AI to do it once, invest in building the pipeline that does it continuously. Measure the compounding: does the second run produce better results than the first?

---

## 8. Risk Management

AI in life-safety software introduces specific risks that AI in e-commerce does not. Here is an honest accounting.

### Risk #1: Confident Wrong Answers

AI models present incorrect information with the same confidence as correct information. In a codebase where a subtle routing bug can send first responders to the wrong address, this is not an academic concern.

**Mitigation:** Multi-model verification for any change touching routing logic. If two independent models disagree on the correctness of a change, it goes to human review. Period.

### Risk #2: Test Coverage Illusion

AI can generate thousands of tests that all pass. This creates a false sense of safety. The tests may be testing the implementation rather than the requirements — they verify that the code does what the code does, not that the code does what it should.

**Mitigation:** Measure test coverage against production incidents, not against lines of code. A test suite that would have caught 90% of last year's production failures is safer than a test suite with 95% line coverage that would have caught 30%.

### Risk #3: Over-Automation of Critical Paths

The natural tendency is to automate the most valuable paths first. In life-safety, the most valuable paths are also the most dangerous to automate.

**Mitigation:** Start with low-criticality, high-volume workflows (text-to-911 processing, log analysis, documentation). Build trust and governance muscle before touching call routing or location services.

### Risk #4: Regulatory Uncertainty

FCC and NENA have not issued comprehensive guidance on AI in 911 systems. Operating ahead of regulation creates compliance risk.

**Mitigation:** Maintain audit trails for every AI-influenced decision in production systems. When regulations arrive, we need to demonstrate what AI did, why, and how humans were in the loop. Governance-first approach means this audit trail exists from day one.

### Risk #5: Organizational Resistance

Engineers who have built life-safety systems for decades will reasonably question whether AI belongs in their workflows. Dismissing this concern as resistance to change is a mistake — these engineers understand failure modes that AI does not.

**Mitigation:** AI augments domain expertise, it does not replace it. The engineer who has seen a specific PSAP failover scenario is more valuable with AI tools than AI tools are without that engineer. Adoption starts with willing teams and spreads by demonstrated results, not mandates.

---

## 9. Three-Year Roadmap

### Year 1: Foundation (Months 1-12)

- **Q1:** Audit one product line's delivery pipeline. Map bottlenecks. Define ERGOL metrics. Classify codebase into criticality tiers.
- **Q2:** Deploy AI-assisted test analysis for that product line (Tier 1). Measure gap between existing tests and actual failure modes.
- **Q3:** Pilot compliance automation with dual-model verification (Tier 2). Measure time from regulation change to verified compliance.
- **Q4:** Evaluate results. Kill what is not working. Double down on what is. Publish internal findings.

**Success criteria:** At least one ERGOL metric measurably improved. Kill criteria: no ERGOL improvement after two quarters despite investment.

### Year 2: Scale (Months 13-24)

- Expand to additional product lines based on Year 1 learnings
- Deploy incident response acceleration (Tier 3)
- Begin NG911 migration tooling pilot (Tier 4)
- Build first factory-of-factories pipeline (likely compliance or migration)
- Establish governance framework across engineering

### Year 3: AI-Native (Months 25-36)

- AI participation standard across engineering workflows
- Factory-of-factories pipelines running continuously for compliance, testing, monitoring
- Multi-model orchestration mature for architecture review and code analysis
- Governance framework refined through 24+ months of operational data
- Measurable improvement in core ERGOL metrics: call delivery, location accuracy, compliance response time

---

## 10. The Ask

### Budget

Year 1 pilot for one product line:

| Item | Estimated Cost |
|---|---|
| AI model API access (Claude, GPT, Gemini) | $50-100K/year |
| Engineering time (2 engineers, 50% allocation) | Existing headcount |
| Infrastructure (compute, storage for AI pipelines) | $20-40K/year |
| Training and enablement | $10-20K |
| **Total Year 1** | **$80-160K** |

This is conservative. Industry benchmarks show average ROI of 171% within 12-18 months for enterprise AI orchestration implementations.

### What Success Looks Like

After 12 months, we can answer these questions with data:

1. Did AI-assisted test analysis find gaps that manual review missed?
2. Did compliance automation reduce time to verified compliance?
3. Did any ERGOL metric (call delivery, location accuracy, failover time) improve?
4. Did engineering teams adopt the tools voluntarily after the pilot?

If yes to three or more: expand. If yes to fewer than two: stop and reassess.

### What Failure Looks Like

- AI generates more tests but production incident rate unchanged
- Velocity metrics improve but PSAP customer satisfaction unchanged
- Engineers use AI for code completion but skip governance workflows
- Lots of impressive demos, no measurable improvement in the numbers that regulators and customers track

If this describes the state after 12 months, the program was LOLLI. Shut it down, learn from it, try a different approach.

---

## Summary

| Question | Answer |
|---|---|
| What is AI-native engineering? | AI as a governed team member, not just a code-completion tool |
| Why does Intrado need it? | NG911 complexity is scaling faster than our team can scale |
| What does it cost? | $80-160K for a one-product-line pilot in Year 1 |
| What is the risk? | Confident wrong answers, test illusion, over-automation of critical paths |
| How do we manage the risk? | Constitutional governance, multi-model verification, criticality tiers, ERGOL metrics |
| What do we do Monday? | Audit one product line. Map the pipeline. Define ERGOL metrics. Start with test intelligence. |

---

*This thesis is based on experimental findings from AI-native development across a multi-repo governance ecosystem, industry research on AI in emergency services, and Intrado's published NG911 capabilities. Every recommendation is designed to be falsifiable — if the metrics don't move, the approach is wrong.*

### Sources

- [Intrado NG911 + AI-Based Text Translation — Columbus, OH](https://www.intrado.com/news-releases/city-of-columbus-ng911-upgrades)
- [Intrado State of the 9-1-1 Industry Report](https://www.intrado.com/news-releases/intrados-landmark-state-of-the-9-1-1-industry-report-charts-future-of-emergency-response)
- [AI-Powered 911 Call Processing — Police1](https://www.police1.com/911-and-dispatch/smarter-faster-safer-how-ai-is-reinventing-the-emergency-call)
- [911 AI for Non-Emergency Call Filtering — Route Fifty](https://www.route-fifty.com/artificial-intelligence/2025/07/911-looks-ai-filter-out-non-emergency-calls/406552/)
- [AI & ML in Emergency Dispatch Systems — EMS Ricky](https://emsricky.com/ai-in-emergency-dispatch-systems/)
- [2026: The Year Software Engineering Becomes AI-Native — Xebia](https://xebia.com/news/2026-the-year-software-engineering-will-become-ai-native/)
- [Multi-Agent AI Orchestration: Enterprise Strategy 2025-2026](https://www.onabout.ai/p/mastering-multi-agent-orchestration-architectures-patterns-roi-benchmarks-for-2025-2026)
- [Gartner: 40% of Enterprise Apps to Feature AI Agents by 2026](https://www.gartner.com/en/newsroom/press-releases/2025-08-26-gartner-predicts-40-percent-of-enterprise-apps-will-feature-task-specific-ai-agents-by-2026-up-from-less-than-5-percent-in-2025)
- [NG911 and Real-Time Data Integration](https://nga911.com/blogs/post/future-emergency-communication-how-ng911-integrates-ai-and-real-time-data)
- [Smart Devices Transforming 911 — EMS1](https://www.ems1.com/technology/as-smart-devices-change-emergency-calls-911-centers-must-adapt)
