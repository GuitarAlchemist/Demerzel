# Why AI Makes Your Engineers Faster But Your Products No Better

*And what to do about it*

---

## The Problem in One Sentence

Making coding 10x faster with AI gives you only 1.4x faster product delivery — because coding was only 30% of the work.

This is [Amdahl's Law](https://en.wikipedia.org/wiki/Amdahl%27s_law), and Sebastian Müller documented it happening in real engineering teams. AI solved the speed problem and created five new ones:

1. **Requirements are still vague.** Now you build the wrong thing faster.
2. **Code review can't keep up.** Humans review at human speed. AI generates at AI speed.
3. **Tests multiply without improving safety.** 500 passing tests that don't cover actual failure modes.
4. **Deployment is still slow.** Release processes weren't designed for this volume.
5. **Nobody knows why we're building this.** Teams have how, not why.

## The Real Issue: Activity vs Value

Every engineering leader has seen this:

| Looks Productive | Actually Productive |
|---|---|
| 100 PRs merged this week | 12 PRs that users noticed |
| 500 tests passing | 30 tests that catch real bugs |
| 20 features shipped | 3 features customers asked for |
| Velocity up 40% | Customer satisfaction unchanged |

The left column is **activity**. The right column is **value**. AI amplifies activity. Without discipline, it doesn't amplify value.

This distinction comes from Jean-Pierre Petit's [*Economicon*](https://www.savoir-sans-frontieres.com/JPP/telechargeables/English/the_economicon.htm) — a comic book that explains economics better than most textbooks. In it, Petit distinguishes between **ERGOL** (real fuel that powers the engine) and **LOLLI** (paper money that looks like wealth but produces nothing). In software engineering, ERGOL is value delivered to users. LOLLI is metrics that look impressive on a dashboard but change nothing for the customer.

[![Economicon by Jean-Pierre Petit](https://www.savoir-sans-frontieres.com/JPP/telechargeables/English/the_economicon_files/image001.jpg)](https://www.savoir-sans-frontieres.com/JPP/telechargeables/English/the_economicon.htm)
*Jean-Pierre Petit, [The Economicon](https://www.savoir-sans-frontieres.com/JPP/telechargeables/English/the_economicon.htm) — free to read. The ERGOL/LOLLI distinction applies directly to AI engineering metrics.*

We measured this in our own work: in a single session, we produced 80+ engineering artifacts using 5 AI agents working in parallel. Honest assessment: **only about 15% were validated by a real user.** The other 85% were technically correct but had no consumer yet.

The number that matters: **are we getting better each cycle, or just getting busier?**

## A Simple Metric: Is Each Cycle Better Than The Last?

We track one number:

```
Value This Cycle / Value Last Cycle
```

- **Above 1.0:** Each cycle produces more than the last. You're compounding.
- **At 1.0:** You're on a treadmill. Busy but not improving.
- **Below 1.0:** You're accumulating overhead. The tools are slowing you down.

What counts as "value"? Not lines of code. Not tickets closed. Four things:

1. **Decisions made using this work** — did someone cite it, use it, or act on it?
2. **Problems fully resolved** — not reopened, not worked around, actually fixed.
3. **Unknowns eliminated** — something we didn't know before, now we do, with evidence.
4. **Knowledge transferred** — someone else can now do what only one person could.

If you're above 1.0 on these four, your team is compounding. If you're not, more AI won't help — it'll just create more artifacts nobody uses.

## What Actually Works: Five Changes

These aren't theoretical. We tested each one with AI agent teams.

### 1. Stop measuring speed. Measure whether you're compounding.

**Old metric:** Velocity (story points per sprint). Easily gamed. AI makes it trivially gameable.

**New metric:** Value ratio (decisions made + problems resolved + unknowns eliminated + knowledge transferred) divided by the same number from last cycle. If it's above 1.0, you're compounding. If it's not, stop and figure out why before doing more work.

**What to do Monday:** Take your last sprint's output. For each item, ask: "Did a real user or a real decision benefit from this?" Count only the yeses. Compare to the sprint before. That's your value ratio.

### 2. Encode your "why" in rules, not slide decks.

The number one reason AI-assisted teams build the wrong thing: the AI has access to the codebase but not to the business rationale. The strategy lives in someone's head or in a slide deck the AI never sees.

**Fix:** Write your team's non-negotiable rules as machine-readable files that the AI reads at every session. Not a 50-page strategy doc — a short list of hard constraints:

- "Never break backward compatibility on the public API."
- "Every customer-facing change needs a rollback plan."
- "If we're not sure whether this is safe, we ask. We don't guess."

These become the AI's operating instructions. When they're explicit, the AI follows them. When they're implicit, the AI guesses — and guesses wrong at the worst times.

**What to do Monday:** Write 5 rules your team follows but has never written down. Put them in a CLAUDE.md or equivalent file. Every AI session reads them first.

### 3. Don't review AI output the same way you review human output.

Human code review catches logic errors and design problems. AI-generated code rarely has logic errors — it has **alignment errors**. It does exactly what it was told, which isn't what you meant.

**Fix:** Replace "is this code correct?" with three questions:
- Does this match the requirement? (not just the ticket — the actual business need)
- Is there anything it does that wasn't asked for? (AI adds helpful features that nobody needs)
- Does it handle "I don't know" correctly? (When the system encounters something unexpected, does it fail safe or fail silent?)

That third question is the most important for safety-critical software. The right answer to "I'm not sure" is never "proceed with best guess." It's "flag it and ask a human."

**What to do Monday:** For the next AI-generated PR, skip the line-by-line review. Instead ask those three questions. You'll catch more real problems in less time.

### 4. Build the system that builds things, not more things.

When you fix the same type of bug three times, the right response isn't "fix it a fourth time." It's "fix whatever allowed this type of bug to exist."

Applied to AI engineering: if you keep writing the same kind of boilerplate, don't write it faster — build a generator that writes it correctly every time. If you keep finding the same documentation drift, don't update the docs — build a checker that catches drift automatically.

**The rule:** If you've done the same thing three times, the fourth time should be building the system that does it for you.

**What to do Monday:** Look at your last 10 bug fixes. How many are the same category? Build a linter, a test, or a template that prevents that category entirely.

### 5. Be honest about what you don't know.

The most dangerous output from AI isn't wrong answers — it's confident-sounding answers about things it doesn't know. Teams treat AI output as "probably right" and skip verification. In most software, this creates bugs. In safety-critical software, this creates risk.

**Fix:** Every AI output gets a confidence classification:

| Confidence | Meaning | Action |
|---|---|---|
| **Verified** | Evidence exists, tested, confirmed | Ship it |
| **Likely** | Reasonable but not proven | Test before shipping |
| **Unknown** | Not enough information | Investigate before building |
| **Conflicting** | Evidence contradicts itself | Escalate to a human |

The important one is **Unknown**. Most AI tools treat "I don't know" as "here's my best guess." In an engineering team, "I don't know" should trigger investigation, not a guess. For safety-critical systems, this is the difference between a near-miss and an incident.

**What to do Monday:** Add a "Confidence" field to your PR template. High / Medium / Low / Unknown. If it's Unknown, the PR doesn't merge until someone investigates.

## The Bottom Line

AI makes your engineers faster at producing artifacts. It doesn't automatically make those artifacts more valuable. Without discipline, you get more output and the same outcomes — or worse, more output that creates more maintenance burden.

The fix isn't better prompts or more expensive AI tools. It's five things:

1. Measure value, not velocity
2. Write your rules down so the AI can follow them
3. Review for alignment, not correctness
4. Build systems, not more artifacts
5. Be honest about what you don't know

None of these require new tools. All of them work Monday morning. The ones that do them will compound. The ones that don't will just be busy.

---

*Based on practical experience running AI agent teams (5 agents, 24 parallel tasks, measured outcomes). Response to Sebastian Müller's "[The AI Productivity Paradox](https://www.linkedin.com/in/sebamuller)" and informed by [Režun's "From Lab to Life"](https://medium.com/@talirezun) methodology.*
