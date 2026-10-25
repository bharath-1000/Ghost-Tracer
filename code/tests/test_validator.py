"""
Unit tests for output contract validation and schema enforcement.
"""

import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from core.validator import validate_output_file

class TestContractValidator(unittest.TestCase):
    def test_output_csv_validation(self):
        if not os.path.exists("output.csv"):
            self.skipTest("output.csv not generated yet")
        is_valid, violations = validate_output_file("output.csv", expected_count=518)
        self.assertTrue(is_valid, f"Violations encountered: {violations}")
        self.assertEqual(len(violations), 0)

    def test_sample_output_validation(self):
        if not os.path.exists("dataset/sample_output.csv"):
            self.skipTest("dataset/sample_output.csv not found")
        is_valid, violations = validate_output_file("dataset/sample_output.csv", expected_count=32)
        self.assertTrue(is_valid, f"Sample output violations: {violations}")

if __name__ == "__main__":
    unittest.main()
