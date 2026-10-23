#!/usr/bin/env python3
"""Tests for scripts/compliance_checks/ — the per-check modules behind
scripts/compliance_report.py.

Three of these classes are regression witnesses rather than unit tests. They pin
the properties that make the split safe:

  ModuleBoundaryTests   one module per individual check, nothing grouped
  ImportIdentityTests   one canonical checks package in package and script mode
  OrderingRegressionTests  the serialized violation order, persona-major, and
                        the integrity hash are byte-identical to the behaviour
                        before run_checks() was split up

The rest are what the split was for: each check exercised on its own, against a
fixture, without mocking glob() across five artifact tiers.
"""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path
from unittest import mock

try:
    from scripts import compliance_report
    from scripts.compliance_checks import (CHECK_MODULES, MIRROR_CHECKS,
                                           PERSONA_CHECKS, MirrorContext,
                                           Persona, build_context, run_checks)
    from scripts.compliance_checks import (belief_staleness,
                                           persona_behavioral_test,
                                           persona_estimator_pairing,
                                           persona_required_fields,
                                           persona_semver, persona_yaml_valid,
                                           policy_semver, schemas_valid_json)
except ModuleNotFoundError:  # `unittest discover -s scripts` imports top-level tests.
    import compliance_report
    from compliance_checks import (CHECK_MODULES, MIRROR_CHECKS, PERSONA_CHECKS,
                                   MirrorContext, Persona, build_context,
                                   run_checks)
    from compliance_checks import (belief_staleness, persona_behavioral_test,
                                   persona_estimator_pairing,
                                   persona_required_fields, persona_semver,
                                   persona_yaml_valid, policy_semver,
                                   schemas_valid_json)

REPO_ROOT = Path(__file__).resolve().parents[1]
FROZEN_NOW = datetime(2026, 8, 23, 19, 34, 11, tzinfo=timezone.utc)
YAML_ERROR_PREFIX = "persona a-broken.persona.yaml is not valid YAML:"


def build_fixture_mirror(root: Path, include_malformed_persona: bool = True) -> Path:
    """Create a governance mirror under ``root`` that produces violations from
    every check, with several personas each carrying several simultaneous
    violations. ``include_malformed_persona`` is off for the integrity-hash
    witness, whose input has to be byte-stable: the YAML parser's error text is
    not part of this repo's contract and may differ between pyyaml releases."""
    mirror = Path(root) / "governance" / "demerzel"
    personas = mirror / "personas"
    behavioral = mirror / "tests" / "behavioral"
    policies = mirror / "policies"
    schemas = mirror / "schemas"
    beliefs = mirror / "state" / "beliefs"
    for d in (personas, behavioral, policies, schemas, beliefs):
        d.mkdir(parents=True, exist_ok=True)

    # a-broken: front-matter is not valid YAML -> YAML violation, and (because it
    # parses to {}) every persona check fires as well.
    if include_malformed_persona:
        (personas / "a-broken.persona.yaml").write_text(
            "name: [unclosed\nversion: 1.0.0\n", encoding="utf-8")

    # b-alpha: missing required fields incl. constraints (high), no behavioral
    # test, non-semver version, no estimator_pairing and no waiver. Four at once.
    (personas / "b-alpha.persona.yaml").write_text(
        "name: b-alpha\nversion: '1.0'\ndescription: alpha\nrole: tester\n",
        encoding="utf-8")

    # c-beta: missing non-critical fields (medium), has a behavioral test,
    # non-semver version, estimator_pairing that names an unknown persona.
    (personas / "c-beta.persona.yaml").write_text(
        "name: c-beta\nversion: notasemver\ndescription: beta\nrole: tester\n"
        "capabilities: [a]\nconstraints: [b]\nvoice: dry\n"
        "estimator_pairing: ghost-persona\n",
        encoding="utf-8")

    # d-gamma: fully conformant -> contributes no violations.
    (personas / "d-gamma.persona.yaml").write_text(
        "name: d-gamma\nversion: 2.1.3\ndescription: gamma\nrole: tester\n"
        "capabilities: [a]\nconstraints: [b]\nvoice: dry\naffordances: [c]\n"
        "goal_directedness: high\nestimator_pairing: c-beta\n",
        encoding="utf-8")

    # e-waived: no estimator_pairing, but the body documents an explicit waiver.
    (personas / "e-waived.persona.yaml").write_text(
        "name: e-waived\nversion: 1.0.0\ndescription: waived\nrole: tester\n"
        "capabilities: [a]\nconstraints: [b]\nvoice: dry\n"
        "---\n\nThis persona has no estimator_pairing: it is the neutral estimator.\n",
        encoding="utf-8")

    (behavioral / "c-beta-cases.md").write_text("# c-beta\n", encoding="utf-8")
    (behavioral / "d-gamma-cases.md").write_text("# d-gamma\n", encoding="utf-8")
    (behavioral / "e-waived-cases.md").write_text("# e-waived\n", encoding="utf-8")

    (policies / "p-bad.yaml").write_text("version: '1.0'\n", encoding="utf-8")
    (policies / "p-good.yaml").write_text("version: 1.0.0\n", encoding="utf-8")
    (policies / "p-prose.yaml").write_text("version: [unclosed\n", encoding="utf-8")

    (schemas / "bad.schema.json").write_text("{not json", encoding="utf-8")
    (schemas / "good.schema.json").write_text('{"type": "object"}', encoding="utf-8")

    (beliefs / "old-one.belief.json").write_text(
        '{"last_updated": "2020-01-01T00:00:00Z"}', encoding="utf-8")
    (beliefs / "old-two.belief.json").write_text(
        '{"last_updated": "2020-02-01T00:00:00Z"}', encoding="utf-8")
    fresh = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    (beliefs / "fresh.belief.json").write_text(
        '{"last_updated": "%s"}' % fresh, encoding="utf-8")
    return mirror


