---
name: demerzel-metabuild
description: Factory of factories — given a domain description, bootstrap an entire department with grammar, weights, research config, course pipeline, persona mapping, and behavioral tests. One command → complete production capability.
---

# Demerzel MetaBuild — The Factory of Factories

Don't create a thing. Create the thing that creates things. MetaBuild takes a domain description and produces a complete, self-sustaining production capability.

## Usage

`/demerzel metabuild [domain description]` — bootstrap a new department
`/demerzel metabuild --skill [skill description]` — bootstrap a new skill
`/demerzel metabuild --grammar [domain]` — bootstrap a grammar with evolution hooks
`/demerzel metabuild --pipeline [description]` — bootstrap an end-to-end pipeline
`/demerzel metabuild --repo [name] [description]` — bootstrap a new governed repo

## Philosophy

```
Level 0: Create a thing              → one artifact
Level 1: Create a skill              → artifacts on demand
Level 2: Create a factory            → skills on demand
Level 3: Create a factory of factory → factories on demand (this skill)
```

**MetaBuild is Level 3.** It doesn't create grammars — it creates the capability to create, evolve, and maintain grammars. It doesn't create courses — it creates the pipeline that produces courses from research that produces research from grammars.

## Factory Types

### Factory 1: Department Factory

`/demerzel metabuild [domain description]`

**Input:** "Quantum computing — qubits, gates, circuits, algorithms, error correction"

**Produces:**

```
1. Grammar:        grammars/{prefix}-{domain}.ebnf
                   (weighted productions from domain description)

2. Department:     state/streeling/departments/{domain}.department.json
                   (head persona, research areas, curriculum, consumer repos)

3. Weights:        state/streeling/departments/{domain}.weights.json
                   (uniform initial weights, zero cycle count)

4. Course dir:     state/streeling/courses/{domain}/en/
                   (empty, ready for course-pipeline)

5. University:     state/streeling/university.json
                   (updated with new department)

6. Behavioral test: tests/behavioral/{domain}-cases.md
                    (5+ test cases for the department's persona behavior)

7. README:         state/streeling/courses/{domain}/README.md
                   (course catalog for the department)
```

**Process:**

```
ANALYZE domain description
    ↓ extract concepts, relationships, methods
CLASSIFY into grammar prefix (core/music/sci/gov/human)
    ↓ match to existing prefix or propose new
GENERATE grammar
    ↓ 5-8 production groups, each with 4-8 alternatives
    ↓ include investigation, hypothesis, test, conclude, reflect
    ↓ map conclusions to tetravalent logic
    ↓ add evolution hooks
CREATE department
    ↓ map to head persona (best fit from 14)
    ↓ extract 5-8 research areas
    ↓ generate 10-15 curriculum items
    ↓ identify consumer repos and related departments
INITIALIZE weights
    ↓ uniform distribution
    ↓ zero cycle count
WRITE behavioral tests
    ↓ 5 Given/When/Then scenarios
    ↓ test persona constraints, escalation, and domain boundaries
UPDATE university.json
    ↓ add department to list
VERIFY
    ↓ grammar parses (valid EBNF)
    ↓ department JSON validates against schema
    ↓ weights JSON validates against schema
    ↓ behavioral test follows existing patterns
COMMIT
    ↓ feat: Bootstrap {domain} department via metabuild
```

### Factory 2: Skill Factory

`/demerzel metabuild --skill [description]`

**Input:** "A skill that analyzes harmonic progressions in audio files"

**Produces:**

```
1. Skill:          .claude/skills/{name}/SKILL.md
                   (usage, pipeline, steps, governance)

2. Schema:         schemas/{name}.schema.json
                   (if the skill produces structured output)

3. State dir:      state/{name}/.gitkeep
                   (if the skill persists state)

4. Behavioral test: tests/behavioral/{name}-cases.md
                    (5+ test cases)
```

**Process:**

```
ANALYZE skill description
    ↓ extract: inputs, outputs, steps, governance needs
CLASSIFY skill type
    ↓ demerzel-* (governance) | seldon-* (knowledge) | domain-specific
MAP to existing patterns
    ↓ check existing skills for similar structure
    ↓ reuse patterns (pipeline, gates, compound phase)
GENERATE skill
    ↓ frontmatter (name, description)
    ↓ usage section
    ↓ pipeline with numbered steps
    ↓ governance section (which articles apply)
    ↓ compound phase (what to learn from each run)
CREATE schema (if needed)
    ↓ JSON Schema draft-07
    ↓ required fields, enums, descriptions
WRITE behavioral tests
VERIFY
    ↓ skill follows existing patterns
    ↓ schema validates
    ↓ no governance gaps
COMMIT
```

### Factory 3: Grammar Factory

`/demerzel metabuild --grammar [domain]`

**Input:** "Quantum computing"

**Produces:**

```
1. Grammar:        grammars/{prefix}-{domain}.ebnf
2. Evolution hooks: built into grammar (section 9 pattern)
3. External refs:  docs/external-grammar-references.md (updated)
```

