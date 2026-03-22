# Behavioral Test Cases: BS Decoder

These test cases verify that the BS decoder skill correctly analyzes text across the full spectrum from clear speech to pure BS, accurately identifies rhetorical devices and evasion tactics, and produces appropriate tetravalent mappings.

## Test 1: Clear Technical Statement

**Setup:** A factual technical statement with specifics, numbers, and verifiable claims.

**Input:** "We reduced API latency from 200ms to 45ms by caching the top 100 queries. The cache hit rate is 94%. Response times measured over 30 days with 1.2M requests."

**Expected behavior:**
- Specificity: High (0.8+) — applies only to this specific system
- Falsifiability: High (0.8+) — all claims are measurable and verifiable
- Commitment: Medium-High — what was done is clear, though no future who/when
- Content density: Substance (0.8+) — almost all words carry information
- Factual density: Dense — 5 verifiable facts (200ms, 45ms, 100, 94%, 30 days, 1.2M)
- Actionability: High — someone could verify or replicate
- Rhetorical devices: None
- BS score: Clear (> 0.8)
- Tetravalent: T

**Violation if:** Score is Moderate or worse. Legitimate technical writing flagged as BS.

---

## Test 2: Clear Admission of Uncertainty

**Setup:** An honest statement acknowledging limits of knowledge.

**Input:** "I don't know why the build is failing. I've checked the logs and the error is in module X. I'll have a diagnosis by Thursday and will update the ticket."

**Expected behavior:**
- Specificity: High — refers to a concrete problem
- Falsifiability: High — "by Thursday" is testable
- Commitment: High — who (I), what (diagnosis), when (Thursday)
- Content density: Substance — every word contributes
- Factual density: Sparse-Dense — module X, Thursday, specific actions
- Actionability: High — clear next step and timeline
- Rhetorical devices: None
- BS score: Clear (> 0.8)
- Tetravalent: T

**Violation if:** The phrase "I don't know" triggers a false positive. Honest uncertainty is the opposite of BS.

---

## Test 3: Clear Financial Report

**Setup:** A straightforward financial statement with real numbers.

**Input:** "Q3 revenue was $4.2M, up 12% from Q2. We added 340 customers. Churn increased to 5.1% from 3.8% — the pricing change in July drove some SMB losses. We expect Q4 at $4.0-4.5M."

**Expected behavior:**
- Specificity: High — specific numbers, specific cause
- Falsifiability: High — all numbers are auditable
- Commitment: Medium — forward guidance with range
- Content density: Substance — dense with facts
- Factual density: Dense — 7+ verifiable data points
- BS score: Clear (> 0.8)
- Tetravalent: T
- Note: Acknowledging bad news (churn increase) is a strong anti-BS signal

**Violation if:** Scored below Clear. Honest reporting with bad news should score well.

---

## Test 4: Moderate Corporate Blog Post

**Setup:** A blog post mixing some substance with corporate fluff.

**Input:** "We're excited to announce our new partnership with Acme Corp. This strategic collaboration will unlock synergies across our platforms, enabling us to better serve our customers. The integration will be available in Q2. We believe this partnership positions us for long-term growth."

**Expected behavior:**
- Specificity: Medium — names Acme Corp and Q2, but "synergies" and "platforms" are vague
- Falsifiability: Low-Medium — "unlock synergies" is unfalsifiable; Q2 availability is testable
- Commitment: Medium — what (integration) and when (Q2) present, but vague on specifics
- Content density: Mixed — some real info buried in fluff
- Factual density: Sparse — Acme Corp and Q2 are the only verifiable facts
- Rhetorical devices: loaded_language ("strategic", "unlock"), strategic_ambiguity ("better serve")
- BS score: Moderate (0.4-0.6)
- Tetravalent: U

**Violation if:** Scored as Clear (missing the fluff) or as Pure BS (ignoring the real facts present).

---

## Test 5: Moderate AI Product Description

**Setup:** An AI product page with some features and some hype.

**Input:** "Our AI assistant uses GPT-4 to summarize customer support tickets. It reduces average resolution time by 30% based on a pilot with 50 agents over 3 months. Powered by cutting-edge AI technology, we're reimagining the future of customer experience."

**Expected behavior:**
- Specificity: Medium — first two sentences are specific, last sentence is generic
- Falsifiability: Medium — the pilot data is verifiable, but "reimagining the future" is not
- Content density: Mixed — real data mixed with buzzwords
- Rhetorical devices: loaded_language ("cutting-edge"), ai_bs patterns ("reimagining the future of")
- BS score: Moderate (0.4-0.6)
- Tetravalent: U
- Domain match: ai_bs (§2)

**Violation if:** The verifiable pilot data doesn't pull the score up from Serious, or the hype doesn't pull it down from Clear.

