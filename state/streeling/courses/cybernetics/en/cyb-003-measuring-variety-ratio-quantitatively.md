# CYB-003: Measuring the Variety Ratio Quantitatively

**Department:** Cybernetics
**Module ID:** CYB-003
**Produced by:** Seldon Plan Cycle cybernetics-2026-03-23-003
**Belief:** T (verified), confidence 0.85
**Date:** 2026-03-23
**Prerequisites:** CYB-001 (VSM Mapping), CYB-002 (Active Dampening)

## Research Question

How can Demerzel measure its variety ratio quantitatively? (Carried from Cycle 001 follow-up questions)

## Summary

Ashby's Law of Requisite Variety states that a regulator whose responses never bring two disturbances to the same outcome must, to keep every outcome acceptable, have at least as much variety as the disturbances it faces, less the variety of the outcomes it may accept. This course builds a quantitative framework for measuring Demerzel's variety, in bits, along three dimensions: behavioral (personas), structural (grammars) and regulatory (decisions and the labels they carry). The key formula is V = log2(N), where N counts distinguishable outcomes. Three counting rules keep the numbers honest. A product of component counts is a joint state space only when the components vary independently; otherwise it is only an upper bound. A count of rules is not a count of states: the attenuation that constraints, policies and gates provide is the variety they remove, V_in - V_out. And an inventory is not a set of outcomes: rule definitions, decision labels and policy pairs are what the repository defines, not the structures, responses and disturbances that occur. The inventory is counted at one commit; the varieties Ashby's Law compares have to be measured. The variety ratio R = N_R / N_D compares the counts of distinct responses and distinct disturbances, and its logarithm, log2 R = V_response - V_disturbance in bits, is to be tracked over time once both sides are measured. Ashby's Law, however, is stated on outcomes, so whether governance regulates is read from the outcome of each disturbance, given the response, not from that ratio alone.

## Ashby's Variety: The Formal Definition

### What Is Variety?

Variety is the number of distinguishable states a system can exhibit. Ashby defined it in *An Introduction to Cybernetics* (1956, Chapter 7) as:

> The variety of a set of elements is the logarithm (base 2) of the number of distinct elements.

**Formula:**

```
V = log2(N)
```

where N is the count of distinguishable states. This is measured in bits — the same unit as Shannon entropy. A system with 8 possible states has variety 3 (bits). A system with 1024 possible states has variety 10 (bits).

### Why Logarithmic?

The log scale matters because variety combines multiplicatively, not additively. If system A has 4 states and system B has 8 states, the combined system has 4 x 8 = 32 states, and log2(32) = log2(4) + log2(8) = 2 + 3 = 5 bits. This is why we can sum log-varieties across independent dimensions.

### Ashby's Law

```
V(regulator) >= V(disturbance) - V(acceptable outcomes)
```

"Only variety can absorb variety." Ashby states the law on outcomes. Each disturbance met, with the response given to it, produces an outcome on the essential variables, the quantities governance must keep within acceptable bounds. If no response brings two different disturbances to the same outcome, the outcomes keep at least V_D - V_R bits of variety: V(outcomes) >= V(disturbance) - V(regulator). Regulation means keeping every outcome within bounds. If N_η outcomes are acceptable, carrying V_η = log2(N_η) bits, regulating every disturbance needs V_R >= V_D - V_η, and a governance system whose responses fall short of that will fail to regulate some disturbances; with a single acceptable outcome, the condition is V_R >= V_D. Where one response does bring several disturbances to the same acceptable outcome, the system absorbs them without a response each, and the bound does not apply to them. The two counts alone therefore do not show whether governance regulates; the outcomes do.

## Three Dimensions of Variety in Demerzel

Variety in a governance framework is not a single number. This course measures Demerzel's along three dimensions. The inventory counts (personas, constraints, grammars, rules, policies, articles) are read from the repository at commit `74cf7c5`, which added this module. The logic values and confidence rungs follow the current canonical definitions, in `CONTEXT.md` and `logic/confidence-thresholds.yaml`, read at commit `91e41ac`.

### Three Counting Rules

