import unittest
import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, ".."))
if PARENT_DIR not in sys.path: sys.path.insert(0, PARENT_DIR)

print("=== RUNNING FULL CATHEDRAL-ENGINE SYSTEM DIAGNOSTIC ===")
loader = unittest.TestLoader()
suite = loader.discover(start_dir=os.path.join(PARENT_DIR, "tests"), pattern="test_*.py")
runner = unittest.TextTestRunner(verbosity=2)
result = runner.run(suite)

if result.wasSuccessful():
    print("\nSYSTEM DIAGNOSTIC STATUS: 100% PASS (ALL UNITS STABLE)")
else:
    print("\nSYSTEM DIAGNOSTIC STATUS: FAILURES DETECTED")
