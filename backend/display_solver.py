"""
Enhanced display functions for showing the step-by-step Sudoku solving process.
Provides clean, organized output with proper formatting.
"""

from services.enhanced_solver import enhanced_solver
from helpers.get_location import get_cell_location


def print_grid_with_title(grid, title="Grid State"):
    """Print a Sudoku grid with a title and nice formatting."""
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


def print_step_header(step_num, technique, cells_solved, candidates_eliminated):
    """Print a formatted header for each solving step."""
    print("\n" + "=" * 60)
    print(f"STEP {step_num}: {technique.upper()}")
    print("=" * 60)
    if cells_solved > 0:
        print(f"📍 Cells Solved: {cells_solved}")
    if candidates_eliminated > 0:
        print(f"🔍 Candidates Eliminated: {candidates_eliminated}")


def print_solved_cells(solved_positions):
    """Print the cells that were solved in this step."""
    if not solved_positions:
        return

    print(f"\n✅ Cells Filled:")
    # Group by rows for better readability
    cells_by_row = {}
    for pos in solved_positions:
        cell_loc, value = pos.split("=")
        row = cell_loc[1]  # Get row number from A1, B2, etc.
        if row not in cells_by_row:
            cells_by_row[row] = []
        cells_by_row[row].append(f"{cell_loc}={value}")

    for row in sorted(cells_by_row.keys()):
        print(f"   Row {row}: {', '.join(cells_by_row[row])}")


def print_candidate_changes(candidate_changes, max_show=8):
    """Print candidate eliminations in an organized way."""
    if not candidate_changes:
        return

    print(f"\n🔍 Candidate Eliminations:")
    for i, change in enumerate(candidate_changes[:max_show]):
        eliminated = sorted(change["eliminated"])
        remaining = sorted(change["new_candidates"])
        print(
            f"   {change['location']}: removed {eliminated} → {remaining if remaining else 'solved'}"
        )

    if len(candidate_changes) > max_show:
        print(f"   ... and {len(candidate_changes) - max_show} more eliminations")


def print_technique_summary(technique, description):
    """Print a summary of what the technique accomplished."""
    print(f"\n📋 Technique Summary:")
    print(f"   {description}")


def solve_and_display(puzzle, show_candidates=False, pause_between_steps=False):
    """
    Solve a puzzle and display the process with enhanced formatting.

    Args:
        puzzle: 9x9 grid of integers (0 for empty cells)
        show_candidates: Whether to show candidate information
        pause_between_steps: Whether to pause between steps for user input
    """
    print("🧩 SUDOKU SENSEI - STEP-BY-STEP SOLVER")
    print("=" * 60)

    # Show initial puzzle
    print_grid_with_title(puzzle, "Initial Puzzle")
    empty_count = sum(1 for row in puzzle for cell in row if cell == 0)
    print(f"\n📊 Initial Analysis: {empty_count} empty cells to solve")

    if pause_between_steps:
        input("\nPress Enter to start solving...")

    # Solve the puzzle
    result = enhanced_solver.solve(puzzle)

    # Display each step
    for i, step in enumerate(result["solving_steps"]):
        if step["technique"] == "Initial State":
            continue  # Skip initial state as we already showed it

        # Print step header
        print_step_header(
            i,
            step["technique"],
            step["cells_solved"],
            step.get("candidates_eliminated", 0),
        )

        # Print technique summary
        print_technique_summary(step["technique"], step["description"])

        # Print solved cells
        if step.get("solved_positions"):
            print_solved_cells(step["solved_positions"])

        # Print candidate changes
        if step.get("candidate_changes") and show_candidates:
            print_candidate_changes(step["candidate_changes"])

        # Print grid state
        print_grid_with_title(step["grid"], f"Grid After Step {i}")

        # Show remaining empty cells
        remaining = sum(1 for row in step["grid"] for cell in row if cell == 0)
        if remaining > 0:
            print(f"\n📊 Progress: {remaining} cells remaining")
        else:
            print(f"\n🎉 PUZZLE SOLVED!")

        if pause_between_steps and remaining > 0:
            input("\nPress Enter for next step...")

    # Final summary
    print("\n" + "=" * 60)
    print("🏆 SOLVING COMPLETE!")
    print("=" * 60)
    print(f"✅ Puzzle Solved: {result['is_solved']}")
    print(
        f"📈 Total Steps: {len([s for s in result['solving_steps'] if s['technique'] != 'Initial State'])}"
    )
    print(f"🔧 Techniques Used: {', '.join(result['techniques_applied'])}")
    print(f"💡 {result['message']}")

    return result


def solve_with_basic_display(puzzle):
    """Solve with a simpler, more compact display format."""
    print("🧩 SUDOKU SOLVER - COMPACT VIEW")
    print("=" * 50)

    result = enhanced_solver.solve(puzzle)

    print(
        f"📊 Initial: {sum(1 for row in puzzle for cell in row if cell == 0)} empty cells"
    )

    step_count = 0
    for step in result["solving_steps"]:
        if step["technique"] == "Initial State":
            continue

        step_count += 1
        cells_solved = step["cells_solved"]

        if cells_solved > 0:
            positions = step.get("solved_positions", [])
            positions_str = ", ".join(positions[:6])  # Show first 6
            if len(positions) > 6:
                positions_str += f" +{len(positions)-6} more"

            print(f"Step {step_count}: {step['technique']}")
            print(f"  ✅ Filled: {positions_str}")

            remaining = sum(1 for row in step["grid"] for cell in row if cell == 0)
            print(f"  📊 Remaining: {remaining} cells")
            print()

    print(f"🏆 Result: {result['message']}")
    return result


if __name__ == "__main__":
    # Example usage
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

    print("Choose display mode:")
    print("1. Full detailed view")
    print("2. Compact view")
    choice = input("Enter choice (1 or 2): ").strip()

    if choice == "1":
        solve_and_display(puzzle, show_candidates=True, pause_between_steps=True)
    else:
        solve_with_basic_display(puzzle)