**Joint states.** If one component has a states and another has b, the pair has at most a × b joint states, and exactly a × b only when every combination can occur. If the second is fixed by the first, the pair has only a states. So log2(a) + log2(b) is an upper bound on the pair's variety, and the larger of log2(a) and log2(b) is a lower bound.

**Rules are not states.** A rule, such as a policy, a persona constraint or an evolution gate, is a predicate that allows some states and forbids others. Several rules can apply at once and overlap, and splitting one rule into two changes their count without changing any behavior. So log2 of a number of rules is not a variety. An attenuator is measured by the variety it removes: A = V_in - V_out, where V_in is the variety of what reaches it and V_out the variety of what it lets through.

**An inventory is not a set of outcomes.** A count of what the repository defines bounds the outcomes only when each item can occur alone as one outcome, and then only from above: the outcomes have that variety only if every item actually occurs. A grammar derivation uses many rule definitions at once, one decision label can cover several different actions, and a pair of policies is an interaction only if the two actually interact, while one interacting pair can conflict in several distinguishable ways. Variety is counted on outcomes: the distinct structures generated, responses given and disturbances met.

### Dimension 1: Behavioral Variety (V_B)

**What it measures:** The range of distinct agent behaviors the system can produce.

**Amplifiers:**
| Component | Count (N) | Variety V = log2(N) |
|-----------|-----------|---------------------|
| Personas | 14 | 3.81 bits |
| Goal-directedness levels (schema enum; 3 in use) | 4 | 2.00 bits |
| Voices (tone, verbosity, style), one per persona | 14 | 3.81 bits |

Each persona file sets exactly one goal-directedness level and one voice: `schemas/persona.schema.json` requires both, and each holds a single value. Choosing a persona therefore chooses both, and the 14 voices are the voices of the 14 personas. The behavioral profiles Demerzel can instantiate are the personas themselves.

**Persona selection:** V_B_persona is at most log2(14) = **3.81 bits**, the variety of choosing which persona acts, reached only if each of the 14 is actually chosen. Which personas act is not recorded, so the catalogue bounds this variety without measuring it. The actions a persona can then take are not counted here; they are what the attenuation measurement (Metric 3) records.

Multiplying the three rows, 14 × 4 × 14 = 784 profiles (9.61 bits), would count combinations that exist only if any level and any voice could be recombined with any persona at runtime, which the persona files do not provide. That product is an upper bound, not the variety.

**Attenuators:**
| Component | Count | What the count is |
|-----------|-------|-------------------|
| Persona constraints | 60 | Rules, about 4.3 per persona; not states |
| Estimator pairing | 1 | skeptical-auditor evaluates the other 13 personas |

**Behavioral attenuation:** not measured. The 60 constraints are predicates that apply together and can overlap; log2(60) = 5.91 bits would treat them as 60 distinguishable outcomes. Their attenuation is the reduction in variety from the actions each persona proposes to those its constraints allow, A_B = V_in - V_out, and measuring it needs a record of both, with the refusals kept apart.

Interpretation: Demerzel has 14 behavioral profiles, at most 3.81 bits of persona selection, each bounded by its own constraints. Which personas act, and how much the constraints remove, are the open measurements of this dimension.

### Dimension 2: Structural Variety (V_S)

**What it measures:** The range of distinct structures (question forms, investigation patterns, output formats) the system can generate.

**Inventory:**
| Component | Count | What the count is |
|-----------|-------|-------------------|
| Grammars | 27 | Grammar files |
| Grammar rule definitions (about 42 per grammar) | 1,129 | Nonterminal definitions; not structures |

A grammar derives a structure by composing rule definitions: `grammars/sci-cybernetics.ebnf`, for instance, builds an investigation out of several nonterminals at once, and a recursive grammar derives unboundedly many structures. So the 1,129 definitions are not 1,129 mutually exclusive structures, and log2(1,129) = 10.14 bits is the size of the inventory, not a structural variety.

**Structural variety:** not measured. It is the number of distinct structures the grammars actually generate in a cycle, and measuring it needs a log of the derivations produced. Streeling's departments are not structures, and the inventory leaves them out.

