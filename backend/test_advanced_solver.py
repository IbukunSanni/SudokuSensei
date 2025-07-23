"""
Test the advanced solver that distinguishes between constraint propagation and technique eliminations.
"""

from services.advanced_solver import advanced_solver
from helpers.get_location import get_cell_location


def print_elimination_analysis(step):
    """Print detailed analysis of eliminations in a step."""
    if not step.get("candidate_changes"):
        return

    technique_elims = [
        c for c in step["candidate_changes"] if c.get("elimination_type") == "technique"
    ]
    constraint_elims = [
        c
        for c in step["candidate_changes"]
        if c.get("elimination_type") == "constraint_propagation"
    ]

    if technique_elims:
        print(f"  🧠 Technique Eliminations ({len(technique_elims)}):")
        for change in technique_elims[:3]:  # Show first 3
            print(
                f"    {change['location']}: removed {sorted(change['eliminated'])} → {sorted(change['new_candidates']) if change['new_candidates'] else 'solved'}"
            )
        if len(technique_elims) > 3:
            print(f"    ... and {len(technique_elims)-3} more technique eliminations")

    if constraint_elims:
        print(f"  ⚙️  Constraint Propagation ({len(constraint_elims)}):")
        for change in constraint_elims[:3]:  # Show first 3
            print(
                f"    {change['location']}: removed {sorted(change['eliminated'])} → {sorted(change['new_candidates']) if change['new_candidates'] else 'solved'}"
            )
        if len(constraint_elims) > 3:
            print(f"    ... and {len(constraint_elims)-3} more constraint eliminations")


def test_advanced_solver():
    """Test the advanced solver with elimination type tracking."""
    # Puzzle that will require multiple techniques
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

    print("🧩 ADVANCED SUDOKU SOLVER - ELIMINATION TYPE ANALYSIS")
    print("=" * 70)

    # Show initial puzzle
    print("\nInitial Puzzle:")
    print_grid(puzzle)

    # Solve with advanced tracking
    result = advanced_solver.solve(puzzle)

    print(f"\n📊 Solving Summary:")
    print(f"   Puzzle solved: {result['is_solved']}")
    print(
        f"   Total steps: {len([s for s in result['solving_steps'] if s.get('technique_type') != 'final'])}"
    )
    print(f"   Techniques used: {', '.join(result['techniques_applied'])}")

    print(f"\n🔍 Step-by-Step Analysis:")

    for i, step in enumerate(result["solving_steps"]):
        if step.get("technique_type") == "final":
            continue

        print(f"\n{'='*50}")
        print(f"STEP {i}: {step['technique']}")
        print(f"Type: {step.get('technique_type', 'unknown')}")
        print(f"{'='*50}")

        print(f"Description: {step['description']}")

        if step["cells_solved"] > 0:
            print(f"✅ Cells Solved: {step['cells_solved']}")
            if step.get("solved_positions"):
                positions = ", ".join(step["solved_positions"][:5])
                if len(step["solved_positions"]) > 5:
                    positions += f" +{len(step['solved_positions'])-5} more"
                print(f"   Positions: {positions}")

        # Show elimination breakdown
        technique_count = step.get("technique_eliminations", 0)
        constraint_count = step.get("constraint_eliminations", 0)

        if technique_count > 0 or constraint_count > 0:
            print(f"\n🔍 Elimination Breakdown:")
            if technique_count > 0:
                print(f"   🧠 Technique eliminations: {technique_count}")
            if constraint_count > 0:
                print(f"   ⚙️  Constraint propagation: {constraint_count}")

            print_elimination_analysis(step)

        remaining = sum(1 for row in step["grid"] for cell in row if cell == 0)
        print(f"\n📊 Progress: {remaining} cells remaining")

        if i < 3:  # Show grid for first few steps
            print(f"\nGrid after step:")
            print_grid(step["grid"])

    print(f"\n🏆 Final Result: {result['message']}")


def print_grid(grid):
    """Print a Sudoku grid in a readable format."""
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


if __name__ == "__main__":
    test_advanced_solver()
