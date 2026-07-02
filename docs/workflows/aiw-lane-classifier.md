# AIW Lane Classifier

Related: #463, #465, #467, `docs/workflows/aiw-operating-doctrine.md`.

## Purpose

Classify AIW issues before worker execution so vague work is shaped before implementation.

## Lanes

| Lane | Use when | AFK-ready |
|------|----------|-----------|
| `explore` | Ideas, prototypes, alternatives, demos, discovery. | No |
| `shape` | The issue is broad, vague, or missing acceptance criteria. | No |
| `loop` | The issue is scoped, bounded, testable, and ready for a harnessed worker. | Yes |
| `verify` | Output exists and needs review, evidence, tests, or risk notes. | No |
| `govern` | The issue touches governance, authority, risk, policy, or merge gates. | No |

## Classifier output

```yaml
aiw_classification:
  lane: shape
  source_style:
    - pocock
  risk: low
  afk_eligible: false
  reason: "missing test command and allowed paths"
  next_action: "shape the issue before implementation"
  required_before_loop:
    - allowed_paths
    - non_goals
    - test_command
    - acceptance_criteria
    - budget_cap
    - stop_conditions
```

## Promotion rule

Move an issue to `loop` only when it has:

- narrow scope;
- allowed paths;
- explicit non-goals;
- testable acceptance criteria;
- validation or evidence expectation;
- budget cap;
- stop conditions.

When in doubt, keep the issue in `shape` or `govern`.

## Suggested labels

```yaml
aiw/lane/explore
aiw/lane/shape
aiw/lane/loop
aiw/lane/verify
aiw/lane/govern
aiw/afk-candidate
aiw/needs-shaping
aiw/needs-human
```

## Non-goals

- This classifier does not invoke providers.
- This classifier does not merge PRs.
- This classifier does not replace human governance.
- This classifier does not grant AFK autonomy by itself.