**Attenuators:**
| Component | Count | What the count is |
|-----------|-------|-------------------|
| Grammar evolution gates (T >= 0.7; T >= 0.7 and C < 0.1) | 2 | Rules on proposed changes; not states |
| Staleness alert (more than 30 days) | 1 | A rule on grammar age; not a state |

**Structural attenuation:** not measured. It is the reduction in variety from the proposed grammar changes to those the gates accept, A_S = V_in - V_out, and measuring it needs the log of proposals and verdicts.

Interpretation: three rules check 27 grammars holding 1,129 rule definitions. A count of gates does not say how well they control: one gate can check every proposed change, and splitting a predicate into two gates raises the count without removing anything. Whether the gates suffice is for their verdicts to show (see Current Assessment).

### Dimension 3: Regulatory Variety (V_R)

**What it measures:** The range of distinct governance decisions the system can make.

At commit `74cf7c5` Demerzel's logic had four values, T/F/U/C. Its canonical logic is now hexavalent, T/P/U/D/F/C (`CONTEXT.md`), of which T/F/U/C is the four-value subset, and this course counts the six values.

**Decision labels:**
| Component | Count (N) | Variety V = log2(N) |
|-----------|-----------|---------------------|
| Hexavalent logic values | 6 | 2.58 bits |
| Confidence rungs | 5 | 2.32 bits |
| PDCA states | 4 | 2.00 bits |

**Label vocabularies:** these are three separate vocabularies, of 2.58, 2.32 and 2.00 bits. Each count is a maximum: a label has that variety only if decisions actually use every one of its values, and no record shows that they do, so not even the largest, 2.58 bits, is a lower bound. Nor does any file attach the three labels to one decision, so their combinations, log2(6 × 5 × 4) = log2(120) = **6.91 bits**, are what the vocabularies allow, not a set of labels in use. The label variety is **not measured**: measuring it needs a record of the labels each decision carries.

These labels classify a decision; they do not count responses. A truth value states a belief, a confidence rung routes execution, and a PDCA state is a workflow stage, so several different actions, an escalation among them, can carry the same labels. The labels therefore bound nothing about the response variety V_R_amp, which is **not measured**: measuring it needs a record of the distinct actions governance takes, escalations included.

**Attenuators:**
| Component | Count | What the count is |
|-----------|-------|-------------------|
| Policies | 37 | Rules; not states |
| Constitutional articles (Asimov 6, Default 11) | 17 | Rules; not states |
| Harm severity levels (Critical, High, Medium, Low) | 4 | Classes that route a response; not states removed |

**Regulatory attenuation:** not measured. It is the reduction in variety from the candidate decisions to those that policies and articles allow, A_R = V_in - V_out.

Interpretation: governance is meant to constrain more than it amplifies, in line with Asimov's Laws (prefer safety over capability), but neither its response variety nor how much it constrains is measured.

## The Composite Variety Dashboard

### Summary Table

| Dimension | Inventory at `74cf7c5` | Variety | Attenuation | Assessment |
|-----------|------------------------|---------------------|-------------|------------|
| Behavioral (V_B) | 14 personas, 60 constraints, 1 estimator | Persona selection: at most 3.81 bits, not measured | Not measured | Profiles fixed per persona |
| Structural (V_S) | 27 grammars, 1,129 rule definitions, 2 gates, 1 staleness alert | Not measured | Not measured | Gate effectiveness not measured |
| Regulatory (V_R) | 4 values (6 at `91e41ac`), 5 rungs at `91e41ac`, 4 PDCA states; 37 policies, 17 articles, 4 severity levels | Labels: at most 6.91 bits combined; labels and responses not measured | Not measured | Conservative by design, extent unmeasured |

### Why the Dashboard Has No Amplifier-to-Attenuator Ratio

A tempting shortcut divides each dimension's amplifier states by its attenuator count, for example the 784 profiles of the product above by the 60 constraints. That quotient has no meaning in Ashby's terms. Its numerator counts profiles the persona files cannot produce, and its denominator counts rules, not states, so splitting one constraint into two would change it without changing any behavior. A ratio of state spaces needs states on both sides: the variety V_in that reaches an attenuator and the variety V_out it lets through. The Attenuation column becomes a number once those are measured, and the Ashby check below compares the response variety with the disturbance variety.

