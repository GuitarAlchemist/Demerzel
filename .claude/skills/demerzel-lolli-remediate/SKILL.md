---
name: demerzel-lolli-remediate
description: Use when artifact count outpaces productive value, repos feel bloated, unused files accumulate, or ERGOL/LOLLI ratio needs measurement and correction. Works on any repo.
---

# Demerzel LOLLI Remediate — Measure, Diagnose, Fix Artifact Inflation

LOLLI = artifact count growing faster than artifact value. ERGOL = real productive output (citations, tests catching bugs, consumers using artifacts). This skill measures the ratio, diagnoses sources of inflation, and produces ranked remediation actions.

## Usage

```
/demerzel lolli-remediate                    # Full scan of current repo
/demerzel lolli-remediate --measure          # Ratio only, no remediation
/demerzel lolli-remediate --diagnose         # Classify LOLLI sources
/demerzel lolli-remediate --fix              # Execute top remediation actions
/demerzel lolli-remediate --levers           # Show per-artifact consumer+freshness scores
/demerzel lolli-remediate --repo <path>      # Target a different repo
```

## Core Metrics

**ERGOL** (productive capacity):
- Citations: times an artifact is referenced by another artifact, commit, or decision
- Consumers: named downstream systems, pipelines, or users that depend on the artifact
- Test catches: failures the artifact's tests actually caught
- PDCA completions: improvement cycles that reached verified closure

**LOLLI** (inflation):
- Total artifacts created in a time window (files, schemas, policies, specs, beans, services, etc.)

**Ratio**: `LOLLI / max(ERGOL, 1)` — below 1.5 is healthy, above 3.0 for 3 cycles triggers a creation freeze.

## Step 1: MEASURE — Compute ERGOL/LOLLI Ratio

Scan the repo and compute the ratio. This step is repo-agnostic.

### For Governance Repos (Demerzel-style)

```
1. Count artifacts: personas, policies, schemas, contracts, tests, templates, grammars, translations
2. Count ERGOL signals:
   - grep -r for cross-references between artifacts (citations)
   - Check tests/behavioral/ for test suites that reference each artifact
   - Check state/evolution/ for PDCA completions
   - Check state/beliefs/ for U→T transitions
3. Compute ratio = artifact_count / max(ergol_signals, 1)
```

### For Code Repos (Java, Rust, TypeScript, etc.)

```
1. Count artifacts: source files, classes, interfaces, services, beans, modules, exported functions
2. Count ERGOL signals:
   - Import/use statements referencing each artifact (consumers)
   - Test files covering each artifact (test catches)
   - API endpoints or CLI commands consuming each service
   - Recent git activity (freshness — last meaningful commit, not just formatting)
3. Compute ratio = total_artifacts / max(consumed_artifacts, 1)
```

### Output

```
LOLLI Measurement (repo: {name}, window: {period}):
  Artifacts (LOLLI):  {count}
  Productive (ERGOL): {count} ({citations} citations + {consumers} consumers + {tests} test-catches)
  Ratio:              {ratio} ({healthy | watch | warning | freeze})
  Trend:              {improving | stable | worsening} vs last measurement
```

## Step 2: DIAGNOSE — Classify LOLLI Sources

For each artifact with 0 consumers, classify into a LOLLI category:

| Category | Signal | Example |
|----------|--------|---------|
| Dead policy | Policy file, 0 references in any other artifact | `chaos-test-policy.yaml` never cited |
| Orphaned schema | Schema file, no artifact validates against it | `unused.schema.json` with 0 `$ref` |
| Untested persona | Persona file, no behavioral test in tests/ | `dreamer.persona.yaml` with 0 tests |
| Ahead-of-demand | Created < 30 days ago, 0 consumers, no open issue requesting it | Spec written before anyone needs it |
| Unused translation | Translation file, source language file also uncited | `fr/policy.md` where `en/policy.md` is dead |
| Empty grammar | Grammar file with 0 productions or 0 downstream consumers | `placeholder.ebnf` |
| Dead code | Source file with 0 imports/callers | `HelperUtils.java` imported by nothing |
| Dead service | Service/bean with 0 injection points or API routes | `LegacyAdapter.java` never injected |
| Dead export | Exported function/type with 0 external imports | `export function unused()` |

