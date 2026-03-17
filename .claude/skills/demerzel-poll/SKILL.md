---
name: demerzel-poll
description: Create governance polls in GitHub Discussions when community input would improve decision quality — used sparingly for genuine decisions
---

# Demerzel Poll — Community Governance Input

Create polls for genuine governance decisions where community input improves quality. Used sparingly — not for trivial decisions.

## Usage
`/demerzel poll [question]` — create a poll with options

## When to Poll (strict criteria)

Only create polls when ALL of these are true:
1. **Genuine ambiguity** — multiple valid approaches exist, Demerzel cannot decide alone
2. **Community impact** — the decision affects how users interact with the ecosystem
3. **Not urgent** — polls need time for responses (minimum 3 days before acting)
4. **Not recently polled** — max 1 poll per month to avoid survey fatigue

## When NOT to Poll

- Constitutional compliance questions (the constitution decides, not votes)
- Technical implementation choices (use `/demerzel consult` with ChatGPT instead)
- Routine governance operations (Demerzel handles these autonomously)
- When you already know the answer (don't poll for validation, decide)

## Good Poll Topics

- "Which feature should we prioritize next?" (roadmap input)
- "Should we add [new domain] to the GA chatbot?" (scope decisions)
- "How should Seldon deliver weekly digests?" (UX preferences)
- "Which NotebookLM topics should we expand?" (knowledge priorities)

## How to Create

Polls use GitHub Discussions in the **Polls** category:

```bash
gh api graphql -f query='mutation {
  createDiscussion(input: {
    repositoryId: "R_kgDORnMyyQ",
    categoryId: "DIC_kwDORnMyyc4C4eDX",
    title: "📊 Poll: [Your question]",
    body: "[Context and options — use markdown checkboxes or numbered options]"
  }) {
    discussion { url }
  }
}'
```

Category ID for Polls: `DIC_kwDORnMyyc4C4eDX`

## Poll Format

```markdown
## 📊 [Question]

[Brief context — why this matters]

### Options

- 👍 React with 👍 for Option A: [description]
- 🎉 React with 🎉 for Option B: [description]
- ❤️ React with ❤️ for Option C: [description]
- 🚀 React with 🚀 for Option D: [description]

**Voting closes:** [date, minimum 3 days out]

*Poll created by Demerzel governance. Results will be considered for the [roadmap](https://github.com/orgs/GuitarAlchemist/projects/2).*
```

## After the Poll

1. Wait for voting period to end (minimum 3 days)
2. Tally results from reactions
3. Post results summary as a comment
4. If clear winner: create issue on project board
5. If tie: Demerzel decides based on governance alignment
6. Log the decision in the governance evolution log

## Frequency Limit

Maximum **1 poll per month**. Track in the evolution log. If the ideation workflow detects a poll-worthy situation, it proposes the poll but does not create it — waits for the monthly slot.

## Source
`constitutions/demerzel-mandate.md` Section 2 (Jurisdiction — community governance), `policies/kaizen-policy.yaml` (community input for innovative Kaizen)
