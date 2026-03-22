---
name: articulate
description: "Articulate clearly — transform vague ideas, complex systems, or fuzzy plans into crisp, specific, actionable communication. The anti-BS generator."
---

# /demerzel articulate

Transform vague communication into clear, specific, actionable language. The inverse of the BS detector.

## Usage

```
/demerzel articulate <text or topic>
/demerzel articulate --audience <director|engineer|customer|investor>
/demerzel articulate --format <elevator-pitch|one-pager|decision-doc|status-update|architecture-brief>
```

## The Clarity Framework

Every output passes the **4 Clarity Tests** (inverse of the 4 BS Tests):

### Test 1: Specificity
- ❌ "We're improving system performance"
- ✅ "We're reducing API latency from 800ms to 200ms by adding Redis caching to the /search endpoint"
- **Rule:** Every claim names a specific thing, a specific metric, and a specific action

### Test 2: Falsifiability
- ❌ "This will create significant value"
- ✅ "This will reduce support tickets by 30% within 60 days — if it doesn't, we pivot"
- **Rule:** Every claim has a way to prove it wrong

### Test 3: Density
- ❌ "We are strategically leveraging our innovative AI-powered platform to drive unprecedented value creation across the enterprise"
- ✅ "We built a chatbot. It answers guitar theory questions. 4 users tested it today. They liked it."
- **Rule:** Remove every adjective. If the sentence still works, keep only that version.

### Test 4: Commitment
- ❌ "We should explore this opportunity going forward"
- ✅ "I will build a prototype by Friday. Maria will test it Monday. We decide Tuesday."
- **Rule:** WHO does WHAT by WHEN. Missing any = incomplete.

## Output Formats

### Elevator Pitch (30 seconds)
```
[WHAT] in one sentence.
[WHY] it matters — one metric or pain point.
[HOW] it works — one mechanism.
[PROOF] it's real — one evidence point.
```

Example:
> We built an AI chatbot that answers guitar theory questions using formal music grammars. Guitarists ask "reharmonize Let It Be in jazz style" and get actual chord analysis — not generic AI fluff. It's live on Discord right now with real users.

### One-Pager
```
## Problem (2 sentences)
What's broken, who feels the pain, what it costs.

## Solution (3 sentences)
What we built, how it works, what's different.

## Evidence (bullet points)
- Metric 1: specific number
- Metric 2: specific number
- User quote or observation

## Next Steps (WHO does WHAT by WHEN)
- [ ] Person → Action → Date
- [ ] Person → Action → Date

## Risks (honest)
- What could go wrong
- What we don't know yet (U state)
```

### Decision Document
```
## Decision Needed
One sentence: what are we deciding?

## Options
| Option | Pros | Cons | Effort | Confidence |
|--------|------|------|--------|------------|

## Recommendation
Which option, why, what evidence.

## If We're Wrong
What's the rollback plan? (Article 3: Reversibility)
```

### Status Update
```
## Done (this period)
- Specific deliverable → specific outcome
- Specific deliverable → specific outcome

## Blocked
- What's blocked → why → who can unblock

## Next (coming period)
- WHO → WHAT → WHEN

## Metrics
| Metric | Target | Actual | Trend |
```

### Architecture Brief
```
## What It Does (1 paragraph, no jargon)

## How It Works (diagram or 3 bullet points)

## Why This Design (trade-offs considered)

## Dependencies (what it needs, what needs it)

## Risks (what could break)
```

## Audience Adaptation

### For Directors
- Lead with BUSINESS IMPACT, not technical details
- Use the Elevator Pitch format
- Include: cost, timeline, risk, ROI
- No jargon — if you must use a technical term, define it inline
- **The director test:** "If I forwarded this to MY boss, would they understand it?"

### For Engineers
- Lead with ARCHITECTURE, then rationale
- Include code examples or diagrams
- Be specific about trade-offs and alternatives considered
- **The engineer test:** "Could I implement this from what's written?"

### For Customers
- Lead with THEIR PAIN POINT, then your solution
- Use their language, not yours
- Show, don't tell (demo > description)
- **The customer test:** "Does this make me want to try it?"

### For Investors
- Lead with MARKET SIZE, then traction
- Specific numbers: users, revenue, growth rate
- Comparable companies (but honest about differences)
- **The investor test:** "Would I put money into this?"

## Process

1. **Input:** Receive vague text, topic, or "articulate this project"
2. **Diagnose:** Run 4 Clarity Tests on current state — what's vague?
3. **Ask:** What's the audience? What decision does this serve?
4. **Draft:** Generate in the appropriate format
5. **Verify:** Re-run 4 Clarity Tests on the output
6. **Iterate:** If any test fails, fix and re-verify

## Cross-Pollination

This skill works in ANY repo, not just GuitarAlchemist:
- Copy `.claude/skills/demerzel-articulate/` to your work repo
- Use `/demerzel articulate` before sending any status update, design doc, or proposal
- The 4 Clarity Tests apply universally — music, governance, enterprise, anything

## Anti-Patterns

| Anti-Pattern | What It Looks Like | Fix |
|---|---|---|
| **Hedge stacking** | "We might potentially consider exploring..." | Pick a verb. One. |
| **Jargon shield** | Using technical terms to avoid commitment | Define or replace every term |
| **Metrics avoidance** | "Significant improvement" with no numbers | Name the number or say "I don't know yet" |
| **Passive voice escape** | "It was decided that..." | WHO decided? |
| **Future tense everything** | "We will...", "We plan to..." | What have you DONE? |
| **Scope inflation** | Listing 20 features instead of the 3 that matter | What's the ONE thing? |

## Constitutional Basis

- **Article 1 (Truthfulness):** Don't fabricate clarity — if you don't know, say U
- **Article 2 (Transparency):** Explain reasoning, not just conclusions
- **Article 5 (Non-Deception):** Clarity that hides problems is worse than vagueness
- **Manifesto #4 (Tetravalent Truth):** Unknown is a valid state — "I don't have this data yet" is clearer than a made-up number