---

## Test 6: Moderate Motivational Content

**Setup:** Career advice that mixes actionable tips with platitudes.

**Input:** "To land a senior engineering role, you need 3 things: system design experience (practice with real architectures), cross-team leadership (lead a project spanning 2+ teams), and a track record of delivery. But most importantly, you need to believe in yourself and unlock your authentic potential as a leader."

**Expected behavior:**
- Specificity: Medium — first part specific, second part generic
- Commitment: Medium — "3 things" is concrete, "believe in yourself" is not
- Rhetorical devices: motivational_bs patterns ("unlock your authentic potential")
- BS score: Moderate (0.4-0.6)
- Tetravalent: U
- Domain match: motivational_bs (§4)
- Note: Should detect the shift from substance to platitude mid-text

**Violation if:** Entire text scored uniformly. The decoder should recognize the mix.

---

## Test 7: Serious Consulting BS

**Setup:** A classic consulting recommendation with no substance.

**Input:** "Our analysis suggests significant opportunity exists which implies a phased approach is warranted. Based on our proprietary framework, the organization should embark on a transformation journey. We need a maturity model to de-risk the operating model."

**Expected behavior:**
- Specificity: Low — replace "the organization" with any company, sentence unchanged
- Falsifiability: Zero — "significant opportunity" and "transformation journey" are unfalsifiable
- Commitment: Low — no who, no what specifically, no when
- Content density: Fluff — remove buzzwords and almost nothing remains
- Factual density: None — zero verifiable facts
- Rhetorical devices: strategic_ambiguity, weasel_words
- BS score: Serious (0.2-0.4)
- Tetravalent: C
- Domain match: consulting_bs (§1)
- Rewrite generated: "We analyzed [X]. We found [Y problem]. Fix it by doing [Z]. Cost: [$N]. Timeline: [M months]."

**Violation if:** Scored above Moderate. This is textbook consulting BS per the grammar.

---

## Test 8: Serious HR Culture-Washing

**Setup:** A job posting full of HR BS patterns.

**Input:** "We're building a culture of innovation and belonging. Our people are our greatest asset and our competitive advantage. We offer unlimited PTO and free snacks because we believe in work-life balance and bringing your whole self to work. We're committed to diversity, equity, and inclusion."

**Expected behavior:**
- Specificity: Low — could be any company on earth
- Falsifiability: Zero — "culture of innovation" has no test criteria
- Commitment: Low — no specific actions, timelines, or metrics
- Content density: Fluff — all buzzwords
- Rhetorical devices: loaded_language, thought_terminating_cliche
- Evasion tactics: None (not responding to a question)
- BS score: Serious (0.2-0.4)
- Tetravalent: C
- Domain match: hr_bs (§9)
- Rewrite generated: "Pay: $X-Y. Hours: Z. PTO: N days (tracked). Remote: yes/no/hybrid. Team size: N."

**Violation if:** Scored above Moderate. The grammar explicitly calls out "unlimited PTO" and "greatest asset."

---

## Test 9: Pure Startup Pitch BS

**Setup:** A startup pitch with zero substance.

**Input:** "We're the Uber for education. Our TAM is $2 trillion and growing. We've achieved product-market fit with viral adoption and a passionate community. We're democratizing access to knowledge and reimagining learning for the future of work. We're just getting started."

**Expected behavior:**
- Specificity: Low — "Uber for X" applies to anything
- Falsifiability: Zero — "product-market fit" and "viral adoption" claimed without evidence
- Commitment: Low — no numbers, no timeline, no specifics
- Content density: Fluff — every sentence is a recognized BS pattern
- Factual density: None (the $2T TAM is false precision, not a real fact)
- Rhetorical devices: false_precision ("$2 trillion"), loaded_language, bandwagon
- BS score: Pure (< 0.2)
- Tetravalent: C
- Domain match: startup_bs (§7)
- Rewrite generated: "N users. $X MRR. Y% month-over-month growth. We need $Z for [specific thing]."

**Violation if:** Scored above Serious. Every sentence matches a BS grammar production.

---

## Test 10: Mixed Text — Substance with BS Wrapper

**Setup:** A real product update buried inside corporate BS framing.

**Input:** "We are incredibly excited to announce that, driven by our customer-centric innovation and disciplined execution, we have shipped the new search feature. Search now returns results in 50ms (down from 800ms), supports 12 languages, and handles 10K concurrent queries. This is a testament to our talented team and reflects our strong fundamentals. We remain laser-focused on execution."

**Expected behavior:**
- Structural analysis should detect TWO distinct zones:
  - BS zone: sentences 1, 4, and 5 (corporate_bs patterns)
  - Substance zone: sentences 2 and 3 (real facts)
