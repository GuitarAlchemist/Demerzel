# AI-Native Software Engineering at Intrado

*A thesis for engineering leadership on how AI changes what we build, how we build it, and how we measure success*

---

## The One-Sentence Version

AI is not a tool your engineers use -- it is a team member that requires governance, measurement, and clear boundaries to deliver real value instead of impressive-looking activity.

---

## 1. What AI-Native Engineering Actually Looks Like

Most organizations treat AI as autocomplete. Engineers type code, AI finishes sentences. That is AI-assisted engineering. It produces modest gains -- maybe 20-30% faster typing.

AI-native engineering is different. The AI participates in the full lifecycle:

| Stage | AI-Assisted | AI-Native |
|---|---|---|
| Requirements | Engineer writes spec | AI drafts spec from prior incidents, engineer validates |
| Architecture | Engineer designs | AI proposes options with tradeoffs, engineer decides |
| Implementation | AI completes code lines | AI writes first draft of entire modules, engineer reviews |
| Testing | AI generates test stubs | AI writes tests from requirements, catches gaps engineer missed |
| Review | Engineer reads diffs | AI flags risks, compliance issues, regressions before human review |
| Deployment | Manual approval | AI validates compliance, flags anomalies, human approves |

The shift: engineers move from writing to directing. They define what needs to happen and why. AI handles how. The engineer job becomes judgment, not typing.

**What this means for Intrado:** Our engineers spend significant time on compliance documentation, incident post-mortems, and protocol updates. These are structured, rule-bound tasks where AI performs well. Freeing engineers from documentation lets them focus on the hard problems -- system reliability, edge cases in call routing, integration testing across jurisdictions.

**Monday action:** Pick one team. Have them track time spent on documentation vs. design decisions for two weeks. That ratio tells you how much AI can reclaim.

---

## 2. Multi-Model Orchestration -- Why One AI Is Not Enough

No single AI model is best at everything. The same way you would not ask your best database engineer to design the UI, you should not ask one AI to do all the work.

Here is how multiple models work together:

| Model | Strength | Role |
|---|---|---|
| Claude | Architecture, reasoning, governance | Primary: designs systems, reviews for safety, handles complex reasoning |
| GPT | Broad knowledge, second opinions | Challenger: reviews Claude output, catches blind spots |
| Gemini | Research, large context analysis | Researcher: analyzes long documents, regulatory texts, incident histories |
| Codex / Claude | Code generation, execution | Builder: writes and tests implementation code |

This is not theoretical. In practice, multi-model orchestration works like a review board:

1. **Claude** drafts an architecture for a new call-routing feature
2. **GPT** reviews the draft and raises concerns about edge cases
3. **Gemini** checks the draft against FCC regulations and state-specific 911 requirements
4. **Claude** revises based on feedback
5. **Codex** implements the approved design

The result: better decisions than any single model produces alone.

**What this means for Intrado:** Emergency services software has unusually high compliance requirements -- FCC mandates, state regulations, NENA standards, HIPAA for medical dispatch. A single AI model will miss regulatory nuances. Multiple models cross-checking each other is how you get coverage without hiring a larger compliance team.

**Monday action:** Run an experiment. Take a recent design decision and submit it to two different AI models independently. Compare the concerns each raises. The delta between their responses shows you what a single-model approach misses.

---

## 3. Governance Makes AI More Productive, Not Less

The instinct is to let AI run free -- fewer guardrails means faster output. This is wrong. Ungoverned AI produces enormous volumes of plausible-looking work that requires more human review, not less.

Governance is the structure that makes AI trustworthy enough to delegate to:

### Confidence Thresholds

Not every decision needs human approval. A governance framework defines when AI can act alone and when it must ask:

| Confidence Level | Action | Example |
|---|---|---|
| 90%+ | AI proceeds autonomously | Formatting a compliance report from existing data |
| 70-89% | AI proceeds, flags for review | Suggesting a call-routing optimization based on historical patterns |
| 50-69% | AI asks before acting | Proposing changes to dispatch priority algorithms |
| Below 50% | AI stops and escalates | Any change affecting live 911 call handling |

