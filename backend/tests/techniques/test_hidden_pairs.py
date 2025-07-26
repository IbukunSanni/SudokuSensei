"""
Test the hidden pairs technique implementation.
"""

from board.board import SudokuBoard
from logic.hidden_pairs import apply_one_hidden_pair
from helpers.get_location import get_cell_location


def make_board_with_hidden_pairs():
    """
    Create a board with a hidden pair scenario.

    In this setup, candidates 1 and 2 appear only in cells R1C1 and R1C2
    within the first row, making them a hidden pair.
    """
    # Start with empty grid
    grid = [[0 for _ in range(9)] for _ in range(9)]
    board = SudokuBoard(grid)

    # Set up a scenario where 1 and 2 are hidden pairs in R1C1 and R1C2
    # Fill some cells to create constraints
    board.grid[0][2].set_value(3)  # R1C3 = 3
    board.grid[0][3].set_value(4)  # R1C4 = 4
    board.grid[0][4].set_value(5)  # R1C5 = 5
    board.grid[0][5].set_value(6)  # R1C6 = 6
    board.grid[0][6].set_value(7)  # R1C7 = 7
    board.grid[0][7].set_value(8)  # R1C8 = 8
    board.grid[0][8].set_value(9)  # R1C9 = 9

    # Set up candidates manually to create hidden pair scenario
    # R1C1 and R1C2 should have candidates {1, 2} plus some others
    # But 1 and 2 should only appear in these two cells in the row
    board.grid[0][0].set_candidates({1, 2, 3, 4})  # Will be reduced to {1, 2}
    board.grid[0][1].set_candidates({1, 2, 5, 6})  # Will be reduced to {1, 2}

    # Other cells in row should not have 1 or 2 as candidates
    # (they're already filled with 3-9)

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

    # Both cells should now only have candidates {1, 2}
    assert board.grid[0][0].get_candidates() == {
        1,
        2,
    }, f"Expected {{1, 2}}, got {board.grid[0][0].get_candidates()}"
    assert board.grid[0][1].get_candidates() == {
        1,
        2,
    }, f"Expected {{1, 2}}, got {board.grid[0][1].get_candidates()}"

    # Check step details
    assert step.technique == "Hidden Pair"
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
    print("🧩 TESTING HIDDEN PAIRS TECHNIQUE")
    print("=" * 50)

    test_hidden_pairs_elimination()
    print("\n" + "=" * 50)
    test_no_hidden_pairs()

    print("\n✅ All hidden pairs tests passed!")