def _normalize(violations):
    """(article, description, severity) triples, with the pyyaml error text
    trimmed off the one description that carries it."""
    out = []
    for v in violations:
        desc = v["description"]
        if desc.startswith(YAML_ERROR_PREFIX):
            desc = YAML_ERROR_PREFIX
        out.append((v["article"], desc, v["severity"]))
    return out


def _persona(tmp: Path, filename: str, text: str) -> Persona:
    path = tmp / filename
    path.write_text(text, encoding="utf-8")
    return persona_yaml_valid.load_persona(path)[0]


class ModuleBoundaryTests(unittest.TestCase):
    """Blocker 1: one module per individual check. Grouping the four persona
    checks into a single personas.py is what this test exists to prevent."""

    EXPECTED_CHECKS = {
        "persona-yaml-valid", "P1-persona-required-fields",
        "P2-behavioral-test-coverage", "P3-persona-semver",
        "P4-estimator-pairing", "policy-semver", "schemas-valid-json",
        "belief-staleness",
    }

    def test_every_check_is_registered(self):
        self.assertEqual(set(CHECK_MODULES), self.EXPECTED_CHECKS)

    def test_no_module_owns_more_than_one_check(self):
        owners = [mod.__name__ for mod in CHECK_MODULES.values()]
        self.assertEqual(len(owners), len(set(owners)),
                         f"a module implements more than one check: {owners}")

    def test_every_module_in_the_package_is_a_registered_check(self):
        pkg_dir = Path(CHECK_MODULES["belief-staleness"].__file__).parent
        modules = {p.stem for p in pkg_dir.glob("*.py")} - {"__init__", "_common"}
        registered = {mod.__name__.rsplit(".", 1)[-1] for mod in CHECK_MODULES.values()}
        self.assertEqual(modules, registered)

    def test_registries_partition_the_checks(self):
        persona = [n for n, _ in PERSONA_CHECKS]
        mirror = [n for n, _ in MIRROR_CHECKS]
        self.assertEqual(persona, ["P1-persona-required-fields",
                                   "P2-behavioral-test-coverage",
                                   "P3-persona-semver", "P4-estimator-pairing"])
        self.assertEqual(mirror, ["policy-semver", "schemas-valid-json",
                                  "belief-staleness"])
        self.assertEqual(set(persona) | set(mirror) | {"persona-yaml-valid"},
                         self.EXPECTED_CHECKS)