Without these thresholds, you get one of two failure modes: AI does too much (risk) or engineers approve everything without reading it (rubber-stamping). Both are dangerous. Thresholds create a middle ground where AI handles routine decisions and humans focus on high-stakes ones.

### Bounded Autonomy

AI operates within predefined boundaries. For Intrado, these boundaries are non-negotiable:

- **Never modify live call-routing rules** without human approval
- **Never alter dispatch priority logic** without a test cycle
- **Always flag** changes that affect response time SLAs
- **Always escalate** anything touching PII or call recordings

These are not restrictions that slow AI down. They are the reason you can trust AI to work unsupervised on everything else.

**What this means for Intrado:** In emergency services, the cost of an AI mistake is not a bad user experience -- it is a delayed ambulance. Governance is not overhead. It is the reason you can deploy AI in a life-safety domain at all.

**Monday action:** List your team top 10 recurring tasks. For each, assign a confidence threshold. Which ones could AI handle at 90%+ confidence today? Start there.

---

## 4. Concrete Intrado Applications

These are not hypothetical. Intrado is already deploying AI across its product lines. Here is where AI-native engineering amplifies what already exists:

### 4.1 Real-Time Language Translation

Intrado AI translation supports [100+ languages for 911 calls](https://www.intrado.com/blog/ai-powered-innovations-transforming-emergency-communications-centers). Columbus, Ohio recently upgraded to [NG911 with AI-powered text translation](https://www.intrado.com/news-releases/city-of-columbus-ng911-upgrades), serving 1 million+ residents. AI-native engineering extends this: instead of engineers hand-coding translation rules, AI models train on call transcripts to continuously improve accuracy for regional dialects and emergency-specific vocabulary.

### 4.2 Cardiac Arrest Detection

Intrado AI detects cardiac arrests from caller descriptions -- tone of voice, keywords, breathing patterns. Current industry data shows AI-powered dispatch systems achieve [12-35% reductions in response times](https://publicsafety.ieee.org/topics/ai-assisted-dispatch-systems-for-optimal-resource-allocation-in-emergencies/). Every second matters: brain damage begins at 4 minutes without oxygen. A 20% faster detection-to-dispatch time is not a metric -- it is survival.

### 4.3 Quality Assurance and Compliance

Real-time keyword detection and adherence analysis during calls. AI monitors whether dispatchers follow protocol, flags deviations instantly rather than discovering them in monthly reviews. This shifts QA from reactive (audit last month calls) to proactive (flag this call right now).

### 4.4 Dispatch Optimization

AI analyzes historical call data, current unit positions, traffic patterns, and incident severity to recommend optimal resource allocation. Industry projections show [AI-enabled dispatch growing at 19.2% CAGR through 2030](https://www.marlie.ai/blog/emergency-dispatch-software), with traditional CAD systems falling behind.

### 4.5 Compliance Automation

FCC regulations, NENA i3 standards, state-specific mandates, HIPAA requirements -- these change frequently and vary by jurisdiction. AI-native engineering means compliance checks are embedded in the development process, not bolted on after. Every code change is validated against current regulatory requirements before it reaches review.

**Monday action:** For each application above, identify who on the team owns it today. Ask them: "What takes you the longest each week?" That answer is your first AI deployment target.

---

## 5. Measuring What Matters: ERGOL vs LOLLI

This is the most important section. If you measure the wrong things, AI will make your metrics look spectacular while delivering nothing.

### The Problem

AI makes it trivially easy to produce output. Lines of code, documents, test cases, reports -- all can be generated in seconds. Traditional productivity metrics reward this:

| LOLLI (Looks Like Output) | ERGOL (Real Value) |
|---|---|
| 200 PRs merged this sprint | 15 PRs that fixed customer-reported issues |
| 40 pages of compliance docs generated | 3 pages the auditor actually needed |
| 98% test coverage | 12 tests that caught bugs before production |
| 500 lines of code per day per engineer | Response time SLA met for 99.9% of calls |

LOLLI metrics go up with AI. That is guaranteed. The question is whether ERGOL metrics -- the ones your customers and regulators care about -- go up too.

### The ERGOL Framework for Intrado

Measure these. Ignore the rest:

1. **Incidents caught before production** -- AI-assisted testing that prevents outages
2. **Response time SLA compliance** -- the metric that actually matters for 911
3. **Compliance audit findings reduced** -- fewer regulatory gaps found in reviews
4. **Engineer time reclaimed** -- hours shifted from documentation to design
5. **Customer-reported defects** -- are they going down, not just "tickets closed"

### How to Detect LOLLI Inflation

Warning signs that AI is generating activity without value:

- PR count is up but customer satisfaction is flat
- Test count is up but production incidents are unchanged
- Documentation volume is up but new engineers still take the same time to onboard
- "Velocity" is up but release dates have not moved

**Monday action:** Pull your team last sprint metrics. For each metric, ask: "If this number doubled, would a customer notice?" If the answer is no, it is LOLLI. Stop measuring it.

---

## 6. Factory-of-Factories: Build Systems, Not Things

The highest-leverage use of AI is not building things. It is building systems that build things.

### The Principle

| Approach | Example | Leverage |
|---|---|---|
| Manual | Engineer writes one compliance report | 1x -- one report |
| AI-Assisted | AI helps engineer write the report faster | 3x -- same report, less time |
| AI-Native | AI generates report from structured data | 10x -- any report, on demand |
| Factory-of-Factories | AI builds the report generator | 100x -- any report type, any jurisdiction, self-updating |

At Intrado, this means:

- Do not write compliance documentation -- build a system that generates compliant documentation from your codebase and regulatory database
- Do not write dispatch test scenarios -- build a system that generates test scenarios from historical incident data
- Do not write integration specs for each jurisdiction -- build a system that generates jurisdiction-specific configurations from a regulatory knowledge base

### The Discipline Required

Factory-of-factories has a trap: it is so easy to create that teams create systems nobody uses. The discipline is to build a factory only when you have a proven, repeated need. The rule: **no factory without a consumer.** If nobody is waiting for the output, do not build the machine.

**Monday action:** Identify the task your team does most repetitively. Not the hardest task -- the most repetitive one. That is your first factory candidate. Build the system that eliminates it, not a tool that makes it faster.

---

## 7. Amdahl's Law: Why More AI Does Not Always Help

This is the principle that prevents you from wasting money on AI that does not move the needle.

[Amdahl's Law](https://en.wikipedia.org/wiki/Amdahl%27s_law) (1967): **the maximum speedup from improving one part of a system is limited by how much that part contributes to the whole.**

If coding is 30% of your delivery pipeline:
- Make coding **2x faster** -> overall speedup: **1.18x**
- Make coding **10x faster** -> overall speedup: **1.37x**
- Make coding **infinitely fast** -> overall speedup: **1.43x**

The other 70% -- requirements, review, testing, deployment, compliance -- stays the same.

### Applying This to AI Teams

The same law applies to AI agent teams. Adding more AI agents to a project does not help if there is a sequential bottleneck:

```
Requirements (human, 2 days) -> Design (AI, 2 hours) -> Build (AI, 1 hour)
-> Review (human, 1 day) -> Compliance check (human, 3 days) -> Deploy (human, 1 day)
```

Total: ~7 days. AI handles ~3 hours of it. Making AI 100x faster saves you 2 hours and 57 minutes. The serial bottleneck -- human review and compliance -- dominates.

### The Fix

Do not speed up the fast parts. Speed up the slow parts:

1. **Requirements:** Use AI to draft requirements from prior incidents and stakeholder interviews. Human reviews and approves. Time: 2 days to 4 hours.
2. **Compliance:** Use AI to pre-check against regulatory databases. Human validates flagged items only. Time: 3 days to 4 hours.
3. **Review:** Use AI to pre-review for common issues. Human focuses on architecture and edge cases. Time: 1 day to 2 hours.

Now the pipeline is hours, not days. You did not make AI faster -- you applied AI to the bottleneck.

**What this means for Intrado:** Before investing in more AI coding tools, measure where time actually goes in your delivery pipeline. If compliance review takes 3x longer than coding, invest in AI compliance tools, not faster code generation.

**Monday action:** Map your delivery pipeline end-to-end. Time each stage. The longest stage is where AI investment has the highest ROI. Everything else is optimizing the wrong thing.

---

## 8. Risk Management: Uncertainty Is Not a Blocker

Engineering teams often stall because they are uncertain. AI makes this worse -- it can generate confident-sounding answers to questions nobody has verified. The solution is a structured approach to uncertainty.

### Tetravalent Logic: Four States, Not Two

Traditional thinking: something is true or false. In practice, especially in emergency services, there are four states:

| State | Meaning | Action |
|---|---|---|
| **True** | Verified with evidence | Proceed |
| **False** | Refuted with evidence | Do not proceed, document why |
| **Unknown** | Not enough evidence | Investigate before deciding |
| **Contradictory** | Evidence conflicts | Escalate -- do not guess |

This matters because AI models will give you answers in all four categories but present them all as "True." A governance framework forces the system to label its confidence honestly.

### Escalation Policies

For Intrado, escalation is not optional -- it is how you prevent AI from making life-safety decisions it is not qualified to make:

- **Low stakes** (documentation, formatting, internal tools): AI decides, human is notified
- **Medium stakes** (test plans, performance optimization, non-production config): AI proposes, human approves
- **High stakes** (dispatch logic, call routing, SLA-affecting changes): Human decides, AI provides analysis
- **Critical** (live system changes, PII handling, regulatory submissions): Human decides with peer review, AI provides data only

### Human-in-the-Loop Is Not a Limitation

Keeping humans in the loop for high-stakes decisions is not a failure of AI adoption. It is the architecture that makes AI adoption possible in life-safety domains. The goal is not to remove humans -- it is to ensure humans spend their time on decisions that actually require human judgment, while AI handles everything else.

**Monday action:** Classify your current project backlog into the four stakes categories above. For everything in "low stakes," ask: why does a human still touch this? Remove that bottleneck first.

---

## Summary: The Five Things to Remember

1. **AI is a team member, not a tool.** It needs governance, boundaries, and accountability -- just like any other team member.

2. **Measure ERGOL, not LOLLI.** If a metric would not make a customer or regulator notice, stop tracking it.

3. **Apply AI to the bottleneck.** Amdahl's Law: speeding up the fast part does not help. Find the slow part.

4. **Build factories, not products.** The highest leverage is building systems that build things -- but only when someone needs the output.

5. **Govern uncertainty, do not hide it.** Unknown and Contradictory are valid states. The worst outcome is AI pretending to be certain when it is not.

---

## Sources

- [IEEE: AI-Assisted Dispatch Systems for Emergency Resource Allocation](https://publicsafety.ieee.org/topics/ai-assisted-dispatch-systems-for-optimal-resource-allocation-in-emergencies/)
- [Intrado: AI-Powered Innovations in Emergency Communications](https://www.intrado.com/blog/ai-powered-innovations-transforming-emergency-communications-centers)
- [Intrado: Columbus OH NG911 Upgrades with AI Translation](https://www.intrado.com/news-releases/city-of-columbus-ng911-upgrades)
- [Intrado: AI Voice Translation and Transcription for 911](https://www.intrado.com/news-releases/intrados-ai-voice-translation-and-transcription-technology-speeds-9-1-1-response)
- [Xebia: 2026 -- The Year Software Engineering Becomes AI Native](https://xebia.com/news/2026-the-year-software-engineering-will-become-ai-native/)
- [OnAbout: Multi-Agent AI Orchestration Enterprise Strategy 2025-2026](https://www.onabout.ai/p/mastering-multi-agent-orchestration-architectures-patterns-roi-benchmarks-for-2025-2026)
- [OneReach: Agentic AI Adoption Rates, ROI, and Market Trends 2026](https://onereach.ai/blog/agentic-ai-adoption-rates-roi-market-trends/)
- [Frontiers in Big Data: AI-Powered 911 Call Handler Support](https://www.frontiersin.org/journals/big-data/articles/10.3389/fdata.2025.1594062/full)
- [Wikipedia: Amdahl's Law](https://en.wikipedia.org/wiki/Amdahl%27s_law)
- [Jean-Pierre Petit: The Economicon (ERGOL/LOLLI concept)](https://www.savoir-sans-frontieres.com/JPP/telechargeables/English/the_economicon.htm)
