"""
Test the naked triples technique implementation.
"""

from board.board import SudokuBoard
from logic.naked_triples import apply_one_naked_triple
from helpers.get_location import get_cell_location


def make_board_with_naked_triples():
    """
    Create a board with a naked triple scenario.

    In this setup, cells R1C1, R1C2, R1C3 contain candidates that form a naked triple.
    For example: {1,2}, {2,3}, {1,3} - together they contain exactly {1,2,3}
    """
    # Start with empty grid
    grid = [[0 for _ in range(9)] for _ in range(9)]
    board = SudokuBoard(grid)

    # Fill some cells to create constraints
    board.grid[0][3].set_value(4)  # R1C4 = 4
    board.grid[0][4].set_value(5)  # R1C5 = 5
    board.grid[0][5].set_value(6)  # R1C6 = 6
    board.grid[0][6].set_value(7)  # R1C7 = 7
    board.grid[0][7].set_value(8)  # R1C8 = 8
    board.grid[0][8].set_value(9)  # R1C9 = 9

    # Set up naked triple scenario in first row
    # These three cells together contain exactly candidates {1, 2, 3}
    board.grid[0][0].set_candidates({1, 2})  # R1C1: {1, 2}
    board.grid[0][1].set_candidates({2, 3})  # R1C2: {2, 3}
    board.grid[0][2].set_candidates({1, 3})  # R1C3: {1, 3}

    # Other cells in the row that should have candidates eliminated
    # These cells currently have some of {1, 2, 3} which should be removed
    # (Note: positions 3-8 are already filled, so we can't test elimination there)

    # Let's create a column scenario instead for better testing
    # Reset and create column-based naked triple
    board = SudokuBoard(grid)

    # Fill some cells in first column to create constraints
    board.grid[3][0].set_value(4)  # R4C1 = 4
    board.grid[4][0].set_value(5)  # R5C1 = 5
    board.grid[5][0].set_value(6)  # R6C1 = 6
    board.grid[6][0].set_value(7)  # R7C1 = 7
    board.grid[7][0].set_value(8)  # R8C1 = 8
    board.grid[8][0].set_value(9)  # R9C1 = 9

    # Set up naked triple in first column (R1C1, R2C1, R3C1)
    board.grid[0][0].set_candidates({1, 2})  # R1C1: {1, 2}
    board.grid[1][0].set_candidates({2, 3})  # R2C1: {2, 3}
    board.grid[2][0].set_candidates({1, 3})  # R3C1: {1, 3}

    return board


def make_simple_naked_triple_board():
    """
    Create a simpler board with naked triple for easier testing.
    """
    grid = [[0 for _ in range(9)] for _ in range(9)]
    board = SudokuBoard(grid)

    # Create a naked triple in the first row
    # Cells 0, 1, 2 will have the naked triple {1, 2, 3}
    board.grid[0][0].set_candidates({1, 2})  # Can be 1 or 2
    board.grid[0][1].set_candidates({2, 3})  # Can be 2 or 3
    board.grid[0][2].set_candidates({1, 3})  # Can be 1 or 3

    # Cell that should have candidates eliminated (contains some of {1,2,3})
    board.grid[0][3].set_candidates({1, 4, 5})  # Should lose 1
    board.grid[0][4].set_candidates({2, 6, 7})  # Should lose 2
    board.grid[0][5].set_candidates({3, 8, 9})  # Should lose 3
    board.grid[0][6].set_candidates({1, 2, 3, 4})  # Should lose 1, 2, 3

    # Other cells without the triple candidates (should be unchanged)
    board.grid[0][7].set_candidates({4, 5, 6})  # Should remain unchanged
    board.grid[0][8].set_candidates({7, 8, 9})  # Should remain unchanged

    return board


