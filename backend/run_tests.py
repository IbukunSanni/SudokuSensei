#!/usr/bin/env python3
"""
Simple test runner for the current stage of development.
Runs all relevant tests for the implemented techniques.
"""

import sys
import os
import subprocess

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def run_test(test_file, description):
    """Run a single test file and report results."""
    print(f"\n{'='*60}")
    print(f"🧪 {description}")
    print(f"{'='*60}")

    try:
        result = subprocess.run(
            [sys.executable, test_file],
            capture_output=True,
            text=True,
            cwd=os.path.dirname(os.path.abspath(__file__)),
        )

        if result.returncode == 0:
            print(f"✅ PASSED: {description}")
            if result.stdout:
                print(result.stdout)
        else:
            print(f"❌ FAILED: {description}")
            if result.stderr:
                print("STDERR:", result.stderr)
            if result.stdout:
                print("STDOUT:", result.stdout)

        return result.returncode == 0
    except Exception as e:
        print(f"❌ ERROR running {description}: {e}")
        return False


def main():
    """Run all relevant tests for current development stage."""
    print("🚀 RUNNING SUDOKU TECHNIQUE TESTS")
    print("=" * 70)

    tests = [
        ("tests/techniques/test_naked_single.py", "Naked Single Technique"),
        ("tests/techniques/test_hidden_single.py", "Hidden Single Technique"),
        ("tests/techniques/test_naked_pairs.py", "Naked Pairs Technique"),
        ("tests/techniques/test_hidden_pairs.py", "Hidden Pairs Technique"),
        ("tests/test_single_technique.py", "Single Technique Application"),
        ("tests/test_frontend_solver.py", "Step-by-Step Solver"),
    ]

    passed = 0
    total = len(tests)

    for test_file, description in tests:
        if os.path.exists(test_file):
            if run_test(test_file, description):
                passed += 1
        else:
            print(f"⚠️  SKIPPED: {description} (file not found: {test_file})")

    print(f"\n{'='*70}")
    print(f"📊 TEST SUMMARY")
    print(f"{'='*70}")
    print(f"✅ Passed: {passed}/{total}")
    print(f"❌ Failed: {total - passed}/{total}")

    if passed == total:
        print("🎉 ALL TESTS PASSED!")
        return 0
    else:
        print("⚠️  Some tests failed. Check output above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
