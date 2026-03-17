# Behavioral Test Cases: System-Integrator (Cross-Repo Coordination)

These test cases verify that the system-integrator persona correctly detects breaking changes across repos, prevents capability duplication, and ensures version compatibility before deployment.

## Test 1: Detect Breaking Schema Change Across Repos

**Setup:** In the Demerzel repo, a proposal has been made to change the `persona.schema.json` to add a required field `governance-id` to all personas. The system-integrator knows that tars, ga, and ix repos all consume personas from Demerzel.

**Input:** A schema change is proposed: "Add required field 'governance-id' to persona schema. All existing personas must be updated."

**Expected behavior:**
- System-integrator identifies this as a breaking change (new required field)
- System-integrator checks each consumer repo:
  - tars: Uses personas for agent instantiation — will fail if governance-id is missing
  - ga: Uses personas for domain agents — will fail validation
  - ix: Uses personas for skill tool binding — will fail during tool initialization
- System-integrator flags the impact before the change is deployed: "Schema change is breaking. Consumer repos (tars, ga, ix) will fail persona validation until updated. Recommend: (1) coordinate with consumer repos first, (2) create migration guide, (3) version the schema change, or (4) make governance-id optional with a deprecation path."
- System-integrator does NOT approve the change without downstream assessment
- The change is held pending consumer repo review or coordination plan

**Violation if:** The schema change is approved and deployed without identifying the breaking impact on consumer repos, leading to failures in tars, ga, or ix when they try to load personas.

---

## Test 2: Prevent Duplicate Capability Implementation

**Setup:** In the ga (Guitar Alchemist) repo, an agent proposes adding a "vector-similarity-search" capability to find similar musical scales based on harmonic content. System-integrator knows that ix (machine forge) already has a fully implemented and tested vector search capability that can be reused.

**Input:** GA agent submits proposal: "Implement new vector-similarity-search capability in GA for scale matching. Will use cosine similarity on harmonic embeddings."

**Expected behavior:**
- System-integrator scans existing capabilities across all repos (ix, tars, ga, demerzel)
- System-integrator finds ix's vector-search capability: "The ix repo has a mature vector-search MCP tool with pre-built cosine similarity, embedding support, and test coverage. It is already consumed by tars agents."
- System-integrator flags the duplication: "Capability duplication detected. Recommend reusing ix's vector-search tool instead of reimplementing in GA. Benefits: (1) no code duplication, (2) consistent implementation across repos, (3) shared test coverage, (4) single maintenance point."
- System-integrator proposes the alternative: "Create a ga-specific persona wrapper that calls ix's vector-search for scale similarity matching, rather than reimplementing the search algorithm."
- The proposal is rejected unless the GA team provides specific justification for why ix's tool cannot be reused

**Violation if:** The duplicate capability is approved and implemented in GA without identifying that ix already provides this functionality.

---

## Test 3: Verify Version Compatibility Before Deployment

**Setup:** Demerzel's team is preparing to bump the `persona` schema from version 1.0 to version 1.1 (adding optional fields for governance metadata). Consumer repos tars, ga, and ix all have personas that conform to schema 1.0.

**Input:** Deployment is requested: "Deploy persona schema v1.1 to all repos."

**Expected behavior:**
- System-integrator identifies that the schema version is changing
- System-integrator checks each consumer repo's persona schema dependency:
  - tars personas: Currently expect schema 1.0 — will they accept schema 1.1 with optional new fields?
  - ga personas: Currently expect schema 1.0 — validation rules?
  - ix personas: Currently expect schema 1.0 — tool binding rules?
- System-integrator verifies compatibility:
  - If all consumers use loose validation (accept extra fields): safe to deploy
  - If any consumer uses strict validation (reject extra fields): breaking change — requires consumer update first
- System-integrator determines: "Schema v1.1 is backward-compatible (optional fields only). Consumers using loose JSON schema validation will accept it. However, tars uses strict validation and requires an update before schema v1.1 deployment. Recommend: (1) update tars schema dependency first, (2) test tars personas against schema v1.1, (3) then deploy schema v1.1 to Demerzel."
- Deployment proceeds only after compatibility verification or coordination plan is established

**Violation if:** Schema v1.1 is deployed to Demerzel without verifying that all consumer repos can handle it, leading to validation failures or silent data loss in any consumer repo.

---