def test_naked_triples_elimination():
    """Test that naked triples technique eliminates candidates correctly."""
    board = make_simple_naked_triple_board()

    # Before applying technique
    print("Before naked triples:")
    print(f"R1C1 candidates: {sorted(board.grid[0][0].get_candidates())}")  # {1, 2}
    print(f"R1C2 candidates: {sorted(board.grid[0][1].get_candidates())}")  # {2, 3}
    print(f"R1C3 candidates: {sorted(board.grid[0][2].get_candidates())}")  # {1, 3}
    print(f"R1C4 candidates: {sorted(board.grid[0][3].get_candidates())}")  # {1, 4, 5}
    print(f"R1C5 candidates: {sorted(board.grid[0][4].get_candidates())}")  # {2, 6, 7}
    print(f"R1C6 candidates: {sorted(board.grid[0][5].get_candidates())}")  # {3, 8, 9}
    print(
        f"R1C7 candidates: {sorted(board.grid[0][6].get_candidates())}"
    )  # {1, 2, 3, 4}

    # Apply naked triples technique
    changed, step = apply_one_naked_triple(board)

    # Should find and apply naked triples
    assert changed, "Expected naked triples technique to make changes"
    assert step is not None, "Expected a TechniqueStep to be returned"

    # After applying technique
    print("\nAfter naked triples:")
    print(
        f"R1C1 candidates: {sorted(board.grid[0][0].get_candidates())}"
    )  # Should remain {1, 2}
    print(
        f"R1C2 candidates: {sorted(board.grid[0][1].get_candidates())}"
    )  # Should remain {2, 3}
    print(
        f"R1C3 candidates: {sorted(board.grid[0][2].get_candidates())}"
    )  # Should remain {1, 3}
    print(
        f"R1C4 candidates: {sorted(board.grid[0][3].get_candidates())}"
    )  # Should become {4, 5}
    print(
        f"R1C5 candidates: {sorted(board.grid[0][4].get_candidates())}"
    )  # Should become {6, 7}
    print(
        f"R1C6 candidates: {sorted(board.grid[0][5].get_candidates())}"
    )  # Should become {8, 9}
    print(
        f"R1C7 candidates: {sorted(board.grid[0][6].get_candidates())}"
    )  # Should become {4}

    # Verify eliminations
    assert board.grid[0][3].get_candidates() == {
        4,
        5,
    }, f"R1C4 should be {{4, 5}}, got {board.grid[0][3].get_candidates()}"
    assert board.grid[0][4].get_candidates() == {
        6,
        7,
    }, f"R1C5 should be {{6, 7}}, got {board.grid[0][4].get_candidates()}"
    assert board.grid[0][5].get_candidates() == {
        8,
        9,
    }, f"R1C6 should be {{8, 9}}, got {board.grid[0][5].get_candidates()}"
    assert board.grid[0][6].get_candidates() == {
        4
    }, f"R1C7 should be {{4}}, got {board.grid[0][6].get_candidates()}"

    # Triple cells should remain unchanged
    assert board.grid[0][0].get_candidates() == {
        1,
        2,
    }, f"R1C1 should remain {{1, 2}}, got {board.grid[0][0].get_candidates()}"
    assert board.grid[0][1].get_candidates() == {
        2,
        3,
    }, f"R1C2 should remain {{2, 3}}, got {board.grid[0][1].get_candidates()}"
    assert board.grid[0][2].get_candidates() == {
        1,
        3,
    }, f"R1C3 should remain {{1, 3}}, got {board.grid[0][2].get_candidates()}"

    # Check step details
    assert step.technique == "Naked Triple"
    print(f"Focus cells count: {len(step.focus_cells)}")
    print(f"Focus cells: {step.focus_cells}")
    assert len(step.focus_cells) == 3  # Should focus on the triple cells
    assert step.eliminations  # Should have eliminations

    print(f"\nStep description: {step.description}")
    print(f"Focus cells: {step.focus_cells}")
    print(f"Eliminations: {step.eliminations}")


def test_no_naked_triples():
    """Test that technique returns False when no naked triples exist."""
    # Create a simple board with no naked triples
    grid = [[0 for _ in range(9)] for _ in range(9)]
    board = SudokuBoard(grid)

    # Set up candidates with no naked triples
    board.grid[0][0].set_candidates({1, 2, 3})
    board.grid[0][1].set_candidates({4, 5, 6})
    board.grid[0][2].set_candidates({7, 8, 9})

    # Apply technique
    changed, step = apply_one_naked_triple(board)

    # Should not find any naked triples
    assert not changed, "Expected no changes when no naked triples exist"
    assert step is None, "Expected no step when no naked triples found"


def test_naked_triples_different_patterns():
    """Test naked triples with different candidate patterns."""
    grid = [[0 for _ in range(9)] for _ in range(9)]
    board = SudokuBoard(grid)

    # Pattern 1: {1,2,3}, {1,2}, {3} - still a valid naked triple
    board.grid[0][0].set_candidates({1, 2, 3})  # All three candidates
    board.grid[0][1].set_candidates({1, 2})  # Two of the candidates
    board.grid[0][2].set_candidates({3})  # One of the candidates

    # Cell that should be affected
    board.grid[0][3].set_candidates({1, 4, 5})  # Should lose 1

    # Apply technique
    changed, step = apply_one_naked_triple(board)

    # Should find the naked triple
    assert changed, "Expected to find naked triple with mixed pattern"
    assert step is not None
    assert board.grid[0][3].get_candidates() == {4, 5}, "Should eliminate 1 from R1C4"

    print("Mixed pattern naked triple test passed")


if __name__ == "__main__":
    print("TESTING NAKED TRIPLES TECHNIQUE")
    print("=" * 50)

    test_naked_triples_elimination()
    print("\n" + "=" * 50)
    test_no_naked_triples()
    print("\n" + "=" * 50)
    test_naked_triples_different_patterns()

    print("\nAll naked triples tests passed!")
