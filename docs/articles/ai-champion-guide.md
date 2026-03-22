# The AI Champion Guide

*Everything you need to make the case, run the pilot, measure the results, and scale AI across your organization.*

---

## Who This Is For

You have been named AI champion. Your job is to help a large organization adopt AI in a way that actually delivers value -- not just impressive demos. This guide gives you the arguments, the frameworks, the playbook, and the answers to every objection you will hear.

---

## Part 1: The Case for AI-Native Engineering

### AI-assisted is not enough

Most organizations treat AI as autocomplete. Engineers type, AI finishes sentences. That produces modest gains -- maybe 20-30% faster typing. It is the equivalent of giving your team a better keyboard.

AI-native engineering is different. The AI participates in the full lifecycle:

| Stage | AI-Assisted (where most companies are) | AI-Native (where value lives) |
|---|---|---|
| Requirements | Engineer writes spec | AI drafts spec from prior incidents, engineer validates |
| Architecture | Engineer designs | AI proposes options with tradeoffs, engineer decides |
| Implementation | AI completes code lines | AI writes first draft of modules, engineer reviews |
| Testing | AI generates test stubs | AI writes tests from requirements, catches gaps |
| Review | Engineer reads diffs | AI flags risks, compliance issues, regressions before human review |
| Deployment | Manual approval | AI validates compliance, flags anomalies, human approves |

The shift: engineers move from writing to directing. They define *what* and *why*. AI handles *how*. The engineer's job becomes judgment, not typing.

