"""Guard: every schema in schemas/ must declare a *resolvable* $schema metaschema.

Draft-07's registered identifier is `http://json-schema.org/draft-07/schema#`.
The `https://` variant does not resolve: jsonschema silently falls back to the
latest draft (2020-12) and validates the schema under semantics it never
declared, emitting only a warning. Seventeen schemas shipped with the `https`
form (issue #792); this test asserts the class cannot regress.

The check is deliberately about *resolvability*, not a hard-coded string: any
$schema jsonschema cannot map to a concrete validator is a failure, so the
guard also covers future metaschema typos, not just this one.
"""

import glob
import json
import os
import unittest
import warnings

_REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_SCHEMA_GLOB = os.path.join(_REPO_ROOT, "schemas", "*.json")


class SchemaMetaschemaResolves(unittest.TestCase):
    def test_every_schema_declares_a_resolvable_metaschema(self):
        try:
            from jsonschema.validators import validator_for
        except ModuleNotFoundError:
            self.skipTest("jsonschema not installed")

        offenders = []
        for path in sorted(glob.glob(_SCHEMA_GLOB)):
            with open(path, encoding="utf-8") as handle:
                schema = json.load(handle)
            declared = schema.get("$schema")
            if not declared:
                continue
            # validator_for warns and falls back to the latest draft when it
            # cannot resolve the declared metaschema. Turn that warning into the
            # signal: a schema whose $schema does not resolve is the defect.
            with warnings.catch_warnings(record=True) as caught:
                warnings.simplefilter("always")
                validator_for(schema)
                if any("metaschema" in str(w.message).lower() for w in caught):
                    offenders.append(
                        (os.path.relpath(path, _REPO_ROOT), declared)
                    )

        self.assertEqual(
            offenders,
            [],
            "these schemas declare an unresolvable $schema (jsonschema falls back "
            "to the latest draft and validates under undeclared semantics):\n"
            + "\n".join(f"  {rel}: {uri}" for rel, uri in offenders),
        )


if __name__ == "__main__":
    unittest.main()