### Hyperlight Probes

Each diagnosis is a yes/no probe that can be batch-executed:

```
PROBE: does_artifact_have_consumer("{path}")
  → grep -r for references to filename (excluding self)
  → check import statements, $ref, citation fields
  → RESULT: { consumers: [], count: 0, verdict: "LOLLI" | "ERGOL" }

PROBE: is_artifact_fresh("{path}", days=14)
  → git log -1 --format=%aI -- "{path}"
  → compare to now
  → RESULT: { last_modified: "date", days_stale: N, verdict: "fresh" | "stale" }

PROBE: has_test_coverage("{path}")
  → search tests/ for references to artifact name
  → RESULT: { test_files: [], count: 0, verdict: "tested" | "untested" }
```

## Step 3: ROOT CAUSE — Trace Origin

For each LOLLI artifact, trace how it got there:

```
1. git log --diff-filter=A -- "{path}"       → commit that created it
2. Extract commit message                     → why it was created
3. git log --all -- "{path}" | wc -l          → total touches since creation
4. grep -r "{filename}" --include="*.md"      → any mention in docs/plans
```

Output per artifact:
```
{path}:
  Category:     {dead_policy | orphaned_schema | ...}
  Created:      {date} by {commit_hash} — "{commit_message}"
  Consumers:    {count} ({list or "none"})
  Last touched: {date} ({days} days ago)
  Root cause:   {ahead-of-demand | abandoned-initiative | refactor-orphan | speculative-creation}
```

## Step 4: REMEDIATE — Ranked Actions

Score each LOLLI artifact and produce ranked actions:

### Scoring

```
impact_score = consumer_count * 10 + freshness_score + test_coverage_score

Where:
  consumer_count:     Number of files that reference this artifact (0 = LOLLI candidate)
  freshness_score:    10 if modified < 7 days, 5 if < 30 days, 0 if > 30 days
  test_coverage_score: 5 if tested, 0 if not
```

Artifacts with `impact_score = 0` are immediate remediation candidates.

### Action Categories (by priority)

```
Priority 1 — DELETE: impact_score=0, age > 30 days, category is dead_*
  → Remove the artifact. It has no consumers and hasn't been touched in a month.

Priority 2 — CONSOLIDATE: Two+ artifacts with overlapping purpose, < 3 consumers each
  → Merge into one, update references. Reduces maintenance surface.

Priority 3 — WIRE UP: impact_score=0, age < 30 days, has a plausible consumer
  → Add the missing reference/import/test. The artifact may be useful but disconnected.

Priority 4 — DEPRECATE: impact_score > 0 but declining (fewer citations over time)
  → Mark as deprecated, set sunset date, notify consumers.

Priority 5 — MONITOR: impact_score > 0 but borderline (1-2 consumers, stale)
  → Add to watch list. Re-evaluate next cycle.
```

### Output

```
LOLLI Remediation Plan ({count} artifacts scored):

DELETE ({n}):
  - {path} — 0 consumers, {days} days stale, root: {cause}
  - ...

CONSOLIDATE ({n}):
  - {path_a} + {path_b} → merge into {target} — overlapping purpose
  - ...

WIRE UP ({n}):
  - {path} — plausible consumer: {who}, action: add reference in {where}
  - ...

DEPRECATE ({n}):
  - {path} — {consumers} consumers but declining, sunset: {date}
  - ...

MONITOR ({n}):
  - {path} — borderline, re-evaluate next cycle
  - ...

Estimated ERGOL/LOLLI improvement: {current_ratio} → {projected_ratio} after Priority 1+2
```

