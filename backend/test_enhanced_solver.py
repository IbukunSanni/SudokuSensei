"""
Test script to demonstrate the enhanced solver with candidate tracking.
"""

import json
from services.enhanced_solver import enhanced_solver


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


def print_candidates(candidates_grid, row, col):
    """Print candidates for a specific cell."""
    candidates = candidates_grid[row][col]
    if not candidates:
        print(f"  No candidates")
        return

    print(f"  Candidates: {sorted(candidates)}")


def test_enhanced_solver():
    """Test the enhanced solver with candidate tracking."""
    # Example puzzle (0 represents empty cells)
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

    print("Starting puzzle:")
    print_grid(puzzle)
    print("\nSolving puzzle with enhanced solver...\n")

    result = enhanced_solver.solve(puzzle)

    print(f"Puzzle solved: {result['is_solved']}")
    print(f"Message: {result['message']}")
    print(f"Techniques applied: {', '.join(result['techniques_applied'])}")
    print(f"Total steps: {len(result['solving_steps'])}")

    print("\nStep-by-step solving process:")
    for i, step in enumerate(result["solving_steps"]):
        print(f"\nStep {i}: {step['technique']}")
        print(f"Description: {step['description']}")
        print(f"Cells solved: {step['cells_solved']}")
        print(f"Candidates eliminated: {step.get('candidates_eliminated', 0)}")

        if step.get("candidate_changes"):
            print("Candidate changes:")
            for change in step["candidate_changes"][:5]:  # Limit to first 5 for brevity
                print(
                    f"  {change['location']}: {sorted(change['old_candidates'])} → {sorted(change['new_candidates'])}"
                )
            if len(step["candidate_changes"]) > 5:
                print(f"  ... and {len(step['candidate_changes'])-5} more changes")

        print("Grid state:")
        print_grid(step["grid"])

        # Show candidates for a few cells as example
        if (
            step.get("candidates") and i < 2
        ):  # Only for first few steps to avoid clutter
            print("Sample candidates:")
            for r, c in [(0, 2), (1, 1), (2, 0)]:  # Sample positions
                if step["grid"][r][c] == 0:  # Only show for unsolved cells
                    print(f"  R{r+1}C{c+1}:", end=" ")
                    print_candidates(step["candidates"], r, c)

        print("-" * 60)

    print("\nFinal grid:")
    print_grid(result["solved_grid"])


if __name__ == "__main__":
    test_enhanced_solver()