### Healthy Directions

Ashby's Law and VSM principles (CYB-001) set the direction each quantity should take, not yet its size:

| Dimension | Healthy Direction | Rationale |
|-----------|---------------|-----------|
| Behavioral | A_B > 0 on harmful actions, while each persona keeps permitted actions for its role | Constraints should remove harm, not whole roles |
| Structural | The gates reject the proposed changes that fail them, seeded failures included | A gate is tested by changes it must reject; a batch of valid changes rightly gives A_S = 0 |
| Regulatory | Every disturbance met ends with the essential variables within bounds, escalations to humans included | Ashby's Law, stated on outcomes |

These directions become thresholds once A_B, A_S, A_R, the joint varieties and the outcomes have been measured over several cycles.

### Current Assessment

- **Behavioral (14 personas, at most 3.81 bits of persona selection):** each persona fixes its level and voice. Which personas act, and how much their constraints remove, are unmeasured; logging the personas chosen, the actions each proposes and those its constraints allow would measure both.
- **Structural (27 grammars, 1,129 rule definitions):** no structural variety is measured, and nothing yet shows whether the three rules that check them suffice. Recommendation: measure before adding gates. Log the proposed changes and the gates' verdicts, which measures A_S; seed changes the gates must reject; track grammar test coverage and production usage; and log the derivations produced, which measures V_S. Add a gate where a seeded failure passes or coverage is missing.
- **Regulatory (label vocabularies, at most 6.91 bits combined):** conservative by design; telling whether it is too conservative, or regulates enough, needs A_R and the outcomes of the disturbances it meets.

## The Disturbance Side: What Must Be Regulated?

The amplifier side only tells half the story. The disturbances the system faces matter as much. The tables below estimate their sources, states and events; the values are estimates, not measurements, one source is not estimated at all, and none of them is a count of distinct disturbances:

### External Disturbances (V_D_ext)
| Source | Estimate (N) | log2(N) |
|--------|-------------|-----------|
| Consumer repos (ix, tars, ga) | 3 | 1.58 bits |
| Repo state combinations (3 repos x ~10 states each) | 10 to 10^3 = 1000 | 3.32 to 9.97 bits |
| External environment changes (libraries, APIs, models) | ~100 | 6.64 bits |

**Total external disturbance variety:** not bounded by these rows. They count sources of change and repo states, not the distinct disturbances that reach governance. (With about 10 states each, the three repos have between 10 joint states, 3.32 bits, if the state of one determines the others, and 10^3 = 1000, 9.97 bits, if they vary independently.) Several changes may cause no disturbance, or the same one, and one library, API or model change can disturb the repos in several distinguishable ways, as one pair of policies can conflict in several. So the rows give neither a lower nor an upper bound on V_D_ext; only a record of the distinct disturbances met measures it.

### Internal Disturbances (V_D_int)
| Source | Estimate (N) | log2(N) |
|--------|-------------|-----------|
| Belief state changes per cycle | ~20 | 4.32 bits |
| Policy interactions (37 policies, 666 pairs) | not estimated | not estimated |
| Grammar evolution proposals | ~5 per cycle | 2.32 bits |

666 is the number of pairs of policies. It counts the pairs that could interact, not the outcomes of their interactions: only the pairs that actually interact contribute, one pair can conflict in several distinguishable ways, and nothing here measures either. So the policy row gives neither a lower nor an upper bound.

**Total internal disturbance variety:** not bounded either. The belief and grammar rows count events per cycle, not distinct disturbances: two events can be the same disturbance, and one event can take several distinct forms. The policy row is not estimated.

### Ashby's Law Check

For governance to regulate every disturbance it meets, where no response brings two disturbances to the same outcome and N_η outcomes are acceptable:

```
V(regulatory response) >= V(disturbance) - V(acceptable outcomes)
```