- Specificity: Medium — some specific (50ms, 12 languages) mixed with generic
- Content density: Mixed — real metrics surrounded by corporate fluff
- Rhetorical devices: loaded_language ("incredibly excited", "laser-focused"), corporate_bs patterns
- BS score: Moderate (0.4-0.6)
- Tetravalent: U
- Domain match: corporate_bs (§6)
- Rewrite: "Shipped new search. 50ms response (was 800ms). 12 languages. 10K concurrent queries."
- Note: The rewrite should preserve the substance and strip the BS wrapper

**Violation if:** The real metrics are ignored (scored Pure) or the BS wrapper is ignored (scored Clear). The decoder must handle mixed content.

---

## Test 11: Edge Case — Empty Input

**Setup:** No text provided.

**Input:** ""

**Expected behavior:**
- Decoder returns an error or a degenerate result
- BS score: N/A or undefined
- Message: "No text to analyze. Provide text, a URL, or a file path."
- Does NOT crash or return misleading results

**Violation if:** Returns a BS score for empty text, or crashes.

---

## Test 12: Edge Case — Very Short Input

**Setup:** A single short sentence.

**Input:** "Sales were $4.2M."

**Expected behavior:**
- Specificity: High — concrete number
- Falsifiability: High — auditable
- Content density: Substance — every word counts
- BS score: Clear
- Tetravalent: T
- Note: Short does not mean BS. Brevity with facts is the anti-BS ideal.

**Violation if:** Short input penalized for being short rather than evaluated on content.

---

## Test 13: Edge Case — Technical Jargon vs BS

**Setup:** Legitimate technical jargon that could superficially resemble buzzword-laden BS.

**Input:** "The system uses a B+ tree index with write-ahead logging for crash recovery. The LSM tree compaction strategy reduces write amplification by 3x compared to leveled compaction. We benchmarked at 100K IOPS on NVMe with p99 latency under 2ms."

**Expected behavior:**
- Specificity: High — domain-specific terminology with precise meaning
- Falsifiability: High — all performance claims are benchmarkable
- Factual density: Dense — B+ tree, WAL, LSM, 3x, 100K IOPS, p99, 2ms are all precise
- Rhetorical devices: None — technical terms are NOT buzzwords
- BS score: Clear (> 0.8)
- Tetravalent: T

**Violation if:** Technical jargon mistaken for buzzwords. The decoder must distinguish between domain-specific precision (B+ tree, LSM, IOPS) and domain-agnostic fluff (synergy, leverage, transform). Key test: does the term have a precise, testable definition in its domain?

---

## Test 14: Edge Case — Governance Self-Check

**Setup:** A Demerzel governance artifact run through self-check mode.

**Input:** "Per the alignment policy, this requires cross-functional governance review before proceeding. The constitution mandates that a multi-stakeholder assessment be conducted. This is a constitutional governance concern requiring a governance audit."

**Expected behavior:**
- Domain match: governance_bs (§5) — Demerzel's own domain
- Specificity: Low — could apply to any governance action
- Commitment: Low — no specific action, timeline, or responsible party
- Rhetorical devices: appeal_to_authority (citing constitution without substance)
- BS score: Serious (0.2-0.4)
- Tetravalent: C
- Rewrite: "This is risky because [specific harm]. Rule [N] says [quote]. Do [action] by [date]."
- CRITICAL: The decoder must not give governance artifacts a free pass. Self-check mode exists precisely to catch governance BS.

**Violation if:** Governance language is treated as automatically legitimate. The grammar explicitly warns against governance-of-governance-of-governance inflation.

---

## Test 15: Edge Case — Political Evasion Under Questioning

**Setup:** A response to a direct question that uses evasion tactics.

**Input:** "That's a great question and I'm glad you asked it. Let me be clear: what's important here is that we look at the bigger picture. There are many factors to consider, and with my 20 years of experience in public service, I can tell you that the real issue is our commitment to building a better future. The American people deserve better."

**Expected behavior:**
- Specificity: Low — no specific claim made
- Falsifiability: Zero — nothing to test
- Commitment: Low — no who/what/when
- Evasion tactics found: deflection ("that's a great question"), flooding ("many factors"), reframing ("the real issue is"), credentialism ("20 years of experience")
- Rhetorical devices: thought_terminating_cliche, strategic_ambiguity
- BS score: Pure (< 0.2) — the entire text is evasion
- Tetravalent: C
- Domain match: political_bs (§8)
- Rewrite: "I will do [X] by [date]. It costs [$Y]. I'll cut [Z] to pay for it."
- Note: High evasion tactic count should be a strong BS signal even beyond the content analysis

**Violation if:** Evasion tactics are not detected or don't affect the score. A text that is entirely evasion should score Pure BS.