**Process:**

```
ANALYZE domain
    ↓ identify key concepts, methods, subdomains
CLASSIFY prefix
    ↓ core/music/sci/gov/human (or propose new)
RESEARCH external grammars
    ↓ are there formal languages for this domain?
    ↓ (e.g., quantum: QASM, Quil, Cirq syntax)
GENERATE productions
    ↓ 6-10 production groups
    ↓ investigation pattern (observe, hypothesize, test, conclude, reflect)
    ↓ domain-specific methods and concepts
    ↓ tetravalent mapping for conclusions
    ↓ evolution hooks section
    ↓ consumed-by and see-reference headers
VERIFY
    ↓ valid EBNF syntax
    ↓ all productions reachable
    ↓ tetravalent mapping complete
    ↓ evolution hooks present
COMMIT
```

### Factory 4: Pipeline Factory

`/demerzel metabuild --pipeline [description]`

**Input:** "A pipeline that takes a GitHub issue, researches it, produces a plan, executes, and reports"

**Produces:**

```
1. MOG pipeline:   pipelines/{name}.mog
                   (if MOG executor exists)

2. Skill:          .claude/skills/{name}/SKILL.md
                   (pipeline as skill)

3. Schema:         schemas/{name}-run.schema.json
                   (pipeline run log)

4. State dir:      state/{name}/
```

**Process:**

```
ANALYZE pipeline description
    ↓ extract: stages, inputs, outputs, gates
DECOMPOSE into steps
    ↓ each step: tool invocation + governance gate
    ↓ identify parallel vs sequential steps
    ↓ identify compound phase
MAP to MCP tools
    ↓ which tars/ix/ga tools does each step need?
    ↓ check state/tool-catalogs/tars-mcp-tools.json
ASSIGN risk levels
    ↓ per staleness-detection-policy risk classification
    ↓ low/medium/high/critical per step
GENERATE pipeline
    ↓ as MOG if executor available
    ↓ as skill SKILL.md always
CREATE schema for run logging
VERIFY
    ↓ all tools exist in catalog
    ↓ risk gates appropriate
    ↓ compound phase present
COMMIT
```

### Factory 5: Repo Factory

`/demerzel metabuild --repo [name] [description]`

**Input:** "demerzel-dashboard — web dashboard for governance metrics"

**Produces:**

```
1. GitHub repo:    GuitarAlchemist/{name}
2. README.md:      description, setup, architecture
3. Governance:     governance/demerzel/ directory (from templates/)
4. CLAUDE.md:      governance integration snippet
5. .gitignore:     language-appropriate
6. Issue:          created in Demerzel for tracking
7. Directive:      contracts/directives/{name}.directive.md
8. Project board:  added to GuitarAlchemist project #2
```

## Meta-MetaBuild

MetaBuild can bootstrap itself. Given a new factory type description, it produces:

1. A new `--{type}` flag handler in this skill
2. A template for the factory's outputs
3. Behavioral tests for the factory

This is the fixed point: the factory that creates factories can create a factory that creates factories.

## Quality Gates

Every factory output goes through:

1. **Schema validation** — JSON files validate against schemas
2. **Pattern matching** — new artifacts follow existing patterns
3. **Coverage check** — behavioral tests exist for new artifacts
4. **Integration check** — new artifacts are wired into driver cycle
5. **README sync** — all affected READMEs are updated
6. **Evolution hooks** — new artifacts have freshness thresholds and weight tracking

## Anti-Pattern Detection

MetaBuild watches for:

- **Factory without consumers** — created capability nobody uses
- **Factory without evolution** — static factory that doesn't learn
- **Factory bloat** — producing more artifacts than the domain justifies
- **Factory duplication** — two factories producing overlapping outputs

When detected, these become inputs to `/demerzel metafix`.

## Governance

- Article 4 (Proportionality) — factory scope matches domain complexity
- Article 9 (Bounded Autonomy) — factories operate within defined templates
- Article 11 (Ethical Stewardship) — don't over-engineer; YAGNI applies to factories too
- Grammar evolution policy — all produced grammars must be living artifacts
- Staleness detection — all produced state artifacts have freshness thresholds
- README sync — all produced READMEs are registered for sync

## The Hierarchy

```
/demerzel metabuild         → creates factories (departments, skills, grammars, pipelines, repos)
    ↓ produces
/seldon research-cycle      → creates knowledge (questions, evidence, beliefs)
    ↓ feeds
/seldon course-pipeline     → creates courses (content, translations)
    ↓ teaches
Seldon                      → delivers knowledge to humans and agents
    ↓ compounds
/demerzel compound          → creates evolution (patterns, promotions)
    ↓ improves
/demerzel metafix           → creates systemic fixes (detection, prevention)
    ↓ feeds back to
/demerzel metabuild         → improves factories based on what metafix found
```

The loop closes. MetaBuild → production → learning → metafix → better MetaBuild.