class ImportIdentityTests(unittest.TestCase):
    """Blocker 2: the checks package has one canonical identity, whichever way
    compliance_report is reached."""

    def test_package_import_uses_the_package_relative_checks(self):
        probe = (
            "import sys, scripts.compliance_report as m; "
            "print(('compliance_checks' in sys.modules,"
            " 'scripts.compliance_checks' in sys.modules,"
            " m.run_checks.__module__))"
        )
        r = subprocess.run([sys.executable, "-c", probe], cwd=REPO_ROOT,
                           capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertEqual(
            r.stdout.strip(),
            "(False, True, 'scripts.compliance_checks')",
            "importing scripts.compliance_report must bind scripts.compliance_checks "
            "and must not also create a top-level compliance_checks module")

    def test_direct_script_execution_works(self):
        with tempfile.TemporaryDirectory() as root:
            build_fixture_mirror(Path(root) / "ix")
            r = subprocess.run(
                [sys.executable, "scripts/compliance_report.py", "--repo", "ix",
                 "--repos-root", root, "--dry-run"],
                cwd=REPO_ROOT, capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stderr)
        doc = json.loads(r.stdout)
        self.assertEqual(doc["overall_status"], "non-compliant")
        self.assertEqual(len(doc["violations"]), 16)

    def test_report_reexports_the_package_implementation(self):
        self.assertIs(compliance_report.run_checks, run_checks)


class OrderingRegressionTests(unittest.TestCase):
    """Blocker 3: reports are hashed over their serialized form, so the order
    violations are emitted in is contract, not cosmetics. These goldens were
    captured from the pre-split run_checks()."""

    GOLDEN_ORDER = [
        ('Article 7 - Auditability',
         'persona a-broken.persona.yaml is not valid YAML:',
         'high'),
        ('persona-requirements',
         "persona 'a-broken.persona' missing fields: ['name', 'version', 'description', 'role', 'capabilities', 'constraints', 'voice', 'affordances', 'goal_directedness']",
         'high'),
        ('contributing-rules',
         "persona 'a-broken.persona' has no behavioral test",
         'high'),
        ('Article 7 - Auditability',
         "persona 'a-broken.persona' version None is not semver",
         'low'),
        ('persona-requirements',
         "persona 'a-broken.persona' has no estimator_pairing",
         'high'),
        ('persona-requirements',
         "persona 'b-alpha' missing fields: ['capabilities', 'constraints', 'voice', 'affordances', 'goal_directedness']",
         'high'),
        ('contributing-rules',
         "persona 'b-alpha' has no behavioral test",
         'high'),
        ('Article 7 - Auditability',
         "persona 'b-alpha' version '1.0' is not semver",
         'low'),
        ('persona-requirements',
         "persona 'b-alpha' has no estimator_pairing",
         'high'),
        ('persona-requirements',
         "persona 'c-beta' missing fields: ['affordances', 'goal_directedness']",
         'medium'),
        ('Article 7 - Auditability',
         "persona 'c-beta' version 'notasemver' is not semver",
         'low'),
        ('persona-requirements',
         "persona 'c-beta' estimator_pairing 'ghost-persona' is not a known persona",
         'medium'),
        ('persona-requirements',
         "persona 'e-waived' missing fields: ['affordances', 'goal_directedness']",
         'medium'),
        ('Article 7 - Auditability',
         "policy p-bad.yaml version '1.0' is not semver",
         'low'),
        ('Article 7 - Auditability',
         'schema bad.schema.json is not valid JSON',
         'critical'),
        ('Article 8 - Observability',
         '2/3 beliefs are stale (> 7d since last_updated)',
         'medium'),
    ]
    GOLDEN_CHECKED_KEYS = ["personas", "behavioral_tests", "policies",
                           "schemas", "beliefs"]
    GOLDEN_CHECKED = {"personas": 5, "behavioral_tests": 3, "policies": 3,
                      "schemas": 2, "beliefs": 3}
    GOLDEN_CONTENT_HASH = ("278174ddafdd2d774ee238725be65652"
                           "c30cfa2de835810e7b5442f1346a0ae2")

    def _run(self, **kwargs):
        with tempfile.TemporaryDirectory() as root:
            mirror = build_fixture_mirror(Path(root) / "ix", **kwargs)
            return run_checks(mirror)

    def test_violation_order_is_unchanged(self):
        self.assertEqual(_normalize(self._run()["violations"]), self.GOLDEN_ORDER)

    def test_checked_counts_and_key_order_are_unchanged(self):
        checked = self._run()["checked"]
        self.assertEqual(list(checked), self.GOLDEN_CHECKED_KEYS)
        self.assertEqual(checked, self.GOLDEN_CHECKED)

    def test_persona_violations_stay_persona_major(self):
        """All of one persona's violations, then all of the next persona's —
        not all P1s, then all P2s."""
        descriptions = [v["description"] for v in self._run()["violations"]]
        subjects = [d.split("'")[1] for d in descriptions if d.startswith("persona '")]
        self.assertEqual(subjects, [
            "a-broken.persona", "a-broken.persona", "a-broken.persona",
            "a-broken.persona",
            "b-alpha", "b-alpha", "b-alpha", "b-alpha",
            "c-beta", "c-beta", "c-beta",
            "e-waived",
        ])

    def test_integrity_hash_is_unchanged(self):
        result = self._run(include_malformed_persona=False)
        with mock.patch.object(compliance_report, "_now", return_value=FROZEN_NOW):
            doc = compliance_report._attach_integrity(
                compliance_report.build_report("ix", result, 30), "ix")
        self.assertEqual(doc["content_hash"], self.GOLDEN_CONTENT_HASH)
        self.assertEqual(doc["hash_algorithm"], "sha256")
        self.assertEqual(doc["overall_status"], "non-compliant")

    def test_run_checks_is_deterministic(self):
        with tempfile.TemporaryDirectory() as root:
            mirror = build_fixture_mirror(Path(root) / "ix",
                                          include_malformed_persona=False)
            first, second = run_checks(mirror), run_checks(mirror)
        blob = lambda r: json.dumps(r, sort_keys=True, separators=(",", ":"))  # noqa: E731
        self.assertEqual(blob(first), blob(second))
        self.assertEqual(hashlib.sha256(blob(first).encode()).hexdigest(),
                         hashlib.sha256(blob(second).encode()).hexdigest())


class _CheckTestCase(unittest.TestCase):
    """Each check runs against a real directory, but only the tier it reads has
    to exist — that is what splitting run_checks() bought."""

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self._tmp.cleanup)
        self.tmp = Path(self._tmp.name)

    def ctx(self, **kwargs) -> MirrorContext:
        return MirrorContext(mirror=self.tmp, **kwargs)

    def write(self, relative: str, text: str) -> Path:
        path = self.tmp / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        return path


