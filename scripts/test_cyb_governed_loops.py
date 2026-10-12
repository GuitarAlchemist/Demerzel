"""Regression checks for the CYB-023 offline receipt-chain exercise."""

import importlib.util
import pathlib
import unittest


MODULE_PATH = pathlib.Path(__file__).parent / "course-exercises" / "cyb_governed_loops.py"
SPEC = importlib.util.spec_from_file_location("cyb_governed_loops", MODULE_PATH)
assert SPEC and SPEC.loader
cyb_governed_loops = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(cyb_governed_loops)


class ReceiptChainTests(unittest.TestCase):
    def test_valid_chain_passes(self):
        artifact = {"answer": [2, 4], "checker": "exact-v1"}
        self.assertTrue(cyb_governed_loops.verify_chain(cyb_governed_loops.make_chain(artifact), artifact))

    def test_missing_verification_field_rejects_even_with_matching_hash(self):
        artifact = {"answer": [2, 4], "checker": "exact-v1"}
        chain = cyb_governed_loops.make_chain(artifact)
        del chain[-1]["verification_passed"]
        final_without_hash = {key: value for key, value in chain[-1].items() if key != "hash"}
        chain[-1]["hash"] = cyb_governed_loops.digest(final_without_hash)

        self.assertFalse(cyb_governed_loops.verify_chain(chain, artifact))


if __name__ == "__main__":
    unittest.main()