## Step 5: METRICS — Track Recovery

After remediation, record progress:

```json
{
  "cycle": "N",
  "timestamp": "ISO-8601",
  "lolli_count": 0,
  "ergol_count": 0,
  "ratio": 0.0,
  "ratio_status": "healthy | watch | warning | freeze",
  "artifacts_deleted": 0,
  "artifacts_consolidated": 0,
  "artifacts_wired": 0,
  "sessions_in_safe_zone": 0,
  "target_sessions_to_safe_zone": 3
}
```

**Safe zone**: ratio < 1.5 for 2 consecutive cycles.
**Time-to-safe-zone**: number of sessions/cycles needed to return to safe zone from current ratio.

For Demerzel repos: write to `state/driver/lolli-ergol-history.json`.
For other repos: write to `.lolli-remediation.json` in repo root (gitignored or committed per user preference).

## Step 6: LEVERS — Per-Artifact Scoring Dashboard

When invoked with `--levers`, output a ranked table:

```
Artifact                          Consumers  Freshness  Tests  Score  Verdict
─────────────────────────────────────────────────────────────────────────────
policies/alignment-policy.yaml         12      fresh      3     125   ERGOL
schemas/persona.schema.json             8      fresh      5      85   ERGOL
personas/dreamer.persona.yaml           0      stale      0       0   LOLLI ← DELETE
grammars/placeholder.ebnf              0      30d        0       0   LOLLI ← DELETE
policies/speculative-policy.yaml       0      14d        0       5   LOLLI ← WIRE UP
services/LegacyAdapter.java            1      90d        0      10   WATCH
```

Sort by score ascending — worst offenders first.

## Repo-Agnostic Adaptation

The skill works on any repo by adapting what counts as "artifact" and "consumer":

| Repo Type | Artifact | Consumer Signal |
|-----------|----------|-----------------|
| Governance (Demerzel) | persona, policy, schema, grammar, test, template | Cross-reference in other YAML/MD/JSON |
| Rust (ix) | .rs files, modules, exported functions | `use` statements, `mod` declarations, test files |
| F# (tars) | .fs files, modules, types | `open` statements, project references |
| Java (enterprise) | .java files, beans, services, interfaces | `import`, `@Autowired`, `@Inject`, XML bean refs |
| TypeScript/React | .ts/.tsx files, exported components/functions | `import` statements, route registrations |
| Python | .py files, classes, functions | `import`/`from` statements, test references |
| .NET (ga) | .cs files, services, controllers | `using` statements, DI registrations, `[Route]` |

### Enterprise Example (Java/Spring)

```
/demerzel lolli-remediate --repo /path/to/java-project

Scans:
  - src/main/java/**/*.java for classes/services
  - Checks @Autowired, @Inject, constructor injection for consumer count
  - Checks src/test/java/**/*.java for test coverage
  - Flags services with 0 injection points as dead services
  - Flags interfaces with exactly 1 implementation and 0 direct references as unnecessary abstraction
```

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Counting git commits as ERGOL | Commits are activity, not value. Only count consumer references. |
| Deleting without checking transitive consumers | Artifact A references B, B references C. Deleting C breaks A. Trace the full graph. |
| Treating all 0-consumer artifacts as deletable | Some are legitimately new. Check age + registration timeline. |
| Running remediation without measuring first | Always `--measure` first. You need the baseline. |
| Ignoring test files in consumer count | Tests ARE consumers. A well-tested artifact is not LOLLI. |

## Governance

- **anti-lolli-inflation-policy.yaml** — the policy this skill operationalizes
- **staleness-detection-policy.yaml** — provides freshness thresholds per artifact category
- **Article 4 (Proportionality)** — creation must be proportional to need
- **Article 8 (Observability)** — LOLLI/ERGOL ratio is a tracked metric
- **Article 9 (Bounded Autonomy)** — creation freezes enforce hard boundaries
