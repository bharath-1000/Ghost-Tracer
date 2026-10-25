#!/usr/bin/env python3
"""
Test runner script for GHOST TRACER test suites.
"""

import os
import sys
import unittest

def main():
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    sys.path.insert(0, root_dir)
    sys.path.insert(0, os.path.join(root_dir, "code"))

    loader = unittest.TestLoader()
    start_dir = os.path.join(root_dir, "code", "tests")
    suite = loader.discover(start_dir, pattern="test_*.py")

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    print("\n" + "=" * 60)
    print(f" Tests Run:   {result.testsRun}")
    print(f" Errors:      {len(result.errors)}")
    print(f" Failures:    {len(result.failures)}")
    print("=" * 60)

    sys.exit(0 if result.wasSuccessful() else 1)

if __name__ == "__main__":
    main()