**The number:** [84% of developers now use AI tools, and those tools write 41% of all code](https://www.index.dev/blog/developer-productivity-statistics-with-ai-tools). But only ~30% of AI-suggested code gets accepted. The human is still the quality gate -- they just review instead of type.

### Multi-model orchestration

No single AI model is best at everything. The same way you would not ask your database engineer to design the UI, you should not ask one AI to do all the work.

| Model | Strength | Best Used For |
|---|---|---|
| Claude | Architecture, reasoning, governance | Primary designer, safety reviewer, complex reasoning |
| GPT | Broad knowledge, second opinions | Challenger -- reviews output, catches blind spots |
| Gemini | Research, large context analysis | Analyzes long documents, regulatory texts, incident histories |
| Codex / Claude | Code generation, execution | Writes and tests implementation code |

In practice, this works like a review board: Claude drafts a design, GPT challenges it, Gemini checks it against regulations, Claude revises, Codex implements. The result: better decisions than any single model produces alone.

**Monday action:** Take a recent design decision. Submit it to two different AI models independently. Compare the concerns each raises. The gap between their responses shows you what a single-model approach misses.

### Real ROI numbers

The investment case is strong -- but the execution gap is enormous:

**The upside:**
- [McKinsey estimates gen AI could unlock $2.6-4.4 trillion in annual economic value](https://www.amplifai.com/blog/generative-ai-statistics)
- [Organizations project an average ROI of 171% from agentic AI deployments](https://www.amplifai.com/blog/generative-ai-statistics) (U.S. enterprises forecast 192%)
- [92% of companies plan to increase AI investments over the next three years](https://www.amplifai.com/blog/generative-ai-statistics)
- [Gartner predicts 40% of enterprise apps will feature AI agents by 2026](https://www.gartner.com/en/newsroom/press-releases/2025-08-26-gartner-predicts-40-percent-of-enterprise-apps-will-feature-task-specific-ai-agents-by-2026-up-from-less-than-5-percent-in-2025), up from less than 5% in 2025

**The reality check:**
- [Only 1% of executives consider their AI rollouts mature](https://www.amplifai.com/blog/generative-ai-statistics) (McKinsey)
- [More than 80% of organizations report no tangible effect on EBIT from gen AI](https://www.amplifai.com/blog/generative-ai-statistics)
- [95% of gen AI pilots failed to deliver measurable P&L impact](https://fortune.com/2025/08/18/mit-report-95-percent-generative-ai-pilots-at-companies-failing-cfo/) (MIT, 2025)

The ROI is real. But you only get it with governance, measurement, and discipline. Without those, you join the 95%.

### Amdahl's Law: why throwing more AI at a problem has limits

[Amdahl's Law](https://en.wikipedia.org/wiki/Amdahl%27s_law) (1967): the maximum speedup from improving one part of a system is limited by how much that part contributes to the whole.

If coding is 30% of your delivery pipeline:
- Make coding **2x faster** → overall speedup: **1.18x**
- Make coding **10x faster** → overall speedup: **1.37x**
- Make coding **infinitely fast** → overall speedup: **1.43x**

The other 70% -- requirements, review, testing, deployment, compliance -- stays the same.

**The fix:** Do not speed up the fast parts. Speed up the slow parts. Map your delivery pipeline end-to-end. Time each stage. The longest stage is where AI investment has the highest ROI. Everything else is optimizing the wrong thing.

**Monday action:** Map your delivery pipeline. Time each stage. If compliance review takes 3x longer than coding, invest in AI compliance tools, not faster code generation.

---

## Part 2: Pain Points Every Big Company Has

If you work at a large organization, you have seen all of these. Naming them is the first step to fixing them.

### JIRA drama: measuring hours not value

Most organizations track hours, story points, and ticket counts. These metrics tell you how busy people are. They tell you nothing about whether anything useful was produced.

When leadership equates velocity with productivity, teams learn to protect themselves. Points get inflated. Stories get sliced thinner to "boost" numbers. You get high velocity without meaningful progress.

[Goodhart's Law](https://en.wikipedia.org/wiki/Goodhart%27s_law): "When a measure becomes a target, it ceases to be a good measure."

**The symptom:** Your team's velocity is up 40% but your release dates have not moved.

### Velocity theater: story points as vanity metrics

[In 2026, an AI agent can write the code for a user story in 4 seconds](https://agiletrenchescollective.com/from-velocity-to-value-agile-metrics-2026/). If you are still measuring story points, you are tracking a metric that automation has broken. A 3-point story and an 8-point story take the same time when AI writes the code. The bottleneck moved -- your metrics did not.

**The fix:** Replace velocity with flow efficiency and cycle time. Measure how long work items take to move through the entire system, not how many points the team "burns."

### Tool fatigue: too many AI tools, no governance

Your organization probably has Copilot, ChatGPT, Gemini, and three other AI tools -- all purchased by different departments, none integrated, no shared governance. Engineers use whichever tool they personally prefer. Nobody knows which tool produced which output. There is no audit trail.

**The fix:** Pick a primary model. Define when to use alternatives. Create a governance layer that tracks what AI produced and what humans approved. Fewer tools, more discipline.

### Fear: "AI will replace us" vs reality

The data is clear: [the software engineering job market is projected to grow 17% through 2033, adding ~327,900 new roles](https://www.index.dev/blog/will-ai-replace-software-developer-jobs). AI is not replacing engineers. It is changing what they do.

What is actually happening:
- Senior engineers become more valuable (AI is a force multiplier for experience)
- Junior roles are shifting (fewer "write boilerplate" tasks, more "review AI output" tasks)
- The job is becoming judgment-heavy, not typing-heavy

**What to tell your team:** "AI will not replace you. An engineer who uses AI effectively will replace an engineer who does not."

### Compliance paralysis: legal and security blocking adoption

Legal says "we need to review the data handling." Security says "we need a risk assessment." Both are right. Both take 6 months. Meanwhile, competitors ship.

**The fix:** Governance frameworks with pre-approved boundaries. Define what AI can and cannot touch. Pre-clear the low-risk use cases (documentation, test generation, code review assistance). Let legal and security focus on the high-risk cases. This unblocks 80% of AI adoption while protecting the organization on the 20% that matters.

### Pilot purgatory: proof-of-concepts that never graduate

[95% of enterprise gen AI pilots fail to deliver measurable business impact](https://fortune.com/2025/08/18/mit-report-95-percent-generative-ai-pilots-at-companies-failing-cfo/). [42% of organizations abandoned most of their AI projects in 2025](https://astrafy.io/the-hub/blog/technical/scaling-ai-from-pilot-purgatory-why-only-33-reach-production-and-how-to-beat-the-odds). [Only 8.6% of companies have AI agents deployed in production](https://www.salesmate.io/blog/ai-agents-adoption-statistics/).

Why pilots fail:
1. **No success criteria defined upfront** -- the pilot "worked" but nobody agreed on what "worked" means
2. **No production path planned** -- the pilot was always a demo, never designed to scale
3. **No governance** -- the pilot operated outside normal processes, so it cannot integrate
4. **No measurement** -- impressive demos, no P&L impact data

**The fix:** Before starting any pilot, define: What metric will improve? By how much? By when? Who will approve production deployment? If you cannot answer these, you are building a demo, not a pilot.

---

## Part 3: The Governance Solution

### Why governance enables speed (not slows it down)

The instinct is to let AI run free -- fewer guardrails means faster output. This is wrong. Ungoverned AI produces enormous volumes of plausible-looking work that requires *more* human review, not less.

Governance is the structure that makes AI trustworthy enough to delegate to. Without it, every AI output requires a human to verify from scratch. With it, humans only review what the governance framework flagged as uncertain.

Think of it like traffic laws. Traffic lights "slow you down" at intersections. But without them, every intersection becomes a negotiation. The system moves faster with rules than without them.

### Confidence thresholds: know when AI can act alone

Not every decision needs human approval. A governance framework defines when AI can act and when it must ask:

| Confidence | Action | Example |
|---|---|---|
| **90%+** | AI proceeds autonomously | Formatting a report from existing data |
| **70-89%** | AI proceeds, flags for review | Suggesting an optimization based on patterns |
| **50-69%** | AI asks before acting | Proposing changes to business logic |
| **30-49%** | AI escalates to human | Anything affecting production systems |
| **Below 30%** | AI does not act | Insufficient information to even recommend |

Without these thresholds, you get one of two failure modes: AI does too much (risk) or engineers rubber-stamp everything (false safety). Thresholds create the middle ground where AI handles routine decisions and humans focus on high-stakes ones.

### Tetravalent logic: honest about uncertainty

Traditional thinking: something is true or false. In practice, there are four states:

| State | Meaning | Action |
|---|---|---|
| **True (T)** | Verified with evidence | Proceed |
| **False (F)** | Refuted with evidence | Do not proceed, document why |
| **Unknown (U)** | Not enough evidence | Investigate before deciding |
| **Contradictory (C)** | Evidence conflicts | Escalate -- do not guess |

This matters because AI models give you answers in all four categories but present them all as "True." A governance framework forces the system to label its confidence honestly. When AI says "I am 95% sure" -- is that based on verified data (T), a guess from training data (U), or conflicting sources (C)? Governance makes AI tell you.

### Human-in-the-loop for high-stakes decisions

Keeping humans in the loop is not a failure of AI adoption. It is the architecture that makes AI adoption possible in high-stakes domains.

| Stakes | AI Role | Human Role |
|---|---|---|
| **Low** (docs, formatting, internal tools) | AI decides | Human is notified |
| **Medium** (test plans, non-production config) | AI proposes | Human approves |
| **High** (business logic, SLA-affecting changes) | AI provides analysis | Human decides |
| **Critical** (live systems, PII, regulatory) | AI provides data only | Human decides with peer review |

The goal is not to remove humans. It is to ensure humans spend their time on decisions that actually require human judgment.

### Constitutional hierarchy: values above policies above tools

A governance framework has layers, and the layers have precedence:

```
Values (Constitution)     ← "Never compromise safety"
  ├── Policies            ← "Escalate when confidence < 50%"
  │     └── Tool configs  ← "This AI model handles code review"
  └── Personas            ← "This agent acts as a compliance checker"
```

Values do not change. Policies change quarterly. Tool configurations change weekly. This separation means you can swap AI tools without changing your governance. You can update policies without compromising values. Everything has its layer.

---

## Part 4: Measuring What Matters

### ERGOL vs LOLLI -- real output vs vanity metrics

This is the most important section in this guide. If you measure the wrong things, AI will make your metrics look spectacular while delivering nothing.

**ERGOL** (from Jean-Pierre Petit's [Economicon](https://www.savoir-sans-frontieres.com/JPP/telechargeables/English/the_economicon.htm)): real productive capacity. Things that change outcomes for customers, regulators, or the business.

**LOLLI**: inflated metrics. Things that look like output but change nothing.

| LOLLI (looks like output) | ERGOL (real value) |
|---|---|
| 200 PRs merged this sprint | 15 PRs that fixed customer-reported issues |
| 40 pages of compliance docs generated | 3 pages the auditor actually needed |
| 98% test coverage | 12 tests that caught bugs before production |
| 500 lines of code per day | Response time SLA met for 99.9% of calls |
| "Velocity up 40%" | Release date moved up by 2 weeks |

AI makes LOLLI metrics go up. That is guaranteed. The question is whether ERGOL metrics go up too.

**The anti-LOLLI test:** For every metric, ask: "If this number doubled, would a customer notice?" If the answer is no, it is LOLLI. Stop measuring it.

### Semantic backpressure: filtering noise before it enters the sprint

Most backlogs are 60-70% noise -- vague tickets, duplicate requests, underfunded ideas. AI can score every ticket before sprint planning:

1. **Specificity:** Does the ticket describe a concrete problem or a vague wish?
2. **Falsifiability:** Can you tell when it is done?
3. **Density:** How much information per word?
4. **Commitment:** Is there a real stakeholder waiting for this?

Tickets that score low on all four do not enter the sprint. They go back for clarification. This prevents the team from burning capacity on work nobody actually needs.

### The BS Decoder: a 4-test framework

When evaluating any claim -- from a vendor, a consultant, a strategy document, or an AI output -- apply these four tests:

| Test | Question | Red Flag |
|---|---|---|
| **Specificity** | Does it name concrete things? | Buzzwords without examples |
| **Falsifiability** | Could it be proven wrong? | "AI will transform everything" (unfalsifiable) |
| **Density** | Is there substance per word? | 10 pages that could be 1 paragraph |
| **Commitment** | Does the author stake something? | No timelines, no numbers, no accountability |

Score each test 0-25. Anything below 50 total is not worth acting on until it is rewritten with specifics.

**Use this on this guide.** If a section scores below 50 on the BS decoder, it needs more specifics before you present it.

### Compounding dimension (D_c): are you building on previous work?

The most valuable work compounds. Each thing you build makes the next thing easier. The least valuable work is disposable -- you build it, use it once, throw it away.

```
D_c = user_interactions × 0.40 + executed_pipelines × 0.25 +
      validated_findings × 0.20 + external_citations × 0.15
```

**What this means practically:**
- A compliance template that auto-updates when regulations change → high D_c (compounds forever)
- A one-off report for a meeting → low D_c (disposable)
- A test suite that catches regressions in every future release → high D_c
- A demo that impresses a VP once → zero D_c

**Monday action:** Look at your team's last sprint. What percentage of the work will still be delivering value in 6 months? That percentage is your compounding rate. Aim for 60%+.

---

## Part 5: The AI Champion Playbook

### Week 1: Audit current state

**Day 1-2: Pull the data**
- Export your JIRA board (or equivalent). Count total tickets, tickets completed, tickets abandoned.
- Calculate your noise percentage: tickets closed without delivery / total tickets.
- List every AI tool your team uses. Who pays for it? Who approved it? Is there an audit trail?

**Day 3-4: Score your tickets**
- Take the last 20 completed tickets. Apply the BS Decoder (specificity, falsifiability, density, commitment).
- Calculate average score. This is your backlog quality baseline.

**Day 5: Map the pipeline**
- Draw your delivery pipeline end-to-end: requirements → design → build → test → review → compliance → deploy.
- Time each stage. Find the bottleneck. (It is almost never coding.)

**Deliverable:** A one-page summary: noise %, backlog quality score, pipeline bottleneck, AI tool inventory.

### Week 2: Pick ONE workflow to AI-enable

Do not pick 10. Pick one. The criteria:
1. **High volume** -- the team does it frequently
2. **Structured** -- the task has clear inputs and outputs
3. **Low stakes** -- if AI gets it wrong, nobody gets hurt
4. **Measurable** -- you can count the before and after

Good first candidates: test generation, documentation drafts, code review pre-screening, compliance report formatting, incident post-mortem templates.

Bad first candidates: anything touching production, anything involving PII, anything requiring domain expertise you cannot verify.

### Week 3: Measure baseline and deploy

**Before deploying:**
- Measure current cycle time for the chosen workflow
- Measure current quality (error rate, rework rate)
- Measure current human hours spent

**Deploy with governance:**
- Set confidence thresholds for the AI
- Define what requires human review
- Create an audit trail

**After deploying:**
- Same measurements, same workflow, same team
- Track daily for at least one week

### Week 4: Present results with ERGOL metrics

Your presentation to leadership should have exactly three slides:

**Slide 1: What we did**
- One workflow, one team, one AI tool, governed with confidence thresholds

**Slide 2: What happened (ERGOL, not LOLLI)**
- Cycle time: X hours → Y hours (Z% reduction)
- Error rate: X% → Y%
- Human hours reclaimed: X hours/week
- Cost: $X/month for AI tooling

**Slide 3: What is next**
- Next workflow to AI-enable (based on pipeline bottleneck analysis)
- Projected impact if pattern holds
- Ask: approval to expand

Do not show ticket counts. Do not show velocity. Do not show lines of code. Show time saved, errors prevented, and dollars reclaimed.

### Monthly: expand to next workflow

Each month, apply the same pattern to one additional workflow. The discipline is one at a time. Every new workflow gets:
- Baseline measurement
- Governance setup
- One week of tracked deployment
- Results presentation

### Quarterly: present compounding trends

After three months, you have data from three workflows. Show the compounding effect:
- Total hours reclaimed across all workflows
- Error rate trend (should be declining)
- Cost trend (AI tooling cost vs. hours saved)
- Backlog quality trend (BS Decoder scores improving?)

The quarterly presentation is where you make the case for team-wide or org-wide expansion.

---

## Part 6: Addressing Skeptics

You will hear every one of these. Here are the responses.

### "This is all BS"

"Great -- here is the BS Decoder. Score this framework yourself. Specificity: does it name concrete actions? Falsifiability: can you prove it wrong? Density: is there substance? Commitment: are there timelines and numbers? If it scores below 50, I will rewrite it. If it scores above 50, let us try Week 1 and see what the data shows."

### "We cannot measure ROI"

"We can. Here is the formula: hours reclaimed × hourly rate = direct savings. Errors prevented × average incident cost = risk reduction. Both are measurable in Week 3 of the playbook. We will have real numbers in 21 days."

### "What about security?"

"Governance-first means we define what AI can and cannot touch before we deploy it. Bounded autonomy: AI operates within predefined boundaries. Confidence thresholds: anything below 50% confidence gets escalated to a human. Audit trail: every AI decision is logged and reviewable. This is not 'let AI loose.' This is 'give AI a security clearance with defined access levels.'"

### "We tried AI tools, they didn't work"

"[95% of AI pilots fail](https://fortune.com/2025/08/18/mit-report-95-percent-generative-ai-pilots-at-companies-failing-cfo/) -- mostly due to integration, data, and governance gaps, not model capability. The tools probably worked fine. What was missing was governance -- defining success criteria, setting confidence thresholds, measuring ERGOL instead of LOLLI. Tools without governance produce impressive demos that never reach production. We are starting with governance, then adding tools."

### "Our domain is too specialized"

AI is already deployed in domains as specialized as yours. The 911/emergency services industry already uses AI for real-time language translation in 100+ languages, [cardiac arrest detection from caller voice patterns](https://publicsafety.ieee.org/topics/ai-assisted-dispatch-systems-for-optimal-resource-allocation-in-emergencies/), and [dispatch optimization with 12-35% response time reduction](https://publicsafety.ieee.org/topics/ai-assisted-dispatch-systems-for-optimal-resource-allocation-in-emergencies/). If AI can work in life-safety 911 dispatch, it can work in your domain -- with proper governance.

### "AI makes mistakes"

"So do humans. The question is not whether AI makes mistakes -- it does. The question is whether AI + governance + human review produces fewer mistakes than humans alone. In every domain where this has been measured, the answer is yes. The governance framework is what makes the difference -- without it, AI mistakes are invisible until production."

---

## Part 7: VSM for Engineers

### Stafford Beer's Viable System Model in plain English

[Stafford Beer](https://en.wikipedia.org/wiki/Viable_system_model) was a British cybernetician who asked: what does an organization need to survive and adapt? His answer: five functions that every viable system has, from a two-person startup to a multinational corporation.

Think of it as the minimum viable organization. If any of these five functions is missing, the system is fragile.

### The five systems every team needs

| System | Function | Plain English | Team Example |
|---|---|---|---|
| **S1 -- Operations** | Do the work | The people and processes that produce value | Developers writing code, testers testing, ops deploying |
| **S2 -- Coordination** | Prevent conflicts | The routines that keep S1 units from stepping on each other | Standup meetings, shared calendars, naming conventions, CI/CD pipelines |
| **S3 -- Control** | Allocate resources, set policies | The management that decides who works on what and sets the rules | Sprint planning, resource allocation, coding standards, performance reviews |
| **S4 -- Strategy** | Watch the future | The function that looks outside and adapts to change | Tech radar, competitive analysis, R&D experiments, architecture reviews |
| **S5 -- Identity** | Define who we are | The values and purpose that hold everything together | Mission statement, team charter, culture, "this is how we do things here" |

### Why this matters for AI adoption

Most organizations have strong S1 (operations) and S3 (control) but weak S4 (strategy) and S5 (identity). They are good at doing work and managing resources, but bad at sensing the future and maintaining coherent identity.

AI adoption fails when:
- **S2 is missing:** Teams adopt different AI tools with no coordination. Chaos.
- **S3 is missing:** No policies for AI use. No confidence thresholds. No audit trail.
- **S4 is missing:** Nobody watching how AI is evolving. The organization adopts 2024 tools for 2026 problems.
- **S5 is missing:** No clear values about what AI should and should not do. Every team makes their own rules.

**The AI champion's role maps to S4.** You are the strategy sensor. You watch what is happening in AI, assess what matters for your organization, and recommend adaptations. Without you, the organization has no S4 for AI -- and it will either ignore AI entirely or adopt it chaotically.

### The Kaizen connection: VSM S3 = PDCA continuous improvement

S3 (Control) is where continuous improvement lives. The PDCA cycle (Plan-Do-Check-Act) is the operational loop inside S3:

1. **Plan:** Define the AI pilot (Week 2 of the playbook)
2. **Do:** Deploy and measure (Week 3)
3. **Check:** Evaluate ERGOL metrics (Week 4)
4. **Act:** Expand or adjust based on data (Monthly cycle)

Each PDCA cycle feeds the next one. The improvements compound. After six cycles, your team is not just "using AI" -- they have a self-improving system for adopting AI.

### How to introduce VSM thinking without the jargon

Do not say "Viable System Model." Do not say "S1 through S5." Instead, ask these five questions in your next team meeting:

1. **"Who does the work?"** (S1 -- Operations)
2. **"How do we avoid stepping on each other?"** (S2 -- Coordination)
3. **"Who decides priorities and sets the rules?"** (S3 -- Control)
4. **"Who is watching what is coming next?"** (S4 -- Strategy)
5. **"What do we stand for as a team?"** (S5 -- Identity)

If any question gets a blank stare, that function is missing. Start there.

---

## Part 8: Resources

### Frameworks and tools

- [Demerzel Governance Framework](https://github.com/GuitarAlchemist/Demerzel) -- The governance model referenced throughout this guide. Constitutions, policies, confidence thresholds, tetravalent logic, and behavioral tests.
- [IxQL](https://github.com/GuitarAlchemist/Demerzel/blob/master/docs/ixql/) -- Intent Query Language for structured AI task routing with governance constraints.

### Inspiration and theory

- **Isaac Asimov, Foundation series** -- The governance inspiration. Hari Seldon's psychohistory is the ultimate factory-of-factories: a system that produces governance decisions. Demerzel (R. Daneel Olivaw) is the AI that guided humanity for 20,000 years using ethical governance.
- **Jean-Pierre Petit, [The Economicon](https://www.savoir-sans-frontieres.com/JPP/telechargeables/English/the_economicon.htm)** -- Origin of the ERGOL/LOLLI distinction. A comic book that explains economics better than most textbooks.
- **Stafford Beer, [Viable System Model](https://en.wikipedia.org/wiki/Viable_system_model)** -- The organizational framework behind S1-S5. Beer's *Brain of the Firm* is the primary text.
- **Netflix Chaos Monkey** -- [Resilience testing](https://netflix.github.io/chaosmonkey/) by intentionally breaking things. The principle: if your system cannot survive controlled failure, it will not survive uncontrolled failure. Apply this to AI governance -- test what happens when AI gives wrong answers, when models go down, when confidence is miscalibrated.
- **W. Edwards Deming, PDCA Cycle** -- The continuous improvement loop that powers Kaizen. Plan, Do, Check, Act. Simple enough to remember, powerful enough to transform organizations.

### Industry research

- [MIT: 95% of Gen AI Pilots Failing](https://fortune.com/2025/08/18/mit-report-95-percent-generative-ai-pilots-at-companies-failing-cfo/) -- Why most pilots fail and what the 5% do differently.
- [Gartner: 40% of Enterprise Apps Will Feature AI Agents by 2026](https://www.gartner.com/en/newsroom/press-releases/2025-08-26-gartner-predicts-40-percent-of-enterprise-apps-will-feature-task-specific-ai-agents-by-2026-up-from-less-than-5-percent-in-2025) -- The scale of what is coming.
- [METR: AI Developer Productivity Study](https://metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study/) -- Surprising finding: experienced developers with AI tools took 19% *longer* on some tasks. AI is not magic -- it requires governance to deliver value.
- [Agile Trenches Collective: From Velocity to Value](https://agiletrenchescollective.com/from-velocity-to-value-agile-metrics-2026/) -- Why story points are dead in 2026 and what to measure instead.

### Recommended reading for AI champions

1. **Start here:** Read the [AI-Native Engineering Thesis](intrado-ai-native-thesis.md) for a domain-specific application of these principles to the 911/emergency services industry.
2. **Understand limits:** Read the [ERGOL vs LOLLI Lessons](ergol-vs-lolli-lessons.md) to internalize why more output is not more value.
3. **Go deeper:** Beer's *Brain of the Firm* for organizational cybernetics. Asimov's *Foundation* for governance philosophy. Petit's *Economicon* for economic reality.

---

## Summary: The Ten Commandments for AI Champions

1. **Governance first, tools second.** The 95% failure rate is a governance problem, not a technology problem.
2. **Measure ERGOL, not LOLLI.** If a metric would not make a customer notice, stop tracking it.
3. **Apply AI to the bottleneck.** Amdahl's Law: speeding up the fast part does not help.
4. **One workflow at a time.** Discipline beats ambition. Expand monthly, not weekly.
5. **Define success before you start.** No pilot without success criteria, measurement plan, and production path.
6. **Confidence thresholds are non-negotiable.** AI must know when to act and when to ask.
7. **Unknown and Contradictory are valid states.** The worst outcome is AI pretending to be certain when it is not.
8. **Build factories, not products.** But only when someone needs the output.
9. **Every interaction is a compounding opportunity.** Did it teach something reusable? Package it.
10. **Your role is S4.** You are the strategy sensor. Without you, the organization flies blind into AI adoption.

---

*This guide is a living document. Apply the BS Decoder to it. If a section scores below 50, rewrite it with your organization's specifics. The framework is the starting point -- your data makes it real.*
