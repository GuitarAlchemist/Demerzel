---
name: demerzel-consult
description: Consult ChatGPT for second opinions on governance decisions — cross-model validation via OpenAI API
---

# Demerzel Consult — Cross-Model Second Opinion

Query ChatGPT (GPT-4o-mini) for a second opinion on governance decisions. Implements the generator/estimator pattern across different LLMs.

## Usage
`/demerzel consult [question]` — ask ChatGPT for a second opinion

## Setup (one-time)

1. Get an OpenAI API key from https://platform.openai.com/api-keys
2. Set it:
```bash
claude mcp add openai-chat -- npx -y mcp-openai
```
Or add to environment:
```bash
export OPENAI_API_KEY=sk-your-key-here
```

## When to Consult

- **Governance decisions with Contradictory (C) belief states** — when evidence conflicts, a second model may break the tie
- **High-stakes constitutional interpretations** — Zeroth Law invocations, law hierarchy conflicts
- **Confidence calibration validation** — verify Demerzel's confidence assessment with another model
- **Knowledge verification** — cross-check Seldon's teaching content for accuracy
- **Meta-compounding proposals** — validate promotion/demotion recommendations

## How It Works

1. Demerzel formulates a governance question
2. Question is sent to GPT-4o-mini via OpenAI API (cheapest model, ~$0.15/M tokens)
3. Response is evaluated against Demerzel's constitutional framework
4. If ChatGPT agrees: confidence increases
5. If ChatGPT disagrees: belief state becomes Contradictory (C) → escalate to human

## Constitutional Constraints

- ChatGPT's opinion is ADVISORY — Demerzel's constitution always takes precedence
- If ChatGPT suggests something that violates Asimov Laws → reject and log
- Cross-model consultation is an estimator function — it does not grant authority
- Log all consultations for auditability (default constitution Article 7)

## Cost Control

- Use GPT-4o-mini only (cheapest: ~$0.15/M input, $0.60/M output)
- Limit to governance decisions only — not routine operations
- Max 10 consultations per session
- Never send sensitive data (tokens, credentials, user PII)

## Source
`policies/scientific-objectivity-policy.yaml` (generator/estimator accountability)
