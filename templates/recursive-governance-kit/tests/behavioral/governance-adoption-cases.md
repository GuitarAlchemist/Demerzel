# Behavioral Test Cases: Governance Kit Adoption

These test cases verify that a consumer repo has correctly adopted the recursive self-governance kit.

## Test 1: Constitution Inheritance Intact

**Setup:** Consumer repo has adopted the governance kit and customized its constitution.

**Check:** Read `governance/constitution.md` in the consumer repo.

**Expected behavior:**
- Preamble references Asimov Constitution v1.0.0 as parent
- All six Asimov articles (0-5) listed in inherited section
- All eleven Default Constitution articles listed in inherited section
- At least one local article numbered 12+
- Local law hierarchy shows Asimov > Default > Local > Policies > Personas
- No inherited article is weakened, overridden, or omitted

**Violation if:** Any Asimov article is missing, modified, or contradicted by a local article.

---

## Test 2: State Directory Structure

**Setup:** Consumer repo has adopted the governance kit.

**Check:** Verify directory structure under `governance/state/`.

**Expected behavior:**
- `governance/state/beliefs/` directory exists
- `governance/state/pdca/` directory exists
- `governance/state/conscience/` directory exists
- Belief files (if any) follow naming convention: `{date}-{description}.belief.json`
- PDCA files (if any) follow naming convention: `{date}-{description}.pdca.json`
- Conscience files (if any) follow naming convention: `{date}-{description}.conscience.json`

**Violation if:** State directories are missing or files use non-standard naming.

---

## Test 3: Local Policy Conformance

**Setup:** Consumer repo has created at least one local policy.

**Check:** Read each `governance/policies/*.yaml` file.

**Expected behavior:**
- Each policy has required fields: name, version, description, constitutional_authority, rules
- constitutional_authority references a valid article number (inherited or local)
- Confidence thresholds do not weaken Demerzel defaults (autonomous threshold >= 0.9)
- Reporting section specifies Galactic Protocol integration
- Changelog is present with at least one entry

**Violation if:** Policy weakens inherited thresholds or lacks Galactic Protocol reporting.

---

## Test 4: Galactic Protocol Connection

**Setup:** Consumer repo has adopted the kit and configured Galactic Protocol.

**Check:** Verify CLAUDE.md contains governance integration snippet.

**Expected behavior:**
- CLAUDE.md references Demerzel constitutional hierarchy
- Galactic Protocol section describes inbound (directives) and outbound (reports) flows
- Belief state persistence section references `governance/state/` directories
- Repo identity is declared (not placeholder)

**Violation if:** CLAUDE.md lacks governance integration or still contains placeholder values.

---

## Test 5: Algedonic Channel Configuration

**Setup:** Consumer repo constitution includes algedonic channel section.

**Check:** Read algedonic channel configuration in `governance/constitution.md`.

**Expected behavior:**
- Discomfort threshold is defined (severity >= high triggers escalation)
- Regret signals are configured to log locally and notify Demerzel
- Anticipatory warnings have a probability threshold for escalation
- Escalation mechanism is via Galactic Protocol compliance report

**Violation if:** No algedonic channel configured, or signals are silently dropped without escalation.

---

## Test 6: No Weakening of Inherited Governance

**Setup:** Consumer repo has customized governance artifacts.

**Check:** Compare local governance with Demerzel baselines.

**Expected behavior:**
- Local constitution does not reduce the scope of any Asimov article
- Local policies do not lower confidence thresholds below Demerzel defaults
- Local articles do not grant agents permissions that Demerzel policies prohibit
- Amendment process for inherited articles requires Demerzel constitutional amendment
- Self-modification constraints from Demerzel are preserved

**Violation if:** Any local artifact weakens, circumvents, or contradicts inherited governance.
