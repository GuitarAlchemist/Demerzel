#!/usr/bin/env python3
"""Read-only contract checks for Gaia's portable continuity receipt."""

from __future__ import annotations

import hashlib
import json
import unittest
from pathlib import Path

import jsonschema


REPO_ROOT = Path(__file__).resolve().parents[1]
CONTRACT_DIR = REPO_ROOT / "schemas" / "contracts"
FIXTURE_DIR = REPO_ROOT / "fixtures" / "contracts"
SCHEMA_PATH = CONTRACT_DIR / "continuity.successor-transition-receipt.schema.json"
VALID_PATH = FIXTURE_DIR / "continuity.successor-transition-receipt.valid.json"
INVALID_PATHS = (
    FIXTURE_DIR / "continuity.successor-transition-receipt.invalid-authority.json",
    FIXTURE_DIR
    / "continuity.successor-transition-receipt.invalid-missing-consumption.json",
)
DOMAIN = b"continuity.successor-transition-receipt/1"

# SHA-256 pins calculated from the Gaia source contract and fixture bytes.
SOURCE_SHA256 = {
    "continuity.successor-transition-receipt.schema.json": (
        "7ceff2a6ee726aa25575361bc46345c6ff4b42db41abda1c3211e92fe123c00f"
    ),
    "continuity.successor-transition-receipt.valid.json": (
        "0f07ce0a6d7749a7aaa0efc587ce7c5cfb0b6c9d7bfc1b8609ab00492a328d1c"
    ),
    "continuity.successor-transition-receipt.invalid-authority.json": (
        "95accc551dd16cb9d7b961bf00d8fe2ae6997157cbaf2e324a8f36dc7dba51a9"
    ),
    "continuity.successor-transition-receipt.invalid-missing-consumption.json": (
        "60cc78d5bd879e782a94b0af601c3bd29471f0281bf4da1a1a76cef9b364a53e"
    ),
}


def _canonical_string(value: str) -> str:
    encoded: list[str] = ['"']
    for character in value:
        codepoint = ord(character)
        if character == '"':
            encoded.append('\\"')
        elif character == "\\":
            encoded.append("\\\\")
        elif codepoint < 0x20:
            encoded.append(f"\\u{codepoint:04x}")
        elif codepoint <= 0x7E:
            encoded.append(character)
        else:
            raise ValueError("canonical receipt strings must be ASCII")
    encoded.append('"')
    return "".join(encoded)


def canonical_bytes(value: object) -> bytes:
    """Encode the receipt contract's closed canonical JSON subset."""
    if value is None:
        text = "null"
    elif value is True:
        text = "true"
    elif value is False:
        text = "false"
    elif isinstance(value, int) and value >= 0:
        text = str(value)
    elif isinstance(value, str):
        text = _canonical_string(value)
    elif isinstance(value, list):
        text = "[" + ",".join(canonical_bytes(item).decode("ascii") for item in value) + "]"
    elif isinstance(value, dict):
        keys = sorted(value, key=lambda key: key.encode("ascii"))
        text = "{" + ",".join(
            f"{_canonical_string(key)}:{canonical_bytes(value[key]).decode('ascii')}"
            for key in keys
        ) + "}"
    else:
        raise ValueError(f"value is outside the canonical receipt subset: {value!r}")
    return text.encode("ascii")


class ContinuitySuccessorContractTests(unittest.TestCase):
    def setUp(self) -> None:
        self.schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
        self.validator = jsonschema.Draft202012Validator(self.schema)

    def test_vendored_bytes_match_gaia_source_pins(self) -> None:
        paths = (SCHEMA_PATH, VALID_PATH, *INVALID_PATHS)
        for path in paths:
            with self.subTest(path=path.name):
                actual = hashlib.sha256(path.read_bytes()).hexdigest()
                self.assertEqual(actual, SOURCE_SHA256[path.name])

    def test_valid_fixture_is_post_consumption_and_authority_empty(self) -> None:
        receipt = json.loads(VALID_PATH.read_text(encoding="utf-8"))
        errors = list(self.validator.iter_errors(receipt))
        self.assertEqual(errors, [])
        self.assertIn("consumptionDigest", receipt)
        self.assertIn("consumption", receipt)
        self.assertEqual(receipt["authority"]["effects"], [])

    def test_bounded_invalid_fixtures_are_rejected(self) -> None:
        for path in INVALID_PATHS:
            with self.subTest(path=path.name):
                receipt = json.loads(path.read_text(encoding="utf-8"))
                self.assertTrue(list(self.validator.iter_errors(receipt)))

    def test_receipt_digest_matches_independent_canonical_projection(self) -> None:
        receipt = json.loads(VALID_PATH.read_text(encoding="utf-8"))
        projection = {
            key: value for key, value in receipt.items() if key != "receiptDigest"
        }
        digest = hashlib.sha256(
            DOMAIN + b"\0" + canonical_bytes(projection)
        ).hexdigest()
        self.assertEqual(
            digest,
            "7222b292a29e519eb081e9ffd08fe9c8d366e857ad2243074e78750a8972128e",
        )
        self.assertEqual(digest, receipt["receiptDigest"])


if __name__ == "__main__":
    unittest.main()