class PersonaYamlValidTests(_CheckTestCase):
    def test_valid_front_matter_produces_no_violation(self):
        persona, violations = persona_yaml_valid.load_persona(
            self.write("ok.persona.yaml", "name: ok\nversion: 1.0.0\n"))
        self.assertEqual(violations, [])
        self.assertEqual(persona.name, "ok")
        self.assertEqual(persona.data["version"], "1.0.0")

    def test_malformed_front_matter_is_a_high_violation_with_empty_data(self):
        persona, violations = persona_yaml_valid.load_persona(
            self.write("bad.persona.yaml", "name: [unclosed\n"))
        self.assertEqual(len(violations), 1)
        self.assertEqual(violations[0]["severity"], "high")
        self.assertEqual(violations[0]["article"], "Article 7 - Auditability")
        self.assertTrue(violations[0]["description"].startswith(
            "persona bad.persona.yaml is not valid YAML: "))
        self.assertEqual(persona.data, {})
        self.assertEqual(persona.name, "bad.persona", "name falls back to the stem")

    def test_markdown_body_after_the_separator_is_not_parsed(self):
        persona, violations = persona_yaml_valid.load_persona(self.write(
            "hybrid.persona.yaml", "name: hybrid\n---\n# Notes\n`not: yaml: at all`\n"))
        self.assertEqual(violations, [])
        self.assertEqual(persona.data, {"name": "hybrid"})

    def test_load_personas_returns_sorted_file_order(self):
        for name in ("z", "a", "m"):
            self.write(f"personas/{name}.persona.yaml", f"name: {name}\n")
        personas, violations = persona_yaml_valid.load_personas(self.tmp)
        self.assertEqual([p.name for p in personas], ["a", "m", "z"])
        self.assertEqual(violations, [])