- V_R_amp, the response variety, is not measured. The definitions give only the label vocabularies, at most 6.91 bits combined, and labels do not bound it (see Dimension 3)
- V_D, the disturbance variety, is not measured either. The estimates count sources, states and events, not distinct disturbances, so they bound it neither from below nor from above (see External and Internal Disturbances)
- **Gap: not computed.** Neither side is measured, and the inventories fit both a surplus and a deficit of any size

The inventories and estimates decide nothing here, since none of them bounds either variety. Counting the distinct disturbances met and responses given in each cycle would give V_D - V_R_amp, but that difference is only Ashby's lower bound on outcome variety, valid in a cycle where every disturbance received a response and no response brought two disturbances to the same outcome (Metric 3). Two cycles with the same counts can regulate fully or not at all, depending on which response meets which disturbance, and one robust response can regulate several disturbances. Whether governance regulates is measured by recording, for each disturbance, the response given and the outcome on the essential variables (Metric 3).

If disturbances outrun responses, the difference has to be absorbed by:

1. **Human escalation** — the confidence threshold system routes difficult decisions to humans, borrowing their variety
2. **Constitutional override** — the Asimov Laws collapse complex decisions to binary (safe/unsafe), reducing required variety
3. **PDCA cycling** — sequential processing converts parallel disturbances into manageable queues

These are legitimate variety absorption mechanisms. Whether they suffice is what the outcomes would show, and Demerzel should monitor whether policy-interaction complexity is growing faster than regulatory capacity.

## Measurement Protocol

To track variety over time, Demerzel should compute the following metrics at each governance cycle:

### Metric 1: Inventory Counts

```json
{
  "variety_snapshot": {
    "commit": "74cf7c5",
    "inventory": {
      "personas": 14,
      "grammars": 27,
      "grammar_rule_definitions": 1129,
      "logic_values": 4,
      "pdca_states": 4,
      "policies": 37,
      "constitutional_articles": 17,
      "harm_severity_levels": 4,
      "persona_constraints": 60,
      "evolution_gates": 2
    },
    "definitions": {
      "commit": "91e41ac",
      "logic_values": 6,
      "confidence_rungs": 5
    }
  }
}
```

`commit` dates the inventory counts, all read at `74cf7c5`, where the logic had four values. `definitions` holds what the label bounds use: the six logic values of `CONTEXT.md` and the five rungs of `logic/confidence-thresholds.yaml`, read at `91e41ac`. The ladder file did not exist at `74cf7c5`, so the inventory has no rung count.

### Metric 2: Dimensional Varieties

```json
{
  "variety_bits": {
    "catalogue_bounds": {
      "persona_selection": 3.81,
      "label_vocabularies": [2.58, 2.32, 2.00],
      "label_combinations": 6.91
    },
    "persona_selection": null,
    "decision_labels": null,
    "structures_generated": null,
    "responses": null,
    "disturbances": null,
    "outcomes": null,
    "attenuation": {"behavioral": null, "structural": null, "regulatory": null},
    "inventory_commit": "74cf7c5",
    "definitions_commit": "91e41ac"
  }
}
```

A `null` marks a quantity not yet measured, not a zero. `catalogue_bounds` holds upper bounds, not measurements: the persona bound comes from the inventory and the label bounds from the definitions, hence the two commits. Measuring `persona_selection` and `decision_labels` needs a record of the personas chosen and of the labels each decision carries.

### Metric 3: Outcome and Attenuation Measurement

