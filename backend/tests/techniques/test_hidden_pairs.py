"""
Test the hidden pairs technique implementation.
"""

from board.board import SudokuBoard
from logic.hidden_pairs import apply_one_hidden_pair
from helpers.get_location import get_cell_location


def make_board_with_hidden_pairs():
    """
    Create a board with a hidden pair scenario using a realistic Sudoku grid.

    This uses the provided Sudoku puzzle and creates a hidden pairs scenario
    by manually setting up candidates where needed.
    """
    # Use the realistic Sudoku grid you provided
    grid = [
        [0, 0, 9, 0, 3, 2, 0, 0, 0],
        [0, 0, 0, 7, 0, 0, 0, 0, 0],
        [1, 6, 2, 0, 0, 0, 0, 0, 0],
        [0, 0, 1, 0, 2, 0, 5, 6, 0],
        [0, 0, 0, 9, 0, 0, 0, 0, 0],
        [0, 5, 0, 0, 0, 0, 1, 0, 7],
        [0, 0, 0, 0, 0, 0, 4, 0, 3],
        [0, 2, 6, 0, 0, 9, 0, 0, 0],
        [0, 0, 5, 8, 7, 0, 0, 0, 0],
    ]

    board = SudokuBoard(grid)

    # Let the board calculate natural candidates first
    board.update_candidates()

    # Now create a hidden pair scenario in row 1 (index 0)
    # We'll set up candidates so that 4 and 8 are hidden pairs in R1C1 and R1C2

    # Set up R1C1 and R1C2 to contain the hidden pair {4, 8} plus other candidates
    board.grid[0][0].set_candidates({4, 8, 5, 7})  # Hidden pair {4,8} + others {5,7}
    board.grid[0][1].set_candidates({4, 8, 5, 6})  # Hidden pair {4,8} + others {5,6}

    # Make sure other empty cells in row 1 don't have 4 or 8 (making them "hidden")
    board.grid[0][3].set_candidates({1, 5, 6})  # R1C4 - no 4 or 8
    board.grid[0][6].set_candidates({6, 7})  # R1C7 - no 4 or 8
    board.grid[0][7].set_candidates({1, 5})  # R1C8 - no 4 or 8
    board.grid[0][8].set_candidates({1, 5, 6})  # R1C9 - no 4 or 8

    return board


def test_hidden_pairs_elimination():
    """Test that hidden pairs technique eliminates other candidates correctly."""
    board = make_board_with_hidden_pairs()

    # Before applying technique
    print("Before hidden pairs:")
    print(f"R1C1 candidates: {sorted(board.grid[0][0].get_candidates())}")
    print(f"R1C2 candidates: {sorted(board.grid[0][1].get_candidates())}")

    # Apply hidden pairs technique
    changed, step = apply_one_hidden_pair(board)

    # Should find and apply hidden pairs
    assert changed, "Expected hidden pairs technique to make changes"
    assert step is not None, "Expected a TechniqueStep to be returned"

    # After applying technique
    print("\nAfter hidden pairs:")
    print(f"R1C1 candidates: {sorted(board.grid[0][0].get_candidates())}")
    print(f"R1C2 candidates: {sorted(board.grid[0][1].get_candidates())}")

    # Both cells should now only have candidates {4, 8} (the hidden pair)
    assert board.grid[0][0].get_candidates() == {
        4,
        8,
    }, f"Expected {{4, 8}}, got {board.grid[0][0].get_candidates()}"
    assert board.grid[0][1].get_candidates() == {
        4,
        8,
    }, f"Expected {{4, 8}}, got {board.grid[0][1].get_candidates()}"

    # Check step details
    assert step.technique == "Hidden Pair"
    print(f"Focus cells count: {len(step.focus_cells)}")
    print(f"Focus cells: {step.focus_cells}")
    assert len(step.focus_cells) == 2  # Should focus on the pair cells
    assert step.eliminations  # Should have eliminations

    print(f"\nStep description: {step.description}")
    print(f"Focus cells: {step.focus_cells}")
    print(f"Eliminations: {step.eliminations}")


def test_no_hidden_pairs():
    """Test that technique returns False when no hidden pairs exist."""
    # Create a simple board with no hidden pairs
    grid = [[0 for _ in range(9)] for _ in range(9)]
    board = SudokuBoard(grid)

    # Set up candidates with no hidden pairs
    board.grid[0][0].set_candidates({1, 2, 3})
    board.grid[0][1].set_candidates({4, 5, 6})
    board.grid[0][2].set_candidates({7, 8, 9})

    # Apply technique
    changed, step = apply_one_hidden_pair(board)

    # Should not find any hidden pairs
    assert not changed, "Expected no changes when no hidden pairs exist"
    assert step is None, "Expected no step when no hidden pairs found"


if __name__ == "__main__":
    print("TESTING HIDDEN PAIRS TECHNIQUE")
    print("=" * 50)

    test_hidden_pairs_elimination()
    print("\n" + "=" * 50)
    test_no_hidden_pairs()

    print("\nAll hidden pairs tests passed!")