class PersonaRequiredFieldsTests(_CheckTestCase):
    COMPLETE = ("name: p\nversion: 1.0.0\ndescription: d\nrole: r\n"
                "capabilities: [a]\nconstraints: [b]\nvoice: v\naffordances: [c]\n"
                "goal_directedness: high\n")

    def test_complete_persona_has_no_violation(self):
        persona = _persona(self.tmp, "p.persona.yaml", self.COMPLETE)
        self.assertEqual(persona_required_fields.check(persona, self.ctx()), [])

    def test_missing_constraints_is_high(self):
        text = self.COMPLETE.replace("constraints: [b]\n", "")
        persona = _persona(self.tmp, "p.persona.yaml", text)
        [v] = persona_required_fields.check(persona, self.ctx())
        self.assertEqual(v["severity"], "high")
        self.assertEqual(v["article"], "persona-requirements")
        self.assertIn("missing fields: ['constraints']", v["description"])

    def test_missing_non_critical_field_is_medium(self):
        text = self.COMPLETE.replace("affordances: [c]\n", "")
        persona = _persona(self.tmp, "p.persona.yaml", text)
        [v] = persona_required_fields.check(persona, self.ctx())
        self.assertEqual(v["severity"], "medium")

    def test_empty_values_count_as_missing(self):
        text = self.COMPLETE.replace("capabilities: [a]\n", "capabilities: []\n")
        persona = _persona(self.tmp, "p.persona.yaml", text)
        [v] = persona_required_fields.check(persona, self.ctx())
        self.assertIn("'capabilities'", v["description"])

    def test_estimator_pairing_is_not_reported_here(self):
        """It has a waiver rule of its own, so P4 owns it."""
        persona = _persona(self.tmp, "p.persona.yaml", self.COMPLETE)
        self.assertNotIn("estimator_pairing", persona.data)
        self.assertEqual(persona_required_fields.check(persona, self.ctx()), [])


class PersonaBehavioralTestTests(_CheckTestCase):
    def test_uncovered_persona_is_high(self):
        persona = _persona(self.tmp, "p.persona.yaml", "name: lonely\n")
        [v] = persona_behavioral_test.check(persona, self.ctx(test_blob="other-cases"))
        self.assertEqual(v["severity"], "high")
        self.assertEqual(v["article"], "contributing-rules")
        self.assertEqual(v["description"], "persona 'lonely' has no behavioral test")

    def test_substring_match_counts_as_coverage(self):
        persona = _persona(self.tmp, "p.persona.yaml", "name: covered\n")
        ctx = self.ctx(test_blob="covered-cases other-cases")
        self.assertEqual(persona_behavioral_test.check(persona, ctx), [])

    def test_load_test_blob_joins_stems_and_counts(self):
        self.write("tests/behavioral/one-cases.md", "x")
        self.write("tests/behavioral/two-cases.md", "x")
        self.write("tests/behavioral/ignored.txt", "x")
        blob, count = persona_behavioral_test.load_test_blob(self.tmp)
        self.assertEqual(count, 2)
        self.assertEqual(sorted(blob.split()), ["one-cases", "two-cases"])

    def test_missing_directory_yields_empty_blob(self):
        self.assertEqual(persona_behavioral_test.load_test_blob(self.tmp), ("", 0))


