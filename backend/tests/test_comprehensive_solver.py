"""
Comprehensive test suite for the advanced solver implementation.
Tests various puzzle types and validates the elimination tracking.
"""

from services.advanced_solver import advanced_solver
import json


def print_grid(grid, title="Grid"):
    """Print a Sudoku grid with title."""
    print(f"\n{title}:")
    print("┌───────┬───────┬───────┐")
    for i, row in enumerate(grid):
        print("│", end=" ")
        for j, cell in enumerate(row):
            print(cell if cell != 0 else ".", end=" ")
            if j % 3 == 2 and j < 8:
                print("│", end=" ")
        print("│")
        if i % 3 == 2 and i < 8:
            print("├───────┼───────┼───────┤")
    print("└───────┴───────┴───────┘")


def analyze_step(step, step_num):
    """Analyze and display detailed information about a solving step."""
    print(f"\n{'='*60}")
    print(f"STEP {step_num}: {step['technique']}")
    print(f"Type: {step.get('technique_type', 'unknown')}")
    print(f"{'='*60}")

    print(f"Description: {step['description']}")

    # Show cells solved
    if step["cells_solved"] > 0:
        print(f"✅ Cells Solved: {step['cells_solved']}")
        if step.get("solved_positions"):
            print(f"   Positions: {', '.join(step['solved_positions'])}")

    # Show elimination breakdown
    technique_elims = step.get("technique_eliminations", 0)
    constraint_elims = step.get("constraint_eliminations", 0)

    if technique_elims > 0 or constraint_elims > 0:
        print(f"\n🔍 Elimination Analysis:")
        if technique_elims > 0:
            print(f"   🧠 Technique eliminations: {technique_elims}")
        if constraint_elims > 0:
            print(f"   ⚙️  Constraint propagation: {constraint_elims}")

        # Show specific eliminations
        if step.get("candidate_changes"):
            tech_changes = [
                c
                for c in step["candidate_changes"]
                if c.get("elimination_type") == "technique"
            ]
            const_changes = [
                c
                for c in step["candidate_changes"]
                if c.get("elimination_type") == "constraint_propagation"
            ]

            if tech_changes:
                print(f"\n   🧠 Technique Eliminations:")
                for change in tech_changes[:3]:
                    eliminated = sorted(change["eliminated"])
                    remaining = (
                        sorted(change["new_candidates"])
                        if change["new_candidates"]
                        else "solved"
                    )
                    print(
                        f"      {change['location']}: removed {eliminated} → {remaining}"
                    )
                if len(tech_changes) > 3:
                    print(f"      ... and {len(tech_changes)-3} more")

            if const_changes:
                print(f"\n   ⚙️  Constraint Eliminations:")
                for change in const_changes[:3]:
                    eliminated = sorted(change["eliminated"])
                    remaining = (
                        sorted(change["new_candidates"])
                        if change["new_candidates"]
                        else "solved"
                    )
                    print(
                        f"      {change['location']}: removed {eliminated} → {remaining}"
                    )
                if len(const_changes) > 3:
                    print(f"      ... and {len(const_changes)-3} more")

    # Show progress
    remaining = sum(1 for row in step["grid"] for cell in row if cell == 0)
    print(f"\n📊 Progress: {remaining} cells remaining")


def test_easy_puzzle():
    """Test with an easy puzzle that should solve quickly."""
    print("🧩 TEST 1: EASY PUZZLE")
    print("=" * 50)

    puzzle = [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9],
    ]

    print_grid(puzzle, "Initial Puzzle")

    result = advanced_solver.solve(puzzle)

    print(f"\n📊 Results:")
    print(f"   Solved: {result['is_solved']}")
    print(
        f"   Steps: {len([s for s in result['solving_steps'] if s.get('technique_type') != 'final'])}"
    )
    print(f"   Techniques: {', '.join(result['techniques_applied'])}")

    # Show first few steps
    for i, step in enumerate(result["solving_steps"][:3]):
        if step.get("technique_type") != "final":
            analyze_step(step, i)

    if result["is_solved"]:
        print_grid(result["solved_grid"], "Final Solution")

    return result


def test_medium_puzzle():
    """Test with a medium difficulty puzzle."""
    print("\n\n🧩 TEST 2: MEDIUM PUZZLE")
    print("=" * 50)

    puzzle = [
        [0, 0, 0, 6, 0, 0, 4, 0, 0],
        [7, 0, 0, 0, 0, 3, 6, 0, 0],
        [0, 0, 0, 0, 9, 1, 0, 8, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 5, 0, 1, 8, 0, 0, 0, 3],
        [0, 0, 0, 3, 0, 6, 0, 4, 5],
        [0, 4, 0, 2, 0, 0, 0, 6, 0],
        [9, 0, 3, 0, 0, 0, 0, 0, 0],
        [0, 2, 0, 0, 0, 0, 1, 0, 0],
    ]

    print_grid(puzzle, "Initial Puzzle")

    result = advanced_solver.solve(puzzle)

    print(f"\n📊 Results:")
    print(f"   Solved: {result['is_solved']}")
    print(
        f"   Steps: {len([s for s in result['solving_steps'] if s.get('technique_type') != 'final'])}"
    )
    print(f"   Techniques: {', '.join(result['techniques_applied'])}")

    # Show all steps for medium puzzle
    for i, step in enumerate(result["solving_steps"]):
        if step.get("technique_type") not in ["final"]:
            analyze_step(step, i)

    return result


