---
name: demerzel-bootstrap-governance
description: Bootstrap recursive self-governance in a consumer repo -- copies kit, customizes constitution, configures Galactic Protocol, sets up algedonic channel, runs initial audit
---

# Bootstrap Recursive Governance

Bootstrap a consumer repo with Demerzel's recursive self-governance kit, giving it its own S1-S5 subsystem federated under Demerzel.

## Usage

`/demerzel bootstrap-governance [repo]`

Where `[repo]` is one of: `ix`, `tars`, `ga`, or a path to a local repo.

## Steps

### Step 1: Copy Template to Target Repo

Copy the contents of `templates/recursive-governance-kit/` to the target repo under `governance/`:

```
governance/
  constitution.md
  policies/
    local-policy-template.yaml
  state/
    beliefs/.gitkeep
    pdca/.gitkeep
    conscience/.gitkeep
  tests/behavioral/
    governance-adoption-cases.md
```

Do NOT copy README.md (it stays in Demerzel as documentation).

### Step 2: Customize Constitution

Edit `governance/constitution.md` in the target repo:

1. Replace `[REPO_NAME]` with the actual repo name (ix, tars, or ga)
2. Replace `[DATE]` with today's date
3. Replace `[DOMAIN_DESCRIPTION]` with the repo's domain:
   - ix: "Rust ML forge -- machine learning pipelines, model training, inference"
   - tars: "F# reasoning engine -- cognitive agents, inference chains, belief management"
   - ga: ".NET music platform -- Guitar Alchemist, music generation, audio processing"
4. Add at least one local article (Article 12) specific to the repo's domain:
   - ix: ML model safety -- models require validation pipeline approval before deployment
   - tars: Reasoning integrity -- inference chains must be traceable and falsifiable
   - ga: Content safety -- generated audio must not contain harmful or unauthorized samples
5. Verify inherited articles are listed correctly (Asimov 0-5, Default 1-11)

### Step 3: Configure Galactic Protocol Connection

1. Append the `CLAUDE.md.snippet` content to the target repo's `CLAUDE.md`
2. Replace placeholder references with actual Demerzel repo paths
3. Ensure the repo declares its identity in the governance integration section
4. Verify Galactic Protocol section describes:
   - Inbound: directives, knowledge packages from Demerzel
   - Outbound: compliance reports, belief snapshots, learning outcomes, algedonic alerts
   - This establishes the local S3 -> Demerzel S2 coordination link

### Step 4: Set Up Local Algedonic Channel

1. Verify `governance/constitution.md` has the algedonic channel configuration table
2. Configure thresholds appropriate to the repo's risk profile:
   - ix (ML): Lower thresholds (ML errors cascade) -- anticipatory warning at probability >= 0.6
   - tars (reasoning): Standard thresholds -- anticipatory warning at probability >= 0.7
   - ga (music): Standard thresholds -- anticipatory warning at probability >= 0.7
3. Ensure escalation path routes to Demerzel via Galactic Protocol compliance-report
4. This establishes the local S5 -> Demerzel S5 algedonic link

### Step 5: Run Initial Governance Audit

Run through each test case in `governance/tests/behavioral/governance-adoption-cases.md`:

1. **Constitution Inheritance Intact** -- verify all Asimov articles inherited, local articles present
2. **State Directory Structure** -- verify beliefs/, pdca/, conscience/ directories exist
3. **Local Policy Conformance** -- verify at least the template policy exists
4. **Galactic Protocol Connection** -- verify CLAUDE.md has governance integration
5. **Algedonic Channel Configuration** -- verify thresholds and escalation paths
6. **No Weakening of Inherited Governance** -- verify no inherited article is weakened

Report results as a governance adoption belief state in `governance/state/beliefs/{date}-governance-adoption.belief.json`.

## Post-Bootstrap

After bootstrap completes:

1. **Commit** the governance directory with message: `feat: adopt Demerzel recursive self-governance kit`
2. **Notify Demerzel** -- the adoption should be reported as a compliance report responding to the recursive-governance directive
3. **Create first PDCA** -- start a Plan phase for the repo's first governance improvement cycle

## Source

- Template: `templates/recursive-governance-kit/`
- Galactic Protocol: `contracts/galactic-protocol.md`
- Directive: `contracts/directives/recursive-governance-directive.md`
- VSM Course: `state/streeling/courses/cybernetics/en/CYB-001-vsm-ai-governance-mapping.md`