class PersonaSemverTests(_CheckTestCase):
    def _check(self, version_line: str):
        persona = _persona(self.tmp, "p.persona.yaml", "name: p\n" + version_line)
        return persona_semver.check(persona, self.ctx())

    def test_three_numeric_parts_pass(self):
        self.assertEqual(self._check("version: '1.0.0'\n"), [])
        self.assertEqual(self._check("version: '10.20.30'\n"), [])

    def test_two_parts_fail_as_low(self):
        [v] = self._check("version: '1.0'\n")
        self.assertEqual(v["severity"], "low")
        self.assertEqual(v["article"], "Article 7 - Auditability")
        self.assertEqual(v["description"], "persona 'p' version '1.0' is not semver")

    def test_non_string_versions_fail(self):
        self.assertEqual(len(self._check("version: 1.0\n")), 1)
        self.assertEqual(len(self._check("")), 1)


class PersonaEstimatorPairingTests(_CheckTestCase):
    def test_missing_pairing_without_waiver_is_high(self):
        persona = _persona(self.tmp, "p.persona.yaml", "name: p\n")
        [v] = persona_estimator_pairing.check(persona, self.ctx())
        self.assertEqual(v["severity"], "high")
        self.assertEqual(v["description"], "persona 'p' has no estimator_pairing")

    def test_documented_waiver_suppresses_the_violation(self):
        for phrase in persona_estimator_pairing.WAIVER_PHRASES:
            with self.subTest(phrase=phrase):
                persona = _persona(self.tmp, "p.persona.yaml",
                                   "name: p\n---\n\nThis one " + phrase.upper() + " here.\n")
                self.assertEqual(persona_estimator_pairing.check(persona, self.ctx()), [])

    def test_unknown_estimator_is_medium(self):
        persona = _persona(self.tmp, "p.persona.yaml",
                           "name: p\nestimator_pairing: ghost\n")
        [v] = persona_estimator_pairing.check(
            persona, self.ctx(persona_names=frozenset({"p", "other"})))
        self.assertEqual(v["severity"], "medium")
        self.assertIn("estimator_pairing 'ghost' is not a known persona", v["description"])

    def test_known_estimator_passes(self):
        persona = _persona(self.tmp, "p.persona.yaml",
                           "name: p\nestimator_pairing: other\n")
        ctx = self.ctx(persona_names=frozenset({"p", "other"}))
        self.assertEqual(persona_estimator_pairing.check(persona, ctx), [])

    def test_mapping_form_resolves_via_persona_then_name(self):
        for key in ("persona", "name"):
            with self.subTest(key=key):
                persona = _persona(self.tmp, "p.persona.yaml",
                                   "name: p\nestimator_pairing:\n  " + key + ": other\n")
                ctx = self.ctx(persona_names=frozenset({"p", "other"}))
                self.assertEqual(persona_estimator_pairing.check(persona, ctx), [])


class PolicySemverTests(_CheckTestCase):
    def test_bad_version_is_low(self):
        self.write("policies/p.yaml", "version: '1.0'\n")
        outcome = policy_semver.check(self.ctx())
        [v] = outcome.violations
        self.assertEqual(v["severity"], "low")
        self.assertEqual(v["description"], "policy p.yaml version '1.0' is not semver")
        self.assertEqual(outcome.counts, {"policies": 1})

    def test_good_and_versionless_policies_pass(self):
        self.write("policies/good.yaml", "version: 1.0.0\n")
        self.write("policies/none.yaml", "title: no version here\n")
        self.assertEqual(policy_semver.check(self.ctx()).violations, [])

    def test_unparseable_policy_is_skipped_not_reported(self):
        """Policies here are prose-rich human docs; the framework's own audit
        does not require them to be strict YAML."""
        self.write("policies/prose.yaml", "version: [unclosed\n")
        outcome = policy_semver.check(self.ctx())
        self.assertEqual(outcome.violations, [])
        self.assertEqual(outcome.counts, {"policies": 1})