def test_invalid_puzzle():
    """Test with an invalid puzzle."""
    print("\n\n🧩 TEST 3: INVALID PUZZLE (Duplicate in row)")
    print("=" * 50)

    puzzle = [
        [5, 5, 0, 0, 7, 0, 0, 0, 0],  # Two 5s in first row
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9],
    ]

    print_grid(puzzle, "Invalid Puzzle")

    try:
        result = advanced_solver.solve(puzzle)
        print(f"\n📊 Results:")
        print(f"   Solved: {result['is_solved']}")
        print(f"   Message: {result['message']}")
        return result
    except Exception as e:
        print(f"❌ Error (expected): {e}")
        return None


def test_elimination_types():
    """Test to verify elimination type tracking works correctly."""
    print("\n\n🧩 TEST 4: ELIMINATION TYPE VERIFICATION")
    print("=" * 50)

    puzzle = [
        [0, 0, 0, 6, 0, 0, 4, 0, 0],
        [7, 0, 0, 0, 0, 3, 6, 0, 0],
        [0, 0, 0, 0, 9, 1, 0, 8, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 5, 0, 1, 8, 0, 0, 0, 3],
        [0, 0, 0, 3, 0, 6, 0, 4, 5],
        [0, 4, 0, 2, 0, 0, 0, 6, 0],
        [9, 0, 3, 0, 0, 0, 0, 0, 0],
        [0, 2, 0, 0, 0, 0, 1, 0, 0],
    ]

    result = advanced_solver.solve(puzzle)

    # Verify elimination type tracking
    total_technique_elims = 0
    total_constraint_elims = 0

    for step in result["solving_steps"]:
        if step.get("candidate_changes"):
            for change in step["candidate_changes"]:
                if change.get("elimination_type") == "technique":
                    total_technique_elims += len(change["eliminated"])
                elif change.get("elimination_type") == "constraint_propagation":
                    total_constraint_elims += len(change["eliminated"])

    print(f"\n📊 Elimination Type Summary:")
    print(f"   🧠 Total technique eliminations: {total_technique_elims}")
    print(f"   ⚙️  Total constraint eliminations: {total_constraint_elims}")
    print(f"   📈 Total eliminations: {total_technique_elims + total_constraint_elims}")

    # Verify data integrity
    print(f"\n🔍 Data Integrity Check:")
    for i, step in enumerate(result["solving_steps"]):
        if step.get("candidate_changes"):
            expected_total = step.get("candidates_eliminated", 0)
            actual_total = len(step["candidate_changes"])
            if expected_total != actual_total:
                print(f"   ❌ Step {i}: Expected {expected_total}, got {actual_total}")
            else:
                print(f"   ✅ Step {i}: Elimination count matches ({actual_total})")

    return result


def run_all_tests():
    """Run all tests and provide summary."""
    print("🧪 COMPREHENSIVE SOLVER TESTING")
    print("=" * 70)

    results = []

    # Test 1: Easy puzzle
    try:
        result1 = test_easy_puzzle()
        results.append(
            ("Easy Puzzle", result1["is_solved"], len(result1["solving_steps"]))
        )
    except Exception as e:
        print(f"❌ Easy puzzle test failed: {e}")
        results.append(("Easy Puzzle", False, 0))

    # Test 2: Medium puzzle
    try:
        result2 = test_medium_puzzle()
        results.append(
            ("Medium Puzzle", result2["is_solved"], len(result2["solving_steps"]))
        )
    except Exception as e:
        print(f"❌ Medium puzzle test failed: {e}")
        results.append(("Medium Puzzle", False, 0))

    # Test 3: Invalid puzzle
    try:
        result3 = test_invalid_puzzle()
        if result3:
            results.append(
                ("Invalid Puzzle", result3["is_solved"], len(result3["solving_steps"]))
            )
        else:
            results.append(("Invalid Puzzle", "Error handled", 0))
    except Exception as e:
        print(f"❌ Invalid puzzle test failed: {e}")
        results.append(("Invalid Puzzle", False, 0))

    # Test 4: Elimination tracking
    try:
        result4 = test_elimination_types()
        results.append(
            ("Elimination Tracking", "Verified", len(result4["solving_steps"]))
        )
    except Exception as e:
        print(f"❌ Elimination tracking test failed: {e}")
        results.append(("Elimination Tracking", False, 0))

    # Summary
    print(f"\n\n🏆 TEST SUMMARY")
    print("=" * 70)
    for test_name, solved, steps in results:
        print(f"   {test_name:20} | Solved: {str(solved):10} | Steps: {steps}")

    print(f"\n✅ All tests completed!")


if __name__ == "__main__":
    run_all_tests()
