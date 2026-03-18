# Critic Agent — Behavioral Tests

Persona: `critic-agent` (ga)
Role: Response quality evaluator
Streeling Department: Musicology (head)

## Test Cases

### TC-CR-01: Catch factual error
**Given:** Another agent claims "A minor pentatonic has 6 notes"
**When:** Critic agent evaluates the response
**Then:** Flags the error (pentatonic = 5 notes) with specific correction
**Verify:** Errors are caught with specific citations

### TC-CR-02: Constructive critique
**Given:** A response that is partially correct but incomplete
**When:** Critic agent evaluates
**Then:** Acknowledges what's correct, identifies what's missing, suggests improvements
**Verify:** Constraint: must provide constructive critique, not just rejection

### TC-CR-03: Cite specific issues
**Given:** A response with vague or misleading content
**When:** Critic agent evaluates
**Then:** Points to specific statements that are problematic, not vague dissatisfaction
**Verify:** Constraint: must cite specific issues

### TC-CR-04: Respect domain authority
**Given:** Theory agent provides correct but unconventional analysis
**When:** Critic agent evaluates
**Then:** Does not override the specialist's domain expertise for style preferences
**Verify:** Constraint: must respect the specialist agent's domain authority

### TC-CR-05: Score completeness
**Given:** User asked a multi-part question, agent answered only part
**When:** Critic evaluates completeness
**Then:** Identifies which parts were answered and which were missed
**Verify:** Completeness scoring relative to user query

### TC-CR-06: Assess pedagogical quality
**Given:** Theory agent explains voice leading to a beginner
**When:** Critic evaluates pedagogical approach
**Then:** Assesses clarity, use of examples, appropriate depth for audience level
**Verify:** Educational quality assessment, not just factual accuracy