class SchemasValidJsonTests(_CheckTestCase):
    def test_invalid_json_is_critical(self):
        self.write("schemas/bad.schema.json", "{nope")
        outcome = schemas_valid_json.check(self.ctx())
        [v] = outcome.violations
        self.assertEqual(v["severity"], "critical")
        self.assertEqual(v["description"], "schema bad.schema.json is not valid JSON")
        self.assertEqual(outcome.counts, {"schemas": 1})

    def test_valid_json_passes_and_is_counted(self):
        self.write("schemas/a.schema.json", '{"a": 1}')
        self.write("schemas/b.schema.json", "[]")
        outcome = schemas_valid_json.check(self.ctx())
        self.assertEqual(outcome.violations, [])
        self.assertEqual(outcome.counts, {"schemas": 2})

    def test_missing_directory_yields_zero(self):
        outcome = schemas_valid_json.check(MirrorContext(mirror=self.tmp / "nope"))
        self.assertEqual(outcome.violations, [])
        self.assertEqual(outcome.counts, {"schemas": 0})


class BeliefStalenessTests(_CheckTestCase):
    def _belief(self, name: str, age_days=None, raw=None):
        if raw is None:
            ts = datetime.now(timezone.utc) - timedelta(days=age_days)
            raw = json.dumps({"last_updated": ts.strftime("%Y-%m-%dT%H:%M:%SZ")})
        self.write("state/beliefs/" + name, raw)

    def test_stale_beliefs_collapse_into_one_medium_violation(self):
        self._belief("a.belief.json", age_days=30)
        self._belief("b.belief.json", age_days=400)
        self._belief("c.belief.json", age_days=1)
        outcome = belief_staleness.check(self.ctx())
        [v] = outcome.violations
        self.assertEqual(v["severity"], "medium")
        self.assertEqual(v["article"], "Article 8 - Observability")
        self.assertEqual(v["description"],
                         "2/3 beliefs are stale (> 7d since last_updated)")
        self.assertEqual(outcome.counts, {"beliefs": 3})

    def test_boundary_is_strictly_greater_than_stale_days(self):
        self._belief("edge.belief.json", age_days=belief_staleness.STALE_DAYS)
        self.assertEqual(belief_staleness.check(self.ctx()).violations, [])

    def test_corrupt_or_undated_beliefs_are_skipped_but_counted(self):
        self._belief("bad.belief.json", raw="{not json")
        self._belief("undated.belief.json", raw="{}")
        self._belief("weird.belief.json", raw='{"last_updated": "never"}')
        outcome = belief_staleness.check(self.ctx())
        self.assertEqual(outcome.violations, [])
        self.assertEqual(outcome.counts, {"beliefs": 3})

    def test_parse_ts_rejects_non_strings_and_garbage(self):
        self.assertIsNone(belief_staleness.parse_ts(None))
        self.assertIsNone(belief_staleness.parse_ts(17))
        self.assertIsNone(belief_staleness.parse_ts("not-a-date"))
        self.assertIsNotNone(belief_staleness.parse_ts("2026-01-01T00:00:00Z"))


class BuildContextTests(_CheckTestCase):
    def test_context_carries_declared_names_including_none(self):
        with tempfile.TemporaryDirectory() as root:
            mirror = build_fixture_mirror(Path(root) / "ix")
            ctx, violations, counts = build_context(mirror)
        self.assertEqual(counts, {"personas": 5, "behavioral_tests": 3})
        self.assertEqual(len(violations), 1, "only the malformed persona")
        self.assertEqual([p.name for p in ctx.personas],
                         ["a-broken.persona", "b-alpha", "c-beta", "d-gamma",
                          "e-waived"])
        self.assertIn(None, ctx.persona_names,
                      "an unnamed persona must not become a pairable target")
        self.assertEqual(ctx.persona_names,
                         frozenset({None, "b-alpha", "c-beta", "d-gamma", "e-waived"}))


if __name__ == "__main__":
    unittest.main()
