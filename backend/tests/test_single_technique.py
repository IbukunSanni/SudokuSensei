"""
Test individual technique applications to verify single-step behavior.
"""

from board.board import SudokuBoard
from logic.naked_single import apply_one_naked_single
from logic.hidden_single import apply_one_hidden_single
from logic.naked_pairs import apply_one_naked_pair
from logic.hidden_pairs import apply_one_hidden_pair


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


def test_single_naked_single():
    """Test applying one naked single technique."""
    print("🧩 TESTING SINGLE NAKED SINGLE APPLICATION")
    print("=" * 50)

    # Create a puzzle with a naked single
    puzzle = [
        [1, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 2, 3, 4, 5, 6, 7, 8, 9],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
    ]

    board = SudokuBoard(puzzle)
    board.update_candidates()

    print_grid([[cell.get_value() for cell in row] for row in board.grid], "Before")

    # Check candidates for cell [0][1] - should only have candidate 9
    candidates = board.grid[0][1].get_candidates()
    print(f"Candidates for R1C2: {sorted(candidates)}")

    # Apply one naked single
    changed, step = apply_one_naked_single(board)

    print(f"\nTechnique applied: {changed}")
    if step:
        print(f"Technique: {step.technique}")
        print(f"Description: {step.description}")
        print(f"Focus cells: {step.focus_cells}")
        print(f"Value placed: {step.value}")

    print_grid([[cell.get_value() for cell in row] for row in board.grid], "After")


def test_single_hidden_single():
    """Test applying one hidden single technique."""
    print("\n\n🧩 TESTING SINGLE HIDDEN SINGLE APPLICATION")
    print("=" * 50)

    # Create a puzzle with a hidden single
    puzzle = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 2, 3, 4, 5, 6, 7, 8, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
    ]

    board = SudokuBoard(puzzle)
    board.update_candidates()

    print_grid([[cell.get_value() for cell in row] for row in board.grid], "Before")

    # Apply one hidden single
    changed, step = apply_one_hidden_single(board)

    print(f"\nTechnique applied: {changed}")
    if step:
        print(f"Technique: {step.technique}")
        print(f"Description: {step.description}")
        print(f"Focus cells: {step.focus_cells}")
        print(f"Value placed: {step.value}")

    print_grid([[cell.get_value() for cell in row] for row in board.grid], "After")


def test_single_naked_pair():
    """Test applying one naked pair technique."""
    print("\n\n🧩 TESTING SINGLE NAKED PAIR APPLICATION")
    print("=" * 50)

    # Create a puzzle with naked pairs
    puzzle = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
    ]

    board = SudokuBoard(puzzle)

    # Manually set up a naked pair scenario
    # Set cells [0][0] and [0][1] to have candidates {1, 2}
    # Set cell [0][2] to have candidates {1, 2, 3}
    board.grid[0][0].set_candidates({1, 2})
    board.grid[0][1].set_candidates({1, 2})
    board.grid[0][2].set_candidates({1, 2, 3})

    print("Before naked pair application:")
    print(f"R1C1 candidates: {sorted(board.grid[0][0].get_candidates())}")
    print(f"R1C2 candidates: {sorted(board.grid[0][1].get_candidates())}")
    print(f"R1C3 candidates: {sorted(board.grid[0][2].get_candidates())}")

    # Apply one naked pair
    changed, step = apply_one_naked_pair(board)

    print(f"\nTechnique applied: {changed}")
    if step:
        print(f"Technique: {step.technique}")
        print(f"Description: {step.description}")
        print(f"Focus cells: {step.focus_cells}")
        print(f"Eliminations: {step.eliminations}")

    print("\nAfter naked pair application:")
    print(f"R1C1 candidates: {sorted(board.grid[0][0].get_candidates())}")
    print(f"R1C2 candidates: {sorted(board.grid[0][1].get_candidates())}")
    print(f"R1C3 candidates: {sorted(board.grid[0][2].get_candidates())}")


def test_technique_sequence():
    """Test applying techniques in sequence to see single-step behavior."""
    print("\n\n🧩 TESTING TECHNIQUE SEQUENCE")
    print("=" * 50)

    puzzle = [
        [0, 0, 0, 0, 3, 0, 0, 0, 8],
        [0, 4, 2, 0, 0, 0, 6, 0, 0],
        [6, 0, 9, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 5, 7, 0, 0, 4],
        [3, 0, 0, 0, 0, 0, 0, 0, 7],
        [2, 0, 0, 9, 4, 0, 0, 6, 0],
        [0, 0, 5, 0, 0, 3, 2, 0, 1],
        [0, 0, 1, 0, 0, 0, 0, 7, 0],
        [0, 0, 0, 0, 2, 0, 0, 0, 0],
    ]

    board = SudokuBoard(puzzle)
    board.update_candidates()

    print_grid([[cell.get_value() for cell in row] for row in board.grid], "Initial")

    techniques = [
        ("Naked Single", apply_one_naked_single),
        ("Hidden Single", apply_one_hidden_single),
        ("Naked Pair", apply_one_naked_pair),
        ("Hidden Pair", apply_one_hidden_pair),
    ]

    step_count = 0
    for i in range(5):  # Try up to 5 iterations
        print(f"\n--- Iteration {i+1} ---")

        for technique_name, technique_func in techniques:
            changed, step = technique_func(board)

            if changed and step:
                step_count += 1
                print(f"✅ Step {step_count}: {technique_name}")
                print(f"   {step.description}")

                if step.value:
                    print(f"   Filled cell with value {step.value}")

                if step.eliminations:
                    elim_count = sum(
                        len(positions)
                        for elim in step.eliminations
                        for positions in elim.values()
                    )
                    print(f"   Eliminated {elim_count} candidates")

                # Apply constraint propagation
                board.update_candidates()

                # Show current state
                remaining = sum(
                    1 for row in board.grid for cell in row if not cell.is_solved()
                )
                print(f"   {remaining} cells remaining")

                # Only apply one technique per iteration
                break
        else:
            print("No technique could be applied")
            break

    print_grid([[cell.get_value() for cell in row] for row in board.grid], "Final")


if __name__ == "__main__":
    test_single_naked_single()
    test_single_hidden_single()
    test_single_naked_pair()
    test_technique_sequence()
