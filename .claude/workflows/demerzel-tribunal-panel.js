export const meta = {
  name: 'demerzel-tribunal-panel',
  description: 'Multi-persona QA tribunal: fan a PR diff to N persona reviewers, reach consensus, emit a contract-valid qa-verdict.json',
  whenToUse:
    'Phase 0 of qa-tribunal.yml emits a single-reviewer "informational" verdict with a regex blast_radius. This ' +
    'workflow is the deferred Phase-3 multi-reviewer step: it dispatches the PR diff to several Demerzel personas ' +
    '(each a distinct reviewer role), reaches a strictest-wins consensus, and writes a verdict conforming to the ' +
    'frozen schemas/contracts/qa-verdict.schema.json (self-validated, never edits the schema). ' +
    'Run as /demerzel-tribunal-panel with args { repo: "owner/name", pr: <number> }.',
  phases: [
    { title: 'Gather', detail: 'fetch PR title/body/diff/changed-files via gh; derive blast_radius' },
    { title: 'Deliberate', detail: 'each persona reviews the diff for its concern → sub-verdict + findings' },
    { title: 'Synthesize', detail: 'strictest-wins consensus → assemble + jsonschema-validate + write the verdict' },
  ],
}

// ── Inputs ────────────────────────────────────────────────────────────────────
// args: { repo: "owner/name" (required), pr: <number> (required), dryRun?: bool }
const REPO = args && args.repo
const PR = args && args.pr
const DRY_RUN = !!(args && args.dryRun)
const SCHEMA_PATH = 'schemas/contracts/qa-verdict.schema.json'
const EMITTER_REF = 'scripts/qa_tribunal_emit.py'
const VERDICT_ROOT = 'state/quality/verdicts'

if (!REPO || !PR) {
  log('Missing required args. Call with { repo: "owner/name", pr: <number> }.')
  return { error: 'missing_args', need: { repo: 'owner/name', pr: 'number' } }
}

// Personas → reviewer_chain roles (roles MUST be from the schema enum).
const PANEL = [
  { persona: 'skeptical-auditor', role: 'security', concern: 'hidden risk, unverified assumptions, security/data-safety holes, things that will break silently' },
  { persona: 'reflective-architect', role: 'architecture', concern: 'layering, coupling, pattern fit with existing code, structural debt introduced' },
  { persona: 'rational-administrator', role: 'contract_audit', concern: 'cross-repo JSON contracts, schemas, public API shapes, one-way-door changes that need coordination' },
  { persona: 'validator-reflector', role: 'regression_replay', concern: 'test coverage of the change, missing/weakened invariants, regression surface' },
  { persona: 'system-integrator', role: 'semantic_judge', concern: 'does the change actually do what the PR claims; integration/wiring correctness end to end' },
]

// ── Schemas (agent structured output) ─────────────────────────────────────────
const GATHER_SCHEMA = {
  type: 'object',
  required: ['healthy', 'repo', 'pr'],
  properties: {
    healthy: { type: 'boolean', description: 'true only if gh actually returned PR data' },
    repo: { type: 'string', description: 'owner/name' },
    pr: { type: 'number' },
    title: { type: 'string' },
    body: { type: 'string' },
    head_sha: { type: 'string' },
    base_sha: { type: 'string' },
    files: { type: 'array', items: { type: 'string' } },
    additions: { type: 'number' },
    deletions: { type: 'number' },
    diff_excerpt: { type: 'string', description: 'unified diff, truncated to ~15k chars' },
    blast_radius: {
      type: 'object',
      required: ['layers_touched', 'one_way_doors_crossed', 'invariants_at_risk', 'components_reached', 'estimated_blast_score'],
      properties: {
        layers_touched: { type: 'array', items: { type: 'string' } },
        one_way_doors_crossed: { type: 'array', items: { type: 'string' } },
        invariants_at_risk: { type: 'array', items: { type: 'string' } },
        components_reached: { type: 'array', items: { type: 'string' } },
        estimated_blast_score: { type: 'number' },
      },
    },
    note: { type: 'string' },
  },
}
const PERSONA_SCHEMA = {
  type: 'object',
  required: ['verdict', 'risk_tier', 'findings'],
  properties: {
    verdict: { type: 'string', enum: ['block', 'merge_with_followups', 'pass'] },
    risk_tier: { type: 'string', enum: ['P0', 'P1', 'P2', 'P3'] },
    score: { type: 'number', description: '0..1 confidence in this PR for my concern (1 = clean)' },
    notes: { type: 'string', description: 'one-line summary in this persona voice' },
    findings: {
      type: 'array',
      items: {
        type: 'object',
        required: ['severity', 'title', 'rationale', 'blocks_merge'],
        properties: {
          severity: { type: 'string', enum: ['must_fix', 'should_fix', 'nice_to_have', 'info'] },
          title: { type: 'string' },
          rationale: { type: 'string' },
          location: { type: 'string' },
          proposed_test: { type: 'string' },
          blocks_merge: { type: 'boolean' },
        },
      },
    },
  },
}
const WRITE_SCHEMA = {
  type: 'object',
  required: ['valid', 'written_path'],
  properties: {
    valid: { type: 'boolean', description: 'true only if the object passed jsonschema validation against the contract' },
    written_path: { type: 'string' },
    validation_error: { type: 'string' },
    summary: { type: 'string' },
  },
}

