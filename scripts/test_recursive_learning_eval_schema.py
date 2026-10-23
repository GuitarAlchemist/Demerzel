"""Executable guardrails for policy:recursive-learning-eval.

The policy declares two constitutional boundaries and states that both are
enforced by schema validation:

  * `recursion.depth_tracking.enforcement` — "Schema validation rejects
    artifacts with recursion_depth > 2"
  * `article_4_guardrails.enforcement` — `article_4_check` valid_values
    `["understanding"]`, "goal changes rejected at schema level"

Until `schemas/recursive-learning-eval.schema.json` existed, neither was
enforced anywhere, and the policy's own behavioral tests rle-bt-004 and
rle-bt-005 were carried in the YAML pre-graded `tetravalent_grade: T` with
nothing executing them. These are those two tests, made real, plus the
degenerate-denominator cases the meta-metric formulas hit on a first cycle.

Runs under `python -m unittest discover -s scripts` (governance-validate.yml).
Skips rather than passes vacuously when jsonschema is absent — `demerzel_kit.
validate` degrades to a warning in a stdlib-only environment, which would turn
every "must be rejected" assertion into a false pass.
"""

import unittest

import demerzel_kit

try:
    import jsonschema

    HAS_JSONSCHEMA = True
except ImportError:  # pragma: no cover - environment-dependent
    HAS_JSONSCHEMA = False

SCHEMA = "recursive-learning-eval"


def proposal(**overrides):
    """A minimal Article-4-compliant proposal; override one field per test."""
    base = {
        "id": "rle-2026-07-001",
        "failure_pattern": "pattern_graveyard",
        "proposed_change": "Add a 14-day validation reminder for patterns stuck at U.",
        "affected_agent": "continuous-learning-pipeline",
        "expected_impact": "meta_false_positive_rate down; pattern_graveyard cleared",
        "effort": "low",
        "requires_authorization": True,
        "article_4_check": "understanding",
    }
    base.update(overrides)
    return base


def artifact(**overrides):
    base = {
        "schema": SCHEMA,
        "kind": "eval-proposals",
        "period": "2026-07",
        "recursion_depth": 1,
        "proposals": [proposal()],
    }
    base.update(overrides)
    return base


@unittest.skipUnless(HAS_JSONSCHEMA, "jsonschema not installed")
class RecursionDepthBound(unittest.TestCase):
    """rle-bt-004 — recursive depth limit enforced."""

    def test_depths_0_through_2_are_accepted(self):
        for depth in (0, 1, 2):
            with self.subTest(depth=depth):
                demerzel_kit.validate(artifact(recursion_depth=depth), SCHEMA)

    def test_depth_3_is_rejected(self):
        # "Evaluating the evaluation of the evaluation is explicitly
        # prohibited." The fix for a depth-2 finding is to simplify depth-1.
        with self.assertRaises(jsonschema.ValidationError):
            demerzel_kit.validate(artifact(recursion_depth=3), SCHEMA)

    def test_negative_depth_is_rejected(self):
        with self.assertRaises(jsonschema.ValidationError):
            demerzel_kit.validate(artifact(recursion_depth=-1), SCHEMA)

    def test_meta_eval_must_be_depth_2(self):
        demerzel_kit.validate(
            artifact(kind="meta-eval", period="2026-Q3", recursion_depth=2, proposals=[]),
            SCHEMA,
        )
        with self.assertRaises(jsonschema.ValidationError):
            demerzel_kit.validate(
                artifact(kind="meta-eval", period="2026-Q3", recursion_depth=1),
                SCHEMA,
            )


@unittest.skipUnless(HAS_JSONSCHEMA, "jsonschema not installed")
class Article4Boundary(unittest.TestCase):
    """rle-bt-005 — Article 4 guardrail blocks goal modification.

    Asimov Article 4: "Knowledge acquisition is always permitted; goal
    acquisition requires authorization."
    """

    def test_understanding_is_accepted(self):
        demerzel_kit.validate(artifact(), SCHEMA)

    def test_goal_modification_is_unrepresentable(self):
        # The policy's own rle-bt-005 scenario: a proposal to "prioritize music
        # theory learning over governance learning" is goal acquisition. There
        # is no enum value that admits it.
        for value in ("goal_modification", "goals", "goal", "both", ""):
            with self.subTest(article_4_check=value):
                with self.assertRaises(jsonschema.ValidationError):
                    demerzel_kit.validate(
                        artifact(proposals=[proposal(article_4_check=value)]), SCHEMA
                    )

    def test_article_4_check_cannot_be_omitted(self):
        bare = proposal()
        del bare["article_4_check"]
        with self.assertRaises(jsonschema.ValidationError):
            demerzel_kit.validate(artifact(proposals=[bare]), SCHEMA)

    def test_authorization_cannot_be_downgraded(self):
        # Article 9 — Bounded Autonomy. A proposal never self-grants a licence
        # to act, so `false` is not representable either.
        with self.assertRaises(jsonschema.ValidationError):
            demerzel_kit.validate(
                artifact(proposals=[proposal(requires_authorization=False)]), SCHEMA
            )

    def test_proposals_are_required_for_the_proposals_artifact(self):
        bare = artifact()
        del bare["proposals"]
        with self.assertRaises(jsonschema.ValidationError):
            demerzel_kit.validate(bare, SCHEMA)


@unittest.skipUnless(HAS_JSONSCHEMA, "jsonschema not installed")
class DegenerateMetricDenominators(unittest.TestCase):
    """A first cycle has no prior cycle, and effectiveness ratios are 0/0 until
    a proposal is authorized and enacted. null must be representable and
    distinguishable from a healthy 0."""

    def test_null_metrics_are_accepted_with_a_reason(self):
        demerzel_kit.validate(
            artifact(
                kind="eval-report",
                proposals=[],
                meta_metrics={
                    "learning_acceleration": None,
                    "meta_false_positive_rate": None,
                    "undefined_reason": "first cycle: no prior cycle; zero proposals enacted",
                },
            ),
            SCHEMA,
        )

    def test_rates_outside_the_unit_interval_are_rejected(self):
        with self.assertRaises(jsonschema.ValidationError):
            demerzel_kit.validate(
                artifact(
                    kind="eval-report",
                    proposals=[],
                    meta_metrics={"meta_false_positive_rate": 1.4},
                ),
                SCHEMA,
            )


@unittest.skipUnless(HAS_JSONSCHEMA, "jsonschema not installed")
class Envelope(unittest.TestCase):
    def test_unknown_top_level_field_is_rejected(self):
        with self.assertRaises(jsonschema.ValidationError):
            demerzel_kit.validate(artifact(recursion_depth_override=9), SCHEMA)

    def test_period_shape_is_enforced(self):
        for bad in ("2026-13", "2026", "July 2026", "2026-Q5"):
            with self.subTest(period=bad):
                with self.assertRaises(jsonschema.ValidationError):
                    demerzel_kit.validate(artifact(period=bad), SCHEMA)


if __name__ == "__main__":
    unittest.main()
