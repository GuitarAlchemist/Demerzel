# LOLLI Lint Report — 2026-03-23

First comprehensive LOLLI lint across all 28 IxQL pipelines.

## Summary

| Metric | Value |
|--------|-------|
| Files scanned | 28 |
| Total bindings | 256 |
| Dead bindings (actual) | 0 |
| Dead bindings (intentional chaos) | 3 |
| LOLLI score | **0.0%** (excluding chaos-test.ixql) |
| False positives reviewed | 6 (all correctly rejected) |

## Verdict

**System is healthy.** Zero actual dead code across 28 pipelines covering governance, research, optimization, chaos engineering, and examples.

The only LOLLI found was in `pipelines/chaos-test.ixql` — intentional poison for chaos engineering (3 dead bindings: `phantom_state`, `vapor_config`, `useless_metric`). This validates that the detection system can identify dead values when they exist.

## Key Observations

1. **27/28 files clean** — strong execution-first discipline
2. **Side effects clearly marked** — write(), alert(), git operations isolated
3. **Governance gates enforced** — reversibility_check and explanation_requirement prevent accidental LOLLI
4. **Compound phases explicit** — every pipeline documents what is harvested/promoted/taught
5. **Cross-pipeline dependencies healthy** — no orphaned write() targets

## Method

Manual AST-level analysis: tracked all `name <- ...` bindings, verified each name is referenced downstream. Checked fan_out branches for collection. Cross-referenced write() paths against read() paths across all files.

## Next Steps

- Automate this as a GitHub Action (run on every PR)
- Wire into resilience score (LOLLI lint pass = +1 to R)
- Feed results into memristive Markov model as input