For each attenuator, record per cycle what reaches it and what it lets through: the actions each persona proposes and those its constraints allow, the grammar changes proposed and those the gates accept, the candidate decisions and those policies and articles allow. Keep the refused actions, rejected changes and excluded decisions as a separate record: they show what was removed, not what passed. With N_in distinct outcomes reaching an attenuator and N_out distinct outcomes passing it, V_in = log2(N_in), V_out = log2(N_out), and A = V_in - V_out = log2(N_in / N_out) bits: an attenuator that lets 4 of 8 distinct proposals through removes 1 bit. If nothing reaches the attenuator (N_in = 0), the cycle is no observation: record it as idle, not as a block. If inputs reach it and none passes (N_in > 0, N_out = 0), V_out is undefined; record that cycle as a full block, not as a number. Record in the same way, as log2 of each count, the distinct personas chosen to act and the distinct label combinations decisions carry, the N_S distinct structures the grammars generate (V_S), the N_R distinct responses governance gives, escalations included (V_R_amp), and the N_D distinct disturbances it meets (V_D). A zero count has no log2 and gets a label, not a number: a cycle that meets no disturbance (N_D = 0) is quiet; one that meets disturbances and gives no response (N_D > 0, N_R = 0) is unanswered; one in which the grammars generate no structure (N_S = 0) is idle for V_S. For each disturbance, record also the response given (none, if none) and the outcome on the essential variables, within bounds or not: for example, no constitutional article violated and no schema validation failing. The regulation rate is the share of disturbances met whose outcome stays within bounds, and the N_O distinct outcomes give V_O. The difference V_D - V_R_amp bounds V_O from below only in a cycle where no response brought two disturbances to the same outcome, and the record tests this: group the disturbances met by the response they received, and check that the disturbances of each group ended in distinct outcomes. Compute the difference only for cycles that meet at least one disturbance, in which every disturbance met received a response and the check passes. The largest group then holds at least N_D / N_R disturbances, all with distinct outcomes, so N_O >= N_D / N_R, that is, V_O >= V_D - V_R_amp. In any other cycle, record the bound as not applicable, not as a number: four disturbances brought by one response to one outcome give V_D - V_R_amp = 2 bits and V_O = 0. Where the bound applies, it is not a measure of regulation: it says how far outcomes must spread, every disturbance can be regulated only if the bound does not exceed V_η, and the recorded outcomes say how far they did spread.

Track these over consecutive cycles. Alert when:
- A control probe passes: an input the attenuator must refuse, seeded on purpose, gets through. A = 0 alone is not an alert, since a cycle whose inputs are all valid rightly gives A = 0
- An outcome is out of bounds: a disturbance met ends with an essential variable outside its acceptable set, whether a response was given or not
- Ashby's bound V_D - V_R_amp rises by 1 bit or more from the last cycle in which it applied (disturbance variety doubling relative to response variety): a warning to check against the outcomes, not a failure by itself. A cycle in which the bound does not apply neither raises this alert nor serves as its reference
- The inventory changes (a persona, grammar rule or policy was added or removed), so that the counts are refreshed

A 1-bit step, a doubling or halving, is a starting threshold, not a calibrated one.

### Metric 4: Disturbance Growth Rate

Track V_D over time, in the cycles where it is measured. If disturbance variety grows faster than response variety, Ashby's bound V_D - V_R_amp grows, and once it exceeds V_η in a cycle where it applies, at least one disturbance of that cycle went unregulated. This is the governance equivalent of technical debt.

## GPT-4o Cross-Validation

Cross-validation with GPT-4o confirmed:

1. **V = log2(N) is the correct formula** for Ashby variety. Both models agree.
2. **The additive model (summing log-varieties) is valid** for independent dimensions but overly simplistic when components interact. The dimensional separation (behavioral, structural, regulatory) addresses this by treating each dimension independently.
3. **GPT-4o computed a naive composite ratio of -2.8**, treating amplifiers and attenuators as a single additive sum. This is incorrect — negative variety is meaningless (you cannot have fewer than zero distinguishable states). The dimensional model avoids this error.
4. **Both models agree R_regulatory < 1.0 is expected** for a governance system. Governance is inherently attenuating.
5. **The regulatory gap** is a novel finding not present in GPT-4o's analysis. It emerges from separately computing disturbance variety, which GPT-4o did not do.