// ════════════════════════════════════════════════════════════════════════════
// PHASE 1 — Gather PR context
// ════════════════════════════════════════════════════════════════════════════
phase('Gather')

const ctx = await agent(
  `Gather context for a QA review of PR #${PR} in repo ${REPO} (format owner/name).\n` +
  `Use the gh CLI:\n` +
  `  gh pr view ${PR} --repo ${REPO} --json title,body,headRefName,headRefOid,baseRefOid,files,additions,deletions\n` +
  `  gh pr diff ${PR} --repo ${REPO}   (truncate diff_excerpt to ~15000 chars)\n` +
  `If gh errors / not authenticated / PR not found, set healthy=false and explain in note — do NOT fabricate a diff.\n` +
  `Derive blast_radius from the changed file paths (mirror the heuristic in ${EMITTER_REF} derive_blast_radius if helpful):\n` +
  `  - layers_touched: coarse buckets (e.g. api, domain, ml, ui, ci, docs, schema, governance) inferred from paths\n` +
  `  - one_way_doors_crossed: any touched paths that are schemas/contracts, public API surfaces, migrations, OPTIC-K dims, or Galactic Protocol files (else [])\n` +
  `  - invariants_at_risk: best-effort list (else [])\n` +
  `  - components_reached: the changed file paths (cap 50)\n` +
  `  - estimated_blast_score: 0..1\n` +
  `Return repo as owner/name and pr as a number.`,
  { label: 'gather:pr', phase: 'Gather', schema: GATHER_SCHEMA },
)

if (!ctx || !ctx.healthy) {
  log(`Could not gather PR #${PR} in ${REPO} — aborting WITHOUT writing a verdict (cannot substantiate one).`)
  return { error: 'gather_failed', repo: REPO, pr: PR, note: ctx ? ctx.note : 'no result' }
}
log(`Gathered PR #${PR}: "${ctx.title}" — ${ctx.files.length} files, +${ctx.additions}/-${ctx.deletions}. Dispatching ${PANEL.length} personas.`)

// ════════════════════════════════════════════════════════════════════════════
// PHASE 2 — Persona deliberation (parallel, independent)
// ════════════════════════════════════════════════════════════════════════════
phase('Deliberate')

const reviews = await parallel(
  PANEL.map((member) => () =>
    agent(
      `Adopt the Demerzel persona defined in personas/${member.persona}.persona.yaml — read that file for voice and ` +
      `priorities. Review PR #${PR} (${REPO}) STRICTLY through your lens: ${member.concern}.\n\n` +
      `PR title: ${JSON.stringify(ctx.title)}\n` +
      `PR body:\n${(ctx.body || '').slice(0, 2000)}\n\n` +
      `Changed files: ${JSON.stringify(ctx.files.slice(0, 50))}\n\n` +
      `Unified diff (truncated):\n${(ctx.diff_excerpt || '').slice(0, 15000)}\n\n` +
      `Return YOUR verdict only: block (P0, only for genuine merge-stoppers in your domain), merge_with_followups, or pass. ` +
      `Set risk_tier consistently (block⇒P0). List findings with severity (must_fix/should_fix/nice_to_have/info), a short ` +
      `title, rationale, optional location (file:line), optional proposed_test, and blocks_merge (true only for must-fix ` +
      `stoppers in your concern). If the diff is clean for your lens, return pass with empty findings.`,
      { label: `persona:${member.persona}`, phase: 'Deliberate', schema: PERSONA_SCHEMA },
    ).then((r) => (r ? { ...r, persona: member.persona, role: member.role } : null)),
  ),
)

const panel = reviews.filter(Boolean)
if (panel.length === 0) {
  log('No persona returned a review — aborting without writing a verdict.')
  return { error: 'no_reviews', repo: REPO, pr: PR }
}

// ── Strictest-wins consensus (deterministic, in-script) ───────────────────────
// Governance stance: a must_fix finding blocks the merge BY DEFINITION. We
// coerce blocks_merge=true for must_fix so a reviewer cannot accidentally mark a
// merge-stopper non-blocking. severity and blocks_merge stay independent for the
// lower tiers (should_fix / nice_to_have / info), matching the schema's design.
const followups = []
let fid = 1
for (const r of panel) for (const f of r.findings || []) {
  followups.push({
    id: `tp-${fid++}`,
    severity: f.severity,
    title: f.title,
    rationale: f.rationale,
    location: f.location ?? null,
    proposed_test: f.proposed_test ?? null,
    blocks_merge: f.severity === 'must_fix' ? true : !!f.blocks_merge,
  })
}
const anyBlock = panel.some((r) => r.verdict === 'block') || followups.some((f) => f.blocks_merge)
const anyShouldFix = followups.some((f) => f.severity === 'should_fix')

