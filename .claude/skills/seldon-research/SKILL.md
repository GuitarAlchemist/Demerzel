---
name: seldon-research
description: Deep research using ChatGPT + NotebookLM + domain knowledge — cross-model validation for high-quality answers and continuous improvement
---

# Seldon Research — Cross-Model Deep Research

Combines ChatGPT (second opinion), NotebookLM (institutional memory), and GA domain knowledge to produce high-quality, validated answers. Every research interaction compounds back into the governance framework.

## Usage
`/seldon research [question]` — full research pipeline
`/seldon research quick [question]` — fast answer without cross-model validation

## Research Pipeline

```
1. Classify question (governance/experiential/domain)
       ↓
2. Check NotebookLM for existing knowledge
       ↓
3. Query GA domain skills if music-related
       ↓
4. Cross-validate with ChatGPT (GPT-4o-mini)
       ↓
5. Assess confidence via tetravalent logic
       ↓
6. Deliver answer with full agentic trace
       ↓
7. Compound: log interaction, update evolution, detect patterns
```

## Step 1: Classify

Determine knowledge layer:
- **Governance:** constitutional articles, policies, compliance → use Demerzel artifacts directly
- **Experiential:** PDCA outcomes, past decisions, patterns → check evolution log + NotebookLM
- **Domain (music):** theory, chords, scales → GA skills + NotebookLM Compound the Compounding

## Step 2: NotebookLM Research

Query the most relevant notebook:
```javascript
mcp__notebooklm__ask_question({
  question: "[processed question]",
  notebook_id: "[best match]"  // compound-the-compounding, probabilistic-grammars, etc.
})
```

If the notebook has relevant context, incorporate it into the answer with citations.

## Step 3: GA Domain Skills

For music theory questions, invoke GA skills conceptually:
- ScaleInfoSkill → scale notes, patterns, formulas
- ChordExplanationSkill → chord construction, qualities
- IntervalInfoSkill → interval identification
- ModeExplorationSkill → modal theory
- ProgressionSuggestionSkill → chord progressions
- HarmonicAnalysisSkill → harmonic function analysis

These produce deterministic answers (confidence 1.0).

## Step 4: ChatGPT Cross-Validation

For non-trivial questions, ask GPT-4o-mini to validate:
```javascript
mcp__openai-chat__openai_chat({
  model: "gpt-4o-mini",
  messages: [
    { role: "system", content: "You are a music theory expert. Verify this answer is accurate. Be concise." },
    { role: "user", content: "[answer to validate]" }
  ]
})
```

- If ChatGPT agrees → confidence increases
- If ChatGPT disagrees → belief state becomes Contradictory (C) → investigate
- If ChatGPT adds useful context → incorporate with attribution

## Step 5: Tetravalent Assessment

Rate the answer:
- **T (True):** Domain computation + ChatGPT agreement + NotebookLM confirmation
- **U (Unknown):** Partial evidence, needs more research
- **C (Contradictory):** Sources disagree → flag for human review
- **F (False):** Answer debunked → do not deliver

## Step 6: Deliver with Trace

Include full agentic trace showing which sources were used, which models validated, and confidence level.

## Step 7: Compound

Every research interaction feeds back:
- **Citation tracking:** Which governance artifacts were used? Update evolution log.
- **Pattern detection:** Is this topic asked frequently? Candidate for dedicated resource.
- **Knowledge gap detection:** Did we fail to answer? Gap in domain coverage → create issue.
- **Improvement proposals:** Could the answer be better? Log as Kaizen opportunity.
- **Cross-repo learning:** Did this reveal something about GA/TARS/IX? Share via Galactic Protocol.

## Compounding Rules

1. **Every unanswered question = governance gap** → create issue in relevant repo
2. **Every answered question = citation** → update evolution log for Seldon + Streeling
3. **Every ChatGPT disagreement = investigation** → log as Contradictory, escalate if serious
4. **Every 3+ questions on same topic = promotion candidate** → propose dedicated guide
5. **Every failed answer = experiential learning** → package as knowledge state for Seldon

## Cost Control (ChatGPT)
- Use GPT-4o-mini only (~$0.15/M input)
- Only cross-validate non-trivial questions (skip for basic chord/scale lookups)
- Max 1 ChatGPT call per question
- Never send user PII or credentials

## Source
`personas/seldon.persona.yaml`, `policies/streeling-policy.yaml`, `policies/scientific-objectivity-policy.yaml` (confidence calibration)