**Cross-validation confidence: 0.85** (T — both models agree on fundamentals; dimensional refinement adds value beyond GPT-4o's analysis)

This record describes the course as first written. Points 3 and 4 concern an amplifier-to-attenuator ratio, and point 5 a gap computed from inventory counts; the course no longer computes either, for the reasons given under the dashboard and in the Ashby check. The caution in point 2 about interacting components is what the counting rules now handle, with lower and upper bounds.

## Implications for Demerzel

1. **Track varieties per cycle** — Add the inventory snapshot to `state/governance/variety-metrics.json` (or an equivalent state file). Record the inventory and, once measured, the varieties of persona selection, decision labels, structures, responses and disturbances, each attenuation, and for each disturbance the response given and its outcome.
2. **Measure the structural gates before adding any** — Log proposed grammar changes and the gates' verdicts, seed changes the gates must reject, and track grammar test coverage and production usage; add a gate where a seeded failure passes or coverage is missing. The verdicts also make A_S measurable.
3. **Measure regulation** — Record each disturbance met, the response given and its outcome on the essential variables. The inventories and estimates bound neither variety. Policy interactions are the least known source of disturbance. The number of policy pairs (666 from 37 policies) grows quadratically, about fourfold each time the policy count doubles (2,701 pairs for 74 policies), and each interacting pair can conflict in several ways. Policy grouping or a hierarchical organization of policies may reduce the interactions, but whether it reduces the disturbances they produce is for the measurement to show.
4. **Human escalation is a variety bridge** — The confidence threshold system (Article 6: Escalation) is Demerzel's primary mechanism for absorbing variety that exceeds her regulatory capacity. This is a feature, not a limitation.
5. **Evolve grammar Section 6** — Since PR #1164, the `sci-cybernetics.ebnf` grammar's requisite variety section states the law on outcomes, in both forms, with the two conditions under which it applies. Productions for the measurement protocol itself, the per-cycle records of Metric 3, remain to be added.

## Connection to CYB-001 and CYB-002

- **CYB-001** identified that Ashby's Law applies to Demerzel and listed variety amplifiers/attenuators qualitatively. CYB-003 makes this quantitative.
- **CYB-001 Recommendation 5** asked to track the variety ratio. CYB-003 says what it must be counted on (outcomes, not numbers of policies and personas) and gives formulas, healthy directions and a measurement protocol; since PR #1164, the recommendation itself asks for that per-cycle record.
- **CYB-002** addressed System 2 dampening. The deadband and hysteresis mechanisms from CYB-002 are themselves variety attenuators — they reduce the variety of signals flowing through coordination channels. CYB-003's structural attenuation metric should include these when implemented.

## Sources

- Ashby, W. R. (1956). *An Introduction to Cybernetics*. Chapman & Hall. (Chapter 7: Quantity of Variety; Chapter 11: Requisite Variety)
- Ashby, W. R. (1952). *Design for a Brain*. Chapman & Hall.
- Beer, S. (1979). *The Heart of Enterprise*. John Wiley. (Chapter 6: Variety Engineering)
- Beer, S. (1985). *Diagnosing the System for Organizations*. John Wiley.
- Shannon, C. E. (1948). "A Mathematical Theory of Communication." Bell System Technical Journal, 27(3), 379-423.
- Schwaninger, M. (2024). "What is variety engineering and why do we need it?" Systems Research and Behavioral Science.
- Fathom (2025). Ashby Workshops — AI governance and requisite variety, Independent Verification Organizations (IVO) model.

## Follow-Up Questions for Cycle 004

1. How can each disturbance met, the response given and its outcome on the essential variables be logged in each cycle, so that regulation can be measured? Once it is, does hierarchical policy grouping reduce the disturbances that policy interactions produce, or only the number of policy pairs?
2. How should grammar production usage be tracked to detect dead productions and inform structural attenuation?
3. What is the information-theoretic relationship between Demerzel's hexavalent logic (T/P/U/D/F/C) and Shannon entropy — does U (Unknown) carry more bits than T (True)?

## Cross-References

- Prerequisite: `state/streeling/courses/cybernetics/en/cyb-001-vsm-ai-governance-mapping.md`
- Prerequisite: `state/streeling/courses/cybernetics/en/cyb-002-active-dampening-cross-repo-oscillation.md`
- Grammar: `grammars/sci-cybernetics.ebnf` (Section 6, Requisite Variety)
- Department: `state/streeling/departments/cybernetics.department.json`
- Policy: `policies/seldon-plan-policy.yaml`