// block ⇒ P0 (schema-required). merge/pass carry P2 by default; the granular
// risk lives in blast_radius.estimated_blast_score, not the coarse tier.
let verdict, riskTier
if (anyBlock) { verdict = 'block'; riskTier = 'P0' }
else if (anyShouldFix || panel.some((r) => r.verdict === 'merge_with_followups')) { verdict = 'merge_with_followups'; riskTier = 'P2' }
else { verdict = 'pass'; riskTier = 'P2' }

const reviewerChain = panel.map((r) => ({
  agent: r.persona,
  role: r.role,
  score: Number.isFinite(r.score) ? r.score : null,
  notes: r.notes ?? null,
}))
const evidence = panel.map((r) => ({
  kind: 'manual_note',
  name: `${r.persona}:${r.role}`,
  outcome: r.verdict === 'pass' ? 'pass' : r.verdict === 'block' ? 'fail' : 'flaky',
}))

// ════════════════════════════════════════════════════════════════════════════
// PHASE 3 — Assemble + validate against the FROZEN contract + write
// ════════════════════════════════════════════════════════════════════════════
phase('Synthesize')

// Pass the consensus-derived parts; the agent stamps timestamps/verdict_id,
// assembles the full object, validates with jsonschema, and only then writes.
const verdictParts = {
  schema_version: 1,
  producer: 'qa-architect-cycle',
  producer_version: '0.2.0',
  target: { kind: 'pull_request', repo: ctx.repo, ref: String(ctx.pr), sha: ctx.head_sha || null, base_sha: ctx.base_sha || null },
  risk_tier: riskTier,
  verdict,
  blast_radius: ctx.blast_radius,
  evidence,
  followups,
  reviewer_chain: reviewerChain,
  links: { pr: `https://github.com/${ctx.repo}/pull/${ctx.pr}` },
}

const result = await agent(
  `Emit a QA verdict that conforms EXACTLY to the frozen contract at ${SCHEMA_PATH}. Do NOT modify the schema.\n` +
  `1. Read ${SCHEMA_PATH} in full (note: additionalProperties:false everywhere; conditional rules block⇒P0, informational⇒P3; ` +
  `narrative is 1..500 chars).\n` +
  `2. Start from these consensus-derived parts (already strictest-wins aggregated):\n${JSON.stringify(verdictParts)}\n` +
  `3. Add: produced_at = output of \`date -u +%Y-%m-%dT%H:%M:%SZ\`; verdict_id = "<iso8601>-pr-${ctx.pr}-tribunalpanel" ` +
  `(iso with colons replaced by nothing or kept — just keep it sortable and schema-valid); narrative = a <=500 char plain-language ` +
  `summary of the panel outcome (verdict, why, headline followups).\n` +
  `4. Validate the assembled object with python jsonschema:\n` +
  `   python -c "import json,jsonschema,sys; s=json.load(open('${SCHEMA_PATH}')); d=json.load(open('/tmp/verdict.json')); jsonschema.validate(d,s); print('VALID')"\n` +
  `   (write your candidate to /tmp/verdict.json first). If it fails, FIX the object and re-validate. Set valid=true only after VALID prints.\n` +
  (DRY_RUN
    ? `5. DRY RUN: do NOT write to ${VERDICT_ROOT}. Return valid + the would-be path + a summary.`
    : `5. Write the validated object to ${VERDICT_ROOT}/<owner_repo>/${ctx.pr}/<verdict_id>.json where <owner_repo> is ` +
      `the FULL repo with '/' replaced by '_' (e.g. GuitarAlchemist_ga) — matching scripts/qa_tribunal_emit.py so ` +
      `Phase-0 and panel verdicts share one key and */ga repos do not collide. mkdir -p the dir. Return valid=true, the written_path, and a one-line summary.`),
  { label: 'synth:emit-verdict', phase: 'Synthesize', schema: WRITE_SCHEMA },
)

log(`Tribunal verdict: ${verdict} (${riskTier}) from ${panel.length} personas; ${followups.length} followup(s); schema valid=${result ? result.valid : 'unknown'}.`)
return {
  repo: ctx.repo,
  pr: ctx.pr,
  verdict,
  risk_tier: riskTier,
  personas: panel.map((r) => ({ persona: r.persona, verdict: r.verdict })),
  followups: followups.length,
  dry_run: DRY_RUN,
  emitted: result,
}
